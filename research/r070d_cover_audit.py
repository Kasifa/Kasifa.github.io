#!/usr/bin/env python3
"""Exact symbolic audit for the R0.70D cover-positivity obstruction.

The producer checks the exact negative-part mass of

    f_{delta,N}(x) = delta + sin(N*x_1)

on the three-torus and the algebraic frequency gate behind the uniform
refined-cutoff estimate.  It uses no floating-point decision arithmetic.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


delta, x = sp.symbols("delta x", positive=True, real=True)
m0, c1, n = sp.symbols("m0 c1 n", positive=True, real=True)
alpha = sp.asin(delta)

negative_part_1d_direct = sp.integrate(
    -(delta + sp.sin(x)),
    (x, sp.pi + alpha, 2 * sp.pi - alpha),
)
negative_part_1d = (
    2 * sp.sqrt(1 - delta**2)
    - delta * (sp.pi - 2 * sp.asin(delta))
)
negative_part_3d = sp.expand((2 * sp.pi) ** 2 * negative_part_1d)
signed_mass_3d = delta * (2 * sp.pi) ** 3
ratio = sp.simplify(negative_part_3d / signed_mass_3d)

half_value_1d = sp.simplify(negative_part_1d.subs(delta, sp.Rational(1, 2)))
zero_limit_1d = sp.limit(negative_part_1d, delta, 0, dir="+")
zero_limit_3d = sp.limit(negative_part_3d, delta, 0, dir="+")
ratio_coefficient = sp.limit(delta * ratio, delta, 0, dir="+")
negative_mass_derivative = sp.simplify(sp.diff(negative_part_1d, delta))

# If ||partial_1 psi||_1 <= c1 and int psi >= m0, integration by parts gives
# an error at most c1/n in the weighted local mean numerator.  The frequency
# gate n >= 2*c1/(delta*m0) makes the normalized error at most delta/2.
inverse_frequency_gate = sp.simplify(delta * m0 / (2 * c1))
normalized_error_at_gate = sp.simplify(c1 * inverse_frequency_gate / m0)
normalized_lower_at_gate = sp.simplify(delta - normalized_error_at_gate)
normalized_upper_at_gate = sp.simplify(delta + normalized_error_at_gate)

checks = {
    "directNegativePartFormula": sp.simplify(
        negative_part_1d_direct - negative_part_1d
    )
    == 0,
    "negativePartDerivative": sp.simplify(
        negative_mass_derivative + sp.pi - 2 * sp.asin(delta)
    )
    == 0,
    "halfAmplitudeValue": sp.simplify(
        half_value_1d - (sp.sqrt(3) - sp.pi / 3)
    )
    == 0,
    "exactHalfIntervalLowerBoundPositive": bool(
        sp.sqrt(3) - sp.pi / 3 > 0
    ),
    "oneDimensionalZeroLimit": zero_limit_1d == 2,
    "threeDimensionalZeroLimit": sp.simplify(zero_limit_3d - 8 * sp.pi**2)
    == 0,
    "ratioLeadingCoefficient": sp.simplify(ratio_coefficient - 1 / sp.pi)
    == 0,
    "frequencyGateNormalizedError": sp.simplify(
        normalized_error_at_gate - delta / 2
    )
    == 0,
    "frequencyGateLowerAverage": sp.simplify(
        normalized_lower_at_gate - delta / 2
    )
    == 0,
    "frequencyGateUpperAverage": sp.simplify(
        normalized_upper_at_gate - 3 * delta / 2
    )
    == 0,
}

if not all(checks.values()):
    failed = [name for name, passed in checks.items() if not passed]
    raise AssertionError(f"failed exact checks: {failed}")

result = {
    "status": "exact-symbolic-audit",
    "release": "R0.70D",
    "arithmetic": "exact SymPy integers, rationals, pi, radicals, and inverse trigonometric functions",
    "witness": {
        "domain": "T^3 = [0,2*pi)^3",
        "density": "f_delta_N(x) = delta + sin(N*x_1)",
        "parameterRange": "0 < delta <= 1/2; N is a positive integer",
        "signedMass": sp.sstr(signed_mass_3d),
        "negativePartMass": sp.sstr(negative_part_3d),
        "negativePartMassAtDeltaHalf": sp.sstr(
            sp.expand((2 * sp.pi) ** 2 * half_value_1d)
        ),
        "negativePartMassLimitAtZero": sp.sstr(zero_limit_3d),
        "negativeToSignedRatio": sp.sstr(ratio),
        "ratioLeadingAsymptotic": "1/(pi*delta)",
    },
    "cutoffGate": {
        "class": (
            "psi >= 0, integral(psi) >= m0 > 0, "
            "L1_norm(partial_1 psi) <= c1"
        ),
        "integrationByParts": (
            "abs(integral psi*sin(N*x_1)) <= c1/N"
        ),
        "frequencyCondition": "N >= 2*c1/(delta*m0)",
        "everyNormalizedLocalAverage": "delta/2 <= <f>_psi <= 3*delta/2",
        "ensembleConsequence": (
            "every positive-weight ensemble of normalized local averages lies "
            "in the same interval"
        ),
    },
    "claimBoundary": (
        "This is an abstract scalar measure-theoretic obstruction. It does not "
        "realize f as Navier--Stokes flux or annular vortex stretching and does "
        "not negate PDE conclusions that use additional local balance terms."
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
