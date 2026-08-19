#!/usr/bin/env python3
"""R0.56 exact audit for the triad-adapted Leray polarization kernel.

For nonzero, noncollinear frequencies p, q, k=p+q, the ordered critical
Fourier--Leray symbol

    K_(p,q)(a,b) = |k|^-1 P_k[(q dot a)b],
    a perpendicular to p, b perpendicular to q,

has an exact two-channel representation in the triad-adapted
Craya--Herring frame.  The normal output channel has gain

    g_normal^2 = |p cross q|^2 / (|p|^2 |k|^2),

and the in-plane output channel has gain

    g_planar^2 = |p cross q|^2 (q dot k)^2
                   / (|p|^2 |q|^2 |k|^4).

The normal channel can attain one at arbitrary high--high-to-low scale
separation.  If epsilon=|k|/|p| <= rho < 1, the planar channel satisfies

    g_planar <= |q|/(2|p|) <= (1+rho)/2 < 1,

and the limiting constant 1/2 is sharp.  Thus the R0.55 saturation is
confined to one polarization channel; angular resolution alone does not
produce shell decay for that channel.

The frame decomposition is standard triad geometry closely related to the
Craya--Herring and helical decompositions.  The research contribution being
audited is the exact scale-critical channel norm, its equality
classification, and the high--high-to-low one-channel obstruction/gap.

All displayed identities and inequalities are analytic statements.  The
finite integer loops below are exact implementation regressions, not proofs
of the all-frequency theorems.  Nothing in this audit proves global
regularity or excludes finite-time singularity for three-dimensional
Navier--Stokes.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
from typing import Iterable


IntVector = tuple[int, int, int]
Rational = Fraction
RatVector = tuple[Rational, Rational, Rational]
PROGRESS_LOG: Path | None = None


def add(left: IntVector, right: IntVector) -> IntVector:
    return tuple(left[index] + right[index] for index in range(3))  # type: ignore[return-value]


def dot(left: IntVector, right: IntVector) -> int:
    return sum(left[index] * right[index] for index in range(3))


def cross(left: IntVector, right: IntVector) -> IntVector:
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def norm_squared(value: IntVector) -> int:
    return dot(value, value)


def rat_vector(value: IntVector) -> RatVector:
    return tuple(Rational(entry) for entry in value)  # type: ignore[return-value]


def rat_add(left: RatVector, right: RatVector) -> RatVector:
    return tuple(left[index] + right[index] for index in range(3))  # type: ignore[return-value]


def rat_subtract(left: RatVector, right: RatVector) -> RatVector:
    return tuple(left[index] - right[index] for index in range(3))  # type: ignore[return-value]


def rat_scale(factor: Rational, value: RatVector) -> RatVector:
    return tuple(factor * entry for entry in value)  # type: ignore[return-value]


def rat_dot(left: RatVector, right: RatVector) -> Rational:
    return sum((left[index] * right[index] for index in range(3)), Rational(0))


def rat_norm_squared(value: RatVector) -> Rational:
    return rat_dot(value, value)


def leray_project(frequency: RatVector, value: RatVector) -> RatVector:
    denominator = rat_norm_squared(frequency)
    if denominator == 0:
        raise ValueError("the Leray projector requires a nonzero frequency")
    return rat_subtract(
        value,
        rat_scale(rat_dot(frequency, value) / denominator, frequency),
    )


def ordered_symbol(
    left_frequency: IntVector,
    right_frequency: IntVector,
    left_polarization: IntVector,
    right_polarization: IntVector,
) -> RatVector:
    output = rat_vector(add(left_frequency, right_frequency))
    left = rat_vector(left_polarization)
    right = rat_vector(right_polarization)
    coefficient = rat_dot(rat_vector(right_frequency), left)
    return rat_scale(coefficient, leray_project(output, right))


def symmetrized_symbol(
    left_frequency: IntVector,
    right_frequency: IntVector,
    left_polarization: IntVector,
    right_polarization: IntVector,
) -> RatVector:
    output = rat_vector(add(left_frequency, right_frequency))
    left = rat_vector(left_polarization)
    right = rat_vector(right_polarization)
    unprojected = rat_add(
        rat_scale(rat_dot(rat_vector(right_frequency), left), right),
        rat_scale(rat_dot(rat_vector(left_frequency), right), left),
    )
    return leray_project(output, unprojected)


def rational_record(value: Rational) -> dict[str, str]:
    return {
        "numerator": str(value.numerator),
        "denominator": str(value.denominator),
        "decimal": format(float(value), ".17g"),
    }


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(
            f"[R0.56 +{elapsed:8.2f}s] {stage}{suffix}",
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
        if len(source_commit) != 40 or any(
            character not in "0123456789abcdef" for character in source_commit
        ):
            raise AssertionError("--source-commit must be a full lowercase hash")
        if head != source_commit:
            raise AssertionError("the checked-out HEAD does not match --source-commit")
    return {
        "sourceCommit": source_commit or head,
        "head": head,
        "worktreeStatusAtRun": status,
    }


def channel_invariants(left: IntVector, right: IntVector) -> dict[str, object]:
    output = add(left, right)
    left_squared = norm_squared(left)
    right_squared = norm_squared(right)
    output_squared = norm_squared(output)
    if left_squared == 0 or right_squared == 0 or output_squared == 0:
        raise ValueError("all three frequencies must be nonzero")
    cross_squared = norm_squared(cross(left, right))
    if cross_squared == 0:
        raise ValueError("the triad-adapted frame requires a noncollinear triad")
    left_output_dot = dot(left, output)
    right_output_dot = dot(right, output)

    if left_squared * output_squared - left_output_dot**2 != cross_squared:
        raise AssertionError("left/output Gram identity failed")
    if right_squared * output_squared - right_output_dot**2 != cross_squared:
        raise AssertionError("right/output Gram identity failed")

    normal_squared = Rational(
        cross_squared,
        left_squared * output_squared,
    )
    planar_squared = Rational(
        cross_squared * right_output_dot**2,
        left_squared * right_squared * output_squared**2,
    )
    reverse_normal_squared = Rational(
        cross_squared,
        right_squared * output_squared,
    )
    reverse_planar_squared = Rational(
        cross_squared * left_output_dot**2,
        left_squared * right_squared * output_squared**2,
    )
    symmetric_planar_coefficient_squared = Rational(
        cross_squared * (right_squared - left_squared) ** 2,
        left_squared * right_squared * output_squared**2,
    )

    if not Rational(0) < normal_squared <= Rational(1):
        raise AssertionError("the normal channel must lie in (0,1]")
    if not Rational(0) <= planar_squared < normal_squared:
        raise AssertionError("the planar channel must be strictly below the normal channel")
    if Rational(4) * left_squared * planar_squared > right_squared:
        raise AssertionError("the exact planar half-sum bound failed")

    return {
        "output": output,
        "leftSquared": left_squared,
        "rightSquared": right_squared,
        "outputSquared": output_squared,
        "crossSquared": cross_squared,
        "leftOutputDot": left_output_dot,
        "rightOutputDot": right_output_dot,
        "normalGainSquared": normal_squared,
        "planarGainSquared": planar_squared,
        "reverseNormalGainSquared": reverse_normal_squared,
        "reversePlanarGainSquared": reverse_planar_squared,
        "symmetricPlanarCoefficientSquared": symmetric_planar_coefficient_squared,
    }


def projection_channel_check(left: IntVector, right: IntVector) -> None:
    invariants = channel_invariants(left, right)
    left_squared = int(invariants["leftSquared"])
    right_squared = int(invariants["rightSquared"])
    output_squared = int(invariants["outputSquared"])
    left_right_dot = dot(left, right)

    left_tangent = tuple(
        left_squared * right[index] - left_right_dot * left[index]
        for index in range(3)
    )
    normal = cross(left, right)
    right_tangent = tuple(
        right_squared * left[index] - left_right_dot * right[index]
        for index in range(3)
    )

    if dot(left, left_tangent) != 0 or dot(right, right_tangent) != 0:
        raise AssertionError("constructed input tangent is not divergence free")
    if dot(right, normal) != 0 or dot(add(left, right), normal) != 0:
        raise AssertionError("triad normal is not transverse")

    for polarization, expected_key in (
        (normal, "normalGainSquared"),
        (right_tangent, "planarGainSquared"),
    ):
        symbol = ordered_symbol(left, right, left_tangent, polarization)
        ratio_squared = rat_norm_squared(symbol) / (
            Rational(output_squared)
            * Rational(norm_squared(left_tangent))
            * Rational(norm_squared(polarization))
        )
        if ratio_squared != invariants[expected_key]:
            raise AssertionError(f"projected {expected_key} formula failed")


def symmetrized_channel_check(left: IntVector, right: IntVector) -> None:
    invariants = channel_invariants(left, right)
    output_squared = int(invariants["outputSquared"])
    left_squared = int(invariants["leftSquared"])
    right_squared = int(invariants["rightSquared"])
    left_right_dot = dot(left, right)
    left_tangent = tuple(
        left_squared * right[index] - left_right_dot * left[index]
        for index in range(3)
    )
    right_tangent = tuple(
        right_squared * left[index] - left_right_dot * right[index]
        for index in range(3)
    )
    normal = cross(left, right)

    cases = (
        (
            left_tangent,
            normal,
            "normalGainSquared",
        ),
        (
            normal,
            right_tangent,
            "reverseNormalGainSquared",
        ),
        (
            left_tangent,
            right_tangent,
            "symmetricPlanarCoefficientSquared",
        ),
    )
    for left_polarization, right_polarization, expected_key in cases:
        symbol = symmetrized_symbol(
            left,
            right,
            left_polarization,
            right_polarization,
        )
        ratio_squared = rat_norm_squared(symbol) / (
            Rational(output_squared)
            * Rational(norm_squared(left_polarization))
            * Rational(norm_squared(right_polarization))
        )
        if ratio_squared != invariants[expected_key]:
            raise AssertionError(f"symmetrized {expected_key} formula failed")


def integer_vectors(radius: int) -> list[IntVector]:
    if radius < 1:
        raise ValueError("cube radius must be positive")
    return [
        (first, second, third)
        for first in range(-radius, radius + 1)
        for second in range(-radius, radius + 1)
        for third in range(-radius, radius + 1)
        if (first, second, third) != (0, 0, 0)
    ]


def exhaustive_regression(radius: int) -> dict[str, object]:
    vectors = integer_vectors(radius)
    checked = 0
    collinear = 0
    zero_output = 0
    saturation_count = 0
    projection_checks = 0
    symmetrized_projection_checks = 0
    separated_count = 0
    maximum_normal = Rational(0)
    maximum_planar = Rational(0)
    maximum_separated_planar = Rational(0)
    digest = hashlib.sha256()

    for left in vectors:
        for right in vectors:
            output = add(left, right)
            if output == (0, 0, 0):
                zero_output += 1
                continue
            if cross(left, right) == (0, 0, 0):
                collinear += 1
                continue
            invariants = channel_invariants(left, right)
            normal = invariants["normalGainSquared"]
            planar = invariants["planarGainSquared"]
            assert isinstance(normal, Rational)
            assert isinstance(planar, Rational)
            maximum_normal = max(maximum_normal, normal)
            maximum_planar = max(maximum_planar, planar)
            if normal == 1:
                saturation_count += 1
            if 64 * int(invariants["outputSquared"]) <= int(invariants["leftSquared"]):
                separated_count += 1
                maximum_separated_planar = max(maximum_separated_planar, planar)
                if planar > Rational(81, 256):
                    raise AssertionError("rho=1/8 planar gap failed")
            if projection_checks < 4096:
                projection_channel_check(left, right)
                projection_checks += 1
            if symmetrized_projection_checks < 4096:
                symmetrized_channel_check(left, right)
                symmetrized_projection_checks += 1
            digest.update(
                (
                    f"{left}:{right}:"
                    f"{normal.numerator}/{normal.denominator}:"
                    f"{planar.numerator}/{planar.denominator}:"
                    f"{invariants['symmetricPlanarCoefficientSquared']}\n"
                ).encode("ascii")
            )
            checked += 1

    if maximum_normal != 1 or saturation_count == 0:
        raise AssertionError("the finite cube did not contain an exact normal-channel saturation")
    return {
        "cubeRadius": radius,
        "integerVectors": len(vectors),
        "noncollinearOrderedTriadsChecked": checked,
        "collinearOrderedPairsSkipped": collinear,
        "zeroOutputPairsSkipped": zero_output,
        "directProjectionChecks": projection_checks,
        "directSymmetrizedProjectionChecks": symmetrized_projection_checks,
        "normalChannelSaturations": saturation_count,
        "maximumNormalGainSquared": rational_record(maximum_normal),
        "maximumPlanarGainSquared": rational_record(maximum_planar),
        "rhoOneEighthTriads": separated_count,
        "rhoOneEighthMaximumPlanarGainSquared": rational_record(
            maximum_separated_planar
        ),
        "rhoOneEighthFormalUpperGain": rational_record(Rational(9, 16)),
        "rhoOneEighthFormalUpperGainSquared": rational_record(Rational(81, 256)),
        "recordsSha256": digest.hexdigest(),
        "classification": "finite exhaustive exact integer regression",
    }


def family_regression(maximum_index: int) -> dict[str, object]:
    if maximum_index < 2:
        raise ValueError("maximum family index must be at least two")
    selected = {1, 2, 4, 8, 16, 32, 64, 128, 1024, maximum_index}
    saturation_records: list[dict[str, object]] = []
    half_limit_records: list[dict[str, object]] = []
    digest = hashlib.sha256()
    previous_half_limit = Rational(1)

    for index in range(1, maximum_index + 1):
        saturation = channel_invariants(
            (index, 0, 0),
            (-index, 1, 0),
        )
        if saturation["normalGainSquared"] != 1:
            raise AssertionError("normal saturation family failed")
        if saturation["planarGainSquared"] != Rational(1, index * index + 1):
            raise AssertionError("saturation-family planar formula failed")
        if saturation["symmetricPlanarCoefficientSquared"] != Rational(
            1, index * index + 1
        ):
            raise AssertionError("symmetric planar coefficient formula failed")

        half_limit = channel_invariants(
            (index, index, 0),
            (-index - 1, -index, 0),
        )
        expected_half = Rational(
            (index + 1) ** 2,
            2 * (2 * index * index + 2 * index + 1),
        )
        if half_limit["normalGainSquared"] != Rational(1, 2):
            raise AssertionError("half-limit normal formula failed")
        if half_limit["planarGainSquared"] != expected_half:
            raise AssertionError("half-limit planar formula failed")
        if not Rational(1, 4) < expected_half <= previous_half_limit:
            raise AssertionError("half-limit family is not decreasing to one quarter")
        previous_half_limit = expected_half

        digest.update(
            (
                f"{index}:1/{index * index + 1}:"
                f"{expected_half.numerator}/{expected_half.denominator}\n"
            ).encode("ascii")
        )
        if index in selected:
            saturation_records.append(
                {
                    "N": index,
                    "normalGainSquared": rational_record(Rational(1)),
                    "planarGainSquared": rational_record(
                        Rational(1, index * index + 1)
                    ),
                    "inputOutputSeparationLowerBound": str(index),
                }
            )
            half_limit_records.append(
                {
                    "N": index,
                    "normalGainSquared": rational_record(Rational(1, 2)),
                    "planarGainSquared": rational_record(expected_half),
                    "excessAboveOneQuarter": rational_record(
                        expected_half - Rational(1, 4)
                    ),
                }
            )

    return {
        "maximumIndex": maximum_index,
        "familiesChecked": 2 * maximum_index,
        "saturationFamily": {
            "pN": "(N,0,0)",
            "qN": "(-N,1,0)",
            "k": "(0,1,0)",
            "normalGainSquared": "1",
            "planarGainSquared": "1/(N^2+1)",
            "records": saturation_records,
        },
        "halfLimitFamily": {
            "pN": "(N,N,0)",
            "qN": "(-N-1,-N,0)",
            "k": "(-1,0,0)",
            "normalGainSquared": "1/2",
            "planarGainSquared": "(N+1)^2/[2(2N^2+2N+1)]",
            "planarGainSquaredLimit": rational_record(Rational(1, 4)),
            "planarGainLimit": rational_record(Rational(1, 2)),
            "records": half_limit_records,
        },
        "recordsSha256": digest.hexdigest(),
        "classification": "finite exact regressions of two all-index families",
    }


def construct_certificate(
    cube_radius: int,
    maximum_family_index: int,
    source_commit: str | None,
    show_progress: bool,
) -> dict[str, object]:
    started = time.perf_counter()
    progress(
        show_progress,
        started,
        "checking exhaustive integer triad channels",
        cubeRadius=cube_radius,
    )
    exhaustive = exhaustive_regression(cube_radius)
    progress(
        show_progress,
        started,
        "checking the saturation and half-limit families",
        maximumIndex=maximum_family_index,
    )
    families = family_regression(maximum_family_index)

    checks = {
        "formalTriadFrameIsRotationCovariant": True,
        "formalOrderedKernelHasTwoTransverseOutputChannels": True,
        "formalNormalGainSquaredFormula": True,
        "formalPlanarGainSquaredFormula": True,
        "formalNormalGainAtMostOne": True,
        "formalPlanarGainStrictlyBelowNormalForNoncollinearTriads": True,
        "formalPlanarHighHighLowBound": True,
        "formalPlanarLimitOneHalfIsSharp": True,
        "formalNormalChannelAngularProfileHasNoShellDecay": True,
        "formalNearSaturationSolidAngleFormula": True,
        "formalSymmetrizedChannelFormula": True,
        "formalNormalChannelSaturationPersistsAfterSymmetrization": True,
        "finiteExhaustiveIntegerRegressionPassed": exhaustive[
            "noncollinearOrderedTriadsChecked"
        ]
        > 0,
        "finiteDirectProjectionRegressionPassed": exhaustive[
            "directProjectionChecks"
        ]
        > 0,
        "finiteDirectSymmetrizedProjectionRegressionPassed": exhaustive[
            "directSymmetrizedProjectionChecks"
        ]
        > 0,
        "finiteNormalSaturationFound": exhaustive[
            "maximumNormalGainSquared"
        ]["numerator"]
        == "1"
        and exhaustive["maximumNormalGainSquared"]["denominator"] == "1",  # type: ignore[index]
        "finiteAllIndexFamilyRegressionsPassed": families["familiesChecked"]
        == 2 * maximum_family_index,
        "standardCrayaHerringAndHelicalPriorArtAcknowledged": True,
        "finiteChecksAreNotUsedAsProofs": True,
        "noLargeDataClosureClaimed": True,
        "threeDimensionalNavierStokesRegularityNotClaimed": True,
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise AssertionError("R0.56 checks failed: " + ", ".join(failed))
    progress(
        show_progress,
        started,
        "all channel and scope checks passed",
        checks=len(checks),
        triads=exhaustive["noncollinearOrderedTriadsChecked"],
    )

    return {
        "schemaVersion": "1.0",
        "scope": {
            "system": "three-dimensional incompressible Navier-Stokes Fourier-Leray triads",
            "theorems": [
                "exact two-channel triad-adapted decomposition of the ordered critical symbol",
                "a strict planar-polarization gap in high-high-to-low interactions",
                "a one-channel high-high-to-low saturation and angular no-shell-decay obstruction",
                "an exact triad-frame formula for the symmetrized cross interaction",
            ],
            "notClaimed": [
                "invention of the Craya-Herring or helical decomposition",
                "a closed anisotropic Banach algebra for the full PDE",
                "a favorable bound for the remaining normal polarization channel",
                "a bridge from arbitrary data to the R0.54 charge-degree generator",
                "large-data global regularity or exclusion of finite-time singularity",
                "a solution of the three-dimensional Navier-Stokes millennium problem",
            ],
        },
        "literatureBoundary": {
            "standardGeometry": (
                "two transverse Fourier polarizations and helical triad decompositions are classical; see Craya-Herring and Waleffe"
            ),
            "waleffeDoi": "https://doi.org/10.1063/1.858309",
            "crayaReviewDoi": "https://doi.org/10.1016/j.crme.2017.05.004",
            "classification": "prior art; not claimed as new",
        },
        "triadFrame": {
            "normal": "n=(p cross q)/|p cross q|",
            "inputTangents": [
                "t_p=n cross p_hat",
                "t_q=n cross q_hat",
            ],
            "outputTangent": "t_k=n cross k_hat",
            "leftPolarization": "a=a_n*n+a_t*t_p",
            "rightPolarization": "b=b_n*n+b_t*t_q",
            "classification": "formal rotation-covariant orthonormal frame",
        },
        "orderedKernel": {
            "definition": "K_(p,q)(a,b)=|k|^-1 P_k[(q dot a)b]",
            "decomposition": (
                "K_(p,q)(a,b)=g_N*a_t*b_n*n + g_T_signed*a_t*b_t*t_k"
            ),
            "normalGain": "g_N=|p cross q|/(|p||k|)=sin angle(p,k)",
            "planarGain": (
                "|g_T_signed|=g_N*|q_hat dot k_hat|"
            ),
            "operatorNorm": "||K_(p,q)||=g_N<=1",
            "equality": "g_N=1 iff p dot k=0",
            "classification": "formal all-frequency exact identity",
        },
        "highHighToLow": {
            "parameters": (
                "epsilon=|k|/|p|, mu=p_hat dot k_hat, q=k-p"
            ),
            "normalGain": "sqrt(1-mu^2), independent of epsilon",
            "planarGain": (
                "sqrt(1-mu^2)*|epsilon-mu|/sqrt(1+epsilon^2-2epsilon*mu)"
            ),
            "planarBound": (
                "g_planar<=|q|/(2|p|)<=(1+epsilon)/2; hence <=(1+rho)/2 for epsilon<=rho<1"
            ),
            "sharpPlanarLimit": "sup_mu g_planar -> 1/2 as epsilon -> 0",
            "normalAngularMoment": (
                "average_(S^2) g_normal^s = sqrt(pi)*Gamma(1+s/2)/(2*Gamma(3/2+s/2)), s>-2"
            ),
            "normalAngularMean": "pi/4",
            "normalAngularMeanSquare": rational_record(Rational(2, 3)),
            "nearSaturationMeasure": (
                "normalized solid angle of {g_normal>=1-delta} is sqrt(2*delta-delta^2)"
            ),
            "classification": "formal exact identities and sharp asymptotic inequality",
        },
        "symmetrizedKernel": {
            "definition": (
                "S=|k|^-1 P_k[(q dot a)b+(p dot b)a]"
            ),
            "normalCoefficient": "g_p*a_t*b_n-g_q*a_n*b_t",
            "planarCoefficient": (
                "a_t*b_t*|p cross q|*(|q|^2-|p|^2)/(|p||q||k|^2)"
            ),
            "saturationSurvives": (
                "for p_N=(N,0,0), q_N=(-N,1,0), a=t_p, b=n, the reverse term vanishes and |S|=1"
            ),
            "classification": "formal exact triad-frame identity",
        },
        "finiteRegressions": {
            "exhaustiveCube": exhaustive,
            "allIndexFamilies": families,
        },
        "researchDecision": {
            "finiteDirectionResolvedKernel": "passes exactly with two output channels",
            "planarHighHighLowChannel": "strict gap; cannot carry the R0.55 constant-one obstruction",
            "normalHighHighLowChannel": (
                "remains critical and has no shell decay under pure angular averaging"
            ),
            "nextRequiredStructure": [
                "phase or sign cancellation across different triads in the normal channel",
                "time/heat organization of the normal channel",
                "a norm that couples rather than separately envelopes directional cells",
            ],
            "notEnoughForRegularity": True,
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
    parser.add_argument("--cube-radius", type=int, default=5)
    parser.add_argument("--max-family-index", type=int, default=200_000)
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
        arguments.cube_radius,
        arguments.max_family_index,
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
                    "triads": certificate["finiteRegressions"]["exhaustiveCube"][  # type: ignore[index]
                        "noncollinearOrderedTriadsChecked"
                    ],
                    "families": certificate["finiteRegressions"]["allIndexFamilies"][  # type: ignore[index]
                        "familiesChecked"
                    ],
                },
                sort_keys=True,
            ),
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
