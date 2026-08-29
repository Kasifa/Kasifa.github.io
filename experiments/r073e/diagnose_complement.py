#!/usr/bin/env python3
"""Finite R0.73E diagnostics for the complement of the R0.73D cluster.

The matrix is the finite Fourier compression of B_epsilon after the exact
kinetic-space isometry U_mu.  Every norm below is therefore an Euclidean
2-norm in the transformed finite space.  Nothing in this script is an
interval computation or an infinite-dimensional estimate.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import sys
import time


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default=os.environ.get("R073E_DEPS", ""))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--environment", type=Path, required=True)
    parser.add_argument("--progress", type=Path, required=True)
    parser.add_argument("--cutoffs", default="24,48,96")
    parser.add_argument("--epsilons", default="1e-2,1e-3,1e-4,1e-5,1e-6")
    parser.add_argument("--vertical-lines", default="0.05,0.08,0.12")
    parser.add_argument("--imaginary-maximum", type=float, default=0.4)
    parser.add_argument("--imaginary-grid-count", type=int, default=101)
    parser.add_argument("--time-maximum", type=float, default=200.0)
    parser.add_argument("--time-step", type=float, default=2.0)
    return parser.parse_args()


ARGS = parse_args()
if ARGS.deps:
    sys.path.insert(0, ARGS.deps)

import numpy as np  # noqa: E402
import scipy  # noqa: E402
from scipy.linalg import eig, expm, null_space, svdvals  # noqa: E402
from scipy.optimize import minimize_scalar  # noqa: E402


GAMMA = 0.5
MU = 0.25
SOURCE = Path(__file__).resolve()
START = time.perf_counter()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def emit(event: str, **fields: object) -> None:
    row = {
        "timestampUtc": now_utc(),
        "elapsedSeconds": time.perf_counter() - START,
        "event": event,
        **fields,
    }
    with ARGS.progress.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(row, sort_keys=True) + "\n")
    print(json.dumps(row, sort_keys=True), file=sys.stderr, flush=True)


def matrix_recurrence(N: int, epsilon: float) -> np.ndarray:
    """Build U_mu P_N(A-epsilon L)P_N U_mu^{-1} by column recurrence."""
    raw = np.zeros((2 * N + 1, 2 * N + 1), dtype=np.complex128)
    for column, n in enumerate(range(-N, N + 1)):
        lam = n * n + MU
        first = GAMMA * 0.25 * (1.0 - 1.0 / lam)
        second = GAMMA * (-0.125 + 0.5 / lam)
        for shift, value in (
            (1, first),
            (-1, -first),
            (2, second),
            (-2, -second),
        ):
            m = n + shift
            if -N <= m <= N:
                raw[m + N, column] = value

    modes = np.arange(-N, N + 1, dtype=float)
    lam = modes * modes + MU
    transformed = (
        (1.0 / np.sqrt(lam))[:, None]
        * raw
        * np.sqrt(lam)[None, :]
    )
    transformed -= epsilon * np.diag(lam)
    return transformed


def opnorm(matrix: np.ndarray) -> float:
    return float(svdvals(matrix, check_finite=False)[0])


def spectral_split(matrix: np.ndarray) -> dict[str, object]:
    values, left, right = eig(
        matrix, left=True, right=True, check_finite=False
    )
    index = int(np.argmax(values.real))
    value = values[index]
    lvec = left[:, index] / np.linalg.norm(left[:, index])
    rvec = right[:, index] / np.linalg.norm(right[:, index])
    pairing = np.vdot(lvec, rvec)
    projector = np.outer(rvec, lvec.conjugate()) / pairing
    complement = np.eye(matrix.shape[0], dtype=np.complex128) - projector

    # Ran Q = ker(l^*) for this rank-one finite spectral split.  Z is an
    # orthonormal basis, so Bq is the restriction with its inherited norm.
    basis = null_space(lvec.conjugate()[None, :], check_finite=False)
    restricted = basis.conjugate().T @ matrix @ basis
    q_values = eig(restricted, right=False, check_finite=False)
    q_order = np.argsort(q_values.real)[::-1]
    q_values = q_values[q_order]

    return {
        "values": values,
        "value": value,
        "left": lvec,
        "right": rvec,
        "pairing": pairing,
        "P": projector,
        "Q": complement,
        "Z": basis,
        "Bq": restricted,
        "qValues": q_values,
    }


def complex_record(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imag": float(value.imag)}


def resolvent_peak(
    restricted: np.ndarray,
    alpha: float,
    y_max: float,
    grid_count: int,
) -> dict[str, object]:
    identity = np.eye(restricted.shape[0], dtype=np.complex128)

    def sigma_min(y: float) -> float:
        return float(svdvals(
            (alpha + 1j * y) * identity - restricted,
            check_finite=False,
        )[-1])

    positive_y = np.linspace(0.0, y_max, grid_count)
    positive_sigma = np.asarray([sigma_min(float(y)) for y in positive_y])
    negative_sigma = np.asarray([sigma_min(float(-y)) for y in positive_y])
    index = int(np.argmin(positive_sigma))
    lo = float(positive_y[max(0, index - 1)])
    hi = float(positive_y[min(grid_count - 1, index + 1)])
    if hi > lo:
        optimum = minimize_scalar(
            lambda y: math.log(sigma_min(float(y))),
            bounds=(lo, hi),
            method="bounded",
            options={"xatol": 1e-11, "maxiter": 80},
        )
        peak_y = float(optimum.x)
        peak_sigma = float(math.exp(optimum.fun))
        optimizer_success = bool(optimum.success)
    else:
        peak_y = float(positive_y[index])
        peak_sigma = float(positive_sigma[index])
        optimizer_success = True

    return {
        "lineRealPart": alpha,
        "imaginaryWindow": [-y_max, y_max],
        "positiveGridCount": grid_count,
        "coarseGridSpacing": float(positive_y[1] - positive_y[0]),
        "peakImaginaryAbs": peak_y,
        "smallestSingularValue": peak_sigma,
        "resolventNormMaximum": 1.0 / peak_sigma,
        "pseudospectralPeakLog10": -math.log10(peak_sigma),
        "positiveNegativeSymmetryDefectMaximum": float(
            np.max(np.abs(positive_sigma - negative_sigma))
        ),
        "refinementOptimizerSuccess": optimizer_success,
        "finiteSampleAndScalarRefinementOnly": True,
    }


def semigroup_diagnostic(
    matrix: np.ndarray,
    split: dict[str, object],
    base_split: dict[str, object],
    time_grid: np.ndarray,
) -> dict[str, object]:
    basis = split["Z"]
    moving_q = split["Q"]
    fixed_q = base_split["Q"]
    projector = split["P"]
    cluster_value = split["value"]
    restricted = split["Bq"]
    q_alpha = float(np.max(split["qValues"].real))

    time_rows: list[dict[str, float]] = []
    intrinsic_values = []
    moving_values = []
    fixed_values = []
    difference_values = []
    cross_errors = []
    cross_relative_errors = []
    cross_times = {0.0, 40.0, 100.0, float(time_grid[-1])}
    for t in time_grid:
        intrinsic = expm(float(t) * restricted)
        # Exact finite spectral decomposition, evaluated without allowing
        # roundoff from the dominant cluster to pollute the moving Q block.
        moving_operator = (
            basis @ intrinsic @ basis.conjugate().T @ moving_q
        )
        full = (
            np.exp(float(t) * cluster_value) * projector + moving_operator
        )
        intrinsic_norm = opnorm(intrinsic)
        moving_norm = opnorm(moving_operator)
        fixed_norm = opnorm(full @ fixed_q)
        difference_norm = opnorm(full @ (fixed_q - moving_q))
        intrinsic_values.append(intrinsic_norm)
        moving_values.append(moving_norm)
        fixed_values.append(fixed_norm)
        difference_values.append(difference_norm)
        time_rows.append({
            "time": float(t),
            "intrinsicMovingQNorm": intrinsic_norm,
            "ambientMovingQNorm": moving_norm,
            "ambientFixedQ0Norm": fixed_norm,
            "fixedMovingDifferenceNorm": difference_norm,
        })
        if float(t) in cross_times:
            direct_full = expm(float(t) * matrix)
            cross_error = opnorm(full - direct_full)
            cross_errors.append(cross_error)
            cross_relative_errors.append(
                cross_error / max(opnorm(full), np.finfo(float).tiny)
            )

    intrinsic_array = np.asarray(intrinsic_values)
    normalized = intrinsic_array * np.exp(-q_alpha * time_grid)
    peak_index = int(np.argmax(normalized))
    peak_time = float(time_grid[peak_index])
    peak_value = float(normalized[peak_index])

    # Refine only the sampled transient maximum.  This remains a finite-time,
    # binary64 diagnostic and is not a continuous-time certified bound.
    lo = float(time_grid[max(0, peak_index - 1)])
    hi = float(time_grid[min(len(time_grid) - 1, peak_index + 1)])
    if hi > lo and 0 < peak_index < len(time_grid) - 1:
        def normalized_objective(t: float) -> float:
            intrinsic = expm(t * restricted)
            return -opnorm(intrinsic) * math.exp(-q_alpha * t)

        optimum = minimize_scalar(
            normalized_objective,
            bounds=(lo, hi),
            method="bounded",
            options={"xatol": 1e-8, "maxiter": 60},
        )
        if optimum.success:
            peak_time = float(optimum.x)
            peak_value = float(-optimum.fun)

    tail_mask = time_grid >= 0.6 * float(time_grid[-1])
    tail_slope, tail_intercept = np.polyfit(
        time_grid[tail_mask], np.log(intrinsic_array[tail_mask]), 1
    )
    sampled_rate = q_alpha + 0.005
    sampled_constant = float(np.max(
        intrinsic_array * np.exp(-sampled_rate * time_grid)
    ))

    return {
        "qSpectralAbscissa": q_alpha,
        "classificationOnThisFiniteCompression": (
            "growth" if q_alpha > 0.0 else "decay"
        ),
        "timeGrid": {
            "minimum": float(time_grid[0]),
            "maximum": float(time_grid[-1]),
            "step": float(time_grid[1] - time_grid[0]),
            "count": int(len(time_grid)),
        },
        "rows": time_rows,
        "intrinsicMovingQ": {
            "maximumOnGrid": float(np.max(intrinsic_array)),
            "maximumTimeOnGrid": float(time_grid[int(np.argmax(intrinsic_array))]),
            "endpointNorm": float(intrinsic_array[-1]),
            "spectralAbscissaNormalizedPeak": peak_value,
            "spectralAbscissaNormalizedPeakTime": peak_time,
            "tailLogNormLeastSquaresSlope": float(tail_slope),
            "tailLogNormLeastSquaresIntercept": float(tail_intercept),
            "tailFitStartsAt": float(time_grid[tail_mask][0]),
            "sampledEnvelopeRate": sampled_rate,
            "sampledEnvelopeConstant": sampled_constant,
            "sampledStatement": (
                "norm <= constant*exp(rate*t) only at stored grid points"
            ),
        },
        "ambientMovingQ": {
            "maximumOnGrid": float(np.max(moving_values)),
            "endpointNorm": float(moving_values[-1]),
        },
        "ambientFixedQ0": {
            "maximumOnGrid": float(np.max(fixed_values)),
            "endpointNorm": float(fixed_values[-1]),
        },
        "fixedMovingDifference": {
            "maximumOnGrid": float(np.max(difference_values)),
            "endpointNorm": float(difference_values[-1]),
            "endpointRelativeToMoving": float(
                difference_values[-1] / moving_values[-1]
            ),
        },
        "spectralDecompositionVsDirectFullExponentialMaximumAbsoluteError": float(
            max(cross_errors)
        ),
        "spectralDecompositionVsDirectFullExponentialMaximumRelativeError": float(
            max(cross_relative_errors)
        ),
        "continuousTimeBoundCertified": False,
    }


def row_diagnostic(
    N: int,
    epsilon: float,
    base_split: dict[str, object],
    vertical_lines: list[float],
    time_grid: np.ndarray,
) -> dict[str, object]:
    row_start = time.perf_counter()
    matrix = matrix_recurrence(N, epsilon)
    split = spectral_split(matrix)
    projector = split["P"]
    complement = split["Q"]
    base_p = base_split["P"]
    base_q = base_split["Q"]
    value = split["value"]
    q_values = split["qValues"]

    emit(
        "row-split-complete",
        N=N,
        epsilon=epsilon,
        clusterReal=float(value.real),
        qSpectralAbscissa=float(np.max(q_values.real)),
    )
    resolvent = [
        resolvent_peak(
            split["Bq"], alpha, ARGS.imaginary_maximum,
            ARGS.imaginary_grid_count,
        )
        for alpha in vertical_lines
    ]
    emit(
        "row-resolvent-complete",
        N=N,
        epsilon=epsilon,
        peaks={
            str(item["lineRealPart"]): item["resolventNormMaximum"]
            for item in resolvent
        },
    )
    semigroup = semigroup_diagnostic(matrix, split, base_split, time_grid)

    result = {
        "N": N,
        "dimension": 2 * N + 1,
        "epsilon": epsilon,
        "clusterEigenvalue": complex_record(value),
        "clusterLeftRightPairingAbs": float(abs(split["pairing"])),
        "clusterProjectorNorm": opnorm(projector),
        "qProjectorNorm": opnorm(complement),
        "movingVsFixed": {
            "projectorDifferenceNorm": opnorm(projector - base_p),
            "complementDifferenceNorm": opnorm(complement - base_q),
            "movingPFromFixedQLeakageNorm": opnorm(projector @ base_q),
            "movingQFromFixedPLeakageNorm": opnorm(complement @ base_p),
            "fixedPToFixedQCouplingNorm": opnorm(base_q @ matrix @ base_p),
            "fixedQToFixedPCouplingNorm": opnorm(base_p @ matrix @ base_q),
            "movingPToMovingQCouplingNorm": opnorm(
                complement @ matrix @ projector
            ),
            "movingQToMovingPCouplingNorm": opnorm(
                projector @ matrix @ complement
            ),
        },
        "qSpectrum": {
            "spectralAbscissa": float(np.max(q_values.real)),
            "numberWithRealPartAbove1eMinus10": int(
                np.count_nonzero(q_values.real > 1e-10)
            ),
            "sixRightmost": [complex_record(item) for item in q_values[:6]],
        },
        "resolventVerticalLines": resolvent,
        "semigroup": semigroup,
        "residuals": {
            "rightEigenpair": float(np.linalg.norm(
                matrix @ split["right"] - value * split["right"]
            )),
            "leftEigenpair": float(np.linalg.norm(
                matrix.conjugate().T @ split["left"]
                - value.conjugate() * split["left"]
            )),
            "projectorIdempotence": opnorm(projector @ projector - projector),
            "projectorCommutator": opnorm(matrix @ projector - projector @ matrix),
            "qBasisInvariance": opnorm(
                matrix @ split["Z"] - split["Z"] @ split["Bq"]
            ),
        },
        "rowWallTimeSeconds": time.perf_counter() - row_start,
        "finiteBinary64Only": True,
    }
    emit(
        "row-complete",
        N=N,
        epsilon=epsilon,
        qSpectralAbscissa=result["qSpectrum"]["spectralAbscissa"],
        transientPeak=(
            result["semigroup"]["intrinsicMovingQ"]
            ["spectralAbscissaNormalizedPeak"]
        ),
        wallTimeSeconds=result["rowWallTimeSeconds"],
    )
    return result


def main() -> int:
    cutoffs = [int(item) for item in ARGS.cutoffs.split(",")]
    epsilons = [float(item) for item in ARGS.epsilons.split(",")]
    vertical_lines = [float(item) for item in ARGS.vertical_lines.split(",")]
    time_grid = np.arange(
        0.0, ARGS.time_maximum + 0.5 * ARGS.time_step, ARGS.time_step
    )
    if sorted(set(cutoffs)) != cutoffs or cutoffs[0] < 8:
        raise ValueError("cutoffs must be distinct, increasing, and at least 8")
    if any(epsilon <= 0.0 for epsilon in epsilons):
        raise ValueError("this diagnostic requires strictly positive epsilon")
    if any(alpha <= 0.0 for alpha in vertical_lines):
        raise ValueError("vertical lines must lie in the right half-plane")
    if ARGS.imaginary_grid_count < 11 or ARGS.time_step <= 0.0:
        raise ValueError("diagnostic grids are too small")

    ARGS.output.parent.mkdir(parents=True, exist_ok=True)
    ARGS.environment.parent.mkdir(parents=True, exist_ok=True)
    ARGS.progress.parent.mkdir(parents=True, exist_ok=True)
    ARGS.progress.write_text("", encoding="utf-8")

    environment = {
        "schemaVersion": "r073e-finite-environment-v1",
        "createdUtc": now_utc(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "logicalCpuCount": os.cpu_count(),
        "python": platform.python_version(),
        "pythonImplementation": platform.python_implementation(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "precision": "numpy.complex128 / IEEE-754 binary64 components",
        "blasThreadEnvironment": {
            key: os.environ.get(key)
            for key in (
                "OMP_NUM_THREADS",
                "OPENBLAS_NUM_THREADS",
                "VECLIB_MAXIMUM_THREADS",
            )
        },
        "randomSeed": None,
        "randomnessUsed": False,
        "executionMode": "local dense CPU linear algebra",
        "dgxUsed": False,
        "dgxReason": (
            "matrices are at most 193 by 193; transfer and container overhead "
            "would exceed the measured local dense solve time"
        ),
        "claimBoundary": {
            "finiteDimensionalOnly": True,
            "intervalArithmetic": False,
            "tailBound": False,
            "continuumDichotomyCertified": False,
            "continuousTimeSemigroupBoundCertified": False,
        },
    }
    ARGS.environment.write_text(
        json.dumps(environment, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    emit(
        "start",
        cutoffs=cutoffs,
        epsilons=epsilons,
        verticalLines=vertical_lines,
        imaginaryWindow=[-ARGS.imaginary_maximum, ARGS.imaginary_maximum],
        timeMaximum=ARGS.time_maximum,
        timeStep=ARGS.time_step,
        finiteBinary64Only=True,
    )
    rows = []
    total_rows = len(cutoffs) * len(epsilons)
    for N in cutoffs:
        base_matrix = matrix_recurrence(N, 0.0)
        base_split = spectral_split(base_matrix)
        emit(
            "cutoff-start",
            N=N,
            dimension=2 * N + 1,
            inviscidClusterReal=float(base_split["value"].real),
        )
        for epsilon in epsilons:
            rows.append(row_diagnostic(
                N, epsilon, base_split, vertical_lines, time_grid
            ))
            elapsed = time.perf_counter() - START
            rate = elapsed / len(rows)
            emit(
                "progress",
                completedRows=len(rows),
                totalRows=total_rows,
                estimatedRemainingSeconds=rate * (total_rows - len(rows)),
            )
        emit("cutoff-complete", N=N, completedRows=len(rows))

    by_key = {(row["N"], row["epsilon"]): row for row in rows}
    largest = cutoffs[-1]
    previous = cutoffs[-2] if len(cutoffs) >= 2 else None
    comparisons = []
    for epsilon in epsilons if previous is not None else []:
        a = by_key[(largest, epsilon)]
        b = by_key[(previous, epsilon)]
        line_comparisons = []
        for line_a, line_b in zip(
            a["resolventVerticalLines"], b["resolventVerticalLines"]
        ):
            line_comparisons.append({
                "lineRealPart": line_a["lineRealPart"],
                "resolventPeakRelativeDifference": abs(
                    line_a["resolventNormMaximum"]
                    - line_b["resolventNormMaximum"]
                ) / line_a["resolventNormMaximum"],
                "peakImaginaryAbsDifference": abs(
                    line_a["peakImaginaryAbs"]
                    - line_b["peakImaginaryAbs"]
                ),
            })
        comparisons.append({
            "epsilon": epsilon,
            "cutoffs": [previous, largest],
            "qSpectralAbscissaAbsoluteDifference": abs(
                a["qSpectrum"]["spectralAbscissa"]
                - b["qSpectrum"]["spectralAbscissa"]
            ),
            "clusterEigenvalueAbsoluteDifference": abs(
                complex(**{
                    "real": a["clusterEigenvalue"]["real"],
                    "imag": a["clusterEigenvalue"]["imag"],
                })
                - complex(**{
                    "real": b["clusterEigenvalue"]["real"],
                    "imag": b["clusterEigenvalue"]["imag"],
                })
            ),
            "projectorDifferenceAbsoluteDifference": abs(
                a["movingVsFixed"]["projectorDifferenceNorm"]
                - b["movingVsFixed"]["projectorDifferenceNorm"]
            ),
            "normalizedTransientPeakRelativeDifference": abs(
                a["semigroup"]["intrinsicMovingQ"]
                ["spectralAbscissaNormalizedPeak"]
                - b["semigroup"]["intrinsicMovingQ"]
                ["spectralAbscissaNormalizedPeak"]
            ) / a["semigroup"]["intrinsicMovingQ"][
                "spectralAbscissaNormalizedPeak"
            ],
            "verticalLines": line_comparisons,
        })

    largest_rows = [row for row in rows if row["N"] == largest]
    residual_max = max(
        max(row["residuals"].values()) for row in rows
    )
    q_alpha_cutoff_max = max(
        (
            item["qSpectralAbscissaAbsoluteDifference"]
            for item in comparisons
        ),
        default=0.0,
    )
    line_margin_min = min(
        line["lineRealPart"] - row["qSpectrum"]["spectralAbscissa"]
        for row in rows for line in row["resolventVerticalLines"]
    )
    all_largest_q_grow = all(
        row["qSpectrum"]["spectralAbscissa"] > 0.0
        for row in largest_rows
    )
    checks = {
        "allSelectedVerticalLinesRightOfFiniteQSpectrum": line_margin_min > 0.0,
        "largestCutoffComplementHasPositiveSpectralAbscissa": all_largest_q_grow,
        "largestCutoffHasAtLeastOneAdditionalUnstableConjugatePair": all(
            row["qSpectrum"]["numberWithRealPartAbove1eMinus10"] >= 2
            for row in largest_rows
        ),
        "largestTwoCutoffsQSpectralAbscissaAgreeBelow1eMinus6": (
            previous is None or q_alpha_cutoff_max < 1e-6
        ),
        "algebraicResidualsBelow1eMinus10": residual_max < 1e-10,
        "movingAndFixedProjectorComplementDifferencesAgree": all(
            abs(
                row["movingVsFixed"]["projectorDifferenceNorm"]
                - row["movingVsFixed"]["complementDifferenceNorm"]
            ) < 2e-12
            for row in rows
        ),
    }
    total_wall = time.perf_counter() - START
    payload = {
        "schemaVersion": "r073e-finite-complement-diagnostic-v1",
        "release": "R0.73E-exploratory",
        "createdUtc": now_utc(),
        "parameters": {
            "gamma": GAMMA,
            "mu": MU,
            "cutoffs": cutoffs,
            "epsilons": epsilons,
            "verticalLines": vertical_lines,
            "imaginaryWindow": [
                -ARGS.imaginary_maximum, ARGS.imaginary_maximum
            ],
            "imaginaryPositiveGridCount": ARGS.imaginary_grid_count,
            "timeMaximum": ARGS.time_maximum,
            "timeStep": ARGS.time_step,
            "clusterSelection": "unique finite eigenvalue with largest real part",
            "space": "U_mu X_mu = L2 finite Fourier compression",
        },
        "sourceBinding": {
            "path": "experiments/r073e/diagnose_complement.py",
            "sha256": sha256(SOURCE),
        },
        "environment": environment,
        "rows": rows,
        "largestTwoCutoffComparisons": comparisons,
        "maximums": {
            "allAlgebraicResiduals": residual_max,
            "largestTwoCutoffsQSpectralAbscissaDifference": q_alpha_cutoff_max,
            "minimumVerticalLineMarginOverFiniteQSpectrum": line_margin_min,
            "wallTimeSeconds": total_wall,
        },
        "checks": checks,
        "allChecksPass": bool(all(checks.values())),
        "stageFinding": {
            "finiteMovingComplementIsStable": False,
            "finiteMovingComplementContainsAdditionalUnstablePair": True,
            "consequence": (
                "A decay estimate for Q_epsilon=I-P_epsilon is incompatible "
                "with these finite spectra; a continuum theorem must either "
                "enlarge the unstable projection or permit positive Q growth."
            ),
        },
        "claimBoundary": {
            "finiteBinary64Diagnostic": True,
            "ordinaryCutoffAgreementIsContinuumProof": False,
            "additionalContinuumEigenpairProvedHere": False,
            "continuumComplementaryDichotomyProvedHere": False,
            "continuousTimeSemigroupBoundProvedHere": False,
            "movingProfileUniformityProvedHere": False,
            "nonautonomousTransferProvedHere": False,
            "nonlinearNavierStokesProvedHere": False,
            "clayProblemSolved": False,
        },
    }
    ARGS.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    emit(
        "complete",
        output=str(ARGS.output),
        rows=len(rows),
        allChecksPass=payload["allChecksPass"],
        finiteMovingComplementIsStable=False,
        wallTimeSeconds=total_wall,
    )
    return 0 if payload["allChecksPass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
