#!/usr/bin/env python3
"""High-precision algebra audit for the R0.71X one-third endpoint.

The analytic proof belongs in ``r071x_report-source.md`` once the working
draft is closed.  This program independently evaluates the limiting
Chebyshev interpolation, the fixed-small-coupling endpoint diagonal
``A_q = delta q^2``, the initial-data size, the prescribed atom sum, and the
complete first-row proxy.  It does not prove the continuum implicit-function
theorem, absence of extra roots, or Navier--Stokes regularity.

Only Python's standard library is used.  Decimal arithmetic makes the
interpolation and fitted powers reproducible without optional scientific
packages.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from decimal import Decimal, getcontext
import json
from pathlib import Path
from zoneinfo import ZoneInfo


getcontext().prec = 90

ZERO = Decimal(0)
ONE = Decimal(1)
TWO = Decimal(2)

NU = Decimal("0.02")
D_MODULUS = 8
K_Y = 1
K_Z = 1
BACKGROUND_FREQUENCY = 4
MODE_MULTIPLIERS = (1, 2, 3, 4, 5)
ROOTS = (Decimal("0.1"), Decimal("0.2"))
SCALED_LEFT = Decimal("0.05")
PHYSICAL_WINDOW = Decimal("1.0")
Q_VALUES = (32, 64, 128, 256, 512, 1024, 2048)
DELTAS = (
    Decimal(1) / Decimal(1024),
    Decimal(1) / Decimal(512),
    Decimal(1) / Decimal(256),
    Decimal(1) / Decimal(128),
    Decimal(1) / Decimal(64),
)
BETAS = (
    Decimal(0),
    Decimal("0.1"),
    Decimal("0.25"),
    Decimal(1) / Decimal(3),
    Decimal("0.4"),
    Decimal("0.5"),
)


def decimal_exp(value: Decimal) -> Decimal:
    return value.exp()


def decimal_power(value: Decimal, exponent: Decimal) -> Decimal:
    if value <= 0:
        raise ValueError("decimal_power requires a positive base")
    return (exponent * value.ln()).exp()


def as_text(value: Decimal) -> str:
    return format(value, ".50E")


def as_float(value: Decimal) -> float:
    return float(value)


def now() -> str:
    return datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="seconds")


def rate(multiplier: int) -> Decimal:
    return TWO * NU * Decimal(D_MODULUS**2 * multiplier**2)


def psi(multiplier: int, time: Decimal) -> Decimal:
    value = rate(multiplier)
    return (ONE - decimal_exp(-value * time)) / value


def limiting_coefficients() -> tuple[Decimal, Decimal, Decimal]:
    """Solve the two prescribed real-block interpolation equations."""

    a11 = psi(2, ROOTS[0])
    a12 = psi(3, ROOTS[0])
    a21 = psi(2, ROOTS[1])
    a22 = psi(3, ROOTS[1])
    b1 = -psi(1, ROOTS[0])
    b2 = -psi(1, ROOTS[1])
    determinant = a11 * a22 - a12 * a21
    if determinant == 0:
        raise ArithmeticError("singular limiting interpolation matrix")
    c2 = (b1 * a22 - a12 * b2) / determinant
    c3 = (a11 * b2 - b1 * a21) / determinant
    return (ONE, c2, c3)


COEFFICIENTS = limiting_coefficients()


def gamma(time: Decimal) -> Decimal:
    return sum(
        coefficient * psi(multiplier, time)
        for multiplier, coefficient in zip(
            MODE_MULTIPLIERS[:3], COEFFICIENTS, strict=True
        )
    )


def gamma_prime(time: Decimal) -> Decimal:
    return sum(
        coefficient * decimal_exp(-rate(multiplier) * time)
        for multiplier, coefficient in zip(
            MODE_MULTIPLIERS[:3], COEFFICIENTS, strict=True
        )
    )


def gamma_infinity() -> Decimal:
    return sum(
        coefficient / rate(multiplier)
        for multiplier, coefficient in zip(
            MODE_MULTIPLIERS[:3], COEFFICIENTS, strict=True
        )
    )


def heat_factor(wavenumber_squared: Decimal, time: Decimal) -> Decimal:
    return decimal_exp(-TWO * NU * wavenumber_squared * time)


def leading_enstrophy(
    q_value: int,
    amplitude: Decimal,
    time: Decimal,
) -> Decimal:
    q = Decimal(q_value)
    active = ZERO
    for multiplier in MODE_MULTIPLIERS:
        n_value = D_MODULUS * multiplier * q_value
        frequency_squared = Decimal((K_Y - n_value) ** 2 + K_Z**2)
        active += TWO * amplitude**2 * frequency_squared * heat_factor(
            frequency_squared, time
        )

    shear = ZERO
    for multiplier, coefficient in zip(
        MODE_MULTIPLIERS[:3], COEFFICIENTS, strict=True
    ):
        frequency_squared = Decimal((D_MODULUS * multiplier * q_value) ** 2)
        shear += (
            TWO
            * amplitude**2
            * coefficient**2
            * frequency_squared
            * heat_factor(frequency_squared, time)
        )

    background = amplitude * q / Decimal(BACKGROUND_FREQUENCY)
    background_frequency_squared = Decimal(BACKGROUND_FREQUENCY**2)
    background_part = (
        TWO
        * background_frequency_squared
        * background**2
        * heat_factor(background_frequency_squared, time)
    )
    return active + shear + background_part


def initial_data_size(q_value: int, amplitude: Decimal) -> Decimal:
    q = Decimal(q_value)
    active_energy = TWO * amplitude**2 * Decimal(len(MODE_MULTIPLIERS))
    active_enstrophy = ZERO
    for multiplier in MODE_MULTIPLIERS:
        n_value = D_MODULUS * multiplier * q_value
        active_enstrophy += TWO * amplitude**2 * Decimal(
            (K_Y - n_value) ** 2 + K_Z**2
        )

    shear_energy = TWO * amplitude**2 * sum(
        coefficient**2 for coefficient in COEFFICIENTS
    )
    shear_enstrophy = TWO * amplitude**2 * sum(
        Decimal((D_MODULUS * multiplier * q_value) ** 2) * coefficient**2
        for multiplier, coefficient in zip(
            MODE_MULTIPLIERS[:3], COEFFICIENTS, strict=True
        )
    )

    background = amplitude * q / Decimal(BACKGROUND_FREQUENCY)
    background_energy = TWO * background**2
    background_enstrophy = (
        TWO * Decimal(BACKGROUND_FREQUENCY**2) * background**2
    )
    return (
        active_energy
        + active_enstrophy
        + shear_energy
        + shear_enstrophy
        + background_energy
        + background_enstrophy
    )


def rotational_upper(q_value: int, amplitude: Decimal) -> Decimal:
    integral_v_infinity_squared = ZERO
    for left_multiplier, left_coefficient in zip(
        MODE_MULTIPLIERS[:3], COEFFICIENTS, strict=True
    ):
        left_frequency_squared = Decimal(
            (D_MODULUS * left_multiplier * q_value) ** 2
        )
        for right_multiplier, right_coefficient in zip(
            MODE_MULTIPLIERS[:3], COEFFICIENTS, strict=True
        ):
            right_frequency_squared = Decimal(
                (D_MODULUS * right_multiplier * q_value) ** 2
            )
            integral_v_infinity_squared += (
                Decimal(4)
                * amplitude**2
                * abs(left_coefficient * right_coefficient)
                / (NU * (left_frequency_squared + right_frequency_squared))
            )

    scalar_z_energy_upper = (
        TWO * Decimal(K_Z**2) * amplitude**2 * Decimal(len(MODE_MULTIPLIERS))
    )
    background = amplitude * Decimal(q_value) / Decimal(BACKGROUND_FREQUENCY)
    window_right = SCALED_LEFT / Decimal(q_value**2) + PHYSICAL_WINDOW
    background_floor = (
        TWO
        * Decimal(BACKGROUND_FREQUENCY**2)
        * background**2
        * heat_factor(Decimal(BACKGROUND_FREQUENCY**2), window_right)
    )
    return (
        integral_v_infinity_squared
        * scalar_z_energy_upper
        / background_floor
        / PHYSICAL_WINDOW
    )


def fit_power(xs: list[Decimal], ys: list[Decimal]) -> Decimal:
    log_x = [value.ln() for value in xs]
    log_y = [value.ln() for value in ys]
    count = Decimal(len(xs))
    mean_x = sum(log_x) / count
    mean_y = sum(log_y) / count
    numerator = sum(
        (x_value - mean_x) * (y_value - mean_y)
        for x_value, y_value in zip(log_x, log_y, strict=True)
    )
    denominator = sum((value - mean_x) ** 2 for value in log_x)
    return numerator / denominator


def endpoint_case(q_value: int, delta: Decimal) -> dict[str, Decimal]:
    q = Decimal(q_value)
    amplitude = delta * q**2
    data_size = initial_data_size(q_value, amplitude)
    atoms = ZERO
    for root in ROOTS:
        physical_time = root / q**2
        root_enstrophy = leading_enstrophy(q_value, amplitude, physical_time)
        physical_slope = amplitude**2 * abs(gamma_prime(root))
        atoms += TWO * physical_slope**2 / root_enstrophy

    left_time = SCALED_LEFT / q**2
    right_time = left_time + PHYSICAL_WINDOW
    enstrophy_ratio = leading_enstrophy(
        q_value, amplitude, left_time
    ) / leading_enstrophy(q_value, amplitude, right_time)
    rotational = rotational_upper(q_value, amplitude)
    ledger = enstrophy_ratio * (NU**2 + rotational)
    data_one_third = decimal_power(data_size, ONE / Decimal(3))
    return {
        "amplitude": amplitude,
        "dataSize": data_size,
        "atomSum": atoms,
        "rotationalUpper": rotational,
        "enstrophyRatioProxy": enstrophy_ratio,
        "ledgerProxy": ledger,
        "atomOverDataOneThird": atoms / data_one_third,
        "atomOverDataOneThirdLedger": atoms / (data_one_third * ledger),
    }


def check(name: str, passed: bool, value: object, requirement: str) -> dict[str, object]:
    return {
        "name": name,
        "passed": bool(passed),
        "value": value,
        "requirement": requirement,
    }


def audit() -> dict[str, object]:
    interpolation = {
        "coefficients": [as_text(value) for value in COEFFICIENTS],
        "rootResiduals": [as_text(gamma(root)) for root in ROOTS],
        "rootSlopes": [as_text(gamma_prime(root)) for root in ROOTS],
        "zeroRootSlope": as_text(gamma_prime(ZERO)),
        "tailLimit": as_text(gamma_infinity()),
        "ectBasisDimension": 4,
        "ectMaximumFiniteZerosCountingMultiplicity": 3,
        "forcedFiniteRoots": ["0", *[str(root) for root in ROOTS]],
        "meaning": (
            "The limiting exponential polynomial has exhausted its ECT zero "
            "budget at 0, tau_1, tau_2; nonzero slopes and tail coefficient "
            "are the finite algebra prerequisites for the analytic no-extra-root proof."
        ),
    }

    delta = Decimal(1) / Decimal(128)
    rows: list[dict[str, object]] = []
    raw_rows: list[dict[str, Decimal]] = []
    for q_value in Q_VALUES:
        values = endpoint_case(q_value, delta)
        raw_rows.append(values)
        rows.append(
            {
                "q": q_value,
                "delta": as_float(delta),
                **{key: as_float(value) for key, value in values.items()},
            }
        )

    q_decimals = [Decimal(value) for value in Q_VALUES]
    fitted_powers = {
        key: fit_power(q_decimals[-4:], [row[key] for row in raw_rows[-4:]])
        for key in (
            "dataSize",
            "atomSum",
            "rotationalUpper",
            "atomOverDataOneThird",
            "atomOverDataOneThirdLedger",
        )
    }

    delta_rows: list[dict[str, object]] = []
    q_for_delta = Q_VALUES[-1]
    delta_ratios: list[Decimal] = []
    for delta_value in DELTAS:
        values = endpoint_case(q_for_delta, delta_value)
        delta_ratios.append(values["atomOverDataOneThird"])
        delta_rows.append(
            {
                "q": q_for_delta,
                "delta": as_float(delta_value),
                "atomOverDataOneThird": as_float(
                    values["atomOverDataOneThird"]
                ),
                "atomOverDataOneThirdLedger": as_float(
                    values["atomOverDataOneThirdLedger"]
                ),
            }
        )
    delta_power = fit_power(list(DELTAS), delta_ratios)

    beta_rows: list[dict[str, object]] = []
    for beta in BETAS:
        values = [
            row["atomSum"]
            / (decimal_power(row["dataSize"], beta) * row["ledgerProxy"])
            for row in raw_rows
        ]
        fitted = fit_power(q_decimals[-4:], values[-4:])
        predicted = TWO - Decimal(6) * beta
        beta_rows.append(
            {
                "beta": as_float(beta),
                "fittedQPower": as_float(fitted),
                "predictedQPower": as_float(predicted),
                "difference": as_float(fitted - predicted),
                "classification": (
                    "diverges"
                    if beta < ONE / Decimal(3)
                    else "saturates"
                    if beta == ONE / Decimal(3)
                    else "vanishes"
                ),
            }
        )

    maximum_root_residual = max(abs(gamma(root)) for root in ROOTS)
    minimum_root_slope = min(abs(gamma_prime(root)) for root in ROOTS)
    checks = [
        check(
            "limiting root interpolation",
            maximum_root_residual < Decimal("1e-80"),
            as_text(maximum_root_residual),
            "maximum residual < 1e-80",
        ),
        check(
            "limiting roots are simple",
            minimum_root_slope > Decimal("0.1"),
            as_text(minimum_root_slope),
            "minimum absolute slope > 0.1",
        ),
        check(
            "limiting tail is nonzero",
            abs(gamma_infinity()) > Decimal("0.1"),
            as_text(gamma_infinity()),
            "absolute tail limit > 0.1",
        ),
        check(
            "initial-data endpoint power",
            abs(fitted_powers["dataSize"] - Decimal(6)) < Decimal("0.02"),
            as_float(fitted_powers["dataSize"]),
            "fitted q power within 0.02 of 6",
        ),
        check(
            "complete prescribed atom power",
            abs(fitted_powers["atomSum"] - TWO) < Decimal("0.02"),
            as_float(fitted_powers["atomSum"]),
            "fitted q power within 0.02 of 2",
        ),
        check(
            "rotational endpoint power",
            abs(fitted_powers["rotationalUpper"]) < Decimal("0.02"),
            as_float(fitted_powers["rotationalUpper"]),
            "fitted q power within 0.02 of 0",
        ),
        check(
            "one-third q saturation",
            abs(fitted_powers["atomOverDataOneThird"]) < Decimal("0.02"),
            as_float(fitted_powers["atomOverDataOneThird"]),
            "fitted q power within 0.02 of 0",
        ),
        check(
            "delta four-thirds collapse",
            abs(delta_power - Decimal(4) / Decimal(3)) < Decimal("0.002"),
            as_float(delta_power),
            "fitted delta power within 0.002 of 4/3",
        ),
        check(
            "beta trichotomy",
            max(abs(Decimal(str(row["difference"]))) for row in beta_rows)
            < Decimal("0.025"),
            max(abs(row["difference"]) for row in beta_rows),
            "every fitted q power is within 0.025 of 2-6 beta",
        ),
    ]
    passed = all(item["passed"] for item in checks)
    return {
        "schemaVersion": 1,
        "release": "R0.71X-working",
        "audit": "fixed-small-coupling one-third endpoint algebra",
        "generatedAt": now(),
        "status": "passed" if passed else "failed",
        "passed": passed,
        "method": (
            "90-digit Decimal interpolation, exact Fourier initial-data proxy, "
            "fixed-delta endpoint scaling, full-frequency deterministic rotational "
            "upper proxy, and log-power regression"
        ),
        "parameters": {
            "viscosity": as_float(NU),
            "d": D_MODULUS,
            "target": [K_Y, K_Z],
            "backgroundFrequency": BACKGROUND_FREQUENCY,
            "backgroundAmplitudeLaw": "B_q=A_q q/Q",
            "amplitudeLaw": "A_q=delta q^2",
            "modeMultipliers": list(MODE_MULTIPLIERS),
            "scaledRoots": [as_float(value) for value in ROOTS],
            "qValues": list(Q_VALUES),
            "fixedDelta": as_float(delta),
            "deltaSweep": [as_float(value) for value in DELTAS],
        },
        "limitingInterpolation": interpolation,
        "fixedDeltaRows": rows,
        "fittedQPowers": {
            key: as_float(value) for key, value in fitted_powers.items()
        },
        "deltaCollapse": {
            "rows": delta_rows,
            "fittedPower": as_float(delta_power),
            "predictedPower": 4.0 / 3.0,
        },
        "betaTrichotomy": beta_rows,
        "checks": checks,
        "claimBoundary": (
            "Finite high-precision algebra corroboration only. The analytic report "
            "must prove the half-line no-extra-root lemma, the continuum uniform IFT, "
            "and nonlinear enstrophy bounds. This audit proves no universal D^(1/3) "
            "estimate and no Navier-Stokes regularity statement."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
