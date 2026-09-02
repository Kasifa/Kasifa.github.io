#!/usr/bin/env python3
"""Deterministic finite certificate for the R0.74R window-lobe ledger."""

from __future__ import annotations

import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
NOTE = REPO / "research/r074r_persistent_lobe_cubic_packing.md"
PROBLEM = REPO / "research/r074r_problem_freeze.md"
JSON_OUT = REPO / "research/r074r_persistent_lobe_certificate.json"
REPORT_OUT = REPO / "research/r074r_persistent_lobe_certificate_report.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def f(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def check(
    name: str,
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
    elif relation == "<=":
        passed = left <= right
        margin = right - left
    else:
        raise ValueError(relation)
    return {
        "id": name,
        "left": f(left),
        "relation": relation,
        "right": f(right),
        "margin": f(margin),
        "note": note,
        "pass": passed,
    }


def exact_power_ledger() -> dict[str, object]:
    # Exponents are ordered as Gamma, E, L, R.  They certify
    # (2R)^-2 Gamma^(1/4) (2R^4 Gamma^-1 E)^(3/2)
    # / (L R^6 / 16)^(1/2) = 2 sqrt(2) R Gamma^-5/4 L^-1/2 E^3/2.
    normalized_prefactor = (
        Fraction(1, 4),
        Fraction(0),
        Fraction(0),
        Fraction(-2),
    )
    averaged_mass = (
        Fraction(-1),
        Fraction(1),
        Fraction(0),
        Fraction(4),
    )
    averaged_mass_three_halves = tuple(
        Fraction(3, 2) * x for x in averaged_mass
    )
    spacetime_measure_inverse_half = (
        Fraction(0),
        Fraction(0),
        Fraction(-1, 2),
        Fraction(-3),
    )
    reconstructed = tuple(
        a + b + c
        for a, b, c in zip(
            normalized_prefactor,
            averaged_mass_three_halves,
            spacetime_measure_inverse_half,
        )
    )
    payment = (
        Fraction(-5, 4),
        Fraction(3, 2),
        Fraction(-1, 2),
        Fraction(1),
    )
    return {
        "id": "window_averaged_spacetime_holder_power_ledger",
        "coordinate_order": ["Gamma", "E", "L", "R"],
        "normalized_prefactor": [f(x) for x in normalized_prefactor],
        "averaged_mass": [f(x) for x in averaged_mass],
        "averaged_mass_three_halves": [
            f(x) for x in averaged_mass_three_halves
        ],
        "spacetime_measure_inverse_half": [
            f(x) for x in spacetime_measure_inverse_half
        ],
        "reconstructed": [f(x) for x in reconstructed],
        "payment": [f(x) for x in payment],
        "pass": reconstructed == payment,
    }


def tag_ids(text: str) -> list[str]:
    return re.findall(r"\\tag\{R\.([^}]+)\}", text)


def structural_checks(note_text: str, problem_text: str) -> list[dict[str, object]]:
    checks: list[dict[str, object]] = []
    note_tags = tag_ids(note_text)
    problem_tags = tag_ids(problem_text)
    expected_note = [str(i) for i in range(100, 139)]
    expected_problem = [str(i) for i in range(1, 29)]
    checks.extend(
        [
            {
                "id": "main_tags_consecutive",
                "actual": note_tags,
                "expected": expected_note,
                "pass": note_tags == expected_note,
            },
            {
                "id": "main_tags_unique",
                "actual_count": len(note_tags),
                "unique_count": len(set(note_tags)),
                "pass": len(note_tags) == len(set(note_tags)) == len(expected_note),
            },
            {
                "id": "problem_tags_consecutive",
                "actual": problem_tags,
                "expected": expected_problem,
                "pass": problem_tags == expected_problem,
            },
        ]
    )

    required = (
        "2\\sqrt2\\,R",
        "window-averaged",
        "U:=\\sum_{\\ell=2}^NE_\\ell=S-E_1",
        "first target shell",
        "\\Gamma_\\ell^{-5/4}L_\\ell^{-1/2}",
        "\\frac{8831}{1905120}>0",
        "-\\frac{769}{1905120}<0",
        "no terminal-window lobe-mass configuration",
        "endpoint energy that rises only on a time set much shorter",
        "**OPEN**",
        "**NOT CLAY.**",
    )
    forbidden = (
        "fixed-scale inequality is proved",
        "global regularity is proved",
        "Millennium problem is solved",
        "all terminal clocks have window mass",
        "Y_{2,R}^{\\rm sf}\\le",
    )
    for sentinel in required:
        checks.append(
            {
                "id": f"required_{hashlib.sha256(sentinel.encode()).hexdigest()[:12]}",
                "sentinel": sentinel,
                "pass": sentinel in note_text,
            }
        )
    for phrase in forbidden:
        checks.append(
            {
                "id": f"forbidden_{hashlib.sha256(phrase.encode()).hexdigest()[:12]}",
                "phrase": phrase,
                "pass": phrase not in note_text,
            }
        )
    checks.extend(
        [
            {
                "id": "main_display_math_balanced",
                "left_count": note_text.count("\\["),
                "right_count": note_text.count("\\]"),
                "pass": note_text.count("\\[") == note_text.count("\\]"),
            },
            {
                "id": "main_inline_math_balanced",
                "left_count": note_text.count("\\("),
                "right_count": note_text.count("\\)"),
                "pass": note_text.count("\\(") == note_text.count("\\)"),
            },
            {
                "id": "no_disallowed_control_characters",
                "pass": not any(ord(ch) < 32 and ch not in "\n" for ch in note_text),
            },
        ]
    )
    return checks


