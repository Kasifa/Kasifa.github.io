#!/usr/bin/env python3
"""Deterministic finite certificate for R0.74S Step 10.

This standard-library-only producer checks exact rational clock algebra,
the D-first paid/residual truth table, best-N quantifiers, finite-shell
limits, source/claim boundaries, and rejection of dangerous mutations in
``r074s_paid_branch_last_exit_residual.md``.

It does not machine-prove the inherited local-energy identities, the
shell-dependent PDE payment estimates, a fixed-N PDE packing theorem,
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
        "R074S_PAID_BRANCH_NOTE",
        REPO / "research/r074s_paid_branch_last_exit_residual.md",
    )
)
JSON_OUT = Path(
    os.environ.get(
        "R074S_PAID_BRANCH_JSON",
        REPO / "research/r074s_paid_branch_last_exit_certificate.json",
    )
)
REPORT_OUT = Path(
    os.environ.get(
        "R074S_PAID_BRANCH_REPORT",
        REPO / "research/r074s_paid_branch_last_exit_certificate_report.md",
    )
)

LOCKED_NOTE_SHA256 = (
    "9eb5f2a794021b49894adfc167d350f58d93c266e6be319ce835c58db2e0d74c"
)
SCHEMA = "r074s-paid-branch-last-exit-certificate-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO.resolve()))
    except ValueError:
        return str(path.resolve())


def fs(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def powerset_indices(length: int, max_size: int | None = None):
    upper = length if max_size is None else min(length, max_size)
    for size in range(upper + 1):
        yield from itertools.combinations(range(length), size)


def best_n_bruteforce(values: tuple[Fraction, ...], nterm: int) -> Fraction:
    if any(value < 0 for value in values):
        raise ValueError("Step 10 best-N fixtures must be nonnegative")
    candidates = []
    for removed in powerset_indices(len(values), nterm):
        removed_set = set(removed)
        candidates.append(
            sum(
                (value for index, value in enumerate(values) if index not in removed_set),
                Fraction(0),
            )
        )
    return min(candidates)


def best_n_formula(values: tuple[Fraction, ...], nterm: int) -> Fraction:
    ordered = sorted(values, reverse=True)
    return sum(ordered[min(nterm, len(ordered)) :], Fraction(0))


def exact(identifier: str, left: Fraction, right: Fraction, note: str) -> dict:
    return {
        "id": identifier,
        "left": fs(left),
        "right": fs(right),
        "margin": fs(left - right),
        "note": note,
        "pass": left == right,
    }


def exact_checks() -> list[dict]:
    theta = Fraction(2, 3)
    epsilon = Fraction(1, 60)
    lower_residual = Fraction(1, 3) - (Fraction(1, 6) - epsilon)
    upper_residual = Fraction(1, 3) - (-Fraction(1, 6) + epsilon)
    return [
        exact(
            "two_thirds_last_exit_clock_increment",
            Fraction(1) - theta,
            Fraction(1, 3),
            "S.223: Delta K=(1-theta)T=T/3.",
        ),
        exact(
            "positive_q_residual_lower_margin",
            lower_residual - Fraction(1, 6),
            epsilon,
            "The positive-Q fixture approaches r=T/6 from above.",
        ),
        exact(
            "negative_q_residual_upper_margin",
            Fraction(1, 2) - upper_residual,
            epsilon,
            "The negative-Q fixture approaches r=T/2 from below.",
        ),
        exact(
            "lambda_four_exact_long_boundary",
            Fraction(1, 8) ** 2 * Fraction(4) ** 3,
            Fraction(1),
            "d=lambda^(-3/2) is encoded without floating-point roots.",
        ),
        exact(
            "long_payment_lambda_recovery",
            Fraction(1, 8) ** 2 * Fraction(4) ** 3,
            Fraction(1),
            "The duration exponent recovers one factor of lambda after 2/3 power.",
        ),
        exact(
            "C_LE_is_strictly_below_C4_by_cubes",
            Fraction(12**3 * 2**2, 6**3),
            Fraction(32),
            "C4^3/CLE^3=32, so CLE<C4 for C1>0.",
        ),
        exact(
            "one_Q_ledger_sharp_pair",
            Fraction(12 + 12),
            Fraction(6 * (2 + 2)),
            "One P_beta shell and one P_Q shell saturate a single 6 B_Q ledger.",
        ),
        exact(
            "one_cubic_ledger_Holder_equality",
            Fraction((1 + 1) ** 3),
            Fraction((1**3 + 1**3) * (1**3 + 1**3) ** 2),
            "One P_sigma and one P_LE coordinate saturate combined Holder.",
        ),
        exact(
            "plateau_Q_coefficient",
            Fraction(1 + 6),
            Fraction(7),
            "S.241 combines one inherited B_Q with the six-unit paid ledger.",
        ),
        exact(
            "small_payment_fallback",
            Fraction(1, 8),
            Fraction(1, 4) - Fraction(1, 8),
            "For P=1/8, A=P^(2/3)=1/4 and A-P=1/8.",
        ),
        exact(
            "D_persistence_fixture_terminal_excess",
            Fraction(1) - Fraction(3, 5),
            Fraction(2, 5),
            "The S.247 terminal clock has E(tau)=2/5.",
        ),
        exact(
            "D_persistence_fixture_early_excess",
            Fraction(67, 100) - Fraction(3, 5),
            Fraction(7, 100),
            "At t=1 the D-dominated fixture has E=7/100<T/6.",
        ),
    ]


BRANCHES = ("P_beta", "P_sigma", "P_LE", "P_Q", "R_sh", "R_x")


def predicate_memberships(
    d_side: bool,
    beta_side: bool,
    sigma_side: bool,
    long_side: bool,
    q_large_side: bool,
) -> dict[str, bool]:
    """Evaluate the six sets directly, including the D-first priority."""
    return {
        "P_beta": d_side and beta_side,
        "P_sigma": d_side and (not beta_side) and sigma_side,
        "P_LE": (not d_side) and long_side,
        "P_Q": (not d_side) and (not long_side) and q_large_side,
        "R_sh": (not d_side) and (not long_side) and (not q_large_side),
        "R_x": d_side and (not beta_side) and (not sigma_side),
    }


def numeric_branch(
    *,
    terminal: Fraction,
    dissipation: Fraction,
    beta: Fraction,
    sigma: Fraction,
    duration: Fraction,
    q_increment: Fraction,
    lam: Fraction = Fraction(1),
    duration_threshold: Fraction = Fraction(1),
) -> tuple[str, ...]:
    if terminal <= 0:
        return ()
    d_side = dissipation >= terminal / 2
    beta_side = beta >= terminal / 6
    sigma_side = sigma > terminal / (12 * lam)
    long_side = duration >= duration_threshold
    q_large_side = abs(q_increment) >= terminal / 6
    memberships = predicate_memberships(
        d_side, beta_side, sigma_side, long_side, q_large_side
    )
    return tuple(branch for branch in BRANCHES if memberships[branch])


def truth_table_and_boundary_fixtures() -> dict:
    predicate_failures = []
    branch_counts = {branch: 0 for branch in BRANCHES}
    configurations = 0
    for predicates in itertools.product((False, True), repeat=5):
        configurations += 1
        memberships = predicate_memberships(*predicates)
        selected = [branch for branch, present in memberships.items() if present]
        if len(selected) == 1:
            branch_counts[selected[0]] += 1
        elif len(predicate_failures) < 8:
            predicate_failures.append(
                {"predicates": list(predicates), "selected": selected}
            )

    F = Fraction
    fixtures = (
        {
            "id": "zero_terminal",
            "args": (F(0), F(0), F(0), F(0), F(0), F(0)),
            "expected": (),
        },
        {
            "id": "D_beta_equal_priority_over_all_other_tests",
            "args": (F(12), F(6), F(2), F(2), F(1), F(2)),
            "expected": ("P_beta",),
        },
        {
            "id": "D_sigma_strict",
            "args": (F(12), F(6), F(1), F(3, 2), F(1), F(1)),
            "expected": ("P_sigma",),
        },
        {
            "id": "D_sigma_equal_falls_to_Rx",
            "args": (F(12), F(6), F(3, 2), F(1), F(1, 2), F(3, 2)),
            "expected": ("R_x",),
        },
        {
            "id": "nonD_long_equal_precedes_Q_split",
            "args": (F(12), F(5), F(2), F(2), F(1), F(2)),
            "expected": ("P_LE",),
        },
        {
            "id": "nonD_short_positive_Q_equal",
            "args": (F(12), F(5), F(2), F(0), F(1, 2), F(2)),
            "expected": ("P_Q",),
        },
        {
            "id": "nonD_short_negative_Q_equal",
            "args": (F(12), F(5), F(2), F(0), F(1, 2), F(-2)),
            "expected": ("P_Q",),
        },
        {
            "id": "nonD_short_positive_Q_small",
            "args": (F(12), F(5), F(3, 2), F(0), F(1, 2), F(3, 2)),
            "expected": ("R_sh",),
        },
        {
            "id": "nonD_short_negative_Q_small",
            "args": (F(12), F(5), F(3, 2), F(0), F(1, 2), F(-3, 2)),
            "expected": ("R_sh",),
        },
    )
    fixture_rows = []
    fixture_failures = []
    for fixture in fixtures:
        terminal, dissipation, beta, sigma, duration, q_increment = fixture["args"]
        actual = numeric_branch(
            terminal=terminal,
            dissipation=dissipation,
            beta=beta,
            sigma=sigma,
            duration=duration,
            q_increment=q_increment,
        )
        residual = terminal / 3 - q_increment if actual in (("R_x",), ("R_sh",)) else F(0)
        residual_ok = (
            terminal / 6 < residual < terminal / 2
            if actual in (("R_x",), ("R_sh",))
            else residual == 0
        )
        passed = actual == fixture["expected"] and residual_ok
        row = {
            "id": fixture["id"],
            "terminal": fs(terminal),
            "dissipation": fs(dissipation),
            "beta": fs(beta),
            "sigma": fs(sigma),
            "duration": fs(duration),
            "delta_Q": fs(q_increment),
            "expected": list(fixture["expected"]),
            "actual": list(actual),
            "residual": fs(residual),
            "pass": passed,
        }
        fixture_rows.append(row)
        if not passed:
            fixture_failures.append(row)

    low_rayleigh_sigma = Fraction(1, 8) + Fraction(1, 96)
    low_rayleigh_excluded_from_x = low_rayleigh_sigma > Fraction(1, 12)
    passed = (
        not predicate_failures
        and not fixture_failures
        and all(branch_counts[branch] > 0 for branch in BRANCHES)
        and low_rayleigh_excluded_from_x
    )
    return {
        "id": "D_first_full_truth_table_and_boundary_fixtures",
        "predicate_configurations_checked": configurations,
        "branch_counts": branch_counts,
        "boundary_fixture_count": len(fixtures),
        "boundary_rows": fixture_rows,
        "low_Rayleigh_sigma": fs(low_rayleigh_sigma),
        "failures": predicate_failures + fixture_failures,
        "pass": passed,
    }


def level_intersections(
    path: tuple[tuple[Fraction, Fraction], ...], level: Fraction
) -> tuple[Fraction, ...]:
    hits = []
    for time, value in path:
        if value == level:
            hits.append(time)
    for (left_time, left_value), (right_time, right_value) in zip(path, path[1:]):
        if left_value == right_value:
            if left_value == level:
                hits.extend((left_time, right_time))
            continue
        ratio = (level - left_value) / (right_value - left_value)
        if 0 <= ratio <= 1:
            hits.append(left_time + ratio * (right_time - left_time))
    return tuple(sorted(set(hits)))


def last_exit_fixture() -> dict:
    F = Fraction
    fixtures = (
        (
            "oscillatory_last_not_first",
            ((F(0), F(0)), (F(1), F(10)), (F(2), F(7)), (F(3), F(8)), (F(4), F(12))),
            F(4, 5),
            F(3),
        ),
        (
            "level_plateau_uses_right_endpoint",
            ((F(0), F(0)), (F(1), F(8)), (F(2), F(8)), (F(3), F(12))),
            F(1),
            F(2),
        ),
        (
            "monotone_fractional_crossing",
            ((F(0), F(0)), (F(1), F(4)), (F(2), F(12))),
            F(3, 2),
            F(3, 2),
        ),
    )
    rows = []
    failures = []
    for identifier, path, expected_first, expected_last in fixtures:
        terminal = path[-1][1]
        level = Fraction(2, 3) * terminal
        hits = level_intersections(path, level)
        first_exit = min(hits)
        last_exit = max(hits)
        passed = (
            first_exit == expected_first
            and last_exit == expected_last
            and terminal - level == terminal / 3
        )
        row = {
            "id": identifier,
            "level": fs(level),
            "first_exit": fs(first_exit),
            "last_exit": fs(last_exit),
            "expected_first": fs(expected_first),
            "expected_last": fs(expected_last),
            "delta_K": fs(terminal - level),
            "pass": passed,
        }
        rows.append(row)
        if not passed:
            failures.append(row)
    return {
        "id": "two_thirds_last_exit_not_first_exit_fixtures",
        "configurations_checked": len(fixtures),
        "rows": rows,
        "failures": failures,
        "pass": not failures and rows[0]["first_exit"] != rows[0]["last_exit"],
    }


def residual_sharp_limit_fixtures() -> dict:
    epsilons = tuple(Fraction(1, denominator) for denominator in (12, 60, 600, 6000))
    rows = []
    failures = []
    previous_lower_gap = None
    previous_upper_gap = None
    for epsilon in epsilons:
        q_positive = Fraction(1, 6) - epsilon
        q_negative = -Fraction(1, 6) + epsilon
        r_lower = Fraction(1, 3) - q_positive
        r_upper = Fraction(1, 3) - q_negative
        lower_gap = r_lower - Fraction(1, 6)
        upper_gap = Fraction(1, 2) - r_upper
        passed = (
            abs(q_positive) < Fraction(1, 6)
            and abs(q_negative) < Fraction(1, 6)
            and lower_gap == epsilon
            and upper_gap == epsilon
            and Fraction(1, 6) < r_lower < Fraction(1, 2)
            and Fraction(1, 6) < r_upper < Fraction(1, 2)
            and (previous_lower_gap is None or lower_gap < previous_lower_gap)
            and (previous_upper_gap is None or upper_gap < previous_upper_gap)
        )
        row = {
            "epsilon": fs(epsilon),
            "positive_delta_Q": fs(q_positive),
            "lower_residual": fs(r_lower),
            "negative_delta_Q": fs(q_negative),
            "upper_residual": fs(r_upper),
            "lower_boundary_gap": fs(lower_gap),
            "upper_boundary_gap": fs(upper_gap),
            "pass": passed,
        }
        rows.append(row)
        if not passed:
            failures.append(row)
        previous_lower_gap = lower_gap
        previous_upper_gap = upper_gap
    return {
        "id": "signed_delta_Q_sharp_residual_limits",
        "configurations_checked": len(rows),
        "rows": rows,
        "failures": failures,
        "pass": not failures,
    }


def one_q_ledger_fixture() -> dict:
    shells = (
        {"branch": "P_beta", "T": Fraction(12), "variation": Fraction(2)},
        {"branch": "P_Q", "T": Fraction(12), "variation": Fraction(2)},
        {"branch": "P_sigma", "T": Fraction(7), "variation": Fraction(3)},
    )
    q_shells = tuple(shell for shell in shells if shell["branch"] in ("P_beta", "P_Q"))
    terminal_sum = sum((shell["T"] for shell in q_shells), Fraction(0))
    used_variation = sum((shell["variation"] for shell in q_shells), Fraction(0))
    full_ledger = sum((shell["variation"] for shell in shells), Fraction(0))
    one_copy_bound = 6 * full_ledger
    sharp_restricted_bound = 6 * used_variation
    return {
        "id": "disjoint_Q_paid_rows_use_one_global_ledger",
        "Q_paid_shell_count": len(q_shells),
        "terminal_sum": fs(terminal_sum),
        "used_variation": fs(used_variation),
        "full_B_Q": fs(full_ledger),
        "sharp_restricted_bound": fs(sharp_restricted_bound),
        "one_copy_global_bound": fs(one_copy_bound),
        "pass": terminal_sum == sharp_restricted_bound and terminal_sum <= one_copy_bound,
    }


def cubic_holder_enumeration() -> dict:
    values = (Fraction(0), Fraction(1), Fraction(2))
    configurations = 0
    equality_cases = 0
    mixed_branch_equality = False
    failures = []
    for length in range(1, 5):
        for a_values in itertools.product(values, repeat=length):
            for b_values in itertools.product(values, repeat=length):
                configurations += 1
                left = sum((a * b * b for a, b in zip(a_values, b_values)), Fraction(0))
                coefficient_cube = sum((a**3 for a in a_values), Fraction(0))
                payment_base = sum((b**3 for b in b_values), Fraction(0))
                left_cube = left**3
                right_cube = coefficient_cube * payment_base**2
                if left_cube == right_cube:
                    equality_cases += 1
                    if length == 2 and a_values == (1, 1) and b_values == (1, 1):
                        mixed_branch_equality = True
                if left_cube > right_cube and len(failures) < 8:
                    failures.append(
                        {
                            "a": [fs(value) for value in a_values],
                            "b": [fs(value) for value in b_values],
                            "left_cube": fs(left_cube),
                            "right_cube": fs(right_cube),
                        }
                    )
    return {
        "id": "combined_Psigma_PLE_one_cubic_Holder_ledger",
        "configurations_checked": configurations,
        "equality_cases": equality_cases,
        "mixed_branch_labels": ["P_sigma", "P_LE"],
        "mixed_branch_equality_fixture": mixed_branch_equality,
        "failures": failures,
        "pass": not failures and mixed_branch_equality,
    }


def paid_deletion_best_n_enumeration() -> dict:
    # (terminal clock, residual, exact paid charge, label)
    options = (
        (Fraction(0), Fraction(0), Fraction(0), "zero"),
        (Fraction(1), Fraction(0), Fraction(1), "paid"),
        (Fraction(3), Fraction(0), Fraction(3), "paid"),
        (Fraction(3), Fraction(1), Fraction(0), "residual"),
        (Fraction(5), Fraction(1), Fraction(0), "residual"),
        (Fraction(1), Fraction(1, 4), Fraction(0), "residual"),
    )
    pointwise_checks = 0
    best_n_checks = 0
    reverse_checks = 0
    rearrangement_checks = 0
    failures = []
    for length in range(1, 5):
        for coordinates in itertools.product(options, repeat=length):
            terminal = tuple(item[0] for item in coordinates)
            residual = tuple(item[1] for item in coordinates)
            paid = sum((item[2] for item in coordinates), Fraction(0))
            for removed in powerset_indices(length):
                pointwise_checks += 1
                removed_set = set(removed)
                lhs = sum(
                    (value for index, value in enumerate(terminal) if index not in removed_set),
                    Fraction(0),
                )
                rhs = paid + 6 * sum(
                    (value for index, value in enumerate(residual) if index not in removed_set),
                    Fraction(0),
                )
                if lhs > rhs and len(failures) < 8:
                    failures.append(
                        {"kind": "pointwise", "T": [fs(x) for x in terminal], "r": [fs(x) for x in residual], "removed": list(removed), "left": fs(lhs), "right": fs(rhs)}
                    )
            for nterm in range(length + 2):
                best_n_checks += 1
                lhs = best_n_bruteforce(terminal, nterm)
                rhs = paid + 6 * best_n_bruteforce(residual, nterm)
                reverse_checks += 1
                reverse_lhs = best_n_bruteforce(residual, nterm)
                reverse_rhs = Fraction(1, 2) * best_n_bruteforce(terminal, nterm)
                rearrangement_checks += 2
                formula_ok = (
                    lhs == best_n_formula(terminal, nterm)
                    and reverse_lhs == best_n_formula(residual, nterm)
                )
                if (lhs > rhs or reverse_lhs > reverse_rhs or not formula_ok) and len(failures) < 8:
                    failures.append(
                        {
                            "kind": "best_N",
                            "T": [fs(x) for x in terminal],
                            "r": [fs(x) for x in residual],
                            "N": nterm,
                            "forward_left": fs(lhs),
                            "forward_right": fs(rhs),
                            "reverse_left": fs(reverse_lhs),
                            "reverse_right": fs(reverse_rhs),
                            "formula_ok": formula_ok,
                        }
                    )
    return {
        "id": "paid_deletion_same_set_and_best_N_enumeration",
        "pointwise_same_set_checks": pointwise_checks,
        "best_N_forward_checks": best_n_checks,
        "best_N_reverse_checks": reverse_checks,
        "rearrangement_checks": rearrangement_checks,
        "failures": failures,
        "pass": not failures,
    }


def quantifier_fixtures() -> dict:
    residual_x = (Fraction(1), Fraction(0))
    residual_short = (Fraction(0), Fraction(1))
    combined = tuple(x + y for x, y in zip(residual_x, residual_short))
    shared_n = best_n_bruteforce(combined, 1)
    duplicated_n = best_n_bruteforce(residual_x, 1) + best_n_bruteforce(residual_short, 1)

    states = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
    sup_inf = max(best_n_bruteforce(state, 1) for state in states)
    fixed_set_costs = []
    for removed in powerset_indices(2, 1):
        removed_set = set(removed)
        fixed_set_costs.append(
            max(
                sum((x for index, x in enumerate(state) if index not in removed_set), Fraction(0))
                for state in states
            )
        )
    inf_sup = min(fixed_set_costs)

    terminal = (Fraction(3), Fraction(3))
    residual = (Fraction(1), Fraction(1))
    paid_deletion_left = best_n_bruteforce(terminal, 1)
    paid_deletion_right = 6 * best_n_bruteforce(residual, 1)
    passed = (
        shared_n == 1
        and duplicated_n == 0
        and sup_inf == 0
        and inf_sup == 1
        and paid_deletion_left == 3
        and paid_deletion_right == 6
    )
    return {
        "id": "shared_N_and_sup_inf_quantifier_witnesses",
        "shared_combined_tail": fs(shared_n),
        "forbidden_branchwise_tail_sum": fs(duplicated_n),
        "sup_tau_inf_S": fs(sup_inf),
        "inf_S_sup_tau": fs(inf_sup),
        "paid_deletion_left": fs(paid_deletion_left),
        "paid_deletion_right": fs(paid_deletion_right),
        "pass": passed,
    }


def fixed_n_truncation_fixtures() -> dict:
    rows = []
    failures = []
    for shell_count in range(1, 17):
        prefix = tuple(Fraction(1, 2**index) for index in range(1, shell_count + 1))
        fixed_one = best_n_bruteforce(prefix, 1)
        expected_fixed_one = Fraction(1, 2) - Fraction(1, 2**shell_count)
        growing = best_n_bruteforce(prefix, shell_count)
        ones = tuple(Fraction(1) for _ in range(shell_count))
        fixed_two = best_n_bruteforce(ones, 2)
        expected_fixed_two = Fraction(max(shell_count - 2, 0))
        passed = (
            fixed_one == expected_fixed_one
            and growing == 0
            and fixed_two == expected_fixed_two
        )
        row = {
            "M": shell_count,
            "S1_geometric_prefix": fs(fixed_one),
            "expected_S1": fs(expected_fixed_one),
            "SM_geometric_prefix": fs(growing),
            "S2_ones": fs(fixed_two),
            "pass": passed,
        }
        rows.append(row)
        if not passed:
            failures.append(row)
    return {
        "id": "fixed_N_finite_to_infinite_and_growing_budget_fixtures",
        "configurations_checked": len(rows),
        "infinite_S1_limit": fs(Fraction(1, 2)),
        "rows": rows,
        "failures": failures,
        "pass": not failures and rows[-1]["S1_geometric_prefix"] != "0/1",
    }


def full_history_interval_fixtures() -> dict:
    F = Fraction
    beta_correct = numeric_branch(
        terminal=F(12), dissipation=F(6), beta=F(2), sigma=F(0),
        duration=F(1, 2), q_increment=F(0),
    )
    beta_mutated = numeric_branch(
        terminal=F(12), dissipation=F(6), beta=F(0), sigma=F(0),
        duration=F(1, 2), q_increment=F(0),
    )
    sigma_correct = numeric_branch(
        terminal=F(12), dissipation=F(6), beta=F(1), sigma=F(3, 2),
        duration=F(1, 2), q_increment=F(0),
    )
    sigma_mutated = numeric_branch(
        terminal=F(12), dissipation=F(6), beta=F(1), sigma=F(0),
        duration=F(1, 2), q_increment=F(0),
    )
    # On I_x, beta(J_tau)<T/6 controls the smaller last-exit interval.
    beta_full = F(3, 2)
    beta_last_exit = F(1)
    q_increment = F(-1)
    nesting_ok = abs(q_increment) <= beta_last_exit <= beta_full < F(2)
    return {
        "id": "full_history_beta_sigma_not_last_exit_fixtures",
        "beta_full_branch": list(beta_correct),
        "beta_last_exit_mutation_branch": list(beta_mutated),
        "sigma_full_branch": list(sigma_correct),
        "sigma_last_exit_mutation_branch": list(sigma_mutated),
        "nested_beta_chain": {
            "abs_delta_Q": fs(abs(q_increment)),
            "beta_J_LE": fs(beta_last_exit),
            "beta_J_tau": fs(beta_full),
            "T_over_6": fs(F(2)),
        },
        "pass": (
            beta_correct == ("P_beta",)
            and beta_mutated == ("R_x",)
            and sigma_correct == ("P_sigma",)
            and sigma_mutated == ("R_x",)
            and nesting_ok
        ),
    }


def interpolate(
    path: tuple[tuple[Fraction, Fraction], ...], time: Fraction
) -> Fraction:
    for (left_time, left_value), (right_time, right_value) in zip(path, path[1:]):
        if left_time <= time <= right_time:
            if right_time == left_time:
                return right_value
            ratio = (time - left_time) / (right_time - left_time)
            return left_value + ratio * (right_value - left_value)
    if time == path[-1][0]:
        return path[-1][1]
    raise ValueError("time lies outside path")


def d_persistence_counterexample() -> dict:
    F = Fraction
    times = (F(0), F(1, 8), F(1, 4), F(1), F(2))
    k_values = (F(0), F(3, 5), F(2, 3), F(67, 100), F(1))
    d_values = (F(0), F(3, 5), F(3, 5), F(3, 5), F(3, 5))
    k_path = tuple(zip(times, k_values))
    d_path = tuple(zip(times, d_values))
    level = F(2, 3)
    exits = level_intersections(k_path, level)
    last_exit = max(exits)
    terminal_d = d_values[-1]
    nonnegative_excess_at_vertices = all(k >= d for k, d in zip(k_values, d_values))
    monotone_d = all(left <= right for left, right in zip(d_values, d_values[1:]))
    early_times = (F(1, 4), F(1, 2), F(1))
    early_excess = tuple(
        interpolate(k_path, time) - interpolate(d_path, time) for time in early_times
    )
    early_interval_below = max(early_excess) < F(1, 6)
    passed = (
        last_exit == F(1, 4)
        and times[-1] - last_exit == F(7, 4)
        and terminal_d >= F(1, 2)
        and d_values[2] == d_values[-1]
        and nonnegative_excess_at_vertices
        and monotone_d
        and early_interval_below
    )
    return {
        "id": "terminal_D_dominance_does_not_persist_on_last_exit_interval",
        "last_exit": fs(last_exit),
        "normalized_duration": fs(times[-1] - last_exit),
        "terminal_D": fs(terminal_d),
        "delta_D_after_last_exit": fs(d_values[-1] - d_values[2]),
        "early_times": [fs(time) for time in early_times],
        "early_excess": [fs(value) for value in early_excess],
        "T_over_6": fs(F(1, 6)),
        "nonnegative_excess_at_vertices": nonnegative_excess_at_vertices,
        "D_nondecreasing": monotone_d,
        "pass": passed,
    }


def finite_checks() -> list[dict]:
    return [
        truth_table_and_boundary_fixtures(),
        last_exit_fixture(),
        residual_sharp_limit_fixtures(),
        one_q_ledger_fixture(),
        cubic_holder_enumeration(),
        paid_deletion_best_n_enumeration(),
        quantifier_fixtures(),
        fixed_n_truncation_fixtures(),
        full_history_interval_fixtures(),
        d_persistence_counterexample(),
    ]


def section(body: str, start: str, end: str) -> str:
    if start not in body or end not in body:
        return ""
    return body.split(start, 1)[1].split(end, 1)[0]


STRUCTURAL_SENTINELS = (
    ("scope_not_clay", "No fixed universal \\(N_0\\), residual"),
    ("fixed_profile_quantifiers", "independently\nof \\(R\\), \\(\\tau\\), and the solution"),
    ("canonical_last_exit_is_max", r":=\max\{t\in[s_R,\tau]:K_{k,R}(t)\le2T_k/3\}"),
    ("last_exit_strict_after_stop", r"K_{k,R}(t)> {2T_k\over3}"),
    ("delta_F_has_minus_delta_Q", r"\Delta F_k={T_k\over3}-\Delta Q_k"),
    ("positive_terminal_restriction", "All displayed sets in this paragraph are restricted to \\(T_k>0\\)."),
    ("long_boundary_formula", r"\mathcal I_{\rm long}(\tau)&:=\{k:d_k\ge\lambda_k^{-3/2}\}"),
    ("short_boundary_formula", r"\mathcal I_{\rm short}(\tau)&:=\{k:d_k<\lambda_k^{-3/2}\}"),
    ("Q_large_boundary_formula", r"\mathcal I_{Q+}(\tau)&:=\{k:|\Delta Q_k|\ge T_k/6\}"),
    ("Q_small_boundary_formula", r"\mathcal I_{Q-}(\tau)&:=\{k:|\Delta Q_k|<T_k/6\}"),
    ("D_boundary_formula", r"\mathcal I_D(\tau)&:=\{k:D_{k,R}(\tau)\ge T_k/2\}"),
    ("nonD_boundary_formula", r"\mathcal I_{\neg D}(\tau)&:=\{k:D_{k,R}(\tau)<T_k/2\}"),
    ("boundary_assignment_sentence", "Equality is assigned to the long, absolute-\\(Q\\)-large, and\ndissipation-dominated sides."),
    ("full_history_not_last_exit", "using\n\\(J_\\tau=(s_R,\\tau)\\), not the last-exit interval"),
    ("beta_boundary_formula", r"\beta_{k,R}(J_\tau)\ge T_k/6"),
    ("sigma_strict_boundary_formula", r"\sigma_{k,R}(J_\tau)>T_k/(12\lambda_k)"),
    ("D_first_priority", "*D-first* priority rule"),
    ("absolute_Q_meaning", "means *absolute-\\(Q\\)-large*, not positive-sign \\(Q\\)"),
    ("low_Rayleigh_no_double_charge", r"\mathcal I_{\rm lo}\setminus(\mathcal I_\beta\cup\mathcal I_\sigma)=\varnothing"),
    ("one_6BQ_statement", "Thus the correct coefficient is one copy of \\(6B_Q\\), not \\(12B_Q\\)."),
    ("a.e_nonD_persistence", "for almost every local-energy\ngood time \\(t\\in J_k^{\\rm LE}\\)"),
    ("stop_value_not_used", "No value of \\(E_k\\) or \\(D_k\\) at the possibly non-good stop \\(\\ell_k\\)\nis used."),
    ("shell_dependent_sets", "expressly permits a different measurable time set for every shell"),
    ("one_C5_statement", "estimating\nthem as two complete global ledgers would lose an unnecessary second copy\nof \\(C_5\\)."),
    ("residual_union", r"\mathcal I_{\rm res}(\tau):=\mathcal R_{\rm sh}\cup\mathcal R_x"),
    ("Ix_beta_nesting", r"|\Delta Q_k|\le\beta_{k,R}(J_k^{\rm LE})\le\beta_{k,R}(J_\tau)<{T_k\over6}"),
    ("residual_strict_two_sided", r"{T_k\over6}<r_{k,R}^{\boldsymbol\lambda}(\tau)<{T_k\over2}"),
    ("finite_Holder_before_monotone_limit", "Use finite-shell Hölder first and then the inherited estimate (R.211)"),
    ("monotone_convergence_for_infinite_shells", "monotone convergence yields"),
    ("best_N_nonnegative_domain", "For a nonnegative \\(\\ell^1\\) vector \\(x\\), recall"),
    ("best_N_infimum_formula", r"\mathcal S_N(x)=\inf_{S\subset\mathbb N,\,\#S\le N}\sum_{k\notin S}x_k"),
    ("same_set_before_infimum", "apply (S.235) to those same sets"),
    ("one_shared_N", "There is one exceptional set of size at most \\(N\\) for the *combined*\nresidual."),
    ("good_terminal_residual_gate", r"\sup_{\tau\in\mathcal D\cap\mathcal G_R}"),
    ("K_only_domain_closure", "Only the inherited \\(\\ell^1\\)-continuity of the\nterminal \\(K\\)-vector is used"),
    ("reverse_half_tail", r"\mathfrak R_{N,R}^{\boldsymbol\lambda}(\mathcal D)\le{1\over2}\mathcal S_{N,R}^{K}(\mathcal D)"),
    ("fixed_N_equivalence", "For a fixed integer\n\\(N_0\\), independent of the scale and the solution"),
    ("plateau_not_full", "The plateau estimate is not a full-terminal statement."),
    ("full_gate_explicitly_open", r"\text{OPEN: there exist fixed }N_0<\infty, C_{\rm res}<\infty"),
    ("plateau_does_not_give_Q12", "a proof of the residual bound only on\n\\(I_R\\) yields (S.241), not full Q.12."),
    ("sharp_Q_equality_paid", "At \\(|\\Delta Q|=T/6\\), a short non-\\(D\\) shell\nbelongs to \\(\\mathcal P_Q\\)"),
    ("fixed_N_not_truncation_budget", "fixed \\(N\\) cannot be replaced by a truncation-dependent budget"),
    ("D_persistence_invalid", "It would be invalid to apply the long non-\\(D\\) proof to\n\\(\\mathcal I_D\\)."),
    ("double_charge_truth_boundary", "those separate double charges are valid but nonsharp and are not used;"),
    ("open_claim_heading", "The following remain **OPEN**:"),
    ("not_claimed_heading", "The following are **NOT CLAIMED**:"),
    ("selector_regularities_not_claimed", "continuity, measurability, or lower semicontinuity in \\(\\tau\\)"),
    ("full_history_redefinition_not_claimed", "may be\n  redefined on \\(J_k^{\\rm LE}\\)"),
    ("plateau_full_not_identified", "that \\(I_R\\) and \\(\\mathcal T_R\\) give the same terminal supremum"),
    ("final_not_clay", "**NOT CLAY.**"),
)


def structural_checks(
    body: str,
    source_bytes: bytes | None = None,
    enforce_lock: bool = True,
) -> list[dict]:
    checks = []
    body_hash = hashlib.sha256(
        source_bytes if source_bytes is not None else body.encode("utf-8")
    ).hexdigest()
    checks.append(
        {
            "id": "locked_note_sha256",
            "actual": body_hash,
            "expected": LOCKED_NOTE_SHA256,
            "enforced": enforce_lock,
            "pass": body_hash == LOCKED_NOTE_SHA256 if enforce_lock else True,
        }
    )

    tags = re.findall(r"\\tag\{S\.(\d+)\}", body)
    expected_tags = [str(number) for number in range(223, 248)]
    display_left = len(re.findall(r"(?m)^\\\[\s*$", body))
    display_right = len(re.findall(r"(?m)^\\\]\s*$", body))
    checks.extend(
        [
            {"id": "S223_S247_tags_consecutive", "actual": tags, "expected": expected_tags, "pass": tags == expected_tags},
            {"id": "S223_S247_tags_unique", "tag_count": len(tags), "unique_count": len(set(tags)), "pass": len(tags) == len(set(tags)) == len(expected_tags)},
            {"id": "display_math_line_delimiters_balanced", "left_count": display_left, "right_count": display_right, "pass": display_left == display_right},
            {"id": "inline_math_delimiters_balanced", "left_count": body.count("\\("), "right_count": body.count("\\)"), "pass": body.count("\\(") == body.count("\\)")},
            {"id": "no_disallowed_control_or_zero_width_characters", "pass": not any((ord(character) < 32 and character not in "\n\t") or character in "\u200b\u200c\u200d\ufeff" for character in body)},
            {"id": "no_tabs_or_trailing_whitespace", "pass": "\t" not in body and all(line == line.rstrip() for line in body.splitlines())},
        ]
    )

    required_headings = (
        "## 0. Result and scope",
        "## 1. Inherited setting and the \\(2/3\\)-last exit",
        "## 2. The exact paid/residual partition",
        "## 3. The two already-paid ledgers",
        "## 4. The residual stopped-flux vector",
        "## 5. Paid-branch deletion and the best-\\(N\\) theorem",
        "## 6. Plateau corollary, full-domain gate, and linear fallback",
        "## 7. Sharpness, boundary, and quantifier stress tests",
        "## 8. Route decision",
        "## 9. Decision and claim ledger",
        "## 10. Inherited source ledger",
    )
    for number, heading in enumerate(required_headings):
        checks.append(
            {"id": f"required_heading_{number:02d}", "sentinel": heading, "pass": compact(heading) in compact(body)}
        )

    compact_body = compact(body)
    for identifier, sentinel in STRUCTURAL_SENTINELS:
        checks.append(
            {"id": identifier, "sentinel": sentinel, "pass": compact(sentinel) in compact_body}
        )

    proved = section(body, "The following are **PROVED**:", "The following are **INHERITED**:")
    inherited = section(body, "The following are **INHERITED**:", "The following are **REFUTED OR RULED OUT**:")
    refuted = section(body, "The following are **REFUTED OR RULED OUT**:", "The following remain **OPEN**:")
    open_claims = section(body, "The following remain **OPEN**:", "The following are **NOT CLAIMED**:")
    not_claimed = section(body, "The following are **NOT CLAIMED**:", "## 10. Inherited source ledger")
    status_checks = (
        (
            "proved_ledger_keeps_S243_conditional",
            "*if* the explicitly open statement" in proved and "there exist fixed" not in proved,
        ),
        (
            "inherited_ledger_names_all_four_steps",
            all(token in inherited for token in ("R0.74P", "R0.74Q", "Step 7", "Step 8", "Step 9")),
        ),
        (
            "refuted_ledger_preserves_nonsharp_truth",
            "valid but nonsharp" in refuted and r"separate \(N\)-exception" in refuted,
        ),
        (
            "open_ledger_contains_residual_Q12_and_Q1",
            all(token in open_claims for token in ("(S.243)", "Q.12", "Q.1", "regularity")),
        ),
        (
            "not_claimed_ledger_preserves_domain_and_Clay_boundaries",
            all(token in not_claimed for token in ("infinite family", "redefined on", "same terminal supremum", "Millennium problem")),
        ),
    )
    for identifier, passed in status_checks:
        checks.append({"id": identifier, "pass": passed})

    source_ledger = section(body, "## 10. Inherited source ledger", "**NOT CLAY.**")
    for identifier, source in (
        ("source_R074P", "R0.74P, (2.7)--(3.7)"),
        ("source_R074Q", "R0.74Q, (Q.7)--(Q.12)"),
        ("source_R074R", "R0.74R, (R.209)--(R.214)"),
        ("source_Step7", "R0.74S Step 7, (S.142)--(S.155)"),
        ("source_Step8", "R0.74S Step 8, (S.163)--(S.199)"),
        ("source_Step9", "R0.74S Step 9, (S.200)--(S.222)"),
    ):
        checks.append({"id": identifier, "sentinel": source, "pass": source in source_ledger})
    return checks


def algebraic_negative_mutations() -> list[dict]:
    F = Fraction
    rows = []

    def add(identifier: str, true_value, mutated_value, classification: str = "false_formula"):
        rows.append(
            {
                "id": identifier,
                "kind": "algebraic",
                "classification": classification,
                "true_value": true_value,
                "mutated_value": mutated_value,
                "pass": true_value != mutated_value,
            }
        )

    oscillatory = ((F(0), F(0)), (F(1), F(10)), (F(2), F(7)), (F(3), F(8)), (F(4), F(12)))
    hits = level_intersections(oscillatory, F(8))
    add("mutation_last_exit_to_first_exit_rejected", fs(max(hits)), fs(min(hits)))

    boundary_base = dict(terminal=F(12), dissipation=F(6), beta=F(2), sigma=F(1), duration=F(1), q_increment=F(2))
    true_d = numeric_branch(**boundary_base)
    mutated_d = predicate_memberships(False, True, False, True, True)
    add("mutation_D_equality_to_nonD_rejected", list(true_d), [key for key, value in mutated_d.items() if value])

    true_beta = numeric_branch(**boundary_base)
    mutated_beta_membership = predicate_memberships(True, False, False, True, True)
    add("mutation_beta_equality_to_failure_rejected", list(true_beta), [key for key, value in mutated_beta_membership.items() if value])

    true_sigma = numeric_branch(terminal=F(12), dissipation=F(6), beta=F(1), sigma=F(1), duration=F(1, 2), q_increment=F(0))
    mutated_sigma_membership = predicate_memberships(True, False, True, False, False)
    add("mutation_sigma_equality_to_success_rejected", list(true_sigma), [key for key, value in mutated_sigma_membership.items() if value])

    true_long = numeric_branch(terminal=F(12), dissipation=F(5), beta=F(0), sigma=F(0), duration=F(1), q_increment=F(0))
    mutated_long_membership = predicate_memberships(False, False, False, False, False)
    add("mutation_long_equality_to_short_rejected", list(true_long), [key for key, value in mutated_long_membership.items() if value])

    true_q_positive = numeric_branch(terminal=F(12), dissipation=F(5), beta=F(2), sigma=F(0), duration=F(1, 2), q_increment=F(2))
    q_equality_failed = predicate_memberships(False, True, False, False, False)
    add("mutation_Q_equality_to_small_rejected", list(true_q_positive), [key for key, value in q_equality_failed.items() if value])

    true_q_negative = numeric_branch(terminal=F(12), dissipation=F(5), beta=F(2), sigma=F(0), duration=F(1, 2), q_increment=F(-2))
    drop_abs = predicate_memberships(False, True, False, False, False)
    add("mutation_drop_absolute_Q_rejected", list(true_q_negative), [key for key, value in drop_abs.items() if value])

    true_long_q = numeric_branch(terminal=F(12), dissipation=F(5), beta=F(2), sigma=F(0), duration=F(1), q_increment=F(2))
    add("mutation_Q_split_before_long_rejected", list(true_long_q), ["P_Q"])
    add("mutation_Q_split_before_D_rejected", list(true_beta), ["P_Q"])

    true_residual = F(1, 3) - F(1, 10)
    plus_q_residual = F(1, 3) + F(1, 10)
    add("mutation_DeltaF_minus_to_plus_DeltaQ_rejected", fs(true_residual), fs(plus_q_residual))

    epsilon = F(1, 6000)
    near_lower = F(1, 6) + epsilon
    rows.append(
        {
            "id": "mutation_residual_factor_six_to_five_rejected",
            "kind": "algebraic",
            "classification": "false_inequality",
            "true_bound": fs(6 * near_lower),
            "mutated_bound": fs(5 * near_lower),
            "terminal": fs(F(1)),
            "pass": F(1) < 6 * near_lower and not (F(1) < 5 * near_lower),
        }
    )
    near_upper = F(1, 2) - epsilon
    rows.append(
        {
            "id": "mutation_residual_half_to_two_fifths_rejected",
            "kind": "algebraic",
            "classification": "false_inequality",
            "true_bound": fs(F(1, 2)),
            "mutated_bound": fs(F(2, 5)),
            "residual": fs(near_upper),
            "pass": near_upper < F(1, 2) and not (near_upper <= F(2, 5)),
        }
    )

    shared = best_n_bruteforce((F(1), F(1)), 1)
    branchwise = best_n_bruteforce((F(1), F(0)), 1) + best_n_bruteforce((F(0), F(1)), 1)
    add("mutation_shared_N_to_two_branch_budgets_rejected", fs(shared), fs(branchwise), "wrong_quantifier")

    states = ((F(1), F(0)), (F(0), F(1)))
    sup_inf = max(best_n_bruteforce(state, 1) for state in states)
    inf_sup = min(
        max(sum((value for index, value in enumerate(state) if index not in set(removed)), F(0)) for state in states)
        for removed in powerset_indices(2, 1)
    )
    add("mutation_sup_inf_to_inf_sup_rejected", fs(sup_inf), fs(inf_sup), "wrong_quantifier")

    geometric = tuple(F(1, 2**index) for index in range(1, 9))
    add("mutation_fixed_N_to_truncation_N_rejected", fs(best_n_bruteforce(geometric, 1)), fs(best_n_bruteforce(geometric, 8)), "wrong_quantifier")

    add("mutation_full_beta_to_last_exit_beta_rejected", ["P_beta"], ["R_x"], "wrong_interval")
    add("mutation_full_sigma_to_last_exit_sigma_rejected", ["P_sigma"], ["R_x"], "wrong_interval")

    d_counterexample = d_persistence_counterexample()
    add(
        "mutation_terminal_D_to_last_exit_E_persistence_rejected",
        "E below T/6 on a positive-length subinterval",
        "E above T/6 a.e. on J_LE",
        "false_persistence",
    )
    rows[-1]["witness_early_excess"] = d_counterexample["early_excess"]
    rows[-1]["pass"] = d_counterexample["pass"]
    return rows


SOURCE_MUTATIONS = (
    (
        "mutation_source_last_exit_max_to_min_rejected",
        r":=\max\{t\in[s_R,\tau]:K_{k,R}(t)\le2T_k/3\}",
        r":=\min\{t\in[s_R,\tau]:K_{k,R}(t)\le2T_k/3\}",
        "canonical_last_exit_is_max",
        "false_definition",
    ),
    (
        "mutation_source_DeltaF_sign_rejected",
        r"\Delta F_k={T_k\over3}-\Delta Q_k",
        r"\Delta F_k={T_k\over3}+\Delta Q_k",
        "delta_F_has_minus_delta_Q",
        "false_formula",
    ),
    (
        "mutation_source_D_boundary_ge_to_gt_rejected",
        r"&:=\{k:D_{k,R}(\tau)\ge T_k/2\},",
        r"&:=\{k:D_{k,R}(\tau)>T_k/2\},",
        "D_boundary_formula",
        "strict_boundary_drift",
    ),
    (
        "mutation_source_beta_boundary_ge_to_gt_rejected",
        r"\beta_{k,R}(J_\tau)\ge T_k/6\},",
        r"\beta_{k,R}(J_\tau)>T_k/6\},",
        "beta_boundary_formula",
        "strict_boundary_drift",
    ),
    (
        "mutation_source_sigma_boundary_gt_to_ge_rejected",
        r"\sigma_{k,R}(J_\tau)>T_k/(12\lambda_k)\},",
        r"\sigma_{k,R}(J_\tau)\ge T_k/(12\lambda_k)\},",
        "sigma_strict_boundary_formula",
        "strict_boundary_drift",
    ),
    (
        "mutation_source_long_boundary_ge_to_gt_rejected",
        r"&:=\{k:d_k\ge\lambda_k^{-3/2}\},",
        r"&:=\{k:d_k>\lambda_k^{-3/2}\},",
        "long_boundary_formula",
        "strict_boundary_drift",
    ),
    (
        "mutation_source_short_boundary_lt_to_le_rejected",
        r"&:=\{k:d_k<\lambda_k^{-3/2}\},",
        r"&:=\{k:d_k\le\lambda_k^{-3/2}\},",
        "short_boundary_formula",
        "overlapping_boundary_drift",
    ),
    (
        "mutation_source_Q_boundary_ge_to_gt_rejected",
        r"&:=\{k:|\Delta Q_k|\ge T_k/6\},",
        r"&:=\{k:|\Delta Q_k|>T_k/6\},",
        "Q_large_boundary_formula",
        "strict_boundary_drift",
    ),
    (
        "mutation_source_Qsmall_boundary_lt_to_le_rejected",
        r"&:=\{k:|\Delta Q_k|<T_k/6\},",
        r"&:=\{k:|\Delta Q_k|\le T_k/6\},",
        "Q_small_boundary_formula",
        "overlapping_boundary_drift",
    ),
    (
        "mutation_source_full_history_to_LE_rejected",
        "using\n\\(J_\\tau=(s_R,\\tau)\\), not the last-exit interval",
        "using\n\\(J_k^{\\rm LE}=(\\ell_k,\\tau)\\), not the full-history interval",
        "full_history_not_last_exit",
        "wrong_interval",
    ),
    (
        "mutation_source_D_first_to_Q_first_rejected",
        "*D-first* priority rule",
        "*Q-first* priority rule",
        "D_first_priority",
        "overlapping_priority",
    ),
    (
        "mutation_source_absolute_Q_to_signed_positive_rejected",
        "means *absolute-\\(Q\\)-large*, not positive-sign \\(Q\\)",
        "means positive-sign \\(Q\\)-large and excludes negative increments",
        "absolute_Q_meaning",
        "false_sign_rule",
    ),
    (
        "mutation_source_a.e_to_every_time_rejected",
        "for almost every local-energy\ngood time \\(t\\in J_k^{\\rm LE}\\)",
        "for every time \\(t\\in J_k^{\\rm LE}\\)",
        "a.e_nonD_persistence",
        "false_good_time_extension",
    ),
    (
        "mutation_source_same_set_to_separate_sets_rejected",
        "apply (S.235) to those same sets",
        "optimize the two residual branches over separate sets",
        "same_set_before_infimum",
        "wrong_quantifier",
    ),
    (
        "mutation_source_nonnegative_bestN_to_signed_without_positive_part_rejected",
        "For a nonnegative \\(\\ell^1\\) vector \\(x\\), recall",
        "For an arbitrary signed \\(\\ell^1\\) vector \\(x\\), recall",
        "best_N_nonnegative_domain",
        "wrong_positive_part_domain",
    ),
    (
        "mutation_source_finite_Holder_limit_removed_rejected",
        "Use finite-shell Hölder first and then the inherited estimate (R.211)",
        "Apply infinite-shell Hölder and (R.211) directly without approximation",
        "finite_Holder_before_monotone_limit",
        "invalid_infinite_step",
    ),
    (
        "mutation_source_one_shared_N_to_two_N_rejected",
        "There is one exceptional set of size at most \\(N\\) for the *combined*\nresidual.",
        "There is a separate exceptional set of size \\(N\\) for each residual branch.",
        "one_shared_N",
        "wrong_quantifier",
    ),
    (
        "mutation_source_good_gate_to_all_terminals_rejected",
        r"\sup_{\tau\in\mathcal D\cap\mathcal G_R}",
        r"\sup_{\tau\in\mathcal D}",
        "good_terminal_residual_gate",
        "unsupported_closure",
    ),
    (
        "mutation_source_K_continuity_to_residual_continuity_rejected",
        "Only the inherited \\(\\ell^1\\)-continuity of the\nterminal \\(K\\)-vector is used",
        "Continuity of the residual vector and its masks is used",
        "K_only_domain_closure",
        "unsupported_regularity",
    ),
    (
        "mutation_source_fixed_profile_to_solution_dependent_rejected",
        "independently\nof \\(R\\), \\(\\tau\\), and the solution",
        "chosen separately for every \\(R\\), \\(\\tau\\), and solution",
        "fixed_profile_quantifiers",
        "wrong_quantifier",
    ),
    (
        "mutation_source_plateau_to_full_Q12_rejected",
        "a proof of the residual bound only on\n\\(I_R\\) yields (S.241), not full Q.12.",
        "a proof only on \\(I_R\\) yields full Q.12.",
        "plateau_does_not_give_Q12",
        "wrong_domain",
    ),
    (
        "mutation_source_OPEN_to_PROVED_rejected",
        r"\text{OPEN: there exist fixed }N_0<\infty, C_{\rm res}<\infty",
        r"\text{PROVED: there exist fixed }N_0<\infty, C_{\rm res}<\infty",
        "full_gate_explicitly_open",
        "claim_inflation",
    ),
    (
        "mutation_source_selector_continuity_claim_rejected",
        "continuity, measurability, or lower semicontinuity in \\(\\tau\\)",
        "continuity and lower semicontinuity in \\(\\tau\\)",
        "selector_regularities_not_claimed",
        "claim_inflation",
    ),
    (
        "mutation_source_remove_final_tag_rejected",
        r"\tag{S.247}",
        r"\tag{S.248}",
        "S223_S247_tags_consecutive",
        "source_integrity",
    ),
    (
        "mutation_source_6BQ_to_12BQ_statement_drift_rejected",
        "Thus the correct coefficient is one copy of \\(6B_Q\\), not \\(12B_Q\\).",
        "Thus the chosen bound uses two copies, \\(12B_Q\\).",
        "one_6BQ_statement",
        "statement_integrity_nonsharp_drift",
    ),
    (
        "mutation_source_C5_to_2C5_statement_drift_rejected",
        "estimating\nthem as two complete global ledgers would lose an unnecessary second copy\nof \\(C_5\\).",
        "estimating them separately requires two global ledgers and \\(2C_5\\).",
        "one_C5_statement",
        "statement_integrity_nonsharp_drift",
    ),
    (
        "mutation_source_nonsharp_double_charge_called_false_rejected",
        "those separate double charges are valid but nonsharp and are not used;",
        "those separate double charges are false inequalities;",
        "double_charge_truth_boundary",
        "claim_boundary_drift",
    ),
    (
        "mutation_source_D_persistence_warning_removed_rejected",
        "It would be invalid to apply the long non-\\(D\\) proof to\n\\(\\mathcal I_D\\).",
        "The long non-\\(D\\) persistence proof also applies to \\(\\mathcal I_D\\).",
        "D_persistence_invalid",
        "false_persistence",
    ),
    (
        "mutation_source_fixed_N_to_truncation_budget_rejected",
        "fixed \\(N\\) cannot be replaced by a truncation-dependent budget",
        "fixed \\(N\\) may be replaced by a truncation-dependent budget",
        "fixed_N_not_truncation_budget",
        "wrong_quantifier",
    ),
)


def structural_negative_mutations(body: str) -> list[dict]:
    baseline = structural_checks(body, enforce_lock=False)
    baseline_pass = all(row["pass"] for row in baseline)
    rows = []
    for identifier, correct, wrong, expected_failure, classification in SOURCE_MUTATIONS:
        occurrences = body.count(correct)
        mutated = body.replace(correct, wrong, 1)
        mutated_checks = structural_checks(mutated, enforce_lock=False)
        failed_ids = [row["id"] for row in mutated_checks if not row["pass"]]
        changed = mutated != body
        rows.append(
            {
                "id": identifier,
                "kind": "source_mutation",
                "classification": classification,
                "source_occurrences": occurrences,
                "changed": changed,
                "baseline_structural_pass": baseline_pass,
                "expected_failed_check": expected_failure,
                "mutated_structural_failures": failed_ids,
                "mutated_inequality_can_remain_true": classification == "statement_integrity_nonsharp_drift",
                "pass": occurrences == 1 and changed and baseline_pass and expected_failure in failed_ids,
            }
        )
    return rows


def negative_mutations(body: str) -> list[dict]:
    return algebraic_negative_mutations() + structural_negative_mutations(body)


def render_report(data: dict, json_hash: str) -> str:
    summary = data["summary"]
    result = "PASS" if data["pass"] else "FAIL"
    exact_rows = "\n".join(
        f"| {row['id']} | {row['left']} | {row['right']} | {row['margin']} |"
        for row in data["exact_checks"]
    )
    finite_rows = []
    for row in data["finite_checks"]:
        count = (
            row.get("configurations_checked")
            or row.get("predicate_configurations_checked")
            or row.get("pointwise_same_set_checks")
            or row.get("Q_paid_shell_count")
            or 1
        )
        finite_rows.append(
            f"| {row['id']} | {count} | {'PASS' if row['pass'] else 'FAIL'} |"
        )
    mutation_rows = "\n".join(
        f"| {row['id']} | {row['classification']} | {'rejected' if row['pass'] else 'NOT REJECTED'} |"
        for row in data["negative_mutations"]
    )
    truth = next(row for row in data["finite_checks"] if row["id"] == "D_first_full_truth_table_and_boundary_fixtures")
    paid = next(row for row in data["finite_checks"] if row["id"] == "paid_deletion_same_set_and_best_N_enumeration")
    holder = next(row for row in data["finite_checks"] if row["id"] == "combined_Psigma_PLE_one_cubic_Holder_ledger")
    return f"""# R0.74S paid-branch last-exit certificate report

