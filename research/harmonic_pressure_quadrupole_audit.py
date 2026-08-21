#!/usr/bin/env python3
"""Exact audit for the R0.69J harmonic far-field quadrupole obstruction."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


def kernel(source: sp.Matrix) -> sp.Matrix:
    """Return 4*pi times the Newtonian Hessian at x=0."""
    radius_squared = sp.expand(source.dot(source))
    radius = sp.sqrt(radius_squared)
    return sp.simplify(
        3 * (source * source.T) / radius**5 - sp.eye(3) / radius**3
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(source_commit: str | None = None) -> dict[str, object]:
    radius = sp.symbols("R", positive=True)
    e1 = sp.Matrix([1, 0, 0])
    e2 = sp.Matrix([0, 1, 0])
    sources = (
        (radius * e1, sp.Integer(1)),
        (-radius * e1, sp.Integer(1)),
        (radius * e2, sp.Integer(-1)),
        (-radius * e2, sp.Integer(-1)),
    )

    total_mass = sp.simplify(sum(weight for _, weight in sources))
    first_moment = sp.simplify(
        sum((weight * point for point, weight in sources), sp.zeros(3, 1))
    )
    normalized_potential = sp.simplify(
        sum(weight / sp.sqrt(point.dot(point)) for point, weight in sources)
    )
    normalized_gradient = sp.simplify(
        sum(
            (weight * point / sp.sqrt(point.dot(point)) ** 3 for point, weight in sources),
            sp.zeros(3, 1),
        )
    )
    normalized_hessian = sp.simplify(
        sum((weight * kernel(point) for point, weight in sources), sp.zeros(3, 3))
    )
    expected_hessian = sp.diag(6, -6, 0) / radius**3
    strain_jet = sp.diag(1, -1, 0)
    normalized_pairing = sp.simplify(sp.trace(strain_jet.T * normalized_hessian))

    checks = {
        "remoteSourceHasZeroTotalMass": total_mass == 0,
        "remoteSourceHasZeroFirstMoment": first_moment == sp.zeros(3, 1),
        "farPotentialVanishesAtCenter": normalized_potential == 0,
        "farPressureGradientVanishesAtCenter": normalized_gradient == sp.zeros(3, 1),
        "farPressureHessianMatchesExactQuadrupole": normalized_hessian == expected_hessian,
        "farPressureHessianIsTraceFree": sp.trace(normalized_hessian) == 0,
        "localStrainJetIsTraceFree": sp.trace(strain_jet) == 0,
        "traceFreePairingIsNonzero": normalized_pairing == 12 / radius**3,
        "quadrupoleDecaysLikeInverseRadiusCubed": (
            sp.simplify(normalized_hessian.subs(radius, 2) - expected_hessian.subs(radius, 1) / 8)
            == sp.zeros(3, 3)
        ),
        "sourcesLieOutsideEveryStrictSubball": all(
            sp.simplify(point.dot(point) - radius**2) == 0 for point, _ in sources
        ),
    }
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
    note_path = script_path.with_name("harmonic_pressure_quadrupole_note.md")

    return {
        "schemaVersion": "1.0",
        "release": "R0.69J",
        "status": "passed" if all(checks.values()) else "failed",
        "normalization": "reported Hessians are multiplied by 4*pi",
        "provenance": {
            "sourceCommit": source_commit,
            "auditScript": str(script_path.relative_to(script_path.parents[1])),
            "auditScriptSha256": sha256(script_path),
            "researchNote": str(note_path.relative_to(note_path.parents[1])),
            "researchNoteSha256": sha256(note_path),
        },
        "source": {
            "points": ["+R e1", "-R e1", "+R e2", "-R e2"],
            "weights": [1, 1, -1, -1],
            "totalMass": str(total_mass),
            "firstMoment": [str(entry) for entry in first_moment],
        },
        "centerJet": {
            "fourPiPotential": str(normalized_potential),
            "fourPiGradient": [str(entry) for entry in normalized_gradient],
            "fourPiHessian": [
                [str(normalized_hessian[row, column]) for column in range(3)]
                for row in range(3)
            ],
            "strain": [
                [str(strain_jet[row, column]) for column in range(3)]
                for row in range(3)
            ],
            "fourPiStrainHessianPairing": str(normalized_pairing),
            "actualStrainHessianPairing": "3/(pi*R**3)",
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
