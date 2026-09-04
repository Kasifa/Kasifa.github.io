#!/usr/bin/env python3
"""Fail-closed finite certificate for R0.76H."""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
from fractions import Fraction as Q
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STEM = "r076h_full_plateau_absorption_for_shifted_packet"
MAIN = ROOT / f"research/{STEM}.md"
PRIMARY = ROOT / f"research/{STEM}_primary_audit.md"
SOURCE = ROOT / "research/r076h_report-source.md"
FIXTURES = ROOT / f"scripts/{STEM}_fixtures.json"
EXPECTED = ROOT / f"scripts/{STEM}_expected.json"
OUT_JSON = Path(os.environ.get("R076H_JSON", ROOT / f"research/{STEM}_certificate.json"))
OUT_REPORT = Path(os.environ.get("R076H_REPORT", ROOT / f"research/{STEM}_certificate_report.md"))
MUTATION = os.environ.get("R076H_MUTATION", "")
SCHEMA = "r076h-full-plateau-absorption-for-shifted-packet-certificate-v1"

FROZEN = {
    f"research/{STEM}.md": "11490112a1893400a1099dd9f45b906ce78d7dab1ebcf549eaa7870241dc0ef4",
    f"research/{STEM}_primary_audit.md": "91e1f31f3adf19a9f352a8cd6defc8988971e51f0905e4a634f949223992c58d",
    "research/r076h_report-source.md": "3e706ae12caace1118f941f92c85bc0a1a11ed4a6e158acf7258918a67616d87",
    "research/r076g_complete_clock_central_fibre_flux_lower_bound.md": "20f32790b53f2b0f5cb39b7071bd2cda96ddb4e15f75211e1682f4ba37dd0bb2",
    "research/r075p_buffered_collar_entrance_concentration.md": "8df38e54514d82102cd3e568e89ec1db93913da3ceac52f1371d77fd79c1b7a6",
    "research/r075r_outer_cap_spectral_concentration_obstruction.md": "e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3",
    "research/r076e_linear_modal_entropy_window.md": "1494cb7e3863ef934f87746412f2a64ef98f78deb5ce81be3cece7d5a7571ca4",
    f"scripts/{STEM}_fixtures.json": "035ff9b04f61c11744668c51e6fd8ef1e35da93de85fab2bd9b971acca79747d",
    f"scripts/{STEM}_expected.json": "f80cc1d8b6673a6f18069d6756f605de821ac661561d11295a40c468532e083b",
}

