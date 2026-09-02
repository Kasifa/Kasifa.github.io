#!/usr/bin/env python3
"""Deterministic finite certificate for R0.74S Step 11.

The producer checks exact finite best-N algebra, scalar inequalities,
rational clock fixtures, coefficient endpoint tests, statement integrity,
and frozen dependency hashes.  It does not machine-prove the inherited PDE
estimates, either open branch-packing theorem, Q.12, Q.1, regularity, or the
Navier--Stokes Millennium problem.
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
        "R074S_TRACE_NOTE",
        REPO / "research/r074s_shared_budget_terminal_trace_obstruction.md",
    )
)
JSON_OUT = Path(
    os.environ.get(
        "R074S_TRACE_JSON",
        REPO / "research/r074s_shared_budget_terminal_trace_certificate.json",
    )
)
REPORT_OUT = Path(
    os.environ.get(
        "R074S_TRACE_REPORT",
        REPO / "research/r074s_shared_budget_terminal_trace_certificate_report.md",
    )
)

LOCKED_NOTE_SHA256 = (
    "fd022de342b935e3e6e5fe0231f6b08ab9494e2bd38e23da15de6807f14d4693"
)
SCHEMA = "r074s-shared-budget-terminal-trace-certificate-v1"

DEPENDENCIES = {
    "R0.74P": (
        REPO / "research/r074p_temporal_observable_triage.md",
        "a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867",
    ),
    "R0.74Q": (
        REPO / "research/r074q_problem_freeze.md",
        "42efa94f5310d8f7ce3cea1896ee1e0a8ddd9bddf5d588f9bb853c8696a1a962",
    ),
    "R0.74R-step2": (
        REPO / "research/r074r_arbitrary_clock_extraction_gate.md",
        "ac959f30b254001910e5b445264ea7c0d8714afc2f96dcf74505f5e1f794b6b7",
    ),
    "R0.74R-persistent": (
        REPO / "research/r074r_persistent_lobe_cubic_packing.md",
        "e7f151048e85d95133f8c6414849c0fe9dc40cc48b7a12666b7e21496ddb99b5",
    ),
    "R0.74S-step8": (
        REPO / "research/r074s_defect_relaxed_total_rayleigh_excess.md",
        "0a79f2c5bb59644eca710b3d9341776853ceb4d1f65a36869c2465073f8c08ab",
    ),
    "R0.74S-step10": (
        REPO / "research/r074s_paid_branch_last_exit_residual.md",
        "9eb5f2a794021b49894adfc167d350f58d93c266e6be319ce835c58db2e0d74c",
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO.resolve()))
    except ValueError:
        return str(path.resolve())


def q(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def exact(identifier: str, left: Fraction, right: Fraction, note: str) -> dict:
    return {
        "id": identifier,
        "left": q(left),
        "right": q(right),
        "margin": q(left - right),
        "note": note,
        "pass": left == right,
    }


def assertion(identifier: str, passed: bool, note: str, **details) -> dict:
    row = {"id": identifier, "pass": bool(passed), "note": note}
    row.update(details)
    return row


def best_n(values: tuple[Fraction, ...], budget: int) -> Fraction:
    if budget < 0 or any(value < 0 for value in values):
        raise ValueError("best_n requires nonnegative values and budget")
    return sum(sorted(values, reverse=True)[budget:], Fraction(0))


def shared_budget_exhaustive() -> dict:
    values = (Fraction(0), Fraction(1), Fraction(2))
    cases = 0
    failures = []
    # State 0 is empty; 1,2 are branch a values; 3,4 are branch b values.
    for states in itertools.product(range(5), repeat=5):
        a = tuple(values[state] if state < 3 else Fraction(0) for state in states)
        b = tuple(
            values[state - 2] if state >= 3 else Fraction(0) for state in states
        )
        for budget in range(6):
            lhs = best_n(tuple(x + y for x, y in zip(a, b)), budget)
            rhs = min(
                best_n(a, split) + best_n(b, budget - split)
                for split in range(budget + 1)
            )
            cases += 1
            if lhs != rhs:
                failures.append(
                    {
                        "states": states,
                        "budget": budget,
                        "left": q(lhs),
                        "right": q(rhs),
                    }
                )
                if len(failures) >= 8:
                    break
        if failures:
            break
    return assertion(
        "shared_budget_infimal_convolution_exhaustive",
        not failures,
        "S.249 checked on every five-coordinate disjoint state over values 0,1,2.",
        cases=cases,
        failures=failures,
    )


def shared_budget_quantifier_fixtures() -> list[dict]:
    big = Fraction(17)
    a1, b1 = (big, Fraction(0)), (Fraction(0), Fraction(1))
    a2, b2 = (Fraction(1), Fraction(0)), (Fraction(0), big)
    adaptive = max(
        min(best_n(a, n) + best_n(b, 1 - n) for n in range(2))
        for a, b in ((a1, b1), (a2, b2))
    )
    fixed = min(
        max(
            best_n(a, n) + best_n(b, 1 - n)
            for a, b in ((a1, b1), (a2, b2))
        )
        for n in range(2)
    )
    return [
        exact(
            "duplicate_budget_joint_tail",
            best_n((big, big), 1),
            big,
            "S.252: one shared exception leaves one large coordinate.",
        ),
        exact(
            "duplicate_budget_two_exceptions",
            best_n((big, big), 2),
            Fraction(0),
            "Two exceptions, not one, delete both branches.",
        ),
        exact(
            "adaptive_terminal_split_value",
            adaptive,
            Fraction(1),
            "The pointwise adaptive branch split has worst value one.",
        ),
        exact(
            "fixed_terminal_split_value",
            fixed,
            big,
            "A split frozen across terminals has worst value M.",
        ),
    ]


def rx_grid_and_sharpness() -> dict:
    terminal = 60
    cases = 0
    failures = []
    for beta in range(10):
        for delta_q in range(-beta, beta + 1):
            for kinetic_charge in range(11):
                for dissipation in range(30, 61):
                    excess = dissipation - beta - kinetic_charge
                    if excess <= terminal // 6:
                        continue
                    residual = terminal // 3 - delta_q
                    cases += 1
                    if not (Fraction(excess, 5) < residual < 3 * excess):
                        failures.append(
                            {
                                "beta": beta,
                                "delta_q": delta_q,
                                "kinetic_charge": kinetic_charge,
                                "dissipation": dissipation,
                                "excess": excess,
                                "residual": residual,
                            }
                        )
                        if len(failures) >= 8:
                            break
                if failures:
                    break
            if failures:
                break
        if failures:
            break

    lower_terminal = Fraction(600)
    lower_beta = Fraction(99)
    lower_q = Fraction(99)
    lower_x = lower_terminal - lower_beta
    lower_r = lower_terminal / 3 - lower_q

    upper_beta = Fraction(99)
    upper_q = -Fraction(99)
    upper_x = Fraction(300) - upper_beta - Fraction(100)
    upper_r = lower_terminal / 3 - upper_q

    return assertion(
        "selected_excess_ratio_grid_and_sharpness",
        not failures
        and 5 * lower_r - lower_x == 4
        and 3 * upper_x - upper_r == 4,
        "S.262 checked on a finite feasible grid; scaled boundary fixtures leave margin four.",
        cases=cases,
        failures=failures,
        lower_margin=q(5 * lower_r - lower_x),
        upper_margin=q(3 * upper_x - upper_r),
    )


def dyadic_and_layer_cake_checks() -> list[dict]:
    heights = (Fraction(1, 2), Fraction(1, 4), Fraction(1, 8))
    weights = (Fraction(1, 3), Fraction(1, 5), Fraction(1, 7))
    moment = sum((w / (h * h) for w, h in zip(weights, heights)), Fraction(0))
    layer_sum = sum(
        (
            Fraction(4**j) * weights[j - 1]
            for j in range(1, len(weights) + 1)
        ),
        Fraction(0),
    )
    layer_cake = sum(
        (
            w * (1 + 2 * (Fraction(1, 2) * (h ** -2 - 1)))
            for w, h in zip(weights, heights)
        ),
        Fraction(0),
    )

    critical_ok = True
    count = 0
    finite_m = 12
    for n in range(1, finite_m + 1):
        tail = sum((Fraction(1, 4**j) for j in range(n, finite_m + 1)), Fraction(0))
        height_squared = Fraction(1, 4**n)
        critical_ok = critical_ok and tail <= Fraction(4, 3) * height_squared
        count += 1
    critical_moment = sum(
        (
            Fraction(1, 4**j) / Fraction(1, 2**j) ** 2
            for j in range(1, finite_m + 1)
        ),
        Fraction(0),
    )

    return [
        assertion(
            "dyadic_inverse_square_bounds",
            layer_sum <= moment <= 4 * layer_sum,
            "S.255 checked on three exact dyadic atoms.",
            moment=q(moment),
            lower=q(layer_sum),
            upper=q(4 * layer_sum),
        ),
        exact(
            "layer_cake_atomwise_identity",
            moment,
            layer_cake,
            "S.256 evaluated exactly atom by atom.",
        ),
        assertion(
            "critical_carleson_finite_log_growth",
            critical_ok and critical_moment == finite_m,
            "A critical quadratic tail coexists with an inverse moment equal to shell count.",
            thresholds=count,
            inverse_moment=q(critical_moment),
        ),
        assertion(
            "frozen_weight_eventual_ratio_elementary_bound",
            Fraction(97) > Fraction(16),
            "For k>=6 the exponent is at least 96; exp(96)>1+96>16 implies 8 exp(-96)<1/2.",
            exact_margin=q(Fraction(97) - Fraction(16)),
        ),
    ]


def weighted_holder_checks() -> dict:
    # Squares make every square root in the 3/2 Holder row rational.
    energies = (Fraction(1), Fraction(4), Fraction(9))
    weights = (Fraction(1), Fraction(4), Fraction(9))
    # Here e_j=x_j^2 and a_j=y_j^2.
    xs = (Fraction(1), Fraction(2), Fraction(3))
    ys = (Fraction(1), Fraction(2), Fraction(3))
    weighted_density = sum(
        (x**3 / y for x, y in zip(xs, ys)), Fraction(0)
    )
    lhs_cube = sum(energies, Fraction(0)) ** 3
    rhs_cube = sum(weights, Fraction(0)) * weighted_density**2
    return assertion(
        "weighted_holder_cube_form",
        lhs_cube <= rhs_cube,
        "Finite weighted Hölder row underlying S.258, checked without floating point.",
        left=q(lhs_cube),
        right=q(rhs_cube),
        equality=lhs_cube == rhs_cube,
    )


def rational_clock_checks() -> list[dict]:
    # Piecewise-linear h integral: average endpoint values times interval length.
    h0 = Fraction(0)
    h1 = Fraction(1, 15)
    h2 = Fraction(419, 6000)
    h3 = Fraction(2, 5)
    part1 = (h0 + h1) / 2 * Fraction(1, 10)
    part2 = (h1 + h2) / 2 * Fraction(19, 20)
    part3 = (h2 + h3) / 2 * Fraction(1, 20)
    sigma_defect = part1 + part2 + part3
    x_defect = Fraction(3, 5) - 2 * sigma_defect

    bump_integral = Fraction(12, 125) * Fraction(1, 2) ** 3 / 6
    g_integral = 300 * bump_integral
    sigma_high = sigma_defect + bump_integral
    x_high = Fraction(3, 5) - 2 * sigma_high

    return [
        exact(
            "common_h_integral",
            sigma_defect,
            Fraction(959, 12000),
            "Exact trapezoidal integral in S.266.",
        ),
        exact(
            "pure_defect_excess",
            x_defect,
            Fraction(2641, 6000),
            "Pure-defect selected excess.",
        ),
        exact(
            "high_rayleigh_bump_integral",
            bump_integral,
            Fraction(1, 500),
            "Quadratic bump integral.",
        ),
        exact(
            "high_rayleigh_g_integral",
            g_integral,
            Fraction(3, 5),
            "High-Rayleigh viscous ancestor mass.",
        ),
        exact(
            "high_rayleigh_sigma",
            sigma_high,
            Fraction(983, 12000),
            "Common h plus the early kinetic bump.",
        ),
        exact(
            "high_rayleigh_excess",
            x_high,
            Fraction(2617, 6000),
            "High-Rayleigh selected excess.",
        ),
        assertion(
            "both_clock_thresholds",
            sigma_defect < Fraction(1, 12)
            and sigma_high < Fraction(1, 12)
            and x_defect > Fraction(1, 6)
            and x_high > Fraction(1, 6),
            "Both rational rows lie in the intended selected-excess threshold class.",
        ),
    ]


def tower_and_falsification_checks() -> list[dict]:
    rows = []
    for m in (2, 5, 11, 23):
        for budget in range(m + 1):
            tail = best_n(tuple(Fraction(1, 3) for _ in range(m)), budget)
            rows.append(tail == Fraction(max(m - budget, 0), 3))

    paid_bound = Fraction(7)
    target = Fraction(100)
    targets = (target,) * 4
    eventually_residual = all(value > paid_bound for value in targets)
    residual_lower = tuple(value / 6 for value in targets)
    post_delete = best_n(residual_lower, 3)

    return [
        assertion(
            "flat_tower_best_N_formula",
            all(rows),
            "S.268 checked for four tower sizes and every admissible budget.",
            cases=len(rows),
        ),
        assertion(
            "N_plus_one_falsification_finite_fixture",
            eventually_residual and post_delete == target / 6,
            "Four targets above the total paid bound leave one residual after three deletions.",
            tail=q(post_delete),
        ),
        exact(
            "persistent_lobe_positive_exponent",
            Fraction(10, 3) * Fraction(8, 3969)
            - Fraction(2, 3) * Fraction(1, 320),
            Fraction(8831, 1905120),
            "Inherited R0.74R second-shell payment exponent.",
        ),
    ]


REQUIRED_SNIPPETS = {
    "shared_budget_exact": (
        "\\mathcal S_N(a+b)\n"
        " =\\min_{0\\le n\\le N}"
    ),
    "domain_sup_min_warning": "need not be an\nequality because a supremum",
    "honest_two_N": "best-\\(2N\\) combined estimate",
    "short_branch_domain": r"k\in\mathcal H_\tau:",
    "inverse_duration": r"a_kd_k^{-2}",
    "critical_carleson": "critical exponent two",
    "nested_tent": "nested-tent estimate",
    "terminal_trace": "has no terminal\ntrace",
    "anti_concentration_open": r"\tag{S.261}",
    "rx_constants": r"{1\over5}x_k^{\rm sel}<r_k^x<3x_k^{\rm sel}",
    "fixed_solution_nonuniform": r"N=N(u,R,\varepsilon)",
    "pure_defect_tower": "Repeating the pure-defect scalar row",
    "rx_gate_open": r"\tag{S.269}",
    "positive_denominator": r"\(A_R>0\)",
    "falsification_target": r"\tag{S.270}",
    "multipacket_cost": r"A_R^{(N)}:=(P_R^{M,(N)})^{2/3}",
    "bounded_search": "The search is evidence against an immediate literature shortcut",
    "combined_open": r"\tag{S.272}",
    "stress_not_nse": "ABSTRACT STRESS TESTS, NOT NSE COUNTEREXAMPLES",
    "not_clay": "**NOT CLAY.**",
}


def semantic_contract(text: str) -> list[dict]:
    rows = [
        assertion(
            identifier,
            snippet in text,
            f"Required source marker: {snippet}",
        )
        for identifier, snippet in REQUIRED_SNIPPETS.items()
    ]
    tags = [int(value) for value in re.findall(r"\\tag\{S\.(\d+)\}", text)]
    rows.extend(
        [
            assertion(
                "S248_S272_tags_consecutive",
                tags == list(range(248, 273)),
                "The twenty-five equation tags are consecutive and ordered.",
                tags=tags,
            ),
            assertion(
                "S248_S272_tags_unique",
                len(tags) == len(set(tags)) == 25,
                "Every Step 11 tag occurs exactly once.",
            ),
            assertion(
                "display_math_balanced",
                text.count(r"\[") == text.count(r"\]"),
                "Display-math delimiters balance.",
            ),
            assertion(
                "no_tabs_or_trailing_whitespace",
                "\t" not in text
                and not any(line.rstrip() != line for line in text.splitlines()),
                "Source has no tabs or trailing whitespace.",
            ),
            assertion(
                "no_forbidden_control_characters",
                not any(ord(ch) < 32 and ch not in "\n\r" for ch in text),
                "Source has no hidden control characters.",
            ),
            assertion(
                "three_open_gates_not_promoted",
                text.count(r"\textbf{OPEN") >= 3
                and "The antecedent remains open." in text,
                "S.261, S.269, and S.272 remain visibly open.",
            ),
            assertion(
                "literature_search_nonexhaustive",
                "not a\nproof that no related theorem exists" in text,
                "The bounded search is not presented as exhaustive.",
            ),
        ]
    )
    return rows


def negative_mutation_checks(text: str) -> list[dict]:
    mutations = {
        "reject_min_to_max": (
            r"=\min_{0\le n\le N}",
            r"=\max_{0\le n\le N}",
            "shared_budget_exact",
        ),
        "reject_rx_upper_constant_four": (
            r"<r_k^x<3x_k^{\rm sel}",
            r"<r_k^x<4x_k^{\rm sel}",
            "rx_constants",
        ),
        "reject_missing_short_domain": (
            r"k\in\mathcal H_\tau:",
            r"k:",
            "short_branch_domain",
        ),
        "reject_either_row_tower": (
            "Repeating the pure-defect scalar row",
            "Repeating either scalar row",
            "pure_defect_tower",
        ),
        "reject_zero_denominator_omission": (
            r"\(A_R>0\)",
            r"\(A_R\ge0\)",
            "positive_denominator",
        ),
        "reject_open_to_proved": (
            r"\textbf{OPEN",
            r"\textbf{PROVED",
            "three_open_gates_not_promoted",
        ),
        "reject_not_clay_removal": (
            "**NOT CLAY.**",
            "**CLAY.**",
            "not_clay",
        ),
    }
    rows = []
    for identifier, (old, new, expected_failure) in mutations.items():
        mutated = text.replace(old, new)
        checks = {row["id"]: row["pass"] for row in semantic_contract(mutated)}
        rows.append(
            assertion(
                identifier,
                mutated != text and not checks.get(expected_failure, True),
                f"Mutation must be rejected by {expected_failure}.",
            )
        )
    return rows


def structural_checks(text: str) -> list[dict]:
    rows = semantic_contract(text)
    rows.insert(
        0,
        assertion(
            "locked_note_sha256",
            sha256(NOTE) == LOCKED_NOTE_SHA256,
            "The analyzed note is byte-identical to the audited source.",
            actual=sha256(NOTE),
            expected=LOCKED_NOTE_SHA256,
        ),
    )
    for label, (path, expected) in DEPENDENCIES.items():
        actual = sha256(path)
        rows.append(
            assertion(
                f"dependency_{label}",
                actual == expected,
                "Frozen dependency hash.",
                path=str(path.relative_to(REPO)),
                actual=actual,
                expected=expected,
            )
        )
    return rows


def build_payload() -> dict:
    text = NOTE.read_text(encoding="utf-8")
    exact_checks = []
    exact_checks.extend(shared_budget_quantifier_fixtures())
    exact_checks.extend(rational_clock_checks())
    exact_checks.extend(tower_and_falsification_checks())
    finite_checks = [
        shared_budget_exhaustive(),
        rx_grid_and_sharpness(),
        *dyadic_and_layer_cake_checks(),
        weighted_holder_checks(),
    ]
    structural = structural_checks(text)
    negative = negative_mutation_checks(text)
    all_rows = exact_checks + finite_checks + structural + negative
    return {
        "schema": SCHEMA,
        "source": {
            "path": display_path(NOTE),
            "sha256": sha256(NOTE),
            "locked_sha256": LOCKED_NOTE_SHA256,
        },
        "scope": {
            "finite_exact_fraction_and_statement_integrity_only": True,
            "machine_proves_inherited_PDE_estimates": False,
            "machine_proves_terminal_anti_concentration": False,
            "machine_proves_selected_excess_packing": False,
            "machine_proves_S243_Q12_or_Q1": False,
            "machine_proves_regularity_or_Clay": False,
        },
        "exact_checks": exact_checks,
        "finite_checks": finite_checks,
        "structural_checks": structural,
        "negative_mutation_checks": negative,
        "summary": {
            "exact_passed": sum(row["pass"] for row in exact_checks),
            "exact_total": len(exact_checks),
            "finite_passed": sum(row["pass"] for row in finite_checks),
            "finite_total": len(finite_checks),
            "structural_passed": sum(row["pass"] for row in structural),
            "structural_total": len(structural),
            "negative_passed": sum(row["pass"] for row in negative),
            "negative_total": len(negative),
            "all_pass": all(row["pass"] for row in all_rows),
        },
    }


def render_report(payload: dict) -> str:
    summary = payload["summary"]
    lines = [
        "# R0.74S Step 11 — deterministic certificate report",
        "",
        f"- Schema: {payload['schema']}",
        f"- Source: {payload['source']['path']}",
        f"- Source SHA-256: {payload['source']['sha256']}",
        f"- Exact checks: {summary['exact_passed']}/{summary['exact_total']}",
        f"- Finite checks: {summary['finite_passed']}/{summary['finite_total']}",
        f"- Structural checks: {summary['structural_passed']}/{summary['structural_total']}",
        f"- Negative mutations rejected: {summary['negative_passed']}/{summary['negative_total']}",
        f"- Overall: {'PASS' if summary['all_pass'] else 'FAIL'}",
        "",
        "## Scope",
        "",
        "This certificate checks finite exact algebra, rational fixtures, source",
        "integrity, and claim boundaries.  It does not machine-prove the inherited",
        "PDE estimates, either open branch-packing theorem, Q.12, Q.1, regularity,",
        "or the Navier--Stokes Millennium problem.  **NOT CLAY.**",
        "",
        "## Check groups",
        "",
    ]
    for group in (
        "exact_checks",
        "finite_checks",
        "structural_checks",
        "negative_mutation_checks",
    ):
        lines.extend([f"### {group.replace('_', ' ').title()}", ""])
        for row in payload[group]:
            state = "PASS" if row["pass"] else "FAIL"
            lines.append(f"- **{state}** — {row['id']}: {row['note']}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    payload = build_payload()
    JSON_OUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    REPORT_OUT.write_text(render_report(payload), encoding="utf-8")
    print(json.dumps(payload["summary"], sort_keys=True))
    return 0 if payload["summary"]["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
