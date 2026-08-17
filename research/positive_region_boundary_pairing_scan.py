#!/usr/bin/env python3
"""Numerically pair isolated resultant coordinates on an R0.20 face.

An elimination root is only a projected coordinate candidate.  Given exact
isolating intervals for one coordinate, this script seeds the other positive
coordinate over a logarithmic grid and refines the full two-equation face
system.  Successful pairs remain numerical candidates until an exact local
certificate and a resultant-compatibility proof are supplied.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import gzip
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import root

from positive_region_boundary_scan import System, tensor, value


def load_cache(path: Path) -> dict[str, object]:
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        payload = json.load(stream)
    if payload.get("schemaVersion") != 1:
        raise ValueError("R0.20 boundary cache schema version 1 is required")
    return payload


def retained_midpoints(path: Path) -> list[float]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [
        float(interval["midpointDecimal"])
        for factor in payload["positiveFactors"]
        for interval in factor["intervals"]
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--face", required=True)
    parser.add_argument("--isolation", type=Path, required=True)
    parser.add_argument("--retained-variable", default="x")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--log-grid-min", type=float, default=-8.0)
    parser.add_argument("--log-grid-max", type=float, default=8.0)
    parser.add_argument("--log-grid-count", type=int, default=321)
    arguments = parser.parse_args()

    face = load_cache(arguments.cache)["faces"][arguments.face]
    retained_axis = face["freeVariables"].index(arguments.retained_variable)
    free_axis = 1 - retained_axis
    system = System([tensor(rows)[0] for rows in face["reducedStationary"]])
    target_tensor, target_scale = tensor(face["target"])
    total_tensor, total_scale = tensor(face["total"])
    target_degrees = (target_tensor.shape[0] - 1, target_tensor.shape[1] - 1)
    total_degrees = (total_tensor.shape[0] - 1, total_tensor.shape[1] - 1)

    def function(point: np.ndarray) -> np.ndarray:
        return system.evaluate(point[None, :])[0][0]

    def jacobian(point: np.ndarray) -> np.ndarray:
        return system.evaluate(point[None, :])[1][0]

    grid = np.logspace(
        arguments.log_grid_min,
        arguments.log_grid_max,
        arguments.log_grid_count,
    )
    records = []
    for retained in retained_midpoints(arguments.isolation):
        retained_compact = retained / (1.0 + retained)
        candidates = []
        for free_physical in grid:
            initial = np.empty(2, dtype=np.float64)
            initial[retained_axis] = retained_compact
            initial[free_axis] = free_physical / (1.0 + free_physical)
            refined = root(
                function,
                initial,
                jac=jacobian,
                method="hybr",
                options={"xtol": 1.0e-12, "maxfev": 600},
            )
            point = np.asarray(refined.x, dtype=np.float64)
            if not refined.success or not np.all((point > 0) & (point < 1)):
                continue
            physical = point / (1.0 - point)
            if abs(physical[retained_axis] - retained) > 1.0e-8 * max(1.0, retained):
                continue
            functions, derivative = system.evaluate(point[None, :])
            scales = np.maximum(np.max(np.abs(derivative[0]), axis=1), np.abs(functions[0]))
            residual = float(np.max(np.abs(functions[0] / np.maximum(scales, 1.0e-300))))
            if residual > 1.0e-9:
                continue
            if any(np.max(np.abs(point - item["compact"])) < 1.0e-9 for item in candidates):
                continue
            target_normalized = value(target_tensor, point[None, :])[0]
            total_normalized = value(total_tensor, point[None, :])[0]
            fraction = (
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
                    "physical": physical,
                    "scaledResidual": residual,
                    "targetFraction": float(fraction),
                }
            )
        candidates.sort(key=lambda item: tuple(item["physical"]))
        records.append(
            {
                "retainedMidpoint": retained,
                "pairs": [
                    {
                        "physical": {
                            name: float(item["physical"][axis])
                            for axis, name in enumerate(face["freeVariables"])
                        },
                        "compact": item["compact"].tolist(),
                        "scaledResidual": item["scaledResidual"],
                        "targetFraction": item["targetFraction"],
                    }
                    for item in candidates
                ],
            }
        )
    result = {
        "schemaVersion": 1,
        "scope": "numerical pairing of exact resultant-coordinate candidates",
        "proofStatus": "candidate generation only",
        "face": arguments.face,
        "freeVariables": face["freeVariables"],
        "retainedVariable": arguments.retained_variable,
        "configuration": {
            "logGridMin": arguments.log_grid_min,
            "logGridMax": arguments.log_grid_max,
            "logGridCount": arguments.log_grid_count,
        },
        "retainedRoots": records,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
