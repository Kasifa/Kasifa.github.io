#!/usr/bin/env python3
"""Prepare deterministic exact-formula tables for the R0.60 formal figure."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CERTIFICATE_DIR = ROOT / "research" / "certificates" / "r060"
CERTIFICATE = CERTIFICATE_DIR / "invariant-shear-picard.json"
FORMAL_PROGRESS = CERTIFICATE_DIR / "progress.ndjson"
FORMAL_RESOURCES = CERTIFICATE_DIR / "resources.csv"
FORMAL_SOURCE_COMMIT = "db3e7eb9071f67c041a96863f9afc43bbca50aec"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
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

    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate["git"]["sourceCommit"] != FORMAL_SOURCE_COMMIT:
        raise AssertionError("unexpected formal source commit")
    if not all(certificate["checks"].values()):
        raise AssertionError("formal certificate did not pass all checks")

    sample_n = [1, 2, 4, 5, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
    gap_formulas = {3: (3, 1), 5: (2, 2), 7: (1, 3), 9: (0, 4)}
    support_rows: list[dict[str, object]] = []
    for n_value in sample_n:
        high = 4 * n_value
        for order, (slope, intercept) in gap_formulas.items():
            gap = slope * n_value + intercept
            support_rows.append(
                {
                    "N": n_value,
                    "H": high,
                    "order": order,
                    "gap": gap,
                    "gapOverH": format(gap / high, ".17g"),
                    "targetStatus": "excluded",
                    "classification": "formal interval lower bound",
                }
            )
        order_eleven_gap = max(0, 5 - n_value)
        support_rows.append(
            {
                "N": n_value,
                "H": high,
                "order": 11,
                "gap": order_eleven_gap,
                "gapOverH": format(order_eleven_gap / high, ".17g"),
                "targetStatus": "support-admissible" if n_value >= 5 else "excluded",
                "classification": "explicit zero-support witness" if n_value >= 5 else "interval lower bound",
            }
        )
    write_csv(
        HERE / "support-gaps.csv",
        ["N", "H", "order", "gap", "gapOverH", "targetStatus", "classification"],
        support_rows,
    )

    event_rows = [
        {"order": 1, "lane": "original V support", "status": "initial", "path": "-Q"},
        {"order": 2, "lane": "target plane", "status": "reached", "path": "-Q+Q=0"},
        {"order": 2, "lane": "A^4 energy", "status": "positive square", "path": "||G2||^2"},
        {"order": 3, "lane": "target plane", "status": "excluded", "path": "|xi1|>=3N+1"},
        {"order": 3, "lane": "original V support", "status": "returned", "path": "-Q+P-P=-Q"},
        {"order": 3, "lane": "A^4 energy", "status": "cross term", "path": "2<G1,G3>"},
        {"order": 4, "lane": "target plane", "status": "support-admissible", "path": "-Q+Q+P-P=0"},
        {"order": 5, "lane": "target plane", "status": "excluded", "path": "gap 2N+2"},
        {"order": 7, "lane": "target plane", "status": "excluded", "path": "gap N+3"},
        {"order": 9, "lane": "target plane", "status": "excluded", "path": "gap 4"},
        {"order": 11, "lane": "target plane", "status": "support-admissible", "path": "zero path for N>=5"},
    ]
    write_csv(HERE / "picard-events.csv", ["order", "lane", "status", "path"], event_rows)

    shutil.copyfile(FORMAL_PROGRESS, HERE / "formal-progress.ndjson")
    shutil.copyfile(FORMAL_RESOURCES, HERE / "formal-resources.csv")
    elapsed = time.perf_counter() - started
    metadata = {
        "schemaVersion": "1.0",
        "createdUtc": datetime.now(timezone.utc).isoformat(),
        "sourceCommit": arguments.source_commit,
        "formalCertificate": {
            "path": "research/certificates/r060/invariant-shear-picard.json",
            "sha256": sha256(CERTIFICATE),
            "formalSourceCommit": FORMAL_SOURCE_COMMIT,
            "checks": len(certificate["checks"]),
            "stateTransitionsChecked": certificate["finiteRegressions"]["supports"]["stateTransitionsChecked"],
            "convolutionPairsChecked": certificate["finiteRegressions"]["energyCancellation"]["convolutionPairsChecked"],
        },
        "presentationRows": {"supportGaps": len(support_rows), "picardEvents": len(event_rows)},
        "presentationClassification": "exact integer-formula evaluation; no floating-point value controls a formal decision",
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "randomness": False,
            "floatingPointDecisionUse": False,
        },
        "wallSeconds": elapsed,
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"status": "passed", "supportRows": len(support_rows), "eventRows": len(event_rows), "wallSeconds": elapsed}, sort_keys=True))


if __name__ == "__main__":
    main()

