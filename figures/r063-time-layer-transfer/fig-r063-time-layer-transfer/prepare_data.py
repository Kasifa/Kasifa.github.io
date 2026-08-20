#!/usr/bin/env python3
"""Prepare source-locked presentation data for Figure R0.63-1."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / "research/certificates/r063/time-layer-transfer-audit.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", required=True)
    arguments = parser.parse_args()
    started = time.perf_counter()
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, text=True, capture_output=True
    ).stdout.strip()
    if head != arguments.source_commit:
        raise AssertionError("checked-out HEAD does not match --source-commit")

    report = json.loads(SOURCE.read_text(encoding="utf-8"))
    if not all(report["checks"].values()):
        raise AssertionError("R0.63 source audit did not pass")
    probes = report["hostileWeightedProbes"]
    lift = report["cubicLift"]["records"]

    probe_rows = [
        {
            "M": row["M"],
            "target": row["target"],
            "S4OverM": row["S4OverM"],
            "normalizedSignedRatio": row["normalizedSignedRatio"],
            "cancellationConditionNumber": row["cancellationConditionNumber"],
            "orderedQuarticPaths": row["orderedQuarticPaths"],
            "wallSeconds": row["wallSeconds"],
            "classification": row["classification"],
        }
        for row in probes
    ]
    lift_rows = [
        {
            "level": row["level"],
            "M": row["M"],
            "targetWindowMaximum": row["targetWindowMaximum"],
            "exponent": row["exponent"],
            "maximumOverM": row["maximumOverM"],
        }
        for row in lift
    ]
    write_csv(
        HERE / "hostile-target-probes.csv",
        [
            "M",
            "target",
            "S4OverM",
            "normalizedSignedRatio",
            "cancellationConditionNumber",
            "orderedQuarticPaths",
            "wallSeconds",
            "classification",
        ],
        probe_rows,
    )
    write_csv(
        HERE / "cubic-lift-growth.csv",
        ["level", "M", "targetWindowMaximum", "exponent", "maximumOverM"],
        lift_rows,
    )

    outputs = [HERE / "hostile-target-probes.csv", HERE / "cubic-lift-growth.csv"]
    metadata = {
        "schemaVersion": "1.0",
        "createdUtc": datetime.now(timezone.utc).isoformat(),
        "sourceCommit": arguments.source_commit,
        "classification": "exact transfer regression and finite long-double probes; operator norm open",
        "source": {
            "path": str(SOURCE.relative_to(ROOT)),
            "bytes": SOURCE.stat().st_size,
            "sha256": sha256(SOURCE),
        },
        "probeRows": len(probe_rows),
        "liftRows": len(lift_rows),
        "maximumS4OverM": max(float(row["S4OverM"]) for row in probe_rows),
        "maximumCancellationConditionNumber": max(
            float(row["cancellationConditionNumber"]) for row in probe_rows
        ),
        "maximumOrderedQuarticPaths": max(int(row["orderedQuarticPaths"]) for row in probe_rows),
        "outputs": [
            {"path": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}
            for path in outputs
        ],
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "randomness": False,
        },
        "wallSeconds": time.perf_counter() - started,
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(metadata, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
