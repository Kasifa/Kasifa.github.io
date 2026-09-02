#!/usr/bin/env python3
"""Finite certificate for the R0.74S terminal-upcrossing stopped-work gate."""

from __future__ import annotations

import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
NOTE = REPO / "research/r074s_terminal_upcrossing_stopped_work.md"
JSON_OUT = REPO / "research/r074s_terminal_upcrossing_certificate.json"
REPORT_OUT = REPO / "research/r074s_terminal_upcrossing_certificate_report.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def finite_balance_fixture() -> dict:
    """Check the stopped K=Q+F reduction on an exact rational shell family."""
    terminal_k = [
        Fraction(8, 3),
        Fraction(7, 2),
        Fraction(13, 4),
        Fraction(11, 3),
    ]
    initial_k = [
        Fraction(4, 3),
        Fraction(19, 8),
        Fraction(9, 4),
        Fraction(8, 3),
    ]
    delta_q = [
        Fraction(1, 9),
        Fraction(-2, 7),
        Fraction(3, 11),
        Fraction(-1, 5),
    ]
    delta_k = [a - b for a, b in zip(terminal_k, initial_k)]
    delta_f = [a - b for a, b in zip(delta_k, delta_q)]
    left = sum(delta_k)
    right = sum(delta_q) + sum(delta_f)
    threshold_ok = all(
        dk > Fraction(1, 4) * tk
        for dk, tk in zip(delta_k, terminal_k)
    )
    reduced_bound = 4 * sum(abs(x) for x in delta_q) + 4 * max(
        sum(delta_f), Fraction(0)
    )
    return {
        "id": "rational_stopped_balance_fixture",
        "shells": len(terminal_k),
        "sum_delta_k": fs(left),
        "sum_delta_q_plus_f": fs(right),
        "all_quarter_upcrossings": threshold_ok,
        "terminal_sum": fs(sum(terminal_k)),
        "reduced_right_side": fs(reduced_bound),
        "identity_pass": left == right,
        "reduction_pass": sum(terminal_k) <= reduced_bound,
        "pass": left == right and threshold_ok and sum(terminal_k) <= reduced_bound,
    }


def structural_checks(body: str) -> list[dict]:
    tags = re.findall(r"\\tag\{S\.([^}]+)\}", body)
    expected = [str(k) for k in range(22, 39)]
    checks = [
        {
            "id": "tags_consecutive",
            "actual": tags,
            "expected": expected,
            "pass": tags == expected,
        },
        {
            "id": "tags_unique",
            "actual_count": len(tags),
            "unique_count": len(set(tags)),
            "pass": len(tags) == len(set(tags)) == len(expected),
        },
    ]
    required = (
        "K_{k,R}(\\tau)-K_{k,R}(\\sigma)>\\frac T4",
        "\\sum_{k\\in I}K_{k,R}(\\tau)",
        "W_R^M(\\tau;I,\\boldsymbol\\sigma)",
        "\\nabla\\Xi_{\\tau,I,\\boldsymbol\\sigma}",
        "\\sum_{k\\in I}E_{k,R}(\\sigma_k)",
        "\\le\\mathfrak L_{{\\rm abs},R}^M",
        "\\mathfrak W_{{\\rm up},R}^M\\le C A_R",
        "The stopped-work estimate at the quadratic scale remains **OPEN**",
        "**NOT CLAY.**",
    )
    forbidden = (
        "positive variation always has one net upcrossing of the same size",
        "the stopped work is bounded by A_R unconditionally",
        "the dissipation branch is closed",
        "global regularity is proved",
        "Millennium problem is solved",
    )
    for sentinel in required:
        checks.append(
            {
                "id": "required_"
                + hashlib.sha256(sentinel.encode()).hexdigest()[:12],
                "sentinel": sentinel,
                "pass": sentinel in body,
            }
        )
    for phrase in forbidden:
        checks.append(
            {
                "id": "forbidden_"
                + hashlib.sha256(phrase.encode()).hexdigest()[:12],
                "phrase": phrase,
                "pass": phrase not in body,
            }
        )
    checks.extend(
        [
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
                    ord(ch) < 32 and ch not in "\n\t" for ch in body
                ),
            },
        ]
    )
    return checks


