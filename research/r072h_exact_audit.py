#!/usr/bin/env python3
"""Producer audit for R0.72H.

The analytic theorem is in r072h_report-source.md. This script provides
finite corroboration using the original complex Fourier lattice, a
Rudin--Shapiro polynomial recurrence, DOP853 evolution, Simpson quadrature,
and a direct optimization of the reciprocal critical-log envelope.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import platform
import resource
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import scipy
from scipy.integrate import simpson, solve_ivp
from scipy.optimize import minimize_scalar


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_ndjson(path: Path, payload: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def rss_mb() -> float:
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        return float(usage) / 1024.0 / 1024.0
    return float(usage) / 1024.0


def rudin_shapiro_recurrence(M: int) -> np.ndarray:
    if M < 1 or M & (M - 1):
        raise ValueError("M must be a positive power of two")
    p = np.array([1], dtype=np.int8)
    q = np.array([1], dtype=np.int8)
    while p.size < M:
        p_old = p
        q_old = q
        p = np.concatenate((p_old, q_old))
        q = np.concatenate((p_old, -q_old))
    return p


def critical_weight(s: np.ndarray) -> np.ndarray:
    out = np.empty_like(s, dtype=np.float64)
    positive = s > 0.0
    out[positive] = np.power(s[positive], -1.0 / 3.0) * (
        1.0 + np.log(1.0 / s[positive])
    )
    out[~positive] = np.inf
    return out


def envelope_phi(alpha: float) -> tuple[float, float]:
    upper = max(50.0, math.log1p(alpha) + 30.0)

    def negative_log_phi(u: float) -> float:
        return u / 3.0 + alpha * math.exp(-u) + math.log1p(u)

    result = minimize_scalar(
        negative_log_phi,
        bounds=(0.0, upper),
        method="bounded",
        options={"xatol": 1.0e-13},
    )
    u_star = float(result.x)
    return math.exp(-negative_log_phi(u_star)), math.exp(-u_star)


@dataclass
class ComplexLattice:
    M: int
    amplitude: float
    delta: float
    mu: float
    truncation_factor: int

    def __post_init__(self) -> None:
        self.signs = rudin_shapiro_recurrence(self.M).astype(np.float64)
        self.carriers = (
            2 * self.M + 2 * np.arange(self.M, dtype=np.int64) + 1
        )
        self.radius = self.truncation_factor * self.M
        if int(self.carriers[-1]) * 2 > self.radius:
            raise ValueError("truncation must include the one-coupling outer band")
        self.modes = np.arange(-self.radius, self.radius + 1, dtype=np.float64)
        self.zero = self.radius
        self.dimension = self.modes.size
        self.lambdas = self.modes**2 + self.mu
        self.scale = float(self.M * self.M)

    def apply_v(self, y: float, state: np.ndarray) -> np.ndarray:
        x = y / self.scale
        out = np.zeros_like(state, dtype=np.complex128)
        factors = (
            -1j
            * self.amplitude
            * self.signs
            * np.exp(-(self.carriers.astype(np.float64) ** 2) * x)
        )
        for shift, coefficient in zip(self.carriers, factors, strict=True):
            k = int(shift)
            out[k:] += coefficient * state[:-k]
            out[:-k] += coefficient * state[k:]
        return out

    def rhs(self, y: float, state: np.ndarray) -> np.ndarray:
        return (
            -self.lambdas * state + self.delta * self.apply_v(y, state)
        ) / self.scale

    def solve(
        self,
        initial: np.ndarray,
        y_end: float,
        t_eval: np.ndarray | None = None,
        *,
        rtol: float,
        atol: float,
    ) -> Any:
        return solve_ivp(
            self.rhs,
            (0.0, float(y_end)),
            initial,
            method="DOP853",
            t_eval=t_eval,
            rtol=rtol,
            atol=atol,
        )

    def aligned_launch(self) -> np.ndarray:
        state = np.zeros(self.dimension, dtype=np.complex128)
        coefficient = 1j / math.sqrt(2.0)
        for carrier, sign in zip(self.carriers, self.signs, strict=True):
            state[self.zero + int(carrier)] = coefficient * sign
            state[self.zero - int(carrier)] = coefficient * sign
        return state

    def q_row(self, y: float, state: np.ndarray) -> complex:
        x = y / self.scale
        factors = (
            2j
            * self.amplitude
            * self.signs
            * (self.carriers.astype(np.float64) ** 2)
            * np.exp(-(self.carriers.astype(np.float64) ** 2) * x)
        )
        values = state[self.zero - self.carriers] + state[
            self.zero + self.carriers
        ]
        return complex(np.sum(factors * values))

    def observations(
        self, y_values: np.ndarray, states: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        h = np.empty(y_values.size, dtype=np.complex128)
        qf = np.empty(y_values.size, dtype=np.complex128)
        action_density = np.empty(y_values.size, dtype=np.float64)
        for column, y in enumerate(y_values):
            state = states[:, column]
            z = self.apply_v(float(y), state)
            h[column] = z[self.zero]
            qf[column] = self.q_row(float(y), state)
            action_density[column] = float(
                np.sum(np.abs(z) ** 2 / self.lambdas)
            )
        return h, qf, action_density


def build_corrected_launch(
    lattice: ComplexLattice, rtol: float, atol: float
) -> tuple[np.ndarray, complex, float, float, complex]:
    y_tau = 1.0 / lattice.M
    e0 = np.zeros(lattice.dimension, dtype=np.complex128)
    e0[lattice.zero] = 1.0
    g = lattice.aligned_launch()
    col_a = lattice.solve(e0, y_tau, np.array([y_tau]), rtol=rtol, atol=atol)
    col_b = lattice.solve(g, y_tau, np.array([y_tau]), rtol=rtol, atol=atol)
    if not col_a.success or not col_b.success:
        raise RuntimeError("root-column evolution failed")
    A = complex(col_a.y[lattice.zero, -1])
    B = complex(col_b.y[lattice.zero, -1])
    zeta = -B / A
    raw_launch = g + zeta * e0
    normalization = math.sqrt(lattice.M) / float(np.linalg.norm(raw_launch))
    launch = normalization * raw_launch
    residual = normalization * (B + zeta * A)
    return launch, zeta, abs(residual), abs(A), B


def integrate_case(
    M: int,
    args: argparse.Namespace,
    progress_path: Path,
    resource_path: Path,
) -> dict[str, Any]:
    started = time.perf_counter()
    lattice = ComplexLattice(
        M=M,
        amplitude=args.amplitude,
        delta=args.delta,
        mu=args.mu,
        truncation_factor=args.truncation_factor,
    )
    launch, zeta, root_residual, root_column, B = build_corrected_launch(
        lattice, args.rtol, args.atol
    )

    z_max = args.y_max ** (1.0 / 3.0)
    z_grid = np.linspace(0.0, z_max, args.quad_points)
    y_grid = z_grid**3
    solution = lattice.solve(
        launch,
        args.y_max,
        y_grid,
        rtol=args.rtol,
        atol=args.atol,
    )
    if not solution.success:
        raise RuntimeError(f"DOP853 failed for M={M}: {solution.message}")
    h, qf, q_density = lattice.observations(y_grid, solution.y)

    jacobian = 3.0 * z_grid**2 / lattice.scale
    x_values = y_grid / lattice.scale
    weights = critical_weight(x_values / args.window)
    eq_integrand = np.abs(h * qf) * jacobian
    action_integrand = np.zeros_like(z_grid)
    reciprocal_integrand = np.zeros_like(z_grid)
    positive = z_grid > 0.0
    action_integrand[positive] = (
        weights[positive] * q_density[positive] * jacobian[positive]
    )
    reciprocal_integrand[positive] = (
        np.abs(qf[positive]) ** 2
        / weights[positive]
        * jacobian[positive]
    )
    eq_value = float(simpson(eq_integrand, x=z_grid))
    q_star = float(simpson(action_integrand, x=z_grid))
    reciprocal = float(simpson(reciprocal_integrand, x=z_grid))

    moment_terms: list[float] = []
    phi_maximizers: list[float] = []
    for carrier in lattice.carriers.astype(np.float64):
        phi, s_star = envelope_phi(2.0 * args.window * carrier * carrier)
        moment_terms.append(carrier * carrier * args.amplitude**2 * phi)
        phi_maximizers.append(s_star)
    moment = float(sum(moment_terms))

    y_tau = 1.0 / M
    root_state = lattice.solve(
        launch,
        y_tau,
        np.array([y_tau]),
        rtol=args.rtol,
        atol=args.atol,
    )
    if not root_state.success:
        raise RuntimeError(f"root-state evolution failed for M={M}")
    root_vector = root_state.y[:, -1]
    root_target = complex(root_vector[lattice.zero])
    root_h = complex(lattice.apply_v(y_tau, root_vector)[lattice.zero])

    expected_q = args.amplitude**2 * M ** (2.0 / 3.0) * math.log(M)
    expected_m = args.amplitude**2 * M ** (7.0 / 3.0) / math.log(M)
    expected_eq = args.amplitude**2 * M**2
    expected_reciprocal = (
        args.amplitude**2 * M ** (10.0 / 3.0) / math.log(M)
    )
    scale_rhs = math.sqrt(args.mu * M * moment * q_star)
    elapsed = time.perf_counter() - started
    result = {
        "M": M,
        "dimension": lattice.dimension,
        "carrierMin": int(lattice.carriers[0]),
        "carrierMax": int(lattice.carriers[-1]),
        "zetaReal": float(zeta.real),
        "zetaImag": float(zeta.imag),
        "zetaScaled": float(abs(zeta) * M**2 / args.amplitude),
        "rootColumnAbs": root_column,
        "rootColumnBAbs": float(abs(B)),
        "algebraicRootResidual": root_residual,
        "evolvedRootResidual": float(abs(root_target)),
        "rootH": float(abs(root_h)),
        "rootHNormalized": float(abs(root_h) / (args.amplitude * M)),
        "mixedRow": eq_value,
        "criticalAction": q_star,
        "profileMoment": moment,
        "reciprocalMoment": reciprocal,
        "mixedRowNormalized": eq_value / expected_eq,
        "criticalActionNormalized": q_star / expected_q,
        "profileMomentNormalized": moment / expected_m,
        "reciprocalMomentNormalized": reciprocal / expected_reciprocal,
        "momentResolvedRatio": scale_rhs / eq_value,
        "actionOnlyScaledRatio": (
            (eq_value / q_star) / (M ** (4.0 / 3.0) / math.log(M))
        ),
        "phiMaximizerMin": float(min(phi_maximizers)),
        "phiMaximizerMax": float(max(phi_maximizers)),
        "solverNfev": int(solution.nfev),
        "elapsedSeconds": elapsed,
        "maxRssMb": rss_mb(),
    }
    append_ndjson(
        progress_path,
        {
            "time": utc_now(),
            "event": "case_complete",
            "M": M,
            "mixedRowNormalized": result["mixedRowNormalized"],
            "criticalActionNormalized": result["criticalActionNormalized"],
            "profileMomentNormalized": result["profileMomentNormalized"],
            "rootResidual": result["evolvedRootResidual"],
        },
    )
    append_ndjson(
        resource_path,
        {
            "time": utc_now(),
            "M": M,
            "elapsedSeconds": elapsed,
            "maxRssMb": result["maxRssMb"],
            "solverNfev": result["solverNfev"],
            "dimension": lattice.dimension,
        },
    )
    print(
        f"M={M:>3d} dim={lattice.dimension:>4d} "
        f"EQ/(a^2M^2)={result['mixedRowNormalized']:.6g} "
        f"Qnorm={result['criticalActionNormalized']:.6g} "
        f"mnorm={result['profileMomentNormalized']:.6g} "
        f"root={result['evolvedRootResidual']:.3e}",
        flush=True,
    )
    return result


def fit_slope(
    values: list[dict[str, Any]], key: str, log_adjust: int = 0
) -> float:
    M = np.array([row["M"] for row in values], dtype=np.float64)
    y = np.array([row[key] for row in values], dtype=np.float64)
    if log_adjust:
        y = y * np.log(M) ** log_adjust
    slope, _ = np.polyfit(np.log(M), np.log(y), 1)
    return float(slope)


def envelope_audit() -> dict[str, Any]:
    alphas = np.logspace(-4, 7, 120)
    ratios = []
    maximizers = []
    for alpha in alphas:
        phi, s_star = envelope_phi(float(alpha))
        comparator = (1.0 + alpha) ** (-1.0 / 3.0) / (
            1.0 + math.log(2.0 + alpha)
        )
        ratios.append(phi / comparator)
        maximizers.append(s_star)
    return {
        "alphaMin": float(alphas[0]),
        "alphaMax": float(alphas[-1]),
        "samples": int(alphas.size),
        "ratioMin": float(min(ratios)),
        "ratioMax": float(max(ratios)),
        "maximizerMin": float(min(maximizers)),
        "maximizerMax": float(max(maximizers)),
    }


def write_csv(path: Path, cases: list[dict[str, Any]]) -> None:
    fieldnames = list(cases[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(cases)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return "unavailable"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("research/certificates/r072h"),
    )
    parser.add_argument(
        "--m-values", nargs="+", type=int, default=[4, 8, 16, 32, 64]
    )
    parser.add_argument("--amplitude", type=float, default=1.0)
    parser.add_argument("--delta", type=float, default=1.0)
    parser.add_argument("--mu", type=float, default=1.0)
    parser.add_argument("--window", type=float, default=1.0)
    parser.add_argument("--y-max", type=float, default=12.0)
    parser.add_argument("--quad-points", type=int, default=1001)
    parser.add_argument("--truncation-factor", type=int, default=8)
    parser.add_argument("--rtol", type=float, default=2.0e-10)
    parser.add_argument("--atol", type=float, default=2.0e-12)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    progress_path = args.output_dir / "producer-progress.ndjson"
    resource_path = args.output_dir / "producer-resource.ndjson"
    for path in (progress_path, resource_path):
        path.write_text("", encoding="utf-8")

    config = {
        "audit": "R0.72H producer",
        "date": "2026-08-27",
        "mValues": args.m_values,
        "amplitude": args.amplitude,
        "delta": args.delta,
        "mu": args.mu,
        "window": args.window,
        "yMax": args.y_max,
        "quadPoints": args.quad_points,
        "truncationFactor": args.truncation_factor,
        "rtol": args.rtol,
        "atol": args.atol,
        "carrierRule": "r_j=2M+2j+1",
        "signGenerator": "Rudin-Shapiro polynomial recurrence",
        "solver": "SciPy solve_ivp DOP853 on y=M^2 x",
        "quadrature": "Simpson after y=z^3",
    }
    (args.output_dir / "config.json").write_text(
        json.dumps(config, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (args.output_dir / "seed.txt").write_text(
        "deterministic:no-random-seed\n", encoding="utf-8"
    )
    append_ndjson(
        progress_path,
        {"time": utc_now(), "event": "audit_start", "config": config},
    )

    cases = [
        integrate_case(M, args, progress_path, resource_path)
        for M in args.m_values
    ]
    envelope = envelope_audit()
    slopes = {
        "mixedRow": fit_slope(cases, "mixedRow"),
        "criticalActionDivLog": fit_slope(
            cases, "criticalAction", log_adjust=-1
        ),
        "profileMomentTimesLog": fit_slope(
            cases, "profileMoment", log_adjust=1
        ),
        "actionOnlyTimesLog": fit_slope(
            [
                {**row, "ratio": row["mixedRow"] / row["criticalAction"]}
                for row in cases
            ],
            "ratio",
            log_adjust=1,
        ),
    }
    checks = {
        "allOddCarriers": all(
            row["carrierMin"] % 2 == 1 and row["carrierMax"] % 2 == 1
            for row in cases
        ),
        "realCorrection": max(abs(row["zetaImag"]) for row in cases) < 1.0e-8,
        "exactInteriorRoot": max(
            row["evolvedRootResidual"] for row in cases
        ) < 2.0e-8,
        "noncollapsedRootSlope": (
            cases[-1]["rootHNormalized"] > 0.7
            and all(
                right["rootHNormalized"] > left["rootHNormalized"]
                for left, right in zip(cases, cases[1:])
            )
        ),
        "mixedRowSlope": abs(slopes["mixedRow"] - 2.0) < 0.20,
        "criticalActionSlope": abs(
            slopes["criticalActionDivLog"] - 2.0 / 3.0
        ) < 0.36,
        "profileMomentSlope": abs(
            slopes["profileMomentTimesLog"] - 7.0 / 3.0
        ) < 0.30,
        "actionOnlyDivergenceSlope": abs(
            slopes["actionOnlyTimesLog"] - 4.0 / 3.0
        ) < 0.36,
        "momentResolvedRatioFinite": max(
            row["momentResolvedRatio"] for row in cases
        ) / min(row["momentResolvedRatio"] for row in cases)
        < 3.0,
        "envelopeComparator": (
            envelope["ratioMin"] > 0.05 and envelope["ratioMax"] < 20.0
        ),
    }
    passed = all(checks.values())
    result = {
        "schemaVersion": 1,
        "audit": "R0.72H producer",
        "status": "passed" if passed else "failed",
        "generatedAt": utc_now(),
        "gitCommit": git_commit(),
        "config": config,
        "envelopeAudit": envelope,
        "slopes": slopes,
        "checks": checks,
        "cases": cases,
        "limitations": [
            "finite truncated lattices do not prove the analytic theorem",
            "the dynamic integral stops at y=12 where the heat envelope is exponentially small",
            "the audit tests the triangular 2.5D class only",
        ],
    }
    result_path = args.output_dir / "result.json"
    result_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_csv(args.output_dir / "producer-data.csv", cases)
    environment = {
        "generatedAt": utc_now(),
        "python": sys.version,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "executable": sys.executable,
        "cpuCount": os.cpu_count(),
        "maxRssMb": rss_mb(),
    }
    (args.output_dir / "environment.txt").write_text(
        "\n".join(f"{key}={value}" for key, value in environment.items()) + "\n",
        encoding="utf-8",
    )
    append_ndjson(
        progress_path,
        {
            "time": utc_now(),
            "event": "audit_complete",
            "status": result["status"],
            "checks": checks,
        },
    )
    monitored = {
        "status": result["status"],
        "cases": len(cases),
        "maxRssMb": rss_mb(),
        "resultSha256": sha256(result_path),
    }
    (args.output_dir / "producer-monitor.log").write_text(
        json.dumps(monitored, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(monitored, sort_keys=True), flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
