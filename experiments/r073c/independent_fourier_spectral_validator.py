#!/usr/bin/env python3
"""Independent finite-spectrum validator for the R0.73C Fourier screen.

The validator does not import the primary producer.  It reconstructs the
banded matrix from four explicit column recurrences, independently repeats
selected eigensystems, residuals, the finite-rank Fredholm contour screen,
and the conditional operator-tail arithmetic.

Passing this program proves agreement of two finite computations only.  It
never sets an infinite-dimensional spectral claim to true; that requires a
separate interval monodromy or Fourier-tail/Riesz certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default=os.environ.get("R073C_DEPS", ""))
    parser.add_argument("--primary", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--winding-nodes", type=int, default=512)
    parser.add_argument("--quadrature", type=int, default=8192)
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def alternate_matrix(np: object, N: int, gamma: float):
    """Build P_N A_gamma P_N from real column recurrences."""
    matrix = np.zeros((2 * N + 1, 2 * N + 1), dtype=np.complex128)
    for column, n in enumerate(range(-N, N + 1)):
        lam = n * n + gamma * gamma
        first = gamma * 0.25 * (1.0 - 1.0 / lam)
        second = gamma * (-0.125 + 0.5 / lam)
        for shift, value in ((1, first), (-1, -first),
                             (2, second), (-2, -second)):
            m = n + shift
            if -N <= m <= N:
                matrix[m + N, column] = value
    return matrix


def alternate_finite_rank_outer(np: object, outer_N: int, active_N: int,
                                gamma: float):
    """Outer compression of B+C P_active using a separate recurrence."""
    matrix = np.zeros((2 * outer_N + 1, 2 * outer_N + 1),
                      dtype=np.complex128)
    for column, n in enumerate(range(-outer_N, outer_N + 1)):
        lam = n * n + gamma * gamma
        use_compact = abs(n) <= active_N
        first = gamma * 0.25
        second = -gamma * 0.125
        if use_compact:
            first -= gamma * 0.25 / lam
            second += gamma * 0.5 / lam
        for shift, value in ((1, first), (-1, -first),
                             (2, second), (-2, -second)):
            m = n + shift
            if -outer_N <= m <= outer_N:
                matrix[m + outer_N, column] = value
    return matrix


def leading_data(np: object, N: int, gamma: float) -> dict[str, object]:
    matrix = alternate_matrix(np, N, gamma)
    values, right = np.linalg.eig(matrix)
    index = int(np.argmax(values.real))
    value = values[index]
    rvec = right[:, index] / np.linalg.norm(right[:, index])

    left_values, left_vectors = np.linalg.eig(matrix.conj().T)
    left_index = int(np.argmin(np.abs(left_values - value.conjugate())))
    lvec = left_vectors[:, left_index]
    lvec /= np.linalg.norm(lvec)
    condition = 1.0 / abs(np.vdot(lvec, rvec))

    padded = np.zeros(2 * (N + 2) + 1, dtype=np.complex128)
    padded[2:-2] = rvec
    residual = (alternate_matrix(np, N + 2, gamma) @ padded
                - value * padded)
    positive_imag = values[(values.real > 0.01) & (values.imag > 1e-8)]
    secondary = (positive_imag[np.argmax(positive_imag.real)]
                 if len(positive_imag) else None)
    return {
        "leadingReal": float(value.real),
        "leadingImag": float(value.imag),
        "embeddedResidual": float(np.linalg.norm(residual)),
        "projectorCondition": float(condition),
        "secondaryReal": (float(secondary.real)
                          if secondary is not None else None),
        "secondaryImag": (float(secondary.imag)
                          if secondary is not None else None),
    }


def fredholm_matrix(np: object, N: int, gamma: float, z: complex,
                    quadrature: int):
    modes = np.arange(-N, N + 1, dtype=int)
    lam = modes.astype(float) ** 2 + gamma * gamma
    shifts = modes[:, None] - modes[None, :]
    x = 2.0 * math.pi * np.arange(quadrature) / quadrature
    w = -0.5 * np.sin(x) + 0.25 * np.sin(2.0 * x)
    wxx = 0.5 * np.sin(x) - np.sin(2.0 * x)
    h_hat = np.fft.fft(wxx / (z + 1j * gamma * w)) / quadrature
    compact = (-1j * gamma) * h_hat[shifts % quadrature] / lam[None, :]
    return np.eye(2 * N + 1, dtype=np.complex128) - compact


def sampled_winding(np: object, N: int, gamma: float, center: float,
                    radius: float, nodes: int,
                    quadrature: int) -> dict[str, float]:
    phases = []
    minimum = math.inf
    maximum_inverse = 0.0
    for index in range(nodes + 1):
        theta = 2.0 * math.pi * index / nodes
        z = center + radius * np.exp(1j * theta)
        matrix = fredholm_matrix(np, N, gamma, z, quadrature)
        singular = float(np.linalg.svd(matrix, compute_uv=False)[-1])
        minimum = min(minimum, singular)
        maximum_inverse = max(maximum_inverse, 1.0 / singular)
        with np.errstate(over="ignore", under="ignore", divide="ignore",
                         invalid="ignore"):
            sign, _ = np.linalg.slogdet(matrix)
        if not (np.isfinite(sign.real) and np.isfinite(sign.imag)):
            raise FloatingPointError("non-finite determinant phase")
        phases.append(float(np.angle(sign)))
    unwrapped = np.unwrap(np.asarray(phases))
    return {
        "winding": float((unwrapped[-1] - unwrapped[0])
                          / (2.0 * math.pi)),
        "minimumSingular": minimum,
        "maximumInverse": maximum_inverse,
        "maximumPhaseIncrement": float(
            np.max(np.abs(np.diff(unwrapped)))),
    }


def main() -> int:
    args = parse_args()
    if args.deps:
        sys.path.insert(0, args.deps)
    import numpy as np

    primary_path = args.primary.resolve()
    primary = json.loads(primary_path.read_text(encoding="utf-8"))
    checks: dict[str, bool] = {}
    maximum_errors: dict[str, float] = {}
    sentinels: list[dict[str, object]] = []

    boundary = primary.get("claimBoundary", {})
    checks["primaryBoundaryIsFailClosed"] = (
        boundary.get("finiteFourierSpectrumComputed") is True
        and boundary.get("ordinaryCutoffConvergenceIsProof") is False
        and boundary.get("infiniteDimensionalEigenvalueEnclosed") is False
        and boundary.get("nonautonomousTransferProved") is False
    )
    rows = {(round(float(row["gamma"]), 14), int(row["N"])): row
            for row in primary["leadingGalerkinRows"]}

    eigen_errors = []
    residual_absolute_errors = []
    residual_relative_errors = []
    condition_errors = []
    for gamma in (0.25, 0.5, 0.75, 1.0):
        for N in (8, 24, 48, 96, 128):
            record = leading_data(np, N, gamma)
            expected = rows[(round(gamma, 14), N)]
            eigen_error = abs(complex(record["leadingReal"],
                                      record["leadingImag"])
                              - complex(expected["leadingReal"],
                                        expected["leadingImag"]))
            eigen_errors.append(eigen_error)
            residual_error = abs(
                record["embeddedResidual"]
                - float(expected["embeddedResidual"]))
            residual_absolute_errors.append(residual_error)
            residual_relative_errors.append(
                residual_error
                / max(float(expected["embeddedResidual"]), 1e-14))
            condition_errors.append(
                abs(record["projectorCondition"]
                    - float(expected["projectorCondition"])))
            if gamma == 0.5 and N in (8, 48, 128):
                sentinels.append({"gamma": gamma, "N": N, **record})
    maximum_errors["leadingEigenvalueAbsolute"] = max(eigen_errors)
    maximum_errors["embeddedResidualRelative"] = max(
        residual_relative_errors)
    maximum_errors["embeddedResidualAbsolute"] = max(
        residual_absolute_errors)
    maximum_errors["projectorConditionAbsolute"] = max(condition_errors)
    checks["independentBandedEigenvalues"] = max(eigen_errors) < 2e-12
    # At roundoff-scale residuals a relative comparison is meaningless.
    checks["independentEmbeddedResiduals"] = max(
        residual_absolute_errors) < 2e-12
    checks["independentProjectorConditions"] = max(condition_errors) < 2e-8

    half_96 = leading_data(np, 96, 0.5)
    half_128 = leading_data(np, 128, 0.5)
    checks["gammaHalfCandidateCutoffAgreement"] = (
        abs(half_96["leadingReal"] - half_128["leadingReal"]) < 2e-12
        and abs(half_128["leadingReal"] - 0.170407976920434) < 2e-12)
    checks["secondaryPairRecomputed"] = (
        abs(half_128["secondaryReal"] - 0.040539390616) < 2e-10
        and abs(half_128["secondaryImag"] - 0.176137671494) < 2e-10)

    pollution = []
    for N in (32, 64, 128):
        record = leading_data(np, N, math.sqrt(7.0) / 2.0)
        pollution.append(record)
    checks["neutralThresholdRightEdgeFlaggedAsPollution"] = (
        pollution[0]["leadingReal"] > pollution[1]["leadingReal"]
        > pollution[2]["leadingReal"] > 0.0
        and all(abs(row["leadingImag"]) > 0.3 for row in pollution))

    finite_rank_by_N = {int(row["activeN"]): row
                        for row in primary["finiteRankApproximationRows"]}
    finite_rank_errors = []
    for active_N in (8, 24, 48):
        outer_N = int(finite_rank_by_N[active_N]["outerN"])
        values = np.linalg.eigvals(alternate_finite_rank_outer(
            np, outer_N, active_N, 0.5))
        candidate = values[int(np.argmax(values.real))]
        expected = finite_rank_by_N[active_N]
        finite_rank_errors.append(abs(
            candidate - complex(expected["leadingReal"],
                                expected["leadingImag"])))
    maximum_errors["finiteRankOuterEigenvalueAbsolute"] = max(
        finite_rank_errors)
    checks["independentFiniteRankOuterSpots"] = max(
        finite_rank_errors) < 3e-12

    contour = primary["fredholmContourScreen"]
    center = float(contour["center"])
    radius = float(contour["radius"])
    N = int(contour["activeN"])
    spot_singular = []
    for theta in (0.0, math.pi / 2.0, float(contour["minimumTheta"]),
                  math.pi, 3.0 * math.pi / 2.0):
        matrix = fredholm_matrix(
            np, N, 0.5, center + radius * np.exp(1j * theta),
            args.quadrature)
        spot_singular.append(float(np.linalg.svd(
            matrix, compute_uv=False)[-1]))
    checks["fredholmContourSpotMargin"] = min(spot_singular) > 0.056

    winding = sampled_winding(
        np, N, 0.5, center, radius,
        args.winding_nodes, args.quadrature)
    checks["independentSampledWinding"] = (
        abs(winding["winding"] - 1.0) < 1e-12
        and winding["minimumSingular"] > 0.056
        and winding["maximumPhaseIncrement"] < 0.03)

    t_star = (1.0 - math.sqrt(129.0)) / 16.0
    wxx_infinity = math.sqrt(
        (1.0 - t_star * t_star) * (0.5 - 2.0 * t_star) ** 2)
    tail = 0.5 * wxx_infinity / (49.0 ** 2 + 0.25)
    gamma = 0.5
    sum_inverse_sq = (
        math.pi / (2.0 * gamma ** 3) / math.tanh(math.pi * gamma)
        + math.pi ** 2 / (2.0 * gamma ** 2)
        / math.sinh(math.pi * gamma) ** 2)
    u_ceiling = gamma * 3.7 * math.sqrt(sum_inverse_sq)
    resolvent_ceiling = (1.0 + 20.0 * u_ceiling) / (center - radius)
    product = tail * resolvent_ceiling
    constants = primary["enclosureConstants"]
    constant_errors = [
        abs(tail - float(constants["operatorNormTailBound"])),
        abs(sum_inverse_sq
            - float(constants["exactSumLaplacianInverseSquared"])),
        abs(resolvent_ceiling
            - float(constants["conditionalResolventCeiling"])),
        abs(product - float(constants["conditionalNeumannProduct"])),
    ]
    maximum_errors["conditionalConstantAbsolute"] = max(constant_errors)
    checks["independentConditionalTailArithmetic"] = (
        max(constant_errors) < 2e-12 and product < 0.402)

    # A root of the sampled Fredholm determinant is a consistency check only.
    root_z = 0.17040797692043336
    root_matrix = fredholm_matrix(
        np, N, 0.5, root_z, args.quadrature)
    root_singular = float(np.linalg.svd(
        root_matrix, compute_uv=False)[-1])
    checks["finiteRankRootConsistency"] = root_singular < 2e-12

    finite_values = [
        *maximum_errors.values(), *spot_singular,
        *winding.values(), root_singular,
        *(value for row in sentinels for value in row.values()
          if isinstance(value, (int, float))),
        *(value for row in pollution for value in row.values()
          if value is not None),
    ]
    checks["allRecordedNumbersFinite"] = all(
        math.isfinite(float(value)) for value in finite_values)

    checks = {key: bool(value) for key, value in checks.items()}
    status = "passed" if all(checks.values()) else "failed"
    validator_path = Path(__file__).resolve()
    result = {
        "schemaVersion": "r073c-independent-fourier-validation-v1",
        "status": status,
        "scope": "independent finite Fourier and sampled Fredholm validation",
        "primary": {
            "path": str(primary_path),
            "bytes": primary_path.stat().st_size,
            "sha256": sha256(primary_path),
        },
        "validator": {
            "path": str(validator_path),
            "bytes": validator_path.stat().st_size,
            "sha256": sha256(validator_path),
        },
        "parameters": {
            "windingNodes": args.winding_nodes,
            "quadraturePoints": args.quadrature,
            "randomness": "none",
        },
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "platform": platform.platform(),
            "threadEnvironment": {
                key: os.environ.get(key, "") for key in (
                    "OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS",
                    "VECLIB_MAXIMUM_THREADS")
            },
        },
        "checks": checks,
        "tolerances": {
            "leadingEigenvalueAbsolute": 2e-12,
            "embeddedResidualAbsolute": 2e-12,
            "projectorConditionAbsolute": 2e-8,
            "finiteRankOuterEigenvalueAbsolute": 3e-12,
            "fredholmSpotSingularLower": 0.056,
            "sampledPhaseIncrementUpper": 0.03,
        },
        "maximumErrors": maximum_errors,
        "recomputedSentinels": sentinels,
        "neutralThresholdRows": pollution,
        "fredholmSpotSingularValues": spot_singular,
        "independentWindingScreen": winding,
        "finiteRankRootSingularValue": root_singular,
        "claimBoundary": {
            "independentFiniteMatrixAgreement": status == "passed",
            "sampledFredholmWindingAgreement": status == "passed",
            "ordinaryCutoffConvergenceIsProof": False,
            "continuousContourEnclosed": False,
            "infiniteDimensionalSpectrumProved": False,
            "intervalMonodromyValidated": False,
            "fourierTailRieszCertificateValidated": False,
            "nonautonomousTransferProved": False,
            "nonlinearNavierStokesProved": False,
            "clayProblemSolved": False,
        },
    }
    rendered = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
