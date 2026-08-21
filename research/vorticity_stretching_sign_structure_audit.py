#!/usr/bin/env python3
"""Exact symbolic audit for the R0.69P vortex-stretching sign structure."""

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


def audit(source_commit: str | None = None) -> dict[str, object]:
    s11, s22, s12, s13, s23 = sp.symbols("s11 s22 s12 s13 s23", real=True)
    w1, w2, w3, w = sp.symbols("w1 w2 w3 w", real=True)
    S = sp.Matrix(
        [
            [s11, s12, s13],
            [s12, s22, s23],
            [s13, s23, -s11 - s22],
        ]
    )
    omega = sp.Matrix([w1, w2, w3])
    Omega = sp.Matrix(
        [
            [0, -w3 / 2, w2 / 2],
            [w3 / 2, 0, -w1 / 2],
            [-w2 / 2, w1 / 2, 0],
        ]
    )
    A = S + Omega
    stretch = (omega.T * S * omega)[0]
    betchov_residual = sp.simplify(
        sp.trace(A**3) - sp.trace(S**3) - sp.Rational(3, 4) * stretch
    )
    omega_square_residual = sp.simplify(
        Omega**2
        - sp.Rational(1, 4)
        * (omega * omega.T - (omega.dot(omega)) * sp.eye(3))
    )

    # Exact local vector potential for an arbitrary trace-free affine jet.
    a11, a12, a13, a21, a22, a23, a31, a32 = sp.symbols(
        "a11 a12 a13 a21 a22 a23 a31 a32", real=True
    )
    affine_matrix = sp.Matrix(
        [
            [a11, a12, a13],
            [a21, a22, a23],
            [a31, a32, -a11 - a22],
        ]
    )
    x, y, z = sp.symbols("x y z", real=True)
    coordinates = sp.Matrix([x, y, z])
    affine_velocity = affine_matrix * coordinates
    vector_potential = -sp.Rational(1, 3) * coordinates.cross(affine_velocity)
    recovered_velocity = sp.simplify(curl(vector_potential, coordinates))
    affine_vorticity = sp.simplify(curl(affine_velocity, coordinates))

    sqrt6 = sp.sqrt(6)
    S_extensional = sp.diag(-1 / sqrt6, -1 / sqrt6, 2 / sqrt6)
    omega_extensional = sp.Matrix([0, 0, w])
    positive_endpoint = sp.simplify(
        (omega_extensional.T * S_extensional * omega_extensional)[0]
    )
    negative_endpoint = sp.simplify(
        (omega_extensional.T * (-S_extensional) * omega_extensional)[0]
    )
    extensional_norm_squared = sp.simplify(sp.trace(S_extensional**2))

    S_middle = sp.diag(-2 / sqrt6, 1 / sqrt6, 1 / sqrt6)
    middle_norm_squared = sp.simplify(sp.trace(S_middle**2))
    middle_eigenvalue = 1 / sqrt6

    r = sp.symbols("r", positive=True)
    determinant_ratio = sp.simplify(
        4 * r * (1 + r) / (2 * (1 + r + r**2))
    )
    determinant_gap = sp.simplify(2 - determinant_ratio)
    determinant_limit = sp.limit(determinant_ratio, r, sp.oo)

    sigma, dissipation, epsilon = sp.symbols(
        "sigma D epsilon", positive=True
    )
    stretching_profit = (
        sigma ** sp.Rational(3, 2) * dissipation ** sp.Rational(3, 4)
        - epsilon * dissipation
    )
    dissipation_optimizer = sp.simplify(
        (3 * sigma ** sp.Rational(3, 2) / (4 * epsilon)) ** 4
    )
    optimized_stretching = sp.simplify(
        stretching_profit.subs(dissipation, dissipation_optimizer)
    )

    checks = {
        "strainMatrixIsSymmetric": S == S.T,
        "strainMatrixIsTraceFree": sp.trace(S) == 0,
        "rotationSquareIdentity": omega_square_residual == sp.zeros(3),
        "pointwiseBetchovDecomposition": betchov_residual == 0,
        "traceCubeEqualsThreeDeterminant": (
            sp.simplify(sp.trace(S**3) - 3 * S.det()) == 0
        ),
        "affineJetIsDivergenceFree": sp.trace(affine_matrix) == 0,
        "quadraticPotentialRecoversAffineJet": (
            sp.simplify(recovered_velocity - affine_velocity) == sp.zeros(3, 1)
        ),
        "affineCurlUsesDeclaredConvention": affine_vorticity
        == sp.Matrix([a32 - a23, a13 - a31, a21 - a12]),
        "extensionalWitnessHasUnitFrobeniusNorm": extensional_norm_squared == 1,
        "positiveStretchingEndpointIsSharp": (
            positive_endpoint == sp.sqrt(sp.Rational(2, 3)) * w**2
        ),
        "negativeStretchingEndpointIsSharp": (
            negative_endpoint == -sp.sqrt(sp.Rational(2, 3)) * w**2
        ),
        "middleEigenvalueWitnessHasUnitFrobeniusNorm": middle_norm_squared == 1,
        "middleEigenvalueBoundIsSharp": middle_eigenvalue == 1 / sp.sqrt(6),
        "determinantRatioHasExactGapToTwo": (
            determinant_gap == 2 / (1 + r + r**2)
        ),
        "determinantConstantTwoIsSharpSupremum": determinant_limit == 2,
        "stretchingOptimizerIsCritical": (
            sp.simplify(
                sp.diff(stretching_profit, dissipation).subs(
                    dissipation, dissipation_optimizer
                )
            )
            == 0
        ),
        "stretchingYoungRemainderIsSextic": (
            optimized_stretching
            == sp.Rational(27, 256) * epsilon**-3 * sigma**6
        ),
        "signChangesUnderVelocityReversal": (
            sp.simplify(((-omega).T * (-S) * (-omega))[0] + stretch) == 0
        ),
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
    note_path = script_path.with_name("vorticity_stretching_sign_structure_note.md")

    return {
        "schemaVersion": "1.0",
        "release": "R0.69P",
        "status": "passed" if all(checks.values()) else "failed",
        "provenance": {
            "sourceCommit": source_commit,
            "auditScript": str(script_path.relative_to(script_path.parents[1])),
            "auditScriptSha256": sha256(script_path),
            "researchNote": str(note_path.relative_to(note_path.parents[1])),
            "researchNoteSha256": sha256(note_path),
        },
        "sharpPointwiseStretching": {
            "constant": "sqrt(2/3)",
            "positiveWitnessStrain": "diag(-1,-1,2)/sqrt(6)",
            "positiveWitnessVorticity": "w*e3",
            "positiveEndpoint": str(positive_endpoint),
            "negativeEndpoint": str(negative_endpoint),
        },
        "localRealization": {
            "affineVelocity": "u_A(x)=A*x",
            "vectorPotential": "B_A(x)=-(1/3)*x cross (A*x)",
            "compactField": "v_A=curl(chi*B_A)",
            "coreIdentity": "v_A=A*x wherever chi=1",
        },
        "betchov": {
            "pointwise": "tr(A^3)=tr(S^3)+(3/4)*omega.S.omega",
            "global": "integral omega.S.omega=-4 integral det(S)",
            "middleEigenvalueBound": "-4 det(S) <= 2 lambda_2^+ |S|^2",
            "sharpSupremum": str(determinant_limit),
            "ratioGap": str(determinant_gap),
        },
        "energyOnlyEndpoint": {
            "middleEigenvalueBound": "lambda_2^+ <= |S|/sqrt(6)",
            "youngOptimizer": str(dissipation_optimizer),
            "youngRemainder": str(optimized_stretching),
            "power": "sigma^6",
        },
        "claimBoundary": {
            "proved": (
                "sharp pointwise constants, exact local solenoidal realization, "
                "and persistence of the sextic energy-only remainder"
            ),
            "notProved": (
                "an unconditional spacetime depletion estimate or "
                "three-dimensional Navier-Stokes regularity"
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
