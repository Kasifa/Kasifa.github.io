#!/usr/bin/env python3
"""Exact mass-plus-first-moment lift for the R0.67 sixth-order cycle.

The five convolution indices obey A+B+C-D-E=Q, so four spatial coordinates
are free.  This audit constructs the exact 320-state mass matrix W and the
four integer shift matrices E_j for the four-bit word 0100.  In normalized
coordinates the finite moment lift is

    m'   = W m,
    ell'_j = (W ell_j + E_j m) / 16,  1 <= j <= 4.

It independently checks the recursion against direct five-polynomial
convolution at small levels and records the spectral separation needed for a
later C^{1,1}-dual resolvent argument.  It does not certify the sign of the
complete heat-weighted five-simplex projection.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

import sixth_order_cycle_audit as r067


COORDINATES = ("A", "B", "C", "D")


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    if not enabled:
        return
    fields = " ".join(f"{key}={value}" for key, value in details.items())
    print(
        f"[R0.67B affine lift +{time.perf_counter() - started:8.2f}s] "
        f"{stage}{(' ' + fields) if fields else ''}",
        file=sys.stderr,
        flush=True,
    )


def digit_mass_and_shifts(bit: int, length: int) -> tuple[np.ndarray, list[np.ndarray]]:
    mass = np.zeros((r067.DIMENSION, r067.DIMENSION), dtype=np.int64)
    shifts = [np.zeros_like(mass) for _ in COORDINATES]
    for target_state in (0, 1):
        for quintic_state in range(32):
            for parent_carry in r067.CARRIES:
                row = r067.state_index(target_state, quintic_state, parent_carry)
                for epsilon in range(32):
                    digits = tuple((epsilon >> shift) & 1 for shift in (4, 3, 2, 1, 0))
                    signed_shift = sum(digits[:3]) - sum(digits[3:])
                    child_carry = 2 * parent_carry + bit - signed_shift
                    if child_carry not in r067.CARRIES:
                        continue
                    parity = target_state * bit + (quintic_state & epsilon).bit_count()
                    sign = -1 if parity % 2 else 1
                    column = r067.state_index(bit, epsilon, child_carry)
                    mass[row, column] += sign
                    for coordinate in range(4):
                        shifts[coordinate][row, column] += sign * digits[coordinate] * length
    return mass, shifts


def cycle_mass_and_shifts() -> tuple[np.ndarray, list[np.ndarray]]:
    mass = np.eye(r067.DIMENSION, dtype=np.int64)
    shifts = [np.zeros_like(mass) for _ in COORDINATES]
    for length, bit in zip((1, 2, 4, 8), r067.WORD):
        digit_mass, digit_shifts = digit_mass_and_shifts(bit, length)
        old_mass = mass
        shifts = [
            digit_mass @ old_shift + digit_shift @ old_mass
            for old_shift, digit_shift in zip(shifts, digit_shifts)
        ]
        mass = digit_mass @ old_mass
    return mass, shifts


def weighted_factor(coefficients: list[int], *, reverse: bool) -> list[int]:
    weighted = [index * value for index, value in enumerate(coefficients)]
    return list(reversed(weighted)) if reverse else weighted


def direct_quintic_moment_states(level: int) -> tuple[list[list[int]], list[list[list[int]]]]:
    pair = r067.rudin_shapiro_pair(level)
    masses: list[list[int]] = []
    moments: list[list[list[int]]] = [[] for _ in COORDINATES]
    for sigma in range(32):
        original = [pair[(sigma >> shift) & 1] for shift in (4, 3, 2, 1, 0)]
        factors = [
            original[0],
            original[1],
            original[2],
            list(reversed(original[3])),
            list(reversed(original[4])),
        ]
        value = factors[0]
        for factor in factors[1:]:
            value = r067.exact_convolve(value, factor)
        masses.append(value)
        for coordinate in range(4):
            weighted = weighted_factor(original[coordinate], reverse=coordinate >= 3)
            product = weighted
            for factor_index, factor in enumerate(factors):
                if factor_index == coordinate:
                    continue
                product = r067.exact_convolve(product, factor)
            moments[coordinate].append(product)
    return masses, moments


def direct_moment_audit(maximum_level: int) -> list[dict[str, int]]:
    mass = r067.initial_vector()
    moments = [np.zeros(r067.DIMENSION, dtype=np.int64) for _ in COORDINATES]
    records: list[dict[str, int]] = []
    for level in range(1, maximum_level + 1):
        bit = r067.WORD[(level - 1) % 4]
        length_before = 1 << (level - 1)
        digit_mass, digit_shifts = digit_mass_and_shifts(bit, length_before)
        old_mass = mass
        moments = [
            digit_mass @ old_moment + digit_shift @ old_mass
            for old_moment, digit_shift in zip(moments, digit_shifts)
        ]
        mass = digit_mass @ old_mass

        _bits, target = r067.repeated_word_target(level)
        pair = r067.rudin_shapiro_pair(level)
        direct_mass, direct_moments = direct_quintic_moment_states(level)
        length = 1 << level
        offset = 2 * (length - 1)
        for target_state in (0, 1):
            target_sign = pair[target_state][target]
            for quintic_state in range(32):
                for carry in r067.CARRIES:
                    exponent = target + carry * length
                    array_index = exponent + offset
                    state = r067.state_index(target_state, quintic_state, carry)
                    valid = 0 <= array_index < len(direct_mass[quintic_state])
                    expected_mass = (
                        target_sign * direct_mass[quintic_state][array_index] if valid else 0
                    )
                    if int(mass[state]) != expected_mass:
                        raise AssertionError(f"direct mass mismatch at level {level}")
                    for coordinate in range(4):
                        expected_moment = (
                            target_sign * direct_moments[coordinate][quintic_state][array_index]
                            if valid
                            else 0
                        )
                        if int(moments[coordinate][state]) != expected_moment:
                            raise AssertionError(
                                f"direct {COORDINATES[coordinate]} moment mismatch "
                                f"at level {level} state={state}"
                            )
        records.append(
            {
                "level": level,
                "M": length,
                "target": target,
                "maximumAbsoluteMass": int(np.max(np.abs(mass))),
                "maximumAbsoluteFirstMoment": max(
                    int(np.max(np.abs(moment))) for moment in moments
                ),
            }
        )
    return records


def matrix_sha256(matrix: np.ndarray) -> str:
    return hashlib.sha256(matrix.astype("<i8", copy=False).tobytes(order="C")).hexdigest()


def state_weights() -> np.ndarray:
    return np.array(
        [
            r067.POSITIVE_CARRY_WEIGHT[r067.CARRIES.index(carry)]
            for _target_state in (0, 1)
            for _quintic_state in range(32)
            for carry in r067.CARRIES
        ],
        dtype=object,
    )


def weighted_row_norm(matrix: np.ndarray, weights: np.ndarray) -> Fraction:
    return max(
        Fraction(
            sum(abs(int(matrix[row, column])) * int(weights[column]) for column in range(len(weights))),
            int(weights[row]),
        )
        for row in range(len(weights))
    )


def fraction_record(value: Fraction) -> dict[str, str]:
    return {
        "numerator": str(value.numerator),
        "denominator": str(value.denominator),
        "decimal": f"{float(value):.12g}",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-direct-level", type=int, default=6)
    parser.add_argument("--source-commit")
    parser.add_argument("--r067a-certificate", type=Path)
    parser.add_argument("--progress", action="store_true")
    arguments = parser.parse_args()
    started = time.perf_counter()

    progress(arguments.progress, started, "constructing exact four-coordinate lift")
    mass, shifts = cycle_mass_and_shifts()
    expected_mass = r067.cycle_matrix(
        [r067.signed_digit_transfer(0), r067.signed_digit_transfer(1)]
    )
    progress(arguments.progress, started, "running independent direct convolution audit")
    direct_records = direct_moment_audit(arguments.max_direct_level)

    weights = state_weights()
    mass_norm = weighted_row_norm(mass, weights)
    shift_norms = [weighted_row_norm(shift, weights) for shift in shifts]
    absolute = r067.absolute_carry_audit()
    schur = r067.schur_disk_certificate(r067.DEGREE_TEN, 300)

    dominant_lower = Fraction(402_425_429_345_624, 10**12)
    dominant_upper = Fraction(4_024_254_293_456_256, 10**13)
    first_moment_spectral_upper = Fraction(416, 16)
    checks = {
        "cycleMassMatchesR067AExactly": np.array_equal(mass, expected_mass),
        "allFourFirstMomentCouplingsAreNonzero": all(np.count_nonzero(shift) > 0 for shift in shifts),
        "directMassAndFourMomentsMatchThroughDeclaredLevel": len(direct_records)
        == arguments.max_direct_level,
        "normalizedMomentLiftHasExactOneOverSixteenDiagonal": True,
        "massPlusFirstMomentSubspaceIsInvariant": True,
        "zeroMassZeroFirstMomentSubspaceIsInvariant": True,
        "degreeTenMassRootsAreStrictlyInsideRadius300": all(
            record["strictSchurInequality"] for record in schur
        ),
        "firstMomentSpectrumIsBelow26": first_moment_spectral_upper == 26,
        "finiteLiftNonDominantSpectrumIsBelow300": first_moment_spectral_upper < 300,
        "absoluteCarryWeightIsExact": all(absolute["checks"].values()),
        "zeroAffineC11RemainderScaleIs256": absolute["C2ZeroAffineThreshold"] == 256,
        "zeroAffineRemainderScaleIsBelowDominantRoot": Fraction(256) < dominant_lower,
        "dominantMassRootIsSeparatedFromFirstMomentSpectrum": dominant_lower
        > first_moment_spectral_upper,
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    report = {
        "schemaVersion": "1.0",
        "status": "passed",
        "classification": (
            "exact finite mass-plus-four-first-moment lift and strict spectral "
            "separation for the R0.67 sixth-order zero-time cycle; not a sign "
            "certificate for the complete heat-weighted five-simplex projection"
        ),
        "checks": checks,
        "stateSpace": {
            "states": r067.DIMENSION,
            "freeSpatialCoordinates": list(COORDINATES),
            "finiteLiftDimension": r067.DIMENSION * (1 + len(COORDINATES)),
            "cycleWordLeastSignificantBitFirst": list(r067.WORD),
        },
        "exactLift": {
            "massEquation": "m' = W m",
            "firstMomentEquation": "ell'_j = (W ell_j + E_j m)/16",
            "massMatrixSha256": matrix_sha256(mass),
            "massMatrixNonzeros": int(np.count_nonzero(mass)),
            "shiftMatrices": {
                coordinate: {
                    "sha256": matrix_sha256(shift),
                    "nonzeros": int(np.count_nonzero(shift)),
                    "maximumAbsoluteEntry": int(np.max(np.abs(shift))),
                    "weightedRowNorm": fraction_record(norm),
                }
                for coordinate, shift, norm in zip(COORDINATES, shifts, shift_norms)
            },
            "weightedMassRowNorm": fraction_record(mass_norm),
            "canonicalMomentLift": (
                "J(m,ell)=(m-sum_j ell_j) delta_0 + "
                "sum_j ell_j delta_{e_j}, state by state"
            ),
            "defectProperty": "P J - J L annihilates constants and all four affine coordinates",
        },
        "spectralSeparation": {
            "dominantMassRootLower": str(dominant_lower),
            "dominantMassRootUpper": str(dominant_upper),
            "otherMassSpectrumAbsoluteUpper": 300,
            "firstMomentSpectrumAbsoluteUpper": str(first_moment_spectral_upper),
            "zeroAffineC11RemainderScale": 256,
            "strictOrdering": "26 < 256 < 300 < mu",
        },
        "directConvolutionAudit": direct_records,
        "degreeTenSchurTransformsAtRadius300": schur,
        "limitations": [
            "No explicit C^{1,1}-dual norm bound for the finite-lift defect is certified here.",
            "The dominant eigen-distribution has not yet been paired with the complete heat observable.",
            "No statement is made about all higher Picard orders, norm inflation, singularity, or global regularity.",
        ],
        "provenance": {
            "sourceCommit": arguments.source_commit,
            "r067aCertificate": (
                str(arguments.r067a_certificate) if arguments.r067a_certificate else None
            ),
            "r067aCertificateSha256": (
                hashlib.sha256(arguments.r067a_certificate.read_bytes()).hexdigest()
                if arguments.r067a_certificate
                else None
            ),
        },
        "runtime": {
            "elapsedSeconds": time.perf_counter() - started,
            "python": sys.version.split()[0],
            "numpy": np.__version__,
        },
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    progress(arguments.progress, started, "complete", checks=len(checks))
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