## Result

**{result}** — {summary['exact_passed']}/{summary['exact_total']} exact rows,
{summary['finite_passed']}/{summary['finite_total']} finite groups,
{summary['structural_passed']}/{summary['structural_total']} source/claim checks,
and {summary['negative_mutations_passed']}/{summary['negative_mutations_total']}
negative mutations passed.

## Exact rational checks

| Check | Left | Right | Margin |
|---|---:|---:|---:|
{exact_rows}

## Finite groups

| Group | Primary count | Result |
|---|---:|---:|
{chr(10).join(finite_rows)}

The D-first Boolean truth table covers
{truth['predicate_configurations_checked']} predicate configurations and
{truth['boundary_fixture_count']} exact endpoint fixtures, with every one of
the six branches reached and exactly one branch selected for every positive
terminal row.  The paid-deletion enumeration checks
{paid['pointwise_same_set_checks']} same-set inequalities,
{paid['best_N_forward_checks']} forward best-N inequalities, and
{paid['best_N_reverse_checks']} reverse half-tail inequalities.  The combined
cubic ledger passes {holder['configurations_checked']} radical-free cubed
Holder checks, including a mixed P_sigma/P_LE equality row.

The remaining groups certify last-versus-first exit, both signed sharp
residual limits, one combined Q ledger, a shared exception budget, the
sup-inf order, finite-prefix fixtures illustrating fixed-N versus
growing-budget behavior, full-history versus last-exit classification, and
the rational terminal-D counterexample.

