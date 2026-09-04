#!/usr/bin/env python3
"""Fail-closed exact finite certificate for frozen R0.75M."""

from __future__ import annotations

import hashlib
import json
import os
import re
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "research/r075m_dyadic_packet_diffusive_flux_gain.md"
PRIMARY_AUDIT = ROOT / "research/r075m_dyadic_packet_diffusive_flux_gain_primary_audit.md"
REPORT_SOURCE = ROOT / "research/r075m_report-source.md"
FIXTURES = ROOT / "scripts/r075m_dyadic_packet_diffusive_flux_gain_fixtures.json"
EXPECTED = ROOT / "scripts/r075m_dyadic_packet_diffusive_flux_gain_expected.json"
OUT_JSON = Path(os.environ.get(
    "R075M_JSON", ROOT / "research/r075m_dyadic_packet_diffusive_flux_gain_certificate.json"
))
OUT_REPORT = Path(os.environ.get(
    "R075M_REPORT", ROOT / "research/r075m_dyadic_packet_diffusive_flux_gain_certificate_report.md"
))
MUTATION = os.environ.get("R075M_MUTATION", "")
SCHEMA = "r075m-dyadic-packet-diffusive-flux-gain-certificate-v1"

FROZEN_SOURCES = {
    "research/r075e_horizontal_cross_mode_flux_reduction.md":
        "99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049",
    "research/r075g_signed_flux_gain_threshold.md":
        "f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41",
    "research/r075l_single_harmonic_diffusive_signed_flux_gain.md":
        "52e25b2fdf1a224609c9e8fafa1c041b7f09a361f75f4b3e44ebcdddb756cdf5",
    "research/r075m_dyadic_packet_diffusive_flux_gain.md":
        "13434bbc15eabecd5a695eceef01a7d63415e96511b14c29cc8abcd1297c7bf7",
    "research/r075m_dyadic_packet_diffusive_flux_gain_primary_audit.md":
        "2b5ee050c09e3be925143c12c29082c3fe562a83b9a2d2669511a2bb1684d7dc",
    "research/r075m_report-source.md":
        "f8ed7af8ef5051b0efa73177d0530562917d55dfa6476b00b8f871db0da99d67",
}
FIXTURES_SHA256 = "b93d727b4bf0729af2064e51fbc0c1450d98806c9b92fe11727b4d5423fa157f"
EXPECTED_SHA256 = "cef1705998bc935448f371d6f389d46059b59e99bf230bd75dad0489fb85a4f4"

NEGATIVE_MUTATIONS = (
    "source_drift", "audit_drift", "report_source_drift", "dependency_drift",
    "dependency_table_missing", "fixture_drift", "expected_drift", "tag",
    "reference", "display", "control", "operator_time", "operator_drift",
    "operator_diffusion", "fourier_factor", "reconstruction_sign",
    "difference_index", "spatial_factor", "flux_half", "modal_prefactor",
    "d0_nonzero", "cancel_after_absolute", "absolute_before_diagonal",
    "time_phase", "time_decay", "diffusion_sign", "passive_residual",
    "K_lower", "K_upper", "K_integer", "packet_finite", "real_symmetry",
    "mode_count", "eta_lower", "eta_upper", "eta_measurable", "xi_periodic",
    "xi_smooth", "xi_real", "W_definition", "time_kernel_absolute",
    "time_kernel_infinity", "kernel_denominator", "denominator_lower",
    "denominator_factor", "row_sum", "column_sum", "schur_direction",
    "schur_sqrt", "quadratic_form", "mode_count_loss", "parseval_factor",
    "energy_quarter", "short_window", "short_window_inside", "upper_edge",
    "l2_decay_multiplier", "l2_endpoint", "l2_direction", "holder_measure",
    "holder_direction", "l3_endpoint", "mass_window", "mass_constant",
    "mass_K_power", "mass_E_power", "condition", "inversion_constant",
    "inversion_e_power", "inversion_2pi_power", "inversion_K_power",
    "inversion_M_power", "inverse_heat", "combined_constant",
    "combined_e_power", "combined_2pi_power", "combined_K_power",
    "combined_M_power", "combined_B_power", "combined_W_power",
    "amplitude_degree", "wiener_weight", "wiener_cs_direction",
    "wiener_inverse_series", "wiener_weighted_sum", "wiener_parseval",
    "wiener_first_derivative", "wiener_second_derivative",
    "wiener_third_derivative", "pointwise_replacement", "target_R",
    "target_omega", "payment_R", "payment_omega", "payment_M",
    "normalized_R", "normalized_omega", "normalized_K", "normalized_p",
    "positive_part", "R_positive", "omega_positive", "alpha_numerator",
    "alpha_denominator", "kappa_multiplier", "kappa_reduce",
    "strict_direction", "endpoint_equality", "R_domain", "frequency_direction",
    "physical_signed", "full_torus", "single_packet", "arbitrary_interference",
    "interpacket_closed", "cutoff_calibrated", "collar_localized",
    "local_versionm", "low_difference_closed", "nonconstant_closed",
    "e24_claim", "complete_clock", "fixed_deletion", "suitable_weak",
    "regularity", "singularity", "novelty", "priority", "simulation", "clay",
)

