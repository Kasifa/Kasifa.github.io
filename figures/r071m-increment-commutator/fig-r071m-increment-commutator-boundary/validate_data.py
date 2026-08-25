#!/usr/bin/env python3
"""Producer-side validation of the R0.71M figure data."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def require(condition, label, checks):
    checks[label] = bool(condition)
    if not condition:
        raise AssertionError(label)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("data.csv"))
    parser.add_argument("--metadata", type=Path, default=Path("figure-data-metadata.json"))
    parser.add_argument("--output", type=Path, default=Path("validation.json"))
    args = parser.parse_args()
    with args.data.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    grouped = {}
    for row in rows:
        grouped.setdefault((row["panel"], row["series"]), []).append(row)
    checks = {}
    expected = {
        ("A", "signedPairingComponent"): 4,
        ("A", "signedPairingTotal"): 1,
        ("B", "normalizedCriticalRowSquare"): 4,
        ("B", "supportDiagnostic"): 1,
        ("C", "energy"): 7,
        ("C", "YuQuarticDefect"): 7,
        ("C", "velocityCarleson"): 7,
        ("C", "normalizedLamb"): 7,
        ("D", "implicationLedger"): 5,
    }
    require(set(grouped) == set(expected), "seriesSet", checks)
    for key, count in expected.items():
        require(len(grouped[key]) == count, f"count_{key[0]}_{key[1]}", checks)
    require(len(rows) == metadata["rows"], "metadataRowCount", checks)
    require(metadata["release"] == "R0.71M", "release", checks)
    require(metadata["randomSeed"] is None, "deterministic", checks)
    require(metadata["dns"] is False, "notDNS", checks)
    require(metadata["pdeTimeStepping"] is False, "notPDETimeStepper", checks)
    require(metadata["fittedData"] is False, "notFitted", checks)
    require(metadata["gridOrder"] >= 64, "formalGridOrder", checks)
    require(metadata["incrementIdentityRelativeResidual"] < 2.0e-11, "incrementResidual", checks)
    require(metadata["projectivePairingRelativeResidual"] < 3.0e-11, "pairingResidual", checks)
    require(metadata["offBandEnergyFraction"] > 1.0e-4, "offBandWitness", checks)
    require(metadata["highOffBandEnergyFraction"] > 1.0e-4, "highOffBandWitness", checks)

    components = {
        row["category"]: float(row["value"])
        for row in grouped[("A", "signedPairingComponent")]
    }
    total = float(grouped[("A", "signedPairingTotal")][0]["value"])
    component_residual = abs(sum(components.values()) - total)
    require(component_residual < 5.0e-12, "pairingComponentsSum", checks)

    row_fractions = [
        float(row["value"]) for row in grouped[("B", "normalizedCriticalRowSquare")]
    ]
    fraction_residual = abs(sum(row_fractions) - 1.0)
    require(fraction_residual < 5.0e-15, "rowFractionsSum", checks)
    off_band = float(grouped[("B", "supportDiagnostic")][0]["value"])
    require(0.0 < off_band < 1.0, "offBandFractionRange", checks)

    for series, exponent in (
        ("energy", 0.0),
        ("YuQuarticDefect", -2.0),
        ("velocityCarleson", -1.0),
        ("normalizedLamb", -1.0),
    ):
        selected = sorted(grouped[("C", series)], key=lambda row: float(row["x"]))
        for row in selected:
            radius = float(row["x"])
            expected_value = radius**exponent
            require(
                abs(float(row["value"]) - expected_value)
                < 1.0e-12 * max(expected_value, 1.0),
                f"scaling_{series}_{radius}",
                checks,
            )

    payload = {
        "release": "R0.71M",
        "status": "pass",
        "checks": checks,
        "metrics": {
            "rowCount": len(rows),
            "pairingComponentResidual": component_residual,
            "rowFractionResidual": fraction_residual,
            "offBandEnergyFraction": off_band,
        },
    }
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
