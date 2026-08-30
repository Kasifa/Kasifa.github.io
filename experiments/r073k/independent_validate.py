#!/usr/bin/env python3
"""Independent finite validator for the R0.73K viscous-branch diagnostic.

This program never imports the primary producer.  It reconstructs W_d and
W_d'' from their explicit Fourier coefficients, forms

    -i gamma (M_W + M_W'' L^{-1}) - epsilon L,

and only then applies the kinetic-space diagonal conjugation.  Agreement is
evidence about two finite computations, not a continuum spectral proof.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import sys
import time
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default=os.environ.get("R073K_DEPS", ""))
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--primary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--progress", type=Path, required=True)
    parser.add_argument("--resources", type=Path, required=True)
    return parser.parse_args()


ARGS = parse_args()
if ARGS.deps:
    sys.path.insert(0, ARGS.deps)

import numpy as np  # noqa: E402
from scipy.linalg import eig  # noqa: E402


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
START = time.monotonic()


class ValidationFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationFailure(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


class Monitor:
    def __init__(self) -> None:
        for path in (ARGS.progress, ARGS.resources):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("", encoding="utf-8")

    def emit(self, event: str, **fields: object) -> None:
        row = {
            "event": event,
            "timestampUtc": utc_now(),
            "elapsedSeconds": time.monotonic() - START,
            **fields,
        }
        with ARGS.progress.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(row, sort_keys=True) + "\n")
        print(json.dumps(row, sort_keys=True), flush=True)

    def sample(self, event: str, **fields: object) -> None:
        usage = resource.getrusage(resource.RUSAGE_SELF)
        try:
            load_average: list[float] | None = list(os.getloadavg())
        except OSError:
            load_average = None
        row = {
            "event": event,
            "timestampUtc": utc_now(),
            "elapsedSeconds": time.monotonic() - START,
            "userCpuSeconds": usage.ru_utime,
            "systemCpuSeconds": usage.ru_stime,
            "maximumResidentSetSizePlatformUnits": usage.ru_maxrss,
            "loadAverage": load_average,
            **fields,
        }
        with ARGS.resources.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(row, sort_keys=True) + "\n")


def explicit_fourier_kinetic_matrix(
    cutoff: int, d_value: float, epsilon: float, gamma: float,
) -> np.ndarray:
    """Construct independently from Fourier coefficients of W and W''."""
    mu = gamma * gamma
    modes = np.arange(-cutoff, cutoff + 1, dtype=int)
    ell = modes.astype(float) ** 2 + mu
    shifts = modes[:, None] - modes[None, :]
    a = math.exp(-d_value)
    b = math.exp(-4.0 * d_value)
    w_hat = {
        1: 0.25j * a,
        -1: -0.25j * a,
        2: -0.125j * b,
        -2: 0.125j * b,
    }
    w = np.zeros(shifts.shape, dtype=np.complex128)
    wxx = np.zeros(shifts.shape, dtype=np.complex128)
    for shift, coefficient in w_hat.items():
        mask = shifts == shift
        w[mask] = coefficient
        wxx[mask] = -(shift * shift) * coefficient
    raw = -1j * gamma * (w + wxx / ell[None, :])
    matrix = ((1.0 / np.sqrt(ell))[:, None]
              * raw
              * np.sqrt(ell)[None, :])
    matrix -= epsilon * np.diag(ell)
    return matrix


def stable_low_rank_norm(left: np.ndarray, right: np.ndarray) -> float:
    """Compute ||left right^*|| from a rank-two QR core.

    Forming separate Gram matrices loses relative accuracy when two
    projectors are almost identical.  The QR core keeps that subtraction in
    the original factors and is stable at the observed 1e-12 cutoff scale.
    """
    _, left_triangular = np.linalg.qr(left, mode="reduced")
    _, right_triangular = np.linalg.qr(right, mode="reduced")
    core = left_triangular @ right_triangular.conjugate().T
    return float(np.linalg.norm(core, ord=2))


def projector_difference(
    first: dict[str, Any], second: dict[str, Any], target_cutoff: int,
) -> float:
    dimension = 2 * target_cutoff + 1

    def embed(vector: np.ndarray, cutoff: int) -> np.ndarray:
        output = np.zeros(dimension, dtype=np.complex128)
        offset = target_cutoff - cutoff
        require(offset >= 0, "invalid cross-cutoff embedding")
        output[offset:offset + vector.size] = vector
        return output

    r1 = embed(first["right"], int(first["cutoff"]))
    l1 = embed(first["left"], int(first["cutoff"]))
    r2 = embed(second["right"], int(second["cutoff"]))
    l2 = embed(second["left"], int(second["cutoff"]))
    left = np.column_stack((r1 / first["pairing"],
                            -r2 / second["pairing"]))
    right = np.column_stack((l1, l2))
    return stable_low_rank_norm(left, right)


def solve(
    cutoff: int,
    d_value: float,
    epsilon: float,
    gamma: float,
    center: complex,
    radius: float,
    regime: str,
    previous: complex | None,
    padding: int,
) -> dict[str, Any]:
    matrix = explicit_fourier_kinetic_matrix(cutoff, d_value, epsilon, gamma)
    values, left, right = eig(matrix, left=True, right=True,
                              check_finite=False)
    inside = np.flatnonzero(np.abs(values - center) < radius)
    if regime == "core":
        require(inside.size == 1,
                "independent fixed-circle count is not one")
        index = int(inside[0])
        continuation = None
    else:
        require(previous is not None, "independent continuation lacks anchor")
        index = int(np.argmin(np.abs(values - previous)))
        continuation = float(abs(values[index] - previous))
    value = complex(values[index])
    lvec = left[:, index] / np.linalg.norm(left[:, index])
    rvec = right[:, index] / np.linalg.norm(right[:, index])
    pairing = complex(np.vdot(lvec, rvec))
    require(abs(pairing) > 100.0 * np.finfo(float).eps,
            "independent selected eigenpair is numerically defective")
    algebraic_right = float(np.linalg.norm(matrix @ rvec - value * rvec))
    algebraic_left = float(np.linalg.norm(
        matrix.conjugate().T @ lvec - value.conjugate() * lvec
    ))
    overlap = float(abs(pairing))
    projector_left_factor = rvec / pairing
    idempotency_scalar = complex(np.vdot(lvec, projector_left_factor) - 1.0)
    projector_idempotency = float(
        abs(idempotency_scalar)
        * np.linalg.norm(projector_left_factor)
        * np.linalg.norm(lvec)
    )
    larger = explicit_fourier_kinetic_matrix(
        cutoff + padding, d_value, epsilon, gamma,
    )
    padded_right = np.zeros(larger.shape[0], dtype=np.complex128)
    padded_left = np.zeros(larger.shape[0], dtype=np.complex128)
    padded_right[padding:-padding] = rvec
    padded_left[padding:-padding] = lvec
    return {
        "cutoff": cutoff,
        "value": value,
        "left": lvec,
        "right": rvec,
        "pairing": pairing,
        "fixedContourCount": int(inside.size),
        "insideFixedContour": bool(abs(value - center) < radius),
        "continuationDistance": continuation,
        "rightEmbeddedResidual": float(np.linalg.norm(
            larger @ padded_right - value * padded_right
        )),
        "leftEmbeddedResidual": float(np.linalg.norm(
            larger.conjugate().T @ padded_left
            - value.conjugate() * padded_left
        )),
        "overlap": overlap,
        "projectorNorm": float(1.0 / overlap),
        "rightAlgebraicResidual": algebraic_right,
        "leftAlgebraicResidual": algebraic_left,
        "bpMinusLambdaPResidual": algebraic_right / overlap,
        "pbMinusLambdaPResidual": algebraic_left / overlap,
        "projectorIdempotencyResidualLowRank": projector_idempotency,
    }


def finite_metrics(
    state: dict[str, Any], base: dict[str, Any], gamma: float,
) -> dict[str, Any]:
    value = complex(state["value"])
    value0 = complex(base["value"])
    epsilon = float(state["epsilon"])
    cutoff = int(state["cutoff"])
    modes = np.arange(-cutoff, cutoff + 1, dtype=float)
    ell = modes * modes + gamma * gamma
    l0 = base["left"]
    r0 = base["right"]
    r_eps = state["right"]
    first_order = -complex(np.vdot(l0, ell * r0)) / complex(np.vdot(l0, r0))
    if epsilon == 0.0:
        quotient = exact = None
        quotient_exact_difference = quotient_first_difference = None
        identity_residual = 0.0
        p_difference = 0.0
    else:
        denominator = complex(np.vdot(l0, r_eps))
        quotient = (value - value0) / epsilon
        exact = -complex(np.vdot(l0, ell * r_eps)) / denominator
        quotient_exact_difference = float(abs(quotient - exact))
        quotient_first_difference = float(abs(quotient - first_order))
        identity_residual = float(abs(
            (value - value0) * denominator
            + epsilon * complex(np.vdot(l0, ell * r_eps))
        ))
        p_difference = projector_difference(state, base, cutoff)
    return {
        "lambdaReal": float(value.real),
        "lambdaImag": float(value.imag),
        "rightEmbeddedResidual": state["rightEmbeddedResidual"],
        "leftEmbeddedResidual": state["leftEmbeddedResidual"],
        "rightAlgebraicResidual": state["rightAlgebraicResidual"],
        "leftAlgebraicResidual": state["leftAlgebraicResidual"],
        "bpMinusLambdaPResidual": state["bpMinusLambdaPResidual"],
        "pbMinusLambdaPResidual": state["pbMinusLambdaPResidual"],
        "projectorIdempotencyResidualLowRank": state[
            "projectorIdempotencyResidualLowRank"
        ],
        "leftRightOverlap": state["overlap"],
        "projectorNorm": state["projectorNorm"],
        "projectorDifferenceFromEpsilonZero": p_difference,
        "lambdaQuotientReal": None if quotient is None else float(quotient.real),
        "lambdaQuotientImag": None if quotient is None else float(quotient.imag),
        "exactAdjointQuotientReal": None if exact is None else float(exact.real),
        "exactAdjointQuotientImag": None if exact is None else float(exact.imag),
        "firstOrderReal": float(first_order.real),
        "firstOrderImag": float(first_order.imag),
        "quotientExactDifference": quotient_exact_difference,
        "quotientFirstDifference": quotient_first_difference,
        "unscaledAdjointIdentityResidual": identity_residual,
        "fixedContourCount": state["fixedContourCount"],
        "insideFixedContour": state["insideFixedContour"],
        "continuationDistance": state["continuationDistance"],
    }


def expected_metrics(row: dict[str, Any]) -> dict[str, Any]:
    quotient = row["lambdaDifferenceOverEpsilon"]
    exact = row["exactInviscidAdjointQuotient"]
    first = row["firstOrderAdjointFormulaAtZero"]
    return {
        "lambdaReal": row["lambda"]["real"],
        "lambdaImag": row["lambda"]["imag"],
        "rightEmbeddedResidual": row["rightEmbeddedResidual"],
        "leftEmbeddedResidual": row["leftEmbeddedResidual"],
        "rightAlgebraicResidual": row["rightAlgebraicResidual"],
        "leftAlgebraicResidual": row["leftAlgebraicResidual"],
        "bpMinusLambdaPResidual": row["bpMinusLambdaPResidual"],
        "pbMinusLambdaPResidual": row["pbMinusLambdaPResidual"],
        "projectorIdempotencyResidualLowRank": row[
            "projectorIdempotencyResidualLowRank"
        ],
        "leftRightOverlap": row["leftRightOverlap"],
        "projectorNorm": row["projectorNorm"],
        "projectorDifferenceFromEpsilonZero": row[
            "projectorDifferenceFromEpsilonZero"
        ],
        "lambdaQuotientReal": None if quotient is None else quotient["real"],
        "lambdaQuotientImag": None if quotient is None else quotient["imag"],
        "exactAdjointQuotientReal": None if exact is None else exact["real"],
        "exactAdjointQuotientImag": None if exact is None else exact["imag"],
        "firstOrderReal": first["real"],
        "firstOrderImag": first["imag"],
        "quotientExactDifference": row[
            "quotientMinusExactAdjointFormulaAbs"
        ],
        "quotientFirstDifference": row[
            "quotientMinusFirstOrderFormulaAbs"
        ],
        "unscaledAdjointIdentityResidual": row[
            "unscaledAdjointIdentityResidual"
        ],
        "fixedContourCount": row["fixedContourEigenvalueCount"],
        "insideFixedContour": row["selectedInsideFixedContour"],
        "continuationDistance": row["continuationDistance"],
    }


def run(monitor: Monitor) -> int:
    config = json.loads(ARGS.config.read_text(encoding="utf-8"))
    primary = json.loads(ARGS.primary.read_text(encoding="utf-8"))
    require(primary.get("status") == "passed" and primary.get("allChecksPass") is True,
            "primary diagnostic did not pass")
    require(primary["configurationBinding"]["sha256"] == sha256(ARGS.config),
            "primary configuration hash does not match")
    producer = ROOT / primary["sourceBinding"]["path"]
    require(producer.is_file(), "primary producer source is absent")
    require(primary["sourceBinding"]["sha256"] == sha256(producer),
            "primary producer source hash drift")
    gamma = float(config["gamma"])
    cutoffs = [int(value) for value in config["cutoffs"]]
    d_grid = config["dGrid"]
    core = [float(value) for value in config["coreEpsilons"]]
    stress = [float(value) for value in config["stressEpsilons"]]
    epsilons = core + stress
    contour = config["fixedContour"]
    center = complex(float(contour["centerReal"]),
                     float(contour["centerImag"]))
    radius = float(contour["radius"])
    padding = int(config["embeddingPadding"])
    tolerance = float(config["tolerances"]["independentAbsolute"])
    quotient_tolerance = float(
        config["tolerances"]["independentDifferenceQuotientAbsolute"]
    )
    expected_rows = {
        (int(row["N"]), int(row["dIndex"]), float(row["epsilon"])): row
        for row in primary["rows"]
    }
    require(len(expected_rows) == len(primary["rows"]),
            "primary row keys are not unique")
    expected_cross = {
        (int(row["smallN"]), int(row["largeN"]), int(row["dIndex"]),
         float(row["epsilon"])): row
        for row in primary["crossCutoffComparisons"]
    }
    monitor.emit("start", primary=str(ARGS.primary), rows=len(expected_rows),
                 finiteDimensionalOnly=True)
    monitor.sample("start")

    maximum_errors: dict[str, float] = {}
    states: dict[tuple[int, int, float], dict[str, Any]] = {}
    sentinels: list[dict[str, Any]] = []
    numeric_fields = (
        "lambdaReal", "lambdaImag", "rightEmbeddedResidual",
        "leftEmbeddedResidual", "rightAlgebraicResidual",
        "leftAlgebraicResidual", "bpMinusLambdaPResidual",
        "pbMinusLambdaPResidual", "projectorIdempotencyResidualLowRank",
        "leftRightOverlap", "projectorNorm",
        "projectorDifferenceFromEpsilonZero", "lambdaQuotientReal",
        "lambdaQuotientImag", "exactAdjointQuotientReal",
        "exactAdjointQuotientImag", "firstOrderReal", "firstOrderImag",
        "quotientExactDifference", "quotientFirstDifference",
        "unscaledAdjointIdentityResidual", "continuationDistance",
    )
    difference_quotient_fields = {
        "lambdaQuotientReal", "lambdaQuotientImag",
        "quotientExactDifference", "quotientFirstDifference",
    }
    discrete_agreement = True
    for cutoff in cutoffs:
        for d_index, d_row in enumerate(d_grid):
            d_value = float(d_row["value"])
            base: dict[str, Any] | None = None
            previous: dict[str, Any] | None = None
            for epsilon in epsilons:
                regime = "core" if epsilon in core else "stress"
                state = solve(
                    cutoff, d_value, epsilon, gamma, center, radius, regime,
                    None if previous is None else complex(previous["value"]),
                    padding,
                )
                state["epsilon"] = epsilon
                if epsilon == 0.0:
                    base = state
                require(base is not None, "independent zero state is absent")
                observed = finite_metrics(state, base, gamma)
                key = (cutoff, d_index, epsilon)
                require(key in expected_rows, f"primary row missing: {key}")
                expected = expected_metrics(expected_rows[key])
                for field in numeric_fields:
                    left_value = observed[field]
                    right_value = expected[field]
                    if left_value is None or right_value is None:
                        discrete_agreement &= left_value is None and right_value is None
                        continue
                    error = abs(float(left_value) - float(right_value))
                    maximum_errors[field] = max(maximum_errors.get(field, 0.0),
                                                error)
                discrete_agreement &= (
                    observed["fixedContourCount"] == expected["fixedContourCount"]
                    and observed["insideFixedContour"]
                    == expected["insideFixedContour"]
                )
                states[key] = state
                previous = state
                if cutoff == cutoffs[-1] and d_index in (0, len(d_grid) - 1) \
                        and epsilon in (0.0, 1e-3, 3e-3, 1e-2):
                    sentinels.append({
                        "N": cutoff,
                        "dIndex": d_index,
                        "dLabel": str(d_row["label"]),
                        "epsilon": epsilon,
                        "lambdaReal": observed["lambdaReal"],
                        "lambdaImag": observed["lambdaImag"],
                        "projectorNorm": observed["projectorNorm"],
                        "projectorDifferenceFromEpsilonZero": observed[
                            "projectorDifferenceFromEpsilonZero"
                        ],
                    })
                monitor.emit("row", N=cutoff, dIndex=d_index,
                             epsilon=epsilon, regime=regime)
                monitor.sample("row", N=cutoff, dIndex=d_index,
                               epsilon=epsilon)

    cross_lambda_error = 0.0
    cross_projector_error = 0.0
    cross_count = 0
    for small, large in zip(cutoffs[:-1], cutoffs[1:]):
        for d_index, _ in enumerate(d_grid):
            for epsilon in epsilons:
                key = (small, large, d_index, epsilon)
                require(key in expected_cross,
                        f"primary cross-cutoff row missing: {key}")
                first = states[(small, d_index, epsilon)]
                second = states[(large, d_index, epsilon)]
                observed_lambda = float(abs(
                    complex(first["value"]) - complex(second["value"])
                ))
                observed_projector = projector_difference(first, second, large)
                expected = expected_cross[key]
                cross_lambda_error = max(
                    cross_lambda_error,
                    abs(observed_lambda - float(expected[
                        "lambdaAbsoluteDifference"
                    ])),
                )
                cross_projector_error = max(
                    cross_projector_error,
                    abs(observed_projector - float(expected[
                        "embeddedProjectorDifference"
                    ])),
                )
                cross_count += 1
        monitor.emit("cross-cutoff", smallN=small, largeN=large)
        monitor.sample("cross-cutoff", smallN=small, largeN=large)
    maximum_errors["crossCutoffLambdaAbsoluteDifference"] = cross_lambda_error
    maximum_errors["crossCutoffEmbeddedProjectorDifference"] = cross_projector_error

    boundary = primary["claimBoundary"]
    checks = {
        "producerHashMatches": primary["sourceBinding"]["sha256"] == sha256(producer),
        "configurationHashMatches": (
            primary["configurationBinding"]["sha256"] == sha256(ARGS.config)
        ),
        "rowCountComplete": len(states) == len(expected_rows),
        "crossCutoffRowCountComplete": cross_count == len(expected_cross),
        "discreteFieldsAgree": bool(discrete_agreement),
        "allNumericFieldsAgreeWithinTolerance": all(
            error <= (
                quotient_tolerance
                if field in difference_quotient_fields else tolerance
            )
            for field, error in maximum_errors.items()
        ),
        "coreFixedCircleFailsClosedIndependently": all(
            state["fixedContourCount"] == 1
            for key, state in states.items() if key[2] in core
        ),
        "claimBoundaryFailsClosed": (
            boundary["finiteKineticCompressionComputed"] is True
            and boundary["bothAlgebraicResidualsComputed"] is True
            and boundary["finiteIntertwiningResidualsComputed"] is True
            and boundary[
                "finiteProjectorIdempotencyCheckedByLowRankFormula"
            ] is True
            and boundary["ordinaryCutoffAgreementIsContinuumProof"] is False
            and boundary["fixedCircleCountIsContinuumRieszRankProof"] is False
            and boundary["uniformViscosityThresholdCertifiedHere"] is False
            and boundary["infiniteDimensionalProjectionConvergenceProvedHere"] is False
            and boundary["complementSemigroupBoundProvedHere"] is False
            and boundary["nonlinearNavierStokesProvedHere"] is False
            and boundary["clayProblemSolved"] is False
        ),
    }
    all_checks_pass = bool(all(checks.values()))
    output = {
        "schemaVersion": "r073k-independent-finite-validation-v1",
        "release": "R0.73K",
        "createdUtc": utc_now(),
        "status": "passed" if all_checks_pass else "failed",
        "primary": {"path": str(ARGS.primary), "sha256": sha256(ARGS.primary)},
        "configuration": {"path": str(ARGS.config), "sha256": sha256(ARGS.config)},
        "validator": {
            "path": "experiments/r073k/independent_validate.py",
            "sha256": sha256(Path(__file__).resolve()),
            "importsPrimaryProducer": False,
            "matrixConstruction": "explicit Fourier coefficients of W_d and W_d''",
            "projectorNormConstruction": "stable two-column QR core",
        },
        "comparisonTolerances": {
            "ordinaryAbsolute": tolerance,
            "differenceQuotientAbsolute": quotient_tolerance,
            "reason": "division by epsilon amplifies independent eigensolver roundoff at epsilon=1e-8",
        },
        "maximumAbsoluteErrors": maximum_errors,
        "sentinels": sentinels,
        "checks": checks,
        "allChecksPass": all_checks_pass,
        "claimBoundary": {
            "independentFiniteRecomputation": True,
            "continuumTheoremCertifiedByThisValidator": False,
            "continuumRankOneClusterCertifiedHere": False,
            "uniformContinuumViscosityThresholdCertifiedHere": False,
            "nonlinearNavierStokesProvedHere": False,
        },
    }
    atomic_json(ARGS.output, output)
    monitor.sample("complete", allChecksPass=all_checks_pass)
    monitor.emit("complete", output=str(ARGS.output),
                 allChecksPass=all_checks_pass,
                 maximumAbsoluteError=max(maximum_errors.values()),
                 finiteDimensionalOnly=True)
    return 0 if all_checks_pass else 2


def main() -> int:
    monitor = Monitor()
    try:
        return run(monitor)
    except (ValidationFailure, KeyError, TypeError, ValueError) as error:
        output = {
            "schemaVersion": "r073k-independent-finite-validation-v1",
            "release": "R0.73K",
            "createdUtc": utc_now(),
            "status": "failed",
            "failure": f"{type(error).__name__}: {error}",
            "allChecksPass": False,
            "claimBoundary": {
                "finiteDimensionalOnly": True,
                "continuumTheoremCertifiedByThisValidator": False,
            },
        }
        atomic_json(ARGS.output, output)
        monitor.sample("failed")
        monitor.emit("failed", error=output["failure"])
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
