#!/usr/bin/env python3
"""Generate deterministic source data for the R0.71M journal figure."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import time
from pathlib import Path


FIELDS = ("panel", "series", "x", "value", "category", "formula", "evidenceClass")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add(rows, panel, series, x, value, category, formula, evidence):
    rows.append(
        {
            "panel": panel,
            "series": series,
            "x": f"{x:.17g}",
            "value": f"{value:.17g}",
            "category": category,
            "formula": formula,
            "evidenceClass": evidence,
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exact-certificate", type=Path, required=True)
    parser.add_argument("--independent-certificate", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("data.csv"))
    parser.add_argument("--metadata", type=Path, default=Path("figure-data-metadata.json"))
    args = parser.parse_args()
    started = time.perf_counter()
    exact = json.loads(args.exact_certificate.read_text(encoding="utf-8"))
    independent = json.loads(args.independent_certificate.read_text(encoding="utf-8"))
    if exact["status"] != "passed" or independent["status"] != "passed":
        raise RuntimeError("both certificates must pass")
    rows = []

    components = independent["checks"]["pairingComponents"]
    for index, key in enumerate(
        ("sourceSquare", "viscousCross", "projectiveSource", "projectiveViscous")
    ):
        add(
            rows,
            "A",
            "signedPairingComponent",
            float(index),
            float(components[key]),
            key,
            "exact expansion of int chi*(G-alpha curl C).(G+nu H)",
            "fixed-witness deterministic Fourier diagnostic",
        )
    add(
        rows,
        "A",
        "signedPairingTotal",
        4.0,
        float(independent["checks"]["pairingComponentSum"]),
        "total",
        "sum of four signed components",
        "fixed-witness deterministic Fourier diagnostic",
    )

    row_squares = independent["checks"]["weightedRowSquares"]
    total_square = sum(float(value) for value in row_squares.values())
    for index, key in enumerate(
        ("resolvedTransport", "incrementCommutator", "projectiveGeometry", "viscousMismatch")
    ):
        add(
            rows,
            "B",
            "normalizedCriticalRowSquare",
            float(index),
            float(row_squares[key]) / total_square,
            key,
            "weighted row L2 square / sum of four row squares",
            "fixed-witness deterministic Fourier diagnostic",
        )
    add(
        rows,
        "B",
        "supportDiagnostic",
        4.0,
        float(independent["checks"]["commutatorHighOffBandEnergyFraction"]),
        "commutatorHighOffBandFraction",
        "energy of R_j above radius 1.45*kappa / total energy of R_j",
        "fixed-witness deterministic Fourier diagnostic",
    )

    for exponent_index in range(7):
        radius = 2.0 ** (-exponent_index)
        for label, value, formula in (
            ("energy", 1.0, "r^0"),
            ("YuQuarticDefect", radius**-2, "r^-2"),
            ("velocityCarleson", radius**-1, "r^-1"),
            ("normalizedLamb", radius**-1, "r^-1"),
        ):
            add(
                rows,
                "C",
                label,
                radius,
                value,
                label,
                formula,
                "exact analytic heat-packet scaling exponent; coefficients normalized at r=1",
            )

    dependency_rows = (
        ("Leray energy", 0.0, "paid"),
        ("quadratic L2 increments", 1.0, "paid"),
        ("known quartic increment defect", 2.0, "extra hypothesis"),
        ("four-row tangent ledger", 3.0, "conditional"),
        ("signed scalar fusion", 4.0, "open R0.71N"),
    )
    for index, (label, level, status) in enumerate(dependency_rows):
        add(
            rows,
            "D",
            "implicationLedger",
            float(index),
            level,
            label,
            status,
            "exact implication and claim-boundary ledger",
        )

    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    metadata = {
        "release": "R0.71M",
        "rows": len(rows),
        "exactCertificate": str(args.exact_certificate),
        "exactCertificateSha256": digest(args.exact_certificate),
        "independentCertificate": str(args.independent_certificate),
        "independentCertificateSha256": digest(args.independent_certificate),
        "gridOrder": independent["configuration"]["gridOrder"],
        "incrementIdentityRelativeResidual": independent["checks"]["incrementIdentityRelativeResidual"],
        "projectivePairingRelativeResidual": independent["checks"]["projectivePairingRelativeResidual"],
        "offBandEnergyFraction": independent["checks"]["commutatorOffBandEnergyFraction"],
        "highOffBandEnergyFraction": independent["checks"]["commutatorHighOffBandEnergyFraction"],
        "precision": "exact symbolic audit plus deterministic IEEE binary64 Fourier audit",
        "python": platform.python_version(),
        "randomSeed": None,
        "dns": False,
        "pdeTimeStepping": False,
        "fittedData": False,
        "wallTimeSeconds": time.perf_counter() - started,
        "panelEvidence": {
            "A": "fixed-witness deterministic Fourier diagnostic",
            "B": "fixed-witness deterministic Fourier diagnostic",
            "C": "exact analytic heat-packet scaling exponents with normalized coefficients",
            "D": "exact implication and claim-boundary ledger",
        },
        "claimBoundary": (
            "Panels A-B diagnose one smooth finite Fourier witness and do not prove "
            "a continuous sign. Panel C is a function-space heat-flow separation, "
            "not an NSE solution counterexample. No regularity or singularity "
            "conclusion is represented."
        ),
    }
    args.metadata.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
