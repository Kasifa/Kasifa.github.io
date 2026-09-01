#!/usr/bin/env python3
"""Exact rational certificate for the R0.74E outer-annulus exponent gate.

This script certifies finite algebra only.  It does not certify the
Feynman--Kac survival estimate, any PDE bound, or a Navier--Stokes endpoint.
"""

from __future__ import annotations

import json
from fractions import Fraction


def q(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def decimal(value: Fraction, digits: int = 15) -> str:
    return f"{float(value):.{digits}g}"


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
l_min = Fraction(7680)
kappa = Fraction(16)
transition_width_over_R = 2 * kappa

c_gamma = Fraction(1, 1) / (128 * lam * lam)
gu_lower = Fraction(3, 2) * c_gamma
heat_upper = alpha * alpha / 260
leakage_exponent = c_h * c_h / 264
outer_threshold = Fraction(780, 1) / (256 * lam * lam)

midpoint_gu_lower = Fraction(1, 192)
midpoint_heat_upper = Fraction(1, 266240)

checks = [
    strict_greater("lambda_inside_lower_edge", lam, Fraction(1), "target is beyond annulus inner radius"),
    strict_less("lambda_inside_outer_edge", lam, Fraction(2), "target remains below annulus outer radius"),
    equality("radial_split", c_h * c_h + beta_sq, Fraction(1), "h^2+q^2=r^2"),
    equality("gamma_coefficient", c_gamma, Fraction(8, 3969), "1/(128 lambda^2)"),
    equality("packet_Gu_threshold", gu_lower, Fraction(4, 1323), "(3/2)c_gamma"),
    strict_less("window_lower", gu_lower, c_r, "packet target dominates the formal Gu row"),
    strict_less("window_upper", c_r, heat_upper, "direct caloric isolation has exponent room"),
    strict_greater("local_leakage_beats_inverse_R", leakage_exponent, c_r, "transverse leakage beats the inverse-R prefactor in packet survival"),
    strict_greater("local_leakage_margin", leakage_exponent, c_gamma, "transverse leakage exponent beats annular weight"),
    strict_greater("outer_transition_threshold", alpha * alpha, outer_threshold, "equivalent nonempty-window condition"),
    equality("buffer_gap", c_h - alpha, Fraction(1, 240), "reserved asymptotic transition margin"),
    equality("finite_separation_threshold", l_min * (c_h - alpha), transition_width_over_R, "L>=7680 pays arcsin(kappa R)<=32R"),
    strict_greater("midpoint_window_empty", midpoint_gu_lower, midpoint_heat_upper, "old midpoint sufficient conditions are incompatible"),
]

passed = sum(1 for item in checks if item["pass"])
result = {
    "schema": "r074e-outer-annulus-exponent-certificate-v1",
    "scope": "finite exact rational exponent compatibility only",
    "status": "PASS" if passed == len(checks) else "FAIL",
    "inputs": {
        "lambda": q(lam),
        "L_min": q(l_min),
        "kappa": q(kappa),
        "c_h": q(c_h),
        "alpha": q(alpha),
        "beta_squared": q(beta_sq),
        "c_R": q(c_r),
    },
    "derived": {
        "c_gamma": q(c_gamma),
        "packet_Gu_lower": q(gu_lower),
        "heat_isolation_upper": q(heat_upper),
        "local_leakage_exponent": q(leakage_exponent),
        "outer_transition_threshold": q(outer_threshold),
    },
    "decimal_window": {
        "lower": decimal(gu_lower),
        "chosen": decimal(c_r),
        "upper": decimal(heat_upper),
    },
    "checks": checks,
    "summary": {
        "passed": passed,
        "total": len(checks),
    },
    "analytic_boundary": [
        "does not prove heat-evolved contrast bounds",
        "does not prove packet survival or leakage estimates",
        "does not certify pressure or exterior-payment rows",
        "does not prove endpoint divergence, regularity, or Clay",
    ],
}

print(json.dumps(result, indent=2, sort_keys=True))
