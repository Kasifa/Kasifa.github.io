#!/usr/bin/env python3
"""R0.68B-2d exact all-multiindex derivative-majorant audit.

This audit removes binary64 arithmetic from the eleventh-derivative gate in
R0.68B-2c.  Every coefficient of the quadratic heat rates, every cube
supremum, every complete homogeneous polynomial, and every simplex integral
coefficient is evaluated in GMP rational arithmetic.  The only transcendental
quantity is T=log(2)/2=atanh(1/3); a positive rational series gives a proved
upper endpoint, and positivity of the majorant permits evaluation at that
endpoint.

The result is a strict derivative upper bound for one fixed eighth-order heat
packet.  It does not certify the binary64 moment lift or the observable defect,
and it is not a Navier--Stokes regularity result.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import itertools
import json
import math
import platform
import sys
import time
from pathlib import Path

import gmpy2

import eighth_order_heat_jet_pilot as jet


Rational = gmpy2.mpq
Poly = dict[tuple[int, ...], gmpy2.mpq]
VARIABLES = 6
DERIVATIVE_ORDER = 11
THETA = Rational(2, 15)
CENTER = Rational(1, 2)


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    if not enabled:
        return
    fields = " ".join(f"{key}={value}" for key, value in details.items())
    print(
        f"[R0.68B-2d exact derivative +{time.perf_counter() - started:8.2f}s] "
        f"{stage}{(' ' + fields) if fields else ''}",
        file=sys.stderr,
        flush=True,
    )


def poly_add(*values: Poly) -> Poly:
    output: collections.defaultdict[tuple[int, ...], gmpy2.mpq] = (
        collections.defaultdict(lambda: Rational(0))
    )
    for value in values:
        for alpha, coefficient in value.items():
            output[alpha] += coefficient
    return {alpha: coefficient for alpha, coefficient in output.items() if coefficient}


def poly_scale(value: Poly, scalar: gmpy2.mpq) -> Poly:
    return {
        alpha: coefficient * scalar
        for alpha, coefficient in value.items()
        if coefficient * scalar
    }


def poly_multiply(left: Poly, right: Poly) -> Poly:
    output: collections.defaultdict[tuple[int, ...], gmpy2.mpq] = (
        collections.defaultdict(lambda: Rational(0))
    )
    for left_alpha, left_value in left.items():
        for right_alpha, right_value in right.items():
            alpha = tuple(
                left_alpha[index] + right_alpha[index]
                for index in range(VARIABLES)
            )
            output[alpha] += left_value * right_value
    return {alpha: coefficient for alpha, coefficient in output.items() if coefficient}


def truncated_poly_multiply(left: Poly, right: Poly, maximum_degree: int) -> Poly:
    output: collections.defaultdict[tuple[int, ...], gmpy2.mpq] = (
        collections.defaultdict(lambda: Rational(0))
    )
    for left_alpha, left_value in left.items():
        left_degree = sum(left_alpha)
        for right_alpha, right_value in right.items():
            if left_degree + sum(right_alpha) > maximum_degree:
                continue
            alpha = tuple(
                left_alpha[index] + right_alpha[index]
                for index in range(VARIABLES)
            )
            output[alpha] += left_value * right_value
    return {alpha: coefficient for alpha, coefficient in output.items() if coefficient}


def poly_linear(constant: gmpy2.mpq, coefficients: list[gmpy2.mpq]) -> Poly:
    output: Poly = {(0,) * VARIABLES: constant}
    for coordinate, coefficient in enumerate(coefficients):
        if coefficient:
            alpha = [0] * VARIABLES
            alpha[coordinate] = 1
            output[tuple(alpha)] = coefficient
    return output


def poly_derivative(value: Poly, coordinate: int) -> Poly:
    output: collections.defaultdict[tuple[int, ...], gmpy2.mpq] = (
        collections.defaultdict(lambda: Rational(0))
    )
    for alpha, coefficient in value.items():
        if alpha[coordinate]:
            beta = list(alpha)
            beta[coordinate] -= 1
            output[tuple(beta)] += coefficient * alpha[coordinate]
    return {alpha: coefficient for alpha, coefficient in output.items() if coefficient}


def poly_cube_supremum(value: Poly) -> gmpy2.mpq:
    return max(
        abs(
            sum(
                (
                    coefficient
                    * math.prod(
                        point[coordinate] ** alpha[coordinate]
                        for coordinate in range(VARIABLES)
                    )
                    for alpha, coefficient in value.items()
                ),
                Rational(0),
            )
        )
        for point in itertools.product((0, 1), repeat=VARIABLES)
    )


def rate_polynomials(word: tuple[int, ...]) -> list[Poly]:
    zero = Rational(0)
    one = Rational(1)
    quarter = Rational(1, 4)
    variables = [
        poly_linear(
            CENTER,
            [one if other == coordinate else zero for other in range(VARIABLES)],
        )
        for coordinate in range(VARIABLES)
    ]
    constant_one = poly_linear(one, [zero] * VARIABLES)
    dependent = poly_add(
        variables[0],
        variables[1],
        variables[2],
        variables[3],
        poly_scale(variables[4], -one),
        poly_scale(variables[5], -one),
        poly_linear(-THETA, [zero] * VARIABLES),
    )
    magnitudes = [
        poly_add(constant_one, poly_scale(variables[index], quarter))
        for index in range(VARIABLES)
    ] + [poly_add(constant_one, poly_scale(dependent, quarter))]
    positives = iter(magnitudes[:4])
    negatives = iter(magnitudes[4:])
    carriers = [
        next(positives) if sign > 0 else poly_scale(next(negatives), -one)
        for sign in word
    ]
    current = poly_linear(-(one + THETA * quarter), [zero] * VARIABLES)
    suffix = poly_add(*(poly_multiply(value, value) for value in carriers))
    rates = []
    for carrier in carriers:
        rates.append(poly_add(poly_multiply(current, current), suffix))
        suffix = poly_add(
            suffix, poly_scale(poly_multiply(carrier, carrier), -one)
        )
        current = poly_add(current, carrier)
    return rates


def rate_majorant(rate: Poly) -> Poly:
    first = [
        poly_cube_supremum(poly_derivative(rate, coordinate))
        for coordinate in range(VARIABLES)
    ]
    second = [
        [
            poly_cube_supremum(
                poly_derivative(
                    poly_derivative(rate, left_coordinate), right_coordinate
                )
            )
            for right_coordinate in range(VARIABLES)
        ]
        for left_coordinate in range(VARIABLES)
    ]
    majorant: Poly = {}
    for coordinate, value in enumerate(first):
        if value:
            alpha = [0] * VARIABLES
            alpha[coordinate] = 1
            majorant[tuple(alpha)] = value
    for left_coordinate in range(VARIABLES):
        for right_coordinate in range(left_coordinate, VARIABLES):
            value = second[left_coordinate][right_coordinate]
            if not value:
                continue
            alpha = [0] * VARIABLES
            alpha[left_coordinate] += 1
            alpha[right_coordinate] += 1
            majorant[tuple(alpha)] = value * (
                Rational(1, 2) if left_coordinate == right_coordinate else 1
            )
    return majorant


def time_enclosure(terms: int) -> tuple[gmpy2.mpq, gmpy2.mpq]:
    """Enclose log(2)/2=atanh(1/3) by positive rational series."""
    x = Rational(1, 3)
    lower = sum(
        (x ** (2 * index + 1)) / (2 * index + 1)
        for index in range(terms)
    )
    first_omitted = 2 * terms + 1
    remainder = x**first_omitted / first_omitted / (1 - x * x)
    return lower, lower + remainder


def rational_record(value: gmpy2.mpq) -> dict[str, str]:
    numerator = str(gmpy2.numer(value))
    denominator = str(gmpy2.denom(value))
    canonical = f"{numerator}/{denominator}"
    decimal = format(gmpy2.mpfr(value, 256), ".40g")
    return {
        "numerator": numerator,
        "denominator": denominator,
        "decimal": decimal,
        "sha256": hashlib.sha256(canonical.encode("ascii")).hexdigest(),
    }


def exact_derivative_majorants(
    time_upper: gmpy2.mpq,
    shuffle_limit: int,
    report_progress: bool,
    started: float,
) -> tuple[dict[tuple[int, ...], gmpy2.mpq], list[dict[str, object]], gmpy2.mpq]:
    zero = (0,) * VARIABLES
    total: collections.defaultdict[tuple[int, ...], gmpy2.mpq] = (
        collections.defaultdict(lambda: Rational(0))
    )
    records = []
    sum_wordwise_maxima = Rational(0)
    words = jet.shuffle_words()[:shuffle_limit]
    expected_count = math.comb(
        DERIVATIVE_ORDER + VARIABLES - 1, VARIABLES - 1
    )
    time_scalars = [
        time_upper ** (order + 7) / math.factorial(order + 7)
        for order in range(DERIVATIVE_ORDER + 1)
    ]
    factorials = [math.factorial(index) for index in range(DERIVATIVE_ORDER + 1)]
    for word_index, word in enumerate(words):
        majorants = [rate_majorant(rate) for rate in rate_polynomials(word)]
        homogeneous: list[Poly] = [{} for _ in range(DERIVATIVE_ORDER + 1)]
        homogeneous[0] = {zero: Rational(1)}
        for majorant in majorants:
            updated: list[Poly] = [{} for _ in range(DERIVATIVE_ORDER + 1)]
            updated[0] = homogeneous[0]
            for order in range(1, DERIVATIVE_ORDER + 1):
                updated[order] = poly_add(
                    homogeneous[order],
                    truncated_poly_multiply(
                        majorant, updated[order - 1], DERIVATIVE_ORDER
                    ),
                )
            homogeneous = updated

        word_values: collections.defaultdict[tuple[int, ...], gmpy2.mpq] = (
            collections.defaultdict(lambda: Rational(0))
        )
        for order, value in enumerate(homogeneous):
            scalar = time_scalars[order]
            for alpha, coefficient in value.items():
                if sum(alpha) != DERIVATIVE_ORDER:
                    continue
                word_values[alpha] += (
                    scalar
                    * coefficient
                    * math.prod(factorials[exponent] for exponent in alpha)
                )
        if len(word_values) != expected_count:
            raise AssertionError(
                f"shuffle {word_index + 1} has {len(word_values)} derivative "
                f"channels rather than {expected_count}"
            )
        for alpha, value in word_values.items():
            total[alpha] += value
        maximum_alpha = max(word_values, key=word_values.get)
        maximum = word_values[maximum_alpha]
        sum_wordwise_maxima += maximum
        records.append(
            {
                "word": list(word),
                "maximumMultiindex": list(maximum_alpha),
                "maximumUpper": rational_record(maximum),
                "multiindexCount": len(word_values),
            }
        )
        progress(
            report_progress,
            started,
            "exact derivative majorants",
            shuffle=f"{word_index + 1}/{len(words)}",
            multiindices=len(word_values),
            maximum=rational_record(maximum)["decimal"],
        )
    return dict(total), records, sum_wordwise_maxima


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--source-commit", default="uncommitted")
    parser.add_argument("--time-terms", type=int, default=120)
    parser.add_argument("--shuffle-limit", type=int, default=35)
    parser.add_argument("--progress", action="store_true")
    arguments = parser.parse_args()
    if arguments.time_terms < 2:
        parser.error("--time-terms must be at least 2")
    if not 1 <= arguments.shuffle_limit <= len(jet.shuffle_words()):
        parser.error("--shuffle-limit must be between 1 and 35")

    started = time.perf_counter()
    time_lower, time_upper = time_enclosure(arguments.time_terms)
    progress(
        arguments.progress,
        started,
        "time enclosed",
        terms=arguments.time_terms,
        width=rational_record(time_upper - time_lower)["decimal"],
    )
    values, per_shuffle, sum_wordwise_maxima = exact_derivative_majorants(
        time_upper,
        arguments.shuffle_limit,
        arguments.progress,
        started,
    )
    maximum_alpha = max(values, key=values.get)
    maximum = values[maximum_alpha]
    pure = [
        values[
            tuple(
                DERIVATIVE_ORDER if coordinate == selected else 0
                for coordinate in range(VARIABLES)
            )
        ]
        for selected in range(VARIABLES)
    ]
    canonical_vector = "\n".join(
        f"{','.join(map(str, alpha))}:{gmpy2.numer(values[alpha])}/"
        f"{gmpy2.denom(values[alpha])}"
        for alpha in sorted(values)
    )
    full_run = arguments.shuffle_limit == len(jet.shuffle_words())
    checks = {
        "timeEnclosureHasPositiveWidth": time_lower < time_upper,
        "allDerivativeMultiindicesArePresent": len(values)
        == math.comb(DERIVATIVE_ORDER + VARIABLES - 1, VARIABLES - 1),
        "allCoefficientsAreStrictlyPositive": all(value > 0 for value in values.values()),
        "exactMaximumIsBelowTwoPointFiveSixSevenEminusSix": maximum
        < Rational(2567, 1_000_000_000),
        "worstDerivativeIsPureFourthCoordinate": (
            not full_run or maximum_alpha == (0, 0, 0, 11, 0, 0)
        ),
    }
    if not all(checks.values()):
        raise AssertionError(f"exact derivative checks failed: {checks}")

    report = {
        "schemaVersion": "1.0",
        "status": "strict-passed" if full_run else "diagnostic-passed",
        "classification": (
            "GMP exact-rational complete all-multiindex eleventh-derivative "
            "majorant with a proved rational upper enclosure of log(2)/2"
        ),
        "checks": checks,
        "parameters": {
            "spatialVariables": VARIABLES,
            "derivativeOrder": DERIVATIVE_ORDER,
            "shuffleCount": arguments.shuffle_limit,
            "timeTerms": arguments.time_terms,
        },
        "timeEnclosure": {
            "identity": "log(2)/2 = atanh(1/3)",
            "lower": rational_record(time_lower),
            "upper": rational_record(time_upper),
            "width": rational_record(time_upper - time_lower),
            "remainderArgument": (
                "For positive terms x^(2n+1)/(2n+1), the omitted tail is "
                "at most x^(2N+1)/((2N+1)(1-x^2)) at x=1/3."
            ),
        },
        "derivativeMajorant": {
            "multiindexCount": len(values),
            "maximumMultiindex": list(maximum_alpha),
            "maximumUpper": rational_record(maximum),
            "pureMultiindexUppers": [rational_record(value) for value in pure],
            "sumOfWordwiseMaximaUpper": rational_record(sum_wordwise_maxima),
            "exactVectorSha256": hashlib.sha256(
                canonical_vector.encode("ascii")
            ).hexdigest(),
            "canonicalVectorFormat": (
                "lexicographic alpha as comma-separated integers, colon, "
                "reduced numerator/denominator, newline separated"
            ),
            "perShuffle": per_shuffle,
        },
        "provenance": {
            "sourceCommit": arguments.source_commit,
            "exactBackend": f"gmpy2 {gmpy2.version()} / {gmpy2.mp_version()}",
        },
        "runtime": {
            "elapsedSeconds": time.perf_counter() - started,
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "limitations": [
            "This certificate covers the complete eleventh-derivative majorant only.",
            "The dominant moment lift, heat jet, and observable defect still require rigorous enclosures.",
            "The fixed parallel-shear packet does not imply general three-dimensional Navier-Stokes regularity.",
        ],
    }
    serialized = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(serialized)
    sys.stdout.write(serialized)
    progress(
        arguments.progress,
        started,
        "complete",
        maximum=rational_record(maximum)["decimal"],
        multiindex=list(maximum_alpha),
    )


if __name__ == "__main__":
    main()
