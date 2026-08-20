#!/usr/bin/env python3
"""Validate the R0.65 figure tables against the pinned scientific claims."""

from __future__ import annotations

import csv
import hashlib
import json
from decimal import Decimal
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[2]
CERTIFICATE = REPOSITORY / "research/certificates/r065/weighted-cycle-audit.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    rows = list(csv.DictReader((HERE / "cycle-enclosures.csv").open(encoding="utf-8")))
    metadata = json.loads((HERE / "figure-data-metadata.json").read_text(encoding="utf-8"))
    report = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    checks = {
        "twentyFourConsecutiveRows": [int(row["r"]) for row in rows] == list(range(1, 25)),
        "exactCycleLengths": all(int(row["M"]) == 16 ** int(row["r"]) for row in rows),
        "positiveThroughR13": all(row["signCertified"] == "positive" for row in rows[:13]),
        "negativeFromR14": all(row["signCertified"] == "negative" for row in rows[13:]),
        "tenSupercriticalBlocks": all(
            Decimal(rows[index - 1]["absoluteBlockRatioLower"]) > 16
            for index in range(15, 25)
        ),
        "finalRatioCertified": Decimal(rows[-1]["absoluteBlockRatioLower"]) > Decimal("25.29")
        and Decimal(rows[-1]["absoluteBlockRatioUpper"]) < Decimal("25.30"),
        "finalNormalizedMagnitudeExceedsOne": abs(Decimal(rows[-1]["S4OverMCenter"])) > 1,
        "finalTailBelowTwoPartsInTrillion": Decimal(rows[-1]["relativeTail"]) < Decimal("2e-12"),
        "metadataCertificateHashMatches": metadata["certificateSha256"] == sha256(CERTIFICATE),
        "sourceCertificatePassed": all(report["checks"].values()),
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    print(json.dumps({"status": "passed", "checks": checks}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
