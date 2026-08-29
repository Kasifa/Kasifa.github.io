#!/usr/bin/env python3
"""Finite Fourier diagnostics for the R0.73D viscous spectral cluster.

The computation is performed after the exact kinetic-space isometry

    U = mu^(-1/2) L_mu^(-1/2): X_mu -> L2.

Thus Euclidean matrix norms diagnose the physical X_mu operator norm for the
finite compression.  They remain finite-dimensional diagnostics: cutoff
agreement, small residuals, and sampled projector convergence do not prove
the continuum theorem, the isolating contour, or algebraic simplicity.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default=os.environ.get("R073D_DEPS", ""))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--progress", type=Path, required=True)
    parser.add_argument("--cutoffs", default="24,48,96,128")
    parser.add_argument(
        "--epsilons",
        default="0,1e-2,3e-3,1e-3,3e-4,1e-4,3e-5,1e-5,3e-6,1e-6,1e-7,1e-8",
    )
    return parser.parse_args()


ARGS = parse_args()
if ARGS.deps:
    sys.path.insert(0, ARGS.deps)

import numpy as np  # noqa: E402
import scipy  # noqa: E402
from scipy.linalg import eig, svdvals  # noqa: E402


GAMMA = 0.5
MU = GAMMA * GAMMA
SOURCE = Path(__file__).resolve()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def emit(event: str, **fields: object) -> None:
    row = {"event": event, **fields}
    with ARGS.progress.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(row, sort_keys=True) + "\n")
    print(json.dumps(row, sort_keys=True), file=sys.stderr, flush=True)


def inviscid_vorticity_matrix(N: int) -> np.ndarray:
    """Return P_N A_(1/2) P_N in the raw vorticity Fourier basis."""
    matrix = np.zeros((2 * N + 1, 2 * N + 1), dtype=np.complex128)
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
                matrix[m + N, column] = value
    return matrix


def kinetic_matrix(N: int, epsilon: float) -> np.ndarray:
    """Return U P_N(A-epsilon L)P_N U^{-1} on modes -N,...,N."""
    modes = np.arange(-N, N + 1, dtype=float)
    lam = modes * modes + MU
    raw = inviscid_vorticity_matrix(N)
    transformed = ((1.0 / np.sqrt(lam))[:, None]
                   * raw
                   * np.sqrt(lam)[None, :])
    transformed -= epsilon * np.diag(lam)
    return transformed


def leading_eigenpair(N: int, epsilon: float) -> dict[str, object]:
    matrix = kinetic_matrix(N, epsilon)
    values, left, right = eig(
        matrix, left=True, right=True, check_finite=False
    )
    index = int(np.argmax(values.real))
    value = values[index]
    lvec = left[:, index] / np.linalg.norm(left[:, index])
    rvec = right[:, index] / np.linalg.norm(right[:, index])
    pairing = np.vdot(lvec, rvec)
    projector = np.outer(rvec, lvec.conjugate()) / pairing

    larger = kinetic_matrix(N + 2, epsilon)
    padded = np.zeros(2 * (N + 2) + 1, dtype=np.complex128)
    padded[2:-2] = rvec
    residual = larger @ padded - value * padded

    return {
        "N": N,
        "dimension": 2 * N + 1,
        "epsilon": epsilon,
        "lambdaReal": float(value.real),
        "lambdaImag": float(value.imag),
        "embeddedResidual": float(np.linalg.norm(residual)),
        "leftRightPairingAbs": float(abs(pairing)),
        "projectorNorm": float(svdvals(projector, check_finite=False)[0]),
        "rightVector": rvec,
        "leftVector": lvec,
        "projector": projector,
    }


def public_record(private: dict[str, object], inviscid_projector: np.ndarray) -> dict[str, object]:
    projector = private["projector"]
    return {
        "N": private["N"],
        "dimension": private["dimension"],
        "epsilon": private["epsilon"],
        "lambdaReal": private["lambdaReal"],
        "lambdaImag": private["lambdaImag"],
        "embeddedResidual": private["embeddedResidual"],
        "leftRightPairingAbs": private["leftRightPairingAbs"],
        "projectorNorm": private["projectorNorm"],
        "projectorDifferenceFromEpsilonZero": float(
            svdvals(projector - inviscid_projector, check_finite=False)[0]
        ),
        "kineticFiniteCompression": True,
        "finiteDimensionalOnly": True,
    }


def main() -> int:
    cutoffs = [int(item) for item in ARGS.cutoffs.split(",")]
    epsilons = [float(item) for item in ARGS.epsilons.split(",")]
    if sorted(set(cutoffs)) != cutoffs or any(item < 4 for item in cutoffs):
        raise ValueError("cutoffs must be distinct, increasing, and at least 4")
    if epsilons[0] != 0.0 or any(item < 0.0 for item in epsilons):
        raise ValueError("epsilons must begin with zero and be nonnegative")

    ARGS.output.parent.mkdir(parents=True, exist_ok=True)
    ARGS.progress.parent.mkdir(parents=True, exist_ok=True)
    ARGS.progress.write_text("", encoding="utf-8")
    emit(
        "start",
        cutoffs=cutoffs,
        epsilons=epsilons,
        gamma=GAMMA,
        mu=MU,
        finiteDimensionalOnly=True,
    )

    rows: list[dict[str, object]] = []
    for N in cutoffs:
        base = leading_eigenpair(N, 0.0)
        emit(
            "cutoff-start",
            N=N,
            dimension=2 * N + 1,
            inviscidLeadingReal=base["lambdaReal"],
        )
        for epsilon in epsilons:
            private = base if epsilon == 0.0 else leading_eigenpair(N, epsilon)
            record = public_record(private, base["projector"])
            rows.append(record)
            emit(
                "eigenpair",
                N=N,
                epsilon=epsilon,
                lambdaReal=record["lambdaReal"],
                embeddedResidual=record["embeddedResidual"],
                projectorNorm=record["projectorNorm"],
                projectorDifference=record[
                    "projectorDifferenceFromEpsilonZero"
                ],
                finiteDimensionalOnly=True,
            )
        emit("cutoff-complete", N=N, rows=len(epsilons))

    by_key = {(row["N"], row["epsilon"]): row for row in rows}
    largest = cutoffs[-1]
    previous = cutoffs[-2]
    cutoff_differences = []
    for epsilon in epsilons:
        a = by_key[(largest, epsilon)]
        b = by_key[(previous, epsilon)]
        cutoff_differences.append(
            {
                "epsilon": epsilon,
                "lambdaAbsoluteDifference": abs(
                    complex(a["lambdaReal"], a["lambdaImag"])
                    - complex(b["lambdaReal"], b["lambdaImag"])
                ),
                "projectorNormAbsoluteDifference": abs(
                    float(a["projectorNorm"])
                    - float(b["projectorNorm"])
                ),
            }
        )

    largest_rows = [row for row in rows if row["N"] == largest]
    positive = all(float(row["lambdaReal"]) > 0.0 for row in largest_rows)
    max_cutoff_eigen = max(
        float(row["lambdaAbsoluteDifference"])
        for row in cutoff_differences
    )
    max_residual = max(float(row["embeddedResidual"]) for row in rows)
    max_residual_largest = max(
        float(row["embeddedResidual"])
        for row in largest_rows
    )
    payload = {
        "schemaVersion": "r073d-viscous-cluster-diagnostic-v1",
        "release": "R0.73D",
        "created": "2026-08-30",
        "parameters": {
            "gamma": GAMMA,
            "mu": MU,
            "cutoffs": cutoffs,
            "epsilons": epsilons,
            "selectionRule": "largest real part of each finite compression",
            "space": "U_mu X_mu = L2 finite Fourier compression",
        },
        "sourceBinding": {
            "path": "research/r073d_viscous_cluster_diagnostic.py",
            "sha256": sha256(SOURCE),
        },
        "environment": {
            "python": platform.python_version(),
            "pythonImplementation": platform.python_implementation(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "threadEnvironment": {
                key: os.environ.get(key)
                for key in (
                    "OMP_NUM_THREADS",
                    "OPENBLAS_NUM_THREADS",
                    "VECLIB_MAXIMUM_THREADS",
                )
            },
        },
        "rows": rows,
        "cutoffComparisons": cutoff_differences,
        "checks": {
            "largestCutoffRowsRemainPositive": positive,
            "largestCutoffMaximumEmbeddedResidualBelow1eMinus10": (
                max_residual_largest < 1e-10
            ),
            "largestTwoCutoffsEigenvaluesAgreeBelow1eMinus9": (
                max_cutoff_eigen < 1e-9
            ),
        },
        "maximums": {
            "embeddedResidualAllCutoffs": max_residual,
            "embeddedResidualLargestCutoff": max_residual_largest,
            "largestTwoCutoffsEigenvalueDifference": max_cutoff_eigen,
        },
        "claimBoundary": {
            "finiteKineticCompressionComputed": True,
            "finiteProjectorNormsComputed": True,
            "finiteProjectorDifferencesComputed": True,
            "ordinaryCutoffConvergenceIsContinuumProof": False,
            "inviscidClusterRadiusCertifiedHere": False,
            "infiniteDimensionalPersistenceProvedHere": False,
            "algebraicSimplicityProvedHere": False,
            "complementaryDichotomyProvedHere": False,
            "nonautonomousTransferProvedHere": False,
            "nonlinearNavierStokesProvedHere": False,
            "clayProblemSolved": False,
        },
    }
    ARGS.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    emit(
        "complete",
        output=str(ARGS.output),
        rows=len(rows),
        maximumEmbeddedResidualAllCutoffs=max_residual,
        maximumEmbeddedResidualLargestCutoff=max_residual_largest,
        maximumCutoffEigenvalueDifference=max_cutoff_eigen,
        finiteDimensionalOnly=True,
    )
    return 0 if all(payload["checks"].values()) else 2


if __name__ == "__main__":
    raise SystemExit(main())
