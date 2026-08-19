#!/usr/bin/env python3
"""Extract plotted R0.38 radius, contraction, residual, and block metadata."""

from __future__ import annotations

import csv
from fractions import Fraction
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
CERTIFICATE = REPOSITORY / "research/certificates/r038/edge-tail-newton.json"


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
    low_block = payload["lowBlockPreconditionerAudit"]
    tail_columns = payload["finiteRegression"]["tailColumns"]
    candidate = payload["candidateComparison"]

    r031 = Fraction(restart["r031Radius"]["exact"])
    r037 = Fraction(restart["r037Radius"]["exact"])
    r038 = Fraction(restart["targetRadius"]["exact"])
    radius_rows = []
    for quantity, values in (
        (
            "bivariate_radius",
            (("R0.31", r031), ("R0.37", r037), ("R0.38", r038)),
        ),
        (
            "fixed_charge_radius",
            (("R0.31", r031**3), ("R0.37", r037**3), ("R0.38", r038**3)),
        ),
    ):
        baseline = values[0][1]
        for version, value in values:
            radius_rows.append(
                {
                    "quantity": quantity,
                    "version": version,
                    "exact": str(value),
                    "decimal": decimal(value),
                    "normalized_to_r031": str(value / baseline),
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
            "metric": "old_full_space_bound",
            "exact": restart["oldFullSpaceLinearizationBound"]["exact"],
            "decimal": restart["oldFullSpaceLinearizationBound"]["decimal"],
            "threshold": "1",
            "classification": "all-order but insufficient at target",
        },
        {
            "metric": "tail_linearization",
            "exact": restart["tailLinearizationBound"]["exact"],
            "decimal": restart["tailLinearizationBound"]["decimal"],
            "threshold": "1",
            "classification": "all-order tail upper bound",
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
        {
            "metric": "nearby_failure_probe",
            "exact": restart["nearbyFailureProbe"]["tailLinearizationBound"]["exact"],
            "decimal": restart["nearbyFailureProbe"]["tailLinearizationBound"]["decimal"],
            "threshold": "1",
            "classification": "negative control for sufficient inequality",
        },
        {
            "metric": "finite_tail_column",
            "exact": tail_columns["maximumWeightedColumnRatio"]["exact"],
            "decimal": tail_columns["maximumWeightedColumnRatio"]["decimal"],
            "threshold": "1",
            "classification": "finite exact regression only",
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
                "classification": "finite degree-80 complete residual",
            },
            {
                "metric": "residual_allowance",
                "exact": restart["residualAllowance"]["exact"],
                "decimal": restart["residualAllowance"]["decimal"],
                "classification": "all-order contraction allowance",
            },
        ],
    )

    finite_block = low_block["finiteBlock"]
    write_rows(
        PACKAGE / "preconditioner-metadata.csv",
        ("name", "exact_or_text", "classification"),
        [
            {
                "name": "finite_low_block_dimension",
                "exact_or_text": finite_block["dimension"],
                "classification": "finite exact",
            },
            {
                "name": "tail_low_projection_terms",
                "exact_or_text": tail_columns["lowProjectionTerms"],
                "classification": "finite grading regression",
            },
            {
                "name": "tail_defect_factor_after_low_preconditioner",
                "exact_or_text": "1",
                "classification": "all-order grading identity",
            },
            {
                "name": "finite_tail_columns",
                "exact_or_text": tail_columns["admissibleColumns"],
                "classification": "finite exact",
            },
            {
                "name": "candidate_gap_factor_lower",
                "exact_or_text": candidate["candidateGapFactorLower"]["exact"],
                "classification": "finite R0.32 diagnostic comparison",
            },
            {
                "name": "jacobian_sha256",
                "exact_or_text": finite_block["jacobianSha256"],
                "classification": "finite exact",
            },
            {
                "name": "inverse_sha256",
                "exact_or_text": finite_block["inverseSha256"],
                "classification": "finite exact",
            },
        ],
    )


if __name__ == "__main__":
    main()
