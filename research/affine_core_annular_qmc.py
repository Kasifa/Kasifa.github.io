#!/usr/bin/env python3
"""R0.69T monitored QMC audit of the affine-core boundary carrier.

The compact divergence-free field is

    v_A = curl(chi_0 B_A),  B_A = -(1/3) x cross (A x),

where chi_0 is the standard C-infinity radial cutoff equal to one on B_1
and zero outside B_2.  The trace-free affine core uses

    S = diag(-1,-1,2)/sqrt(6),  omega = (0,0,1).

For x in B_1 the exact boundary-carrier identity is integrated over
y in B_2 minus B_1.  Simultaneous axial rotation invariance removes one
common azimuth, leaving a five-dimensional scrambled Sobol integral.

This is exploratory quadrature, not an interval proof or a regularity result.
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
import sys
import time

import numpy as np
import scipy
from scipy.special import expit
from scipy.stats import qmc


CORE_VOLUME = 4.0 * math.pi / 3.0
SHELL_VOLUME = 28.0 * math.pi / 3.0
MEASURE_FACTOR = CORE_VOLUME * SHELL_VOLUME
KERNEL_FACTOR = 3.0 / (4.0 * math.pi)
EXACT_CORE_PRODUCTION = 8.0 * math.pi / (3.0 * math.sqrt(6.0))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def cutoff_value(radius: np.ndarray) -> np.ndarray:
    """C-infinity cutoff: one on [0,1], zero on [2,infinity)."""

    radius = np.asarray(radius, dtype=np.float64)
    result = np.zeros_like(radius)
    result[radius <= 1.0] = 1.0
    active = (radius > 1.0) & (radius < 2.0)
    t = radius[active] - 1.0
    exponent = -1.0 / t + 1.0 / (1.0 - t)
    result[active] = expit(-exponent)
    return result


def cutoff_value_derivatives(radius: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return chi_0, chi_0', chi_0'' with respect to radius."""

    radius = np.asarray(radius, dtype=np.float64)
    value = np.zeros_like(radius)
    first = np.zeros_like(radius)
    second = np.zeros_like(radius)
    value[radius <= 1.0] = 1.0
    active = (radius > 1.0) & (radius < 2.0)
    t = radius[active] - 1.0
    exponent = -1.0 / t + 1.0 / (1.0 - t)
    derivative = 1.0 / t**2 + 1.0 / (1.0 - t) ** 2
    second_derivative = -2.0 / t**3 + 2.0 / (1.0 - t) ** 3
    chi = expit(-exponent)
    product = chi * (1.0 - chi)
    value[active] = chi
    first[active] = -product * derivative
    second[active] = product * (
        (1.0 - 2.0 * chi) * derivative**2 - second_derivative
    )
    return value, first, second


def compact_vorticity(points: np.ndarray) -> np.ndarray:
    """Analytic curl of curl(chi_0 B_A) for the declared affine matrix."""

    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]
    radius = np.linalg.norm(points, axis=1)
    chi, first, second = cutoff_value_derivatives(radius)
    safe_radius = np.where(radius > 0.0, radius, 1.0)
    sqrt6 = math.sqrt(6.0)

    omega_x = z * (
        -4.0 * x * first
        + 6.0 * sqrt6 * y * first
        + (-x + sqrt6 * y) * radius * second
    ) / (6.0 * safe_radius)
    omega_y = z * (
        -6.0 * sqrt6 * x * first
        - 4.0 * y * first
        + (-sqrt6 * x - y) * radius * second
    ) / (6.0 * safe_radius)
    rho2 = x * x + y * y
    omega_z = (
        chi
        + rho2 * second / 6.0
        + (rho2 + z * z / 3.0) * first / safe_radius
    )
    return np.column_stack((omega_x, omega_y, omega_z))


