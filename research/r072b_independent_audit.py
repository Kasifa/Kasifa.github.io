#!/usr/bin/env python3
"""Independent binary64 audit for R0.72B target-row coherence.

This file imports neither the producer nor its result.  It rebuilds the
equal-carrier scaling, the mixed exposure, and the target row of a finite
heat-decaying lattice from raw parameters.  A complex DOP853 evolution and
adaptive quadrature corroborate the dissipation-paired Q payment.  Separate
SciPy Bessel zeros evaluate the short-layer comparison indicators.

The calculations use IEEE-754 binary64.  They are deterministic but are not
interval arithmetic, a proof of the infinite lattice, or a Navier--Stokes
regularity result.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import platform
import resource
import sys
import time

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.special import jn_zeros


# Raw finite-matrix parameters, deliberately repeated here.
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
EQUAL_M_VALUES = tuple(2**power for power in range(0, 21))
EXPOSURE_M_VALUES = (1, 2, 4, 8, 16, 32, 64)
BESSEL_R_VALUES = (8, 16, 32, 64, 128, 256, 512, 1024)
ROOT_NEIGHBORHOOD = 0.35


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--progress-log", type=Path)
    parser.add_argument("--resource-log", type=Path)
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def emit(message: str) -> None:
    print(f"[{utc_now()}] {message}", file=sys.stderr, flush=True)


def append_json(path: Path | None, payload: dict[str, object]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(payload, sort_keys=True) + "\n")


def progress(path: Path | None, stage: str, **fields: object) -> None:
    append_json(path, {"timestampUtc": utc_now(), "stage": stage, **fields})


def resource_snapshot(
    path: Path | None, stage: str, started: float, **fields: object
) -> None:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    append_json(
        path,
        {
            "timestampUtc": utc_now(),
            "stage": stage,
            "elapsedSeconds": time.perf_counter() - started,
            "userCpuSeconds": usage.ru_utime,
            "systemCpuSeconds": usage.ru_stime,
            "maximumResidentSetRaw": usage.ru_maxrss,
            "logicalCpuCount": os.cpu_count(),
            **fields,
        },
    )


def check(
    name: str, passed: bool, value: object, requirement: str
) -> dict[str, object]:
    return {
        "name": name,
        "passed": bool(passed),
        "value": value,
        "requirement": requirement,
    }


def shift_pair(step: int) -> np.ndarray:
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


def heat_coefficients(time_value: float) -> np.ndarray:
    return COEFFICIENTS * np.exp(
        -KAPPA * MULTIPLIERS.astype(float) ** 2 * time_value
    )


def shear_generator(time_value: float) -> np.ndarray:
    matrix = np.zeros((MATRIX_DIMENSION, MATRIX_DIMENSION), dtype=np.complex128)
    for coefficient, shift in zip(
        heat_coefficients(time_value), SHIFT_PAIRS, strict=True
    ):
        matrix += coefficient * shift
    return -1j * K_Z * matrix


def shear_derivative(time_value: float) -> np.ndarray:
    matrix = np.zeros((MATRIX_DIMENSION, MATRIX_DIMENSION), dtype=np.complex128)
    coefficients = heat_coefficients(time_value)
    for multiplier, coefficient, shift in zip(
        MULTIPLIERS, coefficients, SHIFT_PAIRS, strict=True
    ):
        matrix += -KAPPA * float(multiplier) ** 2 * coefficient * shift
    return -1j * K_Z * matrix


def diffusion_data() -> tuple[np.ndarray, np.ndarray]:
    indices = np.arange(-RADIUS, RADIUS + 1, dtype=float)
    lambdas = NU * (
        (D_MODULUS * indices + K_Y / Q_VALUE) ** 2
        + (K_Z / Q_VALUE) ** 2
    )
    return np.diag(-lambdas.astype(np.complex128)), lambdas


DIFFUSION, LAMBDAS = diffusion_data()
LAMBDA_0 = float(LAMBDAS[TARGET_INDEX])


def q_target_row(time_value: float) -> np.ndarray:
    identity = np.eye(MATRIX_DIMENSION, dtype=np.complex128)
    full = shear_derivative(time_value) + shear_generator(time_value) @ (
        DIFFUSION + LAMBDA_0 * identity
    )
    return full[TARGET_INDEX, :]


def finite_target_row_audit() -> dict[str, object]:
    coefficients_at_a0 = heat_coefficients(A_0)
    target_row = shear_generator(A_0)[TARGET_INDEX, :]
    matrix_rho = float(np.linalg.norm(target_row))
    analytic_rho = math.sqrt(2.0 * K_Z**2 * float(np.sum(coefficients_at_a0**2)))
    omega = 2.0 * abs(K_Z) * float(np.sum(coefficients_at_a0))
    chi = analytic_rho**2 / omega**2

    initial = np.zeros(MATRIX_DIMENSION, dtype=np.complex128)
    for multiplier, phase in zip(MULTIPLIERS, INITIAL_PHASES, strict=True):
        initial[TARGET_INDEX - int(multiplier)] = phase

    def right_side(time_value: float, state: np.ndarray) -> np.ndarray:
        return (DIFFUSION + DELTA * shear_generator(time_value)) @ state

    final_time = A_0 + WINDOW_LENGTH
    solution = solve_ivp(
        right_side,
        (0.0, final_time),
        initial,
        method="DOP853",
        dense_output=True,
        rtol=2.0e-11,
        atol=2.0e-13,
        max_step=0.01,
    )
    if not solution.success or solution.sol is None:
        raise RuntimeError(f"finite matrix solve failed: {solution.message}")

    def q_integrand(time_value: float) -> float:
        return float(abs(q_target_row(time_value) @ solution.sol(time_value)))

    q_integral, q_error = quad(
        q_integrand,
        A_0,
        final_time,
        epsabs=2.0e-11,
        epsrel=2.0e-10,
        limit=300,
    )
    a_square_integral = float(np.sum(coefficients_at_a0**2)) / (2.0 * KAPPA)
    cauchy_payment = (
        6.0
        * math.sqrt(2.0 * NU)
        * D_MODULUS
        * abs(K_Z)
        * math.sqrt(a_square_integral)
        * math.sqrt(M_CARRIERS / 2.0)
    )
    reported_payment = 3.0 * analytic_rho * math.sqrt(M_CARRIERS)

    observation_times = np.linspace(A_0, final_time, 81)
    pointwise_ratios: list[float] = []
    for time_value in observation_times:
        state = solution.sol(float(time_value))
        energy = float(np.dot(LAMBDAS, np.abs(state) ** 2))
        coefficients = heat_coefficients(float(time_value))
        a_weight = math.sqrt(
            float(
                np.sum(
                    MULTIPLIERS.astype(float) ** 2 * coefficients**2
                )
            )
        )
        pointwise_bound = (
            6.0
            * math.sqrt(2.0 * NU)
            * D_MODULUS
            * abs(K_Z)
            * a_weight
            * math.sqrt(max(energy, 0.0))
        )
        pointwise_ratios.append(
            float(abs(q_target_row(float(time_value)) @ state))
            / max(pointwise_bound, np.finfo(float).tiny)
        )

    return {
        "rhoFromTargetMatrixRow": matrix_rho,
        "rhoFromParsevalFormula": analytic_rho,
        "rhoRelativeDefect": abs(matrix_rho - analytic_rho) / analytic_rho,
        "omega": omega,
        "chi": chi,
        "qIntegralOnWindow": q_integral,
        "qQuadratureErrorEstimate": q_error,
        "qCauchyPayment": cauchy_payment,
        "qReportedPaymentThreeRhoSqrtM": reported_payment,
        "qIntegralOverReportedPayment": q_integral / reported_payment,
        "qCauchyOverReportedPayment": cauchy_payment / reported_payment,
        "maximumPointwiseQRatio": max(pointwise_ratios),
        "solverSteps": int(solution.t.size),
    }


def independent_mixed_exposure() -> tuple[list[dict[str, float]], float, float]:
    c_kappa = math.pi**2 / (math.sqrt(45.0) * KAPPA)
    c_cross = math.sqrt(c_kappa / (2.0 * KAPPA))
    length = 2.0
    rows: list[dict[str, float]] = []
    for m_value in EXPOSURE_M_VALUES:
        radii = np.arange(1, m_value + 1, dtype=float)
        rho_a = math.sqrt(2.0 * m_value)
        omega = 2.0 * m_value

        def rho(time_value: float) -> float:
            return math.sqrt(
                2.0 * float(np.sum(np.exp(-2.0 * radii**2 * time_value)))
            )

        def norm_v(time_value: float) -> float:
            return 2.0 * float(np.sum(np.exp(-radii**2 * time_value)))

        integral, error = quad(
            lambda value: rho(value) * norm_v(value),
            0.0,
            length,
            epsabs=2.0e-12,
            epsrel=2.0e-11,
            points=[0.0005, 0.002, 0.01, 0.05, 0.25],
            limit=500,
        )
        ell_cross = integral / (rho_a * omega)
        upper = min(length, c_cross)
        rows.append(
            {
                "M": m_value,
                "ellCross": ell_cross,
                "quadratureErrorEstimate": error,
                "upperBound": upper,
                "ratioToBound": ell_cross / upper,
            }
        )
    return rows, c_kappa, c_cross


def equal_carrier_audit() -> tuple[list[dict[str, float]], float]:
    rows: list[dict[str, float]] = []
    values: list[float] = []
    for m_value in EQUAL_M_VALUES:
        # Closed finite sums avoid allocating an array whose length grows with
        # M.  The independent implementation uses binary64 rather than the
        # producer's arbitrary-precision integer/mpmath path.
        ks = float(m_value * (m_value + 1) * (2 * m_value + 1) / 6)
        kv = ks
        omega = 2.0 * m_value
        rho_squared = 2.0 * m_value
        chi = rho_squared / omega**2
        omega_squared_over_kv = omega**2 / kv
        prefactor = (
            (m_value / ks)
            * chi
            * np.cbrt(omega_squared_over_kv)
        )
        values.append(float(prefactor))
        rows.append(
            {
                "M": m_value,
                "Ks": ks,
                "Kv": kv,
                "chi": chi,
                "OmegaSquaredOverKv": omega_squared_over_kv,
                "normalizedGeometricPrefactor": float(prefactor),
                "scaledPrefactor": float(prefactor * m_value ** (10.0 / 3.0)),
            }
        )
    fitted_power = float(
        np.polyfit(
            np.log(np.asarray(EQUAL_M_VALUES[-7:], dtype=float)),
            np.log(np.asarray(values[-7:], dtype=float)),
            1,
        )[0]
    )
    return rows, fitted_power


def comparable_carrier_audit() -> tuple[list[dict[str, float]], float]:
    """Independent non-equal positive family with a fixed amplitude ratio."""

    lower = 0.8
    upper = 1.2
    rows: list[dict[str, float]] = []
    values: list[float] = []
    for m_value in EQUAL_M_VALUES[1:]:
        half = m_value // 2
        ks = float(m_value * (m_value + 1) * (2 * m_value + 1) / 6)
        even_square_sum = float(4 * half * (half + 1) * (2 * half + 1) / 6)
        odd_square_sum = ks - even_square_sum
        sum_z = half * (lower + upper)
        sum_z_square = half * (lower**2 + upper**2)
        kv = upper**2 * odd_square_sum + lower**2 * even_square_sum
        omega = 2.0 * sum_z
        rho_squared = 2.0 * sum_z_square
        chi = rho_squared / omega**2
        multiplier = omega**2 / kv
        prefactor = (m_value / ks) * chi * np.cbrt(multiplier)
        chi_upper = (upper / lower) ** 2 / (2.0 * m_value)
        multiplier_upper = 12.0 * (upper / lower) ** 2 / m_value
        values.append(float(prefactor))
        rows.append(
            {
                "M": m_value,
                "lowerAmplitude": lower,
                "upperAmplitude": upper,
                "chi": chi,
                "chiUpper": chi_upper,
                "chiOverUpper": chi / chi_upper,
                "OmegaSquaredOverKv": multiplier,
                "OmegaSquaredOverKvUpper": multiplier_upper,
                "multiplierRatioOverUpper": multiplier / multiplier_upper,
                "normalizedGeometricPrefactor": float(prefactor),
                "scaledPrefactor": float(prefactor * m_value ** (10.0 / 3.0)),
            }
        )
    fitted_power = float(
        np.polyfit(
            np.log(np.asarray(EQUAL_M_VALUES[-7:], dtype=float)),
            np.log(np.asarray(values[-7:], dtype=float)),
            1,
        )[0]
    )
    return rows, fitted_power


def phase_boundary_audit() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for beta in (0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0):
        rows.append(
            {
                "beta": beta,
                "old": min(1.5, (6.0 + 3.0 * beta) / 7.0),
                "participationOnly": min(2.25, (9.0 + 3.0 * beta) / 7.0),
                "coherent": min(2.5, (10.0 + 3.0 * beta) / 7.0),
            }
        )
    return rows


def bessel_no_go_audit() -> tuple[list[dict[str, float]], dict[str, float]]:
    maximum_r = max(BESSEL_R_VALUES)
    zeros = jn_zeros(1, maximum_r)
    rows: list[dict[str, float]] = []
    for r_value in BESSEL_R_VALUES:
        terminal_tau = float(zeros[r_value - 1] / 2.0 + ROOT_NEIGHBORHOOD)
        delta = float(r_value**4)
        layer = terminal_tau / delta
        frozen_rate = r_value**2 / math.log(r_value) ** 2
        theta = layer * frozen_rate
        xi = 2.0 * delta * (layer + math.expm1(-layer))
        xi_upper = delta * layer**2
        energy_loss = (
            4.0 * terminal_tau
            + 4.0 * terminal_tau**2
            + (8.0 / 3.0) * terminal_tau**3
        ) / delta
        rows.append(
            {
                "R": r_value,
                "terminalTau": terminal_tau,
                "layerLength": layer,
                "frozenEnhancedDissipationRate": frozen_rate,
                "Theta": theta,
                "scaledTheta": theta * r_value * math.log(r_value) ** 2,
                "Xi": xi,
                "XiUpper": xi_upper,
                "XiOverUpper": xi / xi_upper,
                "scaledXi": xi * r_value**2,
                "energyLossUpper": energy_loss,
                "scaledEnergyLoss": energy_loss * r_value,
            }
        )
    tail = rows[-5:]
    log_r = np.log(np.asarray([row["R"] for row in tail], dtype=float))
    powers = {
        name: float(
            np.polyfit(
                log_r,
                np.log(np.asarray([row[key] for row in tail], dtype=float)),
                1,
            )[0]
        )
        for name, key in (
            ("ThetaTailPower", "Theta"),
            ("XiTailPower", "Xi"),
            ("energyLossTailPower", "energyLossUpper"),
        )
    }
    return rows, powers


def main() -> None:
    args = parse_args()
    started = time.perf_counter()
    emit("R0.72B independent audit started")
    progress(args.progress_log, "independent-start")
    resource_snapshot(args.resource_log, "independent-start", started)

    finite = finite_target_row_audit()
    emit(
        "finite target-row audit complete: q/payment="
        f"{finite['qIntegralOverReportedPayment']:.6g}"
    )
    progress(
        args.progress_log,
        "finite-target-row-complete",
        qRatio=finite["qIntegralOverReportedPayment"],
    )
    resource_snapshot(args.resource_log, "finite-target-row-complete", started)

    exposure, c_kappa, c_cross = independent_mixed_exposure()
    emit("independent mixed-exposure quadrature complete")
    progress(
        args.progress_log,
        "mixed-exposure-complete",
        rowCount=len(exposure),
    )

    equal_rows, equal_power = equal_carrier_audit()
    comparable_rows, comparable_power = comparable_carrier_audit()
    phases = phase_boundary_audit()
    emit(
        f"carrier scaling complete: equal power {equal_power:.8f}; "
        f"comparable power {comparable_power:.8f}"
    )
    progress(
        args.progress_log,
        "scaling-complete",
        fittedPower=equal_power,
        comparableFittedPower=comparable_power,
    )

    bessel_rows, bessel_powers = bessel_no_go_audit()
    emit("independent Bessel comparison ledger complete")
    progress(
        args.progress_log,
        "bessel-comparison-complete",
        rowCount=len(bessel_rows),
    )

    checks = [
        check(
            "target matrix row equals Parseval rho",
            finite["rhoRelativeDefect"] < 2.0e-14,
            finite["rhoRelativeDefect"],
            "relative target-row norm defect < 2e-14",
        ),
        check(
            "finite Q payment closes with rho_A",
            finite["maximumPointwiseQRatio"] <= 1.0 + 3.0e-12
            and finite["qIntegralOnWindow"] <= finite["qCauchyPayment"]
            and abs(finite["qCauchyOverReportedPayment"] - 1.0) < 3.0e-15,
            {
                "pointwiseRatio": finite["maximumPointwiseQRatio"],
                "integralOverPayment": finite["qIntegralOverReportedPayment"],
                "cauchyOverPayment": finite["qCauchyOverReportedPayment"],
            },
            "integral |QF| <= Cauchy payment = 3*rho_A*sqrt(M)",
        ),
        check(
            "mixed exposure quadrature obeys analytic bound",
            max(row["ratioToBound"] for row in exposure) <= 1.0 + 2.0e-12,
            max(row["ratioToBound"] for row in exposure),
            "ell_cross<=min(L,Ccross)",
        ),
        check(
            "equal-carrier coherence identities",
            max(
                abs(row["chi"] - 1.0 / (2.0 * row["M"]))
                for row in equal_rows
            )
            < 2.0e-15
            and max(
                abs(
                    row["OmegaSquaredOverKv"]
                    - 24.0
                    * row["M"]
                    / ((row["M"] + 1.0) * (2.0 * row["M"] + 1.0))
                )
                for row in equal_rows
            )
            < 2.0e-14,
            {
                "terminalChi": equal_rows[-1]["chi"],
                "terminalOmegaSquaredOverKv": equal_rows[-1][
                    "OmegaSquaredOverKv"
                ],
            },
            "chi=1/(2M) and Omega^2/Kv=24M/[(M+1)(2M+1)]",
        ),
        check(
            "coherent prefactor tail power",
            abs(equal_power + 10.0 / 3.0) < 7.0e-4,
            equal_power,
            "binary64 log regression approaches -10/3",
        ),
        check(
            "comparable positive amplitude envelope",
            abs(comparable_power + 10.0 / 3.0) < 7.0e-4
            and max(row["chiOverUpper"] for row in comparable_rows) <= 1.0
            and max(row["multiplierRatioOverUpper"] for row in comparable_rows)
            <= 1.0,
            {
                "fittedTailPower": comparable_power,
                "maximumChiOverUpper": max(
                    row["chiOverUpper"] for row in comparable_rows
                ),
                "maximumMultiplierRatioOverUpper": max(
                    row["multiplierRatioOverUpper"] for row in comparable_rows
                ),
            },
            "a separate same-sign non-equal family obeys the uniform O(M^-1), O(M^-1), and M^-10/3 bounds",
        ),
        check(
            "phase boundary endpoints",
            abs(phases[0]["coherent"] - 10.0 / 7.0) < 2.0e-15
            and abs(phases[5]["coherent"] - 2.5) < 2.0e-15,
            [phases[0], phases[5]],
            "alpha<min(5/2,(10+3*beta)/7)",
        ),
        check(
            "Bessel heat-freezing inequality",
            max(row["XiOverUpper"] for row in bessel_rows) <= 1.0 + 2.0e-8,
            max(row["XiOverUpper"] for row in bessel_rows),
            "Xi_R<=R^4*L_R^2",
        ),
        check(
            "Bessel comparison indicators decrease",
            all(
                later[key] < earlier[key]
                for key in ("Theta", "Xi", "energyLossUpper")
                for earlier, later in zip(
                    bessel_rows[:-1], bessel_rows[1:], strict=True
                )
            ),
            {
                "terminal": bessel_rows[-1],
                "tailPowers": bessel_powers,
            },
            "Theta_R, Xi_R, and energy-loss upper bound decrease on the dyadic audit",
        ),
    ]
    all_passed = all(bool(row["passed"]) for row in checks)
    payload = {
        "schemaVersion": "r072b-target-row-coherence-independent-v1",
        "release": "R0.72B",
        "generatedAtUtc": utc_now(),
        "allPassed": all_passed,
        "checkCount": len(checks),
        "passedCheckCount": sum(bool(row["passed"]) for row in checks),
        "independence": {
            "importsProducer": False,
            "readsProducerResult": False,
            "rawParametersRepeatedLocally": True,
        },
        "arithmetic": {
            "format": "IEEE-754 binary64",
            "intervalArithmetic": False,
            "linearAlgebra": "NumPy complex128",
            "odeAndQuadrature": "SciPy DOP853 and adaptive QUADPACK",
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
        },
        "parameters": {
            "nu": NU,
            "d": D_MODULUS,
            "kappa": KAPPA,
            "Ky": K_Y,
            "Kz": K_Z,
            "q": Q_VALUE,
            "A0": A_0,
            "windowLength": WINDOW_LENGTH,
            "delta": DELTA,
            "multipliers": MULTIPLIERS.tolist(),
            "coefficients": COEFFICIENTS.tolist(),
            "matrixRadius": RADIUS,
            "matrixDimension": MATRIX_DIMENSION,
            "randomness": False,
        },
        "constants": {"Ckappa": c_kappa, "Ccross": c_cross},
        "finiteTargetRow": finite,
        "mixedExposure": exposure,
        "equalCarrierLedger": {
            "fittedTailPower": equal_power,
            "expectedPower": -10.0 / 3.0,
            "rows": equal_rows,
        },
        "comparableAmplitudeLedger": {
            "family": "z_l=1.2 on odd l and z_l=0.8 on even l",
            "fittedTailPower": comparable_power,
            "expectedPower": -10.0 / 3.0,
            "rows": comparable_rows,
        },
        "phaseBoundary": phases,
        "besselNoGo": {
            "tailPowers": bessel_powers,
            "rows": bessel_rows,
            "enhancedDissipationScope": (
                "A burn-in estimate acts on the tail after the burn-in time; "
                "the nonnegative pre-burn-in slope ledger remains part of the total."
            ),
        },
        "checks": checks,
        "scope": {
            "intervalArithmetic": False,
            "provesInfiniteLattice": False,
            "provesNSERegularity": False,
            "constructsNormalizedLowerFamily": False,
            "note": (
                "Finite matrices and binary64 quadrature corroborate the row "
                "identities and representative inequalities only."
            ),
        },
        "elapsedSeconds": time.perf_counter() - started,
    }
    if not all_passed:
        failed = [row["name"] for row in checks if not row["passed"]]
        raise AssertionError(f"independent checks failed: {failed}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    progress(
        args.progress_log,
        "independent-complete",
        allPassed=all_passed,
        elapsedSeconds=payload["elapsedSeconds"],
    )
    resource_snapshot(
        args.resource_log,
        "independent-complete",
        started,
        allPassed=all_passed,
    )
    emit(f"R0.72B independent audit passed in {payload['elapsedSeconds']:.2f}s")


if __name__ == "__main__":
    main()
