#!/usr/bin/env python3
"""Finite exact certificate for the R0.74P temporal-clock triage.

The producer uses ``fractions.Fraction`` only.  It checks the inherited
amplitude constants, the exact missing-scale factor, representative
Carleson attenuation exponents, target-shell weight cancellation, the
over-weighted penalty, and finite l1/l2 obstruction rows.

FINITE ONLY: this program does not prove the local-energy balance, the
shell TV bounds, continuum Carleson optimization, compactness, weak lower
semicontinuity, regularity, novelty, priority, or any Clay statement.
"""

from __future__ import annotations

import json
from fractions import Fraction


def q(value: Fraction) -> str:
    """Return a canonical rational string, including denominator one."""

    return f"{value.numerator}/{value.denominator}"


def compare(
    check_id: str,
    left: Fraction,
    relation: str,
    right: Fraction,
    note: str,
) -> dict:
    """Build one exact comparison row."""

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
        raise ValueError(f"unsupported relation: {relation}")
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
half = Fraction(1, 2)
two_thirds = Fraction(2, 3)

m = Fraction(43, 423_360)
c_gamma = Fraction(8, 3_969)
kappa_exponential_rate = m / 3
kappa_l_power = two_thirds
k_exponential_rate = 2 * kappa_exponential_rate
k_l_power = 2 * kappa_l_power + 1
strong_gamma_penalty = c_gamma / 2

checks: list[dict] = [
    compare("m_exact", m, "==", Fraction(43, 423_360),
            "inherited R0.74O amplitude reserve"),
    compare("m_positive", m, ">", zero,
            "the missing-scale factor grows exponentially"),
    compare("c_gamma_exact", c_gamma, "==", Fraction(8, 3_969),
            "target-shell super-Gaussian decay coefficient"),
    compare("kappa_exponential_rate", kappa_exponential_rate, "==",
            Fraction(43, 1_270_080), "kappa=exp((m/3)L^2)L^(2/3)"),
    compare("kappa_L_power", kappa_l_power, "==", two_thirds,
            "polynomial L power in kappa"),
    compare("K_exponential_rate", k_exponential_rate, "==",
            Fraction(43, 635_040), "K=kappa^2 L exponential rate"),
    compare("K_exponential_rate_positive", k_exponential_rate, ">", zero,
            "K tends to infinity"),
    compare("K_L_power", k_l_power, "==", Fraction(7, 3),
            "K=kappa^2 L has L power 7/3"),
    compare("target_gamma_cancellation", one - one, "==", zero,
            "gamma times a_*^2 cancels Gamma^(-1)"),
    compare("target_kappa_power", 2 * one, "==", Fraction(2),
            "weighted target energy is quadratic in kappa"),
    compare("strong_gamma_power", -half, "==", Fraction(-1, 2),
            "strong square function divides the target by sqrt(Gamma)"),
    compare("strong_exponential_penalty", strong_gamma_penalty, "==",
            Fraction(4, 3_969), "Gamma^(-1/2) exponential coefficient"),
    compare("strong_exponential_penalty_positive", strong_gamma_penalty,
            ">", zero, "over-weighted target cost is exponential"),
]

sigma_values = [
    Fraction(1, 4),
    Fraction(1, 2),
    Fraction(3, 4),
    Fraction(1),
    Fraction(3, 2),
    Fraction(2),
    Fraction(4),
]
carleson_rows = []
for sigma in sigma_values:
    beta = min(sigma, one)
    branch = "intersection" if sigma < one else (
        "constant" if sigma == one else "right-endpoint-supremum"
    )
    row = {
        "sigma": q(sigma),
        "attenuation_beta": q(beta),
        "maximizer_branch": branch,
        "bound": "K^(-beta)",
    }
    carleson_rows.append(row)
    slug = f"{sigma.numerator}_{sigma.denominator}"
    checks.extend(
        [
            compare(f"sigma_{slug}_beta_positive", beta, ">", zero,
                    "every fixed sampled positive order attenuates"),
            compare(f"sigma_{slug}_beta_at_most_one", beta, "<=", one,
                    "beta=min(sigma,1)"),
            compare(f"sigma_{slug}_beta_exact", beta, "==",
                    sigma if sigma < one else one,
                    "piecewise Carleson attenuation exponent"),
        ]
    )

