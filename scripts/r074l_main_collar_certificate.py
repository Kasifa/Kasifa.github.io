#!/usr/bin/env python3
"""Exact finite certificate for the R0.74L main-collar proof.

This program checks only rational constants, finite-index thresholds, and
the R/L/B power ledger used by the common-forward-law and short-clock BV
argument.  It does not prove Brownian reversibility, reflection estimates,
stopping-time measurability, slice geometry, or a Navier--Stokes theorem.
"""

from __future__ import annotations

import json
import math
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
    elif relation == "<":
        passed = left < right
        margin = right - left
    elif relation == ">=":
        passed = left >= right
        margin = left - right
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
j_threshold = 14
L14 = lam * 2**j_threshold
distance_threshold = Fraction(262144, 15)

A = (Fraction(255, 256) ** 2) * c_h**2 / 264
A_expected = Fraction(4876875, 1476395008)
A_reserve = A - rho
A_reserve_expected = Fraction(1315703, 7381975040)

x = Fraction(256, 65)
taylor4 = sum(x**k / math.factorial(k) for k in range(5))
taylor4_expected = Fraction(587309569, 17850625)

B_R2_lower = Fraction(1, 128)
B_R2_upper = Fraction(1, 64)
clock_length_upper = 65 * B_R2_upper

c_pr = Fraction(65, 63)
component_length_coefficient = 2 * c_pr
inverse_clock_coefficient = Fraction(4, 3)
B_inverse_R2_coefficient = 128
physical_duration_coefficient = (
    component_length_coefficient
    * inverse_clock_coefficient
    * B_inverse_R2_coefficient
)
modulus_exponent_coefficient = one / (1024 * physical_duration_coefficient)

# Good row:
# R^6 * B^-1 * R^-1 * R^-3 * (L R) = L R^5.
good_R_power = Fraction(6) + 2 - 1 - 3 + 1
good_L_power = Fraction(1)

# Bad row:
# R^6 * R^-1 * L * R^-3 * R^2 * P_bad, P_bad <= 4R.
bad_R_power = Fraction(6) - 1 - 3 + 2 + 1
bad_L_power = Fraction(1)

checks = [
    row("lambda", lam, "==", Fraction(63, 32), "frozen dyadic scale"),
    row("center_height", c_h, "==", Fraction(15, 16), "frozen packet height"),
    row("radius_exponent", rho, "==", Fraction(1, 320), "R=exp(-rho L^2)"),
    row("L14", L14, "==", Fraction(32256), "first discrete index used by the transition buffer"),
    row(
        "L14_beats_distance_threshold",
        L14,
        ">=",
        distance_threshold,
        "64 <= c_h L/256 for every j>=14",
    ),
    row("bad_exponent_A", A, "==", A_expected, "reflection exponent after the 255/256 distance reserve"),
    row("bad_exponent_reserve", A_reserve, "==", A_reserve_expected, "A-rho exact reserve"),
    row("bad_exponent_reserve_positive", A_reserve, ">", zero, "bad paths pay one factor R"),
    row("heat_tail_argument", x, "==", Fraction(256, 65), "32R buffer through time 65R^2"),
    row("taylor4", taylor4, "==", taylor4_expected, "fourth exponential Taylor partial sum"),
    row("taylor4_beats_32", taylor4, ">", Fraction(32), "proves 4 exp(-256/65)<1/8"),
    row("B_R2_lower", B_R2_lower, "==", Fraction(1, 128), "inherited lower calibration"),
    row("B_R2_upper", B_R2_upper, "==", Fraction(1, 64), "inherited upper calibration"),
    row("clock_length_upper", clock_length_upper, "==", Fraction(65, 64), "|J| upper bound"),
    row("clock_length_below_two", clock_length_upper, "<", Fraction(2), "hence |J|<2pi"),
    row("projection_radius", c_pr, "==", Fraction(65, 63), "outer shell projection plus R/8 padding"),
    row(
        "component_length_coefficient",
        component_length_coefficient,
        "==",
        Fraction(130, 63),
        "one q-support component has length at most this times LR",
    ),
    row(
        "physical_duration_coefficient",
        physical_duration_coefficient,
        "==",
        Fraction(66560, 189),
        "component physical duration is at most this times LR^3",
    ),
    row(
        "modulus_exponent_coefficient",
        modulus_exponent_coefficient,
        "==",
        Fraction(189, 68157440),
        "reflection exponent c/(LR) for an R/16 oscillation",
    ),
    row("modulus_exponent_positive", modulus_exponent_coefficient, ">", zero, "short-clock modulus is superexponentially small in L"),
    row("good_R_power", good_R_power, "==", Fraction(5), "good-path R power is exactly target"),
    row("good_L_power", good_L_power, "==", Fraction(1), "good-path L power is exactly target"),
    row("bad_R_power", bad_R_power, "==", Fraction(5), "bad-path R power is exactly target"),
    row("bad_L_power", bad_L_power, "==", Fraction(1), "bad-path L power is exactly target"),
]

passed = sum(1 for item in checks if item["pass"])
result = {
    "schema": "r074l-main-collar-certificate-v1",
    "scope": "finite exact rational constants, thresholds, and scale ledger only",
    "result": "PASS" if passed == len(checks) else "FAIL",
    "inputs": {
        "lambda": q(lam),
        "c_h": q(c_h),
        "rho": q(rho),
        "j_threshold": j_threshold,
        "B_R2_interval": [q(B_R2_lower), q(B_R2_upper)],
    },
    "derived": {
        "L14": q(L14),
        "distance_threshold": q(distance_threshold),
        "bad_exponent_A": q(A),
        "bad_exponent_reserve": q(A_reserve),
        "taylor4_at_256_over_65": q(taylor4),
        "clock_length_upper": q(clock_length_upper),
        "projection_radius_coefficient": q(c_pr),
        "physical_duration_coefficient": q(physical_duration_coefficient),
        "modulus_exponent_coefficient": q(modulus_exponent_coefficient),
    },
    "checks": checks,
    "summary": {"passed": passed, "total": len(checks)},
    "analytic_boundary": [
        "does not prove the normalized-bridge reversal identity",
        "does not prove reflection-principle or stopping-time claims",
        "does not prove the thickened-slice BV geometry",
        "does not prove the short-clock occupation lemma",
        "does not treat the nearest inward collar or the full signed packet condition",
        "does not prove a universal endpoint estimate, regularity, singularity, or Clay",
    ],
    "status_flags": {
        "finite_arithmetic": "PASS",
        "main_collar_analytic_proof": "REQUIRES_INDEPENDENT_AUDIT",
        "nearest_inward_collar": "OUTSIDE_R074L_FREEZE",
        "clay_problem": "NOT_CLAIMED",
    },
}

print(json.dumps(result, indent=2, sort_keys=True))
