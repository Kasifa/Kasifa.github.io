#!/usr/bin/env python3
"""Fail-closed exact finite certificate for frozen R0.75I."""

from __future__ import annotations

import hashlib
import json
import os
import re
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "research/r075i_diffusion_safe_block_participation.md"
PRIMARY_AUDIT = ROOT / "research/r075i_diffusion_safe_block_participation_primary_audit.md"
REPORT_SOURCE = ROOT / "research/r075i_report-source.md"
FIXTURES = ROOT / "scripts/r075i_diffusion_safe_block_participation_fixtures.json"
EXPECTED = ROOT / "scripts/r075i_diffusion_safe_block_participation_expected.json"
OUT_JSON = Path(os.environ.get(
    "R075I_JSON",
    ROOT / "research/r075i_diffusion_safe_block_participation_certificate.json",
))
OUT_REPORT = Path(os.environ.get(
    "R075I_REPORT",
    ROOT / "research/r075i_diffusion_safe_block_participation_certificate_report.md",
))
MUTATION = os.environ.get("R075I_MUTATION", "")
SCHEMA = "r075i-diffusion-safe-block-participation-certificate-v1"

FROZEN_SOURCES = {
    "research/r075b_bulk_clock_outer_padding_gate.md":
        "430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a",
    "research/r075c_background_shear_packing_false_positive.md":
        "1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89",
    "research/r075e_horizontal_cross_mode_flux_reduction.md":
        "99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049",
    "research/r075g_signed_flux_gain_threshold.md":
        "f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41",
    "research/r075h_single_pass_transport_flux_closure.md":
        "849379bea9cf22e0d892ac11ac05bb3b3bc2967a1735753dbc4a6ffc7bb7d7b9",
    "research/r075i_diffusion_safe_block_participation.md":
        "c8511690dc52988b3f3715e589379c72dae0a892dcabd8d0ca218dddbe0fd3a7",
    "research/r075i_diffusion_safe_block_participation_primary_audit.md":
        "a8e481bfa28ba244a6022b782880ce9a86c40de29e3b0064474841eca99cecbd",
    "research/r075i_report-source.md":
        "8459adb6735caa2ee6c6e9c27202125cda34ad9072e2d78167f3f961e34f5de3",
}
FIXTURES_SHA256 = "afda306afcf26640be72978b654a1a7dd1b23c0df5e92137f450520a6c7d515b"
EXPECTED_SHA256 = "27514a38beec5c5e949a2a639faa5db539a4fbdeefec175e9e6e90a0507afd2a"

NEGATIVE_MUTATIONS = (
    "source_drift", "audit_drift", "report_source_drift", "dependency_drift",
    "dependency_table_missing", "fixture_drift", "expected_drift", "tag",
    "reference", "display", "control", "block_time_r", "support_l",
    "support_r", "cylinder_measure", "b_r", "cutoff_r",
    "pointwise_coefficient", "measure_third_l", "measure_third_r",
    "cubic_r", "cubic_omega", "cubic_p", "normalization_r",
    "normalization_omega", "final_l", "holder_cell_measure",
    "holder_l2_power", "holder_l3_power", "holder_direction",
    "cubic_atom_r", "cubic_atom_omega", "transport_half",
    "one_block_direction", "participation_power", "neff_numerator",
    "neff_denominator", "neff_zero", "neff_lower_direction",
    "neff_upper_direction", "aggregation_identity", "unequal_as_count",
    "equal_mass_count", "aggregate_positive_part", "aggregate_absolute_sum",
    "aggregate_direction", "payment_pa_direction", "payment_pf_direction",
    "payment_power", "payment_upper_use", "rho_sign", "cgamma_sign",
    "theta_ratio", "theta_offset", "theta_strict", "beta_complement",
    "beta_strict", "one_rate_fraction", "uniform_theta",
    "uniform_rate_fraction", "endpoint_polynomial", "zero_mode_mean",
    "zero_mode_flux", "zero_mode_payment", "zero_mode_neff", "pde_required",
    "diffusion_unsafe", "participation_proved", "participation_necessary",
    "high_neff_counterexample", "uniform_counterexample",
    "signed_alternative_closed", "transition_closed", "recrossing_closed",
    "e24_closed", "complete_clock", "fixed_deletion", "suitable_weak",
    "regularity", "singularity", "novelty", "simulation_used", "clay",
)

