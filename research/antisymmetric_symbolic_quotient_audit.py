#!/usr/bin/env python3
"""Exact three-variable quotient on the antisymmetric polarization chart.

Write the four positive input polarizations as

    N_P + p M_P,  N_Q - p M_Q,  N_B + q M_B,  N_D - q M_D,

where M is the divergence-free tangent used in R0.14--R0.17.  This script
propagates the two polynomial variables p and q through the complete signed
fifth-order Laurent tree.  Equal-frequency terms are aggregated before the
delta -> 0 limit, and every negative Laurent coefficient is checked exactly.

Let x be the squared catalyst amplitude.  If

    U = 1 + p^2/12,  V = 1 + q^2/3,

then normalization of the twelve leaves in an energy pairing gives

    Energy = N(p,q,x) / (U^6 V^6).

The common denominator cancels from the external/target quotient.  Hence its
three stationary equations are the exact polynomial equations

    E_i T - E T_i = 0,  i in {P,Q,x}.

This is a finite fifth-order calculation.  It does not control a Taylor
remainder or prove a statement about global Navier--Stokes evolution.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import json

import sympy as sp

import fifth_order_tree_audit as tree
import finite_candidate_first_variation_audit as refined
import polarization_first_variation_audit as first


Rational = Fraction
Monomial = tuple[int, int]
Poly = dict[Monomial, Rational]
PolyVector = tuple[Poly, Poly, Poly]
PolyVectorSeries = dict[int, PolyVector]
ScalarPolySeries = dict[int, Poly]
Degree = tree.Degree
FrequencyExpansion = tree.FrequencyExpansion

ZERO_POLY_VECTOR: PolyVector = ({}, {}, {})
P_VAR, Q_VAR, X_VAR = sp.symbols("p q x", positive=True)
VARIABLES = (P_VAR, Q_VAR, X_VAR)
ROOT_CENTER = (
    Rational("6.36987869502312325961530538630896448"),
    Rational("5.65898700923140673205730404156565913"),
    Rational("2.62090432267919812131281111489559215"),
)
ROOT_RADIUS = Rational(1, 10**30)


def poly_add(left: Poly, right: Poly) -> Poly:
    result = dict(left)
    for monomial, value in right.items():
        result[monomial] = result.get(monomial, tree.ZERO_R) + value
        if result[monomial] == 0:
            del result[monomial]
    return result


def poly_scale(value: Rational | int, polynomial: Poly) -> Poly:
    factor = Rational(value)
    if factor == 0:
        return {}
    return {
        monomial: factor * coefficient
        for monomial, coefficient in polynomial.items()
        if factor * coefficient != 0
    }


def poly_multiply(left: Poly, right: Poly) -> Poly:
    result: Poly = {}
    for (left_p, left_q), left_value in left.items():
        for (right_p, right_q), right_value in right.items():
            monomial = left_p + right_p, left_q + right_q
            result[monomial] = result.get(monomial, tree.ZERO_R) + (
                left_value * right_value
            )
    return {
        monomial: value for monomial, value in result.items() if value != 0
    }


def constant_poly(value: Rational | int) -> Poly:
    coefficient = Rational(value)
    return {} if coefficient == 0 else {(0, 0): coefficient}


def variable_poly(axis: int, sign: int) -> Poly:
    if axis not in (0, 1):
        raise ValueError("A polynomial variable axis must be zero or one.")
    monomial = (1, 0) if axis == 0 else (0, 1)
    return {monomial: Rational(sign)}


def poly_vector_add(left: PolyVector, right: PolyVector) -> PolyVector:
    return tuple(
        poly_add(left[index], right[index]) for index in range(3)
    )  # type: ignore[return-value]


def poly_vector_scale(
    value: Rational | int,
    vector: PolyVector,
) -> PolyVector:
    return tuple(
        poly_scale(value, vector[index]) for index in range(3)
    )  # type: ignore[return-value]


def rational_vector_times_poly(
    vector: tree.Vector,
    polynomial: Poly,
) -> PolyVector:
    return tuple(
        poly_scale(vector[index], polynomial) for index in range(3)
    )  # type: ignore[return-value]


def rational_dot_poly_vector(
    vector: tree.Vector,
    poly_vector: PolyVector,
) -> Poly:
    result: Poly = {}
    for index in range(3):
        result = poly_add(
            result,
            poly_scale(vector[index], poly_vector[index]),
        )
    return result


def poly_vector_dot(left: PolyVector, right: PolyVector) -> Poly:
    result: Poly = {}
    for index in range(3):
        result = poly_add(
            result,
            poly_multiply(left[index], right[index]),
        )
    return result


def rational_series_to_poly(series: tree.VectorSeries) -> PolyVectorSeries:
    result: PolyVectorSeries = {}
    for power, vector in series.items():
        converted = tuple(
            constant_poly(vector[index]) for index in range(3)
        )
        if converted != ZERO_POLY_VECTOR:
            result[power] = converted  # type: ignore[assignment]
    return result


def charted_input_series(
    frequency: FrequencyExpansion,
    numerator: tree.VectorSeries,
    axis: int,
    sign: int,
) -> PolyVectorSeries:
    base = rational_series_to_poly(numerator)
    tangent = first.tangent_series(frequency, numerator)
    chart = variable_poly(axis, sign)
    result = dict(base)
    for power, vector in tangent.items():
        term = rational_vector_times_poly(vector, chart)
        result[power] = poly_vector_add(
            result.get(power, ZERO_POLY_VECTOR),
            term,
        )
        if result[power] == ZERO_POLY_VECTOR:
            del result[power]
    return result


def signed_polynomial_inputs() -> tuple[PolyVectorSeries, ...]:
    specifications = ((0, 1), (0, -1), (1, 1), (1, -1))
    positive = tuple(
        charted_input_series(frequency, numerator, axis, sign)
        for (frequency, numerator), (axis, sign) in zip(
            zip(
                tree.POSITIVE_FREQUENCIES,
                tree.POSITIVE_POLARIZATION_SERIES,
                strict=True,
            ),
            specifications,
            strict=True,
        )
    )
    return positive + positive


def poly_series_add(
    left: PolyVectorSeries,
    right: PolyVectorSeries,
    minimum: int,
    maximum: int,
) -> PolyVectorSeries:
    result: PolyVectorSeries = {}
    for power in range(minimum, maximum + 1):
        value = poly_vector_add(
            left.get(power, ZERO_POLY_VECTOR),
            right.get(power, ZERO_POLY_VECTOR),
        )
        if value != ZERO_POLY_VECTOR:
            result[power] = value
    return result


def poly_series_scale(
    value: Rational | int,
    series: PolyVectorSeries,
) -> PolyVectorSeries:
    return {
        power: poly_vector_scale(value, coefficient)
        for power, coefficient in series.items()
        if poly_vector_scale(value, coefficient) != ZERO_POLY_VECTOR
    }


def add_scalar_poly_coefficient(
    series: ScalarPolySeries,
    power: int,
    value: Poly,
) -> None:
    updated = poly_add(series.get(power, {}), value)
    if updated:
        series[power] = updated
    elif power in series:
        del series[power]


def polynomial_bilinear_series(
    left_degree: Degree,
    left: PolyVectorSeries,
    right_degree: Degree,
    right: PolyVectorSeries,
    frequencies: tuple[FrequencyExpansion, ...],
    minimum_power: int,
    maximum_power: int,
) -> PolyVectorSeries:
    """Return one ordered Leray interaction with polynomial coefficients."""

    right_frequency = tree.degree_frequency(right_degree, frequencies)
    output_frequency = tree.frequency_add(
        tree.degree_frequency(left_degree, frequencies),
        right_frequency,
    )
    if tree.is_zero_frequency(output_frequency):
        return {}

    scalar: ScalarPolySeries = {}
    for power, coefficient in left.items():
        if not tree.is_zero_vector(right_frequency[0]):
            add_scalar_poly_coefficient(
                scalar,
                power - 1,
                rational_dot_poly_vector(right_frequency[0], coefficient),
            )
        add_scalar_poly_coefficient(
            scalar,
            power,
            rational_dot_poly_vector(right_frequency[1], coefficient),
        )

    raw: PolyVectorSeries = {}
    for left_power, scalar_value in scalar.items():
        for right_power, coefficient in right.items():
            output_power = left_power + right_power
            if not minimum_power <= output_power <= maximum_power:
                continue
            product = tuple(
                poly_multiply(scalar_value, component)
                for component in coefficient
            )
            raw[output_power] = poly_vector_add(
                raw.get(output_power, ZERO_POLY_VECTOR),
                product,  # type: ignore[arg-type]
            )
            if raw[output_power] == ZERO_POLY_VECTOR:
                del raw[output_power]

    leading, offset = output_frequency
    if tree.is_zero_vector(leading):
        denominator = tree.dot(offset, offset)
        projected: PolyVectorSeries = {}
        for power, coefficient in raw.items():
            scalar_projection = poly_scale(
                -Rational(1, 1) / denominator,
                rational_dot_poly_vector(offset, coefficient),
            )
            value = poly_vector_add(
                coefficient,
                rational_vector_times_poly(offset, scalar_projection),
            )
            if value != ZERO_POLY_VECTOR:
                projected[power] = value
        return projected

    numerator: ScalarPolySeries = {}
    for power, coefficient in raw.items():
        add_scalar_poly_coefficient(
            numerator,
            power - 1,
            rational_dot_poly_vector(leading, coefficient),
        )
        add_scalar_poly_coefficient(
            numerator,
            power,
            rational_dot_poly_vector(offset, coefficient),
        )
    if numerator:
        first_shifted_power = min(numerator) + 2
        inverse_order = max(0, maximum_power + 1 - first_shifted_power)
    else:
        inverse_order = 0
    inverse = tree.inverse_quadratic_series(
        tree.dot(leading, leading),
        2 * tree.dot(leading, offset),
        tree.dot(offset, offset),
        inverse_order,
    )
    quotient: ScalarPolySeries = {}
    for numerator_power, numerator_value in numerator.items():
        for inverse_power, inverse_value in enumerate(inverse):
            output_power = numerator_power + 2 + inverse_power
            if minimum_power <= output_power <= maximum_power + 1:
                add_scalar_poly_coefficient(
                    quotient,
                    output_power,
                    poly_scale(inverse_value, numerator_value),
                )

    projected: PolyVectorSeries = {}
    for power in range(minimum_power, maximum_power + 1):
        correction = poly_vector_add(
            rational_vector_times_poly(
                leading,
                quotient.get(power + 1, {}),
            ),
            rational_vector_times_poly(
                offset,
                quotient.get(power, {}),
            ),
        )
        value = poly_vector_add(
            raw.get(power, ZERO_POLY_VECTOR),
            poly_vector_scale(-1, correction),
        )
        if value != ZERO_POLY_VECTOR:
            projected[power] = value
    return projected


def polynomial_tree() -> list[dict[Degree, PolyVectorSeries]]:
    frequencies = tree.signed_frequencies()
    initial = signed_polynomial_inputs()
    coefficients: list[dict[Degree, PolyVectorSeries]] = [
        {} for _ in range(tree.MAXIMUM_ORDER + 1)
    ]
    for index, polarization in enumerate(initial):
        degree = tuple(
            int(index == coordinate) for coordinate in range(len(frequencies))
        )
        coefficients[0][degree] = polarization

    for order in range(tree.MAXIMUM_ORDER):
        minimum = -(order + 1)
        maximum = tree.MAXIMUM_ORDER - (order + 1)
        output: dict[Degree, PolyVectorSeries] = {}
        for left_order in range(order + 1):
            right_order = order - left_order
            for left_degree, left in coefficients[left_order].items():
                for right_degree, right in coefficients[right_order].items():
                    degree = tree.degree_add(left_degree, right_degree)
                    value = poly_series_scale(
                        Rational(1, order + 1),
                        polynomial_bilinear_series(
                            left_degree,
                            left,
                            right_degree,
                            right,
                            frequencies,
                            minimum,
                            maximum,
                        ),
                    )
                    output[degree] = poly_series_add(
                        output.get(degree, {}),
                        value,
                        minimum,
                        maximum,
                    )
        coefficients[order + 1] = output
    return coefficients


def aggregate_limit() -> tuple[
    dict[FrequencyExpansion, dict[tuple[int, int], PolyVector]],
    int,
]:
    frequencies = tree.signed_frequencies()
    coefficients = polynomial_tree()
    aggregated: dict[
        tuple[FrequencyExpansion, tuple[int, int]],
        PolyVectorSeries,
    ] = {}
    for degree, value in coefficients[5].items():
        output = tree.degree_frequency(degree, frequencies)
        catalyst_degree = tree.catalyst_degrees(degree)
        key = output, catalyst_degree
        aggregated[key] = poly_series_add(
            aggregated.get(key, {}),
            value,
            -5,
            0,
        )

    pole_count = 0
    by_frequency: dict[
        FrequencyExpansion,
        dict[tuple[int, int], PolyVector],
    ] = defaultdict(dict)
    for (output, catalyst_degree), value in aggregated.items():
        for power in range(-5, 0):
            coefficient = value.get(power, ZERO_POLY_VECTOR)
            pole_count += sum(len(component) for component in coefficient)
        constant = value.get(0, ZERO_POLY_VECTOR)
        if constant != ZERO_POLY_VECTOR:
            by_frequency[output][catalyst_degree] = constant
    return dict(by_frequency), pole_count


def energy_polynomials(
    by_frequency: dict[
        FrequencyExpansion,
        dict[tuple[int, int], PolyVector],
    ],
    supports: set[FrequencyExpansion] | None = None,
) -> dict[tuple[int, int], Poly]:
    """Return E/sqrt(3), indexed by the two catalyst leaf counts."""

    result: dict[tuple[int, int], Poly] = {}
    for output, coefficient_by_degree in by_frequency.items():
        if supports is not None and output not in supports:
            continue
        leading = output[0]
        if tree.is_zero_vector(leading):
            continue
        if not leading[0] == leading[1] == leading[2]:
            raise AssertionError("A nonzero cone limit is not diagonal.")
        weight = abs(leading[0]) / tree.NORMALIZATION_SQUARED
        for (left_b, left_d), left in coefficient_by_degree.items():
            for (right_b, right_d), right in coefficient_by_degree.items():
                powers = left_b + right_b, left_d + right_d
                contribution = poly_scale(
                    weight,
                    poly_vector_dot(left, right),
                )
                result[powers] = poly_add(
                    result.get(powers, {}),
                    contribution,
                )
    return {powers: value for powers, value in result.items() if value}


def equal_amplitude_polynomials(
    energy: dict[tuple[int, int], Poly],
) -> dict[int, Poly]:
    """Collapse b=d=sqrt(x)/2 while retaining the chart variables."""

    by_x_power: dict[int, Poly] = {}
    for (b_power, d_power), polynomial in energy.items():
        epsilon_power = b_power + d_power
        if epsilon_power % 2:
            raise AssertionError("An odd equal-amplitude power survived.")
        x_power = epsilon_power // 2
        by_x_power[x_power] = poly_add(
            by_x_power.get(x_power, {}),
            poly_scale(Rational(1, 2**epsilon_power), polynomial),
        )

    return {
        x_power: polynomial
        for x_power, polynomial in by_x_power.items()
        if polynomial
    }


def sympy_rational(value: Rational) -> sp.Rational:
    return sp.Rational(value.numerator, value.denominator)


def sympy_poly(polynomial: Poly) -> sp.Expr:
    return sp.Add(*(
        sympy_rational(coefficient) * P_VAR**p_power * Q_VAR**q_power
        for (p_power, q_power), coefficient in polynomial.items()
    ))


def common_denominator_numerator(energy: dict[int, Poly]) -> sp.Poly:
    u_value = 1 + P_VAR**2 / 12
    v_value = 1 + Q_VAR**2 / 3
    expression = sum(
        (
            sympy_poly(polynomial)
            * X_VAR**x_power
            * u_value**x_power
            * v_value ** (6 - x_power)
        )
        for x_power, polynomial in energy.items()
    )
    return sp.Poly(sp.expand(expression), P_VAR, Q_VAR, X_VAR, domain=sp.QQ)


def rational_digest(value: Rational | sp.Rational) -> str:
    numerator = int(value.numerator if isinstance(value, Fraction) else value.p)
    denominator = int(
        value.denominator if isinstance(value, Fraction) else value.q
    )
    return hashlib.sha256(
        f"{numerator}/{denominator}".encode("ascii")
    ).hexdigest()


def polynomial_digest(polynomial: sp.Poly) -> str:
    payload = "\n".join(
        f"{powers[0]},{powers[1]},{powers[2]}:{coefficient}"
        for powers, coefficient in polynomial.terms()
    )
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def evaluate_rational(expression: sp.Expr, values: dict[sp.Symbol, Rational]) -> sp.Rational:
    substitutions = {
        variable: sympy_rational(value) for variable, value in values.items()
    }
    result = sp.cancel(expression.subs(substitutions))
    if not result.is_Rational:
        raise AssertionError("An exact evaluation was not rational.")
    return result  # type: ignore[return-value]


def candidate_values() -> dict[sp.Symbol, Rational]:
    parameters = refined.candidate_parameters()
    return {
        P_VAR: parameters["pumpChart"],
        Q_VAR: parameters["catalystChart"],
        X_VAR: refined.X_CANDIDATE,
    }


def polynomial_record(polynomial: sp.Poly) -> dict[str, object]:
    return {
        "termCount": len(polynomial.terms()),
        "degreeP": polynomial.degree(P_VAR),
        "degreeQ": polynomial.degree(Q_VAR),
        "degreeX": polynomial.degree(X_VAR),
        "totalDegree": polynomial.total_degree(),
        "exactDigest": polynomial_digest(polynomial),
    }


def exact_system() -> tuple[
    int,
    int,
    sp.Poly,
    sp.Poly,
    dict[str, sp.Poly],
]:
    by_frequency, pole_count = aggregate_limit()
    total_raw = energy_polynomials(by_frequency)
    target_raw = energy_polynomials(
        by_frequency,
        {tree.NEXT_A_POSITIVE, tree.NEXT_A_NEGATIVE},
    )
    total = common_denominator_numerator(
        equal_amplitude_polynomials(total_raw)
    )
    target = common_denominator_numerator(
        equal_amplitude_polynomials(target_raw)
    )
    external = total - target

    target_expression = target.as_expr()
    external_expression = external.as_expr()
    stationary = {
        str(variable): sp.Poly(
            sp.expand(
                sp.diff(external_expression, variable) * target_expression
                - external_expression * sp.diff(target_expression, variable)
            ),
            P_VAR,
            Q_VAR,
            X_VAR,
            domain=sp.QQ,
        )
        for variable in VARIABLES
    }
    return len(by_frequency), pole_count, target, external, stationary


def fraction_from_sympy(value: sp.Rational) -> Rational:
    return Rational(int(value.p), int(value.q))


def evaluate_poly_fraction(
    polynomial: sp.Poly,
    values: tuple[Rational, Rational, Rational],
) -> Rational:
    degrees = tuple(polynomial.degree(variable) for variable in VARIABLES)
    powers = tuple(
        [value**power for power in range(degree + 1)]
        for value, degree in zip(values, degrees, strict=True)
    )
    result = tree.ZERO_R
    for monomial, coefficient in polynomial.terms():
        result += fraction_from_sympy(coefficient) * (
            powers[0][monomial[0]]
            * powers[1][monomial[1]]
            * powers[2][monomial[2]]
        )
    return result


def absolute_poly_bound(
    polynomial: sp.Poly,
    upper_bounds: tuple[Rational, Rational, Rational],
) -> Rational:
    degrees = tuple(polynomial.degree(variable) for variable in VARIABLES)
    powers = tuple(
        [value**power for power in range(degree + 1)]
        for value, degree in zip(upper_bounds, degrees, strict=True)
    )
    result = tree.ZERO_R
    for monomial, coefficient in polynomial.terms():
        result += abs(fraction_from_sympy(coefficient)) * (
            powers[0][monomial[0]]
            * powers[1][monomial[1]]
            * powers[2][monomial[2]]
        )
    return result


def invert_matrix(matrix: list[list[Rational]]) -> list[list[Rational]]:
    size = len(matrix)
    augmented = [
        list(row) + [Rational(int(row_index == column)) for column in range(size)]
        for row_index, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if augmented[row][column] != 0),
            None,
        )
        if pivot is None:
            raise AssertionError("The center Jacobian is singular.")
        if pivot != column:
            augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        pivot_value = augmented[column][column]
        augmented[column] = [value / pivot_value for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor == 0:
                continue
            augmented[row] = [
                augmented[row][index] - factor * augmented[column][index]
                for index in range(2 * size)
            ]
    return [row[size:] for row in augmented]


def interval_string(center: Rational, radius: Rational) -> list[str]:
    return [str(center - radius), str(center + radius)]


def decimal_string(value: Rational, precision: int = 45) -> str:
    with localcontext() as context:
        context.prec = precision
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def krawczyk_certificate(
    target: sp.Poly,
    external: sp.Poly,
    stationary: dict[str, sp.Poly],
) -> dict[str, object]:
    functions = [stationary[str(variable)] for variable in VARIABLES]
    center = ROOT_CENTER
    radii = (ROOT_RADIUS,) * 3
    upper = tuple(center[index] + radii[index] for index in range(3))
    center_values = [
        evaluate_poly_fraction(polynomial, center) for polynomial in functions
    ]
    jacobian_polynomials = [
        [polynomial.diff(variable) for variable in VARIABLES]
        for polynomial in functions
    ]
    jacobian_center = [
        [
            evaluate_poly_fraction(polynomial, center)
            for polynomial in row
        ]
        for row in jacobian_polynomials
    ]
    inverse = invert_matrix(jacobian_center)

    # The mean-value theorem bounds J(X)-J(c) using exact absolute bounds
    # on the Hessians of the three stationary polynomials.
    jacobian_variation: list[list[Rational]] = []
    for function_index in range(3):
        row = []
        for derivative_index in range(3):
            variation = tree.ZERO_R
            for variable_index, variable in enumerate(VARIABLES):
                second_derivative = jacobian_polynomials[
                    function_index
                ][derivative_index].diff(variable)
                variation += (
                    absolute_poly_bound(second_derivative, upper)
                    * radii[variable_index]
                )
            row.append(variation)
        jacobian_variation.append(row)

    contraction_bounds = [
        [
            sum(
                (
                    abs(inverse[row][inner])
                    * jacobian_variation[inner][column]
                    for inner in range(3)
                ),
                start=tree.ZERO_R,
            )
            for column in range(3)
        ]
        for row in range(3)
    ]
    center_shift = [
        -sum(
            (
                inverse[row][column] * center_values[column]
                for column in range(3)
            ),
            start=tree.ZERO_R,
        )
        for row in range(3)
    ]
    image_radii = [
        sum(
            (
                contraction_bounds[row][column] * radii[column]
                for column in range(3)
            ),
            start=tree.ZERO_R,
        )
        for row in range(3)
    ]
    inclusion_ratios = [
        (abs(center_shift[index]) + image_radii[index]) / radii[index]
        for index in range(3)
    ]
    contraction_row_sums = [sum(row, start=tree.ZERO_R) for row in contraction_bounds]

    target_center = evaluate_poly_fraction(target, center)
    external_center = evaluate_poly_fraction(external, center)
    target_variation = sum(
        (
            absolute_poly_bound(target.diff(variable), upper) * radii[index]
            for index, variable in enumerate(VARIABLES)
        ),
        start=tree.ZERO_R,
    )
    external_variation = sum(
        (
            absolute_poly_bound(external.diff(variable), upper) * radii[index]
            for index, variable in enumerate(VARIABLES)
        ),
        start=tree.ZERO_R,
    )
    target_interval = target_center - target_variation, target_center + target_variation
    external_interval = (
        external_center - external_variation,
        external_center + external_variation,
    )
    if target_interval[0] <= 0 or external_interval[0] <= 0:
        raise AssertionError("The energy interval crossed zero.")
    ratio_interval = (
        external_interval[0] / target_interval[1],
        external_interval[1] / target_interval[0],
    )

    reciprocal_center = 1 / target_center**2
    reciprocal_variation = max(
        abs(1 / target_interval[0] ** 2 - reciprocal_center),
        abs(1 / target_interval[1] ** 2 - reciprocal_center),
    )
    hessian_center: list[list[Rational]] = []
    hessian_errors: list[list[Rational]] = []
    for row in range(3):
        center_row = []
        error_row = []
        for column in range(3):
            symmetric_jacobian = Rational(1, 2) * (
                jacobian_center[row][column]
                + jacobian_center[column][row]
            )
            center_row.append(symmetric_jacobian * reciprocal_center)
            error_row.append(
                Rational(1, 2)
                * (
                    jacobian_variation[row][column]
                    + jacobian_variation[column][row]
                )
                / target_interval[0] ** 2
                + Rational(1, 2)
                * (
                    abs(jacobian_center[row][column])
                    + abs(jacobian_center[column][row])
                )
                * reciprocal_variation
            )
        hessian_center.append(center_row)
        hessian_errors.append(error_row)
    diagonal_dominance_margins = []
    for row in range(3):
        diagonal_lower = hessian_center[row][row] - hessian_errors[row][row]
        off_diagonal_upper = sum(
            (
                abs(hessian_center[row][column])
                + hessian_errors[row][column]
                for column in range(3)
                if column != row
            ),
            start=tree.ZERO_R,
        )
        diagonal_dominance_margins.append(
            diagonal_lower - off_diagonal_upper
        )
    hessian_positive = all(value > 0 for value in diagonal_dominance_margins)

    inclusion = all(value < 1 for value in inclusion_ratios)
    contraction = all(value < 1 for value in contraction_row_sums)
    return {
        "method": "exact rational Krawczyk bound",
        "box": {
            str(variable): interval_string(center[index], radii[index])
            for index, variable in enumerate(VARIABLES)
        },
        "boxDecimal": {
            str(variable): [
                decimal_string(center[index] - radii[index]),
                decimal_string(center[index] + radii[index]),
            ]
            for index, variable in enumerate(VARIABLES)
        },
        "radius": str(ROOT_RADIUS),
        "strictInteriorInclusion": inclusion,
        "contractionCertified": contraction,
        "inclusionRatios": [float(value) for value in inclusion_ratios],
        "contractionRowSums": [float(value) for value in contraction_row_sums],
        "targetPositiveOnBox": target_interval[0] > 0,
        "externalOverTargetInterval": {
            "lowerDecimal": float(ratio_interval[0]),
            "upperDecimal": float(ratio_interval[1]),
            "lowerDecimalHighPrecision": decimal_string(ratio_interval[0]),
            "upperDecimalHighPrecision": decimal_string(ratio_interval[1]),
            "lowerDigest": rational_digest(ratio_interval[0]),
            "upperDigest": rational_digest(ratio_interval[1]),
        },
        "antisymmetricHessian": {
            "centerDecimal": [
                [float(value) for value in row] for row in hessian_center
            ],
            "entryErrorUpperBounds": [
                [float(value) for value in row] for row in hessian_errors
            ],
            "strictDiagonalDominanceMargins": [
                float(value) for value in diagonal_dominance_margins
            ],
            "positiveDefiniteAtUniqueRoot": hessian_positive,
        },
    }


def audit() -> dict[str, object]:
    frequency_count, pole_count, target, external, stationary = exact_system()
    target_expression = target.as_expr()
    external_expression = external.as_expr()

    values = candidate_values()
    target_value = evaluate_rational(target_expression, values)
    external_value = evaluate_rational(external_expression, values)
    ratio = sp.cancel(external_value / target_value)
    residuals = {
        label: evaluate_rational(polynomial.as_expr(), values)
        for label, polynomial in stationary.items()
    }
    quotient_derivatives = {
        label: sp.cancel(value / target_value**2)
        for label, value in residuals.items()
    }
    target_fraction = sp.cancel(target_value / (target_value + external_value))

    return {
        "scope": "exact antisymmetric fifth-order quotient",
        "variables": ["p", "q", "x"],
        "aggregatedFrequencyCount": frequency_count,
        "uncancelledLaurentMonomialCount": pole_count,
        "numerators": {
            "target": polynomial_record(target),
            "external": polynomial_record(external),
        },
        "stationaryPolynomials": {
            label: polynomial_record(polynomial)
            for label, polynomial in stationary.items()
        },
        "refinedCandidate": {
            "p": str(values[P_VAR]),
            "q": str(values[Q_VAR]),
            "x": str(values[X_VAR]),
            "externalOverTarget": {
                "decimal": float(ratio),
                "exactDigest": rational_digest(ratio),
            },
            "targetFraction": {
                "decimal": float(target_fraction),
                "percent": 100 * float(target_fraction),
                "exactDigest": rational_digest(target_fraction),
            },
            "quotientDerivatives": {
                label: {
                    "decimal": float(value),
                    "exactDigest": rational_digest(value),
                }
                for label, value in quotient_derivatives.items()
            },
        },
        "stationaryBox": krawczyk_certificate(target, external, stationary),
    }


def validate(result: dict[str, object]) -> None:
    if result["uncancelledLaurentMonomialCount"] != 0:
        raise AssertionError("A Laurent pole survived aggregation.")
    if result["aggregatedFrequencyCount"] != 332:
        raise AssertionError("The signed output support changed.")
    candidate = result["refinedCandidate"]
    expected_ratio_digest = (
        "b03c07a99a7b19d3f3198e6099a19fa6a1335b0b8ad1db6f6f3a72f0884d7cd2"
    )
    expected_fraction_digest = (
        "d88148c260ebf6b434ca8081d77110f1580097cebc7bf64c6c6b1ea111644199"
    )
    if candidate["externalOverTarget"]["exactDigest"] != expected_ratio_digest:
        raise AssertionError("The symbolic quotient did not reproduce R0.17.")
    if candidate["targetFraction"]["exactDigest"] != expected_fraction_digest:
        raise AssertionError("The symbolic target fraction did not reproduce R0.17.")
    certificate = result["stationaryBox"]
    if not certificate["strictInteriorInclusion"]:
        raise AssertionError("The Krawczyk image was not strictly interior.")
    if not certificate["contractionCertified"]:
        raise AssertionError("The Krawczyk map was not a contraction.")
    if not certificate["targetPositiveOnBox"]:
        raise AssertionError("The target numerator was not positive on the box.")
    if not certificate["antisymmetricHessian"]["positiveDefiniteAtUniqueRoot"]:
        raise AssertionError("The antisymmetric Hessian was not certified positive.")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    result = audit()
    if arguments.check:
        validate(result)
    print(json.dumps(result, indent=2 if arguments.pretty else None))


if __name__ == "__main__":
    main()
