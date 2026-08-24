#!/usr/bin/env python3
"""Exact finite audit for the R0.70X signed-trilinear gate.

The producer checks six narrowly delimited facts:

1. the Laplacian-weighted cyclic triad identity;
2. a sharp high-high-low triad family with only one t/R gain;
3. the geometry of a three-wave planar eigenfield;
4. rank-at-most-one covariance for the actual complete radial frame;
5. the exact physical-space signed-work formula and its strict sign; and
6. an independent 36-mode Fourier/Parseval reconstruction.

The finite calculations do not prove a vector-valued trilinear multiplier
theorem, a uniformly positive covariance gap, an enstrophy closure, a
continuation theorem, or any Navier--Stokes regularity conclusion.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from itertools import product
from pathlib import Path

import sympy as sp


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


def matrix_payload(matrix: sp.Matrix) -> list[list[str]]:
    return [
        [scalar_payload(matrix[row, column]) for column in range(matrix.cols)]
        for row in range(matrix.rows)
    ]


def outer(first: sp.Matrix, second: sp.Matrix | None = None) -> sp.Matrix:
    if second is None:
        second = first
    return first * second.T


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


def frobenius(first: sp.Matrix, second: sp.Matrix) -> sp.Expr:
    return canonical(
        sum(
            first[row, column] * second[row, column]
            for row in range(3)
            for column in range(3)
        )
    )


def normalized_torus_mean(expression: sp.Expr, variables: tuple[sp.Symbol, ...]) -> sp.Expr:
    result = expression
    for variable in variables:
        result = sp.integrate(result, (variable, 0, 2 * sp.pi)) / (2 * sp.pi)
    return canonical(result)


e1 = sp.Matrix([1, 0, 0])
e2 = sp.Matrix([0, 1, 0])
e3 = sp.Matrix([0, 0, 1])


# ---------------------------------------------------------------------------
# 1. Generic Laplacian-weighted cyclic identity.
# ---------------------------------------------------------------------------

nmag = sp.symbols("nmag", positive=True, real=True)
px, py, pz = sp.symbols("px py pz", real=True)
c0x, c0y, c0z = sp.symbols("c0x c0y c0z", real=True)
a0x, a0y, a0z = sp.symbols("a0x a0y a0z", real=True)
b0x, b0y, b0z = sp.symbols("b0x b0y b0z", real=True)

n_vector = nmag * e1
p_vector = sp.Matrix([px, py, pz])
q_vector = -n_vector - p_vector
c_vector = n_vector.cross(sp.Matrix([c0x, c0y, c0z]))
a_vector = p_vector.cross(sp.Matrix([a0x, a0y, a0z]))
b_vector = q_vector.cross(sp.Matrix([b0x, b0y, b0z]))


def weighted_triad_leg(
    output: sp.Matrix,
    first_input: sp.Matrix,
    second_input: sp.Matrix,
    output_coefficient: sp.Matrix,
    first_coefficient: sp.Matrix,
    second_coefficient: sp.Matrix,
) -> sp.Expr:
    """Return |output|^2 times its symmetrized strain contraction."""

    return canonical(
        (second_input - first_input)
        .cross(output.cross(output_coefficient))
        .dot(first_coefficient.cross(second_coefficient))
    )


B_n = weighted_triad_leg(
    n_vector, p_vector, q_vector, c_vector, a_vector, b_vector
)
B_p = weighted_triad_leg(
    p_vector, q_vector, n_vector, a_vector, b_vector, c_vector
)
B_q = weighted_triad_leg(
    q_vector, n_vector, p_vector, b_vector, c_vector, a_vector
)
cyclic_residual = canonical(B_n + B_p + B_q)

require(canonical(n_vector.dot(c_vector)) == 0, "n divergence")
require(canonical(p_vector.dot(a_vector)) == 0, "p divergence")
require(canonical(q_vector.dot(b_vector)) == 0, "q divergence")
require(cyclic_residual == 0, "cyclic square-weight identity")

beta_n, beta_p, beta_q = sp.symbols("beta_n beta_p beta_q", real=True)
cyclic_block = canonical(beta_n * B_n + beta_p * B_p + beta_q * B_q)
cyclic_difference_form = canonical(
    (beta_n - beta_q) * B_n + (beta_p - beta_q) * B_p
)
require(
    canonical(cyclic_block - cyclic_difference_form) == 0,
    "cyclic beta-difference form",
)


# ---------------------------------------------------------------------------
# 2. Sharp high-high-low triad family.
# ---------------------------------------------------------------------------

triad_M = sp.symbols("M", integer=True, positive=True)
triad_Q = sp.sqrt(2 * triad_M**2 + 2 * triad_M + 1)
kappa_M = sp.symbols("kappa_M", real=True, nonnegative=True)

sharp_n = e1
sharp_p = sp.Matrix([triad_M, triad_M, 0])
sharp_q = sp.Matrix([-triad_M - 1, -triad_M, 0])
sharp_c = e2
sharp_a = e3
sharp_b = sp.Matrix([triad_M, -triad_M - 1, 0]) / triad_Q


def triad_leg(
    output: sp.Matrix,
    first_input: sp.Matrix,
    second_input: sp.Matrix,
    output_coefficient: sp.Matrix,
    first_coefficient: sp.Matrix,
    second_coefficient: sp.Matrix,
) -> sp.Expr:
    output_square = canonical(output.dot(output))
    return canonical(
        weighted_triad_leg(
            output,
            first_input,
            second_input,
            output_coefficient,
            first_coefficient,
            second_coefficient,
        )
        / output_square
    )


sharp_A_n = triad_leg(
    sharp_n, sharp_p, sharp_q, sharp_c, sharp_a, sharp_b
)
sharp_A_p = triad_leg(
    sharp_p, sharp_q, sharp_n, sharp_a, sharp_b, sharp_c
)
sharp_A_q = triad_leg(
    sharp_q, sharp_n, sharp_p, sharp_b, sharp_c, sharp_a
)
sharp_cyclic_residual = canonical(
    sharp_n.dot(sharp_n) * sharp_A_n
    + sharp_p.dot(sharp_p) * sharp_A_p
    + sharp_q.dot(sharp_q) * sharp_A_q
)
sharp_block = canonical(kappa_M * sharp_A_n + sharp_A_p + sharp_A_q)
sharp_expected = canonical(-(1 + triad_M * kappa_M) / triad_Q)

require(matrix_is_zero(sharp_n + sharp_p + sharp_q), "sharp resonance")
require(canonical(sharp_n.dot(sharp_c)) == 0, "sharp n divergence")
require(canonical(sharp_p.dot(sharp_a)) == 0, "sharp p divergence")
require(canonical(sharp_q.dot(sharp_b)) == 0, "sharp q divergence")
require(sharp_A_n == canonical(-triad_M / triad_Q), "sharp A_n")
require(
    sharp_A_p == canonical(-(triad_M + 1) / triad_Q),
    "sharp A_p",
)
require(sharp_A_q == canonical(triad_M / triad_Q), "sharp A_q")
require(sharp_cyclic_residual == 0, "sharp cyclic residual")
require(canonical(sharp_block - sharp_expected) == 0, "sharp block")


# ---------------------------------------------------------------------------
# 3. Three-wave planar eigenfield for the rank-at-most-one counterexample.
# ---------------------------------------------------------------------------

x1, x2, x3 = sp.symbols("x1 x2 x3", real=True)
x_vector = sp.Matrix([x1, x2, x3])
axis = sp.Matrix([1, -1, 1])
plane_p = sp.Matrix([1, 1, 0])
plane_q = sp.Matrix([-1, 0, 1])
plane_r = sp.Matrix([0, 1, 1])
plane_modes = (plane_p, plane_q, plane_r)

psi = sum(sp.cos(mode.dot(x_vector)) for mode in plane_modes)
grad_psi = sp.Matrix([sp.diff(psi, variable) for variable in (x1, x2, x3)])
w_field = axis.cross(grad_psi)
hessian_psi = sp.hessian(psi, (x1, x2, x3))

divergence_w = canonical(
    sp.diff(w_field[0], x1)
    + sp.diff(w_field[1], x2)
    + sp.diff(w_field[2], x3)
)
laplacian_w = sp.Matrix(
    [
        sum(sp.diff(component, variable, 2) for variable in (x1, x2, x3))
        for component in w_field
    ]
)
eigen_residual = (laplacian_w + 2 * w_field).applyfunc(sp.trigsimp)
psi_cube_mean = normalized_torus_mean(psi**3, (x1, x2, x3))

convective_w = sp.Matrix(
    [
        sum(
            w_field[index] * sp.diff(w_field[component], (x1, x2, x3)[index])
            for index in range(3)
        )
        for component in range(3)
    ]
)
A_field_geometric = sp.expand(w_field.dot(axis.cross(convective_w)))
A_field_hessian = sp.expand(-3 * w_field.dot(hessian_psi * w_field))
A_field_residual = sp.trigsimp(A_field_geometric - A_field_hessian)
A_mean = normalized_torus_mean(A_field_hessian, (x1, x2, x3))

require(matrix_is_zero(plane_p + plane_q - plane_r), "plane resonance")
require(canonical(axis.dot(axis)) == 3, "axis norm")
for mode in plane_modes:
    require(canonical(mode.dot(mode)) == 2, "plane radius")
    require(canonical(axis.dot(mode)) == 0, "plane orthogonality")
require(divergence_w == 0, "w divergence")
require(canonical(axis.dot(w_field)) == 0, "w axis orthogonality")
require(matrix_is_zero(eigen_residual), "w Laplacian eigenfield")
require(psi_cube_mean == sp.Rational(3, 2), "psi cube mean")
require(canonical(A_field_residual) == 0, "A-field representations")
require(A_mean == sp.Rational(81, 2), "A-field mean")


# ---------------------------------------------------------------------------
# 4. Complete-frame covariance and defect algebra.
# ---------------------------------------------------------------------------

f1, fM, fN, frame_kappa = sp.symbols(
    "f1 fM fN kappa", real=True
)
Gamma_1M = sp.Integer(0)
Gamma_1N = sp.Integer(0)
Gamma_MN = 1 - frame_kappa
physical_scalar = canonical((f1 + fM + fN) ** 2)
covariance_scalar = canonical(
    f1**2
    + fM**2
    + fN**2
    + 2 * Gamma_1M * f1 * fM
    + 2 * Gamma_1N * f1 * fN
    + 2 * Gamma_MN * fM * fN
)
defect_scalar = canonical(physical_scalar - covariance_scalar)
defect_scalar_expected = canonical(
    2 * (f1 * fM + f1 * fN + frame_kappa * fM * fN)
)

wx, wy, wz, qscalar = sp.symbols("wx wy wz qscalar", real=True)
generic_w = sp.Matrix([wx, wy, wz])
generic_covariance = qscalar * outer(generic_w)
covariance_minors: list[sp.Expr] = []
for first_row in range(3):
    for second_row in range(first_row + 1, 3):
        for first_column in range(3):
            for second_column in range(first_column + 1, 3):
                covariance_minors.append(
                    canonical(
                        generic_covariance.extract(
                            [first_row, second_row],
                            [first_column, second_column],
                        ).det()
                    )
                )

L1 = sp.Integer(5)
audit_M = sp.Integer(6)
audit_N = sp.Integer(7)
LM = sp.Integer(2) + 3 * audit_M**2
LN = sp.Integer(2) + 3 * audit_N**2
low_high_M_slack = canonical(LM - 16 * L1)
low_high_N_slack = canonical(LN - 16 * L1)

require(
    canonical(defect_scalar - defect_scalar_expected) == 0,
    "complete-frame defect scalar",
)
require(all(minor == 0 for minor in covariance_minors), "rank-one minors")
require(LM == 110 and LN == 149, "audit radii")
require(low_high_M_slack > 0 and low_high_N_slack > 0, "factor-four separation")


# ---------------------------------------------------------------------------
# 5. Exact physical-space signed work and sign.
# ---------------------------------------------------------------------------

amplitude_a, amplitude_b, amplitude_c = sp.symbols(
    "a b c", real=True
)
z = sp.symbols("z", real=True)
physical_kappa = sp.symbols("kappa", real=True, nonnegative=True)
physical_f1 = amplitude_a * sp.cos(z)
physical_fM = amplitude_b * sp.cos(audit_M * z)
physical_fN = amplitude_c * sp.sin(audit_N * z)
physical_functions = (physical_f1, physical_fM, physical_fN)
physical_radii = (L1, LM, LN)

defect_pairs = (
    (sp.Integer(1), physical_f1, physical_fM),
    (sp.Integer(1), physical_f1, physical_fN),
    (physical_kappa, physical_fM, physical_fN),
)
strain_scalar = sum(
    sp.diff(function, z) / radius
    for function, radius in zip(physical_functions, physical_radii)
)
defect_pair_scalar = sum(
    weight * first * second for weight, first, second in defect_pairs
)
axial_mean = canonical(
    sp.integrate(strain_scalar * defect_pair_scalar, (z, 0, 2 * sp.pi))
    / (2 * sp.pi)
)
signed_work_physical = canonical(2 * A_mean * axial_mean)
signed_bracket = canonical(
    audit_N / LN - audit_M / LM - physical_kappa / L1
)
signed_work_expected = canonical(
    sp.Rational(81, 4)
    * amplitude_a
    * amplitude_b
    * amplitude_c
    * signed_bracket
)
fixed_signed_work = canonical(
    signed_work_physical.subs(
        {amplitude_a: 1, amplitude_b: 1, amplitude_c: 1}
    )
)
fixed_signed_expected = canonical(
    -sp.Rational(81, 32780) * (62 + 1639 * physical_kappa)
)
adjacent_free_part = canonical(audit_N / LN - audit_M / LM)

require(
    canonical(signed_work_physical - signed_work_expected) == 0,
    "physical-space signed work",
)
require(
    canonical(fixed_signed_work - fixed_signed_expected) == 0,
    "fixed signed work",
)
require(adjacent_free_part < 0, "strict sign without adjacent response")


# ---------------------------------------------------------------------------
# 6. Independent 36-mode Fourier/Parseval reconstruction.
# ---------------------------------------------------------------------------

I = sp.I
axis_frequency: Frequency = (1, -1, 1)
plane_frequencies: tuple[Frequency, ...] = (
    (1, 1, 0),
    (-1, 0, 1),
    (0, 1, 1),
)

base_fourier: dict[Frequency, sp.Matrix] = {}
axis_matrix = sp.Matrix(axis_frequency)
for base in plane_frequencies:
    for sign in (-1, 1):
        mode: Frequency = tuple(sign * entry for entry in base)  # type: ignore[assignment]
        mode_matrix = sp.Matrix(mode)
        # psi_hat(mode)=1/2 and grad contributes i*mode.
        base_fourier[mode] = scale_vector(I / 2, axis_matrix.cross(mode_matrix))


def scalar_fourier(j: int, kind: str) -> dict[Frequency, sp.Expr]:
    plus: Frequency = tuple(j * entry for entry in axis_frequency)  # type: ignore[assignment]
    minus = negative_frequency(plus)
    if kind == "cos":
        return {plus: sp.Rational(1, 2), minus: sp.Rational(1, 2)}
    if kind == "sin":
        return {plus: -I / 2, minus: I / 2}
    raise ValueError(kind)


omega_fourier: dict[Frequency, sp.Matrix] = {}
shell_label: dict[Frequency, int] = {}
for shell, kind in ((1, "cos"), (6, "cos"), (7, "sin")):
    for base_mode, base_coefficient in base_fourier.items():
        for axial_mode, axial_coefficient in scalar_fourier(shell, kind).items():
            output = add_frequency(base_mode, axial_mode)
            require(output not in omega_fourier, "disjoint Fourier shell modes")
            omega_fourier[output] = scale_vector(
                axial_coefficient, base_coefficient
            )
            shell_label[output] = shell


def response_kernel(first_shell: int, second_shell: int) -> sp.Expr:
    if first_shell == second_shell:
        return sp.Integer(0)
    pair = frozenset((first_shell, second_shell))
    if pair in (frozenset((1, 6)), frozenset((1, 7))):
        return sp.Integer(1)
    if pair == frozenset((6, 7)):
        return physical_kappa
    raise AssertionError(pair)


fourier_radii = {
    shell: sorted(
        {frequency_square(mode) for mode in omega_fourier if shell_label[mode] == shell}
    )
    for shell in (1, 6, 7)
}
for mode, coefficient in omega_fourier.items():
    require(
        canonical(sp.Matrix(mode).dot(coefficient)) == 0,
        "Fourier divergence",
    )
require(fourier_radii == {1: [5], 6: [110], 7: [149]}, "Fourier radii")

strain_fourier: dict[Frequency, sp.Matrix] = {}
for mode, coefficient in omega_fourier.items():
    mode_matrix = sp.Matrix(mode)
    velocity = scale_vector(
        I / frequency_square(mode), mode_matrix.cross(coefficient)
    )
    strain_fourier[mode] = sp.I / 2 * (
        outer(mode_matrix, velocity) + outer(velocity, mode_matrix)
    )

defect_fourier: defaultdict[Frequency, sp.Matrix] = defaultdict(
    lambda: sp.zeros(3, 3)
)
for first_mode, second_mode in product(omega_fourier, repeat=2):
    kernel = response_kernel(
        shell_label[first_mode], shell_label[second_mode]
    )
    if kernel != 0:
        defect_fourier[add_frequency(first_mode, second_mode)] += (
            kernel * outer(omega_fourier[first_mode], omega_fourier[second_mode])
        )

signed_contributions: list[dict[str, object]] = []
fourier_signed_work = sp.S.Zero
for mode, strain_coefficient in sorted(strain_fourier.items()):
    defect_coefficient = defect_fourier.get(
        negative_frequency(mode), sp.zeros(3, 3)
    )
    contribution = frobenius(strain_coefficient, defect_coefficient)
    fourier_signed_work = canonical(fourier_signed_work + contribution)
    if contribution != 0:
        signed_contributions.append(
            {
                "strainMode": list(mode),
                "strainShell": shell_label[mode],
                "contribution": scalar_payload(contribution),
            }
        )

fourier_expected = fixed_signed_expected
fourier_residual = canonical(fourier_signed_work - fourier_expected)
require(len(omega_fourier) == 36, "36 vorticity modes")
require(fourier_residual == 0, "Fourier signed-work reconstruction")
require(len(signed_contributions) > 0, "nonzero signed Fourier terms")

# The three axial strain placements make the cyclic cancellation transparent.
placement_common = sp.symbols("C", real=True)
placement_A_N = canonical(placement_common * audit_N / LN)
placement_A_M = canonical(-placement_common * audit_M / LM)
placement_A_1 = canonical(-placement_common / L1)
placement_cyclic_residual = canonical(
    LN * placement_A_N + LM * placement_A_M + L1 * placement_A_1
)
placement_weighted_block = canonical(
    placement_A_N + placement_A_M + physical_kappa * placement_A_1
)
placement_expected = canonical(placement_common * signed_bracket)
require(placement_cyclic_residual == 0, "sample cyclic cancellation")
require(
    canonical(placement_weighted_block - placement_expected) == 0,
    "sample beta oscillation",
)


payload = {
    "release": "R0.70X",
    "status": "cyclic-null-and-rank-at-most-one-signed-obstruction",
    "checks": {
        "cyclicTriadIdentity": True,
        "sharpHighHighLowFamily": True,
        "planarEigenfieldGeometry": True,
        "completeFrameRankOneCovariance": True,
        "physicalSignedWork": True,
        "fourierSignedWork": True,
    },
    "cyclicLedger": {
        "frequencyConstraint": "n+p+q=0",
        "divergenceResiduals": [
            scalar_payload(n_vector.dot(c_vector)),
            scalar_payload(p_vector.dot(a_vector)),
            scalar_payload(q_vector.dot(b_vector)),
        ],
        "identity": "|n|^2*A_n+|p|^2*A_p+|q|^2*A_q=0",
        "identityResidual": scalar_payload(cyclic_residual),
        "orderedFormula": "E_S=(1/2)*sum_(n+p+q=0; n,p,q!=0) K(p,q)*A_n",
        "cyclicFormula": "E_S=(1/6)*sum_(n+p+q=0; n,p,q!=0)[K(p,q)A_n+K(q,n)A_p+K(n,p)A_q]",
        "betaDefinition": "beta_n=K(p,q)/|n|^2 and cyclically",
        "differenceResidual": scalar_payload(
            cyclic_block - cyclic_difference_form
        ),
        "physicalNullIdentity": "integral (-Delta S(v)):(v tensor v)=0",
    },
    "sharpLedger": {
        "parameterPremise": "integer M>=3",
        "n": vector_payload(sharp_n),
        "p": vector_payload(sharp_p),
        "q": vector_payload(sharp_q),
        "c": vector_payload(sharp_c),
        "a": vector_payload(sharp_a),
        "b": vector_payload(sharp_b),
        "A": [
            scalar_payload(sharp_A_n),
            scalar_payload(sharp_A_p),
            scalar_payload(sharp_A_q),
        ],
        "cyclicResidual": scalar_payload(sharp_cyclic_residual),
        "block": scalar_payload(sharp_block),
        "blockExpected": scalar_payload(sharp_expected),
        "lowerBound": "kappa_M>=0 implies |block|>=1/sqrt(2*M^2+2*M+1)",
        "analyticResponseReading": "strict low/high separation gives the two low-high K factors equal to 1; smooth response gives kappa_M=O_phi(M^-2)",
        "sharpness": "the universal high-high-low gain cannot improve beyond t/R",
    },
    "fieldLedger": {
        "axis": vector_payload(axis),
        "planeModes": [vector_payload(mode) for mode in plane_modes],
        "planeResonanceResidual": vector_payload(
            plane_p + plane_q - plane_r
        ),
        "psi": "cos(p.x)+cos(q.x)+cos(r.x)",
        "w": "axis x grad(psi)",
        "divergenceW": scalar_payload(divergence_w),
        "axisDotW": scalar_payload(axis.dot(w_field)),
        "eigenResidual": vector_payload(eigen_residual),
        "psiCubeMean": scalar_payload(psi_cube_mean),
        "ARepresentationResidual": scalar_payload(A_field_residual),
        "Amean": scalar_payload(A_mean),
    },
    "covarianceLedger": {
        "singleShellRadiiSquared": [scalar_payload(L1), scalar_payload(LM), scalar_payload(LN)],
        "strictFactorFourSquaredSlacks": [
            scalar_payload(low_high_M_slack),
            scalar_payload(low_high_N_slack),
        ],
        "response": "Gamma_1M=Gamma_1N=0 and Gamma_MN=1-kappa",
        "defectScalar": scalar_payload(defect_scalar),
        "defectExpected": scalar_payload(defect_scalar_expected),
        "twoByTwoMinors": [scalar_payload(minor) for minor in covariance_minors],
        "rank": "rank(Q)<=1 everywhere because every Omega_alpha is a scalar multiple of w",
        "covarianceArea": "G_Q=0 everywhere",
        "topGapBoundary": "w vanishes at some points, so no uniformly positive top eigenvalue is asserted",
    },
    "signedLedger": {
        "premise": "M=6, N=7=M+1, real amplitudes a,b,c",
        "radiiSquared": [scalar_payload(L1), scalar_payload(LM), scalar_payload(LN)],
        "Amean": scalar_payload(A_mean),
        "axialMean": scalar_payload(axial_mean),
        "bracket": scalar_payload(signed_bracket),
        "adjacentFreePart": scalar_payload(adjacent_free_part),
        "generalWork": scalar_payload(signed_work_physical),
        "generalWorkExpected": scalar_payload(signed_work_expected),
        "fixedWork": scalar_payload(fixed_signed_work),
        "fixedWorkExpected": scalar_payload(fixed_signed_expected),
        "sign": "a*b*c>0 and kappa>=0 imply E_S<0",
    },
    "fourierLedger": {
        "modeCount": len(omega_fourier),
        "radiiByShell": {
            str(shell): radii for shell, radii in fourier_radii.items()
        },
        "defectOutputCount": len(defect_fourier),
        "nonzeroSignedContributionCount": len(signed_contributions),
        "nonzeroSignedContributions": signed_contributions,
        "signedWork": scalar_payload(fourier_signed_work),
        "signedWorkExpected": scalar_payload(fourier_expected),
        "difference": scalar_payload(fourier_residual),
        "placementCyclicResidual": scalar_payload(
            placement_cyclic_residual
        ),
        "placementWeightedBlock": scalar_payload(
            placement_weighted_block
        ),
        "placementExpected": scalar_payload(placement_expected),
    },
    "analyticDependencies": [
        "the complete scalar frame is real, even, radial, Parseval, and strictly supported in 1/2<|xi|<2",
        "strict factor-four radial separation makes the low-shell response orthogonal to both high-shell responses",
        "unit response vectors imply kappa=1-Gamma_MN>=0 by Cauchy--Schwarz",
        "choosing an admissible nonnegative cutoff gives Gamma_MN>=0, kappa in [0,1], and satisfies the response guard with sigma=1",
        "the infinite frame covariance reduces to the three response inner products used in the scalar Gram calculation",
        "the high-high-low t/R upper bound uses response log-smoothness and triangle inequalities from the report",
        "the standard all-mode cubic Lp estimate uses Riesz-transform and Littlewood--Paley square-function bounds",
        "no G_Q estimate is inferred from a separate-input or current norm estimate",
    ],
    "claimBoundary": [
        "proves the exact Laplacian-weighted cyclic null identity",
        "proves a sharp t/R gain for one high-high-low cyclic orbit",
        "rules out any signed-work estimate whose right side vanishes whenever G_Q=0 on the stated class",
        "rules out the nonnegative-frame branch of the R0.70W candidate |E_S|<=C*||grad omega||_2*||G_Q||_(6/5)",
        "does not rule out an estimate under a uniformly positive covariance top gap",
        "does not control the principal covariance stretching integral S:Q",
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
