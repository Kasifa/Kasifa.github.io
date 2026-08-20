#!/usr/bin/env python3
"""R0.67C-2 audit for the dominant sixth-order heat projection.

The exact 320-state four-bit transfer is lifted through all moments of total
degree six in the four free carrier coordinates.  A Taylor-jet lift centred at
c=(1/2,1/2,1/2,1/2) leaves a zero-sixth-jet remainder.  Its transfer scale is

    65536 / 16^7 = 1/4096.

The script then:

* isolates the dominant mass vector at the real root mu of the scaled quartic;
* solves the triangular moment equations through degree six;
* evaluates the centred sixth Taylor jet of the complete ten-shuffle heat
  observable at theta=2/15 and T=log(2)/2;
* aggregates signed affine branches at identical shifts before taking
  absolute values;
* proves a global seventh-derivative majorant by differentiating the heat
  exponential and integrating every absolute monomial over the five-simplex;
* combines guarded outward bounds into a strict negative interval.

The finite matrices and root isolation are exact.  The analytic sums are
performed in binary64 and admitted only through deliberately wider guard
bands recorded in the certificate.  The guard bands exceed the observed
cross-check discrepancies by many orders of magnitude.  This certifies one
fixed sixth-order heat projection in the periodic model; it is not a result
about all Picard orders or Navier--Stokes regularity.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import itertools
import json
import math
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

import sixth_order_affine_moment_audit as r067b
import sixth_order_cycle_audit as r067


DEGREE = 6
CENTER = 0.5
THETA = Fraction(2, 15)
TAYLOR_ORDER = 96
OBSERVABLE_STATE = r067.state_index(0, 0, 0)

# The raw computations are much tighter than these declared enclosures.
BASE_LOWER = -9.70e-7
BASE_UPPER = -9.48e-7
DEFECT_OBSERVABLE_UPPER = 5.0
DEFECT_WEIGHTED_UPPER = 1.0e-4
DERIVATIVE_UPPER = 6.0e-5


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    if not enabled:
        return
    fields = " ".join(f"{key}={value}" for key, value in details.items())
    print(
        f"[R0.67C-2 dominant heat +{time.perf_counter() - started:8.2f}s] "
        f"{stage}{(' ' + fields) if fields else ''}",
        file=sys.stderr,
        flush=True,
    )


def decimal_fraction(value: Fraction, digits: int = 18) -> str:
    return f"{float(value):.{digits}e}"


def fraction_record(value: Fraction) -> dict[str, str]:
    return {
        "numerator": str(value.numerator),
        "denominator": str(value.denominator),
        "decimal": decimal_fraction(value),
    }


def time_enclosure(terms: int = 160) -> tuple[Fraction, Fraction]:
    """Enclose log(2)/2=atanh(1/3) by positive rational terms."""
    x = Fraction(1, 3)
    lower = sum(
        (x ** (2 * index + 1)) / (2 * index + 1) for index in range(terms)
    )
    first = 2 * terms + 1
    remainder = x**first / first / (1 - x * x)
    return lower, lower + remainder


def polynomial_trim(values: list[Fraction]) -> list[Fraction]:
    output = values[:]
    while len(output) > 1 and output[-1] == 0:
        output.pop()
    return output


def polynomial_add(
    left: list[Fraction], right: list[Fraction]
) -> list[Fraction]:
    output = [Fraction(0)] * max(len(left), len(right))
    for index, value in enumerate(left):
        output[index] += value
    for index, value in enumerate(right):
        output[index] += value
    return polynomial_trim(output)


def polynomial_multiply(
    left: list[Fraction], right: list[Fraction]
) -> list[Fraction]:
    output = [Fraction(0)] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            output[left_index + right_index] += left_value * right_value
    return polynomial_trim(output)


def polynomial_divmod(
    dividend: list[Fraction], divisor: list[Fraction]
) -> tuple[list[Fraction], list[Fraction]]:
    remainder = polynomial_trim(dividend)
    divisor = polynomial_trim(divisor)
    quotient = [Fraction(0)] * max(1, len(remainder) - len(divisor) + 1)
    while len(remainder) >= len(divisor) and remainder != [Fraction(0)]:
        degree = len(remainder) - len(divisor)
        coefficient = remainder[-1] / divisor[-1]
        quotient[degree] += coefficient
        for index, value in enumerate(divisor):
            remainder[index + degree] -= coefficient * value
        remainder = polynomial_trim(remainder)
    return polynomial_trim(quotient), remainder


def polynomial_extended_gcd(
    left: list[Fraction], right: list[Fraction]
) -> tuple[list[Fraction], list[Fraction], list[Fraction]]:
    old_r, current_r = left, right
    old_s, current_s = [Fraction(1)], [Fraction(0)]
    old_t, current_t = [Fraction(0)], [Fraction(1)]
    while current_r != [Fraction(0)]:
        quotient, remainder = polynomial_divmod(old_r, current_r)
        old_r, current_r = current_r, remainder
        old_s, current_s = current_s, polynomial_add(
            old_s, [-value for value in polynomial_multiply(quotient, current_s)]
        )
        old_t, current_t = current_t, polynomial_add(
            old_t, [-value for value in polynomial_multiply(quotient, current_t)]
        )
    leading = old_r[-1]
    return (
        [value / leading for value in old_r],
        [value / leading for value in old_s],
        [value / leading for value in old_t],
    )


def sparse_matrix_vector_fraction(
    matrix: np.ndarray, vector: list[Fraction]
) -> list[Fraction]:
    output: list[Fraction] = []
    for row in matrix:
        output.append(
            sum(
                Fraction(int(row[column])) * vector[column]
                for column in np.flatnonzero(row)
            )
        )
    return output


def dominant_mass_vector(
    mass_matrix: np.ndarray, mu: float
) -> tuple[np.ndarray, dict[str, object]]:
    """Use an exact CRT projector, then isolate the chosen q4 root."""
    q4 = [Fraction(value) for value in reversed(r067.SCALED_QUARTIC)]
    q10 = [Fraction(value) for value in reversed(r067.DEGREE_TEN)]
    complement = polynomial_multiply(
        polynomial_multiply([Fraction(0), Fraction(1)], [-Fraction(256), Fraction(1)]),
        q10,
    )
    gcd, _q4_coefficient, complement_inverse = polynomial_extended_gcd(
        q4, complement
    )
    if gcd != [Fraction(1)]:
        raise AssertionError("q4 projector factors are not coprime")
    projector = polynomial_multiply(complement_inverse, complement)
    _quotient, remainder = polynomial_divmod(projector, q4)
    if remainder != [Fraction(1)]:
        raise AssertionError("invalid exact q4 CRT projector")

    initial = [Fraction(int(value)) for value in r067.initial_vector()]
    q4_component = [Fraction(0)] * r067.DIMENSION
    power = initial
    for coefficient in projector:
        if coefficient:
            for index in range(r067.DIMENSION):
                q4_component[index] += coefficient * power[index]
        power = sparse_matrix_vector_fraction(mass_matrix, power)

    u0 = np.array([float(value) for value in q4_component])
    u1 = mass_matrix.astype(float) @ u0
    u2 = mass_matrix.astype(float) @ u1
    u3 = mass_matrix.astype(float) @ u2
    c3, c2, c1 = -400.0, -30_720.0, 13_303_808.0
    denominator = 4 * mu**3 + 3 * c3 * mu**2 + 2 * c2 * mu + c1
    mass = (
        u3
        + (mu + c3) * u2
        + (mu**2 + c3 * mu + c2) * u1
        + (mu**3 + c3 * mu**2 + c2 * mu + c1) * u0
    ) / denominator

    power_iterate = r067.initial_vector().astype(float)
    for _ in range(220):
        power_iterate = mass_matrix.astype(float) @ power_iterate / mu
    return mass, {
        "projectorDegree": len(projector) - 1,
        "projectorCoefficientSha256": hashlib.sha256(
            json.dumps(
                [f"{value.numerator}/{value.denominator}" for value in projector],
                separators=(",", ":"),
            ).encode("ascii")
        ).hexdigest(),
        "projectorRemainderModuloQ4": [str(value) for value in remainder],
        "powerIterationMaximumDifference": float(np.max(np.abs(power_iterate - mass))),
        "eigenResidualMaximum": float(
            np.max(np.abs(mass_matrix.astype(float) @ mass - mu * mass))
        ),
    }


def multiindices(maximum_degree: int) -> list[tuple[int, int, int, int]]:
    return [
        alpha
        for degree in range(maximum_degree + 1)
        for alpha in itertools.product(range(degree + 1), repeat=4)
        if sum(alpha) == degree
    ]


def digit_edge_groups(bit: int) -> list[tuple[tuple[int, ...], np.ndarray, np.ndarray, np.ndarray]]:
    groups = []
    for epsilon in range(32):
        digits = tuple((epsilon >> shift) & 1 for shift in (4, 3, 2, 1, 0))
        rows: list[int] = []
        columns: list[int] = []
        signs: list[int] = []
        for target_state in (0, 1):
            for quintic_state in range(32):
                for parent_carry in r067.CARRIES:
                    child_carry = (
                        2 * parent_carry
                        + bit
                        - (sum(digits[:3]) - sum(digits[3:]))
                    )
                    if child_carry not in r067.CARRIES:
                        continue
                    rows.append(
                        r067.state_index(target_state, quintic_state, parent_carry)
                    )
                    columns.append(r067.state_index(bit, epsilon, child_carry))
                    parity = target_state * bit + (quintic_state & epsilon).bit_count()
                    signs.append(-1 if parity % 2 else 1)
        groups.append(
            (
                digits,
                np.array(rows, dtype=np.int64),
                np.array(columns, dtype=np.int64),
                np.array(signs, dtype=float),
            )
        )
    return groups


def translation_matrix(
    indices: list[tuple[int, int, int, int]], shift: tuple[int, int, int, int]
) -> np.ndarray:
    output = np.zeros((len(indices), len(indices)), dtype=float)
    for row, alpha in enumerate(indices):
        for column, beta in enumerate(indices):
            if all(beta[index] <= alpha[index] for index in range(4)):
                value = 1
                for index in range(4):
                    value *= (
                        math.comb(alpha[index], beta[index])
                        * shift[index] ** (alpha[index] - beta[index])
                    )
                output[row, column] = value
    return output


def raw_moment_cycle(
    moments: np.ndarray,
    indices: list[tuple[int, int, int, int]],
    edge_groups: dict[int, list[tuple[tuple[int, ...], np.ndarray, np.ndarray, np.ndarray]]],
) -> np.ndarray:
    output = moments
    for length, bit in zip((1, 2, 4, 8), r067.WORD):
        updated = np.zeros_like(output)
        for digits, rows, columns, signs in edge_groups[bit]:
            shift = tuple(length * value for value in digits[:4])
            translate = translation_matrix(indices, shift)
            updated[:, rows] += (translate @ output[:, columns]) * signs
        output = updated
    return output


def dominant_moments(
    mass_matrix: np.ndarray,
    mass: np.ndarray,
    mu: float,
    edge_groups: dict[int, list[tuple[tuple[int, ...], np.ndarray, np.ndarray, np.ndarray]]],
    report_progress: bool,
    started: float,
) -> tuple[list[tuple[int, int, int, int]], np.ndarray, dict[str, object]]:
    old_indices: list[tuple[int, int, int, int]] = []
    old_moments = np.empty((0, r067.DIMENSION))
    records: list[dict[str, object]] = []
    for degree in range(DEGREE + 1):
        indices = multiindices(degree)
        index_map = {alpha: index for index, alpha in enumerate(indices)}
        moments = np.zeros((len(indices), r067.DIMENSION), dtype=float)
        if degree == 0:
            moments[0] = mass
        else:
            for old_index, alpha in enumerate(old_indices):
                moments[index_map[alpha]] = old_moments[old_index]
            transported = raw_moment_cycle(moments, indices, edge_groups)
            current = [index for index, alpha in enumerate(indices) if sum(alpha) == degree]
            moments[current] = np.linalg.solve(
                (16**degree * mu) * np.eye(r067.DIMENSION) - mass_matrix.astype(float),
                transported[current].T,
            ).T
        records.append(
            {
                "degree": degree,
                "channels": math.comb(degree + 3, 3),
                "maximumAbsoluteMoment": float(
                    np.max(
                        np.abs(
                            moments[
                                [
                                    index
                                    for index, alpha in enumerate(indices)
                                    if sum(alpha) == degree
                                ]
                            ]
                        )
                    )
                ),
            }
        )
        progress(
            report_progress,
            started,
            "moment lift",
            degree=degree,
            channels=len(indices),
        )
        old_indices, old_moments = indices, moments

    degrees = np.array([sum(alpha) for alpha in old_indices])
    transported = raw_moment_cycle(old_moments, old_indices, edge_groups)
    residual = max(
        float(
            np.max(
                np.abs(
                    transported[index] / 16 ** int(degrees[index])
                    - mu * old_moments[index]
                )
            )
        )
        for index in range(len(old_indices))
    )
    return old_indices, old_moments, {
        "degreeRecords": records,
        "maximumFiniteEigenResidual": residual,
    }


def centered_moments(
    indices: list[tuple[int, int, int, int]], raw: np.ndarray
) -> np.ndarray:
    output = np.zeros_like(raw)
    for row, alpha in enumerate(indices):
        for column, beta in enumerate(indices):
            if all(beta[index] <= alpha[index] for index in range(4)):
                coefficient = 1.0
                for index in range(4):
                    coefficient *= (
                        math.comb(alpha[index], beta[index])
                        * (-CENTER) ** (alpha[index] - beta[index])
                    )
                output[row] += coefficient * raw[column]
    return output


def shuffle_words() -> list[tuple[int, ...]]:
    output = []
    for positive_positions in itertools.combinations(range(5), 3):
        positive = set(positive_positions)
        output.append(tuple(1 if index in positive else -1 for index in range(5)))
    return output


def heat_taylor_coefficients(
    maximum_degree: int, series_order: int, time_value: float
) -> tuple[list[tuple[int, int, int, int]], np.ndarray]:
    """Taylor coefficients in y=x-c; coefficients already include alpha!^-1."""
    indices = multiindices(maximum_degree)
    index_map = {alpha: index for index, alpha in enumerate(indices)}

    def constant(value: float = 0.0) -> np.ndarray:
        output = np.zeros(len(indices))
        output[0] = value
        return output

    def variable(coordinate: int) -> np.ndarray:
        output = constant(CENTER)
        alpha = [0, 0, 0, 0]
        alpha[coordinate] = 1
        output[index_map[tuple(alpha)]] = 1.0
        return output

    def add(*values: np.ndarray) -> np.ndarray:
        return sum(values, np.zeros(len(indices)))

    def multiply_sparse(left: np.ndarray, right: np.ndarray) -> np.ndarray:
        output = np.zeros(len(indices))
        for left_index in np.flatnonzero(left):
            for right_index in np.flatnonzero(right):
                alpha = tuple(
                    indices[left_index][coordinate]
                    + indices[right_index][coordinate]
                    for coordinate in range(4)
                )
                if sum(alpha) <= maximum_degree:
                    output[index_map[alpha]] += left[left_index] * right[right_index]
        return output

    def rate_maps(rate: np.ndarray) -> list[tuple[float, np.ndarray, np.ndarray]]:
        output = []
        for rate_index in np.flatnonzero(rate):
            beta = indices[rate_index]
            sources: list[int] = []
            targets: list[int] = []
            for source, alpha in enumerate(indices):
                target = tuple(
                    alpha[coordinate] + beta[coordinate] for coordinate in range(4)
                )
                if sum(target) <= maximum_degree:
                    sources.append(source)
                    targets.append(index_map[target])
            output.append(
                (
                    float(rate[rate_index]),
                    np.array(sources, dtype=np.int64),
                    np.array(targets, dtype=np.int64),
                )
            )
        return output

    def multiply_rate(
        value: np.ndarray, maps: list[tuple[float, np.ndarray, np.ndarray]]
    ) -> np.ndarray:
        output = np.zeros_like(value)
        for coefficient, sources, targets in maps:
            output[targets] += coefficient * value[sources]
        return output

    x = [variable(index) for index in range(4)]
    one = constant(1.0)
    theta = float(THETA)
    e = add(x[0], x[1], x[2], -x[3], constant(-theta))
    magnitudes = [add(one, x[index] / 4) for index in range(4)] + [
        add(one, e / 4)
    ]
    observable = constant()
    for word in shuffle_words():
        positives = iter(magnitudes[:3])
        negatives = iter(magnitudes[3:])
        carriers = [
            next(positives) if sign > 0 else -next(negatives) for sign in word
        ]
        current = constant(-(1 + theta / 4))
        suffix = sum(
            (multiply_sparse(value, value) for value in carriers), constant()
        )
        rates: list[np.ndarray] = []
        for carrier in carriers:
            rates.append(add(multiply_sparse(current, current), suffix))
            suffix = add(suffix, -multiply_sparse(carrier, carrier))
            current = add(current, carrier)
        homogeneous = [constant(1.0)] + [constant() for _ in range(series_order)]
        for rate in rates:
            maps = rate_maps(rate)
            for order in range(1, series_order + 1):
                homogeneous[order] += multiply_rate(homogeneous[order - 1], maps)
        for order, value in enumerate(homogeneous):
            observable += (
                (-1) ** order
                * time_value ** (order + 5)
                / math.factorial(order + 5)
                * value
            )
    return indices, observable


def positional_step(
    values: np.ndarray,
    bit: int,
    length: int,
    groups: list[tuple[tuple[int, ...], np.ndarray, np.ndarray, np.ndarray]],
) -> np.ndarray:
    width = values.shape[1]
    output = np.zeros(
        (
            r067.DIMENSION,
            width + length,
            width + length,
            width + length,
            width + length,
        ),
        dtype=float,
    )
    for digits, rows, columns, signs in groups:
        shift = [length * value for value in digits[:4]]
        slices = tuple(slice(value, value + width) for value in shift)
        output[(rows,) + slices] += values[columns] * signs.reshape((-1, 1, 1, 1, 1))
    return output


def defect_bounds(
    indices: list[tuple[int, int, int, int]],
    centered: np.ndarray,
    edge_groups: dict[int, list[tuple[tuple[int, ...], np.ndarray, np.ndarray, np.ndarray]]],
    report_progress: bool,
    started: float,
) -> tuple[np.ndarray, dict[str, object]]:
    grid = np.indices((16, 16, 16, 16), dtype=float).reshape(4, -1).T
    distance_l1 = np.abs((grid + CENTER) / 16 - CENTER).sum(axis=1)
    bounds = np.zeros(r067.DIMENSION)
    for channel, alpha in enumerate(indices):
        degree = sum(alpha)
        factorial = math.prod(math.factorial(value) for value in alpha)
        values = np.zeros((r067.DIMENSION, 1, 1, 1, 1), dtype=float)
        values[:, 0, 0, 0, 0] = centered[channel] / (factorial * 16**degree)
        for length, bit in zip((1, 2, 4, 8), r067.WORD):
            values = positional_step(values, bit, length, edge_groups[bit])
        remainder_degree = DEGREE + 1 - degree
        bounds += np.abs(values.reshape(r067.DIMENSION, -1)) @ (
            distance_l1**remainder_degree / math.factorial(remainder_degree)
        )
        if channel % 25 == 0 or channel + 1 == len(indices):
            progress(
                report_progress,
                started,
                "signed-shift defect",
                channel=f"{channel + 1}/{len(indices)}",
                observable=f"{bounds[OBSERVABLE_STATE]:.12g}",
            )
    weights = r067b.state_weights().astype(float)
    return bounds, {
        "observableRaw": float(bounds[OBSERVABLE_STATE]),
        "weightedMaximumRaw": float(np.max(bounds / weights)),
        "weightedMaximumState": int(np.argmax(bounds / weights)),
        "observableGuardedUpper": DEFECT_OBSERVABLE_UPPER,
        "weightedGuardedUpper": DEFECT_WEIGHTED_UPPER,
    }


Poly4 = dict[tuple[int, int, int, int], float]
Poly9 = dict[tuple[int, ...], float]


def poly4_add(*values: Poly4) -> Poly4:
    output: collections.defaultdict[tuple[int, int, int, int], float] = (
        collections.defaultdict(float)
    )
    for value in values:
        for alpha, coefficient in value.items():
            output[alpha] += coefficient
    return {alpha: coefficient for alpha, coefficient in output.items() if coefficient}


def poly4_scale(value: Poly4, scalar: float) -> Poly4:
    return {alpha: scalar * coefficient for alpha, coefficient in value.items()}


def poly4_multiply(left: Poly4, right: Poly4) -> Poly4:
    output: collections.defaultdict[tuple[int, int, int, int], float] = (
        collections.defaultdict(float)
    )
    for left_alpha, left_value in left.items():
        for right_alpha, right_value in right.items():
            output[
                tuple(
                    left_alpha[index] + right_alpha[index] for index in range(4)
                )
            ] += left_value * right_value
    return dict(output)


def poly4_linear(constant: float, coefficients: list[float]) -> Poly4:
    output: Poly4 = {(0, 0, 0, 0): constant}
    for index, coefficient in enumerate(coefficients):
        if coefficient:
            alpha = [0, 0, 0, 0]
            alpha[index] = 1
            output[tuple(alpha)] = coefficient
    return output


def poly9_derivative(value: Poly9, coordinate: int) -> Poly9:
    output: collections.defaultdict[tuple[int, ...], float] = collections.defaultdict(float)
    for alpha, coefficient in value.items():
        if alpha[coordinate]:
            beta = list(alpha)
            beta[coordinate] -= 1
            output[tuple(beta)] += coefficient * alpha[coordinate]
    return dict(output)


def poly9_multiply(left: Poly9, right: Poly9) -> Poly9:
    output: collections.defaultdict[tuple[int, ...], float] = collections.defaultdict(float)
    for left_alpha, left_value in left.items():
        for right_alpha, right_value in right.items():
            output[
                tuple(
                    left_alpha[index] + right_alpha[index] for index in range(9)
                )
            ] += left_value * right_value
    # Removing only roundoff dust is harmless relative to the 16% guard band.
    return {
        alpha: coefficient
        for alpha, coefficient in output.items()
        if abs(coefficient) > 1.0e-30
    }


def poly9_subtract(left: Poly9, right: Poly9) -> Poly9:
    output: collections.defaultdict[tuple[int, ...], float] = collections.defaultdict(float)
    output.update(left)
    for alpha, coefficient in right.items():
        output[alpha] -= coefficient
    return {
        alpha: coefficient
        for alpha, coefficient in output.items()
        if abs(coefficient) > 1.0e-30
    }


def simplex_absolute_integral(value: Poly9, time_upper: float) -> float:
    output = 0.0
    for alpha, coefficient in value.items():
        spatial_degree = sum(alpha[:4])
        time_alpha = alpha[4:]
        time_degree = sum(time_alpha)
        output += (
            abs(coefficient)
            * CENTER**spatial_degree
            * time_upper ** (time_degree + 5)
            * math.prod(math.factorial(exponent) for exponent in time_alpha)
            / math.factorial(time_degree + 5)
        )
    return output


def analytic_seventh_derivative_bound(
    time_upper: float, report_progress: bool, started: float
) -> tuple[float, dict[str, object]]:
    """Bound all seventh partials after integrating over the five-simplex."""
    theta = float(THETA)
    carrier_a = poly4_linear(1 + CENTER / 4, [0.25, 0, 0, 0])
    carrier_b = poly4_linear(1 + CENTER / 4, [0, 0.25, 0, 0])
    carrier_c = poly4_linear(1 + CENTER / 4, [0, 0, 0.25, 0])
    carrier_d = poly4_linear(1 + CENTER / 4, [0, 0, 0, 0.25])
    e_constant = CENTER + CENTER + CENTER - CENTER - theta
    carrier_e = poly4_linear(
        1 + e_constant / 4, [0.25, 0.25, 0.25, -0.25]
    )
    magnitudes = (carrier_a, carrier_b, carrier_c, carrier_d, carrier_e)
    target = poly4_linear(-(1 + theta / 4), [0, 0, 0, 0])
    seventh = [alpha for alpha in itertools.product(range(8), repeat=4) if sum(alpha) == 7]
    total = {alpha: 0.0 for alpha in seventh}
    records: list[dict[str, object]] = []
    zero9 = (0,) * 9

    for word_index, word in enumerate(shuffle_words()):
        positives = iter(magnitudes[:3])
        negatives = iter(magnitudes[3:])
        carriers = [
            next(positives) if sign > 0 else poly4_scale(next(negatives), -1)
            for sign in word
        ]
        current = target
        suffix = poly4_add(*(poly4_multiply(value, value) for value in carriers))
        rates: list[Poly4] = []
        for carrier in carriers:
            rates.append(poly4_add(poly4_multiply(current, current), suffix))
            suffix = poly4_add(
                suffix, poly4_scale(poly4_multiply(carrier, carrier), -1)
            )
            current = poly4_add(current, carrier)

        exponent: collections.defaultdict[tuple[int, ...], float] = collections.defaultdict(float)
        for time_index, rate in enumerate(rates):
            for alpha, coefficient in rate.items():
                lifted = list(alpha) + [0] * 5
                lifted[4 + time_index] = 1
                exponent[tuple(lifted)] += coefficient
        exponent_poly = dict(exponent)
        exponent_derivatives = [
            poly9_derivative(exponent_poly, coordinate) for coordinate in range(4)
        ]

        level: dict[tuple[int, int, int, int], Poly9] = {
            (0, 0, 0, 0): {zero9: 1.0}
        }
        for degree in range(1, 8):
            next_level: dict[tuple[int, int, int, int], Poly9] = {}
            for alpha in (
                value
                for value in itertools.product(range(degree + 1), repeat=4)
                if sum(value) == degree
            ):
                coordinate = next(index for index, value in enumerate(alpha) if value)
                predecessor = list(alpha)
                predecessor[coordinate] -= 1
                old = level[tuple(predecessor)]
                next_level[alpha] = poly9_subtract(
                    poly9_derivative(old, coordinate),
                    poly9_multiply(exponent_derivatives[coordinate], old),
                )
            level = next_level

        word_bounds = {
            alpha: simplex_absolute_integral(level[alpha], time_upper)
            for alpha in seventh
        }
        for alpha, value in word_bounds.items():
            total[alpha] += value
        records.append(
            {
                "word": list(word),
                "maximumTerms": max(len(level[alpha]) for alpha in seventh),
                "maximumPartialBound": max(word_bounds.values()),
            }
        )
        progress(
            report_progress,
            started,
            "analytic derivative majorant",
            shuffle=f"{word_index + 1}/10",
            maximum=f"{max(word_bounds.values()):.12e}",
        )

    maximum_alpha = max(total, key=total.get)
    return total[maximum_alpha], {
        "rawMaximum": total[maximum_alpha],
        "rawMaximumMultiindex": list(maximum_alpha),
        "guardedUpper": DERIVATIVE_UPPER,
        "perShuffle": records,
        "method": (
            "Differentiate exp(-sum_j rate_j tau_j) seven times; expand the "
            "result as a polynomial in centred space and five simplex times; "
            "use exp(-g)<=1 and integrate every absolute monomial exactly in form."
        ),
    }


def root_interval() -> tuple[Fraction, Fraction]:
    return (
        Fraction(402_425_429_345_624, 10**12),
        Fraction(4_024_254_293_456_256, 10**13),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-commit")
    parser.add_argument("--r067b-certificate", type=Path)
    parser.add_argument("--progress", action="store_true")
    arguments = parser.parse_args()
    started = time.perf_counter()

    lower_mu, upper_mu = root_interval()
    if not (
        r067.evaluate_polynomial(r067.SCALED_QUARTIC, lower_mu) < 0
        < r067.evaluate_polynomial(r067.SCALED_QUARTIC, upper_mu)
    ):
        raise AssertionError("dominant root bracket is invalid")
    mu = max(np.roots(r067.SCALED_QUARTIC).real)
    progress(arguments.progress, started, "constructing exact finite transfer")
    mass_matrix, _first_shifts = r067b.cycle_mass_and_shifts()
    edge_groups = {bit: digit_edge_groups(bit) for bit in (0, 1)}

    mass, mass_metadata = dominant_mass_vector(mass_matrix, mu)
    indices, raw_moments, moment_metadata = dominant_moments(
        mass_matrix,
        mass,
        mu,
        edge_groups,
        arguments.progress,
        started,
    )
    centered = centered_moments(indices, raw_moments)

    time_lower, time_upper = time_enclosure()
    time_midpoint = (float(time_lower) + float(time_upper)) / 2
    progress(arguments.progress, started, "evaluating centred heat jet")
    heat_indices, heat_coefficients = heat_taylor_coefficients(
        DEGREE, TAYLOR_ORDER, time_midpoint
    )
    if heat_indices != indices:
        raise AssertionError("moment and heat multiindex orders disagree")
    jet_base = float(
        sum(
            centered[index, OBSERVABLE_STATE] * heat_coefficients[index]
            for index in range(len(indices))
        )
    )
    _short_indices, short_coefficients = heat_taylor_coefficients(
        DEGREE, TAYLOR_ORDER - 16, time_midpoint
    )
    heat_order_difference = float(
        np.max(np.abs(heat_coefficients - short_coefficients))
    )

    progress(arguments.progress, started, "aggregating signed affine shifts")
    defect, defect_metadata = defect_bounds(
        indices, centered, edge_groups, arguments.progress, started
    )

    raw_derivative, derivative_metadata = analytic_seventh_derivative_bound(
        math.nextafter(float(time_upper), math.inf), arguments.progress, started
    )

    weights = r067b.state_weights().astype(float)
    contraction = Fraction(65_536, 16 ** (DEGREE + 1))
    resolvent_ratio = float(contraction) / float(lower_mu)
    resolvent_observable_upper = (
        DEFECT_OBSERVABLE_UPPER / float(lower_mu)
        + weights[OBSERVABLE_STATE]
        * DEFECT_WEIGHTED_UPPER
        / float(lower_mu)
        * resolvent_ratio
        / (1 - resolvent_ratio)
    )
    correction_upper = resolvent_observable_upper * DERIVATIVE_UPPER
    projection_lower = BASE_LOWER - correction_upper
    projection_upper = BASE_UPPER + correction_upper

    checks = {
        "dominantRootHasExactSignBracket": True,
        "exactQ4ProjectorMatchesPowerIteration": mass_metadata[
            "powerIterationMaximumDifference"
        ]
        < 1.0e-12,
        "massEigenResidualIsBelowTolerance": mass_metadata[
            "eigenResidualMaximum"
        ]
        < 1.0e-10,
        "allMomentsThroughDegreeSixArePresent": len(indices) == math.comb(10, 4),
        "finiteMomentEigenResidualIsBelowTolerance": moment_metadata[
            "maximumFiniteEigenResidual"
        ]
        < 1.0e-9,
        "heatTaylorOrdersAgree": heat_order_difference < 1.0e-15,
        "jetBaseLiesInGuardedInterval": BASE_LOWER < jet_base < BASE_UPPER,
        "signedShiftDefectLiesInsideGuard": defect_metadata[
            "observableRaw"
        ]
        < DEFECT_OBSERVABLE_UPPER,
        "weightedDefectLiesInsideGuard": defect_metadata[
            "weightedMaximumRaw"
        ]
        < DEFECT_WEIGHTED_UPPER,
        "zeroSixJetRemainderScaleIsOneOver4096": contraction == Fraction(1, 4096),
        "analyticDerivativeMajorantLiesInsideGuard": raw_derivative
        < DERIVATIVE_UPPER,
        "resolventObservableUpperIsBelowDeclaredThreshold": resolvent_observable_upper
        < 0.012_425,
        "correctionCannotReachJetBase": correction_upper < -BASE_UPPER,
        "completeDominantHeatProjectionIsStrictlyNegative": projection_upper < 0,
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    checks = {key: bool(value) for key, value in checks.items()}
    report = {
        "schemaVersion": "1.0",
        "status": "passed",
        "classification": (
            "guarded analytic-numerical sign certificate for the dominant "
            "complete sixth-order heat projection in the periodic 0100 model; "
            "not a certificate for all Picard orders or Navier--Stokes regularity"
        ),
        "checks": checks,
        "target": {
            "cycleWordLeastSignificantBitFirst": list(r067.WORD),
            "M_r": "16^r",
            "q_r": "2(16^r-1)/15",
            "theta_r": "q_r/M_r",
            "thetaLimit": "2/15",
            "heatTime": "log(2)/2",
            "observableState": OBSERVABLE_STATE,
        },
        "dominantRoot": {
            "lower": str(lower_mu),
            "upper": str(upper_mu),
            "display": f"{mu:.15f}",
            "quarticAtLower": str(
                r067.evaluate_polynomial(r067.SCALED_QUARTIC, lower_mu)
            ),
            "quarticAtUpper": str(
                r067.evaluate_polynomial(r067.SCALED_QUARTIC, upper_mu)
            ),
        },
        "finiteJet": {
            "degree": DEGREE,
            "spatialVariables": 4,
            "channelsPerState": len(indices),
            "totalDimension": len(indices) * r067.DIMENSION,
            "center": [CENTER] * 4,
            "massProjection": mass_metadata,
            "momentLift": moment_metadata,
            "rawJetBase": jet_base,
            "guardedJetBaseInterval": [BASE_LOWER, BASE_UPPER],
            "heatTaylorOrder": TAYLOR_ORDER,
            "heatTaylorOrderCrossCheckDifference": heat_order_difference,
        },
        "defect": defect_metadata,
        "analyticDerivativeBound": derivative_metadata,
        "resolvent": {
            "remainderTransferScale": fraction_record(contraction),
            "ratioToDominantRootUpper": resolvent_ratio,
            "observableUpper": resolvent_observable_upper,
            "heatCorrectionAbsoluteUpper": correction_upper,
        },
        "conclusion": {
            "dominantHeatProjectionLower": projection_lower,
            "dominantHeatProjectionUpper": projection_upper,
            "strictSign": "negative",
            "rawUnroundedReference": {
                "jetBase": jet_base,
                "defectResolventObservable": float(
                    np.linalg.solve(
                        mu * np.eye(r067.DIMENSION)
                        - r067.cycle_matrix(
                            [
                                r067.signed_digit_transfer(0, absolute=True),
                                r067.signed_digit_transfer(1, absolute=True),
                            ]
                        ).astype(float)
                        / 16 ** (DEGREE + 1),
                        defect,
                    )[OBSERVABLE_STATE]
                ),
                "analyticDerivativeMajorant": raw_derivative,
            },
        },
        "timeEnclosure": {
            "lower": fraction_record(time_lower),
            "upper": fraction_record(time_upper),
        },
        "guardBands": {
            "jetBase": [BASE_LOWER, BASE_UPPER],
            "defectObservableUpper": DEFECT_OBSERVABLE_UPPER,
            "defectWeightedUpper": DEFECT_WEIGHTED_UPPER,
            "seventhDerivativeUpper": DERIVATIVE_UPPER,
            "note": (
                "The declared bounds are deliberately wider than the binary64 "
                "values. They are the only values used in the final sign interval."
            ),
        },
        "limitations": [
            "The certificate concerns one fixed sixth-order coefficient and one periodic target family.",
            "It does not control the full sum over all Picard orders.",
            "The packet remains in a globally smooth invariant shear class.",
            "No statement is made about singularity formation or global regularity for general 3D data.",
        ],
        "provenance": {
            "sourceCommit": arguments.source_commit,
            "r067bCertificate": (
                str(arguments.r067b_certificate) if arguments.r067b_certificate else None
            ),
            "r067bCertificateSha256": (
                hashlib.sha256(arguments.r067b_certificate.read_bytes()).hexdigest()
                if arguments.r067b_certificate
                else None
            ),
        },
        "runtime": {
            "elapsedSeconds": time.perf_counter() - started,
            "python": sys.version.split()[0],
            "numpy": np.__version__,
        },
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    progress(
        arguments.progress,
        started,
        "complete",
        lower=f"{projection_lower:.12e}",
        upper=f"{projection_upper:.12e}",
        checks=len(checks),
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
