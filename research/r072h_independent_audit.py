#!/usr/bin/env python3
"""Independent finite audit for R0.72H.

This checker uses the real all-odd gauge, a binary-parity definition of the
Rudin--Shapiro signs, RK45, and Gauss--Legendre quadrature. It intentionally
does not import the producer implementation.
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
from numpy.polynomial.legendre import leggauss
from scipy.integrate import solve_ivp


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def append(path: Path, payload: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def rss_mb() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return float(value) / (1024.0 * 1024.0 if sys.platform == "darwin" else 1024.0)


def binary_rudin_shapiro(M: int) -> np.ndarray:
    if M < 1 or M & (M - 1):
        raise ValueError("M must be a power of two")
    signs = np.empty(M, dtype=np.float64)
    for n in range(M):
        adjacent_ones = (n & (n >> 1)).bit_count()
        signs[n] = -1.0 if adjacent_ones % 2 else 1.0
    return signs


def real_power_of_i(exponent: int) -> float:
    if exponent % 2:
        raise ValueError("expected an even power of i")
    return -1.0 if (exponent // 2) % 2 else 1.0


def grid_phi(alpha: float) -> float:
    upper = max(45.0, math.log1p(alpha) + 25.0)
    u = np.linspace(0.0, upper, 24001)
    log_values = -u / 3.0 - alpha * np.exp(-u) - np.log1p(u)
    return float(np.exp(np.max(log_values)))


@dataclass
class RealGaugeLattice:
    M: int
    amplitude: float
    delta: float
    mu: float
    truncation_factor: int

    def __post_init__(self) -> None:
        self.signs = binary_rudin_shapiro(self.M)
        self.carriers = (
            2 * self.M + 2 * np.arange(self.M, dtype=np.int64) + 1
        )
        self.sigma = np.array(
            [
                real_power_of_i((int(carrier) - 1))
                for carrier in self.carriers
            ],
            dtype=np.float64,
        )
        self.radius = self.truncation_factor * self.M
        if 2 * int(self.carriers[-1]) > self.radius:
            raise ValueError("truncation misses the first outer interaction band")
        self.modes = np.arange(-self.radius, self.radius + 1, dtype=np.float64)
        self.lambdas = self.modes**2 + self.mu
        self.zero = self.radius
        self.dimension = self.modes.size
        self.scale = float(self.M * self.M)

    def v(self, y: float, state: np.ndarray) -> np.ndarray:
        x = y / self.scale
        factors = (
            self.amplitude
            * self.signs
            * self.sigma
            * np.exp(-(self.carriers.astype(np.float64) ** 2) * x)
        )
        out = np.zeros_like(state)
        for carrier, factor in zip(self.carriers, factors, strict=True):
            shift = int(carrier)
            out[shift:] += factor * state[:-shift]
            out[:-shift] -= factor * state[shift:]
        return out

    def rhs(self, y: float, state: np.ndarray) -> np.ndarray:
        return (-self.lambdas * state + self.delta * self.v(y, state)) / self.scale

    def solve(
        self,
        initial: np.ndarray,
        y_end: float,
        *,
        t_eval: np.ndarray | None,
        rtol: float,
        atol: float,
    ) -> Any:
        return solve_ivp(
            self.rhs,
            (0.0, float(y_end)),
            initial,
            method="RK45",
            t_eval=t_eval,
            rtol=rtol,
            atol=atol,
        )

    def launch(self) -> np.ndarray:
        state = np.zeros(self.dimension, dtype=np.float64)
        for carrier, epsilon in zip(self.carriers, self.signs, strict=True):
            k = int(carrier)
            state[self.zero + k] = (
                epsilon * real_power_of_i(k + 1) / math.sqrt(2.0)
            )
            state[self.zero - k] = (
                epsilon * real_power_of_i(1 - k) / math.sqrt(2.0)
            )
        return state

    def q_row(self, y: float, state: np.ndarray) -> float:
        x = y / self.scale
        factors = (
            -2.0
            * self.amplitude
            * self.signs
            * self.sigma
            * (self.carriers.astype(np.float64) ** 2)
            * np.exp(-(self.carriers.astype(np.float64) ** 2) * x)
        )
        difference = (
            state[self.zero - self.carriers]
            - state[self.zero + self.carriers]
        )
        return float(np.sum(factors * difference))


def corrected_launch(
    lattice: RealGaugeLattice, rtol: float, atol: float
) -> tuple[np.ndarray, float, float]:
    y_tau = 1.0 / lattice.M
    e0 = np.zeros(lattice.dimension)
    e0[lattice.zero] = 1.0
    g = lattice.launch()
    a_solution = lattice.solve(
        e0, y_tau, t_eval=np.array([y_tau]), rtol=rtol, atol=atol
    )
    b_solution = lattice.solve(
        g, y_tau, t_eval=np.array([y_tau]), rtol=rtol, atol=atol
    )
    if not a_solution.success or not b_solution.success:
        raise RuntimeError("independent root-column solve failed")
    A = float(a_solution.y[lattice.zero, -1])
    B = float(b_solution.y[lattice.zero, -1])
    zeta = -B / A
    raw = g + zeta * e0
    normalization = math.sqrt(lattice.M) / float(np.linalg.norm(raw))
    launch = normalization * raw
    return launch, zeta, abs(normalization * (B + zeta * A))


def gauss_nodes(order: int, y_max: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    nodes, weights = leggauss(order)
    z_max = y_max ** (1.0 / 3.0)
    z = 0.5 * z_max * (nodes + 1.0)
    z_weights = 0.5 * z_max * weights
    return z, z**3, z_weights


def run_case(
    M: int,
    args: argparse.Namespace,
    progress: Path,
    resources: Path,
) -> dict[str, Any]:
    started = time.perf_counter()
    lattice = RealGaugeLattice(
        M,
        args.amplitude,
        args.delta,
        args.mu,
        args.truncation_factor,
    )
    launch, zeta, algebraic_residual = corrected_launch(
        lattice, args.rtol, args.atol
    )
    z, y, gauss_weights = gauss_nodes(args.quad_order, args.y_max)
    solution = lattice.solve(
        launch,
        args.y_max,
        t_eval=y,
        rtol=args.rtol,
        atol=args.atol,
    )
    if not solution.success:
        raise RuntimeError(f"independent RK45 failed at M={M}")

    h = np.empty(y.size)
    qf = np.empty(y.size)
    q_density = np.empty(y.size)
    for column, y_value in enumerate(y):
        state = solution.y[:, column]
        vf = lattice.v(float(y_value), state)
        h[column] = vf[lattice.zero]
        qf[column] = lattice.q_row(float(y_value), state)
        q_density[column] = float(np.sum(vf * vf / lattice.lambdas))

    x = y / lattice.scale
    jacobian = 3.0 * z**2 / lattice.scale
    critical = np.power(x / args.window, -1.0 / 3.0) * (
        1.0 + np.log(args.window / x)
    )
    mixed_row = float(np.sum(gauss_weights * jacobian * np.abs(h * qf)))
    action = float(np.sum(gauss_weights * jacobian * critical * q_density))
    reciprocal = float(
        np.sum(gauss_weights * jacobian * qf * qf / critical)
    )

    moment = 0.0
    for carrier in lattice.carriers.astype(np.float64):
        moment += (
            carrier**2
            * args.amplitude**2
            * grid_phi(2.0 * args.window * carrier**2)
        )

    y_tau = 1.0 / M
    root_solution = lattice.solve(
        launch,
        y_tau,
        t_eval=np.array([y_tau]),
        rtol=args.rtol,
        atol=args.atol,
    )
    root_state = root_solution.y[:, -1]
    root_residual = abs(float(root_state[lattice.zero]))
    root_h = abs(float(lattice.v(y_tau, root_state)[lattice.zero]))

    expected_eq = args.amplitude**2 * M**2
    expected_q = args.amplitude**2 * M ** (2.0 / 3.0) * math.log(M)
    expected_m = args.amplitude**2 * M ** (7.0 / 3.0) / math.log(M)
    expected_reciprocal = (
        args.amplitude**2 * M ** (10.0 / 3.0) / math.log(M)
    )
    elapsed = time.perf_counter() - started
    row = {
        "M": M,
        "dimension": lattice.dimension,
        "carrierMin": int(lattice.carriers[0]),
        "carrierMax": int(lattice.carriers[-1]),
        "zeta": zeta,
        "zetaScaled": abs(zeta) * M**2 / args.amplitude,
        "algebraicRootResidual": algebraic_residual,
        "evolvedRootResidual": root_residual,
        "rootHNormalized": root_h / (args.amplitude * M),
        "mixedRow": mixed_row,
        "criticalAction": action,
        "profileMoment": moment,
        "reciprocalMoment": reciprocal,
        "mixedRowNormalized": mixed_row / expected_eq,
        "criticalActionNormalized": action / expected_q,
        "profileMomentNormalized": moment / expected_m,
        "reciprocalMomentNormalized": reciprocal / expected_reciprocal,
        "momentResolvedRatio": math.sqrt(args.mu * M * moment * action)
        / mixed_row,
        "actionOnlyScaledRatio": (mixed_row / action)
        / (M ** (4.0 / 3.0) / math.log(M)),
        "solverNfev": int(solution.nfev),
        "elapsedSeconds": elapsed,
        "maxRssMb": rss_mb(),
    }
    append(
        progress,
        {
            "time": utc_now(),
            "event": "case_complete",
            "M": M,
            "mixedRowNormalized": row["mixedRowNormalized"],
            "criticalActionNormalized": row["criticalActionNormalized"],
            "profileMomentNormalized": row["profileMomentNormalized"],
            "rootResidual": row["evolvedRootResidual"],
        },
    )
    append(
        resources,
        {
            "time": utc_now(),
            "M": M,
            "dimension": lattice.dimension,
            "solverNfev": row["solverNfev"],
            "elapsedSeconds": elapsed,
            "maxRssMb": row["maxRssMb"],
        },
    )
    print(
        f"independent M={M:>3d} dim={lattice.dimension:>4d} "
        f"EQnorm={row['mixedRowNormalized']:.6g} "
        f"Qnorm={row['criticalActionNormalized']:.6g} "
        f"mnorm={row['profileMomentNormalized']:.6g} "
        f"root={row['evolvedRootResidual']:.3e}",
        flush=True,
    )
    return row


def slope(cases: list[dict[str, Any]], key: str, log_power: int = 0) -> float:
    M = np.array([row["M"] for row in cases], dtype=np.float64)
    values = np.array([row[key] for row in cases], dtype=np.float64)
    values *= np.log(M) ** log_power
    return float(np.polyfit(np.log(M), np.log(values), 1)[0])


def relative_error(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return "unavailable"


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("research/certificates/r072h"),
    )
    parser.add_argument("--producer-result", type=Path, default=None)
    parser.add_argument(
        "--m-values", nargs="+", type=int, default=[4, 8, 16, 32, 64]
    )
    parser.add_argument("--amplitude", type=float, default=1.0)
    parser.add_argument("--delta", type=float, default=1.0)
    parser.add_argument("--mu", type=float, default=1.0)
    parser.add_argument("--window", type=float, default=1.0)
    parser.add_argument("--y-max", type=float, default=12.0)
    parser.add_argument("--quad-order", type=int, default=280)
    parser.add_argument("--truncation-factor", type=int, default=9)
    parser.add_argument("--rtol", type=float, default=5.0e-10)
    parser.add_argument("--atol", type=float, default=5.0e-12)
    return parser.parse_args()


def main() -> int:
    args = arguments()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.producer_result is None:
        args.producer_result = args.output_dir / "result.json"
    progress = args.output_dir / "independent-progress.ndjson"
    resources = args.output_dir / "independent-resource.ndjson"
    progress.write_text("", encoding="utf-8")
    resources.write_text("", encoding="utf-8")
    config = {
        "audit": "R0.72H independent",
        "mValues": args.m_values,
        "amplitude": args.amplitude,
        "delta": args.delta,
        "mu": args.mu,
        "window": args.window,
        "yMax": args.y_max,
        "quadOrder": args.quad_order,
        "truncationFactor": args.truncation_factor,
        "rtol": args.rtol,
        "atol": args.atol,
        "signGenerator": "binary parity of overlapping adjacent 11",
        "solver": "real-gauge SciPy RK45",
        "quadrature": "Gauss-Legendre after y=z^3",
    }
    (args.output_dir / "independent-config.json").write_text(
        json.dumps(config, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    append(progress, {"time": utc_now(), "event": "audit_start", "config": config})
    cases = [run_case(M, args, progress, resources) for M in args.m_values]

    slopes = {
        "mixedRow": slope(cases, "mixedRow"),
        "criticalActionDivLog": slope(cases, "criticalAction", -1),
        "profileMomentTimesLog": slope(cases, "profileMoment", 1),
        "actionOnlyTimesLog": slope(
            [
                {**row, "ratio": row["mixedRow"] / row["criticalAction"]}
                for row in cases
            ],
            "ratio",
            1,
        ),
    }
    producer = json.loads(args.producer_result.read_text(encoding="utf-8"))
    producer_by_m = {int(row["M"]): row for row in producer["cases"]}
    comparisons = {}
    for row in cases:
        other = producer_by_m[row["M"]]
        comparisons[str(row["M"])] = {
            key: relative_error(row[key], other[key])
            for key in (
                "mixedRow",
                "criticalAction",
                "profileMoment",
                "reciprocalMoment",
                "rootHNormalized",
            )
        }
    max_cross_error = max(
        error
        for group in comparisons.values()
        for error in group.values()
    )
    checks = {
        "allOddCarriers": all(
            row["carrierMin"] % 2 == 1 and row["carrierMax"] % 2 == 1
            for row in cases
        ),
        "exactRealRoot": max(
            row["evolvedRootResidual"] for row in cases
        ) < 5.0e-8,
        "rootSlopeRecovers": (
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
        "momentResolvedStable": max(
            row["momentResolvedRatio"] for row in cases
        )
        / min(row["momentResolvedRatio"] for row in cases)
        < 3.0,
        "producerAgreement": max_cross_error < 2.0e-3,
    }
    passed = all(checks.values())
    result = {
        "schemaVersion": 1,
        "audit": "R0.72H independent",
        "status": "passed" if passed else "failed",
        "generatedAt": utc_now(),
        "gitCommit": git_commit(),
        "config": config,
        "slopes": slopes,
        "checks": checks,
        "producerComparisons": comparisons,
        "maxProducerRelativeError": max_cross_error,
        "cases": cases,
        "limitations": [
            "finite real-gauge truncations do not prove the asymptotic theorem",
            "the audit is restricted to the all-odd sharpness family",
            "agreement with the producer is numerical corroboration only",
        ],
    }
    result_path = args.output_dir / "independent-result.json"
    result_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    with (args.output_dir / "independent-data.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(cases[0].keys()), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(cases)
    append(
        progress,
        {
            "time": utc_now(),
            "event": "audit_complete",
            "status": result["status"],
            "checks": checks,
        },
    )
    monitor = {
        "status": result["status"],
        "cases": len(cases),
        "maxProducerRelativeError": max_cross_error,
        "maxRssMb": rss_mb(),
        "resultSha256": sha256(result_path),
    }
    (args.output_dir / "independent-monitor.log").write_text(
        json.dumps(monitor, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    independent_environment = {
        "generatedAt": utc_now(),
        "python": sys.version,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "executable": sys.executable,
        "cpuCount": os.cpu_count(),
        "maxRssMb": rss_mb(),
    }
    (args.output_dir / "independent-environment.txt").write_text(
        "\n".join(
            f"{key}={value}" for key, value in independent_environment.items()
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(monitor, sort_keys=True), flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
