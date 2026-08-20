#!/usr/bin/env python3
"""Exact finite-iterate stage for the R0.66 spectral certificate.

The output contains the exact rational endpoints of the degree-2D moment
evaluation of the order-D simplex polynomial.  It intentionally omits both
the infinite Taylor tail and the asymptotic spectral error; those are added
outward by quartic_weighted_cycle_spectral_audit.py.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import sys
import time
from fractions import Fraction
from pathlib import Path

import quartic_weighted_cycle_audit as r065


WORD = (0, 1, 0, 0)


def fraction_hash(value: Fraction) -> str:
    return hashlib.sha256(
        f"{value.numerator}/{value.denominator}".encode("ascii")
    ).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cycles", type=int, default=100)
    parser.add_argument("--order", type=int, default=24)
    parser.add_argument("--progress", action="store_true")
    arguments = parser.parse_args()
    if arguments.cycles < 4 or arguments.order < 8:
        raise ValueError("the exact stage requires cycles>=4 and order>=8")
    started = time.perf_counter()
    degree = 2 * arguments.order
    states = r065.initial_states(degree)
    length = 1
    for level in range(1, 4 * arguments.cycles + 1):
        bit = WORD[(level - 1) % 4]
        states = r065.advance_moments(states, degree, length, bit)
        length *= 2
        if arguments.progress and level % 4 == 0:
            print(
                f"[R0.66 finite +{time.perf_counter()-started:8.2f}s] "
                f"r={level//4:03d}/{arguments.cycles} bits(M)={length.bit_length()}",
                file=sys.stderr,
                flush=True,
            )

    target = 2 * (length - 1) // 15
    moments = states[r065.state_index(0, 0, 0)]
    sequences = [
        r065.complete_homogeneous_sequence(rates, arguments.order)
        for rates in r065.rate_polynomials(length, target)
    ]
    integer_coefficients = [
        sum(
            r065.moment_functional(sequence[index], moments)
            for sequence in sequences
        )
        for index in range(arguments.order + 1)
    ]
    high = 4 * length
    coefficients = [
        Fraction(
            (-1) ** index * value,
            high ** (2 * index) * math.factorial(index + 3),
        )
        for index, value in enumerate(integer_coefficients)
    ]
    time_lower, time_upper = r065.time_enclosure()
    lower, upper = r065.interval_polynomial(
        coefficients, time_lower, time_upper
    )
    checks = {
        "packetScaleIsExactPowerOfSixteen": length == 16**arguments.cycles,
        "targetIsRepeated0100Word": target == 2 * (length - 1) // 15,
        "timeIntervalIsOutward": time_lower < time_upper,
        "finitePolynomialIntervalIsOrdered": lower <= upper,
    }
    if arguments.cycles >= 100 and arguments.order >= 24:
        checks["publicationFinitePolynomialIsNegative"] = upper < 0
    if not all(checks.values()):
        raise AssertionError(checks)

    report = {
        "schemaVersion": "1.0",
        "status": "passed",
        "classification": (
            "exact integer moment iterate and exact rational finite Taylor "
            "polynomial; not by itself an infinite-series or asymptotic theorem"
        ),
        "checks": checks,
        "cycles": arguments.cycles,
        "order": arguments.order,
        "degree": degree,
        "M": str(length),
        "target": str(target),
        "partialLowerNumerator": str(lower.numerator),
        "partialLowerDenominator": str(lower.denominator),
        "partialUpperNumerator": str(upper.numerator),
        "partialUpperDenominator": str(upper.denominator),
        "partialLowerSha256": fraction_hash(lower),
        "partialUpperSha256": fraction_hash(upper),
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "randomness": False,
        },
        "wallSeconds": time.perf_counter() - started,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = arguments.output.with_suffix(arguments.output.suffix + ".tmp")
    temporary.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    temporary.replace(arguments.output)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
