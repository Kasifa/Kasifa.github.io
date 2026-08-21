#!/usr/bin/env python3
"""R0.69V stratified QMC audit of a shape-changing two-scale affine family.

Let u_R be the compact affine field from R0.69U.  After normalizing the outer
radius to one, this script studies

    u_{epsilon,a} = a u_1 + (1-a) u_epsilon,
    epsilon = 2^{-N}.

The affine gradient in the innermost core is fixed because the two amplitudes
sum to one.  The scale ratio 1/epsilon changes with N, so this family is not a
single self-similar dilation orbit.

The complete symmetric two-increment annular integral is evaluated.  Radial
dyadic zones are sampled separately and every unordered zone pair is retained,
including transition--transition pairs.  Randomized QMC errors are diagnostics,
not interval enclosures or a regularity proof.
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

from affine_core_dyadic_qmc import (
    compact_vorticity,
    cutoff_value,
    cutoff_value_derivatives,
)


KERNEL_FACTOR = 3.0 / (8.0 * math.pi)
EVALUATION_CHUNK = 65_536
SQRT6 = math.sqrt(6.0)
A_MATRIX = np.asarray(
    [
        [-1.0 / SQRT6, -0.5, 0.0],
        [0.5, -1.0 / SQRT6, 0.0],
        [0.0, 0.0, 2.0 / SQRT6],
    ],
    dtype=np.float64,
)
S_MATRIX = 0.5 * (A_MATRIX + A_MATRIX.T)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def shell_volume(lower: float, upper: float) -> float:
    return 4.0 * math.pi / 3.0 * (upper**3 - lower**3)


def radial_zones(epsilon: float) -> tuple[tuple[float, float], ...]:
    """Split both transition shells and every intervening dyadic plateau."""

    boundaries = [0.0, epsilon]
    value = epsilon
    while value < 2.0:
        value = min(2.0, 2.0 * value)
        boundaries.append(value)
    return tuple(zip(boundaries[:-1], boundaries[1:], strict=True))


def zone_role(zone: tuple[float, float], epsilon: float) -> str:
    lower, upper = zone
    tolerance = 32.0 * np.finfo(np.float64).eps
    if upper <= epsilon + tolerance:
        return "inner-core"
    if lower >= epsilon - tolerance and upper <= 2.0 * epsilon + tolerance:
        return "inner-transition"
    if lower >= 1.0 - tolerance:
        return "outer-transition"
    return "intermediate-plateau"


def map_sobol_to_zone_pair(
    unit: np.ndarray,
    x_zone: tuple[float, float],
    y_zone: tuple[float, float],
) -> tuple[np.ndarray, np.ndarray]:
    """Map five uniforms to two radial zones, removing one common azimuth."""

    x_lower, x_upper = x_zone
    y_lower, y_upper = y_zone
    x_radius = (
        x_lower**3 + (x_upper**3 - x_lower**3) * unit[:, 0]
    ) ** (1.0 / 3.0)
    x_cosine = 1.0 - 2.0 * unit[:, 1]
    x_sine = np.sqrt(np.maximum(0.0, 1.0 - x_cosine**2))
    x = np.column_stack(
        (x_radius * x_sine, np.zeros_like(x_radius), x_radius * x_cosine)
    )

    y_radius = (
        y_lower**3 + (y_upper**3 - y_lower**3) * unit[:, 2]
    ) ** (1.0 / 3.0)
    y_cosine = 1.0 - 2.0 * unit[:, 3]
    y_sine = np.sqrt(np.maximum(0.0, 1.0 - y_cosine**2))
    relative_azimuth = 2.0 * math.pi * unit[:, 4]
    y = np.column_stack(
        (
            y_radius * y_sine * np.cos(relative_azimuth),
            y_radius * y_sine * np.sin(relative_azimuth),
            y_radius * y_cosine,
        )
    )
    return x, y


def two_scale_vorticity(
    points: np.ndarray,
    epsilon: float,
    outer_amplitude: float,
) -> np.ndarray:
    inner_amplitude = 1.0 - outer_amplitude
    outer = compact_vorticity(points, 1.0)
    if inner_amplitude == 0.0:
        return outer
    inner = compact_vorticity(points, epsilon)
    return outer_amplitude * outer + inner_amplitude * inner


def compact_velocity_gradient(points: np.ndarray, radius_scale: float) -> np.ndarray:
    """Analytic gradient of curl(q(|x|/R) B_A)."""

    radius = np.linalg.norm(points, axis=1)
    safe_radius = np.where(radius > 0.0, radius, 1.0)
    scaled = radius / radius_scale
    value, scaled_first, scaled_second = cutoff_value_derivatives(scaled)
    first = scaled_first / radius_scale
    second = scaled_second / radius_scale**2

    affine = points @ A_MATRIX.T
    strain_image = points @ S_MATRIX.T
    quadratic = np.einsum("ij,ij->i", points, strain_image)
    direction = points / safe_radius[:, None]
    coefficient = value + radius * first / 3.0
    coefficient_first = 4.0 * first / 3.0 + radius * second / 3.0
    radial = first / (3.0 * safe_radius)
    radial_first = (
        second / (3.0 * safe_radius)
        - first / (3.0 * safe_radius**2)
    )

    gradient = coefficient[:, None, None] * A_MATRIX[None, :, :]
    gradient += (
        coefficient_first[:, None, None]
        * affine[:, :, None]
        * direction[:, None, :]
    )
    gradient -= (
        radial_first[:, None, None]
        * points[:, :, None]
        * direction[:, None, :]
        * quadratic[:, None, None]
    )
    gradient -= (
        radial[:, None, None]
        * np.eye(3, dtype=np.float64)[None, :, :]
        * quadratic[:, None, None]
    )
    gradient -= (
        2.0
        * radial[:, None, None]
        * points[:, :, None]
        * strain_image[:, None, :]
    )
    return gradient


def deterministic_total(
    epsilon: float,
    outer_amplitude: float,
    radial_order: int = 96,
    polar_order: int = 16,
) -> float:
    """Axisymmetric Gauss audit of integral omega dot S omega."""

    radial_nodes, radial_weights = np.polynomial.legendre.leggauss(radial_order)
    polar_nodes, polar_weights = np.polynomial.legendre.leggauss(polar_order)
    inner_amplitude = 1.0 - outer_amplitude
    total = 0.0
    for lower, upper in radial_zones(epsilon):
        radii = 0.5 * (upper - lower) * radial_nodes + 0.5 * (upper + lower)
        weights = 0.5 * (upper - lower) * radial_weights
        radius_grid, cosine_grid = np.meshgrid(
            radii, polar_nodes, indexing="ij"
        )
        cylindrical_radius = radius_grid * np.sqrt(
            np.maximum(0.0, 1.0 - cosine_grid**2)
        )
        points = np.column_stack(
            (
                cylindrical_radius.reshape(-1),
                np.zeros(radius_grid.size),
                (radius_grid * cosine_grid).reshape(-1),
            )
        )
        omega = two_scale_vorticity(points, epsilon, outer_amplitude)
        gradient = (
            outer_amplitude * compact_velocity_gradient(points, 1.0)
            + inner_amplitude * compact_velocity_gradient(points, epsilon)
        )
        strain = 0.5 * (gradient + np.swapaxes(gradient, 1, 2))
        density = np.einsum("ni,nij,nj->n", omega, strain, omega).reshape(
            radius_grid.shape
        )
        total += 2.0 * math.pi * float(
            np.sum(
                density
                * radius_grid**2
                * weights[:, None]
                * polar_weights[None, :]
            )
        )
    return total


def deterministic_building_coefficients(
    radial_order: int = 128,
    polar_order: int = 16,
) -> tuple[float, float, float]:
    """Return V_q and the a^2 b, a b^2 local cross coefficients."""

    radial_nodes, radial_weights = np.polynomial.legendre.leggauss(radial_order)
    polar_nodes, polar_weights = np.polynomial.legendre.leggauss(polar_order)
    vertical = np.asarray([0.0, 0.0, 1.0], dtype=np.float64)
    coefficients = np.zeros(3, dtype=np.float64)
    for lower, upper in radial_zones(1.0):
        radii = 0.5 * (upper - lower) * radial_nodes + 0.5 * (upper + lower)
        weights = 0.5 * (upper - lower) * radial_weights
        radius_grid, cosine_grid = np.meshgrid(
            radii, polar_nodes, indexing="ij"
        )
        cylindrical_radius = radius_grid * np.sqrt(
            np.maximum(0.0, 1.0 - cosine_grid**2)
        )
        points = np.column_stack(
            (
                cylindrical_radius.reshape(-1),
                np.zeros(radius_grid.size),
                (radius_grid * cosine_grid).reshape(-1),
            )
        )
        omega = compact_vorticity(points, 1.0)
        gradient = compact_velocity_gradient(points, 1.0)
        strain = 0.5 * (gradient + np.swapaxes(gradient, 1, 2))
        affine_on_vertical = S_MATRIX @ vertical
        density_v = np.einsum("ni,nij,nj->n", omega, strain, omega)
        density_21 = (
            2.0 * np.einsum("ni,i->n", omega, affine_on_vertical)
            + strain[:, 2, 2]
        )
        density_12 = (
            np.einsum("ni,ij,nj->n", omega, S_MATRIX, omega)
            + 2.0 * np.einsum("nij,nj,i->n", strain, omega, vertical)
        )
        densities = np.stack((density_v, density_21, density_12), axis=0)
        measure = (
            2.0
            * math.pi
            * radius_grid**2
            * weights[:, None]
            * polar_weights[None, :]
        )
        coefficients += np.sum(
            densities.reshape(3, *radius_grid.shape) * measure[None, :, :],
            axis=(1, 2),
        )
    return tuple(float(value) for value in coefficients)


def sample_zone_pair(
    unit: np.ndarray,
    x_zone: tuple[float, float],
    y_zone: tuple[float, float],
    diagonal_zone_pair: bool,
    epsilon: float,
    outer_amplitude: float,
    j_min: int,
    j_max: int,
) -> tuple[np.ndarray, dict[int, np.ndarray], np.ndarray, np.ndarray, float]:
    """Return the complete symmetric double-increment integrand by annulus."""

    x, y = map_sobol_to_zone_pair(unit, x_zone, y_zone)
    displacement = y - x
    distance = np.linalg.norm(displacement, axis=1)
    direction = displacement / distance[:, None]
    omega_x = two_scale_vorticity(x, epsilon, outer_amplitude)
    omega_y = two_scale_vorticity(y, epsilon, outer_amplitude)
    delta = omega_y - omega_x
    geometric = np.einsum("ij,ij->i", direction, delta) * np.einsum(
        "ij,ij->i", direction, np.cross(omega_x, delta)
    )

    pair_multiplier = 1.0 if diagonal_zone_pair else 2.0
    measure = (
        pair_multiplier
        * shell_volume(*x_zone)
        * shell_volume(*y_zone)
    )
    base = measure * KERNEL_FACTOR * geometric / distance**3

    annular: dict[int, np.ndarray] = {}
    partition = np.zeros_like(distance)
    for index in range(j_min, j_max + 1):
        weight = cutoff_value(distance / (2.0 ** (index + 1))) - cutoff_value(
            distance / (2.0**index)
        )
        annular[index] = base * weight
        partition += weight
    near_weight = cutoff_value(distance / (2.0**j_min))
    far_weight = 1.0 - cutoff_value(distance / (2.0 ** (j_max + 1)))
    residual = float(np.max(np.abs(partition + near_weight + far_weight - 1.0)))
    return base, annular, base * near_weight, base * far_weight, residual


def amplitude_from_law(law: str, epsilon: float) -> float:
    if law == "outer":
        return 1.0
    if law == "inner":
        return 0.0
    if law == "half":
        return 0.5
    if law == "balanced":
        return epsilon / (1.0 + epsilon)
    if law.startswith("fixed:"):
        return float(law.split(":", 1)[1])
    raise ValueError(f"unknown amplitude law: {law}")


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
    parser.add_argument("--replicates", type=int, default=4)
    parser.add_argument("--power", type=int, default=13)
    parser.add_argument("--separations", default="0,2,4,6")
    parser.add_argument("--amplitude-laws", default="outer,half,balanced,inner")
    parser.add_argument("--j-padding", type=int, default=7)
    parser.add_argument("--seed-base", type=int, default=690901)
    parser.add_argument("--source-commit")
    arguments = parser.parse_args()
    arguments.separations = tuple(
        sorted({int(value) for value in arguments.separations.split(",")})
    )
    arguments.amplitude_laws = tuple(
        dict.fromkeys(
            value.strip()
            for value in arguments.amplitude_laws.split(",")
            if value.strip()
        )
    )
    if arguments.replicates < 2:
        parser.error("--replicates must be at least two")
    if arguments.power < 1 or arguments.j_padding < 2:
        parser.error("invalid QMC power or annular padding")
    if not arguments.separations or arguments.separations[0] < 0:
        parser.error("separations must be nonnegative")
    if not arguments.amplitude_laws:
        parser.error("at least one amplitude law is required")
    for separation in arguments.separations:
        epsilon = 2.0 ** (-separation)
        for law in arguments.amplitude_laws:
            amplitude = amplitude_from_law(law, epsilon)
            if not 0.0 <= amplitude <= 1.0:
                parser.error(f"amplitude law {law!r} leaves [0,1]")
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
    progress_path = output_root / "progress.ndjson"
    source_path = Path(__file__).resolve()
    started = time.perf_counter()
    replicate_records: list[dict[str, object]] = []
    zone_pair_records: list[dict[str, object]] = []
    partition_residual_max = 0.0
    with progress_path.open("w", encoding="utf-8") as progress:
        write_progress(
            progress,
            started,
            "started",
            replicates=arguments.replicates,
            pointsPerZonePair=2**arguments.power,
            separations=list(arguments.separations),
            amplitudeLaws=list(arguments.amplitude_laws),
        )
        for separation in arguments.separations:
            epsilon = 2.0 ** (-separation)
            zones = radial_zones(epsilon)
            j_min = -separation - arguments.j_padding
            j_max = 1
            indices = tuple(range(j_min, j_max + 1))
            zone_pairs = tuple(
                (left, right)
                for left in range(len(zones))
                for right in range(left, len(zones))
            )
            for law in arguments.amplitude_laws:
                outer_amplitude = amplitude_from_law(law, epsilon)
                for replicate in range(arguments.replicates):
                    total = 0.0
                    near = 0.0
                    far = 0.0
                    pieces = {index: 0.0 for index in indices}
                    for pair_number, (left, right) in enumerate(zone_pairs):
                        seed = (
                            arguments.seed_base
                            + separation * 1_000_000
                            + replicate * 10_000
                            + pair_number
                        )
                        sampler = qmc.Sobol(d=5, scramble=True, seed=seed)
                        unit = sampler.random_base2(arguments.power)
                        base, annular, near_values, far_values, residual = (
                            sample_zone_pair(
                                unit,
                                zones[left],
                                zones[right],
                                left == right,
                                epsilon,
                                outer_amplitude,
                                j_min,
                                j_max,
                            )
                        )
                        partition_residual_max = max(partition_residual_max, residual)
                        pair_total = float(np.mean(base))
                        pair_near = float(np.mean(near_values))
                        pair_far = float(np.mean(far_values))
                        pair_pieces = {
                            index: float(np.mean(annular[index])) for index in indices
                        }
                        total += pair_total
                        near += pair_near
                        far += pair_far
                        for index in indices:
                            pieces[index] += pair_pieces[index]
                        zone_pair_records.append(
                            {
                                "separation": separation,
                                "epsilon": epsilon,
                                "amplitudeLaw": law,
                                "outerAmplitude": outer_amplitude,
                                "replicate": replicate,
                                "leftZone": left,
                                "rightZone": right,
                                "leftLower": zones[left][0],
                                "leftUpper": zones[left][1],
                                "rightLower": zones[right][0],
                                "rightUpper": zones[right][1],
                                "leftRole": zone_role(zones[left], epsilon),
                                "rightRole": zone_role(zones[right], epsilon),
                                "pairClass": (
                                    f"{zone_role(zones[left], epsilon)}--"
                                    f"{zone_role(zones[right], epsilon)}"
                                ),
                                "total": pair_total,
                                "near": pair_near,
                                "far": pair_far,
                                **{
                                    f"j{index}": pair_pieces[index] for index in indices
                                },
                            }
                        )
                    reconstructed = near + far + sum(pieces.values())
                    signed_buckets = [near, *pieces.values(), far]
                    denominator = sum(abs(value) for value in signed_buckets)
                    ratio = abs(sum(signed_buckets)) / denominator if denominator else math.nan
                    replicate_records.append(
                        {
                            "separation": separation,
                            "epsilon": epsilon,
                            "amplitudeLaw": law,
                            "outerAmplitude": outer_amplitude,
                            "innerAmplitude": 1.0 - outer_amplitude,
                            "replicate": replicate,
                            "zones": len(zones),
                            "zonePairs": len(zone_pairs),
                            "jMin": j_min,
                            "jMax": j_max,
                            "pointsPerZonePair": 2**arguments.power,
                            "total": total,
                            "near": near,
                            "far": far,
                            "reconstructed": reconstructed,
                            "sampleReconstructionResidual": reconstructed - total,
                            "annularL1WithTailBuckets": denominator,
                            "cancellationRatioWithTailBuckets": ratio,
                            **{f"j{index}": pieces[index] for index in indices},
                        }
                    )
                    write_progress(
                        progress,
                        started,
                        "replicate-complete",
                        separation=separation,
                        amplitudeLaw=law,
                        replicate=replicate + 1,
                        replicates=arguments.replicates,
                        zones=len(zones),
                        total=total,
                        cancellationRatio=ratio,
                    )

        summaries: list[dict[str, object]] = []
        annular_records: list[dict[str, object]] = []
        for separation in arguments.separations:
            epsilon = 2.0 ** (-separation)
            j_min = -separation - arguments.j_padding
            indices = tuple(range(j_min, 2))
            for law in arguments.amplitude_laws:
                records = [
                    record
                    for record in replicate_records
                    if record["separation"] == separation
                    and record["amplitudeLaw"] == law
                ]
                total_mean, total_se = mean_and_se(
                    [float(record["total"]) for record in records]
                )
                outer_amplitude = amplitude_from_law(law, epsilon)
                deterministic_total_value = deterministic_total(
                    epsilon, outer_amplitude
                )
                near_mean, near_se = mean_and_se(
                    [float(record["near"]) for record in records]
                )
                far_mean, far_se = mean_and_se(
                    [float(record["far"]) for record in records]
                )
                signed_means = [near_mean]
                for index in indices:
                    mean, se = mean_and_se(
                        [float(record[f"j{index}"]) for record in records]
                    )
                    signed_means.append(mean)
                    annular_records.append(
                        {
                            "separation": separation,
                            "epsilon": epsilon,
                            "amplitudeLaw": law,
                            "index": index,
                            "mean": mean,
                            "standardError": se,
                        }
                    )
                signed_means.append(far_mean)
                l1 = sum(abs(value) for value in signed_means)
                reconstruction = sum(signed_means)
                summaries.append(
                    {
                        "separation": separation,
                        "epsilon": epsilon,
                        "shapeRatio": 1.0 / epsilon,
                        "amplitudeLaw": law,
                        "outerAmplitude": outer_amplitude,
                        "deterministicTotal": deterministic_total_value,
                        "totalMean": total_mean,
                        "totalStandardError": total_se,
                        "totalZScore": (
                            (total_mean - deterministic_total_value) / total_se
                            if total_se > 0.0
                            else math.nan
                        ),
                        "reconstructedMean": reconstruction,
                        "sampleMeanReconstructionResidual": reconstruction - total_mean,
                        "nearMean": near_mean,
                        "nearStandardError": near_se,
                        "farMean": far_mean,
                        "farStandardError": far_se,
                        "annularL1WithTailBuckets": l1,
                        "cancellationRatioWithTailBuckets": (
                            abs(reconstruction) / l1 if l1 else math.nan
                        ),
                    }
                )

        result = {
            "schemaVersion": "1.0",
            "release": "R0.69V-pilot",
            "status": "passed",
            "claimBoundary": (
                "stratified randomized finite-parameter audit; no interval "
                "enclosure, asymptotic theorem, or Navier-Stokes regularity claim"
            ),
            "method": {
                "sampler": "independently scrambled Sobol by zone pair",
                "dimension": 5,
                "replicates": arguments.replicates,
                "pointsPerZonePair": 2**arguments.power,
                "separations": list(arguments.separations),
                "amplitudeLaws": list(arguments.amplitude_laws),
                "zoneRule": "origin-centred dyadic radial zones in B_2",
                "pairRule": "all unordered zone pairs with off-diagonal factor two",
            },
            "audits": {
                "partitionResidualMax": partition_residual_max,
                "sampleReconstructionResidualMax": max(
                    abs(float(record["sampleReconstructionResidual"]))
                    for record in replicate_records
                ),
                "allTransitionPairsRetained": True,
                "sourceCommitMatchesHead": (
                    arguments.source_commit is None
                    or arguments.source_commit == head_commit
                ),
            },
            "summaries": summaries,
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

        output_root.mkdir(parents=True, exist_ok=True)
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
        with (output_root / "zone-pairs.csv").open(
            "w", newline="", encoding="utf-8"
        ) as stream:
            writer = csv.DictWriter(
                stream,
                fieldnames=sorted(
                    {key for record in zone_pair_records for key in record}
                ),
            )
            writer.writeheader()
            writer.writerows(zone_pair_records)
        with (output_root / "annular.csv").open(
            "w", newline="", encoding="utf-8"
        ) as stream:
            writer = csv.DictWriter(stream, fieldnames=annular_records[0].keys())
            writer.writeheader()
            writer.writerows(annular_records)
        with (output_root / "summary.csv").open(
            "w", newline="", encoding="utf-8"
        ) as stream:
            writer = csv.DictWriter(stream, fieldnames=summaries[0].keys())
            writer.writeheader()
            writer.writerows(summaries)
        (output_root / "result.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        write_progress(
            progress,
            started,
            "completed",
            scenarios=len(summaries),
            partitionResidualMax=partition_residual_max,
            sampleReconstructionResidualMax=result["audits"][
                "sampleReconstructionResidualMax"
            ],
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
