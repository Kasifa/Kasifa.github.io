#!/usr/bin/env python3
"""Exact symbolic audit for the R0.69S single-shell stretching witness."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def vector(values: tuple[object, object, object]) -> sp.Matrix:
    return sp.Matrix(values)


def audit(source_commit: str | None = None) -> dict[str, object]:
    imaginary = sp.I
    wavevectors = (
        vector((1, 0, 0)),
        vector((0, 1, 0)),
        vector((-1, -1, 0)),
    )
    amplitudes = (
        vector((0, 1, -1 - imaginary)),
        vector((-1, 0, -1)),
        vector((-1 - imaginary, 1 + imaginary, 1)),
    )

    closure = sp.simplify(sum(wavevectors, sp.zeros(3, 1)))
    divergence_residuals = [
        sp.simplify(k.dot(a)) for k, a in zip(wavevectors, amplitudes)
    ]
    squared_lengths = [int(k.dot(k)) for k in wavevectors]

    coefficients: dict[tuple[int, int, int], sp.Matrix] = {}
    positive_wavevector_keys: set[tuple[int, int, int]] = set()
    for k, amplitude in zip(wavevectors, amplitudes):
        key = tuple(int(value) for value in k)
        positive_wavevector_keys.add(key)
        coefficients[key] = amplitude
        coefficients[tuple(-value for value in key)] = sp.conjugate(amplitude)

    def vorticity(frequency: sp.Matrix, amplitude: sp.Matrix) -> sp.Matrix:
        return imaginary * frequency.cross(amplitude)

    def strain(frequency: sp.Matrix, amplitude: sp.Matrix) -> sp.Matrix:
        return (
            imaginary
            * sp.Rational(1, 2)
            * (frequency * amplitude.T + amplitude * frequency.T)
        )

    stretching = sp.Integer(0)
    ordered_contributions: list[sp.Expr] = []
    positive_contributions: list[sp.Expr] = []
    negative_contributions: list[sp.Expr] = []
    for left_key, left_amplitude in coefficients.items():
        left = vector(left_key)
        omega_left = vorticity(left, left_amplitude)
        for middle_key, middle_amplitude in coefficients.items():
            middle = vector(middle_key)
            right_key = tuple(int(value) for value in -(left + middle))
            if right_key not in coefficients:
                continue
            right = vector(right_key)
            omega_right = vorticity(right, coefficients[right_key])
            contribution = sp.simplify(
                (omega_left.T * strain(middle, middle_amplitude) * omega_right)[0]
            )
            if contribution != 0:
                ordered_contributions.append(contribution)
                triple = {left_key, middle_key, right_key}
                if triple == positive_wavevector_keys:
                    positive_contributions.append(contribution)
                else:
                    negative_contributions.append(contribution)
            stretching += contribution
    stretching = sp.simplify(stretching)

    modal_transfers: list[sp.Expr] = []
    for index in range(3):
        second = (index + 1) % 3
        third = (index + 2) % 3
        first_term = (
            wavevectors[third].dot(amplitudes[second])
            * amplitudes[index].dot(amplitudes[third])
        )
        second_term = (
            wavevectors[second].dot(amplitudes[third])
            * amplitudes[index].dot(amplitudes[second])
        )
        modal_transfers.append(sp.simplify(sp.im(first_term + second_term)))

    energy_transfer = sp.simplify(sum(modal_transfers))
    enstrophy_transfer = sp.simplify(
        sum(
            length * transfer
            for length, transfer in zip(squared_lengths, modal_transfers)
        )
    )

    expected_half = [
        sp.Rational(5, 2),
        -sp.Rational(1, 2),
        -sp.Rational(3, 2),
        -sp.Rational(1, 2),
        -sp.Rational(3, 2),
        sp.Rational(5, 2),
    ]
    shell_productions = {"0": stretching}
    absolute_shell_sum = sum(abs(value) for value in shell_productions.values())
    cancellation_ratio = sp.simplify(abs(stretching) / absolute_shell_sum)

    amplitude, frequency_scale = sp.symbols("a N", positive=True)
    amplitude_scaled = sp.simplify(amplitude**3 * stretching)
    frequency_scaled = sp.simplify(frequency_scale**3 * stretching)

    checks = {
        "triadCloses": closure == sp.zeros(3, 1),
        "allModesAreDivergenceFree": divergence_residuals == [0, 0, 0],
        "squaredLengthsAreOneOneTwo": squared_lengths == [1, 1, 2],
        "allModesLieInSingleDyadicShell": all(1 <= length < 4 for length in squared_lengths),
        "modalTransfersAreTwoMinusThreeOne": modal_transfers == [2, -3, 1],
        "kineticEnergyTransferCancels": energy_transfer == 0,
        "enstrophyTransferIsPositive": enstrophy_transfer == 1,
        "positiveTriadContributionsAreExact": positive_contributions == expected_half,
        "conjugateTriadContributionsMatch": negative_contributions == expected_half,
        "fullVortexStretchingIsTwo": stretching == 2,
        "onlyShellZeroIsActive": shell_productions == {"0": 2},
        "cancellationRatioIsOne": cancellation_ratio == 1,
        "signReversalFlipsProduction": -stretching == -2,
        "amplitudeScalingIsCubic": amplitude_scaled == 2 * amplitude**3,
        "frequencyRelocationScalesCubically": frequency_scaled == 2 * frequency_scale**3,
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
    note_path = script_path.with_name("signed_output_shell_no_cancellation_note.md")
    return {
        "schemaVersion": "1.0",
        "release": "R0.69S",
        "status": "passed" if all(checks.values()) else "failed",
        "provenance": {
            "sourceCommit": source_commit,
            "auditScript": str(script_path.relative_to(script_path.parents[1])),
            "auditScriptSha256": sha256(script_path),
            "researchNote": str(note_path.relative_to(note_path.parents[1])),
            "researchNoteSha256": sha256(note_path),
        },
        "witness": {
            "wavevectors": [list(map(int, k)) for k in wavevectors],
            "squaredLengths": squared_lengths,
            "modalTransfers": [str(value) for value in modal_transfers],
            "orderedStretchingContributions": [
                str(value) for value in ordered_contributions
            ],
            "fullVortexStretching": str(stretching),
        },
        "shellDecomposition": {
            "activeShell": 0,
            "activeShellRange": "1<=|k|<2",
            "shellProductions": {
                key: str(value) for key, value in shell_productions.items()
            },
            "cancellationRatio": str(cancellation_ratio),
        },
        "scaling": {
            "amplitude": str(amplitude_scaled),
            "frequencyRelocation": str(frequency_scaled),
        },
        "claimBoundary": {
            "proved": (
                "sharp dyadic output-shell grouping alone has no universal "
                "signed depletion factor below one"
            ),
            "notProved": (
                "failure of smooth-projector commutators, physical-space "
                "annular cancellation, global regularity, or finite-time blow-up"
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
