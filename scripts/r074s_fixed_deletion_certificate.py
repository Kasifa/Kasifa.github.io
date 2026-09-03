#!/usr/bin/env python3
"""Deterministic finite certificate for R0.74S Step 18.

The producer uses exact rational arithmetic to audit the minimax hierarchy,
layer-cake identity, completed-clock comparisons, disjoint triangular-clock
values, and the fixed-deletion linear-ledger obstruction.  It also checks the
source equation inventory, claim boundary, literature URLs, and frozen
dependencies.

This finite certificate does not machine-prove local-energy theory,
good-time density, continuum shell estimates, the open fixed-deletion gate,
regularity, or the Navier--Stokes Millennium problem.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import os
import re
import sys
from fractions import Fraction
from functools import lru_cache
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
NOTE = Path(os.environ.get(
    "R074S_FIXED_DELETION_NOTE",
    REPO / "research/r074s_fixed_deletion_simultaneous_height.md",
))
LITERATURE = Path(os.environ.get(
    "R074S_FIXED_DELETION_LITERATURE",
    REPO / "research/r074s_fixed_deletion_literature_audit.md",
))
JSON_OUT = Path(os.environ.get(
    "R074S_FIXED_DELETION_JSON",
    REPO / "research/r074s_fixed_deletion_certificate.json",
))
REPORT_OUT = Path(os.environ.get(
    "R074S_FIXED_DELETION_REPORT",
    REPO / "research/r074s_fixed_deletion_certificate_report.md",
))

SCHEMA = "r074s-fixed-deletion-certificate-v1"
MUTATION = os.environ.get("R074S_FIXED_DELETION_MUTATION", "").strip()

LOCKED_NOTE_SHA256 = "305bf75f978c080a1790fbc42bb9bd725f56f537785ffe0fc45e3ca815aa5dc1"
LOCKED_LITERATURE_SHA256 = "fea7470814c0c21399c6e2b25961e8b3791e584cc24612ac37e9d1be7ce707ce"
EXPECTED_TAGS = tuple(f"S.{number}" for number in range(476, 494))
DEPENDENCIES = {
    "step10_paid_branch": (
        REPO / "research/r074s_paid_branch_last_exit_residual.md",
        "9eb5f2a794021b49894adfc167d350f58d93c266e6be319ce835c58db2e0d74c",
    ),
    "step15_hybrid": (
        REPO / "research/r074s_hybrid_flux_tail_equivalence.md",
        "2e41f89e2ed13c09f64f09ace1b7884303e9add0b874e934ba210519b8a8ba5d",
    ),
    "step17_recurrent": (
        REPO / "research/r074s_recurrent_streamline_temporal_tail_obstruction.md",
        "7d204b326be45a82bc0d8531ea2f2d894c0c125b76e3ccbf02fdc1978a6011c5",
    ),
}

NEGATIVE_MUTATIONS = (
    "minimax_order",
    "layer_cake",
    "q_payment",
    "reverse_six",
    "triangle_fixed",
    "triangle_separable",
    "ledger_power",
    "tag_inventory",
    "claim_boundary",
    "source_hash",
    "literature_hash",
    "dependency_hash",
)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def display_path(path):
    try:
        return str(path.relative_to(REPO))
    except ValueError:
        return str(path)


@lru_cache(maxsize=None)
def deletion_sets(size, budget):
    indices = tuple(range(size))
    return tuple(
        frozenset(choice)
        for count in range(min(size, budget) + 1)
        for choice in itertools.combinations(indices, count)
    )


def tail(vector, deleted):
    return sum(
        (value for index, value in enumerate(vector) if index not in deleted),
        Fraction(0),
    )


def moving_tail(matrix, budget):
    sets = deletion_sets(len(matrix[0]), budget)
    return max(min(tail(row, deleted) for deleted in sets) for row in matrix)


def fixed_tail(matrix, budget):
    sets = deletion_sets(len(matrix[0]), budget)
    return min(max(tail(row, deleted) for row in matrix) for deleted in sets)


def separable_tail(vector, budget):
    return min(
        tail(vector, deleted)
        for deleted in deletion_sets(len(vector), budget)
    )


def coordinate_maxima(matrix):
    return tuple(max(row[index] for row in matrix)
                 for index in range(len(matrix[0])))


def layer_cake_best(vector, budget):
    levels = sorted({value for value in vector if value > 0})
    previous = Fraction(0)
    answer = Fraction(0)
    for level in levels:
        count = sum(value >= level for value in vector)
        answer += (level - previous) * max(count - budget, 0)
        previous = level
    if MUTATION == "layer_cake":
        answer += 1
    return answer


def layer_cake_outside(vector, deleted):
    levels = sorted({value for index, value in enumerate(vector)
                     if index not in deleted and value > 0})
    previous = Fraction(0)
    answer = Fraction(0)
    for level in levels:
        count = sum(
            index not in deleted and value >= level
            for index, value in enumerate(vector)
        )
        answer += (level - previous) * count
        previous = level
    return answer


def check(identifier, passed, note, cases=1, **details):
    row = {
        "id": identifier,
        "pass": bool(passed),
        "note": note,
        "cases": int(cases),
    }
    row.update(details)
    return row


def finite_matrix_cases():
    specifications = (
        (1, 1, 3),
        (2, 2, 3),
        (3, 3, 3),
        (4, 2, 3),
    )
    cases = 0
    failures = []
    strict_seen = False
    for shells, times, alphabet_size in specifications:
        for flat in itertools.product(range(alphabet_size),
                                      repeat=shells * times):
            matrix = tuple(
                tuple(Fraction(flat[time * shells + shell])
                      for shell in range(shells))
                for time in range(times)
            )
            maxima = coordinate_maxima(matrix)
            o_vector = tuple(
                value + Fraction((index + sum(flat)) % 2)
                for index, value in enumerate(maxima)
            )
            for budget in range(shells + 1):
                cases += 1
                moving = moving_tail(matrix, budget)
                fixed = fixed_tail(matrix, budget)
                excursion = separable_tail(o_vector, budget)
                max_tail = separable_tail(maxima, budget)
                if MUTATION == "minimax_order":
                    hierarchy = fixed <= moving <= excursion
                else:
                    hierarchy = moving <= fixed <= excursion
                strict_seen = strict_seen or moving < fixed
                if not hierarchy or fixed > excursion or fixed > max_tail + sum(
                        o_vector[index] - maxima[index]
                        for index in range(shells)):
                    failures.append({
                        "shells": shells,
                        "times": times,
                        "budget": budget,
                        "matrix": [[str(value) for value in row]
                                   for row in matrix],
                        "moving": str(moving),
                        "fixed": str(fixed),
                        "excursion": str(excursion),
                    })
                    if len(failures) >= 8:
                        return check(
                            "finite_minimax_and_separable_hierarchy",
                            False,
                            "A finite hierarchy case failed.",
                            cases=cases,
                            failures=failures,
                        )
    return check(
        "finite_minimax_and_separable_hierarchy",
        not failures and strict_seen,
        "Exact enumeration verifies moving deletion <= fixed deletion <= separable maxima and includes strict cases.",
        cases=cases,
        strict_case_seen=strict_seen,
    )


def layer_cake_cases():
    cases = 0
    failures = []
    # Exhaust all four-valued vectors through length five.  Length six adds
    # nearly one million redundant fixed-set identities without exercising a
    # new branch of the argument.
    for size in range(1, 6):
        for vector_raw in itertools.product(range(4), repeat=size):
            vector = tuple(Fraction(value) for value in vector_raw)
            for budget in range(size + 1):
                cases += 1
                direct = separable_tail(vector, budget)
                integral = layer_cake_best(vector, budget)
                if direct != integral:
                    failures.append({
                        "vector": list(vector_raw),
                        "budget": budget,
                        "direct": str(direct),
                        "integral": str(integral),
                    })
                    if len(failures) >= 8:
                        break
                for deleted in deletion_sets(size, budget):
                    cases += 1
                    if tail(vector, deleted) != layer_cake_outside(
                            vector, deleted):
                        failures.append({
                            "vector": list(vector_raw),
                            "deleted": sorted(deleted),
                            "kind": "fixed_set_tonelli",
                        })
                        break
            if len(failures) >= 8:
                break
        if len(failures) >= 8:
            break
    return check(
        "finite_layer_cake_and_fixed_set_tonelli",
        not failures,
        "Exact finite level integration agrees with best-N rearrangement and every fixed-set sum.",
        cases=cases,
        failures=failures,
    )


def completed_clock_cases():
    cases = 0
    failures = []
    strict_lm_seen = False
    specifications = ((2, 2, 3), (3, 3, 2), (4, 2, 3))
    for shells, times, alphabet_size in specifications:
        for flat in itertools.product(range(alphabet_size),
                                      repeat=shells * times):
            z = tuple(
                tuple(Fraction(flat[time * shells + shell])
                      for shell in range(shells))
                for time in range(times)
            )
            qvar = tuple(Fraction((shell + sum(flat)) % 3)
                         for shell in range(shells))
            k = tuple(
                tuple(max(Fraction(0), row[shell] - qvar[shell])
                      for shell in range(shells))
                for row in z
            )
            bq = sum(qvar, Fraction(0))
            for budget in range(shells + 1):
                cases += 1
                hfix = fixed_tail(z, budget)
                lvalue = fixed_tail(k, budget)
                right = lvalue + (Fraction(0)
                                  if MUTATION == "q_payment" else bq)
                if hfix > right:
                    failures.append({
                        "kind": "forward_q_payment",
                        "z": [[str(value) for value in row] for row in z],
                        "k": [[str(value) for value in row] for row in k],
                        "qvar": [str(value) for value in qvar],
                        "budget": budget,
                    })
                    if len(failures) >= 8:
                        break

                # A nonnegative shared payment vector p with total Pi
                # realizes the fixed-set hypothesis behind S.484.
                payment = tuple(Fraction((shell + 1) % 3)
                                for shell in range(shells))
                pi_value = sum(payment, Fraction(0))
                k_reverse = tuple(
                    tuple(6 * row[shell] + payment[shell]
                          for shell in range(shells))
                    for row in z
                )
                l_reverse = fixed_tail(k_reverse, budget)
                coefficient = 5 if MUTATION == "reverse_six" else 6
                if l_reverse > pi_value + coefficient * hfix:
                    failures.append({
                        "kind": "reverse_paid_branch",
                        "z": [[str(value) for value in row] for row in z],
                        "payment": [str(value) for value in payment],
                        "budget": budget,
                        "left": str(l_reverse),
                        "right": str(pi_value + coefficient * hfix),
                    })
                    if len(failures) >= 8:
                        break

                coordinate = coordinate_maxima(k_reverse)
                mvalue = separable_tail(coordinate, budget)
                strict_lm_seen = strict_lm_seen or l_reverse < mvalue
                if l_reverse > mvalue:
                    failures.append({"kind": "simultaneous_vs_separable"})
            if len(failures) >= 8:
                break
        if len(failures) >= 8:
            break
    return check(
        "completed_clock_forward_reverse_and_separable_bounds",
        not failures and strict_lm_seen,
        "Exact enumeration verifies the Q payment, paid-branch reverse coefficient six, and L <= M.",
        cases=cases,
        strict_L_below_M_seen=strict_lm_seen,
        failures=failures,
    )


def triangular_clock_cases():
    cases = 0
    failures = []
    strict_cases = 0
    for shells in range(1, 9):
        for budget in range(shells):
            for height in (Fraction(1), Fraction(3, 2), Fraction(5)):
                cases += 1
                matrix = [tuple(Fraction(0) for _ in range(shells))]
                for active in range(shells):
                    matrix.append(tuple(
                        height if shell == active else Fraction(0)
                        for shell in range(shells)
                    ))
                matrix.append(tuple(Fraction(0) for _ in range(shells)))
                matrix = tuple(matrix)

                moving = moving_tail(matrix, budget)
                fixed = fixed_tail(matrix, budget)
                lvalue = fixed
                maxima = coordinate_maxima(matrix)
                excursion = separable_tail(maxima, budget)
                mvalue = excursion
                positive_variation = separable_tail(
                    tuple(height for _ in range(shells)), budget)
                total_variation = separable_tail(
                    tuple(2 * height for _ in range(shells)), budget)
                full_tv = 2 * shells * height

                expected_moving = height if budget == 0 else Fraction(0)
                expected_fixed = (height + 1
                                  if MUTATION == "triangle_fixed"
                                  else height)
                expected_separable = (
                    (shells - budget + 1) * height
                    if MUTATION == "triangle_separable"
                    else (shells - budget) * height
                )
                passed = (
                    moving == expected_moving
                    and fixed == expected_fixed
                    and lvalue == height
                    and excursion == expected_separable
                    and mvalue == expected_separable
                    and positive_variation == expected_separable
                    and total_variation == 2 * expected_separable
                    and full_tv == 2 * shells * height
                )
                if budget >= 1 and shells >= budget + 2:
                    strict_cases += 1
                    passed = passed and (
                        moving < fixed == lvalue < excursion == mvalue
                    )
                if not passed:
                    failures.append({
                        "shells": shells,
                        "budget": budget,
                        "height": str(height),
                        "moving": str(moving),
                        "fixed": str(fixed),
                        "separable": str(excursion),
                    })
    return check(
        "disjoint_triangular_clock_exact_values",
        not failures and strict_cases > 0,
        "Every triangular-clock functional and both strict quantifier gaps agree with S.490--S.491.",
        cases=cases,
        strict_cases=strict_cases,
        failures=failures[:8],
    )


def fixed_budget_ledger_obstruction():
    cases = 0
    failures = []
    rows = []
    for budget in range(0, 7):
        shells = budget + 2
        for claimed_constant in (1, 2, 5, 10, 25):
            cases += 1
            height = Fraction(
                4 * claimed_constant ** 3 * shells ** 2 + 1
            )
            payment = 2 * shells * height
            left_cube = height ** 3
            right_cube = claimed_constant ** 3 * payment ** 2
            if MUTATION == "ledger_power":
                right_cube *= height
            passed = left_cube > right_cube
            rows.append({
                "budget": budget,
                "shells": shells,
                "claimed_constant": claimed_constant,
                "height": str(height),
                "left_cube": str(left_cube),
                "right_cube": str(right_cube),
                "pass": passed,
            })
            if not passed:
                failures.append(rows[-1])
    return check(
        "fixed_N_linear_ledger_cannot_force_two_thirds_power",
        not failures,
        "For each tested fixed N and proposed constant C, an exact height violates H <= C P^(2/3).",
        cases=cases,
        rows=rows,
        failures=failures,
    )


def structural_checks():
    note_text = NOTE.read_text(encoding="utf-8")
    literature_text = LITERATURE.read_text(encoding="utf-8")
    tags = re.findall(r"\\tag\{(S\.\d+)\}", note_text)
    expected_tags = (
        tuple(f"S.{number}" for number in range(476, 495))
        if MUTATION == "tag_inventory"
        else EXPECTED_TAGS
    )
    claim_phrases = (
        "**NOT CLAY.**",
        "Equation (S.486) is **OPEN**",
        "Equation (S.487) is also **OPEN**",
        "**ABSTRACT CLOCK STRESS TESTS**",
        "Navier--Stokes counterexample",
        "novelty or priority",
    )
    if MUTATION == "claim_boundary":
        claim_phrases = claim_phrases + ("MILLENNIUM PROBLEM SOLVED",)

    required_urls = (
        "https://doi.org/10.1002/cpa.3160350604",
        "https://doi.org/10.1088/0951-7715/13/1/312",
        "https://www.numdam.org/item/SEDP_1999-2000____A13_0/",
        "https://math.berkeley.edu/~tataru/papers/nas.pdf",
        "https://doi.org/10.1016/j.aim.2024.109654",
        "https://arxiv.org/abs/2210.01783",
        "https://arxiv.org/abs/1101.2193",
        "https://arxiv.org/abs/2008.05588",
        "https://arxiv.org/abs/2606.21783",
        "https://arxiv.org/abs/2606.25322",
        "https://arxiv.org/abs/2606.12756",
        "https://arxiv.org/abs/2606.27560",
    )

    rows = [
        check(
            "structural_tag_inventory_unique_and_ordered",
            tuple(tags) == expected_tags
            and len(tags) == len(set(tags)),
            "The source has exactly one ordered copy of S.476--S.493.",
            observed=tags,
            expected=list(expected_tags),
        ),
        check(
            "structural_display_balance",
            note_text.count(r"\[") == note_text.count(r"\]")
            and note_text.count(r"\begin{aligned}")
            == note_text.count(r"\end{aligned}")
            and note_text.count(r"\begin{gathered}")
            == note_text.count(r"\end{gathered}"),
            "Display delimiters and aligned/gathered environments balance.",
        ),
        check(
            "structural_claim_boundary",
            all(phrase in note_text for phrase in claim_phrases),
            "Open, abstract-only, non-novelty, and NOT CLAY boundaries are explicit.",
            required=list(claim_phrases),
        ),
        check(
            "structural_quantifier_and_route_language",
            all(phrase in note_text for phrase in (
                r"\sup_\tau\inf_{\#S\le N}",
                r"\inf_{\#S\le N}\sup_\tau",
                "same shell set is used for every",
                "terminal-dependent deletion set",
                "equivalent at the target scale",
            )),
            "Both quantifier orders and the route distinction are explicit.",
        ),
        check(
            "literature_primary_url_inventory",
            all(url in literature_text for url in required_urls)
            and "No row contains all target coordinates." in literature_text,
            "All primary-source and open-version URLs plus the bounded non-collision conclusion are present.",
            urls=list(required_urls),
        ),
    ]
    return rows


def hash_checks():
    expected_note = (
        "0" * 64 if MUTATION == "source_hash" else LOCKED_NOTE_SHA256
    )
    expected_literature = (
        "0" * 64
        if MUTATION == "literature_hash"
        else LOCKED_LITERATURE_SHA256
    )
    rows = [
        check(
            "locked_note_sha256",
            sha256(NOTE) == expected_note,
            "The Step 18 theorem note matches its frozen byte hash.",
            path=display_path(NOTE),
            observed=sha256(NOTE),
            expected=expected_note,
        ),
        check(
            "locked_literature_sha256",
            sha256(LITERATURE) == expected_literature,
            "The Step 18 primary-source audit matches its frozen byte hash.",
            path=display_path(LITERATURE),
            observed=sha256(LITERATURE),
            expected=expected_literature,
        ),
    ]
    for index, (name, (path, expected)) in enumerate(DEPENDENCIES.items()):
        if MUTATION == "dependency_hash" and index == 0:
            expected = "0" * 64
        rows.append(check(
            f"dependency_{name}",
            path.is_file() and sha256(path) == expected,
            "An inherited theorem dependency matches its audited hash.",
            path=display_path(path),
            observed=sha256(path) if path.is_file() else None,
            expected=expected,
        ))
    return rows


def render_report(payload):
    checks = payload["checks"]
    finite = [row for row in checks if row["group"] == "finite"]
    structural = [row for row in checks if row["group"] == "structural"]
    hashes = [row for row in checks if row["group"] == "hash"]
    lines = [
        "# R0.74S Step 18 fixed-deletion certificate report",
        "",
        f"- Schema: {SCHEMA}",
        f"- Source note: {display_path(NOTE)}",
        f"- Source SHA-256: {sha256(NOTE)}",
        f"- Literature audit: {display_path(LITERATURE)}",
        f"- Literature SHA-256: {sha256(LITERATURE)}",
        f"- Exact finite groups: {sum(row['pass'] for row in finite)}/{len(finite)}",
        f"- Exact finite cases: {sum(row['cases'] for row in finite)}",
        f"- Structural groups: {sum(row['pass'] for row in structural)}/{len(structural)}",
        f"- Hash locks: {sum(row['pass'] for row in hashes)}/{len(hashes)}",
        "",
        "## Verdict",
        "",
        f"**{payload['verdict']}**",
        "",
        "The certificate supports finite minimax arithmetic, layer-cake",
        "identities, completed-clock comparisons, triangular-clock exact",
        "values, and the abstract fixed-N ledger obstruction.  It does not",
        "machine-prove the continuum analytic inputs or an open PDE gate.",
        "",
        "## Check inventory",
        "",
        "| Check | Group | Result | Cases |",
        "|---|---|---:|---:|",
    ]
    for row in checks:
        lines.append(
            f"| {row['id']} | {row['group']} | "
            f"{'PASS' if row['pass'] else 'FAIL'} | {row['cases']} |"
        )
    lines.extend([
        "",
        "## Audited claim boundary",
        "",
        "- The moving-deletion tail is no larger than the fixed-deletion tail.",
        "- The fixed-deletion tail and completed-clock simultaneous height are equivalent only at the target scale after known payments.",
        "- The strict triangular-clock separations are abstract and are not Navier--Stokes counterexamples.",
        "- The fixed-deletion and completed-clock quadratic gates remain open.",
        "- Q.12, Q.1, scale contraction, regularity, and the Millennium problem remain open.",
        "",
        "## Explicit limitations",
        "",
        "- No machine proof of suitable-weak local-energy theory or dense good-time closure.",
        "- No machine proof of the Version-M payment estimates or Taylor asymptotics.",
        "- No proof of the open fixed-deletion stopped-flux or all-terminal completed-clock estimate.",
        "- No proof of regularity or the Navier--Stokes Millennium problem.",
        "",
    ])
    return "\n".join(lines)


def main():
    checks = []
    for row in (
        finite_matrix_cases(),
        layer_cake_cases(),
        completed_clock_cases(),
        triangular_clock_cases(),
        fixed_budget_ledger_obstruction(),
    ):
        row["group"] = "finite"
        checks.append(row)
    for row in structural_checks():
        row["group"] = "structural"
        checks.append(row)
    for row in hash_checks():
        row["group"] = "hash"
        checks.append(row)

    verdict = "PASS" if all(row["pass"] for row in checks) else "FAIL"
    payload = {
        "schema": SCHEMA,
        "verdict": verdict,
        "mutation": MUTATION or None,
        "note": {
            "path": display_path(NOTE),
            "sha256": sha256(NOTE),
        },
        "literature": {
            "path": display_path(LITERATURE),
            "sha256": sha256(LITERATURE),
        },
        "checks": checks,
        "negative_mutations": list(NEGATIVE_MUTATIONS),
        "limitations": [
            "finite rational and structural audit only",
            "no machine proof of continuum local-energy inputs",
            "no proof of the open fixed-deletion or completed-clock gate",
            "not a regularity theorem and not a Clay claim",
        ],
    }
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    REPORT_OUT.write_text(render_report(payload), encoding="utf-8")
    print(json.dumps({
        "schema": SCHEMA,
        "verdict": verdict,
        "finite_cases": sum(
            row["cases"] for row in checks if row["group"] == "finite"
        ),
        "checks_passed": sum(row["pass"] for row in checks),
        "checks_total": len(checks),
        "mutation": MUTATION or None,
    }, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
