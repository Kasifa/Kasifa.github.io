#!/usr/bin/env python3
"""Independent BDF/Gauss audit for the R0.72F weighted action.

This program imports neither the producer nor producer output.  It evolves a
real invariant lattice with SciPy's implicit BDF solver and evaluates every
singular weighted action after the logarithmic change of variables
``x=exp(-z)`` using composite Gauss--Legendre quadrature plus an analytic
tail.  Radius, tolerance, and quadrature pressure checks are included.  The
calculation is finite-lattice binary64 corroboration, not an interval proof.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import json
import math
import os
from pathlib import Path
import resource
import sys
import time
from typing import Any

import numpy as np
import scipy
from scipy.integrate import quad, solve_ivp
from scipy.sparse import diags


Q0 = 4
MU = Q0**-2
DELTAS = (16.0, 32.0, 64.0, 128.0, 256.0, 512.0)
WEIGHTS = (
    (Fraction(1, 4), 0, "beta-1-4"),
    (Fraction(1, 3), 0, "plain-one-third"),
    (Fraction(1, 3), 1, "critical-log"),
    (Fraction(2, 5), 0, "beta-2-5"),
    (Fraction(49, 100), 0, "beta-49-100"),
)
PRIMARY_RADIUS = 64
PRESSURE_RADIUS = 88
PRIMARY_RTOL = 2.0e-9
PRIMARY_ATOL = 2.0e-11
TIGHT_RTOL = 4.0e-10
TIGHT_ATOL = 4.0e-12


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace(
        "+00:00", "Z"
    )


def peak_rss_bytes() -> int:
    raw = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return raw if sys.platform == "darwin" else 1024 * raw


class Monitor:
    def __init__(self, progress: Path | None, resources: Path | None) -> None:
        self.started = time.perf_counter()
        self.cpu_started = time.process_time()
        self.progress = progress
        self.resources = resources
        for path in (progress, resources):
            if path is not None:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("", encoding="utf-8")

    def event(self, stage: str, message: str, **fields: Any) -> None:
        elapsed = time.perf_counter() - self.started
        row = {
            "schemaVersion": "r072f-independent-monitor-v1",
            "timestampUtc": utc_now(),
            "stage": stage,
            "message": message,
            "elapsedSeconds": elapsed,
            **fields,
        }
        print(
            f"[{row['timestampUtc']}] [{stage}] +{elapsed:.2f}s {message}",
            file=sys.stderr,
            flush=True,
        )
        if self.progress is not None:
            with self.progress.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(row, sort_keys=True) + "\n")
        if self.resources is not None:
            resource_row = {
                **row,
                "processCpuSeconds": time.process_time() - self.cpu_started,
                "peakRssBytes": peak_rss_bytes(),
                "logicalCpus": int(os.cpu_count() or 1),
            }
            with self.resources.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(resource_row, sort_keys=True) + "\n")


def action_integrand(
    x_values: np.ndarray, states: np.ndarray, indices: np.ndarray
) -> np.ndarray:
    differences = np.zeros_like(states)
    differences[1:, :] += states[:-1, :]
    differences[:-1, :] -= states[1:, :]
    weights = 1.0 / (indices * indices + MU)
    return np.exp(-2.0 * x_values) * np.sum(
        weights[:, None] * differences**2, axis=0
    )


def transformed_action(
    solution: Any,
    indices: np.ndarray,
    beta: float,
    gamma: int,
    order: int,
) -> tuple[float, float]:
    """Integrate on the adaptive BDF mesh, with a transformed launch tail."""

    if solution.t.size < 2:
        raise RuntimeError("BDF solution has no positive mesh point")
    nodes, weights = np.polynomial.legendre.leggauss(order)
    total = 0.0
    positive_mesh = np.asarray(solution.t[1:], dtype=float)
    left_mesh = positive_mesh[:-1]
    right_mesh = positive_mesh[1:]
    for left, right in zip(left_mesh, right_mesh, strict=True):
        x = 0.5 * (right - left) * nodes + 0.5 * (right + left)
        states = np.asarray(solution.sol(x), dtype=float)
        g = action_integrand(x, states, indices)
        weighted = x ** (-beta) * (1.0 + np.log(1.0 / x)) ** gamma * g
        total += 0.5 * (right - left) * float(np.dot(weights, weighted))

    # The first BDF interval touches the singular endpoint.  Map it to a
    # logarithmic half-line and integrate to a point where the analytic tail
    # is far below the requested tolerance.
    first_positive = float(positive_mesh[0])
    z_start = -math.log(first_positive)
    z_max = max(60.0, z_start + 36.0)
    launch_order = max(16, 2 * order)
    launch_nodes, launch_weights = np.polynomial.legendre.leggauss(launch_order)
    left = z_start
    while left < z_max - 1.0e-15:
        right = min(z_max, left + 3.0)
        z = (
            0.5 * (right - left) * launch_nodes
            + 0.5 * (right + left)
        )
        x = np.exp(-z)
        states = np.asarray(solution.sol(x), dtype=float)
        g = action_integrand(x, states, indices)
        transformed = np.exp(-(1.0 - beta) * z) * (1.0 + z) ** gamma * g
        total += 0.5 * (right - left) * float(
            np.dot(launch_weights, transformed)
        )
        left = right

    initial = np.asarray(solution.sol(np.array([0.0])), dtype=float)
    g_zero = float(action_integrand(np.array([0.0]), initial, indices)[0])
    rate = 1.0 - beta
    if gamma == 0:
        tail = g_zero * math.exp(-rate * z_max) / rate
    elif gamma == 1:
        tail = g_zero * math.exp(-rate * z_max) * (
            (1.0 + z_max) / rate + 1.0 / rate**2
        )
    else:
        raise ValueError("the independent audit uses gamma 0 or 1")
    return total + tail, tail


def solve_case(
    delta: float,
    radius: int,
    rtol: float,
    atol: float,
    fine_order: int,
    coarse_order: int,
) -> dict[str, Any]:
    indices = np.arange(-radius, radius + 1, dtype=float)
    state = np.zeros(indices.size, dtype=float)
    state[radius - 1] = 1.0
    diagonal = -(indices * indices + MU)
    off = np.ones(indices.size - 1, dtype=float)

    def rhs(x: float, vector: np.ndarray) -> np.ndarray:
        derivative = diagonal * vector
        amplitude = delta * math.exp(-x)
        derivative[1:] += amplitude * vector[:-1]
        derivative[:-1] -= amplitude * vector[1:]
        return derivative

    def jacobian(x: float, _vector: np.ndarray):
        amplitude = delta * math.exp(-x)
        return diags(
            [amplitude * off, diagonal, -amplitude * off],
            [-1, 0, 1],
            format="csc",
        )

    started = time.perf_counter()
    solution = solve_ivp(
        rhs,
        (0.0, 1.0),
        state,
        method="BDF",
        rtol=rtol,
        atol=atol,
        jac=jacobian,
        dense_output=True,
        max_step=0.01,
    )
    if not solution.success or solution.sol is None:
        raise RuntimeError(f"BDF failure for delta={delta}: {solution.message}")

    actions: dict[str, float] = {}
    coarse_actions: dict[str, float] = {}
    tails: dict[str, float] = {}
    quadrature_defects: dict[str, float] = {}
    normalizations: dict[str, float] = {}
    for beta_fraction, gamma, label in WEIGHTS:
        beta = float(beta_fraction)
        value, tail = transformed_action(
            solution, indices, beta, gamma, fine_order
        )
        coarse, _ = transformed_action(
            solution, indices, beta, gamma, coarse_order
        )
        actions[label] = value
        coarse_actions[label] = coarse
        tails[label] = tail
        quadrature_defects[label] = abs(value - coarse) / value
        normalizations[label] = (
            value * delta ** (1.0 - beta) / math.log(delta) ** gamma
        )

    sample_x = np.concatenate(
        (np.array([0.0]), np.geomspace(1.0e-10, 1.0, 600))
    )
    sampled = np.asarray(solution.sol(sample_x), dtype=float)
    energies = np.sum(sampled**2, axis=0)
    edge = np.sum(sampled[:8, :] ** 2, axis=0) + np.sum(
        sampled[-8:, :] ** 2, axis=0
    )
    return {
        "delta": delta,
        "radius": radius,
        "dimension": int(indices.size),
        "rtol": rtol,
        "atol": atol,
        "nfev": int(solution.nfev),
        "njev": int(solution.njev),
        "nlu": int(solution.nlu),
        "actions": actions,
        "coarseActions": coarse_actions,
        "quadratureRelativeDefects": quadrature_defects,
        "analyticTailContributions": tails,
        "asymptoticNormalizations": normalizations,
        "maximumL2Squared": float(np.max(energies)),
        "finalL2Squared": float(energies[-1]),
        "maximumEdgeEnergyFraction": float(
            np.max(edge / np.maximum(energies, 1.0e-300))
        ),
        "elapsedSeconds": time.perf_counter() - started,
    }


def fit(xs: list[float], ys: list[float]) -> dict[str, float]:
    x = np.log(np.asarray(xs, dtype=float))
    y = np.log(np.asarray(ys, dtype=float))
    slope, intercept = np.polyfit(x, y, 1)
    return {"slope": float(slope), "intercept": float(intercept)}


def check(name: str, passed: bool, value: Any, requirement: str) -> dict[str, Any]:
    return {
        "name": name,
        "passed": bool(passed),
        "value": value,
        "requirement": requirement,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--progress-log", type=Path)
    parser.add_argument("--resource-log", type=Path)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    monitor = Monitor(args.progress_log, args.resource_log)
    deltas = DELTAS[:2] if args.smoke else DELTAS
    radius = 48 if args.smoke else PRIMARY_RADIUS
    fine_order = 10
    coarse_order = 6
    rows: list[dict[str, Any]] = []
    monitor.event("start", "R0.72F independent audit started", smoke=args.smoke)
    for delta in deltas:
        monitor.event("bdf", f"delta={delta:g}: primary solve", delta=delta)
        row = solve_case(
            delta,
            radius,
            PRIMARY_RTOL,
            PRIMARY_ATOL,
            fine_order,
            coarse_order,
        )
        rows.append(row)
        monitor.event(
            "bdf",
            f"delta={delta:g}: weighted actions complete",
            delta=delta,
            criticalLog=row["actions"]["critical-log"],
            nfev=row["nfev"],
        )

    pressure_delta = deltas[-1]
    pressure_radius = 64 if args.smoke else PRESSURE_RADIUS
    monitor.event("pressure", "larger-radius solve", delta=pressure_delta)
    radius_check = solve_case(
        pressure_delta,
        pressure_radius,
        PRIMARY_RTOL,
        PRIMARY_ATOL,
        fine_order,
        coarse_order,
    )
    monitor.event("pressure", "tighter-tolerance solve", delta=pressure_delta)
    tolerance_check = solve_case(
        pressure_delta,
        radius,
        TIGHT_RTOL,
        TIGHT_ATOL,
        fine_order,
        coarse_order,
    )
    primary = rows[-1]
    radius_differences = {
        label: abs(primary["actions"][label] - radius_check["actions"][label])
        / radius_check["actions"][label]
        for _, _, label in WEIGHTS
    }
    tolerance_differences = {
        label: abs(primary["actions"][label] - tolerance_check["actions"][label])
        / tolerance_check["actions"][label]
        for _, _, label in WEIGHTS
    }
    weight_integral, weight_error = quad(
        lambda z: math.exp(-z / 3.0) * (1.0 + z) ** 2,
        0.0,
        math.inf,
        epsabs=1.0e-12,
        epsrel=1.0e-12,
    )
    fits = {}
    spreads = {}
    for beta_fraction, gamma, label in WEIGHTS:
        values = [row["actions"][label] for row in rows]
        normalized = [row["asymptoticNormalizations"][label] for row in rows]
        fits[label] = {
            "QAgainstDelta": fit(list(deltas), values),
            "normalizedAgainstDelta": fit(list(deltas), normalized),
            "expectedLeadingPower": float(beta_fraction) - 1.0,
            "expectedLogPower": gamma,
        }
        spreads[label] = max(normalized) / min(normalized)

    quadrature_defects = [
        value
        for row in rows + [radius_check, tolerance_check]
        for value in row["quadratureRelativeDefects"].values()
    ]
    tails = [
        value
        for row in rows + [radius_check, tolerance_check]
        for value in row["analyticTailContributions"].values()
    ]
    checks = [
        check(
            "critical_weight_l2_quadrature",
            abs(weight_integral - 75.0) < 2.0e-10 and weight_error < 2.0e-10,
            {"integral": weight_integral, "reportedError": weight_error},
            "independent improper quadrature agrees with 75",
        ),
        check(
            "positive_weighted_actions",
            all(value > 0.0 for row in rows for value in row["actions"].values()),
            min(value for row in rows for value in row["actions"].values()),
            "all independent weighted actions are positive",
        ),
        check(
            "quadrature_pressure",
            max(quadrature_defects) < 2.0e-7,
            max(quadrature_defects),
            "fine/coarse transformed Gauss quadrature differs by less than 2e-7",
        ),
        check(
            "tail_negligible",
            max(tails) < 2.0e-10,
            max(tails),
            "largest analytic z-tail is below 2e-10",
        ),
        check(
            "lattice_boundary_negligible",
            max(
                row["maximumEdgeEnergyFraction"]
                for row in rows + [radius_check, tolerance_check]
            )
            < 1.0e-12,
            max(
                row["maximumEdgeEnergyFraction"]
                for row in rows + [radius_check, tolerance_check]
            ),
            "outer eight-mode energy fraction remains below 1e-12",
        ),
        check(
            "contractive_evolution",
            max(
                row["maximumL2Squared"]
                for row in rows + [radius_check, tolerance_check]
            )
            <= 1.0 + 2.0e-6,
            max(
                row["maximumL2Squared"]
                for row in rows + [radius_check, tolerance_check]
            ),
            "BDF evolution is contractive to tolerance",
        ),
        check(
            "radius_stability",
            max(radius_differences.values()) < 2.0e-5,
            radius_differences,
            "primary and larger-radius actions agree within 2e-5 relative",
        ),
        check(
            "tolerance_stability",
            max(tolerance_differences.values()) < 2.0e-5,
            tolerance_differences,
            "primary and tighter-tolerance actions agree within 2e-5 relative",
        ),
        check(
            "regular_variation_normalizations",
            max(spreads.values()) < 2.5,
            spreads,
            "each asymptotic normalization varies by less than a factor 2.5",
        ),
    ]
    result = {
        "schemaVersion": "r072f-independent-audit-v1",
        "auditId": "R0.72F-critical-log-independent",
        "createdAtUtc": utc_now(),
        "environment": {
            "python": sys.version,
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "logicalCpus": int(os.cpu_count() or 1),
        },
        "scope": {
            "importsProducer": False,
            "readsProducerOutput": False,
            "intervalArithmetic": False,
            "completeRootUpperBound": False,
            "provesNSERegularity": False,
        },
        "method": {
            "evolution": "adaptive implicit BDF on a real invariant lattice",
            "quadrature": "x=exp(-z), composite Gauss-Legendre, analytic tail",
            "primaryRadius": radius,
            "pressureRadius": pressure_radius,
            "fineGaussOrder": fine_order,
            "coarseGaussOrder": coarse_order,
            "zMaximum": 60.0,
        },
        "weightedActionRows": rows,
        "radiusPressure": {
            "row": radius_check,
            "relativeDifferences": radius_differences,
        },
        "tolerancePressure": {
            "row": tolerance_check,
            "relativeDifferences": tolerance_differences,
        },
        "criticalWeightL2": {
            "value": weight_integral,
            "reportedQuadratureError": weight_error,
            "exactTarget": 75,
        },
        "fits": fits,
        "checks": checks,
        "allRequiredChecksPassed": all(row["passed"] for row in checks),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    monitor.event(
        "complete",
        "independent audit complete",
        passed=result["allRequiredChecksPassed"],
        output=str(args.output),
    )
    return 0 if result["allRequiredChecksPassed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
