#!/usr/bin/env python3
"""Exact symbolic audit for the R0.70F fixed-annulus affine-jet gate.

The script verifies the finite algebra in the report: compact-localization
homotopy potentials before cutoff differentiation, the constant and linear
harmonic strain cores, the solid-rotation vorticity carrier, the two exact
initial-face work factors, and the closed triangular dyadic sums.

It does not computer-prove smooth cutoff support separation, the heat-kernel
BMO^{-1} estimate, Koch--Tataru well-posedness, or any common-top-time
Navier--Stokes packing statement.
"""

from __future__ import annotations

import json

import sympy as sp


x1, x2, x3 = sp.symbols("x1 x2 x3", real=True)
coordinates = sp.Matrix([x1, x2, x3])


def divergence(field: sp.Matrix) -> sp.Expr:
    return sp.simplify(
        sum(sp.diff(field[index], coordinates[index]) for index in range(3))
    )


def curl(field: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.diff(field[2], x2) - sp.diff(field[1], x3),
            sp.diff(field[0], x3) - sp.diff(field[2], x1),
            sp.diff(field[1], x1) - sp.diff(field[0], x2),
        ]
    ).applyfunc(sp.simplify)


def strain(field: sp.Matrix) -> sp.Matrix:
    jacobian = field.jacobian(coordinates)
    return ((jacobian + jacobian.T) / 2).applyfunc(sp.simplify)


def laplacian_scalar(expression: sp.Expr) -> sp.Expr:
    return sp.simplify(
        sum(sp.diff(expression, variable, 2) for variable in coordinates)
    )


def homotopy_potential(field: sp.Matrix, degree: int) -> sp.Matrix:
    return (
        -sp.Rational(1, degree + 2) * coordinates.cross(field)
    ).applyfunc(sp.expand)


constant_strain = sp.diag(1, -sp.Rational(1, 2), -sp.Rational(1, 2))
constant_velocity = constant_strain * coordinates

phi = x1**3 - 3 * x1 * x2**2
linear_velocity = sp.Matrix([sp.diff(phi, variable) for variable in coordinates])
linear_strain = sp.hessian(phi, coordinates)

rotation_matrix = sp.Matrix(
    [
        [0, 0, 0],
        [0, 0, -sp.Rational(1, 2)],
        [0, sp.Rational(1, 2), 0],
    ]
)
rotation_velocity = rotation_matrix * coordinates

constant_potential = homotopy_potential(constant_velocity, 1)
linear_potential = homotopy_potential(linear_velocity, 2)
rotation_potential = homotopy_potential(rotation_velocity, 1)

e1 = sp.Matrix([1, 0, 0])
c = sp.symbols("c", positive=True)

R, r, b, eta, c_chi = sp.symbols(
    "R r b eta c_chi", positive=True
)
core_vorticity_amplitude = b / r**2
cutoff_volume = c_chi * eta**3 * r**3
cutoff_first_x1_moment = c * r * cutoff_volume

constant_snapshot_work = sp.simplify(
    r**3
    * R**-2
    * core_vorticity_amplitude**2
    * cutoff_volume
)
linear_snapshot_work = sp.simplify(
    r**3
    * 6
    * R**-3
    * core_vorticity_amplitude**2
    * cutoff_first_x1_moment
)

Lambda = sp.symbols("Lambda", positive=True)
constant_interlaced_work = sp.simplify(
    constant_snapshot_work.subs(r, R / Lambda)
)
linear_interlaced_work = sp.simplify(
    linear_snapshot_work.subs(r, R / Lambda)
)

beta = sp.symbols("beta", positive=True)
q = sp.symbols("q", positive=True)
N = sp.symbols("N", integer=True, positive=True)
triangular_closed_q = sp.simplify(
    N * q / (1 - q) - q**2 * (1 - q**N) / (1 - q) ** 2
)
triangular_closed_beta = (
    N / (2**beta - 1)
    - (1 - 2 ** (-beta * N)) / (2**beta - 1) ** 2
)

finite_sum_checks = {}
for beta_value in range(1, 5):
    q_value = sp.Rational(1, 2**beta_value)
    for n_value in range(1, 13):
        direct = sum(
            q_value ** (k_value - j_value)
            for k_value in range(1, n_value + 1)
            for j_value in range(k_value)
        )
        closed = triangular_closed_q.subs({q: q_value, N: n_value})
        finite_sum_checks[f"beta{beta_value}N{n_value}"] = (
            sp.simplify(direct - closed) == 0
        )

slopes = {
    degree: sp.simplify(
        sp.limit(
            triangular_closed_beta.subs(beta, degree) / N,
            N,
            sp.oo,
        )
    )
    for degree in range(1, 5)
}

