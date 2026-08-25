#!/usr/bin/env python3
"""Validate formulas and internal consistency of the R0.71I figure data."""

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


def nse_profiles(theta: float) -> tuple[float, float]:
    x = math.exp(-10.0 * theta)
    q_scaled = 4.0 * x * (1.0 - x) ** 2 / (1.0 + x)
    y_scaled = (
        2.0 * math.exp(-2.0 * theta)
        + 2.0 * math.exp(-8.0 * theta)
        + 2.0 * math.exp(-18.0 * theta)
        + 0.8 * math.exp(-10.0 * theta)
        + 0.4 * math.exp(-20.0 * theta)
    )
    f_scaled = 4.0 * (
        math.exp(-10.0 * theta) + math.exp(-20.0 * theta)
    )
    return q_scaled / y_scaled, f_scaled / y_scaled


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("data.csv"))
    parser.add_argument("--metadata", type=Path, default=Path("figure-data-metadata.json"))
    parser.add_argument("--output", type=Path, default=Path("validation.json"))
    args = parser.parse_args()
    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    with args.data.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault((row["panel"], row["series"]), []).append(row)
    for selected in grouped.values():
        selected.sort(key=lambda row: float(row["x"]))

    checks: dict[str, bool] = {}
    require(metadata["release"] == "R0.71I", "release", checks)
    require(metadata["rows"] == len(rows) == 567, "rowCount", checks)
    require(metadata["method"] == "closed-form formula evaluation only", "closedFormOnly", checks)
    require(metadata["randomSeed"] is None, "deterministic", checks)
    require(metadata["dns"] is False, "notDNS", checks)
    require(metadata["pdeTimeStepping"] is False, "notPDETimeStepper", checks)
    require(metadata["fittedData"] is False, "notFitted", checks)
    expected_counts = {
        ("A", "commonHeatPulse"): 151,
        ("A", "pulsePeak"): 1,
        ("B", "traceVolumeRatio"): 9,
        ("C", "A0"): 151,
        ("C", "G0"): 151,
        ("C", "positiveTestPoint"): 1,
        ("D", "aggregateCoefficient"): 101,
        ("D", "refreshEndpoint"): 2,
    }
    require(set(grouped) == set(expected_counts), "seriesSet", checks)
    for key, count in expected_counts.items():
        require(len(grouped[key]) == count, f"count_{key[0]}_{key[1]}", checks)
    require(all(row["formula"] for row in rows), "formulaProvenance", checks)
    require(all(row["evidenceClass"] for row in rows), "evidenceClassPresent", checks)

    maximum_formula_error = 0.0
    maximum_sampling_error = 0.0
    pulse_values: list[float] = []
    for index, row in enumerate(grouped[("A", "commonHeatPulse")]):
        tau = float(row["x"])
        expected_tau = 3.0 * index / 150.0
        x = math.exp(-2.0 * tau)
        expected = x * (1.0 - x) ** 2 / (2.0 * (1.0 + x))
        value = float(row["value"])
        maximum_sampling_error = max(maximum_sampling_error, abs(tau - expected_tau))
        maximum_formula_error = max(maximum_formula_error, abs(value - expected))
        pulse_values.append(value)
    require(pulse_values[0] == 0.0, "commonHeatEntryFaceZero", checks)
    require(pulse_values[-1] < 0.0013, "commonHeatTailNearZero", checks)
    peak_row = grouped[("A", "pulsePeak")][0]
    x_star = (-3.0 + math.sqrt(17.0)) / 4.0
    tau_star = -0.5 * math.log(x_star)
    q_star = 8.0 / (71.0 + 17.0 * math.sqrt(17.0))
    maximum_formula_error = max(
        maximum_formula_error,
        abs(float(peak_row["x"]) - tau_star),
        abs(float(peak_row["value"]) - q_star),
    )
    require(q_star > max(pulse_values) - 3.0e-6, "exactPeakDominatesGrid", checks)
    require(q_star > 0.05, "positiveInteriorPulse", checks)

    ratio_constant = 128.0 / (3.0 * (71.0 + 17.0 * math.sqrt(17.0)))
    ratio_normalized: list[float] = []
    for index, row in enumerate(grouped[("B", "traceVolumeRatio")]):
        frequency = float(row["x"])
        expected_frequency = float(2**index)
        expected = ratio_constant * frequency**2
        value = float(row["value"])
        maximum_sampling_error = max(
            maximum_sampling_error, abs(frequency - expected_frequency)
        )
        maximum_formula_error = max(maximum_formula_error, abs(value - expected))
        ratio_normalized.append(value / frequency**2)
    require(
        max(ratio_normalized) - min(ratio_normalized) < 2.0e-15,
        "exactQuadraticRatio",
        checks,
    )
    require(
        float(grouped[("B", "traceVolumeRatio")][-1]["value"])
        / float(grouped[("B", "traceVolumeRatio")][0]["value"])
        == 256.0**2,
        "quadraticRange",
        checks,
    )

    a_values: list[float] = []
    g_values: list[float] = []
    for index in range(151):
        a_row = grouped[("C", "A0")][index]
        g_row = grouped[("C", "G0")][index]
        theta = float(a_row["x"])
        expected_theta = 0.6 * index / 150.0
        expected_a, expected_g = nse_profiles(theta)
        a_value = float(a_row["value"])
        g_value = float(g_row["value"])
        maximum_sampling_error = max(
            maximum_sampling_error,
            abs(theta - expected_theta),
            abs(float(g_row["x"]) - expected_theta),
        )
        maximum_formula_error = max(
            maximum_formula_error,
            abs(a_value - expected_a),
            abs(g_value - expected_g),
        )
        a_values.append(a_value)
        g_values.append(g_value)
    require(a_values[0] == 0.0, "nseEntryCoefficientZero", checks)
    require(max(a_values[1:]) > 0.02, "nseInteriorPulsePositive", checks)
    require(all(value > 0.0 for value in g_values), "nseHeatDensityPositive", checks)
    require(all(left > right for left, right in zip(g_values, g_values[1:])), "nseHeatDensityDecreases", checks)
    test_row = grouped[("C", "positiveTestPoint")][0]
    theta_test = math.log(2.0) / 10.0
    expected_test, _ = nse_profiles(theta_test)
    maximum_formula_error = max(
        maximum_formula_error,
        abs(float(test_row["x"]) - theta_test),
        abs(float(test_row["value"]) - expected_test),
    )
    require(expected_test > 0.0, "nseExactTestPointPositive", checks)

    aggregate_values: list[float] = []
    for index, row in enumerate(grouped[("D", "aggregateCoefficient")]):
        delta = float(row["x"])
        expected_delta = index / 100.0
        expected = 1.0 / (3.0 * delta**2 + 4.0)
        value = float(row["value"])
        maximum_sampling_error = max(
            maximum_sampling_error, abs(delta - expected_delta)
        )
        maximum_formula_error = max(maximum_formula_error, abs(value - expected))
        aggregate_values.append(value)
    require(all(left > right for left, right in zip(aggregate_values, aggregate_values[1:])), "refreshCurveDecreases", checks)
    endpoints = grouped[("D", "refreshEndpoint")]
    require(float(endpoints[0]["x"]) == 0.0, "refreshLeftX", checks)
    require(float(endpoints[1]["x"]) == 1.0, "refreshRightX", checks)
    refresh_gap = float(endpoints[0]["value"]) - float(endpoints[1]["value"])
    maximum_formula_error = max(maximum_formula_error, abs(refresh_gap - 3.0 / 28.0))
    require(abs(refresh_gap - 3.0 / 28.0) < 2.0e-16, "exactRefreshGap", checks)
    require(maximum_sampling_error < 2.0e-16, "samplingGrid", checks)
    require(maximum_formula_error < 5.0e-12, "formulaAgreement", checks)

    payload = {
        "release": "R0.71I",
        "status": "pass",
        "checks": checks,
        "metrics": {
            "maximumFormulaError": maximum_formula_error,
            "maximumSamplingError": maximum_sampling_error,
            "commonHeatExactPeak": q_star,
            "commonHeatRatioConstantNu1": ratio_constant,
            "nseMaximumA0OnGrid": max(a_values),
            "nseInitialG0": g_values[0],
            "refreshGap": refresh_gap,
        },
        "claimBoundary": (
            "Validates closed-form data, an exact common-heat ratio, the stated "
            "2D3C limiting profiles, and refresh algebra only; no finite-K PDE "
            "simulation, broad-frame theorem, or regularity conclusion."
        ),
    }
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
