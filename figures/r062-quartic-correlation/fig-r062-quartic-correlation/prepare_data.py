#!/usr/bin/env python3
"""Prepare the source-locked data for Figure R0.62-1."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform
import subprocess
import time

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rudin_shapiro(level: int) -> np.ndarray:
    p = np.array([1], dtype=np.int64)
    q = np.array([1], dtype=np.int64)
    for _ in range(level):
        p, q = np.concatenate((p, q)), np.concatenate((p, -q))
    return p


def unweighted_outer_maximum(level: int) -> tuple[int, int, int, float]:
    signs = rudin_shapiro(level)
    outputs = len(signs)
    transform_length = 1 << math.ceil(math.log2(3 * outputs - 2))
    first = np.fft.rfft(signs.astype(np.float64), transform_length)
    reverse = np.fft.rfft(signs[::-1].astype(np.float64), transform_length)
    raw = np.fft.irfft(first * first * reverse, transform_length)[: 3 * outputs - 2]
    coefficients = np.rint(raw).astype(np.int64)
    residual = float(np.max(np.abs(raw - coefficients)))
    if residual >= 1e-5:
        raise AssertionError(f"FFT integer recovery residual too large: {residual}")
    if outputs <= 1024:
        exact = np.convolve(np.convolve(signs, signs), signs[::-1])
        if not np.array_equal(coefficients, exact):
            raise AssertionError("FFT convolution disagrees with exact integer convolution")

    best = (-1, -1, -1)
    for target in range(outputs):
        for carry in (-1, 0, 1):
            exponent = target - carry
            index = exponent + outputs - 1
            value = 0 if not 0 <= index < len(coefficients) else abs(int(coefficients[index]))
            if value > best[0]:
                best = (value, target, carry)
    return best[0], best[1], best[2], residual


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fieldnames)
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

    sources = {
        256: ROOT / "research/certificates/r061/all-targets-summary.json",
        512: ROOT / "research/certificates/r062/m512-all-summary.json",
        1024: ROOT / "research/certificates/r062/m1024-all-summary.json",
        2048: ROOT / "research/certificates/r062/m2048-all-summary.json",
    }
    profile_rows: list[dict[str, object]] = []
    weighted_maxima: dict[int, dict[str, object]] = {}
    source_records: list[dict[str, object]] = []
    for outputs, path in sources.items():
        payload = json.loads(path.read_text(encoding="utf-8"))
        selected = [
            record
            for record in payload["results"]
            if int(record["L"]) == 1 and int(record["M"]) == outputs
        ]
        if len(selected) != outputs:
            raise AssertionError(f"expected {outputs} complete targets in {path}")
        selected.sort(key=lambda record: int(record["target"]))
        maximum = max(selected, key=lambda record: float(record["normalizedSignedRatio"]))
        weighted_maxima[outputs] = maximum
        for record in selected:
            profile_rows.append(
                {
                    "L": 1,
                    "M": outputs,
                    "target": int(record["target"]),
                    "targetFraction": int(record["target"]) / outputs,
                    "normalizedSignedRatio": record["normalizedSignedRatio"],
                    "cancellationConditionNumber": record["cancellationConditionNumber"],
                    "orderedQuarticPaths": record["orderedQuarticPaths"],
                    "classification": record["classification"],
                }
            )
        source_records.append(
            {
                "path": str(path.relative_to(ROOT)),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "rowsSelected": len(selected),
            }
        )

    write_csv(
        HERE / "weighted-target-profiles.csv",
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

    scale_rows: list[dict[str, object]] = []
    largest_fft_residual = 0.0
    for level in range(8, 21):
        outputs = 1 << level
        unweighted, target, carry, residual = unweighted_outer_maximum(level)
        largest_fft_residual = max(largest_fft_residual, residual)
        weighted = weighted_maxima.get(outputs)
        scale_rows.append(
            {
                "levelM": level,
                "M": outputs,
                "weightedMaximumRatio": "" if weighted is None else weighted["normalizedSignedRatio"],
                "weightedMaximumTarget": "" if weighted is None else weighted["target"],
                "unweightedOuterMaximum": unweighted,
                "unweightedMaximumTargetBlock": target,
                "unweightedMaximumCarry": carry,
                "unweightedOuterMaximumOverM": unweighted / outputs,
                "fftIntegerRecoveryResidual": residual,
            }
        )
    write_csv(
        HERE / "scale-comparison.csv",
        [
            "levelM",
            "M",
            "weightedMaximumRatio",
            "weightedMaximumTarget",
            "unweightedOuterMaximum",
            "unweightedMaximumTargetBlock",
            "unweightedMaximumCarry",
            "unweightedOuterMaximumOverM",
            "fftIntegerRecoveryResidual",
        ],
        scale_rows,
    )

    outputs = [HERE / "weighted-target-profiles.csv", HERE / "scale-comparison.csv"]
    metadata = {
        "schemaVersion": "1.0",
        "createdUtc": datetime.now(timezone.utc).isoformat(),
        "sourceCommit": arguments.source_commit,
        "classification": "finite presentation data; all-index theorem is proved separately",
        "profileRows": len(profile_rows),
        "scaleRows": len(scale_rows),
        "weightedFamilies": sorted(weighted_maxima),
        "allDisplayedWeightedRatiosPositive": all(
            float(row["normalizedSignedRatio"]) > 0 for row in profile_rows
        ),
        "weightedMaximum": max(
            (
                {
                    "L": 1,
                    "M": outputs,
                    "target": int(record["target"]),
                    "value": float(record["normalizedSignedRatio"]),
                }
                for outputs, record in weighted_maxima.items()
            ),
            key=lambda record: record["value"],
        ),
        "largestFftIntegerRecoveryResidual": largest_fft_residual,
        "sourceData": source_records,
        "outputs": [
            {"path": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}
            for path in outputs
        ],
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
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