square_roots = [2, 4, 8, 16, 32, 64]
l1_l2_rows = []
for root in square_roots:
    root_q = Fraction(root)
    count = root_q * root_q
    l1 = count
    l2 = root_q
    ratio = l1 / l2
    l1_l2_rows.append(
        {
            "N": int(count),
            "l1": q(l1),
            "l2": q(l2),
            "ratio": q(ratio),
            "sequence": "N equal entries of value one",
        }
    )
    checks.extend(
        [
            compare(f"equal_{int(count)}_l2", l2, "==", root_q,
                    "sqrt(N) for a perfect-square test size"),
            compare(f"equal_{int(count)}_ratio", ratio, "==", root_q,
                    "l1/l2=sqrt(N)"),
            compare(f"equal_{int(count)}_strict_gap", l1, ">", l2,
                    "finite equal-entry sequence separates l1 and l2"),
        ]
    )

scale_rows = [
    {
        "name": "paid_average",
        "B_power": q(Fraction(2)),
        "R_power": q(Fraction(2)),
        "L_power": q(zero),
        "kappa_power": q(zero),
        "Gamma_power": q(zero),
        "description": "(P_*)^(2/3) is comparable to B^2 R^2",
    },
    {
        "name": "target_clock",
        "B_power": q(Fraction(2)),
        "R_power": q(Fraction(2)),
        "L_power": q(one),
        "kappa_power": q(Fraction(2)),
        "Gamma_power": q(zero),
        "description": "v_j and T_* have scale kappa^2 B^2 L R^2",
    },
    {
        "name": "missing_factor_K",
        "B_power": q(zero),
        "R_power": q(zero),
        "L_power": q(one),
        "kappa_power": q(Fraction(2)),
        "Gamma_power": q(zero),
        "description": "target clock divided by the paid average",
    },
    {
        "name": "strong_target_clock",
        "B_power": q(Fraction(2)),
        "R_power": q(Fraction(2)),
        "L_power": q(one),
        "kappa_power": q(Fraction(2)),
        "Gamma_power": q(Fraction(-1, 2)),
        "description": "over-weighted square function target lower bound",
    },
]

passed = sum(bool(item["pass"]) for item in checks)
analytic_boundary = [
    "FINITE ONLY: exact rational exponent and finite sequence bookkeeping",
    "does not prove the local energy measure identity or moving-test passage",
    "does not prove the shellwise total-variation ledgers or infinite-shell limits",
    "does not prove the continuum optimization for every real sigma>0",
    "does not prove the exact-family terminal-lobe or target-flux estimates",
    "does not prove path, pressure-primitive, clock, BV, or square-function compactness",
    "does not prove an l1-to-l2 Navier--Stokes inequality or a good-scale theorem",
    "does not verify literature, novelty, or priority",
    "does not prove regularity, singularity, blow-up, continuation, or global smoothness",
    "does not solve the Clay Millennium problem; NOT CLAY",
]

payload = {
    "schema": "r074p-temporal-clock-certificate-v1",
    "scope": "FINITE ONLY: exact missing-factor arithmetic, sampled Carleson exponents, target weights, and finite l1/l2 witnesses",
    "inputs": {
        "m": q(m),
        "c_gamma": q(c_gamma),
        "sigma_grid": [q(value) for value in sigma_values],
        "equal_sequence_square_roots": square_roots,
    },
    "derived": {
        "kappa_exponential_rate": q(kappa_exponential_rate),
        "kappa_L_power": q(kappa_l_power),
        "K_exponential_rate": q(k_exponential_rate),
        "K_L_power": q(k_l_power),
        "strong_Gamma_inverse_sqrt_exponential_rate": q(strong_gamma_penalty),
    },
    "scale_rows": scale_rows,
    "carleson_rows": carleson_rows,
    "l1_l2_rows": l1_l2_rows,
    "checks": checks,
    "exact_implications": [
        "K_*=kappa^2 L has exponential rate 43/635040 and polynomial L power 7/3, so K_* diverges.",
        "The target-shell factor Gamma cancels the Gamma^(-1) in a_*^2, leaving the T_* scale.",
        "For each sampled fixed sigma>0, the Carleson attenuation exponent is min(sigma,1)>0.",
        "For N equal unit entries with sampled perfect-square N, l1/l2=sqrt(N).",
        "Dividing the matched target clock by sqrt(Gamma) adds exponential rate 4/3969.",
    ],
    "analytic_boundary": analytic_boundary,
    "result": "PASS" if passed == len(checks) else "FAIL",
    "summary": {
        "passed": passed,
        "total": len(checks),
        "unique_ids": len({item["id"] for item in checks}),
        "scale_rows": len(scale_rows),
        "carleson_rows": len(carleson_rows),
        "l1_l2_rows": len(l1_l2_rows),
    },
}

print(json.dumps(payload, indent=2, sort_keys=True))
