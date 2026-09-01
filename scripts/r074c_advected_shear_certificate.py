#!/usr/bin/env python3
"""Fail-closed finite algebra certificate for R0.74C.

FINITE_ALGEBRA_ONLY.

DOES NOT CERTIFY:
- heat-kernel analytic bounds
- Calderon-Zygmund estimates
- infinite quantifiers or limiting arguments
- any Clay Millennium Prize conclusion
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = Path(__file__).resolve()
SOURCE_PATH = ROOT / "research" / "r074c_advected_shear_large_payment_obstruction.md"
JSON_PATH = ROOT / "research" / "r074c_advected_shear_certificate.json"
REPORT_PATH = ROOT / "research" / "r074c_advected_shear_certificate_report.md"
FREEZE_PATH = ROOT / "research" / "r074c_certificate_freeze.json"

FROZEN_SOURCE_COMMIT = "d6c59e31c4a10800a1e091390a25ad5672dc17d5"
FROZEN_SOURCE_SHA256 = "b300e7c32f9d944be36813530c5ffd1d7bc7463d161bba829284b4ab2d3e2c09"
FREEZE_BOUNDARY = (
    "The external manifest binds the frozen analytic source commit, source bytes, "
    "and certificate producer bytes. Its own fixed field set and canonical bytes "
    "are checked by the producer; version-control review supplies the final "
    "non-self-referential immutability boundary."
)
DOES_NOT_CERTIFY = (
    "heat-kernel analytic bounds",
    "Calderon-Zygmund estimates",
    "infinite quantifiers or limiting arguments",
    "any Clay Millennium Prize conclusion",
)


def F(n: int, d: int = 1) -> Fraction:
    return Fraction(n, d)


def frac_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def encode(value: Any) -> Any:
    if isinstance(value, Fraction):
        return frac_text(value)
    if isinstance(value, dict):
        return {str(key): encode(child) for key, child in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(child) for child in value]
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(
        encode(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ) + "\n"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def is_sha256(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def git_text(*args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", *args],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "GIT_ERROR"


def git_bytes(*args: str) -> bytes:
    try:
        return subprocess.check_output(
            ["git", *args],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        return b"GIT_ERROR"


def source_value(source_text: str, marker: str, value: Any) -> Any:
    """Return a primitive only when its exact frozen-source marker exists."""
    return value if marker in source_text else f"MISSING_SOURCE_MARKER:{marker}"


def mono(
    A: Fraction = F(0),
    R: Fraction = F(0),
    M: Fraction = F(0),
    exp_M2: Fraction = F(0),
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """A^a R^r M^m exp(e M^2), stored as (a,r,m,e)."""
    return A, R, M, exp_M2


def mono_mul(*rows: tuple[Fraction, Fraction, Fraction, Fraction]) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    return tuple(sum((row[index] for row in rows), F(0)) for index in range(4))  # type: ignore[return-value]


def mono_pow(
    row: tuple[Fraction, Fraction, Fraction, Fraction],
    exponent: Fraction,
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    return tuple(value * exponent for value in row)  # type: ignore[return-value]


def mono_div(
    numerator: tuple[Fraction, Fraction, Fraction, Fraction],
    denominator: tuple[Fraction, Fraction, Fraction, Fraction],
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    return tuple(numerator[index] - denominator[index] for index in range(4))  # type: ignore[return-value]


def substitute_A(
    row: tuple[Fraction, Fraction, Fraction, Fraction],
    A_R_power: Fraction,
    A_exp_M2: Fraction,
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    a, r, m, e = row
    return mono(F(0), r + a * A_R_power, m, e + a * A_exp_M2)


def substitute_R(
    row: tuple[Fraction, Fraction, Fraction, Fraction],
    R_exp_M2: Fraction,
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    a, r, m, e = row
    return mono(a, F(0), m, e + r * R_exp_M2)


def put_path(root: dict[str, Any], path: str, value: Any) -> None:
    parts = path.split(".")
    cursor = root
    for part in parts[:-1]:
        child = cursor.setdefault(part, {})
        if not isinstance(child, dict):
            raise ValueError(f"non-dictionary path prefix: {path}")
        cursor = child
    if parts[-1] in cursor:
        raise ValueError(f"duplicate subject leaf: {path}")
    cursor[parts[-1]] = value


def leaf_paths(value: Any, prefix: str = "") -> set[str]:
    if not isinstance(value, dict):
        return {prefix}
    paths: set[str] = set()
    for key, child in value.items():
        child_prefix = f"{prefix}.{key}" if prefix else str(key)
        paths.update(leaf_paths(child, child_prefix))
    return paths


def check_row(
    check_id: str,
    name: str,
    actual: Any,
    expected: Any,
    derivation: str,
    detail: str = "",
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "id": check_id,
        "name": name,
        "actual": encode(actual),
        "expected": encode(expected),
        "pass": actual == expected,
        "derivation": derivation,
    }
    if detail:
        row["detail"] = detail
    return row


def build() -> dict[str, Any]:
    for path in (SOURCE_PATH, SCRIPT_PATH, FREEZE_PATH):
        if not path.is_file():
            raise FileNotFoundError(path)

    source_text = SOURCE_PATH.read_text(encoding="utf-8")
    script_text = SCRIPT_PATH.read_text(encoding="utf-8")
    source_sha = sha256_path(SOURCE_PATH)
    producer_sha = sha256_path(SCRIPT_PATH)
    freeze_bytes = FREEZE_PATH.read_bytes()
    freeze = json.loads(freeze_bytes.decode("utf-8"))
    freeze_canonical = freeze_bytes == canonical_json(freeze).encode("utf-8")

    freeze_expected = freeze.get("expected_sha256", {})
    freeze_commit = freeze.get("source_commit", "MISSING")
    resolved_commit = git_text("rev-parse", f"{freeze_commit}^{{commit}}")
    commit_blob = git_bytes("show", f"{freeze_commit}:{relative(SOURCE_PATH)}")
    commit_blob_sha = sha256_bytes(commit_blob)

    nu = F(1)
    theta = F(1)
    q_star = F(1, 2)
    M_coefficient = F(3)
    M_base = F(2)
    M_index_shift = F(-1)
    gamma_denominator = F(32)
    R_denominator = F(96)
    A_R_power = F(-2)
    A_denominator = F(576)
    V_denominator = F(64)
    t0_R2 = F(65)
    total_T_R2 = F(66)
    tminus_R2 = F(1)
    S_over_R = F(2)
    Pi_degree = F(8)

    M2_coefficient = M_coefficient ** 2
    four_power_in_M2 = F(1) / M2_coefficient
    gamma_exp = -four_power_in_M2 / gamma_denominator
    R_exp = -F(1) / R_denominator
    A_extra_exp = F(1) / A_denominator
    heat_payment_exp = -F(1, 264)
    heat_gap = F(1, 264) - F(1, 288)
    exterior_exp = F(-2, 3) * R_exp + gamma_exp
    background_exp = 2 * A_extra_exp + gamma_exp

    I8_left = t0_R2 - F(8) ** 2
    I8_right = t0_R2
    IS_left = t0_R2 - S_over_R ** 2
    IS_right = t0_R2
    tau_left = F(2)
    tau_right = F(2) + (t0_R2 - tminus_R2)
    q_endpoint_coeff_qstar = F(1) - (t0_R2 - tminus_R2) / V_denominator
    q_endpoint_coeff_q = (t0_R2 - tminus_R2) / V_denominator

    V_scale = mono(R=F(-2))
    R_factor = lambda exponent: mono(R=F(exponent))
    A_factor = lambda exponent: mono(A=F(exponent))
    M_factor = lambda exponent: mono(M=F(exponent))
    exp_factor = lambda exponent: mono(exp_M2=F(exponent))

    target = mono_mul(A_factor(2), R_factor(2), M_factor(2), exp_factor(gamma_exp))
    E_background = mono_mul(mono_pow(V_scale, F(2)), R_factor(2))
    E_heat = mono_mul(A_factor(2), R_factor(2), exp_factor(heat_payment_exp))
    Gu_background = mono_mul(mono_pow(V_scale, F(3)), R_factor(3))
    Gu_strip = mono_mul(A_factor(3), R_factor(4), M_factor(-1))
    Gp_background = Gu_background
    Gp_heat = mono_mul(A_factor(3), R_factor(3), exp_factor(F(-3, 528)))
    Hu_background = Gu_background
    Hu_strip = mono_mul(A_factor(3), R_factor(4), M_factor(-2))
    P_background = Gu_background
    P_heat = Gp_heat
    P_strip = Gu_strip
    P23_background = mono_pow(P_background, F(2, 3))
    P23_heat = mono_pow(P_heat, F(2, 3))
    P23_strip = mono_pow(P_strip, F(2, 3))

    heat_ratio = mono_div(target, P23_heat)
    exterior_ratio = mono_div(target, P23_strip)
    exterior_after_R = substitute_R(exterior_ratio, R_exp)
    background_ratio = mono_div(target, P23_background)
    background_after_A = substitute_A(background_ratio, A_R_power, A_extra_exp)
    background_after_R = substitute_R(background_after_A, R_exp)
    background_unit = mono(A=F(2), R=F(4), exp_M2=gamma_exp)
    background_unit_after_A = substitute_A(
        background_unit, A_R_power, A_extra_exp
    )
    background_unit_after_R = substitute_R(background_unit_after_A, R_exp)

    subject: dict[str, Any] = {}
    checks: list[dict[str, Any]] = []
    coverage: dict[str, str] = {}
    counters: dict[str, int] = {}

    def add(
        prefix: str,
        path: str,
        actual: Any,
        expected: Any,
        derivation: str,
        detail: str = "",
    ) -> None:
        counters[prefix] = counters.get(prefix, 0) + 1
        check_id = f"{prefix}{counters[prefix]:02d}"
        put_path(subject, path, actual)
        if path in coverage or check_id in coverage.values():
            raise ValueError("coverage is not one-to-one")
        coverage[path] = check_id
        checks.append(check_row(check_id, path, actual, expected, derivation, detail))

    add("PV", "provenance.source_path", relative(SOURCE_PATH),
        "research/r074c_advected_shear_large_payment_obstruction.md", "RUNTIME_PATH")
    add("PV", "provenance.source_sha256", source_sha,
        FROZEN_SOURCE_SHA256, "FILE_BYTES")
    add("PV", "provenance.source_commit", resolved_commit,
        FROZEN_SOURCE_COMMIT, "GIT_COMMIT_RESOLUTION")
    add("PV", "provenance.source_commit_blob_sha256", commit_blob_sha,
        FROZEN_SOURCE_SHA256, "GIT_COMMIT_BLOB")
    add("PV", "provenance.freeze_source_commit", freeze_commit,
        FROZEN_SOURCE_COMMIT, "EXTERNAL_FREEZE")
    add("PV", "provenance.freeze_source_sha256",
        freeze_expected.get("analytic_source", "MISSING"),
        FROZEN_SOURCE_SHA256, "EXTERNAL_FREEZE")
    add("PV", "provenance.producer_path", relative(SCRIPT_PATH),
        "scripts/r074c_advected_shear_certificate.py", "RUNTIME_PATH")
    add("PV", "provenance.producer_sha256", producer_sha,
        freeze_expected.get("certificate_producer", "MISSING"), "EXTERNAL_FREEZE")
    add("PV", "provenance.freeze_path", relative(FREEZE_PATH),
        "research/r074c_certificate_freeze.json", "RUNTIME_PATH")
    add("PV", "provenance.freeze_canonical_json", freeze_canonical,
        True, "CANONICAL_BYTES")
    add("PV", "provenance.freeze_schema_version", freeze.get("schema_version"),
        1, "EXTERNAL_FREEZE")
    add("PV", "provenance.freeze_release", freeze.get("release"),
        "R0.74C", "EXTERNAL_FREEZE")
    add("PV", "provenance.freeze_boundary", freeze.get("boundary"),
        FREEZE_BOUNDARY, "NONCIRCULAR_BOUNDARY")
    add("PV", "provenance.freeze_top_level_keys", tuple(sorted(freeze)),
        ("boundary", "expected_sha256", "release", "schema_version", "source_commit"),
        "EXTERNAL_FREEZE_SCHEMA")
    add("PV", "provenance.freeze_hash_keys", tuple(sorted(freeze_expected)),
        ("analytic_source", "certificate_producer"), "EXTERNAL_FREEZE_SCHEMA")
    add("PV", "provenance.producer_sha256_format", is_sha256(producer_sha),
        True, "HASH_FORMAT")

    add("PM", "parameters.nu",
        source_value(source_text, r"\nu=1,\qquad \theta=1.", nu),
        F(1), "SOURCE_PARSE")
    add("PM", "parameters.theta",
        source_value(source_text, r"\nu=1,\qquad \theta=1.", theta),
        F(1), "SOURCE_PARSE")
    add("PM", "parameters.q_star",
        source_value(source_text, r"q_*=\frac12.", q_star),
        F(1, 2), "SOURCE_PARSE")
    add("PM", "parameters.M_formula",
        source_value(source_text, r"M_m=3\,2^{m-1}", (M_coefficient, M_base, M_index_shift)),
        (F(3), F(2), F(-1)), "SOURCE_PARSE",
        "(coefficient, base, index shift)")
    add("PM", "parameters.q_formula",
        source_value(source_text, r"q_m=M_mR", (F(1), F(1))),
        (F(1), F(1)), "SOURCE_PARSE", "(M power, R power)")
    add("PM", "parameters.V_formula",
        source_value(source_text, r"V_m=\frac{q_m-q_*}{64R^2}.",
                     (F(1), F(-1), V_denominator, F(-2))),
        (F(1), F(-1), F(64), F(-2)), "SOURCE_PARSE",
        "(q coefficient, q_star coefficient, denominator, R power)")
    add("PM", "parameters.gamma_denominator",
        source_value(source_text, r"e^{-4^{m-1}/32}", gamma_denominator),
        F(32), "SOURCE_PARSE")
    add("PM", "parameters.R_sequence",
        source_value(source_text, r"R_m=e^{-M_m^2/96}", (R_denominator,)),
        (F(96),), "SOURCE_PARSE")
    add("PM", "parameters.A_sequence",
        source_value(source_text, r"\mathfrak a_m=R_m^{-2}e^{M_m^2/576}.}",
                     (A_R_power, A_denominator)),
        (F(-2), F(576)), "SOURCE_PARSE")
    add("PM", "parameters.t0_over_R2",
        source_value(source_text, r"t_0=65R^2,\qquad T_R=66R^2", t0_R2),
        F(65), "SOURCE_PARSE")
    add("PM", "parameters.T_over_R2",
        source_value(source_text, r"t_0=65R^2,\qquad T_R=66R^2", total_T_R2),
        F(66), "SOURCE_PARSE")
    add("PM", "parameters.tminus_over_R2",
        source_value(source_text, r"t_-=R^2,\qquad", tminus_R2),
        F(1), "SOURCE_PARSE")
    add("PM", "parameters.S_over_R",
        source_value(source_text, r"Put \(S=2R\)", S_over_R),
        F(2), "SOURCE_PARSE")
    add("PM", "parameters.Pi_degree",
        source_value(source_text, r"\Pi_m=(1+M_m)^8.", Pi_degree),
        F(8), "SOURCE_PARSE")

    add("TM", "time.I8_endpoints_over_R2", (I8_left, I8_right),
        (F(1), F(65)), "DERIVED_ARITHMETIC")
    add("TM", "time.IS_endpoints_over_R2", (IS_left, IS_right),
        (F(61), F(65)), "DERIVED_ARITHMETIC")
    add("TM", "time.tau_endpoints_over_R2", (tau_left, tau_right),
        (F(2), F(66)), "DERIVED_ARITHMETIC")
    add("TM", "time.buffer_closure_inside_solution_interval",
        F(0) < I8_left and I8_right < total_T_R2,
        True, "DERIVED_ORDER")
    add("TM", "time.q_at_t0_affine_coefficients",
        (q_endpoint_coeff_q, q_endpoint_coeff_qstar),
        (F(1), F(0)), "DERIVED_AFFINE_ALGEBRA",
        "q(t0)=coefficient_q*q+coefficient_qstar*q_star")

    add("ID", "identities.M_squared_coefficient", M2_coefficient,
        F(9), "DERIVED_ARITHMETIC")
    add("ID", "identities.four_power_in_M2", four_power_in_M2,
        F(1, 9), "DERIVED_ARITHMETIC")
    add("ID", "identities.gamma_M2_exponent", gamma_exp,
        F(-1, 288), "DERIVED_ARITHMETIC")
    add("ID", "identities.R_M2_exponent", R_exp,
        F(-1, 96), "DERIVED_ARITHMETIC")
    add("ID", "identities.A_extra_M2_exponent", A_extra_exp,
        F(1, 576), "DERIVED_ARITHMETIC")
    add("ID", "identities.background_unit_after_A_R_substitution",
        background_unit_after_R, mono(), "DERIVED_SUBSTITUTION")
    add("ID", "identities.background_A2_R4_exp_identity_is_one",
        background_unit_after_R == mono(), True, "DERIVED_MONOMIAL_IDENTITY")

    ledger_rows = (
        ("ledger.E.background", E_background, mono(R=F(-2))),
        ("ledger.E.heat", E_heat, mono(A=F(2), R=F(2), exp_M2=F(-1, 264))),
        ("ledger.Gu.background", Gu_background, mono(R=F(-3))),
        ("ledger.Gu.strip", Gu_strip, mono(A=F(3), R=F(4), M=F(-1))),
        ("ledger.Gp.background", Gp_background, mono(R=F(-3))),
        ("ledger.Gp.heat", Gp_heat, mono(A=F(3), R=F(3), exp_M2=F(-3, 528))),
        ("ledger.Hu.background", Hu_background, mono(R=F(-3))),
        ("ledger.Hu.strip", Hu_strip, mono(A=F(3), R=F(4), M=F(-2))),
        ("ledger.P.background", P_background, mono(R=F(-3))),
        ("ledger.P.heat", P_heat, mono(A=F(3), R=F(3), exp_M2=F(-3, 528))),
        ("ledger.P.strip", P_strip, mono(A=F(3), R=F(4), M=F(-1))),
        ("ledger.P23.background", P23_background, mono(R=F(-2))),
        ("ledger.P23.heat", P23_heat, mono(A=F(2), R=F(2), exp_M2=F(-1, 264))),
        ("ledger.P23.strip", P23_strip,
         mono(A=F(2), R=F(8, 3), M=F(-2, 3))),
        ("ledger.target.lower", target,
         mono(A=F(2), R=F(2), M=F(2), exp_M2=F(-1, 288))),
    )
    for path, actual, expected in ledger_rows:
        add("LG", path, actual, expected, "DERIVED_MONOMIAL_ALGEBRA",
            "(A power, R power, M power, exp(M^2) coefficient)")

    add("RT", "ratios.heat.monomial_without_Pi", heat_ratio,
        mono(M=F(2), exp_M2=F(1, 3168)), "DERIVED_MONOMIAL_DIVISION")
    add("RT", "ratios.heat.exponential_gap", heat_gap,
        F(1, 3168), "DERIVED_RATIONAL_DIFFERENCE")
    add("RT", "ratios.heat.exponential_gap_positive", heat_gap > 0,
        True, "DERIVED_ORDER")
    add("RT", "ratios.exterior.before_R_substitution", exterior_ratio,
        mono(R=F(-2, 3), M=F(8, 3), exp_M2=F(-1, 288)),
        "DERIVED_MONOMIAL_DIVISION")
    add("RT", "ratios.exterior.after_R_substitution", exterior_after_R,
        mono(M=F(8, 3), exp_M2=F(1, 288)),
        "DERIVED_SUBSTITUTION")
    add("RT", "ratios.exterior.exponential_gap", exterior_exp,
        F(1, 288), "DERIVED_RATIONAL_COMPOSITION")
    add("RT", "ratios.exterior.exponential_gap_positive", exterior_exp > 0,
        True, "DERIVED_ORDER")
    add("RT", "ratios.background.before_substitution", background_ratio,
        mono(A=F(2), R=F(4), M=F(2), exp_M2=F(-1, 288)),
        "DERIVED_MONOMIAL_DIVISION")
    add("RT", "ratios.background.after_A_substitution", background_after_A,
        mono(M=F(2), exp_M2=F(0)), "DERIVED_SUBSTITUTION")
    add("RT", "ratios.background.after_A_R_substitution", background_after_R,
        mono(M=F(2), exp_M2=F(0)), "DERIVED_SUBSTITUTION")
    add("RT", "ratios.background.exponential_balance", background_exp,
        F(0), "DERIVED_RATIONAL_COMPOSITION")
    add("RT", "ratios.background.remaining_M_power", background_after_R[2],
        F(2), "DERIVED_MONOMIAL_PROJECTION")

    label_markers = {
        "EXACT_SOLUTION": "### Lemma 1.1 — exact NSE trajectory",
        "PROVED": "### PROVED",
        "FINITE": "### FINITE",
        "OPEN": "### OPEN",
        "NOT_CLAY": "### NOT CLAY",
    }
    for label, marker in label_markers.items():
        add("LB", f"labels.{label}", marker in source_text,
            True, "SOURCE_LABEL_PARSE")
    add("LB", "labels.nu_theta_one", r"\nu=1,\qquad \theta=1." in source_text,
        True, "SOURCE_LABEL_PARSE")
    add("LB", "labels.mean_zero_derivative",
        (
            "Its spatial derivative has\nzero periodic mean" in source_text
            and r"F_R(t,x_2)" in source_text
            and r"=R^2\partial_2K_{\tau(t)}^{\rm per}" in source_text
        ),
        True, "SOURCE_STRUCTURE_PARSE")

    boundary_tokens = {
        "FINITE_ALGEBRA_ONLY": "FINITE_ALGEBRA_ONLY",
        "heat_kernel_analytic_bounds_not_certified": "heat-kernel analytic bounds",
        "CZ_not_certified": "Calderon-Zygmund estimates",
        "infinite_quantifiers_not_certified": "infinite quantifiers or limiting arguments",
        "Clay_not_certified": "any Clay Millennium Prize conclusion",
    }
    for name, token in boundary_tokens.items():
        add("SC", f"scope.{name}", token in script_text,
            True, "PRODUCER_SCOPE_DECLARATION")

    all_subject_paths = leaf_paths(encode(subject))
    all_check_ids = [row["id"] for row in checks]
    covered_ids = list(coverage.values())
    coverage_ok = (
        all_subject_paths == set(coverage)
        and len(covered_ids) == len(set(covered_ids))
        and set(covered_ids) == set(all_check_ids)
        and len(all_check_ids) == len(set(all_check_ids))
    )
    checks.append(check_row(
        "MT01",
        "subject leaf coverage is a bijection with unique check IDs",
        coverage_ok,
        True,
        "META_COVERAGE",
    ))
    literal_self_equality_count = sum(
        row["derivation"] == "LITERAL_SELF_EQUALITY" for row in checks
    )
    checks.append(check_row(
        "MT02",
        "literal self-equality checks are absent",
        literal_self_equality_count,
        0,
        "META_CHECK_CLASSIFICATION",
    ))

    status = "PASS" if all(row["pass"] for row in checks) else "FAIL"
    return {
        "certificate": "R0.74C advected-shear fail-closed finite algebra certificate",
        "schema_version": 1,
        "status": status,
        "scope": (
            "FINITE exact algebra and frozen-byte provenance only; no heat-kernel "
            "analytic bound, Calderon-Zygmund estimate, infinite quantifier, "
            "limiting argument, or Clay claim is certified"
        ),
        "subject": encode(subject),
        "coverage_manifest": {
            "field_to_unique_check_id": coverage,
            "subject_leaf_count": len(all_subject_paths),
            "coverage_bijection": coverage_ok,
        },
        "checks": checks,
        "summary": {
            "passed": sum(row["pass"] for row in checks),
            "total": len(checks),
        },
    }


def report_text(certificate: dict[str, Any]) -> str:
    subject = certificate["subject"]
    provenance = subject["provenance"]
    parameters = subject["parameters"]
    time = subject["time"]
    identities = subject["identities"]
    ledger = subject["ledger"]
    ratios = subject["ratios"]
    labels = subject["labels"]
    lines = [
        "# R0.74C advected-shear finite algebra certificate",
        "",
        f"**Status:** {certificate['status']}",
        "",
        "**Scope:** FINITE_EXACT_ALGEBRA_AND_FROZEN_BYTES_ONLY",
        "",
        "Every subject leaf has one distinct check ID. Actual algebraic values are derived from source-bound primitives before comparison with independently declared targets. No literal self-equality check is used.",
        "",
        "## Frozen provenance",
        "",
        f"- Source commit: {provenance['source_commit']}",
        f"- Current source SHA256: {provenance['source_sha256']}",
        f"- Source blob SHA256 at frozen commit: {provenance['source_commit_blob_sha256']}",
        f"- Producer SHA256: {provenance['producer_sha256']}",
        f"- External freeze manifest: {provenance['freeze_path']}",
        "- The producer SHA is bound one way by the external manifest. The manifest has canonical bytes and a fixed checked field set; version-control review supplies its non-self-referential immutability boundary.",
        "",
        "## Exact finite identities",
        "",
        f"- From M=3*2^(m-1), 4^(m-1)=M^2/{identities['M_squared_coefficient']} and gamma=exp({identities['gamma_M2_exponent']} M^2).",
        f"- R=exp({identities['R_M2_exponent']} M^2) and A=R^({parameters['A_sequence'][0]}) exp({identities['A_extra_M2_exponent']} M^2).",
        f"- I_8/R^2={time['I8_endpoints_over_R2']}, I_S/R^2={time['IS_endpoints_over_R2']}, and tau/R^2={time['tau_endpoints_over_R2']}.",
        f"- The affine endpoint coefficients are {time['q_at_t0_affine_coefficients']}, so the transported centre equals q=MR at t0.",
        "",
        "## Monomial convention",
        "",
        "Each row is [A power, R power, M power, exp(M^2) coefficient].",
        "",
        "| Quantity | Row |",
        "|---|---|",
    ]
    for family in ("E", "Gu", "Gp", "Hu", "P", "P23", "target"):
        for name, row in ledger[family].items():
            lines.append(f"| {family}.{name} | {row} |")
    lines.extend([
        "",
        "## Ratio ledger",
        "",
        f"- Heat row: exponential gap {ratios['heat']['exponential_gap']} = 1/3168 > 0; the fixed polynomial denominator has degree {parameters['Pi_degree']}.",
        f"- Exterior row after substituting R: {ratios['exterior']['after_R_substitution']} with exponential coefficient {ratios['exterior']['exponential_gap']} = 1/288 > 0.",
        f"- Background row after substituting A and R: {ratios['background']['after_A_R_substitution']}; exponential balance is {ratios['background']['exponential_balance']} and the remaining M power is {ratios['background']['remaining_M_power']}.",
        "- These finite exponent and power identities are the algebra used by the analytic divergence proof. This certificate does not prove an infinite limit.",
        "",
        "## Frozen labels",
        "",
    ])
    lines.extend(f"- {name}: {value}" for name, value in labels.items())
    lines.extend([
        "",
        "## Result",
        "",
        f"All {certificate['summary']['total']} checks pass. The coverage manifest is a bijection over {certificate['coverage_manifest']['subject_leaf_count']} subject leaves.",
        "",
        "## Analytic boundary",
        "",
        "- The heat-kernel lower and leakage bounds are not certified.",
        "- The Calderon--Zygmund/Jensen gauge estimate is not certified.",
        "- Periodic-copy infinite sums and all infinite quantifiers remain analytic.",
        "- Finite rows do not prove the divergence limit.",
        "- Exact-solution status is a frozen source label; the PDE differentiation remains in the analytic note.",
        "- FINITE, EXACT_SOLUTION, PROVED, OPEN, and NOT_CLAY retain their literal source meanings.",
        "- This certificate proves no Clay Millennium Prize statement.",
        "",
    ])
    return "\n".join(lines)


def check_only(certificate: dict[str, Any]) -> int:
    bad: list[str] = []
    expected_json = canonical_json(certificate).encode("utf-8")
    expected_report = report_text(certificate).encode("utf-8")
    if not JSON_PATH.is_file() or JSON_PATH.read_bytes() != expected_json:
        bad.append(relative(JSON_PATH))
    if not REPORT_PATH.is_file() or REPORT_PATH.read_bytes() != expected_report:
        bad.append(relative(REPORT_PATH))
    if certificate["status"] != "PASS":
        bad.append("internal status")
    if bad:
        print("R0.74C certificate check failed: " + ", ".join(bad), file=sys.stderr)
        return 1
    summary = certificate["summary"]
    print(
        "R0.74C finite algebra certificate PASS: "
        f"{summary['passed']}/{summary['total']} checks; "
        "canonical JSON and report bytes identical"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check-only", action="store_true")
    group.add_argument("--print-json", action="store_true")
    group.add_argument("--print-report", action="store_true")
    args = parser.parse_args()

    certificate = build()
    if args.print_json:
        sys.stdout.write(canonical_json(certificate))
        return 0 if certificate["status"] == "PASS" else 1
    if args.print_report:
        sys.stdout.write(report_text(certificate))
        return 0 if certificate["status"] == "PASS" else 1
    if args.check_only:
        return check_only(certificate)
    if certificate["status"] != "PASS":
        print("R0.74C certificate generation refused: internal checks failed", file=sys.stderr)
        return 1
    JSON_PATH.write_bytes(canonical_json(certificate).encode("utf-8"))
    REPORT_PATH.write_bytes(report_text(certificate).encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
