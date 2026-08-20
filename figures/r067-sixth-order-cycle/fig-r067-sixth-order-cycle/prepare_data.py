#!/usr/bin/env python3
"""Prepare R0.67A journal-figure tables from the pinned exact certificate."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import resource
import time
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[2]
CERTIFICATE = REPOSITORY / "research/certificates/r067/sixth-order-cycle-audit.json"


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


def decimal_fraction(value: str) -> Decimal:
    fraction = Fraction(value)
    return Decimal(fraction.numerator) / Decimal(fraction.denominator)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--certificate-commit", required=True)
    arguments = parser.parse_args()
    started = time.perf_counter()
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate["status"] != "passed" or not all(certificate["checks"].values()):
        raise AssertionError("the pinned R0.67A certificate did not pass")

    reachable = certificate["reachableTargetFamily"]
    projection = reachable["dominantProjection"]
    with localcontext() as context:
        context.prec = 80
        mu_lower = decimal_fraction(projection["dominantRootLower"])
        mu_upper = decimal_fraction(projection["dominantRootUpper"])
        mu_center = (mu_lower + mu_upper) / 2
        c_lower = Decimal(projection["coefficientLowerDisplay"])
        c_upper = Decimal(projection["coefficientUpperDisplay"])
        c_center = (c_lower + c_upper) / 2
        sequence_rows = []
        for cycle, integer_value in enumerate(reachable["initialValues"]):
            value = Decimal(integer_value)
            normalized = value / mu_center**cycle
            ratio = abs(value) / Decimal(256) ** cycle
            sequence_rows.append(
                {
                    "r": cycle,
                    "Y": integer_value,
                    "normalizedByMu": str(normalized),
                    "absoluteOverM2": str(ratio),
                    "asymptoticGuideOverM2": str(
                        abs(c_center) * (mu_center / Decimal(256)) ** cycle
                    ),
                    "sign": "positive" if integer_value > 0 else "negative",
                    "classification": "exact integer sequence; decimal normalizations are display values",
                }
            )
    write_csv(
        HERE / "reachable-sequence.csv",
        [
            "r",
            "Y",
            "normalizedByMu",
            "absoluteOverM2",
            "asymptoticGuideOverM2",
            "sign",
            "classification",
        ],
        sequence_rows,
    )

    root_rows = []
    for index, (lower, upper) in enumerate(certificate["cycle"]["scaledQuarticRootIntervals"], 1):
        root_rows.append(
            {
                "mode": f"q4 root {index}",
                "lower": lower,
                "upper": upper,
                "kind": "dominant" if index == 4 else "quartic",
                "classification": "exact sign-isolating interval",
            }
        )
    root_rows.append(
        {
            "mode": "all q10 roots",
            "lower": -certificate["cycle"]["degreeTenSchurRadius"],
            "upper": certificate["cycle"]["degreeTenSchurRadius"],
            "kind": "disk",
            "classification": "strict Schur disk bound; not a real-root interval",
        }
    )
    write_csv(
        HERE / "spectral-enclosures.csv",
        ["mode", "lower", "upper", "kind", "classification"],
        root_rows,
    )

    threshold_rows = [
        {
            "quantity": "zero-affine C2 threshold",
            "lower": certificate["absoluteTransfer"]["C2ZeroAffineThreshold"],
            "upper": certificate["absoluteTransfer"]["C2ZeroAffineThreshold"],
            "kind": "threshold",
        },
        {
            "quantity": "dominant reachable root mu",
            "lower": str(mu_lower),
            "upper": str(mu_upper),
            "kind": "dominant",
        },
        {
            "quantity": "absolute carry eigenvalue",
            "lower": certificate["absoluteTransfer"]["eigenvalue"],
            "upper": certificate["absoluteTransfer"]["eigenvalue"],
            "kind": "structural",
        },
    ]
    write_csv(
        HERE / "thresholds.csv",
        ["quantity", "lower", "upper", "kind"],
        threshold_rows,
    )

    elapsed = time.perf_counter() - started
    metadata = {
        "schemaVersion": "1.0",
        "sourceCommit": arguments.source_commit,
        "certificateCommit": arguments.certificate_commit,
        "certificate": str(CERTIFICATE.relative_to(REPOSITORY)),
        "certificateSha256": sha256(CERTIFICATE),
        "sequenceRows": len(sequence_rows),
        "exactChecks": len(certificate["checks"]),
        "directLevels": certificate["directAudit"]["exactLevelsChecked"],
        "stateDimension": certificate["stateSpace"]["dimension"],
        "imageDimension": certificate["cycle"]["imageDimension"],
        "muLower": str(mu_lower),
        "muUpper": str(mu_upper),
        "coefficientLower": projection["coefficientLowerDisplay"],
        "coefficientUpper": projection["coefficientUpperDisplay"],
        "C2Threshold": certificate["absoluteTransfer"]["C2ZeroAffineThreshold"],
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
        [
            {
                "elapsedSeconds": f"{elapsed:.6f}",
                "rssMiB": f"{rss_mib():.3f}",
                "status": "exited:0",
            }
        ],
    )
    print(json.dumps(metadata, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
