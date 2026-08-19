#!/usr/bin/env python3
"""Extract the plotted R0.39 radii, charge columns, and proof gates."""

from __future__ import annotations

import csv
from fractions import Fraction
import json
from pathlib import Path
import shutil


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
CERTIFICATE_DIRECTORY = REPOSITORY / "research/certificates/r039"
CERTIFICATE = CERTIFICATE_DIRECTORY / "edge-charge-resolved.json"
R038_CERTIFICATE = REPOSITORY / "research/certificates/r038/edge-tail-newton.json"


def write_rows(
    path: Path,
    fieldnames: tuple[str, ...],
    rows: list[dict[str, object]],
) -> None:
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def decimal(value: Fraction) -> str:
    return format(float(value), ".20g")


def main() -> None:
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    r038_payload = json.loads(R038_CERTIFICATE.read_text(encoding="utf-8"))
    restart = payload["restartCertificate"]

    radii = (
        ("R0.31", Fraction(restart["r031Radius"]["exact"])),
        ("R0.37", Fraction(r038_payload["restartCertificate"]["r037Radius"]["exact"])),
        ("R0.38", Fraction(restart["r038Radius"]["exact"])),
        ("R0.39", Fraction(restart["targetRadius"]["exact"])),
    )
    radius_rows: list[dict[str, object]] = []
    for quantity, power in (("common_radius", 1), ("fixed_charge_radius", 3)):
        baseline = radii[0][1] ** power
        for version, radius in radii:
            value = radius**power
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

    kernel = payload["chargeResolvedKernel"]
    maximum_sector = kernel["maximumSector"]
    charge_rows = []
    for record in kernel["finiteColumns"]:
        value = Fraction(record["bound"]["exact"])
        charge_rows.append(
            {
                "input_charge": record["inputCharge"],
                "minimum_tail_degree": record["minimumTailDegree"],
                "exact": str(value),
                "decimal": decimal(value),
                "is_maximum": str(record["inputCharge"]) == maximum_sector,
                "classification": "all-order fixed-charge column bound",
            }
        )
    write_rows(
        PACKAGE / "charge-columns.csv",
        (
            "input_charge",
            "minimum_tail_degree",
            "exact",
            "decimal",
            "is_maximum",
            "classification",
        ),
        charge_rows,
    )

    large = Fraction(kernel["largeChargeSector"]["bound"]["exact"])
    write_rows(
        PACKAGE / "large-charge-sector.csv",
        ("minimum_input_charge", "exact", "decimal", "classification"),
        [
            {
                "minimum_input_charge": restart["chargeCutoff"],
                "exact": str(large),
                "decimal": decimal(large),
                "classification": "analytic bound for every remaining input charge",
            }
        ],
    )

    mapping_ratio = Fraction(restart["mappingUpperBound"]["exact"]) / Fraction(
        restart["chosenBallRadius"]["exact"]
    )
    gates = [
        (
            "old_tail_bound",
            Fraction(restart["oldR038TailLinearizationBound"]["exact"]),
            "fails",
            "all-order charge-blind bound",
        ),
        (
            "charge_resolved_tail",
            Fraction(restart["chargeResolvedTailLinearizationBound"]["exact"]),
            "passes",
            "all-order charge-resolved bound",
        ),
        (
            "ball_mapping_ratio",
            mapping_ratio,
            "passes",
            "exact contraction ball ratio",
        ),
        (
            "old_transport_bound",
            Fraction(restart["oldScalarTransportBound"]["exact"]),
            "fails",
            "all-order scalar transport bound",
        ),
        (
            "refined_transport_bound",
            Fraction(restart["transportOperatorNormUpperBound"]["exact"]),
            "passes",
            "all-order charge-resolved transport bound",
        ),
        (
            "probe_transport_bound",
            Fraction(payload["negativeControl"]["transportOperatorBound"]["exact"]),
            "fails",
            "nearby negative control for the sufficient inequality",
        ),
    ]
    write_rows(
        PACKAGE / "proof-gates.csv",
        ("metric", "exact", "decimal", "threshold", "status", "classification"),
        [
            {
                "metric": name,
                "exact": str(value),
                "decimal": decimal(value),
                "threshold": "1",
                "status": status,
                "classification": classification,
            }
            for name, value, status, classification in gates
        ],
    )

    finite_rows = []
    for record in payload["finiteRegression"]["tailColumns"]:
        value = Fraction(record["maximumWeightedColumnRatio"]["exact"])
        finite_rows.append(
            {
                "input_degree": record["inputDegree"],
                "maximum_column_charge": record["maximumColumnCharge"],
                "exact": str(value),
                "decimal": decimal(value),
                "admissible_columns": record["admissibleColumns"],
                "classification": "finite exact regression only",
            }
        )
    write_rows(
        PACKAGE / "finite-column-regressions.csv",
        (
            "input_degree",
            "maximum_column_charge",
            "exact",
            "decimal",
            "admissible_columns",
            "classification",
        ),
        finite_rows,
    )

    shutil.copyfile(CERTIFICATE_DIRECTORY / "progress.ndjson", PACKAGE / "progress.ndjson")
    shutil.copyfile(CERTIFICATE_DIRECTORY / "resources.csv", PACKAGE / "resources.csv")


if __name__ == "__main__":
    main()
