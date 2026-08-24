#!/usr/bin/env python3
"""Exact symbolic audit for the R0.70O rank-strata bridge gate.

The producer verifies five finite groups:

1. simple-spectrum eigenvalue, eigenvector, and projector evolution;
2. exact best-plane and best-line finite-frame variational identities;
3. an explicit Bessel-filtered global Navier--Stokes shear obstruction;
4. coercive/near-plane/near-line gap certificates; and
5. fixed-projection Fourier lower-frame reconstruction identities.

All recorded arithmetic is exact SymPy arithmetic.  The arbitrary-measure
Rayleigh--Ritz theorem, infinite-series endpoint argument, and arbitrary
filter-family extensions are proved analytically in the canonical report;
they are not presented as computer proofs.
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


def matrix_payload(matrix: sp.Matrix) -> list[list[str]]:
    return [
        [str(sp.factor(matrix[row, column])) for column in range(matrix.cols)]
        for row in range(matrix.rows)
    ]


def scalar_payload(value: sp.Expr) -> str:
    return str(sp.factor(value))


def divergence(vector: sp.Matrix, coordinates: tuple[sp.Symbol, ...]) -> sp.Expr:
    return sp.simplify(
        sum(sp.diff(vector[index], coordinates[index]) for index in range(3))
    )


def laplacian(vector: sp.Matrix, coordinates: tuple[sp.Symbol, ...]) -> sp.Matrix:
    return vector.applyfunc(
        lambda component: sp.simplify(
            sum(
                sp.diff(component, coordinate, 2)
                for coordinate in coordinates
            )
        )
    )


def advective_derivative(
    vector: sp.Matrix, coordinates: tuple[sp.Symbol, ...]
) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.simplify(
                sum(
                    vector[axis] * sp.diff(vector[index], coordinates[axis])
                    for axis in range(3)
                )
            )
            for index in range(3)
        ]
    )


def curl(vector: sp.Matrix, coordinates: tuple[sp.Symbol, ...]) -> sp.Matrix:
    x, y, z = coordinates
    return sp.Matrix(
        [
            sp.diff(vector[2], y) - sp.diff(vector[1], z),
            sp.diff(vector[0], z) - sp.diff(vector[2], x),
            sp.diff(vector[1], x) - sp.diff(vector[0], y),
        ]
    ).applyfunc(sp.simplify)


# ---------------------------------------------------------------------------
# 1. Exact simple-spectrum evolution ledger.
# ---------------------------------------------------------------------------

lambda_symbols = sp.symbols("lambda1 lambda2 lambda3", real=True)
s11, s12, s13, s22, s23, s33 = sp.symbols(
    "s11 s12 s13 s22 s23 s33", real=True
)
f11, f12, f13, f22, f23, f33 = sp.symbols(
    "f11 f12 f13 f22 f23 f33", real=True
)

Q_symbolic = sp.diag(*lambda_symbols)
Sigma_symbolic = sp.Matrix(
    [[s11, s12, s13], [s12, s22, s23], [s13, s23, s33]]
)
F_symbolic = sp.Matrix(
    [[f11, f12, f13], [f12, f22, f23], [f13, f23, f33]]
)
Qdot_symbolic = sp.expand(
    Sigma_symbolic * Q_symbolic
    + Q_symbolic * Sigma_symbolic
    + F_symbolic
)
projectors = [sp.diag(1, 0, 0), sp.diag(0, 1, 0), sp.diag(0, 0, 1)]

eigenvalue_rates_symbolic = [
    sp.simplify(2 * lambda_symbols[index] * Sigma_symbolic[index, index]
                + F_symbolic[index, index])
    for index in range(3)
]
require(
    all(
        sp.simplify(Qdot_symbolic[index, index] - eigenvalue_rates_symbolic[index])
        == 0
        for index in range(3)
    ),
    "symbolic eigenvalue rates",
)

projector_rates_symbolic: list[sp.Matrix] = []
for index in range(3):
    rate = sp.zeros(3)
    for other in range(3):
        if other == index:
            continue
        numerator = (
            (lambda_symbols[index] + lambda_symbols[other])
            * (
                projectors[other] * Sigma_symbolic * projectors[index]
                + projectors[index] * Sigma_symbolic * projectors[other]
            )
            + projectors[other] * F_symbolic * projectors[index]
            + projectors[index] * F_symbolic * projectors[other]
        )
        rate += numerator / (lambda_symbols[index] - lambda_symbols[other])
    projector_rates_symbolic.append(rate.applyfunc(sp.factor))

require(
    matrix_is_zero(sum(projector_rates_symbolic, sp.zeros(3))),
    "symbolic projector partition derivative",
)

Q_sample = sp.diag(7, 3, 1)
Sigma_sample = sp.Matrix([[2, 1, -2], [1, -1, 3], [-2, 3, 0]])
F_sample = sp.Matrix([[5, -1, 4], [-1, 2, -2], [4, -2, 3]])
Qdot_sample = Sigma_sample * Q_sample + Q_sample * Sigma_sample + F_sample
Qdot_expected = sp.Matrix([[33, 9, -12], [9, -4, 10], [-12, 10, 3]])
require(matrix_equal(Qdot_sample, Qdot_expected), "rational Qdot sample")

sample_substitutions = {
    lambda_symbols[0]: 7,
    lambda_symbols[1]: 3,
    lambda_symbols[2]: 1,
    s11: 2,
    s12: 1,
    s13: -2,
    s22: -1,
    s23: 3,
    s33: 0,
    f11: 5,
    f12: -1,
    f13: 4,
    f22: 2,
    f23: -2,
    f33: 3,
}
projector_rates_sample = [
    rate.subs(sample_substitutions).applyfunc(sp.simplify)
    for rate in projector_rates_symbolic
]
projector_rates_expected = [
    sp.Matrix([[0, sp.Rational(9, 4), -2], [sp.Rational(9, 4), 0, 0], [-2, 0, 0]]),
    sp.Matrix([[0, -sp.Rational(9, 4), 0], [-sp.Rational(9, 4), 0, 5], [0, 5, 0]]),
    sp.Matrix([[0, 0, 2], [0, 0, -5], [2, -5, 0]]),
]
require(
    all(
        matrix_equal(actual, expected)
        for actual, expected in zip(projector_rates_sample, projector_rates_expected)
    ),
    "rational projector rate samples",
)
require(
    matrix_is_zero(sum(projector_rates_sample, sp.zeros(3))),
    "rational projector rate sum",
)

eigenvector_rate_columns = sp.Matrix(
    [
        [0, -sp.Rational(9, 4), 2],
        [sp.Rational(9, 4), 0, -5],
        [-2, 5, 0],
    ]
)
require(
    matrix_equal(
        eigenvector_rate_columns + eigenvector_rate_columns.T, sp.zeros(3)
    ),
    "orthonormal eigenframe derivative",
)

trace_sample = sp.trace(Q_sample)
trace_rate_sample = sp.trace(Qdot_sample)
plane_ratio_sample = sp.Rational(1, 11)
line_ratio_sample = sp.Rational(4, 11)
plane_ratio_rate_sample = sp.simplify(
    (Qdot_sample[2, 2] * trace_sample - Q_sample[2, 2] * trace_rate_sample)
    / trace_sample**2
)
line_ratio_rate_sample = sp.simplify(
    (
        (Qdot_sample[1, 1] + Qdot_sample[2, 2]) * trace_sample
        - (Q_sample[1, 1] + Q_sample[2, 2]) * trace_rate_sample
    )
    / trace_sample**2
)
require(plane_ratio_rate_sample == sp.Rational(1, 121), "plane ratio rate")
require(line_ratio_rate_sample == -sp.Rational(139, 121), "line ratio rate")

s = sp.symbols("s", real=True)
Q_interior_boundary = sp.diag(7, 3, s**2)
Q_endpoint_boundary = sp.diag(7, 3, s)
require(
    sp.diff(Q_interior_boundary[2, 2], s).subs(s, 0) == 0,
    "interior PSD boundary tangent",
)
require(
    sp.diff(Q_endpoint_boundary[2, 2], s).subs(s, 0) == 1,
    "endpoint PSD boundary tangent",
)


# ---------------------------------------------------------------------------
# 2. Exact finite-frame best-plane and best-line certificates.
# ---------------------------------------------------------------------------

rotation = sp.Matrix(
    [
        [sp.Rational(2, 3), -sp.Rational(2, 3), sp.Rational(1, 3)],
        [sp.Rational(2, 3), sp.Rational(1, 3), -sp.Rational(2, 3)],
        [sp.Rational(1, 3), sp.Rational(2, 3), sp.Rational(2, 3)],
    ]
)
require(matrix_equal(rotation.T * rotation, sp.eye(3)), "rational rotation")
Q_rotated = rotation * sp.diag(7, 3, 1) * rotation.T
Q_rotated_expected = sp.Matrix(
    [
        [sp.Rational(41, 9), sp.Rational(20, 9), sp.Rational(4, 9)],
        [sp.Rational(20, 9), sp.Rational(35, 9), sp.Rational(16, 9)],
        [sp.Rational(4, 9), sp.Rational(16, 9), sp.Rational(23, 9)],
    ]
)
require(matrix_equal(Q_rotated, Q_rotated_expected), "rotated covariance")

n1, n2, n3 = sp.symbols("n1 n2 n3", real=True)
l1, l2, l3 = sp.symbols("ell1 ell2 ell3", real=True)
n_vector = sp.Matrix([n1, n2, n3])
ell_vector = sp.Matrix([l1, l2, l3])
n_coordinates = rotation.T * n_vector
ell_coordinates = rotation.T * ell_vector

plane_sos = sp.expand(
    (n_vector.T * Q_rotated * n_vector)[0] - (n_vector.T * n_vector)[0]
)
plane_sos_expected = sp.expand(
    6 * n_coordinates[0] ** 2 + 2 * n_coordinates[1] ** 2
)
require(sp.simplify(plane_sos - plane_sos_expected) == 0, "best-plane SOS")

line_sos = sp.expand(
    sp.trace(Q_rotated) * (ell_vector.T * ell_vector)[0]
    - (ell_vector.T * Q_rotated * ell_vector)[0]
    - 4 * (ell_vector.T * ell_vector)[0]
)
line_sos_expected = sp.expand(
    4 * ell_coordinates[1] ** 2 + 6 * ell_coordinates[2] ** 2
)
require(sp.simplify(line_sos - line_sos_expected) == 0, "best-line SOS")

best_plane_normal = rotation[:, 2]
best_line_axis = rotation[:, 0]
require(
    sp.simplify((best_plane_normal.T * Q_rotated * best_plane_normal)[0]) == 1,
    "best-plane residual",
)
require(
    sp.simplify(
        sp.trace(Q_rotated)
        - (best_line_axis.T * Q_rotated * best_line_axis)[0]
    )
    == 4,
    "best-line residual",
)


# ---------------------------------------------------------------------------
# 3. Explicit Bessel-filtered exact NSE dynamic obstruction.
# ---------------------------------------------------------------------------

x, y, z, t = sp.symbols("x y z t", real=True)
T_horizon = sp.symbols("T", positive=True, real=True)
N = sp.symbols("N", integer=True, positive=True)
nu = sp.symbols("nu", positive=True, real=True)
a = sp.symbols("a", positive=True, real=True)
coordinates = (x, y, z)

u_dynamic = sp.Matrix(
    [
        a * sp.exp(-nu * t) * sp.sin(y),
        0,
        N ** sp.Rational(-1, 2)
        * sp.exp(-nu * N**2 * t)
        * sp.sin(N * y),
    ]
)
require(divergence(u_dynamic, coordinates) == 0, "dynamic shear divergence")
require(
    matrix_is_zero(advective_derivative(u_dynamic, coordinates)),
    "dynamic shear nonlinearity",
)
require(
    matrix_is_zero(
        sp.diff(u_dynamic, t) - nu * laplacian(u_dynamic, coordinates)
    ),
    "dynamic shear heat equation",
)
omega_dynamic = curl(u_dynamic, coordinates)
omega_dynamic_expected = sp.Matrix(
    [
        sp.sqrt(N) * sp.exp(-nu * N**2 * t) * sp.cos(N * y),
        0,
        -a * sp.exp(-nu * t) * sp.cos(y),
    ]
)
require(
    matrix_equal(omega_dynamic, omega_dynamic_expected),
    "dynamic shear vorticity",
)

A_low = sp.Rational(1, 4)
A_high = 1 / (1 + N**2) ** 2
kappa = sp.Integer(2)
a_squared = sp.simplify((1 + kappa * N * A_high) / A_low)
q_transverse = sp.simplify(
    N * A_high * sp.exp(-2 * nu * N**2 * t) / 2
)
q_principal = sp.simplify(
    (1 + kappa * N * A_high) * sp.exp(-2 * nu * t) / 2
)
principal_ratio_at_zero = sp.simplify(
    q_principal.subs(t, 0) / q_transverse.subs(t, 0)
)
require(
    sp.simplify(principal_ratio_at_zero - (2 + 1 / (N * A_high))) == 0,
    "principal eigenvalue dominance ratio",
)

best_line_residual = q_transverse
residual_l2_time_squared = sp.simplify(
    sp.integrate(best_line_residual**2, (t, 0, sp.oo))
)
require(
    residual_l2_time_squared == A_high**2 / (16 * nu),
    "residual L2 time norm",
)
transverse_l2_squared = N * sp.exp(-2 * nu * N**2 * t) / 2
transverse_l4_l2_fourth_power = sp.simplify(
    sp.integrate(transverse_l2_squared**2, (t, 0, sp.oo))
)
require(
    transverse_l4_l2_fourth_power == 1 / (16 * nu),
    "unfiltered transverse critical norm",
)

finite_horizon_factor = 1 - sp.exp(-4 * nu * N**2 * T_horizon)
finite_horizon_residual_l2_squared = sp.simplify(
    A_high**2 * finite_horizon_factor / (16 * nu)
)
finite_horizon_transverse_l4_fourth = sp.simplify(
    finite_horizon_factor / (16 * nu)
)
require(
    sp.simplify(
        finite_horizon_transverse_l4_fourth
        / finite_horizon_residual_l2_squared
        - 1 / A_high**2
    )
    == 0,
    "finite-horizon squared instability ratio",
)

line_ratio_at_zero = sp.simplify(
    q_transverse.subs(t, 0)
    / (q_transverse.subs(t, 0) + q_principal.subs(t, 0))
)
line_ratio_gap_to_one_third = sp.simplify(sp.Rational(1, 3) - line_ratio_at_zero)
require(
    sp.simplify(
        line_ratio_gap_to_one_third - 1 / (3 * (1 + 3 * N * A_high))
    )
    == 0,
    "near-line ratio bound",
)
require(sp.limit(A_high, N, sp.oo) == 0, "Bessel response decay")
require(sp.limit(N * A_high, N, sp.oo) == 0, "bounded low-mode amplitude")

calibration_substitutions = {N: 8, nu: sp.Rational(3, 2)}
calibrated_a_squared = sp.simplify(a_squared.subs(calibration_substitutions))
calibrated_residual_norm_squared = sp.simplify(
    residual_l2_time_squared.subs(calibration_substitutions)
)
calibrated_transverse_fourth = sp.simplify(
    transverse_l4_l2_fourth_power.subs(calibration_substitutions)
)

# Direct Fourier integration at N=8 independently recovers both nonzero
# covariance entries from the Bessel-filtered vorticity at t=0.
calibration_frequency = sp.Integer(8)
calibration_low_multiplier = sp.Rational(1, 2)
calibration_high_multiplier = sp.Rational(1, 65)
calibration_amplitude = sp.sqrt(a_squared.subs(N, calibration_frequency))
filtered_vorticity_at_zero = sp.Matrix(
    [
        sp.sqrt(calibration_frequency)
        * calibration_high_multiplier
        * sp.cos(calibration_frequency * y),
        0,
        -calibration_amplitude * calibration_low_multiplier * sp.cos(y),
    ]
)
fourier_covariance_at_zero = sp.Matrix(
    3,
    3,
    lambda row, column: sp.simplify(
        sp.integrate(
            filtered_vorticity_at_zero[row]
            * filtered_vorticity_at_zero[column],
            (y, 0, 2 * sp.pi),
        )
        / (2 * sp.pi)
    ),
)
fourier_covariance_expected = sp.diag(
    q_transverse.subs({N: calibration_frequency, t: 0}),
    0,
    q_principal.subs({N: calibration_frequency, t: 0}),
)
require(
    matrix_equal(fourier_covariance_at_zero, fourier_covariance_expected),
    "direct Bessel-filtered Fourier covariance",
)

# Finite compact-band dyadic approximants certify the diagonal lower bound
# used by the analytical infinite-series/Tonelli argument in the report.
hidden_frequencies = [sp.Integer(2) ** exponent for exponent in range(4, 16)]
nu_calibration = sp.Rational(3, 2)
full_dyadic_fourth_power = sp.simplify(
    sum(
        first * second / (first**2 + second**2)
        for first in hidden_frequencies
        for second in hidden_frequencies
    )
    / (8 * nu_calibration)
)
diagonal_dyadic_lower_bound = sp.Rational(len(hidden_frequencies), 1) / (
    16 * nu_calibration
)
require(
    full_dyadic_fourth_power >= diagonal_dyadic_lower_bound,
    "finite dyadic critical lower bound",
)


# ---------------------------------------------------------------------------
# 4. Exact spectral trichotomy and gap certificates.
# ---------------------------------------------------------------------------

L1, L2, L3, delta, eta = sp.symbols(
    "L1 L2 L3 delta eta", nonnegative=True, real=True
)
energy = L1 + L2 + L3
near_line_slack = eta * energy - L2 - L3
near_line_gap_identity = sp.expand(
    (L1 - L2) - (1 - 2 * eta) * energy
)
near_line_gap_certificate = sp.expand(2 * near_line_slack + L3)
require(
    sp.simplify(near_line_gap_identity - near_line_gap_certificate) == 0,
    "near-line Farkas certificate",
)

near_plane_sum_slack = L2 + L3 - eta * energy
near_plane_normal_slack = delta * energy - L3
near_plane_gap_identity = sp.expand(
    (L2 - L3) - (eta - 2 * delta) * energy
)
near_plane_gap_certificate = sp.expand(
    near_plane_sum_slack + 2 * near_plane_normal_slack
)
require(
    sp.simplify(near_plane_gap_identity - near_plane_gap_certificate) == 0,
    "near-plane Farkas certificate",
)

delta_sample = sp.Rational(1, 20)
eta_sample = sp.Rational(2, 5)
coercive_spectrum = (sp.Integer(8), sp.Integer(4), sp.Integer(2))
near_plane_spectrum = (sp.Integer(6), sp.Integer(5), sp.Rational(1, 10))
near_line_spectrum = (sp.Integer(10), sp.Integer(1), sp.Rational(1, 10))


def classify_spectrum(spectrum: tuple[sp.Expr, sp.Expr, sp.Expr]) -> str:
    first, second, third = spectrum
    total = first + second + third
    if third / total >= delta_sample:
        return "coercive"
    if (second + third) / total <= eta_sample:
        return "near-line"
    return "near-plane"


require(classify_spectrum(coercive_spectrum) == "coercive", "coercive sample")
require(
    classify_spectrum(near_plane_spectrum) == "near-plane",
    "near-plane sample",
)
require(classify_spectrum(near_line_spectrum) == "near-line", "near-line sample")

near_plane_energy = sum(near_plane_spectrum)
near_line_energy = sum(near_line_spectrum)
require(
    near_plane_spectrum[1] - near_plane_spectrum[2]
    > (eta_sample - 2 * delta_sample) * near_plane_energy,
    "near-plane sample gap",
)
require(
    near_line_spectrum[0] - near_line_spectrum[1]
    >= (1 - 2 * eta_sample) * near_line_energy,
    "near-line sample gap",
)


# ---------------------------------------------------------------------------
# 5. Exact fixed-projection Fourier reconstruction gate.
# ---------------------------------------------------------------------------

frequencies = [sp.Integer(1), sp.Integer(3), sp.Integer(5)]
coefficients = [sp.Integer(2), sp.Integer(-1), sp.Integer(3)]
responses = [sp.Rational(1, 2), sp.Rational(1, 4), sp.Rational(1, 10)]
l2_squared = sum(coefficient**2 for coefficient in coefficients)
observed_energy = sum(
    response * coefficient**2
    for response, coefficient in zip(responses, coefficients)
)
l2_lower_frame_constant = min(responses)
l2_slack = sp.simplify(
    observed_energy - l2_lower_frame_constant * l2_squared
)
require(l2_slack == sp.Rational(7, 4), "finite L2 lower-frame slack")

h_minus_half_squared = sum(
    coefficient**2 / frequency
    for frequency, coefficient in zip(frequencies, coefficients)
)
h_minus_half_lower_frame_constant = min(
    response * frequency
    for response, frequency in zip(responses, frequencies)
)
h_minus_half_slack = sp.simplify(
    observed_energy
    - h_minus_half_lower_frame_constant * h_minus_half_squared
)
require(
    h_minus_half_slack == sp.Rational(1, 12),
    "finite H-minus-half lower-frame slack",
)

a0, X, slack = sp.symbols("a0 X slack", positive=True, real=True)
R = a0 * X + slack
time_bridge_slack = sp.factor(R**2 / a0**2 - X**2)
time_bridge_expected = sp.factor(2 * X * slack / a0 + slack**2 / a0**2)
require(
    sp.simplify(time_bridge_slack - time_bridge_expected) == 0,
    "time-integrated lower-frame bridge",
)

blind_coefficient = sp.Integer(7)
blind_response = sp.Integer(0)
require(blind_response * blind_coefficient**2 == 0, "blind observed energy")
require(blind_coefficient**2 > 0, "blind unfiltered energy")


checks = {
    "spectralProjectorLedger": True,
    "bestSubspaceVariationalLedger": True,
    "dynamicFilterObstruction": True,
    "spectralGapCertificates": True,
    "linearReconstructionGate": True,
}

payload = {
    "release": "R0.70O",
    "status": "exact-rank-strata-bridge-audit",
    "arithmetic": (
        "exact SymPy symbolic, rational, trigonometric, matrix, "
        "and improper-integral arithmetic"
    ),
    "checks": checks,
    "spectralProjectorLedger": {
        "equation": "Qdot=Sigma*Q+Q*Sigma+F, with symmetric inputs",
        "eigenvalueRate": "2*lambda_a*Sigma_aa+F_aa",
        "eigenvectorRate": (
            "((lambda_a+lambda_b)*Sigma_ba+F_ba)/(lambda_a-lambda_b)"
        ),
        "exactSample": {
            "Q": matrix_payload(Q_sample),
            "Sigma": matrix_payload(Sigma_sample),
            "F": matrix_payload(F_sample),
            "Qdot": matrix_payload(Qdot_sample),
            "spectrum": ["7", "3", "1"],
            "eigenvalueRates": ["33", "-4", "3"],
            "eigenvectorRateColumns": matrix_payload(eigenvector_rate_columns),
            "projectorRates": [matrix_payload(rate) for rate in projector_rates_sample],
            "projectorRateSum": matrix_payload(
                sum(projector_rates_sample, sp.zeros(3))
            ),
            "trace": scalar_payload(trace_sample),
            "traceRate": scalar_payload(trace_rate_sample),
            "planeRatio": scalar_payload(plane_ratio_sample),
            "planeRatioRate": scalar_payload(plane_ratio_rate_sample),
            "lineRatio": scalar_payload(line_ratio_sample),
            "lineRatioRate": scalar_payload(line_ratio_rate_sample),
            "nearLinePrincipalGap": "4",
            "nearPlaneNormalGap": "2",
        },
        "rankBoundary": {
            "interiorFamily": "diag(7,3,s**2)",
            "interiorZeroEigenvalueRate": "0",
            "endpointFamily": "diag(7,3,s), s>=0",
            "endpointRightEigenvalueRate": "1",
        },
        "collisionBoundary": (
            "individual projector formulas require simple eigenvalues; "
            "separated cluster projectors are an analytical statement"
        ),
    },
    "bestSubspaceVariationalLedger": {
        "exactFiniteFrame": {
            "rotation": matrix_payload(rotation),
            "covariance": matrix_payload(Q_rotated),
            "eigenvalues": ["7", "3", "1"],
            "bestPlane": {
                "normal": [scalar_payload(value) for value in best_plane_normal],
                "residual": "1",
                "sos": "6*(R.T*n)_1**2+2*(R.T*n)_2**2",
            },
            "bestLine": {
                "axis": [scalar_payload(value) for value in best_line_axis],
                "residual": "4",
                "sos": "4*(R.T*ell)_2**2+6*(R.T*ell)_3**2",
            },
        },
        "analyticBoundary": (
            "the arbitrary-measure best-plane and best-line theorem is "
            "proved by Rayleigh--Ritz in the report"
        ),
    },
    "dynamicFilterObstruction": {
        "solution": (
            "u=a_N*exp(-nu*t)*sin(y)*e1+N**(-1/2)*"
            "exp(-nu*N**2*t)*sin(N*y)*e3"
        ),
        "vorticity": (
            "omega=sqrt(N)*exp(-nu*N**2*t)*cos(N*y)*e1-"
            "a_N*exp(-nu*t)*cos(y)*e3"
        ),
        "pdeChecks": {
            "divergenceFree": True,
            "nonlinearityZero": True,
            "heatEquation": True,
            "curl": True,
        },
        "filter": "T=(I-Delta)**(-1)",
        "filterMultiplier": "1/(1+|k|**2)",
        "frequencySubsequence": "any integer N>=2",
        "lowResponse": scalar_payload(A_low),
        "highResponse": scalar_payload(A_high),
        "amplitudeCalibrationKappa": scalar_payload(kappa),
        "lowModeAmplitudeSquared": scalar_payload(a_squared),
        "principalEigenvalue": scalar_payload(q_principal),
        "bestLineResidual": scalar_payload(best_line_residual),
        "residualL2TimeSquared": scalar_payload(residual_l2_time_squared),
        "residualL2TimeNorm": "1/(4*sqrt(nu)*(N**2 + 1)**2)",
        "unfilteredTransverseL4L2FourthPower": scalar_payload(
            transverse_l4_l2_fourth_power
        ),
        "unfilteredTransverseL4L2Norm": "1/(2*nu**(1/4))",
        "criticalScaling": "2/4+3/2=2",
        "finiteHorizon": {
            "factor": "theta_NT=1-exp(-4*nu*N**2*T)",
            "residualL2TimeNorm": (
                "A(N*e2)*sqrt(theta_NT)/(4*sqrt(nu))"
            ),
            "unfilteredTransverseL4L2NormSquared": (
                "sqrt(theta_NT)/(4*sqrt(nu))"
            ),
            "exactInstabilityRatio": "1/A(N*e2)",
        },
        "normalizedLineResidualAtZero": scalar_payload(line_ratio_at_zero),
        "normalizedLineResidualUpperBound": "1/3",
        "residualLimit": "0",
        "finiteCalibration": {
            "N": "8",
            "nu": "3/2",
            "lowModeAmplitudeSquared": scalar_payload(calibrated_a_squared),
            "residualL2TimeSquared": scalar_payload(
                calibrated_residual_norm_squared
            ),
            "unfilteredTransverseL4L2FourthPower": scalar_payload(
                calibrated_transverse_fourth
            ),
            "directFourierCovarianceAtT0": matrix_payload(
                fourier_covariance_at_zero
            ),
        },
        "compactBandDyadicApproximants": {
            "hiddenFrequencies": [str(value) for value in hidden_frequencies],
            "modeCount": len(hidden_frequencies),
            "nu": scalar_payload(nu_calibration),
            "fullL4L2FourthPower": scalar_payload(full_dyadic_fourth_power),
            "diagonalLowerBound": scalar_payload(diagonal_dyadic_lower_bound),
            "infiniteLimit": (
                "the diagonal lower bound is M/(16*nu), hence diverges as "
                "M tends to infinity; the report supplies the Tonelli proof"
            ),
        },
        "claimBoundary": (
            "finite smooth modes disprove uniform quantitative reconstruction; "
            "the compact-band infinite energy-class example supplies only an "
            "initial-endpoint qualitative obstruction"
        ),
    },
    "spectralGapCertificates": {
        "thresholds": {"delta": "1/20", "eta": "2/5"},
        "partition": (
            "coercive if lambda3/E>=delta; otherwise near-line if "
            "(lambda2+lambda3)/E<=eta; otherwise near-plane"
        ),
        "nearLineIdentity": (
            "(lambda1-lambda2)-(1-2*eta)*E="
            "2*(eta*E-lambda2-lambda3)+lambda3"
        ),
        "nearPlaneIdentity": (
            "(lambda2-lambda3)-(eta-2*delta)*E="
            "(lambda2+lambda3-eta*E)+2*(delta*E-lambda3)"
        ),
        "samples": {
            "coercive": [scalar_payload(value) for value in coercive_spectrum],
            "nearPlane": [scalar_payload(value) for value in near_plane_spectrum],
            "nearLine": [scalar_payload(value) for value in near_line_spectrum],
        },
    },
    "linearReconstructionGate": {
        "l2Condition": "A(k)>=a0 on every reconstructed frequency",
        "hMinusHalfCondition": "A(k)>=a0/|k| on every nonzero frequency",
        "finiteModeSample": {
            "frequencies": [scalar_payload(value) for value in frequencies],
            "coefficients": [scalar_payload(value) for value in coefficients],
            "responses": [scalar_payload(value) for value in responses],
            "l2Squared": scalar_payload(l2_squared),
            "observedEnergy": scalar_payload(observed_energy),
            "l2LowerFrameConstant": scalar_payload(l2_lower_frame_constant),
            "l2Slack": scalar_payload(l2_slack),
            "hMinusHalfSquared": scalar_payload(h_minus_half_squared),
            "hMinusHalfLowerFrameConstant": scalar_payload(
                h_minus_half_lower_frame_constant
            ),
            "hMinusHalfSlack": scalar_payload(h_minus_half_slack),
        },
        "timeBridge": (
            "if R>=a0*X pointwise and R is in L2_t, then integral X**2 "
            "is at most a0**(-2)*integral R**2"
        ),
        "blindModeSample": {
            "response": scalar_payload(blind_response),
            "coefficient": scalar_payload(blind_coefficient),
            "observedEnergy": "0",
            "unfilteredEnergy": "49",
        },
        "variableDirectionBoundary": (
            "space-dependent target projections require commutator, spectral-"
            "gap, covariance-gradient, and orientation estimates"
        ),
    },
    "claimBoundary": (
        "exact no-go and requirements theorem; not a new regularity criterion, "
        "not a singular solution, and not a solution of the Millennium problem"
    ),
    "routeDecision": (
        "close near-plane as algebraically too weak; retain near-line only "
        "behind an all-frequency absolute-residual direction-regularity and "
        "commutator gate"
    ),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
