#!/usr/bin/env python3
"""Exact finite audit for the R0.70W summation obstruction.

The producer checks seven narrowly scoped facts:

1. the exact divergence-free projected-wedge identity;
2. the Fourier geometry of the modulated planar field;
3. rank-one complete-frame covariance and zero physical response area;
4. the exact projected defect X_cross = 2*epsilon**2/729;
5. cancellation of the physical cross product at a representative output;
6. disjoint Fourier support of the actual strain and the frame defect; and
7. a three-shell resonant perturbation as a signed negative control.

The strict-annulus implication Gamma(1,sqrt(17))=0 and the passage from the
finite response model to the infinite pinned Parseval frame are analytic
arguments in the report.  This script does not prove a bilinear multiplier
theorem, a direct signed trilinear estimate, an enstrophy closure, or any
Navier--Stokes regularity conclusion.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import sympy as sp


Frequency = tuple[int, int, int]


def canonical(expression: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.expand(expression)))


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def add_frequency(first: Frequency, second: Frequency) -> Frequency:
    return tuple(first[index] + second[index] for index in range(3))  # type: ignore[return-value]


def negative_frequency(frequency: Frequency) -> Frequency:
    return tuple(-entry for entry in frequency)  # type: ignore[return-value]


def outer(first: sp.Matrix, second: sp.Matrix | None = None) -> sp.Matrix:
    if second is None:
        second = first
    return first * second.T


def matrix_is_zero(matrix: sp.Matrix) -> bool:
    return all(canonical(entry) == 0 for entry in matrix)


def scalar_payload(expression: sp.Expr) -> str:
    return str(canonical(expression))


def vector_payload(vector: sp.Matrix) -> list[str]:
    return [scalar_payload(entry) for entry in vector]


def matrix_payload(matrix: sp.Matrix) -> list[list[str]]:
    return [
        [scalar_payload(matrix[row, column]) for column in range(matrix.cols)]
        for row in range(matrix.rows)
    ]


e1 = sp.Matrix([1, 0, 0])
e2 = sp.Matrix([0, 1, 0])
e3 = sp.Matrix([0, 0, 1])


# ---------------------------------------------------------------------------
# 1. Exact divergence-free projected-wedge identity.
# ---------------------------------------------------------------------------

nmag = sp.symbols("nmag", positive=True, real=True)
px, py, pz = sp.symbols("px py pz", real=True)
a0x, a0y, a0z = sp.symbols("a0x a0y a0z", real=True)
b0x, b0y, b0z = sp.symbols("b0x b0y b0z", real=True)

n_vector = nmag * e1
p_vector = sp.Matrix([px, py, pz])
q_vector = n_vector - p_vector
a_vector = p_vector.cross(sp.Matrix([a0x, a0y, a0z]))
b_vector = q_vector.cross(sp.Matrix([b0x, b0y, b0z]))
wedge_vector = a_vector.cross(b_vector)
nu_vector = e1
polarized_tensor = outer(a_vector, b_vector) + outer(b_vector, a_vector)

projected_tensor = nu_vector.cross(polarized_tensor * nu_vector)
projected_wedge = -nu_vector.cross(
    (q_vector - p_vector).cross(wedge_vector)
) / nmag
projected_wedge_residual = (projected_tensor - projected_wedge).applyfunc(
    canonical
)
current_symbol = sp.I * outer(q_vector - p_vector, wedge_vector)
current_pair_from_definition = 2 * sp.I * (
    outer(q_vector, wedge_vector)
    + outer(p_vector, b_vector.cross(a_vector))
)
swapped_current_symbol = sp.I * outer(
    p_vector - q_vector,
    b_vector.cross(a_vector),
)
current_pair_from_symmetrization = current_symbol + swapped_current_symbol
current_pair_residual = (
    current_pair_from_definition - current_pair_from_symmetrization
).applyfunc(canonical)
current_projected = (
    sp.I
    * (current_symbol - current_symbol.T)
    * nu_vector
    / (2 * nmag)
)
current_projection_residual = (
    current_projected - projected_tensor / 2
).applyfunc(canonical)

require(canonical(p_vector.dot(a_vector)) == 0, "p divergence")
require(canonical(q_vector.dot(b_vector)) == 0, "q divergence")
require(matrix_is_zero(projected_wedge_residual), "projected-wedge identity")
require(
    matrix_is_zero(current_pair_residual),
    "current Fourier symmetrization",
)
require(
    matrix_is_zero(current_projection_residual),
    "antisymmetric current identity",
)


# ---------------------------------------------------------------------------
# 2. Exact field and its two radial supports.
# ---------------------------------------------------------------------------

x1, x2, x3 = sp.symbols("x1 x2 x3", real=True)
epsilon = sp.symbols("epsilon", nonzero=True, real=True)
g_scalar = sp.cos(4 * x3)
w_field = sp.Matrix([sp.cos(x2), -sp.cos(x1), 0])
h_field = g_scalar * w_field
omega_field = w_field + epsilon * h_field

divergence_w = canonical(
    sp.diff(w_field[0], x1)
    + sp.diff(w_field[1], x2)
    + sp.diff(w_field[2], x3)
)
divergence_h = canonical(
    sp.diff(h_field[0], x1)
    + sp.diff(h_field[1], x2)
    + sp.diff(h_field[2], x3)
)
require(divergence_w == 0, "w divergence")
require(divergence_h == 0, "h divergence")

low_radius_squared = sp.Integer(1)
high_radius_squared = sp.Integer(17)
strict_separation_slack = high_radius_squared - 16 * low_radius_squared
require(strict_separation_slack > 0, "strict factor-four separation")


# ---------------------------------------------------------------------------
# 3. Rank-one covariance and exact frame defect.
# ---------------------------------------------------------------------------

# Orthogonal response coordinates represent the two disjoint response
# supports after summing the complete frame.
omega_low_block = w_field
omega_high_block = epsilon * h_field
covariance = outer(omega_low_block) + outer(omega_high_block)
covariance_expected = (1 + epsilon**2 * g_scalar**2) * outer(w_field)
covariance_residual = (covariance - covariance_expected).applyfunc(canonical)
require(matrix_is_zero(covariance_residual), "rank-one covariance formula")

covariance_two_by_two_minors: list[sp.Expr] = []
for first_row in range(3):
    for second_row in range(first_row + 1, 3):
        for first_column in range(3):
            for second_column in range(first_column + 1, 3):
                minor = covariance.extract(
                    [first_row, second_row], [first_column, second_column]
                ).det()
                covariance_two_by_two_minors.append(canonical(minor))
require(
    all(minor == 0 for minor in covariance_two_by_two_minors),
    "covariance rank at most one",
)

physical_cross_product = omega_low_block.cross(omega_high_block)
require(matrix_is_zero(physical_cross_product), "physical response area zero")

defect = outer(omega_field) - covariance
defect_expected = 2 * epsilon * g_scalar * outer(w_field)
defect_residual = (defect - defect_expected).applyfunc(canonical)
require(matrix_is_zero(defect_residual), "exact frame defect")


# ---------------------------------------------------------------------------
# 4. Exact Fourier support and projected H^{-1} defect.
# ---------------------------------------------------------------------------

low_fourier: dict[Frequency, sp.Matrix] = {
    (0, 1, 0): e1 / 2,
    (0, -1, 0): e1 / 2,
    (1, 0, 0): -e2 / 2,
    (-1, 0, 0): -e2 / 2,
}
modulation_frequency: Frequency = (0, 0, 4)

high_fourier: defaultdict[Frequency, sp.Matrix] = defaultdict(
    lambda: sp.zeros(3, 1)
)
for frequency, coefficient in low_fourier.items():
    high_fourier[add_frequency(frequency, modulation_frequency)] += coefficient / 2
    high_fourier[
        add_frequency(frequency, negative_frequency(modulation_frequency))
    ] += coefficient / 2

defect_fourier: defaultdict[Frequency, sp.Matrix] = defaultdict(
    lambda: sp.zeros(3, 3)
)
for first_frequency, first_coefficient in low_fourier.items():
    for second_frequency, second_coefficient in low_fourier.items():
        for shift in (
            modulation_frequency,
            negative_frequency(modulation_frequency),
        ):
            output = add_frequency(
                add_frequency(first_frequency, second_frequency), shift
            )
            # 2*epsilon*g has Fourier coefficient epsilon at each shift.
            defect_fourier[output] += epsilon * outer(
                first_coefficient, second_coefficient
            )

projected_defect = sp.S.Zero
projected_nonzero_modes: list[dict[str, object]] = []
for output, coefficient in sorted(defect_fourier.items()):
    output_vector = sp.Matrix(output)
    output_square = canonical(output_vector.dot(output_vector))
    if output_square == 0:
        continue
    output_unit = output_vector / sp.sqrt(output_square)
    projected = output_unit.cross(coefficient * output_unit)
    projected_square = canonical(projected.dot(projected))
    contribution = canonical(projected_square / output_square)
    projected_defect = canonical(projected_defect + contribution)
    if contribution != 0:
        projected_nonzero_modes.append(
            {
                "frequency": list(output),
                "frequencySquared": scalar_payload(output_square),
                "defectCoefficient": matrix_payload(coefficient),
                "projectedCoefficient": vector_payload(projected),
                "projectedSquared": scalar_payload(projected_square),
                "XContribution": scalar_payload(contribution),
            }
        )

projected_expected = canonical(2 * epsilon**2 / 729)
require(
    canonical(projected_defect - projected_expected) == 0,
    "exact projected defect",
)
require(len(projected_nonzero_modes) == 8, "eight projected output modes")


# ---------------------------------------------------------------------------
# 5. A representative cancellation lost by tensor projection.
# ---------------------------------------------------------------------------

representative_output: Frequency = (1, 1, 4)
first_low = low_fourier[(0, 1, 0)]
first_high = high_fourier[(1, 0, 4)]
second_low = low_fourier[(1, 0, 0)]
second_high = high_fourier[(0, 1, 4)]

first_cross = first_low.cross(first_high)
second_cross = second_low.cross(second_high)
cross_cancellation = (first_cross + second_cross).applyfunc(canonical)
require(matrix_is_zero(cross_cancellation), "representative cross cancellation")

first_tensor = outer(first_low, first_high) + outer(first_high, first_low)
second_tensor = outer(second_low, second_high) + outer(
    second_high, second_low
)
representative_tensor = epsilon * (first_tensor + second_tensor)
representative_expected = -epsilon * (
    outer(e1, e2) + outer(e2, e1)
) / 4
require(
    matrix_is_zero(
        (representative_tensor - representative_expected).applyfunc(canonical)
    ),
    "representative tensor addition",
)
require(
    matrix_is_zero(
        (
            defect_fourier[representative_output]
            - representative_expected
        ).applyfunc(canonical)
    ),
    "representative Fourier coefficient",
)


# ---------------------------------------------------------------------------
# 6. The actual signed work vanishes by support separation.
# ---------------------------------------------------------------------------

omega_support = set(low_fourier) | set(high_fourier)
defect_support = {
    frequency
    for frequency, coefficient in defect_fourier.items()
    if not matrix_is_zero(coefficient)
}
support_overlap = sorted(omega_support & defect_support)
require(support_overlap == [], "strain-defect support disjointness")


# ---------------------------------------------------------------------------
# 7. General separated scale and a three-shell signed negative control.
# ---------------------------------------------------------------------------

M = sp.symbols("M", integer=True, positive=True)
eta = sp.symbols("eta", real=True)
gamma_23 = sp.symbols("gamma_23", real=True)
K_23 = 1 - gamma_23

general_modulation = (0, 0, M)
general_defect_fourier: defaultdict[
    tuple[sp.Expr | int, ...], sp.Matrix
] = defaultdict(lambda: sp.zeros(3, 3))
for first_frequency, first_coefficient in low_fourier.items():
    for second_frequency, second_coefficient in low_fourier.items():
        for shift in (
            general_modulation,
            negative_frequency(general_modulation),
        ):
            output = add_frequency(
                add_frequency(first_frequency, second_frequency), shift
            )
            general_defect_fourier[output] += epsilon * outer(
                first_coefficient, second_coefficient
            )

general_defect_mode_count = 0
general_projected_modes: list[dict[str, object]] = []
general_X = sp.S.Zero
for frequency, coefficient in general_defect_fourier.items():
    if matrix_is_zero(coefficient):
        continue
    general_defect_mode_count += 1
    general_output = sp.Matrix(frequency)
    general_output_square = canonical(general_output.dot(general_output))
    general_output_unit = general_output / sp.sqrt(general_output_square)
    general_projected_coefficient = general_output_unit.cross(
        coefficient * general_output_unit
    )
    general_projected_square = canonical(
        general_projected_coefficient.dot(general_projected_coefficient)
    )
    contribution = canonical(
        general_projected_square / general_output_square
    )
    general_X = canonical(general_X + contribution)
    if contribution != 0:
        general_projected_modes.append(
            {
                "frequency": [str(entry) for entry in frequency],
                "frequencySquared": scalar_payload(general_output_square),
                "defectCoefficient": matrix_payload(coefficient),
                "projectedSquared": scalar_payload(
                    general_projected_square
                ),
                "XContribution": scalar_payload(contribution),
            }
        )
general_X_expected = canonical(epsilon**2 * M**2 / (M**2 + 2) ** 3)
require(
    canonical(general_X - general_X_expected) == 0,
    "general separated-scale projected defect",
)
require(general_defect_mode_count == 18, "eighteen general defect modes")
require(len(general_projected_modes) == 8, "eight general projected modes")


def strain_symbol(
    frequency: tuple[sp.Expr | int, sp.Expr | int, sp.Expr | int],
    coefficient: sp.Matrix,
) -> sp.Matrix:
    frequency_vector = sp.Matrix(frequency)
    frequency_square = canonical(frequency_vector.dot(frequency_vector))
    rotated = frequency_vector.cross(coefficient)
    return -(
        outer(frequency_vector, rotated)
        + outer(rotated, frequency_vector)
    ) / (2 * frequency_square)


def add_symmetric_shell_pair(
    target: defaultdict[tuple[sp.Expr | int, ...], sp.Matrix],
    first_shell: dict | defaultdict,
    second_shell: dict | defaultdict,
    scalar: sp.Expr,
) -> None:
    for first_frequency, first_coefficient in first_shell.items():
        for second_frequency, second_coefficient in second_shell.items():
            output = add_frequency(first_frequency, second_frequency)
            target[output] += scalar * (
                outer(first_coefficient, second_coefficient)
                + outer(second_coefficient, first_coefficient)
            )


def cross_product_fourier(
    first_shell: dict | defaultdict,
    second_shell: dict | defaultdict,
) -> defaultdict[tuple[sp.Expr | int, ...], sp.Matrix]:
    result: defaultdict[tuple[sp.Expr | int, ...], sp.Matrix] = defaultdict(
        lambda: sp.zeros(3, 1)
    )
    for first_frequency, first_coefficient in first_shell.items():
        for second_frequency, second_coefficient in second_shell.items():
            output = add_frequency(first_frequency, second_frequency)
            result[output] += first_coefficient.cross(second_coefficient)
    return result


def hdot_minus_one_vector_square(
    coefficients: dict | defaultdict,
) -> sp.Expr:
    total = sp.S.Zero
    for frequency, coefficient in coefficients.items():
        frequency_vector = sp.Matrix(frequency)
        frequency_square = canonical(frequency_vector.dot(frequency_vector))
        if frequency_square == 0:
            require(matrix_is_zero(coefficient), "zero-mode cross coefficient")
            continue
        total += coefficient.dot(coefficient) / frequency_square
    return canonical(total)


def hdot_minus_one_vector_inner(
    first: dict | defaultdict,
    second: dict | defaultdict,
) -> sp.Expr:
    total = sp.S.Zero
    for frequency in set(first) | set(second):
        frequency_vector = sp.Matrix(frequency)
        frequency_square = canonical(frequency_vector.dot(frequency_vector))
        first_coefficient = first.get(frequency, sp.zeros(3, 1))
        second_coefficient = second.get(frequency, sp.zeros(3, 1))
        if frequency_square == 0:
            require(
                matrix_is_zero(first_coefficient)
                or matrix_is_zero(second_coefficient),
                "zero-mode cross inner product",
            )
            continue
        total += first_coefficient.dot(second_coefficient) / frequency_square
    return canonical(total)


general_high: defaultdict[tuple[sp.Expr | int, ...], sp.Matrix] = defaultdict(
    lambda: sp.zeros(3, 1)
)
for frequency, coefficient in low_fourier.items():
    general_high[add_frequency(frequency, general_modulation)] += coefficient / 2
    general_high[
        add_frequency(frequency, negative_frequency(general_modulation))
    ] += coefficient / 2

resonant_frequency = (1, 1, M)
resonant_polarization = e1 - e2
resonant_unit_shell = {
    resonant_frequency: resonant_polarization / 2,
    negative_frequency(resonant_frequency): resonant_polarization / 2,
}

general_omega: defaultdict[tuple[sp.Expr | int, ...], sp.Matrix] = defaultdict(
    lambda: sp.zeros(3, 1)
)
for frequency, coefficient in low_fourier.items():
    general_omega[frequency] += coefficient
for frequency, coefficient in general_high.items():
    general_omega[frequency] += epsilon * coefficient
for frequency, coefficient in resonant_unit_shell.items():
    general_omega[frequency] += eta * coefficient

general_defect: defaultdict[tuple[sp.Expr | int, ...], sp.Matrix] = defaultdict(
    lambda: sp.zeros(3, 3)
)
add_symmetric_shell_pair(
    general_defect, low_fourier, general_high, epsilon
)
add_symmetric_shell_pair(
    general_defect, low_fourier, resonant_unit_shell, eta
)
add_symmetric_shell_pair(
    general_defect,
    general_high,
    resonant_unit_shell,
    epsilon * eta * K_23,
)

resonant_signed_work = sp.S.Zero
resonant_nonzero_contributions: list[dict[str, object]] = []
for frequency, coefficient in general_omega.items():
    strain_coefficient = strain_symbol(frequency, coefficient)
    defect_coefficient = general_defect.get(
        negative_frequency(frequency), sp.zeros(3, 3)
    )
    contribution = canonical(
        sum(
            strain_coefficient[row, column]
            * defect_coefficient[row, column]
            for row in range(3)
            for column in range(3)
        )
    )
    resonant_signed_work = canonical(resonant_signed_work + contribution)
    if contribution != 0:
        resonant_nonzero_contributions.append(
            {
                "frequency": [str(entry) for entry in frequency],
                "contribution": scalar_payload(contribution),
            }
        )

resonant_signed_expected = canonical(
    -epsilon * eta * M / (2 * (M**2 + 1) * (M**2 + 2))
)
require(
    canonical(resonant_signed_work - resonant_signed_expected) == 0,
    "three-shell resonant signed work",
)
require(
    not resonant_signed_work.has(gamma_23),
    "resonant signed work independent of adjacent response",
)

w_cross_z = cross_product_fourier(low_fourier, resonant_unit_shell)
h_cross_z = cross_product_fourier(general_high, resonant_unit_shell)
area_13 = hdot_minus_one_vector_square(w_cross_z)
area_23 = hdot_minus_one_vector_square(h_cross_z)
area_13_expected = canonical(
    (M**2 + 3) / (2 * (M**2 + 1) * (M**2 + 5))
)
area_23_expected = canonical(
    (2 * M**2 + 3)
    * (12 * M**2 + 5)
    / (20 * (4 * M**2 + 1) * (4 * M**2 + 5))
)
require(canonical(area_13 - area_13_expected) == 0, "area A13")
require(canonical(area_23 - area_23_expected) == 0, "area A23")

response_gram = {
    (1, 1): sp.Integer(1),
    (2, 2): sp.Integer(1),
    (3, 3): sp.Integer(1),
    (1, 2): sp.Integer(0),
    (1, 3): sp.Integer(0),
    (2, 3): gamma_23,
}


def gram_entry(first_index: int, second_index: int) -> sp.Expr:
    key = tuple(sorted((first_index, second_index)))
    return response_gram[key]


def response_wedge_inner(
    first_pair: tuple[int, int],
    second_pair: tuple[int, int],
) -> sp.Expr:
    first, second = first_pair
    third, fourth = second_pair
    return canonical(
        gram_entry(first, third) * gram_entry(second, fourth)
        - gram_entry(first, fourth) * gram_entry(second, third)
    )


response_area_13 = response_wedge_inner((1, 3), (1, 3))
response_area_23 = response_wedge_inner((2, 3), (2, 3))
response_wedge_mixed = response_wedge_inner((1, 3), (2, 3))
physical_area_mixed = hdot_minus_one_vector_inner(w_cross_z, h_cross_z)
resonant_area_hminus_one_direct = canonical(
    eta**2
    * (
        response_area_13 * area_13
        + epsilon**2 * response_area_23 * area_23
        + 2
        * epsilon
        * response_wedge_mixed
        * physical_area_mixed
    )
)
resonant_area_hminus_one_expected = canonical(
    eta**2 * (area_13_expected + epsilon**2 * response_area_23 * area_23_expected)
)
resonant_area_hminus_one_residual = canonical(
    resonant_area_hminus_one_direct - resonant_area_hminus_one_expected
)
require(response_area_13 == 1, "response wedge norm V1 wedge V3")
require(
    response_area_23 == canonical(1 - gamma_23**2),
    "response wedge norm V2 wedge V3",
)
require(
    response_wedge_mixed == 0,
    "mixed response wedge inner product",
)
require(physical_area_mixed == 0, "mixed physical H-minus-one product")
require(
    resonant_area_hminus_one_residual == 0,
    "full resonant response-area H-minus-one identity",
)

# The finite producer records the exact exponent arithmetic behind the
# analytic all-mode Sobolev estimate.  It does not machine-prove the Sobolev
# embedding or the near/far scalar inequalities.
space_dimension = sp.Integer(3)
vorticity_amplitude_degree = sp.Integer(2)
quarter_sobolev_degree = canonical(
    vorticity_amplitude_degree + sp.Rational(1, 4)
    - space_dimension / 2
)
quarter_sobolev_fourth_degree = canonical(4 * quarter_sobolev_degree)
interpolation_L2_power = canonical(2 * sp.Rational(3, 4))
interpolation_H1_power = canonical(2 * sp.Rational(1, 4))
signed_L2_power = interpolation_L2_power
signed_H1_power = canonical(interpolation_H1_power + 1)
require(
    quarter_sobolev_degree == sp.Rational(3, 4),
    "quarter Sobolev scaling",
)
require(
    quarter_sobolev_fourth_degree == 3,
    "quarter Sobolev fourth-power scaling",
)
require(
    signed_L2_power == sp.Rational(3, 2)
    and signed_H1_power == sp.Rational(3, 2),
    "signed interpolation powers",
)


payload = {
    "release": "R0.70W",
    "status": "far-shell-rank-one-projected-summation-obstruction",
    "checks": {
        "projectedWedgeIdentity": True,
        "fieldGeometry": True,
        "rankOneCovariance": True,
        "projectedDefect": True,
        "crossCancellationFailure": True,
        "signedSupportBoundary": True,
        "resonantNegativeControl": True,
    },
    "projectedWedgeLedger": {
        "frequencyConstraint": "n=p+q",
        "divergenceResiduals": [
            scalar_payload(p_vector.dot(a_vector)),
            scalar_payload(q_vector.dot(b_vector)),
        ],
        "identityResidual": matrix_payload(projected_wedge_residual),
        "identity": "nu_n x [(a tensor b+b tensor a)nu_n]=-|n|^-1 nu_n x [(q-p)x(a x b)]",
        "defectFormula": "Fhat(n)=-(2|n|)^-1 sum_(p+q=n) K(p,q) nu_n x [(q-p)x(omegahat(p)xomegahat(q))]",
        "currentProjectionResidual": matrix_payload(
            current_projection_residual
        ),
        "currentPairResidual": matrix_payload(current_pair_residual),
        "currentDefinition": "C_m=2*(omega x partial_m omega-sum_alpha Omega_alpha x partial_m Omega_alpha)",
        "currentFourier": "Chat(n)=i*sum_(p+q=n) K(p,q)*(q-p) tensor (omegahat(p) x omegahat(q))",
        "currentProjection": "Fhat(n)=i*[Chat(n)-Chat(n)^T]*nu_n/(2*|n|)",
    },
    "fieldLedger": {
        "w": "e1*cos(x2)-e2*cos(x1)",
        "g": "cos(4*x3)",
        "h": "g*w",
        "omega": "w+epsilon*h",
        "divergenceW": scalar_payload(divergence_w),
        "divergenceH": scalar_payload(divergence_h),
        "lowRadiusSquared": scalar_payload(low_radius_squared),
        "highRadiusSquared": scalar_payload(high_radius_squared),
        "strictFactorFourSquaredSlack": scalar_payload(strict_separation_slack),
        "lowModeCount": len(low_fourier),
        "highModeCount": len(high_fourier),
    },
    "covarianceLedger": {
        "responseReading": "strict annular support gives Gamma(1,sqrt(17))=0",
        "covariance": "Q=(1+epsilon^2*g^2)*(w tensor w)",
        "covarianceResidual": matrix_payload(covariance_residual),
        "twoByTwoMinors": [
            scalar_payload(minor) for minor in covariance_two_by_two_minors
        ],
        "physicalCrossProduct": vector_payload(physical_cross_product),
        "rank": "rank(Q)<=1 everywhere; rank(Q)=1 wherever w is nonzero",
        "eigenvalueResidual": "lambda2+lambda3=0 everywhere",
        "covarianceArea": "lambda1*r+lambda2*lambda3=0 everywhere",
    },
    "defectLedger": {
        "defect": "D_cross=2*epsilon*cos(4*x3)*(w tensor w)",
        "defectResidual": matrix_payload(defect_residual),
        "fourierModeCount": len(defect_support),
        "projectedNonzeroModeCount": len(projected_nonzero_modes),
        "projectedNonzeroModes": projected_nonzero_modes,
        "X": scalar_payload(projected_defect),
        "XExpected": scalar_payload(projected_expected),
    },
    "cancellationLedger": {
        "output": list(representative_output),
        "firstCross": vector_payload(first_cross),
        "secondCross": vector_payload(second_cross),
        "crossSum": vector_payload(cross_cancellation),
        "tensorSum": matrix_payload(representative_tensor),
        "tensorExpected": matrix_payload(representative_expected),
        "reading": "physical wedge pairs cancel before squaring, while the symmetric tensor pairs add",
    },
    "signedLedger": {
        "omegaSupportCount": len(omega_support),
        "defectSupportCount": len(defect_support),
        "supportOverlap": [list(frequency) for frequency in support_overlap],
        "signedWork": "integral S(omega):D_cross = 0 because S(omega) has omega Fourier support",
        "reading": "the sample disproves the projected majorant bridge but not a direct signed trilinear estimate",
    },
    "resonantLedger": {
        "premise": "integer M>=4; the low shell is response-orthogonal to the radius-sqrt(M^2+1) and radius-sqrt(M^2+2) shells",
        "generalExactRankX": scalar_payload(general_X),
        "generalExactRankXExpected": scalar_payload(general_X_expected),
        "generalDefectModeCount": general_defect_mode_count,
        "generalProjectedModeCount": len(general_projected_modes),
        "generalProjectedModes": general_projected_modes,
        "resonantMode": ["1", "1", "M"],
        "resonantPolarization": vector_payload(resonant_polarization),
        "nonzeroSignedContributions": resonant_nonzero_contributions,
        "signedWork": scalar_payload(resonant_signed_work),
        "signedWorkExpected": scalar_payload(resonant_signed_expected),
        "signedWorkAdjacentResponseDerivative": scalar_payload(
            sp.diff(resonant_signed_work, gamma_23)
        ),
        "A13": scalar_payload(area_13),
        "A13Expected": scalar_payload(area_13_expected),
        "A23": scalar_payload(area_23),
        "A23Expected": scalar_payload(area_23_expected),
        "responseArea13": scalar_payload(response_area_13),
        "responseArea23": scalar_payload(response_area_23),
        "responseWedgeMixed": scalar_payload(response_wedge_mixed),
        "physicalAreaMixed": scalar_payload(physical_area_mixed),
        "areaHdotMinusOne": scalar_payload(
            resonant_area_hminus_one_direct
        ),
        "areaHdotMinusOneExpected": scalar_payload(
            resonant_area_hminus_one_expected
        ),
        "areaHdotMinusOneResidual": scalar_payload(
            resonant_area_hminus_one_residual
        ),
        "asymptoticReading": "signedWork=O(epsilon*eta*M^-3), while sqrt(A13)=Theta(abs(eta)*M^-1); this finite family does not disprove a direct signed-area estimate",
    },
    "universalMajorantLedger": {
        "pairRadius": "R=max(|p|,|q|)",
        "farCase": "|p|<=R/2 gives K*(|p|+|q|)/|p+q|^2<=12/R",
        "nearCase": "|p|>R/2 gives K*(|p|+|q|)/|p+q|^2<=3*M_phi^2/R",
        "constant": "C0=max(12,3*M_phi^2)",
        "majorant": "U_-2=(1/4)*sum_(n!=0)[sum_(p+q=n) R^-1*|omegahat(p) x omegahat(q)|]^2",
        "projectedBound": "X_cross<=C0^2*U_-2",
        "sobolevBound": "sqrt(U_-2)<=(C_S4^2/2)*||omega||_Hdot(1/4)^2",
        "quarterSobolevDegree": scalar_payload(quarter_sobolev_degree),
        "quarterSobolevFourthDegree": scalar_payload(
            quarter_sobolev_fourth_degree
        ),
        "signedInterpolationPowers": {
            "L2": scalar_payload(signed_L2_power),
            "H1": scalar_payload(signed_H1_power),
        },
        "closureBoundary": "Young returns nu*||grad omega||_2^2/2+C_phi*nu^-3*||omega||_2^6; this is not a large-data closure",
    },
    "analyticDependencies": [
        "strict support in 1/2<|xi|<2 makes response supports at radii 1 and sqrt(17)>4 disjoint",
        "the constant Pi_0 channel vanishes on both mean-zero radial supports",
        "the infinite Parseval-frame covariance reduces analytically to the two orthogonal response coordinates used here",
        "Biot--Savart strain is a Fourier multiplier and therefore has exactly the nonzero omega support",
        "no vector-valued bilinear or trilinear multiplier estimate is inferred from the finite calculation",
        "the near/far pair bound, convolution estimate, Parseval identity, and Hdot(3/4)-to-L4 Sobolev embedding are analytic",
    ],
    "claimBoundary": [
        "rules out control of X_cross by any definite norm of the physical covariance-area field alone",
        "rules out the scale-correct L^(6/5) covariance-area candidate for X_cross",
        "does not rule out a direct signed trilinear covariance-area estimate",
        "does not produce nonzero signed work at exact rank one",
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
