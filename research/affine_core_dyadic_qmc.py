#!/usr/bin/env python3
"""Monitored finite-radius QMC companion for the R0.69U theorem.

The field cutoff is the explicit mollification used in the analytic proof:
the beta density on [1/20,19/20] is convolved with the standard even
C-infinity mollifier of radius 1/40.  The same radial cutoff defines the
physical annular partition.

This computation checks finite dyadic radii.  It is randomized quadrature,
not an interval proof; the theorem and its positive rational margin are
independent of this script.
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
from scipy.integrate import quad
from scipy.stats import qmc


CORE_VOLUME = 4.0 * math.pi / 3.0
UNIT_SHELL_VOLUME = 28.0 * math.pi / 3.0
KERNEL_FACTOR = 3.0 / (4.0 * math.pi)
EXACT_CORE_PRODUCTION = 8.0 * math.pi / (3.0 * math.sqrt(6.0))
TRANSITION_A = 1.0 / 20.0
TRANSITION_B = 19.0 / 20.0
TRANSITION_LENGTH = TRANSITION_B - TRANSITION_A
MOLLIFIER_RADIUS = 1.0 / 40.0
ACTIVE_LOW = 1.0 + TRANSITION_A - MOLLIFIER_RADIUS
ACTIVE_HIGH = 1.0 + TRANSITION_B + MOLLIFIER_RADIUS
QUADRATURE_ORDER = 48
EVALUATION_CHUNK = 65_536


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def base_density(t: np.ndarray) -> np.ndarray:
    t = np.asarray(t, dtype=np.float64)
    value = np.zeros_like(t)
    active = (t >= TRANSITION_A) & (t <= TRANSITION_B)
    z = (t[active] - TRANSITION_A) / TRANSITION_LENGTH
    value[active] = 30.0 / TRANSITION_LENGTH * z**2 * (1.0 - z) ** 2
    return value


def base_density_derivative(t: np.ndarray) -> np.ndarray:
    t = np.asarray(t, dtype=np.float64)
    value = np.zeros_like(t)
    active = (t >= TRANSITION_A) & (t <= TRANSITION_B)
    z = (t[active] - TRANSITION_A) / TRANSITION_LENGTH
    value[active] = (
        60.0
        / TRANSITION_LENGTH**2
        * z
        * (1.0 - z)
        * (1.0 - 2.0 * z)
    )
    return value


def base_survival(t: np.ndarray) -> np.ndarray:
    t = np.asarray(t, dtype=np.float64)
    value = np.ones_like(t)
    value[t >= TRANSITION_B] = 0.0
    active = (t > TRANSITION_A) & (t < TRANSITION_B)
    z = (t[active] - TRANSITION_A) / TRANSITION_LENGTH
    value[active] = 1.0 - (10.0 * z**3 - 15.0 * z**4 + 6.0 * z**5)
    return value


def mollifier_rule() -> tuple[np.ndarray, np.ndarray]:
    nodes, weights = np.polynomial.legendre.leggauss(QUADRATURE_ORDER)
    physical_nodes = MOLLIFIER_RADIUS * nodes
    physical_weights = MOLLIFIER_RADIUS * weights
    raw = np.exp(-1.0 / (1.0 - nodes**2))
    weighted = physical_weights * raw
    return physical_nodes, weighted / np.sum(weighted)


MOLLIFIER_NODES, MOLLIFIER_WEIGHTS = mollifier_rule()


def cutoff_value_derivatives(
    radius: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return q, q', q'' for the explicit mollified radial cutoff."""

    radius = np.asarray(radius, dtype=np.float64)
    shape = radius.shape
    flat = radius.reshape(-1)
    value = np.ones_like(flat)
    first = np.zeros_like(flat)
    second = np.zeros_like(flat)
    value[flat >= ACTIVE_HIGH] = 0.0
    active_indices = np.flatnonzero((flat > ACTIVE_LOW) & (flat < ACTIVE_HIGH))
    for start in range(0, active_indices.size, EVALUATION_CHUNK):
        indices = active_indices[start : start + EVALUATION_CHUNK]
        transition_coordinate = flat[indices, None] - 1.0 - MOLLIFIER_NODES[None, :]
        value[indices] = base_survival(transition_coordinate) @ MOLLIFIER_WEIGHTS
        first[indices] = -base_density(transition_coordinate) @ MOLLIFIER_WEIGHTS
        second[indices] = (
            -base_density_derivative(transition_coordinate) @ MOLLIFIER_WEIGHTS
        )
    return value.reshape(shape), first.reshape(shape), second.reshape(shape)


