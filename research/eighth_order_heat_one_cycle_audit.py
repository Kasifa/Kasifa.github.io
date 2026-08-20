#!/usr/bin/env python3
"""Exact first-cycle audit for the complete R0.68B eighth-order heat sum.

At the first stationary four-bit block, M=16, H=64, q=2 and Q=66.  The
audit sums every solution of

    A+B+C+D-E-F-G=Q

and all 35 sign shuffles.  A suffix dynamic program aggregates paths with
the same signed frequency sum and square sum.  It retains the complete
homogeneous Taylor coefficients of all seven nonzero heat rates exactly.
The enclosure of T=log(2)/2 and the omitted Taylor tail are rational.

This is a finite-scale sign certificate.  It is not a certificate for the
dominant asymptotic heat projection, the complete Picard series, or
three-dimensional Navier--Stokes regularity.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import sys
import time
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

import sixth_order_cycle_audit as r067


M = 16
H = 4 * M
Q_OFFSET = 2
Q = H + Q_OFFSET
POSITIVE_CARRIERS = 4
NEGATIVE_CARRIERS = 3
CARRIER_COUNT = POSITIVE_CARRIERS + NEGATIVE_CARRIERS
SHUFFLE_COUNT = math.comb(CARRIER_COUNT, POSITIVE_CARRIERS)
DEFAULT_ORDER = 44
EXPECTED_STATE_COUNTS = [32, 528, 5_796, 38_804, 105_499, 84_553, 4_178]
EXPECTED_VALID_TUPLES = 7_823_536
EXPECTED_ZERO_TIME_MASS = 11_896
EXPECTED_MAXIMUM_RATE = 114_888

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    if not enabled:
        return
    fields = " ".join(f"{key}={value}" for key, value in details.items())
    print(
        f"[R0.68B-2a eighth heat +{time.perf_counter() - started:8.2f}s] "
        f"{stage}{(' ' + fields) if fields else ''}",
        file=sys.stderr,
        flush=True,
    )


def decimal(value: Fraction, digits: int = 56) -> str:
    with localcontext() as context:
        context.prec = digits
        return format(Decimal(value.numerator) / Decimal(value.denominator), ".48E")


def fraction_sha256(value: Fraction) -> str:
    return hashlib.sha256(
        f"{value.numerator}/{value.denominator}".encode("ascii")
    ).hexdigest()


def time_enclosure(terms: int = 140) -> tuple[Fraction, Fraction]:
    """Enclose log(2)/2=atanh(1/3) by a positive rational series."""
    x = Fraction(1, 3)
    lower = sum(
        x ** (2 * index + 1) / (2 * index + 1) for index in range(terms)
    )
    first_omitted = 2 * terms + 1
    remainder = x**first_omitted / first_omitted / (1 - x * x)
    return lower, lower + remainder


def independent_offset_convolution(pair: list[int]) -> tuple[int, int]:
    """Return the unsigned count and signed mass at offset balance q=2."""
    profile: dict[int, tuple[int, int]] = {0: (1, 1)}
    for sign in (1, 1, 1, 1, -1, -1, -1):
        updated: dict[int, tuple[int, int]] = {}
        for total, (count, signed) in profile.items():
            for offset in range(M):
                key = total + sign * offset
                old_count, old_signed = updated.get(key, (0, 0))
                updated[key] = (
                    old_count + count,
                    old_signed + signed * int(pair[offset]),
                )
        profile = updated
    count, signed = profile[Q_OFFSET]
    return count, int(pair[Q_OFFSET]) * signed


def append_complete_homogeneous_factor(
    polynomial: list[int] | tuple[int, ...], rate: int, weight: int
) -> list[int]:
    """Multiply a truncated generating series by weight/(1-rate*z)."""
    output = [0] * len(polynomial)
    accumulated = int(polynomial[0])
    output[0] = weight * accumulated
    for degree in range(1, len(polynomial)):
        accumulated = int(polynomial[degree]) + rate * accumulated
        output[degree] = weight * accumulated
    return output


def enumerate_coefficients(
    order: int, report_progress: bool, started: float
) -> dict[str, object]:
    """Aggregate all 35 shuffle words by an exact suffix-state recursion."""
    pair_array, _companion = r067.rudin_shapiro_pair(4)
    pair = [int(value) for value in pair_array]
    states: dict[tuple[int, int, int], list[int] | tuple[int, ...]] = {
        (0, 0, 0): (1,) + (0,) * order
    }
    state_counts: list[int] = []
    transition_counts: list[int] = []
    maximum_rate = 0

    for depth in range(1, CARRIER_COUNT + 1):
        updated: dict[tuple[int, int, int], list[int]] = {}
        transitions = 0
        for (positive_used, suffix_sum, suffix_square), polynomial in states.items():
            negative_used = depth - 1 - positive_used
            for sign in (1, -1):
                next_positive = positive_used + int(sign > 0)
                next_negative = negative_used + int(sign < 0)
                if (
                    next_positive > POSITIVE_CARRIERS
                    or next_negative > NEGATIVE_CARRIERS
                ):
                    continue

                remaining_positive = POSITIVE_CARRIERS - next_positive
                remaining_negative = NEGATIVE_CARRIERS - next_negative
                remaining_lower = (
                    remaining_positive * H
                    - remaining_negative * (H + M - 1)
                )
                remaining_upper = (
                    remaining_positive * (H + M - 1)
                    - remaining_negative * H
                )

                for offset, carrier_sign in enumerate(pair):
                    magnitude = H + offset
                    next_sum = suffix_sum + sign * magnitude
                    missing = Q - next_sum
                    if not remaining_lower <= missing <= remaining_upper:
                        continue
                    next_square = suffix_square + magnitude * magnitude
                    rate = next_sum * next_sum + next_square
                    maximum_rate = max(maximum_rate, rate)
                    contribution = append_complete_homogeneous_factor(
                        polynomial, rate, carrier_sign
                    )
                    key = (next_positive, next_sum, next_square)
                    destination = updated.get(key)
                    if destination is None:
                        updated[key] = contribution
                    else:
                        for degree, value in enumerate(contribution):
                            destination[degree] += value
                    transitions += 1

        states = updated
        state_counts.append(len(states))
        transition_counts.append(transitions)
        progress(
            report_progress,
            started,
            "suffix dynamic program",
            depth=f"{depth}/{CARRIER_COUNT}",
            states=len(states),
            transitions=transitions,
            maximumRate=maximum_rate,
        )

    coefficients = [0] * (order + 1)
    target_sign = pair[Q_OFFSET]
    endpoint_failures = 0
    for (positive_used, suffix_sum, _suffix_square), polynomial in states.items():
        if positive_used != POSITIVE_CARRIERS or suffix_sum != Q:
            endpoint_failures += 1
            continue
        for degree, value in enumerate(polynomial):
            coefficients[degree] += target_sign * int(value)

    valid_tuples, zero_time_mass = independent_offset_convolution(pair)
    return {
        "coefficients": coefficients,
        "stateCounts": state_counts,
        "transitionCounts": transition_counts,
        "finalStates": len(states),
        "validCarrierTuples": valid_tuples,
        "zeroTimeMass": zero_time_mass,
        "maximumIntegerRate": maximum_rate,
        "endpointFailures": endpoint_failures,
    }


def interval_taylor_sum(
    coefficients: list[int], time_lower: Fraction, time_upper: Fraction
) -> tuple[Fraction, Fraction]:
    lower = Fraction(0)
    upper = Fraction(0)
    for degree, coefficient in enumerate(coefficients):
        scalar = Fraction(
            (-1) ** degree * coefficient,
            H ** (2 * degree) * math.factorial(degree + 7),
        )
        power = degree + 7
        if scalar >= 0:
            lower += scalar * time_lower**power
            upper += scalar * time_upper**power
        else:
            lower += scalar * time_upper**power
            upper += scalar * time_lower**power
    return lower, upper


def absolute_tail_bound(
    order: int,
    path_count: int,
    maximum_integer_rate: int,
    time_upper: Fraction,
) -> tuple[Fraction, Fraction]:
    """Majorize the seven-rate complete-homogeneous Taylor tail."""
    first_degree = order + 1
    alpha_bound = Fraction(maximum_integer_rate, H * H)
    z = alpha_bound * time_upper
    ratio = z / (first_degree + 1)
    if ratio >= 1:
        raise ValueError("Taylor order is too small for the geometric tail")
    first = (
        path_count
        * time_upper**7
        / math.factorial(6)
        * z**first_degree
        / ((first_degree + 7) * math.factorial(first_degree))
    )
    return first / (1 - ratio), ratio


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--order", type=int, default=DEFAULT_ORDER)
    parser.add_argument("--source-commit")
    parser.add_argument("--progress", action="store_true")
    arguments = parser.parse_args()
    if arguments.order < 32:
        raise ValueError("order must be at least 32 for a strict finite certificate")
    started = time.perf_counter()

    progress(arguments.progress, started, "starting", order=arguments.order)
    enumeration = enumerate_coefficients(
        arguments.order, arguments.progress, started
    )
    coefficients = enumeration["coefficients"]
    assert isinstance(coefficients, list)
    time_lower, time_upper = time_enclosure()
    partial_lower, partial_upper = interval_taylor_sum(
        coefficients, time_lower, time_upper
    )
    signed_paths = int(enumeration["validCarrierTuples"]) * SHUFFLE_COUNT
    tail, tail_ratio = absolute_tail_bound(
        arguments.order,
        signed_paths,
        int(enumeration["maximumIntegerRate"]),
        time_upper,
    )
    final_lower = partial_lower - tail
    final_upper = partial_upper + tail

    checks = {
        "thirtyFiveFourPlusThreeMinusShuffleWords": SHUFFLE_COUNT == 35,
        "independentConvolutionCountsSevenMillionEightHundredTwentyThreeThousandFiveHundredThirtySixTuples": (
            enumeration["validCarrierTuples"] == EXPECTED_VALID_TUPLES
        ),
        "independentConvolutionMatchesR068B1ZeroTimeMass": (
            enumeration["zeroTimeMass"] == EXPECTED_ZERO_TIME_MASS
        ),
        "suffixStateCountsMatchPinnedEnumeration": (
            enumeration["stateCounts"] == EXPECTED_STATE_COUNTS
        ),
        "everyRetainedPathHasTheTargetEndpoint": enumeration["endpointFailures"] == 0,
        "zerothTaylorCoefficientIsThirtyFiveTimesZeroTimeMass": (
            coefficients[0] == SHUFFLE_COUNT * EXPECTED_ZERO_TIME_MASS
        ),
        "maximumIntegerRateMatchesEnumeration": (
            enumeration["maximumIntegerRate"] == EXPECTED_MAXIMUM_RATE
        ),
        "tailGeometricRatioIsBelowOne": tail_ratio < 1,
        "absoluteTailIsBelowOneThousandth": tail < Fraction(1, 1000),
        "completeOneCycleEighthOrderHeatSumIsStrictlyPositive": final_lower > 0,
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    report = {
        "schemaVersion": "1.0",
        "status": "passed",
        "classification": (
            "exact finite-scale positive sign certificate for the complete "
            "eighth-order seven-simplex heat sum at M=16 and q=2; not a "
            "dominant asymptotic heat projection certificate, not a complete "
            "Picard-series estimate, and not a Navier-Stokes regularity theorem"
        ),
        "checks": checks,
        "parameters": {
            "M": M,
            "H": H,
            "q": Q_OFFSET,
            "Q": Q,
            "time": "T=log(2)/2",
            "TaylorOrder": arguments.order,
            "validCarrierTuples": enumeration["validCarrierTuples"],
            "timeOrderings": SHUFFLE_COUNT,
            "signedPaths": signed_paths,
        },
        "dynamicProgram": {
            "state": "(positive carriers used, signed suffix sum, suffix square sum)",
            "rateRecurrence": "H^2 alpha_j = suffixSum^2 + suffixSquareSum",
            "stateCountsByDepth": enumeration["stateCounts"],
            "transitionCountsByDepth": enumeration["transitionCounts"],
            "finalStates": enumeration["finalStates"],
        },
        "heatRates": {
            "definition": "H^2 alpha_j = k_j^2 + sum_{l=j+1}^7 p_l^2",
            "maximumIntegerRate": enumeration["maximumIntegerRate"],
            "maximumNormalizedRate": decimal(
                Fraction(int(enumeration["maximumIntegerRate"]), H * H)
            ),
        },
        "exactTaylor": {
            "completeHomogeneousIntegerCoefficients": [
                str(value) for value in coefficients
            ],
            "zerothCoefficient": str(coefficients[0]),
            "zeroTimeMass": str(enumeration["zeroTimeMass"]),
            "partialLower": str(partial_lower),
            "partialUpper": str(partial_upper),
            "partialLowerDisplay": decimal(partial_lower),
            "partialUpperDisplay": decimal(partial_upper),
            "absoluteTailBound": str(tail),
            "absoluteTailBoundDisplay": decimal(tail),
            "tailRatioBound": str(tail_ratio),
            "finalLower": str(final_lower),
            "finalUpper": str(final_upper),
            "finalLowerDisplay": decimal(final_lower),
            "finalUpperDisplay": decimal(final_upper),
            "finalLowerSha256": fraction_sha256(final_lower),
            "finalUpperSha256": fraction_sha256(final_upper),
        },
        "limitations": [
            "Only the first stationary four-bit block M=16 is certified.",
            "Its positive sign does not determine the dominant asymptotic heat projection.",
            "No statement is made about all Picard orders, singularity, or global regularity.",
        ],
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "provenance": {"sourceCommit": arguments.source_commit},
        "runtime": {"elapsedSeconds": time.perf_counter() - started},
    }
    serialized = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(serialized)
    progress(arguments.progress, started, "complete", checks=len(checks))
    sys.stdout.write(serialized)


if __name__ == "__main__":
    main()