def map_sobol_to_pair(unit: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Map five uniforms to B_1 and the shell B_2 minus B_1."""

    core_radius = unit[:, 0] ** (1.0 / 3.0)
    core_cosine = 1.0 - 2.0 * unit[:, 1]
    core_sine = np.sqrt(np.maximum(0.0, 1.0 - core_cosine**2))
    x = np.column_stack(
        (core_radius * core_sine, np.zeros_like(core_radius), core_radius * core_cosine)
    )

    shell_radius = (1.0 + 7.0 * unit[:, 2]) ** (1.0 / 3.0)
    shell_cosine = 1.0 - 2.0 * unit[:, 3]
    shell_sine = np.sqrt(np.maximum(0.0, 1.0 - shell_cosine**2))
    azimuth = 2.0 * math.pi * unit[:, 4]
    y = np.column_stack(
        (
            shell_radius * shell_sine * np.cos(azimuth),
            shell_radius * shell_sine * np.sin(azimuth),
            shell_radius * shell_cosine,
        )
    )
    return x, y


def sample_integrands(
    unit: np.ndarray, j_min: int, j_max: int
) -> tuple[np.ndarray, dict[int, np.ndarray], np.ndarray, float]:
    x, y = map_sobol_to_pair(unit)
    displacement = y - x
    distance = np.linalg.norm(displacement, axis=1)
    direction = displacement / distance[:, None]
    omega_y = compact_vorticity(y)

    # omega_x=(0,0,1), hence omega_y cross omega_x=(omega_y_y,-omega_y_x,0).
    geometric = direction[:, 2] * (
        direction[:, 0] * omega_y[:, 1] - direction[:, 1] * omega_y[:, 0]
    )
    base = MEASURE_FACTOR * KERNEL_FACTOR * geometric / distance**3

    annular: dict[int, np.ndarray] = {}
    partition_sum = np.zeros_like(distance)
    for index in range(j_min, j_max + 1):
        weight = cutoff_value(distance / (2.0 ** (index + 1))) - cutoff_value(
            distance / (2.0**index)
        )
        annular[index] = base * weight
        partition_sum += weight
    near_weight = cutoff_value(distance / (2.0**j_min))
    far_weight = 1.0 - cutoff_value(distance / (2.0 ** (j_max + 1)))
    partition_residual = float(
        np.max(np.abs(partition_sum + near_weight + far_weight - 1.0))
    )
    return base, annular, base * near_weight, partition_residual


def mean_and_se(values: list[float]) -> tuple[float, float]:
    array = np.asarray(values, dtype=np.float64)
    mean = float(np.mean(array))
    if array.size < 2:
        return mean, math.nan
    return mean, float(np.std(array, ddof=1) / math.sqrt(array.size))


def write_progress(stream, started: float, event: str, **fields: object) -> None:
    record = {
        "timestampUtc": datetime.now(timezone.utc).isoformat(),
        "elapsedSeconds": round(time.perf_counter() - started, 6),
        "event": event,
        **fields,
    }
    stream.write(json.dumps(record, sort_keys=True) + "\n")
    stream.flush()
    print(json.dumps(record, sort_keys=True), flush=True)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--replicates", type=int, default=8)
    parser.add_argument("--power", type=int, default=19)
    parser.add_argument("--refinement-powers", default="15,17,19")
    parser.add_argument("--j-min", type=int, default=-8)
    parser.add_argument("--j-max", type=int, default=1)
    parser.add_argument("--seed-base", type=int, default=690701)
    arguments = parser.parse_args()
    arguments.refinement_powers = tuple(
        sorted({int(value) for value in arguments.refinement_powers.split(",")})
    )
    if arguments.replicates < 2:
        parser.error("--replicates must be at least two for a scramble error estimate")
    if not arguments.refinement_powers or arguments.refinement_powers[-1] != arguments.power:
        parser.error("refinement powers must end at --power")
    if arguments.refinement_powers[0] < 1 or arguments.j_min > arguments.j_max:
        parser.error("invalid refinement powers or annular window")
    return arguments


def main() -> int:
    arguments = parse_arguments()
    source_path = Path(__file__).resolve()
    output_root = arguments.output_root
    output_root.mkdir(parents=True, exist_ok=True)
    progress_path = output_root / "progress.ndjson"
    started = time.perf_counter()
    indices = tuple(range(arguments.j_min, arguments.j_max + 1))
    replicate_records: list[dict[str, object]] = []
    partition_residual_max = 0.0

    with progress_path.open("w", encoding="utf-8") as progress:
        write_progress(
            progress,
            started,
            "started",
            replicates=arguments.replicates,
            pointsPerReplicate=2**arguments.power,
            jMin=arguments.j_min,
            jMax=arguments.j_max,
        )
        for replicate in range(arguments.replicates):
            seed = arguments.seed_base + replicate
            sampler = qmc.Sobol(d=5, scramble=True, seed=seed)
            unit = sampler.random_base2(arguments.power)
            base, annular, near, partition_residual = sample_integrands(
                unit, arguments.j_min, arguments.j_max
            )
            partition_residual_max = max(partition_residual_max, partition_residual)
            for power in arguments.refinement_powers:
                count = 2**power
                total = float(np.mean(base[:count]))
                pieces = {index: float(np.mean(annular[index][:count])) for index in indices}
                near_value = float(np.mean(near[:count]))
                reconstructed = near_value + sum(pieces.values())
                replicate_records.append(
                    {
                        "replicate": replicate,
                        "seed": seed,
                        "power": power,
                        "points": count,
                        "total": total,
                        "nearRemainder": near_value,
                        "reconstructed": reconstructed,
                        "sampleReconstructionResidual": reconstructed - total,
                        **{f"j{index}": pieces[index] for index in indices},
                    }
                )
            write_progress(
                progress,
                started,
                "replicate-complete",
                replicate=replicate + 1,
                replicates=arguments.replicates,
                finestTotal=replicate_records[-1]["total"],
                exactCore=EXACT_CORE_PRODUCTION,
            )

        refinement_records: list[dict[str, object]] = []
        annular_records: list[dict[str, object]] = []
        for power in arguments.refinement_powers:
            records = [record for record in replicate_records if record["power"] == power]
            total_mean, total_se = mean_and_se([float(record["total"]) for record in records])
            near_mean, near_se = mean_and_se(
                [float(record["nearRemainder"]) for record in records]
            )
            reconstruction_mean, reconstruction_se = mean_and_se(
                [float(record["reconstructed"]) for record in records]
            )
            signed_pieces: list[float] = []
            for index in indices:
                mean, se = mean_and_se([float(record[f"j{index}"]) for record in records])
                signed_pieces.append(mean)
                if power == arguments.power:
                    annular_records.append(
                        {
                            "index": index,
                            "lengthLower": 2.0**index,
                            "lengthUpper": 2.0 ** (index + 2),
                            "mean": mean,
                            "standardError": se,
                            "ci95Lower": mean - 1.96 * se,
                            "ci95Upper": mean + 1.96 * se,
                        }
                    )
            cancellation_ratio = abs(sum(signed_pieces)) / sum(
                abs(value) for value in signed_pieces
            )
            refinement_records.append(
                {
                    "power": power,
                    "pointsPerReplicate": 2**power,
                    "totalMean": total_mean,
                    "totalStandardError": total_se,
                    "exactCoreProduction": EXACT_CORE_PRODUCTION,
                    "absoluteError": total_mean - EXACT_CORE_PRODUCTION,
                    "zScore": (total_mean - EXACT_CORE_PRODUCTION) / total_se,
                    "reconstructedMean": reconstruction_mean,
                    "reconstructedStandardError": reconstruction_se,
                    "nearRemainderMean": near_mean,
                    "nearRemainderStandardError": near_se,
                    "annularCancellationRatioWithoutNearTail": cancellation_ratio,
                }
            )

        finest = refinement_records[-1]
        checks = {
            "analyticCoreValuePositive": EXACT_CORE_PRODUCTION > 0.0,
            "annularPartitionResidualBelow1e-14": partition_residual_max < 1.0e-14,
            "samplewiseWindowReconstructionBelow1e-12": max(
                abs(float(record["sampleReconstructionResidual"]))
                for record in replicate_records
            )
            < 1.0e-12,
            "finestMeanWithinFourScrambleStandardErrors": abs(float(finest["zScore"])) < 4.0,
            "nearRemainderResolvedBelowOnePercent": abs(
                float(finest["nearRemainderMean"])
            )
            < 0.01 * EXACT_CORE_PRODUCTION,
        }
        write_progress(progress, started, "completed", checks=checks)

    replicate_path = output_root / "replicates.csv"
    refinement_path = output_root / "refinement.csv"
    annular_path = output_root / "annular_summary.csv"
    with replicate_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(replicate_records[0].keys()))
        writer.writeheader()
        writer.writerows(replicate_records)
    with refinement_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(refinement_records[0].keys()))
        writer.writeheader()
        writer.writerows(refinement_records)
    with annular_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(annular_records[0].keys()))
        writer.writeheader()
        writer.writerows(annular_records)

    result_path = output_root / "result.json"
    result = {
        "schemaVersion": 1,
        "audit": "R0.69T affine-core annular boundary-carrier QMC",
        "source": {"path": str(source_path), "sha256": sha256(source_path)},
        "classification": "exploratory scrambled-Sobol quadrature",
        "claimBoundary": [
            "not an interval enclosure",
            "not a universal annular depletion theorem",
            "not a Navier-Stokes regularity criterion",
            "not a solution of the Millennium Problem",
        ],
        "field": {
            "strain": "diag(-1,-1,2)/sqrt(6)",
            "coreVorticity": [0, 0, 1],
            "vectorPotential": "B_A=-(1/3) x cross (A x)",
            "compactVelocity": "v_A=curl(chi_0 B_A)",
            "cutoff": "standard C-infinity radial step, 1 on r<=1 and 0 on r>=2",
        },
        "quadrature": {
            "method": "independently scrambled Sobol",
            "dimension": 5,
            "symmetryReduction": "fixed core azimuth by simultaneous axial rotation invariance",
            "replicates": arguments.replicates,
            "power": arguments.power,
            "pointsPerReplicate": 2**arguments.power,
            "totalFinestPoints": arguments.replicates * 2**arguments.power,
            "seedBase": arguments.seed_base,
            "refinementPowers": arguments.refinement_powers,
            "annularIndices": [arguments.j_min, arguments.j_max],
        },
        "exactCoreProduction": EXACT_CORE_PRODUCTION,
        "finest": finest,
        "annularFinest": annular_records,
        "refinement": refinement_records,
        "partitionResidualMax": partition_residual_max,
        "checks": checks,
        "allChecksPass": all(checks.values()),
        "software": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
        },
        "elapsedSeconds": time.perf_counter() - started,
    }
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    hashes = {
        path.name: sha256(path)
        for path in (result_path, replicate_path, refinement_path, annular_path, progress_path)
    }
    (output_root / "SHA256SUMS").write_text(
        "".join(f"{digest}  {name}\n" for name, digest in sorted(hashes.items())),
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["allChecksPass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
