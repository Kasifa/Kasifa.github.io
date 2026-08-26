#!/usr/bin/env python3
"""Truncated Fourier-coset corroboration for the R0.71W amplitude-doped route.

This program solves a deterministic finite Fourier truncation of the exact
2.5D passive-component equation.  It checks the nonlinear prescribed-root
solve and the predicted amplitude-doped powers.  It is numerical
corroboration only: it does not prove convergence of the truncation, the
uniform infinite-dimensional implicit-function theorem, or any continuum
Navier--Stokes claim.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys
from typing import Callable

import numpy as np
import scipy
from scipy.integrate import simpson, solve_ivp
from scipy.optimize import least_squares


NU = 0.02
D = 8
K_Y = 1
K_Z = 1
BACKGROUND_FREQUENCY = 4
BACKGROUND_MULTIPLIER = 1.0
ALPHA = 1.5
N_ROOTS = 2
MODE_MULTIPLIERS = np.arange(1, 2 * N_ROOTS + 2, dtype=int)
SCALED_ROOTS = np.array([0.1, 0.2], dtype=float)
SCALED_WINDOW_LEFT = 0.05
PHYSICAL_WINDOW_LENGTH = 1.0
MAIN_Q_VALUES = (256, 512, 1024, 2048, 4096)
MAIN_TRUNCATION = 40
TRUNCATION_AUDIT_Q = 1024
TRUNCATION_AUDIT_RADII = (15, 30, 60)
CHARGE_CUTOFF_X = 30.0
CHARGE_GRID_POINTS = 3001
ROOT_RTOL = 2.0e-12
ROOT_ATOL = 2.0e-14
CHARGE_RTOL = 1.0e-9
CHARGE_ATOL = 1.0e-11
ROOT_RESIDUAL_TOLERANCE = 1.0e-10
TRUNCATION_RELATIVE_TOLERANCE = 2.0e-6


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Path for the machine-readable JSON audit result.",
    )
    return parser.parse_args()


def limiting_real_coefficients() -> np.ndarray:
    """Return the three real-block coefficients of the limiting response."""

    rates = 2.0 * NU * D * D * MODE_MULTIPLIERS[: N_ROOTS + 1] ** 2

    def psi(index: int, time: float) -> float:
        return -math.expm1(-rates[index] * time) / rates[index]

    matrix = np.array(
        [
            [psi(column, time) for column in range(1, N_ROOTS + 1)]
            for time in SCALED_ROOTS
        ],
        dtype=float,
    )
    right_hand_side = -np.array(
        [psi(0, time) for time in SCALED_ROOTS], dtype=float
    )
    return np.r_[1.0, np.linalg.solve(matrix, right_hand_side)]


def relative_difference(left: float, right: float) -> float:
    scale = max(abs(left), abs(right), np.finfo(float).tiny)
    return abs(left - right) / scale


def loglog_fit(q_values: list[int], values: list[float]) -> dict[str, float]:
    x_values = np.log(np.asarray(q_values, dtype=float))
    y_values = np.log(np.asarray(values, dtype=float))
    slope, intercept = np.polyfit(x_values, y_values, 1)
    fitted = slope * x_values + intercept
    residual = y_values - fitted
    total = y_values - np.mean(y_values)
    denominator = float(np.dot(total, total))
    r_squared = (
        1.0 - float(np.dot(residual, residual)) / denominator
        if denominator > 0.0
        else 1.0
    )
    return {
        "power": float(slope),
        "logCoefficient": float(intercept),
        "rSquared": r_squared,
    }


class CosetProblem:
    """One deterministic retained Fourier-coset problem."""

    def __init__(self, q: int, radius: int) -> None:
        self.q = q
        self.radius = radius
        self.amplitude = float(q**ALPHA)
        self.delta = self.amplitude / float(q * q)
        self.grid = np.arange(-radius, radius + 1, dtype=int)
        self.zero_index = radius
        self.shear_decay = (
            NU * D * D * MODE_MULTIPLIERS.astype(float) ** 2
        )
        self.scalar_decay = NU * (
            (K_Y / q + D * self.grid) ** 2 + (K_Z / q) ** 2
        )
        self.physical_wavenumber_squared = (
            (K_Y + D * q * self.grid) ** 2 + K_Z * K_Z
        ).astype(float)
        self.initial_state = np.zeros(self.grid.size, dtype=complex)
        phases = (1.0j, 1.0j, 1.0j, 1.0, 1.0)
        for multiplier, phase in zip(MODE_MULTIPLIERS, phases, strict=True):
            self.initial_state[self.zero_index - multiplier] += phase

    def rhs(self, z_values: np.ndarray) -> Callable[[float, np.ndarray], np.ndarray]:
        z_values = np.asarray(z_values, dtype=float)

        def evaluate(time: float, state: np.ndarray) -> np.ndarray:
            derivative = -self.scalar_decay * state
            for shift, coefficient, decay in zip(
                MODE_MULTIPLIERS, z_values, self.shear_decay, strict=True
            ):
                coupling = (
                    -1.0j
                    * K_Z
                    * self.delta
                    * coefficient
                    * math.exp(-decay * time)
                )
                derivative[shift:] += coupling * state[:-shift]
                derivative[:-shift] += coupling * state[shift:]
            return derivative

        return evaluate

    def integrate(
        self,
        z_values: np.ndarray,
        end_time: float,
        evaluation_times: np.ndarray,
        *,
        rtol: float,
        atol: float,
    ) -> np.ndarray:
        solution = solve_ivp(
            self.rhs(z_values),
            (0.0, end_time),
            self.initial_state,
            method="DOP853",
            t_eval=evaluation_times,
            rtol=rtol,
            atol=atol,
        )
        if not solution.success or solution.y.shape[1] != evaluation_times.size:
            raise RuntimeError(
                f"DOP853 failed for q={self.q}, R={self.radius}: "
                f"{solution.message}"
            )
        return solution.y

    def root_residual(self, free_z: np.ndarray) -> np.ndarray:
        z_values = np.r_[1.0, np.asarray(free_z, dtype=float)]
        states = self.integrate(
            z_values,
            float(SCALED_ROOTS[-1]),
            SCALED_ROOTS,
            rtol=ROOT_RTOL,
            atol=ROOT_ATOL,
        )
        target = states[self.zero_index, :]
        return np.r_[target.real, target.imag]

    def solve_roots(self, initial_z: np.ndarray) -> tuple[np.ndarray, dict[str, object]]:
        initial_z = np.asarray(initial_z, dtype=float)
        if initial_z.shape != (2 * N_ROOTS + 1,) or initial_z[0] != 1.0:
            raise ValueError("The continuation seed must contain five values with z1=1.")
        fit = least_squares(
            self.root_residual,
            initial_z[1:],
            method="lm",
            ftol=1.0e-13,
            xtol=1.0e-13,
            gtol=1.0e-13,
            max_nfev=1000,
        )
        z_values = np.r_[1.0, fit.x]
        residual = self.root_residual(fit.x)
        maximum_residual = float(np.max(np.abs(residual)))
        if not fit.success or maximum_residual > ROOT_RESIDUAL_TOLERANCE:
            raise RuntimeError(
                "Nonlinear root solve failed for "
                f"q={self.q}, R={self.radius}: success={fit.success}, "
                f"max residual={maximum_residual:.3e}, message={fit.message}"
            )
        return z_values, {
            "solver": "scipy.optimize.least_squares(method='lm')",
            "success": bool(fit.success),
            "message": str(fit.message),
            "functionEvaluations": int(fit.nfev),
            "optimality": float(fit.optimality),
            "cost": float(fit.cost),
            "residualRealVector": [float(value) for value in residual],
            "maximumRootResidual": maximum_residual,
        }

    def normalized_enstrophy(
        self, time: float, state: np.ndarray, z_values: np.ndarray
    ) -> float:
        scalar = 2.0 * float(
            np.sum(
                self.physical_wavenumber_squared
                * np.square(np.abs(state))
            )
        ) / float(self.q * self.q)
        shear = 2.0 * float(
            np.sum(
                (D * MODE_MULTIPLIERS) ** 2
                * np.square(z_values)
                * np.exp(-2.0 * self.shear_decay * time)
            )
        )
        background = (
            2.0
            * BACKGROUND_FREQUENCY**2
            * BACKGROUND_MULTIPLIER**2
            * math.exp(
                -2.0
                * NU
                * BACKGROUND_FREQUENCY**2
                * time
                / float(self.q * self.q)
            )
        )
        return scalar + shear + background

    def charge_tail_upper_bound(self, z_values: np.ndarray) -> float:
        """Bound the omitted x >= CHARGE_CUTOFF_X rotational charge."""

        absolute_z = np.abs(z_values)
        exponential_integral = 0.0
        for left, left_decay in enumerate(self.shear_decay):
            for right, right_decay in enumerate(self.shear_decay):
                total_decay = left_decay + right_decay
                exponential_integral += (
                    absolute_z[left]
                    * absolute_z[right]
                    * math.exp(-total_decay * CHARGE_CUTOFF_X)
                    / total_decay
                )
        initial_sector_mass = float(np.vdot(self.initial_state, self.initial_state).real)
        minimum_background_factor = math.exp(
            -2.0
            * NU
            * BACKGROUND_FREQUENCY**2
            * (
                PHYSICAL_WINDOW_LENGTH
                + SCALED_WINDOW_LEFT / float(self.q * self.q)
            )
        )
        return (
            4.0
            * initial_sector_mass
            * K_Z**2
            * self.amplitude**2
            * exponential_integral
            / (
                BACKGROUND_FREQUENCY**2
                * BACKGROUND_MULTIPLIER**2
                * self.q**4
                * minimum_background_factor
            )
        )

    def metrics(self, z_values: np.ndarray) -> dict[str, object]:
        root_states = self.integrate(
            z_values,
            float(SCALED_ROOTS[-1]),
            SCALED_ROOTS,
            rtol=ROOT_RTOL,
            atol=ROOT_ATOL,
        )
        normalized_slopes: list[float] = []
        atom_proxies: list[float] = []
        root_enstrophies: list[float] = []
        root_values: list[dict[str, float]] = []
        root_rhs = self.rhs(z_values)
        for time, state in zip(SCALED_ROOTS, root_states.T, strict=True):
            target_value = state[self.zero_index]
            scaled_target_derivative = root_rhs(float(time), state)[self.zero_index]
            normalized_slope = abs(scaled_target_derivative) / self.delta
            enstrophy = self.normalized_enstrophy(float(time), state, z_values)
            atom_proxy = (
                2.0
                * (self.amplitude**2 / self.q**2)
                * normalized_slope**2
                / enstrophy
            )
            root_values.append(
                {"real": float(target_value.real), "imaginary": float(target_value.imag)}
            )
            normalized_slopes.append(float(normalized_slope))
            atom_proxies.append(float(atom_proxy))
            root_enstrophies.append(float(enstrophy))

        charge_times = np.linspace(
            SCALED_WINDOW_LEFT, CHARGE_CUTOFF_X, CHARGE_GRID_POINTS
        )
        charge_states = self.integrate(
            z_values,
            CHARGE_CUTOFF_X,
            charge_times,
            rtol=CHARGE_RTOL,
            atol=CHARGE_ATOL,
        )
        charge_integrand = np.empty(charge_times.size, dtype=float)
        sampled_enstrophy = np.empty(charge_times.size, dtype=float)
        for index, (time, state) in enumerate(
            zip(charge_times, charge_states.T, strict=True)
        ):
            convolution = np.zeros_like(state)
            for shift, coefficient, decay in zip(
                MODE_MULTIPLIERS, z_values, self.shear_decay, strict=True
            ):
                coupling = (
                    -1.0j
                    * K_Z
                    * coefficient
                    * math.exp(-decay * float(time))
                )
                convolution[shift:] += coupling * state[:-shift]
                convolution[:-shift] += coupling * state[shift:]
            enstrophy = self.normalized_enstrophy(
                float(time), state, z_values
            )
            retained_hminus1 = float(
                np.sum(
                    np.square(np.abs(convolution))
                    / self.physical_wavenumber_squared
                )
            )
            charge_integrand[index] = (
                2.0
                * self.amplitude**2
                * retained_hminus1
                / (self.q**4 * enstrophy)
            )
            sampled_enstrophy[index] = enstrophy

        quadrature_charge = float(simpson(charge_integrand, x=charge_times))
        tail_upper_bound = self.charge_tail_upper_bound(z_values)
        charge_upper_bound = quadrature_charge + tail_upper_bound
        if not (
            math.isfinite(quadrature_charge)
            and quadrature_charge > 0.0
            and math.isfinite(charge_upper_bound)
        ):
            raise RuntimeError(
                f"Invalid rotational charge for q={self.q}, R={self.radius}."
            )
        return {
            "q": self.q,
            "truncationRadius": self.radius,
            "amplitude": self.amplitude,
            "delta": self.delta,
            "z": [float(value) for value in z_values],
            "rootValues": root_values,
            "normalizedRootSlopes": normalized_slopes,
            "minimumNormalizedRootSlope": min(normalized_slopes),
            "normalizedRootEnstrophy": root_enstrophies,
            "atomProxyByRoot": atom_proxies,
            "secondRootAtomProxy": atom_proxies[1],
            "retainedCosetHminus1LCharge": quadrature_charge,
            "chargeTailUpperBound": tail_upper_bound,
            "retainedCosetHminus1LChargeUpperBound": charge_upper_bound,
            "chargeTailRelativeUpperBound": tail_upper_bound / quadrature_charge,
            "chargeIntegration": {
                "scaledLeft": SCALED_WINDOW_LEFT,
                "scaledCutoff": CHARGE_CUTOFF_X,
                "gridPoints": CHARGE_GRID_POINTS,
                "quadrature": "scipy.integrate.simpson",
                "tailBoundExtendsTo": "infinity",
            },
            "sampledNormalizedEnstrophy": {
                "minimum": float(np.min(sampled_enstrophy)),
                "maximum": float(np.max(sampled_enstrophy)),
            },
        }


def run_case(
    q: int, radius: int, initial_z: np.ndarray
) -> tuple[np.ndarray, dict[str, object]]:
    problem = CosetProblem(q, radius)
    z_values, solver = problem.solve_roots(initial_z)
    metrics = problem.metrics(z_values)
    metrics["rootSolve"] = solver
    return z_values, metrics


def make_check(
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


def audit() -> dict[str, object]:
    limiting = limiting_real_coefficients()
    continuation_z = np.r_[limiting, np.zeros(N_ROOTS, dtype=float)]
    main_cases: list[dict[str, object]] = []
    for q in MAIN_Q_VALUES:
        continuation_z, case = run_case(q, MAIN_TRUNCATION, continuation_z)
        main_cases.append(case)

    reference = next(
        case for case in main_cases if case["q"] == TRUNCATION_AUDIT_Q
    )
    reference_z = np.asarray(reference["z"], dtype=float)
    truncation_cases: list[dict[str, object]] = []
    for radius in TRUNCATION_AUDIT_RADII:
        _, case = run_case(TRUNCATION_AUDIT_Q, radius, reference_z)
        case_z = np.asarray(case["z"], dtype=float)
        case["comparisonToR40"] = {
            "maximumZDifference": float(np.max(np.abs(case_z - reference_z))),
            "secondRootSlopeRelativeDifference": relative_difference(
                case["normalizedRootSlopes"][1],
                reference["normalizedRootSlopes"][1],
            ),
            "secondRootAtomRelativeDifference": relative_difference(
                case["secondRootAtomProxy"], reference["secondRootAtomProxy"]
            ),
            "rotationalChargeRelativeDifference": relative_difference(
                case["retainedCosetHminus1LCharge"],
                reference["retainedCosetHminus1LCharge"],
            ),
        }
        truncation_cases.append(case)

    q_values = [int(case["q"]) for case in main_cases]
    atom_values = [float(case["secondRootAtomProxy"]) for case in main_cases]
    charge_values = [
        float(case["retainedCosetHminus1LCharge"]) for case in main_cases
    ]
    atom_to_charge = [
        atom / charge for atom, charge in zip(atom_values, charge_values, strict=True)
    ]
    slopes = [float(case["normalizedRootSlopes"][1]) for case in main_cases]
    fits = {
        "secondRootAtomProxy": {
            **loglog_fit(q_values, atom_values),
            "predictedPower": 2.0 * ALPHA - 2.0,
        },
        "retainedCosetHminus1LCharge": {
            **loglog_fit(q_values, charge_values),
            "predictedPower": 2.0 * ALPHA - 4.0,
        },
        "atomToRotationalCharge": {
            **loglog_fit(q_values, atom_to_charge),
            "predictedPower": 2.0,
        },
        "normalizedSecondRootSlope": {
            **loglog_fit(q_values, slopes),
            "predictedPower": 0.0,
        },
    }

    root_residuals = [
        float(case["rootSolve"]["maximumRootResidual"]) for case in main_cases
    ] + [
        float(case["rootSolve"]["maximumRootResidual"])
        for case in truncation_cases
    ]
    truncation_differences = [
        max(
            float(value)
            for key, value in case["comparisonToR40"].items()
            if key != "maximumZDifference"
        )
        for case in truncation_cases
    ]
    maximum_z_difference = max(
        float(case["comparisonToR40"]["maximumZDifference"])
        for case in truncation_cases
    )
    checks = [
        make_check(
            "all nonlinear roots close",
            max(root_residuals) <= ROOT_RESIDUAL_TOLERANCE,
            max(root_residuals),
            f"maximum residual <= {ROOT_RESIDUAL_TOLERANCE}",
        ),
        make_check(
            "second root remains simple",
            min(slopes) >= 0.05,
            min(slopes),
            "minimum |a_t|/A^2 >= 0.05",
        ),
        make_check(
            "atom proxy has predicted power",
            abs(fits["secondRootAtomProxy"]["power"] - (2.0 * ALPHA - 2.0))
            <= 0.15,
            fits["secondRootAtomProxy"]["power"],
            f"within 0.15 of {2.0 * ALPHA - 2.0}",
        ),
        make_check(
            "rotational charge has predicted power",
            abs(
                fits["retainedCosetHminus1LCharge"]["power"]
                - (2.0 * ALPHA - 4.0)
            )
            <= 0.15,
            fits["retainedCosetHminus1LCharge"]["power"],
            f"within 0.15 of {2.0 * ALPHA - 4.0}",
        ),
        make_check(
            "retained-coset charge is truncation-stable",
            max(truncation_differences) <= TRUNCATION_RELATIVE_TOLERANCE,
            max(truncation_differences),
            f"maximum relative difference <= {TRUNCATION_RELATIVE_TOLERANCE}",
        ),
        make_check(
            "root parameters are truncation-stable",
            maximum_z_difference <= 2.0e-6,
            maximum_z_difference,
            "maximum absolute z difference <= 2e-6",
        ),
        make_check(
            "charge tail is negligible",
            max(
                float(case["chargeTailRelativeUpperBound"])
                for case in main_cases + truncation_cases
            )
            <= 1.0e-12,
            max(
                float(case["chargeTailRelativeUpperBound"])
                for case in main_cases + truncation_cases
            ),
            "analytic tail upper bound / quadrature <= 1e-12",
        ),
    ]
    passed = all(bool(check["passed"]) for check in checks)
    return {
        "schemaVersion": 1,
        "audit": "R0.71W truncated Fourier-coset nonlinear corroboration",
        "status": "passed" if passed else "failed",
        "passed": passed,
        "boundary": (
            "Finite retained-coset numerical corroboration only. It does not "
            "prove spectral-truncation convergence, the uniform continuum "
            "implicit-function theorem, or any Navier--Stokes regularity claim."
        ),
        "determinism": (
            "No random numbers are used; q values, truncations, tolerances, "
            "initial phases, continuation order, and quadrature grid are fixed."
        ),
        "software": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "odeSolver": "scipy.integrate.solve_ivp(method='DOP853')",
            "rootSolver": "scipy.optimize.least_squares(method='lm')",
        },
        "parameters": {
            "viscosity": NU,
            "d": D,
            "targetKy": K_Y,
            "targetKz": K_Z,
            "backgroundFrequency": BACKGROUND_FREQUENCY,
            "backgroundAmplitudeLaw": "B_q = q * A_q",
            "alpha": ALPHA,
            "amplitudeLaw": "A_q = q^alpha",
            "modeMultipliers": MODE_MULTIPLIERS.tolist(),
            "initialPositiveKzPhases": ["i", "i", "i", "1", "1"],
            "scaledRoots": SCALED_ROOTS.tolist(),
            "scaledWindowLeft": SCALED_WINDOW_LEFT,
            "physicalWindowLength": PHYSICAL_WINDOW_LENGTH,
            "mainQValues": list(MAIN_Q_VALUES),
            "mainTruncationRadius": MAIN_TRUNCATION,
            "continuationOrder": list(MAIN_Q_VALUES),
            "truncationAuditQ": TRUNCATION_AUDIT_Q,
            "truncationAuditRadii": list(TRUNCATION_AUDIT_RADII),
            "limitingRealBlockCoefficients": limiting.tolist(),
        },
        "mainContinuation": main_cases,
        "truncationAudit": truncation_cases,
        "powerFits": fits,
        "checks": checks,
    }


def write_result(path: Path, result: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    args = parse_args()
    try:
        result = audit()
    except Exception as error:
        failure = {
            "schemaVersion": 1,
            "audit": "R0.71W truncated Fourier-coset nonlinear corroboration",
            "status": "error",
            "passed": False,
            "boundary": "Finite retained-coset numerical corroboration only.",
            "errorType": type(error).__name__,
            "error": str(error),
        }
        write_result(args.output, failure)
        raise
    write_result(args.output, result)
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
