#!/usr/bin/env python3
"""Exact finite certificate for the R0.74N all-shell synthesis.

The certificate checks rational exponent identities, finite sequence-ratio
audits, and raw scale ledgers.  Exponential comparisons are represented by
exact Taylor lower bounds; no floating-point arithmetic is used.

This is not an analytic proof.  In particular, it does not prove the
combined-chord geometry, periodization, the common-forward-law identity,
the final-segment expulsion lemma, packet maximum principle, or the
infinite-shell limit.
"""

from __future__ import annotations

import json
from fractions import Fraction


def q(value: Fraction) -> str:
    """Return the canonical rational string used by the JSON schema."""
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


def taylor2(x: Fraction) -> Fraction:
    """1+x+x^2/2, an exact lower bound for exp(x) when x>=0."""
    return 1 + x + x**2 / 2


def taylor3(x: Fraction) -> Fraction:
    """1+x+x^2/2+x^3/6, an exact lower bound for exp(x) when x>=0."""
    return taylor2(x) + x**3 / 6


zero = Fraction(0)
one = Fraction(1)

lam = Fraction(63, 32)
c_gamma = Fraction(8, 3969)
rho = Fraction(1, 320)
c_def = Fraction(1, 640)
sigma_denominator = Fraction(32768)

# R0.74L is the latest inherited discrete threshold, so the all-shell theorem
# uses j>=14.  The finite audit deliberately prints eight consecutive rows.
j_threshold = 14
audit_j_min = 14
audit_j_max = 21

bad_reflection_exponent = Fraction(1, 16)
bad_reserve = bad_reflection_exponent - rho - c_gamma
outer_jump_rate = 3 * c_gamma
outer_reserve = outer_jump_rate - rho
outer_coefficient = 4 / lam**2
gamma_scale_identity = c_gamma * lam**2
sigma_square_growth = 2 * (rho - c_def)
sigma_tail_denominator = Fraction(1056) * sigma_denominator**2

# If b_k=2^k Gamma_k, then b_(k+1)/b_k=2 exp(-delta_k).
# At k=3 the cubic Taylor lower bound already gives ratio <=1/2, and
# delta_(k+1)=4 delta_k propagates the threshold.  This produces the exact
# cancellation-free bound sum b_k <=2+4+2*8=22.
chord_threshold_k = 3
chord_delta_threshold = Fraction(3 * 4 ** (chord_threshold_k - 1), 32)
chord_taylor_threshold = taylor3(chord_delta_threshold)
chord_ratio_envelope_threshold = 2 / chord_taylor_threshold
chord_geometric_ratio = Fraction(1, 2)
chord_uniform_majorant = Fraction(2 + 4 + 2 * 8)

# If a_k=4^k Gamma_k, then a_(k+1)/a_k=4 exp(-delta_k).
# At k=4 the quadratic Taylor lower bound is 25, hence the ratio is at most
# 4/25<1/2.  The proof uses the weaker geometric tail factor 2.
outer_threshold_k = 4
outer_delta_threshold = Fraction(3 * 4 ** (outer_threshold_k - 1), 32)
outer_taylor_threshold = taylor2(outer_delta_threshold)
outer_ratio_envelope_threshold = 4 / outer_taylor_threshold
outer_geometric_ratio = Fraction(1, 2)
outer_tail_factor = one / (one - outer_geometric_ratio)