checks = {
    "constantVelocityDivergenceFree": divergence(constant_velocity) == 0,
    "constantVelocityCurlFree": curl(constant_velocity) == sp.zeros(3, 1),
    "constantPotentialRecoversVelocity": (
        curl(constant_potential) == constant_velocity
    ),
    "constantCoreStrain": strain(constant_velocity) == constant_strain,
    "constantStrainSymmetric": constant_strain == constant_strain.T,
    "constantStrainTraceFree": sp.trace(constant_strain) == 0,
    "constantStrainPositiveOnE1": (
        sp.simplify((e1.T * constant_strain * e1)[0]) == 1
    ),
    "harmonicCubic": laplacian_scalar(phi) == 0,
    "linearVelocityDivergenceFree": divergence(linear_velocity) == 0,
    "linearVelocityCurlFree": curl(linear_velocity) == sp.zeros(3, 1),
    "linearPotentialRecoversVelocity": (
        curl(linear_potential) == linear_velocity
    ),
    "linearCoreStrainIsHessian": strain(linear_velocity) == linear_strain,
    "linearStrainAtPositiveLobe": (
        sp.simplify(
            (e1.T * linear_strain.subs({x1: c, x2: 0, x3: 0}) * e1)[0]
        )
        == 6 * c
    ),
    "rotationVelocityDivergenceFree": divergence(rotation_velocity) == 0,
    "rotationPotentialRecoversVelocity": (
        curl(rotation_potential) == rotation_velocity
    ),
    "rotationCoreVorticityE1": curl(rotation_velocity) == e1,
    "rotationCoreStrainZero": strain(rotation_velocity) == sp.zeros(3),
    "constantSnapshotFactor": (
        constant_interlaced_work
        == b**2 * c_chi * eta**3 / Lambda**2
    ),
    "linearSnapshotFactor": (
        linear_interlaced_work
        == 6 * b**2 * c * c_chi * eta**3 / Lambda**3
    ),
    "allFiniteTriangularSums": all(finite_sum_checks.values()),
    "triangularBetaOneSlope": slopes[1] == 1,
    "triangularBetaTwoSlope": slopes[2] == sp.Rational(1, 3),
    "triangularBetaThreeSlope": slopes[3] == sp.Rational(1, 7),
    "triangularBetaFourSlope": slopes[4] == sp.Rational(1, 15),
}

if not all(checks.values()):
    failed = [name for name, passed in checks.items() if not passed]
    raise AssertionError(f"failed exact checks: {failed}")

result = {
    "status": "exact-symbolic-audit",
    "release": "R0.70F",
    "arithmetic": "exact SymPy polynomial and rational arithmetic",
    "compactCoreGenerators": {
        "constantVelocity": [sp.sstr(value) for value in constant_velocity],
        "constantStrain": [
            [sp.sstr(value) for value in row]
            for row in constant_strain.tolist()
        ],
        "constantHomotopyPotential": [
            sp.sstr(value) for value in constant_potential
        ],
        "harmonicCubic": sp.sstr(phi),
        "linearVelocity": [sp.sstr(value) for value in linear_velocity],
        "linearStrain": [
            [sp.sstr(value) for value in row]
            for row in linear_strain.tolist()
        ],
        "linearHomotopyPotential": [
            sp.sstr(value) for value in linear_potential
        ],
        "rotationVelocity": [sp.sstr(value) for value in rotation_velocity],
        "rotationVorticity": [
            sp.sstr(value) for value in curl(rotation_velocity)
        ],
        "rotationHomotopyPotential": [
            sp.sstr(value) for value in rotation_potential
        ],
    },
    "initialFaceWork": {
        "constantRawFormula": sp.sstr(constant_snapshot_work),
        "linearRawFormula": sp.sstr(linear_snapshot_work),
        "constantInterlacedFormula": sp.sstr(constant_interlaced_work),
        "linearInterlacedFormula": sp.sstr(linear_interlaced_work),
        "scaleRatio": "r/R=1/Lambda",
        "vorticityFactor": "b_n=sum_{a=0}^{n-1} Lambda^(-4a)",
    },
    "taylorWorkPowers": {
        "constant": "theta^1",
        "linear": "theta^2",
        "affineRemainder": "theta^3",
        "quadraticRemainder": "theta^4",
    },
    "triangularDyadicSum": {
        "closedForm": (
            "N/(2^beta-1)"
            " - (1-2^(-beta*N))/(2^beta-1)^2"
        ),
        "asymptoticSlopes": {
            str(degree): sp.sstr(value) for degree, value in slopes.items()
        },
        "finiteCasesChecked": len(finite_sum_checks),
    },
    "checks": checks,
    "claimBoundary": {
        "proved": (
            "finite polynomial identities, exact initial-face scale factors, "
            "and exact discrete growth formula"
        ),
        "notComputerProved": (
            "smooth support buffers, BMO^{-1} heat estimate, Koch-Tataru "
            "theory, or common-top-time Navier-Stokes packing"
        ),
        "notClaimed": (
            "identification with Yu's moving-shell positive quantity, "
            "large-data regularity, blow-up, or a Millennium solution"
        ),
    },
}

print(json.dumps(result, indent=2, sort_keys=True))
