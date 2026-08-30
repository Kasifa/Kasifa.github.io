#!/usr/bin/env python3
"""Independent finite validation for the R0.73G row-leakage diagnostic.

This validator does not import the producer.  It rebuilds the frozen kinetic
matrix from the Orr--Sommerfeld Fourier coefficients and evaluates nonlinear
leakage on an alias-free physical grid followed by FFT and modewise Leray
projection.  All conclusions remain finite binary64 diagnostics only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import time
from typing import Any


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
from scipy.linalg import eig  # noqa: E402


GAMMA = 0.5
MU = 0.25
TOLERANCE = 2.0e-11
START = time.perf_counter()
SEQUENCE = 0
SENTINELS = ((24, 0.01), (24, 0.0001), (96, 0.001), (96, 0.0001), (128, 0.0001))


def emit(event: str, **fields: Any) -> None:
    global SEQUENCE
    SEQUENCE += 1
    print(json.dumps({
        "sequence": SEQUENCE,
        "elapsedSeconds": round(time.perf_counter() - START, 6),
        "event": event,
        **fields,
    }, sort_keys=True), flush=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n"


def matrix_from_os_formula(n_cut: int, epsilon: float) -> np.ndarray:
    modes = np.arange(-n_cut, n_cut + 1, dtype=int)
    lam = modes.astype(float) ** 2 + MU
    shifts = modes[:, None] - modes[None, :]
    w_hat = {1: 0.25j, -1: -0.25j, 2: -0.125j, -2: 0.125j}
    wxx_hat = {1: -0.25j, -1: 0.25j, 2: 0.5j, -2: -0.5j}
    w = np.zeros(shifts.shape, dtype=np.complex128)
    wxx = np.zeros_like(w)
    for shift, value in w_hat.items():
        w[shifts == shift] = value
    for shift, value in wxx_hat.items():
        wxx[shifts == shift] = value
    raw = -1j * GAMMA * (w + wxx / lam[None, :])
    transformed = (
        (1.0 / np.sqrt(lam))[:, None]
        * raw
        * np.sqrt(lam)[None, :]
    )
    transformed -= epsilon * np.diag(lam)
    return transformed


def canonical_top(matrix: np.ndarray) -> tuple[complex, np.ndarray]:
    values, vectors = eig(matrix, left=False, right=True, check_finite=False)
    top_real = float(np.max(values.real))
    candidates = np.flatnonzero(values.real >= top_real - 1.0e-8)
    selected = max(
        (int(index) for index in candidates),
        key=lambda index: (float(values[index].real), float(values[index].imag)),
    )
    vector = np.asarray(vectors[:, selected], dtype=np.complex128)
    vector /= np.linalg.norm(vector)
    anchor = int(np.argmax(np.abs(vector)))
    vector *= np.exp(-1j * np.angle(vector[anchor]))
    if vector[anchor].real < 0.0:
        vector *= -1.0
    return complex(values[selected]), vector


def recover_profile(vector: np.ndarray, modes: np.ndarray) -> np.ndarray:
    return vector / (2.0 * np.sqrt(modes.astype(float) ** 2 + MU))


def physical_cost(profile: np.ndarray, modes: np.ndarray) -> tuple[float, float]:
    velocity_mass = (1.0 + 4.0 * modes.astype(float) ** 2) * np.abs(profile) ** 2
    l2 = math.sqrt(float(np.sum(velocity_mass)))
    h3 = math.sqrt(float(np.sum(
        (2.0 + 4.0 * modes.astype(float) ** 2) ** 3 * velocity_mass
    )))
    return l2, h3 / l2


def velocity_fourier(
    profile: np.ndarray,
    modes: np.ndarray,
    real_pair: bool,
) -> np.ndarray:
    n_cut = int(np.max(np.abs(modes)))
    y_count = 8 * n_cut + 8
    z_count = 8
    coefficients = np.zeros((3, y_count, z_count), dtype=np.complex128)
    for value, n_mode in zip(profile, modes):
        ky = 2 * int(n_mode)
        vector = np.asarray([0.0j, value, -2.0 * int(n_mode) * value])
        coefficients[:, ky % y_count, 1] += vector
        if real_pair:
            coefficients[:, (-ky) % y_count, -1 % z_count] += np.conjugate(vector)
    return coefficients


def projected_leakage_fft(coefficients: np.ndarray, target_kz: int) -> dict[str, float]:
    _, y_count, z_count = coefficients.shape
    normalization = y_count * z_count
    ky = np.fft.fftfreq(y_count, d=1.0 / y_count)
    kz = np.fft.fftfreq(z_count, d=1.0 / z_count)
    field = np.fft.ifftn(coefficients * normalization, axes=(1, 2))
    derivative_y = np.fft.ifftn(
        1j * ky[None, :, None] * coefficients * normalization,
        axes=(1, 2),
    )
    derivative_z = np.fft.ifftn(
        1j * kz[None, None, :] * coefficients * normalization,
        axes=(1, 2),
    )
    nonlinear = field[1][None, :, :] * derivative_y + field[2][None, :, :] * derivative_z
    nonlinear_hat = np.fft.fftn(nonlinear, axes=(1, 2)) / normalization

    indices = np.flatnonzero(kz == target_kz)
    if len(indices) != 1:
        raise RuntimeError("target Kz is absent from the validation grid")
    z_index = int(indices[0])
    projected_squared = 0.0
    divergence_defect = 0.0
    for y_index, ky_value in enumerate(ky):
        wave = np.asarray([0.0, ky_value, float(target_kz)])
        vector = nonlinear_hat[:, y_index, z_index]
        wave_squared = float(np.dot(wave, wave))
        if wave_squared > 0.0:
            vector = vector - wave * (np.dot(wave, vector) / wave_squared)
            divergence_defect = max(divergence_defect, abs(np.dot(wave, vector)))
        projected_squared += float(np.vdot(vector, vector).real)
    return {
        "projectedL2": math.sqrt(max(0.0, projected_squared)),
        "postProjectionDivergenceMaximum": float(divergence_defect),
        "physicalYGridCount": y_count,
        "physicalZGridCount": z_count,
        "aliasFreeForQuadraticSupport": True,
    }


def scaled_error(left: complex | float, right: complex | float) -> float:
    return float(abs(left - right) / max(1.0, abs(left), abs(right)))


def main() -> int:
    primary_path = ARGS.primary.resolve()
    primary = json.loads(primary_path.read_text(encoding="utf-8"))
    primary_rows = {
        (int(row["N"]), float(row["epsilon"])): row
        for row in primary["rows"]
    }
    emit("start", sentinelCount=len(SENTINELS), diagnosticOnly=True)
    validations = []
    for index, (n_cut, epsilon) in enumerate(SENTINELS, start=1):
        emit("sentinel_start", index=index, N=n_cut, epsilon=epsilon)
        expected = primary_rows[(n_cut, epsilon)]
        matrix = matrix_from_os_formula(n_cut, epsilon)
        eigenvalue, vector = canonical_top(matrix)
        modes = np.arange(-n_cut, n_cut + 1, dtype=int)
        profile = recover_profile(vector, modes)
        physical_l2, h3_cost = physical_cost(profile, modes)
        kz2 = projected_leakage_fft(velocity_fourier(profile, modes, False), 2)
        kz0 = projected_leakage_fft(velocity_fourier(profile, modes, True), 0)
        errors = {
            "topEigenvalue": scaled_error(
                eigenvalue,
                complex(
                    float(expected["topEigenvalueFastReal"]),
                    float(expected["topEigenvalueFastImag"]),
                ),
            ),
            "physicalL2": scaled_error(physical_l2, float(expected["physicalPositiveRowL2"])),
            "physicalH3ToL2Cost": scaled_error(
                h3_cost, float(expected["physicalH3ToL2Cost"])
            ),
            "kz2Leakage": scaled_error(
                kz2["projectedL2"],
                float(expected["kz2ProjectedLeakagePositiveUnitRowKernelA"]),
            ),
            "kz0Leakage": scaled_error(
                kz0["projectedL2"],
                float(expected["kz0ProjectedLeakageUnscaledRealPairKernelA"]),
            ),
        }
        passed = max(errors.values()) <= TOLERANCE
        validations.append({
            "N": n_cut,
            "epsilon": epsilon,
            "absoluteLambda": 1.0 / epsilon,
            "independent": {
                "topEigenvalueFastReal": float(eigenvalue.real),
                "topEigenvalueFastImag": float(eigenvalue.imag),
                "physicalPositiveRowL2": physical_l2,
                "physicalH3ToL2Cost": h3_cost,
                "kz2ProjectedLeakagePositiveUnitRow": kz2["projectedL2"],
                "kz0ProjectedLeakageUnscaledRealPair": kz0["projectedL2"],
                "kz2PostProjectionDivergenceMaximum": kz2["postProjectionDivergenceMaximum"],
                "kz0PostProjectionDivergenceMaximum": kz0["postProjectionDivergenceMaximum"],
                "physicalYGridCount": kz2["physicalYGridCount"],
                "physicalZGridCount": kz2["physicalZGridCount"],
            },
            "scaleOneErrors": errors,
            "maximumScaleOneError": max(errors.values()),
            "pass": passed,
        })
        emit(
            "sentinel_complete",
            index=index,
            N=n_cut,
            epsilon=epsilon,
            maximumScaleOneError=max(errors.values()),
            passCheck=passed,
        )

    result = {
        "schemaVersion": "r073g-independent-validation-v1",
        "release": "R0.73G",
        "evidenceClass": "independent-finite-binary64-diagnostic-only",
        "diagnosticOnly": True,
        "primaryBinding": {
            "path": str(primary_path.relative_to(primary_path.parents[2])),
            "bytes": primary_path.stat().st_size,
            "sha256": sha256(primary_path),
        },
        "validatorSource": {
            "path": str(Path(__file__).resolve().relative_to(primary_path.parents[2])),
            "sha256": sha256(Path(__file__).resolve()),
        },
        "methods": {
            "matrix": "direct Orr--Sommerfeld Fourier coefficients; producer not imported",
            "leakage": "alias-free physical grid, FFT, and independent modewise Leray projection",
            "tolerance": TOLERANCE,
        },
        "validations": validations,
        "maximumScaleOneError": max(row["maximumScaleOneError"] for row in validations),
        "allChecksPass": all(row["pass"] for row in validations),
        "claimBoundary": primary["claimBoundary"],
    }
    temporary = ARGS.output.with_name(f".{ARGS.output.name}.tmp")
    temporary.write_text(canonical(result), encoding="utf-8")
    os.replace(temporary, ARGS.output)
    emit(
        "complete",
        allChecksPass=result["allChecksPass"],
        maximumScaleOneError=result["maximumScaleOneError"],
    )
    return 0 if result["allChecksPass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
