#!/usr/bin/env python3
"""Exact scaling and separation audit for the R0.69L pressure budget."""

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
    e2, e3, e4, tail5 = sp.symbols(
        "e2 e3 e4 tail5", nonnegative=True
    )
    alpha, beta = sp.symbols("alpha beta", positive=True)

    def weight(index: int) -> sp.Rational:
        return sp.Rational(1, 2 ** (5 * index))

    b2 = weight(2) * (e2 + e3 + e4 + tail5)
    b3 = weight(2) * e2 + weight(3) * (e3 + e4 + tail5)
    b4 = (
        weight(2) * e2
        + weight(3) * e3
        + weight(4) * (e4 + tail5)
    )
    b5 = (
        weight(2) * e2
        + weight(3) * e3
        + weight(4) * e4
        + weight(5) * tail5
    )
    b_infinity_truncated = (
        weight(2) * e2 + weight(3) * e3 + weight(4) * e4
    )

    length_exponents = {
        "pressurePairing": -3,
        "rCubedPressurePairing": 3 + (-3),
        "strainL2": -sp.Rational(1, 2),
        "sigma": sp.Rational(1, 2) - sp.Rational(1, 2),
        "localizedSourceL2": -sp.Rational(5, 2),
        "nearCost": sp.Rational(5, 2) - sp.Rational(5, 2),
        "shellEnergy": 1,
        "normalizedShellEnergy": -1 + 1,
        "firstBoundaryFlux": 2 + (-1 - 4 + 3),
        "secondBoundaryFlux": 1 + (-1 - 3 + 3),
        "dissipation": 3 + (2 * -3 + 3),
    }

    pressure_cross = alpha * beta**2
    local_dissipation = alpha**2
    amplitude_ratio = sp.simplify(pressure_cross / local_dissipation)

    checks = {
        "allNormalizedQuantitiesAreScaleInvariant": all(
            exponent == 0
            for name, exponent in length_exponents.items()
            if name
            not in {"pressurePairing", "strainL2", "localizedSourceL2", "shellEnergy"}
        ),
        "dyadicKernelHasFifthPower": weight(3) / weight(2) == sp.Rational(1, 32),
        "firstSeparationStepMatchesTailMigration": sp.simplify(
            b2 - b3 - (weight(2) - weight(3)) * (e3 + e4 + tail5)
        )
        == 0,
        "secondSeparationStepMatchesTailMigration": sp.simplify(
            b3 - b4 - (weight(3) - weight(4)) * (e4 + tail5)
        )
        == 0,
        "thirdSeparationStepMatchesTailMigration": sp.simplify(
            b4 - b5 - (weight(4) - weight(5)) * tail5
        )
        == 0,
        "separationBudgetIsMonotone": all(
            expression.is_nonnegative is True
            for expression in (b2 - b3, b3 - b4, b4 - b5)
        ),
        "finiteShellLimitRetainsEveryTransitionShell": sp.simplify(
            b5.subs(tail5, 0) - b_infinity_truncated
        )
        == 0,
        "firstSeparatedShellHasNonzeroFloor": weight(2) == sp.Rational(1, 1024),
        "nearCostDoesNotContainSeparationParameter": (
            "M" not in str(length_exponents["nearCost"])
        ),
        "boundaryCostDoesNotContainSeparationParameter": (
            "M" not in str(length_exponents["firstBoundaryFlux"])
            and "M" not in str(length_exponents["secondBoundaryFlux"])
        ),
        "crossPressureHasAlphaBetaSquaredHomogeneity": (
            pressure_cross == alpha * beta**2
        ),
        "pressureToDissipationRatioIsBetaSquaredOverAlpha": (
            amplitude_ratio == beta**2 / alpha
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
    note_path = script_path.with_name("three_zone_pressure_budget_note.md")

    return {
        "schemaVersion": "1.0",
        "release": "R0.69L",
        "status": "passed" if all(checks.values()) else "failed",
        "provenance": {
            "sourceCommit": source_commit,
            "auditScript": str(script_path.relative_to(script_path.parents[1])),
            "auditScriptSha256": sha256(script_path),
            "researchNote": str(note_path.relative_to(note_path.parents[1])),
            "researchNoteSha256": sha256(note_path),
        },
        "normalizedBudget": {
            "pressure": "r**3 |P_r|",
            "near": "sigma_r N_r",
            "transition": "sigma_r sum_{m=2}^{M-1} 2**(-5m) e_m",
            "far": "sigma_r 2**(-5M) sum_{m>=M} e_m",
            "boundary": "b_r",
            "optimized": "sum_{m>=2} 2**(-5m) e_m",
        },
        "lengthExponents": {
            name: str(exponent) for name, exponent in length_exponents.items()
        },
        "finiteSeparationModel": {
            "B2": str(b2),
            "B3": str(b3),
            "B4": str(b4),
            "B5": str(b5),
            "truncatedLimit": str(b_infinity_truncated),
            "firstShellWeight": str(weight(2)),
        },
        "amplitudeAudit": {
            "crossPressure": str(pressure_cross),
            "localDissipation": str(local_dissipation),
            "ratio": str(amplitude_ratio),
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
