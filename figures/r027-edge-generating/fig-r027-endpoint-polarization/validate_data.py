#!/usr/bin/env python3
"""Cross-check the plotted R0.27 table against the formal certificate."""

from __future__ import annotations

import csv
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
CERTIFICATE = (
    REPOSITORY / "research/certificates/r027/edge-generating-function.json"
)


def main() -> None:
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    endpoints = payload["runs"][-1]["endpoints"]
    stability = payload["checks"]["precisionStability"]
    with (PACKAGE / "data.csv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))

    assert len(rows) == len(endpoints) == 74
    for row, endpoint in zip(rows, endpoints, strict=True):
        parameter = int(row["N"])
        assert parameter == endpoint["parameter"]
        sigma = float(endpoint["sigma"])
        ratio = abs(float(endpoint["sharpOverLAlpha"]))
        expected = {
            "sigma": sigma,
            "parityNormalizedSigma": ((-1) ** parameter) * sigma,
            "absoluteSigma": float(endpoint["absoluteSigma"]),
            "oneMinusAbsoluteSigma": float(endpoint["oneMinusAbsoluteSigma"]),
            "absoluteSharpOverLAlpha": ratio,
            "inverseAbsoluteSharpOverLAlpha": 1 / ratio,
            "sigmaRelativePrecisionDifference": float(
                stability[f"N{parameter}"]["sigmaRelativeDifference"]
            ),
        }
        for field, value in expected.items():
            assert float(row[field]) == value, (parameter, field)

    assert float(rows[-1]["absoluteSigma"]) > 0.999
    assert max(
        float(row["sigmaRelativePrecisionDifference"]) for row in rows
    ) < 1e-40
    print("validated 74 plotted endpoint rows against the R0.27 certificate")


if __name__ == "__main__":
    main()
