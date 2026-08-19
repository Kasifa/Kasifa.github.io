#!/usr/bin/env python3
"""Validate every R0.40 plotted value against pinned exact certificates."""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
sys.path.insert(0, str(REPOSITORY / "research"))

import edge_rational_asymptotic_audit as r028
import edge_short_continuation_audit as r036
import edge_weighted_restart_audit as r037
import edge_slope_resolved_transport_audit as r040


R040 = REPOSITORY / "research/certificates/r040/edge-slope-resolved-transport.json"
R039 = REPOSITORY / "research/certificates/r039/edge-charge-resolved.json"
R038 = REPOSITORY / "research/certificates/r038/edge-tail-newton.json"
EXPECTED = {
    R040: "cc6257637b42798e9fdf17ef66531bf263072057f38c130320ed108fb116fc3b",
    R039: "59b978c1c5384edb394adc76add0950b3c8e6666f6562dfc199584c22dd0e700",
    R038: "3eb320e8cef0289c7fa2fef00a38c3c66b6b4c5006375bf6386d784f6b95dbf4",
}
SOURCE_COMMIT = "413f1cbcb12a961129eacf2482eb9b705c9a2feb"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    for path, expected in EXPECTED.items():
        if sha256(path) != expected:
            raise AssertionError(f"pinned certificate hash mismatch: {path}")
    payload = json.loads(R040.read_text(encoding="utf-8"))
    r039_payload = json.loads(R039.read_text(encoding="utf-8"))
    r038_payload = json.loads(R038.read_text(encoding="utf-8"))
    if payload["git"] != {"commit": SOURCE_COMMIT, "dirty": False}:
        raise AssertionError("formal source state mismatch")
    if len(payload["checks"]) != 20 or not all(payload["checks"].values()):
        raise AssertionError("formal R0.40 checks did not all pass")

    restart = payload["restartCertificate"]
    expected_radii = {
        "R0.31": Fraction(restart["r031Radius"]["exact"]),
        "R0.37": Fraction(
            r038_payload["restartCertificate"]["r037Radius"]["exact"]
        ),
        "R0.38": Fraction(
            r039_payload["restartCertificate"]["r038Radius"]["exact"]
        ),
        "R0.39": Fraction(restart["r039Radius"]["exact"]),
        "R0.40": Fraction(restart["targetRadius"]["exact"]),
    }
    radius_records = rows("radius-gain.csv")
    if len(radius_records) != 10:
        raise AssertionError("radius table must contain ten records")
    for record in radius_records:
        power = 1 if record["quantity"] == "common_radius" else 3
        expected = expected_radii[record["version"]] ** power
        if Fraction(record["exact"]) != expected:
            raise AssertionError("radius row mismatch")
        if Fraction(record["normalized_to_r031"]) != (
            expected / expected_radii["R0.31"] ** power
        ):
            raise AssertionError("normalized radius mismatch")

    active_field, _, _, _ = r028.rational_edge_recurrence(80, False, 0.0)
    polynomial = r036.field_to_polynomial(active_field, 80)
    if r037.polynomial_digest(polynomial) != restart["degreeEightyPolynomialSha256"]:
        raise AssertionError("polynomial digest mismatch")
    radius = r040.rational(restart["targetRadius"]["exact"])
    endpoint_records = rows("endpoint-columns.csv")
    if len(endpoint_records) != 162:
        raise AssertionError("endpoint table must contain 162 records")
    grouped: dict[str, list[Fraction]] = {"x=-1": [], "x=2": []}
    for record in endpoint_records:
        input_degree = int(record["input_degree"])
        endpoint = record["endpoint"]
        expected_charge = (
            -input_degree if endpoint == "x=-1" else 2 * input_degree
        )
        if int(record["input_charge"]) != expected_charge:
            raise AssertionError("endpoint charge mismatch")
        expected = r040.exact_transport_column(
            polynomial,
            radius,
            input_degree,
            expected_charge,
        )
        actual = Fraction(record["exact"])
        if actual != Fraction(str(expected)):
            raise AssertionError("endpoint column mismatch")
        grouped[endpoint].append(actual)
    for endpoint, values in grouped.items():
        if any(right >= left for left, right in zip(values, values[1:])):
            raise AssertionError(f"endpoint columns are not strictly decreasing: {endpoint}")
    exact_polynomial_maximum = Fraction(
        payload["transportKernel"]["maximumPolynomialBound"]["exact"]
    )
    if max(grouped["x=-1"][0], grouped["x=2"][0]) != exact_polynomial_maximum:
        raise AssertionError("degree-one endpoint maximum mismatch")

    endpoint_totals = {
        record["label"]: Fraction(record["totalBound"]["exact"])
        for record in payload["transportKernel"]["endpointColumns"]
    }
    expected_gates = {
        "target_active_tail": Fraction(
            restart["activeTailLinearizationBound"]["exact"]
        ),
        "r039_termwise_transport": Fraction(
            restart["r039TermwiseTransportBound"]["exact"]
        ),
        "target_transport_x_minus_1": endpoint_totals["x=-1"],
        "target_transport_x_plus_2": endpoint_totals["x=2"],
        "probe_active_tail": Fraction(
            payload["negativeControl"]["activeTailLinearizationBound"]["exact"]
        ),
        "probe_polynomial_transport": Fraction(
            payload["negativeControl"]["polynomialTransportEndpointBound"]["exact"]
        ),
    }
    gate_records = rows("proof-gates.csv")
    if len(gate_records) != 6:
        raise AssertionError("proof gate table must contain six records")
    for record in gate_records:
        actual = Fraction(record["exact"])
        expected = expected_gates[record["metric"]]
        if actual != expected:
            raise AssertionError("proof gate mismatch")
        expected_status = "passes" if actual < 1 else "fails"
        if record["status"] != expected_status:
            raise AssertionError("proof gate status mismatch")

    finite_records = rows("finite-column-regressions.csv")
    expected_finite = payload["finiteRegression"]["transportColumns"]
    if len(finite_records) != len(expected_finite):
        raise AssertionError("finite regression count mismatch")
    for record, expected in zip(finite_records, expected_finite):
        if int(record["input_degree"]) != expected["inputDegree"]:
            raise AssertionError("finite input degree mismatch")
        if Fraction(record["exact"]) != Fraction(
            expected["maximumWeightedColumnRatio"]["exact"]
        ):
            raise AssertionError("finite regression ratio mismatch")

    progress_records = [
        json.loads(line)
        for line in (PACKAGE / "progress.ndjson").read_text(
            encoding="utf-8"
        ).splitlines()
        if line
    ]
    if len(progress_records) != 12:
        raise AssertionError("unexpected progress record count")
    if progress_records[-1]["stage"] != (
        "completed R0.40 slope-resolved transport certificate"
    ):
        raise AssertionError("progress log lacks successful completion")
    resource_records = rows("resources.csv")
    if len(resource_records) != 221:
        raise AssertionError("unexpected resource sample count")
    if max(float(record["cpuPercent"]) for record in resource_records) != 100.0:
        raise AssertionError("resource peak CPU mismatch")

    print(
        "validated ten radius records, 162 exact endpoint columns, six proof "
        "gates, five finite regressions, all 20 formal flags, and the archived "
        "progress/resource records"
    )


if __name__ == "__main__":
    main()
