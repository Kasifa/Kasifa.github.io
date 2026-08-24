#!/usr/bin/env python3
"""Exact algebra audit for the R0.70G adjacent-source jet gate.

The script checks the critical transport factors, the constant-increment
recurrence and its dilation defect, finite Abel summation, two inequivalent
constant/linear harmonic jet profiles with the same positive e1 pairing, the
radial constant-core zero-strain lemma, and the source-side square-function
weights.

It does not prove a common-terminal-time Navier--Stokes packing estimate,
derive a core-moment Carleson bound, or identify a fixed-source positive-part
sum with Yu's moving-shell quantity.
"""

from __future__ import annotations

import json

import sympy as sp


x1, x2, x3 = sp.symbols("x1 x2 x3", real=True)
x = sp.Matrix([x1, x2, x3])
e1 = sp.Matrix([1, 0, 0])


def divergence(field: sp.Matrix) -> sp.Expr:
    return sp.simplify(sum(sp.diff(field[i], x[i]) for i in range(3)))


def curl(field: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.diff(field[2], x2) - sp.diff(field[1], x3),
            sp.diff(field[0], x3) - sp.diff(field[2], x1),
            sp.diff(field[1], x1) - sp.diff(field[0], x2),
        ]
    ).applyfunc(sp.simplify)


def strain(field: sp.Matrix) -> sp.Matrix:
    jacobian = field.jacobian(x)
    return ((jacobian + jacobian.T) / 2).applyfunc(sp.simplify)


def laplacian_scalar(expression: sp.Expr) -> sp.Expr:
    return sp.simplify(sum(sp.diff(expression, variable, 2) for variable in x))


def homotopy_potential(field: sp.Matrix, degree: int) -> sp.Matrix:
    return (-sp.Rational(1, degree + 2) * x.cross(field)).applyfunc(sp.expand)


def coefficient_tensor(linear_matrix_field: sp.Matrix) -> list[list[list[sp.Expr]]]:
    return [
        [
            [sp.diff(linear_matrix_field[i, j], variable) for variable in x]
            for j in range(3)
        ]
        for i in range(3)
    ]


def tensor_squared_norm(tensor: list[list[list[sp.Expr]]]) -> sp.Expr:
    return sp.simplify(
        sum(tensor[i][j][k] ** 2 for i in range(3) for j in range(3) for k in range(3))
    )


# Critical transport law for a degree-n strain jet.
n = sp.symbols("n", integer=True, nonnegative=True)
critical_power = n + 2
dyadic_transport_factor = 2 ** (-(n + 2))
transport_factors = {degree: sp.Rational(1, 2 ** (degree + 2)) for degree in range(5)}


# Constant raw increments and the cumulative critical recurrence.
lam = sp.symbols("lambda", positive=True)
layer = sp.symbols("m", integer=True, positive=True)
cumulative = sp.simplify((1 - lam**layer) / (1 - lam))
cumulative_previous = sp.simplify((1 - lam ** (layer - 1)) / (1 - lam))
covariant_increment = sp.simplify(cumulative - lam * cumulative_previous)
ordinary_increment = sp.simplify(cumulative - cumulative_previous)

N = sp.symbols("N", integer=True, positive=True)
ordinary_l1 = sp.simplify((1 - lam**N) / (1 - lam))
ordinary_l2_mass = sp.simplify((1 - lam ** (2 * N)) / (1 - lam**2))


# Complete-grid spike variation. Each isolated spike is bracketed by zeros,
# hence contributes one entry and one exit. Check finite chains directly.
spike_checks: dict[str, bool] = {}
for count in range(1, 9):
    support = {3 * index + 1 for index in range(count)}
    spike = [sp.Integer(0)] + [sp.Integer(index in support) for index in range(1, 3 * count)] + [sp.Integer(0)]
    differences = [spike[index] - spike[index - 1] for index in range(1, len(spike))]
    spike_checks[f"count{count}"] = (
        sum(abs(value) for value in differences) == 2 * count
        and sum(value**2 for value in differences) == 2 * count
    )


# Finite Abel identity with scalar placeholders. Tensor contractions obey the
# same bilinear algebra component by component.
abel_checks: dict[str, bool] = {}
for length in range(1, 9):
    p_values = [sp.Rational((index + 2) * (index + 5), index + 3) for index in range(length + 1)]
    m_values = [sp.Rational((index + 1) * (2 * index + 3), index + 4) for index in range(length)]
    direct = sum((p_values[j + 1] - p_values[j]) * m_values[j] for j in range(length))
    abel = (
        p_values[-1] * m_values[-1]
        - p_values[0] * m_values[0]
        + sum(p_values[j + 1] * (m_values[j] - m_values[j + 1]) for j in range(length - 1))
    )
    abel_checks[f"length{length}"] = sp.simplify(direct - abel) == 0


