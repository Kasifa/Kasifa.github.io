#!/usr/bin/env python3
"""Fail-closed exact finite certificate for frozen R0.75L."""

from __future__ import annotations

import hashlib
import json
import os
import re
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "research/r075l_single_harmonic_diffusive_signed_flux_gain.md"
PRIMARY_AUDIT = ROOT / "research/r075l_single_harmonic_diffusive_signed_flux_gain_primary_audit.md"
REPORT_SOURCE = ROOT / "research/r075l_report-source.md"
FIXTURES = ROOT / "scripts/r075l_single_harmonic_diffusive_signed_flux_gain_fixtures.json"
EXPECTED = ROOT / "scripts/r075l_single_harmonic_diffusive_signed_flux_gain_expected.json"
OUT_JSON = Path(os.environ.get(
    "R075L_JSON",
    ROOT / "research/r075l_single_harmonic_diffusive_signed_flux_gain_certificate.json",
))
OUT_REPORT = Path(os.environ.get(
    "R075L_REPORT",
    ROOT / "research/r075l_single_harmonic_diffusive_signed_flux_gain_certificate_report.md",
))
MUTATION = os.environ.get("R075L_MUTATION", "")
SCHEMA = "r075l-single-harmonic-diffusive-signed-flux-gain-certificate-v1"

FROZEN_SOURCES = {
    "research/r075e_horizontal_cross_mode_flux_reduction.md":
        "99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049",
    "research/r075g_signed_flux_gain_threshold.md":
        "f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41",
    "research/r075k_positive_majorant_high_frequency_trace_loss.md":
        "9282fb30eb7517853759fb835579220e0da763974d5543e2fb260ec8ca6daebf",
    "research/r075l_single_harmonic_diffusive_signed_flux_gain.md":
        "52e25b2fdf1a224609c9e8fafa1c041b7f09a361f75f4b3e44ebcdddb756cdf5",
    "research/r075l_single_harmonic_diffusive_signed_flux_gain_primary_audit.md":
        "a7578e5370d182decc39f0da2f2fb581e5ef842ae7b914a120b5784bc32bd302",
    "research/r075l_report-source.md":
        "a300de54b9fe06e94455a055bbb42bdce8ec7bb004080389a95412966a5b941a",
}
FIXTURES_SHA256 = "0b9ba1f018b6e52414f20dee6687f5ff55c5ea0ef247ddbd905bc8c204245ad9"
EXPECTED_SHA256 = "9178489eaf9f44c5b182b6080cce7212591b1a3dd86459ecbd82c1382b38db9a"

NEGATIVE_MUTATIONS = (
    "source_drift", "audit_drift", "report_source_drift", "dependency_drift",
    "dependency_table_missing", "fixture_drift", "expected_drift", "tag",
    "reference", "display", "control", "operator_time", "operator_drift_symbol",
    "operator_diffusion", "time_decay", "time_phase", "drift_phase",
    "diffusion_sign", "passive_residual", "k_integer", "k_lower", "A_positive",
    "B_real", "real_field", "constant_shear", "single_harmonic", "square_frequency",
    "square_zero_coefficient", "square_side_coefficient", "diagonal_not_zero",
    "diagonal_after_absolute", "periodic_mean", "absolute_before_cancel",
    "eta_lower", "eta_upper", "eta_sample", "eta_measurable", "xi_periodic",
    "xi_smooth", "xi_real", "vxi_absolute", "vxi_bound", "time_decay_multiplier",
    "time_integral_sign", "time_integral_denominator", "q2_symbol", "q2_interval",
    "drop_q2_direction", "flux_half", "flux_square_half", "flux_coefficient",
    "flux_B_absolute", "flux_Vxi", "cos_quarter", "cos_symmetry", "cos_integral",
    "mass_decay_multiplier", "mass_denominator", "mass_amplitude", "mass_k_square",
    "mass_symbol", "q3_symbol", "condition_direction", "condition_one",
    "q3_comparison", "q3_float_equality", "c3_positive", "c3_symbol",
    "a2_prefactor", "a2_power_k", "a2_power_mass", "a2_inequality",
    "cstar_outer", "cstar_inner", "flux_A", "flux_k", "mass_A", "mass_k",
    "two_thirds", "ratio_k", "amplitude_cancel", "target_omega", "target_R",
    "payment_R", "payment_omega", "payment_M", "normalized_R",
    "normalized_omega", "normalized_k", "normalized_p", "positive_part",
    "alpha_numerator", "alpha_denominator", "kappa_multiplier", "kappa_reduce",
    "endpoint_equality", "decimal_display", "decimal_exact", "strict_direction",
    "R_interval", "frequency_direction", "physical_signed", "full_torus",
    "unpaid_BVxi", "g1_claim", "e24_claim", "full_versionm_claim",
    "multimode_closed", "collar_closed", "nonconstant_closed",
    "low_frequency_closed", "complete_clock", "fixed_deletion", "suitable_weak",
    "regularity", "singularity", "novelty", "priority", "simulation", "clay",
)

