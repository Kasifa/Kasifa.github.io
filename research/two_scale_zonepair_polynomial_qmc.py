#!/usr/bin/env python3
"""R0.69V zone-pair cubic QMC for selected coarse annuli.

For a fixed scale separation, every full-space annular carrier is cubic in
the outer amplitude.  This independent estimator samples all unordered
radial zone pairs directly, evaluates four common amplitude nodes, and
reconstructs selected coarse-annulus polynomials at sample level.

The reported scramble bands are randomized diagnostics.  They are pointwise,
not simultaneous interval enclosures, and do not constitute a sign proof.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform
import subprocess
import sys
import time

import numpy as np
import scipy
from scipy.stats import qmc

from affine_core_dyadic_qmc import compact_vorticity, cutoff_value
from two_scale_full_annular_qmc import (
    KERNEL_FACTOR,
    map_sobol_to_zone_pair,
    mean_and_se,
    radial_zones,
    shell_volume,
    write_progress,
    zone_role,
)


AMPLITUDE_NODES = np.asarray([0.0, 1.0 / 3.0, 2.0 / 3.0, 1.0])
VANDERMONDE = np.vander(AMPLITUDE_NODES, N=4, increasing=True)
VANDERMONDE_INVERSE = np.linalg.inv(VANDERMONDE)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def selected_annular_node_means(
    unit: np.ndarray,
    left_zone: tuple[float, float],
    right_zone: tuple[float, float],
    diagonal: bool,
    epsilon: float,
    indices: tuple[int, ...],
) -> tuple[dict[int, np.ndarray], float]:
    x, y = map_sobol_to_zone_pair(unit, left_zone, right_zone)
    displacement = y - x
    distance = np.linalg.norm(displacement, axis=1)
    direction = displacement / distance[:, None]
    outer_x = compact_vorticity(x, 1.0)
    outer_y = compact_vorticity(y, 1.0)
    inner_x = compact_vorticity(x, epsilon)
    inner_y = compact_vorticity(y, epsilon)
    multiplier = 1.0 if diagonal else 2.0
    common = (
        multiplier
        * shell_volume(*left_zone)
        * shell_volume(*right_zone)
        * KERNEL_FACTOR
        / distance**3
    )

    values_at_nodes = np.empty((4, unit.shape[0]), dtype=np.float64)
    for node_index, amplitude in enumerate(AMPLITUDE_NODES):
        omega_x = amplitude * outer_x + (1.0 - amplitude) * inner_x
        omega_y = amplitude * outer_y + (1.0 - amplitude) * inner_y
        delta = omega_y - omega_x
        geometric = np.einsum("ij,ij->i", direction, delta) * np.einsum(
            "ij,ij->i", direction, np.cross(omega_x, delta)
        )
        values_at_nodes[node_index] = common * geometric

    means: dict[int, np.ndarray] = {}
    residual_max = 0.0
    for index in indices:
        weight = cutoff_value(distance / (2.0 ** (index + 1))) - cutoff_value(
            distance / (2.0**index)
        )
        node_means = np.mean(values_at_nodes * weight[None, :], axis=1)
        coefficients = VANDERMONDE_INVERSE @ node_means
        residual_max = max(
            residual_max,
            float(np.max(np.abs(VANDERMONDE @ coefficients - node_means))),
        )
        means[index] = coefficients
    return means, residual_max


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--replicates", type=int, default=16)
    parser.add_argument("--power", type=int, default=18)
    parser.add_argument("--separation", type=int, default=2)
    parser.add_argument("--indices", default="-2,0")
    parser.add_argument("--amplitude-grid", type=int, default=4001)
    parser.add_argument("--seed-base", type=int, default=691201)
    parser.add_argument("--source-commit")
    arguments = parser.parse_args()
    arguments.indices = tuple(
        sorted({int(value) for value in arguments.indices.split(",")})
    )
    if arguments.replicates < 2 or arguments.power < 1:
        parser.error("invalid replicate count or QMC power")
    if arguments.separation < 1 or not arguments.indices:
        parser.error("positive separation and at least one index are required")
    if arguments.amplitude_grid < 101:
        parser.error("--amplitude-grid must be at least 101")
    return arguments


def main() -> int:
    arguments = parse_arguments()
    head_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if arguments.source_commit is not None and arguments.source_commit != head_commit:
        raise SystemExit(
            f"source commit mismatch: requested {arguments.source_commit}, HEAD is {head_commit}"
        )

    output_root = arguments.output_root
    output_root.mkdir(parents=True, exist_ok=True)
    source_path = Path(__file__).resolve()
    started = time.perf_counter()
    epsilon = 2.0 ** (-arguments.separation)
    zones = radial_zones(epsilon)
    zone_pairs = tuple(
        (left, right)
        for left in range(len(zones))
        for right in range(left, len(zones))
    )
    replicate_coefficients = np.zeros(
        (arguments.replicates, len(arguments.indices), 4), dtype=np.float64
    )
    pair_records: list[dict[str, object]] = []
    reconstruction_residual_max = 0.0

    with (output_root / "progress.ndjson").open("w", encoding="utf-8") as progress:
        write_progress(
            progress,
            started,
            "started",
            separation=arguments.separation,
            epsilon=epsilon,
            indices=list(arguments.indices),
            replicates=arguments.replicates,
            pointsPerZonePair=2**arguments.power,
            zonePairs=len(zone_pairs),
            amplitudeNodes=AMPLITUDE_NODES.tolist(),
        )
        for replicate in range(arguments.replicates):
            for pair_number, (left, right) in enumerate(zone_pairs):
                seed = (
                    arguments.seed_base
                    + replicate * 100_000
                    + pair_number * 1_000
                    + arguments.separation
                )
                sampler = qmc.Sobol(d=5, scramble=True, seed=seed)
                unit = sampler.random_base2(arguments.power)
                coefficients, residual = selected_annular_node_means(
                    unit,
                    zones[left],
                    zones[right],
                    left == right,
                    epsilon,
                    arguments.indices,
                )
                reconstruction_residual_max = max(
                    reconstruction_residual_max, residual
                )
                for row, index in enumerate(arguments.indices):
                    replicate_coefficients[replicate, row] += coefficients[index]
                    pair_records.append(
                        {
                            "replicate": replicate,
                            "index": index,
                            "leftZone": left,
                            "rightZone": right,
                            "leftRole": zone_role(zones[left], epsilon),
                            "rightRole": zone_role(zones[right], epsilon),
                            "pairClass": (
                                f"{zone_role(zones[left], epsilon)}--"
                                f"{zone_role(zones[right], epsilon)}"
                            ),
                            **{
                                f"c{degree}": coefficients[index][degree]
                                for degree in range(4)
                            },
                        }
                    )
            write_progress(
                progress,
                started,
                "replicate-complete",
                replicate=replicate + 1,
                replicates=arguments.replicates,
                coefficients={
                    str(index): replicate_coefficients[replicate, row].tolist()
                    for row, index in enumerate(arguments.indices)
                },
            )

        coefficient_records: list[dict[str, object]] = []
        mean_coefficients = np.mean(replicate_coefficients, axis=0)
        se_coefficients = np.std(
            replicate_coefficients, axis=0, ddof=1
        ) / math.sqrt(arguments.replicates)
        for row, index in enumerate(arguments.indices):
            for degree in range(4):
                coefficient_records.append(
                    {
                        "index": index,
                        "degree": degree,
                        "mean": mean_coefficients[row, degree],
                        "standardError": se_coefficients[row, degree],
                    }
                )

        amplitude_grid = np.linspace(0.0, 1.0, arguments.amplitude_grid)
        powers = np.column_stack([amplitude_grid**degree for degree in range(4)])
        replicate_grid = np.einsum(
            "rid,gd->rig", replicate_coefficients, powers
        )
        mean_grid = np.mean(replicate_grid, axis=0)
        se_grid = np.std(replicate_grid, axis=0, ddof=1) / math.sqrt(
            arguments.replicates
        )
        lower_grid = mean_grid - 1.96 * se_grid
        upper_grid = mean_grid + 1.96 * se_grid
        minimum_mean = np.min(mean_grid, axis=0)
        best_position = int(np.argmax(minimum_mean))
        pointwise_excluded = np.any(upper_grid < 0.0, axis=0)

        root_records: list[dict[str, object]] = []
        mean_roots: dict[str, list[float]] = {}
        for row, index in enumerate(arguments.indices):
            roots = np.roots(mean_coefficients[row, ::-1])
            in_unit = sorted(
                float(root.real)
                for root in roots
                if abs(root.imag) < 1.0e-9 and 0.0 <= root.real <= 1.0
            )
            mean_roots[str(index)] = in_unit
            for replicate in range(arguments.replicates):
                roots = np.roots(replicate_coefficients[replicate, row, ::-1])
                for root in roots:
                    if abs(root.imag) < 1.0e-9 and 0.0 <= root.real <= 1.0:
                        root_records.append(
                            {
                                "replicate": replicate,
                                "index": index,
                                "root": float(root.real),
                            }
                        )

        scan_records: list[dict[str, object]] = []
        for position, amplitude in enumerate(amplitude_grid):
            record: dict[str, object] = {
                "amplitude": float(amplitude),
                "minimumMean": float(minimum_mean[position]),
                "pointwiseExcludedByUpperBand": bool(
                    pointwise_excluded[position]
                ),
            }
            for row, index in enumerate(arguments.indices):
                record.update(
                    {
                        f"j{index}Mean": float(mean_grid[row, position]),
                        f"j{index}StandardError": float(se_grid[row, position]),
                        f"j{index}Ci95Lower": float(lower_grid[row, position]),
                        f"j{index}Ci95Upper": float(upper_grid[row, position]),
                    }
                )
            scan_records.append(record)

        audits_passed = bool(
            reconstruction_residual_max < 1.0e-11
            and np.max(
                np.abs(VANDERMONDE @ VANDERMONDE_INVERSE - np.eye(4))
            )
            < 1.0e-13
        )
        result = {
            "schemaVersion": "1.0",
            "release": "R0.69V-zonepair-polynomial",
            "status": "passed" if audits_passed else "failed",
            "claimBoundary": (
                "independent randomized QMC root-gap diagnostic; pointwise "
                "scramble bands are not simultaneous rigorous enclosures"
            ),
            "method": {
                "separation": arguments.separation,
                "epsilon": epsilon,
                "indices": list(arguments.indices),
                "replicates": arguments.replicates,
                "pointsPerZonePair": 2**arguments.power,
                "zonePairs": len(zone_pairs),
                "sampledPointPairs": (
                    arguments.replicates
                    * len(zone_pairs)
                    * 2**arguments.power
                ),
                "amplitudeNodes": AMPLITUDE_NODES.tolist(),
                "amplitudeGridPoints": arguments.amplitude_grid,
            },
            "audits": {
                "vandermondeResidualMax": float(
                    np.max(
                        np.abs(
                            VANDERMONDE @ VANDERMONDE_INVERSE - np.eye(4)
                        )
                    )
                ),
                "sampleNodeReconstructionResidualMax": (
                    reconstruction_residual_max
                ),
                "sourceCommitMatchesHead": (
                    arguments.source_commit is None
                    or arguments.source_commit == head_commit
                ),
                "allUnorderedZonePairsRetained": True,
            },
            "rootGapDiagnostic": {
                "meanRootsInUnitInterval": mean_roots,
                "noCommonNonnegativeMeanOnGrid": bool(
                    np.all(minimum_mean < 0.0)
                ),
                "bestMinimumMeanAmplitude": float(
                    amplitude_grid[best_position]
                ),
                "bestMinimumMean": float(minimum_mean[best_position]),
                "pointwiseUpperBandExcludesCommonNonnegativeOnGrid": bool(
                    np.all(pointwise_excluded)
                ),
            },
            "provenance": {
                "script": str(source_path.relative_to(Path.cwd())),
                "scriptSha256": sha256(source_path),
                "sourceCommit": head_commit,
                "python": sys.version,
                "platform": platform.platform(),
                "numpy": np.__version__,
                "scipy": scipy.__version__,
            },
        }

        replicate_records = []
        for replicate in range(arguments.replicates):
            record: dict[str, object] = {"replicate": replicate}
            for row, index in enumerate(arguments.indices):
                record.update(
                    {
                        f"j{index}C{degree}": replicate_coefficients[
                            replicate, row, degree
                        ]
                        for degree in range(4)
                    }
                )
            replicate_records.append(record)

        outputs = (
            ("replicates.csv", replicate_records),
            ("pair-coefficients.csv", pair_records),
            ("coefficients.csv", coefficient_records),
            ("amplitude-sign-scan.csv", scan_records),
            ("roots.csv", root_records),
        )
        for file_name, records in outputs:
            with (output_root / file_name).open(
                "w", newline="", encoding="utf-8"
            ) as stream:
                writer = csv.DictWriter(stream, fieldnames=records[0].keys())
                writer.writeheader()
                writer.writerows(records)
        (output_root / "result.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        write_progress(
            progress,
            started,
            "completed",
            **result["rootGapDiagnostic"],
        )
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
