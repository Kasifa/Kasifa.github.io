#!/usr/bin/env python3
"""Validate the presentation tables used by Figure R0.62-1."""

from __future__ import annotations

import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    profiles = rows("weighted-target-profiles.csv")
    scales = rows("scale-comparison.csv")
    metadata = json.loads((HERE / "figure-data-metadata.json").read_text(encoding="utf-8"))
    checks = {
        "profileRowCount": len(profiles) == 3840 == metadata["profileRows"],
        "scaleRowCount": len(scales) == 13 == metadata["scaleRows"],
        "completeFamilies": all(
            sum(int(row["M"]) == outputs for row in profiles) == outputs
            for outputs in (256, 512, 1024, 2048)
        ),
        "targetFractionsExact": all(
            abs(float(row["targetFraction"]) - int(row["target"]) / int(row["M"])) < 1e-15
            for row in profiles
        ),
        "allDisplayedRatiosPositive": all(
            float(row["normalizedSignedRatio"]) > 0 for row in profiles
        ),
        "weightedMaximumPinned": abs(
            max(float(row["normalizedSignedRatio"]) for row in profiles)
            - 0.0012127996801718404
        ) < 1e-18,
        "unweightedRowsPositive": all(
            int(row["unweightedOuterMaximum"]) > 0
            and float(row["unweightedOuterMaximumOverM"]) > 0
            for row in scales
        ),
        "fftIntegerRecoveryStable": all(
            float(row["fftIntegerRecoveryResidual"]) < 1e-5 for row in scales
        ),
        "noRandomness": metadata["environment"]["randomness"] is False,
    }
    report = {"status": "passed" if all(checks.values()) else "failed", "checks": checks}
    print(json.dumps(report, indent=2, sort_keys=True))
    if report["status"] != "passed":
        raise SystemExit("Figure R0.62-1 data validation failed")


if __name__ == "__main__":
    main()
