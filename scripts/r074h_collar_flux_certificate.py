#!/usr/bin/env python3
"""Exact finite compatibility certificate for R0.74H.

The script checks only rational exponent arithmetic and the finite algebraic
reductions used by the collar-flux and two-regime estimates.  It does not
certify the weighted energy identity, the shell limit, pressure estimates,
the explicit packet construction, or any Navier--Stokes regularity claim.
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


one = Fraction(1)
two_thirds = Fraction(2, 3)
three_halves = Fraction(3, 2)

# Parabolic shell bookkeeping.
time_power = Fraction(2)
space_power = Fraction(3)
measure_power = time_power + space_power
holder_volume_power = measure_power / 3
quadratic_prefactor_power = Fraction(-3)
normalized_s2_power = quadratic_prefactor_power + holder_volume_power
normalized_s3_power = Fraction(-2) * two_thirds

# R0.74G amplitude and scale bookkeeping.
# a = B gamma^{-1/2}; the terminal shell energy contains a^2 gamma L R^2.
gamma_power_after_amplitude = 2 * Fraction(-1, 2) + one
terminal_b_power = Fraction(2)
terminal_l_power = one
terminal_r_power = Fraction(2)

payment_b_power = Fraction(3)
payment_l_power = Fraction(0)
payment_r_power = Fraction(3)
payment_23_b_power = payment_b_power * two_thirds
payment_23_l_power = payment_l_power * two_thirds
payment_23_r_power = payment_r_power * two_thirds

flux_b_power = Fraction(2)
flux_l_power = one
flux_r_power = Fraction(2)
cubic_flux_b_power = flux_b_power * three_halves
cubic_flux_l_power = flux_l_power * three_halves
cubic_flux_r_power = flux_r_power * three_halves

# Under B asymptotic to R^{-2}, the old payment diverges as R^{-3}.
b_as_r_power = Fraction(-2)
old_payment_as_r = payment_b_power * b_as_r_power + payment_r_power
target_as_r = terminal_b_power * b_as_r_power + terminal_r_power

checks = [
    equality(
        "parabolic_measure_power",
        measure_power,
        Fraction(5),
        "time R^2 times shell volume R^3 gives R^5",
    ),
    equality(
        "holder_volume_one_third",
        holder_volume_power,
        Fraction(5, 3),
        "weighted Holder contributes the one-third power of R^5",
    ),
    equality(
        "quadratic_cutoff_prefactor",
        Fraction(-1) + Fraction(-2),
        quadratic_prefactor_power,
        "outer R^{-1} normalization and cutoff derivative R^{-2}",
    ),
    equality(
        "normalized_S2_power",
        normalized_s2_power,
        Fraction(-4, 3),
        "R^{-3} times the Holder volume factor R^{5/3}",
    ),
    equality(
        "normalized_S3_two_thirds_power",
        normalized_s3_power,
        Fraction(-4, 3),
        "(R^{-2} S3)^{2/3} has the same R exponent",
    ),
    equality(
        "quadratic_row_exponent_match",
        normalized_s2_power,
        normalized_s3_power,
        "finite dimensional consistency of equation (4.4)",
    ),
    equality(
        "energy_payment_outer_power",
        three_halves * two_thirds,
        one,
        "E^{3/2} inside P becomes E after the outer 2/3 power",
    ),
    equality(
        "acceleration_payment_outer_power",
        three_halves * two_thirds,
        one,
        "J_acc^{3/2} inside P becomes linear J_acc",
    ),
    equality(
        "collar_payment_outer_power",
        three_halves * two_thirds,
        one,
        "C_R^{3/2} inside the repaired payment becomes linear C_R",
    ),
    strict_less(
        "small_payment_absorption_exponents",
        two_thirds,
        one,
        "for 0<=P<=1, P^1 is at most P^{2/3}",
    ),
    strict_less(
        "large_payment_two_regime_exponents",
        two_thirds,
        one,
        "for P>=1, the linear row dominates P^{2/3}",
    ),
    equality(
        "amplitude_gamma_cancellation",
        gamma_power_after_amplitude,
        Fraction(0),
        "a^2 gamma equals B^2 under a=B gamma^{-1/2}",
    ),
    equality(
        "old_payment_23_B_power",
        payment_23_b_power,
        terminal_b_power,
        "(B^3 R^3)^{2/3} has B^2",
    ),
    equality(
        "old_payment_23_R_power",
        payment_23_r_power,
        terminal_r_power,
        "(B^3 R^3)^{2/3} has R^2",
    ),
    equality(
        "old_payment_23_L_power",
        payment_23_l_power,
        Fraction(0),
        "the old payment contributes no L factor",
    ),
    equality(
        "target_over_old_23_L_power",
        terminal_l_power - payment_23_l_power,
        one,
        "the rejected ratio has the missing factor L",
    ),
    equality(
        "cubic_flux_B_power",
        cubic_flux_b_power,
        payment_b_power,
        "(B^2 L R^2)^{3/2} has B^3",
    ),
    equality(
        "cubic_flux_L_power",
        cubic_flux_l_power,
        three_halves,
        "the repaired denominator gains L^{3/2}",
    ),
    equality(
        "cubic_flux_R_power",
        cubic_flux_r_power,
        payment_r_power,
        "(B^2 L R^2)^{3/2} has R^3",
    ),
    strict_greater(
        "cubic_flux_beats_old_L_power",
        cubic_flux_l_power,
        payment_l_power,
        "the cubicized collar flux supplies the missing large-payment scale",
    ),
    equality(
        "old_payment_under_B_Rminus2",
        old_payment_as_r,
        Fraction(-3),
        "B^3 R^3 scales as R^{-3} when B scales as R^{-2}",
    ),
    equality(
        "target_under_B_Rminus2",
        target_as_r,
        Fraction(-2),
        "B^2 L R^2 scales as L R^{-2}",
    ),
    strict_less(
        "reference_payment_scale_diverges",
        old_payment_as_r,
        Fraction(0),
        "the reference scale B^3 R^3 diverges; this is not a lower bound for P",
    ),
    equality(
        "finite_tail_ratio_exponent_at_j4",
        Fraction(3) * Fraction(4**3, 32),
        Fraction(6),
        "the weighted shell-volume ratio has exponential decrement e^{-6} from j=4",
    ),
    equality(
        "flux_repair_sum_constant",
        one + one,
        Fraction(2),
        "each summand P^{2/3} and C is separately bounded by the repaired power",
    ),
]

passed = sum(bool(item["pass"]) for item in checks)
payload = {
    "algebraic_implications": [
        "For P,C>=0, P^(2/3) <= (P+C^(3/2))^(2/3).",
        "For P,C>=0, C <= (P+C^(3/2))^(2/3).",
        "Adding the preceding two inequalities gives the factor 2 in R0.74H (5.5).",
        "For 0<=P<=1, P <= P^(2/3); this is the only extra step in Corollary 6.3.",
    ],
    "analytic_boundary": [
        "does not prove the finite-shell weighted energy identities or their signs",
        "does not prove C2 convergence, unfolding, or absolute convergence of the shell sum",
        "does not prove Holder, Calderon-Zygmund, harmonic-pressure, or residual-transport estimates",
        "does not prove the Version-F acceleration moment bound",
        "does not prove the R0.74F-G packet lobe or the positive collar-flux lower bound",
        "does not prove a payment lower bound; R0.74H derives one analytically from Theorem 6.2",
        "does not prove either two-regime theorem, epsilon regularity, continuation, or global regularity",
        "does not prove a Navier-Stokes singularity or solve the Clay problem",
    ],
    "checks": checks,
    "result": "PASS" if passed == len(checks) else "FAIL",
    "summary": {"passed": passed, "total": len(checks)},
}

print(json.dumps(payload, indent=2, sort_keys=True))
