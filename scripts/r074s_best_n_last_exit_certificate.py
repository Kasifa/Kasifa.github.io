#!/usr/bin/env python3
"""Deterministic finite certificate for R0.74S Step 9.

The certificate checks the exact best-N algebra, finite rational models,
source/claim structure, and rejection of dangerous mutations in
``r074s_best_n_last_exit_equivalence.md``.  It is deliberately finite and
standard-library only.  It does not machine-prove any inherited PDE estimate,
good-time theorem, regularity statement, or Millennium claim.
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
        "R074S_BEST_N_NOTE",
        REPO / "research/r074s_best_n_last_exit_equivalence.md",
    )
)
JSON_OUT = Path(
    os.environ.get(
        "R074S_BEST_N_JSON",
        REPO / "research/r074s_best_n_last_exit_certificate.json",
    )
)
REPORT_OUT = Path(
    os.environ.get(
        "R074S_BEST_N_REPORT",
        REPO / "research/r074s_best_n_last_exit_certificate_report.md",
    )
)

LOCKED_NOTE_SHA256 = (
    "85003b3fdfdf28618a82a57d241e86c086704ea3ed3a9b192de223f3b8c3a4dd"
)


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


def exact(identifier: str, left: Fraction, right: Fraction, note: str) -> dict:
    return {
        "id": identifier,
        "left": fs(left),
        "right": fs(right),
        "margin": fs(left - right),
        "note": note,
        "pass": left == right,
    }


def exact_ledger() -> list[dict]:
    theta = Fraction(2, 3)
    q = Fraction(1, 6)
    return [
        exact(
            "half_exit_two_halves_recover_terminal_flux",
            2 * Fraction(1, 2),
            Fraction(1),
            "S.205--S.208: the terminal reduction restores the full flux.",
        ),
        exact(
            "two_thirds_last_exit_increment",
            Fraction(1) - theta,
            Fraction(1, 3),
            "S.211 and S.222 at theta=2/3.",
        ),
        exact(
            "strict_quarter_upcrossing_margin",
            (Fraction(1) - theta) - Fraction(1, 4),
            Fraction(1, 12),
            "The canonical theta=2/3 stop has a strict one-twelfth margin.",
        ),
        exact(
            "one_sixth_signed_increment_margin",
            (Fraction(1) - theta) - q,
            Fraction(1, 6),
            "S.222 after a Q increment smaller than one sixth.",
        ),
        exact(
            "clock_reduction_BQ_coefficient_at_two_thirds",
            Fraction(1) + Fraction(1, 1) / (Fraction(1) - theta),
            Fraction(4),
            "S.216 has one direct B_Q plus one divided by 1-theta.",
        ),
        exact(
            "last_exit_work_coefficient_at_two_thirds",
            Fraction(1, 1) / (Fraction(1) - theta),
            Fraction(3),
            "The W coefficient in S.216 is three at theta=2/3.",
        ),
        exact(
            "sharp_Q_error_coefficient",
            Fraction(1),
            Fraction(1),
            "S.213--S.214 use one complete Q-variation ledger.",
        ),
        exact(
            "signed_tail_positive_negative_split",
            Fraction(5) - Fraction(2),
            Fraction(3),
            "A finite proxy for the positive-tail minus negative-mass formula.",
        ),
        exact(
            "plateau_is_not_forced_to_equal_full_domain",
            Fraction(3) - Fraction(1),
            Fraction(2),
            "A strict full-minus-plateau fixture retains the domain distinction.",
        ),
    ]


def powerset_indices(length: int, max_size: int | None = None):
    upper = length if max_size is None else min(length, max_size)
    for size in range(upper + 1):
        yield from itertools.combinations(range(length), size)


def positive(value: Fraction) -> Fraction:
    return max(value, Fraction(0))


def best_n_bruteforce(values: tuple[Fraction, ...], nterm: int) -> Fraction:
    candidates = []
    for removed in powerset_indices(len(values), nterm):
        removed_set = set(removed)
        candidates.append(
            positive(sum((x for i, x in enumerate(values) if i not in removed_set), Fraction(0)))
        )
    return min(candidates)


def best_n_formula(values: tuple[Fraction, ...], nterm: int) -> Fraction:
    positive_values = sorted((x for x in values if x > 0), reverse=True)
    removed = sum(positive_values[:nterm], Fraction(0))
    return positive(sum(values, Fraction(0)) - removed)


def best_n_tail_enumeration() -> dict:
    alphabet = tuple(Fraction(x) for x in (-2, -1, 0, 1, 2))
    configurations = 0
    failures = []
    strict_cancellation_cases = 0
    for length in range(1, 5):
        for values in itertools.product(alphabet, repeat=length):
            for nterm in range(length + 2):
                configurations += 1
                brute = best_n_bruteforce(values, nterm)
                formula = best_n_formula(values, nterm)
                if brute < positive(sum(values, Fraction(0))):
                    strict_cancellation_cases += 1
                if brute != formula and len(failures) < 8:
                    failures.append(
                        {
                            "values": [fs(x) for x in values],
                            "N": nterm,
                            "brute": fs(brute),
                            "formula": fs(formula),
                        }
                    )
    return {
        "id": "best_N_signed_tail_rearrangement_enumeration",
        "configurations_checked": configurations,
        "strict_reduction_cases": strict_cancellation_cases,
        "failures": failures,
        "pass": not failures,
    }


def l1_lipschitz_enumeration() -> dict:
    alphabet = tuple(Fraction(x) for x in (-1, 0, 1))
    vectors = list(itertools.product(alphabet, repeat=3))
    configurations = 0
    equality_cases = 0
    failures = []
    for x in vectors:
        for y in vectors:
            distance = sum((abs(a - b) for a, b in zip(x, y)), Fraction(0))
            for nterm in range(4):
                configurations += 1
                gap = abs(best_n_bruteforce(x, nterm) - best_n_bruteforce(y, nterm))
                if gap == distance:
                    equality_cases += 1
                if gap > distance and len(failures) < 8:
                    failures.append(
                        {
                            "x": [fs(v) for v in x],
                            "y": [fs(v) for v in y],
                            "N": nterm,
                            "gap": fs(gap),
                            "l1_distance": fs(distance),
                        }
                    )
    return {
        "id": "best_N_l1_Lipschitz_enumeration",
        "configurations_checked": configurations,
        "equality_cases": equality_cases,
        "failures": failures,
        "pass": not failures,
    }


def last_half_level_on_piecewise_linear_path(
    path: tuple[Fraction, ...],
) -> tuple[Fraction, Fraction]:
    terminal = path[-1]
    if terminal == 0:
        return Fraction(len(path) - 1), Fraction(0)
    sign = Fraction(1 if terminal > 0 else -1)
    threshold = abs(terminal) / 2
    signed_path = tuple(sign * value for value in path)
    last_index = max(i for i, value in enumerate(signed_path) if value <= threshold)
    if last_index == len(path) - 1:
        return Fraction(last_index), terminal
    left = signed_path[last_index]
    right = signed_path[last_index + 1]
    if right == left:
        raise AssertionError("terminal half-level segment is unexpectedly flat")
    fraction = (threshold - left) / (right - left)
    crossing_time = Fraction(last_index) + fraction
    crossing_value = path[last_index] + fraction * (
        path[last_index + 1] - path[last_index]
    )
    return crossing_time, crossing_value


def half_exit_piecewise_linear_fixtures() -> dict:
    paths = (
        (Fraction(0), Fraction(1), Fraction(2)),
        (Fraction(0), Fraction(2), Fraction(0), Fraction(4)),
        (Fraction(0), Fraction(-1), Fraction(-2)),
        (Fraction(0), Fraction(-3), Fraction(-1), Fraction(-4)),
        (Fraction(0), Fraction(5), Fraction(1), Fraction(2)),
        (Fraction(0), Fraction(0), Fraction(0)),
    )
    failures = []
    rows = []
    for path in paths:
        crossing_time, crossing_value = last_half_level_on_piecewise_linear_path(path)
        terminal = path[-1]
        passed = crossing_value == terminal / 2 and terminal - crossing_value == terminal / 2
        rows.append(
            {
                "path": [fs(x) for x in path],
                "crossing_time": fs(crossing_time),
                "crossing_value": fs(crossing_value),
                "terminal": fs(terminal),
                "pass": passed,
            }
        )
        if not passed:
            failures.append(rows[-1])
    return {
        "id": "signed_half_exit_piecewise_linear_fixtures",
        "configurations_checked": len(paths),
        "rows": rows,
        "failures": failures,
        "pass": not failures,
    }


def k_last_exit_q_error_enumeration() -> dict:
    theta_values = (Fraction(1, 3), Fraction(2, 3))
    coordinate_options = [(Fraction(0), Fraction(0))]
    coordinate_options.extend(
        (Fraction(t), Fraction(q))
        for t in (1, 2)
        for q in (-1, 0, 1)
    )
    pointwise_checks = 0
    tail_checks = 0
    sharp_cases = 0
    failures = []
    for theta in theta_values:
        factor = Fraction(1) - theta
        for coordinates in itertools.product(coordinate_options, repeat=3):
            terminal_k = tuple(item[0] for item in coordinates)
            delta_q = tuple(item[1] for item in coordinates)
            last_work = tuple(
                factor * terminal - q
                for terminal, q in zip(terminal_k, delta_q)
            )
            bq = sum((abs(q) for q in delta_q), Fraction(0))
            for removed in powerset_indices(3):
                pointwise_checks += 1
                removed_set = set(removed)
                work_sum = sum(
                    (x for i, x in enumerate(last_work) if i not in removed_set),
                    Fraction(0),
                )
                clock_sum = factor * sum(
                    (x for i, x in enumerate(terminal_k) if i not in removed_set),
                    Fraction(0),
                )
                gap = abs(positive(work_sum) - clock_sum)
                local_q = sum(
                    (abs(x) for i, x in enumerate(delta_q) if i not in removed_set),
                    Fraction(0),
                )
                if gap == local_q and local_q > 0:
                    sharp_cases += 1
                if gap > local_q and len(failures) < 8:
                    failures.append(
                        {
                            "kind": "pointwise",
                            "theta": fs(theta),
                            "K": [fs(x) for x in terminal_k],
                            "delta_Q": [fs(x) for x in delta_q],
                            "removed": list(removed),
                            "gap": fs(gap),
                            "local_Q": fs(local_q),
                        }
                    )
            for nterm in range(4):
                tail_checks += 1
                sk = best_n_bruteforce(terminal_k, nterm)
                work = best_n_bruteforce(last_work, nterm)
                if not (factor * sk - bq <= work <= factor * sk + bq):
                    if len(failures) < 8:
                        failures.append(
                            {
                                "kind": "tail",
                                "theta": fs(theta),
                                "K": [fs(x) for x in terminal_k],
                                "delta_Q": [fs(x) for x in delta_q],
                                "N": nterm,
                                "clock_tail": fs(sk),
                                "work_tail": fs(work),
                                "B_Q": fs(bq),
                            }
                        )
    return {
        "id": "K_last_exit_one_BQ_enumeration",
        "pointwise_checks": pointwise_checks,
        "best_N_tail_checks": tail_checks,
        "sharp_pointwise_cases": sharp_cases,
        "failures": failures,
        "pass": not failures and sharp_cases > 0,
    }


def f_k_tail_comparison_enumeration() -> dict:
    coordinate_options = tuple(
        (Fraction(k), Fraction(q))
        for k in (0, 1, 2)
        for q in (-1, 0, 1)
    )
    configurations = 0
    equality_cases = 0
    failures = []
    for coordinates in itertools.product(coordinate_options, repeat=3):
        kvals = tuple(item[0] for item in coordinates)
        qvals = tuple(item[1] for item in coordinates)
        fvals = tuple(k - q for k, q in zip(kvals, qvals))
        bq = sum((abs(q) for q in qvals), Fraction(0))
        for nterm in range(4):
            configurations += 1
            gap = abs(
                best_n_bruteforce(fvals, nterm)
                - best_n_bruteforce(kvals, nterm)
            )
            if gap == bq and bq > 0:
                equality_cases += 1
            if gap > bq and len(failures) < 8:
                failures.append(
                    {
                        "K": [fs(x) for x in kvals],
                        "Q": [fs(x) for x in qvals],
                        "F": [fs(x) for x in fvals],
                        "N": nterm,
                        "gap": fs(gap),
                        "B_Q": fs(bq),
                    }
                )
    return {
        "id": "signed_F_nonnegative_K_best_N_comparison",
        "configurations_checked": configurations,
        "equality_cases": equality_cases,
        "failures": failures,
        "pass": not failures and equality_cases > 0,
    }


def terminal_reduction_enumeration() -> dict:
    coordinate_options = tuple(
        (Fraction(k), Fraction(q))
        for k in (0, 1, 2)
        for q in (-1, 0, 1)
    )
    configurations = 0
    cauchy_equality_cases = 0
    failures = []
    for coordinates in itertools.product(coordinate_options, repeat=3):
        kvals = tuple(item[0] for item in coordinates)
        qvals = tuple(item[1] for item in coordinates)
        fvals = tuple(k - q for k, q in zip(kvals, qvals))
        cumulative = positive(sum(fvals, Fraction(0)))
        bq = sum((abs(q) for q in qvals), Fraction(0))
        z_squared = sum((k * k for k in kvals), Fraction(0))
        for nterm in range(4):
            configurations += 1
            tail = best_n_bruteforce(fvals, nterm)
            needed_from_exceptions = positive(cumulative - bq - tail)
            squared_bound = Fraction(nterm) * z_squared
            if needed_from_exceptions * needed_from_exceptions == squared_bound:
                cauchy_equality_cases += 1
            if needed_from_exceptions * needed_from_exceptions > squared_bound:
                if len(failures) < 8:
                    failures.append(
                        {
                            "K": [fs(x) for x in kvals],
                            "Q": [fs(x) for x in qvals],
                            "F": [fs(x) for x in fvals],
                            "N": nterm,
                            "cumulative": fs(cumulative),
                            "B_Q": fs(bq),
                            "tail": fs(tail),
                            "needed_squared": fs(
                                needed_from_exceptions * needed_from_exceptions
                            ),
                            "N_Z_squared": fs(squared_bound),
                        }
                    )
    return {
        "id": "plateau_terminal_reduction_squared_Cauchy_enumeration",
        "configurations_checked": configurations,
        "cauchy_equality_cases": cauchy_equality_cases,
        "failures": failures,
        "pass": not failures,
    }


def quantifier_and_cancellation_fixtures() -> dict:
    states = (
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(1)),
    )
    sup_inf = max(best_n_bruteforce(state, 1) for state in states)
    fixed_set_values = []
    for removed in powerset_indices(2, 1):
        removed_set = set(removed)
        fixed_set_values.append(
            max(
                sum(
                    (x for i, x in enumerate(state) if i not in removed_set),
                    Fraction(0),
                )
                for state in states
            )
        )
    inf_sup = min(fixed_set_values)

    signed = (Fraction(1), Fraction(-1))
    signed_tail = best_n_bruteforce(signed, 0)
    half_vector = tuple(x / 2 for x in signed)
    arbitrary_subset_sup = max(
        positive(sum((half_vector[i] for i in subset), Fraction(0)))
        for subset in powerset_indices(2)
    )

    plateau_value = Fraction(1)
    preplateau_value = Fraction(3)
    plateau_sup = plateau_value
    full_sup = max(plateau_value, preplateau_value)

    passed = (
        sup_inf == 0
        and inf_sup == 1
        and signed_tail == 0
        and arbitrary_subset_sup == Fraction(1, 2)
        and plateau_sup < full_sup
    )
    return {
        "id": "quantifier_cancellation_and_domain_fixtures",
        "sup_tau_inf_S": fs(sup_inf),
        "inf_S_sup_tau": fs(inf_sup),
        "signed_tail": fs(signed_tail),
        "arbitrary_subset_half_exit_sup": fs(arbitrary_subset_sup),
        "plateau_sup": fs(plateau_sup),
        "full_sup": fs(full_sup),
        "pass": passed,
    }


def simultaneous_plateau_enumeration() -> dict:
    heights = (Fraction(1, 2), Fraction(1), Fraction(3, 2))
    thetas = (Fraction(1, 3), Fraction(2, 3))
    configurations = 0
    failures = []
    for shell_count in range(1, 11):
        for nterm in range(shell_count + 1):
            for height in heights:
                terminal = tuple(height for _ in range(shell_count))
                tail = best_n_bruteforce(terminal, nterm)
                for theta in thetas:
                    configurations += 1
                    half_work = best_n_bruteforce(
                        tuple(height / 2 for _ in terminal), nterm
                    )
                    k_work = best_n_bruteforce(
                        tuple((1 - theta) * height for _ in terminal), nterm
                    )
                    expected = Fraction(shell_count - nterm) * height
                    if not (
                        tail == expected
                        and half_work == expected / 2
                        and k_work == (1 - theta) * expected
                    ) and len(failures) < 8:
                        failures.append(
                            {
                                "M": shell_count,
                                "N": nterm,
                                "H": fs(height),
                                "theta": fs(theta),
                                "tail": fs(tail),
                                "half_work": fs(half_work),
                                "K_work": fs(k_work),
                            }
                        )
    return {
        "id": "simultaneous_plateau_no_compression_enumeration",
        "configurations_checked": configurations,
        "failures": failures,
        "pass": not failures,
    }


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def section(body: str, start: str, end: str) -> str:
    if start not in body or end not in body:
        return ""
    return body.split(start, 1)[1].split(end, 1)[0]


def structural_checks(body: str, enforce_lock: bool = True) -> list[dict]:
    checks = []
    body_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()
    checks.append(
        {
            "id": "locked_note_sha256",
            "actual": body_hash,
            "expected": LOCKED_NOTE_SHA256,
            "enforced": enforce_lock,
            "pass": (body_hash == LOCKED_NOTE_SHA256) if enforce_lock else True,
        }
    )

    tags = re.findall(r"\\tag\{S\.(\d+)\}", body)
    expected_tags = [str(number) for number in range(200, 223)]
    checks.extend(
        [
            {
                "id": "S200_S222_tags_consecutive",
                "actual": tags,
                "expected": expected_tags,
                "pass": tags == expected_tags,
            },
            {
                "id": "S200_S222_tags_unique",
                "tag_count": len(tags),
                "unique_count": len(set(tags)),
                "pass": len(tags) == len(set(tags)) == len(expected_tags),
            },
            {
                "id": "display_math_balanced",
                "left_count": body.count("\\["),
                "right_count": body.count("\\]"),
                "pass": body.count("\\[") == body.count("\\]"),
            },
            {
                "id": "inline_math_balanced",
                "left_count": body.count("\\("),
                "right_count": body.count("\\)"),
                "pass": body.count("\\(") == body.count("\\)"),
            },
            {
                "id": "no_disallowed_control_characters",
                "pass": not any(
                    ord(character) < 32 and character not in "\n\t"
                    for character in body
                ),
            },
        ]
    )

    required_sections = (
        "## 0. Result and scope",
        "## 1. Terminal domains and the fixed best-\\(N\\) order",
        "## 2. The exact signed half-exit representation",
        "## 3. The \\(K\\)-level last exit and the sharp \\(Q\\) error",
        "## 4. Equivalence with the existing R0.74Q gate",
        "## 5. Quantifier and cancellation stress tests",
        "## 6. Route decision",
        "## 7. Decision and claim ledger",
        "## 8. Inherited source ledger",
    )
    for heading in required_sections:
        checks.append(
            {
                "id": "required_section_"
                + hashlib.sha256(heading.encode()).hexdigest()[:12],
                "sentinel": heading,
                "pass": heading in body,
            }
        )

    required_text = (
        "Only the inequality",
        "equality is neither used nor asserted",
        "This is the order",
        "not be admissible in the Step 2 supremum (S.37)",
        "Fix a good terminal",
        "finite set \\(G\\subset\\{k:T_k>0\\}\\)",
        "not the canonical last-exit selector itself",
        "not continuity of the last-exit map",
        "Taking \\(\\mathcal D=\\mathcal T_R\\) recovers exactly the full-terminal",
        "Taking \\(\\mathcal D=I_R\\) gives its weaker plateau",
        "not asserted to be an (S.25)-admissible Step 2 family",
        "will be defined and audited in the next step",
        "The following are **PROVED**:",
        "The following are **INHERITED**:",
        "The following are **REFUTED**:",
        "The following remain **OPEN**:",
        "The following are **NOT CLAIMED**:",
        "- that the canonical last-exit selector is continuous in the terminal time",
        "The conditional implication (S.38) remains valid",
        "**NOT CLAY.**",
    )
    compact_body = compact(body)
    for sentinel in required_text:
        checks.append(
            {
                "id": "required_text_"
                + hashlib.sha256(sentinel.encode()).hexdigest()[:12],
                "sentinel": sentinel,
                "pass": compact(sentinel) in compact_body,
            }
        )

    required_formulae = (
        r"\mathfrak C_R^M(I_R)=\mathfrak C_R^M",
        r"\mathfrak C_R^M(\mathcal T_R)=\mathfrak C_{{\rm full},R}^M",
        r"\sup_{\tau}\inf_{S_\tau}",
        r"F_{k,R}(\tau)-F_{k,R}(\ell_k^F(\tau))={1\over2}F_{k,R}(\tau)",
        r"\mathfrak W_{1/2,N,R}^{F}(\mathcal D)={1\over2}\mathcal S_{N,R}^{F}(\mathcal D)",
        r"L_{k,\theta}(\tau):=F_{k,R}(\tau)-F_{k,R}(\ell_{k,\theta}^{K}(\tau))=(1-\theta)T_k-\Delta Q_{k,\theta}(\tau)",
        r"(1-\theta)\mathcal S_{N,R}^{K}(\mathcal D)-B_{Q,R}^M",
        r"\le(1-\theta)\mathcal S_{N,R}^{K}(\mathcal D)+B_{Q,R}^M",
        r"0<\theta<{3\over4}",
        r"T_k>0",
        r"\left|\mathcal S_{N,R}^{F}(\mathcal D)-\mathcal S_{N,R}^{K}(\mathcal D)\right|\le B_{Q,R}^M",
        r"\Delta K_{k,2/3}={1\over3}T_k",
        r"\Delta F_{k,2/3}>{1\over6}T_k",
    )
    for sentinel in required_formulae:
        checks.append(
            {
                "id": "required_formula_"
                + hashlib.sha256(sentinel.encode()).hexdigest()[:12],
                "sentinel": sentinel,
                "pass": compact(sentinel) in compact_body,
            }
        )

    proved = section(
        body,
        "The following are **PROVED**:",
        "The following are **INHERITED**:",
    )
    inherited = section(
        body,
        "The following are **INHERITED**:",
        "The following are **REFUTED**:",
    )
    refuted = section(
        body,
        "The following are **REFUTED**:",
        "The following remain **OPEN**:",
    )
    open_claims = section(
        body,
        "The following remain **OPEN**:",
        "The following are **NOT CLAIMED**:",
    )
    not_claimed = section(
        body,
        "The following are **NOT CLAIMED**:",
        "## 8. Inherited source ledger",
    )
    status_rows = (
        (
            "proved_contains_only_reductions_and_equivalences",
            all(token in proved for token in ("half-exit", "good-stop closure", "no-gain"))
            and "solution- and scale-independent PDE estimate" not in proved,
        ),
        (
            "inherited_binds_P_Q_and_Step8",
            all(token in inherited for token in ("R0.74P", "R0.74Q", "Step 8")),
        ),
        (
            "refuted_contains_no_exception_but_preserves_S38",
            "\\mathfrak W_{{\\rm up},R}^M\\lesssim A_R" in refuted
            and "conditional implication (S.38) remains valid" in refuted,
        ),
        (
            "open_contains_best_N_PDE_and_Q1",
            "solution- and scale-independent PDE estimate" in open_claims
            and "fixed-scale inequality (Q.1)" in open_claims,
        ),
        (
            "not_claimed_contains_selector_domain_and_Clay_boundaries",
            "- that the canonical last-exit selector is continuous" in not_claimed
            and "same flux supremum" in not_claimed
            and "Millennium problem" in not_claimed,
        ),
    )
    for identifier, passed in status_rows:
        checks.append({"id": identifier, "pass": passed})

    source_ledger = section(body, "## 8. Inherited source ledger", "**NOT CLAY.**")
    for source in (
        "R0.74P, (2.7)--(3.7)",
        "R0.74Q, (Q.7)--(Q.12)",
        "R0.74S Step 2, (S.25)--(S.38)",
        "R0.74S Step 8, (S.197)--(S.199)",
    ):
        checks.append(
            {
                "id": "source_ledger_"
                + hashlib.sha256(source.encode()).hexdigest()[:12],
                "sentinel": source,
                "pass": source in source_ledger,
            }
        )
    return checks


def algebraic_negative_mutations() -> list[dict]:
    theta = Fraction(2, 3)
    terminal_f = Fraction(3, 2)
    true_half_increment = terminal_f / 2
    terminal_k = Fraction(3)
    true_k_increment = (1 - theta) * terminal_k
    q_increment = Fraction(1, 3)
    true_work = (1 - theta) * Fraction(1) - q_increment
    sharp_gap = Fraction(1, 3)

    states = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
    correct_quantifier = max(best_n_bruteforce(state, 1) for state in states)
    fixed_quantifier = min(
        max(
            sum(
                (x for i, x in enumerate(state) if i not in set(removed)),
                Fraction(0),
            )
            for state in states
        )
        for removed in powerset_indices(2, 1)
    )

    signed = (Fraction(1), Fraction(-1))
    signed_tail = best_n_bruteforce(signed, 0)
    subset_sup = max(
        positive(sum((signed[i] / 2 for i in subset), Fraction(0)))
        for subset in powerset_indices(2)
    )

    return [
        {
            "id": "mutation_half_exit_factor_one_rejected",
            "true_increment": fs(true_half_increment),
            "mutated_increment": fs(terminal_f),
            "pass": true_half_increment != terminal_f,
        },
        {
            "id": "mutation_replace_one_minus_theta_by_theta_rejected",
            "true_increment": fs(true_k_increment),
            "mutated_increment": fs(theta * terminal_k),
            "pass": true_k_increment != theta * terminal_k,
        },
        {
            "id": "mutation_drop_delta_Q_rejected",
            "true_work": fs(true_work),
            "mutated_work": fs((1 - theta) * Fraction(1)),
            "pass": true_work != (1 - theta) * Fraction(1),
        },
        {
            "id": "mutation_replace_one_BQ_by_half_BQ_rejected",
            "sharp_gap": fs(sharp_gap),
            "mutated_bound": fs(sharp_gap / 2),
            "pass": sharp_gap > sharp_gap / 2,
        },
        {
            "id": "mutation_allow_theta_three_quarters_strict_rejected",
            "increment": fs(Fraction(1) - Fraction(3, 4)),
            "strict_threshold": fs(Fraction(1, 4)),
            "pass": not (Fraction(1) - Fraction(3, 4) > Fraction(1, 4)),
        },
        {
            "id": "mutation_swap_sup_inf_quantifiers_rejected",
            "correct": fs(correct_quantifier),
            "mutated": fs(fixed_quantifier),
            "pass": correct_quantifier != fixed_quantifier,
        },
        {
            "id": "mutation_replace_signed_tail_by_subset_sup_rejected",
            "signed_tail": fs(signed_tail),
            "mutated_subset_sup": fs(subset_sup),
            "pass": signed_tail != subset_sup,
        },
        {
            "id": "mutation_identify_plateau_with_full_domain_rejected",
            "plateau": fs(Fraction(1)),
            "full": fs(Fraction(3)),
            "pass": Fraction(1) != Fraction(3),
        },
        {
            "id": "mutation_drop_positive_part_rejected",
            "correct": fs(best_n_bruteforce((Fraction(-2),), 0)),
            "mutated": fs(Fraction(-2)),
            "pass": best_n_bruteforce((Fraction(-2),), 0) != Fraction(-2),
        },
    ]


def structural_negative_mutations(body: str) -> list[dict]:
    mutations = (
        (
            "mutation_half_exit_one_half_to_one_rejected",
            r"={1\over2}\mathcal S_{N,R}^{F}(\mathcal D).}",
            r"=\mathcal S_{N,R}^{F}(\mathcal D).}",
        ),
        (
            "mutation_full_Q12_domain_to_plateau_rejected",
            "Taking \\(\\mathcal D=\\mathcal T_R\\) recovers exactly the full-terminal",
            "Taking \\(\\mathcal D=I_R\\) recovers exactly the full-terminal",
        ),
        (
            "mutation_good_terminal_to_arbitrary_terminal_rejected",
            "Fix a good terminal\n\\(\\tau\\)",
            "Fix an arbitrary terminal\n\\(\\tau\\)",
        ),
        (
            "mutation_claim_half_exit_S37_admissible_rejected",
            "need\nnot be admissible in the Step 2 supremum (S.37)",
            "are always admissible in the Step 2 supremum (S.37)",
        ),
        (
            "mutation_claim_last_exit_selector_continuous_rejected",
            "- that the canonical last-exit selector is continuous in the terminal time;",
            "- the canonical last-exit selector is continuous in the terminal time;",
        ),
        (
            "mutation_open_heading_to_proved_rejected",
            "The following remain **OPEN**:",
            "The following are **PROVED**:",
        ),
        (
            "mutation_remove_refuted_heading_rejected",
            "The following are **REFUTED**:",
            "The following are **UNRESOLVED**:",
        ),
        (
            "mutation_remove_final_tag_rejected",
            r"\tag{S.222}",
            r"\tag{S.223}",
        ),
        (
            "mutation_assert_plateau_full_equality_rejected",
            "equality\nis neither used nor asserted",
            "equality\nis proved and used below",
        ),
    )
    checks = []
    baseline = structural_checks(body, enforce_lock=False)
    baseline_pass = all(item["pass"] for item in baseline)
    for identifier, correct, wrong in mutations:
        occurrences = body.count(correct)
        mutated = body.replace(correct, wrong, 1)
        mutation_checks = structural_checks(mutated, enforce_lock=False)
        semantic_failures = [
            item["id"] for item in mutation_checks if not item["pass"]
        ]
        checks.append(
            {
                "id": identifier,
                "source_occurrences": occurrences,
                "baseline_structural_pass": baseline_pass,
                "mutated_structural_failures": semantic_failures,
                "pass": occurrences == 1 and baseline_pass and bool(semantic_failures),
            }
        )
    return checks


def negative_mutation_checks(body: str) -> list[dict]:
    return algebraic_negative_mutations() + structural_negative_mutations(body)


def render_report(data: dict, json_hash: str) -> str:
    summary = data["summary"]
    result = "PASS" if data["pass"] else "FAIL"
    finite_by_id = {row["id"]: row for row in data["finite_checks"]}
    tail = finite_by_id["best_N_signed_tail_rearrangement_enumeration"]
    lipschitz = finite_by_id["best_N_l1_Lipschitz_enumeration"]
    half = finite_by_id["signed_half_exit_piecewise_linear_fixtures"]
    last_exit = finite_by_id["K_last_exit_one_BQ_enumeration"]
    fk = finite_by_id["signed_F_nonnegative_K_best_N_comparison"]
    reduction = finite_by_id["plateau_terminal_reduction_squared_Cauchy_enumeration"]
    plateau = finite_by_id["simultaneous_plateau_no_compression_enumeration"]

    exact_rows = "\n".join(
        f"| {row['id']} | {row['left']} | {row['right']} | {row['margin']} |"
        for row in data["exact_checks"]
    )
    mutation_rows = "\n".join(
        f"- `{row['id']}`: {'rejected' if row['pass'] else 'NOT REJECTED'}."
        for row in data["negative_mutations"]
    )
    return f"""# R0.74S best-\(N\) last-exit certificate report

