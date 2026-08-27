#!/usr/bin/env python3
"""Producer-side finite audit for the R0.72I parity repair.

The audit uses the complex Fourier lattice rather than the real-gauge code
path.  For every dyadic carrier count M it sets ``delta=M`` on the all-odd
Rudin--Shapiro block, constructs the exact root at x=M^{-3}, and measures
the term that is deliberately left unresolved by the generic R0.72H
complete-root corollary::

    delta * integral |h P_0 V^2 F| dx.

All carriers are odd.  Consequently V flips lattice parity and V^2
preserves it; only the even component of F can contribute to P_0 V^2 F.
The script records that even component directly and compares the measured
term with the generic B_A Q_* upper bound.  It also writes the exact static
moments and the physical amplitude-balance lift used in the R0.72I scaling
ledger.

This is a deterministic binary64 truncation audit, not an interval proof and
not a certificate that every temporal root has been found.
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
        old_p = p
        old_q = q
        p = np.concatenate((old_p, old_q))
        q = np.concatenate((old_p, -old_q))
    return p.astype(np.float64)


def critical_weight(s: np.ndarray) -> np.ndarray:
    result = np.empty_like(s, dtype=np.float64)
    positive = s > 0.0
    result[positive] = np.power(s[positive], -1.0 / 3.0) * (
        1.0 + np.log(1.0 / s[positive])
    )
    result[~positive] = np.inf
    return result


def envelope_phi(alpha: float) -> tuple[float, float]:
    """Return Phi(alpha) and its maximizing s in logarithmic coordinates."""

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


@dataclass
class OddCarrierLattice:
    M: int
    amplitude: float
    mu: float
    truncation_factor: int

    def __post_init__(self) -> None:
        self.delta = float(self.M)
        self.signs = rudin_shapiro_recurrence(self.M)
        self.carriers = 2 * self.M + 2 * np.arange(self.M, dtype=np.int64) + 1
        self.radius = self.truncation_factor * self.M
        if 2 * int(self.carriers[-1]) > self.radius:
            raise ValueError(
                "truncation must include the two-shift band needed for P0 V^2 F"
            )
        self.integer_modes = np.arange(-self.radius, self.radius + 1)
        self.modes = self.integer_modes.astype(np.float64)
        self.zero = self.radius
        self.dimension = self.modes.size
        self.lambdas = self.modes**2 + self.mu
        self.y_scale = float(self.M * self.M)
        self.even_mask = self.integer_modes % 2 == 0
        self.odd_mask = ~self.even_mask

    def apply_v(self, y: float, state: np.ndarray) -> np.ndarray:
        x = y / self.y_scale
        output = np.zeros_like(state, dtype=np.complex128)
        factors = (
            -1j
            * self.amplitude
            * self.signs
            * np.exp(-(self.carriers.astype(np.float64) ** 2) * x)
        )
        for carrier, coefficient in zip(self.carriers, factors, strict=True):
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
        coefficient = 1j / math.sqrt(2.0)
        for carrier, sign in zip(self.carriers, self.signs, strict=True):
            state[self.zero + int(carrier)] = coefficient * sign
            state[self.zero - int(carrier)] = coefficient * sign
        return state

    def q_row(self, y: float, state: np.ndarray) -> complex:
        x = y / self.y_scale
        factors = (
            2j
            * self.amplitude
            * self.signs
            * self.carriers.astype(np.float64) ** 2
            * np.exp(-(self.carriers.astype(np.float64) ** 2) * x)
        )
        values = state[self.zero - self.carriers] + state[
            self.zero + self.carriers
        ]
        return complex(np.sum(factors * values))


def corrected_launch(
    lattice: OddCarrierLattice, *, rtol: float, atol: float
) -> tuple[np.ndarray, complex, float, float, complex]:
    """Correct the target coordinate so that F_0(M^{-3}) is exactly zero."""

    y_tau = 1.0 / lattice.M
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
    normalization = math.sqrt(lattice.M) / float(np.linalg.norm(raw))
    launch = normalization * raw
    algebraic_residual = abs(normalization * (value_b + zeta * value_a))
    return launch, zeta, algebraic_residual, abs(value_a), value_b


def observe(
    lattice: OddCarrierLattice,
    y_values: np.ndarray,
    states: np.ndarray,
) -> dict[str, np.ndarray]:
    count = y_values.size
    h = np.empty(count, dtype=np.complex128)
    qf = np.empty(count, dtype=np.complex128)
    b = np.empty(count, dtype=np.complex128)
    q_density = np.empty(count, dtype=np.float64)
    even_norm = np.empty(count, dtype=np.float64)
    odd_norm = np.empty(count, dtype=np.float64)
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
        even_norm[column] = float(np.linalg.norm(state[lattice.even_mask]))
        odd_norm[column] = float(np.linalg.norm(state[lattice.odd_mask]))
        target[column] = state[lattice.zero]
    return {
        "h": h,
        "qf": qf,
        "b": b,
        "q": q_density,
        "evenNorm": even_norm,
        "oddNorm": odd_norm,
        "target": target,
    }


def integrate_case(
    M: int,
    args: argparse.Namespace,
    progress_path: Path,
    resource_path: Path,
) -> dict[str, Any]:
    started = time.perf_counter()
    lattice = OddCarrierLattice(
        M=M,
        amplitude=args.amplitude,
        mu=args.mu,
        truncation_factor=args.truncation_factor,
    )
    launch, zeta, algebraic_residual, root_column_abs, column_b = (
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
        raise RuntimeError(f"DOP853 failed for M={M}: {solution.message}")
    obs = observe(lattice, y_grid, solution.y)

    x_values = y_grid / lattice.y_scale
    jacobian_dx_dz = 3.0 * z_grid**2 / lattice.y_scale
    weights = critical_weight(x_values / args.window)
    positive = z_grid > 0.0

    mixed_integrand = np.abs(obs["h"] * obs["qf"]) * jacobian_dx_dz
    hb_integrand = (
        lattice.delta
        * np.abs(obs["h"] * obs["b"])
        * jacobian_dx_dz
    )
    h2_integrand = np.abs(obs["h"]) ** 2 * jacobian_dx_dz
    critical_integrand = np.zeros_like(z_grid)
    critical_integrand[positive] = (
        weights[positive]
        * obs["q"][positive]
        * jacobian_dx_dz[positive]
    )

    mixed_row = float(simpson(mixed_integrand, x=z_grid))
    delta_hb = float(simpson(hb_integrand, x=z_grid))
    h2_integral = float(simpson(h2_integrand, x=z_grid))
    critical_q = float(simpson(critical_integrand, x=z_grid))

    carriers_float = lattice.carriers.astype(np.float64)
    k_s = float(np.sum(carriers_float**2))
    k_v = float(args.amplitude**2 * k_s)
    e0 = float(np.vdot(launch, launch).real)
    k_f = float(np.sum(lattice.modes**2 * np.abs(launch) ** 2))
    rho_squared = float(2.0 * args.amplitude**2 * M)
    b_squared = float(
        2.0 * args.amplitude**2 * (k_s + args.mu * M)
    )
    b_static = math.sqrt(b_squared)

    moment_terms: list[float] = []
    phi_maximizers: list[float] = []
    for carrier in carriers_float:
        phi, maximizer = envelope_phi(2.0 * args.window * carrier * carrier)
        moment_terms.append(carrier**2 * args.amplitude**2 * phi)
        phi_maximizers.append(maximizer)
    moment = float(sum(moment_terms))

    y_tau = 1.0 / M
    root_solution = lattice.solve(
        launch,
        y_tau,
        np.array([y_tau]),
        rtol=args.rtol,
        atol=args.atol,
    )
    if not root_solution.success:
        raise RuntimeError(f"root-state evolution failed for M={M}")
    root_state = root_solution.y[:, -1]
    root_target = complex(root_state[lattice.zero])
    root_h = complex(lattice.apply_v(y_tau, root_state)[lattice.zero])

    # Exact R0.72D amplitude balance: S^2 K_f = 3 P^2 K_v.
    # With q=1 and P=delta, E=4 P^2 K_v and the root-atom lift is
    # Theta=S^2 P^2/E=3 P^2/(4 K_f).
    physical_p = lattice.delta
    theta = 3.0 * physical_p**2 / (4.0 * k_f)
    reference_data = 4.0 * physical_p**2 * k_v
    data_one_third = reference_data ** (1.0 / 3.0)
    physical_critical_action = theta * critical_q / args.window
    reference_payment = data_one_third * (1.0 + physical_critical_action)

    raw_terms = {
        "firstRoot": e0 * rho_squared,
        "targetDiagonal": 2.0 * args.mu**2 * critical_q,
        "mixedMoment": 12.0
        * math.sqrt(args.mu * e0 * moment * critical_q),
        "genericB": 2.0
        * lattice.delta
        * math.sqrt(args.mu)
        * b_static
        * critical_q,
    }
    lifted_terms = {key: theta * value for key, value in raw_terms.items()}
    term_ratios = {
        key: value / reference_payment for key, value in lifted_terms.items()
    }

    measured_bv_upper = (
        e0 * rho_squared
        + 2.0 * args.mu * h2_integral
        + 2.0 * mixed_row
        + 2.0 * delta_hb
    )
    parity_scale = lattice.delta * args.amplitude / M
    elapsed = time.perf_counter() - started
    root_slope_normalized = float(abs(root_h) / (args.amplitude * M))
    exact_root_ratio = theta * abs(root_h) ** 2 / reference_payment
    # The finite-M root-slope prefactor approaches its nonzero limit slowly
    # when delta=M.  Removing that measured prefactor exposes the predicted
    # M^{-2/3} physical scaling without pretending that the smallest cases
    # are already asymptotic.
    exact_root_ratio_rescaled = (
        exact_root_ratio
        * M ** (2.0 / 3.0)
        / max(root_slope_normalized**2, np.finfo(np.float64).tiny)
    )
    result: dict[str, Any] = {
        "M": M,
        "delta": lattice.delta,
        "dimension": lattice.dimension,
        "carrierMin": int(lattice.carriers[0]),
        "carrierMax": int(lattice.carriers[-1]),
        "zetaReal": float(zeta.real),
        "zetaImag": float(zeta.imag),
        "zetaTimesM": float(abs(zeta) * M),
        "rootColumnAbs": root_column_abs,
        "rootColumnBAbs": float(abs(column_b)),
        "algebraicRootResidual": algebraic_residual,
        "evolvedRootResidual": float(abs(root_target)),
        "rootH": float(abs(root_h)),
        "rootHOverAM": root_slope_normalized,
        "mixedRow": mixed_row,
        "criticalQ": critical_q,
        "deltaIntegralAbsHB": delta_hb,
        "integralH2": h2_integral,
        "maxAbsH": float(np.max(np.abs(obs["h"]))),
        "maxAbsQF": float(np.max(np.abs(obs["qf"]))),
        "maxActionDensity": float(np.max(obs["q"])),
        "maxAbsB": float(np.max(np.abs(obs["b"]))),
        "maxEvenNorm": float(np.max(obs["evenNorm"])),
        "maxOddNorm": float(np.max(obs["oddNorm"])),
        "maxEvenNormOverDeltaAOverM": float(
            np.max(obs["evenNorm"]) / parity_scale
        ),
        "maxOddNormOverSqrtM": float(np.max(obs["oddNorm"]) / math.sqrt(M)),
        "launchEnergyE0": e0,
        "K_s": k_s,
        "K_v": k_v,
        "K_f": k_f,
        "rhoSquared": rho_squared,
        "B_squared": b_squared,
        "B": b_static,
        "profileMoment": moment,
        "phiMaximizerMin": float(min(phi_maximizers)),
        "phiMaximizerMax": float(max(phi_maximizers)),
        "theta": theta,
        "referenceData": reference_data,
        "dataOneThird": data_one_third,
        "physicalCriticalAction": physical_critical_action,
        "referencePayment": reference_payment,
        "exactRootPhysicalAtom": theta * abs(root_h) ** 2,
        "exactRootRatio": exact_root_ratio,
        "exactRootRatioRescaled": exact_root_ratio_rescaled,
        "measuredBvUpper": measured_bv_upper,
        "measuredBvLiftedRatio": theta * measured_bv_upper / reference_payment,
        "genericBToMeasuredHB": raw_terms["genericB"]
        / max(2.0 * delta_hb, np.finfo(np.float64).tiny),
        "rawTermFirstRoot": raw_terms["firstRoot"],
        "rawTermTargetDiagonal": raw_terms["targetDiagonal"],
        "rawTermMixedMoment": raw_terms["mixedMoment"],
        "rawTermGenericB": raw_terms["genericB"],
        "liftedTermFirstRoot": lifted_terms["firstRoot"],
        "liftedTermTargetDiagonal": lifted_terms["targetDiagonal"],
        "liftedTermMixedMoment": lifted_terms["mixedMoment"],
        "liftedTermGenericB": lifted_terms["genericB"],
        "ratioFirstRoot": term_ratios["firstRoot"],
        "ratioTargetDiagonal": term_ratios["targetDiagonal"],
        "ratioMixedMoment": term_ratios["mixedMoment"],
        "ratioGenericB": term_ratios["genericB"],
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
            "rootResidual": result["evolvedRootResidual"],
            "criticalQ": critical_q,
            "deltaIntegralAbsHB": delta_hb,
            "genericBToMeasuredHB": result["genericBToMeasuredHB"],
            "ratioGenericB": result["ratioGenericB"],
            "exactRootRatio": result["exactRootRatio"],
        },
    )
    append_ndjson(
        resource_path,
        {
            "time": utc_now(),
            "M": M,
            "dimension": lattice.dimension,
            "solverNfev": result["solverNfev"],
            "elapsedSeconds": elapsed,
            "maxRssMb": result["maxRssMb"],
        },
    )
    print(
        f"M={M:>3d} dim={lattice.dimension:>4d} "
        f"Q*={critical_q:.6g} deltaHB={delta_hb:.6g} "
        f"B/measured={result['genericBToMeasuredHB']:.4g} "
        f"B-ratio={result['ratioGenericB']:.4g} "
        f"root-ratio={result['exactRootRatio']:.4g}",
        flush=True,
    )
    return result


def fit_slope(cases: list[dict[str, Any]], key: str, log_adjust: int = 0) -> float:
    m_values = np.array([row["M"] for row in cases], dtype=np.float64)
    values = np.array([row[key] for row in cases], dtype=np.float64)
    if log_adjust:
        values = values * np.log(m_values) ** log_adjust
    slope, _ = np.polyfit(np.log(m_values), np.log(values), 1)
    return float(slope)


def write_csv(path: Path, cases: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(cases[0].keys()), lineterminator="\n"
        )
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
        default=Path("research/certificates/r072i"),
    )
    parser.add_argument(
        "--m-values", nargs="+", type=int, default=[4, 8, 16, 32, 64]
    )
    parser.add_argument("--amplitude", type=float, default=1.0)
    parser.add_argument("--mu", type=float, default=1.0)
    parser.add_argument("--window", type=float, default=1.0)
    parser.add_argument("--y-max", type=float, default=14.0)
    parser.add_argument("--quad-points", type=int, default=1001)
    parser.add_argument("--truncation-factor", type=int, default=8)
    parser.add_argument("--rtol", type=float, default=2.0e-10)
    parser.add_argument("--atol", type=float, default=2.0e-12)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.window <= 0.0:
        raise ValueError("window must be positive")
    if args.amplitude <= 0.0:
        raise ValueError("amplitude must be positive")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    progress_path = args.output_dir / "producer-progress.ndjson"
    resource_path = args.output_dir / "producer-resource.ndjson"
    for path in (progress_path, resource_path):
        path.write_text("", encoding="utf-8")

    config = {
        "audit": "R0.72I parity-resolved producer",
        "date": "2026-08-27",
        "mValues": args.m_values,
        "deltaRule": "delta=M",
        "amplitude": args.amplitude,
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
        "physicalBalance": "S^2 K_f=3 P^2 K_v, q=1, P=delta",
        "referencePayment": "D^(1/3)*(1+Theta*Q_*/window)",
    }
    (args.output_dir / "config.json").write_text(
        json.dumps(config, indent=2, sort_keys=True) + "\n", encoding="utf-8"
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
    slopes = {
        "criticalQDivLog": fit_slope(cases, "criticalQ", log_adjust=-1),
        "mixedRow": fit_slope(cases, "mixedRow"),
        "deltaIntegralAbsHB": fit_slope(cases, "deltaIntegralAbsHB"),
        "genericBDivLog": fit_slope(cases, "rawTermGenericB", log_adjust=-1),
        "referenceData": fit_slope(cases, "referenceData"),
        "genericBRatioDivLog": fit_slope(
            cases, "ratioGenericB", log_adjust=-1
        ),
        "exactRootRatio": fit_slope(cases, "exactRootRatio"),
        "exactRootRatioRescaled": fit_slope(cases, "exactRootRatioRescaled"),
    }
    checks = {
        "allOddCarriers": all(
            row["carrierMin"] % 2 == 1 and row["carrierMax"] % 2 == 1
            for row in cases
        ),
        "deltaEqualsM": all(row["delta"] == row["M"] for row in cases),
        "realCorrection": max(abs(row["zetaImag"]) for row in cases) < 1.0e-8,
        "exactInteriorRoot": max(
            row["evolvedRootResidual"] for row in cases
        )
        < 2.0e-8,
        "noncollapsedRootSlopeAtLargestM": cases[-1]["rootHOverAM"] > 0.70,
        "evenParityScaleFinite": max(
            row["maxEvenNormOverDeltaAOverM"] for row in cases
        )
        < 8.0,
        "oddEnergyScaleFinite": max(
            row["maxOddNormOverSqrtM"] for row in cases
        )
        < 1.1,
        "genericBStrictlyCoarserThanMeasuredHB": min(
            row["genericBToMeasuredHB"] for row in cases[-2:]
        )
        > 2.0,
        "genericBRatioGrows": cases[-1]["ratioGenericB"]
        > cases[0]["ratioGenericB"],
        "exactRootScalingConsistent": max(
            row["exactRootRatioRescaled"] for row in cases
        )
        / min(row["exactRootRatioRescaled"] for row in cases)
        < 1.35,
    }
    passed = all(checks.values())
    result = {
        "schemaVersion": 1,
        "audit": "R0.72I parity-resolved producer",
        "status": "passed" if passed else "failed",
        "generatedAt": utc_now(),
        "gitCommit": git_commit(),
        "config": config,
        "slopes": slopes,
        "checks": checks,
        "cases": cases,
        "limitations": [
            "finite truncated lattices do not prove the parity lemma",
            "the audit constructs one exact root but does not certify the complete root set",
            "D and Theta use the declared enstrophy-dominant amplitude-balance proxy",
            "the calculation is restricted to the all-odd real-gauge triangular class",
            "strong coupling beyond delta*a=O(M^(3/2)) is not tested by this delta=M run",
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
