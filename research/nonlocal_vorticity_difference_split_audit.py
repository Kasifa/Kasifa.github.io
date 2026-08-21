#!/usr/bin/env python3
"""Exact audit for the R0.69R nonlocal vorticity-difference split."""

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
    wx, wy, wz, vx, vy, vz = sp.symbols(
        "wx wy wz vx vy vz", real=True
    )
    omega_x = sp.Matrix([wx, wy, wz])
    omega_y = sp.Matrix([vx, vy, vz])
    cross_difference = sp.simplify(
        omega_x.cross(omega_y)
        - omega_x.cross(omega_y - omega_x)
    )

    radius, capital_x, capital_y = sp.symbols("r X Y", positive=True)
    split_function = capital_x * radius + capital_y * radius ** sp.Rational(-3, 2)
    optimal_radius = (3 * capital_y / (2 * capital_x)) ** sp.Rational(2, 5)
    derivative_at_optimum = sp.simplify(
        sp.diff(split_function, radius).subs(radius, optimal_radius)
    )
    second_derivative_at_optimum = sp.simplify(
        sp.diff(split_function, radius, 2).subs(radius, optimal_radius)
    )
    optimal_value = sp.simplify(split_function.subs(radius, optimal_radius))
    expected_optimal_value = (
        sp.Rational(5, 3)
        * (sp.Rational(3, 2)) ** sp.Rational(2, 5)
        * capital_x ** sp.Rational(3, 5)
        * capital_y ** sp.Rational(2, 5)
    )

    A, B, near_constant, far_constant = sp.symbols(
        "A B C_n C_f", positive=True
    )
    near_scale = near_constant * A ** sp.Rational(1, 2) * B ** sp.Rational(5, 2)
    far_scale = far_constant * A**3
    norm_optimal_radius = sp.simplify(
        optimal_radius.subs({capital_x: near_scale, capital_y: far_scale})
    )
    norm_optimal_value = sp.simplify(
        optimal_value.subs({capital_x: near_scale, capital_y: far_scale})
    )
    expected_norm_value = (
        sp.Rational(5, 3)
        * (sp.Rational(3, 2)) ** sp.Rational(2, 5)
        * near_constant ** sp.Rational(3, 5)
        * far_constant ** sp.Rational(2, 5)
        * A ** sp.Rational(3, 2)
        * B ** sp.Rational(3, 2)
    )

    radial_variable = sp.symbols("s", positive=True)
    far_kernel_l2_squared = sp.integrate(
        4 * sp.pi * radial_variable**2 * radial_variable**-6,
        (radial_variable, radius, sp.oo),
    )
    near_radial_mass = sp.integrate(
        radial_variable**2 * radial_variable**-2,
        (radial_variable, 0, radius),
    )

    p, q = sp.symbols("p q", real=True)
    scaling_solution = sp.solve(
        [sp.Eq(p + q, 3), sp.Eq(p + 3 * q, 6)],
        [p, q],
        dict=True,
    )

    coefficient, epsilon, dissipation = sp.symbols(
        "C epsilon D", positive=True
    )
    young_profit = (
        coefficient * A ** sp.Rational(3, 2)
        * dissipation ** sp.Rational(3, 4)
        - epsilon * dissipation
    )
    young_optimizer = (
        3 * coefficient * A ** sp.Rational(3, 2) / (4 * epsilon)
    ) ** 4
    young_derivative = sp.simplify(
        sp.diff(young_profit, dissipation).subs(
            dissipation, young_optimizer
        )
    )
    young_remainder = sp.simplify(
        young_profit.subs(dissipation, young_optimizer)
    )

    amplitude, lam = sp.symbols("a lambda", positive=True)
    amplitude_production = amplitude**3
    amplitude_norm_product = sp.simplify(
        amplitude ** sp.Rational(3, 2)
        * amplitude ** sp.Rational(3, 2)
    )
    spatial_production = lam**3
    spatial_norm_product = sp.simplify(
        (lam ** sp.Rational(1, 2)) ** sp.Rational(3, 2)
        * (lam ** sp.Rational(3, 2)) ** sp.Rational(3, 2)
    )

    checks = {
        "crossProductDifferenceIdentity": cross_difference == sp.zeros(3, 1),
        "nearKernelRadialMassIsLinear": near_radial_mass == radius,
        "farKernelL2SquaredIsExact": far_kernel_l2_squared
        == 4 * sp.pi / (3 * radius**3),
        "splitOptimizerIsCritical": derivative_at_optimum == 0,
        "splitOptimizerIsStrictMinimum": second_derivative_at_optimum > 0,
        "splitMinimumConstantIsExact": sp.simplify(
            optimal_value - expected_optimal_value
        )
        == 0,
        "optimalRadiusIsEnstrophyLength": sp.simplify(
            norm_optimal_radius
            / (
                (3 * far_constant / (2 * near_constant))
                ** sp.Rational(2, 5)
                * A
                / B
            )
        )
        == 1,
        "optimizedNormPowersAreThreeHalves": sp.simplify(
            norm_optimal_value - expected_norm_value
        )
        == 0,
        "scalingSystemHasUniqueSolution": scaling_solution
        == [{p: sp.Rational(3, 2), q: sp.Rational(3, 2)}],
        "amplitudeScalingMatchesProduction": amplitude_norm_product
        == amplitude_production,
        "spatialScalingMatchesProduction": spatial_norm_product
        == spatial_production,
        "youngOptimizerIsCritical": young_derivative == 0,
        "youngRemainderIsSextic": young_remainder
        == sp.Rational(27, 256)
        * coefficient**4
        * A**6
        * epsilon**-3,
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
    note_path = script_path.with_name("nonlocal_vorticity_difference_split_note.md")
    return {
        "schemaVersion": "1.0",
        "release": "R0.69R",
        "status": "passed" if all(checks.values()) else "failed",
        "provenance": {
            "sourceCommit": source_commit,
            "auditScript": str(script_path.relative_to(script_path.parents[1])),
            "auditScriptSha256": sha256(script_path),
            "researchNote": str(note_path.relative_to(note_path.parents[1])),
            "researchNoteSha256": sha256(note_path),
        },
        "nearFarSplit": {
            "near": "C_n*r*A^(1/2)*B^(5/2)",
            "far": "C_f*r^(-3/2)*A^3",
            "optimalRadius": str(norm_optimal_radius),
            "optimizedBound": str(norm_optimal_value),
        },
        "scalingUniqueness": {
            "amplitudeConstraint": "p+q=3",
            "spatialConstraint": "p+3q=6",
            "solution": {"p": "3/2", "q": "3/2"},
        },
        "youngEndpoint": {
            "optimizer": str(young_optimizer),
            "remainder": str(young_remainder),
            "enstrophyNormPower": 6,
        },
        "claimBoundary": {
            "proved": (
                "the magnitude-coupled nonlocal difference plus an energy far "
                "field returns exactly to the classical A^(3/2)B^(3/2) bound"
            ),
            "notProved": (
                "failure of signed cross-scale cancellation, global regularity, "
                "or finite-time blow-up"
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
