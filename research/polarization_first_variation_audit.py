#!/usr/bin/env python3
"""Exact first-variation audit for the four input polarizations.

The fifth-order cone calculation in R0.13--R0.15 fixes four real input
polarizations: two old-shell pumps and two current-shell catalysts.  Every
limiting wavevector is parallel to (1,1,1), so each real divergence-free
polarization has one angular tangent direction.

For a positive input frequency K(delta), write

    Kbar(delta) = delta K(delta),
    N(delta)    = the R0.11 polarization numerator,
    M(delta)    = Kbar(delta) cross N(delta).

Then N and M are exactly orthogonal and divergence-free.  The normalized
curve (N+tM)/(|N| sqrt(1+t^2 |Kbar|^2)) has first derivative M/|N| at t=0.
This script propagates the four first derivatives through the complete signed
order-five tree with exact Fraction arithmetic.  It differentiates target and
external H^(1/2) energies, then evaluates the quotient derivatives at the
algebraic amplitude minimizer isolated in R0.15.

The output is a local calculation for the fixed finite-order model.  A
nonzero derivative gives a certified polarization descent direction, but it
does not optimize the full polarization torus or estimate a PDE remainder.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
import hashlib
import json
import math

import sympy as sp

import fifth_order_tree_audit as tree
import two_amplitude_global_audit as amplitude


Rational = Fraction
Vector = tree.Vector
VectorSeries = tree.VectorSeries
Degree = tree.Degree
FrequencyExpansion = tree.FrequencyExpansion
Polynomial = dict[int, Rational]
JetSeries = tuple[VectorSeries, VectorSeries, VectorSeries, VectorSeries, VectorSeries]

PARAMETER_LABELS = ("pumpP", "pumpQ", "catalystB", "catalystD")
ZERO_JET: JetSeries = ({}, {}, {}, {}, {})
X_VAR = amplitude.X_VAR


def vector_cross(left: Vector, right: Vector) -> Vector:
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def series_cross(left: VectorSeries, right: VectorSeries) -> VectorSeries:
    result: VectorSeries = {}
    for left_power, left_value in left.items():
        for right_power, right_value in right.items():
            power = left_power + right_power
            result[power] = tree.vector_add(
                result.get(power, tree.ZERO_VECTOR),
                vector_cross(left_value, right_value),
            )
    return {
        power: value
        for power, value in result.items()
        if not tree.is_zero_vector(value)
    }


def scalar_series_dot(
    left: VectorSeries,
    right: VectorSeries,
) -> dict[int, Rational]:
    result: dict[int, Rational] = {}
    for left_power, left_value in left.items():
        for right_power, right_value in right.items():
            power = left_power + right_power
            result[power] = result.get(power, tree.ZERO_R) + tree.dot(
                left_value,
                right_value,
            )
    return {power: value for power, value in result.items() if value != 0}


def scalar_series_multiply(
    left: dict[int, Rational],
    right: dict[int, Rational],
) -> dict[int, Rational]:
    result: dict[int, Rational] = {}
    for left_power, left_value in left.items():
        for right_power, right_value in right.items():
            power = left_power + right_power
            result[power] = result.get(power, tree.ZERO_R) + (
                left_value * right_value
            )
    return {power: value for power, value in result.items() if value != 0}


def tangent_series(
    frequency: FrequencyExpansion,
    polarization: VectorSeries,
) -> VectorSeries:
    kbar = {0: frequency[0], 1: frequency[1]}
    tangent = series_cross(kbar, polarization)
    frequency_series = {-1: frequency[0], 0: frequency[1]}
    if scalar_series_dot(frequency_series, polarization):
        raise AssertionError("The base polarization is not divergence-free.")
    if scalar_series_dot(frequency_series, tangent):
        raise AssertionError("The tangent polarization is not divergence-free.")
    if scalar_series_dot(polarization, tangent):
        raise AssertionError("The base and tangent polarizations are not orthogonal.")
    tangent_norm = scalar_series_dot(tangent, tangent)
    expected_tangent_norm = scalar_series_multiply(
        scalar_series_dot(kbar, kbar),
        scalar_series_dot(polarization, polarization),
    )
    if tangent_norm != expected_tangent_norm:
        raise AssertionError("The tangent norm identity failed.")
    return tangent


def initial_jets() -> tuple[JetSeries, ...]:
    positive: list[JetSeries] = []
    for index, (frequency, polarization) in enumerate(
        zip(
            tree.POSITIVE_FREQUENCIES,
            tree.POSITIVE_POLARIZATION_SERIES,
            strict=True,
        )
    ):
        entries: list[VectorSeries] = [dict(polarization), {}, {}, {}, {}]
        entries[index + 1] = tangent_series(frequency, polarization)
        positive.append(tuple(entries))  # type: ignore[arg-type]
    # Reality requires the negative Fourier coefficient to use the same real
    # curve as its positive partner.  Its tangent is therefore copied rather
    # than reconstructed from the negative wavevector.
    return tuple(positive + positive)


def jet_add(left: JetSeries, right: JetSeries, minimum: int, maximum: int) -> JetSeries:
    return tuple(
        tree.series_add(left[index], right[index], minimum, maximum)
        for index in range(5)
    )  # type: ignore[return-value]


def jet_scale(value: Rational, jet: JetSeries) -> JetSeries:
    return tuple(
        tree.series_scale(value, component) for component in jet
    )  # type: ignore[return-value]


def jet_bilinear(
    left_degree: Degree,
    left: JetSeries,
    right_degree: Degree,
    right: JetSeries,
    frequencies: tuple[FrequencyExpansion, ...],
    minimum: int,
    maximum: int,
) -> JetSeries:
    base = tree.bilinear_series(
        left_degree,
        left[0],
        right_degree,
        right[0],
        frequencies,
        minimum,
        maximum,
    )
    derivatives: list[VectorSeries] = [base]
    for index in range(1, 5):
        left_term = tree.bilinear_series(
            left_degree,
            left[index],
            right_degree,
            right[0],
            frequencies,
            minimum,
            maximum,
        )
        right_term = tree.bilinear_series(
            left_degree,
            left[0],
            right_degree,
            right[index],
            frequencies,
            minimum,
            maximum,
        )
        derivatives.append(
            tree.series_add(left_term, right_term, minimum, maximum)
        )
    return tuple(derivatives)  # type: ignore[return-value]


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
                        output.get(degree, ZERO_JET),
                        value,
                        minimum,
                        maximum,
                    )
        coefficients[order + 1] = output
    return coefficients


def aggregate_limit() -> tuple[
    dict[FrequencyExpansion, dict[tuple[int, int], tuple[Vector, ...]]],
    list[int],
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
            aggregated.get(key, ZERO_JET),
            jet,
            -5,
            0,
        )

    pole_counts = [0] * 5
    by_frequency: dict[
        FrequencyExpansion,
        dict[tuple[int, int], tuple[Vector, ...]],
    ] = defaultdict(dict)
    for (output, catalyst_degree), jet in aggregated.items():
        for component in range(5):
            for power in range(-5, 0):
                if not tree.is_zero_vector(
                    jet[component].get(power, tree.ZERO_VECTOR)
                ):
                    pole_counts[component] += 1
        constants = tuple(
            jet[component].get(0, tree.ZERO_VECTOR)
            for component in range(5)
        )
        if any(not tree.is_zero_vector(value) for value in constants):
            by_frequency[output][catalyst_degree] = constants
    return dict(by_frequency), pole_counts


def add_polynomial(polynomial: Polynomial, power: int, value: Rational) -> None:
    polynomial[power] = polynomial.get(power, tree.ZERO_R) + value


def energy_jets(
    by_frequency: dict[
        FrequencyExpansion,
        dict[tuple[int, int], tuple[Vector, ...]],
    ],
    supports: set[FrequencyExpansion] | None = None,
) -> tuple[Polynomial, ...]:
    polynomials: list[Polynomial] = [{} for _ in range(5)]
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
                add_polynomial(
                    polynomials[0],
                    power,
                    weight
                    * tree.dot(left[0], right[0])
                    / tree.NORMALIZATION_SQUARED,
                )
                for parameter in range(4):
                    derivative = (
                        tree.dot(left[parameter + 1], right[0])
                        + tree.dot(left[0], right[parameter + 1])
                    )
                    add_polynomial(
                        polynomials[parameter + 1],
                        power,
                        weight * derivative / tree.NORMALIZATION_SQUARED,
                    )
    return tuple(
        {
            power: coefficient
            for power, coefficient in polynomial.items()
            if coefficient != 0
        }
        for polynomial in polynomials
    )


def equal_amplitude_expression(polynomial: Polynomial) -> sp.Expr:
    expression = sp.Integer(0)
    for epsilon_power, coefficient in polynomial.items():
        if epsilon_power % 2 != 0:
            raise AssertionError("An odd equal-catalyst amplitude power survived.")
        x_power = epsilon_power // 2
        expression += (
            sp.Rational(coefficient.numerator, coefficient.denominator)
            * X_VAR**x_power
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


def quotient_gradient_record(
    external: tuple[sp.Expr, ...],
    target: tuple[sp.Expr, ...],
) -> dict[str, object]:
    base_external = external[0]
    base_target = target[0]
    table_external, table_target = amplitude.real_amplitude_polynomials()
    if sp.expand(base_external - table_external.subs(amplitude.Y_VAR, 0)) != 0:
        raise AssertionError("The differentiated external baseline changed.")
    if sp.expand(base_target - table_target.subs(amplitude.Y_VAR, 0)) != 0:
        raise AssertionError("The differentiated target baseline changed.")

    stationary = amplitude.primitive_integer_polynomial(
        X_VAR * sp.diff(base_external, X_VAR) - 2 * base_external,
        X_VAR,
    )
    roots = amplitude.positive_root_intervals(stationary, 80)
    if len(roots) != 1:
        raise AssertionError("The algebraic amplitude root is not unique.")
    alpha_interval = roots[0]
    target_interval = amplitude.polynomial_interval(
        sp.Poly(base_target, X_VAR, domain=sp.QQ),
        {X_VAR: alpha_interval},
    )
    denominator = amplitude.interval_multiply(target_interval, target_interval)

    records = []
    numerators: list[sp.Expr] = []
    chart_speeds_squared = (
        sp.Rational(1, 12),
        sp.Rational(1, 12),
        sp.Rational(1, 3),
        sp.Rational(1, 3),
    )
    angular_values = []
    nonzero_count = 0
    for index, label in enumerate(PARAMETER_LABELS):
        numerator = sp.expand(
            external[index + 1] * base_target
            - base_external * target[index + 1]
        )
        numerators.append(numerator)
        if numerator == 0:
            derivative_interval = (sp.Rational(0), sp.Rational(0))
        else:
            numerator_interval = amplitude.polynomial_interval(
                sp.Poly(numerator, X_VAR, domain=sp.QQ),
                {X_VAR: alpha_interval},
            )
            derivative_interval = amplitude.interval_divide(
                numerator_interval,
                denominator,
            )
        if derivative_interval[0] > 0 or derivative_interval[1] < 0:
            nonzero_count += 1
        midpoint = float((derivative_interval[0] + derivative_interval[1]) / 2)
        angular_value = midpoint / math.sqrt(float(chart_speeds_squared[index]))
        angular_values.append(angular_value)
        records.append(
            {
                "parameter": label,
                "chartSpeedSquared": str(chart_speeds_squared[index]),
                "quotientDerivative": amplitude.compact_interval_record(
                    derivative_interval
                ),
                "angularDerivativeDecimal": angular_value,
                "numeratorDegree": int(sp.degree(numerator, X_VAR)),
                "numeratorDigest": expression_digest(numerator),
            }
        )
    if sp.expand(numerators[0] + numerators[1]) != 0:
        raise AssertionError("The pump first variations lost antisymmetry.")
    if sp.expand(numerators[2] + numerators[3]) != 0:
        raise AssertionError("The catalyst first variations lost antisymmetry.")
    norm = math.sqrt(sum(value * value for value in angular_values))
    descent = [-value / norm for value in angular_values]
    return {
        "alpha": amplitude.compact_interval_record(alpha_interval),
        "parameterization": (
            "(N+t*(delta*K cross N))/(|N|*sqrt(1+t^2*|delta*K|^2))"
        ),
        "derivatives": records,
        "certifiedNonzeroDerivativeCount": nonzero_count,
        "fixedPolarizationIsStationary": nonzero_count == 0,
        "antisymmetricPairStructure": True,
        "unitAngularSteepestDescentDecimal": {
            label: value for label, value in zip(PARAMETER_LABELS, descent, strict=True)
        },
        "angularGradientNormDecimal": norm,
    }


def audit() -> dict[str, object]:
    by_frequency, pole_counts = aggregate_limit()
    total_polynomials = energy_jets(by_frequency)
    target_polynomials = energy_jets(
        by_frequency,
        {tree.NEXT_A_POSITIVE, tree.NEXT_A_NEGATIVE},
    )
    total = tuple(equal_amplitude_expression(value) for value in total_polynomials)
    target = tuple(equal_amplitude_expression(value) for value in target_polynomials)
    external = tuple(
        sp.expand(total[index] - target[index]) for index in range(5)
    )
    gradient = quotient_gradient_record(external, target)
    return {
        "scope": "four real input-polarization tangents at the R0.15 minimizer",
        "aggregatedFrequencyCount": len(by_frequency),
        "uncancelledLaurentPoleCounts": {
            label: count
            for label, count in zip(
                ("base", *PARAMETER_LABELS),
                pole_counts,
                strict=True,
            )
        },
        "gradient": gradient,
        "conclusion": (
            "the fixed R0.11 polarization is not stationary for the "
            "fifth-order external/target quotient"
        ),
    }


def validate(result: dict[str, object]) -> None:
    assert result["aggregatedFrequencyCount"] == 322
    assert all(
        count == 0
        for count in result["uncancelledLaurentPoleCounts"].values()
    )
    gradient = result["gradient"]
    assert gradient["certifiedNonzeroDerivativeCount"] == 4
    assert not gradient["fixedPolarizationIsStationary"]
    assert gradient["antisymmetricPairStructure"]
    derivatives = gradient["derivatives"]
    assert derivatives[0]["quotientDerivative"]["upperDecimal"] < 0
    assert derivatives[1]["quotientDerivative"]["lowerDecimal"] > 0
    assert derivatives[2]["quotientDerivative"]["upperDecimal"] < 0
    assert derivatives[3]["quotientDerivative"]["lowerDecimal"] > 0
    assert gradient["angularGradientNormDecimal"] > 0


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
