#!/usr/bin/env python3
"""Exact finite exponent certificate for R0.74I.

The script uses ``fractions.Fraction`` only.  It checks the finite scaling,
threshold-exponent, logarithmic-window, lacunarity, and hypothetical-endpoint
algebra recorded in R0.74I.  It does not certify any analytic Navier--Stokes
argument; the complete boundary is serialized with the checks.
"""

from __future__ import annotations

import json
from fractions import Fraction


def q(value: Fraction) -> str:
    """Return a canonical rational string, including denominator one."""

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


one = Fraction(1)
two = Fraction(2)
half = Fraction(1, 2)
two_thirds = Fraction(2, 3)
three_halves = Fraction(3, 2)

# Navier--Stokes scaling U(s,xi)=r*u(t0+r^2*s,x0+r*xi).
rescaled_velocity_power = one
velocity_cubic_power = 3 * rescaled_velocity_power
inverse_space_jacobian_power = Fraction(-3)
inverse_time_jacobian_power = Fraction(-2)
scaled_l3_power = (
    velocity_cubic_power
    + inverse_space_jacobian_power
    + inverse_time_jacobian_power
)
physical_velocity_cubic_power = Fraction(-3)
physical_space_jacobian_power = Fraction(3)
physical_time_jacobian_power = Fraction(2)
physical_l3_integral_power = (
    physical_velocity_cubic_power
    + physical_space_jacobian_power
    + physical_time_jacobian_power
)
normalized_physical_l3_power = Fraction(-2) + physical_l3_integral_power

# Fixed factors when r=R/2.
half_radius_time_factor = half**2
half_radius_normalization_factor = half ** Fraction(-2)

# E^(3/2) <= P and the epsilon-threshold exponent chain.
energy_recovery_power = three_halves * two_thirds
tube_threshold_recovery_power = three_halves * two_thirds
combined_l3_to_payment_power = two_thirds * three_halves

# Exact R0.74I logarithmic-window constants.
rho = Fraction(1, 320)
two_rho = 2 * rho
three_rho = 3 * rho
window_width = three_rho - two_rho
l_prefactor = Fraction(63, 32)
next_l_prefactor = 2 * l_prefactor
l_square_ratio = two**2
next_lower_log_exponent = 2 * rho * l_square_ratio
lacunarity_log_exponent = next_lower_log_exponent - 3 * rho

# The upper payment scale (B^3 R^3)^(2/3).
payment_b_power = Fraction(3)
payment_r_power = Fraction(3)
payment_l_power = Fraction(0)
payment_23_b_power = payment_b_power * two_thirds
payment_23_r_power = payment_r_power * two_thirds
payment_23_l_power = payment_l_power * two_thirds
sqrt_log_l_power = Fraction(2) * half
frontier_l_power = payment_23_l_power + sqrt_log_l_power

# For gamma=1/2-delta, the gap 1/2-gamma equals delta.  The two
# coefficient rows below verify this affine identity over Q[delta].
gap_constant_coefficient = half - half
gap_delta_coefficient = Fraction(0) - Fraction(-1)

# Algebra forced by a hypothetical endpoint upper bound:
# B^2 L R^2 <= C K L P^(2/3).
endpoint_l_after_cancellation = one - one
endpoint_inverse_outer_power = one / two_thirds
endpoint_payment_power = two_thirds * endpoint_inverse_outer_power
endpoint_b_power = Fraction(2) * endpoint_inverse_outer_power
endpoint_r_power = Fraction(2) * endpoint_inverse_outer_power
endpoint_k_power = Fraction(-1) * endpoint_inverse_outer_power

b_lower = Fraction(1, 256)
b_limit = Fraction(1, 128)
b_upper = Fraction(1, 64)

