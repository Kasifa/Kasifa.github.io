#!/usr/bin/env python3
"""Independent finite audit for the R0.72I odd-carrier absorption test.

This implementation deliberately does not import or execute the producer.
It uses the binary adjacent-11 definition of the Rudin--Shapiro signs, the
all-odd real gauge, SciPy RK45, and Gauss--Legendre quadrature after the
change of variables ``y=z^3``.  Every case sets ``delta=M``.

The audit is a binary64 diagnostic.  It checks the exact static moments,
the evolution-operator root correction, the critical-log action, the mixed
row, the cubic row ``delta * integral |h P0 V^2 F|``, the even-parity
occupancy, and the physical lift used in R0.72I.  It is not interval
arithmetic and it does not enumerate the complete temporal root set.
"""

from __future__ import annotations

import argparse
import csv
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


def adjacent_11_signs(M: int) -> np.ndarray:
    """Rudin--Shapiro signs from parity of overlapping binary 11 blocks."""

    if M < 1 or M & (M - 1):
        raise ValueError("M must be a positive power of two")
    signs = np.empty(M, dtype=np.float64)
    for value in range(M):
        parity = (value & (value >> 1)).bit_count() & 1
        signs[value] = -1.0 if parity else 1.0
    return signs


def even_i_power(exponent: int) -> float:
    """Return i**exponent as a real sign when exponent is even."""

    if exponent % 2:
        raise ValueError("the all-odd gauge requested an odd power of i")
    return -1.0 if (exponent // 2) % 2 else 1.0


def phi_grid(alpha: float, nodes: int) -> float:
    """Independent dense-log-grid evaluation of the scalar envelope Phi."""

    upper = max(48.0, math.log1p(alpha) + 28.0)
    u = np.linspace(0.0, upper, nodes, dtype=np.float64)
    log_value = -u / 3.0 - alpha * np.exp(-u) - np.log1p(u)
    return float(np.exp(np.max(log_value)))


def gauss_after_cube(order: int, y_max: float) -> tuple[np.ndarray, ...]:
    nodes, weights = leggauss(order)
    z_max = y_max ** (1.0 / 3.0)
    z = 0.5 * z_max * (nodes + 1.0)
    z_weight = 0.5 * z_max * weights
    y = z**3
    return z, y, z_weight


@dataclass
class RealOddLattice:
    M: int
    amplitude: float
    mu: float
    truncation_factor: int

    def __post_init__(self) -> None:
        self.delta = float(self.M)
        self.signs = adjacent_11_signs(self.M)
        self.carriers = (
            2 * self.M + 2 * np.arange(self.M, dtype=np.int64) + 1
        )
        self.gauge_signs = np.array(
            [even_i_power(int(carrier) - 1) for carrier in self.carriers],
            dtype=np.float64,
        )
        self.radius = self.truncation_factor * self.M
        if 2 * int(self.carriers[-1]) > self.radius:
            raise ValueError(
                "truncation misses the first two-shift interaction band"
            )
        self.integer_modes = np.arange(-self.radius, self.radius + 1)
        self.modes = self.integer_modes.astype(np.float64)
        self.lambdas = self.modes**2 + self.mu
        self.zero = self.radius
        self.dimension = self.modes.size
        self.y_scale = float(self.M * self.M)
        self.even_mask = self.integer_modes % 2 == 0
        self.odd_mask = ~self.even_mask

    def apply_v(self, y: float, state: np.ndarray) -> np.ndarray:
        """Apply V in the exact all-odd real gauge."""

        x = y / self.y_scale
        factors = (
            self.amplitude
            * self.signs
            * self.gauge_signs
            * np.exp(-(self.carriers.astype(np.float64) ** 2) * x)
        )
        output = np.zeros_like(state)
        for carrier, factor in zip(self.carriers, factors, strict=True):
            shift = int(carrier)
            output[shift:] += factor * state[:-shift]
            output[:-shift] -= factor * state[shift:]
        return output

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

    def aligned_launch(self) -> np.ndarray:
        state = np.zeros(self.dimension, dtype=np.float64)
        for carrier, sign in zip(self.carriers, self.signs, strict=True):
            shift = int(carrier)
            state[self.zero + shift] = (
                sign * even_i_power(shift + 1) / math.sqrt(2.0)
            )
            state[self.zero - shift] = (
                sign * even_i_power(1 - shift) / math.sqrt(2.0)
            )
        return state

    def q_row(self, y: float, state: np.ndarray) -> float:
        """Return QF; in this geometry each target-row entry gains -2r^2."""

        x = y / self.y_scale
        factors = (
            -2.0
            * self.amplitude
            * self.signs
            * self.gauge_signs
            * self.carriers.astype(np.float64) ** 2
            * np.exp(-(self.carriers.astype(np.float64) ** 2) * x)
        )
        difference = (
            state[self.zero - self.carriers]
            - state[self.zero + self.carriers]
        )
        return float(np.sum(factors * difference))


def root_corrected_launch(
    lattice: RealOddLattice,
    *,
    rtol: float,
    atol: float,
) -> tuple[np.ndarray, float, float, float]:
    """Choose the real e0 correction producing F_0(M^-3)=0 exactly."""

    y_tau = 1.0 / lattice.M
    e0 = np.zeros(lattice.dimension, dtype=np.float64)
    e0[lattice.zero] = 1.0
    aligned = lattice.aligned_launch()
    column_a = lattice.solve(
        e0, y_tau, t_eval=np.array([y_tau]), rtol=rtol, atol=atol
    )
    column_b = lattice.solve(
        aligned, y_tau, t_eval=np.array([y_tau]), rtol=rtol, atol=atol
    )
    if not column_a.success or not column_b.success:
        raise RuntimeError("independent root-column evolution failed")
    value_a = float(column_a.y[lattice.zero, -1])
    value_b = float(column_b.y[lattice.zero, -1])
    zeta = -value_b / value_a
    raw = aligned + zeta * e0
    normalization = math.sqrt(lattice.M) / float(np.linalg.norm(raw))
    launch = normalization * raw
    algebraic_residual = abs(normalization * (value_b + zeta * value_a))
    return launch, zeta, normalization, algebraic_residual


def observe(
    lattice: RealOddLattice,
    y_values: np.ndarray,
    states: np.ndarray,
) -> dict[str, np.ndarray]:
    count = y_values.size
    h = np.empty(count, dtype=np.float64)
    qf = np.empty(count, dtype=np.float64)
    b = np.empty(count, dtype=np.float64)
    q_density = np.empty(count, dtype=np.float64)
    even_norm = np.empty(count, dtype=np.float64)
    odd_norm = np.empty(count, dtype=np.float64)
    target = np.empty(count, dtype=np.float64)
    for column, y in enumerate(y_values):
        state = states[:, column]
        vf = lattice.apply_v(float(y), state)
        v2f = lattice.apply_v(float(y), vf)
        h[column] = vf[lattice.zero]
        qf[column] = lattice.q_row(float(y), state)
        b[column] = v2f[lattice.zero]
        q_density[column] = float(np.sum(vf * vf / lattice.lambdas))
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


def run_case(
    M: int,
    args: argparse.Namespace,
    progress_path: Path,
    resource_path: Path,
) -> dict[str, Any]:
    started = time.perf_counter()
    lattice = RealOddLattice(
        M=M,
        amplitude=args.amplitude,
        mu=args.mu,
        truncation_factor=args.truncation_factor,
    )
    launch, zeta, launch_normalization, algebraic_residual = (
        root_corrected_launch(lattice, rtol=args.rtol, atol=args.atol)
    )

    z, y, gauss_weight = gauss_after_cube(args.quad_order, args.y_max)
    solution = lattice.solve(
        launch,
        args.y_max,
        t_eval=y,
        rtol=args.rtol,
        atol=args.atol,
    )
    if not solution.success:
        raise RuntimeError(f"independent RK45 failed for M={M}")
    values = observe(lattice, y, solution.y)

    x = y / lattice.y_scale
    jacobian = 3.0 * z**2 / lattice.y_scale
    relative_time = x / args.window
    critical_weight = np.power(relative_time, -1.0 / 3.0) * (
        1.0 + np.log(1.0 / relative_time)
    )
    quadrature = gauss_weight * jacobian
    mixed_row = float(np.sum(quadrature * np.abs(values["h"] * values["qf"])))
    critical_action = float(
        np.sum(quadrature * critical_weight * values["q"])
    )
    cubic_integral = float(
        lattice.delta
        * np.sum(quadrature * np.abs(values["h"] * values["b"]))
    )
    reciprocal_qf = float(
        np.sum(quadrature * values["qf"] ** 2 / critical_weight)
    )

    y_tau = 1.0 / M
    root_solution = lattice.solve(
        launch,
        y_tau,
        t_eval=np.array([y_tau]),
        rtol=args.rtol,
        atol=args.atol,
    )
    if not root_solution.success:
        raise RuntimeError(f"independent root verification failed for M={M}")
    root_state = root_solution.y[:, -1]
    root_v = lattice.apply_v(y_tau, root_state)
    root_residual = abs(float(root_state[lattice.zero]))
    root_h = abs(float(root_v[lattice.zero]))

    carriers_float = lattice.carriers.astype(np.float64)
    carrier_square_sum = float(np.sum(carriers_float**2))
    carrier_formula = float(M * (28 * M * M - 1) / 3)
    K_s = carrier_square_sum
    K_v = args.amplitude**2 * K_s
    E_0 = float(np.dot(launch, launch))
    K_f = float(np.sum(lattice.modes**2 * launch**2))
    rho_squared = 2.0 * args.amplitude**2 * M
    B_squared = 2.0 * args.amplitude**2 * (K_s + args.mu * M)
    B_value = math.sqrt(B_squared)
    profile_moment = float(
        np.sum(
            carriers_float**2
            * args.amplitude**2
            * np.array(
                [
                    phi_grid(
                        2.0 * args.window * carrier**2,
                        args.phi_nodes,
                    )
                    for carrier in carriers_float
                ]
            )
        )
    )

    coupling_shape = lattice.delta * args.amplitude
    parity_even_scale = coupling_shape / M
    parity_cubic_scale = args.amplitude**2 * coupling_shape**2 / M
    max_even_norm = max(
        abs(float(launch[lattice.zero])),
        float(np.max(values["evenNorm"])),
    )

    # Exact physical amplitude balance with q=nu=d=Kz=1.
    P_squared = lattice.delta**2
    S_squared = 3.0 * P_squared * K_v / K_f
    physical_E = S_squared * K_f + P_squared * K_v
    D_proxy = physical_E
    theta = S_squared * P_squared / physical_E
    # The raw Lamb action carries the factor 2, while the canonical
    # Gamma-normalization has Gamma=q^2 X/(2 nu)=X/2 here.  Their product is
    # therefore theta * Q_*/window, matching the producer convention.
    physical_action = theta * critical_action / args.window
    lambda_star_proxy = 1.0 + physical_action
    D_one_third = D_proxy ** (1.0 / 3.0)
    candidate_scale = D_one_third * lambda_star_proxy

    lifted_first = theta * E_0 * rho_squared
    lifted_lambda = theta * 2.0 * args.mu**2 * critical_action
    lifted_mixed = theta * 12.0 * math.sqrt(
        args.mu * E_0 * profile_moment * critical_action
    )
    lifted_generic_b = (
        theta
        * 2.0
        * lattice.delta
        * math.sqrt(args.mu)
        * B_value
        * critical_action
    )
    lifted_measured_cubic = theta * 2.0 * cubic_integral
    lifted_root_atom = theta * root_h**2
    lifted_m2_complete_scale = theta * args.amplitude**2 * M**2

    expected_mixed = args.amplitude**2 * M**2
    expected_action = (
        args.amplitude**2 * M ** (2.0 / 3.0) * math.log(M)
    )
    expected_moment = (
        args.amplitude**2 * M ** (7.0 / 3.0) / math.log(M)
    )
    expected_reciprocal = (
        args.amplitude**2 * M ** (10.0 / 3.0) / math.log(M)
    )

    elapsed = time.perf_counter() - started
    row: dict[str, Any] = {
        "M": M,
        "delta": lattice.delta,
        "dimension": lattice.dimension,
        "carrierMin": int(lattice.carriers[0]),
        "carrierMax": int(lattice.carriers[-1]),
        "carrierSquareSum": K_s,
        "carrierFormula": carrier_formula,
        "carrierFormulaRelativeError": abs(K_s - carrier_formula) / carrier_formula,
        "Kf": K_f,
        "Kv": K_v,
        "E0": E_0,
        "rhoSquared": rho_squared,
        "BSquared": B_squared,
        "profileMoment": profile_moment,
        "zeta": zeta,
        "zetaScaledByGMminus2": abs(zeta) / (coupling_shape * M**-2),
        "launchNormalization": launch_normalization,
        "algebraicRootResidual": algebraic_residual,
        "evolvedRootResidual": root_residual,
        "rootH": root_h,
        "rootHNormalized": root_h / (args.amplitude * M),
        "mixedRow": mixed_row,
        "criticalAction": critical_action,
        "reciprocalQf": reciprocal_qf,
        "deltaAbsHbIntegral": cubic_integral,
        "maxEvenNorm": max_even_norm,
        "maxOddNorm": float(np.max(values["oddNorm"])),
        "mixedRowNormalized": mixed_row / expected_mixed,
        "criticalActionNormalized": critical_action / expected_action,
        "profileMomentNormalized": profile_moment / expected_moment,
        "reciprocalQfNormalized": reciprocal_qf / expected_reciprocal,
        "evenNormParityRatio": max_even_norm / parity_even_scale,
        "cubicParityRatio": cubic_integral / parity_cubic_scale,
        "P2": P_squared,
        "S2": S_squared,
        "physicalE": physical_E,
        "DProxy": D_proxy,
        "theta": theta,
        "physicalCriticalAction": physical_action,
        "lambdaStarProxy": lambda_star_proxy,
        "candidateScale": candidate_scale,
        "liftedFirst": lifted_first,
        "liftedLambda": lifted_lambda,
        "liftedMixed": lifted_mixed,
        "liftedGenericB": lifted_generic_b,
        "liftedMeasuredCubic": lifted_measured_cubic,
        "liftedRootAtom": lifted_root_atom,
        "liftedM2CompleteScale": lifted_m2_complete_scale,
        "liftedFirstRatio": lifted_first / candidate_scale,
        "liftedLambdaRatio": lifted_lambda / candidate_scale,
        "liftedMixedRatio": lifted_mixed / candidate_scale,
        "liftedGenericBRatio": lifted_generic_b / candidate_scale,
        "liftedMeasuredCubicRatio": lifted_measured_cubic / candidate_scale,
        "liftedRootAtomRatio": lifted_root_atom / candidate_scale,
        "liftedM2CompleteRatio": lifted_m2_complete_scale / candidate_scale,
        "genericBRouteScaled": (
            lifted_generic_b / candidate_scale
        ) / (math.sqrt(M) * math.log(M)),
        "physicalActionScaled": physical_action
        / (M ** (-1.0 / 3.0) * math.log(M)),
        "thetaScaled": theta * M,
        "DScaled": D_proxy / M**5,
        "solverNfev": int(solution.nfev),
        "elapsedSeconds": elapsed,
        "maxRssMb": max_rss_mb(),
    }
    append_ndjson(
        progress_path,
        {
            "time": utc_now(),
            "event": "case_complete",
            "M": M,
            "rootResidual": root_residual,
            "mixedRowNormalized": row["mixedRowNormalized"],
            "criticalActionNormalized": row["criticalActionNormalized"],
            "cubicParityRatio": row["cubicParityRatio"],
            "genericBRouteScaled": row["genericBRouteScaled"],
        },
    )
    append_ndjson(
        resource_path,
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
        f"Qnorm={row['criticalActionNormalized']:.6g} "
        f"cubic/parity={row['cubicParityRatio']:.6g} "
        f"Broute/(sqrtM logM)={row['genericBRouteScaled']:.6g} "
        f"root={root_residual:.3e}",
        flush=True,
    )
    return row


def log_slope(cases: list[dict[str, Any]], key: str) -> float:
    m_values = np.array([case["M"] for case in cases], dtype=np.float64)
    values = np.array([case[key] for case in cases], dtype=np.float64)
    if np.any(values <= 0.0):
        return float("nan")
    return float(np.polyfit(np.log(m_values), np.log(values), 1)[0])


def bounded_spread(cases: list[dict[str, Any]], key: str) -> float:
    values = np.array([case[key] for case in cases], dtype=np.float64)
    return float(np.max(values) / np.min(values))


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
    parser.add_argument("--y-max", type=float, default=12.0)
    parser.add_argument("--quad-order", type=int, default=280)
    parser.add_argument("--phi-nodes", type=int, default=26001)
    parser.add_argument("--truncation-factor", type=int, default=9)
    parser.add_argument("--rtol", type=float, default=5.0e-10)
    parser.add_argument("--atol", type=float, default=5.0e-12)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.window <= 0.0 or args.y_max <= 0.0:
        raise ValueError("window and y-max must be positive")
    if args.y_max / min(args.m_values) ** 2 >= args.window:
        raise ValueError("quadrature tail must stay inside the declared window")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    progress_path = args.output_dir / "independent-progress.ndjson"
    resource_path = args.output_dir / "independent-resource.ndjson"
    progress_path.write_text("", encoding="utf-8")
    resource_path.write_text("", encoding="utf-8")

    config = {
        "schemaVersion": 1,
        "audit": "R0.72I independent odd-parity absorption audit",
        "mValues": args.m_values,
        "deltaRule": "delta=M",
        "amplitude": args.amplitude,
        "mu": args.mu,
        "window": args.window,
        "yMax": args.y_max,
        "quadOrder": args.quad_order,
        "phiNodes": args.phi_nodes,
        "truncationFactor": args.truncation_factor,
        "rtol": args.rtol,
        "atol": args.atol,
        "signGenerator": "parity of overlapping adjacent binary 11 blocks",
        "gauge": "exact all-odd real gauge",
        "solver": "SciPy RK45 after y=M^2 x",
        "quadrature": "Gauss-Legendre after y=z^3",
        "producerImported": False,
        "physicalNormalization": {
            "q": 1,
            "nu": 1,
            "d": 1,
            "Kz": 1,
            "exactBalance": "S^2 Kf = 3 P^2 Kv",
            "DProxy": "S^2 Kf + P^2 Kv",
            "YProxy": "DProxy",
        },
    }
    (args.output_dir / "independent-config.json").write_text(
        json.dumps(config, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    append_ndjson(
        progress_path,
        {"time": utc_now(), "event": "audit_start", "config": config},
    )

    cases = [
        run_case(M, args, progress_path, resource_path) for M in args.m_values
    ]
    slopes = {
        "criticalAction": log_slope(cases, "criticalAction"),
        "deltaAbsHbIntegral": log_slope(cases, "deltaAbsHbIntegral"),
        "maxEvenNorm": log_slope(cases, "maxEvenNorm"),
        "liftedGenericBRatio": log_slope(cases, "liftedGenericBRatio"),
        "liftedM2CompleteRatio": log_slope(cases, "liftedM2CompleteRatio"),
    }
    checks = {
        "deltaEqualsM": all(case["delta"] == case["M"] for case in cases),
        "allCarriersOdd": all(
            case["carrierMin"] % 2 == 1 and case["carrierMax"] % 2 == 1
            for case in cases
        ),
        "exactCarrierMoment": max(
            case["carrierFormulaRelativeError"] for case in cases
        ) < 2.0e-15,
        "rootCorrectionRealAndAccurate": max(
            case["evolvedRootResidual"] for case in cases
        ) < 5.0e-8,
        "rootSlopeNondegenerate": cases[-1]["rootHNormalized"] > 0.65,
        "criticalActionScaleStable": bounded_spread(
            cases, "criticalActionNormalized"
        ) < 3.5,
        "profileMomentScaleStable": bounded_spread(
            cases, "profileMomentNormalized"
        ) < 3.5,
        "evenParityBoundObserved": max(
            case["evenNormParityRatio"] for case in cases
        ) < 8.0,
        "cubicParityBoundObserved": max(
            case["cubicParityRatio"] for case in cases
        ) < 8.0,
        "physicalDScaleExact": bounded_spread(cases, "DScaled") < 1.2,
        "physicalThetaScaleExact": bounded_spread(
            cases, "thetaScaled"
        ) < 1.2,
        "genericBRouteShowsGrowth": (
            cases[-1]["liftedGenericBRatio"]
            > cases[0]["liftedGenericBRatio"]
            and bounded_spread(cases, "genericBRouteScaled") < 3.5
        ),
        "measuredCubicRemainsPayable": max(
            case["liftedMeasuredCubicRatio"] for case in cases
        ) < 1.0,
        "m2CompleteScaleRemainsPayable": max(
            case["liftedM2CompleteRatio"] for case in cases
        ) < 1.0,
    }
    passed = all(checks.values())
    result = {
        "schemaVersion": 1,
        "audit": "R0.72I independent odd-parity absorption audit",
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
            "binary64 finite truncations are not interval certificates",
            "the audit does not enumerate the complete temporal root set",
            "the physical lift uses the declared exact-balance D and Y proxy",
            "the all-odd parity repair does not cover mixed-parity carriers",
            "no producer code or producer output is imported",
        ],
    }
    result_path = args.output_dir / "independent-result.json"
    result_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    csv_path = args.output_dir / "independent-data.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(cases[0].keys()),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(cases)
    append_ndjson(
        progress_path,
        {
            "time": utc_now(),
            "event": "audit_complete",
            "status": result["status"],
            "checks": checks,
        },
    )
    append_ndjson(
        resource_path,
        {
            "time": utc_now(),
            "event": "audit_complete",
            "cases": len(cases),
            "maxRssMb": max_rss_mb(),
            "status": result["status"],
        },
    )
    print(
        json.dumps(
            {
                "status": result["status"],
                "checks": checks,
                "maxRssMb": max_rss_mb(),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
