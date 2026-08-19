#!/usr/bin/env python3
"""Extract plotted R0.37 radius, contraction, and inverse metadata."""

from __future__ import annotations

import csv
from fractions import Fraction
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
CERTIFICATE = REPOSITORY / "research/certificates/r037/edge-weighted-restart.json"


def write_rows(
    path: Path, fieldnames: tuple[str, ...], rows: list[dict[str, object]]
) -> None:
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def decimal(value: Fraction) -> str:
    return format(float(value), ".20g")


def main() -> None:
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    restart = payload["restartCertificate"]
    boundary = payload["boundaryInfiniteInverse"]
    jacobian = payload["finiteRegression"]["jacobian"]

    old_radius = Fraction(restart["r031Radius"]["exact"])
    new_radius = Fraction(restart["targetRadius"]["exact"])
    radius_rows = []
    for quantity, old_value, new_value in (
        ("bivariate_radius", old_radius, new_radius),
        ("fixed_charge_radius", old_radius**3, new_radius**3),
    ):
        for version, value in (("R0.31", old_value), ("R0.37", new_value)):
            radius_rows.append(
                {
                    "quantity": quantity,
                    "version": version,
                    "exact": str(value),
                    "decimal": decimal(value),
                    "normalized_to_r031": str(value / old_value),
                }
            )
    write_rows(
        PACKAGE / "radius-gain.csv",
        ("quantity", "version", "exact", "decimal", "normalized_to_r031"),
        radius_rows,
    )

    mapping_ratio = Fraction(restart["mappingUpperBound"]["exact"]) / Fraction(
        restart["chosenBallRadius"]["exact"]
    )
    contraction_rows = [
        {
            "metric": "active_linearization",
            "exact": restart["linearizationNormUpperBound"]["exact"],
            "decimal": restart["linearizationNormUpperBound"]["decimal"],
            "threshold": "1",
            "classification": "all-order upper bound",
        },
        {
            "metric": "ball_mapping_ratio",
            "exact": str(mapping_ratio),
            "decimal": decimal(mapping_ratio),
            "threshold": "1",
            "classification": "exact contraction ratio",
        },
        {
            "metric": "ball_lipschitz",
            "exact": restart["lipschitzUpperBound"]["exact"],
            "decimal": restart["lipschitzUpperBound"]["decimal"],
            "threshold": "1",
            "classification": "all-order upper bound",
        },
        {
            "metric": "transport_operator",
            "exact": restart["transportOperatorNormUpperBound"]["exact"],
            "decimal": restart["transportOperatorNormUpperBound"]["decimal"],
            "threshold": "1",
            "classification": "all-order upper bound",
        },
    ]
    write_rows(
        PACKAGE / "contraction.csv",
        ("metric", "exact", "decimal", "threshold", "classification"),
        contraction_rows,
    )

    write_rows(
        PACKAGE / "residual-scales.csv",
        ("metric", "exact", "decimal", "classification"),
        [
            {
                "metric": "exact_residual_norm",
                "exact": restart["exactResidualNorm"]["exact"],
                "decimal": restart["exactResidualNorm"]["decimal"],
                "classification": "finite polynomial, complete residual",
            },
            {
                "metric": "residual_allowance",
                "exact": restart["residualAllowance"]["exact"],
                "decimal": restart["residualAllowance"]["decimal"],
                "classification": "all-order contraction allowance",
            },
        ],
    )

    write_rows(
        PACKAGE / "inverse-metadata.csv",
        ("name", "exact_or_text"),
        [
            {
                "name": "boundary_infinite_inverse_norm_bound",
                "exact_or_text": boundary["inverseNormUpperBound"]["exact"],
            },
            {"name": "finite_jacobian_dimension", "exact_or_text": jacobian["dimension"]},
            {
                "name": "finite_restart_derivative_norm",
                "exact_or_text": jacobian["radii"]["restartRadius"][
                    "finiteDerivativeWeightedColumnNorm"
                ]["exact"],
            },
            {
                "name": "finite_restart_inverse_norm",
                "exact_or_text": jacobian["radii"]["restartRadius"][
                    "finiteInverseWeightedColumnNorm"
                ]["exact"],
            },
            {"name": "jacobian_sha256", "exact_or_text": jacobian["jacobianSha256"]},
            {"name": "inverse_sha256", "exact_or_text": jacobian["inverseSha256"]},
        ],
    )


if __name__ == "__main__":
    main()
