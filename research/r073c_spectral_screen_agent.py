#!/usr/bin/env python3
"""R0.73C finite Fourier screen and rigorous-enclosure design diagnostics.

This file deliberately separates two objects.

1. ``P_N A P_N`` is the ordinary finite Fourier--Galerkin compression.  Its
   eigenvalues and residuals are diagnostics only.
2. ``A^(N) = B + C P_N``, where

       B = -i gamma M_W,
       C = -i gamma M_{W''} L_gamma^{-1},

   is an infinite-dimensional finite-rank perturbation of the normal
   multiplication operator B.  It satisfies a genuine operator-norm error

       ||A - A^(N)|| <= gamma ||W''||_infty / ((N+1)^2 + gamma^2).

The script samples the finite Fredholm matrix for A^(N) on a Riesz contour.
Those samples are inputs for a future interval validator; they are not, by
themselves, a spectral enclosure.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default=os.environ.get("R073C_DEPS", ""))
    parser.add_argument("--active-N", type=int, default=48)
    parser.add_argument("--outer-N", type=int, default=192)
    parser.add_argument("--contour-samples", type=int, default=2048)
    parser.add_argument("--quadrature", type=int, default=32768)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--progress", type=Path)
    return parser.parse_args()


ARGS = parse_args()
if ARGS.deps:
    sys.path.insert(0, ARGS.deps)

import numpy as np  # noqa: E402
import scipy  # noqa: E402
from scipy.linalg import eig, eigvals, svdvals  # noqa: E402


PROGRESS: list[dict[str, object]] = []


def progress(event: str, **fields: object) -> None:
    row = {"event": event, **fields}
    PROGRESS.append(row)
    print(json.dumps(row, sort_keys=True), file=sys.stderr, flush=True)


def heat_coefficients() -> tuple[dict[int, complex], dict[int, complex]]:
    """Fourier coefficients of W(0) and W''(0)."""
    w = {1: 0.25j, -1: -0.25j, 2: -0.125j, -2: 0.125j}
    wxx = {1: -0.25j, -1: 0.25j, 2: 0.5j, -2: -0.5j}
    return w, wxx


def split_matrices(N: int, gamma: float) -> tuple[np.ndarray, np.ndarray]:
    """Return the finite matrices of B and C on modes -N,...,N."""
    modes = np.arange(-N, N + 1, dtype=int)
    lam = modes.astype(float) ** 2 + gamma * gamma
    shifts = modes[:, None] - modes[None, :]
    w_hat, wxx_hat = heat_coefficients()
    w = np.zeros(shifts.shape, dtype=np.complex128)
    wxx = np.zeros_like(w)
    for shift in w_hat:
        w[shifts == shift] = w_hat[shift]
        wxx[shifts == shift] = wxx_hat[shift]
    B = -1j * gamma * w
    C = -1j * gamma * wxx / lam[None, :]
    return B, C


def galerkin_matrix(N: int, gamma: float) -> np.ndarray:
    B, C = split_matrices(N, gamma)
    return B + C


def finite_rank_outer_matrix(outer_N: int, active_N: int,
                             gamma: float) -> np.ndarray:
    """Large outer compression of B + C P_active (diagnostic only)."""
    if active_N >= outer_N:
        raise ValueError("active_N must be smaller than outer_N")
    B, C = split_matrices(outer_N, gamma)
    modes = np.arange(-outer_N, outer_N + 1, dtype=int)
    C[:, np.abs(modes) > active_N] = 0.0
    return B + C


def ordered_eigenvalues(matrix: np.ndarray) -> np.ndarray:
    values = eigvals(matrix, check_finite=False)
    order = np.lexsort((-np.abs(values.imag), -values.real))
    return values[order]


def embedded_residual(N: int, gamma: float, value: complex,
                      vector: np.ndarray) -> float:
    """Exact l2 residual after embedding a P_N vector into P_{N+2}."""
    padded = np.zeros(2 * (N + 2) + 1, dtype=np.complex128)
    padded[2:-2] = vector
    residual = galerkin_matrix(N + 2, gamma) @ padded - value * padded
    return float(np.linalg.norm(residual) / np.linalg.norm(padded))


def leading_record(N: int, gamma: float) -> dict[str, object]:
    matrix = galerkin_matrix(N, gamma)
    values, left, right = eig(matrix, left=True, right=True,
                              check_finite=False)
    index = int(np.argmax(values.real))
    value = values[index]
    lvec = left[:, index] / np.linalg.norm(left[:, index])
    rvec = right[:, index] / np.linalg.norm(right[:, index])
    projector_condition = 1.0 / abs(np.vdot(lvec, rvec))
    ordered = values[np.argsort(values.real)[::-1]]
    return {
        "N": N,
        "dimension": 2 * N + 1,
        "gamma": gamma,
        "leadingReal": float(value.real),
        "leadingImag": float(value.imag),
        "secondReal": float(ordered[1].real),
        "secondImag": float(ordered[1].imag),
        "projectorCondition": float(projector_condition),
        "embeddedResidual": embedded_residual(N, gamma, value, rvec),
        "positiveRealCountAbove1e-3": int(np.sum(values.real > 1e-3)),
        "finiteDimensionalOnly": True,
    }


def finite_rank_record(active_N: int, outer_N: int,
                       gamma: float) -> dict[str, object]:
    values = ordered_eigenvalues(
        finite_rank_outer_matrix(outer_N, active_N, gamma))
    value = values[0]
    return {
        "activeN": active_N,
        "outerN": outer_N,
        "outerDimension": 2 * outer_N + 1,
        "leadingReal": float(value.real),
        "leadingImag": float(value.imag),
        "outerFourierCompressionOnly": True,
    }


def wxx_infinity() -> float:
    """Exact maximizer evaluation for W''=.5 sin(x)-sin(2x)."""
    t = (1.0 - math.sqrt(129.0)) / 16.0
    return math.sqrt((1.0 - t * t) * (0.5 - 2.0 * t) ** 2)


def compact_tail_bound(N: int, gamma: float) -> float:
    return (gamma * wxx_infinity()
            / ((N + 1) ** 2 + gamma * gamma))


def fredholm_contour(active_N: int, gamma: float, center: float,
                     radius: float, samples: int,
                     quadrature: int) -> dict[str, object]:
    """Sample M_N(z)=I-P_N(z-B)^(-1)CP_N on a circular contour."""
    if quadrature <= 4 * active_N:
        raise ValueError("quadrature grid is too small for requested modes")
    modes = np.arange(-active_N, active_N + 1, dtype=int)
    lam = modes.astype(float) ** 2 + gamma * gamma
    shifts = modes[:, None] - modes[None, :]
    x = 2.0 * math.pi * np.arange(quadrature) / quadrature
    w = -0.5 * np.sin(x) + 0.25 * np.sin(2.0 * x)
    wxx = 0.5 * np.sin(x) - np.sin(2.0 * x)
    identity = np.eye(2 * active_N + 1, dtype=np.complex128)

    minimum_singular = math.inf
    minimum_theta = 0.0
    maximum_inverse = 0.0
    maximum_j = 0.0
    phases: list[float] = []
    # Include the repeated endpoint only for the unwrapped winding number.
    for index in range(samples + 1):
        theta = 2.0 * math.pi * index / samples
        z = center + radius * np.exp(1j * theta)
        denominator = z + 1j * gamma * w
        h = wxx / denominator
        maximum_j = max(maximum_j,
                        float(np.sqrt(np.mean(np.abs(h) ** 2))))
        h_hat = np.fft.fft(h) / quadrature
        coefficient = h_hat[shifts % quadrature]
        K = (-1j * gamma) * coefficient / lam[None, :]
        fredholm = identity - K
        singular = float(svdvals(fredholm, check_finite=False)[-1])
        if singular < minimum_singular:
            minimum_singular = singular
            minimum_theta = theta
        maximum_inverse = max(maximum_inverse, 1.0 / singular)
        # Some Accelerate-backed NumPy builds emit harmless overflow warnings
        # while internally scaling a complex determinant.  slogdet's phase is
        # still the intended quantity, so silence only those floating warnings.
        with np.errstate(over="ignore", under="ignore", divide="ignore",
                         invalid="ignore"):
            sign, _ = np.linalg.slogdet(fredholm)
        if not (np.isfinite(sign.real) and np.isfinite(sign.imag)):
            raise FloatingPointError("non-finite Fredholm determinant phase")
        phases.append(float(np.angle(sign)))

    unwrapped = np.unwrap(np.asarray(phases))
    winding = float((unwrapped[-1] - unwrapped[0]) / (2.0 * math.pi))
    phase_increments = np.abs(np.diff(unwrapped))
    return {
        "activeN": active_N,
        "dimension": 2 * active_N + 1,
        "gamma": gamma,
        "center": center,
        "radius": radius,
        "minimumRealPartOnContour": center - radius,
        "samples": samples,
        "trapezoidQuadraturePoints": quadrature,
        "sampledMinimumSingularValue": minimum_singular,
        "sampledMaximumInverseNorm": maximum_inverse,
        "minimumTheta": minimum_theta,
        "sampledMaximumL2MultiplierJ": maximum_j,
        "sampledDeterminantWinding": winding,
        "maximumUnwrappedPhaseIncrement": float(np.max(phase_increments)),
        "intervalValidated": False,
    }


def enclosure_constants(active_N: int, gamma: float, center: float,
                        radius: float) -> dict[str, object]:
    """Conditional constants for the planned interval/Riesz validator."""
    x0 = center - radius
    sum_laplacian_inverse_sq = (
        math.pi / (2.0 * gamma ** 3) / math.tanh(math.pi * gamma)
        + math.pi ** 2 / (2.0 * gamma ** 2)
        / math.sinh(math.pi * gamma) ** 2
    )
    # These two rational ceilings still need interval validation on Gamma.
    j_ceiling = 3.7
    fredholm_inverse_ceiling = 20.0
    u_hilbert_schmidt_ceiling = (
        gamma * j_ceiling * math.sqrt(sum_laplacian_inverse_sq))
    resolvent_ceiling = ((1.0 + u_hilbert_schmidt_ceiling
                          * fredholm_inverse_ceiling) / x0)
    tail = compact_tail_bound(active_N, gamma)
    return {
        "exactSumLaplacianInverseSquared": sum_laplacian_inverse_sq,
        "proposedIntervalCeilingJ": j_ceiling,
        "proposedIntervalCeilingFredholmInverse":
            fredholm_inverse_ceiling,
        "conditionalUHilbertSchmidtCeiling":
            u_hilbert_schmidt_ceiling,
        "conditionalResolventCeiling": resolvent_ceiling,
        "operatorNormTailBound": tail,
        "conditionalNeumannProduct": tail * resolvent_ceiling,
        "conditionalRieszTransferPass": tail * resolvent_ceiling < 1.0,
        "formalStatus": "conditional-on-interval-validation-and-winding",
    }


def main() -> int:
    if ARGS.active_N < 4:
        raise ValueError("active-N must be at least 4")
    if ARGS.outer_N <= ARGS.active_N:
        raise ValueError("outer-N must exceed active-N")
    progress("run-start", activeN=ARGS.active_N, outerN=ARGS.outer_N,
             contourSamples=ARGS.contour_samples,
             quadrature=ARGS.quadrature)
    gamma_values = [0.25, 0.5, 0.75, 1.0,
                    math.sqrt(7.0) / 2.0, 1.5]
    convergence_N = [8, 12, 16, 24, 32, 48, 64, 96, 128]
    leading = [leading_record(N, gamma)
               for gamma in gamma_values for N in convergence_N]
    progress("galerkin-complete", rows=len(leading))
    finite_rank_N = [8, 12, 16, 24, 32, 40, ARGS.active_N]
    finite_rank_N = sorted(set(N for N in finite_rank_N
                               if N < ARGS.outer_N))
    finite_rank = [finite_rank_record(N, ARGS.outer_N, 0.5)
                   for N in finite_rank_N]
    progress("finite-rank-complete", rows=len(finite_rank))

    center = 0.1704
    radius = 0.06
    contour = fredholm_contour(
        ARGS.active_N, 0.5, center, radius,
        ARGS.contour_samples, ARGS.quadrature)
    progress("fredholm-complete",
             minimumSingular=contour["sampledMinimumSingularValue"],
             sampledWinding=contour["sampledDeterminantWinding"])
    constants = enclosure_constants(
        ARGS.active_N, 0.5, center, radius)
    result = {
        "schemaVersion": 1,
        "scope": "finite Fourier screen plus conditional Riesz-enclosure design",
        "operator": "A_gamma(0)=-i gamma (W+W_xx L_gamma^{-1})",
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "randomness": "none",
        "leadingGalerkinRows": leading,
        "finiteRankApproximationRows": finite_rank,
        "fredholmContourScreen": contour,
        "enclosureConstants": constants,
        "claimBoundary": {
            "finiteFourierSpectrumComputed": True,
            "compactInputTailBoundAnalytic": True,
            "fredholmContourSampled": True,
            "ordinaryCutoffConvergenceIsProof": False,
            "quadratureIntervalValidated": False,
            "fredholmInverseIntervalValidated": False,
            "determinantWindingIntervalValidated": False,
            "infiniteDimensionalEigenvalueEnclosed": False,
            "nonautonomousTransferProved": False,
        },
    }
    rendered = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if ARGS.output:
        ARGS.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    progress("run-complete", status="completed")
    if ARGS.progress:
        ARGS.progress.write_text(
            "".join(json.dumps(row, sort_keys=True) + "\n"
                    for row in PROGRESS),
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
