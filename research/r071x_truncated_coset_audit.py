#!/usr/bin/env python3
"""Nonlinear retained-coset corroboration for the R0.71X endpoint branch.

The audit fixes a small rescaled coupling ``delta`` and uses the endpoint
amplitude law ``A_q = delta*q^2``.  It solves the exact finite Fourier-coset
ODE and the four nonlinear prescribed-root equations, then reconstructs the
root slopes, initial H1 data, prescribed atom proxies, endpoint quotient, and
the full retained-coset projected-rotational charge.

The annular multiplier is not locked in this finite model, so every atom is
explicitly named ``atomProxy``.  This computation is numerical corroboration
only.  It does not prove convergence of the Fourier truncation, the uniform
continuum IFT, any estimate for all triangular solutions, or Navier--Stokes
regularity.
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
# R0.71W allows arbitrary fixed b_0>0.  The old truncated audit chose b_0=1;
# R0.71X locks b_0=1/Q to match its producer and independent reconstruction.
BACKGROUND_MULTIPLIER = 1.0 / BACKGROUND_FREQUENCY
DELTA = 1.0 / 128.0
N_ROOTS = 2
MODE_MULTIPLIERS = np.arange(1, 2 * N_ROOTS + 2, dtype=int)
INITIAL_PHASES = (1.0j, 1.0j, 1.0j, 1.0, 1.0)
SCALED_ROOTS = np.array([0.1, 0.2], dtype=float)
SCALED_WINDOW_LEFT = 0.05
PHYSICAL_WINDOW_LENGTH = 1.0

MAIN_Q_VALUES = (256, 512, 1024, 2048, 4096)
MAIN_TRUNCATION = 40
TRUNCATION_AUDIT_Q = 1024
TRUNCATION_AUDIT_RADII = (15, 30, 60)

CHARGE_CUTOFF_X = 30.0
CHARGE_GRID_POINTS = 3001
TARGET_SCAN_POINTS = 12001
ROOT_NEIGHBORHOOD_HALF_WIDTH = 0.02
TARGET_TAIL_EVALUATION_X = 60.0
ROOT_RTOL = 2.0e-12
ROOT_ATOL = 2.0e-14
CHARGE_RTOL = 1.0e-9
CHARGE_ATOL = 1.0e-11
TARGET_SCAN_RTOL = 2.0e-11
TARGET_SCAN_ATOL = 2.0e-13
ROOT_RESIDUAL_TOLERANCE = 1.0e-10
PHYSICAL_ROOT_RESIDUAL_TOLERANCE = 1.0e-9
SIMPLE_THETA_TOLERANCE = 0.05
POWER_TOLERANCE = 0.12
TRUNCATION_RELATIVE_TOLERANCE = 2.0e-6
TRUNCATION_Z_TOLERANCE = 2.0e-6
ENDPOINT_IDENTITY_TOLERANCE = 5.0e-13
NO_EXTRA_ROOT_SEPARATION_TOLERANCE = 1.0e-8
ROOT_NEIGHBORHOOD_DERIVATIVE_TOLERANCE = 1.0e-5
TAIL_PROXY_RELATIVE_DRIFT_TOLERANCE = 1.0e-7

# With |m_*(k_*)| = kappa_* = 1, normalized-Haar Parseval would give
# 2 |a_t|^2/Y.  The actual multiplier is intentionally not declared here;
# hence this factor defines an atom proxy rather than the released atom J_*.
ATOM_PROXY_FACTOR = 2.0


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


def limiting_response_block_diagnostics() -> dict[str, object]:
    """Record conditioning of the real and imaginary IFT response blocks."""

    rates = 2.0 * NU * D * D * MODE_MULTIPLIERS.astype(float) ** 2

    def psi(index: int, time: float) -> float:
        return -math.expm1(-rates[index] * time) / rates[index]

    blocks = {
        "real": np.array(
            [[psi(index, time) for index in (1, 2)] for time in SCALED_ROOTS],
            dtype=float,
        ),
        "imaginary": np.array(
            [[psi(index, time) for index in (3, 4)] for time in SCALED_ROOTS],
            dtype=float,
        ),
    }
    result: dict[str, object] = {}
    for name, block in blocks.items():
        singular_values = np.linalg.svd(block, compute_uv=False)
        result[name] = {
            "matrix": block.tolist(),
            "determinant": float(np.linalg.det(block)),
            "conditionNumber2": float(np.linalg.cond(block)),
            "inverseNorm2": float(np.linalg.norm(np.linalg.inv(block), 2)),
            "singularValues": singular_values.tolist(),
        }
    result["interpretation"] = (
        "The imaginary block is invertible but substantially less well "
        "conditioned than the real block. Consequently an O(delta) divided-"
        "map defect may carry a large fixed coefficient in z4,z5. This finite "
        "conditioning diagnostic is not a validated continuum IFT radius."
    )
    return result


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


def complex_record(value: complex) -> dict[str, float]:
    return {
        "real": float(value.real),
        "imaginary": float(value.imag),
        "absolute": float(abs(value)),
    }


class CosetProblem:
    """One deterministic retained positive-Kz Fourier-coset problem."""

    def __init__(self, q: int, radius: int) -> None:
        if radius < int(MODE_MULTIPLIERS[-1]):
            raise ValueError("truncation radius does not contain the initial seed")
        self.q = q
        self.radius = radius
        self.delta = DELTA
        self.amplitude = self.delta * float(q * q)
        self.background_amplitude = (
            BACKGROUND_MULTIPLIER * self.amplitude * float(q)
        )
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
        for multiplier, phase in zip(
            MODE_MULTIPLIERS, INITIAL_PHASES, strict=True
        ):
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
            raise ValueError("continuation seed must contain five values with z1=1")
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
                "nonlinear root solve failed for "
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
            "maximumDimensionlessRootResidual": maximum_residual,
            "maximumPhysicalRootResidual": maximum_residual * self.amplitude,
        }

    def normalized_enstrophy(
        self, time: float, state: np.ndarray, z_values: np.ndarray
    ) -> float:
        """Return Y/(A_q^2 q^2) at scaled time x."""

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

    def exact_initial_data(self, z_values: np.ndarray) -> dict[str, float]:
        """Return exact finite-datum energy, enstrophy, and D=E+Y."""

        scalar_energy = (
            2.0
            * self.amplitude**2
            * float(np.vdot(self.initial_state, self.initial_state).real)
        )
        scalar_enstrophy = (
            2.0
            * self.amplitude**2
            * float(
                np.sum(
                    self.physical_wavenumber_squared
                    * np.square(np.abs(self.initial_state))
                )
            )
        )
        physical_shear_modes = D * MODE_MULTIPLIERS.astype(float) * self.q
        shear_energy = 2.0 * self.amplitude**2 * float(
            np.sum(np.square(z_values))
        )
        shear_enstrophy = 2.0 * self.amplitude**2 * float(
            np.sum(np.square(physical_shear_modes) * np.square(z_values))
        )
        background_energy = 2.0 * self.background_amplitude**2
        background_enstrophy = (
            2.0
            * BACKGROUND_FREQUENCY**2
            * self.background_amplitude**2
        )
        energy = scalar_energy + shear_energy + background_energy
        enstrophy = scalar_enstrophy + shear_enstrophy + background_enstrophy
        data_size = energy + enstrophy
        return {
            "energy": energy,
            "enstrophy": enstrophy,
            "D": data_size,
            "DNormalized": data_size / (self.amplitude**2 * self.q**2),
            "scalarEnergy": scalar_energy,
            "scalarEnstrophy": scalar_enstrophy,
            "shearEnergy": shear_energy,
            "shearEnstrophy": shear_enstrophy,
            "backgroundEnergy": background_energy,
            "backgroundEnstrophy": background_enstrophy,
        }

    def charge_tail_upper_bound(self, z_values: np.ndarray) -> float:
        """Bound the omitted scaled-time interval x >= CHARGE_CUTOFF_X."""

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
        initial_sector_mass = float(
            np.vdot(self.initial_state, self.initial_state).real
        )
        minimum_background_factor = math.exp(
            -2.0
            * NU
            * BACKGROUND_FREQUENCY**2
            * (
                PHYSICAL_WINDOW_LENGTH
                + SCALED_WINDOW_LEFT / float(self.q * self.q)
            )
        )
        # This deliberately uses H^-1 <= L2 on the normalized torus.  It is
        # conservative; no selected-output or target-shell deletion is made.
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

    def root_metrics(
        self, z_values: np.ndarray
    ) -> tuple[list[dict[str, object]], np.ndarray]:
        root_states = self.integrate(
            z_values,
            float(SCALED_ROOTS[-1]),
            SCALED_ROOTS,
            rtol=ROOT_RTOL,
            atol=ROOT_ATOL,
        )
        root_rhs = self.rhs(z_values)
        roots: list[dict[str, object]] = []
        for index, (time, state) in enumerate(
            zip(SCALED_ROOTS, root_states.T, strict=True), start=1
        ):
            target_value = complex(state[self.zero_index])
            scaled_target_derivative = complex(
                root_rhs(float(time), state)[self.zero_index]
            )
            theta = scaled_target_derivative / self.delta
            physical_slope = self.amplitude**2 * theta
            normalized_enstrophy = self.normalized_enstrophy(
                float(time), state, z_values
            )
            physical_enstrophy = (
                self.amplitude**2 * self.q**2 * normalized_enstrophy
            )
            atom_proxy = (
                ATOM_PROXY_FACTOR
                * abs(physical_slope) ** 2
                / physical_enstrophy
            )
            roots.append(
                {
                    "rootIndex": index,
                    "scaledTime": float(time),
                    "physicalTimeFromLaunch": float(time / self.q**2),
                    "dimensionlessTargetValue": complex_record(target_value),
                    "physicalTargetResidual": complex_record(
                        self.amplitude * target_value
                    ),
                    "scaledTargetDerivative": complex_record(
                        scaled_target_derivative
                    ),
                    "Theta": complex_record(theta),
                    "physicalSlope": complex_record(physical_slope),
                    "normalizedRootEnstrophy": normalized_enstrophy,
                    "physicalRootEnstrophy": physical_enstrophy,
                    "atomProxy": atom_proxy,
                }
            )
        return roots, root_states

    def retained_charge(
        self, z_values: np.ndarray
    ) -> dict[str, object]:
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
            # Pair the +/- Kz sectors, restore A_q^4/Y, and use dt=dx/q^2.
            charge_integrand[index] = (
                2.0
                * self.amplitude**2
                * retained_hminus1
                / (self.q**4 * enstrophy)
            )
            sampled_enstrophy[index] = enstrophy

        quadrature_charge = float(simpson(charge_integrand, x=charge_times))
        tail_upper_bound = self.charge_tail_upper_bound(z_values)
        upper_bound = quadrature_charge + tail_upper_bound
        if not (
            math.isfinite(quadrature_charge)
            and quadrature_charge > 0.0
            and math.isfinite(upper_bound)
        ):
            raise RuntimeError(
                f"invalid retained charge for q={self.q}, R={self.radius}"
            )
        return {
            "retainedFullCosetHminus1LCharge": quadrature_charge,
            "chargeTailUpperBound": tail_upper_bound,
            "retainedFullCosetHminus1LChargeUpperBound": upper_bound,
            "chargeTailRelativeUpperBound": tail_upper_bound / quadrature_charge,
            "chargeIntegration": {
                "scaledLeft": SCALED_WINDOW_LEFT,
                "scaledCutoff": CHARGE_CUTOFF_X,
                "gridPoints": CHARGE_GRID_POINTS,
                "quadrature": "scipy.integrate.simpson",
                "tailBoundExtendsTo": "infinity",
                "physicalTimeJacobian": "dt = dx/q^2",
            },
            "sampledNormalizedEnstrophy": {
                "minimum": float(np.min(sampled_enstrophy)),
                "maximum": float(np.max(sampled_enstrophy)),
            },
        }

    def target_scan(self, z_values: np.ndarray) -> dict[str, object]:
        """Numerically probe the finite interval and integrating-factor tail.

        This is deliberately only corroboration.  The analytic half-line
        lemma, not a grid scan, is responsible for excluding additional
        continuum roots in a theorem.
        """

        scan_times = np.linspace(
            SCALED_WINDOW_LEFT, CHARGE_CUTOFF_X, TARGET_SCAN_POINTS
        )
        evaluation_times = np.r_[scan_times, TARGET_TAIL_EVALUATION_X]
        states = self.integrate(
            z_values,
            TARGET_TAIL_EVALUATION_X,
            evaluation_times,
            rtol=TARGET_SCAN_RTOL,
            atol=TARGET_SCAN_ATOL,
        )
        scan_states = states[:, :-1]
        tail_state = states[:, -1]
        target_values = scan_states[self.zero_index, :]
        target_real = target_values.real
        target_derivative_real = np.empty(scan_times.size, dtype=float)
        rhs = self.rhs(z_values)
        for index, (time, state) in enumerate(
            zip(scan_times, scan_states.T, strict=True)
        ):
            target_derivative_real[index] = float(
                rhs(float(time), state)[self.zero_index].real
            )

        neighborhoods: list[dict[str, object]] = []
        outside_mask = np.ones(scan_times.size, dtype=bool)
        for root_index, root_time in enumerate(SCALED_ROOTS, start=1):
            left = float(root_time - ROOT_NEIGHBORHOOD_HALF_WIDTH)
            right = float(root_time + ROOT_NEIGHBORHOOD_HALF_WIDTH)
            mask = (scan_times >= left) & (scan_times <= right)
            outside_mask &= ~mask
            derivative = target_derivative_real[mask]
            values = target_real[mask]
            root_sign = -1.0 if root_index == 1 else 1.0
            signed_derivative = root_sign * derivative
            left_value = float(values[0])
            right_value = float(values[-1])
            neighborhoods.append(
                {
                    "rootIndex": root_index,
                    "left": left,
                    "right": right,
                    "leftRealTarget": left_value,
                    "rightRealTarget": right_value,
                    "endpointSignChange": left_value * right_value < 0.0,
                    "expectedDerivativeSign": (
                        "negative" if root_sign < 0.0 else "positive"
                    ),
                    "minimumSignedDerivative": float(np.min(signed_derivative)),
                    "maximumSignedDerivative": float(np.max(signed_derivative)),
                    "strictlyMonotone": bool(
                        np.min(signed_derivative)
                        >= ROOT_NEIGHBORHOOD_DERIVATIVE_TOLERANCE
                    ),
                }
            )

        segments = (
            (
                "beforeFirstRootNeighborhood",
                SCALED_WINDOW_LEFT,
                float(SCALED_ROOTS[0] - ROOT_NEIGHBORHOOD_HALF_WIDTH),
            ),
            (
                "betweenRootNeighborhoods",
                float(SCALED_ROOTS[0] + ROOT_NEIGHBORHOOD_HALF_WIDTH),
                float(SCALED_ROOTS[1] - ROOT_NEIGHBORHOOD_HALF_WIDTH),
            ),
            (
                "afterSecondRootNeighborhood",
                float(SCALED_ROOTS[1] + ROOT_NEIGHBORHOOD_HALF_WIDTH),
                CHARGE_CUTOFF_X,
            ),
        )
        segment_records: list[dict[str, object]] = []
        for name, left, right in segments:
            mask = (scan_times >= left) & (scan_times <= right)
            values = target_real[mask]
            minimum = float(np.min(values))
            maximum = float(np.max(values))
            minimum_absolute = float(np.min(np.abs(values)))
            one_sign = minimum > 0.0 or maximum < 0.0
            segment_records.append(
                {
                    "name": name,
                    "left": left,
                    "right": right,
                    "minimumRealTarget": minimum,
                    "maximumRealTarget": maximum,
                    "minimumAbsoluteRealTarget": minimum_absolute,
                    "oneStrictSign": bool(one_sign),
                }
            )

        target_at_cutoff = complex(target_values[-1])
        target_at_tail = complex(tail_state[self.zero_index])
        target_decay = float(self.scalar_decay[self.zero_index])
        integrating_factor_cutoff = math.exp(
            target_decay * CHARGE_CUTOFF_X
        ) * target_at_cutoff
        integrating_factor_tail = math.exp(
            target_decay * TARGET_TAIL_EVALUATION_X
        ) * target_at_tail
        tail_relative_drift = abs(
            integrating_factor_cutoff - integrating_factor_tail
        ) / max(
            abs(integrating_factor_cutoff),
            abs(integrating_factor_tail),
            np.finfo(float).tiny,
        )
        minimum_outside_separation = float(
            np.min(np.abs(target_real[outside_mask]))
        )
        no_extra_root_scan_passed = (
            all(bool(record["endpointSignChange"]) for record in neighborhoods)
            and all(bool(record["strictlyMonotone"]) for record in neighborhoods)
            and all(bool(record["oneStrictSign"]) for record in segment_records)
            and minimum_outside_separation
            >= NO_EXTRA_ROOT_SEPARATION_TOLERANCE
        )
        tail_proxy_passed = (
            integrating_factor_cutoff.real * integrating_factor_tail.real > 0.0
            and min(
                abs(integrating_factor_cutoff.real),
                abs(integrating_factor_tail.real),
            )
            >= NO_EXTRA_ROOT_SEPARATION_TOLERANCE
            and tail_relative_drift <= TAIL_PROXY_RELATIVE_DRIFT_TOLERANCE
        )
        return {
            "boundary": (
                "Dense-grid no-extra-root and integrating-factor tail "
                "corroboration only; the analytic half-line lemma is required "
                "for a continuum theorem."
            ),
            "scanInterval": [SCALED_WINDOW_LEFT, CHARGE_CUTOFF_X],
            "scanPoints": TARGET_SCAN_POINTS,
            "rootNeighborhoodHalfWidth": ROOT_NEIGHBORHOOD_HALF_WIDTH,
            "rootNeighborhoods": neighborhoods,
            "outsideSegments": segment_records,
            "minimumOutsideNeighborhoodRealSeparation": (
                minimum_outside_separation
            ),
            "noExtraRealRootScanPassed": no_extra_root_scan_passed,
            "integratingFactor": {
                "targetDecay": target_decay,
                "cutoffX": CHARGE_CUTOFF_X,
                "tailEvaluationX": TARGET_TAIL_EVALUATION_X,
                "cutoffValue": complex_record(integrating_factor_cutoff),
                "tailLimitProxy": complex_record(integrating_factor_tail),
                "relativeDrift": tail_relative_drift,
                "sameNonzeroRealSign": (
                    integrating_factor_cutoff.real
                    * integrating_factor_tail.real
                    > 0.0
                ),
                "minimumRealSeparation": min(
                    abs(integrating_factor_cutoff.real),
                    abs(integrating_factor_tail.real),
                ),
                "tailProxyPassed": tail_proxy_passed,
            },
        }

    def metrics(self, z_values: np.ndarray) -> dict[str, object]:
        roots, _ = self.root_metrics(z_values)
        limiting_tangent = np.r_[
            limiting_real_coefficients(), np.zeros(N_ROOTS, dtype=float)
        ]
        z_correction = z_values - limiting_tangent
        initial_data = self.exact_initial_data(z_values)
        prescribed_atom_sum = math.fsum(
            float(root["atomProxy"]) for root in roots
        )
        d_one_third = initial_data["D"] ** (1.0 / 3.0)
        atom_sum_over_d_one_third = prescribed_atom_sum / d_one_third
        endpoint_coefficient = atom_sum_over_d_one_third / self.delta ** (
            4.0 / 3.0
        )
        normalized_factor_sum = math.fsum(
            ATOM_PROXY_FACTOR
            * float(root["Theta"]["absolute"]) ** 2
            / float(root["normalizedRootEnstrophy"])
            for root in roots
        ) / initial_data["DNormalized"] ** (1.0 / 3.0)
        endpoint_identity_error = relative_difference(
            endpoint_coefficient, normalized_factor_sum
        )
        charge = self.retained_charge(z_values)
        target_scan = self.target_scan(z_values)
        charge_value = float(charge["retainedFullCosetHminus1LCharge"])
        return {
            "q": self.q,
            "truncationRadius": self.radius,
            "delta": self.delta,
            "amplitude": self.amplitude,
            "backgroundAmplitude": self.background_amplitude,
            "z": [float(value) for value in z_values],
            "limitingTangentZ": limiting_tangent.tolist(),
            "zMinusLimitingTangent": z_correction.tolist(),
            "zMinusLimitingTangentOverDelta": (
                z_correction / self.delta
            ).tolist(),
            "maximumAbsZCorrectionOverDelta": float(
                np.max(np.abs(z_correction / self.delta))
            ),
            "roots": roots,
            "minimumTheta": min(float(root["Theta"]["absolute"]) for root in roots),
            "initialData": initial_data,
            "atomProxyByRoot": [float(root["atomProxy"]) for root in roots],
            "completePrescribedAtomProxySum": prescribed_atom_sum,
            "completePrescribedAtomProxySumOverDOneThird": (
                atom_sum_over_d_one_third
            ),
            "endpointCoefficientProxy": endpoint_coefficient,
            "endpointCoefficientFromNormalizedFactors": normalized_factor_sum,
            "endpointIdentityRelativeError": endpoint_identity_error,
            "atomProxySumToRetainedCharge": prescribed_atom_sum / charge_value,
            "noExtraRootCorroboration": target_scan,
            **charge,
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
    response_block_diagnostics = limiting_response_block_diagnostics()
    continuation_z = np.r_[limiting, np.zeros(N_ROOTS, dtype=float)]
    main_cases: list[dict[str, object]] = []
    for q_value in MAIN_Q_VALUES:
        continuation_z, case = run_case(
            q_value, MAIN_TRUNCATION, continuation_z
        )
        main_cases.append(case)

    reference = next(
        case for case in main_cases if case["q"] == TRUNCATION_AUDIT_Q
    )
    reference_z = np.asarray(reference["z"], dtype=float)
    truncation_cases: list[dict[str, object]] = []
    for radius in TRUNCATION_AUDIT_RADII:
        _, case = run_case(TRUNCATION_AUDIT_Q, radius, reference_z)
        case_z = np.asarray(case["z"], dtype=float)
        root_differences = [
            {
                "rootIndex": index + 1,
                "ThetaRelativeDifference": relative_difference(
                    float(case["roots"][index]["Theta"]["absolute"]),
                    float(reference["roots"][index]["Theta"]["absolute"]),
                ),
                "normalizedEnstrophyRelativeDifference": relative_difference(
                    float(case["roots"][index]["normalizedRootEnstrophy"]),
                    float(reference["roots"][index]["normalizedRootEnstrophy"]),
                ),
                "atomProxyRelativeDifference": relative_difference(
                    float(case["roots"][index]["atomProxy"]),
                    float(reference["roots"][index]["atomProxy"]),
                ),
            }
            for index in range(N_ROOTS)
        ]
        case["comparisonToR40"] = {
            "maximumZDifference": float(np.max(np.abs(case_z - reference_z))),
            "rootDifferences": root_differences,
            "initialDRelativeDifference": relative_difference(
                float(case["initialData"]["D"]),
                float(reference["initialData"]["D"]),
            ),
            "atomProxySumRelativeDifference": relative_difference(
                float(case["completePrescribedAtomProxySum"]),
                float(reference["completePrescribedAtomProxySum"]),
            ),
            "endpointCoefficientRelativeDifference": relative_difference(
                float(case["endpointCoefficientProxy"]),
                float(reference["endpointCoefficientProxy"]),
            ),
            "retainedChargeRelativeDifference": relative_difference(
                float(case["retainedFullCosetHminus1LCharge"]),
                float(reference["retainedFullCosetHminus1LCharge"]),
            ),
        }
        truncation_cases.append(case)

    q_values = [int(case["q"]) for case in main_cases]
    fit_specification = {
        "amplitude": 2.0,
        "physicalSecondRootSlope": 4.0,
        "initialDataD": 6.0,
        "completePrescribedAtomProxySum": 2.0,
        "secondRootAtomProxy": 2.0,
        "completePrescribedAtomProxySumOverDOneThird": 0.0,
        "endpointCoefficientProxy": 0.0,
        "retainedFullCosetHminus1LCharge": 0.0,
        "atomProxySumToRetainedCharge": 2.0,
        "secondRootTheta": 0.0,
        "secondRootNormalizedEnstrophy": 0.0,
    }
    fit_values = {
        "amplitude": [float(case["amplitude"]) for case in main_cases],
        "physicalSecondRootSlope": [
            float(case["roots"][1]["physicalSlope"]["absolute"])
            for case in main_cases
        ],
        "initialDataD": [
            float(case["initialData"]["D"]) for case in main_cases
        ],
        "completePrescribedAtomProxySum": [
            float(case["completePrescribedAtomProxySum"])
            for case in main_cases
        ],
        "secondRootAtomProxy": [
            float(case["roots"][1]["atomProxy"]) for case in main_cases
        ],
        "completePrescribedAtomProxySumOverDOneThird": [
            float(case["completePrescribedAtomProxySumOverDOneThird"])
            for case in main_cases
        ],
        "endpointCoefficientProxy": [
            float(case["endpointCoefficientProxy"]) for case in main_cases
        ],
        "retainedFullCosetHminus1LCharge": [
            float(case["retainedFullCosetHminus1LCharge"])
            for case in main_cases
        ],
        "atomProxySumToRetainedCharge": [
            float(case["atomProxySumToRetainedCharge"])
            for case in main_cases
        ],
        "secondRootTheta": [
            float(case["roots"][1]["Theta"]["absolute"])
            for case in main_cases
        ],
        "secondRootNormalizedEnstrophy": [
            float(case["roots"][1]["normalizedRootEnstrophy"])
            for case in main_cases
        ],
    }
    fits: dict[str, dict[str, float]] = {}
    for field, predicted_power in fit_specification.items():
        fits[field] = {
            **loglog_fit(q_values, fit_values[field]),
            "predictedPower": predicted_power,
        }
        fits[field]["absolutePowerError"] = abs(
            fits[field]["power"] - predicted_power
        )

    dimensionless_root_residuals = [
        float(case["rootSolve"]["maximumDimensionlessRootResidual"])
        for case in main_cases + truncation_cases
    ]
    physical_root_residuals = [
        float(case["rootSolve"]["maximumPhysicalRootResidual"])
        for case in main_cases + truncation_cases
    ]
    relative_truncation_differences: list[float] = []
    for case in truncation_cases:
        comparison = case["comparisonToR40"]
        relative_truncation_differences.extend(
            [
                float(comparison["initialDRelativeDifference"]),
                float(comparison["atomProxySumRelativeDifference"]),
                float(comparison["endpointCoefficientRelativeDifference"]),
                float(comparison["retainedChargeRelativeDifference"]),
            ]
        )
        for root in comparison["rootDifferences"]:
            relative_truncation_differences.extend(
                [
                    float(root["ThetaRelativeDifference"]),
                    float(root["normalizedEnstrophyRelativeDifference"]),
                    float(root["atomProxyRelativeDifference"]),
                ]
            )
    maximum_z_difference = max(
        float(case["comparisonToR40"]["maximumZDifference"])
        for case in truncation_cases
    )
    maximum_tail_ratio = max(
        float(case["chargeTailRelativeUpperBound"])
        for case in main_cases + truncation_cases
    )
    maximum_endpoint_identity_error = max(
        float(case["endpointIdentityRelativeError"])
        for case in main_cases + truncation_cases
    )
    minimum_theta = min(
        float(case["minimumTheta"]) for case in main_cases + truncation_cases
    )
    no_extra_root_scan_passed = all(
        bool(case["noExtraRootCorroboration"]["noExtraRealRootScanPassed"])
        for case in main_cases + truncation_cases
    )
    tail_proxy_passed = all(
        bool(
            case["noExtraRootCorroboration"]["integratingFactor"][
                "tailProxyPassed"
            ]
        )
        for case in main_cases + truncation_cases
    )
    minimum_outside_root_separation = min(
        float(
            case["noExtraRootCorroboration"][
                "minimumOutsideNeighborhoodRealSeparation"
            ]
        )
        for case in main_cases + truncation_cases
    )
    maximum_tail_proxy_relative_drift = max(
        float(
            case["noExtraRootCorroboration"]["integratingFactor"][
                "relativeDrift"
            ]
        )
        for case in main_cases + truncation_cases
    )

    checks = [
        make_check(
            "all nonlinear truncated roots close",
            max(dimensionless_root_residuals) <= ROOT_RESIDUAL_TOLERANCE,
            max(dimensionless_root_residuals),
            f"maximum dimensionless residual <= {ROOT_RESIDUAL_TOLERANCE}",
        ),
        make_check(
            "all restored physical root residuals close",
            max(physical_root_residuals) <= PHYSICAL_ROOT_RESIDUAL_TOLERANCE,
            max(physical_root_residuals),
            f"maximum physical residual <= {PHYSICAL_ROOT_RESIDUAL_TOLERANCE}",
        ),
        make_check(
            "all prescribed roots remain simple",
            minimum_theta >= SIMPLE_THETA_TOLERANCE,
            minimum_theta,
            f"minimum |Theta| >= {SIMPLE_THETA_TOLERANCE}",
        ),
        make_check(
            "all endpoint q-power fits close",
            all(
                float(fit["absolutePowerError"]) <= POWER_TOLERANCE
                for fit in fits.values()
            ),
            {
                field: float(fit["absolutePowerError"])
                for field, fit in fits.items()
            },
            f"every absolute fitted-power error <= {POWER_TOLERANCE}",
        ),
        make_check(
            "endpoint delta four-thirds identity closes",
            maximum_endpoint_identity_error <= ENDPOINT_IDENTITY_TOLERANCE,
            maximum_endpoint_identity_error,
            f"maximum relative identity error <= {ENDPOINT_IDENTITY_TOLERANCE}",
        ),
        make_check(
            "retained full-coset observables are truncation-stable",
            max(relative_truncation_differences)
            <= TRUNCATION_RELATIVE_TOLERANCE,
            max(relative_truncation_differences),
            f"maximum relative difference <= {TRUNCATION_RELATIVE_TOLERANCE}",
        ),
        make_check(
            "root parameters are truncation-stable",
            maximum_z_difference <= TRUNCATION_Z_TOLERANCE,
            maximum_z_difference,
            f"maximum absolute z difference <= {TRUNCATION_Z_TOLERANCE}",
        ),
        make_check(
            "charge tail is negligible",
            maximum_tail_ratio <= 1.0e-12,
            maximum_tail_ratio,
            "analytic tail upper bound / quadrature <= 1e-12",
        ),
        make_check(
            "dense scan finds only the two prescribed real roots",
            no_extra_root_scan_passed,
            {
                "allCasesPassed": no_extra_root_scan_passed,
                "minimumOutsideNeighborhoodRealSeparation": (
                    minimum_outside_root_separation
                ),
            },
            (
                "root neighborhoods are monotone with endpoint sign changes; "
                "all complementary segments have one strict real sign"
            ),
        ),
        make_check(
            "integrating-factor cutoff is separated from the tail limit proxy",
            tail_proxy_passed,
            {
                "allCasesPassed": tail_proxy_passed,
                "maximumRelativeDrift": maximum_tail_proxy_relative_drift,
            },
            (
                "cutoff and tail proxy have the same nonzero real sign and "
                f"relative drift <= {TAIL_PROXY_RELATIVE_DRIFT_TOLERANCE}"
            ),
        ),
    ]
    passed = all(bool(check["passed"]) for check in checks)
    return {
        "schemaVersion": 1,
        "audit": "R0.71X fixed-delta truncated Fourier-coset nonlinear corroboration",
        "status": "passed" if passed else "failed",
        "passed": passed,
        "boundary": (
            "Finite retained-coset numerical corroboration only. The annular "
            "multiplier, kappa_*, and m_*(k_*) are not locked, so the output "
            "uses atomProxy rather than J_*. It does not prove spectral-"
            "truncation convergence, the uniform continuum IFT, the analytic "
            "nonlinear enstrophy bounds, an endpoint theorem for every "
            "triangular or 3D solution, or Navier--Stokes regularity."
            " The O(1) numerical z4,z5 values reflect the large fixed inverse "
            "constant of the imaginary response block and are not evidence "
            "that delta=1/128 lies inside a validated continuum IFT radius."
        ),
        "determinism": (
            "No random numbers are used; delta, q values, truncations, "
            "tolerances, initial phases, continuation order, and quadrature "
            "grid are fixed."
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
            "backgroundMultiplier": BACKGROUND_MULTIPLIER,
            "backgroundAmplitudeLaw": "B_q = backgroundMultiplier * A_q * q",
            "delta": DELTA,
            "amplitudeLaw": "A_q = delta * q^2",
            "modeMultipliers": MODE_MULTIPLIERS.tolist(),
            "initialPositiveKzPhases": ["i", "i", "i", "1", "1"],
            "scaledRoots": SCALED_ROOTS.tolist(),
            "scaledWindowLeft": SCALED_WINDOW_LEFT,
            "physicalWindowLength": PHYSICAL_WINDOW_LENGTH,
            "atomNormalization": (
                "atomProxy = 2 |physical target slope|^2 / Y; actual "
                "multiplier factor is not locked"
            ),
            "mainQValues": list(MAIN_Q_VALUES),
            "mainTruncationRadius": MAIN_TRUNCATION,
            "continuationOrder": list(MAIN_Q_VALUES),
            "truncationAuditQ": TRUNCATION_AUDIT_Q,
            "truncationAuditRadii": list(TRUNCATION_AUDIT_RADII),
            "targetScanPoints": TARGET_SCAN_POINTS,
            "targetScanInterval": [SCALED_WINDOW_LEFT, CHARGE_CUTOFF_X],
            "rootNeighborhoodHalfWidth": ROOT_NEIGHBORHOOD_HALF_WIDTH,
            "targetTailEvaluationX": TARGET_TAIL_EVALUATION_X,
            "limitingRealBlockCoefficients": limiting.tolist(),
        },
        "limitingResponseBlockDiagnostics": response_block_diagnostics,
        "mainContinuation": main_cases,
        "truncationAudit": truncation_cases,
        "powerFits": fits,
        "checks": checks,
    }


def write_result(path: Path, result: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )
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
            "audit": "R0.71X fixed-delta truncated Fourier-coset nonlinear corroboration",
            "status": "error",
            "passed": False,
            "boundary": "Finite retained-coset numerical corroboration only.",
            "errorType": type(error).__name__,
            "error": str(error),
        }
        write_result(args.output, failure)
        raise
    write_result(args.output, result)
    print(json.dumps({"output": str(args.output), "status": result["status"]}))
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
