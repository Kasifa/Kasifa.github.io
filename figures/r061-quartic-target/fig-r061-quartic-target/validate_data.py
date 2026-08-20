#!/usr/bin/env python3
"""Validate R0.61 figure tables against the pinned finite certificate."""

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
        for chunk in iter(lambda: source.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    metadata = json.loads((HERE / "figure-data-metadata.json").read_text(encoding="utf-8"))
    certificate_path = ROOT / metadata["formalCertificate"]["path"]
    audit = json.loads(certificate_path.read_text(encoding="utf-8"))
    if sha256(certificate_path) != metadata["formalCertificate"]["sha256"]:
        raise AssertionError("R0.61 certificate hash mismatch")
    if audit["git"]["sourceCommit"] != metadata["formalCertificate"]["formalSourceCommit"]:
        raise AssertionError("R0.61 source commit mismatch")
    if audit["status"] != "passed" or not all(audit["checks"].values()):
        raise AssertionError("R0.61 certificate contains a failed check")

    profiles = rows("target-profiles.csv")
    if len(profiles) != 416:
        raise AssertionError("unexpected target-profile row count")
    families: dict[tuple[int, int], set[int]] = {}
    for row in profiles:
        length, outputs, target = int(row["L"]), int(row["M"]), int(row["target"])
        families.setdefault((length, outputs), set()).add(target)
        if not math.isclose(float(row["targetFraction"]), target / outputs, rel_tol=1e-15):
            raise AssertionError("target fraction mismatch")
        if float(row["normalizedSignedRatio"]) <= 0:
            raise AssertionError("archived target profile lost observed positivity")
    if families != {
        (1, 256): set(range(1, 257)),
        (4, 64): set(range(1, 65)),
        (8, 64): set(range(1, 65)),
        (16, 32): set(range(1, 33)),
    }:
        raise AssertionError("target-profile families are incomplete")

    edges = rows("edge-scaling.csv")
    if len(edges) != 48:
        raise AssertionError("unexpected edge-scaling row count")
    maximum = max(float(row["normalizedSignedRatio"]) for row in edges)
    expected = float(audit["observations"]["maximumNormalizedSignedRatio"]["value"])
    if not math.isclose(maximum, expected, rel_tol=1e-15):
        raise AssertionError("edge maximum does not match certificate")
    if any(float(row["normalizedSignedRatio"]) <= 0 for row in edges):
        raise AssertionError("edge table lost observed positivity")

    print(
        json.dumps(
            {
                "status": "passed",
                "formalChecks": len(audit["checks"]),
                "profileRows": len(profiles),
                "edgeRows": len(edges),
                "maximum": maximum,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

