#!/usr/bin/env python3
"""Producer-side validation for the R0.71K figure data."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path


def require(condition: bool, label: str, checks: dict[str, bool]) -> None:
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
    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault((row["panel"], row["series"]), []).append(row)
    for selected in grouped.values():
        selected.sort(key=lambda row: float(row["x"]))
    checks: dict[str, bool] = {}
    expected_counts = {
        ("A", "leftAtom"): 301,
        ("A", "centerAtom"): 301,
        ("A", "rightAtom"): 301,
        ("A", "partitionSum"): 301,
        ("B", "globalAmplitude"): 241,
        ("B", "globalEndpoint"): 1,
        ("B", "localTemplateEndpoint"): 1,
        ("C", "creationPower"): 11,
        ("C", "heatPower"): 11,
        ("D", "scalingExponent"): 8,
    }
    require(set(grouped) == set(expected_counts), "seriesSet", checks)
    for key, count in expected_counts.items():
        require(len(grouped[key]) == count, f"count_{key[0]}_{key[1]}", checks)
    require(len(rows) == metadata["rows"], "metadataRowCount", checks)
    require(metadata["randomSeed"] is None, "deterministic", checks)
    require(metadata["dns"] is False, "notDNS", checks)
    require(metadata["pdeTimeStepping"] is False, "notPDETimeStepper", checks)
    require(metadata["fittedData"] is False, "notFitted", checks)
    require(all(row["formula"] and row["evidenceClass"] for row in rows), "provenancePresent", checks)

    partition_values = [float(row["value"]) for row in grouped[("A", "partitionSum")]]
    partition_residual = max(abs(value - 1.0) for value in partition_values)
    require(partition_residual < 4.0e-15, "partitionUnity", checks)
    require(all(float(row["value"]) >= 0.0 for key in grouped if key[0] == "A" for row in grouped[key]), "partitionNonnegative", checks)

    profile = grouped[("B", "globalAmplitude")]
    require(float(profile[0]["value"]) == 0.0, "zeroEntry", checks)
    theta_star = metadata["thetaStar"]
    nearest = min(profile, key=lambda row: abs(float(row["x"]) - theta_star))
    require(float(nearest["value"]) > 0.98, "positivePulseNearThetaStar", checks)
    require(float(grouped[("B", "globalEndpoint")][0]["value"]) == 1.0, "normalizedGlobalEndpoint", checks)
    require(float(grouped[("B", "localTemplateEndpoint")][0]["value"]) > 1.0, "positiveLocalTemplateEndpoint", checks)

    creation = grouped[("C", "creationPower")]
    heat = grouped[("C", "heatPower")]
    maximum_formula_error = 0.0
    normalized_ratios = []
    for creation_row, heat_row in zip(creation, heat):
        frequency = float(creation_row["x"])
        require(float(heat_row["x"]) == frequency, f"frequency_{frequency:g}", checks)
        maximum_formula_error = max(
            maximum_formula_error,
            abs(float(creation_row["value"]) - frequency**-2),
            abs(float(heat_row["value"]) - frequency**-4),
        )
        normalized_ratios.append(float(creation_row["value"]) / float(heat_row["value"]) / frequency**2)
    require(maximum_formula_error < 2.0e-20, "powerFormula", checks)
    require(max(normalized_ratios) - min(normalized_ratios) < 2.0e-14, "quadraticRatio", checks)
    require(abs(float(creation[-1]["value"]) / float(creation[0]["value"]) - (8.0 / 8192.0) ** 2) < 2.0e-21, "minusTwoPower", checks)
    require(abs(float(heat[-1]["value"]) / float(heat[0]["value"]) - (8.0 / 8192.0) ** 4) < 2.0e-27, "minusFourPower", checks)

    exponent_rows = grouped[("D", "scalingExponent")]
    exponent_map = {row["category"]: float(row["value"]) for row in exponent_rows}
    expected_exponents = {"B_Q": 0.0, "d_Q": 1.0, "q_Q": -1.0, "a_Q": -3.0, "Z_loc": -2.0, "H_loc": -4.0, "collar": -2.0, "Z/H": 2.0}
    require(exponent_map == expected_exponents, "exponentLedger", checks)
    require(exponent_map["collar"] == exponent_map["Z_loc"], "collarLeading", checks)

    payload = {
        "release": "R0.71K",
        "status": "pass",
        "checks": checks,
        "metrics": {
            "rowCount": len(rows),
            "maximumPartitionResidual": partition_residual,
            "maximumFormulaError": maximum_formula_error,
            "thetaStar": theta_star,
            "AStar": metadata["AStar"],
        },
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

