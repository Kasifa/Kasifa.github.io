#!/usr/bin/env python3
"""R0.59 exact audit for tensor multi-output critical saturation.

The formal all-index proof is in
research/multi_output_critical_saturation_note.md.  This program performs
deterministic integer and Gaussian-integer regressions for the packet shell,
target-output uniqueness, quadratic support separation, tensor
Rudin--Shapiro prefixes, Abel summation, and the symbolic norm envelopes.

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


IntVector = tuple[int, int, int]
Gaussian = tuple[int, int]
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(f"[R0.59 +{elapsed:8.2f}s] {stage}{suffix}", file=os.sys.stderr, flush=True)
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


def add(left: IntVector, right: IntVector) -> IntVector:
    return tuple(left[index] + right[index] for index in range(3))  # type: ignore[return-value]


def dot(left: IntVector, right: IntVector) -> int:
    return sum(left[index] * right[index] for index in range(3))


def norm_squared(vector: IntVector) -> int:
    return dot(vector, vector)


def gaussian_add(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] + right[0], left[1] + right[1])


def gaussian_multiply(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def gaussian_scale(factor: int, value: Gaussian) -> Gaussian:
    return (factor * value[0], factor * value[1])


def gaussian_power_i(exponent: int) -> Gaussian:
    return ((1, 0), (0, 1), (-1, 0), (0, -1))[exponent % 4]


def rudin_shapiro_pair(level: int) -> tuple[list[int], list[int]]:
    p = [1]
    q = [1]
    for _ in range(level):
        p, q = p + q, p + [-value for value in q]
    return p, q


def packet(level_l: int, level_m: int) -> tuple[int, int, int, list[dict[str, object]]]:
    length = 1 << level_l
    outputs = 1 << level_m
    high = 4 * length * outputs
    signs_l, _ = rudin_shapiro_pair(level_l)
    signs_m, _ = rudin_shapiro_pair(level_m)
    modes: list[dict[str, object]] = []
    for block in range(outputs):
        for offset in range(length):
            frequency = high + block * length + offset
            target = block + 1
            sign = signs_m[block] * signs_l[offset]
            modes.append(
                {
                    "block": block,
                    "offset": offset,
                    "frequency": frequency,
                    "target": target,
                    "sign": sign,
                    "p": (frequency, 0, 0),
                    "q": (-frequency, target, 0),
                }
            )
    return length, outputs, high, modes


def packet_family_regression(maximum_level: int) -> dict[str, object]:
    if maximum_level < 0:
        raise ValueError("maximum level must be nonnegative")
    digest = hashlib.sha256()
    modes_checked = 0
    parameter_pairs = 0
    largest_high = 0
    largest_output_count = 0
    for level_l in range(maximum_level + 1):
        for level_m in range(maximum_level + 1):
            length, outputs, high, modes = packet(level_l, level_m)
            if high != 4 * length * outputs:
                raise AssertionError("high-scale identity failed")
            if high // outputs != 4 * length:
                raise AssertionError("high-low separation identity failed")
            seen_frequencies: set[int] = set()
            target_counts = [0] * outputs
            for mode in modes:
                frequency = int(mode["frequency"])
                target = int(mode["target"])
                sign = int(mode["sign"])
                p = mode["p"]
                q = mode["q"]
                if not isinstance(p, tuple) or not isinstance(q, tuple):
                    raise AssertionError("frequency vector type changed")
                if frequency in seen_frequencies:
                    raise AssertionError("carrier frequencies must be unique")
                seen_frequencies.add(frequency)
                if sign not in (-1, 1):
                    raise AssertionError("tensor coefficient left {+1,-1}")
                if add(p, q) != (0, target, 0):
                    raise AssertionError("target-output identity failed")
                if dot(p, (0, 1, 0)) != 0:
                    raise AssertionError("U polarization is not divergence free")
                if dot(q, (0, 0, 1)) != 0:
                    raise AssertionError("V polarization is not divergence free")
                if dot(q, (0, 1, 0)) != target:
                    raise AssertionError("forward interaction coefficient failed")
                if dot(p, (0, 0, 1)) != 0:
                    raise AssertionError("exchanged interaction must vanish")
                if norm_squared(p) < high * high or norm_squared(p) >= 4 * high * high:
                    raise AssertionError("p left the single high shell")
                if norm_squared(q) < high * high or norm_squared(q) >= 4 * high * high:
                    raise AssertionError("q left the single high shell")
                if 4 * frequency >= 5 * high:
                    raise AssertionError("carrier exceeded five-fourths of H")
                if target * 4 > high:
                    raise AssertionError("target exceeded one-fourth of H")
                target_counts[target - 1] += 1
                digest.update(
                    f"{level_l}:{level_m}:{frequency}:{target}:{sign}:{p}:{q}\n".encode()
                )
                modes_checked += 1
            if target_counts != [length] * outputs:
                raise AssertionError("each target must receive exactly L diagonal modes")
            parameter_pairs += 1
            largest_high = max(largest_high, high)
            largest_output_count = max(largest_output_count, outputs)
    return {
        "maximumDyadicLevel": maximum_level,
        "parameterPairsChecked": parameter_pairs,
        "modesChecked": modes_checked,
        "largestHighScale": largest_high,
        "largestOutputCount": largest_output_count,
        "shell": "H<=|xi|<2H",
        "separation": "H/M=4L",
        "eachTargetHasExactlyLModes": True,
        "recordsSha256": digest.hexdigest(),
        "classification": "finite exact integer regression of the all-index packet formulas",
    }


def exhaustive_interaction_regression(maximum_level: int) -> dict[str, object]:
    if maximum_level < 0:
        raise ValueError("maximum exhaustive level must be nonnegative")
    pairs_checked = 0
    projected_pairs = 0
    target_pairs = 0
    digest = hashlib.sha256()
    for level_l in range(maximum_level + 1):
        for level_m in range(maximum_level + 1):
            length, outputs, high, modes = packet(level_l, level_m)
            local_target_pairs = 0
            for u_mode in modes:
                p = u_mode["p"]
                if not isinstance(p, tuple):
                    raise AssertionError("invalid U mode")
                for v_mode in modes:
                    q = v_mode["q"]
                    if not isinstance(q, tuple):
                        raise AssertionError("invalid V mode")
                    output = add(p, q)
                    pairs_checked += 1
                    if output[0] == 0:
                        projected_pairs += 1
                        if u_mode["frequency"] != v_mode["frequency"]:
                            raise AssertionError("xi_1=0 projection retained an off-diagonal pair")
                        if output != (0, int(v_mode["target"]), 0):
                            raise AssertionError("projected output missed its target")
                        if int(u_mode["sign"]) * int(v_mode["sign"]) != 1:
                            raise AssertionError("matched tensor signs did not square to one")
                        target_pairs += 1
                        local_target_pairs += 1
                    elif abs(output[0]) >= high // 4:
                        raise AssertionError("same-side difference output exceeded the low band")

                    opposite_first_coordinate = p[0] - q[0]
                    if opposite_first_coordinate < 2 * high:
                        raise AssertionError("opposite-side sum output entered the input shell")
                    digest.update(
                        f"{level_l}:{level_m}:{p}:{q}:{output}:{opposite_first_coordinate}\n".encode()
                    )
            if local_target_pairs != length * outputs:
                raise AssertionError("projected target count changed")
    return {
        "maximumDyadicLevel": maximum_level,
        "orderedPositivePairsChecked": pairs_checked,
        "projectedPairsChecked": projected_pairs,
        "targetPairsChecked": target_pairs,
        "projectionRetainsOnlyUniqueDiagonalMatches": True,
        "quadraticFirstCoordinateSupport": "|xi_1|<H/4 or |xi_1|>=2H",
        "linearQuadraticL2Orthogonality": True,
        "recordsSha256": digest.hexdigest(),
        "classification": "finite exhaustive interaction regression; support proof is the all-index interval argument",
    }


def tensor_prefix_regression(maximum_level: int) -> dict[str, object]:
    if maximum_level < 0:
        raise ValueError("maximum prefix level must be nonnegative")
    prefixes_checked = 0
    abel_checks = 0
    maximum_ratio_numerator = 0
    maximum_ratio_denominator = 1
    digest = hashlib.sha256()
    for level_l in range(maximum_level + 1):
        for level_m in range(maximum_level + 1):
            length, outputs, _high, modes = packet(level_l, level_m)
            # Four Gaussian phase pairs give exact two-variable regressions.
            for z_exponent, w_exponent in ((1, 1), (1, 2), (2, 1), (3, 3)):
                running = (0, 0)
                prefixes: list[Gaussian] = []
                terms: list[Gaussian] = []
                for mode in modes:
                    frequency = int(mode["frequency"])
                    target = int(mode["target"])
                    sign = int(mode["sign"])
                    phase = gaussian_multiply(
                        gaussian_power_i(z_exponent * frequency),
                        gaussian_power_i(w_exponent * target),
                    )
                    term = gaussian_scale(sign, phase)
                    terms.append(term)
                    running = gaussian_add(running, term)
                    prefixes.append(running)
                    modulus_squared = running[0] * running[0] + running[1] * running[1]
                    # C_T=(4+3sqrt(2)), so C_T^2=34+24sqrt(2)<68.
                    if modulus_squared > 68 * length * outputs:
                        raise AssertionError("sampled tensor prefix exceeded the formal envelope")
                    if modulus_squared * maximum_ratio_denominator > maximum_ratio_numerator * length * outputs:
                        maximum_ratio_numerator = modulus_squared
                        maximum_ratio_denominator = length * outputs
                    prefixes_checked += 1

                weights = list(range(len(terms), 0, -1))
                direct = (0, 0)
                for weight, term in zip(weights, terms):
                    direct = gaussian_add(direct, gaussian_scale(weight, term))
                abel = gaussian_scale(weights[-1], prefixes[-1])
                for index in range(len(weights) - 1):
                    abel = gaussian_add(
                        abel,
                        gaussian_scale(weights[index] - weights[index + 1], prefixes[index]),
                    )
                if direct != abel:
                    raise AssertionError("tensor Abel identity failed")
                abel_checks += 1
                digest.update(
                    f"{level_l}:{level_m}:{z_exponent}:{w_exponent}:{direct}:{prefixes[-1]}\n".encode()
                )
    return {
        "maximumDyadicLevel": maximum_level,
        "prefixesChecked": prefixes_checked,
        "abelChecks": abel_checks,
        "phasePairs": ["(i,i)", "(i,-1)", "(-1,i)", "(-i,-i)"],
        "tensorPrefixConstant": "C_T=(1+sqrt(2))*(2+sqrt(2))=4+3sqrt(2)",
        "rationalSquaredEnvelope": "C_T^2=34+24sqrt(2)<68",
        "maximumSampledModulusSquaredRatio": {
            "numerator": maximum_ratio_numerator,
            "denominator": maximum_ratio_denominator,
        },
        "weightedAbelIdentityPassed": True,
        "recordsSha256": digest.hexdigest(),
        "classification": "finite exact Gaussian-integer regression of the formal tensor-prefix proof",
    }


def symbolic_envelopes() -> dict[str, object]:
    envelopes = {
        "targetCoefficient": {
            "lower": "2mL/(25H^2)",
            "upper": "mL/(2H^2)",
        },
        "heatBesovInput": {
            "upper": "sqrt(2/e)*C_T*A/sqrt(H)",
        },
        "heatBesovOutput": {
            "lower": "exp(-1/4)*A^2/(600H)",
        },
        "heatBesovQuotient": {
            "lower": "exp(3/4)/(1200*C_T^2)",
            "shellPower": 0,
            "outputCountPower": 0,
        },
        "periodicBmoInput": {
            "upper": "sqrt(2)*C_T*A/sqrt(H)",
        },
        "periodicBmoOutput": {
            "lower": "exp(-1/64)*A^2/(3200H)",
        },
        "periodicBmoQuotient": {
            "lower": "exp(-1/64)/(6400*C_T^2)",
            "shellPower": 0,
            "outputCountPower": 0,
        },
    }
    if envelopes["heatBesovQuotient"]["shellPower"] != 0:
        raise AssertionError("heat-Besov quotient must be shell-uniform")
    if envelopes["periodicBmoQuotient"]["outputCountPower"] != 0:
        raise AssertionError("BMO quotient must be output-count uniform")
    return {
        "constant": "C_T=(1+sqrt(2))*(2+sqrt(2))",
        "envelopes": envelopes,
        "projectionContraction": {
            "heatBesov": "L-infinity contraction commuting with heat flow",
            "periodicBmoMinusOne": "Jensen inequality plus translation invariance of balls",
        },
        "classification": "formal all-index symbolic envelopes; exponentials enter only through monotonicity",
    }


def construct_certificate(
    maximum_level: int,
    maximum_exhaustive_level: int,
    maximum_prefix_level: int,
    source_commit: str | None,
    show_progress: bool,
) -> dict[str, object]:
    started = time.perf_counter()
    progress(show_progress, started, "checking tensor packet family", maximumLevel=maximum_level)
    family = packet_family_regression(maximum_level)
    progress(
        show_progress,
        started,
        "checking projected interactions and support separation",
        maximumLevel=maximum_exhaustive_level,
    )
    interactions = exhaustive_interaction_regression(maximum_exhaustive_level)
    progress(
        show_progress,
        started,
        "checking tensor Rudin--Shapiro prefixes and Abel identities",
        maximumLevel=maximum_prefix_level,
    )
    prefixes = tensor_prefix_regression(maximum_prefix_level)
    progress(show_progress, started, "checking symbolic norm envelopes")
    norms = symbolic_envelopes()

    checks = {
        "formalSingleHighShell": True,
        "formalRealAndDivergenceFree": True,
        "formalCompleteQuadraticTermReducesToUAdvectingV": True,
        "formalTargetProjectionRetainsOnlyUniqueDiagonalMatches": True,
        "formalAllTargetSignsSquareToPositiveOne": True,
        "formalExactDuhamelDenominatorIsTwoRSquared": True,
        "formalTargetCoefficientEnvelope": True,
        "formalTensorPrefixBound": True,
        "formalWeightedAbelBoundForBothInputs": True,
        "formalProjectionContractsHeatBesov": True,
        "formalProjectionContractsPeriodicBmoMinusOne": True,
        "formalHeatBesovMultiOutputSaturation": True,
        "formalPeriodicBmoMultiOutputSaturation": True,
        "formalLinearQuadraticL2Orthogonality": True,
        "finitePacketFamilyRegressionPassed": family["maximumDyadicLevel"] == maximum_level,
        "finiteExhaustiveInteractionRegressionPassed": interactions["maximumDyadicLevel"] == maximum_exhaustive_level,
        "finiteTensorPrefixRegressionPassed": prefixes["maximumDyadicLevel"] == maximum_prefix_level,
        "finiteChecksAreNotUsedAsProofs": True,
        "normInflationNotClaimed": True,
        "kochTataruBilinearUnboundednessNotClaimed": True,
        "higherPicardRemainderControlNotClaimed": True,
        "euclideanCompactSupportConstructionNotClaimed": True,
        "largeDataRegularityNotClaimed": True,
        "threeDimensionalNavierStokesRegularityNotClaimed": True,
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise AssertionError("R0.59 checks failed: " + ", ".join(failed))
    progress(
        show_progress,
        started,
        "all multi-output critical-saturation checks passed",
        checks=len(checks),
        modes=family["modesChecked"],
        interactionPairs=interactions["orderedPositivePairsChecked"],
        prefixes=prefixes["prefixesChecked"],
    )

    return {
        "schemaVersion": "1.0",
        "scope": {
            "system": "complete first Navier-Stokes Picard iterate of one real periodic tensor-sign packet",
            "theorems": [
                "single-shell tensor Rudin-Shapiro packet with M coherent low outputs",
                "exact all-index Duhamel coefficients for every target output",
                "uniform multi-output saturation in heat Besov and periodic BMO^-1",
                "exact L2 orthogonality of the linear and first nonlinear terms",
            ],
            "notClaimed": [
                "norm inflation or discontinuity of the solution map",
                "unboundedness of the Koch-Tataru bilinear map",
                "control of higher Picard iterates or the nonlinear remainder",
                "an R^3 compactly supported construction",
                "large-data global regularity or a solution of the Millennium problem",
            ],
        },
        "packet": {
            "parameters": "dyadic L and M; H=4LM",
            "carrier": "R_(r,n)=H+rL+n",
            "frequencies": "p=(R,0,0), q=(-R,r+1,0)",
            "polarizations": "U parallel e_2, V parallel e_3",
            "tensorSigns": "c_(r,n)=b_r*a_n from dyadic Rudin-Shapiro sequences",
            "targetSet": "K_M={(0,m,0):1<=m<=M}",
            "shell": "H<=|xi|<2H",
            "separation": "H/M=4L",
            "classification": "formal all-index construction",
        },
        "exactDuhamel": {
            "coefficient": "d_m(t)=m exp(-m^2t) sum_n (1-exp(-2R_(m-1,n)^2t))/(2R_(m-1,n)^2)",
            "observationTime": "t_H=log(2)/(2H^2)",
            "lowerBound": "2mL/(25H^2)",
            "upperBound": "mL/(2H^2)",
            "projectedPhysicalOutput": "2A^2 sum_(m=1)^M d_m(t_H) sin(mx_2)e_3",
            "classification": "formal exact identity and all-index inequalities",
        },
        "phaseFlattening": {
            "prefixConstant": "C_T=(1+sqrt(2))*(2+sqrt(2))",
            "heatEnvelope": "||exp(sDelta)u_0||_infinity<=4C_T A sqrt(LM) exp(-H^2s)",
            "matchedProducts": "c_(r,n)^2=1 simultaneously for all M targets",
            "classification": "formal tensor-prefix factorization and Abel summation",
        },
        "normComparison": norms,
        "energyBookkeeping": {
            "linearFirstCoordinateSupport": "H<=|xi_1|<5H/4",
            "quadraticFirstCoordinateSupport": "|xi_1|<H/4 or |xi_1|>=2H",
            "orthogonality": "<exp(t_H Delta)u_0,D_(t_H)(u_0,u_0)>_L2=0",
            "higherOrderBoundary": "the order-A^4 output energy requires higher-Picard and dissipative bookkeeping",
        },
        "finiteRegressions": {
            "packetFamily": family,
            "interactions": interactions,
            "tensorPrefixes": prefixes,
        },
        "literatureBoundary": {
            "kochTataru": "https://math.berkeley.edu/~tataru/papers/nas.pdf",
            "bourgainPavlovic": "https://arxiv.org/abs/0807.0882",
            "germainSecondIterate": "https://arxiv.org/abs/0806.4525",
            "cheskidovDai": "https://arxiv.org/abs/1212.3801",
            "rudinShapiroBound": "https://arxiv.org/abs/1909.08777",
        },
        "researchDecision": {
            "multiOutputQuestion": "negative: a growing structured output set need not force a square-function defect",
            "ruledOutStrategy": "shell decay based only on frequency separation, output multiplicity, and isotropic first-iterate critical norms",
            "nextTest": "uniform higher-Picard remainder bound versus an explicit third-order resonance",
            "standaloneNovelty": "moderate at most, pending broader literature review",
            "directClayValue": "low; this is a first-iterate obstruction, not an arbitrary-data a priori estimate",
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
    parser.add_argument("--maximum-level", type=int, default=10)
    parser.add_argument("--maximum-exhaustive-level", type=int, default=5)
    parser.add_argument("--maximum-prefix-level", type=int, default=10)
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
        arguments.maximum_prefix_level,
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
                    "modes": certificate["finiteRegressions"]["packetFamily"]["modesChecked"],  # type: ignore[index]
                    "interactionPairs": certificate["finiteRegressions"]["interactions"]["orderedPositivePairsChecked"],  # type: ignore[index]
                    "prefixes": certificate["finiteRegressions"]["tensorPrefixes"]["prefixesChecked"],  # type: ignore[index]
                },
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
