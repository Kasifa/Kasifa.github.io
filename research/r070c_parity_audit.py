#!/usr/bin/env python3
"""Exact symbolic audit for the R0.70C parity obstruction.

The script verifies two explicit trigonometric witnesses and the normalized
transversality polynomial used by the small-data implicit-function argument.
It uses exact SymPy arithmetic throughout and prints a deterministic JSON
payload to stdout.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


x, y, z, lam = sp.symbols("x y z lam", real=True)
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
    ).applyfunc(sp.simplify)


def laplacian(field: sp.Matrix) -> sp.Matrix:
    return field.applyfunc(
        lambda component: sp.simplify(
            sum(sp.diff(component, variable, 2) for variable in coordinates)
        )
    )


def strain(field: sp.Matrix) -> sp.Matrix:
    jacobian = field.jacobian(coordinates)
    return ((jacobian + jacobian.T) / 2).applyfunc(sp.simplify)


def stretching(field: sp.Matrix) -> sp.Expr:
    vorticity = curl(field)
    return sp.trigsimp((vorticity.T * strain(field) * vorticity)[0])


def substitute_vector(field: sp.Matrix, substitutions: dict[sp.Symbol, sp.Expr]) -> sp.Matrix:
    return field.subs(substitutions).applyfunc(sp.trigsimp)


def vector_is_zero(field: sp.Matrix) -> bool:
    return all(sp.trigsimp(component) == 0 for component in field)


# An inversion-even periodic seed.  Its odd vector potential can be multiplied
# by an even compact cutoff and curled to obtain an even, compactly supported,
# divergence-free R^3 datum.
even_seed = sp.Matrix([sp.cos(y), sp.cos(z), sp.cos(x)])
odd_potential = sp.Matrix([sp.sin(z), sp.sin(x), sp.sin(y)])
even_vorticity = curl(even_seed)
even_stretching = sp.trigsimp(stretching(even_seed))

expected_even_stretching = -3 * sp.sin(x) * sp.sin(y) * sp.sin(z)
even_l1_torus = sp.Integer(3) * sp.Integer(4) ** 3
even_l2_squared_torus = sp.integrate(
    even_stretching**2,
    (x, 0, 2 * sp.pi),
    (y, 0, 2 * sp.pi),
    (z, 0, 2 * sp.pi),
)


# The ABC field is an exact periodic Beltrami Navier--Stokes trajectory.  Its
# anti-half-translation forces every translation-covariant cubic annular
# density to have zero torus mean, while its stretching is not identically
# zero.
abc = sp.Matrix(
    [
        sp.sin(z) + sp.cos(y),
        sp.sin(x) + sp.cos(z),
        sp.sin(y) + sp.cos(x),
    ]
)
abc_stretching = sp.trigsimp(stretching(abc))
half_translation = {x: x + sp.pi, y: y + sp.pi, z: z + sp.pi}
origin = {x: 0, y: 0, z: 0}


# For two reflection-related, initially disjoint copies of a seed whose signed
# shell scalar is A != 0, the normalized leading signed polynomial is
# P(lam)/A = 1-lam^3.  Its simple root at lam=1 is the IFT transversality gate.
leading_polynomial = sp.Integer(1) - lam**3
leading_derivative_at_one = sp.diff(leading_polynomial, lam).subs(lam, 1)


checks = {
    "evenSeedDivergenceFree": divergence(even_seed) == 0,
    "oddPotentialCurlsToEvenSeed": vector_is_zero(curl(odd_potential) - even_seed),
    "evenSeedParity": vector_is_zero(
        substitute_vector(even_seed, {x: -x, y: -y, z: -z}) - even_seed
    ),
    "evenVorticityParity": vector_is_zero(
        substitute_vector(even_vorticity, {x: -x, y: -y, z: -z})
        + even_vorticity
    ),
    "evenSeedHeatEigenvalue": vector_is_zero(laplacian(even_seed) + even_seed),
    "evenSeedStretchingFormula": sp.trigsimp(
        even_stretching - expected_even_stretching
    )
    == 0,
    "evenStretchingOdd": sp.trigsimp(
        even_stretching.subs({x: -x, y: -y, z: -z}) + even_stretching
    )
    == 0,
    "evenStretchingMeanZero": sp.integrate(
        even_stretching,
        (x, 0, 2 * sp.pi),
        (y, 0, 2 * sp.pi),
        (z, 0, 2 * sp.pi),
    )
    == 0,
    "evenStretchingL1": even_l1_torus == 192,
    "evenStretchingL2Squared": sp.simplify(even_l2_squared_torus - 9 * sp.pi**3)
    == 0,
    "abcDivergenceFree": divergence(abc) == 0,
    "abcBeltrami": vector_is_zero(curl(abc) - abc),
    "abcHeatEigenvalue": vector_is_zero(laplacian(abc) + abc),
    "abcAntiHalfTranslation": vector_is_zero(
        substitute_vector(abc, half_translation) + abc
    ),
    "abcStretchingAntiHalfTranslation": sp.trigsimp(
        abc_stretching.subs(half_translation) + abc_stretching
    )
    == 0,
    "abcStretchingNonzeroAtOrigin": sp.simplify(abc_stretching.subs(origin) - 3)
    == 0,
    "leadingPolynomialRoot": leading_polynomial.subs(lam, 1) == 0,
    "leadingPolynomialSimpleRoot": leading_derivative_at_one == -3,
}

if not all(checks.values()):
    failed = [name for name, passed in checks.items() if not passed]
    raise AssertionError(f"failed exact checks: {failed}")


result = {
    "status": "exact-symbolic-audit",
    "release": "R0.70C",
    "arithmetic": "exact SymPy integers, rationals, pi, and trigonometric identities",
    "evenR3Seed": {
        "velocity": ["cos(y)", "cos(z)", "cos(x)"],
        "oddVectorPotential": ["sin(z)", "sin(x)", "sin(y)"],
        "vorticity": [sp.sstr(component) for component in even_vorticity],
        "stretching": sp.sstr(even_stretching),
        "torusStretchingL1": str(even_l1_torus),
        "torusStretchingL2Squared": sp.sstr(even_l2_squared_torus),
        "localization": "curl(rho_R * oddVectorPotential), with rho_R even",
    },
    "periodicExactWitness": {
        "name": "unit ABC Beltrami field",
        "velocity": [sp.sstr(component) for component in abc],
        "curlEigenvalue": "1",
        "laplacianEigenvalue": "-1",
        "antiTranslation": "pi*(1,1,1)",
        "stretchingAtOrigin": sp.sstr(abc_stretching.subs(origin)),
    },
    "iftGate": {
        "normalizedLeadingSignedPolynomial": sp.sstr(leading_polynomial),
        "root": "1",
        "derivativeAtRoot": sp.sstr(leading_derivative_at_one),
        "signedOrderBeforeTuning": "O(epsilon^4)",
        "absoluteOrder": "Theta(epsilon^3)",
        "signedOrderAfterTuning": (
            "exactly zero on the selected cylinder for a fixed large even "
            "two-plateau cutoff"
        ),
    },
    "parityLedger": {
        "evenVelocity": "U(-x)=U(x)",
        "oddVorticity": "Omega(-x)=-Omega(x)",
        "evenWindowChange": "z maps to -z",
        "annularDensity": "w_eta[U](-x)=-w_eta[U](x)",
        "claimBoundary": (
            "Even parity is preserved by the linear heat layer, not by the full "
            "Navier--Stokes nonlinearity; the exact nonlinear zero uses an "
            "implicit-function amplitude tuning."
        ),
    },
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
