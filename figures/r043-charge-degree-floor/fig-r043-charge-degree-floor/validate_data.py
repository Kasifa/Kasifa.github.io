#!/usr/bin/env python3
"""Validate R0.43 figure data against pinned exact sources."""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "research"))

import gmpy2

import edge_charge_degree_floor_audit as r043
import edge_rational_asymptotic_audit as r028
import edge_short_continuation_audit as r036


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
CERTIFICATE = REPOSITORY / "research/certificates/r043/edge-charge-degree-floor.json"
EXPECTED_CERTIFICATE_SHA256 = (
    "0ebaaf6c5a9f731e5b2846f3042553bebd6748b298ce31919e8f423e41369bf8"
)
EXPECTED_SOURCE_COMMIT = "4fe8cb308e20921fb0490aa2e76209b1d2d84221"
Rational = gmpy2.mpq


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    actual_hash = hashlib.sha256(CERTIFICATE.read_bytes()).hexdigest()
    if actual_hash != EXPECTED_CERTIFICATE_SHA256:
        raise AssertionError("R0.43 certificate hash mismatch")
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if payload["git"] != {"commit": EXPECTED_SOURCE_COMMIT, "dirty": False}:
        raise AssertionError("R0.43 source provenance mismatch")
    if len(payload["checks"]) != 22 or not all(payload["checks"].values()):
        raise AssertionError("R0.43 formal checks are incomplete")

    support = rows("support-geometry.csv")
    bridge = rows("large-sector-bridge.csv")
    gates = rows("proof-gates.csv")
    boundary = rows("boundary-bracket.csv")
    finite = rows("finite-large-columns.csv")
    if len(support) != 21 or len(bridge) != 7:
        raise AssertionError("unexpected support or bridge row count")
    if len(gates) != 6 or len(boundary) != 4 or len(finite) != 21:
        raise AssertionError("unexpected gate, boundary, or regression row count")

    for row in support:
        charge = int(row["input_charge"])
        cone_floor = int(row["cone_degree_floor"])
        lattice = int(row["minimum_bivariate_degree"])
        if cone_floor != (charge + 1) // 2:
            raise AssertionError("support cone floor mismatch")
        if lattice < cone_floor or lattice <= 80 or (lattice + charge) % 3:
            raise AssertionError("bivariate lattice minimum is inadmissible")
        if lattice > 81 and (lattice - 1 + charge) % 3 == 0:
            raise AssertionError("bivariate lattice minimum is not minimal")

    bridge_values = [Fraction(row["exact"]) for row in bridge]
    if bridge_values[0] + sum(bridge_values[1:-1]) != bridge_values[-1]:
        raise AssertionError("large-sector additive bridge does not close")
    target = payload["restartCertificate"]
    large = target["largeChargeTailSector"]
    if bridge_values[0] != Fraction(large["legacyBound"]["exact"]):
        raise AssertionError("legacy bridge endpoint mismatch")
    if bridge_values[-1] != Fraction(large["bound"]["exact"]):
        raise AssertionError("improved bridge endpoint mismatch")

    active, _, _, _ = r028.rational_edge_recurrence(80, False, 0.0)
    polynomial = r036.field_to_polynomial(active, 80)
    if r036.polynomial_digest(polynomial) != target["degreeEightyPolynomialSha256"]:
        raise AssertionError("independent polynomial digest mismatch")
    recomputed = r043.charge_degree_floor_tail_bound(
        polynomial,
        Rational(target["radius"]["exact"]),
        80,
        241,
    )
    if Rational(recomputed["maximumBound"]["exact"]) != Rational(
        target["tailLinearizationBound"]["exact"]
    ):
        raise AssertionError("independent improved tail reconstruction mismatch")

    archived_regression = payload["finiteRegression"]["largeChargeColumns"]["records"]
    for row, archived in zip(finite, archived_regression):
        if Fraction(row["exact"]) != Fraction(archived["exactColumn"]["exact"]):
            raise AssertionError("finite exact column extraction mismatch")
        if row["below_sector_bound"] != "True":
            raise AssertionError("finite exact column exceeded the theorem")

    target_gate = {
        row["gate"]: Fraction(row["exact"])
        for row in gates
        if row["stage"] == "target"
    }
    if target_gate["active tail"] != Fraction(target["tailLinearizationBound"]["exact"]):
        raise AssertionError("target active-tail gate mismatch")
    if not target_gate["active tail"] < 1 < target_gate["direct transport"]:
        raise AssertionError("target gate classification mismatch")
    if not target_gate["canonical stretch"] < 1:
        raise AssertionError("target stretch gate mismatch")

    progress_rows = [
        json.loads(line)
        for line in (PACKAGE / "progress.ndjson").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    resources = rows("resources.csv")
    if progress_rows[-1]["stage"] != "all exact checks passed":
        raise AssertionError("progress log lacks successful completion")
    if resources[-1]["status"] != "exited:0" or len(resources) != 255:
        raise AssertionError("resource log does not match the successful run")

    print(
        "validated 21 support rows, seven additive bridge rows, six proof "
        "gates, four boundary points, 21 finite columns, all 22 formal flags, "
        "an independent exact tail reconstruction, and archived monitoring"
    )


if __name__ == "__main__":
    main()