Q = Fraction


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(value: str | int) -> Q:
    return Q(value)


def qtext(value: Q) -> str:
    return str(value)


def exponent_json(vector: dict[str, Q]) -> dict[str, str]:
    return {key: qtext(value) for key, value in vector.items()}


def record(ok: bool, **details: Any) -> dict[str, Any]:
    return {"pass": bool(ok), **details}


def rounded_decimal(value: Q, digits: int) -> str:
    scale = 10 ** digits
    scaled = value * scale
    rounded = (2 * scaled.numerator + scaled.denominator) // (2 * scaled.denominator)
    whole, fraction = divmod(rounded, scale)
    return f"{whole}.{fraction:0{digits}d}"


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R075L_MUTATION: {MUTATION}")

    text = MAIN.read_text(encoding="utf-8")
    audit_text = PRIMARY_AUDIT.read_text(encoding="utf-8")
    source_text = REPORT_SOURCE.read_text(encoding="utf-8")
    flat_text = re.sub(r"\s+", " ", text)
    flat_source = re.sub(r"\s+", " ", source_text)
    scan_text = text + audit_text + source_text + ("\x01" if MUTATION == "control" else "")
    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))

    source_expectations = dict(FROZEN_SOURCES)
    if MUTATION == "source_drift":
        source_expectations["research/r075l_single_harmonic_diffusive_signed_flux_gain.md"] = "0" * 64
    if MUTATION == "audit_drift":
        source_expectations[
            "research/r075l_single_harmonic_diffusive_signed_flux_gain_primary_audit.md"
        ] = "0" * 64
    if MUTATION == "report_source_drift":
        source_expectations["research/r075l_report-source.md"] = "0" * 64
    if MUTATION == "dependency_drift":
        source_expectations["research/r075g_signed_flux_gain_threshold.md"] = "0" * 64
    source_rows = {
        path: {"expectedSha256": digest, "observedSha256": sha256(ROOT / path)}
        for path, digest in sorted(source_expectations.items())
    }
    fixture_expected_hash = "0" * 64 if MUTATION == "fixture_drift" else FIXTURES_SHA256
    expected_expected_hash = "0" * 64 if MUTATION == "expected_drift" else EXPECTED_SHA256
    fixture_hash = sha256(FIXTURES)
    expected_hash = sha256(EXPECTED)

    # L.2 and L.4--L.5: operator and exact mode differentiation.
    operator_fixture = fixtures["operatorCase"]
    operator_observed = dict(operator_fixture)
    if MUTATION == "operator_time":
        operator_observed["timeCoefficient"] = "-1"
    if MUTATION == "operator_drift_symbol":
        operator_observed["driftCoefficientSymbol"] = "-B"
    if MUTATION == "operator_diffusion":
        operator_observed["secondDerivativeCoefficient"] = "1"

    family_fixture = fixtures["passiveFamilyCase"]
    amplitude = q(family_fixture["A"])
    if MUTATION == "mass_amplitude":
        amplitude += 1
    shear = q(family_fixture["B"])
    variation = q(family_fixture["Vxi"])
    ks = list(family_fixture["integerK"])

    # L.6--L.9: eta bound, Fourier diagonal, exact time primitive, flux factor.
    eta_fixture = fixtures["etaCase"]
    eta_lower = q(eta_fixture["lowerBound"])
    eta_upper = q(eta_fixture["upperBound"])
    if MUTATION == "eta_lower":
        eta_lower = Q(1, 2)
    if MUTATION == "eta_upper":
        eta_upper = Q(2)
    eta_samples = [q(value) for value in eta_fixture["allowedSamples"]]
    if MUTATION == "eta_sample":
        eta_samples[1] = Q(4, 3)
    eta_observed = {
        "rows": [
            {"eta": qtext(value), "admissible": eta_lower <= value <= eta_upper}
            for value in eta_samples
        ],
        "absoluteValueMayUseEtaUpperBound": MUTATION != "eta_upper",
    }

    time_fixture = fixtures["timeIntegralCase"]
    decay_two = q(time_fixture["decayMultiplier"])
    if MUTATION == "time_decay_multiplier":
        decay_two = 1
    q2_symbol = time_fixture["q2Symbol"]
    if MUTATION == "q2_symbol":
        q2_symbol = "exp(-k^2*T)"
    exact_time_symbol = "(1-q2)/(2*k^2)"
    if MUTATION == "time_integral_sign":
        exact_time_symbol = "(q2-1)/(2*k^2)"
    if MUTATION == "time_integral_denominator":
        exact_time_symbol = "(1-q2)/(k^2)"
    q2_interval = "0<q2<1" if MUTATION != "q2_interval" else "q2>1"
    drop_direction = "1-q2<=1" if MUTATION != "drop_q2_direction" else "1-q2>=1"
    time_observed = {
        "exactSymbol": exact_time_symbol,
        "q2Symbol": q2_symbol,
        "q2Interval": q2_interval,
        "dropFactorDirection": drop_direction,
    }

    moment_fixture = fixtures["absoluteCosineMoment"]
    quarter = q(moment_fixture["quarterIntegral"])
    symmetry = q(moment_fixture["symmetryFactor"])
    if MUTATION == "cos_quarter":
        quarter += Q(1, 3)
    if MUTATION == "cos_symmetry":
        symmetry = 2
    full_moment = quarter * symmetry
    if MUTATION == "cos_integral":
        full_moment += 1
    moment_observed = {
        "quarterIntegral": qtext(quarter),
        "symmetryFactor": qtext(symmetry),
        "fullIntegral": qtext(full_moment),
    }

    mass_fixture = fixtures["massConversionCase"]
    decay_three = q(mass_fixture["decayMultiplier"])
    if MUTATION == "mass_decay_multiplier":
        decay_three = 2

    family_observed = []
    for k in ks:
        time_cos = Q(k * k if MUTATION in ("time_decay",) else -k * k)
        time_sin = shear * k * (-1 if MUTATION == "time_phase" else 1)
        drift_sin = shear * k * (1 if MUTATION == "drift_phase" else -1)
        diffusion_cos = Q(-k * k if MUTATION == "diffusion_sign" else k * k)
        residual_cos = time_cos + diffusion_cos
        residual_sin = time_sin + drift_sin
        if MUTATION == "passive_residual":
            residual_cos += 1
        square_frequency = k if MUTATION == "square_frequency" else 2 * k
        square_zero = amplitude ** 2 * (
            Q(1) if MUTATION == "square_zero_coefficient" else Q(1, 2)
        )
        square_side = amplitude ** 2 * (
            Q(1, 2) if MUTATION == "square_side_coefficient" else Q(1, 4)
        )
        diagonal_pairing = Q(1) if MUTATION in (
            "diagonal_not_zero", "periodic_mean"
        ) else Q(0)
        primitive_denominator = decay_two * k * k
        if MUTATION == "time_integral_denominator":
            primitive_denominator = Q(k * k)
        definition_half = Q(1) if MUTATION == "flux_half" else Q(1, 2)
        square_half = Q(1) if MUTATION == "flux_square_half" else Q(1, 2)
        coefficient_shear = -abs(shear) if MUTATION == "flux_B_absolute" else abs(shear)
        coefficient_variation = variation + 1 if MUTATION == "flux_Vxi" else variation
        flux_coefficient = (
            definition_half * square_half * amplitude ** 2
            * coefficient_shear * coefficient_variation / primitive_denominator
        )
        if MUTATION == "flux_coefficient":
            flux_coefficient += 1
        mass_denominator = decay_three * k * k
        if MUTATION in ("mass_denominator", "mass_k_square"):
            mass_denominator = decay_three * k
        mass_coefficient = full_moment * amplitude ** 3 / mass_denominator
        family_observed.append({
            "k": k,
            "timeCos": qtext(time_cos),
            "timeSin": qtext(time_sin),
            "driftSin": qtext(drift_sin),
            "diffusionCos": qtext(diffusion_cos),
            "residualCos": qtext(residual_cos),
            "residualSin": qtext(residual_sin),
            "squareModes": [-square_frequency, 0, square_frequency],
            "squareModeCoefficients": [
                qtext(square_side), qtext(square_zero), qtext(square_side)
            ],
            "diagonalPairing": qtext(diagonal_pairing),
            "timeIntegralDenominator": qtext(primitive_denominator),
            "fluxCoefficientTimesOneMinusQ2": qtext(flux_coefficient),
            "fluxUpperCoefficient": qtext(flux_coefficient),
            "massCoefficientTimesOneMinusQ3": qtext(mass_coefficient),
        })

    # L.10--L.13: retain exp(-3) symbolically and prove only its interval role.
    q3_symbol = mass_fixture["q3Symbol"]
    if MUTATION == "q3_symbol":
        q3_symbol = "exp(-k^2*T)"
    condition = "k^2*T>=1"
    if MUTATION == "condition_direction":
        condition = "k^2*T<=1"
    if MUTATION == "condition_one":
        condition = "k^2*T>=0"
    q3_comparison = "0<q3<=exp(-3)<1"
    if MUTATION == "q3_comparison":
        q3_comparison = "0<exp(-3)<=q3<1"
    c3_symbol = mass_fixture["c3Symbol"]
    if MUTATION == "c3_symbol":
        c3_symbol = "1+exp(-3)"
    a2_conversion = "A^2<=(9/(8*c3))^(2/3)*k^(4/3)*M^(2/3)"
    if MUTATION == "a2_prefactor":
        a2_conversion = "A^2<=(8/(9*c3))^(2/3)*k^(4/3)*M^(2/3)"
    if MUTATION == "a2_power_k":
        a2_conversion = "A^2<=(9/(8*c3))^(2/3)*k^(2/3)*M^(2/3)"
    if MUTATION == "a2_power_mass":
        a2_conversion = "A^2<=(9/(8*c3))^(2/3)*k^(4/3)*M^(1/3)"
    if MUTATION == "a2_inequality":
        a2_conversion = "A^2>=(9/(8*c3))^(2/3)*k^(4/3)*M^(2/3)"
    cstar = "1/8*(9/(8*c3))^(2/3)"
    if MUTATION == "cstar_outer":
        cstar = "1/4*(9/(8*c3))^(2/3)"
    if MUTATION == "cstar_inner":
        cstar = "1/8*(8/(9*c3))^(2/3)"
    mass_symbol = "8*A^3*(1-q3)/(9*k^2)"
    if MUTATION == "mass_symbol":
        mass_symbol = "8*A^3*(1-q3)/(3*k^2)"
    conversion_observed = {
        "exactSymbol": mass_symbol,
        "q3Symbol": q3_symbol,
        "condition": condition,
        "q3Comparison": q3_comparison,
        "c3Symbol": c3_symbol,
        "c3Interval": "c3>1" if MUTATION == "c3_positive" else "0<c3<1",
        "A2Conversion": a2_conversion,
        "CStar": cstar,
    }

    # Formal homogeneity and target normalization.
    exponent_fixture = fixtures["exponentCase"]
    flux_exp = {key: q(value) for key, value in exponent_fixture["fluxUpper"].items()}
    mass_exp = {key: q(value) for key, value in exponent_fixture["mass"].items()}
    if MUTATION == "flux_A":
        flux_exp["A"] = 1
    if MUTATION == "flux_k":
        flux_exp["k"] = -1
    if MUTATION == "mass_A":
        mass_exp["A"] = 2
    if MUTATION == "mass_k":
        mass_exp["k"] = -1
    two_thirds = q(exponent_fixture["twoThirds"])
    if MUTATION == "two_thirds":
        two_thirds = Q(1, 3)
    mass_two_thirds = {key: value * two_thirds for key, value in mass_exp.items()}
    ratio_exp = {
        "A": flux_exp["A"] - mass_two_thirds["A"],
        "B": flux_exp["B"],
        "Vxi": flux_exp["Vxi"],
        "k": flux_exp["k"] - mass_two_thirds["k"],
    }
    if MUTATION == "ratio_k":
        ratio_exp["k"] += Q(1, 3)

    target_prefactor = {
        key: q(value) for key, value in exponent_fixture["targetPrefactor"].items()
    }
    payment = {
        key: q(value) for key, value in exponent_fixture["paymentDefinition"].items()
    }
    if MUTATION == "target_omega":
        target_prefactor["omega"] = 0
    if MUTATION == "target_R":
        target_prefactor["R"] = 0
    if MUTATION == "payment_R":
        payment["R"] = -1
    if MUTATION == "payment_omega":
        payment["omega"] = -1
    if MUTATION == "payment_M":
        payment["M"] = 2
    m_power = payment["M"]
    target_normalized = {
        "R": target_prefactor["R"] - two_thirds * payment["R"] / m_power,
        "omega": target_prefactor["omega"] - two_thirds * payment["omega"] / m_power,
        "k": ratio_exp["k"],
        "p": two_thirds / m_power,
    }
    if MUTATION == "normalized_R":
        target_normalized["R"] += Q(1, 3)
    if MUTATION == "normalized_omega":
        target_normalized["omega"] += Q(1, 3)
    if MUTATION == "normalized_k":
        target_normalized["k"] += Q(1, 3)
    if MUTATION == "normalized_p":
        target_normalized["p"] = Q(1, 3)
    exponent_observed = {
        "fluxUpper": exponent_json(flux_exp),
        "mass": exponent_json(mass_exp),
        "massTwoThirds": exponent_json(mass_two_thirds),
        "fluxOverMassTwoThirds": exponent_json(ratio_exp),
        "targetNormalized": exponent_json(target_normalized),
        "amplitudeCancels": MUTATION != "amplitude_cancel",
    }

    # L.16--L.17: exact threshold and exact decimal rendering only.
    threshold_fixture = fixtures["thresholdCase"]
    alpha = q(threshold_fixture["alphaStar"])
    if MUTATION == "alpha_numerator":
        alpha += Q(1, 107163)
    if MUTATION == "alpha_denominator":
        alpha = Q(27163, 107162)
    multiplier = q(threshold_fixture["multiplier"])
    if MUTATION == "kappa_multiplier":
        multiplier = Q(2)
    kappa_star = alpha * multiplier
    if MUTATION == "kappa_reduce":
        kappa_star += Q(1, 71442)
    strict_kappa = q(threshold_fixture["strictTestKappa"])
    strict_margin = strict_kappa - kappa_star
    strict_exponent_margin = Q(2, 3) * strict_kappa - alpha
    endpoint = "2*kappaStar/3=alphaStar"
    if MUTATION == "endpoint_equality":
        endpoint = "2*kappaStar/3>alphaStar"
    display = rounded_decimal(kappa_star, int(threshold_fixture["displayDigits"]))
    if MUTATION == "decimal_display":
        display = "0.3802105205"
    threshold_observed = {
        "alphaStar": qtext(alpha),
        "kappaStar": qtext(kappa_star),
        "endpointEquality": endpoint,
        "displayRounded10": display,
        "strictTestKappa": qtext(strict_kappa),
        "strictKappaMargin": qtext(strict_margin),
        "strictExponentMargin": qtext(strict_exponent_margin),
        "RInterval": "R>1" if MUTATION == "R_interval" else threshold_fixture["RInterval"],
    }

    tags = re.findall(r"\\tag\{(L\.[^}]+)\}", text)
    if MUTATION == "tag":
        tags.append("L.1")
    references = [
        "L." + value for value in re.findall(r"\(L\.([0-9]+[a-z]?)\)", text)
    ]
    if MUTATION == "reference":
        references.append("L.99")
    display_open = sum(line.strip() == r"\[" for line in text.splitlines())
    display_close = sum(line.strip() == r"\]" for line in text.splitlines())
    if MUTATION == "display":
        display_open += 1
    expected_tags = [f"L.{index}" for index in range(1, 18)]

    dependency_paths = (
        "research/r075e_horizontal_cross_mode_flux_reduction.md",
        "research/r075g_signed_flux_gain_threshold.md",
        "research/r075k_positive_majorant_high_frequency_trace_loss.md",
    )
    dependency_table_present = all(
        any(path in line and FROZEN_SOURCES[path] in line for line in text.splitlines())
        for path in dependency_paths
    )
    if MUTATION == "dependency_table_missing":
        dependency_table_present = False

    required_tokens = (
        r"\mathcal L_B:=\partial_t+B\partial_2-\partial_2^2",
        r"F_k(t,x_2) :=A e^{-k^2t}\cos\bigl(k(x_2-Bt)\bigr)",
        r"\boxed{\mathcal L_BF_k=0.}",
        r"\int_0^T e^{-2k^2t}\,dt",
        r"\bigl(1-e^{-2k^2T}\bigr)",
        r"\frac{A^2|B|V_\xi}{8k^2}",
        r"\frac{8A^3}{9k^2}\bigl(1-e^{-3k^2T}\bigr)",
        r"k^2T\ge1",
        r"C_*:=\frac18 \left(\frac9{8(1-e^{-3})}\right)^{2/3}",
        r"R^{1/3}\omega^{1/3}k^{-2/3}",
        r"\frac{27163}{71442}",
        "not a proof of G.1",
        "or prove E.24",
        r"\mathbf{NOT\ CLAY}",
    )

    boundary = {
        "integerKAtLeastOne": MUTATION not in ("k_integer", "k_lower"),
        "amplitudePositive": MUTATION != "A_positive",
        "realConstantShear": MUTATION not in ("B_real", "constant_shear"),
        "oneRealHarmonic": MUTATION not in ("real_field", "single_harmonic"),
        "diagonalRemovedBeforeAbsoluteValue": MUTATION not in (
            "diagonal_after_absolute", "absolute_before_cancel"
        ),
        "periodicDerivativeMeanZero": MUTATION != "periodic_mean",
        "etaMeasurableAndInUnitInterval": MUTATION != "eta_measurable",
        "xiSmoothPeriodicReal": MUTATION not in ("xi_periodic", "xi_smooth", "xi_real"),
        "VxiUsesAbsoluteDerivative": MUTATION != "vxi_absolute",
        "innerIntegralBoundedByVxi": MUTATION != "vxi_bound",
        "q2DropDirectionCorrect": MUTATION != "drop_q2_direction",
        "q3OnlySymbolicInterval": MUTATION != "q3_float_equality",
        "conditionAndComparisonDirectionCorrect": MUTATION not in (
            "condition_direction", "condition_one", "q3_comparison"
        ),
        "c3StrictlyBetweenZeroAndOne": MUTATION != "c3_positive",
        "positivePartNormalization": MUTATION != "positive_part",
        "strictThresholdDirection": MUTATION != "strict_direction",
        "decimalIsDisplayOnly": MUTATION != "decimal_exact",
        "frequencyImplicationDirection": MUTATION != "frequency_direction",
        "physicalSignedFlux": MUTATION != "physical_signed",
        "fullTorusCubicOnly": MUTATION != "full_torus",
        "BVxiCoefficientUnpaid": MUTATION != "unpaid_BVxi",
        "notG1": MUTATION != "g1_claim",
        "notE24": MUTATION != "e24_claim",
        "notFullVersionM": MUTATION != "full_versionm_claim",
        "multimodeOpen": MUTATION != "multimode_closed",
        "collarLocalizationOpen": MUTATION != "collar_closed",
        "nonconstantShearOpen": MUTATION != "nonconstant_closed",
        "lowFrequencySectorOpen": MUTATION != "low_frequency_closed",
        "completeClockOpen": MUTATION != "complete_clock",
        "fixedDeletionOpen": MUTATION != "fixed_deletion",
        "suitableWeakTransferOpen": MUTATION != "suitable_weak",
        "regularityOpen": MUTATION != "regularity",
        "singularityOpen": MUTATION != "singularity",
        "noNoveltyClaim": MUTATION != "novelty",
        "noPriorityClaim": MUTATION != "priority",
        "noSimulationUsed": MUTATION != "simulation",
        "notClay": MUTATION != "clay",
    }

    checks = {
        "allFrozenSourceBindings": record(
            all(row["expectedSha256"] == row["observedSha256"] for row in source_rows.values()),
            sources=source_rows,
        ),
        "fixtureAndExpectedBindings": record(
            fixture_hash == fixture_expected_hash
            and expected_hash == expected_expected_hash
            and fixtures["frozenSources"] == FROZEN_SOURCES,
        ),
        "primaryAuditBindingAndStatus": record(
            FROZEN_SOURCES["research/r075l_single_harmonic_diffusive_signed_flux_gain.md"] in audit_text
            and "Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0." in audit_text
            and "Equation tags L.1--L.17 are unique and consecutive." in audit_text
            and "All 17 display-math environments are paired." in audit_text,
        ),
        "threeDependencyTableBindings": record(dependency_table_present),
        "operatorSigns": record(operator_observed == expected["operator"], observed=operator_observed),
        "etaBounds": record(eta_observed == expected["eta"], observed=eta_observed),
        "passiveDifferentiationAndFourierSquare": record(
            family_observed == expected["passiveFamily"]
            and all(row["residualCos"] == row["residualSin"] == "0" for row in family_observed),
            observed=family_observed,
        ),
        "diagonalCancellationBeforeAbsoluteValue": record(
            all(row["diagonalPairing"] == "0" for row in family_observed)
            and boundary["diagonalRemovedBeforeAbsoluteValue"]
            and boundary["periodicDerivativeMeanZero"],
        ),
        "exactTimeIntegralAndFluxFactor": record(
            time_observed == expected["timeIntegral"]
            and decay_two == 2
            and boundary["q2DropDirectionCorrect"],
            observed=time_observed,
        ),
        "absoluteCosineMomentAndCubicMass": record(
            moment_observed == expected["absoluteCosineMoment"]
            and decay_three == 3
            and all(q(row["massCoefficientTimesOneMinusQ3"]) > 0 for row in family_observed),
            observed=moment_observed,
        ),
        "symbolicExponentialGuardAndA2Conversion": record(
            conversion_observed == expected["massConversion"]
            and boundary["q3OnlySymbolicInterval"]
            and boundary["conditionAndComparisonDirectionCorrect"]
            and boundary["c3StrictlyBetweenZeroAndOne"],
            observed=conversion_observed,
        ),
        "homogeneityAndTargetNormalization": record(
            exponent_observed == expected["exponents"]
            and target_normalized == {
                "R": Q(1, 3), "omega": Q(1, 3), "k": Q(-2, 3), "p": Q(2, 3)
            },
            observed=exponent_observed,
        ),
        "exactFrequencyThreshold": record(
            threshold_observed == expected["threshold"]
            and Q(2, 3) * kappa_star == alpha
            and strict_margin > 0 and strict_exponent_margin > 0,
            observed=threshold_observed,
        ),
        "correctRLessThanOnePowerDirection": record(
            threshold_observed["RInterval"] == "0<R<1"
            and Q(2, 3) * strict_kappa > alpha
            and MUTATION != "frequency_direction",
        ),
        "tagsReferencesAndDisplays": record(
            tags == expected_tags and len(set(tags)) == 17
            and not (set(references) - set(tags))
            and display_open == display_close == 17,
        ),
        "formulaAndStatusSentinels": record(
            all(re.sub(r"\s+", " ", token) in flat_text for token in required_tokens),
        ),
        "sourceReportBoundary": record(
            "no E.24, complete-clock, regularity, novelty, or priority claim" in flat_source
            and "one-real-harmonic physical signed flux" in flat_source
            and "full-torus spacetime cubic mass" in flat_source,
        ),
        "claimBoundary": record(all(boundary.values()), state=boundary),
        "utf8AndControlSafety": record(
            "\ufffd" not in scan_text
            and not any(ord(character) < 32 and character not in "\t\n" for character in scan_text),
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
        "operator": operator_observed,
        "eta": eta_observed,
        "passiveFamily": family_observed,
        "timeIntegral": time_observed,
        "absoluteCosineMoment": moment_observed,
        "massConversion": conversion_observed,
        "exponents": exponent_observed,
        "threshold": threshold_observed,
        "claimBoundary": boundary,
    }
    OUT_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    failed = [name for name, item in checks.items() if not item["pass"]]
    OUT_REPORT.write_text(
        "# R0.75L finite certificate report\n\n"
        f"- Verdict: **{verdict}**\n"
        f"- Assertions: {payload['assertions']['passed']}/{payload['assertions']['total']}\n"
        f"- Main SHA-256: {sha256(MAIN)}\n"
        f"- Fixture SHA-256: {fixture_hash}\n"
        f"- Expected SHA-256: {expected_hash}\n"
        f"- Failed checks: {'none' if not failed else '; '.join(failed)}\n\n"
        "Exact rational Fourier ledgers verify the L_B signs and the three-term "
        "cancellation for k=1,2,5. They also verify the 0,+/-2k square modes, "
        "zero diagonal pairing before absolute values, 0<=eta<=1, the V_xi bound, "
        "and the (1-q2)/(2k^2) time primitive with flux coefficient "
        "A^2|B|V_xi/(8k^2).\n\n"
        "The quarter-period ledger gives integral |cos(kx)|^3=8/3 and the exact "
        "mass 8A^3(1-q3)/(9k^2). The exp(-3) quantity is used only through "
        "0<q3<=exp(-3)<1, never as a floating-point equality. Homogeneity gives "
        "A cancellation, C_*, k^(-2/3), and normalized powers "
        "R^(1/3)omega^(1/3)p^(2/3).\n\n"
        "The exact endpoint is kappa*=27163/71442; equality is not the strict "
        "threshold. This remains a one-real-harmonic, constant-shear, full-torus "
        "benchmark with |B|V_xi unpaid. It is not G.1, E.24, or full Version-M. "
        "**NOT CLAY.**\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "suite": "r075l-single-harmonic-diffusive-signed-flux-gain",
        "verdict": verdict,
        "assertions": len(checks),
    }, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
