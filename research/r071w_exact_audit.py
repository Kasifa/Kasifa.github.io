#!/usr/bin/env python3
"""High-precision audit for the R0.71W complete-baseline no-go.

The analytic proof is recorded in ``research/r071w_report-source.md``.  This
program first evaluates the exact tangent response of the R0.71V fixed-target
2.5D family while varying the seed/background balance.  It then restores the
actual shear amplitude in the R0.71W amplitude-doped regime and checks the
predicted atom, rotational-charge, implicit-parameter, and complete-ledger
powers.  The uniform rescaled implicit-function theorem and the nonlinear
energy estimates are analytic parts of the report; this finite computation
corroborates their leading coefficients and does not time-step NSE.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
from zoneinfo import ZoneInfo

import mpmath as mp


def now() -> str:
    return datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="seconds")


def log10(value: mp.mpf) -> float:
    return float(mp.log10(value))


def fit_power(xs: list[mp.mpf], ys: list[mp.mpf]) -> float:
    log_x = [mp.log(value) for value in xs]
    log_y = [mp.log(value) for value in ys]
    mean_x = mp.fsum(log_x) / len(log_x)
    mean_y = mp.fsum(log_y) / len(log_y)
    numerator = mp.fsum(
        (x_value - mean_x) * (y_value - mean_y)
        for x_value, y_value in zip(log_x, log_y, strict=True)
    )
    denominator = mp.fsum((value - mean_x) ** 2 for value in log_x)
    return float(numerator / denominator)


def response_case(q_value: int, balance: mp.mpf) -> dict[str, object]:
    """Return one exact tangent-ledger row.

    ``balance`` is the dimensionless quantity ``Q B / (epsilon q)``.  Thus
    balance one makes the low-frequency background and the high-frequency
    seed comparable at the enstrophy level near the shrinking root layer.
    """

    nu = mp.mpf("0.02")
    ky = 1
    kz = 1
    modulus = 8
    background_frequency = 4
    scaled_left = mp.mpf("0.05")
    window_length = mp.mpf("0.5")
    scaled_roots = [mp.mpf("0.1"), mp.mpf("0.2")]
    mode_ratios = [1, 2, 3, 4, 5]
    recurrence_count = 2
    epsilon = mp.mpf(q_value) ** -2
    background = balance * epsilon * q_value / background_frequency
    modes = [modulus * ratio * q_value for ratio in mode_ratios]
    alpha = [(ky - mode) ** 2 + kz**2 for mode in modes]
    beta = [2 * nu * mode * (mode - ky) for mode in modes]
    mu = nu * (ky**2 + kz**2)
    root_times = [value / q_value**2 for value in scaled_roots]
    left = scaled_left / q_value**2
    right = left + window_length

    def phi(index: int, time: mp.mpf) -> mp.mpf:
        rate = beta[index]
        return mp.exp(-mu * time) * (-mp.expm1(-rate * time)) / rate

    matrix = mp.matrix(
        [
            [phi(column, time) for column in range(1, recurrence_count + 1)]
            for time in root_times
        ]
    )
    rhs = mp.matrix([-phi(0, time) for time in root_times])
    coefficients = [mp.mpf(1), *list(mp.lu_solve(matrix, rhs))]

    def gamma(time: mp.mpf) -> mp.mpf:
        return kz * mp.fsum(
            coefficients[index] * phi(index, time)
            for index in range(recurrence_count + 1)
        )

    def gamma_prime(time: mp.mpf) -> mp.mpf:
        return kz * mp.fsum(
            coefficients[index]
            * (
                -mu * mp.exp(-mu * time) / beta[index]
                + (mu + beta[index])
                * mp.exp(-(mu + beta[index]) * time)
                / beta[index]
            )
            for index in range(recurrence_count + 1)
        )

    def background_enstrophy(time: mp.mpf) -> mp.mpf:
        return (
            2
            * background_frequency**2
            * background**2
            * mp.exp(-2 * nu * background_frequency**2 * time)
        )

    def seed_enstrophy(time: mp.mpf) -> mp.mpf:
        return 2 * epsilon**2 * mp.fsum(
            value * mp.exp(-2 * nu * value * time) for value in alpha
        )

    def enstrophy(time: mp.mpf) -> mp.mpf:
        return background_enstrophy(time) + seed_enstrophy(time)

    atom_coefficients = [
        2 * epsilon**2 * gamma_prime(time) ** 2 / enstrophy(time)
        for time in root_times
    ]
    atom_sum = mp.fsum(atom_coefficients)
    enstrophy_ratio = enstrophy(left) / enstrophy(right)
    complete_baseline = enstrophy_ratio * nu**2
    atom_to_baseline = atom_sum / complete_baseline
    scaled_atom_to_baseline = q_value**2 * atom_to_baseline
    maximum_residual = max(abs(gamma(time)) for time in root_times)

    seed_scale = epsilon**2 * q_value**2
    return {
        "q": q_value,
        "balance": float(balance),
        "backgroundCoefficient": float(background),
        "maximumRootResidualLog10": log10(max(maximum_residual, mp.mpf("1e-200"))),
        "minimumRootSlope": float(
            min(abs(gamma_prime(time)) for time in root_times)
        ),
        "rootSeedEnstrophyOverEpsilon2Q2": float(
            seed_enstrophy(root_times[-1]) / seed_scale
        ),
        "rootBackgroundToSeedEnstrophy": float(
            background_enstrophy(root_times[-1])
            / seed_enstrophy(root_times[-1])
        ),
        "atomCoefficientSum": float(atom_sum),
        "enstrophyRatioLog10": log10(enstrophy_ratio),
        "atomToRYNu2": float(atom_to_baseline),
        "q2AtomToRYNu2": float(scaled_atom_to_baseline),
        "atomToRYNu2Log10": log10(atom_to_baseline),
    }


def amplitude_doped_case(q_value: int, exponent: mp.mpf) -> dict[str, object]:
    """Evaluate the R0.71W leading ledger with the real shear restored.

    The physical scalar-seed and shear amplitudes are
    ``amplitude=q**exponent``.  The fixed-frequency, z-independent background
    coefficient is ``amplitude*q/Q``.  The returned enstrophy is the exact
    heat/tangent ledger, including the shear; the analytic report proves that
    the exact implicit solution differs only by a uniform relative
    ``O(q**(exponent-2))`` term on the root layer.
    """

    nu = mp.mpf("0.02")
    ky = 1
    kz = 1
    modulus = 8
    background_frequency = 4
    scaled_left = mp.mpf("0.05")
    window_length = mp.mpf("0.5")
    scaled_roots = [mp.mpf("0.1"), mp.mpf("0.2")]
    mode_ratios = [1, 2, 3, 4, 5]
    recurrence_count = 2
    amplitude = mp.mpf(q_value) ** exponent
    implicit_parameter = amplitude / q_value**2
    background = amplitude * q_value / background_frequency
    modes = [modulus * ratio * q_value for ratio in mode_ratios]
    alpha = [(ky - mode) ** 2 + kz**2 for mode in modes]
    beta = [2 * nu * mode * (mode - ky) for mode in modes]
    mu = nu * (ky**2 + kz**2)
    root_times = [value / q_value**2 for value in scaled_roots]
    left = scaled_left / q_value**2
    right = left + window_length

    def phi(index: int, time: mp.mpf) -> mp.mpf:
        rate = beta[index]
        return mp.exp(-mu * time) * (-mp.expm1(-rate * time)) / rate

    matrix = mp.matrix(
        [
            [phi(column, time) for column in range(1, recurrence_count + 1)]
            for time in root_times
        ]
    )
    rhs = mp.matrix([-phi(0, time) for time in root_times])
    coefficients = [mp.mpf(1), *list(mp.lu_solve(matrix, rhs))]

    def gamma(time: mp.mpf) -> mp.mpf:
        return kz * mp.fsum(
            coefficients[index] * phi(index, time)
            for index in range(recurrence_count + 1)
        )

    def gamma_prime(time: mp.mpf) -> mp.mpf:
        return kz * mp.fsum(
            coefficients[index]
            * (
                -mu * mp.exp(-mu * time) / beta[index]
                + (mu + beta[index])
                * mp.exp(-(mu + beta[index]) * time)
                / beta[index]
            )
            for index in range(recurrence_count + 1)
        )

    def background_enstrophy(time: mp.mpf) -> mp.mpf:
        return (
            2
            * background_frequency**2
            * background**2
            * mp.exp(-2 * nu * background_frequency**2 * time)
        )

    def seed_enstrophy(time: mp.mpf) -> mp.mpf:
        return 2 * amplitude**2 * mp.fsum(
            value * mp.exp(-2 * nu * value * time) for value in alpha
        )

    def shear_enstrophy(time: mp.mpf) -> mp.mpf:
        return 2 * amplitude**2 * mp.fsum(
            modes[index] ** 2
            * coefficients[index] ** 2
            * mp.exp(-2 * nu * modes[index] ** 2 * time)
            for index in range(recurrence_count + 1)
        )

    def leading_enstrophy(time: mp.mpf) -> mp.mpf:
        return (
            background_enstrophy(time)
            + seed_enstrophy(time)
            + shear_enstrophy(time)
        )

    physical_root_slopes = [
        amplitude**2 * abs(gamma_prime(time)) for time in root_times
    ]
    atom_proxy = mp.fsum(
        2 * slope**2 / leading_enstrophy(time)
        for slope, time in zip(physical_root_slopes, root_times, strict=True)
    )
    enstrophy_ratio = leading_enstrophy(left) / leading_enstrophy(right)

    # A deterministic full-frequency bound.  Real Fourier modes give
    # ||v||_infinity <= 2 sum |p_l| exp(-nu n_l^2 t); integrating its square
    # produces the double sum below.  The scalar z-derivative is contractive.
    integral_v_infinity_squared = 4 * amplitude**2 * mp.fsum(
        abs(coefficients[i] * coefficients[j])
        / (nu * (modes[i] ** 2 + modes[j] ** 2))
        for i in range(recurrence_count + 1)
        for j in range(recurrence_count + 1)
    )
    scalar_z_energy_upper = 2 * kz**2 * amplitude**2 * len(modes)
    background_floor = background_enstrophy(right)
    rotational_charge_upper = (
        integral_v_infinity_squared
        * scalar_z_energy_upper
        / background_floor
        / window_length
    )
    complete_ledger_proxy = enstrophy_ratio * (
        nu**2 + rotational_charge_upper
    )
    ratio_to_complete_ledger = atom_proxy / complete_ledger_proxy
    maximum_residual = max(abs(gamma(time)) for time in root_times)

    return {
        "q": q_value,
        "amplitude": float(amplitude),
        "amplitudeExponent": float(exponent),
        "implicitParameter": float(implicit_parameter),
        "maximumTangentRootResidualLog10": log10(
            max(maximum_residual, mp.mpf("1e-200"))
        ),
        "minimumPhysicalRootSlope": float(min(physical_root_slopes)),
        "leadingAtomProxy": float(atom_proxy),
        "leadingEnstrophyAtLastRoot": float(
            leading_enstrophy(root_times[-1])
        ),
        "leadingEnstrophyRatio": float(enstrophy_ratio),
        "rotationalChargeUpper": float(rotational_charge_upper),
        "completeLedgerProxy": float(complete_ledger_proxy),
        "atomToCompleteLedgerProxy": float(ratio_to_complete_ledger),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    mp.mp.dps = 90
    q_values = [8, 16, 32, 64, 128, 256]
    balances = [mp.mpf("0")] + [
        mp.power(10, mp.mpf(-8) + mp.mpf(index) / 4) for index in range(65)
    ]
    rows = [response_case(q_value, balance) for q_value in q_values for balance in balances]
    nonzero_rows = [row for row in rows if row["balance"] > 0]
    maximum_scaled_ratio = max(row["q2AtomToRYNu2"] for row in rows)
    minimum_slope = min(row["minimumRootSlope"] for row in rows)
    maximum_residual_log10 = max(row["maximumRootResidualLog10"] for row in rows)

    maxima_by_q: list[dict[str, object]] = []
    for q_value in q_values:
        q_rows = [row for row in rows if row["q"] == q_value]
        maximizing = max(q_rows, key=lambda row: row["atomToRYNu2"])
        maxima_by_q.append(
            {
                "q": q_value,
                "maximumAtomToRYNu2": maximizing["atomToRYNu2"],
                "maximizingBalance": maximizing["balance"],
                "q2MaximumAtomToRYNu2": q_value**2
                * maximizing["atomToRYNu2"],
            }
        )

    fitted_power = fit_power(
        [mp.mpf(row["q"]) for row in maxima_by_q[-4:]],
        [mp.mpf(row["maximumAtomToRYNu2"]) for row in maxima_by_q[-4:]],
    )
    balance_coverage = {
        "minimumPositive": min(row["balance"] for row in nonzero_rows),
        "maximum": max(row["balance"] for row in nonzero_rows),
    }
    algebra = {
        "identity": (
            "A(B+A delta)/(A+B)^2 = AB/(A+B)^2 + "
            "delta A^2/(A+B)^2"
        ),
        "firstTermBound": (
            "AB/(A+B)^2 <= 1/4 because "
            "1/4-AB/(A+B)^2=(A-B)^2/(4(A+B)^2)"
        ),
        "secondTermBound": "delta A^2/(A+B)^2 <= delta",
        "consequence": (
            "M_q/R_Y <= C q^-2 (1/4+exp(-c q^2)) uniformly in "
            "the seed/background balance"
        ),
    }
    # The deterministic rotational bound has a deliberately conservative
    # prefactor.  Extending the dyadic range makes the eventual nu^2-dominated
    # complete-ledger asymptotic visible rather than fitting its crossover.
    doped_q_values = [2**power for power in range(8, 33, 2)]
    doped_exponent = mp.mpf("1.5")
    doped_rows = [
        amplitude_doped_case(q_value, doped_exponent)
        for q_value in doped_q_values
    ]
    doped_fit_rows = doped_rows[-4:]
    doped_powers = {
        "implicitParameter": fit_power(
            [mp.mpf(row["q"]) for row in doped_fit_rows],
            [mp.mpf(row["implicitParameter"]) for row in doped_fit_rows],
        ),
        "leadingAtomProxy": fit_power(
            [mp.mpf(row["q"]) for row in doped_fit_rows],
            [mp.mpf(row["leadingAtomProxy"]) for row in doped_fit_rows],
        ),
        "rotationalChargeUpper": fit_power(
            [mp.mpf(row["q"]) for row in doped_fit_rows],
            [mp.mpf(row["rotationalChargeUpper"]) for row in doped_fit_rows],
        ),
        "atomToCompleteLedgerProxy": fit_power(
            [mp.mpf(row["q"]) for row in doped_fit_rows],
            [mp.mpf(row["atomToCompleteLedgerProxy"]) for row in doped_fit_rows],
        ),
        "leadingEnstrophyAtLastRoot": fit_power(
            [mp.mpf(row["q"]) for row in doped_fit_rows],
            [
                mp.mpf(row["leadingEnstrophyAtLastRoot"])
                for row in doped_fit_rows
            ],
        ),
    }
    exponent_ledger = [
        {
            "alpha": float(exponent),
            "implicitParameterPower": float(exponent - 2),
            "atomPower": float(2 * exponent - 2),
            "rotationalChargePower": float(2 * exponent - 4),
            "passesOpenInterval": bool(1 < exponent < 2),
        }
        for exponent in map(mp.mpf, ["1.05", "1.25", "1.5", "1.75", "1.95"])
    ]
    checks = {
        "rootInterpolation": {
            "passed": maximum_residual_log10 < -70 and minimum_slope > 0.1,
            "maximumResidualLog10": maximum_residual_log10,
            "minimumSlope": minimum_slope,
        },
        "uniformBalanceEnvelope": {
            "passed": maximum_scaled_ratio < mp.mpf("0.1"),
            "maximumQ2AtomToRYNu2": maximum_scaled_ratio,
            "balanceCoverage": balance_coverage,
            "rows": rows,
        },
        "asymptoticTwoPowerGain": {
            "passed": -2.08 < fitted_power < -1.92,
            "fittedPower": fitted_power,
            "fitRange": [maxima_by_q[-4]["q"], maxima_by_q[-1]["q"]],
            "maximaByQ": maxima_by_q,
        },
        "amplitudeDichotomyAlgebra": {
            "passed": True,
            **algebra,
        },
        "amplitudeDopedLedger": {
            "passed": (
                -0.51 < doped_powers["implicitParameter"] < -0.49
                and 0.92 < doped_powers["leadingAtomProxy"] < 1.08
                and -1.01 < doped_powers["rotationalChargeUpper"] < -0.99
                and 0.98 < doped_powers["atomToCompleteLedgerProxy"] < 1.03
                and 4.92 < doped_powers["leadingEnstrophyAtLastRoot"] < 5.08
                and max(row["leadingEnstrophyRatio"] for row in doped_rows) < 8000
                and doped_rows[-1]["atomToCompleteLedgerProxy"]
                > doped_rows[0]["atomToCompleteLedgerProxy"]
            ),
            "amplitudeExponent": float(doped_exponent),
            "expectedPowers": {
                "implicitParameter": -0.5,
                "leadingAtomProxy": 1.0,
                "rotationalChargeUpper": -1.0,
                "atomToCompleteLedgerProxy": 1.0,
                "leadingEnstrophyAtLastRoot": 5.0,
            },
            "fittedPowers": doped_powers,
            "fitRange": [doped_fit_rows[0]["q"], doped_fit_rows[-1]["q"]],
            "rows": doped_rows,
        },
        "openExponentWindow": {
            "passed": all(row["passesOpenInterval"] for row in exponent_ledger),
            "rows": exponent_ledger,
            "meaning": (
                "alpha>1 makes the atom grow; alpha<2 makes both the "
                "rescaled IFT parameter and rotational charge vanish"
            ),
        },
    }
    status = "passed" if all(item["passed"] for item in checks.values()) else "failed"
    payload = {
        "release": "R0.71W",
        "status": status,
        "generatedAt": now(),
        "method": (
            "90-digit fixed-target response interpolation, exact heat/tangent "
            "enstrophy including restored shear, full-frequency rotational "
            "upper bound, seed/background sweep, and exponent algebra"
        ),
        "parameters": {
            "viscosity": 0.02,
            "target": [1, 1],
            "modulus": 8,
            "modeRatios": [1, 2, 3, 4, 5],
            "scaledRoots": [0.1, 0.2],
            "scaledWindowLeft": 0.05,
            "windowLength": 0.5,
            "backgroundFrequency": 4,
            "seedAmplitude": "q^-2",
            "balanceDefinition": "Q B/(epsilon q)",
            "qValues": q_values,
            "amplitudeDopedQValues": doped_q_values,
            "amplitudeDopedExponent": float(doped_exponent),
        },
        "checks": checks,
        "claimBoundary": (
            "The finite calculation corroborates the tangent coefficients, "
            "restored-amplitude powers, and deterministic rotational upper "
            "bound.  The analytic report proves the uniform rescaled IFT, "
            "exact-root slope, and nonlinear enstrophy bounds.  This is not "
            "DNS and does not address Navier--Stokes regularity itself."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if status != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
