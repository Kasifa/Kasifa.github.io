#!/usr/bin/env python3
"""Independently validate the R0.56 figure tables and provenance pins."""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CERTIFICATE = ROOT / "research/certificates/r056/leray-polarization-channels.json"
EXPECTED_CERTIFICATE_SHA256 = (
    "ff0b68729476dfc2d8e53d1483c7a29b383914a5dd8ba761502c57534858fafe"
)
FORMAL_SOURCE_COMMIT = "1b736121127e91727b8ab7ff1b2fd90c2ee873f6"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    assert sha256(CERTIFICATE) == EXPECTED_CERTIFICATE_SHA256
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert len(certificate["checks"]) == 21
    assert all(certificate["checks"].values())
    assert certificate["git"]["sourceCommit"] == FORMAL_SOURCE_COMMIT

    profile = rows("channel-profile.csv")
    assert len(profile) == 801
    epsilon = Fraction(1, 8)
    for index, row in enumerate(profile):
        mu = Fraction(-1) + Fraction(index, 400)
        normal_squared = 1 - mu * mu
        parallel = epsilon - mu
        denominator = normal_squared + parallel * parallel
        planar_squared = (
            Fraction(0)
            if normal_squared == 0
            else normal_squared * parallel * parallel / denominator
        )
        assert Fraction(row["epsilonExact"]) == epsilon
        assert Fraction(row["muExact"]) == mu
        assert Fraction(row["normalGainSquaredExact"]) == normal_squared
        assert Fraction(row["planarGainSquaredExact"]) == planar_squared
        assert Fraction(row["formalPlanarUpperBoundExact"]) == Fraction(9, 16)
        assert row["classification"] == "exact squared-gain presentation row"

    families = rows("channel-families.csv")
    assert len(families) == 512
    for index, row in enumerate(families, start=1):
        assert int(row["N"]) == index
        assert Fraction(row["saturationNormalGainSquaredExact"]) == 1
        assert Fraction(row["saturationPlanarGainSquaredExact"]) == Fraction(
            1, index * index + 1
        )
        assert Fraction(row["halfLimitNormalGainSquaredExact"]) == Fraction(1, 2)
        assert Fraction(row["halfLimitPlanarGainSquaredExact"]) == Fraction(
            (index + 1) ** 2,
            2 * (2 * index * index + 2 * index + 1),
        )
        assert row["classification"] == "exact all-index family presentation row"

    angular = rows("angular-persistence.csv")
    assert len(angular) == 401
    for index, row in enumerate(angular):
        delta = Fraction(index, 400)
        assert Fraction(row["deltaExact"]) == delta
        assert Fraction(row["nearSaturationMeasureSquaredExact"]) == (
            2 * delta - delta * delta
        )
        assert row["classification"] == "exact squared-measure presentation row"

    metadata = json.loads(
        (HERE / "figure-data-metadata.json").read_text(encoding="utf-8")
    )
    assert metadata["certificateSha256"] == EXPECTED_CERTIFICATE_SHA256
    assert len(metadata["figureSourceCommit"]) == 40
    assert metadata["formalSourceCommit"] == FORMAL_SOURCE_COMMIT
    assert metadata["certificateChecks"] == 21
    assert metadata["profileRows"] == 801
    assert metadata["familyRows"] == 512
    assert metadata["angularRows"] == 401
    assert metadata["formalTriadsChecked"] == 1_764_912
    assert metadata["formalFamiliesChecked"] == 400_000
    assert metadata["displayRowsAreProof"] is False
    assert metadata["randomness"] is False
    assert metadata["floatingPointDecisionUse"] is False

    progress = [
        json.loads(line)
        for line in (HERE / "progress.ndjson").read_text(encoding="utf-8").splitlines()
    ]
    assert len(progress) == 3
    assert progress[-1]["checks"] == 21
    with (HERE / "resources.csv").open(newline="", encoding="utf-8") as source:
        resources = list(csv.DictReader(source))
    assert len(resources) == 55
    assert resources[-1]["status"] == "exited:0"

    print(
        "validated R0.56 figure data: 801 exact channel-profile rows, "
        "512 exact family rows, 401 angular rows, and monitored provenance"
    )


if __name__ == "__main__":
    main()
