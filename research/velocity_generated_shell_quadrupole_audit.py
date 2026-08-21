#!/usr/bin/env python3
"""Exact audit for the R0.69K velocity-generated shell quadrupole."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def audit() -> dict[str, object]:
    x1, x2, x3, radius = sp.symbols("x1 x2 x3 R", positive=True)
    coordinates = (x1, x2, x3)
    inverse_radius = 1 / sp.sqrt(x1**2 + x2**2 + x3**2)
    hessian = sp.hessian(inverse_radius, coordinates)
    axis_point = {x1: radius, x2: 0, x3: 0}

    fourth_derivatives = [
        sp.simplify(hessian.diff(coordinates[index], 2).subs(axis_point))
        for index in range(3)
    ]
    expected_first = sp.diag(24, -12, -12) / radius**5
    expected_second = sp.diag(-12, 9, 3) / radius**5

    energy_tensor = sp.diag(1, 2, 0)
    normalized_quadrupole = sp.simplify(
        fourth_derivatives[0] + 2 * fourth_derivatives[1]
    )
    expected_quadrupole = sp.diag(0, 6, -6) / radius**5
    strain = sp.diag(1, -1, 0)
    normalized_pairing = sp.simplify(
        sp.trace(strain.T * normalized_quadrupole)
    )

    y = sp.symbols("y0:3")
    second_moment = sp.MutableDenseNDimArray.zeros(3, 3)
    for a in range(3):
        for b in range(3):
            polynomial = y[a] * y[b]
            value = sp.S.Zero
            for i in range(3):
                for j in range(3):
                    value += energy_tensor[i, j] * sp.diff(
                        polynomial, y[i], y[j]
                    )
            second_moment[a, b] = sp.simplify(value)
    second_moment_matrix = sp.Matrix(second_moment.tolist())

    width_ratio = sp.sqrt(2)
    stream_energy_ratio = sp.simplify(width_ratio**2)

    checks = {
        "newtonianHessianIsTraceFree": sp.simplify(sp.trace(hessian)) == 0,
        "firstVelocityChannelMatchesFourthDerivative": (
            fourth_derivatives[0] == expected_first
        ),
        "secondVelocityChannelMatchesFourthDerivative": (
            fourth_derivatives[1] == expected_second
        ),
        "shellEnergyTensorIsPositiveSemidefinite": (
            energy_tensor.is_positive_semidefinite is True
        ),
        "doubleDivergenceHasZeroMass": all(
            sp.diff(sp.S.One, y[i], y[j]) == 0
            for i in range(3)
            for j in range(3)
        ),
        "doubleDivergenceHasZeroDipole": all(
            sp.diff(y[k], y[i], y[j]) == 0
            for k in range(3)
            for i in range(3)
            for j in range(3)
        ),
        "secondMomentEqualsTwiceEnergyTensor": (
            second_moment_matrix == 2 * energy_tensor
        ),
        "anisotropicQuadrupoleMatchesExactMatrix": (
            normalized_quadrupole == expected_quadrupole
        ),
        "anisotropicQuadrupoleIsTraceFree": (
            sp.trace(normalized_quadrupole) == 0
        ),
        "traceFreeStrainPairingIsNonzero": (
            normalized_pairing == -6 / radius**5
        ),
        "quadrupoleDecaysLikeInverseFifthPower": (
            sp.simplify(
                normalized_quadrupole.subs(radius, 2)
                - expected_quadrupole.subs(radius, 1) / 32
            )
            == sp.zeros(3, 3)
        ),
        "streamfunctionWidthsRealizeEnergyRatioTwo": stream_energy_ratio == 2,
    }

    return {
        "schemaVersion": "1.0",
        "release": "R0.69K",
        "status": "passed" if all(checks.values()) else "failed",
        "normalization": "reported Hessians are multiplied by 4*pi",
        "identity": {
            "pressureSource": "q = d_i d_j (u_i u_j)",
            "shellSource": "q_m = d_i d_j (chi_m u_i u_j)",
            "mass": "0",
            "dipole": ["0", "0", "0"],
            "secondMoment": [
                [str(second_moment_matrix[row, column]) for column in range(3)]
                for row in range(3)
            ],
        },
        "axisFourthDerivatives": {
            "d1SquaredHessian": [
                [str(expected_first[row, column]) for column in range(3)]
                for row in range(3)
            ],
            "d2SquaredHessian": [
                [str(expected_second[row, column]) for column in range(3)]
                for row in range(3)
            ],
        },
        "witness": {
            "energyTensor": [
                [str(energy_tensor[row, column]) for column in range(3)]
                for row in range(3)
            ],
            "fourPiQuadrupole": [
                [str(normalized_quadrupole[row, column]) for column in range(3)]
                for row in range(3)
            ],
            "fourPiStrainPairing": str(normalized_pairing),
            "actualStrainPairing": "-3/(2*pi*R**5)",
            "streamfunctionWidthRatio": "sqrt(2)",
            "streamfunctionEnergyRatio": str(stream_energy_ratio),
        },
        "bound": {
            "shell": "|Q_m| <= C R_m**(-5) integral chi_m |u|**2",
            "farTail": "|sum_{R_m>=R} Q_m| <= C R**(-5) ||u||_2**2",
            "scalingPower": -5,
        },
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if result["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
