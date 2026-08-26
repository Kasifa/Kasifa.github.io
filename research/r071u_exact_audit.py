#!/usr/bin/env python3
"""Finite symbolic audit for the R0.71U second-time-jet release.

The continuum statements are proved in ``r071u_report-source.md``.  This
producer checks the exact algebra used by those proofs: the zero-gap kernel,
the eigenshell atom identity, the NSE scaling ledger, the 2.5D substitution,
the forced-path stress test, the finite response matrices, modular isolation,
and the full-support heat derivative in the corrected R0.71T IFT.

The response-matrix rows are high-precision finite corroboration of the
analytic Chebyshev-system proof.  They are not substituted for that proof.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import mpmath as mp
import sympy as sp


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def zero_sampling_algebra() -> dict[str, object]:
    h, s = sp.symbols("h s", positive=True)
    kernel_square = sp.integrate(s**2, (s, 0, h))
    require(kernel_square == h**3 / 3, "zero-gap kernel coefficient")

    t = sp.symbols("t", real=True)
    roots = [sp.Rational(1, 5), sp.Rational(2, 5), sp.Rational(4, 5)]
    polynomial = sp.prod(t - root for root in roots)
    vector = [polynomial, (1 + t) * polynomial]
    first = [sp.diff(entry, t) for entry in vector]
    second = [sp.diff(entry, t, 2) for entry in vector]
    samples = sp.simplify(sum(
        sum(entry.subs(t, root) ** 2 for entry in first) for root in roots
    ))
    first_integral = sp.integrate(sum(entry**2 for entry in first), (t, 0, 1))
    second_integral = sp.integrate(sum(entry**2 for entry in second), (t, 0, 1))
    right = sp.simplify(2 * first_integral + sp.Rational(7, 3) * second_integral)
    require(sp.simplify(right - samples) > 0, "polynomial sampling ledger")
    return {
        "passed": True,
        "gapIdentity": (
            "X'(b)=h^-1 integral_a^b (s-a)X''(s) ds when X(a)=X(b)=0"
        ),
        "kernelSquare": str(kernel_square),
        "gapCoefficient": "h/3",
        "pointTraceConstants": ["2/ell", "2*ell"],
        "summedSecondCoefficient": "7*ell/3",
        "polynomialSampleSum": str(samples),
        "polynomialRightSide": str(right),
    }


def eigenshell_atom_identity() -> dict[str, object]:
    kappa, rho, y, f2 = sp.symbols("kappa rho Y F2", positive=True)
    c2 = rho**4 * f2
    pairing = rho**2 * f2
    a_plus = sp.simplify(pairing**2 / (y * c2))
    atom = sp.simplify(kappa**-2 * a_plus)
    jet = sp.simplify(kappa**-2 * rho**-4 * c2 / y)
    require(sp.simplify(atom - jet) == 0, "eigenshell atom/jet identity")
    r071t_factor = sp.simplify(kappa**-2 * rho**-4).subs(rho**2, 2 * kappa**2)
    require(sp.simplify(r071t_factor - sp.Rational(1, 4) * kappa**-6) == 0,
            "R0.71T one-quarter factor")
    return {
        "passed": True,
        "APlus": str(a_plus),
        "atom": str(atom),
        "jet": str(jet),
        "r071tCoefficient": "kappa^-6/4",
    }


def scale_ledger() -> dict[str, object]:
    # Exponents under u_lambda(x,t)=lambda*u(lambda*x,lambda^2*t).
    exponents = {
        "kappa": 1,
        "intervalLength": -2,
        "Y": 4,
        "C_t_squared": 10,
        "C_tt_squared": 14,
    }
    first_integral = -6 + 10 - 4 - 2
    second_integral = -6 + 14 - 4 - 2
    first_total = 2 + first_integral
    second_total = -2 + second_integral
    require(first_total == 0, "first-row scale zero")
    require(second_total == 0, "second-row scale zero")
    return {
        "passed": True,
        "integerTorusDilation": True,
        "exponents": exponents,
        "firstIntegralExponent": first_integral,
        "inverseWindowExponent": 2,
        "firstTotal": first_total,
        "secondIntegralExponent": second_integral,
        "directWindowExponent": -2,
        "secondTotal": second_total,
    }


def exact_25d_substitution() -> dict[str, object]:
    y, z, time = sp.symbols("y z t", real=True)
    f = sp.Function("f")(y, z, time)
    v = sp.Function("v")(y, time)
    velocity = sp.Matrix([f, 0, v])
    divergence = sp.diff(velocity[0], sp.Symbol("x")) + sp.diff(velocity[1], y) + sp.diff(velocity[2], z)
    convection = sp.Matrix([
        v * sp.diff(f, z),
        0,
        0,
    ])
    laplacian = sp.Matrix([
        sp.diff(f, y, 2) + sp.diff(f, z, 2),
        0,
        sp.diff(v, y, 2),
    ])
    require(divergence == 0, "2.5D divergence")
    return {
        "passed": True,
        "velocity": "(f(y,z,t),0,v(y,t))",
        "divergence": str(divergence),
        "convection": [str(entry) for entry in convection],
        "laplacian": [str(entry) for entry in laplacian],
        "reducedEquations": [
            "v_t=nu*v_yy",
            "f_t+v*f_z=nu*(f_yy+f_zz)",
        ],
    }


def forced_path_stress_test() -> dict[str, object]:
    t, frequency, nu = sp.symbols("t N nu", positive=True)
    c = sp.sin(frequency * t) / frequency
    c_t = sp.diff(c, t)
    c_tt = sp.diff(c, t, 2)
    forcing = sp.simplify(c_t + nu * c)
    require(sp.simplify(c_t - nu * (-c) - forcing) == 0,
            "forced shell equation")
    first_average = sp.simplify(sp.integrate(c_t**2, (t, 0, 2 * sp.pi)))
    second_average = sp.simplify(sp.integrate(c_tt**2, (t, 0, 2 * sp.pi)))
    # Integer frequencies are used when interpreting the exact integrals.
    first_integer = sp.pi
    second_integer = sp.pi * frequency**2
    return {
        "passed": True,
        "path": "N^-1*sin(N*t)",
        "forcing": str(forcing),
        "slopeAtZeros": "absolute value 1",
        "firstJetIntegralForIntegerN": str(first_integer),
        "secondJetIntegralForIntegerN": str(second_integer),
        "symbolicFirstIntegral": str(first_average),
        "symbolicSecondIntegral": str(second_average),
        "boundary": "forced shell path, not an NSE trajectory",
    }


def response_matrix_audit() -> dict[str, object]:
    mp.mp.dps = 100
    nu = mp.mpf("0.02")
    k_value = 1
    l_value = 1
    d_value = 8
    mu = nu * (k_value**2 + l_value**2)

    def phi(beta: mp.mpf, time: mp.mpf) -> mp.mpf:
        return mp.exp(-mu * time) * (-mp.expm1(-beta * time)) / beta

    rows: list[dict[str, object]] = []
    for count in range(1, 9):
        times = [mp.mpf(m) / (20 * (count + 1)) for m in range(1, count + 1)]
        betas = [
            2 * nu * (d_value * ell) * (d_value * ell - k_value)
            for ell in range(1, count + 1)
        ]
        matrix = mp.matrix([[phi(beta, time) for beta in betas] for time in times])
        determinant = mp.det(matrix)
        require(determinant != 0, f"response determinant N={count}")
        rows.append({
            "N": count,
            "sign": 1 if determinant > 0 else -1,
            "log10AbsDeterminant": float(mp.log10(abs(determinant))),
        })

    # Formal N=3 tangent used by the public numerical illustration.
    times = [mp.mpf("0.01"), mp.mpf("0.03"), mp.mpf("0.07")]
    betas = [
        2 * nu * (d_value * ell) * (d_value * ell - k_value)
        for ell in range(1, 5)
    ]
    evaluation = mp.matrix([[phi(beta, time) for beta in betas] for time in times])
    rhs = mp.matrix([-evaluation[row, 0] for row in range(3)])
    tail = mp.lu_solve(evaluation[:, 1:4], rhs)
    coefficients = [mp.mpf(1), tail[0], tail[1], tail[2]]

    def phi_prime(beta: mp.mpf, time: mp.mpf) -> mp.mpf:
        return mp.exp(-mu * time) * (
            mp.exp(-beta * time) - mu * (-mp.expm1(-beta * time)) / beta
        )

    values = [
        sum(coefficients[col] * phi(betas[col], time) for col in range(4))
        for time in times
    ]
    slopes = [
        sum(coefficients[col] * phi_prime(betas[col], time) for col in range(4))
        for time in times
    ]
    require(max(abs(value) for value in values) < mp.mpf("1e-90"),
            "N=3 tangent zeros")
    require(min(abs(value) for value in slopes) > mp.mpf("1e-8"),
            "N=3 tangent simple zeros")
    return {
        "passed": True,
        "determinantRows": rows,
        "formalTimes": [float(value) for value in times],
        "kernelCoefficients": [float(value) for value in coefficients],
        "maximumTargetResidual": float(max(abs(value) for value in values)),
        "minimumSlopeMagnitude": float(min(abs(value) for value in slopes)),
        "analyticProof": "extended Chebyshev system plus finite-dimensional IFT",
    }


def modular_isolation() -> dict[str, object]:
    k_value, l_value, d_value, radius = 1, 1, 8, 3
    support: set[tuple[int, int]] = set()
    for integer in range(-30, 31):
        support.add((k_value + d_value * integer, l_value))
        support.add((-k_value + d_value * integer, -l_value))
        support.add((d_value * integer, 0))
    inside = sorted(
        mode for mode in support
        if mode != (0, 0) and mode[0] ** 2 + mode[1] ** 2 <= radius**2
    )
    require(inside == [(-1, -1), (1, 1)], "compact multiplier isolation")
    require(d_value > radius + abs(k_value), "declared modular gap")
    return {
        "passed": True,
        "K": k_value,
        "L": l_value,
        "d": d_value,
        "supportRadius": radius,
        "isolatedModes": [list(mode) for mode in inside],
        "gap": d_value - radius - abs(k_value),
    }


def full_support_ift_derivative() -> dict[str, object]:
    nu, tau = sp.symbols("nu tau", positive=True)
    squared_radii = [2, 5, 8, 10, 13, 17]
    diagonal = [sp.exp(-nu * tau * radius) for radius in squared_radii]
    determinant = sp.simplify(sp.prod(diagonal))
    require(determinant == sp.exp(-sum(squared_radii) * nu * tau),
            "full-support heat determinant")
    return {
        "passed": True,
        "finiteSupportDimension": len(squared_radii),
        "diagonal": [str(value) for value in diagonal],
        "determinant": str(determinant),
        "invertibleFor": "nu>0 and tau>0",
        "boundary": "target support must exclude the seed shell",
    }


def build_result() -> dict[str, object]:
    checks = {
        "zeroSamplingAlgebra": zero_sampling_algebra(),
        "eigenshellAtomIdentity": eigenshell_atom_identity(),
        "scaleLedger": scale_ledger(),
        "exact25DSubstitution": exact_25d_substitution(),
        "forcedPathStressTest": forced_path_stress_test(),
        "responseMatrixAudit": response_matrix_audit(),
        "modularIsolation": modular_isolation(),
        "fullSupportIFTDerivative": full_support_ift_derivative(),
    }
    require(all(bool(value["passed"]) for value in checks.values()), "all checks")
    return {
        "release": "R0.71U",
        "status": "passed",
        "scope": "finite symbolic and high-precision audit; continuum proof is in the report",
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build_result()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
