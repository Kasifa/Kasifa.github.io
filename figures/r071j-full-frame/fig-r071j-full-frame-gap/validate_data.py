#!/usr/bin/env python3
"""Producer-side validation for the R0.71J full-frame figure data."""

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


def profiles(theta: float) -> tuple[float, float, float, float, float, float]:
    exponential = lambda power: math.exp(-power * theta)
    b_zero = 4.0 * (exponential(34.0) - exponential(52.0))
    d_zero = (
        32.0 * exponential(32.0)
        + 1156.0 * exponential(34.0)
        + 50.0 * exponential(50.0)
        + 2704.0 * exponential(52.0)
    )
    y_zero = (
        2.0 * exponential(2.0)
        + 2.0 * exponential(32.0)
        + 68.0 * exponential(34.0)
        + 2.0 * exponential(50.0)
        + 104.0 * exponential(52.0)
    )
    f_zero_square = (
        4.0 * exponential(34.0)
        + 192.0 * exponential(36.0)
        + 4.0 * exponential(52.0)
        + 300.0 * exponential(54.0)
    )
    if b_zero == 0.0:
        return b_zero, d_zero, y_zero, f_zero_square, 0.0, 0.0
    b_prime = 4.0 * (-34.0 * exponential(34.0) + 52.0 * exponential(52.0))
    d_prime = -(
        32.0 * 32.0 * exponential(32.0)
        + 34.0 * 1156.0 * exponential(34.0)
        + 50.0 * 50.0 * exponential(50.0)
        + 52.0 * 2704.0 * exponential(52.0)
    )
    y_prime = -(
        2.0 * 2.0 * exponential(2.0)
        + 32.0 * 2.0 * exponential(32.0)
        + 34.0 * 68.0 * exponential(34.0)
        + 50.0 * 2.0 * exponential(50.0)
        + 52.0 * 104.0 * exponential(52.0)
    )
    a_zero = b_zero * b_zero / (d_zero * y_zero)
    a_prime = a_zero * (2.0 * b_prime / b_zero - d_prime / d_zero - y_prime / y_zero)
    return b_zero, d_zero, y_zero, f_zero_square, a_zero, a_prime


