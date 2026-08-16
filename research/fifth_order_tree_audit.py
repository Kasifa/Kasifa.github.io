#!/usr/bin/env python3
"""Exact fifth-order tree and energy audit for the cone relay.

This script refines R0.12.  It writes every cone-chain frequency as

    K(delta) = delta**(-1) K[-1] + K[0],   delta = 4**(-n),

strips the scalar normalization from the four initial polarizations, and
performs the pure nonlinear Taylor recursion with exact ``Fraction``
arithmetic.  At Taylor order m it keeps Laurent powers

    -m <= ell <= 5-m.

This is sufficient for the delta**0 coefficient at order five: one further
Navier--Stokes interaction can lower the Laurent order by at most one.  The
full signed calculation aggregates equal output frequencies and catalyst
degrees before taking the limit.  Every negative Laurent coefficient then
cancels exactly.

The calculation isolates two objects:

* the coefficient at the next-shell target a_(n+1), split by its three
  possible six-leaf count vectors and by the ordered root split;
* the limiting H^(1/2) energy of the homogeneous degree-six coefficient,
  including every external frequency.

It is an exact finite-order algebra calculation.  It does not estimate the
Taylor remainder, derive a dense-packet envelope equation, or prove a
Navier--Stokes regularity or singularity result.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
from functools import reduce
import json
import math
from typing import Iterable

import numpy as np

from polarization_relay import geometry, relay_polarizations, unit
from two_shell_taylor import (
    ZERO,
    add_coefficient,
    add_fields,
    bilinear,
    catalyst_field,
    clean,
    hhalf_pairing,
    key,
    negative,
    pump_field,
)


Rational = Fraction
Vector = tuple[Rational, Rational, Rational]
Degree = tuple[int, ...]
FrequencyExpansion = tuple[Vector, Vector]
VectorSeries = dict[int, Vector]
Polynomial = dict[tuple[int, int], Rational]

ZERO_R = Rational(0)
ZERO_VECTOR: Vector = (ZERO_R, ZERO_R, ZERO_R)
MAXIMUM_ORDER = 5
NORMALIZATION_SQUARED = 216**2


def vector(values: Iterable[int | Rational]) -> Vector:
    """Return a three-component rational vector."""

    result = tuple(Rational(value) for value in values)
    if len(result) != 3:
        raise ValueError("A Fourier vector must have three components.")
    return result  # type: ignore[return-value]


def vector_add(left: Vector, right: Vector) -> Vector:
    return tuple(left[index] + right[index] for index in range(3))  # type: ignore[return-value]


def vector_scale(scalar: Rational | int, value: Vector) -> Vector:
    factor = Rational(scalar)
    return tuple(factor * component for component in value)  # type: ignore[return-value]


def dot(left: Vector, right: Vector) -> Rational:
    return sum(
        (left[index] * right[index] for index in range(3)),
        start=ZERO_R,
    )


def is_zero_vector(value: Vector) -> bool:
    return all(component == 0 for component in value)


def frequency_add(
    left: FrequencyExpansion,
    right: FrequencyExpansion,
) -> FrequencyExpansion:
    return vector_add(left[0], right[0]), vector_add(left[1], right[1])


def frequency_scale(
    scalar: int,
    value: FrequencyExpansion,
) -> FrequencyExpansion:
    return vector_scale(scalar, value[0]), vector_scale(scalar, value[1])


def is_zero_frequency(value: FrequencyExpansion) -> bool:
    return is_zero_vector(value[0]) and is_zero_vector(value[1])


POSITIVE_FREQUENCIES: tuple[FrequencyExpansion, ...] = (
    (
        vector([Rational(1, 6)] * 3),
        vector([Rational(1, 3), Rational(1, 3), Rational(-2, 3)]),
    ),
    (
        vector([Rational(1, 6)] * 3),
        vector([Rational(1, 3), Rational(-2, 3), Rational(1, 3)]),
    ),
    (
        vector([Rational(1, 3)] * 3),
        vector([Rational(-1, 3), Rational(2, 3), Rational(-1, 3)]),
    ),
    (
        vector([Rational(1, 3)] * 3),
        vector([Rational(-1, 3), Rational(-1, 3), Rational(2, 3)]),
    ),
)

# Exact polarization numerators.  Pump polarizations have the omitted scalar
# 1/(sqrt(6) sqrt(1+8 delta^2)); catalyst polarizations have
# 1/(sqrt(6) sqrt(1+2 delta^2)).  Every order-five tree has six leaves, so
# the common scalar at delta=0 is 1/216.
POSITIVE_POLARIZATION_SERIES: tuple[VectorSeries, ...] = (
    {0: vector([-1, -1, 2]), 1: vector([4, 4, 4])},
    {0: vector([1, -2, 1]), 1: vector([-4, -4, -4])},
    {0: vector([1, -2, 1]), 1: vector([2, 2, 2])},
    {0: vector([-1, -1, 2]), 1: vector([-2, -2, -2])},
)


def signed_frequencies() -> tuple[FrequencyExpansion, ...]:
    return POSITIVE_FREQUENCIES + tuple(
        frequency_scale(-1, frequency) for frequency in POSITIVE_FREQUENCIES
    )


def signed_polarizations() -> tuple[VectorSeries, ...]:
    # The selected polarizations are real, so the negative coefficient is the
    # same vector, not its negative.
    return POSITIVE_POLARIZATION_SERIES + POSITIVE_POLARIZATION_SERIES


def degree_add(left: Degree, right: Degree) -> Degree:
    return tuple(left[index] + right[index] for index in range(len(left)))


def degree_frequency(
    degree: Degree,
    frequencies: tuple[FrequencyExpansion, ...],
) -> FrequencyExpansion:
    result: FrequencyExpansion = (ZERO_VECTOR, ZERO_VECTOR)
    for multiplicity, frequency in zip(degree, frequencies, strict=True):
        result = frequency_add(result, frequency_scale(multiplicity, frequency))
    return result


def series_add(
    left: VectorSeries,
    right: VectorSeries,
    minimum_power: int,
    maximum_power: int,
) -> VectorSeries:
    result = {}
    for power in range(minimum_power, maximum_power + 1):
        value = vector_add(
            left.get(power, ZERO_VECTOR),
            right.get(power, ZERO_VECTOR),
        )
        if not is_zero_vector(value):
            result[power] = value
    return result


def series_scale(scalar: Rational | int, value: VectorSeries) -> VectorSeries:
    factor = Rational(scalar)
    if factor == 0:
        return {}
    return {
        power: vector_scale(factor, coefficient)
        for power, coefficient in value.items()
        if not is_zero_vector(coefficient)
    }


def add_scalar_coefficient(
    series: dict[int, Rational],
    power: int,
    value: Rational,
) -> None:
    series[power] = series.get(power, ZERO_R) + value


def inverse_quadratic_series(
    constant: Rational,
    linear: Rational,
    quadratic: Rational,
    maximum_power: int,
) -> list[Rational]:
    """Return coefficients of 1/(constant+linear*d+quadratic*d^2)."""

    coefficients = [1 / constant]
    for power in range(1, maximum_power + 1):
        value = linear * coefficients[power - 1]
        if power >= 2:
            value += quadratic * coefficients[power - 2]
        coefficients.append(-value / constant)
    return coefficients


def bilinear_series(
    left_degree: Degree,
    left: VectorSeries,
    right_degree: Degree,
    right: VectorSeries,
    frequencies: tuple[FrequencyExpansion, ...],
    minimum_power: int,
    maximum_power: int,
) -> VectorSeries:
    """Return the real coefficient behind one ordered Leray interaction."""

    right_frequency = degree_frequency(right_degree, frequencies)
    output_frequency = frequency_add(
        degree_frequency(left_degree, frequencies),
        right_frequency,
    )
    if is_zero_frequency(output_frequency):
        return {}

    # Scalar series for K_right dot left.
    scalar: dict[int, Rational] = {}
    for power, coefficient in left.items():
        if not is_zero_vector(right_frequency[0]):
            add_scalar_coefficient(
                scalar,
                power - 1,
                dot(right_frequency[0], coefficient),
            )
        add_scalar_coefficient(
            scalar,
            power,
            dot(right_frequency[1], coefficient),
        )
    scalar = {power: value for power, value in scalar.items() if value != 0}

    raw: VectorSeries = {}
    for left_power, scalar_value in scalar.items():
        for right_power, coefficient in right.items():
            output_power = left_power + right_power
            if minimum_power <= output_power <= maximum_power:
                raw[output_power] = vector_add(
                    raw.get(output_power, ZERO_VECTOR),
                    vector_scale(scalar_value, coefficient),
                )
    raw = {
        power: value
        for power, value in raw.items()
        if not is_zero_vector(value)
    }

    leading, offset = output_frequency
    if is_zero_vector(leading):
        denominator = dot(offset, offset)
        return {
            power: vector_add(
                coefficient,
                vector_scale(-dot(offset, coefficient) / denominator, offset),
            )
            for power, coefficient in raw.items()
        }

    # Divide K dot raw by K dot K.  Since
    # K dot K = delta^-2 (A+B delta+C delta^2), the quotient begins two
    # powers above the numerator.
    numerator: dict[int, Rational] = {}
    for power, coefficient in raw.items():
        add_scalar_coefficient(
            numerator,
            power - 1,
            dot(leading, coefficient),
        )
        add_scalar_coefficient(
            numerator,
            power,
            dot(offset, coefficient),
        )
    numerator = {
        power: value for power, value in numerator.items() if value != 0
    }
    if numerator:
        first_shifted_power = min(numerator) + 2
        inverse_order = max(0, maximum_power + 1 - first_shifted_power)
    else:
        inverse_order = 0
    inverse = inverse_quadratic_series(
        dot(leading, leading),
        2 * dot(leading, offset),
        dot(offset, offset),
        inverse_order,
    )
    quotient: dict[int, Rational] = {}
    for numerator_power, numerator_value in numerator.items():
        for inverse_power, inverse_value in enumerate(inverse):
            output_power = numerator_power + 2 + inverse_power
            if minimum_power <= output_power <= maximum_power + 1:
                add_scalar_coefficient(
                    quotient,
                    output_power,
                    numerator_value * inverse_value,
                )

    projected = {}
    for power in range(minimum_power, maximum_power + 1):
        correction = vector_add(
            vector_scale(quotient.get(power + 1, ZERO_R), leading),
            vector_scale(quotient.get(power, ZERO_R), offset),
        )
        value = vector_add(
            raw.get(power, ZERO_VECTOR),
            vector_scale(-1, correction),
        )
        if not is_zero_vector(value):
            projected[power] = value
    return projected


def pure_tree_coefficients(
    frequencies: tuple[FrequencyExpansion, ...],
    initial_polarizations: tuple[VectorSeries, ...],
) -> list[dict[Degree, VectorSeries]]:
    """Compute exact Laurent coefficients through nonlinear order five."""

    number_of_types = len(frequencies)
    coefficients: list[dict[Degree, VectorSeries]] = [
        {} for _ in range(MAXIMUM_ORDER + 1)
    ]
    for index, polarization in enumerate(initial_polarizations):
        degree = tuple(
            int(index == coordinate) for coordinate in range(number_of_types)
        )
        coefficients[0][degree] = dict(polarization)

    for order in range(MAXIMUM_ORDER):
        minimum_power = -(order + 1)
        maximum_power = MAXIMUM_ORDER - (order + 1)
        output: dict[Degree, VectorSeries] = {}
        for left_order in range(order + 1):
            right_order = order - left_order
            for left_degree, left in coefficients[left_order].items():
                for right_degree, right in coefficients[right_order].items():
                    degree = degree_add(left_degree, right_degree)
                    value = series_scale(
                        Rational(1, order + 1),
                        bilinear_series(
                            left_degree,
                            left,
                            right_degree,
                            right,
                            frequencies,
                            minimum_power,
                            maximum_power,
                        ),
                    )
                    output[degree] = series_add(
                        output.get(degree, {}),
                        value,
                        minimum_power,
                        maximum_power,
                    )
        coefficients[order + 1] = output
    return coefficients


TARGET_LEAF_COUNTS: tuple[Degree, ...] = (
    (1, 3, 2, 0),
    (2, 2, 1, 1),
    (3, 1, 0, 2),
)


def coefficient_sqrt6_fraction(value: Vector) -> Rational:
    """Return c when the target line scalar is c*sqrt(6)."""

    target_numerator = 2 * value[0] - value[1] - value[2]
    # The six initial unit normalizations contribute 1/216.  Projection onto
    # (2,-1,-1)/sqrt(6), with U_5=(-i)^5 R_5, contributes the remaining
    # sign and 1/sqrt(6).
    return -target_numerator / 1296


def positive_target_record() -> dict[str, object]:
    """Return exact target contributions for positive initial leaves."""

    coefficients = pure_tree_coefficients(
        POSITIVE_FREQUENCIES,
        POSITIVE_POLARIZATION_SERIES,
    )
    records = []
    total = ZERO_R
    for target_degree in TARGET_LEAF_COUNTS:
        value = coefficients[5][target_degree][0]
        coefficient = coefficient_sqrt6_fraction(value)
        total += coefficient
        root_splits = []
        for left_order in range(5):
            right_order = 4 - left_order
            split_value = ZERO_R
            for left_degree, left in coefficients[left_order].items():
                right_degree = tuple(
                    target_degree[index] - left_degree[index]
                    for index in range(4)
                )
                if min(right_degree) < 0:
                    continue
                right = coefficients[right_order].get(right_degree)
                if right is None:
                    continue
                contribution = series_scale(
                    Rational(1, 5),
                    bilinear_series(
                        left_degree,
                        left,
                        right_degree,
                        right,
                        POSITIVE_FREQUENCIES,
                        0,
                        0,
                    ),
                )
                split_value += coefficient_sqrt6_fraction(
                    contribution.get(0, ZERO_VECTOR)
                )
            root_splits.append(
                {
                    "leftOrder": left_order,
                    "rightOrder": right_order,
                    "coefficientSqrt6": fraction_string(split_value),
                    "decimal": float(split_value * square_root_six()),
                }
            )
        records.append(
            {
                "leafCounts": list(target_degree),
                "unnormalizedVector": [fraction_string(component) for component in value],
                "coefficientSqrt6": fraction_string(coefficient),
                "decimal": float(coefficient * square_root_six()),
                "rootSplits": root_splits,
            }
        )
    return {
        "leafClasses": records,
        "totalCoefficientSqrt6": fraction_string(total),
        "totalCoefficientDecimal": float(total * square_root_six()),
        "directedRelayCoefficientSqrt6": "-9/160",
        "directedRelayCoefficientDecimal": -9.0 * math.sqrt(6.0) / 160.0,
    }


def catalyst_degrees(degree: Degree) -> tuple[int, int]:
    """Return total b and d leaf counts for the signed eight-type degree."""

    return degree[2] + degree[6], degree[3] + degree[7]


def add_polynomial_coefficient(
    polynomial: Polynomial,
    powers: tuple[int, int],
    value: Rational,
) -> None:
    polynomial[powers] = polynomial.get(powers, ZERO_R) + value


def aggregate_signed_limit() -> tuple[
    dict[FrequencyExpansion, dict[tuple[int, int], Vector]],
    int,
]:
    """Aggregate signed order-five constants by output and catalyst degree."""

    frequencies = signed_frequencies()
    coefficients = pure_tree_coefficients(frequencies, signed_polarizations())
    aggregated: dict[
        tuple[FrequencyExpansion, tuple[int, int]],
        VectorSeries,
    ] = {}
    for degree, value in coefficients[5].items():
        output = degree_frequency(degree, frequencies)
        catalyst_degree = catalyst_degrees(degree)
        aggregate_key = (output, catalyst_degree)
        aggregated[aggregate_key] = series_add(
            aggregated.get(aggregate_key, {}),
            value,
            -5,
            0,
        )

    pole_count = 0
    by_frequency: dict[FrequencyExpansion, dict[tuple[int, int], Vector]] = (
        defaultdict(dict)
    )
    for (output, catalyst_degree), value in aggregated.items():
        for power in range(-5, 0):
            if not is_zero_vector(value.get(power, ZERO_VECTOR)):
                pole_count += 1
        constant = value.get(0, ZERO_VECTOR)
        if not is_zero_vector(constant):
            by_frequency[output][catalyst_degree] = constant
    return dict(by_frequency), pole_count


def energy_polynomial(
    by_frequency: dict[FrequencyExpansion, dict[tuple[int, int], Vector]],
    supports: set[FrequencyExpansion] | None = None,
) -> Polynomial:
    """Return E/sqrt(3) as a polynomial in the two catalyst amplitudes."""

    polynomial: Polynomial = {}
    for output, coefficient_by_degree in by_frequency.items():
        if supports is not None and output not in supports:
            continue
        leading = output[0]
        if is_zero_vector(leading):
            continue
        if not (leading[0] == leading[1] == leading[2]):
            raise AssertionError("All nonzero cone limits must be diagonal.")
        weight_over_sqrt_three = abs(leading[0])
        for (left_b, left_d), left in coefficient_by_degree.items():
            for (right_b, right_d), right in coefficient_by_degree.items():
                add_polynomial_coefficient(
                    polynomial,
                    (left_b + right_b, left_d + right_d),
                    weight_over_sqrt_three
                    * dot(left, right)
                    / NORMALIZATION_SQUARED,
                )
    return {
        powers: coefficient
        for powers, coefficient in polynomial.items()
        if coefficient != 0
    }


NEXT_A_POSITIVE: FrequencyExpansion = (
    vector([Rational(4, 3)] * 3),
    vector([Rational(2, 3), Rational(-1, 3), Rational(-1, 3)]),
)
NEXT_A_NEGATIVE = frequency_scale(-1, NEXT_A_POSITIVE)


def substitute_equal_amplitudes(
    polynomial: Polynomial,
    relative_sign: int,
) -> dict[int, Rational]:
    """Set b=epsilon and d=relative_sign*epsilon."""

    result: dict[int, Rational] = {}
    for (b_power, d_power), coefficient in polynomial.items():
        total_power = b_power + d_power
        result[total_power] = result.get(total_power, ZERO_R) + (
            relative_sign**d_power * coefficient
        )
    return {
        power: coefficient
        for power, coefficient in result.items()
        if coefficient != 0
    }


def polynomial_subtract(
    left: dict[int, Rational],
    right: dict[int, Rational],
) -> dict[int, Rational]:
    powers = set(left).union(right)
    return {
        power: left.get(power, ZERO_R) - right.get(power, ZERO_R)
        for power in powers
        if left.get(power, ZERO_R) != right.get(power, ZERO_R)
    }


def evaluate_univariate(polynomial: dict[int, Rational], value: float) -> float:
    return sum(float(coefficient) * value**power for power, coefficient in polynomial.items())


def least_common_multiple(left: int, right: int) -> int:
    return abs(left * right) // math.gcd(left, right)


def primitive_stationary_polynomial(
    external: dict[int, Rational],
) -> dict[int, int]:
    """Return the primitive integer polynomial for d/dz of X/T.

    Here z=epsilon^2 and the target is a positive constant times z^2.
    Multiplication by z^3 and by the target constant does not change positive
    stationary points, leaving sum_j (j-2) X_(2j) z^j.
    """

    rational_coefficients = {
        power // 2: Rational(power // 2 - 2) * coefficient
        for power, coefficient in external.items()
        if power % 2 == 0 and power // 2 != 2
    }
    common_denominator = reduce(
        least_common_multiple,
        (value.denominator for value in rational_coefficients.values()),
        1,
    )
    integer_coefficients = {
        power: value.numerator * (common_denominator // value.denominator)
        for power, value in rational_coefficients.items()
    }
    common_divisor = reduce(
        math.gcd,
        (abs(value) for value in integer_coefficients.values() if value != 0),
    )
    return {
        power: value // common_divisor
        for power, value in integer_coefficients.items()
        if value != 0
    }


def evaluate_integer_polynomial(polynomial: dict[int, int], value: float) -> float:
    return sum(coefficient * value**power for power, coefficient in polynomial.items())


def positive_root_by_bisection(polynomial: dict[int, int]) -> float:
    lower = 0.0
    upper = 1.0
    while evaluate_integer_polynomial(polynomial, upper) <= 0.0:
        upper *= 2.0
    for _ in range(200):
        middle = 0.5 * (lower + upper)
        if evaluate_integer_polynomial(polynomial, middle) <= 0.0:
            lower = middle
        else:
            upper = middle
    return 0.5 * (lower + upper)


def coefficient_sign_changes(polynomial: dict[int, int]) -> int:
    signs = [
        1 if polynomial[power] > 0 else -1
        for power in sorted(polynomial, reverse=True)
        if polynomial[power] != 0
    ]
    return sum(signs[index] != signs[index - 1] for index in range(1, len(signs)))


def symmetric_amplitude_record(
    total: Polynomial,
    target: Polynomial,
    relative_sign: int,
) -> dict[str, object]:
    total_one = substitute_equal_amplitudes(total, relative_sign)
    target_one = substitute_equal_amplitudes(target, relative_sign)
    external = polynomial_subtract(total_one, target_one)

    def ratio(epsilon: float) -> float:
        target_value = evaluate_univariate(target_one, epsilon)
        if target_value <= 0.0:
            return math.inf
        return evaluate_univariate(external, epsilon) / target_value

    stationary = primitive_stationary_polynomial(external)
    positive_root = positive_root_by_bisection(stationary)
    epsilon = math.sqrt(positive_root)
    minimum_ratio = ratio(epsilon)
    return {
        "relativeSign": relative_sign,
        "totalOverSqrt3": polynomial_record(total_one),
        "targetOverSqrt3": polynomial_record(target_one),
        "externalOverSqrt3": polynomial_record(external),
        "stationaryPolynomialInZ": [
            {"power": power, "coefficient": coefficient}
            for power, coefficient in sorted(stationary.items())
        ],
        "stationarySignChanges": coefficient_sign_changes(stationary),
        "optimalZ": positive_root,
        "optimalEpsilon": epsilon,
        "minimumExternalOverTarget": minimum_ratio,
        "maximumTargetFraction": 1.0 / (1.0 + minimum_ratio),
        "epsilonPointTwoExternalOverTarget": ratio(0.2),
        "epsilonPointTwoTargetFraction": 1.0 / (1.0 + ratio(0.2)),
    }


def energy_record() -> dict[str, object]:
    by_frequency, pole_count = aggregate_signed_limit()
    total = energy_polynomial(by_frequency)
    target = energy_polynomial(
        by_frequency,
        {NEXT_A_POSITIVE, NEXT_A_NEGATIVE},
    )
    external: Polynomial = {
        powers: total.get(powers, ZERO_R) - target.get(powers, ZERO_R)
        for powers in set(total).union(target)
        if total.get(powers, ZERO_R) != target.get(powers, ZERO_R)
    }
    target_vectors = {
        f"b^{b_power}d^{d_power}": [
            fraction_string(component)
            for component in by_frequency[NEXT_A_POSITIVE][(b_power, d_power)]
        ]
        for b_power, d_power in sorted(by_frequency[NEXT_A_POSITIVE])
    }
    return {
        "aggregatedFrequencyCount": len(by_frequency),
        "uncancelledLaurentPoleCount": pole_count,
        "targetVectors": target_vectors,
        "totalOverSqrt3": bivariate_polynomial_record(total),
        "targetOverSqrt3": bivariate_polynomial_record(target),
        "externalOverSqrt3": bivariate_polynomial_record(external),
        "equalPositiveCatalysts": symmetric_amplitude_record(total, target, 1),
        "equalOppositeCatalysts": symmetric_amplitude_record(total, target, -1),
    }


def pure_nonlinear_field(initial: dict) -> dict:
    coefficients = [initial]
    for order in range(5):
        output = {}
        for left_order in range(order + 1):
            for wavevector, value in bilinear(
                coefficients[left_order],
                coefficients[order - left_order],
            ).items():
                add_coefficient(output, wavevector, -value / (order + 1))
        coefficients.append(clean(output))
    return coefficients[5]


def finite_level_record(level: int, epsilon: float = 0.2) -> dict[str, float | int]:
    relay = relay_polarizations(level)
    initial = add_fields(
        pump_field(level),
        catalyst_field(level, epsilon, relay["B"], relay["D"]),
    )
    coefficient = pure_nonlinear_field(initial)
    next_a = geometry(level + 1)["a"]
    target_support = {key(next_a), negative(key(next_a))}
    total_energy = hhalf_pairing(coefficient, coefficient)
    target_energy = hhalf_pairing(coefficient, coefficient, target_support)
    current = geometry(level)
    value = coefficient[key(next_a)]
    target_direction = 1.0j * unit(current["eta"])
    target_scalar = float(np.vdot(target_direction, value).real)
    return {
        "level": level,
        "targetCoefficientPerEpsilonSquared": target_scalar / epsilon**2,
        "targetFraction": target_energy / total_energy,
        "externalOverTarget": (total_energy - target_energy) / target_energy,
        "supportCount": len(coefficient),
    }


def fraction_string(value: Rational) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def square_root_six() -> float:
    return math.sqrt(6.0)


def polynomial_record(polynomial: dict[int, Rational]) -> list[dict[str, object]]:
    return [
        {
            "power": power,
            "coefficient": fraction_string(coefficient),
            "decimal": float(coefficient),
        }
        for power, coefficient in sorted(polynomial.items())
    ]


def bivariate_polynomial_record(polynomial: Polynomial) -> list[dict[str, object]]:
    return [
        {
            "bPower": powers[0],
            "dPower": powers[1],
            "coefficient": fraction_string(coefficient),
            "decimal": float(coefficient),
        }
        for powers, coefficient in sorted(polynomial.items())
    ]


def audit() -> dict[str, object]:
    return {
        "convention": {
            "delta": "4^(-n)",
            "seriesWindowAtOrderM": "-m <= ell <= 5-m",
            "pureTaylorPhase": "U_m = (-i)^m R_m",
            "unitNormalizationAtOrderFive": "1/216",
        },
        "target": positive_target_record(),
        "energy": energy_record(),
        "finiteLevels": [finite_level_record(level) for level in range(3, 9)],
    }


def lookup_univariate(record: list[dict[str, object]]) -> dict[int, Rational]:
    return {
        int(item["power"]): Rational(str(item["coefficient"])) for item in record
    }


def validate(result: dict[str, object]) -> None:
    target = result["target"]
    assert target["totalCoefficientSqrt6"] == "47797/1120"
    assert [
        record["coefficientSqrt6"] for record in target["leafClasses"]
    ] == ["1273/1120", "45251/1120", "1273/1120"]
    assert target["directedRelayCoefficientSqrt6"] == "-9/160"

    energy = result["energy"]
    assert energy["uncancelledLaurentPoleCount"] == 0
    positive = energy["equalPositiveCatalysts"]
    total = lookup_univariate(positive["totalOverSqrt3"])
    target_energy = lookup_univariate(positive["targetOverSqrt3"])
    assert total == {
        0: Rational(69777, 3200),
        2: Rational(305080037, 39200),
        4: Rational(12206442914731, 12544000),
        6: Rational(113164737228373, 25088000),
        8: Rational(29552031913871, 25088000),
        10: Rational(36561930673, 1075200),
        12: Rational(69777, 1600),
    }
    assert target_energy == {4: Rational(2284553209, 78400)}
    assert positive["stationarySignChanges"] == 1
    assert {
        int(item["power"]): int(item["coefficient"])
        for item in positive["stationaryPolynomialInZ"]
    } == {
        0: -1094103360,
        1: -195251223680,
        3: 113164737228373,
        4: 59104063827742,
        5: 2559335147110,
        6: 4376413440,
    }
    assert abs(positive["optimalEpsilon"] - 0.2088762362) < 2.0e-9
    assert abs(positive["minimumExternalOverTarget"] - 45.73934896) < 1.0e-8
    assert (
        energy["equalOppositeCatalysts"]["minimumExternalOverTarget"]
        > positive["minimumExternalOverTarget"]
    )

    final = result["finiteLevels"][-1]
    assert abs(
        final["targetCoefficientPerEpsilonSquared"]
        - result["target"]["totalCoefficientDecimal"]
    ) < 1.0e-6
    assert abs(
        final["externalOverTarget"]
        - positive["epsilonPointTwoExternalOverTarget"]
    ) < 1.0e-6


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    result = audit()
    if arguments.check:
        validate(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
