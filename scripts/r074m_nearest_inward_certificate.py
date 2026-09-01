#!/usr/bin/env python3
"""Exact finite certificate for the R0.74M nearest-inward proof.

The certificate checks rational constants, monotone finite thresholds, and
the R/L power ledger.  It does not prove the common-forward-law identity,
the Brownian reflection principle, heat-kernel positivity, periodic support
unfolding, or the analytic support-conditioned expulsion argument.
"""

from __future__ import annotations

import json
from fractions import Fraction


def q(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def row(
    check_id: str,
    left: Fraction,
    relation: str,
    right: Fraction,
    note: str,
) -> dict:
    if relation == "==":
        passed = left == right
        margin = left - right
    elif relation == ">":
        passed = left > right
        margin = left - right
    elif relation == ">=":
        passed = left >= right
        margin = left - right
    elif relation == "<":
        passed = left < right
        margin = right - left
    elif relation == "<=":
        passed = left <= right
        margin = right - left
    else:
        raise ValueError(relation)
    return {
        "id": check_id,
        "left": q(left),
        "relation": relation,
        "right": q(right),
        "margin": q(margin),
        "pass": passed,
        "note": note,
    }


zero = Fraction(0)
one = Fraction(1)

lam = Fraction(63, 32)
c_h = Fraction(15, 16)
rho = Fraction(1, 320)
g1 = Fraction(2, 1323)
c_def = Fraction(1, 640)
plateau_a = Fraction(49, 14625)

j_threshold = 13
L13 = lam * 2**j_threshold
L0 = Fraction(9216)

outer_coefficient = Fraction(32, 63)
modulus_coefficient = Fraction(1, 16)
target_path_coefficient = Fraction(3, 5)
geometry_gap = target_path_coefficient - outer_coefficient - modulus_coefficient

ell = Fraction(1, 64)
reflection_exponent = modulus_coefficient**2 / (4 * ell)

heat_time_lower = Fraction(3903, 64)
heat_exponent_multiplier = one / (4 * heat_time_lower)
heat_linear = Fraction(3, 5)
heat_offset = Fraction(64)

# c_def L^2 - 16/3903 (3L/5+64)^2
heat_margin_quadratic = c_def - heat_exponent_multiplier * heat_linear**2
heat_margin_linear = (
    2 * heat_exponent_multiplier * heat_linear * heat_offset
)
heat_margin_constant = heat_exponent_multiplier * heat_offset**2
heat_margin_at_L0 = (
    heat_margin_quadratic * L0**2
    - heat_margin_linear * L0
    - heat_margin_constant
)
heat_margin_derivative_at_L0 = (
    2 * heat_margin_quadratic * L0 - heat_margin_linear
)

plateau_gap = plateau_a - c_def
expulsion_gap = rho - c_def
bad_event_gap = reflection_exponent - rho - g1

sigma_denominator = Fraction(32768)
negative_term_coefficient = Fraction(65, 16)
negative_absorption_required = (
    negative_term_coefficient * sigma_denominator
)

# e^z >= z^2/2.  At L0 this already pays the negative plateau term, and
# z^2/L grows monotonically thereafter.
z0 = plateau_gap * L0**2
plateau_exp_lower = z0**2 / 2

# For L>=63/8, r_-/(LR)<=32/63+1/63=11/21.  The condition
# Sigma >= 4r_- follows from
# e^(L^2/640) >= 32768*(44/21)*L.
radius_coefficient_upper = Fraction(11, 21)
four_radius_coefficient = 4 * radius_coefficient_upper
x0 = c_def * L0**2
expulsion_exp_lower = x0**2 / 2
expulsion_radius_required = (
    sigma_denominator * four_radius_coefficient * L0
)

super_rate = 2 * (rho - c_def)
sigma_square_prefactor_denominator = Fraction(32768**2)

# Scale ledgers before the final exponential comparisons.
# bad: R^6 * R^2(time) * R^-1(K) * L * R^-3(dK L2) = L R^4.
bad_R_power = Fraction(6 + 2 - 1 - 3)
bad_L_power = Fraction(1)
# good: R^6 * R^2(time) * R^-1(K) * L * R^-4(dK tail) = L R^3.
good_R_power = Fraction(6 + 2 - 1 - 4)
good_L_power = Fraction(1)

checks = [
    row("lambda", lam, "==", Fraction(63, 32), "frozen dyadic scale"),
    row("center_height", c_h, "==", Fraction(15, 16), "frozen packet height"),
    row("radius_exponent", rho, "==", Fraction(1, 320), "R=exp(-rho L^2)"),
    row("weight_gap_G1", g1, "==", Fraction(2, 1323), "Gamma_(j-1)/Gamma_j exponent"),
    row("L13", L13, "==", Fraction(16128), "first inherited discrete index"),
    row("L13_beats_heat_threshold", L13, ">=", L0, "actual family index exceeds L>=9216"),
    row("outer_coefficient", outer_coefficient, "==", Fraction(32, 63), "j-1 padded outer radius before R/8"),
    row("geometry_gap", geometry_gap, "==", Fraction(149, 5040), "room below the 3L/5 defect window"),
    row("geometry_gap_positive", geometry_gap, ">", zero, "final segment remains in the defect window"),
    row("final_segment_length", ell, "==", Fraction(1, 64), "physical final segment length in R^2 units"),
    row("reflection_exponent", reflection_exponent, "==", Fraction(1, 16), "LR/16 Brownian modulus exponent"),
    row("heat_time_lower", heat_time_lower, "==", Fraction(3903, 64), "61-1/64"),
    row("heat_exponent_multiplier", heat_exponent_multiplier, "==", Fraction(16, 3903), "reciprocal of four times the lower heat time"),
    row("heat_margin_quadratic", heat_margin_quadratic, "==", Fraction(361, 4163200), "positive L^2 coefficient in the defect comparison"),
    row("heat_margin_linear", heat_margin_linear, "==", Fraction(2048, 6505), "linear cost in the defect comparison"),
    row("heat_margin_constant", heat_margin_constant, "==", Fraction(65536, 3903), "constant cost in the defect comparison"),
    row("heat_margin_at_L0", heat_margin_at_L0, "==", Fraction(433872896, 97575), "defect exponent margin at L=9216"),
    row("heat_margin_at_L0_positive", heat_margin_at_L0, ">", zero, "defect exponent holds at the base threshold"),
    row("heat_margin_derivative_at_L0", heat_margin_derivative_at_L0, "==", Fraction(41744, 32525), "margin is increasing after L=9216"),
    row("heat_margin_derivative_positive", heat_margin_derivative_at_L0, ">", zero, "monotone threshold propagation"),
    row("plateau_gap", plateau_gap, "==", Fraction(3347, 1872000), "plateau defect decays faster than the inward defect"),
    row("plateau_gap_positive", plateau_gap, ">", zero, "positive displacement survives subtraction"),
    row("expulsion_gap", expulsion_gap, "==", Fraction(1, 640), "expulsion scale is larger than LR"),
    row("expulsion_gap_positive", expulsion_gap, ">", zero, "Sigma/(LR) diverges"),
    row("negative_absorption_required", negative_absorption_required, "==", Fraction(133120), "exponential factor needed to absorb the global negative term"),
    row("plateau_exp_lower", plateau_exp_lower, ">", negative_absorption_required, "e^z >= z^2/2 pays the negative term at L=9216"),
    row("radius_coefficient_upper", radius_coefficient_upper, "==", Fraction(11, 21), "padded inward radius divided by LR"),
    row("four_radius_coefficient", four_radius_coefficient, "==", Fraction(44, 21), "coefficient required for Sigma>=4r_-"),
    row("expulsion_exp_lower", expulsion_exp_lower, ">", expulsion_radius_required, "e^x >= x^2/2 makes Sigma>=4r_- at L=9216"),
    row("bad_event_gap", bad_event_gap, "==", Fraction(24497, 423360), "fast-return rarity pays R and the weight gap"),
    row("bad_event_gap_positive", bad_event_gap, ">", zero, "bad path exponent has strict reserve"),
    row("super_rate", super_rate, "==", Fraction(1, 320), "Sigma^2/R^2 has exp(L^2/320) growth"),
    row("super_rate_positive", super_rate, ">", zero, "good-path heat tail is super-Gaussian in L"),
    row("sigma_square_denominator", sigma_square_prefactor_denominator, "==", Fraction(1073741824), "32768^2 exact prefactor denominator"),
    row("bad_R_power", bad_R_power, "==", Fraction(4), "raw bad-path ledger before its extra R payment"),
    row("bad_L_power", bad_L_power, "==", Fraction(1), "bad-path L power"),
    row("good_R_power", good_R_power, "==", Fraction(3), "raw good-path ledger before its R^2 tail payment"),
    row("good_L_power", good_L_power, "==", Fraction(1), "good-path L power"),
]

passed = sum(1 for item in checks if item["pass"])
result = {
    "schema": "r074m-nearest-inward-certificate-v1",
    "scope": "finite exact rational constants, monotone thresholds, and scale ledger only",
    "result": "PASS" if passed == len(checks) else "FAIL",
    "inputs": {
        "lambda": q(lam),
        "c_h": q(c_h),
        "rho": q(rho),
        "G1": q(g1),
        "c_def": q(c_def),
        "plateau_a": q(plateau_a),
        "j_threshold": j_threshold,
        "L_analytic_threshold": q(L0),
    },
    "derived": {
        "L13": q(L13),
        "geometry_gap": q(geometry_gap),
        "reflection_exponent": q(reflection_exponent),
        "heat_margin_at_L0": q(heat_margin_at_L0),
        "heat_margin_derivative_at_L0": q(heat_margin_derivative_at_L0),
        "plateau_gap": q(plateau_gap),
        "expulsion_gap": q(expulsion_gap),
        "bad_event_gap": q(bad_event_gap),
        "super_rate": q(super_rate),
        "bad_scale": f"L^{q(bad_L_power)} R^{q(bad_R_power)}",
        "good_scale": f"L^{q(good_L_power)} R^{q(good_R_power)}",
    },
    "checks": checks,
    "summary": {"passed": passed, "total": len(checks)},
    "analytic_boundary": [
        "does not prove the normalized bridge or common-forward-law identity",
        "does not prove the Brownian reflection estimate",
        "does not prove heat-kernel positivity or the periodic Gaussian tail",
        "does not prove the support-conditioned displacement lemma",
        "does not synthesize every shell row or prove the full R0.74K condition",
        "does not prove a universal endpoint estimate, regularity, singularity, or Clay",
    ],
    "status_flags": {
        "finite_arithmetic": "PASS" if passed == len(checks) else "FAIL",
        "nearest_inward_analytic_proof": "REQUIRES_INDEPENDENT_AUDIT",
        "full_signed_collar_condition": "OPEN",
        "clay_problem": "NOT_CLAIMED",
    },
}

print(json.dumps(result, indent=2, sort_keys=True))
