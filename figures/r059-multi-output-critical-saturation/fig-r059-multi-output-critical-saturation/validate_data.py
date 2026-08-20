#!/usr/bin/env python3
"""Validate the R0.59 figure tables and pinned formal provenance."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def coefficients(length: int, outputs: int) -> tuple[int, float, list[float]]:
    high = 4 * length * outputs
    observation_time = math.log(2) / (2 * high * high)
    values: list[float] = []
    for target in range(1, outputs + 1):
        total = sum(
            (1 - math.exp(-2 * (high + (target - 1) * length + offset) ** 2 * observation_time))
            / (2 * (high + (target - 1) * length + offset) ** 2)
            for offset in range(length)
        )
        values.append(target * math.exp(-target * target * observation_time) * total)
    return high, observation_time, values


def rudin_shapiro(level: int) -> list[int]:
    p = [1]
    q = [1]
    for _ in range(level):
        p, q = p + q, p + [-value for value in q]
    return p


def main() -> None:
    metadata = json.loads((HERE / "figure-data-metadata.json").read_text(encoding="utf-8"))
    certificate_path = ROOT / metadata["formalCertificate"]["path"]
    certificate = json.loads(certificate_path.read_text(encoding="utf-8"))
    if sha256(certificate_path) != metadata["formalCertificate"]["sha256"]:
        raise AssertionError("formal certificate hash mismatch")
    if certificate["git"]["sourceCommit"] != metadata["formalCertificate"]["formalSourceCommit"]:
        raise AssertionError("formal source commit mismatch")
    if not all(certificate["checks"].values()):
        raise AssertionError("formal certificate contains a failed check")

    profiles = rows("target-profiles.csv")
    if len(profiles) != 4 * 256:
        raise AssertionError("unexpected target-profile row count")
    profile_cache: dict[tuple[int, int], tuple[int, float, list[float]]] = {}
    for row in profiles:
        length = int(row["L"])
        outputs = int(row["M"])
        target = int(row["m"])
        key = (length, outputs)
        profile_cache.setdefault(key, coefficients(length, outputs))
        high, observation_time, values = profile_cache[key]
        expected = values[target - 1]
        if int(row["H"]) != high:
            raise AssertionError("profile high scale mismatch")
        if not math.isclose(float(row["observationTime"]), observation_time, rel_tol=2e-15):
            raise AssertionError("profile observation time mismatch")
        if not math.isclose(float(row["coefficient"]), expected, rel_tol=2e-15, abs_tol=1e-20):
            raise AssertionError("target coefficient mismatch")
        if not (float(row["scaledLower"]) < high * expected <= float(row["scaledUpper"])):
            raise AssertionError("target coefficient left the certified envelope")

    witnesses = rows("multi-output-witness.csv")
    if len(witnesses) != 121:
        raise AssertionError("unexpected witness row count")
    witness_cache: dict[tuple[int, int], tuple[int, float, list[float]]] = {}
    for row in witnesses:
        length = int(row["L"])
        outputs = int(row["M"])
        key = (length, outputs)
        witness_cache.setdefault(key, coefficients(length, outputs))
        high, observation_time, values = witness_cache[key]
        sigma = 1 / (4 * outputs * outputs)
        expected = math.sqrt(sigma) * 2 * sum(
            value * math.exp(-target * target * sigma) * math.sin(target / (2 * outputs))
            for target, value in enumerate(values, start=1)
        )
        if int(row["H"]) != high:
            raise AssertionError("witness high scale mismatch")
        if not math.isclose(float(row["observationTime"]), observation_time, rel_tol=2e-15):
            raise AssertionError("witness observation time mismatch")
        if not math.isclose(float(row["heatWitness"]), expected, rel_tol=2e-15, abs_tol=1e-20):
            raise AssertionError("heat witness mismatch")
        if high * expected < float(row["certifiedScaledHeatLower"]):
            raise AssertionError("displayed witness fell below the certified lower bound")

    flattening = rows("tensor-flattening.csv")
    if len(flattening) != 11:
        raise AssertionError("unexpected tensor-flattening row count")
    for row in flattening:
        level = int(row["level"])
        length = 2**level
        if len(rudin_shapiro(level)) != length:
            raise AssertionError("Rudin--Shapiro length mismatch")
        if int(row["totalPhases"]) != length * length:
            raise AssertionError("tensor phase count mismatch")
        if float(row["sampledTensorOverSqrtLM"]) > 2 * (1 + 1e-14):
            raise AssertionError("sampled tensor maximum exceeded the exact full bound")
        if not math.isclose(float(row["allPositiveMaximumOverSqrtLM"]), length, rel_tol=1e-15):
            raise AssertionError("all-positive tensor comparison mismatch")

    print(
        json.dumps(
            {
                "status": "passed",
                "formalChecks": len(certificate["checks"]),
                "profileRows": len(profiles),
                "witnessRows": len(witnesses),
                "flatteningRows": len(flattening),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
