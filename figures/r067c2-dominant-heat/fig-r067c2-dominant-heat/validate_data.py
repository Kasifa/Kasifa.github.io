#!/usr/bin/env python3
"""Validate extracted R0.67C-2 figure data against the certificate."""

from __future__ import annotations

import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def main() -> None:
    intervals = rows("projection-intervals.csv")
    derivative = rows("derivative-budget.csv")
    scales = rows("spectral-scales.csv")
    metadata = json.loads((HERE / "figure-data-metadata.json").read_text())
    final = next(row for row in intervals if row["quantity"] == "complete projection")
    guard = next(row for row in derivative if row["quantity"] == "declared guard")
    threshold = next(row for row in derivative if row["quantity"] == "zero-contact threshold")
    scale = {row["quantity"]: float(row["value"]) for row in scales}
    checks = {
        "threeProjectionIntervals": len(intervals) == 3,
        "strictlyNegativeFinalUpper": float(final["upper"]) < 0,
        "derivativeGuardBelowThreshold": float(guard["value"]) < float(threshold["value"]),
        "degreeSixRemainderIsOneOver4096": scale["degree-six remainder"] == 1 / 4096,
        "spectralOrdering": scale["affine remainder"] < scale["other finite spectrum"] < scale["dominant root"],
        "allCertificateChecksPassed": metadata["checksPassed"] == metadata["checksTotal"] == 14,
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    print(json.dumps({"status": "passed", "checks": checks}, indent=2))


if __name__ == "__main__":
    main()
