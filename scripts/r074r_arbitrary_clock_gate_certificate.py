#!/usr/bin/env python3
"""Finite certificate for the R0.74R arbitrary-clock extraction gate."""

from __future__ import annotations

import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
NOTE = REPO / "research/r074r_arbitrary_clock_extraction_gate.md"
JSON_OUT = REPO / "research/r074r_arbitrary_clock_gate_certificate.json"
REPORT_OUT = REPO / "research/r074r_arbitrary_clock_gate_certificate_report.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def f(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def exact_check(
    identifier: str,
    left: Fraction,
    relation: str,
    right: Fraction,
    note: str,
) -> dict[str, object]:
    if relation == "==":
        passed = left == right
        margin = left - right
    elif relation == ">":
        passed = left > right
        margin = left - right
    elif relation == "<":
        passed = left < right
        margin = right - left
    else:
        raise ValueError(relation)
    return {
        "id": identifier,
        "left": f(left),
        "relation": relation,
        "right": f(right),
        "margin": f(margin),
        "note": note,
        "pass": passed,
    }


def exponent_ledgers() -> list[dict[str, object]]:
    # First ledger: e <= C B gamma^(1/3) R^(4/3) g^(2/3), B=2^k.
    order_1 = ["B", "gamma", "R", "g"]
    endpoint_prefactor = tuple(Fraction(x) for x in (0, 1, -1, 0))
    volume_one_third = tuple(Fraction(x) for x in (1, 0, 1, 0))
    cubic_substitution = (
        Fraction(0),
        Fraction(-2, 3),
        Fraction(4, 3),
        Fraction(2, 3),
    )
    endpoint_bound = tuple(
        a + b + c
        for a, b, c in zip(
            endpoint_prefactor, volume_one_third, cubic_substitution
        )
    )
    endpoint_expected = (
        Fraction(1),
        Fraction(1, 3),
        Fraction(4, 3),
        Fraction(2, 3),
    )
    raised = tuple(Fraction(3, 2) * x for x in endpoint_bound)
    raised_expected = (
        Fraction(3, 2),
        Fraction(1, 2),
        Fraction(2),
        Fraction(1),
    )

    # Second ledger: solve Theta e^(3/2) <= C B^(3/2) gamma^(1/2) p.
    order_2 = ["B", "gamma", "Theta", "p"]
    before_two_thirds = (
        Fraction(3, 2),
        Fraction(1, 2),
        Fraction(-1),
        Fraction(1),
    )
    solved = tuple(Fraction(2, 3) * x for x in before_two_thirds)
    solved_expected = (
        Fraction(1),
        Fraction(1, 3),
        Fraction(-2, 3),
        Fraction(2, 3),
    )

    # Cubing the Holder coefficient B gamma^(1/3) Lambda Theta^(-2/3).
    order_3 = ["B", "gamma", "Lambda", "Theta"]
    coefficient = (
        Fraction(1),
        Fraction(1, 3),
        Fraction(1),
        Fraction(-2, 3),
    )
    coefficient_cubed = tuple(Fraction(3) * x for x in coefficient)
    coefficient_cubed_expected = (
        Fraction(3),
        Fraction(1),
        Fraction(3),
        Fraction(-2),
    )

    return [
        {
            "id": "spatial_holder_endpoint_power_ledger",
            "coordinate_order": order_1,
            "endpoint_prefactor": [f(x) for x in endpoint_prefactor],
            "volume_one_third": [f(x) for x in volume_one_third],
            "cubic_substitution": [f(x) for x in cubic_substitution],
            "reconstructed": [f(x) for x in endpoint_bound],
            "expected": [f(x) for x in endpoint_expected],
            "raised_three_halves": [f(x) for x in raised],
            "raised_expected": [f(x) for x in raised_expected],
            "pass": endpoint_bound == endpoint_expected
            and raised == raised_expected,
        },
        {
            "id": "persistence_solution_power_ledger",
            "coordinate_order": order_2,
            "before_two_thirds": [f(x) for x in before_two_thirds],
            "solved": [f(x) for x in solved],
            "expected": [f(x) for x in solved_expected],
            "pass": solved == solved_expected,
        },
        {
            "id": "ell3_coefficient_power_ledger",
            "coordinate_order": order_3,
            "coefficient": [f(x) for x in coefficient],
            "cubed": [f(x) for x in coefficient_cubed],
            "expected": [f(x) for x in coefficient_cubed_expected],
            "pass": coefficient_cubed == coefficient_cubed_expected,
        },
    ]


