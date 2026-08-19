#!/usr/bin/env python3
"""Independently validate the R0.45 figure tables against the certificate."""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CERTIFICATE = ROOT / "research/certificates/r045/edge-fixed-negative-charge.json"
EXPECTED_CERTIFICATE_SHA256 = (
    "abc588fb80a140cf78f0558119f50e7a15dce9b2d3fa5219a8b0f9456c8d0b7b"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    if sha256(CERTIFICATE) != EXPECTED_CERTIFICATE_SHA256:
        raise SystemExit("certificate hash mismatch")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if sum(certificate["checks"].values()) != 33:
        raise SystemExit("expected 33 passing checks")
    if certificate["git"] != {
        "commit": "8f7f9ec2b90b2d249b474ec4dbba50a71c807745",
        "dirty": False,
    }:
        raise SystemExit("source pin mismatch")

    curve = rows("negative-charge-curve.csv")
    if len(curve) != 202:
        raise SystemExit("curve sample count mismatch")
    for label, block in (
        ("target 0.371", certificate["restartCertificate"]),
        ("probe 0.372", certificate["negativeControl"]),
    ):
        selected = [row for row in curve if row["radiusLabel"] == label]
        if any(row["classification"] != "presentation sample; not used in proof" for row in selected):
            raise SystemExit("curve classification mismatch")
        values = [Fraction(row["columnExact"]) for row in selected]
        if values != sorted(values):
            raise SystemExit("sampled column is not increasing in t")
        endpoint = Fraction(block["exactNegativeChargeColumn"]["bound"]["exact"])
        if values[-1] != endpoint:
            raise SystemExit("curve endpoint mismatch")

    derivative = rows("derivative-certificate.csv")
    target_derivative = {
        row["component"]: Fraction(row["valueExact"])
        for row in derivative
        if row["control"] == "target 0.371"
    }
    if target_derivative["q=2 seed"] - target_derivative["q=1 obstruction"] != target_derivative["certified margin"]:
        raise SystemExit("derivative bridge mismatch")
    if target_derivative["certified margin"] <= 0:
        raise SystemExit("derivative margin is not positive")

    controls = rows("radius-controls.csv")
    if len(controls) != 10:
        raise SystemExit("radius-control count mismatch")
    exact = [row for row in controls if row["series"] == "exact s=-1"]
    if [Fraction(row["boundExact"]) < 1 for row in exact] != [True, True, False]:
        raise SystemExit("exact radius controls do not bracket the threshold")
    old = next(row for row in controls if row["series"] == "R0.44 inherited s=-1")
    if Fraction(old["boundExact"]) <= 1:
        raise SystemExit("R0.44 inherited target control should fail")

    gates = rows("proof-gates.csv")
    formal = [row for row in gates if row["classification"] == "formal gate"]
    if len(formal) != 4 or not all(Fraction(row["boundExact"]) < 1 for row in formal):
        raise SystemExit("formal target gate mismatch")
    if len(rows("resources.csv")) != 240:
        raise SystemExit("resource sample count mismatch")
    progress = [json.loads(line) for line in (HERE / "progress.ndjson").read_text(encoding="utf-8").splitlines()]
    if len(progress) != 8 or progress[-1]["stage"] != "all exact checks passed":
        raise SystemExit("progress log mismatch")
    print("R0.45 figure data validation passed")


if __name__ == "__main__":
    main()
