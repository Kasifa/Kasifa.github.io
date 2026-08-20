#!/usr/bin/env python3
"""Validate the source-backed data for Figure R0.68B-2d/e."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def main() -> None:
    derivative = rows("derivative-bounds.csv")
    margins = rows("interval-margins.csv")
    budget = rows("pilot-budget.csv")
    metadata = json.loads((HERE / "figure-data-metadata.json").read_text())
    assert len(derivative) == 6
    values = [float(row["upper"]) for row in derivative]
    assert max(values) == values[3]
    assert max(values) < 2.567e-6
    assert all(math.isfinite(value) and value > 0 for value in values)
    assert len(margins) == 2
    assert all(float(row["decimalOrdersBeyondGate"]) > 8 for row in margins)
    assert len(budget) == 3
    signal, correction, gap = [float(row["value"]) for row in budget]
    assert correction < signal
    assert abs(signal - correction - gap) < 1e-23
    assert metadata["derivativeSha256"] == "f3fb38c23c872f15d10a2f332f242ab249233709fb4cb2a7cc1012bf42822f88"
    assert metadata["massSha256"] == "d079ba1b0c59beaf3e97b0ba4021bb14abdc131ba61317a11bc0c64e38a9cc7a"
    assert metadata["pilotSha256"] == "3539fdec6428bded0261ed5bef2e50a8423830f1736009605fdb95791e93d6a0"
    print("R0.68B-2d/e figure data validation passed")


if __name__ == "__main__":
    main()