def a_star_exact() -> float:
    root = 2.0 ** (1.0 / 9.0)
    return 4.0 / (57.0 * (root + 44.0) * (3.0 * root + 4.0 * 2.0 ** (7.0 / 9.0) + 120.0))


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
        selected.sort(key=lambda row: (float(row["x"]), row["category"]))

    checks: dict[str, bool] = {}
    require(metadata["release"] == "R0.71J", "release", checks)
    require(metadata["rows"] == len(rows) == 856, "rowCount", checks)
    require(metadata["method"] == "closed-form formula evaluation only", "closedFormOnly", checks)
    require(metadata["randomSeed"] is None, "deterministic", checks)
    require(metadata["dns"] is False, "notDNS", checks)
    require(metadata["pdeTimeStepping"] is False, "notPDETimeStepper", checks)
    require(metadata["fittedData"] is False, "notFitted", checks)
    expected_counts = {
        ("A", "positiveCreation"): 1,
        ("A", "timeDerivative"): 1,
        ("A", "viscousMass"): 1,
        ("A", "negativeDefect"): 1,
        ("B", "Bnormalized"): 201,
        ("B", "Dnormalized"): 201,
        ("B", "Ynormalized"): 201,
        ("B", "anormalized"): 201,
        ("C", "Zlower"): 11,
        ("C", "Hupper"): 11,
        ("C", "ratioOverK2"): 11,
        ("D", "Bgroup"): 3,
        ("D", "F2group"): 3,
        ("D", "dgroup"): 3,
        ("D", "frameRadius"): 6,
    }
    require(set(grouped) == set(expected_counts), "seriesSet", checks)
    for key, expected in expected_counts.items():
        require(len(grouped[key]) == expected, f"count_{key[0]}_{key[1]}", checks)
    require(all(row["formula"] for row in rows), "formulaProvenance", checks)
    require(all(row["evidenceClass"] for row in rows), "evidenceClassPresent", checks)

    maximum_formula_error = 0.0
    maximum_sampling_error = 0.0
    theta_star = math.log(2.0) / 18.0
    _, _, _, _, a_star_profile, a_prime = profiles(theta_star)
    a_star = a_star_exact()
    require(abs(a_star_profile - a_star) < 2.0e-19, "closedAStar", checks)
    source = 0.5 * (a_prime + 32.0 * a_star_profile)
    expected_a = {
        "positiveCreation": 2.0 * max(source, 0.0),
        "timeDerivative": a_prime,
        "viscousMass": 32.0 * a_star_profile,
        "negativeDefect": 2.0 * max(-source, 0.0),
    }
    for series, expected in expected_a.items():
        row = grouped[("A", series)][0]
        maximum_sampling_error = max(maximum_sampling_error, abs(float(row["x"]) - theta_star))
        maximum_formula_error = max(maximum_formula_error, abs(float(row["value"]) - expected))
    lhs = float(grouped[("A", "positiveCreation")][0]["value"])
    rhs = sum(float(grouped[("A", series)][0]["value"]) for series in ("timeDerivative", "viscousMass", "negativeDefect"))
    require(abs(lhs - rhs) < 3.0e-18, "positiveDefectIdentity", checks)
    require(source > 0.0, "positiveSourceAtThetaStar", checks)
    require(float(grouped[("A", "negativeDefect")][0]["value"]) == 0.0, "zeroNegativeDefectAtThetaStar", checks)

    b_star = profiles(theta_star)[0]
    profile_maxima: dict[str, float] = {}
    for index in range(201):
        theta_expected = 0.4 * index / 200.0
        values = profiles(theta_expected)
        expected = {
            "Bnormalized": values[0] / b_star,
            "Dnormalized": values[1] / 3942.0,
            "Ynormalized": values[2] / 178.0,
            "anormalized": values[4] / a_star,
        }
        for series, expected_value in expected.items():
            row = grouped[("B", series)][index]
            maximum_sampling_error = max(maximum_sampling_error, abs(float(row["x"]) - theta_expected))
            maximum_formula_error = max(maximum_formula_error, abs(float(row["value"]) - expected_value))
    for series in ("Bnormalized", "Dnormalized", "Ynormalized", "anormalized"):
        profile_maxima[series] = max(float(row["value"]) for row in grouped[("B", series)])
    require(float(grouped[("B", "Bnormalized")][0]["value"]) == 0.0, "BEntryZero", checks)
    require(float(grouped[("B", "anormalized")][0]["value"]) == 0.0, "aEntryZero", checks)
    require(float(grouped[("B", "Dnormalized")][0]["value"]) == 1.0, "DInitialNormalization", checks)
    require(float(grouped[("B", "Ynormalized")][0]["value"]) == 1.0, "YInitialNormalization", checks)
    require(profile_maxima["anormalized"] > 4.0, "positiveInteriorPulse", checks)

    gap = 1.0 - 2.0 ** (-1.0 / 9.0)
    ratio_constant = a_star / (32.0 * gap)
    normalized_ratios: list[float] = []
    for index, exponent in enumerate(range(3, 14)):
        frequency = float(2**exponent)
        expected_c = {
            "Zlower": a_star / (64.0 * frequency**2),
            "Hupper": gap / (2.0 * frequency**4),
            "ratioOverK2": ratio_constant,
        }
        for series, expected_value in expected_c.items():
            row = grouped[("C", series)][index]
            value = float(row["value"])
            maximum_sampling_error = max(maximum_sampling_error, abs(float(row["x"]) - frequency))
            maximum_formula_error = max(maximum_formula_error, abs(value - expected_value))
        z_value = float(grouped[("C", "Zlower")][index]["value"])
        h_value = float(grouped[("C", "Hupper")][index]["value"])
        normalized_ratios.append(z_value / h_value / frequency**2)
    require(max(normalized_ratios) - min(normalized_ratios) < 2.0e-20, "exactQuadraticGap", checks)
    z_rows = grouped[("C", "Zlower")]
    h_rows = grouped[("C", "Hupper")]
    require(abs(float(z_rows[-1]["value"]) / float(z_rows[0]["value"]) - (8.0 / 8192.0) ** 2) < 2.0e-21, "ZMinusTwoScaling", checks)
    require(abs(float(h_rows[-1]["value"]) / float(h_rows[0]["value"]) - (8.0 / 8192.0) ** 4) < 2.0e-27, "HMinusFourScaling", checks)

    ledger_expected = {
        "Bgroup": [36.0, -36.0, 0.0],
        "F2group": [328.0, 8.0, 164.0],
        "dgroup": [82.0, 3860.0, 0.0],
    }
    for series, expected_values in ledger_expected.items():
        actual = [float(row["value"]) for row in grouped[("D", series)]]
        require(actual == expected_values, f"ledger_{series}", checks)
    require(sum(ledger_expected["Bgroup"]) == 0.0, "initialBCancellation", checks)
    require(sum(ledger_expected["F2group"]) == 500.0, "initialF2Total", checks)
    require(sum(ledger_expected["dgroup"]) == 3942.0, "initialDTotal", checks)
    radius_rows = grouped[("D", "frameRadius")]
    for row in radius_rows:
        group = int(float(row["x"]))
        channel = int(row["category"].split("=")[1])
        expected_radius = math.sqrt(group * group + channel * channel) / 4.0
        maximum_formula_error = max(maximum_formula_error, abs(float(row["value"]) - expected_radius))
    radii = [float(row["value"]) for row in radius_rows]
    require(min(radii) >= 1.0, "flatTopLowerEdge", checks)
    require(max(radii) <= math.sqrt(2.0), "flatTopUpperEdge", checks)
    require({row["category"] for row in radius_rows} == {"n=4", "n=5"}, "verticalChannels", checks)

    require(maximum_sampling_error < 2.0e-16, "samplingGrid", checks)
    require(maximum_formula_error < 2.0e-15, "formulaAgreement", checks)
    payload = {
        "release": "R0.71J",
        "status": "pass",
        "checks": checks,
        "metrics": {
            "maximumFormulaError": maximum_formula_error,
            "maximumSamplingError": maximum_sampling_error,
            "thetaStar": theta_star,
            "AStar": a_star,
            "positiveCreationAtThetaStar": lhs,
            "positiveIdentityResidual": abs(lhs - rhs),
            "ratioOverK2Nu1": ratio_constant,
            "profileMaxima": profile_maxima,
            "modeLedgerTotals": {"B": 0, "F2": 500, "d": 3942},
            "frameRadiusRange": [min(radii), max(radii)],
        },
        "claimBoundary": (
            "Validates only the parent-only broad-frame, global-cell, heat-height-zero "
            "closed formulas and asymptotic comparison bounds. It does not validate a "
            "finite-K trajectory, matched-cell estimate, face-paid BV theorem, or "
            "regularity conclusion."
        ),
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
