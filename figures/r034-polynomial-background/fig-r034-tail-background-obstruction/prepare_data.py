#!/usr/bin/env python3
"""Extract the exact R0.34 tail-background diagnostics for plotting."""

from __future__ import annotations

import csv
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
CERTIFICATE = (
    REPOSITORY / "research/certificates/r034/edge-polynomial-background.json"
)
SEQUENCE_ORDER = ("B_U", "B_V", "H_U", "H_V")


def write_rows(
    path: Path, fieldnames: tuple[str, ...], rows: list[dict[str, object]]
) -> None:
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    searches = payload["finiteWindowAudit"]["searches"]

    thresholds: list[dict[str, object]] = []
    witnesses: list[dict[str, object]] = []
    for sequence in SEQUENCE_ORDER:
        search = searches[sequence]
        witness = search["witness"]
        thresholds.append(
            {
                "sequence": sequence,
                "family": "transport" if sequence.startswith("B_") else "D-log",
                "maximum_excluded_degree": search[
                    "backgroundDegreeExcludedThrough"
                ],
                "witness_shift": witness["shift"],
                "witness_order": witness["order"],
                "monomial_indices": ";".join(
                    str(value) for value in witness["monomialIndices"]
                ),
                "determinant_sha256": witness["determinantSha256"],
            }
        )
        witnesses.append(
            {
                "sequence": sequence,
                "shift": witness["shift"],
                "order": witness["order"],
                "monomial_indices": ";".join(
                    str(value) for value in witness["monomialIndices"]
                ),
                "determinant": witness["determinant"],
                "determinant_decimal": witness["decimal"],
                "numerator_digits": witness["numeratorDigits"],
                "denominator_digits": witness["denominatorDigits"],
                "determinant_sha256": witness["determinantSha256"],
            }
        )

    write_rows(
        PACKAGE / "thresholds.csv",
        (
            "sequence",
            "family",
            "maximum_excluded_degree",
            "witness_shift",
            "witness_order",
            "monomial_indices",
            "determinant_sha256",
        ),
        thresholds,
    )
    write_rows(
        PACKAGE / "witnesses.csv",
        (
            "sequence",
            "shift",
            "order",
            "monomial_indices",
            "determinant",
            "determinant_decimal",
            "numerator_digits",
            "denominator_digits",
            "determinant_sha256",
        ),
        witnesses,
    )

    tail_rows: list[dict[str, object]] = []
    for sequence in SEQUENCE_ORDER:
        search = searches[sequence]
        by_shift = {
            int(record["shift"]): record for record in search["shiftSummaries"]
        }
        maximal = int(search["maximalNegativeShift"])
        for shift in range(40, 50):
            record = by_shift.get(shift)
            tail_rows.append(
                {
                    "sequence": sequence,
                    "shift": shift,
                    "available": int(record is not None),
                    "coefficient_count_available": (
                        record["coefficientCountAvailable"] if record else 0
                    ),
                    "principal_minor_count": (
                        record["principalMinorCount"] if record else 0
                    ),
                    "negative_count": record["negativeCount"] if record else 0,
                    "negative_orders": (
                        ";".join(str(value) for value in record["negativeOrders"])
                        if record
                        else ""
                    ),
                    "is_maximal_witness_shift": int(shift == maximal),
                }
            )
    write_rows(
        PACKAGE / "tail-search.csv",
        (
            "sequence",
            "shift",
            "available",
            "coefficient_count_available",
            "principal_minor_count",
            "negative_count",
            "negative_orders",
            "is_maximal_witness_shift",
        ),
        tail_rows,
    )


if __name__ == "__main__":
    main()