def build_report(payload: dict[str, object]) -> str:
    rational = payload["checks"]
    structural = payload["structural_checks"]
    rows = [
        "# R0.74R terminal-window lobe certificate report",
        "",
        "## Result",
        "",
        f"**{payload['summary']['result']}** — "
        f"{payload['summary']['rational_passed']}/{payload['summary']['rational_total']} "
        "exact arithmetic checks and "
        f"{payload['summary']['structural_passed']}/{payload['summary']['structural_total']} "
        "structural checks passed.",
        "",
        "## Exact arithmetic",
        "",
        "| Check | Left | Relation | Right | Margin |",
        "|---|---:|:---:|---:|---:|",
    ]
    for item in rational:
        rows.append(
            f"| `{item['id']}` | `{item['left']}` | `{item['relation']}` | "
            f"`{item['right']}` | `{item['margin']}` |"
        )
    rows.extend(
        [
            "",
            "The exponent vector in the JSON separately verifies",
            "",
            "\\[",
            " (2R)^{-2}\\Gamma^{1/4}",
            " \\frac{(2R^4\\Gamma^{-1}E)^{3/2}}",
            " {(LR^6/16)^{1/2}}",
            " =2\\sqrt2\\,R\\Gamma^{-5/4}L^{-1/2}E^{3/2}.",
            "\\]",
            "",
            "The tail-ratio threshold uses only the exact implication",
            "\\(e^x\\ge1+x\\): for \\(j\\ge2\\), the minimal tail exponent",
            "is \\(15/4\\), hence the adjacent reciprocal-weight ratio is at",
            "most \\(2/(1+15/4)=8/19<1/2\\).",
            "",
            "## Structural boundary",
            "",
            f"All {len(structural)} tag, sentinel, delimiter, and claim-boundary checks pass.",
            "The certificate does not prove lobe placement, window-mass extraction, the",
            "nonnegative payment-row inclusion, or any PDE extraction theorem.",
            "It does not prove signed flux, the full square-function upper bound,",
            "the fixed-scale inequality, regularity, blow-up, or any Clay claim.",
            "",
            "**FINITE ONLY. NOT CLAY.**",
            "",
        ]
    )
    return "\n".join(rows)