def build_report(payload: dict) -> str:
    lines = [
        "# R0.74S terminal-upcrossing certificate report",
        "",
        "## Result",
        "",
        f"**{payload['summary']['result']}** — "
        f"{payload['summary']['exact_passed']}/"
        f"{payload['summary']['exact_total']} exact rational checks, "
        f"{payload['summary']['finite_passed']}/"
        f"{payload['summary']['finite_total']} finite balance fixtures, and "
        f"{payload['summary']['structural_passed']}/"
        f"{payload['summary']['structural_total']} structural checks passed.",
        "",
        "## Exact rational ledger",
        "",
        "| Check | Left | Right | Margin |",
        "|---|---:|---:|---:|",
    ]
    for item in payload["exact_checks"]:
        lines.append(
            f"| {item['id']} | {item['left']} | {item['right']} | "
            f"{item['margin']} |"
        )
    lines.extend(
        [
            "",
            "## Finite fixture",
            "",
            "The JSON verifies an exact four-shell rational stopped balance,",
            "the strict one-quarter upcrossing hypotheses, and the resulting",
            "factor-four terminal reduction.",
            "",
            "## Boundary",
            "",
            "This certificate does not prove good-time selection, the local",
            "energy identity, the inherited Q-variation or absolute-flux",
            "bounds, or the open signed stopped-work estimate.  It checks",
            "fractions, one exact finite fixture, tags, and claim sentinels.",
            "",
            "**FINITE ONLY. NOT CLAY.**",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    body = NOTE.read_text(encoding="utf-8")
    exact_checks = [
        exact(
            "terminal_energy_floor",
            Fraction(1, 1) - Fraction(1, 2),
            Fraction(1, 2),
            "failure of the half-dissipation branch",
        ),
        exact(
            "net_upcrossing_floor",
            Fraction(1, 2) - Fraction(1, 4),
            Fraction(1, 4),
            "terminal energy minus low stopping energy",
        ),
        exact(
            "reduction_multiplier",
            Fraction(1, 1) / Fraction(1, 4),
            Fraction(4, 1),
            "invert the one-quarter clock increment",
        ),
        exact(
            "small_payment_order",
            Fraction(1, 1) - Fraction(2, 3),
            Fraction(1, 3),
            "for P<=1, P is no larger than P^(2/3)",
        ),
        exact(
            "two_quarter_reserve",
            Fraction(1, 4) + Fraction(1, 4),
            Fraction(1, 2),
            "low stopping energy and net-upcrossing reserve",
        ),
    ]
    finite_checks = [finite_balance_fixture()]
    structural = structural_checks(body)
    passed = (
        all(item["pass"] for item in exact_checks)
        and all(item["pass"] for item in finite_checks)
        and all(item["pass"] for item in structural)
    )
    payload = {
        "schema": "r074s-terminal-upcrossing-certificate-v1",
        "scope": "FINITE ONLY: quarter thresholds, stopped balance fixture, tags, and claim boundaries",
        "note": str(NOTE.relative_to(REPO)),
        "note_sha256": sha256(NOTE),
        "exact_checks": exact_checks,
        "finite_checks": finite_checks,
        "structural_checks": structural,
        "claim_boundary": {
            "single_net_upcrossing_trichotomy": "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
            "stopped_work_identity": "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
            "quadratic_Q_payment": "INHERITED_AND_PROVED_IN_REDUCTION",
            "absolute_stopped_work_bound": "INHERITED_AND_PROVED",
            "quadratic_signed_stopped_work": "OPEN",
            "dissipation_branch": "OPEN",
            "fixed_scale_Q1_unconditional": "OPEN",
            "clay_millennium_problem_solved": False,
        },
        "summary": {
            "result": "PASS" if passed else "FAIL",
            "exact_passed": sum(bool(x["pass"]) for x in exact_checks),
            "exact_total": len(exact_checks),
            "finite_passed": sum(bool(x["pass"]) for x in finite_checks),
            "finite_total": len(finite_checks),
            "structural_passed": sum(bool(x["pass"]) for x in structural),
            "structural_total": len(structural),
        },
    }
    JSON_OUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    REPORT_OUT.write_text(build_report(payload), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
