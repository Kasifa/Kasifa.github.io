#!/usr/bin/env python3
"""Generate stationary candidates on the four finite R0.20 faces.

Each positive pair of free physical variables is compactified to the open unit
square.  Exact face polynomials are converted directly to tensor-product
Bernstein coefficients, then scrambled Sobol points are refined with a
row-scaled trust-region Newton iteration.  The four faces run independently
and may be processed in parallel.

This is a numerical candidate generator.  Exact resultants and interval
certificates are required for root completeness and uniqueness.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
from fractions import Fraction
import gzip
import json
import math
from pathlib import Path
import sys
import time

import numpy as np
from scipy.optimize import root
from scipy.stats import qmc


def emit(stage: str, **fields: object) -> None:
    record = {"timestampUtc": datetime.now(timezone.utc).isoformat(), "stage": stage, **fields}
    print(json.dumps(record, separators=(",", ":")), file=sys.stderr, flush=True)


def load(path: Path) -> dict[str, object]:
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        payload = json.load(stream)
    if payload.get("schemaVersion") != 1:
        raise ValueError("R0.20 boundary cache schema version 1 is required")
    return payload


def tensor(rows: list[list[object]]) -> tuple[np.ndarray, Fraction]:
    degrees = tuple(max(int(row[axis]) for row in rows) for axis in range(2))
    entries = []
    for row in rows:
        powers = (int(row[0]), int(row[1]))
        coefficient = Fraction(int(row[2]), int(row[3]))
        coefficient /= math.comb(degrees[0], powers[0]) * math.comb(degrees[1], powers[1])
        entries.append((powers, coefficient))
    scale = max(abs(coefficient) for _powers, coefficient in entries)
    result = np.zeros((degrees[0] + 1, degrees[1] + 1), dtype=np.float64)
    for powers, coefficient in entries:
        result[powers] = float(coefficient / scale)
    return result, scale


def basis(degree: int, values: np.ndarray) -> np.ndarray:
    indices = np.arange(degree + 1)
    binomials = np.array([math.comb(degree, int(index)) for index in indices], dtype=np.float64)
    return binomials[None, :] * values[:, None] ** indices * (1 - values[:, None]) ** (degree - indices)


def derivative(source: np.ndarray, axis: int) -> np.ndarray:
    return (source.shape[axis] - 1) * np.diff(source, axis=axis)


def value(source: np.ndarray, points: np.ndarray) -> np.ndarray:
    first = basis(source.shape[0] - 1, points[:, 0])
    second = basis(source.shape[1] - 1, points[:, 1])
    return np.einsum("ni,nj,ij->n", first, second, source, optimize=True)


class System:
    def __init__(self, functions: list[np.ndarray]):
        self.functions = functions
        self.jacobian = [[derivative(function, axis) for axis in range(2)] for function in functions]

    def evaluate(self, points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        functions = np.column_stack([value(function, points) for function in self.functions])
        jacobian = np.stack(
            [np.column_stack([value(entry, points) for entry in row]) for row in self.jacobian],
            axis=1,
        )
        return functions, jacobian


def refine(system: System, points: np.ndarray, iterations: int, trust_radius: float) -> np.ndarray:
    points = points.copy()
    active = np.ones(len(points), dtype=bool)
    converged: list[np.ndarray] = []
    for _iteration in range(iterations):
        indices = np.flatnonzero(active)
        if not len(indices):
            break
        current = points[indices]
        functions, jacobian = system.evaluate(current)
        scales = np.maximum(np.max(np.abs(jacobian), axis=2), np.abs(functions))
        functions /= np.maximum(scales, 1.0e-300)
        jacobian /= np.maximum(scales, 1.0e-300)[:, :, None]
        determinant = jacobian[:, 0, 0] * jacobian[:, 1, 1] - jacobian[:, 0, 1] * jacobian[:, 1, 0]
        usable = np.abs(determinant) > 1.0e-13
        delta = np.zeros_like(current)
        delta[usable, 0] = (
            jacobian[usable, 1, 1] * functions[usable, 0]
            - jacobian[usable, 0, 1] * functions[usable, 1]
        ) / determinant[usable]
        delta[usable, 1] = (
            -jacobian[usable, 1, 0] * functions[usable, 0]
            + jacobian[usable, 0, 0] * functions[usable, 1]
        ) / determinant[usable]
        norms = np.max(np.abs(delta), axis=1)
        delta *= np.minimum(1.0, trust_radius / np.maximum(norms, 1.0e-300))[:, None]
        updated = current - delta
        interior = np.all((updated > 0) & (updated < 1), axis=1)
        step_converged = usable & interior & (norms < 1.0e-11) & (np.max(np.abs(functions), axis=1) < 1.0e-9)
        if np.any(step_converged):
            converged.append(updated[step_converged])
        keep = usable & interior & ~step_converged
        points[indices[keep]] = updated[keep]
        active[indices[~keep]] = False
    return np.vstack(converged) if converged else np.empty((0, 2))


def scan_face(
    face_name: str,
    face: dict[str, object],
    power: int,
    seed: int,
    iterations: int,
    boundary_margin: float,
) -> dict[str, object]:
    started = time.perf_counter()
    function_tensors = [tensor(rows)[0] for rows in face["reducedStationary"]]
    system = System(function_tensors)
    initial = qmc.Sobol(d=2, scramble=True, seed=seed).random_base2(power)
    roots = []
    batch_size = 2**15
    for begin in range(0, len(initial), batch_size):
        roots.append(refine(system, initial[begin:begin + batch_size], iterations, 0.2))
    roots_array = np.vstack(roots) if roots else np.empty((0, 2))
    keys = np.round(roots_array / 1.0e-7).astype(np.int64)
    unique, inverse, counts = np.unique(keys, axis=0, return_inverse=True, return_counts=True)
    target_tensor, target_scale = tensor(face["target"])
    total_tensor, total_scale = tensor(face["total"])
    target_degrees = (target_tensor.shape[0] - 1, target_tensor.shape[1] - 1)
    total_degrees = (total_tensor.shape[0] - 1, total_tensor.shape[1] - 1)

    def function(point: np.ndarray) -> np.ndarray:
        return system.evaluate(point[None, :])[0][0]

    def jacobian(point: np.ndarray) -> np.ndarray:
        return system.evaluate(point[None, :])[1][0]

    candidates = []
    for index, count in enumerate(counts):
        representative = roots_array[np.flatnonzero(inverse == index)[0]]
        polished = root(function, representative, jac=jacobian, method="hybr", options={"xtol": 1.0e-12, "maxfev": 400})
        point = np.asarray(polished.x, dtype=np.float64)
        if (
            not polished.success
            or not np.all((point > boundary_margin) & (point < 1 - boundary_margin))
        ):
            continue
        functions, derivative_value = system.evaluate(point[None, :])
        row_scales = np.maximum(np.max(np.abs(derivative_value[0]), axis=1), np.abs(functions[0]))
        residual = float(np.max(np.abs(functions[0] / np.maximum(row_scales, 1.0e-300))))
        if residual > 1.0e-9:
            continue
        if any(np.max(np.abs(point - item["compact"])) < 1.0e-8 for item in candidates):
            continue
        target_normalized = value(target_tensor, point[None, :])[0]
        total_normalized = value(total_tensor, point[None, :])[0]
        target_fraction = (
            target_normalized
            / total_normalized
            * float(target_scale / total_scale)
            * math.prod(
                (1.0 - point[axis]) ** (total_degrees[axis] - target_degrees[axis])
                for axis in range(2)
            )
        )
        candidates.append(
            {
                "compact": point,
                "physical": point / (1 - point),
                "basinCount": int(count),
                "scaledResidual": residual,
                "normalizedJacobianDeterminant": float(
                    np.linalg.det(derivative_value[0] / np.maximum(row_scales, 1.0e-300)[:, None])
                ),
                "targetFraction": float(target_fraction),
            }
        )
    candidates.sort(key=lambda item: tuple(item["physical"]))
    return {
        "face": face_name,
        "fixedVariable": face["fixedVariable"],
        "side": face["side"],
        "freeVariables": face["freeVariables"],
        "starts": len(initial),
        "convergedTrajectories": len(roots_array),
        "wallSeconds": time.perf_counter() - started,
        "candidates": [
            {
                "compact": item["compact"].tolist(),
                "physical": item["physical"].tolist(),
                **{key: item[key] for key in ("basinCount", "scaledResidual", "normalizedJacobianDeterminant", "targetFraction")},
            }
            for item in candidates
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--power", type=int, default=18)
    parser.add_argument("--iterations", type=int, default=60)
    parser.add_argument("--seed", type=int, default=20260821)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--boundary-margin", type=float, default=1.0e-12)
    arguments = parser.parse_args()
    started = time.perf_counter()
    payload = load(arguments.cache)
    results = []
    emit("starting finite-face scans", faces=len(payload["faces"]), workers=arguments.workers)
    with ProcessPoolExecutor(max_workers=arguments.workers) as executor:
        futures = {
            executor.submit(
                scan_face,
                face_name,
                face,
                arguments.power,
                arguments.seed + index,
                arguments.iterations,
                arguments.boundary_margin,
            ): face_name
            for index, (face_name, face) in enumerate(payload["faces"].items())
        }
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            emit(
                "finite-face scan completed",
                face=result["face"],
                candidates=len(result["candidates"]),
                converged=result["convergedTrajectories"],
                faceWallSeconds=round(result["wallSeconds"], 3),
            )
    results.sort(key=lambda item: item["face"])
    output = {
        "schemaVersion": 1,
        "scope": "finite-face stationary candidate scan",
        "proofStatus": "candidate generation only; exact pairing and certification pending",
        "configuration": {
            "powerPerFace": arguments.power,
            "startsPerFace": 2**arguments.power,
            "iterations": arguments.iterations,
            "seed": arguments.seed,
            "workers": arguments.workers,
            "candidateBoundaryMargin": arguments.boundary_margin,
        },
        "faces": results,
        "wallSeconds": time.perf_counter() - started,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    emit("all finite-face scans completed", wallSeconds=round(output["wallSeconds"], 3))


if __name__ == "__main__":
    main()
