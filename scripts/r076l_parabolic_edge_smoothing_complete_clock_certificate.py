#!/usr/bin/env python3
"""Deterministic finite certificate for the frozen R0.76L release.

This program recomputes finite rational, cubic-field, polynomial, shear,
geometry, normalization, and figure ledgers.  It binds the analytic inputs
but does not prove any asymptotic limit, semigroup estimate, signed-clock
theorem, or Navier--Stokes regularity statement.  NOT CLAY.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import re
import struct
import subprocess
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STEM = "r076l_parabolic_edge_smoothing_complete_clock"
FIXTURES = ROOT / f"scripts/{STEM}_fixtures.json"
EXPECTED = ROOT / f"scripts/{STEM}_expected.json"
CERT_SCHEMA = "r076l-parabolic-edge-smoothing-complete-clock-certificate-v1"
FIXTURE_SCHEMA = "r076l-parabolic-edge-smoothing-complete-clock-fixtures-v1"
EXPECTED_SCHEMA = "r076l-parabolic-edge-smoothing-complete-clock-expected-v1"
UPSTREAM_COMMIT = "8a89aee4fe0839de44e21a90ba827a9cc77b3062"
FIXTURE_SHA256 = "cf442a934bd713ef046f1aa5b6f41ea5a1cfe118e6cef91a30d20a26d16bd1a9"
EXPECTED_SHA256 = "48dc286d198512034aaee9ce65ef696fe367942c9ea9a6e840ac0e7c31c2f8ed"

MUTATIONS = [
    "forward_heat_sign",
    "backward_heat_sign",
    "saddle_z_cube",
    "saddle_F_cube",
    "terminal_G_sign",
    "gaussian_tilt_penalty",
    "positive_series_weight",
    "moment_identity",
    "terminal_layer_power",
    "operator_first_order_sign",
    "integer_mode_upper_endpoint",
    "drift_sign",
    "paired_cap_swap",
    "plateau_jacobian",
    "physical_R_power",
    "normalization_omega_third",
    "high_degree_open_to_theorem",
    "arbitrary_packet_upgrade",
    "version_m_upgrade",
    "diagnostic_to_proof",
    "figure_row_count",
    "figure_limit_constant",
    "progress_missing_complete",
    "generated_output_bound",
    "agents_file_bound",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--development", action="store_true")
    parser.add_argument("--mutation")
    parser.add_argument("--list-mutations", action="store_true")
    return parser.parse_args()


def sha256(path: Path) -> str | None:
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qs(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def q(value: Any) -> Q:
    return Q(str(value))


def rational_root(value: Q, degree: int) -> Q:
    """Return an exact positive rational root, rejecting unsupported samples."""
    def integer_root(number: int) -> int:
        lo, hi = 0, number + 1
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if mid**degree <= number:
                lo = mid
            else:
                hi = mid
        if lo**degree != number:
            raise ValueError("sample root is not rational")
        return lo

    if value < 0 or degree < 1:
        raise ValueError("positive rational sample required")
    return Q(integer_root(value.numerator), integer_root(value.denominator))


def poly_trim(poly: list[Q]) -> list[Q]:
    answer = poly[:]
    while len(answer) > 1 and answer[-1] == 0:
        answer.pop()
    return answer


def poly_add(left: list[Q], right: list[Q]) -> list[Q]:
    answer = [Q(0)] * max(len(left), len(right))
    for index in range(len(answer)):
        answer[index] = (
            (left[index] if index < len(left) else Q(0))
            + (right[index] if index < len(right) else Q(0))
        )
    return poly_trim(answer)


def poly_scale(poly: list[Q], scalar: Q) -> list[Q]:
    return poly_trim([scalar * value for value in poly])


def poly_mul(left: list[Q], right: list[Q]) -> list[Q]:
    answer = [Q(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            answer[i + j] += a * b
    return poly_trim(answer)


def poly_derivative(poly: list[Q], order: int = 1) -> list[Q]:
    answer = poly[:]
    for _ in range(order):
        answer = [Q(index) * answer[index] for index in range(1, len(answer))]
        if not answer:
            answer = [Q(0)]
    return answer


def poly_eval(poly: list[Q], value: Q) -> Q:
    answer = Q(0)
    for coefficient in reversed(poly):
        answer = answer * value + coefficient
    return answer


def chebyshev(degree: int) -> list[Q]:
    values = [[Q(1)], [Q(0), Q(1)]]
    if degree == 0:
        return values[0]
    for _ in range(1, degree):
        values.append(
            poly_add(poly_scale([Q(0)] + values[-1], Q(2)), poly_scale(values[-2], Q(-1)))
        )
    return values[degree]


def heat_polynomial(poly: list[Q], time_over_a_squared: Q, sign: int) -> list[Q]:
    answer = [Q(0)]
    for j in range((len(poly) - 1) // 2 + 1):
        derivative = poly_derivative(poly, 2 * j)
        scalar = Q(sign) ** j * time_over_a_squared**j / Q(math.factorial(j))
        answer = poly_add(answer, poly_scale(derivative, scalar))
    return answer


ComplexQ = tuple[Q, Q]


def cadd(left: ComplexQ, right: ComplexQ) -> ComplexQ:
    return left[0] + right[0], left[1] + right[1]


def cmul(left: ComplexQ, right: ComplexQ) -> ComplexQ:
    return left[0] * right[0] - left[1] * right[1], left[0] * right[1] + left[1] * right[0]


def cscale(value: ComplexQ, scalar: Q) -> ComplexQ:
    return value[0] * scalar, value[1] * scalar


def cinv(value: ComplexQ) -> ComplexQ:
    denominator = value[0] ** 2 + value[1] ** 2
    return value[0] / denominator, -value[1] / denominator


def cpow(value: ComplexQ, power: int) -> ComplexQ:
    answer = (Q(1), Q(0))
    for _ in range(power):
        answer = cmul(answer, value)
    return answer


def cpoly_add(left: list[ComplexQ], right: list[ComplexQ]) -> list[ComplexQ]:
    answer = [(Q(0), Q(0))] * max(len(left), len(right))
    for index in range(len(answer)):
        answer[index] = cadd(
            left[index] if index < len(left) else (Q(0), Q(0)),
            right[index] if index < len(right) else (Q(0), Q(0)),
        )
    return answer


def cpoly_mul(left: list[ComplexQ], right: list[ComplexQ]) -> list[ComplexQ]:
    answer = [(Q(0), Q(0)) for _ in range(len(left) + len(right) - 1)]
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            answer[i + j] = cadd(answer[i + j], cmul(a, b))
    return answer


def cpoly_scale(poly: list[ComplexQ], scalar: ComplexQ) -> list[ComplexQ]:
    return [cmul(value, scalar) for value in poly]


def cpoly_compose_real(poly: list[Q], linear: list[ComplexQ]) -> list[ComplexQ]:
    answer = [(Q(0), Q(0))]
    power = [(Q(1), Q(0))]
    for coefficient in poly:
        answer = cpoly_add(answer, cpoly_scale(power, (coefficient, Q(0))))
        power = cpoly_mul(power, linear)
    return answer[: len(poly)]


def cpoly_eval_real(poly: list[Q], value: ComplexQ) -> ComplexQ:
    answer = (Q(0), Q(0))
    for coefficient in reversed(poly):
        answer = cadd(cmul(answer, value), (coefficient, Q(0)))
    return answer


def transformed_derivative_coefficients(poly: list[Q], eta: Q) -> list[ComplexQ]:
    point = (Q(0), Q(1) / eta)
    ieta = (Q(0), eta)
    answer = []
    for j in range(len(poly)):
        numerator = cpoly_eval_real(poly_derivative(poly, j), point)
        denominator = cscale(cpow(ieta, j), Q(math.factorial(j)))
        answer.append(cmul(numerator, cinv(denominator)))
    return answer


Cubic = tuple[Q, Q, Q]


def kmul(left: Cubic, right: Cubic) -> Cubic:
    raw = [Q(0)] * 5
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            raw[i + j] += a * b
    raw[1] += Q(2) * raw[4]
    raw[0] += Q(2) * raw[3]
    return raw[0], raw[1], raw[2]


def kpow(value: Cubic, power: int) -> Cubic:
    answer: Cubic = (Q(1), Q(0), Q(0))
    for _ in range(power):
        answer = kmul(answer, value)
    return answer


def kscale(value: Cubic, scalar: Q) -> Cubic:
    return value[0] * scalar, value[1] * scalar, value[2] * scalar


def ksub(left: Cubic, right: Cubic) -> Cubic:
    return tuple(left[i] - right[i] for i in range(3))  # type: ignore[return-value]


def kjson(value: Cubic) -> list[str]:
    return [qs(part) for part in value]


def png_metadata(path: Path) -> tuple[int, int, int | None]:
    raw = path.read_bytes()
    if raw[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("invalid PNG signature")
    width, height = struct.unpack(">II", raw[16:24])
    offset = 8
    dpi = None
    while offset + 12 <= len(raw):
        length = struct.unpack(">I", raw[offset : offset + 4])[0]
        kind = raw[offset + 4 : offset + 8]
        data = raw[offset + 8 : offset + 8 + length]
        if kind == b"pHYs" and len(data) == 9 and data[8] == 1:
            x_ppm = struct.unpack(">I", data[:4])[0]
            dpi = round(x_ppm * 0.0254)
        offset += 12 + length
        if kind == b"IEND":
            break
    return width, height, dpi


def git_file_bytes(commit: str, relative: str) -> bytes | None:
    try:
        return subprocess.check_output(
            ["git", "show", f"{commit}:{relative}"], cwd=ROOT, stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        return None


def binding(relative: str, expected_hash: str) -> dict[str, Any]:
    observed = sha256(ROOT / relative)
    return {
        "expectedSha256": expected_hash,
        "observedSha256": observed or "MISSING",
        "exists": observed is not None,
        "pass": bool(re.fullmatch(r"[0-9a-f]{64}", expected_hash)) and observed == expected_hash,
    }


def build_exact(fixture: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    main_text = (ROOT / fixture["files"]["main"]).read_text(encoding="utf-8")
    tags = [int(value) for value in re.findall(r"\\tag\{L\.(\d+)\}", main_text)]
    without_tags = re.sub(r"\\tag\{L\.\d+\}", "", main_text)
    refs = [int(value) for value in re.findall(r"(?<![A-Za-z0-9_.])L\.(\d+)", without_tags)]
    displays = len(re.findall(r"(?m)^\\\[$", main_text))

    scale = fixture["scaleSample"]
    A, m = Q(scale["A"]), Q(scale["m"])
    sqrt_a = rational_root(A, 2)
    mu = rational_root(m**2 / A, 3)
    gamma = m / sqrt_a
    power_rows = []
    for alpha_raw in scale["alphaValues"]:
        alpha = q(alpha_raw)
        power_rows.append(
            {
                "alpha": qs(alpha),
                "gammaExponent": qs(alpha - Q(1, 2)),
                "muExponent": qs((Q(2) * alpha - Q(1)) / Q(3)),
                "muSquaredExponent": qs((Q(4) * alpha - Q(2)) / Q(3)),
                "backwardExponent": qs(Q(2) * alpha - Q(2)),
            }
        )

    saddle = fixture["saddleSample"]
    saddle_time = q(saddle["heatTime"])
    alpha: Cubic = (Q(0), Q(1), Q(0))
    z4 = kscale(kpow(alpha, 2), rational_root(saddle_time**2 / Q(2), 3))
    root_two_z4 = kscale(alpha, rational_root(Q(2) * kpow(z4, 3)[0], 6))
    F4 = ksub(root_two_z4, kscale(kpow(z4, 2), Q(1) / (Q(4) * saddle_time)))
    G4 = kscale(z4, Q(1) / (Q(2) * saddle_time))
    f3_cube = Q(27) * (saddle_time - Q(1)) / Q(16)
    gap = q(saddle["capPlateauGap"])

    tilt = fixture["tiltSample"]
    s_tilt, y_tilt, c1, c2 = map(q, (tilt["heatTime"], tilt["y"], tilt["c1"], tilt["c2"]))
    delta_c = c2 - c1
    linear_tilt = delta_c * (y_tilt - c1) / (Q(2) * s_tilt)
    constant_penalty = delta_c**2 / (Q(4) * s_tilt)
    square_difference = ((y_tilt - c1) ** 2 - (y_tilt - c2) ** 2) / (Q(4) * s_tilt)

    heat = fixture["heatSeriesSample"]
    heat_degree = int(heat["degree"])
    t4 = chebyshev(heat_degree)
    heat_A = Q(heat["A"])
    heat_t = q(heat["time"])
    heat_c = q(heat["edgeCoordinate"])
    evaluation = Q(1) + heat_c / heat_A
    forward = heat_polynomial(t4, heat_t / heat_A**2, 1)
    backward = heat_polynomial(t4, heat_t / heat_A**2, -1)
    derivatives = [poly_eval(poly_derivative(t4, k), Q(1)) for k in range(heat_degree + 1)]
    derivative_formula = [Q(1)]
    for k in range(1, heat_degree + 1):
        product = Q(int(heat["degree"]) ** 2)
        for r in range(1, k):
            product *= Q(int(heat["degree"]) ** 2 - r**2)
        odd_double_factorial = math.prod(range(1, 2 * k, 2))
        derivative_formula.append(product / Q(odd_double_factorial))
    weights = []
    for j in range(heat_degree // 2 + 1):
        for ell in range(heat_degree + 1 - 2 * j):
            k = ell + 2 * j
            value = (
                derivatives[k]
                * heat_c**ell
                * heat_t**j
                / (heat_A**k * Q(math.factorial(ell)) * Q(math.factorial(j)))
            )
            weights.append({"ell": ell, "j": j, "k": k, "value": qs(value)})
    weight_values = [q(row["value"]) for row in weights]
    weight_sum = sum(weight_values, Q(0))
    mean_j = sum(Q(row["j"]) * value for row, value in zip(weights, weight_values)) / weight_sum
    mean_ell = sum(Q(row["ell"]) * value for row, value in zip(weights, weight_values)) / weight_sum
    mean_ell2 = (
        sum(Q(row["ell"] * (row["ell"] - 1)) * value for row, value in zip(weights, weight_values))
        / weight_sum
    )
    ell0 = [q(row["value"]) for row in weights if row["ell"] == 0]

    shear = fixture["integerShearSample"]
    shear_m = int(shear["degree"])
    eta = q(shear["eta"])
    shear_poly = chebyshev(shear_m)
    linear_w = [(Q(0), Q(1) / eta), (Q(0), -Q(1) / eta)]
    by_substitution = cpoly_compose_real(shear_poly, linear_w)
    by_derivative = transformed_derivative_coefficients(shear_poly, eta)
    real_substitution = [value[0] for value in by_substitution]
    real_derivative = [value[0] for value in by_derivative]
    first_mode = int(shear["firstMode"])
    modes = list(range(first_mode, first_mode + shear_m + 1))
    amplitudes = [Q(2) * abs(value) for value in real_substitution]
    phases = ["0" if value > 0 else "1" for value in real_substitution]
    pde_mode = int(shear["pdeCheckMode"])
    B = q(shear["backgroundShear"])
    dt_cos = -Q(pde_mode)**2
    dt_sin = Q(pde_mode) * B
    transport_sin = -B * Q(pde_mode)
    minus_laplacian_cos = Q(pde_mode)**2

    operator = fixture["operatorSample"]
    op_eta = q(operator["eta"])
    op_poly = [q(value) for value in operator["polynomialCoefficientsAscending"]]
    op_first = poly_derivative(op_poly)
    op_second = poly_derivative(op_poly, 2)
    # Complex-polynomial implementation of (1+i eta w)^2 p'' + i eta(1+i eta w)p'.
    one_plus = [(Q(1), Q(0)), (Q(0), op_eta)]
    op_l = cpoly_add(
        cpoly_mul(cpoly_mul(one_plus, one_plus), [(value, Q(0)) for value in op_second]),
        cpoly_mul(cpoly_scale(one_plus, (Q(0), op_eta)), [(value, Q(0)) for value in op_first]),
    )
    while len(op_l) < len(op_poly):
        op_l.append((Q(0), Q(0)))
    op_l = op_l[: len(op_poly)]
    op_d2 = [(value, Q(0)) for value in op_second] + [(Q(0), Q(0))] * (len(op_poly) - len(op_second))
    op_difference = [cadd(left, cscale(right, Q(-1))) for left, right in zip(op_l, op_d2)]

    geometry = fixture["geometryClockSample"]
    a, delta0, outer_delta, radius, time4 = map(
        q,
        (
            geometry["a"],
            geometry["delta0"],
            geometry["outerDelta"],
            geometry["pairedRadius"],
            geometry["terminalTime"],
        ),
    )
    R = q(geometry["R"])
    beta = q(geometry["beta"])
    r_center = q(geometry["rCenter"])
    half_width = q(geometry["halfWidth"])
    geom_A = a - delta0
    e_a = geom_A / a
    velocity = -beta / geom_A
    background = velocity * a / R
    geom_gamma = beta * a / geom_A
    c_plus = radius + delta0 + geom_gamma * time4
    c_minus = radius + delta0 - geom_gamma * time4
    subcap = r_center - half_width + delta0
    plateau = Q(2) * delta0
    strip_c0, strip_c1 = map(q, geometry["plateauStripC"])
    strip_z0 = Q(1) + (strip_c0 - delta0) / a
    strip_z1 = Q(1) + (strip_c1 - delta0) / a
    area0 = (a + delta0) ** 2 - a**2 * strip_z0**2
    area1 = (a + delta0) ** 2 - a**2 * strip_z1**2
    # On z>=1 the inner positive part vanishes; integrate in c with dz=dc/a.
    integrated_area = (
        (a + delta0) ** 2 * (strip_c1 - strip_c0)
        - ((a + strip_c1 - delta0) ** 3 - (a + strip_c0 - delta0) ** 3) / Q(3)
    ) / a

    norm = fixture["normalizationSample"]
    omega_rate = q(norm["omegaLogRate"])
    r_rate = q(norm["rLogRate"])
    a_over_l = q(norm["aOverL"])
    flux_coefficient = q(norm["physicalFluxCoefficient"])
    flux_a, flux_r = q(norm["physicalFluxAExponent"]), q(norm["physicalFluxRExponent"])
    mass_a, mass_r = q(norm["plateauMassAExponent"]), q(norm["plateauMassRExponent"])
    mass_power = Q(2, 3)
    quotient_a, quotient_r = flux_a - mass_power * mass_a, flux_r - mass_power * mass_r
    weighted_r = quotient_r + Q(1, 3)
    # L.12 normalizes the mass by R^-2 omega and flux by R^-1 omega.
    normalized_mass_r, normalized_flux_r, omega_power = Q(-2), Q(-1), Q(1)
    normalized_quotient_r = normalized_flux_r - mass_power * normalized_mass_r
    normalized_quotient_omega = omega_power - mass_power * omega_power
    total_r_power = quotient_r + normalized_quotient_r
    normalized_rate = total_r_power * r_rate + normalized_quotient_omega * omega_rate
    penalty = -omega_rate * normalized_quotient_omega / a_over_l**2
    formal_kappa = q(norm["formalKappa"])
    formal_saddle = rational_root(Q(2) * saddle_time * formal_kappa, 2)
    formal_tilt = rational_root(formal_kappa / (Q(2) * saddle_time), 2)
    critical_kappa = saddle_time * penalty**2 / (Q(2) * gap**2)

    back = fixture["backwardHeatSample"]
    back_n, back_m, back_A = int(back["n"]), int(back["m"]), Q(back["A"])
    back_t = q(back["time"])
    back_terms = []
    for j in range(back_n + 1):
        product = Q(1)
        for ell in range(j):
            product *= Q(back_n**2 - ell**2)
        back_terms.append(product * (Q(4) * back_t / back_A**2) ** j / Q(math.factorial(j)))
    back_poly = heat_polynomial(chebyshev(back_m), back_t / back_A**2, -1)
    wrong_poly = heat_polynomial(chebyshev(back_m), back_t / back_A**2, 1)
    axis_y = q(back["imaginaryAxisY"])
    positive_even = [Q(-1) ** back_n * coefficient * Q(-1) ** k for k, coefficient in enumerate(back_poly[::2])]
    axis_terms = [value * axis_y ** (2 * k) for k, value in enumerate(positive_even)]

    diagnostic = fixture["diagnostic"]
    data_path = ROOT / fixture["files"]["figureData"]
    with data_path.open(newline="", encoding="utf-8") as stream:
        data_rows = list(csv.DictReader(stream))
    columns = list(data_rows[0]) if data_rows else []
    max_saddle = max(float(row["saddleDerivativeResidual"]) for row in data_rows)
    max_grid_a = max(float(row["coarseFineAmplitudeDelta"]) for row in data_rows)
    max_grid_t = max(float(row["coarseFineTiltDelta"]) for row in data_rows)
    max_drop_a = max(float(row["phaseDropAmplitudeDelta"]) for row in data_rows)
    max_drop_t = max(float(row["phaseDropTiltDelta"]) for row in data_rows)
    progress = [
        json.loads(line)
        for line in (ROOT / fixture["files"]["figureProgress"]).read_text(encoding="utf-8").splitlines()
        if line
    ]
    with (ROOT / fixture["files"]["figureResources"]).open(newline="", encoding="utf-8") as stream:
        resources = list(csv.DictReader(stream))
    png_width, png_height, png_dpi = png_metadata(ROOT / fixture["files"]["figurePng"])
    pdf_raw = (ROOT / fixture["files"]["figurePdf"]).read_bytes()
    pdf_text = pdf_raw.decode("latin1")
    page_count = len(re.findall(r"/Type\s*/Page\b", pdf_text))
    svg_text = (ROOT / fixture["files"]["figureSvg"]).read_text(encoding="utf-8")

    exact = {
        "structure": {
            "firstTag": tags[0] if tags else None,
            "lastTag": tags[-1] if tags else None,
            "tagCount": len(tags),
            "displayCount": displays,
            "tagSequenceComplete": tags == list(range(fixture["structure"]["firstTag"], fixture["structure"]["lastTag"] + 1)),
            "referencesClosed": not (set(refs) - set(tags)),
        },
        "scaleSample": {
            "mSquaredOverA": qs(m**2 / A),
            "muCubed": qs(mu**3),
            "mu": qs(mu),
            "sqrtA": qs(sqrt_a),
            "gamma": qs(gamma),
            "gammaSquared": qs(gamma**2),
            "terminalLayerWidth": qs(Q(1) / (Q(1) + mu**2)),
            "clockResidualScale": qs(mu),
            "fixedSliceScale": qs(gamma),
            "commonHeatScale": qs(mu**2),
            "strictScaleOrdering": mu < gamma < mu**2,
            "powerLawRows": power_rows,
        },
        "saddleSample": {
            "basisOrder": ["1", "alpha", "alpha^2"],
            "generatorCube": saddle["generatorCube"],
            "z4": kjson(z4),
            "squareRootTwoZ4": kjson(root_two_z4),
            "F4": kjson(F4),
            "G4": kjson(G4),
            "twoG4": kjson(kscale(G4, Q(2))),
            "z4Cube": qs(kpow(z4, 3)[0]),
            "F4Cube": qs(kpow(F4, 3)[0]),
            "F3Cube": qs(f3_cube),
            "F4CubeMinusF3Cube": qs(kpow(F4, 3)[0] - f3_cube),
            "G4Cube": qs(kpow(G4, 3)[0]),
            "z4OverEight": kjson(kscale(z4, Q(1) / (Q(2) * saddle_time))),
            "squareRootTwoZ4Squared": kjson(kpow(root_two_z4, 2)),
            "twoZ4": kjson(kscale(z4, Q(2))),
            "F4FromRateFunction": kjson(ksub(root_two_z4, kscale(kpow(z4, 2), Q(1) / (Q(4) * saddle_time)))),
            "terminalDominatesTimeThree": kpow(F4, 3)[0] > f3_cube,
            "capPlateauGap": qs(gap),
            "squaredRatioSlopeForGap": kjson(kscale(G4, Q(2) * gap)),
            "squaredRatioSlopeForGapCube": qs(kpow(kscale(G4, Q(2) * gap), 3)[0]),
        },
        "tiltSample": {
            "deltaC": qs(delta_c),
            "baseCenteredY": qs(y_tilt - c1),
            "linearTilt": qs(linear_tilt),
            "constantPenalty": qs(constant_penalty),
            "logKernelRatioByTilt": qs(linear_tilt - constant_penalty),
            "logKernelRatioBySquareDifference": qs(square_difference),
            "tiltSignPositive": square_difference > 0,
        },
        "heatSeriesSample": {
            "chebyshevCoefficientsAscending": [qs(value) for value in t4],
            "endpointDerivativesDirect": [qs(value) for value in derivatives],
            "endpointDerivativesFormula": [qs(value) for value in derivative_formula],
            "successiveDerivativeRatios": [qs(derivatives[k + 1] / derivatives[k]) for k in range(heat_degree)],
            "allEndpointDerivativesPositive": all(value > 0 for value in derivatives),
            "forwardHeatCoefficientsAscending": [qs(value) for value in forward],
            "backwardHeatCoefficientsAscending": [qs(value) for value in backward],
            "evaluationPoint": qs(evaluation),
            "forwardHeatValue": qs(poly_eval(forward, evaluation)),
            "backwardHeatValue": qs(poly_eval(backward, evaluation)),
            "positiveWeights": weights,
            "weightSum": qs(weight_sum),
            "meanJ": qs(mean_j),
            "meanEll": qs(mean_ell),
            "meanEllEllMinusOne": qs(mean_ell2),
            "cSquaredMeanJOverTime": qs(heat_c**2 * mean_j / heat_t),
            "ellZeroSuccessiveJRatios": [qs(ell0[k + 1] / ell0[k]) for k in range(len(ell0) - 1)],
            "positiveSeriesIncreasingInTimeAndPositiveC": all(value > 0 for value in weight_values),
            "forwardBackwardDistinct": forward != backward,
        },
        "integerShearSample": {
            "wEtaCoefficientsAscending": [[qs(a), qs(b)] for a, b in linear_w],
            "transformedCoefficientsBySubstitution": [qs(value) for value in real_substitution],
            "transformedCoefficientsByDerivativeFormula": [qs(value) for value in real_derivative],
            "allTransformedCoefficientsNonzero": all(value != 0 for value in real_substitution),
            "carrier": qs(Q(first_mode) * eta),
            "modes": modes,
            "amplitudes": [qs(value) for value in amplitudes],
            "phasesOverPi": phases,
            "strictlyIncreasingModes": all(right == left + 1 for left, right in zip(modes, modes[1:])),
            "closedDyadicBand": modes[0] == shear_m and modes[-1] == 2 * shear_m,
            "pdeMode": pde_mode,
            "pdeTimeDerivativeCosineCoefficient": qs(dt_cos),
            "pdeTimeDerivativeSineCoefficient": qs(dt_sin),
            "pdeTransportSineCoefficient": qs(transport_sin),
            "pdeNegativeLaplacianCosineCoefficient": qs(minus_laplacian_cos),
            "pdeCosineResidual": qs(dt_cos + minus_laplacian_cos),
            "pdeSineResidual": qs(dt_sin + transport_sin),
        },
        "operatorSample": {
            "lEtaCoefficientsAscending": [[qs(a), qs(b)] for a, b in op_l],
            "secondDerivativeCoefficientsAscending": [[qs(a), qs(b)] for a, b in op_d2],
            "differenceCoefficientsAscending": [[qs(a), qs(b)] for a, b in op_difference],
            "firstOrderImaginarySignPositive": op_difference[1][1] > 0,
            "degreePreserved": len(op_l) <= len(op_poly),
        },
        "geometryClockSample": {
            "A": qs(geom_A),
            "eA": qs(e_a),
            "scaledVelocity": qs(velocity),
            "backgroundShear": qs(background),
            "gamma": qs(geom_gamma),
            "rCenterMinusThreeHalfWidths": qs(r_center - Q(3) * half_width),
            "rCenterPlusThreeHalfWidths": qs(r_center + Q(3) * half_width),
            "strictSubcapGeometry": delta0 < r_center - Q(3) * half_width < r_center + Q(3) * half_width < outer_delta,
            "positiveEdgeCoordinate": qs(c_plus),
            "negativeEdgeCoordinate": qs(c_minus),
            "pairedCoordinateGap": qs(c_plus - c_minus),
            "subcapCoordinate": qs(subcap),
            "plateauCoordinate": qs(plateau),
            "capPlateauGap": qs(subcap - plateau),
            "terminalCapCoordinate": qs(subcap + geom_gamma * time4),
            "terminalPlateauCoordinate": qs(plateau + geom_gamma * time4),
            "terminalCoordinateGap": qs(subcap - plateau),
            "plateauStripZ": [qs(strip_z0), qs(strip_z1)],
            "plateauStripZWidth": qs(strip_z1 - strip_z0),
            "areaOverPiAtStripEndpoints": [qs(area0), qs(area1)],
            "integratedStripAreaOverPi": qs(integrated_area),
            "velocitySign": -1 if velocity < 0 else 1,
            "positiveWeightSign": -1,
            "pairedSquareDifferenceSign": (c_plus > c_minus) - (c_plus < c_minus),
            "pairedFluxSign": 1 if velocity * Q(-1) * (c_plus - c_minus) > 0 else -1,
        },
        "normalizationSample": {
            "physicalFlux": {"coefficient": qs(flux_coefficient), "aExponent": qs(flux_a), "rExponent": qs(flux_r)},
            "plateauMass": {"coefficient": "1", "aExponent": qs(mass_a), "rExponent": qs(mass_r)},
            "unweightedQuotient": {"coefficient": qs(flux_coefficient), "aExponent": qs(quotient_a), "rExponent": qs(quotient_r)},
            "rWeightedQuotient": {"coefficient": qs(flux_coefficient), "aExponent": qs(quotient_a), "rExponent": qs(weighted_r)},
            "lowerBoundAExponent": qs(quotient_a - mass_power),
            "lowerBoundTerminalLayerExponent": qs(Q(1) - mass_power * Q(0)),
            "upperBoundAExponent": qs(quotient_a),
            "upperBoundTerminalLayerExponent": qs(Q(0) - mass_power * Q(1)),
            "normalizedPlateau": {"rExponent": qs(normalized_mass_r), "omegaExponent": qs(omega_power)},
            "normalizedFlux": {"rExponent": qs(normalized_flux_r), "omegaExponent": qs(omega_power)},
            "normalizedQuotientFactor": {"rExponent": qs(normalized_quotient_r), "omegaExponent": qs(normalized_quotient_omega)},
            "omegaThirdLogRate": qs(normalized_rate),
            "aSquaredLeadingDensity": qs(a_over_l**2),
            "aSquaredPenaltyCoefficient": qs(penalty),
            "aSquaredPenaltyLogRate": qs(-a_over_l**2 * penalty),
            "formalHighDegree": {
                "status": "OPEN_DIRECTION",
                "kappa": norm["formalKappa"],
                "heatTime": qs(saddle_time),
                "capPlateauGap": qs(gap),
                "integrationSaddleCoefficient": qs(formal_saddle),
                "physicalDisplacementCoefficient": qs(formal_saddle),
                "tiltCoefficient": qs(formal_tilt),
                "squaredRatioExponentCoefficient": qs(Q(2) * gap * formal_tilt),
                "criticalKappa": qs(critical_kappa),
                "sampleExceedsFormalThreshold": q(norm["formalKappa"]) > critical_kappa,
            },
        },
        "backwardHeatSample": {
            "terms": [qs(value) for value in back_terms],
            "exactAbsoluteValue": qs(sum(back_terms, Q(0))),
            "wrongForwardSignAbsoluteValue": qs(sum((Q(-1) ** j) * value for j, value in enumerate(back_terms))),
            "backwardPolynomialCoefficientsAscending": [qs(value) for value in back_poly],
            "wrongForwardPolynomialCoefficientsAscending": [qs(value) for value in wrong_poly],
            "imaginaryAxisPositiveEvenCoefficients": [qs(value) for value in positive_even],
            "imaginaryAxisTerms": [qs(value) for value in axis_terms],
            "imaginaryAxisValue": qs(sum(axis_terms, Q(0))),
            "forwardBackwardDistinct": back_poly != wrong_poly,
        },
        "diagnostic": {
            "rowCount": len(data_rows),
            "columnCount": len(columns),
            "columns": columns,
            "AValues": sorted({int(row["A"]) for row in data_rows}),
            "degreePowers": [qs(value) for value in sorted({q(row["degreePower"]) for row in data_rows})],
            "theoreticalLimitDecimals": {
                "saddle": data_rows[0]["saddleLimit"],
                "amplitude": data_rows[0]["amplitudeLimit"],
                "tilt": data_rows[0]["tiltLimit"],
            },
            "maximumSaddleDerivativeResidual": f"{max_saddle:.12e}",
            "maximumCoarseFineAmplitudeDelta": f"{max_grid_a:.12e}",
            "maximumCoarseFineTiltDelta": f"{max_grid_t:.12e}",
            "maximumPhaseDropAmplitudeDelta": f"{max_drop_a:.12e}",
            "maximumPhaseDropTiltDelta": f"{max_drop_t:.12e}",
            "progressEventCount": len(progress),
            "resourceSampleCount": len(resources),
            "progressStages": list(dict.fromkeys(row["stage"] for row in progress)),
            "pngPixels": [png_width, png_height],
            "pngDpi": png_dpi,
            "pdfPages": page_count,
            "pdfEncrypted": "/Encrypt" in pdf_text,
            "pdfHasJavaScript": "/JavaScript" in pdf_text or "/JS" in pdf_text,
            "svgWidth": re.search(r'<svg[^>]+width="([^"]+)"', svg_text).group(1),  # type: ignore[union-attr]
            "svgHeight": re.search(r'<svg[^>]+height="([^"]+)"', svg_text).group(1),  # type: ignore[union-attr]
            "panelCount": sum(svg_text.count(label) for label in (">(a)<", ">(b)<", ">(c)<")),
            "monotonicityRequired": diagnostic["monotonicityRequired"],
            "knownPreasymptoticAwaySequence": diagnostic["knownPreasymptoticAwaySequence"],
            "finiteDiagnosticOnly": True,
        },
        "claims": fixture["claims"],
    }

    tolerance = lambda value: float(q(value))
    degree_ok = all(
        int(row["m"]) == max(2, 2 * int(round((int(row["A"]) ** float(row["degreePower"])) / 2.0)))
        for row in data_rows
    )
    mu_ok = all(
        abs(float(row["mu"]) ** 3 - int(row["m"]) ** 2 / int(row["A"]))
        / (int(row["m"]) ** 2 / int(row["A"]))
        < tolerance(diagnostic["muIdentityRelativeTolerance"])
        for row in data_rows
    )
    finite_ok = all(math.isfinite(float(value)) for row in data_rows for value in row.values())
    error_ok = all(
        abs((float(row[field]) - float(row[limit])) - float(row[error])) < 2.0e-12
        for row in data_rows
        for field, limit, error in (
            ("saddleOverMu", "saddleLimit", "saddleError"),
            ("logIntegralOverMuSquared", "amplitudeLimit", "amplitudeError"),
            ("unitTiltOverMu", "tiltLimit", "tiltError"),
        )
    )
    limit_expected = (
        2.0 ** (5.0 / 3.0),
        3.0 * 2.0 ** (-2.0 / 3.0),
        2.0 ** (-4.0 / 3.0),
    )
    limit_ok = all(
        abs(float(data_rows[0][field]) - expected_value)
        < tolerance(diagnostic["limitDecimalTolerance"])
        for field, expected_value in zip(
            ("saddleLimit", "amplitudeLimit", "tiltLimit"), limit_expected
        )
    )
    p075 = [row for row in data_rows if row["degreePower"] == "0.75"]
    p075.sort(key=lambda row: int(row["A"]))
    away_ok = all(
        float(right["unitTiltOverMu"]) < float(left["unitTiltOverMu"])
        for left, right in zip(p075, p075[1:])
    )
    progress_elapsed = [float(row["elapsedSeconds"]) for row in progress]
    resource_elapsed = [float(row["elapsedSeconds"]) for row in resources]
    figure_config = json.loads((ROOT / fixture["files"]["figureConfig"]).read_text(encoding="utf-8"))
    config_numeric = ("heatTime", "phaseDrop", "fineGridPoints", "coarseGridPoints",
                      "figureWidthMillimetres", "figureHeightMillimetres")
    config_ok = all(q(figure_config[key]) == q(diagnostic[key]) for key in config_numeric)
    config_ok = config_ok and all(
        [q(value) for value in figure_config[key]] == [q(value) for value in diagnostic[key]]
        for key in ("edgeCoordinates", "AValues", "degreePowers")
    )
    config_ok = config_ok and all(
        figure_config[key] == diagnostic[key] for key in ("schema", "degreePolicy")
    )
    isolation_left, isolation_right = map(q, saddle["generatorIsolatingInterval"])
    diagnostics = {
        "fullComplexShear": by_substitution == by_derivative
        and all(imaginary == 0 for _, imaginary in by_substitution),
        "cubicField": saddle["cubicGenerator"] == "alpha"
        and q(saddle["generatorCube"]) == Q(2)
        and Q(0) < isolation_left < isolation_right
        and isolation_left**3 < Q(2) < isolation_right**3,
        "structureInventory": all(
            exact["structure"][key] == fixture["structure"][key]
            for key in ("firstTag", "lastTag", "tagCount", "displayCount")
        ) and fixture["structure"]["equationPrefix"] == "L",
        "figureConfig": config_ok,
        "finite": finite_ok,
        "degreePolicy": degree_ok,
        "muIdentity": mu_ok,
        "limitConstants": limit_ok,
        "errorColumns": error_ok,
        "saddleGate": max_saddle <= tolerance(diagnostic["saddleResidualTolerance"]),
        "gridGate": max(max_grid_a, max_grid_t) <= tolerance(diagnostic["coarseFineTolerance"]),
        "phaseDropGate": max(max_drop_a, max_drop_t) <= tolerance(diagnostic["phaseDropTolerance"]),
        "progressStages": [row["stage"] for row in progress].count("start") == 1
        and [row["stage"] for row in progress].count("quadrature") == 16
        and [row["stage"] for row in progress].count("complete") == 1,
        "progressMonotone": progress_elapsed == sorted(progress_elapsed),
        "resourcesMonotone": resource_elapsed == sorted(resource_elapsed),
        "preasymptoticAwayRecorded": away_ok,
    }
    return exact, diagnostics


def corrupt_observation(exact: dict[str, Any], mutation: str) -> None:
    """Negative controls corrupt observed ledgers, never a check or verdict.

    These test validation sensitivity, not the analytic proof. Computation
    sensitivity is separately checked by varying fixture arithmetic inputs.
    """
    targets: dict[str, tuple[tuple[str, ...], Any]] = {
        "forward_heat_sign": (("heatSeriesSample", "forwardHeatValue"), exact["heatSeriesSample"]["backwardHeatValue"]),
        "backward_heat_sign": (("backwardHeatSample", "wrongForwardSignAbsoluteValue"), exact["backwardHeatSample"]["exactAbsoluteValue"]),
        "saddle_z_cube": (("saddleSample", "z4Cube"), "31"),
        "saddle_F_cube": (("saddleSample", "F4Cube"), "27/8"),
        "terminal_G_sign": (("saddleSample", "G4Cube"), "-1/16"),
        "gaussian_tilt_penalty": (("tiltSample", "logKernelRatioByTilt"), "63/16"),
        "positive_series_weight": (("heatSeriesSample", "weightSum"), "299/8"),
        "moment_identity": (("heatSeriesSample", "meanEllEllMinusOne"), "425/291"),
        "terminal_layer_power": (("scaleSample", "terminalLayerWidth"), "1/5"),
        "operator_first_order_sign": (("operatorSample", "differenceCoefficientsAscending"), [["0", "0"], ["0", "-3"], ["-1/2", "0"]]),
        "integer_mode_upper_endpoint": (("integerShearSample", "modes"), [4, 5, 6, 7, 9]),
        "drift_sign": (("geometryClockSample", "scaledVelocity"), "1/40"),
        "paired_cap_swap": (("geometryClockSample", "pairedCoordinateGap"), "-2"),
        "plateau_jacobian": (("geometryClockSample", "integratedStripAreaOverPi"), "191/24"),
        "physical_R_power": (("normalizationSample", "rWeightedQuotient", "rExponent"), "1"),
        "normalization_omega_third": (("normalizationSample", "omegaThirdLogRate"), "-2/3969"),
        "high_degree_open_to_theorem": (("normalizationSample", "formalHighDegree", "status"), "PROVED"),
        "arbitrary_packet_upgrade": (("claims", "uniformArbitraryPacketTheorem"), True),
        "version_m_upgrade": (("claims", "versionMTransfer"), True),
        "diagnostic_to_proof": (("claims", "finiteDiagnosticProvesLimit"), True),
        "figure_row_count": (("diagnostic", "rowCount"), 15),
        "figure_limit_constant": (("diagnostic", "theoreticalLimitDecimals", "tilt"), "0.5"),
        "progress_missing_complete": (("diagnostic", "progressStages"), ["start", "quadrature"]),
    }
    if mutation not in targets:
        return
    path, value = targets[mutation]
    target = exact
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def main() -> int:
    args = parse_args()
    if args.list_mutations:
        print("\n".join(MUTATIONS))
        return 0
    mutation = args.mutation or os.environ.get("R076L_MUTATION", "")
    if mutation and mutation not in MUTATIONS:
        print(f"unknown mutation: {mutation}", file=sys.stderr)
        return 2

    fixture = json.loads(FIXTURES.read_text(encoding="utf-8"))
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    expected_exact = {key: value for key, value in expected.items() if key != "schema"}
    exact, diagnostic_checks = build_exact(fixture)
    corrupt_observation(exact, mutation)

    frozen = dict(fixture["frozen"]["sha256"])
    if mutation == "generated_output_bound":
        frozen[f"research/{STEM}_certificate.json"] = "0" * 64
    elif mutation == "agents_file_bound":
        frozen["AGENTS.md"] = sha256(ROOT / "AGENTS.md") or "0" * 64
    frozen[f"scripts/{STEM}_fixtures.json"] = FIXTURE_SHA256
    frozen[f"scripts/{STEM}_expected.json"] = EXPECTED_SHA256
    bindings = {relative: binding(relative, digest) for relative, digest in sorted(frozen.items())}

    source_commit = fixture["frozen"]["sourceCommit"]
    source_ready = bool(re.fullmatch(r"[0-9a-f]{40}", source_commit))
    source_tree_ok = False
    if source_ready:
        source_tree_ok = all(
            git_file_bytes(source_commit, relative) == (ROOT / relative).read_bytes()
            for relative in fixture["frozen"]["sha256"]
        )
    elif args.development and source_commit == "__SOURCE_COMMIT__":
        source_tree_ok = True

    text_paths = [
        fixture["files"]["main"],
        fixture["files"]["source"],
        fixture["files"]["primaryAudit"],
    ]
    text_raw = [(ROOT / path).read_bytes() for path in text_paths]
    text_clean = all(
        b"\r" not in raw
        and b"\t" not in raw
        and not re.search(rb"[ \t]+$", raw, re.M)
        and not any((byte < 32 and byte != 10) or byte == 127 for byte in raw)
        for raw in text_raw
    )
    main_text, source_text, audit_text = [raw.decode("utf-8") for raw in text_raw]
    forbidden = (
        "AGENTS.md",
        "__pycache__",
        ".pyc",
        f"research/{STEM}_certificate.json",
        f"research/{STEM}_certificate_report.md",
        f"research/{STEM}_independent_audit.md",
        f"research/{STEM}_qa_report.md",
        "publication",
        "public/",
    )
    frozen_paths = list(frozen)
    no_forbidden = not any(token in path for path in frozen_paths for token in forbidden)

    claims = fixture["claims"]
    proved_true = [
        "explicitStartPrepaidFamily",
        "forwardHeatObject",
        "completeClockEventuallyPositiveForFamily",
        "fullPhysicalPlateauUsed",
        "normalizedQuadraticRateEstablishedForFamily",
        "fixedSliceMuThreeHalvesReducedToClockMu",
        "candidateKilledForThisFamily",
        "formalScientificFigureIncluded",
        "finiteDiagnosticIncluded",
    ]
    boundary_false = [key for key in claims if key not in proved_true]
    claim_values_ok = all(claims[key] is True for key in proved_true) and all(
        claims[key] is False for key in boundary_false
    )

    checks: dict[str, bool] = {
        "fixture_schema": fixture.get("schema") == FIXTURE_SCHEMA,
        "expected_schema": expected.get("schema") == EXPECTED_SCHEMA,
        "fixture_hash_ready": bool(re.fullmatch(r"[0-9a-f]{64}", FIXTURE_SHA256))
        or (args.development and FIXTURE_SHA256 == "__FIXTURE_SHA256__"),
        "expected_hash_ready": bool(re.fullmatch(r"[0-9a-f]{64}", EXPECTED_SHA256))
        or (args.development and EXPECTED_SHA256 == "__EXPECTED_SHA256__"),
        "all_bindings": all(row["pass"] for row in bindings.values())
        or (
            args.development
            and all(
                row["pass"]
                for path, row in bindings.items()
                if path not in {f"scripts/{STEM}_fixtures.json", f"scripts/{STEM}_expected.json"}
            )
        ),
        "source_commit_ready": source_ready or (args.development and source_commit == "__SOURCE_COMMIT__"),
        "source_tree_bindings": source_tree_ok,
        "upstream_commit": fixture["frozen"]["upstreamCoreCommit"] == UPSTREAM_COMMIT,
        "upstream_tree": all(
            git_file_bytes(UPSTREAM_COMMIT, fixture["files"][key])
            == (ROOT / fixture["files"][key]).read_bytes()
            for key in ("r076kMain", "r076kSource", "r076kPrimaryAudit", "r076kCertificate", "r076kQaReport")
        ),
        "frozen_inventory": len(fixture["frozen"]["sha256"]) == 19
        and len(fixture["files"]) == 19
        and set(fixture["files"].values()) == set(fixture["frozen"]["sha256"]),
        "no_forbidden_bindings": no_forbidden,
        "text_hygiene": text_clean,
        "tag_sequence": exact["structure"]["tagSequenceComplete"] is True,
        "display_inventory": diagnostic_checks["structureInventory"],
        "reference_closure": exact["structure"]["referencesClosed"] is True,
        "scale_identity": exact["scaleSample"]["mSquaredOverA"] == "64"
        and exact["scaleSample"]["muCubed"] == "64",
        "scale_ordering": exact["scaleSample"]["strictScaleOrdering"] is True,
        "terminal_layer": exact["scaleSample"]["terminalLayerWidth"] == "1/17",
        "power_law_ledger": len(exact["scaleSample"]["powerLawRows"]) == 5,
        "saddle_z": exact["saddleSample"]["z4Cube"] == "32" and diagnostic_checks["cubicField"],
        "saddle_F": exact["saddleSample"]["F4Cube"] == "27/4",
        "saddle_G": exact["saddleSample"]["G4Cube"] == "1/16",
        "terminal_time_dominance": exact["saddleSample"]["terminalDominatesTimeThree"] is True,
        "terminal_gap_slope": exact["saddleSample"]["squaredRatioSlopeForGapCube"] == "27/16",
        "gaussian_tilt": exact["tiltSample"]["logKernelRatioByTilt"] == "45/16"
        and exact["tiltSample"]["logKernelRatioBySquareDifference"] == "45/16",
        "heat_endpoint_derivatives": exact["heatSeriesSample"]["endpointDerivativesDirect"]
        == exact["heatSeriesSample"]["endpointDerivativesFormula"],
        "forward_heat": exact["heatSeriesSample"]["forwardHeatValue"] == "291/8",
        "backward_heat_control": exact["heatSeriesSample"]["backwardHeatValue"] == "91/8",
        "positive_series": exact["heatSeriesSample"]["weightSum"] == "291/8"
        and exact["heatSeriesSample"]["positiveSeriesIncreasingInTimeAndPositiveC"] is True,
        "moment_identity": exact["heatSeriesSample"]["meanEllEllMinusOne"]
        == exact["heatSeriesSample"]["cSquaredMeanJOverTime"] == "424/291",
        "integer_coefficients": exact["integerShearSample"]["transformedCoefficientsBySubstitution"]
        == exact["integerShearSample"]["transformedCoefficientsByDerivativeFormula"]
        and diagnostic_checks["fullComplexShear"],
        "integer_band": exact["integerShearSample"]["modes"] == [4, 5, 6, 7, 8]
        and exact["integerShearSample"]["closedDyadicBand"] is True,
        "pde_residual": exact["integerShearSample"]["pdeCosineResidual"] == "0"
        and exact["integerShearSample"]["pdeSineResidual"] == "0",
        "operator_sign": exact["operatorSample"]["firstOrderImaginarySignPositive"] is True
        and exact["operatorSample"]["differenceCoefficientsAscending"][1] == ["0", "3"],
        "geometry_drift": exact["geometryClockSample"]["scaledVelocity"] == "-1/40",
        "paired_coordinates": exact["geometryClockSample"]["pairedCoordinateGap"] == "2"
        and exact["geometryClockSample"]["pairedFluxSign"] == 1,
        "subcap_gap": exact["geometryClockSample"]["capPlateauGap"] == "3/2",
        "plateau_jacobian": exact["geometryClockSample"]["integratedStripAreaOverPi"] == "191/240",
        "physical_scaling": exact["normalizationSample"]["rWeightedQuotient"]["rExponent"] == "0",
        "normalization_rate": exact["normalizationSample"]["omegaThirdLogRate"] == "-2/11907"
        and exact["normalizationSample"]["aSquaredPenaltyLogRate"] == "-2/11907",
        "high_degree_open": exact["normalizationSample"]["formalHighDegree"]["status"] == "OPEN_DIRECTION"
        and exact["normalizationSample"]["formalHighDegree"]["criticalKappa"] == "1/2654208",
        "backward_terms": exact["backwardHeatSample"]["exactAbsoluteValue"] == "614/243",
        "backward_wrong_sign": exact["backwardHeatSample"]["wrongForwardSignAbsoluteValue"] == "88/243",
        "imaginary_axis": exact["backwardHeatSample"]["imaginaryAxisValue"] == "2663/729",
        "diagnostic_finite": diagnostic_checks["finite"],
        "diagnostic_degree_policy": diagnostic_checks["degreePolicy"],
        "diagnostic_mu_identity": diagnostic_checks["muIdentity"],
        "diagnostic_limits": diagnostic_checks["limitConstants"]
        and exact["diagnostic"]["theoreticalLimitDecimals"] == expected_exact["diagnostic"]["theoreticalLimitDecimals"],
        "diagnostic_errors": diagnostic_checks["errorColumns"],
        "diagnostic_saddle_gate": diagnostic_checks["saddleGate"],
        "diagnostic_grid_gate": diagnostic_checks["gridGate"],
        "diagnostic_phase_drop_gate": diagnostic_checks["phaseDropGate"],
        "diagnostic_progress": diagnostic_checks["progressStages"] and diagnostic_checks["progressMonotone"]
        and exact["diagnostic"]["progressStages"] == ["start", "quadrature", "complete"],
        "diagnostic_resources": diagnostic_checks["resourcesMonotone"],
        "diagnostic_preasymptotic_boundary": diagnostic_checks["preasymptoticAwayRecorded"],
        "figure_formats": all(
            exact["diagnostic"][key] == fixture["diagnostic"][key]
            for key in ("rowCount", "columnCount", "AValues", "degreePowers",
                        "progressEventCount", "resourceSampleCount", "pngPixels", "pngDpi", "pdfPages")
        ) and exact["diagnostic"]["panelCount"] == 3
        and exact["diagnostic"]["svgWidth"] == f'{fixture["diagnostic"]["figureWidthMillimetres"]}mm'
        and exact["diagnostic"]["svgHeight"] == f'{fixture["diagnostic"]["figureHeightMillimetres"]}mm'
        and diagnostic_checks["figureConfig"],
        "claims_inventory": len(claims) == 21,
        "claims_values": claim_values_ok,
        "main_claim_boundary": all(marker in main_text for marker in ("LITERATURE-ESTABLISHED", "PROVED LOCALLY", "FINITE COMPUTATION", "OPEN", "NOT CLAY")),
        "source_claim_boundary": all(marker in source_text for marker in ("CLASSICAL INPUT", "PROVED LOCALLY", "OPEN DIRECTION", "NOT CLAY")),
        "primary_pass": "**PASS" in audit_text and "**NOT CLAY.**" in audit_text,
        "no_novelty_priority": claims["noveltyClaimed"] is False and claims["priorityClaimed"] is False,
        "not_clay": claims["clayClaimed"] is False,
        "full_expected_match": exact == expected_exact,
    }

    failures = [name for name, passed in checks.items() if not passed]
    verdict = "PASS" if not failures else "FAIL"
    freeze_ready = verdict == "PASS" and source_ready and not args.development
    certificate = {
        "schema": CERT_SCHEMA,
        "verdict": verdict,
        "freezeReady": freeze_ready,
        "development": args.development,
        "sourceCommit": source_commit,
        "upstreamCommit": UPSTREAM_COMMIT,
        "assertionsTotal": len(checks),
        "assertionsPassed": sum(checks.values()),
        "failures": failures,
        "negativeMutations": MUTATIONS,
        "bindings": bindings,
        "exact": exact,
        "claimBoundary": {
            "finiteCertificateProvesAsymptotics": False,
            "finiteCertificateProvesSemigroupTheorem": False,
            "finiteCertificateProvesSignedClock": False,
            "finiteDiagnosticProvesLimit": False,
            "regularityOrSingularityClaim": False,
            "notClay": True,
        },
    }
    rendered = (json.dumps(certificate, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(rendered)
    else:
        sys.stdout.buffer.write(rendered)
    if args.report:
        report = f"""# R0.76L finite certificate report

Verdict: **{verdict}**

- Freeze ready: `{str(freeze_ready).lower()}`
- Assertions: `{sum(checks.values())}/{len(checks)}`
- Negative controls: `{len(MUTATIONS)}`
- Source commit: `{source_commit}`
- Upstream R0.76K core: `{UPSTREAM_COMMIT}`

The certificate recomputes finite exact ledgers and binds the archived
diagnostic.  It does not prove L.22, L.25, L.29, L.47, the continuum signed
clock estimate, regularity, singularity, novelty, or priority.  **NOT CLAY.**
"""
        args.report.write_text(report, encoding="utf-8")
    if args.check and not freeze_ready:
        return 1
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
