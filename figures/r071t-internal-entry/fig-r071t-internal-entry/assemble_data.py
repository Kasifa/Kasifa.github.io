#!/usr/bin/env python3
"""Assemble the plotting table from the two R0.71T Galerkin solvers."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from time import perf_counter


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add(
    rows: list[dict[str, object]],
    panel: str,
    series: str,
    case: str,
    grid_order: object,
    cutoff: object,
    x: float,
    y: float,
    unit: str,
    formula: str,
    evidence: str,
    note: str,
) -> None:
    rows.append({
        "panel": panel,
        "series": series,
        "case": case,
        "N": grid_order,
        "Kcut": cutoff,
        "x": x,
        "y": y,
        "value": y,
        "unit": unit,
        "formula": formula,
        "evidenceClass": evidence,
        "note": note,
    })


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--producer", type=Path, required=True)
    parser.add_argument("--independent", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    args = parser.parse_args()
    started = perf_counter()
    producer = json.loads(args.producer.read_text(encoding="utf-8"))
    independent = json.loads(args.independent.read_text(encoding="utf-8"))
    if producer["release"] != independent["release"] or producer["release"] != "R0.71T":
        raise AssertionError("R0.71T inputs required")
    if producer["status"] != independent["status"] or producer["status"] != "passed":
        raise AssertionError("both numerical inputs must pass")
    model = producer["model"]
    rows: list[dict[str, object]] = []

    for run in producer["tauRuns"]:
        add(
            rows,
            "A",
            "primary precompensation ratio",
            "pseudo-spectral",
            model["gridOrder"],
            model["cutoff"],
            float(run["tau"]),
            float(run["precompensationRatio"]),
            "dimensionless",
            "||z_tau||/(tau*||P_*F(u_*)||_2)",
            "finite Fourier--Galerkin shooting",
            "ratio tends to one as tau decreases",
        )
    refined = next(run for run in independent["runs"] if run["cutoff"] == 3)
    add(
        rows,
        "A",
        "independent refined check",
        "direct convolution",
        refined["gridOrder"],
        refined["cutoff"],
        float(refined["tau"]),
        float(refined["precompensationRatio"]),
        "dimensionless",
        "||z_tau||/(tau*||P_*F(u_*)||_2)",
        "independent finite Fourier--Galerkin shooting",
        "N=12,Kcut=3 direct-convolution validation point",
    )

    for sample in producer["trajectory"]["samples"]:
        add(
            rows,
            "B",
            "signed principal coefficient",
            "tau=0.04",
            model["gridOrder"],
            model["cutoff"],
            float(sample["timeOverTau"]),
            float(sample["principalNormalized"]),
            "normalized target coefficient",
            "<P_*u(t),e_tau>/(tau*||P_*F(u_*)||_2)",
            "finite Fourier--Galerkin trajectory",
            "event direction e_tau is the normalized target forcing at t=tau",
        )
        add(
            rows,
            "B",
            "transverse target norm",
            "tau=0.04",
            model["gridOrder"],
            model["cutoff"],
            float(sample["timeOverTau"]),
            float(sample["transverseNormalized"]),
            "normalized target coefficient",
            "||P_*u-<P_*u,e_tau>e_tau||/(tau*||P_*F(u_*)||_2)",
            "finite Fourier--Galerkin trajectory",
            "nonnegative transverse residual in the eight-real-dimensional shell",
        )

    for run in producer["tauRuns"]:
        for series, value, formula in (
            (
                "entry atom A+",
                run["APlus"],
                "||P_*F(u(tau))||_2^2/Y(tau)",
            ),
            (
                "slope-charge reconstruction",
                run["slopeCharge"],
                "||C_t(tau)||_2^2/(rho^4*Y(tau)), rho^2=2",
            ),
            ("small-time limit 1/4", 0.25, "||P_*F(u_*)||_2^2/Y(0)=1/4"),
        ):
            add(
                rows,
                "C",
                series,
                "pseudo-spectral",
                model["gridOrder"],
                model["cutoff"],
                float(run["tau"]),
                float(value),
                "normalized atom",
                formula,
                "finite Fourier--Galerkin shooting" if "limit" not in series else "exact seed reference",
                "simple positive-time target-shell entry",
            )
    add(
        rows,
        "C",
        "independent refined A+",
        "direct convolution",
        refined["gridOrder"],
        refined["cutoff"],
        float(refined["tau"]),
        float(refined["APlus"]),
        "normalized atom",
        "||P_*F(u(tau))||_2^2/Y(tau)",
        "independent finite Fourier--Galerkin shooting",
        "N=12,Kcut=3 direct-convolution validation point",
    )

    viscosity = float(model["viscosity"])
    tau = 0.04
    atom_coefficient = math.exp(-2.0 * viscosity * tau) / 4.0
    budget_coefficient = (
        1.0 - math.exp(-4.0 * viscosity * tau)
    ) / (16.0 * viscosity)
    for frequency in (1, 2, 4, 8, 16, 32, 64):
        atom = atom_coefficient * frequency**-4
        budget = budget_coefficient * frequency**-6
        ratio = atom / budget
        for series, value, unit, formula in (
            ("leading internal atom", atom, "leading scale", "exp(-2nu*tau)/(4*lambda^4)"),
            ("leading bare budget", budget, "leading scale", "(1-exp(-4nu*tau))/(16nu*lambda^6)"),
            ("atom-to-budget ratio", ratio, "dimensionless ratio", "2nu*lambda^2/sinh(2nu*tau)"),
        ):
            add(
                rows,
                "D",
                series,
                "tau=0.04,nu=1",
                "",
                "",
                float(frequency),
                float(value),
                unit,
                formula,
                "exact leading small-amplitude and NSE-dilation ledger",
                "a_lambda=lambda^-2 before integer NSE dilation",
            )

    fields = [
        "panel", "series", "case", "N", "Kcut", "x", "y", "value",
        "unit", "formula", "evidenceClass", "note",
    ]
    with args.output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    metadata = {
        "release": "R0.71T",
        "rows": len(rows),
        "generationWallSeconds": perf_counter() - started,
        "producerSha256": digest(args.producer),
        "independentSha256": digest(args.independent),
        "evidenceMap": {
            "A": "primary pseudo-spectral Galerkin shooting plus one refined direct-convolution point",
            "B": "primary finite Galerkin trajectory through the shot internal zero",
            "C": "finite Galerkin entry atom and algebraically identical slope charge",
            "D": "exact leading two-parameter scaling ledger, not fitted slopes",
        },
        "primaryConfiguration": {
            "gridOrder": model["gridOrder"],
            "cutoff": model["cutoff"],
            "viscosity": model["viscosity"],
            "tauValues": [run["tau"] for run in producer["tauRuns"]],
        },
        "independentConfiguration": {
            "gridOrder": refined["gridOrder"],
            "cutoff": refined["cutoff"],
            "tau": refined["tau"],
        },
        "finiteGalerkin": True,
        "pdeTimeStepping": True,
        "dns": False,
        "fittedData": False,
        "intervalCertified": False,
        "claimBoundary": (
            "Panels A--C are finite Fourier--Galerkin corroboration in the "
            "x3-independent three-component invariant sector. Panel D is an "
            "exact leading asymptotic ledger. The figure gives no continuum "
            "Galerkin error bound, DNS claim, Leray occupation bound, repeated-"
            "entry packing, singularity, continuation, or regularity theorem."
        ),
    }
    args.metadata.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
