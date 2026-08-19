#!/usr/bin/env python3
"""Prepare R0.50 journal-figure tables from the pinned exact certificate."""

from __future__ import annotations

import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys
import time

import gmpy2
import mpmath


Q = gmpy2.mpq
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESEARCH = ROOT / "research"
sys.path.insert(0, str(RESEARCH))

import edge_charge_character_optimization_audit as r050  # noqa: E402
import edge_charge_threshold_root_audit as r048  # noqa: E402
import edge_rational_asymptotic_audit as r028  # noqa: E402
import edge_short_continuation_audit as r036  # noqa: E402
import edge_weighted_restart_audit as r037  # noqa: E402


CERTIFICATE = (
    RESEARCH
    / "certificates/r050/edge-charge-character-optimization.json"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "fc173a2108ef881d21d9d54046085f0d5daf5cc33ed50e024ca32ec867f7b79a"
)


def progress(started: float, stage: str, **details: object) -> None:
    suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
    print(
        f"[R0.50 figure +{time.perf_counter() - started:7.2f}s] {stage}{suffix}",
        file=sys.stderr,
        flush=True,
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def to_mpf(value: Q) -> mpmath.mpf:
    return mpmath.mpf(int(value.numerator)) / mpmath.mpf(
        int(value.denominator)
    )


def write_csv(
    path: Path,
    fieldnames: list[str],
    rows: list[dict[str, object]],
) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=fieldnames,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    started = time.perf_counter()
    if sha256(CERTIFICATE) != EXPECTED_CERTIFICATE_SHA256:
        raise SystemExit("R0.50 certificate hash mismatch")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if len(certificate["checks"]) != 33 or not all(
        certificate["checks"].values()
    ):
        raise SystemExit("R0.50 certificate checks are incomplete")

    progress(started, "reconstructing exact active Laurent polynomial")
    active_field, _, _, _ = r028.rational_edge_recurrence(80, False, started)
    polynomial = r036.field_to_polynomial(active_field, 80)
    if r037.polynomial_digest(polynomial) != certificate[
        "finiteConstruction"
    ]["degreeEightyPolynomialSha256"]:
        raise SystemExit("degree-80 polynomial hash mismatch")
    terms = r048.independent_terms(polynomial)
    laurent = r050.active_laurent_terms(terms, 81, 162)

    mpmath.mp.dps = 90
    numeric_terms = [
        (degree, charge, to_mpf(coefficient))
        for degree, charge, coefficient in laurent
    ]

    def value_and_derivative(
        radius: mpmath.mpf,
        character: mpmath.mpf,
    ) -> tuple[mpmath.mpf, mpmath.mpf]:
        values = [
            coefficient * radius**degree * character**charge
            for degree, charge, coefficient in numeric_terms
        ]
        value = mpmath.fsum(values)
        derivative = mpmath.fsum(
            degree * term / radius
            for term, (degree, _, _) in zip(
                values,
                numeric_terms,
                strict=True,
            )
        )
        return value, derivative

    def threshold_root(
        character: Q,
        initial: mpmath.mpf,
    ) -> tuple[mpmath.mpf, mpmath.mpf, int]:
        c = to_mpf(character)
        radius = mpmath.mpf(initial)
        for iteration in range(1, 31):
            value, derivative = value_and_derivative(radius, c)
            step = (value - 1) / derivative
            candidate = radius - step
            if candidate <= 0:
                candidate = radius / 2
            radius = candidate
            if abs(step) < mpmath.mpf("1e-82"):
                break
        residual = value_and_derivative(radius, c)[0] - 1
        if abs(residual) >= mpmath.mpf("1e-78"):
            raise SystemExit(f"threshold solve failed at c={character}")
        return radius, residual, iteration

    def sample_grid(
        lower: Q,
        upper: Q,
        count: int,
        grid_name: str,
    ) -> list[dict[str, object]]:
        rows: list[dict[str, object]] = []
        root = mpmath.mpf("0.3826")
        for index in range(count):
            position = Q(index, count - 1)
            character = lower + position * (upper - lower)
            root, residual, iterations = threshold_root(character, root)
            rows.append(
                {
                    "grid": grid_name,
                    "sampleIndex": index,
                    "characterExact": str(character),
                    "characterDecimal": mpmath.nstr(to_mpf(character), 24),
                    "thresholdRadiusDecimal": mpmath.nstr(root, 82),
                    "absoluteResidualDecimal": mpmath.nstr(abs(residual), 12),
                    "newtonIterations": iterations,
                    "classification": (
                        "90-digit presentation sample of the reconstructed "
                        "degree-80 active Laurent polynomial; not an interval proof"
                    ),
                }
            )
        return rows

    progress(started, "sampling global threshold profile", points=191)
    global_rows = sample_grid(Q(9, 20), Q(7, 5), 191, "global")
    progress(started, "sampling local threshold profile", points=151)
    local_rows = sample_grid(Q(159, 200), Q(81, 100), 151, "local")
    reference = next(
        mpmath.mpf(row["thresholdRadiusDecimal"])
        for row in local_rows
        if Q(row["characterExact"]) == Q(4, 5)
    )
    for row in local_rows:
        radius = mpmath.mpf(row["thresholdRadiusDecimal"])
        row["gainRelativeToFourFifthsPpmDecimal"] = mpmath.nstr(
            (radius / reference - 1) * 1_000_000,
            24,
        )

    profile_fields = [
        "grid",
        "sampleIndex",
        "characterExact",
        "characterDecimal",
        "thresholdRadiusDecimal",
        "absoluteResidualDecimal",
        "newtonIterations",
        "classification",
    ]
    write_csv(HERE / "global-threshold-profile.csv", profile_fields, global_rows)
    write_csv(
        HERE / "local-threshold-profile.csv",
        profile_fields[:6]
        + ["gainRelativeToFourFifthsPpmDecimal"]
        + profile_fields[6:],
        local_rows,
    )

    theorem = certificate["globalOptimizationTheorem"]
    face_rows = []
    for key, record in theorem["faceCertificates"].items():
        face_rows.append(
            {
                "key": key,
                "face": record["face"],
                "variable": record["variable"],
                "expectedSign": record["expectedSign"],
                "bernsteinDegree": record["bernsteinDegree"],
                "minimumSignedBernsteinCoefficientExact": record[
                    "minimumSignedBernsteinCoefficient"
                ]["exact"],
                "minimumSignedBernsteinCoefficientDecimal": record[
                    "minimumSignedBernsteinCoefficient"
                ]["decimal"],
                "signedBernsteinSha256": record["signedBernsteinSha256"],
            }
        )
    write_csv(
        HERE / "optimization-box.csv",
        list(face_rows[0]),
        face_rows,
    )

    ordered_competitors = sorted(
        certificate["rectangleDominance"]["records"],
        key=lambda record: Q(record["gapBelowActiveAtWindowLeft"]["exact"]),
    )
    competitor_rows = []
    for rank, record in enumerate(ordered_competitors, start=1):
        gap = Q(record["gapBelowActiveAtWindowLeft"]["exact"])
        competitor_rows.append(
            {
                "rankByGap": rank,
                "label": record["label"],
                "sector": record["sector"],
                "gapExact": str(gap),
                "gapDecimal": format(gmpy2.mpfr(gap), ".20g"),
                "isNearest": str(rank == 1).lower(),
                "classification": (
                    "formal exact competitor gap on the complete R0.50 rectangle"
                ),
            }
        )
    write_csv(
        HERE / "competitor-gaps.csv",
        list(competitor_rows[0]),
        competitor_rows,
    )

    shutil.copyfile(
        RESEARCH / "certificates/r050/progress.ndjson",
        HERE / "progress.ndjson",
    )
    shutil.copyfile(
        RESEARCH / "certificates/r050/resources.csv",
        HERE / "resources.csv",
    )
    metadata = {
        "createdAtUtc": datetime.now(timezone.utc).isoformat(),
        "precisionDecimalDigits": 90,
        "certificateSha256": EXPECTED_CERTIFICATE_SHA256,
        "globalSamples": len(global_rows),
        "localSamples": len(local_rows),
        "maximumGlobalAbsoluteResidual": max(
            row["absoluteResidualDecimal"] for row in global_rows
        ),
        "maximumLocalAbsoluteResidual": max(
            row["absoluteResidualDecimal"] for row in local_rows
        ),
        "wallSeconds": time.perf_counter() - started,
        "randomness": False,
    }
    (HERE / "sampling-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    progress(
        started,
        "figure tables complete",
        globalSamples=len(global_rows),
        localSamples=len(local_rows),
        competitors=len(competitor_rows),
    )


if __name__ == "__main__":
    main()