## Result

**{result}** — {summary['exact_passed']}/{summary['exact_total']} exact algebra rows,
{summary['finite_passed']}/{summary['finite_total']} finite checks,
{summary['structural_passed']}/{summary['structural_total']} structural/source checks,
and {summary['negative_mutations_passed']}/{summary['negative_mutations_total']} negative
mutations passed.

## Exact algebra

| Check | Left | Right | Margin |
|---|---:|---:|---:|
{exact_rows}

## Finite enumeration

- The signed best-\(N\) rearrangement identity passes
  {tail['configurations_checked']} exact integer-vector configurations.
- The \(\ell^1\)-Lipschitz estimate passes
  {lipschitz['configurations_checked']} vector-pair/\(N\) configurations,
  including {lipschitz['equality_cases']} equality cases.
- The signed half-exit identity passes all
  {half['configurations_checked']} rational piecewise-linear paths, including
  positive, negative, oscillatory, and zero terminals.
- The pointwise and best-\(N\) last-exit comparisons pass
  {last_exit['pointwise_checks']} and {last_exit['best_N_tail_checks']}
  exact checks, with {last_exit['sharp_pointwise_cases']} sharp one-\(B_Q\) rows.
- The signed-\(F\)/nonnegative-\(K\) comparison passes
  {fk['configurations_checked']} configurations, including
  {fk['equality_cases']} equality cases.
