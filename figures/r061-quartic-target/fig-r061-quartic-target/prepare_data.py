#!/usr/bin/env python3
"""Prepare presentation tables for the R0.61 quartic-target figure."""

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
CERTIFICATE_DIR = ROOT / "research" / "certificates" / "r061"
AUDIT = CERTIFICATE_DIR / "quartic-target-exploration.json"
ALL_TARGETS = CERTIFICATE_DIR / "all-targets-summary.json"
SCALING = CERTIFICATE_DIR / "scaling-summary.json"
EXTENDED = CERTIFICATE_DIR / "extended-summary.json"
FORMAL_SOURCE_COMMIT = "895543f44b3c83c777014eefc9594f95b3b9d829"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_source_commit(expected: str) -> None:
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, text=True, capture_output=True
    ).stdout.strip()
    if len(expected) != 40 or any(character not in "0123456789abcdef" for character in expected):
        raise AssertionError("--source-commit must be a full lowercase hash")
    if head != expected:
        raise AssertionError("checked-out HEAD does not match --source-commit")


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", required=True)
    arguments = parser.parse_args()
    require_source_commit(arguments.source_commit)
    started = time.perf_counter()

    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    if audit["status"] != "passed" or not all(audit["checks"].values()):
        raise AssertionError("R0.61 finite audit did not pass")
    if audit["git"]["sourceCommit"] != FORMAL_SOURCE_COMMIT:
        raise AssertionError("unexpected R0.61 formal source commit")

    all_targets = json.loads(ALL_TARGETS.read_text(encoding="utf-8"))["results"]
    profile_rows = [
        {
            "L": int(record["L"]),
            "M": int(record["M"]),
            "target": int(record["target"]),
            "targetFraction": format(int(record["target"]) / int(record["M"]), ".17g"),
            "normalizedSignedRatio": format(float(record["normalizedSignedRatio"]), ".17g"),
            "cancellationConditionNumber": format(float(record["cancellationConditionNumber"]), ".17g"),
            "orderedQuarticPaths": int(record["orderedQuarticPaths"]),
            "classification": "finite long-double observation",
        }
        for record in all_targets
    ]
    write_csv(
        HERE / "target-profiles.csv",
        [
            "L",
            "M",
            "target",
            "targetFraction",
            "normalizedSignedRatio",
            "cancellationConditionNumber",
            "orderedQuarticPaths",
            "classification",
        ],
        profile_rows,
    )

    edge_records: dict[tuple[int, int, int], dict[str, object]] = {}
    for source in (SCALING, EXTENDED):
        for record in json.loads(source.read_text(encoding="utf-8"))["results"]:
            key = (int(record["L"]), int(record["M"]), int(record["target"]))
            edge_records[key] = record
    edge_rows = [
        {
            "L": key[0],
            "M": key[1],
            "target": key[2],
            "normalizedSignedRatio": format(float(record["normalizedSignedRatio"]), ".17g"),
            "cancellationConditionNumber": format(float(record["cancellationConditionNumber"]), ".17g"),
            "orderedQuarticPaths": int(record["orderedQuarticPaths"]),
            "classification": "finite long-double edge observation",
        }
        for key, record in sorted(edge_records.items())
    ]
    write_csv(
        HERE / "edge-scaling.csv",
        [
            "L",
            "M",
            "target",
            "normalizedSignedRatio",
            "cancellationConditionNumber",
            "orderedQuarticPaths",
            "classification",
        ],
        edge_rows,
    )

    metadata = {
        "schemaVersion": "1.0",
        "createdUtc": datetime.now(timezone.utc).isoformat(),
        "sourceCommit": arguments.source_commit,
        "formalCertificate": {
            "path": "research/certificates/r061/quartic-target-exploration.json",
            "sha256": sha256(AUDIT),
            "formalSourceCommit": FORMAL_SOURCE_COMMIT,
            "checks": len(audit["checks"]),
            "distinctParameterTargetTriples": audit["coverage"][
                "distinctParameterTargetTriples"
            ],
            "orderedQuarticPaths": audit["coverage"][
                "orderedQuarticPathsAcrossDistinctTriples"
            ],
            "maximumNormalizedSignedRatio": audit["observations"][
                "maximumNormalizedSignedRatio"
            ],
            "highPrecisionRelativeDifference": audit["observations"][
                "highPrecisionVersusLongDoubleRelativeDifference"
            ],
        },
        "sourceFiles": [
            {"path": str(path.relative_to(ROOT)), "sha256": sha256(path), "bytes": path.stat().st_size}
            for path in (AUDIT, ALL_TARGETS, SCALING, EXTENDED)
        ],
        "presentationRows": {
            "targetProfiles": len(profile_rows),
            "edgeScaling": len(edge_rows),
        },
        "presentationClassification": (
            "deterministic finite observations; no plotted value is an all-index theorem"
        ),
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
    print(
        json.dumps(
            {
                "status": "passed",
                "profileRows": len(profile_rows),
                "edgeRows": len(edge_rows),
                "wallSeconds": metadata["wallSeconds"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

