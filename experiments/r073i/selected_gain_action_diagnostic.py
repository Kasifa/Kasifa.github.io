#!/usr/bin/env python3
"""Finite R0.73I selected-gain action and WKB diagnostic.

Every result produced here is a finite binary64 Fourier--Galerkin
calculation.  The program does not certify an infinite-dimensional spectral
branch, a Fourier tail, the unknown endpoint d0, or a continuum adiabatic
theorem.
"""

from __future__ import annotations

import argparse
import copy
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
from typing import Any, Iterable, Mapping


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SCHEMA_VERSION = "r073i-finite-diagnostic-v1"
SUMMARY_SCHEMA_VERSION = "r073i-finite-summary-v1"
EVIDENCE_CLASS = "finite-binary64-galerkin-diagnostic-only"
GAMMA = 0.5
MU = 0.25

SOURCE_FILES = (
    "experiments/r073i/README.md",
    "experiments/r073i/command.txt",
    "experiments/r073i/config.json",
    "experiments/r073i/requirements.txt",
    "experiments/r073i/summary.schema.json",
    "experiments/r073i/selected_gain_action_diagnostic.py",
    "experiments/r073i/validate.py",
    "tests/r073i-finite-diagnostic.test.mjs",
)

ACTION_FIELDS = (
    "schemaVersion", "evidenceClass", "diagnosticOnly", "smokeMode",
    "windowId", "endpoint", "endpointExpression", "endpointRole", "N",
    "quadratureOrder", "finiteAction", "finiteAverageRate",
    "finiteWkbCorrection", "berryIntegral", "viscousIntegral",
    "edgeAtZeroReal", "edgeAtEndpointReal", "minimumNodeRealGap",
    "minimumNodeComplexSeparation", "maximumNodeEigenCondition",
    "maximumNodeEigenResidualRelative", "maximumDerivativeResidualRelative",
)

GAIN_FIELDS = (
    "schemaVersion", "evidenceClass", "diagnosticOnly", "smokeMode",
    "gridKind", "windowId", "endpoint", "endpointRole", "N", "Lambda",
    "epsilon", "integrator", "fastStep", "stepCount", "logSelectedGain",
    "LambdaInverseLogGain", "finiteAction", "finiteAverageRate",
    "finiteWkbCorrection", "residualLogGainMinusLambdaAction",
    "residualMinusWkb", "topClusterDimension", "topEigenvalueReal",
    "topEigenvalueImag", "topRealGap", "topComplexSeparation",
    "topEigenCondition", "topEigenResidualRelative", "wallTimeSeconds",
)

