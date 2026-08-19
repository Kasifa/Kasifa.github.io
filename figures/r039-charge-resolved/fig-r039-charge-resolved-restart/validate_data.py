#!/usr/bin/env python3
"""Validate every plotted R0.39 value against the pinned exact certificates."""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
CERTIFICATE = REPOSITORY / "research/certificates/r039/edge-charge-resolved.json"
R038_CERTIFICATE = REPOSITORY / "research/certificates/r038/edge-tail-newton.json"
EXPECTED_CERTIFICATE_SHA256 = (
    "59b978c1c5384edb394adc76add0950b3c8e6666f6562dfc199584c22dd0e700"
)
EXPECTED_R038_SHA256 = (
    "3eb320e8cef0289c7fa2fef00a38c3c66b6b4c5006375bf6386d784f6b95dbf4"
)
EXPECTED_SOURCE_COMMIT = "ed08ad45b3440a679d8132d7b3464dc21dd07fa5"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    if sha256(CERTIFICATE) != EXPECTED_CERTIFICATE_SHA256:
        raise AssertionError("R0.39 certificate hash mismatch")
    if sha256(R038_CERTIFICATE) != EXPECTED_R038_SHA256:
        raise AssertionError("R0.38 certificate hash mismatch")
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    r038 = json.loads(R038_CERTIFICATE.read_text(encoding="utf-8"))
    if payload["git"] != {"commit": EXPECTED_SOURCE_COMMIT, "dirty": False}:
        raise AssertionError("R0.39 source provenance mismatch")
    if len(payload["checks"]) != 18 or not all(payload["checks"].values()):
        raise AssertionError("not all formal R0.39 checks passed")

    restart = payload["restartCertificate"]
    expected_radii = {
        "R0.31": Fraction(restart["r031Radius"]["exact"]),
        "R0.37": Fraction(r038["restartCertificate"]["r037Radius"]["exact"]),
        "R0.38": Fraction(restart["r038Radius"]["exact"]),
        "R0.39": Fraction(restart["targetRadius"]["exact"]),
    }
    radius_rows = rows("radius-gain.csv")
    if len(radius_rows) != 8:
        raise AssertionError("radius table must contain eight rows")
    for row in radius_rows:
        power = 1 if row["quantity"] == "common_radius" else 3
        value = expected_radii[row["version"]] ** power
        baseline = expected_radii["R0.31"] ** power
        if Fraction(row["exact"]) != value:
            raise AssertionError("radius value mismatch")
        if Fraction(row["normalized_to_r031"]) != value / baseline:
            raise AssertionError("normalized radius mismatch")

    kernel = payload["chargeResolvedKernel"]
    charge_rows = rows("charge-columns.csv")
    if len(charge_rows) != kernel["finiteColumnCount"] or len(charge_rows) != 242:
        raise AssertionError("charge-column count mismatch")
    expected_columns = {
        record["inputCharge"]: record for record in kernel["finiteColumns"]
    }
    maximum_count = 0
    for row in charge_rows:
        input_charge = int(row["input_charge"])
        record = expected_columns[input_charge]
        if int(row["minimum_tail_degree"]) != record["minimumTailDegree"]:
            raise AssertionError("minimum tail degree mismatch")
        if Fraction(row["exact"]) != Fraction(record["bound"]["exact"]):
            raise AssertionError("charge-column bound mismatch")
        is_maximum = row["is_maximum"] == "True"
        if is_maximum != (str(input_charge) == kernel["maximumSector"]):
            raise AssertionError("maximum charge-sector marker mismatch")
        maximum_count += int(is_maximum)
    if maximum_count != 1:
        raise AssertionError("charge table must contain one marked maximum")

    large_rows = rows("large-charge-sector.csv")
    if len(large_rows) != 1:
        raise AssertionError("large-charge table must contain one row")
    if int(large_rows[0]["minimum_input_charge"]) != restart["chargeCutoff"]:
        raise AssertionError("large-charge cutoff mismatch")
    if Fraction(large_rows[0]["exact"]) != Fraction(
        kernel["largeChargeSector"]["bound"]["exact"]
    ):
        raise AssertionError("large-charge bound mismatch")

    mapping_ratio = Fraction(restart["mappingUpperBound"]["exact"]) / Fraction(
        restart["chosenBallRadius"]["exact"]
    )
    expected_gates = {
        "old_tail_bound": Fraction(
            restart["oldR038TailLinearizationBound"]["exact"]
        ),
        "charge_resolved_tail": Fraction(
            restart["chargeResolvedTailLinearizationBound"]["exact"]
        ),
        "ball_mapping_ratio": mapping_ratio,
        "old_transport_bound": Fraction(restart["oldScalarTransportBound"]["exact"]),
        "refined_transport_bound": Fraction(
            restart["transportOperatorNormUpperBound"]["exact"]
        ),
        "probe_transport_bound": Fraction(
            payload["negativeControl"]["transportOperatorBound"]["exact"]
        ),
    }
    gate_rows = rows("proof-gates.csv")
    if set(row["metric"] for row in gate_rows) != set(expected_gates):
        raise AssertionError("proof-gate names mismatch")
    for row in gate_rows:
        value = Fraction(row["exact"])
        if value != expected_gates[row["metric"]]:
            raise AssertionError("proof-gate value mismatch")
        if Fraction(row["threshold"]) != 1:
            raise AssertionError("proof-gate threshold mismatch")
        expected_status = "passes" if value < 1 else "fails"
        if row["status"] != expected_status:
            raise AssertionError("proof-gate status mismatch")

    finite_rows = rows("finite-column-regressions.csv")
    expected_finite = {
        record["inputDegree"]: record
        for record in payload["finiteRegression"]["tailColumns"]
    }
    if set(int(row["input_degree"]) for row in finite_rows) != set(expected_finite):
        raise AssertionError("finite regression degrees mismatch")
    all_order_bound = Fraction(
        restart["chargeResolvedTailLinearizationBound"]["exact"]
    )
    for row in finite_rows:
        record = expected_finite[int(row["input_degree"])]
        value = Fraction(row["exact"])
        if value != Fraction(record["maximumWeightedColumnRatio"]["exact"]):
            raise AssertionError("finite column value mismatch")
        if int(row["maximum_column_charge"]) != record["maximumColumnCharge"]:
            raise AssertionError("finite column charge mismatch")
        if int(row["admissible_columns"]) != record["admissibleColumns"]:
            raise AssertionError("finite column count mismatch")
        if value > all_order_bound:
            raise AssertionError("finite column exceeds the all-order bound")

    progress_records = [
        json.loads(line)
        for line in (PACKAGE / "progress.ndjson").read_text(encoding="utf-8").splitlines()
        if line
    ]
    if len(progress_records) != 10:
        raise AssertionError("progress record count mismatch")
    if progress_records[-1]["stage"] != "completed R0.39 charge-resolved certificate":
        raise AssertionError("progress log has no successful completion record")
    if progress_records[-1].get("passed") is not True:
        raise AssertionError("progress log did not record a passed run")

    resource_rows = rows("resources.csv")
    if len(resource_rows) != 228:
        raise AssertionError("resource sample count mismatch")
    if resource_rows[-1]["status"] != "exited:0":
        raise AssertionError("resource monitor did not record a clean exit")
    if max(float(row["cpuPercent"]) for row in resource_rows) != 100.0:
        raise AssertionError("unexpected peak CPU record")
    if max(float(row["rssMiB"]) for row in resource_rows) != 41.656:
        raise AssertionError("unexpected peak RSS record")

    print(
        "validated four radius stages, 242 finite charge columns, one analytic "
        "large-charge sector, six proof gates, four finite regressions, all 18 "
        "formal flags, and the archived progress/resource records"
    )


if __name__ == "__main__":
    main()
