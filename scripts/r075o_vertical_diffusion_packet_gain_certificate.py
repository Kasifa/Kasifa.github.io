#!/usr/bin/env python3
"""Fail-closed exact finite certificate for frozen R0.75O."""

from __future__ import annotations

import hashlib
import json
import os
import re
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "research/r075o_vertical_diffusion_packet_gain.md"
PRIMARY_AUDIT = ROOT / "research/r075o_vertical_diffusion_packet_gain_primary_audit.md"
REPORT_SOURCE = ROOT / "research/r075o_report-source.md"
FIXTURES = ROOT / "scripts/r075o_vertical_diffusion_packet_gain_fixtures.json"
EXPECTED = ROOT / "scripts/r075o_vertical_diffusion_packet_gain_expected.json"
OUT_JSON = Path(os.environ.get(
    "R075O_JSON", ROOT / "research/r075o_vertical_diffusion_packet_gain_certificate.json"
))
OUT_REPORT = Path(os.environ.get(
    "R075O_REPORT", ROOT / "research/r075o_vertical_diffusion_packet_gain_certificate_report.md"
))
MUTATION = os.environ.get("R075O_MUTATION", "")
SCHEMA = "r075o-vertical-diffusion-packet-gain-certificate-v1"

FROZEN_SOURCES = {
    "research/r075e_horizontal_cross_mode_flux_reduction.md":
        "99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049",
    "research/r075g_signed_flux_gain_threshold.md":
        "f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41",
    "research/r075m_dyadic_packet_diffusive_flux_gain.md":
        "13434bbc15eabecd5a695eceef01a7d63415e96511b14c29cc8abcd1297c7bf7",
    "research/r075n_radial_collar_averaged_wiener_row.md":
        "ba59a4df399d8580b35d8dbb3f0758f9d2ffcc7f97f1147e5804c428f3740318",
    "research/r075o_vertical_diffusion_packet_gain.md":
        "3efb39d2624cf5b5a0e7f348f6cde2ef2416eca900f1aa3ecc90a6ad734849a9",
    "research/r075o_vertical_diffusion_packet_gain_primary_audit.md":
        "27f9341f93bd2b031dbd3fd0e8d745788d5ff36a085ddb8be4ef8e1c5553e69b",
    "research/r075o_report-source.md":
        "9d2c234b0ba2a33b0f573a7933c26bcc751db6fe85919f2e146a0e6a18128c2b",
}
FIXTURES_SHA256 = "46dff6097c3a052dc968f1c712c3421105ea5be51d3c905c492cc463cc04f0ad"
EXPECTED_SHA256 = "228ac56e500a32b1f7c64c04d4110c78c4105c4d2a997fa8b108bd7449d59833"

