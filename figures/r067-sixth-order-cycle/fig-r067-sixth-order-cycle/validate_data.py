#!/usr/bin/env python3
"""Validate R0.67A figure tables against the pinned exact certificate."""

from __future__ import annotations

import csv
import hashlib
import json
from decimal import Decimal
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[2]
CERTIFICATE = REPOSITORY / "research/certificates/r067/sixth-order-cycle-audit.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def csv_rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    sequence = csv_rows("reachable-sequence.csv")
    spectrum = csv_rows("spectral-enclosures.csv")
    thresholds = csv_rows("thresholds.csv")
    metadata = json.loads((HERE / "figure-data-metadata.json").read_text(encoding="utf-8"))
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    exact_sequence = certificate["reachableTargetFamily"]["initialValues"]
    checks = {
        "fortyConsecutiveExactSequenceRows": [int(row["r"]) for row in sequence]
        == list(range(40)),
        "allExactSequenceIntegersMatch": [int(row["Y"]) for row in sequence]
        == exact_sequence,
        "firstNegativeCycleIsEleven": next(
            int(row["r"]) for row in sequence if row["sign"] == "negative"
        )
        == 11,
        "lateNormalizedValueIsNegative": Decimal(sequence[-1]["normalizedByMu"]) < 0,
        "lateM2RatioExceedsOneHundredThousand": Decimal(sequence[-1]["absoluteOverM2"])
        > Decimal("1e5"),
        "fourQuarticIntervalsPlusSchurDisk": len(spectrum) == 5,
        "dominantQuarticIntervalIs400To416": spectrum[3]["lower"] == "400"
        and spectrum[3]["upper"] == "416",
        "degreeTenDiskIsStrictlyInsideDominantRoot": Decimal(spectrum[4]["upper"])
        < Decimal(metadata["muLower"]),
        "C2ThresholdIs256": Decimal(thresholds[0]["lower"]) == Decimal(256),
        "dominantRootExceedsC2Threshold": Decimal(thresholds[1]["lower"])
        > Decimal(thresholds[0]["upper"]),
        "absoluteCarryEigenvalueIs65536": Decimal(thresholds[2]["lower"])
        == Decimal(65536),
        "certificateHashMatches": metadata["certificateSha256"] == sha256(CERTIFICATE),
        "certificatePassed": certificate["status"] == "passed"
        and all(certificate["checks"].values()),
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    print(json.dumps({"status": "passed", "checks": checks}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
