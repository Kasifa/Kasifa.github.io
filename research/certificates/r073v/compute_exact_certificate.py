#!/usr/bin/env python3
"""Build the exact R0.73V signed-third-order finite certificate.

The producer uses only Python's standard library.  Every coefficient is a
polynomial in q=exp(-s), with Gaussian-rational coefficients represented by
fractions.Fraction.  There is no floating point, tolerance, network access,
GPU, or DGX computation.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CHECKLIST_PATH = HERE / "audit-checklist.json"
CONTRACT_PATH = HERE / "contract.json"
RESULTS_PATH = HERE / "results.json"

F = Fraction
Mode = tuple[int, int, int]
Gaussian = tuple[Fraction, Fraction]
Poly = dict[int, Gaussian]
ScalarField = dict[Mode, Poly]

ZERO: Gaussian = (F(0), F(0))
I: Gaussian = (F(0), F(1))
TARGET: Mode = (1, 2, 0)
QUARTIC_TARGET: Mode = (0, 2, 0)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink(), "missing regular JSON: " + str(path))
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys)
    require(isinstance(value, dict), "JSON root must be an object: " + str(path))
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: int | Fraction) -> str:
    return str(F(value))


def z(real: int | Fraction = 0, imag: int | Fraction = 0) -> Gaussian:
    return F(real), F(imag)


def gadd(a: Gaussian, b: Gaussian) -> Gaussian:
    return a[0] + b[0], a[1] + b[1]


def gneg(a: Gaussian) -> Gaussian:
    return -a[0], -a[1]


def gmul(a: Gaussian, b: Gaussian) -> Gaussian:
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def gscale(a: Gaussian, scalar: int | Fraction) -> Gaussian:
    factor = F(scalar)
    return a[0] * factor, a[1] * factor


def gconj(a: Gaussian) -> Gaussian:
    return a[0], -a[1]


def gexpr(a: Gaussian) -> str:
    real, imag = a
    if imag == 0:
        return qstr(real)
    if real == 0:
        if imag == 1:
            return "i"
        if imag == -1:
            return "-i"
        return qstr(imag) + "*i"
    sign = "+" if imag > 0 else "-"
    magnitude = abs(imag)
    suffix = "i" if magnitude == 1 else qstr(magnitude) + "*i"
    return qstr(real) + sign + suffix


def pclean(poly: Poly) -> Poly:
    return {exponent: coefficient for exponent, coefficient in poly.items() if coefficient != ZERO}


def pconst(value: Gaussian) -> Poly:
    return {} if value == ZERO else {0: value}


def padd(a: Poly, b: Poly) -> Poly:
    result = dict(a)
    for exponent, coefficient in b.items():
        result[exponent] = gadd(result.get(exponent, ZERO), coefficient)
    return pclean(result)


def pneg(a: Poly) -> Poly:
    return {exponent: gneg(coefficient) for exponent, coefficient in a.items()}


def pscale(a: Poly, scalar: Gaussian) -> Poly:
    return pclean({exponent: gmul(coefficient, scalar) for exponent, coefficient in a.items()})


def pmul(a: Poly, b: Poly) -> Poly:
    result: Poly = {}
    for left_exp, left_coefficient in a.items():
        for right_exp, right_coefficient in b.items():
            exponent = left_exp + right_exp
            result[exponent] = gadd(
                result.get(exponent, ZERO),
                gmul(left_coefficient, right_coefficient),
            )
    return pclean(result)


def pshift(a: Poly, exponent: int) -> Poly:
    return {power + exponent: coefficient for power, coefficient in a.items()}


def peval(a: Poly, value: Fraction) -> Gaussian:
    result = ZERO
    for exponent, coefficient in a.items():
        result = gadd(result, gscale(coefficient, value ** exponent))
    return result


def pderivative(a: Poly) -> Poly:
    return pclean({
        exponent - 1: gscale(coefficient, exponent)
        for exponent, coefficient in a.items()
        if exponent > 0
    })


def small_s(poly: Poly) -> dict[str, object]:
    if not poly:
        return {"leadingCoefficient": "0", "order": "infinity"}
    derivative = poly
    order = 0
    at_one = peval(derivative, F(1))
    while at_one == ZERO:
        derivative = pderivative(derivative)
        order += 1
        require(derivative, "nonzero polynomial lost during multiplicity calculation")
        at_one = peval(derivative, F(1))
    factorial = 1
    for integer in range(2, order + 1):
        factorial *= integer
    leading = gscale(at_one, F((-1) ** order, factorial))
    return {"leadingCoefficient": gexpr(leading), "order": order}


def poly_json(poly: Poly) -> dict[str, object]:
    return {
        "coefficients": {str(exponent): gexpr(coefficient) for exponent, coefficient in sorted(poly.items())},
        "smallS": small_s(poly),
    }


def mode_key(mode: Mode) -> str:
    return ",".join(str(value) for value in mode)


def add_mode(a: Mode, b: Mode) -> Mode:
    return tuple(a[index] + b[index] for index in range(3))  # type: ignore[return-value]


def neg_mode(a: Mode) -> Mode:
    return tuple(-value for value in a)  # type: ignore[return-value]


def norm2(mode: Mode) -> int:
    return sum(value * value for value in mode)


def fclean(field: ScalarField) -> ScalarField:
    return {mode: pclean(poly) for mode, poly in field.items() if pclean(poly)}


def fadd(a: ScalarField, b: ScalarField) -> ScalarField:
    result = {mode: dict(poly) for mode, poly in a.items()}
    for mode, poly in b.items():
        result[mode] = padd(result.get(mode, {}), poly)
    return fclean(result)


def fneg(a: ScalarField) -> ScalarField:
    return {mode: pneg(poly) for mode, poly in a.items()}


def fscale(a: ScalarField, scalar: Gaussian) -> ScalarField:
    return fclean({mode: pscale(poly, scalar) for mode, poly in a.items()})


def fmul(a: ScalarField, b: ScalarField) -> ScalarField:
    result: ScalarField = {}
    for left_mode, left_poly in a.items():
        for right_mode, right_poly in b.items():
            mode = add_mode(left_mode, right_mode)
            result[mode] = padd(result.get(mode, {}), pmul(left_poly, right_poly))
    return fclean(result)


def heat(a: ScalarField) -> ScalarField:
    return {mode: pshift(poly, norm2(mode)) for mode, poly in a.items()}


def derivative(a: ScalarField, index: int) -> ScalarField:
    return fclean({
        mode: pscale(poly, z(0, mode[index]))
        for mode, poly in a.items()
        if mode[index] != 0
    })


def component(field: ScalarField, mode: Mode) -> Poly:
    return field.get(mode, {})


def conjugate_completion(positive: dict[Mode, tuple[Gaussian, Gaussian, Gaussian]]) -> list[ScalarField]:
    velocity: list[ScalarField] = [{}, {}, {}]
    for mode, vector in positive.items():
        negative = neg_mode(mode)
        require(negative not in positive, "positive support contains a conjugate pair")
        for index in range(3):
            velocity[index][mode] = pconst(vector[index])
            velocity[index][negative] = pconst(gconj(vector[index]))
    return velocity


def four_site_velocity() -> list[ScalarField]:
    return conjugate_completion({
        (1, 0, 0): (z(), z(0, -1), z()),
        (1, 1, 0): (z(0, -1), z(0, 1), z()),
    })


def six_site_velocity() -> list[ScalarField]:
    return conjugate_completion({
        (0, 1, 0): (z(0, -3), z(), z()),
        (1, 0, 0): (z(), z(0, -2), z()),
        (1, 1, 0): (z(0, 2), z(0, -2), z()),
    })


def field_coefficients_json(velocity: list[ScalarField]) -> dict[str, list[str]]:
    modes = sorted(set().union(*(field.keys() for field in velocity)))
    result: dict[str, list[str]] = {}
    for mode in modes:
        result[mode_key(mode)] = [gexpr(peval(component(field, mode), F(1))) for field in velocity]
    return result


def field_reality(velocity: list[ScalarField]) -> bool:
    modes = set().union(*(field.keys() for field in velocity))
    for mode in modes:
        opposite = neg_mode(mode)
        for index in range(3):
            value = peval(component(velocity[index], mode), F(1))
            other = peval(component(velocity[index], opposite), F(1))
            if other != gconj(value):
                return False
    return True


def field_divergence(velocity: list[ScalarField]) -> bool:
    modes = set().union(*(field.keys() for field in velocity))
    for mode in modes:
        total = ZERO
        for index in range(3):
            total = gadd(total, gscale(peval(component(velocity[index], mode), F(1)), mode[index]))
        if total != ZERO:
            return False
    return True


def tensor_product(velocity: list[ScalarField]) -> list[list[ScalarField]]:
    return [[fmul(velocity[i], velocity[j]) for j in range(3)] for i in range(3)]


def pressure_from_velocity(velocity: list[ScalarField]) -> ScalarField:
    tensor = tensor_product(velocity)
    modes = set().union(*(field.keys() for row in tensor for field in row))
    pressure: ScalarField = {}
    for mode in modes:
        denominator = norm2(mode)
        if denominator == 0:
            continue
        coefficient: Poly = {}
        for i in range(3):
            for j in range(3):
                coefficient = padd(
                    coefficient,
                    pscale(component(tensor[i][j], mode), z(F(-mode[i] * mode[j], denominator))),
                )
        if coefficient:
            pressure[mode] = coefficient
    return pressure


def strain(velocity: list[ScalarField]) -> list[list[ScalarField]]:
    return [[
        fscale(fadd(derivative(velocity[j], i), derivative(velocity[i], j)), z(F(1, 2)))
        for j in range(3)
    ] for i in range(3)]


def nonlinear_n(velocity: list[ScalarField]) -> list[ScalarField]:
    tensor = tensor_product(velocity)
    pressure = pressure_from_velocity(velocity)
    output: list[ScalarField] = []
    for i in range(3):
        row: ScalarField = {}
        for k in range(3):
            row = fadd(row, derivative(tensor[i][k], k))
        row = fadd(row, derivative(pressure, i))
        output.append(row)
    return output


def tau2(a: ScalarField, b: ScalarField) -> ScalarField:
    return fadd(heat(fmul(a, b)), fneg(fmul(heat(a), heat(b))))


def tau3(a: ScalarField, b: ScalarField, c: ScalarField) -> ScalarField:
    result = heat(fmul(fmul(a, b), c))
    result = fadd(result, fneg(fmul(heat(a), heat(fmul(b, c)))))
    result = fadd(result, fneg(fmul(heat(b), heat(fmul(a, c)))))
    result = fadd(result, fneg(fmul(heat(c), heat(fmul(a, b)))))
    result = fadd(result, fscale(fmul(fmul(heat(a), heat(b)), heat(c)), z(2)))
    return result


def kappa_bundle(velocity: list[ScalarField]) -> list[list[list[ScalarField]]]:
    return [[[
        tau3(velocity[i], velocity[j], velocity[k])
        for k in range(3)
    ] for j in range(3)] for i in range(3)]


def q_bundle(velocity: list[ScalarField], pressure: ScalarField) -> list[ScalarField]:
    return [tau2(pressure, velocity[i]) for i in range(3)]


def r_bundle(velocity: list[ScalarField], pressure: ScalarField) -> list[list[ScalarField]]:
    s = strain(velocity)
    return [[tau2(pressure, s[i][j]) for j in range(3)] for i in range(3)]


def matrix_zero() -> list[list[Poly]]:
    return [[{} for _ in range(3)] for _ in range(3)]


def matrix_add(a: list[list[Poly]], b: list[list[Poly]]) -> list[list[Poly]]:
    return [[padd(a[i][j], b[i][j]) for j in range(3)] for i in range(3)]


def matrix_neg(a: list[list[Poly]]) -> list[list[Poly]]:
    return [[pneg(a[i][j]) for j in range(3)] for i in range(3)]


def matrix_scale(a: list[list[Poly]], scalar: Gaussian) -> list[list[Poly]]:
    return [[pscale(a[i][j], scalar) for j in range(3)] for i in range(3)]


def matrix_at(fields: list[list[ScalarField]], mode: Mode) -> list[list[Poly]]:
    return [[component(fields[i][j], mode) for j in range(3)] for i in range(3)]


def contracted_kappa_flux(kappa: list[list[list[ScalarField]]], mode: Mode) -> list[list[Poly]]:
    result = matrix_zero()
    for i in range(3):
        for j in range(3):
            value: Poly = {}
            for k in range(3):
                value = padd(value, pscale(component(kappa[i][j][k], mode), z(0, -mode[k])))
            result[i][j] = value
    return result


def pressure_diffusion(q_fields: list[ScalarField], mode: Mode) -> list[list[Poly]]:
    result = matrix_zero()
    for i in range(3):
        for j in range(3):
            left = pscale(component(q_fields[j], mode), z(0, -mode[i]))
            right = pscale(component(q_fields[i], mode), z(0, -mode[j]))
            result[i][j] = padd(left, right)
    return result


def matrix_poly_json(matrix: list[list[Poly]]) -> list[list[dict[str, object]]]:
    return [[poly_json(matrix[i][j]) for j in range(3)] for i in range(3)]


def sparse_field_json(field: ScalarField) -> dict[str, dict[str, object]]:
    return {mode_key(mode): poly_json(poly) for mode, poly in sorted(fclean(field).items())}


def sparse_tensor3_json(bundle: list[list[list[ScalarField]]]) -> dict[str, object]:
    output: dict[str, object] = {}
    for i in range(3):
        for j in range(3):
            for k in range(3):
                field = fclean(bundle[i][j][k])
                if field:
                    output[f"{i + 1}{j + 1}{k + 1}"] = sparse_field_json(field)
    return output


def sparse_vector_json(bundle: list[ScalarField]) -> dict[str, object]:
    return {str(i + 1): sparse_field_json(field) for i, field in enumerate(bundle) if fclean(field)}


def sparse_matrix_json(bundle: list[list[ScalarField]], scale: int = 1) -> dict[str, object]:
    output: dict[str, object] = {}
    for i in range(3):
        for j in range(3):
            field = fscale(bundle[i][j], z(scale))
            if fclean(field):
                output[f"{i + 1}{j + 1}"] = sparse_field_json(field)
    return output


def digest_object(value: object) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def expected_matrix(factor: Poly, constants: list[list[int]]) -> list[list[Poly]]:
    return [[pscale(factor, z(constants[i][j])) for j in range(3)] for i in range(3)]


def matrix_equal(a: list[list[Poly]], b: list[list[Poly]]) -> bool:
    return all(pclean(a[i][j]) == pclean(b[i][j]) for i in range(3) for j in range(3))


def matrix_eval_json(matrix: list[list[Poly]], q_value: Fraction) -> list[list[str]]:
    return [[gexpr(peval(matrix[i][j], q_value)) for j in range(3)] for i in range(3)]


def compressed_lift(velocity: list[ScalarField], mode: Mode) -> dict[str, list[list[Poly]]]:
    n_field = nonlinear_n(velocity)
    ccal_fields = [[heat(fadd(fmul(velocity[i], n_field[j]), fmul(n_field[i], velocity[j])))
                    for j in range(3)] for i in range(3)]
    v = [heat(field) for field in velocity]
    ns = [heat(field) for field in n_field]
    resolved_fields = [[fadd(fmul(v[i], ns[j]), fmul(ns[i], v[j]))
                        for j in range(3)] for i in range(3)]
    ccal = matrix_at(ccal_fields, mode)
    resolved = matrix_at(resolved_fields, mode)
    chi = matrix_add(ccal, matrix_neg(resolved))
    return {"Ccal": ccal, "chi": chi, "resolved": resolved}


def zero_mode_xi_groups(pressure: ScalarField, velocity: list[ScalarField]) -> dict[int, list[list[Poly]]]:
    s = strain(velocity)
    groups: dict[int, list[list[Poly]]] = {}
    for mode in pressure:
        opposite = neg_mode(mode)
        m = norm2(mode)
        if m == 0:
            continue
        if not any(component(s[i][j], opposite) for i in range(3) for j in range(3)):
            continue
        if m not in groups:
            groups[m] = matrix_zero()
        # 2 * p(mode) S(-mode) * (1-q^(2m)).
        weight = {0: z(1), 2 * m: z(-1)}
        for i in range(3):
            for j in range(3):
                product = pmul(component(pressure, mode), component(s[i][j], opposite))
                groups[m][i][j] = padd(
                    groups[m][i][j],
                    pscale(pmul(product, weight), z(2)),
                )
    return groups


def quartic_kappa_tangent(velocity: list[ScalarField]) -> ScalarField:
    n_field = nonlinear_n(velocity)
    # Inviscid Navier--Stokes direction is du/dt=-N.  Differentiate
    # kappa_112=τ3(u1,u1,u2) by trilinearity.
    result: ScalarField = {}
    for term in (
        tau3(n_field[0], velocity[0], velocity[1]),
        tau3(velocity[0], n_field[0], velocity[1]),
        tau3(velocity[0], velocity[0], n_field[1]),
    ):
        result = fadd(result, fneg(term))
    return result


def epsilon_extract_at_half(velocity: list[ScalarField], mode: Mode) -> dict[str, object]:
    n_field = nonlinear_n(velocity)

    def value(epsilon: int) -> Gaussian:
        perturbed = [
            fadd(velocity[index], fscale(n_field[index], z(-epsilon)))
            for index in range(3)
        ]
        kappa_112 = tau3(perturbed[0], perturbed[0], perturbed[1])
        return peval(component(kappa_112, mode), F(1, 2))

    samples = {epsilon: value(epsilon) for epsilon in (0, 1, 2, 3)}
    # Exact derivative at epsilon=0 of a polynomial of degree at most three.
    extracted = ZERO
    for epsilon, weight in ((0, F(-11, 6)), (1, F(3)), (2, F(-3, 2)), (3, F(1, 3))):
        extracted = gadd(extracted, gscale(samples[epsilon], weight))
    return {
        "extractedLinearCoefficient": gexpr(extracted),
        "formula": "(-11*f(0)+18*f(1)-9*f(2)+2*f(3))/6",
        "q": "1/2",
        "samples": {str(epsilon): gexpr(samples[epsilon]) for epsilon in samples},
    }


def build_core() -> dict[str, object]:
    four = four_site_velocity()
    four_pressure = pressure_from_velocity(four)
    four_kappa = kappa_bundle(four)
    four_q = q_bundle(four, four_pressure)
    four_r = r_bundle(four, four_pressure)
    four_xi = [[fscale(four_r[i][j], z(2)) for j in range(3)] for i in range(3)]

    local_flux = contracted_kappa_flux(four_kappa, TARGET)
    pressure_row = pressure_diffusion(four_q, TARGET)
    xi_target = matrix_scale(matrix_at(four_r, TARGET), z(2))
    signed_source = matrix_add(matrix_add(local_flux, pressure_row), xi_target)

    kappa_factor = pmul({3: z(1)}, pmul(pmul({0: z(1), 2: z(-1)}, {0: z(1), 2: z(-1)}), {0: z(2), 2: z(1)}))
    first_order_factor = pmul({3: z(1)}, {0: z(1), 2: z(-1)})
    expected_local = expected_matrix(kappa_factor, [[2, -3, 0], [-3, 4, 0], [0, 0, 0]])
    expected_pressure = expected_matrix(first_order_factor, [[4, 2, 0], [2, -8, 0], [0, 0, 0]])
    expected_xi = expected_matrix(first_order_factor, [[-4, 0, 0], [0, 4, 0], [0, 0, 0]])
    require(matrix_equal(local_flux, expected_local), "four-site target kappa flux drift")
    require(matrix_equal(pressure_row, expected_pressure), "four-site target pressure diffusion drift")
    require(matrix_equal(xi_target, expected_xi), "four-site target Xi drift")

    compressed = compressed_lift(four, TARGET)
    k_matrix = [[-2, 1, 0], [1, 0, 0], [0, 0, 0]]
    expected_ccal = expected_matrix({5: z(-1)}, k_matrix)
    expected_resolved = expected_matrix({3: z(-1)}, k_matrix)
    expected_chi = expected_matrix({3: z(1), 5: z(-1)}, k_matrix)
    require(matrix_equal(compressed["Ccal"], expected_ccal), "compressed Ccal target drift")
    require(matrix_equal(compressed["resolved"], expected_resolved), "compressed resolved target drift")
    require(matrix_equal(compressed["chi"], expected_chi), "compressed chi target drift")

    kappa_table = sparse_tensor3_json(four_kappa)
    q_table = sparse_vector_json(four_q)
    xi_table = sparse_matrix_json(four_r, scale=2)

    six = six_site_velocity()
    six_pressure = pressure_from_velocity(six)
    six_kappa = kappa_bundle(six)
    six_q = q_bundle(six, six_pressure)
    six_r = r_bundle(six, six_pressure)
    zero: Mode = (0, 0, 0)
    six_local = contracted_kappa_flux(six_kappa, zero)
    six_pressure_diffusion = pressure_diffusion(six_q, zero)
    six_xi = matrix_scale(matrix_at(six_r, zero), z(2))
    six_xi_expected = expected_matrix({0: z(1), 4: z(-1)}, [[-48, 0, 0], [0, 48, 0], [0, 0, 0]])
    require(matrix_equal(six_local, matrix_zero()), "six-site zero-mode kappa contraction must vanish")
    require(matrix_equal(six_pressure_diffusion, matrix_zero()), "six-site zero-mode Q divergence must vanish")
    require(matrix_equal(six_xi, six_xi_expected), "six-site zero-mode Xi drift")
    xi_groups = zero_mode_xi_groups(six_pressure, six)
    require(set(xi_groups) == {1, 2}, "six-site pressure-strain norm groups drift")
    require(matrix_equal(xi_groups[1], matrix_zero()), "six-site |m|^2=1 Xi group must cancel")
    require(matrix_equal(xi_groups[2], six_xi_expected), "six-site |m|^2=2 Xi group drift")

    quartic_field = quartic_kappa_tangent(four)
    quartic_poly = component(quartic_field, QUARTIC_TARGET)
    quartic_expected = {2: z(0, 2), 4: z(0, -4), 6: z(0, 2)}
    require(quartic_poly == quartic_expected, "quartic selected coefficient drift")
    epsilon = epsilon_extract_at_half(four, QUARTIC_TARGET)
    require(epsilon["extractedLinearCoefficient"] == "9/32*i", "finite-epsilon extraction drift")

    complete_tables = {"Q": q_table, "XiEquals2R": xi_table, "kappa": kappa_table}
    common_core = {
        "compressedTarget": {
            "Ccal": matrix_poly_json(compressed["Ccal"]),
            "chi": matrix_poly_json(compressed["chi"]),
            "resolved": matrix_poly_json(compressed["resolved"]),
            "signPairDifference": matrix_poly_json(matrix_scale(compressed["chi"], z(2))),
        },
        "fourSiteTarget": {
            "localKappaFlux": matrix_poly_json(local_flux),
            "pressureDiffusion": matrix_poly_json(pressure_row),
            "pressureStrainXi": matrix_poly_json(xi_target),
            "signedStressSource": matrix_poly_json(signed_source),
        },
        "quarticSelected": {
            "coefficient": poly_json(quartic_poly),
            "finiteEpsilonAtQHalf": epsilon,
            "index": "kappa112",
            "mode": list(QUARTIC_TARGET),
        },
        "sixSiteZeroMode": {
            "contractedKappaFlux": matrix_poly_json(six_local),
            "pressureDiffusion": matrix_poly_json(six_pressure_diffusion),
            "pressureStrainXi": matrix_poly_json(six_xi),
            "pressureStrainXiByInputNormSquared": {
                str(m): matrix_poly_json(matrix) for m, matrix in sorted(xi_groups.items())
            },
        },
        "tableDigest": digest_object(complete_tables),
    }

    return {
        "arithmetic": "fractions.Fraction Gaussian rationals and finite q-polynomials; no floating point",
        "commonCore": common_core,
        "compressedLift": {
            "definition": "chi=P_s(u odot N)-v_s odot N_s",
            "distinctFrom": "Germano signedStressSource",
            "dilationAtSThetaOverLSquaredFrobeniusSignDifference": "2*sqrt(6)*L*(exp(-3*theta)-exp(-5*theta))",
            "targetMode": list(TARGET),
        },
        "dilation": {
            "germanoRows": "replace q by exp(-s*L^2) and multiply contracted rows by L",
            "quarticSelected": "2*i*L*q^2*(1-q^2)^2 at mode L*(0,2,0)",
            "support": "u_L(x)=u(L*x)",
        },
        "fourSite": {
            "completeTables": complete_tables,
            "field": {
                "coefficients": field_coefficients_json(four),
                "divergenceFree": field_divergence(four),
                "meanZero": all((0, 0, 0) not in component_field for component_field in four),
                "physical": ["2*sin(x+y)", "2*sin(x)-2*sin(x+y)", "0"],
                "realConjugacy": field_reality(four),
                "siteCount": len(set().union(*(field.keys() for field in four))),
            },
            "target": common_core["fourSiteTarget"],
        },
        "parity": {
            "CcalOdd": True,
            "QOdd": True,
            "XiOdd": True,
            "chiOdd": True,
            "kappaOdd": True,
            "quarticKappaTangentEven": True,
            "signPairDifferenceOfOddRows": "2*value_for_u",
        },
        "quartic": common_core["quarticSelected"],
        "scope": {
            "arbitraryThreeDimensionalGlobalRegularity": "OPEN",
            "cAloneInformationTheoreticallyInsufficient": "OPEN",
            "clayConclusion": "OPEN",
            "coefficientwiseNonRecoveryOnly": True,
            "genericPdeIntegration": False,
            "notClay": True,
            "ordinaryTranslationPath": "LOCAL_DIRECT_NO_DGX",
        },
        "sixSite": {
            "field": {
                "coefficients": field_coefficients_json(six),
                "divergenceFree": field_divergence(six),
                "meanZero": all((0, 0, 0) not in component_field for component_field in six),
                "physical": ["6*sin(y)-4*sin(x+y)", "4*sin(x)+4*sin(x+y)", "0"],
                "realConjugacy": field_reality(six),
                "siteCount": len(set().union(*(field.keys() for field in six))),
            },
            "zeroMode": common_core["sixSiteZeroMode"],
        },
    }


def resolve_path(document: dict[str, Any], path: str) -> object:
    current: object = document
    for segment in path.split("."):
        if isinstance(current, dict):
            require(segment in current, "missing check path: " + path)
            current = current[segment]
        elif isinstance(current, list):
            require(segment.isdigit(), "list path segment is not numeric: " + path)
            index = int(segment)
            require(0 <= index < len(current), "list path index out of range: " + path)
            current = current[index]
        else:
            raise RuntimeError("check path enters scalar: " + path)
    return current


def build_results() -> dict[str, object]:
    checklist = load_json(CHECKLIST_PATH)
    contract = load_json(CONTRACT_PATH)
    require(checklist.get("schemaVersion") == 1, "audit checklist schema drift")
    require(contract.get("schemaVersion") == 1, "contract schema drift")
    core = build_core()
    result: dict[str, object] = {
        "certificate": "R0.73V exact signed-third-order heat-lift certificate",
        "claimBoundary": (
            "Exact finite Fourier q-polynomials, parity, dilation, one coefficientwise pressure witness, "
            "and one selected quartic tangent only; no information-theoretic minimality, PDE closure, "
            "generic integration, singularity, global regularity, or Clay conclusion."
        ),
        **core,
    }
    checks = checklist.get("requiredChecks")
    require(isinstance(checks, list) and checks, "audit checklist has no checks")
    identifiers: set[str] = set()
    rows: list[dict[str, object]] = []
    for specification in checks:
        require(isinstance(specification, dict), "invalid checklist row")
        check_id = specification.get("id")
        path = specification.get("path")
        expected = specification.get("expected")
        require(isinstance(check_id, str) and check_id, "invalid check id")
        require(check_id not in identifiers, "duplicate check id: " + check_id)
        identifiers.add(check_id)
        require(isinstance(path, str) and path, "invalid check path")
        actual = resolve_path(result, path)
        rows.append({"actual": actual, "expected": expected, "id": check_id, "pass": actual == expected, "path": path})
    require(all(row["pass"] is True for row in rows), "fixed audit checklist failed")
    result["audit"] = {
        "checklistPath": CHECKLIST_PATH.relative_to(ROOT).as_posix(),
        "checklistSha256": sha256(CHECKLIST_PATH),
        "contractPath": CONTRACT_PATH.relative_to(ROOT).as_posix(),
        "contractSha256": sha256(CONTRACT_PATH),
        "passed": len(rows),
        "required": len(rows),
        "results": rows,
    }
    result["producer"] = {
        "dgx": "not used",
        "floatingPoint": "not used",
        "gpu": "not used",
        "network": "not used",
        "scriptSha256": sha256(Path(__file__).resolve()),
        "standardLibraryOnly": True,
    }
    return result


def parse_arguments(arguments: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true")
    return parser.parse_args(arguments)


def main(arguments: Iterable[str] | None = None) -> int:
    options = parse_arguments(arguments)
    results = build_results()
    rendered = canonical(results)
    if options.check_only:
        require(RESULTS_PATH.is_file() and not RESULTS_PATH.is_symlink(), "missing regular results.json")
        require(RESULTS_PATH.read_text(encoding="utf-8") == rendered, "results.json is stale")
        mode = "check-only"
    else:
        RESULTS_PATH.write_text(rendered, encoding="utf-8")
        mode = "write"
    print(
        f"R073V_EXACT_CERTIFICATE=PASS mode={mode} "
        f"checks={results['audit']['passed']}/{results['audit']['required']} "
        f"tableDigest={results['commonCore']['tableDigest']}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print("R073V_EXACT_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