## Source and claim boundary

The producer locks the exact source bytes and consecutive unique tags
(S.223)--(S.247).  It checks the full-history Step 8 classes, D-first
priority, all strict/equality conventions, a.e. non-D persistence, the
single 6 B_Q and C5 ledgers, one shared N, good-terminal residual domain,
K-only terminal closure, plateau/full separation, and distinct PROVED,
INHERITED, REFUTED OR RULED OUT, OPEN, and NOT CLAIMED ledgers.

## Negative mutations

| Mutation | Classification | Result |
|---|---|---:|
{mutation_rows}

The `6B_Q -> 12B_Q` and `C5 -> 2C5` mutations are rejected as
statement-integrity drift.  Their looser inequalities may remain true; this
certificate does not mislabel them as algebraically false.

## Reproducibility

- Expected locked note SHA-256: `{data['source']['locked_note_sha256']}`
- Actual note SHA-256: `{data['source']['note_sha256']}`
- Generator SHA-256: `{data['source']['generator_sha256']}`
- JSON payload SHA-256: `{json_hash}`
- Schema: `{data['schema']}`
- No timestamp, random input, floating-point arithmetic, network input, or
  non-standard Python dependency is used.
- `R074S_PAID_BRANCH_NOTE`, `R074S_PAID_BRANCH_JSON`, and
  `R074S_PAID_BRANCH_REPORT` provide explicit deterministic path overrides.

