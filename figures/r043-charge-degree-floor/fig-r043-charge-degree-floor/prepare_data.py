#!/usr/bin/env python3
"""Extract exact R0.43 support, bridge, gate, and regression data."""

from __future__ import annotations

import csv
from fractions import Fraction
import json
from pathlib import Path
import shutil


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
CERTIFICATE_DIRECTORY = REPOSITORY / "research/certificates/r043"
CERTIFICATE = CERTIFICATE_DIRECTORY / "edge-charge-degree-floor.json"


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


def minimum_tail_degree(input_charge: int, cutoff: int) -> int:
    candidate = max(cutoff + 1, (input_charge + 1) // 2)
    while (candidate + input_charge) % 3:
        candidate += 1
    return candidate


def main() -> None:
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    target = payload["restartCertificate"]
    failure = payload["negativeControl"]
    charge_cutoff = target["chargeCutoff"]
    polynomial_cutoff = target["polynomialCutoff"]

    support_rows = []
    for input_charge in range(235, 256):
        cone_floor = (input_charge + 1) // 2
        support_rows.append(
            {
                "input_charge": input_charge,
                "generic_tail_floor": polynomial_cutoff + 1,
                "cone_degree_floor": cone_floor,
                "minimum_bivariate_degree": minimum_tail_degree(
                    input_charge,
                    polynomial_cutoff,
                ),
                "in_large_sector": input_charge >= charge_cutoff,
                "uniform_large_sector_floor": (
                    target["chargeImpliedDegreeFloor"]
                    if input_charge >= charge_cutoff
                    else ""
                ),
            }
        )
    write_rows(
        PACKAGE / "support-geometry.csv",
        (
            "input_charge",
            "generic_tail_floor",
            "cone_degree_floor",
            "minimum_bivariate_degree",
            "in_large_sector",
            "uniform_large_sector_floor",
        ),
        support_rows,
    )

    large = target["largeChargeTailSector"]
    legacy = Fraction(large["legacyBound"]["exact"])
    improved = Fraction(large["bound"]["exact"])
    bridge_rows: list[dict[str, object]] = [
        {
            "order": 0,
            "component": "legacy",
            "kind": "start",
            "exact": str(legacy),
            "decimal": decimal(legacy),
        }
    ]
    for order, group in enumerate(large["baseChargeContributions"], start=1):
        reduction = Fraction(group["reduction"]["exact"])
        bridge_rows.append(
            {
                "order": order,
                "component": group["baseChargeGroup"],
                "kind": "reduction",
                "exact": str(-reduction),
                "decimal": decimal(-reduction),
            }
        )
    bridge_rows.append(
        {
            "order": len(bridge_rows),
            "component": "improved",
            "kind": "end",
            "exact": str(improved),
            "decimal": decimal(improved),
        }
    )
    write_rows(
        PACKAGE / "large-sector-bridge.csv",
        ("order", "component", "kind", "exact", "decimal"),
        bridge_rows,
    )

    gate_rows = []
    for stage, record in (("target", target), ("failure", failure)):
        radius = Fraction(record["radius"]["exact"])
        for gate, field in (
            ("active tail", "tailLinearizationBound"),
            ("direct transport", "directTransportBound"),
            ("canonical stretch", "stretchOperatorBound"),
        ):
            value = Fraction(record[field]["exact"])
            full_field = stage == "target" or gate == "active tail"
            gate_rows.append(
                {
                    "stage": stage,
                    "radius_exact": str(radius),
                    "radius_decimal": decimal(radius),
                    "gate": gate,
                    "exact": str(value),
                    "decimal": decimal(value),
                    "threshold": "1",
                    "status": "passes" if value < 1 else "fails",
                    "scope": (
                        "full certified field"
                        if full_field
                        else "degree-80 polynomial diagnostic"
                    ),
                }
            )
    write_rows(
        PACKAGE / "proof-gates.csv",
        (
            "stage",
            "radius_exact",
            "radius_decimal",
            "gate",
            "exact",
            "decimal",
            "threshold",
            "status",
            "scope",
        ),
        gate_rows,
    )

    boundary_records = (
        (
            "improved",
            payload["previousRadiusControl"]["radius"],
            payload["previousRadiusControl"]["tailLinearizationBound"],
        ),
        (
            "legacy",
            payload["legacyFailureAtTarget"]["radius"],
            payload["legacyFailureAtTarget"]["tailBound"],
        ),
        ("improved", target["radius"], target["tailLinearizationBound"]),
        ("improved", failure["radius"], failure["tailLinearizationBound"]),
    )
    boundary_rows = []
    for method, radius_record, bound_record in boundary_records:
        radius = Fraction(radius_record["exact"])
        value = Fraction(bound_record["exact"])
        boundary_rows.append(
            {
                "method": method,
                "radius_exact": str(radius),
                "radius_decimal": decimal(radius),
                "exact": str(value),
                "decimal": decimal(value),
                "status": "passes" if value < 1 else "fails",
            }
        )
    write_rows(
        PACKAGE / "boundary-bracket.csv",
        (
            "method",
            "radius_exact",
            "radius_decimal",
            "exact",
            "decimal",
            "status",
        ),
        boundary_rows,
    )

    finite_rows = []
    regression = payload["finiteRegression"]["largeChargeColumns"]
    for record in regression["records"]:
        value = Fraction(record["exactColumn"]["exact"])
        bound = Fraction(record["allOrderLargeSectorBound"]["exact"])
        finite_rows.append(
            {
                "input_charge": record["inputCharge"],
                "input_degree": record["inputDegree"],
                "exact": str(value),
                "decimal": decimal(value),
                "sector_bound_exact": str(bound),
                "ratio_to_bound": str(value / bound),
                "below_sector_bound": record["belowSectorBound"],
                "classification": record["classification"],
            }
        )
    write_rows(
        PACKAGE / "finite-large-columns.csv",
        (
            "input_charge",
            "input_degree",
            "exact",
            "decimal",
            "sector_bound_exact",
            "ratio_to_bound",
            "below_sector_bound",
            "classification",
        ),
        finite_rows,
    )

    shutil.copyfile(CERTIFICATE_DIRECTORY / "progress.ndjson", PACKAGE / "progress.ndjson")
    shutil.copyfile(CERTIFICATE_DIRECTORY / "resources.csv", PACKAGE / "resources.csv")


if __name__ == "__main__":
    main()
