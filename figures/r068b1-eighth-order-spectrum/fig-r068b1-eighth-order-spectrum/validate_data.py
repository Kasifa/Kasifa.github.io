#!/usr/bin/env python3
"""Validate the R0.68B-1 figure tables and strict claim boundary."""

from __future__ import annotations

import csv
from decimal import Decimal
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def main() -> None:
    ranks = rows("rank-collapse.csv")
    blocks = rows("spectral-blocks.csv")
    sequence = rows("reachable-sequence.csv")
    scales = {row["quantity"]: row for row in rows("certified-scales.csv")}
    metadata = json.loads((HERE / "figure-data-metadata.json").read_text())
    normalized = [Decimal(row["normalizedByDominantRootMidpoint"]) for row in sequence]
    checks = {
        "rankCollapseIsExact": [int(row["exactRank"]) for row in ranks] == [1792, 204, 148, 148],
        "imageBlocksSumToTwoZeroFour": sum(int(row["imageDimension"]) for row in blocks) == 204,
        "factorDegreesMatchMultiplicities": sum(int(row["degree"]) * int(row["multiplicity"]) for row in blocks) == 204,
        "dominantRootExceedsRemainderRadius": Decimal(scales["dominant root nu"]["lower"]) > Decimal(scales["remainder spectral radius"]["upper"]),
        "projectionIntervalStrictlyNegative": Decimal(scales["dominant coefficient C8,0"]["upper"]) < 0,
        "probeRateContracts": Decimal(scales["quartic-critical probe rate"]["upper"]) < 1,
        "sequenceCrossesToNegative": any(value > 0 for value in normalized) and all(value < 0 for value in normalized[10:]),
        "lateSequenceApproachesCoefficientInterval": abs(
            normalized[-1]
            - (
                Decimal(scales["dominant coefficient C8,0"]["lower"])
                + Decimal(scales["dominant coefficient C8,0"]["upper"])
            )
            / 2
        ) < Decimal("1e-10"),
        "formalAuditPassedSeventeenChecks": metadata["checksPassed"] == metadata["checksTotal"] == 17,
        "heatBoundaryStillExplicit": "not a certificate for the complete heat-weighted" in metadata["claimBoundary"],
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    print(json.dumps({"status": "passed", "checks": checks}, indent=2))


if __name__ == "__main__":
    main()
