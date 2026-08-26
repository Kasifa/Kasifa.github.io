#!/usr/bin/env python3
"""Assemble plot-ready rows and provenance metadata for Figure R0.71U."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


FIELDS = [
    "panel",
    "series",
    "case",
    "x",
    "y",
    "time",
    "p1",
    "cutoff",
    "value",
    "unit",
    "formula",
    "evidenceClass",
    "note",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row(
    panel: str,
    series: str,
    case: str,
    x: float,
    y: float,
    *,
    time: float | str = "",
    p1: float | str = "",
    cutoff: int | str = "",
    value: float | str = "",
    unit: str,
    formula: str,
    evidence: str,
    note: str,
) -> dict[str, object]:
    return {
        "panel": panel,
        "series": series,
        "case": case,
        "x": f"{x:.17g}",
        "y": f"{y:.17g}",
        "time": "" if time == "" else f"{float(time):.17g}",
        "p1": "" if p1 == "" else f"{float(p1):.17g}",
        "cutoff": cutoff,
        "value": "" if value == "" else f"{float(value):.17g}",
        "unit": unit,
        "formula": formula,
        "evidenceClass": evidence,
        "note": note,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--primary", type=Path, required=True)
    parser.add_argument("--independent", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    args = parser.parse_args()
    primary = json.loads(args.primary.read_text(encoding="utf-8"))
    independent = json.loads(args.independent.read_text(encoding="utf-8"))
    config = json.loads(args.config.read_text(encoding="utf-8"))
    rows: list[dict[str, object]] = []

    for item in primary["main"]["trace"]:
        time = float(item["time"])
        rows.append(row(
            "A", "real target", "mcut=24", time, float(item["real"]),
            time=time, unit="Fourier coefficient",
            formula="Re a_0(t)", evidence="finite Galerkin",
            note="primary vectorized lattice trace",
        ))
        rows.append(row(
            "A", "imaginary target", "mcut=24", time, float(item["imag"]),
            time=time, unit="Fourier coefficient",
            formula="Im a_0(t)", evidence="finite Galerkin",
            note="primary vectorized lattice trace",
        ))

    root_window = 0.004
    for event_index, event in enumerate(primary["main"]["events"], start=1):
        target_time = float(event["time"])
        rows.append(row(
            "A", "prescribed root", f"t{event_index}", target_time,
            float(event["target"][0]), time=target_time,
            value=float(event["slopeMagnitude"]), unit="Fourier coefficient",
            formula="a_0(t_m)=0; value column stores |partial_t a_0(t_m)|",
            evidence="finite Galerkin", note="solver-enforced prescribed-time root",
        ))
        for trace in primary["main"]["trace"]:
            time = float(trace["time"])
            if abs(time - target_time) <= root_window + 1e-15:
                rows.append(row(
                    "B", "complex passage", f"t{event_index}",
                    float(trace["real"]), float(trace["imag"]), time=time,
                    value=time - target_time, unit="Fourier coefficient",
                    formula="(Re a_0(t), Im a_0(t))",
                    evidence="finite Galerkin",
                    note=f"local window |t-t{event_index}| <= {root_window}",
                ))
        rows.append(row(
            "B", "complex root", f"t{event_index}",
            float(event["target"][0]), float(event["target"][1]), time=target_time,
            value=float(event["slopeMagnitude"]), unit="Fourier coefficient",
            formula="a_0(t_m)=0",
            evidence="finite Galerkin", note="nonzero slope stored in value column",
        ))

    for sweep_case in primary["parameterSweep"]:
        p1 = float(sweep_case["p1"])
        for event_index, event in enumerate(sweep_case["events"], start=1):
            time = float(event["time"])
            atom = float(event["jetAtom"])
            first_jet_quarter = 0.25 * float(event["firstJetTrace"])
            rows.append(row(
                "C", "jet atom", f"t{event_index}", p1, atom,
                time=time, p1=p1, value=atom / p1**2, unit="dimensionless",
                formula="J=kappa^-2 2|a_0'|^2/Y",
                evidence="finite Galerkin plus exact one-shell identity",
                note="value column stores J/p1^2",
            ))
            rows.append(row(
                "C", "quarter first-jet trace", f"t{event_index}", p1, first_jet_quarter,
                time=time, p1=p1, value=float(event["firstJetTrace"]),
                unit="dimensionless",
                formula="(1/4) kappa^-6 ||C_t||_2^2/Y",
                evidence="finite Galerkin plus exact one-shell identity",
                note="rho^2=2 kappa^2, hence J is one quarter of the first-jet trace P",
            ))

    for item in primary["cutoffSweep"]:
        cutoff = int(item["cutoff"])
        rows.append(row(
            "D", "prescribed-time residual", f"mcut={cutoff}",
            cutoff, float(item["maximumTargetResidual"]), cutoff=cutoff,
            value=float(item["maximumTargetDifferenceToM36"]),
            unit="Fourier coefficient",
            formula="max_m |a_0(t_m)|",
            evidence="finite Galerkin cutoff sweep",
            note="same mcut=24-shot parameters; value column stores difference to mcut=36",
        ))
        rows.append(row(
            "D", "slope relative error", f"mcut={cutoff}",
            cutoff, float(item["maximumRelativeSlopeDifferenceToM36"]), cutoff=cutoff,
            value=float(item["maximumBoundaryCoefficient"]), unit="relative",
            formula="max_m |a_0'(mcut)-a_0'(36)|/|a_0'(36)|",
            evidence="finite Galerkin cutoff sweep",
            note="value column stores maximum boundary coefficient",
        ))
    rows.append(row(
        "D", "independent root residual", "sparse mcut=36", 36,
        float(independent["shooting"]["targetResidualMaximum"]), cutoff=36,
        value=float(independent["maximumSlopeRelativeDifferenceFromPrimary"]),
        unit="Fourier coefficient",
        formula="max_m |a_0(t_m)| after independent reshooting",
        evidence="independent finite Galerkin",
        note="value column stores maximum slope relative difference from primary",
    ))

    with args.output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    metadata = {
        "release": config["release"],
        "figureId": config["figureId"],
        "rowCount": len(rows),
        "schema": ",".join(FIELDS),
        "inputs": {
            args.config.name: digest(args.config),
            args.primary.name: digest(args.primary),
            args.independent.name: digest(args.independent),
        },
        "evidenceMap": {
            "A": "primary mcut=24 DOP853 target trace; prescribed roots and RHS slopes",
            "B": "local complex-plane passages through the three prescribed target times",
            "C": "five freshly shot p1 values; O(p1^2) sampling and the exact one-shell first-jet identity",
            "D": "fixed-parameter cutoff sweep plus independent sparse mcut=36 reshooting",
        },
        "annulus": {
            "supportRadius": config["annulusSupportRadius"],
            "modulus": config["modulus"],
            "targetPair": [[0, 1, 1], [0, -1, -1]],
            "nearestNonTargetRadius": 50 ** 0.5,
        },
        "classification": config["classification"],
        "claimBoundary": (
            "The traces, roots, and cutoff comparison are finite Fourier-lattice "
            "corroboration. The exact 2.5D NSE reduction, modular annulus isolation, "
            "and existence of the infinite-dimensional recurrence curve are analytic "
            "results in the R0.71U report and are not inferred from this plot."
        ),
    }
    args.metadata.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
