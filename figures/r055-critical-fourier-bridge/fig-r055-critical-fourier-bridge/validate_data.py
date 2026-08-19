#!/usr/bin/env python3
"""Independently validate the R0.55 figure tables and provenance pins."""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CERTIFICATE = ROOT / "research/certificates/r055/fourier-critical-charge-bridge.json"
EXPECTED_CERTIFICATE_SHA256 = (
    "feacd0c47aa123d508f4889bfb1e6770c40da1fef6e438acc1aa9ecd99fc19ae"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    assert sha256(CERTIFICATE) == EXPECTED_CERTIFICATE_SHA256
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert len(certificate["checks"]) == 17
    assert all(certificate["checks"].values())

    scaling = rows("critical-scaling.csv")
    assert len(scaling) == 81
    for index, row in enumerate(scaling):
        sigma = Fraction(-2) + Fraction(index, 20)
        assert Fraction(row["sigmaExact"]) == sigma
        assert Fraction(row["spatialScalingExponentExact"]) == sigma + 1
        assert row["classification"] == "exact change-of-variables presentation sample"
    assert next(
        row for row in scaling if Fraction(row["sigmaExact"]) == -1
    )["spatialScalingExponentExact"] == "0"

    triads = rows("triad-saturation.csv")
    assert len(triads) == 256
    for index, row in enumerate(triads, start=1):
        assert int(row["N"]) == index
        assert int(row["leftFrequencySquaredExact"]) == index * index
        assert int(row["rightFrequencySquaredExact"]) == index * index + 1
        assert row["outputFrequencySquaredExact"] == "1"
        assert row["criticalSymbolRatioExact"] == "1"
        assert int(row["minimumInputOutputSeparationExact"]) == index
        assert row["classification"] == "formal all-index identity presentation row"

    bridge = rows("bridge-decisions.csv")
    assert len(bridge) == 3
    assert [row["status"] for row in bridge] == [
        "finite",
        "impossible under both axioms",
        "open",
    ]
    assert bridge[0]["classification"] == "formal all-frequency upper bound"
    assert bridge[1]["classification"] == "formal algebraic no-go theorem"
    assert bridge[2]["classification"] == "next research alternative; no theorem claimed"

    metadata = json.loads(
        (HERE / "figure-data-metadata.json").read_text(encoding="utf-8")
    )
    assert metadata["certificateSha256"] == EXPECTED_CERTIFICATE_SHA256
    assert len(metadata["figureSourceCommit"]) == 40
    assert metadata["formalSourceCommit"] == "640cf4ce9b97c2caa8d22f9159b4d0aa2e3a65a0"
    assert metadata["certificateChecks"] == 17
    assert metadata["scalingRows"] == 81
    assert metadata["triadRows"] == 256
    assert metadata["bridgeRows"] == 3
    assert metadata["formalTriadsChecked"] == 200_000
    assert metadata["formalRotationWitnessesChecked"] == 15_624
    assert metadata["displayRowsAreProof"] is False
    assert metadata["randomness"] is False
    assert metadata["floatingPointDecisionUse"] is False

    progress = [
        json.loads(line)
        for line in (HERE / "progress.ndjson").read_text(encoding="utf-8").splitlines()
    ]
    assert len(progress) == 5
    assert progress[-1]["checks"] == 17
    with (HERE / "resources.csv").open(newline="", encoding="utf-8") as source:
        resources = list(csv.DictReader(source))
    assert len(resources) == 21
    assert resources[-1]["status"] == "exited:0"

    print(
        "validated R0.55 figure data: exact scaling line, 256 exact triads, "
        "three theorem-classified bridge decisions, and monitored provenance"
    )


if __name__ == "__main__":
    main()
