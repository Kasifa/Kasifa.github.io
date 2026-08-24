#!/usr/bin/env python3
"""Exact symbolic audit for the R0.70B 3:4:5 triad obstruction.

The script derives, rather than hard-codes, the four helical rows used in the
normal-form no-go.  All displayed coefficients are exact SymPy rationals.
It is a consistency audit of the finite-dimensional symbol calculation, not
a computer-assisted proof of the wave-packet limiting argument.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


I = sp.I
SQRT2 = sp.sqrt(2)


def dot(left: sp.Matrix, right: sp.Matrix) -> sp.Expr:
    """Bilinear Fourier-triad pairing; deliberately no complex conjugation."""

    return sp.expand((left.T * right)[0])


def cross(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(left).cross(sp.Matrix(right))


def norm_sq(vector: sp.Matrix) -> sp.Expr:
    return dot(vector, vector)


def projector(wave: sp.Matrix) -> sp.Matrix:
    return sp.eye(3) - wave * wave.T / norm_sq(wave)


def velocity_from_vorticity(wave: sp.Matrix, amplitude: sp.Matrix) -> sp.Matrix:
    return sp.simplify(I * cross(wave, amplitude) / norm_sq(wave))


def strain_symbol(wave: sp.Matrix, vorticity: sp.Matrix) -> sp.Matrix:
    velocity = velocity_from_vorticity(wave, vorticity)
    return sp.simplify(I * (wave * velocity.T + velocity * wave.T) / 2)


def euler_vorticity_pair(
    output: sp.Matrix,
    first_wave: sp.Matrix,
    first_vorticity: sp.Matrix,
    second_wave: sp.Matrix,
    second_vorticity: sp.Matrix,
) -> sp.Matrix:
    """Polarized Euler vorticity nonlinearity at output=first+second.

    The Leray projector is retained in the velocity nonlinearity before curl.
    """

    assert output == first_wave + second_wave
    first_velocity = velocity_from_vorticity(first_wave, first_vorticity)
    second_velocity = velocity_from_vorticity(second_wave, second_vorticity)
    convection = (
        dot(second_wave, first_velocity) * second_velocity
        + dot(first_wave, second_velocity) * first_velocity
    )
    velocity_nonlinearity = -I * projector(output) * convection
    return sp.simplify(I * cross(output, velocity_nonlinearity))


def helical_basis(name: str, sign: int) -> sp.Matrix:
    if sign not in {-1, 1}:
        raise ValueError("helical sign must be -1 or +1")
    if name == "k":
        return sp.Matrix([0, 1, I * sign]) / SQRT2
    if name == "p":
        return sp.Matrix([-1, 0, I * sign]) / SQRT2
    if name == "q":
        return sp.Matrix([sp.Rational(4, 5), sp.Rational(-3, 5), I * sign]) / SQRT2
    raise ValueError(name)


def rational_string(value: sp.Expr) -> str:
    value = sp.simplify(value)
    if value.is_Rational:
        return str(value)
    return sp.sstr(value)


def derive_rows() -> tuple[sp.Matrix, sp.Matrix, list[tuple[int, int, int]]]:
    k = sp.Matrix([3, 0, 0])
    p = sp.Matrix([0, 4, 0])
    q = sp.Matrix([-3, -4, 0])
    assert k + p + q == sp.zeros(3, 1)

    sign_rows = [(-1, -1, -1), (-1, -1, 1), (-1, 1, -1), (-1, 1, 1)]
    # A single oriented complex triad carries sqrt(2)/50.  Adding its
    # conjugate orientation to form a real six-mode field doubles both sides,
    # so the corresponding real-field common factor is sqrt(2)/25.
    common = SQRT2 / 50
    derivative_rows: list[list[sp.Expr]] = []
    target_rows: list[list[sp.Expr]] = []

    for sigma_k, sigma_p, sigma_q in sign_rows:
        a = helical_basis("k", sigma_k)
        b = helical_basis("p", sigma_p)
        c = I * helical_basis("q", sigma_q)

        derivative = [
            dot(a, euler_vorticity_pair(-k, p, b, q, c)),
            dot(b, euler_vorticity_pair(-p, q, c, k, a)),
            dot(c, euler_vorticity_pair(-q, k, a, p, b)),
        ]
        target = [
            2 * dot(b, strain_symbol(k, a) * c),
            2 * dot(c, strain_symbol(p, b) * a),
            2 * dot(a, strain_symbol(q, c) * b),
        ]

        derivative_rows.append([sp.simplify(entry / common) for entry in derivative])
        target_rows.append([sp.simplify(entry / common) for entry in target])

    return sp.Matrix(derivative_rows), sp.Matrix(target_rows), sign_rows


def audit() -> dict[str, object]:
    derivative, target, sign_rows = derive_rows()
    k = sp.Matrix([3, 0, 0])
    p = sp.Matrix([0, 4, 0])
    q = sp.Matrix([-3, -4, 0])

    helical_residuals: list[sp.Matrix] = []
    divergence_residuals: list[sp.Expr] = []
    for name, wave in [("k", k), ("p", p), ("q", q)]:
        length = sp.sqrt(norm_sq(wave))
        for sign in (-1, 1):
            basis = helical_basis(name, sign)
            divergence_residuals.append(sp.simplify(dot(wave, basis)))
            helical_residuals.append(
                sp.simplify(I * cross(wave, basis) - sign * length * basis)
            )
    assert all(value == 0 for value in divergence_residuals)
    assert all(value == sp.zeros(3, 1) for value in helical_residuals)

    expected_derivative = sp.Matrix(
        [
            [sp.Rational(9, 2), -16, sp.Rational(25, 2)],
            [sp.Rational(27, 4), sp.Rational(-32, 3), sp.Rational(-25, 12)],
            [sp.Rational(-27, 2), sp.Rational(16, 3), sp.Rational(175, 6)],
            [sp.Rational(9, 4), -32, sp.Rational(175, 4)],
        ]
    )
    expected_target = sp.Matrix(
        [
            [10, -15, 6],
            [-15, 10, -1],
            [30, 5, -14],
            [5, 30, -21],
        ]
    )
    assert derivative == expected_derivative
    assert target == expected_target
    assert derivative.rank() == 2

    energy_gauge = sp.Matrix(
        [sp.Rational(1, 9), sp.Rational(1, 16), sp.Rational(1, 25)]
    )
    constant_weight = sp.ones(3, 1)
    squared_lengths = sp.Matrix([9, 16, 25])
    assert derivative * energy_gauge == sp.zeros(4, 1)
    assert derivative * constant_weight == target * constant_weight
    assert target * squared_lengths == sp.zeros(4, 1)

    left_null_vectors = [
        sp.Matrix([sp.Rational(-9, 5), sp.Rational(16, 5), 1, 0]),
        sp.Matrix([sp.Rational(-16, 5), sp.Rational(9, 5), 0, 1]),
    ]
    for vector in left_null_vectors:
        assert (vector.T * derivative) == sp.zeros(1, 3)

    target_obstructions = [sp.simplify(vector.T * target) for vector in left_null_vectors]
    necessary_vector = sp.Matrix([[-9, 16, -7]])
    assert target_obstructions[0] == 4 * necessary_vector
    assert target_obstructions[1] == 6 * necessary_vector

    quadratic_combination = 16 * 4**2 - 9 * 3**2 - 7 * 5**2
    quartic_combination = 16 * 4**4 - 9 * 3**4 - 7 * 5**4
    leading_i4_coefficient = sp.Rational(-quartic_combination, 70)
    assert quadratic_combination == 0
    assert quartic_combination == -1008
    assert leading_i4_coefficient == sp.Rational(72, 5)

    return {
        "release": "R0.70B",
        "status": "exact-symbolic-audit",
        "scope": (
            "finite-dimensional 3:4:5 helical symbol arithmetic; "
            "wave-packet and O(3)-averaging arguments remain analytic"
        ),
        "waveNumberLengths": [3, 4, 5],
        "triad": [[3, 0, 0], [0, 4, 0], [-3, -4, 0]],
        "lengthSquared": [9, 16, 25],
        "closure": [0, 0, 0],
        "singleOrientedTriadCommonFactorRemoved": "sqrt(2)/50",
        "realSixModeCommonFactor": "sqrt(2)/25",
        "helicalSignRows": [list(row) for row in sign_rows],
        "derivativeMatrix": [
            [rational_string(value) for value in derivative.row(index)]
            for index in range(derivative.rows)
        ],
        "targetMatrix": [
            [rational_string(value) for value in target.row(index)]
            for index in range(target.rows)
        ],
        "leftNullVectors": [
            [rational_string(value) for value in vector]
            for vector in left_null_vectors
        ],
        "targetObstructionRows": [
            [rational_string(value) for value in row]
            for row in target_obstructions
        ],
        "necessaryCondition": "16*g4 - 9*g3 - 7*g5 = 0",
        "rankDerivativeMatrix": derivative.rank(),
        "energyGauge": [rational_string(value) for value in energy_gauge],
        "derivativeTimesEnergyGauge": [
            rational_string(value) for value in derivative * energy_gauge
        ],
        "constantWeightCheck": [
            rational_string(value)
            for value in derivative * constant_weight - target * constant_weight
        ],
        "squaredLengthTargetNullCheck": [
            rational_string(value) for value in target * squared_lengths
        ],
        "smallFrequencyExpansion": {
            "j2Coefficients": ["1/15", "-1/210", "1/7560"],
            "GCoefficients": ["1/5", "-1/70", "1/2520"],
            "G(s)": "(I2/5)*s^2 - (I4/70)*s^4 + O(s^6)",
            "quadraticCombination": quadratic_combination,
            "quarticCombination": quartic_combination,
            "leadingI4Coefficient": rational_string(leading_i4_coefficient),
            "strictnessCondition": "I4 > 0",
            "I4Identity": "(Lambda^4 - 1) * integral_0^infinity chi(x)*x^3 dx",
        },
        "checks": {
            "allPolarizationsDivergenceFree": True,
            "allHelicalEigenrelationsExact": True,
            "derivedDerivativeMatrixMatchesLockedTable": True,
            "derivedTargetMatrixMatchesLockedTable": True,
            "derivativeRankIsTwo": True,
            "energyGaugeVerified": True,
            "constantWeightEnstrophyCheck": True,
            "squaredLengthTargetNullCheck": True,
            "twoLeftNullVectorsVerified": True,
            "necessaryConditionVerified": True,
            "quadraticTermCancels": True,
            "quarticTermIsPositiveAfterBesselCoefficient": True,
            "floatCount": 0,
        },
        "claimBoundary": (
            "This audit does not prove Navier-Stokes regularity, does not "
            "exclude normal forms with same-order remainders, and does not "
            "cover non-translation-invariant or nonquadratic constructions."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    result = audit()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if arguments.output is None:
        print(rendered, end="")
    else:
        arguments.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
