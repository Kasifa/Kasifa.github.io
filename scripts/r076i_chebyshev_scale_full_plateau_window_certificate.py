#!/usr/bin/env python3
"""Fail-closed finite certificate scaffold for R0.76I.

The producer checks the finite arithmetic and textual ledger behind the
Chebyshev-scale full-plateau window.  It does not prove Zhang's extrapolation
theorem, the imported Erdelyi/Kos inequalities, or any continuum PDE claim.

The R0.76I research/audit hashes below are sealed 64-character SHA-256
digests.  The verifier still recognizes conspicuous placeholders so that any
future unsealed rebuild can produce only ``SCAFFOLD_PASS`` rather than
``PASS``.  A malformed or mismatching locked digest fails closed.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from fractions import Fraction as Q
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STEM = "r076i_chebyshev_scale_full_plateau_window"
MAIN = ROOT / f"research/{STEM}.md"
SOURCE = ROOT / "research/r076i_report-source.md"
PRIMARY = ROOT / f"research/{STEM}_primary_audit.md"
INDEPENDENT = ROOT / f"research/{STEM}_independent_audit.md"
FIXTURES = ROOT / f"scripts/{STEM}_fixtures.json"
EXPECTED = ROOT / f"scripts/{STEM}_expected.json"
OUT_JSON = Path(os.environ.get("R076I_JSON", ROOT / f"research/{STEM}_certificate.json"))
OUT_REPORT = Path(os.environ.get("R076I_REPORT", ROOT / f"research/{STEM}_certificate_report.md"))
MUTATION = os.environ.get("R076I_MUTATION", "")
SCHEMA = "r076i-chebyshev-scale-full-plateau-window-certificate-v1"

PLACEHOLDER_RE = re.compile(r"^PENDING_R076I_[A-Z0-9_]+_SHA256$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

# Generated certificate/report/independent-audit outputs are deliberately
# excluded from this binding set to avoid a self-referential hash cycle.
FROZEN = {
    f"research/{STEM}.md": "6277cb69dfad94cae89088c6a8c007967bdde97aceee7b19954d10ec53f6efce",
    "research/r076i_report-source.md": "0ee0fbd75f9691e2ac898a57921f8a0574ba9af9ea652f85d0199856d7e3d423",
    f"research/{STEM}_primary_audit.md": "65adf8bc77f33c5d18184c612acc67246e48e7ad3c9059b85f269e92c9372dbe",
    "research/r076e_linear_modal_entropy_window.md": "1494cb7e3863ef934f87746412f2a64ef98f78deb5ce81be3cece7d5a7571ca4",
    "research/r076h_full_plateau_absorption_for_shifted_packet.md": "11490112a1893400a1099dd9f45b906ce78d7dab1ebcf549eaa7870241dc0ef4",
    f"scripts/{STEM}_fixtures.json": "f1475b2549490c3639c15a4fc103e704d0de98a518f50249b732a8e0a135d776",
    f"scripts/{STEM}_expected.json": "26485db072bf886fae88f0737546d7090f77b9b23e55c356bf8affe6aeba1da5",
}

GROUPS = {
    "bindings": [
        "main_hash", "source_hash", "primary_audit_hash",
        "r076e_dependency_hash",
        "r076h_dependency_hash", "fixture_hash", "expected_hash",
        "hash_specs_well_formed", "freeze_state_consistent",
    ],
    "inputs": [
        "fixture_schema", "expected_schema", "fixture_keys",
        "expected_keys", "fixture_utf8", "expected_utf8", "p_value",
        "rho_value", "gamma_value", "sample_values", "source_inventory",
        "dependency_inventory",
    ],
    "integrity": [
        "main_utf8", "source_utf8", "no_controls", "no_cr",
        "no_trailing", "tag_sequence", "tag_count", "display_balance",
        "display_count", "reference_closure",
    ],
    "geometry": [
        "delta_order", "e_rule", "e_value", "e_length",
        "right_endpoint", "delta_rule", "delta_value",
        "rescaled_endpoint", "endpoint_identity", "physical_gap",
        "endpoint_regime", "main_geometry_fragments",
    ],
    "zhang": [
        "afr_value", "complex_coefficients", "real_frequencies",
        "duplicates_merged", "unnormalized_norm", "branch_count",
        "amplitude_exponent", "squared_exponent", "q_squared_exponent",
        "phi_square", "scaled_prefactor", "i17_constant", "i17_range",
        "i18_bilateral", "i19_full_interval",
    ],
    "derivative": [
        "markov_coefficient", "two_to_fifth", "leading_coefficient",
        "sample_markov_leading", "frequency_square_coefficient",
        "sample_frequency_square", "observation_power", "q_seven",
        "q_three_alpha_two", "ledger_sum", "high_carrier_power",
        "i20_fragment", "i21_fragment", "i33_fragment",
    ],
    "terminal": [
        "branch_upper", "endpoint_factor", "cube_rule",
        "two_thirds_rule", "sample_cube", "sample_two_thirds",
        "i23_fragment", "i24_fragment",
    ],
    "energy": [
        "row_count", "row_names", "row_signs", "row_coefficients",
        "row_a_powers", "terminal_row", "cutoff_row", "curvature_row",
        "gradient_row", "four_line_identity", "complete_real_boundary",
    ],
    "physical": [
        "a_power", "r_power", "q_power", "physical_bound",
        "normalized_bound", "mode_window", "growing_example",
        "window_margin", "gamma_rate", "normalized_rate",
        "delta_asymptotic", "phi_asymptotic", "physical_conversion",
    ],
    "source": [
        "zhang_abs", "zhang_pdf", "erdelyi_abs", "erdelyi_journal",
        "erdelyi_pdf", "kos_journal", "zhang_metadata",
        "erdelyi_metadata", "kos_metadata", "lower_witness_boundary",
        "local_dependencies_named", "no_priority_claim",
    ],
    "boundary": [
        "conditional_literature", "preprint_boundary",
        "full_class_sharpness", "real_dyadic_sharpness_open",
        "arbitrary_packets_open", "version_m_open", "regularity_open",
        "singularity_open", "no_figure", "no_simulation", "not_clay",
        "no_clay_claim", "exact_shear_scope",
    ],
}
NEGATIVE_MUTATIONS = tuple(name for names in GROUPS.values() for name in names)


def sha256(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


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


def q(value: object) -> Q:
    return Q(str(value))


def binding_row(relative: str, expected: str) -> dict[str, object]:
    path = ROOT / relative
    observed = sha256(path)
    locked = bool(SHA256_RE.fullmatch(expected))
    placeholder = bool(PLACEHOLDER_RE.fullmatch(expected))
    valid_spec = locked or placeholder
    passed = valid_spec and (not locked or observed == expected)
    if locked:
        status = "locked_match" if passed else "locked_mismatch"
    else:
        status = "placeholder_unlocked" if placeholder else "invalid_hash_spec"
    return {
        "expectedSha256": expected,
        "observedSha256": observed or "MISSING",
        "exists": path.is_file(),
        "locked": locked,
        "placeholder": placeholder,
        "status": status,
        "pass": passed,
    }


def mutate(checks: dict[str, dict[str, bool]]) -> None:
    if not MUTATION:
        return
    if MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R076I_MUTATION: {MUTATION}")
    for group, names in GROUPS.items():
        if MUTATION in names:
            checks[group][MUTATION] = False
            return
    raise AssertionError(MUTATION)


def main() -> int:
    if len(set(NEGATIVE_MUTATIONS)) != len(NEGATIVE_MUTATIONS):
        raise SystemExit("duplicate mutation name in R0.76I Python suite")

    raw_main = MAIN.read_bytes()
    raw_source = SOURCE.read_bytes()
    raw_fixture = FIXTURES.read_bytes()
    raw_expected = EXPECTED.read_bytes()
    main_text = raw_main.decode("utf-8")
    source_text = raw_source.decode("utf-8")
    cm = compact(main_text)
    cs = compact(source_text)
    fixture = json.loads(raw_fixture)
    expected = json.loads(raw_expected)

    bindings = {
        relative: binding_row(relative, digest)
        for relative, digest in sorted(FROZEN.items())
    }
    placeholders = [
        relative for relative, row in bindings.items() if row["placeholder"]
    ]
    freeze_ready = all(row["locked"] and row["pass"] for row in bindings.values())

    frozen = fixture["frozen"]
    sample = fixture["sample"]
    zhang = fixture["zhang"]
    geometry = fixture["geometry"]
    derivative = fixture["derivative"]
    terminal = fixture["terminal"]
    energy = fixture["energyIdentity"]
    physical = fixture["physical"]
    sources = fixture["sources"]
    dependencies = fixture["dependencies"]
    boundary = fixture["boundary"]

    a = int(sample["a"])
    delta0 = q(sample["delta0"])
    delta = q(sample["delta"])
    q_modes = int(sample["q"])
    alpha = q(sample["alpha"])
    branches = 2 * q_modes
    e_a = Q(1) - delta0 / a
    e_length = 2 * e_a
    right_endpoint = Q(1) + delta / a
    delta_a = (delta + delta0) / (a - delta0)
    rescaled_endpoint = right_endpoint / e_a
    physical_gap = right_endpoint - e_a

    afr = int(zhang["AFr"])
    amplitude_sqrt2_coefficient = 3 * branches
    squared_sqrt2_coefficient = 6 * branches
    q_squared_sqrt2_coefficient = 12 * q_modes
    phi_squared = Q(q_squared_sqrt2_coefficient**2 * 2) * delta_a
    scaled_squared_prefactor = Q(18 * afr * q_modes * q_modes) / e_a

    two_to_fifth = 2**5
    markov_leading_coefficient = int(derivative["markovCoefficient"]) * two_to_fifth
    sample_markov_leading = int(derivative["markovCoefficient"]) * branches**5
    sample_frequency_square = Q(int(derivative["frequencySquareCoefficient"])) * q_modes * alpha**2
    q_seven = q_modes**7
    q_three_alpha_two = Q(q_modes**3) * alpha**2
    ledger_sum = Q(q_seven) + q_three_alpha_two
    high_carrier_intermediate = Q(3) + Q(8, 3)

    endpoint_factor = 4 * q_modes
    cubed_coefficient = endpoint_factor**3
    two_thirds_coefficient = 16 * q_modes**2

    rows = energy["rows"]
    row_names = [row["name"] for row in rows]
    row_signs = [int(row["sign"]) for row in rows]
    row_coefficients = [int(row["coefficient"]) for row in rows]
    row_a_powers = [int(row["aPower"]) for row in rows]

    mode_window = q(physical["modeWindowExponent"])
    example_window = q(physical["growingExampleExponent"])
    window_margin = mode_window - example_window
    omega_third_rate = -q(frozen["cGamma"]) / 12

    tags = [int(value) for value in re.findall(r"\\tag\{I\.(\d+)\}", main_text)]
    refs = [int(value) for value in re.findall(r"(?<![A-Za-z0-9_.])I\.(\d+)", main_text)]
    display_opens = len(re.findall(r"(?m)^\\\[$", main_text))
    display_closes = len(re.findall(r"(?m)^\\\]$", main_text))

    expected_fixture_keys = {
        "schema", "freeze", "frozen", "sample", "zhang", "geometry",
        "derivative", "terminal", "energyIdentity", "physical", "sources",
        "dependencies", "boundary",
    }
    expected_expected_keys = {
        "schema", "sample", "geometry", "zhang", "derivative", "terminal",
        "energyIdentity", "physical", "structure", "claims",
    }

    def bound(relative: str) -> bool:
        return bool(bindings[relative]["pass"])

    checks = {
        "bindings": {
            "main_hash": bound(f"research/{STEM}.md"),
            "source_hash": bound("research/r076i_report-source.md"),
            "primary_audit_hash": bound(f"research/{STEM}_primary_audit.md"),
            "r076e_dependency_hash": bound("research/r076e_linear_modal_entropy_window.md"),
            "r076h_dependency_hash": bound("research/r076h_full_plateau_absorption_for_shifted_packet.md"),
            "fixture_hash": bound(f"scripts/{STEM}_fixtures.json"),
            "expected_hash": bound(f"scripts/{STEM}_expected.json"),
            "hash_specs_well_formed": all(row["locked"] or row["placeholder"] for row in bindings.values()),
            "freeze_state_consistent": (
                bool(placeholders) and fixture["freeze"]["state"] == "PENDING_PRIMARY_AUDIT_HASH_SEAL"
            ) or (
                not placeholders and fixture["freeze"]["state"] == "HASH_SEALED"
            ),
        },
        "inputs": {
            "fixture_schema": fixture["schema"] == "r076i-chebyshev-scale-full-plateau-window-fixtures-v1",
            "expected_schema": expected["schema"] == "r076i-chebyshev-scale-full-plateau-window-expected-v1",
            "fixture_keys": set(fixture) == expected_fixture_keys,
            "expected_keys": set(expected) == expected_expected_keys,
            "fixture_utf8": clean_bytes(raw_fixture),
            "expected_utf8": clean_bytes(raw_expected),
            "p_value": q(frozen["p"]) == Q(32, 63),
            "rho_value": q(frozen["rho"]) == Q(9, 10000),
            "gamma_value": q(frozen["cGamma"]) == Q(8, 3969),
            "sample_values": (a, delta0, delta, q_modes, alpha) == (64, Q(1, 10), Q(1, 2), 3, Q(5, 2)),
            "source_inventory": set(sources) == {"zhangAbs", "zhangPdf", "erdelyiAbs", "erdelyiJournal", "erdelyiPdf", "kosJournal"},
            "dependency_inventory": dependencies == {
                "research/r076e_linear_modal_entropy_window.md": FROZEN["research/r076e_linear_modal_entropy_window.md"],
                "research/r076h_full_plateau_absorption_for_shifted_packet.md": FROZEN["research/r076h_full_plateau_absorption_for_shifted_packet.md"],
            },
        },
        "integrity": {
            "main_utf8": clean_bytes(raw_main),
            "source_utf8": clean_bytes(raw_source),
            "no_controls": all(clean_bytes(value) for value in (raw_main, raw_source, raw_fixture, raw_expected)),
            "no_cr": all(b"\r" not in value for value in (raw_main, raw_source, raw_fixture, raw_expected)),
            "no_trailing": all(
                not line.endswith((" ", "\t"))
                for text in (main_text, source_text)
                for line in text.splitlines()
            ),
            "tag_sequence": tags == list(range(1, 39)),
            "tag_count": len(tags) == expected["structure"]["tagCount"] == 38,
            "display_balance": display_opens == display_closes,
            "display_count": display_opens == expected["structure"]["displayCount"] == 42,
            "reference_closure": not (set(refs) - set(tags)),
        },
        "geometry": {
            "delta_order": Q(0) < delta0 < delta,
            "e_rule": geometry["eRule"] == "1-delta0/a",
            "e_value": e_a == q(expected["geometry"]["eA"]),
            "e_length": e_length == q(expected["geometry"]["eALength"]),
            "right_endpoint": right_endpoint == q(expected["geometry"]["rightEndpoint"]),
            "delta_rule": geometry["deltaRule"] == "(delta+delta0)/(a-delta0)",
            "delta_value": delta_a == q(expected["geometry"]["deltaA"]),
            "rescaled_endpoint": rescaled_endpoint == q(expected["geometry"]["rescaledRightEndpoint"]),
            "endpoint_identity": rescaled_endpoint == Q(1) + delta_a,
            "physical_gap": physical_gap == q(expected["geometry"]["physicalExteriorWidthOneSide"]) == e_a * delta_a,
            "endpoint_regime": a >= delta + 2 * delta0 and delta_a <= 1 and expected["geometry"]["endpointRegime"],
            "main_geometry_fragments": all(fragment in cm for fragment in (
                r"e_a:=1-\frac{\delta_0}{a}",
                r"E_a=[-e_a,e_a]",
                r"I_a=\left[-1-\frac\deltaa,1+\frac\deltaa\right]",
                r"\Delta_a:=\frac{\delta+\delta_0}{a-\delta_0}",
            )),
        },
        "zhang": {
            "afr_value": afr == expected["zhang"]["AFr"] == 8191,
            "complex_coefficients": zhang["coefficientField"] == "complex" and r"c_r\in\mathbbC" in cm,
            "real_frequencies": zhang["frequencyField"] == "real" and r"\mu_r\in\mathbbR" in cm,
            "duplicates_merged": zhang["duplicateFrequencyRule"] == "merge-before-counting" and "duplicatebranchesareremoved" in cm,
            "unnormalized_norm": zhang["normRule"] == "unnormalized-L2-minus1-plus1" and r"\|g\|_{L^2[-1,1]}" in cm,
            "branch_count": branches == expected["sample"]["complexBranches"] == 6 and "N=2q" in cm,
            "amplitude_exponent": amplitude_sqrt2_coefficient == expected["zhang"]["amplitudeExponentSqrt2Coefficient"] == 18,
            "squared_exponent": squared_sqrt2_coefficient == expected["zhang"]["squaredExponentSqrt2Coefficient"] == 36,
            "q_squared_exponent": q_squared_sqrt2_coefficient == expected["zhang"]["qSquaredExponentSqrt2Coefficient"] == 36,
            "phi_square": phi_squared == q(expected["zhang"]["phiSquared"]),
            "scaled_prefactor": scaled_squared_prefactor == q(expected["zhang"]["scaledSquaredPrefactor"]),
            "i17_constant": r"\sqrt{\frac{9A_{\rmfr}}2}\,N" in cm and r"A_{\rmfr}\le8191" in cm,
            "i17_range": "0<=d<=1" in main_text and r"e^{3\sqrt2N\sqrtd}" in cm,
            "i18_bilateral": r"\frac{18A_{\rmfr}}{e_a}q^2" in cm and r"e^{12\sqrt2q\sqrt{\Delta_a}}" in cm and "reflectionontheleftexterior" in cm,
            "i19_full_interval": r"\|G(s)\|_{L^\infty(I_a)}^2" in cm and r"\Phi_a:=12\sqrt2q\sqrt{\Delta_a}" in cm,
        },
        "derivative": {
            "markov_coefficient": int(derivative["markovCoefficient"]) == 108,
            "two_to_fifth": two_to_fifth == expected["derivative"]["twoToFifth"] == 32,
            "leading_coefficient": markov_leading_coefficient == expected["derivative"]["markovLeadingCoefficient"] == 3456,
            "sample_markov_leading": sample_markov_leading == expected["derivative"]["sampleMarkovLeading"] == 839808,
            "frequency_square_coefficient": int(derivative["frequencySquareCoefficient"]) == 8,
            "sample_frequency_square": sample_frequency_square == q(expected["derivative"]["sampleFrequencySquareUpper"]) == 150,
            "observation_power": int(derivative["observationQPower"]) == 2,
            "q_seven": q_seven == expected["derivative"]["qSeven"] == 2187,
            "q_three_alpha_two": q_three_alpha_two == q(expected["derivative"]["qThreeAlphaTwo"]),
            "ledger_sum": ledger_sum == q(expected["derivative"]["ledgerSum"]),
            "high_carrier_power": high_carrier_intermediate == q(expected["derivative"]["highCarrierIntermediatePower"]) < q(expected["derivative"]["highCarrierDominatingPower"]),
            "i20_fragment": r"108N^5+\sum_{r=1}^N\mu_r^2" in cm,
            "i21_fragment": r"q^7+q^3\alpha^2" in cm and r"\sum_{j=1}^q\bigl(\kappa_j^2+(-\kappa_j)^2\bigr)\le8q\alpha^2" in cm,
            "i33_fragment": r"q^3[q\log(q+1)]^{4/3}" in cm and r"\leCq^7H^{2/3}" in cm,
        },
        "terminal": {
            "branch_upper": terminal["branchUpperRule"] == "2q" and r"N_z\le2q" in cm,
            "endpoint_factor": endpoint_factor == expected["terminal"]["endpointFactor"] == 12,
            "cube_rule": terminal["cubedRule"] == "64q3" and 4**3 == 64,
            "two_thirds_rule": terminal["twoThirdsRule"] == "16q2" and 16**3 == 64**2,
            "sample_cube": cubed_coefficient == expected["terminal"]["cubedCoefficient"] == 1728,
            "sample_two_thirds": two_thirds_coefficient == expected["terminal"]["twoThirdsCoefficient"] == 144,
            "i23_fragment": r"|G(4,z)|\le2N_z\left(\int_3^4|G(s,z)|^2ds\right)^{1/2}" in cm,
            "i24_fragment": r"h(4)\le64q^3\int_3^4h(s)ds\le64q^3H" in cm and r"h(4)^{2/3}\le16q^2H^{2/3}" in cm,
        },
        "energy": {
            "row_count": len(rows) == int(energy["rowCount"]) == 4,
            "row_names": row_names == expected["energyIdentity"]["rowNames"],
            "row_signs": row_signs == expected["energyIdentity"]["signs"],
            "row_coefficients": row_coefficients == expected["energyIdentity"]["coefficients"],
            "row_a_powers": row_a_powers == expected["energyIdentity"]["aPowers"],
            "terminal_row": r"=\zeta(4)\mathcalE(4)" in cm,
            "cutoff_row": r"-\int_0^4\zeta'\mathcalE\,ds" in cm,
            "curvature_row": r"-a^{-2}\int_0^4\zeta\int\Xi_a''G^2" in cm,
            "gradient_row": r"+2a^{-2}\int_0^4\zeta\int\Xi_a|G_z|^2" in cm,
            "four_line_identity": all(name in row_names for name in ("terminal", "cutoff", "curvature", "gradient")) and "I.28--I.34" in main_text,
            "complete_real_boundary": "completerealsquare" in cm and "densityprojection" in cm and "standalonecarrierintegrationbyparts" in cm,
        },
        "physical": {
            "a_power": q(physical["aPower"]) == q(expected["physical"]["aPower"]) == Q(2, 3),
            "r_power": q(physical["rPower"]) == q(expected["physical"]["rPower"]) == -Q(1, 3),
            "q_power": int(physical["polynomialQPower"]) == expected["physical"]["qPower"] == 7,
            "physical_bound": r"a^{2/3}R^{-1/3}q^7" in cm,
            "normalized_bound": r"a^{2/3}q^7\omega^{1/3}" in cm,
            "mode_window": mode_window == q(expected["physical"]["modeWindowExponent"]) == Q(5, 2) and r"q(L)=o(L^{5/2})" in cm,
            "growing_example": example_window == q(expected["physical"]["growingExampleExponent"]) == Q(12, 5),
            "window_margin": window_margin == q(expected["physical"]["windowMarginExponent"]) == Q(1, 10),
            "gamma_rate": omega_third_rate == q(frozen["omegaThirdLogRate"]) == -Q(2, 11907),
            "normalized_rate": q(physical["normalizedLogRate"]) == q(expected["physical"]["normalizedLogRate"]) == -Q(2, 11907) and r"=-\frac2{11907}" in cm,
            "delta_asymptotic": r"\Delta_a=\frac{\delta+\delta_0}{pL-\delta_0}=O(L^{-1})" in cm,
            "phi_asymptotic": r"\frac{q(L)\sqrt{\Delta_a}}{L^2}=O\!\left(\frac{q(L)}{L^{5/2}}\right)" in cm,
            "physical_conversion": r"\mathcalT_{\boldsymboln,R}=\frac{a^2R^3}{2}v\int_0^4\zeta\intW_aG^2" in cm,
        },
        "source": {
            "zhang_abs": sources["zhangAbs"] == "https://arxiv.org/abs/2607.10501v1"
                and "https://arxiv.org/abs/2607.10501" in source_text
                and "arXiv:2607.10501v1" in source_text,
            "zhang_pdf": sources["zhangPdf"] == "https://arxiv.org/pdf/2607.10501v1"
                and "https://arxiv.org/pdf/2607.10501" in source_text
                and "arXiv:2607.10501v1" in source_text,
            "erdelyi_abs": sources["erdelyiAbs"] in source_text,
            "erdelyi_journal": sources["erdelyiJournal"] in source_text,
            "erdelyi_pdf": sources["erdelyiPdf"] in source_text,
            "kos_journal": sources["kosJournal"] in source_text,
            "zhang_metadata": all(fragment in source_text for fragment in ("Ruizhe Zhang", "arXiv:2607.10501v1", "2026-07-11", "34 pages")),
            "erdelyi_metadata": all(fragment in source_text for fragment in ("Theorem 2.20", "108 n^5", "equation (1.2)")),
            "kos_metadata": "Two Turán type inequalities" in source_text and "10.1007/s10474-007-6176-5" in source_text,
            "lower_witness_boundary": all(fragment in source_text for fragment in ("confluent sequence", "complex sums", "larger `T_k` class", "**OPEN**")),
            "local_dependencies_named": "R0.76E" in main_text and "R0.76H" in main_text,
            "no_priority_claim": "not evidence of novelty or priority" in source_text and "no priority claim is made" in source_text,
        },
        "boundary": {
            "conditional_literature": boundary["conditionalLiterature"] and expected["claims"]["conditionalLiterature"] and "**CONDITIONAL-LITERATURE**" in main_text,
            "preprint_boundary": not boundary["zhangPeerReviewed"] and expected["claims"]["preprintBoundary"] and "UNREFEREED PREPRINT" in source_text,
            "full_class_sharpness": boundary["fullClassSharpnessOnly"] and "full class `T_N`" in main_text,
            "real_dyadic_sharpness_open": not boundary["realDyadicSharpness"] and expected["claims"]["realDyadicSharpnessOpen"] and "matching lower bound within I.2" in main_text,
            "arbitrary_packets_open": not boundary["arbitraryPacketGeneralization"] and expected["claims"]["arbitraryPacketsOpen"] and "arbitrary nonlinear packets" in main_text,
            "version_m_open": not boundary["versionMExtraction"] and expected["claims"]["versionMOpen"] and "complete Version-M extraction" in main_text,
            "regularity_open": not boundary["regularityClaimed"] and expected["claims"]["regularityOpen"] and "regularity" in main_text,
            "singularity_open": not boundary["singularityClaimed"] and expected["claims"]["singularityOpen"] and "singularity" in main_text,
            "no_figure": not boundary["formalFigureRequired"] and "No simulation or formal scientific figure is claimed" in main_text,
            "no_simulation": not boundary["simulationClaimed"],
            "not_clay": not boundary["clayClaimed"] and expected["claims"]["notClay"] and "**NOT CLAY.**" in main_text,
            "no_clay_claim": "Nonovelty,priority,orClayimplicationisclaimed" in cm,
            "exact_shear_scope": "exact real constant shears in one dyadic band" in main_text and r"u=(0,B,F(t,x_2))" in cm,
        },
    }

    if set(checks) != set(GROUPS):
        raise SystemExit("group inventory mismatch")
    if any(list(checks[group]) != names for group, names in GROUPS.items()):
        raise SystemExit("assertion inventory mismatch")
    mutate(checks)
    failures = [
        f"{group}.{name}"
        for group, rows_in_group in checks.items()
        for name, passed in rows_in_group.items()
        if not passed
    ]
    assertions = sum(len(rows_in_group) for rows_in_group in checks.values())

    exact = {
        "sample": {
            "a": a, "delta0": str(delta0), "delta": str(delta),
            "q": q_modes, "alpha": str(alpha), "complexBranches": branches,
        },
        "geometry": {
            "eA": str(e_a), "eALength": str(e_length),
            "rightEndpoint": str(right_endpoint),
            "rescaledRightEndpoint": str(rescaled_endpoint),
            "deltaA": str(delta_a), "physicalExteriorWidthOneSide": str(physical_gap),
        },
        "zhang": {
            "AFr": afr,
            "amplitudeExponentSqrt2Coefficient": amplitude_sqrt2_coefficient,
            "squaredExponentSqrt2Coefficient": squared_sqrt2_coefficient,
            "qSquaredExponentSqrt2Coefficient": q_squared_sqrt2_coefficient,
            "phiSquared": str(phi_squared),
            "scaledSquaredPrefactor": str(scaled_squared_prefactor),
        },
        "derivative": {
            "markovLeadingCoefficient": markov_leading_coefficient,
            "sampleMarkovLeading": sample_markov_leading,
            "sampleFrequencySquareUpper": str(sample_frequency_square),
            "qSeven": q_seven, "qThreeAlphaTwo": str(q_three_alpha_two),
            "ledgerSum": str(ledger_sum),
            "highCarrierIntermediatePower": str(high_carrier_intermediate),
        },
        "terminal": {
            "endpointFactor": endpoint_factor,
            "cubedCoefficient": cubed_coefficient,
            "twoThirdsCoefficient": two_thirds_coefficient,
        },
        "energyIdentity": {
            "rowNames": row_names, "signs": row_signs,
            "coefficients": row_coefficients, "aPowers": row_a_powers,
        },
        "physical": {
            "aPower": str(q(physical["aPower"])),
            "rPower": str(q(physical["rPower"])),
            "qPower": int(physical["polynomialQPower"]),
            "modeWindowExponent": str(mode_window),
            "growingExampleExponent": str(example_window),
            "windowMarginExponent": str(window_margin),
            "normalizedLogRate": str(omega_third_rate),
        },
        "structure": {
            "firstTag": tags[0] if tags else None,
            "lastTag": tags[-1] if tags else None,
            "tagCount": len(tags), "displayCount": display_opens,
        },
    }

    verdict = "FAIL" if failures else ("PASS" if freeze_ready else "SCAFFOLD_PASS")
    result = {
        "schema": SCHEMA,
        "verdict": verdict,
        "freezeReady": freeze_ready,
        "hashSealState": "SEALED" if freeze_ready else "PENDING",
        "placeholders": placeholders,
        "assertionsPassed": assertions - len(failures),
        "assertionsTotal": assertions,
        "failures": failures,
        "groups": {
            group: {
                "passed": sum(bool(value) for value in rows_in_group.values()),
                "total": len(rows_in_group),
            }
            for group, rows_in_group in checks.items()
        },
        "bindings": bindings,
        "exact": exact,
        "negativeMutations": list(NEGATIVE_MUTATIONS),
        "scope": {
            "finiteLedgerOnly": True,
            "importedTheoremsProved": False,
            "continuumProofCertified": False,
            "conditionalLiterature": True,
            "realDyadicSharpness": False,
            "clay": False,
        },
    }
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = [
        "# R0.76I finite certificate report",
        "",
        f"- Verdict: **{verdict}**",
        f"- Freeze-ready hash seal: **{'yes' if freeze_ready else 'no'}**",
        f"- Assertions: {result['assertionsPassed']}/{assertions}",
        f"- Named negative mutations: {len(NEGATIVE_MUTATIONS)}",
        f"- Pending hash placeholders: {len(placeholders)}",
        f"- Exact sample: e_a={e_a}, Delta_a={delta_a}, N={branches}",
        f"- Squared Chebyshev exponent: 12 sqrt(2) q sqrt(Delta_a); Phi_a^2={phi_squared}",
        f"- Exact normalized logarithmic rate: {omega_third_rate}",
        f"- Failures: {'none' if not failures else failures}",
        "",
        "SCAFFOLD_PASS validates the infrastructure but is not a frozen research",
        "certificate.  PASS is impossible until every hash placeholder is sealed.",
        "The finite checks do not prove the imported literature. **NOT CLAY.**",
        "",
    ]
    OUT_REPORT.write_text("\n".join(report), encoding="utf-8")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