COMPARISON_FIELDS = (
    "schemaVersion", "evidenceClass", "diagnosticOnly", "smokeMode",
    "kind", "windowId", "leftLabel", "rightLabel", "absoluteDifference",
    "tolerance", "passCheck", "diagnosticInterpretation",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


ARGS = parse_args()
if ARGS.deps:
    sys.path.insert(0, ARGS.deps)

import numpy as np  # noqa: E402
import scipy  # noqa: E402
from scipy.linalg import eig, expm  # noqa: E402


START = time.perf_counter()
PROGRESS: Path | None = None
SEQUENCE = 0


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"


def atomic_text(path: Path, value: str) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def binding(path: Path, base: Path) -> dict[str, object]:
    return {
        "path": path.resolve().relative_to(base.resolve()).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def emit(event: str, **fields: object) -> None:
    global SEQUENCE
    SEQUENCE += 1
    row = {
        "sequence": SEQUENCE,
        "timestampUtc": now_utc(),
        "elapsedSeconds": round(time.perf_counter() - START, 6),
        "event": event,
        **fields,
    }
    rendered = json.dumps(row, sort_keys=True, allow_nan=False)
    print(rendered, flush=True)
    if PROGRESS is not None:
        with PROGRESS.open("a", encoding="utf-8") as stream:
            stream.write(rendered + "\n")


def git_text(*arguments: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), *arguments],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def endpoint_from_expression(expression: str) -> float:
    values = {
        "1e-4": 1.0e-4,
        "sqrt(19/180)/392": math.sqrt(19.0 / 180.0) / 392.0,
        "1/450": 1.0 / 450.0,
    }
    if expression not in values:
        raise ValueError(f"unsupported endpoint expression: {expression}")
    return values[expression]


def validate_config(config: Mapping[str, object]) -> None:
    required = {
        "schemaVersion", "release", "evidenceClass", "diagnosticOnly",
        "windows", "action", "gain", "finiteTopRealTolerance",
        "tolerances", "claimBoundary",
    }
    if set(config) != required:
        raise ValueError("configuration top-level keys are not exact")
    if config["schemaVersion"] != "r073i-finite-config-v1":
        raise ValueError("unexpected configuration schema")
    if config["release"] != "R0.73I-finite-diagnostic":
        raise ValueError("unexpected release")
    if config["evidenceClass"] != EVIDENCE_CLASS or config["diagnosticOnly"] is not True:
        raise ValueError("configuration must remain finite diagnostic only")
    windows = config["windows"]
    if not isinstance(windows, list) or [row["id"] for row in windows] != [
        "explicit-pilot", "analytic-upper-bound", "one-over-450"
    ]:
        raise ValueError("the three endpoint roles changed")
    for row in windows:
        endpoint = endpoint_from_expression(str(row["expression"]))
        if not math.isfinite(endpoint) or endpoint <= 0.0:
            raise ValueError("invalid endpoint")
        role = str(row["role"]).lower()
        if "not" not in role or "theorem endpoint" not in role and "not d0" not in role:
            raise ValueError("endpoint role must fail closed")
    action = config["action"]
    gain = config["gain"]
    if not isinstance(action, dict) or not isinstance(gain, dict):
        raise ValueError("action/gain configuration must be objects")
    cutoffs = [int(value) for value in action["cutoffs"]]
    orders = [int(value) for value in action["quadratureOrders"]]
    if sorted(cutoffs) != cutoffs or len(cutoffs) < 2 or min(cutoffs) < 4:
        raise ValueError("action cutoffs are invalid")
    if sorted(orders) != orders or len(orders) < 2 or min(orders) < 4:
        raise ValueError("quadrature orders are invalid")
    if int(action["primaryQuadratureOrder"]) != max(orders):
        raise ValueError("primary quadrature order must be the finest")
    lambdas = [int(value) for value in gain["lambdas"]]
    if sorted(lambdas) != lambdas or len(lambdas) < 2 or min(lambdas) <= 0:
        raise ValueError("lambda grid is invalid")
    if int(gain["primaryCutoff"]) not in cutoffs:
        raise ValueError("primary gain cutoff is absent from action grid")
    boundary = config["claimBoundary"]
    if not isinstance(boundary, dict):
        raise ValueError("claim boundary must be an object")
    if boundary.get("finiteBinary64GalerkinDiagnostic") is not True:
        raise ValueError("finite evidence flag must be true")
    if any(value is not False for key, value in boundary.items() if key != "finiteBinary64GalerkinDiagnostic"):
        raise ValueError("continuum and theorem claim flags must remain false")


def smoke_config(config: Mapping[str, object]) -> dict[str, object]:
    result = copy.deepcopy(config)
    result["action"] = {
        "cutoffs": [8, 12],
        "quadratureOrders": [8, 12],
        "primaryQuadratureOrder": 12,
    }
    result["gain"] = {
        "primaryCutoff": 12,
        "lambdas": [1000, 2000],
        "primaryFastStep": 0.5,
        "cutoffComparison": {"cutoffs": [8, 12], "lambda": 2000, "fastStep": 0.5},
        "stepComparison": {"cutoff": 12, "lambda": 2000, "fastSteps": [1.0, 0.5, 0.25]},
        "independentRk4": {"cutoff": 8, "lambda": 2000, "fastStep": 0.25},
    }
    # Smoke mode checks the complete artifact/validation path on deliberately
    # tiny truncations.  Its cutoff gates are therefore structural gates, not
    # the convergence gates used by the canonical formal configuration.
    result["tolerances"] = copy.deepcopy(result["tolerances"])
    result["tolerances"].update({
        "actionFinestCutoffAbsolute": 1.0e-8,
        "wkbFinestCutoffAbsolute": 1.0e-5,
        "selectedGainFinestCutoffLogAbsolute": 2.0e-5,
    })
    return result


def prepare_output(output_dir: Path, overwrite: bool) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated = (
        "action_rows.csv", "gain_rows.csv", "comparison_rows.csv",
        "environment.json", "summary.json", "manifest.json",
        "progress.ndjson", "SHA256SUMS",
    )
    existing = [output_dir / name for name in generated if (output_dir / name).exists()]
    if existing and not overwrite:
        raise RuntimeError("refusing to overwrite generated files without --overwrite")
    for path in existing:
        path.unlink()


def matrix_recurrence(n_cut: int, epsilon: float, d_value: float) -> np.ndarray:
    raw = np.zeros((2 * n_cut + 1, 2 * n_cut + 1), dtype=np.complex128)
    exp1 = math.exp(-d_value)
    exp4 = math.exp(-4.0 * d_value)
    for column, n_mode in enumerate(range(-n_cut, n_cut + 1)):
        lam = n_mode * n_mode + MU
        first = GAMMA * 0.25 * exp1 * (1.0 - 1.0 / lam)
        second = GAMMA * exp4 * (-0.125 + 0.5 / lam)
        for shift, value in ((1, first), (-1, -first), (2, second), (-2, -second)):
            output = n_mode + shift
            if -n_cut <= output <= n_cut:
                raw[output + n_cut, column] = value
    modes = np.arange(-n_cut, n_cut + 1, dtype=float)
    lam = modes * modes + MU
    transformed = (1.0 / np.sqrt(lam))[:, None] * raw * np.sqrt(lam)[None, :]
    transformed -= epsilon * np.diag(lam)
    return transformed


def matrix_derivative(n_cut: int, d_value: float) -> np.ndarray:
    raw = np.zeros((2 * n_cut + 1, 2 * n_cut + 1), dtype=np.complex128)
    exp1 = math.exp(-d_value)
    exp4 = math.exp(-4.0 * d_value)
    for column, n_mode in enumerate(range(-n_cut, n_cut + 1)):
        lam = n_mode * n_mode + MU
        first = -GAMMA * 0.25 * exp1 * (1.0 - 1.0 / lam)
        second = -4.0 * GAMMA * exp4 * (-0.125 + 0.5 / lam)
        for shift, value in ((1, first), (-1, -first), (2, second), (-2, -second)):
            output = n_mode + shift
            if -n_cut <= output <= n_cut:
                raw[output + n_cut, column] = value
    modes = np.arange(-n_cut, n_cut + 1, dtype=float)
    lam = modes * modes + MU
    return (1.0 / np.sqrt(lam))[:, None] * raw * np.sqrt(lam)[None, :]


def canonical_top(matrix: np.ndarray, real_tolerance: float) -> dict[str, object]:
    values, left_vectors, right_vectors = eig(
        matrix, left=True, right=True, check_finite=False
    )
    top_real = float(np.max(values.real))
    indices = np.flatnonzero(values.real >= top_real - real_tolerance)
    selected = max(
        (int(index) for index in indices),
        key=lambda index: (float(values[index].real), float(values[index].imag)),
    )
    value = complex(values[selected])
    right = np.asarray(right_vectors[:, selected], dtype=np.complex128)
    right /= np.linalg.norm(right)
    anchor = int(np.argmax(np.abs(right)))
    right *= np.exp(-1j * np.angle(right[anchor]))
    if right[anchor].real < 0.0:
        right *= -1.0
    left_raw = np.asarray(left_vectors[:, selected], dtype=np.complex128)
    overlap = np.vdot(left_raw, right)
    condition = float(np.linalg.norm(left_raw) / abs(overlap))
    left = left_raw / np.conjugate(overlap)
    scale = max(1.0, float(np.linalg.norm(matrix)), abs(value))
    right_residual = float(np.linalg.norm(matrix @ right - value * right) / scale)
    left_residual = float(
        np.linalg.norm(matrix.conjugate().T @ left - np.conjugate(value) * left)
        / (scale * max(1.0, np.linalg.norm(left)))
    )
    complement = np.delete(values, selected)
    real_gap = top_real - float(np.max(complement.real)) if len(complement) else math.inf
    separation = float(np.min(np.abs(value - complement))) if len(complement) else math.inf
    return {
        "value": value,
        "right": right,
        "left": left,
        "clusterDimension": int(len(indices)),
        "realGap": real_gap,
        "complexSeparation": separation,
        "condition": condition,
        "eigenResidualRelative": max(right_residual, left_residual),
        "biorthogonalityDefect": float(abs(np.vdot(left, right) - 1.0)),
    }


def eigenvector_derivative(
    matrix: np.ndarray,
    derivative: np.ndarray,
    eigen: Mapping[str, object],
) -> tuple[np.ndarray, complex, float]:
    value = complex(eigen["value"])
    right = np.asarray(eigen["right"])
    dimension = len(right)
    augmented = np.zeros((dimension + 1, dimension + 1), dtype=np.complex128)
    augmented[:dimension, :dimension] = matrix - value * np.eye(dimension)
    augmented[:dimension, dimension] = -right
    augmented[dimension, :dimension] = np.conjugate(right)
    rhs = np.zeros(dimension + 1, dtype=np.complex128)
    rhs[:dimension] = -(derivative @ right)
    solution = np.linalg.solve(augmented, rhs)
    right_prime = solution[:dimension]
    value_prime = complex(solution[dimension])
    residual = np.concatenate((
        (matrix - value * np.eye(dimension)) @ right_prime
        - value_prime * right
        + derivative @ right,
        np.asarray([np.vdot(right, right_prime)]),
    ))
    scale = max(1.0, np.linalg.norm(derivative @ right), abs(value_prime))
    return right_prime, value_prime, float(np.linalg.norm(residual) / scale)


def action_wkb_row(
    window: Mapping[str, object],
    n_cut: int,
    quadrature_order: int,
    real_tolerance: float,
    smoke: bool,
) -> dict[str, object]:
    endpoint = float(window["endpoint"])
    nodes, weights = np.polynomial.legendre.leggauss(quadrature_order)
    profile_nodes = endpoint * (nodes + 1.0) / 2.0
    factor = endpoint / 2.0
    modes = np.arange(-n_cut, n_cut + 1, dtype=float)
    laplacian = modes * modes + MU
    actions: list[float] = []
    berries: list[float] = []
    viscous: list[float] = []
    real_gaps: list[float] = []
    separations: list[float] = []
    conditions: list[float] = []
    eigen_residuals: list[float] = []
    derivative_residuals: list[float] = []
    for d_value in profile_nodes:
        matrix = matrix_recurrence(n_cut, 0.0, float(d_value))
        derivative = matrix_derivative(n_cut, float(d_value))
        eigen = canonical_top(matrix, real_tolerance)
        right_prime, _, derivative_residual = eigenvector_derivative(
            matrix, derivative, eigen
        )
        left = np.asarray(eigen["left"])
        right = np.asarray(eigen["right"])
        actions.append(float(complex(eigen["value"]).real))
        berries.append(float(np.vdot(left, right_prime).real))
        viscous.append(float(np.vdot(left, laplacian * right).real))
        real_gaps.append(float(eigen["realGap"]))
        separations.append(float(eigen["complexSeparation"]))
        conditions.append(float(eigen["condition"]))
        eigen_residuals.append(float(eigen["eigenResidualRelative"]))
        derivative_residuals.append(derivative_residual)
    action = factor * float(np.dot(weights, actions))
    berry = factor * float(np.dot(weights, berries))
    viscous_value = factor * float(np.dot(weights, viscous))
    start = canonical_top(matrix_recurrence(n_cut, 0.0, 0.0), real_tolerance)
    finish = canonical_top(matrix_recurrence(n_cut, 0.0, endpoint), real_tolerance)
    return {
        "schemaVersion": SCHEMA_VERSION,
        "evidenceClass": EVIDENCE_CLASS,
        "diagnosticOnly": True,
        "smokeMode": smoke,
        "windowId": window["id"],
        "endpoint": endpoint,
        "endpointExpression": window["expression"],
        "endpointRole": window["role"],
        "N": n_cut,
        "quadratureOrder": quadrature_order,
        "finiteAction": action,
        "finiteAverageRate": action / endpoint,
        "finiteWkbCorrection": -(berry + viscous_value),
        "berryIntegral": berry,
        "viscousIntegral": viscous_value,
        "edgeAtZeroReal": float(complex(start["value"]).real),
        "edgeAtEndpointReal": float(complex(finish["value"]).real),
        "minimumNodeRealGap": min(real_gaps),
        "minimumNodeComplexSeparation": min(separations),
        "maximumNodeEigenCondition": max(conditions),
        "maximumNodeEigenResidualRelative": max(eigen_residuals),
        "maximumDerivativeResidualRelative": max(derivative_residuals),
    }


def cf4_step(n_cut: int, epsilon: float, theta: float, step: float) -> np.ndarray:
    root3 = math.sqrt(3.0)
    c1 = 0.5 - root3 / 6.0
    c2 = 0.5 + root3 / 6.0
    a1 = (3.0 - 2.0 * root3) / 12.0
    a2 = (3.0 + 2.0 * root3) / 12.0
    first = matrix_recurrence(n_cut, epsilon, epsilon * (theta + c1 * step))
    second = matrix_recurrence(n_cut, epsilon, epsilon * (theta + c2 * step))
    early = expm(step * (a2 * first + a1 * second))
    late = expm(step * (a1 * first + a2 * second))
    return late @ early


def propagate_cf4(
    n_cut: int,
    absolute_lambda: int,
    endpoint: float,
    fast_step: float,
    real_tolerance: float,
) -> dict[str, object]:
    started = time.perf_counter()
    epsilon = 1.0 / absolute_lambda
    top = canonical_top(matrix_recurrence(n_cut, epsilon, 0.0), real_tolerance)
    state = np.asarray(top["right"]).copy()
    log_scale = 0.0
    theta = 0.0
    target = endpoint / epsilon
    step_count = 0
    while theta < target - 1.0e-13:
        step = min(fast_step, target - theta)
        state = cf4_step(n_cut, epsilon, theta, step) @ state
        norm = float(np.linalg.norm(state))
        if not math.isfinite(norm) or norm <= 0.0:
            raise FloatingPointError("selected CF4 propagation lost finite norm")
        state /= norm
        log_scale += math.log(norm)
        theta += step
        step_count += 1
    return {
        "integrator": "kinetic-cf4-exponential",
        "logSelectedGain": log_scale + math.log(float(np.linalg.norm(state))),
        "stepCount": step_count,
        "top": top,
        "wallTimeSeconds": time.perf_counter() - started,
    }


def propagate_rk4(
    n_cut: int,
    absolute_lambda: int,
    endpoint: float,
    fast_step: float,
    real_tolerance: float,
) -> dict[str, object]:
    started = time.perf_counter()
    epsilon = 1.0 / absolute_lambda
    top = canonical_top(matrix_recurrence(n_cut, epsilon, 0.0), real_tolerance)
    state = np.asarray(top["right"]).copy()
    log_scale = 0.0
    theta = 0.0
    target = endpoint / epsilon
    step_count = 0

    def rhs(time_value: float, value: np.ndarray) -> np.ndarray:
        return matrix_recurrence(n_cut, epsilon, epsilon * time_value) @ value

    while theta < target - 1.0e-13:
        step = min(fast_step, target - theta)
        k1 = rhs(theta, state)
        k2 = rhs(theta + step / 2.0, state + step * k1 / 2.0)
        k3 = rhs(theta + step / 2.0, state + step * k2 / 2.0)
        k4 = rhs(theta + step, state + step * k3)
        state += step * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
        norm = float(np.linalg.norm(state))
        if not math.isfinite(norm) or norm <= 0.0:
            raise FloatingPointError("selected RK4 propagation lost finite norm")
        state /= norm
        log_scale += math.log(norm)
        theta += step
        step_count += 1
    return {
        "integrator": "independent-kinetic-rk4",
        "logSelectedGain": log_scale + math.log(float(np.linalg.norm(state))),
        "stepCount": step_count,
        "top": top,
        "wallTimeSeconds": time.perf_counter() - started,
    }


def gain_row(
    grid_kind: str,
    window: Mapping[str, object],
    n_cut: int,
    absolute_lambda: int,
    fast_step: float,
    integrator: str,
    action: Mapping[str, object],
    real_tolerance: float,
    smoke: bool,
) -> dict[str, object]:
    endpoint = float(window["endpoint"])
    if integrator == "cf4":
        result = propagate_cf4(n_cut, absolute_lambda, endpoint, fast_step, real_tolerance)
    elif integrator == "rk4":
        result = propagate_rk4(n_cut, absolute_lambda, endpoint, fast_step, real_tolerance)
    else:
        raise ValueError(f"unknown integrator: {integrator}")
    log_gain = float(result["logSelectedGain"])
    finite_action = float(action["finiteAction"])
    wkb = float(action["finiteWkbCorrection"])
    residual = log_gain - absolute_lambda * finite_action
    top = result["top"]
    return {
        "schemaVersion": SCHEMA_VERSION,
        "evidenceClass": EVIDENCE_CLASS,
        "diagnosticOnly": True,
        "smokeMode": smoke,
        "gridKind": grid_kind,
        "windowId": window["id"],
        "endpoint": endpoint,
        "endpointRole": window["role"],
        "N": n_cut,
        "Lambda": absolute_lambda,
        "epsilon": 1.0 / absolute_lambda,
        "integrator": result["integrator"],
        "fastStep": fast_step,
        "stepCount": result["stepCount"],
        "logSelectedGain": log_gain,
        "LambdaInverseLogGain": log_gain / absolute_lambda,
        "finiteAction": finite_action,
        "finiteAverageRate": action["finiteAverageRate"],
        "finiteWkbCorrection": wkb,
        "residualLogGainMinusLambdaAction": residual,
        "residualMinusWkb": residual - wkb,
        "topClusterDimension": top["clusterDimension"],
        "topEigenvalueReal": float(complex(top["value"]).real),
        "topEigenvalueImag": float(complex(top["value"]).imag),
        "topRealGap": top["realGap"],
        "topComplexSeparation": top["complexSeparation"],
        "topEigenCondition": top["condition"],
        "topEigenResidualRelative": top["eigenResidualRelative"],
        "wallTimeSeconds": result["wallTimeSeconds"],
    }


def comparison_row(
    kind: str,
    window_id: str,
    left_label: str,
    right_label: str,
    difference: float,
    tolerance: float,
    interpretation: str,
    smoke: bool,
) -> dict[str, object]:
    return {
        "schemaVersion": SCHEMA_VERSION,
        "evidenceClass": EVIDENCE_CLASS,
        "diagnosticOnly": True,
        "smokeMode": smoke,
        "kind": kind,
        "windowId": window_id,
        "leftLabel": left_label,
        "rightLabel": right_label,
        "absoluteDifference": abs(float(difference)),
        "tolerance": float(tolerance),
        "passCheck": abs(float(difference)) <= float(tolerance),
        "diagnosticInterpretation": interpretation,
    }


def write_csv(path: Path, fields: Iterable[str], rows: list[Mapping[str, object]]) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    with temporary.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(fields), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            encoded: dict[str, object] = {}
            for field in fields:
                value = row[field]
                if isinstance(value, bool):
                    encoded[field] = "true" if value else "false"
                elif isinstance(value, float):
                    if not math.isfinite(value):
                        raise ValueError(f"nonfinite CSV field {field}")
                    encoded[field] = format(value, ".17g")
                else:
                    encoded[field] = value
            writer.writerow(encoded)
    os.replace(temporary, path)


def main() -> int:
    global PROGRESS
    output_dir = ARGS.output_dir.resolve()
    config_path = ARGS.config.resolve()
    if ARGS.smoke:
        if output_dir == HERE.resolve() or HERE.resolve() in output_dir.parents:
            raise RuntimeError("smoke output must be outside the formal package")
    elif output_dir != HERE.resolve() or config_path != (HERE / "config.json").resolve():
        raise RuntimeError("formal mode must use the canonical R0.73I config and output directory")

    raw_config = json.loads(config_path.read_text(encoding="utf-8"))
    validate_config(raw_config)
    config = smoke_config(raw_config) if ARGS.smoke else raw_config
    prepare_output(output_dir, ARGS.overwrite)
    PROGRESS = output_dir / "progress.ndjson"
    PROGRESS.write_text("", encoding="utf-8")
    source_commit = git_text("rev-parse", "HEAD")
    branch = git_text("rev-parse", "--abbrev-ref", "HEAD")
    emit("start", smokeMode=ARGS.smoke, sourceCommit=source_commit, branch=branch)

    windows = []
    for row in config["windows"]:
        windows.append({**row, "endpoint": endpoint_from_expression(str(row["expression"]))})
    action_spec = config["action"]
    gain_spec = config["gain"]
    tolerances = config["tolerances"]
    real_tolerance = float(config["finiteTopRealTolerance"])
    cutoffs = [int(value) for value in action_spec["cutoffs"]]
    orders = [int(value) for value in action_spec["quadratureOrders"]]
    primary_order = int(action_spec["primaryQuadratureOrder"])

    action_rows: list[dict[str, object]] = []
    action_cache: dict[tuple[str, int, int], dict[str, object]] = {}
    total_action_cases = len(windows) * len(cutoffs) * len(orders)
    action_index = 0
    for window in windows:
        for n_cut in cutoffs:
            for order in orders:
                action_index += 1
                emit(
                    "action_case_start", index=action_index, total=total_action_cases,
                    windowId=window["id"], N=n_cut, quadratureOrder=order,
                )
                row = action_wkb_row(window, n_cut, order, real_tolerance, ARGS.smoke)
                action_rows.append(row)
                action_cache[(str(window["id"]), n_cut, order)] = row
                emit(
                    "action_case_complete", index=action_index, total=total_action_cases,
                    windowId=window["id"], N=n_cut, quadratureOrder=order,
                    finiteAction=row["finiteAction"], finiteWkbCorrection=row["finiteWkbCorrection"],
                )

    gain_rows: list[dict[str, object]] = []
    gain_cache: dict[tuple[str, int, int, float, str], dict[str, object]] = {}

    def obtain_gain(
        grid_kind: str,
        window: Mapping[str, object],
        n_cut: int,
        absolute_lambda: int,
        fast_step: float,
        integrator: str,
    ) -> dict[str, object]:
        key = (str(window["id"]), n_cut, absolute_lambda, fast_step, integrator)
        if key not in gain_cache:
            emit(
                "gain_case_start", gridKind=grid_kind, windowId=window["id"],
                N=n_cut, Lambda=absolute_lambda, fastStep=fast_step,
                integrator=integrator,
            )
            action = action_cache[(str(window["id"]), n_cut, primary_order)]
            gain_cache[key] = gain_row(
                grid_kind, window, n_cut, absolute_lambda, fast_step,
                integrator, action, real_tolerance, ARGS.smoke,
            )
            emit(
                "gain_case_complete", gridKind=grid_kind, windowId=window["id"],
                N=n_cut, Lambda=absolute_lambda, fastStep=fast_step,
                integrator=integrator,
                logSelectedGain=gain_cache[key]["logSelectedGain"],
            )
        return {**gain_cache[key], "gridKind": grid_kind}

    primary_n = int(gain_spec["primaryCutoff"])
    primary_step = float(gain_spec["primaryFastStep"])
    lambdas = [int(value) for value in gain_spec["lambdas"]]
    for window in windows:
        for absolute_lambda in lambdas:
            gain_rows.append(obtain_gain(
                "primary", window, primary_n, absolute_lambda, primary_step, "cf4"
            ))

    cutoff_spec = gain_spec["cutoffComparison"]
    cutoff_lambda = int(cutoff_spec["lambda"])
    cutoff_step = float(cutoff_spec["fastStep"])
    cutoff_grid = [int(value) for value in cutoff_spec["cutoffs"]]
    for window in windows:
        for n_cut in cutoff_grid:
            gain_rows.append(obtain_gain(
                "cutoff", window, n_cut, cutoff_lambda, cutoff_step, "cf4"
            ))

    step_spec = gain_spec["stepComparison"]
    step_n = int(step_spec["cutoff"])
    step_lambda = int(step_spec["lambda"])
    step_grid = [float(value) for value in step_spec["fastSteps"]]
    for window in windows:
        for fast_step in step_grid:
            gain_rows.append(obtain_gain(
                "step", window, step_n, step_lambda, fast_step, "cf4"
            ))

    independent_spec = gain_spec["independentRk4"]
    independent_n = int(independent_spec["cutoff"])
    independent_lambda = int(independent_spec["lambda"])
    independent_step = float(independent_spec["fastStep"])
    for window in windows:
        gain_rows.append(obtain_gain(
            "independent-rk4", window, independent_n, independent_lambda,
            independent_step, "rk4",
        ))

    comparisons: list[dict[str, object]] = []
    for window in windows:
        window_id = str(window["id"])
        for n_cut in cutoffs:
            for coarse, fine in zip(orders, orders[1:]):
                left = action_cache[(window_id, n_cut, coarse)]
                right = action_cache[(window_id, n_cut, fine)]
                comparisons.append(comparison_row(
                    "action-quadrature", window_id, f"q={coarse},N={n_cut}",
                    f"q={fine},N={n_cut}",
                    float(left["finiteAction"]) - float(right["finiteAction"]),
                    float(tolerances["actionQuadratureAbsolute"]),
                    "finite quadrature agreement only", ARGS.smoke,
                ))
        for coarse, fine in zip(cutoffs, cutoffs[1:]):
            left = action_cache[(window_id, coarse, primary_order)]
            right = action_cache[(window_id, fine, primary_order)]
            comparisons.append(comparison_row(
                "action-cutoff", window_id, f"N={coarse}", f"N={fine}",
                float(left["finiteAction"]) - float(right["finiteAction"]),
                float(tolerances["actionFinestCutoffAbsolute"]),
                "ordinary finite cutoff agreement; not a tail enclosure", ARGS.smoke,
            ))
            comparisons.append(comparison_row(
                "wkb-cutoff", window_id, f"N={coarse}", f"N={fine}",
                float(left["finiteWkbCorrection"]) - float(right["finiteWkbCorrection"]),
                float(tolerances["wkbFinestCutoffAbsolute"]),
                "ordinary finite WKB cutoff agreement; not an asymptotic proof", ARGS.smoke,
            ))
        cutoff_values = {
            n_cut: obtain_gain("comparison-cache", window, n_cut, cutoff_lambda, cutoff_step, "cf4")
            for n_cut in cutoff_grid
        }
        for coarse, fine in zip(cutoff_grid, cutoff_grid[1:]):
            comparisons.append(comparison_row(
                "selected-gain-cutoff", window_id, f"N={coarse}", f"N={fine}",
                float(cutoff_values[coarse]["logSelectedGain"])
                - float(cutoff_values[fine]["logSelectedGain"]),
                float(tolerances["selectedGainFinestCutoffLogAbsolute"]),
                "ordinary finite selected-gain cutoff agreement; not a tail enclosure",
                ARGS.smoke,
            ))
        step_values = {
            step: obtain_gain("comparison-cache", window, step_n, step_lambda, step, "cf4")
            for step in step_grid
        }
        ordered_steps = sorted(step_grid, reverse=True)
        for coarse, fine in zip(ordered_steps, ordered_steps[1:]):
            comparisons.append(comparison_row(
                "selected-gain-step", window_id, f"h={coarse}", f"h={fine}",
                float(step_values[coarse]["logSelectedGain"])
                - float(step_values[fine]["logSelectedGain"]),
                float(tolerances["selectedGainStepLogAbsolute"]),
                "finite fast-step agreement only", ARGS.smoke,
            ))
        rk4 = obtain_gain(
            "comparison-cache", window, independent_n, independent_lambda,
            independent_step, "rk4",
        )
        cf4 = obtain_gain(
            "comparison-cache", window, independent_n, independent_lambda,
            cutoff_step, "cf4",
        )
        comparisons.append(comparison_row(
            "independent-integrator", window_id,
            f"RK4,N={independent_n},h={independent_step}",
            f"CF4,N={independent_n},h={cutoff_step}",
            float(rk4["logSelectedGain"]) - float(cf4["logSelectedGain"]),
            float(tolerances["independentRk4LogAbsolute"]),
            "independent time integrator on the same finite kinetic generator",
            ARGS.smoke,
        ))

    action_path = output_dir / "action_rows.csv"
    gain_path = output_dir / "gain_rows.csv"
    comparison_path = output_dir / "comparison_rows.csv"
    write_csv(action_path, ACTION_FIELDS, action_rows)
    write_csv(gain_path, GAIN_FIELDS, gain_rows)
    write_csv(comparison_path, COMPARISON_FIELDS, comparisons)

    environment = {
        "schemaVersion": "r073i-finite-environment-v1",
        "createdUtc": now_utc(),
        "python": platform.python_version(),
        "pythonImplementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "logicalCpuCount": os.cpu_count(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "precision": "numpy.complex128 / IEEE-754 binary64 components",
        "randomnessUsed": False,
        "randomSeed": None,
        "executionMode": "local dense CPU linear algebra",
        "dgxUsed": False,
        "dgxReason": "finite matrices are at most 193 by 193; local execution avoids transfer overhead",
        "threadEnvironment": {
            key: os.environ.get(key) for key in (
                "OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"
            )
        },
        "sourceCommit": source_commit,
        "branch": branch,
        "workingTreeCleanAtRun": not bool(git_text("status", "--porcelain")),
        "smokeMode": ARGS.smoke,
        "scientificWallTimeSeconds": time.perf_counter() - START,
    }
    environment_path = output_dir / "environment.json"
    atomic_text(environment_path, canonical(environment))

    comparisons_pass = all(bool(row["passCheck"]) for row in comparisons)
    eigen_residual_pass = all(
        float(row["maximumNodeEigenResidualRelative"])
        <= float(tolerances["topEigenResidualRelative"])
        for row in action_rows
    ) and all(
        float(row["topEigenResidualRelative"])
        <= float(tolerances["topEigenResidualRelative"])
        for row in gain_rows
    )
    finite_top_one = all(int(row["topClusterDimension"]) == 1 for row in gain_rows)
    endpoint_roles_fail_closed = all(
        "not" in str(window["role"]).lower() for window in windows
    )
    boundary_fail_closed = (
        config["claimBoundary"]["finiteBinary64GalerkinDiagnostic"] is True
        and all(
            value is False for key, value in config["claimBoundary"].items()
            if key != "finiteBinary64GalerkinDiagnostic"
        )
    )
    checks = {
        "allComparisonChecksPass": comparisons_pass,
        "finiteTopDimensionOneOnComputedGrid": finite_top_one,
        "finiteEigenResidualsPass": eigen_residual_pass,
        "endpointRolesFailClosed": endpoint_roles_fail_closed,
        "claimBoundaryFailClosed": boundary_fail_closed,
        "threeDeclaredWindowsPresent": len(windows) == 3,
        "finiteWkbIdentityPass": all(
            abs(
                float(row["finiteWkbCorrection"])
                + float(row["berryIntegral"])
                + float(row["viscousIntegral"])
            ) <= 2.0e-15
            for row in action_rows
        ),
    }

    primary_actions = {
        (str(row["windowId"]), int(row["N"])): row
        for row in action_rows if int(row["quadratureOrder"]) == primary_order
    }
    primary_gain_rows = [row for row in gain_rows if row["gridKind"] == "primary"]
    window_summaries = []
    for window in windows:
        window_id = str(window["id"])
        action = primary_actions[(window_id, primary_n)]
        largest = max(
            (row for row in primary_gain_rows if row["windowId"] == window_id),
            key=lambda row: int(row["Lambda"]),
        )
        window_summaries.append({
            "windowId": window_id,
            "endpoint": window["endpoint"],
            "role": window["role"],
            "primaryAction": action["finiteAction"],
            "primaryAverageRate": action["finiteAverageRate"],
            "primaryWkbCorrection": action["finiteWkbCorrection"],
            "largestLambda": largest["Lambda"],
            "largestLambdaNormalizedLogGain": largest["LambdaInverseLogGain"],
            "largestLambdaResidual": largest["residualLogGainMinusLambdaAction"],
            "largestLambdaResidualMinusWkb": largest["residualMinusWkb"],
        })

    data_files = [
        "action_rows.csv", "gain_rows.csv", "comparison_rows.csv",
        "environment.json", "progress.ndjson",
    ]
    summary = {
        "schemaVersion": SUMMARY_SCHEMA_VERSION,
        "release": "R0.73I-finite-diagnostic",
        "evidenceClass": EVIDENCE_CLASS,
        "diagnosticOnly": True,
        "createdUtc": now_utc(),
        "sourceCommit": source_commit,
        "configuration": {
            "smokeMode": ARGS.smoke,
            "windows": windows,
            "action": action_spec,
            "gain": gain_spec,
            "tolerances": tolerances,
            "configBinding": binding(config_path, ROOT),
            "commandLine": sys.argv,
        },
        "counts": {
            "actionRows": len(action_rows),
            "gainRows": len(gain_rows),
            "comparisonRows": len(comparisons),
            "windowCount": len(windows),
        },
        "windowSummaries": window_summaries,
        "checks": checks,
        "allChecksPass": all(checks.values()),
        "claimBoundary": config["claimBoundary"],
        "dataFiles": data_files,
    }
    summary_path = output_dir / "summary.json"
    atomic_text(summary_path, canonical(summary))
    emit(
        "complete", allChecksPass=summary["allChecksPass"],
        actionRows=len(action_rows), gainRows=len(gain_rows),
        comparisonRows=len(comparisons),
    )

    source_bindings = []
    for relative in SOURCE_FILES:
        path = ROOT / relative
        source_bindings.append(binding(path, ROOT))
    generated_paths = [
        action_path, gain_path, comparison_path, environment_path,
        summary_path, PROGRESS,
    ]
    manifest = {
        "schemaVersion": "r073i-finite-manifest-v1",
        "release": "R0.73I-finite-diagnostic",
        "evidenceClass": EVIDENCE_CLASS,
        "diagnosticOnly": True,
        "sourceCommit": source_commit,
        "branch": branch,
        "smokeMode": ARGS.smoke,
        "sourceBindings": source_bindings,
        "generatedBindings": [binding(path, output_dir) for path in generated_paths],
        "allChecksPass": summary["allChecksPass"],
        "claimBoundary": config["claimBoundary"],
        "continuumConclusion": "none; finite binary64 Fourier--Galerkin diagnostics only",
    }
    manifest_path = output_dir / "manifest.json"
    atomic_text(manifest_path, canonical(manifest))

    ledger_paths = sorted(
        path for path in output_dir.iterdir()
        if path.is_file() and path.name != "SHA256SUMS"
    )
    ledger = "".join(f"{sha256(path)}  {path.name}\n" for path in ledger_paths)
    atomic_text(output_dir / "SHA256SUMS", ledger)
    return 0 if summary["allChecksPass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
