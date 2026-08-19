#!/usr/bin/env python3
"""Independently validate the archived R0.53 figure tables."""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CERTIFICATE = ROOT / "research/certificates/r053/edge-product-affine-charge-weight.json"
EXPECTED_CERTIFICATE_SHA256 = "5d6486dfcc6f2c016380a29698ed986213701b9441dd007d95acce4fc0ea67a5"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    assert sha256(CERTIFICATE) == EXPECTED_CERTIFICATE_SHA256
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert len(certificate["checks"]) == 28
    assert all(certificate["checks"].values())

    profile = rows("threshold-profile.csv")
    assert len(profile) == 121
    radii = [Fraction(row["radiusExact"]) for row in profile]
    assert radii[0] == Fraction(382624, 1_000_000)
    assert radii[-1] == Fraction(382630, 1_000_000)
    assert all(right - left == Fraction(1, 20_000_000) for left, right in zip(radii, radii[1:]))
    zero = [Fraction(row["zeroDeficitPpmExact"]) for row in profile]
    active = [Fraction(row["active162DeficitPpmExact"]) for row in profile]
    assert all(left > right for left, right in zip(zero, zero[1:]))
    assert all(left > right for left, right in zip(active, active[1:]))
    assert zero[0] > 0 > zero[-1]
    root_lower = Fraction(certificate["input"]["rootBox"][0]["exact"])
    root_upper = Fraction(certificate["input"]["rootBox"][1]["exact"])
    left_index = max(index for index, radius in enumerate(radii) if radius < root_lower)
    right_index = min(index for index, radius in enumerate(radii) if radius > root_upper)
    assert active[left_index] > 0
    assert active[right_index] > 0
    assert all(abs(float(row["zeroDeficitPpmDecimal"]) / float(value) - 1) < 1e-12 for row, value in zip(profile, zero) if value)

    gains = rows("strict-gains.csv")
    assert [row["label"] for row in gains] == ["fixed restart", "sharp threshold"]
    assert all(Fraction(row["factorExact"]) > 1 for row in gains)
    assert all(Fraction(row["gainPpmExact"]) == (Fraction(row["factorExact"]) - 1) * 1_000_000 for row in gains)
    assert Fraction(gains[1]["gainPpmExact"]) > Fraction(gains[0]["gainPpmExact"])

    competitors = rows("competitor-gaps.csv")
    assert len(competitors) == 281
    assert [int(row["rankByGap"]) for row in competitors] == list(range(1, 282))
    gaps = [Fraction(row["gapExact"]) for row in competitors]
    assert all(gap > 0 for gap in gaps)
    assert all(left <= right for left, right in zip(gaps, gaps[1:]))
    assert competitors[0]["label"] == "s=162,j=81"
    assert competitors[0]["isNearest"] == "true"
    assert sum(row["isLargeChargeTail"] == "true" for row in competitors) == 1
    assert Fraction(competitors[0]["gapExact"]) == Fraction(certificate["competitorDominance"]["minimumGap"]["exact"])

    metadata = json.loads((HERE / "sampling-metadata.json").read_text(encoding="utf-8"))
    assert metadata["certificateSha256"]["r053"] == EXPECTED_CERTIFICATE_SHA256
    assert metadata["profileRows"] == 121
    assert metadata["gainRows"] == 2
    assert metadata["competitorRows"] == 281
    assert metadata["nearestCompetitor"] == "s=162,j=81"
    assert metadata["randomness"] is False
    assert metadata["decimalDecisionUse"] is False
    assert metadata["displaySamplesAreProof"] is False

    with (ROOT / "research/certificates/r053/resources.csv").open(newline="", encoding="utf-8") as source:
        resources = list(csv.DictReader(source))
    assert len(resources) == 72
    assert resources[-1]["status"] == "exited:0"
    progress = [json.loads(line) for line in (ROOT / "research/certificates/r053/progress.ndjson").read_text(encoding="utf-8").splitlines()]
    assert progress[-1]["checks"] == 28

    print("validated R0.53 figure data: 121 exact display samples, 2 strict gains, all 281 formal competitor gaps, and monitored certificate provenance")


if __name__ == "__main__":
    main()
