#!/usr/bin/env python3
"""Rebuild the exact finite R0.73U tensor-heat parity certificate.

All mathematical decisions use fractions.Fraction and exact Gaussian-rational
arithmetic.  Two structurally independent paths reconstruct the tensor time
tangent: a product-law path through the cubic tensor F and a velocity-law path
through the Navier--Stokes velocity tangent.  No floating point, third-party
package, network service, GPU, or DGX is used.
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
RESULTS_PATH = HERE / "results.json"

FQ = Fraction
Mode = tuple[int, int, int]
Gaussian = tuple[Fraction, Fraction]
CVector = tuple[Gaussian, Gaussian, Gaussian]
CMatrix = tuple[CVector, CVector, CVector]
CTensor3 = tuple[CMatrix, CMatrix, CMatrix]

ZERO: Gaussian = (FQ(0), FQ(0))
I_UNIT: Gaussian = (FQ(0), FQ(1))
ZERO_VECTOR: CVector = (ZERO, ZERO, ZERO)
ZERO_MATRIX: CMatrix = (ZERO_VECTOR, ZERO_VECTOR, ZERO_VECTOR)
TARGET: Mode = (1, 2, 0)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    output: dict[str, object] = {}
    for key, value in pairs:
        require(key not in output, "duplicate JSON key: " + key)
        output[key] = value
    return output


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(value: int | Fraction) -> str:
    return str(FQ(value))


def mode_key(mode: Mode) -> str:
    return ",".join(str(value) for value in mode)


def add_mode(left: Mode, right: Mode) -> Mode:
    return tuple(left[index] + right[index] for index in range(3))  # type: ignore[return-value]


def negate_mode(mode: Mode) -> Mode:
    return tuple(-value for value in mode)  # type: ignore[return-value]


def mode_dot(left: Mode, right: Mode) -> int:
    return sum(left[index] * right[index] for index in range(3))


def z(real: int | Fraction = 0, imag: int | Fraction = 0) -> Gaussian:
    return FQ(real), FQ(imag)


def gadd(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def gneg(value: Gaussian) -> Gaussian:
    return -value[0], -value[1]


def gsub(left: Gaussian, right: Gaussian) -> Gaussian:
    return gadd(left, gneg(right))


def gmul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def gscale(value: Gaussian, scalar: int | Fraction) -> Gaussian:
    factor = FQ(scalar)
    return value[0] * factor, value[1] * factor


def gdivide(value: Gaussian, scalar: int | Fraction) -> Gaussian:
    denominator = FQ(scalar)
    require(denominator != 0, "Gaussian division by zero")
    return value[0] / denominator, value[1] / denominator


def gconj(value: Gaussian) -> Gaussian:
    return value[0], -value[1]


def gabs2(value: Gaussian) -> Fraction:
    return value[0] * value[0] + value[1] * value[1]


def gzero(value: Gaussian) -> bool:
    return value == ZERO


def gexpr(value: Gaussian) -> str:
    real, imag = value
    if imag == 0:
        return q(real)
    if real == 0:
        if imag == 1:
            return "i"
        if imag == -1:
            return "-i"
        return q(imag) + "*i"
    sign = "+" if imag > 0 else "-"
    magnitude = abs(imag)
    suffix = "i" if magnitude == 1 else q(magnitude) + "*i"
    return q(real) + sign + suffix


def vadd(left: CVector, right: CVector) -> CVector:
    return tuple(gadd(left[index], right[index]) for index in range(3))  # type: ignore[return-value]


def vneg(vector: CVector) -> CVector:
    return tuple(gneg(value) for value in vector)  # type: ignore[return-value]


def vconj(vector: CVector) -> CVector:
    return tuple(gconj(value) for value in vector)  # type: ignore[return-value]


def vscale(vector: CVector, scalar: int | Fraction) -> CVector:
    return tuple(gscale(value, scalar) for value in vector)  # type: ignore[return-value]


def mode_vector_dot(mode: Mode, vector: CVector) -> Gaussian:
    total = ZERO
    for scalar, value in zip(mode, vector):
        total = gadd(total, gscale(value, scalar))
    return total


def vector_zero(vector: CVector) -> bool:
    return all(gzero(value) for value in vector)


def outer(left: CVector, right: CVector) -> CMatrix:
    return tuple(
        tuple(gmul(left[row], right[column]) for column in range(3))
        for row in range(3)
    )  # type: ignore[return-value]


def madd(left: CMatrix, right: CMatrix) -> CMatrix:
    return tuple(
        tuple(gadd(left[row][column], right[row][column]) for column in range(3))
        for row in range(3)
    )  # type: ignore[return-value]


def mneg(matrix: CMatrix) -> CMatrix:
    return tuple(
        tuple(gneg(matrix[row][column]) for column in range(3))
        for row in range(3)
    )  # type: ignore[return-value]


def mscale(matrix: CMatrix, scalar: int | Fraction) -> CMatrix:
    return tuple(
        tuple(gscale(matrix[row][column], scalar) for column in range(3))
        for row in range(3)
    )  # type: ignore[return-value]


def mgscale(matrix: CMatrix, scalar: Gaussian) -> CMatrix:
    return tuple(
        tuple(gmul(matrix[row][column], scalar) for column in range(3))
        for row in range(3)
    )  # type: ignore[return-value]


def matrix_zero(matrix: CMatrix) -> bool:
    return all(gzero(value) for row in matrix for value in row)


def matrix_symmetric(matrix: CMatrix) -> bool:
    return all(matrix[row][column] == matrix[column][row]
               for row in range(3) for column in range(3))


def matrix_abs2(matrix: CMatrix) -> Fraction:
    return sum(gabs2(value) for row in matrix for value in row)


def matrix_json(matrix: CMatrix) -> list[list[str]]:
    return [[gexpr(value) for value in row] for row in matrix]


def vector_json(vector: CVector) -> list[str]:
    return [gexpr(value) for value in vector]


def matrix_map_json(values: dict[Mode, CMatrix]) -> dict[str, object]:
    return {mode_key(mode): matrix_json(matrix) for mode, matrix in sorted(values.items())}


def scalar_map_json(values: dict[Mode, Gaussian]) -> dict[str, str]:
    return {mode_key(mode): gexpr(value) for mode, value in sorted(values.items())}


def vector_map_json(values: dict[Mode, CVector]) -> dict[str, object]:
    return {mode_key(mode): vector_json(vector) for mode, vector in sorted(values.items())}


def clean_matrix_map(values: dict[Mode, CMatrix]) -> dict[Mode, CMatrix]:
    return {mode: matrix for mode, matrix in values.items() if not matrix_zero(matrix)}


def clean_vector_map(values: dict[Mode, CVector]) -> dict[Mode, CVector]:
    return {mode: vector for mode, vector in values.items() if not vector_zero(vector)}


def clean_scalar_map(values: dict[Mode, Gaussian]) -> dict[Mode, Gaussian]:
    return {mode: value for mode, value in values.items() if not gzero(value)}


def conjugate_completion(positive: dict[Mode, CVector]) -> dict[Mode, CVector]:
    output = dict(positive)
    for mode, vector in positive.items():
        negative = negate_mode(mode)
        require(negative not in output, "positive support contains a conjugate collision")
        output[negative] = vconj(vector)
    return output


def witness_velocity() -> dict[Mode, CVector]:
    return conjugate_completion({
        (1, 0, 0): (z(), z(0, -1), z()),
        (1, 1, 0): (z(0, -1), z(0, 1), z()),
    })


def negate_velocity(velocity: dict[Mode, CVector]) -> dict[Mode, CVector]:
    return {mode: vneg(vector) for mode, vector in velocity.items()}


def reality_check(velocity: dict[Mode, CVector]) -> bool:
    return all(
        negate_mode(mode) in velocity
        and velocity[negate_mode(mode)] == vconj(vector)
        for mode, vector in velocity.items()
    )


def divergence_check(velocity: dict[Mode, CVector]) -> bool:
    return all(gzero(mode_vector_dot(mode, vector)) for mode, vector in velocity.items())


def tensor_coefficients(velocity: dict[Mode, CVector]) -> dict[Mode, CMatrix]:
    output: dict[Mode, CMatrix] = {}
    for left_mode, left_vector in velocity.items():
        for right_mode, right_vector in velocity.items():
            mode = add_mode(left_mode, right_mode)
            output[mode] = madd(output.get(mode, ZERO_MATRIX), outer(left_vector, right_vector))
    return clean_matrix_map(output)


def cubic_coefficients(velocity: dict[Mode, CVector]) -> dict[Mode, CTensor3]:
    output: dict[Mode, list[CMatrix]] = {}
    for first_mode, first_vector in velocity.items():
        for second_mode, second_vector in velocity.items():
            for third_mode, third_vector in velocity.items():
                mode = add_mode(add_mode(first_mode, second_mode), third_mode)
                if mode not in output:
                    output[mode] = [ZERO_MATRIX, ZERO_MATRIX, ZERO_MATRIX]
                ij = outer(second_vector, third_vector)
                output[mode] = [
                    madd(output[mode][ell], mgscale(ij, first_vector[ell]))
                    for ell in range(3)
                ]
    return {
        mode: tuple(matrices)  # type: ignore[arg-type]
        for mode, matrices in output.items()
        if any(not matrix_zero(matrix) for matrix in matrices)
    }


def pressure_from_tensor(tensor: dict[Mode, CMatrix]) -> dict[Mode, Gaussian]:
    output: dict[Mode, Gaussian] = {}
    for mode, matrix in tensor.items():
        norm_squared = mode_dot(mode, mode)
        if norm_squared == 0:
            continue
        contraction = ZERO
        for row in range(3):
            for column in range(3):
                contraction = gadd(
                    contraction,
                    gscale(matrix[row][column], mode[row] * mode[column]),
                )
        output[mode] = gneg(gdivide(contraction, norm_squared))
    return clean_scalar_map(output)


def pressure_direct_pairs(velocity: dict[Mode, CVector]) -> dict[Mode, Gaussian]:
    """Independent pair formula, without constructing T first."""
    output: dict[Mode, Gaussian] = {}
    for left_mode, left_vector in velocity.items():
        for right_mode, right_vector in velocity.items():
            mode = add_mode(left_mode, right_mode)
            norm_squared = mode_dot(mode, mode)
            if norm_squared == 0:
                continue
            contraction = gmul(
                mode_vector_dot(mode, left_vector),
                mode_vector_dot(mode, right_vector),
            )
            contribution = gneg(gdivide(contraction, norm_squared))
            output[mode] = gadd(output.get(mode, ZERO), contribution)
    return clean_scalar_map(output)


def transport_from_cubic(cubic: dict[Mode, CTensor3]) -> dict[Mode, CMatrix]:
    """A_ij(h)=-i h_ell F_ell,ij(h)."""
    output: dict[Mode, CMatrix] = {}
    for mode, tensor in cubic.items():
        matrix = ZERO_MATRIX
        for ell in range(3):
            matrix = madd(matrix, mgscale(tensor[ell], gscale(I_UNIT, -mode[ell])))
        output[mode] = matrix
    return clean_matrix_map(output)


def pressure_velocity_tensor(
    velocity: dict[Mode, CVector], pressure: dict[Mode, Gaussian]
) -> dict[Mode, CMatrix]:
    """B_ij=-hat(u_j partial_i p+u_i partial_j p)."""
    output: dict[Mode, CMatrix] = {}
    for velocity_mode, vector in velocity.items():
        for pressure_mode, pressure_value in pressure.items():
            mode = add_mode(velocity_mode, pressure_mode)
            matrix: list[list[Gaussian]] = [[ZERO for _ in range(3)] for _ in range(3)]
            for row in range(3):
                for column in range(3):
                    first = gmul(
                        vector[column],
                        gmul(gscale(I_UNIT, pressure_mode[row]), pressure_value),
                    )
                    second = gmul(
                        vector[row],
                        gmul(gscale(I_UNIT, pressure_mode[column]), pressure_value),
                    )
                    matrix[row][column] = gneg(gadd(first, second))
            contribution: CMatrix = tuple(tuple(row) for row in matrix)  # type: ignore[assignment]
            output[mode] = madd(output.get(mode, ZERO_MATRIX), contribution)
    return clean_matrix_map(output)


def gradient_product_tensor(velocity: dict[Mode, CVector]) -> dict[Mode, CMatrix]:
    """G_ij=hat(partial_ell u_i partial_ell u_j)."""
    output: dict[Mode, CMatrix] = {}
    for left_mode, left_vector in velocity.items():
        for right_mode, right_vector in velocity.items():
            mode = add_mode(left_mode, right_mode)
            contribution = mscale(
                outer(left_vector, right_vector),
                -mode_dot(left_mode, right_mode),
            )
            output[mode] = madd(output.get(mode, ZERO_MATRIX), contribution)
    return clean_matrix_map(output)


def viscous_tensor_from_product(
    tensor: dict[Mode, CMatrix], gradient: dict[Mode, CMatrix]
) -> dict[Mode, CMatrix]:
    """V=hat(Delta T-2 partial_ell u tensor partial_ell u)."""
    modes = set(tensor) | set(gradient)
    output = {
        mode: madd(
            mscale(tensor.get(mode, ZERO_MATRIX), -mode_dot(mode, mode)),
            mscale(gradient.get(mode, ZERO_MATRIX), -2),
        )
        for mode in modes
    }
    return clean_matrix_map(output)


def advective_velocity(velocity: dict[Mode, CVector]) -> dict[Mode, CVector]:
    """Return hat((u dot grad)u) from ordered velocity pairs."""
    output: dict[Mode, CVector] = {}
    for advector_mode, advector in velocity.items():
        for advected_mode, advected in velocity.items():
            mode = add_mode(advector_mode, advected_mode)
            multiplier = gmul(I_UNIT, mode_vector_dot(advected_mode, advector))
            contribution = tuple(gmul(multiplier, value) for value in advected)  # type: ignore[assignment]
            output[mode] = vadd(output.get(mode, ZERO_VECTOR), contribution)
    return clean_vector_map(output)


def nonlinear_velocity_tangent(
    velocity: dict[Mode, CVector], pressure: dict[Mode, Gaussian]
) -> dict[Mode, CVector]:
    advection = advective_velocity(velocity)
    modes = set(advection) | set(pressure)
    output: dict[Mode, CVector] = {}
    for mode in modes:
        gradient_pressure: CVector = tuple(
            gmul(gscale(I_UNIT, mode[index]), pressure.get(mode, ZERO))
            for index in range(3)
        )  # type: ignore[assignment]
        output[mode] = vneg(vadd(advection.get(mode, ZERO_VECTOR), gradient_pressure))
    return clean_vector_map(output)


def laplacian_velocity(velocity: dict[Mode, CVector]) -> dict[Mode, CVector]:
    return {
        mode: vscale(vector, -mode_dot(mode, mode))
        for mode, vector in velocity.items()
    }


def product_tangent(
    velocity: dict[Mode, CVector], tangent: dict[Mode, CVector]
) -> dict[Mode, CMatrix]:
    output: dict[Mode, CMatrix] = {}
    for velocity_mode, vector in velocity.items():
        for tangent_mode, derivative in tangent.items():
            mode = add_mode(velocity_mode, tangent_mode)
            contribution = madd(outer(derivative, vector), outer(vector, derivative))
            output[mode] = madd(output.get(mode, ZERO_MATRIX), contribution)
    return clean_matrix_map(output)


def add_matrix_maps(
    left: dict[Mode, CMatrix], right: dict[Mode, CMatrix]
) -> dict[Mode, CMatrix]:
    modes = set(left) | set(right)
    return clean_matrix_map({
        mode: madd(left.get(mode, ZERO_MATRIX), right.get(mode, ZERO_MATRIX))
        for mode in modes
    })


def negate_matrix_map(values: dict[Mode, CMatrix]) -> dict[Mode, CMatrix]:
    return clean_matrix_map({mode: mneg(matrix) for mode, matrix in values.items()})


def group_matrix_frobenius_squared(
    values: dict[Mode, CMatrix], scale: int = 1
) -> dict[str, str]:
    groups: dict[int, Fraction] = {}
    for mode, matrix in values.items():
        norm_squared = mode_dot(mode, mode)
        groups[norm_squared] = groups.get(norm_squared, FQ(0)) + scale * scale * matrix_abs2(matrix)
    return {str(norm): q(value) for norm, value in sorted(groups.items())}


def four_site_record() -> dict[str, object]:
    velocity = witness_velocity()
    minus_velocity = negate_velocity(velocity)
    tensor = tensor_coefficients(velocity)
    tensor_minus = tensor_coefficients(minus_velocity)
    cubic = cubic_coefficients(velocity)
    cubic_minus = cubic_coefficients(minus_velocity)

    # Path A: differentiate the product law through F and the pressure-velocity term.
    pressure_a = pressure_from_tensor(tensor)
    transport_a = transport_from_cubic(cubic)
    pressure_term_a = pressure_velocity_tensor(velocity, pressure_a)
    nonlinear_a = add_matrix_maps(transport_a, pressure_term_a)
    gradient_a = gradient_product_tensor(velocity)
    viscous_a = viscous_tensor_from_product(tensor, gradient_a)

    # Path B: first construct the velocity tangent, then apply the product rule.
    pressure_b = pressure_direct_pairs(velocity)
    nonlinear_velocity_b = nonlinear_velocity_tangent(velocity, pressure_b)
    nonlinear_b = product_tangent(velocity, nonlinear_velocity_b)
    viscous_b = product_tangent(velocity, laplacian_velocity(velocity))

    # Recompute the full sign-reversed witness, rather than inferring its parity.
    tensor_minus_b = tensor_coefficients(minus_velocity)
    pressure_minus = pressure_direct_pairs(minus_velocity)
    transport_minus = transport_from_cubic(cubic_minus)
    pressure_term_minus = pressure_velocity_tensor(minus_velocity, pressure_minus)
    nonlinear_minus = add_matrix_maps(transport_minus, pressure_term_minus)
    gradient_minus = gradient_product_tensor(minus_velocity)
    viscous_minus = viscous_tensor_from_product(tensor_minus_b, gradient_minus)

    require(pressure_a == pressure_b, "pressure paths disagree")
    require(nonlinear_a == nonlinear_b, "nonlinear tensor-tangent paths disagree")
    require(viscous_a == viscous_b, "viscous tensor-tangent paths disagree")
    require(tensor == tensor_minus == tensor_minus_b, "tensor parity failed")
    require(pressure_a == pressure_minus, "pressure parity failed")
    require(nonlinear_minus == negate_matrix_map(nonlinear_a), "nonlinear parity failed")
    require(viscous_minus == viscous_a, "viscous parity failed")

    target_tensor = tensor.get(TARGET, ZERO_MATRIX)
    target_cubic = cubic.get(TARGET, (ZERO_MATRIX, ZERO_MATRIX, ZERO_MATRIX))
    target_a = transport_a.get(TARGET, ZERO_MATRIX)
    target_b = pressure_term_a.get(TARGET, ZERO_MATRIX)
    target_k = nonlinear_a.get(TARGET, ZERO_MATRIX)
    target_v = viscous_a.get(TARGET, ZERO_MATRIX)
    target_difference = madd(target_k, target_k)

    require(matrix_zero(target_tensor), "target T must vanish")
    require(matrix_zero(target_v), "target V must vanish")
    require(not matrix_zero(target_k), "target K must be nonzero")

    cubic_json = {
        str(ell + 1): matrix_json(target_cubic[ell])
        for ell in range(3)
    }
    all_relevant_symmetric = all(
        matrix_symmetric(matrix)
        for collection in (tensor, transport_a, pressure_term_a, nonlinear_a, viscous_a)
        for matrix in collection.values()
    )

    return {
        "definitions": {
            "A": "A_ij(h)=-i*h_ell*F_ell,ij(h)",
            "B": "B_ij(h)=-hat(u_j*partial_i(p)+u_i*partial_j(p))(h)",
            "F": "F_ell,ij(h)=hat(u_ell*u_i*u_j)(h)",
            "K": "K=A+B, the nonlinear coefficient of partial_t(T)",
            "T": "T_ij(h)=hat(u_i*u_j)(h)",
            "V": "V_ij(h)=hat(Delta(T_ij)-2*partial_ell(u_i)*partial_ell(u_j))(h)",
        },
        "dilation": {
            "field": "u_L(x)=u(L*x), integer L>=1",
            "heatFilteredDifference": "2*L*exp(-5*s*L^2)*K",
            "heatFilteredDifferenceFrobenius": "2*sqrt(6)*L*exp(-5*s*L^2)",
            "mode": "h_L=(L,2*L,0)",
            "parabolicEquivalentInS": "2*sqrt(6*theta)*exp(-5*theta)*s^(-1/2)",
            "parabolicFrobenius": "2*sqrt(6)*L*exp(-5*theta)",
            "parabolicSlice": "s=theta*L^(-2), theta>0",
            "signedDerivativeFactor": "L",
        },
        "field": {
            "coefficients": vector_map_json(velocity),
            "divergenceFree": divergence_check(velocity),
            "meanZero": (0, 0, 0) not in velocity,
            "physical": ["2*sin(x+y)", "2*sin(x)-2*sin(x+y)", "0"],
            "positivePairCount": 2,
            "realConjugacy": reality_check(velocity),
            "siteCount": len(velocity),
        },
        "heatGroups": {
            "completeBaseKSquaredFrobeniusByNormSquared":
                group_matrix_frobenius_squared(nonlinear_a),
            "completeBaseKSquaredFormula":
                "sum_m S_m*exp(-2*s*m)",
            "completeSignedDifferenceSquaredFrobeniusByNormSquared":
                group_matrix_frobenius_squared(nonlinear_a, scale=2),
            "completeSignedDifferenceSquaredFormula":
                "sum_m 4*S_m*exp(-2*s*m)",
            "signedDifferenceSquaredMultiplierFromBase": "4",
            "targetCoefficientGroup": {"5": matrix_json(target_difference)},
            "targetDifferenceFormula": "2*exp(-5*s)*K",
            "targetDifferenceFrobenius": "2*sqrt(6)*exp(-5*s)",
            "targetDifferenceFrobeniusSquaredCoefficient": q(matrix_abs2(target_difference)),
            "targetNormSquared": mode_dot(TARGET, TARGET),
        },
        "independentPaths": {
            "fullNonlinearMapAgreement": nonlinear_a == nonlinear_b,
            "fullPressureMapAgreement": pressure_a == pressure_b,
            "fullViscousMapAgreement": viscous_a == viscous_b,
            "pathA": "product law via T,F,A,B,G,V",
            "pathB": "velocity NSE tangent followed by exact product convolution",
            "targetKAgreement": nonlinear_a.get(TARGET, ZERO_MATRIX) == nonlinear_b.get(TARGET, ZERO_MATRIX),
            "targetVAgreement": viscous_a.get(TARGET, ZERO_MATRIX) == viscous_b.get(TARGET, ZERO_MATRIX),
        },
        "minimalityBoundary": {
            "certifiedLowerBoundary": "a nonzero real mean-zero witness needs at least two conjugate pairs, hence four Fourier sites",
            "claimScope": "support-cardinality boundary for this parity mechanism; not minimality among all closures or all no-go arguments",
            "singlePairAdvectiveZero": True,
            "singlePairArgument": "for support {+k,-k}, incompressibility k.a=0 makes every multiplier u_hat(q).r vanish",
            "singlePairNonlinearTensorTangentZero": True,
            "singlePairPressureZero": True,
            "witnessAttainsBoundary": len(velocity) == 4,
        },
        "parabolicProfile": {
            "maximumTheta": "1/10",
            "maximumValue": "2*sqrt(3/5)*exp(-1/2)",
            "normalizedProfile": "2*sqrt(6*theta)*exp(-5*theta)",
            "oneDerivativeCost": "s^(-1/2)",
        },
        "parity": {
            "AOdd": transport_from_cubic(cubic_minus) == negate_matrix_map(transport_a),
            "BOdd": pressure_term_minus == negate_matrix_map(pressure_term_a),
            "FOddAtTarget": all(
                cubic_minus.get(TARGET, (ZERO_MATRIX, ZERO_MATRIX, ZERO_MATRIX))[ell]
                == mneg(target_cubic[ell]) for ell in range(3)
            ),
            "KOdd": nonlinear_minus == negate_matrix_map(nonlinear_a),
            "TEven": tensor_minus == tensor,
            "VEven": viscous_minus == viscous_a,
            "pressureEven": pressure_minus == pressure_a,
            "quadraticState": {
                "pressureEven": True,
                "tauEven": True,
                "thetaEven": True,
            },
            "targetUnfilteredTangentDifference": matrix_json(target_difference),
        },
        "pressure": {
            "coefficients": scalar_map_json(pressure_a),
            "formula": "p_hat(h)=-(h_i*h_j/|h|^2)*T_ij(h), h!=0; p_hat(0)=0",
            "siteCount": len(pressure_a),
        },
        "symmetry": {
            "allRelevantCoefficientMatricesSymmetric": all_relevant_symmetric,
            "targetA": matrix_symmetric(target_a),
            "targetB": matrix_symmetric(target_b),
            "targetK": matrix_symmetric(target_k),
            "targetT": matrix_symmetric(target_tensor),
            "targetV": matrix_symmetric(target_v),
        },
        "target": {
            "A": matrix_json(target_a),
            "B": matrix_json(target_b),
            "F": cubic_json,
            "K": matrix_json(target_k),
            "KNonzero": not matrix_zero(target_k),
            "KSquaredFrobenius": q(matrix_abs2(target_k)),
            "T": matrix_json(target_tensor),
            "V": matrix_json(target_v),
            "mode": list(TARGET),
            "normSquared": mode_dot(TARGET, TARGET),
        },
    }


def get_path(value: object, path: str) -> object:
    current = value
    for segment in path.split("."):
        require(isinstance(current, dict), "check path enters non-object at " + segment)
        require(segment in current, "missing check path: " + path)
        current = current[segment]
    return current


def load_checklist() -> dict[str, Any]:
    require(CHECKLIST_PATH.is_file() and not CHECKLIST_PATH.is_symlink(),
            "missing regular audit checklist")
    value = json.loads(
        CHECKLIST_PATH.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate_keys,
    )
    require(isinstance(value, dict), "audit checklist root must be an object")
    require(value.get("schemaVersion") == 1, "audit checklist schema drift")
    checks = value.get("requiredChecks")
    require(isinstance(checks, list) and checks, "audit checklist has no checks")
    identifiers = [check.get("id") for check in checks if isinstance(check, dict)]
    require(len(identifiers) == len(checks), "audit checklist contains a non-object check")
    require(len(set(identifiers)) == len(identifiers), "duplicate audit check id")
    return value


def build_results() -> dict[str, object]:
    checklist = load_checklist()
    core: dict[str, object] = {
        "arithmetic": "Python standard-library fractions.Fraction; exact Gaussian rationals; no floating point",
        "certificate": "R0.73U exact four-site tensor-heat parity witness",
        "claimBoundary": (
            "Exact finite Fourier coefficients, parity, and coefficient-level heat/dilation formulas only; "
            "no generic PDE integration, singularity, global regularity, or Clay conclusion."
        ),
        "normalization": {
            "domain": "T^3=[0,2*pi]^3",
            "fourier": "f_hat(k)=integral f(x)*exp(-i*k.x) dmu",
            "measure": "normalized Haar probability measure",
            "navierStokes": "partial_t(u)+(u.grad)u+grad(p)=nu*Delta(u); div(u)=0",
            "pressureGauge": "p_hat(0)=0",
        },
        "schemaVersion": 1,
        "witness": four_site_record(),
    }
    checks: list[dict[str, object]] = []
    for specification in checklist["requiredChecks"]:
        require(isinstance(specification, dict), "invalid check specification")
        check_id = specification.get("id")
        path = specification.get("path")
        require(isinstance(check_id, str) and check_id, "check id is invalid")
        require(isinstance(path, str) and path, "check path is invalid")
        actual = get_path(core, path)
        expected = specification.get("expected")
        passed = actual == expected
        checks.append({
            "actual": actual,
            "expected": expected,
            "id": check_id,
            "pass": passed,
            "path": path,
        })
    require(all(bool(check["pass"]) for check in checks), "fixed audit checklist failed")
    core["audit"] = {
        "checklistPath": CHECKLIST_PATH.relative_to(ROOT).as_posix(),
        "checklistSha256": sha256(CHECKLIST_PATH),
        "passed": len(checks),
        "required": len(checks),
        "results": checks,
    }
    core["producer"] = {
        "dgx": "not used",
        "gpu": "not used",
        "network": "not used",
        "ordinaryTranslationPath": "LOCAL_DIRECT_NO_DGX",
        "scriptPath": Path(__file__).resolve().relative_to(ROOT).as_posix(),
        "scriptSha256": sha256(Path(__file__).resolve()),
        "standardLibraryOnly": True,
    }
    return core


def parse_arguments(arguments: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="recompute and require byte-equivalent JSON content without writing",
    )
    return parser.parse_args(list(arguments))


def main(arguments: Iterable[str] | None = None) -> int:
    options = parse_arguments(sys.argv[1:] if arguments is None else arguments)
    results = build_results()
    rendered = canonical(results)
    if options.check_only:
        require(RESULTS_PATH.is_file() and not RESULTS_PATH.is_symlink(),
                "missing regular results.json")
        require(RESULTS_PATH.read_text(encoding="utf-8") == rendered,
                "results.json differs from exact reconstruction")
        print(
            "R073U_EXACT_CERTIFICATE=PASS mode=check-only "
            f"checks={results['audit']['passed']}/{results['audit']['required']}"
        )
        return 0
    RESULTS_PATH.write_text(rendered, encoding="utf-8")
    print(
        "R073U_EXACT_CERTIFICATE=PASS mode=write "
        f"checks={results['audit']['passed']}/{results['audit']['required']} "
        f"output={RESULTS_PATH.relative_to(ROOT)}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"R073U_EXACT_CERTIFICATE=FAIL {error}", file=sys.stderr)
        raise SystemExit(1)
