#!/usr/bin/env python3
"""Fail-closed finite certificate for the frozen R0.75G threshold."""

from __future__ import annotations

import hashlib
import json
import os
import re
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "research/r075g_signed_flux_gain_threshold.md"
PRIMARY_AUDIT = ROOT / "research/r075g_signed_flux_gain_threshold_primary_audit.md"
REPORT_SOURCE = ROOT / "research/r075g_report-source.md"
FIXTURES = ROOT / "scripts/r075g_signed_flux_gain_threshold_fixtures.json"
EXPECTED = ROOT / "scripts/r075g_signed_flux_gain_threshold_expected.json"
OUT_JSON = Path(os.environ.get(
    "R075G_JSON",
    ROOT / "research/r075g_signed_flux_gain_threshold_certificate.json",
))
OUT_REPORT = Path(os.environ.get(
    "R075G_REPORT",
    ROOT / "research/r075g_signed_flux_gain_threshold_certificate_report.md",
))
MUTATION = os.environ.get("R075G_MUTATION", "")
SCHEMA = "r075g-signed-flux-gain-threshold-certificate-v1"

FROZEN_SOURCES = {
    "research/r075c_background_shear_packing_false_positive.md":
        "1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89",
    "research/r075d_passive_gradient_route_screen.md":
        "54bcd703aff9a55f8fff522ded2bf1c5b629ee2497bd4f2255a6224e4bb747f6",
    "research/r075e_horizontal_cross_mode_flux_reduction.md":
        "99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049",
    "research/r075f_modal_phase_integration_identity.md":
        "f7a72ebfe0471e18c0d5d44bd3123491d7cd47a79293d1860c5d023c13acf440",
    "research/r075g_report-source.md":
        "2722d2801945a2ee074b0a9c4a973f592849ae012ddd4c264b7fea5ad76e9896",
    "research/r075g_signed_flux_gain_threshold.md":
        "f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41",
    "research/r075g_signed_flux_gain_threshold_primary_audit.md":
        "4717b365e5a4dc1bff169db51708a8a74fe51e6dd414a9a68a448813d95541aa",
}
FIXTURES_SHA256 = "6bcf72a52763b04f98c21109fabbd570aa552cfe472280cff7ff4a0738eb0c9a"
EXPECTED_SHA256 = "03b3475a3f8e82cb986e63ef52af6fdb899ac200b70024661c379542356b6ab0"

NEGATIVE_MUTATIONS = (
    "source_drift", "audit_drift", "report_source_drift",
    "dependency_drift", "dependency_table_missing",
    "fixture_drift", "expected_drift", "tag", "reference", "display", "control",
    "g9_normalization_r", "g9_time_r", "g9_volume_l", "g9_volume_r",
    "g9_b_cubic_r", "g9_cube_root", "rho_value", "c_gamma_value",
    "alpha_formula", "alpha_fraction", "equality_non_strict",
    "equality_polynomial", "alpha_third_sign", "alpha_third_denominator",
    "alpha_quarter_sign", "alpha_quarter_denominator", "beta_factor",
    "beta_fraction", "amplitude_flux_degree", "amplitude_atom_degree",
    "amplitude_two_thirds", "amplitude_ratio", "zero_convention",
    "transport_pde_sign", "transport_energy_sign", "transport_endpoint_sign",
    "transport_flux_factor", "transport_cutoff_frequency",
    "passage_width_exponent", "passage_speed_exponent",
    "passage_occupation_product", "passage_window_exponent",
    "passage_winding", "conditional_proved", "threshold_necessary",
    "equality_closes", "quarter_counterexample", "amplitude_gain",
    "interaction_proved", "diffusion_benchmark_proved", "e24_closed",
    "full_clock", "fixed_deletion", "suitable_weak", "regularity", "clay",
)

Q = Fraction


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(value: str | int) -> Q:
    return Q(value)


def qtext(value: Q) -> str:
    return str(value)


