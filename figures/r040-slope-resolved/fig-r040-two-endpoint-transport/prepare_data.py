#!/usr/bin/env python3
"""Extract R0.40 radius, endpoint-column, and proof-gate data."""

from __future__ import annotations

import csv
from fractions import Fraction
import json
from pathlib import Path
import shutil
import sys


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
sys.path.insert(0, str(REPOSITORY / "research"))

import edge_rational_asymptotic_audit as r028
import edge_short_continuation_audit as r036
import edge_weighted_restart_audit as r037
import edge_slope_resolved_transport_audit as r040


CERTIFICATE_DIRECTORY = REPOSITORY / "research/certificates/r040"
CERTIFICATE = CERTIFICATE_DIRECTORY / "edge-slope-resolved-transport.json"
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
    r039_payload = json.loads(R039_CERTIFICATE.read_text(encoding="utf-8"))
    r038_payload = json.loads(R038_CERTIFICATE.read_text(encoding="utf-8"))
    restart = payload["restartCertificate"]

    radii = (
        ("R0.31", Fraction(restart["r031Radius"]["exact"])),
        (
            "R0.37",
            Fraction(r038_payload["restartCertificate"]["r037Radius"]["exact"]),
        ),
        (
            "R0.38",
            Fraction(r039_payload["restartCertificate"]["r038Radius"]["exact"]),
        ),
        ("R0.39", Fraction(restart["r039Radius"]["exact"])),
        ("R0.40", Fraction(restart["targetRadius"]["exact"])),
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

    active_field, _, _, _ = r028.rational_edge_recurrence(80, False, 0.0)
    polynomial = r036.field_to_polynomial(active_field, 80)
    if r037.polynomial_digest(polynomial) != restart["degreeEightyPolynomialSha256"]:
        raise AssertionError("degree-80 polynomial digest mismatch")
    radius = r040.rational(restart["targetRadius"]["exact"])
    endpoint_rows = []
    for input_degree in range(1, 82):
        for label, input_charge in (
            ("x=-1", -input_degree),
            ("x=2", 2 * input_degree),
        ):
            value = r040.exact_transport_column(
                polynomial,
                radius,
                input_degree,
                input_charge,
            )
            endpoint_rows.append(
                {
                    "input_degree": input_degree,
                    "endpoint": label,
                    "input_charge": input_charge,
                    "exact": str(value),
                    "decimal": decimal(Fraction(str(value))),
                    "is_global_maximum": (
                        input_degree == 1
                        and label
                        == payload["transportKernel"]["maximumPolynomialEndpoint"]
                    ),
                    "classification": (
                        "exact finite column; all-order monotonicity theorem "
                        "covers every larger degree"
                    ),
                }
            )
    write_rows(
        PACKAGE / "endpoint-columns.csv",
        (
            "input_degree",
            "endpoint",
            "input_charge",
            "exact",
            "decimal",
            "is_global_maximum",
            "classification",
        ),
        endpoint_rows,
    )

    endpoint_totals = {
        record["label"]: Fraction(record["totalBound"]["exact"])
        for record in payload["transportKernel"]["endpointColumns"]
    }
    gates = [
        (
            "target_active_tail",
            Fraction(restart["activeTailLinearizationBound"]["exact"]),
            "passes",
            "all-order active-tail bound at 32/125",
        ),
        (
            "r039_termwise_transport",
            Fraction(restart["r039TermwiseTransportBound"]["exact"]),
            "fails",
            "R0.39 termwise transport bound at 32/125",
        ),
        (
            "target_transport_x_minus_1",
            endpoint_totals["x=-1"],
            "passes",
            "R0.40 all-order x=-1 endpoint including strict tail",
        ),
        (
            "target_transport_x_plus_2",
            endpoint_totals["x=2"],
            "passes",
            "R0.40 all-order x=2 endpoint including strict tail",
        ),
        (
            "probe_active_tail",
            Fraction(
                payload["negativeControl"]["activeTailLinearizationBound"]["exact"]
            ),
            "fails",
            "active-tail negative control at 257/1000",
        ),
        (
            "probe_polynomial_transport",
            Fraction(
                payload["negativeControl"][
                    "polynomialTransportEndpointBound"
                ]["exact"]
            ),
            "passes",
            "exact polynomial transport endpoint at 257/1000",
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
    for record in payload["finiteRegression"]["transportColumns"]:
        value = Fraction(record["maximumWeightedColumnRatio"]["exact"])
        finite_rows.append(
            {
                "input_degree": record["inputDegree"],
                "maximum_column_charge": record["maximumColumnCharge"],
                "maximum_input_slope": record["maximumInputSlope"]["exact"],
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
            "maximum_input_slope",
            "exact",
            "decimal",
            "admissible_columns",
            "classification",
        ),
        finite_rows,
    )

    shutil.copyfile(
        CERTIFICATE_DIRECTORY / "progress.ndjson",
        PACKAGE / "progress.ndjson",
    )
    shutil.copyfile(
        CERTIFICATE_DIRECTORY / "resources.csv",
        PACKAGE / "resources.csv",
    )


if __name__ == "__main__":
    main()
