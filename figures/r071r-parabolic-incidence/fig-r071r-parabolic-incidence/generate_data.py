#!/usr/bin/env python3
"""Generate the journal-figure data for R0.71R."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from time import perf_counter

import numpy as np


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exact-certificate", type=Path, required=True)
    parser.add_argument("--independent-certificate", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    args = parser.parse_args()
    started = perf_counter()
    exact = json.loads(args.exact_certificate.read_text(encoding="utf-8"))
    independent = json.loads(args.independent_certificate.read_text(encoding="utf-8"))
    if exact["status"] != "passed" or independent["status"] != "passed":
        raise AssertionError("both R0.71R certificates must pass")

    rows: list[dict[str, object]] = []
    for rho in np.linspace(0.0, 2.0, 101):
        for name, value, formula in (
            ("Lamb Sobolev order", -rho / 2.0, "F in H^(-rho/2)"),
            ("vorticity Sobolev order", 1.0 - rho / 2.0, "W in H^(1-rho/2)"),
        ):
            rows.append({"panel": "A", "series": name, "case": "", "N": "", "x": rho, "y": value, "value": value, "unit": "Sobolev order", "formula": formula, "evidenceClass": "exact derivative ledger", "note": "rho=0 critical; rho=2 minimal Leray matched"})

    jet_rows = exact["checks"]["nseFrequencyJetScaling"]["rows"]
    for row in jet_rows:
        frequency = int(row["K"])
        gamma = float(row["gammaTwoTaylorJetSurrogate"].split("/")[0]) / float(row["gammaTwoTaylorJetSurrogate"].split("/")[1]) if "/" in row["gammaTwoTaylorJetSurrogate"] else float(row["gammaTwoTaylorJetSurrogate"])
        energy = float(row["kineticEnergy"].split("/")[0]) / float(row["kineticEnergy"].split("/")[1]) if "/" in row["kineticEnergy"] else float(row["kineticEnergy"])
        for name, value, formula in (
            ("Gamma_2 jet surrogate", gamma, "K^2/(4 theta^2)"),
            ("K squared law", 16.0 * frequency**2, "K^2/(4 theta^2), theta=1/8"),
            ("kinetic energy", energy, "a^2, a=1/8"),
        ):
            rows.append({"panel": "B", "series": name, "case": "", "N": frequency, "x": frequency, "y": value, "value": value, "unit": "coefficient or energy", "formula": formula, "evidenceClass": "exact NSE initial Fourier jet", "note": "first-jet coefficient; no positive-time integration"})

    touch_rows = exact["checks"]["scaledEvenTouch"]["rows"]
    for row in touch_rows:
        epsilon = float(row["epsilon"].split("/")[0]) / float(row["epsilon"].split("/")[1]) if "/" in row["epsilon"] else float(row["epsilon"])
        energy_text = row["sourceSquareEnergy"]
        energy = float(energy_text.split("/")[0]) / float(energy_text.split("/")[1]) if "/" in energy_text else float(energy_text)
        for name, value, formula in (
            ("positive entry", 1.0, "A_plus=1"),
            ("source-square energy", energy, "epsilon^2 E_1"),
        ):
            rows.append({"panel": "C", "series": name, "case": "", "N": "", "x": epsilon, "y": value, "value": value, "unit": "mass", "formula": formula, "evidenceClass": "exact forced scalar family", "note": "not an NSE trajectory"})

    for row in exact["checks"]["sequentialForcedFamily"]["rows"]:
        count = int(row["N"])
        for name, value, formula in (
            ("sequential entries", count, "entry mass=N"),
            ("sequential source", 1.0, "normalized source energy=1"),
        ):
            rows.append({"panel": "D", "series": name, "case": "sequential", "N": count, "x": count, "y": value, "value": value, "unit": "mass", "formula": formula, "evidenceClass": "exact forced scalar family", "note": "one observable"})
    for row in exact["checks"]["componentUnionFamily"]["rows"]:
        count = int(row["componentCount"])
        energy_text = row["summedSourceSquareEnergy"]
        energy = float(energy_text.split("/")[0]) / float(energy_text.split("/")[1]) if "/" in energy_text else float(energy_text)
        for name, value, formula in (
            ("component-union entries", count, "entry mass=Q"),
            ("component source", energy, "sum source energy<3"),
        ):
            rows.append({"panel": "D", "series": name, "case": "union", "N": count, "x": count, "y": value, "value": value, "unit": "mass", "formula": formula, "evidenceClass": "exact forced component family", "note": "not an NSE frame realization"})

    fields = ["panel", "series", "case", "N", "x", "y", "value", "unit", "formula", "evidenceClass", "note"]
    with args.output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    metadata = {
        "release": "R0.71R",
        "rows": len(rows),
        "generationWallSeconds": perf_counter() - started,
        "exactCertificateSha256": digest(args.exact_certificate),
        "independentCertificateSha256": digest(args.independent_certificate),
        "evidenceMap": {"A": "exact rho-dependent cutoff and annular derivative ledger", "B": "exact scaled NSE initial Fourier jet and first-jet incidence coefficient", "C": "exact scalar even-touch homogeneity family", "D": "exact sequential and component-union forced scalar families"},
        "dns": False,
        "pdeTimeStepping": False,
        "fittedData": False,
        "intervalCertified": False,
        "claimBoundary": "Panel B is an exact NSE initial Fourier jet and first-jet coefficient, not a positive-time integration. Panels C-D are forced scalar method tests, not NSE trajectories. No temporal packing, continuation, singularity, regularity, novelty, or Millennium-problem claim is shown."
    }
    args.metadata.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
