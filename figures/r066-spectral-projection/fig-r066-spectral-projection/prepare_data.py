#!/usr/bin/env python3
"""Prepare R0.66 journal-figure tables from the pinned certificates."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import resource
import time
from decimal import Decimal, localcontext
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[2]
FINITE_CERTIFICATE = REPOSITORY / "research/certificates/r065/weighted-cycle-audit.json"
SPECTRAL_CERTIFICATE = REPOSITORY / "research/certificates/r066/spectral-audit.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rss_mib() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024 * 1024) if platform.system() == "Darwin" else value / 1024


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--certificate-commit", required=True)
    arguments = parser.parse_args()
    started = time.perf_counter()
    finite = json.loads(FINITE_CERTIFICATE.read_text(encoding="utf-8"))
    spectral = json.loads(SPECTRAL_CERTIFICATE.read_text(encoding="utf-8"))
    if not all(finite["checks"].values()) or not all(spectral["checks"].values()):
        raise AssertionError("a pinned source certificate did not pass")

    convergence_rows: list[dict[str, object]] = []
    with localcontext() as context:
        context.prec = 70
        lambda_lower = Decimal(spectral["massSpectrum"]["dominantLowerDisplay"])
        lambda_upper = Decimal(spectral["massSpectrum"]["dominantUpperDisplay"])
        lambda_center = (lambda_lower + lambda_upper) / 2
        for scale in finite["scales"]:
            lower = Decimal(scale["intervalLower"])
            upper = Decimal(scale["intervalUpper"])
            center = (lower + upper) / 2
            cycle = int(scale["r"])
            convergence_rows.append(
                {
                    "r": cycle,
                    "normalizedCenter": str(center / lambda_center**cycle),
                    "signCertified": scale["signCertified"],
                    "classification": (
                        "display center from a certified finite interval; "
                        "not used in the R0.66 proof"
                    ),
                }
            )
    write_csv(
        HERE / "cycle-normalized.csv",
        ["r", "normalizedCenter", "signCertified", "classification"],
        convergence_rows,
    )

    finite_stage = spectral["exactFiniteIterate"]
    theorem = spectral["certifiedTheorem"]
    interval_rows = [
        {
            "quantity": "cycle-100 order-24 polynomial",
            "lower": finite_stage["normalizedLowerDisplay"],
            "upper": finite_stage["normalizedUpperDisplay"],
            "classification": "exact finite moment and rational time interval",
        },
        {
            "quantity": "complete dominant coefficient C_*",
            "lower": theorem["coefficientLowerDisplay"],
            "upper": theorem["coefficientUpperDisplay"],
            "classification": "complete outward asymptotic certificate",
        },
    ]
    write_csv(
        HERE / "coefficient-intervals.csv",
        ["quantity", "lower", "upper", "classification"],
        interval_rows,
    )

    errors = spectral["errorBudget"]
    coefficient_upper = abs(Decimal(theorem["coefficientUpperDisplay"]))
    error_rows = [
        {
            "component": "simplex tail projection",
            "bound": errors["infiniteSimplexTailProjection"],
            "kind": "error",
        },
        {
            "component": "finite spectral convergence",
            "bound": errors["finiteSpectralConvergence"],
            "kind": "error",
        },
        {
            "component": "finite target parameter",
            "bound": errors["finiteTargetParameter"],
            "kind": "error",
        },
        {"component": "total outward error", "bound": errors["total"], "kind": "total"},
        {
            "component": "certified distance to zero",
            "bound": str(coefficient_upper),
            "kind": "margin",
        },
    ]
    write_csv(HERE / "error-budget.csv", ["component", "bound", "kind"], error_rows)

    elapsed = time.perf_counter() - started
    metadata = {
        "schemaVersion": "1.0",
        "sourceCommit": arguments.source_commit,
        "certificateCommit": arguments.certificate_commit,
        "finiteCertificate": str(FINITE_CERTIFICATE.relative_to(REPOSITORY)),
        "finiteCertificateSha256": sha256(FINITE_CERTIFICATE),
        "spectralCertificate": str(SPECTRAL_CERTIFICATE.relative_to(REPOSITORY)),
        "spectralCertificateSha256": sha256(SPECTRAL_CERTIFICATE),
        "finiteRows": len(convergence_rows),
        "lambdaLower": spectral["massSpectrum"]["dominantLowerDisplay"],
        "lambdaUpper": spectral["massSpectrum"]["dominantUpperDisplay"],
        "coefficientLower": theorem["coefficientLowerDisplay"],
        "coefficientUpper": theorem["coefficientUpperDisplay"],
        "asymptoticFormula": theorem["asymptoticFormula"],
        "totalError": errors["total"],
        "randomness": False,
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "samplingWallSeconds": elapsed,
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_csv(
        HERE / "figure-data-resources.csv",
        ["elapsedSeconds", "rssMiB", "status"],
        [{"elapsedSeconds": f"{elapsed:.6f}", "rssMiB": f"{rss_mib():.3f}", "status": "exited:0"}],
    )
    print(json.dumps(metadata, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
