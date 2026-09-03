#!/usr/bin/env python3
"""Fail-closed exact finite certificate for frozen R0.75J."""

from __future__ import annotations

import hashlib
import json
import os
import re
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "research/r075j_mean_zero_adjoint_flux_obstruction.md"
PRIMARY_AUDIT = ROOT / "research/r075j_mean_zero_adjoint_flux_obstruction_primary_audit.md"
REPORT_SOURCE = ROOT / "research/r075j_report-source.md"
FIXTURES = ROOT / "scripts/r075j_mean_zero_adjoint_flux_obstruction_fixtures.json"
EXPECTED = ROOT / "scripts/r075j_mean_zero_adjoint_flux_obstruction_expected.json"
OUT_JSON = Path(os.environ.get(
    "R075J_JSON",
    ROOT / "research/r075j_mean_zero_adjoint_flux_obstruction_certificate.json",
))
OUT_REPORT = Path(os.environ.get(
    "R075J_REPORT",
    ROOT / "research/r075j_mean_zero_adjoint_flux_obstruction_certificate_report.md",
))
MUTATION = os.environ.get("R075J_MUTATION", "")
SCHEMA = "r075j-mean-zero-adjoint-flux-obstruction-certificate-v1"

FROZEN_SOURCES = {
    "research/r075e_horizontal_cross_mode_flux_reduction.md":
        "99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049",
    "research/r075f_modal_phase_integration_identity.md":
        "f7a72ebfe0471e18c0d5d44bd3123491d7cd47a79293d1860c5d023c13acf440",
    "research/r075h_single_pass_transport_flux_closure.md":
        "849379bea9cf22e0d892ac11ac05bb3b3bc2967a1735753dbc4a6ffc7bb7d7b9",
    "research/r075i_diffusion_safe_block_participation.md":
        "c8511690dc52988b3f3715e589379c72dae0a892dcabd8d0ca218dddbe0fd3a7",
    "research/r075j_mean_zero_adjoint_flux_obstruction.md":
        "960e3cbc18ac8207253a8802da215b3eac07a714ddbcc7209985f27a00c9ff4d",
    "research/r075j_mean_zero_adjoint_flux_obstruction_primary_audit.md":
        "f2de2d439d428ccd2885f7d3fc333496cb9753896c772a54df04622e4c52c76e",
    "research/r075j_report-source.md":
        "1d195b0bc6760a4458fd3b4f7d11c5c892ca259c88aa5de3b014b4986ad166ca",
}
FIXTURES_SHA256 = "754d585bab0b194adaa3f945dc8b14950e3c078564f38dc63919cf733fcfea2c"
EXPECTED_SHA256 = "6c32cd1ff38895c5e3b0a580ad9a5e789fc3d9d8e672ba6644dceeb29befe5b8"

NEGATIVE_MUTATIONS = (
    "source_drift", "audit_drift", "report_source_drift", "dependency_drift",
    "dependency_table_missing", "fixture_drift", "expected_drift", "tag",
    "reference", "display", "control", "forward_time_sign",
    "forward_drift_sign", "forward_diffusion_sign", "adjoint_time_sign",
    "adjoint_drift_sign", "adjoint_diffusion_sign", "drift_divergence",
    "square_diss_sign", "square_diss_factor", "derivative_source_abs",
    "derivative_source_positive", "source_b_x2", "source_mean_quantifier",
    "positive_source_equal", "tau_direction", "A_sign", "B_sign", "b_sign",
    "terminal_nonzero", "adjoint_source_cos", "adjoint_source_sin",
    "eta_denominator", "eta_positive", "slice_sign", "sign_change_false",
    "j12_initial_sign", "j12_terminal_sign", "j12_bulk_sign",
    "j12_endpoint_swap", "j12_source_pairing", "j5_half", "j5_diss_sign",
    "j13_initial_sign", "j13_diss_sign", "j13_drop_negative_initial",
    "signed_decomposition", "energy_endpoint_sign", "energy_factor",
    "shift_initial_sign", "shift_terminal_sign", "shift_diss_sign",
    "constant_homogeneous", "exact_shift_nonzero", "surcharge_half",
    "surcharge_not_cd", "majorant_direction", "phi_nonnegative",
    "terminal_nonnegative", "majorant_half", "majorant_terminal_sign",
    "majorant_diss_sign", "majorant_source_direction", "favorable_terminal",
    "favorable_dissipation", "pde_backward", "exact_adjoint_nonnegative",
    "aplus_signed", "majorant_paid", "uncontrolled_dissipation_paid",
    "free_shift", "blanket_no_go", "feynman_kac_closed", "transition_closed",
    "periodic_closed", "e24_closed", "complete_clock", "fixed_deletion",
    "suitable_weak", "regularity", "singularity", "simulation_used",
    "novelty", "clay",
)

