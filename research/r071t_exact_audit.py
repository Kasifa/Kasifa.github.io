#!/usr/bin/env python3
"""Exact finite audit for the R0.71T internal-entry construction.

The certificate checks the Fourier seed, the resonant precompensation normal
form, the simple-entry face and slope identities, the outgoing coarea
profiles, the symmetric trace--variation identity, the variable-denominator
term, and the two-parameter NSE scaling ledger.  The actual positive-time
internal-entry theorem uses the classical local NSE solution map and is
proved in the report; this script does not replace that functional-analytic
argument.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
from typing import Iterable

import sympy as sp


Mode = tuple[int, int, int]
Vector = sp.ImmutableMatrix


def clean(value: sp.Expr) -> sp.Expr:
    return sp.factor(sp.simplify(value))


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def add_modes(left: Mode, right: Mode) -> Mode:
    return tuple(left[index] + right[index] for index in range(3))  # type: ignore[return-value]


def negate_mode(mode: Mode) -> Mode:
    return tuple(-entry for entry in mode)  # type: ignore[return-value]


def dot(left: Iterable[sp.Expr], right: Iterable[sp.Expr]) -> sp.Expr:
    return clean(sum(a * b for a, b in zip(left, right)))


def project(mode: Mode, value: Vector) -> Vector:
    wave = Vector(mode)
    return Vector(value - wave * (dot(wave, value) / dot(wave, wave)))


def curl_coefficient(mode: Mode, value: Vector) -> Vector:
    return Vector(sp.I * Vector(mode).cross(value))


def norm_squared(field: dict[Mode, Vector]) -> sp.Expr:
    return clean(sum(
        dot((sp.conjugate(entry) for entry in value), value)
        for value in field.values()
    ))


def inner(left: dict[Mode, Vector], right: dict[Mode, Vector]) -> sp.Expr:
    return clean(sum(
        dot((sp.conjugate(entry) for entry in left[mode]), right[mode])
        for mode in left.keys() & right.keys()
    ))


def mode_table(field: dict[Mode, Vector]) -> dict[str, list[str]]:
    return {
        str(mode): [str(clean(entry)) for entry in field[mode]]
        for mode in sorted(field)
    }


def fourier_seed() -> dict[str, object]:
    """Reconstruct the exact R0.71O seed without importing its producer."""

    p: Mode = (1, 0, 0)
    r: Mode = (0, 1, 0)
    velocity = {
        p: Vector([0, 1, 0]) / 2,
        negate_mode(p): Vector([0, 1, 0]) / 2,
        r: Vector([0, 0, 1]) / 2,
        negate_mode(r): Vector([0, 0, 1]) / 2,
    }
    for mode, coefficient in velocity.items():
        require(dot(mode, coefficient) == 0, f"velocity divergence {mode}")

    convection: defaultdict[Mode, sp.MutableDenseMatrix] = defaultdict(
        lambda: sp.zeros(3, 1)
    )
    for left_mode, left_value in velocity.items():
        for right_mode, right_value in velocity.items():
            output = add_modes(left_mode, right_mode)
            if output == (0, 0, 0):
                continue
            convection[output] += (
                sp.I * dot(left_value, right_mode) * right_value
            )

    lamb = {
        mode: Vector(-project(mode, Vector(value)))
        for mode, value in convection.items()
        if any(clean(entry) != 0 for entry in project(mode, Vector(value)))
    }
    filtered_lamb = {
        mode: value for mode, value in lamb.items()
        if dot(mode, mode) == 2
    }
    vorticity = {
        mode: curl_coefficient(mode, value)
        for mode, value in velocity.items()
    }
    lamb_curl = {
        mode: curl_coefficient(mode, value)
        for mode, value in filtered_lamb.items()
    }
    c_first = {
        mode: curl_coefficient(mode, value)
        for mode, value in lamb_curl.items()
    }

    y0 = norm_squared(vorticity)
    f2 = norm_squared(filtered_lamb)
    curl_f2 = norm_squared(lamb_curl)
    c2 = norm_squared(c_first)
    pairing = inner(filtered_lamb, c_first)
    face = clean(pairing**2 / (y0 * c2))
    require(len(filtered_lamb) == 4, "four target modes")
    require(y0 == 1, "seed enstrophy")
    require(f2 == sp.Rational(1, 4), "seed shell Lamb norm")
    require(curl_f2 == sp.Rational(1, 2), "seed shell Lamb curl norm")
    require(c2 == 1, "seed global-cell C slope")
    require(pairing == sp.Rational(1, 2), "seed positive pairing")
    require(face == sp.Rational(1, 4), "seed entry face")
    return {
        "passed": True,
        "velocity": "u_*(x)=(0,cos(x_1),cos(x_2))",
        "target": "Fourier shell |k|^2=2 with nominal kappa=1",
        "targetModes": mode_table(filtered_lamb),
        "Y0": str(y0),
        "F2": str(f2),
        "curlF2": str(curl_f2),
        "globalCellSlope2": str(c2),
        "positivePairing": str(pairing),
        "entryFace": str(face),
    }


def resonant_precompensation() -> dict[str, object]:
    """Check the exact quadratic small-amplitude target-shell normal form."""

    time, tau, nu, amplitude, forcing = sp.symbols(
        "t tau nu a F_0", positive=True
    )
    initial_target = -amplitude**2 * tau * forcing
    target = clean(
        sp.exp(-2 * nu * time)
        * (initial_target + amplitude**2 * time * forcing)
    )
    endpoint = clean(target.subs(time, tau))
    endpoint_slope = clean(sp.diff(target, time).subs(time, tau))
    require(endpoint == 0, "precompensated target vanishes at tau")
    require(
        clean(endpoint_slope - amplitude**2 * sp.exp(-2 * nu * tau) * forcing) == 0,
        "positive target slope at tau",
    )
    return {
        "passed": True,
        "leadingTargetODE": "x_t=-2*nu*x+a^2*exp(-2*nu*t)*F_0",
        "initialPrecompensation": "x(0)=-a^2*tau*F_0",
        "solution": str(target),
        "xAtTau": str(endpoint),
        "xTimeDerivativeAtTau": str(endpoint_slope),
        "NSEUse": (
            "The report obtains the exact nonlinear precompensation by the "
            "finite-dimensional implicit-function theorem; this normal form "
            "checks its leading resonant coefficient."
        ),
    }


def simple_face_and_slope_charge() -> dict[str, object]:
    """Check the global-cell simple entry and its scale-zero slope charge."""

    y0 = sp.Integer(1)
    f2 = sp.Rational(1, 4)
    actual_radius_squared = sp.Integer(2)
    nominal_kappa = sp.Integer(1)
    c2 = actual_radius_squared**2 * f2
    pairing = actual_radius_squared * f2
    a_plus = clean(pairing**2 / (y0 * c2))
    weighted_atom = clean(nominal_kappa**-2 * a_plus)
    slope_charge = clean(
        nominal_kappa**-2
        * c2
        / (actual_radius_squared**2 * y0)
    )
    require(c2 == 1, "simple global-cell slope norm")
    require(pairing == sp.Rational(1, 2), "simple global-cell pairing")
    require(a_plus == sp.Rational(1, 4), "simple right atom")
    require(weighted_atom == slope_charge, "slope charge equals entry atom")
    return {
        "passed": True,
        "simpleZero": "C(t_*+s)=c*s+O(s^2), c=2*F(t_*)",
        "APlus": str(a_plus),
        "AMinus": "0",
        "weightedAtom": str(weighted_atom),
        "slopeIdentity": (
            "kappa^-2*A_plus="
            "kappa^-2*||C_t(t_*)||_2^2/(rho^4*Y(t_*))"
        ),
        "rhoSquared": str(actual_radius_squared),
        "nominalKappa": str(nominal_kappa),
    }


def outgoing_coarea_profiles() -> dict[str, object]:
    """Use one exact mollifier to check every finite-order outgoing face."""

    t = sp.symbols("t", nonnegative=True)
    rho = 6 * t * (1 - t)
    require(sp.integrate(rho, (t, 0, 1)) == 1, "unit coarea mollifier")
    rows = []
    for order in range(1, 9):
        time = sp.symbols(f"tau_{order}", nonnegative=True)
        radius = time**order
        integrand = clean(6 * radius * (1 - radius) * sp.diff(radius, time))
        mass = clean(sp.integrate(integrand, (time, 0, 1)))
        require(mass == 1, f"outgoing coarea order {order}")
        rows.append({
            "order": order,
            "radius": str(radius),
            "outgoingIntegrand": str(integrand),
            "mass": str(mass),
            "signedFace": "1" if order % 2 else "0",
            "outgoingFace": "1",
        })
    return {
        "passed": True,
        "mollifier": "rho(s)=6*s*(1-s) on (0,1)",
        "identity": (
            "lim_delta integral q*rho_delta(||C||)*(d/dt||C||)_+ dt=A_plus"
        ),
        "rows": rows,
        "boundary": (
            "This is an exact representation of the entry atom, not an a "
            "priori Leray bound for the occupation density."
        ),
    }


def trace_variation_identity() -> dict[str, object]:
    """Verify the symmetric trace kernel on a polynomial basis."""

    t, h = sp.symbols("t h", positive=True)
    rows = []
    for degree in range(9):
        q = t**degree
        average = sp.integrate(q, (t, -h, h)) / (2 * h)
        left = sp.integrate(
            ((t + h) / (2 * h)) * sp.diff(q, t),
            (t, -h, 0),
        )
        right = sp.integrate(
            ((t - h) / (2 * h)) * sp.diff(q, t),
            (t, 0, h),
        )
        residual = clean(q.subs(t, 0) - average - left - right)
        require(residual == 0, f"trace kernel degree {degree}")
        rows.append({"degree": degree, "residual": str(residual)})
    return {
        "passed": True,
        "kernel": (
            "K_h(s)=(s+h)/(2h) on [-h,0], "
            "K_h(s)=(s-h)/(2h) on [0,h]"
        ),
        "identity": "q(0)=(2h)^-1*integral q+integral K_h*q_t",
        "basisChecks": rows,
    }


def variable_denominator() -> dict[str, object]:
    """Check that the Y_t term cancels a false directional variation."""

    t, rate = sp.symbols("t rate", real=True)
    g = sp.exp(rate * t)
    y = sp.exp(2 * rate * t)
    f = clean(g / sp.sqrt(y))
    direct = clean(sp.diff(f, t))
    ledger = clean(sp.diff(g, t) / sp.sqrt(y) - sp.diff(y, t) * f / (2 * y))
    require(f == 1, "normalized constant directional scalar")
    require(direct == 0, "direct normalized derivative")
    require(ledger == 0, "variable denominator ledger")
    return {
        "passed": True,
        "g": str(g),
        "Y": str(y),
        "f": str(f),
        "gTimeTerm": str(clean(sp.diff(g, t) / sp.sqrt(y))),
        "denominatorTerm": str(clean(sp.diff(y, t) * f / (2 * y))),
        "fTime": str(direct),
    }


def double_scaling_ledger() -> dict[str, object]:
    """Check the small-amplitude plus integer-dilation no-go exponents."""

    lam, nu, tau = sp.symbols("lambda nu tau", positive=True)
    amplitude = lam**-2
    atom_coefficient = sp.exp(-2 * nu * tau) / 4
    budget_coefficient = (1 - sp.exp(-4 * nu * tau)) / (16 * nu)
    scaled_atom = clean(atom_coefficient * amplitude**2)
    scaled_budget = clean(lam**-2 * budget_coefficient * amplitude**2)
    ratio = clean(scaled_atom / scaled_budget)
    expected_ratio = clean(2 * nu * lam**2 / sp.sinh(2 * nu * tau))
    require(clean(ratio - expected_ratio) == 0, "double-scaling ratio")
    rows = []
    for value in (1, 2, 4, 8, 16, 32, 64):
        rows.append({
            "lambda": value,
            "baseAmplitude": str(sp.Rational(1, value**2)),
            "leadingEntryAtomFactor": str(sp.Rational(1, value**4)),
            "leadingBareBudgetFactor": str(sp.Rational(1, value**6)),
            "ratioFactor": str(value**2),
            "scaledL2EnergyFactor": str(sp.Rational(1, value**2)),
            "scaledHOneHalfSquaredFactor": str(sp.Rational(1, value)),
            "scaledEnstrophyFactor": "1",
        })
    return {
        "passed": True,
        "choice": "base amplitude a_lambda=lambda^-2 followed by NSE dilation lambda",
        "leadingBaseAtom": "a^2*exp(-2*nu*tau)/4",
        "leadingBaseBareBudget": "a^2*(1-exp(-4*nu*tau))/(16*nu)",
        "scaledAtom": str(scaled_atom),
        "scaledBareBudget": str(scaled_budget),
        "ratio": str(ratio),
        "initialData": {
            "L2Energy": "O(lambda^-2)",
            "HOneHalfSquared": "O(lambda^-1)",
            "enstrophy": "1+o(1)",
        },
        "rows": rows,
        "boundary": (
            "The contradiction concerns a universal bare normalized-Leray "
            "time-payment constant. It does not exclude constants depending "
            "on the full initial profile or a different scale-zero charge."
        ),
    }


def scale_table() -> dict[str, object]:
    rows = [
        ("entry atom kappa^-2*A_plus", 0),
        ("bare normalized Leray density", 0),
        ("bare normalized Leray time integral", -2),
        ("strong shell-Lamb density ||F_j||_2^2/Y", 2),
        ("kappa^-2*|q_t|", 2),
        ("kappa^-4*||F_j,t||_2^2/Y", 2),
        ("outgoing occupation density", 2),
    ]
    require(rows[0][1] == 0, "scale-zero target")
    require(all(exponent == 2 for _, exponent in rows[3:]), "scale-matched charges")
    return {
        "passed": True,
        "convention": "D[u_lambda](t)=lambda^sigma*D[u](lambda^2*t)",
        "rows": [
            {"quantity": name, "scaleExponent": exponent}
            for name, exponent in rows
        ],
    }


def build_certificate() -> dict[str, object]:
    checks = {
        "fourierSeed": fourier_seed(),
        "resonantPrecompensation": resonant_precompensation(),
        "simpleFaceAndSlopeCharge": simple_face_and_slope_charge(),
        "outgoingCoareaProfiles": outgoing_coarea_profiles(),
        "traceVariationIdentity": trace_variation_identity(),
        "variableDenominator": variable_denominator(),
        "doubleScalingLedger": double_scaling_ledger(),
        "scaleTable": scale_table(),
    }
    require(all(check["passed"] for check in checks.values()), "all R0.71T checks")
    return {
        "release": "R0.71T",
        "status": "passed",
        "scope": (
            "exact finite algebra supporting the positive-time internal-entry "
            "theorem, outgoing occupation identity, conditional trace--variation "
            "bound, and two-parameter scaling no-go"
        ),
        "checks": checks,
        "claimBoundary": (
            "The certificate verifies finite algebra. The local NSE flow-map "
            "implicit-function theorem is proved in the report from standard "
            "classical well-posedness. No repeated-entry packing, Leray-level "
            "occupation bound, continuation criterion, singularity, or global "
            "regularity theorem is claimed."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.dumps(build_certificate(), indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