checks = [
    equality(
        "ns_rescaled_velocity_cubic_power",
        velocity_cubic_power,
        Fraction(3),
        "U=r*u contributes r^3 to |U|^3",
    ),
    equality(
        "ns_inverse_space_jacobian_power",
        inverse_space_jacobian_power,
        Fraction(-3),
        "xi=(x-x0)/r gives dxi=r^-3 dx",
    ),
    equality(
        "ns_inverse_time_jacobian_power",
        inverse_time_jacobian_power,
        Fraction(-2),
        "s=(t-t0)/r^2 gives ds=r^-2 dt",
    ),
    equality(
        "ns_scaled_l3_total_power",
        scaled_l3_power,
        Fraction(-2),
        "the transformed unit-cylinder integral equals r^-2 times the physical integral",
    ),
    equality(
        "ns_physical_l3_integral_power",
        physical_l3_integral_power,
        Fraction(2),
        "u=r^-1 U, dx=r^3 dxi, and dt=r^2 ds give physical L3 power r^2",
    ),
    equality(
        "ns_normalized_l3_scale_invariance",
        normalized_physical_l3_power,
        Fraction(0),
        "r^-2 times the physical L3 integral is scale invariant",
    ),
    equality(
        "half_radius_time_length_factor",
        half_radius_time_factor,
        Fraction(1, 4),
        "the interval I_(R/2) has length R^2/4",
    ),
    equality(
        "half_radius_normalization_factor",
        half_radius_normalization_factor,
        Fraction(4),
        "(R/2)^-2 equals 4 R^-2",
    ),
    equality(
        "half_radius_fixed_factor_product",
        half_radius_time_factor * half_radius_normalization_factor,
        one,
        "the exact time-length and normalization factors multiply to one",
    ),
    equality(
        "energy_from_payment_inverse_power",
        energy_recovery_power,
        one,
        "raising E^(3/2)<=P to the power 2/3 recovers E<=P^(2/3)",
    ),
    equality(
        "tube_to_payment_threshold_power",
        tube_threshold_recovery_power,
        one,
        "P<=epsilon_tube^(3/2) implies P^(2/3)<=epsilon_tube at the exponent level",
    ),
    equality(
        "l3_to_payment_threshold_chain",
        combined_l3_to_payment_power,
        one,
        "an L3 threshold exponent 2/3 followed by the payment exponent 3/2 is linear",
    ),
    equality(
        "rho_exact_value",
        rho,
        Fraction(1, 320),
        "the frozen packet family uses rho=1/320",
    ),
    equality(
        "two_rho",
        two_rho,
        Fraction(1, 160),
        "the lower logarithmic-window coefficient is 2 rho",
    ),
    equality(
        "three_rho",
        three_rho,
        Fraction(3, 320),
        "the upper logarithmic-window coefficient is 3 rho",
    ),
    equality(
        "log_window_width",
        window_width,
        Fraction(1, 320),
        "3 rho minus 2 rho equals rho",
    ),
    equality(
        "next_L_prefactor",
        next_l_prefactor,
        Fraction(63, 16),
        "L_(j+1)=2 L_j doubles the exact prefactor 63/32",
    ),
    equality(
        "L_square_ratio",
        l_square_ratio,
        Fraction(4),
        "L_(j+1)^2=4 L_j^2",
    ),
    equality(
        "next_lower_log_exponent",
        next_lower_log_exponent,
        Fraction(1, 40),
        "2 rho L_(j+1)^2 contributes 8 rho L_j^2",
    ),
    equality(
        "lacunarity_log_exponent",
        lacunarity_log_exponent,
        Fraction(1, 64),
        "8 rho minus 3 rho equals 5 rho=1/64",
    ),
    equality(
        "payment_upper_23_B_power",
        payment_23_b_power,
        Fraction(2),
        "(B^3 R^3)^(2/3) recovers B^2",
    ),
    equality(
        "payment_upper_23_R_power",
        payment_23_r_power,
        Fraction(2),
        "(B^3 R^3)^(2/3) recovers R^2",
    ),
    equality(
        "payment_upper_23_L_power",
        payment_23_l_power,
        Fraction(0),
        "the frozen payment upper scale has no L power before the logarithmic factor",
    ),
    equality(
        "sqrt_log_recovers_L_power",
        sqrt_log_l_power,
        one,
        "sqrt of a logarithmic window proportional to L^2 contributes L^1",
    ),
    equality(
        "frontier_total_L_power",
        frontier_l_power,
        one,
        "P^(2/3) sqrt(log P) has the target L power",
    ),
    equality(
        "subcritical_gap_constant_coefficient",
        gap_constant_coefficient,
        Fraction(0),
        "in 1/2-(1/2-delta), the constant coefficient cancels",
    ),
    equality(
        "subcritical_gap_delta_coefficient",
        gap_delta_coefficient,
        one,
        "in 1/2-(1/2-delta), the delta coefficient is one",
    ),
    equality(
        "endpoint_gamma_gap",
        half - half,
        Fraction(0),
        "at gamma=1/2 the logarithmic exponent gap is zero",
    ),
    equality(
        "endpoint_L_cancellation",
        endpoint_l_after_cancellation,
        Fraction(0),
        "the target L and sqrt-log L factors cancel in a hypothetical endpoint estimate",
    ),
    equality(
        "endpoint_inverse_outer_power",
        endpoint_inverse_outer_power,
        three_halves,
        "inverting the outer power 2/3 requires raising to 3/2",
    ),
    equality(
        "endpoint_payment_power",
        endpoint_payment_power,
        one,
        "raising P^(2/3) to 3/2 recovers P",
    ),
    equality(
        "endpoint_forced_B_power",
        endpoint_b_power,
        Fraction(3),
        "raising B^2 to 3/2 forces B^3",
    ),
    equality(
        "endpoint_forced_R_power",
        endpoint_r_power,
        Fraction(3),
        "raising R^2 to 3/2 forces R^3",
    ),
    equality(
        "endpoint_forced_K_power",
        endpoint_k_power,
        Fraction(-3, 2),
        "the hypothetical endpoint constant forces the factor K^-3/2",
    ),
    strict_less(
        "eventual_b_lower_is_below_limit",
        b_lower,
        b_limit,
        "1/256 is strictly below the limit 1/128",
    ),
    strict_less(
        "eventual_b_upper_is_above_limit",
        b_limit,
        b_upper,
        "1/128 is strictly below the convenient upper bound 1/64",
    ),
]

