#!/usr/bin/env python3
"""Generate deterministic source data for the R0.71K formal figure."""

from __future__ import annotations

import argparse
import csv
import json
import math
import platform
import time
from pathlib import Path


FIELDS = ("panel", "series", "x", "value", "category", "formula", "evidenceClass")
RADIUS = 1.5 * math.pi


def bump(value: float) -> float:
    if abs(value) >= RADIUS:
        return 0.0
    return math.exp(-1.0 / (1.0 - (value / RADIUS) ** 2))


def atom(value: float) -> float:
    denominator = sum(bump(value - 2.0 * math.pi * shift) for shift in range(-3, 4))
    return bump(value) / denominator


def amplitude(theta: float) -> float:
    exponential = lambda power: math.exp(-power * theta)
    b_value = 4.0 * (exponential(34.0) - exponential(52.0))
    d_value = (
        32.0 * exponential(32.0)
        + 1156.0 * exponential(34.0)
        + 50.0 * exponential(50.0)
        + 2704.0 * exponential(52.0)
    )
    y_value = (
        2.0 * exponential(2.0)
        + 2.0 * exponential(32.0)
        + 68.0 * exponential(34.0)
        + 2.0 * exponential(50.0)
        + 104.0 * exponential(52.0)
    )
    return 0.0 if b_value == 0.0 else b_value**2 / (d_value * y_value)


def add(rows, panel, series, x, value, category, formula, evidence):
    rows.append({
        "panel": panel,
        "series": series,
        "x": f"{x:.17g}",
        "value": f"{value:.17g}",
        "category": category,
        "formula": formula,
        "evidenceClass": evidence,
    })


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("data.csv"))
    parser.add_argument("--metadata", type=Path, default=Path("figure-data-metadata.json"))
    args = parser.parse_args()
    started = time.perf_counter()
    rows = []

    for index in range(301):
        x_value = -math.pi + 2.0 * math.pi * index / 300.0
        values = {
            "leftAtom": atom(x_value + 2.0 * math.pi),
            "centerAtom": atom(x_value),
            "rightAtom": atom(x_value - 2.0 * math.pi),
        }
        values["partitionSum"] = sum(values.values())
        for series, value in values.items():
            add(rows, "A", series, x_value, value, "partition profile", "translated h atom", "explicit C-infinity partition")

    theta_star = math.log(2.0) / 18.0
    a_star = amplitude(theta_star)
    for index in range(241):
        theta = 0.12 * index / 240.0
        add(rows, "B", "globalAmplitude", theta, amplitude(theta) / a_star, "closed profile", "A0(theta)/A*", "pure-heat fixed-window formula")
    add(rows, "B", "globalEndpoint", theta_star, 1.0, "endpoint", "A0(theta*)/A*", "exact closed endpoint")
    add(rows, "B", "localTemplateEndpoint", theta_star, 1.6511660824611684e-5 / a_star, "diagnostic endpoint", "independent local template amplitude/A*", "independent one-cell quadrature")

    for exponent in range(3, 14):
        frequency = float(2**exponent)
        add(rows, "C", "creationPower", frequency, frequency**-2, "normalized bound", "K^-2", "exact exponent")
        add(rows, "C", "heatPower", frequency, frequency**-4, "normalized bound", "K^-4", "exact exponent")

    exponents = [
        ("B_Q", 0.0, "per cell"),
        ("d_Q", 1.0, "per cell"),
        ("q_Q", -1.0, "per cell"),
        ("a_Q", -3.0, "per cell"),
        ("Z_loc", -2.0, "all cells"),
        ("H_loc", -4.0, "all cells"),
        ("collar", -2.0, "all cells"),
        ("Z/H", 2.0, "ratio"),
    ]
    for index, (label, value, category) in enumerate(exponents):
        add(rows, "D", "scalingExponent", float(index), value, label, f"{label} scales as K^{value:g}", category)

    args.output.write_text("", encoding="utf-8")
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    metadata = {
        "release": "R0.71K",
        "rows": len(rows),
        "series": sorted({(row["panel"], row["series"]) for row in rows}),
        "thetaStar": theta_star,
        "AStar": a_star,
        "partitionRadius": RADIUS,
        "partitionOverlap3D": 8,
        "localTemplateEndpoint": 1.6511660824611684e-5,
        "precision": "IEEE binary64",
        "python": platform.python_version(),
        "randomSeed": None,
        "dns": False,
        "pdeTimeStepping": False,
        "fittedData": False,
        "wallTimeSeconds": time.perf_counter() - started,
        "claimBoundary": "One fixed aligned matched partition; collar-paid closure and general partitions remain open.",
    }
    args.metadata.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
