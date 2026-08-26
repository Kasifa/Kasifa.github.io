#!/usr/bin/env python3
"""Generate the journal-figure data for R0.71S."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import shutil
from time import perf_counter


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def number(value: object) -> float:
    text = str(value)
    if "/" in text:
        numerator, denominator = text.split("/", 1)
        return float(numerator) / float(denominator)
    return float(text)


def add(
    rows: list[dict[str, object]],
    panel: str,
    series: str,
    case: str,
    count: object,
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
        "N": count,
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
    parser.add_argument("--exact-certificate", type=Path, required=True)
    parser.add_argument("--independent-certificate", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    args = parser.parse_args()
    started = perf_counter()
    exact = json.loads(args.exact_certificate.read_text(encoding="utf-8"))
    independent = json.loads(args.independent_certificate.read_text(encoding="utf-8"))
    if exact["release"] != "R0.71S" or independent["release"] != "R0.71S":
        raise AssertionError("R0.71S certificates required")
    if exact["status"] != "passed" or independent["status"] != "passed":
        raise AssertionError("both R0.71S certificates must pass")

    package = args.output.parent
    shutil.copyfile(args.exact_certificate, package / "exact-certificate.json")
    shutil.copyfile(args.independent_certificate, package / "independent-certificate.json")

    rows: list[dict[str, object]] = []
    for row in exact["checks"]["boxDiagonalScaling"]["rows"]:
        frequency = int(row["K"])
        critical = number(row["constantReproductionDiagonal"])
        add(
            rows, "A", "critical H^-1 packet cost", "", frequency,
            frequency, critical, "dimensionless coefficient", "1/h=K^2/theta",
            "exact nonzero-mean box packet",
            "time sampling on the Leray-paid amplitude",
        )
        add(
            rows, "A", "strong L2 coefficient", "", frequency,
            frequency, critical / frequency**2, "dimensionless coefficient",
            "K^-2/h=1/theta", "exact nonzero-mean box packet",
            "constant only after moving to the strong L2 Lamb ledger",
        )

    gram_rows = [
        row for row in exact["checks"]["finiteBoxGram"]["rows"]
        if int(row["N"]) == 64
    ]
    for row in sorted(gram_rows, key=lambda item: int(item["integerWindowOverlap"])):
        overlap = int(row["integerWindowOverlap"])
        for name, value, formula in (
            ("largest eigenvalue", float(row["numericalLargestEigenvalue"]), "lambda_max(G)"),
            ("exact Rayleigh lower", number(row["exactRayleighLowerBound"]), "p-(p^2-1)/(3N)"),
            ("exact row-sum upper", number(row["exactMaximumRowSumUpperBound"]), "p"),
        ):
            add(
                rows, "B", name, "N=64", 64, overlap, value,
                "Gram eigenvalue", formula, "exact finite box Gram matrix",
                "same spatial direction; p=Nh/T",
            )

    for row in exact["checks"]["backwardHeatConstants"]["rows"]:
        frequency = int(row["K"])
        critical = float(row["inverseNormalizedMeanSquared"])
        add(
            rows, "C", "critical H^-1 heat cost", "", frequency,
            frequency, critical, "dimensionless coefficient",
            "(nu*K^2/2)coth(nu*theta/2)", "exact adjoint heat packet",
            "endpoint upper packet; not an event lower charge",
        )
        add(
            rows, "C", "strong L2 heat coefficient", "", frequency,
            frequency, critical / frequency**2, "dimensionless coefficient",
            "(nu/2)coth(nu*theta/2)", "exact adjoint heat packet",
            "constant only with the strong L2 ledger",
        )

    for row in exact["checks"]["evenTouchCancellation"]["rows"]:
        eta = number(row["softEta"])
        exponent = int(round(-math.log2(eta) / 8.0))
        positive = number(row["rightSignedLayerMass"])
        jordan = number(row["totalJordanMass"])
        for name, value, formula, evidence in (
            ("positive face response", positive, "r^4/(r^4+eta)", "exact soft even-touch profile"),
            ("Jordan response", jordan, "2r^4/(r^4+eta)", "exact soft even-touch profile"),
            ("signed precursor response", 0.0, "A_+-A_-=0", "exact signed face cancellation"),
            ("zero-mean detector response", 0.0, "mean(psi_0)=0", "exact separable bilinear mean dichotomy"),
        ):
            add(
                rows, "D", name, "", exponent, exponent, value,
                "normalized response", formula, evidence,
                "forced-parabolic even touch; not an NSE trajectory",
            )

    fields = [
        "panel", "series", "case", "N", "x", "y", "value", "unit",
        "formula", "evidenceClass", "note",
    ]
    with args.output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    metadata = {
        "release": "R0.71S",
        "rows": len(rows),
        "generationWallSeconds": perf_counter() - started,
        "exactCertificateSha256": digest(args.exact_certificate),
        "independentCertificateSha256": digest(args.independent_certificate),
        "evidenceMap": {
            "A": "exact L2-normalized nonzero-mean box packet diagonal",
            "B": "exact finite same-direction box Gram matrix and bounds",
            "C": "exact backward/adjoint heat packet norm and mean",
            "D": "exact forced-parabolic even-touch and separable zero-mean responses",
        },
        "parameters": {"theta": 0.125, "nu": 1.0, "panelB_N": 64},
        "dns": False,
        "pdeTimeStepping": False,
        "fittedData": False,
        "intervalCertified": False,
        "claimBoundary": (
            "Panels A-C are exact finite packet or linear heat models. Panel D is a forced-parabolic even touch and is not an NSE trajectory. "
            "For the separately certified covariant family a_K=a0*K, the genuine R0.71O/R0.71P NSE information is limited to the initial "
            "observation face: A_plus=a0^2*K^2/4, K^-2*A_plus=a0^2/4, and the bare Leray time-integral scale K^-2. It is not plotted as a "
            "positive-time result. No temporal packing, continuation, singularity, regularity, novelty, or Millennium-problem claim is shown."
        ),
    }
    args.metadata.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
