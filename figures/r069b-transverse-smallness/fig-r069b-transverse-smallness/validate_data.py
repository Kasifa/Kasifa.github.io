#!/usr/bin/env python3
"""Validate Figure R0.69B data against the source-bound certificate."""

from __future__ import annotations

import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def main() -> None:
    scales = rows("scale-separation.csv")
    decisions = rows("decision-depth.csv")
    crossings = rows("certified-crossings.csv")
    metadata = json.loads((HERE / "figure-data-metadata.json").read_text())
    amplitudes = [float(row["physicalAmplitudeLower"]) for row in scales]
    critical = [float(row["criticalNormUpper"]) for row in scales]
    expected = {"1": 11, "1e-1": 22, "1e-2": 32, "1e-3": 42, "1e-6": 72}
    observed = {
        row["budget"]: int(row["firstDepthStrictlyBelow"])
        for row in crossings
    }
    decision_depths = [int(row["firstDepthStrictlyBelow"]) for row in decisions]
    checks = {
        "fiftyOneScaleDepths": len(scales) == 51,
        "physicalAmplitudeLowerBoundStrictlyGrows": all(
            right > left for left, right in zip(amplitudes, amplitudes[1:])
        ),
        "criticalNormUpperBoundStrictlyDecays": all(
            right < left for left, right in zip(critical, critical[1:])
        ),
        "criticalRateIsBelowOne": 0 < float(metadata["rhoUpper"]) < 1,
        "physicalAmplitudeBaseIsAboveOne": (
            float(metadata["physicalAmplitudeBaseLower"]) > 1
        ),
        "certifiedCrossingsMatch": observed == expected,
        "decisionDepthIsMonotone": all(
            right >= left for left, right in zip(decision_depths, decision_depths[1:])
        ),
        "formalCertificatePassedThirteenChecks": (
            metadata["checksPassed"] == metadata["checksTotal"] == 13
        ),
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    print(json.dumps({"status": "passed", "checks": checks}, indent=2))


if __name__ == "__main__":
    main()
