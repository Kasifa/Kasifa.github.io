#!/usr/bin/env python3
"""Generate closed-form source data for the R0.71I volume-gap figure."""

from __future__ import annotations

import argparse
import csv
import json
import math
import platform
import time
from pathlib import Path


FIELDNAMES = (
    "panel",
    "series",
    "x",
    "value",
    "parameter",
    "evidenceClass",
    "formula",
)


def add(
    rows: list[dict[str, str]],
    panel: str,
    series: str,
    x: float,
    value: float,
    parameter: str,
    evidence: str,
    formula: str,
) -> None:
    rows.append(
        {
            "panel": panel,
            "series": series,
            "x": f"{x:.17g}",
            "value": f"{value:.17g}",
            "parameter": parameter,
            "evidenceClass": evidence,
            "formula": formula,
        }
    )


def pulse_value(tau: float) -> float:
    x = math.exp(-2.0 * tau)
    return x * (1.0 - x) ** 2 / (2.0 * (1.0 + x))


def nse_profiles(theta: float) -> tuple[float, float, float, float, float]:
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
    return q_scaled / y_scaled, f_scaled / y_scaled, q_scaled, y_scaled, f_scaled


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("data.csv"))
    parser.add_argument("--metadata", type=Path, default=Path("figure-data-metadata.json"))
    args = parser.parse_args()
    started = time.perf_counter()
    rows: list[dict[str, str]] = []

    pulse_parameter = "A0=diag(K^2,2K^2);F0=(e1-e2)/sqrt(2);C0=(e1+e2)/sqrt(2);Y=1"
    pulse_evidence = "closed-form common-heat Hilbert model; not NSE"
    for index in range(151):
        tau = 3.0 * index / 150.0
        add(
            rows,
            "A",
            "commonHeatPulse",
            tau,
            pulse_value(tau),
            pulse_parameter,
            pulse_evidence,
            "x*(1-x)^2/(2*(1+x));x=exp(-2*tau)",
        )
    x_star = (-3.0 + math.sqrt(17.0)) / 4.0
    tau_star = -0.5 * math.log(x_star)
    # Rationalized forms avoid binary64 cancellation in 71-17*sqrt(17).
    q_star = 8.0 / (71.0 + 17.0 * math.sqrt(17.0))
    add(
        rows,
        "A",
        "pulsePeak",
        tau_star,
        q_star,
        pulse_parameter,
        pulse_evidence,
        "q*=(71-17*sqrt(17))/16",
    )

    ratio_constant = 128.0 / (3.0 * (71.0 + 17.0 * math.sqrt(17.0)))
    for exponent in range(9):
        frequency = float(2**exponent)
        add(
            rows,
            "B",
            "traceVolumeRatio",
            frequency,
            ratio_constant * frequency**2,
            "nu=1;outerWeight=K^-2",
            "exact common-heat trace-to-volume algebra; no fitted exponent",
            "nu*(71-17*sqrt(17))*K^2/3",
        )

    nse_parameter = "fixedEnergy=263/90;theta=nu*K^2*t;radialRingsSquared=5,10"
    nse_evidence = "closed-form C1 fixed-window limit of exact global-smooth 2D3C NSE"
    for index in range(151):
        theta = 0.6 * index / 150.0
        a_zero, g_zero, _, _, _ = nse_profiles(theta)
        add(
            rows,
            "C",
            "A0",
            theta,
            a_zero,
            nse_parameter,
            nse_evidence,
            "A0=4*x*(1-x)^2/((1+x)*Y0);x=exp(-10*theta)",
        )
        add(
            rows,
            "C",
            "G0",
            theta,
            g_zero,
            nse_parameter,
            nse_evidence,
            "G0=4*(exp(-10*theta)+exp(-20*theta))/Y0",
        )
    theta_test = math.log(2.0) / 10.0
    a_test, _, _, _, _ = nse_profiles(theta_test)
    add(
        rows,
        "C",
        "positiveTestPoint",
        theta_test,
        a_test,
        nse_parameter,
        nse_evidence,
        "theta*=log(2)/10;A0(theta*)>0",
    )

    refresh_parameter = "U=1;chi_delta,+/-=(1+/-delta*cos(K*x3))/2"
    refresh_evidence = "exact initial-time Fourier orthogonality on global-smooth 2D3C NSE"
    for index in range(101):
        delta = index / 100.0
        aggregate = 1.0 / (3.0 * delta**2 + 4.0)
        add(
            rows,
            "D",
            "aggregateCoefficient",
            delta,
            aggregate,
            refresh_parameter,
            refresh_evidence,
            "sum_+/- a_delta=U^2/(3*delta^2+4);U=1",
        )
    for delta, value in ((0.0, 0.25), (1.0, 1.0 / 7.0)):
        add(
            rows,
            "D",
            "refreshEndpoint",
            delta,
            value,
            refresh_parameter,
            refresh_evidence,
            "endpoint gap=1/4-1/7=3/28",
        )

    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    metadata = {
        "release": "R0.71I",
        "status": "generated",
        "rows": len(rows),
        "method": "closed-form formula evaluation only",
        "randomSeed": None,
        "dns": False,
        "pdeTimeStepping": False,
        "fittedData": False,
        "parameters": {
            "panelA": {"tauRange": [0.0, 3.0], "samples": 151},
            "panelB": {"viscosity": 1.0, "frequencies": [2**i for i in range(9)]},
            "panelC": {
                "thetaRange": [0.0, 0.6],
                "samples": 151,
                "kineticEnergy": "263/90",
                "radialMultiplierRingsSquared": [5, 10],
                "convergence": "C1([0,M]) for every fixed M",
            },
            "panelD": {"deltaRange": [0.0, 1.0], "samples": 101, "U": 1.0},
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "wallSeconds": time.perf_counter() - started,
        "claimBoundary": (
            "Closed-form common-heat data, a rigorous fixed-window 2D3C NSE limit, "
            "and exact cutoff-refresh algebra only; no DNS, fitting, PDE time stepping, "
            "broad-frame comparison, regularity theorem, singularity claim, originality "
            "claim, or Millennium-problem claim."
        ),
    }
    args.metadata.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
