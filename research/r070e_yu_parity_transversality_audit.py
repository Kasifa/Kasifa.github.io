#!/usr/bin/env python3
"""Exact symbolic audit for the R0.70E Yu-parity transversality gate.

The audit has deliberately narrow scope.  It verifies the explicit periodic
even/odd pair, all four coefficients of the reflection-parameter cubic, and
the leading small-frequency moment of Yu's hard annular strain kernel.  The
compact localization, heat-tail limit, Kato solution map, and implicit
function theorem are analytic arguments in the accompanying report; this
script does not pretend to certify them numerically.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


x, y, z, s, lam = sp.symbols("x y z s lam", real=True)
A1, A3 = sp.symbols("A1 A3", real=True)
a_bessel = sp.symbols("a_bessel", positive=True, real=True)
a_shell, b_shell, q = sp.symbols(
    "a_shell b_shell q", positive=True, real=True
)
coordinates = (x, y, z)


def divergence(field: sp.Matrix) -> sp.Expr:
    return sp.simplify(sum(sp.diff(field[i], coordinates[i]) for i in range(3)))


def curl(field: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.diff(field[2], y) - sp.diff(field[1], z),
            sp.diff(field[0], z) - sp.diff(field[2], x),
            sp.diff(field[1], x) - sp.diff(field[0], y),
        ]
    ).applyfunc(sp.trigsimp)


def laplacian(field: sp.Matrix) -> sp.Matrix:
    return field.applyfunc(
        lambda component: sp.simplify(
            sum(sp.diff(component, variable, 2) for variable in coordinates)
        )
    )


def strain(field: sp.Matrix) -> sp.Matrix:
    jacobian = field.jacobian(coordinates)
    return ((jacobian + jacobian.T) / 2).applyfunc(sp.trigsimp)


def stretching(field: sp.Matrix) -> sp.Expr:
    omega = curl(field)
    return sp.expand_trig(sp.expand((omega.T * strain(field) * omega)[0]))


def vector_is_zero(field: sp.Matrix) -> bool:
    return all(sp.trigsimp(component) == 0 for component in field)


def invert(field: sp.Matrix) -> sp.Matrix:
    """The Navier--Stokes inversion action R u(x)=-u(-x)."""

    return (-field.subs({x: -x, y: -y, z: -z})).applyfunc(sp.trigsimp)


# E is an ordinary even velocity and O is an ordinary odd velocity.  Under
# R u=-u(-x), their eigenvalues are -1 and +1, respectively.
E = sp.Matrix([sp.cos(y), sp.cos(z), sp.cos(x)])
O = sp.Matrix([sp.sin(y), sp.sin(z), sp.sin(x)])
potential_E = sp.Matrix([sp.sin(z), sp.sin(x), sp.sin(y)])
potential_O = curl(O)

mixed_stretching = sp.collect(sp.trigsimp(stretching(E + s * O)), s)
coefficients_s = [
    sp.trigsimp(sp.expand(mixed_stretching).coeff(s, degree))
    for degree in range(4)
]

expected_coefficients_s = [
    -3 * sp.sin(x) * sp.sin(y) * sp.sin(z),
    3
    * (
        sp.sin(x) * sp.sin(y) * sp.cos(z)
        + sp.sin(x) * sp.sin(z) * sp.cos(y)
        + sp.sin(y) * sp.sin(z) * sp.cos(x)
    ),
    -3
    * (
        sp.sin(x) * sp.cos(y) * sp.cos(z)
        + sp.sin(y) * sp.cos(x) * sp.cos(z)
        + sp.sin(z) * sp.cos(x) * sp.cos(y)
    ),
    3 * sp.cos(x) * sp.cos(y) * sp.cos(z),
]

phase_point = {x: sp.pi / 4, y: sp.pi / 4, z: sp.pi / 4}
phase_values = [sp.simplify(coefficient.subs(phase_point)) for coefficient in coefficients_s]

# If F(E+sO)=A1*s+A3*s^3 after integration against an inversion-even cutoff,
# then v=(E+O)/2 and q_lam=v-lam*R(v) give the exact four-coefficient cubic.
q_lambda_polynomial = sp.expand(
    (A1 * (1 + lam) ** 2 * (1 - lam) + A3 * (1 - lam) ** 3) / 8
)
q_lambda_coefficients = [
    sp.expand(q_lambda_polynomial).coeff(lam, degree) for degree in range(4)
]
expected_lambda_coefficients = [
    (A1 + A3) / 8,
    (A1 - 3 * A3) / 8,
    (-A1 + 3 * A3) / 8,
    (-A1 - A3) / 8,
]

# Leading hard-shell multiplier.  For a plane wave with wavevector e1 and
# vorticity in e2, K_132=3(z1^2-z3^2)/(8*pi*|z|^5).  The constant and odd
# Taylor terms vanish.  The q^2 coefficient uses
# integral_S2(n1^4-n1^2*n3^2)=8*pi/15 and integral_a^b r dr=(b^2-a^2)/2.
angular_fourth_moment_difference = sp.Rational(8, 15) * sp.pi
radial_first_moment = (b_shell**2 - a_shell**2) / 2
kernel_multiplier_q2 = sp.simplify(
    -sp.Rational(1, 2)
    * sp.Rational(3, 8)
    / sp.pi
    * angular_fourth_moment_difference
    * radial_first_moment
)
# With Yu's kernel and omega=curl(u), the full S_13/omega_2 multiplier is
# -1/2.  Therefore the scalar shell multiplier relative to the full strain is
# -2 times the kernel-component multiplier.
relative_shell_multiplier_q2 = sp.simplify(-2 * kernel_multiplier_q2)

# Exact spherical-Bessel antiderivative and the next Taylor coefficient.
j1 = sp.sin(a_bessel) / a_bessel**2 - sp.cos(a_bessel) / a_bessel
j2 = (
    (sp.Integer(3) / a_bessel**3 - sp.Integer(1) / a_bessel)
    * sp.sin(a_bessel)
    - sp.Integer(3) * sp.cos(a_bessel) / a_bessel**2
)
bessel_antiderivative_check = sp.trigsimp(
    sp.diff(j1 / a_bessel, a_bessel) + j2 / a_bessel
)
relative_shell_multiplier_q4 = -(b_shell**4 - a_shell**4) / 280

equal_phase_substitution = {x: s, y: s, z: s}
equal_phase_base = sp.trigsimp(coefficients_s[0].subs(equal_phase_substitution))
equal_phase_linear = sp.trigsimp(coefficients_s[1].subs(equal_phase_substitution))
equal_phase_cubic = sp.trigsimp(coefficients_s[3].subs(equal_phase_substitution))

checks = {
    "evenFieldDivergenceFree": divergence(E) == 0,
    "oddFieldDivergenceFree": divergence(O) == 0,
    "evenPotentialCurlsToField": vector_is_zero(curl(potential_E) - E),
    "oddPotentialCurlsToField": vector_is_zero(curl(potential_O) - O),
    "evenFieldREigenvalueMinusOne": vector_is_zero(invert(E) + E),
    "oddFieldREigenvaluePlusOne": vector_is_zero(invert(O) - O),
    "commonHeatEigenvalue": vector_is_zero(laplacian(E) + E)
    and vector_is_zero(laplacian(O) + O),
    "allFourStretchingCoefficients": all(
        sp.trigsimp(actual - expected) == 0
        for actual, expected in zip(coefficients_s, expected_coefficients_s)
    ),
    "coefficientParityOddEvenOddEven": all(
        sp.trigsimp(
            coefficient.subs({x: -x, y: -y, z: -z})
            - ((-1) ** (degree + 1)) * coefficient
        )
        == 0
        for degree, coefficient in enumerate(coefficients_s)
    ),
    "phasePointValues": phase_values
    == [
        -3 * sp.sqrt(2) / 4,
        9 * sp.sqrt(2) / 4,
        -9 * sp.sqrt(2) / 4,
        3 * sp.sqrt(2) / 4,
    ],
    "lambdaFourCoefficients": all(
        sp.simplify(actual - expected) == 0
        for actual, expected in zip(
            q_lambda_coefficients, expected_lambda_coefficients
        )
    ),
    "lambdaRootAtOne": sp.simplify(q_lambda_polynomial.subs(lam, 1)) == 0,
    "lambdaDerivativeAtOne": sp.simplify(
        sp.diff(q_lambda_polynomial, lam).subs(lam, 1) + A1 / 2
    )
    == 0,
    "lambdaAntiPalindromic": q_lambda_coefficients[3]
    == -q_lambda_coefficients[0]
    and q_lambda_coefficients[2] == -q_lambda_coefficients[1],
    "sphereMoment": angular_fourth_moment_difference == 8 * sp.pi / 15,
    "kernelComponentLeadingMoment": kernel_multiplier_q2
    == -(b_shell**2 - a_shell**2) / 20,
    "relativeShellLeadingMoment": relative_shell_multiplier_q2
    == (b_shell**2 - a_shell**2) / 10,
    "besselAntiderivative": bessel_antiderivative_check == 0,
    "relativeShellNextMoment": relative_shell_multiplier_q4
    == -(b_shell**4 - a_shell**4) / 280,
    "equalPhaseBase": sp.trigsimp(equal_phase_base + 3 * sp.sin(s) ** 3) == 0,
    "equalPhaseLinear": sp.trigsimp(
        equal_phase_linear - sp.Rational(9, 4) * (sp.cos(s) - sp.cos(3 * s))
    )
    == 0,
    "equalPhaseCubic": sp.trigsimp(equal_phase_cubic - 3 * sp.cos(s) ** 3)
    == 0,
}

if not all(checks.values()):
    failed = [name for name, passed in checks.items() if not passed]
    raise AssertionError(f"failed exact checks: {failed}")

result = {
    "status": "exact-symbolic-audit",
    "release": "R0.70E",
    "arithmetic": "exact SymPy trigonometry and spherical moments",
    "periodicPair": {
        "evenVelocityE": [sp.sstr(component) for component in E],
        "oddVelocityO": [sp.sstr(component) for component in O],
        "potentialE": [sp.sstr(component) for component in potential_E],
        "potentialO": [sp.sstr(component) for component in potential_O],
        "stretchingPolynomial": sp.sstr(mixed_stretching),
        "coefficientsAtPiOverFour": [sp.sstr(value) for value in phase_values],
        "localization": (
            "curl(rho_L*A_E) and curl(rho_L*A_O), with rho_L even and "
            "constant on the complete core-plus-shell dependency region"
        ),
    },
    "reflectionCubic": {
        "parameterization": (
            "q_lambda=((1+lambda)/2)E+((1-lambda)/2)O"
        ),
        "polynomial": sp.sstr(q_lambda_polynomial),
        "coefficientsIncreasingPower": [
            sp.sstr(value) for value in q_lambda_coefficients
        ],
        "root": "1",
        "derivativeAtRoot": "-A1/2",
        "simpleRootCondition": "A1 != 0",
    },
    "hardShellMoment": {
        "kernelComponent": "K_132=3*(z1^2-z3^2)/(8*pi*|z|^5)",
        "angularMoment": sp.sstr(angular_fourth_moment_difference),
        "componentMultiplier": (
            "-q^2*(b_shell^2-a_shell^2)/20 + O(q^4*b_shell^4)"
        ),
        "relativeStrainMultiplier": (
            "+q^2*(b_shell^2-a_shell^2)/10 "
            "- q^4*(b_shell^4-a_shell^4)/280 + O(q^6*b_shell^6)"
        ),
        "exactBesselMultiplier": (
            "3*(j1(q*a_shell)/(q*a_shell) "
            "- j1(q*b_shell)/(q*b_shell))"
        ),
        "claimBoundary": (
            "This is a small-frequency analytic coefficient, not a DNS or "
            "interval-arithmetic simulation."
        ),
    },
    "claimBoundary": (
        "The script certifies algebraic identities only. Compact localization, "
        "heat-tail convergence, small-data Navier--Stokes smooth dependence, "
        "and implicit-function tuning remain analytic proof steps."
    ),
    "checks": checks,
}

payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
parser = argparse.ArgumentParser()
parser.add_argument("--output", type=Path)
arguments = parser.parse_args()
if arguments.output is not None:
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(payload, encoding="utf-8")
print(payload, end="")
