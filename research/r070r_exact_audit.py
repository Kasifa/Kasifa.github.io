#!/usr/bin/env python3
"""Exact finite-dimensional audit for the R0.70R near-rank diffusion gate.

The producer verifies four finite groups:

1. the canonical block/derivative decomposition behind the candidate upper
   bound for the report half-curvature K_Q;
2. the exact scalar square slack giving the near-rank diffusion deficit;
3. a two-block, one-transverse-derivative jet attaining the constant; and
4. a smooth periodic divergence-free vorticity/velocity initial datum with
   two disjoint active tight-frame index groups that realizes the same jet.

All arithmetic is exact SymPy arithmetic.  The certificate concerns a
pointwise covariance jet.  It does not prove that the sharp jet relation is
preserved by one Navier--Stokes/Littlewood--Paley evolution, and it does not
close the covariance PDE.
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


# ---------------------------------------------------------------------------
# 1. Canonical finite block/derivative decomposition.
# ---------------------------------------------------------------------------

top_amp, second_amp, third_amp = sp.symbols(
    "A_top A_second A_third", positive=True, real=True
)
e1 = sp.Matrix([1, 0, 0])
e2 = sp.Matrix([0, 1, 0])
e3 = sp.Matrix([0, 0, 1])
L = e1 * e1.T
P = sp.eye(3) - L

# Orthogonal block-index coordinates diagonalize the pointwise synthesis map.
# The ordering assumption is A_top>A_second>=A_third>=0.
canonical_blocks = [top_amp * e1, second_amp * e2, third_amp * e3]
Q_canonical = sum(
    (block * block.T for block in canonical_blocks), sp.zeros(3)
)
require(
    matrix_equal(
        Q_canonical,
        sp.diag(top_amp**2, second_amp**2, third_amp**2),
    ),
    "canonical covariance",
)

# Two spatial derivative directions are enough to certify all finite Hilbert
# space steps and keep the symbolic payload inspectable.
derivative_symbols = sp.symbols("d111:114 d121:124 d131:134 d211:214 d221:224 d231:234", real=True)
derivative_jets = [
    [
        sp.Matrix(derivative_symbols[0:3]),
        sp.Matrix(derivative_symbols[3:6]),
        sp.Matrix(derivative_symbols[6:9]),
    ],
    [
        sp.Matrix(derivative_symbols[9:12]),
        sp.Matrix(derivative_symbols[12:15]),
        sp.Matrix(derivative_symbols[15:18]),
    ],
]

D_symbolic = sp.simplify(
    sum(
        norm_squared(P * derivative)
        for spatial_jet in derivative_jets
        for derivative in spatial_jet
    )
)
C_symbolic = sp.simplify(
    sum(
        norm_squared(L * derivative)
        for spatial_jet in derivative_jets
        for derivative in spatial_jet
    )
)
require(
    sp.simplify(
        D_symbolic
        + C_symbolic
        - sum(
            norm_squared(derivative)
            for spatial_jet in derivative_jets
            for derivative in spatial_jet
        )
    )
    == 0,
    "longitudinal transverse derivative partition",
)

dQ_jets = []
y_jets = []
top_parts = []
lower_parts = []
for spatial_jet in derivative_jets:
    dQ = sum(
        (
            spatial_jet[index] * canonical_blocks[index].T
            + canonical_blocks[index] * spatial_jet[index].T
            for index in range(3)
        ),
        sp.zeros(3),
    )
    y_value = sp.simplify(P * dQ * e1)
    top_part = sp.simplify(
        sum(
            (
                (e1.T * canonical_blocks[index])[0]
                * P
                * spatial_jet[index]
                for index in range(3)
            ),
            sp.zeros(3, 1),
        )
    )
    lower_part = sp.simplify(
        sum(
            (
                (e1.T * spatial_jet[index])[0]
                * P
                * canonical_blocks[index]
                for index in range(3)
            ),
            sp.zeros(3, 1),
        )
    )
    require(
        matrix_equal(y_value, top_part + lower_part),
        "off-diagonal derivative decomposition",
    )
    dQ_jets.append(dQ)
    y_jets.append(y_value)
    top_parts.append(top_part)
    lower_parts.append(lower_part)

top_norm_squared = sp.simplify(sum(norm_squared(value) for value in top_parts))
lower_norm_squared = sp.simplify(
    sum(norm_squared(value) for value in lower_parts)
)
y_norm_squared = sp.simplify(sum(norm_squared(value) for value in y_jets))
top_cauchy_slack = sp.factor(top_amp**2 * D_symbolic - top_norm_squared)
lower_operator_slack = sp.factor(
    second_amp**2 * C_symbolic - lower_norm_squared
)

expected_top_slack = sp.factor(
    top_amp**2
    * sum(
        norm_squared(P * derivative_jets[spatial][block])
        for spatial in range(2)
        for block in (1, 2)
    )
)
require(
    sp.simplify(top_cauchy_slack - expected_top_slack) == 0,
    "top coefficient Cauchy slack",
)

expected_lower_slack = sp.factor(
    sum(
        second_amp**2 * derivative_jets[spatial][0][0] ** 2
        + (second_amp**2 - third_amp**2)
        * derivative_jets[spatial][2][0] ** 2
        for spatial in range(2)
    )
)
require(
    sp.simplify(lower_operator_slack - expected_lower_slack) == 0,
    "lower synthesis operator slack",
)

top_flat = sp.Matrix(
    [top_parts[spatial][component] for spatial in range(2) for component in (1, 2)]
)
lower_flat = sp.Matrix(
    [
        lower_parts[spatial][component]
        for spatial in range(2)
        for component in (1, 2)
    ]
)
cross_inner_product = sp.simplify((top_flat.T * lower_flat)[0])
minkowski_gram_slack = sp.factor(
    norm_squared(top_flat) * norm_squared(lower_flat) - cross_inner_product**2
)
minkowski_sos = sp.expand(
    sum(
        (
            top_flat[first] * lower_flat[second]
            - top_flat[second] * lower_flat[first]
        )
        ** 2
        for first in range(4)
        for second in range(first + 1, 4)
    )
)
require(
    sp.simplify(minkowski_gram_slack - minkowski_sos) == 0,
    "direct-sum Minkowski Gram SOS",
)

lambda1_symbolic = top_amp**2
lambda2_symbolic = second_amp**2
lambda3_symbolic = third_amp**2
KQ_symbolic = sp.factor(
    sum(
        y_value[1] ** 2 / (lambda1_symbolic - lambda2_symbolic)
        + y_value[2] ** 2 / (lambda1_symbolic - lambda3_symbolic)
        for y_value in y_jets
    )
)
denominator_upper = sp.factor(
    y_norm_squared / (lambda1_symbolic - lambda2_symbolic)
)
denominator_slack = sp.factor(denominator_upper - KQ_symbolic)
expected_denominator_slack = sp.factor(
    sum(y_value[2] ** 2 for y_value in y_jets)
    * (
        1 / (lambda1_symbolic - lambda2_symbolic)
        - 1 / (lambda1_symbolic - lambda3_symbolic)
    )
)
require(
    sp.simplify(denominator_slack - expected_denominator_slack) == 0,
    "reduced-resolvent denominator slack",
)


# ---------------------------------------------------------------------------
# 2. Exact scalar reduction and near-rank diffusion deficit.
# ---------------------------------------------------------------------------

p_root, q_root = sp.symbols("p_root q_root", nonnegative=True, real=True)
rho_symbolic = sp.factor(second_amp**2 / top_amp**2)
sqrt_rho_symbolic = sp.factor(second_amp / top_amp)
c_rho_symbolic = sp.factor(
    sqrt_rho_symbolic / (1 - sqrt_rho_symbolic)
)
candidate_scalar = sp.factor(
    (top_amp * p_root + second_amp * q_root) ** 2
    / (top_amp**2 - second_amp**2)
)
deficit_slack_scalar = sp.factor(
    p_root**2
    + c_rho_symbolic * (p_root**2 + q_root**2)
    - candidate_scalar
)
expected_deficit_sos = sp.factor(
    top_amp
    * second_amp
    * (p_root - q_root) ** 2
    / (top_amp**2 - second_amp**2)
)
require(
    sp.simplify(deficit_slack_scalar - expected_deficit_sos) == 0,
    "near-rank deficit scalar SOS",
)
require(
    sp.simplify(
        c_rho_symbolic
        - sp.sqrt(rho_symbolic) / (1 - sp.sqrt(rho_symbolic))
    )
    == 0,
    "c(rho) formula",
)


# ---------------------------------------------------------------------------
# 3. Two-block one-transverse-derivative sharp jet.
# ---------------------------------------------------------------------------

jet_p, jet_q = sp.symbols("jet_p jet_q", positive=True, real=True)
sharp_blocks = [top_amp * e1, second_amp * e2]
sharp_derivatives = [jet_p * e2, jet_q * e1]
Q_sharp = sum((block * block.T for block in sharp_blocks), sp.zeros(3))
dQ_sharp = sum(
    (
        sharp_derivatives[index] * sharp_blocks[index].T
        + sharp_blocks[index] * sharp_derivatives[index].T
        for index in range(2)
    ),
    sp.zeros(3),
)
D_sharp = sp.simplify(
    sum(norm_squared(P * derivative) for derivative in sharp_derivatives)
)
C_sharp = sp.simplify(
    sum(norm_squared(L * derivative) for derivative in sharp_derivatives)
)
y_sharp = sp.simplify(P * dQ_sharp * e1)
KQ_sharp = sp.factor(
    y_sharp[1] ** 2 / (top_amp**2 - second_amp**2)
)
candidate_sharp = sp.factor(
    (sp.sqrt(top_amp**2) * sp.sqrt(D_sharp)
     + sp.sqrt(second_amp**2) * sp.sqrt(C_sharp)) ** 2
    / (top_amp**2 - second_amp**2)
)
require(D_sharp == jet_p**2, "sharp jet D")
require(C_sharp == jet_q**2, "sharp jet C")
require(
    sp.simplify(
        KQ_sharp
        - (top_amp * jet_p + second_amp * jet_q) ** 2
        / (top_amp**2 - second_amp**2)
    )
    == 0,
    "sharp jet curvature",
)
require(sp.simplify(KQ_sharp - candidate_sharp) == 0, "candidate equality jet")

sharp_equal_derivative_deficit = sp.factor(
    (D_sharp - KQ_sharp + c_rho_symbolic * (D_sharp + C_sharp)).subs(
        jet_q, jet_p
    )
)
require(sharp_equal_derivative_deficit == 0, "deficit constant sharpness")

sharp_rational_substitution = {
    top_amp: 3,
    second_amp: 1,
    jet_p: 2,
    jet_q: 2,
}
Q_sharp_rational = Q_sharp.subs(sharp_rational_substitution)
dQ_sharp_rational = dQ_sharp.subs(sharp_rational_substitution)
D_sharp_rational = D_sharp.subs(sharp_rational_substitution)
C_sharp_rational = C_sharp.subs(sharp_rational_substitution)
KQ_sharp_rational = KQ_sharp.subs(sharp_rational_substitution)
rho_sharp_rational = rho_symbolic.subs(sharp_rational_substitution)
c_sharp_rational = c_rho_symbolic.subs(sharp_rational_substitution)
require(matrix_equal(Q_sharp_rational, sp.diag(9, 1, 0)), "rational sharp Q")
require(D_sharp_rational == 4, "rational sharp D")
require(C_sharp_rational == 4, "rational sharp C")
require(KQ_sharp_rational == 8, "rational sharp K_Q")
require(rho_sharp_rational == sp.Rational(1, 9), "rational sharp rho")
require(c_sharp_rational == sp.Rational(1, 2), "rational sharp c")
require(
    D_sharp_rational - KQ_sharp_rational
    == -c_sharp_rational * (D_sharp_rational + C_sharp_rational),
    "rational deficit equality",
)

# A nonaligned rational jet checks the complete candidate away from equality.
nonsharp_substitution = {symbol: 0 for symbol in derivative_symbols}
nonsharp_substitution.update(
    {
        top_amp: 5,
        second_amp: 3,
        third_amp: 1,
        derivative_jets[0][0][1]: 3,
        derivative_jets[0][0][2]: 4,
        derivative_jets[0][1][0]: 4,
    }
)
D_nonsharp = D_symbolic.subs(nonsharp_substitution)
C_nonsharp = C_symbolic.subs(nonsharp_substitution)
KQ_nonsharp = KQ_symbolic.subs(nonsharp_substitution)
candidate_nonsharp = sp.factor(
    (
        5 * sp.sqrt(D_nonsharp) + 3 * sp.sqrt(C_nonsharp)
    )
    ** 2
    / (25 - 9)
)
c_nonsharp = sp.Rational(3, 2)
require(D_nonsharp == 25, "nonsharp D")
require(C_nonsharp == 16, "nonsharp C")
require(candidate_nonsharp - KQ_nonsharp > 0, "nonsharp candidate slack")
require(
    D_nonsharp - KQ_nonsharp
    + c_nonsharp * (D_nonsharp + C_nonsharp)
    > 0,
    "nonsharp deficit slack",
)


# ---------------------------------------------------------------------------
# 4. Smooth torus initial datum with disjoint active tight index groups.
# ---------------------------------------------------------------------------

x1, x2, x3 = sp.symbols("x1 x2 x3", real=True)
coordinates = (x1, x2, x3)
k_frequency, ell_frequency = sp.symbols(
    "k ell", positive=True, integer=True
)
torus_p, torus_q = sp.symbols("p q", positive=True, real=True)
torus_v = e2
torus_w = e3

omega_k = (
    top_amp * sp.cos(k_frequency * x1) * torus_v
    + torus_p / k_frequency * sp.sin(k_frequency * x1) * torus_w
)
omega_ell = (
    second_amp * sp.cos(ell_frequency * x1) * torus_w
    + torus_q / ell_frequency * sp.sin(ell_frequency * x1) * torus_v
)
omega_torus = sp.simplify(omega_k + omega_ell)
velocity_torus = sp.Matrix(
    [
        0,
        -torus_p / k_frequency**2 * sp.cos(k_frequency * x1)
        + second_amp / ell_frequency * sp.sin(ell_frequency * x1),
        -top_amp / k_frequency * sp.sin(k_frequency * x1)
        + torus_q / ell_frequency**2 * sp.cos(ell_frequency * x1),
    ]
)
require(divergence(omega_torus, coordinates) == 0, "torus vorticity divergence")
require(divergence(velocity_torus, coordinates) == 0, "torus velocity divergence")
require(
    matrix_equal(curl(velocity_torus, coordinates), omega_torus),
    "torus curl realization",
)

k_group_coefficients = [sp.Rational(3, 5), sp.Rational(4, 5)]
ell_group_coefficients = [sp.Rational(5, 13), sp.Rational(12, 13)]
require(
    sum(value**2 for value in k_group_coefficients) == 1,
    "k tight coefficient group",
)
require(
    sum(value**2 for value in ell_group_coefficients) == 1,
    "ell tight coefficient group",
)

# The labels encode disjoint active LP index sets.  Each scalar multiplier is
# constant on the corresponding +/- frequency pair for this finite audit.
filtered_blocks = [
    *(coefficient * omega_k for coefficient in k_group_coefficients),
    *(coefficient * omega_ell for coefficient in ell_group_coefficients),
]
block_values_at_zero = [sp.simplify(block.subs(x1, 0)) for block in filtered_blocks]
block_derivatives_at_zero = [
    sp.simplify(sp.diff(block, x1).subs(x1, 0)) for block in filtered_blocks
]
Q_torus_zero = sum(
    (value * value.T for value in block_values_at_zero), sp.zeros(3)
)
dQ_torus_zero = sum(
    (
        block_derivatives_at_zero[index] * block_values_at_zero[index].T
        + block_values_at_zero[index] * block_derivatives_at_zero[index].T
        for index in range(len(filtered_blocks))
    ),
    sp.zeros(3),
)
L_torus = torus_v * torus_v.T
P_torus = sp.eye(3) - L_torus
D_torus_zero = sp.simplify(
    sum(
        norm_squared(P_torus * derivative)
        for derivative in block_derivatives_at_zero
    )
)
C_torus_zero = sp.simplify(
    sum(
        norm_squared(L_torus * derivative)
        for derivative in block_derivatives_at_zero
    )
)
y_torus_zero = sp.simplify(P_torus * dQ_torus_zero * torus_v)
KQ_torus_zero = sp.factor(
    (torus_w.T * dQ_torus_zero * torus_v)[0] ** 2
    / (top_amp**2 - second_amp**2)
)
require(
    matrix_equal(
        Q_torus_zero,
        top_amp**2 * torus_v * torus_v.T
        + second_amp**2 * torus_w * torus_w.T,
    ),
    "torus tight covariance at zero",
)
require(D_torus_zero == torus_p**2, "torus D at zero")
require(C_torus_zero == torus_q**2, "torus C at zero")
require(
    matrix_equal(
        dQ_torus_zero,
        (top_amp * torus_p + second_amp * torus_q)
        * (torus_v * torus_w.T + torus_w * torus_v.T),
    ),
    "torus covariance derivative at zero",
)
require(
    sp.simplify(
        KQ_torus_zero
        - (top_amp * torus_p + second_amp * torus_q) ** 2
        / (top_amp**2 - second_amp**2)
    )
    == 0,
    "torus curvature at zero",
)

torus_sharp_deficit = sp.factor(
    (
        D_torus_zero
        - KQ_torus_zero
        + c_rho_symbolic * (D_torus_zero + C_torus_zero)
    ).subs(torus_q, torus_p)
)
require(torus_sharp_deficit == 0, "torus sharp p=q ratio")

torus_rational_substitution = {
    top_amp: 3,
    second_amp: 1,
    torus_p: 2,
    torus_q: 2,
    k_frequency: 2,
    ell_frequency: 32,
}
require(
    matrix_equal(
        Q_torus_zero.subs(torus_rational_substitution),
        sp.diag(0, 9, 1),
    ),
    "rational torus covariance",
)
require(
    D_torus_zero.subs(torus_rational_substitution) == 4,
    "rational torus D",
)
require(
    C_torus_zero.subs(torus_rational_substitution) == 4,
    "rational torus C",
)
require(
    KQ_torus_zero.subs(torus_rational_substitution) == 8,
    "rational torus K_Q",
)


result = {
    "release": "R0.70R",
    "status": "exact-near-rank-diffusion-jet-audit",
    "arithmetic": "exact SymPy symbolic, rational, matrix, sum-of-squares, trigonometric, and finite-jet arithmetic",
    "checks": {
        "candidateCurvatureBound": True,
        "nearRankDiffusionDeficit": True,
        "twoBlockSharpJet": True,
        "periodicDisjointFrameRealization": True,
    },
    "definitions": {
        "curvatureConvention": "K_Q is the canonical report half-curvature, not the R0.70Q certificate variable K=2*K_Q",
        "aAlpha": "a_alpha=v1 dot Omega_alpha",
        "bAlpha": "b_alpha=P*Omega_alpha",
        "cAlphaK": "c_alpha_k=v1 dot partial_k Omega_alpha",
        "hAlphaK": "h_alpha_k=P*partial_k Omega_alpha",
        "D": "sum_alpha,k |h_alpha_k|^2",
        "C": "sum_alpha,k |c_alpha_k|^2",
        "derivativePartition": "D+C=sum_alpha,k |partial_k Omega_alpha|^2",
        "rho": "lambda2/lambda1 with lambda1>lambda2>=lambda3>=0",
        "cRho": "sqrt(rho)/(1-sqrt(rho))",
    },
    "candidateBoundLedger": {
        "offDiagonalIdentity": "y_k=P*(partial_k Q)*v1=sum_alpha(a_alpha*h_alpha_k+c_alpha_k*b_alpha)",
        "topCoefficientBound": "sum_k|sum_alpha a_alpha*h_alpha_k|^2<=lambda1*D",
        "topCoefficientSlack": scalar_payload(top_cauchy_slack),
        "lowerSynthesisBound": "sum_k|sum_alpha c_alpha_k*b_alpha|^2<=lambda2*C",
        "lowerSynthesisSlack": scalar_payload(lower_operator_slack),
        "minkowskiGramSOSCount": 6,
        "minkowskiGramIdentityResidual": scalar_payload(
            minkowski_gram_slack - minkowski_sos
        ),
        "reducedResolventBound": "K_Q<=sum_k|y_k|^2/(lambda1-lambda2)",
        "reducedResolventSlack": scalar_payload(denominator_slack),
        "candidate": "K_Q<=(sqrt(lambda1)*sqrt(D)+sqrt(lambda2)*sqrt(C))^2/(lambda1-lambda2)",
        "assumptions": "finite block and derivative sums; lambda1>lambda2>=lambda3>=0",
        "nonalignedRationalCase": {
            "eigenvalues": ["25", "9", "1"],
            "D": scalar_payload(D_nonsharp),
            "C": scalar_payload(C_nonsharp),
            "KQ": scalar_payload(KQ_nonsharp),
            "candidateUpperBound": scalar_payload(candidate_nonsharp),
            "candidateSlack": scalar_payload(candidate_nonsharp - KQ_nonsharp),
            "cRho": scalar_payload(c_nonsharp),
            "deficitSlack": scalar_payload(
                D_nonsharp
                - KQ_nonsharp
                + c_nonsharp * (D_nonsharp + C_nonsharp)
            ),
        },
    },
    "nearRankDeficitLedger": {
        "rho": "A_second**2/A_top**2",
        "cRho": "A_second/(A_top-A_second)",
        "candidateInSquareRootVariables": "(A_top*p_root+A_second*q_root)**2/(A_top**2-A_second**2)",
        "inequality": "D-K_Q>=-c(rho)*(D+C)",
        "exactScalarSlack": "A_top*A_second*(p_root-q_root)**2/(A_top**2-A_second**2)",
        "sumOfSquares": "A_top*A_second*(p_root-q_root)**2/(A_top**2-A_second**2)",
        "equalityConditionForPositiveAmplitudes": "sqrt(D)=sqrt(C)",
    },
    "twoBlockSharpJetLedger": {
        "blocks": ["Omega1=sqrt(lambda1)*e1", "Omega2=sqrt(lambda2)*e2"],
        "oneDerivative": ["partial Omega1=sqrt(D)*e2", "partial Omega2=sqrt(C)*e1"],
        "Q": matrix_payload(Q_sharp),
        "partialQ": matrix_payload(dQ_sharp),
        "D": scalar_payload(D_sharp),
        "C": scalar_payload(C_sharp),
        "KQ": "(A_top*jet_p+A_second*jet_q)**2/(A_top**2-A_second**2)",
        "candidateEqualityResidual": scalar_payload(KQ_sharp - candidate_sharp),
        "sharpConstantCondition": "jet_p=jet_q, equivalently D=C",
        "sharpDeficitResidual": scalar_payload(sharp_equal_derivative_deficit),
        "rationalInstance": {
            "blocks": ["3*e1", "e2"],
            "derivatives": ["2*e2", "2*e1"],
            "Q": matrix_payload(Q_sharp_rational),
            "partialQ": matrix_payload(dQ_sharp_rational),
            "D": scalar_payload(D_sharp_rational),
            "C": scalar_payload(C_sharp_rational),
            "KQ": scalar_payload(KQ_sharp_rational),
            "rho": scalar_payload(rho_sharp_rational),
            "cRho": scalar_payload(c_sharp_rational),
            "DminusKQ": scalar_payload(D_sharp_rational - KQ_sharp_rational),
            "minusCRhoTimesDplusC": scalar_payload(
                -c_sharp_rational * (D_sharp_rational + C_sharp_rational)
            ),
        },
    },
    "periodicRealizationLedger": {
        "domain": "T^3=(R/(2*pi*Z))^3 with normalized Haar measure",
        "constantDirections": ["v=e2", "w=e3"],
        "vorticity": "omega0=A*cos(k*x1)*v+(p/k)*sin(k*x1)*w+B*cos(ell*x1)*w+(q/ell)*sin(ell*x1)*v",
        "velocity": vector_payload(velocity_torus),
        "vorticityDivergence": "0",
        "velocityDivergence": "0",
        "curlResidual": vector_payload(curl(velocity_torus, coordinates) - omega_torus),
        "frameAssumption": "the +/-k and +/-ell Fourier pairs have disjoint active scalar LP index sets I_k and I_ell",
        "activeIndexIntersection": "empty",
        "kGroupCoefficients": [
            scalar_payload(value) for value in k_group_coefficients
        ],
        "kGroupCoefficientSquareSum": "1",
        "ellGroupCoefficients": [
            scalar_payload(value) for value in ell_group_coefficients
        ],
        "ellGroupCoefficientSquareSum": "1",
        "atX1Zero": {
            "Q": matrix_payload(Q_torus_zero),
            "partialQ": matrix_payload(dQ_torus_zero),
            "D": scalar_payload(D_torus_zero),
            "C": scalar_payload(C_torus_zero),
            "KQ": "(A_top*p+A_second*q)**2/(A_top**2-A_second**2)",
            "sharpRatio": "p=q",
            "sharpDeficitResidual": scalar_payload(torus_sharp_deficit),
        },
        "farSeparatedRationalInstance": {
            "A": "3",
            "B": "1",
            "p": "2",
            "q": "2",
            "k": "2",
            "ell": "32",
            "Q": matrix_payload(Q_torus_zero.subs(torus_rational_substitution)),
            "D": "4",
            "C": "4",
            "KQ": "8",
        },
        "initialDatumBoundary": "the displayed smooth periodic divergence-free velocity has curl omega0, so it is a valid smooth NSE initial datum; the certificate does not assert preservation of the sharp LP jet relation",
    },
    "claimBoundary": (
        "This certificate proves the displayed exact finite-dimensional "
        "covariance-jet identities and realizes the sharp pointwise jet in a "
        "smooth periodic divergence-free vorticity/velocity initial datum, "
        "conditional on two disjoint active tight-frame index groups. It does "
        "not prove that one Navier--Stokes/Littlewood--Paley evolution "
        "preserves the sharp relation, does not close the covariance PDE, and "
        "does not prove a continuation criterion, finite-time blow-up, global "
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
