#!/usr/bin/env python3
"""Exact exponent and shell-comparison audit for R0.69M."""

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
    m, k = sp.symbols("m k", integer=True, positive=True)
    gamma = sp.Rational(1, 2)

    morrey_constant = sp.simplify(
        2 * sp.summation(2 ** (-4 * m), (m, 2, sp.oo))
    )
    no_reverse_ratio = sp.simplify(2 ** (4 * k - 1))

    high_frequency_exponents = {
        "velocityL3": -gamma,
        "kineticMorrey": -2 * gamma,
        "nearL2Source": 2 - 2 * gamma,
        "absoluteAnnularUQ": 2 - 3 * gamma,
    }

    length_exponents = {
        "U_r": -1 + 3 * sp.Rational(1, 3),
        "G_r": 1 - 2 + 3 * sp.Rational(1, 3),
        "Q_r": 2 - 4 + 3 * sp.Rational(2, 3),
        "rCubedNearPairing": 3 + (-2 + 3 * sp.Rational(1, 3)) + (
            -4 + 3 * sp.Rational(2, 3)
        ),
        "BInfinity": -1 + 1,
        "kineticMorrey": -1 + 1,
        "parabolicGradientL3Cubed": 1 + 3 * (-2 + 1) + 2,
    }

    mixed_gradient_sum = sp.Rational(3, 3) + sp.Rational(2, 3)

    checks = {
        "morreySeriesConstantIsOneOver120": morrey_constant == sp.Rational(1, 120),
        "farBudgetAndMorreyAreScaleInvariant": (
            length_exponents["BInfinity"] == 0
            and length_exponents["kineticMorrey"] == 0
        ),
        "noReverseRatioDivergesWithShellIndex": sp.limit(
            no_reverse_ratio, k, sp.oo
        )
        == sp.oo,
        "velocityL3TendsToZeroInWitness": high_frequency_exponents["velocityL3"] < 0,
        "kineticMorreyTendsToZeroInWitness": high_frequency_exponents[
            "kineticMorrey"
        ]
        < 0,
        "nearL2SourceDivergesInWitness": high_frequency_exponents[
            "nearL2Source"
        ]
        > 0,
        "absoluteAnnularTermDivergesInWitness": high_frequency_exponents[
            "absoluteAnnularUQ"
        ]
        > 0,
        "lowerExponentNearQuantitiesAreScaleInvariant": all(
            length_exponents[name] == 0
            for name in ("U_r", "G_r", "Q_r", "rCubedNearPairing")
        ),
        "parabolicCubicGradientQuantityIsScaleInvariant": (
            length_exponents["parabolicGradientL3Cubed"] == 0
        ),
        "cubicGradientMixedExponentIsBelowCriticalLine": (
            mixed_gradient_sum == sp.Rational(5, 3) and mixed_gradient_sum < 2
        ),
        "energyEndpointIsNotAHolderDualPair": sp.Rational(1, 2) + 1 > 1,
        "annularEnergyEndpointIsNotAHolderProduct": sp.Rational(1, 6) + 1 > 1,
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
    note_path = script_path.with_name("criterion_comparison_pressure_budget_note.md")

    return {
        "schemaVersion": "1.0",
        "release": "R0.69M",
        "status": "passed" if all(checks.values()) else "failed",
        "provenance": {
            "sourceCommit": source_commit,
            "auditScript": str(script_path.relative_to(script_path.parents[1])),
            "auditScriptSha256": sha256(script_path),
            "researchNote": str(note_path.relative_to(note_path.parents[1])),
            "researchNoteSha256": sha256(note_path),
        },
        "morreyComparison": {
            "upperBound": "B_infinity <= M_2 / 120",
            "geometricSeriesConstant": str(morrey_constant),
            "singleShellReverseRatioLowerBound": str(no_reverse_ratio),
        },
        "highFrequencyWitness": {
            "amplitude": "N**(-1/2)",
            "powerExponents": {
                name: str(exponent)
                for name, exponent in high_frequency_exponents.items()
            },
            "interpretation": "functional time-slice obstruction only",
        },
        "lowerExponentRepair": {
            "bound": "r**3 |P_near| <= C G_r (G_r**2 + U_r G_r + U_r**2)",
            "mixedGradientExponentSum": str(mixed_gradient_sum),
            "criticalGradientLine": "2",
        },
        "lengthExponents": {
            name: str(exponent) for name, exponent in length_exponents.items()
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