def structural_checks(text: str) -> list[dict[str, object]]:
    tags = re.findall(r"\\tag\{R\.([^}]+)\}", text)
    expected_tags = [str(i) for i in range(200, 226)]
    checks: list[dict[str, object]] = [
        {
            "id": "tags_consecutive",
            "actual": tags,
            "expected": expected_tags,
            "pass": tags == expected_tags,
        },
        {
            "id": "tags_unique",
            "actual_count": len(tags),
            "unique_count": len(set(tags)),
            "pass": len(tags) == len(set(tags)) == len(expected_tags),
        },
        {
            "id": "terminal_endpoint_included_in_variation",
            "pass": "\\operatorname {Var}^{+}_{J\\rightsquigarrow\\tau}" in text
            and "\\operatorname {TV}_{J\\rightsquigarrow\\tau}" in text,
        },
        {
            "id": "full_cutoff_interval_hypothesis",
            "pass": "terminal time \\(\\tau\\in(s_R,t_0)\\)" in text
            and "J_{k,\\tau}\\subset(s_R,\\tau)" in text,
        },
        {
            "id": "cutoff_weighted_persistence",
            "pass": "e_{k,R}^{\\eta}" in text
            and "p_{k,R}^{u,\\eta}" in text
            and "\\eta_R(t)^{3/2}" in text,
        },
        {
            "id": "all_time_tail_closure",
            "pass": "\\mathcal S_N(x)" in text
            and "lower semicontinuous for coordinatewise convergence" in text
            and "Local-energy good times are dense" in text,
        },
    ]
    required = (
        "D_{k,R}(\\tau)\\ge\\frac T2",
        "2^k\\gamma_k^{1/3}",
        "2^{3k}\\gamma_k\\Lambda_{k,R,\\tau}^3",
        "\\mathcal S_{N_0,R}^{K}\\le C A_R",
        "None of the constructed",
        "not Navier--Stokes solutions",
        "The arbitrary-clock extraction theorem itself remains **OPEN**",
        "**NOT CLAY.**",
    )
    forbidden = (
        "all terminal clocks contain a kinetic window",
        "dissipation is controlled by velocity cubic",
        "fixed-scale inequality (Q.1) is proved unconditionally",
        "terminal time \\(\\tau\\in I_R\\)",
        "C_1,2^{3k/2}",
        "K_{k,R}(\\tau)le CA_R",
        "global regularity is proved",
        "Millennium problem is solved",
    )
    for sentinel in required:
        checks.append(
            {
                "id": f"required_{hashlib.sha256(sentinel.encode()).hexdigest()[:12]}",
                "sentinel": sentinel,
                "pass": sentinel in text,
            }
        )
    for phrase in forbidden:
        checks.append(
            {
                "id": f"forbidden_{hashlib.sha256(phrase.encode()).hexdigest()[:12]}",
                "phrase": phrase,
                "pass": phrase not in text,
            }
        )
    checks.extend(
        [
            {
                "id": "display_math_balanced",
                "left_count": text.count("\\["),
                "right_count": text.count("\\]"),
                "pass": text.count("\\[") == text.count("\\]"),
            },
            {
                "id": "inline_math_balanced",
                "left_count": text.count("\\("),
                "right_count": text.count("\\)"),
                "pass": text.count("\\(") == text.count("\\)"),
            },
            {
                "id": "no_disallowed_control_characters",
                "pass": not any(ord(ch) < 32 and ch != "\n" for ch in text),
            },
        ]
    )
    return checks


def build_report(payload: dict[str, object]) -> str:
    rows = [
        "# R0.74R arbitrary-clock gate certificate report",
        "",
        "## Result",
        "",
        f"**{payload['summary']['result']}** — "
        f"{payload['summary']['rational_passed']}/"
        f"{payload['summary']['rational_total']} exact rational checks, "
        f"{payload['summary']['power_ledgers_passed']}/"
        f"{payload['summary']['power_ledgers_total']} exponent ledgers, and "
        f"{payload['summary']['structural_passed']}/"
        f"{payload['summary']['structural_total']} structural checks passed.",
        "",
        "## Exact rational checks",
        "",
        "| Check | Left | Relation | Right | Margin |",
        "|---|---:|:---:|---:|---:|",
    ]
    for item in payload["checks"]:
        rows.append(
            f"| `{item['id']}` | `{item['left']}` | `{item['relation']}` | "
            f"`{item['right']}` | `{item['margin']}` |"
        )
    rows.extend(
        [
            "",
            "## Power ledger",
            "",
            "The JSON checks the complete exponent chain",
            "",
            r"\[",
            r" e_k^{\eta}(t)",
            r" \lesssim2^kR^{4/3}\gamma_k^{1/3}g_k(t)^{2/3},",
            r"\]",
            "",
            r"\[",
            r" e_k^{\eta}(\tau)",
            r" \lesssim2^k\gamma_k^{1/3}(\Theta_k^{\eta})^{-2/3}(p_k^{\eta})^{2/3},",
            r"\]",
            "",
            "and the cubed coefficient",
            r"\(2^{3k}\gamma_k\Lambda_k^3(\Theta_k^{\eta})^{-2}\).",
            "",
            "## Boundary",
            "",
            "This finite certificate verifies rational constants, exponent",
            "bookkeeping, tags, and fail-closed claim sentinels.  It does not",
            "prove the local-energy identities, the inherited payment bound,",
            "the conditional hypotheses (R.216)--(R.217), or any PDE extraction",
            "theorem.  The no-go fields are not Navier--Stokes solutions.",
            "",
            "**FINITE ONLY. NOT CLAY.**",
            "",
        ]
    )
    return "\n".join(rows)