def cutoff_value(radius: np.ndarray) -> np.ndarray:
    return cutoff_value_derivatives(radius)[0]


def compact_vorticity(points: np.ndarray, radius_scale: float) -> np.ndarray:
    """Analytic curl curl(q(|x|/R) B_A) for the declared affine matrix."""

    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]
    radius = np.linalg.norm(points, axis=1)
    scaled_radius = radius / radius_scale
    chi, scaled_first, scaled_second = cutoff_value_derivatives(scaled_radius)
    first = scaled_first / radius_scale
    second = scaled_second / radius_scale**2
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


def map_sobol_to_pair(
    unit: np.ndarray, radius_scale: float
) -> tuple[np.ndarray, np.ndarray]:
    core_radius = unit[:, 0] ** (1.0 / 3.0)
    core_cosine = 1.0 - 2.0 * unit[:, 1]
    core_sine = np.sqrt(np.maximum(0.0, 1.0 - core_cosine**2))
    x = np.column_stack(
        (core_radius * core_sine, np.zeros_like(core_radius), core_radius * core_cosine)
    )

    shell_radius = radius_scale * (1.0 + 7.0 * unit[:, 2]) ** (1.0 / 3.0)
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
    unit: np.ndarray,
    radius_power: int,
    relative_min: int,
    relative_max: int,
) -> tuple[np.ndarray, dict[int, np.ndarray], np.ndarray, np.ndarray, float]:
    radius_scale = float(2**radius_power)
    x, y = map_sobol_to_pair(unit, radius_scale)
    displacement = y - x
    distance = np.linalg.norm(displacement, axis=1)
    direction = displacement / distance[:, None]
    omega_y = compact_vorticity(y, radius_scale)

    geometric = direction[:, 2] * (
        direction[:, 0] * omega_y[:, 1] - direction[:, 1] * omega_y[:, 0]
    )
    measure = CORE_VOLUME * UNIT_SHELL_VOLUME * radius_scale**3
    base = measure * KERNEL_FACTOR * geometric / distance**3

    annular: dict[int, np.ndarray] = {}
    partition_sum = np.zeros_like(distance)
    for relative in range(relative_min, relative_max + 1):
        index = radius_power + relative
        weight = cutoff_value(distance / (2.0 ** (index + 1))) - cutoff_value(
            distance / (2.0**index)
        )
        annular[relative] = base * weight
        partition_sum += weight
    lowest_index = radius_power + relative_min
    highest_index = radius_power + relative_max
    near_weight = cutoff_value(distance / (2.0**lowest_index))
    far_weight = 1.0 - cutoff_value(distance / (2.0 ** (highest_index + 1)))
    partition_residual = float(
        np.max(np.abs(partition_sum + near_weight + far_weight - 1.0))
    )
    return base, annular, base * near_weight, base * far_weight, partition_residual


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
    parser.add_argument("--power", type=int, default=18)
    parser.add_argument("--radius-powers", default="0,1,2,3,4,5,6")
    parser.add_argument("--relative-min", type=int, default=-8)
    parser.add_argument("--relative-max", type=int, default=2)
    parser.add_argument("--seed-base", type=int, default=690801)
    arguments = parser.parse_args()
    arguments.radius_powers = tuple(
        sorted({int(value) for value in arguments.radius_powers.split(",")})
    )
    if arguments.replicates < 2:
        parser.error("--replicates must be at least two")
    if arguments.power < 1 or arguments.relative_min > arguments.relative_max:
        parser.error("invalid QMC or annular parameters")
    if not arguments.radius_powers or arguments.radius_powers[0] < 0:
        parser.error("radius powers must be nonnegative")
    return arguments


