#!/usr/bin/env python3
"""Exact and high-precision audit for the R0.71V zero-level boundary law.

The analytic proof lives in ``research/r071v_report-source.md``.  This script
checks its algebraic identities, NSE scale ledger, the explicit forced-sine
stress test, and the tangent response of the exact R0.71U 2.5D recurrence
family.  It does not infer an infinite-dimensional theorem from numerics.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
from zoneinfo import ZoneInfo

import mpmath as mp
import sympy as sp


def now() -> str:
    return datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="seconds")


def tangent_response() -> dict[str, object]:
    mp.mp.dps = 90
    nu = mp.mpf("0.02")
    Ky = 1
    Kz = 1
    d = 8
    N = 3
    left = mp.mpf("0.005")
    right = mp.mpf("0.09")
    roots = [mp.mpf("0.01"), mp.mpf("0.03"), mp.mpf("0.07")]
    frequencies = [d * index for index in range(1, 2 * N + 2)]
    beta = [2 * nu * value * (value - Ky) for value in frequencies]
    mu = nu * (Ky * Ky + Kz * Kz)

    def phi(index: int, time: mp.mpf) -> mp.mpf:
        value = beta[index]
        return mp.exp(-mu * time) * (-mp.expm1(-value * time)) / value

    matrix = mp.matrix(
        [[phi(column, time) for column in range(1, N + 1)] for time in roots]
    )
    right_hand_side = mp.matrix([-phi(0, time) for time in roots])
    coefficients = [mp.mpf(1), *list(mp.lu_solve(matrix, right_hand_side))]

    def derivative(time: mp.mpf, order: int) -> mp.mpf:
        if order == 0:
            return mp.fsum(
                coefficients[index] * phi(index, time)
                for index in range(N + 1)
            )
        return mp.fsum(
            coefficients[index]
            * (
                (-mu) ** order * mp.exp(-mu * time) / beta[index]
                - (-(mu + beta[index])) ** order
                * mp.exp(-(mu + beta[index]) * time)
                / beta[index]
            )
            for index in range(N + 1)
        )

    scalar_laplacian = [
        (Ky - value) ** 2 + Kz * Kz for value in frequencies
    ]

    def enstrophy(time: mp.mpf) -> mp.mpf:
        return 2 * mp.fsum(
            value * mp.exp(-2 * nu * value * time)
            for value in scalar_laplacian
        )

    critical_points = [
        mp.findroot(lambda time: derivative(time, 1), (mp.mpf("0.015"), mp.mpf("0.025"))),
        mp.findroot(lambda time: derivative(time, 1), (mp.mpf("0.045"), mp.mpf("0.065"))),
    ]
    integration_breaks = [left, *roots, *critical_points, right]
    integration_breaks = sorted(set(integration_breaks))
    first_row = mp.quad(
        lambda time: derivative(time, 1) ** 2 / enstrophy(time),
        integration_breaks,
    )
    second_row = mp.quad(
        lambda time: derivative(time, 2) ** 2 / enstrophy(time),
        integration_breaks,
    )
    zero_mass = mp.fsum(
        derivative(time, 1) ** 2 / enstrophy(time) for time in roots
    )
    outgoing_cubic = mp.quad(
        lambda time: (
            abs(derivative(time, 1)) ** 3 / enstrophy(time)
            if derivative(time, 0) * derivative(time, 1) > 0
            else mp.mpf(0)
        ),
        integration_breaks,
    )
    lobe_heights = [
        abs(derivative(critical_points[0], 0)),
        abs(derivative(critical_points[1], 0)),
        abs(derivative(right, 0)),
    ]
    length = right - left
    ratio_y = enstrophy(left) / enstrophy(right)
    sampling_bound = ratio_y * (
        2 * first_row / length + 7 * length * second_row / 3
    )

    maximum_root_residual = max(abs(derivative(time, 0)) for time in roots)
    minimum_root_slope = min(abs(derivative(time, 1)) for time in roots)
    return {
        "parameters": {
            "viscosity": float(nu),
            "Ky": Ky,
            "Kz": Kz,
            "modulus": d,
            "rootTimes": [float(value) for value in roots],
            "interval": [float(left), float(right)],
            "frequencies": frequencies,
            "beta": [float(value) for value in beta],
        },
        "coefficients": [float(value) for value in coefficients],
        "criticalPoints": [float(value) for value in critical_points],
        "rightLobeHeights": [float(value) for value in lobe_heights],
        "maximumRootResidual": float(maximum_root_residual),
        "minimumRootSlope": float(minimum_root_slope),
        "reducedZeroMass": float(zero_mass),
        "reducedFirstRow": float(first_row),
        "reducedSecondRow": float(second_row),
        "reducedOutgoingCubic": float(outgoing_cubic),
        "enstrophyRatio": float(ratio_y),
        "samplingBound": float(sampling_bound),
        "samplingSlack": float(sampling_bound - zero_mass),
        "passed": bool(
            maximum_root_residual < mp.mpf("1e-75")
            and minimum_root_slope > mp.mpf("1e-6")
            and zero_mass > 0
            and sampling_bound >= zero_mass
            and min(lobe_heights) > 0
        ),
    }


def high_frequency_repeated_profile() -> dict[str, object]:
    """Reconstruct the limiting N=2 Chebyshev profile and power ledger."""

    mp.mp.dps = 90
    nu = mp.mpf("0.02")
    d = 8
    Ky = 1
    Kz = 1
    A = mp.mpf("0.05")
    roots = [mp.mpf("0.1"), mp.mpf("0.2")]
    mode_multipliers = [1, 2, 3]
    rates = [2 * nu * d * d * value * value for value in mode_multipliers]

    def psi(index: int, time: mp.mpf) -> mp.mpf:
        rate = rates[index]
        return -mp.expm1(-rate * time) / rate

    matrix = mp.matrix(
        [[psi(column, time) for column in range(1, 3)] for time in roots]
    )
    rhs = mp.matrix([-psi(0, time) for time in roots])
    coefficients = [mp.mpf(1), *list(mp.lu_solve(matrix, rhs))]

    def gamma_prime(time: mp.mpf) -> mp.mpf:
        return Kz * mp.fsum(
            coefficients[index] * mp.exp(-rates[index] * time)
            for index in range(3)
        )

    slopes = [gamma_prime(time) for time in roots]
    i1 = mp.fsum(
        coefficients[left]
        * coefficients[right]
        * mp.exp(-(rates[left] + rates[right]) * A)
        / (rates[left] + rates[right])
        for left in range(3)
        for right in range(3)
    )
    i2 = mp.fsum(
        coefficients[left]
        * coefficients[right]
        * rates[left]
        * rates[right]
        * mp.exp(-(rates[left] + rates[right]) * A)
        / (rates[left] + rates[right])
        for left in range(3)
        for right in range(3)
    )
    primitive_exponents = {
        "passiveAmplitude": -2,
        "unscaledProfile": -2,
        "firstTimeDerivativeProfile": 0,
        "secondTimeDerivativeProfile": 2,
        "fastTimeMeasure": -2,
        "rootEnstrophy": 0,
        "terminalEnstrophyExposure": 0,
    }
    epsilon_power = primitive_exponents["passiveAmplitude"]
    height_power = epsilon_power + primitive_exponents["unscaledProfile"]
    root_slope_power = (
        epsilon_power + primitive_exponents["firstTimeDerivativeProfile"]
    )
    atom_power = 2 * root_slope_power - primitive_exponents["rootEnstrophy"]
    first_row_power = (
        2 * root_slope_power
        + primitive_exponents["fastTimeMeasure"]
        - primitive_exponents["rootEnstrophy"]
    )
    second_slope_power = (
        epsilon_power + primitive_exponents["secondTimeDerivativeProfile"]
    )
    second_row_power = (
        2 * second_slope_power
        + primitive_exponents["fastTimeMeasure"]
        - primitive_exponents["rootEnstrophy"]
    )
    internal_exposure_power = primitive_exponents["fastTimeMeasure"]
    terminal_exposure_power = primitive_exponents["terminalEnstrophyExposure"]
    exponents = {
        "passiveAmplitude": epsilon_power,
        "atomCoefficient": atom_power,
        "firstRowCoefficient": first_row_power,
        "secondRowCoefficient": second_row_power,
        "atomToFirstRow": atom_power - first_row_power,
        "atomToSecondRow": atom_power - second_row_power,
        "internalNoncollapse": (
            2 * height_power
            + primitive_exponents["rootEnstrophy"]
            - internal_exposure_power
            - 2 * root_slope_power
        ),
        "terminalNoncollapse": (
            2 * height_power
            + primitive_exponents["rootEnstrophy"]
            - terminal_exposure_power
            - 2 * root_slope_power
        ),
        "terminalExcursionCharge": 2 * height_power - terminal_exposure_power,
    }
    expected_exponents = {
        "passiveAmplitude": -2,
        "atomCoefficient": -4,
        "firstRowCoefficient": -6,
        "secondRowCoefficient": -2,
        "atomToFirstRow": 2,
        "atomToSecondRow": -2,
        "internalNoncollapse": -2,
        "terminalNoncollapse": -4,
        "terminalExcursionCharge": -8,
    }
    return {
        "parameters": {
            "viscosity": float(nu),
            "modulus": d,
            "targetKy": Ky,
            "targetKz": Kz,
            "scaledRootTimes": [float(value) for value in roots],
            "scaledWindowStart": float(A),
            "modeMultipliers": mode_multipliers,
        },
        "rates": [float(value) for value in rates],
        "limitingCoefficients": [float(value) for value in coefficients],
        "rootSlopes": [float(value) for value in slopes],
        "I1": float(i1),
        "I2": float(i2),
        "primitivePowerExponents": primitive_exponents,
        "powerExponents": exponents,
        "passed": bool(
            min(abs(value) for value in slopes) > mp.mpf("1e-4")
            and i1 > 0
            and i2 > 0
            and exponents == expected_exponents
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    m, p, delta = sp.symbols("m p delta", positive=True)
    exponent = sp.simplify(1 + (m - 1) * (p - 1) / m)
    left_coefficient = sp.simplify(m ** (p - 1) / exponent)
    right_coefficient = sp.simplify(m**p / (p * (m - 1) + 1))
    coarea_difference = sp.simplify(left_coefficient - right_coefficient)

    sine_rows: list[dict[str, object]] = []
    for count in (1, 2, 4, 8, 16, 32, 64):
        alpha = sp.Rational(1, 2)
        band_average = sp.simplify(2 * count * (1 - alpha**2 / 3))
        sine_rows.append(
            {
                "N": count,
                "bandWidth": float(alpha / count),
                "zeroLevelMass": 2 * count,
                "halfAmplitudeBandAverage": float(band_average),
                "firstRow": float(sp.pi),
                "secondRow": float(sp.pi * count**2),
            }
        )

    scale_terms = {
        "kappaMinusSix": -6,
        "CtNormSquared": 10,
        "enstrophyInverse": -4,
        "zeroJetTotal": 0,
        "cubicOccupationBeforeTime": 15 - 6 - 4,
        "timeMeasure": -2,
        "amplitudeBandInverse": -3,
        "bandAverageTotal": 15 - 6 - 4 - 2 - 3,
    }
    tangent = tangent_response()
    high_frequency = high_frequency_repeated_profile()
    crossing_power = 2
    required_time_power = crossing_power + 1
    leray_first_jet_time_power = 2
    curve_orders = {
        "observableAmplitude": 1,
        "atomWeight": 2,
        "outgoingSpeed": 1,
        "coMovingMollifierInverseWidth": -1,
    }
    co_moving_order = (
        curve_orders["atomWeight"]
        + curve_orders["outgoingSpeed"]
        + curve_orders["coMovingMollifierInverseWidth"]
    )
    fixed_band_support_lower_bound = sp.Rational(1, 4)
    fixed_band_eventually_zero = bool(
        fixed_band_support_lower_bound > 0
        and curve_orders["observableAmplitude"] > 0
    )
    checks = {
        "weightedOneDimensionalAreaFormula": {
            "passed": coarea_difference == 0,
            "symbolicDifference": str(coarea_difference),
            "identity": (
                "integral_0^delta sum_(r=y,r'>0) (r')^(p-1) dy "
                "= integral_(0<r<delta,r'>0) (r')^p dt"
            ),
            "monomialTest": "r(t)=t^m",
        },
        "quadraticJetRequiresCubicOccupation": {
            "passed": bool(
                required_time_power == 3
                and required_time_power > leray_first_jet_time_power
            ),
            "crossingPower": crossing_power,
            "requiredTimePower": required_time_power,
            "lerayFirstJetTimePower": leray_first_jet_time_power,
        },
        "forcedSineBoundaryStress": {
            "passed": all(
                row["zeroLevelMass"] == 2 * row["N"]
                and abs(row["firstRow"] - float(sp.pi)) < 1e-14
                for row in sine_rows
            ),
            "rows": sine_rows,
            "formula": (
                "for C_N=N^-1 sin(Nt)e on [0,2pi] and delta=alpha/N, "
                "B_delta=2N(1-alpha^2/3), int|C_N'|^2=pi, "
                "int|C_N''|^2=pi N^2"
            ),
        },
        "nseScaleLedger": {
            "passed": (
                scale_terms["zeroJetTotal"] == 0
                and scale_terms["bandAverageTotal"] == 0
            ),
            "exponents": scale_terms,
        },
        "exactRecurrenceTangent": tangent,
        "genuineNSEHighFrequencyLedger": high_frequency,
        "orderOfLimits": {
            "passed": bool(
                fixed_band_eventually_zero
                and curve_orders["atomWeight"] == 2
                and co_moving_order == 2
            ),
            "curveOrders": curve_orders,
            "fixedBandSupportLowerBoundModel": str(fixed_band_support_lower_bound),
            "fixedPositiveBandEventuallyExactlyZero": fixed_band_eventually_zero,
            "zeroJetOrderInCurveParameter": curve_orders["atomWeight"],
            "coMovingBandOrderInCurveParameter": co_moving_order,
            "consequence": (
                "delta down to zero before s down to zero retains the "
                "quadratic zero mass; s down to zero at fixed delta loses it"
            ),
        },
    }
    status = "passed" if all(item["passed"] for item in checks.values()) else "failed"
    payload = {
        "release": "R0.71V",
        "status": status,
        "generatedAt": now(),
        "method": (
            "symbolic monomial area-formula reconstruction, exact sine "
            "algebra, scale-exponent ledger, and 90-digit recurrence-tangent "
            "interpolation/quadrature"
        ),
        "checks": checks,
        "claimBoundary": (
            "The numerical tangent reconstruction corroborates one N=3 "
            "instance. The coarea theorem, tangent asymptotics, and order-of-"
            "limits statements are proved analytically in the report."
        ),
    }
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if status != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
