#!/usr/bin/env python3
"""Exact finite audit for the R0.70P harmonic/projector bridge gate.

The producer verifies five finite groups:

1. the orientation-free rank-one-projector identity for a symbolic
   trace-free velocity-gradient family;
2. exact periodic trigonometric/Fourier integration-by-parts examples;
3. the finite Rademacher orthogonality identity;
4. bounded-weight square-function scaling and an exact unbounded-weight
   near-single-frequency commutator obstruction; and
5. finite-dimensional reconstruction/commutator bridge inequalities,
   including fixed adversarial and pseudorandom rational cases.

Every recorded value is exact SymPy arithmetic.  This finite audit does not
prove a Calderon reproducing theorem, an infinite-dimensional multiplier or
commutator theorem, or a Navier--Stokes continuation theorem.
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
from pathlib import Path

import sympy as sp


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def matrix_is_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def matrix_equal(first: sp.Matrix, second: sp.Matrix) -> bool:
    return first.shape == second.shape and matrix_is_zero(first - second)


def matrix_payload(matrix: sp.Matrix) -> list[list[str]]:
    return [
        [str(sp.factor(matrix[row, column])) for column in range(matrix.cols)]
        for row in range(matrix.rows)
    ]


def vector_payload(vector: sp.Matrix) -> list[str]:
    return [str(sp.factor(entry)) for entry in vector]


def scalar_payload(value: sp.Expr) -> str:
    return str(sp.factor(value))


def norm_squared(vector: sp.Matrix) -> sp.Expr:
    return sp.simplify((sp.conjugate(vector).T * vector)[0])


def normalized_average_2d(expression: sp.Expr, x: sp.Symbol, y: sp.Symbol) -> sp.Expr:
    return sp.simplify(
        sp.integrate(
            sp.expand_trig(expression),
            (x, 0, 2 * sp.pi),
            (y, 0, 2 * sp.pi),
        )
        / (2 * sp.pi) ** 2
    )


def normalized_average_1d(expression: sp.Expr, x: sp.Symbol) -> sp.Expr:
    return sp.simplify(
        sp.integrate(sp.expand_trig(expression), (x, 0, 2 * sp.pi))
        / (2 * sp.pi)
    )


def curl_from_row_gradient(matrix: sp.Matrix) -> sp.Matrix:
    """Curl for B_ij = partial_i u_j."""

    return sp.Matrix(
        [
            matrix[1, 2] - matrix[2, 1],
            matrix[2, 0] - matrix[0, 2],
            matrix[0, 1] - matrix[1, 0],
        ]
    )


def projector_identity_terms(
    matrix: sp.Matrix, line_projector: sp.Matrix
) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    strain = (matrix + matrix.T) / 2
    transverse = sp.eye(3) - line_projector
    vorticity = curl_from_row_gradient(matrix)
    left = sp.simplify(
        sp.trace(line_projector * strain**2)
        - norm_squared(transverse * vorticity) / 4
    )
    right = sp.simplify(
        sum(
            matrix[i, j] * matrix[k, i] * line_projector[j, k]
            for i in range(3)
            for j in range(3)
            for k in range(3)
        )
    )
    residual = sp.factor(sp.together(left - right))
    residual = sp.trigsimp(residual)
    return left, right, residual


# ---------------------------------------------------------------------------
# 1. Symbolic orientation-free projector identity.
# ---------------------------------------------------------------------------

b11, b12, b13, b21, b22, b23, b31, b32 = sp.symbols(
    "b11 b12 b13 b21 b22 b23 b31 b32", real=True
)
B_symbolic = sp.Matrix(
    [
        [b11, b12, b13],
        [b21, b22, b23],
        [b31, b32, -b11 - b22],
    ]
)
p, q = sp.symbols("p q", real=True)
stereographic_denominator = 1 + p**2 + q**2
v_symbolic = sp.Matrix(
    [
        (1 - p**2 - q**2) / stereographic_denominator,
        2 * p / stereographic_denominator,
        2 * q / stereographic_denominator,
    ]
)
L_symbolic = sp.simplify(v_symbolic * v_symbolic.T)
P_symbolic = sp.simplify(sp.eye(3) - L_symbolic)

require(sp.trace(B_symbolic) == 0, "symbolic gradient is trace-free")
require(sp.simplify(norm_squared(v_symbolic)) == 1, "symbolic unit line lift")
require(matrix_equal(L_symbolic**2, L_symbolic), "symbolic line projector")
require(matrix_equal(P_symbolic**2, P_symbolic), "symbolic transverse projector")
require(matrix_is_zero(L_symbolic * P_symbolic), "symbolic complementary projectors")
require(sp.simplify(sp.trace(L_symbolic)) == 1, "symbolic line rank")
require(sp.simplify(sp.trace(P_symbolic)) == 2, "symbolic transverse rank")

projector_left, projector_right, projector_residual = projector_identity_terms(
    B_symbolic, L_symbolic
)
require(projector_residual == 0, "symbolic projector identity")

sample_gradients = [
    sp.Matrix([[1, 2, -1], [3, -2, 4], [0, 5, 1]]),
    sp.Matrix([[0, 1, 2], [-3, 4, 1], [5, -2, -4]]),
    sp.Matrix([[2, -1, 3], [4, -5, 0], [-2, 7, 3]]),
]
sample_lifts = [
    sp.Matrix([0, 0, 1]),
    sp.Matrix([sp.Rational(2, 3), sp.Rational(2, 3), sp.Rational(1, 3)]),
    v_symbolic.subs({p: sp.Rational(1, 2), q: -sp.Rational(1, 3)}),
]
projector_samples: list[dict[str, object]] = []
for index, (gradient, lift) in enumerate(zip(sample_gradients, sample_lifts), 1):
    require(sp.trace(gradient) == 0, f"sample {index} trace-free")
    require(sp.simplify(norm_squared(lift)) == 1, f"sample {index} unit lift")
    line_projector = sp.simplify(lift * lift.T)
    left, right, residual = projector_identity_terms(gradient, line_projector)
    require(residual == 0, f"sample {index} projector identity")
    projector_samples.append(
        {
            "gradient": matrix_payload(gradient),
            "lift": vector_payload(lift),
            "lineProjector": matrix_payload(line_projector),
            "left": scalar_payload(left),
            "right": scalar_payload(right),
            "residual": scalar_payload(residual),
        }
    )


# ---------------------------------------------------------------------------
# 2. Periodic Fourier/trigonometric integration by parts.
# ---------------------------------------------------------------------------

x, y, z = sp.symbols("x y z", real=True)
coordinates = (x, y, z)
u_periodic = sp.Matrix([sp.sin(y), sp.sin(x), 0])
B_periodic = sp.Matrix(
    3,
    3,
    lambda row, column: sp.diff(u_periodic[column], coordinates[row]),
)
S_periodic = sp.simplify((B_periodic + B_periodic.T) / 2)
omega_periodic = curl_from_row_gradient(B_periodic)
divergence_periodic = sp.simplify(sp.trace(B_periodic))
require(divergence_periodic == 0, "periodic sample is divergence-free")


def periodic_case(line_projector: sp.Matrix, label: str) -> dict[str, object]:
    transverse = sp.simplify(sp.eye(3) - line_projector)
    pointwise_left, pointwise_right, pointwise_residual = projector_identity_terms(
        B_periodic, line_projector
    )
    require(pointwise_residual == 0, f"{label} pointwise identity")
    correction = sp.simplify(
        -sum(
            u_periodic[j]
            * B_periodic[k, i]
            * sp.diff(line_projector[j, k], coordinates[i])
            for i in range(3)
            for j in range(3)
            for k in range(3)
        )
    )
    right_average = normalized_average_2d(pointwise_right, x, y)
    correction_average = normalized_average_2d(correction, x, y)
    strain_average = normalized_average_2d(
        sp.trace(line_projector * S_periodic**2), x, y
    )
    transverse_average = normalized_average_2d(
        norm_squared(transverse * omega_periodic) / 4, x, y
    )
    require(
        sp.simplify(right_average - correction_average) == 0,
        f"{label} integration by parts",
    )
    require(
        sp.simplify(strain_average - transverse_average - right_average) == 0,
        f"{label} integrated projector identity",
    )
    return {
        "pointwiseRight": str(sp.trigsimp(pointwise_right)),
        "integrationByPartsCorrection": str(sp.trigsimp(correction)),
        "rightAverage": scalar_payload(right_average),
        "correctionAverage": scalar_payload(correction_average),
        "strainAverage": scalar_payload(strain_average),
        "quarterTransverseVorticityAverage": scalar_payload(transverse_average),
        "integratedResidual": scalar_payload(
            strain_average - transverse_average - right_average
        ),
    }


constant_lift = sp.Matrix(
    [sp.Rational(2, 3), sp.Rational(2, 3), sp.Rational(1, 3)]
)
L_constant = constant_lift * constant_lift.T
constant_periodic_case = periodic_case(L_constant, "constant projector")
require(constant_periodic_case["rightAverage"] == "0", "constant projector zero I")
require(constant_periodic_case["strainAverage"] == "2/9", "constant projector strain")
require(
    constant_periodic_case["quarterTransverseVorticityAverage"] == "2/9",
    "constant projector transverse vorticity",
)

# This local lift changes sign after one x- or y-period, while L is periodic.
# It is therefore a useful finite orientation-free test of the projector formula.
half_angle = (x + y) / 2
local_lift = sp.Matrix([sp.cos(half_angle), 0, sp.sin(half_angle)])
L_variable = sp.simplify(local_lift * local_lift.T)
require(
    matrix_equal(L_variable.subs(x, x + 2 * sp.pi), L_variable),
    "variable projector is x-periodic",
)
require(
    matrix_equal(L_variable.subs(y, y + 2 * sp.pi), L_variable),
    "variable projector is y-periodic",
)
require(
    matrix_equal(
        local_lift.subs(x, x + 2 * sp.pi),
        -local_lift,
    ),
    "local lift changes sign around x-cycle",
)
variable_periodic_case = periodic_case(L_variable, "variable projector")
require(variable_periodic_case["rightAverage"] == "1/8", "variable projector I")
require(
    variable_periodic_case["correctionAverage"] == "1/8",
    "variable projector correction",
)
require(variable_periodic_case["strainAverage"] == "3/16", "variable strain")
require(
    variable_periodic_case["quarterTransverseVorticityAverage"] == "1/16",
    "variable transverse vorticity",
)


# ---------------------------------------------------------------------------
# 3. Finite Rademacher orthogonality.
# ---------------------------------------------------------------------------

g11, g22, g33, g44, g12, g13, g14, g23, g24, g34 = sp.symbols(
    "g11 g22 g33 g44 g12 g13 g14 g23 g24 g34", real=True
)
gram_symbolic = sp.Matrix(
    [
        [g11, g12, g13, g14],
        [g12, g22, g23, g24],
        [g13, g23, g33, g34],
        [g14, g24, g34, g44],
    ]
)
rademacher_signs = list(itertools.product((-1, 1), repeat=4))
rademacher_average_symbolic = sp.simplify(
    sum(
        (sp.Matrix(signs).T * gram_symbolic * sp.Matrix(signs))[0]
        for signs in rademacher_signs
    )
    / len(rademacher_signs)
)
require(
    sp.simplify(rademacher_average_symbolic - sp.trace(gram_symbolic)) == 0,
    "symbolic Rademacher orthogonality",
)
rademacher_moments = sp.Matrix(
    4,
    4,
    lambda row, column: sp.Rational(
        sum(signs[row] * signs[column] for signs in rademacher_signs),
        len(rademacher_signs),
    ),
)
require(matrix_equal(rademacher_moments, sp.eye(4)), "Rademacher sign moments")

rademacher_vectors = [
    sp.Matrix([sp.Rational(1, 2), -sp.Rational(1, 3), 2]),
    sp.Matrix([-sp.Rational(2, 5), sp.Rational(3, 4), sp.Rational(1, 6)]),
    sp.Matrix([sp.Rational(7, 8), 0, -sp.Rational(1, 2)]),
    sp.Matrix([sp.Rational(1, 3), sp.Rational(5, 7), -sp.Rational(4, 9)]),
]
rademacher_gram = sp.Matrix(
    4,
    4,
    lambda row, column: sp.simplify(
        (rademacher_vectors[row].T * rademacher_vectors[column])[0]
    ),
)
rademacher_sample_average = sp.simplify(
    sum(
        norm_squared(
            sum(
                (signs[index] * rademacher_vectors[index] for index in range(4)),
                sp.zeros(3, 1),
            )
        )
        for signs in rademacher_signs
    )
    / len(rademacher_signs)
)
rademacher_square_sum = sp.simplify(
    sum(norm_squared(vector) for vector in rademacher_vectors)
)
require(
    rademacher_sample_average == rademacher_square_sum,
    "rational-vector Rademacher identity",
)


# ---------------------------------------------------------------------------
# 4. Bounded and unbounded square-function weight scaling.
# ---------------------------------------------------------------------------

bounded_component_squares = [
    sp.Rational(1, 7),
    sp.Rational(5, 12),
    sp.Rational(9, 20),
    sp.Rational(2, 3),
]
bounded_weights = [
    sp.Rational(1, 5),
    sp.Rational(2, 3),
    sp.Rational(7, 8),
    sp.Rational(1, 1),
]
bounded_W = sp.Integer(1)
bounded_unweighted_sum = sum(bounded_component_squares)
bounded_weighted_sum = sum(
    weight * component
    for weight, component in zip(bounded_weights, bounded_component_squares)
)
bounded_slack = sp.simplify(
    bounded_W * bounded_unweighted_sum - bounded_weighted_sum
)
require(all(weight <= bounded_W for weight in bounded_weights), "bounded weights")
require(bounded_slack >= 0, "bounded weight exact slack")
require(
    sp.simplify(
        bounded_slack
        - sum(
            (bounded_W - weight) * component
            for weight, component in zip(
                bounded_weights, bounded_component_squares
            )
        )
    )
    == 0,
    "bounded weight slack decomposition",
)
symbolic_component_squares = sp.symbols("c1sq c2sq c3sq c4sq", nonnegative=True)
symbolic_weights = sp.symbols("w1 w2 w3 w4", nonnegative=True)
symbolic_W = sp.symbols("W", nonnegative=True)
bounded_weight_symbolic_residual = sp.simplify(
    symbolic_W * sum(symbolic_component_squares)
    - sum(
        symbolic_weights[index] * symbolic_component_squares[index]
        for index in range(4)
    )
    - sum(
        (symbolic_W - symbolic_weights[index])
        * symbolic_component_squares[index]
        for index in range(4)
    )
)
require(bounded_weight_symbolic_residual == 0, "symbolic bounded-weight identity")

# Exact near-single-frequency projector commutator.  Work on the normalized
# one-dimensional torus, take v=(0,cos x,sin x), P=I-v v^T, and
# f_n=n exp(i n x)e_2.  The projector has only frequency shifts 0,+/-2.
n = sp.symbols("n", positive=True, integer=True)
k = sp.symbols("k", real=True)
r = sp.symbols("r", real=True)
phi = 2 * r / (1 + r**2)
scale_R = 2 * n


def scaled_multiplier(frequency: sp.Expr) -> sp.Expr:
    return sp.factor(
        2 * (frequency / scale_R) / (1 + (frequency / scale_R) ** 2)
    )


multiplier_at_n = scaled_multiplier(n)
multiplier_delta_plus = sp.factor(scaled_multiplier(n + 2) - multiplier_at_n)
multiplier_delta_minus = sp.factor(scaled_multiplier(n - 2) - multiplier_at_n)
projector_commutator_norm_squared = sp.factor(
    n**2
    * sp.Rational(1, 8)
    * (multiplier_delta_plus**2 + multiplier_delta_minus**2)
)
projector_commutator_limit = sp.limit(
    projector_commutator_norm_squared, n, sp.oo
)
require(
    sp.simplify(projector_commutator_limit - sp.Rational(144, 625)) == 0,
    "projector commutator positive limit",
)
phi_bound_identity = sp.factor(1 - phi**2)
require(
    sp.simplify(phi_bound_identity - (1 - r**2) ** 2 / (1 + r**2) ** 2)
    == 0,
    "bounded multiplier profile",
)
phi_derivative_at_half = sp.simplify(sp.diff(phi, r).subs(r, sp.Rational(1, 2)))
require(phi_derivative_at_half == sp.Rational(24, 25), "profile derivative")

commutator_limit_slack = sp.factor(
    projector_commutator_norm_squared - sp.Rational(144, 625)
)
slack_numerator = sp.factor(
    sp.together(commutator_limit_slack).as_numer_denom()[0]
)
slack_denominator = sp.factor(
    sp.together(commutator_limit_slack).as_numer_denom()[1]
)
expected_slack_core = 4075 * n**6 + 1604 * n**4 - 1328 * n**2 - 576
require(
    sp.simplify(slack_numerator - 64 * expected_slack_core) == 0,
    "commutator lower-bound numerator",
)
require(
    sp.simplify(
        slack_denominator
        - 625 * (5 * n**2 - 4 * n + 4) ** 2 * (5 * n**2 + 4 * n + 4) ** 2
    )
    == 0,
    "commutator lower-bound denominator",
)
denominator_minus_positivity = sp.expand(
    5 * (n - sp.Rational(2, 5)) ** 2 + sp.Rational(16, 5)
)
denominator_plus_positivity = sp.expand(
    5 * (n + sp.Rational(2, 5)) ** 2 + sp.Rational(16, 5)
)
require(
    denominator_minus_positivity == 5 * n**2 - 4 * n + 4,
    "commutator minus denominator positivity certificate",
)
require(
    denominator_plus_positivity == 5 * n**2 + 4 * n + 4,
    "commutator plus denominator positivity certificate",
)
t = sp.symbols("t", nonnegative=True)
positive_slack_polynomial = sp.expand(
    (4075 * (t + 1) ** 3 + 1604 * (t + 1) ** 2 - 1328 * (t + 1) - 576)
)
require(
    positive_slack_polynomial
    == 4075 * t**3 + 13829 * t**2 + 14105 * t + 3775,
    "commutator lower-bound positive polynomial",
)
require(
    all(coefficient > 0 for coefficient in sp.Poly(positive_slack_polynomial, t).all_coeffs()),
    "commutator lower-bound positive coefficients",
)
require(slack_numerator != 0, "strict commutator lower bound")

unbounded_weighted_limit = sp.limit(
    n * projector_commutator_norm_squared, n, sp.oo
)
require(unbounded_weighted_limit == sp.oo, "unbounded weights destroy uniformity")

projector_frequency_samples = []
# The subsequence n=2^(J-1) makes the scale 2*n exactly dyadic: the multiplier
# above is T_J=phi(2^(-J)D), and the choice w_J=n is unbounded.
for frequency in (2, 4, 8, 16, 32):
    norm_square = sp.factor(projector_commutator_norm_squared.subs(n, frequency))
    require(norm_square > sp.Rational(144, 625), f"frequency {frequency} lower bound")
    projector_frequency_samples.append(
        {
            "n": frequency,
            "commutatorNormSquared": scalar_payload(norm_square),
            "weight": str(frequency),
            "weightedContributionSquared": scalar_payload(frequency * norm_square),
        }
    )

x_one = sp.symbols("x_one", real=True)
commutator_lift = sp.Matrix([0, sp.cos(x_one), sp.sin(x_one)])
commutator_projector = sp.simplify(
    sp.eye(3) - commutator_lift * commutator_lift.T
)
commutator_projector_derivative = sp.diff(commutator_projector, x_one)
require(
    sp.simplify(
        sp.trace(
            commutator_projector_derivative.T * commutator_projector_derivative
        )
    )
    == 2,
    "projector derivative Frobenius norm",
)
commutator_e2 = sp.Matrix([0, 1, 0])
projector_e2 = sp.simplify(commutator_projector * commutator_e2)
projector_shift_zero = sp.Matrix([0, sp.Rational(1, 2), 0])
projector_shift_plus = sp.Matrix([0, -sp.Rational(1, 4), sp.I / 4])
projector_shift_minus = sp.Matrix([0, -sp.Rational(1, 4), -sp.I / 4])
projector_fourier_reconstruction = (
    projector_shift_zero
    + projector_shift_plus * sp.exp(2 * sp.I * x_one)
    + projector_shift_minus * sp.exp(-2 * sp.I * x_one)
)
require(
    matrix_is_zero(
        (projector_e2 - projector_fourier_reconstruction).applyfunc(
            lambda entry: sp.simplify(sp.expand_complex(entry))
        )
    ),
    "projector exact frequency shifts",
)
require(norm_squared(projector_shift_plus) == sp.Rational(1, 8), "plus shift mass")
require(norm_squared(projector_shift_minus) == sp.Rational(1, 8), "minus shift mass")
commutator_from_coefficients = sp.factor(
    n**2
    * (
        multiplier_delta_plus**2 * norm_squared(projector_shift_plus)
        + multiplier_delta_minus**2 * norm_squared(projector_shift_minus)
    )
)
require(
    sp.simplify(
        commutator_from_coefficients - projector_commutator_norm_squared
    )
    == 0,
    "commutator norm from exact Fourier coefficients",
)
input_hminusone_norm_squared = sp.simplify(n**2 * n ** (-2))
require(input_hminusone_norm_squared == 1, "near-frequency input H-minus-one norm")


# ---------------------------------------------------------------------------
# 5. Finite-dimensional harmonic bridge checks.
# ---------------------------------------------------------------------------

coordinate_filters = [
    sp.diag(1, 0, 0),
    sp.diag(0, 1, 0),
    sp.diag(0, 0, 1),
]
require(
    matrix_equal(
        sum((filter_matrix**2 for filter_matrix in coordinate_filters), sp.zeros(3)),
        sp.eye(3),
    ),
    "finite tight-frame reconstruction",
)
h_symbols = sp.symbols("h11 h12 h13 h21 h22 h23 h31 h32 h33", real=True)
h_blocks = [
    sp.Matrix(h_symbols[0:3]),
    sp.Matrix(h_symbols[3:6]),
    sp.Matrix(h_symbols[6:9]),
]
synthesized_h = sum(
    (
        coordinate_filters[index] * h_blocks[index]
        for index in range(3)
    ),
    sp.zeros(3, 1),
)
synthesis_square_slack = sp.factor(
    sum(norm_squared(block) for block in h_blocks) - norm_squared(synthesized_h)
)
expected_synthesis_slack = (
    h_symbols[1] ** 2
    + h_symbols[2] ** 2
    + h_symbols[3] ** 2
    + h_symbols[5] ** 2
    + h_symbols[6] ** 2
    + h_symbols[7] ** 2
)
require(
    sp.simplify(synthesis_square_slack - expected_synthesis_slack) == 0,
    "finite synthesis constant one",
)

# The periodic harmonic bridge needs T_star=Pi_0 because multiplication by a
# variable projector can create a zero mode even when vorticity is mean-zero.
zero_mode_velocity = sp.Matrix([0, 0, -sp.sin(2 * x_one) / 2])
zero_mode_gradient = sp.Matrix(
    3,
    3,
    lambda row, column: (
        sp.diff(zero_mode_velocity[column], x_one) if row == 0 else 0
    ),
)
zero_mode_input = curl_from_row_gradient(zero_mode_gradient)
require(
    matrix_equal(zero_mode_input, sp.Matrix([0, sp.cos(2 * x_one), 0])),
    "zero-mode sample is an exact periodic vorticity",
)
require(sp.trace(zero_mode_gradient) == 0, "zero-mode velocity is divergence-free")
zero_mode_input_mean = zero_mode_input.applyfunc(
    lambda entry: normalized_average_1d(entry, x_one)
)
zero_mode_projected = sp.simplify(commutator_projector * zero_mode_input)
zero_mode_projected_mean = zero_mode_projected.applyfunc(
    lambda entry: normalized_average_1d(entry, x_one)
)
zero_mode_commutator = sp.simplify(
    zero_mode_projected_mean - commutator_projector * zero_mode_input_mean
)
require(matrix_is_zero(zero_mode_input_mean), "mean-zero vorticity mode")
require(
    matrix_equal(
        zero_mode_commutator,
        zero_mode_projected_mean,
    ),
    "zero-mode commutator identity",
)
require(
    matrix_equal(
        zero_mode_projected_mean,
        sp.Matrix([0, -sp.Rational(1, 4), 0]),
    ),
    "variable projector creates a zero mode",
)

zero_mode_oscillatory_coefficient = sp.simplify(
    commutator_projector[1, 1]
    - normalized_average_1d(commutator_projector[1, 1], x_one)
)
zero_mode_pairing = normalized_average_1d(
    zero_mode_oscillatory_coefficient * zero_mode_input[1], x_one
)
zero_mode_hminusone_squared = sp.Rational(1, 8)
zero_mode_hone_squared = normalized_average_1d(
    sp.diff(zero_mode_oscillatory_coefficient, x_one) ** 2, x_one
)
zero_mode_duality_slack = sp.simplify(
    zero_mode_hminusone_squared * zero_mode_hone_squared
    - zero_mode_pairing**2
)
require(
    sp.trigsimp(zero_mode_oscillatory_coefficient)
    == -sp.cos(2 * x_one) / 2,
    "zero-mode oscillatory coefficient",
)
require(zero_mode_pairing == -sp.Rational(1, 4), "zero-mode pairing")
require(zero_mode_hone_squared == sp.Rational(1, 2), "zero-mode H-one norm")
require(zero_mode_duality_slack == 0, "zero-mode H-minus-one H-one equality")
zero_mode_commutator_norm_squared = norm_squared(zero_mode_commutator)
require(
    zero_mode_commutator_norm_squared == sp.Rational(1, 16),
    "zero-mode commutator norm",
)

# The covariance ledger uses Omega_star=Pi_0*omega, Q_star=Omega_star tensor
# Omega_star, and residual contribution ||P*Omega_star||_2^2.  All three
# direct constant-block terms vanish for periodic vorticity even though the
# reconstruction commutator above need not vanish.
Omega_star = zero_mode_input_mean
Qstar_covariance = sp.simplify(Omega_star * Omega_star.T)
Rstar_residual_field = sp.simplify(commutator_projector * Omega_star)
Rstar_residual = normalized_average_1d(
    norm_squared(Rstar_residual_field), x_one
)
require(matrix_is_zero(Omega_star), "T-star vorticity block")
require(matrix_is_zero(Qstar_covariance), "Q-star covariance contribution")
require(Rstar_residual == 0, "R-star residual contribution")


def finite_bridge_case(
    line_lift: sp.Matrix, vector: sp.Matrix, label: str
) -> dict[str, object]:
    require(sp.simplify(norm_squared(line_lift)) == 1, f"{label} unit lift")
    line_projector = sp.simplify(line_lift * line_lift.T)
    transverse = sp.simplify(sp.eye(3) - line_projector)
    target = sp.simplify(transverse * vector)
    observed_blocks = []
    commutator_blocks = []
    combined_blocks = []
    for filter_matrix in coordinate_filters:
        observed = sp.simplify(transverse * filter_matrix * vector)
        commutator = sp.simplify(
            (filter_matrix * transverse - transverse * filter_matrix) * vector
        )
        combined = sp.simplify(observed + commutator)
        require(
            matrix_equal(combined, filter_matrix * target),
            f"{label} block commutator identity",
        )
        observed_blocks.append(observed)
        commutator_blocks.append(commutator)
        combined_blocks.append(combined)
    reconstructed = sp.simplify(
        sum(
            (
                coordinate_filters[index] * combined_blocks[index]
                for index in range(3)
            ),
            sp.zeros(3, 1),
        )
    )
    require(matrix_equal(reconstructed, target), f"{label} reconstruction")
    observed_energy = sp.simplify(sum(norm_squared(block) for block in observed_blocks))
    commutator_energy = sp.simplify(
        sum(norm_squared(block) for block in commutator_blocks)
    )
    cross_inner_product = sp.simplify(
        sum(
            (observed_blocks[index].T * commutator_blocks[index])[0]
            for index in range(3)
        )
    )
    target_energy = sp.simplify(norm_squared(target))
    block_identity_residual = sp.simplify(
        target_energy
        - observed_energy
        - commutator_energy
        - 2 * cross_inner_product
    )
    cauchy_slack = sp.factor(
        observed_energy * commutator_energy - cross_inner_product**2
    )
    require(block_identity_residual == 0, f"{label} block energy identity")
    require(cauchy_slack >= 0, f"{label} block Cauchy slack")
    return {
        "label": label,
        "lift": vector_payload(line_lift),
        "input": vector_payload(vector),
        "target": vector_payload(target),
        "targetEnergy": scalar_payload(target_energy),
        "observedSquareSum": scalar_payload(observed_energy),
        "commutatorSquareSum": scalar_payload(commutator_energy),
        "blockCrossInnerProduct": scalar_payload(cross_inner_product),
        "blockEnergyIdentityResidual": scalar_payload(block_identity_residual),
        "cauchySlack": scalar_payload(cauchy_slack),
        "reconstructed": vector_payload(reconstructed),
    }


bridge_random = random.Random(70070)
bridge_cases = []
for case_index in range(6):
    p_value = sp.Rational(bridge_random.randint(-4, 4), bridge_random.randint(2, 6))
    q_value = sp.Rational(bridge_random.randint(-4, 4), bridge_random.randint(2, 6))
    lift = v_symbolic.subs({p: p_value, q: q_value}).applyfunc(sp.factor)
    vector = sp.Matrix(
        [
            sp.Rational(bridge_random.randint(-7, 7), bridge_random.randint(2, 7))
            for _ in range(3)
        ]
    )
    bridge_cases.append(
        finite_bridge_case(lift, vector, f"random-rational-{case_index + 1}")
    )

# An orthogonal one-channel analysis/synthesis pair for which the observed
# term vanishes and the commutator is the entire bridge.  This locks the fact
# that the commutator cannot simply be deleted.
swap_filter = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
swap_synthesis = swap_filter.T
swap_projector = sp.diag(0, 1, 1)
swap_input = sp.Matrix([0, 1, 0])
swap_target = swap_projector * swap_input
swap_observed = swap_projector * swap_filter * swap_input
swap_commutator = (
    swap_filter * swap_projector - swap_projector * swap_filter
) * swap_input
swap_reconstructed = swap_synthesis * (swap_observed + swap_commutator)
require(matrix_equal(swap_filter.T * swap_filter, sp.eye(3)), "swap exact frame")
require(matrix_is_zero(swap_observed), "adversarial observed term vanishes")
require(norm_squared(swap_commutator) == 1, "adversarial commutator supplies bridge")
require(matrix_equal(swap_reconstructed, swap_target), "adversarial reconstruction")

# A blind analysis map shows that a reproducing/lower-frame hypothesis is
# indispensable.  It is outside the positive bridge assumptions by design.
blind_filter = sp.diag(1, 1, 0)
blind_input = sp.Matrix([0, 0, 1])
blind_target_energy = norm_squared(blind_input)
blind_observed_energy = norm_squared(blind_filter * blind_input)
require(blind_target_energy == 1, "blind adversary target")
require(blind_observed_energy == 0, "blind adversary observation")
require(
    not matrix_equal(blind_filter.T * blind_filter, sp.eye(3)),
    "blind adversary violates reconstruction",
)

# The scalar Young step used by the periodic projector estimate has an exact
# square slack.  Finite rational cases include its equality configuration.
X, Y = sp.symbols("X Y", nonnegative=True)
young_slack = sp.factor(X**2 / 8 + 2 * Y**2 - (X / 4 + Y) ** 2)
require(
    sp.simplify(young_slack - (X / 4 - Y) ** 2) == 0,
    "projector bridge Young identity",
)
young_cases = []
young_inputs = [
    (sp.Rational(8, 3), sp.Rational(2, 3)),
    (sp.Rational(5, 7), sp.Rational(11, 13)),
    (sp.Rational(9, 4), sp.Rational(3, 10)),
    (sp.Rational(17, 9), sp.Rational(7, 8)),
]
for x_value, y_value in young_inputs:
    slack = sp.factor(young_slack.subs({X: x_value, Y: y_value}))
    require(slack >= 0, "finite Young case")
    young_cases.append(
        {
            "X": scalar_payload(x_value),
            "Y": scalar_payload(y_value),
            "slack": scalar_payload(slack),
        }
    )


result = {
    "release": "R0.70P",
    "status": "exact-harmonic-projector-bridge-audit",
    "arithmetic": "exact SymPy symbolic, rational, trigonometric, Fourier-coefficient, matrix, finite-sign, and limit arithmetic",
    "checks": {
        "projectorIdentity": True,
        "periodicIntegrationByParts": True,
        "rademacherOrthogonality": True,
        "boundedUnboundedWeightScaling": True,
        "finiteDimensionalBridge": True,
    },
    "projectorIdentityLedger": {
        "convention": "B_ij=partial_i u_j; S=(B+B^T)/2; L=v v^T; P=I-L; omega=curl u",
        "symbolicFamily": {
            "traceConstraint": "B_33=-B_11-B_22",
            "freeGradientParameters": 8,
            "freeDirectionParameters": 2,
            "unitLiftParametrization": vector_payload(v_symbolic),
            "lineProjectorRank": "1",
            "transverseProjectorRank": "2",
            "identity": "tr(L*S**2)-|P*omega|**2/4=sum_ijk B_ij*B_ki*L_jk",
            "residual": scalar_payload(projector_residual),
        },
        "traceFreeRationalSamples": projector_samples,
    },
    "periodicIntegrationByPartsLedger": {
        "domain": "normalized (R/2*pi*Z)^3",
        "velocity": ["sin(y)", "sin(x)", "0"],
        "FourierSupport": ["(+/-1,0,0)", "(0,+/-1,0)"],
        "divergence": scalar_payload(divergence_periodic),
        "identity": "I_L=-integral (u-u_bar)_j*(partial_k u_i)*(partial_i L_jk)",
        "constantProjector": constant_periodic_case,
        "variableProjector": {
            **variable_periodic_case,
            "localLift": ["cos((x+y)/2)", "0", "sin((x+y)/2)"],
            "projectorIsPeriodic": True,
            "localLiftChangesSignAroundXCycle": True,
        },
    },
    "rademacherLedger": {
        "signCount": len(rademacher_signs),
        "signSecondMomentMatrix": matrix_payload(rademacher_moments),
        "symbolicIdentity": "E_epsilon ||sum_j epsilon_j g_j||**2=sum_j ||g_j||**2",
        "symbolicResidual": scalar_payload(
            rademacher_average_symbolic - sp.trace(gram_symbolic)
        ),
        "rationalVectorGram": matrix_payload(rademacher_gram),
        "rationalVectorAverage": scalar_payload(rademacher_sample_average),
        "rationalVectorSquareSum": scalar_payload(rademacher_square_sum),
    },
    "weightScalingLedger": {
        "boundedWeights": {
            "rule": "0<=w_j<=W implies (sum w_j*c_j^2)^(1/2)<=sqrt(W)*(sum c_j^2)^(1/2)",
            "W": scalar_payload(bounded_W),
            "weights": [scalar_payload(value) for value in bounded_weights],
            "componentSquares": [
                scalar_payload(value) for value in bounded_component_squares
            ],
            "unweightedSquareSum": scalar_payload(bounded_unweighted_sum),
            "weightedSquareSum": scalar_payload(bounded_weighted_sum),
            "exactSlack": scalar_payload(bounded_slack),
            "symbolicSlackIdentityResidual": scalar_payload(
                bounded_weight_symbolic_residual
            ),
        },
        "unboundedWeightsNearSingleFrequency": {
            "coefficient": "P(x)=I-v(x)v(x)^T; v=(0,cos(x),sin(x))",
            "projectorDerivativeFrobeniusNormSquared": "2",
            "input": "f_n=n*exp(i*n*x)*e_2",
            "inputHomogeneousHMinusOneNormSquared": scalar_payload(
                input_hminusone_norm_squared
            ),
            "projectorFrequencyShifts": ["-2", "0", "+2"],
            "projectorTimesE2FourierCoefficients": {
                "-2": vector_payload(projector_shift_minus),
                "0": vector_payload(projector_shift_zero),
                "+2": vector_payload(projector_shift_plus),
            },
            "profile": "phi(r)=2*r/(1+r**2)",
            "profileBoundIdentity": str(phi_bound_identity),
            "normalizedCentralFrequency": "rho=n/(2*n)=1/2",
            "profileDerivativeAtOneHalf": scalar_payload(phi_derivative_at_half),
            "profileNondegeneracy": "phi'(rho)=24/25!=0 at rho=1/2",
            "normalizedShiftedFrequencies": ["rho-1/n", "rho+1/n"],
            "multiplier": "m_n(k)=phi(k/(2*n))=4*k*n/(k**2+4*n**2)",
            "deltaPlus": scalar_payload(multiplier_delta_plus),
            "deltaMinus": scalar_payload(multiplier_delta_minus),
            "commutatorNormSquaredFormula": scalar_payload(
                projector_commutator_norm_squared
            ),
            "strictLowerBound": ">144/625 for integer n>=1",
            "strictLowerBoundSlackFormula": scalar_payload(
                commutator_limit_slack
            ),
            "denominatorPositivityCertificates": [
                "5*n**2-4*n+4=5*(n-2/5)**2+16/5>0",
                "5*n**2+4*n+4=5*(n+2/5)**2+16/5>0",
            ],
            "positiveNumeratorAfterSettingT=nSquaredMinusOne": str(
                positive_slack_polynomial
            ),
            "limit": scalar_payload(projector_commutator_limit),
            "dyadicSubsequence": "n_J=2^(J-1), so m_n(k)=phi(2^(-J)*k)",
            "unboundedWeightChoice": "w_J=n_J=2^(J-1)",
            "weightedSquaredLimit": "oo",
            "finiteFrequencySamples": projector_frequency_samples,
        },
    },
    "finiteDimensionalBridgeLedger": {
        "periodicZeroModeCompletion": {
            "domain": "T^3=(R/(2*pi*Z))^3 with normalized Haar measure",
            "FourierConvention": "exp(i*k dot x), k in Z^3; |D| exp(i*k dot x)=|k| exp(i*k dot x)",
            "homogeneousNormConvention": "||f||_{Hdot^-1_#}^2=sum_{k!=0}|f_hat(k)|^2/|k|^2",
            "frameCompletion": "T_star=Pi_0, in addition to the nonzero-mode annular blocks T_j",
            "reason": "Pi_0*omega=0 but Pi_0(P*omega)=[Pi_0,P]*omega can be nonzero",
            "projector": "P(x)=I-v(x)v(x)^T; v=(0,cos(x),sin(x))",
            "periodicVelocity": ["0", "0", "-sin(2*x)/2"],
            "meanZeroInput": "f=curl(u)=cos(2*x)*e_2",
            "inputMean": vector_payload(zero_mode_input_mean),
            "projectedInputMean": vector_payload(zero_mode_projected_mean),
            "commutator": vector_payload(zero_mode_commutator),
            "commutatorNormSquared": scalar_payload(
                zero_mode_commutator_norm_squared
            ),
            "commutatorIdentity": "[Pi_0,P]*f=Pi_0(P*f) because Pi_0*f=0",
            "oscillatoryCoefficient": str(
                sp.trigsimp(zero_mode_oscillatory_coefficient)
            ),
            "dualityPairing": scalar_payload(zero_mode_pairing),
            "inputHomogeneousHMinusOneNormSquared": scalar_payload(
                zero_mode_hminusone_squared
            ),
            "coefficientHomogeneousHOneNormSquared": scalar_payload(
                zero_mode_hone_squared
            ),
            "homogeneousDualityCauchySlack": scalar_payload(
                zero_mode_duality_slack
            ),
            "directTstarVorticityBlock": vector_payload(Omega_star),
            "directQstarCovarianceContribution": matrix_payload(
                Qstar_covariance
            ),
            "directRstarResidualContribution": scalar_payload(Rstar_residual),
            "canonicalPeriodicBridge": "||P*omega||_2<=C_LP*((sum_j||P*T_j*omega||_2^2)^(1/2)+(||[Pi_0,P]*omega||_2^2+sum_j||[T_j,P]*omega||_2^2)^(1/2))",
        },
        "positiveModel": {
            "dimension": 3,
            "analysisFilters": [matrix_payload(matrix) for matrix in coordinate_filters],
            "synthesisFilters": [matrix_payload(matrix) for matrix in coordinate_filters],
            "synthesisConstant": "1",
            "synthesisSquareSlack": str(synthesis_square_slack),
            "reconstruction": "sum_j R_j*T_j=I",
            "blockIdentity": "T_j(P*f)=P*T_j*f+[T_j,P]*f",
            "bridge": "||P*f||<=sqrt(sum_j||P*T_j*f||**2)+sqrt(sum_j||[T_j,P]*f||**2)",
            "randomSeed": 70070,
            "randomRationalCases": bridge_cases,
        },
        "commutatorEssentialAdversary": {
            "analysis": matrix_payload(swap_filter),
            "projector": matrix_payload(swap_projector),
            "input": vector_payload(swap_input),
            "targetEnergy": scalar_payload(norm_squared(swap_target)),
            "observedEnergy": scalar_payload(norm_squared(swap_observed)),
            "commutatorEnergy": scalar_payload(norm_squared(swap_commutator)),
            "reconstructed": vector_payload(swap_reconstructed),
        },
        "missingReconstructionAdversary": {
            "analysis": matrix_payload(blind_filter),
            "input": vector_payload(blind_input),
            "targetEnergy": scalar_payload(blind_target_energy),
            "observedEnergy": scalar_payload(blind_observed_energy),
            "reconstructionHypothesisSatisfied": False,
        },
        "projectorYoungStep": {
            "identity": "X**2/8+2*Y**2-(X/4+Y)**2=(X/4-Y)**2",
            "symbolicSlack": str(young_slack),
            "rationalCases": young_cases,
        },
    },
    "claimBoundary": (
        "This certificate proves only the displayed finite symbolic, rational, "
        "trigonometric, Fourier-coefficient, Rademacher, matrix, and scaling "
        "identities. It does not prove a Calderon reproducing theorem, an "
        "infinite-dimensional Littlewood-Paley or commutator estimate, a "
        "Navier--Stokes continuation criterion, finite-time blow-up, global "
        "smoothness, or the Millennium problem."
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
