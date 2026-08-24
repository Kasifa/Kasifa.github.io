#!/usr/bin/env python3
"""Exact symbolic audit for the R0.70N multi-scale frame gate.

The producer verifies four separate facts:

1. scalar/componentwise filtered covariance ledgers aggregate exactly, with
   explicit source-mismatch and time-dependent-weight terms;
2. an exact unforced periodic Navier--Stokes shear makes every nonzero
   multi-scale covariance rank one;
3. an exact unforced periodic helical Beltrami wave makes every such
   covariance rank at most two, despite spatially rotating vorticity; and
4. scale normalization and positive time aggregation do not repair a common
   null direction, so no universal positive frame constant can follow from
   trace/enstrophy alone.

All finite certificate quantities use exact SymPy arithmetic.  The producer
does not claim to computer-prove the analytic common-subspace lemma for an
arbitrary filter family; that proof is written in the canonical report.
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
        [str(sp.simplify(matrix[row, column])) for column in range(matrix.cols)]
        for row in range(matrix.rows)
    ]


def scalar_payload(value: sp.Expr) -> str:
    return str(sp.simplify(value))


def generic_symmetric(prefix: str) -> sp.Matrix:
    a11, a12, a13, a22, a23, a33 = sp.symbols(
        f"{prefix}11 {prefix}12 {prefix}13 "
        f"{prefix}22 {prefix}23 {prefix}33"
    )
    return sp.Matrix(
        [[a11, a12, a13], [a12, a22, a23], [a13, a23, a33]]
    )


# ---------------------------------------------------------------------------
# 1. Exact aggregate ledger, including mismatch and moving weights.
# ---------------------------------------------------------------------------

Q1 = generic_symmetric("q")
Q2 = generic_symmetric("r")
F1 = generic_symmetric("f")
F2 = generic_symmetric("g")
Sigma_star = generic_symmetric("s")
Delta1 = generic_symmetric("d")
Delta2 = generic_symmetric("e")
w1, w2, dw1, dw2 = sp.symbols("w1 w2 dw1 dw2")

Sigma1 = Sigma_star + Delta1
Sigma2 = Sigma_star + Delta2
aggregate_Q = w1 * Q1 + w2 * Q2
native_derivative = (
    dw1 * Q1
    + dw2 * Q2
    + w1 * (Sigma1 * Q1 + Q1 * Sigma1 + F1)
    + w2 * (Sigma2 * Q2 + Q2 * Sigma2 + F2)
)
aggregate_residual = (
    w1 * (F1 + Delta1 * Q1 + Q1 * Delta1)
    + w2 * (F2 + Delta2 * Q2 + Q2 * Delta2)
    + dw1 * Q1
    + dw2 * Q2
)
common_source_derivative = (
    Sigma_star * aggregate_Q
    + aggregate_Q * Sigma_star
    + aggregate_residual
)
require(
    matrix_equal(native_derivative, common_source_derivative),
    "common-source aggregate ledger",
)

# A positive time window has the same source-mismatch structure.  The two
# matrices here represent exact time samples; the algebra is independent of
# the quadrature interpretation.
a1, a2 = sp.symbols("a1 a2")
time_aggregate_Q = a1 * Q1 + a2 * Q2
time_native_derivative = (
    a1 * (Sigma1 * Q1 + Q1 * Sigma1 + F1)
    + a2 * (Sigma2 * Q2 + Q2 * Sigma2 + F2)
)
time_residual = (
    a1 * (F1 + Delta1 * Q1 + Q1 * Delta1)
    + a2 * (F2 + Delta2 * Q2 + Q2 * Delta2)
)
time_common_derivative = (
    Sigma_star * time_aggregate_Q
    + time_aggregate_Q * Sigma_star
    + time_residual
)
require(
    matrix_equal(time_native_derivative, time_common_derivative),
    "time-window source mismatch ledger",
)

# The common pullback cancels only the chosen common source.
M = sp.Matrix(3, 3, lambda i, j: sp.symbols(f"m{i}{j}"))
Q = generic_symmetric("x")
F = generic_symmetric("h")
pullback_derivative = (
    -M * Sigma_star * Q * M.T
    + M * (Sigma_star * Q + Q * Sigma_star + F) * M.T
    - M * Q * Sigma_star * M.T
)
require(
    matrix_equal(pullback_derivative, M * F * M.T),
    "common pullback identity",
)


# ---------------------------------------------------------------------------
# 2. Exact unforced periodic shear and its rank-one multi-scale covariance.
# ---------------------------------------------------------------------------

x, y, z, t = sp.symbols("x y z t", real=True)
A, N, nu = sp.symbols("A N nu", positive=True, real=True)
coordinates = (x, y, z)
shear_factor = A * sp.exp(-nu * N**2 * t)
u_shear = sp.Matrix([shear_factor * sp.sin(N * y), 0, 0])


def divergence(vector: sp.Matrix) -> sp.Expr:
    return sp.simplify(sum(sp.diff(vector[i], coordinates[i]) for i in range(3)))


def laplacian(vector: sp.Matrix) -> sp.Matrix:
    return vector.applyfunc(
        lambda component: sp.simplify(
            sum(sp.diff(component, coordinate, 2) for coordinate in coordinates)
        )
    )


def advective_derivative(vector: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.simplify(
                sum(
                    vector[a] * sp.diff(vector[i], coordinates[a])
                    for a in range(3)
                )
            )
            for i in range(3)
        ]
    )


def curl(vector: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.diff(vector[2], y) - sp.diff(vector[1], z),
            sp.diff(vector[0], z) - sp.diff(vector[2], x),
            sp.diff(vector[1], x) - sp.diff(vector[0], y),
        ]
    ).applyfunc(sp.simplify)


require(divergence(u_shear) == 0, "shear divergence")
require(matrix_is_zero(advective_derivative(u_shear)), "shear nonlinearity")
require(
    matrix_is_zero(sp.diff(u_shear, t) - nu * laplacian(u_shear)),
    "shear heat equation",
)
omega_shear = curl(u_shear)
omega_shear_expected = sp.Matrix(
    [0, 0, -A * N * sp.exp(-nu * N**2 * t) * sp.cos(N * y)]
)
require(matrix_equal(omega_shear, omega_shear_expected), "shear vorticity")

filter_multipliers = [sp.Integer(1), sp.Rational(1, 2), sp.Rational(1, 3)]
frame_weights = [sp.Integer(1), sp.Integer(2), sp.Integer(3)]
weighted_multiplier_square = sp.simplify(
    sum(
        weight * multiplier**2
        for weight, multiplier in zip(frame_weights, filter_multipliers)
    )
)
require(weighted_multiplier_square == sp.Rational(11, 6), "frame coefficient")

P_shear = sp.diag(0, 0, 1)
Q_shear = sp.simplify(weighted_multiplier_square * P_shear / 2)
require(Q_shear == sp.Rational(11, 12) * P_shear, "shear covariance")
require(Q_shear.rank() == 1, "shear covariance rank")
require(sp.trace(Q_shear) == sp.Rational(11, 12), "shear covariance trace")


# ---------------------------------------------------------------------------
# 3. Exact helical Beltrami wave and its rank-two common-null covariance.
# ---------------------------------------------------------------------------

beltrami_factor = A * sp.exp(-nu * N**2 * t)
u_beltrami = sp.Matrix(
    [beltrami_factor * sp.cos(N * z), -beltrami_factor * sp.sin(N * z), 0]
)
require(divergence(u_beltrami) == 0, "Beltrami divergence")
require(
    matrix_is_zero(advective_derivative(u_beltrami)),
    "Beltrami nonlinearity",
)
require(
    matrix_is_zero(sp.diff(u_beltrami, t) - nu * laplacian(u_beltrami)),
    "Beltrami heat equation",
)
omega_beltrami = curl(u_beltrami)
require(
    matrix_equal(omega_beltrami, N * u_beltrami),
    "Beltrami curl eigenfield",
)

P_beltrami = sp.diag(1, 1, 0)
Q_beltrami = sp.simplify(weighted_multiplier_square * P_beltrami / 2)
require(
    Q_beltrami == sp.Rational(11, 12) * P_beltrami,
    "Beltrami covariance",
)
require(Q_beltrami.rank() == 2, "Beltrami covariance rank")
require(sp.trace(Q_beltrami) == sp.Rational(11, 6), "Beltrami trace")

# Two nonparallel real helical axes give a positive control.  This prevents
# the no-go from being misread as saying that every Beltrami covariance is
# singular.
a_mode, b_mode = sp.symbols("a_mode b_mode", positive=True, real=True)
two_axis_factor = sp.exp(-nu * t)
b_z = sp.Matrix([sp.sin(z), sp.cos(z), 0])
b_x = sp.Matrix([0, sp.sin(x), sp.cos(x)])
u_two_axis = two_axis_factor * (a_mode * b_z + b_mode * b_x)
p_two_axis = -sp.simplify((u_two_axis.T * u_two_axis)[0]) / 2
grad_p_two_axis = sp.Matrix([sp.diff(p_two_axis, coordinate) for coordinate in coordinates])
require(divergence(u_two_axis) == 0, "two-axis Beltrami divergence")
require(matrix_equal(curl(u_two_axis), u_two_axis), "two-axis Beltrami curl")
require(
    matrix_is_zero(
        sp.diff(u_two_axis, t)
        + advective_derivative(u_two_axis)
        + grad_p_two_axis
        - nu * laplacian(u_two_axis)
    ),
    "two-axis Beltrami NSE with exact pressure",
)

alpha, beta = sp.symbols("alpha beta", positive=True, real=True)
Q_two_axis = alpha * P_beltrami + beta * sp.diag(0, 1, 1)
Q_two_axis_expected = sp.diag(alpha, alpha + beta, beta)
require(matrix_equal(Q_two_axis, Q_two_axis_expected), "two-axis covariance")
require(
    sp.simplify(sp.det(Q_two_axis) - alpha * beta * (alpha + beta)) == 0,
    "two-axis determinant",
)
require(Q_two_axis.rank() == 3, "two-axis covariance positive rank")
require(sp.trace(Q_two_axis) == 2 * (alpha + beta), "two-axis trace")


# ---------------------------------------------------------------------------
# 4. Normalization, positive time aggregation, and coercivity violations.
# ---------------------------------------------------------------------------

normalized_shear_scales = [P_shear for _ in filter_multipliers]
normalized_shear_sum = sum(
    (weight * covariance for weight, covariance in zip(frame_weights, normalized_shear_scales)),
    sp.zeros(3),
)
require(normalized_shear_sum == 6 * P_shear, "normalized shear scale sum")
require(normalized_shear_sum.rank() == 1, "normalized shear rank")

normalized_beltrami_scales = [P_beltrami / 2 for _ in filter_multipliers]
normalized_beltrami_sum = sum(
    (
        weight * covariance
        for weight, covariance in zip(frame_weights, normalized_beltrami_scales)
    ),
    sp.zeros(3),
)
require(
    normalized_beltrami_sum == 3 * P_beltrami,
    "normalized Beltrami scale sum",
)
require(normalized_beltrami_sum.rank() == 2, "normalized Beltrami rank")

# Two exact positive time weights preserve the same nullspace.
time_weights = [sp.Rational(2, 5), sp.Rational(3, 5)]
time_shear = sum((weight * Q_shear for weight in time_weights), sp.zeros(3))
time_beltrami = sum(
    (weight * Q_beltrami for weight in time_weights), sp.zeros(3)
)
require(matrix_equal(time_shear, Q_shear), "positive-time shear aggregate")
require(
    matrix_equal(time_beltrami, Q_beltrami),
    "positive-time Beltrami aggregate",
)

c = sp.symbols("c", positive=True)
e1 = sp.Matrix([1, 0, 0])
e3 = sp.Matrix([0, 0, 1])
shear_violation = sp.simplify(
    (e1.T * (Q_shear - c * sp.trace(Q_shear) * sp.eye(3)) * e1)[0]
)
beltrami_violation = sp.simplify(
    (e3.T * (Q_beltrami - c * sp.trace(Q_beltrami) * sp.eye(3)) * e3)[0]
)
require(shear_violation == -sp.Rational(11, 12) * c, "shear coercivity gap")
require(beltrami_violation == -sp.Rational(11, 6) * c, "Beltrami gap")
require(bool(shear_violation < 0), "shear violates every positive c")
require(bool(beltrami_violation < 0), "Beltrami violates every positive c")

# Whole-space finite-energy quantitative calibration.  Every finite L gives
# a genuinely three-dimensional Schwartz datum and a positive-definite
# identity-filter vorticity covariance, but its optimal frame constant tends
# to zero as L grows.
L = sp.symbols("L", positive=True, real=True)
psi_L = sp.exp(-(x**2 + y**2) / 2 - z**2 / (2 * L**2))
u_L = sp.Matrix([-y * psi_L, x * psi_L, 0])
omega_L = curl(u_L)
omega_L_expected = sp.Matrix(
    [x * z * psi_L / L**2, y * z * psi_L / L**2, (2 - x**2 - y**2) * psi_L]
)
require(divergence(u_L) == 0, "whole-space datum divergence")
require(matrix_equal(omega_L, omega_L_expected), "whole-space datum curl")

Q_L = sp.zeros(3)
for row in range(3):
    for column in range(3):
        Q_L[row, column] = sp.simplify(
            sp.integrate(
                omega_L[row] * omega_L[column],
                (x, -sp.oo, sp.oo),
                (y, -sp.oo, sp.oo),
                (z, -sp.oo, sp.oo),
            )
        )
Q_L_expected = sp.pi ** sp.Rational(3, 2) * sp.diag(
    1 / (4 * L), 1 / (4 * L), 2 * L
)
require(matrix_equal(Q_L, Q_L_expected), "whole-space exact covariance")
whole_space_frame_ratio = sp.simplify(
    Q_L[0, 0] / sp.trace(Q_L)
)
require(
    sp.simplify(whole_space_frame_ratio - 1 / (8 * L**2 + 2)) == 0,
    "whole-space frame ratio",
)
require(
    sp.limit(whole_space_frame_ratio, L, sp.oo) == 0,
    "whole-space frame ratio degenerates",
)


check_details = {
    "aggregateLedger": {
        "commonReferenceSource": True,
        "nativeSourceMismatchRetained": True,
        "timeDependentWeightTermRetained": True,
        "positiveTimeWindowMismatchRetained": True,
        "commonPullbackCancelsOnlyCommonSource": True,
    },
    "exactPeriodicShear": {
        "divergenceFree": True,
        "nonlinearityZero": True,
        "solvesHeatEquation": True,
        "vorticityHasFixedDirection": True,
        "threeScaleCovarianceRankOne": True,
    },
    "exactBeltramiWave": {
        "divergenceFree": True,
        "nonlinearityZero": True,
        "solvesHeatEquation": True,
        "curlEigenfield": True,
        "threeScaleCovarianceHasCommonNullDirection": True,
        "twoNonparallelAxesGivePositiveControl": True,
        "twoAxisPressureSignVerified": True,
    },
    "universalFrameNoGo": {
        "scaleNormalizationDoesNotRepairShear": True,
        "scaleNormalizationDoesNotRepairBeltrami": True,
        "positiveTimeAggregationDoesNotRepairCommonNullspace": True,
        "shearViolatesEveryPositiveFrameConstant": True,
        "beltramiViolatesEveryPositiveFrameConstant": True,
        "wholeSpaceSchwartzFamilyHasNoUniformConstant": True,
    },
}

for group_name, group in check_details.items():
    for check_name, value in group.items():
        require(bool(value), f"{group_name}.{check_name}")


payload = {
    "release": "R0.70N",
    "status": "exact-multiscale-frame-no-go-audit",
    "arithmetic": "exact SymPy symbolic, trigonometric, matrix, and rational arithmetic",
    "checks": {
        name: all(values.values()) for name, values in check_details.items()
    },
    "checkDetails": check_details,
    "aggregateLedger": {
        "perScale": "Qdot_j=Sigma_j*Q_j+Q_j*Sigma_j+F_j",
        "commonSource": "Sigma_j=Sigma_star+Delta_j",
        "aggregate": "Qcal=sum_j w_j*Q_j",
        "residual": "Fcal=sum_j w_j*(F_j+Delta_j*Q_j+Q_j*Delta_j)+sum_j wdot_j*Q_j",
        "pullback": "QcalHat=G_star**(-1)*Qcal*G_star**(-T)",
        "pullbackIdentity": "QcalHatDot=G_star**(-1)*Fcal*G_star**(-T)",
        "timeWindowBoundary": "past sources create the same Delta*Q+Q*Delta mismatch relative to any current common source",
    },
    "finiteFrame": {
        "filterMultipliers": [scalar_payload(value) for value in filter_multipliers],
        "weights": [scalar_payload(value) for value in frame_weights],
        "weightedMultiplierSquare": scalar_payload(weighted_multiplier_square),
        "optimalConstant": "lambda_min(Qcal)/trace(Qcal)",
        "equivalentCondition": "sum observations |n dot Omega|**2 >= c*sum observations |Omega|**2 for every unit n",
    },
    "periodicShear": {
        "solution": "u=A*exp(-nu*N**2*t)*sin(N*y)*e1",
        "vorticity": "omega=-A*N*exp(-nu*N**2*t)*cos(N*y)*e3",
        "threeScaleCovariance": matrix_payload(Q_shear),
        "rank": str(Q_shear.rank()),
        "trace": scalar_payload(sp.trace(Q_shear)),
        "nullDirection": "e1 (and every vector in span(e1,e2))",
        "coercivityQuadraticGap": scalar_payload(shear_violation),
    },
    "beltramiWave": {
        "solution": "u=A*exp(-nu*N**2*t)*(cos(N*z),-sin(N*z),0)",
        "vorticity": "omega=N*u",
        "threeScaleCovariance": matrix_payload(Q_beltrami),
        "rank": str(Q_beltrami.rank()),
        "trace": scalar_payload(sp.trace(Q_beltrami)),
        "nullDirection": "e3",
        "coercivityQuadraticGap": scalar_payload(beltrami_violation),
        "twoAxisPositiveControl": {
            "covariance": matrix_payload(Q_two_axis),
            "determinant": scalar_payload(sp.det(Q_two_axis)),
            "trace": scalar_payload(sp.trace(Q_two_axis)),
            "optimalConstant": "min(alpha,beta)/(2*(alpha+beta))",
        },
    },
    "wholeSpaceCalibration": {
        "datum": "u_L=(-y*psi_L,x*psi_L,0), psi_L=exp(-(x**2+y**2)/2-z**2/(2*L**2))",
        "vorticity": "(x*z*psi_L/L**2,y*z*psi_L/L**2,(2-x**2-y**2)*psi_L)",
        "identityFilterCovariance": matrix_payload(Q_L),
        "optimalConstantForLAtLeastOne": scalar_payload(whole_space_frame_ratio),
        "limit": "lim_L_to_infinity lambda_min(Q_L)/trace(Q_L)=0",
        "scope": "exact initial-data calibration; not a positive-time rank claim",
    },
    "commonSubspaceBoundary": {
        "analyticLemma": "if every scalar/componentwise filtered vorticity lies in a fixed proper subspace V, every nonnegative scale/time Gramian has range contained in V",
        "normalizingEachScale": "does not change the range or common nullspace",
        "addingCentersCutoffsScales": "does not repair a fixed common subspace",
        "claimScope": "finite exact examples certify the no-go; the arbitrary-family statement is proved analytically in the report",
    },
    "claimBoundary": {
        "proved": "the universal positive multi-scale covariance frame bound fails for scalar/componentwise filters, including normalized scales and positive time windows",
        "exactNSEInputs": "unforced smooth periodic shear and helical Beltrami solutions",
        "notClaimed": "conditional frame bounds are impossible; all augmented observables fail; low-rank geometry implies regularity; global smoothness; finite-time blow-up; or a Millennium solution",
        "routeDecision": "replace universal frame coercivity by a coercive-versus-common-subspace geometric dichotomy, and derive any augmented-observable PDE ledger before computation",
    },
}


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output")
arguments = parser.parse_args()
rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
if arguments.output:
    Path(arguments.output).write_text(rendered, encoding="utf-8")
else:
    print(rendered, end="")
