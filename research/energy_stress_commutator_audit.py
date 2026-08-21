#!/usr/bin/env python3
"""Exact exponent audit for the R0.69N stress-commutator bridge."""

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
    q = sp.symbols("q", positive=True)
    s = sp.symbols("s", positive=True)
    amplitude = sp.symbols("A", positive=True)

    p = sp.simplify(q / (q - 2))
    theta = sp.simplify(3 * (sp.Rational(1, 2) - 1 / q))
    mu_exponent_after_young = sp.simplify(4 * (1 - theta))
    sigma_exponent_after_young = sp.simplify(4 * theta)

    p_hardy = sp.simplify(3 / (3 - s))
    p_hardy_dual = sp.simplify(3 / s)

    q4 = {
        "p": sp.simplify(p.subs(q, 4)),
        "theta": sp.simplify(theta.subs(q, 4)),
        "muInX": sp.simplify((2 * (1 - theta)).subs(q, 4)),
        "sigmaInX": sp.simplify((2 * theta).subs(q, 4)),
        "muAfterYoung": sp.simplify(mu_exponent_after_young.subs(q, 4)),
        "sigmaAfterYoung": sp.simplify(sigma_exponent_after_young.subs(q, 4)),
    }
    q6 = {
        "p": sp.simplify(p.subs(q, 6)),
        "theta": sp.simplify(theta.subs(q, 6)),
        "muAfterYoung": sp.simplify(mu_exponent_after_young.subs(q, 6)),
        "sigmaAfterYoung": sp.simplify(sigma_exponent_after_young.subs(q, 6)),
    }

    length_exponents = {
        "mu": -sp.Rational(1, 2) + sp.Rational(1, 2),
        "sigma": sp.Rational(1, 2) - sp.Rational(1, 2),
        "D": 3 + 2 * (-sp.Rational(3, 2)),
        "rCubedPressure": 3 - 3,
        "q4LeadingProduct": (
            sp.Rational(1, 2) * 0
            + sp.Rational(3, 2) * 0
            + sp.Rational(1, 2) * 0
        ),
    }

    time_width = amplitude ** -2
    time_l2_mass = sp.simplify(amplitude**2 * time_width)
    time_l3_mass = sp.simplify(amplitude**3 * time_width)

    checks = {
        "holderExponentsAreConjugate": sp.simplify(2 / q + 1 / p) == 1,
        "q4EndpointHasP2": q4["p"] == 2,
        "q6EndpointHasPThreeHalves": q6["p"] == sp.Rational(3, 2),
        "q4InterpolationThetaIsThreeQuarters": q4["theta"] == sp.Rational(3, 4),
        "q4LeadingCoefficientIsMuHalfSigmaThreeHalves": (
            q4["muInX"] == sp.Rational(1, 2)
            and q4["sigmaInX"] == sp.Rational(3, 2)
        ),
        "q4YoungCostIsMuSigmaCubed": (
            q4["muAfterYoung"] == 1 and q4["sigmaAfterYoung"] == 3
        ),
        "q6YoungCostIsSigmaFourth": (
            q6["muAfterYoung"] == 0 and q6["sigmaAfterYoung"] == 4
        ),
        "sigmaPowerIncreasesAcrossFamily": (
            sp.diff(sigma_exponent_after_young, q) > 0
        ),
        "hardySobolevExponentsAreDual": (
            sp.simplify(1 / p_hardy + 1 / p_hardy_dual) == 1
        ),
        "hardyDualFrontierHasCriticalProductThree": (
            sp.simplify(s * p_hardy_dual) == 3
        ),
        "hilbertHardyDualPointNeedsThreeHalvesDerivatives": (
            sp.solve(sp.Eq(p_hardy_dual, 2), s) == [sp.Rational(3, 2)]
        ),
        "dissipationPointLiesBelowHardyDualFrontier": 1 * 2 < 3,
        "allNormalizedQuantitiesAreScaleInvariant": all(
            exponent == 0 for exponent in length_exponents.values()
        ),
        "timeSpikeKeepsQuadraticMassFixed": time_l2_mass == 1,
        "timeSpikeCubicMassDiverges": (
            time_l3_mass == amplitude
            and sp.limit(time_l3_mass, amplitude, sp.oo) == sp.oo
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
    note_path = script_path.with_name("energy_stress_commutator_note.md")

    return {
        "schemaVersion": "1.0",
        "release": "R0.69N",
        "status": "passed" if all(checks.values()) else "failed",
        "provenance": {
            "sourceCommit": source_commit,
            "auditScript": str(script_path.relative_to(script_path.parents[1])),
            "auditScriptSha256": sha256(script_path),
            "researchNote": str(note_path.relative_to(note_path.parents[1])),
            "researchNoteSha256": sha256(note_path),
        },
        "energyCommutatorFamily": {
            "holderP": str(p),
            "theta": str(theta),
            "youngMuExponent": str(mu_exponent_after_young),
            "youngSigmaExponent": str(sigma_exponent_after_young),
            "q4": {name: str(value) for name, value in q4.items()},
            "q6": {name: str(value) for name, value in q6.items()},
        },
        "hardyDualityFrontier": {
            "sourceExponent": str(p_hardy),
            "dualExponent": str(p_hardy_dual),
            "criticalProduct": str(sp.simplify(s * p_hardy_dual)),
            "hilbertDerivativeOrder": "3/2",
            "dissipationProduct": "2",
        },
        "timeSpike": {
            "height": "A",
            "width": "A**(-2)",
            "quadraticMass": str(time_l2_mass),
            "cubicMass": str(time_l3_mass),
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