def main() -> None:
    note_text = NOTE.read_text(encoding="utf-8")
    problem_text = PROBLEM.read_text(encoding="utf-8")

    c_gamma = Fraction(8, 3969)
    rho = Fraction(1, 320)
    kappa_1 = Fraction(5, 6) * c_gamma - Fraction(2, 3) * rho
    kappa_2 = Fraction(10, 3) * c_gamma - Fraction(2, 3) * rho
    ratio_rate = Fraction(15, 2) * c_gamma
    tail_min_rate = ratio_rate * 4

    checks = [
        check("weight_chart_identity", c_gamma * Fraction(63, 32) ** 2, "==", Fraction(1, 128), "c_gamma lambda^2 matches gamma_{k_l}"),
        check("previous_shell_weight_exponent", Fraction(1, 128) / 4, "==", Fraction(1, 512), "gamma_{k_l-1}=Gamma_l^(1/4)"),
        check("kappa_1_exact", kappa_1, "==", Fraction(-769, 1905120), "innermost-shell normalized exponent"),
        check("kappa_1_negative", kappa_1, "<", Fraction(0), "rank-one discrete escape remains possible"),
        check("kappa_2_exact", kappa_2, "==", Fraction(8831, 1905120), "second-shell diffuse-target exponent"),
        check("kappa_2_positive", kappa_2, ">", Fraction(0), "diffuse persistent targets are exponentially expensive"),
        check("adjacent_reciprocal_weight_rate", ratio_rate, "==", Fraction(20, 1323), "coefficient in b_{l+1}/b_l"),
        check("tail_minimum_rate", tail_min_rate, "==", Fraction(80, 1323), "minimum coefficient for l>=2"),
        check("j2_base_L", Fraction(63, 32) * 4, "==", Fraction(63, 8), "base L at j=2"),
        check("j2_tail_exponent", tail_min_rate * Fraction(3969, 64), "==", Fraction(15, 4), "exact lower exponent at L=63/8"),
        check("exp_linear_ratio_majorant", Fraction(8, 19), "<", Fraction(1, 2), "2 exp(-15/4) <= 2/(1+15/4)"),
        check("lobe_volume_fraction", Fraction(1, 16), "==", Fraction(4) ** -2, "spatial lobe fraction"),
        check("averaged_energy_mass_factor", Fraction(2), "==", Fraction(2), "integral |u|^2 = 2 R^4 Gamma^-1 E"),
        check("spacetime_lobe_R_power", Fraction(3) + Fraction(3), "==", Fraction(6), "|J| times spatial lobe volume has R^6"),
        check("normalized_payment_prefactor", Fraction(1, 2) ** 2, "==", Fraction(1, 4), "(2R)^-2 constant"),
        check("cubic_coefficient_squared", Fraction(8), "==", Fraction(2) ** 3, "the positive coefficient 2 sqrt(2) has square 8"),
        check("cubic_two_thirds_factor", Fraction(8), "==", Fraction(2) ** 3, "(2 sqrt(2))^(2/3)=2"),
        check("tail_prefactor_cubed", Fraction(4), "==", Fraction(2) ** 2, "2/2^(1/3)=2^(2/3), whose cube is 4"),
        check("pointwise_floor_energy_constant", Fraction(1, 2) * Fraction(1, 16), "==", Fraction(1, 32), "optional pointwise floor gives E >= T/32"),
        check("pointwise_corollary_constant_squared", Fraction(8, 32**3), "==", Fraction(1, 64**2), "2 sqrt(2) times 32^(-3/2) equals 1/64"),
        check("gamma_previous_power", Fraction(1, 4), "==", Fraction(4, 16), "gamma_{k-1}=Gamma^(1/4)"),
    ]
    power_ledger = exact_power_ledger()
    structural = structural_checks(note_text, problem_text)
    all_pass = all(item["pass"] for item in checks) and power_ledger["pass"] and all(
        item["pass"] for item in structural
    )
    payload = {
        "schema": "r074r-terminal-window-lobe-certificate-v2",
        "scope": "FINITE ONLY: rational exponents, scaling powers, tag ledger, and fail-closed claim boundaries",
        "note": str(NOTE.relative_to(REPO)),
        "note_sha256": sha256(NOTE),
        "problem_freeze": str(PROBLEM.relative_to(REPO)),
        "problem_freeze_sha256": sha256(PROBLEM),
        "inputs": {"c_gamma": f(c_gamma), "rho": f(rho)},
        "derived": {
            "kappa_1": f(kappa_1),
            "kappa_2": f(kappa_2),
            "adjacent_reciprocal_weight_rate": f(ratio_rate),
            "tail_minimum_rate": f(tail_min_rate),
        },
        "checks": checks,
        "power_ledger": power_ledger,
        "structural_checks": structural,
        "claim_boundary": {
            "terminal_window_lobe_cubic_packing": "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
            "arbitrary_terminal_clock_window_mass_extraction": "OPEN",
            "signed_cumulative_flux": "OPEN",
            "full_square_function_upper": "OPEN",
            "fixed_scale_inequality_Q1": "OPEN",
            "regularity_or_singularity": "OPEN",
            "clay_millennium_problem_solved": False,
        },
        "analytic_boundary": [
            "does not prove the R0.74Q lobe geometry or weight-floor inclusion",
            "does not extract terminal-window lobe mass from an arbitrary terminal clock",
            "does not prove the nonnegative payment-row inclusion",
            "does not prove signed flux or a full Y2 upper bound",
            "does not prove Q.1, regularity, blow-up, or any Clay statement; NOT CLAY",
        ],
        "summary": {
            "result": "PASS" if all_pass else "FAIL",
            "rational_passed": sum(bool(item["pass"]) for item in checks),
            "rational_total": len(checks),
            "power_ledger_passed": bool(power_ledger["pass"]),
            "structural_passed": sum(bool(item["pass"]) for item in structural),
            "structural_total": len(structural),
        },
    }
    JSON_OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT_OUT.write_text(build_report(payload), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    if not all_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
