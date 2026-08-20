#!/usr/bin/env python3
"""Extract Figure R0.69A data from the formal assembly certificate."""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import resource
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CERTIFICATE = (
    ROOT / "research/certificates/r069a/full-picard-target-closure.json"
)
SOURCE_COMMIT = "9ca36bcadb43a5e43e84fdd779cd22959cfc6518"
CERTIFICATE_COMMIT = "df2c1051227f6316c2584350e1788ef52f7e1d2c"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_rows(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def rss_mib() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024 * 1024) if platform.system() == "Darwin" else value / 1024


def main() -> None:
    started = time.perf_counter()
    report = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    intervals = report["certifiedIntervals"]
    excess = intervals["positiveQuarticCorrection"]
    full = intervals["completeNormalizedTargetLimit"]
    write_rows(
        "limit-interval.csv",
        ["quantity", "lower", "upper", "lowerTimes1e8", "upperTimes1e8"],
        [
            {
                "quantity": "positive quartic correction",
                "lower": excess["lower"],
                "upper": excess["upper"],
                "lowerTimes1e8": f"{float(excess['lower']) * 1e8:.18e}",
                "upperTimes1e8": f"{float(excess['upper']) * 1e8:.18e}",
            },
            {
                "quantity": "complete normalized target",
                "lower": full["lower"],
                "upper": full["upper"],
                "lowerTimes1e8": f"{(float(full['lower']) - 1) * 1e8:.18e}",
                "upperTimes1e8": f"{(float(full['upper']) - 1) * 1e8:.18e}",
            },
        ],
    )
    rates = report["decayRates"]
    rate_rows = [
        {
            "component": "sixth order",
            "rate": rates["sixthUpperFromLambdaLower"]["decimal"],
            "exact": rates["sixthUpperFromLambdaLower"]["exact"],
        },
        {
            "component": "eighth order",
            "rate": rates["eighthUpperFromLambdaLower"]["decimal"],
            "exact": rates["eighthUpperFromLambdaLower"]["exact"],
        },
        {
            "component": "orders at least ten",
            "rate": rates["ordersAtLeastTen"]["decimal"],
            "exact": rates["ordersAtLeastTen"]["exact"],
        },
    ]
    write_rows("decay-rates.csv", ["component", "rate", "exact"], rate_rows)
    envelope_rows = []
    for block in range(21):
        row: dict[str, object] = {"block": block}
        for rate in rate_rows:
            key = rate["component"].replace(" ", "_")
            row[key] = f"{float(rate['rate']) ** block:.18e}"
        envelope_rows.append(row)
    write_rows(
        "rate-envelopes.csv",
        ["block", "sixth_order", "eighth_order", "orders_at_least_ten"],
        envelope_rows,
    )
    write_rows(
        "order-status.csv",
        ["order", "label", "status"],
        [
            {"order": "1", "label": "linear target", "status": "absent"},
            {"order": "2", "label": "quadratic reference", "status": "limit one"},
            {"order": "3,5,7,9", "label": "odd target terms", "status": "support zero"},
            {"order": "4", "label": "quartic branch", "status": "positive limit"},
            {"order": "6", "label": "sixth branch", "status": "vanishes"},
            {"order": "8", "label": "eighth branch", "status": "vanishes"},
            {"order": ">=10", "label": "complete tail", "status": "vanishes"},
        ],
    )
    metadata = {
        "status": "passed",
        "sourceCommit": SOURCE_COMMIT,
        "certificateCommit": CERTIFICATE_COMMIT,
        "certificateSha256": sha256(CERTIFICATE),
        "checksPassed": sum(bool(value) for value in report["checks"].values()),
        "checksTotal": len(report["checks"]),
        "claimBoundary": report["classification"],
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_rows(
        "figure-data-resources.csv",
        ["elapsedSeconds", "maximumRssMiB", "status"],
        [{
            "elapsedSeconds": f"{time.perf_counter() - started:.6f}",
            "maximumRssMiB": f"{rss_mib():.3f}",
            "status": "passed",
        }],
    )


if __name__ == "__main__":
    main()
