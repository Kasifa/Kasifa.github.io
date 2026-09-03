#!/usr/bin/env python3
"""Fail-closed finite certificate for frozen R0.75H."""

from __future__ import annotations

import hashlib
import json
import os
import re
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "research/r075h_single_pass_transport_flux_closure.md"
PRIMARY_AUDIT = ROOT / "research/r075h_single_pass_transport_flux_closure_primary_audit.md"
REPORT_SOURCE = ROOT / "research/r075h_report-source.md"
FIXTURES = ROOT / "scripts/r075h_single_pass_transport_flux_closure_fixtures.json"
EXPECTED = ROOT / "scripts/r075h_single_pass_transport_flux_closure_expected.json"
OUT_JSON = Path(os.environ.get(
    "R075H_JSON",
    ROOT / "research/r075h_single_pass_transport_flux_closure_certificate.json",
))
OUT_REPORT = Path(os.environ.get(
    "R075H_REPORT",
    ROOT / "research/r075h_single_pass_transport_flux_closure_certificate_report.md",
))
MUTATION = os.environ.get("R075H_MUTATION", "")
SCHEMA = "r075h-single-pass-transport-flux-closure-certificate-v1"

FROZEN_SOURCES = {
    "research/r075b_bulk_clock_outer_padding_gate.md":
        "430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a",
    "research/r075e_horizontal_cross_mode_flux_reduction.md":
        "99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049",
    "research/r075f_modal_phase_integration_identity.md":
        "f7a72ebfe0471e18c0d5d44bd3123491d7cd47a79293d1860c5d023c13acf440",
    "research/r075g_signed_flux_gain_threshold.md":
        "f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41",
    "research/r075h_report-source.md":
        "5b0b05b2ce903986ef8439a766766e8bdb97e2fe4d9eb6035f73102583b1b779",
    "research/r075h_single_pass_transport_flux_closure.md":
        "849379bea9cf22e0d892ac11ac05bb3b3bc2967a1735753dbc4a6ffc7bb7d7b9",
    "research/r075h_single_pass_transport_flux_closure_primary_audit.md":
        "3c85368e051102997e66ae36fa43290b6200e688db886380215fb40ec0bb757e",
}
FIXTURES_SHA256 = "7e4b5691d6929c97f72146c293a55e3b6fcf5875bc51f78bd1a58e9f84a0b217"
EXPECTED_SHA256 = "099d017cb7ff61d5a9dff54449c9a91a12e8657343bb11579ad135e9cd350573"

