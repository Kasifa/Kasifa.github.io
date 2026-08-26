#!/usr/bin/env python3
"""Producer-side scientific validation for Figure R0.71U."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np


def cpair(values: list[float]) -> complex:
    return complex(float(values[0]), float(values[1]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--primary", type=Path, required=True)
    parser.add_argument("--independent", type=Path, required=True)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    primary = json.loads(args.primary.read_text(encoding="utf-8"))
    independent = json.loads(args.independent.read_text(encoding="utf-8"))
    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    data_rows = list(csv.DictReader(args.data.open(encoding="utf-8")))
    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool, observed: object, criterion: str) -> None:
        checks.append({
            "name": name,
            "passed": bool(passed),
            "observed": observed,
            "criterion": criterion,
        })

    classification = config["classification"]
    check(
        "numerical classification",
        classification == {
            "finiteGalerkin": True,
            "pdeTimeStepping": True,
            "dns": False,
            "analyticProofFromNumerics": False,
        },
        classification,
        "finiteGalerkin=true, pdeTimeStepping=true, dns=false, analyticProofFromNumerics=false",
    )
    check(
        "PDE divergence reduction",
        primary["pdeReduction"]["divergence"] == "partial_x f + partial_z v = 0",
        primary["pdeReduction"],
        "u=(f(y,z),0,v(y)) has div u=0",
    )
    check(
        "PDE nonlinear reduction",
        primary["pdeReduction"]["advection"] == "(u dot grad)u=(v f_z,0,0)",
        primary["pdeReduction"]["advection"],
        "the only advective component is v f_z",
    )
    expected_formula = "a_m'=-nu[(K+dm)^2+L^2]a_m-iL sum_l p_l exp(-nu(dl)^2t)(a_(m-l)+a_(m+l))"
    check(
        "lattice ODE formula",
        primary["latticeFormula"] == expected_formula,
        primary["latticeFormula"],
        "diagonal heat decay plus both modular shifts",
    )
    check(
        "fixed numerical problem",
        (
            float(config["viscosity"]) == 0.02
            and int(config["K"]) == 1
            and int(config["L"]) == 1
            and int(config["modulus"]) == 8
            and list(config["targetTimes"]) == [0.01, 0.03, 0.07]
            and int(config["primaryCutoff"]) == 24
            and int(config["independentCutoff"]) == 36
        ),
        {
            key: config[key]
            for key in ("viscosity", "K", "L", "modulus", "targetTimes", "primaryCutoff", "independentCutoff")
        },
        "matches the declared R0.71U corroboration instance",
    )
    parameters = np.asarray(primary["main"]["parameters"], dtype=float)
    check(
        "real shooting parameters and fixed p1",
        parameters.shape == (7,) and np.all(np.isfinite(parameters)) and parameters[0] == 0.002,
        parameters.tolist(),
        "seven finite real numbers with p1=0.002",
    )
    linear = primary["linearAudits"]["p1=0.002"]
    check(
        "analytic response Jacobian rank",
        int(linear["jacobianRank"]) == 6,
        linear,
        "the six free-parameter response matrix has rank six",
    )
    maximum_residual = float(primary["main"]["shooting"]["targetResidualMaximum"])
    check(
        "primary prescribed-time target residual",
        maximum_residual < 1e-16,
        maximum_residual,
        "max |a_0(t_m)| < 1e-16",
    )
    slopes = np.asarray([cpair(item["slope"]) for item in primary["main"]["events"]])
    minimum_slope = float(np.min(np.abs(slopes)))
    check(
        "three nonzero slopes",
        len(slopes) == 3 and minimum_slope > 1e-6,
        {"minimum": minimum_slope, "values": [[z.real, z.imag] for z in slopes]},
        "three slopes and min |a_0'(t_m)| > 1e-6",
    )
    pairings = [float(item["positivePairing"]) for item in primary["main"]["events"]]
    check(
        "positive entry pairing",
        all(value > 0.0 for value in pairings),
        pairings,
        "rho^2 ||F_*||_2^2 is positive at every root",
    )

    trace = primary["main"]["trace"]
    trace_times = np.asarray([float(item["time"]) for item in trace])
    trace_values = np.asarray([complex(float(item["real"]), float(item["imag"])) for item in trace])
    crossing_margins: list[float] = []
    for event, slope in zip(primary["main"]["events"], slopes, strict=True):
        time = float(event["time"])
        left = trace_values[np.argmin(np.abs(trace_times - (time - 0.0005)))]
        right = trace_values[np.argmin(np.abs(trace_times - (time + 0.0005)))]
        crossing_margins.append(float(np.real(np.conjugate(slope) * (right - left))))
    check(
        "directed complex passages",
        all(value > 0.0 for value in crossing_margins),
        crossing_margins,
        "projection of the local increment onto the root slope is positive",
    )

    d = int(config["modulus"])
    K = int(config["K"])
    L = int(config["L"])
    radius = float(config["annulusSupportRadius"])
    check(
        "analytic modular gap inequality",
        d > radius + abs(K),
        {"d": d, "RstarPlusAbsK": radius + abs(K)},
        "d > R_* + |K|",
    )
    support: set[tuple[int, int]] = set()
    for r in range(-12, 13):
        support.add((K + d * r, L))
        support.add((-K + d * r, -L))
        support.add((d * r, 0))
    inside = sorted(
        (q, z) for q, z in support
        if q * q + z * z > 0 and math.hypot(q, z) <= radius
    )
    check(
        "full-annulus modular isolation",
        inside == [(-1, -1), (1, 1)],
        inside,
        "the invariant support meets |k|<=R_* only at the conjugate target pair",
    )
    outside_radii = sorted(
        math.hypot(q, z) for q, z in support
        if (q, z) not in {(-1, -1), (1, 1)} and q * q + z * z > 0
    )
    check(
        "nearest modular sideband",
        abs(outside_radii[0] - math.sqrt(50.0)) < 1e-14,
        outside_radii[0],
        "nearest non-target radius is sqrt(50)",
    )

    atom_errors: list[float] = []
    first_jet_errors: list[float] = []
    ratio_errors: list[float] = []
    for event in primary["main"]["events"]:
        slope = cpair(event["slope"])
        enstrophy = float(event["enstrophy"])
        atom_expected = 2.0 * abs(slope) ** 2 / enstrophy
        first_jet_expected = 8.0 * abs(slope) ** 2 / enstrophy
        atom_errors.append(abs(float(event["jetAtom"]) - atom_expected) / atom_expected)
        first_jet_errors.append(abs(float(event["firstJetTrace"]) - first_jet_expected) / first_jet_expected)
        ratio_errors.append(abs(float(event["atomToFirstJetTraceRatio"]) - 0.25))
    check(
        "single-shell atom formula",
        max(atom_errors) < 2e-15,
        max(atom_errors),
        "J=2|a_0'|^2/Y for kappa=m_*=1",
    )
    check(
        "first-jet trace formula",
        max(first_jet_errors) < 2e-15,
        max(first_jet_errors),
        "kappa^-6 ||C_t||_2^2/Y=8|a_0'|^2/Y because rho^2=2",
    )
    check(
        "atom-to-first-jet identity",
        max(ratio_errors) < 2e-15,
        max(ratio_errors),
        "J/P=1/4",
    )
    atoms = [float(item["jetAtom"]) for item in primary["main"]["events"]]
    check(
        "three positive jet atoms",
        len(atoms) == 3 and min(atoms) > 0.0,
        atoms,
        "one strictly positive atom at each prescribed root",
    )
    exponents = [float(item["logLogExponent"]) for item in primary["scalingFits"]]
    check(
        "quadratic small-curve sampling",
        all(abs(value - 2.0) < 0.02 for value in exponents),
        exponents,
        "each sampled log-log exponent is within 0.02 of two",
    )

    by_cutoff = {int(item["cutoff"]): item for item in primary["cutoffSweep"]}
    check(
        "cutoff target convergence",
        float(by_cutoff[24]["maximumTargetDifferenceToM36"]) < 1e-17,
        float(by_cutoff[24]["maximumTargetDifferenceToM36"]),
        "mcut=24 versus 36 target difference < 1e-17",
    )
    check(
        "cutoff slope convergence",
        float(by_cutoff[24]["maximumRelativeSlopeDifferenceToM36"]) < 1e-10,
        float(by_cutoff[24]["maximumRelativeSlopeDifferenceToM36"]),
        "mcut=24 versus 36 maximum relative slope difference < 1e-10",
    )
    check(
        "boundary-tail decay",
        float(by_cutoff[24]["maximumBoundaryCoefficient"]) < 1e-16,
        float(by_cutoff[24]["maximumBoundaryCoefficient"]),
        "mcut=24 boundary coefficients < 1e-16",
    )
    check(
        "independent reshooting residual",
        bool(independent["shooting"]["success"])
        and float(independent["shooting"]["targetResidualMaximum"]) < 1e-16,
        independent["shooting"],
        "independent mcut=36 shoot converges with residual < 1e-16",
    )
    check(
        "independent parameter agreement",
        float(independent["maximumParameterAbsoluteDifference"]) < 1e-12,
        float(independent["maximumParameterAbsoluteDifference"]),
        "max absolute parameter difference < 1e-12",
    )
    check(
        "independent slope agreement",
        float(independent["maximumSlopeRelativeDifferenceFromPrimary"]) < 1e-9,
        float(independent["maximumSlopeRelativeDifferenceFromPrimary"]),
        "max relative slope difference < 1e-9",
    )
    grid_check = independent["pdeReductionGridCheck"]
    grid_residual = max(
        float(value) for key, value in grid_check.items() if "Residual" in key
    )
    check(
        "independent PDE reduction sample",
        grid_residual < 1e-14,
        grid_check,
        "deterministic pointwise reduction residuals < 1e-14",
    )
    check(
        "plot data row count",
        len(data_rows) == int(metadata["rowCount"]) and len(data_rows) > 3000,
        {"csv": len(data_rows), "metadata": metadata["rowCount"]},
        "CSV and metadata row counts agree and include dense traces",
    )
    panel_counts = {
        panel: sum(row["panel"] == panel for row in data_rows)
        for panel in ("A", "B", "C", "D")
    }
    check(
        "all four panels populated",
        all(value > 0 for value in panel_counts.values()),
        panel_counts,
        "panels A-D all have data rows",
    )
    check(
        "claim boundary retained",
        "not inferred from this plot" in metadata["claimBoundary"]
        and "finite Fourier-lattice" in metadata["claimBoundary"],
        metadata["claimBoundary"],
        "metadata distinguishes numerical corroboration from analytic proof",
    )

    failed = [item for item in checks if not item["passed"]]
    payload = {
        "release": config["release"],
        "method": "producer-side formula, residual, slope, atom, modular-gap, cutoff, provenance, and boundary checks",
        "passed": not failed,
        "checkCount": len(checks),
        "failedCount": len(failed),
        "checks": checks,
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if failed:
        raise SystemExit("failed checks: " + ", ".join(item["name"] for item in failed))


if __name__ == "__main__":
    main()
