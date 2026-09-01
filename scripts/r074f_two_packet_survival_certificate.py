#!/usr/bin/env python3
"""Exact finite certificate for the R0.74F two-packet survival gate.

This script certifies finite rational arithmetic and a conditional annular
inclusion only.  It does not certify Brownian confinement, a Brownian-bridge
or Feynman--Kac survival estimate, any Navier--Stokes endpoint, or Clay.
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


# Frozen R0.74E geometry.
lam = Fraction(63, 32)
c_h = Fraction(15, 16)
alpha = Fraction(14, 15)
beta_sq = Fraction(31, 256)
c_r = Fraction(1, 320)
kappa = Fraction(16)
c_gamma = Fraction(8, 3969)

# New finite R0.74F bookkeeping constants.
l_contrast = Fraction(7680)
l_surv = Fraction(9216)
shrink = Fraction(255, 256)
transition_width_over_rsmall = 2 * kappa
terminal_vertical_error_over_rsmall = Fraction(1)
buffer_over_rsmall = transition_width_over_rsmall + terminal_vertical_error_over_rsmall
effective_separation = shrink * c_h
minimum_continuous_l = 256 * buffer_over_rsmall / c_h

# Exponents.  A separately proved analytic estimate would supply the
# denominators 260 and 264; this certificate checks only their compatibility.
c_surv = effective_separation * effective_separation / 260
c_leak = c_h * c_h / 264
c_alpha_heat = alpha * alpha / 260

# Discrete scale sequence L_j=lambda 2^j.
l_12 = lam * 2**12
l_13 = lam * 2**13

# Conditional terminal-lobe geometry.  For either sign, assume
# x=(x1, +/-q+e2, +/-h+e3), q^2+h^2=r^2, and the three absolute bounds below.
x1_half_width_over_r = Fraction(1, 16)
z_abs_over_rsmall = Fraction(2)
q_error_over_rsmall = Fraction(1, 32)
e2_abs_over_rsmall = z_abs_over_rsmall + q_error_over_rsmall
e3_abs_over_rsmall = Fraction(1)
error_l1_over_rsmall = e2_abs_over_rsmall + e3_abs_over_rsmall

inner_radius_ratio = Fraction(1, 1) / lam
outer_radius_sq_ratio = (Fraction(2, 1) / lam) ** 2
inner_margin_at_threshold = (
    Fraction(1) - inner_radius_ratio - error_l1_over_rsmall / l_surv
)
outer_asymptotic_margin = (
    outer_radius_sq_ratio - Fraction(1) - x1_half_width_over_r**2
)
conditional_upper_sq_at_threshold = (
    Fraction(1)
    + x1_half_width_over_r**2
    + 2 * error_l1_over_rsmall / l_surv
    + (
        e2_abs_over_rsmall**2 + e3_abs_over_rsmall**2
    )
    / l_surv**2
)
outer_sq_margin_at_threshold = (
    outer_radius_sq_ratio - conditional_upper_sq_at_threshold
)

checks = [
    strict_greater(
        "lambda_inside_lower_edge",
        lam,
        Fraction(1),
        "the target radius is beyond the dyadic inner edge",
    ),
    strict_less(
        "lambda_inside_outer_edge",
        lam,
        Fraction(2),
        "the target radius is below the dyadic outer edge",
    ),
    equality(
        "radial_split",
        c_h * c_h + beta_sq,
        Fraction(1),
        "q_j squared plus h_j squared equals r_j squared",
    ),
    equality(
        "gamma_coefficient",
        c_gamma,
        Fraction(1, 1) / (128 * lam * lam),
        "R0.74E annular-weight coefficient",
    ),
    equality(
        "transition_width",
        transition_width_over_rsmall,
        Fraction(32),
        "2 kappa small-radius units reserved for the transition strip",
    ),
    equality(
        "buffer_definition",
        buffer_over_rsmall,
        Fraction(33),
        "transition width plus one terminal vertical-error unit",
    ),
    strict_greater(
        "survival_threshold_above_contrast_threshold",
        l_surv,
        l_contrast,
        "the new finite threshold retains the R0.74E contrast threshold",
    ),
    strict_greater(
        "buffer_budget_at_threshold",
        c_h * l_surv / 256,
        buffer_over_rsmall,
        "one 256th of h_j pays the 33-small-radius buffer",
    ),
    equality(
        "minimum_continuous_threshold",
        minimum_continuous_l,
        Fraction(45056, 5),
        "exact continuous L threshold for the buffer inequality",
    ),
    strict_greater(
        "chosen_threshold_above_continuous_minimum",
        l_surv,
        minimum_continuous_l,
        "the transparent integer threshold has positive room",
    ),
    equality(
        "effective_separation",
        effective_separation,
        Fraction(3825, 4096),
        "the conservative post-buffer separation coefficient",
    ),
    strict_greater(
        "effective_separation_beats_alpha",
        effective_separation,
        alpha,
        "the post-buffer coefficient remains above the R0.74E alpha",
    ),
    strict_greater(
        "denominator_swap",
        shrink * shrink / 260,
        Fraction(1, 264),
        "the 255/256 shrink still beats the denominator-264 exponent",
    ),
    equality(
        "survival_exponent",
        c_surv,
        Fraction(2926125, 872415232),
        "conditional buffered survival exponent",
    ),
    equality(
        "leakage_exponent",
        c_leak,
        Fraction(75, 22528),
        "conditional local-leakage exponent",
    ),
    strict_greater(
        "survival_exponent_beats_leakage_exponent",
        c_surv,
        c_leak,
        "the buffered exponent hierarchy is strict",
    ),
    strict_greater(
        "survival_exponent_beats_inverse_R",
        c_surv,
        c_r,
        "conditional survival decay has room after an inverse-R prefactor",
    ),
    strict_greater(
        "leakage_exponent_beats_inverse_R",
        c_leak,
        c_r,
        "conditional leakage decay has room after an inverse-R prefactor",
    ),
    strict_greater(
        "inverse_R_beats_annular_weight",
        c_r,
        c_gamma,
        "the inherited R0.74E exponent ordering is retained",
    ),
    strict_greater(
        "survival_exponent_beats_alpha_heat",
        c_surv,
        c_alpha_heat,
        "the buffered exponent also exceeds the earlier alpha heat exponent",
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
    strict_less(
        "discrete_L12_below_threshold",
        l_12,
        l_surv,
        "the threshold excludes j=12",
    ),
    strict_greater(
        "discrete_L13_above_threshold",
        l_13,
        l_surv,
        "j=13 is the first admissible sequence index",
    ),
    equality(
        "terminal_horizontal_error_budget",
        e2_abs_over_rsmall,
        Fraction(65, 32),
        "two packet units plus the conditional 1/32 Q-error",
    ),
    equality(
        "terminal_total_transverse_L1_budget",
        error_l1_over_rsmall,
        Fraction(97, 32),
        "conditional e2 plus e3 absolute-error budget",
    ),
    strict_greater(
        "conditional_inner_annulus_margin",
        inner_margin_at_threshold,
        Fraction(0),
        "at L_surv the terminal lobe is strictly beyond the inner edge",
    ),
    strict_greater(
        "outer_asymptotic_margin",
        outer_asymptotic_margin,
        Fraction(0),
        "the chosen r/16 x1 half-width leaves asymptotic outer room",
    ),
    equality(
        "conditional_upper_square_at_threshold",
        conditional_upper_sq_at_threshold,
        Fraction(87370044545, 86973087744),
        "rational upper bound for terminal-lobe squared radius",
    ),
    strict_greater(
        "conditional_outer_annulus_margin",
        outer_sq_margin_at_threshold,
        Fraction(0),
        "at L_surv the terminal lobe is strictly inside the outer edge",
    ),
]

passed = sum(1 for item in checks if item["pass"])
result = {
    "schema": "r074f-two-packet-survival-finite-certificate-v1",
    "scope": "finite exact rational compatibility and conditional annular geometry only",
    "status": "PASS" if passed == len(checks) else "FAIL",
    "inputs": {
        "lambda": q(lam),
        "c_h": q(c_h),
        "alpha": q(alpha),
        "beta_squared": q(beta_sq),
        "c_R": q(c_r),
        "kappa": q(kappa),
        "c_gamma": q(c_gamma),
        "L_contrast": q(l_contrast),
        "L_surv": q(l_surv),
        "shrink": q(shrink),
    },
    "conditional_geometry_hypotheses": {
        "x1_half_width_over_r": q(x1_half_width_over_r),
        "z_abs_over_R": q(z_abs_over_rsmall),
        "Q_error_abs_over_R": q(q_error_over_rsmall),
        "e2_abs_over_R": q(e2_abs_over_rsmall),
        "e3_abs_over_R": q(e3_abs_over_rsmall),
        "statement": "For either lobe sign, x=(x1,+/-q+e2,+/-h+e3) with q^2+h^2=r^2; the listed absolute bounds are hypotheses, not outputs of this certificate.",
    },
    "derived": {
        "buffer_over_R": q(buffer_over_rsmall),
        "minimum_continuous_L": q(minimum_continuous_l),
        "effective_separation": q(effective_separation),
        "c_surv": q(c_surv),
        "c_leak": q(c_leak),
        "inner_margin_at_L_surv": q(inner_margin_at_threshold),
        "outer_sq_margin_at_L_surv": q(outer_sq_margin_at_threshold),
    },
    "decimal_exponents": {
        "c_gamma": decimal(c_gamma),
        "c_R": decimal(c_r),
        "c_leak": decimal(c_leak),
        "c_surv": decimal(c_surv),
    },
    "checks": checks,
    "summary": {
        "passed": passed,
        "total": len(checks),
    },
    "analytic_boundary": [
        "does not prove the transition-width or Q-error hypotheses",
        "does not prove torus-chart validity or periodic heat-kernel estimates",
        "does not prove Brownian confinement or any Brownian-bridge estimate",
        "does not prove Feynman--Kac time ordering, packet survival, or sign preservation",
        "does not certify pressure, leakage, exterior-payment, or endpoint rows",
        "does not prove Navier--Stokes regularity, singularity, or the Clay problem",
    ],
}

print(json.dumps(result, indent=2, sort_keys=True))