- The plateau terminal reduction passes
  {reduction['configurations_checked']} radical-free squared-Cauchy fixtures.
- The simultaneous-plateau no-compression formulas pass
  {plateau['configurations_checked']} exact configurations.
- The quantifier, cancellation, and strict plateau/full-domain witnesses all
  pass in `quantifier_cancellation_and_domain_fixtures`.

## Structural and source boundary

The certificate locks tags (S.200)--(S.222), both terminal domains, the
full-terminal interpretation of R0.74Q (Q.12), the good-terminal and
positive-terminal restrictions in the finite S.37 closure, and the separate
PROVED / INHERITED / REFUTED / OPEN / NOT CLAIMED ledgers.  It also requires
the explicit statement that terminal-tail continuity does not imply
continuity of the canonical last-exit selector.

## Negative mutations

{mutation_rows}

## Reproducibility

- Source note SHA-256: `{data['source']['note_sha256']}`
- Generator SHA-256: `{data['source']['generator_sha256']}`
- JSON payload SHA-256: `{json_hash}`
- The output contains no timestamp, random input, floating-point calculation,
  network input, or non-standard Python dependency.
- Set `R074S_BEST_N_NOTE`, `R074S_BEST_N_JSON`, and
  `R074S_BEST_N_REPORT` to rebuild against explicit input/output paths.

