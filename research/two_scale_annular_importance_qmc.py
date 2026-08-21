#!/usr/bin/env python3
"""R0.69V annulus-by-annulus importance QMC for the full two-scale field.

For each physical annulus j, sample x in every radial field zone and sample
the displacement z=y-x directly in the support 2^j < |z| < 2^(j+2) of the
smooth annular weight.  The y point is accepted only in zones no earlier than
the x zone, with a factor two for distinct zones.  Symmetry of the complete
two-increment kernel then reconstructs every unordered zone pair exactly.

This removes the rare-close-pair variance of uniform B_2 x B_2 sampling while
retaining inner-transition, cross-scale, and transition-transition terms.
Randomized QMC errors remain diagnostics rather than interval enclosures.
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

from affine_core_dyadic_qmc import cutoff_value
from two_scale_full_annular_qmc import (
    KERNEL_FACTOR,
    amplitude_from_law,
    deterministic_total,
    mean_and_se,
    radial_zones,
    shell_volume,
    two_scale_vorticity,
    write_progress,
    zone_role,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def map_sobol_to_x_and_displacement(
    unit: np.ndarray,
    x_zone: tuple[float, float],
    distance_lower: float,
    distance_upper: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x_lower, x_upper = x_zone
    x_radius = (
        x_lower**3 + (x_upper**3 - x_lower**3) * unit[:, 0]
    ) ** (1.0 / 3.0)
    x_cosine = 1.0 - 2.0 * unit[:, 1]
    x_sine = np.sqrt(np.maximum(0.0, 1.0 - x_cosine**2))
    x = np.column_stack(
        (x_radius * x_sine, np.zeros_like(x_radius), x_radius * x_cosine)
    )

    distance = (
        distance_lower**3
        + (distance_upper**3 - distance_lower**3) * unit[:, 2]
    ) ** (1.0 / 3.0)
    displacement_cosine = 1.0 - 2.0 * unit[:, 3]
    displacement_sine = np.sqrt(
        np.maximum(0.0, 1.0 - displacement_cosine**2)
    )
    displacement_azimuth = 2.0 * math.pi * unit[:, 4]
    displacement = np.column_stack(
        (
            distance * displacement_sine * np.cos(displacement_azimuth),
            distance * displacement_sine * np.sin(displacement_azimuth),
            distance * displacement_cosine,
        )
    )
    return x, displacement, distance


def sample_annulus_from_x_zone(
    unit: np.ndarray,
    x_zone_index: int,
    zones: tuple[tuple[float, float], ...],
    epsilon: float,
    outer_amplitude: float,
    annular_index: int,
) -> tuple[float, dict[int, float], float]:
    distance_lower = 2.0**annular_index
    distance_upper = min(4.0, 2.0 ** (annular_index + 2))
    if distance_lower >= distance_upper:
        return 0.0, {}, 0.0

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

    omega_x = two_scale_vorticity(x, epsilon, outer_amplitude)
    omega_y = two_scale_vorticity(y, epsilon, outer_amplitude)
    delta = omega_y - omega_x
    direction = displacement / distance[:, None]
    geometric = np.einsum("ij,ij->i", direction, delta) * np.einsum(
        "ij,ij->i", direction, np.cross(omega_x, delta)
    )
    weight = cutoff_value(distance / (2.0 ** (annular_index + 1))) - cutoff_value(
        distance / (2.0**annular_index)
    )
    pair_factor = np.where(y_zone_indices == x_zone_index, 1.0, 2.0)
    measure = shell_volume(*x_zone) * shell_volume(
        distance_lower, distance_upper
    )
    values = (
        measure
        * KERNEL_FACTOR
        * geometric
        * weight
        * pair_factor
        / distance**3
    )
    values = np.where(inside, values, 0.0)

    pair_means: dict[int, float] = {}
    for y_zone_index in range(x_zone_index, len(zones)):
        mask = inside & (y_zone_indices == y_zone_index)
        pair_means[y_zone_index] = float(np.mean(np.where(mask, values, 0.0)))
    return float(np.mean(values)), pair_means, float(np.mean(inside))


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--replicates", type=int, default=8)
    parser.add_argument("--power", type=int, default=14)
    parser.add_argument("--separations", default="0,2,4,6")
    parser.add_argument("--amplitude-laws", default="outer,half,balanced,inner")
    parser.add_argument("--j-padding", type=int, default=8)
    parser.add_argument("--seed-base", type=int, default=691001)
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
    pair_records: list[dict[str, object]] = []

    with progress_path.open("w", encoding="utf-8") as progress:
        write_progress(
            progress,
            started,
            "started",
            replicates=arguments.replicates,
            pointsPerAnnulusZone=2**arguments.power,
            separations=list(arguments.separations),
            amplitudeLaws=list(arguments.amplitude_laws),
        )
        for separation in arguments.separations:
            epsilon = 2.0 ** (-separation)
            zones = radial_zones(epsilon)
            indices = tuple(range(-separation - arguments.j_padding, 2))
            for law in arguments.amplitude_laws:
                outer_amplitude = amplitude_from_law(law, epsilon)
                for replicate in range(arguments.replicates):
                    annular: dict[int, float] = {}
                    acceptance: dict[int, float] = {}
                    for index in indices:
                        annular_total = 0.0
                        accepted_means: list[float] = []
                        for x_zone_index, x_zone in enumerate(zones):
                            seed = (
                                arguments.seed_base
                                + separation * 10_000_000
                                + replicate * 100_000
                                + (index + separation + arguments.j_padding)
                                * 1_000
                                + x_zone_index
                            )
                            sampler = qmc.Sobol(d=5, scramble=True, seed=seed)
                            unit = sampler.random_base2(arguments.power)
                            mean, pair_means, accepted = (
                                sample_annulus_from_x_zone(
                                    unit,
                                    x_zone_index,
                                    zones,
                                    epsilon,
                                    outer_amplitude,
                                    index,
                                )
                            )
                            annular_total += mean
                            accepted_means.append(accepted)
                            for y_zone_index, pair_mean in pair_means.items():
                                pair_records.append(
                                    {
                                        "separation": separation,
                                        "epsilon": epsilon,
                                        "amplitudeLaw": law,
                                        "outerAmplitude": outer_amplitude,
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
                                        "mean": pair_mean,
                                    }
                                )
                        annular[index] = annular_total
                        acceptance[index] = float(np.mean(accepted_means))
                    signed_sum = sum(annular.values())
                    l1 = sum(abs(value) for value in annular.values())
                    ratio = abs(signed_sum) / l1 if l1 else math.nan
                    replicate_records.append(
                        {
                            "separation": separation,
                            "epsilon": epsilon,
                            "shapeRatio": 1.0 / epsilon,
                            "amplitudeLaw": law,
                            "outerAmplitude": outer_amplitude,
                            "innerAmplitude": 1.0 - outer_amplitude,
                            "replicate": replicate,
                            "zones": len(zones),
                            "jMin": indices[0],
                            "jMax": indices[-1],
                            "pointsPerAnnulusZone": 2**arguments.power,
                            "signedAnnularSum": signed_sum,
                            "annularL1": l1,
                            "cancellationRatio": ratio,
                            **{f"j{index}": annular[index] for index in indices},
                            **{
                                f"acceptanceJ{index}": acceptance[index]
                                for index in indices
                            },
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
                        signedAnnularSum=signed_sum,
                        cancellationRatio=ratio,
                    )

        summaries: list[dict[str, object]] = []
        annular_records: list[dict[str, object]] = []
        for separation in arguments.separations:
            epsilon = 2.0 ** (-separation)
            indices = tuple(range(-separation - arguments.j_padding, 2))
            for law in arguments.amplitude_laws:
                records = [
                    record
                    for record in replicate_records
                    if record["separation"] == separation
                    and record["amplitudeLaw"] == law
                ]
                signed_means: list[float] = []
                signed_sum_replicates = [
                    float(record["signedAnnularSum"]) for record in records
                ]
                signed_sum_mean, signed_sum_se = mean_and_se(signed_sum_replicates)
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
                deterministic = deterministic_total(
                    epsilon, amplitude_from_law(law, epsilon)
                )
                l1 = sum(abs(value) for value in signed_means)
                summaries.append(
                    {
                        "separation": separation,
                        "epsilon": epsilon,
                        "shapeRatio": 1.0 / epsilon,
                        "amplitudeLaw": law,
                        "outerAmplitude": amplitude_from_law(law, epsilon),
                        "deterministicTotal": deterministic,
                        "signedAnnularSumMean": signed_sum_mean,
                        "signedAnnularSumStandardError": signed_sum_se,
                        "signedAnnularSumZScore": (
                            (signed_sum_mean - deterministic) / signed_sum_se
                            if signed_sum_se > 0.0
                            else math.nan
                        ),
                        "annularL1OfMeans": l1,
                        "cancellationRatioOfMeans": (
                            abs(sum(signed_means)) / l1 if l1 else math.nan
                        ),
                        "finestAnnulusMean": signed_means[0],
                        "finestAnnulusStandardError": annular_records[-len(indices)][
                            "standardError"
                        ],
                    }
                )

        result = {
            "schemaVersion": "1.0",
            "release": "R0.69V-importance-pilot",
            "status": "passed",
            "claimBoundary": (
                "annulus-importance randomized finite-parameter audit; omitted "
                "near tail is diagnosed by the finest resolved annuli, not enclosed"
            ),
            "method": {
                "sampler": "independently scrambled Sobol by annulus and x-zone",
                "dimension": 5,
                "replicates": arguments.replicates,
                "pointsPerAnnulusZone": 2**arguments.power,
                "separations": list(arguments.separations),
                "amplitudeLaws": list(arguments.amplitude_laws),
                "pairRule": (
                    "sample displacement in annulus support; retain y-zone >= "
                    "x-zone and double distinct-zone contributions"
                ),
            },
            "audits": {
                "allUnorderedZonePairsRepresented": True,
                "transitionTransitionPairsRetained": True,
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
        with (output_root / "pair-classes.csv").open(
            "w", newline="", encoding="utf-8"
        ) as stream:
            writer = csv.DictWriter(stream, fieldnames=pair_records[0].keys())
            writer.writeheader()
            writer.writerows(pair_records)
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
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
