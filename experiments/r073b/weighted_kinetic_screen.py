#!/usr/bin/env python3
"""Deterministic finite-Fourier screen for the R0.73B kinetic norm.

The program integrates the transformed Orr--Sommerfeld row on the special
``beta=xi=0`` slice and measures one propagator in several diagonal norms.
It is deliberately a finite-dimensional falsification and theorem-design
screen: no Galerkin tail enclosure or interval arithmetic is supplied.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import sys

import numpy as np


@dataclass(frozen=True)
class Case:
    family: str
    path_id: str
    mu: float
    c: float
    p: float
    kappa: float
    sign: int
    start: float
    end: float


NORM_SPECS = {
    # raw_q is special: q_0=mu*h and q_k=r_k.
    "raw_q": (-2.0, 0.0),
    "xmu": (0.0, 0.0),
    "hminus1": (0.0, 1.0),
    "balanced_l2": (1.0, 0.0),
    "kinetic": (1.0, 1.0),
    "kinetic_under": (0.5, 1.0),
    "kinetic_over": (1.5, 1.0),
}

FIELDS = (
    "caseId", "family", "pathId", "N", "dimension", "start", "end",
    "tau", "mu", "gammaAbs", "c", "Lambda", "p", "kappa", "sign",
    "norm", "muWeightExponentA", "laplacianWeightExponentB", "gain",
    "logGain", "xmuLogBound", "kineticLogBound", "boundMargin",
    "inputMeanFraction", "inputK1Fraction", "inputK2Fraction",
    "inputTailFraction", "outputMeanFraction", "outputK1Fraction",
    "outputK2Fraction", "outputTailFraction", "rk4Steps",
    "finiteDimensionalOnly",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path,
                        default=Path(__file__).resolve().parent)
    parser.add_argument("--N", type=int, default=10)
    parser.add_argument("--dt", type=float, default=0.0025)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def emit(path: Path, sequence: int, event: str, **payload: object) -> None:
    record = {"sequence": sequence, "event": event, **payload}
    line = json.dumps(record, sort_keys=True, ensure_ascii=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
    print(line, flush=True)


def modes_for(n_cut: int) -> np.ndarray:
    return np.arange(-n_cut, n_cut + 1, dtype=int)


def w_fourier(d_value: float) -> dict[int, complex]:
    """Fourier coefficients of W=-e^-d sin(x)/2+e^-4d sin(2x)/4."""
    return {
        -2: 1j * math.exp(-4.0 * d_value) / 8.0,
        -1: -1j * math.exp(-d_value) / 4.0,
        1: 1j * math.exp(-d_value) / 4.0,
        2: -1j * math.exp(-4.0 * d_value) / 8.0,
    }


def hr_generator(n_cut: int, mu: float, c: float,
                 d_value: float) -> np.ndarray:
    """Fourier matrix for the exact R0.73A (h,r) equations at beta=0."""
    modes = modes_for(n_cut)
    zero = n_cut
    w = w_fourier(d_value)
    matrix = np.zeros((len(modes), len(modes)), dtype=np.complex128)
    for row, n_mode in enumerate(modes):
        if n_mode == 0:
            matrix[row, row] = -mu
            for column, m_mode in enumerate(modes):
                if m_mode != 0:
                    matrix[row, column] = (
                        -1j * c * w.get(-int(m_mode), 0j)
                        / (m_mode * m_mode + mu)
                    )
            continue
        matrix[row, row] = -(n_mode * n_mode + mu)
        matrix[row, zero] += (
            -1j * c * w.get(int(n_mode), 0j)
            * (mu - n_mode * n_mode)
        )
        for column, m_mode in enumerate(modes):
            if m_mode == 0:
                continue
            shift = int(n_mode - m_mode)
            matrix[row, column] += (
                -1j * c * w.get(shift, 0j)
                * (1.0 - shift * shift / (m_mode * m_mode + mu))
            )
    return matrix


def rk4_propagator(n_cut: int, mu: float, c: float, start: float,
                   end: float, dt_max: float) -> tuple[np.ndarray, int]:
    dimension = 2 * n_cut + 1
    steps = max(1, math.ceil((end - start) / dt_max))
    dt = (end - start) / steps
    propagator = np.eye(dimension, dtype=np.complex128)
    d_value = start
    for _ in range(steps):
        k1 = hr_generator(n_cut, mu, c, d_value) @ propagator
        k2 = hr_generator(n_cut, mu, c, d_value + dt / 2.0) @ (
            propagator + dt * k1 / 2.0
        )
        k3 = hr_generator(n_cut, mu, c, d_value + dt / 2.0) @ (
            propagator + dt * k2 / 2.0
        )
        k4 = hr_generator(n_cut, mu, c, d_value + dt) @ (
            propagator + dt * k3
        )
        propagator += dt * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
        d_value += dt
    return propagator, steps


def norm_weights(name: str, modes: np.ndarray, mu: float) -> np.ndarray:
    """Square-root energy weights in the (h,r) coordinates."""
    weights = np.ones(len(modes), dtype=float)
    zero = modes == 0
    if name == "raw_q":
        weights[zero] = mu
        return weights
    a_value, b_value = NORM_SPECS[name]
    nonzero = ~zero
    lam = modes[nonzero].astype(float) ** 2 + mu
    weights[nonzero] = mu ** (-a_value / 2.0) * lam ** (-b_value / 2.0)
    return weights


def block_fractions(vector: np.ndarray, modes: np.ndarray) -> dict[str, float]:
    mass = np.abs(vector) ** 2
    total = float(np.sum(mass))
    if total <= 0.0:
        raise RuntimeError("zero singular vector")
    return {
        "MeanFraction": float(np.sum(mass[modes == 0]) / total),
        "K1Fraction": float(np.sum(mass[np.abs(modes) == 1]) / total),
        "K2Fraction": float(np.sum(mass[np.abs(modes) == 2]) / total),
        "TailFraction": float(np.sum(mass[np.abs(modes) >= 3]) / total),
    }


def xmu_primitive(start: float, end: float) -> float:
    return (
        7.0 / 4.0 * (math.exp(-start) - math.exp(-end))
        + 1.0 / 2.0 * (math.exp(-4.0 * start) - math.exp(-4.0 * end))
    )


def wx_primitive(start: float, end: float) -> float:
    """Exact integral of ||W_x||_infinity on the double-harmonic profile."""
    return (
        0.5 * (math.exp(-start) - math.exp(-end))
        + 0.125 * (math.exp(-4.0 * start) - math.exp(-4.0 * end))
    )


def case_grid() -> list[Case]:
    mus = tuple(10.0 ** (-exponent) for exponent in range(2, 9))
    intervals = ((0.0, 0.1), (0.0, 0.75), (0.5, 2.0))
    candidates: list[Case] = []
    for p_value in (0.0, 0.25, 0.5, 0.75, 1.0):
        for sign in (-1, 1):
            for mu in mus:
                for start, end in intervals:
                    candidates.append(Case(
                        "power", f"p{p_value:g}-k1", mu,
                        sign * mu ** p_value, p_value, 1.0, sign, start, end,
                    ))
    for family, p_value, kappas in (
        ("fixed-c", 0.0, (0.25, 1.0, 4.0)),
        ("fixed-Lambda", 0.5, (0.25, 1.0, 4.0, 16.0)),
    ):
        for kappa in kappas:
            for sign in (-1, 1):
                for mu in mus:
                    candidates.append(Case(
                        family, f"p{p_value:g}-k{kappa:g}", mu,
                        sign * kappa * mu ** p_value, p_value, kappa, sign,
                        0.0, 0.75,
                    ))
    # Prefer explicitly named fixed-c/fixed-Lambda cases when grids overlap.
    rank = {"power": 0, "fixed-c": 1, "fixed-Lambda": 1}
    unique: dict[tuple[float, float, float, float], Case] = {}
    for case in candidates:
        key = (case.mu, case.c, case.start, case.end)
        if key not in unique or rank[case.family] > rank[unique[key].family]:
            unique[key] = case
    return sorted(unique.values(), key=lambda item: (
        item.start, item.end, item.p, item.kappa, item.sign, item.mu,
    ))


def measure(case_id: str, case: Case, n_cut: int,
            propagator: np.ndarray, steps: int) -> list[dict[str, object]]:
    modes = modes_for(n_cut)
    tau = case.end - case.start
    lam = case.c / math.sqrt(case.mu)
    rows: list[dict[str, object]] = []
    for name, (a_value, b_value) in NORM_SPECS.items():
        weights = norm_weights(name, modes, case.mu)
        weighted = weights[:, None] * propagator / weights[None, :]
        left, singular, right_h = np.linalg.svd(weighted, full_matrices=False)
        gain = float(singular[0])
        input_parts = block_fractions(right_h.conj().T[:, 0], modes)
        output_parts = block_fractions(left[:, 0], modes)
        kinetic_bound = -case.mu * tau + abs(lam) * wx_primitive(
            case.start, case.end
        ) / 2.0
        rows.append({
            "caseId": case_id,
            "family": case.family,
            "pathId": case.path_id,
            "N": n_cut,
            "dimension": len(modes),
            "start": case.start,
            "end": case.end,
            "tau": tau,
            "mu": case.mu,
            "gammaAbs": math.sqrt(case.mu),
            "c": case.c,
            "Lambda": lam,
            "p": case.p,
            "kappa": case.kappa,
            "sign": case.sign,
            "norm": name,
            "muWeightExponentA": a_value,
            "laplacianWeightExponentB": b_value,
            "gain": gain,
            "logGain": math.log(gain),
            "xmuLogBound": -case.mu * tau + abs(case.c) * xmu_primitive(
                case.start, case.end
            ),
            "kineticLogBound": kinetic_bound,
            "boundMargin": kinetic_bound - math.log(gain),
            **{f"input{key}": value for key, value in input_parts.items()},
            **{f"output{key}": value for key, value in output_parts.items()},
            "rk4Steps": steps,
            "finiteDimensionalOnly": True,
        })
    return rows


def fitted_exponent(rows: list[dict[str, object]], norm: str,
                    path_id: str, start: float, end: float,
                    sign: int) -> dict[str, object] | None:
    subset = sorted((
        row for row in rows
        if row["norm"] == norm and row["pathId"] == path_id
        and row["start"] == start and row["end"] == end
        and row["sign"] == sign
    ), key=lambda row: float(row["mu"]))[:4]
    if len(subset) != 4:
        return None
    x_values = np.log([float(row["mu"]) for row in subset])
    y_values = np.log([float(row["gain"]) for row in subset])
    slope, intercept = np.polyfit(x_values, y_values, 1)
    fitted = slope * x_values + intercept
    residual = float(np.sum((y_values - fitted) ** 2))
    total = float(np.sum((y_values - np.mean(y_values)) ** 2))
    return {
        "norm": norm,
        "pathId": path_id,
        "start": start,
        "end": end,
        "sign": sign,
        "muRange": [float(subset[0]["mu"]), float(subset[-1]["mu"])],
        "logGainVsLogMuSlope": float(slope),
        "divergenceExponent": float(max(0.0, -slope)),
        "rSquared": 1.0 if total == 0.0 else 1.0 - residual / total,
        "gainAtSmallestMu": float(subset[0]["gain"]),
        "inputMeanFractionAtSmallestMu": float(
            subset[0]["inputMeanFraction"]
        ),
    }


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    fits: list[dict[str, object]] = []
    for norm in NORM_SPECS:
        for path_id in sorted({str(row["pathId"]) for row in rows}):
            for start, end in sorted({
                (float(row["start"]), float(row["end"])) for row in rows
            }):
                for sign in (-1, 1):
                    fit = fitted_exponent(rows, norm, path_id, start, end, sign)
                    if fit is not None:
                        fits.append(fit)
    positive = {
        (row["mu"], abs(float(row["c"])), row["start"], row["end"],
         row["norm"]): row
        for row in rows if int(row["sign"]) == 1
    }
    symmetry_errors = []
    for negative in (row for row in rows if int(row["sign"]) == -1):
        key = (negative["mu"], abs(float(negative["c"])), negative["start"],
               negative["end"], negative["norm"])
        match = positive.get(key)
        if match is not None:
            denominator = max(float(match["gain"]), float(negative["gain"]),
                              1e-300)
            symmetry_errors.append(
                abs(float(match["gain"]) - float(negative["gain"]))
                / denominator
            )
    kinetic_rows = [row for row in rows if row["norm"] == "kinetic"]
    return {
        "schemaVersion": 1,
        "status": "completed",
        "scope": "finite Fourier-Galerkin nonautonomous weighted-norm screen",
        "finiteDimensionalOnly": True,
        "caseCount": len({str(row["caseId"]) for row in rows}),
        "rowCount": len(rows),
        "norms": list(NORM_SPECS),
        "fits": fits,
        "maximumSignOrientationRelativeDifference": max(
            symmetry_errors, default=0.0
        ),
        "kineticFiniteBoundViolations": sum(
            float(row["logGain"]) > float(row["kineticLogBound"]) + 5e-8
            for row in kinetic_rows
        ),
        "minimumFiniteKineticBoundMargin": min(
            float(row["boundMargin"]) for row in kinetic_rows
        ),
    }


def main() -> int:
    args = parse_args()
    if args.N < 4:
        raise ValueError("N must be at least 4")
    if args.dt <= 0.0:
        raise ValueError("dt must be positive")
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    names = (
        "weighted_propagator_rows.csv", "summary.json", "environment.json",
        "manifest.json", "progress.ndjson",
    )
    paths = {name: out / name for name in names}
    if not args.overwrite and any(path.exists() for path in paths.values()):
        raise RuntimeError("output exists; use --overwrite")
    for path in paths.values():
        if path.exists():
            path.unlink()

    grid = case_grid()
    emit(paths["progress.ndjson"], 0, "start", N=args.N, dt=args.dt,
         caseCount=len(grid), normCount=len(NORM_SPECS))
    rows: list[dict[str, object]] = []
    for index, case in enumerate(grid, start=1):
        propagator, steps = rk4_propagator(
            args.N, case.mu, case.c, case.start, case.end, args.dt
        )
        rows.extend(measure(f"R073B-W{index:04d}", case, args.N,
                            propagator, steps))
        if index % 20 == 0 or index == len(grid):
            emit(paths["progress.ndjson"], index, "progress",
                 completed=index, total=len(grid), rowCount=len(rows))

    with paths["weighted_propagator_rows.csv"].open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = summarize(rows)
    paths["summary.json"].write_text(canonical(summary), encoding="utf-8")
    environment = {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "cpuCount": os.cpu_count(),
        "randomness": "none",
        "threadPolicy": "caller requests one BLAS/OpenMP thread",
        "sourceLineage": "R0.73A hidden-mean coordinates",
    }
    paths["environment.json"].write_text(canonical(environment), encoding="utf-8")
    emit(paths["progress.ndjson"], len(grid) + 1, "complete",
         rowCount=len(rows), summarySha256=sha256(paths["summary.json"]))

    manifest = {
        "schemaVersion": 1,
        "status": "completed",
        "finiteDimensionalOnly": True,
        "source": "weighted_kinetic_screen.py",
        "sourceSha256": sha256(Path(__file__).resolve()),
        "validator": "validate_weighted_kinetic_screen.py",
        "configuration": {
            "N": args.N,
            "dtMax": args.dt,
            "caseCount": len(grid),
            "normCount": len(NORM_SPECS),
        },
        "limitations": [
            "finite Fourier-Galerkin matrices only; no tail enclosure",
            "fixed-step complex128 RK4; no interval arithmetic",
            "sampled paths do not prove parameter-uniform operator estimates",
            "only the beta=xi=0 Orr--Sommerfeld row is integrated",
            "Squire lift-up, Bloch direct sums, and nonlinear convolution are absent",
        ],
        "outputs": [],
    }
    for name in (
        "weighted_propagator_rows.csv", "summary.json", "environment.json",
        "progress.ndjson",
    ):
        path = paths[name]
        manifest["outputs"].append({
            "path": name,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    paths["manifest.json"].write_text(canonical(manifest), encoding="utf-8")
    print(canonical(summary), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
