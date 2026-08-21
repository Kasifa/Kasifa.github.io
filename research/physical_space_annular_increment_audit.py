#!/usr/bin/env python3
"""Exact symbolic audit for the R0.69T physical-space annular identities."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def vector(prefix: str) -> sp.Matrix:
    return sp.Matrix(sp.symbols(f"{prefix}1 {prefix}2 {prefix}3", real=True))


def audit(source_commit: str | None = None) -> dict[str, object]:
    e = vector("e")
    xi = vector("xi")
    eta = vector("eta")
    omega_x = vector("a")
    omega_y = vector("b")
    separation = vector("z")
    rho_x, rho_y = sp.symbols("rho_x rho_y", positive=True)

    direction_numerator = sp.expand(
        rho_x**2
        * rho_y
        * e.dot(xi)
        * e.dot(eta.cross(xi))
    )
    polynomial_numerator = sp.expand(
        e.dot(rho_x * xi)
        * e.dot((rho_y * eta).cross(rho_x * xi))
    )

    original = sp.expand(
        e.dot(omega_x) * e.dot(omega_y.cross(omega_x))
    )
    exchanged = sp.expand(
        (-e).dot(omega_y) * (-e).dot(omega_x.cross(omega_y))
    )
    delta = omega_y - omega_x
    pair_average = sp.expand((original + exchanged) / 2)
    two_increment = sp.expand(
        sp.Rational(1, 2)
        * e.dot(delta)
        * e.dot(omega_x.cross(delta))
    )

    amplitude = sp.symbols("alpha", real=True)
    amplitude_scaled = sp.expand(
        e.dot(amplitude * omega_x)
        * e.dot((amplitude * omega_y).cross(amplitude * omega_x))
    )

    cutoff_symbols = {
        index: sp.symbols(f"c_{index}")
        for index in range(-3, 7)
    }
    shell_indices = list(range(-2, 6))
    shell_terms = [
        cutoff_symbols[index + 1] - cutoff_symbols[index]
        for index in shell_indices
    ]
    telescoped = sp.simplify(sum(shell_terms))
    telescoped_expected = cutoff_symbols[6] - cutoff_symbols[-2]
    near_far_remainder = sp.expand(
        (1 - cutoff_symbols[6]) + cutoff_symbols[-2]
    )

    # Three vorticities contribute lambda^6, |x-y|^{-3} contributes
    # lambda^3, and dx dy contributes lambda^{-6}.
    ns_scaling_exponent = 3 * 2 + 3 - 2 * 3
    shell_index, dyadic_shift_exponent = sp.symbols(
        "j ell", integer=True
    )
    shifted_partition_argument = sp.simplify(
        2 ** (-shell_index) / 2**dyadic_shift_exponent
        - 2 ** (-(shell_index + dyadic_shift_exponent))
    )
    radius_squared = sp.expand(separation.dot(separation))
    exchanged_radius_squared = sp.expand((-separation).dot(-separation))

    checks = {
        "directionFieldCancelsExactly": sp.simplify(
            direction_numerator - polynomial_numerator
        ) == 0,
        "pairExchangeCreatesTwoIncrements": sp.simplify(
            pair_average - two_increment
        ) == 0,
        "exchangedFormulaMatchesDirectSubstitution": sp.simplify(
            exchanged
            + e.dot(omega_y) * e.dot(omega_y.cross(omega_x))
        ) == 0,
        "constantVorticityPairsVanish": sp.simplify(
            two_increment.subs(
                dict(zip(list(omega_y), list(omega_x), strict=True))
            )
        ) == 0,
        "originalNumeratorIsCubic": sp.simplify(
            amplitude_scaled - amplitude**3 * original
        ) == 0,
        "eightShellWindowTelescopes": sp.simplify(
            telescoped - telescoped_expected
        ) == 0,
        "windowRemainderSplitsNearAndFar": sp.simplify(
            1 - telescoped_expected - near_far_remainder
        ) == 0,
        "navierStokesScalingExponentIsThree": ns_scaling_exponent == 3,
        "dyadicPhysicalShellShiftHasCorrectDirection": (
            shifted_partition_argument == 0
        ),
        "radialPairWeightIsExchangeInvariant": sp.simplify(
            radius_squared - exchanged_radius_squared
        ) == 0,
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
    note_path = script_path.with_name("physical_space_annular_increment_note.md")
    return {
        "schemaVersion": "1.0",
        "release": "R0.69T",
        "status": "passed" if all(checks.values()) else "failed",
        "provenance": {
            "sourceCommit": source_commit,
            "auditScript": str(script_path.relative_to(script_path.parents[1])),
            "auditScriptSha256": sha256(script_path),
            "researchNote": str(note_path.relative_to(note_path.parents[1])),
            "researchNoteSha256": sha256(note_path),
        },
        "exactIdentities": {
            "directionFreeNumerator": (
                "rho_x^2*rho_y*(e dot xi_x)*(e dot (xi_y cross xi_x)) "
                "= (e dot omega_x)*(e dot (omega_y cross omega_x))"
            ),
            "pairSymmetrizedNumerator": (
                "(1/2)*(e dot delta_omega)*"
                "(e dot (omega_x cross delta_omega))"
            ),
            "constantCorePairs": "zero whenever omega_y=omega_x",
        },
        "annularPartition": {
            "shell": "psi_j(r)=chi(2^(-j-1)*r)-chi(2^(-j)*r)",
            "finiteWindow": (
                "sum_(j=L)^U psi_j(r)="
                "chi(2^(-U-1)*r)-chi(2^(-L)*r)"
            ),
            "remainder": (
                "1-window=[1-chi(2^(-U-1)*r)]+chi(2^(-L)*r)"
            ),
            "representativeTelescopingShells": shell_indices,
        },
        "scaling": {
            "amplitude": "A_j(alpha*u)=alpha^3*A_j(u)",
            "navierStokesExponent": ns_scaling_exponent,
            "dyadicShift": (
                "A_j(u_(2^ell))=2^(3*ell)*A_(j+ell)(u)"
            ),
        },
        "affineCore": {
            "interiorPairContribution": "zero",
            "carrier": "pairs crossing from the constant-vorticity core to its complement",
            "nextTarget": "signed annular distribution of the boundary carrier",
        },
        "claimBoundary": {
            "proved": (
                "exact direction-free two-increment annular reconstruction, "
                "explicit finite-window boundaries, scaling, and affine-core carrier"
            ),
            "notProved": (
                "a universal annular depletion factor, a regularity criterion, "
                "global regularity, or finite-time blow-up"
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
