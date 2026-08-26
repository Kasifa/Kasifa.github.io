#!/usr/bin/env python3
"""Independent numerical audit for R0.71T.

This checker imports neither the symbolic producer nor its output.  It uses a
standalone FFT reconstruction, adaptive quadrature, direct polynomial
integration, and floating-point scale ratios.  The positive-time NSE
internalization itself is an analytic flow-map theorem, not a numerical
claim.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from time import perf_counter

import numpy as np
from scipy.integrate import quad


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def relative_error(value: float, target: float) -> float:
    return abs(value - target) / max(1.0, abs(target))


def spectral_curl(coefficients: np.ndarray, waves: np.ndarray) -> np.ndarray:
    return 1j * np.cross(waves, coefficients)


def leray(coefficients: np.ndarray, waves: np.ndarray) -> np.ndarray:
    squared = np.sum(waves * waves, axis=-1)
    radial = np.sum(waves * coefficients, axis=-1)
    result = coefficients.copy()
    nonzero = squared > 0
    result[nonzero] -= (
        waves[nonzero]
        * (radial[nonzero] / squared[nonzero])[:, None]
    )
    result[~nonzero] = 0.0
    return result


def coefficient_norm_squared(coefficients: np.ndarray) -> float:
    return float(np.sum(np.abs(coefficients) ** 2).real)


def fourier_seed(order: int = 32) -> dict[str, object]:
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
    lamb_raw = np.cross(velocity, vorticity)
    lamb_raw_hat = np.stack([
        np.fft.fftn(lamb_raw[..., component]) / normalization
        for component in range(3)
    ], axis=-1)
    lamb_hat = leray(lamb_raw_hat, waves)
    shell = squared == 2
    filtered_lamb = np.where(shell[..., None], lamb_hat, 0.0)
    filtered_vorticity = np.where(shell[..., None], vorticity_hat, 0.0)
    curl_f = spectral_curl(filtered_lamb, waves)
    c_first = spectral_curl(curl_f, waves)

    y0 = coefficient_norm_squared(vorticity_hat)
    f2 = coefficient_norm_squared(filtered_lamb)
    curl_f2 = coefficient_norm_squared(curl_f)
    c2 = coefficient_norm_squared(c_first)
    pairing = float(np.vdot(filtered_lamb, c_first).real)
    face = pairing**2 / (y0 * c2)
    residuals = {
        "velocityDivergence": float(np.max(np.abs(
            np.sum(waves * velocity_hat, axis=-1)
        ))),
        "lambDivergence": float(np.max(np.abs(
            np.sum(waves * filtered_lamb, axis=-1)
        ))),
        "initialTargetVorticity": coefficient_norm_squared(filtered_vorticity),
        "Y0": relative_error(y0, 1.0),
        "F2": relative_error(f2, 0.25),
        "curlF2": relative_error(curl_f2, 0.5),
        "CFirst2": relative_error(c2, 1.0),
        "pairing": relative_error(pairing, 0.5),
        "face": relative_error(face, 0.25),
    }
    maximum = max(residuals.values())
    require(maximum < 3e-12, "independent Fourier seed")
    count = int(np.count_nonzero(
        np.linalg.norm(filtered_lamb, axis=-1) > 1e-13
    ))
    require(count == 4, "four target Fourier modes")
    return {
        "passed": True,
        "gridOrder": order,
        "targetModeCount": count,
        "Y0": y0,
        "F2": f2,
        "curlF2": curl_f2,
        "CFirst2": c2,
        "pairing": pairing,
        "entryFace": face,
        "maximumResidual": maximum,
        "residuals": residuals,
    }


def outgoing_coarea() -> dict[str, object]:
    rows = []
    maximum = 0.0
    for order in range(1, 9):
        for delta in (0.2, 0.03, 0.004):
            endpoint = delta ** (1.0 / order)

            def integrand(time: float) -> float:
                radius = time**order
                mollifier = 6.0 * (radius / delta) * (1.0 - radius / delta) / delta
                radial_speed = order * time ** (order - 1)
                return mollifier * radial_speed

            value, error = quad(
                integrand,
                0.0,
                endpoint,
                epsabs=2e-12,
                epsrel=2e-12,
                limit=500,
            )
            residual = abs(value - 1.0)
            maximum = max(maximum, residual)
            require(residual < 3e-10, f"coarea order {order} delta {delta}")
            rows.append({
                "order": order,
                "delta": delta,
                "mass": value,
                "quadratureError": error,
                "residual": residual,
            })
    return {
        "passed": True,
        "maximumResidual": maximum,
        "rows": rows,
    }


def trace_variation() -> dict[str, object]:
    coefficients = np.array([0.7, -0.4, 0.13, 0.08, -0.025, 0.006])

    def polynomial(time: float) -> float:
        return float(sum(value * time**degree for degree, value in enumerate(coefficients)))

    def derivative(time: float) -> float:
        return float(sum(
            degree * value * time ** (degree - 1)
            for degree, value in enumerate(coefficients)
            if degree
        ))

    rows = []
    maximum = 0.0
    for height in (0.013, 0.07, 0.31, 0.8):
        average = quad(
            polynomial, -height, height, epsabs=1e-13, epsrel=1e-13
        )[0] / (2.0 * height)
        left = quad(
            lambda time: ((time + height) / (2.0 * height)) * derivative(time),
            -height,
            0.0,
            epsabs=1e-13,
            epsrel=1e-13,
        )[0]
        right = quad(
            lambda time: ((time - height) / (2.0 * height)) * derivative(time),
            0.0,
            height,
            epsabs=1e-13,
            epsrel=1e-13,
        )[0]
        reconstructed = average + left + right
        residual = abs(reconstructed - polynomial(0.0))
        maximum = max(maximum, residual)
        require(residual < 2e-12, f"trace identity h={height}")
        rows.append({
            "height": height,
            "trace": polynomial(0.0),
            "reconstructed": reconstructed,
            "residual": residual,
        })
    return {
        "passed": True,
        "polynomialCoefficients": coefficients.tolist(),
        "maximumResidual": maximum,
        "rows": rows,
    }


def variable_denominator() -> dict[str, object]:
    rows = []
    maximum = 0.0
    for rate in (-1.7, -0.2, 0.4, 2.3):
        for time in (-0.3, 0.0, 0.6):
            g = math.exp(rate * time)
            y = math.exp(2.0 * rate * time)
            f = g / math.sqrt(y)
            g_term = rate * g / math.sqrt(y)
            denominator_term = (2.0 * rate * y) * f / (2.0 * y)
            residual = abs(g_term - denominator_term)
            maximum = max(maximum, residual, abs(f - 1.0))
            rows.append({
                "rate": rate,
                "time": time,
                "f": f,
                "gTimeTerm": g_term,
                "denominatorTerm": denominator_term,
                "residual": residual,
            })
    require(maximum < 8e-15, "variable denominator cancellation")
    return {"passed": True, "maximumResidual": maximum, "rows": rows}


def double_scaling() -> dict[str, object]:
    viscosity = 1.0
    tau = 0.05
    atom_coefficient = math.exp(-2.0 * viscosity * tau) / 4.0
    budget_coefficient = (
        1.0 - math.exp(-4.0 * viscosity * tau)
    ) / (16.0 * viscosity)
    expected_ratio_coefficient = 2.0 * viscosity / math.sinh(
        2.0 * viscosity * tau
    )
    rows = []
    maximum = 0.0
    for frequency in (1, 2, 4, 8, 16, 32, 64, 128):
        amplitude = frequency ** -2
        atom = atom_coefficient * amplitude**2
        budget = frequency ** -2 * budget_coefficient * amplitude**2
        ratio = atom / budget
        normalized = ratio / frequency**2
        residual = relative_error(normalized, expected_ratio_coefficient)
        maximum = max(maximum, residual)
        rows.append({
            "lambda": frequency,
            "amplitude": amplitude,
            "leadingAtom": atom,
            "leadingBareBudget": budget,
            "ratio": ratio,
            "ratioOverLambdaSquared": normalized,
            "scaledEnergy": frequency**2 * amplitude**2,
            "scaledHOneHalfSquared": frequency**3 * amplitude**2,
            "scaledEnstrophy": frequency**4 * amplitude**2,
        })
    require(maximum < 2e-13, "double-scaling coefficient")
    return {
        "passed": True,
        "tau": tau,
        "viscosity": viscosity,
        "expectedRatioOverLambdaSquared": expected_ratio_coefficient,
        "maximumResidual": maximum,
        "rows": rows,
    }


def resonant_normal_form() -> dict[str, object]:
    rows = []
    maximum = 0.0
    for viscosity in (0.3, 1.0, 2.1):
        for amplitude in (0.07, 0.2):
            for tau in (0.01, 0.08):
                forcing = -0.37
                initial = -(amplitude**2) * tau * forcing

                def target(time: float) -> float:
                    return math.exp(-2.0 * viscosity * time) * (
                        initial + amplitude**2 * time * forcing
                    )

                endpoint = target(tau)
                slope = amplitude**2 * math.exp(
                    -2.0 * viscosity * tau
                ) * forcing
                step = 1e-6
                numerical_slope = (target(tau + step) - target(tau - step)) / (2 * step)
                residual = max(abs(endpoint), relative_error(numerical_slope, slope))
                maximum = max(maximum, residual)
                rows.append({
                    "viscosity": viscosity,
                    "amplitude": amplitude,
                    "tau": tau,
                    "endpoint": endpoint,
                    "slope": slope,
                    "finiteDifferenceSlope": numerical_slope,
                    "residual": residual,
                })
    require(maximum < 2e-10, "resonant normal form")
    return {"passed": True, "maximumResidual": maximum, "rows": rows}


def build_certificate() -> dict[str, object]:
    started = perf_counter()
    checks = {
        "fourierSeed": fourier_seed(),
        "resonantNormalForm": resonant_normal_form(),
        "outgoingCoarea": outgoing_coarea(),
        "traceVariation": trace_variation(),
        "variableDenominator": variable_denominator(),
        "doubleScaling": double_scaling(),
    }
    require(all(check["passed"] for check in checks.values()), "all independent checks")
    return {
        "release": "R0.71T",
        "status": "passed",
        "implementation": (
            "standalone NumPy FFT, SciPy adaptive quadrature, direct finite "
            "differences, and floating-point scaling reconstruction"
        ),
        "elapsedSeconds": perf_counter() - started,
        "checks": checks,
        "claimBoundary": (
            "Independent finite corroboration only. It does not replace the "
            "classical NSE flow-map theorem, prove a Leray occupation bound, "
            "or give a regularity conclusion."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.dumps(build_certificate(), indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
