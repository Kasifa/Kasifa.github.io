#!/usr/bin/env python3
"""Classify positive-interior R0.20 stationary roots by Bernstein subdivision.

The three saturated stationary polynomials are compactified by

    p = u/(1-u), q = v/(1-v), x = w/(1-w).

Their tensor-product Bernstein coefficients are constructed directly from
the exact rational monomial cache.  Every Float64 coefficient is enclosed by
an outward-rounded interval, and midpoint de Casteljau subdivision preserves
that enclosure.  A box is excluded when one polynomial has Bernstein
coefficients of one strict sign.  Boxes contained in an independently
certified Krawczyk root box are delegated to that uniqueness certificate.

The run is a completeness proof for the open positive cube only when every
seed checkpoint finishes with no unresolved box and every supplied root and
boundary-strip region is reached.  Compact boundary points are separate
objects handled by the finite-face and blow-up audits.  Box or depth budgets
produce an explicitly incomplete pilot result.
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
from typing import NamedTuple

import numpy as np


SYSTEM_NAMES = (
    "saturated_stationary_p",
    "saturated_stationary_q",
    "saturated_stationary_x",
)
Rational = Fraction
CoefficientIntervals = tuple[tuple[np.ndarray, np.ndarray], ...]


class Node(NamedTuple):
    coefficients: CoefficientIntervals
    indices: tuple[int, int, int]
    depths: tuple[int, int, int]


_INITIAL: CoefficientIntervals | None = None
_ROOT_REGIONS: tuple[tuple[tuple[Rational, Rational], ...], ...] = ()
_BOUNDARY_STRIPS: tuple[tuple[tuple[Rational, Rational], ...], ...] = ()
_MAX_DEPTH = 0
_MAX_BOXES = 0


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path: Path, payload: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def emit(stage: str, started: float, **fields: object) -> None:
    print(
        json.dumps(
            {
                "timestampUtc": datetime.now(timezone.utc).isoformat(),
                "elapsedSeconds": round(time.perf_counter() - started, 3),
                "stage": stage,
                **fields,
            },
            separators=(",", ":"),
        ),
        file=sys.stderr,
        flush=True,
    )


def load_cache(path: Path) -> dict[str, object]:
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        payload = json.load(stream)
    if payload.get("schemaVersion") != 2:
        raise ValueError("R0.20 exact cache schema version 2 is required")
    return payload


def exact_bernstein_intervals(
    rows: list[list[object]],
) -> tuple[tuple[np.ndarray, np.ndarray], str, tuple[int, int, int]]:
    degrees = tuple(max(int(row[axis]) for row in rows) for axis in range(3))
    entries: list[tuple[tuple[int, int, int], Rational]] = []
    for row in rows:
        powers = tuple(int(row[axis]) for axis in range(3))
        coefficient = Rational(int(row[3]), int(row[4]))
        divisor = math.prod(
            math.comb(degrees[axis], powers[axis]) for axis in range(3)
        )
        entries.append((powers, coefficient / divisor))
    scale = max(abs(coefficient) for _powers, coefficient in entries)
    shape = tuple(degree + 1 for degree in degrees)
    lower = np.zeros(shape, dtype=np.float64)
    upper = np.zeros(shape, dtype=np.float64)
    for powers, coefficient in entries:
        exact_value = coefficient / scale
        value = float(exact_value)
        if not math.isfinite(value) or (value == 0.0 and exact_value != 0):
            raise FloatingPointError("an exact Bernstein coefficient was not representable")
        lower[powers] = np.nextafter(value, -np.inf)
        upper[powers] = np.nextafter(value, np.inf)
    return (lower, upper), str(scale), degrees


def decimal_rational(value: str) -> Rational:
    return Rational(value)


def load_root_regions(path: Path) -> tuple[tuple[tuple[Rational, Rational], ...], ...]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    regions = []
    for root in payload["roots"]:
        certificate = root["stationarySystemCertificate"]
        if not certificate["strictInteriorInclusion"] or not certificate["contractionCertified"]:
            raise AssertionError("a supplied root box lacked a strict Krawczyk certificate")
        compact_intervals = []
        for lower_text, upper_text in certificate["boxDecimal"]:
            lower = decimal_rational(lower_text)
            upper = decimal_rational(upper_text)
            compact_intervals.append(
                (
                    lower / (1 + lower),
                    upper / (1 + upper),
                )
            )
        regions.append(tuple(compact_intervals))
    return tuple(regions)


def load_boundary_strip_regions(
    path: Path | None,
) -> tuple[tuple[tuple[Rational, Rational], ...], ...]:
    if path is None:
        return ()
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schemaVersion") != 1:
        raise ValueError("R0.20 boundary-strip schema version 1 is required")
    regions = []
    for key in ("zeroBoundary", "infinityBoundary"):
        boundary = payload[key]
        certificate = boundary["certificate"]
        if not certificate["certified"]:
            raise AssertionError("a supplied boundary strip was not certified")
        for cell in certificate["cells"]:
            if not cell["certified"] or not all(
                half["certified"] and half["exactReconstructionCheck"]
                for half in cell["halves"]
            ):
                raise AssertionError("a boundary-strip subcell lacked its exact sign certificate")
        regions.append(
            tuple(
                (Rational(lower), Rational(upper))
                for lower, upper in boundary["dyadicCoreCompactCube"]
            )
        )
    return tuple(regions)


def outward_midpoint(lower_left: np.ndarray, lower_right: np.ndarray, upper_left: np.ndarray, upper_right: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    lower_sum = np.nextafter(lower_left + lower_right, -np.inf)
    upper_sum = np.nextafter(upper_left + upper_right, np.inf)
    lower = np.nextafter(0.5 * lower_sum, -np.inf)
    upper = np.nextafter(0.5 * upper_sum, np.inf)
    exact_zero = (
        (lower_left == 0.0)
        & (upper_left == 0.0)
        & (lower_right == 0.0)
        & (upper_right == 0.0)
    )
    lower[exact_zero] = 0.0
    upper[exact_zero] = 0.0
    return lower, upper


def subdivide_tensor(
    lower: np.ndarray,
    upper: np.ndarray,
    axis: int,
) -> tuple[tuple[np.ndarray, np.ndarray], tuple[np.ndarray, np.ndarray]]:
    work_lower = np.moveaxis(lower, axis, -1).copy()
    work_upper = np.moveaxis(upper, axis, -1).copy()
    degree = work_lower.shape[-1] - 1
    left_lower = np.empty_like(work_lower)
    left_upper = np.empty_like(work_upper)
    right_lower = np.empty_like(work_lower)
    right_upper = np.empty_like(work_upper)
    left_lower[..., 0] = work_lower[..., 0]
    left_upper[..., 0] = work_upper[..., 0]
    right_lower[..., degree] = work_lower[..., degree]
    right_upper[..., degree] = work_upper[..., degree]
    length = degree + 1
    for level in range(1, degree + 1):
        work_lower, work_upper = outward_midpoint(
            work_lower[..., : length - 1],
            work_lower[..., 1:length],
            work_upper[..., : length - 1],
            work_upper[..., 1:length],
        )
        length -= 1
        left_lower[..., level] = work_lower[..., 0]
        left_upper[..., level] = work_upper[..., 0]
        right_lower[..., degree - level] = work_lower[..., length - 1]
        right_upper[..., degree - level] = work_upper[..., length - 1]
    return (
        (np.moveaxis(left_lower, -1, axis), np.moveaxis(left_upper, -1, axis)),
        (np.moveaxis(right_lower, -1, axis), np.moveaxis(right_upper, -1, axis)),
    )


def subdivide_system(
    coefficients: CoefficientIntervals,
    axis: int,
) -> tuple[CoefficientIntervals, CoefficientIntervals]:
    children = [subdivide_tensor(lower, upper, axis) for lower, upper in coefficients]
    return (
        tuple(child[0] for child in children),
        tuple(child[1] for child in children),
    )


def restrict_to_seed(
    coefficients: CoefficientIntervals,
    indices: tuple[int, int, int],
    depth: int,
) -> CoefficientIntervals:
    current = coefficients
    for axis in range(3):
        for level in range(depth):
            left, right = subdivide_system(current, axis)
            bit = (indices[axis] >> (depth - level - 1)) & 1
            current = right if bit else left
    return current


def dyadic_bounds(indices: tuple[int, int, int], depths: tuple[int, int, int]) -> tuple[tuple[Rational, Rational], ...]:
    return tuple(
        (
            Rational(indices[axis], 2 ** depths[axis]),
            Rational(indices[axis] + 1, 2 ** depths[axis]),
        )
        for axis in range(3)
    )


def subset_region(
    bounds: tuple[tuple[Rational, Rational], ...],
    region: tuple[tuple[Rational, Rational], ...],
) -> bool:
    return all(
        bounds[axis][0] >= region[axis][0]
        and bounds[axis][1] <= region[axis][1]
        for axis in range(3)
    )


def intersects_region(
    bounds: tuple[tuple[Rational, Rational], ...],
    region: tuple[tuple[Rational, Rational], ...],
) -> bool:
    return all(
        bounds[axis][1] >= region[axis][0]
        and bounds[axis][0] <= region[axis][1]
        for axis in range(3)
    )


def choose_axis(
    bounds: tuple[tuple[Rational, Rational], ...],
    depths: tuple[int, int, int],
) -> int | None:
    available = [axis for axis in range(3) if depths[axis] < _MAX_DEPTH]
    if not available:
        return None
    target_regions = _ROOT_REGIONS + _BOUNDARY_STRIPS
    overlapping = [region for region in target_regions if intersects_region(bounds, region)]
    if overlapping:
        return max(
            available,
            key=lambda axis: max(
                float(
                    (bounds[axis][1] - bounds[axis][0])
                    / (region[axis][1] - region[axis][0])
                )
                for region in overlapping
            ),
        )
    return min(available, key=lambda axis: depths[axis])


def serialize_box(indices: tuple[int, int, int], depths: tuple[int, int, int]) -> dict[str, list[int]]:
    return {"indices": list(indices), "depths": list(depths)}


def initialize_worker(
    cache_path: str,
    certificates_path: str,
    boundary_strips_path: str | None,
    max_depth: int,
    max_boxes: int,
) -> None:
    global _INITIAL, _ROOT_REGIONS, _BOUNDARY_STRIPS, _MAX_DEPTH, _MAX_BOXES
    cache = load_cache(Path(cache_path))
    tensors = []
    for name in SYSTEM_NAMES:
        intervals, _scale, _degrees = exact_bernstein_intervals(
            cache["polynomials"][name]
        )
        tensors.append(intervals)
    _INITIAL = tuple(tensors)
    _ROOT_REGIONS = load_root_regions(Path(certificates_path))
    _BOUNDARY_STRIPS = load_boundary_strip_regions(
        Path(boundary_strips_path) if boundary_strips_path is not None else None
    )
    _MAX_DEPTH = max_depth
    _MAX_BOXES = max_boxes


def process_seed(seed: tuple[int, int, int], seed_depth: int) -> dict[str, object]:
    if _INITIAL is None:
        raise RuntimeError("worker was not initialized")
    started = time.perf_counter()
    initial = restrict_to_seed(_INITIAL, seed, seed_depth)
    stack = [Node(initial, seed, (seed_depth, seed_depth, seed_depth))]
    visited = 0
    subdivisions = 0
    excluded = [0, 0, 0]
    covered = [0] * len(_ROOT_REGIONS)
    covered_boundary_strips = [0] * len(_BOUNDARY_STRIPS)
    unresolved: list[dict[str, list[int]]] = []
    maximum_depths = [seed_depth, seed_depth, seed_depth]
    budget_exhausted = False

    while stack:
        node = stack.pop()
        visited += 1
        if visited > _MAX_BOXES:
            budget_exhausted = True
            unresolved.append(serialize_box(node.indices, node.depths))
            unresolved.extend(
                serialize_box(item.indices, item.depths) for item in stack[:49]
            )
            break

        equation = next(
            (
                index
                for index, (lower, upper) in enumerate(node.coefficients)
                if float(np.min(lower)) > 0.0 or float(np.max(upper)) < 0.0
            ),
            None,
        )
        if equation is not None:
            excluded[equation] += 1
            continue

        bounds = dyadic_bounds(node.indices, node.depths)
        region_index = next(
            (
                index
                for index, region in enumerate(_ROOT_REGIONS)
                if subset_region(bounds, region)
            ),
            None,
        )
        if region_index is not None:
            covered[region_index] += 1
            continue

        strip_index = next(
            (
                index
                for index, region in enumerate(_BOUNDARY_STRIPS)
                if subset_region(bounds, region)
            ),
            None,
        )
        if strip_index is not None:
            covered_boundary_strips[strip_index] += 1
            continue

        axis = choose_axis(bounds, node.depths)
        if axis is None:
            unresolved.append(serialize_box(node.indices, node.depths))
            if len(unresolved) >= 50:
                budget_exhausted = True
                break
            continue

        left_coefficients, right_coefficients = subdivide_system(node.coefficients, axis)
        child_depths = list(node.depths)
        child_depths[axis] += 1
        left_indices = list(node.indices)
        right_indices = list(node.indices)
        left_indices[axis] *= 2
        right_indices[axis] = 2 * right_indices[axis] + 1
        child_depths_tuple = tuple(child_depths)
        stack.append(Node(right_coefficients, tuple(right_indices), child_depths_tuple))
        stack.append(Node(left_coefficients, tuple(left_indices), child_depths_tuple))
        subdivisions += 1
        for index in range(3):
            maximum_depths[index] = max(maximum_depths[index], child_depths[index])

    return {
        "schemaVersion": 1,
        "seed": list(seed),
        "seedDepth": seed_depth,
        "complete": not budget_exhausted and not stack and not unresolved,
        "boxesVisited": visited,
        "subdivisions": subdivisions,
        "excludedByEquation": excluded,
        "coveredByRootRegion": covered,
        "coveredByBoundaryStrip": covered_boundary_strips,
        "maximumDepths": maximum_depths,
        "unresolvedCountRecorded": len(unresolved),
        "unresolvedSample": unresolved[:50],
        "frontierCountAtStop": len(stack),
        "budgetExhausted": budget_exhausted,
        "wallSeconds": time.perf_counter() - started,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--certificates", type=Path, required=True)
    parser.add_argument("--boundary-strips", type=Path)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--seed-depth", type=int, default=2)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--max-depth", type=int, default=48)
    parser.add_argument("--max-boxes-per-seed", type=int, default=100000)
    arguments = parser.parse_args()
    if arguments.workers < 1 or arguments.seed_depth < 0:
        raise ValueError("workers must be positive and seed depth nonnegative")
    started = time.perf_counter()
    arguments.run_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_dir = arguments.run_dir / "checkpoints"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    cache = load_cache(arguments.cache)
    scales = []
    degrees = []
    for name in SYSTEM_NAMES:
        _intervals, scale, polynomial_degrees = exact_bernstein_intervals(
            cache["polynomials"][name]
        )
        scales.append(scale)
        degrees.append(list(polynomial_degrees))
    root_regions = load_root_regions(arguments.certificates)
    boundary_strip_regions = load_boundary_strip_regions(arguments.boundary_strips)
    configuration = {
        "schemaVersion": 1,
        "cache": str(arguments.cache.resolve()),
        "cacheSha256": sha256_file(arguments.cache),
        "certificates": str(arguments.certificates.resolve()),
        "certificatesSha256": sha256_file(arguments.certificates),
        "boundaryStrips": (
            str(arguments.boundary_strips.resolve())
            if arguments.boundary_strips is not None
            else None
        ),
        "boundaryStripsSha256": (
            sha256_file(arguments.boundary_strips)
            if arguments.boundary_strips is not None
            else None
        ),
        "coordinateMap": ["p=u/(1-u)", "q=v/(1-v)", "x=w/(1-w)"],
        "systemNames": list(SYSTEM_NAMES),
        "degrees": degrees,
        "exactPositiveScales": scales,
        "seedDepth": arguments.seed_depth,
        "workers": arguments.workers,
        "maxDepth": arguments.max_depth,
        "maxBoxesPerSeed": arguments.max_boxes_per_seed,
        "rootRegionCount": len(root_regions),
        "boundaryStripCount": len(boundary_strip_regions),
        "python": sys.version,
        "numpy": np.__version__,
        "platform": platform.platform(),
    }
    atomic_json(arguments.run_dir / "config.json", configuration)

    side = 2 ** arguments.seed_depth
    seeds = [
        (i, j, k)
        for i in range(side)
        for j in range(side)
        for k in range(side)
    ]
    pending = [
        seed
        for seed in seeds
        if not (checkpoint_dir / f"seed-{seed[0]}-{seed[1]}-{seed[2]}.json").exists()
    ]
    emit(
        "starting certified Bernstein seed audit",
        started,
        seeds=len(seeds),
        pending=len(pending),
        workers=arguments.workers,
    )

    if pending:
        with ProcessPoolExecutor(
            max_workers=arguments.workers,
            initializer=initialize_worker,
            initargs=(
                str(arguments.cache),
                str(arguments.certificates),
                (
                    str(arguments.boundary_strips)
                    if arguments.boundary_strips is not None
                    else None
                ),
                arguments.max_depth,
                arguments.max_boxes_per_seed,
            ),
        ) as executor:
            futures = {
                executor.submit(process_seed, seed, arguments.seed_depth): seed
                for seed in pending
            }
            for completed, future in enumerate(as_completed(futures), start=1):
                seed = futures[future]
                result = future.result()
                path = checkpoint_dir / f"seed-{seed[0]}-{seed[1]}-{seed[2]}.json"
                atomic_json(path, result)
                emit(
                    "Bernstein seed checkpoint completed",
                    started,
                    completed=completed,
                    pending=len(pending),
                    seed=list(seed),
                    complete=result["complete"],
                    boxesVisited=result["boxesVisited"],
                    maximumDepths=result["maximumDepths"],
                    wallSeconds=round(result["wallSeconds"], 3),
                )

    records = [
        json.loads(
            (checkpoint_dir / f"seed-{seed[0]}-{seed[1]}-{seed[2]}.json").read_text(
                encoding="utf-8"
            )
        )
        for seed in seeds
    ]
    covered = [
        sum(record["coveredByRootRegion"][index] for record in records)
        for index in range(len(root_regions))
    ]
    covered_boundary_strips = [
        sum(record["coveredByBoundaryStrip"][index] for record in records)
        for index in range(len(boundary_strip_regions))
    ]
    complete = all(record["complete"] for record in records) and all(
        count > 0 for count in covered
    ) and all(count > 0 for count in covered_boundary_strips)
    summary = {
        "schemaVersion": 1,
        "scope": "positive open compactified cube stationary-root classification",
        "proofStatus": (
            "complete positive-interior Bernstein exclusion outside independently certified root boxes and boundary strips"
            if complete
            else "incomplete pilot; unresolved or budget-limited seed boxes remain"
        ),
        "complete": complete,
        "configuration": configuration,
        "totals": {
            "seeds": len(records),
            "completeSeeds": sum(bool(record["complete"]) for record in records),
            "boxesVisited": sum(record["boxesVisited"] for record in records),
            "subdivisions": sum(record["subdivisions"] for record in records),
            "excludedByEquation": [
                sum(record["excludedByEquation"][index] for record in records)
                for index in range(3)
            ],
            "coveredByRootRegion": covered,
            "coveredByBoundaryStrip": covered_boundary_strips,
            "maximumDepths": [
                max(record["maximumDepths"][index] for record in records)
                for index in range(3)
            ],
            "unresolvedSamplesRecorded": sum(
                record["unresolvedCountRecorded"] for record in records
            ),
        },
        "wallSeconds": time.perf_counter() - started,
    }
    atomic_json(arguments.run_dir / "summary.json", summary)
    emit("Bernstein cube audit completed", started, complete=complete, totals=summary["totals"])


if __name__ == "__main__":
    main()
