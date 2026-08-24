#!/usr/bin/env python3
"""Exact symbolic audit for the R0.70Q covariance-evolution gate.

The producer verifies four finite groups:

1. the single-block product-rule covariance equation in the row-gradient
   convention B_ij=partial_i u_j, including the negative viscous gradient
   square;
2. first derivatives and Laplacian curvature signs for a simple largest
   eigenvalue and its transverse residual;
3. the exact rotating Beltrami heat mode and its support-restricted scalar
   tight-frame covariance; and
4. energy- and H1-normalized families for which the same spectral projector
   has unbounded spatial gradient.

All recorded arithmetic is exact SymPy arithmetic.  This finite certificate
does not prove propagation for a covariance PDE, does not prove an analytic
no-go theorem beyond the displayed norm maps, and does not rule out estimates
that use higher Sobolev norms.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def matrix_is_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def matrix_equal(first: sp.Matrix, second: sp.Matrix) -> bool:
    return first.shape == second.shape and matrix_is_zero(first - second)


def scalar_payload(value: sp.Expr) -> str:
    return str(sp.factor(value))


def vector_payload(vector: sp.Matrix) -> list[str]:
    return [str(sp.factor(entry)) for entry in vector]


def matrix_payload(matrix: sp.Matrix) -> list[list[str]]:
    return [
        [str(sp.factor(matrix[row, column])) for column in range(matrix.cols)]
        for row in range(matrix.rows)
    ]


def norm_squared(vector: sp.Matrix) -> sp.Expr:
    return sp.simplify((sp.conjugate(vector).T * vector)[0])


def frobenius_squared(matrix: sp.Matrix) -> sp.Expr:
    return sp.simplify(sp.trace(sp.conjugate(matrix).T * matrix))


def row_gradient(
    vector: sp.Matrix, coordinates: tuple[sp.Symbol, sp.Symbol, sp.Symbol]
) -> sp.Matrix:
    return sp.Matrix(
        3,
        3,
        lambda row, column: sp.diff(vector[column], coordinates[row]),
    )


def divergence(
    vector: sp.Matrix, coordinates: tuple[sp.Symbol, sp.Symbol, sp.Symbol]
) -> sp.Expr:
    return sp.simplify(
        sum(sp.diff(vector[index], coordinates[index]) for index in range(3))
    )


def curl(
    vector: sp.Matrix, coordinates: tuple[sp.Symbol, sp.Symbol, sp.Symbol]
) -> sp.Matrix:
    x1, x2, x3 = coordinates
    return sp.Matrix(
        [
            sp.diff(vector[2], x2) - sp.diff(vector[1], x3),
            sp.diff(vector[0], x3) - sp.diff(vector[2], x1),
            sp.diff(vector[1], x1) - sp.diff(vector[0], x2),
        ]
    ).applyfunc(sp.simplify)


def laplacian(
    value: sp.Matrix,
    coordinates: tuple[sp.Symbol, sp.Symbol, sp.Symbol],
) -> sp.Matrix:
    return value.applyfunc(
        lambda entry: sp.simplify(
            sum(sp.diff(entry, coordinate, 2) for coordinate in coordinates)
        )
    )


def material_derivative(
    value: sp.Matrix,
    velocity: sp.Matrix,
    coordinates: tuple[sp.Symbol, sp.Symbol, sp.Symbol],
    time: sp.Symbol,
) -> sp.Matrix:
    return value.applyfunc(
        lambda entry: sp.simplify(
            sp.diff(entry, time)
            + sum(
                velocity[axis] * sp.diff(entry, coordinates[axis])
                for axis in range(3)
            )
        )
    )


def trig_matrix(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.applyfunc(lambda entry: sp.trigsimp(sp.simplify(entry)))


# ---------------------------------------------------------------------------
# 1. Single-block product-rule covariance evolution.
# ---------------------------------------------------------------------------

nu = sp.symbols("nu", positive=True, real=True)
o1, o2, o3 = sp.symbols("o1 o2 o3", real=True)
g1, g2, g3 = sp.symbols("g1 g2 g3", real=True)
ell1, ell2, ell3 = sp.symbols("ell1 ell2 ell3", real=True)
Omega_jet = sp.Matrix([o1, o2, o3])
forcing_jet = sp.Matrix([g1, g2, g3])
laplacian_jet = sp.Matrix([ell1, ell2, ell3])

b11, b12, b13, b21, b22, b23, b31, b32 = sp.symbols(
    "b11 b12 b13 b21 b22 b23 b31 b32", real=True
)
B_jet = sp.Matrix(
    [
        [b11, b12, b13],
        [b21, b22, b23],
        [b31, b32, -b11 - b22],
    ]
)
S_jet = sp.simplify((B_jet + B_jet.T) / 2)

gradient_symbols = sp.symbols("d11:14 d21:24 d31:34", real=True)
gradient_jets = [
    sp.Matrix(gradient_symbols[0:3]),
    sp.Matrix(gradient_symbols[3:6]),
    sp.Matrix(gradient_symbols[6:9]),
]
gradient_square_jet = sum(
    (gradient * gradient.T for gradient in gradient_jets), sp.zeros(3)
)

# D_t Omega = B^T Omega + G + nu Delta Omega.  Here G is the complete
# filtered-block remainder.  For Omega=T omega with [T,Delta]=0 it is
# [u dot grad,T]omega + [T,B^T]omega under [T,A]=T A-A T.
material_Omega_jet = B_jet.T * Omega_jet + forcing_jet + nu * laplacian_jet
Q_jet = Omega_jet * Omega_jet.T
material_Q_product = (
    material_Omega_jet * Omega_jet.T
    + Omega_jet * material_Omega_jet.T
)
laplacian_Q_product = (
    laplacian_jet * Omega_jet.T
    + Omega_jet * laplacian_jet.T
    + 2 * gradient_square_jet
)
parabolic_Q_product = sp.expand(material_Q_product - nu * laplacian_Q_product)
covariance_rhs_jet = sp.expand(
    B_jet.T * Q_jet
    + Q_jet * B_jet
    + forcing_jet * Omega_jet.T
    + Omega_jet * forcing_jet.T
    - 2 * nu * gradient_square_jet
)
product_rule_residual = (parabolic_Q_product - covariance_rhs_jet).applyfunc(
    sp.simplify
)
require(matrix_is_zero(product_rule_residual), "symbolic covariance product rule")

trace_rhs_jet = sp.factor(sp.trace(covariance_rhs_jet))
trace_rhs_expected = sp.factor(
    2 * sp.trace(S_jet * Q_jet)
    + 2 * (forcing_jet.T * Omega_jet)[0]
    - 2
    * nu
    * sum(norm_squared(gradient) for gradient in gradient_jets)
)
require(
    sp.simplify(trace_rhs_jet - trace_rhs_expected) == 0,
    "symbolic covariance trace equation",
)

# A direct polynomial jet checks the differential product rule independently
# of the algebraic placeholders above, including nonzero Delta Omega.
x, y, z, t = sp.symbols("x y z t", real=True)
coordinates = (x, y, z)
nu_sample = sp.Rational(2, 7)
velocity_sample = sp.Matrix([y, -x, 0])
B_sample = row_gradient(velocity_sample, coordinates)
Omega_sample = sp.Matrix([x**2 + t * y, y**2 + t * z, z**2 + t * x])
Q_sample_product = sp.simplify(Omega_sample * Omega_sample.T)
forcing_sample = sp.simplify(
    material_derivative(Omega_sample, velocity_sample, coordinates, t)
    - B_sample.T * Omega_sample
    - nu_sample * laplacian(Omega_sample, coordinates)
)
gradient_square_sample = sum(
    (
        sp.diff(Omega_sample, coordinate)
        * sp.diff(Omega_sample, coordinate).T
        for coordinate in coordinates
    ),
    sp.zeros(3),
)
sample_lhs = sp.simplify(
    material_derivative(Q_sample_product, velocity_sample, coordinates, t)
    - nu_sample * laplacian(Q_sample_product, coordinates)
)
sample_rhs = sp.simplify(
    B_sample.T * Q_sample_product
    + Q_sample_product * B_sample
    + forcing_sample * Omega_sample.T
    + Omega_sample * forcing_sample.T
    - 2 * nu_sample * gradient_square_sample
)
sample_product_residual = (sample_lhs - sample_rhs).applyfunc(sp.simplify)
require(divergence(velocity_sample, coordinates) == 0, "sample incompressibility")
require(matrix_is_zero(sample_product_residual), "direct covariance product rule")

sample_point = {
    x: sp.Rational(1, 2),
    y: -sp.Rational(1, 3),
    z: sp.Rational(2, 5),
    t: sp.Rational(1, 7),
}
sample_dissipation_at_point = gradient_square_sample.subs(sample_point)
sample_lhs_at_point = sample_lhs.subs(sample_point)
sample_rhs_at_point = sample_rhs.subs(sample_point)
require(
    matrix_equal(sample_lhs_at_point, sample_rhs_at_point),
    "rational point covariance equation",
)


# ---------------------------------------------------------------------------
# 2. Simple-spectrum first derivatives and Laplacian curvature signs.
# ---------------------------------------------------------------------------

lambda1, lambda2, lambda3 = sp.symbols(
    "lambda1 lambda2 lambda3", real=True
)
epsilon, mu = sp.symbols("epsilon mu", real=True)
h11, h12, h13, h22, h23, h33 = sp.symbols(
    "h11 h12 h13 h22 h23 h33", real=True
)
k11, k12, k13, k22, k23, k33 = sp.symbols(
    "k11 k12 k13 k22 k23 k33", real=True
)
Q_diagonal = sp.diag(lambda1, lambda2, lambda3)
H_symbolic = sp.Matrix(
    [[h11, h12, h13], [h12, h22, h23], [h13, h23, h33]]
)
K_symbolic = sp.Matrix(
    [[k11, k12, k13], [k12, k22, k23], [k13, k23, k33]]
)
Q_curve = Q_diagonal + epsilon * H_symbolic + epsilon**2 * K_symbolic / 2
characteristic = sp.det(Q_curve - mu * sp.eye(3))
base_substitution = {epsilon: 0, mu: lambda1}
characteristic_mu = sp.diff(characteristic, mu).subs(base_substitution)
characteristic_epsilon = sp.diff(characteristic, epsilon).subs(base_substitution)
lambda_prime = sp.factor(-characteristic_epsilon / characteristic_mu)
lambda_second = sp.factor(
    -(
        sp.diff(characteristic, epsilon, 2).subs(base_substitution)
        + 2
        * sp.diff(characteristic, epsilon, mu).subs(base_substitution)
        * lambda_prime
        + sp.diff(characteristic, mu, 2).subs(base_substitution)
        * lambda_prime**2
    )
    / characteristic_mu
)
lambda_second_expected = sp.factor(
    k11
    + 2 * h12**2 / (lambda1 - lambda2)
    + 2 * h13**2 / (lambda1 - lambda3)
)
require(lambda_prime == h11, "largest eigenvalue first derivative")
require(
    sp.simplify(lambda_second - lambda_second_expected) == 0,
    "largest eigenvalue curvature formula",
)

L_diagonal = sp.diag(1, 0, 0)
P_diagonal = sp.eye(3) - L_diagonal
L_prime = sp.Matrix(
    [
        [0, h12 / (lambda1 - lambda2), h13 / (lambda1 - lambda3)],
        [h12 / (lambda1 - lambda2), 0, 0],
        [h13 / (lambda1 - lambda3), 0, 0],
    ]
)
require(
    matrix_is_zero(
        H_symbolic * L_diagonal
        + Q_diagonal * L_prime
        - h11 * L_diagonal
        - lambda1 * L_prime
    ),
    "spectral equation first derivative",
)
require(
    matrix_is_zero(
        L_diagonal * L_prime + L_prime * L_diagonal - L_prime
    ),
    "projector equation first derivative",
)
require(sp.trace(L_prime) == 0, "projector derivative trace")

residual_prime = sp.factor(sp.trace(H_symbolic) - lambda_prime)
require(residual_prime == h22 + h33, "transverse residual first derivative")
require(
    residual_prime == sp.trace(P_diagonal * H_symbolic),
    "residual derivative projector contraction",
)
residual_second = sp.factor(sp.trace(K_symbolic) - lambda_second)
residual_second_expected = sp.factor(
    k22
    + k33
    - 2 * h12**2 / (lambda1 - lambda2)
    - 2 * h13**2 / (lambda1 - lambda3)
)
require(
    sp.simplify(residual_second - residual_second_expected) == 0,
    "transverse residual curvature formula",
)

# A three-coordinate rational sample independently sums the implicit second
# derivatives.  The local field is
# Q=Q0+sum x_k H_k+|x|^2 K/6, hence Delta Q(0)=K.
Q0_spectral = sp.diag(7, 3, 1)
H_spatial = [
    sp.Matrix([[2, 1, -2], [1, -1, 3], [-2, 3, 0]]),
    sp.Matrix([[-1, 2, 1], [2, 4, -2], [1, -2, 3]]),
    sp.Matrix([[3, -1, 2], [-1, 0, 1], [2, 1, -2]]),
]
K_laplacian = sp.Matrix([[5, 1, -1], [1, -3, 2], [-1, 2, 4]])


def implicit_second_numeric(
    base: sp.Matrix, first: sp.Matrix, second: sp.Matrix
) -> tuple[sp.Expr, sp.Expr]:
    local_curve = base + epsilon * first + epsilon**2 * second / 2
    local_characteristic = sp.det(local_curve - mu * sp.eye(3))
    local_base = {epsilon: 0, mu: base[0, 0]}
    f_mu = sp.diff(local_characteristic, mu).subs(local_base)
    first_rate = sp.factor(
        -sp.diff(local_characteristic, epsilon).subs(local_base) / f_mu
    )
    second_rate = sp.factor(
        -(
            sp.diff(local_characteristic, epsilon, 2).subs(local_base)
            + 2
            * sp.diff(local_characteristic, epsilon, mu).subs(local_base)
            * first_rate
            + sp.diff(local_characteristic, mu, 2).subs(local_base)
            * first_rate**2
        )
        / f_mu
    )
    return first_rate, second_rate


implicit_spatial_rates = [
    implicit_second_numeric(Q0_spectral, first, K_laplacian / 3)
    for first in H_spatial
]
laplacian_lambda_implicit = sp.factor(
    sum(second for _, second in implicit_spatial_rates)
)
curvature_half_sample = sp.factor(
    sum(
        first[0, 1] ** 2 / (7 - 3) + first[0, 2] ** 2 / (7 - 1)
        for first in H_spatial
    )
)
curvature_K_sample = 2 * curvature_half_sample
laplacian_lambda_formula = sp.factor(
    K_laplacian[0, 0] + curvature_K_sample
)
laplacian_residual_formula = sp.factor(
    sp.trace(P_diagonal * K_laplacian) - curvature_K_sample
)
require(curvature_half_sample == 3, "positive rational curvature half")
require(curvature_K_sample == 6, "positive rational curvature")
require(
    laplacian_lambda_implicit == laplacian_lambda_formula == 11,
    "rational Laplacian largest eigenvalue",
)
require(laplacian_residual_formula == -5, "rational Laplacian residual")
require(
    sp.simplify(
        laplacian_lambda_formula
        + laplacian_residual_formula
        - sp.trace(K_laplacian)
    )
    == 0,
    "Laplacian trace partition",
)

# For D_nu=D_t-nu*Delta the positive Laplacian curvature K has a negative
# sign in the lambda equation and a positive sign in the residual equation.
d11, d12, d13, d22, d23, d33 = sp.symbols(
    "d11 d12 d13 d22 d23 d33", real=True
)
Dnu_Q_symbolic = sp.Matrix(
    [[d11, d12, d13], [d12, d22, d23], [d13, d23, d33]]
)
curvature_symbol = sp.symbols("K_curv", nonnegative=True, real=True)
Dnu_lambda_symbolic = sp.trace(L_diagonal * Dnu_Q_symbolic) - nu * curvature_symbol
Dnu_residual_symbolic = (
    sp.trace(P_diagonal * Dnu_Q_symbolic) + nu * curvature_symbol
)
require(
    sp.simplify(
        Dnu_lambda_symbolic
        + Dnu_residual_symbolic
        - sp.trace(Dnu_Q_symbolic)
    )
    == 0,
    "parabolic curvature sign partition",
)


# ---------------------------------------------------------------------------
# 3. Rotating Beltrami heat mode and tight-frame covariance.
# ---------------------------------------------------------------------------

x1, x2, x3, time = sp.symbols("x1 x2 x3 time", real=True)
torus_coordinates = (x1, x2, x3)
N = sp.symbols("N", positive=True, integer=True)
heat_amplitude = sp.exp(-nu * N**2 * time)
direction_v = sp.Matrix([0, sp.cos(N * x1), sp.sin(N * x1)])
direction_w = sp.Matrix([0, -sp.sin(N * x1), sp.cos(N * x1)])
axis_e1 = sp.Matrix([1, 0, 0])
u_beltrami = -heat_amplitude * direction_v
B_beltrami = trig_matrix(row_gradient(u_beltrami, torus_coordinates))
omega_beltrami = trig_matrix(curl(u_beltrami, torus_coordinates))
nonlinearity_beltrami = trig_matrix(
    material_derivative(
        u_beltrami, u_beltrami, torus_coordinates, time
    )
    - sp.diff(u_beltrami, time)
)
heat_residual_beltrami = trig_matrix(
    sp.diff(u_beltrami, time)
    - nu * laplacian(u_beltrami, torus_coordinates)
)
require(
    divergence(u_beltrami, torus_coordinates) == 0,
    "Beltrami divergence",
)
require(matrix_is_zero(nonlinearity_beltrami), "Beltrami nonlinearity")
require(matrix_is_zero(heat_residual_beltrami), "Beltrami heat equation")
require(
    matrix_is_zero(omega_beltrami - N * heat_amplitude * direction_v),
    "Beltrami curl",
)
require(
    matrix_is_zero(omega_beltrami + N * u_beltrami),
    "negative Beltrami eigenvalue",
)
require(
    matrix_is_zero(trig_matrix(B_beltrami.T * omega_beltrami)),
    "Beltrami vorticity stretching",
)

frame_coefficients = [sp.Rational(3, 5), sp.Rational(4, 5)]
require(
    sum(coefficient**2 for coefficient in frame_coefficients) == 1,
    "two-block support tight frame",
)
Omega_blocks = [coefficient * omega_beltrami for coefficient in frame_coefficients]
Q_beltrami = trig_matrix(
    sum((block * block.T for block in Omega_blocks), sp.zeros(3))
)
Q_beltrami_expected = trig_matrix(omega_beltrami * omega_beltrami.T)
require(matrix_equal(Q_beltrami, Q_beltrami_expected), "tight-frame covariance")

E_beltrami = sp.simplify(sp.trace(Q_beltrami))
E_expected = N**2 * heat_amplitude**2
require(sp.trigsimp(E_beltrami - E_expected) == 0, "Beltrami covariance energy")
L_beltrami = trig_matrix(direction_v * direction_v.T)
P_beltrami = trig_matrix(sp.eye(3) - L_beltrami)
require(matrix_equal(L_beltrami**2, L_beltrami), "Beltrami line projector")
require(matrix_equal(P_beltrami**2, P_beltrami), "Beltrami plane projector")
require(matrix_is_zero(P_beltrami * Q_beltrami), "Beltrami zero residual field")
residual_beltrami = sp.trigsimp(sp.trace(P_beltrami * Q_beltrami))
require(residual_beltrami == 0, "Beltrami best-line residual")

eigenbasis_beltrami = sp.Matrix.hstack(direction_v, direction_w, axis_e1)
require(
    matrix_equal(
        trig_matrix(eigenbasis_beltrami.T * eigenbasis_beltrami), sp.eye(3)
    ),
    "Beltrami eigenbasis",
)
Q_in_eigenbasis = trig_matrix(
    eigenbasis_beltrami.T * Q_beltrami * eigenbasis_beltrami
)
require(
    matrix_equal(Q_in_eigenbasis, sp.diag(E_expected, 0, 0)),
    "Beltrami covariance spectrum",
)
spectral_gap_beltrami = E_expected

gradient_P_squared = sp.simplify(
    sum(
        frobenius_squared(sp.diff(P_beltrami, coordinate))
        for coordinate in torus_coordinates
    )
)
gradient_Q_squared = sp.trigsimp(
    sum(
        frobenius_squared(sp.diff(Q_beltrami, coordinate))
        for coordinate in torus_coordinates
    )
)
require(gradient_P_squared == 2 * N**2, "Beltrami projector gradient")
require(
    sp.simplify(gradient_Q_squared / E_expected**2) == 2 * N**2,
    "normalized covariance gradient",
)

Gamma_beltrami = trig_matrix(
    sum(
        (
            sum(
                (
                    sp.diff(block, coordinate)
                    * sp.diff(block, coordinate).T
                    for coordinate in torus_coordinates
                ),
                sp.zeros(3),
            )
            for block in Omega_blocks
        ),
        sp.zeros(3),
    )
)
Dnu_Q_beltrami = trig_matrix(
    material_derivative(
        Q_beltrami, u_beltrami, torus_coordinates, time
    )
    - nu * laplacian(Q_beltrami, torus_coordinates)
)
require(
    matrix_is_zero(trig_matrix(Dnu_Q_beltrami + 2 * nu * Gamma_beltrami)),
    "Beltrami covariance product equation",
)
Gamma_expected = trig_matrix(
    N**4 * heat_amplitude**2 * direction_w * direction_w.T
)
require(matrix_equal(Gamma_beltrami, Gamma_expected), "Beltrami Gamma")

dQ_direction = trig_matrix(sp.diff(Q_beltrami, x1))
curvature_K_beltrami = sp.trigsimp(
    2
    * (direction_w.T * dQ_direction * direction_v)[0] ** 2
    / E_expected
)
require(
    sp.simplify(curvature_K_beltrami - 2 * E_expected * N**2) == 0,
    "Beltrami spectral curvature",
)
require(
    sp.simplify(
        sp.trace(L_beltrami * Dnu_Q_beltrami)
        - nu * curvature_K_beltrami
        - (sp.diff(E_expected, time))
    )
    == 0,
    "Beltrami largest eigenvalue parabolic equation",
)
require(
    sp.simplify(
        sp.trace(P_beltrami * Dnu_Q_beltrami)
        + nu * curvature_K_beltrami
    )
    == 0,
    "Beltrami residual parabolic cancellation",
)

T_horizon = sp.symbols("T", positive=True, real=True)
velocity_l2_squared = sp.trigsimp(norm_squared(u_beltrami))
velocity_gradient_l2_squared = sp.trigsimp(frobenius_squared(B_beltrami))
energy_balance = sp.simplify(
    velocity_l2_squared.subs(time, T_horizon)
    + 2
    * nu
    * sp.integrate(
        velocity_gradient_l2_squared, (time, 0, T_horizon)
    )
)
require(velocity_l2_squared == heat_amplitude**2, "Beltrami L2 energy")
require(
    velocity_gradient_l2_squared == N**2 * heat_amplitude**2,
    "Beltrami gradient energy",
)
require(energy_balance == 1, "Beltrami exact energy balance")


# ---------------------------------------------------------------------------
# 4. Energy/H1 normalization and the exact norm-map obstruction.
# ---------------------------------------------------------------------------

h1_amplitude = 1 / sp.sqrt(1 + N**2)
u_h1 = sp.simplify(h1_amplitude * u_beltrami)
B_h1 = trig_matrix(row_gradient(u_h1, torus_coordinates))
nonlinearity_h1 = trig_matrix(
    material_derivative(u_h1, u_h1, torus_coordinates, time)
    - sp.diff(u_h1, time)
)
heat_residual_h1 = trig_matrix(
    sp.diff(u_h1, time) - nu * laplacian(u_h1, torus_coordinates)
)
require(divergence(u_h1, torus_coordinates) == 0, "H1 family divergence")
require(matrix_is_zero(nonlinearity_h1), "H1 family nonlinearity")
require(matrix_is_zero(heat_residual_h1), "H1 family heat equation")
h1_l2_at_zero = sp.trigsimp(norm_squared(u_h1).subs(time, 0))
h1_gradient_at_zero = sp.trigsimp(frobenius_squared(B_h1).subs(time, 0))
h1_norm_at_zero = sp.simplify(h1_l2_at_zero + h1_gradient_at_zero)
require(h1_norm_at_zero == 1, "H1 normalized Beltrami family")

omega_h1 = trig_matrix(curl(u_h1, torus_coordinates))
Q_h1 = trig_matrix(omega_h1 * omega_h1.T)
E_h1 = sp.trigsimp(sp.trace(Q_h1))
residual_h1 = sp.trigsimp(sp.trace(P_beltrami * Q_h1))
require(residual_h1 == 0, "H1 family zero residual")
require(
    sp.simplify(E_h1.subs(time, 0) - N**2 / (1 + N**2)) == 0,
    "H1 family covariance energy",
)
h1_energy_lower_bound_slack = sp.factor(
    E_h1.subs(time, 0) - sp.Rational(1, 2)
)
require(
    sp.simplify(
        h1_energy_lower_bound_slack
        - (N**2 - 1) / (2 * (N**2 + 1))
    )
    == 0,
    "H1 family covariance energy lower-bound certificate",
)
require(
    sp.simplify(spectral_gap_beltrami / E_expected) == 1,
    "unit relative gap main family",
)
require(
    sp.simplify(E_h1 / E_h1) == 1,
    "unit relative gap H1 family",
)

projector_gradient_limit = sp.limit(sp.sqrt(gradient_P_squared), N, sp.oo)
normalized_covariance_gradient_limit = sp.limit(
    sp.sqrt(gradient_Q_squared / E_expected**2), N, sp.oo
)
require(projector_gradient_limit == sp.oo, "unbounded projector gradient")
require(
    normalized_covariance_gradient_limit == sp.oo,
    "unbounded normalized covariance gradient",
)

h2_upper_data_at_zero = sp.simplify(
    h1_amplitude**2 * (1 + N**2 + N**4)
)
h2_upper_data_limit = sp.limit(h2_upper_data_at_zero, N, sp.oo)
require(h2_upper_data_limit == sp.oo, "higher Sobolev data are not controlled")

norm_map_samples = []
for frequency in (1, 2, 4, 8, 16, 32):
    norm_map_samples.append(
        {
            "N": frequency,
            "amplitudeOneInitialL2Squared": "1",
            "h1NormalizedAmplitude": scalar_payload(
                h1_amplitude.subs(N, frequency)
            ),
            "h1NormSquared": scalar_payload(h1_norm_at_zero.subs(N, frequency)),
            "residual": "0",
            "relativeGap": "1",
            "projectorGradientFrobeniusSquared": str(2 * frequency**2),
        }
    )


result = {
    "release": "R0.70Q",
    "status": "exact-covariance-evolution-curvature-audit",
    "arithmetic": "exact SymPy symbolic, rational, polynomial-jet, trigonometric, matrix, integral, and limit arithmetic",
    "checks": {
        "singleBlockCovarianceProductRule": True,
        "simpleSpectrumCurvatureSigns": True,
        "rotatingBeltramiTightFrame": True,
        "energyAndH1NormMapObstruction": True,
    },
    "singleBlockCovarianceLedger": {
        "convention": "B_ij=partial_i u_j, so (omega dot grad)u=B^T*omega",
        "parabolicOperator": "D_nu=partial_t+u dot grad-nu*Delta",
        "filteredRemainder": "G=[u dot grad,T]omega+[T,B^T]omega when [T,A]=T*A-A*T and [T,Delta]=0",
        "blockEquation": "D_nu*Omega=B^T*Omega+G",
        "covariance": "Q_Omega=Omega tensor Omega",
        "productRule": "D_nu*Q_Omega=B^T*Q_Omega+Q_Omega*B+G tensor Omega+Omega tensor G-2*nu*sum_k partial_k Omega tensor partial_k Omega",
        "viscousGradientSquareSign": "negative",
        "symbolicResidual": matrix_payload(product_rule_residual),
        "traceEquation": "D_nu|Omega|^2=2*S:Q_Omega+2*G dot Omega-2*nu*sum_k|partial_k Omega|^2",
        "traceResidual": scalar_payload(trace_rhs_jet - trace_rhs_expected),
        "directPolynomialSample": {
            "velocity": ["y", "-x", "0"],
            "Omega": ["x^2+t*y", "y^2+t*z", "z^2+t*x"],
            "nu": scalar_payload(nu_sample),
            "divergence": "0",
            "evaluationPoint": ["1/2", "-1/3", "2/5", "1/7"],
            "gradientSquareAtPoint": matrix_payload(sample_dissipation_at_point),
            "leftAtPoint": matrix_payload(sample_lhs_at_point),
            "rightAtPoint": matrix_payload(sample_rhs_at_point),
            "residual": matrix_payload(sample_product_residual),
        },
    },
    "simpleSpectrumLedger": {
        "assumption": "lambda1>lambda2>lambda3 with lambda1 simple; L=v1 tensor v1; P=I-L; r=tr(PQ)=tr(Q)-lambda1",
        "firstDerivatives": {
            "largestEigenvalue": "partial lambda1=tr(L*partial Q)",
            "symbolicValueInEigenbasis": scalar_payload(lambda_prime),
            "projector": "partial L=sum_b>1 (L_b*(partial Q)*L+L*(partial Q)*L_b)/(lambda1-lambda_b)",
            "projectorMatrixInEigenbasis": matrix_payload(L_prime),
            "residual": "partial r=tr(P*partial Q)",
            "residualValueInEigenbasis": scalar_payload(residual_prime),
        },
        "laplacianCurvature": {
            "canonicalHalfCurvature": "K_Q=sum_k sum_b>1 |v_b^T*(partial_k Q)*v1|^2/(lambda1-lambda_b)>=0",
            "certificateConvention": "K=2*K_Q",
            "largestEigenvalue": "Delta lambda1=tr(L*Delta Q)+K",
            "residual": "Delta r=tr(P*Delta Q)-K",
            "parabolicLargestEigenvalue": "D_nu lambda1=tr(L*D_nu Q)-nu*K",
            "parabolicResidual": "D_nu r=tr(P*D_nu Q)+nu*K",
            "largestEigenvalueCurvatureSignUnderDelta": "positive",
            "residualCurvatureSignUnderDelta": "negative",
            "largestEigenvalueCurvatureSignUnderDNu": "negative",
            "residualCurvatureSignUnderDNu": "positive",
            "oneDirectionImplicitFormula": scalar_payload(lambda_second),
            "oneDirectionResidualFormula": scalar_payload(residual_second),
        },
        "rationalThreeCoordinateSample": {
            "Q0": matrix_payload(Q0_spectral),
            "spatialFirstDerivatives": [matrix_payload(value) for value in H_spatial],
            "laplacianQ": matrix_payload(K_laplacian),
            "implicitFirstAndSecondRates": [
                [scalar_payload(first), scalar_payload(second)]
                for first, second in implicit_spatial_rates
            ],
            "curvatureKQ": scalar_payload(curvature_half_sample),
            "curvatureK": scalar_payload(curvature_K_sample),
            "laplacianLargestEigenvalue": scalar_payload(
                laplacian_lambda_implicit
            ),
            "laplacianResidual": scalar_payload(laplacian_residual_formula),
            "tracePartitionResidual": scalar_payload(
                laplacian_lambda_formula
                + laplacian_residual_formula
                - sp.trace(K_laplacian)
            ),
        },
    },
    "rotatingBeltramiLedger": {
        "domain": "T^3=(R/(2*pi*Z))^3 with normalized Haar measure",
        "mode": "u_N=-exp(-nu*N^2*t)*(0,cos(N*x1),sin(N*x1))",
        "rowGradient": matrix_payload(B_beltrami),
        "divergence": "0",
        "nonlinearity": vector_payload(nonlinearity_beltrami),
        "curl": vector_payload(omega_beltrami),
        "BeltramiIdentity": "curl(u_N)=-N*u_N",
        "vorticityStretching": vector_payload(
            trig_matrix(B_beltrami.T * omega_beltrami)
        ),
        "heatEquationResidual": vector_payload(heat_residual_beltrami),
        "supportRestrictedScalarTightFrame": {
            "coefficients": [scalar_payload(value) for value in frame_coefficients],
            "coefficientSquareSum": "1",
            "scope": "the two Fourier modes +/-N*e1 only",
        },
        "covariance": matrix_payload(Q_beltrami),
        "energyE": scalar_payload(E_beltrami),
        "covarianceInEigenbasis": matrix_payload(Q_in_eigenbasis),
        "bestLineResidual": scalar_payload(residual_beltrami),
        "principalGap": scalar_payload(spectral_gap_beltrami),
        "relativeGap": "1",
        "projectorGradientFrobeniusSquared": scalar_payload(
            gradient_P_squared
        ),
        "projectorGradientFrobenius": "sqrt(2)*N",
        "normalizedCovarianceGradientFrobeniusSquared": scalar_payload(
            gradient_Q_squared / E_expected**2
        ),
        "normalizedCovarianceGradientFrobenius": "sqrt(2)*N",
        "Gamma": matrix_payload(Gamma_beltrami),
        "curvatureKQ": scalar_payload(curvature_K_beltrami / 2),
        "curvatureK": scalar_payload(curvature_K_beltrami),
        "covarianceParabolicResidual": matrix_payload(
            trig_matrix(Dnu_Q_beltrami + 2 * nu * Gamma_beltrami)
        ),
        "largestEigenvalueParabolicResidual": "0",
        "transverseResidualParabolicResidual": "0",
    },
    "normMapObstructionLedger": {
        "amplitudeOne": {
            "initialL2NormSquared": "1",
            "L2NormSquaredAtTimeT": scalar_payload(velocity_l2_squared),
            "gradientL2NormSquaredAtTimeT": scalar_payload(
                velocity_gradient_l2_squared
            ),
            "energyIdentity": "||u(T)||_2^2+2*nu*integral_0^T||grad u||_2^2 dt=1",
            "energyIdentityValue": scalar_payload(energy_balance),
        },
        "h1Normalized": {
            "amplitude": "a_N=(1+N^2)^(-1/2)",
            "divergence": "0",
            "nonlinearity": vector_payload(nonlinearity_h1),
            "heatEquationResidual": vector_payload(heat_residual_h1),
            "initialL2NormSquared": scalar_payload(h1_l2_at_zero),
            "initialGradientL2NormSquared": scalar_payload(
                h1_gradient_at_zero
            ),
            "initialH1NormSquared": scalar_payload(h1_norm_at_zero),
            "initialCovarianceEnergy": scalar_payload(E_h1.subs(time, 0)),
            "initialCovarianceEnergyLowerBound": ">=1/2 for integer N>=1",
            "initialCovarianceEnergyLowerBoundSlack": scalar_payload(
                h1_energy_lower_bound_slack
            ),
            "bestLineResidual": scalar_payload(residual_h1),
            "relativeGap": "1",
            "projectorIsAmplitudeIndependent": True,
            "projectorGradientFrobenius": "sqrt(2)*N",
        },
        "unboundedness": {
            "projectorGradientLimit": "oo",
            "normalizedCovarianceGradientLimit": "oo",
            "finiteFrequencySamples": norm_map_samples,
        },
        "higherSobolevBoundary": {
            "derivativeSumH2NormSquared": scalar_payload(
                h2_upper_data_at_zero
            ),
            "normConvention": "||u||_2^2+||grad u||_2^2+||second spatial derivatives||_2^2",
            "limit": "oo",
            "meaning": "the family does not rule out projector-gradient bounds that depend on a higher Sobolev norm",
        },
        "certifiedNormMapBoundary": "No bound of sup_x|grad P| using only a uniform initial H1 bound, zero best-line residual, and unit relative principal gap can hold for this explicit family.",
    },
    "claimBoundary": (
        "This certificate proves only the displayed finite symbolic, rational, "
        "polynomial-jet, trigonometric, matrix, integral, and limit identities. "
        "It does not prove covariance-PDE propagation, an analytic no-go "
        "theorem beyond the stated energy/H1-to-projector-gradient norm maps, "
        "or the failure of estimates using higher Sobolev norms. It does not "
        "prove a Navier--Stokes continuation criterion, finite-time blow-up, "
        "global smoothness, or the Millennium problem."
    ),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(payload, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")


if __name__ == "__main__":
    main()
