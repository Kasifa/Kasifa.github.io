#!/usr/bin/env python3
"""Extract R0.49 journal-figure tables from the pinned GMP certificate."""

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

import edge_charge_character_weight_audit as r049  # noqa: E402
import edge_charge_degree_lattice_audit as r047  # noqa: E402
import edge_charge_threshold_root_audit as r048  # noqa: E402
import edge_rational_asymptotic_audit as r028  # noqa: E402
import edge_short_continuation_audit as r036  # noqa: E402


CERTIFICATE = RESEARCH / "certificates/r049/edge-charge-character-weight.json"
EXPECTED_CERTIFICATE_SHA256 = (
    "b60405d395a4b927ab674af8cec1aef8f3b42e4962fd7118425851e075a49e44"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decimal(value: Q, digits: int = 20) -> str:
    context = gmpy2.get_context()
    old_precision = context.precision
    context.precision = 256
    try:
        return format(gmpy2.mpfr(value), f".{digits}g")
    finally:
        context.precision = old_precision


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    if sha256(CERTIFICATE) != EXPECTED_CERTIFICATE_SHA256:
        raise SystemExit("R0.49 certificate hash mismatch")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if not all(certificate["checks"].values()) or len(certificate["checks"]) != 31:
        raise SystemExit("R0.49 certificate checks are incomplete")

    theorem = certificate["thresholdTheorem"]
    window_lower = Q(theorem["window"]["lower"]["exact"])
    window_upper = Q(theorem["window"]["upper"]["exact"])
    character = Q(certificate["chargeCharacter"]["c"]["exact"])

    active_field, _, _, _ = r028.rational_edge_recurrence(80, False, 0.0)
    polynomial = r036.field_to_polynomial(active_field, 80)
    scaled = r049.charge_scale(polynomial, character)
    if r036.polynomial_digest(scaled) != certificate["chargeCharacter"][
        "chargeScaledPolynomialSha256"
    ]:
        raise SystemExit("reconstructed charge-scaled polynomial hash mismatch")
    terms = r048.independent_terms(scaled)
    active_column = r048.exact_column_polynomial(terms, 80, 81, 162, Q(1))
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
                    "degree-80 charge-character threshold polynomial"
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
    for side in ("lower", "upper"):
        root_rows.append(
            {
                "side": side,
                "radiusExact": root[side]["exact"],
                "radiusDecimal": root[side]["decimal"],
                "polynomialValueExact": root[f"{side}PolynomialValue"]["exact"],
                "polynomialValueDecimal": root[f"{side}PolynomialValue"]["decimal"],
                "sturmVariations": sturm[f"{side}Endpoint"]["variations"],
                "zeroSturmValues": sturm[f"{side}Endpoint"]["zeroValues"],
            }
        )
    write_csv(
        HERE / "root-endpoints.csv",
        [
            "side",
            "radiusExact",
            "radiusDecimal",
            "polynomialValueExact",
            "polynomialValueDecimal",
            "sturmVariations",
            "zeroSturmValues",
        ],
        root_rows,
    )

    contribution_rows = []
    contribution_source = theorem["activeColumn"]["chargeDistribution"]["records"]
    for record in contribution_source:
        charge = int(record["centerCharge"])
        contribution_rows.append(
            {
                "centerCharge": charge,
                "outputCharge": record["outputCharge"],
                "centerTermCount": record["centerTermCount"],
                "contributionExact": record["contribution"]["exact"],
                "contributionDecimal": record["contribution"]["decimal"],
                "shareExact": record["shareOfActiveColumn"]["exact"],
                "shareDecimal": record["shareOfActiveColumn"]["decimal"],
                "sharePercentDecimal": decimal(
                    Q(record["shareOfActiveColumn"]["exact"]) * 100
                ),
                "displayGroup": (
                    f"q={charge:+d}" if charge in (-1, 0, 1, 2, 3) else "q>=+4"
                ),
                "classification": "exact active-column contribution by center charge",
            }
        )
    write_csv(
        HERE / "charge-contributions.csv",
        [
            "centerCharge",
            "outputCharge",
            "centerTermCount",
            "contributionExact",
            "contributionDecimal",
            "shareExact",
            "shareDecimal",
            "sharePercentDecimal",
            "displayGroup",
            "classification",
        ],
        contribution_rows,
    )

    ordered_competitors = sorted(
        theorem["fullWindowDominance"]["records"],
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

    old_radius = Q(certificate["input"]["r048"]["previousRootUpper"]["exact"])
    rho_z = Q(certificate["anisotropicGeometry"]["rhoZ"]["exact"])
    rho_w = Q(certificate["anisotropicGeometry"]["rhoW"]["exact"])
    geometry = [
        ("Z polyradius", rho_z / old_radius, "rho_Z / r_(48,U)"),
        ("W polyradius", rho_w / old_radius, "rho_W / r_(48,U)"),
        ("R=Z^2W disk", window_lower**3 / old_radius**3, "r_(49,L)^3 / r_(48,U)^3"),
    ]
    geometry_rows = []
    for order, (label, ratio, definition) in enumerate(geometry):
        geometry_rows.append(
            {
                "order": order,
                "label": label,
                "ratioExact": str(ratio),
                "ratioDecimal": decimal(ratio),
                "percentChangeExact": str((ratio - 1) * 100),
                "percentChangeDecimal": decimal((ratio - 1) * 100),
                "definition": definition,
                "referenceRadiusExact": str(old_radius),
                "classification": (
                    "exact normalized geometry comparison; the old and new "
                    "polydiscs are not nested"
                ),
            }
        )
    write_csv(
        HERE / "anisotropic-geometry.csv",
        [
            "order",
            "label",
            "ratioExact",
            "ratioDecimal",
            "percentChangeExact",
            "percentChangeDecimal",
            "definition",
            "referenceRadiusExact",
            "classification",
        ],
        geometry_rows,
    )

    shutil.copyfile(
        RESEARCH / "certificates/r049/progress.ndjson",
        HERE / "progress.ndjson",
    )
    shutil.copyfile(
        RESEARCH / "certificates/r049/resources.csv",
        HERE / "resources.csv",
    )


if __name__ == "__main__":
    main()
