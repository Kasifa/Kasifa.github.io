#!/usr/bin/env python3
"""Independently validate the R0.52 journal-figure tables."""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys


sys.set_int_max_str_digits(0)


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[2]
CERTIFICATE = ROOT / "research/certificates/r052/edge-affine-family-global.json"
EXPECTED_CERTIFICATE_SHA256 = (
    "b79e59ec327bc02b64e23ad3f903b6d61860a075d59ff75a43d82f5684590def"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def rational_digest(value: Fraction) -> str:
    rendered = (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )
    return hashlib.sha256(rendered.encode("ascii")).hexdigest()


def main() -> None:
    assert sha256(CERTIFICATE) == EXPECTED_CERTIFICATE_SHA256
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert len(certificate["checks"]) == 22
    assert all(certificate["checks"].values())

    profile = rows("feasibility-profile.csv")
    assert len(profile) == 80
    for side in ("left", "right"):
        selected = [row for row in profile if row["side"] == side]
        assert [int(row["distanceExponent"]) for row in selected] == list(
            range(1, 41)
        )
        distances = [Fraction(row["distanceExact"]) for row in selected]
        assert distances == [Fraction(1, 10**exponent) for exponent in range(1, 41)]
    for row in profile:
        value = Fraction(row["negativeClearedFeasibilityExact"])
        assert value > 0
        assert rational_digest(value) == row["valueSha256"]
        displayed = float(row["negativeClearedFeasibilityDecimal"])
        assert abs(displayed / float(value) - 1) < 1e-12

    contraction = rows("krawczyk-contraction.csv")
    assert [row["variable"] for row in contraction] == ["r", "c", "alpha"]
    assert all(Fraction(row["boxWidthExact"]) == Fraction(1, 10**40) for row in contraction)
    assert all(float(row["krawczykImageRadiusDecimal"]) > 0 for row in contraction)
    assert all(
        float(row["krawczykImageRadiusDecimal"]) < float(row["boxWidthDecimal"])
        for row in contraction
    )

    competitors = rows("inactive-gaps.csv")
    assert len(competitors) == 242
    assert [int(row["rankByGap"]) for row in competitors] == list(range(1, 243))
    gaps = [float(row["gapDecimal"]) for row in competitors]
    assert all(gap > 0 for gap in gaps)
    assert all(left <= right for left, right in zip(gaps, gaps[1:]))
    assert competitors[0]["label"] == "s=164,j=82"
    assert competitors[0]["isNearest"] == "true"
    assert competitors[0]["gapDecimal"] == certificate["inactiveSectorTheorem"][
        "minimumGapBelowOne"
    ]["decimal"]
    assert all(row["isNearest"] == "false" for row in competitors[1:])

    metadata = json.loads(
        (PACKAGE / "sampling-metadata.json").read_text(encoding="utf-8")
    )
    assert metadata["certificateSha256"] == EXPECTED_CERTIFICATE_SHA256
    assert metadata["profileRows"] == 80
    assert metadata["contractionRows"] == 3
    assert metadata["inactiveRows"] == 242
    assert metadata["descartesSignVariations"] == 3
    assert metadata["positiveDerivativeRootsExactly"] == 3
    assert metadata["randomness"] is False

    formal_progress = [
        json.loads(line)
        for line in (
            ROOT / "research/certificates/r052/progress.ndjson"
        ).read_text(encoding="utf-8").splitlines()
    ]
    assert formal_progress[-1]["checks"] == 22
    formal_resources = rows_from_path(
        ROOT / "research/certificates/r052/resources.csv"
    )
    assert len(formal_resources) == 121
    assert formal_resources[-1]["status"] == "exited:0"

    print(
        "validated R0.52 figure data: 80 exact feasibility samples, 3 "
        "Krawczyk contractions, 242 inactive gaps, and monitored formal provenance"
    )


def rows_from_path(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


if __name__ == "__main__":
    main()