def main() -> None:
    text = NOTE.read_text(encoding="utf-8")
    checks = [
        exact_check("primary_half_split", Fraction(1, 2), "==", Fraction(1, 2), "dissipation versus endpoint split"),
        exact_check("secondary_half_split", Fraction(1, 2) * Fraction(1, 2), "==", Fraction(1, 4), "window mass versus recent variation"),
        exact_check("triage_fraction_sum", Fraction(1, 2) + 2 * Fraction(1, 4), "==", Fraction(1), "three-way threshold ledger"),
        exact_check("holder_conjugacy", Fraction(1, 3) + Fraction(2, 3), "==", Fraction(1), "ell3 and ell3/2 Holder"),
        exact_check("endpoint_gamma_after_substitution", Fraction(1) - Fraction(2, 3), "==", Fraction(1, 3), "gamma power in endpoint estimate"),
        exact_check("endpoint_R_after_substitution", Fraction(-1) + Fraction(1) + Fraction(4, 3), "==", Fraction(4, 3), "R power in endpoint estimate"),
        exact_check("raised_gamma_power", Fraction(1, 3) * Fraction(3, 2), "==", Fraction(1, 2), "gamma power before integration"),
        exact_check("raised_R_power", Fraction(4, 3) * Fraction(3, 2), "==", Fraction(2), "R squared cancels persistence normalization"),
        exact_check("cutoff_power_after_raise", Fraction(1) * Fraction(3, 2), "==", Fraction(3, 2), "eta power in the cutoff-weighted cubic row"),
        exact_check("persistence_theta_power", Fraction(-1) * Fraction(2, 3), "==", Fraction(-2, 3), "Theta exponent after solving"),
        exact_check("coefficient_cube_gamma", Fraction(1, 3) * Fraction(3), "==", Fraction(1), "gamma exponent in ell3 packing"),
        exact_check("coefficient_cube_theta", Fraction(-2, 3) * Fraction(3), "==", Fraction(-2), "Theta exponent in ell3 packing"),
        exact_check("payment_outer_power", Fraction(1) * Fraction(2, 3), "==", Fraction(2, 3), "sum p raised to two thirds"),
    ]
    ledgers = exponent_ledgers()
    structural = structural_checks(text)
    passed = (
        all(item["pass"] for item in checks)
        and all(item["pass"] for item in ledgers)
        and all(item["pass"] for item in structural)
    )
    payload = {
        "schema": "r074r-arbitrary-clock-gate-certificate-v2",
        "scope": "FINITE ONLY: triage fractions, cutoff-weighted Holder powers, all-time sentinels, tags, and claim boundaries",
        "note": str(NOTE.relative_to(REPO)),
        "note_sha256": sha256(NOTE),
        "checks": checks,
        "power_ledgers": ledgers,
        "structural_checks": structural,
        "claim_boundary": {
            "endpoint_averaging": "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
            "three_way_clock_triage": "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
            "persistence_to_payment": "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
            "good_time_to_all_time_tail_closure": "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
            "conditional_Q1_implication": "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
            "arbitrary_clock_extraction_hypotheses": "OPEN",
            "fixed_scale_Q1_unconditional": "OPEN",
            "regularity_or_singularity": "OPEN",
            "clay_millennium_problem_solved": False,
        },
        "summary": {
            "result": "PASS" if passed else "FAIL",
            "rational_passed": sum(bool(item["pass"]) for item in checks),
            "rational_total": len(checks),
            "power_ledgers_passed": sum(bool(item["pass"]) for item in ledgers),
            "power_ledgers_total": len(ledgers),
            "structural_passed": sum(bool(item["pass"]) for item in structural),
            "structural_total": len(structural),
        },
    }
    JSON_OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT_OUT.write_text(build_report(payload), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
