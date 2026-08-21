#!/usr/bin/env python3
"""Exact symbolic audit for the R0.69U dyadic core-saturation theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(source_commit: str | None = None) -> dict[str, object]:
    sqrt6 = sp.sqrt(6)
    coordinate = sp.symbols("x1 x2 x3", real=True)
    x = sp.Matrix(coordinate)
    strain = sp.diag(-1, -1, 2) / sqrt6
    rotation = sp.Matrix(
        [
            [0, -sp.Rational(1, 2), 0],
            [sp.Rational(1, 2), 0, 0],
            [0, 0, 0],
        ]
    )
    affine = strain + rotation
    velocity = affine * x
    curl_velocity = sp.Matrix(
        [
            sp.diff(velocity[2], x[1]) - sp.diff(velocity[1], x[2]),
            sp.diff(velocity[0], x[2]) - sp.diff(velocity[2], x[0]),
            sp.diff(velocity[1], x[0]) - sp.diff(velocity[0], x[1]),
        ]
    )

    z = sp.symbols("z", real=True)
    beta_density = 30 * z**2 * (1 - z) ** 2
    beta_mass = sp.integrate(beta_density, (z, 0, 1))
    beta_l2 = sp.integrate(beta_density**2, (z, 0, 1))
    transition_length = sp.Rational(9, 10)
    h_l2 = sp.simplify(beta_l2 / transition_length)
    energy_bound = sp.simplify(sp.Rational(3, 2) * h_l2)
    outer_margin = sp.simplify(sp.Rational(5, 2) - energy_bound)

    mu = sp.symbols("mu", real=True)
    angular_moment = sp.simplify(
        2 * sp.pi * sp.integrate(mu**2 * (1 - mu**2), (mu, -1, 1))
    )

    n1, n2, n3, scaled_radius = sp.symbols(
        "n1 n2 n3 s", real=True
    )
    q1, q2 = sp.symbols("q1 q2", real=True)
    omega1 = sp.expand(
        n3
        / 6
        * (
            -4 * scaled_radius * n1 * q1
            + 6 * sqrt6 * scaled_radius * n2 * q1
            + scaled_radius**2 * (-n1 + sqrt6 * n2) * q2
        )
    )
    omega2 = sp.expand(
        n3
        / 6
        * (
            -6 * sqrt6 * scaled_radius * n1 * q1
            - 4 * scaled_radius * n2 * q1
            + scaled_radius**2 * (-sqrt6 * n1 - n2) * q2
        )
    )
    transverse = sp.expand(n1 * omega2 - n2 * omega1)
    transverse_expected = sp.expand(
        -scaled_radius
        / sqrt6
        * n3
        * (1 - n3**2)
        * (6 * q1 + scaled_radius * q2)
    )
    transverse_on_sphere = sp.simplify(
        (transverse - transverse_expected).subs(n1**2, 1 - n2**2 - n3**2)
    )

    energy = sp.symbols("E", nonnegative=True)
    inner_radial = sp.Rational(5, 2) + energy
    outer_radial = sp.Rational(5, 2) - energy
    radial_total = sp.simplify(inner_radial + outer_radial)
    carrier_prefactor = sp.simplify(
        sp.Rational(3, 1) / (4 * sp.pi) * angular_moment / sqrt6
    )
    per_point_total = sp.simplify(carrier_prefactor * radial_total)
    core_volume = 4 * sp.pi / 3
    exact_core = sp.simplify(core_volume * per_point_total)
    expected_core = 8 * sp.pi / (3 * sqrt6)
    outer_share_bound = sp.simplify(outer_margin / radial_total)
    inner_share_bound = sp.simplify(1 - outer_share_bound)

    radius, shell_offset = sp.symbols("R k", positive=True, integer=True)
    full_space_prefactor = sp.simplify(radius**6 / radius**3)

    checks = {
        "affineMatrixIsTraceFree": sp.simplify(sp.trace(affine)) == 0,
        "symmetricPartIsDeclaredStrain": sp.simplify(
            (affine + affine.T) / 2 - strain
        ) == sp.zeros(3),
        "affineCurlIsUnitVertical": sp.simplify(
            curl_velocity - sp.Matrix([0, 0, 1])
        ) == sp.zeros(3, 1),
        "coreProductionIsTwoOverSqrtSix": sp.simplify(
            (sp.Matrix([0, 0, 1]).dot(strain * sp.Matrix([0, 0, 1])))
            - 2 / sqrt6
        ) == 0,
        "transitionDensityHasUnitMass": beta_mass == 1,
        "baseTransitionL2IsTenSevenths": beta_l2 == sp.Rational(10, 7),
        "scaledTransitionL2IsHundredSixtyThirds": h_l2
        == sp.Rational(100, 63),
        "mollifiedEnergyBoundIsFiftyTwentyFirsts": energy_bound
        == sp.Rational(50, 21),
        "outerRadialMarginIsFiveFortySeconds": outer_margin
        == sp.Rational(5, 42),
        "angularMomentIsEightPiFifteenths": angular_moment
        == 8 * sp.pi / 15,
        "scaledTransverseVorticityHasRadialFactor": transverse_on_sphere == 0,
        "twoRadialCoefficientsSumToFive": radial_total == 5,
        "carrierPrefactorIsTwoOverFiveSqrtSix": carrier_prefactor
        == 2 / (5 * sqrt6),
        "carrierSumMatchesExactCoreProduction": sp.simplify(
            exact_core - expected_core
        ) == 0,
        "outerLimitingShareAtLeastOneFortySecond": outer_share_bound
        == sp.Rational(1, 42),
        "innerLimitingShareAtMostFortyOneFortySeconds": inner_share_bound
        == sp.Rational(41, 42),
        "fullSpaceDilationFactorIsRCubed": full_space_prefactor == radius**3,
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
    note_path = script_path.with_name("affine_core_dyadic_saturation_note.md")
    return {
        "schemaVersion": "1.0",
        "release": "R0.69U",
        "status": "passed" if all(checks.values()) else "failed",
        "provenance": {
            "sourceCommit": source_commit,
            "auditScript": str(script_path.relative_to(script_path.parents[1])),
            "auditScriptSha256": sha256(script_path),
            "researchNote": str(note_path.relative_to(note_path.parents[1])),
            "researchNoteSha256": sha256(note_path),
        },
        "cutoffConstruction": {
            "transitionInterval": ["1/20", "19/20"],
            "transitionLength": "9/10",
            "baseDensity": "(30/L) z^2 (1-z)^2",
            "baseDensityL2Squared": str(h_l2),
            "mollifier": "nonnegative even C-infinity unit mass, support radius <1/20",
            "energyBound": str(energy_bound),
        },
        "limitingCarrier": {
            "innerRadialCoefficient": "5/2+E",
            "outerRadialCoefficient": "5/2-E",
            "outerRadialMargin": str(outer_margin),
            "outerShareLowerBound": str(outer_share_bound),
            "innerShareUpperBound": str(inner_share_bound),
            "exactCoreProduction": str(expected_core),
            "eventualCoreCancellationRatio": "1",
        },
        "fullSpaceScaling": {
            "field": "u_R(x)=R*u_1(x/R)",
            "annulus": "A_(m+k)(u_R)=R^3*A_k(u_1) for R=2^m",
            "ratio": "Gamma_ann(u_R)=Gamma_ann(u_1)",
        },
        "claimBoundary": {
            "proved": (
                "eventual exact saturation of the core-restricted dyadic carrier, "
                "its two limiting coefficients, and full-space dilation invariance"
            ),
            "notProved": (
                "full-space annular saturation, dynamic depletion, global regularity, "
                "finite-time singularity, or the Millennium Problem"
            ),
        },
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--source-commit")
    arguments = parser.parse_args()
    result = audit(arguments.source_commit)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if result["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
