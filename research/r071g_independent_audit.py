#!/usr/bin/env python3
"""Independent FFT and Fourier-chain audit for R0.71G.

This checker does not import the exact producer.  It reconstructs the true
Navier--Stokes time derivative of the full trigonometric datum by an FFT
Leray projection, then integrates the exact 2D3C sideband chain with a
separate adaptive ODE method at two truncation radii.

The chain calculations are finite numerical checks, not interval proofs.
The arbitrary-M sign-residence statement is proved by an explicit analytic
Duhamel bound in the report and exact certificate.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def wave_numbers(size: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    modes = np.fft.fftfreq(size, d=1.0 / size)
    return np.meshgrid(modes, modes, modes, indexing="ij")


def fft_vector(field: np.ndarray) -> np.ndarray:
    return np.stack([np.fft.fftn(field[index]) for index in range(3)])


def ifft_vector(coefficients: np.ndarray) -> np.ndarray:
    return np.stack([np.fft.ifftn(coefficients[index]).real for index in range(3)])


def curl_hat(coefficients: np.ndarray, waves) -> np.ndarray:
    kx, ky, kz = waves
    output = np.empty_like(coefficients)
    output[0] = 1j * (ky * coefficients[2] - kz * coefficients[1])
    output[1] = 1j * (kz * coefficients[0] - kx * coefficients[2])
    output[2] = 1j * (kx * coefficients[1] - ky * coefficients[0])
    return output


def leray_project(coefficients: np.ndarray, waves) -> np.ndarray:
    kx, ky, kz = waves
    k2 = kx**2 + ky**2 + kz**2
    dot = kx * coefficients[0] + ky * coefficients[1] + kz * coefficients[2]
    safe = np.where(k2 == 0, 1.0, k2)
    output = np.empty_like(coefficients)
    output[0] = coefficients[0] - kx * dot / safe
    output[1] = coefficients[1] - ky * dot / safe
    output[2] = coefficients[2] - kz * dot / safe
    output[:, k2 == 0] = 0.0
    return output


def cross(first: np.ndarray, second: np.ndarray) -> np.ndarray:
    return np.moveaxis(
        np.cross(np.moveaxis(first, 0, -1), np.moveaxis(second, 0, -1)),
        -1,
        0,
    )


def mean_pair(first: np.ndarray, second: np.ndarray) -> float:
    return float(np.mean(np.sum(first * second, axis=0)))


def initial_fft_case(size: int, scale: int, amplitude: float, viscosity: float):
    grid = 2.0 * np.pi * np.arange(size) / size
    x, y, _z = np.meshgrid(grid, grid, grid, indexing="ij")
    waves = wave_numbers(size)
    kx, ky, kz = waves
    k2 = kx**2 + ky**2 + kz**2

    velocity = np.zeros((3, size, size, size), dtype=float)
    velocity[1] = -2.0 * amplitude * scale * np.cos(scale * x)
    velocity[2] = amplitude * scale * (
        -2.0 * np.sin(scale * x + scale * y) - 2.0 * np.cos(scale * y)
    )
    velocity_hat = fft_vector(velocity)
    omega_hat = curl_hat(velocity_hat, waves)
    omega = ifft_vector(omega_hat)
    lamb_hat = leray_project(fft_vector(cross(velocity, omega)), waves)
    lamb = ifft_vector(lamb_hat)
    velocity_t_hat = lamb_hat - viscosity * k2 * velocity_hat
    velocity_t = ifft_vector(velocity_t_hat)
    omega_t_hat = curl_hat(velocity_t_hat, waves)
    omega_t = ifft_vector(omega_t_hat)
    lamb_t_hat = leray_project(
        fft_vector(cross(velocity_t, omega) + cross(velocity, omega_t)), waves
    )

    mask = np.isclose(k2, float(scale**2), atol=0.0, rtol=0.0)
    w_hat = omega_hat * mask
    f_hat = lamb_hat * mask
    wt_hat = omega_t_hat * mask
    ft_hat = lamb_t_hat * mask
    c_hat = curl_hat(w_hat, waves)
    ct_hat = curl_hat(wt_hat, waves)
    w = ifft_vector(w_hat)
    f = ifft_vector(f_hat)
    ft = ifft_vector(ft_hat)
    c = ifft_vector(c_hat)
    ct = ifft_vector(ct_hat)

    b = mean_pair(f, c)
    d = mean_pair(c, c)
    q = b**2 / d
    y_norm = mean_pair(omega, omega)
    b_t = mean_pair(ft, c) + mean_pair(f, ct)
    d_t = 2.0 * mean_pair(c, ct)
    q_t = 2.0 * b * b_t / d - b**2 * d_t / d**2
    y_t = 2.0 * mean_pair(omega, omega_t)
    a_norm = q / y_norm
    a_t = q_t / y_norm - q * y_t / y_norm**2

    expected = {
        "B": 2.0 * amplitude**3 * scale**6,
        "d": 4.0 * amplitude**2 * scale**6,
        "q": amplitude**4 * scale**6,
        "Y": 8.0 * amplitude**2 * scale**4,
        "B_t": -2.0 * amplitude**3 * (amplitude + 4.0 * viscosity) * scale**8,
        "d_t": 4.0 * amplitude**2 * (amplitude - 2.0 * viscosity) * scale**8,
        "q_t": -3.0 * amplitude**4 * (amplitude + 2.0 * viscosity) * scale**8,
        "Y_t": -4.0 * amplitude**2 * (amplitude + 6.0 * viscosity) * scale**6,
        "qOverY": amplitude**2 * scale**2 / 8.0,
        "qOverY_t": -amplitude**2 * (5.0 * amplitude + 6.0 * viscosity) * scale**4 / 16.0,
    }
    observed = {
        "B": b,
        "d": d,
        "q": q,
        "Y": y_norm,
        "B_t": b_t,
        "d_t": d_t,
        "q_t": q_t,
        "Y_t": y_t,
        "qOverY": a_norm,
        "qOverY_t": a_t,
    }
    relative_errors = {
        key: abs(observed[key] - value) / max(abs(value), 1.0e-300)
        for key, value in expected.items()
    }
    divergence_error = float(
        np.max(np.abs(kx * velocity_hat[0] + ky * velocity_hat[1] + kz * velocity_hat[2]))
        / size**3
    )
    maximum_error = max(relative_errors.values())
    require(divergence_error < 2.0e-12, "FFT divergence")
    require(maximum_error < 2.0e-10, "FFT initial derivative formulas")

    return {
        "grid": size,
        "K": scale,
        "a": amplitude,
        "nu": viscosity,
        "mu": amplitude / viscosity,
        "observed": observed,
        "expected": expected,
        "relativeErrors": relative_errors,
        "maximumRelativeError": maximum_error,
        "divergenceError": divergence_error,
    }


def chain_solution(mu: float, radius: int):
    modes = np.arange(-radius, radius + 1, dtype=float)
    initial = np.zeros(2 * radius + 1, dtype=complex)
    initial[radius] = -1.0
    initial[radius + 1] = 1.0j

    def rhs(theta: float, values: np.ndarray) -> np.ndarray:
        left = np.concatenate(([0.0j], values[:-1]))
        right = np.concatenate((values[1:], [0.0j]))
        return -(modes**2 + 1.0) * values + 1.0j * mu * np.exp(-theta) * (left + right)

    def h_value(theta: float, values: np.ndarray) -> float:
        ell = 1.0j * np.exp(-theta) * (values[radius - 1] + values[radius + 1])
        return float(np.real(np.conjugate(values[radius]) * ell))

    def q_relative(theta: float, values: np.ndarray) -> float:
        h = max(h_value(theta, values), 0.0)
        g = abs(values[radius]) ** 2 + np.exp(-2.0 * theta)
        return float(2.0 * h**2 / g)

    events = []

    def sign_event(theta, values):
        return h_value(theta, values)

    sign_event.direction = -1
    sign_event.terminal = False
    events.append(sign_event)
    levels = (0.5, 0.1, 0.01)
    for level in levels:
        def level_event(theta, values, level=level):
            return q_relative(theta, values) - level

        level_event.direction = -1
        level_event.terminal = False
        events.append(level_event)

    final_time = max(2.0, min(12.0, 0.62 / mu + 1.0))
    solution = solve_ivp(
        rhs,
        (0.0, final_time),
        initial,
        method="DOP853",
        rtol=2.0e-12,
        atol=2.0e-18,
        max_step=0.0025,
        events=events,
    )
    require(solution.success, "adaptive chain integration")
    event_times = [float(group[0]) if len(group) else None for group in solution.t_events]
    require(all(value is not None for value in event_times), "all chain events found")

    energy_identity_residual = 0.0
    boundary_mass = 0.0
    for theta, values in zip(solution.t[:: max(1, len(solution.t) // 200)], solution.y.T[:: max(1, len(solution.t) // 200)]):
        derivative = rhs(float(theta), values)
        observed = 2.0 * float(np.real(np.vdot(values, derivative)))
        expected = -2.0 * float(np.sum((modes**2 + 1.0) * np.abs(values) ** 2))
        energy_identity_residual = max(energy_identity_residual, abs(observed - expected))
        boundary_mass = max(
            boundary_mass,
            float(np.sum(np.abs(values[[0, 1, -2, -1]]) ** 2)),
        )
    require(energy_identity_residual < 2.0e-13, "chain energy identity")

    return {
        "mu": mu,
        "radius": radius,
        "finalTime": final_time,
        "steps": len(solution.t),
        "functionEvaluations": solution.nfev,
        "firstSignExit": event_times[0],
        "relativeQExit": {
            str(level): event_times[index + 1] for index, level in enumerate(levels)
        },
        "maximumEnergyIdentityResidual": energy_identity_residual,
        "maximumOuterTwoModeMass": boundary_mass,
    }


def chain_case(mu: float):
    smaller = chain_solution(mu, 12)
    larger = chain_solution(mu, 18)
    differences = {
        "firstSignExit": abs(smaller["firstSignExit"] - larger["firstSignExit"]),
        "relativeQExit0.5": abs(
            smaller["relativeQExit"]["0.5"] - larger["relativeQExit"]["0.5"]
        ),
        "relativeQExit0.1": abs(
            smaller["relativeQExit"]["0.1"] - larger["relativeQExit"]["0.1"]
        ),
        "relativeQExit0.01": abs(
            smaller["relativeQExit"]["0.01"] - larger["relativeQExit"]["0.01"]
        ),
    }
    maximum_difference = max(differences.values())
    require(maximum_difference < 2.0e-8, "chain truncation agreement")
    return {
        "mu": mu,
        "radius12": smaller,
        "radius18": larger,
        "eventDifferences": differences,
        "maximumEventDifference": maximum_difference,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--grid", type=int, default=48)
    args = parser.parse_args()
    require(args.grid >= 40, "grid resolves all selected nonlinear modes")

    fft_cases = [
        initial_fft_case(args.grid, 1, 0.8, 0.3),
        initial_fft_case(args.grid, 2, 0.35, 0.3),
        initial_fft_case(args.grid, 4, 0.15, 0.3),
    ]
    chain_cases = [chain_case(mu) for mu in (1.0, 0.5, 0.2, 0.1, 0.05)]
    sign_exits = [case["radius18"]["firstSignExit"] for case in chain_cases]
    require(all(
        sign_exits[index] < sign_exits[index + 1]
        for index in range(len(sign_exits) - 1)
    ), "sign interval grows as mu decreases on checked cases")

    payload = {
        "version": "R0.71G-independent",
        "status": "pass",
        "method": (
            "independent pseudospectral Leray differentiation plus adaptive complex DOP853 integration of the exact 2D3C sideband chain"
        ),
        "fftCases": fft_cases,
        "chainCases": chain_cases,
        "checks": {
            "fullVelocityUsedBeforeProjection": True,
            "trueNSEInitialDerivativeReconstructed": True,
            "allTenInitialFormulasVerified": True,
            "infiniteSidebandChainTruncatedIndependently": True,
            "twoTruncationRadiiAgree": True,
            "chainEnergyIdentityVerified": True,
            "signIntervalsGrowOnFiniteCheckedSequence": True,
            "relativeThresholdEventsRecorded": True,
            "noExactProducerImport": True,
        },
        "claimBoundary": (
            "The FFT and ODE results are finite floating-point checks. The arbitrary-M sign-only no-go follows from the report's analytic Duhamel estimate, not from these samples. No general K^-2 occupation theorem is claimed."
        ),
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