# Two constant-strain profiles: same e1 pairing, different spectra.
A0 = sp.diag(1, -sp.Rational(1, 2), -sp.Rational(1, 2))
A1 = sp.diag(1, -sp.Rational(1, 4), -sp.Rational(3, 4))
P0 = A0 * x
P1 = A1 * x
A0_potential = homotopy_potential(P0, 1)
A1_potential = homotopy_potential(P1, 1)
constant_difference_squared = sp.simplify(sum(value**2 for value in (A1 - A0)))


# Two harmonic cubic profiles: same positive e1-lobe contraction, but
# different coefficient-tensor norms, hence not related by an orthogonal frame.
phi0 = x1**3 - 3 * x1 * x2**2
phi1 = x1**3 - sp.Rational(3, 2) * x1 * (x2**2 + x3**2)
V0 = sp.Matrix([sp.diff(phi0, variable) for variable in x])
V1 = sp.Matrix([sp.diff(phi1, variable) for variable in x])
L0 = sp.hessian(phi0, x)
L1 = sp.hessian(phi1, x)
B0 = coefficient_tensor(L0)
B1 = coefficient_tensor(L1)
B_difference = [
    [
        [sp.simplify(B1[i][j][k] - B0[i][j][k]) for k in range(3)]
        for j in range(3)
    ]
    for i in range(3)
]
linear_difference_squared = tensor_squared_norm(B_difference)
linear_norm0_squared = tensor_squared_norm(B0)
linear_norm1_squared = tensor_squared_norm(B1)
c = sp.symbols("c", positive=True)


# The paired scalar is constant for both alternating profile families, while
# the positive baseline work retains the increasing b_m^2 factor.
paired_constant_difference = sp.simplify((e1.T * (A1 - A0) * e1)[0])
paired_linear_difference = sp.simplify(
    (
        e1.T
        * (L1 - L0).subs({x1: c, x2: 0, x3: 0})
        * e1
    )[0]
)


# Radial constant-core lemma. If -Delta F=a0 in a ball, the regular radial
# solution has quadratic part -a0|x|^2/6. curl(F e1) is a solid rotation.
a0 = sp.symbols("a0", real=True)
radial_potential = -a0 * (x1**2 + x2**2 + x3**2) / 6
radial_velocity = sp.Matrix(
    [sp.diff(radial_potential, variable) for variable in x]
).cross(e1)


# Kernel L2 exponent: |D^n K|~r^(-3-n), so its squared annular integral
# scales as r^(-3-2n); the compensating source-side square-function weight is
# r^(3+2n)=r^(2(n+2)-1).
kernel_l2_squared_exponent = sp.simplify(-2 * (3 + n) + 3)
square_function_weight_exponent = sp.simplify(-kernel_l2_squared_exponent)
critical_weight_identity = sp.simplify(square_function_weight_exponent - (2 * critical_power - 1))


# Reuse the exact positive-work scale factors from R0.70F.
Lambda, b, eta, c_chi = sp.symbols("Lambda b eta c_chi", positive=True)
constant_work = sp.simplify(c_chi * eta**3 * b**2 / Lambda**2)
linear_work = sp.simplify(6 * c * c_chi * eta**3 * b**2 / Lambda**3)

baseline_checks: dict[str, bool] = {}
for length in range(2, 9):
    lambda_value = sp.Integer(2)
    b_values = [
        sp.simplify((1 - lambda_value ** (-4 * index)) / (1 - lambda_value**-4))
        for index in range(1, length + 1)
    ]
    variation = sum(b_values[index + 1] ** 2 - b_values[index] ** 2 for index in range(length - 1))
    baseline_checks[f"length{length}"] = sp.simplify(
        variation - (b_values[-1] ** 2 - 1)
    ) == 0


checks = {
    "constantTransportFactor": transport_factors[0] == sp.Rational(1, 4),
    "linearTransportFactor": transport_factors[1] == sp.Rational(1, 8),
    "quadraticTransportFactor": transport_factors[2] == sp.Rational(1, 16),
    "covariantIncrementStaysOne": covariant_increment == 1,
    "ordinaryIncrementIsGeometric": ordinary_increment == lam ** (layer - 1),
    "allFiniteSpikeChecks": all(spike_checks.values()),
    "allFiniteAbelChecks": all(abel_checks.values()),
    "constantProfilesTraceFree": sp.trace(A0) == 0 and sp.trace(A1) == 0,
    "constantProfilesDivergenceFree": divergence(P0) == 0 and divergence(P1) == 0,
    "constantProfilesCurlFree": curl(P0) == sp.zeros(3, 1) and curl(P1) == sp.zeros(3, 1),
    "constantHomotopyRecovery": curl(A0_potential) == P0 and curl(A1_potential) == P1,
    "constantProfilesSamePositivePairing": (e1.T * A0 * e1)[0] == 1 and (e1.T * A1 * e1)[0] == 1,
    "constantProfilesDifferent": constant_difference_squared == sp.Rational(1, 8),
    "linearCubicsHarmonic": laplacian_scalar(phi0) == 0 and laplacian_scalar(phi1) == 0,
    "linearVelocitiesDivergenceFree": divergence(V0) == 0 and divergence(V1) == 0,
    "linearVelocitiesCurlFree": curl(V0) == sp.zeros(3, 1) and curl(V1) == sp.zeros(3, 1),
    "linearProfilesSamePositivePairing": (
        sp.simplify((e1.T * L0.subs({x1: c, x2: 0, x3: 0}) * e1)[0]) == 6 * c
        and sp.simplify((e1.T * L1.subs({x1: c, x2: 0, x3: 0}) * e1)[0]) == 6 * c
    ),
    "linearProfilesDifferentNorms": linear_norm0_squared != linear_norm1_squared,
    "linearProfilesDifference": linear_difference_squared == 54,
    "pairedConstantDifferenceZero": paired_constant_difference == 0,
    "pairedLinearDifferenceZero": paired_linear_difference == 0,
    "allFiniteBaselineVariationChecks": all(baseline_checks.values()),
    "radialCorePoissonEquation": -laplacian_scalar(radial_potential) == a0,
    "radialCoreVelocityIsSolidRotation": strain(radial_velocity) == sp.zeros(3),
    "sourceSquareWeight": square_function_weight_exponent == 2 * n + 3,
    "criticalWeightIdentity": critical_weight_identity == 0,
    "constantWorkPositive": constant_work.is_positive,
    "linearWorkPositive": linear_work.is_positive,
}

