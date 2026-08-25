#!/usr/bin/env python3
"""Independent spectral/real-space audit for R0.71F.

This checker does not import the exact producer.  It starts from the full
trigonometric six-mode velocity, differentiates and applies the Leray
projection with an independent FFT implementation, extracts the radius-K
block, inserts a nonconstant spatial cutoff before curl, and verifies the
finite-height trace relation by numerical quadrature.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.integrate import quad


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def wave_numbers(size: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    modes = np.fft.fftfreq(size, d=1.0 / size)
    return np.meshgrid(modes, modes, modes, indexing="ij")


def fft_vector(field: np.ndarray) -> np.ndarray:
    return np.stack([np.fft.fftn(field[index]) for index in range(3)])


def ifft_vector(coefficients: np.ndarray) -> np.ndarray:
    return np.stack(
        [np.fft.ifftn(coefficients[index]).real for index in range(3)]
    )


def spectral_curl(field: np.ndarray, waves) -> np.ndarray:
    kx, ky, kz = waves
    hat = fft_vector(field)
    output = np.empty_like(hat)
    output[0] = 1j * (ky * hat[2] - kz * hat[1])
    output[1] = 1j * (kz * hat[0] - kx * hat[2])
    output[2] = 1j * (kx * hat[1] - ky * hat[0])
    return ifft_vector(output)


def leray_project(coefficients: np.ndarray, waves) -> np.ndarray:
    kx, ky, kz = waves
    k2 = kx**2 + ky**2 + kz**2
    dot = kx * coefficients[0] + ky * coefficients[1] + kz * coefficients[2]
    safe = np.where(k2 == 0, 1.0, k2)
    projected = np.empty_like(coefficients)
    projected[0] = coefficients[0] - kx * dot / safe
    projected[1] = coefficients[1] - ky * dot / safe
    projected[2] = coefficients[2] - kz * dot / safe
    projected[:, k2 == 0] = 0.0
    return projected


def normalized_mean(value: np.ndarray) -> float:
    return float(np.mean(value))


def run_case(size: int, scale: int, amplitude: float) -> dict[str, object]:
    grid = 2.0 * np.pi * np.arange(size) / size
    x, y, z = np.meshgrid(grid, grid, grid, indexing="ij")
    waves = wave_numbers(size)
    kx, ky, kz = waves
    k2 = kx**2 + ky**2 + kz**2

    velocity = np.zeros((3, size, size, size), dtype=float)
    velocity[1] = -2.0 * amplitude * scale * np.cos(scale * x)
    velocity[2] = amplitude * scale * (
        -2.0 * np.sin(scale * x + scale * y)
        - 2.0 * np.cos(scale * y)
    )
    omega = spectral_curl(velocity, waves)

    raw_lamb = np.cross(
        np.moveaxis(velocity, 0, -1),
        np.moveaxis(omega, 0, -1),
    )
    raw_lamb = np.moveaxis(raw_lamb, -1, 0)
    projected_lamb_hat = leray_project(fft_vector(raw_lamb), waves)
    omega_hat = fft_vector(omega)
    low_mask = np.isclose(k2, float(scale**2), atol=0.0, rtol=0.0)
    low_omega_hat = omega_hat * low_mask
    low_lamb_hat = projected_lamb_hat * low_mask
    low_omega = ifft_vector(low_omega_hat)
    low_lamb = ifft_vector(low_lamb_hat)

    expected_omega = np.zeros_like(low_omega)
    expected_omega[0] = 2.0 * amplitude * scale**2 * np.sin(scale * y)
    expected_omega[2] = 2.0 * amplitude * scale**2 * np.sin(scale * x)
    expected_lamb = np.zeros_like(low_lamb)
    expected_lamb[2] = -2.0 * amplitude**2 * scale**3 * np.cos(scale * y)

    omega_error = float(np.max(np.abs(low_omega - expected_omega)))
    lamb_error = float(np.max(np.abs(low_lamb - expected_lamb)))
    divergence_hat = kx * fft_vector(velocity)[0] + ky * fft_vector(velocity)[1] + kz * fft_vector(velocity)[2]
    divergence_error = float(np.max(np.abs(divergence_hat)) / size**3)

    # A fixed, nonconstant, strictly positive smooth torus cutoff.  Its
    # Fourier support is disjoint from the Nyquist boundary for all cases.
    phi = (
        1.0
        + 0.31 * np.cos(x - 0.37)
        + 0.19 * np.cos(y + 0.41)
        + 0.11 * np.sin(z - 0.23)
    )
    require(float(np.min(phi)) > 0.0, "positive independent cutoff")

    curl_phi_omega = spectral_curl(phi[None, ...] * low_omega, waves)
    bottom_work = normalized_mean(np.sum(low_lamb * curl_phi_omega, axis=0))
    bottom_denominator = normalized_mean(np.sum(curl_phi_omega**2, axis=0))
    bottom_quotient = bottom_work**2 / bottom_denominator

    expected_work = normalized_mean(
        4.0
        * amplitude**3
        * scale**6
        * phi
        * np.sin(scale * y) ** 2
    )
    work_identity_error = abs(bottom_work - expected_work)
    require(bottom_work > 0.0, "positive localized work")

    def quotient_at(height: float) -> float:
        factor = np.exp(-(scale**2) * height)
        heat_lamb = factor * low_lamb
        heat_curl = factor * curl_phi_omega
        work = normalized_mean(np.sum(heat_lamb * heat_curl, axis=0))
        denominator = normalized_mean(np.sum(heat_curl**2, axis=0))
        return work**2 / denominator

    sample_thetas = [0.0, 0.125, 0.5, 1.0, 2.0]
    sample_rows = []
    max_decay_error = 0.0
    for theta in sample_thetas:
        height = theta / scale**2
        observed = quotient_at(height)
        expected = bottom_quotient * np.exp(-2.0 * theta)
        relative_error = abs(observed - expected) / max(abs(expected), 1.0e-300)
        max_decay_error = max(max_decay_error, relative_error)
        sample_rows.append(
            {
                "theta": theta,
                "height": height,
                "observedQ": observed,
                "expectedQ": expected,
                "relativeError": relative_error,
            }
        )

    theta_window = 1.7
    height_window = theta_window / scale**2
    numerical_bulk, quadrature_error = quad(
        quotient_at,
        0.0,
        height_window,
        epsabs=1.0e-12,
        epsrel=1.0e-12,
        limit=100,
    )
    expected_bulk = (
        bottom_quotient
        * (1.0 - np.exp(-2.0 * theta_window))
        / (2.0 * scale**2)
    )
    finite_trace_residual = (
        bottom_quotient
        - 2.0
        * scale**2
        * numerical_bulk
        / (1.0 - np.exp(-2.0 * theta_window))
    )

    tolerances = {
        "field": 2.0e-11,
        "work": 2.0e-10,
        "decayRelative": 2.0e-12,
        "finiteTraceRelative": 2.0e-12,
    }
    require(omega_error < tolerances["field"], "independent omega extraction")
    require(lamb_error < tolerances["field"], "independent Lamb extraction")
    require(divergence_error < tolerances["field"], "independent divergence")
    require(work_identity_error < tolerances["work"], "independent cutoff work")
    require(max_decay_error < tolerances["decayRelative"], "independent heat decay")
    require(
        abs(finite_trace_residual) / bottom_quotient
        < tolerances["finiteTraceRelative"],
        "independent finite trace",
    )

    return {
        "grid": size,
        "K": scale,
        "a": amplitude,
        "divergenceError": divergence_error,
        "lowOmegaMaxError": omega_error,
        "lowProjectedLambMaxError": lamb_error,
        "cutoffMinimum": float(np.min(phi)),
        "bottomWork": bottom_work,
        "expectedBottomWork": expected_work,
        "workIdentityError": work_identity_error,
        "bottomDenominator": bottom_denominator,
        "bottomQuotient": bottom_quotient,
        "sampleRows": sample_rows,
        "maxHeatDecayRelativeError": max_decay_error,
        "finiteWindow": {
            "theta": theta_window,
            "height": height_window,
            "numericalBulk": numerical_bulk,
            "expectedBulk": expected_bulk,
            "quadratureErrorEstimate": quadrature_error,
            "traceResidual": finite_trace_residual,
        },
        "tolerances": tolerances,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--grid", type=int, default=48)
    args = parser.parse_args()

    require(args.grid >= 40, "grid resolves K=8 nonlinear modes")
    cases = [run_case(args.grid, scale, 1.0 / scale) for scale in (1, 2, 4, 8)]
    payload = {
        "version": "R0.71F-independent",
        "status": "pass",
        "method": (
            "independent FFT differentiation, Leray projection, low-sphere "
            "extraction, real-space cutoff-curl pairing, and adaptive quadrature"
        ),
        "cases": cases,
        "checks": {
            "cutoffIsNonconstantAndPositive": True,
            "cutoffCurlRetained": True,
            "finiteHeightTraceVerifiedNumerically": True,
            "fullVelocityUsedBeforeIndependentProjection": True,
            "multipleDyadicFrequenciesChecked": True,
            "noProducerImport": True,
        },
        "claimBoundary": (
            "This is a finite-grid independent check of the localized "
            "cutoff-curl and finite-height trace identities. The moving-cylinder "
            "ledger and arbitrary-cutoff quantifiers are proved analytically in "
            "the report and exact producer."
        ),
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
