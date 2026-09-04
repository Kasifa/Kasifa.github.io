#!/usr/bin/env python3
"""Deterministic finite certificate for the frozen R0.76K release.

The certificate binds the analytic note, source report, primary audit, exact
fixtures, and R0.76J dependency.  It independently recomputes finite
coefficient, phase, polynomial, constant, geometry, and backward-heat
ledgers.  It does not prove the continuum limits or a full-clock flux lower
bound.  NOT CLAY.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STEM = "r076k_real_dyadic_edge_sharpness"
FIXTURES = ROOT / f"scripts/{STEM}_fixtures.json"
EXPECTED = ROOT / f"scripts/{STEM}_expected.json"
CERT_SCHEMA = "r076k-real-dyadic-edge-sharpness-certificate-v1"
FIXTURE_SCHEMA = "r076k-real-dyadic-edge-sharpness-fixtures-v1"
EXPECTED_SCHEMA = "r076k-real-dyadic-edge-sharpness-expected-v1"
UPSTREAM_COMMIT = "25d44e986d5283107816f910f89b94bceb1d5726"

# Generated reports are excluded to avoid a self-referential hash cycle.
FROZEN = {
    f"research/{STEM}.md":
        "e293a3aa3e9c1dde443ed7a8c07afd2c709d3855d8b469b38033b04d71116bf2",
    "research/r076k_report-source.md":
        "21dbd71aae07ecbe910d4bcefbf6e1caccc3cddc41171a57ffd239c6eed34f3e",
    f"research/{STEM}_primary_audit.md":
        "36a26cb421a108127b516e47a0008625d67ec43a1d009a14bef9d7684ef03671",
    "research/r076j_local_edge_extrapolation_reconstruction.md":
        "a3d67c8a27ef6ffb7068313732e8e8a08ba98931226df726ac4ee2140ab0f57f",
    "research/r076j_local_edge_extrapolation_reconstruction_primary_audit.md":
        "1b2a608c6ffe16c35489b95fd384f0f47a1d4a79b22491a7825ac53382a746d5",
    f"scripts/{STEM}_fixtures.json":
        "16acf468a6722ee1e66e36a855fdd1e84e56bdc3519e6e2326d6bec0a3b82518",
    f"scripts/{STEM}_expected.json":
        "8f32d96856fdf5d0a86030737f5bf049b227f976661089ed6d31d4a41a1c5b50",
}

GROUPS = {
    "bindings": [
        "all_frozen_bindings",
        "all_hash_specs_well_formed",
        "python_frozen_inventory",
        "fixture_frozen_values",
        "upstream_commit_format",
        "upstream_commit_in_audit",
        "upstream_hashes_in_audit",
    ],
    "inputs": [
        "fixture_schema",
        "expected_schema",
        "fixture_inventory",
        "fixture_top_level_inventory",
        "fixture_frozen_inventory",
        "expected_top_level_inventory",
        "polynomial_sample_inventory",
        "polynomial_epsilons_positive",
        "positive_domains",
        "claims_inventory",
    ],
    "structure": [
        "utf8",
        "no_controls",
        "no_cr",
        "no_tabs",
        "no_trailing_whitespace",
        "tag_sequence",
        "tag_unique",
        "tag_count",
        "display_balance",
        "display_count",
        "reference_closure",
    ],
    "coefficients": [
        "binomial_values",
        "taylor_route_agrees",
        "scaled_values",
        "leading_limits",
        "all_sample_coefficients_nonzero",
        "coefficient_formula_fragment",
        "eventual_nonzero_boundary",
    ],
    "polynomials": [
        "chebyshev_recurrence",
        "t3_value",
        "t3_l2_integral",
        "legendre_kernel_coefficients",
        "legendre_endpoint",
        "legendre_l2_integral",
        "l3_ledger",
        "pointwise_sample_selector",
        "endpoint_gap_left_open",
    ],
    "pointwise_exterior": [
        "pointwise_values",
        "pointwise_prefactor",
        "exterior_interval",
        "exterior_square_root",
        "exterior_exponent",
        "exterior_constant_chain",
        "l3_two_thirds_inequality",
        "main_lower_bound_fragments",
    ],
    "integer_slice": [
        "integer_indices",
        "dyadic_band",
        "branch_count",
        "coefficient_arguments",
        "phase_values",
        "phase_residuals",
        "quarter_turn_w",
        "exact_profile",
        "cosine_contribution_route",
        "heat_exponent_compensation",
        "compensated_amplitudes",
        "heat_compensation_fragment",
        "slice_quantifier_fragment",
    ],
    "asymptotic": [
        "seven_base_sample",
        "six_base_sample",
        "five_base_sample",
        "error_power_used",
        "legendre_leading_sample",
        "general_leading_lower",
        "half_critical_rate",
        "window_values",
        "window_gap",
        "q_window_fragments",
    ],
    "signed_cap": [
        "strict_subcap_geometry",
        "plateau_gap",
        "cap_gap",
        "cap_gap_strictly_larger",
        "gamma_leading_data",
        "pair_identity_numeric",
        "cap_left_point",
        "carrier_sine_positive",
        "fixed_velocity_sign_fragment",
        "single_slice_boundary_fragment",
    ],
    "semigroup": [
        "diffusion_time",
        "exact_transformed_coefficients",
        "integer_dyadic_modes",
        "real_drift_sign",
        "imaginary_shift_sign",
        "direct_decay_exponents",
        "rhs_decay_decomposition",
        "wrong_imaginary_sign_rejected",
        "phase_decomposition",
        "scalar_heat_exponent",
        "carrier_phase",
        "semigroup_formula_fragment",
    ],
    "backward_heat": [
        "index_relation",
        "term_values",
        "sum_value",
        "direct_polynomial_value",
        "wrong_forward_sign_control",
        "overlap_fragment",
        "conditional_slab_fragment",
    ],
    "claims": [
        "fixture_claims",
        "expected_claims",
        "single_slice_proved",
        "complete_flux_open",
        "five_halves_not_claimed",
        "l3_optimality_open",
        "no_figure_or_simulation",
        "no_figure_files",
        "no_novelty_or_priority",
        "not_clay",
        "primary_audit_pass",
        "source_boundary",
        "finite_certificate_boundary",
    ],
    "expected": ["full_expected_match"],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--mutation")
    parser.add_argument("--list-mutations", action="store_true")
    return parser.parse_args()


def sha256(path: Path) -> str | None:
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean_bytes(data: bytes) -> bool:
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return not any((b < 32 and b not in (9, 10, 13)) or b == 127 for b in data)


def compact(value: str) -> str:
    return re.sub(r"\s+", "", value)


def q(value: Any) -> Q:
    return Q(str(value))


def qs(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


ComplexQ = tuple[Q, Q]


def cadd(left: ComplexQ, right: ComplexQ) -> ComplexQ:
    return left[0] + right[0], left[1] + right[1]


def cmul(left: ComplexQ, right: ComplexQ) -> ComplexQ:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def cinv(value: ComplexQ) -> ComplexQ:
    denominator = value[0] ** 2 + value[1] ** 2
    return value[0] / denominator, -value[1] / denominator


def cpow(value: ComplexQ, power: int) -> ComplexQ:
    answer = (Q(1), Q(0))
    for _ in range(power):
        answer = cmul(answer, value)
    return answer


def cscale(value: ComplexQ, scalar: Q) -> ComplexQ:
    return value[0] * scalar, value[1] * scalar


def cjson(value: ComplexQ) -> dict[str, str]:
    return {"re": qs(value[0]), "im": qs(value[1])}


def cos_pi_six(angle_over_pi: Q) -> tuple[Q, Q]:
    """Return constant and sqrt(3) coefficients for cos(pi*angle)."""

    scaled = angle_over_pi * Q(6)
    if scaled.denominator != 1:
        raise ValueError(f"angle is not a multiple of pi/6: {angle_over_pi}")
    table = {
        0: (Q(1), Q(0)),
        1: (Q(0), Q(1, 2)),
        2: (Q(1, 2), Q(0)),
        3: (Q(0), Q(0)),
        4: (Q(-1, 2), Q(0)),
        5: (Q(0), Q(-1, 2)),
        6: (Q(-1), Q(0)),
        7: (Q(0), Q(-1, 2)),
        8: (Q(-1, 2), Q(0)),
        9: (Q(0), Q(0)),
        10: (Q(1, 2), Q(0)),
        11: (Q(0), Q(1, 2)),
    }
    return table[int(scaled) % 12]


def poly_trim(poly: list[Q]) -> list[Q]:
    answer = poly[:]
    while len(answer) > 1 and answer[-1] == 0:
        answer.pop()
    return answer


def poly_add(left: list[Q], right: list[Q]) -> list[Q]:
    length = max(len(left), len(right))
    answer = [Q(0)] * length
    for index in range(length):
        answer[index] = (
            (left[index] if index < len(left) else Q(0))
            + (right[index] if index < len(right) else Q(0))
        )
    return poly_trim(answer)


def poly_scale(poly: list[Q], scalar: Q) -> list[Q]:
    return poly_trim([scalar * coefficient for coefficient in poly])


def poly_x(poly: list[Q]) -> list[Q]:
    return [Q(0)] + poly


def poly_eval(poly: list[Q], value: Q) -> Q:
    answer = Q(0)
    for coefficient in reversed(poly):
        answer = answer * value + coefficient
    return answer


def poly_eval_complex(poly: list[Q], value: ComplexQ) -> ComplexQ:
    answer = (Q(0), Q(0))
    for coefficient in reversed(poly):
        answer = cadd(cmul(answer, value), (coefficient, Q(0)))
    return answer


def poly_derivative(poly: list[Q], order: int = 1) -> list[Q]:
    answer = poly[:]
    for _ in range(order):
        answer = [Q(index) * answer[index] for index in range(1, len(answer))]
        if not answer:
            answer = [Q(0)]
    return answer


def poly_square_integral(poly: list[Q]) -> Q:
    total = Q(0)
    for left_index, left in enumerate(poly):
        for right_index, right in enumerate(poly):
            power = left_index + right_index
            if power % 2 == 0:
                total += left * right * Q(2, power + 1)
    return total


def chebyshev_through(max_degree: int) -> list[list[Q]]:
    values = [[Q(1)]]
    if max_degree == 0:
        return values
    values.append([Q(0), Q(1)])
    for _degree in range(1, max_degree):
        values.append(poly_add(poly_scale(poly_x(values[-1]), Q(2)), poly_scale(values[-2], Q(-1))))
    return values


def legendre_through(max_degree: int) -> list[list[Q]]:
    values = [[Q(1)]]
    if max_degree == 0:
        return values
    values.append([Q(0), Q(1)])
    for degree in range(1, max_degree):
        numerator = poly_add(
            poly_scale(poly_x(values[-1]), Q(2 * degree + 1)),
            poly_scale(values[-2], Q(-degree)),
        )
        values.append(poly_scale(numerator, Q(1, degree + 1)))
    return values


def transformed_coefficients(poly: list[Q], epsilon: Q) -> list[ComplexQ]:
    iepsilon = (Q(0), epsilon)
    inverse = cinv(iepsilon)
    answer: list[ComplexQ] = []
    for j in range(len(poly)):
        value = (Q(0), Q(0))
        for degree in range(j, len(poly)):
            scalar = poly[degree] * Q((-1) ** (degree - j) * math.comb(degree, j))
            value = cadd(value, cscale(cpow(inverse, degree), scalar))
        answer.append(value)
    return answer


def transformed_coefficients_taylor(poly: list[Q], epsilon: Q) -> list[ComplexQ]:
    iepsilon = (Q(0), epsilon)
    point = (Q(0), Q(1, 1) / epsilon)
    answer: list[ComplexQ] = []
    for j in range(len(poly)):
        numerator = poly_eval_complex(poly_derivative(poly, j), point)
        denominator_inverse = cinv(cscale(cpow(iepsilon, j), Q(math.factorial(j))))
        answer.append(cmul(numerator, denominator_inverse))
    return answer


def binding_row(relative: str, expected_hash: str) -> dict[str, Any]:
    observed = sha256(ROOT / relative)
    well_formed = bool(re.fullmatch(r"[0-9a-f]{64}", expected_hash))
    return {
        "expectedSha256": expected_hash,
        "observedSha256": observed if observed is not None else "MISSING",
        "exists": observed is not None,
        "pass": well_formed and observed == expected_hash,
    }


def polynomial_exact(fixture: dict[str, Any]) -> tuple[list[dict[str, Any]], bool]:
    rows: list[dict[str, Any]] = []
    taylor_agrees = True
    for sample in fixture["polynomialSamples"]:
        poly = [q(value) for value in sample["coefficientsAscending"]]
        epsilon = q(sample["epsilon"])
        values = transformed_coefficients(poly, epsilon)
        taylor = transformed_coefficients_taylor(poly, epsilon)
        taylor_agrees = taylor_agrees and values == taylor
        degree = len(poly) - 1
        scaled = [cmul(cpow((Q(0), epsilon), degree), value) for value in values]
        leading = [
            poly[-1] * Q((-1) ** (degree - j) * math.comb(degree, j))
            for j in range(degree + 1)
        ]
        rows.append({
            "name": sample["name"],
            "coefficients": [cjson(value) for value in values],
            "scaledCoefficients": [cjson(value) for value in scaled],
            "leadingLimits": [qs(value) for value in leading],
        })
    return rows, taylor_agrees


def main() -> int:
    args = parse_args()
    names = [f"{group}.{name}" for group, group_names in GROUPS.items() for name in group_names]
    if args.list_mutations:
        print("\n".join(sorted(names)))
        return 0
    mutation = args.mutation or os.environ.get("R076K_MUTATION", "")
    if mutation and mutation not in names:
        print(f"unknown mutation: {mutation}", file=sys.stderr)
        return 2

    fixture_raw = FIXTURES.read_bytes()
    expected_raw = EXPECTED.read_bytes()
    fixture = json.loads(fixture_raw)
    expected = json.loads(expected_raw)
    main_path = ROOT / fixture["files"]["main"]
    source_path = ROOT / fixture["files"]["source"]
    audit_path = ROOT / fixture["files"]["primaryAudit"]
    main_raw, source_raw, audit_raw = (path.read_bytes() for path in (main_path, source_path, audit_path))
    main_text, source_text, audit_text = (data.decode("utf-8") for data in (main_raw, source_raw, audit_raw))
    cm, cs, ca = compact(main_text), compact(source_text), compact(audit_text)

    bindings = {relative: binding_row(relative, digest) for relative, digest in sorted(FROZEN.items())}
    tags = [int(value) for value in re.findall(r"\\tag\{K\.(\d+)\}", main_text)]
    main_without_tags = re.sub(r"\\tag\{K\.\d+\}", "", main_text)
    refs = [int(value) for value in re.findall(r"(?<![A-Za-z0-9_.])K\.(\d+)", main_without_tags)]
    display_opens = len(re.findall(r"(?m)^\\\[$", main_text))
    display_closes = len(re.findall(r"(?m)^\\\]$", main_text))

    poly_rows, taylor_agrees = polynomial_exact(fixture)
    cheb = chebyshev_through(4)
    legendre = legendre_through(3)
    q_kernel = 4
    unnormalized_kernel = [Q(0)]
    for degree, polynomial in enumerate(legendre):
        unnormalized_kernel = poly_add(unnormalized_kernel, poly_scale(polynomial, Q(2 * degree + 1, 2)))
    normalized_kernel = poly_scale(unnormalized_kernel, Q(1, q_kernel))
    unnormalized_endpoint = poly_eval(unnormalized_kernel, Q(1))
    unnormalized_l2 = poly_square_integral(unnormalized_kernel)
    normalized_endpoint = poly_eval(normalized_kernel, Q(1))
    normalized_l2 = poly_square_integral(normalized_kernel)
    l3_cube_upper = unnormalized_endpoint * unnormalized_l2
    l3_ratio_lower = unnormalized_endpoint / Q(4)

    point = fixture["pointwiseSample"]
    point_q = int(point["q"])
    point_d = q(point["d"])
    point_poly_fixture = next(row for row in fixture["polynomialSamples"] if row["name"] == point["polynomialSample"])
    point_poly = [q(value) for value in point_poly_fixture["coefficientsAscending"]]
    point_value = poly_eval(point_poly, Q(1) + point_d)
    point_l2 = poly_square_integral(point_poly)

    exterior = fixture["exteriorSample"]
    exterior_q = int(exterior["q"])
    exterior_d = q(exterior["d"])
    interval_left = Q(1) + Q(7, 8) * exterior_d
    interval_right = Q(1) + exterior_d
    sqrt_radicand = Q(7, 8) * exterior_d
    sqrt_numerator = math.isqrt(sqrt_radicand.numerator)
    sqrt_denominator = math.isqrt(sqrt_radicand.denominator)
    sqrt_value = Q(sqrt_numerator, sqrt_denominator)
    numerator_coefficient = exterior_d / Q(16)
    ratio_coefficient = numerator_coefficient / Q(8)

    slice_sample = fixture["integerSliceSample"]
    slice_q = int(slice_sample["q"])
    n0 = int(slice_sample["n0"])
    eta = q(slice_sample["eta"])
    theta = q(slice_sample["thetaOverPi"])
    transport = q(slice_sample["transportPhaseOverPi"])
    heat_scale = q(slice_sample["heatScale"])
    x_over_pi = q(slice_sample["xOverPi"])
    indices = list(range(n0, n0 + slice_q))
    frequencies = [Q(index) * eta for index in indices]
    slice_poly_fixture = next(row for row in fixture["polynomialSamples"] if row["name"] == slice_sample["polynomialSample"])
    slice_poly = [q(value) for value in slice_poly_fixture["coefficientsAscending"]]
    slice_coefficients = transformed_coefficients(slice_poly, eta)
    arguments = [Q(-1, 2) if value[1] < 0 else Q(1, 2) for value in slice_coefficients]
    phases = [-theta - argument - Q(index) * transport for index, argument in zip(indices, arguments)]
    residuals = [-(phase + Q(index) * transport) for phase, index in zip(phases, indices)]
    prepaid_heat_exponents = [Q(index**2) * heat_scale for index in indices]
    damping_heat_exponents = [-value for value in prepaid_heat_exponents]
    net_heat_exponents = [left + right for left, right in zip(prepaid_heat_exponents, damping_heat_exponents)]
    compensated_amplitudes = [Q(2) * abs(value[1]) for value in slice_coefficients]
    quarter_turn = eta * x_over_pi
    if quarter_turn != Q(1, 2):
        raise ValueError("integer slice fixture is not at the exact quarter turn")
    w_sample = (Q(1) / eta, Q(1) / eta)
    h_sample = poly_eval_complex(slice_poly, w_sample)
    slice_carrier_phase = theta + Q(n0) * eta * x_over_pi
    carrier_cos_constant = Q(1, 2)
    carrier_sin_sqrt_coefficient = Q(-1, 2)
    exact_profile = (
        Q(2) * h_sample[0] * carrier_cos_constant,
        -Q(2) * h_sample[1] * carrier_sin_sqrt_coefficient,
    )
    cosine_contributions: list[tuple[Q, Q]] = []
    for index, argument, coefficient in zip(indices, arguments, slice_coefficients):
        cosine = cos_pi_six(Q(index) * eta * x_over_pi + theta + argument)
        amplitude = Q(2) * abs(coefficient[1])
        cosine_contributions.append((amplitude * cosine[0], amplitude * cosine[1]))

    asymptotic = fixture["asymptoticSample"]
    aq = int(asymptotic["q"])
    aeta = q(asymptotic["eta"])
    rho = q(asymptotic["rho"])
    base7 = int(asymptotic["convergenceBase"])
    base6 = int(asymptotic["approximationBase"])
    base5 = int(asymptotic["remainderBase"])
    error_power = int(asymptotic["errorPower"])

    cap = fixture["signedCapSample"]
    delta0 = q(cap["delta0"])
    r_center = q(cap["rCenter"])
    half_width = q(cap["halfWidth"])
    collar_radius = q(cap["collarRadius"])
    cap_A = q(cap["A"])
    identity_x_q = q(cap["identityTestX"])
    carrier_x = float(identity_x_q)
    cap_left_x = q(cap["capLeftX"])
    cap_m = int(cap["chebyshevDegree"])
    plateau_gap = Q(2) * delta0 / cap_A
    cap_gap = (r_center - half_width + delta0) / cap_A
    gamma_rational = Q(cap_m, math.isqrt(cap_A.numerator))
    gamma_sqrt_argument = Q(2) * (r_center - half_width + delta0)
    gamma_subtrahend = Q(2) * delta0
    t_carrier = poly_eval(cheb[cap_m], identity_x_q)
    t_cap_left = poly_eval(cheb[cap_m], cap_left_x)
    cap_left_pair_sine_coefficient = Q(4) * t_cap_left**2
    carrier_sine_positive = math.sin(2.0 * carrier_x) > 0
    u_plus = 2.0 * float(t_carrier) * math.cos(carrier_x - math.pi / 4.0)
    u_minus = 2.0 * float((-1) ** cap_m * t_carrier) * math.cos(-carrier_x - math.pi / 4.0)
    pair_left = u_plus * u_plus - u_minus * u_minus
    pair_right = 4.0 * math.sin(2.0 * carrier_x) * float(t_carrier * t_carrier)

    semigroup = fixture["semigroupSample"]
    semi_epsilon = q(semigroup["epsilon"])
    semi_tau = q(semigroup["tau"])
    semi_A = q(semigroup["A"])
    semi_e = q(semigroup["e"])
    semi_v = q(semigroup["v"])
    semi_M = q(semigroup["M"])
    semi_x = q(semigroup["x"])
    semi_poly = [q(value) for value in semigroup["polynomialCoefficientsAscending"]]
    diffusion_time = semi_tau / semi_A**2
    real_drift_argument = semi_x - semi_v * semi_tau / semi_e
    imaginary_shift = Q(2) * semi_M * diffusion_time
    semi_coefficients = transformed_coefficients(semi_poly, semi_epsilon)
    semi_offsets = [Q(index) * semi_epsilon for index in range(len(semi_coefficients))]
    semi_modes = [semi_M + offset for offset in semi_offsets]
    semi_mode_ratios = [mode / semi_epsilon for mode in semi_modes]
    semi_integer_modes = [int(value) for value in semi_mode_ratios]
    direct_decay_exponents = [-(mode**2) * diffusion_time for mode in semi_modes]
    internal_heat_exponents = [-(offset**2) * diffusion_time for offset in semi_offsets]
    imaginary_shift_exponents = [-offset * imaginary_shift for offset in semi_offsets]
    scalar_heat_exponent = -(semi_M**2) * diffusion_time
    carrier_phase = semi_M * real_drift_argument
    rhs_decay_exponents = [scalar_heat_exponent + internal + shift for internal, shift in zip(internal_heat_exponents, imaginary_shift_exponents)]
    wrong_imaginary_shift_exponents = [offset * imaginary_shift for offset in semi_offsets]
    wrong_rhs_decay_exponents = [scalar_heat_exponent + internal + shift for internal, shift in zip(internal_heat_exponents, wrong_imaginary_shift_exponents)]
    direct_phases = [mode * real_drift_argument for mode in semi_modes]
    internal_phases = [offset * real_drift_argument for offset in semi_offsets]
    rhs_phases = [carrier_phase + internal for internal in internal_phases]

    backward = fixture["backwardHeatSample"]
    back_n = int(backward["n"])
    back_m = int(backward["m"])
    back_A = q(backward["A"])
    back_T = q(backward["T"])
    back_terms = [
        Q(back_n * math.factorial(back_n + j - 1), math.factorial(back_n - j))
        * (Q(4) * back_T / back_A**2) ** j
        / Q(math.factorial(j))
        for j in range(back_n + 1)
    ]
    back_sum = sum(back_terms, Q(0))
    wrong_forward_sign = sum((Q(-1) ** j) * value for j, value in enumerate(back_terms))
    # Directly apply exp(-tD^2) to T_4 at zero; only even derivatives survive.
    t4 = cheb[back_m]
    direct_back = sum(
        (-back_T / back_A**2) ** j * Q(math.factorial(2 * j)) * t4[2 * j] / Q(math.factorial(j))
        for j in range(back_n + 1)
    )
    direct_forward = sum(
        (back_T / back_A**2) ** j * Q(math.factorial(2 * j)) * t4[2 * j] / Q(math.factorial(j))
        for j in range(back_n + 1)
    )

    exact = {
        "structure": {
            "firstTag": tags[0] if tags else None,
            "lastTag": tags[-1] if tags else None,
            "tagCount": len(tags),
            "displayCount": display_opens,
        },
        "polynomialSamples": poly_rows,
        "orthogonalPolynomials": {
            "chebyshevThrough4": [[qs(value) for value in poly] for poly in cheb],
            "t3AtThreeHalves": qs(poly_eval(cheb[3], Q(3, 2))),
            "t3L2Squared": qs(poly_square_integral(cheb[3])),
            "normalizedLegendreKernelQ4": [qs(value) for value in normalized_kernel],
            "normalizedLegendreEndpoint": qs(normalized_endpoint),
            "normalizedLegendreL2Squared": qs(normalized_l2),
            "unnormalizedLegendreEndpoint": qs(unnormalized_endpoint),
            "unnormalizedLegendreL2Squared": qs(unnormalized_l2),
            "unnormalizedLegendreL3CubeUpper": qs(l3_cube_upper),
            "l3EndpointRatioLower": qs(l3_ratio_lower),
            "l3EndpointSquaredLower": qs(l3_ratio_lower**2),
        },
        "pointwiseSample": {
            "q": point_q,
            "degree": point_q - 1,
            "d": qs(point_d),
            "chebyshevValue": qs(point_value),
            "polynomialL2Squared": qs(point_l2),
            "theoremSquaredPrefactor": "1/8",
        },
        "exteriorSample": {
            "q": exterior_q,
            "degree": exterior_q - 1,
            "d": qs(exterior_d),
            "intervalLeft": qs(interval_left),
            "intervalRight": qs(interval_right),
            "intervalLength": qs(interval_right - interval_left),
            "sqrtSevenDOverEight": qs(sqrt_value),
            "exponent": qs(Q(2 * (exterior_q - 1)) * sqrt_value),
            "numeratorCoefficient": qs(numerator_coefficient),
            "l2DenominatorUpper": "8",
            "l3CubeUpper": "16",
            "l3TwoThirdsStrictUpper": "8",
            "ratioCoefficient": qs(ratio_coefficient),
        },
        "integerSliceSample": {
            "indices": indices,
            "scaledFrequencies": [qs(value) for value in frequencies],
            "M": qs(Q(n0) * eta),
            "complexBranchCount": 2 * slice_q,
            "coefficientArgumentsOverPi": [qs(value) for value in arguments],
            "phasesOverPi": [qs(value) for value in phases],
            "phaseResidualsOverPi": [qs(value) for value in residuals],
            "prepaidHeatExponents": [qs(value) for value in prepaid_heat_exponents],
            "dampingHeatExponents": [qs(value) for value in damping_heat_exponents],
            "netHeatExponents": [qs(value) for value in net_heat_exponents],
            "compensatedAmplitudes": [qs(value) for value in compensated_amplitudes],
            "wAtSample": cjson(w_sample),
            "carrierPhaseOverPi": qs(slice_carrier_phase),
            "exactProfile": {"constant": qs(exact_profile[0]), "sqrt3Coefficient": qs(exact_profile[1])},
            "cosineContributions": [
                {"constant": qs(value[0]), "sqrt3Coefficient": qs(value[1])}
                for value in cosine_contributions
            ],
        },
        "asymptoticSample": {
            "etaQSquaredSevenToQ": qs(aeta * aq**error_power * base7**aq),
            "etaQSquaredSixToQ": qs(aeta * aq**error_power * base6**aq),
            "etaQFiveToQ": qs(aeta * aq * base5**aq),
            "normalizedLegendreLeadingQ4": qs(normalized_kernel[-1]),
            "generalLeadingLower": "3/4",
            "halfCriticalNetExponentCoefficient": qs(-rho / Q(8)),
            "provedWindowExponent": asymptotic["provedWindowExponent"],
            "upperWindowExponent": asymptotic["upperWindowExponent"],
            "windowGap": qs(q(asymptotic["upperWindowExponent"]) - q(asymptotic["provedWindowExponent"])),
        },
        "signedCapSample": {
            "plateauGap": qs(plateau_gap),
            "capGap": qs(cap_gap),
            "capGapLarger": cap_gap > plateau_gap,
            "strictSubcapGeometry": delta0 < r_center - Q(3) * half_width < r_center + Q(3) * half_width < collar_radius,
            "gammaLeadingRationalFactor": qs(gamma_rational),
            "gammaLeadingSqrtArgument": qs(gamma_sqrt_argument),
            "gammaLeadingConstantSubtrahend": qs(gamma_subtrahend),
            "pairIdentityCoefficient": "4",
            "t3AtCarrier": qs(t_carrier),
            "capLeftX": qs(cap_left_x),
            "t3AtCapLeft": qs(t_cap_left),
            "capLeftPairSineCoefficient": qs(cap_left_pair_sine_coefficient),
            "carrierSinePositive": carrier_sine_positive,
        },
        "semigroupSample": {
            "epsilon": qs(semi_epsilon),
            "diffusionTime": qs(diffusion_time),
            "realDriftArgument": qs(real_drift_argument),
            "imaginaryShift": qs(imaginary_shift),
            "transformedCoefficients": [qs(value[0]) for value in semi_coefficients],
            "integerModes": semi_integer_modes,
            "modeFrequencies": [qs(value) for value in semi_modes],
            "directDecayExponents": [qs(value) for value in direct_decay_exponents],
            "internalHeatExponents": [qs(value) for value in internal_heat_exponents],
            "imaginaryShiftExponents": [qs(value) for value in imaginary_shift_exponents],
            "rhsCombinedDecayExponents": [qs(value) for value in rhs_decay_exponents],
            "directPhases": [qs(value) for value in direct_phases],
            "internalPhases": [qs(value) for value in internal_phases],
            "rhsCombinedPhases": [qs(value) for value in rhs_phases],
            "scalarHeatExponent": qs(scalar_heat_exponent),
            "carrierPhase": qs(carrier_phase),
        },
        "backwardHeatSample": {
            "terms": [qs(value) for value in back_terms],
            "exactValue": qs(back_sum),
            "wrongForwardSignValue": qs(wrong_forward_sign),
        },
        "claims": fixture["claims"],
    }

    file_values = fixture["frozen"]
    frozen_value_map = {
        fixture["files"]["main"]: file_values["mainSha256"],
        fixture["files"]["source"]: file_values["sourceSha256"],
        fixture["files"]["primaryAudit"]: file_values["primaryAuditSha256"],
        fixture["files"]["r076jMain"]: file_values["r076jMainSha256"],
        fixture["files"]["r076jPrimaryAudit"]: file_values["r076jPrimaryAuditSha256"],
    }
    input_bytes = [main_raw, source_raw, audit_raw, fixture_raw, expected_raw]
    checks: dict[str, dict[str, bool]] = {group: {} for group in GROUPS}
    required_frozen_paths = {
        f"research/{STEM}.md",
        "research/r076k_report-source.md",
        f"research/{STEM}_primary_audit.md",
        "research/r076j_local_edge_extrapolation_reconstruction.md",
        "research/r076j_local_edge_extrapolation_reconstruction_primary_audit.md",
        f"scripts/{STEM}_fixtures.json",
        f"scripts/{STEM}_expected.json",
    }
    checks["bindings"] = {
        "all_frozen_bindings": all(row["pass"] for row in bindings.values()),
        "all_hash_specs_well_formed": all(re.fullmatch(r"[0-9a-f]{64}", value) is not None for value in FROZEN.values()),
        "python_frozen_inventory": set(FROZEN) == required_frozen_paths and not any("AGENTS.md" in path or "certificate.json" in path or "qa_report" in path for path in FROZEN),
        "fixture_frozen_values": all(FROZEN.get(path) == digest for path, digest in frozen_value_map.items()),
        "upstream_commit_format": bool(re.fullmatch(r"[0-9a-f]{40}", UPSTREAM_COMMIT)) and file_values["r076jCoreCommit"] == UPSTREAM_COMMIT,
        "upstream_commit_in_audit": UPSTREAM_COMMIT in audit_text,
        "upstream_hashes_in_audit": file_values["r076jMainSha256"] in audit_text and file_values["r076jPrimaryAuditSha256"] in audit_text,
    }
    checks["inputs"] = {
        "fixture_schema": fixture.get("schema") == FIXTURE_SCHEMA,
        "expected_schema": expected.get("schema") == EXPECTED_SCHEMA,
        "fixture_inventory": set(fixture.get("files", {})) == {"main", "source", "primaryAudit", "r076jMain", "r076jPrimaryAudit"},
        "fixture_top_level_inventory": set(fixture) == {"schema", "files", "frozen", "polynomialSamples", "pointwiseSample", "exteriorSample", "integerSliceSample", "asymptoticSample", "signedCapSample", "semigroupSample", "backwardHeatSample", "claims"},
        "fixture_frozen_inventory": set(fixture.get("frozen", {})) == {"mainSha256", "sourceSha256", "primaryAuditSha256", "r076jMainSha256", "r076jPrimaryAuditSha256", "r076jCoreCommit"},
        "expected_top_level_inventory": set(expected) == {"schema", "structure", "polynomialSamples", "orthogonalPolynomials", "pointwiseSample", "exteriorSample", "integerSliceSample", "asymptoticSample", "signedCapSample", "semigroupSample", "backwardHeatSample", "claims"},
        "polynomial_sample_inventory": [row["name"] for row in fixture.get("polynomialSamples", [])] == ["genericCubic", "chebyshevT3", "normalizedLegendreKernelQ4"],
        "polynomial_epsilons_positive": all(q(row["epsilon"]) > 0 for row in fixture.get("polynomialSamples", [])),
        "positive_domains": point_q >= 2 and Q(0) < point_d <= Q(1) and exterior_q >= 2 and Q(0) < exterior_d <= Q(1) and eta > 0,
        "claims_inventory": set(fixture.get("claims", {})) == set(expected.get("claims", {})),
    }
    checks["structure"] = {
        "utf8": all(clean_bytes(data) for data in input_bytes),
        "no_controls": all(clean_bytes(data) for data in input_bytes),
        "no_cr": all(b"\r" not in data for data in input_bytes),
        "no_tabs": all(b"\t" not in data for data in input_bytes),
        "no_trailing_whitespace": all(not re.search(rb"[ \t]+$", data, re.MULTILINE) for data in input_bytes),
        "tag_sequence": tags == list(range(1, 49)),
        "tag_unique": len(tags) == len(set(tags)),
        "tag_count": len(tags) == expected["structure"]["tagCount"],
        "display_balance": display_opens == display_closes,
        "display_count": display_opens == expected["structure"]["displayCount"],
        "reference_closure": bool(refs) and set(refs).issubset(set(tags)),
    }
    expected_poly = expected["polynomialSamples"]
    checks["coefficients"] = {
        "binomial_values": [row["coefficients"] for row in poly_rows] == [row["coefficients"] for row in expected_poly],
        "taylor_route_agrees": taylor_agrees,
        "scaled_values": [row["scaledCoefficients"] for row in poly_rows] == [row["scaledCoefficients"] for row in expected_poly],
        "leading_limits": [row["leadingLimits"] for row in poly_rows] == [row["leadingLimits"] for row in expected_poly],
        "all_sample_coefficients_nonzero": all(any(q(value[key]) != 0 for key in ("re", "im")) for row in poly_rows for value in row["coefficients"]),
        "coefficient_formula_fragment": "b_j(\\epsilon)=\\sum_{r=j}^na_r(i\\epsilon)^{-r}" in cm and "p^{(j)}(i/\\epsilon)" in cm,
        "eventual_nonzero_boundary": "sufficientlysmall" in cm and "doesnotassertnonvanishingforeverypositive" in ca,
    }
    orth = exact["orthogonalPolynomials"]
    checks["polynomials"] = {
        "chebyshev_recurrence": orth["chebyshevThrough4"] == expected["orthogonalPolynomials"]["chebyshevThrough4"],
        "t3_value": point_value == Q(9),
        "t3_l2_integral": point_l2 == Q(34, 35),
        "legendre_kernel_coefficients": orth["normalizedLegendreKernelQ4"] == expected["orthogonalPolynomials"]["normalizedLegendreKernelQ4"],
        "legendre_endpoint": normalized_endpoint == Q(2) and unnormalized_endpoint == Q(8),
        "legendre_l2_integral": normalized_l2 == Q(1, 2) and unnormalized_l2 == Q(8),
        "l3_ledger": l3_cube_upper == Q(64) and l3_ratio_lower == Q(2),
        "pointwise_sample_selector": point["polynomialSample"] == "chebyshevT3" and point_poly == cheb[point_q - 1],
        "endpoint_gap_left_open": "between`q^(4/3)`and`q^2`remainsopen" in cm,
    }
    checks["pointwise_exterior"] = {
        "pointwise_values": point_value == Q(9) and point_l2 == Q(34, 35),
        "pointwise_prefactor": exact["pointwiseSample"]["theoremSquaredPrefactor"] == "1/8",
        "exterior_interval": interval_left == Q(10, 9) and interval_right == Q(71, 63) and interval_right - interval_left == Q(1, 63),
        "exterior_square_root": sqrt_value == Q(1, 3) and sqrt_value**2 == sqrt_radicand,
        "exterior_exponent": Q(2 * (exterior_q - 1)) * sqrt_value == Q(2),
        "exterior_constant_chain": numerator_coefficient == Q(1, 126) and ratio_coefficient == Q(1, 1008),
        "l3_two_thirds_inequality": 16**2 < 8**3,
        "main_lower_bound_fragments": "\\frac1{2\\sqrt2}" in cm and "\\fracd{128}" in cm and "\\sqrt{\\frac{7d}{8}}" in cm,
    }
    checks["integer_slice"] = {
        "integer_indices": indices == [3, 4, 5, 6],
        "dyadic_band": indices[-1] <= 2 * indices[0] and frequencies == [Q(3, 8), Q(1, 2), Q(5, 8), Q(3, 4)],
        "branch_count": 2 * slice_q == 8,
        "coefficient_arguments": [qs(value) for value in arguments] == expected["integerSliceSample"]["coefficientArgumentsOverPi"],
        "phase_values": [qs(value) for value in phases] == expected["integerSliceSample"]["phasesOverPi"],
        "phase_residuals": all(left == theta + argument for left, argument in zip(residuals, arguments)),
        "quarter_turn_w": quarter_turn == Q(1, 2) and w_sample == (Q(1) / eta, Q(1) / eta) == (Q(8), Q(8)),
        "exact_profile": slice_carrier_phase == Q(5, 3) and h_sample == (Q(-4120), Q(4072)) and exact_profile == (Q(-4120), Q(4072)),
        "cosine_contribution_route": cosine_contributions == [
            (Q(0), Q(-2072)),
            (Q(-6168), Q(0)),
            (Q(0), Q(6144)),
            (Q(2048), Q(0)),
        ] and (
            sum((value[0] for value in cosine_contributions), Q(0)),
            sum((value[1] for value in cosine_contributions), Q(0)),
        ) == h_sample,
        "heat_exponent_compensation": prepaid_heat_exponents == [Q(9, 7), Q(16, 7), Q(25, 7), Q(36, 7)] and damping_heat_exponents == [-Q(9, 7), -Q(16, 7), -Q(25, 7), -Q(36, 7)] and net_heat_exponents == [Q(0)] * 4,
        "compensated_amplitudes": all(value[0] == 0 and value[1] != 0 for value in slice_coefficients) and compensated_amplitudes == [Q(4144), Q(12336), Q(12288), Q(4096)],
        "heat_compensation_fragment": "A_j=2|b_j(\\eta_L)|e^{n_j^2R^2s_*}" in cm,
        "slice_quantifier_fragment": "foreveryprescribed`s_*`and`B`thereexistssuchapacket" in cm,
    }
    checks["asymptotic"] = {
        "seven_base_sample": aeta * aq**error_power * base7**aq == Q(1, 16),
        "six_base_sample": aeta * aq**error_power * base6**aq == Q(81, 2401),
        "five_base_sample": aeta * aq * base5**aq == Q(625, 153664),
        "error_power_used": error_power == 2,
        "legendre_leading_sample": normalized_kernel[-1] == Q(35, 16),
        "general_leading_lower": Q(35, 16) >= Q(3, 4),
        "half_critical_rate": -rho / Q(8) == Q(-9, 80000),
        "window_values": q(asymptotic["provedWindowExponent"]) == Q(2) and q(asymptotic["upperWindowExponent"]) == Q(5, 2),
        "window_gap": q(asymptotic["upperWindowExponent"]) - q(asymptotic["provedWindowExponent"]) == Q(1, 2),
        "q_window_fragments": "q(L)=o(L^2)" in main_text and "q=o(L^(5/2))" in main_text and "limitationofthepresentuniformapproximationproof" in cm,
    }
    checks["signed_cap"] = {
        "strict_subcap_geometry": delta0 < r_center - Q(3) * half_width < r_center + Q(3) * half_width < collar_radius,
        "plateau_gap": plateau_gap == Q(1, 50),
        "cap_gap": cap_gap == Q(1, 20),
        "cap_gap_strictly_larger": cap_gap > plateau_gap,
        "gamma_leading_data": gamma_rational == Q(3, 10) and gamma_sqrt_argument == Q(10) and gamma_subtrahend == Q(2),
        "pair_identity_numeric": abs(pair_left - pair_right) < 1e-12,
        "cap_left_point": cap_left_x == Q(21, 20) and t_cap_left == Q(2961, 2000) and cap_left_pair_sine_coefficient == Q(8767521, 1000000),
        "carrier_sine_positive": carrier_sine_positive and t_carrier == Q(1),
        "fixed_velocity_sign_fragment": "Chooseafixed`v<0`" in cm,
        "single_slice_boundary_fragment": "Thisclosesthesignedsingle-slicealgebraonly." in cm,
    }
    checks["semigroup"] = {
        "diffusion_time": diffusion_time == Q(1, 4),
        "exact_transformed_coefficients": semi_coefficients == [(Q(-16), Q(0)), (Q(32), Q(0)), (Q(-16), Q(0))],
        "integer_dyadic_modes": all(value.denominator == 1 for value in semi_mode_ratios) and semi_integer_modes == [4, 5, 6] and semi_integer_modes[-1] <= 2 * semi_integer_modes[0],
        "real_drift_sign": real_drift_argument == Q(2),
        "imaginary_shift_sign": imaginary_shift == Q(1, 2),
        "direct_decay_exponents": direct_decay_exponents == [Q(-1, 4), Q(-25, 64), Q(-9, 16)],
        "rhs_decay_decomposition": rhs_decay_exponents == direct_decay_exponents and internal_heat_exponents == [Q(0), Q(-1, 64), Q(-1, 16)] and imaginary_shift_exponents == [Q(0), Q(-1, 8), Q(-1, 4)],
        "wrong_imaginary_sign_rejected": wrong_rhs_decay_exponents != direct_decay_exponents,
        "phase_decomposition": direct_phases == [Q(2), Q(5, 2), Q(3)] and internal_phases == [Q(0), Q(1, 2), Q(1)] and rhs_phases == direct_phases,
        "scalar_heat_exponent": scalar_heat_exponent == Q(-1, 4),
        "carrier_phase": carrier_phase == Q(2),
        "semigroup_formula_fragment": "x-\\frac{v\\tau}{e_a}+\\frac{2iM_L\\tau}{A^2}" in cm and "-M_L^2\\tau/A^2" in cm,
    }
    checks["backward_heat"] = {
        "index_relation": back_m == 2 * back_n,
        "term_values": back_terms == [Q(1), Q(4, 25), Q(6, 625)],
        "sum_value": back_sum == Q(731, 625),
        "direct_polynomial_value": direct_back == back_sum,
        "wrong_forward_sign_control": direct_forward == wrong_forward_sign == Q(531, 625) and wrong_forward_sign != back_sum and "e^{-(T/A^2)D^2}" in cm,
        "overlap_fragment": "A^(3/2)<<m=o(A^2)" in main_text and "A^(3/2)<<m=o(A^2)" in source_text,
        "conditional_slab_fragment": "Evengrantingaterminalslab" in cm,
    }
    claims = fixture["claims"]
    checks["claims"] = {
        "fixture_claims": claims == expected["claims"],
        "expected_claims": exact["claims"] == expected["claims"],
        "single_slice_proved": claims["realDyadicSharpness"] and claims["exactIntegerSingleSlice"] and claims["signedTwoCapSingleSlice"],
        "complete_flux_open": not claims["completeFluxLowerBound"] and "completesignedflux" in cm.lower(),
        "five_halves_not_claimed": not claims["fullQOLFiveHalvesRange"] and "doesnotcoverthefullR0.76Jupperwindow`q=o(L^(5/2))`" in cm,
        "l3_optimality_open": not claims["l3EndpointOptimality"] and "remainsopen" in cm,
        "no_figure_or_simulation": not claims["formalFigureRequired"] and not claims["simulationRequired"] and "Nosimulationorformalscientificfigureisneeded" in cm,
        "no_figure_files": not any(path.name.startswith("r076k_") and path.suffix.lower() in {".png", ".pdf", ".svg", ".jpg", ".jpeg"} for path in ROOT.rglob("*")),
        "no_novelty_or_priority": not claims["noveltyClaimed"] and "Nonoveltyorpriorityclaimismade" in cm and "not evidence of novelty or priority" in source_text,
        "not_clay": not claims["clayClaimed"] and "NOTCLAY" in cm and "NOTCLAY" in cs and "NOTCLAY" in ca,
        "primary_audit_pass": "PASS--single-slicetheoremonly" in ca and "complete-clockfluxremainsopen" in ca,
        "source_boundary": "fixed-sliceclasssharpnessfromcomplete-clocksigned-fluxsharpness" in cs and "Furtherbroadsearchingwasunlikely" in cs,
        "finite_certificate_boundary": "cannotproveuniformconvergence" in ca and "cannotprove" in cm,
    }
    expected_without_schema = {key: value for key, value in expected.items() if key != "schema"}
    checks["expected"] = {"full_expected_match": exact == expected_without_schema}

    if mutation:
        mutation_group, mutation_name = mutation.split(".", 1)
        checks[mutation_group][mutation_name] = False
    # Fail closed if a programming error omitted or added a named assertion.
    group_shape_ok = all(list(checks[group]) == GROUPS[group] for group in GROUPS)
    all_pass = group_shape_ok and all(value for group in checks.values() for value in group.values())
    failures = [
        f"{group}.{name}"
        for group, values in checks.items()
        for name, value in values.items()
        if not value
    ]
    assertion_count = sum(len(group) for group in checks.values())
    assertion_passed = assertion_count - len(failures)
    result = {
        "schema": CERT_SCHEMA,
        "status": "PASS" if all_pass else "FAIL",
        "verdict": "PASS" if all_pass else "FAIL",
        "freezeReady": all_pass,
        "checkMode": bool(args.check),
        "mutation": mutation or None,
        "upstreamCoreCommit": UPSTREAM_COMMIT,
        "bindings": bindings,
        "assertions": checks,
        "assertionCount": assertion_count,
        "assertionsPassed": assertion_passed,
        "assertionsTotal": assertion_count,
        "groups": {
            group: {
                "passed": sum(values.values()),
                "total": len(values),
            }
            for group, values in checks.items()
        },
        "failures": failures,
        "negativeMutations": sorted(names),
        "groupShapePass": group_shape_ok,
        "exact": exact,
        "boundary": "Finite exact audit only; continuum convergence, semigroup analysis, and full-clock flux remain analytic or open. NOT CLAY.",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    if not all_pass:
        print("failed assertions: " + ", ".join(failures), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
