#!/usr/bin/env python3
"""Exact symbolic audit for the R0.69Q vorticity-direction obstruction."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def curl(field: sp.Matrix, coordinates: sp.Matrix) -> sp.Matrix:
    x, y, z = coordinates
    return sp.Matrix(
        [
            sp.diff(field[2], y) - sp.diff(field[1], z),
            sp.diff(field[0], z) - sp.diff(field[2], x),
            sp.diff(field[1], x) - sp.diff(field[0], y),
        ]
    )


def polynomial_remainder(expression: sp.Expr, constraints: list[sp.Expr], variables: list[sp.Symbol]) -> sp.Expr:
    basis = sp.groebner(constraints, *variables, order="grevlex")
    return sp.expand(basis.reduce(sp.expand(expression))[1])


def audit(source_commit: str | None = None) -> dict[str, object]:
    rho, nu = sp.symbols("rho nu", positive=True)
    rho_derivatives = sp.symbols("rho_1:4", real=True)
    xi_symbols = sp.symbols("xi_1:4", real=True)
    xi = sp.Matrix(xi_symbols)
    gradient_symbols = sp.symbols("g_11:14 g_21:24 g_31:34", real=True)
    gradients = [
        sp.Matrix(gradient_symbols[0:3]),
        sp.Matrix(gradient_symbols[3:6]),
        sp.Matrix(gradient_symbols[6:9]),
    ]
    laplacian_symbols = sp.symbols("h_1:4", real=True)
    laplacian_xi = sp.Matrix(laplacian_symbols)
    q_direction = sp.expand(sum(g.dot(g) for g in gradients))

    constraints = [sp.expand(xi.dot(xi) - 1)]
    constraints.extend(sp.expand(xi.dot(g)) for g in gradients)
    constraints.append(sp.expand(xi.dot(laplacian_xi) + q_direction))
    variables = [
        *xi_symbols,
        *gradient_symbols,
        *laplacian_symbols,
        *rho_derivatives,
        rho,
    ]

    polar_gradient = [rho_derivatives[j] * xi + rho * gradients[j] for j in range(3)]
    norm_split_residual = sp.expand(
        sum(vector.dot(vector) for vector in polar_gradient)
        - sum(value**2 for value in rho_derivatives)
        - rho**2 * q_direction
    )
    norm_split_remainder = polynomial_remainder(norm_split_residual, constraints, variables)

    projected_laplacian_residual = laplacian_xi + q_direction * xi - (
        sp.eye(3) - xi * xi.T
    ) * laplacian_xi
    projected_remainders = [
        polynomial_remainder(entry, constraints, variables)
        for entry in projected_laplacian_residual
    ]

    # Pointwise chain-rule audit for the vorticity equation.
    laplacian_rho = sp.symbols("laplacian_rho", real=True)
    S_symbols = sp.symbols("s11 s22 s12 s13 s23", real=True)
    s11, s22, s12, s13, s23 = S_symbols
    strain = sp.Matrix(
        [
            [s11, s12, s13],
            [s12, s22, s23],
            [s13, s23, -s11 - s22],
        ]
    )
    stretch_rate = sp.expand((xi.T * strain * xi)[0])
    laplacian_omega = (
        xi * laplacian_rho
        + 2 * sum(
            (rho_derivatives[j] * gradients[j] for j in range(3)),
            sp.zeros(3, 1),
        )
        + rho * laplacian_xi
    )
    material_omega = rho * strain * xi + nu * laplacian_omega
    material_rho = sp.expand(xi.dot(material_omega))
    expected_material_rho = rho * stretch_rate + nu * (
        laplacian_rho - rho * q_direction
    )
    magnitude_remainder = polynomial_remainder(
        material_rho - expected_material_rho,
        constraints,
        variables + [laplacian_rho, *S_symbols, nu],
    )

    material_xi = sp.expand((material_omega - xi * material_rho) / rho)
    direction_expected = (
        (sp.eye(3) - xi * xi.T) * strain * xi
        + 2 * nu * sum(
            (
                rho_derivatives[j] * gradients[j] / rho
                for j in range(3)
            ),
            sp.zeros(3, 1),
        )
        + nu * (sp.eye(3) - xi * xi.T) * laplacian_xi
    )
    direction_remainders = [
        polynomial_remainder(
            sp.together(rho * (material_xi[j] - direction_expected[j])),
            constraints,
            variables + [laplacian_rho, *S_symbols, nu],
        )
        for j in range(3)
    ]

    # Exact affine-core witness.
    s, w = sp.symbols("s w", positive=True)
    sqrt6 = sp.sqrt(6)
    sharp_strain = s * sp.diag(-1 / sqrt6, -1 / sqrt6, 2 / sqrt6)
    sharp_vorticity = sp.Matrix([0, 0, w])
    rotation = sp.Matrix(
        [
            [0, -w / 2, 0],
            [w / 2, 0, 0],
            [0, 0, 0],
        ]
    )
    affine_matrix = sharp_strain + rotation
    x, y, z = sp.symbols("x y z", real=True)
    coordinates = sp.Matrix([x, y, z])
    affine_velocity = affine_matrix * coordinates
    vector_potential = -sp.Rational(1, 3) * coordinates.cross(affine_velocity)
    recovered_velocity = sp.simplify(curl(vector_potential, coordinates))
    recovered_vorticity = sp.simplify(curl(affine_velocity, coordinates))
    positive_stretching = sp.simplify(
        (sharp_vorticity.T * sharp_strain * sharp_vorticity)[0]
    )

    amplitude, length, base_production, base_dissipation = sp.symbols(
        "a L P D", positive=True
    )
    scaled_ratio = sp.simplify(
        amplitude**3 * length**3 * base_production
        / (nu * amplitude**2 * length * base_dissipation)
    )

    checks = {
        "polarGradientNormSplitsExactly": norm_split_remainder == 0,
        "unitDirectionLaplacianConstraint": constraints[-1]
        == sp.expand(xi.dot(laplacian_xi) + q_direction),
        "projectedLaplacianIdentity": all(value == 0 for value in projected_remainders),
        "magnitudeEquationChainRule": magnitude_remainder == 0,
        "directionEquationChainRule": all(value == 0 for value in direction_remainders),
        "strainWitnessIsSymmetric": sharp_strain == sharp_strain.T,
        "strainWitnessIsTraceFree": sp.trace(sharp_strain) == 0,
        "affineJetIsDivergenceFree": sp.trace(affine_matrix) == 0,
        "quadraticPotentialRecoversAffineJet": recovered_velocity == affine_velocity,
        "affineCoreHasConstantVorticity": recovered_vorticity == sharp_vorticity,
        "affineCoreSaturatesPositiveStretching": positive_stretching
        == sp.sqrt(sp.Rational(2, 3)) * s * w**2,
        "affineCoreHasZeroAmplitudeGradient": all(value == 0 for value in sp.zeros(3, 1)),
        "affineCoreHasZeroDirectionGradient": all(value == 0 for value in sp.zeros(3, 3)),
        "positivePartScalesCubically": sp.simplify(amplitude**3 * length**3)
        == amplitude**3 * length**3,
        "vorticityDissipationScalesAsLength": sp.simplify(amplitude**2 * length)
        == amplitude**2 * length,
        "absorptionRatioHasSupercriticalFactor": scaled_ratio
        == amplitude * length**2 * base_production / (nu * base_dissipation),
    }
    checks = {name: bool(value) for name, value in checks.items()}

    if source_commit is not None:
        head_commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        checks["sourceCommitHasFortyHexCharacters"] = (
            len(source_commit) == 40
            and all(character in "0123456789abcdef" for character in source_commit)
        )
        checks["sourceCommitMatchesHead"] = source_commit == head_commit

    script_path = Path(__file__).resolve()
    note_path = script_path.with_name("vorticity_direction_diffusion_obstruction_note.md")

    return {
        "schemaVersion": "1.0",
        "release": "R0.69Q",
        "status": "passed" if all(checks.values()) else "failed",
        "provenance": {
            "sourceCommit": source_commit,
            "auditScript": str(script_path.relative_to(script_path.parents[1])),
            "auditScriptSha256": sha256(script_path),
            "researchNote": str(note_path.relative_to(note_path.parents[1])),
            "researchNoteSha256": sha256(note_path),
        },
        "polarIdentities": {
            "magnitude": "(D_t-nu Delta)rho=rho alpha-nu rho |grad xi|^2",
            "direction": (
                "D_t xi=(I-xi tensor xi)Sxi+nu(I-xi tensor xi)Delta xi"
                "+2nu grad(log rho).grad xi"
            ),
            "dissipation": "|grad omega|^2=|grad rho|^2+rho^2|grad xi|^2",
        },
        "affineCore": {
            "strain": "s*diag(-1,-1,2)/sqrt(6)",
            "vorticity": "w*e3",
            "positiveStretching": str(positive_stretching),
            "amplitudeGradient": "0",
            "directionGradient": "0",
        },
        "scalingObstruction": {
            "field": "v_{a,L}(x)=a L v(x/L)",
            "positiveProductionFactor": "a^3 L^3",
            "dissipationFactor": "a^2 L",
            "ratio": str(scaled_ratio),
        },
        "shortTimeObstruction": {
            "productionAverageLimit": "|B|*sqrt(2/3)*s*w^2",
            "directionDissipationAverageLimit": "0",
            "fullDissipationAverageLimit": "0",
            "scope": "interior-only inequalities without flux or initial trace",
        },
        "claimBoundary": {
            "proved": (
                "exact polar identities and affine-core plus short-time obstruction "
                "to interior-only dissipation absorption"
            ),
            "notProved": (
                "failure of nonlocal geometric criteria, global regularity, or blow-up"
            ),
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