GROUPS = {
    "bindings": [
        "main_hash", "primary_hash", "source_hash", "packet_dependency_hash",
        "plateau_dependency_hash", "subcap_dependency_hash",
        "uniform_dependency_hash", "fixture_hash", "expected_hash",
    ],
    "inputs": [
        "fixture_schema", "expected_schema", "fixture_keys", "expected_keys",
        "fixture_utf8", "expected_utf8", "p_value", "rho_value",
        "gamma_value", "m_denominator", "beta_value", "rate_inputs",
    ],
    "integrity": [
        "main_utf8", "primary_utf8", "source_utf8", "no_controls", "no_cr",
        "no_trailing", "tag_sequence", "display_balance", "reference_closure",
        "no_discouraged_prose", "no_bare_left", "holder_spelling",
    ],
    "clock_packet": [
        "absolute_start", "absolute_terminal_start", "absolute_end",
        "clock_length", "reset_start", "reset_terminal_start", "reset_end",
        "sample_a", "sample_m", "mode_count", "mode_list", "strict_modes",
        "dyadic_equality", "packet_rules", "exact_shear",
    ],
    "geometry": [
        "sample_geometry", "subcap_order", "distance_rule", "distance_value",
        "strip_endpoints", "strip_width", "terminal_endpoints",
        "terminal_widths", "area_rule", "area_interior", "area_samples",
        "area_upper", "mass_jacobian", "strip_mass_coefficient",
        "terminal_mass_coefficient",
    ],
    "moment": [
        "variance_rule", "coefficient_rule", "degree", "coefficient_count",
        "coefficients", "coefficients_nonnegative", "sample_value",
        "sample_derivative", "global_upper", "relative_comparison",
        "tail_bases", "tail_rate_negative", "derivative_bound",
        "log_comparison", "moment_not_finite_proof",
    ],
    "adjacent": [
        "compact_w_range", "comparison_exponent", "cubed_exponent",
        "two_thirds_exponent", "sup_inf_direction", "strip_factor",
        "cap_l1", "favourable_sign", "adverse_reduces", "time_holder",
        "physical_upper",
    ],
    "terminal": [
        "s0", "w_star", "w0", "k0_definition", "box_order",
        "mass_box_scale", "flux_box_scale", "negative_ratio",
        "signed_positive", "mass_two_sided", "flux_two_sided",
    ],
    "rates": [
        "a_square_density", "m_density", "q_density", "raw_rate",
        "r_third_rate", "omega_third_rate", "normalization_cancel",
        "normalized_rate",
    ],
    "source": [
        "local_dependencies", "heat_sources", "small_time_sources",
        "remez_sources", "no_external_import", "no_priority_claim",
    ],
    "boundary": [
        "explicit_only", "full_plateau", "complete_signed_flux",
        "exact_raw", "exact_normalized", "arbitrary_open",
        "uniform_open", "version_m_open", "regularity_open",
        "no_figure", "no_simulation", "not_clay",
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


def q(value: object) -> Q:
    return Q(str(value))


def mutate(checks: dict[str, dict[str, bool]]) -> None:
    if not MUTATION:
        return
    if MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R076H_MUTATION: {MUTATION}")
    for group, names in GROUPS.items():
        if MUTATION in names:
            checks[group][MUTATION] = False
            return
    raise AssertionError(MUTATION)


def main() -> int:
    if len(set(NEGATIVE_MUTATIONS)) != len(NEGATIVE_MUTATIONS):
        raise SystemExit("duplicate mutation name in R0.76H suite")

    raws = {
        "main": MAIN.read_bytes(),
        "primary": PRIMARY.read_bytes(),
        "source": SOURCE.read_bytes(),
        "fixtures": FIXTURES.read_bytes(),
        "expected": EXPECTED.read_bytes(),
    }
    texts = {
        key: value.decode("utf-8")
        for key, value in raws.items()
        if key in ("main", "primary", "source")
    }
    compact = {key: flat(value) for key, value in texts.items()}
    fixture = json.loads(raws["fixtures"])
    expected = json.loads(raws["expected"])
    bindings = {
        path: {"expectedSha256": digest, "observedSha256": sha256(ROOT / path)}
        for path, digest in sorted(FROZEN.items())
    }

    frozen = fixture["frozen"]
    sample = fixture["sample"]
    packet = fixture["packet"]
    clock = fixture["clock"]
    geometry = fixture["geometry"]
    moment_fixture = fixture["moment"]
    bounds = fixture["bounds"]
    boundary = fixture["boundary"]

    a = int(sample["a"])
    m = int(sample["m"])
    delta0 = q(sample["delta0"])
    delta = q(sample["delta"])
    beta = q(frozen["beta"])
    s_star = q(sample["sStar"])
    h = q(sample["h"])
    q_modes = 2 * m + 1
    modes = list(range(2 * m, 4 * m + 1))
    D = delta + 3 * delta0
    s0 = Q(4) - Q(1, a)
    w_star = Q(3, 2) + 4 * beta
    w0 = w_star - (4 * delta0 + beta) / a
    strip_left = Q(1) - 3 * delta0 / a
    strip_right = Q(1) - 2 * delta0 / a
    terminal_left = Q(1) - 4 * delta0 / a
    terminal_right = Q(1) - 3 * delta0 / a
    time_width = Q(1, a)
    cap_width = 2 * h / a

    def area_over_pi(z: Q) -> Q:
        outer = max(Q(0), (a + delta0) ** 2 - a * a * z * z)
        inner = max(Q(0), (a - delta0) ** 2 - a * a * z * z)
        return outer - inner

    interior_area = 4 * a * delta0
    inner_sample = Q(1) - 2 * delta0 / a
    outer_edge = Q(1) + delta0 / a
    strip_mass_coefficient = 4 * delta0 * a * a
    terminal_mass_coefficient = a * interior_area * time_width * (delta0 / a)

    coeffs = [
        Q(math.factorial(2 * m), math.factorial(2 * m - 2 * ell) * math.factorial(ell))
        for ell in range(m + 1)
    ]
    moment_s = q(sample["momentS"])
    moment_w = q(sample["momentW"])
    t = moment_s / (a * a)
    moment_value = sum(
        coeffs[ell] * t**ell * moment_w ** (2 * m - 2 * ell)
        for ell in range(m + 1)
    )
    moment_derivative = sum(
        coeffs[ell] * t**ell * (2 * m - 2 * ell)
        * moment_w ** (2 * m - 2 * ell - 1)
        for ell in range(m)
    )
    comparison_exponent = Q(10, 7) * D * m / a
    cubed_exponent = Q(30, 7) * D * m / a
    two_thirds_exponent = Q(20, 7) * D * m / a
    tail_rate_upper = Q(1, 512) * Q(2, 7) - Q(49, 800)

    p = q(frozen["p"])
    p_square = p * p
    a_square_density = p_square
    m_density = p_square / int(frozen["mDenominator"])
    q_density = 2 * m_density
    r_rate = q(frozen["rLogRate"])
    omega_rate = q(frozen["omegaLogRate"])
    raw_rate = -r_rate / 3
    r_third_rate = r_rate / 3
    omega_third_rate = omega_rate / 3
    normalized_rate = raw_rate + r_third_rate + omega_third_rate

    tags = [int(value) for value in re.findall(r"\\tag\{H\.(\d+)\}", texts["main"])]
    refs = [int(value) for value in re.findall(r"(?<![A-Za-z0-9_.])H\.(\d+)", texts["main"])]
    opens = len(re.findall(r"(?m)^\\\[$", texts["main"]))
    closes = len(re.findall(r"(?m)^\\\]$", texts["main"]))
    discouraged = ("我们", "攻关", "主攻", "研究纪律", "三重审计", "杀死错误想法")

    def bound(path: str) -> bool:
        return bindings[path]["expectedSha256"] == bindings[path]["observedSha256"]

    expected_fixture_keys = {
        "schema", "frozen", "sample", "packet", "clock", "geometry",
        "moment", "bounds", "boundary",
    }
    expected_expected_keys = {"schema", "sample", "geometry", "moment", "rates", "claims"}

    checks = {
        "bindings": {
            "main_hash": bound(f"research/{STEM}.md"),
            "primary_hash": bound(f"research/{STEM}_primary_audit.md"),
            "source_hash": bound("research/r076h_report-source.md"),
            "packet_dependency_hash": bound("research/r076g_complete_clock_central_fibre_flux_lower_bound.md"),
            "plateau_dependency_hash": bound("research/r075p_buffered_collar_entrance_concentration.md"),
            "subcap_dependency_hash": bound("research/r075r_outer_cap_spectral_concentration_obstruction.md"),
            "uniform_dependency_hash": bound("research/r076e_linear_modal_entropy_window.md"),
            "fixture_hash": bound(f"scripts/{STEM}_fixtures.json"),
            "expected_hash": bound(f"scripts/{STEM}_expected.json"),
        },
        "inputs": {
            "fixture_schema": fixture["schema"] == "r076h-full-plateau-absorption-for-shifted-packet-fixtures-v1",
            "expected_schema": expected["schema"] == "r076h-full-plateau-absorption-for-shifted-packet-expected-v1",
            "fixture_keys": set(fixture) == expected_fixture_keys
                and set(frozen) == {"p", "rho", "cGamma", "mDenominator", "beta", "rLogRate", "omegaLogRate"}
                and set(sample) == {"a", "m", "delta0", "delta", "sStar", "h", "momentS", "momentW"}
                and set(packet) == {"modeCountRule", "firstModeRule", "lastModeRule", "carrierRule", "spacingRule", "samplePositiveModes"}
                and set(clock) == {"absoluteStartOverR2", "absoluteTerminalStartOverR2", "absoluteEndOverR2", "resetStart", "resetTerminalStart", "resetEnd"}
                and set(geometry) == {"distanceRule", "plateauStripWidthRule", "positiveCapWidthRule", "areaInteriorRule", "scaledMassJacobianRule"}
                and set(moment_fixture) == {"varianceRule", "coefficientRule", "comparisonSlopeRule", "sampleDegree"}
                and set(bounds) == {"wLower", "wUpper", "tailMomentBase", "tailReferenceBase", "tailExponent", "negativeBase"}
                and set(boundary) == {"explicitShiftedBinomialOnly", "fullPhysicalPlateauMass", "completeSignedFlux", "exactRawRate", "exactNormalizedRate", "arbitraryPacketGeneralization", "uniformExpCqImproved", "versionMExtraction", "formalFigureRequired", "simulationClaimed", "clayClaimed"},
            "expected_keys": set(expected) == expected_expected_keys
                and set(expected["sample"]) == {"a", "m", "q", "firstMode", "lastMode", "twiceFirstMode", "strictlyIncreasing", "dyadicBand"}
                and set(expected["geometry"]) == {"D", "s0", "wStar", "w0", "plateauStripLeft", "plateauStripRight", "plateauStripWidth", "terminalPlateauLeft", "terminalPlateauRight", "terminalTimeWidth", "positiveCapWidth", "interiorAreaOverPi", "areaAtZeroOverPi", "areaAtInnerSampleOverPi", "areaAtOneOverPi", "areaAtOuterEdgeOverPi", "stripMassCoefficientOverPiR5", "terminalMassCoefficientOverPiR5"}
                and set(expected["moment"]) == {"coefficients", "sampleValue", "sampleDerivative", "comparisonExponent", "cubedExponent", "twoThirdsExponent"}
                and set(expected["rates"]) == {"aSquareDensity", "mDensity", "qDensity", "rawRate", "rThirdRate", "omegaThirdRate", "normalizedRate"}
                and set(expected["claims"]) == {"candidateKilled", "signedFluxEventuallyPositive", "fullPlateauUsed", "arbitraryPacketsOpen", "uniformExpCqOpen", "versionMOpen", "notClay"},
            "fixture_utf8": clean_bytes(raws["fixtures"]),
            "expected_utf8": clean_bytes(raws["expected"]),
            "p_value": p == Q(32, 63),
            "rho_value": q(frozen["rho"]) == Q(9, 10000),
            "gamma_value": q(frozen["cGamma"]) == Q(8, 3969),
            "m_denominator": int(frozen["mDenominator"]) == 1024,
            "beta_value": beta == Q(1, 100) and r"\beta=\frac1{100}" in compact["main"],
            "rate_inputs": r_rate == -q(frozen["rho"]) / 4 and omega_rate == -q(frozen["cGamma"]) / 4,
        },
        "integrity": {
            "main_utf8": clean_bytes(raws["main"]),
            "primary_utf8": clean_bytes(raws["primary"]),
            "source_utf8": clean_bytes(raws["source"]),
            "no_controls": all(clean_bytes(value) for value in raws.values()),
            "no_cr": all(b"\r" not in value for value in raws.values()),
            "no_trailing": all(
                not line.endswith((" ", "\t"))
                for value in texts.values()
                for line in value.splitlines()
            ),
            "tag_sequence": tags == list(range(1, 40)),
            "display_balance": opens == closes == 39,
            "reference_closure": not (set(refs) - set(tags)),
            "no_discouraged_prose": not any(
                word in value for word in discouraged for value in texts.values()
            ),
            "no_bare_left": re.search(r"(?<!\\)left[\[(]", texts["main"]) is None,
            "holder_spelling": "Holder" not in texts["main"] and "Hölder" in texts["main"],
        },
        "clock_packet": {
            "absolute_start": clock["absoluteStartOverR2"] == 61,
            "absolute_terminal_start": clock["absoluteTerminalStartOverR2"] == 64,
            "absolute_end": clock["absoluteEndOverR2"] == 65,
            "clock_length": clock["absoluteEndOverR2"] - clock["absoluteStartOverR2"] == 4,
            "reset_start": clock["resetStart"] == 0,
            "reset_terminal_start": clock["resetTerminalStart"] == 3,
            "reset_end": clock["resetEnd"] == 4,
            "sample_a": a == expected["sample"]["a"] == 64,
            "sample_m": m == expected["sample"]["m"] == a * a // 1024 == 4,
            "mode_count": q_modes == expected["sample"]["q"] == 9,
            "mode_list": modes == packet["samplePositiveModes"],
            "strict_modes": modes == sorted(set(modes)) and expected["sample"]["strictlyIncreasing"],
            "dyadic_equality": modes[0] == expected["sample"]["firstMode"] == 8
                and modes[-1] == expected["sample"]["lastMode"] == 16
                and modes[-1] == 2 * modes[0] == expected["sample"]["twiceFirstMode"]
                and expected["sample"]["dyadicBand"],
            "packet_rules": packet == {
                "modeCountRule": "2m+1", "firstModeRule": "2m",
                "lastModeRule": "4m", "carrierRule": "3m",
                "spacingRule": "aR", "samplePositiveModes": modes,
            } and all(fragment in compact["main"] for fragment in (
                "q=2m+1", r"\cos(3my)", r"\varepsilon=aR",
                r"B=-\frac{\beta a}{R}",
            )),
            "exact_shear": "smooth unforced shear" in compact["main"]
                and r"u=(0,B,F_L(t,x_2))" in compact["main"],
        },
        "geometry": {
            "sample_geometry": (delta0, delta, s_star, h) == (Q(1, 10), Q(1, 2), Q(1, 4), Q(1, 40)),
            "subcap_order": delta0 < s_star - 3 * h < s_star + 3 * h < delta,
            "distance_rule": geometry["distanceRule"] == "delta+3delta0",
            "distance_value": D == q(expected["geometry"]["D"]) == Q(4, 5),
            "strip_endpoints": strip_left == q(expected["geometry"]["plateauStripLeft"])
                and strip_right == q(expected["geometry"]["plateauStripRight"]),
            "strip_width": strip_right - strip_left == q(expected["geometry"]["plateauStripWidth"])
                == delta0 / a and geometry["plateauStripWidthRule"] == "delta0/a",
            "terminal_endpoints": terminal_left == q(expected["geometry"]["terminalPlateauLeft"])
                and terminal_right == q(expected["geometry"]["terminalPlateauRight"]),
            "terminal_widths": time_width == q(expected["geometry"]["terminalTimeWidth"])
                and cap_width == q(expected["geometry"]["positiveCapWidth"])
                and geometry["positiveCapWidthRule"] == "2h/a",
            "area_rule": geometry["areaInteriorRule"] == "4a delta0"
                and r"-[(a-\delta_0)^2-a^2z^2]_+" in compact["main"],
            "area_interior": interior_area == q(expected["geometry"]["interiorAreaOverPi"]),
            "area_samples": area_over_pi(Q(0)) == q(expected["geometry"]["areaAtZeroOverPi"])
                and area_over_pi(inner_sample) == q(expected["geometry"]["areaAtInnerSampleOverPi"])
                and area_over_pi(Q(1)) == q(expected["geometry"]["areaAtOneOverPi"])
                and area_over_pi(outer_edge) == q(expected["geometry"]["areaAtOuterEdgeOverPi"]),
            "area_upper": all(area_over_pi(z) <= interior_area for z in (
                Q(0), inner_sample, Q(1), outer_edge,
            )) and r"\le4\pi a\delta_0" in compact["main"],
            "mass_jacobian": geometry["scaledMassJacobianRule"] == "aR5"
                and "dx_2=aR dz" in compact["main"] and "dt=R^2ds" in compact["main"]
                and r"M_L^{\rm plat}=aR^5" in compact["main"],
            "strip_mass_coefficient": strip_mass_coefficient
                == q(expected["geometry"]["stripMassCoefficientOverPiR5"]),
            "terminal_mass_coefficient": terminal_mass_coefficient
                == q(expected["geometry"]["terminalMassCoefficientOverPiR5"]),
        },
        "moment": {
            "variance_rule": moment_fixture["varianceRule"] == "2s/a2"
                and r"\sigma_s:=\frac{\sqrt{2s}}a" in compact["main"],
            "coefficient_rule": moment_fixture["coefficientRule"] == "(2m)!/((2m-2l)!l!)"
                and r"\frac{(2m)!}{(2m-2\ell)!\,\ell!}" in compact["main"],
            "degree": moment_fixture["sampleDegree"] == 2 * m == 8,
            "coefficient_count": len(coeffs) == m + 1,
            "coefficients": [int(value) for value in coeffs] == expected["moment"]["coefficients"],
            "coefficients_nonnegative": all(value >= 0 for value in coeffs),
            "sample_value": moment_value == q(expected["moment"]["sampleValue"]),
            "sample_derivative": moment_derivative == q(expected["moment"]["sampleDerivative"]),
            "global_upper": r"|G_L(s,z)|\le A\varepsilon^{2m}\mathcal M_{m,s}" in compact["main"],
            "relative_comparison": r"=o(1)\mathcal M_{m,s}(w)" in compact["main"]
                and r"\frac12A\varepsilon^{2m}\mathcal M_{m,s}(w)" in compact["main"],
            "tail_bases": q(bounds["tailMomentBase"]) == Q(9, 5)
                and q(bounds["tailReferenceBase"]) == Q(7, 5)
                and q(bounds["tailExponent"]) == -Q(49, 800),
            "tail_rate_negative": tail_rate_upper < 0
                and "2m log(9/7)-49a^2/800+O(1)" in compact["main"],
            "derivative_bound": moment_fixture["comparisonSlopeRule"] == "10m/7"
                and r"\le\frac{2m}{w}\le\frac{10m}{7}" in compact["main"],
            "log_comparison": r"\exp\!\left(\frac{10m}{7}|w-w'|\right)" in compact["main"],
            "moment_not_finite_proof": "cannot replace the limiting moment argument" in compact["source"],
        },
        "adjacent": {
            "compact_w_range": q(bounds["wLower"]) == Q(7, 5)
                and q(bounds["wUpper"]) == Q(8, 5)
                and r"\frac75\le w(s,z_o),w(s,z_p)\le\frac85" in compact["main"],
            "comparison_exponent": comparison_exponent == q(expected["moment"]["comparisonExponent"]),
            "cubed_exponent": cubed_exponent == q(expected["moment"]["cubedExponent"]),
            "two_thirds_exponent": two_thirds_exponent == q(expected["moment"]["twoThirdsExponent"]),
            "sup_inf_direction": "U_L(s)" in texts["main"] and r"\inf_{z\in J_{a,p}}G_L(s,z)" in compact["main"],
            "strip_factor": r"\frac{\delta_0}{8a}" in compact["main"]
                and r"-\frac{30D}{7}\frac ma" in compact["main"],
            "cap_l1": r"\int_{\mathcal C_{a,+}}(-W_a(z))\,dz" in compact["main"],
            "favourable_sign": "positive cap is the only favourable sign" in compact["main"],
            "adverse_reduces": "full negative cap may only reduce the signed integral" in compact["main"],
            "time_holder": r"\le4^{1/3}Q_L^{2/3}" in compact["main"],
            "physical_upper": r"a^{4/3}R^{-1/3}" in compact["main"]
                and r"\exp\!\left(C_*\frac ma\right)" in compact["main"],
        },
        "terminal": {
            "s0": s0 == q(expected["geometry"]["s0"]) == Q(255, 64),
            "w_star": w_star == q(expected["geometry"]["wStar"]) == Q(77, 50),
            "w0": w0 == q(expected["geometry"]["w0"]) == Q(1963, 1280),
            "k0_definition": r"K_0:=\mathcal M_{m,s_0}(w_0)" in compact["main"],
            "box_order": terminal_left < terminal_right < strip_right < 1
                and s0 < 4 and cap_width > 0,
            "mass_box_scale": terminal_mass_coefficient == 4 * delta0 * delta0
                and r"cR^5A^3\varepsilon^{6m}K_0^3" in compact["main"],
            "flux_box_scale": a * time_width * cap_width == 2 * h / a
                and r"c\beta a^{-1}A^2\varepsilon^{4m}K_0^2" in compact["main"],
            "negative_ratio": q(bounds["negativeBase"]) == Q(2, 3)
                and r"\left(\frac{2}{3w_0}\right)^{4m}=o(1)" in compact["main"],
            "signed_positive": "eventual strict positivity" in compact["primary"]
                and expected["claims"]["signedFluxEventuallyPositive"],
            "mass_two_sided": r"\le M_L^{\rm plat}" in compact["main"]
                and r"\le Ca^2e^{Ca}R^5A^3\varepsilon^{6m}K_0^3" in compact["main"],
            "flux_two_sided": r"\le\mathcal S_L" in compact["main"]
                and r"\le C\beta e^{Ca}A^2\varepsilon^{4m}K_0^2" in compact["main"],
        },
        "rates": {
            "a_square_density": a_square_density == q(expected["rates"]["aSquareDensity"]),
            "m_density": m_density == q(expected["rates"]["mDensity"]) == Q(1, 3969),
            "q_density": q_density == q(expected["rates"]["qDensity"]) == Q(2, 3969),
            "raw_rate": raw_rate == q(expected["rates"]["rawRate"]) == Q(3, 40000),
            "r_third_rate": r_third_rate == q(expected["rates"]["rThirdRate"]) == -Q(3, 40000),
            "omega_third_rate": omega_third_rate == q(expected["rates"]["omegaThirdRate"]) == -Q(2, 11907),
            "normalization_cancel": raw_rate + r_third_rate == 0
                and r"R^{1/3}\omega^{1/3}" in compact["main"],
            "normalized_rate": normalized_rate == q(expected["rates"]["normalizedRate"])
                == -Q(2, 11907) and r"=-\frac2{11907}" in compact["main"],
        },
        "source": {
            "local_dependencies": all(digest in texts["source"] for digest in (
                FROZEN["research/r076g_complete_clock_central_fibre_flux_lower_bound.md"],
                FROZEN["research/r075p_buffered_collar_entrance_concentration.md"],
                FROZEN["research/r075r_outer_cap_spectral_concentration_obstruction.md"],
                FROZEN["research/r076e_linear_modal_entropy_window.md"],
            )),
            "heat_sources": "1711.04279" in texts["source"] and "1711.06088" in texts["source"],
            "small_time_sources": "math/0307158" in texts["source"]
                and "10.1016/j.jde.2004.05.007" in texts["source"]
                and "1806.00969" in texts["source"],
            "remez_sources": "F. L. Nazarov" in texts["source"]
                and "1809.09726" in texts["source"],
            "no_external_import": "imports no external observability, Remez, or control theorem" in compact["source"],
            "no_priority_claim": "not evidence of novelty or priority" in compact["source"],
        },
        "boundary": {
            "explicit_only": boundary["explicitShiftedBinomialOnly"]
                and expected["claims"]["candidateKilled"]
                and "kills only the explicit shifted-binomial candidate" in compact["primary"],
            "full_plateau": boundary["fullPhysicalPlateauMass"]
                and expected["claims"]["fullPlateauUsed"]
                and "full physical plateau mass" in compact["primary"],
            "complete_signed_flux": boundary["completeSignedFlux"]
                and "complete-clock signed flux" in compact["primary"],
            "exact_raw": boundary["exactRawRate"]
                and expected["claims"]["fullPlateauUsed"]
                and r"=\frac3{40000}" in compact["main"],
            "exact_normalized": boundary["exactNormalizedRate"]
                and r"=-\frac2{11907}<0" in compact["main"],
            "arbitrary_open": not boundary["arbitraryPacketGeneralization"]
                and expected["claims"]["arbitraryPacketsOpen"]
                and "arbitrary packets" in compact["main"],
            "uniform_open": not boundary["uniformExpCqImproved"]
                and expected["claims"]["uniformExpCqOpen"]
                and "does not improve R0.76E" in compact["main"],
            "version_m_open": not boundary["versionMExtraction"]
                and expected["claims"]["versionMOpen"]
                and "complete Version-M extraction" in compact["main"],
            "regularity_open": "regularity" in compact["main"] and "singularity" in compact["main"],
            "no_figure": not boundary["formalFigureRequired"]
                and "No simulation or formal scientific figure is claimed" in compact["main"],
            "no_simulation": not boundary["simulationClaimed"],
            "not_clay": not boundary["clayClaimed"] and expected["claims"]["notClay"]
                and "**NOT CLAY.**" in texts["main"],
        },
    }

    if set(checks) != set(GROUPS):
        raise SystemExit("group inventory mismatch")
    if any(list(checks[group]) != names for group, names in GROUPS.items()):
        raise SystemExit("assertion inventory mismatch")
    mutate(checks)
    failures = [
        f"{group}.{name}"
        for group, rows in checks.items()
        for name, value in rows.items()
        if not value
    ]
    assertions = sum(len(rows) for rows in checks.values())
    exact = {
        "sample": {"a": a, "m": m, "q": q_modes, "modes": modes},
        "geometry": {
            "D": str(D), "s0": str(s0), "wStar": str(w_star), "w0": str(w0),
            "plateauStrip": [str(strip_left), str(strip_right)],
            "terminalPlateau": [str(terminal_left), str(terminal_right)],
            "interiorAreaOverPi": str(interior_area),
            "stripMassCoefficientOverPiR5": str(strip_mass_coefficient),
            "terminalMassCoefficientOverPiR5": str(terminal_mass_coefficient),
        },
        "moment": {
            "coefficients": [int(value) for value in coeffs],
            "sampleValue": str(moment_value),
            "sampleDerivative": str(moment_derivative),
            "comparisonExponent": str(comparison_exponent),
            "cubedExponent": str(cubed_exponent),
            "twoThirdsExponent": str(two_thirds_exponent),
        },
        "rates": {
            "mDensity": str(m_density), "qDensity": str(q_density),
            "rawRate": str(raw_rate), "rThirdRate": str(r_third_rate),
            "omegaThirdRate": str(omega_third_rate),
            "normalizedRate": str(normalized_rate),
        },
    }
    result = {
        "schema": SCHEMA,
        "verdict": "PASS" if not failures else "FAIL",
        "assertionsPassed": assertions - len(failures),
        "assertionsTotal": assertions,
        "failures": failures,
        "groups": {
            group: {
                "passed": sum(bool(value) for value in rows.values()),
                "total": len(rows),
            }
            for group, rows in checks.items()
        },
        "bindings": bindings,
        "exact": exact,
        "negativeMutations": list(NEGATIVE_MUTATIONS),
        "scope": {
            "continuumMomentProof": False,
            "explicitShiftedBinomialOnly": True,
            "fullPhysicalPlateau": True,
            "arbitraryPackets": False,
            "clay": False,
        },
    }
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = [
        "# R0.76H finite certificate report",
        "",
        f"- Verdict: **{result['verdict']}**",
        f"- Assertions: {result['assertionsPassed']}/{result['assertionsTotal']}",
        f"- Negative mutation inventory: {len(NEGATIVE_MUTATIONS)}",
        f"- Exact sample: a={a}, m={m}, q={q_modes}, modes {modes[0]}--{modes[-1]}",
        f"- Exact raw logarithmic rate: {raw_rate}",
        f"- Exact normalized logarithmic rate: {normalized_rate}",
        f"- Failures: {'none' if not failures else failures}",
        "",
        "The finite certificate binds the exact geometry, arithmetic, structure,",
        "dependencies, and claim boundary.  It does not prove the uniform",
        "Gaussian-moment comparison.  The theorem concerns one explicit",
        "shifted-binomial packet on the full physical plateau. **NOT CLAY.**",
        "",
    ]
    OUT_REPORT.write_text("\n".join(report), encoding="utf-8")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
