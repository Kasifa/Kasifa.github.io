#!/usr/bin/env python3
"""Exact finite regression for the R0.62 quartic correlation reduction.

The all-index carry identity and analytic estimates are proved in
``research/quartic_correlation_reduction_note.md``.  This program checks the
integer identities on finite dyadic boxes and reports the explicit constants.
Finite enumeration is a regression of the formulas, not a proof of their
all-index validity.  No random input is used.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from decimal import Decimal, getcontext
import hashlib
import json
from pathlib import Path
import platform
import time


def rudin_shapiro(level: int) -> list[int]:
    p = [1]
    q = [1]
    for _ in range(level):
        p, q = p + q, p + [-value for value in q]
    return p


def inner_correlations(signs: list[int]) -> dict[int, int]:
    length = len(signs)
    result = {-1: 0, 0: 0, 1: 0}
    for q in range(length):
        for a in range(length):
            for b in range(length):
                difference = a + b - q
                for carry in (-1, 0, 1):
                    c = difference - carry * length
                    if 0 <= c < length:
                        result[carry] += signs[q] * signs[a] * signs[b] * signs[c]
    return result


def outer_correlations(signs: list[int], target_block: int) -> dict[int, int]:
    outputs = len(signs)
    result = {-1: 0, 0: 0, 1: 0}
    for carry in (-1, 0, 1):
        for a in range(outputs):
            for b in range(outputs):
                c = a + b - target_block + carry
                if 0 <= c < outputs:
                    result[carry] += (
                        signs[target_block] * signs[a] * signs[b] * signs[c]
                    )
    return result


def direct_carrier_correlation(
    signs_l: list[int], signs_m: list[int], target_block: int
) -> tuple[int, int]:
    length = len(signs_l)
    outputs = len(signs_m)
    carriers = length * outputs
    total = 0
    paths = 0
    for q_offset in range(length):
        q = target_block * length + q_offset
        q_sign = signs_m[target_block] * signs_l[q_offset]
        for a in range(carriers):
            a_block, a_offset = divmod(a, length)
            a_sign = signs_m[a_block] * signs_l[a_offset]
            for b in range(carriers):
                c = a + b - q
                if not 0 <= c < carriers:
                    continue
                b_block, b_offset = divmod(b, length)
                c_block, c_offset = divmod(c, length)
                b_sign = signs_m[b_block] * signs_l[b_offset]
                c_sign = signs_m[c_block] * signs_l[c_offset]
                total += q_sign * a_sign * b_sign * c_sign
                paths += 1
    return total, paths


def analytic_constants() -> dict[str, str]:
    getcontext().prec = 60
    two = Decimal(2)
    sqrt_two = two.sqrt()
    c_rs = two + sqrt_two
    c_tensor = (Decimal(1) + sqrt_two) * c_rs
    time_scale = two.ln() / two
    kappa_two = Decimal(8) / Decimal(25) * (
        Decimal(1) - (-(Decimal(25) / Decimal(16)) * two.ln()).exp()
    )
    quartic_constant = (
        c_rs * c_tensor**3 * time_scale**3 / (Decimal(48) * kappa_two)
    )
    return {
        "C_RS": str(c_rs),
        "C_tensor": str(c_tensor),
        "T": str(time_scale),
        "kappa_2": str(kappa_two),
        "C_quartic": str(quartic_constant),
        "bound": "|R_{L,M,m}| <= C_quartic (m/M)^2 sqrt(M)",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-level", type=int, default=3)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--progress-log", type=Path)
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    if not 0 <= arguments.maximum_level <= 5:
        raise ValueError("maximum level must lie between zero and five")

    started = time.perf_counter()
    if arguments.progress_log is not None:
        arguments.progress_log.parent.mkdir(parents=True, exist_ok=True)
        arguments.progress_log.write_text("", encoding="utf-8")

    digest = hashlib.sha256()
    boxes = 0
    target_blocks = 0
    direct_paths = 0
    largest_absolute_correlation = 0
    all_factorizations_hold = True
    all_carries_valid = True

    for level_l in range(arguments.maximum_level + 1):
        signs_l = rudin_shapiro(level_l)
        length = len(signs_l)
        inner = inner_correlations(signs_l)
        for level_m in range(arguments.maximum_level + 1):
            signs_m = rudin_shapiro(level_m)
            outputs = len(signs_m)
            boxes += 1
            for target_block in range(outputs):
                outer = outer_correlations(signs_m, target_block)
                factorized = sum(inner[k] * outer[k] for k in (-1, 0, 1))
                direct, paths = direct_carrier_correlation(
                    signs_l, signs_m, target_block
                )
                if direct != factorized:
                    all_factorizations_hold = False
                # The offset difference has absolute value below 2L and is a
                # multiple of L, hence only -1, 0, 1 can occur.
                for q in range(length):
                    for a in range(length):
                        for b in range(length):
                            c = (a + b - q) % length
                            difference = a + b - c - q
                            if difference % length or difference // length not in (-1, 0, 1):
                                all_carries_valid = False
                target_blocks += 1
                direct_paths += paths
                largest_absolute_correlation = max(
                    largest_absolute_correlation, abs(direct)
                )
                digest.update(
                    (
                        f"{level_l}:{level_m}:{target_block}:{inner}:"
                        f"{outer}:{direct}:{paths}\n"
                    ).encode()
                )
            if arguments.progress_log is not None:
                record = {
                    "timestampUtc": datetime.now(timezone.utc).isoformat(),
                    "elapsedSeconds": time.perf_counter() - started,
                    "levelL": level_l,
                    "levelM": level_m,
                    "L": length,
                    "M": outputs,
                    "targetBlocksChecked": target_blocks,
                }
                with arguments.progress_log.open("a", encoding="utf-8") as target:
                    target.write(json.dumps(record, sort_keys=True) + "\n")

    checks = {
        "onlyThreeCarriesOccur": all_carries_valid,
        "directCorrelationEqualsCarryFactorization": all_factorizations_hold,
        "allRudinShapiroCoefficientsAreSigns": all(
            value in (-1, 1)
            for level in range(arguments.maximum_level + 1)
            for value in rudin_shapiro(level)
        ),
        "noRandomness": True,
    }
    report = {
        "schemaVersion": "0.1",
        "status": "passed" if all(checks.values()) else "failed",
        "classification": (
            "exact finite integer regression of the R0.62 carry reduction; "
            "the all-index proof is in the accompanying mathematical note"
        ),
        "createdUtc": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
        "coverage": {
            "maximumDyadicLevel": arguments.maximum_level,
            "parameterBoxes": boxes,
            "targetBlocks": target_blocks,
            "directCarrierTriples": direct_paths,
            "largestAbsoluteUnweightedCorrelation": largest_absolute_correlation,
            "recordsSha256": digest.hexdigest(),
        },
        "analyticConstants": analytic_constants(),
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
        raise SystemExit("R0.62 correlation reduction audit failed")


if __name__ == "__main__":
    main()