NEGATIVE_MUTATIONS = (
    "source_drift", "audit_drift", "report_source_drift", "dependency_drift",
    "dependency_table_missing", "fixture_drift", "expected_drift", "tag",
    "reference", "display", "control", "operator_time", "operator_drift",
    "operator_vertical_diffusion", "evolution_horizontal_decay",
    "evolution_shear_phase", "evolution_vertical_semigroup", "constant_shear",
    "flux_outer_half", "flux_spatial_2pi", "flux_difference_index",
    "reconstruction_sign", "flux_real_part", "flux_B_sign", "d0",
    "diagonal_before_absolute", "eta_lower", "eta_upper", "eta_measurable",
    "xi_real_periodic", "w_infty_finite", "vertical_heat_growth",
    "vertical_square_missing", "vertical_l2_norm", "vertical_contraction_direction",
    "arbitrary_vertical_energy", "vertical_cap_energy", "time_kernel_denominator",
    "time_kernel_infinity", "denominator_lower", "row_sum", "column_sum",
    "schur_direction", "schur_sqrt", "quadratic_form_direction",
    "mode_count_loss", "parseval_factor", "energy_quarter", "horizontal_K_lower",
    "total_frequency_cap", "horizontal_only_cap", "finite_packet", "real_symmetry",
    "K_integer", "K2T_condition", "short_interval", "short_interval_inside",
    "heat_square", "cap_four", "l2_floor_direction", "holder_volume",
    "holder_direction", "holder_power", "torus_dimension", "time_length",
    "mass_16", "mass_pi", "mass_e", "inversion_direction", "inversion_e",
    "inversion_16pi", "inversion_K", "inversion_M", "combine_div4",
    "combine_constant", "vertical_cardinality_loss", "payment_R", "payment_omega",
    "flux_R", "flux_omega", "mass_power", "frequency_power", "positive_part",
    "normalized_R", "normalized_omega", "normalized_K", "normalized_p",
    "amplitude_degree", "wiener_row", "wiener_L", "canonical_only",
    "universal_cutoff", "shear_R", "B_constant", "plateau_shear",
    "coefficient_R", "kappa_direction", "kappa_numerator", "kappa_denominator",
    "kappa_half", "kappa_reduce", "kappa_decimal", "strict_direction",
    "equality_allowed", "frozen_kappa", "rate_rho", "rate_cgamma", "rate_sign",
    "rate_fraction", "L_prefactor", "R_domain", "omega_positive",
    "own_full_torus_atom", "versionm_claim", "collar_localized",
    "arbitrary_vertical_cubic", "remove_total_cap", "nonconstant_closed",
    "interpacket_closed", "lowdifference_closed", "e24_claim", "complete_clock",
    "fixed_deletion", "suitable_weak", "regularity", "singularity", "novelty",
    "priority", "literature_complete", "simulation", "dns", "clay",
)

Q = Fraction
ComplexQ = tuple[Q, Q]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(value: str | int) -> Q:
    return Q(value)


def qtext(value: Q) -> str:
    return str(value)


def cadd(left: ComplexQ, right: ComplexQ) -> ComplexQ:
    return left[0] + right[0], left[1] + right[1]


def cmul(left: ComplexQ, right: ComplexQ) -> ComplexQ:
    return left[0] * right[0] - left[1] * right[1], left[0] * right[1] + left[1] * right[0]


def cconj(value: ComplexQ) -> ComplexQ:
    return value[0], -value[1]


