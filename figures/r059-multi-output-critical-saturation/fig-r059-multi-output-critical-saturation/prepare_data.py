#!/usr/bin/env python3
"""Prepare deterministic presentation tables for the R0.59 formal figure."""

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
CERTIFICATE_DIR = ROOT / "research" / "certificates" / "r059"
CERTIFICATE = CERTIFICATE_DIR / "multi-output-critical-saturation.json"
FORMAL_PROGRESS = CERTIFICATE_DIR / "progress.ndjson"
FORMAL_RESOURCES = CERTIFICATE_DIR / "resources.csv"
FORMAL_SOURCE_COMMIT = "f80788625f97a3038c492a6697832a7653bb8b82"
C_RS = 2 + math.sqrt(2)
C_T = (1 + math.sqrt(2)) * C_RS


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


def coefficients(length: int, outputs: int) -> tuple[int, float, list[float]]:
    high = 4 * length * outputs
    observation_time = math.log(2) / (2 * high * high)
    values: list[float] = []
    for target in range(1, outputs + 1):
        total = 0.0
        for offset in range(length):
            carrier = high + (target - 1) * length + offset
            total += (1 - math.exp(-2 * carrier * carrier * observation_time)) / (
                2 * carrier * carrier
            )
        values.append(target * math.exp(-target * target * observation_time) * total)
    return high, observation_time, values


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", required=True)
    arguments = parser.parse_args()
    require_source_commit(arguments.source_commit)
    started = time.perf_counter()

    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate["git"]["sourceCommit"] != FORMAL_SOURCE_COMMIT:
        raise AssertionError("unexpected formal source commit")
    if not all(certificate["checks"].values()):
        raise AssertionError("formal certificate did not pass all checks")

    profile_rows: list[dict[str, object]] = []
    fixed_outputs = 256
    for length in (4, 16, 64, 256):
        high, observation_time, values = coefficients(length, fixed_outputs)
        for target, value in enumerate(values, start=1):
            profile_rows.append(
                {
                    "L": length,
                    "M": fixed_outputs,
                    "H": high,
                    "m": target,
                    "mOverM": format(target / fixed_outputs, ".17g"),
                    "observationTime": format(observation_time, ".17g"),
                    "coefficient": format(value, ".17g"),
                    "scaledCoefficient": format(high * value, ".17g"),
                    "scaledLower": format(target / (50 * fixed_outputs), ".17g"),
                    "scaledUpper": format(target / (8 * fixed_outputs), ".17g"),
                }
            )
    write_csv(
        HERE / "target-profiles.csv",
        [
            "L",
            "M",
            "H",
            "m",
            "mOverM",
            "observationTime",
            "coefficient",
            "scaledCoefficient",
            "scaledLower",
            "scaledUpper",
        ],
        profile_rows,
    )

    witness_rows: list[dict[str, object]] = []
    heat_lower_scaled = math.exp(-0.25) / 600
    bmo_lower_scaled = math.exp(-1 / 64) / 3200
    for level_l in range(11):
        length = 2**level_l
        for level_m in range(11):
            outputs = 2**level_m
            high, observation_time, values = coefficients(length, outputs)
            sigma = 1 / (4 * outputs * outputs)
            heat_witness = math.sqrt(sigma) * 2 * sum(
                value
                * math.exp(-target * target * sigma)
                * math.sin(target / (2 * outputs))
                for target, value in enumerate(values, start=1)
            )
            witness_rows.append(
                {
                    "levelL": level_l,
                    "levelM": level_m,
                    "L": length,
                    "M": outputs,
                    "H": high,
                    "observationTime": format(observation_time, ".17g"),
                    "additionalHeatTime": format(sigma, ".17g"),
                    "heatWitness": format(heat_witness, ".17g"),
                    "scaledHeatWitness": format(high * heat_witness, ".17g"),
                    "certifiedScaledHeatLower": format(heat_lower_scaled, ".17g"),
                    "certifiedScaledBmoLower": format(bmo_lower_scaled, ".17g"),
                }
            )
    write_csv(
        HERE / "multi-output-witness.csv",
        [
            "levelL",
            "levelM",
            "L",
            "M",
            "H",
            "observationTime",
            "additionalHeatTime",
            "heatWitness",
            "scaledHeatWitness",
            "certifiedScaledHeatLower",
            "certifiedScaledBmoLower",
        ],
        witness_rows,
    )

    flattening_rows: list[dict[str, object]] = []
    for level in range(11):
        length = 2**level
        outputs = 2**level
        maximum_l = sampled_unit_circle_maximum(rudin_shapiro(level))
        maximum_m = sampled_unit_circle_maximum(rudin_shapiro(level))
        tensor_maximum = maximum_l * maximum_m
        total_phases = length * outputs
        flattening_rows.append(
            {
                "level": level,
                "L": length,
                "M": outputs,
                "totalPhases": total_phases,
                "sampledTensorMaximum": format(tensor_maximum, ".17g"),
                "sampledTensorOverSqrtLM": format(tensor_maximum / math.sqrt(total_phases), ".17g"),
                "exactFullTensorUpperOverSqrtLM": format(2.0, ".17g"),
                "formalPrefixUpperOverSqrtLM": format(C_T, ".17g"),
                "allPositiveMaximumOverSqrtLM": format(math.sqrt(total_phases), ".17g"),
                "samplesPerCircle": 16 * length,
            }
        )
    write_csv(
        HERE / "tensor-flattening.csv",
        [
            "level",
            "L",
            "M",
            "totalPhases",
            "sampledTensorMaximum",
            "sampledTensorOverSqrtLM",
            "exactFullTensorUpperOverSqrtLM",
            "formalPrefixUpperOverSqrtLM",
            "allPositiveMaximumOverSqrtLM",
            "samplesPerCircle",
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
            "modesChecked": certificate["finiteRegressions"]["packetFamily"]["modesChecked"],
            "interactionPairsChecked": certificate["finiteRegressions"]["interactions"]["orderedPositivePairsChecked"],
            "prefixesChecked": certificate["finiteRegressions"]["tensorPrefixes"]["prefixesChecked"],
        },
        "presentationRows": {
            "targetProfiles": len(profile_rows),
            "multiOutputWitness": len(witness_rows),
            "tensorFlattening": len(flattening_rows),
        },
        "presentationClassification": (
            "floating-point evaluation and sampled unit-circle maxima for display only; "
            "the formal inequalities use exact integer algebra and monotonicity"
        ),
        "constants": {
            "C_RS": C_RS,
            "C_T": C_T,
            "heatOutputScaledLower": heat_lower_scaled,
            "periodicBmoOutputScaledLower": bmo_lower_scaled,
        },
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
                "profileRows": len(profile_rows),
                "witnessRows": len(witness_rows),
                "flatteningRows": len(flattening_rows),
                "wallSeconds": metadata["wallSeconds"],
            },
            sort_keys=True,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
