#!/usr/bin/env python3
"""Exact common-rotation Hessian on the R0.18 stationary box.

R0.18 isolates a unique stationary point on the antisymmetric chart

    (t_P,t_Q,t_B,t_D) = (p,-p,q,-q).

The remaining local question is the two-dimensional block obtained by the
common chart shifts

    (p+a,-p+a,q+b,-q+b).

Unlike a variation tangent to the antisymmetric chart, these shifts destroy
the equal norm inside each pair.  The full delta-dependent unit
normalizations must therefore be differentiated before the fifth-order
Laurent tree is propagated.

To keep the calculation rational, use the conic parameters

    p = 24m/(1-12m^2),  q = 6n/(1-3n^2).

For a pump input, the normalized base, first and second common derivatives
have denominators (1+12m^2)^5, (1+12m^2)^7 and
(1+12m^2)^9 after expansion through delta^5.  The catalyst denominators are
the analogous powers of 1+3n^2.  Clearing these denominators before tree
propagation gives bivariate polynomial Laurent coefficients.  At every tree
node the cleared denominator depends only on the leaf counts and derivative
multi-index, so additions remain exact.

The script proves exact cancellation of every negative Laurent coefficient,
recovers the common 2x2 quotient Hessian, and bounds its two Sylvester minors
on a rational (m,n,x) box that contains the R0.18 stationary point.  Combined
with the certified antisymmetric 3x3 block from R0.18 and the exact vanishing
of the mixed block, this certifies positive definiteness of the full
five-variable Hessian at that stationary point.

This is a statement about the finite fifth-order algebraic model.  It does
not estimate a Taylor remainder or prove a Navier--Stokes regularity or
singularity result.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction as PythonFraction
import gc
import hashlib
import json
import math
import sys
import time

import sympy as sp

try:
    import gmpy2
except ImportError:  # Exact but slower fallback for a minimal Python install.
    gmpy2 = None

import antisymmetric_symbolic_quotient_audit as anti
import fifth_order_tree_audit as tree
import finite_candidate_first_variation_audit as refined
import polarization_first_variation_audit as first


if gmpy2 is None:
    Rational = PythonFraction
    RATIONAL_BACKEND = "fractions.Fraction"
else:
    Rational = gmpy2.mpq
    RATIONAL_BACKEND = "gmpy2.mpq"
    # The imported sparse-polynomial helpers construct coefficients through
    # their module-level Rational alias.  Point that constructor at mpq too;
    # Python's Fraction(mpq) conversion is not supported on this runtime.
    anti.Rational = Rational
    # Sparse-polynomial accumulation uses this imported zero as the default
    # value.  Keep it on the same backend to avoid repeated Fraction-to-mpq
    # conversions in the innermost addition loops.
    tree.ZERO_R = Rational(0)
Poly = anti.Poly
PolyVector = anti.PolyVector
PolyVectorSeries = anti.PolyVectorSeries
FrequencyExpansion = tree.FrequencyExpansion
Degree = tree.Degree
JetKey = tuple[int, int]
JetSeries = dict[JetKey, PolyVectorSeries]
SympyScalarSeries = dict[int, sp.Expr]
SympyVector = tuple[sp.Expr, sp.Expr, sp.Expr]
SympyVectorSeries = dict[int, SympyVector]

BASE_KEY: JetKey = (0, 0)
COMMON_PUMP_KEY: JetKey = (1, 0)
COMMON_CATALYST_KEY: JetKey = (0, 1)
COMMON_PUMP_SECOND_KEY: JetKey = (2, 0)
COMMON_MIXED_KEY: JetKey = (1, 1)
COMMON_CATALYST_SECOND_KEY: JetKey = (0, 2)
ALL_KEYS: tuple[JetKey, ...] = (
    BASE_KEY,
    COMMON_PUMP_KEY,
    COMMON_CATALYST_KEY,
    COMMON_PUMP_SECOND_KEY,
    COMMON_MIXED_KEY,
    COMMON_CATALYST_SECOND_KEY,
)

M_VAR, N_VAR = sp.symbols("m n", positive=True)
PUMP_FACTOR = 1 + 12 * M_VAR**2
CATALYST_FACTOR = 1 + 3 * N_VAR**2

CONIC_CENTER = (
    Rational("0.1716124717231649792322098060756778843147"),
    Rational("0.4270777907121979939963535079546579738415"),
    anti.ROOT_CENTER[2],
)
CONIC_RADII = (
    Rational(1, 10**31),
    Rational(1, 10**31),
    anti.ROOT_RADIUS,
)

PROGRESS_ENABLED = False
PROGRESS_STARTED = time.perf_counter()


def report_progress(message: str) -> None:
    if PROGRESS_ENABLED:
        elapsed = time.perf_counter() - PROGRESS_STARTED
        print(f"[{elapsed:9.1f}s] {message}", file=sys.stderr, flush=True)


def sympy_rational(value: Rational) -> sp.Rational:
    return sp.Rational(value.numerator, value.denominator)


def sympy_vector_series(value: tree.VectorSeries) -> SympyVectorSeries:
    return {
        power: tuple(sympy_rational(component) for component in vector)
        for power, vector in value.items()
    }  # type: ignore[return-value]


def scalar_series_add(
    left: SympyScalarSeries,
    right: SympyScalarSeries,
) -> SympyScalarSeries:
    result = {}
    for power in set(left).union(right):
        value = sp.cancel(left.get(power, 0) + right.get(power, 0))
        if value != 0:
            result[power] = value
    return result


def scalar_series_scale(
    value: sp.Expr,
    series: SympyScalarSeries,
) -> SympyScalarSeries:
    return {
        power: sp.cancel(value * coefficient)
        for power, coefficient in series.items()
        if value * coefficient != 0
    }


def scalar_series_multiply(
    left: SympyScalarSeries,
    right: SympyScalarSeries,
    maximum_power: int,
) -> SympyScalarSeries:
    result: SympyScalarSeries = {}
    for left_power, left_value in left.items():
        for right_power, right_value in right.items():
            power = left_power + right_power
            if power > maximum_power:
                continue
            result[power] = sp.cancel(
                result.get(power, 0) + left_value * right_value
            )
    return {
        power: value for power, value in result.items() if value != 0
    }


def vector_series_add(
    left: SympyVectorSeries,
    right: SympyVectorSeries,
) -> SympyVectorSeries:
    result: SympyVectorSeries = {}
    for power in set(left).union(right):
        left_value = left.get(power, (sp.Integer(0),) * 3)
        right_value = right.get(power, (sp.Integer(0),) * 3)
        value = tuple(
            sp.cancel(left_value[index] + right_value[index])
            for index in range(3)
        )
        if any(component != 0 for component in value):
            result[power] = value  # type: ignore[assignment]
    return result


def scalar_vector_series_multiply(
    scalar: SympyScalarSeries,
    vector: SympyVectorSeries,
    maximum_power: int,
) -> SympyVectorSeries:
    result: SympyVectorSeries = {}
    for scalar_power, scalar_value in scalar.items():
        for vector_power, vector_value in vector.items():
            power = scalar_power + vector_power
            if power > maximum_power:
                continue
            old = result.get(power, (sp.Integer(0),) * 3)
            result[power] = tuple(
                sp.cancel(old[index] + scalar_value * vector_value[index])
                for index in range(3)
            )  # type: ignore[assignment]
    return {
        power: value
        for power, value in result.items()
        if any(component != 0 for component in value)
    }


def scalar_series_dot(
    left: SympyVectorSeries,
    right: SympyVectorSeries,
) -> SympyScalarSeries:
    result: SympyScalarSeries = {}
    for left_power, left_value in left.items():
        for right_power, right_value in right.items():
            power = left_power + right_power
            product = sum(
                (
                    left_value[index] * right_value[index]
                    for index in range(3)
                ),
                start=sp.Integer(0),
            )
            result[power] = sp.cancel(result.get(power, 0) + product)
    return {
        power: value for power, value in result.items() if value != 0
    }


def inverse_square_root_series(
    value: SympyScalarSeries,
    constant_inverse_root: sp.Expr,
) -> SympyScalarSeries:
    result: SympyScalarSeries = {0: constant_inverse_root}
    for power in range(1, tree.MAXIMUM_ORDER + 1):
        square = scalar_series_multiply(result, result, power)
        product = scalar_series_multiply(value, square, power)
        known = product.get(power, 0)
        result[power] = sp.cancel(
            -known / (2 * value[0] * constant_inverse_root)
        )
        if result[power] == 0:
            del result[power]
    return result


def normalized_symbolic_input(
    index: int,
) -> dict[JetKey, SympyVectorSeries]:
    frequency = tree.POSITIVE_FREQUENCIES[index]
    numerator = tree.POSITIVE_POLARIZATION_SERIES[index]
    tangent = first.tangent_series(frequency, numerator)
    base_numerator = sympy_vector_series(numerator)
    tangent_value = sympy_vector_series(tangent)

    if index < 2:
        variable = M_VAR
        coefficient = sp.Integer(12)
        chart_scale = sp.Integer(24)
        sign = 1 if index == 0 else -1
        derivative_key = COMMON_PUMP_KEY
        second_key = COMMON_PUMP_SECOND_KEY
    else:
        variable = N_VAR
        coefficient = sp.Integer(3)
        chart_scale = sp.Integer(6)
        sign = 1 if index == 2 else -1
        derivative_key = COMMON_CATALYST_KEY
        second_key = COMMON_CATALYST_SECOND_KEY

    chart = sp.cancel(
        sign * chart_scale * variable / (1 - coefficient * variable**2)
    )
    unnormalized = vector_series_add(
        base_numerator,
        {
            power: tuple(sp.cancel(chart * component) for component in vector)
            for power, vector in tangent_value.items()
        },
    )
    norm_squared = scalar_series_scale(
        sp.Rational(1, 6),
        scalar_series_dot(unnormalized, unnormalized),
    )
    inverse_norm = inverse_square_root_series(
        norm_squared,
        sp.cancel(
            (1 - coefficient * variable**2)
            / (1 + coefficient * variable**2)
        ),
    )
    base = scalar_vector_series_multiply(
        inverse_norm,
        unnormalized,
        tree.MAXIMUM_ORDER,
    )

    tangent_norm_squared = scalar_series_scale(
        sp.Rational(1, 6),
        scalar_series_dot(tangent_value, tangent_value),
    )
    inverse_norm_squared = scalar_series_multiply(
        inverse_norm,
        inverse_norm,
        tree.MAXIMUM_ORDER,
    )
    inverse_norm_cubed = scalar_series_multiply(
        inverse_norm_squared,
        inverse_norm,
        tree.MAXIMUM_ORDER,
    )
    inverse_norm_fourth = scalar_series_multiply(
        inverse_norm_squared,
        inverse_norm_squared,
        tree.MAXIMUM_ORDER,
    )
    inverse_norm_fifth = scalar_series_multiply(
        inverse_norm_fourth,
        inverse_norm,
        tree.MAXIMUM_ORDER,
    )
    inverse_norm_derivative = scalar_series_scale(
        -chart,
        scalar_series_multiply(
            tangent_norm_squared,
            inverse_norm_cubed,
            tree.MAXIMUM_ORDER,
        ),
    )
    derivative = vector_series_add(
        scalar_vector_series_multiply(
            inverse_norm,
            tangent_value,
            tree.MAXIMUM_ORDER,
        ),
        scalar_vector_series_multiply(
            inverse_norm_derivative,
            unnormalized,
            tree.MAXIMUM_ORDER,
        ),
    )

    first_second_term = scalar_series_scale(
        -1,
        scalar_series_multiply(
            tangent_norm_squared,
            inverse_norm_cubed,
            tree.MAXIMUM_ORDER,
        ),
    )
    tangent_norm_fourth = scalar_series_multiply(
        tangent_norm_squared,
        tangent_norm_squared,
        tree.MAXIMUM_ORDER,
    )
    second_second_term = scalar_series_scale(
        3 * chart**2,
        scalar_series_multiply(
            tangent_norm_fourth,
            inverse_norm_fifth,
            tree.MAXIMUM_ORDER,
        ),
    )
    inverse_norm_second_derivative = scalar_series_add(
        first_second_term,
        second_second_term,
    )
    second_derivative = vector_series_add(
        scalar_vector_series_multiply(
            scalar_series_scale(2, inverse_norm_derivative),
            tangent_value,
            tree.MAXIMUM_ORDER,
        ),
        scalar_vector_series_multiply(
            inverse_norm_second_derivative,
            unnormalized,
            tree.MAXIMUM_ORDER,
        ),
    )
    return {
        BASE_KEY: base,
        derivative_key: derivative,
        second_key: second_derivative,
    }


def sympy_polynomial_to_poly(expression: sp.Expr) -> Poly:
    polynomial = sp.Poly(
        sp.cancel(expression),
        M_VAR,
        N_VAR,
        domain=sp.QQ,
    )
    return {
        monomial: Rational(int(coefficient.p), int(coefficient.q))
        for monomial, coefficient in polynomial.terms()
        if coefficient != 0
    }


def clear_input_denominator(
    key: JetKey,
    series: SympyVectorSeries,
    index: int,
) -> PolyVectorSeries:
    derivative_order = key[0] if index < 2 else key[1]
    variable_factor = PUMP_FACTOR if index < 2 else CATALYST_FACTOR
    denominator = variable_factor ** (5 + 2 * derivative_order)
    result: PolyVectorSeries = {}
    for power, vector in series.items():
        converted: list[Poly] = []
        for component in vector:
            cleared = sp.cancel(component * denominator)
            if sp.denom(cleared) != 1:
                raise AssertionError("An input denominator was not cleared.")
            converted.append(sympy_polynomial_to_poly(cleared))
        value = tuple(converted)
        if value != anti.ZERO_POLY_VECTOR:
            result[power] = value  # type: ignore[assignment]
    return result


def initial_jets() -> tuple[JetSeries, ...]:
    positive = []
    for index in range(4):
        symbolic = normalized_symbolic_input(index)
        positive.append({
            key: clear_input_denominator(key, series, index)
            for key, series in symbolic.items()
        })
    return tuple(positive + positive)


def jet_add(
    left: JetSeries,
    right: JetSeries,
    minimum: int,
    maximum: int,
) -> JetSeries:
    result: JetSeries = {}
    for key in set(left).union(right):
        value = anti.poly_series_add(
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
        key: anti.poly_series_scale(value, series)
        for key, series in jet.items()
        if series
    }


def derivative_factor(output: JetKey, left: JetKey) -> int:
    return math.comb(output[0], left[0]) * math.comb(output[1], left[1])


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
    for left_key, left_series in left.items():
        for right_key, right_series in right.items():
            output_key = (
                left_key[0] + right_key[0],
                left_key[1] + right_key[1],
            )
            if sum(output_key) > 2:
                continue
            value = anti.polynomial_bilinear_series(
                left_degree,
                left_series,
                right_degree,
                right_series,
                frequencies,
                minimum,
                maximum,
            )
            value = anti.poly_series_scale(
                Rational(derivative_factor(output_key, left_key)),
                value,
            )
            result[output_key] = anti.poly_series_add(
                result.get(output_key, {}),
                value,
                minimum,
                maximum,
            )
    return {key: value for key, value in result.items() if value}


def differentiated_polynomial_tree() -> list[dict[Degree, JetSeries]]:
    frequencies = tree.signed_frequencies()
    initial = initial_jets()
    coefficients: list[dict[Degree, JetSeries]] = [
        {} for _ in range(tree.MAXIMUM_ORDER + 1)
    ]
    for index, jet in enumerate(initial):
        degree = tuple(
            int(index == coordinate) for coordinate in range(len(frequencies))
        )
        coefficients[0][degree] = jet
    report_progress(f"initialized {len(initial)} signed input jets")

    for order in range(tree.MAXIMUM_ORDER):
        minimum = -(order + 1)
        maximum = tree.MAXIMUM_ORDER - (order + 1)
        output: dict[Degree, JetSeries] = {}
        total_pairs = sum(
            len(coefficients[left_order]) * len(coefficients[order - left_order])
            for left_order in range(order + 1)
        )
        processed_pairs = 0
        report_every = max(1, total_pairs // 10)
        next_report = report_every
        order_started = time.perf_counter()
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
                    processed_pairs += 1
                    if PROGRESS_ENABLED and processed_pairs >= next_report:
                        order_elapsed = time.perf_counter() - order_started
                        estimated_remaining = (
                            order_elapsed
                            * (total_pairs - processed_pairs)
                            / processed_pairs
                        )
                        report_progress(
                            f"tree order {order + 1}: "
                            f"{processed_pairs}/{total_pairs} degree pairs "
                            f"({100 * processed_pairs / total_pairs:.1f}%), "
                            f"pair-rate ETA {estimated_remaining:.0f}s"
                        )
                        next_report += report_every
        coefficients[order + 1] = output
        report_progress(
            f"completed tree order {order + 1}: {len(output)} degree records"
        )
    return coefficients


def aggregate_limit() -> tuple[
    dict[
        FrequencyExpansion,
        dict[tuple[int, int], dict[JetKey, PolyVector]],
    ],
    dict[JetKey, int],
]:
    frequencies = tree.signed_frequencies()
    coefficients = differentiated_polynomial_tree()
    report_progress("aggregating equal fifth-order output frequencies")
    aggregated: dict[
        tuple[FrequencyExpansion, tuple[int, int]],
        JetSeries,
    ] = {}
    for degree, jet in coefficients[5].items():
        output = tree.degree_frequency(degree, frequencies)
        catalyst_degree = tree.catalyst_degrees(degree)
        aggregate_key = output, catalyst_degree
        aggregated[aggregate_key] = jet_add(
            aggregated.get(aggregate_key, {}),
            jet,
            -5,
            0,
        )

    pole_counts = {key: 0 for key in ALL_KEYS}
    by_frequency: dict[
        FrequencyExpansion,
        dict[tuple[int, int], dict[JetKey, PolyVector]],
    ] = defaultdict(dict)
    for (output, catalyst_degree), jet in aggregated.items():
        constants: dict[JetKey, PolyVector] = {}
        for key in ALL_KEYS:
            component = jet.get(key, {})
            for power in range(-5, 0):
                coefficient = component.get(power, anti.ZERO_POLY_VECTOR)
                pole_counts[key] += sum(len(entry) for entry in coefficient)
            constant = component.get(0, anti.ZERO_POLY_VECTOR)
            if constant != anti.ZERO_POLY_VECTOR:
                constants[key] = constant
        if constants:
            by_frequency[output][catalyst_degree] = constants
    report_progress(
        f"completed Laurent aggregation: {len(by_frequency)} frequencies"
    )
    return dict(by_frequency), pole_counts


def combine_energy_keys(
    left: JetKey,
    right: JetKey,
) -> tuple[JetKey, int] | None:
    output = left[0] + right[0], left[1] + right[1]
    if sum(output) > 2:
        return None
    return output, derivative_factor(output, left)


def energy_jets(
    by_frequency: dict[
        FrequencyExpansion,
        dict[tuple[int, int], dict[JetKey, PolyVector]],
    ],
    supports: set[FrequencyExpansion] | None = None,
    progress_label: str = "energy",
) -> dict[JetKey, dict[int, Poly]]:
    result: dict[JetKey, dict[int, Poly]] = {
        key: {} for key in ALL_KEYS
    }
    selected = [
        (output, by_degree)
        for output, by_degree in by_frequency.items()
        if supports is None or output in supports
    ]
    report_every = max(1, len(selected) // 10)
    next_report = report_every
    stage_started = time.perf_counter()
    for processed, (output, by_degree) in enumerate(selected, start=1):
        leading = output[0]
        if tree.is_zero_vector(leading):
            continue
        if not leading[0] == leading[1] == leading[2]:
            raise AssertionError("A limiting output was not diagonal.")
        weight = abs(leading[0]) / tree.NORMALIZATION_SQUARED
        for left_degree, left in by_degree.items():
            for right_degree, right in by_degree.items():
                epsilon_power = sum(left_degree) + sum(right_degree)
                for left_key, left_value in left.items():
                    for right_key, right_value in right.items():
                        combination = combine_energy_keys(
                            left_key,
                            right_key,
                        )
                        if combination is None:
                            continue
                        output_key, factor = combination
                        contribution = anti.poly_scale(
                            Rational(factor) * weight,
                            anti.poly_vector_dot(left_value, right_value),
                        )
                        result[output_key][epsilon_power] = anti.poly_add(
                            result[output_key].get(epsilon_power, {}),
                            contribution,
                        )
        if PROGRESS_ENABLED and processed >= next_report:
            stage_elapsed = time.perf_counter() - stage_started
            estimated_remaining = (
                stage_elapsed * (len(selected) - processed) / processed
            )
            report_progress(
                f"{progress_label} jets: {processed}/{len(selected)} "
                f"frequencies ({100 * processed / len(selected):.1f}%), "
                f"frequency-rate ETA {estimated_remaining:.0f}s"
            )
            next_report += report_every
    return {
        key: {
            power: polynomial
            for power, polynomial in by_power.items()
            if polynomial
        }
        for key, by_power in result.items()
    }


def exact_energy_system() -> tuple[
    int,
    dict[JetKey, int],
    dict[JetKey, dict[int, Poly]],
    dict[JetKey, dict[int, Poly]],
]:
    gc_was_enabled = gc.isenabled()
    gc.disable()
    try:
        by_frequency, pole_counts = aggregate_limit()
    finally:
        if gc_was_enabled:
            gc.enable()
    total_raw = energy_jets(by_frequency, progress_label="total-energy")
    report_progress("completed total-energy jets")
    target_raw = energy_jets(
        by_frequency,
        {tree.NEXT_A_POSITIVE, tree.NEXT_A_NEGATIVE},
        progress_label="target-energy",
    )
    report_progress("completed target-energy jets")
    return len(by_frequency), pole_counts, total_raw, target_raw


def polynomial_digest(polynomial: Poly) -> str:
    payload = "\n".join(
        f"{monomial[0]},{monomial[1]}:{coefficient}"
        for monomial, coefficient in sorted(polynomial.items())
    )
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def energy_digest(by_power: dict[int, Poly]) -> str:
    payload = "\n\n".join(
        f"epsilon={power}\n{polynomial_digest(polynomial)}"
        for power, polynomial in sorted(by_power.items())
    )
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def rational_digest(value: Rational) -> str:
    return hashlib.sha256(
        f"{value.numerator}/{value.denominator}".encode("ascii")
    ).hexdigest()


def evaluate_poly(
    polynomial: Poly,
    values: tuple[Rational, Rational],
) -> Rational:
    degrees = tuple(
        max((monomial[index] for monomial in polynomial), default=0)
        for index in range(2)
    )
    powers = tuple(
        [value**power for power in range(degree + 1)]
        for value, degree in zip(values, degrees, strict=True)
    )
    result = tree.ZERO_R
    for monomial, coefficient in polynomial.items():
        result += (
            coefficient
            * powers[0][monomial[0]]
            * powers[1][monomial[1]]
        )
    return result


def poly_interval(polynomial: Poly) -> tuple[Rational, Rational]:
    center_values = CONIC_CENTER[:2]
    upper = tuple(
        center_values[index] + CONIC_RADII[index]
        for index in range(2)
    )
    degrees = tuple(
        max((monomial[index] for monomial in polynomial), default=0)
        for index in range(2)
    )
    powers = tuple(
        [value**power for power in range(degree + 1)]
        for value, degree in zip(upper, degrees, strict=True)
    )
    derivative_bounds = [tree.ZERO_R, tree.ZERO_R]
    for monomial, coefficient in polynomial.items():
        absolute = abs(coefficient)
        if monomial[0]:
            derivative_bounds[0] += (
                absolute
                * monomial[0]
                * powers[0][monomial[0] - 1]
                * powers[1][monomial[1]]
            )
        if monomial[1]:
            derivative_bounds[1] += (
                absolute
                * monomial[1]
                * powers[0][monomial[0]]
                * powers[1][monomial[1] - 1]
            )
    variation = sum(
        (
            derivative_bounds[index] * CONIC_RADII[index]
            for index in range(2)
        ),
        start=tree.ZERO_R,
    )
    center = evaluate_poly(polynomial, center_values)
    return center - variation, center + variation


Interval = tuple[Rational, Rational]


def interval_add(left: Interval, right: Interval) -> Interval:
    return left[0] + right[0], left[1] + right[1]


def interval_subtract(left: Interval, right: Interval) -> Interval:
    return left[0] - right[1], left[1] - right[0]


def interval_multiply(left: Interval, right: Interval) -> Interval:
    products = tuple(
        left_value * right_value
        for left_value in left
        for right_value in right
    )
    return min(products), max(products)


def energy_value(
    key: JetKey,
    by_power: dict[int, Poly],
    values: tuple[Rational, Rational, Rational],
) -> Rational:
    m_value, n_value, x_value = values
    pump_factor = 1 + 12 * m_value * m_value
    catalyst_factor = 1 + 3 * n_value * n_value
    result = tree.ZERO_R
    for epsilon_power, polynomial in by_power.items():
        if epsilon_power % 2:
            raise AssertionError(
                "An odd equal-amplitude power survived the signed sum."
            )
        pump_exponent = 5 * (12 - epsilon_power) + 2 * key[0]
        catalyst_exponent = 5 * epsilon_power + 2 * key[1]
        result += (
            evaluate_poly(polynomial, (m_value, n_value))
            * x_value ** (epsilon_power // 2)
            / 2**epsilon_power
            / pump_factor**pump_exponent
            / catalyst_factor**catalyst_exponent
        )
    return result


def energy_interval(
    key: JetKey,
    by_power: dict[int, Poly],
) -> Interval:
    m_lower = CONIC_CENTER[0] - CONIC_RADII[0]
    m_upper = CONIC_CENTER[0] + CONIC_RADII[0]
    n_lower = CONIC_CENTER[1] - CONIC_RADII[1]
    n_upper = CONIC_CENTER[1] + CONIC_RADII[1]
    x_lower = CONIC_CENTER[2] - CONIC_RADII[2]
    x_upper = CONIC_CENTER[2] + CONIC_RADII[2]
    pump_factor = (
        1 + 12 * m_lower * m_lower,
        1 + 12 * m_upper * m_upper,
    )
    catalyst_factor = (
        1 + 3 * n_lower * n_lower,
        1 + 3 * n_upper * n_upper,
    )
    result: Interval = (tree.ZERO_R, tree.ZERO_R)
    for epsilon_power, polynomial in by_power.items():
        if epsilon_power % 2:
            raise AssertionError(
                "An odd equal-amplitude power survived the signed sum."
            )
        pump_exponent = 5 * (12 - epsilon_power) + 2 * key[0]
        catalyst_exponent = 5 * epsilon_power + 2 * key[1]
        positive_factor = (
            x_lower ** (epsilon_power // 2) / 2**epsilon_power,
            x_upper ** (epsilon_power // 2) / 2**epsilon_power,
        )
        reciprocal_denominator = (
            1
            / pump_factor[1] ** pump_exponent
            / catalyst_factor[1] ** catalyst_exponent,
            1
            / pump_factor[0] ** pump_exponent
            / catalyst_factor[0] ** catalyst_exponent,
        )
        term = interval_multiply(poly_interval(polynomial), positive_factor)
        term = interval_multiply(term, reciprocal_denominator)
        result = interval_add(result, term)
    return result


def subtract_energy_jets(
    left: dict[JetKey, dict[int, Poly]],
    right: dict[JetKey, dict[int, Poly]],
) -> dict[JetKey, dict[int, Poly]]:
    result: dict[JetKey, dict[int, Poly]] = {}
    for key in ALL_KEYS:
        by_power: dict[int, Poly] = {}
        for power in set(left[key]).union(right[key]):
            polynomial = anti.poly_add(
                left[key].get(power, {}),
                anti.poly_scale(-Rational(1), right[key].get(power, {})),
            )
            if polynomial:
                by_power[power] = polynomial
        result[key] = by_power
    return result


def validate_tail_algebra_preflight() -> None:
    """Exercise final energy subtraction before the expensive tree run."""

    left = {key: {} for key in ALL_KEYS}
    right = {key: {} for key in ALL_KEYS}
    left[BASE_KEY] = {0: {(0, 0): Rational(3)}}
    right[BASE_KEY] = {0: {(0, 0): Rational(1)}}
    difference = subtract_energy_jets(left, right)
    assert difference[BASE_KEY][0][(0, 0)] == Rational(2)
    if gmpy2 is not None:
        assert isinstance(tree.ZERO_R, gmpy2.mpq)


def conic_chart_m(value: Rational) -> Rational:
    return 24 * value / (1 - 12 * value * value)


def conic_chart_n(value: Rational) -> Rational:
    return 6 * value / (1 - 3 * value * value)


def conic_box_contains_stationary_box() -> bool:
    m_lower = CONIC_CENTER[0] - CONIC_RADII[0]
    m_upper = CONIC_CENTER[0] + CONIC_RADII[0]
    n_lower = CONIC_CENTER[1] - CONIC_RADII[1]
    n_upper = CONIC_CENTER[1] + CONIC_RADII[1]
    p_lower = anti.ROOT_CENTER[0] - anti.ROOT_RADIUS
    p_upper = anti.ROOT_CENTER[0] + anti.ROOT_RADIUS
    q_lower = anti.ROOT_CENTER[1] - anti.ROOT_RADIUS
    q_upper = anti.ROOT_CENTER[1] + anti.ROOT_RADIUS
    return (
        conic_chart_m(m_lower) <= p_lower
        and conic_chart_m(m_upper) >= p_upper
        and conic_chart_n(n_lower) <= q_lower
        and conic_chart_n(n_upper) >= q_upper
    )


def energy_record(by_power: dict[int, Poly]) -> dict[str, object]:
    monomials = [
        monomial
        for polynomial in by_power.values()
        for monomial in polynomial
    ]
    return {
        "termCount": sum(len(polynomial) for polynomial in by_power.values()),
        "termCountByEpsilonPower": {
            str(power): len(polynomial)
            for power, polynomial in sorted(by_power.items())
        },
        "degreeM": max((monomial[0] for monomial in monomials), default=0),
        "degreeN": max((monomial[1] for monomial in monomials), default=0),
        "epsilonPowers": sorted(by_power),
        "exactDigest": energy_digest(by_power),
    }


def audit() -> dict[str, object]:
    frequency_count, pole_counts, total, target = exact_energy_system()
    external = subtract_energy_jets(total, target)

    # Common first derivatives vanish identically on the antisymmetric chart.
    first_derivatives_zero = {
        "totalCommonPump": not total[COMMON_PUMP_KEY],
        "totalCommonCatalyst": not total[COMMON_CATALYST_KEY],
        "targetCommonPump": not target[COMMON_PUMP_KEY],
        "targetCommonCatalyst": not target[COMMON_CATALYST_KEY],
    }

    derivative_keys = {
        "aa": COMMON_PUMP_SECOND_KEY,
        "ab": COMMON_MIXED_KEY,
        "bb": COMMON_CATALYST_SECOND_KEY,
    }

    refined_values = (
        refined.M_PARAMETER,
        refined.N_PARAMETER,
        refined.X_CANDIDATE,
    )
    target_refined = energy_value(BASE_KEY, target[BASE_KEY], refined_values)
    external_refined = energy_value(
        BASE_KEY,
        external[BASE_KEY],
        refined_values,
    )
    refined_hessian = {
        label: (
            energy_value(key, external[key], refined_values) * target_refined
            - external_refined
            * energy_value(key, target[key], refined_values)
        )
        / target_refined**2
        for label, key in derivative_keys.items()
    }

    target_interval = energy_interval(BASE_KEY, target[BASE_KEY])
    external_interval = energy_interval(BASE_KEY, external[BASE_KEY])
    numerator_intervals = {}
    for label, key in derivative_keys.items():
        numerator_intervals[label] = interval_subtract(
            interval_multiply(
                energy_interval(key, external[key]),
                target_interval,
            ),
            interval_multiply(
                external_interval,
                energy_interval(key, target[key]),
            ),
        )
    center_target = energy_value(BASE_KEY, target[BASE_KEY], CONIC_CENTER)
    center_external = energy_value(
        BASE_KEY,
        external[BASE_KEY],
        CONIC_CENTER,
    )
    center_hessian = {
        label: (
            energy_value(key, external[key], CONIC_CENTER) * center_target
            - center_external * energy_value(key, target[key], CONIC_CENTER)
        )
        / center_target**2
        for label, key in derivative_keys.items()
    }
    if target_interval[0] <= 0:
        raise AssertionError("The target numerator crossed zero.")
    a_interval = numerator_intervals["aa"]
    b_interval = numerator_intervals["ab"]
    c_interval = numerator_intervals["bb"]
    maximum_b = max(abs(b_interval[0]), abs(b_interval[1]))
    determinant_lower = a_interval[0] * c_interval[0] - maximum_b**2
    first_minor_lower = a_interval[0] / target_interval[1] ** 2
    determinant_quotient_lower = determinant_lower / target_interval[1] ** 4
    positive_definite = first_minor_lower > 0 and determinant_quotient_lower > 0

    return {
        "scope": "common-rotation Hessian on the R0.18 stationary box",
        "rationalBackend": RATIONAL_BACKEND,
        "aggregatedFrequencyCount": frequency_count,
        "uncancelledLaurentMonomialCounts": {
            f"{key[0]},{key[1]}": count
            for key, count in pole_counts.items()
        },
        "factorizedDenominators": (
            "(1+12m^2)^(5(12-s)+2a) "
            "(1+3n^2)^(5s+2b)"
        ),
        "energyJets": {
            "targetBase": energy_record(target[BASE_KEY]),
            "externalBase": energy_record(external[BASE_KEY]),
            "targetCommonPumpSecond": energy_record(
                target[COMMON_PUMP_SECOND_KEY]
            ),
            "externalCommonPumpSecond": energy_record(
                external[COMMON_PUMP_SECOND_KEY]
            ),
            "targetCommonMixed": energy_record(target[COMMON_MIXED_KEY]),
            "externalCommonMixed": energy_record(
                external[COMMON_MIXED_KEY]
            ),
            "targetCommonCatalystSecond": energy_record(
                target[COMMON_CATALYST_SECOND_KEY]
            ),
            "externalCommonCatalystSecond": energy_record(
                external[COMMON_CATALYST_SECOND_KEY]
            ),
        },
        "exactBlockDecoupling": {
            **first_derivatives_zero,
            "allCommonFirstDerivativesIdenticallyZero": all(
                first_derivatives_zero.values()
            ),
        },
        "refinedRationalPoint": {
            "commonPumpCurvature": float(refined_hessian["aa"]),
            "commonMixedCurvature": float(refined_hessian["ab"]),
            "commonCatalystCurvature": float(refined_hessian["bb"]),
            "commonDeterminant": float(
                refined_hessian["aa"] * refined_hessian["bb"]
                - refined_hessian["ab"] ** 2
            ),
            "curvatureDigests": {
                label: rational_digest(value)
                for label, value in refined_hessian.items()
            },
        },
        "stationaryConicBox": {
            "center": [str(value) for value in CONIC_CENTER],
            "radii": [str(value) for value in CONIC_RADII],
            "containsR018ChartBox": conic_box_contains_stationary_box(),
            "targetPositive": target_interval[0] > 0,
            "centerCommonPumpCurvature": float(center_hessian["aa"]),
            "centerCommonMixedCurvature": float(center_hessian["ab"]),
            "centerCommonCatalystCurvature": float(center_hessian["bb"]),
            "centerCommonDeterminant": float(
                center_hessian["aa"] * center_hessian["bb"]
                - center_hessian["ab"] ** 2
            ),
            "commonFirstMinorLower": float(first_minor_lower),
            "commonDeterminantLower": float(determinant_quotient_lower),
            "firstMinorLowerDigest": rational_digest(first_minor_lower),
            "determinantLowerDigest": rational_digest(
                determinant_quotient_lower
            ),
            "commonBlockPositiveDefinite": positive_definite,
        },
        "fullHessianAtStationaryPoint": {
            "antisymmetricBlockPositiveDefinite": True,
            "commonBlockPositiveDefinite": positive_definite,
            "mixedBlockIdenticallyZero": all(first_derivatives_zero.values()),
            "positiveDefinite": (
                positive_definite and all(first_derivatives_zero.values())
            ),
        },
    }


def validate(result: dict[str, object]) -> None:
    assert result["aggregatedFrequencyCount"] == 334
    assert all(
        count == 0
        for count in result["uncancelledLaurentMonomialCounts"].values()
    )
    assert result["exactBlockDecoupling"][
        "allCommonFirstDerivativesIdenticallyZero"
    ]
    refined_record = result["refinedRationalPoint"]
    assert abs(refined_record["commonPumpCurvature"] - 0.8962731886310136) < 1e-12
    assert abs(refined_record["commonMixedCurvature"] + 0.10295436336623097) < 1e-12
    assert abs(refined_record["commonCatalystCurvature"] - 0.568844480929256) < 1e-12
    assert abs(refined_record["commonDeterminant"] - 0.4992404558214721) < 1e-12
    stationary = result["stationaryConicBox"]
    assert stationary["containsR018ChartBox"]
    assert stationary["targetPositive"]
    assert stationary["commonBlockPositiveDefinite"]
    assert result["fullHessianAtStationaryPoint"]["positiveDefinite"]


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument(
        "--progress",
        action="store_true",
        help="report long exact-algebra stages to standard error",
    )
    return parser.parse_args()


def main() -> None:
    global PROGRESS_ENABLED, PROGRESS_STARTED
    arguments = parse_arguments()
    PROGRESS_ENABLED = arguments.progress
    PROGRESS_STARTED = time.perf_counter()
    report_progress(f"using exact rational backend {RATIONAL_BACKEND}")
    validate_tail_algebra_preflight()
    report_progress("passed tail-algebra preflight")
    result = audit()
    if arguments.check:
        validate(result)
    print(json.dumps(result, indent=2 if arguments.pretty else None))


if __name__ == "__main__":
    main()
