#!/usr/bin/env python3
"""High-precision cross-check of the complete R0.61 quartic target formula.

This program evaluates the same finite path formula as
research/quartic_target_scan.cpp with mpmath arbitrary-precision arithmetic.
It is a numerical cross-check, not an interval certificate or an all-index
proof.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time

import mpmath as mp


def rudin_shapiro(level: int) -> list[int]:
    p = [1]
    q = [1]
    for _ in range(level):
        p, q = p + q, p + [-value for value in q]
    return p


def factorial(order: int) -> int:
    return (1, 1, 2, 6)[order]


def simplex_kernel_three(
    integer_rates: tuple[int, int, int, int], high: int, terminal_time: mp.mpf
) -> mp.mpf:
    rates = sorted(integer_rates)
    high_squared = mp.mpf(high) ** 2
    nodes = [mp.mpf(rate) / high_squared for rate in rates]
    divided = [[mp.mpf("0") for _ in range(4)] for _ in range(4)]
    for index, node in enumerate(nodes):
        divided[index][0] = mp.exp(-terminal_time * node)
    for order in range(1, 4):
        for index in range(4 - order):
            if rates[index + order] == rates[index]:
                divided[index][order] = (
                    (-terminal_time) ** order
                    * mp.exp(-terminal_time * nodes[index])
                    / factorial(order)
                )
            else:
                divided[index][order] = (
                    divided[index + 1][order - 1] - divided[index][order - 1]
                ) / (nodes[index + order] - nodes[index])
    kernel = -divided[0][3]
    if not kernel > 0:
        raise AssertionError("simplex kernel must be positive")
    return kernel


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


def append_progress(path: Path | None, started: float, stage: str, **details: object) -> None:
    record = {
        "timestampUtc": datetime.now(timezone.utc).isoformat(),
        "elapsedSeconds": time.perf_counter() - started,
        "stage": stage,
        **details,
    }
    print(
        f"[R0.61 high precision +{record['elapsedSeconds']:8.2f}s] {stage}"
        + (" " + json.dumps(details, sort_keys=True) if details else ""),
        file=sys.stderr,
        flush=True,
    )
    if path is not None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as target:
            target.write(json.dumps(record, sort_keys=True) + "\n")
            target.flush()
            os.fsync(target.fileno())


def decimal(value: mp.mpf, digits: int) -> str:
    return mp.nstr(value, n=digits, strip_zeros=False)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level-l", type=int, required=True)
    parser.add_argument("--level-m", type=int, required=True)
    parser.add_argument("--target", type=int, default=0)
    parser.add_argument("--precision", type=int, default=60)
    parser.add_argument("--reference", type=Path)
    parser.add_argument("--source-commit")
    parser.add_argument("--progress-log", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    if arguments.level_l < 0 or arguments.level_m < 0:
        parser.error("levels must be nonnegative")
    if arguments.precision < 30:
        parser.error("precision must be at least 30 decimal digits")

    mp.mp.dps = arguments.precision
    length = 1 << arguments.level_l
    outputs = 1 << arguments.level_m
    count = length * outputs
    high = 4 * count
    target_index = arguments.target or outputs
    if not 1 <= target_index <= outputs:
        parser.error("target must lie in one through M")

    signs_l = rudin_shapiro(arguments.level_l)
    signs_m = rudin_shapiro(arguments.level_m)
    signs = [
        signs_m[block] * signs_l[offset]
        for block in range(outputs)
        for offset in range(length)
    ]

    def carrier_sign(carrier: int) -> int:
        return signs[carrier - high]

    started = time.perf_counter()
    if arguments.progress_log is not None and arguments.progress_log.exists():
        arguments.progress_log.unlink()
    append_progress(
        arguments.progress_log,
        started,
        "started",
        L=length,
        M=outputs,
        target=target_index,
        precision=arguments.precision,
    )

    terminal_time = mp.log(2) / 2
    q_start = high + (target_index - 1) * length
    q_stop = q_start + length
    quadratic = mp.fsum(
        (
            1 - mp.exp(-2 * (mp.mpf(q) / high) ** 2 * terminal_time)
        )
        / (2 * (mp.mpf(q) / high) ** 2)
        for q in range(q_start, q_stop)
    )

    signed_terms: list[mp.mpf] = []
    absolute_terms: list[mp.mpf] = []
    paths = 0
    for q_offset, q in enumerate(range(q_start, q_stop), start=1):
        for a in range(high, high + count):
            for b in range(high, high + count):
                c = a + b - q
                if not high <= c < high + count:
                    continue
                sign = carrier_sign(q) * carrier_sign(a) * carrier_sign(b) * carrier_sign(c)
                for p1, p2, p3 in ((a, b, -c), (a, -c, b), (-c, a, b)):
                    k1 = -q + p1
                    k2 = k1 + p2
                    if k2 + p3 != 0:
                        raise AssertionError("quartic path did not reach target")
                    kernel = simplex_kernel_three(
                        (
                            q * q + p1 * p1 + p2 * p2 + p3 * p3,
                            k1 * k1 + p2 * p2 + p3 * p3,
                            k2 * k2 + p3 * p3,
                            0,
                        ),
                        high,
                        terminal_time,
                    )
                    signed_terms.append(sign * kernel)
                    absolute_terms.append(kernel)
                    paths += 1
        append_progress(
            arguments.progress_log,
            started,
            "target-carrier-completed",
            completed=q_offset,
            total=length,
            paths=paths,
        )

    quartic = mp.fsum(signed_terms)
    absolute = mp.fsum(absolute_terms)
    normalized = (
        mp.mpf(length) ** 2
        * target_index**2
        / mp.mpf(high) ** 3
        * quartic
        / quadratic
    )
    reference: dict[str, object] | None = None
    if arguments.reference is not None:
        payload = json.loads(arguments.reference.read_text(encoding="utf-8"))
        reference_value = mp.mpf(str(payload["normalizedSignedRatio"]))
        reference = {
            "path": str(arguments.reference),
            "normalizedSignedRatio": str(payload["normalizedSignedRatio"]),
            "absoluteDifference": decimal(abs(normalized - reference_value), arguments.precision),
            "relativeDifference": decimal(
                abs(normalized - reference_value) / abs(normalized), arguments.precision
            ),
        }

    append_progress(
        arguments.progress_log,
        started,
        "completed",
        paths=paths,
        normalizedSignedRatio=decimal(normalized, min(arguments.precision, 30)),
    )
    result = {
        "schemaVersion": "0.1-exploratory",
        "classification": (
            "arbitrary-precision evaluation of the complete finite quartic path formula; "
            "not an interval certificate or proof"
        ),
        "createdUtc": datetime.now(timezone.utc).isoformat(),
        "git": git_state(arguments.source_commit),
        "levelL": arguments.level_l,
        "levelM": arguments.level_m,
        "L": length,
        "M": outputs,
        "H": high,
        "target": target_index,
        "decimalPrecision": arguments.precision,
        "orderedQuarticPaths": paths,
        "dimensionlessQuadraticKernelSum": decimal(quadratic, arguments.precision),
        "dimensionlessQuarticKernelSum": decimal(quartic, arguments.precision),
        "absoluteQuarticKernelSum": decimal(absolute, arguments.precision),
        "cancellationConditionNumber": decimal(absolute / abs(quartic), arguments.precision),
        "normalizedSignedRatio": decimal(normalized, arguments.precision),
        "normalization": "L^2*(G4/G2)/epsilon^2 for A=epsilon*sqrt(H)",
        "phaseRelation": "positive normalized ratio means G4 opposes G2",
        "terminalDimensionlessTime": decimal(terminal_time, arguments.precision),
        "referenceComparison": reference,
        "randomness": False,
        "wallSeconds": time.perf_counter() - started,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"status": "completed", **result}, sort_keys=True))


if __name__ == "__main__":
    main()
