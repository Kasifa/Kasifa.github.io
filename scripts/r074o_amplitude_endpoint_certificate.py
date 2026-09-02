#!/usr/bin/env python3
"""Exact finite certificate for the R0.74O amplitude-endpoint ledger.

The producer uses :class:\`fractions.Fraction\` exclusively.  It checks the
frozen rational constants, the exact amplitude exponent cancellation, raw
scale ledgers, an eight-index exponent window, monotone factor-four
propagation, and a finite polynomial-amplitude sample grid.

FINITE ONLY: this program does not prove any packet, energy, occupation,
collar-flux, endpoint, Navier--Stokes, novelty, priority, or Clay statement.
"""

from __future__ import annotations

import json
from fractions import Fraction


def q(value: Fraction) -> str:
    """Return the canonical rational spelling, including denominator one."""

    return f"{value.numerator}/{value.denominator}"


def row(
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


def scale(
    name: str,
    b_power: Fraction,
    r_power: Fraction,
    l_power: Fraction,
    kappa_power: Fraction,
    gamma_power: Fraction,
    heat_decay: Fraction,
    note: str,
) -> dict:
    """Serialize one raw B/R/L/kappa/Gamma scale ledger."""

    return {
        "name": name,
        "B_power": q(b_power),
        "R_power": q(r_power),
        "L_power": q(l_power),
        "kappa_power": q(kappa_power),
        "Gamma_power": q(gamma_power),
        "heat_decay_coefficient": q(heat_decay),
        "note": note,
    }


zero = Fraction(0)
one = Fraction(1)
half = Fraction(1, 2)
two_thirds = Fraction(2, 3)
three_halves = Fraction(3, 2)

lam = Fraction(63, 32)
rho = Fraction(1, 320)
c_gamma = Fraction(8, 3969)
d_energy = Fraction(98, 29475)
e_energy = d_energy - c_gamma
m = rho - three_halves * c_gamma
energy_reserve = e_energy - two_thirds * m
delta = 2 * m / (9 * rho)
q_star = two_thirds + delta

# The exact exponential amplitude is
# kappa=exp((m/3)L^2)L^(2/3).  Only its exponent ledger is certified here.
kappa_exponential_rate = m / 3
kappa_l_power = two_thirds

audit_j_min = 14
audit_j_max = 21

checks: list[dict] = [
    row("lambda_exact", lam, "==", Fraction(63, 32), "frozen dyadic prefactor"),
    row("rho_exact", rho, "==", Fraction(1, 320), "R=exp(-rho L^2)"),
    row(
        "c_gamma_exact",
        c_gamma,
        "==",
        Fraction(8, 3969),
        "Gamma=exp(-c_gamma L^2)",
    ),
    row(
        "d_energy_exact",
        d_energy,
        "==",
        Fraction(98, 29475),
        "buffered packet-energy decay coefficient",
    ),
    row(
        "e_energy_definition",
        e_energy,
        "==",
        d_energy - c_gamma,
        "e_E=d_E-c_gamma",
    ),
    row(
        "e_energy_exact",
        e_energy,
        "==",
        Fraction(17018, 12998475),
        "exact packet-energy reserve before kappa",
    ),
    row(
        "m_definition",
        m,
        "==",
        rho - three_halves * c_gamma,
        "m=rho-3c_gamma/2",
    ),
    row(
        "m_exact",
        m,
        "==",
        Fraction(43, 423360),
        "exact cubic occupation reserve",
    ),
    row("m_positive", m, ">", zero, "the exponential amplitude rate is positive"),
    row(
        "energy_reserve_definition",
        energy_reserve,
        "==",
        e_energy - two_thirds * m,
        "energy reserve after the squared kappa amplitude",
    ),
    row(
        "energy_reserve_exact",
        energy_reserve,
        "==",
        Fraction(1171, 943200),
        "e_E-2m/3",
    ),
    row(
        "energy_reserve_positive",
        energy_reserve,
        ">",
        zero,
        "packet energy retains strict exponential decay",
    ),
    row(
        "delta_definition",
        delta,
        "==",
        2 * m / (9 * rho),
        "delta=2m/(9rho)",
    ),
    row(
        "delta_exact",
        delta,
        "==",
        Fraction(86, 11907),
        "exact payment-power increment",
    ),
    row("delta_positive", delta, ">", zero, "q_star lies above two thirds"),
    row(
        "q_star_definition",
        q_star,
        "==",
        two_thirds + delta,
        "q_star=2/3+delta",
    ),
    row(
        "q_star_exact",
        q_star,
        "==",
        Fraction(8024, 11907),
        "exact amplitude endpoint power",
    ),
    row("q_star_above_two_thirds", q_star, ">", two_thirds, "strict power lift"),
    row("q_star_below_one", q_star, "<", one, "the endpoint power stays sublinear"),
    row(
        "kappa_exponential_rate",
        kappa_exponential_rate,
        "==",
        Fraction(43, 1270080),
        "exp((m/3)L^2) rate",
    ),
    row(
        "kappa_polynomial_L_power",
        kappa_l_power,
        "==",
        two_thirds,
        "L^(2/3) factor in the exact exponential amplitude",
    ),
    row(
        "G_exponential_cancellation",
        3 * kappa_exponential_rate - rho + three_halves * c_gamma,
        "==",
        zero,
        "kappa^3 R Gamma^(-3/2) has zero L^2 exponent",
    ),
    row(
        "G_polynomial_cancellation",
        3 * kappa_l_power - 2,
        "==",
        zero,
        "kappa^3 L^-2 has zero L power",
    ),
    row(
        "H_polynomial_power",
        3 * kappa_l_power - Fraction(7, 2),
        "==",
        Fraction(-3, 2),
        "the harmonic packet ratio retains L^-3/2",
    ),
    row(
        "energy_polynomial_power",
        2 * kappa_l_power,
        "==",
        Fraction(4, 3),
        "the squared amplitude contributes L^(4/3)",
    ),
    row(
        "observable_polynomial_power",
        2 * kappa_l_power + 1,
        "==",
        Fraction(7, 3),
        "collar and X observables carry kappa^2 L",
    ),
    row(
        "observable_log_power",
        (2 * kappa_l_power + 1) / 2,
        "==",
        Fraction(7, 6),
        "log P is proportional to L^2",
    ),
    row(
        "sqrt_log_L_power",
        2 * half,
        "==",
        one,
        "sqrt(log P) contributes one L power",
    ),
    row(
        "endpoint_ratio_L_power",
        2 * kappa_l_power + 1 - 1,
        "==",
        Fraction(4, 3),
        "ratio to the square-root-log comparator",
    ),
    row(
        "endpoint_ratio_log_power",
        (2 * kappa_l_power + 1 - 1) / 2,
        "==",
        Fraction(2, 3),
        "L^(4/3) equals (log P)^(2/3)",
    ),
    row(
        "payment_growth_coefficient",
        3 * rho,
        "==",
        Fraction(3, 320),
        "B R^2 asymptotically constant makes B^3R^3 grow like exp(3rho L^2)",
    ),
    row(
        "observable_growth_coefficient",
        2 * rho + 2 * kappa_exponential_rate,
        "==",
        Fraction(1003, 158760),
        "kappa^2 B^2 L R^2 exponential coefficient",
    ),
    row(
        "delta_payment_match",
        3 * rho * delta,
        "==",
        two_thirds * m,
        "P^delta supplies exactly exp((2m/3)L^2)",
    ),
    row(
        "q_star_exponential_match",
        3 * rho * q_star,
        "==",
        2 * rho + 2 * kappa_exponential_rate,
        "P^q_star matches the observable exponential rate",
    ),
    row(
        "calibrated_payment_R_power",
        -2 * 3 + 3,
        "==",
        Fraction(-3),
        "B~R^-2 sends B^3R^3 to R^-3",
    ),
    row(
        "calibrated_observable_R_power",
        -2 * 2 + 2,
        "==",
        Fraction(-2),
        "B~R^-2 sends B^2R^2 to R^-2 before kappa",
    ),
]

scale_ledgers = [
    scale(
        "E_shear",
        Fraction(2),
        Fraction(2),
        zero,
        zero,
        zero,
        zero,
        "background buffered energy B^2 R^2",
    ),
    scale(
        "E_packet",
        Fraction(2),
        Fraction(2),
        zero,
        Fraction(2),
        Fraction(-1),
        -d_energy,
        "a^2 R^2 exp(-d_E L^2) after a=kappa B Gamma^-1/2",
    ),
    scale(
        "G_shear",
        Fraction(3),
        Fraction(3),
        zero,
        zero,
        zero,
        zero,
        "background cubic row B^3 R^3",
    ),
    scale(
        "G_packet",
        Fraction(3),
        Fraction(4),
        Fraction(-2),
        Fraction(3),
        Fraction(-3, 2),
        zero,
        "packet cubic row kappa^3 B^3 Gamma^-3/2 R^4 L^-2",
    ),
    scale(
        "H_shear",
        Fraction(3),
        Fraction(3),
        zero,
        zero,
        zero,
        zero,
        "background harmonic row B^3 R^3",
    ),
    scale(
        "H_packet",
        Fraction(3),
        Fraction(4),
        Fraction(-7, 2),
        Fraction(3),
        Fraction(-3, 2),
        zero,
        "packet harmonic row kappa^3 B^3 Gamma^-3/2 R^4 L^-7/2",
    ),
    scale(
        "P",
        Fraction(3),
        Fraction(3),
        zero,
        zero,
        zero,
        zero,
        "complete payment scale B^3 R^3 after analytic absorption",
    ),
    scale(
        "C",
        Fraction(2),
        Fraction(2),
        one,
        Fraction(2),
        zero,
        zero,
        "collar observable a^2 Gamma L R^2 after amplitude substitution",
    ),
    scale(
        "X",
        Fraction(2),
        Fraction(2),
        one,
        Fraction(2),
        zero,
        zero,
        "exterior observable a^2 Gamma L R^2 after amplitude substitution",
    ),
]

# Every raw ledger coordinate gets a separately named exact check.
for entry in scale_ledgers:
    name = entry["name"]
    expected = {
        "E_shear": (2, 2, 0, 0, 0, 0),
        "E_packet": (2, 2, 0, 2, Fraction(-1), -d_energy),
        "G_shear": (3, 3, 0, 0, 0, 0),
        "G_packet": (3, 4, -2, 3, Fraction(-3, 2), 0),
        "H_shear": (3, 3, 0, 0, 0, 0),
        "H_packet": (3, 4, Fraction(-7, 2), 3, Fraction(-3, 2), 0),
        "P": (3, 3, 0, 0, 0, 0),
        "C": (2, 2, 1, 2, 0, 0),
        "X": (2, 2, 1, 2, 0, 0),
    }[name]
    labels = (
        "B_power",
        "R_power",
        "L_power",
        "kappa_power",
        "Gamma_power",
        "heat_decay_coefficient",
    )
    for label, value in zip(labels, expected):
        checks.append(
            row(
                f"scale_{name}_{label}",
                Fraction(entry[label].split("/")[0])
                / Fraction(entry[label].split("/")[1]),
                "==",
                Fraction(value),
                f"raw {name} {label} ledger",
            )
        )

checks.extend(
    [
        row(
            "E_packet_exponential_coefficient",
            2 * kappa_exponential_rate + c_gamma - d_energy,
            "==",
            -energy_reserve,
            "packet-to-shear energy ratio decays at the strict reserve",
        ),
        row(
            "E_packet_L_power_after_kappa",
            2 * kappa_l_power,
            "==",
            Fraction(4, 3),
            "energy ratio polynomial factor",
        ),
        row(
            "G_packet_R_power_relative_to_shear",
            4 - 3,
            "==",
            one,
            "one R remains before exponential-amplitude cancellation",
        ),
        row(
            "G_packet_L_power_after_kappa",
            -2 + 3 * kappa_l_power,
            "==",
            zero,
            "cubic packet matches the background polynomial scale",
        ),
        row(
            "H_packet_R_power_relative_to_shear",
            4 - 3,
            "==",
            one,
            "one R remains before exponential-amplitude cancellation",
        ),
        row(
            "H_packet_L_power_after_kappa",
            Fraction(-7, 2) + 3 * kappa_l_power,
            "==",
            Fraction(-3, 2),
            "harmonic packet is lower by L^-3/2",
        ),
        row(
            "C_Gamma_cancellation",
            -one + one,
            "==",
            zero,
            "a^2 contributes Gamma^-1 and the collar contributes Gamma",
        ),
        row(
            "X_Gamma_cancellation",
            -one + one,
            "==",
            zero,
            "a^2 contributes Gamma^-1 and the exterior lower bound contributes Gamma",
        ),
    ]
)

window_ledgers = []
for j in range(audit_j_min, audit_j_max + 1):
    l_squared = (lam * 2**j) ** 2
    gamma_decay = c_gamma * l_squared
    radius_decay = rho * l_squared
    kappa_exp = kappa_exponential_rate * l_squared
    kappa_cubed_exp = 3 * kappa_exp
    reserve_decay = energy_reserve * l_squared
    payment_growth = 3 * radius_decay
    observable_growth = (2 * rho + 2 * kappa_exponential_rate) * l_squared
    endpoint_growth = 3 * rho * q_star * l_squared
    window_ledgers.append(
        {
            "j": j,
            "L_squared": q(l_squared),
            "Gamma_decay_exponent": q(gamma_decay),
            "R_decay_exponent": q(radius_decay),
            "kappa_exponent": q(kappa_exp),
            "kappa_cubed_exponent": q(kappa_cubed_exp),
            "energy_reserve_exponent": q(reserve_decay),
            "payment_growth_exponent": q(payment_growth),
            "observable_growth_exponent": q(observable_growth),
            "endpoint_growth_exponent": q(endpoint_growth),
        }
    )
    checks.extend(
        [
            row(
                f"window_j{j}_L_squared",
                l_squared,
                "==",
                Fraction(3969, 1024) * 4**j,
                "exact dyadic L_j^2",
            ),
            row(
                f"window_j{j}_Gamma_decay",
                gamma_decay,
                "==",
                Fraction(4**j, 128),
                "c_gamma L_j^2",
            ),
            row(
                f"window_j{j}_R_decay",
                radius_decay,
                "==",
                Fraction(3969 * 4**j, 327680),
                "rho L_j^2",
            ),
            row(
                f"window_j{j}_kappa_cubed",
                kappa_cubed_exp,
                "==",
                m * l_squared,
                "three kappa exponential rates equal m L_j^2",
            ),
            row(
                f"window_j{j}_energy_reserve_positive",
                reserve_decay,
                ">",
                zero,
                "strict packet-energy decay at this audited index",
            ),
            row(
                f"window_j{j}_G_exponential_cancel",
                kappa_cubed_exp - radius_decay + three_halves * gamma_decay,
                "==",
                zero,
                "kappa^3 R Gamma^-3/2 cancellation at this index",
            ),
            row(
                f"window_j{j}_endpoint_growth_match",
                endpoint_growth,
                "==",
                observable_growth,
                "P^q_star and the observable have the same exponential rate",
            ),
        ]
    )

for left, right in zip(window_ledgers, window_ledgers[1:]):
    j = left["j"]
    for field in (
        "L_squared",
        "Gamma_decay_exponent",
        "R_decay_exponent",
        "kappa_exponent",
        "kappa_cubed_exponent",
        "energy_reserve_exponent",
        "payment_growth_exponent",
        "observable_growth_exponent",
        "endpoint_growth_exponent",
    ):
        left_value = Fraction(left[field])
        right_value = Fraction(right[field])
        checks.append(
            row(
                f"window_j{j}_to_j{j + 1}_{field}_factor",
                right_value,
                "==",
                4 * left_value,
                "all L^2 exponent ledgers propagate monotonically by factor four",
            )
        )

polynomial_choices = [
    (Fraction(-2), Fraction(0)),
    (Fraction(-1), Fraction(0)),
    (Fraction(0), Fraction(0)),
    (Fraction(1, 2), Fraction(1)),
    (Fraction(1), Fraction(1)),
    (Fraction(2), Fraction(2)),
    (Fraction(4), Fraction(4)),
]
polynomial_kappa_grid = []
for gamma, capital_m in polynomial_choices:
    threshold = gamma - half
    observable_l = 2 * capital_m + 1
    comparator_l = 2 * gamma
    divergence_l = observable_l - comparator_l
    entry = {
        "gamma": q(gamma),
        "M": q(capital_m),
        "threshold_gamma_minus_half": q(threshold),
        "energy_ratio_L_power": q(2 * capital_m),
        "G_ratio_L_power": q(3 * capital_m - 2),
        "H_ratio_L_power": q(3 * capital_m - Fraction(7, 2)),
        "observable_L_power": q(observable_l),
        "comparator_L_power": q(comparator_l),
        "divergence_L_power": q(divergence_l),
    }
    polynomial_kappa_grid.append(entry)
    slug = (
        str(gamma.numerator)
        if gamma.denominator == 1
        else f"{gamma.numerator}_{gamma.denominator}"
    ).replace("-", "neg")
    checks.extend(
        [
            row(
                f"poly_gamma_{slug}_M_threshold",
                capital_m,
                ">",
                threshold,
                "chosen polynomial amplitude M exceeds gamma-1/2",
            ),
            row(
                f"poly_gamma_{slug}_observable_L_power",
                observable_l,
                "==",
                2 * capital_m + 1,
                "kappa^2 L observable power",
            ),
            row(
                f"poly_gamma_{slug}_comparator_L_power",
                comparator_l,
                "==",
                2 * gamma,
                "(log P)^gamma contributes L^(2gamma)",
            ),
            row(
                f"poly_gamma_{slug}_divergence_L_power",
                divergence_l,
                ">",
                zero,
                "observable/comparator ratio has a positive L power",
            ),
        ]
    )

passed = sum(bool(item["pass"]) for item in checks)
analytic_boundary = [
    "FINITE ONLY: exact rational exponent and raw scale bookkeeping",
    "does not prove the buffered-energy, cubic-occupation, harmonic, pressure, or calibration estimates",
    "does not prove the collar-flux or exterior-observable lower bounds",
    "does not prove that the displayed asymptotic scales hold for any Navier--Stokes family",
    "does not prove a universal endpoint inequality or its failure without the separate analytic argument",
    "does not verify literature, novelty, or priority",
    "does not prove regularity, singularity, blow-up, continuation, or global smoothness",
    "does not solve the Clay Millennium problem; NOT CLAY",
]

payload = {
    "schema": "r074o-amplitude-endpoint-certificate-v1",
    "scope": "FINITE ONLY: exact rational amplitude-endpoint arithmetic, raw scale ledgers, finite index window, and polynomial-kappa sample grid",
    "inputs": {
        "lambda": q(lam),
        "rho": q(rho),
        "c_gamma": q(c_gamma),
        "d_E": q(d_energy),
        "audit_window": [audit_j_min, audit_j_max],
        "polynomial_gamma_grid": [q(item[0]) for item in polynomial_choices],
    },
    "derived": {
        "e_E": q(e_energy),
        "m": q(m),
        "energy_reserve": q(energy_reserve),
        "delta": q(delta),
        "q_star": q(q_star),
        "kappa_exponential_rate": q(kappa_exponential_rate),
        "kappa_L_power": q(kappa_l_power),
        "G_post_cancellation_L_power": q(zero),
        "H_post_cancellation_L_power": q(Fraction(-3, 2)),
        "energy_polynomial_L_power": q(Fraction(4, 3)),
        "observable_L_power": q(Fraction(7, 3)),
        "observable_log_power": q(Fraction(7, 6)),
        "endpoint_ratio_log_power": q(Fraction(2, 3)),
    },
    "scale_ledgers": scale_ledgers,
    "window_ledgers": window_ledgers,
    "window_propagation": {
        "factor": q(Fraction(4)),
        "fields": [
            "L_squared",
            "Gamma_decay_exponent",
            "R_decay_exponent",
            "kappa_exponent",
            "kappa_cubed_exponent",
            "energy_reserve_exponent",
            "payment_growth_exponent",
            "observable_growth_exponent",
            "endpoint_growth_exponent",
        ],
        "reason": "L_(j+1)^2=4L_j^2 and every displayed exponent is a fixed positive multiple of L_j^2",
    },
    "polynomial_kappa_grid": polynomial_kappa_grid,
    "checks": checks,
    "exact_implications": [
        "For kappa=exp((m/3)L^2)L^(2/3), kappa^3 R Gamma^(-3/2)L^(-2)=1 at the exponent-ledger level.",
        "The H packet ratio has L power -3/2, while the packet energy ratio has L power 4/3 and strict exponential reserve 1171/943200.",
        "Under B R^2 asymptotically constant, P has exponential rate 3rho and the collar/X observable has the same exponential rate as P^q_star.",
        "The observable has residual L power 7/3, hence log power 7/6; relative to a square-root-log comparator the ratio has log power 2/3.",
        "For polynomial kappa=L^M, every sampled M exceeds gamma-1/2, so the observable divided by P^(2/3)(log P)^gamma has positive L power.",
    ],
    "analytic_boundary": analytic_boundary,
    "result": "PASS" if passed == len(checks) else "FAIL",
    "summary": {
        "passed": passed,
        "total": len(checks),
        "unique_ids": len({item["id"] for item in checks}),
        "scale_rows": len(scale_ledgers),
        "window_rows": len(window_ledgers),
        "polynomial_rows": len(polynomial_kappa_grid),
    },
}

print(json.dumps(payload, indent=2, sort_keys=True))
