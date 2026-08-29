#!/usr/bin/env python3
"""Independent finite recomputation of the exploratory R0.73E diagnostic.

This validator does not import the primary producer.  It builds the matrix
from the explicit Fourier coefficients of W and W'', obtains the selected
Riesz projectors by contour quadrature, and recomputes the reported finite
resolvent and semigroup sentinels.  Agreement is not a continuum proof.
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
from scipy.linalg import eig, expm, orth, svdvals  # noqa: E402


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def matrix_from_fourier_coefficients(N: int, epsilon: float) -> np.ndarray:
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
    transformed = (
        (1.0 / np.sqrt(lam))[:, None]
        * raw
        * np.sqrt(lam)[None, :]
    )
    transformed -= epsilon * np.diag(lam)
    return transformed


def opnorm(matrix: np.ndarray) -> float:
    return float(svdvals(matrix, check_finite=False)[0])


def contour_projector(
    matrix: np.ndarray, center: complex, radius: float, nodes: int = 64
) -> np.ndarray:
    identity = np.eye(matrix.shape[0], dtype=np.complex128)
    projector = np.zeros_like(matrix)
    for index in range(nodes):
        theta = 2.0 * np.pi * index / nodes
        phase = np.exp(1j * theta)
        z = center + radius * phase
        projector += (
            radius * phase / nodes
            * np.linalg.solve(z * identity - matrix, identity)
        )
    return projector


def split_by_contour(matrix: np.ndarray) -> dict[str, object]:
    values = eig(matrix, right=False, check_finite=False)
    index = int(np.argmax(values.real))
    value = values[index]
    remainder = np.delete(values, index)
    gap = float(np.min(np.abs(remainder - value)))
    radius = min(0.05, 0.3 * gap)
    projector = contour_projector(matrix, value, radius)
    complement = np.eye(matrix.shape[0], dtype=np.complex128) - projector
    basis = orth(complement, rcond=1e-11)
    if basis.shape[1] != matrix.shape[0] - 1:
        raise RuntimeError("contour complement did not have codimension one")
    restricted = basis.conjugate().T @ matrix @ basis
    q_values = eig(restricted, right=False, check_finite=False)
    return {
        "value": value,
        "radius": radius,
        "P": projector,
        "Q": complement,
        "Z": basis,
        "Bq": restricted,
        "qAlpha": float(np.max(q_values.real)),
        "projectorIdempotence": opnorm(projector @ projector - projector),
        "projectorCommutator": opnorm(matrix @ projector - projector @ matrix),
    }


def relative_error(actual: float, expected: float) -> float:
    return abs(actual - expected) / max(abs(expected), np.finfo(float).tiny)


def main() -> int:
    primary = json.loads(ARGS.primary.read_text(encoding="utf-8"))
    root = Path(__file__).resolve().parents[2]
    producer = root / primary["sourceBinding"]["path"]
    base_splits: dict[int, dict[str, object]] = {}
    validations = []
    maximums = {
        "clusterEigenvalueAbsolute": 0.0,
        "qSpectralAbscissaAbsolute": 0.0,
        "projectorDifferenceAbsolute": 0.0,
        "resolventPeakRelative": 0.0,
        "semigroupEndpointRelative": 0.0,
        "semigroupNormalizedPeakRelative": 0.0,
        "movingEndpointRelative": 0.0,
        "fixedEndpointRelative": 0.0,
        "fixedMovingDifferenceEndpointRelative": 0.0,
        "contourProjectorIdempotence": 0.0,
        "contourProjectorCommutator": 0.0,
    }

    for row in primary["rows"]:
        N = int(row["N"])
        epsilon = float(row["epsilon"])
        if N not in base_splits:
            base_splits[N] = split_by_contour(
                matrix_from_fourier_coefficients(N, 0.0)
            )
        base = base_splits[N]
        matrix = matrix_from_fourier_coefficients(N, epsilon)
        split = split_by_contour(matrix)
        projector_difference = opnorm(split["P"] - base["P"])
        expected_value = complex(
            row["clusterEigenvalue"]["real"],
            row["clusterEigenvalue"]["imag"],
        )

        eigen_error = abs(split["value"] - expected_value)
        q_alpha_error = abs(
            split["qAlpha"] - row["qSpectrum"]["spectralAbscissa"]
        )
        projector_error = abs(
            projector_difference
            - row["movingVsFixed"]["projectorDifferenceNorm"]
        )
        maximums["clusterEigenvalueAbsolute"] = max(
            maximums["clusterEigenvalueAbsolute"], eigen_error
        )
        maximums["qSpectralAbscissaAbsolute"] = max(
            maximums["qSpectralAbscissaAbsolute"], q_alpha_error
        )
        maximums["projectorDifferenceAbsolute"] = max(
            maximums["projectorDifferenceAbsolute"], projector_error
        )
        maximums["contourProjectorIdempotence"] = max(
            maximums["contourProjectorIdempotence"],
            split["projectorIdempotence"],
        )
        maximums["contourProjectorCommutator"] = max(
            maximums["contourProjectorCommutator"],
            split["projectorCommutator"],
        )

        identity_q = np.eye(split["Bq"].shape[0], dtype=np.complex128)
        resolvent_errors = []
        for expected in row["resolventVerticalLines"]:
            z = (
                float(expected["lineRealPart"])
                + 1j * float(expected["peakImaginaryAbs"])
            )
            # Independent evaluation: form the inverse and take its norm,
            # rather than taking the reciprocal of sigma_min(zI-Bq).
            inverse = np.linalg.inv(z * identity_q - split["Bq"])
            actual = opnorm(inverse)
            error = relative_error(
                actual, float(expected["resolventNormMaximum"])
            )
            resolvent_errors.append(error)
            maximums["resolventPeakRelative"] = max(
                maximums["resolventPeakRelative"], error
            )

        semigroup_expected = row["semigroup"]
        endpoint = float(semigroup_expected["timeGrid"]["maximum"])
        peak_time = float(
            semigroup_expected["intrinsicMovingQ"]
            ["spectralAbscissaNormalizedPeakTime"]
        )
        endpoint_q = expm(endpoint * split["Bq"])
        endpoint_q_norm = opnorm(endpoint_q)
        peak_q = expm(peak_time * split["Bq"])
        normalized_peak = (
            opnorm(peak_q) * math_exp(-split["qAlpha"] * peak_time)
        )
        full_endpoint = (
            np.exp(endpoint * split["value"]) * split["P"]
            + split["Z"] @ endpoint_q @ split["Z"].conjugate().T @ split["Q"]
        )
        moving_endpoint = opnorm(
            split["Z"] @ endpoint_q @ split["Z"].conjugate().T @ split["Q"]
        )
        fixed_endpoint = opnorm(full_endpoint @ base["Q"])
        difference_endpoint = opnorm(full_endpoint @ (base["Q"] - split["Q"]))

        semigroup_errors = {
            "intrinsicEndpointRelative": relative_error(
                endpoint_q_norm,
                semigroup_expected["intrinsicMovingQ"]["endpointNorm"],
            ),
            "normalizedPeakRelative": relative_error(
                normalized_peak,
                semigroup_expected["intrinsicMovingQ"]
                ["spectralAbscissaNormalizedPeak"],
            ),
            "movingEndpointRelative": relative_error(
                moving_endpoint,
                semigroup_expected["ambientMovingQ"]["endpointNorm"],
            ),
            "fixedEndpointRelative": relative_error(
                fixed_endpoint,
                semigroup_expected["ambientFixedQ0"]["endpointNorm"],
            ),
            "differenceEndpointRelative": relative_error(
                difference_endpoint,
                semigroup_expected["fixedMovingDifference"]["endpointNorm"],
            ),
        }
        for target, key in (
            ("semigroupEndpointRelative", "intrinsicEndpointRelative"),
            ("semigroupNormalizedPeakRelative", "normalizedPeakRelative"),
            ("movingEndpointRelative", "movingEndpointRelative"),
            ("fixedEndpointRelative", "fixedEndpointRelative"),
            (
                "fixedMovingDifferenceEndpointRelative",
                "differenceEndpointRelative",
            ),
        ):
            maximums[target] = max(maximums[target], semigroup_errors[key])

        validations.append({
            "N": N,
            "epsilon": epsilon,
            "contourRadius": split["radius"],
            "clusterEigenvalueAbsoluteError": eigen_error,
            "qSpectralAbscissaAbsoluteError": q_alpha_error,
            "projectorDifferenceAbsoluteError": projector_error,
            "resolventPeakRelativeErrors": resolvent_errors,
            "semigroupRelativeErrors": semigroup_errors,
        })

    boundary = primary["claimBoundary"]
    checks = {
        "producerHashMatches": (
            sha256(producer) == primary["sourceBinding"]["sha256"]
        ),
        "independentMatrixClusterEigenvalues": (
            maximums["clusterEigenvalueAbsolute"] < 3e-12
        ),
        "independentContourComplementSpectralAbscissae": (
            maximums["qSpectralAbscissaAbsolute"] < 3e-11
        ),
        "independentContourProjectorDifferences": (
            maximums["projectorDifferenceAbsolute"] < 3e-10
        ),
        "independentInverseResolventPeaks": (
            maximums["resolventPeakRelative"] < 3e-9
        ),
        "independentSemigroupSentinels": max(
            maximums["semigroupEndpointRelative"],
            maximums["semigroupNormalizedPeakRelative"],
            maximums["movingEndpointRelative"],
            maximums["fixedEndpointRelative"],
            maximums["fixedMovingDifferenceEndpointRelative"],
        ) < 3e-9,
        "contourProjectorsNumericallyAlgebraic": max(
            maximums["contourProjectorIdempotence"],
            maximums["contourProjectorCommutator"],
        ) < 3e-10,
        "claimBoundaryFailClosed": (
            boundary["finiteBinary64Diagnostic"] is True
            and boundary["ordinaryCutoffAgreementIsContinuumProof"] is False
            and boundary["additionalContinuumEigenpairProvedHere"] is False
            and boundary["continuumComplementaryDichotomyProvedHere"] is False
            and boundary["continuousTimeSemigroupBoundProvedHere"] is False
            and boundary["movingProfileUniformityProvedHere"] is False
            and boundary["nonautonomousTransferProvedHere"] is False
            and boundary["nonlinearNavierStokesProvedHere"] is False
            and boundary["clayProblemSolved"] is False
        ),
    }
    checks = {key: bool(value) for key, value in checks.items()}
    output = {
        "schemaVersion": "r073e-independent-finite-validation-v1",
        "release": "R0.73E-exploratory",
        "primary": {
            "path": str(ARGS.primary),
            "sha256": sha256(ARGS.primary),
        },
        "validator": {
            "path": "experiments/r073e/independent_validate.py",
            "sha256": sha256(Path(__file__).resolve()),
            "importsPrimaryProducer": False,
            "matrixConstruction": "explicit W and W'' Fourier coefficients",
            "projectorConstruction": "64-node Riesz contour quadrature",
            "resolventConstruction": "explicit inverse followed by 2-norm",
        },
        "maximumErrors": maximums,
        "rows": validations,
        "checks": checks,
        "allChecksPass": bool(all(checks.values())),
        "claimBoundary": {
            "independentFiniteRecomputation": True,
            "intervalArithmetic": False,
            "continuumDichotomyCertified": False,
            "continuousTimeBoundCertified": False,
        },
    }
    ARGS.output.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "event": "independent-validation-complete",
        "allChecksPass": output["allChecksPass"],
        "maximumErrors": maximums,
    }, sort_keys=True))
    return 0 if output["allChecksPass"] else 2


def math_exp(value: float) -> float:
    # Kept outside the main loop so the validator's exponential scalar path
    # is explicit and independent of the producer's helper functions.
    return float(np.exp(value))


if __name__ == "__main__":
    raise SystemExit(main())
