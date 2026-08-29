#!/usr/bin/env python3
"""Independent finite validator for the R0.73D kinetic-space diagnostic.

This program does not import the primary producer.  It reconstructs the
matrix from the Fourier coefficients of W and W'', rather than from the
primary column recurrence.  Agreement certifies two finite computations
only; it does not certify the infinite-dimensional theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--primary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


ARGS = parse_args()
if ARGS.deps:
    sys.path.insert(0, ARGS.deps)

import numpy as np  # noqa: E402
from scipy.linalg import eig, svdvals  # noqa: E402


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def independent_matrix(N: int, epsilon: float) -> np.ndarray:
    gamma = 0.5
    mu = 0.25
    modes = np.arange(-N, N + 1, dtype=int)
    lam = modes.astype(float) ** 2 + mu
    shifts = modes[:, None] - modes[None, :]

    w_hat = {1: 0.25j, -1: -0.25j, 2: -0.125j, -2: 0.125j}
    wxx_hat = {1: -0.25j, -1: 0.25j, 2: 0.5j, -2: -0.5j}
    w = np.zeros(shifts.shape, dtype=np.complex128)
    wxx = np.zeros_like(w)
    for shift, coefficient in w_hat.items():
        w[shifts == shift] = coefficient
    for shift, coefficient in wxx_hat.items():
        wxx[shifts == shift] = coefficient

    raw = -1j * gamma * (w + wxx / lam[None, :])
    transformed = ((1.0 / np.sqrt(lam))[:, None]
                   * raw
                   * np.sqrt(lam)[None, :])
    transformed -= epsilon * np.diag(lam)
    return transformed


def record(N: int, epsilon: float, base_projector: np.ndarray | None = None):
    matrix = independent_matrix(N, epsilon)
    values, left, right = eig(
        matrix, left=True, right=True, check_finite=False
    )
    index = int(np.argmax(values.real))
    value = values[index]
    lvec = left[:, index] / np.linalg.norm(left[:, index])
    rvec = right[:, index] / np.linalg.norm(right[:, index])
    pairing = np.vdot(lvec, rvec)
    projector = np.outer(rvec, lvec.conjugate()) / pairing

    larger = independent_matrix(N + 2, epsilon)
    padded = np.zeros(2 * (N + 2) + 1, dtype=np.complex128)
    padded[2:-2] = rvec
    residual = larger @ padded - value * padded
    return {
        "value": value,
        "residual": float(np.linalg.norm(residual)),
        "pairing": float(abs(pairing)),
        "projectorNorm": float(svdvals(projector, check_finite=False)[0]),
        "projectorDifference": (
            0.0 if base_projector is None else float(
                svdvals(projector - base_projector, check_finite=False)[0]
            )
        ),
        "projector": projector,
    }


def main() -> int:
    primary = json.loads(ARGS.primary.read_text(encoding="utf-8"))
    root = Path(__file__).resolve().parents[2]
    producer = root / primary["sourceBinding"]["path"]
    rows = {(int(row["N"]), float(row["epsilon"])): row
            for row in primary["rows"]}

    eigen_errors = []
    residual_errors = []
    pairing_errors = []
    projector_norm_errors = []
    projector_difference_errors = []
    sentinels = []
    for N in primary["parameters"]["cutoffs"]:
        base = record(int(N), 0.0)
        for epsilon in primary["parameters"]["epsilons"]:
            independent = (base if float(epsilon) == 0.0
                           else record(int(N), float(epsilon), base["projector"]))
            expected = rows[(int(N), float(epsilon))]
            eigen_errors.append(abs(
                independent["value"]
                - complex(expected["lambdaReal"], expected["lambdaImag"])
            ))
            residual_errors.append(abs(
                independent["residual"] - float(expected["embeddedResidual"])
            ))
            pairing_errors.append(abs(
                independent["pairing"] - float(expected["leftRightPairingAbs"])
            ))
            projector_norm_errors.append(abs(
                independent["projectorNorm"] - float(expected["projectorNorm"])
            ))
            projector_difference_errors.append(abs(
                independent["projectorDifference"]
                - float(expected["projectorDifferenceFromEpsilonZero"])
            ))
            if int(N) == max(primary["parameters"]["cutoffs"]) and float(epsilon) in (0.01, 0.0001, 1e-7, 1e-8):
                sentinels.append({
                    "N": int(N),
                    "epsilon": float(epsilon),
                    "lambdaReal": float(independent["value"].real),
                    "lambdaImag": float(independent["value"].imag),
                    "projectorNorm": independent["projectorNorm"],
                    "projectorDifference": independent["projectorDifference"],
                })

    boundary = primary["claimBoundary"]
    checks = {
        "producerHashMatches": (
            sha256(producer) == primary["sourceBinding"]["sha256"]
        ),
        "independentEigenvalues": bool(max(eigen_errors) < 2e-12),
        "independentEmbeddedResiduals": bool(max(residual_errors) < 2e-12),
        "independentPairings": bool(max(pairing_errors) < 2e-12),
        "independentProjectorNorms": bool(max(projector_norm_errors) < 2e-11),
        "independentProjectorDifferences": bool(
            max(projector_difference_errors) < 2e-11
        ),
        "claimBoundaryFailClosed": (
            boundary["finiteKineticCompressionComputed"] is True
            and boundary["finiteProjectorNormsComputed"] is True
            and boundary["ordinaryCutoffConvergenceIsContinuumProof"] is False
            and boundary["infiniteDimensionalPersistenceProvedHere"] is False
            and boundary["algebraicSimplicityProvedHere"] is False
            and boundary["complementaryDichotomyProvedHere"] is False
            and boundary["nonautonomousTransferProvedHere"] is False
            and boundary["nonlinearNavierStokesProvedHere"] is False
            and boundary["clayProblemSolved"] is False
        ),
    }
    output = {
        "schemaVersion": "r073d-independent-finite-validation-v1",
        "release": "R0.73D",
        "primary": {
            "path": str(ARGS.primary),
            "sha256": sha256(ARGS.primary),
        },
        "validator": {
            "path": "experiments/r073d/independent_validate.py",
            "sha256": sha256(Path(__file__).resolve()),
            "importsPrimaryProducer": False,
            "matrixConstruction": "explicit W and W'' Fourier coefficients",
        },
        "maximumErrors": {
            "eigenvalueAbsolute": max(eigen_errors),
            "embeddedResidualAbsolute": max(residual_errors),
            "leftRightPairingAbsolute": max(pairing_errors),
            "projectorNormAbsolute": max(projector_norm_errors),
            "projectorDifferenceAbsolute": max(projector_difference_errors),
        },
        "sentinels": sentinels,
        "checks": checks,
        "allChecksPass": bool(all(checks.values())),
        "claimBoundary": {
            "independentFiniteRecomputation": True,
            "continuumTheoremCertifiedByThisValidator": False,
            "rankOneContinuumClusterCertified": False,
            "fastTimeTransferCertified": False,
        },
    }
    ARGS.output.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "event": "independent-validation-complete",
        "allChecksPass": output["allChecksPass"],
        "maximumErrors": output["maximumErrors"],
    }, sort_keys=True))
    return 0 if output["allChecksPass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
