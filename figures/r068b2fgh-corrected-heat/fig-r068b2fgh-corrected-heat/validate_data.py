#!/usr/bin/env python3
"""Validate source-backed data for Figure R0.68B-2f/g/h."""

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
    moments = rows("moment-radius-by-degree.csv")
    heat = rows("heat-partial-by-degree.csv")
    budget = rows("sign-budget.csv")
    summary = rows("certified-summary.csv")[0]
    metadata = json.loads((HERE / "figure-data-metadata.json").read_text())

    assert [int(row["degree"]) for row in moments] == list(range(11))
    radii = [float(row["maximumRadius"]) for row in moments]
    assert all(math.isfinite(value) and value > 0 for value in radii)
    assert all(left < right for left, right in zip(radii, radii[1:]))
    assert radii[-1] == 7.91179658125257438e-22
    assert [int(row["degree"]) for row in heat] == list(range(11))
    assert all(float(row["upper"]) < 0 for row in heat)
    assert float(heat[-1]["centre"]) == -1.49238243184751323e-8
    assert len(budget) == 3
    signal, correction, margin = [float(row["value"]) for row in budget]
    assert correction < signal
    assert margin > 0
    assert abs((signal - correction) - margin) < 1e-23
    assert float(summary["correctedUpper"]) < 0
    assert summary["independentVerificationStatus"] == "strict-passed"
    assert metadata["momentSha256"] == (
        "2aae68d256e7e17e8689e8536ba4a52398a0cf0c21f0de657537ee6c66b28c60"
    )
    assert metadata["heatSha256"] == (
        "0e21199c676d74950029ea93f2562032787361e00e9332c4c1bc1c2aa6b5f38d"
    )
    assert metadata["defectSha256"] == (
        "c79f78816ae780074b90c7eb098d0b804253e1a449cbd0e0b8e60861de0f5bca"
    )
    assert metadata["verificationSha256"] == (
        "499e9914d8b5bf2248070f84f0e09c7f68cdc8f43fc84fa47a357fc9896fcc78"
    )
    print("R0.68B-2f/g/h figure data validation passed")


if __name__ == "__main__":
    main()
