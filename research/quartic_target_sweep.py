#!/usr/bin/env python3
"""Run a monitored family of exploratory R0.61 quartic target scans.

The compiled scanner uses long-double exponentials.  These sweeps diagnose
scaling and cancellation; they are not interval certificates or proofs.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time


def scaling_pairs() -> list[tuple[int, int]]:
    pairs: list[tuple[int, int]] = []
    pairs.extend((0, level_m) for level_m in range(4, 11))
    pairs.extend((1, level_m) for level_m in range(4, 10))
    pairs.extend((2, level_m) for level_m in range(4, 9))
    pairs.extend((3, level_m) for level_m in range(4, 8))
    pairs.extend([(4, 4), (5, 5)])
    pairs.extend((level_l, 0) for level_l in range(4, 10))
    return pairs


def parse_pairs(value: str) -> list[tuple[int, int]]:
    pairs: list[tuple[int, int]] = []
    for item in value.split(","):
        left, right = item.split(":", maxsplit=1)
        pairs.append((int(left), int(right)))
    return pairs


def append_progress(
    path: Path | None, started: float, stage: str, **details: object
) -> None:
    if path is None:
        return
    record = {
        "timestampUtc": datetime.now(timezone.utc).isoformat(),
        "elapsedSeconds": time.perf_counter() - started,
        "stage": stage,
        **details,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as target:
        target.write(json.dumps(record, sort_keys=True) + "\n")
        target.flush()
        os.fsync(target.fileno())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--preset", choices=["scaling"])
    parser.add_argument("--pairs")
    parser.add_argument("--threads", type=int, default=16)
    parser.add_argument("--target-mode", choices=["edge", "all"], default="edge")
    parser.add_argument("--run-directory", type=Path, required=True)
    parser.add_argument("--progress-log", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    if bool(arguments.preset) == bool(arguments.pairs):
        parser.error("choose exactly one of --preset or --pairs")
    if arguments.threads < 1:
        parser.error("--threads must be positive")

    pairs = scaling_pairs() if arguments.preset else parse_pairs(arguments.pairs)
    arguments.run_directory.mkdir(parents=True, exist_ok=True)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    if arguments.progress_log is not None and arguments.progress_log.exists():
        arguments.progress_log.unlink()
    records: list[dict[str, object]] = []

    jobs = [
        (level_l, level_m, target)
        for level_l, level_m in pairs
        for target in (
            [1 << level_m]
            if arguments.target_mode == "edge"
            else range(1, (1 << level_m) + 1)
        )
    ]
    append_progress(
        arguments.progress_log,
        started,
        "started",
        parameterPairs=len(pairs),
        jobs=len(jobs),
        targetMode=arguments.target_mode,
        threadsPerRun=arguments.threads,
    )

    for index, (level_l, level_m, target) in enumerate(jobs, start=1):
        length = 1 << level_l
        outputs = 1 << level_m
        destination = arguments.run_directory / f"l{length}-m{outputs}-t{target}.json"
        command = [
            str(arguments.binary),
            "--level-l",
            str(level_l),
            "--level-m",
            str(level_m),
            "--target",
            str(target),
            "--threads",
            str(arguments.threads),
            "--output",
            str(destination),
        ]
        subprocess.run(command, check=True)
        record = json.loads(destination.read_text(encoding="utf-8"))
        record["command"] = command
        records.append(record)
        elapsed = time.perf_counter() - started
        rate = index / elapsed if elapsed else 0.0
        eta = (len(jobs) - index) / rate if rate else 0.0
        print(
            f"[R0.61 sweep +{elapsed:8.2f}s] {index}/{len(jobs)} "
            f"L={length} M={outputs} ratio={record['normalizedSignedRatio']:.12g} "
            f"condition={record['cancellationConditionNumber']:.6g} eta={eta:.1f}s",
            file=sys.stderr,
            flush=True,
        )
        append_progress(
            arguments.progress_log,
            started,
            "job-completed",
            completed=index,
            jobs=len(jobs),
            L=length,
            M=outputs,
            target=target,
            normalizedSignedRatio=record["normalizedSignedRatio"],
            cancellationConditionNumber=record["cancellationConditionNumber"],
            orderedQuarticPaths=record["orderedQuarticPaths"],
            etaSeconds=eta,
        )

    maximum = max(records, key=lambda item: float(item["normalizedSignedRatio"]))
    largest_condition = max(
        records, key=lambda item: float(item["cancellationConditionNumber"])
    )
    aggregate = {
        "schemaVersion": "0.1-exploratory",
        "classification": (
            "long-double quartic target scaling sweep; numerical evidence only"
        ),
        "createdUtc": datetime.now(timezone.utc).isoformat(),
        "preset": arguments.preset,
        "parameterPairs": len(pairs),
        "jobs": len(records),
        "targetMode": arguments.target_mode,
        "threadsPerRun": arguments.threads,
        "randomness": False,
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
        "results": records,
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "binary": str(arguments.binary),
        },
        "wallSeconds": time.perf_counter() - started,
    }
    arguments.output.write_text(
        json.dumps(aggregate, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    append_progress(
        arguments.progress_log,
        started,
        "completed",
        parameterPairs=len(pairs),
        jobs=len(records),
        maximumNormalizedSignedRatio=aggregate["maximumNormalizedSignedRatio"],
        largestCancellationConditionNumber=aggregate[
            "largestCancellationConditionNumber"
        ],
    )
    print(
        json.dumps(
            {
                "status": "completed",
                "parameterPairs": len(pairs),
                "jobs": len(records),
                "maximum": aggregate["maximumNormalizedSignedRatio"],
                "largestCondition": aggregate["largestCancellationConditionNumber"],
                "wallSeconds": aggregate["wallSeconds"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
