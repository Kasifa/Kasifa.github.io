#!/usr/bin/env python3
"""Independent binary64 reconstruction of the R0.71W amplitude ledger.

This program does not import ``r071w_exact_audit`` and does not read its
output.  It rebuilds the response interpolation, heat enstrophy, restored
shear contribution, deterministic rotational bound, and complete-baseline
ratio with NumPy.  Log-sum-exp evaluation keeps the zero-background endpoint
check meaningful when the high modes have decayed below binary64 range.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import math
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np


def now() -> str:
    return datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="seconds")


def logsumexp(values: np.ndarray) -> float:
    maximum = float(np.max(values))
    return maximum + math.log(float(np.sum(np.exp(values - maximum))))


def fit_power(xs: np.ndarray, ys: np.ndarray) -> float:
    return float(np.polyfit(np.log(xs), np.log(ys), 1)[0])


def build_case(q_value: int, balance: float) -> dict[str, float]:
    nu = 0.02
    ky = 1
    kz = 1
    modulus = 8
    background_frequency = 4
    scaled_left = 0.05
    window_length = 0.5
    scaled_roots = np.asarray([0.1, 0.2], dtype=float)
    mode_ratios = np.arange(1.0, 6.0)
    epsilon = q_value**-2
    background = balance * epsilon * q_value / background_frequency
    modes = modulus * mode_ratios * q_value
    alpha = (ky - modes) ** 2 + kz**2
    beta = 2.0 * nu * modes * (modes - ky)
    mu = nu * (ky**2 + kz**2)
    roots = scaled_roots / q_value**2
    left = scaled_left / q_value**2
    right = left + window_length

    def phi(index: int, time_value: float) -> float:
        rate = beta[index]
        return math.exp(-mu * time_value) * (-math.expm1(-rate * time_value)) / rate

    evaluation = np.asarray(
        [[phi(column, root) for column in range(3)] for root in roots]
    )
    coefficients = np.concatenate(
        (np.asarray([1.0]), np.linalg.solve(evaluation[:, 1:], -evaluation[:, 0]))
    )

    def gamma(time_value: float) -> float:
        return float(
            kz
            * sum(
                coefficients[index] * phi(index, time_value)
                for index in range(3)
            )
        )

    def gamma_prime(time_value: float) -> float:
        total = 0.0
        for index in range(3):
            rate = beta[index]
            total += coefficients[index] * (
                -mu * math.exp(-mu * time_value) / rate
                + (mu + rate) * math.exp(-(mu + rate) * time_value) / rate
            )
        return float(kz * total)

    def log_enstrophy(time_value: float) -> float:
        seed_logs = (
            math.log(2.0 * epsilon**2)
            + np.log(alpha)
            - 2.0 * nu * alpha * time_value
        )
        terms = seed_logs
        if background > 0.0:
            background_log = (
                math.log(2.0 * background_frequency**2 * background**2)
                - 2.0 * nu * background_frequency**2 * time_value
            )
            terms = np.concatenate((seed_logs, np.asarray([background_log])))
        return logsumexp(terms)

    atom_coefficients = []
    for root in roots:
        atom_coefficients.append(
            2.0 * epsilon**2 * gamma_prime(float(root)) ** 2
            * math.exp(-log_enstrophy(float(root)))
        )
    atom_sum = float(sum(atom_coefficients))
    log_ry = log_enstrophy(left) - log_enstrophy(right)
    log_ratio = math.log(atom_sum) - log_ry - math.log(nu**2)
    return {
        "q": float(q_value),
        "balance": float(balance),
        "maximumRootResidual": float(max(abs(gamma(float(root))) for root in roots)),
        "minimumRootSlope": float(min(abs(gamma_prime(float(root))) for root in roots)),
        "log10RY": log_ry / math.log(10.0),
        "atomToRYNu2": float(math.exp(log_ratio)) if log_ratio > -740.0 else 0.0,
        "log10AtomToRYNu2": log_ratio / math.log(10.0),
        "q2AtomToRYNu2": float(math.exp(log_ratio + 2.0 * math.log(q_value)))
        if log_ratio + 2.0 * math.log(q_value) > -740.0
        else 0.0,
    }


def build_amplitude_case(q_value: int, exponent: float = 1.5) -> dict[str, float]:
    """Standalone binary64 version of the restored-amplitude proxy."""

    nu = 0.02
    ky = 1
    kz = 1
    modulus = 8
    background_frequency = 4
    scaled_left = 0.05
    window_length = 0.5
    scaled_roots = np.asarray([0.1, 0.2], dtype=float)
    mode_ratios = np.arange(1.0, 6.0)
    amplitude = float(q_value) ** exponent
    implicit_parameter = amplitude / float(q_value) ** 2
    background = amplitude * q_value / background_frequency
    modes = modulus * mode_ratios * q_value
    alpha = (ky - modes) ** 2 + kz**2
    beta = 2.0 * nu * modes * (modes - ky)
    mu = nu * (ky**2 + kz**2)
    roots = scaled_roots / q_value**2
    left = scaled_left / q_value**2
    right = left + window_length

    def phi(index: int, time_value: float) -> float:
        rate = beta[index]
        return math.exp(-mu * time_value) * (-math.expm1(-rate * time_value)) / rate

    evaluation = np.asarray(
        [[phi(column, float(root)) for column in range(3)] for root in roots]
    )
    coefficients = np.concatenate(
        (np.asarray([1.0]), np.linalg.solve(evaluation[:, 1:], -evaluation[:, 0]))
    )

    def gamma(time_value: float) -> float:
        return float(
            kz
            * sum(coefficients[index] * phi(index, time_value) for index in range(3))
        )

    def gamma_prime(time_value: float) -> float:
        total = 0.0
        for index in range(3):
            rate = beta[index]
            total += coefficients[index] * (
                -mu * math.exp(-mu * time_value) / rate
                + (mu + rate)
                * math.exp(-(mu + rate) * time_value)
                / rate
            )
        return float(kz * total)

    def background_enstrophy(time_value: float) -> float:
        return float(
            2.0
            * background_frequency**2
            * background**2
            * math.exp(-2.0 * nu * background_frequency**2 * time_value)
        )

    def seed_enstrophy(time_value: float) -> float:
        return float(
            2.0
            * amplitude**2
            * np.sum(alpha * np.exp(-2.0 * nu * alpha * time_value))
        )

    def shear_enstrophy(time_value: float) -> float:
        active_modes = modes[:3]
        return float(
            2.0
            * amplitude**2
            * np.sum(
                active_modes**2
                * coefficients**2
                * np.exp(-2.0 * nu * active_modes**2 * time_value)
            )
        )

    def leading_enstrophy(time_value: float) -> float:
        return (
            background_enstrophy(time_value)
            + seed_enstrophy(time_value)
            + shear_enstrophy(time_value)
        )

    slopes = np.asarray(
        [amplitude**2 * abs(gamma_prime(float(root))) for root in roots]
    )
    atom_proxy = float(
        sum(
            2.0 * slope**2 / leading_enstrophy(float(root))
            for slope, root in zip(slopes, roots, strict=True)
        )
    )
    enstrophy_ratio = leading_enstrophy(left) / leading_enstrophy(right)

    active_modes = modes[:3]
    integral_v_infinity_squared = 0.0
    for i in range(3):
        for j in range(3):
            integral_v_infinity_squared += (
                4.0
                * amplitude**2
                * abs(coefficients[i] * coefficients[j])
                / (nu * (active_modes[i] ** 2 + active_modes[j] ** 2))
            )
    scalar_z_energy_upper = 2.0 * kz**2 * amplitude**2 * len(modes)
    background_floor = background_enstrophy(right)
    rotational_upper = (
        integral_v_infinity_squared
        * scalar_z_energy_upper
        / background_floor
        / window_length
    )
    complete_ledger = enstrophy_ratio * (nu**2 + rotational_upper)
    root_residual = max(abs(gamma(float(root))) for root in roots)

    return {
        "q": float(q_value),
        "implicitParameter": implicit_parameter,
        "maximumTangentRootResidual": root_residual,
        "minimumPhysicalRootSlope": float(np.min(slopes)),
        "leadingAtomProxy": atom_proxy,
        "leadingEnstrophyAtLastRoot": leading_enstrophy(float(roots[-1])),
        "leadingEnstrophyRatio": enstrophy_ratio,
        "rotationalChargeUpper": rotational_upper,
        "completeLedgerProxy": complete_ledger,
        "atomToCompleteLedgerProxy": atom_proxy / complete_ledger,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    q_values = np.asarray([8, 16, 32, 64, 128, 256], dtype=float)
    balances = np.concatenate((np.asarray([0.0]), np.logspace(-8, 8, 65)))
    rows = [
        build_case(int(q_value), float(balance))
        for q_value in q_values
        for balance in balances
    ]
    maxima = []
    for q_value in q_values:
        candidates = [row for row in rows if row["q"] == q_value]
        maximizing = max(candidates, key=lambda row: row["atomToRYNu2"])
        maxima.append(
            {
                "q": int(q_value),
                "maximumAtomToRYNu2": maximizing["atomToRYNu2"],
                "maximizingBalance": maximizing["balance"],
                "q2MaximumAtomToRYNu2": maximizing["q2AtomToRYNu2"],
            }
        )

    fitted_power = fit_power(
        q_values[-4:],
        np.asarray([row["maximumAtomToRYNu2"] for row in maxima[-4:]]),
    )
    maximum_scaled = max(row["q2MaximumAtomToRYNu2"] for row in maxima)
    maximum_residual = max(row["maximumRootResidual"] for row in rows)
    minimum_slope = min(row["minimumRootSlope"] for row in rows)

    inequality_slack = []
    for exponent_a in range(-12, 13, 2):
        for exponent_b in range(-12, 13, 2):
            for delta in (0.0, 1e-12, 1e-6, 0.1, 1.0):
                a_value = 10.0**exponent_a
                b_value = 10.0**exponent_b
                left = a_value * (b_value + a_value * delta) / (a_value + b_value) ** 2
                right = 0.25 + delta
                inequality_slack.append(right - left)

    doped_q_values = np.asarray([2.0**power for power in range(8, 33, 2)])
    doped_rows = [build_amplitude_case(int(q_value)) for q_value in doped_q_values]
    doped_fit_rows = doped_rows[-4:]
    fit_x = np.asarray([row["q"] for row in doped_fit_rows])
    doped_powers = {
        key: fit_power(fit_x, np.asarray([row[key] for row in doped_fit_rows]))
        for key in (
            "implicitParameter",
            "leadingAtomProxy",
            "rotationalChargeUpper",
            "atomToCompleteLedgerProxy",
            "leadingEnstrophyAtLastRoot",
        )
    }

    checks = {
        "independentRootInterpolation": {
            "passed": maximum_residual < 2e-16 and minimum_slope > 0.1,
            "maximumResidual": maximum_residual,
            "minimumSlope": minimum_slope,
        },
        "independentBalanceEnvelope": {
            "passed": maximum_scaled < 0.1,
            "maximumQ2AtomToRYNu2": maximum_scaled,
            "maximaByQ": maxima,
            "fittedPower": fitted_power,
        },
        "zeroBackgroundStress": {
            "passed": all(
                row["log10RY"] > 100.0 and row["log10AtomToRYNu2"] < -100.0
                for row in rows
                if row["balance"] == 0.0 and row["q"] >= 32.0
            ),
            "rows": [row for row in rows if row["balance"] == 0.0],
        },
        "independentAlgebraGrid": {
            "passed": min(inequality_slack) >= -2e-15,
            "minimumSlack": min(inequality_slack),
            "testedTriples": len(inequality_slack),
        },
        "independentAmplitudeLedger": {
            "passed": (
                -0.51 < doped_powers["implicitParameter"] < -0.49
                and 0.98 < doped_powers["leadingAtomProxy"] < 1.02
                and -1.01 < doped_powers["rotationalChargeUpper"] < -0.99
                and 0.98 < doped_powers["atomToCompleteLedgerProxy"] < 1.03
                and 4.98 < doped_powers["leadingEnstrophyAtLastRoot"] < 5.02
                and max(row["leadingEnstrophyRatio"] for row in doped_rows) < 8000
                and max(row["maximumTangentRootResidual"] for row in doped_rows)
                < 5e-18
            ),
            "amplitudeExponent": 1.5,
            "fittedPowers": doped_powers,
            "fitRange": [doped_fit_rows[0]["q"], doped_fit_rows[-1]["q"]],
            "rows": doped_rows,
        },
    }
    status = "passed" if all(item["passed"] for item in checks.values()) else "failed"
    payload = {
        "release": "R0.71W",
        "status": status,
        "generatedAt": now(),
        "method": (
            "standalone binary64 response solve, log-sum-exp heat enstrophy, "
            "restored shear ledger, deterministic rotational upper bound, "
            "dense seed/background sweep, and algebra grid"
        ),
        "checks": checks,
        "claimBoundary": (
            "This independent finite reconstruction checks the q^-2 tangent "
            "envelope and the restored-amplitude complete-ledger powers.  It "
            "does not prove the uniform rescaled IFT or nonlinear PDE bounds."
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
