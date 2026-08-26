#!/usr/bin/env python3
"""Independent numerical audit for the R0.71P entry-batching result.

This checker imports neither the exact producer nor prior release code.  It
tests random finite overlap ledgers, detects the entries of the oscillatory
path from sampled signs and Brent roots, integrates the soft rising layers,
and reconstructs the sharp NSE initial entry with a standalone FFT.

The numerical checks corroborate finite algebra.  They do not prove a uniform
NSE zero count, an internal NSE multiple-face construction, or regularity.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from time import perf_counter

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def relative_error(value: float, target: float) -> float:
    return abs(value - target) / max(1.0, abs(target))


def random_overlap_ledgers() -> dict[str, object]:
    """Test cellwise projection and bounded overlap with random arrays."""

    generator = np.random.default_rng(71071)
    rows: list[dict[str, float | int]] = []
    maximum_cell_ratio = 0.0
    maximum_overlap_ratio = 0.0
    for trial in range(64):
        dimension = 48
        cell_width = 9
        stride = 5
        starts = list(range(0, dimension - cell_width + 1, stride))
        supports = [np.arange(start, start + cell_width) for start in starts]
        multiplicity = np.zeros(dimension, dtype=np.int64)
        for support in supports:
            multiplicity[support] += 1
        overlap = int(np.max(multiplicity))

        field = generator.normal(size=dimension)
        enstrophy = float(0.5 + generator.random())
        entry_sum = 0.0
        local_budget_sum = 0.0
        cell_ratio = 0.0
        for support in supports:
            direction = np.zeros(dimension)
            direction[support] = generator.normal(size=cell_width)
            norm_squared = float(np.dot(direction, direction))
            pairing = float(np.dot(field, direction))
            atom = max(pairing, 0.0) ** 2 / (enstrophy * norm_squared)
            local_budget = float(np.dot(field[support], field[support]) / enstrophy)
            entry_sum += atom
            local_budget_sum += local_budget
            if local_budget > 0.0:
                cell_ratio = max(cell_ratio, atom / local_budget)

        overlap_budget = overlap * float(np.dot(field, field)) / enstrophy
        require(entry_sum <= local_budget_sum * (1.0 + 3e-14),
                f"trial {trial} local sum")
        require(local_budget_sum <= overlap_budget * (1.0 + 3e-14),
                f"trial {trial} overlap sum")
        overlap_ratio = entry_sum / overlap_budget
        maximum_cell_ratio = max(maximum_cell_ratio, cell_ratio)
        maximum_overlap_ratio = max(maximum_overlap_ratio, overlap_ratio)
        rows.append({
            "trial": trial,
            "cellCount": len(supports),
            "overlap": overlap,
            "entrySum": entry_sum,
            "localBudgetSum": local_budget_sum,
            "overlapBudget": overlap_budget,
            "maximumCellRatio": cell_ratio,
            "entryToOverlapRatio": overlap_ratio,
        })

    require(maximum_cell_ratio <= 1.0 + 3e-14, "cellwise Cauchy constant")
    require(maximum_overlap_ratio <= 1.0 + 3e-14, "overlap constant")
    return {
        "passed": True,
        "seed": 71071,
        "trialCount": len(rows),
        "maximumCellRatio": maximum_cell_ratio,
        "maximumEntryToOverlapRatio": maximum_overlap_ratio,
        "rows": rows,
    }


def oscillatory_entries() -> dict[str, object]:
    """Detect entry times and independently integrate each soft rising layer."""

    rows: list[dict[str, float | int]] = []
    maximum_entry_error = 0.0
    maximum_soft_error = 0.0
    for frequency in (1, 2, 4, 8, 16, 32, 64):
        samples_per_period = 20
        sample_count = samples_per_period * frequency
        times = np.linspace(0.0, 2.0 * np.pi, sample_count + 1)

        def c(time: float) -> float:
            return np.sin(frequency * time) / frequency

        values = np.array([c(time) for time in times])
        entry_times = [0.0]
        for index in range(1, sample_count):
            left = values[index]
            right = values[index + 1]
            if left <= 0.0 and right > 0.0:
                if abs(left) < 2e-14:
                    root = times[index]
                else:
                    root = brentq(c, times[index], times[index + 1])
                if root > 1e-12:
                    entry_times.append(float(root))

        hard_entry_mass = float(len(entry_times))
        entry_error = abs(hard_entry_mass - frequency)
        maximum_entry_error = max(maximum_entry_error, entry_error)
        require(entry_error == 0.0, f"frequency {frequency} entry count")
        require(
            max(entry_times) < 2.0 * np.pi,
            f"frequency {frequency} right endpoint excluded",
        )

        epsilon = frequency ** -4

        def soft_derivative(time: float) -> float:
            value = c(time)
            if value <= 0.0:
                return 0.0
            derivative = np.cos(frequency * time)
            return (
                2.0 * epsilon * value * derivative
                / (value * value + epsilon) ** 2
            )

        rising_mass, quadrature_error = quad(
            soft_derivative,
            0.0,
            np.pi / (2.0 * frequency),
            epsabs=2e-12,
            epsrel=2e-12,
            limit=500,
        )
        soft_positive_mass = frequency * rising_mass
        expected_soft = frequency / (1.0 + frequency**-2)
        soft_error = relative_error(soft_positive_mass, expected_soft)
        maximum_soft_error = max(maximum_soft_error, soft_error)
        require(soft_error < 2e-10, f"frequency {frequency} soft mass")

        time_integral_batch_density = 2.0 * np.pi
        denominator_mass = np.pi / frequency**2
        rows.append({
            "N": frequency,
            "window": "[0,2*pi)",
            "rightEndpointExcluded": True,
            "detectedEntryCount": len(entry_times),
            "hardEntryMass": hard_entry_mass,
            "countingIntegral": hard_entry_mass,
            "ordinaryTimeIntegralOfUnitBatchDensity": time_integral_batch_density,
            "softPositiveMass": soft_positive_mass,
            "expectedSoftPositiveMass": expected_soft,
            "softRelativeError": soft_error,
            "quadratureError": quadrature_error,
            "denominatorMass": denominator_mass,
            "C_tSquareMass": np.pi,
            "FTimeMass": 2.0 * np.pi,
        })

    require(rows[-1]["hardEntryMass"] == 64.0, "large entry count")
    require(rows[-1]["denominatorMass"] < 1e-3,
            "small denominator mass")
    return {
        "passed": True,
        "maximumEntryCountError": maximum_entry_error,
        "maximumSoftRelativeError": maximum_soft_error,
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


def coefficient_inner(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.vdot(left, right).real)


def nse_sharp_initial_entry(order: int = 32) -> dict[str, object]:
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
    filtered_vorticity_hat = np.where(
        shell[..., None], vorticity_hat, 0.0
    )
    viscous_filtered_jet_hat = -squared[..., None] * filtered_vorticity_hat
    F_hat = np.where(shell[..., None], lamb_hat, 0.0)
    G_hat = spectral_curl(F_hat, waves)
    c_hat = spectral_curl(G_hat, waves)

    Y0 = coefficient_norm_squared(vorticity_hat)
    filtered_vorticity2 = coefficient_norm_squared(filtered_vorticity_hat)
    viscous_filtered_jet2 = coefficient_norm_squared(
        viscous_filtered_jet_hat
    )
    F2 = coefficient_norm_squared(F_hat)
    c2 = coefficient_norm_squared(c_hat)
    pairing = coefficient_inner(F_hat, c_hat)
    atom = pairing**2 / (Y0 * c2)
    budget = F2 / Y0
    ratio = atom / budget
    cauchy_residual = F2 * c2 - pairing**2
    residuals = {
        "Y0": abs(Y0 - 1.0),
        "initialFilteredVorticity2": abs(filtered_vorticity2),
        "initialFilteredViscousJet2": abs(viscous_filtered_jet2),
        "F2": abs(F2 - 0.25),
        "c2": abs(c2 - 1.0),
        "pairing": abs(pairing - 0.5),
        "entryAtom": abs(atom - 0.25),
        "projectionBudget": abs(budget - 0.25),
        "sharpnessRatio": abs(ratio - 1.0),
        "CauchyResidual": abs(cauchy_residual),
    }
    maximum_residual = max(residuals.values())
    require(maximum_residual < 2e-13, "NSE initial sharpness")
    return {
        "passed": True,
        "gridOrder": order,
        "Y0": Y0,
        "initialFilteredVorticity2": filtered_vorticity2,
        "initialFilteredViscousJet2": viscous_filtered_jet2,
        "F2": F2,
        "leadingDirection2": c2,
        "leadingPairing": pairing,
        "rightEntryAtom": atom,
        "projectionBudget": budget,
        "sharpnessRatio": ratio,
        "CauchyResidual": cauchy_residual,
        "maximumResidual": maximum_residual,
        "residuals": residuals,
    }


def run() -> dict[str, object]:
    started = perf_counter()
    checks = {
        "randomOverlapLedgers": random_overlap_ledgers(),
        "oscillatoryEntries": oscillatory_entries(),
        "nseSharpInitialEntry": nse_sharp_initial_entry(),
    }
    return {
        "release": "R0.71P",
        "status": "passed",
        "implementation": (
            "standalone NumPy overlap tests, sampled-sign/Brent entry "
            "detection, SciPy quadrature, and NumPy FFT"
        ),
        "checks": checks,
        "wallSeconds": perf_counter() - started,
        "claimBoundary": (
            "Floating-point corroboration of finite overlap batching, an "
            "abstract sequential-entry family, and one sharp NSE initial jet. "
            "No time-stepped NSE multiple-face result, interval certificate, "
            "uniform zero count, or regularity conclusion."
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
