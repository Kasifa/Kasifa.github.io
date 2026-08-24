#!/usr/bin/env python3
"""Exact finite/symbolic audit for the R0.70U square-root obstruction.

The producer checks four narrowly scoped groups:

1. the Pythagorean three-mode geometry, divergence constraints, and exact
   Biot--Savart recovery;
2. the normalized Fourier resonance giving the nonzero signed coefficient;
3. the fixed-frame covariance factorization, physical covariance defect,
   and rank-two spectral invariants; and
4. the elementary exponent arithmetic behind the super-square-root no-go.

The arbitrary-cutoff overlap/existence lemma, uniform eigenprojector
perturbation, Lp asymptotics, and every Navier--Stokes continuation statement
are analytic arguments in the report.  They are not inferred from this
finite certificate.  Nothing here proves a PDE closure, singularity, global
regularity, or a solution of the Millennium problem.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
from typing import TypeAlias

import sympy as sp


Mode: TypeAlias = tuple[sp.Expr, sp.Expr, sp.Expr]
VectorField: TypeAlias = dict[Mode, sp.Matrix]
MatrixField: TypeAlias = dict[Mode, sp.Matrix]


def canonical(expression: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.expand(expression)))


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def scalar_payload(expression: sp.Expr) -> str:
    return str(canonical(expression))


def vector_payload(vector: sp.Matrix) -> list[str]:
    return [scalar_payload(entry) for entry in vector]


def matrix_payload(matrix: sp.Matrix) -> list[list[str]]:
    return [
        [scalar_payload(matrix[row, column]) for column in range(matrix.cols)]
        for row in range(matrix.rows)
    ]


def matrix_is_zero(matrix: sp.Matrix) -> bool:
    return all(canonical(entry) == 0 for entry in matrix)


def outer(first: sp.Matrix, second: sp.Matrix | None = None) -> sp.Matrix:
    if second is None:
        second = first
    return first * second.T


def normalize_mode(mode: tuple[sp.Expr | int, ...]) -> Mode:
    return tuple(canonical(sp.sympify(entry)) for entry in mode)  # type: ignore[return-value]


def add_modes(*modes: Mode) -> Mode:
    return normalize_mode(
        tuple(sum((mode[index] for mode in modes), sp.S.Zero) for index in range(3))
    )


def negative_mode(mode: Mode) -> Mode:
    return normalize_mode(tuple(-entry for entry in mode))


def is_zero_mode(mode: Mode) -> bool:
    return all(canonical(entry) == 0 for entry in mode)


def add_vector_atom(field: VectorField, mode: Mode, coefficient: sp.Matrix) -> None:
    key = normalize_mode(mode)
    if key in field:
        field[key] = (field[key] + coefficient).applyfunc(canonical)
    else:
        field[key] = coefficient.applyfunc(canonical)


def cosine_vector(mode: Mode, amplitude: sp.Matrix) -> VectorField:
    result: VectorField = {}
    add_vector_atom(result, mode, amplitude / 2)
    add_vector_atom(result, negative_mode(mode), amplitude / 2)
    return result


def sine_vector(mode: Mode, amplitude: sp.Matrix) -> VectorField:
    result: VectorField = {}
    add_vector_atom(result, mode, amplitude / (2 * sp.I))
    add_vector_atom(result, negative_mode(mode), -amplitude / (2 * sp.I))
    return result


def add_vector_fields(*fields: VectorField) -> VectorField:
    result: VectorField = {}
    for field in fields:
        for mode, coefficient in field.items():
            add_vector_atom(result, mode, coefficient)
    return result


def scale_vector_field(field: VectorField, scalar: sp.Expr) -> VectorField:
    return {
        mode: (scalar * coefficient).applyfunc(canonical)
        for mode, coefficient in field.items()
    }


def curl_coefficient(mode: Mode, coefficient: sp.Matrix) -> sp.Matrix:
    return (sp.I * sp.Matrix(mode).cross(coefficient)).applyfunc(canonical)


def divergence_coefficient(mode: Mode, coefficient: sp.Matrix) -> sp.Expr:
    return canonical(sp.I * (sp.Matrix(mode).dot(coefficient)))


def strain_field(velocity: VectorField) -> MatrixField:
    result: MatrixField = {}
    for mode, coefficient in velocity.items():
        wave = sp.Matrix(mode)
        gradient = sp.I * outer(wave, coefficient)
        result[mode] = ((gradient + gradient.T) / 2).applyfunc(canonical)
    return result


def add_matrix_atom(field: MatrixField, mode: Mode, coefficient: sp.Matrix) -> None:
    key = normalize_mode(mode)
    if key in field:
        field[key] = (field[key] + coefficient).applyfunc(canonical)
    else:
        field[key] = coefficient.applyfunc(canonical)


def add_matrix_fields(*fields: MatrixField) -> MatrixField:
    result: MatrixField = {}
    for field in fields:
        for mode, coefficient in field.items():
            add_matrix_atom(result, mode, coefficient)
    return result


def scale_matrix_field(field: MatrixField, scalar: sp.Expr) -> MatrixField:
    return {
        mode: (scalar * coefficient).applyfunc(canonical)
        for mode, coefficient in field.items()
    }


def normalized_average_vector_matrix_vector(
    left: VectorField,
    matrix: MatrixField,
    right: VectorField,
) -> sp.Expr:
    total = sp.S.Zero
    for (left_mode, left_value), (matrix_mode, matrix_value), (
        right_mode,
        right_value,
    ) in itertools.product(left.items(), matrix.items(), right.items()):
        if is_zero_mode(add_modes(left_mode, matrix_mode, right_mode)):
            total += (left_value.T * matrix_value * right_value)[0]
    return canonical(total)


# ---------------------------------------------------------------------------
# 1. Pythagorean triad and exact Fourier/Biot--Savart fields.
# ---------------------------------------------------------------------------

m = sp.symbols("m", integer=True, positive=True)
A, delta = sp.symbols("A delta", positive=True, real=True)
epsilon, gamma = sp.symbols("epsilon gamma", real=True)

a = m**2 - 1
b = 2 * m
K = m**2 + 1

k = normalize_mode((a, b, 0))
p = normalize_mode((a, -b, 0))
q = normalize_mode((2 * a, 0, 0))

e1 = sp.Matrix([1, 0, 0])
e2 = sp.Matrix([0, 1, 0])
e3 = sp.Matrix([0, 0, 1])
n = sp.Matrix([-b / K, a / K, 0])
t = sp.Matrix([b / K, a / K, 0])

w1 = add_vector_fields(
    cosine_vector(k, A * n),
    sine_vector(k, A * e3),
)
w2 = cosine_vector(p, delta * e3)
w = add_vector_fields(w1, w2)
h = cosine_vector(q, e2)

u1 = scale_vector_field(w1, -1 / K)
u2 = sine_vector(p, delta * sp.Matrix([b, a, 0]) / K**2)
u_w = add_vector_fields(u1, u2)
u_h = sine_vector(q, -e3 / (2 * a))

require(canonical(a**2 + b**2 - K**2) == 0, "Pythagorean identity")
require(add_modes(k, p) == q, "triad resonance q=k+p")
require(canonical(n.dot(n) - 1) == 0, "n unit")
require(canonical(sp.Matrix(k).dot(n)) == 0, "n transverse to k")

for label, field in (("w", w), ("h", h), ("u_w", u_w), ("u_h", u_h)):
    for mode, coefficient in field.items():
        require(divergence_coefficient(mode, coefficient) == 0, f"divergence {label}")

for mode in w:
    require(
        matrix_is_zero(curl_coefficient(mode, u_w[mode]) - w[mode]),
        "curl u_w=w",
    )

for mode in h:
    require(
        matrix_is_zero(curl_coefficient(mode, u_h[mode]) - h[mode]),
        "curl u_h=h",
    )

for mode, coefficient in w1.items():
    require(
        matrix_is_zero(curl_coefficient(mode, coefficient) + K * coefficient),
        "curl w1=-K w1",
    )


# ---------------------------------------------------------------------------
# 2. Exact normalized Fourier resonance and signed first variation.
# ---------------------------------------------------------------------------

S_w = strain_field(u_w)
S_h = strain_field(u_h)

I = normalized_average_vector_matrix_vector(h, S_w, w)
J = normalized_average_vector_matrix_vector(w, S_h, w)
I_expected = -A * delta * a**2 * b / (2 * K**3)
J_expected = A * delta * b / (4 * K)

require(canonical(I - I_expected) == 0, "nonzero resonant I coefficient")
require(canonical(J - J_expected) == 0, "auxiliary J coefficient")

physical_stretching_derivative = canonical(2 * I + J)
frame_covariance_derivative = canonical(2 * gamma * I + J)
commutator_derivative = canonical(
    physical_stretching_derivative - frame_covariance_derivative
)
commutator_expected = canonical(-(1 - gamma) * A * delta * a**2 * b / K**3)

require(
    canonical(commutator_derivative - commutator_expected) == 0,
    "signed commutator first variation",
)

omega_epsilon_field = add_vector_fields(w, scale_vector_field(h, epsilon))
S_epsilon_field = add_matrix_fields(S_w, scale_matrix_field(S_h, epsilon))
physical_stretching_polynomial = normalized_average_vector_matrix_vector(
    omega_epsilon_field,
    S_epsilon_field,
    omega_epsilon_field,
)
frame_covariance_polynomial = canonical(
    normalized_average_vector_matrix_vector(w, S_epsilon_field, w)
    + epsilon
    * gamma
    * (
        normalized_average_vector_matrix_vector(w, S_epsilon_field, h)
        + normalized_average_vector_matrix_vector(h, S_epsilon_field, w)
    )
    + epsilon**2
    * normalized_average_vector_matrix_vector(h, S_epsilon_field, h)
)
commutator_polynomial = canonical(
    physical_stretching_polynomial - frame_covariance_polynomial
)

require(
    canonical(
        physical_stretching_polynomial
        - epsilon * physical_stretching_derivative
    )
    == 0,
    "physical stretching is exactly linear in epsilon",
)
require(
    canonical(
        frame_covariance_polynomial
        - epsilon * frame_covariance_derivative
    )
    == 0,
    "frame covariance contraction is exactly linear in epsilon",
)
require(
    canonical(commutator_polynomial - epsilon * commutator_expected) == 0,
    "commutator is exactly linear in epsilon",
)

m3_substitution = {m: 3, A: 2, delta: 1}
m3_I = canonical(I.subs(m3_substitution))
m3_J = canonical(J.subs(m3_substitution))
m3_physical_derivative = canonical(
    physical_stretching_derivative.subs(m3_substitution)
)
m3_commutator_derivative = canonical(
    commutator_derivative.subs(m3_substitution)
)
require(m3_I == -sp.Rational(48, 125), "m=3 I anchor")
require(m3_J == sp.Rational(3, 10), "m=3 J anchor")
require(
    m3_physical_derivative == -sp.Rational(117, 250),
    "m=3 physical stretching anchor",
)
require(
    canonical(m3_commutator_derivative + sp.Rational(96, 125) * (1 - gamma))
    == 0,
    "m=3 commutator anchor",
)


# ---------------------------------------------------------------------------
# 3. Fixed-frame covariance, tensor defect, and spectral invariants.
# ---------------------------------------------------------------------------

w0, w1s, w2s, h0, h1, h2 = sp.symbols(
    "w0 w1 w2 h0 h1 h2", real=True
)
w_symbol = sp.Matrix([w0, w1s, w2s])
h_symbol = sp.Matrix([h0, h1, h2])
kappa = 1 - gamma**2

Q_frame = (
    outer(w_symbol)
    + epsilon * gamma * (outer(w_symbol, h_symbol) + outer(h_symbol, w_symbol))
    + epsilon**2 * outer(h_symbol)
)
z_symbol = w_symbol + epsilon * gamma * h_symbol
Q_factor = outer(z_symbol) + kappa * epsilon**2 * outer(h_symbol)
omega_symbol = w_symbol + epsilon * h_symbol
physical_covariance = outer(omega_symbol)
tensor_defect = physical_covariance - Q_frame
tensor_defect_expected = epsilon * (1 - gamma) * (
    outer(w_symbol, h_symbol) + outer(h_symbol, w_symbol)
)

require(matrix_is_zero(Q_frame - Q_factor), "exact covariance factorization")
require(
    matrix_is_zero(tensor_defect - tensor_defect_expected),
    "exact physical covariance defect",
)
require(canonical(Q_frame.det()) == 0, "rank at most two")

W2_matrix = canonical(w_symbol.dot(w_symbol))
C_matrix = canonical(w_symbol.dot(h_symbol))
H2_matrix = canonical(h_symbol.dot(h_symbol))
trace_from_matrix = canonical(sp.trace(Q_frame))
trace_expected_from_vectors = canonical(
    W2_matrix + 2 * epsilon * gamma * C_matrix + epsilon**2 * H2_matrix
)
sigma_two_from_matrix = canonical(
    (sp.trace(Q_frame) ** 2 - sp.trace(Q_frame * Q_frame)) / 2
)
sigma_two_expected_from_vectors = canonical(
    kappa * epsilon**2 * (W2_matrix * H2_matrix - C_matrix**2)
)

require(
    canonical(trace_from_matrix - trace_expected_from_vectors) == 0,
    "trace derived from covariance matrix",
)
require(
    canonical(sigma_two_from_matrix - sigma_two_expected_from_vectors) == 0,
    "second spectral invariant derived from covariance matrix",
)

W2, H2 = sp.symbols("W2 H2", positive=True, real=True)
C = sp.symbols("C", real=True)
trace_invariant = W2 + 2 * epsilon * gamma * C + epsilon**2 * H2
product_invariant = kappa * epsilon**2 * (W2 * H2 - C**2)
lambda_two = (
    trace_invariant
    - sp.sqrt(trace_invariant**2 - 4 * product_invariant)
) / 2
lambda_two_leading = canonical(sp.limit(lambda_two / epsilon**2, epsilon, 0))
lambda_two_expected = canonical(kappa * (H2 - C**2 / W2))

require(
    canonical(lambda_two_leading - lambda_two_expected) == 0,
    "quadratic residual coefficient",
)

w_origin = sp.Matrix([-A * b / K, A * a / K, delta])
h_origin = e2
origin_cross_square = canonical(w_origin.cross(h_origin).dot(w_origin.cross(h_origin)))
origin_cross_expected = canonical(delta**2 + A**2 * b**2 / K**2)
require(
    canonical(origin_cross_square - origin_cross_expected) == 0,
    "positive origin transverse coefficient",
)

x, y = sp.symbols("x y", real=True)
overlap_sos = canonical(
    (x**2 + y**2) ** 2 / 4 - (x * y) ** 2 - (x**2 - y**2) ** 2 / 4
)
require(overlap_sos == 0, "two-entry shifted overlap SOS")

Q_gamma_plus = Q_frame.subs(gamma, 1).applyfunc(canonical)
Q_gamma_minus = Q_frame.subs(gamma, -1).applyfunc(canonical)
plus_target = outer(w_symbol + epsilon * h_symbol)
minus_target = outer(w_symbol - epsilon * h_symbol)
plus_defect = tensor_defect.subs(gamma, 1).applyfunc(canonical)
minus_defect = tensor_defect.subs(gamma, -1).applyfunc(canonical)
minus_defect_expected = (
    2
    * epsilon
    * (outer(w_symbol, h_symbol) + outer(h_symbol, w_symbol))
).applyfunc(canonical)
plus_commutator = canonical(commutator_polynomial.subs(gamma, 1))
minus_commutator = canonical(commutator_polynomial.subs(gamma, -1))
minus_commutator_expected = canonical(-2 * epsilon * A * delta * a**2 * b / K**3)

require(matrix_is_zero(Q_gamma_plus - plus_target), "gamma=+1 exact-rank branch")
require(matrix_is_zero(Q_gamma_minus - minus_target), "gamma=-1 exact-rank branch")
require(matrix_is_zero(plus_defect), "gamma=+1 physical/frame cancellation")
require(
    matrix_is_zero(minus_defect - minus_defect_expected),
    "gamma=-1 nonzero physical/frame defect",
)
require(plus_commutator == 0, "gamma=+1 commutator cancellation")
require(
    canonical(minus_commutator - minus_commutator_expected) == 0,
    "gamma=-1 nonzero commutator branch",
)


# ---------------------------------------------------------------------------
# 4. Critical exponent arithmetic.
# ---------------------------------------------------------------------------

theta = sp.symbols("theta", real=True)
ratio_power = canonical(1 - 2 * theta)
require(canonical(ratio_power.subs(theta, 1) + 1) == 0, "linear exponent")
require(
    canonical(ratio_power.subs(theta, sp.Rational(3, 4)) + sp.Rational(1, 2))
    == 0,
    "three-quarter exponent",
)
require(canonical(ratio_power.subs(theta, sp.Rational(1, 2))) == 0, "critical exponent")


payload = {
    "release": "R0.70U",
    "status": "fixed-frame-signed-square-root-obstruction-audit",
    "checks": {
        "pythagoreanTriadAndBiotSavart": True,
        "nonzeroSignedFourierResonance": True,
        "fixedFrameCovarianceAndSpectrum": True,
        "superSquareRootExponentArithmetic": True,
    },
    "triadLedger": {
        "parameterPremise": "integer m>=2 and amplitudes A>delta>0",
        "a": scalar_payload(a),
        "b": scalar_payload(b),
        "K": scalar_payload(K),
        "pythagoreanResidual": scalar_payload(a**2 + b**2 - K**2),
        "k": vector_payload(sp.Matrix(k)),
        "p": vector_payload(sp.Matrix(p)),
        "q": vector_payload(sp.Matrix(q)),
        "qMinusKPlusP": vector_payload(sp.Matrix(q) - sp.Matrix(k) - sp.Matrix(p)),
        "n": vector_payload(n),
        "nNormResidual": scalar_payload(n.dot(n) - 1),
        "kDotN": scalar_payload(sp.Matrix(k).dot(n)),
        "w1HelicitySign": "curl(w1)=-K*w1",
        "allFourierDivergenceResiduals": "0",
        "curlUwMinusWResiduals": "0",
        "curlUhMinusHResiduals": "0",
    },
    "resonanceLedger": {
        "normalizedI": scalar_payload(I),
        "expectedI": scalar_payload(I_expected),
        "normalizedJ": scalar_payload(J),
        "expectedJ": scalar_payload(J_expected),
        "physicalStretchingDerivative": scalar_payload(physical_stretching_derivative),
        "frameCovarianceDerivative": scalar_payload(frame_covariance_derivative),
        "commutatorDerivative": scalar_payload(commutator_derivative),
        "commutatorExpected": scalar_payload(commutator_expected),
        "physicalStretchingPolynomial": scalar_payload(
            physical_stretching_polynomial
        ),
        "frameCovariancePolynomial": scalar_payload(
            frame_covariance_polynomial
        ),
        "commutatorPolynomial": scalar_payload(commutator_polynomial),
        "physicalHigherOrderResidual": scalar_payload(
            physical_stretching_polynomial
            - epsilon * physical_stretching_derivative
        ),
        "frameHigherOrderResidual": scalar_payload(
            frame_covariance_polynomial
            - epsilon * frame_covariance_derivative
        ),
        "commutatorHigherOrderResidual": scalar_payload(
            commutator_polynomial - epsilon * commutator_expected
        ),
        "m3Anchor": {
            "parameters": "m=3, a=8, b=6, K=10, A=2, delta=1",
            "I": scalar_payload(m3_I),
            "J": scalar_payload(m3_J),
            "physicalStretchingDerivative": scalar_payload(
                m3_physical_derivative
            ),
            "commutatorDerivative": scalar_payload(m3_commutator_derivative),
            "scope": "algebraic sign/coefficient anchor only; it does not certify |gamma|<=3/4 for the unspecified cutoff",
        },
        "nonzeroPremises": "A>delta>0, integer m>=2, and |gamma|<=3/4",
    },
    "covarianceLedger": {
        "factorizationResidual": matrix_payload(Q_frame - Q_factor),
        "tensorDefectResidual": matrix_payload(tensor_defect - tensor_defect_expected),
        "determinant": scalar_payload(Q_frame.det()),
        "traceFromMatrix": scalar_payload(trace_from_matrix),
        "traceExpectedFromVectors": scalar_payload(trace_expected_from_vectors),
        "traceMatrixResidual": scalar_payload(
            trace_from_matrix - trace_expected_from_vectors
        ),
        "sigmaTwoFromMatrix": scalar_payload(sigma_two_from_matrix),
        "sigmaTwoExpectedFromVectors": scalar_payload(
            sigma_two_expected_from_vectors
        ),
        "sigmaTwoMatrixResidual": scalar_payload(
            sigma_two_from_matrix - sigma_two_expected_from_vectors
        ),
        "traceInvariant": scalar_payload(trace_invariant),
        "nonzeroEigenvalueProduct": scalar_payload(product_invariant),
        "lambdaTwoOverEpsilonSquaredLimit": scalar_payload(lambda_two_leading),
        "expectedResidualCoefficient": scalar_payload(lambda_two_expected),
        "originCrossSquare": scalar_payload(origin_cross_square),
        "originCrossExpected": scalar_payload(origin_cross_expected),
        "shiftedTwoEntryOverlapSOSResidual": scalar_payload(overlap_sos),
    },
    "exactRankSignLedger": {
        "gammaPlusCovarianceResidual": matrix_payload(Q_gamma_plus - plus_target),
        "gammaMinusCovarianceResidual": matrix_payload(Q_gamma_minus - minus_target),
        "gammaPlusPhysicalDefect": matrix_payload(plus_defect),
        "gammaMinusPhysicalDefectResidual": matrix_payload(
            minus_defect - minus_defect_expected
        ),
        "gammaPlusCommutator": scalar_payload(plus_commutator),
        "gammaMinusCommutator": scalar_payload(minus_commutator),
        "gammaMinusCommutatorExpected": scalar_payload(
            minus_commutator_expected
        ),
        "boundary": "kappa=0 permits gamma=+1 or gamma=-1; exact rank alone does not imply aggregate commutator cancellation under sign-indefinite frame responses",
    },
    "exponentLedger": {
        "remainderOrder": "|epsilon|",
        "residualNormOrder": "|epsilon|^2",
        "ratioPowerForResidualTheta": scalar_payload(ratio_power),
        "linearRatioPower": scalar_payload(ratio_power.subs(theta, 1)),
        "threeQuarterRatioPower": scalar_payload(
            ratio_power.subs(theta, sp.Rational(3, 4))
        ),
        "criticalRatioPower": scalar_payload(
            ratio_power.subs(theta, sp.Rational(1, 2))
        ),
        "analyticReading": "1-2*theta<0 exactly when theta>1/2",
    },
    "analyticDependencies": [
        "the countable pinned complete-frame definition, convergence, and multiplier response lifting",
        "for each fixed cutoff, the arbitrary-profile overlap estimate and analytic existence of m0(phi); no numerical m is certified without an explicit phi",
        "the uniform global top-gap bound and smooth simple-eigenprojector perturbation from Q_tilde to Q",
        "the uniform residual expansion and its Lp Theta(epsilon^2) consequence, which is not a pointwise positive lower bound",
        "the locally bounded-prefactor quantifiers and the general modulus o(sqrt(s)) no-go",
        "local Navier--Stokes existence from smooth data and every time-evolution or continuation interpretation",
    ],
    "claimBoundary": (
        "The direct certificate checks finite exact Fourier, Biot--Savart, "
        "resonance, covariance, rank-two invariant, and exponent algebra. It "
        "does not numerically select m for an unspecified cutoff, prove a "
        "pointwise residual lower bound, exclude the critical exponent 1/2, "
        "exclude derivative, paraproduct, or time-integrated estimates, prove "
        "persistence of the finite Fourier form, provide an enstrophy closure "
        "or singularity, establish unconditional global regularity, or solve "
        "the Millennium problem."
    ),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    serialized = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if arguments.output is None:
        print(serialized, end="")
    else:
        arguments.output.write_text(serialized, encoding="utf-8")


if __name__ == "__main__":
    main()