passed = sum(bool(item["pass"]) for item in checks)
payload = {
    "analytic_boundary": [
        "does not prove or justify the local energy inequality or the moving-test limit",
        "does not prove existence, uniqueness, confinement, or any estimate for the mollified path",
        "does not prove the fixed-cylinder interpolation inequality",
        "does not prove or invoke the velocity-only epsilon-regularity criterion",
        "does not prove the R0.74F-H packet construction or any packet upper or lower bound",
        "does not verify the literature boundary, novelty, or priority",
        "does not prove regularity, singularity exclusion, continuation, or global smoothness",
        "does not solve the Clay Millennium problem",
    ],
    "checks": checks,
    "exact_implications": [
        "The Navier-Stokes rescaling gives integral_(Q1)|U|^3 = r^-2 integral_(Qr)|u|^3 at the exponent level.",
        "From E^(3/2)<=P, the inverse exponent is 2/3; choosing P<=epsilon_tube^(3/2) is exponent-compatible with E<=epsilon_tube.",
        "For rho=1/320, the logarithmic window is [2 rho,3 rho] and the consecutive-index lower-minus-upper exponent is 5 rho=1/64.",
        "The payment upper scale to the 2/3 power supplies B^2 R^2, while sqrt(log P) supplies the missing L power.",
        "Writing gamma=1/2-delta makes the subcritical exponent gap exactly delta; the endpoint gap is zero.",
        "A hypothetical endpoint upper bound forces P to have powers B^3 R^3 and K^-3/2 after L cancellation.",
    ],
    "result": "PASS" if passed == len(checks) else "FAIL",
    "summary": {"passed": passed, "total": len(checks)},
}

print(json.dumps(payload, indent=2, sort_keys=True))
