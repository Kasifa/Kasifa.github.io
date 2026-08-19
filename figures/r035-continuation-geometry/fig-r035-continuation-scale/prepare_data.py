#!/usr/bin/env python3
"""Extract exact R0.35 continuation geometry and operator witnesses."""

from __future__ import annotations

import csv
from fractions import Fraction
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
CERTIFICATE = (
    REPOSITORY / "research/certificates/r035/edge-continuation-geometry.json"
)


def write_rows(
    path: Path, fieldnames: tuple[str, ...], rows: list[dict[str, object]]
) -> None:
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    geometry = payload["fixedChargeExtraction"]
    r031 = geometry["r031"]
    candidate = geometry["r032FiniteCandidate"]
    operator = payload["operatorScale"]

    write_rows(
        PACKAGE / "geometry.csv",
        ("metric", "exact_lower", "exact_upper", "decimal_lower", "decimal_upper"),
        [
            {
                "metric": "r031_bivariate_radius",
                "exact_lower": r031["bivariateRadius"],
                "exact_upper": r031["bivariateRadius"],
                "decimal_lower": r031["bivariateRadiusDecimal"],
                "decimal_upper": r031["bivariateRadiusDecimal"],
            },
            {
                "metric": "r031_fixed_charge_radius",
                "exact_lower": r031["fixedChargeRadius"],
                "exact_upper": r031["fixedChargeRadius"],
                "decimal_lower": r031["fixedChargeRadiusDecimal"],
                "decimal_upper": r031["fixedChargeRadiusDecimal"],
            },
            {
                "metric": "r032_candidate_abs_R",
                "exact_lower": candidate["absoluteRLower"],
                "exact_upper": candidate["absoluteRUpper"],
                "decimal_lower": candidate["absoluteRLowerDecimal"],
                "decimal_upper": candidate["absoluteRUpperDecimal"],
            },
            {
                "metric": "r032_candidate_balanced_radius",
                "exact_lower": candidate["balancedRadiusLower"],
                "exact_upper": candidate["balancedRadiusUpper"],
                "decimal_lower": candidate["balancedRadiusLowerDecimal"],
                "decimal_upper": candidate["balancedRadiusUpperDecimal"],
            },
            {
                "metric": "balanced_radius_ratio",
                "exact_lower": candidate["balancedToR031RadiusRatioLower"],
                "exact_upper": candidate["balancedToR031RadiusRatioUpper"],
                "decimal_lower": candidate[
                    "balancedToR031RadiusRatioLowerDecimal"
                ],
                "decimal_upper": candidate[
                    "balancedToR031RadiusRatioUpperDecimal"
                ],
            },
            {
                "metric": "fixed_charge_R_ratio",
                "exact_lower": candidate["absoluteRToR031FixedChargeRatioLower"],
                "exact_upper": candidate["absoluteRToR031FixedChargeRatioUpper"],
                "decimal_lower": candidate[
                    "absoluteRToR031FixedChargeRatioLowerDecimal"
                ],
                "decimal_upper": candidate[
                    "absoluteRToR031FixedChargeRatioUpperDecimal"
                ],
            },
        ],
    )

    witness_rows: list[dict[str, object]] = []
    for n in range(1, 129):
        same = Fraction(3 * n * n, 4 * (2 * n - 1))
        half = same / (4**n)
        witness_rows.append(
            {
                "N": n,
                "same_radius_exact": str(same),
                "same_radius_decimal": format(float(same), ".18g"),
                "half_radius_exact": str(half),
                "half_radius_decimal": format(float(half), ".18g"),
            }
        )
    write_rows(
        PACKAGE / "operator-witness.csv",
        (
            "N",
            "same_radius_exact",
            "same_radius_decimal",
            "half_radius_exact",
            "half_radius_decimal",
        ),
        witness_rows,
    )

    half_bound = operator["halfRadiusBilinearBound"]
    multipliers = operator["halfRadiusMultipliers"]
    write_rows(
        PACKAGE / "operator-constants.csv",
        ("name", "exact", "decimal"),
        [
            {
                "name": "first_derivative_multiplier",
                "exact": multipliers["sup_n_n_over_2n"],
                "decimal": format(float(Fraction(multipliers["sup_n_n_over_2n"])), ".18g"),
            },
            {
                "name": "second_derivative_multiplier",
                "exact": multipliers["sup_n_n2_over_2n"],
                "decimal": format(float(Fraction(multipliers["sup_n_n2_over_2n"])), ".18g"),
            },
            {
                "name": "mixed_derivative_multiplier",
                "exact": multipliers["sup_nm_nm_over_2n2m"],
                "decimal": format(float(Fraction(multipliers["sup_nm_nm_over_2n2m"])), ".18g"),
            },
            {
                "name": "half_radius_bilinear_bound",
                "exact": half_bound["total"],
                "decimal": format(float(Fraction(half_bound["total"])), ".18g"),
            },
        ],
    )


if __name__ == "__main__":
    main()
