#!/usr/bin/env python3
"""Finite Fourier dynamics diagnostic for R0.73L.

The script evolves the selected finite-dimensional viscous branch under the
non-autonomous compressed generator.  It checks action-normalized gain,
instantaneous complementary leakage, epsilon scaling, and cutoff agreement.
Every output is a finite-compression diagnostic; none proves the continuum
adiabatic theorem or a Navier--Stokes regularity statement.
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
    parser.add_argument("--deps", default=os.environ.get("R073L_DEPS", ""))
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
from scipy.integrate import solve_ivp  # noqa: E402
from scipy.interpolate import CubicSpline  # noqa: E402
from scipy.linalg import eig  # noqa: E402


SOURCE = Path(__file__).resolve()
START_MONOTONIC = time.monotonic()


class DiagnosticFailure(RuntimeError):
    """A fail-closed configuration or numerical consistency failure."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise DiagnosticFailure(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(canonical_json(value), encoding="utf-8")
    os.replace(temporary, path)


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


def load_configuration(path: Path) -> dict[str, Any]:
    config = json.loads(path.read_text(encoding="utf-8"))
    require(
        config.get("schemaVersion") == "r073l-adiabatic-diagnostic-config-v1",
        "configuration schema mismatch",
    )
    require(float(config["gamma"]) == 0.5, "R0.73L freezes gamma=1/2")
    cutoffs = [int(value) for value in config["cutoffs"]]
    require(cutoffs == sorted(set(cutoffs)) and len(cutoffs) >= 2,
            "cutoffs must be distinct and increasing")
    epsilons = [float(value) for value in config["epsilons"]]
    require(epsilons == sorted(set(epsilons), reverse=True),
            "epsilons must be distinct and decreasing")
    require(all(0.0 < value <= 0.001 for value in epsilons),
            "each epsilon must lie in the finite core interval (0,0.001]")
    require(int(config["sampleCount"]) >= 17,
            "at least seventeen slow-time samples are required")
    require(float(config["slowEnd"]) == 1.0 / 450.0,
            "the slow endpoint must be 1/450")
    return config


def recurrence_kinetic_matrix(
    cutoff: int,
    d_value: float,
    epsilon: float,
    gamma: float,
) -> np.ndarray:
    mu = gamma * gamma
    dimension = 2 * cutoff + 1
    raw = np.zeros((dimension, dimension), dtype=np.complex128)
    first_scale = math.exp(-d_value)
    second_scale = math.exp(-4.0 * d_value)
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


class FastMatrixAction:
    """O(N) action of the same recurrence matrix used for eigenanalysis."""

    def __init__(self, cutoff: int, epsilon: float, gamma: float) -> None:
        self.cutoff = cutoff
        self.epsilon = epsilon
        self.gamma = gamma
        modes = np.arange(-cutoff, cutoff + 1, dtype=float)
        self.ell = modes * modes + gamma * gamma
        self.sqrt_ell = np.sqrt(self.ell)
        self.first_base = gamma * 0.25 * (1.0 - 1.0 / self.ell)
        self.second_base = gamma * (-0.125 + 0.5 / self.ell)

    def __call__(self, d_value: float, vector: np.ndarray) -> np.ndarray:
        weighted = self.sqrt_ell * vector
        raw = np.zeros_like(weighted)
        first = math.exp(-d_value) * self.first_base
        second = math.exp(-4.0 * d_value) * self.second_base
        raw[1:] += first[:-1] * weighted[:-1]
        raw[:-1] -= first[1:] * weighted[1:]
        raw[2:] += second[:-2] * weighted[:-2]
        raw[:-2] -= second[2:] * weighted[2:]
        return raw / self.sqrt_ell - self.epsilon * self.ell * vector


def branch_state(
    matrix: np.ndarray,
    center: complex,
    radius: float,
) -> dict[str, Any]:
    values, left, right = eig(matrix, left=True, right=True,
                              check_finite=False)
    inside = np.flatnonzero(np.abs(values - center) < radius)
    require(inside.size == 1,
            f"fixed-contour count is {inside.size}, not one")
    index = int(inside[0])
    value = complex(values[index])
    lvec = left[:, index] / np.linalg.norm(left[:, index])
    rvec = right[:, index] / np.linalg.norm(right[:, index])
    pairing = complex(np.vdot(lvec, rvec))
    require(abs(pairing) > 1.0e-12,
            "selected finite eigenpair is numerically defective")
    return {
        "lambda": value,
        "left": lvec,
        "right": rvec,
        "pairing": pairing,
        "overlap": float(abs(pairing)),
        "contourCount": int(inside.size),
    }


def project(state: dict[str, Any], vector: np.ndarray) -> np.ndarray:
    return (state["right"]
            * (np.vdot(state["left"], vector) / state["pairing"]))


