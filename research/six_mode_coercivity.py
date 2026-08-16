#!/usr/bin/env python3
"""Closed six-mode leakage formulas and a quantitative coercivity audit.

The Fourier support is

    k1=(1,0,0), k2=(0,1,0), k3=(-1,-1,0),

together with its negatives.  A real divergence-free field on this support is
encoded by six complex numbers

    u_k1=(0, alpha, zeta),
    u_k2=(beta, 0, eta),
    u_k3=(gamma, -gamma, theta).

This file verifies the closed formulas against the direct convolution in
``triad_leakage_variation.py``.  It also checks a non-sharp but explicit
coercivity inequality and computes the constrained Hessian at the R0.6
candidate.  The Hessian calculation is numerical evidence; the closed
formulas and coercivity inequality are elementary algebraic identities and
estimates.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import math

import numpy as np

from triad_leakage_variation import (
    analytic_fixed_injection_candidates,
    diagnostics,
    normalize,
    ORIGINAL_PARAMETERS,
)


SQRT2 = math.sqrt(2.0)
SQRT5 = math.sqrt(5.0)
TRANSFER_FACTOR = 2.0 * (SQRT2 - 1.0)
COERCIVITY_C1 = 1.0 / (2.0 * 5.0**0.25)
COERCIVITY_C2 = 5.0**0.125 / 2.0**1.375


def complex_variables(parameters: np.ndarray) -> tuple[complex, ...]:
    values = np.asarray(parameters, dtype=float)
    if values.shape != (12,):
        raise ValueError("six-mode parameters must have twelve real entries")
    return tuple(
        complex(values[2 * index], values[2 * index + 1])
        for index in range(6)
    )


def closed_form_diagnostics(parameters: np.ndarray) -> dict[str, float]:
    alpha, zeta, beta, eta, gamma, theta = complex_variables(parameters)
    horizontal = abs(alpha) ** 2 + abs(beta) ** 2
    vertical = abs(zeta) ** 2 + abs(eta) ** 2
    gamma_squared = abs(gamma) ** 2
    theta_squared = abs(theta) ** 2

    first_difference = beta.conjugate() * zeta - alpha * eta.conjugate()
    second_difference = beta * theta.conjugate() - gamma.conjugate() * eta
    third_difference = gamma * zeta.conjugate() + alpha.conjugate() * theta
    transfer_product = theta * (alpha * eta + beta * zeta)

    energy = (
        2.0 * (horizontal + vertical)
        + 4.0 * SQRT2 * gamma_squared
        + 2.0 * SQRT2 * theta_squared
    )
    transfer = TRANSFER_FACTOR * (1.0j * transfer_product).real
    outside_squared = (
        2.0 * SQRT2 * abs(first_difference) ** 2
        + 2.0 / SQRT5 * gamma_squared * horizontal
        + 2.0
        * SQRT5
        * (abs(second_difference) ** 2 + abs(third_difference) ** 2)
    )
    return {
        "energy": energy,
        "transfer": transfer,
        "outsideSquared": outside_squared,
        "horizontalSquared": horizontal,
        "verticalSquared": vertical,
        "gammaSquared": gamma_squared,
        "thetaSquared": theta_squared,
        "firstDifferenceSquared": abs(first_difference) ** 2,
        "secondPairSquared": abs(second_difference) ** 2 + abs(third_difference) ** 2,
    }


def normalized_coercive_lower_bound(energy: float, transfer: float) -> float:
    """Return the explicit lower bound for L_out^2.

    If ``F=L_out^2`` and ``E`` is the H^(1/2) energy, the proof gives

        J <= c1 f^(1/2) + c2 f^(1/4),
        J = |T| / (2(sqrt(2)-1) E^(3/2)),  f = F/E^2.

    Solving the increasing quadratic in y=f^(1/4) gives the result below.
    """

    if energy <= 0:
        if abs(transfer) == 0:
            return 0.0
        raise ValueError("positive transfer requires positive energy")
    normalized_transfer = abs(transfer) / (TRANSFER_FACTOR * energy**1.5)
    root = (
        math.sqrt(COERCIVITY_C2**2 + 4.0 * COERCIVITY_C1 * normalized_transfer)
        - COERCIVITY_C2
    ) / (2.0 * COERCIVITY_C1)
    return energy**2 * root**4


def coercivity_rhs(energy: float, outside_squared: float) -> float:
    if energy < 0 or outside_squared < 0:
        raise ValueError("energy and squared leakage must be nonnegative")
    return TRANSFER_FACTOR * (
        COERCIVITY_C1 * math.sqrt(energy * outside_squared)
        + COERCIVITY_C2 * energy * outside_squared**0.25
    )


@dataclass(frozen=True)
class Jet:
    value: float
    gradient: np.ndarray
    hessian: np.ndarray

    @classmethod
    def constant(cls, value: float, dimension: int) -> "Jet":
        return cls(value, np.zeros(dimension), np.zeros((dimension, dimension)))

    @classmethod
    def variable(cls, value: float, index: int, dimension: int) -> "Jet":
        gradient = np.zeros(dimension)
        gradient[index] = 1.0
        return cls(value, gradient, np.zeros((dimension, dimension)))

    def __add__(self, other: "Jet | float") -> "Jet":
        right = other if isinstance(other, Jet) else Jet.constant(other, len(self.gradient))
        return Jet(
            self.value + right.value,
            self.gradient + right.gradient,
            self.hessian + right.hessian,
        )

    __radd__ = __add__

    def __neg__(self) -> "Jet":
        return Jet(-self.value, -self.gradient, -self.hessian)

    def __sub__(self, other: "Jet | float") -> "Jet":
        return self + (-other if isinstance(other, Jet) else -float(other))

    def __rsub__(self, other: "Jet | float") -> "Jet":
        return (-self) + other

    def __mul__(self, other: "Jet | float") -> "Jet":
        right = other if isinstance(other, Jet) else Jet.constant(other, len(self.gradient))
        return Jet(
            self.value * right.value,
            self.gradient * right.value + self.value * right.gradient,
            self.hessian * right.value
            + self.value * right.hessian
            + np.outer(self.gradient, right.gradient)
            + np.outer(right.gradient, self.gradient),
        )

    __rmul__ = __mul__


ComplexJet = tuple[Jet, Jet]


def jet_complex_add(left: ComplexJet, right: ComplexJet) -> ComplexJet:
    return left[0] + right[0], left[1] + right[1]


def jet_complex_neg(value: ComplexJet) -> ComplexJet:
    return -value[0], -value[1]


def jet_complex_sub(left: ComplexJet, right: ComplexJet) -> ComplexJet:
    return jet_complex_add(left, jet_complex_neg(right))


def jet_complex_multiply(left: ComplexJet, right: ComplexJet) -> ComplexJet:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def jet_complex_conjugate(value: ComplexJet) -> ComplexJet:
    return value[0], -value[1]


def jet_complex_abs_squared(value: ComplexJet) -> Jet:
    return value[0] * value[0] + value[1] * value[1]


def jet_diagnostics(parameters: np.ndarray) -> dict[str, Jet]:
    dimension = len(parameters)
    variables = [
        Jet.variable(float(value), index, dimension)
        for index, value in enumerate(parameters)
    ]
    alpha, zeta, beta, eta, gamma, theta = [
        (variables[2 * index], variables[2 * index + 1])
        for index in range(6)
    ]
    horizontal = jet_complex_abs_squared(alpha) + jet_complex_abs_squared(beta)
    vertical = jet_complex_abs_squared(zeta) + jet_complex_abs_squared(eta)
    gamma_squared = jet_complex_abs_squared(gamma)
    theta_squared = jet_complex_abs_squared(theta)

    first_difference = jet_complex_sub(
        jet_complex_multiply(jet_complex_conjugate(beta), zeta),
        jet_complex_multiply(alpha, jet_complex_conjugate(eta)),
    )
    second_difference = jet_complex_sub(
        jet_complex_multiply(beta, jet_complex_conjugate(theta)),
        jet_complex_multiply(jet_complex_conjugate(gamma), eta),
    )
    third_difference = jet_complex_add(
        jet_complex_multiply(gamma, jet_complex_conjugate(zeta)),
        jet_complex_multiply(jet_complex_conjugate(alpha), theta),
    )
    transfer_product = jet_complex_multiply(
        theta,
        jet_complex_add(
            jet_complex_multiply(alpha, eta),
            jet_complex_multiply(beta, zeta),
        ),
    )

    energy = (
        2.0 * (horizontal + vertical)
        + 4.0 * SQRT2 * gamma_squared
        + 2.0 * SQRT2 * theta_squared
    )
    transfer = -TRANSFER_FACTOR * transfer_product[1]
    outside_squared = (
        2.0 * SQRT2 * jet_complex_abs_squared(first_difference)
        + 2.0 / SQRT5 * gamma_squared * horizontal
        + 2.0
        * SQRT5
        * (
            jet_complex_abs_squared(second_difference)
            + jet_complex_abs_squared(third_difference)
        )
    )
    return {
        "energy": energy,
        "transfer": transfer,
        "outsideSquared": outside_squared,
    }


def phase_direction(parameters: np.ndarray, x_phase: float, y_phase: float) -> np.ndarray:
    alpha, zeta, beta, eta, gamma, theta = complex_variables(parameters)
    frequencies = [x_phase, x_phase, y_phase, y_phase, -x_phase - y_phase, -x_phase - y_phase]
    values = [alpha, zeta, beta, eta, gamma, theta]
    direction = np.empty(12)
    for index, (frequency, value) in enumerate(zip(frequencies, values, strict=True)):
        derivative = 1.0j * frequency * value
        direction[2 * index] = derivative.real
        direction[2 * index + 1] = derivative.imag
    return direction


def null_space(rows: np.ndarray, tolerance: float = 1e-11) -> np.ndarray:
    _, singular_values, right = np.linalg.svd(rows, full_matrices=True)
    rank = int(np.sum(singular_values > tolerance))
    return right[rank:].T


def constrained_hessian_audit(parameters: np.ndarray) -> dict[str, object]:
    jets = jet_diagnostics(parameters)
    energy = jets["energy"]
    transfer = jets["transfer"]
    outside = jets["outsideSquared"]
    constraint_gradients = np.column_stack((energy.gradient, transfer.gradient))
    multipliers, *_ = np.linalg.lstsq(
        constraint_gradients,
        outside.gradient,
        rcond=None,
    )
    stationarity_residual = outside.gradient - constraint_gradients @ multipliers
    lagrangian_hessian = (
        outside.hessian
        - multipliers[0] * energy.hessian
        - multipliers[1] * transfer.hessian
    )

    tangent_basis = null_space(constraint_gradients.T)
    tangent_hessian = tangent_basis.T @ lagrangian_hessian @ tangent_basis
    tangent_eigenvalues = np.linalg.eigvalsh(tangent_hessian)

    translation_x = phase_direction(parameters, 1.0, 0.0)
    translation_y = phase_direction(parameters, 0.0, 1.0)
    quotient_rows = np.vstack(
        (
            energy.gradient,
            transfer.gradient,
            translation_x,
            translation_y,
        )
    )
    quotient_basis = null_space(quotient_rows)
    quotient_hessian = quotient_basis.T @ lagrangian_hessian @ quotient_basis
    quotient_eigenvalues = np.linalg.eigvalsh(quotient_hessian)

    return {
        "multipliers": multipliers.tolist(),
        "stationarityResidual": float(np.linalg.norm(stationarity_residual)),
        "constraintRank": int(np.linalg.matrix_rank(constraint_gradients)),
        "tangentEigenvalues": tangent_eigenvalues.tolist(),
        "translationResiduals": {
            "x": float(np.linalg.norm(lagrangian_hessian @ translation_x)),
            "y": float(np.linalg.norm(lagrangian_hessian @ translation_y)),
        },
        "quotientEigenvalues": quotient_eigenvalues.tolist(),
    }


def validate() -> dict[str, object]:
    random = np.random.default_rng(20260816)
    maximum_formula_error = 0.0
    maximum_coercivity_ratio = 0.0
    for _ in range(2000):
        parameters = random.normal(size=12)
        direct = diagnostics(parameters)
        closed = closed_form_diagnostics(parameters)
        for field in ("energy", "transfer", "outsideSquared"):
            scale = max(1.0, abs(direct[field]), abs(closed[field]))
            maximum_formula_error = max(
                maximum_formula_error,
                abs(direct[field] - closed[field]) / scale,
            )
        right = coercivity_rhs(closed["energy"], closed["outsideSquared"])
        if right > 0:
            maximum_coercivity_ratio = max(
                maximum_coercivity_ratio,
                abs(closed["transfer"]) / right,
            )
        assert abs(closed["transfer"]) <= right * (1.0 + 1e-12)

    original = normalize(ORIGINAL_PARAMETERS)
    injection = abs(diagnostics(original)["transfer"])
    analytic = analytic_fixed_injection_candidates(injection)["largeRoot"]
    candidate = np.asarray(analytic["parameters"], dtype=float)
    candidate_closed = closed_form_diagnostics(candidate)
    lower_bound = normalized_coercive_lower_bound(
        candidate_closed["energy"],
        candidate_closed["transfer"],
    )
    hessian = constrained_hessian_audit(candidate)

    assert maximum_formula_error < 2e-14
    assert lower_bound > 0
    assert lower_bound < candidate_closed["outsideSquared"]
    assert hessian["stationarityResidual"] < 2e-10
    assert hessian["constraintRank"] == 2

    return {
        "closedFormula": {
            "maximumRelativeError": maximum_formula_error,
            "randomSamples": 2000,
        },
        "coercivity": {
            "c1": COERCIVITY_C1,
            "c2": COERCIVITY_C2,
            "maximumSampledLeftRightRatio": maximum_coercivity_ratio,
            "candidateCertifiedLowerBound": lower_bound,
            "candidateActualOutsideSquared": candidate_closed["outsideSquared"],
            "gapFactor": candidate_closed["outsideSquared"] / lower_bound,
        },
        "candidate": candidate_closed,
        "constrainedHessian": hessian,
        "statement": (
            "the closed formula and coercivity estimate are algebraic; "
            "the Hessian spectrum is a floating-point local audit"
        ),
    }


def main() -> None:
    print(json.dumps(validate(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
