#!/usr/bin/env python3
"""Validate every R0.46 plotted table against the pinned certificate."""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CERTIFICATE = ROOT / "research/certificates/r046/edge-two-block-weight.json"
EXPECTED_CERTIFICATE_SHA256 = (
    "9310267b894c32b61034ec5e8f34b7d49144028830713a5e86b59d5be00109d1"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def main() -> None:
    assert sha256(CERTIFICATE) == EXPECTED_CERTIFICATE_SHA256
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert len(certificate["checks"]) == 31
    assert all(certificate["checks"].values())
    assert certificate["git"]["commit"].startswith("a521a84")
    assert certificate["git"]["dirty"] is False

    envelope = rows("weight-envelope.csv")
    assert len(envelope) == 606
    assert {row["series"] for row in envelope} == {
        "s=0 endpoint",
        "s=-1 endpoint",
        "s=1 bound",
        "finite s=162",
        "large s>=241",
        "complete envelope",
    }
    certified = [
        row
        for row in envelope
        if row["series"] == "complete envelope"
        and row["isCertifiedWeight"] == "true"
    ]
    assert len(certified) == 1
    assert Fraction(certified[0]["boundExact"]) == Fraction(
        certificate["restartCertificate"]["tailLinearizationBound"]["exact"]
    )

    controls = rows("radius-controls.csv")
    assert len(controls) == 12
    target = next(
        row
        for row in controls
        if row["control"] == "target" and row["series"] == "two-block tail"
    )
    probe = next(
        row
        for row in controls
        if row["control"] == "probe" and row["series"] == "two-block tail"
    )
    assert Fraction(target["boundExact"]) < 1
    assert Fraction(probe["boundExact"]) > 1

    sectors = rows("sector-bounds.csv")
    assert len(sectors) == 5
    assert max(Fraction(row["boundExact"]) for row in sectors) == Fraction(
        certificate["restartCertificate"]["tailLinearizationBound"]["exact"]
    )
    assert all(row["classification"] == "formal all-order sector" for row in sectors)

    gates = rows("proof-gates.csv")
    assert len(gates) == 6
    assert gates[0]["valueExact"] == ""
    assert "display-only" in gates[0]["classification"]
    assert all(
        Fraction(row["valueExact"]) < 1
        for row in gates
        if row["classification"] == "formal gate"
    )

    progress = rows("resources.csv")
    assert len(progress) == 264
    assert max(float(row["cpuPercent"]) for row in progress) == 100.0
    assert max(float(row["rssMiB"]) for row in progress) == 47.047
    assert sum(1 for _ in (HERE / "progress.ndjson").open(encoding="utf-8")) == 9
    print("R0.46 figure data validation passed")


if __name__ == "__main__":
    main()
