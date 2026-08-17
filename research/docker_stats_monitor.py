#!/usr/bin/env python3
"""Append Docker and NVIDIA resource samples for a named offline job."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import time


FIELDS = (
    "timestampUtc",
    "container",
    "status",
    "cpuPercent",
    "memoryUsage",
    "memoryPercent",
    "processCount",
    "blockIO",
    "networkIO",
    "gpuUtilPercentMean",
    "gpuMemoryUsedMiB",
    "gpuTemperatureCMax",
)


def command(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(arguments, text=True, capture_output=True, check=False)


def running(container: str) -> tuple[bool, str]:
    result = command("docker", "inspect", "--format", "{{json .State}}", container)
    if result.returncode:
        return False, "not-found"
    state = json.loads(result.stdout)
    return bool(state.get("Running")), str(state.get("Status", "unknown"))


def docker_sample(container: str) -> dict[str, str]:
    result = command("docker", "stats", "--no-stream", "--format", "{{json .}}", container)
    if result.returncode or not result.stdout.strip():
        return {}
    return json.loads(result.stdout)


def gpu_sample() -> tuple[str, str, str]:
    result = command(
        "nvidia-smi",
        "--query-gpu=utilization.gpu,memory.used,temperature.gpu",
        "--format=csv,noheader,nounits",
    )
    if result.returncode or not result.stdout.strip():
        return "", "", ""
    rows = [
        [part.strip() for part in line.split(",")]
        for line in result.stdout.splitlines()
        if line.strip()
    ]
    utilization = [float(row[0]) for row in rows if row[0] not in {"N/A", "[N/A]"}]
    memory = [float(row[1]) for row in rows if row[1] not in {"N/A", "[N/A]"}]
    temperature = [float(row[2]) for row in rows if row[2] not in {"N/A", "[N/A]"}]
    return (
        str(sum(utilization) / len(utilization)) if utilization else "",
        str(sum(memory)) if memory else "",
        str(max(temperature)) if temperature else "",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--container", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--interval", type=float, default=5.0)
    arguments = parser.parse_args()
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    new_file = not arguments.output.exists()
    with arguments.output.open("a", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        if new_file:
            writer.writeheader()
            stream.flush()
        observed = False
        while True:
            is_running, status = running(arguments.container)
            if is_running:
                observed = True
                sample = docker_sample(arguments.container)
                gpu_utilization, gpu_memory, gpu_temperature = gpu_sample()
                writer.writerow(
                    {
                        "timestampUtc": datetime.now(timezone.utc).isoformat(),
                        "container": arguments.container,
                        "status": status,
                        "cpuPercent": sample.get("CPUPerc", ""),
                        "memoryUsage": sample.get("MemUsage", ""),
                        "memoryPercent": sample.get("MemPerc", ""),
                        "processCount": sample.get("PIDs", ""),
                        "blockIO": sample.get("BlockIO", ""),
                        "networkIO": sample.get("NetIO", ""),
                        "gpuUtilPercentMean": gpu_utilization,
                        "gpuMemoryUsedMiB": gpu_memory,
                        "gpuTemperatureCMax": gpu_temperature,
                    }
                )
                stream.flush()
                time.sleep(arguments.interval)
                continue
            if observed:
                writer.writerow(
                    {
                        "timestampUtc": datetime.now(timezone.utc).isoformat(),
                        "container": arguments.container,
                        "status": status,
                    }
                )
                stream.flush()
                break
            time.sleep(min(arguments.interval, 1.0))


if __name__ == "__main__":
    main()