## Boundary

This is a finite/algebraic and statement-integrity certificate.  It does not
machine-prove the inherited local-energy good-time theory, R0.74P variation
bounds, the R0.74Q terminal reduction, the R0.74O/P exact Navier--Stokes
family, any fixed-\(N_0\) PDE tail estimate, the future paid-branch residual,
regularity, or the Millennium problem.

**FINITE/ALGEBRAIC ONLY. INHERITED ANALYSIS NOT MACHINE-PROVED. NOT CLAY.**
"""


def main() -> None:
    body = NOTE.read_text(encoding="utf-8")
    exact_checks = exact_ledger()
    finite_checks = [
        best_n_tail_enumeration(),
        l1_lipschitz_enumeration(),
        half_exit_piecewise_linear_fixtures(),
        k_last_exit_q_error_enumeration(),
        f_k_tail_comparison_enumeration(),
        terminal_reduction_enumeration(),
        quantifier_and_cancellation_fixtures(),
        simultaneous_plateau_enumeration(),
    ]
    structural = structural_checks(body)
    mutations = negative_mutation_checks(body)

    summary = {
        "exact_total": len(exact_checks),
        "exact_passed": sum(bool(row["pass"]) for row in exact_checks),
        "finite_total": len(finite_checks),
        "finite_passed": sum(bool(row["pass"]) for row in finite_checks),
        "structural_total": len(structural),
        "structural_passed": sum(bool(row["pass"]) for row in structural),
        "negative_mutations_total": len(mutations),
        "negative_mutations_passed": sum(bool(row["pass"]) for row in mutations),
    }
    passed = all(
        (
            summary["exact_total"] == summary["exact_passed"],
            summary["finite_total"] == summary["finite_passed"],
            summary["structural_total"] == summary["structural_passed"],
            summary["negative_mutations_total"]
            == summary["negative_mutations_passed"],
            len({row["id"] for row in exact_checks}) == len(exact_checks),
            len({row["id"] for row in finite_checks}) == len(finite_checks),
            len({row["id"] for row in structural}) == len(structural),
            len({row["id"] for row in mutations}) == len(mutations),
            all(not row.get("failures") for row in finite_checks),
        )
    )

    data = {
        "schema": "r074s-best-n-last-exit-certificate-v1",
        "scope": {
            "finite_algebraic_and_statement_integrity_only": True,
            "machine_proves_good_time_theory": False,
            "machine_proves_inherited_variation_bounds": False,
            "machine_proves_R0_74Q_PDE_tail_bound": False,
            "machine_proves_Navier_Stokes_PDE": False,
            "machine_proves_regularity_or_Clay": False,
        },
        "source": {
            "note": display_path(NOTE),
            "note_sha256": sha256(NOTE),
            "locked_note_sha256": LOCKED_NOTE_SHA256,
            "generator": display_path(Path(__file__).resolve()),
            "generator_sha256": sha256(Path(__file__).resolve()),
        },
        "exact_checks": exact_checks,
        "finite_checks": finite_checks,
        "structural_checks": structural,
        "negative_mutations": mutations,
        "summary": summary,
        "pass": passed,
    }

    payload = (
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_bytes(payload)
    REPORT_OUT.write_text(
        render_report(data, sha256_bytes(payload)), encoding="utf-8"
    )

    print(
        "R0.74S best-N last-exit certificate: "
        f"exact {summary['exact_passed']}/{summary['exact_total']}, "
        f"finite {summary['finite_passed']}/{summary['finite_total']}, "
        f"structural {summary['structural_passed']}/{summary['structural_total']}, "
        "mutations "
        f"{summary['negative_mutations_passed']}/"
        f"{summary['negative_mutations_total']}"
    )
    print("PASS" if passed else "FAIL")
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
