#!/usr/bin/env python3
"""Rigorous Arb ODE core for the R0.73J periodic Evans certificate.

The autonomous state contains ``sin(x)``, ``cos(x)``, ``sin(2x)``,
``cos(2x)`` and the two columns of the fundamental matrix.  Each step uses
an explicitly verified convex Picard tube and a normalized Taylor remainder.
All arithmetic is performed by python-flint/Arb; binary64 values never enter
the proof path.

This module contains no contour or theorem decisions.  The release driver is
``experiments/r073j/certify_contours.py``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from flint import acb, arb


@dataclass
class IntegrationAudit:
    """Worst-case inclusion data accumulated over one monodromy solve."""

    minimum_denominator_lower: arb | None = None
    minimum_component_slack: arb | None = None
    maximum_picard_attempt: int = 0
    step_count: int = 0

    def observe_denominator(self, value: arb) -> None:
        if self.minimum_denominator_lower is None or value < self.minimum_denominator_lower:
            self.minimum_denominator_lower = value

    def observe_slack(self, value: arb) -> None:
        if self.minimum_component_slack is None or value < self.minimum_component_slack:
            self.minimum_component_slack = value


def hull(left: acb, right: acb) -> acb:
    return acb(left.real.union(right.real), left.imag.union(right.imag))


def inflate(value: acb, factor: int, absolute: arb) -> acb:
    return acb(
        arb(value.real.mid(), factor * value.real.rad() + absolute),
        arb(value.imag.mid(), factor * value.imag.rad() + absolute),
    )


def vector_hull(left: Sequence[acb], right: Sequence[acb]) -> list[acb]:
    return [hull(a, b) for a, b in zip(left, right)]


def vector_contains(outer: Sequence[acb], inner: Sequence[acb]) -> bool:
    return all(a.contains(b) for a, b in zip(outer, inner))


def component_slack(outer: acb, inner: acb) -> arb:
    """Return a rigorous lower bound for the four endpoint clearances."""
    clearances = (
        inner.real.lower() - outer.real.lower(),
        outer.real.upper() - inner.real.upper(),
        inner.imag.lower() - outer.imag.lower(),
        outer.imag.upper() - inner.imag.upper(),
    )
    return min(clearances)


def state_rhs(state: Sequence[acb], d: arb, spectral: acb) -> list[acb]:
    sin_x, cos_x, sin_2x, cos_2x = state[:4]
    exp_one = (-d).exp()
    exp_four = (-4 * d).exp()
    velocity = -exp_one * sin_x / 2 + exp_four * sin_2x / 4
    velocity_xx = exp_one * sin_x / 2 - exp_four * sin_2x
    denominator = velocity - 2j * spectral
    if denominator.abs_lower() <= 0:
        raise ZeroDivisionError("Rayleigh denominator enclosure contains zero")
    potential = arb(1) / 4 + velocity_xx / denominator
    result = [cos_x, -sin_x, 2 * cos_2x, -2 * sin_2x]
    for offset in (4, 6):
        value, derivative = state[offset:offset + 2]
        result.extend([derivative, potential * value])
    return result


def series_add(left: Sequence[acb], right: Sequence[acb]) -> list[acb]:
    return [a + b for a, b in zip(left, right)]


def series_scale(values: Sequence[acb], factor: acb | arb | int) -> list[acb]:
    return [factor * value for value in values]


def series_multiply(
    left: Sequence[acb],
    right: Sequence[acb],
    degree: int,
) -> list[acb]:
    result = [acb(0) for _ in range(degree + 1)]
    for order in range(degree + 1):
        result[order] = sum(
            (left[index] * right[order - index] for index in range(order + 1)),
            acb(0),
        )
    return result


def series_reciprocal(values: Sequence[acb], degree: int) -> list[acb]:
    if values[0].contains(0):
        raise ZeroDivisionError("series constant coefficient contains zero")
    result = [acb(0) for _ in range(degree + 1)]
    result[0] = 1 / values[0]
    for order in range(1, degree + 1):
        total = sum(
            (values[index] * result[order - index]
             for index in range(1, order + 1)),
            acb(0),
        )
        result[order] = -result[0] * total
    return result


def series_divide(
    numerator: Sequence[acb],
    denominator: Sequence[acb],
    degree: int,
) -> list[acb]:
    return series_multiply(
        numerator,
        series_reciprocal(denominator, degree),
        degree,
    )


def normalized_taylor_coefficients(
    initial: Sequence[acb],
    d: arb,
    spectral: acb,
    degree: int,
    audit: IntegrationAudit | None = None,
) -> list[list[acb]]:
    """Return normalized time-Taylor coefficients through ``degree``.

    When ``initial`` is an interval tube, the coefficient of order ``r``
    encloses ``y^(r)/r!`` at every state in that tube.  This is the quantity
    used in the Lagrange remainder of :func:`validated_step`.
    """
    coefficients = [
        [acb(0) for _ in range(degree + 1)] for _ in initial
    ]
    for index, value in enumerate(initial):
        coefficients[index][0] = value

    exp_one = (-d).exp()
    exp_four = (-4 * d).exp()
    for order in range(degree):
        coefficients[0][order + 1] = coefficients[1][order] / (order + 1)
        coefficients[1][order + 1] = -coefficients[0][order] / (order + 1)
        coefficients[2][order + 1] = 2 * coefficients[3][order] / (order + 1)
        coefficients[3][order + 1] = -2 * coefficients[2][order] / (order + 1)

    sin_x = coefficients[0]
    sin_2x = coefficients[2]
    velocity = series_add(
        series_scale(sin_x, -exp_one / 2),
        series_scale(sin_2x, exp_four / 4),
    )
    velocity_xx = series_add(
        series_scale(sin_x, exp_one / 2),
        series_scale(sin_2x, -exp_four),
    )
    denominator = list(velocity)
    denominator[0] -= 2j * spectral
    denominator_lower = denominator[0].abs_lower()
    if denominator_lower <= 0:
        raise ZeroDivisionError("Taylor Rayleigh denominator contains zero")
    if audit is not None:
        audit.observe_denominator(denominator_lower)
    potential = series_divide(velocity_xx, denominator, degree)
    potential[0] += arb(1) / 4

    for offset in (4, 6):
        solution = [acb(0) for _ in range(degree + 2)]
        solution[0] = initial[offset]
        solution[1] = initial[offset + 1]
        for order in range(degree):
            total = sum(
                (potential[index] * solution[order - index]
                 for index in range(order + 1)),
                acb(0),
            )
            solution[order + 2] = total / ((order + 2) * (order + 1))
        for order in range(degree + 1):
            coefficients[offset][order] = solution[order]
            coefficients[offset + 1][order] = (order + 1) * solution[order + 1]
    return coefficients


def polynomial_evaluate(coefficients: Sequence[acb], value: arb, stop: int) -> acb:
    result = coefficients[stop]
    for index in range(stop - 1, -1, -1):
        result = coefficients[index] + value * result
    return result


def picard_tube(
    initial: Sequence[acb],
    d: arb,
    spectral: acb,
    step_size: arb,
    audit: IntegrationAudit,
    max_attempts: int = 24,
) -> list[acb]:
    """Find a convex interval box containing the complete exact step.

    The accepted box ``B`` is checked to contain both ``X0`` and
    ``X0+h F(B)``.  Since a complex interval box is convex, it then contains
    ``X0+t F(B)`` for every ``0 <= t <= h``.  The denominator check in
    :func:`state_rhs` makes ``F`` analytic on a neighborhood of ``B``.
    """
    euler = [
        value + step_size * derivative
        for value, derivative in zip(initial, state_rhs(initial, d, spectral))
    ]
    base = vector_hull(initial, euler)
    absolute = 64 * step_size * step_size + arb("1e-70")
    for attempt in range(max_attempts):
        factor = 2 ** attempt
        # The trigonometric clock is an independent linear subsystem.  It
        # does not need to inherit the sometimes much larger inflation needed
        # by a growing fundamental-matrix column.  Keeping the first four
        # components tight also prevents an artificial Rayleigh-pole overlap.
        enclosure = [
            inflate(value, 1, absolute) for value in base[:4]
        ] + [
            inflate(value, factor, factor * absolute) for value in base[4:]
        ]
        endpoint_image = [
            value + step_size * derivative
            for value, derivative in zip(
                initial,
                state_rhs(enclosure, d, spectral),
            )
        ]
        if vector_contains(enclosure, initial) and vector_contains(
            enclosure, endpoint_image
        ):
            audit.maximum_picard_attempt = max(
                audit.maximum_picard_attempt,
                attempt,
            )
            for outer, inner in zip(enclosure, initial):
                audit.observe_slack(component_slack(outer, inner))
            for outer, inner in zip(enclosure, endpoint_image):
                audit.observe_slack(component_slack(outer, inner))
            return enclosure
    raise RuntimeError("Picard enclosure did not close")


def validated_step(
    initial: Sequence[acb],
    d: arb,
    spectral: acb,
    step_size: arb,
    order: int,
    audit: IntegrationAudit,
) -> list[acb]:
    enclosure = picard_tube(initial, d, spectral, step_size, audit)
    launch = normalized_taylor_coefficients(
        initial,
        d,
        spectral,
        order - 1,
        audit,
    )
    remainder = normalized_taylor_coefficients(
        enclosure,
        d,
        spectral,
        order,
        audit,
    )
    return [
        polynomial_evaluate(launch[index], step_size, order - 1)
        + step_size ** order * remainder[index][order]
        for index in range(len(initial))
    ]


def monodromy(
    d: arb,
    spectral: acb,
    steps: int,
    order: int,
) -> tuple[list[acb], IntegrationAudit]:
    if steps < 1 or order < 2:
        raise ValueError("steps must be positive and order at least two")
    state = [acb(value) for value in (0, 1, 0, 1, 1, 0, 0, 1)]
    step_size = 2 * arb.pi() / steps
    audit = IntegrationAudit(step_count=steps)
    for _ in range(steps):
        state = validated_step(
            state,
            d,
            spectral,
            step_size,
            order,
            audit,
        )
    return state, audit


def evans(
    d: arb,
    spectral: acb,
    steps: int,
    order: int,
) -> tuple[acb, IntegrationAudit]:
    state, audit = monodromy(d, spectral, steps, order)
    return 2 - state[4] - state[7], audit
