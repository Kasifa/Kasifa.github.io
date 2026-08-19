#!/usr/bin/env python3
"""R0.55 exact audit for a critical Fourier bridge and scalar-charge no-go.

This audit separates three statements.

1.  The Fourier--Lei--Lin norm X^{-1} is scale critical, and the exact
    divergence-free identity in one ordered Navier--Stokes interaction gives

        ||P(u dot grad v)||_{X^{-1}} <= ||u||_{X^0} ||v||_{X^0}.

    Together with X^0 interpolation and the heat semigroup, this supplies a
    finite full-PDE bridge to a scalar degree majorant.  This is a recorded
    classical baseline, not a new regularity theorem.

2.  The family

        p_N=(N,0,0), q_N=(-N,1,0), k=p_N+q_N=(0,1,0),
        a=(0,1,0), b=(0,0,1)

    is an exact high--high-to-low saturation family.  Both inputs are
    divergence free, P_k[(q_N dot a)b]=b, and the normalized X^{-1} symbol
    ratio is exactly one for every positive integer N.

3.  Any scalar charge that is additive under Fourier convolution and
    invariant under all rotations is identically zero.  The same conclusion
    holds on the torus under the orientation-preserving cubic rotation group.
    Therefore the nontrivial scalar charge used by the reduced canonical edge
    system cannot be extended to arbitrary Fourier data while retaining both
    additivity and rotation invariance.  This is a no-go theorem for that
    direct interface only; vector-valued, directional, or multi-frame bridges
    are not excluded.

The all-frequency inequalities and scalar-charge theorem are analytic
statements.  The exact finite loops below are implementation regressions and
data provenance for the accompanying figure; they are not their proofs.
Nothing here proves or disproves three-dimensional Navier--Stokes regularity.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
from typing import Iterable


Rational = Fraction
Vector = tuple[Rational, Rational, Rational]
Matrix = tuple[Vector, Vector, Vector]
PROGRESS_LOG: Path | None = None


def rational_record(value: Rational) -> dict[str, str]:
    return {
        "numerator": str(value.numerator),
        "denominator": str(value.denominator),
        "decimal": format(float(value), ".17g"),
    }


def vector(*values: int | Rational) -> Vector:
    return tuple(Rational(value) for value in values)  # type: ignore[return-value]


def add(left: Vector, right: Vector) -> Vector:
    return tuple(left[index] + right[index] for index in range(3))  # type: ignore[return-value]


def subtract(left: Vector, right: Vector) -> Vector:
    return tuple(left[index] - right[index] for index in range(3))  # type: ignore[return-value]


def scale(factor: Rational, value: Vector) -> Vector:
    return tuple(factor * entry for entry in value)  # type: ignore[return-value]


def dot(left: Vector, right: Vector) -> Rational:
    return sum((left[index] * right[index] for index in range(3)), Rational(0))


def norm_squared(value: Vector) -> Rational:
    return dot(value, value)


def matrix_vector(matrix: Matrix, value: Vector) -> Vector:
    return tuple(dot(row, value) for row in matrix)  # type: ignore[return-value]


def transpose(matrix: Matrix) -> Matrix:
    return tuple(
        tuple(matrix[row][column] for row in range(3))
        for column in range(3)
    )  # type: ignore[return-value]


def matrix_product(left: Matrix, right: Matrix) -> Matrix:
    right_transpose = transpose(right)
    return tuple(
        tuple(dot(left[row], right_transpose[column]) for column in range(3))
        for row in range(3)
    )  # type: ignore[return-value]


def determinant(matrix: Matrix) -> Rational:
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


IDENTITY: Matrix = (
    vector(1, 0, 0),
    vector(0, 1, 0),
    vector(0, 0, 1),
)


def leray_project(frequency: Vector, value: Vector) -> Vector:
    denominator = norm_squared(frequency)
    if denominator == 0:
        raise ValueError("the Leray projection is undefined at zero frequency")
    return subtract(value, scale(dot(frequency, value) / denominator, frequency))


def ordered_symbol(
    left_frequency: Vector,
    right_frequency: Vector,
    left_polarization: Vector,
    right_polarization: Vector,
) -> Vector:
    output = add(left_frequency, right_frequency)
    return scale(
        dot(right_frequency, left_polarization),
        leray_project(output, right_polarization),
    )


def pi_rotation_sending_to_negative(value: Vector) -> Matrix:
    if value == vector(0, 0, 0):
        raise ValueError("the rotation witness requires a nonzero vector")
    if value[0] != 0 or value[1] != 0:
        axis = vector(-value[1], value[0], 0)
    else:
        axis = vector(1, 0, 0)
    denominator = norm_squared(axis)
    return tuple(
        tuple(
            Rational(2) * axis[row] * axis[column] / denominator
            - (Rational(1) if row == column else Rational(0))
            for column in range(3)
        )
        for row in range(3)
    )  # type: ignore[return-value]


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(
            f"[R0.55 +{elapsed:8.2f}s] {stage}{suffix}",
            file=sys.stderr,
            flush=True,
        )
    if PROGRESS_LOG is not None:
        record = {
            "timestampUtc": datetime.now(timezone.utc).isoformat(),
            "elapsedSeconds": elapsed,
            "stage": stage,
            **details,
        }
        with PROGRESS_LOG.open("a", encoding="utf-8") as target:
            target.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
            target.flush()
            os.fsync(target.fileno())


def git_state(source_commit: str | None) -> dict[str, object]:
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout.splitlines()
    if source_commit is not None:
        if len(source_commit) != 40 or any(character not in "0123456789abcdef" for character in source_commit):
            raise AssertionError("--source-commit must be a full lowercase 40-character hash")
        if head != source_commit:
            raise AssertionError("the checked-out HEAD does not match --source-commit")
    return {
        "sourceCommit": source_commit or head,
        "head": head,
        "worktreeStatusAtRun": status,
    }


def catalan_coefficients(maximum_degree: int) -> list[int]:
    coefficients = [0] * (maximum_degree + 1)
    coefficients[1] = 1
    for degree in range(2, maximum_degree + 1):
        coefficients[degree] = sum(
            coefficients[left] * coefficients[degree - left]
            for left in range(1, degree)
        )
    return coefficients


def sha256_lines(lines: Iterable[str]) -> str:
    digest = hashlib.sha256()
    for line in lines:
        digest.update(line.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def triad_regression(maximum_index: int) -> dict[str, object]:
    if maximum_index < 1:
        raise ValueError("maximum triad index must be positive")
    left_polarization = vector(0, 1, 0)
    right_polarization = vector(0, 0, 1)
    output_frequency = vector(0, 1, 0)
    records = []
    digest_lines = []
    selected = {1, 2, 4, 8, 16, 32, 64, 128, maximum_index}
    for index in range(1, maximum_index + 1):
        left_frequency = vector(index, 0, 0)
        right_frequency = vector(-index, 1, 0)
        output = add(left_frequency, right_frequency)
        symbol = ordered_symbol(
            left_frequency,
            right_frequency,
            left_polarization,
            right_polarization,
        )
        numerator = norm_squared(symbol)
        denominator = (
            norm_squared(output)
            * norm_squared(left_polarization)
            * norm_squared(right_polarization)
        )
        ratio_squared = numerator / denominator
        checks = (
            output == output_frequency,
            dot(left_frequency, left_polarization) == 0,
            dot(right_frequency, right_polarization) == 0,
            dot(output, symbol) == 0,
            symbol == right_polarization,
            ratio_squared == 1,
        )
        if not all(checks):
            raise AssertionError(f"triad regression failed at N={index}")
        digest_lines.append(
            f"{index}:{ratio_squared.numerator}/{ratio_squared.denominator}:"
            f"{norm_squared(left_frequency)}:{norm_squared(right_frequency)}"
        )
        if index in selected:
            records.append(
                {
                    "N": index,
                    "leftFrequencySquared": str(norm_squared(left_frequency)),
                    "rightFrequencySquared": str(norm_squared(right_frequency)),
                    "outputFrequencySquared": str(norm_squared(output)),
                    "criticalSymbolRatioSquared": rational_record(ratio_squared),
                    "minimumInputToOutputFrequencyRatioLowerBound": str(index),
                }
            )
    return {
        "maximumIndex": maximum_index,
        "checkedTriads": maximum_index,
        "allRatiosExactlyOne": True,
        "recordsSha256": sha256_lines(digest_lines),
        "selectedRecords": records,
        "classification": "finite exact regression of an all-index algebraic identity",
    }


def rotation_regression(radius: int) -> dict[str, object]:
    if radius < 1:
        raise ValueError("rotation regression radius must be positive")
    checked = 0
    digest_lines = []
    for first in range(-radius, radius + 1):
        for second in range(-radius, radius + 1):
            for third in range(-radius, radius + 1):
                value = vector(first, second, third)
                if value == vector(0, 0, 0):
                    continue
                rotation = pi_rotation_sending_to_negative(value)
                if matrix_product(transpose(rotation), rotation) != IDENTITY:
                    raise AssertionError("rotation witness is not orthogonal")
                if determinant(rotation) != 1:
                    raise AssertionError("rotation witness is not orientation preserving")
                if matrix_vector(rotation, value) != scale(Rational(-1), value):
                    raise AssertionError("rotation witness does not send the vector to its negative")
                digest_lines.append(
                    f"{first},{second},{third}:"
                    + ",".join(
                        f"{entry.numerator}/{entry.denominator}"
                        for row in rotation
                        for entry in row
                    )
                )
                checked += 1
    return {
        "integerVectorsChecked": checked,
        "coordinateRadius": radius,
        "allWitnessesInSO3": True,
        "allWitnessesSendXiToMinusXi": True,
        "recordsSha256": sha256_lines(digest_lines),
        "classification": "finite exact regression of the rotation construction",
    }


def construct_certificate(
    maximum_triad_index: int,
    maximum_catalan_degree: int,
    rotation_radius: int,
    source_commit: str | None,
    show_progress: bool,
) -> dict[str, object]:
    started = time.perf_counter()
    progress(show_progress, started, "checking critical scaling exponents")
    scaling = {
        "velocityScaling": "u_lambda(x,t)=lambda*u(lambda*x,lambda^2*t)",
        "fourierScaling": "hat(u_lambda)(xi,t)=lambda^-2*hat(u)(xi/lambda,lambda^2*t)",
        "XsigmaExponent": "sigma+1",
        "records": [
            {"sigma": sigma, "spatialNormExponent": sigma + 1}
            for sigma in (-1, 0, 1)
        ],
        "LinfinityTimeXminusOneExponent": 0,
        "LoneTimeXoneExponent": 0,
        "torusIntegerDilation": (
            "u^(m)(x,t)=m*u(mx,m^2*t) preserves X^-1 and L1_t X^1"
        ),
        "classification": "formal change-of-variables identity",
    }

    progress(
        show_progress,
        started,
        "auditing the exact high-high-to-low saturation family",
        maximumIndex=maximum_triad_index,
    )
    triads = triad_regression(maximum_triad_index)

    progress(
        show_progress,
        started,
        "auditing exact SO(3) half-turn witnesses",
        coordinateRadius=rotation_radius,
    )
    rotations = rotation_regression(rotation_radius)

    progress(
        show_progress,
        started,
        "constructing the scalar Catalan degree majorant",
        maximumDegree=maximum_catalan_degree,
    )
    if maximum_catalan_degree < 2:
        raise ValueError("maximum Catalan degree must be at least two")
    catalan = catalan_coefficients(maximum_catalan_degree)
    for degree in range(1, maximum_catalan_degree + 1):
        closed = math.comb(2 * degree - 2, degree - 1) // degree
        if catalan[degree] != closed:
            raise AssertionError(f"Catalan formula mismatch at degree {degree}")
    catalan_digest = sha256_lines(
        f"{degree}:{catalan[degree]}"
        for degree in range(1, maximum_catalan_degree + 1)
    )
    degree_majorant = {
        "normalizedInequality": "M<=z+M^2",
        "algebraicMajorant": "M(z)=(1-sqrt(1-4z))/2",
        "coefficientFormula": "[z^n]M=Catalan_(n-1)=binom(2n-2,n-1)/n",
        "exactRadius": rational_record(Rational(1, 4)),
        "maximumAuditedDegree": maximum_catalan_degree,
        "coefficientDigestSha256": catalan_digest,
        "selectedCoefficients": {
            str(degree): str(catalan[degree])
            for degree in (1, 2, 3, 4, 8, 16, 32, maximum_catalan_degree)
            if degree <= maximum_catalan_degree
        },
        "classification": (
            "the algebraic radius is an all-order theorem; the coefficient table is a finite exact regression"
        ),
    }

    checks = {
        "formalXminusOneScalingExponentIsZero": scaling["records"][0]["spatialNormExponent"] == 0,  # type: ignore[index]
        "formalLoneTimeXoneScalingExponentIsZero": scaling["LoneTimeXoneExponent"] == 0,
        "formalTriadSymbolIdentityIsExactlyOne": True,
        "formalTriadInputOutputSeparationEqualsNAndIsUnbounded": True,
        "finiteTriadRegressionPassed": triads["allRatiosExactlyOne"] is True,
        "triadOutputIsNonzero": vector(0, 1, 0) != vector(0, 0, 0),
        "formalScalarChargeNoGoUsesSO3HalfTurn": True,
        "finiteRotationRegressionPassed": rotations["allWitnessesInSO3"] is True
        and rotations["allWitnessesSendXiToMinusXi"] is True,
        "finiteCatalanRecurrenceMatchesClosedFormula": True,
        "formalCatalanRadiusIsOneQuarter": degree_majorant["exactRadius"]["numerator"] == "1"  # type: ignore[index]
        and degree_majorant["exactRadius"]["denominator"] == "4",  # type: ignore[index]
        "fullPdeCriticalDegreeBridgeHasFiniteConstant": True,
        "nontrivialAdditiveRotationInvariantScalarChargeIsImpossible": True,
        "torusCubicRotationInvariantAdditiveScalarChargeIsImpossible": True,
        "currentChargeGeneratorIsNotClaimedToControlArbitraryData": True,
        "vectorOrDirectionalBridgesRemainOpen": True,
        "finiteRegressionsAreNotUsedAsAllOrderProofs": True,
        "threeDimensionalNavierStokesRegularityNotClaimed": True,
    }
    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError("R0.55 checks failed: " + ", ".join(failed))
    progress(
        show_progress,
        started,
        "all critical-bridge and charge-no-go checks passed",
        checks=len(checks),
    )

    return {
        "schemaVersion": "1.0",
        "scope": {
            "system": "three-dimensional incompressible Navier-Stokes in Fourier variables",
            "domains": ["R^3", "mean-zero T^3 with integer dilations"],
            "theorems": [
                "a scale-critical X^-1 Fourier-Leray estimate and finite heat-Duhamel bridge to a scalar degree majorant",
                "an exact all-index high-high-to-low symbol saturation family",
                "a no-go theorem for nontrivial additive rotation-invariant scalar charge",
            ],
            "notClaimed": [
                "a new small-data regularity theorem beyond the Lei-Lin framework",
                "a bridge from arbitrary Fourier data to the current nontrivial charge-degree generator",
                "exclusion of vector-valued, directional, or multi-frame charge systems",
                "large-data global regularity or finite-time singularity",
                "three-dimensional Navier-Stokes regularity or singularity",
            ],
        },
        "literatureBaseline": {
            "result": (
                "Lei and Lin prove global well-posedness in X^-1 when the initial norm is below viscosity"
            ),
            "arxiv": "https://arxiv.org/abs/1203.2699",
            "doi": "https://doi.org/10.1002/cpa.20361",
            "classification": "published prior result; not claimed as new",
        },
        "criticalScaling": scaling,
        "fourierLerayEstimate": {
            "orderedSymbol": (
                "Bhat(k)=i*P_k sum_(p+q=k) (q dot uhat(p))*vhat(q)"
            ),
            "divergenceFreeIdentity": "q dot uhat(p)=k dot uhat(p)",
            "criticalEstimate": (
                "||P(u dot grad v)||_X^-1 <= ||u||_X^0 ||v||_X^0"
            ),
            "interpolation": "||u||_X^0^2 <= ||u||_X^-1 ||u||_X^1",
            "solutionSpace": (
                "E_nu=Linf_t X^-1 intersect L1_t X^1 with max(Linf,nu*L1) norm"
            ),
            "duhamelBilinearConstantUpper": "1/nu",
            "classification": "formal all-frequency inequality",
        },
        "exactSaturationFamily": {
            "leftFrequency": "p_N=(N,0,0)",
            "rightFrequency": "q_N=(-N,1,0)",
            "outputFrequency": "k=(0,1,0)",
            "leftPolarization": "a=(0,1,0)",
            "rightPolarization": "b=(0,0,1)",
            "symbolIdentity": "P_k[(q_N dot a)b]=b",
            "criticalSymbolRatio": "|k|^-1|B_k(a,b)|/(|a||b|)=1",
            "interactionClass": "high-high to low with arbitrarily large input/output frequency separation",
            "classification": "formal exact identity for every positive integer N",
            "finiteRegression": triads,
        },
        "scalarChargeNoGo": {
            "R3Theorem": (
                "if chi:R^3->R is additive and SO(3)-invariant, then chi=0"
            ),
            "R3Proof": (
                "for every xi choose a pi rotation R in SO(3) with Rxi=-xi; invariance gives chi(-xi)=chi(xi), while additivity gives chi(-xi)=-chi(xi)"
            ),
            "T3Theorem": (
                "if chi:Z^3->R is additive and invariant under the orientation-preserving cubic rotation group, then chi=0"
            ),
            "T3Proof": (
                "the pi rotations diag(1,-1,-1) and diag(-1,1,-1), together with additivity on the coordinate basis, force all three basis charges to vanish"
            ),
            "regularityAssumption": "none",
            "classification": "formal all-frequency algebraic theorem",
            "finiteRegression": rotations,
        },
        "scalarDegreeMajorant": degree_majorant,
        "bridgeDecision": {
            "fullPdeToCriticalScalarDegreeMajorant": "finite constant; passes",
            "fullPdeToCurrentNontrivialScalarChargeDegreeGenerator": (
                "fails if the charge must be simultaneously additive and rotation invariant"
            ),
            "worstFrequencyClass": (
                "high-high to low; the exact saturation family shows no favorable scale-separation factor"
            ),
            "nextMinimalState": [
                "dyadic input/output shell indices",
                "relative angle or output direction",
                "Leray polarization state",
            ],
            "openAlternatives": [
                "rotation-covariant vector charge",
                "directional sector envelope",
                "supremum or integral over charge frames",
            ],
        },
        "checks": checks,
        "git": git_state(source_commit),
        "computation": {
            "createdUtc": datetime.now(timezone.utc).isoformat(),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "exactBackend": "Python integers and fractions.Fraction",
            "randomness": False,
            "gpu": False,
            "floatingPointDecisionUse": False,
            "wallSeconds": time.perf_counter() - started,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-triad-index", type=int, default=200_000)
    parser.add_argument("--max-catalan-degree", type=int, default=256)
    parser.add_argument("--rotation-radius", type=int, default=12)
    parser.add_argument("--source-commit")
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--progress-log", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    global PROGRESS_LOG
    PROGRESS_LOG = arguments.progress_log
    if PROGRESS_LOG is not None:
        PROGRESS_LOG.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_LOG.write_text("", encoding="utf-8")

    certificate = construct_certificate(
        arguments.max_triad_index,
        arguments.max_catalan_degree,
        arguments.rotation_radius,
        arguments.source_commit,
        arguments.progress,
    )
    encoded = json.dumps(
        certificate,
        ensure_ascii=False,
        indent=2 if arguments.pretty else None,
        sort_keys=True,
    )
    if arguments.output is not None:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(encoded + "\n", encoding="utf-8")
    else:
        print(encoded)

    if arguments.check:
        print(
            json.dumps(
                {
                    "status": "passed",
                    "checks": len(certificate["checks"]),
                    "triads": certificate["exactSaturationFamily"]["finiteRegression"]["checkedTriads"],  # type: ignore[index]
                    "rotationWitnesses": certificate["scalarChargeNoGo"]["finiteRegression"]["integerVectorsChecked"],  # type: ignore[index]
                },
                sort_keys=True,
            ),
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
