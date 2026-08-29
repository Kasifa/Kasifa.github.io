#!/usr/bin/env python3
"""Finite-dimensional frozen-time OS spectral audit for R0.73A.

This is an exploratory counterexample/theorem-design screen.  It never treats
Fourier--Galerkin output as a proof about the infinite-dimensional operator.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
import time


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default=os.environ.get("R073A_DEPS", ""))
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--broad-N", type=int, default=18)
    parser.add_argument("--target-N", default="12,18,24")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


ARGS = parse_args()
if ARGS.deps:
    sys.path.insert(0, ARGS.deps)

import numpy as np  # noqa: E402
import scipy  # noqa: E402
from scipy.linalg import eig, eigvalsh, expm, qr, svdvals  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
OUT = ARGS.out.resolve()
PROGRESS = OUT / "progress.ndjson"
ROW_FIELDS = [
    "tier", "caseId", "projection", "N", "dimension", "d", "beta", "mu",
    "gap", "c", "alpha", "spectralAbscissa", "spectralImagAtEdge",
    "numericalAbscissa", "frobeniusNorm", "henriciRelativeDeparture",
    "eigenvectorCondition", "sampledTransientGain", "sampledPeakTime",
    "sampledLog10TransientGain", "transientGainCensored", "timeGridCount",
    "resolventSampleScale", "resolventPeak",
    "sampledKreissLowerBound", "epsilonRelative", "pseudoRightExcursion",
    "pseudospectralAbscissaLowerSample", "projectionRankRemoved",
    "qStarCompressionLeakage", "finiteDimensionalOnly",
]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def emit(event: str, **payload: object) -> None:
    record = {
        "time": datetime.now(timezone.utc).isoformat(),
        "event": event,
        **payload,
    }
    line = json.dumps(record, sort_keys=True, ensure_ascii=True)
    with PROGRESS.open("a", encoding="utf-8") as stream:
        stream.write(line + "\n")
    print(line, flush=True)


def heat_profile_coefficients(d: float) -> tuple[dict[int, complex], dict[int, complex]]:
    # If a*sin(kx), then the +k Fourier coefficient is a/(2i).
    w = {
        1: 0.25j * math.exp(-d),
        -1: -0.25j * math.exp(-d),
        2: -0.125j * math.exp(-4.0 * d),
        -2: 0.125j * math.exp(-4.0 * d),
    }
    wxx = {
        1: -0.25j * math.exp(-d),
        -1: 0.25j * math.exp(-d),
        2: 0.5j * math.exp(-4.0 * d),
        -2: -0.5j * math.exp(-4.0 * d),
    }
    return w, wxx


def generator(N: int, d: float, beta: float, mu: float, c: float) -> tuple[np.ndarray, np.ndarray]:
    modes = np.arange(-N, N + 1, dtype=float)
    lam = (modes + beta) ** 2 + mu
    if np.min(lam) <= 0:
        raise ValueError("L must be strictly positive in this audit")
    w, wxx = heat_profile_coefficients(d)
    size = len(modes)
    matrix = np.zeros((size, size), dtype=np.complex128)
    matrix[np.diag_indices(size)] = -lam
    integer_modes = np.arange(-N, N + 1, dtype=int)
    for row, m in enumerate(integer_modes):
        for col, n in enumerate(integer_modes):
            shift = m - n
            if shift in w:
                matrix[row, col] += -1j * c * w[shift]
                matrix[row, col] += -1j * c * wxx[shift] / lam[col]
    return matrix, lam


def sine_vector(N: int, harmonic: int, amplitude: float = 1.0) -> np.ndarray:
    vector = np.zeros(2 * N + 1, dtype=np.complex128)
    if harmonic <= N:
        vector[N + harmonic] = amplitude / (2j)
        vector[N - harmonic] = -amplitude / (2j)
    return vector


def projection_basis(N: int, d: float, projection: str) -> tuple[np.ndarray, int]:
    size = 2 * N + 1
    if projection == "unprojected":
        return np.eye(size, dtype=np.complex128), 0
    if projection == "qstar-Wxx":
        qstar = (0.5 * math.exp(-d) * sine_vector(N, 1)
                 - math.exp(-4.0 * d) * sine_vector(N, 2))
        constraints = qstar[:, None]
    elif projection == "span-sin1-sin2":
        constraints = np.column_stack((sine_vector(N, 1), sine_vector(N, 2)))
    else:
        raise ValueError(f"unknown projection: {projection}")
    orthogonal, _ = qr(constraints, mode="full", check_finite=False)
    removed = constraints.shape[1]
    return orthogonal[:, removed:], removed


def compress(matrix: np.ndarray, basis: np.ndarray) -> np.ndarray:
    return basis.conj().T @ matrix @ basis


def qstar_leakage(matrix: np.ndarray, N: int, d: float, basis: np.ndarray) -> float:
    qstar = (0.5 * math.exp(-d) * sine_vector(N, 1)
             - math.exp(-4.0 * d) * sine_vector(N, 2))
    return float(np.linalg.norm(basis.conj().T @ matrix @ qstar) / np.linalg.norm(qstar))


def static_metrics(matrix: np.ndarray) -> dict[str, float]:
    eigenvalues, eigenvectors = eig(matrix, check_finite=False)
    edge_index = int(np.argmax(eigenvalues.real))
    spectral = float(eigenvalues[edge_index].real)
    numerical = float(eigvalsh((matrix + matrix.conj().T) / 2.0,
                               check_finite=False)[-1])
    frob = float(np.linalg.norm(matrix, "fro"))
    departure_sq = max(0.0, frob * frob - float(np.sum(np.abs(eigenvalues) ** 2)))
    condition = float(np.linalg.cond(eigenvectors))
    return {
        "spectralAbscissa": spectral,
        "spectralImagAtEdge": float(eigenvalues[edge_index].imag),
        "numericalAbscissa": numerical,
        "frobeniusNorm": frob,
        "henriciRelativeDeparture": math.sqrt(departure_sq) / max(frob, 1e-300),
        "eigenvectorCondition": condition,
    }


def time_grid(c: float) -> np.ndarray:
    alpha = (abs(c) / 4.0) ** (-0.2)
    block = alpha * alpha
    values = np.concatenate((
        np.array([0.0]),
        np.geomspace(1e-5 * block, 8.0 * block, 13),
        np.linspace(0.25 * block, 8.0 * block, 11),
    ))
    return np.unique(np.round(values, 16))


def transient_metrics(matrix: np.ndarray, c: float,
                      numerical_abscissa: float) -> dict[str, float | int | bool]:
    best_log_gain = 0.0
    best_time = 0.0
    grid = time_grid(c)
    shift = max(0.0, numerical_abscissa)
    shifted = matrix - shift * np.eye(matrix.shape[0], dtype=np.complex128)
    for tau in grid:
        shifted_gain = float(svdvals(expm(shifted * tau), check_finite=False)[0])
        log_gain = shift * float(tau) + math.log(max(shifted_gain, 1e-300))
        if log_gain > best_log_gain:
            best_log_gain = log_gain
            best_time = float(tau)
    censored = best_log_gain > math.log(sys.float_info.max) - 2.0
    best_gain = sys.float_info.max if censored else math.exp(best_log_gain)
    return {
        "sampledTransientGain": best_gain,
        "sampledPeakTime": best_time,
        "sampledLog10TransientGain": best_log_gain / math.log(10.0),
        "transientGainCensored": censored,
        "timeGridCount": int(len(grid)),
    }


def pseudospectral_metrics(matrix: np.ndarray, spectral: float) -> dict[str, float]:
    eigenvalues = eig(matrix, left=False, right=False, check_finite=False)
    scale = max(1.0, float(np.linalg.norm(matrix, 2)))
    imag_lo = float(np.min(eigenvalues.imag))
    imag_hi = float(np.max(eigenvalues.imag))
    padding = 0.05 * max(scale, imag_hi - imag_lo, 1.0)
    uniform = np.linspace(imag_lo - padding, imag_hi + padding, 21)
    edge_imag = eigenvalues.imag[np.argsort(eigenvalues.real)[-8:]]
    omegas = np.unique(np.concatenate((uniform, edge_imag, np.array([0.0]))))
    deltas = scale * np.geomspace(1e-5, 1e-1, 10)
    epsilon = 1e-2
    identity = np.eye(matrix.shape[0], dtype=np.complex128)
    peak_resolvent = 0.0
    kreiss = 0.0
    excursion = 0.0
    for delta in deltas:
        x = spectral + float(delta)
        minimum = math.inf
        for omega in omegas:
            sigma_min = float(svdvals((x + 1j * omega) * identity - matrix,
                                      check_finite=False)[-1])
            minimum = min(minimum, sigma_min)
        peak_resolvent = max(peak_resolvent, 1.0 / max(minimum, 1e-300))
        if minimum / scale <= epsilon:
            excursion = float(delta)
        if spectral < 0 and x > 0:
            kreiss = max(kreiss, x / max(minimum, 1e-300))
    return {
        "resolventSampleScale": scale,
        "resolventPeak": peak_resolvent,
        "sampledKreissLowerBound": kreiss,
        "epsilonRelative": epsilon,
        "pseudoRightExcursion": excursion,
        "pseudospectralAbscissaLowerSample": spectral + excursion,
    }


def blank_dynamic() -> dict[str, str]:
    return {key: "" for key in (
        "sampledTransientGain", "sampledPeakTime", "sampledLog10TransientGain",
        "transientGainCensored", "timeGridCount",
        "resolventSampleScale", "resolventPeak", "sampledKreissLowerBound",
        "epsilonRelative", "pseudoRightExcursion", "pseudospectralAbscissaLowerSample",
    )}


def make_row(tier: str, case_id: str, projection: str, N: int, d: float,
             beta: float, mu: float, c: float, dynamic: bool) -> dict[str, object]:
    raw, _ = generator(N, d, beta, mu, c)
    basis, removed = projection_basis(N, d, projection)
    matrix = compress(raw, basis)
    alpha = (abs(c) / 4.0) ** (-0.2)
    metrics: dict[str, object] = static_metrics(matrix)
    if dynamic:
        metrics.update(transient_metrics(matrix, c, float(metrics["numericalAbscissa"])))
        metrics.update(pseudospectral_metrics(matrix, float(metrics["spectralAbscissa"])))
    else:
        metrics.update(blank_dynamic())
    return {
        "tier": tier,
        "caseId": case_id,
        "projection": projection,
        "N": N,
        "dimension": matrix.shape[0],
        "d": d,
        "beta": beta,
        "mu": mu,
        "gap": beta * beta + mu,
        "c": c,
        "alpha": alpha,
        **metrics,
        "projectionRankRemoved": removed,
        "qStarCompressionLeakage": qstar_leakage(raw, N, d, basis),
        "finiteDimensionalOnly": True,
    }


def broad_cases() -> list[tuple[str, float, float, float, float]]:
    rows = []
    count = 0
    for d in (0.0, 0.05, 0.25, 1.0):
        for beta in (0.0, 1e-4, 1e-3, 1e-2, 0.05, 0.25, 0.49):
            for mu in (1e-6, 1e-4, 1e-2, 1e-1):
                for c in (4.0, 128.0, 4096.0, 131072.0):
                    count += 1
                    rows.append((f"B{count:04d}", d, beta, mu, c))
    return rows


def target_cases() -> list[tuple[str, float, float, float, float]]:
    return [
        ("T01-lowest-gap-c4", 0.0, 0.0, 1e-6, 4.0),
        ("T02-near-bloch-c128", 0.0, 1e-4, 1e-6, 128.0),
        ("T03-near-bloch-c4096", 0.0, 1e-3, 1e-4, 4096.0),
        ("T04-strong-c131072", 0.0, 1e-2, 1e-2, 131072.0),
        ("T05-post-collision", 0.25, 0.0, 1e-4, 4096.0),
        ("T06-late-weak-bloch", 1.0, 1e-2, 1e-4, 128.0),
        ("T07-off-axis", 0.05, 0.25, 1e-4, 4096.0),
        ("T08-edge-bloch", 0.25, 0.49, 1e-2, 128.0),
        ("T09-collision-alpha025", 0.0625, 0.0, 0.0625, 4096.0),
        ("T10-collision-alpha0125", 0.015625, 0.0, 0.015625, 131072.0),
    ]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=ROW_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def finite_number(value: object) -> bool:
    if value == "":
        return True
    return math.isfinite(float(value))


def summarize(rows: list[dict[str, object]], elapsed: float) -> dict[str, object]:
    target = [row for row in rows if row["tier"] == "target"]
    broad = [row for row in rows if row["tier"] == "broad"]
    by_projection: dict[str, dict[str, object]] = {}
    for projection in ("unprojected", "qstar-Wxx", "span-sin1-sin2"):
        subset = [row for row in target if row["projection"] == projection]
        by_projection[projection] = {
            "rows": len(subset),
            "positiveSpectralRows": sum(float(row["spectralAbscissa"]) > 0 for row in subset),
            "positiveNumericalRows": sum(float(row["numericalAbscissa"]) > 0 for row in subset),
            "maximumSampledLog10TransientGain": max(float(row["sampledLog10TransientGain"])
                                                     for row in subset),
            "censoredTransientRows": sum(bool(row["transientGainCensored"])
                                          for row in subset),
            "maximumSampledKreissLowerBound": max(float(row["sampledKreissLowerBound"])
                                                   for row in subset),
            "maximumEigenvectorCondition": max(float(row["eigenvectorCondition"])
                                                for row in subset),
        }
    convergence = []
    for case_id, *_ in target_cases():
        for projection in ("unprojected", "qstar-Wxx", "span-sin1-sin2"):
            subset = sorted((row for row in target if row["caseId"] == case_id
                             and row["projection"] == projection), key=lambda row: int(row["N"]))
            last, previous = subset[-1], subset[-2]
            convergence.append({
                "caseId": case_id,
                "projection": projection,
                "NPair": [int(previous["N"]), int(last["N"])],
                "spectralAbscissaDifference": abs(float(last["spectralAbscissa"])
                                                  - float(previous["spectralAbscissa"])),
                "sampledLog10TransientGainDifference": abs(
                    float(last["sampledLog10TransientGain"])
                    - float(previous["sampledLog10TransientGain"])),
                "pseudoRightExcursionRelativeDifference": abs(
                    float(last["pseudoRightExcursion"]) - float(previous["pseudoRightExcursion"]))
                    / max(float(last["resolventSampleScale"]) * 1e-12,
                          float(last["pseudoRightExcursion"]), 1e-300),
            })
    return {
        "schemaVersion": 1,
        "status": "completed",
        "scope": "finite Fourier-Galerkin frozen-time counterexample and theorem-design audit",
        "finiteDimensionalOnly": True,
        "broadRows": len(broad),
        "targetRows": len(target),
        "totalRows": len(rows),
        "projections": by_projection,
        "convergence": convergence,
        "broadPositiveSpectralRows": sum(float(row["spectralAbscissa"]) > 0 for row in broad),
        "broadPositiveNumericalRows": sum(float(row["numericalAbscissa"]) > 0 for row in broad),
        "allRecordedNumbersFinite": all(finite_number(row[field]) for row in rows
                                        for field in ROW_FIELDS if field not in {
                                            "tier", "caseId", "projection", "finiteDimensionalOnly"
                                        }),
        "elapsedSeconds": elapsed,
    }


def environment_record() -> dict[str, object]:
    stream = io.StringIO()
    old_stdout = sys.stdout
    try:
        sys.stdout = stream
        np.show_config()
    finally:
        sys.stdout = old_stdout
    git_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                       text=True).strip()
    return {
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "cpuCount": os.cpu_count(),
        "depsPath": ARGS.deps,
        "gitHead": git_head,
        "blasAndLapack": stream.getvalue(),
        "randomness": "none",
        "threadsRequested": 1,
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    outputs = [OUT / name for name in (
        "broad_spectral.csv", "target_dynamics.csv", "all_rows.csv",
        "summary.json", "environment.json", "manifest.json", "progress.ndjson",
    )]
    if not ARGS.overwrite and any(path.exists() for path in outputs):
        raise RuntimeError("output exists; pass --overwrite for a fresh deterministic run")
    for path in outputs:
        if path.exists():
            path.unlink()
    start = time.perf_counter()
    target_ns = [int(item) for item in ARGS.target_N.split(",")]
    projections = ("unprojected", "qstar-Wxx", "span-sin1-sin2")
    emit("start", broadN=ARGS.broad_N, targetN=target_ns,
         broadCases=len(broad_cases()), targetCases=len(target_cases()))
    broad_rows: list[dict[str, object]] = []
    for index, (case_id, d, beta, mu, c) in enumerate(broad_cases(), start=1):
        for projection in projections:
            broad_rows.append(make_row("broad", case_id, projection, ARGS.broad_N,
                                       d, beta, mu, c, dynamic=False))
        if index % 32 == 0 or index == len(broad_cases()):
            emit("broad-progress", completedCases=index, totalCases=len(broad_cases()),
                 rows=len(broad_rows), elapsedSeconds=time.perf_counter() - start)
            write_csv(OUT / "broad_spectral.csv", broad_rows)
    target_rows: list[dict[str, object]] = []
    for index, (case_id, d, beta, mu, c) in enumerate(target_cases(), start=1):
        for N in target_ns:
            for projection in projections:
                target_rows.append(make_row("target", case_id, projection, N,
                                            d, beta, mu, c, dynamic=True))
        write_csv(OUT / "target_dynamics.csv", target_rows)
        emit("target-progress", completedCases=index, totalCases=len(target_cases()),
             caseId=case_id, rows=len(target_rows), elapsedSeconds=time.perf_counter() - start)
    rows = broad_rows + target_rows
    write_csv(OUT / "all_rows.csv", rows)
    elapsed = time.perf_counter() - start
    summary = summarize(rows, elapsed)
    (OUT / "summary.json").write_text(canonical_json(summary), encoding="utf-8")
    environment = environment_record()
    (OUT / "environment.json").write_text(canonical_json(environment), encoding="utf-8")
    emit("complete", rows=len(rows), elapsedSeconds=elapsed,
         summarySha256=sha256(OUT / "summary.json"))
    manifest = {
        "schemaVersion": 1,
        "status": "completed",
        "finiteDimensionalOnly": True,
        "source": "frozen_os_spectral_audit.py",
        "sourceSha256": sha256(Path(__file__).resolve()),
        "validator": "validate_frozen_os_spectral_audit.py",
        "requirements": "requirements.txt",
        "command": "command.txt",
        "configuration": {
            "broadN": ARGS.broad_N,
            "targetN": target_ns,
            "projections": list(projections),
            "broadCases": len(broad_cases()),
            "targetCases": [list(row) for row in target_cases()],
            "timeGrid": "unique union of 0, 13 geometric, and 11 linear samples on [0,8 alpha^2]",
            "pseudospectrum": "10 right-edge offsets x adaptive 21-point-plus-edge-imaginary grid",
            "epsilonRelative": 1e-2,
        },
        "limitations": [
            "finite Fourier-Galerkin compression is not an infinite-dimensional proof",
            "projected matrices are modified compressed generators, not proved invariant quotients",
            "sampled transient gain is not the continuous-time global maximum",
            "sampled pseudospectral and Kreiss quantities are lower-resolution diagnostics",
            "no Galerkin tail error bound is supplied",
        ],
        "outputs": [],
    }
    for path in (OUT / "broad_spectral.csv", OUT / "target_dynamics.csv",
                 OUT / "all_rows.csv", OUT / "summary.json", OUT / "environment.json",
                 OUT / "progress.ndjson"):
        manifest["outputs"].append({
            "path": path.name,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    (OUT / "manifest.json").write_text(canonical_json(manifest), encoding="utf-8")
    print(canonical_json(summary), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
