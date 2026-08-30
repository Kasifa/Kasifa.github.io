#!/usr/bin/env python3
"""Independent validation for the R0.73F finite diagnostic.

This file does not import the primary producer.  It reconstructs the finite
operator from explicit Fourier coefficients and repeats selected propagations
at a finer fast-time step.  Agreement remains finite binary64 evidence only.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import sys
import time


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--primary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


ARGS = parse_args()
if ARGS.deps:
    sys.path.insert(0, ARGS.deps)

import numpy as np  # noqa: E402
from scipy.linalg import eig, expm, orth, svdvals  # noqa: E402


GAMMA = 0.5
MU = 0.25
START = time.perf_counter()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def opnorm(matrix: np.ndarray) -> float:
    return float(svdvals(matrix, check_finite=False)[0])


def conorm(matrix: np.ndarray) -> float:
    return float(svdvals(matrix, check_finite=False)[-1])


def matrix_fourier(N: int, epsilon: float, d: float, sign: int = 1) -> np.ndarray:
    modes = np.arange(-N, N + 1, dtype=int)
    lam = modes.astype(float) ** 2 + MU
    shifts = modes[:, None] - modes[None, :]
    e1 = math.exp(-d)
    e4 = math.exp(-4.0 * d)
    w_hat = {
        1: 0.25j * e1,
        -1: -0.25j * e1,
        2: -0.125j * e4,
        -2: 0.125j * e4,
    }
    wxx_hat = {
        1: -0.25j * e1,
        -1: 0.25j * e1,
        2: 0.5j * e4,
        -2: -0.5j * e4,
    }
    w = np.zeros(shifts.shape, dtype=np.complex128)
    wxx = np.zeros_like(w)
    for shift, value in w_hat.items():
        w[shifts == shift] = value
    for shift, value in wxx_hat.items():
        wxx[shifts == shift] = value
    raw = sign * (-1j * GAMMA) * (w + wxx / lam[None, :])
    transformed = (
        (1.0 / np.sqrt(lam))[:, None]
        * raw
        * np.sqrt(lam)[None, :]
    )
    transformed -= epsilon * np.diag(lam)
    return transformed


def matrix_recurrence_reference(
    N: int, epsilon: float, d: float, sign: int = 1
) -> np.ndarray:
    raw = np.zeros((2 * N + 1, 2 * N + 1), dtype=np.complex128)
    e1 = math.exp(-d)
    e4 = math.exp(-4.0 * d)
    for column, n in enumerate(range(-N, N + 1)):
        lam = n * n + MU
        values = (
            (1, GAMMA * 0.25 * e1 * (1.0 - 1.0 / lam)),
            (-1, -GAMMA * 0.25 * e1 * (1.0 - 1.0 / lam)),
            (2, GAMMA * e4 * (-0.125 + 0.5 / lam)),
            (-2, -GAMMA * e4 * (-0.125 + 0.5 / lam)),
        )
        for shift, value in values:
            target = n + shift
            if -N <= target <= N:
                raw[target + N, column] = sign * value
    modes = np.arange(-N, N + 1, dtype=float)
    lam = modes * modes + MU
    result = (
        (1.0 / np.sqrt(lam))[:, None] * raw * np.sqrt(lam)[None, :]
    )
    result -= epsilon * np.diag(lam)
    return result


def finite_top_basis(matrix: np.ndarray, tolerance: float) -> tuple[np.ndarray, dict[str, float]]:
    values, right = eig(matrix, right=True, check_finite=False)
    edge = float(np.max(values.real))
    indices = np.flatnonzero(values.real >= edge - tolerance)
    basis = orth(right[:, indices], rcond=1e-12)
    other = np.delete(values, indices)
    return basis, {
        "dimension": int(len(indices)),
        "spectralAbscissa": edge,
        "realGap": edge - float(np.max(other.real)),
    }


def cf4_step(N: int, epsilon: float, theta: float, h: float, sign: int) -> np.ndarray:
    root3 = math.sqrt(3.0)
    c1 = 0.5 - root3 / 6.0
    c2 = 0.5 + root3 / 6.0
    a1 = (3.0 - 2.0 * root3) / 12.0
    a2 = (3.0 + 2.0 * root3) / 12.0
    first = matrix_fourier(N, epsilon, epsilon * (theta + c1 * h), sign)
    second = matrix_fourier(N, epsilon, epsilon * (theta + c2 * h), sign)
    early = expm(h * (a2 * first + a1 * second))
    late = expm(h * (a1 * first + a2 * second))
    return late @ early


def propagate(N: int, epsilon: float, d_end: float, step: float, sign: int = 1) -> dict[str, float]:
    dimension = 2 * N + 1
    state = np.eye(dimension, dtype=np.complex128)
    scale = float(np.linalg.norm(state, ord="fro"))
    state /= scale
    log_scale = math.log(scale)
    basis, top = finite_top_basis(
        matrix_fourier(N, epsilon, 0.0, sign), 1e-8
    )
    theta = 0.0
    target = d_end / epsilon
    while theta < target - 1e-13:
        h = min(step, target - theta)
        state = cf4_step(N, epsilon, theta, h, sign) @ state
        local = float(np.linalg.norm(state, ord="fro"))
        state /= local
        log_scale += math.log(local)
        theta += h
    full = log_scale + math.log(opnorm(state))
    top_log = log_scale + math.log(conorm(state @ basis))
    return {
        "logFullNorm": full,
        "logTopConorm": top_log,
        "normalizedFullRate": epsilon * full / d_end,
        "normalizedTopRate": epsilon * top_log / d_end,
        "finiteTopDimension": top["dimension"],
        "finiteTopSpectralAbscissa": top["spectralAbscissa"],
        "finiteTopRealGap": top["realGap"],
    }


def main() -> int:
    config = json.loads(ARGS.config.read_text(encoding="utf-8"))
    primary = json.loads(ARGS.primary.read_text(encoding="utf-8"))
    rows_path = ARGS.primary.parent / "moving_gain_rows.csv"
    with rows_path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    endpoint = float(config["diagnosticPhysicalEndpoint"])
    expected = {
        (int(row["N"]), float(row["epsilon"])): row
        for row in rows
        if abs(float(row["physicalTime"]) - endpoint) < 1e-14
    }

    maximum_matrix_error = 0.0
    maximum_log_error = 0.0
    maximum_rate_error = 0.0
    maximum_sign_error = 0.0
    validations = []
    independent_step = float(config["primaryFastStep"]) / 2.0
    for sentinel in config["independentSentinels"]:
        N = int(sentinel["N"])
        epsilon = float(sentinel["epsilon"])
        for d in (0.0, endpoint / 2.0, endpoint):
            matrix_error = opnorm(
                matrix_fourier(N, epsilon, d)
                - matrix_recurrence_reference(N, epsilon, d)
            )
            maximum_matrix_error = max(maximum_matrix_error, matrix_error)
        actual = propagate(N, epsilon, endpoint, independent_step)
        reference = expected[(N, epsilon)]
        errors = {
            "fullLog": abs(actual["logFullNorm"] - float(reference["logFullNorm"])),
            "topLog": abs(actual["logTopConorm"] - float(reference["logTopConorm"])),
            "fullRate": abs(actual["normalizedFullRate"] - float(reference["normalizedFullRate"])),
            "topRate": abs(actual["normalizedTopRate"] - float(reference["normalizedTopRate"])),
        }
        maximum_log_error = max(maximum_log_error, errors["fullLog"], errors["topLog"])
        maximum_rate_error = max(maximum_rate_error, errors["fullRate"], errors["topRate"])
        plus = matrix_fourier(N, epsilon, endpoint, 1)
        minus = matrix_fourier(N, epsilon, endpoint, -1)
        reversal = np.eye(2 * N + 1, dtype=np.complex128)[::-1]
        sign_error = opnorm(minus - reversal @ plus.conjugate() @ reversal)
        maximum_sign_error = max(maximum_sign_error, sign_error)
        validations.append({
            "N": N,
            "epsilon": epsilon,
            "independentFastStep": independent_step,
            "actual": actual,
            "errors": errors,
            "signGeneratorConjugacyDefect": sign_error,
        })

    sizes = config["counterexampleSizes"]
    maximum_counterexample_error = 0.0
    for size in sizes:
        n = float(size)
        block = np.asarray([[-n, n * n], [0.0, -n]])
        closed = math.exp(-1.0) * np.asarray([[1.0, n], [0.0, 1.0]])
        maximum_counterexample_error = max(
            maximum_counterexample_error, opnorm(expm(block / n) - closed)
        )

    phase = np.linspace(0.0, 1.0, int(config["counterexamplePhaseGridCount"]))
    lambdas = np.stack([
        np.cos(2.0 * np.pi * phase - 2.0 * np.pi * j / 3.0) - 0.25
        for j in range(3)
    ])
    rotating_floor = float(np.min(np.max(lambdas, axis=0)))
    tolerances = config["tolerances"]
    boundary = primary["claimBoundary"]
    checks = {
        "primaryProducerBindingMatches": (
            sha256(Path(primary["sourceBinding"]["path"]))
            == primary["sourceBinding"]["sha256"]
        ),
        "primaryAllChecksPass": primary["allPrimaryChecksPass"] is True,
        "independentFourierVsRecurrenceMatrices": (
            maximum_matrix_error < float(tolerances["matrixConstructionMaximumAbsolute"])
        ),
        "independentFineStepLogGains": (
            maximum_log_error < float(tolerances["independentLogGainAbsolute"])
        ),
        "independentFineStepNormalizedRates": (
            maximum_rate_error < float(tolerances["independentNormalizedRateAbsolute"])
        ),
        "independentSignConjugacy": (
            maximum_sign_error < float(tolerances["signGeneratorConjugacy"])
        ),
        "nonnormalClosedFormRecomputed": (
            maximum_counterexample_error < float(tolerances["exactCounterexampleResidual"])
        ),
        "rotatingPositiveEdgeQuarterFloor": rotating_floor >= 0.25 - 2e-12,
        "claimBoundaryFailClosed": (
            boundary["finiteBinary64Diagnostic"] is True
            and all(value is False for key, value in boundary.items()
                    if key != "finiteBinary64Diagnostic")
        ),
    }
    # The config uses a more explicit key for the generator check.
    checks["independentSignConjugacy"] = (
        maximum_sign_error < float(tolerances["signGeneratorConjugacy"])
    )
    checks = {key: bool(value) for key, value in checks.items()}
    output = {
        "schemaVersion": "r073f-independent-validation-v1",
        "release": "R0.73F-finite-diagnostic",
        "primary": {"path": str(ARGS.primary), "sha256": sha256(ARGS.primary)},
        "validator": {
            "path": "experiments/r073f/independent_validate.py",
            "sha256": sha256(Path(__file__).resolve()),
            "importsPrimaryProducer": False,
        },
        "maximums": {
            "matrixConstructionAbsolute": maximum_matrix_error,
            "logGainAbsolute": maximum_log_error,
            "normalizedRateAbsolute": maximum_rate_error,
            "signGeneratorConjugacy": maximum_sign_error,
            "counterexampleClosedForm": maximum_counterexample_error,
        },
        "rotatingEdgeSampledFloor": rotating_floor,
        "validations": validations,
        "checks": checks,
        "allChecksPass": all(checks.values()),
        "wallTimeSeconds": time.perf_counter() - START,
        "claimBoundary": boundary,
    }
    ARGS.output.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 0 if output["allChecksPass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
