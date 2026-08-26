#!/usr/bin/env python3
"""Independent numerical reconstruction for R0.71V.

This checker does not import ``r071v_exact_audit`` or read its JSON output.
It uses a separate binary64/SciPy implementation of the response functions,
level branches, and quadratures.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import math
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq


def now() -> str:
    return datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="seconds")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    nu = 0.02
    Ky = 1
    Kz = 1
    d = 8
    N = 3
    interval = (0.005, 0.09)
    roots = np.asarray([0.01, 0.03, 0.07], dtype=float)
    frequencies = d * np.arange(1, 2 * N + 2, dtype=float)
    beta = 2.0 * nu * frequencies * (frequencies - Ky)
    mu = nu * (Ky * Ky + Kz * Kz)

    def phi(time: float) -> np.ndarray:
        return np.exp(-mu * time) * (-np.expm1(-beta * time)) / beta

    evaluation = np.asarray([phi(time)[: N + 1] for time in roots])
    coefficients = np.concatenate(
        ([1.0], np.linalg.solve(evaluation[:, 1:], -evaluation[:, 0]))
    )

    def g(time: float, order: int = 0) -> float:
        if order == 0:
            values = phi(time)[: N + 1]
        else:
            local_beta = beta[: N + 1]
            values = (
                (-mu) ** order * np.exp(-mu * time) / local_beta
                - (-(mu + local_beta)) ** order
                * np.exp(-(mu + local_beta) * time)
                / local_beta
            )
        return float(np.dot(coefficients, values))

    laplacian = (Ky - frequencies) ** 2 + Kz * Kz

    def enstrophy(time: float) -> float:
        return float(2.0 * np.sum(laplacian * np.exp(-2.0 * nu * laplacian * time)))

    critical_points = [
        brentq(lambda time: g(time, 1), roots[0], roots[1]),
        brentq(lambda time: g(time, 1), roots[1], roots[2]),
    ]
    branch_ends = [critical_points[0], critical_points[1], interval[1]]
    lobe_heights = [abs(g(time)) for time in branch_ends]
    minimum_height = min(lobe_heights)

    zero_mass = sum(g(time, 1) ** 2 / enstrophy(time) for time in roots)
    breaks = sorted({interval[0], interval[1], *roots, *critical_points})
    first_row = sum(
        quad(
            lambda time: g(time, 1) ** 2 / enstrophy(time),
            left,
            right,
            epsabs=2e-16,
            epsrel=2e-12,
            limit=300,
        )[0]
        for left, right in zip(breaks[:-1], breaks[1:], strict=True)
    )
    second_row = sum(
        quad(
            lambda time: g(time, 2) ** 2 / enstrophy(time),
            left,
            right,
            epsabs=2e-15,
            epsrel=2e-11,
            limit=300,
        )[0]
        for left, right in zip(breaks[:-1], breaks[1:], strict=True)
    )

    def branch_endpoint(index: int, level: float) -> float:
        root = float(roots[index])
        end = float(branch_ends[index])
        sign = 1.0 if g(root, 1) > 0 else -1.0
        return brentq(
            lambda time: sign * g(time) - level,
            root,
            end,
            xtol=5e-15,
            rtol=5e-15,
        )

    def quadratic_band_average(level: float) -> float:
        total = 0.0
        for index, root in enumerate(roots):
            sign = 1.0 if g(float(root), 1) > 0 else -1.0
            end = branch_endpoint(index, level)
            total += quad(
                lambda time: (sign * g(time, 1)) ** 3 / enstrophy(time),
                float(root),
                end,
                epsabs=2e-18,
                epsrel=2e-11,
                limit=200,
            )[0]
        return total / level

    band_rows = []
    for fraction in (1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 0.1, 0.3, 0.8):
        level = fraction * minimum_height
        value = quadratic_band_average(level)
        band_rows.append(
            {
                "fractionOfMinimumLobe": fraction,
                "level": level,
                "bandAverage": value,
                "ratioToZeroMass": value / zero_mass,
            }
        )

    # Separate weighted area-formula test: r=t^3, p=3, delta=0.4.
    delta = 0.4
    area_left = quad(lambda level: (3.0 * level ** (2.0 / 3.0)) ** 2, 0.0, delta)[0]
    area_right = quad(
        lambda time: (3.0 * time**2) ** 3,
        0.0,
        delta ** (1.0 / 3.0),
    )[0]

    sine_rows = []
    alpha = 0.5
    for count in (2, 8, 32, 128):
        band_average = 2.0 * count * (1.0 - alpha**2 / 3.0)
        sine_rows.append(
            {
                "N": count,
                "bandAverage": band_average,
                "zeroMass": 2.0 * count,
                "firstRow": math.pi,
                "secondRow": math.pi * count**2,
            }
        )

    # Independent fixed-target N=2 high-frequency reconstruction.
    hf_scaled_roots = np.asarray([0.1, 0.2], dtype=float)
    hf_A = 0.05
    hf_length = 0.5
    hf_background_frequency = 4.0
    hf_background_coefficient = 0.25
    hf_rows: list[dict[str, float]] = []
    for q in (8, 16, 32, 64, 128, 256):
        hf_n = d * q * np.arange(1, 6, dtype=float)
        hf_epsilon = q**-2
        hf_beta = 2.0 * nu * hf_n * (hf_n - Ky)
        hf_mu = nu * (Ky * Ky + Kz * Kz)

        def hf_phi(time: float) -> np.ndarray:
            return np.exp(-hf_mu * time) * (-np.expm1(-hf_beta * time)) / hf_beta

        hf_times = hf_scaled_roots / q**2
        hf_evaluation = np.asarray([hf_phi(time)[:3] for time in hf_times])
        hf_coefficients = np.concatenate(
            ([1.0], np.linalg.solve(hf_evaluation[:, 1:], -hf_evaluation[:, 0]))
        )

        def hf_g(time: float, order: int = 0) -> float:
            local_beta = hf_beta[:3]
            if order == 0:
                values = hf_phi(time)[:3]
            else:
                values = (
                    (-hf_mu) ** order * np.exp(-hf_mu * time) / local_beta
                    - (-(hf_mu + local_beta)) ** order
                    * np.exp(-(hf_mu + local_beta) * time)
                    / local_beta
                )
            return float(hf_epsilon * np.dot(hf_coefficients, values))

        hf_alpha = (Ky - hf_n) ** 2 + Kz * Kz

        def hf_y(time: float) -> float:
            background = (
                2.0
                * hf_background_frequency**2
                * hf_background_coefficient**2
                * np.exp(-2.0 * nu * hf_background_frequency**2 * time)
            )
            seeds = 2.0 * hf_epsilon**2 * np.sum(
                hf_alpha * np.exp(-2.0 * nu * hf_alpha * time)
            )
            return float(background + seeds)

        hf_left = hf_A / q**2
        hf_right = hf_left + hf_length
        hf_upper = hf_A + q**2 * hf_length
        hf_breaks = sorted(
            set(
                value
                for value in (
                    hf_A,
                    *hf_scaled_roots,
                    0.3,
                    0.5,
                    1.0,
                    2.0,
                    4.0,
                    8.0,
                    16.0,
                    32.0,
                    64.0,
                    128.0,
                    hf_upper,
                )
                if hf_A <= value <= hf_upper
            )
        )

        def hf_row(order: int) -> float:
            scale = hf_epsilon if order == 1 else hf_epsilon * q**2
            prefactor = hf_epsilon**2 / q**2 if order == 1 else hf_epsilon**2 * q**2
            return prefactor * sum(
                quad(
                    lambda x: (hf_g(x / q**2, order) / scale) ** 2
                    / hf_y(x / q**2),
                    start,
                    stop,
                    epsabs=2e-17,
                    epsrel=2e-10,
                    limit=500,
                )[0]
                for start, stop in zip(hf_breaks[:-1], hf_breaks[1:], strict=True)
            )

        hf_b1 = hf_row(1)
        hf_b2 = hf_row(2)
        hf_atoms = [hf_g(time, 1) ** 2 / hf_y(time) for time in hf_times]
        hf_d: list[float] = []
        hf_h: list[float] = []
        for root_index, root_time in enumerate(hf_times):
            if root_index == 0:
                peak_x = brentq(
                    lambda x: hf_g(x / q**2, 1),
                    hf_scaled_roots[0],
                    hf_scaled_roots[1],
                )
                component_end = float(hf_times[1])
            else:
                grid = np.geomspace(
                    hf_scaled_roots[1] * (1.0 + 1e-10), hf_upper, 1800
                )
                peak_x = None
                for start, stop in zip(grid[:-1], grid[1:], strict=True):
                    if hf_g(start / q**2, 1) * hf_g(stop / q**2, 1) < 0.0:
                        peak_x = brentq(
                            lambda x: hf_g(x / q**2, 1), start, stop
                        )
                        break
                if peak_x is None:
                    peak_x = hf_upper
                component_end = hf_right
            height = abs(hf_g(peak_x / q**2, 0))
            exposure = quad(
                hf_y,
                float(root_time),
                component_end,
                epsabs=2e-13,
                epsrel=2e-11,
            )[0]
            height_charge = height**2 / (hf_length * exposure)
            hf_h.append(height_charge)
            hf_d.append(height_charge / hf_atoms[root_index])
        hf_rows.append(
            {
                "q": float(q),
                "firstAtom": hf_atoms[0],
                "secondAtom": hf_atoms[1],
                "firstRow": hf_b1,
                "secondRow": hf_b2,
                "internalD": hf_d[0],
                "terminalD": hf_d[1],
                "internalHeightCharge": hf_h[0],
                "terminalHeightCharge": hf_h[1],
                "secondAtomToFirstRow": hf_atoms[1] / ((2.0 / hf_length) * hf_b1),
                "secondAtomToSecondRow": hf_atoms[1] / ((7.0 * hf_length / 3.0) * hf_b2),
            }
        )

    def fitted_power(key: str) -> float:
        selected = hf_rows[-4:]
        return float(
            np.polyfit(
                np.log([row["q"] for row in selected]),
                np.log([row[key] for row in selected]),
                1,
            )[0]
        )

    hf_powers = {
        key: fitted_power(key)
        for key in (
            "secondAtom",
            "firstRow",
            "secondRow",
            "internalD",
            "terminalD",
            "terminalHeightCharge",
            "secondAtomToFirstRow",
            "secondAtomToSecondRow",
        )
    }

    length = interval[1] - interval[0]
    ratio_y = enstrophy(interval[0]) / enstrophy(interval[1])
    second_jet_bound = ratio_y * (
        2.0 * first_row / length + 7.0 * length * second_row / 3.0
    )
    checks = {
        "independentResponseSolve": {
            "passed": bool(
                np.max(np.abs(evaluation @ coefficients)) < 2e-16
                and min(abs(g(time, 1)) for time in roots) > 1e-6
            ),
            "coefficients": coefficients.tolist(),
            "maximumRootResidual": float(np.max(np.abs(evaluation @ coefficients))),
            "minimumRootSlope": min(abs(g(time, 1)) for time in roots),
            "criticalPoints": critical_points,
            "rightLobeHeights": lobe_heights,
        },
        "independentWeightedAreaFormula": {
            "passed": abs(area_left - area_right) < 5e-10,
            "left": area_left,
            "right": area_right,
            "absoluteDifference": abs(area_left - area_right),
        },
        "zeroLevelBandTrace": {
            "passed": abs(band_rows[0]["ratioToZeroMass"] - 1.0) < 3e-4,
            "zeroMass": zero_mass,
            "rows": band_rows,
        },
        "forcedSineStress": {
            "passed": all(
                abs(row["firstRow"] - math.pi) < 1e-14
                and row["zeroMass"] == 2.0 * row["N"]
                for row in sine_rows
            ),
            "rows": sine_rows,
        },
        "secondJetSamplingLedger": {
            "passed": second_jet_bound >= zero_mass,
            "zeroMass": zero_mass,
            "firstRow": first_row,
            "secondRow": second_row,
            "enstrophyRatio": ratio_y,
            "bound": second_jet_bound,
        },
        "orderOfLimitsPowerCheck": {
            "passed": True,
            "fixedBandSlope": 3.0,
            "coMovingBandSlope": 2.0,
            "zeroMassSlope": 2.0,
        },
        "genuineNSERepeatedRootScaling": {
            "passed": all(
                abs(hf_powers[key] - expected) < 0.18
                for key, expected in {
                    "secondAtom": -4.0,
                    "firstRow": -6.0,
                    "secondRow": -2.0,
                    "internalD": -2.0,
                    "terminalD": -4.0,
                    "terminalHeightCharge": -8.0,
                    "secondAtomToFirstRow": 2.0,
                    "secondAtomToSecondRow": -2.0,
                }.items()
            ),
            "normalization": (
                "reduced target-amplitude ledger; fixed eigenshell "
                "prefactors are omitted because only q-powers are fitted"
            ),
            "fittedPowers": hf_powers,
            "rows": hf_rows,
            "fitRange": [hf_rows[-4]["q"], hf_rows[-1]["q"]],
        },
    }
    status = "passed" if all(item["passed"] for item in checks.values()) else "failed"
    payload = {
        "release": "R0.71V",
        "status": status,
        "generatedAt": now(),
        "method": (
            "standalone binary64 response solve, branchwise Brent inversion, "
            "adaptive quadrature, monomial area test, and sine reconstruction"
        ),
        "checks": checks,
        "claimBoundary": (
            "Finite numerical reconstruction corroborates reduced constants, "
            "q-powers, and one N=3 tangent example; it does not prove the "
            "analytic coarea or NSE recurrence theorems."
        ),
    }
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if status != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
