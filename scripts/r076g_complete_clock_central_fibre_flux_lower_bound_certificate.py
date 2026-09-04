#!/usr/bin/env python3
"""Fail-closed finite certificate for R0.76G."""

from __future__ import annotations

import hashlib
import json
import os
import re
from fractions import Fraction as Q
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STEM = "r076g_complete_clock_central_fibre_flux_lower_bound"
MAIN = ROOT / f"research/{STEM}.md"
PRIMARY = ROOT / f"research/{STEM}_primary_audit.md"
SOURCE = ROOT / "research/r076g_report-source.md"
FIXTURES = ROOT / f"scripts/{STEM}_fixtures.json"
EXPECTED = ROOT / f"scripts/{STEM}_expected.json"
OUT_JSON = Path(os.environ.get("R076G_JSON", ROOT / f"research/{STEM}_certificate.json"))
OUT_REPORT = Path(os.environ.get("R076G_REPORT", ROOT / f"research/{STEM}_certificate_report.md"))
MUTATION = os.environ.get("R076G_MUTATION", "")
SCHEMA = "r076g-complete-clock-central-fibre-flux-lower-bound-certificate-v1"

FROZEN = {
    f"research/{STEM}.md": "20f32790b53f2b0f5cb39b7071bd2cda96ddb4e15f75211e1682f4ba37dd0bb2",
    f"research/{STEM}_primary_audit.md": "af47153c4e1f4c5749f68c3f89d7533c5d95f3c0c6f15b0c775a9e35317c807e",
    "research/r076g_report-source.md": "3aea1d04dce4987c3883c1b93bec04e714ee17b540fb6a99546d084efa326f74",
    "research/r075b_bulk_clock_outer_padding_gate.md": "430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a",
    "research/r075r_outer_cap_spectral_concentration_obstruction.md": "e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3",
    "research/r076e_linear_modal_entropy_window.md": "1494cb7e3863ef934f87746412f2a64ef98f78deb5ce81be3cece7d5a7571ca4",
    "research/r076f_exponential_spatial_observation_lower_bound.md": "48204fcbf8fe9af3f0fdc7720844c3dd8362d8767caf73de016eda7250b70973",
    f"scripts/{STEM}_fixtures.json": "32e1dcf71a77ba0d28e3924fcb7e7aeb4d2840aa08ba2b2e352bb4d20d0464af",
    f"scripts/{STEM}_expected.json": "0a2d3d086381029941310ae502b4cf9462e025d0c75e62dd87c07334728a6ba8",
}

GROUPS = {
    "bindings": [
        "main_hash", "primary_hash", "source_hash", "clock_dependency_hash",
        "cap_dependency_hash", "upper_dependency_hash", "static_dependency_hash",
        "fixture_hash", "expected_hash",
    ],
    "inputs": [
        "fixture_schema", "expected_schema", "fixture_utf8", "expected_utf8",
        "rho_value", "beta_value", "mode_count_rule", "first_mode_rule",
        "last_mode_rule", "expected_dyadic_band", "expected_claim_complete",
        "expected_claim_rate", "expected_claim_plateau_open",
        "expected_claim_not_clay",
    ],
    "integrity": [
        "main_utf8", "primary_utf8", "source_utf8", "no_controls", "no_cr",
        "no_trailing", "tag_sequence", "display_balance", "reference_closure",
        "no_discouraged_prose", "no_bare_left", "no_undefined_delta_c",
    ],
    "clock": [
        "absolute_start", "absolute_terminal_start", "absolute_end", "clock_length",
        "reset_start", "reset_terminal_start", "reset_end", "terminal_unit_length",
        "translated_cutoff", "terminal_cutoff_one",
    ],
    "packet": [
        "sample_m", "mode_count", "mode_list", "integer_modes", "strict_order",
        "first_mode", "last_mode", "dyadic_equality", "no_zero_mode",
        "carrier_rule", "spacing_rule", "drift_nonzero", "scaled_drift",
        "real_scalar", "exact_heat", "nse_embedding",
    ],
    "rational": [
        "central_drift", "moment_allowance", "central_raw", "central_gap",
        "central_strict", "positive_base", "negative_geometry", "negative_base",
        "ratio_base", "adverse_ratio", "p_square", "mode_density",
        "four_m_density", "omega_rate", "log_lower", "net_rate",
        "net_rate_positive", "central_drift_from_beta",
        "fixture_negative_base", "fixture_ratio_base",
    ],
    "analysis": [
        "gaussian_formula", "moment_upper", "coherent_lower", "tail_bound",
        "central_spacetime", "positive_cap", "negative_cap", "signed_combination",
        "complete_flux_ratio", "physical_conversion", "central_proxy",
        "negative_support_sign", "good_bad_bridge", "log_inequality",
        "normalized_rate", "static_near_cap",
    ],
    "source": [
        "wang_source", "egidi_source", "miller_source", "laurent_source",
        "nazarov_source", "remez_source", "local_proof_boundary",
        "no_novelty_claim", "primary_pass", "math_blocker_zero",
        "release_blocker_zero",
    ],
    "boundary": [
        "complete_signed_flux", "central_only", "no_full_plateau_lower",
        "no_version_m_counterexample", "optimal_base_open", "arbitrary_open",
        "version_m_open", "regularity_open", "singularity_open", "no_figure",
        "no_simulation", "not_clay",
    ],
}
NEGATIVE_MUTATIONS = tuple(name for names in GROUPS.values() for name in names)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean_bytes(data: bytes) -> bool:
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return not any((byte < 32 and byte not in (9, 10, 13)) or byte == 127 for byte in data)


