#!/usr/bin/env python3
"""Run a research command while recording its process-tree resources.

The wrapped solver should write scientific progress (step, physical time,
residual, CFL, checkpoints, ETA) to its own ``progress.ndjson``.  This
wrapper supplies the independent machine-side ``resources.csv`` record.
On NVIDIA systems it also samples ``nvidia-smi`` when available.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time


RESOURCE_FIELDS = (
    "timestampUtc",
    "elapsedSeconds",
    "status",
    "processCount",
    "cpuPercent",
    "rssMiB",
    "gpuCount",
    "gpuUtilPercentMean",
    "gpuMemoryUsedMiB",
    "gpuMemoryTotalMiB",
    "gpuTemperatureCMax",
)


def process_tree_snapshot(root_pid: int) -> tuple[int, float, float]:
    """Return descendant count, summed CPU percentage, and RSS in MiB."""

    completed = subprocess.run(
        ["ps", "-axo", "pid=,ppid=,%cpu=,rss="],
        check=True,
        capture_output=True,
        text=True,
    )
    entries: dict[int, tuple[int, float, int]] = {}
    for line in completed.stdout.splitlines():
        fields = line.split()
        if len(fields) != 4:
            continue
        try:
            pid, parent = int(fields[0]), int(fields[1])
            cpu, rss_kib = float(fields[2]), int(fields[3])
        except ValueError:
            continue
        entries[pid] = parent, cpu, rss_kib

    descendants = {root_pid}
    changed = True
    while changed:
        changed = False
        for pid, (parent, _cpu, _rss) in entries.items():
            if parent in descendants and pid not in descendants:
                descendants.add(pid)
                changed = True

    live = [entries[pid] for pid in descendants if pid in entries]
    return (
        len(live),
        sum(record[1] for record in live),
        sum(record[2] for record in live) / 1024,
    )


def nvidia_snapshot() -> tuple[int, float | None, float | None, float | None, float | None]:
    executable = shutil.which("nvidia-smi")
    if executable is None:
        return 0, None, None, None, None
    completed = subprocess.run(
        [
            executable,
            "--query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu",
            "--format=csv,noheader,nounits",
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    if completed.returncode != 0:
        return 0, None, None, None, None
    rows: list[tuple[float, float, float, float]] = []
    for line in completed.stdout.splitlines():
        try:
            utilization, used, total, temperature = (
                float(field.strip()) for field in line.split(",")
            )
        except (TypeError, ValueError):
            continue
        rows.append((utilization, used, total, temperature))
    if not rows:
        return 0, None, None, None, None
    return (
        len(rows),
        sum(row[0] for row in rows) / len(rows),
        sum(row[1] for row in rows),
        sum(row[2] for row in rows),
        max(row[3] for row in rows),
    )


def record_row(
    writer: csv.DictWriter,
    stream,
    root_pid: int,
    started: float,
    status: str,
) -> None:
    try:
        process_count, cpu_percent, rss_mib = process_tree_snapshot(root_pid)
    except (OSError, subprocess.SubprocessError):
        process_count, cpu_percent, rss_mib = 0, 0.0, 0.0
    try:
        gpu_count, gpu_util, gpu_used, gpu_total, gpu_temp = nvidia_snapshot()
    except (OSError, subprocess.SubprocessError):
        gpu_count, gpu_util, gpu_used, gpu_total, gpu_temp = 0, None, None, None, None
    writer.writerow(
        {
            "timestampUtc": datetime.now(timezone.utc).isoformat(),
            "elapsedSeconds": f"{time.perf_counter() - started:.6f}",
            "status": status,
            "processCount": process_count,
            "cpuPercent": f"{cpu_percent:.3f}",
            "rssMiB": f"{rss_mib:.3f}",
            "gpuCount": gpu_count,
            "gpuUtilPercentMean": "" if gpu_util is None else f"{gpu_util:.3f}",
            "gpuMemoryUsedMiB": "" if gpu_used is None else f"{gpu_used:.3f}",
            "gpuMemoryTotalMiB": "" if gpu_total is None else f"{gpu_total:.3f}",
            "gpuTemperatureCMax": "" if gpu_temp is None else f"{gpu_temp:.3f}",
        }
    )
    stream.flush()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--interval", type=float, default=60.0)
    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="command to run; place it after --",
    )
    arguments = parser.parse_args()
    if arguments.interval <= 0:
        parser.error("--interval must be positive")
    if arguments.command and arguments.command[0] == "--":
        arguments.command = arguments.command[1:]
    if not arguments.command:
        parser.error("a command is required after --")
    return arguments


def main() -> int:
    arguments = parse_arguments()
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    process = subprocess.Popen(arguments.command, start_new_session=True)
    print(
        f"monitor: started pid={process.pid}, interval={arguments.interval:g}s, "
        f"output={arguments.output}",
        file=sys.stderr,
        flush=True,
    )
    interrupted = False
    with arguments.output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=RESOURCE_FIELDS)
        writer.writeheader()
        while True:
            record_row(writer, stream, process.pid, started, "running")
            try:
                return_code = process.wait(timeout=arguments.interval)
                break
            except subprocess.TimeoutExpired:
                continue
            except KeyboardInterrupt:
                interrupted = True
                if os.name == "posix":
                    os.killpg(process.pid, signal.SIGINT)
                else:
                    process.send_signal(signal.SIGINT)
                return_code = process.wait()
                break
        record_row(
            writer,
            stream,
            process.pid,
            started,
            f"exited:{return_code}",
        )
    elapsed = time.perf_counter() - started
    print(
        f"monitor: finished returncode={return_code}, elapsed={elapsed:.1f}s",
        file=sys.stderr,
        flush=True,
    )
    return 130 if interrupted else return_code


if __name__ == "__main__":
    raise SystemExit(main())
