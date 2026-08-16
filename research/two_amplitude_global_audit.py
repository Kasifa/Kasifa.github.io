#!/usr/bin/env python3
"""Certified amplitude and phase audit for the fifth-order cone relay.

This script continues fifth_order_tree_audit.py. It keeps the positive and
negative catalyst leaves separate, so two complex catalyst amplitudes can be
inserted before the order-five energy is formed. Exact conjugation shows that
the energy depends only on the relative phase and has harmonics at most three.

The exchange symmetry is encoded by three real invariants

    x = |beta + delta|^2,
    y = |beta - delta|^2,
    h = 4 |beta|^2 |delta|^2 sin(theta)^2,

whose exact domain is x >= 0, y >= 0, 0 <= h <= x*y.

Two independent certificates are produced. On the real boundary h=0, a
subresultant eliminant and Sturm root isolation enumerate every positive
stationary point. For arbitrary complex amplitudes, radial compactification
maps the domain to the unit cube, where a rational Bernstein subdivision
proves X/T >= 45.739348.

Every algebraic coefficient and every Bernstein coefficient used by the
certificate is rational. Floating-point values are output only as readable
approximations after the exact sign checks have passed.

This is a finite-order algebra result for fixed R0.11 polarizations. It does
not estimate the Navier--Stokes Taylor remainder or prove regularity or
singularity for the PDE.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
import gc
import hashlib
from itertools import product
import json
import math
from pathlib import Path
import subprocess
import sys

import sympy as sp

import fifth_order_tree_audit as tree


sys.set_int_max_str_digits(0)

Rational = sp.Rational
Index3 = tuple[int, int, int]
Interval = tuple[Rational, Rational]
SignedCatalystDegree = tuple[int, int, int, int]
TrigKey = tuple[int, int, int]

X_VAR, Y_VAR, H_VAR = sp.symbols("x y h", nonnegative=True)
R_VAR, Q_VAR = sp.symbols("r q", positive=True)
Z_VAR, A_VAR, S_VAR = sp.symbols("z a s", nonnegative=True)

COMPLEX_LOWER_BOUND = Rational(11_434_837, 250_000)
BERNSTEIN_MAXIMUM_DEPTH = 52

# Exact h=0 coefficients in the invariant variables x=(b+d)^2 and
# y=(b-d)^2. They let the subresultant/Sturm certificate run in an isolated
# process, while the parent independently verifies them against the full
# signed-tree construction.
REAL_EXTERNAL_COEFFICIENTS = {
    (6, 0): (69777, 6553600),
    (5, 1): (-4383, 131072),
    (5, 0): (36561930673, 1101004800),
    (4, 2): (269343, 6553600),
    (4, 1): (-70731104489, 1101004800),
    (4, 0): (29552031913871, 6422528000),
    (3, 3): (-11997, 327680),
    (3, 2): (130467755477, 2752512000),
    (3, 1): (-25654018671287, 2752512000),
    (3, 0): (113164737228373, 1605632000),
    (2, 4): (269343, 6553600),
    (2, 3): (-33066950753, 2752512000),
    (2, 2): (33227924945737, 3853516800),
    (2, 1): (-6130320647159, 64225280),
    (2, 0): (11840914401291, 200704000),
    (1, 5): (-4383, 131072),
    (1, 4): (-23729563523, 1101004800),
    (1, 3): (-15265094887837, 2752512000),
    (1, 2): (4762145064359, 1605632000),
    (1, 1): (-290677975509, 6272000),
    (1, 0): (305080037, 156800),
    (0, 6): (69777, 6553600),
    (0, 5): (35596537749, 1835008000),
    (0, 4): (1730161579991, 642252800),
    (0, 3): (57411517664547, 1605632000),
    (0, 2): (10642714961381, 200704000),
    (0, 1): (38552469807, 5017600),
    (0, 0): (69777, 3200),
}

REAL_TARGET_COEFFICIENTS = {
    (2, 0): (2284553209, 1254400),
    (1, 1): (-1909531749, 627200),
    (0, 2): (72948681, 50176),
}


def fraction(value: Fraction | int | sp.Rational) -> Rational:
    """Convert a standard-library or SymPy rational to sp.Rational."""

    if isinstance(value, Fraction):
        return Rational(value.numerator, value.denominator)
    return Rational(value)


def signed_catalyst_degree(degree: tree.Degree) -> SignedCatalystDegree:
    """Return positive/negative leaf counts for b and d."""

    return degree[2], degree[6], degree[3], degree[7]


def aggregate_signed_complex_limit() -> tuple[
    dict[
        tree.FrequencyExpansion,
        dict[SignedCatalystDegree, tree.Vector],
    ],
    int,
]:
    """Aggregate exact order-five constants without collapsing conjugates."""

    frequencies = tree.signed_frequencies()
    coefficients = tree.pure_tree_coefficients(
        frequencies,
        tree.signed_polarizations(),
    )
    aggregated: dict[
        tuple[tree.FrequencyExpansion, SignedCatalystDegree],
        tree.VectorSeries,
    ] = {}
    for degree, value in coefficients[5].items():
        output = tree.degree_frequency(degree, frequencies)
        catalyst_degree = signed_catalyst_degree(degree)
        key = output, catalyst_degree
        aggregated[key] = tree.series_add(
            aggregated.get(key, {}),
            value,
            -5,
            0,
        )

    pole_count = 0
    by_frequency: dict[
        tree.FrequencyExpansion,
        dict[SignedCatalystDegree, tree.Vector],
    ] = defaultdict(dict)
    for (output, degree), series in aggregated.items():
        for power in range(-5, 0):
            if not tree.is_zero_vector(series.get(power, tree.ZERO_VECTOR)):
                pole_count += 1
        constant = series.get(0, tree.ZERO_VECTOR)
        if not tree.is_zero_vector(constant):
            by_frequency[output][degree] = constant
    return dict(by_frequency), pole_count


def add_rational(
    polynomial: dict[tuple[int, ...], Fraction],
    key: tuple[int, ...],
    value: Fraction,
) -> None:
    polynomial[key] = polynomial.get(key, tree.ZERO_R) + value


def complex_energy_monomials(
    by_frequency: dict[
        tree.FrequencyExpansion,
        dict[SignedCatalystDegree, tree.Vector],
    ],
    supports: set[tree.FrequencyExpansion] | None = None,
) -> dict[tuple[int, int, int, int], Fraction]:
    """Return energy in beta, beta-bar, delta and delta-bar."""

    polynomial: dict[tuple[int, ...], Fraction] = {}
    for output, coefficients in by_frequency.items():
        if supports is not None and output not in supports:
            continue
        leading = output[0]
        if tree.is_zero_vector(leading):
            continue
        if not (leading[0] == leading[1] == leading[2]):
            raise AssertionError("Every nonzero limiting frequency must be diagonal.")
        weight = abs(leading[0])
        for left_degree, left in coefficients.items():
            for right_degree, right in coefficients.items():
                value = (
                    weight
                    * tree.dot(left, right)
                    / tree.NORMALIZATION_SQUARED
                )
                if value == 0:
                    continue
                exponent = (
                    left_degree[0] + right_degree[1],
                    left_degree[1] + right_degree[0],
                    left_degree[2] + right_degree[3],
                    left_degree[3] + right_degree[2],
                )
                add_rational(polynomial, exponent, value)
    return {key: value for key, value in polynomial.items() if value != 0}


def trigonometric_energy(
    monomials: dict[tuple[int, int, int, int], Fraction],
) -> dict[TrigKey, Fraction]:
    """Combine conjugate monomials into cos(m theta) coefficients."""

    charged: dict[tuple[int, ...], Fraction] = {}
    for exponent, coefficient in monomials.items():
        b_power = exponent[0] + exponent[1]
        d_power = exponent[2] + exponent[3]
        b_charge = exponent[0] - exponent[1]
        d_charge = exponent[2] - exponent[3]
        if b_charge != -d_charge:
            raise AssertionError("The energy has more than one phase charge.")
        add_rational(charged, (b_power, d_power, b_charge), coefficient)

    result: dict[TrigKey, Fraction] = {}
    for (b_power, d_power, charge), coefficient in charged.items():
        if charge < 0:
            continue
        if charge == 0:
            result[(b_power, d_power, 0)] = coefficient
            continue
        reflected = charged[(b_power, d_power, -charge)]
        if reflected != coefficient:
            raise AssertionError("Conjugate phase coefficients do not match.")
        result[(b_power, d_power, charge)] = 2 * coefficient
    return result


def power_sum(power: int, total: sp.Expr, product_: sp.Expr) -> sp.Expr:
    """Return U^power+V^power from U+V and U*V."""

    if power == 0:
        return sp.Integer(2)
    if power == 1:
        return total
    previous_two = sp.Integer(2)
    previous_one = total
    for _ in range(2, power + 1):
        current = sp.expand(total * previous_one - product_ * previous_two)
        previous_two, previous_one = previous_one, current
    return previous_one


def symmetric_uv_to_elementary(expression: sp.Expr) -> sp.Expr:
    """Rewrite a U,V-symmetric polynomial using A=U+V and W=U*V."""

    u_var, v_var, a_var, w_var, b_var = sp.symbols("U V A W B")
    polynomial = sp.Poly(expression, u_var, v_var, b_var, domain=sp.QQ)
    terms = dict(polynomial.terms())
    used: set[tuple[int, int, int]] = set()
    result = sp.Integer(0)
    for (u_power, v_power, b_power), coefficient in terms.items():
        key = u_power, v_power, b_power
        if key in used:
            continue
        if u_power == v_power:
            result += coefficient * w_var**u_power * b_var**b_power
            used.add(key)
            continue
        reflected_key = v_power, u_power, b_power
        if terms.get(reflected_key) != coefficient:
            raise AssertionError("The amplitude polynomial is not exchange-symmetric.")
        low = min(u_power, v_power)
        gap = abs(u_power - v_power)
        result += (
            coefficient
            * w_var**low
            * power_sum(gap, a_var, w_var)
            * b_var**b_power
        )
        used.add(key)
        used.add(reflected_key)
    return sp.expand(result)


def invariant_polynomial(trigonometric: dict[TrigKey, Fraction]) -> sp.Expr:
    """Return the exact polynomial in x, y, h."""

    u_var, v_var, b_var = sp.symbols("U V B")
    expression = sp.Integer(0)
    for (b_power, d_power, harmonic), raw_coefficient in trigonometric.items():
        coefficient = fraction(raw_coefficient)
        if harmonic == 0:
            term = u_var ** (b_power // 2) * v_var ** (d_power // 2)
        elif harmonic == 1:
            term = (
                u_var ** ((b_power - 1) // 2)
                * v_var ** ((d_power - 1) // 2)
                * b_var
                / 2
            )
        elif harmonic == 2:
            term = (
                u_var ** ((b_power - 2) // 2)
                * v_var ** ((d_power - 2) // 2)
                * (b_var**2 / 2 - u_var * v_var)
            )
        elif harmonic == 3:
            term = (
                u_var ** ((b_power - 3) // 2)
                * v_var ** ((d_power - 3) // 2)
                * (b_var**3 / 2 - 3 * u_var * v_var * b_var / 2)
            )
        else:
            raise AssertionError("Unexpected phase harmonic.")
        expression += coefficient * term

    elementary = symmetric_uv_to_elementary(sp.expand(expression))
    a_var, w_var, b_var = sp.symbols("A W B")
    phase_inner_product = (X_VAR - Y_VAR) / 2
    substitutions = {
        a_var: (X_VAR + Y_VAR) / 2,
        b_var: phase_inner_product,
        w_var: (phase_inner_product**2 + H_VAR) / 4,
    }
    return sp.expand(elementary.subs(substitutions))


def polynomial_digest(polynomial: sp.Poly) -> str:
    payload = "\n".join(
        f"{monomial}:{coefficient}"
        for monomial, coefficient in polynomial.terms()
    )
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def interval_add(left: Interval, right: Interval) -> Interval:
    return left[0] + right[0], left[1] + right[1]


def interval_scale(value: Rational, interval: Interval) -> Interval:
    products = value * interval[0], value * interval[1]
    return min(products), max(products)


def interval_multiply(left: Interval, right: Interval) -> Interval:
    products = (
        left[0] * right[0],
        left[0] * right[1],
        left[1] * right[0],
        left[1] * right[1],
    )
    return min(products), max(products)


def interval_power(interval: Interval, power: int) -> Interval:
    if power == 0:
        return Rational(1), Rational(1)
    if interval[0] < 0:
        raise ValueError("Only nonnegative variable intervals are used.")
    return interval[0] ** power, interval[1] ** power


def interval_reciprocal(interval: Interval) -> Interval:
    if interval[0] <= 0 <= interval[1]:
        raise ZeroDivisionError("The denominator interval contains zero.")
    values = 1 / interval[0], 1 / interval[1]
    return min(values), max(values)


def interval_divide(numerator: Interval, denominator: Interval) -> Interval:
    return interval_multiply(numerator, interval_reciprocal(denominator))


def polynomial_interval(
    polynomial: sp.Poly,
    boxes: dict[sp.Symbol, Interval],
) -> Interval:
    """Natural exact interval evaluation on a nonnegative rational box."""

    result: Interval = Rational(0), Rational(0)
    for monomial, coefficient in polynomial.terms():
        term: Interval = Rational(1), Rational(1)
        for variable, power in zip(polynomial.gens, monomial, strict=True):
            term = interval_multiply(
                term,
                interval_power(boxes[variable], power),
            )
        result = interval_add(
            result,
            interval_scale(Rational(coefficient), term),
        )
    return result


def primitive_integer_polynomial(
    expression: sp.Expr,
    *variables: sp.Symbol,
) -> sp.Poly:
    polynomial = sp.Poly(expression, *variables, domain=sp.QQ)
    _, integer_polynomial = polynomial.clear_denoms()
    _, primitive = integer_polynomial.primitive()
    if primitive.LC() < 0:
        primitive = -primitive
    return primitive


def sign_changes(polynomial: sp.Poly) -> int:
    signs = [
        1 if coefficient > 0 else -1
        for coefficient in polynomial.all_coeffs()
        if coefficient != 0
    ]
    return sum(
        signs[index] != signs[index - 1]
        for index in range(1, len(signs))
    )


def positive_root_intervals(polynomial: sp.Poly, digits: int) -> list[Interval]:
    tolerance = Rational(1, 10**digits)
    return [
        (Rational(interval[0]), Rational(interval[1]))
        for interval, multiplicity in sp.intervals(polynomial, eps=tolerance)
        if interval[0] > 0 and multiplicity == 1
    ]


def interval_record(interval: Interval) -> dict[str, object]:
    return {
        "lower": str(interval[0]),
        "upper": str(interval[1]),
        "lowerDecimal": float(interval[0]),
        "upperDecimal": float(interval[1]),
    }


def compact_interval_record(interval: Interval) -> dict[str, object]:
    """Record a large exact interval by decimal endpoints and a digest."""

    payload = f"{interval[0]}\n{interval[1]}"
    return {
        "lowerDecimal": float(interval[0]),
        "upperDecimal": float(interval[1]),
        "exactEndpointDigest": hashlib.sha256(
            payload.encode("ascii")
        ).hexdigest(),
    }


def boundary_record(
    external: sp.Expr,
    target: sp.Expr,
    variable: sp.Symbol,
    zero_variable: sp.Symbol,
) -> dict[str, object]:
    boundary_external = sp.expand(external.subs(zero_variable, 0))
    boundary_target = sp.expand(target.subs(zero_variable, 0))
    stationary = primitive_integer_polynomial(
        variable * sp.diff(boundary_external, variable) - 2 * boundary_external,
        variable,
    )
    roots = positive_root_intervals(stationary, 45)
    if len(roots) != 1:
        raise AssertionError("A boundary must have one positive stationary root.")
    root = roots[0]
    ratio = interval_divide(
        polynomial_interval(
            sp.Poly(boundary_external, variable, domain=sp.QQ),
            {variable: root},
        ),
        polynomial_interval(
            sp.Poly(boundary_target, variable, domain=sp.QQ),
            {variable: root},
        ),
    )
    root_midpoint = (root[0] + root[1]) / 2
    return {
        "stationaryDegree": stationary.degree(),
        "stationarySignChanges": sign_changes(stationary),
        "positiveRootCount": int(stationary.count_roots(0, sp.oo)),
        "stationaryPolynomial": [
            {
                "power": stationary.degree() - index,
                "coefficient": str(coefficient),
            }
            for index, coefficient in enumerate(stationary.all_coeffs())
            if coefficient != 0
        ],
        "radialRoot": interval_record(root),
        "catalystMagnitude": math.sqrt(float(root_midpoint)) / 2,
        "externalOverTarget": interval_record(ratio),
    }


def real_critical_polynomials(
    external: sp.Expr,
    target: sp.Expr,
) -> tuple[sp.Expr, sp.Expr, sp.Poly, sp.Poly]:
    external_rq = sp.expand(
        external.subs({X_VAR: R_VAR, Y_VAR: Q_VAR * R_VAR})
    )
    target_rq = sp.expand(
        target.subs({X_VAR: R_VAR, Y_VAR: Q_VAR * R_VAR})
    )
    radial_stationary = primitive_integer_polynomial(
        R_VAR * sp.diff(external_rq, R_VAR) - 2 * external_rq,
        R_VAR,
        Q_VAR,
    )
    directional_stationary = primitive_integer_polynomial(
        sp.diff(external_rq, Q_VAR) * target_rq
        - external_rq * sp.diff(target_rq, Q_VAR),
        R_VAR,
        Q_VAR,
    )
    return external_rq, target_rq, radial_stationary, directional_stationary


def real_interior_record(
    external: sp.Expr,
    target: sp.Expr,
) -> dict[str, object]:
    (
        external_rq,
        target_rq,
        radial_stationary,
        directional_stationary,
    ) = real_critical_polynomials(external, target)
    sequence = sp.subresultants(
        radial_stationary.as_expr(),
        directional_stationary.as_expr(),
        R_VAR,
    )
    if len(sequence) != 8:
        raise AssertionError("Unexpected subresultant-chain length.")
    linear_relation = sp.Poly(sequence[-2], R_VAR, Q_VAR, domain=sp.QQ)
    resultant = primitive_integer_polynomial(sequence[-1], Q_VAR)
    factors = sp.factor_list(resultant.as_expr())[1]
    degree_one_factors = [
        factor for factor, multiplicity in factors
        if sp.degree(factor, Q_VAR) == 1 and multiplicity == 1
    ]
    degree_35_factors = [
        factor for factor, multiplicity in factors
        if sp.degree(factor, Q_VAR) == 35 and multiplicity == 1
    ]
    if len(degree_one_factors) != 1 or len(degree_35_factors) != 1:
        raise AssertionError("The resultant must factor into degrees 1 and 35.")
    eliminant = primitive_integer_polynomial(
        degree_35_factors[0],
        Q_VAR,
    )
    radial_coefficient = sp.Poly(
        sp.Poly(linear_relation.as_expr(), R_VAR).coeff_monomial(R_VAR),
        Q_VAR,
        domain=sp.QQ,
    )
    radial_offset = sp.Poly(
        sp.Poly(linear_relation.as_expr(), R_VAR).coeff_monomial(1),
        Q_VAR,
        domain=sp.QQ,
    )

    root_intervals = positive_root_intervals(eliminant, 78)
    radial_intervals: list[Interval] = []
    for q_interval in root_intervals:
        coefficient_interval = polynomial_interval(
            radial_coefficient,
            {Q_VAR: q_interval},
        )
        offset_interval = polynomial_interval(
            radial_offset,
            {Q_VAR: q_interval},
        )
        radial_intervals.append(
            interval_divide(
                (-offset_interval[1], -offset_interval[0]),
                coefficient_interval,
            )
        )
    positive_indices = [
        index
        for index, interval in enumerate(radial_intervals)
        if interval[0] > 0
    ]
    if len(positive_indices) != 1:
        raise AssertionError("There must be one positive interior scale.")
    positive_index = positive_indices[0]
    q_interval = root_intervals[positive_index]
    r_interval = radial_intervals[positive_index]
    ratio_interval = interval_divide(
        polynomial_interval(
            sp.Poly(external_rq, R_VAR, Q_VAR, domain=sp.QQ),
            {R_VAR: r_interval, Q_VAR: q_interval},
        ),
        polynomial_interval(
            sp.Poly(target_rq, R_VAR, Q_VAR, domain=sp.QQ),
            {R_VAR: r_interval, Q_VAR: q_interval},
        ),
    )
    return {
        "radialStationaryDegrees": [
            radial_stationary.degree(R_VAR),
            radial_stationary.degree(Q_VAR),
        ],
        "directionalStationaryDegrees": [
            directional_stationary.degree(R_VAR),
            directional_stationary.degree(Q_VAR),
        ],
        "subresultantDegrees": [
            [
                sp.Poly(item, R_VAR, Q_VAR).degree(R_VAR),
                sp.Poly(item, R_VAR, Q_VAR).degree(Q_VAR),
            ]
            for item in sequence
        ],
        "resultantDegree": resultant.degree(),
        "resultantFactorDegrees": sorted(
            int(sp.degree(factor, Q_VAR))
            for factor, _ in factors
        ),
        "eliminantDegree": eliminant.degree(),
        "eliminantDigest": polynomial_digest(eliminant),
        # sp.intervals is a Sturm isolator and returned every real root.
        # All eleven isolating intervals lie in the positive half-line.
        "allRealRootCount": len(root_intervals),
        "positiveDirectionalRootCount": len(root_intervals),
        "positiveScaleCount": len(positive_indices),
        "scaleSigns": [
            1 if interval[0] > 0 else -1
            for interval in radial_intervals
        ],
        "positivePoint": {
            "qEqualsYOverX": compact_interval_record(q_interval),
            "x": compact_interval_record(r_interval),
            "externalOverTarget": compact_interval_record(ratio_interval),
        },
    }


def power_to_bernstein(
    polynomial: sp.Poly,
    degrees: Index3,
) -> dict[Index3, Rational]:
    """Convert a power polynomial on the unit cube to Bernstein form."""

    power_coefficients = {
        index: Rational(polynomial.coeff_monomial(
            Z_VAR**index[0] * A_VAR**index[1] * S_VAR**index[2]
        ))
        for index in product(*(range(degree + 1) for degree in degrees))
    }
    bernstein: dict[Index3, Rational] = {}
    for upper in product(*(range(degree + 1) for degree in degrees)):
        value = Rational(0)
        for lower in product(*(range(index + 1) for index in upper)):
            factor = Rational(1)
            for axis in range(3):
                factor *= Rational(
                    math.comb(upper[axis], lower[axis]),
                    math.comb(degrees[axis], lower[axis]),
                )
            value += power_coefficients[lower] * factor
        bernstein[upper] = value
    return bernstein


def split_bernstein(
    coefficients: dict[Index3, Rational],
    degrees: Index3,
    axis: int,
) -> tuple[dict[Index3, Rational], dict[Index3, Rational]]:
    """Split one Bernstein box at the midpoint using de Casteljau."""

    left: dict[Index3, Rational] = {}
    right: dict[Index3, Rational] = {}
    other_axes = [index for index in range(3) if index != axis]
    for fixed in product(
        range(degrees[other_axes[0]] + 1),
        range(degrees[other_axes[1]] + 1),
    ):
        base_indices = [0, 0, 0]
        base_indices[other_axes[0]] = fixed[0]
        base_indices[other_axes[1]] = fixed[1]
        values = []
        for axis_index in range(degrees[axis] + 1):
            base_indices[axis] = axis_index
            values.append(coefficients[tuple(base_indices)])
        levels = [values]
        for _ in range(degrees[axis]):
            previous = levels[-1]
            levels.append([
                (previous[index] + previous[index + 1]) / 2
                for index in range(len(previous) - 1)
            ])
        for axis_index in range(degrees[axis] + 1):
            base_indices[axis] = axis_index
            left[tuple(base_indices)] = levels[axis_index][0]
            right[tuple(base_indices)] = (
                levels[degrees[axis] - axis_index][axis_index]
            )
    return left, right


def bernstein_variation(
    coefficients: dict[Index3, Rational],
    degrees: Index3,
    axis: int,
) -> float:
    maximum = 0.0
    for index in product(*(range(degree + 1) for degree in degrees)):
        if index[axis] == degrees[axis]:
            continue
        neighbor = list(index)
        neighbor[axis] += 1
        maximum = max(
            maximum,
            abs(float(coefficients[tuple(neighbor)] - coefficients[index])),
        )
    return maximum


def bernstein_certificate(
    external: sp.Expr,
    target: sp.Expr,
) -> dict[str, object]:
    """Prove the rational complex-amplitude lower bound on the unit cube."""

    radial = Z_VAR / (1 - Z_VAR)
    substitutions = {
        X_VAR: radial * A_VAR,
        Y_VAR: radial * (1 - A_VAR),
        H_VAR: radial**2 * A_VAR * (1 - A_VAR) * S_VAR,
    }
    compact_expression = sp.cancel(
        (external - COMPLEX_LOWER_BOUND * target).subs(substitutions)
        * (1 - Z_VAR) ** 6
    )
    compact = sp.Poly(
        compact_expression,
        Z_VAR,
        A_VAR,
        S_VAR,
        domain=sp.QQ,
    )
    degrees: Index3 = (
        compact.degree(Z_VAR),
        compact.degree(A_VAR),
        compact.degree(S_VAR),
    )
    if degrees != (6, 6, 3):
        raise AssertionError("Unexpected compactified polynomial degrees.")
    initial = power_to_bernstein(compact, degrees)
    initial_negative_count = sum(
        1 for value in initial.values() if bool(value < 0)
    )

    stack: list[tuple[dict[Index3, Rational], int, str]] = [
        (initial, 0, "")
    ]
    leaves: list[tuple[str, Rational, Rational]] = []
    maximum_depth = 0
    while stack:
        coefficients, depth, path = stack.pop()
        minimum = min(coefficients.values())
        maximum = max(coefficients.values())
        if minimum >= 0:
            leaves.append((path, minimum, maximum))
            maximum_depth = max(maximum_depth, depth)
            continue
        if depth >= BERNSTEIN_MAXIMUM_DEPTH:
            raise AssertionError("Bernstein subdivision did not certify the box.")
        variations = [
            bernstein_variation(coefficients, degrees, axis)
            for axis in range(3)
        ]
        axis = max(range(3), key=lambda index: variations[index])
        left, right = split_bernstein(coefficients, degrees, axis)
        label = "zas"[axis]
        stack.append((right, depth + 1, f"{path}{label}R"))
        stack.append((left, depth + 1, f"{path}{label}L"))

    leaf_payload = "\n".join(
        f"{path}:{minimum}:{maximum}"
        for path, minimum, maximum in sorted(leaves)
    )
    return {
        "lowerBound": str(COMPLEX_LOWER_BOUND),
        "lowerBoundDecimal": float(COMPLEX_LOWER_BOUND),
        "compactifiedDegrees": list(degrees),
        "compactifiedTermCount": len(compact.terms()),
        "compactifiedDigest": polynomial_digest(compact),
        "initialNegativeBernsteinCount": initial_negative_count,
        "certifiedLeafCount": len(leaves),
        "maximumSubdivisionDepth": maximum_depth,
        "zeroMinimumLeafCount": sum(
            1 for _, minimum, _ in leaves if minimum == 0
        ),
        "allLeafCoefficientsNonnegative": True,
        "partitionDigest": hashlib.sha256(
            leaf_payload.encode("ascii")
        ).hexdigest(),
    }


def polynomial_summary(polynomial: sp.Expr) -> dict[str, object]:
    poly = sp.Poly(polynomial, X_VAR, Y_VAR, H_VAR, domain=sp.QQ)
    return {
        "termCount": len(poly.terms()),
        "degrees": [
            poly.degree(X_VAR),
            poly.degree(Y_VAR),
            poly.degree(H_VAR),
        ],
        "digest": polynomial_digest(poly),
    }


def polynomial_from_coefficient_table(
    coefficients: dict[tuple[int, int], tuple[int, int]],
) -> sp.Expr:
    return sp.expand(sum(
        Rational(numerator, denominator) * X_VAR**x_power * Y_VAR**y_power
        for (x_power, y_power), (numerator, denominator)
        in coefficients.items()
    ))


def real_amplitude_polynomials() -> tuple[sp.Expr, sp.Expr]:
    return (
        polynomial_from_coefficient_table(REAL_EXTERNAL_COEFFICIENTS),
        polynomial_from_coefficient_table(REAL_TARGET_COEFFICIENTS),
    )


def homogeneous_component(
    expression: sp.Expr,
    degree: int,
) -> sp.Expr:
    polynomial = sp.Poly(expression, X_VAR, Y_VAR, domain=sp.QQ)
    return sp.expand(sum(
        coefficient * X_VAR**monomial[0] * Y_VAR**monomial[1]
        for monomial, coefficient in polynomial.terms()
        if sum(monomial) == degree
    ))


def real_properness_record(
    external: sp.Expr,
    target: sp.Expr,
) -> dict[str, object]:
    target_discriminant = sp.factor(sp.discriminant(target, Y_VAR))
    leading_six = sp.factor(homogeneous_component(external, 6))
    leading_five_on_diagonal = sp.factor(
        homogeneous_component(external, 5).subs(Y_VAR, X_VAR)
    )
    expected_leading_six = (
        Rational(9, 6_553_600)
        * (X_VAR - Y_VAR) ** 2
        * (
            7753 * X_VAR**4
            - 8844 * X_VAR**3 * Y_VAR
            + 4486 * X_VAR**2 * Y_VAR**2
            - 8844 * X_VAR * Y_VAR**3
            + 7753 * Y_VAR**4
        )
    )
    if sp.expand(leading_six - expected_leading_six) != 0:
        raise AssertionError("Unexpected highest radial coefficient.")
    if leading_five_on_diagonal != Rational(1969, 896) * X_VAR**5:
        raise AssertionError("The diagonal next coefficient must be positive.")
    return {
        "targetDiscriminant": str(target_discriminant),
        "externalConstant": str(external.subs({X_VAR: 0, Y_VAR: 0})),
        "leadingDegreeSixFactor": str(leading_six),
        "palindromicQuarticReduction": (
            "7753*w^2-8844*w-11020, w=x/y+y/x>=2"
        ),
        "quarticValueAtTwo": 2304,
        "quarticDerivativeAtTwo": 22168,
        "degreeFiveOnDiagonal": str(leading_five_on_diagonal),
    }


def real_amplitude_audit() -> dict[str, object]:
    external, target = real_amplitude_polynomials()
    same_sign = boundary_record(external, target, X_VAR, Y_VAR)
    opposite_sign = boundary_record(external, target, Y_VAR, X_VAR)
    interior = real_interior_record(external, target)
    same_upper = same_sign["externalOverTarget"]["upperDecimal"]
    return {
        "sameSignBoundary": same_sign,
        "oppositeSignBoundary": opposite_sign,
        "interior": interior,
        "properness": real_properness_record(external, target),
        "globalMinimumLocation": "equal same-sign amplitudes",
        "minimumExternalOverTarget": same_upper,
        "maximumTargetFraction": 1 / (1 + same_upper),
    }


def isolated_real_amplitude_audit() -> dict[str, object]:
    """Run the large elimination basis in a short-lived child process."""

    completed = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).resolve()),
            "--real-worker",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def audit() -> dict[str, object]:
    real_result = isolated_real_amplitude_audit()
    by_frequency, pole_count = aggregate_signed_complex_limit()
    total_trigonometric = trigonometric_energy(
        complex_energy_monomials(by_frequency)
    )
    target_trigonometric = trigonometric_energy(
        complex_energy_monomials(
            by_frequency,
            {tree.NEXT_A_POSITIVE, tree.NEXT_A_NEGATIVE},
        )
    )
    total = invariant_polynomial(total_trigonometric)
    target = invariant_polynomial(target_trigonometric)
    external = sp.expand(total - target)
    table_external, table_target = real_amplitude_polynomials()
    if sp.expand(external.subs(H_VAR, 0) - table_external) != 0:
        raise AssertionError("The complex expansion disagrees with the real table.")
    if sp.expand(target.subs(H_VAR, 0) - table_target) != 0:
        raise AssertionError("The target expansion disagrees with the real table.")
    frequency_count = len(by_frequency)
    total_trigonometric_count = len(total_trigonometric)
    target_trigonometric_count = len(target_trigonometric)
    harmonics = sorted({key[2] for key in total_trigonometric})
    target_polynomial_string = str(sp.factor(target))
    total_summary = polynomial_summary(total)
    external_summary = polynomial_summary(external)

    # The tagged tree dictionary is much larger than the three invariant
    # polynomials. Release it before the exact certificate checks to keep the
    # certificate within an ordinary desktop memory budget.
    del by_frequency
    del total_trigonometric
    del target_trigonometric
    gc.collect()

    complex_certificate = bernstein_certificate(external, target)

    same_upper = real_result["minimumExternalOverTarget"]
    lower = float(COMPLEX_LOWER_BOUND)
    return {
        "convention": {
            "phase": "theta = arg(beta)-arg(delta)",
            "invariants": {
                "x": "|beta+delta|^2",
                "y": "|beta-delta|^2",
                "h": "4|beta|^2|delta|^2 sin(theta)^2",
            },
            "domain": "x>=0, y>=0, 0<=h<=xy",
            "energyNormalization": "E/sqrt(3)",
        },
        "complexExpansion": {
            "aggregatedFrequencyCount": frequency_count,
            "uncancelledLaurentPoleCount": pole_count,
            "totalTrigonometricTermCount": total_trigonometric_count,
            "targetTrigonometricTermCount": target_trigonometric_count,
            "phaseHarmonics": harmonics,
            "targetInvariantPolynomial": target_polynomial_string,
            "totalInvariant": total_summary,
            "externalInvariant": external_summary,
        },
        "realAmplitudes": real_result,
        "complexAmplitudes": {
            "bernsteinCertificate": complex_certificate,
            "infimumExternalOverTargetBracket": {
                "lower": lower,
                "upper": same_upper,
                "width": same_upper - lower,
            },
            "maximumTargetFractionBracket": {
                "lower": 1 / (1 + same_upper),
                "upper": 1 / (1 + lower),
            },
        },
    }


def validate(result: dict[str, object]) -> None:
    expansion = result["complexExpansion"]
    assert expansion["uncancelledLaurentPoleCount"] == 0
    assert expansion["totalTrigonometricTermCount"] == 48
    assert expansion["targetTrigonometricTermCount"] == 6
    assert expansion["phaseHarmonics"] == [0, 1, 2, 3]
    assert expansion["targetInvariantPolynomial"] == (
        "(8164683540*h + 2284553209*x**2 - 3819063498*x*y"
        " + 1823717025*y**2)/1254400"
    )

    real = result["realAmplitudes"]
    same = real["sameSignBoundary"]
    opposite = real["oppositeSignBoundary"]
    interior = real["interior"]
    assert same["stationarySignChanges"] == 1
    assert same["positiveRootCount"] == 1
    assert opposite["stationarySignChanges"] == 1
    assert opposite["positiveRootCount"] == 1
    assert abs(real["minimumExternalOverTarget"] - 45.7393489647) < 2e-9
    assert opposite["externalOverTarget"]["lowerDecimal"] > 59.7
    assert interior["eliminantDegree"] == 35
    assert interior["allRealRootCount"] == 11
    assert interior["positiveDirectionalRootCount"] == 11
    assert interior["positiveScaleCount"] == 1
    assert (
        interior["positivePoint"]["externalOverTarget"]["lowerDecimal"]
        > 434
    )
    assert real["properness"]["quarticValueAtTwo"] == 2304
    assert real["properness"]["degreeFiveOnDiagonal"] == "1969*x**5/896"

    complex_result = result["complexAmplitudes"]
    certificate = complex_result["bernsteinCertificate"]
    assert certificate["allLeafCoefficientsNonnegative"]
    assert certificate["lowerBound"] == "11434837/250000"
    bracket = complex_result["infimumExternalOverTargetBracket"]
    assert 0 < bracket["width"] < 1.0e-6


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--real-worker", action="store_true", help=argparse.SUPPRESS)
    arguments = parser.parse_args()
    if arguments.real_worker:
        print(json.dumps(real_amplitude_audit(), ensure_ascii=False))
        return
    result = audit()
    if arguments.check:
        validate(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
