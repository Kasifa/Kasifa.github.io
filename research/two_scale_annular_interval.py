#!/usr/bin/env python3
"""R0.69W rigorous interval certificate for the separation-four family.

The computation certifies the *declared* smooth cutoff, not the 48-point
floating quadrature used by the exploratory QMC programs.  The cutoff is the
convolution of the beta(3,3) survival profile on [1/20,19/20] with the
normalized standard C-infinity bump of radius 1/40.

Two exact reductions precede interval arithmetic.

1. A common SO(3) rotation is integrated by exact sphere moments up to degree
   six.  The five-dimensional angular integral becomes an integral in
   r, s, and t = n dot m.
2. The substitution d^2 = r^2+s^2-2rs t integrates t through five primitive
   moments of the nonnegative annular cutoff.  Only a two-dimensional radial
   interval sum remains.

Every transcendental bump evaluation is enclosed by Arb.  All later binary64
interval operations use explicit outward rounding with nextafter.  Raw bump
moments, cutoff values, annular primitives, and the final radial sum are all
one-sided Darboux enclosures.  No probabilistic error estimate enters.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import platform
import subprocess
import sys
import time
from typing import Iterable

from flint import arb, ctx
import numpy as np
import sympy as sp


TRANSITION_A = Fraction(1, 20)
TRANSITION_B = Fraction(19, 20)
TRANSITION_LENGTH = Fraction(9, 10)
MOLLIFIER_RADIUS = Fraction(1, 40)
ACTIVE_LOW = Fraction(41, 40)
ACTIVE_HIGH = Fraction(79, 40)
ACTIVE_SPAN = ACTIVE_HIGH - ACTIVE_LOW
EPSILON = Fraction(1, 4)
INNER_ACTIVE_LOW = EPSILON * ACTIVE_LOW
INNER_ACTIVE_HIGH = EPSILON * ACTIVE_HIGH
ANNULAR_POWERS = (-4, -2, 0, 2, 4)
NEGATIVE_INFINITY = -math.inf
POSITIVE_INFINITY = math.inf
BUMP_SECOND_ABSOLUTE_BOUND = Fraction(8)


def down(value):
    return np.nextafter(value, NEGATIVE_INFINITY)


def up(value):
    return np.nextafter(value, POSITIVE_INFINITY)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fraction_float_bounds(value: Fraction) -> tuple[float, float]:
    nearest = float(value)
    return math.nextafter(nearest, NEGATIVE_INFINITY), math.nextafter(
        nearest, POSITIVE_INFINITY
    )


def arb_float_bounds(value: arb) -> tuple[float, float]:
    midpoint, radius, exponent = value.mid_rad_10exp()
    midpoint = int(midpoint)
    radius = int(radius)
    exponent = int(exponent)
    if exponent >= 0:
        lower = Fraction(midpoint - radius) * 10**exponent
        upper = Fraction(midpoint + radius) * 10**exponent
    else:
        denominator = 10 ** (-exponent)
        lower = Fraction(midpoint - radius, denominator)
        upper = Fraction(midpoint + radius, denominator)
    return fraction_float_bounds(lower)[0], fraction_float_bounds(upper)[1]


def fraction_arb(value: Fraction) -> arb:
    return arb(value.numerator) / arb(value.denominator)


def bump_second_critical_audit() -> dict[str, object]:
    """Certify the critical structure and the global ``|bump''| < 8`` bound."""

    variable = sp.symbols("bump_second_t", real=True)
    critical = sp.Poly(
        2 * variable**3 - 14 * variable**2 + 21 * variable - 6,
        variable,
    )
    isolated = critical.intervals(eps=sp.Rational(1, 10**12))
    relevant = [
        (Fraction(interval[0]), Fraction(interval[1]))
        for interval, multiplicity in isolated
        if multiplicity == 1 and interval[1] > 1
    ]
    value_bounds = []
    for lower, upper in relevant:
        midpoint = (lower + upper) / 2
        radius = (upper - lower) / 2
        t_ball = arb(fraction_arb(midpoint), fraction_arb(radius))
        value = (-t_ball).exp() * (
            4 * t_ball**4 - 12 * t_ball**3 + 6 * t_ball**2
        )
        value_bounds.append(arb_float_bounds(value))
    passed = bool(
        len(relevant) == 2
        and relevant[0][0] > Fraction(159, 100)
        and relevant[0][1] < Fraction(160, 100)
        and relevant[1][0] > Fraction(503, 100)
        and relevant[1][1] < Fraction(504, 100)
        and relevant[0][0]
        > 1 / (1 - Fraction(3, 5) ** 2)
        and relevant[0][1]
        < 1 / (1 - Fraction(31, 50) ** 2)
        and relevant[1][0]
        > 1 / (1 - Fraction(89, 100) ** 2)
        and relevant[1][1]
        < 1 / (1 - Fraction(9, 10) ** 2)
        and all(
            max(abs(lower), abs(upper))
            < float(BUMP_SECOND_ABSOLUTE_BOUND)
            for lower, upper in value_bounds
        )
    )
    if not passed:
        raise RuntimeError("failed to certify the standard-bump second derivative")
    return {
        "criticalPolynomial": str(critical.as_expr()),
        "positiveCriticalIntervalsAboveOne": [
            [str(lower), str(upper)] for lower, upper in relevant
        ],
        "criticalValueIntervals": [list(bounds) for bounds in value_bounds],
        "absoluteBound": int(BUMP_SECOND_ABSOLUTE_BOUND),
        "passed": True,
    }


@dataclass(frozen=True)
class Interval:
    lower: np.ndarray
    upper: np.ndarray

    __array_priority__ = 1000

    def __init__(self, lower, upper=None):
        if upper is None:
            upper = lower
        object.__setattr__(self, "lower", np.asarray(lower, dtype=np.float64))
        object.__setattr__(self, "upper", np.asarray(upper, dtype=np.float64))
        if np.any(self.lower > self.upper):
            raise ValueError("invalid interval")

    @staticmethod
    def exact_integer(value: int) -> "Interval":
        return Interval(float(value))

    @staticmethod
    def from_fraction(value: Fraction) -> "Interval":
        return Interval(*fraction_float_bounds(value))

    @staticmethod
    def from_number(value) -> "Interval":
        if isinstance(value, Interval):
            return value
        if isinstance(value, (int, np.integer)):
            return Interval.exact_integer(int(value))
        if isinstance(value, Fraction):
            return Interval.from_fraction(value)
        if isinstance(value, np.ndarray):
            return Interval(down(value), up(value))
        nearest = float(value)
        return Interval(
            math.nextafter(nearest, NEGATIVE_INFINITY),
            math.nextafter(nearest, POSITIVE_INFINITY),
        )

    def __add__(self, other):
        other = Interval.from_number(other)
        return Interval(
            down(self.lower + other.lower),
            up(self.upper + other.upper),
        )

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.upper, -self.lower)

    def __sub__(self, other):
        return self + (-Interval.from_number(other))

    def __rsub__(self, other):
        return Interval.from_number(other) - self

    def __mul__(self, other):
        other = Interval.from_number(other)
        candidates = np.stack(
            np.broadcast_arrays(
                self.lower * other.lower,
                self.lower * other.upper,
                self.upper * other.lower,
                self.upper * other.upper,
            )
        )
        return Interval(down(np.min(candidates, axis=0)), up(np.max(candidates, axis=0)))

    __rmul__ = __mul__

    def reciprocal(self):
        if np.any((self.lower <= 0.0) & (self.upper >= 0.0)):
            raise ZeroDivisionError("interval contains zero")
        candidates = np.stack(
            np.broadcast_arrays(1.0 / self.lower, 1.0 / self.upper)
        )
        return Interval(down(np.min(candidates, axis=0)), up(np.max(candidates, axis=0)))

    def __truediv__(self, other):
        return self * Interval.from_number(other).reciprocal()

    def __rtruediv__(self, other):
        return Interval.from_number(other) / self

    def __pow__(self, exponent: int):
        if not isinstance(exponent, (int, np.integer)) or exponent < 0:
            raise ValueError("only nonnegative integer interval powers are supported")
        if exponent == 0:
            return Interval.exact_integer(1)
        result = Interval.exact_integer(1)
        base = self
        power = int(exponent)
        while power:
            if power & 1:
                result = result * base
            power >>= 1
            if power:
                base = base * base
        return result

    def sqrt(self) -> "Interval":
        if np.any(self.upper < 0.0):
            raise ValueError("cannot take the square root of a negative interval")
        lower = np.maximum(self.lower, 0.0)
        upper = np.maximum(self.upper, 0.0)
        return Interval(down(np.sqrt(lower)), up(np.sqrt(upper)))

    def intersect(self, lower: float, upper: float) -> "Interval":
        result = Interval(np.maximum(self.lower, lower), np.minimum(self.upper, upper))
        return result

    def width(self):
        return up(self.upper - self.lower)

    def midpoint(self):
        return 0.5 * (self.lower + self.upper)

    def scalar(self) -> list[float]:
        return [float(self.lower), float(self.upper)]


class PolyInterval:
    """Polynomial in amplitude with interval-valued coefficients."""

    __array_priority__ = 1000

    def __init__(self, coefficients: Iterable[Interval]):
        self.coefficients = tuple(Interval.from_number(value) for value in coefficients)

    @staticmethod
    def coerce(value) -> "PolyInterval":
        if isinstance(value, PolyInterval):
            return value
        return PolyInterval((Interval.from_number(value),))

    def __add__(self, other):
        other = PolyInterval.coerce(other)
        degree = max(len(self.coefficients), len(other.coefficients))
        zero = Interval.exact_integer(0)
        return PolyInterval(
            (
                self.coefficients[index] if index < len(self.coefficients) else zero
            )
            + (
                other.coefficients[index] if index < len(other.coefficients) else zero
            )
            for index in range(degree)
        )

    __radd__ = __add__

    def __neg__(self):
        return PolyInterval(-value for value in self.coefficients)

    def __sub__(self, other):
        return self + (-PolyInterval.coerce(other))

    def __rsub__(self, other):
        return PolyInterval.coerce(other) - self

    def __mul__(self, other):
        other = PolyInterval.coerce(other)
        zero = Interval.exact_integer(0)
        result = [zero for _ in range(len(self.coefficients) + len(other.coefficients) - 1)]
        for left_degree, left in enumerate(self.coefficients):
            for right_degree, right in enumerate(other.coefficients):
                degree = left_degree + right_degree
                result[degree] = result[degree] + left * right
        return PolyInterval(result)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = PolyInterval.coerce(other)
        if len(other.coefficients) != 1:
            raise ValueError("polynomial denominator must be amplitude-independent")
        return PolyInterval(value / other.coefficients[0] for value in self.coefficients)

    def __rtruediv__(self, other):
        numerator = PolyInterval.coerce(other)
        if len(self.coefficients) != 1:
            raise ValueError("polynomial denominator must be amplitude-independent")
        return PolyInterval(value / self.coefficients[0] for value in numerator.coefficients)

    def __pow__(self, exponent: int):
        if not isinstance(exponent, (int, np.integer)) or exponent < 0:
            raise ValueError("only nonnegative integer polynomial powers are supported")
        result = PolyInterval((Interval.exact_integer(1),))
        base = self
        power = int(exponent)
        while power:
            if power & 1:
                result = result * base
            power >>= 1
            if power:
                base = base * base
        return result


class CenteredInterval:
    """A rigorous centered form ``center + error``.

    It retains the cancellation of the box midpoint while enclosing all
    first- and higher-order deviations with ordinary outward-rounded
    intervals.  This is a centered interval extension, not a stochastic or
    floating-error heuristic.
    """

    __array_priority__ = 1001

    def __init__(self, center: Interval, error: Interval):
        self.center = Interval.from_number(center)
        self.error = Interval.from_number(error)

    @staticmethod
    def from_interval(value: Interval) -> "CenteredInterval":
        value = Interval.from_number(value)
        midpoint = value.midpoint()
        center = Interval.from_number(midpoint)
        return CenteredInterval(center, value - center)

    @staticmethod
    def coerce(value) -> "CenteredInterval":
        if isinstance(value, CenteredInterval):
            return value
        return CenteredInterval.from_interval(Interval.from_number(value))

    def range(self) -> Interval:
        return self.center + self.error

    def __add__(self, other):
        other = CenteredInterval.coerce(other)
        return CenteredInterval(
            self.center + other.center,
            self.error + other.error,
        )

    __radd__ = __add__

    def __neg__(self):
        return CenteredInterval(-self.center, -self.error)

    def __sub__(self, other):
        return self + (-CenteredInterval.coerce(other))

    def __rsub__(self, other):
        return CenteredInterval.coerce(other) - self

    def __mul__(self, other):
        other = CenteredInterval.coerce(other)
        return CenteredInterval(
            self.center * other.center,
            self.center * other.error
            + self.error * other.center
            + self.error * other.error,
        )

    __rmul__ = __mul__

    def reciprocal(self):
        full = self.range().reciprocal()
        center_reciprocal = self.center.reciprocal()
        return CenteredInterval(center_reciprocal, full - center_reciprocal)

    def __truediv__(self, other):
        return self * CenteredInterval.coerce(other).reciprocal()

    def __rtruediv__(self, other):
        return CenteredInterval.coerce(other) / self

    def __pow__(self, exponent: int):
        if not isinstance(exponent, (int, np.integer)) or exponent < 0:
            raise ValueError("only nonnegative integer centered powers are supported")
        full = self.range() ** int(exponent)
        center = self.center ** int(exponent)
        return CenteredInterval(center, full - center)


class CenteredPoly:
    """Polynomial in amplitude with centered-interval coefficients."""

    __array_priority__ = 1001

    def __init__(self, coefficients: Iterable[CenteredInterval]):
        self.coefficients = tuple(
            CenteredInterval.coerce(value) for value in coefficients
        )

    @staticmethod
    def coerce(value) -> "CenteredPoly":
        if isinstance(value, CenteredPoly):
            return value
        return CenteredPoly((CenteredInterval.coerce(value),))

    def __add__(self, other):
        other = CenteredPoly.coerce(other)
        degree = max(len(self.coefficients), len(other.coefficients))
        zero = CenteredInterval.coerce(0)
        return CenteredPoly(
            (
                self.coefficients[index]
                if index < len(self.coefficients)
                else zero
            )
            + (
                other.coefficients[index]
                if index < len(other.coefficients)
                else zero
            )
            for index in range(degree)
        )

    __radd__ = __add__

    def __neg__(self):
        return CenteredPoly(-value for value in self.coefficients)

    def __sub__(self, other):
        return self + (-CenteredPoly.coerce(other))

    def __rsub__(self, other):
        return CenteredPoly.coerce(other) - self

    def __mul__(self, other):
        other = CenteredPoly.coerce(other)
        zero = CenteredInterval.coerce(0)
        result = [zero for _ in range(len(self.coefficients) + len(other.coefficients) - 1)]
        for left_degree, left in enumerate(self.coefficients):
            for right_degree, right in enumerate(other.coefficients):
                degree = left_degree + right_degree
                result[degree] = result[degree] + left * right
        return CenteredPoly(result)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = CenteredPoly.coerce(other)
        if len(other.coefficients) != 1:
            raise ValueError("polynomial denominator must be amplitude-independent")
        return CenteredPoly(
            value / other.coefficients[0] for value in self.coefficients
        )

    def __rtruediv__(self, other):
        numerator = CenteredPoly.coerce(other)
        if len(self.coefficients) != 1:
            raise ValueError("polynomial denominator must be amplitude-independent")
        return CenteredPoly(
            value / self.coefficients[0] for value in numerator.coefficients
        )

    def __pow__(self, exponent: int):
        if not isinstance(exponent, (int, np.integer)) or exponent < 0:
            raise ValueError("only nonnegative integer polynomial powers are supported")
        if len(self.coefficients) == 1:
            return CenteredPoly((self.coefficients[0] ** int(exponent),))
        result = CenteredPoly((CenteredInterval.coerce(1),))
        base = self
        power = int(exponent)
        while power:
            if power & 1:
                result = result * base
            power >>= 1
            if power:
                base = base * base
        return result


class RawMomentTable:
    """Darboux enclosures for integral bump(u) u^k du, 0 <= k <= 5."""

    def __init__(self, power: int):
        self.power = power
        self.cells = 1 << power
        self.step = Fraction(2, self.cells)
        self.prefix: list[tuple[np.ndarray, np.ndarray]] = []
        self.cell_ranges: list[tuple[np.ndarray, np.ndarray]] = []
        self.critical_blocks: dict[str, list[list[int]]] = {}
        endpoint_intervals: list[list[tuple[float, float]]] = [
            [] for _ in range(6)
        ]

        for index in range(self.cells + 1):
            if index in (0, self.cells):
                for degree in range(6):
                    endpoint_intervals[degree].append((0.0, 0.0))
                continue
            u = arb(2 * index - self.cells) / arb(self.cells)
            bump = (-1 / (1 - u * u)).exp()
            for degree in range(6):
                endpoint_intervals[degree].append(
                    arb_float_bounds(bump * u**degree)
                )

        for degree in range(6):
            endpoint_lower = np.asarray(
                [value[0] for value in endpoint_intervals[degree]]
            )
            endpoint_upper = np.asarray(
                [value[1] for value in endpoint_intervals[degree]]
            )
            cell_lower = np.minimum(endpoint_lower[:-1], endpoint_lower[1:])
            cell_upper = np.maximum(endpoint_upper[:-1], endpoint_upper[1:])
            blocks: list[list[int]] = []
            critical_intervals: list[tuple[float, float]] = []
            if degree == 0:
                critical_intervals.append((0.0, 0.0))
            else:
                z = (arb(degree + 1) - arb(2 * degree + 1).sqrt()) / arb(degree)
                positive = z.sqrt()
                positive_bounds = arb_float_bounds(positive)
                critical_intervals.extend(
                    [
                        (-positive_bounds[1], -positive_bounds[0]),
                        positive_bounds,
                    ]
                )
            for critical_lower, critical_upper in critical_intervals:
                start = max(
                    0,
                    math.floor(
                        (critical_lower + 1.0) * self.cells / 2.0
                    )
                    - 2,
                )
                stop = min(
                    self.cells,
                    math.floor(
                        (critical_upper + 1.0) * self.cells / 2.0
                    )
                    + 3,
                )
                cell_lower[start:stop] = -1.0
                cell_upper[start:stop] = 1.0
                blocks.append([start, stop])
            self.critical_blocks[str(degree)] = blocks
            self.cell_ranges.append((cell_lower, cell_upper))

            prefix_lower = np.empty(self.cells + 1, dtype=np.float64)
            prefix_upper = np.empty(self.cells + 1, dtype=np.float64)
            prefix_lower[0] = 0.0
            prefix_upper[0] = 0.0
            step_float = float(self.step)
            for index in range(self.cells):
                contribution_lower = math.nextafter(
                    float(cell_lower[index]) * step_float,
                    NEGATIVE_INFINITY,
                )
                contribution_upper = math.nextafter(
                    float(cell_upper[index]) * step_float,
                    POSITIVE_INFINITY,
                )
                prefix_lower[index + 1] = math.nextafter(
                    prefix_lower[index] + contribution_lower,
                    NEGATIVE_INFINITY,
                )
                prefix_upper[index + 1] = math.nextafter(
                    prefix_upper[index] + contribution_upper,
                    POSITIVE_INFINITY,
                )
            self.prefix.append((prefix_lower, prefix_upper))
        self.normalization = self.moment(Fraction(-1), Fraction(1), 0)
        if float(self.normalization.lower) <= 0.0:
            raise RuntimeError("mollifier normalization did not stay positive")

    def _cell_segment(
        self, degree: int, cell: int, length: Fraction
    ) -> Interval:
        lower, upper = self.cell_ranges[degree]
        return Interval(float(lower[cell]), float(upper[cell])) * Interval.from_fraction(
            length
        )

    def moment(self, lower: Fraction, upper: Fraction, degree: int) -> Interval:
        lower = max(Fraction(-1), lower)
        upper = min(Fraction(1), upper)
        if lower >= upper:
            return Interval.exact_integer(0)
        lower_position = (lower + 1) * self.cells / 2
        upper_position = (upper + 1) * self.cells / 2
        first_grid = (
            lower_position.numerator + lower_position.denominator - 1
        ) // lower_position.denominator
        last_grid = upper_position.numerator // upper_position.denominator
        prefix_lower, prefix_upper = self.prefix[degree]
        if last_grid >= first_grid:
            result = Interval(
                math.nextafter(
                    float(prefix_lower[last_grid] - prefix_upper[first_grid]),
                    NEGATIVE_INFINITY,
                ),
                math.nextafter(
                    float(prefix_upper[last_grid] - prefix_lower[first_grid]),
                    POSITIVE_INFINITY,
                ),
            )
        else:
            result = Interval.exact_integer(0)
        first_grid_value = Fraction(-1) + first_grid * self.step
        if lower < first_grid_value:
            result = result + self._cell_segment(
                degree, first_grid - 1, first_grid_value - lower
            )
        last_grid_value = Fraction(-1) + last_grid * self.step
        if last_grid_value < upper:
            result = result + self._cell_segment(
                degree, last_grid, upper - last_grid_value
            )
        return result


def compose_linear(
    coefficients: list[Fraction], constant: Fraction, slope: Fraction
) -> list[Fraction]:
    result = [Fraction(0) for _ in coefficients]
    for degree, coefficient in enumerate(coefficients):
        for power in range(degree + 1):
            result[power] += (
                coefficient
                * math.comb(degree, power)
                * constant ** (degree - power)
                * (-slope) ** power
            )
    return result


SURVIVAL_COEFFICIENTS = [
    Fraction(1),
    Fraction(0),
    Fraction(0),
    Fraction(-10),
    Fraction(15),
    Fraction(-6),
]
DENSITY_COEFFICIENTS = [
    Fraction(0),
    Fraction(0),
    Fraction(30) / TRANSITION_LENGTH,
    Fraction(-60) / TRANSITION_LENGTH,
    Fraction(30) / TRANSITION_LENGTH,
]
DENSITY_DERIVATIVE_COEFFICIENTS = [
    Fraction(0),
    Fraction(60) / TRANSITION_LENGTH**2,
    Fraction(-180) / TRANSITION_LENGTH**2,
    Fraction(120) / TRANSITION_LENGTH**2,
]


def polynomial_derivative(coefficients: list[Fraction]) -> list[Fraction]:
    if len(coefficients) <= 1:
        return [Fraction(0)]
    return [
        Fraction(degree) * coefficients[degree]
        for degree in range(1, len(coefficients))
    ]


SURVIVAL_DERIVATIVES: list[list[Fraction]] = [SURVIVAL_COEFFICIENTS]
for derivative_order in range(1, 7):
    differentiated = polynomial_derivative(SURVIVAL_DERIVATIVES[-1])
    SURVIVAL_DERIVATIVES.append(
        [coefficient / TRANSITION_LENGTH for coefficient in differentiated]
    )


def coefficient_absolute_bound(coefficients: list[Fraction]) -> Fraction:
    return sum((abs(value) for value in coefficients), Fraction(0))


DERIVATIVE_GLOBAL_BOUNDS = [
    Fraction(1),
    Fraction(25, 12),
    Fraction(1500, 81),
    Fraction(60000, 729),
    Fraction(360) / TRANSITION_LENGTH**4,
    Fraction(720) / TRANSITION_LENGTH**5,
]


class CutoffCertificate:
    def __init__(self, raw_moments: RawMomentTable, cells: int):
        self.raw_moments = raw_moments
        self.cells = cells
        normalization_lower = float(raw_moments.normalization.lower)
        bump_maximum = math.exp(-1.0)
        rho_maximum = bump_maximum / float(MOLLIFIER_RADIUS) / normalization_lower
        rho_prime_maximum = (
            1.0
            / float(MOLLIFIER_RADIUS) ** 2
            / normalization_lower
        )
        rho_second_maximum = (
            float(BUMP_SECOND_ABSOLUTE_BOUND)
            / float(MOLLIFIER_RADIUS) ** 3
            / normalization_lower
        )
        self.derivative_bounds = list(DERIVATIVE_GLOBAL_BOUNDS)
        self.derivative_bounds[4] = (
            float(Fraction(360) / TRANSITION_LENGTH**4)
            + float(Fraction(120) / TRANSITION_LENGTH**3) * rho_maximum
        )
        self.derivative_bounds[5] = (
            float(Fraction(720) / TRANSITION_LENGTH**5)
            + float(Fraction(720) / TRANSITION_LENGTH**4) * rho_maximum
            + float(Fraction(120) / TRANSITION_LENGTH**3)
            * rho_prime_maximum
        )
        self.derivative_bounds.append(
            float(Fraction(1440) / TRANSITION_LENGTH**5) * rho_maximum
            + float(Fraction(720) / TRANSITION_LENGTH**4)
            * rho_prime_maximum
            + float(Fraction(120) / TRANSITION_LENGTH**3)
            * rho_second_maximum
        )
        self.nodes = [
            ACTIVE_LOW + ACTIVE_SPAN * Fraction(index, cells)
            for index in range(cells + 1)
        ]
        values = [self.point(node) for node in self.nodes]
        self.q_lower = np.asarray([float(value[0].lower) for value in values])
        self.q_upper = np.asarray([float(value[0].upper) for value in values])
        self.q_lower[0] = 1.0
        self.q_upper[0] = 1.0
        self.q_lower[-1] = 0.0
        self.q_upper[-1] = 0.0
        self.profiles = [
            self.profile_interval(self.nodes[index], self.nodes[index + 1])
            for index in range(cells)
        ]
        self.derivative_cell_ranges: list[tuple[np.ndarray, np.ndarray]] = []
        self.derivative_range_lower: list[np.ndarray] = []
        self.derivative_range_upper: list[np.ndarray] = []
        for order in range(5):
            cell_values = [
                self.derivative_interval(
                    self.nodes[index], self.nodes[index + 1], order
                )
                for index in range(cells)
            ]
            lower = np.asarray([float(value.lower) for value in cell_values])
            upper = np.asarray([float(value.upper) for value in cell_values])
            self.derivative_cell_ranges.append((lower, upper))
            lower_table = np.empty((cells, cells), dtype=np.float64)
            upper_table = np.empty((cells, cells), dtype=np.float64)
            for start in range(cells):
                lower_table[start, start:] = np.minimum.accumulate(lower[start:])
                upper_table[start, start:] = np.maximum.accumulate(upper[start:])
            self.derivative_range_lower.append(lower_table)
            self.derivative_range_upper.append(upper_table)

    def _linear_combination(
        self,
        coefficients: list[Fraction],
        lower: Fraction,
        upper: Fraction,
    ) -> Interval:
        total = Interval.exact_integer(0)
        for degree, coefficient in enumerate(coefficients):
            total = total + Interval.from_fraction(coefficient) * self.raw_moments.moment(
                lower, upper, degree
            )
        return total

    def point_derivatives(
        self, radius: Fraction, maximum_order: int = 5
    ) -> tuple[Interval, ...]:
        if radius <= ACTIVE_LOW:
            return tuple(
                Interval.exact_integer(1 if order == 0 else 0)
                for order in range(maximum_order + 1)
            )
        if radius >= ACTIVE_HIGH:
            return tuple(
                Interval.exact_integer(0) for _ in range(maximum_order + 1)
            )
        active_lower = (radius - 1 - TRANSITION_B) / MOLLIFIER_RADIUS
        active_upper = (radius - 1 - TRANSITION_A) / MOLLIFIER_RADIUS
        lower = max(Fraction(-1), active_lower)
        upper = min(Fraction(1), active_upper)
        constant = (radius - 1 - TRANSITION_A) / TRANSITION_LENGTH
        slope = MOLLIFIER_RADIUS / TRANSITION_LENGTH

        result: list[Interval] = []
        for order in range(maximum_order + 1):
            numerator = Interval.exact_integer(0)
            if order == 0 and active_upper < 1:
                numerator = numerator + self.raw_moments.moment(
                    max(Fraction(-1), active_upper), Fraction(1), 0
                )
            if lower < upper:
                numerator = numerator + self._linear_combination(
                    compose_linear(
                        SURVIVAL_DERIVATIVES[order], constant, slope
                    ),
                    lower,
                    upper,
                )
            enclosed = numerator / self.raw_moments.normalization
            if order in (4, 5, 6):
                lower_boundary = Fraction(1) + TRANSITION_A
                upper_boundary = Fraction(1) + TRANSITION_B
                boundary_value = Interval.exact_integer(0)
                for boundary, jump_third, jump_fourth in (
                    (
                        lower_boundary,
                        -Fraction(60) / TRANSITION_LENGTH**3,
                        Fraction(360) / TRANSITION_LENGTH**4,
                    ),
                    (
                        upper_boundary,
                        Fraction(60) / TRANSITION_LENGTH**3,
                        Fraction(360) / TRANSITION_LENGTH**4,
                    ),
                ):
                    coordinate = (radius - boundary) / MOLLIFIER_RADIUS
                    if not (Fraction(-1) < coordinate < Fraction(1)):
                        continue
                    u = arb(coordinate.numerator) / arb(coordinate.denominator)
                    bump = (-1 / (1 - u * u)).exp()
                    rho_interval = Interval(*arb_float_bounds(bump)) / (
                        Interval.from_fraction(MOLLIFIER_RADIUS)
                        * self.raw_moments.normalization
                    )
                    if order == 4:
                        boundary_value = boundary_value + Interval.from_fraction(
                            jump_third
                        ) * rho_interval
                    elif order == 5:
                        bump_prime = bump * (-2 * u) / (1 - u * u) ** 2
                        rho_prime_interval = Interval(
                            *arb_float_bounds(bump_prime)
                        ) / (
                            Interval.from_fraction(MOLLIFIER_RADIUS) ** 2
                            * self.raw_moments.normalization
                        )
                        boundary_value = (
                            boundary_value
                            + Interval.from_fraction(jump_fourth) * rho_interval
                            + Interval.from_fraction(jump_third)
                            * rho_prime_interval
                        )
                    else:
                        bump_log_prime = (-2 * u) / (1 - u * u) ** 2
                        bump_log_second = (
                            -2 / (1 - u * u) ** 2
                            - 8 * u * u / (1 - u * u) ** 3
                        )
                        bump_prime = bump * bump_log_prime
                        bump_second = bump * (
                            bump_log_prime * bump_log_prime
                            + bump_log_second
                        )
                        rho_prime_interval = Interval(
                            *arb_float_bounds(bump_prime)
                        ) / (
                            Interval.from_fraction(MOLLIFIER_RADIUS) ** 2
                            * self.raw_moments.normalization
                        )
                        rho_second_interval = Interval(
                            *arb_float_bounds(bump_second)
                        ) / (
                            Interval.from_fraction(MOLLIFIER_RADIUS) ** 3
                            * self.raw_moments.normalization
                        )
                        jump_fifth = (
                            -Fraction(720) / TRANSITION_LENGTH**5
                            if boundary == lower_boundary
                            else Fraction(720) / TRANSITION_LENGTH**5
                        )
                        boundary_value = (
                            boundary_value
                            + Interval.from_fraction(jump_fifth) * rho_interval
                            + Interval.from_fraction(jump_fourth)
                            * rho_prime_interval
                            + Interval.from_fraction(jump_third)
                            * rho_second_interval
                        )
                enclosed = enclosed + boundary_value
            if order == 0:
                enclosed = enclosed.intersect(0.0, 1.0)
            else:
                bound = float(self.derivative_bounds[order])
                enclosed = enclosed.intersect(-bound, bound)
            result.append(enclosed)
        return tuple(result)

    def point(self, radius: Fraction) -> tuple[Interval, Interval, Interval]:
        values = self.point_derivatives(radius, 2)
        return values[0], values[1], values[2]

    def _bump_endpoint(self, coordinate: Fraction) -> tuple[Interval, Interval]:
        if not (Fraction(-1) < coordinate < Fraction(1)):
            zero = Interval.exact_integer(0)
            return zero, zero
        u = arb(coordinate.numerator) / arb(coordinate.denominator)
        bump = (-1 / (1 - u * u)).exp()
        bump_prime = bump * (-2 * u) / (1 - u * u) ** 2
        return Interval(*arb_float_bounds(bump)), Interval(
            *arb_float_bounds(bump_prime)
        )

    def _bump_ranges(
        self, lower: Fraction, upper: Fraction
    ) -> tuple[Interval, Interval]:
        clipped_lower = max(Fraction(-1), lower)
        clipped_upper = min(Fraction(1), upper)
        if clipped_lower >= clipped_upper:
            zero = Interval.exact_integer(0)
            return zero, zero
        bump_left, derivative_left = self._bump_endpoint(clipped_lower)
        bump_right, derivative_right = self._bump_endpoint(clipped_upper)
        bump_lower = min(float(bump_left.lower), float(bump_right.lower))
        bump_upper = max(float(bump_left.upper), float(bump_right.upper))
        derivative_lower = min(
            float(derivative_left.lower), float(derivative_right.lower)
        )
        derivative_upper = max(
            float(derivative_left.upper), float(derivative_right.upper)
        )
        if lower < -1 or upper > 1:
            bump_lower = min(bump_lower, 0.0)
            derivative_lower = min(derivative_lower, 0.0)
            derivative_upper = max(derivative_upper, 0.0)
        if clipped_lower <= 0 <= clipped_upper:
            bump_at_zero = Interval(*arb_float_bounds((-arb(1)).exp()))
            bump_upper = max(bump_upper, float(bump_at_zero.upper))
            derivative_lower = min(derivative_lower, 0.0)
            derivative_upper = max(derivative_upper, 0.0)
        # The only nonzero critical points of bump' lie in these rational
        # guard blocks.  A global unit bound is inserted whenever a query
        # intersects a block; outside them endpoint monotonicity applies.
        if clipped_lower < Fraction(-3, 4) and clipped_upper > Fraction(-77, 100):
            derivative_upper = max(derivative_upper, 1.0)
        if clipped_lower < Fraction(77, 100) and clipped_upper > Fraction(3, 4):
            derivative_lower = min(derivative_lower, -1.0)
        return Interval(bump_lower, bump_upper), Interval(
            derivative_lower, derivative_upper
        )

    def _bump_second_range(
        self, lower: Fraction, upper: Fraction
    ) -> Interval:
        """Enclose the second bump derivative using its certified extrema."""

        if upper <= -1 or lower >= 1:
            return Interval.exact_integer(0)
        clipped_lower = max(Fraction(-1), lower)
        clipped_upper = min(Fraction(1), upper)

        def endpoint(coordinate: Fraction) -> Interval:
            if not (Fraction(-1) < coordinate < Fraction(1)):
                return Interval.exact_integer(0)
            u = fraction_arb(coordinate)
            bump = (-1 / (1 - u * u)).exp()
            log_first = (-2 * u) / (1 - u * u) ** 2
            log_second = (
                -2 / (1 - u * u) ** 2
                - 8 * u * u / (1 - u * u) ** 3
            )
            return Interval(
                *arb_float_bounds(
                    bump * (log_first * log_first + log_second)
                )
            )

        left = endpoint(clipped_lower)
        right = endpoint(clipped_upper)
        result_lower = min(float(left.lower), float(right.lower))
        result_upper = max(float(left.upper), float(right.upper))
        if lower < -1 or upper > 1:
            result_lower = min(result_lower, 0.0)
            result_upper = max(result_upper, 0.0)
        if clipped_lower <= 0 <= clipped_upper:
            result_lower = min(result_lower, -1.0)
        # The exact Sturm audit leaves only the guarded critical pairs
        # |u| in (0.60, 0.62) and |u| in (0.89, 0.90).
        for guard_lower, guard_upper in (
            (Fraction(3, 5), Fraction(31, 50)),
            (Fraction(-31, 50), Fraction(-3, 5)),
        ):
            if clipped_lower < guard_upper and clipped_upper > guard_lower:
                result_lower = min(result_lower, -2.0)
        for guard_lower, guard_upper in (
            (Fraction(89, 100), Fraction(9, 10)),
            (Fraction(-9, 10), Fraction(-89, 100)),
        ):
            if clipped_lower < guard_upper and clipped_upper > guard_lower:
                result_upper = max(
                    result_upper, float(BUMP_SECOND_ABSOLUTE_BOUND)
                )
        return Interval(result_lower, result_upper)

    def _normalized_bump_mass(
        self, lower: Fraction, upper: Fraction
    ) -> Interval:
        """Enclose normalized bump mass on a fixed coordinate interval."""

        clipped_lower = max(Fraction(-1), lower)
        clipped_upper = min(Fraction(1), upper)
        if clipped_lower >= clipped_upper:
            return Interval.exact_integer(0)
        if clipped_lower == -1 and clipped_upper == 1:
            return Interval.exact_integer(1)
        return (
            self.raw_moments.moment(
                clipped_lower, clipped_upper, 0
            )
            / self.raw_moments.normalization
        ).intersect(0.0, 1.0)

    def _interior_mass_range(
        self, lower_radius: Fraction, upper_radius: Fraction
    ) -> Interval:
        """Enclose the mollifier mass seeing the open beta transition.

        For a fixed radius ``r``, the contributing bump coordinates form
        ``[(r-b)/rho, (r-a)/rho]``.  As ``r`` ranges over a radial cell, the
        intersection of these intervals supplies a rigorous lower mass and
        their union supplies a rigorous upper mass.  This local enclosure is
        crucial for the fifth derivative: its interior beta contribution is
        a constant times precisely this mass.
        """

        lower_boundary = Fraction(1) + TRANSITION_A
        upper_boundary = Fraction(1) + TRANSITION_B
        guaranteed = self._normalized_bump_mass(
            (upper_radius - upper_boundary) / MOLLIFIER_RADIUS,
            (lower_radius - lower_boundary) / MOLLIFIER_RADIUS,
        )
        possible = self._normalized_bump_mass(
            (lower_radius - upper_boundary) / MOLLIFIER_RADIUS,
            (upper_radius - lower_boundary) / MOLLIFIER_RADIUS,
        )
        return Interval(
            max(0.0, float(guaranteed.lower)),
            min(1.0, float(possible.upper)),
        )

    def high_derivative_range(
        self, lower_radius: Fraction, upper_radius: Fraction, order: int
    ) -> Interval:
        if order not in (4, 5, 6):
            raise ValueError(
                "direct high-derivative range only supports orders 4, 5, and 6"
            )
        if order == 4:
            midpoint = (lower_radius + upper_radius) / 2
            half_width = (upper_radius - lower_radius) / 2
            midpoint_value = self.point_derivatives(midpoint, 4)[4]
            fifth = self.high_derivative_range(
                lower_radius, upper_radius, 5
            )
            absolute_fifth = max(
                abs(float(fifth.lower)), abs(float(fifth.upper))
            )
            lipschitz = Interval.from_fraction(
                Fraction.from_float(absolute_fifth) * half_width
            )
            bound = float(self.derivative_bounds[4])
            return (
                midpoint_value
                + Interval(-float(lipschitz.upper), float(lipschitz.upper))
            ).intersect(-bound, bound)
        elif order == 5:
            result = (
                Interval.from_fraction(SURVIVAL_DERIVATIVES[5][0])
                * self._interior_mass_range(
                    lower_radius, upper_radius
                )
            )
        else:
            result = Interval.exact_integer(0)
        for boundary, jump_third, jump_fourth in (
            (
                Fraction(1) + TRANSITION_A,
                -Fraction(60) / TRANSITION_LENGTH**3,
                Fraction(360) / TRANSITION_LENGTH**4,
            ),
            (
                Fraction(1) + TRANSITION_B,
                Fraction(60) / TRANSITION_LENGTH**3,
                Fraction(360) / TRANSITION_LENGTH**4,
            ),
        ):
            coordinate_lower = (lower_radius - boundary) / MOLLIFIER_RADIUS
            coordinate_upper = (upper_radius - boundary) / MOLLIFIER_RADIUS
            bump, bump_prime = self._bump_ranges(
                coordinate_lower, coordinate_upper
            )
            rho = bump / (
                Interval.from_fraction(MOLLIFIER_RADIUS)
                * self.raw_moments.normalization
            )
            if order == 4:
                result = result + Interval.from_fraction(jump_third) * rho
            elif order == 5:
                rho_prime = bump_prime / (
                    Interval.from_fraction(MOLLIFIER_RADIUS) ** 2
                    * self.raw_moments.normalization
                )
                result = (
                    result
                    + Interval.from_fraction(jump_fourth) * rho
                    + Interval.from_fraction(jump_third) * rho_prime
                )
            else:
                rho_prime = bump_prime / (
                    Interval.from_fraction(MOLLIFIER_RADIUS) ** 2
                    * self.raw_moments.normalization
                )
                rho_second = self._bump_second_range(
                    coordinate_lower, coordinate_upper
                ) / (
                    Interval.from_fraction(MOLLIFIER_RADIUS) ** 3
                    * self.raw_moments.normalization
                )
                jump_fifth = (
                    -Fraction(720) / TRANSITION_LENGTH**5
                    if boundary == Fraction(1) + TRANSITION_A
                    else Fraction(720) / TRANSITION_LENGTH**5
                )
                result = (
                    result
                    + Interval.from_fraction(jump_fifth) * rho
                    + Interval.from_fraction(jump_fourth) * rho_prime
                    + Interval.from_fraction(jump_third) * rho_second
                )
        bound = float(self.derivative_bounds[order])
        return result.intersect(-bound, bound)

    def derivative_interval(
        self, lower_radius: Fraction, upper_radius: Fraction, order: int
    ) -> Interval:
        if order in (4, 5, 6):
            return self.high_derivative_range(
                lower_radius, upper_radius, order
            )
        midpoint = (lower_radius + upper_radius) / 2
        half_width = (upper_radius - lower_radius) / 2
        midpoint_value = self.point_derivatives(midpoint, order)[order]
        lipschitz = Interval.from_fraction(
            Fraction.from_float(float(self.derivative_bounds[order + 1]))
            * half_width
        )
        bound = float(self.derivative_bounds[order])
        return (
            midpoint_value
            + Interval(-float(lipschitz.upper), float(lipschitz.upper))
        ).intersect(-bound, bound)

    def derivative_range_array(
        self,
        lower_scaled: np.ndarray,
        upper_scaled: np.ndarray,
        order: int,
    ) -> Interval:
        lower_scaled, upper_scaled = np.broadcast_arrays(
            np.asarray(lower_scaled, dtype=np.float64),
            np.asarray(upper_scaled, dtype=np.float64),
        )
        if order == 0:
            result_lower = np.zeros(lower_scaled.shape)
            result_upper = np.ones(lower_scaled.shape)
        else:
            result_lower = np.zeros(lower_scaled.shape)
            result_upper = np.zeros(lower_scaled.shape)
        below = upper_scaled <= float(ACTIVE_LOW)
        above = lower_scaled >= float(ACTIVE_HIGH)
        if order == 0:
            result_lower[below] = 1.0
            result_upper[below] = 1.0
        active = ~(below | above)
        if np.any(active):
            lo = np.clip(
                np.floor(
                    (lower_scaled[active] - float(ACTIVE_LOW))
                    / float(ACTIVE_SPAN)
                    * self.cells
                ).astype(int),
                0,
                self.cells - 1,
            )
            hi = np.clip(
                np.floor(
                    (upper_scaled[active] - float(ACTIVE_LOW))
                    / float(ACTIVE_SPAN)
                    * self.cells
                ).astype(int),
                0,
                self.cells - 1,
            )
            values_lower = self.derivative_range_lower[order][lo, hi]
            values_upper = self.derivative_range_upper[order][lo, hi]
            crosses_low = lower_scaled[active] < float(ACTIVE_LOW)
            crosses_high = upper_scaled[active] > float(ACTIVE_HIGH)
            if order == 0:
                values_lower = np.where(crosses_high, np.minimum(values_lower, 0.0), values_lower)
                values_upper = np.where(crosses_low, np.maximum(values_upper, 1.0), values_upper)
            else:
                crosses = crosses_low | crosses_high
                values_lower = np.where(crosses, np.minimum(values_lower, 0.0), values_lower)
                values_upper = np.where(crosses, np.maximum(values_upper, 0.0), values_upper)
            result_lower[active] = values_lower
            result_upper[active] = values_upper
        return Interval(result_lower, result_upper)

    def profile_interval(
        self, lower_radius: Fraction, upper_radius: Fraction
    ) -> tuple[Interval, Interval, Interval]:
        midpoint = (lower_radius + upper_radius) / 2
        half_width = (upper_radius - lower_radius) / 2
        q_lower = self.point(upper_radius)[0]
        q_upper = self.point(lower_radius)[0]
        value = Interval(float(q_lower.lower), float(q_upper.upper)).intersect(0.0, 1.0)
        _, first_midpoint, second_midpoint = self.point(midpoint)
        first_lipschitz = Interval.from_fraction(Fraction(1500, 81) * half_width)
        second_lipschitz = Interval.from_fraction(Fraction(60000, 729) * half_width)
        first = (
            first_midpoint + Interval(-float(first_lipschitz.upper), float(first_lipschitz.upper))
        ).intersect(-float(Fraction(25, 12)), 0.0)
        second = (
            second_midpoint
            + Interval(
                -float(second_lipschitz.upper),
                float(second_lipschitz.upper),
            )
        ).intersect(
            -float(Fraction(1500, 81)), float(Fraction(1500, 81))
        )
        radius = Interval.from_fraction(lower_radius)
        radius = Interval(
            radius.lower,
            Interval.from_fraction(upper_radius).upper,
        )
        radius_squared = radius * radius
        profile_p = value + radius * first + radius_squared * second / 6
        profile_q = (4 * radius * first + radius_squared * second) / 6
        sqrt_six = Interval(*arb_float_bounds(arb(6).sqrt()))
        profile_r = sqrt_six * (
            6 * radius * first + radius_squared * second
        ) / 6
        return profile_p, profile_q, profile_r

    def q_range_array(
        self, lower_scaled: np.ndarray, upper_scaled: np.ndarray
    ) -> Interval:
        lower_scaled = np.asarray(lower_scaled, dtype=np.float64)
        upper_scaled = np.asarray(upper_scaled, dtype=np.float64)
        result_lower = np.zeros(np.broadcast(lower_scaled, upper_scaled).shape)
        result_upper = np.ones_like(result_lower)
        below = upper_scaled <= float(ACTIVE_LOW)
        above = lower_scaled >= float(ACTIVE_HIGH)
        result_lower[below] = 1.0
        result_upper[below] = 1.0
        result_lower[above] = 0.0
        result_upper[above] = 0.0
        active = ~(below | above)
        if np.any(active):
            lower_position = (
                (lower_scaled[active] - float(ACTIVE_LOW))
                / float(ACTIVE_SPAN)
                * self.cells
            )
            upper_position = (
                (upper_scaled[active] - float(ACTIVE_LOW))
                / float(ACTIVE_SPAN)
                * self.cells
            )
            lower_cell = np.clip(np.floor(lower_position).astype(int), 0, self.cells - 1)
            upper_cell = np.clip(np.floor(upper_position).astype(int), 0, self.cells - 1)
            result_lower[active] = self.q_lower[np.minimum(upper_cell + 1, self.cells)]
            result_upper[active] = self.q_upper[lower_cell]
        return Interval(np.maximum(0.0, result_lower), np.minimum(1.0, result_upper))

    def q_point_array(self, radius: Interval) -> Interval:
        """Second-order certified linear interpolation at point intervals."""
        lower_radius, upper_radius = np.broadcast_arrays(
            radius.lower, radius.upper
        )
        result_lower = np.zeros(lower_radius.shape)
        result_upper = np.zeros(lower_radius.shape)
        below = upper_radius <= float(ACTIVE_LOW)
        above = lower_radius >= float(ACTIVE_HIGH)
        result_lower[below] = 1.0
        result_upper[below] = 1.0
        active = ~(below | above)
        if np.any(active):
            clipped_lower = np.maximum(lower_radius[active], float(ACTIVE_LOW))
            clipped_upper = np.minimum(upper_radius[active], float(ACTIVE_HIGH))
            position_lower = (
                (clipped_lower - float(ACTIVE_LOW))
                / float(ACTIVE_SPAN)
                * self.cells
            )
            position_upper = (
                (clipped_upper - float(ACTIVE_LOW))
                / float(ACTIVE_SPAN)
                * self.cells
            )
            cell = np.clip(
                np.floor(position_lower).astype(int), 0, self.cells - 1
            )
            same_cell = np.floor(position_upper).astype(int) == cell
            theta = Interval(
                np.maximum(0.0, position_lower - cell),
                np.minimum(1.0, position_upper - cell),
            )
            left = Interval(self.q_lower[cell], self.q_upper[cell])
            right = Interval(self.q_lower[cell + 1], self.q_upper[cell + 1])
            interpolated = (1 - theta) * left + theta * right
            cell_width = ACTIVE_SPAN / self.cells
            interpolation_error = float(
                DERIVATIVE_GLOBAL_BOUNDS[2] * cell_width**2 / 8
            )
            lower_value = interpolated.lower - interpolation_error
            upper_value = interpolated.upper + interpolation_error
            if np.any(~same_cell):
                fallback = self.q_range_array(clipped_lower, clipped_upper)
                lower_value = np.where(
                    same_cell, lower_value, fallback.lower
                )
                upper_value = np.where(
                    same_cell, upper_value, fallback.upper
                )
            crosses_low = lower_radius[active] < float(ACTIVE_LOW)
            crosses_high = upper_radius[active] > float(ACTIVE_HIGH)
            lower_value = np.where(crosses_high, np.minimum(lower_value, 0.0), lower_value)
            upper_value = np.where(crosses_low, np.maximum(upper_value, 1.0), upper_value)
            result_lower[active] = np.maximum(0.0, lower_value)
            result_upper[active] = np.minimum(1.0, upper_value)
        return Interval(result_lower, result_upper)


class AnnularPrimitiveTable:
    def __init__(
        self,
        cutoff: CutoffCertificate,
        index: int,
        power: int,
    ):
        self.index = index
        self.power = power
        self.cells = 1 << power
        self.maximum = 4.0
        self.step = self.maximum / self.cells
        lower_distance = np.arange(self.cells, dtype=np.float64) * self.step
        upper_distance = lower_distance + self.step
        first_scale = 2.0 ** (index + 1)
        second_scale = 2.0**index
        first = cutoff.q_range_array(
            down(lower_distance / first_scale),
            up(upper_distance / first_scale),
        )
        second = cutoff.q_range_array(
            down(lower_distance / second_scale),
            up(upper_distance / second_scale),
        )
        psi = (first - second).intersect(0.0, 1.0)
        support_lower = float(Fraction(2**max(index, 0), 2 ** max(-index, 0)) * ACTIVE_LOW)
        support_upper = float(
            Fraction(2 ** max(index + 1, 0), 2 ** max(-(index + 1), 0))
            * ACTIVE_HIGH
        )
        outside = (upper_distance <= support_lower) | (
            lower_distance >= support_upper
        )
        psi_lower = np.where(outside, 0.0, psi.lower)
        psi_upper = np.where(outside, 0.0, psi.upper)
        self.prefix: dict[int, tuple[np.ndarray, np.ndarray]] = {}
        for moment_power in ANNULAR_POWERS:
            factor_lower = np.zeros(self.cells)
            factor_upper = np.zeros(self.cells)
            active = ~outside
            if moment_power >= 0:
                factor_lower[active] = lower_distance[active] ** moment_power
                factor_upper[active] = upper_distance[active] ** moment_power
            else:
                factor_lower[active] = upper_distance[active] ** moment_power
                factor_upper[active] = lower_distance[active] ** moment_power
            integrand_lower = down(psi_lower * factor_lower)
            integrand_upper = up(psi_upper * factor_upper)
            prefix_lower = np.empty(self.cells + 1)
            prefix_upper = np.empty(self.cells + 1)
            prefix_lower[0] = 0.0
            prefix_upper[0] = 0.0
            for cell in range(self.cells):
                prefix_lower[cell + 1] = math.nextafter(
                    prefix_lower[cell]
                    + math.nextafter(
                        float(integrand_lower[cell]) * self.step,
                        NEGATIVE_INFINITY,
                    ),
                    NEGATIVE_INFINITY,
                )
                prefix_upper[cell + 1] = math.nextafter(
                    prefix_upper[cell]
                    + math.nextafter(
                        float(integrand_upper[cell]) * self.step,
                        POSITIVE_INFINITY,
                    ),
                    POSITIVE_INFINITY,
                )
            self.prefix[moment_power] = (prefix_lower, prefix_upper)

    def primitive_lower(self, value: np.ndarray, moment_power: int) -> np.ndarray:
        value = np.clip(value, 0.0, self.maximum)
        position = np.clip(np.floor(value / self.step).astype(int), 0, self.cells)
        return self.prefix[moment_power][0][position]

    def primitive_upper(self, value: np.ndarray, moment_power: int) -> np.ndarray:
        value = np.clip(value, 0.0, self.maximum)
        position = np.clip(np.ceil(value / self.step).astype(int), 0, self.cells)
        return self.prefix[moment_power][1][position]

    def moment_between(
        self,
        lower_min: np.ndarray,
        lower_max: np.ndarray,
        upper_min: np.ndarray,
        upper_max: np.ndarray,
        moment_power: int,
    ) -> Interval:
        result_lower = down(
            self.primitive_lower(upper_min, moment_power)
            - self.primitive_upper(lower_max, moment_power)
        )
        result_upper = up(
            self.primitive_upper(upper_max, moment_power)
            - self.primitive_lower(lower_min, moment_power)
        )
        return Interval(np.maximum(0.0, result_lower), np.maximum(0.0, result_upper))


def derive_radial_functions():
    kx, ky, kz, t, u, r, s, d = sp.symbols(
        "kx ky kz t u r s d", real=True
    )
    px, qx, rx, py, qy, ry = sp.symbols("px qx rx py qy ry", real=True)
    j_m4, j_m2, j_0, j_2, j_4 = sp.symbols("j_m4 j_m2 j_0 j_2 j_4")
    moment_symbols = {-4: j_m4, -2: j_m2, 0: j_0, 2: j_2, 4: j_4}
    vertical = sp.Matrix([kx, ky, kz])
    n = sp.Matrix([0, 0, 1])
    m = sp.Matrix([u, 0, t])

    def vorticity(p, q, radial, direction):
        return (
            p * vertical
            - q * vertical.dot(direction) * direction
            - radial * vertical.dot(direction) * vertical.cross(direction)
        )

    omega_x = vorticity(px, qx, rx, n)
    omega_y = vorticity(py, qy, ry, m)
    delta = omega_y - omega_x
    displacement = s * m - r * n
    polynomial = sp.Poly(
        sp.expand(
            displacement.dot(delta)
            * displacement.dot(omega_x.cross(delta))
        ),
        kx,
        ky,
        kz,
    )

    def sphere_moment(a: int, b: int, c: int):
        if a % 2 or b % 2 or c % 2:
            return sp.S.Zero

        def odd_double_factorial(degree: int):
            return sp.factorial2(degree - 1) if degree else sp.S.One

        return (
            odd_double_factorial(a)
            * odd_double_factorial(b)
            * odd_double_factorial(c)
            / sp.factorial2(a + b + c + 1)
        )

    angular_average = sum(
        coefficient * sphere_moment(*exponents)
        for exponents, coefficient in polynomial.terms()
    )
    angular_average = sp.expand(angular_average).subs(u**2, 1 - t**2)
    if angular_average.has(u):
        raise RuntimeError("common-rotation average retained a spurious square root")
    t_polynomial = sp.Poly(sp.expand(angular_average), t)
    radial_expression = sp.S.Zero
    for (degree,), coefficient in t_polynomial.terms():
        moment_combination = sum(
            sp.binomial(degree, power)
            * (r * r + s * s) ** (degree - power)
            * (-1) ** power
            * moment_symbols[2 * power - 4]
            for power in range(degree + 1)
        )
        radial_expression += (
            3
            * r
            * s
            * coefficient
            * moment_combination
            / (2 * r * s) ** degree
        )
    radial_expression = sp.cancel(radial_expression)
    core_expression = sp.cancel(
        radial_expression.subs({px: 1, qx: 0, rx: 0})
    )
    direct_expression = sp.cancel(
        3 * r**2 * s**2 * angular_average / d**5
    )
    direct_core_expression = sp.cancel(
        direct_expression.subs({px: 1, qx: 0, rx: 0})
    )
    distance_integrand = sp.expand(
        3
        * r
        * s
        * angular_average.subs(t, (r * r + s * s - d * d) / (2 * r * s))
        / d**4
    )
    reconstructed_moments = sp.S.Zero
    for term in sp.Add.make_args(distance_integrand):
        powers = term.as_powers_dict()
        distance_power = int(powers.get(d, 0))
        coefficient = term / d**distance_power
        reconstructed_moments += coefficient * moment_symbols[distance_power]
    direct_to_moments_exact = bool(
        sp.cancel(reconstructed_moments - radial_expression) == 0
    )
    if not direct_to_moments_exact:
        raise RuntimeError("direct angular kernel did not reproduce distance moments")
    arguments = (r, s, px, qx, rx, py, qy, ry, j_m4, j_m2, j_0, j_2, j_4)
    generic = sp.lambdify(arguments, radial_expression, modules="math", cse=True)
    core = sp.lambdify(
        (r, s, py, qy, ry, j_m4, j_m2, j_0, j_2, j_4),
        core_expression,
        modules="math",
        cse=True,
    )
    direct = sp.lambdify(
        (r, s, t, d, px, qx, rx, py, qy, ry),
        direct_expression,
        modules="math",
        cse=True,
    )
    direct_core = sp.lambdify(
        (r, s, t, d, py, qy, ry),
        direct_core_expression,
        modules="math",
        cse=True,
    )
    audits = {
        "spherePolynomialTerms": len(polynomial.terms()),
        "angularDegree": int(t_polynomial.degree()),
        "commonRotationSquareRootEliminated": not angular_average.has(u),
        "genericDenominator": str(sp.factor(sp.denom(radial_expression))),
        "coreDenominator": str(sp.factor(sp.denom(core_expression))),
        "coreCoreExactlyZero": bool(
            sp.simplify(
                radial_expression.subs(
                    {px: 1, qx: 0, rx: 0, py: 1, qy: 0, ry: 0}
                )
            )
            == 0
        ),
        "directAngularKernelDenominator": str(
            sp.factor(sp.denom(direct_expression))
        ),
        "directAngularToDistanceMomentsExact": direct_to_moments_exact,
        "bumpSecondDerivativeAudit": bump_second_critical_audit(),
    }
    return generic, core, direct, direct_core, audits


@dataclass
class RadialCell:
    lower: Fraction
    upper: Fraction
    role: str
    p: PolyInterval
    q: PolyInterval
    r: PolyInterval


def constant_poly(value: Interval) -> PolyInterval:
    return PolyInterval((value,))


def affine_poly(constant: Interval, slope: Interval) -> PolyInterval:
    return PolyInterval((constant, slope))


def build_radial_cells(
    cutoff: CutoffCertificate,
    core_cells: int,
    plateau_cells: int,
    boundary_refinement: int = 1,
) -> list[RadialCell]:
    cells: list[RadialCell] = []
    zero = Interval.exact_integer(0)
    one = Interval.exact_integer(1)
    for index in range(core_cells):
        lower = INNER_ACTIVE_LOW * Fraction(index, core_cells)
        upper = INNER_ACTIVE_LOW * Fraction(index + 1, core_cells)
        cells.append(
            RadialCell(
                lower,
                upper,
                "fixed-core",
                constant_poly(one),
                constant_poly(zero),
                constant_poly(zero),
            )
        )
    boundary_bands = (
        (
            Fraction(1) + TRANSITION_A - MOLLIFIER_RADIUS,
            Fraction(1) + TRANSITION_A + MOLLIFIER_RADIUS,
        ),
        (
            Fraction(1) + TRANSITION_B - MOLLIFIER_RADIUS,
            Fraction(1) + TRANSITION_B + MOLLIFIER_RADIUS,
        ),
    )

    def subdivisions(lower: Fraction, upper: Fraction) -> int:
        if any(lower < band_upper and upper > band_lower for band_lower, band_upper in boundary_bands):
            return boundary_refinement
        return 1

    for index in range(cutoff.cells):
        scaled_lower = cutoff.nodes[index]
        scaled_upper = cutoff.nodes[index + 1]
        count = subdivisions(scaled_lower, scaled_upper)
        for subindex in range(count):
            sub_lower = scaled_lower + (scaled_upper - scaled_lower) * Fraction(subindex, count)
            sub_upper = scaled_lower + (scaled_upper - scaled_lower) * Fraction(subindex + 1, count)
            profile = cutoff.profile_interval(sub_lower, sub_upper)
            lower = EPSILON * sub_lower
            upper = EPSILON * sub_upper
            cells.append(
                RadialCell(
                    lower,
                    upper,
                    "inner-transition",
                    affine_poly(profile[0], one - profile[0]),
                    affine_poly(profile[1], -profile[1]),
                    affine_poly(profile[2], -profile[2]),
                )
            )
    plateau_length = ACTIVE_LOW - INNER_ACTIVE_HIGH
    for index in range(plateau_cells):
        lower = INNER_ACTIVE_HIGH + plateau_length * Fraction(index, plateau_cells)
        upper = INNER_ACTIVE_HIGH + plateau_length * Fraction(
            index + 1, plateau_cells
        )
        cells.append(
            RadialCell(
                lower,
                upper,
                "intermediate-plateau",
                affine_poly(zero, one),
                constant_poly(zero),
                constant_poly(zero),
            )
        )
    for index in range(cutoff.cells):
        scaled_lower = cutoff.nodes[index]
        scaled_upper = cutoff.nodes[index + 1]
        count = subdivisions(scaled_lower, scaled_upper)
        for subindex in range(count):
            lower = scaled_lower + (scaled_upper - scaled_lower) * Fraction(subindex, count)
            upper = scaled_lower + (scaled_upper - scaled_lower) * Fraction(subindex + 1, count)
            profile = cutoff.profile_interval(lower, upper)
            cells.append(
                RadialCell(
                    lower,
                    upper,
                    "outer-transition",
                    affine_poly(zero, profile[0]),
                    affine_poly(zero, profile[1]),
                    affine_poly(zero, profile[2]),
                )
            )
    return cells


def cell_interval(lower: Fraction, upper: Fraction) -> Interval:
    lower_bound = fraction_float_bounds(lower)[0]
    upper_bound = fraction_float_bounds(upper)[1]
    return Interval(lower_bound, upper_bound)


def integrate_coefficients(
    radial_cells: list[RadialCell],
    primitives: AnnularPrimitiveTable,
    generic_function,
    core_function,
    progress,
) -> tuple[list[Interval], dict[str, object]]:
    total = [Interval.exact_integer(0) for _ in range(4)]
    pi_interval = Interval(*arb_float_bounds(arb.pi()))
    maximum_box_width = [0.0] * 4
    evaluated_boxes = 0
    skipped_core_boxes = 0
    cell_count = len(radial_cells)
    lower_float = np.asarray(
        [fraction_float_bounds(cell.lower)[0] for cell in radial_cells]
    )
    upper_float = np.asarray(
        [fraction_float_bounds(cell.upper)[1] for cell in radial_cells]
    )
    widths = [
        Interval.from_fraction(cell.upper - cell.lower) for cell in radial_cells
    ]

    for left_index, left in enumerate(radial_cells):
        if left.role == "fixed-core":
            first_right = next(
                index
                for index, cell in enumerate(radial_cells)
                if cell.role != "fixed-core"
            )
            skipped_core_boxes += max(0, first_right - left_index)
            right_start = first_right
        else:
            right_start = left_index
        if right_start >= cell_count:
            continue
        indices = np.arange(right_start, cell_count)
        right_lower = lower_float[indices]
        right_upper = upper_float[indices]
        sum_lower = down(lower_float[left_index] + right_lower)
        sum_upper = up(upper_float[left_index] + right_upper)
        if left_index == right_start and left_index in indices:
            pass
        difference_lower = np.empty(indices.size)
        difference_upper = np.empty(indices.size)
        for position, right_index in enumerate(indices):
            right = radial_cells[int(right_index)]
            if right_index == left_index:
                exact_lower = Fraction(0)
                exact_upper = left.upper - left.lower
            else:
                exact_lower = max(Fraction(0), right.lower - left.upper)
                exact_upper = right.upper - left.lower
            difference_lower[position] = fraction_float_bounds(exact_lower)[0]
            difference_upper[position] = fraction_float_bounds(exact_upper)[1]
        moments = {
            moment_power: primitives.moment_between(
                difference_lower,
                difference_upper,
                sum_lower,
                sum_upper,
                moment_power,
            )
            for moment_power in ANNULAR_POWERS
        }
        left_radius = PolyInterval((cell_interval(left.lower, left.upper),))
        right_radius_interval = Interval(right_lower, right_upper)
        right_radius = PolyInterval((right_radius_interval,))
        right_p = PolyInterval(
            (
                Interval(
                    np.asarray(
                        [
                            radial_cells[index].p.coefficients[degree].lower
                            if degree < len(radial_cells[index].p.coefficients)
                            else 0.0
                            for index in indices
                        ]
                    ),
                    np.asarray(
                        [
                            radial_cells[index].p.coefficients[degree].upper
                            if degree < len(radial_cells[index].p.coefficients)
                            else 0.0
                            for index in indices
                        ]
                    ),
                )
                for degree in range(2)
            )
        )
        right_q = PolyInterval(
            (
                Interval(
                    np.asarray(
                        [
                            radial_cells[index].q.coefficients[degree].lower
                            if degree < len(radial_cells[index].q.coefficients)
                            else 0.0
                            for index in indices
                        ]
                    ),
                    np.asarray(
                        [
                            radial_cells[index].q.coefficients[degree].upper
                            if degree < len(radial_cells[index].q.coefficients)
                            else 0.0
                            for index in indices
                        ]
                    ),
                )
                for degree in range(2)
            )
        )
        right_r = PolyInterval(
            (
                Interval(
                    np.asarray(
                        [
                            radial_cells[index].r.coefficients[degree].lower
                            if degree < len(radial_cells[index].r.coefficients)
                            else 0.0
                            for index in indices
                        ]
                    ),
                    np.asarray(
                        [
                            radial_cells[index].r.coefficients[degree].upper
                            if degree < len(radial_cells[index].r.coefficients)
                            else 0.0
                            for index in indices
                        ]
                    ),
                )
                for degree in range(2)
            )
        )
        moment_arguments = tuple(
            PolyInterval((moments[moment_power],))
            for moment_power in ANNULAR_POWERS
        )
        if left.role == "fixed-core":
            value = core_function(
                left_radius,
                right_radius,
                right_p,
                right_q,
                right_r,
                *moment_arguments,
            )
        else:
            value = generic_function(
                left_radius,
                right_radius,
                left.p,
                left.q,
                left.r,
                right_p,
                right_q,
                right_r,
                *moment_arguments,
            )
        multipliers = np.full(indices.size, 2.0)
        if right_start == left_index:
            multipliers[0] = 1.0
        area_lower = np.asarray(
            [
                float(
                    (
                        widths[left_index]
                        * widths[int(index)]
                        * Interval.exact_integer(int(multipliers[position]))
                    ).lower
                )
                for position, index in enumerate(indices)
            ]
        )
        area_upper = np.asarray(
            [
                float(
                    (
                        widths[left_index]
                        * widths[int(index)]
                        * Interval.exact_integer(int(multipliers[position]))
                    ).upper
                )
                for position, index in enumerate(indices)
            ]
        )
        area = Interval(area_lower, area_upper)
        for degree in range(4):
            coefficient = (
                value.coefficients[degree]
                if degree < len(value.coefficients)
                else Interval.exact_integer(0)
            )
            boxes = coefficient * area * pi_interval
            row = Interval(
                math.nextafter(math.fsum(float(item) for item in boxes.lower), NEGATIVE_INFINITY),
                math.nextafter(math.fsum(float(item) for item in boxes.upper), POSITIVE_INFINITY),
            )
            total[degree] = total[degree] + row
            maximum_box_width[degree] = max(
                maximum_box_width[degree],
                float(np.max(boxes.upper - boxes.lower)),
            )
        evaluated_boxes += indices.size
        if progress is not None and (
            left_index == 0
            or (left_index + 1) % max(1, cell_count // 20) == 0
            or left_index + 1 == cell_count
        ):
            record = {
                "timestampUtc": datetime.now(timezone.utc).isoformat(),
                "event": "radial-progress",
                "annulus": primitives.index,
                "rowsComplete": left_index + 1,
                "rows": cell_count,
                "evaluatedBoxes": evaluated_boxes,
                "coefficientIntervals": [value.scalar() for value in total],
            }
            progress.write(json.dumps(record, sort_keys=True) + "\n")
            progress.flush()
            print(json.dumps(record, sort_keys=True), flush=True)
    return total, {
        "radialCells": cell_count,
        "evaluatedBoxes": evaluated_boxes,
        "skippedCoreCoreBoxes": skipped_core_boxes,
        "maximumSingleBoxWidths": maximum_box_width,
    }


class AnnularAngularKernel:
    """Certified annular-cutoff ranges on distance intervals."""

    def __init__(self, cutoff: CutoffCertificate, index: int):
        self.cutoff = cutoff
        self.index = index
        self.first_scale = 2.0 ** (index + 1)
        self.second_scale = 2.0**index
        self.support_lower = float(
            Fraction(2 ** max(index, 0), 2 ** max(-index, 0)) * ACTIVE_LOW
        )
        self.support_upper = float(
            Fraction(
                2 ** max(index + 1, 0),
                2 ** max(-(index + 1), 0),
            )
            * ACTIVE_HIGH
        )

    def enclose(
        self, distance: Interval
    ) -> tuple[Interval, Interval, np.ndarray]:
        outside = (distance.upper <= self.support_lower) | (
            distance.lower >= self.support_upper
        )
        clipped_lower = np.maximum(distance.lower, self.support_lower)
        clipped_upper = np.minimum(distance.upper, self.support_upper)
        clipped_lower = np.where(outside, self.support_lower, clipped_lower)
        clipped_upper = np.where(outside, self.support_lower, clipped_upper)
        clipped = Interval(clipped_lower, clipped_upper)
        first = self.cutoff.q_range_array(
            down(clipped_lower / self.first_scale),
            up(clipped_upper / self.first_scale),
        )
        second = self.cutoff.q_range_array(
            down(clipped_lower / self.second_scale),
            up(clipped_upper / self.second_scale),
        )
        psi = (first - second).intersect(0.0, 1.0)
        psi = Interval(
            np.where(outside, 0.0, psi.lower),
            np.where(outside, 0.0, psi.upper),
        )
        partial = (~outside) & (
            (distance.lower < self.support_lower)
            | (distance.upper > self.support_upper)
        )
        return clipped, psi, partial


class Jet2:
    """Second-order interval jet in the variables (r, s, t)."""

    __array_priority__ = 1002
    dimension = 3

    def __init__(
        self,
        value: PolyInterval,
        gradient: list[PolyInterval] | None = None,
        hessian: list[list[PolyInterval]] | None = None,
    ):
        self.value = PolyInterval.coerce(value)
        zero = PolyInterval.coerce(0)
        self.gradient = gradient or [zero for _ in range(self.dimension)]
        self.hessian = hessian or [
            [zero for _ in range(self.dimension)]
            for _ in range(self.dimension)
        ]

    @staticmethod
    def coerce(value) -> "Jet2":
        if isinstance(value, Jet2):
            return value
        return Jet2(PolyInterval.coerce(value))

    @staticmethod
    def variable(value: Interval, axis: int) -> "Jet2":
        zero = PolyInterval.coerce(0)
        gradient = [zero for _ in range(Jet2.dimension)]
        gradient[axis] = PolyInterval.coerce(1)
        return Jet2(PolyInterval.coerce(value), gradient)

    def __add__(self, other):
        other = Jet2.coerce(other)
        return Jet2(
            self.value + other.value,
            [
                self.gradient[i] + other.gradient[i]
                for i in range(self.dimension)
            ],
            [
                [
                    self.hessian[i][j] + other.hessian[i][j]
                    for j in range(self.dimension)
                ]
                for i in range(self.dimension)
            ],
        )

    __radd__ = __add__

    def __neg__(self):
        return Jet2(
            -self.value,
            [-value for value in self.gradient],
            [[-value for value in row] for row in self.hessian],
        )

    def __sub__(self, other):
        return self + (-Jet2.coerce(other))

    def __rsub__(self, other):
        return Jet2.coerce(other) - self

    def __mul__(self, other):
        other = Jet2.coerce(other)
        return Jet2(
            self.value * other.value,
            [
                self.gradient[i] * other.value
                + self.value * other.gradient[i]
                for i in range(self.dimension)
            ],
            [
                [
                    self.hessian[i][j] * other.value
                    + self.gradient[i] * other.gradient[j]
                    + self.gradient[j] * other.gradient[i]
                    + self.value * other.hessian[i][j]
                    for j in range(self.dimension)
                ]
                for i in range(self.dimension)
            ],
        )

    __rmul__ = __mul__

    def reciprocal(self):
        inverse = 1 / self.value
        inverse_squared = inverse * inverse
        inverse_cubed = inverse_squared * inverse
        return Jet2(
            inverse,
            [-value * inverse_squared for value in self.gradient],
            [
                [
                    2
                    * self.gradient[i]
                    * self.gradient[j]
                    * inverse_cubed
                    - self.hessian[i][j] * inverse_squared
                    for j in range(self.dimension)
                ]
                for i in range(self.dimension)
            ],
        )

    def __truediv__(self, other):
        return self * Jet2.coerce(other).reciprocal()

    def __rtruediv__(self, other):
        return Jet2.coerce(other) / self

    def __pow__(self, exponent: int):
        if not isinstance(exponent, (int, np.integer)) or exponent < 0:
            raise ValueError("only nonnegative integer jet powers are supported")
        result = Jet2.coerce(1)
        base = self
        power = int(exponent)
        while power:
            if power & 1:
                result = result * base
            power >>= 1
            if power:
                base = base * base
        return result


def radial_field_components(
    radius: Interval,
    q_derivatives: tuple[Interval, ...],
) -> tuple[list[Interval], list[Interval], list[Interval]]:
    q0, q1, q2, q3, q4, q5, q6 = q_derivatives[:7]
    sqrt_six = Interval(*arb_float_bounds(arb(6).sqrt()))
    p = [
        q0 + radius * q1 + radius**2 * q2 / 6,
        2 * q1 + Fraction(4, 3) * radius * q2 + radius**2 * q3 / 6,
        Fraction(10, 3) * q2
        + Fraction(5, 3) * radius * q3
        + radius**2 * q4 / 6,
        5 * q3 + 2 * radius * q4 + radius**2 * q5 / 6,
        7 * q4 + Fraction(7, 3) * radius * q5 + radius**2 * q6 / 6,
    ]
    q = [
        (4 * radius * q1 + radius**2 * q2) / 6,
        Fraction(2, 3) * q1 + radius * q2 + radius**2 * q3 / 6,
        Fraction(5, 3) * q2
        + Fraction(4, 3) * radius * q3
        + radius**2 * q4 / 6,
        3 * q3 + Fraction(5, 3) * radius * q4 + radius**2 * q5 / 6,
        Fraction(14, 3) * q4
        + 2 * radius * q5
        + radius**2 * q6 / 6,
    ]
    h = [
        radius * q1 + radius**2 * q2 / 6,
        q1 + Fraction(4, 3) * radius * q2 + radius**2 * q3 / 6,
        Fraction(7, 3) * q2
        + Fraction(5, 3) * radius * q3
        + radius**2 * q4 / 6,
        4 * q3 + 2 * radius * q4 + radius**2 * q5 / 6,
        6 * q4 + Fraction(7, 3) * radius * q5 + radius**2 * q6 / 6,
    ]
    return p, q, [sqrt_six * value for value in h]


def profile_polynomial_by_role(
    role: str,
    components: tuple[list[Interval], list[Interval], list[Interval]] | None,
    derivative_order: int,
) -> tuple[PolyInterval, PolyInterval, PolyInterval]:
    zero = Interval.exact_integer(0)
    one = Interval.exact_integer(1)
    if role == "fixed-core":
        return (
            PolyInterval((one if derivative_order == 0 else zero,)),
            PolyInterval((zero,)),
            PolyInterval((zero,)),
        )
    if role == "intermediate-plateau":
        return (
            PolyInterval((zero, one if derivative_order == 0 else zero)),
            PolyInterval((zero,)),
            PolyInterval((zero,)),
        )
    if components is None:
        raise ValueError("transition cells require profile components")
    p, q, radial = (
        component[derivative_order] for component in components
    )
    if role == "inner-transition":
        return (
            PolyInterval((p, (one if derivative_order == 0 else zero) - p)),
            PolyInterval((q, -q)),
            PolyInterval((radial, -radial)),
        )
    if role == "outer-transition":
        return (
            PolyInterval((zero, p)),
            PolyInterval((zero, q)),
            PolyInterval((zero, radial)),
        )
    raise ValueError(f"unknown radial role {role}")


def radial_cell_profile_data(
    cell: RadialCell,
    cutoff: CutoffCertificate,
    at_midpoint: bool,
) -> list[tuple[PolyInterval, PolyInterval, PolyInterval]]:
    if cell.role in ("fixed-core", "intermediate-plateau"):
        return [
            profile_polynomial_by_role(cell.role, None, order)
            for order in range(5)
        ]
    scale = EPSILON if cell.role == "inner-transition" else Fraction(1)
    if at_midpoint:
        scaled = (cell.lower + cell.upper) / (2 * scale)
        derivatives = cutoff.point_derivatives(scaled, 6)
        radius = Interval.from_fraction(scaled)
    else:
        scaled_lower = cell.lower / scale
        scaled_upper = cell.upper / scale
        derivatives = tuple(
            cutoff.derivative_range_array(
                np.asarray(float(scaled_lower)),
                np.asarray(float(scaled_upper)),
                order,
            )
            for order in range(4)
        ) + (
            cutoff.high_derivative_range(
                scaled_lower, scaled_upper, 4
            ),
            cutoff.high_derivative_range(
                scaled_lower, scaled_upper, 5
            ),
            cutoff.high_derivative_range(
                scaled_lower, scaled_upper, 6
            ),
        )
        radius = cell_interval(scaled_lower, scaled_upper)
    components = radial_field_components(radius, derivatives)
    result = []
    for order in range(5):
        fields = profile_polynomial_by_role(cell.role, components, order)
        scale_factor = Interval.from_fraction(scale**order)
        if order:
            fields = tuple(field / scale_factor for field in fields)
        result.append(fields)
    return result


def field_jet(
    data: list[tuple[PolyInterval, PolyInterval, PolyInterval]],
    field_index: int,
    axis: int,
) -> Jet2:
    zero = PolyInterval.coerce(0)
    gradient = [zero for _ in range(3)]
    gradient[axis] = data[1][field_index]
    hessian = [[zero for _ in range(3)] for _ in range(3)]
    hessian[axis][axis] = data[2][field_index]
    return Jet2(data[0][field_index], gradient, hessian)


def vector_polynomial(polynomials: list[PolyInterval]) -> PolyInterval:
    degree_count = max(len(value.coefficients) for value in polynomials)
    return PolyInterval(
        Interval(
            np.asarray(
                [
                    float(value.coefficients[degree].lower)
                    if degree < len(value.coefficients)
                    else 0.0
                    for value in polynomials
                ]
            ),
            np.asarray(
                [
                    float(value.coefficients[degree].upper)
                    if degree < len(value.coefficients)
                    else 0.0
                    for value in polynomials
                ]
            ),
        )
        for degree in range(degree_count)
    )


def vector_profile_data(
    all_data: list[list[tuple[PolyInterval, PolyInterval, PolyInterval]]],
    indices: np.ndarray,
) -> list[tuple[PolyInterval, PolyInterval, PolyInterval]]:
    return [
        tuple(
            vector_polynomial(
                [all_data[int(index)][order][field] for index in indices]
            )
            for field in range(3)
        )
        for order in range(len(all_data[0]))
    ]


def distance_jet_on_active_support(
    radius_r: Jet2,
    radius_s: Jet2,
    cosine: Jet2,
    clipped_distance: Interval,
) -> Jet2:
    squared = radius_r**2 + radius_s**2 - 2 * radius_r * radius_s * cosine
    distance_value = PolyInterval.coerce(clipped_distance)
    two_distance = 2 * distance_value
    four_distance_cubed = 4 * distance_value**3
    gradient = [
        squared.gradient[index] / two_distance for index in range(3)
    ]
    hessian = [
        [
            squared.hessian[i][j] / two_distance
            - squared.gradient[i]
            * squared.gradient[j]
            / four_distance_cubed
            for j in range(3)
        ]
        for i in range(3)
    ]
    return Jet2(distance_value, gradient, hessian)


def annular_cutoff_derivatives(
    cutoff: CutoffCertificate,
    index: int,
    distance: Interval,
    point_value: bool,
) -> tuple[Interval, ...]:
    first_scale = 2.0 ** (index + 1)
    second_scale = 2.0**index
    values: list[Interval] = []
    for order in range(4):
        first_lower = down(distance.lower / first_scale)
        first_upper = up(distance.upper / first_scale)
        second_lower = down(distance.lower / second_scale)
        second_upper = up(distance.upper / second_scale)
        if point_value and order == 0:
            first = cutoff.q_point_array(Interval(first_lower, first_upper))
            second = cutoff.q_point_array(Interval(second_lower, second_upper))
        else:
            first = cutoff.derivative_range_array(
                first_lower, first_upper, order
            )
            second = cutoff.derivative_range_array(
                second_lower, second_upper, order
            )
        values.append(
            first / Interval.from_number(first_scale**order)
            - second / Interval.from_number(second_scale**order)
        )
    return tuple(values)


def compose_scalar_jet(
    argument: Jet2,
    derivatives: tuple[Interval, Interval, Interval],
) -> Jet2:
    value, first, second = (PolyInterval.coerce(item) for item in derivatives)
    return Jet2(
        value,
        [first * argument.gradient[i] for i in range(3)],
        [
            [
                second * argument.gradient[i] * argument.gradient[j]
                + first * argument.hessian[i][j]
                for j in range(3)
            ]
            for i in range(3)
        ],
    )


def polynomial_coefficient(value: PolyInterval, degree: int) -> Interval:
    if degree < len(value.coefficients):
        return value.coefficients[degree]
    return Interval.exact_integer(0)


def interval_absolute_maximum(value: Interval) -> np.ndarray:
    return np.maximum(np.abs(value.lower), np.abs(value.upper))


class Taylor2D4:
    """Bivariate normalized derivative algebra through total degree four."""

    __array_priority__ = 1003
    maximum_degree = 4

    def __init__(self, coefficients: dict[tuple[int, int], PolyInterval]):
        self.coefficients = {
            key: PolyInterval.coerce(value)
            for key, value in coefficients.items()
            if sum(key) <= self.maximum_degree
        }

    @staticmethod
    def coerce(value) -> "Taylor2D4":
        if isinstance(value, Taylor2D4):
            return value
        return Taylor2D4({(0, 0): PolyInterval.coerce(value)})

    def coefficient(self, i: int, j: int) -> PolyInterval:
        return self.coefficients.get((i, j), PolyInterval.coerce(0))

    def __add__(self, other):
        other = Taylor2D4.coerce(other)
        keys = set(self.coefficients) | set(other.coefficients)
        return Taylor2D4(
            {
                key: self.coefficient(*key) + other.coefficient(*key)
                for key in keys
            }
        )

    __radd__ = __add__

    def __neg__(self):
        return Taylor2D4({key: -value for key, value in self.coefficients.items()})

    def __sub__(self, other):
        return self + (-Taylor2D4.coerce(other))

    def __rsub__(self, other):
        return Taylor2D4.coerce(other) - self

    def __mul__(self, other):
        other = Taylor2D4.coerce(other)
        result: dict[tuple[int, int], PolyInterval] = {}
        for (i, j), left in self.coefficients.items():
            for (k, ell), right in other.coefficients.items():
                key = (i + k, j + ell)
                if sum(key) > self.maximum_degree:
                    continue
                result[key] = result.get(key, PolyInterval.coerce(0)) + left * right
        return Taylor2D4(result)

    __rmul__ = __mul__

    def reciprocal(self):
        a00 = self.coefficient(0, 0)
        inverse00 = 1 / a00
        result: dict[tuple[int, int], PolyInterval] = {(0, 0): inverse00}
        for total_degree in range(1, self.maximum_degree + 1):
            for i in range(total_degree + 1):
                j = total_degree - i
                convolution = PolyInterval.coerce(0)
                for p in range(i + 1):
                    for q in range(j + 1):
                        if p == 0 and q == 0:
                            continue
                        convolution = convolution + self.coefficient(p, q) * result.get(
                            (i - p, j - q), PolyInterval.coerce(0)
                        )
                result[(i, j)] = -inverse00 * convolution
        return Taylor2D4(result)

    def __truediv__(self, other):
        return self * Taylor2D4.coerce(other).reciprocal()

    def __rtruediv__(self, other):
        return Taylor2D4.coerce(other) / self

    def __pow__(self, exponent: int):
        if not isinstance(exponent, (int, np.integer)) or exponent < 0:
            raise ValueError("only nonnegative Taylor powers are supported")
        result = Taylor2D4.coerce(1)
        base = self
        power = int(exponent)
        while power:
            if power & 1:
                result = result * base
            power >>= 1
            if power:
                base = base * base
        return result


def profile_taylor(
    data: list[tuple[PolyInterval, PolyInterval, PolyInterval]],
    field_index: int,
    axis: int,
) -> Taylor2D4:
    coefficients: dict[tuple[int, int], PolyInterval] = {}
    for order in range(5):
        key = (order, 0) if axis == 0 else (0, order)
        coefficients[key] = data[order][field_index] / math.factorial(order)
    return Taylor2D4(coefficients)


def radius_taylor(value: Interval, axis: int) -> Taylor2D4:
    key = (1, 0) if axis == 0 else (0, 1)
    return Taylor2D4(
        {(0, 0): PolyInterval.coerce(value), key: PolyInterval.coerce(1)}
    )


def integrate_coefficients_midpoint(
    radial_cells: list[RadialCell],
    cutoff: CutoffCertificate,
    annular: AnnularAngularKernel,
    direct_function,
    direct_core_function,
    angular_cells: int,
    progress,
) -> tuple[list[Interval], dict[str, object]]:
    """Certified midpoint cubature with a full interval-Hessian remainder."""

    total = [Interval.exact_integer(0) for _ in range(4)]
    pi_interval = Interval(*arb_float_bounds(arb.pi()))
    maximum_midpoint_remainder = [0.0] * 4
    evaluated_radial_boxes = 0
    active_angular_boxes = 0
    cell_count = len(radial_cells)
    first_non_core = next(
        index for index, cell in enumerate(radial_cells) if cell.role != "fixed-core"
    )
    midpoint_data = [
        radial_cell_profile_data(cell, cutoff, True) for cell in radial_cells
    ]
    range_data = [
        radial_cell_profile_data(cell, cutoff, False) for cell in radial_cells
    ]
    widths_fraction = [cell.upper - cell.lower for cell in radial_cells]
    widths = [Interval.from_fraction(value) for value in widths_fraction]
    midpoint_fraction = [(cell.lower + cell.upper) / 2 for cell in radial_cells]
    midpoint_intervals = [Interval.from_fraction(value) for value in midpoint_fraction]
    angular_width_fraction = Fraction(2, angular_cells)
    angular_width = Interval.from_fraction(angular_width_fraction)
    angular_width_float = float(angular_width_fraction)

    for left_index, left in enumerate(radial_cells):
        right_start = first_non_core if left.role == "fixed-core" else left_index
        if right_start >= cell_count:
            continue
        indices = np.arange(right_start, cell_count)
        right_midpoint = Interval(
            np.asarray([float(midpoint_intervals[int(i)].lower) for i in indices]),
            np.asarray([float(midpoint_intervals[int(i)].upper) for i in indices]),
        )
        right_radius_range = Interval(
            np.asarray(
                [fraction_float_bounds(radial_cells[int(i)].lower)[0] for i in indices]
            ),
            np.asarray(
                [fraction_float_bounds(radial_cells[int(i)].upper)[1] for i in indices]
            ),
        )
        right_midpoint_data = vector_profile_data(midpoint_data, indices)
        right_range_data = vector_profile_data(range_data, indices)
        left_midpoint_radius = PolyInterval.coerce(midpoint_intervals[left_index])
        right_midpoint_radius = PolyInterval.coerce(right_midpoint)
        left_midpoint_fields = midpoint_data[left_index][0]
        right_midpoint_fields = right_midpoint_data[0]
        left_radius_jet = Jet2.variable(
            cell_interval(left.lower, left.upper), 0
        )
        right_radius_jet = Jet2.variable(right_radius_range, 1)
        left_field_jets = [
            field_jet(range_data[left_index], field, 0) for field in range(3)
        ]
        right_field_jets = [
            field_jet(right_range_data, field, 1) for field in range(3)
        ]
        row_total = [
            Interval(np.zeros(indices.size), np.zeros(indices.size))
            for _ in range(4)
        ]

        for angular_index in range(angular_cells):
            t_lower = Fraction(-1) + angular_width_fraction * angular_index
            t_upper = t_lower + angular_width_fraction
            t_midpoint = (t_lower + t_upper) / 2
            t_midpoint_interval = Interval.from_fraction(t_midpoint)
            t_range = cell_interval(t_lower, t_upper)

            center_squared = (
                midpoint_intervals[left_index] ** 2
                + right_midpoint**2
                - 2
                * midpoint_intervals[left_index]
                * right_midpoint
                * t_midpoint_interval
            )
            center_distance = Interval(
                np.maximum(0.0, center_squared.lower),
                np.maximum(0.0, center_squared.upper),
            ).sqrt()
            center_clipped, _, _ = annular.enclose(center_distance)
            center_psi = annular_cutoff_derivatives(
                cutoff, annular.index, center_distance, True
            )[0].intersect(0.0, 1.0)
            if left.role == "fixed-core":
                center_value = direct_core_function(
                    left_midpoint_radius,
                    right_midpoint_radius,
                    PolyInterval.coerce(t_midpoint_interval),
                    PolyInterval.coerce(center_clipped),
                    *right_midpoint_fields,
                )
            else:
                center_value = direct_function(
                    left_midpoint_radius,
                    right_midpoint_radius,
                    PolyInterval.coerce(t_midpoint_interval),
                    PolyInterval.coerce(center_clipped),
                    *left_midpoint_fields,
                    *right_midpoint_fields,
                )
            center_value = center_value * PolyInterval.coerce(center_psi)

            t_jet = Jet2.variable(t_range, 2)
            squared_range = (
                cell_interval(left.lower, left.upper) ** 2
                + right_radius_range**2
                - 2
                * cell_interval(left.lower, left.upper)
                * right_radius_range
                * t_range
            )
            distance_range = Interval(
                np.maximum(0.0, squared_range.lower),
                np.maximum(0.0, squared_range.upper),
            ).sqrt()
            clipped_distance, psi_range, _ = annular.enclose(distance_range)
            active = psi_range.upper > 0.0
            active_angular_boxes += int(np.count_nonzero(active))
            distance_jet = distance_jet_on_active_support(
                left_radius_jet,
                right_radius_jet,
                t_jet,
                clipped_distance,
            )
            psi_derivatives = annular_cutoff_derivatives(
                cutoff, annular.index, clipped_distance, False
            )
            psi_derivatives = tuple(
                Interval(
                    np.where(active, value.lower, 0.0),
                    np.where(active, value.upper, 0.0),
                )
                for value in psi_derivatives
            )
            psi_jet = compose_scalar_jet(distance_jet, psi_derivatives[:3])
            if left.role == "fixed-core":
                box_value = direct_core_function(
                    left_radius_jet,
                    right_radius_jet,
                    t_jet,
                    distance_jet,
                    *right_field_jets,
                )
            else:
                box_value = direct_function(
                    left_radius_jet,
                    right_radius_jet,
                    t_jet,
                    distance_jet,
                    *left_field_jets,
                    *right_field_jets,
                )
            box_value = box_value * psi_jet

            width_r = float(widths_fraction[left_index])
            width_s = np.asarray(
                [float(widths_fraction[int(i)]) for i in indices]
            )
            for degree in range(4):
                remainder = np.zeros(indices.size)
                variable_widths = [width_r, width_s, angular_width_float]
                for i in range(3):
                    diagonal = polynomial_coefficient(
                        box_value.hessian[i][i], degree
                    )
                    remainder += (
                        interval_absolute_maximum(diagonal)
                        * variable_widths[i] ** 2
                        / 24.0
                    )
                    for j in range(i + 1, 3):
                        mixed = polynomial_coefficient(
                            box_value.hessian[i][j], degree
                        )
                        remainder += (
                            interval_absolute_maximum(mixed)
                            * variable_widths[i]
                            * variable_widths[j]
                            / 16.0
                        )
                remainder = up(remainder)
                center_coefficient = polynomial_coefficient(center_value, degree)
                enclosed = center_coefficient + Interval(-remainder, remainder)
                row_total[degree] = row_total[degree] + enclosed * angular_width
                maximum_midpoint_remainder[degree] = max(
                    maximum_midpoint_remainder[degree],
                    float(np.max(remainder)),
                )

        multipliers = np.full(indices.size, 2)
        if right_start == left_index:
            multipliers[0] = 1
        area = Interval(
            np.asarray(
                [
                    float(
                        (
                            widths[left_index]
                            * widths[int(index)]
                            * Interval.exact_integer(int(multipliers[position]))
                        ).lower
                    )
                    for position, index in enumerate(indices)
                ]
            ),
            np.asarray(
                [
                    float(
                        (
                            widths[left_index]
                            * widths[int(index)]
                            * Interval.exact_integer(int(multipliers[position]))
                        ).upper
                    )
                    for position, index in enumerate(indices)
                ]
            ),
        )
        for degree in range(4):
            boxes = row_total[degree] * area * pi_interval
            row = Interval(
                math.nextafter(math.fsum(float(item) for item in boxes.lower), NEGATIVE_INFINITY),
                math.nextafter(math.fsum(float(item) for item in boxes.upper), POSITIVE_INFINITY),
            )
            total[degree] = total[degree] + row
        evaluated_radial_boxes += indices.size
        if progress is not None and (
            left_index == 0
            or (left_index + 1) % max(1, cell_count // 20) == 0
            or left_index + 1 == cell_count
        ):
            record = {
                "timestampUtc": datetime.now(timezone.utc).isoformat(),
                "event": "midpoint-progress",
                "annulus": annular.index,
                "rowsComplete": left_index + 1,
                "rows": cell_count,
                "angularCells": angular_cells,
                "evaluatedRadialBoxes": evaluated_radial_boxes,
                "activeAngularBoxes": active_angular_boxes,
                "coefficientIntervals": [value.scalar() for value in total],
            }
            progress.write(json.dumps(record, sort_keys=True) + "\n")
            progress.flush()
            print(json.dumps(record, sort_keys=True), flush=True)
    return total, {
        "rule": "tensor midpoint with full interval-Hessian remainder",
        "radialCells": cell_count,
        "angularCells": angular_cells,
        "evaluatedRadialBoxes": evaluated_radial_boxes,
        "activeAngularBoxes": active_angular_boxes,
        "maximumPointwiseMidpointRemainders": maximum_midpoint_remainder,
        "skippedCoreCoreBoxes": first_non_core * (first_non_core + 1) // 2,
    }


class AnnularMomentCertificate:
    """Validated trapezoidal primitives for the five distance moments."""

    def __init__(
        self,
        cutoff: CutoffCertificate,
        annular: AnnularAngularKernel,
        power: int,
    ):
        self.cutoff = cutoff
        self.annular = annular
        self.power = power
        self.cells = 1 << power
        self.maximum = 4.0
        self.step = self.maximum / self.cells
        nodes = np.arange(self.cells + 1, dtype=np.float64) * self.step
        node_interval = Interval(down(nodes), up(nodes))
        node_clipped, _, _ = annular.enclose(node_interval)
        node_psi = annular_cutoff_derivatives(
            cutoff, annular.index, node_interval, True
        )[0].intersect(0.0, 1.0)
        node_active = node_psi.upper > 0.0
        lower_nodes = nodes[:-1]
        upper_nodes = nodes[1:]
        cell_distance = Interval(down(lower_nodes), up(upper_nodes))
        clipped_distance, psi_range, _ = annular.enclose(cell_distance)
        active = psi_range.upper > 0.0
        psi0, psi1, psi2, _psi3 = annular_cutoff_derivatives(
            cutoff, annular.index, clipped_distance, False
        )
        psi0 = Interval(
            np.where(active, psi0.lower, 0.0),
            np.where(active, psi0.upper, 0.0),
        )
        psi1 = Interval(
            np.where(active, psi1.lower, 0.0),
            np.where(active, psi1.upper, 0.0),
        )
        psi2 = Interval(
            np.where(active, psi2.lower, 0.0),
            np.where(active, psi2.upper, 0.0),
        )
        self.endpoint_integrands: dict[int, Interval] = {}
        self.second_derivative_bounds: dict[int, np.ndarray] = {}
        self.prefix: dict[int, tuple[np.ndarray, np.ndarray]] = {}
        for moment_power in ANNULAR_POWERS:
            safe_nodes = Interval(
                np.where(node_active, node_clipped.lower, annular.support_lower),
                np.where(node_active, node_clipped.upper, annular.support_lower),
            )
            endpoint = node_psi * safe_nodes**moment_power if moment_power >= 0 else node_psi / safe_nodes ** (-moment_power)
            endpoint = Interval(
                np.where(node_active, endpoint.lower, 0.0),
                np.where(node_active, endpoint.upper, 0.0),
            )
            self.endpoint_integrands[moment_power] = endpoint
            if moment_power >= 0:
                d_n = clipped_distance**moment_power
                d_n1 = clipped_distance ** max(0, moment_power - 1)
                d_n2 = clipped_distance ** max(0, moment_power - 2)
            else:
                d_n = 1 / clipped_distance ** (-moment_power)
                d_n1 = 1 / clipped_distance ** (1 - moment_power)
                d_n2 = 1 / clipped_distance ** (2 - moment_power)
            second_derivative = psi2 * d_n
            if moment_power:
                second_derivative = second_derivative + 2 * moment_power * psi1 * d_n1
            if moment_power * (moment_power - 1):
                second_derivative = (
                    second_derivative
                    + moment_power
                    * (moment_power - 1)
                    * psi0
                    * d_n2
                )
            second_bound = interval_absolute_maximum(second_derivative)
            second_bound = np.where(active, second_bound, 0.0)
            self.second_derivative_bounds[moment_power] = second_bound
            trapezoid = (
                Interval(endpoint.lower[:-1], endpoint.upper[:-1])
                + Interval(endpoint.lower[1:], endpoint.upper[1:])
            ) * Interval.from_number(self.step / 2.0)
            error = up(second_bound * self.step**3 / 12.0)
            contribution = trapezoid + Interval(-error, error)
            prefix_lower = np.empty(self.cells + 1)
            prefix_upper = np.empty(self.cells + 1)
            prefix_lower[0] = 0.0
            prefix_upper[0] = 0.0
            for cell in range(self.cells):
                prefix_lower[cell + 1] = math.nextafter(
                    prefix_lower[cell] + float(contribution.lower[cell]),
                    NEGATIVE_INFINITY,
                )
                prefix_upper[cell + 1] = math.nextafter(
                    prefix_upper[cell] + float(contribution.upper[cell]),
                    POSITIVE_INFINITY,
                )
            self.prefix[moment_power] = (prefix_lower, prefix_upper)

    def primitive_point(self, value: Interval, moment_power: int) -> Interval:
        lower_value, upper_value = np.broadcast_arrays(value.lower, value.upper)
        clipped_lower = np.clip(lower_value, 0.0, self.maximum)
        clipped_upper = np.clip(upper_value, 0.0, self.maximum)
        lower_position = clipped_lower / self.step
        upper_position = clipped_upper / self.step
        lower_cell = np.clip(np.floor(lower_position).astype(int), 0, self.cells - 1)
        upper_cell = np.clip(np.floor(upper_position).astype(int), 0, self.cells - 1)
        same = lower_cell == upper_cell
        prefix_lower, prefix_upper = self.prefix[moment_power]
        start = lower_cell.astype(int)
        start_node = start * self.step
        delta = Interval(
            np.maximum(0.0, clipped_lower - start_node),
            np.maximum(0.0, clipped_upper - start_node),
        )
        endpoint = self.endpoint_integrands[moment_power]
        left_value = Interval(endpoint.lower[start], endpoint.upper[start])
        if moment_power >= 0:
            safe_value = Interval(
                np.maximum(value.lower, self.annular.support_lower),
                np.maximum(value.upper, self.annular.support_lower),
            )
            point_factor = safe_value**moment_power
        else:
            safe_value = Interval(
                np.maximum(value.lower, self.annular.support_lower),
                np.maximum(value.upper, self.annular.support_lower),
            )
            point_factor = 1 / safe_value ** (-moment_power)
        point_psi = annular_cutoff_derivatives(
            self.cutoff, self.annular.index, value, True
        )[0].intersect(0.0, 1.0)
        right_value = point_psi * point_factor
        partial = delta * (left_value + right_value) / 2
        error = up(
            self.second_derivative_bounds[moment_power][start]
            * np.maximum(delta.upper, 0.0) ** 3
            / 12.0
        )
        result = Interval(prefix_lower[start], prefix_upper[start]) + partial + Interval(-error, error)
        if np.any(~same):
            fallback = Interval(
                prefix_lower[np.clip(np.floor(lower_position).astype(int), 0, self.cells)],
                prefix_upper[np.clip(np.ceil(upper_position).astype(int), 0, self.cells)],
            )
            result = Interval(
                np.where(same, result.lower, fallback.lower),
                np.where(same, result.upper, fallback.upper),
            )
        return result

    def primitive_range(self, value: Interval, moment_power: int) -> Interval:
        lower_position = np.clip(
            np.floor(np.clip(value.lower, 0.0, self.maximum) / self.step).astype(int),
            0,
            self.cells,
        )
        upper_position = np.clip(
            np.ceil(np.clip(value.upper, 0.0, self.maximum) / self.step).astype(int),
            0,
            self.cells,
        )
        prefix_lower, prefix_upper = self.prefix[moment_power]
        return Interval(prefix_lower[lower_position], prefix_upper[upper_position])

    def integrand_derivatives(
        self, value: Interval, moment_power: int
    ) -> tuple[Interval, Interval, Interval, Interval]:
        clipped, psi_range, _ = self.annular.enclose(value)
        active = psi_range.upper > 0.0
        psi0, psi1, psi2, psi3 = annular_cutoff_derivatives(
            self.cutoff, self.annular.index, clipped, False
        )
        safe = clipped
        if moment_power >= 0:
            power = safe**moment_power
            previous = safe ** max(0, moment_power - 1)
        else:
            power = 1 / safe ** (-moment_power)
            previous = 1 / safe ** (1 - moment_power)
        value0 = psi0 * power
        value1 = psi1 * power
        if moment_power:
            value1 = value1 + moment_power * psi0 * previous
        if moment_power >= 0:
            previous2 = safe ** max(0, moment_power - 2)
        else:
            previous2 = 1 / safe ** (2 - moment_power)
        value2 = psi2 * power
        if moment_power:
            value2 = value2 + 2 * moment_power * psi1 * previous
        if moment_power * (moment_power - 1):
            value2 = (
                value2
                + moment_power
                * (moment_power - 1)
                * psi0
                * previous2
            )
        if moment_power >= 0:
            previous3 = safe ** max(0, moment_power - 3)
        else:
            previous3 = 1 / safe ** (3 - moment_power)
        value3 = psi3 * power
        if moment_power:
            value3 = value3 + 3 * moment_power * psi2 * previous
        if moment_power * (moment_power - 1):
            value3 = (
                value3
                + 3
                * moment_power
                * (moment_power - 1)
                * psi1
                * previous2
            )
        if moment_power * (moment_power - 1) * (moment_power - 2):
            value3 = (
                value3
                + moment_power
                * (moment_power - 1)
                * (moment_power - 2)
                * psi0
                * previous3
            )
        return tuple(
            Interval(
                np.where(active, result.lower, 0.0),
                np.where(active, result.upper, 0.0),
            )
            for result in (value0, value1, value2, value3)
        )


def moment_jet(
    certificate: AnnularMomentCertificate,
    moment_power: int,
    radius_r: Interval,
    radius_s: Interval,
    center_r: Interval,
    center_s: Interval,
) -> tuple[PolyInterval, Jet2]:
    center_sum = center_r + center_s
    center_difference = center_s - center_r
    range_sum = radius_r + radius_s
    range_difference = radius_s - radius_r
    center_lower = certificate.primitive_point(center_difference, moment_power)
    center_value = certificate.primitive_point(center_sum, moment_power) - center_lower
    lower_range = certificate.primitive_range(range_difference, moment_power)
    value_range = certificate.primitive_range(range_sum, moment_power) - lower_range
    upper_g, upper_gp, *_ = certificate.integrand_derivatives(range_sum, moment_power)
    lower_g, lower_gp, *_ = certificate.integrand_derivatives(
        range_difference, moment_power
    )
    zero = PolyInterval.coerce(0)
    gradient = [
        PolyInterval.coerce(upper_g + lower_g),
        PolyInterval.coerce(upper_g - lower_g),
        zero,
    ]
    hessian = [[zero for _ in range(3)] for _ in range(3)]
    hessian[0][0] = PolyInterval.coerce(upper_gp - lower_gp)
    hessian[1][1] = PolyInterval.coerce(upper_gp - lower_gp)
    hessian[0][1] = PolyInterval.coerce(upper_gp + lower_gp)
    hessian[1][0] = hessian[0][1]
    return PolyInterval.coerce(center_value), Jet2(
        PolyInterval.coerce(value_range), gradient, hessian
    )


def moment_taylor(
    certificate: AnnularMomentCertificate,
    moment_power: int,
    radius_r: Interval,
    radius_s: Interval,
    point_value: bool,
) -> Taylor2D4:
    summed = radius_r + radius_s
    difference = radius_s - radius_r
    primitive = (
        certificate.primitive_point if point_value else certificate.primitive_range
    )
    value = primitive(summed, moment_power) - primitive(difference, moment_power)
    gu, gpu, gppu, g3u = certificate.integrand_derivatives(
        summed, moment_power
    )
    gv, gpv, gppv, g3v = certificate.integrand_derivatives(
        difference, moment_power
    )
    return Taylor2D4(
        {
            (0, 0): PolyInterval.coerce(value),
            (1, 0): PolyInterval.coerce(gu + gv),
            (0, 1): PolyInterval.coerce(gu - gv),
            (2, 0): PolyInterval.coerce((gpu - gpv) / 2),
            (1, 1): PolyInterval.coerce(gpu + gpv),
            (0, 2): PolyInterval.coerce((gpu - gpv) / 2),
            (3, 0): PolyInterval.coerce((gppu + gppv) / 6),
            (2, 1): PolyInterval.coerce((gppu - gppv) / 2),
            (1, 2): PolyInterval.coerce((gppu + gppv) / 2),
            (0, 3): PolyInterval.coerce((gppu - gppv) / 6),
            (4, 0): PolyInterval.coerce((g3u - g3v) / 24),
            (3, 1): PolyInterval.coerce((g3u + g3v) / 6),
            (2, 2): PolyInterval.coerce((g3u - g3v) / 4),
            (1, 3): PolyInterval.coerce((g3u + g3v) / 6),
            (0, 4): PolyInterval.coerce((g3u - g3v) / 24),
        }
    )


def integrate_coefficients_moment_midpoint(
    radial_cells: list[RadialCell],
    cutoff: CutoffCertificate,
    annular: AnnularAngularKernel,
    moments: AnnularMomentCertificate,
    generic_function,
    core_function,
    progress,
) -> tuple[list[Interval], dict[str, object]]:
    total = [Interval.exact_integer(0) for _ in range(4)]
    pi_interval = Interval(*arb_float_bounds(arb.pi()))
    cell_count = len(radial_cells)
    first_non_core = next(
        index for index, cell in enumerate(radial_cells) if cell.role != "fixed-core"
    )
    midpoint_data = [radial_cell_profile_data(cell, cutoff, True) for cell in radial_cells]
    range_data = [radial_cell_profile_data(cell, cutoff, False) for cell in radial_cells]
    widths_fraction = [cell.upper - cell.lower for cell in radial_cells]
    widths = [Interval.from_fraction(value) for value in widths_fraction]
    midpoint_fraction = [(cell.lower + cell.upper) / 2 for cell in radial_cells]
    midpoint_intervals = [Interval.from_fraction(value) for value in midpoint_fraction]
    evaluated_boxes = 0
    maximum_remainder = [0.0] * 4
    for left_index, left in enumerate(radial_cells):
        right_start = first_non_core if left.role == "fixed-core" else left_index
        indices = np.arange(right_start, cell_count)
        if not indices.size:
            continue
        left_range = cell_interval(left.lower, left.upper)
        right_range = Interval(
            np.asarray([fraction_float_bounds(radial_cells[int(i)].lower)[0] for i in indices]),
            np.asarray([fraction_float_bounds(radial_cells[int(i)].upper)[1] for i in indices]),
        )
        left_center = midpoint_intervals[left_index]
        right_center = Interval(
            np.asarray([float(midpoint_intervals[int(i)].lower) for i in indices]),
            np.asarray([float(midpoint_intervals[int(i)].upper) for i in indices]),
        )
        right_midpoint_data = vector_profile_data(midpoint_data, indices)
        right_range_data = vector_profile_data(range_data, indices)
        moment_centers: list[PolyInterval] = []
        moment_jets: list[Jet2] = []
        for moment_power in ANNULAR_POWERS:
            center, jet = moment_jet(
                moments,
                moment_power,
                left_range,
                right_range,
                left_center,
                right_center,
            )
            moment_centers.append(center)
            moment_jets.append(jet)
        left_center_fields = midpoint_data[left_index][0]
        right_center_fields = right_midpoint_data[0]
        if left.role == "fixed-core":
            center_value = core_function(
                PolyInterval.coerce(left_center),
                PolyInterval.coerce(right_center),
                *right_center_fields,
                *moment_centers,
            )
        else:
            center_value = generic_function(
                PolyInterval.coerce(left_center),
                PolyInterval.coerce(right_center),
                *left_center_fields,
                *right_center_fields,
                *moment_centers,
            )
        left_radius_jet = Jet2.variable(left_range, 0)
        right_radius_jet = Jet2.variable(right_range, 1)
        left_field_jets = [field_jet(range_data[left_index], field, 0) for field in range(3)]
        right_field_jets = [field_jet(right_range_data, field, 1) for field in range(3)]
        if left.role == "fixed-core":
            box_value = core_function(
                left_radius_jet,
                right_radius_jet,
                *right_field_jets,
                *moment_jets,
            )
        else:
            box_value = generic_function(
                left_radius_jet,
                right_radius_jet,
                *left_field_jets,
                *right_field_jets,
                *moment_jets,
            )
        width_r = float(widths_fraction[left_index])
        width_s = np.asarray([float(widths_fraction[int(i)]) for i in indices])
        multipliers = np.full(indices.size, 2)
        if right_start == left_index:
            multipliers[0] = 1
        area = Interval(
            np.asarray([
                float((widths[left_index] * widths[int(index)] * Interval.exact_integer(int(multipliers[pos]))).lower)
                for pos, index in enumerate(indices)
            ]),
            np.asarray([
                float((widths[left_index] * widths[int(index)] * Interval.exact_integer(int(multipliers[pos]))).upper)
                for pos, index in enumerate(indices)
            ]),
        )
        for degree in range(4):
            rr = interval_absolute_maximum(polynomial_coefficient(box_value.hessian[0][0], degree))
            ss = interval_absolute_maximum(polynomial_coefficient(box_value.hessian[1][1], degree))
            rs = interval_absolute_maximum(polynomial_coefficient(box_value.hessian[0][1], degree))
            remainder = up(rr * width_r**2 / 24 + ss * width_s**2 / 24 + rs * width_r * width_s / 16)
            maximum_remainder[degree] = max(maximum_remainder[degree], float(np.max(remainder)))
            enclosed = polynomial_coefficient(center_value, degree) + Interval(-remainder, remainder)
            boxes = enclosed * area * pi_interval
            row = Interval(
                math.nextafter(math.fsum(float(item) for item in boxes.lower), NEGATIVE_INFINITY),
                math.nextafter(math.fsum(float(item) for item in boxes.upper), POSITIVE_INFINITY),
            )
            total[degree] = total[degree] + row
        evaluated_boxes += indices.size
        if progress is not None and (
            left_index == 0
            or (left_index + 1) % max(1, cell_count // 20) == 0
            or left_index + 1 == cell_count
        ):
            record = {
                "timestampUtc": datetime.now(timezone.utc).isoformat(),
                "event": "moment-midpoint-progress",
                "annulus": annular.index,
                "rowsComplete": left_index + 1,
                "rows": cell_count,
                "evaluatedRadialBoxes": evaluated_boxes,
                "coefficientIntervals": [value.scalar() for value in total],
            }
            progress.write(json.dumps(record, sort_keys=True) + "\n")
            progress.flush()
            print(json.dumps(record, sort_keys=True), flush=True)
    return total, {
        "rule": "exact angular moment reduction plus radial midpoint with interval-Hessian remainder",
        "radialCells": cell_count,
        "momentPrimitivePower": moments.power,
        "momentPrimitiveCells": moments.cells,
        "evaluatedRadialBoxes": evaluated_boxes,
        "maximumPointwiseMidpointRemainders": maximum_remainder,
        "skippedCoreCoreBoxes": first_non_core * (first_non_core + 1) // 2,
    }


def integrate_coefficients_moment_taylor4(
    radial_cells: list[RadialCell],
    cutoff: CutoffCertificate,
    annular: AnnularAngularKernel,
    moments: AnnularMomentCertificate,
    generic_function,
    core_function,
    progress,
    worker_index: int = 0,
    workers: int = 1,
) -> tuple[list[Interval], dict[str, object]]:
    """Radial cubature using cubic cancellation and a fourth-order bound."""
    total = [Interval.exact_integer(0) for _ in range(4)]
    pi_interval = Interval(*arb_float_bounds(arb.pi()))
    cell_count = len(radial_cells)
    first_non_core = next(
        index for index, cell in enumerate(radial_cells) if cell.role != "fixed-core"
    )
    midpoint_data = [radial_cell_profile_data(cell, cutoff, True) for cell in radial_cells]
    range_data = [radial_cell_profile_data(cell, cutoff, False) for cell in radial_cells]
    widths_fraction = [cell.upper - cell.lower for cell in radial_cells]
    widths = [Interval.from_fraction(value) for value in widths_fraction]
    midpoint_intervals = [
        Interval.from_fraction((cell.lower + cell.upper) / 2)
        for cell in radial_cells
    ]
    evaluated_boxes = 0
    maximum_remainder = [0.0] * 4
    assigned_rows = list(range(worker_index, cell_count, workers))
    for completed_rows, left_index in enumerate(assigned_rows, start=1):
        left = radial_cells[left_index]
        right_start = first_non_core if left.role == "fixed-core" else left_index
        indices = np.arange(right_start, cell_count)
        if not indices.size:
            continue
        left_range = cell_interval(left.lower, left.upper)
        right_range = Interval(
            np.asarray([fraction_float_bounds(radial_cells[int(i)].lower)[0] for i in indices]),
            np.asarray([fraction_float_bounds(radial_cells[int(i)].upper)[1] for i in indices]),
        )
        left_center = midpoint_intervals[left_index]
        right_center = Interval(
            np.asarray([float(midpoint_intervals[int(i)].lower) for i in indices]),
            np.asarray([float(midpoint_intervals[int(i)].upper) for i in indices]),
        )
        right_midpoint_data = vector_profile_data(midpoint_data, indices)
        right_range_data = vector_profile_data(range_data, indices)
        center_moments = [
            moment_taylor(moments, power, left_center, right_center, True)
            for power in ANNULAR_POWERS
        ]
        range_moments = [
            moment_taylor(moments, power, left_range, right_range, False)
            for power in ANNULAR_POWERS
        ]
        left_center_radius = radius_taylor(left_center, 0)
        right_center_radius = radius_taylor(right_center, 1)
        left_range_radius = radius_taylor(left_range, 0)
        right_range_radius = radius_taylor(right_range, 1)
        left_center_fields = [
            profile_taylor(midpoint_data[left_index], field, 0)
            for field in range(3)
        ]
        right_center_fields = [
            profile_taylor(right_midpoint_data, field, 1)
            for field in range(3)
        ]
        left_range_fields = [
            profile_taylor(range_data[left_index], field, 0)
            for field in range(3)
        ]
        right_range_fields = [
            profile_taylor(right_range_data, field, 1)
            for field in range(3)
        ]
        if left.role == "fixed-core":
            center_value = core_function(
                left_center_radius,
                right_center_radius,
                *right_center_fields,
                *center_moments,
            )
            range_value = core_function(
                left_range_radius,
                right_range_radius,
                *right_range_fields,
                *range_moments,
            )
        else:
            center_value = generic_function(
                left_center_radius,
                right_center_radius,
                *left_center_fields,
                *right_center_fields,
                *center_moments,
            )
            range_value = generic_function(
                left_range_radius,
                right_range_radius,
                *left_range_fields,
                *right_range_fields,
                *range_moments,
            )
        width_r = float(widths_fraction[left_index])
        width_s = np.asarray([float(widths_fraction[int(i)]) for i in indices])
        multipliers = np.full(indices.size, 2)
        if right_start == left_index:
            multipliers[0] = 1
        area = Interval(
            np.asarray([
                float((widths[left_index] * widths[int(index)] * Interval.exact_integer(int(multipliers[pos]))).lower)
                for pos, index in enumerate(indices)
            ]),
            np.asarray([
                float((widths[left_index] * widths[int(index)] * Interval.exact_integer(int(multipliers[pos]))).upper)
                for pos, index in enumerate(indices)
            ]),
        )
        for degree in range(4):
            average = polynomial_coefficient(center_value.coefficient(0, 0), degree)
            average = average + polynomial_coefficient(
                center_value.coefficient(2, 0), degree
            ) * Interval.from_number(width_r**2 / 12.0)
            average = average + polynomial_coefficient(
                center_value.coefficient(0, 2), degree
            ) * Interval.from_number(width_s**2 / 12.0)
            c40 = interval_absolute_maximum(
                polynomial_coefficient(range_value.coefficient(4, 0), degree)
            )
            c31 = interval_absolute_maximum(
                polynomial_coefficient(range_value.coefficient(3, 1), degree)
            )
            c22 = interval_absolute_maximum(
                polynomial_coefficient(range_value.coefficient(2, 2), degree)
            )
            c13 = interval_absolute_maximum(
                polynomial_coefficient(range_value.coefficient(1, 3), degree)
            )
            c04 = interval_absolute_maximum(
                polynomial_coefficient(range_value.coefficient(0, 4), degree)
            )
            remainder = up(
                c40 * width_r**4 / 80.0
                + c31 * width_r**3 * width_s / 128.0
                + c22 * width_r**2 * width_s**2 / 144.0
                + c13 * width_r * width_s**3 / 128.0
                + c04 * width_s**4 / 80.0
            )
            maximum_remainder[degree] = max(maximum_remainder[degree], float(np.max(remainder)))
            enclosed = average + Interval(-remainder, remainder)
            boxes = enclosed * area * pi_interval
            row = Interval(
                math.nextafter(math.fsum(float(item) for item in boxes.lower), NEGATIVE_INFINITY),
                math.nextafter(math.fsum(float(item) for item in boxes.upper), POSITIVE_INFINITY),
            )
            total[degree] = total[degree] + row
        evaluated_boxes += indices.size
        if progress is not None and (
            completed_rows == 1
            or completed_rows % max(1, len(assigned_rows) // 20) == 0
            or completed_rows == len(assigned_rows)
        ):
            record = {
                "timestampUtc": datetime.now(timezone.utc).isoformat(),
                "event": "moment-taylor4-progress",
                "annulus": annular.index,
                "rowsComplete": completed_rows,
                "rows": len(assigned_rows),
                "workerIndex": worker_index,
                "workers": workers,
                "evaluatedRadialBoxes": evaluated_boxes,
                "coefficientIntervals": [value.scalar() for value in total],
            }
            progress.write(json.dumps(record, sort_keys=True) + "\n")
            progress.flush()
            print(json.dumps(record, sort_keys=True), flush=True)
    return total, {
        "rule": (
            "exact angular moments plus integrated Hessian, exact cubic "
            "parity cancellation, and fourth-order Taylor remainder"
        ),
        "radialCells": cell_count,
        "assignedRows": len(assigned_rows),
        "workerIndex": worker_index,
        "workers": workers,
        "momentPrimitivePower": moments.power,
        "momentPrimitiveCells": moments.cells,
        "evaluatedRadialBoxes": evaluated_boxes,
        "maximumPointwiseFourthOrderRemainders": maximum_remainder,
        "skippedCoreCoreBoxes": first_non_core * (first_non_core + 1) // 2,
    }


def vector_profile(
    radial_cells: list[RadialCell], indices: np.ndarray, field: str
) -> PolyInterval:
    profiles = [getattr(radial_cells[int(index)], field) for index in indices]
    return PolyInterval(
        Interval(
            np.asarray(
                [
                    profile.coefficients[degree].lower
                    if degree < len(profile.coefficients)
                    else 0.0
                    for profile in profiles
                ]
            ),
            np.asarray(
                [
                    profile.coefficients[degree].upper
                    if degree < len(profile.coefficients)
                    else 0.0
                    for profile in profiles
                ]
            ),
        )
        for degree in range(2)
    )


def centered_vector_profile(
    radial_cells: list[RadialCell], indices: np.ndarray, field: str
) -> CenteredPoly:
    ordinary = vector_profile(radial_cells, indices, field)
    return CenteredPoly(
        CenteredInterval.from_interval(value) for value in ordinary.coefficients
    )


def hull_zero_on_mask(value: PolyInterval, mask: np.ndarray) -> PolyInterval:
    return PolyInterval(
        Interval(
            np.where(mask, np.minimum(coefficient.lower, 0.0), coefficient.lower),
            np.where(mask, np.maximum(coefficient.upper, 0.0), coefficient.upper),
        )
        for coefficient in value.coefficients
    )


def centered_hull_zero_on_mask(
    value: CenteredPoly, mask: np.ndarray
) -> list[Interval]:
    result: list[Interval] = []
    for coefficient in value.coefficients:
        enclosed = coefficient.range()
        result.append(
            Interval(
                np.where(mask, np.minimum(enclosed.lower, 0.0), enclosed.lower),
                np.where(mask, np.maximum(enclosed.upper, 0.0), enclosed.upper),
            )
        )
    return result


def integrate_coefficients_direct(
    radial_cells: list[RadialCell],
    annular: AnnularAngularKernel,
    direct_function,
    direct_core_function,
    angular_cells: int,
    progress,
) -> tuple[list[Interval], dict[str, object]]:
    """Integrate the unsplit angular kernel by outward-rounded boxes.

    Keeping the polynomial in t intact is essential: separately enclosing the
    five distance moments destroys a removable analytic cancellation near the
    diagonal r=s.  This routine is mathematically equivalent to that exact
    reduction, but performs interval evaluation before the cancellation is
    split.
    """

    total = [Interval.exact_integer(0) for _ in range(4)]
    pi_interval = Interval(*arb_float_bounds(arb.pi()))
    maximum_box_width = [0.0] * 4
    evaluated_boxes = 0
    skipped_core_boxes = 0
    active_angular_boxes = 0
    partial_support_boxes = 0
    cell_count = len(radial_cells)
    first_non_core = next(
        index for index, cell in enumerate(radial_cells) if cell.role != "fixed-core"
    )
    lower_float = np.asarray(
        [fraction_float_bounds(cell.lower)[0] for cell in radial_cells]
    )
    upper_float = np.asarray(
        [fraction_float_bounds(cell.upper)[1] for cell in radial_cells]
    )
    widths = [
        Interval.from_fraction(cell.upper - cell.lower) for cell in radial_cells
    ]
    angular_width = Interval.from_fraction(Fraction(2, angular_cells))

    for left_index, left in enumerate(radial_cells):
        if left.role == "fixed-core":
            skipped_core_boxes += max(0, first_non_core - left_index)
            right_start = first_non_core
        else:
            right_start = left_index
        if right_start >= cell_count:
            continue
        indices = np.arange(right_start, cell_count)
        right_lower = lower_float[indices]
        right_upper = upper_float[indices]
        left_radius_interval = cell_interval(left.lower, left.upper)
        right_radius_interval = Interval(right_lower, right_upper)
        left_radius = CenteredPoly(
            (CenteredInterval.from_interval(left_radius_interval),)
        )
        right_radius = CenteredPoly(
            (CenteredInterval.from_interval(right_radius_interval),)
        )
        left_p = CenteredPoly(
            CenteredInterval.from_interval(value) for value in left.p.coefficients
        )
        left_q = CenteredPoly(
            CenteredInterval.from_interval(value) for value in left.q.coefficients
        )
        left_r = CenteredPoly(
            CenteredInterval.from_interval(value) for value in left.r.coefficients
        )
        right_p = centered_vector_profile(radial_cells, indices, "p")
        right_q = centered_vector_profile(radial_cells, indices, "q")
        right_r = centered_vector_profile(radial_cells, indices, "r")
        angular_total = [
            Interval(np.zeros(indices.size), np.zeros(indices.size))
            for _ in range(4)
        ]

        for angular_index in range(angular_cells):
            t_lower = Fraction(-1) + Fraction(2 * angular_index, angular_cells)
            t_upper = Fraction(-1) + Fraction(
                2 * (angular_index + 1), angular_cells
            )
            t_interval = cell_interval(t_lower, t_upper)
            distance_squared = (
                left_radius_interval * left_radius_interval
                + right_radius_interval * right_radius_interval
                - 2
                * left_radius_interval
                * right_radius_interval
                * t_interval
            )
            distance_squared = Interval(
                np.maximum(distance_squared.lower, 0.0),
                np.maximum(distance_squared.upper, 0.0),
            )
            distance = distance_squared.sqrt()
            clipped_distance, psi, partial = annular.enclose(distance)
            active = psi.upper > 0.0
            active_angular_boxes += int(np.count_nonzero(active))
            partial_support_boxes += int(np.count_nonzero(partial))
            t_polynomial = CenteredPoly(
                (CenteredInterval.from_interval(t_interval),)
            )
            distance_polynomial = CenteredPoly(
                (CenteredInterval.from_interval(clipped_distance),)
            )
            if left.role == "fixed-core":
                value = direct_core_function(
                    left_radius,
                    right_radius,
                    t_polynomial,
                    distance_polynomial,
                    right_p,
                    right_q,
                    right_r,
                )
            else:
                value = direct_function(
                    left_radius,
                    right_radius,
                    t_polynomial,
                    distance_polynomial,
                    left_p,
                    left_q,
                    left_r,
                    right_p,
                    right_q,
                    right_r,
                )
            enclosed_coefficients = centered_hull_zero_on_mask(
                value
                * CenteredPoly((CenteredInterval.from_interval(psi),)),
                partial,
            )
            for degree in range(4):
                coefficient = (
                    enclosed_coefficients[degree]
                    if degree < len(enclosed_coefficients)
                    else Interval.exact_integer(0)
                )
                angular_total[degree] = (
                    angular_total[degree] + coefficient * angular_width
                )

        multipliers = np.full(indices.size, 2)
        if right_start == left_index:
            multipliers[0] = 1
        area = Interval(
            np.asarray(
                [
                    float(
                        (
                            widths[left_index]
                            * widths[int(index)]
                            * Interval.exact_integer(int(multipliers[position]))
                        ).lower
                    )
                    for position, index in enumerate(indices)
                ]
            ),
            np.asarray(
                [
                    float(
                        (
                            widths[left_index]
                            * widths[int(index)]
                            * Interval.exact_integer(int(multipliers[position]))
                        ).upper
                    )
                    for position, index in enumerate(indices)
                ]
            ),
        )
        for degree in range(4):
            boxes = angular_total[degree] * area * pi_interval
            row = Interval(
                math.nextafter(
                    math.fsum(float(item) for item in boxes.lower),
                    NEGATIVE_INFINITY,
                ),
                math.nextafter(
                    math.fsum(float(item) for item in boxes.upper),
                    POSITIVE_INFINITY,
                ),
            )
            total[degree] = total[degree] + row
            maximum_box_width[degree] = max(
                maximum_box_width[degree],
                float(np.max(boxes.upper - boxes.lower)),
            )
        evaluated_boxes += indices.size
        if progress is not None and (
            left_index == 0
            or (left_index + 1) % max(1, cell_count // 20) == 0
            or left_index + 1 == cell_count
        ):
            record = {
                "timestampUtc": datetime.now(timezone.utc).isoformat(),
                "event": "radial-progress",
                "annulus": annular.index,
                "rowsComplete": left_index + 1,
                "rows": cell_count,
                "angularCells": angular_cells,
                "evaluatedRadialBoxes": evaluated_boxes,
                "activeAngularBoxes": active_angular_boxes,
                "coefficientIntervals": [value.scalar() for value in total],
            }
            progress.write(json.dumps(record, sort_keys=True) + "\n")
            progress.flush()
            print(json.dumps(record, sort_keys=True), flush=True)
    return total, {
        "radialCells": cell_count,
        "angularCells": angular_cells,
        "evaluatedRadialBoxes": evaluated_boxes,
        "activeAngularBoxes": active_angular_boxes,
        "partialSupportAngularBoxes": partial_support_boxes,
        "skippedCoreCoreBoxes": skipped_core_boxes,
        "maximumSingleBoxWidths": maximum_box_width,
    }


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--raw-moment-power", type=int, default=17)
    parser.add_argument("--cutoff-cells", type=int, default=512)
    parser.add_argument("--moment-power", type=int, default=16)
    parser.add_argument("--core-cells", type=int, default=128)
    parser.add_argument("--plateau-cells", type=int, default=256)
    parser.add_argument("--boundary-refinement", type=int, default=1)
    parser.add_argument("--arb-precision", type=int, default=160)
    parser.add_argument("--source-commit")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--worker-index", type=int, default=0)
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    if arguments.workers < 1:
        raise SystemExit("--workers must be positive")
    if not 0 <= arguments.worker_index < arguments.workers:
        raise SystemExit("--worker-index must lie in [0, workers)")
    started = time.perf_counter()
    ctx.prec = arguments.arb_precision
    head_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if arguments.source_commit is not None and arguments.source_commit != head_commit:
        raise SystemExit(
            f"source commit mismatch: requested {arguments.source_commit}, HEAD is {head_commit}"
        )
    output_root = arguments.output_root
    output_root.mkdir(parents=True, exist_ok=True)
    progress_path = output_root / "progress.ndjson"
    with progress_path.open("w", encoding="utf-8") as progress:
        raw = RawMomentTable(arguments.raw_moment_power)
        cutoff = CutoffCertificate(raw, arguments.cutoff_cells)
        (
            generic_function,
            core_function,
            direct_function,
            direct_core_function,
            symbolic_audits,
        ) = derive_radial_functions()
        if arguments.boundary_refinement < 1:
            raise SystemExit("--boundary-refinement must be positive")
        radial_cells = build_radial_cells(
            cutoff,
            arguments.core_cells,
            arguments.plateau_cells,
            arguments.boundary_refinement,
        )
        setup_record = {
            "timestampUtc": datetime.now(timezone.utc).isoformat(),
            "event": "setup-complete",
            "elapsedSeconds": time.perf_counter() - started,
            "radialCells": len(radial_cells),
            "normalizationInterval": raw.normalization.scalar(),
            "symbolicAudits": symbolic_audits,
        }
        progress.write(json.dumps(setup_record, sort_keys=True) + "\n")
        progress.flush()
        print(json.dumps(setup_record, sort_keys=True), flush=True)

        results: dict[str, list[Interval]] = {}
        integration_audits: dict[str, object] = {}
        for index in (0, -2):
            annular = AnnularAngularKernel(cutoff, index)
            moment_certificate = AnnularMomentCertificate(
                cutoff, annular, arguments.moment_power
            )
            coefficients, audit = integrate_coefficients_moment_taylor4(
                radial_cells,
                cutoff,
                annular,
                moment_certificate,
                generic_function,
                core_function,
                progress,
                arguments.worker_index,
                arguments.workers,
            )
            results[str(index)] = coefficients
            integration_audits[str(index)] = audit

    j0 = results["0"]
    jm2 = results["-2"]
    c1, c2, c3 = j0[1], j0[2], j0[3]
    discriminant = c2 * c2 - 4 * c1 * c3
    endpoint = jm2[0]
    is_partial = arguments.workers > 1
    passed = bool(
        float(j0[0].lower) <= 0.0 <= float(j0[0].upper)
        and float(c3.upper) < 0.0
        and float(discriminant.upper) < 0.0
        and float(endpoint.upper) < 0.0
    )
    result = {
        "schemaVersion": "1.0",
        "release": "R0.69W",
        "status": "partial" if is_partial else ("passed" if passed else "failed"),
        "claimBoundary": (
            "rigorous static sign obstruction for the declared separation-four "
            "two-scale family; no dynamical propagation or Navier-Stokes "
            "regularity conclusion"
        ),
        "method": {
            "rawMomentPower": arguments.raw_moment_power,
            "rawMomentCells": 1 << arguments.raw_moment_power,
            "cutoffCells": arguments.cutoff_cells,
            "momentPower": arguments.moment_power,
            "momentCells": 1 << arguments.moment_power,
            "coreCells": arguments.core_cells,
            "plateauCells": arguments.plateau_cells,
            "boundaryRefinement": arguments.boundary_refinement,
            "arbPrecisionBits": arguments.arb_precision,
            "workers": arguments.workers,
            "workerIndex": arguments.worker_index,
            "epsilon": 0.25,
            "annuli": [0, -2],
            "intervalRule": (
                "Arb transcendental endpoints plus outward-rounded binary64 "
                "validated trapezoidal distance primitives and radial "
                "midpoint-Hessian boxes with exact cubic parity cancellation "
                "and a fourth-order remainder"
            ),
            "maximumCertifiedCutoffDerivativeOrder": 6,
        },
        "mollifier": {
            "baseTransition": ["1/20", "19/20"],
            "radius": "1/40",
            "normalizationInterval": raw.normalization.scalar(),
            "criticalBlocks": raw.critical_blocks,
            "trueConvolutionCertified": True,
            "floatingQuadratureNodesUsed": 0,
            "endpointDistributionTermsThroughOrderFive": True,
            "endpointDistributionTermsThroughOrderSix": True,
        },
        "symbolicAudits": symbolic_audits,
        "integrationAudits": integration_audits,
        "coefficientIntervals": {
            "j0": {
                f"c{degree}": interval.scalar()
                for degree, interval in enumerate(j0)
            },
            "jMinus2": {
                f"c{degree}": interval.scalar()
                for degree, interval in enumerate(jm2)
            },
        },
        "decision": {
            "j0ConstantContainsExactZero": bool(
                float(j0[0].lower) <= 0.0 <= float(j0[0].upper)
            ),
            "j0LeadingCoefficientStrictlyNegative": bool(float(c3.upper) < 0.0),
            "j0QuadraticDiscriminantInterval": discriminant.scalar(),
            "j0QuadraticDiscriminantStrictlyNegative": bool(
                float(discriminant.upper) < 0.0
            ),
            "jMinus2AtZeroInterval": endpoint.scalar(),
            "jMinus2AtZeroStrictlyNegative": bool(float(endpoint.upper) < 0.0),
            "allPositiveAmplitudesHaveNegativeJ0": bool(
                float(c3.upper) < 0.0 and float(discriminant.upper) < 0.0
            ),
            "endpointHasNegativeJMinus2": bool(float(endpoint.upper) < 0.0),
            "entireAmplitudeFamilyExcluded": passed,
        },
        "provenance": {
            "script": str(Path(__file__).resolve().relative_to(Path.cwd())),
            "scriptSha256": sha256(Path(__file__).resolve()),
            "sourceCommit": head_commit,
            "requestedSourceCommit": arguments.source_commit,
            "sourceTreeDirty": bool(
                subprocess.run(
                    ["git", "status", "--porcelain"],
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout.strip()
            ),
            "python": sys.version,
            "pythonFlint": __import__("flint").__version__,
            "numpy": np.__version__,
            "sympy": sp.__version__,
            "platform": platform.platform(),
        },
        "runtime": {
            "elapsedSeconds": time.perf_counter() - started,
        },
        "partial": {
            "enabled": is_partial,
            "workers": arguments.workers,
            "workerIndex": arguments.worker_index,
            "mustBeMergedBeforeDecision": is_partial,
        },
    }
    result_path = output_root / "result.json"
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["decision"], indent=2, sort_keys=True), flush=True)
    print(
        json.dumps(
            {
                "status": result["status"],
                "elapsedSeconds": result["runtime"]["elapsedSeconds"],
                "result": str(result_path),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if is_partial or passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
