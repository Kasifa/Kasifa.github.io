#!/usr/bin/env python3
"""Exact second-variation audit for the four input polarizations.

R0.15 propagated the four first polarization derivatives through the signed
fifth-order cone tree.  This script propagates every first and second partial
derivative.  Its first purpose is structural: a finite Hessian is meaningful
only if every differentiated Laurent pole still cancels after equal-frequency
aggregation.

For parameter indices i,j in {0,1,2,3}, derivative keys are (), (i,), and
(i,j) with i <= j.  They store actual derivatives, not Taylor coefficients.
The bilinear product therefore carries the usual factor two when two equal
first derivatives form a diagonal second derivative.

The input chart is the exact normalized divergence-free curve used in R0.15,

    p(t,delta) = (N+t M)/(|N| sqrt(1+t^2 kappa)),
    M = (delta K) cross N,  kappa = |delta K|^2.

Thus p'(0) has numerator M and p''(0) has numerator -kappa N.  After the tree
calculation, the script forms the four-by-four quotient Hessian and its mixed
derivatives with the equal-catalyst amplitude variable x.  Exact rational
intervals are evaluated at the algebraic R0.15 minimizer.

This is a finite-order local calculation.  It does not optimize the complete
polarization torus or estimate a Navier--Stokes remainder.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
import hashlib
import json
import math

import numpy as np
import sympy as sp

import fifth_order_tree_audit as tree
import polarization_first_variation_audit as first
import two_amplitude_global_audit as amplitude


Rational = Fraction
Vector = tree.Vector
VectorSeries = tree.VectorSeries
Degree = tree.Degree
FrequencyExpansion = tree.FrequencyExpansion
Polynomial = dict[int, Rational]
DerivativeKey = tuple[int, ...]
JetSeries = dict[DerivativeKey, VectorSeries]

PARAMETER_LABELS = first.PARAMETER_LABELS
X_VAR = amplitude.X_VAR
BASE_KEY: DerivativeKey = ()
FIRST_KEYS: tuple[DerivativeKey, ...] = tuple((index,) for index in range(4))
SECOND_KEYS: tuple[DerivativeKey, ...] = tuple(
    (left, right)
    for left in range(4)
    for right in range(left, 4)
)
ALL_KEYS = (BASE_KEY, *FIRST_KEYS, *SECOND_KEYS)
CHART_SPEEDS_SQUARED = (
    sp.Rational(1, 12),
    sp.Rational(1, 12),
    sp.Rational(1, 3),
    sp.Rational(1, 3),
)


def scalar_vector_series_multiply(
    scalar: dict[int, Rational],
    vector: VectorSeries,
) -> VectorSeries:
    result: VectorSeries = {}
    for scalar_power, scalar_value in scalar.items():
        for vector_power, vector_value in vector.items():
            power = scalar_power + vector_power
            result[power] = tree.vector_add(
                result.get(power, tree.ZERO_VECTOR),
                tree.vector_scale(scalar_value, vector_value),
            )
    return {
        power: value
        for power, value in result.items()
        if not tree.is_zero_vector(value)
    }


def initial_jets() -> tuple[JetSeries, ...]:
    positive: list[JetSeries] = []
    for index, (frequency, polarization) in enumerate(
        zip(
            tree.POSITIVE_FREQUENCIES,
            tree.POSITIVE_POLARIZATION_SERIES,
            strict=True,
        )
    ):
        kbar = {0: frequency[0], 1: frequency[1]}
        tangent = first.tangent_series(frequency, polarization)
        kappa = first.scalar_series_dot(kbar, kbar)
        second = tree.series_scale(
            Rational(-1),
            scalar_vector_series_multiply(kappa, polarization),
        )
        jet: JetSeries = {
            BASE_KEY: dict(polarization),
            (index,): tangent,
            (index, index): second,
        }
        positive.append(jet)
    # The negative Fourier coefficient follows the same real polarization
    # curve as its positive partner.
    return tuple(positive + positive)


def combine_keys(
    left: DerivativeKey,
    right: DerivativeKey,
) -> tuple[DerivativeKey, int] | None:
    combined = tuple(sorted((*left, *right)))
    if len(combined) > 2:
        return None
    factor = 1
    for parameter in range(4):
        left_count = left.count(parameter)
        right_count = right.count(parameter)
        factor *= math.comb(left_count + right_count, left_count)
    return combined, factor


def jet_add(
    left: JetSeries,
    right: JetSeries,
    minimum: int,
    maximum: int,
) -> JetSeries:
    result: JetSeries = {}
    for key in set(left).union(right):
        value = tree.series_add(
            left.get(key, {}),
            right.get(key, {}),
            minimum,
            maximum,
        )
        if value:
            result[key] = value
    return result


def jet_scale(value: Rational, jet: JetSeries) -> JetSeries:
    return {
        key: scaled
        for key, component in jet.items()
        if (scaled := tree.series_scale(value, component))
    }


def jet_bilinear(
    left_degree: Degree,
    left: JetSeries,
    right_degree: Degree,
    right: JetSeries,
    frequencies: tuple[FrequencyExpansion, ...],
    minimum: int,
    maximum: int,
) -> JetSeries:
    result: JetSeries = {}
    for left_key, left_value in left.items():
        for right_key, right_value in right.items():
            combination = combine_keys(left_key, right_key)
            if combination is None:
                continue
            output_key, factor = combination
            value = tree.bilinear_series(
                left_degree,
                left_value,
                right_degree,
                right_value,
                frequencies,
                minimum,
                maximum,
            )
            if factor != 1:
                value = tree.series_scale(Rational(factor), value)
            if not value:
                continue
            result[output_key] = tree.series_add(
                result.get(output_key, {}),
                value,
                minimum,
                maximum,
            )
    return result


def differentiated_tree() -> list[dict[Degree, JetSeries]]:
    frequencies = tree.signed_frequencies()
    jets = initial_jets()
    coefficients: list[dict[Degree, JetSeries]] = [
        {} for _ in range(tree.MAXIMUM_ORDER + 1)
    ]
    for index, jet in enumerate(jets):
        degree = tuple(
            int(index == coordinate) for coordinate in range(len(frequencies))
        )
        coefficients[0][degree] = jet

    for order in range(tree.MAXIMUM_ORDER):
        minimum = -(order + 1)
        maximum = tree.MAXIMUM_ORDER - (order + 1)
        output: dict[Degree, JetSeries] = {}
        for left_order in range(order + 1):
            right_order = order - left_order
            for left_degree, left in coefficients[left_order].items():
                for right_degree, right in coefficients[right_order].items():
                    degree = tree.degree_add(left_degree, right_degree)
                    value = jet_scale(
                        Rational(1, order + 1),
                        jet_bilinear(
                            left_degree,
                            left,
                            right_degree,
                            right,
                            frequencies,
                            minimum,
                            maximum,
                        ),
                    )
                    output[degree] = jet_add(
                        output.get(degree, {}),
                        value,
                        minimum,
                        maximum,
                    )
        coefficients[order + 1] = output
    return coefficients


def aggregate_limit() -> tuple[
    dict[
        FrequencyExpansion,
        dict[tuple[int, int], dict[DerivativeKey, Vector]],
    ],
    dict[DerivativeKey, int],
]:
    frequencies = tree.signed_frequencies()
    coefficients = differentiated_tree()
    aggregated: dict[
        tuple[FrequencyExpansion, tuple[int, int]],
        JetSeries,
    ] = {}
    for degree, jet in coefficients[5].items():
        output = tree.degree_frequency(degree, frequencies)
        catalyst_degree = tree.catalyst_degrees(degree)
        key = output, catalyst_degree
        aggregated[key] = jet_add(
            aggregated.get(key, {}),
            jet,
            -5,
            0,
        )

    pole_counts = {key: 0 for key in ALL_KEYS}
    by_frequency: dict[
        FrequencyExpansion,
        dict[tuple[int, int], dict[DerivativeKey, Vector]],
    ] = defaultdict(dict)
    for (output, catalyst_degree), jet in aggregated.items():
        for key in ALL_KEYS:
            component = jet.get(key, {})
            for power in range(-5, 0):
                if not tree.is_zero_vector(
                    component.get(power, tree.ZERO_VECTOR)
                ):
                    pole_counts[key] += 1
        constants = {
            key: component[0]
            for key, component in jet.items()
            if 0 in component and not tree.is_zero_vector(component[0])
        }
        if constants:
            by_frequency[output][catalyst_degree] = constants
    return dict(by_frequency), pole_counts


def add_polynomial(polynomial: Polynomial, power: int, value: Rational) -> None:
    polynomial[power] = polynomial.get(power, tree.ZERO_R) + value


def energy_jets(
    by_frequency: dict[
        FrequencyExpansion,
        dict[tuple[int, int], dict[DerivativeKey, Vector]],
    ],
    supports: set[FrequencyExpansion] | None = None,
) -> dict[DerivativeKey, Polynomial]:
    polynomials: dict[DerivativeKey, Polynomial] = {
        key: {} for key in ALL_KEYS
    }
    for output, by_degree in by_frequency.items():
        if supports is not None and output not in supports:
            continue
        leading = output[0]
        if tree.is_zero_vector(leading):
            continue
        if not (leading[0] == leading[1] == leading[2]):
            raise AssertionError("Every limiting output must be diagonal.")
        weight = abs(leading[0])
        for left_degree, left in by_degree.items():
            for right_degree, right in by_degree.items():
                power = sum(left_degree) + sum(right_degree)
                for left_key, left_value in left.items():
                    for right_key, right_value in right.items():
                        combination = combine_keys(left_key, right_key)
                        if combination is None:
                            continue
                        output_key, factor = combination
                        add_polynomial(
                            polynomials[output_key],
                            power,
                            weight
                            * factor
                            * tree.dot(left_value, right_value)
                            / tree.NORMALIZATION_SQUARED,
                        )
    return {
        key: {
            power: coefficient
            for power, coefficient in polynomial.items()
            if coefficient != 0
        }
        for key, polynomial in polynomials.items()
    }


def equal_amplitude_expression(polynomial: Polynomial) -> sp.Expr:
    expression = sp.Integer(0)
    for epsilon_power, coefficient in polynomial.items():
        if epsilon_power % 2 != 0:
            raise AssertionError("An odd equal-catalyst amplitude power survived.")
        expression += (
            sp.Rational(coefficient.numerator, coefficient.denominator)
            * X_VAR ** (epsilon_power // 2)
            / 2**epsilon_power
        )
    return sp.expand(expression)


def expression_digest(expression: sp.Expr) -> str:
    polynomial = sp.Poly(expression, X_VAR, domain=sp.QQ)
    payload = "\n".join(
        f"{monomial}:{coefficient}"
        for monomial, coefficient in polynomial.terms()
    )
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def rational_interval(
    expression: sp.Expr,
    alpha_interval: amplitude.Interval,
) -> amplitude.Interval:
    numerator, denominator = sp.fraction(sp.cancel(expression))
    numerator_interval = amplitude.polynomial_interval(
        sp.Poly(numerator, X_VAR, domain=sp.QQ),
        {X_VAR: alpha_interval},
    )
    denominator_interval = amplitude.polynomial_interval(
        sp.Poly(denominator, X_VAR, domain=sp.QQ),
        {X_VAR: alpha_interval},
    )
    return amplitude.interval_divide(
        numerator_interval,
        denominator_interval,
    )


def midpoint(interval: amplitude.Interval) -> float:
    return float((interval[0] + interval[1]) / 2)


def quotient_record(
    external: dict[DerivativeKey, sp.Expr],
    target: dict[DerivativeKey, sp.Expr],
) -> dict[str, object]:
    base_external = external[BASE_KEY]
    base_target = target[BASE_KEY]
    table_external, table_target = amplitude.real_amplitude_polynomials()
    if sp.expand(base_external - table_external.subs(amplitude.Y_VAR, 0)) != 0:
        raise AssertionError("The second-variation external baseline changed.")
    if sp.expand(base_target - table_target.subs(amplitude.Y_VAR, 0)) != 0:
        raise AssertionError("The second-variation target baseline changed.")

    stationary = amplitude.primitive_integer_polynomial(
        X_VAR * sp.diff(base_external, X_VAR) - 2 * base_external,
        X_VAR,
    )
    roots = amplitude.positive_root_intervals(stationary, 80)
    if len(roots) != 1:
        raise AssertionError("The algebraic amplitude root is not unique.")
    alpha_interval = roots[0]

    quotient = sp.cancel(base_external / base_target)
    gradient_expressions: list[sp.Expr] = []
    for index in range(4):
        key = (index,)
        gradient_expressions.append(sp.cancel(
            (
                external[key] * base_target
                - base_external * target[key]
            )
            / base_target**2
        ))

    hessian_expressions: list[list[sp.Expr]] = []
    for left in range(4):
        row = []
        for right in range(4):
            key = tuple(sorted((left, right)))
            value = sp.cancel(
                external[key] / base_target
                - external[(left,)] * target[(right,)] / base_target**2
                - external[(right,)] * target[(left,)] / base_target**2
                - base_external * target[key] / base_target**2
                + 2
                * base_external
                * target[(left,)]
                * target[(right,)]
                / base_target**3
            )
            row.append(value)
        hessian_expressions.append(row)

    amplitude_second_expression = sp.diff(quotient, X_VAR, 2)
    mixed_expressions = [
        sp.diff(value, X_VAR) for value in gradient_expressions
    ]
    exact_symmetry_checks = {
        "pumpGradientSumZero": sp.cancel(
            gradient_expressions[0] + gradient_expressions[1]
        ) == 0,
        "catalystGradientSumZero": sp.cancel(
            gradient_expressions[2] + gradient_expressions[3]
        ) == 0,
        "pumpMixedSumZero": sp.cancel(
            mixed_expressions[0] + mixed_expressions[1]
        ) == 0,
        "catalystMixedSumZero": sp.cancel(
            mixed_expressions[2] + mixed_expressions[3]
        ) == 0,
        "pumpDiagonalEqual": sp.cancel(
            hessian_expressions[0][0] - hessian_expressions[1][1]
        ) == 0,
        "catalystDiagonalEqual": sp.cancel(
            hessian_expressions[2][2] - hessian_expressions[3][3]
        ) == 0,
        "crossParallelEqual": sp.cancel(
            hessian_expressions[0][2] - hessian_expressions[1][3]
        ) == 0,
        "crossOppositeEqual": sp.cancel(
            hessian_expressions[0][3] - hessian_expressions[1][2]
        ) == 0,
    }
    if not all(exact_symmetry_checks.values()):
        raise AssertionError("The expected pair-exchange symmetry failed.")

    common_pump_curvature_expression = sp.cancel(
        hessian_expressions[0][0]
        + 2 * hessian_expressions[0][1]
        + hessian_expressions[1][1]
    )
    common_catalyst_curvature_expression = sp.cancel(
        hessian_expressions[2][2]
        + 2 * hessian_expressions[2][3]
        + hessian_expressions[3][3]
    )
    amplitude_second_interval = rational_interval(
        amplitude_second_expression,
        alpha_interval,
    )
    mixed_intervals = [
        rational_interval(value, alpha_interval)
        for value in mixed_expressions
    ]
    chart_hessian_intervals = [
        [rational_interval(value, alpha_interval) for value in row]
        for row in hessian_expressions
    ]
    common_pump_curvature_interval = rational_interval(
        common_pump_curvature_expression,
        alpha_interval,
    )
    common_catalyst_curvature_interval = rational_interval(
        common_catalyst_curvature_expression,
        alpha_interval,
    )

    chart_hessian = np.asarray([
        [midpoint(value) for value in row]
        for row in chart_hessian_intervals
    ])
    speed = np.sqrt(np.asarray([float(value) for value in CHART_SPEEDS_SQUARED]))
    angular_hessian = chart_hessian / np.outer(speed, speed)
    mixed_chart = np.asarray([midpoint(value) for value in mixed_intervals])
    mixed_angular = mixed_chart / speed
    amplitude_second = midpoint(amplitude_second_interval)
    reduced_angular = angular_hessian - np.outer(
        mixed_angular,
        mixed_angular,
    ) / amplitude_second

    return {
        "alpha": amplitude.compact_interval_record(alpha_interval),
        "amplitudeSecondDerivative": amplitude.compact_interval_record(
            amplitude_second_interval
        ),
        "amplitudePolarizationMixedChart": [
            amplitude.compact_interval_record(value)
            for value in mixed_intervals
        ],
        "polarizationHessianChart": [
            [amplitude.compact_interval_record(value) for value in row]
            for row in chart_hessian_intervals
        ],
        "polarizationHessianAngularDecimal": angular_hessian.tolist(),
        "polarizationHessianAngularEigenvaluesDecimal": np.linalg.eigvalsh(
            angular_hessian
        ).tolist(),
        "amplitudeOptimizedAngularHessianDecimal": reduced_angular.tolist(),
        "amplitudeOptimizedAngularEigenvaluesDecimal": np.linalg.eigvalsh(
            reduced_angular
        ).tolist(),
        "gradientAngularDecimal": [
            midpoint(rational_interval(value, alpha_interval)) / speed[index]
            for index, value in enumerate(gradient_expressions)
        ],
        "exactPairSymmetryChecks": exact_symmetry_checks,
        "commonPumpChartCurvature": amplitude.compact_interval_record(
            common_pump_curvature_interval
        ),
        "commonCatalystChartCurvature": amplitude.compact_interval_record(
            common_catalyst_curvature_interval
        ),
        "expressionDigests": {
            "amplitudeSecond": expression_digest(
                sp.fraction(sp.cancel(amplitude_second_expression))[0]
            ),
            "polarizationSecondNumerators": [
                [
                    expression_digest(sp.fraction(sp.cancel(value))[0])
                    for value in row
                ]
                for row in hessian_expressions
            ],
        },
    }


def key_label(key: DerivativeKey) -> str:
    if not key:
        return "base"
    return ".".join(PARAMETER_LABELS[index] for index in key)


def audit() -> dict[str, object]:
    by_frequency, pole_counts = aggregate_limit()
    total_polynomials = energy_jets(by_frequency)
    target_polynomials = energy_jets(
        by_frequency,
        {tree.NEXT_A_POSITIVE, tree.NEXT_A_NEGATIVE},
    )
    total = {
        key: equal_amplitude_expression(value)
        for key, value in total_polynomials.items()
    }
    target = {
        key: equal_amplitude_expression(value)
        for key, value in target_polynomials.items()
    }
    external = {
        key: sp.expand(total[key] - target[key]) for key in ALL_KEYS
    }
    quotient = quotient_record(external, target)
    return {
        "scope": "four real polarization second variations at the R0.15 minimizer",
        "derivativeKeyCount": len(ALL_KEYS),
        "aggregatedFrequencyCount": len(by_frequency),
        "uncancelledLaurentPoleCounts": {
            key_label(key): count for key, count in pole_counts.items()
        },
        "quotient": quotient,
    }


def validate(result: dict[str, object]) -> None:
    assert result["derivativeKeyCount"] == 15
    assert result["aggregatedFrequencyCount"] == 326
    assert all(
        count == 0
        for count in result["uncancelledLaurentPoleCounts"].values()
    )
    quotient = result["quotient"]
    assert quotient["amplitudeSecondDerivative"]["lowerDecimal"] > 0
    assert all(quotient["exactPairSymmetryChecks"].values())
    assert quotient["commonPumpChartCurvature"]["lowerDecimal"] > 0
    assert quotient["commonCatalystChartCurvature"]["upperDecimal"] < 0
    assert len(quotient["polarizationHessianAngularEigenvaluesDecimal"]) == 4


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
