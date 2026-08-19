#!/usr/bin/env python3
"""Independently validate the R0.44 figure tables against exact sources."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import sys
import time

import gmpy2


ROOT = Path(__file__).resolve().parents[3]
RESEARCH = ROOT / "research"
if str(RESEARCH) not in sys.path:
    sys.path.insert(0, str(RESEARCH))

import edge_common_slope_tail_audit as r044  # noqa: E402
import edge_charge_resolved_audit as r039  # noqa: E402
import edge_rational_asymptotic_audit as r028  # noqa: E402
import edge_short_continuation_audit as r036  # noqa: E402
import edge_weighted_restart_audit as r037  # noqa: E402


Q = gmpy2.mpq
HERE = Path(__file__).resolve().parent
CERTIFICATE = RESEARCH / "certificates/r044/edge-common-slope-tail.json"
EXPECTED_CERTIFICATE_SHA256 = (
    "7966771f25305211907e11e1a7ab7b6d784b1a14e3db92b3cbec37b96382bb1f"
)
SOURCE_COMMIT = "aade631ea1a492d078f052776b443875d6a3dd73"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def main() -> None:
    assert sha256(CERTIFICATE) == EXPECTED_CERTIFICATE_SHA256
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert certificate["git"]["commit"] == SOURCE_COMMIT
    assert certificate["git"]["dirty"] is False
    assert len(certificate["checks"]) == 34
    assert all(certificate["checks"].values())

    started = time.perf_counter()
    active, _, _, _ = r028.rational_edge_recurrence(80, False, started)
    polynomial = r036.field_to_polynomial(active, 80)
    assert r037.polynomial_digest(polynomial) == certificate[
        "restartCertificate"
    ]["degreeEightyPolynomialSha256"]
    radius = Q(certificate["restartCertificate"]["radius"]["exact"])
    terms = r039.weighted_base_terms(polynomial, radius)

    envelope = rows("common-slope-envelope.csv")
    assert len(envelope) == certificate["finiteRegression"][
        "commonSlopeBreakpoints"
    ]["breakpointCount"] == 1313
    values = []
    for row in envelope:
        slope = Q(row["slopeExact"])
        value = Q(row["boundExact"])
        assert value == r044.common_slope_value(terms, slope, 80, 241)
        assert (row["isEndpoint"] == "true") == (slope in {Q(0), Q(2)})
        values.append((slope, value))
    maximum_slope, maximum_value = max(values, key=lambda item: item[1])
    assert maximum_slope == Q(2)
    assert maximum_value == Q(
        certificate["restartCertificate"]["commonSlopeLargeSector"]["bound"][
            "exact"
        ]
    )
    assert all(value <= maximum_value for _slope, value in values)

    bridge = rows("slope-loss-bridge.csv")
    assert len(bridge) == 5
    legacy = sum((Q(row["legacyExact"]) for row in bridge), Q(0))
    common = sum((Q(row["commonExact"]) for row in bridge), Q(0))
    reduction = sum((Q(row["reductionExact"]) for row in bridge), Q(0))
    assert legacy == Q(certificate["restartCertificate"]["r043LargeSectorAtTarget"]["exact"])
    assert common == maximum_value
    assert legacy - common == reduction

    controls = rows("radius-controls.csv")
    assert len(controls) == 9
    blocks = {
        "entry": certificate["entryControl"],
        "target": certificate["restartCertificate"],
        "failureProbe": certificate["negativeControl"],
    }
    for row in controls:
        block = blocks[row["control"]]
        assert Q(row["radiusExact"]) == Q(block["radius"]["exact"])
        value = Q(row["boundExact"])
        if row["series"] == "common large sector":
            expected = Q(block["commonSlopeLargeSector"]["bound"]["exact"])
        elif row["series"] == "finite s=-1 / complete tail":
            expected = Q(block["tailLinearizationBound"]["exact"])
        else:
            assert row["series"] == "canonical stretch"
            expected = Q(block["stretchOperatorBound"]["exact"])
        assert value == expected
        assert (row["passes"] == "true") == (value < 1)

    gates = rows("proof-gates.csv")
    assert len(gates) == 5
    target = certificate["restartCertificate"]
    ball = Q(target["chosenBallRadius"]["exact"])
    expected_gates = {
        "active tail": Q(target["tailLinearizationBound"]["exact"]),
        "ball mapping / radius": Q(target["mappingUpperBound"]["exact"]) / ball,
        "Lipschitz": Q(target["lipschitzUpperBound"]["exact"]),
        "canonical stretch": Q(target["stretchOperatorBound"]["exact"]),
        "old direct transport": Q(target["directTransportBound"]["exact"]),
    }
    for row in gates:
        value = Q(row["boundExact"])
        assert value == expected_gates[row["gate"]]
        assert (row["passes"] == "true") == (value < 1)
        if row["gate"] == "old direct transport":
            assert row["classification"] == "diagnostic, not a construction gate"
        else:
            assert row["classification"] == "formal gate"

    progress_rows = [
        json.loads(line)
        for line in (HERE / "progress.ndjson").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    resource_rows = rows("resources.csv")
    assert progress_rows[-1]["stage"] == "all exact checks passed"
    assert progress_rows[-1]["checks"] == 34
    assert len(resource_rows) == 300
    assert max(float(row["cpuPercent"]) for row in resource_rows) == 100.0
    assert max(float(row["rssMiB"]) for row in resource_rows) == 47.906
    assert {row["gpuCount"] for row in resource_rows} == {"0"}

    print(
        "validated 1,313 exact common-slope breakpoints, five additive "
        "charge-group reductions, nine radius-control rows, five proof gates, "
        "all 34 formal flags, the reconstructed degree-80 polynomial, and "
        "archived monitoring"
    )


if __name__ == "__main__":
    main()
