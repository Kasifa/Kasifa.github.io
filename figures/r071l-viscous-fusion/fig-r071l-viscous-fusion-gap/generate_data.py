#!/usr/bin/env python3
"""Generate deterministic source data for the R0.71L journal figure."""

from __future__ import annotations

import argparse
import csv
import json
import math
import platform
import time
from pathlib import Path


FIELDS = ("panel", "series", "x", "value", "category", "formula", "evidenceClass")


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
    parser.add_argument("--certificate", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("data.csv"))
    parser.add_argument("--metadata", type=Path, default=Path("figure-data-metadata.json"))
    args = parser.parse_args()
    started = time.perf_counter()
    certificate = json.loads(args.certificate.read_text(encoding="utf-8"))
    rows = []

    epsilon = 0.5
    for index in range(321):
        x_value = -math.pi + 2.0 * math.pi * index / 320.0
        interior = -3.0 * epsilon * math.cos(2.0 * x_value)
        collar = -interior
        add(rows, "A", "localizedLaplacian", x_value, interior, "expanded row", "-3*epsilon*cos(2*x)", "exact analytic profile")
        add(rows, "A", "rawCollarContribution", x_value, collar, "expanded row", "+3*epsilon*cos(2*x)", "exact analytic profile")
        add(rows, "A", "fusedViscous", x_value, interior + collar, "fused row", "interior+raw collar", "exact cancellation")

    row_map = certificate["integratedContributions"]["rows"]
    integrated = [
        ("radial", row_map["radial"]["aggregateKMinus2CoefficientSigned"]),
        ("heat tangent", row_map["heatMainTangent"]["aggregateKMinus2CoefficientSigned"]),
        ("raw collar", row_map["viscousCollar"]["aggregateKMinus2CoefficientSigned"]),
        ("fused tangent", row_map["projectiveTangent"]["aggregateKMinus2CoefficientSigned"]),
        ("normalization", row_map["normalization"]["aggregateKMinus2CoefficientSigned"]),
        ("joint source", row_map["fusedJoint"]["aggregateKMinus2CoefficientSigned"]),
    ]
    for index, (label, value) in enumerate(integrated):
        add(
            rows,
            "B",
            "integratedCoefficient",
            float(index),
            1.0e7 * value,
            label,
            "1e7*(K^-2 leading coefficient)",
            "fixed-witness deterministic quadrature diagnostic; not an interval sign certificate",
        )

    exponent_rows = [
        ("local heat", -4.0, "analytic upper scale K^-4", "earlier analytic upper-bound scale"),
        ("positive creation", -2.0, "analytic lower scale K^-2", "earlier analytic lower-bound scale"),
        ("raw collar", -2.0, "analytic expanded-row order K^-2", "earlier analytic expanded-row order"),
        (
            "fused tangent",
            -2.0,
            "diagnostic leading coefficient times K^-2",
            "fixed-witness deterministic diagnostic; nonzero coefficient is not an interval sign certificate",
        ),
        ("joint source", -2.0, "analytic selected-aggregate order K^-2", "earlier analytic selected-aggregate order"),
    ]
    for index, (label, value, formula, evidence) in enumerate(exponent_rows):
        add(rows, "C", "scalingExponent", float(index), value, label, formula, evidence)

    dependency_rows = [
        ("Leray energy", 0.0, "given"),
        ("denominator mass", 1.0, "paid"),
        ("angular ratio", 2.0, "unpaid"),
        ("normalized Lamb", 2.0, "unpaid"),
        ("absolute tangent", 3.0, "open"),
    ]
    for index, (label, level, status) in enumerate(dependency_rows):
        add(rows, "D", "dependency", float(index), level, label, status, "exact implication ledger")

    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    metadata = {
        "release": "R0.71L",
        "rows": len(rows),
        "sourceCertificate": str(args.certificate),
        "spatialOrder": certificate["configuration"]["spatialGaussLegendreOrder"],
        "timeOrder": certificate["configuration"]["timeGaussLegendreOrder"],
        "maximumTangentFusionResidual": certificate["identityDiagnostics"]["maximumTangentFusionResidual"],
        "integratedScalarIdentityResidual": certificate["identityDiagnostics"]["integratedScalarIdentityResidual"],
        "epsilonInExactExample": epsilon,
        "precision": "IEEE binary64 diagnostic plus exact analytic cancellation",
        "python": platform.python_version(),
        "randomSeed": None,
        "dns": False,
        "pdeTimeStepping": False,
        "fittedData": False,
        "wallTimeSeconds": time.perf_counter() - started,
        "panelEvidence": {
            "A": "exact algebra",
            "B": "fixed-witness deterministic quadrature diagnostic",
            "C": "mixed earlier analytic scaling bounds and fixed-witness deterministic diagnostic",
            "D": "exact implication ledger",
        },
        "finiteKScaleProvenance": "The checker supplies leading coefficients only; O_nu(K^-3) comes from earlier analytic finite-K theory.",
        "claimBoundary": "Panel B is diagnostic. In Panel C, the nonzero fused-tangent K^-2 coefficient is also a fixed-witness deterministic diagnostic, not an interval sign certificate.",
    }
    args.metadata.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
