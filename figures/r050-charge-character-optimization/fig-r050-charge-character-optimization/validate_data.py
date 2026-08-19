#!/usr/bin/env python3
"""Independently validate the R0.50 journal-figure tables."""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[2]
CERTIFICATE = (
    ROOT
    / "research/certificates/r050/edge-charge-character-optimization.json"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "fc173a2108ef881d21d9d54046085f0d5daf5cc33ed50e024ca32ec867f7b79a"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    assert sha256(CERTIFICATE) == EXPECTED_CERTIFICATE_SHA256
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert len(certificate["checks"]) == 33
    assert all(certificate["checks"].values())

    global_profile = rows("global-threshold-profile.csv")
    assert len(global_profile) == 191
    global_characters = [Fraction(row["characterExact"]) for row in global_profile]
    assert global_characters[0] == Fraction(9, 20)
    assert global_characters[-1] == Fraction(7, 5)
    assert all(
        left < right
        for left, right in zip(global_characters, global_characters[1:])
    )
    assert Fraction(4, 5) in global_characters
    assert max(
        float(row["absoluteResidualDecimal"]) for row in global_profile
    ) < 1e-78

    local_profile = rows("local-threshold-profile.csv")
    assert len(local_profile) == 151
    local_characters = [Fraction(row["characterExact"]) for row in local_profile]
    assert local_characters[0] == Fraction(159, 200)
    assert local_characters[-1] == Fraction(81, 100)
    assert Fraction(4, 5) in local_characters
    assert max(
        float(row["absoluteResidualDecimal"]) for row in local_profile
    ) < 1e-78
    reference = next(
        row for row in local_profile if Fraction(row["characterExact"]) == Fraction(4, 5)
    )
    assert abs(float(reference["gainRelativeToFourFifthsPpmDecimal"])) < 1e-70
    local_maximum = max(
        local_profile,
        key=lambda row: float(row["thresholdRadiusDecimal"]),
    )
    assert Fraction(local_maximum["characterExact"]) == Fraction(1605, 2000)

    theorem = certificate["globalOptimizationTheorem"]
    radius_lower = Fraction(theorem["optimalRadiusLower"]["exact"])
    radius_upper = Fraction(theorem["optimalRadiusUpper"]["exact"])
    character_lower = Fraction(theorem["optimalCharacterLower"]["exact"])
    character_upper = Fraction(theorem["optimalCharacterUpper"]["exact"])
    assert radius_upper - radius_lower == Fraction(1, 10**15)
    assert character_upper - character_lower == Fraction(1, 10**10)
    assert radius_lower > Fraction(
        certificate["comparisonWithR049"]["r049RootUpper"]["exact"]
    )

    box = rows("optimization-box.csv")
    assert len(box) == 4
    assert {row["key"] for row in box} == {
        "radiusLower",
        "radiusUpper",
        "characterLower",
        "characterUpper",
    }
    assert all(
        Fraction(row["minimumSignedBernsteinCoefficientExact"]) > 0
        for row in box
    )

    competitors = rows("competitor-gaps.csv")
    assert len(competitors) == 243
    assert [int(row["rankByGap"]) for row in competitors] == list(range(1, 244))
    gaps = [Fraction(row["gapExact"]) for row in competitors]
    assert all(gap > 0 for gap in gaps)
    assert all(left <= right for left, right in zip(gaps, gaps[1:]))
    assert competitors[0]["label"] == "fixed s=164"
    assert competitors[0]["isNearest"] == "true"
    assert gaps[0] == Fraction(
        certificate["rectangleDominance"]["minimumDominanceGap"]["exact"]
    )

    metadata = json.loads(
        (PACKAGE / "sampling-metadata.json").read_text(encoding="utf-8")
    )
    assert metadata["precisionDecimalDigits"] == 90
    assert metadata["globalSamples"] == 191
    assert metadata["localSamples"] == 151
    assert metadata["randomness"] is False

    progress_records = [
        json.loads(line)
        for line in (PACKAGE / "progress.ndjson")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    assert progress_records[-1]["checks"] == 33
    assert progress_records[-1]["competitors"] == 243
    resources = rows("resources.csv")
    assert len(resources) == 70
    assert resources[-1]["status"] == "exited:0"

    print(
        "validated R0.50 figure data: 191 global and 151 local 90-digit "
        "presentation samples, 4 exact face certificates, 243 exact competitor "
        "gaps, and monitored formal provenance"
    )


if __name__ == "__main__":
    main()
