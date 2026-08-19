#!/usr/bin/env python3
"""Prepare deterministic presentation tables for the R0.58 formal figure."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform
import shutil
import subprocess
import time

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CERTIFICATE_DIR = ROOT / "research" / "certificates" / "r058"
CERTIFICATE = CERTIFICATE_DIR / "duhamel-critical-saturation.json"
FORMAL_PROGRESS = CERTIFICATE_DIR / "progress.ndjson"
FORMAL_RESOURCES = CERTIFICATE_DIR / "resources.csv"
C_RS = 2 + math.sqrt(2)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def require_source_commit(expected: str) -> None:
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()
    if len(expected) != 40 or any(character not in "0123456789abcdef" for character in expected):
        raise AssertionError("--source-commit must be a full lowercase hash")
    if head != expected:
        raise AssertionError("checked-out HEAD does not match --source-commit")


def rudin_shapiro(level: int) -> list[int]:
    p = [1]
    q = [1]
    for _ in range(level):
        p, q = p + q, p + [-value for value in q]
    return p


def sampled_unit_circle_maximum(coefficients: list[int], oversampling: int = 16) -> float:
    padded = np.zeros(oversampling * len(coefficients), dtype=np.complex128)
    padded[: len(coefficients)] = coefficients
    return float(np.abs(np.fft.fft(padded)).max())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", required=True)
    arguments = parser.parse_args()
    require_source_commit(arguments.source_commit)
    started = time.perf_counter()

    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate["git"]["sourceCommit"] != "35a817f00d8821e91f033764f6bd29fc1697ad56":
        raise AssertionError("unexpected formal source commit")
    if not all(certificate["checks"].values()):
        raise AssertionError("formal certificate did not pass all checks")

    coefficient_rows: list[dict[str, object]] = []
    for exponent in range(17):
        shell = 2**exponent
        observation_time = math.log(2) / (2 * shell * shell)
        coefficient = math.exp(-observation_time) * sum(
            (1 - math.exp(-2 * frequency * frequency * observation_time))
            / (2 * frequency * frequency)
            for frequency in range(shell, 2 * shell)
        )
        coefficient_rows.append(
            {
                "exponent": exponent,
                "L": shell,
                "observationTime": format(observation_time, ".17g"),
                "duhamelCoefficient": format(coefficient, ".17g"),
                "scaledCoefficient": format(shell * coefficient, ".17g"),
                "certifiedScaledLower": format(1 / 32, ".17g"),
                "certifiedScaledUpper": format(1 / 2, ".17g"),
            }
        )
    write_csv(
        HERE / "duhamel-coefficient.csv",
        [
            "exponent",
            "L",
            "observationTime",
            "duhamelCoefficient",
            "scaledCoefficient",
            "certifiedScaledLower",
            "certifiedScaledUpper",
        ],
        coefficient_rows,
    )

    c0 = math.sqrt(2) * math.cos(0.25) * math.sqrt(1 - math.exp(-0.125))
    heat_lower = math.sqrt(math.e) / (32 * math.sqrt(2) * C_RS * C_RS)
    bmo_lower = c0 / (64 * C_RS * C_RS)
    norm_rows: list[dict[str, object]] = []
    for exponent in range(17):
        shell = 2**exponent
        norm_rows.append(
            {
                "exponent": exponent,
                "L": shell,
                "blockLower": format(1 / (32 * shell**2), ".17g"),
                "blockUpper": format(1 / (2 * shell**2), ".17g"),
                "xMinusOneLower": format(1 / (64 * shell), ".17g"),
                "xMinusOneUpper": format(1 / shell, ".17g"),
                "hOneHalfLower": format(1 / (64 * math.sqrt(2) * shell**3), ".17g"),
                "hOneHalfUpper": format(1 / (2 * math.sqrt(2) * shell**3), ".17g"),
                "heatBesovUniformLower": format(heat_lower, ".17g"),
                "periodicBmoUniformLower": format(bmo_lower, ".17g"),
            }
        )
    write_csv(
        HERE / "norm-envelopes.csv",
        [
            "exponent",
            "L",
            "blockLower",
            "blockUpper",
            "xMinusOneLower",
            "xMinusOneUpper",
            "hOneHalfLower",
            "hOneHalfUpper",
            "heatBesovUniformLower",
            "periodicBmoUniformLower",
        ],
        norm_rows,
    )

    flattening_rows: list[dict[str, object]] = []
    for level in range(17):
        coefficients = rudin_shapiro(level)
        shell = len(coefficients)
        sampled_maximum = sampled_unit_circle_maximum(coefficients)
        flattening_rows.append(
            {
                "level": level,
                "L": shell,
                "sampledRudinShapiroMaximum": format(sampled_maximum, ".17g"),
                "sampledRudinShapiroOverSqrtL": format(sampled_maximum / math.sqrt(shell), ".17g"),
                "exactFullPolynomialUpperOverSqrtL": format(math.sqrt(2), ".17g"),
                "allPositiveMaximumOverSqrtL": format(math.sqrt(shell), ".17g"),
                "samplesOnUnitCircle": 16 * shell,
            }
        )
    write_csv(
        HERE / "phase-flattening.csv",
        [
            "level",
            "L",
            "sampledRudinShapiroMaximum",
            "sampledRudinShapiroOverSqrtL",
            "exactFullPolynomialUpperOverSqrtL",
            "allPositiveMaximumOverSqrtL",
            "samplesOnUnitCircle",
        ],
        flattening_rows,
    )

    shutil.copyfile(FORMAL_PROGRESS, HERE / "formal-progress.ndjson")
    shutil.copyfile(FORMAL_RESOURCES, HERE / "formal-resources.csv")

    metadata = {
        "schemaVersion": "1.0",
        "createdUtc": datetime.now(timezone.utc).isoformat(),
        "sourceCommit": arguments.source_commit,
        "formalCertificate": {
            "path": str(CERTIFICATE.relative_to(ROOT)),
            "sha256": sha256(CERTIFICATE),
            "formalSourceCommit": certificate["git"]["sourceCommit"],
            "checks": len(certificate["checks"]),
            "modesChecked": certificate["finiteRegressions"]["duhamelFamily"]["modesChecked"],
            "maximumRudinShapiroLength": certificate["finiteRegressions"]["rudinShapiro"]["maximumLength"],
        },
        "presentationRows": {
            "coefficient": len(coefficient_rows),
            "normEnvelopes": len(norm_rows),
            "phaseFlattening": len(flattening_rows),
        },
        "presentationClassification": (
            "floating-point evaluation and sampled unit-circle maxima for display only; "
            "the formal inequalities use exact algebra and monotonicity"
        ),
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "randomness": False,
            "floatingPointDecisionUse": False,
        },
        "wallSeconds": time.perf_counter() - started,
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "status": "passed",
                "coefficientRows": len(coefficient_rows),
                "normRows": len(norm_rows),
                "flatteningRows": len(flattening_rows),
                "wallSeconds": metadata["wallSeconds"],
            },
            sort_keys=True,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
