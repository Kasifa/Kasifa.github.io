#!/usr/bin/env python3
"""Prepare lossless figure tables from the pinned R0.64 certificate."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[2]
CERTIFICATE = REPOSITORY / "research/certificates/r064/supercritical-cycle-audit.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", required=True)
    arguments = parser.parse_args()
    started = time.perf_counter()

    report = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if not all(report["checks"].values()):
        raise AssertionError("R0.64 source certificate did not pass")

    roots = report["cycle"]["realRootsDisplayOnly"]
    intervals = report["cycle"]["quarticRootIntervals"]
    spectrum_rows: list[dict[str, object]] = []
    for index, (root, interval) in enumerate(zip(roots, intervals), start=1):
        spectrum_rows.append(
            {
                "label": f"quartic root {index}",
                "eigenvalueDisplayOnly": f"{root:.15g}",
                "certifiedLower": interval[0],
                "certifiedUpper": interval[1],
                "multiplicity": 1,
                "factor": "x^4-25x^3-120x^2+3248x-8192",
            }
        )
    spectrum_rows.append(
        {
            "label": "threshold eigenvalue",
            "eigenvalueDisplayOnly": "16",
            "certifiedLower": 16,
            "certifiedUpper": 16,
            "multiplicity": 2,
            "factor": "(x-16)^2",
        }
    )
    write_csv(
        HERE / "cycle-spectrum.csv",
        [
            "label",
            "eigenvalueDisplayOnly",
            "certifiedLower",
            "certifiedUpper",
            "multiplicity",
            "factor",
        ],
        spectrum_rows,
    )

    values = [int(value) for value in report["reachableTargetFamily"]["initialValuesR0ThroughR15"]]
    recurrence = [int(value) for value in report["reachableTargetFamily"]["recurrenceFromR6"]["coefficients"]]
    while len(values) <= 30:
        values.append(
            sum(recurrence[lag] * values[-1 - lag] for lag in range(len(recurrence)))
        )
    reachable_rows: list[dict[str, object]] = []
    for r, value in enumerate(values):
        block_growth = "" if r == 0 or value == 0 else f"{math.exp(math.log(abs(value)) / r):.15g}"
        reachable_rows.append(
            {
                "r": r,
                "M": 16**r,
                "target": 2 * (16**r - 1) // 15,
                "y": value,
                "absoluteY": abs(value),
                "sign": 0 if value == 0 else (1 if value > 0 else -1),
                "absoluteYOverM": f"{abs(value) / (16**r):.15g}",
                "observedBlockGrowth": block_growth,
                "classification": "exact recurrence value",
            }
        )
    write_csv(
        HERE / "reachable-cycle.csv",
        [
            "r",
            "M",
            "target",
            "y",
            "absoluteY",
            "sign",
            "absoluteYOverM",
            "observedBlockGrowth",
            "classification",
        ],
        reachable_rows,
    )

    metadata = {
        "schemaVersion": "1.0",
        "sourceCommit": arguments.source_commit,
        "certificate": str(CERTIFICATE.relative_to(REPOSITORY)),
        "certificateSha256": sha256(CERTIFICATE),
        "spectrumRows": len(spectrum_rows),
        "reachableRows": len(reachable_rows),
        "dominantEigenvalueDisplayOnly": report["cycle"]["dominantEigenvalueDisplayOnly"],
        "fourLevelThreshold": report["cycle"]["fourLevelThreshold"],
        "exactCharacteristicPolynomial": report["cycle"]["fullCharacteristicPolynomial"],
        "randomness": False,
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "samplingWallSeconds": time.perf_counter() - started,
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(metadata, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

