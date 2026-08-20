#!/usr/bin/env python3
"""Validate the presentation data used by Figure R0.63-1."""

from __future__ import annotations

import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    probes = rows("hostile-target-probes.csv")
    lift = rows("cubic-lift-growth.csv")
    metadata = json.loads((HERE / "figure-data-metadata.json").read_text(encoding="utf-8"))
    checks = {
        "probeRows": len(probes) == 6 == metadata["probeRows"],
        "liftRows": len(lift) == 10 == metadata["liftRows"],
        "probeScales": [int(row["M"]) for row in probes]
        == [4096, 8192, 16384, 32768, 65536, 131072],
        "finiteClassification": all("not a proof" in row["classification"] for row in probes),
        "S4OverMRange": all(0.0 < float(row["S4OverM"]) < 0.02 for row in probes),
        "largestPathCount": max(int(row["orderedQuarticPaths"]) for row in probes)
        == 28977859974,
        "exactLiftScales": [int(row["M"]) for row in lift] == [1 << level for level in range(1, 11)],
        "unweightedLiftShowsGrowth": float(lift[-1]["maximumOverM"]) > 2.5,
        "noRandomness": metadata["environment"]["randomness"] is False,
    }
    report = {"status": "passed" if all(checks.values()) else "failed", "checks": checks}
    print(json.dumps(report, indent=2, sort_keys=True))
    if report["status"] != "passed":
        raise SystemExit("Figure R0.63-1 data validation failed")


if __name__ == "__main__":
    main()
