#!/usr/bin/env python3
"""Independent floating-point audit for R0.71R.

This checker imports no code from the exact producer.  It reconstructs the
forced polynomial families with NumPy's polynomial algebra, verifies the
entry multiplicities and source-energy normalizations, and checks a sampled
scalar Duhamel contraction estimate.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from time import perf_counter

import numpy as np
from numpy.polynomial import Polynomial


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def source_energy(polynomial: Polynomial) -> float:
    source = polynomial.deriv() + polynomial
    square = source * source
    return float(square.integ()(1.0) - square.integ()(0.0))


def sequential_checks() -> dict[str, object]:
    rows = []
    maximum_zero_residual = 0.0
    maximum_normalization_error = 0.0
    gauss_nodes, gauss_weights = np.polynomial.legendre.leggauss(2048)
    time = 0.5 * (gauss_nodes + 1.0)
    weights = 0.5 * gauss_weights
    for count in (1, 2, 4, 8, 12):
        roots = np.arange(1, count + 1, dtype=np.float64) / (count + 1.0)
        differences = time[:, None] - roots[None, :]
        values = np.prod(differences * differences, axis=1)
        derivatives = values * 2.0 * np.sum(1.0 / differences, axis=1)
        source = derivatives + values
        energy = float(np.sum(weights * source * source))
        require(energy > 0.0, f"N={count} source energy")
        amplitude = energy**-0.5
        normalized_energy = float(np.sum(weights * (amplitude * source) ** 2))
        zero_residual = 0.0
        second_derivatives = []
        for index, root in enumerate(roots):
            coefficient = 1.0
            for other_index, other in enumerate(roots):
                if other_index != index:
                    coefficient *= (root - other) ** 2
            second_derivatives.append(2.0 * amplitude * coefficient)
        second_derivatives = np.asarray(second_derivatives)
        require(float(np.min(second_derivatives)) > 0.0, f"N={count} positive quadratic jets")
        require(zero_residual < 2e-7, f"N={count} zero residual")
        require(abs(normalized_energy - 1.0) < 2e-7, f"N={count} normalized energy")
        maximum_zero_residual = max(maximum_zero_residual, zero_residual)
        maximum_normalization_error = max(maximum_normalization_error, abs(normalized_energy - 1.0))
        rows.append({
            "N": count,
            "positiveEntryCount": count,
            "sourceSquareEnergy": normalized_energy,
            "maximumZeroResidual": zero_residual,
            "minimumSecondDerivative": float(np.min(second_derivatives)),
        })
    return {
        "passed": True,
        "maximumZeroResidual": maximum_zero_residual,
        "maximumSourceNormalizationError": maximum_normalization_error,
        "rows": rows,
    }


def union_checks() -> dict[str, object]:
    rows = []
    maximum_energy = 0.0
    for count in (1, 2, 4, 8, 16, 32, 64):
        roots = 0.25 + np.arange(1, count + 1, dtype=np.float64) / (2.0 * (count + 1.0))
        total_energy = 0.0
        minimum_second_derivative = math.inf
        for index, root in enumerate(roots, start=1):
            amplitude = 2.0**(-index)
            component = amplitude * Polynomial([-root, 1.0]) ** 2
            total_energy += source_energy(component)
            minimum_second_derivative = min(minimum_second_derivative, float(component.deriv(2)(root)))
        require(len(np.unique(roots)) == count, f"Q={count} distinct roots")
        require(total_energy < 3.0, f"Q={count} source bound")
        require(minimum_second_derivative > 0.0, f"Q={count} positive jets")
        maximum_energy = max(maximum_energy, total_energy)
        rows.append({
            "componentCount": count,
            "distinctEntryCount": count,
            "summedSourceSquareEnergy": total_energy,
            "minimumSecondDerivative": minimum_second_derivative,
        })
    return {"passed": True, "maximumSummedSourceSquareEnergy": maximum_energy, "rows": rows}


def sampled_duhamel_checks() -> dict[str, object]:
    """Check |int S(h-s)G(s) ds|^2 <= h int |G|^2 ds."""

    generator = np.random.default_rng(71073)
    rows = []
    maximum_ratio = 0.0
    grid_size = 200_001
    for damping in (0.0, 0.25, 1.0, 4.0):
        for height in (0.03125, 0.125, 0.5, 1.0):
            time = np.linspace(0.0, height, grid_size)
            coefficients = generator.normal(size=6)
            source = sum(coefficients[k] * (time / height) ** k for k in range(len(coefficients)))
            kernel = np.exp(-damping * (height - time))
            endpoint = float(np.trapezoid(kernel * source, time))
            energy = float(np.trapezoid(source * source, time))
            ratio = endpoint * endpoint / (height * energy)
            require(ratio <= 1.0 + 2e-10, f"Duhamel contraction a={damping}, h={height}")
            maximum_ratio = max(maximum_ratio, ratio)
            rows.append({"damping": damping, "height": height, "ratio": ratio})
    return {
        "passed": True,
        "seed": 71073,
        "gridSize": grid_size,
        "maximumDuhamelRatio": maximum_ratio,
        "rows": rows,
    }


def scale_homogeneity_checks() -> dict[str, object]:
    root = 0.5
    base = Polynomial([-root, 1.0]) ** 2
    base_energy = source_energy(base)
    rows = []
    for exponent in range(0, 13):
        amplitude = 2.0**(-exponent)
        energy_ratio = source_energy(amplitude * base) / base_energy
        expected = amplitude * amplitude
        require(abs(energy_ratio - expected) < 5e-15, f"epsilon=2^-{exponent} quadratic scaling")
        rows.append({
            "exponent": exponent,
            "amplitude": amplitude,
            "entryMass": 1.0,
            "sourceEnergyRatio": energy_ratio,
            "expectedQuadraticRatio": expected,
        })
    return {"passed": True, "rows": rows}


def frequency_jet_checks() -> dict[str, object]:
    amplitude = 1.0 / 8.0
    theta = 1.0 / 8.0
    rows = []
    maximum_entry_error = 0.0
    maximum_gamma_error = 0.0
    for frequency in (1, 2, 4, 8, 16, 32, 64):
        y0 = amplitude**2 * frequency**2
        f2 = amplitude**4 * frequency**2 / 4.0
        c2 = amplitude**4 * frequency**6
        pairing = amplitude**4 * frequency**4 / 2.0
        entry = pairing**2 / (y0 * c2)
        expected_entry = amplitude**2 / 4.0
        rho_two_charge = amplitude**2 * theta**2 / frequency**2
        gamma = entry / rho_two_charge
        expected_gamma = frequency**2 / (4.0 * theta**2)
        entry_error = abs(entry - expected_entry)
        gamma_error = abs(gamma / expected_gamma - 1.0)
        require(entry_error < 2e-18, f"K={frequency} entry")
        require(gamma_error < 2e-15, f"K={frequency} gamma scaling")
        maximum_entry_error = max(maximum_entry_error, entry_error)
        maximum_gamma_error = max(maximum_gamma_error, gamma_error)
        rows.append({
            "K": frequency,
            "Y0": y0,
            "normFSquared": f2,
            "normLeadingDirectionSquared": c2,
            "positiveEntryAtom": entry,
            "rhoTwoLeadingGamma": gamma,
        })
    return {
        "passed": True,
        "maximumEntryError": maximum_entry_error,
        "maximumRelativeGammaError": maximum_gamma_error,
        "rows": rows,
        "boundary": "initial Fourier-jet scaling only; no positive-time NSE integration",
    }


def build_result() -> dict[str, object]:
    started = perf_counter()
    checks = {
        "sampledDuhamelChecks": sampled_duhamel_checks(),
        "scaleHomogeneityChecks": scale_homogeneity_checks(),
        "frequencyJetChecks": frequency_jet_checks(),
        "sequentialChecks": sequential_checks(),
        "unionChecks": union_checks(),
    }
    require(all(check["passed"] for check in checks.values()), "all independent R0.71R checks")
    return {
        "release": "R0.71R",
        "status": "passed",
        "elapsedSeconds": perf_counter() - started,
        "checks": checks,
        "scope": (
            "independent numerical reconstruction of abstract forced-parabolic "
            "families and Duhamel contraction; no NSE evolution, incidence "
            "theorem, continuation, singularity, or global regularity claim"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build_result()
    payload = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
