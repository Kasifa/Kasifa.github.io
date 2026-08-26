#!/usr/bin/env python3
"""Independent binary64 finite-matrix audit for R0.71Z.

This program is deliberately self-contained.  It imports no R0.71Z producer
and reads no producer result.  Starting from raw parameters repeated below, it
constructs the truncated shift matrices and diagonal heat generator directly.
It checks

* skew-adjointness, dissipativity, contraction, and the energy identity;
* the exact target row of Q = P_0[V' + V(D + lambda_0)];
* the dissipation-paired L1 payment for QF;
* the exact multiplier L1/L2 integrals and the stated dimension-free bounds;
* the complex-scalar bounded-variation sampling inequality on an independent
  smooth function with simple, double, and triple roots.

The calculation uses IEEE-754 binary64 through NumPy/SciPy.  It corroborates
finite algebra and numerical inequalities.  It is not interval arithmetic,
does not prove the infinite-lattice theorem, and does not locate the complete
root set of a nonlinear continuum evolution.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path

import numpy as np
from numpy.polynomial import Polynomial
from scipy.integrate import quad, solve_ivp


# Raw audit parameters.  They are intentionally repeated rather than imported.
NU = 0.02
D_MODULUS = 8.0
K_Y = 1.0
K_Z = 1.0
Q_VALUE = 64.0
A_0 = 0.05
WINDOW_LENGTH = 0.30
DELTA = 0.035
RADIUS = 24
MULTIPLIERS = np.array([1, 2, 4, 7], dtype=int)
COEFFICIENTS = np.array([0.80, 0.55, 0.35, 0.20], dtype=float)
INITIAL_PHASES = np.exp(1j * np.array([0.0, 0.7, 1.8, -0.4], dtype=float))

KAPPA = NU * D_MODULUS**2
M_CARRIERS = int(MULTIPLIERS.size)
MATRIX_DIMENSION = 2 * RADIUS + 1
TARGET_INDEX = RADIUS
Q_STAR = max(1.0, 2.0 * abs(K_Y) / D_MODULUS)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def check(
    name: str,
    passed: bool,
    value: object,
    requirement: str,
) -> dict[str, object]:
    return {
        "name": name,
        "passed": bool(passed),
        "value": value,
        "requirement": requirement,
    }


def shift_pair(step: int) -> np.ndarray:
    """Return the symmetric zero-padded finite shift T_step + T_-step."""

    matrix = np.zeros((MATRIX_DIMENSION, MATRIX_DIMENSION), dtype=np.complex128)
    for column in range(MATRIX_DIMENSION):
        lower = column - step
        upper = column + step
        if lower >= 0:
            matrix[lower, column] += 1.0
        if upper < MATRIX_DIMENSION:
            matrix[upper, column] += 1.0
    return matrix


SHIFT_PAIRS = tuple(shift_pair(int(step)) for step in MULTIPLIERS)


def heat_coefficients(scaled_time: float) -> np.ndarray:
    return COEFFICIENTS * np.exp(
        -KAPPA * MULTIPLIERS.astype(float) ** 2 * scaled_time
    )


def shear_generator(scaled_time: float) -> np.ndarray:
    matrix = np.zeros((MATRIX_DIMENSION, MATRIX_DIMENSION), dtype=np.complex128)
    for amplitude, shift in zip(
        heat_coefficients(scaled_time), SHIFT_PAIRS, strict=True
    ):
        matrix += amplitude * shift
    return -1j * K_Z * matrix


def shear_derivative(scaled_time: float) -> np.ndarray:
    matrix = np.zeros((MATRIX_DIMENSION, MATRIX_DIMENSION), dtype=np.complex128)
    amplitudes = heat_coefficients(scaled_time)
    for multiplier, amplitude, shift in zip(
        MULTIPLIERS, amplitudes, SHIFT_PAIRS, strict=True
    ):
        matrix += (-KAPPA * float(multiplier) ** 2 * amplitude) * shift
    return -1j * K_Z * matrix


def diffusion_data() -> tuple[np.ndarray, np.ndarray]:
    indices = np.arange(-RADIUS, RADIUS + 1, dtype=float)
    lambdas = NU * (
        (D_MODULUS * indices + K_Y / Q_VALUE) ** 2
        + (K_Z / Q_VALUE) ** 2
    )
    return np.diag((-lambdas).astype(np.complex128)), lambdas


DIFFUSION, LAMBDAS = diffusion_data()
LAMBDA_0 = float(LAMBDAS[TARGET_INDEX])


def target_q_row(scaled_time: float) -> np.ndarray:
    identity = np.eye(MATRIX_DIMENSION, dtype=np.complex128)
    full = shear_derivative(scaled_time) + shear_generator(scaled_time) @ (
        DIFFUSION + LAMBDA_0 * identity
    )
    return full[TARGET_INDEX, :]


def expected_q_row(scaled_time: float) -> np.ndarray:
    row = np.zeros(MATRIX_DIMENSION, dtype=np.complex128)
    amplitudes = heat_coefficients(scaled_time)
    for multiplier, amplitude in zip(MULTIPLIERS, amplitudes, strict=True):
        radius = float(multiplier)
        common = -1j * K_Z * amplitude
        negative_coefficient = (
            -2.0 * NU * D_MODULUS**2 * radius**2
            + 2.0 * NU * D_MODULUS * radius * K_Y / Q_VALUE
        )
        positive_coefficient = (
            -2.0 * NU * D_MODULUS**2 * radius**2
            - 2.0 * NU * D_MODULUS * radius * K_Y / Q_VALUE
        )
        row[TARGET_INDEX - multiplier] = common * negative_coefficient
        row[TARGET_INDEX + multiplier] = common * positive_coefficient
    return row


def multiplier_norm(scaled_time: float) -> float:
    """Exact infinite-lattice norm for the positive coefficients used here."""

    # The torus multiplier is -2 i K_Z sum_l a_l cos(r_l theta).  All a_l are
    # positive, so the maximum absolute value is attained at theta = 0.
    return 2.0 * abs(K_Z) * float(np.sum(heat_coefficients(scaled_time)))


def initial_state() -> np.ndarray:
    state = np.zeros(MATRIX_DIMENSION, dtype=np.complex128)
    for multiplier, phase in zip(MULTIPLIERS, INITIAL_PHASES, strict=True):
        state[TARGET_INDEX - multiplier] = phase
    return state


def finite_evolution_audit() -> dict[str, object]:
    initial = initial_state()
    initial_norm_square = float(np.vdot(initial, initial).real)
    require(abs(initial_norm_square - M_CARRIERS) < 2.0e-15, "initial norm")

    observation_times = np.linspace(A_0, A_0 + WINDOW_LENGTH, 121)
    skew_defects = []
    q_row_defects = []
    q_support_defects = []
    allowed = {TARGET_INDEX - int(r) for r in MULTIPLIERS}
    allowed.update({TARGET_INDEX + int(r) for r in MULTIPLIERS})
    forbidden = [index for index in range(MATRIX_DIMENSION) if index not in allowed]

    for scaled_time in observation_times[::10]:
        shear = shear_generator(float(scaled_time))
        shear_norm = float(np.linalg.norm(shear, ord=2))
        skew_defects.append(
            float(
                np.linalg.norm(shear + shear.conj().T, ord=2)
                / max(shear_norm, np.finfo(float).tiny)
            )
        )
        actual_row = target_q_row(float(scaled_time))
        expected_row = expected_q_row(float(scaled_time))
        row_scale = max(float(np.linalg.norm(expected_row)), np.finfo(float).tiny)
        q_row_defects.append(float(np.linalg.norm(actual_row - expected_row) / row_scale))
        q_support_defects.append(float(np.max(np.abs(actual_row[forbidden]))))

    max_skew_defect = max(skew_defects)
    max_q_row_defect = max(q_row_defects)
    max_q_support_defect = max(q_support_defects)

    def right_side(scaled_time: float, state: np.ndarray) -> np.ndarray:
        return (DIFFUSION + DELTA * shear_generator(scaled_time)) @ state

    solution = solve_ivp(
        right_side,
        (0.0, A_0 + WINDOW_LENGTH),
        initial,
        method="DOP853",
        t_eval=np.concatenate(([0.0], observation_times)),
        dense_output=True,
        rtol=2.0e-11,
        atol=2.0e-13,
    )
    require(solution.success and solution.sol is not None, "finite evolution solve")

    norm_squares = np.sum(np.abs(solution.y) ** 2, axis=0)
    max_contraction_ratio = float(np.sqrt(np.max(norm_squares) / initial_norm_square))
    max_observation_contraction_ratio = float(
        np.sqrt(np.max(norm_squares[1:]) / initial_norm_square)
    )
    final_norm_square = float(norm_squares[-1])
    final_contraction_ratio = math.sqrt(final_norm_square / initial_norm_square)

    def dissipation_integrand(scaled_time: float) -> float:
        state = solution.sol(scaled_time)
        return float(np.dot(LAMBDAS, np.abs(state) ** 2))

    dissipation_integral, dissipation_error = quad(
        dissipation_integrand,
        0.0,
        A_0 + WINDOW_LENGTH,
        epsabs=2.0e-11,
        epsrel=2.0e-10,
        limit=300,
    )
    energy_identity_defect = abs(
        initial_norm_square - final_norm_square - 2.0 * dissipation_integral
    )
    energy_identity_scale = max(initial_norm_square - final_norm_square, 1.0e-15)
    energy_identity_relative_defect = energy_identity_defect / energy_identity_scale

    omega = multiplier_norm(A_0)
    a0 = heat_coefficients(A_0)
    a_square_integral_full = float(np.sum(a0**2) / (2.0 * KAPPA))
    q_cauchy_bound = (
        6.0
        * math.sqrt(2.0 * NU)
        * D_MODULUS
        * abs(K_Z)
        * math.sqrt(a_square_integral_full)
        * math.sqrt(M_CARRIERS / 2.0)
    )
    q_report_bound = 3.0 * omega * math.sqrt(M_CARRIERS)

    def q_integrand(scaled_time: float) -> float:
        state = solution.sol(scaled_time)
        return float(abs(target_q_row(scaled_time) @ state))

    q_integral, q_integral_error = quad(
        q_integrand,
        A_0,
        A_0 + WINDOW_LENGTH,
        epsabs=2.0e-11,
        epsrel=2.0e-10,
        limit=300,
    )

    weighted_pointwise_ratios = []
    for scaled_time in observation_times:
        state = solution.sol(float(scaled_time))
        energy = float(np.dot(LAMBDAS, np.abs(state) ** 2))
        amplitudes = heat_coefficients(float(scaled_time))
        a_weight = math.sqrt(
            float(np.sum(MULTIPLIERS.astype(float) ** 2 * amplitudes**2))
        )
        bound = 6.0 * math.sqrt(2.0 * NU) * D_MODULUS * abs(K_Z)
        bound *= a_weight * math.sqrt(max(energy, 0.0))
        actual = float(abs(target_q_row(float(scaled_time)) @ state))
        weighted_pointwise_ratios.append(actual / max(bound, np.finfo(float).tiny))
    max_weighted_pointwise_ratio = max(weighted_pointwise_ratios)

    return {
        "initialNormSquared": initial_norm_square,
        "maximumSkewAdjointDefect": max_skew_defect,
        "maximumQRowRelativeDefect": max_q_row_defect,
        "maximumQOffSupportEntry": max_q_support_defect,
        "maximumContractionRatio": max_contraction_ratio,
        "maximumObservationContractionRatio": max_observation_contraction_ratio,
        "finalNormSquared": final_norm_square,
        "finalContractionRatio": final_contraction_ratio,
        "dissipationIntegral": dissipation_integral,
        "dissipationQuadratureError": dissipation_error,
        "energyIdentityRelativeDefect": energy_identity_relative_defect,
        "maximumWeightedPointwiseQRatio": max_weighted_pointwise_ratio,
        "qIntegralOnFiniteWindow": q_integral,
        "qIntegralQuadratureError": q_integral_error,
        "qCauchyBoundOnInfiniteWindow": q_cauchy_bound,
        "qReportedBound": q_report_bound,
        "qIntegralOverReportedBound": q_integral / q_report_bound,
        "qCauchyOverReportedBound": q_cauchy_bound / q_report_bound,
        "omega": omega,
        "eta": abs(DELTA) * omega,
    }


def multiplier_integral_audit() -> dict[str, object]:
    radii = MULTIPLIERS.astype(float)
    a0 = heat_coefficients(A_0)
    omega = multiplier_norm(A_0)
    c_kappa = math.pi**2 / (math.sqrt(45.0) * KAPPA)

    exact_l1 = 2.0 * abs(K_Z) / KAPPA * float(np.sum(a0 / radii**2))
    exact_l2 = 0.0
    for left, left_radius in enumerate(radii):
        for right, right_radius in enumerate(radii):
            exact_l2 += (
                4.0
                * K_Z**2
                * a0[left]
                * a0[right]
                / (KAPPA * (left_radius**2 + right_radius**2))
            )

    quadrature_l1, quadrature_l1_error = quad(
        multiplier_norm,
        A_0,
        np.inf,
        epsabs=2.0e-12,
        epsrel=2.0e-11,
        limit=400,
    )
    quadrature_l2, quadrature_l2_error = quad(
        lambda time: multiplier_norm(time) ** 2,
        A_0,
        np.inf,
        epsabs=2.0e-12,
        epsrel=2.0e-11,
        limit=400,
    )

    haar_l2_square = 2.0 * K_Z**2 * float(np.sum(a0**2))
    l1_bound = c_kappa * omega
    l2_bound = c_kappa * omega**2
    return {
        "omega": omega,
        "haarL2NormSquaredAtA0": haar_l2_square,
        "haarL2OverOmegaSquared": haar_l2_square / omega**2,
        "exactL1Integral": exact_l1,
        "quadratureL1Integral": quadrature_l1,
        "quadratureL1ErrorEstimate": quadrature_l1_error,
        "relativeL1FormulaDefect": abs(exact_l1 - quadrature_l1) / exact_l1,
        "cKappaOmegaBound": l1_bound,
        "L1OverBound": exact_l1 / l1_bound,
        "exactL2Integral": exact_l2,
        "quadratureL2Integral": quadrature_l2,
        "quadratureL2ErrorEstimate": quadrature_l2_error,
        "relativeL2FormulaDefect": abs(exact_l2 - quadrature_l2) / exact_l2,
        "cKappaOmegaSquaredBound": l2_bound,
        "L2OverBound": exact_l2 / l2_bound,
        "cKappa": c_kappa,
    }


def complex_bv_sampling_audit() -> dict[str, object]:
    roots = np.array([0.125, 0.25, 0.50, 0.75, 0.875], dtype=float)
    multiplicities = np.array([1, 2, 1, 3, 1], dtype=int)
    polynomial = Polynomial([1.0])
    for root, multiplicity in zip(roots, multiplicities, strict=True):
        for _ in range(int(multiplicity)):
            polynomial *= Polynomial([-float(root), 1.0])
    polynomial *= complex(1.0, -0.35)
    first = polynomial.deriv()
    second = polynomial.deriv(2)
    frequency = 2.3

    def value(time: float) -> complex:
        return complex(np.exp(1j * frequency * time) * polynomial(time))

    def derivative(time: float) -> complex:
        phase = np.exp(1j * frequency * time)
        return complex(phase * (first(time) + 1j * frequency * polynomial(time)))

    def second_derivative(time: float) -> complex:
        phase = np.exp(1j * frequency * time)
        inside = second(time) + 2j * frequency * first(time)
        inside -= frequency**2 * polynomial(time)
        return complex(phase * inside)

    root_residuals = [abs(value(float(root))) for root in roots]
    root_slopes = [abs(derivative(float(root))) for root in roots]
    lhs = float(math.fsum(slope**2 for slope in root_slopes))

    dense_times = np.linspace(0.0, 1.0, 200_001)
    dense_derivatives = np.exp(1j * frequency * dense_times) * (
        first(dense_times) + 1j * frequency * polynomial(dense_times)
    )
    derivative_sup_sample = float(np.max(np.abs(dense_derivatives)))
    variation, variation_error = quad(
        lambda time: abs(second_derivative(time)),
        0.0,
        1.0,
        epsabs=2.0e-13,
        epsrel=2.0e-12,
        limit=500,
        points=roots.tolist(),
    )
    rhs_sampled = root_slopes[0] ** 2 + derivative_sup_sample * variation

    tail_l1 = 0.0
    segment_rows = []
    for left, right in zip(roots[:-1], roots[1:], strict=True):
        segment_variation, _ = quad(
            lambda time: abs(second_derivative(time)),
            float(left),
            float(right),
            epsabs=2.0e-13,
            epsrel=2.0e-12,
            limit=200,
        )
        right_slope = abs(derivative(float(right)))
        tail_l1 += right_slope
        segment_rows.append(
            {
                "leftRoot": float(left),
                "rightRoot": float(right),
                "rightSlope": right_slope,
                "variationIntegral": segment_variation,
                "ratio": right_slope / max(segment_variation, np.finfo(float).tiny),
            }
        )

    multiple_root_slopes = [
        root_slopes[index]
        for index, multiplicity in enumerate(multiplicities)
        if multiplicity > 1
    ]
    return {
        "roots": roots.tolist(),
        "multiplicities": multiplicities.tolist(),
        "maximumRootResidual": max(root_residuals),
        "rootSlopes": root_slopes,
        "maximumMultipleRootSlope": max(multiple_root_slopes),
        "sampledSquaredSlopeMass": lhs,
        "firstRootSlopeSquared": root_slopes[0] ** 2,
        "sampledDerivativeSupremum": derivative_sup_sample,
        "variationIntegral": variation,
        "variationQuadratureError": variation_error,
        "bvRightSide": rhs_sampled,
        "leftOverRight": lhs / rhs_sampled,
        "sumOfSlopesAfterFirstRoot": tail_l1,
        "sumAfterFirstOverVariation": tail_l1 / variation,
        "segmentRows": segment_rows,
        "note": (
            "The supremum is a dense binary64 sample and the variation is "
            "adaptive binary64 quadrature; this is corroboration, not a "
            "directed-rounding interval certificate."
        ),
    }


def audit() -> dict[str, object]:
    require(Q_VALUE >= Q_STAR, "q threshold")
    finite = finite_evolution_audit()
    multiplier = multiplier_integral_audit()
    bv = complex_bv_sampling_audit()

    checks = [
        check(
            "finite shift shear is skew-adjoint",
            finite["maximumSkewAdjointDefect"] < 2.0e-14,
            finite["maximumSkewAdjointDefect"],
            "max ||V+V*||_2 / ||V||_2 < 2e-14",
        ),
        check(
            "diagonal heat generator is strictly dissipative",
            float(np.min(LAMBDAS)) > 0.0,
            float(np.min(LAMBDAS)),
            "min_r lambda_(q,r) > 0",
        ),
        check(
            "time-dependent finite evolution contracts",
            finite["maximumContractionRatio"] <= 1.0 + 2.0e-11
            and finite["maximumObservationContractionRatio"] < 1.0,
            {
                "includingLaunch": finite["maximumContractionRatio"],
                "onObservationGrid": finite["maximumObservationContractionRatio"],
                "atWindowEnd": finite["finalContractionRatio"],
            },
            "norm ratio never exceeds 1 + 2e-11 and is strictly below 1 after launch",
        ),
        check(
            "finite energy-dissipation identity closes",
            finite["energyIdentityRelativeDefect"] < 2.0e-8,
            finite["energyIdentityRelativeDefect"],
            "relative defect in ||F0||^2-||FT||^2=2 integral E below 2e-8",
        ),
        check(
            "explicit Q target-row coefficients match",
            finite["maximumQRowRelativeDefect"] < 2.0e-13,
            finite["maximumQRowRelativeDefect"],
            "relative row defect < 2e-13 at all sampled times",
        ),
        check(
            "Q target row has only the declared plus-minus carrier support",
            finite["maximumQOffSupportEntry"] < 2.0e-14,
            finite["maximumQOffSupportEntry"],
            "maximum off-support coefficient < 2e-14",
        ),
        check(
            "pointwise dissipation pairing bounds QF",
            finite["maximumWeightedPointwiseQRatio"] <= 1.0 + 2.0e-12,
            finite["maximumWeightedPointwiseQRatio"],
            "max |QF|/[6 sqrt(2nu)d|Kz| A sqrt(E)] <= 1 + 2e-12",
        ),
        check(
            "integrated QF is below the dissipation payment",
            finite["qIntegralOnFiniteWindow"] <= finite["qCauchyBoundOnInfiniteWindow"],
            finite["qIntegralOverReportedBound"],
            "integral_window |QF| <= Cauchy bound <= 3 Omega sqrt(M)",
        ),
        check(
            "Cauchy payment is below 3 Omega sqrt(M)",
            finite["qCauchyBoundOnInfiniteWindow"] <= finite["qReportedBound"] + 2.0e-13,
            finite["qCauchyOverReportedBound"],
            "Cauchy bound / [3 Omega sqrt(M)] <= 1",
        ),
        check(
            "multiplier L1 integral formula and bound close",
            multiplier["relativeL1FormulaDefect"] < 2.0e-10
            and multiplier["L1OverBound"] <= 1.0,
            {
                "formulaDefect": multiplier["relativeL1FormulaDefect"],
                "boundRatio": multiplier["L1OverBound"],
            },
            "quadrature agrees with exact formula and integral ||V|| <= C_kappa Omega",
        ),
        check(
            "multiplier L2 integral formula and bound close",
            multiplier["relativeL2FormulaDefect"] < 2.0e-10
            and multiplier["L2OverBound"] <= 1.0,
            {
                "formulaDefect": multiplier["relativeL2FormulaDefect"],
                "boundRatio": multiplier["L2OverBound"],
            },
            "quadrature agrees with exact formula and integral ||V||^2 <= C_kappa Omega^2",
        ),
        check(
            "Haar L2 multiplier lower bound is respected",
            multiplier["haarL2OverOmegaSquared"] <= 1.0 + 2.0e-15,
            multiplier["haarL2OverOmegaSquared"],
            "2 Kz^2 sum |a_l(A0)|^2 / Omega^2 <= 1",
        ),
        check(
            "synthetic complex zeros are resolved",
            bv["maximumRootResidual"] < 2.0e-14,
            bv["maximumRootResidual"],
            "maximum |g(tau_m)| < 2e-14",
        ),
        check(
            "double and triple roots have zero sampled slope",
            bv["maximumMultipleRootSlope"] < 2.0e-13,
            bv["maximumMultipleRootSlope"],
            "maximum |g'(tau)| at multiplicity > 1 below 2e-13",
        ),
        check(
            "complex bounded-variation sampling inequality holds",
            bv["leftOverRight"] <= 1.0
            and bv["sumAfterFirstOverVariation"] <= 1.0 + 2.0e-11,
            {
                "squaredSlopeRatio": bv["leftOverRight"],
                "intermediateL1Ratio": bv["sumAfterFirstOverVariation"],
            },
            "sum |g'(tau)|^2 <= |g'(tau1)|^2 + ||g'||_inf integral |g''|",
        ),
    ]
    passed = all(item["passed"] for item in checks)
    return {
        "schemaVersion": 1,
        "release": "R0.71Z",
        "audit": "independent-binary64-finite-matrix",
        "generatedAtUtc": utc_now(),
        "passed": passed,
        "checkCount": len(checks),
        "passedCheckCount": sum(bool(item["passed"]) for item in checks),
        "independence": {
            "importsProducer": False,
            "readsProducerResult": False,
            "rawParametersRepeatedLocally": True,
        },
        "arithmetic": {
            "format": "IEEE-754 binary64",
            "intervalArithmetic": False,
            "linearAlgebra": "NumPy complex128",
            "odeAndQuadrature": "SciPy solve_ivp(DOP853) and quad",
        },
        "parameters": {
            "nu": NU,
            "d": D_MODULUS,
            "Ky": K_Y,
            "Kz": K_Z,
            "q": Q_VALUE,
            "qThreshold": Q_STAR,
            "A0": A_0,
            "windowLength": WINDOW_LENGTH,
            "delta": DELTA,
            "carrierCount": M_CARRIERS,
            "multipliers": MULTIPLIERS.tolist(),
            "coefficients": COEFFICIENTS.tolist(),
            "matrixRadius": RADIUS,
            "matrixDimension": MATRIX_DIMENSION,
        },
        "checks": checks,
        "finiteEvolution": finite,
        "multiplierIntegrals": multiplier,
        "complexBvSampling": bv,
        "limitations": [
            "The matrix has a fixed zero-padded Fourier cutoff and is not the infinite lattice.",
            "Binary64 ODE solves, norm evaluations, dense sampling, and quadrature are not directed-rounding interval proofs.",
            "The synthetic W^{2,1} function tests the BV lemma but is not a target coordinate of the triangular evolution.",
            "No complete continuum root set, growing-dimensional IFT branch, three-dimensional turbulence, or Navier-Stokes endpoint theorem is certified.",
        ],
    }


def main() -> None:
    args = parse_args()
    result = audit()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
