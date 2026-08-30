#!/usr/bin/env python3
"""Validated Chebyshev and Bernstein helpers for R0.73J.

The routines operate only on Arb/Acb balls.  They convert the tensor
Chebyshev interpolant to tensor Bernstein form, whose coefficient hull is a
rigorous range enclosure on a real parameter rectangle.
"""

from __future__ import annotations

import math
from typing import Sequence

from flint import acb, arb


def chebyshev_roots(count: int) -> list[arb]:
    if count < 1:
        raise ValueError("node count must be positive")
    return [
        ((2 * index + 1) * arb.pi() / (2 * count)).cos()
        for index in range(count)
    ]


def chebyshev_coefficients(values: Sequence[acb]) -> list[acb]:
    count = len(values)
    roots_angle = [
        (2 * index + 1) * arb.pi() / (2 * count)
        for index in range(count)
    ]
    result: list[acb] = []
    for order in range(count):
        total = sum(
            (value * (order * angle).cos()
             for value, angle in zip(values, roots_angle)),
            acb(0),
        )
        total *= arb(2) / count
        if order == 0:
            total /= 2
        result.append(total)
    return result


def tensor_chebyshev_coefficients(
    values: Sequence[Sequence[acb]],
) -> list[list[acb]]:
    d_count = len(values)
    if d_count == 0:
        raise ValueError("empty tensor grid")
    parameter_count = len(values[0])
    if parameter_count == 0 or any(len(row) != parameter_count for row in values):
        raise ValueError("ragged tensor grid")

    first = [
        chebyshev_coefficients([values[d_index][s_index]
                                for d_index in range(d_count)])
        for s_index in range(parameter_count)
    ]
    result = [[acb(0) for _ in range(parameter_count)]
              for _ in range(d_count)]
    for d_order in range(d_count):
        transformed = chebyshev_coefficients(
            [first[s_index][d_order] for s_index in range(parameter_count)]
        )
        result[d_order] = transformed
    return result


def chebyshev_evaluate(coefficients: Sequence[acb], value: arb) -> acb:
    if not coefficients:
        raise ValueError("empty Chebyshev polynomial")
    if len(coefficients) == 1:
        return coefficients[0]
    next_one = acb(0)
    next_two = acb(0)
    for order in range(len(coefficients) - 1, 0, -1):
        current = 2 * value * next_one - next_two + coefficients[order]
        next_two, next_one = next_one, current
    return value * next_one - next_two + coefficients[0]


def chebyshev_to_power(coefficients: Sequence[acb]) -> list[acb]:
    degree = len(coefficients) - 1
    basis: list[list[int]] = [[1]]
    if degree >= 1:
        basis.append([0, 1])
    for order in range(2, degree + 1):
        current = [0 for _ in range(order + 1)]
        for index, value in enumerate(basis[order - 1]):
            current[index + 1] += 2 * value
        for index, value in enumerate(basis[order - 2]):
            current[index] -= value
        basis.append(current)
    result = [acb(0) for _ in range(degree + 1)]
    for order, coefficient in enumerate(coefficients):
        for index, integer in enumerate(basis[order]):
            result[index] += integer * coefficient
    return result


def power_minus_one_one_to_bernstein(
    coefficients: Sequence[acb],
) -> list[acb]:
    """Map ``t=2u-1`` and convert power coefficients to Bernstein form."""
    degree = len(coefficients) - 1
    mapped = [acb(0) for _ in range(degree + 1)]
    for power, coefficient in enumerate(coefficients):
        for mapped_power in range(power + 1):
            mapped[mapped_power] += (
                coefficient
                * math.comb(power, mapped_power)
                * 2 ** mapped_power
                * (-1) ** (power - mapped_power)
            )
    result = [acb(0) for _ in range(degree + 1)]
    for bernstein_index in range(degree + 1):
        for power in range(bernstein_index + 1):
            result[bernstein_index] += (
                mapped[power]
                * math.comb(bernstein_index, power)
                / math.comb(degree, power)
            )
    return result


def chebyshev_to_bernstein(coefficients: Sequence[acb]) -> list[acb]:
    return power_minus_one_one_to_bernstein(
        chebyshev_to_power(coefficients)
    )


