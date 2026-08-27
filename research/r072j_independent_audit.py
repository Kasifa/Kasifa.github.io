#!/usr/bin/env python3
"""Independent finite audit of the R0.72J mixed-parity block.

This file does not import the producer implementation.  It represents V by
an explicit directed edge list, advances the complex system with RK45, and
uses Gauss--Legendre quadrature after y=z^3.  Triangle counts are recovered
from a signed-sum Counter, and the scalar profile envelope is evaluated on a
dense logarithmic grid.

The calculation constructs one exact complex root by an evolution-column
correction.  It does not invoke the real-valued Rolle complete-root
corollary, does not enumerate every root, and is not interval arithmetic.
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
from collections import Counter
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


def append_ndjson(path: Path, payload: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def max_rss_mb() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        return float(value) / (1024.0 * 1024.0)
    return float(value) / 1024.0


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "unavailable"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def phi_dense(alpha: float, nodes: int) -> float:
    upper = max(48.0, math.log1p(alpha) + 28.0)
    u = np.linspace(0.0, upper, nodes, dtype=np.float64)
    log_value = -u / 3.0 - alpha * np.exp(-u) - np.log1p(u)
    return float(np.exp(np.max(log_value)))


def gauss_after_cube(order: int, y_max: float) -> tuple[np.ndarray, ...]:
    raw_nodes, raw_weights = leggauss(order)
    z_max = y_max ** (1.0 / 3.0)
    z = 0.5 * z_max * (raw_nodes + 1.0)
    z_weights = 0.5 * z_max * raw_weights
    return z, z**3, z_weights


def square_sum(n: int) -> int:
    return n * (n + 1) * (2 * n + 1) // 6


def signed_triangle_counter(carriers: np.ndarray) -> tuple[int, int]:
    positive = [int(value) for value in carriers]
    signed = positive + [-value for value in positive]
    pair_sums = Counter(left + right for left in signed for right in signed)
    signed_count = sum(pair_sums[-third] for third in signed)
    positive_set = set(positive)
    positive_count = sum(
        1 for left in positive for right in positive if left + right in positive_set
    )
    return positive_count, signed_count


def log_slope(rows: list[dict[str, Any]], key: str, tail: int = 0) -> float:
    selected = rows[-tail:] if tail else rows
    scales = np.array([row["R"] for row in selected], dtype=np.float64)
    values = np.array([row[key] for row in selected], dtype=np.float64)
    if np.any(values <= 0.0):
        return float("nan")
    return float(np.polyfit(np.log(scales), np.log(values), 1)[0])


@dataclass
class EdgeLattice:
    R: int
    gamma: float
    amplitude: float
    mu: float
    truncation_factor: int

    def __post_init__(self) -> None:
        self.N = 2 * self.R
        self.delta = self.gamma * self.R
        self.carriers = np.arange(self.R, 3 * self.R, dtype=np.int64)
        self.radius = self.truncation_factor * self.R
        if 2 * int(self.carriers[-1]) > self.radius:
            raise ValueError("truncation misses the two-shift band")
        self.dimension = 2 * self.radius + 1
        self.zero = self.radius
        self.integer_modes = np.arange(-self.radius, self.radius + 1)
        self.modes = self.integer_modes.astype(np.float64)
        self.lambdas = self.modes**2 + self.mu
        self.y_scale = float(self.R * self.R)

        destinations: list[np.ndarray] = []
        sources: list[np.ndarray] = []
        labels: list[np.ndarray] = []
        for label, carrier in enumerate(self.carriers):
            shift = int(carrier)
            span = self.dimension - shift
            destinations.append(np.arange(shift, self.dimension, dtype=np.int64))
            sources.append(np.arange(0, span, dtype=np.int64))
            labels.append(np.full(span, label, dtype=np.int64))
            destinations.append(np.arange(0, span, dtype=np.int64))
            sources.append(np.arange(shift, self.dimension, dtype=np.int64))
            labels.append(np.full(span, label, dtype=np.int64))
        self.edge_destination = np.concatenate(destinations)
        self.edge_source = np.concatenate(sources)
        self.edge_carrier = np.concatenate(labels)

    def apply_v(self, y: float, state: np.ndarray) -> np.ndarray:
        x = y / self.y_scale
        carrier_weights = (
            -1j
            * self.amplitude
            * np.exp(-self.carriers.astype(np.float64) ** 2 * x)
        )
        edge_values = (
            carrier_weights[self.edge_carrier] * state[self.edge_source]
        )
        real = np.bincount(
            self.edge_destination,
            weights=edge_values.real,
            minlength=self.dimension,
        )
        imag = np.bincount(
            self.edge_destination,
            weights=edge_values.imag,
            minlength=self.dimension,
        )
        return real + 1j * imag

    def rhs(self, y: float, state: np.ndarray) -> np.ndarray:
        return (
            -self.lambdas * state + self.delta * self.apply_v(y, state)
        ) / self.y_scale

    def solve(
        self,
        initial: np.ndarray,
        y_end: float,
        *,
        t_eval: np.ndarray | None,
        rtol: float,
        atol: float,
        dense_output: bool = False,
    ) -> Any:
        return solve_ivp(
            self.rhs,
            (0.0, float(y_end)),
            initial,
            method="RK45",
            t_eval=t_eval,
            rtol=rtol,
            atol=atol,
            dense_output=dense_output,
        )

    def aligned_launch(self) -> np.ndarray:
        state = np.zeros(self.dimension, dtype=np.complex128)
        state[self.zero + self.carriers] = 1j / math.sqrt(2.0)
        state[self.zero - self.carriers] = 1j / math.sqrt(2.0)
        return state

    def q_row(self, y: float, state: np.ndarray) -> complex:
        x = y / self.y_scale
        coefficient = (
            2j
            * self.amplitude
            * self.carriers.astype(np.float64) ** 2
            * np.exp(-self.carriers.astype(np.float64) ** 2 * x)
        )
        return complex(
            np.dot(
                coefficient,
                state[self.zero - self.carriers]
                + state[self.zero + self.carriers],
            )
        )


def corrected_launch(
    lattice: EdgeLattice, *, rtol: float, atol: float
) -> tuple[np.ndarray, complex, float, float]:
    y_tau = 1.0 / lattice.R
    e0 = np.zeros(lattice.dimension, dtype=np.complex128)
    e0[lattice.zero] = 1.0
    aligned = lattice.aligned_launch()
    response_e0 = lattice.solve(
        e0,
        y_tau,
        t_eval=np.array([y_tau]),
        rtol=rtol,
        atol=atol,
    )
    response_aligned = lattice.solve(
        aligned,
        y_tau,
        t_eval=np.array([y_tau]),
        rtol=rtol,
        atol=atol,
    )
    if not response_e0.success or not response_aligned.success:
        raise RuntimeError("independent root columns failed")
    value_e0 = complex(response_e0.y[lattice.zero, -1])
    value_aligned = complex(response_aligned.y[lattice.zero, -1])
    zeta = -value_aligned / value_e0
    raw = aligned + zeta * e0
    normalization = math.sqrt(lattice.N) / float(np.linalg.norm(raw))
    launch = normalization * raw
    algebraic = abs(normalization * (value_aligned + zeta * value_e0))
    return launch, zeta, normalization, algebraic


def run_case(
    R: int,
    args: argparse.Namespace,
    progress_path: Path,
    resource_path: Path,
) -> dict[str, Any]:
    started = time.perf_counter()
    lattice = EdgeLattice(
        R=R,
        gamma=args.gamma,
        amplitude=args.amplitude,
        mu=args.mu,
        truncation_factor=args.truncation_factor,
    )
    positive_triangles, signed_triangles = signed_triangle_counter(
        lattice.carriers
    )
    aligned = lattice.aligned_launch()
    aligned_h0 = lattice.apply_v(0.0, aligned)[lattice.zero]
    aligned_b0 = lattice.apply_v(
        0.0, lattice.apply_v(0.0, aligned)
    )[lattice.zero]
    launch, zeta, normalization, algebraic = corrected_launch(
        lattice, rtol=args.rtol, atol=args.atol
    )

    z, y, z_weights = gauss_after_cube(args.quad_order, args.y_max)
    solution = lattice.solve(
        launch,
        args.y_max,
        t_eval=y,
        rtol=args.rtol,
        atol=args.atol,
        dense_output=True,
    )
    if not solution.success or solution.sol is None:
        raise RuntimeError(f"independent RK45 failed for R={R}")
    count = y.size
    h = np.empty(count, dtype=np.complex128)
    qf = np.empty(count, dtype=np.complex128)
    b = np.empty(count, dtype=np.complex128)
    q_density = np.empty(count, dtype=np.float64)
    for column, y_value in enumerate(y):
        state = solution.y[:, column]
        vf = lattice.apply_v(float(y_value), state)
        v2f = lattice.apply_v(float(y_value), vf)
        h[column] = vf[lattice.zero]
        qf[column] = lattice.q_row(float(y_value), state)
        b[column] = v2f[lattice.zero]
        q_density[column] = float(
            np.sum(np.abs(vf) ** 2 / lattice.lambdas)
        )

    x = y / lattice.y_scale
    dx_dz = 3.0 * z**2 / lattice.y_scale
    relative_time = x / args.window
    critical_weight = np.power(relative_time, -1.0 / 3.0) * (
        1.0 + np.log(1.0 / relative_time)
    )
    quadrature = z_weights * dx_dz
    critical_q = float(np.sum(quadrature * critical_weight * q_density))
    mixed_row = float(np.sum(quadrature * np.abs(h * qf)))
    true_cubic = float(
        lattice.delta * np.sum(quadrature * np.abs(h * b))
    )
    h2_integral = float(np.sum(quadrature * np.abs(h) ** 2))

    y_tau = 1.0 / R
    root_state = solution.sol(y_tau)
    root_target = complex(root_state[lattice.zero])
    root_h = complex(lattice.apply_v(y_tau, root_state)[lattice.zero])

    carrier_float = lattice.carriers.astype(np.float64)
    K_v = float(args.amplitude**2 * np.sum(carrier_float**2))
    K_v_formula = float(
        args.amplitude**2
        * (square_sum(3 * R - 1) - square_sum(R - 1))
    )
    K_f = float(np.sum(lattice.modes**2 * np.abs(launch) ** 2))
    E_0 = float(np.vdot(launch, launch).real)
    rho_squared = 2.0 * args.amplitude**2 * lattice.N
    profile_moment = float(
        np.sum(
            carrier_float**2
            * args.amplitude**2
            * np.array(
                [
                    phi_dense(
                        2.0 * args.window * carrier**2, args.phi_nodes
                    )
                    for carrier in carrier_float
                ]
            )
        )
    )

    theta = 3.0 * lattice.delta**2 / (4.0 * K_f)
    D_value = 4.0 * lattice.delta**2 * K_v
    physical_action = theta * critical_q / args.window
    reference_payment = D_value ** (1.0 / 3.0) * (1.0 + physical_action)
    raw_first = E_0 * rho_squared
    raw_diagonal = 2.0 * args.mu**2 * critical_q
    raw_mixed = 12.0 * math.sqrt(
        args.mu * E_0 * profile_moment * critical_q
    )
    raw_true_cubic = 2.0 * true_cubic
    raw_bv_proxy = raw_first + raw_diagonal + raw_mixed + raw_true_cubic
    normalized_true = theta * raw_true_cubic / reference_payment
    normalized_bv_proxy = theta * raw_bv_proxy / reference_payment
    exact_exposure = float(
        lattice.delta
        * 2.0
        * args.amplitude
        * np.sum(carrier_float**-2)
    )
    predicted_b0 = signed_triangles * args.amplitude**2 / math.sqrt(2.0)
    elapsed = time.perf_counter() - started
    row: dict[str, Any] = {
        "R": R,
        "N": lattice.N,
        "gamma": args.gamma,
        "delta": lattice.delta,
        "dimension": lattice.dimension,
        "edgeCount": int(lattice.edge_destination.size),
        "carrierMin": int(lattice.carriers[0]),
        "carrierMax": int(lattice.carriers[-1]),
        "orderedPositiveTriangles": positive_triangles,
        "orderedPositiveFormula": R * (R + 1) // 2,
        "signedTriangles": signed_triangles,
        "signedTriangleFormula": 3 * R * (R + 1),
        "cayleyGraphNonBipartite": signed_triangles > 0,
        "uncorrectedH0Abs": float(abs(aligned_h0)),
        "uncorrectedH0Formula": math.sqrt(2.0) * args.amplitude * lattice.N,
        "uncorrectedB0Abs": float(abs(aligned_b0)),
        "uncorrectedB0Formula": predicted_b0,
        "uncorrectedB0RelativeError": abs(abs(aligned_b0) - predicted_b0)
        / predicted_b0,
        "zetaReal": float(zeta.real),
        "zetaImag": float(zeta.imag),
        "launchNormalization": normalization,
        "algebraicRootResidual": algebraic,
        "evolvedRootResidual": float(abs(root_target)),
        "rootH": float(abs(root_h)),
        "rootHNormalized": float(abs(root_h) / (args.amplitude * lattice.N)),
        "criticalQ": critical_q,
        "mixedRow": mixed_row,
        "deltaIntegralAbsHB": true_cubic,
        "deltaIntegralAbsHBDivR2": true_cubic / R**2,
        "integralH2": h2_integral,
        "maxAbsH": float(np.max(np.abs(h))),
        "maxAbsB": float(np.max(np.abs(b))),
        "maxActionDensity": float(np.max(q_density)),
        "launchEnergy": E_0,
        "K_f": K_f,
        "K_v": K_v,
        "K_vFormula": K_v_formula,
        "K_vFormulaRelativeError": abs(K_v - K_v_formula) / K_v_formula,
        "rhoSquared": rho_squared,
        "profileMoment": profile_moment,
        "theta": theta,
        "thetaTimesR": theta * R,
        "D": D_value,
        "DScaledR5": D_value / R**5,
        "physicalCriticalAction": physical_action,
        "referencePayment": reference_payment,
        "rawBvProxyFirstRoot": raw_first,
        "rawBvProxyTargetDiagonal": raw_diagonal,
        "rawBvProxyMixedMoment": raw_mixed,
        "rawBvProxyTrueCubic": raw_true_cubic,
        "rawMeasuredBvUpperProxy": raw_bv_proxy,
        "normalizedTrueCubic": normalized_true,
        "normalizedTrueCubicTimesR23": normalized_true * R ** (2.0 / 3.0),
        "normalizedMeasuredBvUpperProxy": normalized_bv_proxy,
        "exactExposure": exact_exposure,
        "lambdaExposure": float(
            lattice.delta
            * 2.0
            * args.amplitude
            * np.sum(1.0 / (carrier_float**2 + args.mu))
        ),
        "exactExposureLimit": 4.0 * args.gamma * args.amplitude / 3.0,
        "exactExposureLimitRelativeError": abs(
            exact_exposure - 4.0 * args.gamma * args.amplitude / 3.0
        )
        / (4.0 * args.gamma * args.amplitude / 3.0),
        "solverNfev": int(solution.nfev),
        "elapsedSeconds": elapsed,
        "maxRssMb": max_rss_mb(),
    }
    append_ndjson(
        progress_path,
        {
            "time": utc_now(),
            "event": "case_complete",
            "R": R,
            "rootResidual": row["evolvedRootResidual"],
            "triangles": signed_triangles,
            "criticalQ": critical_q,
            "rawTrueCubic": true_cubic,
            "normalizedTrueCubic": normalized_true,
            "normalizedMeasuredBvUpperProxy": normalized_bv_proxy,
            "exactExposure": exact_exposure,
        },
    )
    append_ndjson(
        resource_path,
        {
            "time": utc_now(),
            "R": R,
            "dimension": lattice.dimension,
            "edgeCount": int(lattice.edge_destination.size),
            "solverNfev": int(solution.nfev),
            "elapsedSeconds": elapsed,
            "maxRssMb": max_rss_mb(),
        },
    )
    print(
        f"independent R={R:>3d} edges={lattice.edge_destination.size:>8d} "
        f"T={signed_triangles:>6d} cubic={true_cubic:.6g} "
        f"cubic/R^2={row['deltaIntegralAbsHBDivR2']:.6g} "
        f"norm={normalized_true:.6g} root={abs(root_target):.2e}",
        flush=True,
    )
    return row


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("research/certificates/r072j"),
    )
    parser.add_argument(
        "--r-values", nargs="+", type=int, default=[4, 8, 16, 32, 64]
    )
    parser.add_argument("--gamma", type=float, default=0.05)
    parser.add_argument("--amplitude", type=float, default=1.0)
    parser.add_argument("--mu", type=float, default=1.0)
    parser.add_argument("--window", type=float, default=1.0)
    parser.add_argument("--y-max", type=float, default=12.0)
    parser.add_argument("--quad-order", type=int, default=260)
    parser.add_argument("--phi-nodes", type=int, default=24001)
    parser.add_argument("--truncation-factor", type=int, default=9)
    parser.add_argument("--rtol", type=float, default=5.0e-10)
    parser.add_argument("--atol", type=float, default=5.0e-12)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.gamma <= 0.0 or args.amplitude <= 0.0:
        raise ValueError("gamma and amplitude must be positive")
    if args.window <= 0.0 or args.y_max <= 0.0:
        raise ValueError("window and y-max must be positive")
    if args.y_max / min(args.r_values) ** 2 >= args.window:
        raise ValueError("the independent quadrature tail must remain in the window")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    progress_path = args.output_dir / "independent-progress.ndjson"
    resource_path = args.output_dir / "independent-resource.ndjson"
    progress_path.write_text("", encoding="utf-8")
    resource_path.write_text("", encoding="utf-8")
    config = {
        "schemaVersion": 1,
        "audit": "R0.72J independent mixed-parity audit",
        "rValues": args.r_values,
        "carrierRule": "S_R={R,...,3R-1}, N=2R",
        "deltaRule": "delta=gamma*R",
        "gamma": args.gamma,
        "amplitude": args.amplitude,
        "mu": args.mu,
        "window": args.window,
        "rootTime": "tau=R^-3",
        "scaledTime": "y=R^2*x",
        "yMax": args.y_max,
        "quadOrder": args.quad_order,
        "phiNodes": args.phi_nodes,
        "truncationFactor": args.truncation_factor,
        "rtol": args.rtol,
        "atol": args.atol,
        "operator": "explicit edge list with destination accumulation",
        "solver": "SciPy solve_ivp RK45",
        "quadrature": "Gauss-Legendre after y=z^3",
        "triangleCounter": "signed ordered pair-sum Counter",
        "producerImported": False,
        "sourceSha256": sha256(Path(__file__).resolve()),
        "rootBoundary": "one exact complex root; no real Rolle complete-root claim",
        "normalizedTrueCubic": (
            "2*theta*(delta*integral|h P0 V^2 F|)/referencePayment"
        ),
    }
    (args.output_dir / "independent-config.json").write_text(
        json.dumps(config, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    append_ndjson(
        progress_path, {"time": utc_now(), "event": "audit_start", "config": config}
    )
    cases = [
        run_case(R, args, progress_path, resource_path) for R in args.r_values
    ]
    tail = min(3, len(cases))
    slopes = {
        "rawTrueCubicAll": log_slope(cases, "deltaIntegralAbsHB"),
        "rawTrueCubicTail": log_slope(cases, "deltaIntegralAbsHB", tail),
        "normalizedTrueCubicAll": log_slope(cases, "normalizedTrueCubic"),
        "normalizedTrueCubicTail": log_slope(
            cases, "normalizedTrueCubic", tail
        ),
        "normalizedMeasuredBvUpperProxyAll": log_slope(
            cases, "normalizedMeasuredBvUpperProxy"
        ),
    }
    checks = {
        "carrierCountNEquals2R": all(row["N"] == 2 * row["R"] for row in cases),
        "orderedPositiveTriangleFormula": all(
            row["orderedPositiveTriangles"] == row["orderedPositiveFormula"]
            for row in cases
        ),
        "signedTriangleFormula": all(
            row["signedTriangles"] == row["signedTriangleFormula"]
            for row in cases
        ),
        "cayleyGraphNonBipartite": all(
            row["cayleyGraphNonBipartite"] for row in cases
        ),
        "uncorrectedTriangleAmplitudeExact": max(
            row["uncorrectedB0RelativeError"] for row in cases
        )
        < 8.0e-15,
        "staticCarrierMomentExact": max(
            row["K_vFormulaRelativeError"] for row in cases
        )
        < 2.0e-15,
        "launchEnergyEqualsN": max(
            abs(row["launchEnergy"] - row["N"]) / row["N"] for row in cases
        )
        < 8.0e-14,
        "rootCorrectionAccurate": max(
            row["evolvedRootResidual"] for row in cases
        )
        < 8.0e-8,
        "rootSlopeNondegenerate": cases[-1]["rootHNormalized"] > 0.5,
        "exposureUniform": max(row["exactExposure"] for row in cases) < 0.2,
        "exposureApproachesFourGammaAOverThree": (
            cases[-1]["exactExposureLimitRelativeError"]
            < cases[0]["exactExposureLimitRelativeError"]
            and cases[-1]["exactExposureLimitRelativeError"] < 0.03
        ),
        "rawCubicNearR2": 1.5 < slopes["rawTrueCubicTail"] < 2.4,
        "normalizedCubicDecays": slopes["normalizedTrueCubicTail"] < -0.3,
    }
    checks = {key: bool(value) for key, value in checks.items()}
    passed = all(checks.values())
    result = {
        "schemaVersion": 1,
        "audit": "R0.72J independent mixed-parity audit",
        "status": "passed" if passed else "failed",
        "generatedAt": utc_now(),
        "gitCommit": git_commit(),
        "config": config,
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "executable": sys.executable,
            "cpuCount": os.cpu_count(),
        },
        "slopes": slopes,
        "checks": checks,
        "cases": cases,
        "limitations": [
            "finite binary64 truncations are not interval certificates",
            "one exact complex temporal root is constructed; no real Rolle complete-root claim is made",
            "the independent edge-list representation is slower but does not import producer code",
            "the block S_R does not represent every non-bipartite carrier set",
            "the scaling observations are finite evidence, not an asymptotic proof",
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
    (args.output_dir / "independent-environment.txt").write_text(
        "\n".join(
            [
                f"generatedAt={utc_now()}",
                f"python={sys.version}",
                f"platform={platform.platform()}",
                f"numpy={np.__version__}",
                f"scipy={scipy.__version__}",
                f"executable={sys.executable}",
                f"cpuCount={os.cpu_count()}",
                f"maxRssMb={max_rss_mb()}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    append_ndjson(
        progress_path,
        {
            "time": utc_now(),
            "event": "audit_complete",
            "status": result["status"],
            "slopes": slopes,
            "checks": checks,
        },
    )
    monitor = {
        "status": result["status"],
        "cases": len(cases),
        "maxRssMb": max_rss_mb(),
    }
    (args.output_dir / "independent-monitor.log").write_text(
        json.dumps(monitor, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(monitor, sort_keys=True), flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
