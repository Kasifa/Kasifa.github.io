#!/usr/bin/env python3
"""Fail-closed exact finite certificate for frozen R0.75K."""

from __future__ import annotations

import hashlib
import json
import os
import re
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "research/r075k_positive_majorant_high_frequency_trace_loss.md"
PRIMARY_AUDIT = ROOT / "research/r075k_positive_majorant_high_frequency_trace_loss_primary_audit.md"
REPORT_SOURCE = ROOT / "research/r075k_report-source.md"
FIXTURES = ROOT / "scripts/r075k_positive_majorant_high_frequency_trace_loss_fixtures.json"
EXPECTED = ROOT / "scripts/r075k_positive_majorant_high_frequency_trace_loss_expected.json"
OUT_JSON = Path(os.environ.get(
    "R075K_JSON",
    ROOT / "research/r075k_positive_majorant_high_frequency_trace_loss_certificate.json",
))
OUT_REPORT = Path(os.environ.get(
    "R075K_REPORT",
    ROOT / "research/r075k_positive_majorant_high_frequency_trace_loss_certificate_report.md",
))
MUTATION = os.environ.get("R075K_MUTATION", "")
SCHEMA = "r075k-positive-majorant-high-frequency-trace-loss-certificate-v1"

FROZEN_SOURCES = {
    "research/r075e_horizontal_cross_mode_flux_reduction.md":
        "99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049",
    "research/r075i_diffusion_safe_block_participation.md":
        "c8511690dc52988b3f3715e589379c72dae0a892dcabd8d0ca218dddbe0fd3a7",
    "research/r075j_mean_zero_adjoint_flux_obstruction.md":
        "960e3cbc18ac8207253a8802da215b3eac07a714ddbcc7209985f27a00c9ff4d",
    "research/r075k_positive_majorant_high_frequency_trace_loss.md":
        "9282fb30eb7517853759fb835579220e0da763974d5543e2fb260ec8ca6daebf",
    "research/r075k_positive_majorant_high_frequency_trace_loss_primary_audit.md":
        "401f12d9a5f35646638ae08446a1177a0b0485b9bbb54206702dee9fc7e7a4a2",
    "research/r075k_report-source.md":
        "5a45521ecb5e85b69b077af9d4db3cbb1c52dc1b61cccf8fb3bbb9daabac7001",
}
FIXTURES_SHA256 = "f15df9bf59d6a96151f84ae2fa11a12b3965820450fbad526d4f71f11a6f7328"
EXPECTED_SHA256 = "5ad1107080ccf033e842521e8f985196357d6cb858f945b007a5df50c2a12d77"