def finite_float(value: float) -> float:
    result = float(value)
    require(math.isfinite(result), "a reported scalar is not finite")
    return result


def run_case(
    monitor: Monitor,
    config: dict[str, Any],
    cutoff: int,
    epsilon: float,
    d_grid: np.ndarray,
) -> dict[str, Any]:
    gamma = float(config["gamma"])
    contour = config["fixedContour"]
    center = complex(float(contour["centerReal"]),
                     float(contour["centerImag"]))
    radius = float(contour["radius"])
    monitor.emit("case-start", N=cutoff, dimension=2 * cutoff + 1,
                 epsilon=epsilon)

    states: list[dict[str, Any]] = []
    for index, d_value in enumerate(d_grid):
        state = branch_state(
            recurrence_kinetic_matrix(cutoff, float(d_value), epsilon, gamma),
            center,
            radius,
        )
        states.append(state)
        if index in {0, len(d_grid) // 2, len(d_grid) - 1}:
            monitor.emit(
                "branch-sample", N=cutoff, epsilon=epsilon,
                sampleIndex=index, d=float(d_value),
                lambdaReal=float(state["lambda"].real),
                lambdaImag=float(state["lambda"].imag),
                overlap=state["overlap"], contourCount=state["contourCount"],
            )

    lambdas = np.array([state["lambda"].real for state in states],
                       dtype=float)
    lambda_spline = CubicSpline(d_grid, lambdas)
    action_primitive = lambda_spline.antiderivative()
    actions = ((action_primitive(d_grid) - action_primitive(d_grid[0]))
               / epsilon)

    initial = states[0]["right"].copy()
    initial /= np.linalg.norm(initial)
    matrix_action = FastMatrixAction(cutoff, epsilon, gamma)

    def rhs(d_value: float, vector: np.ndarray) -> np.ndarray:
        return matrix_action(d_value, vector) / epsilon

    solver = solve_ivp(
        rhs,
        (float(d_grid[0]), float(d_grid[-1])),
        initial,
        method=str(config["solver"]["method"]),
        t_eval=d_grid,
        rtol=float(config["solver"]["rtol"]),
        atol=float(config["solver"]["atol"]),
        max_step=float(config["solver"]["maxStep"]),
    )
    require(solver.success, f"solve_ivp failed: {solver.message}")
    require(solver.y.shape == (2 * cutoff + 1, len(d_grid)),
            "unexpected solver output shape")

    trajectory: list[dict[str, Any]] = []
    for index, d_value in enumerate(d_grid):
        vector = solver.y[:, index]
        selected = project(states[index], vector)
        complement = vector - selected
        gain = float(np.linalg.norm(vector))
        selected_norm = float(np.linalg.norm(selected))
        complement_norm = float(np.linalg.norm(complement))
        action = float(actions[index])
        exp_action = math.exp(action)
        leakage_ratio = complement_norm / max(selected_norm, 1.0e-300)
        trajectory.append({
            "sampleIndex": index,
            "d": float(d_value),
            "slowFraction": float(d_value / d_grid[-1]),
            "fastTime": float(d_value / epsilon),
            "lambda": float(lambdas[index]),
            "action": action,
            "gain": gain,
            "selectedNorm": selected_norm,
            "complementNorm": complement_norm,
            "actionNormalizedGain": gain / exp_action,
            "actionNormalizedSelectedNorm": selected_norm / exp_action,
            "actionNormalizedComplementNorm": complement_norm / exp_action,
            "complementToSelectedRatio": leakage_ratio,
            "leakageRatioOverEpsilon": leakage_ratio / epsilon,
            "finiteCompressionOnly": True,
        })

    terminal = trajectory[-1]
    terminal_action = float(actions[-1])
    for row in trajectory:
        row["backwardActionResidual"] = (
            math.log(max(row["gain"], 1.0e-300)
                     / max(terminal["gain"], 1.0e-300))
            + terminal_action - float(row["action"])
        )

    result = {
        "N": cutoff,
        "dimension": 2 * cutoff + 1,
        "epsilon": epsilon,
        "fastEnd": float(d_grid[-1] / epsilon),
        "solver": {
            "success": bool(solver.success),
            "message": solver.message,
            "nfev": int(solver.nfev),
            "njev": int(solver.njev),
            "nlu": int(solver.nlu),
        },
        "trajectory": trajectory,
        "summary": {
            "terminalAction": terminal_action,
            "terminalGain": terminal["gain"],
            "terminalActionNormalizedGain": terminal[
                "actionNormalizedGain"
            ],
            "terminalComplementToSelectedRatio": terminal[
                "complementToSelectedRatio"
            ],
            "terminalLeakageRatioOverEpsilon": terminal[
                "leakageRatioOverEpsilon"
            ],
            "minimumActionNormalizedGain": min(
                row["actionNormalizedGain"] for row in trajectory
            ),
            "maximumActionNormalizedGain": max(
                row["actionNormalizedGain"] for row in trajectory
            ),
            "maximumComplementToSelectedRatio": max(
                row["complementToSelectedRatio"] for row in trajectory
            ),
            "maximumLeakageRatioOverEpsilon": max(
                row["leakageRatioOverEpsilon"] for row in trajectory
            ),
            "maximumBackwardActionResidualAbs": max(
                abs(row["backwardActionResidual"]) for row in trajectory
            ),
            "maximumLambdaImaginaryAbs": max(
                abs(state["lambda"].imag) for state in states
            ),
            "minimumLeftRightOverlap": min(
                state["overlap"] for state in states
            ),
        },
        "claimBoundary": {
            "finiteKineticCompressionOnly": True,
            "continuumAdiabaticTheoremProvedHere": False,
        },
    }
    monitor.sample("case-complete", N=cutoff, epsilon=epsilon,
                   nfev=int(solver.nfev))
    monitor.emit(
        "case-complete", N=cutoff, epsilon=epsilon,
        fastEnd=result["fastEnd"], nfev=int(solver.nfev),
        normalizedGain=terminal["actionNormalizedGain"],
        leakageRatio=terminal["complementToSelectedRatio"],
        leakageOverEpsilon=terminal["leakageRatioOverEpsilon"],
    )
    return result


def regression_slope(rows: list[dict[str, Any]], field: str) -> float:
    x = np.log(np.array([row["epsilon"] for row in rows], dtype=float))
    y_values = np.array([row["summary"][field] for row in rows], dtype=float)
    require(np.all(y_values > 0.0), f"{field} must be positive")
    y = np.log(y_values)
    return float(np.polyfit(x, y, 1)[0])


def environment_payload(config_path: Path) -> dict[str, Any]:
    return {
        "schemaVersion": "r073l-adiabatic-environment-v1",
        "createdUtc": utc_now(),
        "python": platform.python_version(),
        "pythonImplementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "configurationSha256": sha256(config_path),
        "threadEnvironment": {
            key: os.environ.get(key)
            for key in (
                "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS",
                "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS",
            )
        },
        "claimBoundary": {
            "finiteDimensionalOnly": True,
            "continuumAdiabaticTheoremCertifiedByEnvironment": False,
        },
    }


def failure_payload(config_path: Path, message: str) -> dict[str, Any]:
    return {
        "schemaVersion": "r073l-adiabatic-diagnostic-v1",
        "release": "R0.73L",
        "status": "failed",
        "failure": message,
        "sourceBinding": {
            "path": "research/r073l_adiabatic_diagnostic.py",
            "sha256": sha256(SOURCE),
        },
        "configurationBinding": {
            "path": str(config_path),
            "sha256": sha256(config_path) if config_path.is_file() else None,
        },
        "claimBoundary": {
            "finiteDimensionalOnly": True,
            "continuumAdiabaticTrackingProvedHere": False,
            "clayProblemSolved": False,
        },
    }


def run(monitor: Monitor) -> int:
    config = load_configuration(ARGS.config)
    atomic_json(ARGS.environment, environment_payload(ARGS.config))
    cutoffs = [int(value) for value in config["cutoffs"]]
    epsilons = [float(value) for value in config["epsilons"]]
    slow_end = float(config["slowEnd"])
    d_grid = np.linspace(0.0, slow_end, int(config["sampleCount"]))
    monitor.emit(
        "start", cutoffs=cutoffs, epsilons=epsilons,
        sampleCount=len(d_grid), slowEnd=slow_end,
        finiteDimensionalOnly=True,
    )
    monitor.sample("start")

    cases: list[dict[str, Any]] = []
    for cutoff in cutoffs:
        for epsilon in epsilons:
            cases.append(run_case(
                monitor, config, cutoff, epsilon, d_grid,
            ))

    by_cutoff: dict[str, Any] = {}
    for cutoff in cutoffs:
        rows = [case for case in cases if case["N"] == cutoff]
        by_cutoff[str(cutoff)] = {
            "terminalLeakageLogLogSlope": regression_slope(
                rows, "terminalComplementToSelectedRatio"
            ),
            "terminalLeakageTailThreeLogLogSlope": regression_slope(
                rows[-3:], "terminalComplementToSelectedRatio"
            ),
            "maximumLeakageLogLogSlope": regression_slope(
                rows, "maximumComplementToSelectedRatio"
            ),
            "terminalNormalizedGainRange": [
                min(row["summary"]["terminalActionNormalizedGain"]
                    for row in rows),
                max(row["summary"]["terminalActionNormalizedGain"]
                    for row in rows),
            ],
        }

    cross_cutoff: list[dict[str, Any]] = []
    for small, large in zip(cutoffs[:-1], cutoffs[1:]):
        for epsilon in epsilons:
            left = next(case for case in cases
                        if case["N"] == small and case["epsilon"] == epsilon)
            right = next(case for case in cases
                         if case["N"] == large and case["epsilon"] == epsilon)
            cross_cutoff.append({
                "smallN": small,
                "largeN": large,
                "epsilon": epsilon,
                "terminalNormalizedGainAbsDifference": abs(
                    left["summary"]["terminalActionNormalizedGain"]
                    - right["summary"]["terminalActionNormalizedGain"]
                ),
                "terminalLeakageRatioAbsDifference": abs(
                    left["summary"]["terminalComplementToSelectedRatio"]
                    - right["summary"]["terminalComplementToSelectedRatio"]
                ),
                "finiteCompressionOnly": True,
            })

    tolerances = config["tolerances"]
    largest_pair = [row for row in cross_cutoff
                    if row["smallN"] == cutoffs[-2]
                    and row["largeN"] == cutoffs[-1]]
    maximums = {
        "lambdaImaginaryAbs": max(
            case["summary"]["maximumLambdaImaginaryAbs"] for case in cases
        ),
        "largestPairTerminalNormalizedGainDifference": max(
            row["terminalNormalizedGainAbsDifference"] for row in largest_pair
        ),
        "largestPairTerminalLeakageRatioDifference": max(
            row["terminalLeakageRatioAbsDifference"] for row in largest_pair
        ),
        "actionNormalizedGain": max(
            max(abs(case["summary"]["minimumActionNormalizedGain"]),
                abs(case["summary"]["maximumActionNormalizedGain"]))
            for case in cases
        ),
        "leakageRatioOverEpsilon": max(
            case["summary"]["maximumLeakageRatioOverEpsilon"]
            for case in cases
        ),
        "backwardActionResidualAbs": max(
            case["summary"]["maximumBackwardActionResidualAbs"]
            for case in cases
        ),
    }
    checks = {
        "allSolversSucceeded": all(case["solver"]["success"] for case in cases),
        "allSelectedEigenvaluesNumericallyReal": (
            maximums["lambdaImaginaryAbs"]
            <= float(tolerances["numericalReality"])
        ),
        "largestCutoffsAgreeOnNormalizedGain": (
            maximums["largestPairTerminalNormalizedGainDifference"]
            <= float(tolerances["cutoffNormalizedGain"])
        ),
        "largestCutoffsAgreeOnLeakage": (
            maximums["largestPairTerminalLeakageRatioDifference"]
            <= float(tolerances["cutoffLeakage"])
        ),
        "allReportedScalarsFinite": all(
            math.isfinite(float(value))
            for case in cases
            for row in case["trajectory"]
            for key, value in row.items()
            if key not in {"finiteCompressionOnly"}
        ),
    }
    all_checks_pass = bool(all(checks.values()))
    payload = {
        "schemaVersion": "r073l-adiabatic-diagnostic-v1",
        "release": "R0.73L",
        "createdUtc": utc_now(),
        "status": "passed" if all_checks_pass else "failed",
        "sourceBinding": {
            "path": "research/r073l_adiabatic_diagnostic.py",
            "sha256": sha256(SOURCE),
        },
        "configurationBinding": {
            "path": str(ARGS.config),
            "sha256": sha256(ARGS.config),
        },
        "parameters": {
            "gamma": float(config["gamma"]),
            "cutoffs": cutoffs,
            "epsilons": epsilons,
            "slowEnd": slow_end,
            "sampleCount": len(d_grid),
            "fixedContour": config["fixedContour"],
            "solver": config["solver"],
            "matrixConstruction": (
                "four-term raw-vorticity recurrence followed by kinetic L2 conjugation"
            ),
        },
        "cases": cases,
        "epsilonScalingByCutoff": by_cutoff,
        "crossCutoffComparisons": cross_cutoff,
        "maximums": maximums,
        "checks": checks,
        "allChecksPass": all_checks_pass,
        "claimBoundary": {
            "finiteKineticCompressionComputed": True,
            "actionNormalizedGainComputed": True,
            "instantaneousComplementLeakageComputed": True,
            "backwardActionResidualComputedFromForwardOrbit": True,
            "finiteScalingIsContinuumProof": False,
            "finiteCutoffAgreementIsContinuumProof": False,
            "explicitContinuumEpsilonThresholdCertifiedHere": False,
            "nonlinearNavierStokesProvedHere": False,
            "clayProblemSolved": False,
        },
    }
    atomic_json(ARGS.output, payload)
    monitor.sample("complete", cases=len(cases))
    monitor.emit("complete", output=str(ARGS.output), cases=len(cases),
                 allChecksPass=all_checks_pass,
                 finiteDimensionalOnly=True)
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
