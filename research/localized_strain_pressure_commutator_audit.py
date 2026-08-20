#!/usr/bin/env python3
"""Exact Fourier audit for the R0.69I localized strain identities."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


Mode = tuple[int, int, int]
Field = dict[Mode, sp.Expr]
ZERO: Mode = (0, 0, 0)
I = sp.I


def clean(field: Field) -> Field:
    output: Field = {}
    for mode, value in field.items():
        simplified = sp.simplify(value)
        if simplified != 0:
            output[mode] = simplified
    return output


def add(*fields: Field) -> Field:
    output: Field = {}
    for field in fields:
        for mode, value in field.items():
            output[mode] = output.get(mode, sp.S.Zero) + value
    return clean(output)


def scale(field: Field, factor: sp.Expr) -> Field:
    return clean({mode: factor * value for mode, value in field.items()})


def multiply(left: Field, right: Field) -> Field:
    output: Field = {}
    for first, first_value in left.items():
        for second, second_value in right.items():
            mode = tuple(first[index] + second[index] for index in range(3))
            output[mode] = output.get(mode, sp.S.Zero) + first_value * second_value
    return clean(output)


def derivative(field: Field, axis: int) -> Field:
    return clean({mode: I * mode[axis] * value for mode, value in field.items()})


def mean(field: Field) -> sp.Expr:
    return sp.simplify(field.get(ZERO, sp.S.Zero))


def dot(left: list[Field], right: list[Field]) -> Field:
    return add(*(multiply(left[index], right[index]) for index in range(3)))


def matrix_product(left: list[list[Field]], right: list[list[Field]]) -> list[list[Field]]:
    return [
        [
            add(*(multiply(left[row][inner], right[inner][column]) for inner in range(3)))
            for column in range(3)
        ]
        for row in range(3)
    ]


def matrix_vector(matrix: list[list[Field]], vector: list[Field]) -> list[Field]:
    return [
        add(*(multiply(matrix[row][column], vector[column]) for column in range(3)))
        for row in range(3)
    ]


def matrix_inner(left: list[list[Field]], right: list[list[Field]]) -> Field:
    return add(
        *(multiply(left[row][column], right[row][column]) for row in range(3) for column in range(3))
    )


def trace(matrix: list[list[Field]]) -> Field:
    return add(*(matrix[index][index] for index in range(3)))


def determinant(matrix: list[list[Field]]) -> Field:
    positive = add(
        multiply(multiply(matrix[0][0], matrix[1][1]), matrix[2][2]),
        multiply(multiply(matrix[0][1], matrix[1][2]), matrix[2][0]),
        multiply(multiply(matrix[0][2], matrix[1][0]), matrix[2][1]),
    )
    negative = add(
        multiply(multiply(matrix[0][2], matrix[1][1]), matrix[2][0]),
        multiply(multiply(matrix[0][1], matrix[1][0]), matrix[2][2]),
        multiply(multiply(matrix[0][0], matrix[1][2]), matrix[2][1]),
    )
    return add(positive, scale(negative, -1))


def matched_weight_mode(field: Field, mode: Mode, amplitude: sp.Rational) -> Field:
    opposite = tuple(-entry for entry in mode)
    coefficient = sp.simplify(field[mode])
    real_part = sp.simplify(sp.re(coefficient))
    imaginary_part = sp.simplify(sp.im(coefficient))
    if real_part != 0:
        phase = sp.sign(real_part)
    elif imaginary_part != 0:
        phase = I * sp.sign(imaginary_part)
    else:
        raise RuntimeError("active mode has a zero coefficient")
    return {mode: amplitude * phase / 2, opposite: amplitude * sp.conjugate(phase) / 2}


def rational_text(value: sp.Expr) -> str:
    return str(sp.factor(sp.simplify(value)))


def build_velocity() -> list[Field]:
    carriers = (
        ((1, 1, 0), (1, -1, 2), sp.Rational(1, 1)),
        ((1, 0, 1), (2, 1, -2), sp.Rational(2, 3)),
        ((0, 1, 1), (1, 2, -2), sp.Rational(3, 5)),
        ((1, -1, 1), (1, 2, 1), sp.Rational(4, 7)),
    )
    velocity: list[Field] = [{}, {}, {}]
    for mode, amplitude, weight in carriers:
        assert sum(mode[index] * amplitude[index] for index in range(3)) == 0
        opposite = tuple(-entry for entry in mode)
        for component in range(3):
            coefficient = weight * sp.Rational(amplitude[component], 2)
            velocity[component][mode] = coefficient
            velocity[component][opposite] = coefficient
    return [clean(component) for component in velocity]


def choose_active_mode(field: Field, excluded: set[Mode] | None = None) -> Mode:
    excluded = excluded or set()
    candidates = [
        mode
        for mode, value in field.items()
        if mode != ZERO
        and mode not in excluded
        and value != 0
        and next((entry for entry in mode if entry), 1) > 0
    ]
    if not candidates:
        raise RuntimeError("no nonzero active Fourier mode")
    return min(candidates, key=lambda mode: (sum(abs(entry) for entry in mode), mode))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(source_commit: str | None = None) -> dict[str, object]:
    velocity = build_velocity()
    gradient = [[derivative(velocity[row], column) for column in range(3)] for row in range(3)]
    divergence = trace(gradient)
    strain = [
        [scale(add(gradient[row][column], gradient[column][row]), sp.Rational(1, 2)) for column in range(3)]
        for row in range(3)
    ]

    curl = [
        add(derivative(velocity[2], 1), scale(derivative(velocity[1], 2), -1)),
        add(derivative(velocity[0], 2), scale(derivative(velocity[2], 0), -1)),
        add(derivative(velocity[1], 0), scale(derivative(velocity[0], 1), -1)),
    ]
    gradient_squared = matrix_product(gradient, gradient)
    q = trace(gradient_squared)
    pressure: Field = {}
    for mode, value in q.items():
        if mode == ZERO:
            continue
        norm_squared = sum(entry * entry for entry in mode)
        pressure[mode] = sp.simplify(value / norm_squared)
    pressure = clean(pressure)
    hessian = [[derivative(derivative(pressure, row), column) for column in range(3)] for row in range(3)]

    pressure_density = matrix_inner(strain, hessian)
    gradient_cubed = matrix_product(gradient_squared, gradient)
    betchov_density = trace(gradient_cubed)

    pressure_mode = choose_active_mode(pressure_density)
    betchov_mode = choose_active_mode(
        betchov_density,
        {pressure_mode, tuple(-entry for entry in pressure_mode)},
    )
    phi = add(
        {ZERO: sp.S.One},
        matched_weight_mode(pressure_density, pressure_mode, sp.Rational(1, 7)),
        matched_weight_mode(betchov_density, betchov_mode, sp.Rational(1, 11)),
    )
    grad_phi = [derivative(phi, axis) for axis in range(3)]
    hess_phi = [[derivative(derivative(phi, row), column) for column in range(3)] for row in range(3)]

    laplacian_pressure = add(*(derivative(derivative(pressure, axis), axis) for axis in range(3)))
    gradient_pressure = [derivative(pressure, axis) for axis in range(3)]

    pressure_left = mean(multiply(phi, pressure_density))
    pressure_right_first = mean(multiply(laplacian_pressure, dot(velocity, grad_phi)))
    pressure_right_second = mean(
        add(
            *(
                multiply(multiply(velocity[row], gradient_pressure[column]), hess_phi[row][column])
                for row in range(3)
                for column in range(3)
            )
        )
    )
    pressure_right = sp.simplify(pressure_right_first + pressure_right_second)

    a_squared_u = matrix_vector(gradient_squared, velocity)
    betchov_flux = [
        add(scale(multiply(q, velocity[index]), sp.Rational(1, 2)), scale(a_squared_u[index], -1))
        for index in range(3)
    ]
    betchov_left = mean(multiply(phi, betchov_density))
    betchov_right = mean(dot(betchov_flux, grad_phi))

    strain_cubed = matrix_product(matrix_product(strain, strain), strain)
    tr_strain_cubed = trace(strain_cubed)
    omega_strain_omega = dot(curl, matrix_vector(strain, curl))
    nonlinear_density = add(tr_strain_cubed, scale(omega_strain_omega, sp.Rational(1, 4)))
    localized_reduction = add(
        scale(determinant(strain), 2),
        scale(betchov_density, sp.Rational(1, 3)),
    )
    nonlinear_difference = add(nonlinear_density, scale(localized_reduction, -1))

    global_pressure = mean(pressure_density)
    global_betchov = mean(betchov_density)
    poisson_residual = add(laplacian_pressure, q)

    scaling_terms = {
        "phi_S_H": 0 + 2 + 4 - 3,
        "laplacianP_u_gradPhi": 4 + 1 + 1 - 3,
        "u_gradP_hessPhi": 1 + 3 + 2 - 3,
        "phi_trA3": 0 + 6 - 3,
        "q_u_gradPhi": 4 + 1 + 1 - 3,
        "A2_u_gradPhi": 4 + 1 + 1 - 3,
    }

    checks = {
        "velocityIsExactlyDivergenceFree": not divergence,
        "pressureSourceHasZeroMean": mean(q) == 0,
        "poissonEquationHoldsModeByMode": not poisson_residual,
        "globalPressureOrthogonalityHolds": global_pressure == 0,
        "localizedPressureCommutatorIsExact": sp.simplify(pressure_left - pressure_right) == 0,
        "localizedPressureCommutatorIsNonzero": pressure_left != 0,
        "globalBetchovCancellationHolds": global_betchov == 0,
        "localizedBetchovFluxIsExact": sp.simplify(betchov_left - betchov_right) == 0,
        "localizedBetchovFluxIsNonzero": betchov_left != 0,
        "localizedCubicReductionIsPointwiseExact": not nonlinear_difference,
        "allLocalizedTermsHaveScalingDegreeThree": set(scaling_terms.values()) == {3},
        "weightUsesTwoNonconstantModes": pressure_mode != ZERO and betchov_mode != ZERO,
    }
    if source_commit is not None:
        head_commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        checks["sourceCommitHasFortyHexCharacters"] = (
            len(source_commit) == 40 and all(character in "0123456789abcdef" for character in source_commit)
        )
        checks["sourceCommitMatchesHead"] = source_commit == head_commit

    script_path = Path(__file__).resolve()
    note_path = script_path.with_name("localized_strain_pressure_commutator_note.md")

    return {
        "schemaVersion": "1.0",
        "release": "R0.69I",
        "status": "passed" if all(checks.values()) else "failed",
        "domain": "T^3 with period 2*pi",
        "normalization": "Fourier zero coefficient equals spatial mean",
        "weight": {
            "pressureMode": list(pressure_mode),
            "pressureAmplitude": "1/7",
            "pressureDensityCoefficient": rational_text(pressure_density[pressure_mode]),
            "betchovMode": list(betchov_mode),
            "betchovAmplitude": "1/11",
            "betchovDensityCoefficient": rational_text(betchov_density[betchov_mode]),
        },
        "exactValues": {
            "localizedPressurePairing": rational_text(pressure_left),
            "pressureLaplacianFlux": rational_text(pressure_right_first),
            "pressureGradientFlux": rational_text(pressure_right_second),
            "localizedBetchovPairing": rational_text(betchov_left),
            "globalPressurePairing": rational_text(global_pressure),
            "globalBetchovPairing": rational_text(global_betchov),
        },
        "scalingDegrees": scaling_terms,
        "support": {
            "velocityModes": sum(len(component) for component in velocity),
            "pressureSourceModes": len(q),
            "pressureHessianModes": sum(len(hessian[row][column]) for row in range(3) for column in range(3)),
        },
        "provenance": {
            "sourceCommit": source_commit,
            "auditScript": str(script_path.relative_to(script_path.parents[1])),
            "auditScriptSha256": sha256(script_path),
            "researchNote": str(note_path.relative_to(note_path.parents[1])),
            "researchNoteSha256": sha256(note_path),
        },
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--source-commit")
    args = parser.parse_args()
    result = audit(args.source_commit)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if result["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