if not all(checks.values()):
    failures = [name for name, passed in checks.items() if not passed]
    raise AssertionError(f"failed exact checks: {failures}")


result = {
    "status": "exact-symbolic-audit",
    "release": "R0.70G",
    "arithmetic": "exact SymPy polynomial and rational arithmetic",
    "criticalTransport": {
        "generalDegree": "h_j^(n)=c_j^(n)-2^(-(n+2))*c_(j-1)^(n)",
        "factors": {str(degree): sp.sstr(value) for degree, value in transport_factors.items()},
        "ordinaryDifferenceSplit": "h_j=(c_j-c_(j-1))+(1-lambda_n)*c_(j-1)",
    },
    "constantRawIncrementRecurrence": {
        "cumulative": sp.sstr(cumulative),
        "covariantIncrement": sp.sstr(covariant_increment),
        "ordinaryIncrement": sp.sstr(ordinary_increment),
        "rawL1ThroughN": "N",
        "rawL2MassThroughN": "N",
        "ordinaryL1ThroughN": sp.sstr(ordinary_l1),
        "ordinaryL2MassThroughN": sp.sstr(ordinary_l2_mass),
    },
    "fullGridSpikes": {
        "constantL1": "2*N*Lambda^(-2)",
        "constantSquareMass": "2*N*Lambda^(-4)",
        "linearL1": "12*N*Lambda^(-3)",
        "linearSquareMass": "72*N*Lambda^(-6)",
        "finiteChainsChecked": len(spike_checks),
    },
    "sourceSquareFunction": {
        "degreeNWeight": "r_j^(2*n+3)*|J_j^(n)|^2",
        "criticalCoordinateWeight": "r_j^(-1)*|h_j^(n)|^2",
        "bound": "sum_j weight <= C*||Omega||_2^2 for bounded-overlap annuli",
        "missingDualInput": "core-moment square summability or variation",
    },
    "alternatingProfiles": {
        "constantDifferenceSquared": sp.sstr(constant_difference_squared),
        "constantPairingOnE1": "1 for both profiles",
        "linearDifferenceSquared": sp.sstr(linear_difference_squared),
        "linearNormsSquared": [sp.sstr(linear_norm0_squared), sp.sstr(linear_norm1_squared)],
        "linearPairingAtCE1": "6*c for both profiles",
        "constantActiveSquareMass": "(N-1)*Lambda^(-4)/8",
        "linearActiveSquareMass": "54*(N-1)*Lambda^(-6)",
    },
    "radialCoreLemma": {
        "potential": sp.sstr(radial_potential),
        "velocity": [sp.sstr(value) for value in radial_velocity],
        "strain": [[sp.sstr(value) for value in row] for row in strain(radial_velocity).tolist()],
    },
    "initialFaceWork": {
        "constant": sp.sstr(constant_work),
        "linear": sp.sstr(linear_work),
        "pairedScalarDifferences": "0 for both alternating families",
        "workVariation": "C_q*(b_N^2-1)",
        "finiteVariationCasesChecked": len(baseline_checks),
    },
    "finiteAbelCasesChecked": len(abel_checks),
    "checks": checks,
    "claimBoundary": {
        "proved": (
            "critical transport algebra, finite Abel identity, source-side square-function "
            "weights, exact profile differences, and initial-face recurrence factors"
        ),
        "notComputerProved": (
            "smooth partition construction, heat BMO^{-1} estimate, source-to-core dual "
            "Carleson control, or Navier-Stokes time persistence"
        ),
        "notClaimed": (
            "moving-shell identification, common-top-time packing, large-data regularity, "
            "blow-up, or a Millennium solution"
        ),
    },
}

print(json.dumps(result, indent=2, sort_keys=True))
