#!/usr/bin/env python3
"""Exact finite/symbolic audit for the R0.70T stretching ledger.

The producer directly checks five narrowly scoped groups:

1. a noncommuting finite Parseval model that fixes the plus sign in the
   stretching-commutator identity;
2. a nonzero periodic row-gradient/integration-by-parts sample;
3. finite covariance-block algebra, the divergence-free amplitude
   cancellation modulo its explicit block constraints, and the sharp
   Cauchy--Schwarz sum-of-squares certificate;
4. the displayed M=16 two-shell vertical-shear field, its global heat-flow
   residuals, and its pointwise sharp fixed-frame response algebra modulo
   rho**2+sigma**2=1; and
5. an isolated exact-rank block jet for which A_L=0 but J_P>0.

The countable Parseval theorem, the pinned multiplier support/tightness
lifting, general simple-eigenprojector calculus, and the PDE continuation
reading are analytic lemmas in the report.  They are not inferred from these
finite checks.  This certificate proves neither a PDE closure nor a
singularity/global-regularity result.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def canonical(expression: sp.Expr) -> sp.Expr:
    # All zero tests below arise from exact product-rule cancellation with
    # identical Fourier atoms.  Expanding and cancelling is both sufficient
    # and far more deterministic than a global trigsimp of the 80-mode field.
    return sp.cancel(sp.expand(expression))


def matrix_is_zero(matrix: sp.Matrix) -> bool:
    return all(canonical(entry) == 0 for entry in matrix)


def matrix_equal(first: sp.Matrix, second: sp.Matrix) -> bool:
    return first.shape == second.shape and matrix_is_zero(first - second)


def scalar_payload(value: sp.Expr) -> str:
    return str(canonical(value))


def vector_payload(vector: sp.Matrix) -> list[str]:
    return [scalar_payload(entry) for entry in vector]


def matrix_payload(matrix: sp.Matrix) -> list[list[str]]:
    return [
        [scalar_payload(matrix[row, column]) for column in range(matrix.cols)]
        for row in range(matrix.rows)
    ]


def outer(vector: sp.Matrix) -> sp.Matrix:
    return vector * vector.T


def divergence(
    vector: sp.Matrix,
    coordinates: tuple[sp.Symbol, sp.Symbol, sp.Symbol],
) -> sp.Expr:
    return canonical(
        sum(sp.diff(vector[index], coordinates[index]) for index in range(3))
    )


def curl(
    vector: sp.Matrix,
    coordinates: tuple[sp.Symbol, sp.Symbol, sp.Symbol],
) -> sp.Matrix:
    x1, x2, x3 = coordinates
    return sp.Matrix(
        [
            sp.diff(vector[2], x2) - sp.diff(vector[1], x3),
            sp.diff(vector[0], x3) - sp.diff(vector[2], x1),
            sp.diff(vector[1], x1) - sp.diff(vector[0], x2),
        ]
    ).applyfunc(canonical)


def laplacian(
    vector: sp.Matrix,
    coordinates: tuple[sp.Symbol, sp.Symbol, sp.Symbol],
) -> sp.Matrix:
    return sp.Matrix(
        [
            sum(sp.diff(component, coordinate, 2) for coordinate in coordinates)
            for component in vector
        ]
    ).applyfunc(canonical)


def row_gradient(
    vector: sp.Matrix,
    coordinates: tuple[sp.Symbol, sp.Symbol, sp.Symbol],
) -> sp.Matrix:
    return sp.Matrix(
        3,
        3,
        lambda row, column: sp.diff(vector[column], coordinates[row]),
    )


def advective_derivative(
    velocity: sp.Matrix,
    vector: sp.Matrix,
    coordinates: tuple[sp.Symbol, sp.Symbol, sp.Symbol],
) -> sp.Matrix:
    return sp.Matrix(
        [
            sum(
                velocity[index] * sp.diff(component, coordinates[index])
                for index in range(3)
            )
            for component in vector
        ]
    ).applyfunc(canonical)


def tensor_row_divergence(
    tensor: sp.Matrix,
    coordinates: tuple[sp.Symbol, sp.Symbol, sp.Symbol],
) -> sp.Matrix:
    return sp.Matrix(
        [
            sum(
                sp.diff(tensor[row, column], coordinates[row])
                for row in range(3)
            )
            for column in range(3)
        ]
    ).applyfunc(canonical)


def normalized_average_2d(
    expression: sp.Expr,
    x1: sp.Symbol,
    x2: sp.Symbol,
) -> sp.Expr:
    integral = sp.integrate(
        sp.integrate(expression, (x1, 0, 2 * sp.pi)),
        (x2, 0, 2 * sp.pi),
    )
    return canonical(integral / (2 * sp.pi) ** 2)


def at_origin(
    expression: sp.Expr | sp.Matrix,
    coordinates: tuple[sp.Symbol, sp.Symbol, sp.Symbol],
) -> sp.Expr | sp.Matrix:
    substitutions = {coordinate: 0 for coordinate in coordinates}
    if isinstance(expression, sp.MatrixBase):
        return expression.subs(substitutions).applyfunc(canonical)
    return canonical(expression.subs(substitutions))


def projector_derivative_at_diagonal_top(
    covariance_derivative: sp.Matrix,
    eigenvalues: tuple[sp.Expr, sp.Expr, sp.Expr],
) -> sp.Matrix:
    basis = [
        sp.Matrix([1, 0, 0]),
        sp.Matrix([0, 1, 0]),
        sp.Matrix([0, 0, 1]),
    ]
    top = basis[0]
    result = sp.zeros(3)
    for index in (1, 2):
        transverse = basis[index]
        coefficient = canonical(
            (transverse.T * covariance_derivative * top)[0]
            / (eigenvalues[0] - eigenvalues[index])
        )
        result += coefficient * (transverse * top.T + top * transverse.T)
    return result.applyfunc(canonical)


def projected_block_divergence_at_point(
    block_value: sp.Matrix,
    block_derivatives: list[sp.Matrix],
    projector: sp.Matrix,
    projector_derivatives: list[sp.Matrix],
) -> sp.Expr:
    terms = []
    for coordinate_index in range(3):
        derivative = (
            projector_derivatives[coordinate_index] * block_value
            + projector * block_derivatives[coordinate_index]
        )
        terms.append(derivative[coordinate_index])
    return canonical(sum(terms))


# ---------------------------------------------------------------------------
# 1. A genuinely noncommuting finite Parseval stretching ledger.
# ---------------------------------------------------------------------------

T_1 = sp.diag(sp.Rational(3, 5), sp.Rational(5, 13))
T_2 = sp.diag(sp.Rational(4, 5), sp.Rational(12, 13))
finite_S = sp.Matrix([[2, 3], [3, -1]])
finite_w = sp.Matrix([1, 2])
finite_blocks = [T_1, T_2]

finite_parseval = T_1.T * T_1 + T_2.T * T_2
require(matrix_equal(finite_parseval, sp.eye(2)), "finite Parseval resolution")
require(matrix_equal(T_1, T_1.T), "T_1 self-adjoint")
require(matrix_equal(T_2, T_2.T), "T_2 self-adjoint")
require(matrix_equal(finite_S, finite_S.T), "finite S symmetric")

finite_lhs = canonical((finite_w.T * finite_S * finite_w)[0])
finite_direct_terms = [
    canonical(((operator * finite_w).T * finite_S * (operator * finite_w))[0])
    for operator in finite_blocks
]
finite_commutator_terms = [
    canonical(
        (
            (operator * finite_w).T
            * (operator * finite_S - finite_S * operator)
            * finite_w
        )[0]
    )
    for operator in finite_blocks
]
finite_direct = canonical(sum(finite_direct_terms))
finite_commutator = canonical(sum(finite_commutator_terms))
finite_parseval_residual = canonical(
    finite_lhs - finite_direct - finite_commutator
)
require(finite_lhs == 10, "finite stretching left side")
require(finite_direct == sp.Rational(626, 65), "finite covariance term")
require(
    finite_commutator == sp.Rational(24, 65),
    "finite nonzero commutator term",
)
require(finite_commutator != 0, "commutator must be nonzero")
require(finite_parseval_residual == 0, "finite stretching split")


# ---------------------------------------------------------------------------
# 2. A nonzero periodic integration-by-parts and row-gradient sample.
# ---------------------------------------------------------------------------

x1, x2, x3, t = sp.symbols("x1 x2 x3 t", real=True)
coordinates = (x1, x2, x3)
periodic_u = sp.Matrix(
    [
        2 * sp.cos(x2),
        0,
        2 * sp.cos(x1) + 2 * sp.sin(x1 + x2),
    ]
)
periodic_B = row_gradient(periodic_u, coordinates)
periodic_S = (periodic_B + periodic_B.T) / 2
periodic_omega = curl(periodic_u, coordinates)
periodic_Q = outer(periodic_omega)
periodic_div_Q = tensor_row_divergence(periodic_Q, coordinates)
periodic_transport = advective_derivative(
    periodic_omega, periodic_omega, coordinates
)

require(divergence(periodic_u, coordinates) == 0, "periodic velocity divergence")
require(
    divergence(periodic_omega, coordinates) == 0,
    "periodic vorticity divergence",
)
require(
    matrix_equal(periodic_div_Q, periodic_transport),
    "div(omega tensor omega) transport identity",
)
require(matrix_equal(periodic_Q, periodic_Q.T), "periodic Q symmetric")

periodic_covariance_integrand = canonical(
    sum(
        periodic_S[row, column] * periodic_Q[row, column]
        for row in range(3)
        for column in range(3)
    )
)
periodic_gradient_integrand = canonical(
    sum(
        periodic_B[row, column] * periodic_Q[row, column]
        for row in range(3)
        for column in range(3)
    )
)
periodic_ibp_integrand = canonical(-periodic_u.dot(periodic_div_Q))
periodic_covariance_average = normalized_average_2d(
    periodic_covariance_integrand, x1, x2
)
periodic_gradient_average = normalized_average_2d(
    periodic_gradient_integrand, x1, x2
)
periodic_ibp_average = normalized_average_2d(
    periodic_ibp_integrand, x1, x2
)
require(periodic_covariance_average == 2, "nonzero S:Q integral")
require(periodic_gradient_average == 2, "nonzero B:Q integral")
require(periodic_ibp_average == 2, "nonzero integration-by-parts integral")


# ---------------------------------------------------------------------------
# 3. Finite covariance splitting, cancellation polynomial, and sharp SOS.
# ---------------------------------------------------------------------------

ell = sp.Matrix([1, 0, 0])
L = outer(ell)
P = sp.eye(3) - L
a_symbols = sp.symbols("a1 a2 a3", real=True)
d_symbols = sp.symbols("d1 d2 d3", real=True)
p_symbols = sp.symbols("p1 p2 p3", real=True)
b22, b23, b32, b33, b42, b43 = sp.symbols(
    "b12 b13 b22 b23 b32 b33", real=True
)
b_vectors = [
    sp.Matrix([0, b22, b23]),
    sp.Matrix([0, b32, b33]),
    sp.Matrix([0, b42, b43]),
]
omega_blocks = [
    a_symbols[index] * ell + b_vectors[index] for index in range(3)
]
symbolic_Q = sp.zeros(3)
symbolic_H = sp.zeros(3)
symbolic_C = sp.zeros(3, 1)
for index in range(3):
    symbolic_Q += outer(omega_blocks[index])
    symbolic_H += outer(b_vectors[index])
    symbolic_C += a_symbols[index] * b_vectors[index]
symbolic_lambda = sum(value**2 for value in a_symbols)
covariance_expansion_residual = (
    symbolic_Q
    - symbolic_lambda * L
    - symbolic_H
    - ell * symbolic_C.T
    - symbolic_C * ell.T
).applyfunc(canonical)
spectral_cross_residual = (P * symbolic_Q * ell - symbolic_C).applyfunc(canonical)
require(
    matrix_is_zero(covariance_expansion_residual),
    "finite covariance block expansion",
)
require(matrix_is_zero(spectral_cross_residual), "spectral cross vector")

g12, g13, g22, g23, g32, g33 = sp.symbols(
    "g12 g13 g22 g23 g32 g33", real=True
)
ell_gradient = sp.Matrix(
    [
        [0, g12, g13],
        [0, g22, g23],
        [0, g32, g33],
    ]
)
ell_derivatives = [sp.Matrix(ell_gradient.row(index)).T for index in range(3)]
L_derivatives = [
    derivative * ell.T + ell * derivative.T for derivative in ell_derivatives
]
div_L = sp.Matrix(
    [
        sum(L_derivatives[index][index, component] for index in range(3))
        for component in range(3)
    ]
).applyfunc(canonical)
div_ell = canonical(sum(ell_gradient[index, index] for index in range(3)))
L_div_L_residual = (L * div_L - div_ell * ell).applyfunc(canonical)
require(matrix_is_zero(L_div_L_residual), "L div L identity")

lambda_gradient_symbols = sp.Matrix(sp.symbols("lambda_x1 lambda_x2 lambda_x3"))
A_L_definition = L * (
    lambda_gradient_symbols + 2 * symbolic_lambda * div_L
)
div_lambda_L = L * lambda_gradient_symbols + symbolic_lambda * div_L
reflection_decomposition_residual = (
    div_lambda_L
    - symbolic_lambda * (sp.eye(3) - 2 * L) * div_L
    - A_L_definition
).applyfunc(canonical)
require(
    matrix_is_zero(reflection_decomposition_residual),
    "orientation-free reflection decomposition",
)

block_divergence_residuals = [
    p_symbols[index]
    + a_symbols[index] * div_ell
    + d_symbols[index]
    for index in range(3)
]
raw_longitudinal_A = canonical(
    2 * sum(a_symbols[index] * p_symbols[index] for index in range(3))
    + 2 * symbolic_lambda * div_ell
)
cancellation_polynomial = canonical(
    raw_longitudinal_A
    + 2 * sum(a_symbols[index] * d_symbols[index] for index in range(3))
    - 2
    * sum(
        a_symbols[index] * block_divergence_residuals[index]
        for index in range(3)
    )
)
require(cancellation_polynomial == 0, "amplitude cancellation polynomial")

orientation_flip_residual = (
    -2
    * (-ell)
    * sum((-a_symbols[index]) * d_symbols[index] for index in range(3))
    + 2 * ell * sum(a_symbols[index] * d_symbols[index] for index in range(3))
).applyfunc(canonical)
require(matrix_is_zero(orientation_flip_residual), "orientation flip invariance")

symbolic_J = sum(value**2 for value in d_symbols)
symbolic_pairing = sum(
    a_symbols[index] * d_symbols[index] for index in range(3)
)
sharp_sos = sum(
    (a_symbols[first] * d_symbols[second] - a_symbols[second] * d_symbols[first])
    ** 2
    for first in range(3)
    for second in range(first + 1, 3)
)
sharp_sos_residual = canonical(
    symbolic_lambda * symbolic_J - symbolic_pairing**2 - sharp_sos
)
require(sharp_sos_residual == 0, "sharp Cauchy SOS")

sharp_witness = {
    a_symbols[0]: 1,
    a_symbols[1]: 0,
    a_symbols[2]: 0,
    d_symbols[0]: 1,
    d_symbols[1]: 0,
    d_symbols[2]: 0,
}
sharp_witness_slack = canonical(
    (4 * symbolic_lambda * symbolic_J - 4 * symbolic_pairing**2).subs(
        sharp_witness
    )
)
require(sharp_witness_slack == 0, "sharp SOS equality witness")


# ---------------------------------------------------------------------------
# 4. The M=16 fixed-frame vertical shear and pointwise sharpness.
# ---------------------------------------------------------------------------

M = sp.Integer(16)
nu = sp.symbols("nu", positive=True, real=True)
psi_low = (
    M * sp.sin(5 * x2) / 5
    + M
    * (sp.cos(3 * x1 + 4 * x2) - sp.cos(3 * x1 - 4 * x2))
    / 24
)
psi_high = (
    -sp.sin(5 * M * x1) / (5 * M)
    + sp.cos(5 * M * x2) / 25
)
velocity_low = sp.Matrix([0, 0, psi_low / M])
velocity_high = sp.Matrix([0, 0, psi_high / M])
velocity_zero = velocity_low + velocity_high
omega_low = curl(velocity_low, coordinates)
omega_high = curl(velocity_high, coordinates)
omega_total = (omega_low + omega_high).applyfunc(canonical)

require(divergence(velocity_zero, coordinates) == 0, "shear velocity divergence")
require(divergence(omega_low, coordinates) == 0, "low-shell divergence")
require(divergence(omega_high, coordinates) == 0, "high-shell divergence")
require(
    matrix_equal(curl(velocity_zero, coordinates), omega_total),
    "shear curl identity",
)
require(
    matrix_is_zero(laplacian(omega_low, coordinates) + 25 * omega_low),
    "low shell Laplace eigenvalue",
)
require(
    matrix_is_zero(
        laplacian(omega_high, coordinates) + (5 * M) ** 2 * omega_high
    ),
    "high shell Laplace eigenvalue",
)

mean_omega_low = sp.Matrix(
    [normalized_average_2d(component, x1, x2) for component in omega_low]
)
mean_omega_high = sp.Matrix(
    [normalized_average_2d(component, x1, x2) for component in omega_high]
)
require(matrix_is_zero(mean_omega_low), "low-shell mean zero")
require(matrix_is_zero(mean_omega_high), "high-shell mean zero")

low_decay = sp.exp(-25 * nu * t)
high_decay = sp.exp(-(5 * M) ** 2 * nu * t)
velocity_time = low_decay * velocity_low + high_decay * velocity_high
omega_time = curl(velocity_time, coordinates)
heat_residual = (
    sp.diff(velocity_time, t) - nu * laplacian(velocity_time, coordinates)
).applyfunc(canonical)
vorticity_heat_residual = (
    sp.diff(omega_time, t) - nu * laplacian(omega_time, coordinates)
).applyfunc(canonical)
shear_nonlinearity = advective_derivative(
    velocity_time, velocity_time, coordinates
)
shear_B = row_gradient(velocity_time, coordinates)
shear_S = (shear_B + shear_B.T) / 2
shear_stretching = (shear_S * omega_time).applyfunc(canonical)
require(matrix_is_zero(heat_residual), "global shear heat equation")
require(
    matrix_is_zero(vorticity_heat_residual),
    "global shear vorticity heat equation",
)
require(matrix_is_zero(shear_nonlinearity), "global shear nonlinearity")
require(matrix_is_zero(shear_stretching), "vertical shear stretching")

rho, sigma = sp.symbols("rho sigma", real=True)
tight_relation = rho**2 + sigma**2 - 1
frame_blocks = [
    rho * omega_low,
    sigma * omega_low,
    rho * omega_high,
    sigma * omega_high,
]
frame_covariance = sp.zeros(3)
for block in frame_blocks:
    frame_covariance += outer(block)
target_covariance = outer(omega_low) + outer(omega_high)
frame_factor_certificate = (
    frame_covariance - target_covariance - tight_relation * target_covariance
).applyfunc(canonical)
require(
    matrix_is_zero(frame_factor_certificate),
    "conditional fixed-frame covariance factor",
)

omega_low_zero = at_origin(omega_low, coordinates)
omega_high_zero = at_origin(omega_high, coordinates)
omega_low_derivatives = [
    at_origin(omega_low.diff(coordinate), coordinates) for coordinate in coordinates
]
omega_high_derivatives = [
    at_origin(omega_high.diff(coordinate), coordinates)
    for coordinate in coordinates
]
require(
    matrix_equal(omega_low_zero, sp.Matrix([1, 0, 0])),
    "low-shell origin value",
)
require(
    matrix_equal(omega_high_zero, sp.Matrix([0, sp.Rational(1, 16), 0])),
    "high-shell origin value",
)
expected_low_derivatives = [
    sp.Matrix([-1, 0, 0]),
    sp.Matrix([0, 1, 0]),
    sp.zeros(3, 1),
]
expected_high_derivatives = [
    sp.zeros(3, 1),
    sp.Matrix([-16, 0, 0]),
    sp.zeros(3, 1),
]
for index in range(3):
    require(
        matrix_equal(omega_low_derivatives[index], expected_low_derivatives[index]),
        f"low-shell derivative {index}",
    )
    require(
        matrix_equal(
            omega_high_derivatives[index], expected_high_derivatives[index]
        ),
        f"high-shell derivative {index}",
    )

covariance_zero = at_origin(target_covariance, coordinates)
covariance_derivatives = [
    at_origin(target_covariance.diff(coordinate), coordinates)
    for coordinate in coordinates
]
expected_covariance_zero = sp.diag(1, sp.Rational(1, 256), 0)
expected_covariance_derivatives = [
    sp.diag(-2, 0, 0),
    sp.zeros(3),
    sp.zeros(3),
]
require(
    matrix_equal(covariance_zero, expected_covariance_zero),
    "origin covariance",
)
for index in range(3):
    require(
        matrix_equal(
            covariance_derivatives[index], expected_covariance_derivatives[index]
        ),
        f"origin covariance derivative {index}",
    )

shear_eigenvalues = (sp.Integer(1), sp.Rational(1, 256), sp.Integer(0))
shear_energy = canonical(sp.trace(covariance_zero))
shear_residual = canonical(sp.trace(P * covariance_zero))
shear_absolute_gap = canonical(shear_eigenvalues[0] - shear_eigenvalues[1])
shear_relative_gap = canonical(shear_absolute_gap / shear_energy)
shear_residual_ratio = canonical(shear_residual / shear_energy)
require(shear_energy == sp.Rational(257, 256), "origin energy")
require(shear_residual == sp.Rational(1, 256), "origin residual")
require(shear_absolute_gap == sp.Rational(255, 256), "origin absolute gap")
require(shear_relative_gap == sp.Rational(255, 257), "origin relative gap")
require(shear_residual_ratio == sp.Rational(1, 257), "origin residual ratio")
shear_L_derivatives = [
    projector_derivative_at_diagonal_top(derivative, shear_eigenvalues)
    for derivative in covariance_derivatives
]
require(
    all(matrix_is_zero(derivative) for derivative in shear_L_derivatives),
    "origin top-projector derivative",
)
shear_div_L = sp.Matrix(
    [
        sum(
            shear_L_derivatives[index][index, component] for index in range(3)
        )
        for component in range(3)
    ]
).applyfunc(canonical)
shear_lambda_gradient = sp.Matrix(
    [
        canonical((ell.T * derivative * ell)[0])
        for derivative in covariance_derivatives
    ]
)
shear_A_definition = (
    L * (shear_lambda_gradient + 2 * shear_eigenvalues[0] * shear_div_L)
).applyfunc(canonical)
require(
    matrix_equal(shear_A_definition, sp.Matrix([-2, 0, 0])),
    "origin A_L from covariance derivative",
)

shear_P_derivatives = [(-derivative).applyfunc(canonical) for derivative in shear_L_derivatives]
frame_block_values = [
    rho * omega_low_zero,
    sigma * omega_low_zero,
    rho * omega_high_zero,
    sigma * omega_high_zero,
]
frame_block_derivatives = [
    [rho * derivative for derivative in omega_low_derivatives],
    [sigma * derivative for derivative in omega_low_derivatives],
    [rho * derivative for derivative in omega_high_derivatives],
    [sigma * derivative for derivative in omega_high_derivatives],
]
frame_gradient_density_raw = canonical(
    sum(
        sum(
            sum(component**2 for component in derivative)
            for derivative in block_derivatives
        )
        for block_derivatives in frame_block_derivatives
    )
)
require(
    canonical(frame_gradient_density_raw - 258 * (rho**2 + sigma**2)) == 0,
    "fixed-frame gradient density",
)
projected_divergences = [
    projected_block_divergence_at_point(
        frame_block_values[index],
        frame_block_derivatives[index],
        P,
        shear_P_derivatives,
    )
    for index in range(4)
]
expected_projected_divergences = [rho, sigma, sp.Integer(0), sp.Integer(0)]
require(
    all(
        canonical(projected_divergences[index] - expected_projected_divergences[index])
        == 0
        for index in range(4)
    ),
    "full projected block divergences",
)
frame_J_raw = canonical(sum(value**2 for value in projected_divergences))
frame_a_values = [canonical((ell.T * value)[0]) for value in frame_block_values]
frame_A_raw = (
    -2
    * ell
    * sum(
        frame_a_values[index] * projected_divergences[index]
        for index in range(4)
    )
).applyfunc(canonical)
require(
    canonical(frame_J_raw - (rho**2 + sigma**2)) == 0,
    "raw fixed-frame J_P",
)
require(
    matrix_is_zero(frame_A_raw + 2 * (rho**2 + sigma**2) * ell),
    "raw fixed-frame A_L",
)
conditional_A_residual = (
    frame_A_raw - shear_A_definition + 2 * tight_relation * ell
).applyfunc(canonical)
require(matrix_is_zero(conditional_A_residual), "conditional sharp A_L")
fixed_frame_sharp_slack = canonical(
    4 * shear_eigenvalues[0] * frame_J_raw - (frame_A_raw.T * frame_A_raw)[0]
)
require(
    canonical(fixed_frame_sharp_slack.subs(sigma**2, 1 - rho**2)) == 0,
    "fixed-frame sharp equality modulo tightness",
)


# ---------------------------------------------------------------------------
# 5. Isolated exact-rank point: A_L=0 but J_P=2.
# ---------------------------------------------------------------------------

rank_block_1 = sp.Matrix([1 - x1, x2, 0])
rank_block_2 = sp.Matrix([1 + x1, -x2, 0])
require(divergence(rank_block_1, coordinates) == 0, "rank block 1 divergence")
require(divergence(rank_block_2, coordinates) == 0, "rank block 2 divergence")
rank_Q = outer(rank_block_1) + outer(rank_block_2)
rank_Q_zero = at_origin(rank_Q, coordinates)
rank_Q_derivatives = [
    at_origin(rank_Q.diff(coordinate), coordinates) for coordinate in coordinates
]
require(matrix_equal(rank_Q_zero, sp.diag(2, 0, 0)), "rank-one Q at origin")
require(
    all(matrix_is_zero(derivative) for derivative in rank_Q_derivatives),
    "rank-one covariance first derivatives",
)
rank_eigenvalues = (sp.Integer(2), sp.Integer(0), sp.Integer(0))
rank_L_derivatives = [
    projector_derivative_at_diagonal_top(derivative, rank_eigenvalues)
    for derivative in rank_Q_derivatives
]
rank_P_derivatives = [(-derivative).applyfunc(canonical) for derivative in rank_L_derivatives]
rank_block_values = [
    at_origin(rank_block_1, coordinates),
    at_origin(rank_block_2, coordinates),
]
rank_block_derivatives = [
    [at_origin(rank_block_1.diff(coordinate), coordinates) for coordinate in coordinates],
    [at_origin(rank_block_2.diff(coordinate), coordinates) for coordinate in coordinates],
]
rank_projected_values = [(P * value).applyfunc(canonical) for value in rank_block_values]
rank_projected_divergences = [
    projected_block_divergence_at_point(
        rank_block_values[index],
        rank_block_derivatives[index],
        P,
        rank_P_derivatives,
    )
    for index in range(2)
]
rank_J = canonical(sum(value**2 for value in rank_projected_divergences))
rank_a_values = [canonical((ell.T * value)[0]) for value in rank_block_values]
rank_A = (
    -2
    * ell
    * sum(
        rank_a_values[index] * rank_projected_divergences[index]
        for index in range(2)
    )
).applyfunc(canonical)
require(
    all(matrix_is_zero(value) for value in rank_projected_values),
    "rank-one projected block values",
)
require(
    rank_projected_divergences == [sp.Integer(1), sp.Integer(-1)],
    "isolated rank-one projected divergences",
)
require(rank_J == 2, "isolated rank-one J_P")
require(matrix_is_zero(rank_A), "isolated rank-one A_L")


# ---------------------------------------------------------------------------
# Deterministic payload.
# ---------------------------------------------------------------------------

payload = {
    "release": "R0.70T",
    "status": "exact-frame-stretching-divergence-defect-audit",
    "arithmetic": "exact SymPy rational, matrix, polynomial, trigonometric, and finite Fourier-shell arithmetic",
    "checks": {
        "finiteParsevalStretchingSign": True,
        "nonzeroPeriodicProductRuleSample": True,
        "coordinateCancellationAndSharpSOS": True,
        "fixedFrameGlobalShearSharpness": True,
        "isolatedRankOneBoundaryJet": True,
    },
    "definitions": {
        "torus": "(R/(2*pi*Z))^3 with normalized Haar measure",
        "rowGradient": "B_ij=partial_i u_j",
        "tensorDivergence": "(div Q)_j=sum_i partial_i Q_ij",
        "commutator": "[T,S]=T(S dot)-S*T",
        "completeFrame": "{T_star=Pi_0} union {T_j:j in Z}",
        "longitudinalDefect": "A_L=L*(grad(lambda)+2*lambda*div(L))",
        "projectedDivergenceSquare": "J_P=sum_alpha |div(P*Omega_alpha)|^2",
    },
    "finiteParsevalLedger": {
        "T1": matrix_payload(T_1),
        "T2": matrix_payload(T_2),
        "S": matrix_payload(finite_S),
        "w": vector_payload(finite_w),
        "parsevalResolution": matrix_payload(finite_parseval),
        "leftSide": scalar_payload(finite_lhs),
        "covarianceTerms": [scalar_payload(value) for value in finite_direct_terms],
        "covarianceTotal": scalar_payload(finite_direct),
        "commutatorTerms": [
            scalar_payload(value) for value in finite_commutator_terms
        ],
        "commutatorTotal": scalar_payload(finite_commutator),
        "splitResidual": scalar_payload(finite_parseval_residual),
        "scope": "finite noncommuting Hilbert-space model fixing the exact plus sign; not a proof of the countable Fourier-frame theorem",
    },
    "periodicProductRuleLedger": {
        "velocity": vector_payload(periodic_u),
        "vorticity": vector_payload(periodic_omega),
        "velocityDivergence": scalar_payload(divergence(periodic_u, coordinates)),
        "vorticityDivergence": scalar_payload(
            divergence(periodic_omega, coordinates)
        ),
        "divQMinusOmegaDotGradOmega": vector_payload(
            periodic_div_Q - periodic_transport
        ),
        "normalizedIntegralSColonQ": scalar_payload(periodic_covariance_average),
        "normalizedIntegralBColonQ": scalar_payload(periodic_gradient_average),
        "normalizedIntegralMinusUDotDivQ": scalar_payload(periodic_ibp_average),
        "scope": "one exact nonzero smooth periodic sample fixing row-gradient and integration-by-parts signs; the general Sobolev identity is analytic",
    },
    "amplitudeCancellationLedger": {
        "covarianceExpansionResidual": matrix_payload(
            covariance_expansion_residual
        ),
        "spectralCrossResidual": vector_payload(spectral_cross_residual),
        "spectralPremise": "P*Q*ell=C=sum_alpha a_alpha*b_alpha; the eigenline premise is C=0",
        "LDivLResidual": vector_payload(L_div_L_residual),
        "reflectionDecompositionResidual": vector_payload(
            reflection_decomposition_residual
        ),
        "blockDivergenceResiduals": [
            scalar_payload(value) for value in block_divergence_residuals
        ],
        "polynomialCertificate": "A_parallel+2*sum(a*d)=2*sum(a*c), where c=p+a*div(ell)+d",
        "polynomialResidual": scalar_payload(cancellation_polynomial),
        "conclusionModuloDivergenceConstraints": "A_L=-2*ell*sum_alpha(a_alpha*div(b_alpha))",
        "orientationFlipResidual": vector_payload(orientation_flip_residual),
        "sharpSOS": "lambda*J_P-(sum a*d)^2=sum_(i<j)(a_i*d_j-a_j*d_i)^2",
        "sharpSOSResidual": scalar_payload(sharp_sos_residual),
        "sharpWitnessSlack": scalar_payload(sharp_witness_slack),
        "scope": "finite coordinate-gauge polynomial identities; rotation to a general local orientation and smooth eigenline calculus are analytic lemmas",
    },
    "fixedFrameShearLedger": {
        "M": int(M),
        "lowShellRadius": 5,
        "highShellRadius": int(5 * M),
        "lowPossibleIndices": [2, 3],
        "highPossibleIndices": [6, 7],
        "possibleIndexIntersection": "empty",
        "activeSetBoundary": "I_5 is a nonempty subset of {2,3}; neither possible index is asserted individually nonzero; I_80=I_5+4",
        "responseSymbols": {
            "rho": "phi(5/4)",
            "sigma": "phi(5/8)",
            "tightPremise": "rho^2+sigma^2=1",
        },
        "framePremiseBoundary": "strict annular support, real-even radiality, dyadic response shift, and exact square tightness are analytic properties of the pinned frame; phi is not numerically evaluated",
        "lowVorticity": vector_payload(omega_low),
        "highVorticity": vector_payload(omega_high),
        "lowDivergence": scalar_payload(divergence(omega_low, coordinates)),
        "highDivergence": scalar_payload(divergence(omega_high, coordinates)),
        "lowMean": vector_payload(mean_omega_low),
        "highMean": vector_payload(mean_omega_high),
        "lowLaplacianResidual": vector_payload(
            laplacian(omega_low, coordinates) + 25 * omega_low
        ),
        "highLaplacianResidual": vector_payload(
            laplacian(omega_high, coordinates) + (5 * M) ** 2 * omega_high
        ),
        "frameCovarianceFactorResidual": matrix_payload(
            frame_factor_certificate
        ),
        "frameCovarianceFactorIdentity": "Q_frame-Q_target=(rho^2+sigma^2-1)*Q_target",
        "originLowValue": vector_payload(omega_low_zero),
        "originHighValue": vector_payload(omega_high_zero),
        "originLowDerivatives": [
            vector_payload(value) for value in omega_low_derivatives
        ],
        "originHighDerivatives": [
            vector_payload(value) for value in omega_high_derivatives
        ],
        "originCovariance": matrix_payload(covariance_zero),
        "originCovarianceDerivatives": [
            matrix_payload(value) for value in covariance_derivatives
        ],
        "originEigenvalues": ["1", "1/256", "0"],
        "originEnergy": scalar_payload(shear_energy),
        "originResidual": scalar_payload(shear_residual),
        "originAbsoluteGap": scalar_payload(shear_absolute_gap),
        "originRelativeGap": scalar_payload(shear_relative_gap),
        "originResidualRatio": scalar_payload(shear_residual_ratio),
        "originProjectorDerivatives": [
            matrix_payload(value) for value in shear_L_derivatives
        ],
        "originDivL": vector_payload(shear_div_L),
        "originALFromCovariance": vector_payload(shear_A_definition),
        "projectedBlockDivergences": [
            scalar_payload(value) for value in projected_divergences
        ],
        "JRaw": scalar_payload(frame_J_raw),
        "JUnderTightPremise": "1",
        "gradientDensityRaw": scalar_payload(frame_gradient_density_raw),
        "gradientDensityUnderTightPremise": "258",
        "ALRaw": vector_payload(frame_A_raw),
        "ALUnderTightPremise": ["-2", "0", "0"],
        "conditionalALResidual": vector_payload(conditional_A_residual),
        "sharpSlackModuloTightness": "0",
        "curlResidual": vector_payload(
            curl(velocity_zero, coordinates) - omega_total
        ),
        "heatEquationResidual": vector_payload(heat_residual),
        "vorticityHeatEquationResidual": vector_payload(
            vorticity_heat_residual
        ),
        "advectiveNonlinearity": vector_payload(shear_nonlinearity),
        "vortexStretching": vector_payload(shear_stretching),
        "solutionBoundary": "the displayed finite Fourier vertical shear is an exact smooth global unforced heat-flow solution; sharpness is pointwise at t=0 and stretching is identically zero",
    },
    "rankOneBoundaryLedger": {
        "blockDivergences": [
            scalar_payload(divergence(rank_block_1, coordinates)),
            scalar_payload(divergence(rank_block_2, coordinates)),
        ],
        "originCovariance": matrix_payload(rank_Q_zero),
        "originCovarianceDerivatives": [
            matrix_payload(value) for value in rank_Q_derivatives
        ],
        "originProjectedValues": [
            vector_payload(value) for value in rank_projected_values
        ],
        "originProjectedDivergences": [
            scalar_payload(value) for value in rank_projected_divergences
        ],
        "originJ": scalar_payload(rank_J),
        "originAL": vector_payload(rank_A),
        "boundary": "an isolated smooth rank-one point forces A_L=0 but need not force J_P=0; J_P=0 follows when rank one holds on an open neighborhood",
    },
    "analyticDependencies": [
        "the countable complete-frame Parseval identity, convergence, and sum/integral interchange",
        "the pinned cutoff's strict support, real-even radial response, square partition, and derivative commutation",
        "the report's general M=2^m parameter extension and limit r/E=1/(M^2+1)->0; the direct machine anchor here is M=16",
        "general smooth simple-eigenvalue projector calculus and orientation patching",
        "periodic integration by parts at the stated general Sobolev regularity",
        "the report's reduced inverse R_Q, half-curvature normalization K_Q, and general derivative-level upper ledger J_P<=6*D_P+12*gamma^(-1)*K_Q",
        "the standard H1 continuation alternative and every PDE closure implication",
    ],
    "claimBoundary": (
        "The direct certificate checks finite matrix, trigonometric, polynomial, "
        "Fourier-shell, conditional pinned-response, point-jet, and global vertical-"
        "shear heat residuals. Together with the named analytic frame lemmas, the "
        "report's analytic general-M extension proves that common origin and a "
        "pointwise residual ratio 1/(M^2+1) do not improve the sharp coefficient "
        "2 or force A_L small; the direct machine anchor is M=16. It does not "
        "assert uniform near rank on the "
        "torus, propagation of equality, nonzero vortex stretching, control of "
        "J_P or the stretching commutator by energy data, an enstrophy estimate, "
        "PDE closure or singularity, and it does not verify the Section 8 "
        "continuation hypotheses from lower-order or initial data. It proves "
        "neither unconditional global regularity nor a solution of the "
        "Millennium problem."
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
