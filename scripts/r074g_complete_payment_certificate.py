#!/usr/bin/env python3
"""Exact finite certificate for the R0.74G payment-closure gates.

This script checks rational identities, strict exponent margins, conditional
calibration arithmetic, bridge chart reserves, and scaling exponents.  It
does not certify heat-kernel, Brownian-bridge, Peetre, Riesz-transform,
Navier--Stokes, endpoint, or Clay statements.
"""

from __future__ import annotations

import json
from fractions import Fraction


def q(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def equality(check_id: str, left: Fraction, right: Fraction, note: str) -> dict:
    return {
        "id": check_id,
        "left": q(left),
        "relation": "==",
        "right": q(right),
        "margin": q(left - right),
        "pass": left == right,
        "note": note,
    }


def strict_less(check_id: str, left: Fraction, right: Fraction, note: str) -> dict:
    return {
        "id": check_id,
        "left": q(left),
        "relation": "<",
        "right": q(right),
        "margin": q(right - left),
        "pass": left < right,
        "note": note,
    }


def strict_greater(check_id: str, left: Fraction, right: Fraction, note: str) -> dict:
    return {
        "id": check_id,
        "left": q(left),
        "relation": ">",
        "right": q(right),
        "margin": q(left - right),
        "pass": left > right,
        "note": note,
    }


lam = Fraction(63, 32)
c_h = Fraction(15, 16)
alpha = Fraction(14, 15)
beta_sq = Fraction(31, 256)
c_r = Fraction(1, 320)
c_gamma = Fraction(8, 3969)

a_plateau = alpha * alpha / 260
d_energy = alpha * alpha / 262
main_gap = c_r - Fraction(3, 2) * c_gamma
shift_gap = a_plateau - c_r
energy_gap = d_energy - c_gamma

buffer_width = Fraction(16)
buffer_threshold = buffer_width / (c_h - alpha)
l_12 = lam * 2**12
l_13 = lam * 2**13

# Conditional large-j calibration arithmetic used in the analytic proof.
q_upper = Fraction(1, 4)
theta_lower = Fraction(3, 4)
calibration_length = Fraction(64)
denominator_lower = theta_lower * calibration_length
b_upper_scaled = (q_upper + Fraction(1, 2)) / denominator_lower
b_lower_scaled = Fraction(1, 2) / calibration_length
shift_upper = 2 * b_upper_scaled * 65
centre_left_reserve = Fraction(1, 2) + shift_upper

q_over_h_sq = beta_sq / (c_h * c_h)
near_s_sq_factor = Fraction(1) + 2**2
far_s_sq_factor = Fraction(1) + Fraction(1, 2) ** 2

checks = [
    equality(
        "radial_split",
        c_h * c_h + beta_sq,
        Fraction(1),
        "h squared plus q squared equals r squared",
    ),
    equality(
        "gamma_coefficient",
        c_gamma,
        Fraction(1, 1) / (128 * lam * lam),
        "frozen Gaussian annular-weight exponent",
    ),
    equality(
        "q_over_h_squared",
        q_over_h_sq,
        Fraction(31, 225),
        "exact squared longitudinal-to-transverse centre ratio",
    ),
    strict_less(
        "q_less_than_half_h",
        q_over_h_sq,
        Fraction(1, 4),
        "q/h is positive and strictly below one half",
    ),
    equality(
        "plateau_exponent",
        a_plateau,
        Fraction(49, 14625),
        "plateau heat-leakage exponent",
    ),
    equality(
        "buffered_energy_exponent",
        d_energy,
        Fraction(98, 29475),
        "squared transverse-energy exponent with denominator 262",
    ),
    strict_greater(
        "plateau_beats_inverse_R",
        a_plateau,
        c_r,
        "the one-sided shift is o(R)",
    ),
    equality(
        "plateau_shift_gap",
        shift_gap,
        Fraction(211, 936000),
        "exact positive exponent in delta/R",
    ),
    strict_greater(
        "buffered_energy_beats_gamma",
        d_energy,
        c_gamma,
        "packet energy remains below the shear energy after amplitude choice",
    ),
    equality(
        "buffered_energy_gap",
        energy_gap,
        Fraction(17018, 12998475),
        "exact energy-amplitude exponent margin",
    ),
    strict_greater(
        "inverse_R_beats_three_halves_gamma",
        c_r,
        Fraction(3, 2) * c_gamma,
        "packet cubic and harmonic rows remain below the shear floor",
    ),
    equality(
        "complete_payment_gap",
        main_gap,
        Fraction(43, 423360),
        "exact common G and H exponent margin",
    ),
    equality(
        "buffer_width_threshold",
        buffer_threshold,
        Fraction(3840),
        "continuous L threshold for h minus 16R to exceed alpha L R",
    ),
    strict_greater(
        "L12_above_buffer_threshold",
        l_12,
        buffer_threshold,
        "the inherited discrete scales clear the buffered-energy geometry",
    ),
    equality(
        "discrete_L12",
        l_12,
        Fraction(8064),
        "exact twelfth scale",
    ),
    equality(
        "discrete_L13",
        l_13,
        Fraction(16128),
        "exact thirteenth scale",
    ),
    equality(
        "conditional_calibration_denominator",
        denominator_lower,
        Fraction(48),
        "theta at least 3/4 over 64 small-time units gives 48",
    ),
    equality(
        "conditional_B_upper",
        b_upper_scaled,
        Fraction(1, 64),
        "q at most 1/4 and denominator at least 48 give BR squared at most 1/64",
    ),
    equality(
        "conditional_B_lower",
        b_lower_scaled,
        Fraction(1, 128),
        "numerator at least 1/2 and denominator at most 64 give BR squared at least 1/128",
    ),
    equality(
        "path_shift_upper",
        shift_upper,
        Fraction(65, 32),
        "two-sided theta range and conditional B upper bound",
    ),
    equality(
        "left_chart_reserve",
        centre_left_reserve,
        Fraction(81, 32),
        "Q at least minus one half plus maximal positive shift",
    ),
    strict_less(
        "left_chart_reserve_below_three",
        centre_left_reserve,
        Fraction(3),
        "the path centre stays above minus 3, hence above minus pi",
    ),
    equality(
        "bridge_heat_lower",
        Fraction(1) + Fraction(61),
        Fraction(62),
        "R squared initial heat age plus the I_2R lower time",
    ),
    equality(
        "bridge_heat_upper",
        Fraction(1) + Fraction(65),
        Fraction(66),
        "R squared initial heat age plus the I_2R upper time",
    ),
    equality(
        "energy_gaussian_denominator",
        Fraction(2) + 4 * Fraction(65),
        Fraction(262),
        "squared initial Gaussian age plus maximal heat spreading",
    ),
    equality(
        "near_case_s_squared_factor",
        near_s_sq_factor,
        Fraction(5),
        "Q at least minus 2h and q below h/2 imply s squared at most 5h squared",
    ),
    equality(
        "far_case_s_squared_factor",
        far_s_sq_factor,
        Fraction(5, 4),
        "Q below minus 2h implies s squared at most 5Q squared over 4",
    ),
    equality(
        "peetre_power_p2",
        3 * 2 + (1 - 2) + (1 - 2 * 2),
        Fraction(2),
        "R exponents after bridge Jensen for p=2",
    ),
    equality(
        "peetre_power_p3",
        3 * 3 + (1 - 3) + (1 - 2 * 3),
        Fraction(2),
        "R exponents after bridge Jensen for p=3",
    ),
    equality(
        "occupation_output_p2",
        Fraction(1) + Fraction(2),
        Fraction(3),
        "L-weight prefactor R times common R squared gives R cubed",
    ),
    equality(
        "occupation_output_p3",
        Fraction(4) + Fraction(2),
        Fraction(6),
        "W-weight prefactor R to the fourth times common R squared gives R to the sixth",
    ),
]

passed = sum(bool(item["pass"]) for item in checks)
payload = {
    "analytic_boundary": [
        "does not prove the large-j hypotheses q<=1/4 or theta(t,h)>=3/4",
        "does not prove the transverse-energy subsolution or heat-kernel bounds",
        "does not prove the local Riesz/Newton pressure identity",
        "does not prove the Brownian-bridge representation or pathwise displacement bounds",
        "does not prove the periodic Peetre inequality or weighted kernel moments",
        "does not prove the complete denominator theorem or either endpoint counterexample",
        "does not prove Navier-Stokes singularity, regularity, or the Clay problem",
    ],
    "checks": checks,
    "result": "PASS" if passed == len(checks) else "FAIL",
    "summary": {
        "passed": passed,
        "total": len(checks),
    },
}

print(json.dumps(payload, indent=2, sort_keys=True))
