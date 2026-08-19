#!/usr/bin/env python3
"""Extract the R0.32 exact Padé root and residue enclosures."""

from __future__ import annotations

import csv
from fractions import Fraction
import json
from pathlib import Path
import sys


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
CERTIFICATE = REPOSITORY / "research/certificates/r032/edge-singularity-candidates.json"

sys.set_int_max_str_digits(0)


def midpoint(record: dict[str, str]) -> str:
    value = (Fraction(record["lower"]) + Fraction(record["upper"])) / 2
    return format(float(value), ".17g")


def write_rows(path: Path, fieldnames: tuple[str, ...], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    diagnostic = payload["diagnostic"]
    rows: list[dict[str, object]] = []
    for record in diagnostic["transportApproximants"]:
        root = record["isolatedRoot"]
        residue = record["residue"]
        rows.append(
            {
                "field": record["field"].upper(),
                "coefficient_cut": record["coefficientCut"],
                "pade_order": record["padeOrder"][0],
                "root_lower": root["lower"],
                "root_upper": root["upper"],
                "root_mid": midpoint(root),
                "residue_lower": residue["lower"],
                "residue_upper": residue["upper"],
                "residue_mid": midpoint(residue),
                "classification": "transport branch candidate",
            }
        )
    for record in diagnostic["dCenterZeroApproximants"]:
        root = record["isolatedRoot"]
        residue = record["residue"]
        rows.append(
            {
                "field": "D center",
                "coefficient_cut": record["coefficientCut"],
                "pade_order": record["padeOrder"][0],
                "root_lower": root["lower"],
                "root_upper": root["upper"],
                "root_mid": midpoint(root),
                "residue_lower": residue["lower"],
                "residue_upper": residue["upper"],
                "residue_mid": midpoint(residue),
                "classification": "zero candidate",
            }
        )
    write_rows(
        PACKAGE / "candidate-poles.csv",
        (
            "field",
            "coefficient_cut",
            "pade_order",
            "root_lower",
            "root_upper",
            "root_mid",
            "residue_lower",
            "residue_upper",
            "residue_mid",
            "classification",
        ),
        rows,
    )

    guaranteed = payload["allOrderInput"]["guaranteedRadius"]
    summary_rows = [
        {
            "quantity": "fixed-charge guaranteed radius",
            "lower": guaranteed["exact"],
            "upper": guaranteed["exact"],
            "width": "0",
        }
    ]
    for quantity, record in (
        ("transport cluster, all cuts", diagnostic["transportClusterHull"]),
        ("transport cluster, cuts 42-50", diagnostic["tailTransportClusterHull"]),
        ("D-center zero cluster, all cuts", diagnostic["dCenterZeroClusterHull"]),
    ):
        summary_rows.append(
            {
                "quantity": quantity,
                "lower": record["lower"],
                "upper": record["upper"],
                "width": record["width"],
            }
        )
    write_rows(
        PACKAGE / "summary.csv",
        ("quantity", "lower", "upper", "width"),
        summary_rows,
    )


if __name__ == "__main__":
    main()
