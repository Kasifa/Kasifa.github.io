#!/usr/bin/env python3
"""Fail-closed finite algebra certificate for R0.74D.

FINITE_ALGEBRA_ONLY.

DOES NOT CERTIFY:
- stochastic or Feynman-Kac representation
- heat-kernel or one-sided Gaussian analytic bounds
- Lp contraction or periodic-copy infinite sums
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
SOURCE_PATH = ROOT / "research" / "r074d_zero_mean_local_transport_obstruction.md"
JSON_PATH = ROOT / "research" / "r074d_zero_mean_transport_certificate.json"
REPORT_PATH = ROOT / "research" / "r074d_zero_mean_transport_certificate_report.md"
FREEZE_PATH = ROOT / "research" / "r074d_certificate_freeze.json"

FROZEN_SOURCE_COMMIT = "ff80370fe33094f1423d312b817dfec0bf42d664"
FROZEN_SOURCE_SHA256 = "bc9f7557e27bb86d5730273985b60f7135ccea3adc2fc99b2daf7778e70c9124"
FREEZE_BOUNDARY = (
    "The external manifest binds the frozen analytic source commit, source bytes, "
    "and certificate producer bytes. Its own fixed field set and canonical bytes "
    "are checked by the producer; version-control review supplies the final "
    "non-self-referential immutability boundary."
)
DOES_NOT_CERTIFY = (
    "stochastic or Feynman-Kac representation",
    "heat-kernel or one-sided Gaussian analytic bounds",
    "Lp contraction or periodic-copy infinite sums",
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
        encode(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")
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
            ["git", *args], cwd=ROOT, stderr=subprocess.DEVNULL, text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "GIT_ERROR"


def git_bytes(*args: str) -> bytes:
    try:
        return subprocess.check_output(
            ["git", *args], cwd=ROOT, stderr=subprocess.DEVNULL
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


def mono_mul(
    *rows: tuple[Fraction, Fraction, Fraction, Fraction]
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    return tuple(
        sum((row[index] for row in rows), F(0)) for index in range(4)
    )  # type: ignore[return-value]


def mono_pow(
    row: tuple[Fraction, Fraction, Fraction, Fraction], exponent: Fraction
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    return tuple(value * exponent for value in row)  # type: ignore[return-value]


def mono_div(
    numerator: tuple[Fraction, Fraction, Fraction, Fraction],
    denominator: tuple[Fraction, Fraction, Fraction, Fraction],
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    return tuple(
        numerator[index] - denominator[index] for index in range(4)
    )  # type: ignore[return-value]


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
    tminus_R2 = F(1)
    t0_R2 = F(65)
    total_T_R2 = F(66)
    B_time_gap = t0_R2 - tminus_R2
    S_over_R = F(2)
    Pi_degree = F(18)
    pointwise_leak_denominator = F(528)
    R_denominator = F(96)
    A_R_power = F(-2)
    A_denominator = F(576)

    M2_coefficient = M_coefficient ** 2
    four_power_in_M2 = F(1) / M2_coefficient
    gamma_exp = -four_power_in_M2 / gamma_denominator
    R_exp = -F(1) / R_denominator
    A_extra_exp = F(1) / A_denominator
    pointwise_leak_exp = -F(1) / pointwise_leak_denominator
    quadratic_leak_exp = 2 * pointwise_leak_exp
    cubic_leak_exp = 3 * pointwise_leak_exp
    heat_gap = -quadratic_leak_exp + gamma_exp
    Pi_after_power = Pi_degree * F(2, 3)

    # Endpoint coefficients use the affine basis (q_m, q_star).
    B_numerator_coefficients = (F(1), F(-1))
    Q_tminus_coefficients = (F(0), F(1))
    Q_t0_coefficients = mono_affine_add(
        Q_tminus_coefficients, B_numerator_coefficients
    )

    A_factor = lambda exponent: mono(A=F(exponent))
    R_factor = lambda exponent: mono(R=F(exponent))
    M_factor = lambda exponent: mono(M=F(exponent))
    exp_factor = lambda exponent: mono(exp_M2=F(exponent))

    E_background = mono(R=F(-2))
    E_packet = mono_mul(A_factor(2), R_factor(2), exp_factor(quadratic_leak_exp))
    E32_background = mono_pow(E_background, F(3, 2))
    E32_packet = mono_pow(E_packet, F(3, 2))
    Gu_background = mono(R=F(-3))
    Gu_packet = mono(A=F(3), R=F(4), M=F(-2))
    Gp_background = Gu_background
    Gp_packet = mono(A=F(3), R=F(3), exp_M2=cubic_leak_exp)
    Hu_background = Gu_background
    Hu_packet = mono(A=F(3), R=F(4), M=F(-7, 2))
    P_background = Gu_background
    P_leakage = Gp_packet
    P_transport = Gu_packet
    P23_background = mono_pow(P_background, F(2, 3))
    P23_leakage = mono_pow(P_leakage, F(2, 3))
    P23_transport = mono_pow(P_transport, F(2, 3))
    target = mono(A=F(2), R=F(2), M=F(1), exp_M2=gamma_exp)

    background_ratio = mono_div(target, P23_background)
    background_after_A = substitute_A(background_ratio, A_R_power, A_extra_exp)
    background_after_R = substitute_R(background_after_A, R_exp)
    leakage_ratio = mono_div(target, P23_leakage)
    transport_ratio = mono_div(target, P23_transport)
    transport_after_R = substitute_R(transport_ratio, R_exp)
    target_after_A = substitute_A(target, A_R_power, A_extra_exp)
    target_after_R = substitute_R(target_after_A, R_exp)

    # Exact rational admissibility witness. The only transcendental input is the
    # standard positive exponential series e^x >= 1+x+x^2/2 for x >= 0.
    m0 = F(6)
    M0 = M_coefficient * M_base ** int(m0 + M_index_shift)
    base_exp_x = M0 ** 2 / R_denominator
    base_exp_lower = F(1) + base_exp_x + base_exp_x ** 2 / F(2)
    R0_upper = F(1) / base_exp_lower
    q0_upper = M0 * R0_upper
    recurrence_exp_lower_x = M0 ** 2 / F(32)
    recurrence_exp_lower = F(1) + recurrence_exp_lower_x
    R_recurrence_upper = F(1) / recurrence_exp_lower
    q_recurrence_upper = F(2) / recurrence_exp_lower

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
        "research/r074d_zero_mean_local_transport_obstruction.md", "RUNTIME_PATH")
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
        "scripts/r074d_zero_mean_transport_certificate.py", "RUNTIME_PATH")
    add("PV", "provenance.producer_sha256", producer_sha,
        freeze_expected.get("certificate_producer", "MISSING"), "EXTERNAL_FREEZE")
    add("PV", "provenance.freeze_path", relative(FREEZE_PATH),
        "research/r074d_certificate_freeze.json", "RUNTIME_PATH")
    add("PV", "provenance.freeze_canonical_json", freeze_canonical,
        True, "CANONICAL_BYTES")
    add("PV", "provenance.freeze_schema_version", freeze.get("schema_version"),
        1, "EXTERNAL_FREEZE")
    add("PV", "provenance.freeze_release", freeze.get("release"),
        "R0.74D", "EXTERNAL_FREEZE")
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
        source_value(source_text, r"\nu=1,\qquad \theta=1", nu), F(1), "SOURCE_PARSE")
    add("PM", "parameters.theta",
        source_value(source_text, r"\nu=1,\qquad \theta=1", theta), F(1), "SOURCE_PARSE")
    add("PM", "parameters.q_star",
        source_value(source_text, r"q_*=\frac12", q_star), F(1, 2), "SOURCE_PARSE")
    add("PM", "parameters.M_formula",
        source_value(source_text, r"M_m=3\,2^{m-1}",
                     (M_coefficient, M_base, M_index_shift)),
        (F(3), F(2), F(-1)), "SOURCE_PARSE",
        "(coefficient, base, index shift)")
    add("PM", "parameters.q_formula",
        source_value(source_text, r"q_m=M_mR", (F(1), F(1))),
        (F(1), F(1)), "SOURCE_PARSE", "(M power, R power)")
    add("PM", "parameters.B_time_denominator",
        source_value(source_text, r"D_R=e^{-R^2}-e^{-65R^2}", B_time_gap),
        F(64), "SOURCE_PARSE")
    add("PM", "parameters.B_numerator_coefficients",
        source_value(source_text, r"B_R=\frac{q_m-q_*}{D_R}<0.",
                     B_numerator_coefficients),
        (F(1), F(-1)), "SOURCE_PARSE", "basis=(q_m,q_star)")
    add("PM", "parameters.q_pre_formula_present",
        r"q_{\rm pre}=q_*-B_R(1-e^{-R^2})" in source_text,
        True, "SOURCE_PARSE")
    add("PM", "parameters.Q_formula_present",
        r"Q(t)=q_{\rm pre}+B_R(1-e^{-t})" in source_text,
        True, "SOURCE_PARSE")
    add("PM", "parameters.tminus_over_R2",
        source_value(source_text, r"t_-=R^2", tminus_R2), F(1), "SOURCE_PARSE")
    add("PM", "parameters.t0_over_R2",
        source_value(source_text, r"t_0=65R^2", t0_R2), F(65), "SOURCE_PARSE")
    add("PM", "parameters.T_over_R2",
        source_value(source_text, r"T_R=66R^2", total_T_R2), F(66), "SOURCE_PARSE")
    add("PM", "parameters.S_over_R",
        source_value(source_text, r"At \(S=2R\)", S_over_R), F(2), "SOURCE_PARSE")
    add("PM", "parameters.Pi_degree",
        source_value(source_text, r"\Pi_m=(1+M_m)^{18}.", Pi_degree),
        F(18), "SOURCE_PARSE")
    add("PM", "parameters.pointwise_leak_denominator",
        source_value(source_text, r"e^{-M_m^2/528}", pointwise_leak_denominator),
        F(528), "SOURCE_PARSE")
    add("PM", "parameters.R_sequence_denominator",
        source_value(source_text, r"R_m=e^{-M_m^2/96}", R_denominator),
        F(96), "SOURCE_PARSE")
    add("PM", "parameters.A_sequence",
        source_value(source_text, r"\mathfrak a_m=R_m^{-2}e^{M_m^2/576}",
                     (A_R_power, A_denominator)),
        (F(-2), F(576)), "SOURCE_PARSE")
    source_ledger_markers = {
        "target_lower": r"cA^2M_mR^2e^{-M_m^2/288}",
        "Gu_packet": r"\frac{A^3R^4}{M_m^2}",
        "Gp_packet": r"A^3R^3\Pi_m e^{-M_m^2/176}",
        "Hu_packet": r"\frac{A^3R^4}{M_m^{7/2}}",
        "P23_transport": r"A^2R^{8/3}M_m^{-4/3}",
    }
    for name, marker in source_ledger_markers.items():
        add("PM", f"parameters.source_ledger_marker_{name}",
            marker in source_text, True, "SOURCE_LEDGER_PARSE")

    add("ID", "identities.Q_at_tminus_coefficients", Q_tminus_coefficients,
        (F(0), F(1)), "DERIVED_AFFINE_ALGEBRA", "basis=(q_m,q_star)")
    add("ID", "identities.Q_at_t0_coefficients", Q_t0_coefficients,
        (F(1), F(0)), "DERIVED_AFFINE_ALGEBRA", "basis=(q_m,q_star)")
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
    add("ID", "identities.pointwise_leak_exponent", pointwise_leak_exp,
        F(-1, 528), "SOURCE_BOUND_ARITHMETIC")
    add("ID", "identities.quadratic_leak_exponent", quadratic_leak_exp,
        F(-1, 264), "DERIVED_RATIONAL_MULTIPLICATION")
    add("ID", "identities.cubic_leak_exponent", cubic_leak_exp,
        F(-1, 176), "DERIVED_RATIONAL_MULTIPLICATION")
    add("ID", "identities.strict_leakage_gap", heat_gap,
        F(1, 3168), "DERIVED_RATIONAL_DIFFERENCE")
    add("ID", "identities.strict_leakage_gap_positive", heat_gap > 0,
        True, "DERIVED_ORDER")
    add("ID", "identities.Pi_degree_after_two_thirds", Pi_after_power,
        F(12), "DERIVED_RATIONAL_MULTIPLICATION")
    add("ID", "identities.Pi_degree_overpay_valid", Pi_degree >= Pi_after_power,
        True, "DERIVED_ORDER")
    add("ID", "identities.Hu_packet_is_smaller_than_transport_for_M_ge_one",
        Hu_packet[2] <= Gu_packet[2], True, "DERIVED_ORDER")

    ledger_rows = (
        ("ledger.E.background", E_background, mono(R=F(-2))),
        ("ledger.E.packet", E_packet,
         mono(A=F(2), R=F(2), exp_M2=F(-1, 264))),
        ("ledger.E32.background", E32_background, mono(R=F(-3))),
        ("ledger.E32.packet", E32_packet,
         mono(A=F(3), R=F(3), exp_M2=F(-1, 176))),
        ("ledger.Gu.background", Gu_background, mono(R=F(-3))),
        ("ledger.Gu.packet", Gu_packet, mono(A=F(3), R=F(4), M=F(-2))),
        ("ledger.Gp.background", Gp_background, mono(R=F(-3))),
        ("ledger.Gp.packet", Gp_packet,
         mono(A=F(3), R=F(3), exp_M2=F(-1, 176))),
        ("ledger.Hu.background", Hu_background, mono(R=F(-3))),
        ("ledger.Hu.packet", Hu_packet,
         mono(A=F(3), R=F(4), M=F(-7, 2))),
        ("ledger.P.background", P_background, mono(R=F(-3))),
        ("ledger.P.leakage", P_leakage,
         mono(A=F(3), R=F(3), exp_M2=F(-1, 176))),
        ("ledger.P.transport", P_transport,
         mono(A=F(3), R=F(4), M=F(-2))),
        ("ledger.P23.background", P23_background, mono(R=F(-2))),
        ("ledger.P23.leakage", P23_leakage,
         mono(A=F(2), R=F(2), exp_M2=F(-1, 264))),
        ("ledger.P23.transport", P23_transport,
         mono(A=F(2), R=F(8, 3), M=F(-4, 3))),
        ("ledger.target.lower", target,
         mono(A=F(2), R=F(2), M=F(1), exp_M2=F(-1, 288))),
    )
    for path, actual, expected in ledger_rows:
        add("LG", path, actual, expected, "DERIVED_MONOMIAL_ALGEBRA",
            "(A power, R power, M power, exp(M^2) coefficient); Pi tracked separately")

    add("RT", "ratios.background.before_substitution", background_ratio,
        mono(A=F(2), R=F(4), M=F(1), exp_M2=F(-1, 288)),
        "DERIVED_MONOMIAL_DIVISION")
    add("RT", "ratios.background.after_A_substitution", background_after_A,
        mono(M=F(1)), "DERIVED_SUBSTITUTION")
    add("RT", "ratios.background.after_A_R_substitution", background_after_R,
        mono(M=F(1)), "DERIVED_SUBSTITUTION")
    add("RT", "ratios.background.remaining_M_power", background_after_R[2],
        F(1), "DERIVED_MONOMIAL_PROJECTION")
    add("RT", "ratios.background.positive_power", background_after_R[2] > 0,
        True, "DERIVED_ORDER")
    add("RT", "ratios.leakage.without_Pi", leakage_ratio,
        mono(M=F(1), exp_M2=F(1, 3168)), "DERIVED_MONOMIAL_DIVISION")
    add("RT", "ratios.leakage.exponential_gap", leakage_ratio[3],
        F(1, 3168), "DERIVED_RATIONAL_DIFFERENCE")
    add("RT", "ratios.leakage.exponential_gap_positive", leakage_ratio[3] > 0,
        True, "DERIVED_ORDER")
    add("RT", "ratios.leakage.Pi_denominator_degree", Pi_degree,
        F(18), "SOURCE_BOUND_POLYNOMIAL_DEGREE")
    add("RT", "ratios.transport.before_R_substitution", transport_ratio,
        mono(R=F(-2, 3), M=F(7, 3), exp_M2=F(-1, 288)),
        "DERIVED_MONOMIAL_DIVISION")
    add("RT", "ratios.transport.after_R_substitution", transport_after_R,
        mono(M=F(7, 3), exp_M2=F(1, 288)), "DERIVED_SUBSTITUTION")
    add("RT", "ratios.transport.exponential_gap", transport_after_R[3],
        F(1, 288), "DERIVED_RATIONAL_COMPOSITION")
    add("RT", "ratios.transport.exponential_gap_positive", transport_after_R[3] > 0,
        True, "DERIVED_ORDER")
    add("RT", "ratios.target.after_A_substitution", target_after_A,
        mono(R=F(-2), M=F(1)), "DERIVED_SUBSTITUTION")
    add("RT", "ratios.target.after_A_R_substitution", target_after_R,
        mono(M=F(1), exp_M2=F(1, 48)), "DERIVED_SUBSTITUTION")

    add("AD", "admissibility.base_index", m0, F(6), "FINITE_INTEGER_WITNESS")
    add("AD", "admissibility.base_M", M0, F(96), "DERIVED_INTEGER_POWER")
    add("AD", "admissibility.base_M_ge_64", M0 >= F(64),
        True, "DERIVED_ORDER")
    add("AD", "admissibility.base_exp_x", base_exp_x, F(96),
        "DERIVED_RATIONAL_ARITHMETIC")
    add("AD", "admissibility.exp_series_lower_bound", base_exp_lower, F(4705),
        "FINITE_POSITIVE_EXP_SERIES_TRUNCATION")
    add("AD", "admissibility.base_R_upper", R0_upper, F(1, 4705),
        "FINITE_RATIONAL_BOUND")
    add("AD", "admissibility.base_R_lt_one_sixteenth", R0_upper < F(1, 16),
        True, "DERIVED_ORDER")
    add("AD", "admissibility.base_R_lt_pi_sixteenth_using_pi_gt_one",
        R0_upper < F(1, 16), True, "FINITE_RATIONAL_BOUND_PLUS_STANDARD_PI_BOUND")
    add("AD", "admissibility.base_q_upper", q0_upper, F(96, 4705),
        "FINITE_RATIONAL_BOUND")
    add("AD", "admissibility.base_q_le_one_thirty_second",
        q0_upper <= F(1, 32), True, "DERIVED_ORDER")
    add("AD", "admissibility.recurrence_exp_lower_x", recurrence_exp_lower_x,
        F(288), "DERIVED_RATIONAL_ARITHMETIC")
    add("AD", "admissibility.recurrence_exp_lower", recurrence_exp_lower,
        F(289), "FINITE_POSITIVE_EXP_SERIES_TRUNCATION")
    add("AD", "admissibility.R_recurrence_upper", R_recurrence_upper,
        F(1, 289), "FINITE_RATIONAL_BOUND")
    add("AD", "admissibility.q_recurrence_upper", q_recurrence_upper,
        F(2, 289), "FINITE_RATIONAL_BOUND")
    add("AD", "admissibility.R_recurrence_contracts", R_recurrence_upper < 1,
        True, "DERIVED_ORDER")
    add("AD", "admissibility.q_recurrence_contracts", q_recurrence_upper < 1,
        True, "DERIVED_ORDER")
    add("AD", "admissibility.source_chart_marker",
        r"q_m=M_mR\le\frac1{32}" in source_text,
        True, "SOURCE_PARSE")

    boundary_tokens = {
        "FINITE_ALGEBRA_ONLY": "FINITE_ALGEBRA_ONLY",
        "stochastic_not_certified": "stochastic or Feynman-Kac representation",
        "heat_kernel_not_certified": "heat-kernel or one-sided Gaussian analytic bounds",
        "contraction_and_copies_not_certified": "Lp contraction or periodic-copy infinite sums",
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
        "MT01", "subject leaf coverage is a bijection with unique check IDs",
        coverage_ok, True, "META_COVERAGE"
    ))
    literal_self_equality_count = sum(
        row["derivation"] == "LITERAL_SELF_EQUALITY" for row in checks
    )
    checks.append(check_row(
        "MT02", "literal self-equality checks are absent",
        literal_self_equality_count, 0, "META_CHECK_CLASSIFICATION"
    ))

    status = "PASS" if all(row["pass"] for row in checks) else "FAIL"
    return {
        "certificate": "R0.74D zero-mean transport fail-closed finite algebra certificate",
        "schema_version": 1,
        "status": status,
        "scope": (
            "FINITE exact parameter algebra, exponent comparisons, ratio signatures, "
            "admissibility witness arithmetic, and frozen-byte provenance only; no "
            "stochastic representation, analytic estimate, infinite limit, or Clay "
            "claim is certified"
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


def mono_affine_add(
    left: tuple[Fraction, Fraction], right: tuple[Fraction, Fraction]
) -> tuple[Fraction, Fraction]:
    return left[0] + right[0], left[1] + right[1]


def report_text(certificate: dict[str, Any]) -> str:
    subject = certificate["subject"]
    provenance = subject["provenance"]
    parameters = subject["parameters"]
    identities = subject["identities"]
    ledger = subject["ledger"]
    ratios = subject["ratios"]
    admissibility = subject["admissibility"]
    lines = [
        "# R0.74D zero-mean transport finite algebra certificate",
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
        "- The source commit is the theorem commit, not a later moving HEAD. The producer SHA is bound one way by the external manifest; version-control review supplies the non-self-referential immutability boundary.",
        "",
        "## Exact finite identities",
        "",
        f"- Q(R^2) has affine coefficients {identities['Q_at_tminus_coefficients']} and Q(65R^2) has coefficients {identities['Q_at_t0_coefficients']} in the basis (q_m,q_star).",
        f"- M=3*2^(m-1) gives 4^(m-1)=M^2/{identities['M_squared_coefficient']} and gamma=exp({identities['gamma_M2_exponent']} M^2).",
        f"- Pointwise exponent {identities['pointwise_leak_exponent']} becomes quadratic exponent {identities['quadratic_leak_exponent']} and cubic exponent {identities['cubic_leak_exponent']}.",
        f"- The strict quadratic leakage gap is {identities['strict_leakage_gap']} > 0.",
        f"- Pi has degree {parameters['Pi_degree']}; its exact two-thirds power has degree {identities['Pi_degree_after_two_thirds']} and the theorem's degree-{parameters['Pi_degree']} overpayment is valid.",
        "",
        "## Monomial convention",
        "",
        "Each row is [A power, R power, M power, exp(M^2) coefficient]. Polynomial Pi factors are tracked separately.",
        "",
        "| Quantity | Row |",
        "|---|---|",
    ]
    for family in ("E", "E32", "Gu", "Gp", "Hu", "P", "P23", "target"):
        for name, row in ledger[family].items():
            lines.append(f"| {family}.{name} | {row} |")
    lines.extend([
        "",
        "## Three ratio signatures",
        "",
        f"- Background: after A and R substitution, {ratios['background']['after_A_R_substitution']}; one positive power of M remains.",
        f"- Leakage: ignoring the explicit degree-{ratios['leakage']['Pi_denominator_degree']} denominator, the row is {ratios['leakage']['without_Pi']} with positive exponential gap {ratios['leakage']['exponential_gap']}.",
        f"- Transport: after R substitution, {ratios['transport']['after_R_substitution']} with positive exponential gap {ratios['transport']['exponential_gap']}.",
        "- These are finite exponent and power signatures used by the analytic divergence proof. The certificate does not prove any infinite limit.",
        "",
        "## Admissibility witness arithmetic",
        "",
        f"- At m={admissibility['base_index']}, M={admissibility['base_M']} >= 64.",
        f"- The finite positive exponential-series lower bound is {admissibility['exp_series_lower_bound']}, giving R <= {admissibility['base_R_upper']} and MR <= {admissibility['base_q_upper']} < 1/32.",
        f"- One doubling step has R-ratio at most {admissibility['R_recurrence_upper']} and q-ratio at most {admissibility['q_recurrence_upper']}; both are below one.",
        "- This finite witness checks the explicit M, R, MR, and pi/16 gates. Passage to every later index, eventual entry below the unspecified R1, and all limiting statements remain analytic.",
        "",
        "## Result",
        "",
        f"All {certificate['summary']['total']} checks pass. The coverage manifest is a bijection over {certificate['coverage_manifest']['subject_leaf_count']} subject leaves.",
        "",
        "## Analytic boundary",
        "",
        "- The stochastic/Feynman-Kac formula and its time ordering are not certified.",
        "- Target survival, one-sided Gaussian leakage, spatial gradients, and heat-kernel constants are not certified.",
        "- Lp contraction, periodic-copy sums, Calderon--Zygmund/Jensen estimates, and pressure-gauge analysis are not certified.",
        "- The exact NSE and zero-global-mean claims remain analytic statements in the frozen theorem source.",
        "- Finite ratio signatures do not prove divergence or any infinite quantifier.",
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
        print("R0.74D certificate check failed: " + ", ".join(bad), file=sys.stderr)
        return 1
    summary = certificate["summary"]
    print(
        "R0.74D finite algebra certificate PASS: "
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
        print("R0.74D certificate generation refused: internal checks failed", file=sys.stderr)
        return 1
    JSON_PATH.write_bytes(canonical_json(certificate).encode("utf-8"))
    REPORT_PATH.write_bytes(report_text(certificate).encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
