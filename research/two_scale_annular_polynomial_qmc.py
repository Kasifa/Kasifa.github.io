#!/usr/bin/env python3
"""R0.69V common-sample cubic reconstruction of every full annular carrier.

At fixed dyadic separation, the vorticity is affine in the outer amplitude a,
so every signed two-increment annulus is a cubic polynomial in a.  Four common
amplitude nodes reconstruct that polynomial exactly at the sample level.
The resulting coefficient means can be scanned on a continuous amplitude
grid without rerunning the point-pair integral.

This is randomized QMC evidence.  Scramble intervals are diagnostics and the
dense amplitude scan is not an interval proof.
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
from two_scale_annular_importance_qmc import map_sobol_to_x_and_displacement
from two_scale_full_annular_qmc import (
    KERNEL_FACTOR,
    deterministic_building_coefficients,
    deterministic_total,
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


def sample_annular_node_means(
    unit: np.ndarray,
    x_zone_index: int,
    zones: tuple[tuple[float, float], ...],
    epsilon: float,
    annular_index: int,
) -> tuple[np.ndarray, dict[int, np.ndarray]]:
    distance_lower = 2.0**annular_index
    distance_upper = min(4.0, 2.0 ** (annular_index + 2))
    if distance_lower >= distance_upper:
        return np.zeros(4), {}

    x_zone = zones[x_zone_index]
    x, displacement, distance = map_sobol_to_x_and_displacement(
        unit, x_zone, distance_lower, distance_upper
    )
    y = x + displacement
    y_radius = np.linalg.norm(y, axis=1)
    boundaries = np.asarray(
        [zones[0][0], *[zone[1] for zone in zones]], dtype=np.float64
    )
    y_zone_indices = np.searchsorted(boundaries, y_radius, side="right") - 1
    inside = (y_radius < 2.0) & (y_zone_indices >= x_zone_index)

    outer_x = compact_vorticity(x, 1.0)
    outer_y = compact_vorticity(y, 1.0)
    inner_x = compact_vorticity(x, epsilon)
    inner_y = compact_vorticity(y, epsilon)
    direction = displacement / distance[:, None]
    weight = cutoff_value(distance / (2.0 ** (annular_index + 1))) - cutoff_value(
        distance / (2.0**annular_index)
    )
    pair_factor = np.where(y_zone_indices == x_zone_index, 1.0, 2.0)
    measure = shell_volume(*x_zone) * shell_volume(
        distance_lower, distance_upper
    )
    common = (
        measure
        * KERNEL_FACTOR
        * weight
        * pair_factor
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
        values_at_nodes[node_index] = np.where(
            inside, common * geometric, 0.0
        )

    pair_node_means: dict[int, np.ndarray] = {}
    for y_zone_index in range(x_zone_index, len(zones)):
        mask = inside & (y_zone_indices == y_zone_index)
        pair_node_means[y_zone_index] = np.mean(
            np.where(mask[None, :], values_at_nodes, 0.0), axis=1
        )
    return np.mean(values_at_nodes, axis=1), pair_node_means


def evaluate_coefficients(coefficients: np.ndarray, amplitude: np.ndarray) -> np.ndarray:
    return sum(
        coefficients[..., degree] * amplitude**degree for degree in range(4)
    )


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--replicates", type=int, default=8)
    parser.add_argument("--power", type=int, default=15)
    parser.add_argument("--separation", type=int, default=2)
    parser.add_argument("--j-padding", type=int, default=8)
    parser.add_argument("--amplitude-grid", type=int, default=2001)
    parser.add_argument("--seed-base", type=int, default=691101)
    parser.add_argument("--source-commit")
    arguments = parser.parse_args()
    if arguments.replicates < 2:
        parser.error("--replicates must be at least two")
    if arguments.power < 1 or arguments.j_padding < 2:
        parser.error("invalid QMC power or annular padding")
    if arguments.separation < 1:
        parser.error("--separation must be positive")
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
    progress_path = output_root / "progress.ndjson"
    started = time.perf_counter()
    epsilon = 2.0 ** (-arguments.separation)
    zones = radial_zones(epsilon)
    indices = tuple(
        range(-arguments.separation - arguments.j_padding, 2)
    )
    replicate_records: list[dict[str, object]] = []
    pair_records: list[dict[str, object]] = []
    sample_node_reconstruction_residual_max = 0.0

    with progress_path.open("w", encoding="utf-8") as progress:
        write_progress(
            progress,
            started,
            "started",
            separation=arguments.separation,
            epsilon=epsilon,
            replicates=arguments.replicates,
            pointsPerAnnulusZone=2**arguments.power,
            amplitudeNodes=AMPLITUDE_NODES.tolist(),
        )
        for replicate in range(arguments.replicates):
            annular_coefficients: dict[int, np.ndarray] = {}
            for index in indices:
                node_means = np.zeros(4, dtype=np.float64)
                for x_zone_index, x_zone in enumerate(zones):
                    seed = (
                        arguments.seed_base
                        + replicate * 100_000
                        + (index + arguments.separation + arguments.j_padding)
                        * 1_000
                        + x_zone_index
                    )
                    sampler = qmc.Sobol(d=5, scramble=True, seed=seed)
                    unit = sampler.random_base2(arguments.power)
                    stratum_nodes, pair_nodes = sample_annular_node_means(
                        unit,
                        x_zone_index,
                        zones,
                        epsilon,
                        index,
                    )
                    node_means += stratum_nodes
                    for y_zone_index, values in pair_nodes.items():
                        coefficients = VANDERMONDE_INVERSE @ values
                        pair_records.append(
                            {
                                "replicate": replicate,
                                "index": index,
                                "xZone": x_zone_index,
                                "yZone": y_zone_index,
                                "xRole": zone_role(x_zone, epsilon),
                                "yRole": zone_role(
                                    zones[y_zone_index], epsilon
                                ),
                                "pairClass": (
                                    f"{zone_role(x_zone, epsilon)}--"
                                    f"{zone_role(zones[y_zone_index], epsilon)}"
                                ),
                                **{
                                    f"c{degree}": coefficients[degree]
                                    for degree in range(4)
                                },
                            }
                        )
                coefficients = VANDERMONDE_INVERSE @ node_means
                sample_node_reconstruction_residual_max = max(
                    sample_node_reconstruction_residual_max,
                    float(np.max(np.abs(VANDERMONDE @ coefficients - node_means))),
                )
                annular_coefficients[index] = coefficients
            total_coefficients = sum(annular_coefficients.values())
            replicate_records.append(
                {
                    "replicate": replicate,
                    "separation": arguments.separation,
                    "epsilon": epsilon,
                    "zones": len(zones),
                    "jMin": indices[0],
                    "jMax": indices[-1],
                    "pointsPerAnnulusZone": 2**arguments.power,
                    **{
                        f"totalC{degree}": total_coefficients[degree]
                        for degree in range(4)
                    },
                    **{
                        f"j{index}C{degree}": annular_coefficients[index][degree]
                        for index in indices
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
                totalCoefficients=total_coefficients.tolist(),
            )

        coefficient_records: list[dict[str, object]] = []
        mean_coefficients = np.empty((len(indices), 4), dtype=np.float64)
        se_coefficients = np.empty((len(indices), 4), dtype=np.float64)
        for row, index in enumerate(indices):
            for degree in range(4):
                mean, se = mean_and_se(
                    [
                        float(record[f"j{index}C{degree}"])
                        for record in replicate_records
                    ]
                )
                mean_coefficients[row, degree] = mean
                se_coefficients[row, degree] = se
                coefficient_records.append(
                    {
                        "index": index,
                        "degree": degree,
                        "mean": mean,
                        "standardError": se,
                    }
                )

        V_q, _, C_q = deterministic_building_coefficients(160)
        exact_total_coefficients = np.asarray(
            [
                epsilon**3 * V_q,
                epsilon**3 * (-3.0 * V_q + C_q),
                epsilon**3 * (3.0 * V_q - 2.0 * C_q),
                V_q - epsilon**3 * V_q + epsilon**3 * C_q,
            ],
            dtype=np.float64,
        )
        deterministic_node_values = np.asarray(
            [
                deterministic_total(epsilon, float(amplitude), 160, 20)
                for amplitude in AMPLITUDE_NODES
            ],
            dtype=np.float64,
        )
        deterministic_node_reconstruction = VANDERMONDE @ exact_total_coefficients
        deterministic_node_residual_max = float(
            np.max(
                np.abs(
                    deterministic_node_reconstruction - deterministic_node_values
                )
            )
        )
        sampled_total_coefficients = np.sum(mean_coefficients, axis=0)
        sampled_total_se = np.empty(4, dtype=np.float64)
        for degree in range(4):
            _, sampled_total_se[degree] = mean_and_se(
                [
                    float(record[f"totalC{degree}"])
                    for record in replicate_records
                ]
            )

        amplitude_grid = np.linspace(0.0, 1.0, arguments.amplitude_grid)
        annular_grid = np.column_stack(
            [
                evaluate_coefficients(mean_coefficients, amplitude)
                for amplitude in amplitude_grid
            ]
        )
        signed_grid = np.sum(annular_grid, axis=0)
        l1_grid = np.sum(np.abs(annular_grid), axis=0)
        ratio_grid = np.divide(
            np.abs(signed_grid),
            l1_grid,
            out=np.full_like(signed_grid, np.nan),
            where=l1_grid > 0.0,
        )
        minimum_grid = np.min(annular_grid, axis=0)
        negative_count_grid = np.sum(annular_grid < 0.0, axis=0)
        best_index = int(np.nanargmax(ratio_grid))
        best_amplitude = float(amplitude_grid[best_index])

        # Pointwise scramble bands on the candidate amplitude.  These are not
        # simultaneous or rigorous confidence intervals.
        candidate_values: list[dict[str, object]] = []
        candidate_replicate_annuli = np.empty(
            (arguments.replicates, len(indices)), dtype=np.float64
        )
        for row, index in enumerate(indices):
            values = [
                float(
                    evaluate_coefficients(
                        np.asarray(
                            [
                                record[f"j{index}C{degree}"]
                                for degree in range(4)
                            ],
                            dtype=np.float64,
                        ),
                        best_amplitude,
                    )
                )
                for record in replicate_records
            ]
            candidate_replicate_annuli[:, row] = values
            mean, se = mean_and_se(values)
            candidate_values.append(
                {
                    "index": index,
                    "mean": mean,
                    "standardError": se,
                    "ci95Lower": mean - 1.96 * se,
                    "ci95Upper": mean + 1.96 * se,
                }
            )
        candidate_replicate_signed = np.sum(candidate_replicate_annuli, axis=1)
        candidate_replicate_l1 = np.sum(
            np.abs(candidate_replicate_annuli), axis=1
        )
        candidate_replicate_ratio = np.divide(
            np.abs(candidate_replicate_signed),
            candidate_replicate_l1,
            out=np.full(arguments.replicates, np.nan),
            where=candidate_replicate_l1 > 0.0,
        )
        candidate_ratio_mean, candidate_ratio_se = mean_and_se(
            candidate_replicate_ratio.tolist()
        )

        scan_records = [
            {
                "amplitude": float(amplitude_grid[position]),
                "signedSum": float(signed_grid[position]),
                "annularL1": float(l1_grid[position]),
                "cancellationRatio": float(ratio_grid[position]),
                "minimumAnnulus": float(minimum_grid[position]),
                "negativeAnnulusCount": int(negative_count_grid[position]),
            }
            for position in range(arguments.amplitude_grid)
        ]
        deterministic_audits_passed = bool(
            np.max(np.abs(VANDERMONDE @ VANDERMONDE_INVERSE - np.eye(4)))
            < 1.0e-13
            and sample_node_reconstruction_residual_max < 1.0e-11
            and deterministic_node_residual_max < 1.0e-6
        )
        result = {
            "schemaVersion": "1.0",
            "release": "R0.69V-polynomial",
            "status": "passed" if deterministic_audits_passed else "failed",
            "claimBoundary": (
                "common-sample cubic QMC and dense amplitude scan; pointwise "
                "scramble bands are neither simultaneous nor rigorous enclosures"
            ),
            "method": {
                "separation": arguments.separation,
                "epsilon": epsilon,
                "amplitudeNodes": AMPLITUDE_NODES.tolist(),
                "replicates": arguments.replicates,
                "pointsPerAnnulusZone": 2**arguments.power,
                "indices": list(indices),
                "zones": [list(zone) for zone in zones],
                "amplitudeGridPoints": arguments.amplitude_grid,
                "sampledPointPairs": (
                    arguments.replicates
                    * len(indices)
                    * len(zones)
                    * 2**arguments.power
                ),
            },
            "audits": {
                "vandermondeResidualMax": float(
                    np.max(
                        np.abs(
                            VANDERMONDE @ VANDERMONDE_INVERSE
                            - np.eye(4)
                        )
                    )
                ),
                "sampleNodeReconstructionResidualMax": (
                    sample_node_reconstruction_residual_max
                ),
                "deterministicNodeValues": deterministic_node_values.tolist(),
                "deterministicNodeReconstruction": (
                    deterministic_node_reconstruction.tolist()
                ),
                "deterministicNodeResidualMax": deterministic_node_residual_max,
                "deterministicNodeResidualTolerance": 1.0e-6,
                "sampledTotalCoefficients": sampled_total_coefficients.tolist(),
                "sampledTotalCoefficientStandardErrors": sampled_total_se.tolist(),
                "deterministicTotalCoefficients": exact_total_coefficients.tolist(),
                "totalCoefficientZScores": (
                    (sampled_total_coefficients - exact_total_coefficients)
                    / sampled_total_se
                ).tolist(),
                "sourceCommitMatchesHead": (
                    arguments.source_commit is None
                    or arguments.source_commit == head_commit
                ),
                "transitionTransitionPairsRetained": True,
                "deterministicAuditsPassed": deterministic_audits_passed,
            },
            "candidate": {
                "bestAmplitude": best_amplitude,
                "cancellationRatioOfMeans": float(ratio_grid[best_index]),
                "signedSumOfMeans": float(signed_grid[best_index]),
                "annularL1OfMeans": float(l1_grid[best_index]),
                "minimumAnnulusMean": float(minimum_grid[best_index]),
                "negativeAnnulusCount": int(negative_count_grid[best_index]),
                "replicateCancellationRatioMean": candidate_ratio_mean,
                "replicateCancellationRatioStandardError": candidate_ratio_se,
                "replicateCancellationRatios": candidate_replicate_ratio.tolist(),
                "annuli": candidate_values,
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

        with (output_root / "replicates.csv").open(
            "w", newline="", encoding="utf-8"
        ) as stream:
            writer = csv.DictWriter(
                stream,
                fieldnames=sorted(
                    {key for record in replicate_records for key in record}
                ),
            )
            writer.writeheader()
            writer.writerows(replicate_records)
        with (output_root / "pair-coefficients.csv").open(
            "w", newline="", encoding="utf-8"
        ) as stream:
            writer = csv.DictWriter(stream, fieldnames=pair_records[0].keys())
            writer.writeheader()
            writer.writerows(pair_records)
        with (output_root / "coefficients.csv").open(
            "w", newline="", encoding="utf-8"
        ) as stream:
            writer = csv.DictWriter(
                stream, fieldnames=coefficient_records[0].keys()
            )
            writer.writeheader()
            writer.writerows(coefficient_records)
        with (output_root / "amplitude-scan.csv").open(
            "w", newline="", encoding="utf-8"
        ) as stream:
            writer = csv.DictWriter(stream, fieldnames=scan_records[0].keys())
            writer.writeheader()
            writer.writerows(scan_records)
        with (output_root / "candidate-annuli.csv").open(
            "w", newline="", encoding="utf-8"
        ) as stream:
            writer = csv.DictWriter(stream, fieldnames=candidate_values[0].keys())
            writer.writeheader()
            writer.writerows(candidate_values)
        (output_root / "result.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        write_progress(
            progress,
            started,
            "completed",
            bestAmplitude=best_amplitude,
            cancellationRatio=result["candidate"]["cancellationRatioOfMeans"],
            negativeAnnulusCount=result["candidate"]["negativeAnnulusCount"],
        )
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
