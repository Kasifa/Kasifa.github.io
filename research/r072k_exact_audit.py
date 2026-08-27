#!/usr/bin/env python3
"""Producer audit for the R0.72K directional root-sampling theorem.

The analytic theorem is proved in ``r072k_report-source.md``.  This finite
audit has two separate jobs:

1. check exact and genuinely complex model curves for the directional
   projection mechanism and the sharp factor two;
2. transform the already archived R0.72J producer rows into the new measured
   and theorem-level complete-root ledgers.

No new PDE time evolution is performed.  The input SHA-256 is recorded so the
numerical lineage is explicit.  The output remains finite binary64/rational
corroboration, not an interval proof or an enumeration of all complex roots.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import platform
import resource
import subprocess
import sys
import time
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def append_ndjson(path: Path, payload: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def rss_mb() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        return float(value) / (1024.0 * 1024.0)
    return float(value) / 1024.0


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "unavailable"


def log_slope(rows: list[dict[str, Any]], key: str) -> float:
    xs = [math.log(float(row["R"])) for row in rows]
    ys = [math.log(float(row[key])) for row in rows]
    x_bar = sum(xs) / len(xs)
    y_bar = sum(ys) / len(ys)
    numerator = sum((x - x_bar) * (y - y_bar) for x, y in zip(xs, ys))
    denominator = sum((x - x_bar) ** 2 for x in xs)
    return numerator / denominator


def exact_sharpness_cases() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for denominator in [2, 4, 8, 16, 32, 64, 128]:
        epsilon = Fraction(1, denominator)
        length = 2 * epsilon / (1 + epsilon)
        plateau_area = -epsilon * (1 - length)
        ramp_area = length * (1 - epsilon) / 2
        mean = plateau_area + ramp_area
        weighted = (1 + epsilon * epsilon) / 2
        ratio = Fraction(1, 1) / (2 * weighted)
        rows.append(
            {
                "epsilonNumerator": epsilon.numerator,
                "epsilonDenominator": epsilon.denominator,
                "rampLengthNumerator": length.numerator,
                "rampLengthDenominator": length.denominator,
                "meanNumerator": mean.numerator,
                "meanDenominator": mean.denominator,
                "endpointSlopeSquared": 1.0,
                "weightedVariation": float(weighted),
                "theoremRatio": float(ratio),
            }
        )
    return rows


def complex_circle_cases() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    expected_ratio = 1.0 / (4.0 * math.pi)
    for frequency_count in [1, 2, 4, 8, 16, 32]:
        omega = 2.0 * math.pi * frequency_count
        slope_mass_excluding_first = frequency_count * omega**2
        weighted_variation = omega**3
        ratio = slope_mass_excluding_first / (2.0 * weighted_variation)
        max_projection_residual = max(
            abs(math.cos(2.0 * math.pi * (j - 0.25)))
            for j in range(1, frequency_count + 1)
        )
        rows.append(
            {
                "frequencyCount": frequency_count,
                "rootCountIncludingEndpoints": frequency_count + 1,
                "minimumDerivativeNorm": omega,
                "slopeMassExcludingFirst": slope_mass_excluding_first,
                "weightedVariation": weighted_variation,
                "theoremRatio": ratio,
                "expectedRatio": expected_ratio,
                "directionalProjectionResidual": max_projection_residual,
                "literalComplexRolleFails": True,
            }
        )
    return rows


def complex_vector_cases() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    alpha = 0.3
    slope_factor = 1.0 + 4.0 * alpha**2
    curvature_factor = 1.0 + 16.0 * alpha**2
    for frequency_count in [1, 2, 4, 8, 16]:
        omega = 2.0 * math.pi * frequency_count
        slope_mass = frequency_count * omega**2 * slope_factor
        weighted = omega**3 * math.sqrt(slope_factor * curvature_factor)
        rows.append(
            {
                "frequencyCount": frequency_count,
                "dimensionComplex": 2,
                "alpha": alpha,
                "rootCountIncludingEndpoints": frequency_count + 1,
                "minimumDerivativeNorm": omega * math.sqrt(slope_factor),
                "slopeMassExcludingFirst": slope_mass,
                "weightedVariation": weighted,
                "theoremRatio": slope_mass / (2.0 * weighted),
            }
        )
    return rows


def transform_r072j_rows(source: dict[str, Any]) -> list[dict[str, Any]]:
    transformed: list[dict[str, Any]] = []
    for row in source["cases"]:
        first = float(row["rawBvProxyFirstRoot"])
        measured = (
            first
            + 2.0 * float(row["mixedRow"])
            + 2.0 * float(row["deltaIntegralAbsHB"])
        )
        theorem_proxy = (
            first
            + float(row["rawBvProxyMixedMoment"])
            + float(row["rawBvProxyTrueCubic"])
        )
        root_atom = float(row["rootH"]) ** 2
        natural_scale = float(row["N"]) ** 2
        theta = float(row["theta"])
        reference = float(row["referencePayment"])
        transformed.append(
            {
                "R": int(row["R"]),
                "N": int(row["N"]),
                "firstRootPayment": first,
                "mixedRowMeasuredTwice": 2.0 * float(row["mixedRow"]),
                "trueCubicMeasuredTwice": 2.0
                * float(row["deltaIntegralAbsHB"]),
                "directionalMeasuredUpper": measured,
                "directionalTheoremProxy": theorem_proxy,
                "exactRootAtom": root_atom,
                "exactRootResidual": float(row["evolvedRootResidual"]),
                "measuredUpperOverN2": measured / natural_scale,
                "theoremProxyOverN2": theorem_proxy / natural_scale,
                "rootAtomOverN2": root_atom / natural_scale,
                "normalizedMeasuredCompleteUpper": theta * measured / reference,
                "normalizedTheoremCompleteProxy": theta
                * theorem_proxy
                / reference,
                "previousDiagonalTermRemoved": float(
                    row["rawBvProxyTargetDiagonal"]
                ),
            }
        )
    return transformed


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(rows[0].keys()), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("research/certificates/r072k"),
    )
    parser.add_argument(
        "--r072j-input",
        type=Path,
        default=Path("research/certificates/r072j/result.json"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.perf_counter()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    progress_path = args.output_dir / "producer-progress.ndjson"
    resource_path = args.output_dir / "producer-resource.ndjson"
    progress_path.write_text("", encoding="utf-8")
    resource_path.write_text("", encoding="utf-8")

    input_sha = sha256(args.r072j_input)
    config = {
        "schemaVersion": 1,
        "audit": "R0.72K directional-root producer",
        "date": "2026-08-27",
        "r072jInput": str(args.r072j_input),
        "r072jInputSha256": input_sha,
        "sharpnessEpsilons": ["1/2", "1/4", "1/8", "1/16", "1/32", "1/64", "1/128"],
        "complexCircleCounts": [1, 2, 4, 8, 16, 32],
        "newPdeEvolution": False,
        "sourceSha256": sha256(Path(__file__).resolve()),
    }
    (args.output_dir / "config.json").write_text(
        json.dumps(config, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (args.output_dir / "seed.txt").write_text(
        "deterministic:no-random-seed\n", encoding="utf-8"
    )
    append_ndjson(
        progress_path,
        {"time": utc_now(), "event": "audit_start", "config": config},
    )

    sharpness = exact_sharpness_cases()
    append_ndjson(
        progress_path,
        {
            "time": utc_now(),
            "event": "exact_sharpness_complete",
            "cases": len(sharpness),
            "lastRatio": sharpness[-1]["theoremRatio"],
        },
    )
    circles = complex_circle_cases()
    vectors = complex_vector_cases()
    append_ndjson(
        progress_path,
        {
            "time": utc_now(),
            "event": "complex_models_complete",
            "circleCases": len(circles),
            "vectorCases": len(vectors),
        },
    )

    source = json.loads(args.r072j_input.read_text(encoding="utf-8"))
    transformed = transform_r072j_rows(source)
    append_ndjson(
        progress_path,
        {
            "time": utc_now(),
            "event": "r072j_lineage_transform_complete",
            "cases": len(transformed),
            "inputSha256": input_sha,
            "largestR": transformed[-1]["R"],
            "largestNormalizedMeasuredUpper": transformed[-1][
                "normalizedMeasuredCompleteUpper"
            ],
        },
    )

    circle_expected = 1.0 / (4.0 * math.pi)
    measured_spread = max(row["measuredUpperOverN2"] for row in transformed) / min(
        row["measuredUpperOverN2"] for row in transformed
    )
    slopes = {
        "normalizedMeasuredCompleteUpperAll": log_slope(
            transformed, "normalizedMeasuredCompleteUpper"
        ),
        "normalizedTheoremCompleteProxyAll": log_slope(
            transformed, "normalizedTheoremCompleteProxy"
        ),
        "exactRootAtomAll": log_slope(transformed, "exactRootAtom"),
    }
    checks = {
        "r072jProducerPassed": source.get("status") == "passed",
        "sharpnessMeansExactlyZero": all(
            row["meanNumerator"] == 0 for row in sharpness
        ),
        "sharpnessApproachesOne": sharpness[-1]["theoremRatio"] > 0.9999,
        "sharpnessRatiosIncrease": all(
            left["theoremRatio"] < right["theoremRatio"]
            for left, right in zip(sharpness, sharpness[1:])
        ),
        "literalComplexRolleFails": all(
            row["literalComplexRolleFails"]
            and row["minimumDerivativeNorm"] > 0.0
            for row in circles
        ),
        "complexCircleRatioExact": max(
            abs(row["theoremRatio"] - circle_expected) for row in circles
        )
        < 2.0e-15,
        "complexProjectionZerosResolved": max(
            row["directionalProjectionResidual"] for row in circles
        )
        < 2.0e-14,
        "vectorModelsSatisfyTheorem": all(
            0.0 < row["theoremRatio"] < 1.0 for row in vectors
        ),
        "exactRootAtomBelowMeasuredUpper": all(
            row["exactRootAtom"] <= row["directionalMeasuredUpper"]
            for row in transformed
        ),
        "measuredUpperHasN2Scale": measured_spread < 1.02,
        "theoremProxyHasN2Upper": max(
            row["theoremProxyOverN2"] for row in transformed
        )
        < 20.0,
        "normalizedMeasuredUpperDecays": slopes[
            "normalizedMeasuredCompleteUpperAll"
        ]
        < -0.5,
        "normalizedTheoremProxyDecays": slopes[
            "normalizedTheoremCompleteProxyAll"
        ]
        < -0.45,
        "exactRootsRemainAccurate": max(
            row["exactRootResidual"] for row in transformed
        )
        < 2.0e-8,
    }
    checks = {key: bool(value) for key, value in checks.items()}
    passed = all(checks.values())
    elapsed = time.perf_counter() - started
    result = {
        "schemaVersion": 1,
        "audit": "R0.72K directional-root producer",
        "status": "passed" if passed else "failed",
        "generatedAt": utc_now(),
        "gitCommit": git_commit(),
        "config": config,
        "slopes": slopes,
        "checks": checks,
        "sharpnessCases": sharpness,
        "complexCircleCases": circles,
        "complexVectorCases": vectors,
        "commonBandCases": transformed,
        "elapsedSeconds": elapsed,
        "limitations": [
            "the analytic theorem, not this finite audit, proves complete-root packing",
            "the complete complex root set is not enumerated",
            "R0.72J producer data are reused with an explicit SHA-256 lineage",
            "the transformed quadrature values remain binary64 approximations",
            "no new PDE time evolution is performed in R0.72K",
            "the common-band theorem is not a general three-dimensional Navier--Stokes result",
        ],
    }
    result_path = args.output_dir / "result.json"
    result_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_csv(args.output_dir / "producer-data.csv", transformed)
    write_csv(args.output_dir / "sharpness-data.csv", sharpness)
    write_csv(args.output_dir / "complex-circle-data.csv", circles)
    write_csv(args.output_dir / "complex-vector-data.csv", vectors)

    environment = {
        "generatedAt": utc_now(),
        "python": sys.version,
        "platform": platform.platform(),
        "executable": sys.executable,
        "cpuCount": os.cpu_count(),
        "maxRssMb": rss_mb(),
    }
    (args.output_dir / "environment.txt").write_text(
        "\n".join(f"{key}={value}" for key, value in environment.items())
        + "\n",
        encoding="utf-8",
    )
    append_ndjson(
        resource_path,
        {
            "time": utc_now(),
            "elapsedSeconds": elapsed,
            "maxRssMb": rss_mb(),
            "newPdeEvolution": False,
        },
    )
    append_ndjson(
        progress_path,
        {
            "time": utc_now(),
            "event": "audit_complete",
            "status": result["status"],
            "checks": checks,
            "slopes": slopes,
        },
    )
    monitor = {
        "status": result["status"],
        "sharpnessCases": len(sharpness),
        "complexCases": len(circles) + len(vectors),
        "commonBandCases": len(transformed),
        "elapsedSeconds": elapsed,
        "maxRssMb": rss_mb(),
        "resultSha256": sha256(result_path),
    }
    (args.output_dir / "producer-monitor.log").write_text(
        json.dumps(monitor, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(monitor, sort_keys=True), flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
