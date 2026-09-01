#!/usr/bin/env python3
"""Exact finite certificate for the R0.74J matching-payment arithmetic.

Only rational shell geometry, Brownian/Chebyshev coefficients, payment
normalization powers, and logarithmic exponents are checked.  The script does
not prove the periodic heat representation, the analytic shear lower bound,
the inherited R0.74G upper bound, or any Navier--Stokes theorem.
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


one = Fraction(1)
half = Fraction(1, 2)
two_thirds = Fraction(2, 3)

shell_index = Fraction(5)
rho_over_r = Fraction(2)
shell_inner = Fraction(2) ** int(shell_index) * rho_over_r
shell_outer = Fraction(2) ** (int(shell_index) + 1) * rho_over_r
box_x1_length = Fraction(2)
box_x2_length = Fraction(2)
box_x3_lower = Fraction(80)
box_x3_upper = Fraction(96)
box_x3_length = box_x3_upper - box_x3_lower
box_volume = box_x1_length * box_x2_length * box_x3_length
box_outer_square = box_x3_upper**2 + one + one
shell_outer_square = shell_outer**2

gamma_numerator = Fraction(4) ** (int(shell_index) - 1)
gamma_exponent = gamma_numerator / Fraction(32)

r_cap = Fraction(1, 200)
arcsin_input_cap = Fraction(16) * r_cap
delta_over_r = Fraction(2) * Fraction(16)
left_distance = box_x3_lower - delta_over_r
right_distance_absolute_lower = Fraction(3) - (
    delta_over_r + box_x3_upper
) * r_cap
required_distance_at_cap = Fraction(48) * r_cap

time_upper = Fraction(65)
brownian_variance_coefficient = Fraction(2) * time_upper
exit_denominator = left_distance**2
exit_probability = brownian_variance_coefficient / exit_denominator
one_minus_theta = Fraction(2) * exit_probability
theta_lower = one - one_minus_theta

time_lower = Fraction(61)
time_length = time_upper - time_lower
normalization_coefficient = Fraction(1, 4)
box_volume_coefficient = box_volume
theta_cube_floor = half**3
gu_coefficient = (
    normalization_coefficient
    * time_length
    * box_volume_coefficient
    * theta_cube_floor
)
gu_r_power = Fraction(-2) + Fraction(2) + Fraction(3)

rho = Fraction(1, 320)
log_payment_coefficient = Fraction(3) * rho
l_square_ratio = Fraction(2) ** 2
lacunarity_coefficient = log_payment_coefficient * (l_square_ratio - one)

payment_b_power = Fraction(3)
payment_r_power = Fraction(3)
payment_l_power = Fraction(0)
payment_23_b_power = payment_b_power * two_thirds
payment_23_r_power = payment_r_power * two_thirds
payment_23_l_power = payment_l_power * two_thirds
sqrt_log_l_power = Fraction(2) * half
frontier_l_power = payment_23_l_power + sqrt_log_l_power

ratio_b_power = payment_b_power - Fraction(2)
ratio_r_power = payment_r_power - Fraction(2)
ratio_l_power = payment_l_power - Fraction(1)

checks = [
    equality(
        "payment_shell_index",
        shell_index,
        Fraction(5),
        "the selected payment shell has index k=5",
    ),
    equality(
        "payment_radius_over_R",
        rho_over_r,
        Fraction(2),
        "the complete payment is evaluated at rho=2R",
    ),
    equality(
        "shell_inner_over_R",
        shell_inner,
        Fraction(64),
        "2^5 times 2R gives the fifth-shell inner radius 64R",
    ),
    equality(
        "shell_outer_over_R",
        shell_outer,
        Fraction(128),
        "2^6 times 2R gives the fifth-shell outer radius 128R",
    ),
    strict_less(
        "box_inner_is_outside_shell_inner",
        shell_inner,
        box_x3_lower,
        "the box has |x|>80R>64R",
    ),
    strict_less(
        "box_outer_square_is_inside_shell_outer",
        box_outer_square,
        shell_outer_square,
        "96^2+1^2+1^2 is strictly below 128^2",
    ),
    equality(
        "box_outer_squared_margin",
        shell_outer_square - box_outer_square,
        Fraction(7166),
        "the exact squared outer-shell margin is 7166 R^2",
    ),
    equality(
        "box_volume_coefficient",
        box_volume,
        Fraction(64),
        "the side lengths 2R,2R,16R give volume 64R^3",
    ),
    equality(
        "gamma5_power_numerator",
        gamma_numerator,
        Fraction(256),
        "4^(5-1)=256",
    ),
    equality(
        "gamma5_exponent",
        gamma_exponent,
        Fraction(8),
        "4^4/32=8, so gamma_5=e^-8",
    ),
    equality(
        "R_cap",
        r_cap,
        Fraction(1, 200),
        "the analytic proof imposes R<=1/200",
    ),
    equality(
        "arcsin_input_cap",
        arcsin_input_cap,
        Fraction(2, 25),
        "16R<=2/25 under the frozen R cap",
    ),
    strict_less(
        "arcsin_input_below_half",
        arcsin_input_cap,
        half,
        "2/25<1/2 permits arcsin(s)<=2s",
    ),
    equality(
        "delta_over_R_upper",
        delta_over_r,
        Fraction(32),
        "arcsin(16R)<=32R",
    ),
    equality(
        "left_plateau_distance_over_R",
        left_distance,
        Fraction(48),
        "80R-32R=48R",
    ),
    strict_less(
        "right_plateau_distance_at_R_cap",
        required_distance_at_cap,
        right_distance_absolute_lower,
        "pi>3 and R<=1/200 leave more than 48R on the right",
    ),
    equality(
        "brownian_variance_coefficient",
        brownian_variance_coefficient,
        Fraction(130),
        "Var(Z_t)=2t<=130R^2",
    ),
    equality(
        "chebyshev_denominator_coefficient",
        exit_denominator,
        Fraction(2304),
        "(48R)^2=2304R^2",
    ),
    equality(
        "exit_probability_upper",
        exit_probability,
        Fraction(65, 1152),
        "130/2304 reduces to 65/1152",
    ),
    equality(
        "one_minus_theta_upper",
        one_minus_theta,
        Fraction(65, 576),
        "the range bound 0<=1-g<=2 doubles the exit probability",
    ),
    equality(
        "theta_rational_lower",
        theta_lower,
        Fraction(511, 576),
        "1-65/576=511/576",
    ),
    strict_less(
        "half_is_below_theta_lower",
        half,
        theta_lower,
        "511/576>1/2",
    ),
    equality(
        "I_2R_length_coefficient",
        time_length,
        Fraction(4),
        "65-61=4",
    ),
    equality(
        "payment_normalization_coefficient",
        normalization_coefficient,
        Fraction(1, 4),
        "(2R)^-2=(1/4)R^-2",
    ),
    equality(
        "theta_cube_floor",
        theta_cube_floor,
        Fraction(1, 8),
        "(1/2)^3=1/8",
    ),
    equality(
        "Gu_lower_coefficient",
        gu_coefficient,
        Fraction(8),
        "(1/4)*4*64*(1/8)=8",
    ),
    equality(
        "Gu_R_power",
        gu_r_power,
        Fraction(3),
        "normalization,time,and volume give -2+2+3=3",
    ),
    equality(
        "rho_exact_value",
        rho,
        Fraction(1, 320),
        "the frozen family uses rho=1/320",
    ),
    equality(
        "log_payment_coefficient",
        log_payment_coefficient,
        Fraction(3, 320),
        "matching B^3R^3 payment gives logarithmic coefficient 3rho",
    ),
    equality(
        "L_square_ratio",
        l_square_ratio,
        Fraction(4),
        "L_(j+1)^2=4L_j^2",
    ),
    equality(
        "lacunarity_coefficient",
        lacunarity_coefficient,
        Fraction(9, 320),
        "3rho*(4-1)=9rho=9/320",
    ),
    equality(
        "payment_23_B_power",
        payment_23_b_power,
        Fraction(2),
        "(B^3R^3)^(2/3) has B power 2",
    ),
    equality(
        "payment_23_R_power",
        payment_23_r_power,
        Fraction(2),
        "(B^3R^3)^(2/3) has R power 2",
    ),
    equality(
        "sqrt_log_L_power",
        sqrt_log_l_power,
        one,
        "sqrt of a logarithm proportional to L^2 supplies L power 1",
    ),
    equality(
        "frontier_total_L_power",
        frontier_l_power,
        one,
        "P^(2/3)sqrt(log P) has total L power 1",
    ),
    equality(
        "payment_to_target_ratio_B_power",
        ratio_b_power,
        one,
        "(B^3R^3)/(B^2LR^2) has B power 1",
    ),
    equality(
        "payment_to_target_ratio_R_power",
        ratio_r_power,
        one,
        "(B^3R^3)/(B^2LR^2) has R power 1",
    ),
    equality(
        "payment_to_target_ratio_L_power",
        ratio_l_power,
        Fraction(-1),
        "(B^3R^3)/(B^2LR^2) has L power -1",
    ),
]

passed = sum(bool(item["pass"]) for item in checks)
payload = {
    "analytic_boundary": [
        "does not prove the periodic heat-semigroup or Brownian representation",
        "does not prove arcsin(s)<=2s, pi>3, Chebyshev, or the circle-distance implication",
        "does not prove the shear lower bound for the continuum heat equation",
        "does not prove the R0.74F family construction or zero-frame identities",
        "does not prove the inherited R0.74G complete-payment upper bound",
        "does not prove any upper bound for X_j or C_j",
        "does not verify literature novelty or publication priority",
        "does not prove regularity, singularity exclusion, global smoothness, or the Clay Millennium problem",
    ],
    "analytic_inputs": [
        "the selected periodic shear equals one on P_R and lies in [-1,1]",
        "the periodic heat semigroup is expectation under Z_t mod 2pi with Var(Z_t)=2t",
        "all complete-payment rows are nonnegative",
        "Version M and Version F coincide on the explicit family",
        "R0.74G supplies P_j<=C B_j^3 R_j^3 and B_j R_j^2 tends to 1/128",
    ],
    "checks": checks,
    "exact_implications": [
        "The fifth-shell proof box has weight e^-8 and volume 64R^3.",
        "The rational Chebyshev ledger gives theta>=511/576>1/2.",
        "The cubic row coefficient based on theta>=1/2 is 8e^-8 B^3R^3.",
        "Matching payment gives log(P_j)/L_j^2 tending to 3rho and lacunarity coefficient 9rho.",
        "P_j^(2/3)sqrt(log P_j) has the monomial scale B_j^2 L_j R_j^2.",
    ],
    "result": "PASS" if passed == len(checks) else "FAIL",
    "summary": {"passed": passed, "total": len(checks)},
}

print(json.dumps(payload, indent=2, sort_keys=True))
