#!/usr/bin/env python3
"""Validate the R0.64 figure tables against the pinned exact certificate."""

from __future__ import annotations

import csv
import hashlib
import json
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


def read_rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    report = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    metadata = json.loads((HERE / "figure-data-metadata.json").read_text(encoding="utf-8"))
    spectrum = read_rows("cycle-spectrum.csv")
    reachable = read_rows("reachable-cycle.csv")

    assert metadata["certificateSha256"] == sha256(CERTIFICATE)
    assert len(spectrum) == 5
    assert len(reachable) == 121
    assert sum(int(row["multiplicity"]) for row in spectrum) == 6
    assert 25 < max(float(row["eigenvalueDisplayOnly"]) for row in spectrum) < 26
    assert [int(row["y"]) for row in reachable[:16]] == report["reachableTargetFamily"]["initialValuesR0ThroughR15"]
    assert all(int(row["M"]) == 16 ** int(row["r"]) for row in reachable)
    assert all(
        int(row["target"]) == 2 * (16 ** int(row["r"]) - 1) // 15
        for row in reachable
    )
    assert 24 < float(reachable[-1]["observedBlockGrowth"]) < 25
    print(
        json.dumps(
            {
                "status": "passed",
                "spectrumRows": len(spectrum),
                "reachableRows": len(reachable),
                "certificateSha256": metadata["certificateSha256"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
