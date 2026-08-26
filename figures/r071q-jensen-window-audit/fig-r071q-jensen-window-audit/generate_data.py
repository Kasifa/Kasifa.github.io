#!/usr/bin/env python3
"""Generate the journal-figure data for R0.71Q."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
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
        raise AssertionError("both certificates must pass")

    rows: list[dict[str, object]] = []

    theta = np.linspace(-1.48, 1.48, 401)
    radius = np.cos(theta) ** 3
    for index, (angle, radial) in enumerate(zip(theta, radius)):
        rows.append({"panel": "A", "series": "Temam lobe", "case": index, "N": "", "x": radial * math.cos(angle), "y": radial * math.sin(angle), "value": radial, "unit": "T1", "formula": "s=cos(theta)^3", "evidenceClass": "primary theorem plus exact geometry", "note": "normalized T1=1"})
    circle = np.linspace(0.0, 2.0 * np.pi, 257)
    for index, angle in enumerate(circle):
        rows.append({"panel": "A", "series": "certified disk", "case": index, "N": "", "x": 0.25 + math.cos(angle) / 64.0, "y": math.sin(angle) / 64.0, "value": 1.0 / 64.0, "unit": "T1", "formula": "D(T1/4,T1/64)", "evidenceClass": "exact rational certificate", "note": "two-sided disk"})
    for enstrophy in np.geomspace(0.05, 256.0, 100):
        rows.append({"panel": "A", "series": "inverse window scale", "case": "", "N": "", "x": enstrophy, "y": (1.0 + enstrophy) ** 2, "value": (1.0 + enstrophy) ** -2, "unit": "normalized", "formula": "T1=(1+Y)^-2", "evidenceClass": "Temam scale", "note": "K_nu normalized to one"})

    for n in range(1, 65):
        zeros = (2.0 * n * n - np.arange(1, n + 1)) / (4.0 * n * n)
        minus_log_anchor = -float(np.sum(np.log(zeros)))
        jensen = minus_log_anchor / math.log(2.0)
        for series, value, formula in (
            ("distinct zeros", n, "#Z=N"),
            ("Jensen bound", jensen, "log(1/|B_N(0)|)/log2"),
            ("positive entries of B_N squared", n, "#entries=N"),
        ):
            rows.append({"panel": "B", "series": series, "case": "", "N": n, "x": n, "y": value, "value": value, "unit": "count", "formula": formula, "evidenceClass": "exact analytic family", "note": "unit-disk sup norm equals one"})

    per_component = math.log(6.0) / math.log(4.0 / 3.0)
    for count in range(1, 65):
        for series, value, formula in (
            ("distinct union", count, "#union=Q"),
            ("one-component capacity", per_component, "log6/log(4/3)"),
            ("summed capacity", per_component * count, "Q log6/log(4/3)"),
        ):
            rows.append({"panel": "C", "series": series, "case": "", "N": count, "x": count, "y": value, "value": value, "unit": "count", "formula": formula, "evidenceClass": "exact analytic union family", "note": "uniform M and anchor per component"})

    relative_growth = math.cosh(3.0 * math.pi / 4.0) ** 2
    for n in range(1, 65):
        for series, value, formula in (
            ("owned entries", n, "#entries=N"),
            ("owned windows", n, "#windows=N"),
            ("relative complex growth", relative_growth, "cosh(3pi/4)^2"),
        ):
            rows.append({"panel": "D", "series": series, "case": "", "N": n, "x": n, "y": value, "value": value, "unit": "count or ratio", "formula": formula, "evidenceClass": "exact sine-square family", "note": "local radii proportional to 1/N"})

    fields = ["panel", "series", "case", "N", "x", "y", "value", "unit", "formula", "evidenceClass", "note"]
    with args.output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    metadata = {
        "release": "R0.71Q",
        "rows": len(rows),
        "generationWallSeconds": perf_counter() - started,
        "exactCertificateSha256": digest(args.exact_certificate),
        "independentCertificateSha256": digest(args.independent_certificate),
        "evidenceMap": {
            "A": "Temam Chapter 7 scale plus exact rational disk extraction",
            "B": "exact rational finite Blaschke and squared positive-entry families",
            "C": "exact uniform-data component-union family",
            "D": "exact locally uniform sine-square ownership-cover family",
        },
        "dns": False,
        "pdeTimeStepping": False,
        "fittedData": False,
        "intervalCertified": False,
        "claimBoundary": "Panels B-D are analytic Hilbert-path or scalar-observable counterfamilies, not Navier-Stokes trajectories. Panel A uses a classical strong-solution complex-time theorem. No uniform NSE zero count, continuation, singularity, regularity, novelty, or Millennium-problem claim is shown.",
    }
    args.metadata.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
