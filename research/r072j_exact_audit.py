#!/usr/bin/env python3
"""Producer finite audit for the R0.72J mixed-parity carrier block.

For every dyadic R the carrier set is S_R={R,...,3R-1}, so N=2R.  The
coupling is delta=gamma*R and every carrier coefficient is one.  The launch
has i/sqrt(2) at both signed copies of every carrier; an e_0 column correction
then makes F_0(R^-3)=0 exactly, after which the launch is normalized to
||F(0)||^2=N.

The audit measures the true cubic row

    delta * integral |(P_0 V F)(P_0 V^2 F)| dx

and its physical amplitude-balance lift.  It also certifies the elementary
triangle obstruction to a bipartite carrier graph.  This is deterministic
binary64 evidence on finite truncated lattices, not an interval proof and not
a complete enumeration of temporal roots.
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
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def critical_weight(s: np.ndarray) -> np.ndarray:
    result = np.empty_like(s, dtype=np.float64)
    positive = s > 0.0
    result[positive] = np.power(s[positive], -1.0 / 3.0) * (
        1.0 + np.log(1.0 / s[positive])
    )
    result[~positive] = np.inf
    return result


def envelope_phi(alpha: float) -> tuple[float, float]:
    upper = max(50.0, math.log1p(alpha) + 30.0)

    def negative_log_value(u: float) -> float:
        return u / 3.0 + alpha * math.exp(-u) + math.log1p(u)

    optimum = minimize_scalar(
        negative_log_value,
        bounds=(0.0, upper),
        method="bounded",
        options={"xatol": 1.0e-13},
    )
    u_star = float(optimum.x)
    return math.exp(-negative_log_value(u_star)), math.exp(-u_star)


def log_slope(cases: list[dict[str, Any]], key: str, tail: int = 0) -> float:
    selected = cases[-tail:] if tail else cases
    scales = np.array([row["R"] for row in selected], dtype=np.float64)
    values = np.array([row[key] for row in selected], dtype=np.float64)
    if np.any(values <= 0.0):
        return float("nan")
    return float(np.polyfit(np.log(scales), np.log(values), 1)[0])


def spread(cases: list[dict[str, Any]], key: str) -> float:
    values = np.array([row[key] for row in cases], dtype=np.float64)
    return float(np.max(values) / np.min(values))


@dataclass
class MixedCarrierLattice:
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
            raise ValueError("truncation must contain the two-shift band")
        self.integer_modes = np.arange(-self.radius, self.radius + 1)
        self.modes = self.integer_modes.astype(np.float64)
        self.zero = self.radius
        self.dimension = self.integer_modes.size
        self.lambdas = self.modes**2 + self.mu
        self.y_scale = float(self.R * self.R)

    def apply_v(self, y: float, state: np.ndarray) -> np.ndarray:
        x = y / self.y_scale
        coefficients = (
            -1j
            * self.amplitude
            * np.exp(-self.carriers.astype(np.float64) ** 2 * x)
        )
        output = np.zeros_like(state, dtype=np.complex128)
        for carrier, coefficient in zip(
            self.carriers, coefficients, strict=True
        ):
            shift = int(carrier)
            output[shift:] += coefficient * state[:-shift]
            output[:-shift] += coefficient * state[shift:]
        return output

    def rhs(self, y: float, state: np.ndarray) -> np.ndarray:
        return (
            -self.lambdas * state + self.delta * self.apply_v(y, state)
        ) / self.y_scale

    def solve(
        self,
        initial: np.ndarray,
        y_end: float,
        t_eval: np.ndarray | None,
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
        value = 1j / math.sqrt(2.0)
        for carrier in self.carriers:
            state[self.zero + int(carrier)] = value
            state[self.zero - int(carrier)] = value
        return state

    def q_row(self, y: float, state: np.ndarray) -> complex:
        x = y / self.y_scale
        coefficients = (
            2j
            * self.amplitude
            * self.carriers.astype(np.float64) ** 2
            * np.exp(-self.carriers.astype(np.float64) ** 2 * x)
        )
        values = state[self.zero - self.carriers] + state[
            self.zero + self.carriers
        ]
        return complex(np.sum(coefficients * values))


def triangle_counts(carriers: np.ndarray) -> tuple[int, int]:
    carrier_set = {int(value) for value in carriers}
    ordered_positive = sum(
        1
        for left in carrier_set
        for right in carrier_set
        if left + right in carrier_set
    )
    signed = carrier_set | {-value for value in carrier_set}
    signed_count = sum(
        1 for left in signed for right in signed if -(left + right) in signed
    )
    return ordered_positive, signed_count


def corrected_launch(
    lattice: MixedCarrierLattice, *, rtol: float, atol: float
) -> tuple[np.ndarray, complex, float, float, complex, float]:
    y_tau = 1.0 / lattice.R
    e0 = np.zeros(lattice.dimension, dtype=np.complex128)
    e0[lattice.zero] = 1.0
    aligned = lattice.aligned_launch()
    column_a = lattice.solve(
        e0, y_tau, np.array([y_tau]), rtol=rtol, atol=atol
    )
    column_b = lattice.solve(
        aligned, y_tau, np.array([y_tau]), rtol=rtol, atol=atol
    )
    if not column_a.success or not column_b.success:
        raise RuntimeError("root-column evolution failed")
    value_a = complex(column_a.y[lattice.zero, -1])
    value_b = complex(column_b.y[lattice.zero, -1])
    zeta = -value_b / value_a
    raw = aligned + zeta * e0
    normalization = math.sqrt(lattice.N) / float(np.linalg.norm(raw))
    launch = normalization * raw
    residual = abs(normalization * (value_b + zeta * value_a))
    return launch, zeta, normalization, abs(value_a), value_b, residual


def observe(
    lattice: MixedCarrierLattice,
    y_values: np.ndarray,
    states: np.ndarray,
) -> dict[str, np.ndarray]:
    count = y_values.size
    h = np.empty(count, dtype=np.complex128)
    qf = np.empty(count, dtype=np.complex128)
    b = np.empty(count, dtype=np.complex128)
    q_density = np.empty(count, dtype=np.float64)
    target = np.empty(count, dtype=np.complex128)
    for column, y in enumerate(y_values):
        state = states[:, column]
        vf = lattice.apply_v(float(y), state)
        v2f = lattice.apply_v(float(y), vf)
        h[column] = vf[lattice.zero]
        qf[column] = lattice.q_row(float(y), state)
        b[column] = v2f[lattice.zero]
        q_density[column] = float(
            np.sum(np.abs(vf) ** 2 / lattice.lambdas)
        )
        target[column] = state[lattice.zero]
    return {"h": h, "qf": qf, "b": b, "q": q_density, "target": target}


def integrate_case(
    R: int,
    args: argparse.Namespace,
    progress_path: Path,
    resource_path: Path,
) -> dict[str, Any]:
    started = time.perf_counter()
    lattice = MixedCarrierLattice(
        R=R,
        gamma=args.gamma,
        amplitude=args.amplitude,
        mu=args.mu,
        truncation_factor=args.truncation_factor,
    )
    ordered_positive, signed_triangles = triangle_counts(lattice.carriers)
    launch_aligned = lattice.aligned_launch()
    uncorrected_h0 = lattice.apply_v(0.0, launch_aligned)[lattice.zero]
    uncorrected_b0 = lattice.apply_v(
        0.0, lattice.apply_v(0.0, launch_aligned)
    )[lattice.zero]
    launch, zeta, normalization, root_column_abs, root_column_b, algebraic = (
        corrected_launch(lattice, rtol=args.rtol, atol=args.atol)
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
        raise RuntimeError(f"DOP853 failed for R={R}: {solution.message}")
    values = observe(lattice, y_grid, solution.y)
    x_grid = y_grid / lattice.y_scale
    dx_dz = 3.0 * z_grid**2 / lattice.y_scale
    weights = critical_weight(x_grid / args.window)
    positive = z_grid > 0.0

    mixed_row = float(
        simpson(np.abs(values["h"] * values["qf"]) * dx_dz, x=z_grid)
    )
    true_cubic = float(
        simpson(
            lattice.delta * np.abs(values["h"] * values["b"]) * dx_dz,
            x=z_grid,
        )
    )
    h2_integral = float(
        simpson(np.abs(values["h"]) ** 2 * dx_dz, x=z_grid)
    )
    critical_integrand = np.zeros_like(z_grid)
    critical_integrand[positive] = (
        weights[positive] * values["q"][positive] * dx_dz[positive]
    )
    critical_q = float(simpson(critical_integrand, x=z_grid))

    y_tau = 1.0 / R
    root_solution = lattice.solve(
        launch,
        y_tau,
        np.array([y_tau]),
        rtol=args.rtol,
        atol=args.atol,
    )
    if not root_solution.success:
        raise RuntimeError(f"root-state evolution failed for R={R}")
    root_state = root_solution.y[:, -1]
    root_target = complex(root_state[lattice.zero])
    root_h = complex(lattice.apply_v(y_tau, root_state)[lattice.zero])

    carriers_float = lattice.carriers.astype(np.float64)
    K_v = float(args.amplitude**2 * np.sum(carriers_float**2))
    K_f = float(np.sum(lattice.modes**2 * np.abs(launch) ** 2))
    E_0 = float(np.vdot(launch, launch).real)
    rho_squared = float(2.0 * args.amplitude**2 * lattice.N)
    B_squared = float(
        2.0
        * args.amplitude**2
        * np.sum(carriers_float**2 + args.mu)
    )
    profile_terms: list[float] = []
    phi_maximizers: list[float] = []
    for carrier in carriers_float:
        phi, maximizer = envelope_phi(2.0 * args.window * carrier**2)
        profile_terms.append(carrier**2 * args.amplitude**2 * phi)
        phi_maximizers.append(maximizer)
    profile_moment = float(sum(profile_terms))

    theta = 3.0 * lattice.delta**2 / (4.0 * K_f)
    D_value = 4.0 * lattice.delta**2 * K_v
    D_one_third = D_value ** (1.0 / 3.0)
    physical_action = theta * critical_q / args.window
    reference_payment = D_one_third * (1.0 + physical_action)
    raw_first = E_0 * rho_squared
    raw_diagonal = 2.0 * args.mu**2 * critical_q
    raw_mixed = 12.0 * math.sqrt(
        args.mu * E_0 * profile_moment * critical_q
    )
    raw_true_cubic = 2.0 * true_cubic
    measured_bv_proxy = raw_first + raw_diagonal + raw_mixed + raw_true_cubic
    normalized_true_cubic = theta * raw_true_cubic / reference_payment
    normalized_bv_proxy = theta * measured_bv_proxy / reference_payment

    exact_exposure = float(
        lattice.delta
        * 2.0
        * args.amplitude
        * np.sum(carriers_float**-2)
    )
    lambda_exposure = float(
        lattice.delta
        * 2.0
        * args.amplitude
        * np.sum(1.0 / (carriers_float**2 + args.mu))
    )
    elapsed = time.perf_counter() - started
    predicted_b0 = signed_triangles * args.amplitude**2 / math.sqrt(2.0)
    predicted_h0 = math.sqrt(2.0) * args.amplitude * lattice.N
    row: dict[str, Any] = {
        "R": R,
        "N": lattice.N,
        "gamma": args.gamma,
        "delta": lattice.delta,
        "dimension": lattice.dimension,
        "carrierMin": int(lattice.carriers[0]),
        "carrierMax": int(lattice.carriers[-1]),
        "containsEvenCarrier": bool(np.any(lattice.carriers % 2 == 0)),
        "containsOddCarrier": bool(np.any(lattice.carriers % 2 == 1)),
        "orderedPositiveTriangles": ordered_positive,
        "orderedPositiveFormula": R * (R + 1) // 2,
        "signedTriangles": signed_triangles,
        "signedTriangleFormula": 3 * R * (R + 1),
        "cayleyGraphNonBipartite": signed_triangles > 0,
        "uncorrectedH0Abs": float(abs(uncorrected_h0)),
        "uncorrectedH0Formula": predicted_h0,
        "uncorrectedB0Abs": float(abs(uncorrected_b0)),
        "uncorrectedB0Formula": predicted_b0,
        "uncorrectedB0RelativeError": abs(abs(uncorrected_b0) - predicted_b0)
        / predicted_b0,
        "zetaReal": float(zeta.real),
        "zetaImag": float(zeta.imag),
        "launchNormalization": normalization,
        "rootColumnAbs": root_column_abs,
        "rootColumnBAbs": float(abs(root_column_b)),
        "algebraicRootResidual": algebraic,
        "evolvedRootResidual": float(abs(root_target)),
        "rootH": float(abs(root_h)),
        "rootHNormalized": float(abs(root_h) / (args.amplitude * lattice.N)),
        "criticalQ": critical_q,
        "mixedRow": mixed_row,
        "deltaIntegralAbsHB": true_cubic,
        "deltaIntegralAbsHBDivR2": true_cubic / R**2,
        "integralH2": h2_integral,
        "maxAbsH": float(np.max(np.abs(values["h"]))),
        "maxAbsB": float(np.max(np.abs(values["b"]))),
        "maxActionDensity": float(np.max(values["q"])),
        "launchEnergy": E_0,
        "K_f": K_f,
        "K_v": K_v,
        "rhoSquared": rho_squared,
        "B_squared": B_squared,
        "profileMoment": profile_moment,
        "phiMaximizerMin": float(min(phi_maximizers)),
        "phiMaximizerMax": float(max(phi_maximizers)),
        "theta": theta,
        "thetaTimesR": theta * R,
        "D": D_value,
        "DScaledR5": D_value / R**5,
        "DOneThird": D_one_third,
        "physicalCriticalAction": physical_action,
        "referencePayment": reference_payment,
        "rawBvProxyFirstRoot": raw_first,
        "rawBvProxyTargetDiagonal": raw_diagonal,
        "rawBvProxyMixedMoment": raw_mixed,
        "rawBvProxyTrueCubic": raw_true_cubic,
        "rawMeasuredBvUpperProxy": measured_bv_proxy,
        "normalizedTrueCubic": normalized_true_cubic,
        "normalizedTrueCubicTimesR23": normalized_true_cubic * R ** (2.0 / 3.0),
        "normalizedMeasuredBvUpperProxy": normalized_bv_proxy,
        "exactExposure": exact_exposure,
        "lambdaExposure": lambda_exposure,
        "exactExposureLimit": 4.0 * args.gamma * args.amplitude / 3.0,
        "exactExposureLimitRelativeError": abs(
            exact_exposure - 4.0 * args.gamma * args.amplitude / 3.0
        )
        / (4.0 * args.gamma * args.amplitude / 3.0),
        "solverNfev": int(solution.nfev),
        "elapsedSeconds": elapsed,
        "maxRssMb": rss_mb(),
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
            "normalizedTrueCubic": normalized_true_cubic,
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
            "solverNfev": int(solution.nfev),
            "elapsedSeconds": elapsed,
            "maxRssMb": rss_mb(),
        },
    )
    print(
        f"R={R:>3d} N={lattice.N:>3d} dim={lattice.dimension:>4d} "
        f"T={signed_triangles:>6d} cubic={true_cubic:.6g} "
        f"cubic/R^2={row['deltaIntegralAbsHBDivR2']:.6g} "
        f"norm={normalized_true_cubic:.6g} "
        f"BVproxy={normalized_bv_proxy:.6g} root={abs(root_target):.2e}",
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
    parser.add_argument("--y-max", type=float, default=14.0)
    parser.add_argument("--quad-points", type=int, default=1201)
    parser.add_argument("--truncation-factor", type=int, default=8)
    parser.add_argument("--rtol", type=float, default=2.0e-10)
    parser.add_argument("--atol", type=float, default=2.0e-12)
    return parser.parse_args()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(rows[0].keys()), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    if args.gamma <= 0.0 or args.amplitude <= 0.0:
        raise ValueError("gamma and amplitude must be positive")
    if args.window <= 0.0 or args.y_max <= 0.0:
        raise ValueError("window and y-max must be positive")
    if min(args.r_values) < 1:
        raise ValueError("all R values must be positive")
    if args.y_max / min(args.r_values) ** 2 >= args.window:
        raise ValueError("the quadrature tail must remain inside the window")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    progress_path = args.output_dir / "producer-progress.ndjson"
    resource_path = args.output_dir / "producer-resource.ndjson"
    progress_path.write_text("", encoding="utf-8")
    resource_path.write_text("", encoding="utf-8")
    config = {
        "schemaVersion": 1,
        "audit": "R0.72J mixed-parity producer",
        "date": "2026-08-27",
        "rValues": args.r_values,
        "carrierRule": "S_R={R,...,3R-1}, N=2R",
        "deltaRule": "delta=gamma*R",
        "gamma": args.gamma,
        "amplitude": args.amplitude,
        "mu": args.mu,
        "window": args.window,
        "rootTime": "tau=R^-3",
        "scaledTime": "y=R^2*x",
        "launch": "i/sqrt(2) at every signed carrier, e0 root correction, ||F||^2=N",
        "yMax": args.y_max,
        "quadPoints": args.quad_points,
        "truncationFactor": args.truncation_factor,
        "rtol": args.rtol,
        "atol": args.atol,
        "solver": "SciPy solve_ivp DOP853",
        "quadrature": "composite Simpson after y=z^3",
        "sourceSha256": sha256(Path(__file__).resolve()),
        "physicalNormalization": {
            "theta": "3*delta^2/(4*K_f)",
            "D": "4*delta^2*K_v",
            "referencePayment": "D^(1/3)*(1+theta*Q_*/window)",
            "normalizedTrueCubic": (
                "2*theta*(delta*integral|h P0 V^2 F|)/referencePayment"
            ),
        },
        "exactExposure": "2*delta*amplitude*sum_{r in S_R} r^-2",
    }
    (args.output_dir / "config.json").write_text(
        json.dumps(config, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (args.output_dir / "seed.txt").write_text(
        "deterministic:no-random-seed\n", encoding="utf-8"
    )
    append_ndjson(
        progress_path, {"time": utc_now(), "event": "audit_start", "config": config}
    )
    cases = [
        integrate_case(R, args, progress_path, resource_path)
        for R in args.r_values
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
        "exactExposureAll": log_slope(cases, "exactExposure"),
    }
    checks = {
        "carrierCountNEquals2R": all(row["N"] == 2 * row["R"] for row in cases),
        "deltaEqualsGammaR": all(
            abs(row["delta"] - args.gamma * row["R"]) < 1.0e-15
            for row in cases
        ),
        "mixedParity": all(
            row["containsEvenCarrier"] and row["containsOddCarrier"]
            for row in cases
        ),
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
        < 5.0e-15,
        "launchEnergyEqualsN": max(
            abs(row["launchEnergy"] - row["N"]) / row["N"] for row in cases
        )
        < 5.0e-14,
        "rootCorrectionAccurate": max(
            row["evolvedRootResidual"] for row in cases
        )
        < 2.0e-8,
        "rootSlopeNondegenerate": cases[-1]["rootHNormalized"] > 0.5,
        "thetaHasRMinusOneScale": spread(cases, "thetaTimesR") < 1.5,
        "DHasR5Scale": spread(cases, "DScaledR5") < 1.5,
        "exposureUniform": max(row["exactExposure"] for row in cases) < 0.2,
        "exposureApproachesFourGammaAOverThree": (
            cases[-1]["exactExposureLimitRelativeError"]
            < cases[0]["exactExposureLimitRelativeError"]
            and cases[-1]["exactExposureLimitRelativeError"] < 0.03
        ),
        "rawCubicNearR2": 1.55 < slopes["rawTrueCubicTail"] < 2.35,
        "normalizedCubicDecays": slopes["normalizedTrueCubicTail"] < -0.35,
    }
    checks = {key: bool(value) for key, value in checks.items()}
    passed = all(checks.values())
    result = {
        "schemaVersion": 1,
        "audit": "R0.72J mixed-parity producer",
        "status": "passed" if passed else "failed",
        "generatedAt": utc_now(),
        "gitCommit": git_commit(),
        "config": config,
        "slopes": slopes,
        "checks": checks,
        "cases": cases,
        "limitations": [
            "finite binary64 truncations are not interval certificates",
            "one exact complex temporal root is constructed; the real Rolle complete-root corollary does not apply",
            "the block S_R is one genuinely non-bipartite carrier family, not every mixed-parity set",
            "D and theta use the declared exact amplitude-balance normalization",
            "the observed scaling does not by itself prove the corresponding asymptotic theorem",
        ],
    }
    result_path = args.output_dir / "result.json"
    result_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
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
            "slopes": slopes,
            "checks": checks,
        },
    )
    monitor = {
        "status": result["status"],
        "cases": len(cases),
        "maxRssMb": rss_mb(),
        "resultSha256": sha256(result_path),
    }
    (args.output_dir / "producer-monitor.log").write_text(
        json.dumps(monitor, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(monitor, sort_keys=True), flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
