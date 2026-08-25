#!/usr/bin/env python3
"""Validate formulas and internal consistency of the R0.71H figure data."""

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
    parser.add_argument(
        "--metadata", type=Path, default=Path("figure-data-metadata.json")
    )
    parser.add_argument("--output", type=Path, default=Path("validation.json"))
    args = parser.parse_args()

    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    with args.data.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        row["x"] = float(row["x"])
        row["value"] = float(row["value"])

    checks: dict[str, bool] = {}
    require(metadata["release"] == "R0.71H", "release", checks)
    require(metadata["rows"] == len(rows) == 391, "rowCount", checks)
    require(metadata["method"] == "closed-form formula evaluation only", "closedFormOnly", checks)
    require(metadata["randomSeed"] is None, "deterministic", checks)
    require(metadata["dns"] is False, "notDNS", checks)
    require(metadata["pdeTimeStepping"] is False, "notPDETimeStepper", checks)
    require(metadata["fittedData"] is False, "notFitted", checks)

    by_key: dict[tuple[str, str], list[dict[str, str | float]]] = {}
    for row in rows:
        by_key.setdefault((str(row["panel"]), str(row["series"])), []).append(row)
    expected_counts = {
        ("A", "rayleighPayment"): 61,
        ("A", "angularIntegral"): 61,
        ("A", "curvatureIntegral"): 61,
        ("A", "identitySum"): 61,
        ("B", "angularSpeed"): 9,
        ("B", "sourceDensity"): 9,
        ("C", "rayleighQuotient"): 51,
        ("C", "projectiveSource"): 51,
        ("D", "knownHeatWeight"): 9,
        ("D", "directRequiredWeight"): 9,
        ("D", "gapRatio"): 9,
    }
    require(set(by_key) == set(expected_counts), "seriesSet", checks)
    for key, count in expected_counts.items():
        require(len(by_key[key]) == count, f"count_{key[0]}_{key[1]}", checks)

    lookup = {
        (str(row["panel"]), str(row["series"]), float(row["x"])): float(row["value"])
        for row in rows
    }
    maximum_formula_error = 0.0
    maximum_identity_error = 0.0

    for index in range(61):
        t = index / 40.0
        z = math.exp(-6.0 * t)
        payment = 2.5 - (1.0 + 4.0 * z) / (1.0 + z)
        expected = {
            "rayleighPayment": payment,
            "angularIntegral": 0.5 * payment,
            "curvatureIntegral": 0.5 * payment,
            "identitySum": payment,
        }
        for name, value in expected.items():
            maximum_formula_error = max(
                maximum_formula_error, abs(lookup[("A", name, t)] - value)
            )
        maximum_identity_error = max(
            maximum_identity_error,
            abs(
                lookup[("A", "identitySum", t)]
                - lookup[("A", "angularIntegral", t)]
                - lookup[("A", "curvatureIntegral", t)]
            ),
            abs(
                lookup[("A", "identitySum", t)]
                - lookup[("A", "rayleighPayment", t)]
            ),
        )

    source_values = []
    for exponent in range(9):
        k = float(2**exponent)
        omega = k / 2.0
        source = 0.25 * (3.0 + 2.0 / k) ** 2
        source_values.append(lookup[("B", "sourceDensity", k)])
        maximum_formula_error = max(
            maximum_formula_error,
            abs(lookup[("B", "angularSpeed", k)] - omega),
            abs(lookup[("B", "sourceDensity", k)] - source),
        )
    require(all(a > b for a, b in zip(source_values, source_values[1:])), "sourceApproachesLimitMonotonically", checks)
    require(abs(source_values[-1] - 9.0 / 4.0) < 0.05, "finiteSourceNearLimit", checks)
    require(lookup[("B", "angularSpeed", 256.0)] == 128.0, "pointwiseAngularGrowth", checks)

    for index in range(51):
        delta = index / 50.0
        square = delta * delta
        rayleigh = 2.0 * (3.0 * square + 2.0) / (3.0 * square + 4.0)
        projective = 12.0 * square / (3.0 * square + 4.0) ** 2
        maximum_formula_error = max(
            maximum_formula_error,
            abs(lookup[("C", "rayleighQuotient", delta)] - rayleigh),
            abs(lookup[("C", "projectiveSource", delta)] - projective),
        )
    require(lookup[("C", "rayleighQuotient", 0.0)] == 1.0, "cutoffRayleighAtZero", checks)
    require(abs(lookup[("C", "rayleighQuotient", 1.0)] - 10.0 / 7.0) < 2.0e-15, "cutoffRayleighAtOne", checks)
    require(abs(lookup[("C", "projectiveSource", 1.0)] - 12.0 / 49.0) < 2.0e-15, "cutoffSourceAtOne", checks)
    require(all(lookup[("C", "projectiveSource", index / 50.0)] > 0.0 for index in range(1, 51)), "cutoffSourcePositive", checks)

    for exponent in range(9):
        k = float(2**exponent)
        known = k ** (-2.0)
        required = 1.0
        ratio = k**2
        maximum_formula_error = max(
            maximum_formula_error,
            abs(lookup[("D", "knownHeatWeight", k)] - known),
            abs(lookup[("D", "directRequiredWeight", k)] - required),
            abs(lookup[("D", "gapRatio", k)] - ratio),
        )
        maximum_identity_error = max(
            maximum_identity_error,
            abs(required / known - ratio),
        )

    require(maximum_formula_error < 2.0e-15, "formulaAgreement", checks)
    require(maximum_identity_error < 2.0e-13, "exactBalances", checks)

    payload = {
        "release": "R0.71H",
        "status": "pass",
        "checks": checks,
        "metrics": {
            "maximumFormulaError": maximum_formula_error,
            "maximumIdentityError": maximum_identity_error,
            "panelBFinalSourceDensity": source_values[-1],
            "panelBSourceLimit": 9.0 / 4.0,
            "panelDMaximumGapRatio": 256.0**2,
        },
        "claimBoundary": (
            "Validates closed-form data and exact scaling identities only; it does not validate "
            "a general NSE angular budget or any regularity conclusion."
        ),
    }
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
