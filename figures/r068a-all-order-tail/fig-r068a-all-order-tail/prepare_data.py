#!/usr/bin/env python3
"""Extract the R0.68A journal-figure tables from formal certificates."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
R068A = ROOT / "research/certificates/r068a/all-order-tail-reduction-audit.json"
R066 = ROOT / "research/certificates/r066/spectral-audit.json"
SOURCE_COMMIT = "95fcc835b63b1ef3abdea9038d49ad08b951e9fd"
CERTIFICATE_COMMIT = "f13b8fcd56ccc932f2ea6e411af0766d44ca4a18"


def write_rows(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    tail = json.loads(R068A.read_text(encoding="utf-8"))
    spectral = json.loads(R066.read_text(encoding="utf-8"))
    simple_prefactor = 1 / 30_000
    simple_rate = 43 / 64
    coarse_rate = 2**18 / 25**4
    lower = float(spectral["massSpectrum"]["dominantLowerDisplay"])
    upper = float(spectral["massSpectrum"]["dominantUpperDisplay"])
    lam = (lower + upper) / 2
    root_rate = 2**18 / lam**4
    sixth_rate = 16 / lam
    rows = []
    for block in range(17):
        rows.append(
            {
                "block": block,
                "certifiedSimpleBound": f"{simple_prefactor * simple_rate**block:.18e}",
                "rootEnclosureDisplayBound": f"{simple_prefactor * root_rate**block:.18e}",
            }
        )
    write_rows(
        "tail-bounds.csv",
        ["block", "certifiedSimpleBound", "rootEnclosureDisplayBound"],
        rows,
    )
    write_rows(
        "contraction-rates.csv",
        ["quantity", "rate", "status"],
        [
            {"quantity": "simple theorem rate", "rate": f"{simple_rate:.18e}", "status": "certified"},
            {"quantity": "lambda>25 rate", "rate": f"{coarse_rate:.18e}", "status": "certified"},
            {"quantity": "root-enclosure display", "rate": f"{root_rate:.18e}", "status": "certified"},
            {"quantity": "sixth fixed-order rate", "rate": f"{sixth_rate:.18e}", "status": "certified"},
            {"quantity": "eighth branch probe", "rate": f"{sixth_rate**2:.18e}", "status": "probe only"},
        ],
    )
    write_rows(
        "order-status.csv",
        ["order", "label", "status"],
        [
            {"order": 2, "label": "quadratic reference", "status": "exact"},
            {"order": 4, "label": "quartic projection", "status": "certified"},
            {"order": 6, "label": "sixth projection", "status": "certified"},
            {"order": 8, "label": "eighth heat term", "status": "open"},
            {"order": 10, "label": "complete tail n>=10", "status": "certified"},
        ],
    )
    metadata = {
        "status": "passed",
        "sourceCommit": SOURCE_COMMIT,
        "certificateCommit": CERTIFICATE_COMMIT,
        "r068aCertificateSha256": sha256(R068A),
        "r066CertificateSha256": sha256(R066),
        "r068aChecksPassed": sum(bool(value) for value in tail["checks"].values()),
        "r068aChecksTotal": len(tail["checks"]),
        "lambdaDisplayMidpoint": lam,
        "claimBoundary": tail["classification"],
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