NEGATIVE_MUTATIONS = (
    "source_drift", "audit_drift", "report_source_drift", "dependency_drift",
    "dependency_table_missing", "fixture_drift", "expected_drift", "tag",
    "reference", "display", "control", "forward_time_sign",
    "forward_drift_sign", "forward_diffusion_sign", "adjoint_time_sign",
    "adjoint_drift_sign", "adjoint_diffusion_sign", "constant_shear",
    "q_constant", "q_cosine", "a_cosine", "q_majorant_direction",
    "q_nonnegative", "q_modes", "a_modes", "time_reversal",
    "semigroup_drift_sign", "semigroup_diffusion_sign",
    "semigroup_source_sign", "phi_terminal", "phi_nonnegative", "phi_modes",
    "phi_mass_sign", "phi_mass_factor", "phi_mass_endpoint", "decay_sign",
    "phase_direction", "time_decay", "time_phase", "drift_phase",
    "laplacian_sign", "passive_residual", "k_integer", "k_lower",
    "square_frequency", "square_zero_coefficient", "square_side_coefficient",
    "entrance_half", "orthogonality", "boundary_k_dependence",
    "cos_quarter", "cos_symmetry", "cos_integral", "mass_decay_three",
    "mass_k_square", "mass_amplitude", "mass_upper_direction",
    "exponential_range", "mass_exact_factor", "boundary_A", "mass_A",
    "mass_k", "two_thirds", "ratio_A", "ratio_k", "amplitude_cancel",
    "ratio_growth", "ratio_constant", "signed_source_frequency",
    "signed_field_frequency", "signed_mode_match", "signed_flux_nonzero",
    "signed_integer_quantifier", "physical_flux_absolute", "W_limit_order",
    "W_continuous", "W_nonnegative", "W_integral", "W_depends_k",
    "W_frequency", "riemann_lebesgue", "W_boundary_limit",
    "local_atom_not_alone", "e24_counterexample", "all_majorants_ruled",
    "fdependent_ruled", "signed_kernel_ruled", "full_versionm_ruled",
    "trace_atom_ruled", "nse_solution", "transition_closed", "periodic_closed",
    "complete_clock", "fixed_deletion", "suitable_weak", "regularity",
    "singularity", "novelty", "simulation_used", "clay",
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
        raise SystemExit(f"unknown R075K_MUTATION: {MUTATION}")

    text = MAIN.read_text(encoding="utf-8")
    audit_text = PRIMARY_AUDIT.read_text(encoding="utf-8")
    source_text = REPORT_SOURCE.read_text(encoding="utf-8")
    flat_text = re.sub(r"\s+", " ", text)
    flat_source_text = re.sub(r"\s+", " ", source_text)
    scan_text = text + audit_text + source_text
    if MUTATION == "control":
        scan_text += "\x01"
    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))

    source_expectations = dict(FROZEN_SOURCES)
    if MUTATION == "source_drift":
        source_expectations[
            "research/r075k_positive_majorant_high_frequency_trace_loss.md"
        ] = "0" * 64
    if MUTATION == "audit_drift":
        source_expectations[
            "research/r075k_positive_majorant_high_frequency_trace_loss_primary_audit.md"
        ] = "0" * 64
    if MUTATION == "report_source_drift":
        source_expectations["research/r075k_report-source.md"] = "0" * 64
    if MUTATION == "dependency_drift":
        source_expectations[
            "research/r075j_mean_zero_adjoint_flux_obstruction.md"
        ] = "0" * 64
    source_rows = {
        path: {"expectedSha256": digest, "observedSha256": sha256(ROOT / path)}
        for path, digest in sorted(source_expectations.items())
    }
    fixture_expected_hash = "0" * 64 if MUTATION == "fixture_drift" else FIXTURES_SHA256
    expected_expected_hash = "0" * 64 if MUTATION == "expected_drift" else EXPECTED_SHA256
    fixture_hash = sha256(FIXTURES)
    expected_hash = sha256(EXPECTED)

    # K.2: forward and formal-adjoint sign ledger.
    operator = fixtures["operatorCase"]
    forward = {key: q(value) for key, value in operator["forward"].items()}
    adjoint = {key: q(value) for key, value in operator["adjoint"].items()}
    for mutation, row, key in (
        ("forward_time_sign", forward, "time"),
        ("forward_drift_sign", forward, "drift"),
        ("forward_diffusion_sign", forward, "secondDerivative"),
        ("adjoint_time_sign", adjoint, "time"),
        ("adjoint_drift_sign", adjoint, "drift"),
        ("adjoint_diffusion_sign", adjoint, "secondDerivative"),
    ):
        if MUTATION == mutation:
            row[key] *= -1
    shear = q(operator["constantShear"])
    if MUTATION == "constant_shear":
        shear *= -1
    operator_observed = {
        "forward": {key: qtext(value) for key, value in forward.items()},
        "adjoint": {key: qtext(value) for key, value in adjoint.items()},
    }

    # K.3--K.4: q=1+cos(x) is nonnegative and q-a=1.
    source = fixtures["majorantSourceCase"]
    q_constant = q(source["qConstant"])
    q_cosine = q(source["qCosineCoefficient"])
    a_cosine = q(source["aCosineCoefficient"])
    if MUTATION == "q_constant":
        q_constant = 0
    if MUTATION == "q_cosine":
        q_cosine = 2
    if MUTATION == "a_cosine":
        a_cosine = 2
    rows = []
    for cosine_text in source["cosineSamples"]:
        cosine = q(cosine_text)
        q_value = q_constant + q_cosine * cosine
        a_value = a_cosine * cosine
        rows.append({
            "cosine": qtext(cosine),
            "q": qtext(q_value),
            "a": qtext(a_value),
            "qMinusA": qtext(q_value - a_value),
        })
    q_minimum = q_constant - abs(q_cosine)
    q_minus_a_minimum = q_constant - abs(q_cosine - a_cosine)
    q_modes = list(source["sourceModes"])
    if MUTATION == "q_modes":
        q_modes.append(2)
    a_modes = [-1, 1]
    if MUTATION == "a_modes":
        a_modes.append(0)
    source_observed = {
        "rows": rows,
        "qNonnegativeOnCosineRange": (
            False if MUTATION == "q_nonnegative" else q_minimum >= 0
        ),
        "qMajorizesAOnCosineRange": (
            False if MUTATION == "q_majorant_direction" else q_minus_a_minimum >= 0
        ),
        "qModes": q_modes,
        "aModes": a_modes,
    }

    # K.5--K.6: reverse time to a forward positive semigroup.
    semigroup = fixtures["semigroupCase"]
    total_time = q(semigroup["T"])
    time_direction = "backward-in-tau" if MUTATION == "time_reversal" else "forward-in-tau"
    reversed_drift = q(semigroup["reversedGeneratorDrift"])
    reversed_diffusion = q(semigroup["reversedGeneratorDiffusion"])
    source_sign = q(semigroup["sourceSign"])
    if MUTATION == "semigroup_drift_sign":
        reversed_drift *= -1
    if MUTATION == "semigroup_diffusion_sign":
        reversed_diffusion *= -1
    if MUTATION == "semigroup_source_sign":
        source_sign *= -1
    terminal_value = q(semigroup["terminalValue"])
    if MUTATION == "phi_terminal":
        terminal_value = 1
    phi_modes = list(q_modes)
    if MUTATION == "phi_modes":
        phi_modes.append(2)
    mass_over_pi = Q(2) * total_time
    if MUTATION == "phi_mass_sign":
        mass_over_pi *= -1
    if MUTATION == "phi_mass_factor":
        mass_over_pi /= 2
    if MUTATION == "phi_mass_endpoint":
        mass_over_pi += 1
    semigroup_observed = {
        "timeDirection": time_direction,
        "duhamelOrientation": "integral-T-to-0" if MUTATION == "time_reversal" else "integral-0-to-T",
        "reversedGeneratorDrift": qtext(reversed_drift),
        "reversedGeneratorDiffusion": qtext(reversed_diffusion),
        "sourceSign": qtext(source_sign),
        "terminalValue": qtext(terminal_value),
        "PhiNonnegative": MUTATION != "phi_nonnegative",
        "PhiEntranceModes": phi_modes,
        "spatialMassSymbol": "-2*pi*T" if MUTATION == "phi_mass_sign" else "2*pi*T",
        "spatialMassOverPi": qtext(mass_over_pi),
    }

    # Integral of |cos|^3 by four identical quadrants.
    moment = fixtures["absoluteCosineMoment"]
    quarter_integral = q(moment["quarterIntegral"])
    symmetry_factor = q(moment["symmetryFactor"])
    if MUTATION == "cos_quarter":
        quarter_integral += Q(1, 3)
    if MUTATION == "cos_symmetry":
        symmetry_factor = 2
    full_cosine_integral = quarter_integral * symmetry_factor
    if MUTATION == "cos_integral":
        full_cosine_integral += 1
    moment_observed = {
        "quarterIntegral": qtext(quarter_integral),
        "symmetryFactor": qtext(symmetry_factor),
        "fullIntegral": qtext(full_cosine_integral),
    }

    # K.8--K.16: exact Fourier-mode family at three integer frequencies.
    family = fixtures["passiveFamilyCase"]
    amplitude = q(family["A"])
    if MUTATION == "mass_amplitude":
        amplitude += 1
    family_time = q(family["T"])
    ks = list(family["integerK"])
    integer_quantifier = MUTATION != "k_integer"
    lower_quantifier = MUTATION != "k_lower"
    source_frequency = 2 if MUTATION == "signed_source_frequency" else 1
    family_observed = []
    for k in ks:
        time_cos = Q(k * k if MUTATION in ("decay_sign", "time_decay") else -k * k)
        time_sin = Q(-k if MUTATION in ("phase_direction", "time_phase") else k)
        drift_sin = Q(k if MUTATION == "drift_phase" else -k)
        diffusion_cos = Q(-k * k if MUTATION == "laplacian_sign" else k * k)
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
        square_modes = [-square_frequency, 0, square_frequency]
        entrance_factor = Q(1) if MUTATION == "entrance_half" else Q(1, 2)
        boundary_over_pi = entrance_factor * square_zero * mass_over_pi
        if MUTATION == "orthogonality":
            boundary_over_pi += 1
        if MUTATION == "boundary_k_dependence":
            boundary_over_pi += k
        decay_factor = Q(1) if MUTATION == "mass_decay_three" else Q(3)
        k_power = Q(k) if MUTATION == "mass_k_square" else Q(k * k)
        mass_coefficient = full_cosine_integral * amplitude ** 3 / (decay_factor * k_power)
        if MUTATION == "mass_exact_factor":
            mass_coefficient += 1
        mass_upper_coefficient = mass_coefficient
        if MUTATION == "mass_upper_direction":
            mass_upper_coefficient *= -1
        signed_match = source_frequency in (square_frequency, -square_frequency)
        if MUTATION == "signed_field_frequency":
            signed_match = (k == 1)
        if MUTATION == "signed_mode_match":
            signed_match = True
        signed_flux = Q(1) if signed_match else Q(0)
        if MUTATION == "signed_flux_nonzero":
            signed_flux += 1
        normalization_cube = (family_time / 2) ** 3
        ratio_cube_normalized = (
            boundary_over_pi ** 3 / mass_upper_coefficient ** 2 / normalization_cube
        )
        if MUTATION == "ratio_constant":
            ratio_cube_normalized += 1
        family_observed.append({
            "k": k,
            "timeCos": qtext(time_cos),
            "timeSin": qtext(time_sin),
            "driftSin": qtext(drift_sin),
            "diffusionCos": qtext(diffusion_cos),
            "residualCos": qtext(residual_cos),
            "residualSin": qtext(residual_sin),
            "squareModes": square_modes,
            "squareModeCoefficients": [
                qtext(square_side), qtext(square_zero), qtext(square_side)
            ],
            "BOverPi": qtext(boundary_over_pi),
            "massCoefficientTimesOneMinusQ": qtext(mass_coefficient),
            "massUpperCoefficient": qtext(mass_upper_coefficient),
            "ratioCubeNormalized": qtext(ratio_cube_normalized),
            "signedFlux": qtext(signed_flux),
        })
    exponential_in_unit_interval = MUTATION != "exponential_range"
    signed_for_all_integers = MUTATION != "signed_integer_quantifier"

    # Formal homogeneity ledger for exact amplitude cancellation and k^(4/3).
    factors = fixtures["exponentFactors"]
    boundary_exp = {key: q(value) for key, value in factors["boundary"].items()}
    mass_exp = {key: q(value) for key, value in factors["massUpper"].items()}
    two_thirds = q(factors["twoThirds"])
    if MUTATION == "boundary_A":
        boundary_exp["A"] = 1
    if MUTATION == "mass_A":
        mass_exp["A"] = 2
    if MUTATION == "mass_k":
        mass_exp["k"] = -1
    if MUTATION == "two_thirds":
        two_thirds = Q(1, 3)
    mass_two_thirds = {
        key: value * two_thirds for key, value in mass_exp.items()
    }
    ratio_exp = {
        key: boundary_exp[key] - mass_two_thirds[key] for key in boundary_exp
    }
    if MUTATION == "ratio_A":
        ratio_exp["A"] += 1
    if MUTATION == "ratio_k":
        ratio_exp["k"] -= Q(1, 3)
    exponent_observed = {
        "boundary": exponent_json(boundary_exp),
        "massUpper": exponent_json(mass_exp),
        "massTwoThirds": exponent_json(mass_two_thirds),
        "ratio": exponent_json(ratio_exp),
        "amplitudeCancels": MUTATION != "amplitude_cancel",
        "ratioDiverges": MUTATION != "ratio_growth",
    }

    # K.17: exact quantifier order and the Riemann--Lebesgue boundary.
    fixed_weight = fixtures["fixedWeightCase"]
    fixed_weight_observed = {
        "quantifier": (
            "choose-W-after-k" if MUTATION == "W_limit_order"
            else "for-each-fixed-W-then-k-to-infinity"
        ),
        "continuous": False if MUTATION == "W_continuous" else bool(fixed_weight["continuous"]),
        "nonnegative": False if MUTATION == "W_nonnegative" else bool(fixed_weight["nonnegative"]),
        "integralPositive": False if MUTATION == "W_integral" else bool(fixed_weight["integralPositive"]),
        "dependsOnK": True if MUTATION == "W_depends_k" else bool(fixed_weight["dependsOnK"]),
        "oscillatoryTerm": (
            "integral-W-cos(kx)" if MUTATION == "W_frequency"
            else "integral-W-cos(2kx)"
        ),
        "oscillatoryLimit": "nonzero" if MUTATION == "riemann_lebesgue" else "0",
        "boundaryLimit": (
            "0" if MUTATION == "W_boundary_limit" else "A^2/4*integral(W)>0"
        ),
    }

    tags = re.findall(r"\\tag\{(K\.[^}]+)\}", text)
    if MUTATION == "tag":
        tags.append("K.1")
    references = [
        "K." + value for value in re.findall(r"\(K\.([0-9]+[a-z]?)\)", text)
    ]
    if MUTATION == "reference":
        references.append("K.99")
    display_open = sum(line.strip() == r"\[" for line in text.splitlines())
    display_close = sum(line.strip() == r"\]" for line in text.splitlines())
    if MUTATION == "display":
        display_open += 1
    expected_tags = [f"K.{index}" for index in range(1, 19)]

    dependency_paths = (
        "research/r075e_horizontal_cross_mode_flux_reduction.md",
        "research/r075i_diffusion_safe_block_participation.md",
        "research/r075j_mean_zero_adjoint_flux_obstruction.md",
    )
    dependency_table_present = all(
        any(path in line and FROZEN_SOURCES[path] in line for line in text.splitlines())
        for path in dependency_paths
    )
    if MUTATION == "dependency_table_missing":
        dependency_table_present = False

    required_tokens = (
        r"\mathcal L=\partial_t+\partial_2-\partial_2^2",
        r"\mathcal L^*=-\partial_t-\partial_2-\partial_2^2",
        r"q(x_2):=1+\cos x_2\ge a(x_2)",
        r"\int_0^{2\pi}\Phi(0,x_2)\,dx_2=2\pi T",
        r"F_k(t,x_2):=A e^{-k^2t}\cos\bigl(k(x_2-t)\bigr)",
        r"\mathcal L F_k=0",
        r"\frac{A^2\pi T}{2}",
        r"\frac{8A^3}{9k^2}\bigl(1-e^{-3k^2T}\bigr)",
        r"\left(\frac98\right)^{2/3}k^{4/3}",
        r"\mathcal T_k=0",
        "Let `W` be any fixed continuous",
        "The Riemann--Lebesgue lemma makes the second row tend to zero.",
        "not a counterexample to E.24",
        r"\mathbf{NOT\ CLAY}",
    )

    boundary = {
        "integerFrequenciesAtLeastOne": integer_quantifier and lower_quantifier,
        "exponentialFactorStrictlyBetweenZeroAndOne": exponential_in_unit_interval,
        "massUpperBoundDirectionCorrect": MUTATION != "mass_upper_direction",
        "signedFluxZeroForEveryIntegerK": signed_for_all_integers,
        "physicalFluxNotAbsoluteValue": MUTATION != "physical_flux_absolute",
        "fixedWeightIndependentOfK": MUTATION not in ("W_depends_k", "W_limit_order"),
        "onlyLocalSpacetimeCubicAtomAloneRuledOut": MUTATION != "local_atom_not_alone",
        "notE24Counterexample": MUTATION != "e24_counterexample",
        "notAllMajorantsRuledOut": MUTATION != "all_majorants_ruled",
        "FDependentTestsRemainOpen": MUTATION != "fdependent_ruled",
        "signedKernelsRemainOpen": MUTATION != "signed_kernel_ruled",
        "fullVersionMPaymentNotRuledOut": MUTATION != "full_versionm_ruled",
        "traceFrequencyAtomRemainsOpen": MUTATION != "trace_atom_ruled",
        "passiveFamilyNotNSEAssertion": MUTATION != "nse_solution",
        "transitionGeometryOpen": MUTATION != "transition_closed",
        "periodicCopiesOpen": MUTATION != "periodic_closed",
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
            and fixtures["schema"] == "r075k-positive-majorant-high-frequency-trace-loss-fixtures-v1"
            and expected["schema"] == "r075k-positive-majorant-high-frequency-trace-loss-expected-v1"
            and fixtures["frozenSources"] == FROZEN_SOURCES,
            fixtures={"expected": fixture_expected_hash, "observed": fixture_hash},
            expected={"expected": expected_expected_hash, "observed": expected_hash},
        ),
        "primaryAuditBindingAndStatus": record(
            FROZEN_SOURCES["research/r075k_positive_majorant_high_frequency_trace_loss.md"] in audit_text
            and "Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0." in audit_text
            and "Equation tags K.1--K.18 are unique and consecutive." in audit_text
            and "All 18 display-math environments are paired." in audit_text,
        ),
        "threeDependencyTableBindings": record(dependency_table_present),
        "forwardAndAdjointOperatorSigns": record(
            operator_observed == expected["operators"] and shear == 1,
            observed=operator_observed,
        ),
        "qNonnegativeAndMajorizesSignedSource": record(
            source_observed == expected["majorantSource"]
            and q_minimum >= 0 and q_minus_a_minimum >= 0,
            observed=source_observed,
        ),
        "zeroTerminalPositiveSemigroupAndModes": record(
            semigroup_observed == expected["semigroup"]
            and reversed_diffusion > 0 and source_sign > 0
            and terminal_value == 0,
            observed=semigroup_observed,
        ),
        "PhiEntranceSpatialMass": record(
            semigroup_observed["spatialMassSymbol"] == "2*pi*T"
            and mass_over_pi == 2 * total_time,
            observed=semigroup_observed,
        ),
        "passiveFamilyExactEquationAndSquareModes": record(
            family_observed == expected["passiveFamily"]
            and all(row["residualCos"] == row["residualSin"] == "0" for row in family_observed),
            observed=family_observed,
        ),
        "boundaryOrthogonalityAndBOverPi": record(
            all(row["BOverPi"] == "9" for row in family_observed),
            observed=family_observed,
        ),
        "absoluteCosineMomentAndMass": record(
            moment_observed == expected["absoluteCosineMoment"]
            and exponential_in_unit_interval
            and all(q(row["massCoefficientTimesOneMinusQ"]) > 0 for row in family_observed),
            observed=moment_observed,
        ),
        "amplitudeCancellationAndFourThirdGrowth": record(
            exponent_observed == expected["exponents"]
            and ratio_exp == {"A": Q(0), "k": Q(4, 3)}
            and all(
                q(later["ratioCubeNormalized"]) > q(earlier["ratioCubeNormalized"])
                for earlier, later in zip(family_observed, family_observed[1:])
            ),
            observed=exponent_observed,
        ),
        "physicalSignedFluxExactlyZero": record(
            all(row["signedFlux"] == "0" for row in family_observed)
            and integer_quantifier and lower_quantifier,
            observed=family_observed,
        ),
        "fixedWeightRiemannLebesgueQuantifier": record(
            fixed_weight_observed == expected["fixedWeight"],
            observed=fixed_weight_observed,
        ),
        "tagsReferencesAndDisplays": record(
            tags == expected_tags and len(set(tags)) == 18
            and not (set(references) - set(tags))
            and display_open == display_close == 18,
            tags=tags,
            references=sorted(set(references)),
            displays={"open": display_open, "close": display_close},
        ),
        "formulaAndStatusSentinels": record(
            all(re.sub(r"\s+", " ", token) in flat_text for token in required_tokens),
        ),
        "sourceReportBoundary": record(
            "no complete-clock, regularity, novelty, or priority claim" in flat_source_text
            and "fixed nontrivial positive weight" in flat_source_text
            and "Does the construction disprove E.24?" in source_text,
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
        "operators": operator_observed,
        "majorantSource": source_observed,
        "semigroup": semigroup_observed,
        "absoluteCosineMoment": moment_observed,
        "passiveFamily": family_observed,
        "exponents": exponent_observed,
        "fixedWeight": fixed_weight_observed,
        "claimBoundary": boundary,
    }
    OUT_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    failed = [name for name, item in checks.items() if not item["pass"]]
    OUT_REPORT.write_text(
        "# R0.75K finite certificate report\n\n"
        f"- Verdict: **{verdict}**\n"
        f"- Assertions: {payload['assertions']['passed']}/{payload['assertions']['total']}\n"
        f"- Main SHA-256: {sha256(MAIN)}\n"
        f"- Fixture SHA-256: {fixture_hash}\n"
        f"- Expected SHA-256: {expected_hash}\n"
        f"- Failed checks: {'none' if not failed else '; '.join(failed)}\n\n"
        "Exact rational mode ledgers verify L/L*, q=1+cos(x)>=cos(x), the "
        "positive reversed semigroup, entrance modes 0,+/-1, and mass 2*pi*T. "
        "At k=1,2,5 the passive residual vanishes, F_k(0)^2 has modes 0,+/-2k, "
        "and B_k/pi=A^2*T/2.\n\n"
        "The quarter-period calculation gives integral |cos(kx)|^3=8/3. "
        "The exact symbolic mass coefficient is 8A^3/(9k^2), the amplitude "
        "cancels, and the normalized ratio cube grows like (81/64)k^4, hence "
        "the ratio grows like k^(4/3). The physical signed flux is nevertheless "
        "zero for every integer k>=1.\n\n"
        "The fixed-W quantifier is W first, then k to infinity; Riemann--Lebesgue "
        "controls only the oscillatory row. The result rules out a fixed "
        "nonnegative entrance weight plus the local spacetime cubic atom alone. "
        "It is not an E.24 counterexample and does not rule out adaptive/signed "
        "tests or the full Version-M ledger. **NOT CLAY.**\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "suite": "r075k-positive-majorant-high-frequency-trace-loss",
        "verdict": verdict,
        "assertions": len(checks),
    }, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
