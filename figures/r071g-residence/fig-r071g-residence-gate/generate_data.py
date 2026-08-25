#!/usr/bin/env python3
"""Generate the finite and exact data used by the R0.71G formal figure.

The sideband profiles use a fixed-step complex RK4 method at |m| <= 24.
They are finite checks of the exact 2D3C chain.  The arbitrary-duration theorem
is analytic and does not depend on extrapolating these samples.
"""

from __future__ import annotations

import argparse
import csv
import json
import platform
import time
from pathlib import Path

import numpy as np


RADIUS = 24
STEP = 0.00025
FINAL_TIME = 10.5
PROFILE_STEP = 0.02
MUS = (1.0, 0.5, 0.2, 0.1, 0.05)
LEVELS = (0.5, 0.1, 0.01)


def rhs(theta: float, values: np.ndarray, modes: np.ndarray, mu: float):
    left = np.concatenate(([0.0j], values[:-1]))
    right = np.concatenate((values[1:], [0.0j]))
    return -(modes**2 + 1.0) * values + 1.0j * mu * np.exp(-theta) * (left + right)


def rk4_step(theta, values, modes, mu):
    k1 = rhs(theta, values, modes, mu)
    k2 = rhs(theta + STEP / 2.0, values + STEP * k1 / 2.0, modes, mu)
    k3 = rhs(theta + STEP / 2.0, values + STEP * k2 / 2.0, modes, mu)
    k4 = rhs(theta + STEP, values + STEP * k3, modes, mu)
    return values + STEP * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0


def observables(theta: float, values: np.ndarray):
    center = RADIUS
    ell = 1.0j * np.exp(-theta) * (values[center - 1] + values[center + 1])
    h = float(np.real(np.conjugate(values[center]) * ell))
    g = float(abs(values[center]) ** 2 + np.exp(-2.0 * theta))
    q_relative = 2.0 * max(h, 0.0) ** 2 / g
    return h, g, q_relative


def interpolate_crossing(theta0, value0, theta1, value1, target=0.0):
    fraction = (value0 - target) / (value0 - value1)
    return theta0 + fraction * (theta1 - theta0)


def integrate_case(mu: float):
    modes = np.arange(-RADIUS, RADIUS + 1, dtype=float)
    values = np.zeros(2 * RADIUS + 1, dtype=complex)
    values[RADIUS] = -1.0
    values[RADIUS + 1] = 1.0j
    profile_every = int(round(PROFILE_STEP / STEP))
    total_steps = int(round(FINAL_TIME / STEP))
    rows = []
    exits = {"sign": None, **{f"q:{level}": None for level in LEVELS}}
    maximum_boundary_mass = 0.0

    theta = 0.0
    previous_h, _previous_g, previous_q = observables(theta, values)
    rows.append((theta, previous_h, previous_q))
    for index in range(1, total_steps + 1):
        next_values = rk4_step(theta, values, modes, mu)
        next_theta = index * STEP
        h, _g, q_relative = observables(next_theta, next_values)
        if exits["sign"] is None and previous_h > 0.0 >= h:
            exits["sign"] = interpolate_crossing(theta, previous_h, next_theta, h)
        for level in LEVELS:
            key = f"q:{level}"
            if exits[key] is None and previous_q > level >= q_relative:
                exits[key] = interpolate_crossing(
                    theta, previous_q, next_theta, q_relative, level
                )
        maximum_boundary_mass = max(
            maximum_boundary_mass,
            float(np.sum(np.abs(next_values[[0, 1, -2, -1]]) ** 2)),
        )
        if index % profile_every == 0:
            rows.append((next_theta, h, q_relative))
        theta = next_theta
        values = next_values
        previous_h = h
        previous_q = q_relative

    if any(value is None for value in exits.values()):
        raise RuntimeError(f"missing event for mu={mu}: {exits}")
    return rows, exits, maximum_boundary_mass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("data.csv"))
    parser.add_argument(
        "--metadata", type=Path, default=Path("figure-data-metadata.json")
    )
    args = parser.parse_args()
    started = time.perf_counter()
    records = []
    event_summary = {}
    boundary_summary = {}

    for mu in MUS:
        rows, exits, boundary_mass = integrate_case(mu)
        event_summary[str(mu)] = exits
        boundary_summary[str(mu)] = boundary_mass
        for theta, h, q_relative in rows:
            records.append(
                {
                    "recordType": "profile",
                    "mu": mu,
                    "theta": theta,
                    "value": h,
                    "aux": np.exp(4.0 * theta) * h,
                    "level": "H",
                }
            )
            records.append(
                {
                    "recordType": "profile",
                    "mu": mu,
                    "theta": theta,
                    "value": q_relative,
                    "aux": np.nan,
                    "level": "qRelative",
                }
            )
        records.append(
            {
                "recordType": "signExit",
                "mu": mu,
                "theta": exits["sign"],
                "value": exits["sign"],
                "aux": 1.0 / mu,
                "level": "0",
            }
        )
        for level in LEVELS:
            records.append(
                {
                    "recordType": "qExit",
                    "mu": mu,
                    "theta": exits[f"q:{level}"],
                    "value": exits[f"q:{level}"],
                    "aux": -np.log(level) / 6.0,
                    "level": str(level),
                }
            )

    for n in range(1, 13):
        records.append(
            {
                "recordType": "functional",
                "mu": np.nan,
                "theta": n,
                "value": n,
                "aux": (4.0**n - 1.0) / (3.0 * 4.0**n),
                "level": "partialSums",
            }
        )

    fieldnames = ["recordType", "mu", "theta", "value", "aux", "level"]
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for record in records:
            writer.writerow(
                {
                    key: (
                        f"{record[key]:.16e}"
                        if isinstance(record[key], (float, np.floating))
                        else record[key]
                    )
                    for key in fieldnames
                }
            )

    metadata = {
        "release": "R0.71G",
        "status": "generated",
        "rows": len(records),
        "method": "fixed-step complex RK4 on the exact 2D3C sideband chain plus closed-form functional partial sums",
        "chain": {
            "radius": RADIUS,
            "step": STEP,
            "finalTime": FINAL_TIME,
            "profileStep": PROFILE_STEP,
            "muValues": list(MUS),
            "relativeQLevels": list(LEVELS),
            "events": event_summary,
            "maximumOuterTwoModeMass": boundary_summary,
        },
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "platform": platform.platform(),
        },
        "randomSeed": None,
        "dns": False,
        "pdeTimeStepping": False,
        "wallSeconds": time.perf_counter() - started,
        "claimBoundary": (
            "Finite integration of the exact reduced chain; arbitrary-duration sign residence is proved analytically, not numerically."
        ),
    }
    args.metadata.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
