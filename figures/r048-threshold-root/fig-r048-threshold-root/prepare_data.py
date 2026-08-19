#!/usr/bin/env python3
"""Extract R0.48 journal-figure tables from the pinned GMP certificate."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import shutil
import sys

import gmpy2


Q = gmpy2.mpq
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESEARCH = ROOT / "research"
sys.path.insert(0, str(RESEARCH))

import edge_charge_degree_lattice_audit as r047  # noqa: E402
import edge_charge_threshold_root_audit as r048  # noqa: E402
import edge_rational_asymptotic_audit as r028  # noqa: E402
import edge_short_continuation_audit as r036  # noqa: E402
import edge_weighted_restart_audit as r037  # noqa: E402


CERTIFICATE = RESEARCH / "certificates/r048/edge-charge-threshold-root.json"
EXPECTED_CERTIFICATE_SHA256 = (
    "246bcfa6623b1050511554312c32e9973b42b620a20ff571a1b5f340041c9af0"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decimal(value: Q, digits: int = 20) -> str:
    """Display-only decimal; every stored decision also retains exact data."""

    return format(float(value), f".{digits}g")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    if sha256(CERTIFICATE) != EXPECTED_CERTIFICATE_SHA256:
        raise SystemExit("R0.48 certificate hash mismatch")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if not all(certificate["checks"].values()) or len(certificate["checks"]) != 22:
        raise SystemExit("R0.48 certificate checks are incomplete")

    theorem = certificate["thresholdTheorem"]
    window_lower = Q(theorem["window"]["lower"]["exact"])
    window_upper = Q(theorem["window"]["upper"]["exact"])

    active_field, _, _, _ = r028.rational_edge_recurrence(80, False, 0.0)
    polynomial = r036.field_to_polynomial(active_field, 80)
    terms = r048.independent_terms(polynomial)
    active_column = r048.exact_column_polynomial(terms, 80, 81, 162, Q(3, 4))
    threshold = r048.threshold_polynomial(active_column)
    if r047.polynomial_digest(threshold) != theorem["polynomial"][
        "rationalCoefficientSha256"
    ]:
        raise SystemExit("reconstructed threshold-polynomial hash mismatch")

    curve_rows = []
    for sample_index in range(101):
        position = Q(sample_index, 100)
        radius = window_lower + position * (window_upper - window_lower)
        margin = r047.poly_evaluate(threshold, radius)
        curve_rows.append(
            {
                "sampleIndex": sample_index,
                "windowPositionExact": str(position),
                "windowPositionDecimal": decimal(position, 12),
                "radiusExact": str(radius),
                "radiusDecimal": decimal(radius, 18),
                "activeMarginExact": str(margin),
                "activeMarginDecimal": decimal(margin),
                "activeMarginPpmDecimal": decimal(margin * 1_000_000),
                "sign": "negative" if margin < 0 else "positive" if margin > 0 else "zero",
                "classification": (
                    "exact rational presentation sample of the explicit "
                    "degree-80 active-column polynomial"
                ),
            }
        )
    write_csv(
        HERE / "threshold-curve.csv",
        [
            "sampleIndex",
            "windowPositionExact",
            "windowPositionDecimal",
            "radiusExact",
            "radiusDecimal",
            "activeMarginExact",
            "activeMarginDecimal",
            "activeMarginPpmDecimal",
            "sign",
            "classification",
        ],
        curve_rows,
    )

    root = theorem["rootIsolation"]
    sturm = theorem["sturmCertificate"]
    root_rows = []
    for side, position in (("lower", 0), ("upper", 1)):
        root_rows.append(
            {
                "side": side,
                "normalizedBracketPosition": position,
                "radiusExact": root[side]["exact"],
                "radiusDecimal": root[side]["decimal"],
                "polynomialValueExact": root[f"{side}PolynomialValue"]["exact"],
                "polynomialValueDecimal": root[f"{side}PolynomialValue"]["decimal"],
                "polynomialValueAttoDecimal": decimal(
                    Q(root[f"{side}PolynomialValue"]["exact"]) * 10**18
                ),
                "sturmVariations": sturm[f"{side}Endpoint"]["variations"],
                "zeroSturmValues": sturm[f"{side}Endpoint"]["zeroValues"],
                "sturmSigns": sturm[f"{side}Endpoint"]["signs"],
            }
        )
    write_csv(
        HERE / "root-endpoints.csv",
        [
            "side",
            "normalizedBracketPosition",
            "radiusExact",
            "radiusDecimal",
            "polynomialValueExact",
            "polynomialValueDecimal",
            "polynomialValueAttoDecimal",
            "sturmVariations",
            "zeroSturmValues",
            "sturmSigns",
        ],
        root_rows,
    )

    source_competitors = theorem["fullWindowDominance"]["records"]
    ordered_competitors = sorted(
        source_competitors,
        key=lambda record: Q(record["gapBelowActiveAtWindowLeft"]["exact"]),
    )
    competitor_rows = []
    for rank, record in enumerate(ordered_competitors, start=1):
        gap = Q(record["gapBelowActiveAtWindowLeft"]["exact"])
        bound = Q(record["upperBoundAtWindowRight"]["exact"])
        competitor_rows.append(
            {
                "rankByGap": rank,
                "label": record["label"],
                "sector": record["sector"],
                "upperBoundAtWindowRightExact": str(bound),
                "upperBoundAtWindowRightDecimal": decimal(bound),
                "gapBelowActiveAtWindowLeftExact": str(gap),
                "gapBelowActiveAtWindowLeftDecimal": decimal(gap),
                "gapPpmDecimal": decimal(gap * 1_000_000),
                "isNearest": str(rank == 1).lower(),
                "classification": "formal full-window monotone-sandwich competitor",
            }
        )
    write_csv(
        HERE / "competitor-gaps.csv",
        [
            "rankByGap",
            "label",
            "sector",
            "upperBoundAtWindowRightExact",
            "upperBoundAtWindowRightDecimal",
            "gapBelowActiveAtWindowLeftExact",
            "gapBelowActiveAtWindowLeftDecimal",
            "gapPpmDecimal",
            "isNearest",
            "classification",
        ],
        competitor_rows,
    )

    active_lower = Q(theorem["activeColumn"]["valueAtWindowLower"]["exact"])
    top_rows = [
        {
            "order": 0,
            "label": "active s=162,j=81 (left)",
            "radiusSide": "window left",
            "boundExact": str(active_lower),
            "boundDecimal": decimal(active_lower),
            "distanceBelowOnePpmDecimal": decimal((1 - active_lower) * 1_000_000),
            "isActive": "true",
            "classification": "exact active-column lower bound across the window",
        }
    ]
    for order, record in enumerate(ordered_competitors[:7], start=1):
        bound = Q(record["upperBoundAtWindowRight"]["exact"])
        top_rows.append(
            {
                "order": order,
                "label": f'{record["label"]} (right)',
                "radiusSide": "window right",
                "boundExact": str(bound),
                "boundDecimal": decimal(bound),
                "distanceBelowOnePpmDecimal": decimal((1 - bound) * 1_000_000),
                "isActive": "false",
                "classification": "exact competitor upper bound across the window",
            }
        )
    write_csv(
        HERE / "sandwich-leaders.csv",
        [
            "order",
            "label",
            "radiusSide",
            "boundExact",
            "boundDecimal",
            "distanceBelowOnePpmDecimal",
            "isActive",
            "classification",
        ],
        top_rows,
    )

    shutil.copyfile(
        RESEARCH / "certificates/r048/progress.ndjson",
        HERE / "progress.ndjson",
    )
    shutil.copyfile(
        RESEARCH / "certificates/r048/resources.csv",
        HERE / "resources.csv",
    )


if __name__ == "__main__":
    main()
