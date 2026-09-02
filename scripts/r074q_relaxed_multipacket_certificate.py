#!/usr/bin/env python3
"""Finite, fail-closed certificate for the R0.74Q relaxed multipacket gate.

This producer checks exact rational arithmetic and binds those checks to the
tagged formulas and claim boundaries in the analytic note.  It does not prove
any PDE estimate, asymptotic theorem, novelty claim, or Clay statement.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "research" / "r074q_relaxed_multipacket_cubic_obstruction.md"


def q(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def compare(check_id: str, left: Fraction, relation: str,
            right: Fraction, note: str) -> dict:
    if relation == "==":
        passed, margin = left == right, left - right
    elif relation == ">":
        passed, margin = left > right, left - right
    elif relation == "<":
        passed, margin = left < right, right - left
    elif relation == "<=":
        passed, margin = left <= right, right - left
    else:
        raise ValueError(f"unsupported relation: {relation}")
    return {
        "id": check_id,
        "left": q(left),
        "margin": q(margin),
        "note": note,
        "pass": passed,
        "relation": relation,
        "right": q(right),
    }


zero = Fraction(0)
half = Fraction(1, 2)
quarter = Fraction(1, 4)
lambda_ = Fraction(63, 32)
c_h = Fraction(15, 16)
alpha = Fraction(14, 15)
rho = Fraction(1, 320)
a_d = Fraction(49, 14625)
a_s = Fraction(75, 22528)
c_gamma = Fraction(8, 3969)
a_x = alpha * alpha / 264
l_n_ratio = 1 / (2 * lambda_)

checks = [
    compare("lambda_between_1_and_2_lower", lambda_, ">", Fraction(1),
            "lambda in (1,2) makes floor(log2(lambda*2^j))=j"),
    compare("lambda_between_1_and_2_upper", lambda_, "<", Fraction(2),
            "lambda in (1,2) makes floor(log2(lambda*2^j))=j"),
    compare("L_N_ratio_algebra", l_n_ratio, "==", Fraction(16, 63),
            "L_N/L^2=1/(2 lambda) when N=j"),
    compare("L_N_strict_lower", l_n_ratio, ">", quarter,
            "strict lower bound L^2/4<L_N"),
    compare("L_N_upper", l_n_ratio, "<=", half,
            "upper bound L_N<=L^2/2"),
    compare("a_D_minus_rho", a_d - rho, "==", Fraction(211, 936000),
            "positive-platform inversion reserve"),
    compare("a_D_minus_rho_positive", a_d - rho, ">", zero,
            "positive-platform inversion reserve is positive"),
    compare("a_S_minus_rho", a_s - rho, "==", Fraction(23, 112640),
            "inner survival reserve"),
    compare("a_S_minus_rho_positive", a_s - rho, ">", zero,
            "inner survival reserve is positive"),
    compare("a_x_exact", a_x, "==", Fraction(49, 14850),
            "cross-packet heat-tail exponent"),
    compare("a_x_minus_three_halves_c_gamma",
            a_x - Fraction(3, 2) * c_gamma, "==", Fraction(67, 242550),
            "amplitude-weighted adjacent-packet margin"),
    compare("a_x_margin_positive", a_x - Fraction(3, 2) * c_gamma,
            ">", zero, "adjacent-packet margin is positive"),
    compare("five_c_gamma_minus_a_S", 5 * c_gamma - a_s, "==",
            Fraction(603445, 89413632), "cubic target exponent conflict"),
    compare("five_c_gamma_minus_a_S_positive", 5 * c_gamma - a_s,
            ">", zero, "cubic target exponent conflict is positive"),
    compare("annular_margin_left", c_h * c_h + Fraction(1, 256), "==",
            Fraction(113, 128), "uniform moving-lobe annular margin"),
    compare("annular_margin_strict", c_h * c_h + Fraction(1, 256), "<",
            Fraction(64, 63) ** 2, "strict annular containment margin"),
    compare("leading_log_coefficient", 5 * c_gamma / 96, "==",
            Fraction(5, 47628), "positive L^4 coefficient in Q.170"),
    compare("leading_log_coefficient_positive", 5 * c_gamma / 96, ">",
            zero, "positive L^4 coefficient in Q.170"),
    compare("mu_in_exact", a_x / 4 + Fraction(3, 4) * (c_gamma / 2),
            "==", Fraction(4601, 2910600),
            "adjacent inner-packet exponent in Q.151"),
    compare("mu_in_positive", a_x / 4 + Fraction(3, 4) * (c_gamma / 2),
            ">", zero, "adjacent inner-packet exponent is positive"),
    compare("periodic_polynomial_exponent",
            (c_gamma / 2) * l_n_ratio * l_n_ratio, "==",
            Fraction(1024, 15752961), "q L_N^2 coefficient in Q.155"),
    compare("periodic_double_exponent", 2 * rho, "==", Fraction(1, 160),
            "R^{-2}=exp(L^2/160) in Q.155"),
]

try:
    note_bytes = NOTE.read_bytes()
    note_text = note_bytes.decode("utf-8")
    note_read_error = None
except (OSError, UnicodeDecodeError) as exc:
    note_bytes = b""
    note_text = ""
    note_read_error = f"{type(exc).__name__}: {exc}"

tags = re.findall(r"\\tag\{Q\.([0-9]+[a-z]?)\}", note_text)
expected_tags = [str(value) for value in range(100, 181)]

required_sentinels = [
    r"L_N=\frac{L^2}{2\lambda}=\frac{16}{63}L^2",
    r"\frac{L^2}{4}<L_N\le\frac{L^2}{2}",
    r"a_D-\rho",
    r"\frac{211}{936000}>0",
    r"a_S-\rho",
    r"\frac{23}{112640}>0",
    r"c_h^2+\frac1{256}",
    r"\frac{113}{128}",
    r"\left(\frac{64}{63}\right)^2",
    r"a_\times=\frac{\alpha^2}{264}=\frac{49}{14850}",
    r"a_\times-\frac32c_\gamma",
    r"\frac{67}{242550}>0",
    r"\mu_{\rm in}",
    r"\frac{4601}{2910600}>0",
    r"qL_N^2=\frac{1024}{15752961}L^4",
    r"R^{-2}=e^{L^2/160}",
    r"\gamma_{k_N-1}",
    r"=\Gamma_N^{1/4}",
    r"\frac{(P_R^{M,(N)})^{2/3}}{NT}",
    r"-\log N-O(1)",
    r"\frac{5c_\gamma}{96}=\frac5{47628}>0",
    r"5c_\gamma-a_S",
    r"\frac{603445}{89413632}>0",
    "Statement (Q.178) remains **OPEN** for this family.",
    "This is a quantitative obstruction for one canonical smooth stress-test",
    "It is not a theorem that every common-shear family fails",
    "**NOT CLAY.**",
    "<!-- R074Q_STEP2_STATUS_GEOMETRY_PROVED -->",
    "<!-- R074Q_STEP2_STATUS_CUBIC_PAYMENT_PROVED -->",
    "<!-- R074Q_STEP2_STATUS_SIGNED_FLUX_OPEN -->",
    "<!-- R074Q_STEP2_END -->",
]

forbidden_phrases = [
    "signed cumulative flux is proved",
    "all common-shear families fail",
    "fixed-scale inequality (Q.1) is proved",
    "global regularity is proved",
    "Millennium problem is solved",
]

structural_checks = [
    {"id": "note_readable_utf8", "pass": note_read_error is None,
     "error": note_read_error},
    {"id": "equation_tags_consecutive", "pass": tags == expected_tags,
     "actual": tags, "expected": expected_tags},
    {"id": "equation_tags_unique", "pass": len(tags) == len(set(tags)),
     "actual_count": len(tags), "unique_count": len(set(tags))},
    {"id": "no_disallowed_control_characters",
     "pass": not any(ord(char) < 32 and char not in "\n\r" for char in note_text),
     "note": "tabs and non-newline C0 controls are forbidden"},
    {"id": "no_malformed_qquad", "pass": ",qquad" not in note_text,
     "sentinel": ",qquad"},
]
for sentinel in required_sentinels:
    structural_checks.append({
        "id": "required_" + hashlib.sha256(sentinel.encode()).hexdigest()[:12],
        "pass": sentinel in note_text,
        "sentinel": sentinel,
    })
for phrase in forbidden_phrases:
    structural_checks.append({
        "id": "forbidden_" + hashlib.sha256(phrase.encode()).hexdigest()[:12],
        "pass": phrase not in note_text,
        "phrase": phrase,
    })

all_pass = all(row["pass"] for row in checks + structural_checks)
payload = {
    "analytic_boundary": [
        "does not prove the heat-shear estimates, periodic bridge, or packet dominance lemmas",
        "does not prove the outer-lobe PDE lower bound or terminal clock lower bound",
        "does not prove signed cumulative flux of order NT; Q.178 remains OPEN",
        "does not prove a matching full Y2 upper bound or decide fixed-scale Q.1",
        "does not verify literature, novelty, or priority",
        "does not prove regularity, blow-up, or any Clay statement; NOT CLAY",
    ],
    "checks": checks,
    "claim_boundary": {
        "geometry_and_uniform_packet_dominance": "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
        "outer_cubic_payment_obstruction": "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
        "terminal_K_lower": "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
        "signed_cumulative_flux_order_NT": "OPEN",
        "matching_full_Y2_upper": "OPEN",
        "fixed_scale_effective_shell_inequality_decided": False,
        "global_regularity": False,
        "clay_millennium_problem_solved": False,
    },
    "derived": {
        "L_N_over_L_squared": q(l_n_ratio),
        "a_D_minus_rho": q(a_d - rho),
        "a_S_minus_rho": q(a_s - rho),
        "a_x": q(a_x),
        "a_x_minus_three_halves_c_gamma": q(a_x - Fraction(3, 2) * c_gamma),
        "annular_margin_left": q(c_h * c_h + Fraction(1, 256)),
        "five_c_gamma_minus_a_S": q(5 * c_gamma - a_s),
        "leading_log_coefficient": q(5 * c_gamma / 96),
    },
    "inputs": {
        "a_D": q(a_d), "a_S": q(a_s), "alpha": q(alpha),
        "c_gamma": q(c_gamma), "c_h": q(c_h), "lambda": q(lambda_),
        "rho": q(rho),
    },
    "note": str(NOTE.relative_to(ROOT)),
    "note_sha256": hashlib.sha256(note_bytes).hexdigest(),
    "schema": "r074q-relaxed-multipacket-certificate-v1",
    "scope": "FINITE ONLY: rational arithmetic, tag ledger, source sentinels, and fail-closed claim boundaries",
    "structural_checks": structural_checks,
    "summary": {
        "rational_passed": sum(bool(row["pass"]) for row in checks),
        "rational_total": len(checks),
        "result": "PASS" if all_pass else "FAIL",
        "structural_passed": sum(bool(row["pass"]) for row in structural_checks),
        "structural_total": len(structural_checks),
    },
}

rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
if len(sys.argv) == 1:
    sys.stdout.write(rendered)
elif len(sys.argv) == 3 and sys.argv[1] == "--output":
    Path(sys.argv[2]).write_text(rendered, encoding="utf-8")
else:
    raise SystemExit("usage: producer [--output PATH]")
if not all_pass:
    raise SystemExit(1)
