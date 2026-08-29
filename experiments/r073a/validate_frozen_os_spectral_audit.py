#!/usr/bin/env python3
"""Independent fail-closed checks for the finite R0.73A spectral audit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--directory", type=Path,
                        default=Path(__file__).resolve().parent)
    return parser.parse_args()


ARGS = parse_args()
if ARGS.deps:
    sys.path.insert(0, ARGS.deps)

import numpy as np  # noqa: E402
from scipy.linalg import eigvals, eigvalsh, null_space  # noqa: E402


DIRECTORY = ARGS.directory.resolve()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sine_vector(N: int, harmonic: int, amplitude: float = 1.0) -> np.ndarray:
    vector = np.zeros(2 * N + 1, dtype=np.complex128)
    vector[N + harmonic] = amplitude / (2j)
    vector[N - harmonic] = -amplitude / (2j)
    return vector


def alternate_generator(N: int, d: float, beta: float, mu: float,
                        c: float) -> np.ndarray:
    modes = np.arange(-N, N + 1)
    lam = (modes + beta) ** 2 + mu
    shifts = modes[:, None] - modes[None, :]
    w = np.zeros_like(shifts, dtype=np.complex128)
    wxx = np.zeros_like(shifts, dtype=np.complex128)
    coefficients = {
        1: (0.25j * np.exp(-d), -0.25j * np.exp(-d)),
        -1: (-0.25j * np.exp(-d), 0.25j * np.exp(-d)),
        2: (-0.125j * np.exp(-4*d), 0.5j * np.exp(-4*d)),
        -2: (0.125j * np.exp(-4*d), -0.5j * np.exp(-4*d)),
    }
    for shift, (w_value, wxx_value) in coefficients.items():
        w[shifts == shift] = w_value
        wxx[shifts == shift] = wxx_value
    matrix = -np.diag(lam.astype(float)) - 1j * c * w
    matrix += -1j * c * wxx / lam[None, :]
    return matrix


def independent_basis(N: int, d: float, projection: str) -> np.ndarray:
    if projection == "unprojected":
        return np.eye(2 * N + 1, dtype=np.complex128)
    if projection == "qstar-Wxx":
        constraints = (0.5 * np.exp(-d) * sine_vector(N, 1)
                       - np.exp(-4*d) * sine_vector(N, 2))[:, None]
    elif projection == "span-sin1-sin2":
        constraints = np.column_stack((sine_vector(N, 1), sine_vector(N, 2)))
    else:
        raise ValueError(projection)
    return null_space(constraints.conj().T)


def exact_tangent_residual(N: int, d: float, c: float) -> float:
    modes = np.arange(-N, N + 1)
    qstar = 0.5 * np.exp(-d) * sine_vector(N, 1) - np.exp(-4*d) * sine_vector(N, 2)
    w = -0.5 * np.exp(-d) * sine_vector(N, 1) + 0.25 * np.exp(-4*d) * sine_vector(N, 2)
    lam = modes.astype(float) ** 2
    inverse_q = np.zeros_like(qstar)
    nonzero = lam > 0
    inverse_q[nonzero] = qstar[nonzero] / lam[nonzero]
    def convolution(left: np.ndarray, right: np.ndarray) -> np.ndarray:
        result = np.zeros_like(left)
        for row, m in enumerate(modes):
            for col, n in enumerate(modes):
                shift = m - n
                if -N <= shift <= N:
                    result[row] += left[shift + N] * right[col]
        return result
    pressure_cancel = convolution(w, qstar) + convolution(qstar, inverse_q)
    action = -lam * qstar - 1j * c * pressure_cancel
    expected = -lam * qstar
    return float(np.linalg.norm(action - expected) / max(1.0, np.linalg.norm(expected)))


def main() -> int:
    manifest = json.loads((DIRECTORY / "manifest.json").read_text())
    summary = json.loads((DIRECTORY / "summary.json").read_text())
    with (DIRECTORY / "all_rows.csv").open(encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    checks: dict[str, bool] = {}
    checks["manifestScope"] = (manifest["finiteDimensionalOnly"] is True
                               and len(manifest["limitations"]) == 5)
    checks["sourceHash"] = (
        manifest["sourceSha256"] == sha256(DIRECTORY / manifest["source"]))
    checks["manifestHashes"] = all(
        (DIRECTORY / record["path"]).stat().st_size == record["bytes"]
        and sha256(DIRECTORY / record["path"]) == record["sha256"]
        for record in manifest["outputs"])
    checks["rowCounts"] = (len(rows) == 1494 and summary["broadRows"] == 1344
                           and summary["targetRows"] == 150)
    checks["coverage"] = (
        {float(row["d"]) for row in rows if row["tier"] == "broad"}
        == {0.0, 0.05, 0.25, 1.0}
        and {float(row["beta"]) for row in rows if row["tier"] == "broad"}
        == {0.0, 1e-4, 1e-3, 1e-2, 0.05, 0.25, 0.49}
        and {float(row["mu"]) for row in rows if row["tier"] == "broad"}
        == {1e-6, 1e-4, 1e-2, 1e-1}
        and {float(row["c"]) for row in rows if row["tier"] == "broad"}
        == {4.0, 128.0, 4096.0, 131072.0}
        and {int(row["N"]) for row in rows if row["tier"] == "target"}
        == {12, 18, 24, 32, 40})
    checks["noNaNOrInfinity"] = summary["allRecordedNumbersFinite"] is True
    checks["exactTangentResidual"] = exact_tangent_residual(8, 0.37, 131072.0) < 1e-12

    indexed = {(row["caseId"], row["projection"], int(row["N"])): row
               for row in rows if row["tier"] == "target"}
    spots = [
        ("T01-lowest-gap-c4", "unprojected", 12),
        ("T03-near-bloch-c4096", "span-sin1-sin2", 18),
        ("T09-collision-alpha025", "qstar-Wxx", 24),
        ("T10-collision-alpha0125", "span-sin1-sin2", 40),
    ]
    spot_errors = []
    for case_id, projection, N in spots:
        row = indexed[(case_id, projection, N)]
        matrix = alternate_generator(N, *(float(row[key]) for key in ("d", "beta", "mu", "c")))
        basis = independent_basis(N, float(row["d"]), projection)
        compressed = basis.conj().T @ matrix @ basis
        spectral = float(np.max(eigvals(compressed).real))
        numerical = float(eigvalsh((compressed + compressed.conj().T) / 2)[-1])
        spot_errors.append(max(abs(spectral - float(row["spectralAbscissa"])),
                               abs(numerical - float(row["numericalAbscissa"]))))
    checks["independentMatrixSpots"] = max(spot_errors) < 2e-7

    convergence_ok = True
    for case_id in {row["caseId"] for row in rows if row["tier"] == "target"}:
        for projection in ("unprojected", "qstar-Wxx", "span-sin1-sin2"):
            a = indexed[(case_id, projection, 32)]
            b = indexed[(case_id, projection, 40)]
            spectral_relative = abs(float(a["spectralAbscissa"])
                                    - float(b["spectralAbscissa"])) / max(
                                        1.0, abs(float(b["spectralAbscissa"])))
            gain_difference = abs(float(a["sampledLog10TransientGain"])
                                  - float(b["sampledLog10TransientGain"]))
            convergence_ok &= spectral_relative < 3e-3 and gain_difference < 1e-4
    checks["targetSpectralAndGainConvergence"] = convergence_ok
    checks["pseudospectrumExplicitlySampled"] = all(
        float(row["epsilonRelative"]) == 1e-2
        for row in rows if row["tier"] == "target")
    checks["projectionIsCompressionNotInvariantClaim"] = (
        "not proved invariant quotients" in " ".join(manifest["limitations"]))
    checks["unprojectedTargetSpectralInstabilityScreen"] = all(
        float(row["spectralAbscissa"]) > 0
        for row in rows if row["tier"] == "target"
        and row["projection"] == "unprojected")
    checks["spanProjectionDoesNotUniformlyStabilize"] = any(
        float(row["spectralAbscissa"]) > 1
        for row in rows if row["tier"] == "target"
        and row["projection"] == "span-sin1-sin2" and row["N"] == "40")
    require(all(checks.values()),
            "validation failure: " + ", ".join(key for key, ok in checks.items() if not ok))
    result = {
        "schemaVersion": 1,
        "status": "passed",
        "checks": checks,
        "maximumIndependentSpotError": max(spot_errors),
        "claimBoundary": {
            "finiteDimensionalFrozenAudit": True,
            "infiniteDimensionalSpectrumProved": False,
            "continuousTimeMaximumTransientGainProved": False,
            "GalerkinTailBoundProved": False,
            "nonautonomousPropagatorProved": False,
        },
    }
    (DIRECTORY / "validation.json").write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
