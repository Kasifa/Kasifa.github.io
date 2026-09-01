#!/usr/bin/env python3
"""Exact finite certificate for the R0.74K single-collar exponent audit.

The program checks rational annular geometry, Gaussian/weight exponent
comparisons, and the algebraic normalization of the conditional collar
statement.  It does not prove a Brownian-bridge estimate, a passive-scalar
PDE bound, an observable upper bound, or any Navier--Stokes regularity result.
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
    elif relation == "<":
        passed = left < right
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


one = Fraction(1)
zero = Fraction(0)

lam = Fraction(63, 32)
c_h = Fraction(15, 16)
rho = Fraction(1, 320)
c_gamma = Fraction(8, 3969)
epsilon = Fraction(1, 128)


def outer_edge(m: int) -> Fraction:
    return one / (lam * 2 ** (m - 1))


def distance(m: int) -> Fraction:
    return c_h - outer_edge(m)


def gain(m: int) -> Fraction:
    return c_gamma * (one - Fraction(1, 4**m))


def sharp_cost(m: int) -> Fraction:
    return distance(m) ** 2 / 132


def coarse_cost(m: int) -> Fraction:
    return distance(m) ** 2 / 262


d1 = distance(1)
d2 = distance(2)
d3 = distance(3)
g1 = gain(1)
g2 = gain(2)
g3 = gain(3)

d_epsilon = c_h - one / lam + epsilon
eta_epsilon = one / lam - epsilon
chord_square = one / lam**2 - (one / lam - epsilon) ** 2
nearest_boundary_wrong_margin = g1 - sharp_cost(1)
nearest_slab_wrong_margin = g1 - d_epsilon**2 / 132

sharp_m2_margin = sharp_cost(2) - g2
uniform_deep_margin = d2**2 / 132 - c_gamma
coarse_m2_margin = coarse_cost(2) - g2
coarse_m3_margin = coarse_cost(3) - g3
padding_robust_m2_margin = (d2 - epsilon) ** 2 / 132 - g2

outer_one_shell_decay = 3 * c_gamma
outer_after_one_r_loss = outer_one_shell_decay - rho

# Conditional collar scaling:
# (a^2 B / R) (Gamma L R^5), with a^2=B^2/Gamma,
# equals B^3 L R^4 = (B R^2)(B^2 L R^2).
prefactor_b = Fraction(3)
prefactor_gamma = Fraction(-1)
prefactor_r = Fraction(-1)
integral_gamma = Fraction(1)
integral_l = Fraction(1)
integral_r = Fraction(5)
combined_b = prefactor_b
combined_gamma = prefactor_gamma + integral_gamma
combined_l = integral_l
combined_r = prefactor_r + integral_r
target_b = Fraction(2)
target_l = Fraction(1)
target_r = Fraction(2)
beta_b = Fraction(1)
beta_r = Fraction(2)

checks = [
    row("lambda", lam, "==", Fraction(63, 32), "frozen scale ratio"),
    row("center_height", c_h, "==", Fraction(15, 16), "frozen packet height"),
    row("radius_exponent", rho, "==", Fraction(1, 320), "R=exp(-rho L^2)"),
    row("annular_exponent", c_gamma, "==", Fraction(8, 3969), "Gamma_j=exp(-c_gamma L^2)"),
    row("annular_scale_identity", c_gamma * lam**2, "==", Fraction(1, 128), "c_gamma L_j^2=4^j/128"),
    row("inverse_lambda", one / lam, "==", Fraction(32, 63), "target-shell inner radius in r units"),
    row("m1_distance", d1, "==", Fraction(433, 1008), "nearest inward boundary gap"),
    row("m2_distance", d2, "==", Fraction(689, 1008), "second inward boundary gap"),
    row("m3_distance", d3, "==", Fraction(817, 1008), "third inward boundary gap"),
    row("m1_weight_gain", g1, "==", Fraction(2, 1323), "(3/4)c_gamma"),
    row("m2_weight_gain", g2, "==", Fraction(5, 2646), "(15/16)c_gamma"),
    row("m3_weight_gain", g3, "==", Fraction(1, 504), "(63/64)c_gamma"),
    row(
        "nearest_boundary_wrong_margin",
        nearest_boundary_wrong_margin,
        "==",
        Fraction(15263, 134120448),
        "even the sharp free squared kernel loses at the j-1 boundary",
    ),
    row("nearest_boundary_wrong_sign", nearest_boundary_wrong_margin, ">", zero, "wrong-direction exponent is strict"),
    row("epsilon", epsilon, "==", Fraction(1, 128), "fixed positive-volume inward offset"),
    row("epsilon_slab_height", eta_epsilon, "==", Fraction(4033, 8064), "positive-volume slab height in r units"),
    row("epsilon_distance", d_epsilon, "==", Fraction(3527, 8064), "gap at the positive-volume slab"),
    row("chord_square", chord_square, "==", Fraction(8129, 1032192), "available x1 chord squared"),
    row("chord_positive", chord_square, ">", zero, "the slab has a nonzero invariant-direction chord"),
    row(
        "nearest_slab_wrong_margin",
        nearest_slab_wrong_margin,
        "==",
        Fraction(536399, 8583708672),
        "positive-volume wrong-direction exponent",
    ),
    row("nearest_slab_wrong_sign", nearest_slab_wrong_margin, ">", zero, "free-heat replacement cannot close j-1"),
    row(
        "sharp_m2_margin",
        sharp_m2_margin,
        "==",
        Fraction(221281, 134120448),
        "sharp p=2 exponent closes j-2",
    ),
    row("sharp_m2_positive", sharp_m2_margin, ">", zero, "j-2 has sharp exponent room"),
    row(
        "uniform_deep_margin",
        uniform_deep_margin,
        "==",
        Fraction(204385, 134120448),
        "uniform lower margin for all m>=2 after replacing gain by c_gamma",
    ),
    row("uniform_deep_positive", uniform_deep_margin, ">", zero, "all m>=2 have optimistic sharp room"),
    row(
        "padding_robust_m2_margin",
        padding_robust_m2_margin,
        "==",
        Fraction(13471441, 8583708672),
        "j-2 remains sharp-compatible after an epsilon padding loss",
    ),
    row("padding_robust_m2_positive", padding_robust_m2_margin, ">", zero, "padded j-2 margin is strict"),
    row(
        "coarse_m2_margin",
        coarse_m2_margin,
        "==",
        Fraction(-28319, 266208768),
        "the inherited denominator 262 narrowly misses at j-2",
    ),
    row("coarse_m2_negative", coarse_m2_margin, "<", zero, "j-2 needs the sharp p=2 denominator"),
    row(
        "coarse_m3_margin",
        coarse_m3_margin,
        "==",
        Fraction(139297, 266208768),
        "the inherited denominator 262 closes j-3",
    ),
    row("coarse_m3_positive", coarse_m3_margin, ">", zero, "all m>=3 are coarsely compatible"),
    row("outer_one_shell_decay", outer_one_shell_decay, "==", Fraction(8, 1323), "Gamma_{j+1}/Gamma_j exponent"),
    row(
        "outer_after_one_R_loss",
        outer_after_one_r_loss,
        "==",
        Fraction(1237, 423360),
        "one outer-shell weight jump beats one inverse-R loss",
    ),
    row("outer_after_one_R_loss_positive", outer_after_one_r_loss, ">", zero, "outer compatibility margin is strict"),
    row("conditional_gamma_cancellation", combined_gamma, "==", zero, "Gamma from the integral cancels amplitude Gamma inverse"),
    row("conditional_B_power", combined_b, "==", Fraction(3), "collar implication first gives B^3"),
    row("conditional_L_power", combined_l, "==", Fraction(1), "one L remains"),
    row("conditional_R_power", combined_r, "==", Fraction(4), "R^-1 times R^5 gives R^4"),
    row("beta_times_target_B_power", beta_b + target_b, "==", combined_b, "(BR^2)(B^2LR^2) has B^3"),
    row("beta_times_target_L_power", target_l, "==", combined_l, "conditional and target L powers agree"),
    row("beta_times_target_R_power", beta_r + target_r, "==", combined_r, "(BR^2)(B^2LR^2) has R^4"),
]

passed = sum(1 for item in checks if item["pass"])
result = {
    "schema": "r074k-single-collar-exponent-certificate-v1",
    "scope": "finite exact rational shell, exponent, and conditional-scaling algebra only",
    "result": "PASS" if passed == len(checks) else "FAIL",
    "inputs": {
        "lambda": q(lam),
        "c_h": q(c_h),
        "rho": q(rho),
        "c_gamma": q(c_gamma),
        "epsilon": q(epsilon),
    },
    "derived": {
        "nearest_boundary_wrong_margin": q(nearest_boundary_wrong_margin),
        "nearest_positive_volume_wrong_margin": q(nearest_slab_wrong_margin),
        "positive_volume_chord_square": q(chord_square),
        "sharp_m2_margin": q(sharp_m2_margin),
        "uniform_m_ge_2_margin": q(uniform_deep_margin),
        "padding_robust_m2_margin": q(padding_robust_m2_margin),
        "coarse_m2_margin": q(coarse_m2_margin),
        "coarse_m3_margin": q(coarse_m3_margin),
        "outer_after_one_R_loss": q(outer_after_one_r_loss),
    },
    "checks": checks,
    "summary": {"passed": passed, "total": len(checks)},
    "analytic_boundary": [
        "does not prove free heat is a lower or upper model for the true packet",
        "does not prove a normalized Brownian-bridge or exceptional-path estimate",
        "does not prove the conditional collar hypothesis",
        "does not prove a matching upper bound for X_j or mathfrak C_j",
        "does not prove a universal endpoint estimate, regularity, singularity, or Clay",
    ],
    "status_flags": {
        "finite_arithmetic": "PASS",
        "nearest_free_tail": "FAIL_FREE_TAIL_AS_PROOF_MECHANISM",
        "required_next_mechanism": "ANALYTIC_SHEAR_LAG_REQUIRED",
        "conditional_collar_hypothesis": "OPEN",
        "clay_problem": "NOT_CLAIMED",
    },
}

print(json.dumps(result, indent=2, sort_keys=True))
