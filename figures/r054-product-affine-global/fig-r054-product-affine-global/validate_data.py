#!/usr/bin/env python3
"""Independently validate every archived R0.54 figure table and provenance pin."""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CERTIFICATE = ROOT / "research/certificates/r054/edge-product-affine-family-global.json"
DIAGNOSTIC = ROOT / "research/certificates/r054/product-family-diagnostic.json"
EXPECTED = {
    "certificate": "130e954c3f8b711c28664f6f1d2aeb589942f69773ac9c839d98cc8f71b3006b",
    "diagnostic": "0553525f77aeffbe74eb64eda300d5673159022776aa15a6d963d5e7f45618bf",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    assert sha256(CERTIFICATE) == EXPECTED["certificate"]
    assert sha256(DIAGNOSTIC) == EXPECTED["diagnostic"]
    exact = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    diagnostic = json.loads(DIAGNOSTIC.read_text(encoding="utf-8"))
    assert len(exact["checks"]) == 16
    assert all(exact["checks"].values())

    domain = rows("invariant-domain.csv")
    assert len(domain) == 201
    for index, row in enumerate(domain):
        x = Fraction(row["scaledAExact"])
        assert x == Fraction(index, 100)
        assert Fraction(row["scaledBLowerExact"]) == max(Fraction(0), x - 1)
        assert Fraction(row["scaledBUpperExact"]) == x * x / 4
        assert row["classification"] == "exact invariant-domain presentation sample"

    leaves = rows("cover-leaves.csv")
    assert len(leaves) == 14
    assert {key: sum(row["excludedBy"] == key for row in leaves) for key in ("H", "P", "Q")} == {"H": 9, "P": 1, "Q": 4}
    cover = exact["continuousDomainCover"]
    c_width = Fraction(cover["characterInterval"][1]["exact"]) - Fraction(cover["characterInterval"][0]["exact"])
    for region in ("A<=h", "A>=h"):
        area = sum(
            (Fraction(row["characterUpperExact"]) - Fraction(row["characterLowerExact"]))
            * (Fraction(row["scaledAUpperExact"]) - Fraction(row["scaledALowerExact"]))
            for row in leaves
            if row["region"] == region
        )
        assert area == c_width
    assert cover["noParameterGridUsed"] is True
    assert cover["leafSetSha256"] == "449345d8d5daf02d549d75bc7c4eafe16b7d59dc8213c6e173df5a87a6253ef9"

    enclosure = rows("global-enclosure.csv")
    assert len(enclosure) == 3
    assert [row["status"] for row in enclosure] == ["certified", "not proof", "certified"]
    lower = Fraction(enclosure[0]["radiusExact"])
    upper = Fraction(enclosure[2]["radiusExact"])
    candidate = Fraction(diagnostic["symmetricCandidate"]["radius"])
    assert lower < candidate < upper
    affine = Fraction(exact["comparisonWithCompleteAffineFamily"]["completeAffineUpper"]["exact"])
    assert Fraction(enclosure[0]["gainPpmExact"]) == (lower / affine - 1) * 1_000_000
    assert Fraction(enclosure[2]["gainPpmExact"]) == (upper / affine - 1) * 1_000_000

    starts = rows("diagnostic-starts.csv")
    assert len(starts) == 64
    assert sum(row["success"] == "true" for row in starts) == diagnostic["multistart"]["convergedFeasibleRuns"] == 56
    basin_counts = {name: sum(row["basin"] == name for row in starts) for name in diagnostic["multistart"]["basinCounts"]}
    assert basin_counts == diagnostic["multistart"]["basinCounts"]

    metadata = json.loads((HERE / "figure-data-metadata.json").read_text(encoding="utf-8"))
    assert metadata["certificateSha256"] == EXPECTED
    assert len(metadata["figureSourceCommit"]) == 40
    assert metadata["certificateChecks"] == 16
    assert metadata["coverLeafCount"] == 14
    assert metadata["domainRows"] == 201
    assert metadata["diagnosticRows"] == 64
    assert metadata["diagnosticConvergedFeasibleRuns"] == 56
    assert metadata["randomSeed"] == 54054
    assert metadata["decimalDecisionUse"] is False
    assert metadata["displaySamplesAreProof"] is False

    with (ROOT / "research/certificates/r054/resources.csv").open(newline="", encoding="utf-8") as source:
        formal_resources = list(csv.DictReader(source))
    with (ROOT / "research/certificates/r054/diagnostic-resources.csv").open(newline="", encoding="utf-8") as source:
        diagnostic_resources = list(csv.DictReader(source))
    assert len(formal_resources) == 38 and formal_resources[-1]["status"] == "exited:0"
    assert len(diagnostic_resources) == 7 and diagnostic_resources[-1]["status"] == "exited:0"
    progress = [json.loads(line) for line in (ROOT / "research/certificates/r054/progress.ndjson").read_text(encoding="utf-8").splitlines()]
    assert progress[-1]["checks"] == 16

    print("validated R0.54 figure data: exact invariant domain, all 14 cover leaves, formal enclosure, 64 diagnostic starts, and monitored provenance")


if __name__ == "__main__":
    main()
