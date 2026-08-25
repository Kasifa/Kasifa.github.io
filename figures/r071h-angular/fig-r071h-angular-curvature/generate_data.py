#!/usr/bin/env python3
"""Generate the closed-form data for the R0.71H angular-curvature figure."""

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
)


def append_record(
    records: list[dict[str, str]],
    panel: str,
    series: str,
    x: float,
    value: float,
    parameter: str,
    evidence_class: str,
) -> None:
    records.append(
        {
            "panel": panel,
            "series": series,
            "x": f"{x:.17g}",
            "value": f"{value:.17g}",
            "parameter": parameter,
            "evidenceClass": evidence_class,
        }
    )


def heat_records(records: list[dict[str, str]]) -> None:
    """Two-mode pure heat flow with eigenvalues 1 and 4 and nu=1."""

    for index in range(61):
        tau = index / 40.0
        z = math.exp(-6.0 * tau)
        rayleigh = (1.0 + 4.0 * z) / (1.0 + z)
        payment = 2.5 - rayleigh
        angular = 0.5 * payment
        curvature = 0.5 * payment
        identity_sum = angular + curvature
        parameter = "nu=1;lambda1=1;lambda2=4;c1=c2=1"
        evidence = "closed-form pure-heat Hilbert model"
        append_record(records, "A", "rayleighPayment", tau, payment, parameter, evidence)
        append_record(records, "A", "angularIntegral", tau, angular, parameter, evidence)
        append_record(records, "A", "curvatureIntegral", tau, curvature, parameter, evidence)
        append_record(records, "A", "identitySum", tau, identity_sum, parameter, evidence)


def fixed_energy_records(records: list[dict[str, str]]) -> None:
    """Exact t=0 identities for the fixed-energy 2D3C family."""

    for exponent in range(9):
        frequency = float(2**exponent)
        amplitude = 1.0 / frequency
        omega = 0.5 * amplitude * frequency**2
        source_density = 0.25 * amplitude**2 * (3.0 + 2.0 * amplitude) ** 2 * frequency**2
        parameter = "nu=1;kineticEnergy=6;aK=1/K;t=0"
        evidence = "exact initial-time Fourier algebra for global-smooth 2D3C NSE"
        append_record(records, "B", "angularSpeed", frequency, omega, parameter, evidence)
        append_record(records, "B", "sourceDensity", frequency, source_density, parameter, evidence)


def cutoff_records(records: list[dict[str, str]]) -> None:
    """Exact finite-Fourier cutoff quotients for chi=(1+delta cos Z)/2."""

    for index in range(51):
        delta = index / 50.0
        square = delta * delta
        rayleigh = 2.0 * (3.0 * square + 2.0) / (3.0 * square + 4.0)
        projective = 12.0 * square / (3.0 * square + 4.0) ** 2
        parameter = "chi_delta=(1+delta*cos(Z))/2;0<=delta<=1"
        evidence = "closed-form finite-Fourier orthogonality"
        append_record(records, "C", "rayleighQuotient", delta, rayleigh, parameter, evidence)
        append_record(records, "C", "projectiveSource", delta, projective, parameter, evidence)


def scaling_records(records: list[dict[str, str]]) -> None:
    """Exact shell-weight comparison in the direct weighted-BV Young bound."""

    for exponent in range(9):
        frequency = float(2**exponent)
        known_weight = frequency ** (-2.0)
        required_weight = 1.0
        gap_ratio = frequency**2
        parameter = "outerBVWeight=K^-2;dimensionlessCurvatureRate=1"
        evidence = "exact scaling bookkeeping; no fitted exponent"
        append_record(records, "D", "knownHeatWeight", frequency, known_weight, parameter, evidence)
        append_record(records, "D", "directRequiredWeight", frequency, required_weight, parameter, evidence)
        append_record(records, "D", "gapRatio", frequency, gap_ratio, parameter, evidence)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("data.csv"))
    parser.add_argument(
        "--metadata", type=Path, default=Path("figure-data-metadata.json")
    )
    args = parser.parse_args()
    started = time.perf_counter()

    records: list[dict[str, str]] = []
    heat_records(records)
    fixed_energy_records(records)
    cutoff_records(records)
    scaling_records(records)

    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)

    metadata = {
        "release": "R0.71H",
        "status": "generated",
        "rows": len(records),
        "method": "closed-form formula evaluation only",
        "randomSeed": None,
        "dns": False,
        "pdeTimeStepping": False,
        "fittedData": False,
        "parameters": {
            "panelA": {
                "viscosity": 1.0,
                "eigenvalues": [1.0, 4.0],
                "initialCoefficients": [1.0, 1.0],
                "timeRange": [0.0, 1.5],
                "samples": 61,
            },
            "panelB": {
                "viscosity": 1.0,
                "kineticEnergy": 6.0,
                "amplitude": "1/K",
                "time": 0.0,
                "frequencies": [2**index for index in range(9)],
            },
            "panelC": {
                "cutoff": "(1+delta*cos(Z))/2",
                "deltaRange": [0.0, 1.0],
                "samples": 51,
            },
            "panelD": {
                "frequencies": [2**index for index in range(9)],
                "knownWeight": "K^-2",
                "directRequiredWeight": "1",
                "gapRatio": "K^2",
            },
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "wallSeconds": time.perf_counter() - started,
        "claimBoundary": (
            "Closed-form identities, exact initial-time Fourier algebra, and scaling comparison only; "
            "no DNS, fitting, time-evolved 3D simulation, regularity theorem, singularity claim, "
            "originality claim, or Millennium-problem claim."
        ),
    }
    args.metadata.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