## Boundary

This is a finite rational-algebra and statement-integrity certificate.  It
does not machine-prove the inherited local-energy theory, R.211/R.214, a
fixed solution- and scale-independent residual packing theorem, Q.12, Q.1,
regularity, or the Millennium problem.

**FINITE/ALGEBRAIC ONLY. INHERITED ANALYSIS NOT MACHINE-PROVED. NOT CLAY.**
"""


def main() -> None:
    note_bytes = NOTE.read_bytes()
    note_hash = sha256_bytes(note_bytes)
    body = note_bytes.decode("utf-8", errors="strict")
    exact_rows = exact_checks()
    finite_rows = finite_checks()
    structural_rows = structural_checks(body, source_bytes=note_bytes)
    mutation_rows = negative_mutations(body)

    summary = {
        "exact_total": len(exact_rows),
        "exact_passed": sum(bool(row["pass"]) for row in exact_rows),
        "finite_total": len(finite_rows),
        "finite_passed": sum(bool(row["pass"]) for row in finite_rows),
        "structural_total": len(structural_rows),
        "structural_passed": sum(bool(row["pass"]) for row in structural_rows),
        "negative_mutations_total": len(mutation_rows),
        "negative_mutations_passed": sum(bool(row["pass"]) for row in mutation_rows),
    }
    passed = all(
        (
            summary["exact_total"] == summary["exact_passed"],
            summary["finite_total"] == summary["finite_passed"],
            summary["structural_total"] == summary["structural_passed"],
            summary["negative_mutations_total"] == summary["negative_mutations_passed"],
            len({row["id"] for row in exact_rows}) == len(exact_rows),
            len({row["id"] for row in finite_rows}) == len(finite_rows),
            len({row["id"] for row in structural_rows}) == len(structural_rows),
            len({row["id"] for row in mutation_rows}) == len(mutation_rows),
            all(not row.get("failures") for row in finite_rows),
        )
    )

    data = {
        "schema": SCHEMA,
        "scope": {
            "finite_exact_fraction_and_statement_integrity_only": True,
            "machine_proves_inherited_good_time_theory": False,
            "machine_proves_R211_R214": False,
            "machine_proves_fixed_N_PDE_packing": False,
            "machine_proves_Q12_or_Q1": False,
            "machine_proves_regularity_or_Clay": False,
        },
        "source": {
            "note": display_path(NOTE),
            "note_sha256": note_hash,
            "locked_note_sha256": LOCKED_NOTE_SHA256,
            "generator": display_path(Path(__file__).resolve()),
            "generator_sha256": sha256(Path(__file__).resolve()),
        },
        "exact_checks": exact_rows,
        "finite_checks": finite_rows,
        "structural_checks": structural_rows,
        "negative_mutations": mutation_rows,
        "summary": summary,
        "pass": passed,
    }

    payload = (json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_bytes(payload)
    REPORT_OUT.write_text(render_report(data, sha256_bytes(payload)), encoding="utf-8")

    print(
        "R0.74S paid-branch last-exit certificate: "
        f"exact {summary['exact_passed']}/{summary['exact_total']}, "
        f"finite {summary['finite_passed']}/{summary['finite_total']}, "
        f"structural {summary['structural_passed']}/{summary['structural_total']}, "
        f"mutations {summary['negative_mutations_passed']}/{summary['negative_mutations_total']}"
    )
    print("PASS" if passed else "FAIL")
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
