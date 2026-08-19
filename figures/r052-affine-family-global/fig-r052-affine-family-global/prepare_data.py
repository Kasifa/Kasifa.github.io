#!/usr/bin/env python3
"""Prepare exact and certificate-backed data for the R0.52 journal figure."""

from __future__ import annotations

import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time

import gmpy2


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[2]
RESEARCH = ROOT / "research"
sys.path.insert(0, str(RESEARCH))

import edge_affine_family_kkt_audit as r052  # noqa: E402
import edge_charge_character_optimization_audit as r050  # noqa: E402
import edge_charge_threshold_root_audit as r048  # noqa: E402
import edge_rational_asymptotic_audit as r028  # noqa: E402
import edge_short_continuation_audit as r036  # noqa: E402


Rational = gmpy2.mpq
CERTIFICATE = RESEARCH / "certificates/r052/edge-affine-family-global.json"
EXPECTED_CERTIFICATE_SHA256 = (
    "b79e59ec327bc02b64e23ad3f903b6d61860a075d59ff75a43d82f5684590def"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(name: str, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with (PACKAGE / name).open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def evaluate_laurent(polynomial: dict[int, Rational], character: Rational) -> Rational:
    return sum(
        (
            coefficient * character**exponent
            for exponent, coefficient in polynomial.items()
        ),
        Rational(0),
    )


def exact_feasibility_polynomial(
    radius: Rational,
) -> tuple[dict[int, Rational], str, int, int]:
    started = time.perf_counter()
    active_field, _, _, interactions = r028.rational_edge_recurrence(
        80, True, started
    )
    center = r036.field_to_polynomial(active_field, 80)
    center_digest = r036.polynomial_digest(center)
    terms = r048.independent_terms(center)
    active_terms = r050.active_laurent_terms(terms, 81, 162)
    zero_terms = r052.zero_terms(terms, 80)

    one = {0: Rational(1)}
    m0 = r052.fixed_radius_moment(active_terms, radius, lambda _q: 1)
    m1 = r052.fixed_radius_moment(active_terms, radius, lambda q: q)
    u0 = r052.fixed_radius_moment(zero_terms, radius, lambda _q: 1)
    u1 = r052.fixed_radius_moment(zero_terms, radius, abs)
    one_minus_u0 = r052.laurent_add((one, Rational(1)), (u0, Rational(-1)))
    m0_minus_one = r052.laurent_add((m0, Rational(1)), (one, Rational(-1)))
    zero_denominator = r052.laurent_add(
        (u1, Rational(1)),
        (one_minus_u0, Rational(162)),
    )
    feasibility = r052.laurent_add(
        (r052.laurent_multiply(m1, one_minus_u0), Rational(-1)),
        (
            r052.laurent_multiply(m0_minus_one, zero_denominator),
            Rational(-1),
        ),
    )
    return feasibility, center_digest, len(terms), interactions


def main() -> None:
    started = time.perf_counter()
    if sha256(CERTIFICATE) != EXPECTED_CERTIFICATE_SHA256:
        raise AssertionError("R0.52 certificate hash mismatch")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if len(certificate["checks"]) != 22 or not all(certificate["checks"].values()):
        raise AssertionError("R0.52 certificate checks are incomplete")

    radius_upper = Rational(
        certificate["globalAffineFamilyBound"]["optimalRadiusUpper"]["exact"]
    )
    feasibility, center_digest, center_terms, interactions = (
        exact_feasibility_polynomial(radius_upper)
    )
    expected_polynomial_digest = certificate["finiteConstruction"][
        "degreeEightyPolynomialSha256"
    ]
    if center_digest != expected_polynomial_digest:
        raise AssertionError("degree-80 center digest changed")

    character_box = certificate["rootIsolation"]["character"]
    character_lower = Rational(character_box[0]["exact"])
    character_upper = Rational(character_box[1]["exact"])
    character_midpoint = (character_lower + character_upper) / 2
    profile_rows = []
    for exponent in range(1, 41):
        distance = Rational(1, 10**exponent)
        for side, sign in (("left", -1), ("right", 1)):
            character = character_midpoint + sign * distance
            value = -character**2 * evaluate_laurent(feasibility, character)
            if value <= 0:
                raise AssertionError("sampled eliminated feasibility lost negativity")
            profile_rows.append(
                {
                    "side": side,
                    "distanceExponent": exponent,
                    "distanceExact": str(distance),
                    "distanceDecimal": r052.r037.rational_decimal(distance, 24),
                    "characterExact": str(character),
                    "negativeClearedFeasibilityExact": str(value),
                    "negativeClearedFeasibilityDecimal": (
                        r052.r037.rational_decimal(value, 24)
                    ),
                    "valueSha256": r052.r037.rational_digest(value),
                    "classification": "exact rational presentation sample",
                }
            )
    write_csv(
        "feasibility-profile.csv",
        [
            "side",
            "distanceExponent",
            "distanceExact",
            "distanceDecimal",
            "characterExact",
            "negativeClearedFeasibilityExact",
            "negativeClearedFeasibilityDecimal",
            "valueSha256",
            "classification",
        ],
        profile_rows,
    )

    krawczyk = certificate["rootIsolation"]["krawczykCertificate"]
    contraction_rows = []
    for index, variable in enumerate(("r", "c", "alpha")):
        box_key = {"r": "radius", "c": "character", "alpha": "alpha162"}[
            variable
        ]
        lower, upper = certificate["rootIsolation"][box_key]
        width = Rational(upper["exact"]) - Rational(lower["exact"])
        image_radius = krawczyk["krawczykImageRadii"][index]
        contraction_rows.append(
            {
                "variable": variable,
                "boxWidthExact": str(width),
                "boxWidthDecimal": r052.r037.rational_decimal(width, 24),
                "krawczykImageRadiusDecimal": image_radius["decimal"],
                "krawczykImageRadiusSha256": image_radius["sha256"],
                "classification": (
                    "exact box width and certificate-rendered exact image radius"
                ),
            }
        )
    write_csv(
        "krawczyk-contraction.csv",
        [
            "variable",
            "boxWidthExact",
            "boxWidthDecimal",
            "krawczykImageRadiusDecimal",
            "krawczykImageRadiusSha256",
            "classification",
        ],
        contraction_rows,
    )

    competitor_rows = []
    inactive = certificate["inactiveSectorTheorem"]
    ordered = sorted(
        inactive["inactiveRecords"],
        key=lambda record: float(record["gapBelowOne"]["decimal"]),
    )
    for rank, record in enumerate(ordered, start=1):
        competitor_rows.append(
            {
                "rankByGap": rank,
                "label": record["label"],
                "gapDecimal": record["gapBelowOne"]["decimal"],
                "gapSha256": record["gapBelowOne"]["sha256"],
                "isNearest": str(rank == 1).lower(),
                "classification": "formal exact root-box upper-envelope gap",
            }
        )
    write_csv(
        "inactive-gaps.csv",
        [
            "rankByGap",
            "label",
            "gapDecimal",
            "gapSha256",
            "isNearest",
            "classification",
        ],
        competitor_rows,
    )

    metadata = {
        "schemaVersion": "1.0",
        "createdUtc": datetime.now(timezone.utc).isoformat(),
        "certificateSha256": EXPECTED_CERTIFICATE_SHA256,
        "sourceCommit": certificate["git"]["commit"],
        "radiusUpper": str(radius_upper),
        "characterMidpoint": str(character_midpoint),
        "profileRows": len(profile_rows),
        "profileDistanceExponents": [1, 40],
        "contractionRows": len(contraction_rows),
        "inactiveRows": len(competitor_rows),
        "nearestInactiveSector": inactive["nearestInactiveSector"],
        "minimumInactiveGapDecimal": inactive["minimumGapBelowOne"]["decimal"],
        "maximumBernsteinCoefficientDecimal": certificate[
            "globalUpperCertificate"
        ]["maximumBoxSignCertificate"]["maximumBernsteinCoefficient"]["decimal"],
        "descartesSignVariations": certificate["globalUpperCertificate"]
        ["derivativeRootTheorem"]["descartesSignVariations"],
        "positiveDerivativeRootsExactly": certificate["globalUpperCertificate"]
        ["derivativeRootTheorem"]["positiveRootsExactly"],
        "centerTerms": center_terms,
        "recurrenceOrderedInteractions": interactions,
        "degreeEightyPolynomialSha256": center_digest,
        "randomness": False,
        "formalArithmetic": "gmpy2.mpq",
        "wallSeconds": time.perf_counter() - started,
    }
    (PACKAGE / "sampling-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "profileRows": len(profile_rows),
                "contractionRows": len(contraction_rows),
                "inactiveRows": len(competitor_rows),
                "wallSeconds": metadata["wallSeconds"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
