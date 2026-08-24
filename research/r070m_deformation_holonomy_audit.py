#!/usr/bin/env python3
"""Exact symbolic audit for the R0.70M deformation-holonomy gate.

The producer verifies four distinct facts:

1. a zero-signed-integral loop of symmetric trace-free strains can have a
   hyperbolic, non-normal time-ordered exponential;
2. the Euclidean normalized pullback residual pays a sharp kappa(G)^2 loss;
3. an affine-relative SPD shape speed is congruence invariant; and
4. the affine construction is singular on rank-deficient covariances, while
   isotropic regularization reintroduces an order-one strain term.

All certificate quantities use exact SymPy arithmetic.
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


def normalized_deviatoric_energy(matrix: sp.Matrix) -> sp.Expr:
    dimension = matrix.rows
    energy = sp.trace(matrix)
    normalized = matrix / energy
    deviator = normalized - sp.eye(dimension) / dimension
    return sp.simplify(sp.trace(deviator * deviator))


# ---------------------------------------------------------------------------
# 1. Exact zero-integral noncommutative strain loop.
# ---------------------------------------------------------------------------

log_three = sp.log(3)
A2 = log_three * sp.diag(1, -1)
C2 = log_three * sp.Matrix([[0, 1], [1, 0]])

exp_A = sp.diag(3, sp.Rational(1, 3))
exp_C = sp.Matrix(
    [[sp.Rational(5, 3), sp.Rational(4, 3)],
     [sp.Rational(4, 3), sp.Rational(5, 3)]]
)

require(matrix_equal(A2.T, A2), "A symmetric")
require(matrix_equal(C2.T, C2), "C symmetric")
require(sp.trace(A2) == 0 and sp.trace(C2) == 0, "A and C trace free")
require(not matrix_is_zero(A2 * C2 - C2 * A2), "A and C do not commute")
require(matrix_equal(A2.exp(), exp_A), "exp(A)")
require(matrix_equal(C2.exp(), exp_C), "exp(C)")
require(matrix_is_zero(A2 + C2 - A2 - C2), "zero signed integral")

G2 = sp.simplify(exp_C.inv() * exp_A.inv() * exp_C * exp_A)
G2_expected = sp.Matrix(
    [
        [sp.Rational(-119, 9), sp.Rational(-160, 81)],
        [sp.Rational(160, 9), sp.Rational(209, 81)],
    ]
)
require(matrix_equal(G2, G2_expected), "exact monodromy")
require(sp.det(G2) == 1, "monodromy determinant")
require(sp.trace(G2) == sp.Rational(-862, 81), "monodromy trace")
require(bool(sp.trace(G2) < -2), "monodromy is hyperbolic")

eigenvalue_minus = (-sp.Integer(431) - 160 * sp.sqrt(7)) / 81
eigenvalue_plus = (-sp.Integer(431) + 160 * sp.sqrt(7)) / 81
for eigenvalue in (eigenvalue_minus, eigenvalue_plus):
    characteristic = sp.det(G2 - eigenvalue * sp.eye(2))
    require(sp.simplify(characteristic) == 0, "exact monodromy eigenvalue")

non_normality = sp.simplify(G2.T * G2 - G2 * G2.T)
non_normality_expected = (
    sp.Rational(2048000, 6561) * sp.Matrix([[1, 1], [1, -1]])
)
require(matrix_equal(non_normality, non_normality_expected), "non-normality")

Q2 = sp.simplify(G2 * G2.T)
Q2_expected = sp.Rational(1, 6561) * sp.Matrix(
    [[1172641, -1575680], [-1575680, 2117281]]
)
require(matrix_equal(Q2, Q2_expected), "physical covariance after one loop")
require(sp.det(Q2) == 1, "physical covariance determinant")
require(sp.trace(Q2) == sp.Rational(3289922, 6561), "physical trace")

pulled_Q2 = sp.simplify(G2.inv() * Q2 * G2.inv().T)
require(matrix_equal(pulled_Q2, sp.eye(2)), "zero-residual pullback is constant")

kappa_G2 = (
    sp.Integer(1644961) + 1280 * sp.sqrt(1651522)
) / 6561
gram_trace = sp.trace(G2.T * G2)
require(
    sp.simplify(kappa_G2 + 1 / kappa_G2 - gram_trace) == 0,
    "exact two-norm condition number",
)
require(bool(kappa_G2 > 1), "condition number branch")

G3 = sp.diag(G2, sp.Integer(1))
Q3 = sp.simplify(G3 * G3.T)
B3_energy = normalized_deviatoric_energy(Q3)
B3_expected = sp.Rational(6553600, 9889449)
B3_gap = sp.simplify(sp.Rational(2, 3) - B3_energy)
require(B3_energy == B3_expected, "three-dimensional anisotropy")
require(B3_gap == sp.Rational(13122, 3296483), "rank-one gap")

loop_records: list[dict[str, str]] = []
for loop_count in range(0, 6):
    monodromy = G3**loop_count
    covariance = sp.simplify(monodromy * monodromy.T)
    loop_records.append(
        {
            "loops": str(loop_count),
            "traceQ": scalar_payload(sp.trace(covariance)),
            "trB2": scalar_payload(normalized_deviatoric_energy(covariance)),
        }
    )


# ---------------------------------------------------------------------------
# 2. Sharp kappa(G)^2 amplification in the Euclidean normalized pullback.
# ---------------------------------------------------------------------------

k = sp.symbols("k", positive=True)
epsilon = sp.symbols("epsilon", positive=True)
Gk = sp.diag(k, 1 / k, 1)
Qepsilon = sp.diag(1, epsilon, epsilon)
Fweak = sp.diag(0, 1, 0)

hat_Qepsilon = sp.simplify(Gk.inv() * Qepsilon * Gk.inv().T)
hat_Fweak = sp.simplify(Gk.inv() * Fweak * Gk.inv().T)
physical_ratio = sp.simplify(1 / sp.trace(Qepsilon))
pulled_ratio = sp.simplify(k**2 / sp.trace(hat_Qepsilon))
amplification = sp.factor(pulled_ratio / physical_ratio)
amplification_expected = sp.factor(
    k**4 * (1 + 2 * epsilon) /
    (1 + epsilon * (k**4 + k**2))
)
require(
    sp.simplify(amplification - amplification_expected) == 0,
    "exact Euclidean amplification",
)
require(
    sp.limit(amplification, epsilon, 0, dir="+") == k**4,
    "sharp kappa squared limit",
)

sharp_gap = sp.factor(k**4 - amplification)
sharp_gap_expected = sp.factor(
    k**4 * epsilon * (k**4 + k**2 - 2)
    / (1 + epsilon * (k**4 + k**2))
)
require(sp.simplify(sharp_gap - sharp_gap_expected) == 0, "sharp upper gap")

# The quotient used in the BV theorem minimizes over scalar amplitude changes.
# For diagonal matrices this least-squares minimization is explicit.
lambda_physical = sp.simplify(
    sp.trace(Fweak * Qepsilon) / sp.trace(Qepsilon * Qepsilon)
)
lambda_pulled = sp.simplify(
    sp.trace(hat_Fweak * hat_Qepsilon)
    / sp.trace(hat_Qepsilon * hat_Qepsilon)
)
rho0_squared = sp.simplify(
    sp.trace((Fweak - lambda_physical * Qepsilon) ** 2)
    / sp.trace(Qepsilon) ** 2
)
rhoG_squared = sp.simplify(
    sp.trace((hat_Fweak - lambda_pulled * hat_Qepsilon) ** 2)
    / sp.trace(hat_Qepsilon) ** 2
)
optimized_amplification_squared = sp.factor(rhoG_squared / rho0_squared)
require(
    sp.limit(optimized_amplification_squared, epsilon, 0, dir="+")
    == k**8,
    "optimized quotient has sharp kappa-squared amplification",
)

hat_energy = sp.trace(hat_Qepsilon)
hat_R = sp.simplify(hat_Qepsilon / hat_energy)
hat_R_dot = sp.simplify(
    hat_Fweak / hat_energy
    - hat_R * sp.trace(hat_Fweak) / hat_energy
)
hat_R_dot_limit = hat_R_dot.applyfunc(
    lambda entry: sp.simplify(sp.limit(entry, epsilon, 0, dir="+"))
)
hat_R_dot_limit_expected = k**4 * sp.diag(-1, 1, 0)
require(
    matrix_equal(hat_R_dot_limit, hat_R_dot_limit_expected),
    "normalized derivative sharp limit",
)
require(
    sp.simplify(sp.trace(hat_R_dot_limit**2) - 2 * k**8) == 0,
    "normalized derivative Frobenius amplification",
)


# ---------------------------------------------------------------------------
# 3. Congruence-invariant affine-relative shape speed for Q positive definite.
# ---------------------------------------------------------------------------

G_affine = sp.Matrix([[1, 1, 0], [0, 1, 0], [0, 0, 1]])
Q_affine = sp.diag(2, 3, 5)
F_affine = sp.Matrix([[1, 1, 0], [1, -2, 1], [0, 1, 3]])
hat_Q_affine = sp.simplify(G_affine.inv() * Q_affine * G_affine.inv().T)
hat_F_affine = sp.simplify(G_affine.inv() * F_affine * G_affine.inv().T)

relative_trace = sp.simplify(sp.trace(Q_affine.inv() * F_affine))
hat_relative_trace = sp.simplify(
    sp.trace(hat_Q_affine.inv() * hat_F_affine)
)
relative_square_trace = sp.simplify(
    sp.trace((Q_affine.inv() * F_affine) ** 2)
)
hat_relative_square_trace = sp.simplify(
    sp.trace((hat_Q_affine.inv() * hat_F_affine) ** 2)
)
affine_shape_speed_squared = sp.simplify(
    relative_square_trace - relative_trace**2 / 3
)
hat_affine_shape_speed_squared = sp.simplify(
    hat_relative_square_trace - hat_relative_trace**2 / 3
)

require(sp.det(G_affine) == 1, "affine test congruence determinant")
require(sp.det(hat_Q_affine) == sp.det(Q_affine), "determinant congruence")
require(relative_trace == hat_relative_trace, "relative trace invariant")
require(
    relative_square_trace == hat_relative_square_trace,
    "relative quadratic trace invariant",
)
require(
    affine_shape_speed_squared == hat_affine_shape_speed_squared,
    "affine shape speed invariant",
)
require(bool(affine_shape_speed_squared > 0), "nontrivial affine shape speed")


# ---------------------------------------------------------------------------
# 4. Rank defect and the non-uniform isotropic regularization boundary.
# ---------------------------------------------------------------------------

Q_rank_one = sp.diag(0, 0, 1)
Sigma_null_plane = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]])
require(
    matrix_is_zero(Sigma_null_plane * Q_rank_one + Q_rank_one * Sigma_null_plane),
    "rank-one covariance is unchanged by null-plane strain",
)
require(sp.det(Q_rank_one) == 0 and Q_rank_one.rank() == 1, "rank defect")

Q_regularized = Q_rank_one + epsilon * sp.eye(3)
F_regularized = -2 * epsilon * Sigma_null_plane
regularized_relative_trace = sp.simplify(
    sp.trace(Q_regularized.inv() * F_regularized)
)
regularized_relative_square = sp.simplify(
    sp.trace((Q_regularized.inv() * F_regularized) ** 2)
)
require(regularized_relative_trace == 0, "regularized relative trace")
require(
    regularized_relative_square == 8,
    "regularized strain leakage is independent of epsilon",
)


check_details = {
    "zeroIntegralHolonomy": {
        "symmetricTraceFreeGenerators": True,
        "noncommutingGenerators": True,
        "zeroSignedIntegral": True,
        "exactHyperbolicMonodromy": True,
        "nonNormalMonodromy": True,
        "zeroResidualPullback": True,
        "nearRankOnePhysicalCovariance": True,
    },
    "sharpEuclideanAmplification": {
        "exactAmplificationFamily": True,
        "kappaSquaredLimit": True,
        "normalizedDerivativeLimit": True,
        "sharpUpperGap": True,
        "optimizedShapeQuotientSharp": True,
    },
    "affineRelativeGeometry": {
        "determinantPreservedBySL3Congruence": True,
        "relativeTraceInvariant": True,
        "relativeQuadraticTraceInvariant": True,
        "deviatoricShapeSpeedInvariant": True,
    },
    "rankDefectBoundary": {
        "rankOneCovariance": True,
        "nullPlaneStrainLeavesRawCovarianceFixed": True,
        "isotropicRegularizationReintroducesStrain": True,
        "regularizationLeakageDoesNotVanish": True,
    },
}

for group_name, group in check_details.items():
    for check_name, value in group.items():
        require(bool(value), f"{group_name}.{check_name}")


payload = {
    "release": "R0.70M",
    "status": "exact-deformation-holonomy-and-affine-boundary-audit",
    "arithmetic": "exact SymPy matrix, algebraic-number, rational, and limit arithmetic",
    "checks": {
        name: all(values.values()) for name, values in check_details.items()
    },
    "checkDetails": check_details,
    "pullbackLedger": {
        "equation": "Qdot=Sigma*Q+Q*Sigma+F",
        "deformation": "Gdot=Sigma*G; det(G)=1",
        "pullback": "Qhat=G**(-1)*Q*G**(-T)",
        "identity": "QhatDot=G**(-1)*F*G**(-T)",
        "integrated": "Q=G*(Q0+integral(G**(-1)*F*G**(-T)))*G**T",
    },
    "zeroIntegralLoop": {
        "generators": {
            "A": "log(3)*diag(1,-1)",
            "C": "log(3)*[[0,1],[1,0]]",
            "order": "A,C,-A,-C",
        },
        "signedIntegral": "zero",
        "residual": "zero",
        "expA": matrix_payload(exp_A),
        "expC": matrix_payload(exp_C),
        "monodromy": matrix_payload(G2),
        "detMonodromy": scalar_payload(sp.det(G2)),
        "traceMonodromy": scalar_payload(sp.trace(G2)),
        "eigenvalues": [scalar_payload(eigenvalue_minus), scalar_payload(eigenvalue_plus)],
        "nonNormality": matrix_payload(non_normality),
        "physicalCovariance2D": matrix_payload(Q2),
        "tracePhysicalCovariance2D": scalar_payload(sp.trace(Q2)),
        "kappaG2": scalar_payload(kappa_G2),
        "kappaG2Approx": f"{float(sp.N(kappa_G2, 18)):.15g}",
        "physicalAnisotropy3D": scalar_payload(B3_energy),
        "rankOneGap3D": scalar_payload(B3_gap),
        "loopRecords": loop_records,
        "smoothPulseBoundary": "four disjoint smooth unit-mass scalar pulses preserve the same ordered exponentials exactly",
    },
    "sharpEuclideanAmplification": {
        "family": "G=diag(k,k**(-1),1), Q=diag(1,epsilon,epsilon), F=e2 tensor e2",
        "kappaG": "k**2",
        "amplification": scalar_payload(amplification),
        "sharpLimit": "lim_epsilon_to_0 amplification=k**4=kappa(G)**2",
        "optimizedShapeQuotientSquared": scalar_payload(
            optimized_amplification_squared
        ),
        "optimizedShapeQuotientLimit": "lim_epsilon_to_0 rhoG/rho0=k**4=kappa(G)**2",
        "normalizedDerivativeLimit": matrix_payload(hat_R_dot_limit),
        "spectralSpreadBound": "kappa(G(t))<=exp(integral(lambda_max(Sigma)-lambda_min(Sigma)))",
        "normalizedSensitivityBound": "Euclidean pulled residual sensitivity can require exp(2*integral spectral spread)",
    },
    "affineRelativeGeometry": {
        "requires": "Q positive definite",
        "determinantRate": "d/dt log(det(Q))=trace(Q**(-1)*F) because trace(Sigma)=0",
        "shape": "C=det(Q)**(-1/3)*Q",
        "shapeSpeedSquared": "trace((Q**(-1)*F)**2)-trace(Q**(-1)*F)**2/3",
        "congruenceInvariant": True,
        "distanceBound": "d_AI(Chat(t0),Chat(t))<=integral affine shape speed",
        "testRelativeTrace": scalar_payload(relative_trace),
        "testShapeSpeedSquared": scalar_payload(affine_shape_speed_squared),
    },
    "rankDefect": {
        "smoothNSEWitness": "u=A*exp(-nu*N**2*t)*sin(N*y)*e1 has vorticity parallel to e3 and every weighted covariance has rank at most one",
        "inverseDiagnostic": "undefined on the periodic shear whenever the covariance is nonzero",
        "regularization": "Q_epsilon=Q+epsilon*trace(Q)*I",
        "effectiveResidual": "F_epsilon=F+epsilon*E_dot*I-2*epsilon*E*Sigma",
        "nullPlaneExampleRelativeSpeedSquared": scalar_payload(regularized_relative_square),
        "epsilonLimit": "the added strain contribution remains order one as epsilon tends to zero",
    },
    "claimBoundary": {
        "proved": "exact matrix pullback, sharp kappa-squared Euclidean loss, zero-integral noncommutative holonomy, affine-relative SPD identity, and non-uniform rank regularization",
        "exactNSEInput": "the rank-defect boundary occurs on a smooth unforced periodic shear solution",
        "notClaimed": "the four-pulse holonomy is not yet embedded in one unforced finite-energy periodic NSE trajectory; no critical residual estimate, blow-up theorem, global regularity theorem, or Millennium solution is claimed",
        "routeDecision": "a universal pullback estimate needs either direct spectral-spread control or a scale-frame coercivity lower bound that prevents covariance rank collapse",
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
