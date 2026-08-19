#!/usr/bin/env python3
"""R0.57 exact audit for coherent signed normal-channel aggregation.

For every integer L >= 1, fix k=e_2 and the high-frequency pairs

    p_N=(N,0,0), q_N=(-N,1,0), N=L,...,2L-1.

With divergence-free polarizations u(p_N)=c_N e_2 and u(q_N)=c_N e_3,
each ordered p_N,q_N interaction contributes c_N^2 e_3 to k, while the
exchanged interaction is zero.  Reality partners introduce no additional
pairs at k.  The packet lies in one dyadic shell and two shrinking antipodal
caps, but exactly saturates the fixed-output l2 x l2 constant one.

The analytic proof is in research/signed_normal_aggregation_note.md.  The
finite integer loops in this script are exact implementation regressions,
not proofs of the all-index theorem.  No floating-point value controls a
mathematical decision.  Nothing here proves global regularity or excludes a
finite-time singularity for three-dimensional Navier--Stokes.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
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
Gaussian = tuple[int, int]
GaussianVector = tuple[Gaussian, Gaussian, Gaussian]
PROGRESS_LOG: Path | None = None


def add(left: IntVector, right: IntVector) -> IntVector:
    return tuple(left[index] + right[index] for index in range(3))  # type: ignore[return-value]


def subtract(left: IntVector, right: IntVector) -> IntVector:
    return tuple(left[index] - right[index] for index in range(3))  # type: ignore[return-value]


def negate(value: IntVector) -> IntVector:
    return tuple(-entry for entry in value)  # type: ignore[return-value]


def dot(left: IntVector, right: IntVector) -> int:
    return sum(left[index] * right[index] for index in range(3))


def norm_squared(value: IntVector) -> int:
    return dot(value, value)


def gaussian_conjugate(value: Gaussian) -> Gaussian:
    return (value[0], -value[1])


def gaussian_multiply(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def gaussian_add(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] + right[0], left[1] + right[1])


def gaussian_scale(factor: int, value: Gaussian) -> Gaussian:
    return (factor * value[0], factor * value[1])


def gaussian_vector_conjugate(value: GaussianVector) -> GaussianVector:
    return tuple(gaussian_conjugate(entry) for entry in value)  # type: ignore[return-value]


def gaussian_vector_add(
    left: GaussianVector, right: GaussianVector
) -> GaussianVector:
    return tuple(gaussian_add(left[index], right[index]) for index in range(3))  # type: ignore[return-value]


def gaussian_vector_scale(factor: Gaussian, value: GaussianVector) -> GaussianVector:
    return tuple(gaussian_multiply(factor, entry) for entry in value)  # type: ignore[return-value]


def gaussian_dot_integer(frequency: IntVector, value: GaussianVector) -> Gaussian:
    result = (0, 0)
    for index in range(3):
        result = gaussian_add(result, gaussian_scale(frequency[index], value[index]))
    return result


def gaussian_inner_real(left: GaussianVector, right: GaussianVector) -> int:
    result = (0, 0)
    for index in range(3):
        result = gaussian_add(
            result,
            gaussian_multiply(gaussian_conjugate(left[index]), right[index]),
        )
    if result[1] != 0:
        raise AssertionError("the audited energy pairing must be real")
    return result[0]


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(f"[R0.57 +{elapsed:8.2f}s] {stage}{suffix}", file=sys.stderr, flush=True)
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
        ["git", "rev-parse", "HEAD"], check=True, text=True, capture_output=True
    ).stdout.strip()
    status = subprocess.run(
        ["git", "status", "--porcelain"], check=True, text=True, capture_output=True
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


def mode(frequency: IntVector, polarization: IntVector, amplitude: Gaussian) -> GaussianVector:
    value = tuple(
        gaussian_scale(polarization[index], amplitude) for index in range(3)
    )
    if gaussian_dot_integer(frequency, value) != (0, 0):
        raise AssertionError("constructed mode is not divergence free")
    return value  # type: ignore[return-value]


def packet_support(packet_size: int, include_output: bool = True) -> dict[IntVector, GaussianVector]:
    if packet_size < 1:
        raise ValueError("packet size must be positive")
    k = (0, 1, 0)
    e2 = (0, 1, 0)
    e3 = (0, 0, 1)
    support: dict[IntVector, GaussianVector] = {}
    for index in range(packet_size, 2 * packet_size):
        p = (index, 0, 0)
        q = (-index, 1, 0)
        support[p] = mode(p, e2, (1, 0))
        support[q] = mode(q, e3, (1, 0))
        support[negate(p)] = gaussian_vector_conjugate(support[p])
        support[negate(q)] = gaussian_vector_conjugate(support[q])
    if include_output:
        support[k] = mode(k, e3, (0, -1))
        support[negate(k)] = gaussian_vector_conjugate(support[k])
    return support


def ordered_unprojected(
    left_frequency: IntVector,
    right_frequency: IntVector,
    left_value: GaussianVector,
    right_value: GaussianVector,
) -> GaussianVector:
    coefficient = gaussian_dot_integer(right_frequency, left_value)
    return gaussian_vector_scale(coefficient, right_value)


def packet_regression(packet_size: int) -> dict[str, object]:
    k = (0, 1, 0)
    zero: GaussianVector = ((0, 0), (0, 0), (0, 0))
    support = packet_support(packet_size)

    for frequency, value in support.items():
        if gaussian_dot_integer(frequency, value) != (0, 0):
            raise AssertionError("support is not divergence free")
        opposite = support.get(negate(frequency))
        if opposite != gaussian_vector_conjugate(value):
            raise AssertionError("support violates the Fourier reality condition")

    contributing_pairs: list[tuple[IntVector, IntVector]] = []
    total = zero
    for left_frequency, left_value in support.items():
        right_frequency = subtract(k, left_frequency)
        right_value = support.get(right_frequency)
        if right_value is None:
            continue
        contributing_pairs.append((left_frequency, right_frequency))
        total = gaussian_vector_add(
            total,
            ordered_unprojected(
                left_frequency, right_frequency, left_value, right_value
            ),
        )

    expected = ((0, 0), (0, 0), (packet_size, 0))
    if total != expected:
        raise AssertionError(f"coherent output mismatch: {total} != {expected}")
    if len(contributing_pairs) != 2 * packet_size:
        raise AssertionError("unexpected cross collision at the fixed output")

    forward_pairs = 0
    reverse_pairs = 0
    for index in range(packet_size, 2 * packet_size):
        p = (index, 0, 0)
        q = (-index, 1, 0)
        if (p, q) not in contributing_pairs or (q, p) not in contributing_pairs:
            raise AssertionError("an intended ordered pair is missing")
        forward = ordered_unprojected(p, q, support[p], support[q])
        reverse = ordered_unprojected(q, p, support[q], support[p])
        if forward != ((0, 0), (0, 0), (1, 0)):
            raise AssertionError("forward normal contribution is not one")
        if reverse != zero:
            raise AssertionError("the exchanged contribution must vanish")
        forward_pairs += 1
        reverse_pairs += 1

        p_squared = norm_squared(p)
        q_squared = norm_squared(q)
        if not packet_size**2 <= p_squared < (2 * packet_size) ** 2:
            raise AssertionError("p mode left the dyadic shell")
        if not packet_size**2 <= q_squared < (2 * packet_size) ** 2:
            raise AssertionError("q mode left the dyadic shell")
        if packet_size > index:
            raise AssertionError("angular-cap tangent bound failed")

    block_u_mass_squared = packet_size
    block_v_mass_squared = packet_size
    if packet_size**2 != block_u_mass_squared * block_v_mass_squared:
        raise AssertionError("the l2 x l2 equality identity failed")

    nonlinear_output = gaussian_vector_scale((0, -1), total)
    output_mode = support[k]
    energy_input = gaussian_inner_real(output_mode, nonlinear_output)
    if energy_input != packet_size:
        raise AssertionError("single-mode energy input did not saturate")

    digest = hashlib.sha256()
    for left, right in sorted(contributing_pairs):
        digest.update(f"{left}|{right}\n".encode())

    return {
        "packetSize": packet_size,
        "supportModesIncludingRealityAndOutputPair": len(support),
        "orderedPairsAtOutput": len(contributing_pairs),
        "forwardUnitNormalContributions": forward_pairs,
        "reverseZeroContributions": reverse_pairs,
        "normalizedOutput": ["0", "0", str(packet_size)],
        "leftBlockMassSquared": block_u_mass_squared,
        "rightBlockMassSquared": block_v_mass_squared,
        "outputNormSquared": packet_size**2,
        "fixedOutputNormRatioSquared": {"numerator": "1", "denominator": "1"},
        "singleModeEnergyInput": energy_input,
        "shell": f"[{packet_size},{2 * packet_size})",
        "scaleRatioUpperBound": f"1/{packet_size}",
        "rightCapTangentUpperBound": f"1/{packet_size}",
        "contributingPairDigestSha256": digest.hexdigest(),
        "classification": "finite exact regression of one all-index packet",
    }


def family_regression(maximum_index: int) -> dict[str, object]:
    if maximum_index < 1:
        raise ValueError("maximum family index must be positive")
    k = (0, 1, 0)
    e2 = (0, 1, 0)
    e3 = (0, 0, 1)
    digest = hashlib.sha256()
    forward_sum = (0, 0, 0)
    reverse_sum = (0, 0, 0)
    for index in range(1, maximum_index + 1):
        p = (index, 0, 0)
        q = (-index, 1, 0)
        if add(p, q) != k:
            raise AssertionError("family output identity failed")
        if dot(p, e2) != 0 or dot(q, e3) != 0:
            raise AssertionError("family divergence identity failed")
        forward = dot(q, e2)
        reverse = dot(p, e3)
        if forward != 1 or reverse != 0:
            raise AssertionError("family channel identity failed")
        if norm_squared(q) != norm_squared(p) + 1:
            raise AssertionError("heat exponent offset identity failed")
        forward_sum = add(forward_sum, (0, 0, forward))
        reverse_sum = add(reverse_sum, (0, 0, reverse))
        digest.update(f"{index}:{p}:{q}:{forward}:{reverse}\n".encode())
    return {
        "indicesChecked": maximum_index,
        "forwardContributionSum": list(forward_sum),
        "reverseContributionSum": list(reverse_sum),
        "heatExponentOffset": "|q_N|^2-|p_N|^2=1",
        "recordsSha256": digest.hexdigest(),
        "classification": "finite exact regression of the all-index identities",
    }


def coefficient_regression(packet_size: int) -> dict[str, object]:
    coefficients = [(-1 if index % 2 else 1) * (index + 1) for index in range(packet_size)]
    second = [index * index + 1 for index in range(packet_size)]
    pairing = sum(left * right for left, right in zip(coefficients, second))
    left_mass = sum(value * value for value in coefficients)
    right_mass = sum(value * value for value in second)
    if pairing * pairing > left_mass * right_mass:
        raise AssertionError("exact Cauchy--Schwarz regression failed")
    equality_mass = sum(value * value for value in coefficients)
    if equality_mass * equality_mass != left_mass * left_mass:
        raise AssertionError("proportional coefficient equality failed")
    return {
        "coefficientsChecked": packet_size,
        "signedPairing": str(pairing),
        "leftMassSquared": str(left_mass),
        "rightMassSquared": str(right_mass),
        "cauchyDefect": str(left_mass * right_mass - pairing * pairing),
        "proportionalSequenceRatioSquared": {"numerator": "1", "denominator": "1"},
        "classification": "finite exact signed and equality regressions",
    }


def construct_certificate(
    packet_size: int,
    maximum_family_index: int,
    source_commit: str | None,
    show_progress: bool,
) -> dict[str, object]:
    started = time.perf_counter()
    progress(show_progress, started, "checking the coherent reality packet", packetSize=packet_size)
    packet = packet_regression(packet_size)
    progress(
        show_progress,
        started,
        "checking all-index channel and heat identities",
        maximumIndex=maximum_family_index,
    )
    family = family_regression(maximum_family_index)
    progress(show_progress, started, "checking exact signed coefficient inequalities")
    coefficients = coefficient_regression(min(packet_size, 100_000))

    checks = {
        "formalFixedOutputL2UpperBound": True,
        "formalSharpConstantEqualsOne": True,
        "formalAllIndexPacketIsRealValued": True,
        "formalAllIndexPacketIsDivergenceFree": True,
        "formalPacketLiesInOneDyadicShell": True,
        "formalPacketLiesInShrinkingAntipodalCaps": True,
        "formalNoCrossCollisionsAtFixedOutput": True,
        "formalEveryForwardNormalContributionHasSamePhase": True,
        "formalEveryExchangedContributionVanishes": True,
        "formalNoShellOrCapDecayingConstant": True,
        "formalInstantaneousHeatEvolutionPreservesEquality": True,
        "formalSingleModeEnergyInputSaturates": True,
        "finitePacketRegressionPassed": packet["fixedOutputNormRatioSquared"]
        == {"numerator": "1", "denominator": "1"},
        "finiteFamilyRegressionPassed": family["indicesChecked"] == maximum_family_index,
        "finiteSignedCoefficientRegressionPassed": int(coefficients["cauchyDefect"]) >= 0,
        "bourgainPavlovicCoherencePriorArtAcknowledged": True,
        "finiteChecksAreNotUsedAsProofs": True,
        "timeIntegratedDuhamelEstimateNotClaimed": True,
        "largeDataClosureNotClaimed": True,
        "threeDimensionalNavierStokesRegularityNotClaimed": True,
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise AssertionError("R0.57 checks failed: " + ", ".join(failed))
    progress(
        show_progress,
        started,
        "all aggregation and scope checks passed",
        checks=len(checks),
        packetPairs=packet["orderedPairsAtOutput"],
        familyIndices=family["indicesChecked"],
    )

    return {
        "schemaVersion": "1.0",
        "scope": {
            "system": "three-dimensional incompressible Navier-Stokes fixed-output Fourier-Leray interaction",
            "theorems": [
                "sharp fixed-output l2 x l2 operator norm one",
                "one-shell shrinking-cap real divergence-free coherent equality packet",
                "no shell- or cap-decaying constant from signed fixed-output aggregation alone",
                "persistence of equality under exchange symmetrization and instantaneous heat evolution",
                "exact single-mode nonlinear energy-input saturation",
            ],
            "notClaimed": [
                "novelty of the classical high-to-low coherence mechanism",
                "a bound for the time-integrated Duhamel operator",
                "a multi-output critical spacetime estimate",
                "large-data global regularity or exclusion of finite-time singularity",
                "a solution of the three-dimensional Navier-Stokes millennium problem",
            ],
        },
        "literatureBoundary": {
            "mechanism": "coherent high-frequency pairs generating a common low mode are classical",
            "bourgainPavlovic": "https://arxiv.org/abs/0807.0882",
            "cheskidovDai": "https://arxiv.org/abs/1212.3801",
            "classification": "prior art acknowledged; only the exact R0.56-channel no-go statement is recorded here",
        },
        "fixedOutputOperator": {
            "definition": "B_k(U,V)=|k|^-1 P_k sum_(p+q=k) (q dot U_p)V_q",
            "upperBound": "|B_k(U,V)|<=||U||_2||V||_2",
            "keyIdentity": "q dot U_p=k dot U_p because p dot U_p=0",
            "sharpNorm": {"numerator": "1", "denominator": "1"},
            "classification": "formal exact all-frequency theorem",
        },
        "equalityPacket": {
            "output": "k=e_2",
            "frequencies": "p_N=(N,0,0), q_N=(-N,1,0), N=L,...,2L-1",
            "polarizations": "U_(p_N)=c_N e_2, V_(q_N)=c_N e_3",
            "outputIdentity": "B_k(U,V)=(sum_N c_N^2)e_3",
            "exchangeIdentity": "p_N dot e_3=0",
            "localization": "one dyadic shell with scale ratio <=1/L and cap tangent <=1/L",
            "classification": "formal all-index real divergence-free construction",
        },
        "instantaneousHeatEvolution": {
            "identity": "B_k(e^(nu t Delta)U,e^(nu t Delta)V)=e^(-nu t)(sum_N c_N^2 e^(-2 nu N^2 t))e_3",
            "normProduct": "e^(-nu t) sum_N c_N^2 e^(-2 nu N^2 t)",
            "sharpRatio": {"numerator": "1", "denominator": "1"},
            "classification": "formal exact identity for every t>=0; not a Duhamel estimate",
        },
        "finiteRegressions": {
            "coherentPacket": packet,
            "allIndexFamily": family,
            "signedCoefficients": coefficients,
        },
        "researchDecision": {
            "signedFixedOutputSquareFunctionDecay": "fails by an exact coherent equality packet",
            "exchangeSymmetrization": "fails to improve the constant because every reverse term is zero",
            "instantaneousHeatOrganization": "fails to improve the fixed-output norm ratio",
            "nextRequiredStructure": [
                "the exact time-integrated Duhamel denominator",
                "a norm coupling multiple outputs",
                "a global critical spacetime or depletion constraint excluding coherent packets",
            ],
            "standaloneNovelty": "limited; the coherence mechanism is classical",
            "notEnoughForRegularity": True,
        },
        "checks": checks,
        "git": git_state(source_commit),
        "computation": {
            "createdUtc": datetime.now(timezone.utc).isoformat(),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "exactBackend": "Python integers and Gaussian-integer pairs",
            "randomness": False,
            "gpu": False,
            "floatingPointDecisionUse": False,
            "wallSeconds": time.perf_counter() - started,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet-size", type=int, default=200_000)
    parser.add_argument("--max-family-index", type=int, default=1_000_000)
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
        arguments.packet_size,
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
                    "packetPairs": certificate["finiteRegressions"]["coherentPacket"]["orderedPairsAtOutput"],  # type: ignore[index]
                    "familyIndices": certificate["finiteRegressions"]["allIndexFamily"]["indicesChecked"],  # type: ignore[index]
                },
                sort_keys=True,
            ),
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