Q = Fraction
Poly = list[Q]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(value: str | int) -> Q:
    return Q(value)


def qtext(value: Q) -> str:
    return str(value)


def poly_trim(poly: Poly) -> Poly:
    result = list(poly)
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def poly_add(*polys: Poly) -> Poly:
    size = max(len(poly) for poly in polys)
    return poly_trim([
        sum((poly[index] if index < len(poly) else Q(0)) for poly in polys)
        for index in range(size)
    ])


def poly_scale(poly: Poly, scale: Q) -> Poly:
    return poly_trim([scale * coefficient for coefficient in poly])


def poly_multiply(left: Poly, right: Poly) -> Poly:
    result = [Q(0)] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] += left_value * right_value
    return poly_trim(result)


def poly_derivative(poly: Poly) -> Poly:
    if len(poly) == 1:
        return [Q(0)]
    return poly_trim([index * coefficient for index, coefficient in enumerate(poly)][1:])


def poly_eval(poly: Poly, value: Q) -> Q:
    result = Q(0)
    for coefficient in reversed(poly):
        result = result * value + coefficient
    return result


def poly_json(poly: Poly, degree: int) -> list[str]:
    return [qtext(poly[index] if index < len(poly) else Q(0)) for index in range(degree + 1)]


def record(ok: bool, **details: Any) -> dict[str, Any]:
    return {"pass": bool(ok), **details}


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R075J_MUTATION: {MUTATION}")

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
        source_expectations["research/r075j_mean_zero_adjoint_flux_obstruction.md"] = "0" * 64
    if MUTATION == "audit_drift":
        source_expectations[
            "research/r075j_mean_zero_adjoint_flux_obstruction_primary_audit.md"
        ] = "0" * 64
    if MUTATION == "report_source_drift":
        source_expectations["research/r075j_report-source.md"] = "0" * 64
    if MUTATION == "dependency_drift":
        source_expectations[
            "research/r075f_modal_phase_integration_identity.md"
        ] = "0" * 64
    source_rows = {
        path: {"expectedSha256": digest, "observedSha256": sha256(ROOT / path)}
        for path, digest in sorted(source_expectations.items())
    }
    fixture_expected_hash = "0" * 64 if MUTATION == "fixture_drift" else FIXTURES_SHA256
    expected_expected_hash = "0" * 64 if MUTATION == "expected_drift" else EXPECTED_SHA256
    fixture_hash = sha256(FIXTURES)
    expected_hash = sha256(EXPECTED)

    # J.1 and J.11: operator and passive-square signs.
    operator = fixtures["operatorCase"]
    forward = {key: q(value) for key, value in operator["forward"].items()}
    adjoint = {key: q(value) for key, value in operator["adjoint"].items()}
    if MUTATION == "forward_time_sign":
        forward["time"] *= -1
    if MUTATION == "forward_drift_sign":
        forward["drift"] *= -1
    if MUTATION == "forward_diffusion_sign":
        forward["laplacian"] *= -1
    if MUTATION == "adjoint_time_sign":
        adjoint["time"] *= -1
    if MUTATION == "adjoint_drift_sign":
        adjoint["drift"] *= -1
    if MUTATION == "adjoint_diffusion_sign":
        adjoint["laplacian"] *= -1
    divergence_term = Q(1) if MUTATION == "drift_divergence" else Q(0)
    square_dissipation = q(operator["squareDissipationCoefficient"])
    if MUTATION == "square_diss_sign":
        square_dissipation *= -1
    if MUTATION == "square_diss_factor":
        square_dissipation /= 2
    operator_observed = {
        "forward": {key: qtext(value) for key, value in forward.items()},
        "adjoint": {key: qtext(value) for key, value in adjoint.items()},
        "driftDivergenceTerm": qtext(divergence_term),
        "squareDissipationCoefficient": qtext(square_dissipation),
    }

    # J.7: finite product quadrature preserving the pointwise-in-(t,x1)
    # derivative cancellation for each x3 cell.
    physical = fixtures["physicalDerivativeSourceCase"]
    eta = q(physical["eta"])
    x2_measures = [q(value) for value in physical["x2CellMeasures"]]
    derivatives = [q(value) for value in physical["cutoffDerivativeValues"]]
    if MUTATION == "derivative_source_abs":
        derivatives = [abs(value) for value in derivatives]
    if MUTATION == "derivative_source_positive":
        derivatives = [max(value, Q(0)) for value in derivatives]
    x3_measures = [q(value) for value in physical["x3CellMeasures"]]
    drifts = [q(value) for value in physical["driftValues"]]
    derivative_means = []
    source_means = []
    for drift in drifts:
        derivative_mean = sum(
            measure * value for measure, value in zip(x2_measures, derivatives)
        )
        derivative_means.append(derivative_mean)
        if MUTATION == "source_b_x2":
            local_drifts = [drift, drift + 1]
            source_mean = eta * sum(
                measure * local_drift * derivative
                for measure, local_drift, derivative
                in zip(x2_measures, local_drifts, derivatives)
            )
        else:
            source_mean = eta * drift * derivative_mean
        source_means.append(source_mean)
    total_signed_mean = sum(
        measure * value for measure, value in zip(x3_measures, source_means)
    )
    drift_average = sum(
        measure * value for measure, value in zip(x3_measures, drifts)
    )
    original_derivatives = [q(value) for value in physical["cutoffDerivativeValues"]]
    positive_derivative_mean = sum(
        measure * max(value, Q(0))
        for measure, value in zip(x2_measures, original_derivatives)
    )
    absolute_derivative_mean = sum(
        measure * abs(value)
        for measure, value in zip(x2_measures, original_derivatives)
    )
    physical_observed = {
        "derivativeMeanByX3Cell": [qtext(value) for value in derivative_means],
        "sourceMeanByX3Cell": [qtext(value) for value in source_means],
        "totalSignedMean": qtext(total_signed_mean),
        "positivePartMean": qtext(eta * drift_average * positive_derivative_mean),
        "absoluteMean": qtext(eta * drift_average * absolute_derivative_mean),
        "positivePartEqualsSignedSource": MUTATION == "positive_source_equal",
        "quantifier": "integrated-only" if MUTATION == "source_mean_quantifier" else "every-(t,x1)",
    }

    # Fully rational Fourier-coefficient computation for the requested
    # zero-terminal adjoint fixture, with tau=1-t.
    explicit = fixtures["explicitAdjointCase"]
    a_poly = [q(value) for value in explicit["AInTau"]]
    b_poly_field = [q(value) for value in explicit["BInTau"]]
    drift_poly = [q(value) for value in explicit["bInTau"]]
    if MUTATION == "A_sign":
        a_poly = poly_scale(a_poly, -1)
    if MUTATION == "B_sign":
        b_poly_field = poly_scale(b_poly_field, -1)
    if MUTATION == "b_sign":
        drift_poly[1] *= -1
    if MUTATION == "terminal_nonzero":
        a_poly[0] += 1
    tau_time_factor = Q(-1) if MUTATION == "tau_direction" else Q(1)
    # -s_t d/dt = -s_t*(-d/dtau), with the final tau_time_factor mutating
    # the chain-rule orientation.
    cos_poly = poly_add(
        poly_scale(poly_derivative(a_poly), -adjoint["time"] * tau_time_factor),
        poly_scale(poly_multiply(drift_poly, b_poly_field), adjoint["drift"]),
        poly_scale(a_poly, -adjoint["laplacian"]),
    )
    sin_poly = poly_add(
        poly_scale(poly_derivative(b_poly_field), -adjoint["time"] * tau_time_factor),
        poly_scale(poly_multiply(drift_poly, a_poly), -adjoint["drift"]),
        poly_scale(b_poly_field, -adjoint["laplacian"]),
    )
    source_cos = [Q(1), Q(1), Q(2), Q(1)]
    source_sin = [Q(0)]
    if MUTATION == "adjoint_source_cos":
        source_cos[2] += 1
    if MUTATION == "adjoint_source_sin":
        source_sin[0] = 1
    eta_samples = []
    sample_taus = [q(value) for value in explicit["sampleTau"]]
    eta_denominator = [Q(2), Q(-1)] if MUTATION == "eta_denominator" else drift_poly
    for tau in sample_taus:
        eta_samples.append(poly_eval(source_cos, tau) / poly_eval(eta_denominator, tau))
    eta_numerator_minimum = min(poly_eval(source_cos, Q(0)), poly_eval(source_cos, Q(1)))
    eta_denominator_minimum = min(
        poly_eval(eta_denominator, Q(0)), poly_eval(eta_denominator, Q(1))
    )
    eta_positive_on_interval = (
        eta_numerator_minimum > 0
        and eta_denominator_minimum > 0
        and all(coefficient >= 0 for coefficient in source_cos)
        and len(eta_denominator) <= 2
    )
    if MUTATION == "eta_positive":
        eta_positive_on_interval = False
    slice_samples = []
    for tau in sample_taus[1:]:
        at_zero = poly_eval(a_poly, tau)
        at_pi = -at_zero
        if MUTATION == "slice_sign":
            at_pi *= -1
        slice_samples.append({
            "tau": qtext(tau),
            "atX0": qtext(at_zero),
            "atXPi": qtext(at_pi),
        })
    explicit_observed = {
        "cosineCoefficientsInTau": poly_json(cos_poly, 3),
        "sineCoefficientsInTau": poly_json(sin_poly, 3),
        "sourceCosineCoefficientsInTau": poly_json(source_cos, 3),
        "terminalA": qtext(poly_eval(a_poly, Q(0))),
        "terminalB": qtext(poly_eval(b_poly_field, Q(0))),
        "etaSamples": [qtext(value) for value in eta_samples],
        "etaNumeratorMinimumOnUnitInterval": qtext(eta_numerator_minimum),
        "etaDenominatorMinimumOnUnitInterval": qtext(eta_denominator_minimum),
        "etaPositiveOnUnitInterval": eta_positive_on_interval,
        "sliceSamples": slice_samples,
        "nonzeroSlicesChangeSign": MUTATION != "sign_change_false",
    }
    eta_positive = eta_positive_on_interval and all(value > 0 for value in eta_samples)

    # J.12: endpoint and bulk signs.
    duality = fixtures["dualityCase"]
    initial = q(duality["initialBoundary"])
    terminal = q(duality["terminalBoundary"])
    bulk = q(duality["bulkLg"])
    initial_coefficient = Q(-1) if MUTATION == "j12_initial_sign" else Q(1)
    terminal_coefficient = Q(1) if MUTATION == "j12_terminal_sign" else Q(-1)
    bulk_coefficient = Q(-1) if MUTATION == "j12_bulk_sign" else Q(1)
    if MUTATION == "j12_endpoint_swap":
        initial, terminal = terminal, initial
    duality_rhs = initial_coefficient * initial + terminal_coefficient * terminal + bulk_coefficient * bulk
    source_pairing = q(duality["sourcePairing"])
    if MUTATION == "j12_source_pairing":
        source_pairing += 1
    duality_observed = {
        "initialCoefficient": qtext(initial_coefficient),
        "terminalCoefficient": qtext(terminal_coefficient),
        "bulkCoefficient": qtext(bulk_coefficient),
        "rhs": qtext(duality_rhs),
        "sourcePairing": qtext(source_pairing),
        "residual": qtext(duality_rhs - source_pairing),
    }

    # J.5 and J.13: exact signed decomposition and upper-bound signs.
    signed = fixtures["signedDissipationCase"]
    initial_plus = q(signed["initialPsiPlus"])
    initial_minus = q(signed["initialPsiMinus"])
    diss_plus = q(signed["dissipationPsiPlus"])
    diss_minus = q(signed["dissipationPsiMinus"])
    if MUTATION == "signed_decomposition":
        initial_minus *= -1
    j5_initial_coefficient = Q(1) if MUTATION == "j5_half" else Q(1, 2)
    j5_diss_coefficient = Q(1) if MUTATION == "j5_diss_sign" else Q(-1)
    exact_flux = (
        j5_initial_coefficient * (initial_plus - initial_minus)
        + j5_diss_coefficient * (diss_plus - diss_minus)
    )
    j13_initial_coefficient = Q(-1, 2) if MUTATION == "j13_initial_sign" else Q(1, 2)
    j13_diss_coefficient = Q(-1) if MUTATION == "j13_diss_sign" else Q(1)
    upper_bound = (
        j13_initial_coefficient * initial_plus
        + j13_diss_coefficient * diss_minus
    )
    if MUTATION == "j13_drop_negative_initial":
        upper_bound += Q(1, 2) * initial_minus
    signed_observed = {
        "squareDissipationCoefficient": qtext(square_dissipation),
        "J5InitialCoefficient": qtext(j5_initial_coefficient),
        "J5DissipationCoefficient": qtext(j5_diss_coefficient),
        "exactFlux": qtext(exact_flux),
        "J13InitialPositiveCoefficient": qtext(j13_initial_coefficient),
        "J13NegativeDissipationCoefficient": qtext(j13_diss_coefficient),
        "upperBound": qtext(upper_bound),
        "upperSlack": qtext(upper_bound - exact_flux),
    }

    # J.14--J.18: global energy identity and exact constant cancellation.
    shift = fixtures["constantShiftCase"]
    constant = q(shift["C"])
    energy_initial = q(shift["energyInitial"])
    energy_terminal = q(shift["energyTerminal"])
    dissipation = q(shift["dissipation"])
    endpoint_sign = Q(1) if MUTATION == "energy_endpoint_sign" else Q(-1)
    dissipation_factor = Q(1) if MUTATION == "energy_factor" else Q(2)
    energy_residual = energy_initial + endpoint_sign * energy_terminal - dissipation_factor * dissipation
    homogeneous_source = Q(1) if MUTATION == "constant_homogeneous" else Q(0)
    initial_constant = (
        (-Q(1, 2) if MUTATION == "shift_initial_sign" else Q(1, 2))
        * constant * energy_initial
    )
    terminal_constant = (
        (Q(1, 2) if MUTATION == "shift_terminal_sign" else -Q(1, 2))
        * constant * energy_terminal
    )
    dissipation_constant = (
        (Q(1) if MUTATION == "shift_diss_sign" else Q(-1))
        * constant * dissipation
    )
    exact_constant_sum = initial_constant + terminal_constant + dissipation_constant
    if MUTATION == "exact_shift_nonzero":
        exact_constant_sum += 1
    surcharge = (
        Q(1, 4) if MUTATION == "surcharge_half" else Q(1, 2)
    ) * constant * (energy_initial - energy_terminal)
    c_times_d = constant * dissipation
    if MUTATION == "surcharge_not_cd":
        c_times_d += 1
    shift_observed = {
        "energyIdentityResidual": qtext(energy_residual),
        "homogeneousAdjointSource": qtext(homogeneous_source),
        "initialConstantContribution": qtext(initial_constant),
        "terminalConstantContribution": qtext(terminal_constant),
        "dissipationConstantContribution": qtext(dissipation_constant),
        "exactConstantSum": qtext(exact_constant_sum),
        "droppedDissipationSurcharge": qtext(surcharge),
        "CtimesD": qtext(c_times_d),
    }

    # J.19--J.20: nonnegative majorant direction and favorable rows.
    majorant = fixtures["majorantCase"]
    half_source = q(majorant["halfSourcePairing"])
    if MUTATION == "majorant_source_direction":
        half_source += 1
    majorant_half = Q(1) if MUTATION == "majorant_half" else Q(1, 2)
    half_initial = majorant_half * q(majorant["initialPairing"])
    terminal_row = (
        majorant_half if MUTATION == "majorant_terminal_sign" else -majorant_half
    ) * q(majorant["terminalPairing"])
    dissipation_row = (
        Q(1) if MUTATION == "majorant_diss_sign" else Q(-1)
    ) * q(majorant["weightedDissipation"])
    exact_majorant_rhs = half_initial + terminal_row + dissipation_row
    majorant_observed = {
        "direction": "a>=LstarPhi" if MUTATION == "majorant_direction" else "a<=LstarPhi",
        "PhiNonnegative": False if MUTATION == "phi_nonnegative" else bool(majorant["PhiNonnegative"]),
        "terminalNonnegative": False if MUTATION == "terminal_nonnegative" else bool(majorant["terminalNonnegative"]),
        "halfSourcePairing": qtext(half_source),
        "halfInitialRow": qtext(half_initial),
        "negativeHalfTerminalRow": qtext(terminal_row),
        "negativeDissipationRow": qtext(dissipation_row),
        "exactMajorantRhs": qtext(exact_majorant_rhs),
        "boundaryOnlyUpper": qtext(half_initial),
        "terminalTermFavorable": MUTATION != "favorable_terminal",
        "dissipationTermFavorable": MUTATION != "favorable_dissipation",
    }

    tags = re.findall(r"\\tag\{(J\.[^}]+)\}", text)
    if MUTATION == "tag":
        tags.append("J.1")
    references = [
        "J." + value for value in re.findall(r"\(J\.([0-9]+[a-z]?)\)", text)
    ]
    if MUTATION == "reference":
        references.append("J.99")
    display_open = sum(line.strip() == r"\[" for line in text.splitlines())
    display_close = sum(line.strip() == r"\]" for line in text.splitlines())
    if MUTATION == "display":
        display_open += 1
    expected_tags = [f"J.{index}" for index in range(1, 21)]

    dependency_paths = (
        "research/r075e_horizontal_cross_mode_flux_reduction.md",
        "research/r075f_modal_phase_integration_identity.md",
        "research/r075h_single_pass_transport_flux_closure.md",
        "research/r075i_diffusion_safe_block_participation.md",
    )
    dependency_table_present = all(
        any(path in line and FROZEN_SOURCES[path] in line for line in text.splitlines())
        for path in dependency_paths
    )
    if MUTATION == "dependency_table_missing":
        dependency_table_present = False

    required_tokens = (
        r"\mathcal L:=\partial_t+b(t,x_3)\partial_2-\Delta_{23}",
        r"\mathcal L^*:=-\partial_t-b(t,x_3)\partial_2-\Delta_{23}",
        r"\int_{\mathbb T^2_{23}}a(t,x_1,x_2,x_3)\,dx_2dx_3",
        r"-\frac d{dt}\int_{\mathbb T^2_{23}}\psi",
        r"\mathcal Lg=-2|\nabla_{23}F|^2",
        r"\int_{\mathbb T^3}\phi(s)g(s)",
        r"-\int_{\mathbb T^3}\phi(t_2)g(t_2)",
        r"+\int_s^{t_2}\!\int\phi\,\mathcal Lg",
        r"E(s)-E(t_2)=2D",
        r"\frac C2\bigl(E(s)-E(t_2)\bigr)-CD=0",
        r"a\le\mathcal L^*\Phi",
        "Replacing `a` by `|a|` or `a_+` changes the equation",
        "does not construct the paid majorant or close E.24",
        "It is not a no-go theorem for all resolvent or Feynman--Kac methods",
        r"\mathbf{NOT\ CLAY}",
    )

    boundary = {
        "backwardProblemIsAdjointNotPassiveIllPosedness": MUTATION != "pde_backward",
        "exactAdjointForcedSignChanging": MUTATION != "exact_adjoint_nonnegative",
        "positivePartIsNotPhysicalSignedSource": MUTATION not in (
            "aplus_signed", "positive_source_equal"
        ),
        "majorantInitialRowUnpaid": MUTATION != "majorant_paid",
        "negativeAdjointDissipationUnpaid": MUTATION != "uncontrolled_dissipation_paid",
        "constantShiftNotFree": MUTATION != "free_shift",
        "notBlanketNoGoForAdjointMethods": MUTATION != "blanket_no_go",
        "FeynmanKacMajorantPaymentOpen": MUTATION != "feynman_kac_closed",
        "transitionGeometryOpen": MUTATION != "transition_closed",
        "periodicRecrossingOpen": MUTATION != "periodic_closed",
        "E24Open": MUTATION != "e24_closed",
        "completeClockOpen": MUTATION != "complete_clock",
        "fixedDeletionOpen": MUTATION != "fixed_deletion",
        "suitableWeakTransferOpen": MUTATION != "suitable_weak",
        "regularityOpen": MUTATION != "regularity",
        "singularityOpen": MUTATION != "singularity",
        "noSimulationUsed": MUTATION != "simulation_used",
        "noNoveltyOrPriorityClaim": MUTATION != "novelty",
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
            and fixtures["schema"] == "r075j-mean-zero-adjoint-flux-obstruction-fixtures-v1"
            and expected["schema"] == "r075j-mean-zero-adjoint-flux-obstruction-expected-v1"
            and fixtures["frozenSources"] == FROZEN_SOURCES,
            fixtures={"expected": fixture_expected_hash, "observed": fixture_hash},
            expected={"expected": expected_expected_hash, "observed": expected_hash},
        ),
        "primaryAuditBindingAndStatus": record(
            FROZEN_SOURCES["research/r075j_mean_zero_adjoint_flux_obstruction.md"] in audit_text
            and "Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0." in audit_text
            and "Equation tags J.1--J.20 are unique and consecutive." in audit_text
            and "All 20 display-math environments are paired." in audit_text,
        ),
        "fourDependencyTableBindings": record(dependency_table_present),
        "forwardAdjointAndSquareSigns": record(
            operator_observed == expected["operators"],
            observed=operator_observed,
        ),
        "physicalDerivativeSourceMeanZeroEverySlice": record(
            physical_observed == expected["physicalSource"]
            and all(value == 0 for value in derivative_means + source_means)
            and total_signed_mean == 0,
            observed=physical_observed,
        ),
        "positivePartIsDifferentSource": record(
            physical_observed["positivePartMean"] == "6"
            and physical_observed["absoluteMean"] == "12"
            and not physical_observed["positivePartEqualsSignedSource"],
        ),
        "explicitAdjointPolynomialIdentity": record(
            explicit_observed == expected["explicitAdjoint"]
            and cos_poly == source_cos and sin_poly == source_sin,
            observed=explicit_observed,
        ),
        "explicitTerminalEtaAndSliceSigns": record(
            poly_eval(a_poly, Q(0)) == poly_eval(b_poly_field, Q(0)) == 0
            and eta_positive
            and all(q(row["atX0"]) > 0 > q(row["atXPi"]) for row in slice_samples)
            and explicit_observed["nonzeroSlicesChangeSign"],
        ),
        "dualityJ12EndpointAndBulkSigns": record(
            duality_observed == expected["duality"] and duality_rhs == source_pairing,
            observed=duality_observed,
        ),
        "J5AndJ13DissipationSigns": record(
            signed_observed == expected["signedDissipation"]
            and exact_flux <= upper_bound,
            observed=signed_observed,
        ),
        "constantShiftExactCancellation": record(
            shift_observed == expected["constantShift"]
            and energy_residual == homogeneous_source == exact_constant_sum == 0,
            observed=shift_observed,
        ),
        "droppedDissipationCreatesCDSurcharge": record(
            surcharge == c_times_d > 0,
            observed=shift_observed,
        ),
        "nonnegativeMajorantDirectionAndFavorableRows": record(
            majorant_observed == expected["majorant"]
            and half_source <= exact_majorant_rhs <= half_initial
            and terminal_row <= 0 and dissipation_row <= 0,
            observed=majorant_observed,
        ),
        "tagsReferencesAndDisplays": record(
            tags == expected_tags and len(set(tags)) == 20
            and not (set(references) - set(tags))
            and display_open == display_close == 20,
            tags=tags,
            references=sorted(set(references)),
            displays={"open": display_open, "close": display_close},
        ),
        "formulaAndStatusSentinels": record(
            all(re.sub(r"\s+", " ", token) in flat_text for token in required_tokens),
        ),
        "sourceReportBoundary": record(
            "does not establish novelty" in source_text
            and "Viable but open" in source_text,
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
        "physicalSource": physical_observed,
        "explicitAdjoint": explicit_observed,
        "duality": duality_observed,
        "signedDissipation": signed_observed,
        "constantShift": shift_observed,
        "majorant": majorant_observed,
        "claimBoundary": boundary,
    }
    OUT_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    failed = [name for name, item in checks.items() if not item["pass"]]
    OUT_REPORT.write_text(
        "# R0.75J finite certificate report\n\n"
        f"- Verdict: **{verdict}**\n"
        f"- Assertions: {payload['assertions']['passed']}/{payload['assertions']['total']}\n"
        f"- Main SHA-256: {sha256(MAIN)}\n"
        f"- Fixture SHA-256: {fixture_hash}\n"
        f"- Expected SHA-256: {expected_hash}\n"
        f"- Failed checks: {'none' if not failed else '; '.join(failed)}\n\n"
        "Exact rational Fourier arithmetic verifies the forward/adjoint signs "
        "and the requested tau-polynomial fixture: L*psi has cosine coefficient "
        "1+tau+2tau^2+tau^3, zero sine coefficient, zero terminal data, positive "
        "eta samples, and both signs on every sampled nonzero slice.\n\n"
        "Finite product quadrature verifies zero mean of the physical derivative "
        "source for each fixed parameter slice and distinguishes a_+ and |a|. "
        "The J.12 endpoint signs, J.5/J.13 dissipation signs, constant-shift "
        "cancellation, CD surcharge, and nonnegative-majorant direction are all "
        "recomputed exactly.\n\n"
        "The signed exact adjoint is not a nonnegative majorant. The a_+-driven "
        "majorant changes the source and its initial row remains unpaid. This is "
        "not a blanket no-go theorem for adjoint or Feynman--Kac methods. E.24 "
        "and all larger claims remain OPEN. **NOT CLAY.**\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "suite": "r075j-mean-zero-adjoint-flux-obstruction",
        "verdict": verdict,
        "assertions": len(checks),
    }, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