def tensor_chebyshev_to_bernstein(
    coefficients: Sequence[Sequence[acb]],
) -> list[list[acb]]:
    d_count = len(coefficients)
    if d_count == 0:
        raise ValueError("empty tensor coefficient array")
    s_count = len(coefficients[0])
    if any(len(row) != s_count for row in coefficients):
        raise ValueError("ragged tensor coefficient array")

    after_d = [[acb(0) for _ in range(s_count)] for _ in range(d_count)]
    for s_order in range(s_count):
        converted = chebyshev_to_bernstein(
            [coefficients[d_order][s_order] for d_order in range(d_count)]
        )
        for d_index, value in enumerate(converted):
            after_d[d_index][s_order] = value

    result = [[acb(0) for _ in range(s_count)] for _ in range(d_count)]
    for d_index in range(d_count):
        result[d_index] = chebyshev_to_bernstein(after_d[d_index])
    return result


def split_bernstein_half(coefficients: Sequence[acb]) -> tuple[list[acb], list[acb]]:
    degree = len(coefficients) - 1
    row = list(coefficients)
    left = [row[0]]
    right = [row[-1]]
    for _ in range(degree):
        row = [(row[index] + row[index + 1]) / 2
               for index in range(len(row) - 1)]
        left.append(row[0])
        right.append(row[-1])
    right.reverse()
    return left, right


def subdivide_bernstein(
    coefficients: Sequence[acb],
    depth: int,
) -> list[list[acb]]:
    pieces = [list(coefficients)]
    for _ in range(depth):
        refined: list[list[acb]] = []
        for piece in pieces:
            left, right = split_bernstein_half(piece)
            refined.extend((left, right))
        pieces = refined
    return pieces


def split_tensor_axis(
    coefficients: Sequence[Sequence[acb]],
    axis: int,
) -> tuple[list[list[acb]], list[list[acb]]]:
    d_count = len(coefficients)
    s_count = len(coefficients[0])
    if axis == 1:
        left = [[acb(0) for _ in range(s_count)] for _ in range(d_count)]
        right = [[acb(0) for _ in range(s_count)] for _ in range(d_count)]
        for d_index in range(d_count):
            left[d_index], right[d_index] = split_bernstein_half(
                coefficients[d_index]
            )
        return left, right
    if axis == 0:
        columns_left: list[list[acb]] = []
        columns_right: list[list[acb]] = []
        for s_index in range(s_count):
            column = [coefficients[d_index][s_index]
                      for d_index in range(d_count)]
            left_column, right_column = split_bernstein_half(column)
            columns_left.append(left_column)
            columns_right.append(right_column)
        left = [[columns_left[s_index][d_index]
                 for s_index in range(s_count)]
                for d_index in range(d_count)]
        right = [[columns_right[s_index][d_index]
                  for s_index in range(s_count)]
                 for d_index in range(d_count)]
        return left, right
    raise ValueError("axis must be zero or one")


def subdivide_tensor_bernstein(
    coefficients: Sequence[Sequence[acb]],
    d_depth: int,
    s_depth: int,
) -> list[tuple[int, int, list[list[acb]]]]:
    pieces: list[tuple[int, int, list[list[acb]]]] = [
        (0, 0, [list(row) for row in coefficients])
    ]
    for _ in range(d_depth):
        refined = []
        for d_index, s_index, piece in pieces:
            left, right = split_tensor_axis(piece, 0)
            refined.extend((
                (2 * d_index, s_index, left),
                (2 * d_index + 1, s_index, right),
            ))
        pieces = refined
    for _ in range(s_depth):
        refined = []
        for d_index, s_index, piece in pieces:
            left, right = split_tensor_axis(piece, 1)
            refined.extend((
                (d_index, 2 * s_index, left),
                (d_index, 2 * s_index + 1, right),
            ))
        pieces = refined
    return sorted(pieces, key=lambda item: (item[0], item[1]))


def complex_hull(values: Sequence[acb]) -> acb:
    if not values:
        raise ValueError("empty complex hull")
    real = values[0].real
    imag = values[0].imag
    for value in values[1:]:
        real = real.union(value.real)
        imag = imag.union(value.imag)
    return acb(real, imag)


def tensor_bernstein_hull(coefficients: Sequence[Sequence[acb]]) -> acb:
    return complex_hull([value for row in coefficients for value in row])


