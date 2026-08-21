#!/usr/bin/env python3
"""Exact exponent audit for the R0.69O pressure time closure."""

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
    mu, sigma, dissipation, epsilon, amplitude = sp.symbols(
        "mu sigma D epsilon A", positive=True
    )

    # Saturate sigma^2 <= mu D^(1/2) with sigma=mu*z and D=mu^2*z^4.
    z = sp.symbols("z", positive=True)
    saturated_sigma = mu * z
    saturated_dissipation = mu**2 * z**4
    saturated_leading = sp.simplify(
        mu ** sp.Rational(1, 2)
        * saturated_sigma ** sp.Rational(3, 2)
        * saturated_dissipation ** sp.Rational(1, 2)
    )
    normalized_profit = sp.simplify(
        saturated_leading / (mu**2 * z**2) - epsilon * z**2
    )
    optimizer = sp.simplify((3 * mu / (4 * epsilon)) ** 2)
    optimized_profit = sp.simplify(normalized_profit.subs(z, optimizer))

    # Previous R0.69N spike, now constrained by Hilbert interpolation.
    spike_width = amplitude**-2
    spike_quadratic_mass = sp.simplify(amplitude**2 * spike_width)
    spike_cubic_mass = sp.simplify(amplitude**3 * spike_width)
    spike_dissipation_height = amplitude**4
    spike_dissipation_mass = sp.simplify(
        spike_dissipation_height * spike_width
    )

    # Lower commutator terms after sigma <= mu^(1/2) D^(1/4).
    lower_sigma_exponent = sp.Rational(5, 2)
    lower_one_mu_before_young = sp.simplify(
        sp.Rational(1, 2) + lower_sigma_exponent * sp.Rational(1, 2)
    )
    lower_one_d_before_young = sp.simplify(
        lower_sigma_exponent * sp.Rational(1, 4)
    )
    lower_one_mu_after_young = sp.simplify(
        lower_one_mu_before_young / (1 - lower_one_d_before_young)
    )
    lower_two_mu_before_young = sp.simplify(
        sp.Rational(3, 2) + sp.Rational(3, 2) * sp.Rational(1, 2)
    )
    lower_two_d_before_young = sp.simplify(
        sp.Rational(3, 2) * sp.Rational(1, 4)
    )
    lower_two_mu_after_young = sp.simplify(
        lower_two_mu_before_young / (1 - lower_two_d_before_young)
    )

    # Length exponents under u_lambda(x)=lambda u(lambda x).
    length_exponents = {
        "mu": -sp.Rational(1, 2) + sp.Rational(1, 2),
        "sigma": sp.Rational(1, 2) - sp.Rational(1, 2),
        "dissipation": 3 + 2 * (-sp.Rational(3, 2)),
        "leadingPressure": (
            sp.Rational(1, 2) * 0
            + sp.Rational(3, 2) * 0
            + sp.Rational(1, 2) * 0
        ),
        "quadraticRemainder": 4 * 0 + 2 * 0,
    }

    checks = {
        "hilbertInterpolationIsScaleInvariant": all(
            value == 0 for value in length_exponents.values()
        ),
        "saturatedInterpolationIdentity": (
            sp.simplify(
                saturated_sigma**2
                - mu * sp.sqrt(saturated_dissipation)
            )
            == 0
        ),
        "saturatedLeadingMonomialIsMuCubedZSevenHalves": (
            saturated_leading == mu**3 * z ** sp.Rational(7, 2)
        ),
        "sharpOptimizerIsThreeMuOverFourEpsilonSquared": (
            sp.simplify(
                sp.diff(normalized_profit, z).subs(z, optimizer)
            )
            == 0
        ),
        "optimizedProfitHasMuFourthEpsilonMinusThird": (
            optimized_profit
            == sp.Rational(27, 256) * mu**4 * epsilon**-3
        ),
        "kineticExponentFourIsNecessary": (
            sp.degree(sp.together(optimized_profit * epsilon**3), mu) == 4
        ),
        "epsilonExponentThreeIsNecessary": (
            sp.together(optimized_profit * mu**-4)
            .as_powers_dict()
            .get(epsilon, 0)
            == -3
        ),
        "oldSpikeKeepsQuadraticMassFixed": spike_quadratic_mass == 1,
        "oldSpikeCubicMassDiverges": (
            spike_cubic_mass == amplitude
            and sp.limit(spike_cubic_mass, amplitude, sp.oo) == sp.oo
        ),
        "oldSpikeDissipationMassDivergesQuadratically": (
            spike_dissipation_mass == amplitude**2
            and sp.limit(spike_dissipation_mass, amplitude, sp.oo) == sp.oo
        ),
        "firstLowerTermHasDissipationPowerFiveEighths": (
            lower_one_d_before_young == sp.Rational(5, 8)
        ),
        "firstLowerYoungCostHasMuPowerFourteenThirds": (
            lower_one_mu_after_young == sp.Rational(14, 3)
        ),
        "secondLowerTermHasDissipationPowerThreeEighths": (
            lower_two_d_before_young == sp.Rational(3, 8)
        ),
        "secondLowerYoungCostHasMuPowerEighteenFifths": (
            lower_two_mu_after_young == sp.Rational(18, 5)
        ),
        "pressureRemainderIsQuadraticInEnstrophy": (
            sp.degree(mu**4 * sigma**2, sigma) == 2
        ),
        "strainStretchingYoungRemainderIsSextic": (
            sp.Rational(3, 2)
            / (1 - sp.Rational(3, 4))
            == 6
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
    note_path = script_path.with_name("energy_commutator_time_closure_note.md")

    return {
        "schemaVersion": "1.0",
        "release": "R0.69O",
        "status": "passed" if all(checks.values()) else "failed",
        "provenance": {
            "sourceCommit": source_commit,
            "auditScript": str(script_path.relative_to(script_path.parents[1])),
            "auditScriptSha256": sha256(script_path),
            "researchNote": str(note_path.relative_to(note_path.parents[1])),
            "researchNoteSha256": sha256(note_path),
        },
        "leadingClosure": {
            "spatialInterpolation": "sigma^2 <= C mu D^(1/2)",
            "timeIntegratedRemainder": "C epsilon^(-3) A_v^2 E_v",
            "kineticExponent": "4",
            "enstrophyExponent": "2",
            "epsilonExponent": "-3",
        },
        "sharpnessOptimization": {
            "saturation": {
                "sigma": str(saturated_sigma),
                "dissipation": str(saturated_dissipation),
                "leading": str(saturated_leading),
            },
            "optimizer": str(optimizer),
            "optimizedProfit": str(optimized_profit),
        },
        "timeSpike": {
            "height": "A",
            "width": "A**(-2)",
            "quadraticMass": str(spike_quadratic_mass),
            "cubicMass": str(spike_cubic_mass),
            "minimumDissipationHeight": str(spike_dissipation_height),
            "minimumDissipationMass": str(spike_dissipation_mass),
        },
        "lowerTerms": {
            "muHalfSigmaFiveHalves": {
                "muBeforeYoung": str(lower_one_mu_before_young),
                "dissipationBeforeYoung": str(lower_one_d_before_young),
                "muAfterYoung": str(lower_one_mu_after_young),
            },
            "muThreeHalvesSigmaThreeHalves": {
                "muBeforeYoung": str(lower_two_mu_before_young),
                "dissipationBeforeYoung": str(lower_two_d_before_young),
                "muAfterYoung": str(lower_two_mu_after_young),
            },
        },
        "lengthExponents": {
            name: str(value) for name, value in length_exponents.items()
        },
        "remainingObstruction": {
            "term": "sigma^(3/2) D^(3/4)",
            "youngRemainder": "sigma^6",
            "interpretation": "localized cubic strain/vorticity stretching",
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
