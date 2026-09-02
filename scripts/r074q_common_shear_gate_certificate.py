#!/usr/bin/env python3
"""Finite exact certificate for the R0.74Q common-shear gate.

This producer verifies rational exponent arithmetic, the consecutive equation
tag ledger, and fail-closed claim-boundary sentinels in the analytic note.

FINITE ONLY: it does not prove the parabolic estimates, terminal-lobe lower
bounds, calibration lemma, payment inequalities, regularity, novelty, or any
Clay statement.
"""

from __future__ import annotations

import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "research" / "r074q_common_shear_multipacket_gate.md"


def q(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def compare(
    check_id: str,
    left: Fraction,
    relation: str,
    right: Fraction,
    note: str,
) -> dict:
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

alpha = Fraction(14, 15)
c_h = Fraction(15, 16)
a_d = alpha * alpha / 260
a_s = c_h * c_h / 264
rho = Fraction(1, 320)
c_gamma = Fraction(8, 3969)
m = rho - Fraction(3, 2) * c_gamma

exact_amplified_outer_rate = 4 * rho
general_normalized_outer_rate = 6 * c_gamma
conditional_cubic_outer_rate = 5 * c_gamma
platform_margin_at_base = (c_h - alpha) * 9216

checks = [
    compare("a_D_exact", a_d, "==", Fraction(49, 14625),
            "positive-platform deficit exponent"),
    compare("a_S_exact", a_s, "==", Fraction(75, 22528),
            "slow survival/shift exponent"),
    compare("a_D_above_a_S", a_d, ">", a_s,
            "inner survival reserve implies the calibration separation reserve"),
    compare("a_D_minus_a_S", a_d - a_s, "==",
            Fraction(6997, 329472000), "exact exponent margin"),
    compare("platform_margin_at_base", platform_margin_at_base, "==",
            Fraction(192, 5), "(c_h-alpha) times the base L"),
    compare("platform_margin_above_32", platform_margin_at_base, ">",
            Fraction(32), "distance from the transition edge at L=9216"),
    compare("heat_denominator", Fraction(4 * 65), "==", Fraction(260),
            "4t is at most 260 R^2 on the platform interval"),
    compare("integrated_tail_prefactor", Fraction(64 * 4), "==",
            Fraction(256), "64 R^2 interval times the pointwise tail factor"),
    compare("c_gamma_exact", c_gamma, "==", Fraction(8, 3969),
            "dyadic physical-shell weight exponent"),
    compare("m_exact", m, "==", Fraction(43, 423360),
            "R0.74O amplified-amplitude reserve"),
    compare("m_positive", m, ">", zero,
            "amplified-amplitude reserve is positive"),
    compare("amplified_ratio_exponent", m + Fraction(3, 2) * c_gamma,
            "==", rho, "m+(3/2)c_gamma=rho"),
    compare("adjacent_exact_outer_rate", exact_amplified_outer_rate, "==",
            Fraction(1, 80), "rho L_2^2=(1/80)L_1^2 for L_2=2L_1"),
    compare("exact_window_gap", exact_amplified_outer_rate - a_s, "==",
            Fraction(1033, 112640), "exact amplified proof-window gap"),
    compare("exact_window_gap_positive", exact_amplified_outer_rate, ">",
            a_s, "exact amplified outer closure conflicts with inner survival"),
    compare("general_outer_rate", general_normalized_outer_rate, "==",
            Fraction(16, 1323), "(3/2)c_gamma L_2^2 coefficient"),
    compare("general_window_gap", general_normalized_outer_rate - a_s, "==",
            Fraction(261223, 29804544), "normalized-majorant window gap"),
    compare("general_window_gap_positive", general_normalized_outer_rate, ">",
            a_s, "normalized outer majorant conflicts with inner survival"),
    compare("conditional_outer_rate", conditional_cubic_outer_rate, "==",
            Fraction(40, 3969), "(5/4)c_gamma L_2^2 coefficient"),
    compare("conditional_window_gap",
            conditional_cubic_outer_rate - a_s, "==",
            Fraction(603445, 89413632), "conditional genuine-cubic window gap"),
    compare("conditional_window_gap_positive", conditional_cubic_outer_rate,
            ">", a_s, "no-cancellation cubic lower bound conflicts with survival"),
]

note_bytes = NOTE.read_bytes()
note_text = note_bytes.decode("utf-8")
tags = re.findall(r"\\tag\{Q\.([0-9]+[a-z]?)\}", note_text)
expected_tags = (
    [str(value) for value in range(28, 48)]
    + ["47a", "48", "48a", "48b", "49", "49a", "49b", "49c"]
    + [str(value) for value in range(50, 63)]
    + ["62a"]
    + [str(value) for value in range(63, 77)]
    + ["76a"]
    + [str(value) for value in range(77, 97)]
    + ["96a"]
    + [str(value) for value in range(97, 100)]
)

required_sentinels = [
    "asymptotic frozen-geometry",
    "not an exact PDE no-go",
    "Divergence of an upper majorant does not prove",
    "The no-cancellation premise in Proposition 7.2 has not been proved",
    "**NOT CLAY.**",
    r"\boxed{\text{physical pressure flux }=0}",
    r"\boxed{\text{frozen local-pressure payment need not vanish}.}",
    r"\frac1{80}-\frac{75}{22528}",
    r"\frac{1033}{112640}>0",
    r"\frac{16}{1323}-\frac{75}{22528}",
    r"\frac{261223}{29804544}>0",
    r"\frac{40}{3969}-\frac{75}{22528}",
    r"\frac{603445}{89413632}>0",
]
forbidden_phrases = [
    "common-shear packets are impossible",
    "global regularity is proved",
    "Millennium problem is solved",
    r"\boxed{\text{the frozen local-pressure payment must vanish}.}",
]

structural_checks = [
    {
        "id": "equation_tags_consecutive",
        "pass": tags == expected_tags,
        "actual": tags,
        "expected": expected_tags,
    },
    {
        "id": "equation_tags_unique",
        "pass": len(tags) == len(set(tags)),
        "actual_count": len(tags),
        "unique_count": len(set(tags)),
    },
]
for sentinel in required_sentinels:
    structural_checks.append(
        {
            "id": "required_" + hashlib.sha256(sentinel.encode()).hexdigest()[:12],
            "pass": sentinel in note_text,
            "sentinel": sentinel,
        }
    )
for phrase in forbidden_phrases:
    structural_checks.append(
        {
            "id": "forbidden_" + hashlib.sha256(phrase.encode()).hexdigest()[:12],
            "pass": phrase not in note_text,
            "phrase": phrase,
        }
    )

all_pass = all(row["pass"] for row in checks + structural_checks)
payload = {
    "schema": "r074q-common-shear-gate-certificate-v1",
    "scope": (
        "FINITE ONLY: exact rational exponent arithmetic, equation-tag ledger, "
        "and fail-closed textual claim boundaries"
    ),
    "note": str(NOTE.relative_to(ROOT)),
    "note_sha256": hashlib.sha256(note_bytes).hexdigest(),
    "inputs": {
        "alpha": q(alpha),
        "c_h": q(c_h),
        "rho": q(rho),
        "c_gamma": q(c_gamma),
    },
    "derived": {
        "a_D": q(a_d),
        "a_S": q(a_s),
        "m": q(m),
        "exact_amplified_outer_rate": q(exact_amplified_outer_rate),
        "general_normalized_outer_rate": q(general_normalized_outer_rate),
        "conditional_cubic_outer_rate": q(conditional_cubic_outer_rate),
    },
    "checks": checks,
    "structural_checks": structural_checks,
    "claim_boundary": {
        "exact_finite_N_common_shear_NSE": "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
        "frozen_angle_common_B_obstruction": "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
        "inherited_proof_window_incompatibility": "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
        "conditional_genuine_cubic_obstruction": "CONDITIONAL",
        "all_common_shear_multipacket_families_impossible": False,
        "fixed_scale_effective_shell_inequality_decided": False,
        "global_regularity": False,
        "clay_millennium_problem_solved": False,
    },
    "analytic_boundary": [
        "does not prove the common-shear parabolic solution or NSE substitution",
        "does not prove the periodic bridge and terminal-lobe estimates",
        "does not prove the positive-platform deficit estimate",
        "does not prove the calibration obstruction or cubic-payment bounds",
        "does not prove packet-tail non-cancellation",
        "does not decide the fixed-scale effective-shell inequality",
        "does not verify literature, novelty, or priority",
        "does not prove regularity, blow-up, or any Clay statement; NOT CLAY",
    ],
    "summary": {
        "rational_passed": sum(bool(row["pass"]) for row in checks),
        "rational_total": len(checks),
        "structural_passed": sum(
            bool(row["pass"]) for row in structural_checks
        ),
        "structural_total": len(structural_checks),
        "result": "PASS" if all_pass else "FAIL",
    },
}

print(json.dumps(payload, indent=2, sort_keys=True))
if not all_pass:
    raise SystemExit(1)
