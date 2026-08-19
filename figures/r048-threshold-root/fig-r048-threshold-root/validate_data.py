#!/usr/bin/env python3
"""Independently validate the R0.48 figure tables against exact sources."""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[2]
CERTIFICATE = ROOT / "research/certificates/r048/edge-charge-threshold-root.json"
EXPECTED_CERTIFICATE_SHA256 = (
    "246bcfa6623b1050511554312c32e9973b42b620a20ff571a1b5f340041c9af0"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    assert sha256(CERTIFICATE) == EXPECTED_CERTIFICATE_SHA256
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert len(certificate["checks"]) == 22
    assert all(certificate["checks"].values())
    theorem = certificate["thresholdTheorem"]

    curve = rows("threshold-curve.csv")
    assert len(curve) == 101
    assert [int(row["sampleIndex"]) for row in curve] == list(range(101))
    assert Fraction(curve[0]["radiusExact"]) == Fraction(
        theorem["window"]["lower"]["exact"]
    )
    assert Fraction(curve[-1]["radiusExact"]) == Fraction(
        theorem["window"]["upper"]["exact"]
    )
    assert Fraction(curve[0]["activeMarginExact"]) == Fraction(
        theorem["activeColumn"]["valueAtWindowLower"]["exact"]
    ) - 1
    assert Fraction(curve[-1]["activeMarginExact"]) == Fraction(
        theorem["activeColumn"]["valueAtWindowUpper"]["exact"]
    ) - 1
    margins = [Fraction(row["activeMarginExact"]) for row in curve]
    assert all(left < right for left, right in zip(margins, margins[1:]))
    assert margins[0] < 0 < margins[-1]

    root = rows("root-endpoints.csv")
    assert len(root) == 2
    assert [row["side"] for row in root] == ["lower", "upper"]
    assert Fraction(root[0]["polynomialValueExact"]) < 0
    assert Fraction(root[1]["polynomialValueExact"]) > 0
    assert Fraction(root[1]["radiusExact"]) - Fraction(root[0]["radiusExact"]) == Fraction(
        1, 10**18
    )
    assert [int(row["sturmVariations"]) for row in root] == [40, 39]
    assert [int(row["zeroSturmValues"]) for row in root] == [0, 0]
    assert theorem["sturmCertificate"]["sequenceLength"] == 81
    assert theorem["sturmCertificate"]["rootCount"] == 1

    competitors = rows("competitor-gaps.csv")
    assert len(competitors) == 243
    assert [int(row["rankByGap"]) for row in competitors] == list(range(1, 244))
    gaps = [Fraction(row["gapBelowActiveAtWindowLeftExact"]) for row in competitors]
    assert all(gap > 0 for gap in gaps)
    assert all(left <= right for left, right in zip(gaps, gaps[1:]))
    assert competitors[0]["label"] == "fixed s=164"
    assert competitors[0]["isNearest"] == "true"
    assert Fraction(competitors[0]["gapBelowActiveAtWindowLeftExact"]) == Fraction(
        theorem["fullWindowDominance"]["minimumDominanceGap"]["exact"]
    )

    leaders = rows("sandwich-leaders.csv")
    assert len(leaders) == 8
    assert leaders[0]["isActive"] == "true"
    assert Fraction(leaders[0]["boundExact"]) == Fraction(
        theorem["activeColumn"]["valueAtWindowLower"]["exact"]
    )
    for leader, competitor in zip(leaders[1:], competitors[:7], strict=True):
        assert leader["isActive"] == "false"
        assert Fraction(leader["boundExact"]) == Fraction(
            competitor["upperBoundAtWindowRightExact"]
        )

    progress = (PACKAGE / "progress.ndjson").read_text(encoding="utf-8").splitlines()
    assert len(progress) == 7
    assert json.loads(progress[-1])["checks"] == 22
    resources = rows("resources.csv")
    assert len(resources) == 144
    assert resources[-1]["status"] == "exited:0"

    print(
        "validated R0.48 figure data: 101 exact polynomial samples, "
        "2 exact root endpoints, 81-term Sturm certificate, 243 formal "
        "competitors, 8 sandwich leaders, and monitored provenance"
    )


if __name__ == "__main__":
    main()
