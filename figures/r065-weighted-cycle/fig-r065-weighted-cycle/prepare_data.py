#!/usr/bin/env python3
"""Prepare lossless R0.65 figure tables from the pinned certificate."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import time
from decimal import Decimal, localcontext
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[2]
CERTIFICATE = REPOSITORY / "research/certificates/r065/weighted-cycle-audit.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--certificate-commit", required=True)
    arguments = parser.parse_args()
    started = time.perf_counter()
    report = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if report["profile"] != "publication" or not all(report["checks"].values()):
        raise AssertionError("R0.65 source certificate did not pass")

    fields = [
        "r",
        "M",
        "q",
        "m",
        "S4Lower",
        "S4Upper",
        "S4Center",
        "S4OverMLower",
        "S4OverMUpper",
        "S4OverMCenter",
        "signCertified",
        "tailBound",
        "relativeTail",
        "absoluteBlockRatioLower",
        "absoluteBlockRatioUpper",
        "absoluteBlockRatioCenter",
        "classification",
    ]
    rows: list[dict[str, object]] = []
    with localcontext() as context:
        context.prec = 60
        for scale in report["scales"]:
            length = Decimal(scale["M"])
            lower = Decimal(scale["intervalLower"])
            upper = Decimal(scale["intervalUpper"])
            center = (lower + upper) / 2
            ratio_lower = scale.get("absoluteBlockRatioLower", "")
            ratio_upper = scale.get("absoluteBlockRatioUpper", "")
            ratio_center = ""
            if ratio_lower != "":
                ratio_center = str((Decimal(ratio_lower) + Decimal(ratio_upper)) / 2)
            rows.append(
                {
                    "r": scale["r"],
                    "M": scale["M"],
                    "q": scale["q"],
                    "m": scale["m"],
                    "S4Lower": scale["intervalLower"],
                    "S4Upper": scale["intervalUpper"],
                    "S4Center": str(center),
                    "S4OverMLower": str(lower / length),
                    "S4OverMUpper": str(upper / length),
                    "S4OverMCenter": str(center / length),
                    "signCertified": scale["signCertified"],
                    "tailBound": scale["tailBound"],
                    "relativeTail": scale["relativeTailDisplayOnly"],
                    "absoluteBlockRatioLower": ratio_lower,
                    "absoluteBlockRatioUpper": ratio_upper,
                    "absoluteBlockRatioCenter": ratio_center,
                    "classification": "exact rational interval at a specified finite scale",
                }
            )
    with (HERE / "cycle-enclosures.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    metadata = {
        "schemaVersion": "1.0",
        "sourceCommit": arguments.source_commit,
        "certificateCommit": arguments.certificate_commit,
        "certificate": str(CERTIFICATE.relative_to(REPOSITORY)),
        "certificateSha256": sha256(CERTIFICATE),
        "rows": len(rows),
        "firstSignChangeR": report["certifiedSummary"]["firstSignChangeR"],
        "consecutiveSupercriticalBlocks": report["certifiedSummary"]["consecutiveSupercriticalBlocks"],
        "finalAbsoluteBlockRatioLower": report["certifiedSummary"]["finalAbsoluteBlockRatioLower"],
        "finalAbsoluteBlockRatioUpper": report["certifiedSummary"]["finalAbsoluteBlockRatioUpper"],
        "finalAbsoluteS4OverMLower": report["certifiedSummary"]["finalAbsoluteS4OverMLower"],
        "finalAbsoluteS4OverMUpper": report["certifiedSummary"]["finalAbsoluteS4OverMUpper"],
        "maximumRelativeTail": max(
            Decimal(scale["relativeTailDisplayOnly"]) for scale in report["scales"]
        ).to_eng_string(),
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
