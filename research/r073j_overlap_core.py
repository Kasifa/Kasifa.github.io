#!/usr/bin/env python3
"""Validated real-parameter kinetic-overlap integrator for R0.73J.

For real ``d`` and real ``lambda`` the right Rayleigh solution is initialized
by the periodic-kernel vector ``(M12, 1-M11)``.  The companion

``p = conjugate(phi) / (W + 2 i lambda)``

is the kinetic left potential.  The program encloses the numerator and both
energy norms entering the normalized kinetic pairing.  Complex-parameter
analytic remainders are derived separately in the certificate driver; this
ODE core is used only at real Chebyshev nodes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from flint import acb, arb

from research.r073j_interval_core import (
    IntegrationAudit,
    component_slack,
    hull,
    inflate,
    monodromy,
    polynomial_evaluate,
    series_add,
    series_divide,
    series_multiply,
    series_scale,
    vector_contains,
    vector_hull,
)


@dataclass
class OverlapAudit:
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


def overlap_rhs(state: Sequence[acb], d: arb, eigenvalue: arb) -> list[acb]:
    sin_x, cos_x, sin_2x, cos_2x, phi, phi_x, _, _, _ = state
    exp_one = (-d).exp()
    exp_four = (-4 * d).exp()
    velocity = -exp_one * sin_x / 2 + exp_four * sin_2x / 4
    velocity_x = -exp_one * cos_x / 2 + exp_four * cos_2x / 2
    velocity_xx = exp_one * sin_x / 2 - exp_four * sin_2x
    c_value = acb(0, 2 * eigenvalue)
    right_denominator = velocity - c_value
    left_denominator = velocity + c_value
    if right_denominator.abs_lower() <= 0 or left_denominator.abs_lower() <= 0:
        raise ZeroDivisionError("overlap Rayleigh denominator contains zero")
    potential = arb(1) / 4 + velocity_xx / right_denominator
    left_potential = phi.conjugate() / left_denominator
    left_potential_x = (
        phi_x.conjugate() / left_denominator
        - phi.conjugate() * velocity_x / left_denominator ** 2
    )
    numerator = -velocity_xx * phi ** 2 / right_denominator ** 2
    right_energy = phi_x * phi_x.conjugate() + phi * phi.conjugate() / 4
    left_energy = (
        left_potential_x * left_potential_x.conjugate()
        + left_potential * left_potential.conjugate() / 4
    )
    return [
        cos_x,
        -sin_x,
        2 * cos_2x,
        -2 * sin_2x,
        phi_x,
        potential * phi,
        numerator,
        right_energy,
        left_energy,
    ]


def overlap_taylor_coefficients(
    initial: Sequence[acb],
    d: arb,
    eigenvalue: arb,
    degree: int,
    audit: OverlapAudit,
) -> list[list[acb]]:
    coefficients = [
        [acb(0) for _ in range(degree + 1)] for _ in initial
    ]
    for index, value in enumerate(initial):
        coefficients[index][0] = value

    exp_one = (-d).exp()
    exp_four = (-4 * d).exp()
    c_value = acb(0, 2 * eigenvalue)
    for order in range(degree):
        coefficients[0][order + 1] = coefficients[1][order] / (order + 1)
        coefficients[1][order + 1] = -coefficients[0][order] / (order + 1)
        coefficients[2][order + 1] = 2 * coefficients[3][order] / (order + 1)
        coefficients[3][order + 1] = -2 * coefficients[2][order] / (order + 1)

    sin_x, cos_x, sin_2x, cos_2x = coefficients[:4]
    velocity = series_add(
        series_scale(sin_x, -exp_one / 2),
        series_scale(sin_2x, exp_four / 4),
    )
    velocity_x = series_add(
        series_scale(cos_x, -exp_one / 2),
        series_scale(cos_2x, exp_four / 2),
    )
    velocity_xx = series_add(
        series_scale(sin_x, exp_one / 2),
        series_scale(sin_2x, -exp_four),
    )
    right_denominator = list(velocity)
    right_denominator[0] -= c_value
    left_denominator = list(velocity)
    left_denominator[0] += c_value
    denominator_lower = min(
        right_denominator[0].abs_lower(),
        left_denominator[0].abs_lower(),
    )
    if denominator_lower <= 0:
        raise ZeroDivisionError("overlap Taylor denominator contains zero")
    audit.observe_denominator(denominator_lower)
    potential = series_divide(velocity_xx, right_denominator, degree)
    potential[0] += arb(1) / 4

    solution = [acb(0) for _ in range(degree + 2)]
    solution[0] = initial[4]
    solution[1] = initial[5]
    for order in range(degree):
        total = sum(
            (potential[index] * solution[order - index]
             for index in range(order + 1)),
            acb(0),
        )
        solution[order + 2] = total / ((order + 2) * (order + 1))
    phi = solution[:degree + 1]
    phi_x = [(order + 1) * solution[order + 1]
             for order in range(degree + 1)]
    coefficients[4] = phi
    coefficients[5] = phi_x

    phi_conjugate = [value.conjugate() for value in phi]
    phi_x_conjugate = [value.conjugate() for value in phi_x]
    left_potential = series_divide(
        phi_conjugate, left_denominator, degree
    )
    left_potential_x = [
        (order + 1) * left_potential[order + 1]
        for order in range(degree)
    ] + [acb(0)]
    numerator = series_scale(
        series_divide(
            series_multiply(
                velocity_xx,
                series_multiply(phi, phi, degree),
                degree,
            ),
            series_multiply(
                right_denominator, right_denominator, degree
            ),
            degree,
        ),
        -1,
    )
    right_energy = series_add(
        series_multiply(phi_x, phi_x_conjugate, degree),
        series_scale(
            series_multiply(phi, phi_conjugate, degree),
            arb(1) / 4,
        ),
    )
    left_energy = series_add(
        series_multiply(
            left_potential_x,
            [value.conjugate() for value in left_potential_x],
            degree,
        ),
        series_scale(
            series_multiply(
                left_potential,
                [value.conjugate() for value in left_potential],
                degree,
            ),
            arb(1) / 4,
        ),
    )
    for offset, integrand in zip(
        (6, 7, 8), (numerator, right_energy, left_energy)
    ):
        for order in range(degree):
            coefficients[offset][order + 1] = integrand[order] / (order + 1)
    return coefficients


def overlap_picard_tube(
    initial: Sequence[acb],
    d: arb,
    eigenvalue: arb,
    step_size: arb,
    audit: OverlapAudit,
    max_attempts: int = 24,
) -> list[acb]:
    euler = [
        value + step_size * derivative
        for value, derivative in zip(
            initial, overlap_rhs(initial, d, eigenvalue)
        )
    ]
    base = vector_hull(initial, euler)
    absolute = 64 * step_size * step_size + arb("1e-70")
    for attempt in range(max_attempts):
        factor = 2 ** attempt
        trigonometric = [inflate(value, 1, absolute) for value in base[:4]]
        rayleigh = [
            inflate(value, factor, factor * absolute) for value in base[4:6]
        ]
        trial = trigonometric + rayleigh + base[6:]
        derivatives = overlap_rhs(trial, d, eigenvalue)
        accumulated = [
            inflate(
                hull(initial[index], initial[index] + step_size * derivatives[index]),
                1,
                absolute,
            )
            for index in range(6, 9)
        ]
        enclosure = trigonometric + rayleigh + accumulated
        endpoint_image = [
            value + step_size * derivative
            for value, derivative in zip(
                initial, overlap_rhs(enclosure, d, eigenvalue)
            )
        ]
        if vector_contains(enclosure, initial) and vector_contains(
            enclosure, endpoint_image
        ):
            audit.maximum_picard_attempt = max(
                audit.maximum_picard_attempt, attempt
            )
            for outer, inner in zip(enclosure, initial):
                audit.observe_slack(component_slack(outer, inner))
            for outer, inner in zip(enclosure, endpoint_image):
                audit.observe_slack(component_slack(outer, inner))
            return enclosure
    raise RuntimeError("overlap Picard enclosure did not close")


def overlap_step(
    initial: Sequence[acb],
    d: arb,
    eigenvalue: arb,
    step_size: arb,
    order: int,
    audit: OverlapAudit,
) -> list[acb]:
    enclosure = overlap_picard_tube(
        initial, d, eigenvalue, step_size, audit
    )
    launch = overlap_taylor_coefficients(
        initial, d, eigenvalue, order - 1, audit
    )
    remainder = overlap_taylor_coefficients(
        enclosure, d, eigenvalue, order, audit
    )
    return [
        polynomial_evaluate(launch[index], step_size, order - 1)
        + step_size ** order * remainder[index][order]
        for index in range(len(initial))
    ]


def integrate_overlap(
    d: arb,
    eigenvalue: arb,
    steps: int,
    order: int,
) -> tuple[dict[str, acb], OverlapAudit, IntegrationAudit]:
    matrix, monodromy_audit = monodromy(
        d, acb(eigenvalue), steps, order
    )
    anchor = matrix[6]
    initial_phi = anchor
    initial_phi_x = 1 - matrix[4]
    state = [acb(value) for value in (0, 1, 0, 1)] + [
        initial_phi,
        initial_phi_x,
        acb(0),
        acb(0),
        acb(0),
    ]
    step_size = 2 * arb.pi() / steps
    audit = OverlapAudit(step_count=steps)
    for _ in range(steps):
        state = overlap_step(
            state, d, eigenvalue, step_size, order, audit
        )
    return {
        "anchor": anchor,
        "numerator": state[6],
        "rightEnergy": state[7],
        "leftEnergy": state[8],
    }, audit, monodromy_audit