Q = Fraction
Vector = dict[str, Q]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(value: str | int) -> Q:
    return Q(value)


def qtext(value: Q) -> str:
    return str(value)


def vector_add(*vectors: Vector) -> Vector:
    keys = sorted(set().union(*(vector.keys() for vector in vectors)))
    return {key: sum(vector.get(key, Q(0)) for vector in vectors) for key in keys}


def vector_scale(vector: Vector, scale: Q) -> Vector:
    return {key: value * scale for key, value in vector.items()}


def vector_json(vector: Vector) -> dict[str, str]:
    return {key: qtext(value) for key, value in vector.items()}


def exact_integer_cuberoot(value: int) -> int:
    if value < 0:
        return -exact_integer_cuberoot(-value)
    root = 0
    while (root + 1) ** 3 <= value:
        root += 1
    if root ** 3 != value:
        raise ValueError(f"not a perfect cube: {value}")
    return root


def exact_cuberoot(value: Q) -> Q:
    if value < 0:
        raise ValueError("participation payments must be nonnegative")
    return Q(
        exact_integer_cuberoot(value.numerator),
        exact_integer_cuberoot(value.denominator),
    )


def record(ok: bool, **details: Any) -> dict[str, Any]:
    return {"pass": bool(ok), **details}


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R075I_MUTATION: {MUTATION}")

    text = MAIN.read_text(encoding="utf-8")
    audit_text = PRIMARY_AUDIT.read_text(encoding="utf-8")
    source_text = REPORT_SOURCE.read_text(encoding="utf-8")
    flat_text = re.sub(r"\s+", " ", text)
    scan_text = text + audit_text + source_text
    if MUTATION == "control":
        scan_text += "\x01"
    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))

    source_expectations = dict(FROZEN_SOURCES)
    if MUTATION == "source_drift":
        source_expectations[
            "research/r075i_diffusion_safe_block_participation.md"
        ] = "0" * 64
    if MUTATION == "audit_drift":
        source_expectations[
            "research/r075i_diffusion_safe_block_participation_primary_audit.md"
        ] = "0" * 64
    if MUTATION == "report_source_drift":
        source_expectations["research/r075i_report-source.md"] = "0" * 64
    if MUTATION == "dependency_drift":
        source_expectations[
            "research/r075c_background_shear_packing_false_positive.md"
        ] = "0" * 64
    source_rows = {
        path: {"expectedSha256": digest, "observedSha256": sha256(ROOT / path)}
        for path, digest in sorted(source_expectations.items())
    }
    fixture_expected_hash = "0" * 64 if MUTATION == "fixture_drift" else FIXTURES_SHA256
    expected_expected_hash = "0" * 64 if MUTATION == "expected_drift" else EXPECTED_SHA256
    fixture_hash = sha256(FIXTURES)
    expected_hash = sha256(EXPECTED)

    # I.5--I.13: derive every Laurent exponent rather than checking only the
    # final displayed row.
    zero = {"L": Q(0), "R": Q(0), "omega": Q(0), "p": Q(0)}
    block_time = dict(zero)
    block_time["R"] = Q(2) if MUTATION == "block_time_r" else Q(3)
    support = dict(zero)
    support["L"] = Q(1) if MUTATION == "support_l" else Q(2)
    support["R"] = Q(2) if MUTATION == "support_r" else Q(3)
    cylinder = vector_add(block_time, support)
    if MUTATION == "cylinder_measure":
        cylinder["R"] += 1
    b_bound = dict(zero)
    b_bound["R"] = Q(-1) if MUTATION == "b_r" else Q(-2)
    cutoff_bound = dict(zero)
    cutoff_bound["R"] = Q(1) if MUTATION == "cutoff_r" else Q(-1)
    pointwise = vector_add(b_bound, cutoff_bound)
    if MUTATION == "pointwise_coefficient":
        pointwise["R"] += 1
    measure_third = vector_scale(cylinder, Q(1, 3))
    if MUTATION == "measure_third_l":
        measure_third["L"] = Q(1, 3)
    if MUTATION == "measure_third_r":
        measure_third["R"] = Q(1)
    cubic_base = {"L": Q(0), "R": Q(2), "omega": Q(-1), "p": Q(1)}
    cubic_two_thirds = vector_scale(cubic_base, Q(2, 3))
    if MUTATION == "cubic_r":
        cubic_two_thirds["R"] = Q(2, 3)
    if MUTATION == "cubic_omega":
        cubic_two_thirds["omega"] = Q(2, 3)
    if MUTATION == "cubic_p":
        cubic_two_thirds["p"] = Q(1, 3)
    normalization = dict(zero)
    normalization["R"] = Q(1) if MUTATION == "normalization_r" else Q(-1)
    normalization["omega"] = Q(0) if MUTATION == "normalization_omega" else Q(1)
    final_product = vector_add(
        normalization, pointwise, measure_third, cubic_two_thirds
    )
    if MUTATION == "final_l":
        final_product["L"] += Q(1, 3)
    exponent_observed = {
        "blockTime": vector_json(block_time),
        "supportVolume": vector_json(support),
        "cylinderMeasure": vector_json(cylinder),
        "pointwiseCoefficient": vector_json(pointwise),
        "measureOneThird": vector_json(measure_third),
        "cubicTwoThirds": vector_json(cubic_two_thirds),
        "fluxNormalization": vector_json(normalization),
        "finalProduct": vector_json(final_product),
    }

    # Nonconstant, nondegenerate rational two-cell Holder fixture.
    holder = fixtures["oneBlockHolderCase"]
    hr = q(holder["R"])
    hl = q(holder["L"])
    homega = q(holder["omega"])
    htime = q(holder["timeLength"])
    hsupport = q(holder["supportVolume"])
    measures = [q(value) for value in holder["cellMeasures"]]
    if MUTATION == "holder_cell_measure":
        measures[0] += Q(1, 64)
    values = [q(value) for value in holder["fieldValues"]]
    l2_power = 1 if MUTATION == "holder_l2_power" else 2
    l3_power = 2 if MUTATION == "holder_l3_power" else 3
    l2_integral = sum(measure * value ** l2_power for measure, value in zip(measures, values))
    l3_integral = sum(measure * value ** l3_power for measure, value in zip(measures, values))
    cylinder_measure = sum(measures)
    holder_left_cubed = l2_integral ** 3
    holder_right_cubed = cylinder_measure * l3_integral ** 2
    cubic_r_power = 2 if MUTATION == "cubic_atom_r" else -2
    cubic_omega_power = -1 if MUTATION == "cubic_atom_omega" else 1
    cubic_atom = hr ** cubic_r_power * homega ** cubic_omega_power * l3_integral
    reconstructed_cubic = hr ** 2 * homega ** -1 * cubic_atom
    half = Q(1) if MUTATION == "transport_half" else Q(1, 2)
    transport_upper = (
        half * q(holder["eta"]) * q(holder["bMagnitude"])
        * q(holder["cutoffDerivativeMagnitude"]) * l2_integral
    )
    normalized_flux = homega / hr * transport_upper
    one_block_left_cubed = normalized_flux ** 3
    one_block_right_cubed = hl ** 2 * homega * hr ** -2 * cubic_atom ** 2
    holder_observed = {
        "timeFromR": qtext(hr ** 3),
        "supportFromLR": qtext(hl ** 2 * hr ** 3),
        "cylinderMeasure": qtext(cylinder_measure),
        "l2Integral": qtext(l2_integral),
        "l3Integral": qtext(l3_integral),
        "holderLeftCubed": qtext(holder_left_cubed),
        "holderRightCubed": qtext(holder_right_cubed),
        "holderStrictGap": qtext(holder_right_cubed - holder_left_cubed),
        "cubicAtom": qtext(cubic_atom),
        "cubicIntegralFromAtom": qtext(reconstructed_cubic),
        "transportAbsoluteUpper": qtext(transport_upper),
        "normalizedFlux": qtext(normalized_flux),
        "oneBlockRightCubed": qtext(one_block_right_cubed),
        "oneBlockLeftCubed": qtext(one_block_left_cubed),
        "oneBlockStrictGap": qtext(one_block_right_cubed - one_block_left_cubed),
    }
    holder_direction = "left>=right" if MUTATION == "holder_direction" else "left<=right"
    one_block_direction = "left>=right" if MUTATION == "one_block_direction" else "left<=right"

    # I.2 and I.16--I.17 on perfect-cube payments.
    participation_observed = []
    for case in fixtures["participationCases"]:
        payments = [q(value) for value in case["payments"]]
        roots = [exact_cuberoot(value) for value in payments]
        terms = roots if MUTATION == "participation_power" else [root ** 2 for root in roots]
        total = sum(payments, Q(0))
        sum_two_thirds = sum(terms, Q(0))
        cardinality = len(payments)
        if MUTATION == "equal_mass_count" and case["name"] == "equalMassFourBlocks":
            cardinality = 3
        if total == 0:
            n_eff = Q(1) if MUTATION == "neff_zero" else Q(0)
        else:
            numerator_power = 2 if MUTATION == "neff_numerator" else 3
            denominator_power = 1 if MUTATION == "neff_denominator" else 2
            n_eff = sum_two_thirds ** numerator_power / total ** denominator_power
        if MUTATION == "unequal_as_count" and case["name"] == "unequalPerfectCubes":
            n_eff = Q(cardinality)
        identity_residual = (
            sum_two_thirds ** 3 - n_eff * total ** 2
            + (Q(1) if MUTATION == "aggregation_identity" else Q(0))
        )
        positive = total > 0
        lower_slack = n_eff - 1 if positive else None
        upper_slack = cardinality - n_eff if positive else None
        participation_observed.append({
            "name": case["name"],
            "cardinality": cardinality,
            "totalPayment": qtext(total),
            "sumTwoThirds": qtext(sum_two_thirds),
            "nEff": qtext(n_eff),
            "lowerSlack": qtext(lower_slack) if lower_slack is not None else "not-applicable",
            "upperSlack": qtext(upper_slack) if upper_slack is not None else "not-applicable",
            "identityResidual": qtext(identity_residual),
        })
    neff_lower_direction = "N_eff<=1" if MUTATION == "neff_lower_direction" else "1<=N_eff"
    neff_upper_direction = "N<=N_eff" if MUTATION == "neff_upper_direction" else "N_eff<=N"

    # Signed aggregate triangle inequality: include a negative-total case to
    # distinguish positive part from absolute value.
    signed_observed = []
    for case in fixtures["signedAggregationCases"]:
        fluxes = [q(value) for value in case["fluxes"]]
        signed_sum = sum(fluxes, Q(0))
        positive_part = (
            abs(signed_sum) if MUTATION == "aggregate_positive_part"
            else max(signed_sum, Q(0))
        )
        absolute_sum = (
            signed_sum if MUTATION == "aggregate_absolute_sum"
            else sum((abs(value) for value in fluxes), Q(0))
        )
        signed_observed.append({
            "name": case["name"],
            "signedSum": qtext(signed_sum),
            "positivePart": qtext(positive_part),
            "sumAbsolute": qtext(absolute_sum),
            "triangleSlack": qtext(absolute_sum - positive_part),
            "inequalityDirection": (
                "left>=right" if MUTATION == "aggregate_direction" else "left<=right"
            ),
        })

    # I.18 is an upper-domination chain; no lower-bound substitution is valid.
    payment = fixtures["paymentDirectionCase"]
    pa = q(payment["pA"])
    pf = q(payment["pF"])
    constant_times_p = q(payment["constant"]) * q(payment["P"])
    payment_observed = {
        "pA": qtext(pa),
        "pF": qtext(pf),
        "constantTimesP": qtext(constant_times_p),
        "pAToPFDirection": "pA>=pF" if MUTATION == "payment_pa_direction" else "pA<=pF",
        "pFToPDirection": "pF>=CP" if MUTATION == "payment_pf_direction" else "pF<=CP",
        "targetPower": "1/3" if MUTATION == "payment_power" else "2/3",
        "usesUpperDomination": MUTATION != "payment_upper_use",
        "firstSlack": qtext(pf - pa),
        "secondSlack": qtext(constant_times_p - pf),
    }

    # I.14 and I.21--I.26 exact threshold arithmetic.
    constants = fixtures["thresholdConstants"]
    rho = q(constants["rho"])
    c_gamma = q(constants["cGamma"])
    if MUTATION == "rho_sign":
        rho *= -1
    if MUTATION == "cgamma_sign":
        c_gamma *= -1
    theta_star = (
        rho / c_gamma - 2 if MUTATION == "theta_ratio"
        else c_gamma / rho - (1 if MUTATION == "theta_offset" else 2)
    )
    beta_star = (
        1 + theta_star if MUTATION == "beta_complement" else 1 - theta_star
    )
    one_rate = rho / 6 - c_gamma / 12
    if MUTATION == "one_rate_fraction":
        one_rate += Q(1, 238140000)
    below_rate = (rho * (2 + q(constants["thetaBelow"])) - c_gamma) / 12
    endpoint_rate = (rho * (2 + theta_star) - c_gamma) / 12
    above_rate = (rho * (2 + q(constants["thetaAbove"])) - c_gamma) / 12
    full_theta = Q(0) if MUTATION == "uniform_theta" else Q(1)
    full_uniform_rate = (rho * (2 + full_theta) - c_gamma) / 12
    if MUTATION == "uniform_rate_fraction":
        full_uniform_rate += Q(1, 476280000)
    threshold_observed = {
        "thetaStar": qtext(theta_star),
        "betaStar": qtext(beta_star),
        "oneBlockRate": qtext(one_rate),
        "belowRate": qtext(below_rate),
        "endpointRate": qtext(endpoint_rate),
        "aboveRate": qtext(above_rate),
        "fullUniformRate": qtext(full_uniform_rate),
        "thetaEndpointAccepted": MUTATION == "theta_strict",
        "betaEndpointAccepted": MUTATION == "beta_strict",
        "remainingEndpointFactor": "1" if MUTATION == "endpoint_polynomial" else "L^(2/3)",
    }

    # I.27: an x2-zero mode has exact derivative cancellation on every block
    # while equal positive cubic atoms give maximal participation.
    zero_mode = fixtures["zeroModeCase"]
    z_measures = [q(value) for value in zero_mode["x2CellMeasures"]]
    z_derivatives = [q(value) for value in zero_mode["cutoffDerivativeValues"]]
    derivative_mean = sum(
        measure * (abs(value) if MUTATION == "zero_mode_mean" else value)
        for measure, value in zip(z_measures, z_derivatives)
    )
    z_flux = (
        Q(1, 2) * q(zero_mode["timeLength"]) * q(zero_mode["eta"])
        * q(zero_mode["bValue"]) * q(zero_mode["fieldValue"]) ** 2
        * derivative_mean
    )
    if MUTATION == "zero_mode_flux":
        z_flux += 1
    z_cubic_integral = (
        q(zero_mode["timeLength"]) * q(zero_mode["domainVolume"])
        * abs(q(zero_mode["fieldValue"])) ** 3
    )
    z_payment = (
        q(zero_mode["R"]) ** -2 * q(zero_mode["omega"]) * z_cubic_integral
    )
    if MUTATION == "zero_mode_payment":
        z_payment *= 8
    z_count = int(zero_mode["blockCount"])
    z_total = z_count * z_payment
    z_term = exact_cuberoot(z_payment) ** 2
    z_sum = z_count * z_term
    z_neff = z_sum ** 3 / z_total ** 2
    if MUTATION == "zero_mode_neff":
        z_neff -= 1
    zero_mode_observed = {
        "cutoffDerivativeMean": qtext(derivative_mean),
        "fluxPerBlock": qtext(z_flux),
        "cubicIntegralPerBlock": qtext(z_cubic_integral),
        "paymentPerBlock": qtext(z_payment),
        "totalPayment": qtext(z_total),
        "sumTwoThirds": qtext(z_sum),
        "nEff": qtext(z_neff),
        "blockCount": z_count,
        "highParticipationIsCounterexample": MUTATION == "high_neff_counterexample",
        "participationBoundIsNecessary": MUTATION == "participation_necessary",
    }

    tags = re.findall(r"\\tag\{(I\.[^}]+)\}", text)
    if MUTATION == "tag":
        tags.append("I.1")
    references = [
        "I." + value for value in re.findall(r"\(I\.([0-9]+[a-z]?)\)", text)
    ]
    if MUTATION == "reference":
        references.append("I.99")
    display_open = sum(line.strip() == r"\[" for line in text.splitlines())
    display_close = sum(line.strip() == r"\]" for line in text.splitlines())
    if MUTATION == "display":
        display_open += 1
    expected_tags = [f"I.{index}" for index in range(1, 28)]

    dependency_paths = (
        "research/r075b_bulk_clock_outer_padding_gate.md",
        "research/r075c_background_shear_packing_false_positive.md",
        "research/r075e_horizontal_cross_mode_flux_reduction.md",
        "research/r075g_signed_flux_gain_threshold.md",
        "research/r075h_single_pass_transport_flux_closure.md",
    )
    dependency_table_present = all(
        any(path in line and FROZEN_SOURCES[path] in line for line in text.splitlines())
        for path in dependency_paths
    )
    if MUTATION == "dependency_table_missing":
        dependency_table_present = False

    required_tokens = (
        "No equation for the passive field is used in this estimate.",
        "For an arbitrary real measurable field",
        "physical diffusion cannot invalidate this conclusion.",
        r"\left[\sum_{j\in A}\mathcal T_j\right]_+",
        r"N_{\rm eff}(A)^{1/3}p_A^{2/3}",
        r"\theta<\frac{c_\gamma}{\rho}-2",
        r"\frac{8558}{35721}=\theta_*",
        r"\frac{27163}{35721}",
        r"\frac{27163}{476280000}>0",
        r"\int_{\mathbb T_{x_2}}\partial_2\xi\,dx_2",
        "is only a sufficient route.",
        "Failure of (I.19) neither disproves",
        r"\mathbf{NOT\ CLAY}",
    )

    boundary = {
        "arbitraryFieldNoPDEUsed": MUTATION != "pde_required",
        "oneBlockEstimateDiffusionSafe": MUTATION != "diffusion_unsafe",
        "participationEstimateRemainsConditional": MUTATION != "participation_proved",
        "participationIsSufficientNotNecessary": MUTATION != "participation_necessary",
        "highParticipationIsNotCounterexample": MUTATION != "high_neff_counterexample",
        "uniformAbsoluteLossIsNotCounterexample": MUTATION != "uniform_counterexample",
        "signedCancellationAlternativeOpen": MUTATION != "signed_alternative_closed",
        "shearTransitionBandsOpen": MUTATION != "transition_closed",
        "periodicRecrossingOpen": MUTATION != "recrossing_closed",
        "E24Open": MUTATION != "e24_closed",
        "completeClockOpen": MUTATION != "complete_clock",
        "fixedDeletionOpen": MUTATION != "fixed_deletion",
        "suitableWeakTransferOpen": MUTATION != "suitable_weak",
        "regularityOpen": MUTATION != "regularity",
        "singularityOpen": MUTATION != "singularity",
        "noNoveltyOrPriorityClaim": MUTATION != "novelty",
        "noSimulationUsed": MUTATION != "simulation_used",
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
            and fixtures["schema"] == "r075i-diffusion-safe-block-participation-fixtures-v1"
            and expected["schema"] == "r075i-diffusion-safe-block-participation-expected-v1"
            and fixtures["frozenSources"] == FROZEN_SOURCES,
            fixtures={"expected": fixture_expected_hash, "observed": fixture_hash},
            expected={"expected": expected_expected_hash, "observed": expected_hash},
        ),
        "primaryAuditBindingAndStatus": record(
            FROZEN_SOURCES["research/r075i_diffusion_safe_block_participation.md"] in audit_text
            and "Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0." in audit_text
            and "Equation tags I.1--I.27 are unique and consecutive." in audit_text
            and "All 27 display-math environments are paired." in audit_text
            and "High participation is neither an E.24 counterexample"
                in re.sub(r"\s+", " ", audit_text),
        ),
        "fiveDependencyTableBindings": record(dependency_table_present),
        "i5ToI13ExponentLedger": record(
            exponent_observed == expected["exponentLedger"],
            observed=exponent_observed,
        ),
        "nondegenerateOneBlockHolder": record(
            holder_observed == expected["oneBlockHolder"]
            and htime == hr ** 3
            and hsupport == hl ** 2 * hr ** 3
            and holder_direction == "left<=right"
            and holder_left_cubed < holder_right_cubed,
            observed=holder_observed,
        ),
        "oneBlockCubicNormalizationAndFluxBound": record(
            reconstructed_cubic == l3_integral
            and one_block_direction == "left<=right"
            and one_block_left_cubed < one_block_right_cubed,
            observed=holder_observed,
        ),
        "participationExamplesAndExactIdentity": record(
            participation_observed == expected["participation"]
            and all(row["identityResidual"] == "0" for row in participation_observed)
            and participation_observed[2]["nEff"] == "125/81",
            observed=participation_observed,
        ),
        "participationBoundsOneToN": record(
            neff_lower_direction == "1<=N_eff"
            and neff_upper_direction == "N_eff<=N"
            and all(
                q(row["lowerSlack"]) >= 0 and q(row["upperSlack"]) >= 0
                for row in participation_observed if row["lowerSlack"] != "not-applicable"
            ),
        ),
        "signedPositivePartTriangle": record(
            signed_observed == expected["signedAggregation"]
            and all(q(row["triangleSlack"]) >= 0 for row in signed_observed),
            observed=signed_observed,
        ),
        "versionMPaymentUpperDirection": record(
            payment_observed == expected["paymentDirection"]
            and pa <= pf <= constant_times_p,
            observed=payment_observed,
        ),
        "exactThresholdsAndEndpointStrictness": record(
            threshold_observed == expected["thresholds"]
            and one_rate < 0 and below_rate < 0
            and endpoint_rate == 0 and above_rate > 0 and full_uniform_rate > 0
            and not threshold_observed["thetaEndpointAccepted"]
            and not threshold_observed["betaEndpointAccepted"],
            observed=threshold_observed,
        ),
        "zeroModeHighParticipationZeroFluxI27": record(
            zero_mode_observed == expected["zeroMode"]
            and z_flux == 0 and z_payment > 0 and z_neff == z_count,
            observed=zero_mode_observed,
        ),
        "tagsReferencesAndDisplays": record(
            tags == expected_tags and len(set(tags)) == 27
            and not (set(references) - set(tags))
            and display_open == display_close == 27,
            tags=tags,
            references=sorted(set(references)),
            displays={"open": display_open, "close": display_close},
        ),
        "formulaAndStatusSentinels": record(
            all(re.sub(r"\s+", " ", token) in flat_text for token in required_tokens),
        ),
        "sourceReportBoundary": record(
            "This is a bounded non-hit, not evidence of novelty or priority." in source_text
            and "high participation is not a counterexample or a" in source_text
            and "necessary obstruction" in source_text,
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
        "exponentLedger": exponent_observed,
        "oneBlockHolder": holder_observed,
        "participation": participation_observed,
        "signedAggregation": signed_observed,
        "paymentDirection": payment_observed,
        "thresholds": threshold_observed,
        "zeroMode": zero_mode_observed,
        "claimBoundary": boundary,
    }
    OUT_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    failed = [name for name, item in checks.items() if not item["pass"]]
    OUT_REPORT.write_text(
        "# R0.75I finite certificate report\n\n"
        f"- Verdict: **{verdict}**\n"
        f"- Assertions: {payload['assertions']['passed']}/{payload['assertions']['total']}\n"
        f"- Main SHA-256: {sha256(MAIN)}\n"
        f"- Fixture SHA-256: {fixture_hash}\n"
        f"- Expected SHA-256: {expected_hash}\n"
        f"- Failed checks: {'none' if not failed else '; '.join(failed)}\n\n"
        "Exact Laurent arithmetic reconstructs every I.5--I.13 power and the "
        "final L^(2/3) omega^(1/3) R^(-2/3) p_j^(2/3) row. A nonconstant "
        "two-cell rational field gives strict Holder and one-block margins.\n\n"
        "Perfect-cube payments verify the exact participation identity, the "
        "bounds 1 <= N_eff <= N, and [1,8] -> 125/81. Mixed signed fluxes "
        "verify [sum T_j]_+ <= sum |T_j|. The Version-M substitution is an "
        "upper-domination chain. Exact threshold rates and strict endpoints "
        "agree with I.14 and I.21--I.26.\n\n"
        "The I.27 zero-mode fixture has equal positive payment on four blocks, "
        "N_eff=4, and flux zero on every block. Thus I.19 is only sufficient "
        "for the absolute block-summation route; high participation is neither "
        "necessary nor an E.24 counterexample. No PDE is used in the one-block "
        "bound, but diffusion-safe does not prove participation. E.24 and all "
        "larger claims remain OPEN. **NOT CLAY.**\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "suite": "r075i-diffusion-safe-block-participation",
        "verdict": verdict,
        "assertions": len(checks),
    }, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
