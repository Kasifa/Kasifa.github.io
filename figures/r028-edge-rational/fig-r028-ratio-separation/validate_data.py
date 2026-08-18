#!/usr/bin/env python3
"""Cross-check the R0.28 plotted table against the exact certificate."""

from __future__ import annotations

import csv
from decimal import Decimal, getcontext
from fractions import Fraction
import json
from pathlib import Path


getcontext().prec = 80
PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
CERTIFICATE = (
    REPOSITORY / "research/certificates/r028/edge-rational-asymptotic.json"
)


def close(actual: str, expected: str, tolerance: Decimal = Decimal("2e-15")) -> None:
    if abs(Decimal(actual) - Decimal(expected)) > tolerance:
        raise AssertionError(f"plotted value {actual} != certified value {expected}")


def main() -> None:
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    endpoints = [
        record for record in payload["endpoints"] if record["parameter"] >= 18
    ]
    with (PACKAGE / "data.csv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))

    assert len(rows) == len(endpoints) == 23
    minimum_gamma = None
    for row, endpoint in zip(rows, endpoints, strict=True):
        parameter = endpoint["parameter"]
        assert int(row["N"]) == parameter
        ratios = endpoint["consecutiveRatios"]
        expected = {
            "rhoA": ratios["normalizedRadiusProxyA"]["decimal"],
            "rhoDLower": ratios["normalizedRadiusProxyD"]["decimal"][0],
            "rhoDUpper": ratios["normalizedRadiusProxyD"]["decimal"][1],
            "gammaLower": ratios["sharpToAlphaBlockFactorRootBox"]["decimal"][0],
            "gammaUpper": ratios["sharpToAlphaBlockFactorRootBox"]["decimal"][1],
        }
        for field, value in expected.items():
            close(row[field], value)

        rho_a = Fraction(ratios["normalizedRadiusProxyA"]["exact"])
        rho_d_lower = Fraction(ratios["normalizedRadiusProxyD"]["lower"])
        rho_d_upper = Fraction(ratios["normalizedRadiusProxyD"]["upper"])
        gamma_lower = Fraction(
            ratios["sharpToAlphaBlockFactorRootBox"]["lower"]
        )
        gamma_upper = Fraction(
            ratios["sharpToAlphaBlockFactorRootBox"]["upper"]
        )
        assert 0 < rho_d_lower <= rho_d_upper < rho_a
        assert 1 < gamma_lower <= gamma_upper
        assert gamma_lower == rho_a / rho_d_upper
        assert gamma_upper == rho_a / rho_d_lower
        minimum_gamma = (
            gamma_lower
            if minimum_gamma is None
            else min(minimum_gamma, gamma_lower)
        )

    summary = payload["finiteTailSummary"]
    assert summary["persistentFiniteRatioSeparationFrom"] == 18
    assert summary["persistentFiniteRatioSeparationWindow"]["end"] == 40
    assert summary["finiteBandsDisjoint"] is True
    assert summary["finiteSharpFactorAboveOne"] is True
    assert minimum_gamma is not None
    assert Decimal(minimum_gamma.numerator) / Decimal(minimum_gamma.denominator) > Decimal(
        "1.0294319301"
    )
    print("validated 23 plotted rows against the exact R0.28 certificate")


if __name__ == "__main__":
    main()