def main() -> int:
    arguments = parse_arguments()
    output_root = arguments.output_root
    output_root.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    progress_path = output_root / "progress.ndjson"
    source_path = Path(__file__).resolve()
    relative_indices = tuple(range(arguments.relative_min, arguments.relative_max + 1))
    replicate_records: list[dict[str, object]] = []
    partition_residual_max = 0.0

    energy, energy_error = quad(
        lambda value: float(
            value * cutoff_value_derivatives(np.asarray([value]))[1][0] ** 2
        ),
        1.0,
        2.0,
        epsabs=1e-12,
        epsrel=1e-12,
        limit=300,
        points=[ACTIVE_LOW, 1.5, ACTIVE_HIGH],
    )
    limiting_inner = CORE_VOLUME * 2.0 / (5.0 * math.sqrt(6.0)) * (2.5 + energy)
    limiting_outer = CORE_VOLUME * 2.0 / (5.0 * math.sqrt(6.0)) * (2.5 - energy)

    with progress_path.open("w", encoding="utf-8") as progress:
        write_progress(
            progress,
            started,
            "started",
            replicates=arguments.replicates,
            pointsPerReplicate=2**arguments.power,
            radiusPowers=list(arguments.radius_powers),
        )
        for replicate in range(arguments.replicates):
            sampler = qmc.Sobol(
                d=5, scramble=True, seed=arguments.seed_base + replicate
            )
            unit = sampler.random_base2(arguments.power)
            for radius_power in arguments.radius_powers:
                base, annular, near, far, residual = sample_integrands(
                    unit,
                    radius_power,
                    arguments.relative_min,
                    arguments.relative_max,
                )
                partition_residual_max = max(partition_residual_max, residual)
                pieces = {
                    relative: float(np.mean(annular[relative]))
                    for relative in relative_indices
                }
                near_value = float(np.mean(near))
                far_value = float(np.mean(far))
                total = float(np.mean(base))
                reconstructed = near_value + sum(pieces.values()) + far_value
                replicate_records.append(
                    {
                        "replicate": replicate,
                        "seed": arguments.seed_base + replicate,
                        "radiusPower": radius_power,
                        "radius": 2**radius_power,
                        "points": 2**arguments.power,
                        "total": total,
                        "nearRemainder": near_value,
                        "farRemainder": far_value,
                        "reconstructed": reconstructed,
                        "sampleReconstructionResidual": reconstructed - total,
                        **{f"k{relative}": pieces[relative] for relative in relative_indices},
                    }
                )
            write_progress(
                progress,
                started,
                "replicate-complete",
                replicate=replicate + 1,
                replicates=arguments.replicates,
            )

        summary_records: list[dict[str, object]] = []
        annular_records: list[dict[str, object]] = []
        for radius_power in arguments.radius_powers:
            records = [
                record
                for record in replicate_records
                if record["radiusPower"] == radius_power
            ]
            total_mean, total_se = mean_and_se([float(record["total"]) for record in records])
            near_mean, near_se = mean_and_se(
                [float(record["nearRemainder"]) for record in records]
            )
            far_mean, far_se = mean_and_se(
                [float(record["farRemainder"]) for record in records]
            )
            piece_means: dict[int, float] = {}
            for relative in relative_indices:
                mean, se = mean_and_se(
                    [float(record[f"k{relative}"]) for record in records]
                )
                piece_means[relative] = mean
                annular_records.append(
                    {
                        "radiusPower": radius_power,
                        "radius": 2**radius_power,
                        "relativeIndex": relative,
                        "annulusIndex": radius_power + relative,
                        "mean": mean,
                        "scrambleSe": se,
                        "ci95Lower": mean - 1.96 * se,
                        "ci95Upper": mean + 1.96 * se,
                    }
                )
            denominator = abs(near_mean) + abs(far_mean) + sum(
                abs(value) for value in piece_means.values()
            )
            ratio = abs(near_mean + far_mean + sum(piece_means.values())) / denominator
            nonprincipal = near_mean + far_mean + sum(
                value
                for relative, value in piece_means.items()
                if relative not in (-1, 0)
            )
            summary_records.append(
                {
                    "radiusPower": radius_power,
                    "radius": 2**radius_power,
                    "totalMean": total_mean,
                    "totalScrambleSe": total_se,
                    "exactCoreProduction": EXACT_CORE_PRODUCTION,
                    "absoluteError": total_mean - EXACT_CORE_PRODUCTION,
                    "relativeError": (total_mean - EXACT_CORE_PRODUCTION)
                    / EXACT_CORE_PRODUCTION,
                    "coreCancellationRatio": ratio,
                    "innerAnnulusMean": piece_means[-1],
                    "outerAnnulusMean": piece_means[0],
                    "nonprincipalSignedMean": nonprincipal,
                    "nearMean": near_mean,
                    "nearScrambleSe": near_se,
                    "farMean": far_mean,
                    "farScrambleSe": far_se,
                }
            )
            write_progress(
                progress,
                started,
                "radius-summary",
                radius=2**radius_power,
                totalMean=total_mean,
                coreCancellationRatio=ratio,
                innerAnnulus=piece_means[-1],
                outerAnnulus=piece_means[0],
                nonprincipalSignedMean=nonprincipal,
            )

        profile = {
            "mollifierRadius": MOLLIFIER_RADIUS,
            "quadratureOrder": QUADRATURE_ORDER,
            "activeRadialInterval": [ACTIVE_LOW, ACTIVE_HIGH],
            "transitionEnergy": energy,
            "transitionEnergyQuadratureError": energy_error,
            "rigorousEnergyUpperBound": 50.0 / 21.0,
            "limitingInnerCarrier": limiting_inner,
            "limitingOuterCarrier": limiting_outer,
            "limitingCoreRatio": 1.0,
            "exactCoreProduction": EXACT_CORE_PRODUCTION,
        }

        def write_csv(path: Path, records: list[dict[str, object]]) -> None:
            with path.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=list(records[0].keys()))
                writer.writeheader()
                writer.writerows(records)

        write_csv(output_root / "replicates.csv", replicate_records)
        write_csv(output_root / "summary.csv", summary_records)
        write_csv(output_root / "annular.csv", annular_records)
        (output_root / "profile.json").write_text(
            json.dumps(profile, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

        result = {
            "schemaVersion": "1.0",
            "release": "R0.69U",
            "status": "passed",
            "method": {
                "sampler": "independently scrambled Sobol",
                "dimension": 5,
                "replicates": arguments.replicates,
                "pointsPerReplicate": 2**arguments.power,
                "pairsPerRadius": arguments.replicates * 2**arguments.power,
                "radiusPowers": list(arguments.radius_powers),
                "relativeAnnuli": [arguments.relative_min, arguments.relative_max],
                "seedBase": arguments.seed_base,
            },
            "profile": profile,
            "summaries": summary_records,
            "audits": {
                "partitionResidualMax": partition_residual_max,
                "sampleReconstructionResidualMax": max(
                    abs(float(record["sampleReconstructionResidual"]))
                    for record in replicate_records
                ),
                "energyBelowRigorousBound": energy < 50.0 / 21.0,
                "limitingOuterPositive": limiting_outer > 0.0,
            },
            "provenance": {
                "script": str(source_path.relative_to(source_path.parents[1])),
                "scriptSha256": sha256(source_path),
                "python": sys.version,
                "platform": platform.platform(),
                "numpy": np.__version__,
                "scipy": scipy.__version__,
            },
            "claimBoundary": (
                "exploratory finite-radius randomized quadrature; the analytic "
                "R0.69U theorem and rational sign margin do not depend on it"
            ),
        }
        (output_root / "result.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        write_progress(
            progress,
            started,
            "finished",
            status="passed",
            partitionResidualMax=partition_residual_max,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
