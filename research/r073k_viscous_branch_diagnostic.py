#!/usr/bin/env python3
"""Finite Fourier diagnostics for the R0.73K uniform viscous branch.

The primary matrix is assembled from the four-term column recurrence for the
raw-vorticity operator and then conjugated by the exact kinetic-space isometry
to L2.  Every result produced here concerns a finite Fourier compression.  In
particular, fixed-circle counts, cutoff agreement, and small residuals do not
prove the continuum Riesz-projection theorem or any Navier--Stokes regularity
claim.
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
import resource
import sys
import time
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default=os.environ.get("R073K_DEPS", ""))
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--progress", type=Path, required=True)
    parser.add_argument("--resources", type=Path, required=True)
    parser.add_argument("--environment", type=Path, required=True)
    return parser.parse_args()


ARGS = parse_args()
if ARGS.deps:
    sys.path.insert(0, ARGS.deps)

import numpy as np  # noqa: E402
import scipy  # noqa: E402
from scipy.linalg import eig  # noqa: E402


SOURCE = Path(__file__).resolve()
START_MONOTONIC = time.monotonic()


class DiagnosticFailure(RuntimeError):
    """A fail-closed configuration or fixed-contour failure."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise DiagnosticFailure(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(canonical_json(value), encoding="utf-8")
    os.replace(temporary, path)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Monitor:
    def __init__(self, progress: Path, resources: Path) -> None:
        self.progress = progress
        self.resources = resources
        for path in (progress, resources):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("", encoding="utf-8")

    def emit(self, event: str, **fields: object) -> None:
        row = {
            "event": event,
            "timestampUtc": utc_now(),
            "elapsedSeconds": time.monotonic() - START_MONOTONIC,
            **fields,
        }
        with self.progress.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(row, sort_keys=True) + "\n")
        print(json.dumps(row, sort_keys=True), file=sys.stderr, flush=True)

    def sample(self, event: str, **fields: object) -> None:
        usage = resource.getrusage(resource.RUSAGE_SELF)
        try:
            load_average: list[float] | None = list(os.getloadavg())
        except OSError:
            load_average = None
        row = {
            "event": event,
            "timestampUtc": utc_now(),
            "elapsedSeconds": time.monotonic() - START_MONOTONIC,
            "userCpuSeconds": usage.ru_utime,
            "systemCpuSeconds": usage.ru_stime,
            "maximumResidentSetSizePlatformUnits": usage.ru_maxrss,
            "loadAverage": load_average,
            **fields,
        }
        with self.resources.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(row, sort_keys=True) + "\n")


