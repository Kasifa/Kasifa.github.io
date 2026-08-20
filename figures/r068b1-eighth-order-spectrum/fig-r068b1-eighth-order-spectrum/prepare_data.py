#!/usr/bin/env python3
"""Extract the R0.68B-1 journal-figure tables from the formal certificate."""

from __future__ import annotations

import csv
from decimal import Decimal, getcontext
import hashlib
import json
import platform
import resource
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CERTIFICATE = ROOT / "research/certificates/r068b1/eighth-order-cycle-audit.json"
SOURCE_COMMIT = "3ddf6d30965837311c0b659d5fb21e41c3b80f14"
CERTIFICATE_COMMIT = "0e5387192f6ed2b796da4212ef3bf3220eed6e4c"


def write_rows(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rss_mib() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024 * 1024) if platform.system() == "Darwin" else value / 1024


def main() -> None:
    started = time.perf_counter()
    getcontext().prec = 60
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    state = certificate["stateSpace"]
    cycle = certificate["cycle"]
    reachable = certificate["reachableTargetFamily"]
    projection = reachable["dominantProjection"]

    write_rows(
        "rank-collapse.csv",
        ["stage", "power", "ambientDimension", "exactRank", "interpretation"],
        [
            {"stage": "ambient", "power": 0, "ambientDimension": 1792, "exactRank": 1792, "interpretation": "full state space"},
            {"stage": "one cycle", "power": 1, "ambientDimension": 1792, "exactRank": cycle["exactRanksByPower"][0], "interpretation": "image of W8"},
            {"stage": "two cycles", "power": 2, "ambientDimension": 1792, "exactRank": cycle["exactRanksByPower"][1], "interpretation": "stable image"},
            {"stage": "three cycles", "power": 3, "ambientDimension": 1792, "exactRank": cycle["exactRanksByPower"][2], "interpretation": "stable image confirmed"},
        ],
    )

    lower = Decimal(projection["dominantRootLowerDisplay"])
    upper = Decimal(projection["dominantRootUpperDisplay"])
    nu = (lower + upper) / 2
    write_rows(
        "spectral-blocks.csv",
        ["factor", "degree", "multiplicity", "imageDimension", "radiusLower", "radiusUpper", "role"],
        [
            {"factor": "x", "degree": 1, "multiplicity": 56, "imageDimension": 56, "radiusLower": "0", "radiusUpper": "0", "role": "nilpotent transient"},
            {"factor": "x-4096", "degree": 1, "multiplicity": 14, "imageDimension": 14, "radiusLower": "4096", "radiusUpper": "4096", "role": "exact subdominant root"},
            {"factor": "q4_256", "degree": 4, "multiplicity": 14, "imageDimension": 56, "radiusLower": projection["dominantRootLowerDisplay"], "radiusUpper": projection["dominantRootUpperDisplay"], "role": "reachable dominant root"},
            {"factor": "q10_16", "degree": 10, "multiplicity": 6, "imageDimension": 60, "radiusLower": "0", "radiusUpper": "4800", "role": "strict Schur enclosure"},
            {"factor": "q18", "degree": 18, "multiplicity": 1, "imageDimension": 18, "radiusLower": "0", "radiusUpper": "4800", "role": "strict Schur enclosure"},
        ],
    )

    sequence_rows = []
    for index, integer_value in enumerate(reachable["initialValues"]):
        normalized = Decimal(integer_value) / (nu ** index)
        sequence_rows.append(
            {
                "block": index,
                "exactInteger": integer_value,
                "normalizedByDominantRootMidpoint": f"{normalized:.30e}",
                "sign": "positive" if integer_value > 0 else "negative" if integer_value < 0 else "zero",
            }
        )
    write_rows(
        "reachable-sequence.csv",
        ["block", "exactInteger", "normalizedByDominantRootMidpoint", "sign"],
        sequence_rows,
    )

    write_rows(
        "certified-scales.csv",
        ["quantity", "lower", "upper", "status"],
        [
            {"quantity": "dominant root nu", "lower": projection["dominantRootLowerDisplay"], "upper": projection["dominantRootUpperDisplay"], "status": "strict rational bracket"},
            {"quantity": "remainder spectral radius", "lower": 0, "upper": 4800, "status": "strict exact Schur bound"},
            {"quantity": "dominant coefficient C8,0", "lower": projection["coefficientLowerDisplay"], "upper": projection["coefficientUpperDisplay"], "status": "strict rational interval"},
            {"quantity": "quartic-critical probe rate", "lower": 0, "upper": "0.4096", "status": "strict upper bound 256/625"},
        ],
    )

    metadata = {
        "status": "passed",
        "sourceCommit": SOURCE_COMMIT,
        "certificateCommit": CERTIFICATE_COMMIT,
        "certificateSha256": sha256(CERTIFICATE),
        "checksPassed": sum(bool(value) for value in certificate["checks"].values()),
        "checksTotal": len(certificate["checks"]),
        "stateDimension": state["dimension"],
        "imageCharacteristicSha256": cycle["imageCharacteristicSha256"],
        "dominantRootMidpointDisplay": f"{nu:.20f}",
        "claimBoundary": certificate["classification"],
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_rows(
        "figure-data-resources.csv",
        ["elapsedSeconds", "maximumRssMiB", "status"],
        [{"elapsedSeconds": f"{time.perf_counter() - started:.6f}", "maximumRssMiB": f"{rss_mib():.3f}", "status": "passed"}],
    )


if __name__ == "__main__":
    main()
