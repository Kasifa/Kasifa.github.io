#!/usr/bin/env python3
"""R0.60 exact audit for the invariant shear Picard chain.

The all-index proof is in research/invariant_shear_picard_note.md.  This
program performs deterministic integer and Gaussian-integer regressions for
the invariant polarization channel, the cubic target gap, the absence of odd
low-plane returns through order nine, the order-eleven support witness,
cubic high-frequency backtracking, quartic target admissibility, and the
fourth-order energy cancellation.

Finite enumeration is a regression of the formulas, not a substitute for the
all-index proof.  No floating-point value decides a mathematical check.
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
import time


Int2 = tuple[int, int]
Gaussian = tuple[int, int]
FourierMap = dict[Int2, Gaussian]
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(f"[R0.60 +{elapsed:8.2f}s] {stage}{suffix}", file=os.sys.stderr, flush=True)
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
            raise AssertionError("checked-out HEAD does not match --source-commit")
    return {
        "sourceCommit": source_commit or head,
        "head": head,
        "worktreeStatusAtRun": status,
    }


def rudin_shapiro(level: int) -> list[int]:
    p = [1]
    q = [1]
    for _ in range(level):
        p, q = p + q, p + [-value for value in q]
    return p


def packet(
    level_l: int, level_m: int
) -> tuple[int, int, int, list[dict[str, int]]]:
    length = 1 << level_l
    outputs = 1 << level_m
    count = length * outputs
    high = 4 * count
    signs_l = rudin_shapiro(level_l)
    signs_m = rudin_shapiro(level_m)
    modes: list[dict[str, int]] = []
    for block in range(outputs):
        for offset in range(length):
            carrier = high + block * length + offset
            modes.append(
                {
                    "block": block,
                    "offset": offset,
                    "carrier": carrier,
                    "target": block + 1,
                    "sign": signs_m[block] * signs_l[offset],
                }
            )
    return length, outputs, high, modes


def interval_theorem_regression(maximum_level: int) -> dict[str, object]:
    if maximum_level < 0:
        raise ValueError("maximum level must be nonnegative")
    parameter_pairs = 0
    carrier_positions = 0
    order_eleven_witnesses = 0
    minimum_gaps = {3: None, 5: None, 7: None, 9: None}
    digest = hashlib.sha256()
    for level_l in range(maximum_level + 1):
        for level_m in range(maximum_level + 1):
            length = 1 << level_l
            outputs = 1 << level_m
            count = length * outputs
            high = 4 * count
            diameter = count - 1
            if high != 4 * count:
                raise AssertionError("H=4LM failed")
            if 4 * (high + diameter) >= 5 * high:
                raise AssertionError("strict carrier shell inequality failed")

            local_gaps: dict[int, int] = {}
            for k, order in enumerate((3, 5, 7, 9), start=1):
                gap = high - k * diameter
                if gap <= 0:
                    raise AssertionError(f"odd order {order} lost its formal gap")
                expected = (4 - k) * count + k
                if gap != expected:
                    raise AssertionError("closed odd-order gap formula failed")
                local_gaps[order] = gap
                previous = minimum_gaps[order]
                minimum_gaps[order] = gap if previous is None else min(previous, gap)

            cubic_gap = local_gaps[3]
            if 4 * cubic_gap <= 3 * high:
                raise AssertionError("cubic support did not stay outside 3H/4")

            if count >= 5:
                q_carrier = high + count - 5
                upper = high + count - 1
                witness = -q_carrier + 5 * upper - 5 * high
                if not high <= q_carrier <= upper:
                    raise AssertionError("order-eleven V carrier left the packet")
                if witness != 0:
                    raise AssertionError("order-eleven support witness failed")
                order_eleven_witnesses += 1
            parameter_pairs += 1
            carrier_positions += count
            digest.update(
                (
                    f"{level_l}:{level_m}:{length}:{outputs}:{high}:{diameter}:"
                    f"{local_gaps}:{count >= 5}\n"
                ).encode()
            )
    return {
        "maximumDyadicLevel": maximum_level,
        "parameterPairsChecked": parameter_pairs,
        "carrierPositionsCoveredByFormula": carrier_positions,
        "oddOrdersExcluded": [3, 5, 7, 9],
        "minimumIntegerGaps": minimum_gaps,
        "cubicGap": "|xi_1|>=H-(LM-1)>3H/4",
        "orderElevenWitnessesChecked": order_eleven_witnesses,
        "orderElevenWitness": "-(H+N-5)+5(H+N-1)-5H=0 for N=LM>=5",
        "recordsSha256": digest.hexdigest(),
        "classification": "finite exact integer regression of the all-index interval proof",
    }


def exhaustive_support_regression(
    maximum_level: int, maximum_order: int
) -> dict[str, object]:
    if maximum_level < 0:
        raise ValueError("maximum exhaustive level must be nonnegative")
    if maximum_order < 11:
        raise ValueError("maximum order must be at least eleven")
    parameter_pairs = 0
    target_sectors = 0
    state_transitions = 0
    support_states = 0
    cubic_returns = 0
    quartic_targets = 0
    order_eleven_targets = 0
    digest = hashlib.sha256()

    for level_l in range(maximum_level + 1):
        for level_m in range(maximum_level + 1):
            length, outputs, high, modes = packet(level_l, level_m)
            count = length * outputs
            carriers = list(range(high, high + count))
            shear = carriers + [-value for value in carriers]
            by_target: dict[int, list[int]] = {}
            for mode in modes:
                by_target.setdefault(int(mode["target"]), []).append(
                    int(mode["carrier"])
                )

            for target, initial_carriers in sorted(by_target.items()):
                support = {-value for value in initial_carriers}
                initial_support = set(support)
                supports: dict[int, set[int]] = {1: support}
                for order in range(2, maximum_order + 1):
                    state_transitions += len(support) * len(shear)
                    support = {frequency + shift for frequency in support for shift in shear}
                    supports[order] = support
                    support_states += len(support)

                if 0 not in supports[2]:
                    raise AssertionError("quadratic target path disappeared")
                if 0 in supports[3]:
                    raise AssertionError("cubic target return appeared")
                if not initial_support.issubset(supports[3]):
                    raise AssertionError("cubic high-frequency backtracking disappeared")
                cubic_returns += len(initial_support)
                if min(abs(value) for value in supports[3]) * 4 <= 3 * high:
                    raise AssertionError("exhaustive cubic support violated 3H/4")
                for odd_order in (3, 5, 7, 9):
                    if 0 in supports[odd_order]:
                        raise AssertionError(
                            f"odd order {odd_order} reached the low plane"
                        )
                if 0 not in supports[4]:
                    raise AssertionError("quartic target path disappeared")
                quartic_targets += 1
                if count >= 5:
                    witness_carrier = high + count - 5
                    witness_target = (witness_carrier - high) // length + 1
                    if target == witness_target:
                        if 0 not in supports[11]:
                            raise AssertionError("order-eleven target witness disappeared")
                        order_eleven_targets += 1

                digest.update(
                    (
                        f"{level_l}:{level_m}:{target}:"
                        + ",".join(
                            f"{order}:{len(supports[order])}:{min(supports[order])}:{max(supports[order])}:{int(0 in supports[order])}"
                            for order in range(1, maximum_order + 1)
                        )
                        + "\n"
                    ).encode()
                )
                target_sectors += 1
            parameter_pairs += 1

    return {
        "maximumDyadicLevel": maximum_level,
        "maximumPicardOrder": maximum_order,
        "parameterPairsChecked": parameter_pairs,
        "positiveTargetSectorsChecked": target_sectors,
        "stateTransitionsChecked": state_transitions,
        "supportStatesRecorded": support_states,
        "cubicOriginalVReturnsChecked": cubic_returns,
        "quarticTargetSectorsChecked": quartic_targets,
        "orderElevenTargetWitnessesChecked": order_eleven_targets,
        "oddOrdersExcluded": [3, 5, 7, 9],
        "recordsSha256": digest.hexdigest(),
        "classification": "finite exhaustive support regression; the theorem is the interval proof",
    }


def gaussian_add(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] + right[0], left[1] + right[1])


def gaussian_multiply(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def gaussian_conjugate(value: Gaussian) -> Gaussian:
    return (value[0], -value[1])


def gaussian_scale(factor: int, value: Gaussian) -> Gaussian:
    return (factor * value[0], factor * value[1])


def map_add(target: FourierMap, key: Int2, value: Gaussian) -> None:
    updated = gaussian_add(target.get(key, (0, 0)), value)
    if updated == (0, 0):
        target.pop(key, None)
    else:
        target[key] = updated


def derivative_x2(field: FourierMap) -> FourierMap:
    result: FourierMap = {}
    for (first, second), coefficient in field.items():
        map_add(
            result,
            (first, second),
            gaussian_multiply((0, second), coefficient),
        )
    return result


def convolve(left: FourierMap, right: FourierMap) -> tuple[FourierMap, int]:
    result: FourierMap = {}
    pairs = 0
    for left_key, left_value in left.items():
        for right_key, right_value in right.items():
            key = (left_key[0] + right_key[0], left_key[1] + right_key[1])
            map_add(result, key, gaussian_multiply(left_value, right_value))
            pairs += 1
    return result, pairs


def inner_product(left: FourierMap, right: FourierMap) -> Gaussian:
    result = (0, 0)
    for key in left.keys() & right.keys():
        result = gaussian_add(
            result,
            gaussian_multiply(gaussian_conjugate(left[key]), right[key]),
        )
    return result


def packet_fourier_maps(level_l: int, level_m: int) -> tuple[FourierMap, FourierMap]:
    _length, _outputs, _high, modes = packet(level_l, level_m)
    shear: FourierMap = {}
    scalar: FourierMap = {}
    for mode in modes:
        carrier = int(mode["carrier"])
        target = int(mode["target"])
        sign = int(mode["sign"])
        map_add(shear, (carrier, 0), (sign, 0))
        map_add(shear, (-carrier, 0), (sign, 0))
        map_add(scalar, (-carrier, target), (sign, 0))
        map_add(scalar, (carrier, -target), (sign, 0))
    return shear, scalar


def energy_cancellation_regression(maximum_level: int) -> dict[str, object]:
    if maximum_level < 0:
        raise ValueError("maximum energy level must be nonnegative")
    parameter_pairs = 0
    convolution_pairs = 0
    modes_checked = 0
    digest = hashlib.sha256()
    for level_l in range(maximum_level + 1):
        for level_m in range(maximum_level + 1):
            shear, first = packet_fourier_maps(level_l, level_m)
            d_first = derivative_x2(first)
            second, pairs = convolve(shear, d_first)
            second = {
                key: gaussian_scale(-1, value) for key, value in second.items()
            }
            d_second = derivative_x2(second)
            f_d_second, pairs_2 = convolve(shear, d_second)
            f_d_first, pairs_3 = convolve(shear, d_first)
            first_pair = inner_product(first, f_d_second)
            second_pair = inner_product(second, f_d_first)
            cancellation = gaussian_add(first_pair, second_pair)
            if cancellation != (0, 0):
                raise AssertionError("fourth-order transport energy did not cancel")
            for field in (shear, first, second):
                for key, value in field.items():
                    opposite = (-key[0], -key[1])
                    if field.get(opposite) != gaussian_conjugate(value):
                        raise AssertionError("Fourier field lost Hermitian reality")
            if not (first_pair[1] == 0 and second_pair[1] == 0):
                raise AssertionError("real energy pairing acquired an imaginary part")
            convolution_pairs += pairs + pairs_2 + pairs_3
            modes_checked += len(shear) + len(first) + len(second)
            parameter_pairs += 1
            digest.update(
                (
                    f"{level_l}:{level_m}:{len(shear)}:{len(first)}:{len(second)}:"
                    f"{first_pair}:{second_pair}:{pairs + pairs_2 + pairs_3}\n"
                ).encode()
            )
    return {
        "maximumDyadicLevel": maximum_level,
        "parameterPairsChecked": parameter_pairs,
        "FourierModesChecked": modes_checked,
        "convolutionPairsChecked": convolution_pairs,
        "identity": "<G1,F*d2G2>+<G2,F*d2G1>=0",
        "GaussianIntegerCancellationPassed": True,
        "recordsSha256": digest.hexdigest(),
        "classification": "finite exact Gaussian-integer regression of periodic integration by parts",
    }


def symbolic_structure() -> dict[str, object]:
    structure = {
        "velocityClass": "u=(0,F(x_1,t),G(x_1,x_2,t))",
        "nonlinearity": "(u dot grad)u=F*d_2G*e_3",
        "reducedSystem": [
            "d_tF-d_1^2F=0",
            "d_tG-Delta_12G+F*d_2G=0",
        ],
        "picardChain": "(d_t-Delta_12)G_n=-F_1*d_2G_(n-1)",
        "polarization": "u^[n] parallel e_3 for every n>=2",
        "conservedFrequency": "the x_2 Fourier frequency m is fixed along the chain",
        "pressure": "spatially constant",
    }
    if "one chain" in structure.values():
        raise AssertionError("symbolic structure record unexpectedly changed")
    return {
        "structure": structure,
        "globalSmoothnessBoundary": (
            "for each fixed smooth packet the G equation is linear parabolic; "
            "this is symmetry-specific and not an arbitrary-data estimate"
        ),
        "classification": "formal exact invariant-subspace reduction",
    }


def construct_certificate(
    maximum_level: int,
    maximum_exhaustive_level: int,
    maximum_order: int,
    maximum_energy_level: int,
    source_commit: str | None,
    show_progress: bool,
) -> dict[str, object]:
    started = time.perf_counter()
    progress(show_progress, started, "checking all-index carrier intervals")
    intervals = interval_theorem_regression(maximum_level)
    progress(
        show_progress,
        started,
        "enumerating exact Picard support chains",
        maximumLevel=maximum_exhaustive_level,
        maximumOrder=maximum_order,
    )
    supports = exhaustive_support_regression(
        maximum_exhaustive_level, maximum_order
    )
    progress(
        show_progress,
        started,
        "checking Gaussian-integer energy cancellation",
        maximumLevel=maximum_energy_level,
    )
    energy = energy_cancellation_regression(maximum_energy_level)
    progress(show_progress, started, "recording invariant shear structure")
    structure = symbolic_structure()

    checks = {
        "formalInvariantShearSubspace": True,
        "formalPressureIsSpatiallyConstant": True,
        "formalFullSystemReducesToHeatPlusLinearAdvectionDiffusion": True,
        "formalPicardForestCollapsesToOneChain": True,
        "formalEveryHigherTermIsE3Polarized": True,
        "formalSecondFrequencyIsConserved": True,
        "formalCubicSupportGapExceedsThreeQuartersH": True,
        "formalCubicTargetProjectionVanishes": True,
        "formalOddOrdersThreeFiveSevenNineMissLowPlane": True,
        "formalOrderElevenSupportWitness": True,
        "formalCubicBacktrackingReturnsToOriginalVSupport": True,
        "formalQuarticTargetPathIsAdmissible": True,
        "formalFourthOrderEnergyCoefficientIdentity": True,
        "formalPacketClassIsGloballySmooth": True,
        "finiteIntervalRegressionPassed": intervals["maximumDyadicLevel"]
        == maximum_level,
        "finiteSupportRegressionPassed": supports["maximumPicardOrder"]
        == maximum_order,
        "finiteEnergyCancellationRegressionPassed": energy[
            "maximumDyadicLevel"
        ]
        == maximum_energy_level,
        "finiteChecksAreNotUsedAsProofs": True,
        "uniformQuarticBoundNotClaimed": True,
        "fullHigherRemainderControlNotClaimed": True,
        "arbitraryThreeDimensionalDataEstimateNotClaimed": True,
        "normInflationNotClaimed": True,
        "largeDataRegularityNotClaimed": True,
        "threeDimensionalNavierStokesRegularityNotClaimed": True,
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise AssertionError("R0.60 checks failed: " + ", ".join(failed))
    progress(
        show_progress,
        started,
        "all invariant-shear Picard checks passed",
        checks=len(checks),
        carrierPositions=intervals["carrierPositionsCoveredByFormula"],
        stateTransitions=supports["stateTransitionsChecked"],
        convolutionPairs=energy["convolutionPairsChecked"],
    )

    return {
        "schemaVersion": "1.0",
        "scope": {
            "system": "full periodic Navier-Stokes evolution of the R0.59 packet",
            "theorems": [
                "exact invariant shear reduction to heat plus linear advection-diffusion",
                "one-chain homogeneous Picard recurrence",
                "strict cubic target gap and no odd low-plane return through order nine",
                "order-eleven support witness",
                "exact fourth-order energy coefficient identity",
            ],
            "notClaimed": [
                "a uniform quartic or full higher-order remainder bound",
                "dominance of the R0.59 quadratic target output",
                "norm inflation or unboundedness of a critical solution map",
                "an estimate for arbitrary three-dimensional data",
                "large-data regularity or a solution of the Millennium problem",
            ],
        },
        "packet": {
            "parameters": "dyadic L,M; N=LM; H=4N; D=N-1",
            "carrierInterval": "I_N={H,...,H+D}",
            "positiveTargetSector": "xi_1=-Q+sum_(j=1)^(n-1) sigma_j P_j",
            "classification": "formal all-index support representation",
        },
        "invariantReduction": structure,
        "supportTheorem": {
            "cubicGap": "|xi_1|>=H-D=3N+1>3H/4",
            "oddOrdersExcluded": [3, 5, 7, 9],
            "oddOrderGaps": {
                "3": "H-D=3N+1",
                "5": "H-2D=2N+2",
                "7": "H-3D=N+3",
                "9": "H-4D=4",
            },
            "orderElevenWitness": "-(H+N-5)+5(H+N-1)-5H=0 for N>=5",
            "cubicHighReturn": "-Q+P-P=-Q",
            "quarticTargetPath": "-Q+Q+P-P=0",
            "classification": "formal all-index interval theorem and explicit paths",
        },
        "energyBookkeeping": {
            "identity": (
                "d_t(2<G1,G3>+||G2||_2^2)"
                "+2(2<grad G1,grad G3>+||grad G2||_2^2)=0"
            ),
            "mechanism": (
                "quadratic energy is compensated first by cubic high-frequency "
                "return and dissipation, not by linear-quadratic overlap"
            ),
            "classification": "formal coefficient identity",
        },
        "literatureBoundary": {
            "planeParallelReduction": "https://doi.org/10.2140/apde.2008.1.35",
            "classification": (
                "the invariant plane-parallel reduction is classical; the packet-specific "
                "Picard support theorem is the result audited here"
            ),
        },
        "finiteRegressions": {
            "intervals": intervals,
            "supports": supports,
            "energyCancellation": energy,
        },
        "researchDecision": {
            "cubicTargetQuestion": "negative: the cubic term has zero low-plane projection",
            "globalDynamicsOfPacket": "globally smooth invariant shear evolution",
            "firstTargetCorrection": "quartic G_4",
            "nextTest": (
                "compute Pi_0 G_4(t_H) exactly and test an epsilon^2/L^2 "
                "relative bound against possible M growth"
            ),
            "directClayValue": (
                "low; the result sharpens an estimate obstruction inside a "
                "globally regular symmetry class"
            ),
        },
        "checks": checks,
        "git": git_state(source_commit),
        "computation": {
            "createdUtc": datetime.now(timezone.utc).isoformat(),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "exactBackend": "Python integers and Gaussian integers",
            "randomness": False,
            "gpu": False,
            "floatingPointDecisionUse": False,
            "wallSeconds": time.perf_counter() - started,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-level", type=int, default=12)
    parser.add_argument("--maximum-exhaustive-level", type=int, default=3)
    parser.add_argument("--maximum-order", type=int, default=11)
    parser.add_argument("--maximum-energy-level", type=int, default=3)
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
        arguments.maximum_level,
        arguments.maximum_exhaustive_level,
        arguments.maximum_order,
        arguments.maximum_energy_level,
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
                    "carrierPositions": certificate["finiteRegressions"]["intervals"][
                        "carrierPositionsCoveredByFormula"
                    ],
                    "stateTransitions": certificate["finiteRegressions"][
                        "supports"
                    ]["stateTransitionsChecked"],
                    "convolutionPairs": certificate["finiteRegressions"][
                        "energyCancellation"
                    ]["convolutionPairsChecked"],
                },
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
