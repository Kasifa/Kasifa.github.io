#!/usr/bin/env python3
"""Exact finite audit for the R0.70Z principal-eigengap gate.

The producer checks six narrowly delimited facts:

1. exact spectral and anisotropy decompositions of ``S:Q``;
2. the derivative formula for a simple principal eigenprojector;
3. a six-mode, two-radius field with nonzero principal covariance work;
4. a separated 49/197 filler yielding the same covariance for a sign pair;
5. exact Fourier reconstruction and arithmetic supporting uniform absolute
   and relative principal eigengaps for that sign pair; and
6. the two-channel response lift and its unavoidable common-response branch.

The finite calculations do not prove a projector-coherence regularity
criterion, a pre-convolution tensor estimate, an enstrophy closure, a
continuation theorem, global regularity, or any Millennium-problem claim.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from itertools import product
from pathlib import Path

import sympy as sp

import r070x_exact_audit as r070x


Frequency = tuple[int, int, int]


def canonical(expression: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.expand(expression)))


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def scalar_payload(expression: sp.Expr) -> str:
    return str(canonical(expression))


def vector_payload(vector: sp.Matrix) -> list[str]:
    return [scalar_payload(entry) for entry in vector]


def matrix_is_zero(matrix: sp.Matrix) -> bool:
    return all(canonical(entry) == 0 for entry in matrix)


def add_frequency(first: Frequency, second: Frequency) -> Frequency:
    return tuple(first[index] + second[index] for index in range(3))  # type: ignore[return-value]


def negative_frequency(frequency: Frequency) -> Frequency:
    return tuple(-entry for entry in frequency)  # type: ignore[return-value]


def frequency_square(frequency: Frequency) -> int:
    return sum(entry * entry for entry in frequency)


def scale_vector(scalar: sp.Expr, vector: sp.Matrix) -> sp.Matrix:
    return vector.applyfunc(lambda entry: canonical(scalar * entry))


def outer(first: sp.Matrix, second: sp.Matrix | None = None) -> sp.Matrix:
    if second is None:
        second = first
    return first * second.T


def frobenius(first: sp.Matrix, second: sp.Matrix) -> sp.Expr:
    return canonical(
        sum(
            first[row, column] * second[row, column]
            for row in range(3)
            for column in range(3)
        )
    )


e1 = sp.Matrix([1, 0, 0])
e2 = sp.Matrix([0, 1, 0])
e3 = sp.Matrix([0, 0, 1])
identity = sp.eye(3)


# ---------------------------------------------------------------------------
# 1. Spectral and anisotropy decompositions.
# ---------------------------------------------------------------------------

lambda_1, lambda_2, lambda_3 = sp.symbols(
    "lambda_1 lambda_2 lambda_3", real=True
)
s_1, s_3 = sp.symbols("s_1 s_3", real=True)
s_2 = -s_1 - s_3

gap_12 = lambda_1 - lambda_2
gap_23 = lambda_2 - lambda_3
trace_Q = lambda_1 + lambda_2 + lambda_3
principal_contraction = canonical(
    lambda_1 * s_1 + lambda_2 * s_2 + lambda_3 * s_3
)
gap_split = canonical(gap_12 * s_1 - gap_23 * s_3)
require(
    canonical(principal_contraction - gap_split) == 0,
    "trace-free gap split",
)

P_1 = sp.diag(1, 0, 0)
P_2 = sp.diag(0, 1, 0)
P_3 = sp.diag(0, 0, 1)
Q_diagonal = sp.diag(lambda_1, lambda_2, lambda_3)
anisotropy = Q_diagonal - trace_Q * identity / 3
axisymmetric_coefficient = canonical(
    lambda_1 - (lambda_2 + lambda_3) / 2
)
biaxial_remainder = gap_23 * (P_2 - P_3) / 2
anisotropy_split = (
    axisymmetric_coefficient * (P_1 - identity / 3)
    + biaxial_remainder
)
require(
    matrix_is_zero(anisotropy - anisotropy_split),
    "axisymmetric-biaxial split",
)
require(
    frobenius(P_1 - identity / 3, P_2 - P_3) == 0,
    "anisotropy split orthogonality",
)

anisotropy_square = canonical(frobenius(anisotropy, anisotropy))
anisotropy_square_expected = canonical(
    sp.Rational(2, 3) * axisymmetric_coefficient**2
    + sp.Rational(1, 2) * gap_23**2
)
require(
    canonical(anisotropy_square - anisotropy_square_expected) == 0,
    "anisotropy norm split",
)

sign_strain = P_1 - identity / 3
sign_contraction = canonical(frobenius(sign_strain, Q_diagonal))
sign_expected = canonical((2 * lambda_1 - lambda_2 - lambda_3) / 3)
require(
    canonical(sign_contraction - sign_expected) == 0,
    "pointwise sign pair",
)


# ---------------------------------------------------------------------------
# 2. Principal eigenprojector derivative.
# ---------------------------------------------------------------------------

h_11, h_12, h_13, h_22, h_23, h_33 = sp.symbols(
    "h_11 h_12 h_13 h_22 h_23 h_33", real=True
)
H = sp.Matrix(
    [
        [h_11, h_12, h_13],
        [h_12, h_22, h_23],
        [h_13, h_23, h_33],
    ]
)
projector_derivative = sp.Matrix(
    [
        [0, h_12 / gap_12, h_13 / (lambda_1 - lambda_3)],
        [h_12 / gap_12, 0, 0],
        [h_13 / (lambda_1 - lambda_3), 0, 0],
    ]
)
projector_idempotence_residual = (
    P_1 * projector_derivative
    + projector_derivative * P_1
    - projector_derivative
).applyfunc(canonical)
projector_eigen_residual = (
    H * P_1
    + Q_diagonal * projector_derivative
    - h_11 * P_1
    - lambda_1 * projector_derivative
).applyfunc(canonical)
require(
    matrix_is_zero(projector_idempotence_residual),
    "projector derivative idempotence",
)
require(
    matrix_is_zero(projector_eigen_residual),
    "projector derivative eigen-equation",
)

projector_derivative_square = canonical(
    frobenius(projector_derivative, projector_derivative)
)
projector_derivative_expected = canonical(
    2 * h_12**2 / gap_12**2
    + 2 * h_13**2 / (lambda_1 - lambda_3) ** 2
)
require(
    canonical(projector_derivative_square - projector_derivative_expected)
    == 0,
    "projector derivative norm",
)


# ---------------------------------------------------------------------------
# 3. A two-radius principal-work field.
# ---------------------------------------------------------------------------

base_M = sp.Integer(4)
base_radius_square = sp.Integer(41)
base_n: Frequency = (1, 1, 0)
base_p: Frequency = (4, -5, 0)
base_q: Frequency = (-5, 4, 0)
base_c = sp.Matrix([1, -1, 0])
base_a = e3
base_b = sp.Matrix([4, 5, 0]) / sp.sqrt(base_radius_square)

require(
    all(base_n[index] + base_p[index] + base_q[index] == 0 for index in range(3)),
    "base resonance",
)
require(frequency_square(base_n) == 2, "base low radius")
require(frequency_square(base_p) == 41, "base first high radius")
require(frequency_square(base_q) == 41, "base second high radius")
require(base_radius_square - 16 * frequency_square(base_n) == 9, "base separation")
for frequency, coefficient in (
    (base_n, base_c),
    (base_p, base_a),
    (base_q, base_b),
):
    require(
        canonical(sp.Matrix(frequency).dot(coefficient)) == 0,
        "base Fourier divergence",
    )
require(canonical(base_a.dot(base_a)) == 1, "base a normalization")
require(canonical(base_b.dot(base_b)) == 1, "base b normalization")


def real_cosine_modes(
    frequency: Frequency, coefficient: sp.Matrix
) -> dict[Frequency, sp.Matrix]:
    return {
        frequency: scale_vector(sp.Rational(1, 2), coefficient),
        negative_frequency(frequency): scale_vector(
            sp.Rational(1, 2), coefficient
        ),
    }


base_fourier: dict[Frequency, sp.Matrix] = {}
for frequency, coefficient in (
    (base_n, base_c),
    (base_p, base_a),
    (base_q, base_b),
):
    base_fourier.update(real_cosine_modes(frequency, coefficient))


def strain_coefficients(
    omega_fourier: dict[Frequency, sp.Matrix],
) -> dict[Frequency, sp.Matrix]:
    strain: dict[Frequency, sp.Matrix] = {}
    for mode, coefficient in omega_fourier.items():
        mode_matrix = sp.Matrix(mode)
        velocity = scale_vector(
            sp.I / frequency_square(mode), mode_matrix.cross(coefficient)
        )
        strain[mode] = sp.I / 2 * (
            outer(mode_matrix, velocity) + outer(velocity, mode_matrix)
        )
    return strain


def covariance_convolution(
    omega_fourier: dict[Frequency, sp.Matrix],
    kernel,
) -> defaultdict[Frequency, sp.Matrix]:
    covariance: defaultdict[Frequency, sp.Matrix] = defaultdict(
        lambda: sp.zeros(3, 3)
    )
    for first_mode, second_mode in product(omega_fourier, repeat=2):
        weight = kernel(first_mode, second_mode)
        if weight != 0:
            covariance[add_frequency(first_mode, second_mode)] += (
                weight
                * outer(
                    omega_fourier[first_mode], omega_fourier[second_mode]
                )
            )
    return covariance


def contraction_work(
    strain: dict[Frequency, sp.Matrix],
    covariance: dict[Frequency, sp.Matrix],
) -> sp.Expr:
    work = sp.S.Zero
    for mode, strain_coefficient in strain.items():
        covariance_coefficient = covariance.get(
            negative_frequency(mode), sp.zeros(3, 3)
        )
        work = canonical(
            work + frobenius(strain_coefficient, covariance_coefficient)
        )
    return work


def separated_frame_gamma(
    first_mode: Frequency, second_mode: Frequency
) -> sp.Integer:
    return sp.Integer(
        frequency_square(first_mode) == frequency_square(second_mode)
    )


base_strain = strain_coefficients(base_fourier)
base_principal_covariance = covariance_convolution(
    base_fourier, separated_frame_gamma
)
base_full_covariance = covariance_convolution(
    base_fourier, lambda _first, _second: sp.Integer(1)
)
base_defect_covariance = covariance_convolution(
    base_fourier,
    lambda first, second: 1 - separated_frame_gamma(first, second),
)

base_principal_work = contraction_work(
    base_strain, base_principal_covariance
)
base_full_work = contraction_work(base_strain, base_full_covariance)
base_defect_work = contraction_work(base_strain, base_defect_covariance)
base_principal_expected = canonical(9 * sp.sqrt(41) / 164)
base_full_expected = canonical(351 * sp.sqrt(41) / 6724)
base_defect_expected = canonical(-9 * sp.sqrt(41) / 3362)

require(
    canonical(base_principal_work - base_principal_expected) == 0,
    "base principal work",
)
require(
    canonical(base_full_work - base_full_expected) == 0,
    "base full work",
)
require(
    canonical(base_defect_work - base_defect_expected) == 0,
    "base defect work",
)
require(
    canonical(base_full_work - base_principal_work - base_defect_work) == 0,
    "base full-principal-defect split",
)

# The low response and the common high response are orthogonal.  Pointwise,
# Q_base=xi_low tensor xi_low + xi_high tensor xi_high.  We have
# |xi_low|^2<=2.  The two high polarizations are orthonormal, so
# |xi_high|^2=cos(p.x)^2+cos(q.x)^2<=2.  Hence
# ||Q_base||_op<=tr Q_base<=4.
base_low_energy_upper = canonical(base_c.dot(base_c))
base_high_polarization_dot = canonical(base_a.dot(base_b))
base_high_energy_upper = canonical(
    base_a.dot(base_a) + base_b.dot(base_b)
)
base_covariance_operator_bound = canonical(
    base_low_energy_upper + base_high_energy_upper
)
require(base_low_energy_upper == 2, "base low pointwise energy upper")
require(base_high_polarization_dot == 0, "base high polarization orthogonality")
require(base_high_energy_upper == 2, "base high pointwise energy upper")
require(base_covariance_operator_bound == 4, "base covariance operator upper")


# ---------------------------------------------------------------------------
# 4. Separated filler, equal covariance, and sign-flipped principal work.
# ---------------------------------------------------------------------------

filler_m = sp.Integer(49)
filler_n = sp.Integer(197)
filler_denominator = filler_m**2 + filler_n**2
filler_first_slack = canonical(
    filler_m**2 - 16 * base_radius_square
)
filler_second_slack = canonical(filler_n**2 - 16 * filler_m**2)
filler_amplitude_square = canonical(12 * filler_denominator)
filler_amplitude = sp.sqrt(filler_amplitude_square)

require(filler_denominator == 41210, "filler lower denominator")
require(filler_first_slack == 1745, "first filler separation")
require(filler_second_slack == 393, "second filler separation")

filler_fourier: dict[Frequency, sp.Matrix] = {
    (int(filler_m), 0, 0): scale_vector(filler_amplitude / 2, e2),
    (-int(filler_m), 0, 0): scale_vector(filler_amplitude / 2, e2),
    (int(filler_n), 0, 0): scale_vector(-sp.I * filler_amplitude / 2, e2),
    (-int(filler_n), 0, 0): scale_vector(sp.I * filler_amplitude / 2, e2),
}


def combined_modes(sign: int) -> dict[Frequency, sp.Matrix]:
    combined = {
        mode: scale_vector(sp.Integer(sign), coefficient)
        for mode, coefficient in base_fourier.items()
    }
    for mode, coefficient in filler_fourier.items():
        require(mode not in combined, "disjoint combined Fourier support")
        combined[mode] = coefficient
    return combined


combined_plus = combined_modes(1)
combined_minus = combined_modes(-1)
base_support = set(base_fourier)
filler_support = set(filler_fourier)
all_support = tuple(sorted(base_support | filler_support))

filler_resonances: list[tuple[Frequency, Frequency, Frequency]] = []
for first_mode, second_mode, third_mode in product(all_support, repeat=3):
    if not ({first_mode, second_mode, third_mode} & filler_support):
        continue
    total = tuple(
        first_mode[index] + second_mode[index] + third_mode[index]
        for index in range(3)
    )
    if total == (0, 0, 0):
        filler_resonances.append((first_mode, second_mode, third_mode))
require(len(filler_resonances) == 0, "no filler-involving resonance")

combined_plus_covariance = covariance_convolution(
    combined_plus, separated_frame_gamma
)
combined_minus_covariance = covariance_convolution(
    combined_minus, separated_frame_gamma
)
combined_outputs = set(combined_plus_covariance) | set(combined_minus_covariance)
for output in combined_outputs:
    difference = (
        combined_plus_covariance.get(output, sp.zeros(3, 3))
        - combined_minus_covariance.get(output, sp.zeros(3, 3))
    ).applyfunc(canonical)
    require(matrix_is_zero(difference), "sign-pair covariance equality")

combined_plus_work = contraction_work(
    strain_coefficients(combined_plus), combined_plus_covariance
)
combined_minus_work = contraction_work(
    strain_coefficients(combined_minus), combined_minus_covariance
)
require(
    canonical(combined_plus_work - base_principal_expected) == 0,
    "positive-sign principal work",
)
require(
    canonical(combined_minus_work + base_principal_expected) == 0,
    "negative-sign principal work",
)
require(
    canonical(combined_plus_work + combined_minus_work) == 0,
    "principal-work sign flip",
)


# ---------------------------------------------------------------------------
# 5. Uniform absolute and relative eigengap arithmetic.
# ---------------------------------------------------------------------------

# The R0.70Y zero-set lemma gives
# h=cos(49*x1)^2+sin(197*x1)^2 >= 1/(49^2+197^2).
filler_eigenvalue_lower = canonical(
    filler_amplitude_square / filler_denominator
)
absolute_gap_lower = canonical(
    filler_eigenvalue_lower - base_covariance_operator_bound
)
top_normalized_gap_lower = canonical(
    1 - base_covariance_operator_bound / filler_eigenvalue_lower
)
trace_relative_gap_lower = canonical(
    (filler_eigenvalue_lower - base_covariance_operator_bound)
    / (filler_eigenvalue_lower + base_covariance_operator_bound)
)

require(filler_eigenvalue_lower == 12, "filler eigenvalue lower bound")
require(absolute_gap_lower == 8, "absolute principal eigengap")
require(
    top_normalized_gap_lower == sp.Rational(2, 3),
    "top-normalized principal eigengap",
)
require(
    trace_relative_gap_lower == sp.Rational(1, 2),
    "trace-relative principal eigengap",
)


# ---------------------------------------------------------------------------
# 6. Pre-convolution response lift and common-response obstruction.
# ---------------------------------------------------------------------------

vp = sp.Matrix(sp.symbols("vp_0:3", real=True))
vq = sp.Matrix(sp.symbols("vq_0:3", real=True))
response_common = (vp + vq) / 2
response_chord = (vp - vq) / 2
response_H_plus = outer(response_common) + outer(response_chord)
response_H_minus = outer(response_common) - outer(response_chord)
response_H_delta = 2 * outer(response_chord)

response_lift_residual = (
    response_H_plus - response_H_minus - response_H_delta
).applyfunc(canonical)
response_plus_expected = (outer(vp) + outer(vq)) / 2
response_minus_expected = (outer(vp, vq) + outer(vq, vp)) / 2
require(matrix_is_zero(response_lift_residual), "response lift split")
require(
    matrix_is_zero(response_H_plus - response_plus_expected),
    "response common-channel identity",
)
require(
    matrix_is_zero(response_H_minus - response_minus_expected),
    "response principal-channel identity",
)

vp_norm_square = canonical(vp.dot(vp))
vq_norm_square = canonical(vq.dot(vq))
response_gamma = canonical(vp.dot(vq))
response_trace_plus = canonical(sp.trace(response_H_plus))
response_trace_minus = canonical(sp.trace(response_H_minus))
response_trace_delta = canonical(sp.trace(response_H_delta))
require(
    canonical(response_trace_plus - (vp_norm_square + vq_norm_square) / 2)
    == 0,
    "response plus trace",
)
require(
    canonical(response_trace_minus - response_gamma) == 0,
    "response minus trace",
)
require(
    canonical(
        response_trace_delta
        - (vp_norm_square + vq_norm_square) / 2
        + response_gamma
    )
    == 0,
    "response delta trace",
)

# The archived R0.70X field supplies a fixed nonvanishing test of all three
# scalar response traces: kernel 1 (full), Gamma (principal), and K (defect).
r070x_full_covariance = covariance_convolution(
    r070x.omega_fourier, lambda _first, _second: sp.Integer(1)
)
r070x_principal_covariance = covariance_convolution(
    r070x.omega_fourier,
    lambda first, second: 1
    - r070x.response_kernel(
        r070x.shell_label[first], r070x.shell_label[second]
    ),
)
r070x_defect_covariance = covariance_convolution(
    r070x.omega_fourier,
    lambda first, second: r070x.response_kernel(
        r070x.shell_label[first], r070x.shell_label[second]
    ),
)
r070x_full_work = contraction_work(
    r070x.strain_fourier, r070x_full_covariance
)
r070x_principal_work = contraction_work(
    r070x.strain_fourier, r070x_principal_covariance
)
r070x_defect_work = contraction_work(
    r070x.strain_fourier, r070x_defect_covariance
)
r070x_full_expected = canonical(-sp.Rational(137781, 32780))
r070x_principal_expected = canonical(
    sp.Rational(81, 20) * (r070x.physical_kappa - 1)
)
r070x_defect_expected = canonical(
    -sp.Rational(81, 32780)
    * (1639 * r070x.physical_kappa + 62)
)
require(
    canonical(r070x_full_work - r070x_full_expected) == 0,
    "R0.70X full work",
)
require(
    canonical(r070x_principal_work - r070x_principal_expected) == 0,
    "R0.70X principal work",
)
require(
    canonical(r070x_defect_work - r070x_defect_expected) == 0,
    "R0.70X defect work",
)
require(
    canonical(
        r070x_full_work - r070x_principal_work - r070x_defect_work
    )
    == 0,
    "R0.70X response trace split",
)

# On the sharp HHL family, the common-response channel remains order one,
# while the chord channel has the one-power response gain proved in R0.70Y.
sharp_full = canonical(
    r070x.sharp_A_n + r070x.sharp_A_p + r070x.sharp_A_q
)
sharp_defect = canonical(
    r070x.kappa_M * r070x.sharp_A_n
    + r070x.sharp_A_p
    + r070x.sharp_A_q
)
sharp_principal = canonical(sharp_full - sharp_defect)
sharp_full_expected = canonical(
    -(r070x.triad_M + 1) / r070x.triad_Q
)
sharp_defect_expected = canonical(
    -(1 + r070x.triad_M * r070x.kappa_M) / r070x.triad_Q
)
sharp_principal_expected = canonical(
    -r070x.triad_M * (1 - r070x.kappa_M) / r070x.triad_Q
)
require(
    canonical(sharp_full - sharp_full_expected) == 0,
    "sharp full channel",
)
require(
    canonical(sharp_defect - sharp_defect_expected) == 0,
    "sharp chord channel",
)
require(
    canonical(sharp_principal - sharp_principal_expected) == 0,
    "sharp principal channel",
)


payload = {
    "release": "R0.70Z",
    "status": "principal-eigengap-sign-no-go",
    "checks": {
        "spectralDecomposition": True,
        "principalProjectorDerivative": True,
        "twoRadiusPrincipalWork": True,
        "sameCovarianceSignPair": True,
        "uniformAbsoluteRelativeEigengap": True,
        "responseLiftCommonChannel": True,
    },
    "spectralLedger": {
        "traceFreeSplit": "S:Q=(lambda_1-lambda_2)*s_1-(lambda_2-lambda_3)*s_3",
        "traceFreeSplitResidual": scalar_payload(
            principal_contraction - gap_split
        ),
        "axisymmetricCoefficient": scalar_payload(
            axisymmetric_coefficient
        ),
        "axisymmetricBiaxialResidual": [
            scalar_payload(entry) for entry in anisotropy - anisotropy_split
        ],
        "anisotropyNormSquare": scalar_payload(anisotropy_square),
        "anisotropyNormSquareExpected": scalar_payload(
            anisotropy_square_expected
        ),
        "signPair": "S_+=P_1-I/3 and S_-=-S_+",
        "positiveContraction": scalar_payload(sign_contraction),
        "interpretation": "a positive principal eigengap makes anisotropy nonzero but does not determine the sign of S:Q",
    },
    "projectorLedger": {
        "projector": "P_1=e_1 tensor e_1",
        "derivative": "D P_1[H]=sum_(j=2,3) (P_j H P_1+P_1 H P_j)/(lambda_1-lambda_j)",
        "idempotenceResidual": [
            scalar_payload(entry) for entry in projector_idempotence_residual
        ],
        "eigenEquationResidual": [
            scalar_payload(entry) for entry in projector_eigen_residual
        ],
        "frobeniusNormSquare": scalar_payload(
            projector_derivative_square
        ),
        "bestGapBound": "|D P_1[H]|_F<=|H|_F/(lambda_1-lambda_2)",
        "exactGeometricCoefficient": "|grad P_1|_F",
        "criticalCoefficient": "chi_Q=|grad Q|_F/(lambda_1-lambda_2) is a sharp sufficient upper majorant, not an exact or necessary coefficient",
        "navierStokesScaling": "under dyadic frame-covariant Navier-Stokes scaling chi_Q scales as one inverse length; L3 is dimensionally critical and whole-space invariant, but the fixed-torus L3 norm scales by the replication factor",
    },
    "baseFieldLedger": {
        "field": "xi=c*cos(n.x)+a*cos(p.x)+b*cos(q.x)",
        "n": list(base_n),
        "p": list(base_p),
        "q": list(base_q),
        "c": vector_payload(base_c),
        "a": vector_payload(base_a),
        "b": vector_payload(base_b),
        "radiiSquared": [2, 41, 41],
        "strictFactorFourSquaredSlack": 9,
        "modeCount": len(base_fourier),
        "principalWork": scalar_payload(base_principal_work),
        "principalWorkExpected": scalar_payload(base_principal_expected),
        "defectWork": scalar_payload(base_defect_work),
        "fullWork": scalar_payload(base_full_work),
        "splitResidual": scalar_payload(
            base_full_work - base_principal_work - base_defect_work
        ),
        "lowEnergyUpper": scalar_payload(base_low_energy_upper),
        "highPolarizationDot": scalar_payload(
            base_high_polarization_dot
        ),
        "highEnergyUpper": scalar_payload(base_high_energy_upper),
        "covarianceOperatorBound": scalar_payload(
            base_covariance_operator_bound
        ),
    },
    "signPairLedger": {
        "fields": "omega_(Lambda,sigma)=Lambda*(sigma*xi+sqrt(12*41210)*eta), sigma in {-1,1}",
        "eta": "e_2*(cos(49*x_1)+sin(197*x_1))",
        "radiiSquared": [2, 41, 2401, 38809],
        "strictFactorFourSquaredSlacks": [9, 1745, 393],
        "modeCount": len(combined_plus),
        "covarianceOutputCount": len(combined_plus_covariance),
        "covarianceDifference": "0 at every Fourier output",
        "fillerInvolvingResonanceCount": len(filler_resonances),
        "positiveWork": scalar_payload(combined_plus_work),
        "negativeWork": scalar_payload(combined_minus_work),
        "scaledWork": "+/-(9*sqrt(41)/164)*Lambda^3",
    },
    "eigengapLedger": {
        "fillerLowerLemma": "cos(49*x_1)^2+sin(197*x_1)^2>=1/41210",
        "fillerAmplitudeSquare": scalar_payload(filler_amplitude_square),
        "fillerEigenvalueLower": scalar_payload(
            filler_eigenvalue_lower
        ),
        "baseOperatorUpper": scalar_payload(
            base_covariance_operator_bound
        ),
        "absoluteGap": "lambda_1-lambda_2>=8*Lambda^2",
        "absoluteGapCoefficient": scalar_payload(absolute_gap_lower),
        "topNormalizedGap": "(lambda_1-lambda_2)/lambda_1>=2/3",
        "topNormalizedGapCoefficient": scalar_payload(
            top_normalized_gap_lower
        ),
        "traceRelativeGap": "(lambda_1-lambda_2)/trace(Q)>=1/2",
        "traceRelativeGapCoefficient": scalar_payload(
            trace_relative_gap_lower
        ),
        "weylStep": "lambda_1>=12*Lambda^2 and lambda_2<=4*Lambda^2",
    },
    "responseLiftLedger": {
        "common": "U_pq=(V(p)+V(q))/2",
        "chord": "C_pq=(V(p)-V(q))/2",
        "operators": {
            "Hplus": "U tensor U+C tensor C",
            "Hminus": "U tensor U-C tensor C",
            "Hdelta": "2*C tensor C",
        },
        "operatorSplitResidual": [
            scalar_payload(entry) for entry in response_lift_residual
        ],
        "unitResponseTraces": {
            "Hplus": "1",
            "Hminus": "Gamma(p,q)",
            "Hdelta": "1-Gamma(p,q)",
        },
        "preConvolutionInterpretation": "response traces of Mplus, Mminus, and Mdelta recover omega tensor omega, Q, and D_cross before the p+q convolution is discarded",
        "r070x": {
            "modeCount": len(r070x.omega_fourier),
            "fullWork": scalar_payload(r070x_full_work),
            "principalWork": scalar_payload(r070x_principal_work),
            "defectWork": scalar_payload(r070x_defect_work),
            "splitResidual": scalar_payload(
                r070x_full_work
                - r070x_principal_work
                - r070x_defect_work
            ),
        },
        "sharpHHL": {
            "full": scalar_payload(sharp_full),
            "principal": scalar_payload(sharp_principal),
            "defect": scalar_payload(sharp_defect),
            "analyticPremise": "kappa_M=O_frame(M^-2)",
            "consequence": "full and principal stay order one while the signed chord channel is order M^-1",
        },
        "sequenceBoundary": "any uniform absolute common-response HHL majorant stays order one along the sharp family, unlike the summable 2^(-m) defect kernel",
        "positiveEndpoint": "one classical sufficient control is |full stretching|<=C*||omega||_BMO*||omega||_2^2 by periodic div-curl H1-BMO duality; other compensations are not excluded",
    },
    "analyticDependencies": [
        "the scalar frame is real, even, radial, smooth, dyadic, Parseval, and strictly supported in 1/2<|xi|<2",
        "strict factor-four separation makes response vectors at distinct listed radii orthogonal",
        "the h lower bound reuses the exact zero-set parity lemma proved analytically in R0.70Y",
        "Weyl monotonicity and lambda_2(A+B)<=lambda_2(A)+lambda_1(B) convert the pointwise covariance bounds into the eigengap",
        "the reduced resolvent inverse is restricted to the lower spectral plane and the projector derivative is for symmetric perturbations where lambda_1>lambda_2",
        "the finite producer verifies the Fourier and algebraic identities but not an infinite-dimensional regularity theorem",
    ],
    "claimBoundary": [
        "proves a smooth finite-Fourier sign pair with identical pointwise frame covariance and a uniform absolute and relative principal eigengap",
        "rules out any universal sign law for the principal work based only on Q or its spectral data",
        "shows that a principal eigengap alone does not make the principal work vanish or become lower than cubic under amplitude scaling",
        "identifies |grad P_1| as the exact geometric derivative and |grad Q|/(lambda_1-lambda_2) as a sharp sufficient upper majorant rather than a necessary coefficient",
        "constructs an exact two-channel pre-convolution response lift that survives the R0.70X rank-one field",
        "proves that the full and principal HHL symbols retain a common-response order-one channel, so the R0.70Y summable chord kernel does not extend to full stretching",
        "does not rule out a scale-homogeneous absolute estimate with additional derivative, alignment, signed, or Carleson-type compensation",
        "does not prove that projector coherence controls the principal work",
        "does not prove an enstrophy closure, continuation criterion, singularity, global regularity, or solve the Millennium problem",
    ],
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if arguments.output is None:
        print(rendered, end="")
    else:
        arguments.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
