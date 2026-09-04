#!/usr/bin/env python3
"""Deterministic finite certificate for the frozen R0.76J reconstruction.

The script binds the frozen research, source, and audit files; verifies the
J.1--J.46 ledger; recomputes the exact rational constant chain; and checks
finite Laguerre and tail fixtures.  These checks do not prove Plancherel, the
continuum Volterra argument, or any imported downstream theorem.  NOT CLAY.

With no arguments the JSON certificate is written to stdout.  ``--output``
writes the same deterministic JSON to a named file.  ``--check`` makes the
expected-file comparison explicit; all checks are fail-closed in either mode.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STEM = "r076j_local_edge_extrapolation_reconstruction"
FIXTURES = ROOT / f"scripts/{STEM}_fixtures.json"
EXPECTED = ROOT / f"scripts/{STEM}_expected.json"
CERT_SCHEMA = "r076j-local-edge-extrapolation-reconstruction-certificate-v1"
FIXTURE_SCHEMA = "r076j-local-edge-extrapolation-reconstruction-fixtures-v1"
EXPECTED_SCHEMA = "r076j-local-edge-extrapolation-reconstruction-expected-v1"
CORE_COMMIT = "0b73f68e072e573d9aaaa824e137e29a49d3cd67"

# Generated certificate outputs are deliberately not part of the binding set,
# which avoids a self-referential hash cycle.
FROZEN = {
    f"research/{STEM}.md": "a3d67c8a27ef6ffb7068313732e8e8a08ba98931226df726ac4ee2140ab0f57f",
    "research/r076j_report-source.md": "371eac6e3f053d4ba51ded16f35024ba805d10c5a81c1f01879704ce583763c7",
    f"research/{STEM}_primary_audit.md": "1b2a608c6ffe16c35489b95fd384f0f47a1d4a79b22491a7825ac53382a746d5",
    "research/r076i_chebyshev_scale_full_plateau_window.md": "6277cb69dfad94cae89088c6a8c007967bdde97aceee7b19954d10ec53f6efce",
    "research/r076i_chebyshev_scale_full_plateau_window_primary_audit.md": "65adf8bc77f33c5d18184c612acc67246e48e7ad3c9059b85f269e92c9372dbe",
    f"scripts/{STEM}_fixtures.json": "f0957b65e763339d1ff8cc029a13e13231b22b44dff8796b3b21883ffb352c31",
    f"scripts/{STEM}_expected.json": "9e5ad2f9bed318cd1232319240d2e574f070eda0364f97957df9c013f35878e8",
}

GROUPS = {
    "bindings": [
        "all_frozen_bindings",
        "source_hash",
        "primary_audit_hash",
        "r076i_main_hash",
        "r076i_primary_audit_hash",
        "fixture_hash",
        "expected_hash",
        "all_hash_specs_well_formed",
        "r076i_core_commit_format",
        "r076i_core_commit_in_main",
        "r076i_core_commit_in_primary_audit",
        "j_hashes_in_primary_audit",
        "r076i_hashes_in_main",
        "r076i_hashes_in_primary_audit",
    ],
    "inputs": [
        "fixture_schema",
        "expected_schema",
        "fixture_keys",
        "expected_keys",
        "file_inventory",
        "fixture_frozen_inventory",
        "fixture_hash_values",
        "fixture_utf8",
        "expected_utf8",
        "positive_fixture_domains",
    ],
    "structure": [
        "main_utf8",
        "source_utf8",
        "primary_audit_utf8",
        "no_controls",
        "no_cr",
        "no_trailing_whitespace",
        "tag_sequence",
        "tag_unique",
        "tag_count",
        "display_balance",
        "display_count",
        "reference_closure",
    ],
    "constants": [
        "tail_loss",
        "tail_recovery",
        "alpha_coefficient",
        "cutoff_exact",
        "edge_squared_prefactor",
        "branch_multiplier",
        "exterior_squared_prefactor",
        "observation_prefactor",
        "squared_exponent",
        "amplitude_exponent",
        "post_branch_exponent",
        "edge_sample_count",
        "edge_sample_sqrt_delta",
        "edge_sample_alpha",
        "edge_sample_cutoff",
        "edge_sample_exponents_agree",
        "edge_sample_prefactors",
        "main_constant_fragments",
        "main_exponent_fragments",
    ],
    "laguerre": [
        "sample_inventory",
        "series_values_exact",
        "recurrence_values_exact",
        "recurrence_matches_series",
        "majorant_values_expected",
        "majorant_holds_all_samples",
        "laguerre_recurrence_fragment",
        "laguerre_bound_fragment",
    ],
    "tail": [
        "sample_inventory",
        "sample_values_expected",
        "sample_bound_holds",
        "sample_values_decrease",
        "seven_term_exp5_lower_bound",
        "tail_integral_fragment",
        "tail_bound_fragment",
        "tail_recovery_fragment",
    ],
    "asymptotic": [
        "mode_window",
        "sample_growth_window",
        "window_margin",
        "rate_from_gamma",
        "fixture_rate",
        "expected_values",
        "q_window_fragment",
        "rate_fragment",
        "phi_asymptotic_fragment",
    ],
    "claims": [
        "fixture_claims",
        "expected_claims",
        "proved_phrase",
        "proved_local_ledger",
        "open_phrase",
        "not_clay_phrase",
        "no_figure_phrase",
        "no_figure_files",
        "no_simulation_claim",
        "zhang_not_imported",
        "exact_shear_scope",
        "no_priority_claim",
        "primary_audit_pass",
        "source_stop_reason",
        "finite_certificate_boundary",
    ],
    "expected": [
        "full_expected_match",
    ],
}


def sha256(path: Path) -> str | None:
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean_bytes(data: bytes) -> bool:
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return not any(
        (byte < 32 and byte not in (9, 10, 13)) or byte == 127
        for byte in data
    )


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def frac(value: Any) -> Q:
    return Q(str(value))


def exact_sqrt(value: Q) -> Q:
    numerator = math.isqrt(value.numerator)
    denominator = math.isqrt(value.denominator)
    if numerator * numerator != value.numerator:
        raise ValueError(f"non-square numerator: {value}")
    if denominator * denominator != value.denominator:
        raise ValueError(f"non-square denominator: {value}")
    return Q(numerator, denominator)


def laguerre_series(m: int, y: Q) -> Q:
    """Return L_m(-y) from its defining finite series."""

    return sum(
        Q(math.comb(m, ell)) * y**ell / Q(math.factorial(ell))
        for ell in range(m + 1)
    )


def laguerre_recurrence(m: int, y: Q) -> Q:
    """Return L_m(-y) using the exact three-term recurrence."""

    if m == 0:
        return Q(1)
    previous = Q(1)
    current = Q(1) + y
    for degree in range(1, m):
        following = (
            (Q(2 * degree + 1) + y) * current - Q(degree) * previous
        ) / Q(degree + 1)
        previous, current = current, following
    return current


def decimal_bound(m: int, y: Q) -> tuple[Decimal, str]:
    with localcontext() as context:
        context.prec = 80
        radicand = Decimal(m) * Decimal(y.numerator) / Decimal(y.denominator)
        upper = (Decimal(2) * radicand.sqrt()).exp()
        return upper, format(upper, ".30E")


def decimal_tail(n_terms: int) -> tuple[Decimal, str]:
    with localcontext() as context:
        context.prec = 80
        value = Decimal(5 * n_terms) * Decimal(-5 * n_terms).exp()
        return value, format(value, ".30E")


def binding_row(relative: str, expected_hash: str) -> dict[str, Any]:
    observed_hash = sha256(ROOT / relative)
    well_formed = bool(re.fullmatch(r"[0-9a-f]{64}", expected_hash))
    passed = well_formed and observed_hash == expected_hash
    return {
        "expectedSha256": expected_hash,
        "observedSha256": observed_hash if observed_hash is not None else "MISSING",
        "exists": observed_hash is not None,
        "pass": passed,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        help="write deterministic JSON to this path instead of stdout",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate the computed ledger against the frozen expected JSON",
    )
    parser.add_argument(
        "--mutation",
        help="force one named assertion false for fail-closed QA",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    mutation = args.mutation or os.environ.get("R076J_MUTATION", "")

    fixture_raw = FIXTURES.read_bytes()
    expected_raw = EXPECTED.read_bytes()
    fixture = json.loads(fixture_raw)
    expected = json.loads(expected_raw)

    main_path = ROOT / fixture["files"]["main"]
    source_path = ROOT / fixture["files"]["source"]
    primary_path = ROOT / fixture["files"]["primaryAudit"]
    main_raw = main_path.read_bytes()
    source_raw = source_path.read_bytes()
    primary_raw = primary_path.read_bytes()
    main_text = main_raw.decode("utf-8")
    source_text = source_raw.decode("utf-8")
    primary_text = primary_raw.decode("utf-8")
    cm = compact(main_text)
    cs = compact(source_text)

    bindings = {
        relative: binding_row(relative, digest)
        for relative, digest in sorted(FROZEN.items())
    }

    tags = [int(value) for value in re.findall(r"\\tag\{J\.(\d+)\}", main_text)]
    refs = [
        int(value)
        for value in re.findall(r"(?<![A-Za-z0-9_.])J\.(\d+)", main_text)
    ]
    display_opens = len(re.findall(r"(?m)^\\\[$", main_text))
    display_closes = len(re.findall(r"(?m)^\\\]$", main_text))

    rules = fixture["rules"]
    tail_loss = frac(rules["tailLoss"])
    tail_recovery = Q(1) / (Q(1) - tail_loss)
    alpha_coefficient = frac(rules["alphaCoefficient"])
    cutoff = Q(int(rules["cutoffNumeratorCoefficient"])) / alpha_coefficient
    edge_squared_prefactor = tail_recovery * alpha_coefficient
    branch_multiplier = int(rules["branchCountMultiplier"])
    exterior_squared_prefactor = edge_squared_prefactor * branch_multiplier**2
    observation_prefactor = Q(2) * exterior_squared_prefactor
    squared_exponent = int(rules["squaredExponentSqrt2Coefficient"])
    amplitude_exponent = int(rules["amplitudeExponentSqrt2Coefficient"])
    post_branch_exponent = squared_exponent * branch_multiplier

    edge_fixture = fixture["edgeSample"]
    q_modes = int(edge_fixture["q"])
    n_terms = int(edge_fixture["N"])
    delta_a = frac(edge_fixture["deltaA"])
    sqrt_delta_a = exact_sqrt(delta_a)
    sample_alpha = alpha_coefficient * n_terms
    sample_cutoff = Q(25 * n_terms) / sample_alpha
    pre_branch_exponent = Q(squared_exponent * n_terms) * sqrt_delta_a
    post_branch_sample = Q(post_branch_exponent * q_modes) * sqrt_delta_a
    edge_prefactor_sample = edge_squared_prefactor * n_terms**2
    exterior_prefactor_sample = exterior_squared_prefactor * q_modes**2
    observation_prefactor_sample = observation_prefactor * q_modes**2

    laguerre_rows = []
    for row in fixture["laguerreSamples"]:
        m = int(row["m"])
        y = frac(row["y"])
        series_value = laguerre_series(m, y)
        recurrence_value = laguerre_recurrence(m, y)
        upper, upper_text = decimal_bound(m, y)
        with localcontext() as context:
            context.prec = 80
            exact_decimal = Decimal(series_value.numerator) / Decimal(series_value.denominator)
        laguerre_rows.append(
            {
                "m": m,
                "y": str(y),
                "exactValue": str(series_value),
                "majorantUpperDecimal": upper_text,
                "recurrenceMatchesSeries": recurrence_value == series_value,
                "majorantHolds": exact_decimal <= upper,
            }
        )

    tail_rows = []
    previous_tail = None
    tail_decreases = True
    for n_value in fixture["tailSamples"]:
        n_value = int(n_value)
        tail_value, tail_text = decimal_tail(n_value)
        if previous_tail is not None:
            tail_decreases = tail_decreases and tail_value < previous_tail
        previous_tail = tail_value
        tail_rows.append(
            {
                "N": n_value,
                "fiveNExpMinusFiveN": tail_text,
                "lessThanOneTwentieth": tail_value < Decimal(1) / Decimal(20),
            }
        )

    mode_window = frac(rules["modeWindowExponent"])
    sample_growth = frac(rules["sampleGrowthExponent"])
    window_margin = mode_window - sample_growth
    rate_from_gamma = -frac(rules["cGamma"]) / int(rules["rateDivisor"])

    observed = {
        "schema": EXPECTED_SCHEMA,
        "structure": {
            "firstTag": tags[0] if tags else None,
            "lastTag": tags[-1] if tags else None,
            "tagCount": len(tags),
            "displayCount": display_opens,
        },
        "constants": {
            "tailRecovery": str(tail_recovery),
            "alphaCoefficient": str(alpha_coefficient),
            "cutoff": str(cutoff),
            "edgeSquaredPrefactor": str(edge_squared_prefactor),
            "exteriorSquaredPrefactor": str(exterior_squared_prefactor),
            "observationPrefactor": str(observation_prefactor),
            "squaredExponentSqrt2Coefficient": squared_exponent,
            "amplitudeExponentSqrt2Coefficient": amplitude_exponent,
            "postBranchSquaredExponentSqrt2Coefficient": post_branch_exponent,
        },
        "edgeSample": {
            "q": q_modes,
            "N": n_terms,
            "deltaA": str(delta_a),
            "sqrtDeltaA": str(sqrt_delta_a),
            "alpha": str(sample_alpha),
            "cutoff": str(sample_cutoff),
            "preBranchSquaredExponentSqrt2": str(pre_branch_exponent),
            "postBranchSquaredExponentSqrt2": str(post_branch_sample),
            "edgeSquaredPrefactorAtN": str(edge_prefactor_sample),
            "exteriorSquaredPrefactorAtQ": str(exterior_prefactor_sample),
            "observationPrefactorAtQ": str(observation_prefactor_sample),
        },
        "laguerreSamples": laguerre_rows,
        "tailSamples": tail_rows,
        "asymptotic": {
            "modeWindowExponent": str(mode_window),
            "sampleGrowthExponent": str(sample_growth),
            "windowMarginExponent": str(window_margin),
            "normalizedLogRate": str(rate_from_gamma),
        },
        "claims": dict(fixture["claims"]),
    }

    expected_fixture_keys = {
        "schema",
        "files",
        "frozen",
        "rules",
        "edgeSample",
        "laguerreSamples",
        "tailSamples",
        "claims",
    }
    expected_expected_keys = {
        "schema",
        "structure",
        "constants",
        "edgeSample",
        "laguerreSamples",
        "tailSamples",
        "asymptotic",
        "claims",
    }
    expected_files = {
        "main": f"research/{STEM}.md",
        "source": "research/r076j_report-source.md",
        "primaryAudit": f"research/{STEM}_primary_audit.md",
        "r076iMain": "research/r076i_chebyshev_scale_full_plateau_window.md",
        "r076iPrimaryAudit": "research/r076i_chebyshev_scale_full_plateau_window_primary_audit.md",
    }
    expected_frozen = {
        "mainSha256": FROZEN[f"research/{STEM}.md"],
        "sourceSha256": FROZEN["research/r076j_report-source.md"],
        "primaryAuditSha256": FROZEN[f"research/{STEM}_primary_audit.md"],
        "r076iMainSha256": FROZEN["research/r076i_chebyshev_scale_full_plateau_window.md"],
        "r076iPrimaryAuditSha256": FROZEN["research/r076i_chebyshev_scale_full_plateau_window_primary_audit.md"],
        "r076iCoreCommit": CORE_COMMIT,
    }

    def bound(relative: str) -> bool:
        return bool(bindings[relative]["pass"])

    checks = {
        "bindings": {
            "all_frozen_bindings": all(row["pass"] for row in bindings.values()),
            "source_hash": bound("research/r076j_report-source.md"),
            "primary_audit_hash": bound(f"research/{STEM}_primary_audit.md"),
            "r076i_main_hash": bound("research/r076i_chebyshev_scale_full_plateau_window.md"),
            "r076i_primary_audit_hash": bound("research/r076i_chebyshev_scale_full_plateau_window_primary_audit.md"),
            "fixture_hash": bound(f"scripts/{STEM}_fixtures.json"),
            "expected_hash": bound(f"scripts/{STEM}_expected.json"),
            "all_hash_specs_well_formed": all(
                re.fullmatch(r"[0-9a-f]{64}", digest) for digest in FROZEN.values()
            ),
            "r076i_core_commit_format": bool(re.fullmatch(r"[0-9a-f]{40}", CORE_COMMIT)),
            "r076i_core_commit_in_main": CORE_COMMIT in main_text,
            "r076i_core_commit_in_primary_audit": CORE_COMMIT in primary_text,
            "j_hashes_in_primary_audit": all(
                value in primary_text
                for value in (
                    FROZEN[f"research/{STEM}.md"],
                    FROZEN["research/r076j_report-source.md"],
                )
            ),
            "r076i_hashes_in_main": all(
                value in main_text
                for value in (
                    FROZEN["research/r076i_chebyshev_scale_full_plateau_window.md"],
                    FROZEN["research/r076i_chebyshev_scale_full_plateau_window_primary_audit.md"],
                )
            ),
            "r076i_hashes_in_primary_audit": all(
                value in primary_text
                for value in (
                    FROZEN["research/r076i_chebyshev_scale_full_plateau_window.md"],
                    FROZEN["research/r076i_chebyshev_scale_full_plateau_window_primary_audit.md"],
                )
            ),
        },
        "inputs": {
            "fixture_schema": fixture["schema"] == FIXTURE_SCHEMA,
            "expected_schema": expected["schema"] == EXPECTED_SCHEMA,
            "fixture_keys": set(fixture) == expected_fixture_keys,
            "expected_keys": set(expected) == expected_expected_keys,
            "file_inventory": fixture["files"] == expected_files,
            "fixture_frozen_inventory": set(fixture["frozen"]) == set(expected_frozen),
            "fixture_hash_values": fixture["frozen"] == expected_frozen,
            "fixture_utf8": clean_bytes(fixture_raw),
            "expected_utf8": clean_bytes(expected_raw),
            "positive_fixture_domains": (
                n_terms >= 1
                and q_modes >= 1
                and delta_a >= 0
                and all(int(row["m"]) >= 0 and frac(row["y"]) >= 0 for row in fixture["laguerreSamples"])
                and all(int(value) >= 1 for value in fixture["tailSamples"])
            ),
        },
        "structure": {
            "main_utf8": clean_bytes(main_raw),
            "source_utf8": clean_bytes(source_raw),
            "primary_audit_utf8": clean_bytes(primary_raw),
            "no_controls": all(
                clean_bytes(value)
                for value in (main_raw, source_raw, primary_raw, fixture_raw, expected_raw)
            ),
            "no_cr": all(
                b"\r" not in value
                for value in (main_raw, source_raw, primary_raw, fixture_raw, expected_raw)
            ),
            "no_trailing_whitespace": all(
                not line.endswith((" ", "\t"))
                for text in (main_text, source_text, primary_text)
                for line in text.splitlines()
            ),
            "tag_sequence": tags == list(range(1, 47)),
            "tag_unique": len(tags) == len(set(tags)) == 46,
            "tag_count": len(tags) == expected["structure"]["tagCount"] == 46,
            "display_balance": display_opens == display_closes,
            "display_count": display_opens == expected["structure"]["displayCount"] == 48,
            "reference_closure": not (set(refs) - set(tags)),
        },
        "constants": {
            "tail_loss": tail_loss == Q(1, 20),
            "tail_recovery": tail_recovery == frac(expected["constants"]["tailRecovery"]) == Q(20, 19),
            "alpha_coefficient": alpha_coefficient == frac(expected["constants"]["alphaCoefficient"]) == Q(25, 2),
            "cutoff_exact": cutoff == frac(expected["constants"]["cutoff"]) == 2,
            "edge_squared_prefactor": edge_squared_prefactor == frac(expected["constants"]["edgeSquaredPrefactor"]) == Q(250, 19),
            "branch_multiplier": branch_multiplier == 2,
            "exterior_squared_prefactor": exterior_squared_prefactor == frac(expected["constants"]["exteriorSquaredPrefactor"]) == Q(1000, 19),
            "observation_prefactor": observation_prefactor == frac(expected["constants"]["observationPrefactor"]) == Q(2000, 19),
            "squared_exponent": squared_exponent == expected["constants"]["squaredExponentSqrt2Coefficient"] == 10 and 2 * squared_exponent**2 == 16 * alpha_coefficient,
            "amplitude_exponent": amplitude_exponent == expected["constants"]["amplitudeExponentSqrt2Coefficient"] == 5 and 2 * amplitude_exponent == squared_exponent,
            "post_branch_exponent": post_branch_exponent == expected["constants"]["postBranchSquaredExponentSqrt2Coefficient"] == 20,
            "edge_sample_count": n_terms == branch_multiplier * q_modes == 14,
            "edge_sample_sqrt_delta": sqrt_delta_a**2 == delta_a == Q(9, 400),
            "edge_sample_alpha": sample_alpha == 175,
            "edge_sample_cutoff": sample_cutoff == 2,
            "edge_sample_exponents_agree": pre_branch_exponent == post_branch_sample == 21,
            "edge_sample_prefactors": (
                edge_prefactor_sample == exterior_prefactor_sample == Q(49000, 19)
                and observation_prefactor_sample == Q(98000, 19)
            ),
            "main_constant_fragments": all(
                fragment in cm
                for fragment in (
                    r"\frac{20}{19}",
                    r"\frac{250}{19}",
                    r"\frac{1000}{19e_a}",
                    r"\frac{2000}{19}",
                    "alpha=25N/2",
                    "25N/alpha=2",
                )
            ),
            "main_exponent_fragments": all(
                fragment in cm
                for fragment in (
                    r"e^{10\sqrt2N\sqrtd}",
                    r"e^{5\sqrt2N\sqrtd}",
                    r"\Phi_a^{\rmloc}:=20\sqrt2q\sqrt{\Delta_a}",
                    "N<=2q",
                )
            ),
        },
        "laguerre": {
            "sample_inventory": [
                (row["m"], row["y"]) for row in laguerre_rows
            ] == [
                (row["m"], row["y"]) for row in expected["laguerreSamples"]
            ],
            "series_values_exact": [row["exactValue"] for row in laguerre_rows] == [
                row["exactValue"] for row in expected["laguerreSamples"]
            ],
            "recurrence_values_exact": all(
                laguerre_recurrence(int(row["m"]), frac(row["y"]))
                == frac(expected_row["exactValue"])
                for row, expected_row in zip(fixture["laguerreSamples"], expected["laguerreSamples"])
            ),
            "recurrence_matches_series": all(row["recurrenceMatchesSeries"] for row in laguerre_rows),
            "majorant_values_expected": [
                row["majorantUpperDecimal"] for row in laguerre_rows
            ] == [
                row["majorantUpperDecimal"] for row in expected["laguerreSamples"]
            ],
            "majorant_holds_all_samples": all(row["majorantHolds"] for row in laguerre_rows),
            "laguerre_recurrence_fragment": all(
                fragment in cm
                for fragment in (
                    r"P_{r+1}(x):=P_r(x)+\alpha\int_0^xP_r(y)\,dy",
                    r"P_r(x)=\sum_{\ell=0}^r\binomr\ell\frac{(\alphax)^\ell}{\ell!}=L_r(-\alphax)",
                )
            ),
            "laguerre_bound_fragment": r"0\leL_m(-y)" in cm and r"\lee^{2\sqrt{my}}" in cm,
        },
        "tail": {
            "sample_inventory": [row["N"] for row in tail_rows] == [row["N"] for row in expected["tailSamples"]],
            "sample_values_expected": [
                row["fiveNExpMinusFiveN"] for row in tail_rows
            ] == [
                row["fiveNExpMinusFiveN"] for row in expected["tailSamples"]
            ],
            "sample_bound_holds": all(row["lessThanOneTwentieth"] for row in tail_rows),
            "sample_values_decrease": tail_decreases,
            "seven_term_exp5_lower_bound": sum(Q(5**k, math.factorial(k)) for k in range(7)) > 100,
            "tail_integral_fragment": r"N\int_{25N}^\inftye^{-y+4\sqrt{Ny}}\,dy" in cm,
            "tail_bound_fragment": r"=5Ne^{-5N}<\frac1{20}" in cm,
            "tail_recovery_fragment": r"\frac{19}{20}I_\alpha(F)\le\int_0^{25N/\alpha}|F(t)|^2e^{-\alphat}\,dt" in cm,
        },
        "asymptotic": {
            "mode_window": mode_window == Q(5, 2),
            "sample_growth_window": sample_growth == Q(12, 5) < mode_window,
            "window_margin": window_margin == Q(1, 10),
            "rate_from_gamma": rate_from_gamma == -Q(2, 11907),
            "fixture_rate": frac(rules["normalizedLogRate"]) == rate_from_gamma,
            "expected_values": observed["asymptotic"] == expected["asymptotic"],
            "q_window_fragment": r"q=o(L^{5/2})" in cm,
            "rate_fragment": r"=-\frac2{11907}" in cm and "-2/11907" in main_text,
            "phi_asymptotic_fragment": r"O\!\left(\frac{q(L)}{L^{5/2}}\right)" in cm,
        },
        "claims": {
            "fixture_claims": fixture["claims"] == expected["claims"],
            "expected_claims": observed["claims"] == expected["claims"],
            "proved_phrase": "**PROVED LOCALLY FROM ESTABLISHED LITERATURE**" in main_text,
            "proved_local_ledger": "**PROVED LOCALLY:**" in main_text and "**PROVED LOCALLY**" in source_text,
            "open_phrase": "**OPEN:**" in main_text and "**OPEN**" in source_text,
            "not_clay_phrase": "**NOT CLAY.**" in main_text and "**NOT CLAY.**" in source_text,
            "no_figure_phrase": "No simulation or formal figure is needed" in main_text,
            "no_figure_files": not any(
                path.suffix.lower() in {".png", ".jpg", ".jpeg", ".svg", ".pdf"}
                for path in (ROOT / "research").glob("r076j*")
            ),
            "no_simulation_claim": (
                not fixture["claims"]["simulationRequired"]
                and "No simulation or formal figure is needed" in main_text
            ),
            "zhang_not_imported": (
                not fixture["claims"]["zhangTheoremImported"]
                and "No theorem from the preprint is assumed" in source_text
                and "not an unproved theorem used by J.2" in main_text
            ),
            "exact_shear_scope": r"u=(0,B,F(t,x_2))" in cm and "exact one-band constant shear" in main_text,
            "no_priority_claim": (
                "noindependent-discoveryorpriorityclaimismade" in cm
                and "notevidenceofnoveltyorpriority" in cs
            ),
            "primary_audit_pass": "Mathematical verdict: **PASS**" in primary_text and "Mathematical blockers: **0**" in primary_text,
            "source_stop_reason": "## Search limits and stop reason" in source_text,
            "finite_certificate_boundary": "They cannot prove Plancherel" in main_text and "They cannot prove" in primary_text,
        },
        "expected": {
            "full_expected_match": observed == expected,
        },
    }

    if set(checks) != set(GROUPS):
        raise SystemExit("certificate group inventory mismatch")
    for group, names in GROUPS.items():
        if list(checks[group]) != names:
            raise SystemExit(f"assertion inventory mismatch in {group}")

    all_mutations = [
        f"{group}.{name}"
        for group, names in GROUPS.items()
        for name in names
    ]
    if mutation:
        if mutation not in all_mutations:
            raise SystemExit(f"unknown mutation: {mutation}")
        group, name = mutation.split(".", 1)
        checks[group][name] = False

    failures = [
        f"{group}.{name}"
        for group, rows in checks.items()
        for name, passed in rows.items()
        if not passed
    ]
    total = sum(len(rows) for rows in checks.values())
    passed = total - len(failures)
    verdict = "PASS" if not failures else "FAIL"
    freeze_ready = all(row["pass"] for row in bindings.values()) and verdict == "PASS"
    exact = {
        key: value
        for key, value in observed.items()
        if key not in {"schema", "claims"}
    }

    result = {
        "schema": CERT_SCHEMA,
        "verdict": verdict,
        "freezeReady": freeze_ready,
        "assertionsPassed": passed,
        "assertionsTotal": total,
        "failures": failures,
        "groups": {
            group: {
                "passed": sum(bool(value) for value in rows.values()),
                "total": len(rows),
            }
            for group, rows in checks.items()
        },
        "bindings": bindings,
        "r076iCoreCommit": CORE_COMMIT,
        "exact": exact,
        "observed": observed,
        "negativeMutations": all_mutations,
        "scope": {
            "finiteLedgerOnly": True,
            "continuumProofCertified": False,
            "importedTheoremsProved": False,
            "formalFigureRequired": False,
            "simulationRequired": False,
            "zhangTheoremImported": False,
            "clay": False,
        },
    }
    rendered = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output is None:
        sys.stdout.write(rendered)
    else:
        args.output.write_text(rendered, encoding="utf-8")

    # The expected ledger is always checked.  The flag exists for a clear QA
    # interface and deliberately does not weaken the default fail-closed mode.
    if args.check and observed != expected:
        return 1
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
