#!/usr/bin/env python3
"""Finite R0.73G top-profile and quadratic row-leakage diagnostic.

The frozen matrix is the R0.73F kinetic-space Fourier compression at d=0,
gamma=1/2, beta=xi=0 and epsilon=1/|Lambda|.  Each selected finite top
eigenvector is reconstructed as a physical Kz=1 velocity row.  Two independent
Fourier kernels then evaluate its Leray-projected Kz=2 self-interaction and the
Kz=0 interaction with the conjugate row.

Every result is a binary64 finite-compression diagnostic only.  Cutoff
agreement is not a Galerkin tail bound, and no output proves a continuum
spectral, nonlinear-instability, transition-threshold, or regularity claim.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import Any, Iterable, Mapping


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = Path(__file__).resolve()
GAMMA = 0.5
MU = 0.25
TOP_REAL_TOLERANCE = 1.0e-8
KERNEL_SCALE_ONE_TOLERANCE = 5.0e-12
DISPLAY_FLOOR = 1.0e-18
DEFAULT_EPSILONS = "0.01,0.005,0.002,0.001,0.0005,0.0002,0.0001"
DEFAULT_CUTOFFS = "24,48,96,128"
SCHEMA_VERSION = "r073g-nonlinear-row-leakage-v1"
EVIDENCE_CLASS = "finite-binary64-diagnostic-only"
OUTPUT_NAMES = (
    "nonlinear_row_leakage_rows.csv",
    "nonlinear_row_leakage_convergence.csv",
    "nonlinear_row_leakage_summary.json",
    "fig-r073g-nonlinear-row-leakage.pdf",
    "fig-r073g-nonlinear-row-leakage.svg",
    "fig-r073g-nonlinear-row-leakage.png",
)
ROW_FIELDS = (
    "schemaVersion",
    "evidenceClass",
    "diagnosticOnly",
    "N",
    "dimension",
    "epsilon",
    "absoluteLambda",
    "topEigenvalueFastReal",
    "topEigenvalueFastImag",
    "topPhysicalGrowthRateReal",
    "topClusterDimensionAtRealTolerance",
    "topRealGapBelowCluster",
    "topEigenResidualRelative",
    "physicalPositiveRowL2",
    "physicalPositiveRowH3",
    "physicalH3ToL2Cost",
    "kineticBoundaryMassFraction",
    "kineticOuterThreeMassFraction",
    "h3OuterThreeContributionFraction",
    "kz2ProjectedLeakagePositiveUnitRowKernelA",
    "kz2ProjectedLeakagePositiveUnitRowKernelB",
    "kz2ProjectedLeakageUnitRealPairKernelA",
    "kz0ProjectedLeakageUnscaledRealPairKernelA",
    "kz0ProjectedLeakageUnscaledRealPairKernelB",
    "kz0ProjectedLeakageUnitRealPairKernelA",
    "kz2KernelScaleOneDifference",
    "kz0KernelScaleOneDifference",
    "maximumKernelCoefficientScaleOneDifference",
    "kernelCheckPass",
)
CONVERGENCE_FIELDS = (
    "schemaVersion",
    "evidenceClass",
    "diagnosticOnly",
    "epsilon",
    "absoluteLambda",
    "coarseN",
    "fineN",
    "topEigenvalueRelativeChange",
    "physicalH3ToL2RelativeChange",
    "kz2LeakageRelativeChange",
    "kz0LeakageRelativeChange",
    "maximumRelativeChange",
    "ordinaryCutoffAgreementIsTailBound",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--deps",
        default="",
        help="optional directory containing NumPy, SciPy and Matplotlib",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=HERE,
        help="formal output directory; defaults to this experiment directory",
    )
    parser.add_argument("--epsilons", default=DEFAULT_EPSILONS)
    parser.add_argument("--cutoffs", default=DEFAULT_CUTOFFS)
    parser.add_argument("--png-dpi", type=int, default=600)
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="use a tiny grid and permit an uncommitted source for pre-commit QA",
    )
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


ARGS = parse_args()
if ARGS.deps:
    sys.path.insert(0, ARGS.deps)

import numpy as np  # noqa: E402
import scipy  # noqa: E402
from scipy.linalg import eig  # noqa: E402


START = time.perf_counter()
SEQUENCE = 0


def emit(event: str, **fields: Any) -> None:
    """Print one machine-readable progress line without changing result files."""
    global SEQUENCE
    SEQUENCE += 1
    record = {
        "sequence": SEQUENCE,
        "elapsedSeconds": round(time.perf_counter() - START, 6),
        "event": event,
        **fields,
    }
    print(json.dumps(record, sort_keys=True), flush=True)


def canonical_json(value: object) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        indent=2,
        ensure_ascii=True,
        allow_nan=False,
    ) + "\n"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def binding(path: Path, base: Path) -> dict[str, object]:
    return {
        "path": str(path.resolve().relative_to(base.resolve())),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def atomic_text(path: Path, text: str) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, path)


def parse_positive_floats(text: str) -> list[float]:
    values = sorted({float(part.strip()) for part in text.split(",")}, reverse=True)
    if not values or any(not math.isfinite(value) or value <= 0.0 for value in values):
        raise ValueError("epsilons must be finite positive numbers")
    return values


def parse_positive_ints(text: str) -> list[int]:
    values = sorted({int(part.strip()) for part in text.split(",")})
    if not values or any(value < 3 for value in values):
        raise ValueError("cutoffs must be integers at least 3")
    return values


def git_source_provenance(smoke: bool) -> dict[str, object]:
    relative = SOURCE.relative_to(ROOT)
    head = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    committed = subprocess.run(
        ["git", "-C", str(ROOT), "show", f"HEAD:{relative.as_posix()}"],
        check=False,
        capture_output=True,
    )
    source_at_head = committed.returncode == 0
    working_bytes = SOURCE.read_bytes()
    matches = source_at_head and committed.stdout == working_bytes
    if not smoke and not matches:
        raise RuntimeError(
            "formal run refused: commit this exact diagnostic source before running"
        )
    return {
        "sourceCommit": head,
        "sourcePath": relative.as_posix(),
        "workingSourceSha256": sha256_bytes(working_bytes),
        "sourcePresentAtHead": source_at_head,
        "workingSourceMatchesHead": matches,
        "sourceBeforeRunGateEnforced": not smoke,
    }


def frozen_kinetic_matrix(n_cut: int, epsilon: float) -> np.ndarray:
    """Exact R0.73F finite matrix_recurrence at d=0 and sign +1."""
    raw = np.zeros((2 * n_cut + 1, 2 * n_cut + 1), dtype=np.complex128)
    for column, n_mode in enumerate(range(-n_cut, n_cut + 1)):
        lam = n_mode * n_mode + MU
        first = GAMMA * 0.25 * (1.0 - 1.0 / lam)
        second = GAMMA * (-0.125 + 0.5 / lam)
        for shift, value in (
            (1, first),
            (-1, -first),
            (2, second),
            (-2, -second),
        ):
            m_mode = n_mode + shift
            if -n_cut <= m_mode <= n_cut:
                raw[m_mode + n_cut, column] = value

    modes = np.arange(-n_cut, n_cut + 1, dtype=float)
    lam = modes * modes + MU
    transformed = (
        (1.0 / np.sqrt(lam))[:, None]
        * raw
        * np.sqrt(lam)[None, :]
    )
    transformed -= epsilon * np.diag(lam)
    return transformed


def canonicalize_vector(vector: np.ndarray) -> np.ndarray:
    vector = np.asarray(vector, dtype=np.complex128).copy()
    norm = float(np.linalg.norm(vector))
    if not math.isfinite(norm) or norm <= 0.0:
        raise RuntimeError("top eigenvector has invalid norm")
    vector /= norm
    anchor = int(np.argmax(np.abs(vector)))
    if abs(vector[anchor]) > 0.0:
        vector *= np.exp(-1j * np.angle(vector[anchor]))
    if vector[anchor].real < 0.0:
        vector *= -1.0
    return vector


def select_top_profile(
    matrix: np.ndarray,
    real_tolerance: float = TOP_REAL_TOLERANCE,
) -> tuple[complex, np.ndarray, dict[str, float | int]]:
    values, vectors = eig(matrix, left=False, right=True, check_finite=False)
    top_real = float(np.max(values.real))
    top_indices = np.flatnonzero(values.real >= top_real - real_tolerance)
    selected = max(
        (int(index) for index in top_indices),
        key=lambda index: (float(values[index].real), float(values[index].imag)),
    )
    eigenvalue = complex(values[selected])
    vector = canonicalize_vector(vectors[:, selected])
    matrix_scale = max(1.0, float(np.linalg.norm(matrix)), abs(eigenvalue))
    residual = float(np.linalg.norm(matrix @ vector - eigenvalue * vector) / matrix_scale)
    complement = np.delete(values, top_indices)
    gap = (
        top_real - float(np.max(complement.real))
        if len(complement)
        else math.inf
    )
    return eigenvalue, vector, {
        "topClusterDimension": int(len(top_indices)),
        "topRealGapBelowCluster": float(gap),
        "topEigenResidualRelative": residual,
    }


def recover_physical_profile(
    kinetic_vector: np.ndarray,
    modes: np.ndarray,
) -> np.ndarray:
    """Recover v from the unitary coordinate y=2 L^(1/2) v."""
    lam = modes.astype(float) ** 2 + MU
    return kinetic_vector / (2.0 * np.sqrt(lam))


def physical_costs(
    profile: np.ndarray,
    kinetic_vector: np.ndarray,
    modes: np.ndarray,
) -> dict[str, float]:
    physical_wave_number_squared = 4.0 * modes.astype(float) ** 2 + 1.0
    velocity_mass = (1.0 + 4.0 * modes.astype(float) ** 2) * np.abs(profile) ** 2
    l2_squared = float(np.sum(velocity_mass))
    h3_weights = (1.0 + physical_wave_number_squared) ** 3
    h3_contributions = h3_weights * velocity_mass
    h3_squared = float(np.sum(h3_contributions))
    outer_three = np.abs(modes) >= int(np.max(np.abs(modes))) - 2
    kinetic_mass = np.abs(kinetic_vector) ** 2
    boundary = np.abs(modes) == int(np.max(np.abs(modes)))
    return {
        "physicalPositiveRowL2": math.sqrt(l2_squared),
        "physicalPositiveRowH3": math.sqrt(h3_squared),
        "physicalH3ToL2Cost": math.sqrt(h3_squared / l2_squared),
        "kineticBoundaryMassFraction": float(np.sum(kinetic_mass[boundary])),
        "kineticOuterThreeMassFraction": float(np.sum(kinetic_mass[outer_three])),
        "h3OuterThreeContributionFraction": (
            float(np.sum(h3_contributions[outer_three]) / h3_squared)
            if h3_squared > 0.0
            else 0.0
        ),
    }


WaveKey = tuple[int, int, int]
CoefficientMap = dict[WaveKey, np.ndarray]


def leray_project(wave: WaveKey, vector: np.ndarray) -> np.ndarray:
    k_vector = np.asarray(wave, dtype=float)
    k_squared = float(np.dot(k_vector, k_vector))
    if k_squared == 0.0:
        return np.asarray(vector, dtype=np.complex128)
    return np.asarray(vector, dtype=np.complex128) - (
        k_vector * (np.dot(k_vector, vector) / k_squared)
    )


def map_l2_norm(coefficients: Mapping[WaveKey, np.ndarray]) -> float:
    return math.sqrt(
        max(
            0.0,
            sum(float(np.vdot(value, value).real) for value in coefficients.values()),
        )
    )


def project_map(coefficients: Mapping[WaveKey, np.ndarray]) -> CoefficientMap:
    return {wave: leray_project(wave, value) for wave, value in coefficients.items()}


def reduced_profile_kernel(
    profile: np.ndarray,
    modes: np.ndarray,
) -> dict[str, CoefficientMap]:
    """Kernel A: exact one-dimensional product identities from (6.3)."""
    derivative = 1j * modes * profile
    second_derivative = -(modes.astype(float) ** 2) * profile
    conjugate_profile = np.conjugate(profile[::-1])
    conjugate_second = -(modes.astype(float) ** 2) * conjugate_profile
    output_modes = np.arange(2 * int(modes[0]), 2 * int(modes[-1]) + 1)

    self_scalar = 4j * (
        np.convolve(profile, second_derivative)
        - np.convolve(derivative, derivative)
    )
    modulus_squared = np.convolve(conjugate_profile, profile)
    mean_y = 4j * output_modes * modulus_squared
    mean_z = 4j * (
        np.convolve(conjugate_profile, second_derivative)
        - np.convolve(profile, conjugate_second)
    )

    kz2_raw: CoefficientMap = {}
    kz0_raw: CoefficientMap = {}
    for index, output_mode in enumerate(output_modes):
        kz2_raw[(0, 2 * int(output_mode), 2)] = np.asarray(
            [0.0j, 0.0j, self_scalar[index]], dtype=np.complex128
        )
        kz0_raw[(0, 2 * int(output_mode), 0)] = np.asarray(
            [0.0j, mean_y[index], mean_z[index]], dtype=np.complex128
        )
    return {"kz2": project_map(kz2_raw), "kz0": project_map(kz0_raw)}


def positive_velocity_coefficients(
    profile: np.ndarray,
    modes: np.ndarray,
) -> CoefficientMap:
    coefficients: CoefficientMap = {}
    for value, n_mode in zip(profile, modes):
        n_integer = int(n_mode)
        coefficients[(0, 2 * n_integer, 1)] = np.asarray(
            [0.0j, value, -2.0 * n_integer * value],
            dtype=np.complex128,
        )
    return coefficients


def real_pair_coefficients(positive: Mapping[WaveKey, np.ndarray]) -> CoefficientMap:
    coefficients = {
        wave: np.asarray(value, dtype=np.complex128).copy()
        for wave, value in positive.items()
    }
    for wave, value in positive.items():
        conjugate_wave = tuple(-entry for entry in wave)
        coefficients[conjugate_wave] = np.conjugate(value)
    return coefficients


def generic_quadratic_kernel(
    left: Mapping[WaveKey, np.ndarray],
    right: Mapping[WaveKey, np.ndarray],
    target_kz: int,
) -> CoefficientMap:
    """Kernel B: generic physical Fourier convolution followed by Leray."""
    raw: CoefficientMap = {}
    for left_wave, left_value in left.items():
        for right_wave, right_value in right.items():
            output_wave = tuple(
                left_wave[index] + right_wave[index] for index in range(3)
            )
            if output_wave[2] != target_kz:
                continue
            derivative_wave = np.asarray(right_wave, dtype=float)
            contribution = 1j * np.dot(left_value, derivative_wave) * right_value
            if output_wave in raw:
                raw[output_wave] += contribution
            else:
                raw[output_wave] = np.asarray(contribution, dtype=np.complex128)
    return project_map(raw)


def map_difference(
    left: Mapping[WaveKey, np.ndarray],
    right: Mapping[WaveKey, np.ndarray],
) -> dict[str, float]:
    keys = sorted(set(left) | set(right))
    zero = np.zeros(3, dtype=np.complex128)
    squared = 0.0
    maximum = 0.0
    for key in keys:
        difference = left.get(key, zero) - right.get(key, zero)
        size = float(np.linalg.norm(difference))
        squared += size * size
        maximum = max(maximum, size)
    difference_norm = math.sqrt(squared)
    scale = max(1.0, map_l2_norm(left), map_l2_norm(right))
    coefficient_scale = max(
        1.0,
        max((float(np.linalg.norm(value)) for value in left.values()), default=0.0),
        max((float(np.linalg.norm(value)) for value in right.values()), default=0.0),
    )
    return {
        "l2ScaleOneDifference": difference_norm / scale,
        "maximumCoefficientScaleOneDifference": maximum / coefficient_scale,
    }


def measure_case(n_cut: int, epsilon: float) -> dict[str, object]:
    matrix = frozen_kinetic_matrix(n_cut, epsilon)
    eigenvalue, kinetic_vector, spectral = select_top_profile(matrix)
    modes = np.arange(-n_cut, n_cut + 1, dtype=int)
    profile = recover_physical_profile(kinetic_vector, modes)
    costs = physical_costs(profile, kinetic_vector, modes)

    reduced = reduced_profile_kernel(profile, modes)
    positive = positive_velocity_coefficients(profile, modes)
    real_pair = real_pair_coefficients(positive)
    generic_kz2 = generic_quadratic_kernel(positive, positive, target_kz=2)
    generic_kz0 = generic_quadratic_kernel(real_pair, real_pair, target_kz=0)

    kz2_a = map_l2_norm(reduced["kz2"])
    kz2_b = map_l2_norm(generic_kz2)
    kz0_a = map_l2_norm(reduced["kz0"])
    kz0_b = map_l2_norm(generic_kz0)
    kz2_difference = map_difference(reduced["kz2"], generic_kz2)
    kz0_difference = map_difference(reduced["kz0"], generic_kz0)
    maximum_coefficient_difference = max(
        kz2_difference["maximumCoefficientScaleOneDifference"],
        kz0_difference["maximumCoefficientScaleOneDifference"],
    )
    kernel_pass = max(
        kz2_difference["l2ScaleOneDifference"],
        kz0_difference["l2ScaleOneDifference"],
        maximum_coefficient_difference,
    ) <= KERNEL_SCALE_ONE_TOLERANCE

    row: dict[str, object] = {
        "schemaVersion": SCHEMA_VERSION,
        "evidenceClass": EVIDENCE_CLASS,
        "diagnosticOnly": True,
        "N": n_cut,
        "dimension": 2 * n_cut + 1,
        "epsilon": epsilon,
        "absoluteLambda": 1.0 / epsilon,
        "topEigenvalueFastReal": float(eigenvalue.real),
        "topEigenvalueFastImag": float(eigenvalue.imag),
        "topPhysicalGrowthRateReal": float(4.0 * eigenvalue.real / epsilon),
        "topClusterDimensionAtRealTolerance": spectral["topClusterDimension"],
        "topRealGapBelowCluster": spectral["topRealGapBelowCluster"],
        "topEigenResidualRelative": spectral["topEigenResidualRelative"],
        **costs,
        "kz2ProjectedLeakagePositiveUnitRowKernelA": kz2_a,
        "kz2ProjectedLeakagePositiveUnitRowKernelB": kz2_b,
        "kz2ProjectedLeakageUnitRealPairKernelA": 0.5 * kz2_a,
        "kz0ProjectedLeakageUnscaledRealPairKernelA": kz0_a,
        "kz0ProjectedLeakageUnscaledRealPairKernelB": kz0_b,
        "kz0ProjectedLeakageUnitRealPairKernelA": 0.5 * kz0_a,
        "kz2KernelScaleOneDifference": kz2_difference["l2ScaleOneDifference"],
        "kz0KernelScaleOneDifference": kz0_difference["l2ScaleOneDifference"],
        "maximumKernelCoefficientScaleOneDifference": maximum_coefficient_difference,
        "kernelCheckPass": kernel_pass,
    }
    return row


def relative_change(left: complex | float, right: complex | float) -> float:
    return float(abs(left - right) / max(1.0e-14, abs(left), abs(right)))


def convergence_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    epsilons = sorted({float(row["epsilon"]) for row in rows}, reverse=True)
    for epsilon in epsilons:
        subset = sorted(
            (row for row in rows if float(row["epsilon"]) == epsilon),
            key=lambda row: int(row["N"]),
        )
        for coarse, fine in zip(subset, subset[1:]):
            coarse_eigenvalue = complex(
                float(coarse["topEigenvalueFastReal"]),
                float(coarse["topEigenvalueFastImag"]),
            )
            fine_eigenvalue = complex(
                float(fine["topEigenvalueFastReal"]),
                float(fine["topEigenvalueFastImag"]),
            )
            changes = {
                "topEigenvalueRelativeChange": relative_change(
                    coarse_eigenvalue, fine_eigenvalue
                ),
                "physicalH3ToL2RelativeChange": relative_change(
                    float(coarse["physicalH3ToL2Cost"]),
                    float(fine["physicalH3ToL2Cost"]),
                ),
                "kz2LeakageRelativeChange": relative_change(
                    float(coarse["kz2ProjectedLeakagePositiveUnitRowKernelA"]),
                    float(fine["kz2ProjectedLeakagePositiveUnitRowKernelA"]),
                ),
                "kz0LeakageRelativeChange": relative_change(
                    float(coarse["kz0ProjectedLeakageUnscaledRealPairKernelA"]),
                    float(fine["kz0ProjectedLeakageUnscaledRealPairKernelA"]),
                ),
            }
            result.append({
                "schemaVersion": SCHEMA_VERSION,
                "evidenceClass": EVIDENCE_CLASS,
                "diagnosticOnly": True,
                "epsilon": epsilon,
                "absoluteLambda": 1.0 / epsilon,
                "coarseN": int(coarse["N"]),
                "fineN": int(fine["N"]),
                **changes,
                "maximumRelativeChange": max(changes.values()),
                "ordinaryCutoffAgreementIsTailBound": False,
            })
    return result


def csv_cell(value: object) -> object:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return format(value, ".17g")
    return value


def write_csv(path: Path, fields: Iterable[str], rows: list[dict[str, object]]) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    with temporary.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(fields), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_cell(row[field]) for field in fields})
    os.replace(temporary, path)


def plot_results(
    rows: list[dict[str, object]],
    convergence: list[dict[str, object]],
    output_dir: Path,
    png_dpi: int,
) -> list[Path]:
    import matplotlib  # noqa: WPS433

    matplotlib.use("Agg")
    matplotlib.rcParams["svg.hashsalt"] = "r073g-nonlinear-row-leakage-v1"
    import matplotlib.pyplot as plt  # noqa: WPS433

    style = ROOT / "figures" / "journal.mplstyle"
    if style.exists():
        plt.style.use(style)

    cutoffs = sorted({int(row["N"]) for row in rows})
    primary_cutoff = max(cutoffs)
    colors = ["#737373", "#67a9cf", "#2166ac", "#053061"]
    markers = ["v", "s", "o", "D"]
    if len(cutoffs) > len(colors):
        colors = [plt.cm.Blues(value) for value in np.linspace(0.4, 0.95, len(cutoffs))]
        markers = ["o"] * len(cutoffs)

    width = 178.0 / 25.4
    height = 132.0 / 25.4
    fig, axes = plt.subplots(2, 2, figsize=(width, height), constrained_layout=True)
    fig.suptitle(
        "R0.73G finite top-profile and row-leakage diagnostic",
        x=0.01,
        ha="left",
        fontweight="bold",
    )

    ax = axes[0, 0]
    for color, marker, n_cut in zip(colors, markers, cutoffs):
        subset = sorted(
            (row for row in rows if int(row["N"]) == n_cut),
            key=lambda row: float(row["absoluteLambda"]),
        )
        ax.plot(
            [float(row["absoluteLambda"]) for row in subset],
            [float(row["topEigenvalueFastReal"]) for row in subset],
            color=color,
            marker=marker,
            markerfacecolor="white" if n_cut != primary_cutoff else color,
            label=rf"$N={n_cut}$",
        )
    ax.axhline(0.17035, color="#b35806", linestyle=":", label="0.17035 reference")
    ax.set_xscale("log")
    ax.set_xlabel(r"$|\Lambda|=\varepsilon^{-1}$")
    ax.set_ylabel(r"$\Re\lambda_{\rm top}$ (fast time)")
    ax.set_title("A  Frozen top eigenvalue", loc="left", fontweight="bold")
    ax.legend(ncol=2, handlelength=1.8)

    ax = axes[0, 1]
    for color, marker, n_cut in zip(colors, markers, cutoffs):
        subset = sorted(
            (row for row in rows if int(row["N"]) == n_cut),
            key=lambda row: float(row["absoluteLambda"]),
        )
        ax.plot(
            [float(row["absoluteLambda"]) for row in subset],
            [float(row["physicalH3ToL2Cost"]) for row in subset],
            color=color,
            marker=marker,
            markerfacecolor="white" if n_cut != primary_cutoff else color,
            label=rf"$N={n_cut}$",
        )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"$|\Lambda|=\varepsilon^{-1}$")
    ax.set_ylabel(r"physical $\|u_v\|_{H^3}/\|u_v\|_2$")
    ax.set_title("B  Physical Sobolev cost", loc="left", fontweight="bold")

    primary = sorted(
        (row for row in rows if int(row["N"]) == primary_cutoff),
        key=lambda row: float(row["absoluteLambda"]),
    )
    x_primary = [float(row["absoluteLambda"]) for row in primary]
    ax = axes[1, 0]
    ax.plot(
        x_primary,
        [float(row["kz2ProjectedLeakagePositiveUnitRowKernelA"]) for row in primary],
        color="#2166ac",
        marker="o",
        label=r"$K_z=2$: $B(u_+,u_+)$",
    )
    ax.plot(
        x_primary,
        [float(row["kz0ProjectedLeakageUnscaledRealPairKernelA"]) for row in primary],
        color="#b35806",
        marker="s",
        markerfacecolor="white",
        linestyle="--",
        label=r"$K_z=0$: $B(u_++\bar u_+,u_++\bar u_+)$",
    )
    ax.set_xscale("log")
    if all(
        float(row[field]) > 0.0
        for row in primary
        for field in (
            "kz2ProjectedLeakagePositiveUnitRowKernelA",
            "kz0ProjectedLeakageUnscaledRealPairKernelA",
        )
    ):
        ax.set_yscale("log")
    ax.set_xlabel(r"$|\Lambda|=\varepsilon^{-1}$")
    ax.set_ylabel(r"projected quadratic leakage $L^2$")
    ax.set_title(
        f"C  Generated rows at cutoff $N={primary_cutoff}$",
        loc="left",
        fontweight="bold",
    )
    ax.legend(handlelength=2.2)

    ax = axes[1, 1]
    kernel_defect = [
        max(
            float(row["kz2KernelScaleOneDifference"]),
            float(row["kz0KernelScaleOneDifference"]),
            float(row["maximumKernelCoefficientScaleOneDifference"]),
        )
        for row in primary
    ]
    finest_pairs = sorted(
        (
            row for row in convergence
            if int(row["fineN"]) == primary_cutoff
        ),
        key=lambda row: float(row["absoluteLambda"]),
    )
    ax.plot(
        x_primary,
        np.maximum(kernel_defect, DISPLAY_FLOOR),
        color="#252525",
        marker="x",
        linestyle=":",
        label=r"independent-kernel defect (floor $10^{-18}$)",
    )
    if finest_pairs:
        ax.plot(
            [float(row["absoluteLambda"]) for row in finest_pairs],
            [max(float(row["maximumRelativeChange"]), DISPLAY_FLOOR) for row in finest_pairs],
            color="#2166ac",
            marker="o",
            label=f"cutoff {int(finest_pairs[0]['coarseN'])} vs {primary_cutoff}",
        )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"$|\Lambda|=\varepsilon^{-1}$")
    ax.set_ylabel("scale-one defect or relative change")
    ax.set_title("D  Numerical cross-checks", loc="left", fontweight="bold")
    ax.legend(handlelength=2.2)

    for axis in axes.flat:
        axis.tick_params(pad=2)
    fig.text(
        0.01,
        0.002,
        "Finite binary64 Fourier compressions; diagnostic only.  "
        "Normalized Fourier basis; physical positive row has L2 norm one.",
        ha="left",
        va="bottom",
        fontsize=6.2,
        color="#252525",
    )

    title = "R0.73G finite nonlinear row-leakage diagnostic"
    creator = "nonlinear_row_leakage_diagnostic.py"
    paths = [
        output_dir / "fig-r073g-nonlinear-row-leakage.pdf",
        output_dir / "fig-r073g-nonlinear-row-leakage.svg",
        output_dir / "fig-r073g-nonlinear-row-leakage.png",
    ]
    specifications = (
        (paths[0], "pdf", {"Creator": creator, "Title": title, "Subject": EVIDENCE_CLASS,
                           "CreationDate": None, "ModDate": None}, None),
        (paths[1], "svg", {"Creator": creator, "Title": title, "Description": EVIDENCE_CLASS,
                           "Date": None}, None),
        (paths[2], "png", {"Software": creator, "Title": title,
                           "Description": EVIDENCE_CLASS}, png_dpi),
    )
    for path, file_format, metadata, dpi in specifications:
        temporary = path.with_name(f".{path.name}.tmp")
        kwargs: dict[str, object] = {
            "format": file_format,
            "metadata": metadata,
        }
        if dpi is not None:
            kwargs["dpi"] = dpi
        fig.savefig(temporary, **kwargs)
        os.replace(temporary, path)
    plt.close(fig)
    return paths


def summarize(
    rows: list[dict[str, object]],
    convergence: list[dict[str, object]],
    epsilons: list[float],
    cutoffs: list[int],
    provenance: dict[str, object],
    output_bindings: list[dict[str, object]],
    png_dpi: int,
    smoke: bool,
) -> dict[str, object]:
    primary_cutoff = max(cutoffs)
    primary = [row for row in rows if int(row["N"]) == primary_cutoff]
    finest = [row for row in convergence if int(row["fineN"]) == primary_cutoff]
    maximum_kernel_defect = max(
        max(
            float(row["kz2KernelScaleOneDifference"]),
            float(row["kz0KernelScaleOneDifference"]),
            float(row["maximumKernelCoefficientScaleOneDifference"]),
        )
        for row in rows
    )
    return {
        "schemaVersion": SCHEMA_VERSION,
        "release": "R0.73G",
        "evidenceClass": EVIDENCE_CLASS,
        "diagnosticOnly": True,
        "smokeMode": smoke,
        "sourceProvenance": provenance,
        "software": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
        "parameters": {
            "gamma": GAMMA,
            "mu": MU,
            "profileTime": 0.0,
            "epsilons": epsilons,
            "cutoffs": cutoffs,
            "primaryCutoff": primary_cutoff,
            "topRealTolerance": TOP_REAL_TOLERANCE,
            "kernelScaleOneTolerance": KERNEL_SCALE_ONE_TOLERANCE,
            "pngDpi": png_dpi,
            "fourierNormalization": "normalized periodic Parseval basis",
            "physicalPositiveRow": "(0,v(2y),2 i v'(2y)) exp(i z)",
            "physicalH3Convention": "Bessel potential multiplier (1+|k|^2)^(3/2)",
            "unscaledRealPairL2": math.sqrt(2.0),
        },
        "rows": rows,
        "cutoffComparisons": convergence,
        "crossValidation": {
            "kernelA": "reduced one-dimensional identities for Kz=2 and Kz=0",
            "kernelB": "generic physical Fourier convolution and modewise Leray projection",
            "maximumScaleOneDifference": maximum_kernel_defect,
            "allKernelChecksPass": all(bool(row["kernelCheckPass"]) for row in rows),
        },
        "primaryCutoffObservedRanges": {
            "topEigenvalueFastReal": [
                min(float(row["topEigenvalueFastReal"]) for row in primary),
                max(float(row["topEigenvalueFastReal"]) for row in primary),
            ],
            "physicalH3ToL2Cost": [
                min(float(row["physicalH3ToL2Cost"]) for row in primary),
                max(float(row["physicalH3ToL2Cost"]) for row in primary),
            ],
            "kz2ProjectedLeakagePositiveUnitRow": [
                min(float(row["kz2ProjectedLeakagePositiveUnitRowKernelA"]) for row in primary),
                max(float(row["kz2ProjectedLeakagePositiveUnitRowKernelA"]) for row in primary),
            ],
            "kz0ProjectedLeakageUnscaledRealPair": [
                min(float(row["kz0ProjectedLeakageUnscaledRealPairKernelA"]) for row in primary),
                max(float(row["kz0ProjectedLeakageUnscaledRealPairKernelA"]) for row in primary),
            ],
            "maximumFinestCutoffRelativeChange": (
                max(float(row["maximumRelativeChange"]) for row in finest)
                if finest
                else None
            ),
        },
        "outputs": output_bindings,
        "claimBoundary": {
            "finiteBinary64Diagnostic": True,
            "actualFiniteTopEigenprofileUsed": True,
            "twoIndependentFourierKernelsCrossChecked": True,
            "ordinaryCutoffAgreementIsTailBound": False,
            "finiteTopEqualsContinuumTop": False,
            "finiteH3CostProvesUniformContinuumH3Bound": False,
            "finiteLeakageProvesNonlinearInstability": False,
            "transitionThresholdEstablished": False,
            "threeDimensionalVortexStretchingPresentInThisPlanarRow": False,
            "clayProblemSolved": False,
        },
    }


def main() -> int:
    epsilons = parse_positive_floats(ARGS.epsilons)
    cutoffs = parse_positive_ints(ARGS.cutoffs)
    if ARGS.smoke:
        epsilons = [0.01]
        cutoffs = [6, 8]
    if ARGS.png_dpi <= 0:
        raise ValueError("png dpi must be positive")

    output_dir = ARGS.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_paths = [output_dir / name for name in OUTPUT_NAMES]
    if not ARGS.overwrite and any(path.exists() for path in output_paths):
        existing = [path.name for path in output_paths if path.exists()]
        raise RuntimeError(f"output exists; pass --overwrite: {existing}")

    provenance = git_source_provenance(ARGS.smoke)
    emit(
        "start",
        diagnosticOnly=True,
        smokeMode=ARGS.smoke,
        epsilons=epsilons,
        cutoffs=cutoffs,
        outputDirectory=str(output_dir),
        sourceCommit=provenance["sourceCommit"],
        sourceMatchesHead=provenance["workingSourceMatchesHead"],
    )

    rows: list[dict[str, object]] = []
    total = len(epsilons) * len(cutoffs)
    case_index = 0
    for n_cut in cutoffs:
        for epsilon in epsilons:
            case_index += 1
            emit(
                "case_start",
                caseIndex=case_index,
                caseCount=total,
                N=n_cut,
                epsilon=epsilon,
                absoluteLambda=1.0 / epsilon,
            )
            row = measure_case(n_cut, epsilon)
            rows.append(row)
            emit(
                "case_complete",
                caseIndex=case_index,
                caseCount=total,
                N=n_cut,
                epsilon=epsilon,
                topEigenvalueFastReal=row["topEigenvalueFastReal"],
                physicalH3ToL2Cost=row["physicalH3ToL2Cost"],
                kz2Leakage=row["kz2ProjectedLeakagePositiveUnitRowKernelA"],
                kz0Leakage=row["kz0ProjectedLeakageUnscaledRealPairKernelA"],
                kernelCheckPass=row["kernelCheckPass"],
            )

    rows.sort(key=lambda row: (int(row["N"]), -float(row["epsilon"])))
    convergence = convergence_rows(rows)
    row_csv = output_dir / OUTPUT_NAMES[0]
    convergence_csv = output_dir / OUTPUT_NAMES[1]
    write_csv(row_csv, ROW_FIELDS, rows)
    write_csv(convergence_csv, CONVERGENCE_FIELDS, convergence)

    emit("plot_start", pngDpi=ARGS.png_dpi)
    figure_paths = plot_results(rows, convergence, output_dir, ARGS.png_dpi)
    emit("plot_complete", outputs=[path.name for path in figure_paths])

    data_and_figure_paths = [row_csv, convergence_csv, *figure_paths]
    summary = summarize(
        rows,
        convergence,
        epsilons,
        cutoffs,
        provenance,
        [binding(path, output_dir) for path in data_and_figure_paths],
        ARGS.png_dpi,
        ARGS.smoke,
    )
    summary_path = output_dir / OUTPUT_NAMES[2]
    atomic_text(summary_path, canonical_json(summary))

    all_kernel_checks = bool(summary["crossValidation"]["allKernelChecksPass"])
    emit(
        "complete",
        diagnosticOnly=True,
        allKernelChecksPass=all_kernel_checks,
        maximumKernelScaleOneDifference=summary["crossValidation"]["maximumScaleOneDifference"],
        outputCount=len(OUTPUT_NAMES),
    )
    return 0 if all_kernel_checks else 2


if __name__ == "__main__":
    raise SystemExit(main())