def flat(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def fragments(text: str, values: list[str]) -> bool:
    return all(value in text for value in values)


def mutate(checks: dict[str, dict[str, bool]]) -> None:
    if not MUTATION:
        return
    if MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R076G_MUTATION: {MUTATION}")
    for group, names in GROUPS.items():
        if MUTATION in names:
            checks[group][MUTATION] = False
            return
    raise AssertionError(MUTATION)


def main() -> int:
    if len(set(NEGATIVE_MUTATIONS)) != len(NEGATIVE_MUTATIONS):
        raise SystemExit("duplicate mutation name in R0.76G suite")

    raws = {
        "main": MAIN.read_bytes(),
        "primary": PRIMARY.read_bytes(),
        "source": SOURCE.read_bytes(),
        "fixtures": FIXTURES.read_bytes(),
        "expected": EXPECTED.read_bytes(),
    }
    texts = {key: value.decode("utf-8") for key, value in raws.items() if key in ("main", "primary", "source")}
    compact = {key: flat(value) for key, value in texts.items()}
    fixture = json.loads(raws["fixtures"])
    expected = json.loads(raws["expected"])
    bindings = {
        path: {"expectedSha256": digest, "observedSha256": sha256(ROOT / path)}
        for path, digest in sorted(FROZEN.items())
    }

    sample_m = int(fixture["packet"]["sampleM"])
    modes = list(range(2 * sample_m, 4 * sample_m + 1))
    count = 2 * sample_m + 1
    clock = fixture["clock"]
    central_drift = Q(fixture["bounds"]["centralDriftBase"])
    moment = Q(fixture["bounds"]["momentAllowance"])
    central_raw = central_drift + moment
    central_base = Q(fixture["bounds"]["centralBase"])
    central_gap = central_base - central_raw
    positive = Q(fixture["bounds"]["positiveBase"])
    negative_geometry = Q(1, 2) + Q(fixture["bounds"]["negativeGeometryAllowance"])
    negative = negative_geometry + moment
    ratio_base = positive / central_base
    adverse_ratio = negative / positive
    p = Q(fixture["frozen"]["p"])
    p_square = p * p
    mode_density = 2 * p_square / fixture["frozen"]["mDenominator"]
    four_m_density = 4 * p_square / fixture["frozen"]["mDenominator"]
    omega_rate = -Q(fixture["frozen"]["cGamma"]) / 12
    log_lower = Q(expected["rational"]["logLowerBound"])
    net_rate = four_m_density * log_lower + omega_rate

    tags = [int(value) for value in re.findall(r"\\tag\{G\.(\d+)\}", texts["main"])]
    refs = [int(value) for value in re.findall(r"(?<![A-Za-z0-9_.])G\.(\d+)", texts["main"])]
    opens = len(re.findall(r"(?m)^\\\[$", texts["main"]))
    closes = len(re.findall(r"(?m)^\\\]$", texts["main"]))
    discouraged = ("我们", "攻关", "主攻", "研究纪律", "三重审计", "杀死错误想法")

    def bound(name: str) -> bool:
        path = next(path for path in bindings if path.endswith(name))
        return bindings[path]["expectedSha256"] == bindings[path]["observedSha256"]

    checks = {
        "bindings": {
            "main_hash": bound(f"research/{STEM}.md"),
            "primary_hash": bound(f"research/{STEM}_primary_audit.md"),
            "source_hash": bound("research/r076g_report-source.md"),
            "clock_dependency_hash": bound("research/r075b_bulk_clock_outer_padding_gate.md"),
            "cap_dependency_hash": bound("research/r075r_outer_cap_spectral_concentration_obstruction.md"),
            "upper_dependency_hash": bound("research/r076e_linear_modal_entropy_window.md"),
            "static_dependency_hash": bound("research/r076f_exponential_spatial_observation_lower_bound.md"),
            "fixture_hash": bound(f"scripts/{STEM}_fixtures.json"),
            "expected_hash": bound(f"scripts/{STEM}_expected.json"),
        },
        "inputs": {
            "fixture_schema": fixture["schema"] == "r076g-complete-clock-central-fibre-flux-lower-bound-fixtures-v1",
            "expected_schema": expected["schema"] == "r076g-complete-clock-central-fibre-flux-lower-bound-expected-v1",
            "fixture_utf8": clean_bytes(raws["fixtures"]),
            "expected_utf8": clean_bytes(raws["expected"]),
            "rho_value": Q(fixture["frozen"]["rho"]) == Q(9, 10000) and "`rho=9/10000`" in texts["main"],
            "beta_value": Q(fixture["frozen"]["beta"]) == Q(1, 100) and "\\beta=\\frac1{100}" in compact["main"],
            "mode_count_rule": fixture["packet"]["modeCountRule"] == "2m+1" and "q=2m+1" in compact["main"],
            "first_mode_rule": fixture["packet"]["firstModeRule"] == "2m" and modes[0] == 2 * sample_m,
            "last_mode_rule": fixture["packet"]["lastModeRule"] == "4m" and modes[-1] == 4 * sample_m,
            "expected_dyadic_band": expected["sample"]["dyadicBand"] is True and modes[-1] <= 2 * modes[0],
            "expected_claim_complete": expected["claims"]["exponentialCompleteCentralRow"] is True,
            "expected_claim_rate": expected["claims"]["positiveNormalizedCentralRate"] is True,
            "expected_claim_plateau_open": expected["claims"]["physicalPlateauSharpnessOpen"] is True,
            "expected_claim_not_clay": expected["claims"]["notClay"] is True,
        },
        "integrity": {
            "main_utf8": clean_bytes(raws["main"]),
            "primary_utf8": clean_bytes(raws["primary"]),
            "source_utf8": clean_bytes(raws["source"]),
            "no_controls": all(clean_bytes(value) for value in raws.values()),
            "no_cr": all(b"\r" not in value for value in raws.values()),
            "no_trailing": all(not line.endswith((" ", "\t")) for text in texts.values() for line in text.splitlines()),
            "tag_sequence": tags == list(range(1, 41)),
            "display_balance": opens == closes == 40,
            "reference_closure": not (set(refs) - set(tags)),
            "no_discouraged_prose": not any(word in text for word in discouraged for text in texts.values()),
            "no_bare_left": re.search(r"(?<!\\)left[\[(]", texts["main"]) is None,
            "no_undefined_delta_c": "\\delta_c" not in texts["main"] and "delta_c" not in texts["primary"],
        },
        "clock": {
            "absolute_start": clock["absoluteStartOverR2"] == 61,
            "absolute_terminal_start": clock["absoluteTerminalStartOverR2"] == 64,
            "absolute_end": clock["absoluteEndOverR2"] == 65,
            "clock_length": clock["absoluteEndOverR2"] - clock["absoluteStartOverR2"] == 4,
            "reset_start": clock["resetStart"] == 0,
            "reset_terminal_start": clock["resetTerminalStart"] == 3,
            "reset_end": clock["resetEnd"] == 4,
            "terminal_unit_length": clock["resetEnd"] - clock["resetTerminalStart"] == 1,
            "translated_cutoff": "\\widetilde\\eta_R(t):=\\eta_R(s_R+t)" in compact["main"],
            "terminal_cutoff_one": "\\zeta(s)=1\\quad(3<s<4)" in compact["main"],
        },
        "packet": {
            "sample_m": sample_m == expected["sample"]["m"] == 3,
            "mode_count": count == expected["sample"]["modeCount"] == 7,
            "mode_list": modes == fixture["packet"]["samplePositiveModes"],
            "integer_modes": all(isinstance(value, int) for value in modes),
            "strict_order": modes == sorted(set(modes)) and expected["sample"]["strictlyIncreasing"],
            "first_mode": modes[0] == expected["sample"]["firstMode"] == 6,
            "last_mode": modes[-1] == expected["sample"]["lastMode"] == 12,
            "dyadic_equality": modes[-1] == 2 * modes[0] == expected["sample"]["twiceFirstMode"],
            "no_zero_mode": modes[0] > 0,
            "carrier_rule": fixture["packet"]["carrierRule"] == "3m" and "\\cos(3my)" in texts["main"],
            "spacing_rule": fixture["packet"]["spacingRule"] == "aR" and "\\varepsilon=aR" in texts["main"],
            "drift_nonzero": Q(fixture["frozen"]["beta"]) > 0 and "B=-\\frac{\\beta a}{R}" in compact["main"],
            "scaled_drift": "v=\\frac{BR}{a}=-\\beta" in compact["main"],
            "real_scalar": "real trigonometric polynomial" in compact["main"],
            "exact_heat": "(\\partial_t+B\\partial_2-\\partial_2^2)F_L=0" in compact["main"],
            "nse_embedding": "u_L(t,x)=(0,B,F_L(t,x_2))" in compact["main"],
        },
        "rational": {
            "central_drift": central_drift == Q(26, 25),
            "moment_allowance": moment == Q(1, 8),
            "central_raw": central_raw == Q(expected["rational"]["centralRaw"]),
            "central_gap": central_gap == Q(expected["rational"]["centralComparisonGap"]),
            "central_strict": central_raw < central_base,
            "positive_base": positive == Q(3, 2),
            "negative_geometry": negative_geometry == Q(13, 24),
            "negative_base": negative == Q(expected["rational"]["negativeBase"]) == Q(2, 3),
            "ratio_base": ratio_base == Q(expected["rational"]["positiveOverCentral"]) == Q(9, 7),
            "adverse_ratio": adverse_ratio == Q(expected["rational"]["negativeOverPositive"]) == Q(4, 9),
            "p_square": p_square == Q(1024, 3969),
            "mode_density": mode_density == Q(expected["rational"]["modeDensity"]) == Q(2, 3969),
            "four_m_density": four_m_density == Q(expected["rational"]["fourMDensity"]) == Q(4, 3969),
            "omega_rate": omega_rate == Q(expected["rational"]["omegaRate"]) == -Q(2, 11907),
            "log_lower": log_lower == Q(2, 9),
            "net_rate": net_rate == Q(expected["rational"]["netRateRationalLowerBound"]) == Q(2, 35721),
            "net_rate_positive": net_rate > 0,
            "central_drift_from_beta": central_drift == 1 + 4 * Q(fixture["frozen"]["beta"]),
            "fixture_negative_base": Q(fixture["bounds"]["negativeBase"]) == negative,
            "fixture_ratio_base": Q(fixture["bounds"]["ratioBase"]) == ratio_base,
        },
        "analysis": {
            "gaussian_formula": "The periodic heat-kernel representation" in texts["main"] and "\\mathbb E" in texts["main"],
            "moment_upper": "\\left(|w|+\\frac{4\\sqrt m}{a}\\right)^{2m}" in compact["main"],
            "coherent_lower": "G_L(s,z)\\ge\\frac A2\\varepsilon^{2m}w^{2m}" in compact["main"],
            "tail_bound": "e^{-49a^2/800}" in texts["main"],
            "central_spacetime": "H_L\\le4A^3\\varepsilon^{6m}\\left(\\frac76\\right)^{6m}" in compact["main"],
            "positive_cap": "\\left(\\frac32\\right)^{4m}" in texts["main"],
            "negative_cap": "\\left(\\frac23\\right)^{4m}" in texts["main"],
            "signed_combination": "Only the negative cap can contribute with the adverse sign" in compact["main"],
            "complete_flux_ratio": "\\left(\\frac97\\right)^{4m}" in texts["main"],
            "physical_conversion": "\\mathcal T_L=\\frac{a^2R^3}{2}\\mathcal S_L" in compact["main"],
            "central_proxy": "This `M_L^I` is not the full physical plateau mass" in compact["main"],
            "negative_support_sign": "\\delta/a+4\\beta<1/2" in compact["main"] and "w<0" in texts["main"],
            "good_bad_bridge": "(1-o(1))(\\mathbb E|X|^{2m}-E_{\\rm tail})-E_{\\rm tail}" in compact["main"],
            "log_inequality": "\\log(1+x)>x/(1+x)" in compact["main"] and "x=2/7" in texts["main"],
            "normalized_rate": "\\frac{4\\log(9/7)}{3969}-\\frac2{11907}>0" in compact["main"],
            "static_near_cap": "\\le C_{\\delta_0,s_*}\\frac ma" in compact["main"],
        },
        "source": {
            "wang_source": "1711.04279" in texts["source"],
            "egidi_source": "1711.06088" in texts["source"],
            "miller_source": "math/0307158" in texts["source"] and "10.1016/j.jde.2004.05.007" in texts["source"],
            "laurent_source": "1806.00969" in texts["source"] and "10.2140/apde.2021.14.355" in texts["source"],
            "nazarov_source": "F. L. Nazarov" in texts["source"] and "mathnet.ru" in texts["source"],
            "remez_source": "S. Tikhonov and P. Yuditskii" in texts["source"],
            "local_proof_boundary": "does not import a control or observability theorem" in compact["source"],
            "no_novelty_claim": "not evidence of novelty or priority" in compact["source"],
            "primary_pass": "Current verdict: **PASS**" in texts["primary"],
            "math_blocker_zero": "Mathematical blocker count: **0**" in texts["primary"],
            "release_blocker_zero": "Release blocker count: **0**" in texts["primary"],
        },
        "boundary": {
            "complete_signed_flux": fixture["boundary"]["completeSignedFlux"] and "complete signed flux" in compact["main"],
            "central_only": fixture["boundary"]["centralFibreProxy"] and "central-fibre proxy" in compact["main"],
            "no_full_plateau_lower": not fixture["boundary"]["fullPhysicalPlateauLowerBound"] and "does **not** prove an exponential lower bound" in compact["main"],
            "no_version_m_counterexample": not fixture["boundary"]["versionMCounterexample"] and "No counterexample to R0.76E, E.24, or Version-M is claimed" in compact["main"],
            "optimal_base_open": "optimal exponential base" in compact["main"],
            "arbitrary_open": "arbitrary packets" in compact["main"],
            "version_m_open": "complete Version-M extraction" in compact["main"],
            "regularity_open": "regularity" in compact["main"],
            "singularity_open": "singularity" in compact["main"],
            "no_figure": not fixture["boundary"]["formalFigureRequired"] and "No simulation or formal scientific figure is claimed" in compact["main"],
            "no_simulation": not fixture["boundary"]["simulationClaimed"],
            "not_clay": not fixture["boundary"]["clayClaimed"] and "**NOT CLAY.**" in texts["main"],
        },
    }

    mutate(checks)
    failures = [f"{group}.{name}" for group, rows in checks.items() for name, value in rows.items() if not value]
    assertions = sum(len(rows) for rows in checks.values())
    verdict = "PASS" if not failures else "FAIL"
    exact = {
        "sample": {"m": sample_m, "modeCount": count, "modes": modes},
        "rational": {
            "centralRaw": str(central_raw), "centralGap": str(central_gap),
            "ratioBase": str(ratio_base), "adverseRatio": str(adverse_ratio),
            "modeDensity": str(mode_density), "fourMDensity": str(four_m_density),
            "omegaRate": str(omega_rate), "netRateRationalLowerBound": str(net_rate),
        },
    }
    output = {
        "schema": SCHEMA,
        "verdict": verdict,
        "assertionsPassed": assertions - len(failures),
        "assertionsTotal": assertions,
        "failures": failures,
        "exact": exact,
        "sourceSha256": {
            "main": sha256(MAIN), "primaryAudit": sha256(PRIMARY),
            "sourceReport": sha256(SOURCE), "fixtures": sha256(FIXTURES),
            "expected": sha256(EXPECTED),
        },
        "bindings": bindings,
        "negativeMutations": list(NEGATIVE_MUTATIONS),
        "checks": checks,
        "boundary": {
            "finiteComputation": True, "continuumProof": False,
            "completeSignedFlux": True, "fullPhysicalPlateauLowerBound": False,
            "clay": False,
        },
    }
    OUT_JSON.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = [
        "# R0.76G finite certificate report", "",
        f"- Verdict: **{verdict}**",
        f"- Assertions: {assertions - len(failures)}/{assertions}",
        f"- Negative mutation inventory: {len(NEGATIVE_MUTATIONS)}",
        f"- Exact sample: m={sample_m}, q={count}, modes={modes}",
        f"- Exact central comparison: {central_raw} < {central_base}, gap {central_gap}",
        f"- Exact exponential base: {ratio_base}",
        f"- Exact normalized rational rate lower bound: {net_rate} > 0",
        f"- Failures: {failures if failures else 'none'}", "",
        "The finite certificate checks the exact clock, frequency, rational,",
        "source, and claim-boundary ledgers.  It is not proof of the Gaussian",
        "limiting lemma or the continuum signed-flux inequality.",
        "**NOT CLAY.**", "",
    ]
    OUT_REPORT.write_text("\n".join(report), encoding="utf-8")
    print(json.dumps({"suite": "r076g", "verdict": verdict, "assertions": assertions, "failures": failures}, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
