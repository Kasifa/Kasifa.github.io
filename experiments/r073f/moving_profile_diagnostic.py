#!/usr/bin/env python3
"""R0.73F finite moving-profile propagation diagnostic.

All matrices are finite Fourier compressions after the exact kinetic-space
isometry.  Results are binary64 diagnostics only; no cutoff row is used as
continuum evidence.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import sys
import time
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--benchmark-only", action="store_true")
    return parser.parse_args()


ARGS = parse_args()
if ARGS.deps:
    sys.path.insert(0, ARGS.deps)

import numpy as np  # noqa: E402
import scipy  # noqa: E402
from scipy.linalg import eig, expm, orth, svdvals  # noqa: E402


GAMMA = 0.5
MU = 0.25
CA = 49.0 / 4.0
START = time.perf_counter()
SOURCE = Path(__file__).resolve()
CONFIG = json.loads(ARGS.config.read_text(encoding="utf-8"))
OUT = ARGS.output_dir.resolve()
OUT.mkdir(parents=True, exist_ok=True)
PROGRESS = OUT / "progress.ndjson"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def emit(event: str, **fields: Any) -> None:
    row = {
        "timestampUtc": now_utc(),
        "elapsedSeconds": time.perf_counter() - START,
        "event": event,
        **fields,
    }
    with PROGRESS.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(row, sort_keys=True) + "\n")
    print(json.dumps(row, sort_keys=True), file=sys.stderr, flush=True)


def opnorm(matrix: np.ndarray) -> float:
    return float(svdvals(matrix, check_finite=False)[0])


def conorm(matrix: np.ndarray) -> float:
    return float(svdvals(matrix, check_finite=False)[-1])


def matrix_recurrence(N: int, epsilon: float, d: float, sign: int = 1) -> np.ndarray:
    """Kinetic-conjugated finite matrix from the exact column recurrence."""
    raw = np.zeros((2 * N + 1, 2 * N + 1), dtype=np.complex128)
    e1 = math.exp(-d)
    e4 = math.exp(-4.0 * d)
    for column, n in enumerate(range(-N, N + 1)):
        lam = n * n + MU
        first = GAMMA * 0.25 * e1 * (1.0 - 1.0 / lam)
        second = GAMMA * e4 * (-0.125 + 0.5 / lam)
        for shift, value in (
            (1, first),
            (-1, -first),
            (2, second),
            (-2, -second),
        ):
            m = n + shift
            if -N <= m <= N:
                raw[m + N, column] = sign * value

    modes = np.arange(-N, N + 1, dtype=float)
    lam = modes * modes + MU
    transformed = (
        (1.0 / np.sqrt(lam))[:, None]
        * raw
        * np.sqrt(lam)[None, :]
    )
    transformed -= epsilon * np.diag(lam)
    return transformed


def leading_split(matrix: np.ndarray, real_tolerance: float) -> dict[str, Any]:
    values, left, right = eig(matrix, left=True, right=True, check_finite=False)
    top_real = float(np.max(values.real))
    indices = np.flatnonzero(values.real >= top_real - real_tolerance)
    right_block = right[:, indices]
    left_block = left[:, indices]
    overlap = left_block.conjugate().T @ right_block
    projector = (
        right_block
        @ np.linalg.inv(overlap)
        @ left_block.conjugate().T
    )
    basis = orth(right_block, rcond=1e-12)
    if basis.shape[1] != len(indices):
        raise RuntimeError("finite top block lost numerical rank")
    other = np.delete(values, indices)
    real_gap = top_real - float(np.max(other.real)) if len(other) else math.inf
    return {
        "values": values,
        "indices": indices,
        "projector": projector,
        "basis": basis,
        "topReal": top_real,
        "realGap": real_gap,
        "dimension": int(len(indices)),
        "idempotenceResidual": opnorm(projector @ projector - projector),
        "commutatorResidual": opnorm(matrix @ projector - projector @ matrix),
    }


def normalized_rep(matrix: np.ndarray, log_scale: float = 0.0) -> tuple[np.ndarray, float]:
    scale = float(np.linalg.norm(matrix, ord="fro"))
    if not math.isfinite(scale) or scale <= 0.0:
        raise FloatingPointError("propagator normalization failed")
    return matrix / scale, log_scale + math.log(scale)


def cf4_step(N: int, epsilon: float, theta: float, h: float, sign: int) -> np.ndarray:
    root3 = math.sqrt(3.0)
    c1 = 0.5 - root3 / 6.0
    c2 = 0.5 + root3 / 6.0
    a1 = (3.0 - 2.0 * root3) / 12.0
    a2 = (3.0 + 2.0 * root3) / 12.0
    A1 = matrix_recurrence(N, epsilon, epsilon * (theta + c1 * h), sign)
    A2 = matrix_recurrence(N, epsilon, epsilon * (theta + c2 * h), sign)
    early = expm(h * (a2 * A1 + a1 * A2))
    late = expm(h * (a1 * A1 + a2 * A2))
    return late @ early


def propagate(
    N: int,
    epsilon: float,
    physical_targets: list[float],
    fast_step: float,
    sign: int = 1,
    physical_start: float = 0.0,
) -> dict[str, Any]:
    dimension = 2 * N + 1
    state = np.eye(dimension, dtype=np.complex128)
    state, log_scale = normalized_rep(state)
    theta = physical_start / epsilon
    start_theta = theta
    split = leading_split(
        matrix_recurrence(N, epsilon, physical_start, sign),
        float(CONFIG["finiteTopRealTolerance"]),
    )
    top_basis = split["basis"]
    snapshots = []

    for physical_target in physical_targets:
        target_theta = physical_target / epsilon
        if target_theta < theta - 1e-13:
            raise ValueError("physical targets must be increasing")
        while theta < target_theta - 1e-13:
            h = min(fast_step, target_theta - theta)
            state = cf4_step(N, epsilon, theta, h, sign) @ state
            state, log_scale = normalized_rep(state, log_scale)
            theta += h

        full_sigma = opnorm(state)
        top_sigma = conorm(state @ top_basis)
        snapshots.append({
            "physicalTime": float(physical_target),
            "fastTime": float(theta - start_theta),
            "logFullNorm": float(log_scale + math.log(full_sigma)),
            "logTopConorm": float(log_scale + math.log(top_sigma)),
            "normalizedFullRate": (
                0.0 if physical_target == physical_start
                else float(epsilon * (log_scale + math.log(full_sigma))
                           / (physical_target - physical_start))
            ),
            "normalizedTopRate": (
                0.0 if physical_target == physical_start
                else float(epsilon * (log_scale + math.log(top_sigma))
                           / (physical_target - physical_start))
            ),
        })

    return {
        "N": N,
        "epsilon": epsilon,
        "sign": sign,
        "fastStep": fast_step,
        "physicalStart": physical_start,
        "physicalEnd": physical_targets[-1],
        "finiteTop": {
            "dimension": split["dimension"],
            "spectralAbscissa": split["topReal"],
            "realGapToRemainder": split["realGap"],
            "projectorIdempotenceResidual": split["idempotenceResidual"],
            "projectorCommutatorResidual": split["commutatorResidual"],
        },
        "snapshots": snapshots,
        "scaledPropagator": state,
        "logScale": log_scale,
    }


def rep_relative_difference(
    first: tuple[np.ndarray, float], second: tuple[np.ndarray, float]
) -> float:
    a, sa = first
    b, sb = second
    smax = max(sa, sb)
    aa = math.exp(sa - smax) * a
    bb = math.exp(sb - smax) * b
    return opnorm(aa - bb) / max(opnorm(aa), opnorm(bb), np.finfo(float).tiny)


def composition_check(N: int, epsilon: float, d_end: float, fast_step: float) -> float:
    mid = d_end / 2.0
    whole = propagate(N, epsilon, [d_end], fast_step)
    left = propagate(N, epsilon, [mid], fast_step)
    right = propagate(N, epsilon, [d_end], fast_step, physical_start=mid)
    product = right["scaledPropagator"] @ left["scaledPropagator"]
    product, product_scale = normalized_rep(
        product, right["logScale"] + left["logScale"]
    )
    return rep_relative_difference(
        (whole["scaledPropagator"], whole["logScale"]),
        (product, product_scale),
    )


def sign_check(N: int, epsilon: float, d_end: float, fast_step: float) -> dict[str, float]:
    plus = propagate(N, epsilon, [d_end], fast_step, sign=1)
    minus = propagate(N, epsilon, [d_end], fast_step, sign=-1)
    reversal = np.eye(2 * N + 1, dtype=np.complex128)[::-1]
    generator_defect = opnorm(
        matrix_recurrence(N, epsilon, d_end, -1)
        - reversal @ matrix_recurrence(N, epsilon, d_end, 1).conjugate() @ reversal
    )
    transformed_plus = (
        reversal @ plus["scaledPropagator"].conjugate() @ reversal,
        plus["logScale"],
    )
    propagator_defect = rep_relative_difference(
        transformed_plus,
        (minus["scaledPropagator"], minus["logScale"]),
    )
    plus_log = plus["snapshots"][-1]["logFullNorm"]
    minus_log = minus["snapshots"][-1]["logFullNorm"]
    return {
        "generatorConjugacyDefect": generator_defect,
        "propagatorConjugacyRelativeDefect": propagator_defect,
        "absoluteLogGainDifference": abs(plus_log - minus_log),
    }


def drift_rows(N: int) -> list[dict[str, float]]:
    base = matrix_recurrence(N, 0.0, 0.0)
    rows = []
    for d in CONFIG["driftSamplePhysicalTimes"]:
        difference = opnorm(matrix_recurrence(N, 0.0, float(d)) - base)
        rows.append({
            "N": N,
            "physicalTime": float(d),
            "finiteDriftNorm": difference,
            "analyticBound": CA * float(d),
            "ratioToAnalyticBound": difference / (CA * float(d)),
        })
    return rows


def counterexamples() -> dict[str, Any]:
    prefactor_rows = []
    maximum_closed_form_residual = 0.0
    for n in CONFIG["counterexampleSizes"]:
        n_float = float(n)
        block = np.asarray([[-n_float, n_float * n_float], [0.0, -n_float]])
        actual = expm(block / n_float)
        closed = math.exp(-1.0) * np.asarray([[1.0, n_float], [0.0, 1.0]])
        residual = opnorm(actual - closed)
        maximum_closed_form_residual = max(maximum_closed_form_residual, residual)
        prefactor_rows.append({
            "size": int(n),
            "spectralValue": -n_float,
            "evaluationTime": 1.0 / n_float,
            "semigroupNorm": opnorm(actual),
            "lowerReference": n_float / math.e,
            "closedFormResidual": residual,
        })

    count = int(CONFIG["counterexamplePhaseGridCount"])
    phase = np.linspace(0.0, 1.0, count)
    branches = np.stack([
        np.cos(2.0 * np.pi * phase - 2.0 * np.pi * j / 3.0) - 0.25
        for j in range(3)
    ])
    pointwise_max = np.max(branches, axis=0)
    rotating_rows = []
    for index, x in enumerate(phase):
        rotating_rows.append({
            "normalizedPhysicalTime": float(x),
            "lambda0": float(branches[0, index]),
            "lambda1": float(branches[1, index]),
            "lambda2": float(branches[2, index]),
            "pointwiseMaximum": float(pointwise_max[index]),
        })
    return {
        "nonnormalPrefactor": {
            "rows": prefactor_rows,
            "maximumClosedFormResidual": maximum_closed_form_residual,
            "exactStatement": "exp(D_n/n)=exp(-1)*[[1,n],[0,1]] and norm>=n/e",
        },
        "rotatingPositiveEdge": {
            "rows": rotating_rows,
            "sampledMinimumPointwiseMaximum": float(np.min(pointwise_max)),
            "exactMinimumPointwiseMaximum": 0.25,
            "exactBranchIntegral": -0.25,
            "exactEndpointLogGainPerInverseEpsilon": -0.25,
            "exactStatement": "max_j lambda_j(d)>=1/4 while every branch integrates to -1/4 on d/D in [0,1]",
        },
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    if PROGRESS.exists():
        PROGRESS.unlink()
    emit("start", config=str(ARGS.config), benchmarkOnly=ARGS.benchmark_only)

    if ARGS.benchmark_only:
        N = int(CONFIG["primaryCutoff"])
        epsilon = float(CONFIG["primaryEpsilons"][-1])
        start = time.perf_counter()
        result = propagate(
            N, epsilon, [0.001], float(CONFIG["primaryFastStep"])
        )
        benchmark = {
            "schemaVersion": "r073f-benchmark-v1",
            "N": N,
            "epsilon": epsilon,
            "physicalEnd": 0.001,
            "wallTimeSeconds": time.perf_counter() - start,
            "projectedFullGridWallTimeSeconds": (
                (time.perf_counter() - start)
                * float(CONFIG["diagnosticPhysicalEndpoint"]) / 0.001
            ),
            "endpoint": result["snapshots"][-1],
        }
        (OUT / "benchmark.json").write_text(
            json.dumps(benchmark, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        emit("benchmark-complete", **benchmark)
        return 0

    d_end = float(CONFIG["diagnosticPhysicalEndpoint"])
    snapshots = [float(value) for value in CONFIG["physicalSnapshots"]]
    primary_step = float(CONFIG["primaryFastStep"])
    primary_N = int(CONFIG["primaryCutoff"])

    requested: set[tuple[int, float]] = {
        (primary_N, float(epsilon)) for epsilon in CONFIG["primaryEpsilons"]
    }
    for N in CONFIG["cutoffComparison"]["cutoffs"]:
        for epsilon in CONFIG["cutoffComparison"]["epsilons"]:
            requested.add((int(N), float(epsilon)))

    rows: list[dict[str, Any]] = []
    full_results: dict[tuple[int, float], dict[str, Any]] = {}
    ordered = sorted(requested, key=lambda item: (item[0], -item[1]))
    for index, (N, epsilon) in enumerate(ordered, start=1):
        row_start = time.perf_counter()
        result = propagate(N, epsilon, snapshots, primary_step)
        full_results[(N, epsilon)] = result
        for snap in result["snapshots"]:
            rows.append({
                "N": N,
                "epsilon": epsilon,
                "absoluteLambda": 1.0 / epsilon,
                "fastStep": primary_step,
                "physicalTime": snap["physicalTime"],
                "fastTime": snap["fastTime"],
                "finiteTopDimension": result["finiteTop"]["dimension"],
                "finiteTopSpectralAbscissa": result["finiteTop"]["spectralAbscissa"],
                "finiteTopRealGap": result["finiteTop"]["realGapToRemainder"],
                "projectorIdempotenceResidual": result["finiteTop"]["projectorIdempotenceResidual"],
                "projectorCommutatorResidual": result["finiteTop"]["projectorCommutatorResidual"],
                "logFullNorm": snap["logFullNorm"],
                "logTopConorm": snap["logTopConorm"],
                "normalizedFullRate": snap["normalizedFullRate"],
                "normalizedTopRate": snap["normalizedTopRate"],
                "topConormNoLargerThanFullNorm": bool(
                    snap["logTopConorm"] <= snap["logFullNorm"] + 5e-12
                ),
                "r073bUpperLogBound": 5.0 / (16.0 * epsilon),
                "r073bUpperSlack": 5.0 / (16.0 * epsilon) - snap["logFullNorm"],
            })
        emit(
            "propagation-row-complete",
            row=index,
            totalRows=len(ordered),
            N=N,
            epsilon=epsilon,
            endpoint=result["snapshots"][-1],
            wallTimeSeconds=time.perf_counter() - row_start,
            estimatedSecondsRemaining=(
                (time.perf_counter() - START) / index * (len(ordered) - index)
            ),
        )

    convergence_rows: list[dict[str, Any]] = []
    for epsilon in CONFIG["stepHalving"]["epsilons"]:
        epsilon = float(epsilon)
        levels = []
        for h in CONFIG["stepHalving"]["fastSteps"]:
            h = float(h)
            if abs(h - primary_step) < 1e-15:
                result = full_results[(primary_N, epsilon)]
            else:
                result = propagate(primary_N, epsilon, [d_end], h)
            levels.append((h, result["snapshots"][-1]))
        levels.sort(reverse=True)
        for (h0, coarse), (h1, fine) in zip(levels, levels[1:]):
            convergence_rows.append({
                "kind": "step-halving",
                "N": primary_N,
                "epsilon": epsilon,
                "coarseFastStep": h0,
                "fineFastStep": h1,
                "fullLogDifference": abs(coarse["logFullNorm"] - fine["logFullNorm"]),
                "topLogDifference": abs(coarse["logTopConorm"] - fine["logTopConorm"]),
                "fullNormalizedRateDifference": abs(coarse["normalizedFullRate"] - fine["normalizedFullRate"]),
                "topNormalizedRateDifference": abs(coarse["normalizedTopRate"] - fine["normalizedTopRate"]),
            })
        emit("step-halving-complete", epsilon=epsilon)

    for epsilon in CONFIG["cutoffComparison"]["epsilons"]:
        epsilon = float(epsilon)
        cutoff_results = []
        for N in CONFIG["cutoffComparison"]["cutoffs"]:
            result = full_results[(int(N), epsilon)]["snapshots"][-1]
            cutoff_results.append((int(N), result))
        cutoff_results.sort()
        for (n0, coarse), (n1, fine) in zip(cutoff_results, cutoff_results[1:]):
            convergence_rows.append({
                "kind": "cutoff-discrepancy-not-tail-bound",
                "N": n1,
                "epsilon": epsilon,
                "coarseFastStep": n0,
                "fineFastStep": n1,
                "fullLogDifference": abs(coarse["logFullNorm"] - fine["logFullNorm"]),
                "topLogDifference": abs(coarse["logTopConorm"] - fine["logTopConorm"]),
                "fullNormalizedRateDifference": abs(coarse["normalizedFullRate"] - fine["normalizedFullRate"]),
                "topNormalizedRateDifference": abs(coarse["normalizedTopRate"] - fine["normalizedTopRate"]),
            })

    composition = composition_check(primary_N, 0.001, d_end, primary_step)
    sign = sign_check(primary_N, 0.001, d_end, primary_step)
    drifts = drift_rows(primary_N)
    examples = counterexamples()

    matrix_rows = []
    reversal = np.eye(2 * primary_N + 1, dtype=np.complex128)[::-1]
    for d in CONFIG["driftSamplePhysicalTimes"]:
        plus = matrix_recurrence(primary_N, 0.001, float(d), 1)
        minus = matrix_recurrence(primary_N, 0.001, float(d), -1)
        matrix_rows.append({
            "physicalTime": float(d),
            "signConjugacyDefect": opnorm(minus - reversal @ plus.conjugate() @ reversal),
        })

    tolerances = CONFIG["tolerances"]
    maximum_idempotence = max(row["projectorIdempotenceResidual"] for row in rows)
    maximum_commutator = max(row["projectorCommutatorResidual"] for row in rows)
    minimum_upper_slack = min(row["r073bUpperSlack"] for row in rows)
    maximum_drift_ratio = max(row["ratioToAnalyticBound"] for row in drifts)
    maximum_step_log = max(
        max(row["fullLogDifference"], row["topLogDifference"])
        for row in convergence_rows if row["kind"] == "step-halving" and row["fineFastStep"] == 0.125
    )
    checks = {
        "declaredPrimaryGridComplete": len([
            row for row in rows
            if row["N"] == primary_N and row["physicalTime"] == d_end
        ]) == len(CONFIG["primaryEpsilons"]),
        "diagnosticEndpointExplicitlyNotCertifiedD0": (
            CONFIG["diagnosticEndpointIsCertifiedD0"] is False
            and CONFIG["claimBoundary"]["diagnosticDIsCertifiedD0"] is False
        ),
        "finiteTopProjectorsNumericallyAlgebraic": max(
            maximum_idempotence, maximum_commutator
        ) < float(tolerances["projectorIdempotence"]),
        "topConormNeverExceedsFullNorm": all(
            row["topConormNoLargerThanFullNorm"] for row in rows
        ),
        "r073bFiveSixteenthsSentinel": minimum_upper_slack >= -float(tolerances["upperBoundSlack"]),
        "profileDriftBelowAnalyticBoundOnSample": maximum_drift_ratio <= 1.0 + float(tolerances["driftRatioExcess"]),
        "stepHalvingStableAtFinestPair": maximum_step_log < 5e-7,
        "compositionSentinel": composition < float(tolerances["compositionRelative"]),
        "signConjugacySentinel": max(
            sign["generatorConjugacyDefect"],
            sign["propagatorConjugacyRelativeDefect"],
            sign["absoluteLogGainDifference"],
            max(row["signConjugacyDefect"] for row in matrix_rows),
        ) < float(tolerances["signGainAbsoluteLog"]),
        "nonnormalCounterexampleClosedForm": (
            examples["nonnormalPrefactor"]["maximumClosedFormResidual"]
            < float(tolerances["exactCounterexampleResidual"])
        ),
        "rotatingEdgeSampleRespectsExactQuarterFloor": (
            examples["rotatingPositiveEdge"]["sampledMinimumPointwiseMaximum"]
            >= 0.25 - 2e-12
        ),
        "claimBoundaryFailClosed": all(
            value is False for key, value in CONFIG["claimBoundary"].items()
            if key != "finiteBinary64Diagnostic"
        ) and CONFIG["claimBoundary"]["finiteBinary64Diagnostic"] is True,
    }
    checks = {key: bool(value) for key, value in checks.items()}

    write_csv(OUT / "moving_gain_rows.csv", rows)
    write_csv(OUT / "convergence_rows.csv", convergence_rows)
    write_csv(OUT / "drift_rows.csv", drifts)
    write_csv(
        OUT / "counterexample_nonnormal_rows.csv",
        examples["nonnormalPrefactor"]["rows"],
    )
    write_csv(
        OUT / "counterexample_rotating_rows.csv",
        examples["rotatingPositiveEdge"]["rows"],
    )

    selected = full_results[(primary_N, float(CONFIG["primaryEpsilons"][-1]))]
    np.savez_compressed(
        OUT / "selected_propagator.npz",
        scaledPropagator=selected["scaledPropagator"],
        logScale=np.asarray([selected["logScale"]]),
        N=np.asarray([primary_N]),
        epsilon=np.asarray([float(CONFIG["primaryEpsilons"][-1])]),
        physicalEnd=np.asarray([d_end]),
    )

    environment = {
        "schemaVersion": "r073f-finite-environment-v1",
        "createdUtc": now_utc(),
        "executionMode": "local dense CPU linear algebra",
        "dgxUsed": False,
        "dgxReason": "largest matrix is 193 by 193; local dense CPU execution avoids transfer overhead",
        "python": platform.python_version(),
        "pythonImplementation": platform.python_implementation(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "logicalCpuCount": os.cpu_count(),
        "blasThreadEnvironment": {
            key: os.environ.get(key) for key in (
                "OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"
            )
        },
        "precision": "numpy.complex128 / IEEE-754 binary64 components",
        "randomnessUsed": False,
        "randomSeed": None,
        "claimBoundary": CONFIG["claimBoundary"],
    }
    (OUT / "environment.json").write_text(
        json.dumps(environment, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    summary = {
        "schemaVersion": "r073f-finite-summary-v1",
        "release": "R0.73F-finite-diagnostic",
        "createdUtc": now_utc(),
        "sourceBinding": {
            "path": "experiments/r073f/moving_profile_diagnostic.py",
            "sha256": sha256(SOURCE),
        },
        "configBinding": {
            "path": "experiments/r073f/config.json",
            "sha256": sha256(ARGS.config),
        },
        "diagnosticPhysicalEndpoint": d_end,
        "diagnosticEndpointIsCertifiedD0": False,
        "primaryGrid": {
            "N": primary_N,
            "epsilons": CONFIG["primaryEpsilons"],
            "rowCount": len(CONFIG["primaryEpsilons"]),
            "fastStep": primary_step,
        },
        "finiteSentinels": {
            "maximumProjectorIdempotenceResidual": maximum_idempotence,
            "maximumProjectorCommutatorResidual": maximum_commutator,
            "minimumR073BUpperSlack": minimum_upper_slack,
            "maximumDriftRatio": maximum_drift_ratio,
            "maximumFinestStepPairLogDifference": maximum_step_log,
            "compositionRelativeDefect": composition,
            "sign": sign,
        },
        "counterexamples": {
            "nonnormalPrefactor": {
                key: value for key, value in examples["nonnormalPrefactor"].items()
                if key != "rows"
            },
            "rotatingPositiveEdge": {
                key: value for key, value in examples["rotatingPositiveEdge"].items()
                if key != "rows"
            },
        },
        "checks": checks,
        "allPrimaryChecksPass": all(checks.values()),
        "dataFiles": [
            "moving_gain_rows.csv",
            "convergence_rows.csv",
            "drift_rows.csv",
            "counterexample_nonnormal_rows.csv",
            "counterexample_rotating_rows.csv",
            "selected_propagator.npz",
            "progress.ndjson",
            "environment.json"
        ],
        "scientificWallTimeSeconds": time.perf_counter() - START,
        "claimBoundary": CONFIG["claimBoundary"],
    }
    (OUT / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    emit(
        "complete",
        allPrimaryChecksPass=summary["allPrimaryChecksPass"],
        checks=checks,
        scientificWallTimeSeconds=summary["scientificWallTimeSeconds"],
    )
    return 0 if summary["allPrimaryChecksPass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
