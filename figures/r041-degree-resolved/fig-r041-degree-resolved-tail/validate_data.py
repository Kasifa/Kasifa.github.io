#!/usr/bin/env python3
"""Validate every R0.41 plotted value against pinned exact certificates."""

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
import edge_degree_resolved_tail_audit as r041


R041 = REPOSITORY / "research/certificates/r041/edge-degree-resolved-tail.json"
R040 = REPOSITORY / "research/certificates/r040/edge-slope-resolved-transport.json"
R039 = REPOSITORY / "research/certificates/r039/edge-charge-resolved.json"
R038 = REPOSITORY / "research/certificates/r038/edge-tail-newton.json"
EXPECTED = {
    R041: "1eb4bbe5f7e53e9eacf7f445b716194ab492603a7de35884549e9c7def640653",
    R040: "cc6257637b42798e9fdf17ef66531bf263072057f38c130320ed108fb116fc3b",
    R039: "59b978c1c5384edb394adc76add0950b3c8e6666f6562dfc199584c22dd0e700",
    R038: "3eb320e8cef0289c7fa2fef00a38c3c66b6b4c5006375bf6386d784f6b95dbf4",
}
SOURCE_COMMIT = "c851762902bb97dd3f3f2510b7321771e0a1ff03"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    for path, expected in EXPECTED.items():
        if sha256(path) != expected:
            raise AssertionError(f"pinned certificate hash mismatch: {path}")
    payload = json.loads(R041.read_text(encoding="utf-8"))
    r040_payload = json.loads(R040.read_text(encoding="utf-8"))
    r039_payload = json.loads(R039.read_text(encoding="utf-8"))
    r038_payload = json.loads(R038.read_text(encoding="utf-8"))
    if payload["git"] != {"commit": SOURCE_COMMIT, "dirty": False}:
        raise AssertionError("formal source state mismatch")
    if len(payload["checks"]) != 30 or not all(payload["checks"].values()):
        raise AssertionError("formal R0.41 checks did not all pass")

    restart = payload["restartCertificate"]
    r040_restart = r040_payload["restartCertificate"]
    expected_radii = {
        "R0.31": Fraction(r040_restart["r031Radius"]["exact"]),
        "R0.37": Fraction(
            r038_payload["restartCertificate"]["r037Radius"]["exact"]
        ),
        "R0.38": Fraction(
            r039_payload["restartCertificate"]["r038Radius"]["exact"]
        ),
        "R0.39": Fraction(r040_restart["r039Radius"]["exact"]),
        "R0.40": Fraction(restart["previousRadius"]["exact"]),
        "R0.41": Fraction(restart["radius"]["exact"]),
    }
    radius_records = rows("radius-gain.csv")
    if len(radius_records) != 12:
        raise AssertionError("radius table must contain twelve records")
    for record in radius_records:
        power = 1 if record["quantity"] == "common_radius" else 3
        expected = expected_radii[record["version"]] ** power
        if Fraction(record["exact"]) != expected:
            raise AssertionError("radius row mismatch")
        if Fraction(record["normalized_to_r031"]) != (
            expected / expected_radii["R0.31"] ** power
        ):
            raise AssertionError("normalized radius mismatch")

    certificate_columns = payload["activeTailKernel"]["finiteColumns"]
    charge_records = rows("charge-columns.csv")
    if len(charge_records) != 243:
        raise AssertionError("charge table must cover 242 finite sectors and one tail")
    for record, expected in zip(charge_records[:-1], certificate_columns):
        if int(record["input_charge"]) != expected["inputCharge"]:
            raise AssertionError("finite charge mismatch")
        if int(record["minimum_tail_degree"]) != expected["minimumTailDegree"]:
            raise AssertionError("minimum tail degree mismatch")
        if Fraction(record["exact"]) != Fraction(expected["bound"]["exact"]):
            raise AssertionError("finite charge bound mismatch")
    large_record = charge_records[-1]
    large_expected = payload["activeTailKernel"]["largeChargeSector"]
    if large_record["sector"] != ">=241":
        raise AssertionError("large-charge sector label mismatch")
    if Fraction(large_record["exact"]) != Fraction(
        large_expected["bound"]["exact"]
    ):
        raise AssertionError("large-charge bound mismatch")
    if max(Fraction(row["exact"]) for row in charge_records) != Fraction(
        payload["activeTailKernel"]["maximumBound"]["exact"]
    ):
        raise AssertionError("active-tail maximum mismatch")

    active_field, _, _, _ = r028.rational_edge_recurrence(80, False, 0.0)
    polynomial = r036.field_to_polynomial(active_field, 80)
    if r037.polynomial_digest(polynomial) != restart["degreeEightyPolynomialSha256"]:
        raise AssertionError("degree-80 polynomial digest mismatch")
    radius = r041.rational(restart["radius"]["exact"])
    degree_records = rows("degree-columns.csv")
    expected_degrees = payload["finiteRegression"]["degreeColumnsAtCharge162"][
        "records"
    ]
    if len(degree_records) != 12:
        raise AssertionError("degree table must contain twelve exact regressions")
    for record, expected in zip(degree_records, expected_degrees):
        degree = int(record["input_degree"])
        if degree != expected["inputDegree"] or int(record["input_charge"]) != 162:
            raise AssertionError("degree-column index mismatch")
        exact = r041.exact_tail_column(polynomial, radius, degree, 162)
        if Fraction(record["exact"]) != Fraction(str(exact)):
            raise AssertionError("independently reconstructed degree column mismatch")
        if Fraction(record["exact"]) != Fraction(expected["exactColumn"]["exact"]):
            raise AssertionError("archived degree column mismatch")
        if Fraction(record["all_order_bound_exact"]) != Fraction(
            expected["allOrderSectorBound"]["exact"]
        ):
            raise AssertionError("degree-column sector bound mismatch")
    values = [Fraction(record["exact"]) for record in degree_records]
    if values.index(min(values)) != 8 or not values[-1] > values[8]:
        raise AssertionError("archived nonmonotone degree signature changed")

    expected_gates = {
        "acceptance_legacy_tail": Fraction(
            payload["legacyComparison"]["legacyAcceptanceTail"]["exact"]
        ),
        "acceptance_resolved_tail": Fraction(
            payload["acceptanceTest"]["tailLinearizationBound"]["exact"]
        ),
        "acceptance_transport": Fraction(
            payload["acceptanceTest"]["transportBound"]["exact"]
        ),
        "target_legacy_tail": Fraction(
            payload["legacyComparison"]["legacyTargetTail"]["exact"]
        ),
        "target_resolved_tail": Fraction(restart["tailLinearizationBound"]["exact"]),
        "target_transport": Fraction(restart["transportBound"]["exact"]),
        "probe_resolved_tail": Fraction(
            payload["negativeControl"]["tailLinearizationBound"]["exact"]
        ),
        "probe_transport": Fraction(
            payload["negativeControl"]["transportBound"]["exact"]
        ),
    }
    gate_records = rows("proof-gates.csv")
    if len(gate_records) != 8:
        raise AssertionError("proof-gate table must contain eight records")
    for record in gate_records:
        actual = Fraction(record["exact"])
        if actual != expected_gates[record["metric"]]:
            raise AssertionError("proof-gate mismatch")
        if record["status"] != ("passes" if actual < 1 else "fails"):
            raise AssertionError("proof-gate status mismatch")

    progress_records = [
        json.loads(line)
        for line in (PACKAGE / "progress.ndjson").read_text(
            encoding="utf-8"
        ).splitlines()
        if line
    ]
    if len(progress_records) != 6:
        raise AssertionError("unexpected progress record count")
    if progress_records[-1]["stage"] != "all exact checks passed":
        raise AssertionError("progress log lacks successful completion")
    resource_records = rows("resources.csv")
    if len(resource_records) != 274:
        raise AssertionError("unexpected resource sample count")
    if max(float(record["cpuPercent"]) for record in resource_records) != 100.0:
        raise AssertionError("resource peak CPU mismatch")
    if max(float(record["rssMiB"]) for record in resource_records) != 53.938:
        raise AssertionError("resource peak RSS mismatch")
    if resource_records[-1]["status"] != "exited:0":
        raise AssertionError("resource log lacks clean exit")

    print(
        "validated 12 radius records, 243 all-order charge sectors, 12 "
        "independently reconstructed degree columns, eight proof gates, all "
        "30 formal flags, and the archived progress/resource records"
    )


if __name__ == "__main__":
    main()
