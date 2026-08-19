#!/usr/bin/env python3
"""Independently validate the R0.51 journal-figure tables."""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[2]
CERTIFICATE = ROOT / "research/certificates/r051/edge-affine-charge-weight.json"
EXPECTED_CERTIFICATE_SHA256 = (
    "db72d40ee304d1a6ce5dd96d9f5971e78037675e79c837e409c5691bb8aa582f"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    assert sha256(CERTIFICATE) == EXPECTED_CERTIFICATE_SHA256
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert len(certificate["checks"]) == 26
    assert all(certificate["checks"].values())

    switch = rows("constraint-switch.csv")
    assert len(switch) == 126
    lambdas = [Fraction(row["lambdaExact"]) for row in switch]
    assert lambdas[0] == Fraction(7652, 10000)
    assert lambdas[-1] == Fraction(15309, 20000)
    assert all(
        right - left == Fraction(1, 500000)
        for left, right in zip(lambdas, lambdas[1:])
    )
    gaps = [float(row["activeMinusZeroPpmDecimal"]) for row in switch]
    assert all(left > right for left, right in zip(gaps, gaps[1:]))
    assert sum(left * right < 0 for left, right in zip(gaps, gaps[1:])) == 1
    selected = [row for row in switch if row["isCertifiedChoice"] == "true"]
    assert len(selected) == 1
    assert Fraction(selected[0]["lambdaExact"]) == Fraction(7653, 10000)
    certified_gap = Fraction(
        certificate["competitorDominance"]["minimumDominanceGap"]["exact"]
    )
    assert abs(
        float(selected[0]["activeMinusZeroPpmDecimal"])
        - float(certified_gap * 1_000_000)
    ) < 1e-20

    gains = rows("incremental-gains.csv")
    assert len(gains) == 3
    assert [int(row["order"]) for row in gains] == [1, 2, 3]
    assert all(Fraction(row["strictGainFactorExact"]) > 1 for row in gains)
    assert gains[-1]["label"] == "R0.51 / R0.50"
    assert Fraction(gains[-1]["strictGainFactorExact"]) == Fraction(
        certificate["comparisonWithR050"]["r051RadiusGainLowerFactor"]["exact"]
    )

    competitors = rows("competitor-gaps.csv")
    assert len(competitors) == 243
    assert [int(row["rankByGap"]) for row in competitors] == list(range(1, 244))
    competitor_gaps = [Fraction(row["gapExact"]) for row in competitors]
    assert all(gap > 0 for gap in competitor_gaps)
    assert all(
        left <= right
        for left, right in zip(competitor_gaps, competitor_gaps[1:])
    )
    assert competitors[0]["label"] == "s=0"
    assert competitors[1]["label"] == "s=164,j=82"
    assert competitors[0]["isNearest"] == "true"
    assert competitor_gaps[0] == certified_gap

    metadata = json.loads(
        (PACKAGE / "sampling-metadata.json").read_text(encoding="utf-8")
    )
    assert metadata["switchSamples"] == 126
    assert metadata["switchSignChanges"] == 1
    assert metadata["gainRows"] == 3
    assert metadata["competitors"] == 243
    assert metadata["randomness"] is False

    progress_records = [
        json.loads(line)
        for line in (PACKAGE / "progress.ndjson")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    assert progress_records[-1]["checks"] == 26
    assert progress_records[-1]["competitors"] == 243
    resources = rows("resources.csv")
    assert len(resources) == 64
    assert resources[-1]["status"] == "exited:0"

    print(
        "validated R0.51 figure data: 126 exact switch samples, 3 exact "
        "incremental gains, 243 exact competitor gaps, and monitored formal "
        "provenance"
    )


if __name__ == "__main__":
    main()