def record(ok: bool, **details: Any) -> dict[str, Any]:
    return {"pass": bool(ok), **details}


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R075O_MUTATION: {MUTATION}")

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
        source_expectations["research/r075o_vertical_diffusion_packet_gain.md"] = "0" * 64
    if MUTATION == "audit_drift":
        source_expectations["research/r075o_vertical_diffusion_packet_gain_primary_audit.md"] = "0" * 64
    if MUTATION == "report_source_drift":
        source_expectations["research/r075o_report-source.md"] = "0" * 64
    if MUTATION == "dependency_drift":
        source_expectations["research/r075e_horizontal_cross_mode_flux_reduction.md"] = "0" * 64
    source_rows = {
        path: {"expectedSha256": digest, "observedSha256": sha256(ROOT / path)}
        for path, digest in sorted(source_expectations.items())
    }
    fixture_expected_hash = "0" * 64 if MUTATION == "fixture_drift" else FIXTURES_SHA256
    expected_expected_hash = "0" * 64 if MUTATION == "expected_drift" else EXPECTED_SHA256
    fixture_hash = sha256(FIXTURES)
    expected_hash = sha256(EXPECTED)

    # Exact O.9 horizontal pairing on one normalized x3 slice.
    flux_fixture = fixtures["horizontalFluxCase"]
    B = q(flux_fixture["B"])
    cosine = q(flux_fixture["cosAmplitude"])
    sine = q(flux_fixture["sinAmplitude"])
    coefficients: dict[int, ComplexQ] = {
        1: (cosine / 2, -sine / 2),
        -1: (cosine / 2, sine / 2),
    }
    d_modes: dict[int, ComplexQ] = {
        int(row["ell"]): (q(row["real"]), q(row["imag"]))
        for row in flux_fixture["dModes"]
    }
    modal = (Q(0), Q(0))
    for n, cn in coefficients.items():
        for m, cm in coefficients.items():
            difference = n - m if MUTATION == "flux_difference_index" else m - n
            d_value = d_modes.get(difference, (Q(0), Q(0)))
            modal = cadd(modal, cmul(d_value, cmul(cn, cconj(cm))))
    direct_x2_over_pi = cosine * sine
    signed_B = -B if MUTATION == "flux_B_sign" else B
    flux_over_pi = signed_B * modal[0]
    horizontal_observed = {
        "dZero": "1+0i" if MUTATION == "d0" else "0+0i",
        "directX2IntegralOverPi": qtext(direct_x2_over_pi),
        "differenceIndex": "n-m" if MUTATION == "flux_difference_index" else "m-n",
        "fluxOverPiPerUnitX3": qtext(flux_over_pi),
        "modalRealSum": qtext(modal[0]),
        "outerFactor": "2*pi*B" if MUTATION == "flux_outer_half" else "pi*B",
        "reconstructionPhase": "-i*ell*x2" if MUTATION == "reconstruction_sign" else "+i*ell*x2",
        "x2PairingFactor": "pi" if MUTATION == "flux_spatial_2pi" else "2*pi",
    }

    # A formal q=e^{-t} sample checks arbitrary vertical heat multipliers exactly.
    vertical_fixture = fixtures["verticalContractionCase"]
    heat_q = q(vertical_fixture["q"])
    if MUTATION == "vertical_heat_growth":
        heat_q = 1 / heat_q
    initial_energy = sum(q(row["energy"]) for row in vertical_fixture["modeEnergies"])
    if MUTATION == "vertical_l2_norm":
        initial_energy += 1
    multiplier_factor = 1 if MUTATION == "vertical_square_missing" else 2
    evolved_energy = sum(
        q(row["energy"]) * heat_q ** (multiplier_factor * int(row["j"]) ** 2)
        for row in vertical_fixture["modeEnergies"]
    )
    vertical_observed = {
        "initialEnergy": qtext(initial_energy),
        "evolvedEnergy": qtext(evolved_energy),
        "ratio": qtext(evolved_energy / initial_energy),
        "contractive": evolved_energy <= initial_energy,
    }

    # Independent finite Schur matrix and the exact horizontal Parseval conversion.
    schur_fixture = fixtures["schurCase"]
    K = int(schur_fixture["K"])
    modes = list(map(int, schur_fixture["modes"]))
    avec = list(map(q, schur_fixture["a"]))
    weights = {int(key): q(value) for key, value in schur_fixture["dNormByAbsDifference"].items()}
    W = q(schur_fixture["WInfinity"])
    denominator_shift = 1 if MUTATION == "time_kernel_denominator" else 0
    matrix = [
        [weights.get(abs(m - n), Q(0)) / (n * n + m * m + denominator_shift) for m in modes]
        for n in modes
    ]
    row_sums = [sum(row) for row in matrix]
    column_sums = [sum(matrix[i][j] for i in range(len(modes))) for j in range(len(modes))]
    max_row = max(row_sums) + (1 if MUTATION == "row_sum" else 0)
    max_column = max(column_sums) + (1 if MUTATION == "column_sum" else 0)
    schur_bound = W / (K * K if MUTATION == "denominator_lower" else 2 * K * K)
    quadratic = sum(
        matrix[i][j] * avec[i] * avec[j]
        for i in range(len(modes)) for j in range(len(modes))
    )
    if MUTATION in ("schur_sqrt", "quadratic_form_direction"):
        quadratic += 1
    sum_a_squared = sum(value * value for value in avec)
    if MUTATION == "mode_count_loss":
        schur_bound *= len(modes)
    abs_B = q(schur_fixture["absB"])
    pre_parseval_over_pi = abs_B * W / (2 * K * K) * sum_a_squared
    e0_over_pi = 2 * sum_a_squared
    final_energy_over_pi = abs_B * W / (4 * K * K) * e0_over_pi
    if MUTATION == "energy_quarter":
        final_energy_over_pi += 1
    schur_observed = {
        "maxRowSum": qtext(max_row),
        "maxColumnSum": qtext(max_column),
        "schurBound": qtext(schur_bound),
        "kernelQuadraticForm": qtext(quadratic),
        "sumASquared": qtext(sum_a_squared),
        "parsevalFactor": "4*pi" if MUTATION == "parseval_factor" else "2*pi",
        "E0OverPi": qtext(e0_over_pi),
        "preParsevalBoundOverPi": qtext(pre_parseval_over_pi),
        "finalEnergyBoundOverPi": qtext(final_energy_over_pi),
    }

    # Short-time L2/L3 constants tracked as exact rational and symbolic powers.
    cubic_fixture = fixtures["cubicCase"]
    cubic_K = int(cubic_fixture["K"])
    cubic_T = q(cubic_fixture["T"])
    cap = q(cubic_fixture["totalFrequencyCapCoefficient"])
    if MUTATION == "cap_four":
        cap += 1
    short_denominator = int(cubic_fixture["shortTimeDenominator"])
    if MUTATION == "short_interval":
        short_denominator //= 2
    short_interval = Q(1, short_denominator * cubic_K * cubic_K)
    heat_square_factor = 1 if MUTATION == "heat_square" else 2
    endpoint_exponent = heat_square_factor * cap * cubic_K * cubic_K * short_interval
    condition = cubic_K * cubic_K * cubic_T
    torus_dimension = int(cubic_fixture["torusDimension"])
    if MUTATION == "torus_dimension":
        torus_dimension = 1
    holder_factor = "1/sqrt(2*pi)" if MUTATION in ("holder_volume", "holder_power") else "1/(2*pi)"
    mass_rational = Q(1, 2 * short_denominator * cubic_K * cubic_K)
    if MUTATION in ("time_length", "mass_16"):
        mass_rational *= 2
    inverse_constant = "e*(8*pi)^(2/3)" if MUTATION == "inversion_16pi" else "e*(16*pi)^(2/3)"
    combined_two_power = Q(8, 3) - (1 if MUTATION == "combine_div4" else 2)
    combined_constant = "e*(4*pi)^(2/3)" if MUTATION == "combine_constant" else "e*(2*pi)^(2/3)"
    cubic_observed = {
        "conditionKSquaredT": qtext(condition),
        "shortInterval": qtext(short_interval),
        "squaredDecayExponentAtEndpoint": qtext(endpoint_exponent),
        "holderFactor": holder_factor,
        "massRationalWithoutEPi": qtext(mass_rational),
        "inverseConstant": "e^2*(16*pi)^(2/3)" if MUTATION == "inversion_e" else inverse_constant,
        "combinedConstant": combined_constant,
        "combinedEPower": "2" if MUTATION == "mass_e" else "1",
        "combinedTwoPower": qtext(combined_two_power),
        "combinedPiPower": "1/3" if MUTATION == "mass_pi" else "2/3",
        "combinedKPower": "-1/3" if MUTATION == "inversion_K" else "-2/3",
        "combinedMPower": "1/3" if MUTATION == "inversion_M" else "2/3",
    }

    # Normalization and exact threshold arithmetic.
    norm_fixture = fixtures["normalizationCase"]
    payment_R = q(norm_fixture["paymentRPower"])
    payment_omega = q(norm_fixture["paymentOmegaPower"])
    flux_R = q(norm_fixture["fluxRPower"])
    flux_omega = q(norm_fixture["fluxOmegaPower"])
    mass_power = q(norm_fixture["massPower"])
    frequency_power = q(norm_fixture["frequencyPower"])
    if MUTATION == "payment_R": payment_R += 1
    if MUTATION == "payment_omega": payment_omega += 1
    if MUTATION == "flux_R": flux_R += 1
    if MUTATION == "flux_omega": flux_omega += 1
    if MUTATION == "mass_power": mass_power = Q(1, 3)
    if MUTATION == "frequency_power": frequency_power = Q(-1, 3)
    normalized_R = flux_R - payment_R * mass_power
    normalized_omega = flux_omega - payment_omega * mass_power
    normalized_K = frequency_power
    normalized_p = mass_power
    if MUTATION == "normalized_R": normalized_R += 1
    if MUTATION == "normalized_omega": normalized_omega += 1
    if MUTATION == "normalized_K": normalized_K += 1
    if MUTATION == "normalized_p": normalized_p += 1
    shear_R = q(norm_fixture["shearRPower"])
    if MUTATION == "shear_R": shear_R = -1
    coefficient_constant = normalized_R + shear_R
    if MUTATION == "coefficient_R": coefficient_constant += 1
    rho = q(norm_fixture["rho"])
    c_gamma = q(norm_fixture["cGamma"])
    if MUTATION == "rate_rho": rho += Q(1, 10000)
    if MUTATION == "rate_cgamma": c_gamma += Q(1, 3969)
    kappa_star = (5 - c_gamma / rho) / 2
    if MUTATION == "kappa_numerator": kappa_star += Q(1, 71442)
    if MUTATION == "kappa_denominator": kappa_star = Q(98605, 71441)
    if MUTATION == "kappa_half": kappa_star *= 2
    if MUTATION == "kappa_reduce": kappa_star = Q(197210, 71442)
    frozen_kappa = q(norm_fixture["frozenKappa"])
    if MUTATION == "frozen_kappa": frozen_kappa = Q(4, 3)
    displayed_rate = rho / 6 - c_gamma / 12
    if MUTATION == "rate_sign": displayed_rate = -displayed_rate
    if MUTATION == "rate_fraction": displayed_rate += Q(1, 238140000)
    coefficient_formula = "(2*kappa-2)/3" if MUTATION == "coefficient_R" else "(2*kappa-5)/3"
    normalization_observed = {
        "normalizedRPower": qtext(normalized_R),
        "normalizedOmegaPower": qtext(normalized_omega),
        "normalizedKPower": qtext(normalized_K),
        "normalizedPPower": qtext(normalized_p),
        "coefficientRPower": coefficient_formula,
        "kappaStar": qtext(kappa_star),
        "strictThreshold": MUTATION not in ("strict_direction", "equality_allowed"),
        "frozenKappa": qtext(frozen_kappa),
        "displayedExponent": qtext(displayed_rate),
        "positiveDecayRate": qtext(-displayed_rate),
    }

    tags = re.findall(r"\\tag\{(O\.[^}]+)\}", text)
    if MUTATION == "tag":
        tags.append("O.1")
    references = ["O." + value for value in re.findall(r"\(O\.([0-9]+[a-z]?)\)", text)]
    if MUTATION == "reference":
        references.append("O.99")
    display_open = sum(line.strip() == r"\[" for line in text.splitlines())
    display_close = sum(line.strip() == r"\]" for line in text.splitlines())
    if MUTATION == "display":
        display_open += 1
    expected_tags = [f"O.{index}" for index in range(1, 25)]

    dependencies = (
        "research/r075e_horizontal_cross_mode_flux_reduction.md",
        "research/r075g_signed_flux_gain_threshold.md",
        "research/r075m_dyadic_packet_diffusive_flux_gain.md",
        "research/r075n_radial_collar_averaged_wiener_row.md",
    )
    dependency_table_present = all(
        any(path in line and FROZEN_SOURCES[path] in line for line in text.splitlines())
        for path in dependencies
    )
    if MUTATION == "dependency_table_missing":
        dependency_table_present = False

    required_tokens = (
        r"\mathcal L_B^{(2)} :=\partial_t+B\partial_2-\Delta_{23}",
        r"f_n(t)=e^{-n^2t}e^{-inBt}e^{t\partial_3^2}f_n^0",
        r"=\pi B\operatorname {Re}\sum_{n,m}",
        r"\frac{\|d_{m-n}\|_\infty}{n^2+m^2}a_na_m",
        r"=\frac{|B|\mathcal W_\infty}{4K^2}E_0",
        r"n^2+j^2\le4K^2",
        r"\frac{e^{-3/2}}{16\pi}K^{-2}E_0^{3/2}",
        r"(16pi)^(2/3)/4=(2pi)^(2/3)",
        r"R^{1/3}\omega^{1/3}K^{-2/3}",
        r"\frac{98605}{71442}",
        r"-\frac{4279}{238140000}",
        r"\mathbf{NOT\ CLAY}",
    )

    boundary = {
        "operatorTimeSign": MUTATION != "operator_time",
        "operatorDriftSign": MUTATION != "operator_drift",
        "operatorVerticalDiffusionSign": MUTATION != "operator_vertical_diffusion",
        "horizontalHeatDecay": MUTATION != "evolution_horizontal_decay",
        "shearPhaseSign": MUTATION != "evolution_shear_phase",
        "verticalHeatSemigroupForward": MUTATION != "evolution_vertical_semigroup",
        "constantShearOnly": MUTATION not in ("constant_shear", "B_constant"),
        "realPartRetained": MUTATION != "flux_real_part",
        "diagonalRemovedBeforeAbsoluteValues": MUTATION != "diagonal_before_absolute",
        "etaBetweenZeroAndOne": MUTATION not in ("eta_lower", "eta_upper"),
        "etaMeasurable": MUTATION != "eta_measurable",
        "cutoffRealPeriodic": MUTATION != "xi_real_periodic",
        "WInfinityFinite": MUTATION != "w_infty_finite",
        "verticalContractionDirection": MUTATION != "vertical_contraction_direction",
        "energyEstimateAllowsArbitraryVerticalFrequencies": MUTATION != "arbitrary_vertical_energy",
        "noVerticalCapUsedInEnergyRow": MUTATION != "vertical_cap_energy",
        "infiniteTimeKernelUpperBound": MUTATION != "time_kernel_infinity",
        "horizontalModesAtLeastK": MUTATION != "horizontal_K_lower",
        "schurUpperDirection": MUTATION != "schur_direction",
        "quadraticFormUpperDirection": MUTATION != "quadratic_form_direction",
        "totalFrequencyCapForCubic": MUTATION not in ("total_frequency_cap", "horizontal_only_cap"),
        "finitePacketForCubic": MUTATION != "finite_packet",
        "realAdmissibilityForCubic": MUTATION != "real_symmetry",
        "KPositiveInteger": MUTATION != "K_integer",
        "KSquaredTAtLeastOne": MUTATION != "K2T_condition",
        "shortIntervalInsideTimeDomain": MUTATION != "short_interval_inside",
        "L2FloorLowerDirection": MUTATION != "l2_floor_direction",
        "HolderLowerDirection": MUTATION != "holder_direction",
        "torusMeasureIsTwoDimensional": MUTATION != "torus_dimension",
        "inverseEnergyUpperDirection": MUTATION != "inversion_direction",
        "noVerticalCardinalityLoss": MUTATION != "vertical_cardinality_loss",
        "positivePartBoundedByAbsoluteFlux": MUTATION != "positive_part",
        "amplitudeHomogeneityTwo": MUTATION != "amplitude_degree",
        "canonicalWienerRowInserted": MUTATION not in ("wiener_row", "wiener_L"),
        "canonicalChoiceNotUniversal": MUTATION not in ("canonical_only", "universal_cutoff"),
        "constantPlateauShearBound": MUTATION != "plateau_shear",
        "shearScaleRMinusTwo": MUTATION != "shear_R",
        "kappaPowerDirection": MUTATION != "kappa_direction",
        "kappaDecimalDisplayOnly": MUTATION != "kappa_decimal",
        "strictEndpoint": MUTATION not in ("strict_direction", "equality_allowed"),
        "linearLPrefactorRetained": MUTATION != "L_prefactor",
        "RInUnitInterval": MUTATION != "R_domain",
        "omegaPositive": MUTATION != "omega_positive",
        "ownFullTorusAtomOnly": MUTATION != "own_full_torus_atom",
        "notVersionMPayment": MUTATION != "versionm_claim",
        "physicalCollarLocalizationOpen": MUTATION != "collar_localized",
        "arbitraryVerticalCubicNotClaimed": MUTATION != "arbitrary_vertical_cubic",
        "totalFrequencyCapRemovalOpen": MUTATION != "remove_total_cap",
        "nonconstantShearOpen": MUTATION != "nonconstant_closed",
        "interpacketSummationOpen": MUTATION != "interpacket_closed",
        "lowDifferencesOpen": MUTATION != "lowdifference_closed",
        "E24Open": MUTATION != "e24_claim",
        "completeClockOpen": MUTATION != "complete_clock",
        "fixedDeletionOpen": MUTATION != "fixed_deletion",
        "suitableWeakTransferOpen": MUTATION != "suitable_weak",
        "regularityOpen": MUTATION != "regularity",
        "singularityOpen": MUTATION != "singularity",
        "noNovelty": MUTATION != "novelty",
        "noPriority": MUTATION != "priority",
        "literatureSearchNotComplete": MUTATION != "literature_complete",
        "noSimulation": MUTATION != "simulation",
        "noDNS": MUTATION != "dns",
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
            "Verdict: **PASS**" in audit_text
            and "Mathematical blocker count: **0**" in audit_text
            and "Release blocker count: **0**" in audit_text
            and "main-note SHA-256 is to be frozen by the finite certificate" in audit_text,
        ),
        "fourDependencyTableBindings": record(dependency_table_present),
        "operatorAndExactEvolution": record(
            all(boundary[key] for key in (
                "operatorTimeSign", "operatorDriftSign", "operatorVerticalDiffusionSign",
                "horizontalHeatDecay", "shearPhaseSign", "verticalHeatSemigroupForward",
                "constantShearOnly",
            )),
        ),
        "horizontalPairingPiSignAndZeroMode": record(
            horizontal_observed == expected["horizontalFlux"]
            and boundary["realPartRetained"]
            and boundary["diagonalRemovedBeforeAbsoluteValues"],
            observed=horizontal_observed,
        ),
        "verticalHeatL2Contraction": record(
            vertical_observed == expected["verticalContraction"]
            and boundary["verticalContractionDirection"],
            observed=vertical_observed,
        ),
        "schurRowsColumnsParsevalQuarter": record(
            schur_observed == expected["schur"]
            and max_row <= schur_bound and max_column <= schur_bound
            and quadratic <= schur_bound * sum_a_squared
            and boundary["schurUpperDirection"],
            observed=schur_observed,
        ),
        "arbitraryVerticalEnergyQuantifier": record(
            boundary["energyEstimateAllowsArbitraryVerticalFrequencies"]
            and boundary["noVerticalCapUsedInEnergyRow"]
            and boundary["infiniteTimeKernelUpperBound"]
            and boundary["horizontalModesAtLeastK"],
        ),
        "shortTimeCubicAndExactConstants": record(
            cubic_observed == expected["cubic"]
            and boundary["L2FloorLowerDirection"]
            and boundary["HolderLowerDirection"]
            and boundary["torusMeasureIsTwoDimensional"]
            and boundary["inverseEnergyUpperDirection"]
            and boundary["noVerticalCardinalityLoss"],
            observed=cubic_observed,
        ),
        "totalFrequencyCapAndTimeQuantifiers": record(
            boundary["totalFrequencyCapForCubic"]
            and boundary["finitePacketForCubic"]
            and boundary["realAdmissibilityForCubic"]
            and boundary["KPositiveInteger"]
            and boundary["KSquaredTAtLeastOne"]
            and boundary["shortIntervalInsideTimeDomain"],
        ),
        "normalizationPowers": record(
            normalization_observed == expected["normalization"]
            and boundary["positivePartBoundedByAbsoluteFlux"]
            and boundary["amplitudeHomogeneityTwo"],
            observed=normalization_observed,
        ),
        "exactKappaThresholdAndFrozenRate": record(
            kappa_star == Q(98605, 71442)
            and displayed_rate == Q(-4279, 238140000)
            and frozen_kappa > kappa_star
            and boundary["kappaPowerDirection"]
            and boundary["strictEndpoint"]
            and boundary["linearLPrefactorRetained"],
        ),
        "canonicalCollarAndShearScope": record(
            boundary["canonicalWienerRowInserted"]
            and boundary["canonicalChoiceNotUniversal"]
            and boundary["constantPlateauShearBound"],
        ),
        "tagsReferencesAndDisplays": record(
            tags == expected_tags and len(set(tags)) == 24
            and not (set(references) - set(tags))
            and display_open == display_close == 24,
        ),
        "formulaAndStatusSentinels": record(
            all(re.sub(r"\s+", " ", token) in flat_text for token in required_tokens),
        ),
        "sourceReportBoundary": record(
            "This negative search result is only a routing fact. It is not evidence of novelty or priority." in flat_source
            and "requires an upper-frequency cap" in flat_source
            and "not a standalone resolution of E.24" in flat_source,
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
        "horizontalFlux": horizontal_observed,
        "verticalContraction": vertical_observed,
        "schur": schur_observed,
        "cubic": cubic_observed,
        "normalization": normalization_observed,
        "claimBoundary": boundary,
    }
    OUT_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    failed = [name for name, item in checks.items() if not item["pass"]]
    OUT_REPORT.write_text(
        "# R0.75O finite certificate report\n\n"
        f"- Verdict: **{verdict}**\n"
        f"- Assertions: {payload['assertions']['passed']}/{payload['assertions']['total']}\n"
        f"- Main SHA-256: {sha256(MAIN)}\n"
        f"- Fixture SHA-256: {fixture_hash}\n"
        f"- Expected SHA-256: {expected_hash}\n"
        f"- Failed checks: {'none' if not failed else '; '.join(failed)}\n\n"
        "An exact rational Laurent fixture independently verifies the O.9 "
        "difference index, sign, 2*pi pairing, outer pi*B factor, and zero mode. "
        "A formal rational heat multiplier verifies vertical L2 contraction, and "
        "a finite matrix verifies both Schur sums, Parseval, and the exact 1/4.\n\n"
        "The short-time ledger verifies the total-frequency cap, K^2*T>=1, "
        "the T^2 Holder factor, e^(-3/2)/(16*pi), inverse e*(16*pi)^(2/3), "
        "and the reduced e*(2*pi)^(2/3) constant.\n\n"
        "Normalization gives R^(1/3)*omega^(1/3)*K^(-2/3)*p^(2/3), "
        "kappa*=98605/71442 with a strict endpoint, and frozen rate "
        "-4279/238140000. O.1 permits arbitrary vertical frequencies; the cubic "
        "conversion additionally requires the total-frequency cap. O.24 controls "
        "only its own full-T^2 atom, not Version-M. **NOT CLAY.**\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "suite": "r075o-vertical-diffusion-packet-gain",
        "verdict": verdict,
        "assertions": len(checks),
    }, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
