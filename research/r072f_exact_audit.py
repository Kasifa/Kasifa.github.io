#!/usr/bin/env python3
"""Producer-side finite audit for the R0.72F critical-log repair.

This corroborative binary64 calculation evolves the exact one-carrier lattice
with a time-dependent Strang split-step Fourier method.  It integrates the
singular initial-layer weights by using their exact zeroth and first moments
on every time step, compares a fine and a coarse discretization, rebuilds the
frozen Bessel mass, and checks the rational exponent frontier.  It is not an
interval proof and does not control the complete root set.
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
from typing import Any, Iterable

import numpy as np
import scipy
from scipy.special import jn_zeros, jv


Q0 = 4
MU = Q0**-2
X_MAX = 1.0
DELTAS = (16, 32, 64, 128, 256, 512)
WEIGHTS = (
    (Fraction(1, 4), 0, "beta-1-4"),
    (Fraction(1, 3), 0, "plain-one-third"),
    (Fraction(1, 3), 1, "critical-log"),
    (Fraction(2, 5), 0, "beta-2-5"),
    (Fraction(49, 100), 0, "beta-49-100"),
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace(
        "+00:00", "Z"
    )


def rss_bytes() -> int:
    value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return value if sys.platform == "darwin" else 1024 * value


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
        common = {
            "schemaVersion": "r072f-monitor-v1",
            "timestampUtc": utc_now(),
            "stage": stage,
            "message": message,
            "elapsedSeconds": elapsed,
            **fields,
        }
        print(
            f"[{common['timestampUtc']}] [{stage}] +{elapsed:.2f}s {message}",
            file=sys.stderr,
            flush=True,
        )
        if self.progress is not None:
            with self.progress.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(common, sort_keys=True) + "\n")
        if self.resources is not None:
            row = {
                **common,
                "processCpuSeconds": time.process_time() - self.cpu_started,
                "peakRssBytes": rss_bytes(),
                "logicalCpus": int(os.cpu_count() or 1),
            }
            with self.resources.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(row, sort_keys=True) + "\n")


def primitive(power: float, gamma: int, x: float, x_max: float) -> float:
    """Primitive of x**(power-1) * (1+log(X/x))**gamma at x."""

    if x == 0.0:
        return 0.0
    if gamma == 0:
        return x**power / power
    if gamma == 1:
        return x**power / power * (1.0 + math.log(x_max / x) + 1.0 / power)
    raise ValueError("the producer uses only gamma=0 or gamma=1")


def weight_moment(
    beta: float, gamma: int, degree: int, left: float, right: float
) -> float:
    power = degree + 1.0 - beta
    return X_MAX**beta * (
        primitive(power, gamma, right, X_MAX)
        - primitive(power, gamma, left, X_MAX)
    )


def weighted_linear_increment(
    left: float,
    right: float,
    g_left: float,
    g_right: float,
    beta: float,
    gamma: int,
) -> float:
    mass = weight_moment(beta, gamma, 0, left, right)
    if right == left:
        return 0.0
    first = weight_moment(beta, gamma, 1, left, right)
    return (
        g_left * (right * mass - first)
        + g_right * (first - left * mass)
    ) / (right - left)


def action_integrand(coefficients: np.ndarray, modes: np.ndarray, x: float) -> float:
    shifted = np.zeros_like(coefficients)
    factor = -1j * math.exp(-x)
    shifted[1:] += factor * coefficients[:-1]
    shifted[:-1] += factor * coefficients[1:]
    return float(
        np.sum(np.abs(shifted) ** 2 / (modes * modes + MU), dtype=np.float64)
    )


def solve_split(
    delta: float,
    modes_count: int,
    phase_step: float,
    maximum_step: float,
) -> dict[str, Any]:
    modes = np.arange(-modes_count // 2, modes_count // 2, dtype=np.float64)
    theta = 2.0 * math.pi * np.arange(modes_count, dtype=np.float64) / modes_count
    cosine = np.cos(theta)
    diagonal = modes * modes + MU
    state = np.zeros(modes_count, dtype=np.complex128)
    state[modes_count // 2 - 1] = 1j
    actions = {label: 0.0 for _, _, label in WEIGHTS}
    x = 0.0
    steps = 0
    g_left = action_integrand(state, modes, x)
    maximum_norm = 1.0
    maximum_tail = 0.0

    while x < X_MAX - 1.0e-15:
        amplitude = delta * math.exp(-x)
        step = min(maximum_step, phase_step / amplitude, X_MAX - x)
        heat = np.exp(-0.5 * step * diagonal)
        state *= heat
        integrated_phase = delta * (math.exp(-x) - math.exp(-(x + step)))
        grid = np.fft.ifft(np.fft.ifftshift(state)) * modes_count
        grid *= np.exp(-2j * integrated_phase * cosine)
        state = np.fft.fftshift(np.fft.fft(grid) / modes_count)
        state *= heat
        right = x + step
        g_right = action_integrand(state, modes, right)
        for beta_fraction, gamma, label in WEIGHTS:
            actions[label] += weighted_linear_increment(
                x,
                right,
                g_left,
                g_right,
                float(beta_fraction),
                gamma,
            )
        x = right
        g_left = g_right
        steps += 1
        energy = np.abs(state) ** 2
        norm = float(np.sum(energy))
        maximum_norm = max(maximum_norm, norm)
        tail = float(np.sum(energy[np.abs(modes) >= 0.4 * modes_count])) / max(
            norm, 1.0e-300
        )
        maximum_tail = max(maximum_tail, tail)

    return {
        "delta": delta,
        "modes": modes_count,
        "steps": steps,
        "actions": actions,
        "maximumL2Squared": maximum_norm,
        "maximumSpectralTailFraction": maximum_tail,
        "finalL2Squared": float(np.sum(np.abs(state) ** 2)),
    }


def fit(xs: Iterable[float], ys: Iterable[float]) -> dict[str, float]:
    x = np.log(np.asarray(tuple(xs), dtype=float))
    y = np.log(np.asarray(tuple(ys), dtype=float))
    slope, intercept = np.polyfit(x, y, 1)
    predicted = slope * x + intercept
    residual = y - predicted
    total = y - np.mean(y)
    denominator = float(np.dot(total, total))
    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "rSquared": 1.0
        if denominator == 0.0
        else 1.0 - float(np.dot(residual, residual)) / denominator,
    }


def check(name: str, passed: bool, value: Any, requirement: str) -> dict[str, Any]:
    return {
        "name": name,
        "passed": bool(passed),
        "value": value,
        "requirement": requirement,
    }


def bessel_rows() -> list[dict[str, float]]:
    maximum = 128
    roots = np.asarray(jn_zeros(1, maximum), dtype=float)
    slopes = 2.0 * np.asarray(jv(0, roots), dtype=float)
    cumulative = np.cumsum(slopes**2)
    target = 8.0 / math.pi**2
    return [
        {
            "R": count,
            "selectedSlopeMass": float(cumulative[count - 1]),
            "massOverLogR": float(cumulative[count - 1] / math.log(count)),
            "targetEightOverPiSquared": target,
            "relativeTargetError": abs(
                float(cumulative[count - 1] / math.log(count)) - target
            )
            / target,
            "maximumRootResidual": float(
                np.max(np.abs(jv(1, roots[:count])))
            ),
        }
        for count in (8, 16, 32, 64, 128)
    ]


def frontier_ledger() -> dict[str, Any]:
    vertices = [
        {
            "name": "critical-log-action",
            "a": Fraction(1, 3),
            "c": Fraction(0),
            "beta": Fraction(1, 3),
            "gamma": 1,
            "alpha": Fraction(0),
        },
        {
            "name": "explicit-coupling",
            "a": Fraction(1, 3),
            "c": Fraction(1, 3),
            "beta": Fraction(0),
            "gamma": 0,
            "alpha": Fraction(0),
        },
        {
            "name": "root-weight",
            "a": Fraction(1, 3),
            "c": Fraction(0),
            "beta": Fraction(0),
            "gamma": 0,
            "alpha": Fraction(4, 9),
        },
    ]
    rows = []
    for item in vertices:
        raw_sum = 2 * item["a"] + item["c"] + item["beta"]
        weighted_sum = raw_sum + 3 * item["alpha"] / 4
        rows.append(
            {
                **{
                    key: str(value) if isinstance(value, Fraction) else value
                    for key, value in item.items()
                },
                "rawFrontierSum": str(raw_sum),
                "weightedFrontierSum": str(weighted_sum),
                "onDeclaredBoundary": bool(
                    (item["alpha"] == 0 and raw_sum == 1)
                    or (item["alpha"] > 0 and weighted_sum == 1)
                ),
            }
        )
    return {
        "positiveBetaRawNecessaryCondition": "2*a+c+beta>1, or equality with gamma>=1",
        "betaZeroRawNecessaryCondition": "2*a+c>=1 from the separate logarithmic endpoint law",
        "weightedNecessaryCondition": "2*a+c+beta+3*alpha/4>=1 for alpha>0",
        "vertices": rows,
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
    fine_rows: list[dict[str, Any]] = []
    monitor.event("start", "R0.72F producer audit started", smoke=args.smoke)
    for delta in deltas:
        monitor.event("solve", f"delta={delta}: coarse split-step", delta=delta)
        coarse = solve_split(float(delta), 256, 0.12, 0.02)
        monitor.event("solve", f"delta={delta}: fine split-step", delta=delta)
        fine = solve_split(float(delta), 512, 0.06, 0.01)
        relative = {
            label: abs(fine["actions"][label] - coarse["actions"][label])
            / fine["actions"][label]
            for _, _, label in WEIGHTS
        }
        normalized: dict[str, float] = {}
        physical: dict[str, float] = {}
        for beta_fraction, gamma, label in WEIGHTS:
            beta = float(beta_fraction)
            q_value = fine["actions"][label]
            normalized[label] = (
                q_value
                * float(delta) ** (1.0 - beta)
                / math.log(float(delta)) ** gamma
            )
            physical[label] = (
                float(delta) / math.log(2.0 + float(delta)) * q_value
            )
        fine_rows.append(
            {
                **fine,
                "coarseModes": coarse["modes"],
                "coarseActions": coarse["actions"],
                "fineCoarseRelativeDifferences": relative,
                "asymptoticNormalizations": normalized,
                "physicalWeightedActions": physical,
                "criticalSelectedRatioProxy": (
                    float(delta) ** (1.0 / 3.0)
                    * math.log(float(delta))
                    / max(physical["critical-log"], 1.0e-300)
                ),
            }
        )
        monitor.event(
            "solve",
            f"delta={delta}: weighted actions complete",
            delta=delta,
            criticalLog=fine["actions"]["critical-log"],
            maximumRelativeDifference=max(relative.values()),
        )

    fits = {}
    for beta_fraction, gamma, label in WEIGHTS:
        q_values = [row["actions"][label] for row in fine_rows]
        normalized_values = [
            row["asymptoticNormalizations"][label] for row in fine_rows
        ]
        fits[label] = {
            "QAgainstDelta": fit(deltas, q_values),
            "normalizedAgainstDelta": fit(deltas, normalized_values),
            "expectedLeadingPower": float(beta_fraction) - 1.0,
            "expectedLogPower": gamma,
            "normalizedSpread": max(normalized_values) / min(normalized_values),
        }

    bessel = bessel_rows()
    frontier = frontier_ledger()
    all_relative = [
        value
        for row in fine_rows
        for value in row["fineCoarseRelativeDifferences"].values()
    ]
    all_normalized_spreads = [row["normalizedSpread"] for row in fits.values()]
    checks = [
        check(
            "critical_weight_l2_identity",
            Fraction(1, 1) / Fraction(1, 3)
            + Fraction(2, 1) / Fraction(1, 3) ** 2
            + Fraction(2, 1) / Fraction(1, 3) ** 3
            == 75,
            75,
            "integral_0^1 s^(-2/3)(1+log(1/s))^2 ds equals 75",
        ),
        check(
            "positive_weighted_actions",
            all(
                value > 0.0
                for row in fine_rows
                for value in row["actions"].values()
            ),
            min(
                value for row in fine_rows for value in row["actions"].values()
            ),
            "every computed weighted action is positive",
        ),
        check(
            "fine_coarse_stability",
            max(all_relative) < (0.08 if args.smoke else 0.035),
            max(all_relative),
            "all weighted actions agree across discretizations within tolerance",
        ),
        check(
            "spectral_tail_negligible",
            max(row["maximumSpectralTailFraction"] for row in fine_rows) < 1.0e-10,
            max(row["maximumSpectralTailFraction"] for row in fine_rows),
            "outer spectral tail remains below 1e-10",
        ),
        check(
            "contractive_evolution",
            max(row["maximumL2Squared"] for row in fine_rows) <= 1.0 + 2.0e-10,
            max(row["maximumL2Squared"] for row in fine_rows),
            "split-step evolution is contractive to tolerance",
        ),
        check(
            "regular_variation_normalizations",
            max(all_normalized_spreads) < 2.5,
            {label: row["normalizedSpread"] for label, row in fits.items()},
            "each theorem normalization varies by less than a factor 2.5",
        ),
        check(
            "bessel_mass_asymptotic",
            bessel[-1]["relativeTargetError"] < 0.05,
            bessel[-1]["relativeTargetError"],
            "R=128 frozen mass/log(R) is within 5 percent of 8/pi^2",
        ),
        check(
            "bessel_root_residual",
            max(row["maximumRootResidual"] for row in bessel) < 2.0e-13,
            max(row["maximumRootResidual"] for row in bessel),
            "SciPy Bessel roots have residual below 2e-13",
        ),
        check(
            "frontier_vertices_exact",
            all(row["onDeclaredBoundary"] for row in frontier["vertices"]),
            frontier["vertices"],
            "the three declared vertices satisfy the rational frontier exactly",
        ),
    ]
    result = {
        "schemaVersion": "r072f-producer-audit-v1",
        "auditId": "R0.72F-critical-log-producer",
        "createdAtUtc": utc_now(),
        "environment": {
            "python": sys.version,
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "logicalCpus": int(os.cpu_count() or 1),
        },
        "scope": {
            "intervalArithmetic": False,
            "completeRootUpperBound": False,
            "provesNSERegularity": False,
            "role": "finite corroboration of analytic exponents and constants",
        },
        "method": {
            "evolution": "time-dependent Strang split-step Fourier",
            "weightedQuadrature": "exact weight moments against piecewise-linear integrand",
            "fine": {"modes": 512, "phaseStep": 0.06, "maximumStep": 0.01},
            "coarse": {"modes": 256, "phaseStep": 0.12, "maximumStep": 0.02},
            "xMaximum": X_MAX,
            "weights": [
                {"beta": str(beta), "gamma": gamma, "label": label}
                for beta, gamma, label in WEIGHTS
            ],
        },
        "weightedActionRows": fine_rows,
        "fits": fits,
        "bessel": bessel,
        "frontier": frontier,
        "checks": checks,
        "allRequiredChecksPassed": all(row["passed"] for row in checks),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    monitor.event(
        "complete",
        "producer audit complete",
        passed=result["allRequiredChecksPassed"],
        output=str(args.output),
    )
    return 0 if result["allRequiredChecksPassed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
