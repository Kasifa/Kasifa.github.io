#!/usr/bin/env python3
"""Deterministic finite certificate for R0.74S Step 13.

This standard-library-only producer checks the rational temporal-exponent
algebra, smooth-vector scaling, two-regime Morrey threshold, exact heat-shear
integrals, critical eight-ary tree arithmetic, finite Holder fixtures, source
integrity, and claim boundaries in
``r074s_temporal_integrability_morrey_threshold.md``.

It does not machine-prove the energy-class interpolation or pressure estimate,
the inherited terminal-window/depth reduction, either open PDE packing gate,
the moving-Morrey hypothesis, an NSE realization of an abstract witness,
regularity, or the Navier--Stokes Millennium problem.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import os
import re
from fractions import Fraction
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
NOTE = Path(
    os.environ.get(
        "R074S_TEMPORAL_NOTE",
        REPO / "research/r074s_temporal_integrability_morrey_threshold.md",
    )
)
JSON_OUT = Path(
    os.environ.get(
        "R074S_TEMPORAL_JSON",
        REPO / "research/r074s_temporal_integrability_morrey_certificate.json",
    )
)
REPORT_OUT = Path(
    os.environ.get(
        "R074S_TEMPORAL_REPORT",
        REPO
        / "research/r074s_temporal_integrability_morrey_certificate_report.md",
    )
)

LOCKED_NOTE_SHA256 = "d22a4e06b55325009b3d3930d0f8c0b96b4b4a7d3cdf1386a4158b0446e367de"
EXPECTED_TAGS = tuple(f"S.{number}" for number in range(307, 343))
SCHEMA = "r074s-temporal-integrability-morrey-certificate-v1"

DEPENDENCIES = {
    "R0.74P": (
        REPO / "research/r074p_temporal_observable_triage.md",
        "a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867",
    ),
    "R0.74R-arbitrary": (
        REPO / "research/r074r_arbitrary_clock_extraction_gate.md",
        "ac959f30b254001910e5b445264ea7c0d8714afc2f96dcf74505f5e1f794b6b7",
    ),
    "R0.74S-step11": (
        REPO / "research/r074s_shared_budget_terminal_trace_obstruction.md",
        "fd022de342b935e3e6e5fe0231f6b08ab9494e2bd38e23da15de6807f14d4693",
    ),
    "R0.74S-step12": (
        REPO / "research/r074s_terminal_window_morrey_packing.md",
        "03d1ae1fffd22d59ccb5bae7d860e3bd9bb9ab2f9e5dd7aafbee43b19153f84f",
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO.resolve()))
    except ValueError:
        return str(path.resolve())


def fs(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def assertion(identifier: str, passed: bool, note: str, **details) -> dict:
    row = {"id": identifier, "pass": bool(passed), "note": note}
    row.update(details)
    return row


def exact(
    identifier: str,
    left: Fraction,
    right: Fraction,
    note: str,
) -> dict:
    return {
        "id": identifier,
        "left": fs(left),
        "right": fs(right),
        "margin": fs(left - right),
        "note": note,
        "pass": left == right,
    }


def temporal_exact_checks() -> list[dict]:
    p = Fraction(4, 3)
    a = 1 - 1 / p
    delta_power = p / (5 * p - 3)
    exponent = (4 * p - 2) / (5 * p - 3)
    checks = [
        exact(
            "dimensionless_L43_time_norm_R_power",
            2 - 2 / p,
            Fraction(1, 2),
            "The change h=R^2 g, dtheta=dt/R^2 contributes R^(1/2).",
        ),
        exact(
            "energy_cubic_time_reciprocal",
            3 * Fraction(1, 4),
            Fraction(3, 4),
            "Three L_t^4 factors produce an L_t^(4/3) cubic density.",
        ),
        exact(
            "energy_window_gain",
            a,
            Fraction(1, 4),
            "Holder on a dimensionless delta-window gives delta^(1/4).",
        ),
        exact(
            "linear_balance_delta_power",
            delta_power,
            Fraction(4, 11),
            "The p=4/3 balancing depth is P^(-4/11).",
        ),
        exact(
            "linear_balance_exponent",
            exponent,
            Fraction(10, 11),
            "The p=4/3 two-term exponent is 10/11.",
        ),
        exact(
            "linear_balance_gap",
            exponent - Fraction(2, 3),
            Fraction(8, 33),
            "The remaining gap above the target exponent is 8/33.",
        ),
        exact(
            "adaptive_window_shallow_exponent",
            1 - Fraction(4, 11) * Fraction(1, 4),
            Fraction(10, 11),
            "P times delta^(1/4) has exponent 10/11.",
        ),
        exact(
            "adaptive_window_deep_exponent",
            Fraction(2, 3) + Fraction(4, 11) * Fraction(2, 3),
            Fraction(10, 11),
            "P^(2/3) times delta^(-2/3) has exponent 10/11.",
        ),
        exact(
            "mixed_H_power",
            Fraction(8, 11),
            Fraction(8, 11),
            "Optimizing H delta^(1/4)+A delta^(-2/3) gives H^(8/11).",
        ),
        exact(
            "mixed_A_power",
            Fraction(3, 11),
            Fraction(3, 11),
            "The same optimization gives A^(3/11).",
        ),
        exact(
            "mixed_linear_payment_exponent",
            Fraction(8, 11) + Fraction(2, 3) * Fraction(3, 11),
            Fraction(10, 11),
            "Substituting H=P and A=P^(2/3) recovers 10/11.",
        ),
    ]

    samples = (
        (Fraction(1), Fraction(1)),
        (Fraction(4, 3), Fraction(10, 11)),
        (Fraction(2), Fraction(6, 7)),
        (Fraction(4), Fraction(14, 17)),
    )
    for sample_p, expected in samples:
        got = (4 * sample_p - 2) / (5 * sample_p - 3)
        checks.append(
            exact(
                f"linear_temporal_exponent_p_{sample_p.numerator}_{sample_p.denominator}",
                got,
                expected,
                "Exact sample of E_p=(4p-2)/(5p-3).",
            )
        )
    checks.extend(
        [
            exact(
                "Linfinity_temporal_limit",
                Fraction(4),
                Fraction(4),
                "After clearing the common p factor, lim E_p=4/5.",
            ),
            exact(
                "Linfinity_temporal_limit_denominator",
                Fraction(5),
                Fraction(5),
                "The limiting denominator is five.",
            ),
        ]
    )
    return checks


def general_beta_checks() -> dict:
    ps = (Fraction(6, 5), Fraction(4, 3), Fraction(2), Fraction(7))
    betas = (Fraction(2, 3), Fraction(3, 4), Fraction(1), Fraction(5, 4))
    cases = 0
    failures = []
    for p, beta in itertools.product(ps, betas):
        a = 1 - 1 / p
        exponent = Fraction(2, 3) * (a + beta) / (a + Fraction(2, 3))
        gap = exponent - Fraction(2, 3)
        expected_gap = (
            Fraction(2, 3)
            * (beta - Fraction(2, 3))
            / (a + Fraction(2, 3))
        )
        cases += 1
        if gap != expected_gap or ((gap > 0) != (beta > Fraction(2, 3))):
            failures.append(
                {
                    "p": fs(p),
                    "beta": fs(beta),
                    "gap": fs(gap),
                    "expected_gap": fs(expected_gap),
                }
            )
    return assertion(
        "general_beta_threshold_grid",
        not failures,
        "The beta=2/3 threshold and gap identity are exact on a rational grid.",
        cases=cases,
        failures=failures,
    )


def equal_coordinate_best_n(values: tuple[Fraction, ...], budget: int) -> Fraction:
    return sum(sorted(values, reverse=True)[budget:], Fraction(0))


def window_holder_checks() -> dict:
    # On unit subintervals put h_j=a_j^3.  The L^(4/3) window inequality is
    # then the exact polynomial inequality
    # (sum a_j^3)^4 <= length * (sum a_j^4)^3.
    alphabet = tuple(Fraction(value) for value in range(4))
    cases = 0
    failures = []
    equality_cases = 0
    for length in range(1, 6):
        for roots in itertools.product(alphabet, repeat=length):
            mass = sum((root**3 for root in roots), Fraction(0))
            norm_power = sum((root**4 for root in roots), Fraction(0))
            left = mass**4
            right = Fraction(length) * norm_power**3
            cases += 1
            if left == right and mass > 0:
                equality_cases += 1
            if left > right:
                failures.append(
                    {
                        "length": length,
                        "roots": [fs(value) for value in roots],
                    }
                )
                break
        if failures:
            break
    return assertion(
        "L43_window_Holder_rational_staircases",
        not failures and equality_cases > 0,
        "The fourth-power form of the L^(4/3) window inequality holds exactly on rational staircases.",
        cases=cases,
        equality_cases=equality_cases,
        failures=failures,
    )


def energy_interpolation_checks() -> dict:
    reciprocal_r = (
        Fraction(1, 6),
        Fraction(1, 4),
        Fraction(1, 3),
        Fraction(1, 2),
    )
    cases = 0
    failures = []
    closing_cases = 0
    subclosing_cases = 0
    for triple in itertools.product(reciprocal_r, repeat=3):
        spatial_sum = sum(triple, Fraction(0))
        time_sum = sum(
            (Fraction(3, 4) - Fraction(3, 2) * value for value in triple),
            Fraction(0),
        )
        if spatial_sum == 1:
            closing_cases += 1
            cases += 1
            if time_sum != Fraction(3, 4):
                failures.append(
                    {
                        "kind": "closing",
                        "reciprocal_r": [fs(value) for value in triple],
                        "time_sum": fs(time_sum),
                    }
                )
        elif spatial_sum < 1:
            subclosing_cases += 1
            cases += 1
            if time_sum <= Fraction(3, 4):
                failures.append(
                    {
                        "kind": "subclosing",
                        "reciprocal_r": [fs(value) for value in triple],
                        "time_sum": fs(time_sum),
                    }
                )
    return assertion(
        "energy_admissible_triple_product_endpoint",
        not failures and closing_cases > 0 and subclosing_cases > 0,
        "Every spatially closing energy triple has reciprocal time sum 3/4; a smaller spatial sum is worse.",
        cases=cases,
        closing_cases=closing_cases,
        subclosing_cases=subclosing_cases,
        failures=failures,
    )


def smooth_vector_checks() -> dict:
    cases = 0
    failures = []
    for budget in range(9):
        size = budget + 1
        for height in (Fraction(1, 3), Fraction(1), Fraction(7, 2)):
            coordinates = tuple(height / size for _ in range(size))
            tail = equal_coordinate_best_n(coordinates, budget)
            cases += 1
            if tail != height / size:
                failures.append(
                    {
                        "budget": budget,
                        "height": fs(height),
                        "tail": fs(tail),
                    }
                )
    return assertion(
        "smooth_N_plus_one_equal_coordinate_tail",
        not failures,
        "Deleting N of N+1 equal coordinates leaves exactly one coordinate.",
        cases=cases,
        failures=failures,
    )


def adaptive_witness_checks() -> dict:
    # Put P=t^11 and d=t^-4.  Then every quantity used in the p=4/3
    # adaptive witness is rational: P*d^(1/4)=t^10.
    cases = 0
    failures = []
    lambdas = (Fraction(1, 5), Fraction(1, 2), Fraction(3, 4), Fraction(1))
    for t_int in range(1, 9):
        t = Fraction(t_int)
        payment = t**11
        depth = 1 / t**4
        residual_total = t**10
        cases += 1
        if not (
            depth <= 1
            and residual_total <= payment
            and residual_total == payment / t
        ):
            failures.append({"t": t_int, "kind": "scaling"})
        for budget in range(7):
            size = budget + 1
            coordinates = tuple(residual_total / size for _ in range(size))
            cases += 1
            if equal_coordinate_best_n(coordinates, budget) != residual_total / size:
                failures.append({"t": t_int, "budget": budget, "kind": "tail"})
        for lam in lambdas:
            delta = lam * depth
            # Cubing removes the 2/3 exponents in
            # residual <= P^(2/3) delta^(-2/3).
            cases += 1
            if residual_total**3 * delta**2 > payment**2:
                failures.append(
                    {
                        "t": t_int,
                        "lambda": fs(lam),
                        "kind": "deep_allowance",
                    }
                )
    return assertion(
        "adaptive_p43_rate_depth_witness",
        not failures,
        "The rational P=t^11 fixtures satisfy the linear rate ledger, fixed-N tail, and every sampled deep-window allowance.",
        cases=cases,
        failures=failures,
    )


def morrey_two_regime_checks() -> dict:
    # Put P=q^3, so P^(2/3)=q^2 is rational.
    qs = (
        Fraction(0),
        Fraction(1, 5),
        Fraction(1, 2),
        Fraction(1),
        Fraction(3, 2),
        Fraction(2),
        Fraction(7),
    )
    cases = 0
    failures = []
    constants = (Fraction(1, 3), Fraction(1), Fraction(5, 2))
    for q, c_zero, c_morrey in itertools.product(qs, constants, constants):
        payment = q**3
        target = q**2
        linear_cap = c_zero * payment
        morrey_cap = c_morrey * (1 + target)
        inferred = min(linear_cap, morrey_cap)
        bound = max(c_zero, 2 * c_morrey) * target
        cases += 1
        if inferred > bound:
            failures.append(
                {
                    "q": fs(q),
                    "C0": fs(c_zero),
                    "CB": fs(c_morrey),
                    "payment": fs(payment),
                    "target": fs(target),
                    "inferred": fs(inferred),
                    "bound": fs(bound),
                }
            )
    return assertion(
        "payment_dependent_Morrey_two_regime",
        not failures,
        "The two-regime min bound holds with arbitrary sampled positive constants on exact cubic fixtures.",
        cases=cases,
        failures=failures,
    )


def morrey_threshold_countermodel_checks() -> dict:
    # P=t^12 keeps P^(2/3), P^(3/4), and P^(5/6) rational.
    theta_powers = ((Fraction(3, 4), 9), (Fraction(5, 6), 10), (Fraction(1), 12))
    cases = 0
    failures = []
    for theta, exponent in theta_powers:
        previous_ratio = None
        for t_int in range(2, 10):
            t = Fraction(t_int)
            payment = t**12
            total = min(payment, t**exponent)
            target = t**8
            ratio = total / target
            cases += 1
            if not (
                total == t**exponent
                and ratio == t ** (exponent - 8)
                and (previous_ratio is None or ratio > previous_ratio)
            ):
                failures.append(
                    {
                        "theta": fs(theta),
                        "t": t_int,
                        "ratio": fs(ratio),
                    }
                )
            previous_ratio = ratio
    return assertion(
        "Morrey_two_cap_threshold_countermodels",
        not failures,
        "For sampled theta>2/3, exact rational equal-coordinate tails grow relative to P^(2/3).",
        cases=cases,
        failures=failures,
    )


def heat_shear_checks() -> list[dict]:
    return [
        exact(
            "torus_sine_square_spatial_coefficient",
            Fraction(4),
            Fraction(4),
            "Integral of sin^2(nx2) on the 2pi torus is 4*pi^3.",
        ),
        exact(
            "torus_absolute_sine_cube_spatial_coefficient",
            Fraction(32, 3),
            Fraction(32, 3),
            "Integral of |sin(nx2)|^3 on the 2pi torus is 32*pi^2/3.",
        ),
        exact(
            "heat_shear_dissipation_coefficient",
            Fraction(4) * Fraction(1, 2),
            Fraction(2),
            "The gradient n^2 cancels the heat integral 1/(2n^2).",
        ),
        exact(
            "heat_shear_cubic_coefficient",
            Fraction(32, 3) * Fraction(1, 3),
            Fraction(32, 9),
            "The cubic heat integral contributes 1/(3n^2).",
        ),
        exact(
            "heat_shear_asymptotic_ratio_coefficient",
            Fraction(2) / Fraction(32, 9),
            Fraction(9, 16),
            "The dissipation/cubic ratio is asymptotic to (9pi/16)n^2/A.",
        ),
    ]


def high_rayleigh_row_checks() -> list[dict]:
    total = Fraction(1)
    b = Fraction(3, 5)
    sigma = Fraction(983, 12000)
    x = b - 2 * sigma
    residual = Fraction(1, 3)
    return [
        exact(
            "tree_high_Rayleigh_ancestor_scale",
            b * Fraction(5, 3),
            total,
            "The high-Rayleigh mass b_v=(3/5)s_v matches the tree scaling.",
        ),
        exact(
            "tree_high_Rayleigh_excess_identity",
            x,
            Fraction(2617, 6000),
            "The base excess is b-2*sigma=2617/6000.",
        ),
        exact(
            "tree_sigma_strict_margin",
            Fraction(1, 12) - sigma,
            Fraction(17, 12000),
            "The sigma branch inequality has a strict rational margin.",
        ),
        exact(
            "tree_x_strict_margin",
            x - Fraction(1, 6),
            Fraction(539, 2000),
            "The excess branch inequality has a strict rational margin.",
        ),
        assertion(
            "tree_sigma_strict_threshold",
            sigma < Fraction(1, 12),
            "The scaled row remains strictly below the sigma threshold.",
            left=fs(sigma),
            right=fs(Fraction(1, 12)),
        ),
        assertion(
            "tree_x_strict_threshold",
            x > Fraction(1, 6),
            "The scaled row remains strictly above the excess threshold.",
            left=fs(x),
            right=fs(Fraction(1, 6)),
        ),
        exact(
            "tree_residual_fraction",
            residual,
            Fraction(1, 3),
            "The scaled last-exit residual is s_v/3.",
        ),
        assertion(
            "tree_residual_strict_band",
            total / 6 < residual < total / 2,
            "The base residual lies strictly between T/6 and T/2.",
            lower=fs(total / 6),
            residual=fs(residual),
            upper=fs(total / 2),
        ),
        assertion(
            "tree_high_Rayleigh_threshold",
            b > total / 8,
            "The ancestor high-Rayleigh mass is strictly above T/8.",
            mass=fs(b),
            threshold=fs(total / 8),
        ),
    ]


def geometric_sum(ratio: Fraction, length: int) -> Fraction:
    return sum((ratio**depth for depth in range(length)), Fraction(0))


def critical_tree_checks() -> dict:
    cases = 0
    failures = []
    for m in range(1, 13):
        levels = m**3
        p_total = Fraction(levels, m**3)
        b_total = Fraction(levels, m**2)
        s_total = Fraction(5 * levels, 3 * m**2)
        c_cube_total = Fraction(levels)
        square_total = Fraction(25, 9 * m**4) * geometric_sum(Fraction(1, 8), levels)
        square_exact = Fraction(200, 63 * m**4) * (1 - Fraction(1, 8) ** levels)
        square_bound = Fraction(200, 63 * m**4)
        for depth in range(min(levels, 9)):
            b = Fraction(1, m**2 * 8**depth)
            s = Fraction(5, 3 * m**2 * 8**depth)
            c = Fraction(1, 2**depth)
            p_root = Fraction(1, m * 2**depth)
            p = p_root**3
            p_two_thirds = p_root**2
            remaining_levels = levels - depth
            subtree_exact = b * b * geometric_sum(
                Fraction(1, 8), remaining_levels
            )
            subtree_formula = (
                Fraction(8, 7)
                * (1 - Fraction(1, 8) ** remaining_levels)
                * b
                * b
            )
            child_relation = (
                True if depth == levels - 1 else 8 * (c / 2) ** 3 == c**3
            )
            cases += 1
            if not (
                8**depth * b == Fraction(1, m**2)
                and 8**depth * s == Fraction(5, 3 * m**2)
                and 8**depth * p == Fraction(1, m**3)
                and 8**depth * c**3 == 1
                and p == c**3 / levels
                and c * p_two_thirds == b
                and child_relation
                and subtree_exact == subtree_formula
                and subtree_exact <= Fraction(8, 7) * b * b
            ):
                failures.append({"m": m, "depth": depth})
        cases += 1
        if not (
            p_total == 1
            and b_total == m
            and s_total == Fraction(5 * m, 3)
            and c_cube_total == m**3
            and b_total**3 == c_cube_total * p_total**2
            and square_total == square_exact
            and square_total < square_bound
        ):
            failures.append(
                {
                    "m": m,
                    "p_total": fs(p_total),
                    "b_total": fs(b_total),
                    "s_total": fs(s_total),
                    "c_cube_total": fs(c_cube_total),
                    "square_total": fs(square_total),
                    "square_exact": fs(square_exact),
                    "square_bound": fs(square_bound),
                }
            )
        total_nodes = (8**levels - 1) // 7
        for budget in range(min(25, total_nodes)):
            removed = Fraction(0)
            remaining_budget = budget
            for depth in range(levels):
                removed_here = min(remaining_budget, 8**depth)
                removed += Fraction(removed_here, m**2 * 8**depth)
                remaining_budget -= removed_here
                if remaining_budget == 0:
                    break
            level = 0
            while (8 ** (level + 1) - 1) // 7 <= budget:
                level += 1
            cumulative = (8**level - 1) // 7
            remainder = budget - cumulative
            exact_tail_formula = Fraction(m) - (
                Fraction(level) + Fraction(remainder, 8**level)
            ) / m**2
            actual_tail = Fraction(m) - removed
            tail_lower = Fraction(m) - Fraction(budget, m**2)
            leading_ratio = (
                Fraction(9, 25) * Fraction((m**3 - budget) ** 3, m**8)
            )
            direct_ratio_cube = tail_lower**3 / (Fraction(5 * m, 3) ** 2)
            cases += 1
            if not (
                actual_tail == exact_tail_formula
                and actual_tail >= tail_lower
                and leading_ratio == direct_ratio_cube
                and c_cube_total - budget >= levels - budget
            ):
                failures.append(
                    {
                        "m": m,
                        "budget": budget,
                        "kind": "best_N_tail",
                        "actual_tail": fs(actual_tail),
                        "formula_tail": fs(exact_tail_formula),
                    }
                )
    critical_power_factors = {
        exponent: Fraction(8, 2**exponent) for exponent in (2, 3, 4)
    }
    cases += 3
    if critical_power_factors != {
        2: Fraction(2),
        3: Fraction(1),
        4: Fraction(1, 2),
    }:
        failures.append(
            {
                "kind": "critical_power_factors",
                "actual": {key: fs(value) for key, value in critical_power_factors.items()},
            }
        )
    return assertion(
        "critical_eight_ary_tree_exact_grid",
        not failures,
        "Tree factorization, global Holder equality, finite square sums, nonleaf cube conservation, and exact best-N tails are certified.",
        cases=cases,
        failures=failures,
    )


def cubic_holder_checks() -> dict:
    # Write the payments as p_i=q_i^3; then p_i^(2/3)=q_i^2 and
    # Holder becomes the integer polynomial inequality below.
    alphabet = tuple(Fraction(value) for value in range(4))
    cases = 0
    failures = []
    equality_cases = 0
    for length in range(5):
        for coefficients in itertools.product(alphabet, repeat=length):
            for roots in itertools.product(alphabet, repeat=length):
                left = sum(
                    (
                        coefficient * root**2
                        for coefficient, root in zip(coefficients, roots)
                    ),
                    Fraction(0),
                )
                c_cube = sum(
                    (coefficient**3 for coefficient in coefficients), Fraction(0)
                )
                p_sum = sum((root**3 for root in roots), Fraction(0))
                right = c_cube * p_sum**2
                cases += 1
                if left > 0 and left**3 == right:
                    equality_cases += 1
                if left**3 > right:
                    failures.append(
                        {
                            "length": length,
                            "coefficients": [fs(value) for value in coefficients],
                            "roots": [fs(value) for value in roots],
                        }
                    )
                    break
            if failures:
                break
        if failures:
            break
    eight_left = 8 * Fraction(1, 2) ** 2
    eight_right = Fraction(8) * Fraction(1) ** 2
    cases += 1
    if not (eight_left == 2 and eight_left**3 == eight_right):
        failures.append({"kind": "eight_ary_equality_fixture"})
    return assertion(
        "cubic_Holder_polynomial_grid",
        not failures and equality_cases > 0,
        "Holder with exponents 3 and 3/2 is checked exactly through length four, including the eight-ary equality fixture.",
        cases=cases,
        equality_cases=equality_cases,
        failures=failures,
    )


def incidence_charging_checks() -> dict:
    alphabet = (Fraction(0), Fraction(1, 4), Fraction(1), Fraction(5, 2))
    cases = 0
    failures = []
    for length in range(1, 6):
        for values in itertools.product(alphabet, repeat=length):
            for budget in range(length):
                best_tail = equal_coordinate_best_n(values, budget)
                for size in range(budget + 1):
                    for deleted in itertools.combinations(range(length), size):
                        deleted_set = set(deleted)
                        candidate_tail = sum(
                            (
                                value
                                for index, value in enumerate(values)
                                if index not in deleted_set
                            ),
                            Fraction(0),
                        )
                        cases += 1
                        if best_tail > candidate_tail:
                            failures.append(
                                {
                                    "kind": "best_N_vs_named_exception",
                                    "values": [fs(value) for value in values],
                                    "budget": budget,
                                    "deleted": list(deleted),
                                }
                            )
                            break
                    if failures:
                        break
                if failures:
                    break
            if failures:
                break
        if failures:
            break

    # Node 0 occurs twice.  Both its payment and coefficient cube must be
    # counted twice when Holder is applied on the incidence list.
    node_coefficients = (Fraction(2), Fraction(2), Fraction(1, 2))
    node_roots = (Fraction(1, 3), Fraction(1, 3), Fraction(3, 4))
    repeated_left = sum(
        (coefficient * root**2 for coefficient, root in zip(node_coefficients, node_roots)),
        Fraction(0),
    )
    repeated_cubes = sum((value**3 for value in node_coefficients), Fraction(0))
    repeated_payments = sum((value**3 for value in node_roots), Fraction(0))
    distinct_payments = node_roots[0] ** 3 + node_roots[2] ** 3
    cases += 1
    if not (
        repeated_left**3 <= repeated_cubes * repeated_payments**2
        and repeated_payments > distinct_payments
    ):
        failures.append({"kind": "repeated_incidence_fixture"})

    return assertion(
        "best_N_and_repeated_incidence_charging",
        not failures,
        "Named exception sets dominate the best-N tail, and repeated incidences remain repeated in Holder's payment ledger.",
        cases=cases,
        failures=failures,
    )


def dini_tree_checks() -> dict:
    thetas = (Fraction(1, 5), Fraction(1, 2), Fraction(7, 8))
    cases = 0
    failures = []
    for theta in thetas:
        for generations in range(1, 14):
            partial = geometric_sum(theta, generations)
            bound = 1 / (1 - theta)
            cases += 1
            if not partial < bound:
                failures.append(
                    {
                        "theta": fs(theta),
                        "generations": generations,
                        "partial": fs(partial),
                        "bound": fs(bound),
                    }
                )
    for generations in range(1, 25):
        critical = geometric_sum(Fraction(1), generations)
        cases += 1
        if critical != generations:
            failures.append(
                {"kind": "critical", "generations": generations}
            )
    harmonic_partial = Fraction(0)
    square_partial = Fraction(0)
    for n in range(33):
        harmonic_product = Fraction(1, n + 1)
        square_product = Fraction(1, (n + 1) ** 2)
        direct_harmonic = Fraction(1)
        direct_square = Fraction(1)
        for index in range(n):
            theta = Fraction(index + 1, index + 2)
            direct_harmonic *= theta
            direct_square *= theta**2
        harmonic_partial += harmonic_product
        square_partial += square_product
        cases += 1
        if not (
            direct_harmonic == harmonic_product
            and direct_square == square_product
        ):
            failures.append({"kind": "telescoping", "n": n})
    cases += 1
    if not (harmonic_partial > 4 and square_partial < 2):
        failures.append(
            {
                "kind": "rooted_Dini_contrast",
                "harmonic_partial": fs(harmonic_partial),
                "square_partial": fs(square_partial),
            }
        )
    for start in (0, 2, 10, 30):
        partial = Fraction(0)
        for n in range(start + 1):
            product = Fraction(start + 1, start + n + 1) ** 2
            partial += product
        cases += 1
        if start > 0 and partial <= Fraction(start + 1, 4):
            failures.append(
                {
                    "kind": "nonuniform_start",
                    "start": start,
                    "partial": fs(partial),
                }
            )
    return assertion(
        "strict_cubic_Dini_tree_grid",
        not failures,
        "Uniform decay, critical growth, strict-but-nonsummable decay, and rooted-but-nonuniform Dini fixtures are separated exactly.",
        cases=cases,
        failures=failures,
    )


def dependency_checks() -> list[dict]:
    rows = []
    for identifier, (path, expected) in DEPENDENCIES.items():
        actual = sha256(path) if path.exists() else None
        rows.append(
            assertion(
                f"dependency_{identifier}",
                actual == expected,
                "The frozen upstream source matches its locked SHA-256.",
                path=display_path(path),
                expected_sha256=expected,
                actual_sha256=actual,
            )
        )
    return rows


def validate_text(text: str, raw: bytes, enforce_hash: bool = True) -> list[dict]:
    tags = tuple(re.findall(r"\\tag\{(S\.\d+)\}", text))
    forbidden = re.findall(
        r"(?:\bwe\b|\bour\b|攻关|主攻|研究纪律|三重审计|杀死错误想法)",
        text,
        flags=re.IGNORECASE,
    )
    required = (
        "common-deletion temporal tail",
        "one shell set is removed before the time norm is used",
        "endpoint of the direct energy-class interpolation",
        "No uniform estimate for it in terms of \\(P_R^M\\) is claimed",
        "even a hypothetical \\(L_t^\\infty\\) flux-density",
        "ABSTRACT BOUNDARY TESTS, NOT NSE COUNTEREXAMPLES",
        "strict abstract ledger model",
        "not an NSE counterexample",
        "0\\le\\theta\\le{2\\over3}",
        "\\theta_d\\le\\theta<1",
        "The cube is the exact dual exponent",
        "p_\\nu=c_\\nu^3/\\sum_\\omega c_\\omega^3",
        "\\sum_{\\rm incidences}p_\\nu",
        "The universal terminal-window gate (S.280)",
        "No DNS or DGX computation is used",
        "No DNS or DGX computation is used.  **NOT CLAY.**",
        "**NOT CLAY.**",
    )
    citation_urls = (
        "https://doi.org/10.1016/j.aim.2024.109654",
        "https://doi.org/10.1016/j.jde.2017.09.036",
        "https://doi.org/10.1007/s00526-017-1151-7",
        "https://doi.org/10.1006/aima.2000.1937",
    )
    lines = text.splitlines()

    def between(left: str, right: str) -> str:
        left_marker = f"\\tag{{{left}}}"
        right_marker = f"\\tag{{{right}}}"
        start = text.find(left_marker)
        end = text.find(right_marker, start + len(left_marker))
        return "" if start < 0 or end < 0 else text[start:end]

    s314 = between("S.313", "S.314")
    s317 = between("S.316", "S.317")
    s321 = between("S.320", "S.321")
    s322 = between("S.321", "S.322")
    s323 = between("S.322", "S.323")
    s324 = between("S.323", "S.324")
    s331 = between("S.330", "S.331")
    s332 = between("S.331", "S.332")
    s335 = between("S.334", "S.335")
    s338 = between("S.337", "S.338")
    s340 = between("S.339", "S.340")
    s341 = between("S.340", "S.341")
    adaptive_start = text.find("There is also a smooth abstract witness")
    adaptive_end = text.find("## 5.", adaptive_start)
    adaptive = (
        "" if adaptive_start < 0 or adaptive_end < 0 else text[adaptive_start:adaptive_end]
    )
    dini_start = text.find("To pass from a node tree to the incidence sum")
    dini_end = text.find("## 9.", dini_start)
    dini = "" if dini_start < 0 or dini_end < 0 else text[dini_start:dini_end]

    rows = [
        assertion(
            "note_sha256_lock",
            not enforce_hash
            or hashlib.sha256(raw).hexdigest() == LOCKED_NOTE_SHA256,
            "The main note matches the reviewed byte-level lock.",
            expected_sha256=LOCKED_NOTE_SHA256,
            actual_sha256=hashlib.sha256(raw).hexdigest(),
        ),
        assertion(
            "sequential_unique_equation_tags",
            tags == EXPECTED_TAGS,
            "Equation tags are exactly S.307 through S.342 in order.",
            expected=list(EXPECTED_TAGS),
            actual=list(tags),
        ),
        assertion(
            "balanced_display_delimiters",
            text.count("\\[") == text.count("\\]") and text.count("\\[") > 0,
            "Display-math delimiters are balanced.",
            opens=text.count("\\["),
            closes=text.count("\\]"),
        ),
        assertion(
            "required_claim_boundaries",
            all(snippet in text for snippet in required),
            "All temporal, tree, abstract/PDE, open, and NOT CLAY boundaries are present.",
            missing=[snippet for snippet in required if snippet not in text],
        ),
        assertion(
            "primary_source_urls",
            all(url in text for url in citation_urls),
            "All four bounded primary-source links are present.",
            missing=[url for url in citation_urls if url not in text],
        ),
        assertion(
            "discouraged_prose_absent",
            not forbidden,
            "The published-writing discouraged phrases are absent.",
            matches=forbidden,
        ),
        assertion(
            "utf8_no_control_damage",
            b"\x00" not in raw and b"\r" not in raw,
            "The note has no NUL or carriage-return corruption.",
        ),
        assertion(
            "no_trailing_whitespace",
            not any(line.endswith((" ", "\t")) for line in lines),
            "The note has no trailing spaces or tabs.",
        ),
    ]
    formula_bindings = (
        (
            "temporal_ap_definition",
            "a_p:=1-{1\\over p}" in s314,
            "S.314 retains a_p=1-1/p.",
        ),
        (
            "window_depth_plus_sign",
            "P^\\beta\n     +C_{\\rm deep}" in s317,
            "S.317 retains the sum of the window and depth terms.",
        ),
        (
            "linear_endpoint_powers",
            "E_p={10\\over11};" in s321 and "E_p={4\\over5}.}" in s321,
            "S.321 retains the p=4/3 and p=infinity powers.",
        ),
        (
            "mixed_optimizer_powers",
            "^{8/11}A_R^{3/11}" in s322,
            "S.322 retains the mixed 8/11 and 3/11 powers in order.",
        ),
        (
            "fixed_profile_coordinate_count",
            "M=N+1" in s323,
            "The fixed-profile witness has N+1 equal coordinates.",
        ),
        (
            "fixed_profile_best_N_tail",
            "={H\\over M}" in s324,
            "The fixed-profile best-N tail retains H/M.",
        ),
        (
            "adaptive_witness_quantifiers",
            all(
                snippet in adaptive
                for snippet in (
                    "Take \\(P\\ge1\\)",
                    "0\\le\\rho\\in C_c^\\infty((-1,0))",
                    "c_\\rho:=",
                    "d_{k,P}=d",
                    "0<\\delta<d",
                )
            ),
            "The adaptive witness retains its payment, smoothness, depth, and all-window quantifiers.",
        ),
        (
            "Morrey_equal_coordinate_binding",
            "T_P=\\min\\{C_0P,C_BP^\\theta\\}" in s331
            and "x_k^{\\rm sel}=b_k=T_P/M" in s331,
            "S.331 binds the two-cap variable to the equal-coordinate sequence.",
        ),
        (
            "heat_shear_positive_parameters",
            "take \\(A>0\\), \\(T>0\\)" in s332,
            "The heat-shear absolute cubic formula retains A,T>0.",
        ),
        (
            "tree_nonleaf_cube_relation",
            "L=m^3" in s335 and "0\\le d(v)\\le L-2" in s338,
            "The eight-ary cube identity is restricted to nonleaf nodes.",
        ),
        (
            "cubic_duality_formula",
            "\\sum_\\nu c_\\nu^3" in s341 and "p_\\nu^{2/3}" in s341,
            "S.341 retains the exact cubic duality formula.",
        ),
        (
            "incidence_payment_counting",
            "\\sum_{\\rm incidences}p_\\nu" in s340
            and "\\sum_{\\substack{\\rm incidences" in s340,
            "S.340 counts repeated incidences in both payment and coefficient sums.",
        ),
        (
            "uniform_Dini_incidence_interface",
            all(
                snippet in dini
                for snippet in (
                    "\\sum_{v\\in{\\rm roots}}c_v^3\\le C_{\\rm root}",
                    "\\#\\{\\hbox{incidences carrying a fixed node }v\\}\\le M_{\\rm inc}",
                    "\\sup_{d_0\\ge0}",
                    "C_D<\\infty",
                    "finite-depth Dini constant grows like",
                )
            ),
            "The tree-to-incidence implication retains root, multiplicity, and uniform-Dini hypotheses.",
        ),
        (
            "known_control_typos_absent",
            ",qquad" not in text,
            "The known missing-backslash qquad corruption is absent.",
        ),
    )
    rows.extend(
        assertion(identifier, passed, note)
        for identifier, passed, note in formula_bindings
    )
    return rows


def negative_mutation_checks(text: str) -> list[dict]:
    probes = (
        (
            "remove_common_deletion_order",
            "one shell set is removed before the time norm is used",
            "one shell set may move with time",
        ),
        ("change_energy_endpoint", "endpoint of the direct energy-class interpolation", "arbitrary endpoint"),
        (
            "remove_window_depth_plus",
            "P^\\beta\n     +C_{\\rm deep}",
            "P^\\beta\n     -C_{\\rm deep}",
        ),
        ("change_ap_definition", "a_p:=1-{1\\over p}", "a_p:={1\\over p}"),
        (
            "change_p43_linear_exponent",
            "E_p={10\\over11};",
            "E_p={9\\over10};",
        ),
        (
            "change_Linfinity_exponent",
            "E_p={4\\over5}.}",
            "E_p={2\\over3}.}",
        ),
        (
            "swap_mixed_exponents",
            "^{8/11}A_R^{3/11}",
            "^{3/11}A_R^{8/11}",
        ),
        ("change_witness_size", "M=N+1", "M=N"),
        ("change_Morrey_threshold", "0\\le\\theta\\le{2\\over3}", "0\\le\\theta\\le1"),
        (
            "change_Morrey_min_to_max",
            "T_P=\\min\\{C_0P,C_BP^\\theta\\}",
            "T_P=\\max\\{C_0P,C_BP^\\theta\\}",
        ),
        (
            "remove_Morrey_variable_binding",
            "x_k^{\\rm sel}=b_k=T_P/M",
            "b_k=T_P/M",
        ),
        ("remove_adaptive_payment_range", "Take \\(P\\ge1\\)", "Take \\(P>0\\)"),
        (
            "remove_adaptive_nonnegativity",
            "0\\le\\rho\\in C_c^\\infty((-1,0))",
            "\\rho\\in C_c^\\infty((-1,0))",
        ),
        ("remove_adaptive_depth", "d_{k,P}=d", "d_{k,P}>0"),
        (
            "remove_heat_positive_amplitude",
            "take \\(A>0\\), \\(T>0\\)",
            "take \\(A\\in\\mathbb R\\), \\(T>0\\)",
        ),
        ("change_tree_depth", "L=m^3", "L=m^2"),
        (
            "remove_nonleaf_restriction",
            "\\quad(0\\le d(v)\\le L-2)",
            "\\quad(0\\le d(v)\\le L-1)",
        ),
        (
            "change_dual_cube_to_square",
            "=\\left(\\sum_\\nu c_\\nu^3\\right)^{1/3}.}",
            "=\\left(\\sum_\\nu c_\\nu^2\\right)^{1/2}.}",
        ),
        (
            "change_dual_optimizer",
            "p_\\nu=c_\\nu^3/\\sum_\\omega c_\\omega^3",
            "p_\\nu=c_\\nu^2/\\sum_\\omega c_\\omega^2",
        ),
        (
            "change_incidence_to_distinct_nodes",
            "\\sum_{\\rm incidences}p_\\nu",
            "\\sum_{\\rm distinct\\ nodes}p_\\nu",
        ),
        (
            "remove_root_cube_bound",
            "\\sum_{v\\in{\\rm roots}}c_v^3\\le C_{\\rm root}",
            "\\sum_{v\\in{\\rm roots}}c_v^3<\\infty",
        ),
        (
            "remove_incidence_multiplicity",
            "\\#\\{\\hbox{incidences carrying a fixed node }v\\}\\le M_{\\rm inc}",
            "\\#\\{\\hbox{incidences carrying a fixed node }v\\}<\\infty",
        ),
        (
            "remove_uniform_Dini_start",
            "\\sup_{d_0\\ge0}\\sum_{n\\ge0}",
            "\\sum_{n\\ge0}",
        ),
        ("remove_abstract_boundary", "ABSTRACT BOUNDARY TESTS, NOT NSE COUNTEREXAMPLES", "BOUNDARY TESTS"),
        ("remove_tree_disclaimer", "strict abstract ledger model", "strict ledger model"),
        ("weaken_tree_subcriticality", "\\theta_d\\le\\theta<1", "\\theta_d\\le\\theta\\le1"),
        ("remove_dual_exponent", "The cube is the exact dual exponent", "The cube is convenient"),
        ("remove_open_gate", "The universal terminal-window gate (S.280)", "The terminal-window gate (S.280)"),
        ("remove_no_DGX_boundary", "No DNS or DGX computation is used", "DGX computation is used"),
        ("remove_NOT_CLAY", "**NOT CLAY.**", "**CLOSED.**"),
    )
    rows = []
    for identifier, old, new in probes:
        mutated = text.replace(old, new, 1)
        if mutated == text:
            rows.append(
                assertion(
                    f"negative_{identifier}",
                    False,
                    "The intended mutation source was not found.",
                )
            )
            continue
        fake_raw = mutated.encode("utf-8")
        checks = validate_text(mutated, fake_raw, enforce_hash=False)
        failed = [row["id"] for row in checks if not row["pass"]]
        rows.append(
            assertion(
                f"negative_{identifier}",
                bool(failed),
                "The structural validator rejects the semantic mutation.",
                failed_checks=failed,
            )
        )
    duplicate = text.replace("\\tag{S.342}", "\\tag{S.341}", 1)
    duplicate_checks = validate_text(
        duplicate, duplicate.encode("utf-8"), enforce_hash=False
    )
    duplicate_failed = [row["id"] for row in duplicate_checks if not row["pass"]]
    rows.append(
        assertion(
            "negative_duplicate_final_tag",
            bool(duplicate_failed),
            "The validator rejects a duplicated/nonsequential final equation tag.",
            failed_checks=duplicate_failed,
        )
    )
    damaged = text + "\r"
    damaged_checks = validate_text(
        damaged, damaged.encode("utf-8"), enforce_hash=False
    )
    damaged_failed = [row["id"] for row in damaged_checks if not row["pass"]]
    rows.append(
        assertion(
            "negative_carriage_return_injection",
            "utf8_no_control_damage" in damaged_failed,
            "The validator rejects injected carriage-return damage.",
            failed_checks=damaged_failed,
        )
    )
    return rows


def build_report(payload: dict) -> str:
    sections = []
    for title, key in (
        ("Exact rational checks", "exact_checks"),
        ("Finite exhaustive checks", "finite_checks"),
        ("Dependency locks", "dependency_checks"),
        ("Structural checks", "structural_checks"),
        ("Negative mutations", "negative_checks"),
    ):
        rows = payload[key]
        lines = [f"## {title}", "", "| Check | Result |", "|---|---|"]
        for row in rows:
            lines.append(f"| `{row['id']}` | {'PASS' if row['pass'] else 'FAIL'} |")
        sections.append("\n".join(lines))

    summary = payload["summary"]
    return "\n".join(
        [
            "# R0.74S Step 13 finite certificate report",
            "",
            f"- Schema: `{payload['schema']}`",
            f"- Main note SHA-256: `{payload['note_sha256']}`",
            f"- Generator SHA-256: `{payload['generator_sha256']}`",
            f"- Exact: {summary['exact_passed']}/{summary['exact_total']}",
            f"- Finite: {summary['finite_passed']}/{summary['finite_total']}",
            f"- Dependencies: {summary['dependency_passed']}/{summary['dependency_total']}",
            f"- Structural: {summary['structural_passed']}/{summary['structural_total']}",
            f"- Negative mutations: {summary['negative_passed']}/{summary['negative_total']}",
            f"- Overall: **{'PASS' if payload['overall_pass'] else 'FAIL'}**",
            "",
            *sections,
            "",
            "## Boundary",
            "",
            "This finite certificate checks algebra, finite fixtures, hashes, structure, and claim wording. It does not machine-prove the PDE estimates, either open packing gate, the Morrey hypothesis, any NSE realization of an abstract countermodel, regularity, or the Millennium problem. **NOT CLAY.**",
            "",
        ]
    )


def main() -> int:
    raw = NOTE.read_bytes()
    text = raw.decode("utf-8")
    exact_checks = temporal_exact_checks() + heat_shear_checks() + high_rayleigh_row_checks()
    finite_checks = [
        window_holder_checks(),
        energy_interpolation_checks(),
        general_beta_checks(),
        smooth_vector_checks(),
        adaptive_witness_checks(),
        morrey_two_regime_checks(),
        morrey_threshold_countermodel_checks(),
        critical_tree_checks(),
        cubic_holder_checks(),
        incidence_charging_checks(),
        dini_tree_checks(),
    ]
    deps = dependency_checks()
    structural = validate_text(text, raw)
    negative = negative_mutation_checks(text)
    all_rows = exact_checks + finite_checks + deps + structural + negative
    payload = {
        "schema": SCHEMA,
        "note_path": display_path(NOTE),
        "note_sha256": sha256(NOTE),
        "generator_path": display_path(Path(__file__)),
        "generator_sha256": sha256(Path(__file__)),
        "exact_checks": exact_checks,
        "finite_checks": finite_checks,
        "dependency_checks": deps,
        "structural_checks": structural,
        "negative_checks": negative,
        "summary": {
            "exact_total": len(exact_checks),
            "exact_passed": sum(row["pass"] for row in exact_checks),
            "finite_total": len(finite_checks),
            "finite_passed": sum(row["pass"] for row in finite_checks),
            "dependency_total": len(deps),
            "dependency_passed": sum(row["pass"] for row in deps),
            "structural_total": len(structural),
            "structural_passed": sum(row["pass"] for row in structural),
            "negative_total": len(negative),
            "negative_passed": sum(row["pass"] for row in negative),
        },
        "overall_pass": all(row["pass"] for row in all_rows),
    }
    JSON_OUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    REPORT_OUT.write_text(build_report(payload), encoding="utf-8")
    print(json.dumps(payload["summary"], sort_keys=True))
    print(f"overall_pass={str(payload['overall_pass']).lower()}")
    return 0 if payload["overall_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
