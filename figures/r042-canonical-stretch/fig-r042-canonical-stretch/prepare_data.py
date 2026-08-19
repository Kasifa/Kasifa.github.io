#!/usr/bin/env python3
"""Extract exact R0.42 radius, gate, endpoint, and regression data."""

from __future__ import annotations

import csv
from fractions import Fraction
import json
from pathlib import Path
import shutil


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
CERTIFICATE_DIRECTORY = REPOSITORY / "research/certificates/r042"
CERTIFICATE = CERTIFICATE_DIRECTORY / "edge-stretch-transport.json"
R041_CERTIFICATE = (
    REPOSITORY / "research/certificates/r041/edge-degree-resolved-tail.json"
)
R040_CERTIFICATE = (
    REPOSITORY / "research/certificates/r040/edge-slope-resolved-transport.json"
)
R039_CERTIFICATE = (
    REPOSITORY / "research/certificates/r039/edge-charge-resolved.json"
)
R038_CERTIFICATE = (
    REPOSITORY / "research/certificates/r038/edge-tail-newton.json"
)


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
    r041 = json.loads(R041_CERTIFICATE.read_text(encoding="utf-8"))
    r040 = json.loads(R040_CERTIFICATE.read_text(encoding="utf-8"))
    r039 = json.loads(R039_CERTIFICATE.read_text(encoding="utf-8"))
    r038 = json.loads(R038_CERTIFICATE.read_text(encoding="utf-8"))
    target = payload["restartCertificate"]

    radii = (
        ("R0.31", Fraction(r040["restartCertificate"]["r031Radius"]["exact"])),
        (
            "R0.37",
            Fraction(r038["restartCertificate"]["r037Radius"]["exact"]),
        ),
        (
            "R0.38",
            Fraction(r039["restartCertificate"]["r038Radius"]["exact"]),
        ),
        ("R0.39", Fraction(r040["restartCertificate"]["r039Radius"]["exact"])),
        ("R0.40", Fraction(r041["restartCertificate"]["previousRadius"]["exact"])),
        ("R0.41", Fraction(target["previousRadius"]["exact"])),
        ("R0.42", Fraction(target["radius"]["exact"])),
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

    stages = (
        ("acceptance", "0.282", payload["acceptanceTest"]),
        ("target", "0.329", payload["restartCertificate"]),
        ("failure", "0.330", payload["negativeControl"]),
    )
    gate_rows: list[dict[str, object]] = []
    for stage, radius, record in stages:
        values = (
            ("active tail", Fraction(record["tailLinearizationBound"]["exact"])),
            ("direct transport", Fraction(record["directTransportBound"]["exact"])),
            ("canonical stretch", Fraction(record["stretchOperatorBound"]["exact"])),
        )
        for gate, value in values:
            full_field = stage != "failure" or gate == "active tail"
            gate_rows.append(
                {
                    "stage": stage,
                    "radius": radius,
                    "gate": gate,
                    "exact": str(value),
                    "decimal": decimal(value),
                    "threshold": "1",
                    "status": "passes" if value < 1 else "fails",
                    "scope": "full certified field" if full_field else "degree-80 polynomial only",
                    "classification": (
                        "all-order sufficient inequality"
                        if full_field
                        else "finite polynomial diagnostic at a failed active radius"
                    ),
                }
            )
    write_rows(
        PACKAGE / "proof-gates.csv",
        (
            "stage",
            "radius",
            "gate",
            "exact",
            "decimal",
            "threshold",
            "status",
            "scope",
            "classification",
        ),
        gate_rows,
    )

    endpoint_rows: list[dict[str, object]] = []
    for stage, radius, record in stages[:2]:
        for operator_key, operator_label in (
            ("directTransportComparison", "direct transport"),
            ("stretchOperator", "canonical stretch"),
        ):
            operator = record[operator_key]
            endpoint = next(
                item for item in operator["endpointColumns"] if item["label"] == "x=2"
            )
            polynomial = Fraction(endpoint["bound"]["exact"])
            tail = Fraction(endpoint["tailContributionUpperBound"]["exact"])
            total = Fraction(endpoint["totalBound"]["exact"])
            for component, value in (
                ("polynomial", polynomial),
                ("tail", tail),
                ("total", total),
            ):
                endpoint_rows.append(
                    {
                        "stage": stage,
                        "radius": radius,
                        "operator": operator_label,
                        "endpoint": "x=2",
                        "component": component,
                        "exact": str(value),
                        "decimal": decimal(value),
                        "status": "passes" if total < 1 else "fails",
                    }
                )
    write_rows(
        PACKAGE / "endpoint-decomposition.csv",
        (
            "stage",
            "radius",
            "operator",
            "endpoint",
            "component",
            "exact",
            "decimal",
            "status",
        ),
        endpoint_rows,
    )

    finite_rows: list[dict[str, object]] = []
    theorem = Fraction(
        target["stretchOperator"]["maximumPolynomialBound"]["exact"]
    )
    for record in payload["finiteRegression"]["stretchColumns"]:
        value = Fraction(record["maximumWeightedColumnRatio"]["exact"])
        finite_rows.append(
            {
                "input_degree": record["inputDegree"],
                "admissible_columns": record["admissibleColumns"],
                "maximum_charge": record["maximumColumnCharge"],
                "maximum_slope_exact": record["maximumInputSlope"]["exact"],
                "exact": str(value),
                "decimal": decimal(value),
                "theorem_exact": str(theorem),
                "equals_theorem": value == theorem,
                "classification": record["classification"],
            }
        )
    write_rows(
        PACKAGE / "finite-columns.csv",
        (
            "input_degree",
            "admissible_columns",
            "maximum_charge",
            "maximum_slope_exact",
            "exact",
            "decimal",
            "theorem_exact",
            "equals_theorem",
            "classification",
        ),
        finite_rows,
    )

    shutil.copyfile(CERTIFICATE_DIRECTORY / "progress.ndjson", PACKAGE / "progress.ndjson")
    shutil.copyfile(CERTIFICATE_DIRECTORY / "resources.csv", PACKAGE / "resources.csv")


if __name__ == "__main__":
    main()