def complex_record(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imag": float(value.imag)}


def load_configuration(path: Path) -> dict[str, Any]:
    config = json.loads(path.read_text(encoding="utf-8"))
    require(config.get("schemaVersion") == "r073k-viscous-branch-config-v1",
            "configuration schema mismatch")
    require(float(config["gamma"]) == 0.5,
            "R0.73K freezes gamma=1/2")
    cutoffs = config["cutoffs"]
    require(cutoffs == sorted(set(cutoffs)) and len(cutoffs) >= 2,
            "cutoffs must be distinct and increasing")
    require(all(type(value) is int and value >= 8 for value in cutoffs),
            "every cutoff must be an integer at least eight")
    d_grid = config["dGrid"]
    require(len(d_grid) >= 2, "the parameter grid needs at least two nodes")
    d_values = [float(row["value"]) for row in d_grid]
    require(d_values == sorted(set(d_values)),
            "d-grid values must be distinct and increasing")
    require(d_values[0] == 0.0 and d_values[-1] == 1.0 / 450.0,
            "d-grid endpoints must be 0 and 1/450")
    core = [float(value) for value in config["coreEpsilons"]]
    stress = [float(value) for value in config["stressEpsilons"]]
    require(core == sorted(set(core)) and core[0] == 0.0,
            "core viscosities must be distinct, increasing, and begin at zero")
    require(core[-1] <= float(config["coreMaximumEpsilon"]),
            "a core viscosity exceeds the frozen core maximum")
    require(stress == sorted(set(stress)) and bool(stress),
            "stress viscosities must be distinct and increasing")
    require(stress[0] > core[-1],
            "stress viscosities must follow the core grid")
    contour = config["fixedContour"]
    require(float(contour["radius"]) > 0.0,
            "fixed contour radius must be positive")
    require(int(config["embeddingPadding"]) >= 2,
            "embedding padding must cover both Fourier shifts")
    return config


def recurrence_kinetic_matrix(
    cutoff: int,
    d_value: float,
    epsilon: float,
    gamma: float,
) -> np.ndarray:
    """Build the finite matrix from the four-term column recurrence."""
    mu = gamma * gamma
    first_scale = math.exp(-d_value)
    second_scale = math.exp(-4.0 * d_value)
    dimension = 2 * cutoff + 1
    raw = np.zeros((dimension, dimension), dtype=np.complex128)
    for column, n in enumerate(range(-cutoff, cutoff + 1)):
        ell = n * n + mu
        first = gamma * first_scale * 0.25 * (1.0 - 1.0 / ell)
        second = gamma * second_scale * (-0.125 + 0.5 / ell)
        for shift, coefficient in (
            (1, first), (-1, -first),
            (2, second), (-2, -second),
        ):
            m = n + shift
            if -cutoff <= m <= cutoff:
                raw[m + cutoff, column] = coefficient

    modes = np.arange(-cutoff, cutoff + 1, dtype=float)
    ell = modes * modes + mu
    matrix = ((1.0 / np.sqrt(ell))[:, None]
              * raw
              * np.sqrt(ell)[None, :])
    matrix -= epsilon * np.diag(ell)
    return matrix


def low_rank_operator_norm(left: np.ndarray, right: np.ndarray) -> float:
    """Return ||left right^*||_2 using only a small dense core."""
    q_left, r_left = np.linalg.qr(left, mode="reduced")
    q_right, r_right = np.linalg.qr(right, mode="reduced")
    del q_left, q_right
    core = r_left @ r_right.conjugate().T
    return float(np.linalg.norm(core, ord=2))


def projector_difference(
    left_state: dict[str, Any],
    right_state: dict[str, Any],
    target_cutoff: int | None = None,
) -> float:
    """Operator norm of two rank-one projectors, with optional zero embedding."""
    if target_cutoff is None:
        target_cutoff = int(left_state["cutoff"])
    target_dimension = 2 * target_cutoff + 1

    def embed(vector: np.ndarray, cutoff: int) -> np.ndarray:
        result = np.zeros(target_dimension, dtype=np.complex128)
        offset = target_cutoff - cutoff
        require(offset >= 0, "cannot embed a larger cutoff into a smaller one")
        result[offset:offset + vector.size] = vector
        return result

    r_left = embed(left_state["right"], int(left_state["cutoff"]))
    l_left = embed(left_state["left"], int(left_state["cutoff"]))
    r_right = embed(right_state["right"], int(right_state["cutoff"]))
    l_right = embed(right_state["left"], int(right_state["cutoff"]))
    factors_left = np.column_stack((
        r_left / left_state["pairing"],
        -r_right / right_state["pairing"],
    ))
    factors_right = np.column_stack((l_left, l_right))
    return low_rank_operator_norm(factors_left, factors_right)


def solve_state(
    cutoff: int,
    d_value: float,
    epsilon: float,
    gamma: float,
    contour_center: complex,
    contour_radius: float,
    regime: str,
    previous_value: complex | None,
    padding: int,
) -> dict[str, Any]:
    matrix = recurrence_kinetic_matrix(cutoff, d_value, epsilon, gamma)
    values, left, right = eig(
        matrix, left=True, right=True, check_finite=False,
    )
    distances = np.abs(values - contour_center)
    inside = np.flatnonzero(distances < contour_radius)
    if regime == "core":
        require(
            inside.size == 1,
            f"fixed-circle multiplicity is {inside.size}, not one "
            f"(N={cutoff}, d={d_value:.17g}, epsilon={epsilon:.17g})",
        )
        index = int(inside[0])
        selection_rule = "unique eigenvalue in the fixed circle"
        continuation_distance = None
    else:
        require(previous_value is not None,
                "stress continuation requires a previous branch value")
        index = int(np.argmin(np.abs(values - previous_value)))
        selection_rule = "nearest eigenvalue to previous viscosity branch value"
        continuation_distance = float(abs(values[index] - previous_value))

    value = complex(values[index])
    lvec = left[:, index] / np.linalg.norm(left[:, index])
    rvec = right[:, index] / np.linalg.norm(right[:, index])
    pairing = complex(np.vdot(lvec, rvec))
    require(abs(pairing) > 100.0 * np.finfo(float).eps,
            "selected finite eigenpair is numerically defective")

    algebraic_right_vector = matrix @ rvec - value * rvec
    algebraic_left_vector = (
        matrix.conjugate().T @ lvec - value.conjugate() * lvec
    )
    algebraic_right_residual = float(np.linalg.norm(algebraic_right_vector))
    algebraic_left_residual = float(np.linalg.norm(algebraic_left_vector))
    overlap = float(abs(pairing))
    bp_intertwining_residual = algebraic_right_residual / overlap
    pb_intertwining_residual = algebraic_left_residual / overlap

    # With u=r/<l,r> and v=l, P=u v^*.  Hence
    # P^2-P = u (v^*u-1) v^*.  This rank-one formula evaluates the exact
    # operator norm without forming or multiplying dense projector matrices.
    projector_left_factor = rvec / pairing
    projector_right_factor = lvec
    idempotency_scalar = complex(
        np.vdot(projector_right_factor, projector_left_factor) - 1.0
    )
    projector_idempotency_residual = float(
        abs(idempotency_scalar)
        * np.linalg.norm(projector_left_factor)
        * np.linalg.norm(projector_right_factor)
    )

    larger = recurrence_kinetic_matrix(
        cutoff + padding, d_value, epsilon, gamma,
    )
    padded_right = np.zeros(larger.shape[0], dtype=np.complex128)
    padded_left = np.zeros(larger.shape[0], dtype=np.complex128)
    padded_right[padding:-padding] = rvec
    padded_left[padding:-padding] = lvec
    right_residual = float(np.linalg.norm(larger @ padded_right
                                          - value * padded_right))
    left_residual = float(np.linalg.norm(
        larger.conjugate().T @ padded_left
        - value.conjugate() * padded_left
    ))
    projector_norm = low_rank_operator_norm(
        projector_left_factor[:, None], projector_right_factor[:, None],
    )
    return {
        "cutoff": cutoff,
        "epsilon": epsilon,
        "value": value,
        "left": lvec,
        "right": rvec,
        "pairing": pairing,
        "overlap": overlap,
        "projectorNorm": projector_norm,
        "rightAlgebraicResidual": algebraic_right_residual,
        "leftAlgebraicResidual": algebraic_left_residual,
        "bpMinusLambdaPResidual": bp_intertwining_residual,
        "pbMinusLambdaPResidual": pb_intertwining_residual,
        "projectorIdempotencyResidualLowRank": (
            projector_idempotency_residual
        ),
        "rightEmbeddedResidual": right_residual,
        "leftEmbeddedResidual": left_residual,
        "fixedContourCount": int(inside.size),
        "insideFixedContour": bool(abs(value - contour_center) < contour_radius),
        "selectionRule": selection_rule,
        "continuationDistance": continuation_distance,
    }


def public_row(
    state: dict[str, Any],
    base: dict[str, Any],
    d_index: int,
    d_label: str,
    d_value: float,
    gamma: float,
    regime: str,
) -> dict[str, Any]:
    epsilon = float(state["epsilon"])
    value = complex(state["value"])
    value0 = complex(base["value"])
    modes = np.arange(-int(state["cutoff"]), int(state["cutoff"]) + 1,
                      dtype=float)
    ell = modes * modes + gamma * gamma
    l0 = base["left"]
    r0 = base["right"]
    r_eps = state["right"]
    denominator = complex(np.vdot(l0, r_eps))
    first_order = -complex(np.vdot(l0, ell * r0)) / complex(np.vdot(l0, r0))
    if epsilon == 0.0:
        quotient = None
        exact_quotient = None
        quotient_formula_difference = None
        quotient_first_order_difference = None
        identity_residual = 0.0
    else:
        quotient_value = (value - value0) / epsilon
        exact_value = -complex(np.vdot(l0, ell * r_eps)) / denominator
        quotient = complex_record(quotient_value)
        exact_quotient = complex_record(exact_value)
        quotient_formula_difference = float(abs(quotient_value - exact_value))
        quotient_first_order_difference = float(abs(quotient_value - first_order))
        identity_residual = float(abs(
            (value - value0) * denominator
            + epsilon * complex(np.vdot(l0, ell * r_eps))
        ))
    projector_difference_from_zero = (
        0.0 if epsilon == 0.0 else projector_difference(state, base)
    )
    return {
        "dIndex": d_index,
        "dLabel": d_label,
        "d": d_value,
        "N": int(state["cutoff"]),
        "dimension": 2 * int(state["cutoff"]) + 1,
        "epsilon": epsilon,
        "regime": regime,
        "selectionRule": state["selectionRule"],
        "continuationDistance": state["continuationDistance"],
        "fixedContourEigenvalueCount": state["fixedContourCount"],
        "selectedInsideFixedContour": state["insideFixedContour"],
        "lambda": complex_record(value),
        "rightEmbeddedResidual": state["rightEmbeddedResidual"],
        "leftEmbeddedResidual": state["leftEmbeddedResidual"],
        "rightAlgebraicResidual": state["rightAlgebraicResidual"],
        "leftAlgebraicResidual": state["leftAlgebraicResidual"],
        "bpMinusLambdaPResidual": state["bpMinusLambdaPResidual"],
        "pbMinusLambdaPResidual": state["pbMinusLambdaPResidual"],
        "projectorIdempotencyResidualLowRank": state[
            "projectorIdempotencyResidualLowRank"
        ],
        "projectorIdempotencyFormula": (
            "P=u v*, u=r/<l,r>, v=l; ||P^2-P||="
            "|<v,u>-1| ||u|| ||v||"
        ),
        "leftRightOverlap": state["overlap"],
        "projectorNorm": state["projectorNorm"],
        "projectorNormMinusReciprocalOverlap": float(
            state["projectorNorm"] - 1.0 / state["overlap"]
        ),
        "projectorDifferenceFromEpsilonZero": projector_difference_from_zero,
        "lambdaDifferenceOverEpsilon": quotient,
        "exactInviscidAdjointQuotient": exact_quotient,
        "firstOrderAdjointFormulaAtZero": complex_record(first_order),
        "quotientMinusExactAdjointFormulaAbs": quotient_formula_difference,
        "quotientMinusFirstOrderFormulaAbs": quotient_first_order_difference,
        "unscaledAdjointIdentityResidual": identity_residual,
        "finiteKineticCompressionOnly": True,
    }


def environment_payload(config: Path) -> dict[str, Any]:
    return {
        "schemaVersion": "r073k-finite-diagnostic-environment-v1",
        "createdUtc": utc_now(),
        "python": platform.python_version(),
        "pythonImplementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "configurationSha256": sha256(config),
        "threadEnvironment": {
            key: os.environ.get(key)
            for key in (
                "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS",
                "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS",
            )
        },
        "claimBoundary": {
            "finiteDimensionalOnly": True,
            "continuumTheoremCertifiedByThisEnvironment": False,
        },
    }


def failure_payload(config: Path, message: str) -> dict[str, Any]:
    return {
        "schemaVersion": "r073k-viscous-branch-diagnostic-v1",
        "release": "R0.73K",
        "status": "failed",
        "failure": message,
        "sourceBinding": {
            "path": "research/r073k_viscous_branch_diagnostic.py",
            "sha256": sha256(SOURCE),
        },
        "configurationBinding": {
            "path": str(config),
            "sha256": sha256(config) if config.is_file() else None,
        },
        "claimBoundary": {
            "finiteDimensionalOnly": True,
            "continuumUniformViscousBranchProvedHere": False,
            "clayProblemSolved": False,
        },
    }


def run(monitor: Monitor) -> int:
    config = load_configuration(ARGS.config)
    atomic_json(ARGS.environment, environment_payload(ARGS.config))
    gamma = float(config["gamma"])
    contour = config["fixedContour"]
    contour_center = complex(float(contour["centerReal"]),
                             float(contour["centerImag"]))
    contour_radius = float(contour["radius"])
    padding = int(config["embeddingPadding"])
    core_epsilons = [float(value) for value in config["coreEpsilons"]]
    stress_epsilons = [float(value) for value in config["stressEpsilons"]]
    all_epsilons = core_epsilons + stress_epsilons
    cutoffs = [int(value) for value in config["cutoffs"]]
    d_grid = config["dGrid"]
    tolerances = config["tolerances"]
    monitor.emit(
        "start", cutoffs=cutoffs, dGrid=d_grid,
        coreEpsilons=core_epsilons, stressEpsilons=stress_epsilons,
        fixedContour=contour, finiteDimensionalOnly=True,
    )
    monitor.sample("start")

    rows: list[dict[str, Any]] = []
    states: dict[tuple[int, int, float], dict[str, Any]] = {}
    for cutoff in cutoffs:
        monitor.emit("cutoff-start", N=cutoff, dimension=2 * cutoff + 1)
        for d_index, d_row in enumerate(d_grid):
            d_label = str(d_row["label"])
            d_value = float(d_row["value"])
            monitor.emit("parameter-start", N=cutoff, dIndex=d_index,
                         dLabel=d_label, d=d_value)
            base: dict[str, Any] | None = None
            previous: dict[str, Any] | None = None
            for epsilon in all_epsilons:
                regime = "core" if epsilon in core_epsilons else "stress"
                state = solve_state(
                    cutoff, d_value, epsilon, gamma,
                    contour_center, contour_radius, regime,
                    None if previous is None else complex(previous["value"]),
                    padding,
                )
                if epsilon == 0.0:
                    base = state
                require(base is not None, "zero-viscosity state was not computed first")
                row = public_row(
                    state, base, d_index, d_label, d_value, gamma, regime,
                )
                rows.append(row)
                states[(cutoff, d_index, epsilon)] = state
                previous = state
                monitor.emit(
                    "eigenpair", N=cutoff, dIndex=d_index, dLabel=d_label,
                    epsilon=epsilon, regime=regime,
                    lambdaReal=row["lambda"]["real"],
                    lambdaImag=row["lambda"]["imag"],
                    fixedContourCount=row["fixedContourEigenvalueCount"],
                    insideFixedContour=row["selectedInsideFixedContour"],
                    rightEmbeddedResidual=row["rightEmbeddedResidual"],
                    leftEmbeddedResidual=row["leftEmbeddedResidual"],
                    rightAlgebraicResidual=row["rightAlgebraicResidual"],
                    leftAlgebraicResidual=row["leftAlgebraicResidual"],
                    bpMinusLambdaPResidual=row["bpMinusLambdaPResidual"],
                    pbMinusLambdaPResidual=row["pbMinusLambdaPResidual"],
                    projectorIdempotencyResidual=row[
                        "projectorIdempotencyResidualLowRank"
                    ],
                    overlap=row["leftRightOverlap"],
                    projectorNorm=row["projectorNorm"],
                    projectorDifference=row[
                        "projectorDifferenceFromEpsilonZero"
                    ],
                    finiteDimensionalOnly=True,
                )
                monitor.sample("eigenpair", N=cutoff, dIndex=d_index,
                               epsilon=epsilon)
            monitor.emit("parameter-complete", N=cutoff, dIndex=d_index,
                         dLabel=d_label)
        monitor.emit("cutoff-complete", N=cutoff)

    cross_cutoff: list[dict[str, Any]] = []
    for small, large in zip(cutoffs[:-1], cutoffs[1:]):
        for d_index, d_row in enumerate(d_grid):
            for epsilon in all_epsilons:
                small_state = states[(small, d_index, epsilon)]
                large_state = states[(large, d_index, epsilon)]
                cross_cutoff.append({
                    "smallN": small,
                    "largeN": large,
                    "dIndex": d_index,
                    "dLabel": str(d_row["label"]),
                    "d": float(d_row["value"]),
                    "epsilon": epsilon,
                    "regime": "core" if epsilon in core_epsilons else "stress",
                    "lambdaAbsoluteDifference": float(abs(
                        complex(small_state["value"])
                        - complex(large_state["value"])
                    )),
                    "embeddedProjectorDifference": projector_difference(
                        small_state, large_state, target_cutoff=large,
                    ),
                    "finiteKineticCompressionOnly": True,
                })
        monitor.emit("cross-cutoff-complete", smallN=small, largeN=large)
        monitor.sample("cross-cutoff", smallN=small, largeN=large)

    core_rows = [row for row in rows if row["regime"] == "core"]
    positive_core_rows = [row for row in core_rows if row["epsilon"] > 0.0]
    largest = cutoffs[-1]
    previous = cutoffs[-2]
    terminal_cross = [
        row for row in cross_cutoff
        if row["smallN"] == previous and row["largeN"] == largest
        and row["regime"] == "core"
    ]
    maximums = {
        "coreLambdaImaginaryAbs": max(abs(row["lambda"]["imag"])
                                      for row in core_rows),
        "projectorNormReciprocalOverlapErrorAbs": max(abs(
            row["projectorNormMinusReciprocalOverlap"]
        ) for row in rows),
        "coreUnscaledAdjointIdentityResidual": max(
            row["unscaledAdjointIdentityResidual"]
            for row in positive_core_rows
        ),
        "coreQuotientExactFormulaDifferenceAbs": max(
            row["quotientMinusExactAdjointFormulaAbs"]
            for row in positive_core_rows
        ),
        "rightAlgebraicResidual": max(
            row["rightAlgebraicResidual"] for row in rows
        ),
        "leftAlgebraicResidual": max(
            row["leftAlgebraicResidual"] for row in rows
        ),
        "bpMinusLambdaPResidual": max(
            row["bpMinusLambdaPResidual"] for row in rows
        ),
        "pbMinusLambdaPResidual": max(
            row["pbMinusLambdaPResidual"] for row in rows
        ),
        "projectorIdempotencyResidualLowRank": max(
            row["projectorIdempotencyResidualLowRank"] for row in rows
        ),
        "largestCutoffCoreRightEmbeddedResidual": max(
            row["rightEmbeddedResidual"] for row in core_rows
            if row["N"] == largest
        ),
        "largestCutoffCoreLeftEmbeddedResidual": max(
            row["leftEmbeddedResidual"] for row in core_rows
            if row["N"] == largest
        ),
        "largestTwoCutoffsCoreEigenvalueDifference": max(
            row["lambdaAbsoluteDifference"] for row in terminal_cross
        ),
        "largestTwoCutoffsCoreEmbeddedProjectorDifference": max(
            row["embeddedProjectorDifference"] for row in terminal_cross
        ),
    }
    checks = {
        "coreFixedContourMultiplicityExactlyOne": all(
            row["fixedContourEigenvalueCount"] == 1 for row in core_rows
        ),
        "coreSelectedEigenvaluesInsideFixedContour": all(
            row["selectedInsideFixedContour"] for row in core_rows
        ),
        "stressRowsUseContinuationRatherThanCircleFallback": all(
            row["regime"] != "stress"
            or row["selectionRule"].startswith("nearest eigenvalue")
            for row in rows
        ),
        "coreEigenvaluesNumericallyReal": (
            maximums["coreLambdaImaginaryAbs"]
            <= float(tolerances["numericalReality"])
        ),
        "projectorNormEqualsReciprocalOverlap": (
            maximums["projectorNormReciprocalOverlapErrorAbs"]
            <= float(tolerances["projectorIdentity"])
        ),
        "unscaledAdjointIdentityCloses": (
            maximums["coreUnscaledAdjointIdentityResidual"]
            <= float(tolerances["unscaledAdjointIdentity"])
        ),
        "rightAndLeftAlgebraicResidualsClose": (
            max(maximums["rightAlgebraicResidual"],
                maximums["leftAlgebraicResidual"])
            <= float(tolerances["unscaledAdjointIdentity"])
        ),
        "rankOneIntertwiningResidualsClose": (
            max(maximums["bpMinusLambdaPResidual"],
                maximums["pbMinusLambdaPResidual"])
            <= float(tolerances["unscaledAdjointIdentity"])
        ),
        "rankOneProjectorIdempotencyCloses": (
            maximums["projectorIdempotencyResidualLowRank"]
            <= float(tolerances["projectorIdentity"])
        ),
        "allReportedScalarsFinite": all(
            math.isfinite(float(row[field]))
            for row in rows
            for field in (
                "rightEmbeddedResidual", "leftEmbeddedResidual",
                "rightAlgebraicResidual", "leftAlgebraicResidual",
                "bpMinusLambdaPResidual", "pbMinusLambdaPResidual",
                "projectorIdempotencyResidualLowRank",
                "leftRightOverlap", "projectorNorm",
                "projectorDifferenceFromEpsilonZero",
                "unscaledAdjointIdentityResidual",
            )
        ),
    }
    all_checks_pass = bool(all(checks.values()))
    payload = {
        "schemaVersion": "r073k-viscous-branch-diagnostic-v1",
        "release": "R0.73K",
        "createdUtc": utc_now(),
        "status": "passed" if all_checks_pass else "failed",
        "sourceBinding": {
            "path": "research/r073k_viscous_branch_diagnostic.py",
            "sha256": sha256(SOURCE),
        },
        "configurationBinding": {
            "path": str(ARGS.config),
            "sha256": sha256(ARGS.config),
        },
        "parameters": {
            "gamma": gamma,
            "mu": gamma * gamma,
            "cutoffs": cutoffs,
            "dGrid": d_grid,
            "coreEpsilons": core_epsilons,
            "stressEpsilons": stress_epsilons,
            "fixedContour": contour,
            "coreSelectionRule": "exactly one eigenvalue in fixed circle; fail closed otherwise",
            "stressSelectionRule": "nearest-eigenvalue continuation from the preceding viscosity",
            "matrixConstruction": "four-term raw-vorticity recurrence followed by kinetic L2 conjugation",
        },
        "rows": rows,
        "crossCutoffComparisons": cross_cutoff,
        "maximums": maximums,
        "checks": checks,
        "allChecksPass": all_checks_pass,
        "claimBoundary": {
            "finiteKineticCompressionComputed": True,
            "bothEmbeddedResidualsComputed": True,
            "bothAlgebraicResidualsComputed": True,
            "finiteIntertwiningResidualsComputed": True,
            "finiteProjectorIdempotencyCheckedByLowRankFormula": True,
            "finiteProjectorDifferencesComputed": True,
            "finiteAdjointIdentityChecked": True,
            "ordinaryCutoffAgreementIsContinuumProof": False,
            "fixedCircleCountIsContinuumRieszRankProof": False,
            "uniformViscosityThresholdCertifiedHere": False,
            "infiniteDimensionalProjectionConvergenceProvedHere": False,
            "complementSemigroupBoundProvedHere": False,
            "nonlinearNavierStokesProvedHere": False,
            "clayProblemSolved": False,
        },
    }
    atomic_json(ARGS.output, payload)
    monitor.sample("complete", rows=len(rows),
                   crossCutoffRows=len(cross_cutoff))
    monitor.emit(
        "complete", output=str(ARGS.output), rows=len(rows),
        crossCutoffRows=len(cross_cutoff), allChecksPass=all_checks_pass,
        finiteDimensionalOnly=True,
    )
    return 0 if all_checks_pass else 2


def main() -> int:
    monitor = Monitor(ARGS.progress, ARGS.resources)
    try:
        return run(monitor)
    except (DiagnosticFailure, KeyError, TypeError, ValueError) as error:
        message = f"{type(error).__name__}: {error}"
        atomic_json(ARGS.output, failure_payload(ARGS.config, message))
        monitor.sample("failed")
        monitor.emit("failed", error=message, finiteDimensionalOnly=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