def inflate_by_modulus_error(value: acb, error: arb) -> acb:
    if error < 0:
        raise ValueError("negative interpolation error")
    return acb(
        arb(value.real.mid(), value.real.rad() + error),
        arb(value.imag.mid(), value.imag.rad() + error),
    )


def restrict_first_chebyshev_variable(
    coefficients: Sequence[Sequence[acb]],
    value: arb,
) -> list[acb]:
    s_count = len(coefficients[0])
    return [
        chebyshev_evaluate(
            [coefficients[d_order][s_order]
             for d_order in range(len(coefficients))],
            value,
        )
        for s_order in range(s_count)
    ]


def interpolation_error(majorant: arb, degree: int, rho: arb) -> arb:
    """Bernstein-ellipse Chebyshev-root interpolation error.

    The bound is ``4 M rho**(-n)/(rho-1)`` for a degree-``n`` interpolant
    at the ``n+1`` roots of ``T_(n+1)``.
    """
    if rho <= 1 or degree < 0 or majorant < 0:
        raise ValueError("invalid interpolation-bound input")
    return 4 * majorant * rho ** (-degree) / (rho - 1)


def chebyshev_lebesgue_bound(degree: int) -> arb:
    """Standard upper bound for first-kind Chebyshev roots."""
    if degree < 0:
        raise ValueError("negative degree")
    return 1 + 2 * arb(degree + 1).log() / arb.pi()


def real_d_evans_majorant(minimum_lambda_real: arb) -> dict[str, arb]:
    """Majorize ``E`` for real ``d`` and complexified contour parameter."""
    if minimum_lambda_real <= 0:
        raise ValueError("the complex contour ellipse reaches Re lambda <= 0")
    denominator_lower = 2 * minimum_lambda_real
    velocity_xx_upper = arb(3) / 2
    potential_upper = arb(1) / 4 + velocity_xx_upper / denominator_lower
    evans_upper = 2 + 2 * (
        2 * arb.pi() * potential_upper.sqrt()
    ).exp()
    return {
        "minimumLambdaReal": minimum_lambda_real,
        "denominatorLower": denominator_lower,
        "velocityXXUpper": velocity_xx_upper,
        "potentialUpper": potential_upper,
        "evansUpper": evans_upper,
    }


def complex_d_evans_majorant(
    minimum_lambda_real: arb,
    rho: arb,
) -> dict[str, arb]:
    """Majorize ``E`` on the complex ``d`` Bernstein ellipse."""
    if minimum_lambda_real <= 0 or rho <= 1:
        raise ValueError("invalid complex-d majorant input")
    maximum_d = arb(1) / 450
    real_semiaxis = (rho + 1 / rho) / 2
    imag_semiaxis = (rho - 1 / rho) / 2
    d_real_minimum = maximum_d * (1 - real_semiaxis) / 2
    d_real_maximum = maximum_d * (1 + real_semiaxis) / 2
    d_imag_maximum = maximum_d * imag_semiaxis / 2
    exponential_one = (-d_real_minimum).exp()
    exponential_four = (-4 * d_real_minimum).exp()
    imaginary_velocity_upper = (
        exponential_one * d_imag_maximum / 2
        + exponential_four * d_imag_maximum
    )
    denominator_lower = 2 * minimum_lambda_real - imaginary_velocity_upper
    if denominator_lower <= 0:
        raise ValueError("complex-d ellipse reaches a Rayleigh pole")
    velocity_xx_upper = exponential_one / 2 + exponential_four
    potential_upper = arb(1) / 4 + velocity_xx_upper / denominator_lower
    evans_upper = 2 + 2 * (
        2 * arb.pi() * potential_upper.sqrt()
    ).exp()
    return {
        "dRealMinimum": d_real_minimum,
        "dRealMaximum": d_real_maximum,
        "dImagMaximum": d_imag_maximum,
        "imaginaryVelocityUpper": imaginary_velocity_upper,
        "minimumLambdaReal": minimum_lambda_real,
        "denominatorLower": denominator_lower,
        "velocityXXUpper": velocity_xx_upper,
        "potentialUpper": potential_upper,
        "evansUpper": evans_upper,
    }