def vector_add(*vectors: dict[str, Q]) -> dict[str, Q]:
    keys = sorted(set().union(*(vector.keys() for vector in vectors)))
    return {key: sum(vector.get(key, Q(0)) for vector in vectors) for key in keys}


def vector_scale(scale: Q, vector: dict[str, Q]) -> dict[str, Q]:
    return {key: scale * value for key, value in vector.items()}


def vector_json(vector: dict[str, Q]) -> dict[str, str]:
    return {key: qtext(value) for key, value in vector.items()}


def record(ok: bool, **details: Any) -> dict[str, Any]:
    return {"pass": bool(ok), **details}


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R075G_MUTATION: {MUTATION}")

    text = MAIN.read_text(encoding="utf-8")
    flat_text = re.sub(r"\s+", " ", text)
    scan_text = text + ("\x01" if MUTATION == "control" else "")
    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))

    source_expectations = dict(FROZEN_SOURCES)
    if MUTATION == "source_drift":
        source_expectations[
            "research/r075g_signed_flux_gain_threshold.md"
        ] = "0" * 64
    if MUTATION == "audit_drift":
        source_expectations[
            "research/r075g_signed_flux_gain_threshold_primary_audit.md"
        ] = "0" * 64
    if MUTATION == "report_source_drift":
        source_expectations["research/r075g_report-source.md"] = "0" * 64
    if MUTATION == "dependency_drift":
        source_expectations[
            "research/r075c_background_shear_packing_false_positive.md"
        ] = "0" * 64
    source_rows = {
        path: {
            "expectedSha256": digest,
            "observedSha256": sha256(ROOT / path),
        }
        for path, digest in sorted(source_expectations.items())
    }
    fixture_expected_hash = "0" * 64 if MUTATION == "fixture_drift" else FIXTURES_SHA256
    expected_expected_hash = "0" * 64 if MUTATION == "expected_drift" else EXPECTED_SHA256
    fixture_hash = sha256(FIXTURES)
    expected_hash = sha256(EXPECTED)

    # G.9--G.10 exponent multiplication.
    factors = []
    for item in fixtures["g9Factors"]:
        row = {key: q(item[key]) for key in ("L", "R", "omega")}
        factors.append((item["name"], row))
    replacements = {
        "g9_normalization_r": ("paymentNormalization", "R", Q(-1)),
        "g9_time_r": ("timeLength", "R", Q(3)),
        "g9_volume_l": ("collarVolume", "L", Q(1)),
        "g9_volume_r": ("collarVolume", "R", Q(2)),
        "g9_b_cubic_r": ("bCubed", "R", Q(-5)),
    }
    if MUTATION in replacements:
        target, key, value = replacements[MUTATION]
        factors = [
            (name, {**row, key: value} if name == target else row)
            for name, row in factors
        ]
    g9_product = vector_add(*(row for _, row in factors))
    cube_scale = Q(1, 2) if MUTATION == "g9_cube_root" else Q(1, 3)
    g9_cube_root = vector_scale(cube_scale, g9_product)
    g9_observed = {
        "product": vector_json(g9_product),
        "cubeRoot": vector_json(g9_cube_root),
    }

    # G.2--G.4 and G.12--G.14 exact threshold arithmetic.
    constants = fixtures["constants"]
    rho = q(constants["rho"]) + (Q(1, 10000) if MUTATION == "rho_value" else 0)
    c_gamma = q(constants["cGamma"]) + (
        Q(1, 3969) if MUTATION == "c_gamma_value" else 0
    )
    threshold_denominator = 2 * rho if MUTATION == "alpha_formula" else 3 * rho
    alpha_star = Q(1) - c_gamma / threshold_denominator
    if MUTATION == "alpha_fraction":
        alpha_star += Q(1, 107163)

    def rate(alpha: Q, sign: int = -1, gamma_denominator: int = 12) -> Q:
        return (Q(1) - alpha) * rho / 4 + sign * c_gamma / gamma_denominator

    equality_rate = rate(alpha_star)
    equality_strict = MUTATION != "equality_non_strict"
    equality_polynomial = (
        Q(0) if MUTATION == "equality_polynomial" else Q(2, 3)
    )
    alpha_third = q(constants["testAlphas"][0])
    alpha_quarter = q(constants["testAlphas"][1])
    third_sign = 1 if MUTATION == "alpha_third_sign" else -1
    third_denominator = 6 if MUTATION == "alpha_third_denominator" else 12
    quarter_sign = 1 if MUTATION == "alpha_quarter_sign" else -1
    quarter_denominator = 6 if MUTATION == "alpha_quarter_denominator" else 12
    third_rate = rate(alpha_third, third_sign, third_denominator)
    quarter_rate = rate(alpha_quarter, quarter_sign, quarter_denominator)
    beta_factor = Q(2) if MUTATION == "beta_factor" else Q(3)
    beta_star = beta_factor * alpha_star
    if MUTATION == "beta_fraction":
        beta_star += Q(1, 35721)
    threshold_observed = {
        "alphaStar": qtext(alpha_star),
        "alphaEqualityRate": qtext(equality_rate),
        "alphaEqualityPolynomialPower": qtext(equality_polynomial),
        "alphaOneThirdRate": qtext(third_rate),
        "alphaOneQuarterRate": qtext(quarter_rate),
        "betaStar": qtext(beta_star),
        "betaOverAlpha": qtext(beta_factor),
    }

    # G.16--G.17: a perfect-cube rational amplitude family.
    amplitude = fixtures["amplitudeCase"]
    base_flux = q(amplitude["baseFlux"])
    base_pb = q(amplitude["basePB"])
    base_pf = q(amplitude["basePF"])
    pb_cube_root = Q(3)
    pf_cube_root = Q(2)
    amplitude_rows: dict[str, dict[str, str]] = {}
    for raw_a in amplitude["positiveAmplitudes"]:
        a = q(raw_a)
        flux_degree = 1 if MUTATION == "amplitude_flux_degree" else 2
        atom_degree = 2 if MUTATION == "amplitude_atom_degree" else 3
        two_thirds_degree = 3 if MUTATION == "amplitude_two_thirds" else 2
        flux = base_flux * a ** flux_degree
        p_af = base_pf * a ** atom_degree
        p_af_two_thirds = pf_cube_root ** 2 * a ** two_thirds_degree
        ratio = flux / (pb_cube_root * p_af_two_thirds)
        if MUTATION == "amplitude_ratio" and raw_a == "3":
            ratio += 1
        amplitude_rows[raw_a] = {
            "flux": qtext(flux),
            "pAF": qtext(p_af),
            "pAFTwoThirds": qtext(p_af_two_thirds),
            "correlationRatio": qtext(ratio),
        }
    zero_convention = (
        "1" if MUTATION == "zero_convention"
        else amplitude["zeroSignedNumeratorConvention"]
    )

    # G.21--G.23: H(t,x)=cos(x-t), xi=1+c*sin(2x), normalized by 2*pi.
    transport = fixtures["pureTransportCase"]
    drift = q(transport["drift"])
    cutoff_mean = q(transport["cutoffMean"])
    cutoff_amplitude = q(transport["cutoffSineAmplitude"])
    initial_phase = q(transport["initialPhaseOverPi"])
    terminal_phase = q(transport["terminalPhaseOverPi"])
    # Exact lookup for sin(2*pi*phase) at 0 and 1/4.
    sin_twice = {Q(0): Q(0), Q(1, 4): Q(1)}
    initial_sine = sin_twice[initial_phase]
    terminal_sine = sin_twice[terminal_phase]
    initial_energy = cutoff_mean / 4 + cutoff_amplitude * initial_sine / 8
    terminal_energy = cutoff_mean / 4 + cutoff_amplitude * terminal_sine / 8
    endpoint_difference = terminal_energy - initial_energy
    if MUTATION == "transport_endpoint_sign":
        endpoint_difference *= -1
    pde_direction = -1 if MUTATION == "transport_pde_sign" else 1
    energy_sign = -1 if MUTATION == "transport_energy_sign" else 1
    flux_factor = Q(1, 2) if MUTATION == "transport_flux_factor" else Q(1, 4)
    frequency_active = MUTATION != "transport_cutoff_frequency"
    integrated_flux = (
        pde_direction * energy_sign * drift * cutoff_amplitude
        * flux_factor * Q(1, 2)
        * (terminal_sine - initial_sine)
        if frequency_active else Q(0)
    )
    transport_observed = {
        "initialHalfEnergy": qtext(initial_energy),
        "terminalHalfEnergy": qtext(terminal_energy),
        "endpointDifference": qtext(endpoint_difference),
        "integratedPositiveFlux": qtext(integrated_flux),
        "identityResidual": qtext(integrated_flux - endpoint_difference),
        "cutoffMinimum": qtext(cutoff_mean - cutoff_amplitude),
        "cutoffMaximum": qtext(cutoff_mean + cutoff_amplitude),
    }

    # G.20: exact monotone lift q(t)=v*t through one interval.
    passage = fixtures["singlePassageCase"]
    r_value = q(passage["R"])
    width_factor = q(passage["intervalWidthFactor"])
    speed_factor = q(passage["speedLowerFactor"])
    window_factor = q(passage["fullWindowFactor"])
    width_exponent = 2 if MUTATION == "passage_width_exponent" else 1
    speed_exponent = -1 if MUTATION == "passage_speed_exponent" else -2
    width = width_factor * r_value ** width_exponent
    speed = speed_factor * r_value ** speed_exponent
    occupation = (
        width * speed if MUTATION == "passage_occupation_product"
        else width / speed
    )
    window_exponent = 3 if MUTATION == "passage_window_exponent" else 2
    window = window_factor * r_value ** window_exponent
    occupation_fraction = occupation / window
    passage_observed = {
        "intervalWidth": qtext(width),
        "speedLowerBound": qtext(speed),
        "occupationUpperBound": qtext(occupation),
        "rCubed": qtext(r_value ** 3),
        "occupationOverRCubed": qtext(occupation / (r_value ** 3)),
        "fullWindowLength": qtext(window),
        "occupationFraction": qtext(occupation_fraction),
        "occupationFractionOverR": qtext(occupation_fraction / r_value),
        "occupationRExponent": str(width_exponent - speed_exponent),
        "relativeFractionRExponent": str(
            width_exponent - speed_exponent - window_exponent
        ),
    }

    tags = re.findall(r"\\tag\{(G\.[^}]+)\}", text)
    if MUTATION == "tag":
        tags.append("G.1")
    references = [
        "G." + value for value in re.findall(r"\(G\.([0-9]+[a-z]?)\)", text)
    ]
    if MUTATION == "reference":
        references.append("G.99")
    display_open = sum(line.strip() == r"\[" for line in text.splitlines())
    display_close = sum(line.strip() == r"\]" for line in text.splitlines())
    if MUTATION == "display":
        display_open += 1
    expected_tags = [f"G.{index}" for index in range(1, 25)]

    dependency_paths = (
        "research/r075c_background_shear_packing_false_positive.md",
        "research/r075d_passive_gradient_route_screen.md",
        "research/r075e_horizontal_cross_mode_flux_reduction.md",
        "research/r075f_modal_phase_integration_identity.md",
    )
    dependency_table_present = all(
        any(path in line and FROZEN_SOURCES[path] in line for line in text.splitlines())
        for path in dependency_paths
    )
    if MUTATION == "dependency_table_missing":
        dependency_table_present = False

    required_tokens = (
        r"\alpha>\alpha_*:=1-\frac{c_\gamma}{3\rho}",
        r"\frac{27163}{107163}",
        r"-\frac{4279}{238140000}<0",
        r"\frac{1489}{1905120000}>0",
        r"R^{-2}\omega (R^2)(L^2R^3)(R^{-6})",
        r"\beta>\beta_*:=3\alpha_*",
        r"\frac{27163}{35721}",
        r"\mathfrak X_{\xi,R}(AF,b)=A^2\mathfrak X_{\xi,R}(F,b)",
        r"\le C R^3",
        r"\partial_tH+b(t)\partial_2H=0",
        "not a proof for the passive advection-diffusion problem",
        "None of those three outcomes is established here.",
        r"\mathbf{NOT\ CLAY}",
    )

    e_text = (ROOT / "research/r075e_horizontal_cross_mode_flux_reduction.md").read_text(
        encoding="utf-8"
    )
    f_text = (ROOT / "research/r075f_modal_phase_integration_identity.md").read_text(
        encoding="utf-8"
    )
    audit_text = PRIMARY_AUDIT.read_text(encoding="utf-8")
    boundary = {
        "G1ConditionalUnproved": MUTATION != "conditional_proved",
        "thresholdOnlyForG1Route": MUTATION != "threshold_necessary",
        "equalityDoesNotCloseUnrefined": MUTATION != "equality_closes",
        "quarterIsNotCounterexample": MUTATION != "quarter_counterexample",
        "amplitudeCannotCreateGain": MUTATION != "amplitude_gain",
        "interactionAtomUnproved": MUTATION != "interaction_proved",
        "singleUnwrappedPassageOnly": MUTATION != "passage_winding",
        "pureTransportNotDiffusiveProof": MUTATION != "diffusion_benchmark_proved",
        "E24Open": MUTATION != "e24_closed",
        "completeClockOpen": MUTATION != "full_clock",
        "fixedDeletionOpen": MUTATION != "fixed_deletion",
        "suitableWeakTransferOpen": MUTATION != "suitable_weak",
        "regularityAndSingularityOpen": MUTATION != "regularity",
        "notClay": MUTATION != "clay",
    }

    checks = {
        "allFrozenSourceBindings": record(
            all(row["expectedSha256"] == row["observedSha256"]
                for row in source_rows.values()),
            sources=source_rows,
        ),
        "fixtureAndExpectedBindings": record(
            fixture_hash == fixture_expected_hash
            and expected_hash == expected_expected_hash
            and fixtures["schema"] == "r075g-signed-flux-gain-threshold-fixtures-v1"
            and expected["schema"] == "r075g-signed-flux-gain-threshold-expected-v1"
            and fixtures["frozenSources"] == FROZEN_SOURCES,
            fixtures={"expected": fixture_expected_hash, "observed": fixture_hash},
            expected={"expected": expected_expected_hash, "observed": expected_hash},
        ),
        "primaryAuditBindingAndStatus": record(
            FROZEN_SOURCES["research/r075g_signed_flux_gain_threshold.md"]
                in audit_text
            and "Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0."
                in audit_text
            and "Equation tags G.1--G.24 are unique and consecutive." in audit_text,
        ),
        "mainDependencyTableBindings": record(dependency_table_present),
        "g9ExponentProduct": record(
            g9_observed["product"] == expected["g9"]["product"],
            factors={name: vector_json(row) for name, row in factors},
            product=g9_observed["product"],
        ),
        "g10CubeRootExponents": record(
            g9_observed["cubeRoot"] == expected["g9"]["cubeRoot"],
            cubeRoot=g9_observed["cubeRoot"],
        ),
        "alphaStarAndEqualityBoundary": record(
            threshold_observed["alphaStar"] ==
                expected["threshold"]["alphaStar"]
            and threshold_observed["alphaEqualityRate"] == "0"
            and threshold_observed["alphaEqualityPolynomialPower"] == "2/3"
            and equality_strict,
            threshold=threshold_observed,
            strictInequalityRequired=equality_strict,
        ),
        "alphaOneThirdAndQuarterMargins": record(
            third_rate == q(expected["threshold"]["alphaOneThirdRate"])
            and third_rate < 0
            and quarter_rate == q(expected["threshold"]["alphaOneQuarterRate"])
            and quarter_rate > 0,
            alphaOneThirdRate=qtext(third_rate),
            alphaOneQuarterRate=qtext(quarter_rate),
        ),
        "betaThresholdAndConversion": record(
            threshold_observed["betaStar"] == expected["threshold"]["betaStar"]
            and beta_factor == 3
            and Q(1) / beta_factor == Q(1, 3),
            betaStar=qtext(beta_star),
            betaOverAlpha=qtext(beta_factor),
        ),
        "amplitudeHomogeneityFiniteFamily": record(
            amplitude_rows == expected["amplitudeRows"]
            and base_pb == pb_cube_root ** 3
            and base_pf == pf_cube_root ** 3
            and zero_convention == "0",
            rows=amplitude_rows,
            zeroNumeratorConvention=zero_convention,
        ),
        "pureTransportPositiveSignAndEndpoint": record(
            transport_observed == expected["pureTransportNormalized"]
            and integrated_flux > 0
            and integrated_flux == endpoint_difference,
            normalizedBy="2*pi",
            observed=transport_observed,
        ),
        "singleUnwrappedPassageScaleG20": record(
            passage_observed == expected["singlePassage"],
            observed=passage_observed,
        ),
        "tagsReferencesAndDisplays": record(
            tags == expected_tags
            and len(set(tags)) == 24
            and not (set(references) - set(tags))
            and display_open == display_close == 24,
            tags=tags,
            references=sorted(set(references)),
            displays={"open": display_open, "close": display_close},
        ),
        "externalReferencesAndSentinels": record(
            r"\tag{E.22}" in e_text
            and r"\tag{F.17}" in f_text
            and r"\tag{F.18}" in f_text
            and all(re.sub(r"\s+", " ", token) in flat_text
                    for token in required_tokens),
        ),
        "claimBoundary": record(
            all(boundary.values()),
            state=boundary,
        ),
        "utf8AndControlSafety": record(
            "\ufffd" not in scan_text
            and not any(
                ord(character) < 32 and character not in "\t\n"
                for character in scan_text
            ),
        ),
    }

    verdict = "PASS" if all(item["pass"] for item in checks.values()) else "FAIL"
    payload = {
        "schema": SCHEMA,
        "verdict": verdict,
        "assertions": {
            "passed": sum(item["pass"] for item in checks.values()),
            "total": len(checks),
        },
        "mutation": MUTATION or None,
        "checks": checks,
        "g9ExponentLedger": g9_observed,
        "thresholdLedger": threshold_observed,
        "amplitudeRows": amplitude_rows,
        "pureTransportNormalized": transport_observed,
        "singlePassage": passage_observed,
        "claimBoundary": boundary,
    }
    OUT_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    failed = [name for name, item in checks.items() if not item["pass"]]
    OUT_REPORT.write_text(
        "# R0.75G finite certificate report\n\n"
        f"- Verdict: **{verdict}**\n"
        f"- Assertions: {payload['assertions']['passed']}/{payload['assertions']['total']}\n"
        f"- Main SHA-256: {sha256(MAIN)}\n"
        f"- Fixture SHA-256: {fixture_hash}\n"
        f"- Expected SHA-256: {expected_hash}\n"
        f"- Failed checks: {'none' if not failed else '; '.join(failed)}\n\n"
        "Exact exponent-vector multiplication gives G.9 and its cube root. "
        "Rational arithmetic gives alpha*=27163/107163, zero exponential "
        "rate but an L^(2/3) loss at equality, margins -4279/238140000 and "
        "1489/1905120000, and beta*=27163/35721=3*alpha*.\n\n"
        "A perfect-cube amplitude family verifies quadratic/cubic homogeneity. "
        "The pure transport example H=cos(x-t), xi=1/2+(1/4)sin(2x) has "
        "positive integrated flux 1/32 equal to its endpoint half-energy "
        "increase. A "
        "rational monotone passage realizes the O(R^3) bound and O(R) window "
        "fraction. These are finite benchmarks, not proofs of G.1, G.18, or "
        "G.24. E.24 and all larger conclusions remain OPEN. **NOT CLAY.**\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "suite": "r075g-signed-flux-gain-threshold",
        "verdict": verdict,
        "assertions": len(checks),
    }, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