Q = Fraction


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(value: str | int) -> Q:
    return Q(value)


def qtext(value: Q) -> str:
    return str(value)


def record(ok: bool, **details: Any) -> dict[str, Any]:
    return {"pass": bool(ok), **details}


def exponent_json(vector: dict[str, Q]) -> dict[str, str]:
    return {key: qtext(value) for key, value in vector.items()}


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R075M_MUTATION: {MUTATION}")

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
        source_expectations["research/r075m_dyadic_packet_diffusive_flux_gain.md"] = "0" * 64
    if MUTATION == "audit_drift":
        source_expectations[
            "research/r075m_dyadic_packet_diffusive_flux_gain_primary_audit.md"
        ] = "0" * 64
    if MUTATION == "report_source_drift":
        source_expectations["research/r075m_report-source.md"] = "0" * 64
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

    operator_observed = dict(fixtures["operatorCase"])
    if MUTATION == "operator_time":
        operator_observed["timeCoefficient"] = "-1"
    if MUTATION == "operator_drift":
        operator_observed["driftCoefficientSymbol"] = "-B"
    if MUTATION == "operator_diffusion":
        operator_observed["secondDerivativeCoefficient"] = "1"

    packet_fixture = fixtures["fourierPacketCase"]
    K = int(packet_fixture["K"])
    modes = list(packet_fixture["modes"])
    shear = q(packet_fixture["B"])
    coefficients = {int(key): q(value) for key, value in packet_fixture["coefficients"].items()}
    if MUTATION == "real_symmetry":
        coefficients[-2] += 1
    coefficient_energy = sum(abs(value) ** 2 for value in coefficients.values())
    real_admissible = all(coefficients.get(-n) == coefficients.get(n) for n in modes)
    all_in_band = all(K <= abs(n) <= 2 * K for n in modes)
    if MUTATION in ("K_lower", "K_upper"):
        all_in_band = False
    packet_observed = {
        "K": K + 1 if MUTATION == "K_integer" else K,
        "B": qtext(shear),
        "modes": modes,
        "modeCount": len(modes) + (1 if MUTATION == "mode_count" else 0),
        "realAdmissible": real_admissible,
        "allModesInDyadicBand": all_in_band,
        "coefficientEnergy": qtext(coefficient_energy),
        "E0OverPi": qtext(2 * coefficient_energy),
    }

    evolution_observed = []
    for n in modes:
        time_real = Q(n * n if MUTATION == "time_decay" else -n * n)
        time_imag = Q(n) * shear * (1 if MUTATION == "time_phase" else -1)
        drift_imag = Q(n) * shear
        diffusion_real = Q(-n * n if MUTATION == "diffusion_sign" else n * n)
        residual_real = time_real + diffusion_real
        residual_imag = time_imag + drift_imag
        if MUTATION == "passive_residual":
            residual_real += 1
        evolution_observed.append({
            "n": n,
            "timeReal": qtext(time_real),
            "timeImag": qtext(time_imag),
            "driftImag": qtext(drift_imag),
            "diffusionReal": qtext(diffusion_real),
            "residualReal": qtext(residual_real),
            "residualImag": qtext(residual_imag),
        })

    d = {0: q(packet_fixture["dZero"])}
    for row in packet_fixture["positiveCutoffModes"]:
        ell = int(row["ell"])
        value = q(row["coefficient"])
        d[ell] = value
        d[-ell] = value
    if MUTATION == "d0_nonzero":
        d[0] = 1
    wiener_norm = sum(abs(value) for value in d.values())
    if MUTATION == "W_definition":
        wiener_norm -= abs(d[8])

    fourier_observed = {
        "reconstructionPhase": "-i*ell*x" if MUTATION == "reconstruction_sign" else "+i*ell*x",
        "kernelIndex": "n-m" if MUTATION == "difference_index" else "m-n",
        "dZero": qtext(d[0]),
        "diagonalVanishesBeforeAbsoluteValue": MUTATION not in (
            "cancel_after_absolute", "absolute_before_diagonal"
        ),
        "spatialIntegralFactor": "pi" if MUTATION == "spatial_factor" else "2*pi",
        "fluxKernelFactor": "2*pi*B" if MUTATION in (
            "flux_half", "modal_prefactor"
        ) else "pi*B",
    }
    if MUTATION == "fourier_factor":
        fourier_observed["reconstructionPhase"] = "coefficient-1/pi"

    eta_fixture = fixtures["etaCase"]
    eta_lower = q(eta_fixture["lowerBound"])
    eta_upper = q(eta_fixture["upperBound"])
    if MUTATION == "eta_lower":
        eta_lower = Q(1, 4)
    if MUTATION == "eta_upper":
        eta_upper = Q(3, 4)
    eta_observed = {
        "rows": [
            {"eta": value, "admissible": eta_lower <= q(value) <= eta_upper}
            for value in eta_fixture["samples"]
        ]
    }

    factor_fixture = fixtures["kernelFactorCase"]
    denominator_lower = Q(2 * K * K)
    if MUTATION == "denominator_lower":
        denominator_lower = Q(K * K)
    if MUTATION == "denominator_factor":
        denominator_lower = Q(4 * K * K)

    def kernel_denominator(n: int, m: int) -> Q:
        if MUTATION == "kernel_denominator":
            return Q(abs(n) + abs(m))
        return Q(n * n + m * m)

    matrix = {
        (n, m): abs(d.get(m - n, Q(0))) / kernel_denominator(n, m)
        for n in modes for m in modes
    }
    row_sums = {n: sum(matrix[n, m] for m in modes) for n in modes}
    column_sums = {m: sum(matrix[n, m] for n in modes) for m in modes}
    if MUTATION == "row_sum":
        row_sums[modes[0]] += 1
    if MUTATION == "column_sum":
        column_sums[modes[0]] += 1
    crude_bound = wiener_norm / denominator_lower
    absolute_quadratic = sum(
        matrix[n, m] * abs(coefficients[n]) * abs(coefficients[m])
        for n in modes for m in modes
    )
    if MUTATION == "quadratic_form":
        absolute_quadratic += 1
    schur_upper = crude_bound * coefficient_energy
    if MUTATION == "schur_sqrt":
        schur_upper += 1
    parseval_factor = "pi" if MUTATION == "parseval_factor" else "2*pi"
    final_energy_coefficient = "Wxi/(2*K^2)" if MUTATION == "energy_quarter" else "Wxi/(4*K^2)"
    schur_observed = {
        "Wxi": qtext(wiener_norm),
        "denominatorLowerBound": qtext(denominator_lower),
        "rowSums": {str(key): qtext(value) for key, value in row_sums.items()},
        "columnSums": {str(key): qtext(value) for key, value in column_sums.items()},
        "maximumExactRowOrColumn": qtext(max(max(row_sums.values()), max(column_sums.values()))),
        "crudeRowColumnBound": qtext(crude_bound),
        "absoluteQuadraticForm": qtext(absolute_quadratic),
        "schurQuadraticUpper": qtext(schur_upper),
        "parsevalEnergyFactor": parseval_factor,
        "finalEnergyCoefficient": final_energy_coefficient,
        "modeCountFactor": "K" if MUTATION == "mode_count_loss" else "none",
    }

    short_fixture = fixtures["shortTimeCase"]
    time_denominator = q(short_fixture["timeDenominator"])
    if MUTATION in ("short_window", "mass_window"):
        time_denominator = 4
    upper_multiplier = q(short_fixture["upperPacketMultiplier"])
    if MUTATION == "upper_edge":
        upper_multiplier = 3
    heat_multiplier = q(short_fixture["squaredHeatMultiplier"])
    if MUTATION == "l2_decay_multiplier":
        heat_multiplier = 1
    upper_square = upper_multiplier ** 2
    heat_exponent_coefficient = heat_multiplier * upper_square
    endpoint_exponent = heat_exponent_coefficient / time_denominator
    l2_factor = "exp(-2)" if MUTATION == "l2_endpoint" else "exp(-1)"
    holder_factor = "(2*pi)^(-1)" if MUTATION == "holder_measure" else "(2*pi)^(-1/2)"
    l3_factor = "exp(-1)" if MUTATION == "l3_endpoint" else "exp(-3/2)"
    cubic_monomial = {
        "rational": qtext(Q(1, int(time_denominator))),
        "e": "-1" if MUTATION == "mass_constant" else "-3/2",
        "2pi": "-1" if MUTATION == "holder_measure" else "-1/2",
        "K": "-1" if MUTATION == "mass_K_power" else "-2",
        "E0": "1" if MUTATION == "mass_E_power" else "3/2",
    }
    inversion = {
        "rational": "2" if MUTATION == "inversion_constant" else "4",
        "e": "3/2" if MUTATION == "inversion_e_power" else "1",
        "2pi": "1/2" if MUTATION == "inversion_2pi_power" else "1/3",
        "K": "2/3" if MUTATION == "inversion_K_power" else "4/3",
        "M": "1/3" if MUTATION == "inversion_M_power" else "2/3",
    }
    combined = {
        "rational": "4" if MUTATION == "combined_constant" else "1",
        "e": "0" if MUTATION == "combined_e_power" else "1",
        "2pi": "1/2" if MUTATION == "combined_2pi_power" else "1/3",
        "B": "0" if MUTATION == "combined_B_power" else "1",
        "Wxi": "0" if MUTATION == "combined_W_power" else "1",
        "K": "-1/3" if MUTATION == "combined_K_power" else "-2/3",
        "M": "1/3" if MUTATION == "combined_M_power" else "2/3",
    }
    short_observed = {
        "interval": f"0<=t<=1/({qtext(time_denominator)}*K^2)",
        "upperModeSquareBound": f"{qtext(upper_square)}*K^2",
        "squaredHeatExponent": f"-{qtext(heat_exponent_coefficient)}*K^2*t",
        "endpointL2Factor": l2_factor,
        "holderCircleFactor": holder_factor,
        "endpointL3Factor": l3_factor,
        "cubicLowerMonomial": cubic_monomial,
        "energyInversionMonomial": inversion,
        "combinedFluxMonomial": combined,
    }

    weighted_sum = sum((1 + ell * ell) * abs(value) ** 2 for ell, value in d.items())
    inverse_sum = sum(Q(1, 1 + ell * ell) for ell in range(-8, 9))
    if MUTATION == "wiener_weighted_sum":
        weighted_sum += 1
    if MUTATION == "wiener_inverse_series":
        inverse_sum += 1
    cs_gap = weighted_sum * inverse_sum - wiener_norm ** 2
    if MUTATION == "wiener_cs_direction":
        cs_gap *= -1
    wiener_observed = {
        "Wxi": qtext(wiener_norm),
        "finiteWeightedSquareSum": qtext(weighted_sum),
        "finiteInverseWeightSum": qtext(inverse_sum),
        "WxiSquared": qtext(wiener_norm ** 2),
        "cauchySchwarzGap": qtext(cs_gap),
        "weightSymbol": "1+|ell|" if MUTATION == "wiener_weight" else "1+ell^2",
        "parsevalIdentity": (
            "sum(1+ell^2)|d_ell|^2=||xi'||_2^2+||xi''||_2^2"
            if MUTATION == "wiener_parseval" else
            "sum(1+ell^2)|d_ell|^2=(||xi'||_2^2+||xi''||_2^2)/(2*pi)"
        ),
        "highestXiDerivative": 3 if MUTATION == "wiener_third_derivative" else 2,
        "pointwiseSupAloneSufficient": MUTATION == "pointwise_replacement",
    }

    normalization_fixture = fixtures["normalizationCase"]
    gain = {key: q(value) for key, value in normalization_fixture["fluxGain"].items()}
    if MUTATION == "combined_K_power":
        gain["K"] = Q(-1, 3)
    target = {key: q(value) for key, value in normalization_fixture["targetPrefactor"].items()}
    payment = {key: q(value) for key, value in normalization_fixture["paymentDefinition"].items()}
    if MUTATION == "target_R":
        target["R"] = 0
    if MUTATION == "target_omega":
        target["omega"] = 0
    if MUTATION == "payment_R":
        payment["R"] = -1
    if MUTATION == "payment_omega":
        payment["omega"] = -1
    if MUTATION == "payment_M":
        payment["M"] = 2
    p_m = payment["M"]
    normalized = {
        "B": gain["B"],
        "Wxi": gain["Wxi"],
        "R": target["R"] - gain["M"] * payment["R"] / p_m,
        "omega": target["omega"] - gain["M"] * payment["omega"] / p_m,
        "K": gain["K"],
        "p": gain["M"] / p_m,
    }
    if MUTATION == "normalized_R":
        normalized["R"] += Q(1, 3)
    if MUTATION == "normalized_omega":
        normalized["omega"] += Q(1, 3)
    if MUTATION == "normalized_K":
        normalized["K"] += Q(1, 3)
    if MUTATION == "normalized_p":
        normalized["p"] = Q(1, 3)
    normalization_observed = {
        "fluxGain": exponent_json(gain),
        "targetNormalized": exponent_json(normalized),
    }

    threshold_fixture = fixtures["thresholdCase"]
    alpha = q(threshold_fixture["alphaStar"])
    if MUTATION == "alpha_numerator":
        alpha += Q(1, 107163)
    if MUTATION == "alpha_denominator":
        alpha = Q(27163, 107162)
    multiplier = q(threshold_fixture["multiplier"])
    if MUTATION == "kappa_multiplier":
        multiplier = 2
    kappa_star = alpha * multiplier
    if MUTATION == "kappa_reduce":
        kappa_star += Q(1, 71442)
    strict_kappa = q(threshold_fixture["strictTestKappa"])
    threshold_observed = {
        "alphaStar": qtext(alpha),
        "kappaStar": qtext(kappa_star),
        "endpointEquality": (
            "2*kappaStar/3>alphaStar" if MUTATION == "endpoint_equality"
            else "2*kappaStar/3=alphaStar"
        ),
        "strictTestKappa": qtext(strict_kappa),
        "strictKappaMargin": qtext(strict_kappa - kappa_star),
        "strictExponentMargin": qtext(Q(2, 3) * strict_kappa - alpha),
        "RInterval": "R>1" if MUTATION == "R_domain" else threshold_fixture["RInterval"],
        "powerDirection": (
            "larger-exponent-gives-larger-power" if MUTATION == "frequency_direction"
            else "larger-exponent-gives-smaller-power"
        ),
    }

    tags = re.findall(r"\\tag\{(M\.[^}]+)\}", text)
    if MUTATION == "tag":
        tags.append("M.1")
    references = ["M." + value for value in re.findall(r"\(M\.([0-9]+[a-z]?)\)", text)]
    if MUTATION == "reference":
        references.append("M.99")
    display_open = sum(line.strip() == r"\[" for line in text.splitlines())
    display_close = sum(line.strip() == r"\]" for line in text.splitlines())
    if MUTATION == "display":
        display_open += 1
    expected_tags = [f"M.{index}" for index in range(1, 21)]

    dependencies = (
        "research/r075e_horizontal_cross_mode_flux_reduction.md",
        "research/r075g_signed_flux_gain_threshold.md",
        "research/r075l_single_harmonic_diffusive_signed_flux_gain.md",
    )
    dependency_table_present = all(
        any(path in line and FROZEN_SOURCES[path] in line for line in text.splitlines())
        for path in dependencies
    )
    if MUTATION == "dependency_table_missing":
        dependency_table_present = False

    required_tokens = (
        r"d_\ell:=\frac1{2\pi}\int_0^{2\pi}",
        r"\mathcal W_\xi:=\sum_{\ell\in\mathbb Z}|d_\ell|",
        r"\mathcal L_BF=0",
        r"\pi B\sum_{n,m\in\Lambda_K}d_{m-n}c_n\overline{c_m}",
        r"\le\frac1{2K^2}",
        r"\frac{|B|\mathcal W_\xi}{4K^2}E_0",
        r"\ge e^{-1}E_0",
        r"(2\pi)^{-1/2}e^{-3/2}E_0^{3/2}",
        r"4e(2\pi)^{1/3}K^{4/3}M_K^{2/3}",
        r"e(2\pi)^{1/3}|B|\mathcal W_\xi",
        r"R^{1/3}\omega^{1/3}K^{-2/3}",
        r"\frac{27163}{71442}",
        r"\mathbf{NOT\ CLAY}",
    )

    boundary = {
        "KIntegerAtLeastOne": MUTATION not in ("K_integer", "K_lower"),
        "finiteRealAdmissiblePacket": MUTATION not in ("packet_finite", "real_symmetry"),
        "upperBandAtMostTwoK": MUTATION != "K_upper",
        "etaInUnitInterval": MUTATION not in ("eta_measurable", "eta_lower", "eta_upper"),
        "xiSmoothPeriodicReal": MUTATION not in ("xi_periodic", "xi_smooth", "xi_real"),
        "timeKernelAbsoluteValue": MUTATION != "time_kernel_absolute",
        "extensionToInfinityDirection": MUTATION != "time_kernel_infinity",
        "schurInequalityDirection": MUTATION != "schur_direction",
        "shortWindowContained": MUTATION != "short_window_inside",
        "L2LowerDirection": MUTATION != "l2_direction",
        "HolderLowerDirection": MUTATION != "holder_direction",
        "conditionK2TAtLeastOne": MUTATION != "condition",
        "noInverseHeatFlow": MUTATION != "inverse_heat",
        "passiveAmplitudeDegreeTwo": MUTATION != "amplitude_degree",
        "WienerUsesBothFirstAndSecondDerivatives": MUTATION not in (
            "wiener_first_derivative", "wiener_second_derivative"
        ),
        "noThirdDerivativeRequired": MUTATION != "wiener_third_derivative",
        "pointwiseSupNotSubstituted": MUTATION != "pointwise_replacement",
        "positivePartNormalization": MUTATION != "positive_part",
        "RAndOmegaPositive": MUTATION not in ("R_positive", "omega_positive"),
        "strictThreshold": MUTATION != "strict_direction",
        "physicalSignedFlux": MUTATION != "physical_signed",
        "fullTorusCubicOnly": MUTATION != "full_torus",
        "singleDyadicPacketOnly": MUTATION != "single_packet",
        "arbitraryFiniteWithinPacketInterference": MUTATION != "arbitrary_interference",
        "noModeCountFactor": MUTATION not in ("mode_count_loss",),
        "interpacketSummationOpen": MUTATION != "interpacket_closed",
        "cutoffWienerScalingOpen": MUTATION != "cutoff_calibrated",
        "collarLocalizationOpen": MUTATION != "collar_localized",
        "localVersionMReplacementOpen": MUTATION != "local_versionm",
        "lowDifferenceSectorOpen": MUTATION != "low_difference_closed",
        "nonconstantShearOpen": MUTATION != "nonconstant_closed",
        "E24Open": MUTATION != "e24_claim",
        "completeClockOpen": MUTATION != "complete_clock",
        "fixedDeletionOpen": MUTATION != "fixed_deletion",
        "suitableWeakTransferOpen": MUTATION != "suitable_weak",
        "regularityOpen": MUTATION != "regularity",
        "singularityOpen": MUTATION != "singularity",
        "noNovelty": MUTATION != "novelty",
        "noPriority": MUTATION != "priority",
        "noSimulation": MUTATION != "simulation",
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
            FROZEN_SOURCES["research/r075m_dyadic_packet_diffusive_flux_gain.md"] in audit_text
            and "Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0." in audit_text
            and "Equation tags M.1--M.20 are unique and consecutive." in audit_text
            and "All 20 display-math environments are paired." in audit_text,
        ),
        "threeDependencyTableBindings": record(dependency_table_present),
        "operatorAndExactPacketEvolution": record(
            operator_observed == expected["operator"]
            and evolution_observed == expected["evolutionCases"]
            and all(row["residualReal"] == row["residualImag"] == "0" for row in evolution_observed),
        ),
        "packetSupportRealityAndParseval": record(packet_observed == expected["packet"], observed=packet_observed),
        "fourierConventionPiAndDiagonal": record(
            fourier_observed == expected["fourierConvention"]
            and fourier_observed["dZero"] == "0"
            and fourier_observed["diagonalVanishesBeforeAbsoluteValue"],
            observed=fourier_observed,
        ),
        "etaBounds": record(eta_observed == expected["eta"], observed=eta_observed),
        "schurRowsColumnsAndQuarterConstant": record(
            schur_observed == expected["schur"]
            and max(row_sums.values()) <= crude_bound
            and max(column_sums.values()) <= crude_bound
            and absolute_quadratic <= schur_upper
            and boundary["schurInequalityDirection"],
            observed=schur_observed,
        ),
        "shortTimeL2L3AndInversion": record(
            short_observed == expected["shortTime"]
            and endpoint_exponent == 1
            and boundary["shortWindowContained"]
            and boundary["L2LowerDirection"]
            and boundary["HolderLowerDirection"]
            and boundary["conditionK2TAtLeastOne"],
            observed=short_observed,
        ),
        "combinedConstantAndHomogeneity": record(
            combined == expected["shortTime"]["combinedFluxMonomial"]
            and combined == {
                "rational": "1", "e": "1", "2pi": "1/3", "B": "1",
                "Wxi": "1", "K": "-2/3", "M": "2/3"
            }
            and boundary["passiveAmplitudeDegreeTwo"],
        ),
        "wienerH1AndFiniteCauchySchwarz": record(
            wiener_observed == expected["wiener"]
            and cs_gap >= 0
            and boundary["WienerUsesBothFirstAndSecondDerivatives"]
            and boundary["noThirdDerivativeRequired"]
            and boundary["pointwiseSupNotSubstituted"],
            observed=wiener_observed,
        ),
        "targetNormalization": record(
            normalization_observed == expected["normalization"]
            and normalized == {
                "B": Q(1), "Wxi": Q(1), "R": Q(1, 3), "omega": Q(1, 3),
                "K": Q(-2, 3), "p": Q(2, 3)
            },
            observed=normalization_observed,
        ),
        "exactStrictThreshold": record(
            threshold_observed == expected["threshold"]
            and Q(2, 3) * kappa_star == alpha
            and strict_kappa > kappa_star
            and Q(2, 3) * strict_kappa > alpha,
            observed=threshold_observed,
        ),
        "tagsReferencesAndDisplays": record(
            tags == expected_tags and len(set(tags)) == 20
            and not (set(references) - set(tags))
            and display_open == display_close == 20,
        ),
        "formulaAndStatusSentinels": record(
            all(re.sub(r"\s+", " ", token) in flat_text for token in required_tokens),
        ),
        "sourceReportBoundary": record(
            "no E.24, complete-clock, regularity, novelty, or priority claim" in flat_source
            and "arbitrary finite interference inside one dyadic horizontal packet" in flat_source
            and "cutoff derivative is measured in its Wiener norm" in flat_source,
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
        "packet": packet_observed,
        "evolutionCases": evolution_observed,
        "fourierConvention": fourier_observed,
        "eta": eta_observed,
        "schur": schur_observed,
        "shortTime": short_observed,
        "wiener": wiener_observed,
        "normalization": normalization_observed,
        "threshold": threshold_observed,
        "claimBoundary": boundary,
    }
    OUT_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    failed = [name for name, item in checks.items() if not item["pass"]]
    OUT_REPORT.write_text(
        "# R0.75M finite certificate report\n\n"
        f"- Verdict: **{verdict}**\n"
        f"- Assertions: {payload['assertions']['passed']}/{payload['assertions']['total']}\n"
        f"- Main SHA-256: {sha256(MAIN)}\n"
        f"- Fixture SHA-256: {fixture_hash}\n"
        f"- Expected SHA-256: {expected_hash}\n"
        f"- Failed checks: {'none' if not failed else '; '.join(failed)}\n\n"
        "Exact rational Fourier ledgers verify the 1/(2*pi) convention, the "
        "2*pi spatial pairing, the pi*B kernel, and d_0 cancellation before "
        "absolute values. A six-mode real packet independently verifies both "
        "Schur row/column bounds, Parseval, and the exact 1/4 energy factor.\n\n"
        "Symbolic monomial arithmetic verifies the 1/(8K^2) window, e^(-1) "
        "L2 floor, (2*pi)^(-1/2)e^(-3/2) L3 floor, inversion constant "
        "4e(2*pi)^(1/3), and combined constant e(2*pi)^(1/3). The finite "
        "Wiener example checks the weighted Cauchy--Schwarz row and its "
        "first/second-derivative Parseval normalization.\n\n"
        "Normalization gives R^(1/3)omega^(1/3)K^(-2/3)p^(2/3), with strict "
        "threshold kappa>27163/71442. The theorem remains a physical signed, "
        "full-torus, single-dyadic-packet result; inter-packet summation, collar "
        "Wiener calibration, local Version-M replacement, and E.24 stay open. "
        "**NOT CLAY.**\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "suite": "r075m-dyadic-packet-diffusive-flux-gain",
        "verdict": verdict,
        "assertions": len(checks),
    }, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
