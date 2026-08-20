#!/usr/bin/env python3
"""Exact one-cycle audit for the complete R0.67C sixth-order heat observable.

For the first four-bit cycle M=16 and q=2, enumerate every solution of

    A+B+C-D-E=Q,

and all ten (3,2)-shuffle time orderings.  The five-simplex kernel is expanded
in complete homogeneous polynomials of its five nonzero heat rates.  All
Taylor coefficients and the enclosure of T=log(2)/2 are exact rationals; the
omitted series is bounded absolutely.

This is a finite-scale sign certificate.  It is not a certificate for the
dominant asymptotic heat projection and not a Navier--Stokes regularity result.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import sys
import time
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

import sixth_order_cycle_audit as r067


M = 16
Q_OFFSET = 2
H = 4 * M
DEFAULT_ORDER = 32

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    if not enabled:
        return
    fields = " ".join(f"{key}={value}" for key, value in details.items())
    print(
        f"[R0.67C one-cycle +{time.perf_counter() - started:8.2f}s] "
        f"{stage}{(' ' + fields) if fields else ''}",
        file=sys.stderr,
        flush=True,
    )


def shuffle_words() -> list[tuple[int, ...]]:
    words: list[tuple[int, ...]] = []
    for positive_positions in itertools.combinations(range(5), 3):
        positive = set(positive_positions)
        words.append(tuple(1 if index in positive else -1 for index in range(5)))
    return words


def complete_homogeneous_values(rates: list[int], order: int) -> list[int]:
    """Return h_0,...,h_order for five integer heat rates."""
    values = [1] + [0] * order
    for rate in rates:
        for degree in range(1, order + 1):
            values[degree] += rate * values[degree - 1]
    return values


def path_rates(
    word: tuple[int, ...], magnitudes: tuple[int, int, int, int, int]
) -> tuple[list[int], int]:
    """Return H^2 alpha_0,...,H^2 alpha_4 and the final frequency."""
    a, b, c, d, e = magnitudes
    positives = iter((a, b, c))
    negatives = iter((d, e))
    carriers = [
        next(positives) if sign > 0 else -next(negatives) for sign in word
    ]
    current = -(H + Q_OFFSET)
    suffix_square = sum(carrier * carrier for carrier in carriers)
    rates: list[int] = []
    for carrier in carriers:
        rates.append(current * current + suffix_square)
        suffix_square -= carrier * carrier
        current += carrier
    return rates, current


def time_enclosure(terms: int = 120) -> tuple[Fraction, Fraction]:
    """Enclose log(2)/2=atanh(1/3) by a positive rational series."""
    x = Fraction(1, 3)
    lower = sum(
        (x ** (2 * index + 1)) / (2 * index + 1) for index in range(terms)
    )
    first_omitted = 2 * terms + 1
    remainder = x**first_omitted / first_omitted / (1 - x * x)
    return lower, lower + remainder


def decimal(value: Fraction, digits: int = 48) -> str:
    with localcontext() as context:
        context.prec = digits
        return format(Decimal(value.numerator) / Decimal(value.denominator), ".40E")


def fraction_sha256(value: Fraction) -> str:
    return hashlib.sha256(
        f"{value.numerator}/{value.denominator}".encode("ascii")
    ).hexdigest()


def interval_taylor_sum(
    coefficients: list[int], time_lower: Fraction, time_upper: Fraction
) -> tuple[Fraction, Fraction]:
    lower = Fraction(0)
    upper = Fraction(0)
    for degree, coefficient in enumerate(coefficients):
        scalar = Fraction(
            (-1) ** degree * coefficient,
            H ** (2 * degree) * math.factorial(degree + 5),
        )
        power = degree + 5
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
    """Bound the complete-homogeneous Taylor tail for every signed path."""
    first_degree = order + 1
    alpha_bound = Fraction(maximum_integer_rate, H * H)
    z = alpha_bound * time_upper
    ratio = z / (first_degree + 1)
    if ratio >= 1:
        raise ValueError("Taylor order is too small for the geometric tail")
    first = (
        path_count
        * time_upper**5
        / 24
        * z**first_degree
        / ((first_degree + 5) * math.factorial(first_degree))
    )
    return first / (1 - ratio), ratio


def enumerate_coefficients(
    order: int, report_progress: bool, started: float
) -> dict[str, object]:
    pair, _companion = r067.rudin_shapiro_pair(4)
    words = shuffle_words()
    coefficients = [0] * (order + 1)
    valid_tuples = 0
    zero_time_mass = 0
    maximum_rate = 0
    endpoint_failures = 0

    for a in range(M):
        carrier_a = H + a
        sign_a = pair[a]
        for b in range(M):
            carrier_b = H + b
            sign_ab = sign_a * pair[b]
            for c in range(M):
                carrier_c = H + c
                sign_abc = sign_ab * pair[c]
                for d in range(M):
                    e = a + b + c - d - Q_OFFSET
                    if not 0 <= e < M:
                        continue
                    valid_tuples += 1
                    signed_weight = (
                        pair[Q_OFFSET]
                        * sign_abc
                        * pair[d]
                        * pair[e]
                    )
                    zero_time_mass += signed_weight
                    magnitudes = (
                        carrier_a,
                        carrier_b,
                        carrier_c,
                        H + d,
                        H + e,
                    )
                    for word in words:
                        rates, endpoint = path_rates(word, magnitudes)
                        endpoint_failures += endpoint != 0
                        maximum_rate = max(maximum_rate, *rates)
                        values = complete_homogeneous_values(rates, order)
                        for degree, value in enumerate(values):
                            coefficients[degree] += signed_weight * value
        if (a + 1) % 4 == 0:
            progress(
                report_progress,
                started,
                "enumeration",
                carrierA=f"{a + 1}/{M}",
                validTuples=valid_tuples,
            )

    return {
        "words": words,
        "coefficients": coefficients,
        "validTuples": valid_tuples,
        "zeroTimeMass": zero_time_mass,
        "maximumIntegerRate": maximum_rate,
        "endpointFailures": endpoint_failures,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--order", type=int, default=DEFAULT_ORDER)
    parser.add_argument("--source-commit")
    parser.add_argument("--progress", action="store_true")
    arguments = parser.parse_args()
    if arguments.order < 16:
        raise ValueError("order must be at least 16 for a useful finite certificate")
    started = time.perf_counter()

    progress(arguments.progress, started, "starting", order=arguments.order)
    enumeration = enumerate_coefficients(arguments.order, arguments.progress, started)
    coefficients = enumeration["coefficients"]
    assert isinstance(coefficients, list)
    time_lower, time_upper = time_enclosure()
    partial_lower, partial_upper = interval_taylor_sum(
        coefficients, time_lower, time_upper
    )
    path_count = int(enumeration["validTuples"]) * 10
    tail, tail_ratio = absolute_tail_bound(
        arguments.order,
        path_count,
        int(enumeration["maximumIntegerRate"]),
        time_upper,
    )
    final_lower = partial_lower - tail
    final_upper = partial_upper + tail
    zero_time_mass = int(enumeration["zeroTimeMass"])

    checks = {
        "tenDistinctThreePlusTwoMinusWords": len(set(enumeration["words"])) == 10,
        "everyEnumeratedPathEndsAtZero": enumeration["endpointFailures"] == 0,
        "zerothTaylorCoefficientIsTenTimesZeroTimeMass": coefficients[0]
        == 10 * zero_time_mass,
        "zeroTimeMassMatchesR067AFirstCycle": zero_time_mass == 500,
        "maximumIntegerRateMatchesEnumeration": enumeration["maximumIntegerRate"]
        == 67_014,
        "tailGeometricRatioIsBelowOne": tail_ratio < 1,
        "absoluteTailIsBelowTwoTimesTenToMinusTwelve": tail
        < Fraction(2, 10**12),
        "completeOneCycleHeatCoefficientIsStrictlyPositive": final_lower > 0,
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    report = {
        "schemaVersion": "1.0",
        "status": "passed",
        "classification": (
            "exact finite-scale positive sign certificate for the complete "
            "sixth-order five-simplex heat observable at M=16 and q=2; not "
            "a dominant asymptotic projection certificate and not a "
            "Navier-Stokes regularity theorem"
        ),
        "checks": checks,
        "parameters": {
            "M": M,
            "q": Q_OFFSET,
            "Q": H + Q_OFFSET,
            "H": H,
            "time": "T=log(2)/2",
            "TaylorOrder": arguments.order,
            "validCarrierTuples": enumeration["validTuples"],
            "timeOrderings": 10,
            "signedPaths": path_count,
        },
        "heatRates": {
            "definition": "H^2 alpha_j = k_j^2 + sum_{l=j+1}^5 p_l^2",
            "maximumIntegerRate": enumeration["maximumIntegerRate"],
            "maximumNormalizedRate": decimal(
                Fraction(int(enumeration["maximumIntegerRate"]), H * H)
            ),
        },
        "exactTaylor": {
            "completeHomogeneousIntegerCoefficients": [str(value) for value in coefficients],
            "zerothCoefficient": str(coefficients[0]),
            "zeroTimeMass": str(zero_time_mass),
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
            "Only the first stationary four-bit cycle M=16 is certified.",
            "A positive finite-scale sign does not determine the dominant mu-projection.",
            "No statement is made about higher Picard orders, singularity, or global regularity.",
        ],
        "provenance": {"sourceCommit": arguments.source_commit},
        "runtime": {"elapsedSeconds": time.perf_counter() - started},
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    progress(arguments.progress, started, "complete", checks=len(checks))
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