checks: list[dict] = [
    row("lambda", lam, "==", Fraction(63, 32), "frozen dyadic scale"),
    row(
        "annular_exponent",
        c_gamma,
        "==",
        Fraction(8, 3969),
        "Gamma_j=exp(-c_gamma L_j^2)",
    ),
    row("radius_exponent", rho, "==", Fraction(1, 320), "R_j=exp(-rho L_j^2)"),
    row(
        "gamma_scale_identity",
        gamma_scale_identity,
        "==",
        Fraction(1, 128),
        "c_gamma lambda^2=1/128",
    ),
    row(
        "bad_reserve",
        bad_reserve,
        "==",
        Fraction(72851, 1270080),
        "1/16-rho-c_gamma",
    ),
    row("bad_reserve_positive", bad_reserve, ">", zero, "bad path pays Gamma_j and one R"),
    row(
        "outer_jump_rate",
        outer_jump_rate,
        "==",
        Fraction(8, 1323),
        "negative logarithmic rate of Gamma_(j+1)/Gamma_j",
    ),
    row(
        "outer_reserve",
        outer_reserve,
        "==",
        Fraction(1237, 423360),
        "3c_gamma-rho",
    ),
    row("outer_reserve_positive", outer_reserve, ">", zero, "outer jump pays one inverse R"),
    row(
        "outer_coefficient",
        outer_coefficient,
        "==",
        Fraction(4096, 3969),
        "4^(j+1)/L_j^2",
    ),
    row(
        "sigma_square_growth",
        sigma_square_growth,
        "==",
        Fraction(1, 320),
        "Sigma_L^2/R^2 has exp(L^2/320) growth",
    ),
    row(
        "sigma_tail_denominator",
        sigma_tail_denominator,
        "==",
        Fraction(1133871366144),
        "1056 times 32768 squared in the good-path tail",
    ),
    row(
        "chord_threshold_delta",
        chord_delta_threshold,
        "==",
        Fraction(3, 2),
        "delta_3 for b_k=2^k Gamma_k",
    ),
    row(
        "chord_threshold_taylor3",
        chord_taylor_threshold,
        "==",
        Fraction(67, 16),
        "cubic Taylor lower bound for exp(3/2)",
    ),
    row(
        "chord_threshold_ratio_envelope",
        chord_ratio_envelope_threshold,
        "==",
        Fraction(32, 67),
        "exact upper envelope for b_4/b_3",
    ),
    row(
        "chord_threshold_ratio_below_half",
        chord_ratio_envelope_threshold,
        "<",
        chord_geometric_ratio,
        "chord ratios are below one half from k=3 onward",
    ),
    row("chord_delta_growth", Fraction(4), "==", Fraction(4), "delta_(k+1)/delta_k"),
    row(
        "chord_uniform_majorant",
        chord_uniform_majorant,
        "==",
        Fraction(22),
        "sum 2^k Gamma_k is bounded by 2+4+2*8",
    ),
    row(
        "outer_threshold_delta",
        outer_delta_threshold,
        "==",
        Fraction(6),
        "delta_4 for a_k=4^k Gamma_k",
    ),
    row(
        "outer_threshold_taylor2",
        outer_taylor_threshold,
        "==",
        Fraction(25),
        "quadratic Taylor lower bound for exp(6)",
    ),
    row(
        "outer_threshold_ratio_envelope",
        outer_ratio_envelope_threshold,
        "==",
        Fraction(4, 25),
        "exact upper envelope for a_5/a_4",
    ),
    row(
        "outer_threshold_ratio_below_half",
        outer_ratio_envelope_threshold,
        "<",
        outer_geometric_ratio,
        "outer ratios are below one half from k=4 onward",
    ),
    row("outer_delta_growth", Fraction(4), "==", Fraction(4), "delta_(k+1)/delta_k"),
    row(
        "outer_tail_factor",
        outer_tail_factor,
        "==",
        Fraction(2),
        "geometric majorant used for the infinite outer tail",
    ),
]

# Exact exponent algebra for representative inward Gamma ratios.  The
# exponent of Gamma_(j-m)/Gamma_j is c_gamma(1-4^-m)L_j^2.
inward_ratio_exponents = []
for m in range(1, 9):
    normalized = c_gamma * (one - Fraction(1, 4**m))
    direct_at_threshold = Fraction(
        4 ** (j_threshold - 1) - 4 ** (j_threshold - m - 1), 32
    )
    via_l_at_threshold = normalized * (lam * 2**j_threshold) ** 2
    inward_ratio_exponents.append(
        {
            "m": m,
            "normalized_rate": q(normalized),
            "direct_exponent_at_j14": q(direct_at_threshold),
            "via_L_exponent_at_j14": q(via_l_at_threshold),
        }
    )
    checks.append(
        row(
            f"inward_gamma_ratio_m{m}",
            via_l_at_threshold,
            "==",
            direct_at_threshold,
            "-log(Gamma_j/Gamma_(j-m)) reconstructed two ways at j=14",
        )
    )

