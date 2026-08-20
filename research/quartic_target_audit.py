#!/usr/bin/env python3
"""Aggregate and audit the finite R0.61 quartic-target computations.

The exact all-index coefficient formula is proved in
research/quartic_target_note.md.  This script checks the internal consistency
of deterministic long-double sweeps and an arbitrary-precision cross-check.
Its positivity and size conclusions apply only to the archived finite set.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import time


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_state(source_commit: str | None) -> dict[str, object]:
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], check=True, text=True, capture_output=True
    ).stdout.strip()
    if source_commit is not None:
        if len(source_commit) != 40 or any(
            character not in "0123456789abcdef" for character in source_commit
        ):
            raise ValueError("--source-commit must be a full lowercase hash")
        if source_commit != head:
            raise AssertionError("checked-out HEAD does not match --source-commit")
    status = subprocess.run(
        ["git", "status", "--porcelain"], check=True, text=True, capture_output=True
    ).stdout.splitlines()
    return {
        "sourceCommit": source_commit or head,
        "head": head,
        "worktreeStatusAtRun": status,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", type=Path, action="append", required=True)
    parser.add_argument("--high-precision", type=Path, required=True)
    parser.add_argument("--source-commit")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    started = time.perf_counter()

    evaluations: list[dict[str, object]] = []
    input_files: list[dict[str, object]] = []
    for path in arguments.summary:
        payload = json.loads(path.read_text(encoding="utf-8"))
        results = payload.get("results")
        if not isinstance(results, list):
            raise AssertionError(f"summary has no result list: {path}")
        evaluations.extend(results)
        input_files.append(
            {
                "path": str(path),
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
                "evaluations": len(results),
            }
        )

    unique: dict[tuple[int, int, int], dict[str, object]] = {}
    duplicate_discrepancies: list[float] = []
    for record in evaluations:
        length = int(record["L"])
        outputs = int(record["M"])
        target = int(record["target"])
        key = (length, outputs, target)
        if length <= 0 or length & (length - 1):
            raise AssertionError("L must be a positive power of two")
        if outputs <= 0 or outputs & (outputs - 1):
            raise AssertionError("M must be a positive power of two")
        if int(record["H"]) != 4 * length * outputs:
            raise AssertionError("H=4LM failed in scan output")
        if not 1 <= target <= outputs:
            raise AssertionError("target lies outside one through M")
        if int(record["orderedQuarticPaths"]) <= 0:
            raise AssertionError("ordered path count must be positive")
        if key in unique:
            old = float(unique[key]["normalizedSignedRatio"])
            new = float(record["normalizedSignedRatio"])
            duplicate_discrepancies.append(abs(old - new) / max(abs(old), abs(new)))
        else:
            unique[key] = record

    records = list(unique.values())
    maximum = max(records, key=lambda record: float(record["normalizedSignedRatio"]))
    minimum = min(records, key=lambda record: float(record["normalizedSignedRatio"]))
    largest_condition = max(
        records, key=lambda record: float(record["cancellationConditionNumber"])
    )
    high_precision = json.loads(arguments.high_precision.read_text(encoding="utf-8"))
    input_files.append(
        {
            "path": str(arguments.high_precision),
            "sha256": sha256(arguments.high_precision),
            "bytes": arguments.high_precision.stat().st_size,
            "evaluations": 1,
        }
    )
    high_value = float(high_precision["normalizedSignedRatio"])
    maximum_value = float(maximum["normalizedSignedRatio"])
    relative_high_difference = abs(high_value - maximum_value) / abs(high_value)
    reference_difference = float(
        high_precision["referenceComparison"]["relativeDifference"]
    )

    checks = {
        "allInputsClassifiedAsExploratory": all(
            "not a proof" in str(record["classification"]) for record in records
        ),
        "allObservedRatiosPositive": all(
            float(record["normalizedSignedRatio"]) > 0 for record in records
        ),
        "allPathCountsPositive": all(
            int(record["orderedQuarticPaths"]) > 0 for record in records
        ),
        "allCancellationConditionsFinitePositive": all(
            1 <= float(record["cancellationConditionNumber"]) < float("inf")
            for record in records
        ),
        "duplicateRunsAgree": max(duplicate_discrepancies, default=0.0) < 1e-15,
        "observedMaximumBelowPoint0014": maximum_value < 0.0014,
        "highPrecisionChecksObservedMaximum": (
            int(high_precision["L"]),
            int(high_precision["M"]),
            int(high_precision["target"]),
        )
        == (int(maximum["L"]), int(maximum["M"]), int(maximum["target"])),
        "highPrecisionAndLongDoubleAgree": relative_high_difference < 1e-12,
        "referenceComparisonAgrees": reference_difference < 1e-12,
        "noRandomness": all(record.get("randomness", False) is False for record in records)
        and high_precision.get("randomness") is False,
    }

    report = {
        "schemaVersion": "0.1-exploratory",
        "status": "passed" if all(checks.values()) else "failed",
        "classification": (
            "finite deterministic audit of the exact quartic path formula; "
            "observed signs and bounds are numerical evidence, not all-index theorems"
        ),
        "createdUtc": datetime.now(timezone.utc).isoformat(),
        "git": git_state(arguments.source_commit),
        "checks": checks,
        "coverage": {
            "evaluationsIncludingDuplicates": len(evaluations),
            "distinctParameterTargetTriples": len(records),
            "distinctParameterPairs": len(
                {(int(record["L"]), int(record["M"])) for record in records}
            ),
            "orderedQuarticPathsAcrossDistinctTriples": sum(
                int(record["orderedQuarticPaths"]) for record in records
            ),
            "duplicates": len(evaluations) - len(records),
        },
        "observations": {
            "minimumNormalizedSignedRatio": {
                "L": minimum["L"],
                "M": minimum["M"],
                "target": minimum["target"],
                "value": minimum["normalizedSignedRatio"],
            },
            "maximumNormalizedSignedRatio": {
                "L": maximum["L"],
                "M": maximum["M"],
                "target": maximum["target"],
                "value": maximum["normalizedSignedRatio"],
            },
            "largestCancellationConditionNumber": {
                "L": largest_condition["L"],
                "M": largest_condition["M"],
                "target": largest_condition["target"],
                "value": largest_condition["cancellationConditionNumber"],
            },
            "highPrecisionNormalizedSignedRatio": high_precision[
                "normalizedSignedRatio"
            ],
            "highPrecisionVersusLongDoubleRelativeDifference": relative_high_difference,
            "interpretation": (
                "Every archived ratio is positive, so every observed quartic target "
                "opposes the quadratic target. Uniform positivity and boundedness "
                "outside the archived finite set remain open."
            ),
        },
        "inputs": input_files,
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "randomness": False,
        },
        "wallSeconds": time.perf_counter() - started,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(report, indent=2 if arguments.pretty else None, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2 if arguments.pretty else None, sort_keys=True))
    if arguments.check and report["status"] != "passed":
        failed = [name for name, passed in checks.items() if not passed]
        raise SystemExit("R0.61 checks failed: " + ", ".join(failed))


if __name__ == "__main__":
    main()
