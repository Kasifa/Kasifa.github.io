#!/usr/bin/env python3
"""Validate the R0.58 figure tables and pinned formal provenance."""

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

    coefficients = rows("duhamel-coefficient.csv")
    if len(coefficients) != 17:
        raise AssertionError("unexpected Duhamel row count")
    for row in coefficients:
        shell = int(row["L"])
        if shell != 2 ** int(row["exponent"]):
            raise AssertionError("non-dyadic shell")
        observation_time = math.log(2) / (2 * shell * shell)
        expected = math.exp(-observation_time) * sum(
            (1 - math.exp(-2 * frequency * frequency * observation_time))
            / (2 * frequency * frequency)
            for frequency in range(shell, 2 * shell)
        )
        if not math.isclose(float(row["duhamelCoefficient"]), expected, rel_tol=2e-15, abs_tol=1e-18):
            raise AssertionError("Duhamel presentation value mismatch")
        if not (1 / 32 <= shell * expected <= 1 / 2):
            raise AssertionError("Duhamel coefficient left the formal envelope")

    norms = rows("norm-envelopes.csv")
    if len(norms) != 17:
        raise AssertionError("unexpected norm-envelope row count")
    for row in norms:
        shell = int(row["L"])
        if float(row["blockLower"]) != 1 / (32 * shell**2):
            raise AssertionError("block lower envelope mismatch")
        if float(row["xMinusOneUpper"]) != 1 / shell:
            raise AssertionError("X^-1 upper envelope mismatch")
        if not math.isclose(
            float(row["hOneHalfLower"]),
            1 / (64 * math.sqrt(2) * shell**3),
            rel_tol=2e-16,
        ):
            raise AssertionError("H^1/2 lower envelope mismatch")

    flattening = rows("phase-flattening.csv")
    if len(flattening) != 17:
        raise AssertionError("unexpected phase-flattening row count")
    for row in flattening:
        level = int(row["level"])
        shell = int(row["L"])
        coefficients_at_level = rudin_shapiro(level)
        if len(coefficients_at_level) != shell or set(coefficients_at_level) - {-1, 1}:
            raise AssertionError("Rudin--Shapiro data mismatch")
        if float(row["sampledRudinShapiroOverSqrtL"]) > math.sqrt(2) * (1 + 1e-14):
            raise AssertionError("sampled maximum exceeded the exact full-polynomial bound")
        if float(row["allPositiveMaximumOverSqrtL"]) != math.sqrt(shell):
            raise AssertionError("all-positive comparison mismatch")

    print(
        json.dumps(
            {
                "status": "passed",
                "formalChecks": len(certificate["checks"]),
                "coefficientRows": len(coefficients),
                "normRows": len(norms),
                "flatteningRows": len(flattening),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