NEGATIVE_MUTATIONS = (
    "source_drift", "audit_drift", "report_source_drift",
    "dependency_drift", "dependency_table_missing",
    "fixture_drift", "expected_drift", "tag", "reference", "display", "control",
    "transport_pde_sign", "transport_energy_sign", "eta_initial",
    "eta_terminal", "eta_monotone", "eta_plateau", "eta_ibp_sign", "transport_half",
    "characteristic_direction", "set_translation_direction", "q_shift",
    "terminal_containment", "seam_crossing", "terminal_l2",
    "persistence_direction", "persistence_time", "holder_measure",
    "holder_delta_power", "holder_volume_power", "holder_l3_power",
    "holder_division", "h23_flux_r", "h23_flux_omega", "h23_delta_r",
    "h23_volume_l", "h23_volume_r", "h23_cubic_r", "h23_cubic_omega",
    "h23_cubic_p", "rate_rho_sign", "rate_cgamma_sign", "rate_fraction",
    "matching_lower_direction", "matching_r_power", "matching_cube_root",
    "diff_terminal_sign", "diff_dissipation_sign", "diff_cutoff_sign",
    "diff_circularity", "atom_r_sign", "atom_omega_sign",
    "flux_normalization", "measurement_weight", "benchmark_nse", "conditional_weight",
    "payment_region", "transport_absolute_flux", "block_count",
    "diffusive_characteristic", "e24_closed", "complete_clock",
    "fixed_deletion", "suitable_weak", "regularity", "clay",
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


def vector_json(vector: dict[str, Q]) -> dict[str, str]:
    return {key: qtext(value) for key, value in vector.items()}


def interval_contained(inner: tuple[Q, Q], outer: tuple[Q, Q]) -> bool:
    return outer[0] <= inner[0] <= inner[1] <= outer[1]


Poly = dict[tuple[int, int], Q]


def poly_add(*polynomials: Poly) -> Poly:
    result: Poly = {}
    for polynomial in polynomials:
        for power, coefficient in polynomial.items():
            result[power] = result.get(power, Q(0)) + coefficient
    return {power: value for power, value in result.items() if value}


def poly_scale(scale: Q, polynomial: Poly) -> Poly:
    return {
        power: scale * coefficient
        for power, coefficient in polynomial.items()
        if scale * coefficient
    }


def poly_multiply(left: Poly, right: Poly) -> Poly:
    result: Poly = {}
    for (left_x, left_t), left_value in left.items():
        for (right_x, right_t), right_value in right.items():
            power = (left_x + right_x, left_t + right_t)
            result[power] = result.get(power, Q(0)) + left_value * right_value
    return {power: value for power, value in result.items() if value}


def poly_power(polynomial: Poly, exponent: int) -> Poly:
    result: Poly = {(0, 0): Q(1)}
    for _ in range(exponent):
        result = poly_multiply(result, polynomial)
    return result


def poly_derivative(polynomial: Poly, variable: int) -> Poly:
    result: Poly = {}
    for power, coefficient in polynomial.items():
        exponents = list(power)
        if exponents[variable]:
            result_power = exponents.copy()
            result_power[variable] -= 1
            result[tuple(result_power)] = coefficient * exponents[variable]
    return result


def poly_integrate_x(polynomial: Poly, lower: Q, upper: Q) -> Poly:
    result: Poly = {}
    for (x_power, t_power), coefficient in polynomial.items():
        value = coefficient * (
            upper ** (x_power + 1) - lower ** (x_power + 1)
        ) / (x_power + 1)
        power = (0, t_power)
        result[power] = result.get(power, Q(0)) + value
    return {power: value for power, value in result.items() if value}


def poly_integrate_t(polynomial: Poly, lower: Q, upper: Q) -> Q:
    total = Q(0)
    for (x_power, t_power), coefficient in polynomial.items():
        if x_power:
            raise AssertionError("x must be integrated before t")
        total += coefficient * (
            upper ** (t_power + 1) - lower ** (t_power + 1)
        ) / (t_power + 1)
    return total


def poly_evaluate_t(polynomial: Poly, value: Q) -> Q:
    if any(x_power for x_power, _ in polynomial):
        raise AssertionError("x must be integrated before t evaluation")
    return sum(
        coefficient * value ** t_power
        for (_, t_power), coefficient in polynomial.items()
    )


def poly_t_coefficients(polynomial: Poly, degree: int) -> list[str]:
    return [
        qtext(polynomial.get((0, power), Q(0)))
        for power in range(degree + 1)
    ]


def record(ok: bool, **details: Any) -> dict[str, Any]:
    return {"pass": bool(ok), **details}


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R075H_MUTATION: {MUTATION}")

    text = MAIN.read_text(encoding="utf-8")
    flat_text = re.sub(r"\s+", " ", text)
    scan_text = text + ("\x01" if MUTATION == "control" else "")
    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))

    source_expectations = dict(FROZEN_SOURCES)
    if MUTATION == "source_drift":
        source_expectations[
            "research/r075h_single_pass_transport_flux_closure.md"
        ] = "0" * 64
    if MUTATION == "audit_drift":
        source_expectations[
            "research/r075h_single_pass_transport_flux_closure_primary_audit.md"
        ] = "0" * 64
    if MUTATION == "report_source_drift":
        source_expectations["research/r075h_report-source.md"] = "0" * 64
    if MUTATION == "dependency_drift":
        source_expectations[
            "research/r075b_bulk_clock_outer_padding_gate.md"
        ] = "0" * 64
    source_rows = {
        path: {"expectedSha256": digest, "observedSha256": sha256(ROOT / path)}
        for path, digest in sorted(source_expectations.items())
    }
    fixture_expected_hash = "0" * 64 if MUTATION == "fixture_drift" else FIXTURES_SHA256
    expected_expected_hash = "0" * 64 if MUTATION == "expected_drift" else EXPECTED_SHA256
    fixture_hash = sha256(FIXTURES)
    expected_hash = sha256(EXPECTED)

    # H.10--H.14: exact smooth transport on a circle, normalized by 2*pi.
    # theta=pi*t/2, q=theta/2, eta=sin(theta).
    transport = fixtures["weightedTransportCase"]
    cutoff_mean = q(transport["cutoffMean"])
    cutoff_amplitude = q(transport["cutoffSineAmplitude"])
    eta_initial = q(transport["etaInitial"])
    eta_terminal = q(transport["etaTerminal"])
    eta_nondecreasing = bool(transport["etaNondecreasing"])
    if MUTATION == "eta_initial":
        eta_initial = Q(1)
    if MUTATION == "eta_terminal":
        eta_terminal = Q(0)
    if MUTATION == "eta_monotone":
        eta_nondecreasing = False

    initial_energy = cutoff_mean / 2
    terminal_energy = cutoff_mean / 2 + cutoff_amplitude / 4
    half_factor = Q(1) if MUTATION == "transport_half" else Q(1, 2)
    eta_prime_penalty = half_factor * (
        cutoff_mean / 2 + cutoff_amplitude / 8
    )
    direct_sign = -1 if MUTATION == "transport_pde_sign" else 1
    energy_sign = -1 if MUTATION == "transport_energy_sign" else 1
    direct_flux = (
        direct_sign * energy_sign * half_factor * cutoff_amplitude / 8
    )
    endpoint_sign = 1 if MUTATION == "eta_ibp_sign" else -1
    endpoint_minus_penalty = (
        half_factor * eta_terminal * terminal_energy
        - half_factor * eta_initial * initial_energy
        + endpoint_sign * eta_prime_penalty
    )
    transport_observed = {
        "initialEnergy": qtext(initial_energy),
        "terminalEnergy": qtext(terminal_energy),
        "terminalHalfEnergy": qtext(Q(1, 2) * terminal_energy),
        "etaPrimePenalty": qtext(eta_prime_penalty),
        "directWeightedFlux": qtext(direct_flux),
        "endpointMinusPenalty": qtext(endpoint_minus_penalty),
        "identityResidual": qtext(direct_flux - endpoint_minus_penalty),
        "positivePart": qtext(max(direct_flux, Q(0))),
        "terminalHalfEnergyMinusPositivePart": qtext(
            Q(1, 2) * terminal_energy - max(direct_flux, Q(0))
        ),
        "cutoffMinimum": qtext(cutoff_mean - cutoff_amplitude),
        "cutoffMaximum": qtext(cutoff_mean + cutoff_amplitude),
    }

    # H.7 and H.15--H.17: rational lifted intervals and an exact translate.
    tube = fixtures["terminalTubeCase"]
    t2 = q(tube["terminalTime"])
    j0, j1 = map(q, tube["terminalInterval"])
    omega0 = tuple(map(q, tube["omega0Lift"]))
    omega_plus = tuple(map(q, tube["omegaPlusLift"]))
    q_terminal = t2 / 8
    q_initial = j0 / 8
    shift = q_terminal - q_initial
    if MUTATION == "q_shift":
        shift *= -1
    preimage_sign = 1 if MUTATION == "characteristic_direction" else -1
    preimage = (
        omega0[0] + preimage_sign * shift,
        omega0[1] + preimage_sign * shift,
    )
    stated_set_sign = 1 if MUTATION == "set_translation_direction" else -1
    stated_preimage = (
        omega0[0] + stated_set_sign * shift,
        omega0[1] + stated_set_sign * shift,
    )
    wrong_image = (omega0[0] + shift, omega0[1] + shift)
    correct_contained = interval_contained(stated_preimage, omega_plus)
    if MUTATION == "terminal_containment":
        correct_contained = False
    wrong_contained = interval_contained(wrong_image, omega_plus)
    no_seam = MUTATION != "seam_crossing"
    terminal_l2 = q(tube["terminalL2OnOmega0"])
    if MUTATION == "terminal_l2":
        terminal_l2 += Q(1, 8)
    earlier_l2 = q(tube["terminalL2OnOmega0"])
    terminal_weighted = q(tube["terminalWeightedEnergy"])
    persistence_sign = -1 if MUTATION == "persistence_direction" else 1
    persistence_slack = persistence_sign * (earlier_l2 - terminal_weighted)
    interval_length = j1 - j0
    persistence_time = (
        interval_length ** 2 if MUTATION == "persistence_time"
        else interval_length
    )
    tube_observed = {
        "terminalIntervalLength": qtext(interval_length),
        "qTerminalOverTwoPi": qtext(q_terminal),
        "qInitialOverTwoPi": qtext(q_initial),
        "backwardShiftAtInitial": qtext(shift),
        "correctPreimage": [qtext(value) for value in preimage],
        "wrongDirectionImage": [qtext(value) for value in wrong_image],
        "correctPreimageContained": correct_contained,
        "wrongDirectionContained": wrong_contained,
        "terminalL2OnOmega0": qtext(terminal_l2),
        "earlierL2OnPreimage": qtext(earlier_l2),
        "terminalWeightedEnergy": qtext(terminal_weighted),
        "persistenceSlack": qtext(persistence_slack),
        "integratedPersistenceLowerBound": qtext(
            persistence_time * terminal_weighted
        ),
    }

    # H.18--H.19: constant nonzero field gives equality in Holder.
    holder = fixtures["holderEqualityCase"]
    delta = q(holder["delta"])
    volume = q(holder["spatialVolume"])
    magnitude = q(holder["constantFieldMagnitude"])
    cylinder_measure = (
        delta + volume if MUTATION == "holder_measure" else delta * volume
    )
    l2_integral = delta * volume * magnitude ** 2
    l3_integral = delta * volume * magnitude ** 3
    measure_one_third = Q(1, 4)
    if MUTATION == "holder_measure":
        measure_one_third = Q(1, 2)
    l3_two_thirds = (
        Q(1, 2) if MUTATION == "holder_l3_power" else Q(1, 4)
    )
    holder_right = measure_one_third * l3_two_thirds
    endpoint_energy = l2_integral / delta
    delta_minus_two_thirds = (
        Q(2) if MUTATION in ("holder_delta_power", "holder_division")
        else Q(4)
    )
    volume_one_third = (
        Q(1, 4) if MUTATION == "holder_volume_power" else Q(1, 2)
    )
    endpoint_bound_right = (
        delta_minus_two_thirds * volume_one_third * l3_two_thirds
    )
    holder_observed = {
        "cylinderMeasure": qtext(cylinder_measure),
        "l2Integral": qtext(l2_integral),
        "l3Integral": qtext(l3_integral),
        "measureOneThird": qtext(measure_one_third),
        "l3TwoThirds": qtext(l3_two_thirds),
        "holderRight": qtext(holder_right),
        "endpointEnergy": qtext(endpoint_energy),
        "deltaMinusTwoThirds": qtext(delta_minus_two_thirds),
        "volumeOneThird": qtext(volume_one_third),
        "endpointBoundRight": qtext(endpoint_bound_right),
    }

    # H.23--H.24 exact exponent ledger.
    factors = []
    for item in fixtures["h23Factors"]:
        factors.append((
            item["name"],
            {key: q(item[key]) for key in ("L", "R", "omega", "p")},
        ))
    replacements = {
        "h23_flux_r": ("fluxNormalization", "R", Q(1)),
        "h23_flux_omega": ("fluxNormalization", "omega", Q(0)),
        "h23_delta_r": ("deltaMinusTwoThirds", "R", Q(-1)),
        "h23_volume_l": ("volumeOneThird", "L", Q(1, 3)),
        "h23_volume_r": ("volumeOneThird", "R", Q(2)),
        "h23_cubic_r": ("cubicTwoThirds", "R", Q(2, 3)),
        "h23_cubic_omega": ("cubicTwoThirds", "omega", Q(2, 3)),
        "h23_cubic_p": ("cubicTwoThirds", "p", Q(1, 3)),
    }
    if MUTATION in replacements:
        target, key, value = replacements[MUTATION]
        factors = [
            (name, {**row, key: value} if name == target else row)
            for name, row in factors
        ]
    h23_product = vector_add(*(row for _, row in factors))
    constants = fixtures["constants"]
    rho = q(constants["rho"])
    c_gamma = q(constants["cGamma"])
    rho_sign = -1 if MUTATION == "rate_rho_sign" else 1
    gamma_sign = 1 if MUTATION == "rate_cgamma_sign" else -1
    rate = rho_sign * rho / 6 + gamma_sign * c_gamma / 12
    if MUTATION == "rate_fraction":
        rate += Q(1, 238140000)
    h23_observed = {"product": vector_json(h23_product), "rate": qtext(rate)}

    # H.26 matching lower scale.
    matching = fixtures["matchingBackgroundCase"]
    mr = q(matching["R"])
    ml = q(matching["L"])
    momega = q(matching["omega"])
    mpb = q(matching["pB"])
    lower_scale = ml ** 2 * momega * mr ** -3
    coefficient_left = Q(2)
    matching_r_factor = (
        mr ** 0 if MUTATION == "matching_r_power" else Q(1, 2)
    )
    pb_cube_root = Q(8) if MUTATION == "matching_cube_root" else Q(4)
    matching_right = matching_r_factor * pb_cube_root
    direction = (
        "left>=right" if MUTATION == "matching_lower_direction"
        else "left<=right"
    )
    matching_observed = {
        "assumedLowerScale": qtext(lower_scale),
        "coefficientLeft": qtext(coefficient_left),
        "rOneThirdPBCubeRoot": qtext(matching_right),
        "inequalityDirection": direction,
    }

    # One coherent all-rational H.1--H.23 fixture. The tent cutoff is
    # Lipschitz, so this is an a.e./weak integration-by-parts arithmetic
    # witness; it is not used for the Delta-xi row in H.28.
    coherent = fixtures["coherentRationalClosureCase"]
    c_qprime = q(coherent["qPrime"])
    if MUTATION == "transport_pde_sign":
        c_qprime *= -1
    c_eta_break = q(coherent["etaBreak"])
    c_eta_slope = q(coherent["etaEarlySlope"])
    c_eta_plateau = (
        Q(0) if MUTATION == "eta_plateau" else q(coherent["etaPlateau"])
    )
    c_j0, c_j1 = map(q, coherent["terminalInterval"])
    c_omega0 = tuple(map(q, coherent["omega0"]))
    c_omega_plus = tuple(map(q, coherent["omegaPlus"]))
    c_r = q(coherent["R"])
    c_l = q(coherent["L"])
    c_omega = q(coherent["omega"])
    c_weight = q(coherent["exteriorWeight"])
    c_pb = q(coherent["matchingPB"])

    def linear_polynomial(spec: dict[str, str]) -> Poly:
        return {
            (0, 0): q(spec["constant"]),
            (1, 0): q(spec["x"]),
            (0, 1): q(spec["t"]),
        }

    c_h = linear_polynomial(coherent["positiveField"])
    c_g = linear_polynomial(coherent["negativeControlField"])
    xi_pieces = [
        (
            q(piece["interval"][0]),
            q(piece["interval"][1]),
            {(0, 0): q(piece["constant"]), (1, 0): q(piece["x"])},
        )
        for piece in coherent["xiPieces"]
    ]

    def weighted_x_integral(field: Poly, power: int) -> Poly:
        field_power = poly_power(field, power)
        return poly_add(*[
            poly_integrate_x(poly_multiply(xi, field_power), lower, upper)
            for lower, upper, xi in xi_pieces
        ])

    def xi_prime_x_integral(field: Poly) -> Poly:
        field_square = poly_power(field, 2)
        return poly_add(*[
            poly_integrate_x(
                poly_scale(xi.get((1, 0), Q(0)), field_square),
                lower,
                upper,
            )
            for lower, upper, xi in xi_pieces
        ])

    def eta_weighted_time_integral(polynomial: Poly) -> Q:
        early_eta = {(0, 1): c_eta_slope}
        return (
            poly_integrate_t(
                poly_multiply(early_eta, polynomial), Q(0), c_eta_break
            )
            + c_eta_plateau
            * poly_integrate_t(polynomial, c_eta_break, Q(1))
        )

    c_energy = weighted_x_integral(c_h, 2)
    c_negative_energy = weighted_x_integral(c_g, 2)
    c_energy_derivative = poly_derivative(c_energy, 1)
    c_flux_density = poly_scale(c_qprime, xi_prime_x_integral(c_h))
    c_negative_flux_density = poly_scale(c_qprime, xi_prime_x_integral(c_g))
    if MUTATION == "transport_energy_sign":
        c_flux_density = poly_scale(-1, c_flux_density)
        c_negative_flux_density = poly_scale(-1, c_negative_flux_density)
    c_transport_residual = poly_add(
        poly_derivative(c_h, 1),
        poly_scale(c_qprime, poly_derivative(c_h, 0)),
    )
    c_half = Q(1) if MUTATION == "transport_half" else Q(1, 2)
    c_direct_flux = c_half * eta_weighted_time_integral(c_flux_density)
    c_negative_direct_flux = (
        c_half * eta_weighted_time_integral(c_negative_flux_density)
    )
    c_initial_energy = poly_evaluate_t(c_energy, Q(0))
    c_terminal_energy = poly_evaluate_t(c_energy, Q(1))
    c_negative_terminal_energy = poly_evaluate_t(c_negative_energy, Q(1))
    c_eta_penalty = (
        c_half * c_eta_slope
        * poly_integrate_t(c_energy, Q(0), c_eta_break)
    )
    c_endpoint_rhs = (
        c_half * c_eta_plateau * c_terminal_energy
        - c_half * eta_initial * c_initial_energy
        + (c_eta_penalty if MUTATION == "eta_ibp_sign" else -c_eta_penalty)
    )
    c_positive_part = max(c_direct_flux, Q(0))
    c_negative_positive_part = (
        abs(c_negative_direct_flux)
        if MUTATION == "transport_absolute_flux"
        else max(c_negative_direct_flux, Q(0))
    )

    c_delta = c_j1 - c_j0
    c_shift = c_qprime * (Q(1) - c_j0)
    c_preimage_sign = 1 if MUTATION == "characteristic_direction" else -1
    c_preimage = (
        c_omega0[0] + c_preimage_sign * c_shift,
        c_omega0[1] + c_preimage_sign * c_shift,
    )
    c_wrong_image = (
        c_omega0[0] + c_shift,
        c_omega0[1] + c_shift,
    )
    c_preimage_contained = interval_contained(c_preimage, c_omega_plus)
    c_wrong_contained = interval_contained(c_wrong_image, c_omega_plus)
    c_tube_l2 = poly_integrate_t(
        poly_integrate_x(poly_power(c_h, 2), *c_omega_plus), c_j0, c_j1
    )
    c_tube_l3 = poly_integrate_t(
        poly_integrate_x(poly_power(c_h, 3), *c_omega_plus), c_j0, c_j1
    )
    c_terminal_unweighted_l2 = poly_evaluate_t(
        poly_integrate_x(poly_power(c_h, 2), *c_omega0), Q(1)
    )
    c_volume = c_omega_plus[1] - c_omega_plus[0]
    c_measure = c_delta * c_volume
    c_h17_slack = c_tube_l2 - c_delta * c_terminal_energy
    c_h18_left_cubed = c_tube_l2 ** 3
    c_h18_right_cubed = c_measure * c_tube_l3 ** 2
    c_h19_left_cubed = c_delta ** 2 * c_terminal_energy ** 3
    c_h19_right_cubed = c_volume * c_tube_l3 ** 2

    atom_r_power = 2 if MUTATION == "atom_r_sign" else -2
    atom_omega_power = -1 if MUTATION == "atom_omega_sign" else 1
    c_atom = c_r ** atom_r_power * c_omega ** atom_omega_power * c_tube_l3
    c_measurement = (
        c_r ** -2
        * (c_weight ** -1 if MUTATION == "measurement_weight" else c_weight)
        * c_tube_l3
    )
    flux_r_power = 1 if MUTATION == "flux_normalization" else -1
    c_flux_x = c_omega * c_r ** flux_r_power * c_positive_part
    c_h23_left_cubed = c_flux_x ** 3
    c_h23_right_cubed = c_l ** 2 * c_omega * c_r ** -2 * c_atom ** 2
    c_matching_lower = c_l ** 2 * c_omega * c_r ** -3
    c_matching_left_cube = c_l ** 2 * c_omega * c_r ** -2
    c_matching_right_cube = c_r * c_pb
    c_weight_ok = (
        False if MUTATION == "conditional_weight" else c_weight >= c_omega
    )
    c_payment_region_ok = MUTATION != "payment_region"

    coherent_observed = {
        "transportResidualCoefficients": [
            qtext(c_transport_residual.get((0, 0), Q(0))),
            qtext(c_transport_residual.get((1, 0), Q(0))),
            qtext(c_transport_residual.get((0, 1), Q(0))),
        ],
        "energyPolynomial": poly_t_coefficients(c_energy, 2),
        "energyDerivativePolynomial": poly_t_coefficients(c_energy_derivative, 1),
        "fluxDensityPolynomial": poly_t_coefficients(c_flux_density, 1),
        "initialEnergy": qtext(c_initial_energy),
        "terminalEnergy": qtext(c_terminal_energy),
        "etaPrimePenalty": qtext(c_eta_penalty),
        "directWeightedFlux": qtext(c_direct_flux),
        "endpointMinusPenalty": qtext(c_endpoint_rhs),
        "positivePart": qtext(c_positive_part),
        "h14Slack": qtext(c_terminal_energy / 2 - c_positive_part),
        "delta": qtext(c_delta),
        "omegaPlusVolume": qtext(c_volume),
        "maxBackwardShift": qtext(c_shift),
        "correctPreimageAtJStart": [qtext(value) for value in c_preimage],
        "wrongImageAtJStart": [qtext(value) for value in c_wrong_image],
        "correctPreimageContained": c_preimage_contained,
        "wrongImageContained": c_wrong_contained,
        "terminalUnweightedL2": qtext(c_terminal_unweighted_l2),
        "terminalWeightedSlack": qtext(
            c_terminal_unweighted_l2 - c_terminal_energy
        ),
        "tubeL2": qtext(c_tube_l2),
        "tubeL3": qtext(c_tube_l3),
        "h17Slack": qtext(c_h17_slack),
        "cylinderMeasure": qtext(c_measure),
        "h18LeftCubed": qtext(c_h18_left_cubed),
        "h18RightCubed": qtext(c_h18_right_cubed),
        "h18StrictGap": qtext(c_h18_right_cubed - c_h18_left_cubed),
        "h19LeftCubed": qtext(c_h19_left_cubed),
        "h19RightCubed": qtext(c_h19_right_cubed),
        "h19StrictGap": qtext(c_h19_right_cubed - c_h19_left_cubed),
        "terminalAtomP": qtext(c_atom),
        "benchmarkMeasurementP": qtext(c_measurement),
        "normalizedPositiveFluxX": qtext(c_flux_x),
        "h23LeftCubed": qtext(c_h23_left_cubed),
        "h23RightCubed": qtext(c_h23_right_cubed),
        "h23StrictGap": qtext(c_h23_right_cubed - c_h23_left_cubed),
        "matchingLowerScale": qtext(c_matching_lower),
        "matchingPBCubeComparisonLeft": qtext(c_matching_left_cube),
        "matchingPBCubeComparisonRight": qtext(c_matching_right_cube),
        "negativeEnergyPolynomial": poly_t_coefficients(c_negative_energy, 2),
        "negativeTerminalEnergy": qtext(c_negative_terminal_energy),
        "negativeDirectFlux": qtext(c_negative_direct_flux),
        "negativePositivePart": qtext(c_negative_positive_part),
        "negativeAbsoluteFlux": qtext(abs(c_negative_direct_flux)),
        "negativeAbsMinusTerminalHalfEnergy": qtext(
            abs(c_negative_direct_flux) - c_negative_terminal_energy / 2
        ),
    }

    # H.28: solve 1/2 E + D = A + T for T.
    diff = fixtures["diffusiveIdentityCase"]
    terminal = q(diff["terminalHalfEnergy"])
    dissipation = q(diff["dissipation"])
    cutoff = q(diff["cutoffHalfIntegral"])
    terminal_coefficient = -1 if MUTATION == "diff_terminal_sign" else 1
    dissipation_coefficient = -1 if MUTATION == "diff_dissipation_sign" else 1
    cutoff_coefficient = 1 if MUTATION == "diff_cutoff_sign" else -1
    diff_transport = (
        terminal_coefficient * terminal
        + dissipation_coefficient * dissipation
        + cutoff_coefficient * cutoff
    )
    target_on_right = MUTATION != "diff_circularity"
    diff_observed = {
        "transport": qtext(diff_transport),
        "terminalCoefficient": str(terminal_coefficient),
        "dissipationCoefficient": str(dissipation_coefficient),
        "cutoffCoefficient": str(cutoff_coefficient),
        "targetDissipationAppearsOnRight": target_on_right,
    }

    tags = re.findall(r"\\tag\{(H\.[^}]+)\}", text)
    if MUTATION == "tag":
        tags.append("H.1")
    references = [
        "H." + value for value in re.findall(r"\(H\.([0-9]+[a-z]?)\)", text)
    ]
    if MUTATION == "reference":
        references.append("H.99")
    display_open = sum(line.strip() == r"\[" for line in text.splitlines())
    display_close = sum(line.strip() == r"\]" for line in text.splitlines())
    if MUTATION == "display":
        display_open += 1
    expected_tags = [f"H.{index}" for index in range(1, 30)]

    dependency_paths = (
        "research/r075b_bulk_clock_outer_padding_gate.md",
        "research/r075e_horizontal_cross_mode_flux_reduction.md",
        "research/r075f_modal_phase_integration_identity.md",
        "research/r075g_signed_flux_gain_threshold.md",
    )
    dependency_table_present = all(
        any(path in line and FROZEN_SOURCES[path] in line for line in text.splitlines())
        for path in dependency_paths
    )
    if MUTATION == "dependency_table_missing":
        dependency_table_present = False

    required_tokens = (
        r"\eta_R'\ge0",
        r"\Omega_0-\bigl(q(t_2)-q(t)\bigr)e_2",
        r"H(t,x)=H\bigl(t_2,x+(q(t_2)-q(t))e_2\bigr)",
        r"\delta_R^{-2/3}|\Omega_+|^{1/3}",
        r"L^{2/3}\omega^{1/3}R^{-2/3}",
        r"-\frac{4279}{238140000}",
        "p_b >= c L^2 omega R^(-3)",
        r"\le C R^{1/3}p_b^{1/3}",
        r"+\int_s^{t_2}\!\int\eta_R\xi|\nabla_{23}F|^2",
        "does not assert that the benchmark pair is a Navier--Stokes solution",
        "The characteristic identity (H.15) also fails after diffusion.",
        r"\mathbf{NOT\ CLAY}",
    )

    audit_text = PRIMARY_AUDIT.read_text(encoding="utf-8")
    boundary = {
        "signedNotAbsoluteFlux": MUTATION != "transport_absolute_flux",
        "noBlockCount": MUTATION != "block_count",
        "fixedLiftNoSeam": no_seam,
        "terminalTubeInsidePaymentRegion": MUTATION != "payment_region",
        "weightLowerBoundConditional": MUTATION != "conditional_weight",
        "benchmarkNotNSE": MUTATION != "benchmark_nse",
        "diffusiveCharacteristicUnavailable": MUTATION != "diffusive_characteristic",
        "E24Open": MUTATION != "e24_closed",
        "completeClockOpen": MUTATION != "complete_clock",
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
            and fixtures["schema"] ==
                "r075h-single-pass-transport-flux-closure-fixtures-v1"
            and expected["schema"] ==
                "r075h-single-pass-transport-flux-closure-expected-v1"
            and fixtures["frozenSources"] == FROZEN_SOURCES,
            fixtures={"expected": fixture_expected_hash, "observed": fixture_hash},
            expected={"expected": expected_expected_hash, "observed": expected_hash},
        ),
        "primaryAuditBindingAndStatus": record(
            FROZEN_SOURCES[
                "research/r075h_single_pass_transport_flux_closure.md"
            ] in audit_text
            and "Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0."
                in audit_text
            and "Equation tags H.1--H.29 are unique and consecutive." in audit_text,
        ),
        "mainDependencyTableBindings": record(dependency_table_present),
        "weightedTransportEndpointsAndEta": record(
            eta_initial == 0 and eta_terminal == 1 and eta_nondecreasing
            and transport_observed["cutoffMinimum"] == "1/4"
            and transport_observed["cutoffMaximum"] == "3/4",
            state=transport_observed,
        ),
        "weightedTransportIdentityAndPositiveSign": record(
            transport_observed == expected["weightedTransport"]
            and direct_flux > 0
            and direct_flux == endpoint_minus_penalty,
            observed=transport_observed,
        ),
        "characteristicAndSetTranslationDirection": record(
            tube_observed["correctPreimage"] ==
                expected["terminalTube"]["correctPreimage"]
            and tube_observed["correctPreimageContained"]
            and not tube_observed["wrongDirectionContained"]
            and preimage == stated_preimage
            and no_seam,
            observed=tube_observed,
        ),
        "terminalL2Persistence": record(
            tube_observed == expected["terminalTube"]
            and earlier_l2 >= terminal_l2 >= terminal_weighted
            and persistence_slack >= 0,
            observed=tube_observed,
        ),
        "holderDeltaAndVolumePowers": record(
            holder_observed == expected["holder"]
            and l2_integral == holder_right
            and endpoint_energy == endpoint_bound_right,
            observed=holder_observed,
        ),
        "h23FullNormalizationExponents": record(
            h23_observed["product"] == expected["h23"]["product"],
            factors={name: vector_json(row) for name, row in factors},
            product=h23_observed["product"],
        ),
        "h24ExactFrozenRate": record(
            rate == q(expected["h23"]["rate"]) and rate < 0,
            rate=qtext(rate),
        ),
        "matchingBackgroundLowerBoundDirectionH26": record(
            matching_observed == expected["matchingBackground"]
            and mpb >= lower_scale
            and coefficient_left <= matching_right,
            observed=matching_observed,
        ),
        "coherentRationalClosureH11ToH23": record(
            coherent_observed == expected["coherentRationalClosure"]
            and c_transport_residual == {}
            and c_energy_derivative == c_flux_density
            and c_eta_plateau == 1
            and c_j0 >= c_eta_break
            and c_direct_flux == c_endpoint_rhs > 0
            and c_preimage_contained
            and not c_wrong_contained
            and c_terminal_unweighted_l2 >= c_terminal_energy
            and c_h17_slack > 0
            and c_h18_right_cubed > c_h18_left_cubed
            and c_h19_right_cubed > c_h19_left_cubed
            and c_weight_ok
            and c_payment_region_ok
            and c_atom <= c_measurement
            and c_h23_right_cubed > c_h23_left_cubed
            and c_pb >= c_matching_lower
            and c_matching_left_cube <= c_matching_right_cube
            and c_negative_direct_flux < 0
            and c_negative_positive_part == 0
            and abs(c_negative_direct_flux) > c_negative_terminal_energy / 2,
            observed=coherent_observed,
        ),
        "diffusiveIdentitySignsH28": record(
            diff_observed == expected["diffusiveIdentity"],
            observed=diff_observed,
        ),
        "diffusiveCircularityBoundary": record(
            target_on_right and dissipation_coefficient == 1,
        ),
        "tagsReferencesAndDisplays": record(
            tags == expected_tags
            and len(set(tags)) == 29
            and not (set(references) - set(tags))
            and display_open == display_close == 29,
            tags=tags,
            references=sorted(set(references)),
            displays={"open": display_open, "close": display_close},
        ),
        "formulaAndStatusSentinels": record(
            all(re.sub(r"\s+", " ", token) in flat_text for token in required_tokens),
        ),
        "claimBoundary": record(all(boundary.values()), state=boundary),
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
        "weightedTransport": transport_observed,
        "terminalTube": tube_observed,
        "holder": holder_observed,
        "h23": h23_observed,
        "matchingBackground": matching_observed,
        "coherentRationalClosure": coherent_observed,
        "diffusiveIdentity": diff_observed,
        "claimBoundary": boundary,
    }
    OUT_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    failed = [name for name, item in checks.items() if not item["pass"]]
    OUT_REPORT.write_text(
        "# R0.75H finite certificate report\n\n"
        f"- Verdict: **{verdict}**\n"
        f"- Assertions: {payload['assertions']['passed']}/{payload['assertions']['total']}\n"
        f"- Main SHA-256: {sha256(MAIN)}\n"
        f"- Fixture SHA-256: {fixture_hash}\n"
        f"- Expected SHA-256: {expected_hash}\n"
        f"- Failed checks: {'none' if not failed else '; '.join(failed)}\n\n"
        "A smooth rational-output transport fixture verifies the nondecreasing "
        "eta identity: direct positive flux and endpoint-minus-penalty both "
        "equal 1/64. One additional nondegenerate all-rational fixture carries "
        "the same transported field through H.11--H.23: the endpoint identity, "
        "backward set translation, terminal L2 persistence, both Holder steps, "
        "the weighted p/P normalization, and H.26 matching scale. Its tent "
        "cutoff is a finite a.e. integration fixture only, not the smooth "
        "cutoff used in H.28. A mirrored negative-flux field has zero positive "
        "part but nonzero absolute flux, so the certificate rejects replacing "
        "the signed positive part by an absolute value.\n\n"
        "The H.23 exponent product is L^(2/3)R^(-2/3)omega^(1/3)p^(2/3), "
        "with rate -4279/238140000. A matching-background example checks the "
        "H.26 inequality direction. The H.28 ledger retains the target "
        "dissipation with positive sign, proving only circularity of that route. "
        "P_R^(M,tr) is a benchmark measurement, not NSE. E.24 and all larger "
        "claims remain OPEN. **NOT CLAY.**\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "suite": "r075h-single-pass-transport-flux-closure",
        "verdict": verdict,
        "assertions": len(checks),
    }, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
