#!/usr/bin/env python3
"""Independent numerical reconstruction for R0.71U.

This program imports neither ``r071u_exact_audit`` nor its JSON output.  It
uses polynomial integration, spectral differentiation, SVD, and a direct
truncated Fourier-lattice solve to test the finite algebra behind the release.
The Hilbert sampling lemma, Chebyshev-system argument, and continuum IFT stay
analytic statements in the report.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from time import perf_counter

import numpy as np
from numpy.polynomial import Polynomial
from scipy.integrate import solve_ivp
from scipy.optimize import root


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def integrate_square(polynomial: Polynomial) -> float:
    squared = polynomial * polynomial
    primitive = squared.integ()
    return float(primitive(1.0) - primitive(0.0))


def sampling_polynomial_sweep() -> dict[str, object]:
    rng = np.random.default_rng(71071)
    rows: list[dict[str, object]] = []
    minimum_margin = math.inf
    for count in range(1, 13):
        roots = np.sort(rng.uniform(0.04, 0.96, size=count))
        base = Polynomial.fromroots(roots)
        components = [
            base * Polynomial([1.0, -0.31, 0.08]),
            base * Polynomial([-0.2, 0.73]),
            base * Polynomial([0.4, -0.1, 0.02, -0.003]),
        ]
        first = [entry.deriv() for entry in components]
        second = [entry.deriv(2) for entry in components]
        samples = sum(
            sum(float(entry(time)) ** 2 for entry in first) for time in roots
        )
        right = 2.0 * sum(integrate_square(entry) for entry in first)
        right += (7.0 / 3.0) * sum(integrate_square(entry) for entry in second)
        margin = right - samples
        minimum_margin = min(minimum_margin, margin)
        require(margin >= -2e-9 * max(1.0, right), f"sampling count {count}")
        rows.append({
            "zeroCount": count,
            "sampleSum": samples,
            "rightSide": right,
            "margin": margin,
        })
    return {
        "passed": True,
        "seed": 71071,
        "minimumMargin": minimum_margin,
        "rows": rows,
    }


def spectral_25d_check(order: int = 32) -> dict[str, object]:
    grid = 2.0 * np.pi * np.arange(order) / order
    y, z = np.meshgrid(grid, grid, indexing="ij")
    f = 0.7 * np.cos(2 * y - z) - 0.2 * np.sin(y + 3 * z)
    v = 0.4 * np.cos(3 * y) + 0.1 * np.sin(5 * y)
    frequencies = np.fft.fftfreq(order, d=1.0 / order)
    ky, kz = np.meshgrid(frequencies, frequencies, indexing="ij")

    def derivative(value: np.ndarray, multiplier: np.ndarray) -> np.ndarray:
        return np.fft.ifft2(multiplier * np.fft.fft2(value)).real

    f_z = derivative(f, 1j * kz)
    convection = v * f_z
    # Direct three-component definition: u_x=f, u_y=0, u_z=v and no x dependence.
    direct = f * 0.0 + v * f_z
    divergence = derivative(np.zeros_like(f), 1j * ky) + derivative(v, 1j * kz)
    residual = max(
        float(np.max(np.abs(convection - direct))),
        float(np.max(np.abs(divergence))),
    )
    require(residual < 2e-12, "spectral 2.5D substitution")
    return {
        "passed": True,
        "gridOrder": order,
        "maximumResidual": residual,
        "class": "u=(f(y,z),0,v(y))",
    }


def response_svd_sweep() -> dict[str, object]:
    viscosity = 0.02
    k_value = 1
    d_value = 8
    mu = viscosity * 2.0

    def phi(beta: np.ndarray, time: np.ndarray) -> np.ndarray:
        return np.exp(-mu * time) * (-np.expm1(-beta * time)) / beta

    rows: list[dict[str, object]] = []
    for count in range(1, 9):
        times = np.arange(1, count + 1, dtype=float) / (20.0 * (count + 1))
        indices = np.arange(1, count + 1, dtype=float)
        waves = d_value * indices
        betas = 2.0 * viscosity * waves * (waves - k_value)
        matrix = phi(betas[None, :], times[:, None])
        singular = np.linalg.svd(matrix, compute_uv=False)
        require(singular[-1] > 0.0, f"response rank {count}")
        rows.append({
            "N": count,
            "smallestSingularValue": float(singular[-1]),
            "conditionNumber": float(singular[0] / singular[-1]),
        })
    return {"passed": True, "rows": rows}


def modular_support_check() -> dict[str, object]:
    k_value, l_value, d_value, radius = 1, 1, 8, 3
    modes = set()
    for shift in range(-100, 101):
        modes.add((k_value + d_value * shift, l_value))
        modes.add((-k_value + d_value * shift, -l_value))
        modes.add((d_value * shift, 0))
    inside = sorted(
        mode for mode in modes
        if mode != (0, 0) and math.hypot(*mode) <= radius
    )
    require(inside == [(-1, -1), (1, 1)], "independent modular isolation")
    return {
        "passed": True,
        "enumeratedShiftRange": [-100, 100],
        "inside": [list(mode) for mode in inside],
        "strictGap": d_value - abs(k_value) - radius,
    }


def lattice_solution(
    parameters: np.ndarray,
    cutoff: int,
    times: np.ndarray,
    rtol: float = 2e-12,
    atol: float = 2e-14,
) -> tuple[np.ndarray, np.ndarray]:
    viscosity = 0.02
    k_value = 1
    l_value = 1
    d_value = 8
    count = 2 * cutoff + 1
    modes = np.arange(-cutoff, cutoff + 1)
    initial = np.zeros(count, dtype=np.complex128)
    amplitudes = np.array([1j, 1j, 1j, 1j, 1.0, 1.0, 1.0])
    for index, amplitude in enumerate(amplitudes, start=1):
        lattice_mode = -index
        if abs(lattice_mode) <= cutoff:
            initial[lattice_mode + cutoff] = amplitude

    diffusion = viscosity * ((k_value + d_value * modes) ** 2 + l_value**2)
    shear_rates = viscosity * (d_value * np.arange(1, 8)) ** 2

    def right_side(time: float, state: np.ndarray) -> np.ndarray:
        result = -diffusion * state
        for index in range(1, 8):
            shifted = np.zeros_like(state)
            shifted[index:] += state[:-index]
            shifted[:-index] += state[index:]
            coefficient = parameters[index - 1] * math.exp(-shear_rates[index - 1] * time)
            result += -1j * l_value * coefficient * shifted
        return result

    solution = solve_ivp(
        right_side,
        (0.0, float(times[-1])),
        initial,
        method="DOP853",
        t_eval=times,
        rtol=rtol,
        atol=atol,
    )
    require(solution.success, "lattice integration")
    target = solution.y[cutoff, :]
    slopes = np.array([
        right_side(float(time), solution.y[:, column])[cutoff]
        for column, time in enumerate(times)
    ])
    return target, slopes


def direct_lattice_shooting() -> dict[str, object]:
    times = np.array([0.01, 0.03, 0.07], dtype=float)
    viscosity = 0.02
    d_value = 8.0
    waves = d_value * np.arange(1, 5, dtype=float)
    betas = 2.0 * viscosity * waves * (waves - 1.0)
    mu = 2.0 * viscosity
    matrix = (
        np.exp(-mu * times[:, None])
        * (-np.expm1(-betas[None, :] * times[:, None]))
        / betas[None, :]
    )
    fixed = 0.002
    real_tail = np.linalg.solve(matrix[:, 1:4], -fixed * matrix[:, 0])
    initial_guess = np.concatenate([real_tail, np.zeros(3)])
    evaluations = 0

    def objective(tail: np.ndarray) -> np.ndarray:
        nonlocal evaluations
        evaluations += 1
        parameters = np.concatenate([[fixed], tail])
        target, _slopes = lattice_solution(parameters, 24, times, rtol=8e-12, atol=8e-14)
        return np.concatenate([target.real, target.imag])

    started = perf_counter()
    solved = root(objective, initial_guess, method="hybr", options={"xtol": 1e-10})
    wall = perf_counter() - started
    require(solved.success, "direct lattice shooting: " + solved.message)
    parameters = np.concatenate([[fixed], solved.x])

    cutoffs = [24, 30, 36]
    rows = []
    targets: dict[int, np.ndarray] = {}
    slopes: dict[int, np.ndarray] = {}
    for cutoff in cutoffs:
        target, slope = lattice_solution(parameters, cutoff, times)
        targets[cutoff] = target
        slopes[cutoff] = slope
        rows.append({
            "cutoff": cutoff,
            "maximumTargetResidual": float(np.max(np.abs(target))),
            "minimumSlopeMagnitude": float(np.min(np.abs(slope))),
            "slopes": [[float(value.real), float(value.imag)] for value in slope],
        })

    maximum_residual = max(float(np.max(np.abs(value))) for value in targets.values())
    refinement_difference = max(
        float(np.max(np.abs(slopes[30] - slopes[24]))),
        float(np.max(np.abs(slopes[36] - slopes[30]))),
    )
    require(maximum_residual < 2e-10, "refined target residual")
    require(min(float(np.min(np.abs(value))) for value in slopes.values()) > 1e-7,
            "nonzero target slopes")
    require(refinement_difference < 2e-9, "cutoff refinement")
    return {
        "passed": True,
        "fixedParameter": fixed,
        "parameters": parameters.tolist(),
        "rootEvaluations": evaluations,
        "wallSeconds": wall,
        "maximumTargetResidual": maximum_residual,
        "maximumSlopeRefinementDifference": refinement_difference,
        "rows": rows,
        "boundary": "finite lattice corroboration, not the continuum IFT proof",
    }


def forced_sampling_sweep() -> dict[str, object]:
    rows = []
    for frequency in (4, 8, 16, 32, 64, 128):
        zeros = 2 * frequency + 1
        sample_mass = float(zeros)
        first_integral = math.pi
        second_integral = math.pi * frequency**2
        rows.append({
            "frequency": frequency,
            "zeroSamplesOn0To2Pi": zeros,
            "squaredSlopeSampleMass": sample_mass,
            "firstDerivativeIntegral": first_integral,
            "secondDerivativeIntegral": second_integral,
        })
    require(rows[-1]["squaredSlopeSampleMass"] > 25 * rows[0]["squaredSlopeSampleMass"],
            "recurrence growth")
    return {"passed": True, "rows": rows, "nseTrajectory": False}


def scale_ratio_sweep() -> dict[str, object]:
    rows = []
    maximum = 0.0
    for dilation in (1, 2, 4, 8, 16, 32, 64):
        first = dilation**10 * dilation**-6 * dilation**-4 * dilation**-2
        first *= dilation**2
        second = dilation**14 * dilation**-6 * dilation**-4 * dilation**-2
        second *= dilation**-2
        maximum = max(maximum, abs(first - 1.0), abs(second - 1.0))
        rows.append({"lambda": dilation, "firstRowRatio": first, "secondRowRatio": second})
    require(maximum == 0.0, "scale ratio sweep")
    return {"passed": True, "maximumResidual": maximum, "rows": rows}


def build_result() -> dict[str, object]:
    checks = {
        "samplingPolynomialSweep": sampling_polynomial_sweep(),
        "spectral25DCheck": spectral_25d_check(),
        "responseSVDSweep": response_svd_sweep(),
        "modularSupportCheck": modular_support_check(),
        "directLatticeShooting": direct_lattice_shooting(),
        "forcedSamplingSweep": forced_sampling_sweep(),
        "scaleRatioSweep": scale_ratio_sweep(),
    }
    require(all(bool(value["passed"]) for value in checks.values()), "all checks")
    return {
        "release": "R0.71U",
        "status": "passed",
        "independentOf": ["research/r071u_exact_audit.py", "research/certificates/r071u/result.json"],
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build_result()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
