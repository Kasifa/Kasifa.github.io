#!/usr/bin/env python3
"""Independent numerical audit for the R0.71O face calculation.

This checker imports neither the symbolic producer nor earlier release code.
It verifies the finite-order inner profiles by adaptive quadrature, evaluates
the oscillatory soft paths without time stepping, and reconstructs the smooth
periodic NSE initial face with a standalone FFT implementation.

The floating-point checks support the exact report; they do not replace its
symbolic proofs or create an interval-certified Navier--Stokes theorem.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from time import perf_counter

import numpy as np
from scipy.integrate import quad


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def relative_error(value: float, target: float) -> float:
    return abs(value - target) / max(1.0, abs(target))


def inner_profiles() -> dict[str, object]:
    rows: list[dict[str, float | int]] = []
    maximum_error = 0.0
    for order in range(1, 9):
        def derivative(s: float) -> float:
            power = s ** (2 * order)
            return 2 * order * s ** (2 * order - 1) / (1 + power) ** 2

        def radial(s: float) -> float:
            power = s ** (2 * order)
            return power / (1 + power) ** 2

        derivative_mass, derivative_error = quad(
            derivative, 0.0, np.inf, epsabs=2e-13, epsrel=2e-13, limit=500
        )
        radial_mass, radial_error = quad(
            radial, 0.0, np.inf, epsabs=2e-13, epsrel=2e-13, limit=500
        )
        error = abs(derivative_mass - 1.0)
        maximum_error = max(maximum_error, error)
        require(error < 2e-11, f"order {order} derivative mass")
        require(radial_mass > 0.0, f"order {order} radial mass")
        rows.append({
            "order": order,
            "derivativeMass": derivative_mass,
            "derivativeQuadratureError": derivative_error,
            "radialProfileMass": radial_mass,
            "radialQuadratureError": radial_error,
        })
    return {
        "passed": True,
        "maximumDerivativeMassError": maximum_error,
        "rows": rows,
    }


def raw_split_cancellation() -> dict[str, object]:
    """Numerically verify the cancelling logarithms on one active half-face."""

    gamma = 0.73
    endpoint = 1.0
    rows: list[dict[str, float]] = []
    maximum_relative_error = 0.0
    for epsilon in (1e-1, 1e-2, 1e-4, 1e-6):
        def source(x: float) -> float:
            return gamma**2 / (x + epsilon)

        def radial(x: float) -> float:
            return -gamma**2 * x / (x + epsilon) ** 2

        source_mass, source_error = quad(
            source, 0.0, endpoint, epsabs=2e-12, epsrel=2e-12, limit=500
        )
        radial_mass, radial_error = quad(
            radial, 0.0, endpoint, epsabs=2e-12, epsrel=2e-12, limit=500
        )
        joint_mass = source_mass + radial_mass
        expected_joint = gamma**2 * endpoint / (endpoint + epsilon)
        error = relative_error(joint_mass, expected_joint)
        maximum_relative_error = max(maximum_relative_error, error)
        require(error < 2e-10, f"epsilon {epsilon} raw cancellation")
        rows.append({
            "epsilon": epsilon,
            "sourceMass": source_mass,
            "sourceQuadratureError": source_error,
            "radialMass": radial_mass,
            "radialQuadratureError": radial_error,
            "jointMass": joint_mass,
            "expectedJointMass": expected_joint,
            "jointRelativeError": error,
        })

    require(rows[-1]["sourceMass"] > rows[0]["sourceMass"] + 5.0,
            "raw source logarithmic growth")
    require(-rows[-1]["radialMass"] > -rows[0]["radialMass"] + 5.0,
            "raw radial logarithmic growth")
    return {
        "passed": True,
        "gamma": gamma,
        "endpoint": endpoint,
        "maximumJointRelativeError": maximum_relative_error,
        "rows": rows,
    }


def oscillatory_paths() -> dict[str, object]:
    rows: list[dict[str, float | int]] = []
    maximum_variation_error = 0.0
    lam = 0.37
    for frequency in (1, 2, 4, 8, 16, 32, 64):
        epsilon = frequency ** -4

        def c(t: float) -> float:
            return np.sin(frequency * t) / frequency

        def c_t(t: float) -> float:
            return np.cos(frequency * t)

        def a_t(t: float) -> float:
            value = c(t)
            if value <= 0.0:
                return 0.0
            return (
                2.0 * epsilon * value * c_t(t)
                / (value * value + epsilon) ** 2
            )

        def extra_radial(t: float) -> float:
            value = c(t)
            if value <= 0.0:
                return 0.0
            denominator = value * value + epsilon
            return 2.0 * lam * epsilon * value * value / denominator**2

        rising_mass, rising_error = quad(
            a_t,
            0.0,
            np.pi / (2 * frequency),
            epsabs=2e-12,
            epsrel=2e-12,
            limit=500,
        )
        positive_variation = frequency * rising_mass
        expected = frequency / (1.0 + epsilon * frequency**2)
        variation_error = relative_error(positive_variation, expected)
        maximum_variation_error = max(maximum_variation_error, variation_error)
        require(variation_error < 2e-10,
                f"frequency {frequency} positive variation")

        radial_half, radial_error = quad(
            extra_radial,
            0.0,
            np.pi / frequency,
            epsabs=2e-12,
            epsrel=2e-12,
            limit=500,
        )
        radial_total = frequency * radial_half
        delta = epsilon * frequency**2
        radial_expected = (
            lam * np.pi * np.sqrt(delta) / (1.0 + delta) ** 1.5
        )
        radial_relative_error = relative_error(radial_total, radial_expected)
        require(radial_relative_error < 2e-10,
                f"frequency {frequency} extra radial mass")
        denominator_mass = np.pi / frequency**2
        c_t_square_mass = np.pi
        m_square_mass = np.pi * (1.0 + lam**2 / frequency**2)
        field_mass = 2.0 * np.pi
        rows.append({
            "N": frequency,
            "epsilon": epsilon,
            "positiveVariation": positive_variation,
            "expectedPositiveVariation": expected,
            "variationRelativeError": variation_error,
            "risingQuadratureError": rising_error,
            "extraRadialMass": radial_total,
            "expectedExtraRadialMass": radial_expected,
            "extraRadialRelativeError": radial_relative_error,
            "extraRadialQuadratureError": radial_error,
            "denominatorMass": denominator_mass,
            "C_tSquareMass": c_t_square_mass,
            "M_SquareMass": m_square_mass,
            "FTimeMass": field_mass,
        })

    require(rows[-1]["positiveVariation"] > 60.0,
            "large face count at bounded square budgets")
    require(rows[-1]["denominatorMass"] < 1e-3,
            "small denominator mass at large face count")
    return {
        "passed": True,
        "lambda": lam,
        "maximumVariationRelativeError": maximum_variation_error,
        "rows": rows,
    }


def spectral_curl(coefficients: np.ndarray, waves: np.ndarray) -> np.ndarray:
    return 1j * np.cross(waves, coefficients)


def leray(coefficients: np.ndarray, waves: np.ndarray) -> np.ndarray:
    squared = np.sum(waves * waves, axis=-1)
    projected = coefficients.copy()
    nonzero = squared > 0
    radial = np.sum(waves * coefficients, axis=-1)
    projected[nonzero] -= (
        waves[nonzero]
        * (radial[nonzero] / squared[nonzero])[:, None]
    )
    projected[~nonzero] = 0.0
    return projected


def coefficient_norm_squared(coefficients: np.ndarray) -> float:
    return float(np.sum(np.abs(coefficients) ** 2).real)


def nse_initial_face(order: int = 32) -> dict[str, object]:
    coordinates = 2.0 * np.pi * np.arange(order) / order
    x1, x2, _x3 = np.meshgrid(
        coordinates, coordinates, coordinates, indexing="ij"
    )
    velocity = np.zeros((order, order, order, 3), dtype=np.float64)
    velocity[..., 1] = np.cos(x1)
    velocity[..., 2] = np.cos(x2)

    normalization = order**3
    velocity_hat = np.stack([
        np.fft.fftn(velocity[..., component]) / normalization
        for component in range(3)
    ], axis=-1)
    integers = np.fft.fftfreq(order, d=1.0 / order)
    k1, k2, k3 = np.meshgrid(integers, integers, integers, indexing="ij")
    waves = np.stack([k1, k2, k3], axis=-1)
    squared = np.sum(waves * waves, axis=-1)

    vorticity_hat = spectral_curl(velocity_hat, waves)
    vorticity = np.stack([
        np.fft.ifftn(vorticity_hat[..., component] * normalization).real
        for component in range(3)
    ], axis=-1)
    lamb_unprojected = np.cross(velocity, vorticity)
    lamb_unprojected_hat = np.stack([
        np.fft.fftn(lamb_unprojected[..., component]) / normalization
        for component in range(3)
    ], axis=-1)
    lamb_hat = leray(lamb_unprojected_hat, waves)

    shell = squared == 2
    filtered_lamb_hat = np.where(shell[..., None], lamb_hat, 0.0)
    filtered_vorticity_hat = np.where(shell[..., None], vorticity_hat, 0.0)
    G_hat = spectral_curl(filtered_lamb_hat, waves)
    C_first_hat = spectral_curl(G_hat, waves)

    divergence_velocity = np.max(np.abs(
        np.sum(waves * velocity_hat, axis=-1)
    ))
    divergence_lamb = np.max(np.abs(
        np.sum(waves * filtered_lamb_hat, axis=-1)
    ))
    initial_filtered_vorticity = coefficient_norm_squared(
        filtered_vorticity_hat
    )
    Y0 = coefficient_norm_squared(vorticity_hat)
    F_squared = coefficient_norm_squared(filtered_lamb_hat)
    G_squared = coefficient_norm_squared(G_hat)
    C_first_squared = coefficient_norm_squared(C_first_hat)
    B_first = float(np.vdot(filtered_lamb_hat, C_first_hat).real)
    face_trace = B_first**2 / (Y0 * C_first_squared)

    residuals = {
        "velocityDivergence": float(divergence_velocity),
        "filteredLambDivergence": float(divergence_lamb),
        "filteredVorticityAtZero": initial_filtered_vorticity,
        "Y0": relative_error(Y0, 1.0),
        "F2": relative_error(F_squared, 0.25),
        "G2": relative_error(G_squared, 0.5),
        "CFirst2": relative_error(C_first_squared, 1.0),
        "BFirst": relative_error(B_first, 0.5),
        "faceTrace": relative_error(face_trace, 0.25),
    }
    maximum_residual = max(residuals.values())
    require(maximum_residual < 2e-12, "standalone FFT initial face")
    target_mode_count = int(np.count_nonzero(
        np.linalg.norm(filtered_lamb_hat, axis=-1) > 1e-13
    ))
    require(target_mode_count == 4, "four target interaction modes")

    return {
        "passed": True,
        "gridOrder": order,
        "targetModeCount": target_mode_count,
        "Y0": Y0,
        "F2": F_squared,
        "G2": G_squared,
        "CFirst2": C_first_squared,
        "BFirst": B_first,
        "rightEntryTrace": face_trace,
        "residuals": residuals,
        "maximumResidual": maximum_residual,
    }


def run() -> dict[str, object]:
    started = perf_counter()
    checks = {
        "innerProfiles": inner_profiles(),
        "rawSplitCancellation": raw_split_cancellation(),
        "oscillatoryPaths": oscillatory_paths(),
        "nseInitialFace": nse_initial_face(),
    }
    return {
        "release": "R0.71O",
        "status": "passed",
        "implementation": "standalone scipy quadrature and numpy FFT",
        "checks": checks,
        "wallSeconds": perf_counter() - started,
        "claimBoundary": (
            "Floating-point corroboration of exact face profiles, a smooth "
            "abstract path, and one NSE initial jet. No time integration, "
            "interval arithmetic, internal NSE face-count theorem, or "
            "Navier--Stokes regularity conclusion."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    rendered = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
