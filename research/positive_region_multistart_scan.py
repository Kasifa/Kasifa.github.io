#!/usr/bin/env python3
"""Generate positive stationary candidates on the compactified R0.20 cube.

This script reads the exact cache produced by
``positive_region_stationary_audit.py`` and evaluates the saturated stationary
system in its *direct* tensor-product Bernstein form.  If

    p = u/(1-u),  q = v/(1-v),  x = w/(1-w),

then an original monomial ``c p^i q^j x^k`` becomes

    c u^i (1-u)^(d_p-i)
      v^j (1-v)^(d_q-j)
      w^k (1-w)^(d_x-k).

Consequently its degree-``d`` Bernstein coefficient is obtained by dividing
``c`` by the three binomial coefficients.  Constructing these coefficients
directly is important: expanding the compact polynomial in the power basis
causes severe cancellation near the R0.18 root.

Scrambled Sobol points are refined by a row-scaled, trust-region Newton method
inside the open unit cube.  Batch checkpoints make the scan resumable.  This
is a deterministic candidate generator, not a proof that every positive root
has been found.  Completeness and uniqueness require interval or exact
certificates after candidate generation.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
from fractions import Fraction
import gzip
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import sys
import time

import numpy as np
from scipy.optimize import root
from scipy.stats import qmc


SYSTEM_NAMES = (
    "saturated_stationary_p",
    "saturated_stationary_q",
    "saturated_stationary_x",
)
R018_COMPACT_ROOT = np.array(
    [
        0.8643125563687636,
        0.8498270084303075,
        0.7238258979292568,
    ],
    dtype=np.float64,
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def emit_progress(run_dir: Path, stage: str, **fields: object) -> None:
    record = {
        "timestampUtc": datetime.now(timezone.utc).isoformat(),
        "stage": stage,
        **fields,
    }
    line = json.dumps(record, ensure_ascii=False, separators=(",", ":"))
    with (run_dir / "progress.ndjson").open("a", encoding="utf-8") as stream:
        stream.write(line + "\n")
        stream.flush()
    print(line, file=sys.stderr, flush=True)


def load_exact_cache(path: Path) -> dict[str, object]:
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        cache = json.load(stream)
    if cache.get("schemaVersion") != 2:
        raise ValueError("R0.20 exact cache schema version 2 is required")
    missing = [
        name for name in SYSTEM_NAMES if name not in cache.get("polynomials", {})
    ]
    if missing:
        raise ValueError(f"exact cache is missing {missing}")
    return cache


def direct_bernstein_tensor(
    rows: list[list[object]],
) -> tuple[np.ndarray, str]:
    degrees = tuple(max(int(row[axis]) for row in rows) for axis in range(3))
    exact_entries: list[tuple[tuple[int, int, int], Fraction]] = []
    for row in rows:
        powers = tuple(int(row[axis]) for axis in range(3))
        coefficient = Fraction(int(row[3]), int(row[4]))
        divisor = math.prod(
            math.comb(degrees[axis], powers[axis]) for axis in range(3)
        )
        exact_entries.append((powers, coefficient / divisor))
    scale = max(abs(coefficient) for _powers, coefficient in exact_entries)
    tensor = np.zeros(tuple(degree + 1 for degree in degrees), dtype=np.float64)
    for powers, coefficient in exact_entries:
        value = float(coefficient / scale)
        if value == 0.0 and coefficient != 0:
            raise FloatingPointError("a Bernstein coefficient underflowed")
        tensor[powers] = value
    return tensor, str(scale)


def bernstein_basis(degree: int, values: np.ndarray) -> np.ndarray:
    indices = np.arange(degree + 1)
    binomials = np.array(
        [math.comb(degree, int(index)) for index in indices],
        dtype=np.float64,
    )
    return (
        binomials[None, :]
        * values[:, None] ** indices[None, :]
        * (1.0 - values[:, None]) ** (degree - indices)[None, :]
    )


def derivative_tensor(tensor: np.ndarray, axis: int) -> np.ndarray:
    return (tensor.shape[axis] - 1) * np.diff(tensor, axis=axis)


class BernsteinSystem:
    def __init__(self, tensors: list[np.ndarray]):
        self.tensors = tensors
        self.jacobian_tensors = [
            [derivative_tensor(tensor, axis) for axis in range(3)]
            for tensor in tensors
        ]

    @staticmethod
    def _value(tensor: np.ndarray, points: np.ndarray) -> np.ndarray:
        bases = [
            bernstein_basis(tensor.shape[axis] - 1, points[:, axis])
            for axis in range(3)
        ]
        return np.einsum(
            "ni,nj,nk,ijk->n",
            bases[0],
            bases[1],
            bases[2],
            tensor,
            optimize=True,
        )

    def evaluate(self, points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        functions = np.column_stack(
            [self._value(tensor, points) for tensor in self.tensors]
        )
        jacobian = np.stack(
            [
                np.column_stack(
                    [self._value(tensor, points) for tensor in row]
                )
                for row in self.jacobian_tensors
            ],
            axis=1,
        )
        return functions, jacobian


def newton_batch(
    system: BernsteinSystem,
    initial: np.ndarray,
    iterations: int,
    trust_radius: float,
    run_dir: Path,
    batch_index: int,
) -> tuple[np.ndarray, dict[str, int]]:
    points = initial.copy()
    active = np.ones(len(points), dtype=bool)
    converged = np.zeros(len(points), dtype=bool)
    singular = np.zeros(len(points), dtype=bool)
    stalled = np.zeros(len(points), dtype=bool)
    for iteration in range(iterations):
        active_indices = np.flatnonzero(active)
        if not len(active_indices):
            break
        current = points[active_indices]
        functions, jacobian = system.evaluate(current)
        row_scales = np.maximum(
            np.max(np.abs(jacobian), axis=2),
            np.abs(functions),
        )
        row_scales = np.maximum(row_scales, 1.0e-300)
        scaled_functions = functions / row_scales
        scaled_jacobian = jacobian / row_scales[:, :, None]
        determinants = np.linalg.det(scaled_jacobian)
        regular = (
            np.isfinite(determinants)
            & (np.abs(determinants) > 1.0e-12)
            & np.all(np.isfinite(scaled_functions), axis=1)
        )
        irregular_indices = active_indices[~regular]
        active[irregular_indices] = False
        singular[irregular_indices] = True
        if np.any(regular):
            indices = active_indices[regular]
            regular_points = current[regular]
            delta = np.linalg.solve(
                scaled_jacobian[regular],
                -scaled_functions[regular, :, None],
            )[..., 0]
            step_norm = np.max(np.abs(delta), axis=1)
            residual_norm = np.max(np.abs(scaled_functions[regular]), axis=1)
            finished = (step_norm < 1.0e-10) & (residual_norm < 1.0e-10)
            converged[indices[finished]] = True
            active[indices[finished]] = False

            moving_indices = indices[~finished]
            moving_points = regular_points[~finished]
            moving_delta = delta[~finished]
            moving_norm = step_norm[~finished]
            if len(moving_indices):
                moving_delta *= np.minimum(
                    1.0,
                    trust_radius / np.maximum(moving_norm, 1.0e-300),
                )[:, None]
                positive = moving_delta > 0
                negative = moving_delta < 0
                limits = np.where(
                    positive,
                    (1.0 - 1.0e-12 - moving_points) / moving_delta,
                    np.where(
                        negative,
                        (1.0e-12 - moving_points) / moving_delta,
                        np.inf,
                    ),
                )
                damping = np.minimum(1.0, 0.9 * np.min(limits, axis=1))
                damping = np.maximum(damping, 0.0)
                points[moving_indices] = (
                    moving_points + damping[:, None] * moving_delta
                )
                stopped = (
                    (damping < 1.0e-12)
                    | ~np.all(np.isfinite(points[moving_indices]), axis=1)
                )
                active[moving_indices[stopped]] = False
                stalled[moving_indices[stopped]] = True
        if (iteration + 1) % 10 == 0 or iteration + 1 == iterations:
            emit_progress(
                run_dir,
                "Newton batch iteration",
                batch=batch_index,
                iteration=iteration + 1,
                iterations=iterations,
                active=int(np.count_nonzero(active)),
                converged=int(np.count_nonzero(converged)),
                singular=int(np.count_nonzero(singular)),
                stalled=int(np.count_nonzero(stalled)),
            )
    return points[converged], {
        "starts": len(points),
        "converged": int(np.count_nonzero(converged)),
        "singular": int(np.count_nonzero(singular)),
        "stalled": int(np.count_nonzero(stalled)),
        "iterationLimit": int(np.count_nonzero(active)),
    }


def checkpoint_path(run_dir: Path, batch_index: int) -> Path:
    return run_dir / "checkpoints" / f"batch-{batch_index:04d}.npz"


def write_checkpoint(
    path: Path,
    roots: np.ndarray,
    statistics: dict[str, int],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("wb") as stream:
        np.savez_compressed(
            stream,
            roots=roots,
            statistics=np.array(
                [
                    statistics["starts"],
                    statistics["converged"],
                    statistics["singular"],
                    statistics["stalled"],
                    statistics["iterationLimit"],
                ],
                dtype=np.int64,
            ),
        )
    os.replace(temporary, path)


def load_checkpoint(path: Path) -> tuple[np.ndarray, dict[str, int]]:
    with np.load(path) as data:
        roots = data["roots"]
        values = data["statistics"]
    keys = ("starts", "converged", "singular", "stalled", "iterationLimit")
    return roots, {key: int(value) for key, value in zip(keys, values, strict=True)}


def cluster_and_polish(
    system: BernsteinSystem,
    roots: np.ndarray,
    cluster_tolerance: float = 1.0e-7,
) -> list[dict[str, object]]:
    if not len(roots):
        return []
    keys = np.round(roots / cluster_tolerance).astype(np.int64)
    unique_keys, inverse, counts = np.unique(
        keys,
        axis=0,
        return_inverse=True,
        return_counts=True,
    )
    representatives = np.vstack(
        [roots[np.flatnonzero(inverse == index)[0]] for index in range(len(counts))]
    )

    def function(point: np.ndarray) -> np.ndarray:
        values, _jacobian = system.evaluate(point[None, :])
        return values[0]

    def jacobian(point: np.ndarray) -> np.ndarray:
        _values, value = system.evaluate(point[None, :])
        return value[0]

    polished: list[dict[str, object]] = []
    for representative, basin_count in zip(representatives, counts, strict=True):
        result = root(
            function,
            representative,
            jac=jacobian,
            method="hybr",
            options={"xtol": 1.0e-11, "maxfev": 400},
        )
        # A small scaled residual alone is not enough near a compactification
        # face: the saturated system can decay toward a boundary without
        # having an interior zero.  Only a successful interior polish is
        # admitted to the positive-root candidate table.
        if not result.success:
            continue
        point = np.asarray(result.x, dtype=np.float64)
        if not np.all((point > 0.0) & (point < 1.0)):
            continue
        values, derivative = system.evaluate(point[None, :])
        row_scales = np.maximum(
            np.max(np.abs(derivative[0]), axis=1),
            np.abs(values[0]),
        )
        scaled_residual = float(
            np.max(np.abs(values[0] / np.maximum(row_scales, 1.0e-300)))
        )
        if scaled_residual > 1.0e-8:
            continue
        matched = None
        for existing in polished:
            if np.max(np.abs(point - existing["compact"])) < 1.0e-8:
                matched = existing
                break
        if matched is not None:
            matched["basinCount"] += int(basin_count)
            if scaled_residual < matched["scaledResidual"]:
                matched["compact"] = point
                matched["scaledResidual"] = scaled_residual
            continue
        physical = point / (1.0 - point)
        polished.append(
            {
                "compact": point,
                "physical": physical,
                "basinCount": int(basin_count),
                "scaledResidual": scaled_residual,
                "normalizedJacobianDeterminant": float(
                    np.linalg.det(
                        derivative[0]
                        / np.maximum(row_scales, 1.0e-300)[:, None]
                    )
                ),
                "scipySuccess": bool(result.success),
            }
        )
    polished.sort(key=lambda item: tuple(item["physical"]))
    return polished


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", required=True, type=Path)
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--power", type=int, default=18)
    parser.add_argument("--batch-power", type=int, default=15)
    parser.add_argument("--iterations", type=int, default=60)
    parser.add_argument("--seed", type=int, default=20260817)
    parser.add_argument("--trust-radius", type=float, default=0.2)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--no-resume", action="store_true")
    arguments = parser.parse_args()
    if not 1 <= arguments.batch_power <= arguments.power:
        parser.error("batch power must lie between 1 and the total power")
    if arguments.iterations <= 0:
        parser.error("iterations must be positive")
    if not 0 < arguments.trust_radius < 1:
        parser.error("trust radius must lie between zero and one")
    if arguments.workers <= 0:
        parser.error("workers must be positive")
    return arguments


def main() -> None:
    arguments = parse_arguments()
    started = time.perf_counter()
    run_dir = arguments.run_dir.resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    cache_path = arguments.cache.resolve()
    config = {
        "schemaVersion": 1,
        "cache": str(cache_path),
        "cacheSha256": sha256_file(cache_path),
        "power": arguments.power,
        "batchPower": arguments.batch_power,
        "iterations": arguments.iterations,
        "seed": arguments.seed,
        "trustRadius": arguments.trust_radius,
        "workers": arguments.workers,
        "coordinateMap": "p=u/(1-u), q=v/(1-v), x=w/(1-w)",
    }
    config_path = run_dir / "config.json"
    if config_path.exists():
        existing = json.loads(config_path.read_text(encoding="utf-8"))
        if existing != config:
            raise ValueError("run directory contains a different configuration")
    else:
        atomic_json(config_path, config)

    emit_progress(run_dir, "loading exact saturated system")
    cache = load_exact_cache(cache_path)
    tensors: list[np.ndarray] = []
    scales: dict[str, str] = {}
    for name in SYSTEM_NAMES:
        tensor, scale = direct_bernstein_tensor(cache["polynomials"][name])
        tensors.append(tensor)
        scales[name] = scale
    system = BernsteinSystem(tensors)
    emit_progress(
        run_dir,
        "direct Bernstein system completed",
        shapes=[list(tensor.shape) for tensor in tensors],
    )

    total_starts = 2**arguments.power
    batch_size = 2**arguments.batch_power
    sequence = qmc.Sobol(d=3, scramble=True, seed=arguments.seed).random_base2(
        arguments.power
    )
    batch_count = math.ceil(total_starts / batch_size)
    roots_by_batch: dict[int, np.ndarray] = {}
    totals = {
        "starts": 0,
        "converged": 0,
        "singular": 0,
        "stalled": 0,
        "iterationLimit": 0,
    }
    pending: list[tuple[int, np.ndarray, Path]] = []
    completed_batches = 0
    for batch_index in range(1, batch_count + 1):
        begin = (batch_index - 1) * batch_size
        end = min(batch_index * batch_size, total_starts)
        checkpoint = checkpoint_path(run_dir, batch_index)
        if checkpoint.exists() and not arguments.no_resume:
            roots, statistics = load_checkpoint(checkpoint)
            roots_by_batch[batch_index] = roots
            for key in totals:
                totals[key] += statistics[key]
            completed_batches += 1
            emit_progress(
                run_dir,
                "loaded Newton checkpoint",
                batch=batch_index,
                batches=batch_count,
                completedBatches=completed_batches,
                **totals,
            )
        else:
            initial = sequence[begin:end]
            if batch_index == 1:
                initial = np.vstack([R018_COMPACT_ROOT, initial])
            pending.append((batch_index, initial, checkpoint))

    if pending:
        with ProcessPoolExecutor(max_workers=arguments.workers) as executor:
            futures = {
                executor.submit(
                    newton_batch,
                    system,
                    initial,
                    arguments.iterations,
                    arguments.trust_radius,
                    run_dir,
                    batch_index,
                ): (batch_index, checkpoint)
                for batch_index, initial, checkpoint in pending
            }
            for future in as_completed(futures):
                batch_index, checkpoint = futures[future]
                roots, statistics = future.result()
                write_checkpoint(checkpoint, roots, statistics)
                roots_by_batch[batch_index] = roots
                for key in totals:
                    totals[key] += statistics[key]
                completed_batches += 1
                elapsed = time.perf_counter() - started
                eta = elapsed * (batch_count - completed_batches) / completed_batches
                emit_progress(
                    run_dir,
                    "completed Newton batch",
                    batch=batch_index,
                    batches=batch_count,
                    completedBatches=completed_batches,
                    **totals,
                    etaSeconds=eta,
                )

    roots = (
        np.vstack([roots_by_batch[index] for index in sorted(roots_by_batch)])
        if roots_by_batch
        else np.empty((0, 3))
    )
    emit_progress(
        run_dir,
        "clustering and polishing candidates",
        convergedTrajectories=len(roots),
    )
    candidates = cluster_and_polish(system, roots)
    candidates_path = run_dir / "positive-candidates.tsv"
    with candidates_path.open("w", encoding="utf-8") as stream:
        stream.write(
            "index\tbasinCount\tu\tv\tw\tp\tq\tx\t"
            "scaledResidual\tnormalizedJacobianDeterminant\tscipySuccess\n"
        )
        for index, candidate in enumerate(candidates, start=1):
            compact = candidate["compact"]
            physical = candidate["physical"]
            stream.write(
                f"{index}\t{candidate['basinCount']}\t"
                f"{compact[0]:.17g}\t{compact[1]:.17g}\t{compact[2]:.17g}\t"
                f"{physical[0]:.17g}\t{physical[1]:.17g}\t{physical[2]:.17g}\t"
                f"{candidate['scaledResidual']:.17g}\t"
                f"{candidate['normalizedJacobianDeterminant']:.17g}\t"
                f"{str(candidate['scipySuccess']).lower()}\n"
            )
    summary = {
        "scope": "Sobol/Bernstein positive-root candidate scan",
        "proofStatus": "candidate generation only; not a completeness proof",
        "configuration": config,
        "exactBernsteinScales": scales,
        "totals": totals,
        "uniquePositiveCandidates": len(candidates),
        "candidatesSha256": sha256_file(candidates_path),
        "wallSeconds": time.perf_counter() - started,
        "runtime": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": __import__("scipy").__version__,
            "machine": platform.machine(),
            "platform": platform.platform(),
            "logicalCpus": os.cpu_count(),
        },
    }
    atomic_json(run_dir / "summary.json", summary)
    emit_progress(
        run_dir,
        "positive candidate scan completed",
        uniquePositiveCandidates=len(candidates),
        wallSeconds=summary["wallSeconds"],
    )


if __name__ == "__main__":
    main()