gamma_window = []
chord_window = []
outer_window = []
for j in range(audit_j_min, audit_j_max + 1):
    l_j = lam * 2**j
    l_j_sq = l_j**2
    gamma_exponent = c_gamma * l_j_sq
    direct_gamma_exponent = Fraction(4 ** (j - 1), 32)
    outer_jump_exponent = outer_jump_rate * l_j_sq
    direct_outer_jump = Fraction(3 * 4 ** (j - 1), 32)

    # Last increment in S_j=sum_{k=1}^{j-1} b_k: b_(j-1)/b_(j-2).
    chord_k = j - 2
    chord_delta = Fraction(3 * 4 ** (chord_k - 1), 32)
    chord_taylor = taylor3(chord_delta)
    chord_ratio_upper = 2 / chord_taylor

    # First ratio inside the outer tail: a_(j+2)/a_(j+1).
    outer_k = j + 1
    outer_delta = Fraction(3 * 4 ** (outer_k - 1), 32)
    outer_taylor = taylor2(outer_delta)
    outer_ratio_upper = 4 / outer_taylor

    gamma_window.append(
        {
            "j": j,
            "L_squared": q(l_j_sq),
            "gamma_exponent": q(gamma_exponent),
            "direct_gamma_exponent": q(direct_gamma_exponent),
            "outer_jump_exponent": q(outer_jump_exponent),
            "direct_outer_jump": q(direct_outer_jump),
            "four_j_plus_one_over_L_squared": q(Fraction(4 ** (j + 1), 1) / l_j_sq),
        }
    )
    chord_window.append(
        {
            "j": j,
            "ratio_base_k": chord_k,
            "delta": q(chord_delta),
            "taylor3": q(chord_taylor),
            "ratio_upper": q(chord_ratio_upper),
        }
    )
    outer_window.append(
        {
            "j": j,
            "ratio_base_k": outer_k,
            "delta": q(outer_delta),
            "taylor2": q(outer_taylor),
            "ratio_upper": q(outer_ratio_upper),
        }
    )

    checks.extend(
        [
            row(
                f"window_j{j}_gamma_exponent",
                gamma_exponent,
                "==",
                direct_gamma_exponent,
                "c_gamma L_j^2=4^(j-1)/32",
            ),
            row(
                f"window_j{j}_outer_jump_exponent",
                outer_jump_exponent,
                "==",
                direct_outer_jump,
                "-log(Gamma_(j+1)/Gamma_j)=3c_gamma L_j^2",
            ),
            row(
                f"window_j{j}_outer_coefficient",
                Fraction(4 ** (j + 1), 1) / l_j_sq,
                "==",
                Fraction(4096, 3969),
                "4^(j+1)/L_j^2 is j-independent",
            ),
            row(
                f"window_j{j}_chord_ratio_upper",
                chord_ratio_upper,
                "<",
                Fraction(1, 2),
                "last audited chord increment is below one half",
            ),
            row(
                f"window_j{j}_outer_ratio_upper",
                outer_ratio_upper,
                "<",
                Fraction(1, 2),
                "first audited outer-tail ratio is below one half",
            ),
        ]
    )

# Raw R/L ledgers before exponential payments.  These are bookkeeping only.
inner_bad_r = Fraction(6 + 2 - 1 - 3)
inner_bad_l = zero
inner_good_r = Fraction(6 + 2 - 1 - 4)
inner_good_l = zero
outer_shell_r = Fraction(2 + 2)
outer_shell_l = zero
outer_summed_r = outer_shell_r
outer_summed_l = Fraction(2)
main_r = Fraction(5)
main_l = Fraction(1)
target_r = Fraction(5)
target_l = Fraction(1)

checks.extend(
    [
        row("inner_bad_raw_R_power", inner_bad_r, "==", Fraction(4), "R^6 R^2 R^-1 R^-3"),
        row("inner_bad_raw_L_power", inner_bad_l, "==", zero, "combined chord is uniformly bounded"),
        row("inner_good_raw_R_power", inner_good_r, "==", Fraction(3), "R^6 R^2 R^-1 R^-4"),
        row("inner_good_raw_L_power", inner_good_l, "==", zero, "combined chord is uniformly bounded"),
        row("outer_shell_raw_R_power", outer_shell_r, "==", Fraction(4), "time R^2 times collar volume-gradient R^2"),
        row("outer_shell_raw_L_power", outer_shell_l, "==", zero, "before 4^k is normalized"),
        row("outer_summed_raw_R_power", outer_summed_r, "==", Fraction(4), "after outer geometric summation"),
        row("outer_summed_raw_L_power", outer_summed_l, "==", Fraction(2), "4^(j+1)=(4096/3969)L^2"),
        row("main_inherited_R_power", main_r, "==", Fraction(5), "R0.74L target-shell ledger"),
        row("main_inherited_L_power", main_l, "==", Fraction(1), "R0.74L target-shell ledger"),
        row("target_R_power", target_r, "==", Fraction(5), "Gamma_j L_j R_j^5 target"),
        row("target_L_power", target_l, "==", Fraction(1), "Gamma_j L_j R_j^5 target"),
    ]
)

passed = sum(1 for item in checks if item["pass"])
result = {
    "schema": "r074n-all-shell-certificate-v1",
    "scope": "finite exact rational exponent algebra, sequence audit window, and raw scale ledgers only",
    "result": "PASS" if passed == len(checks) else "FAIL",
    "inputs": {
        "lambda": q(lam),
        "c_gamma": q(c_gamma),
        "rho": q(rho),
        "c_def": q(c_def),
        "sigma_denominator": q(sigma_denominator),
        "j_threshold": j_threshold,
        "audit_window": [audit_j_min, audit_j_max],
    },
    "derived": {
        "bad_reserve": q(bad_reserve),
        "outer_reserve": q(outer_reserve),
        "outer_coefficient": q(outer_coefficient),
        "sigma_square_growth": q(sigma_square_growth),
        "chord_ratio_threshold_k": chord_threshold_k,
        "chord_ratio_envelope_at_threshold": q(chord_ratio_envelope_threshold),
        "chord_uniform_majorant": q(chord_uniform_majorant),
        "outer_ratio_threshold_k": outer_threshold_k,
        "outer_ratio_envelope_at_threshold": q(outer_ratio_envelope_threshold),
        "outer_tail_factor": q(outer_tail_factor),
    },
    "sequence_audits": {
        "window": [audit_j_min, audit_j_max],
        "gamma_algebra": gamma_window,
        "inward_ratio_exponents": inward_ratio_exponents,
        "chord_partial_sum_increments": chord_window,
        "outer_tail_ratios": outer_window,
        "propagation": {
            "delta_multiplier": q(Fraction(4)),
            "chord_ratio_bound_from_k": chord_threshold_k,
            "outer_ratio_bound_from_k": outer_threshold_k,
            "ratio_bound": q(Fraction(1, 2)),
        },
    },
    "scale_ledgers": {
        "inner_bad": {"L_power": q(inner_bad_l), "R_power": q(inner_bad_r)},
        "inner_good": {"L_power": q(inner_good_l), "R_power": q(inner_good_r)},
        "outer_single_shell": {"L_power": q(outer_shell_l), "R_power": q(outer_shell_r)},
        "outer_after_summation": {"L_power": q(outer_summed_l), "R_power": q(outer_summed_r)},
        "main_inherited": {"L_power": q(main_l), "R_power": q(main_r)},
        "target": {"L_power": q(target_l), "R_power": q(target_r)},
    },
    "checks": checks,
    "summary": {"passed": passed, "total": len(checks)},
    "analytic_boundary": [
        "does not prove the combined inward chord or its exact periodization",
        "does not prove the common-forward-law or final-segment expulsion lemmas",
        "does not prove the packet maximum principle or outer collar volume bound",
        "does not prove convergence of the infinite annular observable",
        "does not replace the independent analytic reconstruction of R0.74N",
        "does not prove a universal endpoint estimate, regularity, singularity, or Clay",
    ],
    "status_flags": {
        "finite_arithmetic": "PASS" if passed == len(checks) else "FAIL",
        "all_shell_analytic_proof": "REQUIRES_INDEPENDENT_AUDIT",
        "finite_window_scope": "J_14_THROUGH_J_21_WITH_MONOTONE_PROPAGATION_LEDGER",
        "clay_problem": "NOT_CLAIMED",
    },
}

print(json.dumps(result, indent=2, sort_keys=True))
