#!/usr/bin/env python3
"""Independent finite audit for R0.72M.

This implementation does not import the producer.  It reconstructs the
zero-diffusion chain from Bessel recurrences without differentiated Bessel
calls, uses the angular generating function for Parseval checks, and uses a
finite-chain Cayley split for the dissipative diagnostic.
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
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import simpson
from scipy.linalg import solve_banded
from scipy.special import jv, roots_legendre


AUDIT_NAME = "R0.72M independent phase-mixing audit"
SCHEMA_VERSION = 1
MU = 1.0


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_ndjson(path: Path, payload: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"empty CSV: {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def git_commit(repository_root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(repository_root), "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "unavailable"


def max_rss_mb() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024.0 * 1024.0) if sys.platform == "darwin" else value / 1024.0


def resource_row(started: float, event: str) -> dict[str, Any]:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return {
        "time": utc_now(),
        "event": event,
        "elapsedSeconds": time.perf_counter() - started,
        "maxRssMb": max_rss_mb(),
        "userCpuSeconds": float(usage.ru_utime),
        "systemCpuSeconds": float(usage.ru_stime),
        "pid": os.getpid(),
    }


def relative_error(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def next_power_two(value: int) -> int:
    return 1 << max(1, value - 1).bit_length()


def cutoff(s_value: float) -> int:
    return max(64, int(math.ceil(2.0 * s_value + 22.0 * (1.0 + s_value) ** (1.0 / 3.0) + 44.0)))


def f_from_recurrence(modes: np.ndarray, s_value: float) -> np.ndarray:
    argument = 2.0 * s_value
    return (jv(modes - 1.0, argument) - jv(modes + 1.0, argument)) / math.sqrt(2.0)


def bf_from_recurrence(modes: np.ndarray, s_value: float) -> np.ndarray:
    argument = 2.0 * s_value
    return (
        jv(modes - 2.0, argument)
        - 2.0 * jv(modes, argument)
        + jv(modes + 2.0, argument)
    ) / math.sqrt(2.0)


def q_density(s_value: float) -> tuple[float, float, int]:
    nmax = cutoff(s_value)
    modes = np.arange(-nmax, nmax + 1, dtype=float)
    derivative = bf_from_recurrence(modes, s_value)
    value = float(np.sum(derivative * derivative / (MU + modes * modes)))
    boundary = float(derivative[0] ** 2 + derivative[-1] ** 2)
    return value, boundary, nmax


def danger_window_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for u_value, v_value, k_value in (
        (7.0, 2.0, 0.5),
        (120.0, 5.0, 3.0),
        (4096.0, 16.0, 11.0),
        (1.0e7, 125.0, 37.0),
    ):
        h_value = u_value / v_value
        maximum = u_value / (k_value + h_value)
        grid = np.geomspace(1.0e-10, max(100.0 * h_value, 10.0), 200_001)
        values = np.minimum(u_value, v_value * grid) / (k_value + grid)
        sampled_maximum = float(np.max(values))
        for fraction in (0.2, 0.7, 1.0, 1.3):
            threshold = fraction * maximum
            observed = grid[values > threshold]
            nonempty = fraction < 1.0
            if nonempty:
                left = threshold * k_value / (v_value - threshold)
                right = u_value / threshold - k_value
                bracketed = observed.size > 0 and observed[0] >= left * (1.0 - 3.0e-4) and observed[-1] <= right * (1.0 + 3.0e-4)
            else:
                left = math.nan
                right = math.nan
                bracketed = observed.size == 0
            rows.append(
                {
                    "U": u_value,
                    "V": v_value,
                    "K": k_value,
                    "H": h_value,
                    "thresholdFraction": fraction,
                    "threshold": threshold,
                    "maximum": maximum,
                    "sampledMaximum": sampled_maximum,
                    "leftEndpoint": left,
                    "rightEndpoint": right,
                    "nonempty": nonempty,
                    "classificationPassed": bracketed
                    and relative_error(sampled_maximum, maximum) < 2.0e-4,
                }
            )
    return rows


def angular_bessel_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for s_value in (0.0, 0.5, 2.0, 8.0, 32.0, 128.0, 512.0):
        grid = next_power_two(max(2048, int(16.0 * s_value + 1024.0)))
        theta = 2.0 * math.pi * np.arange(grid) / grid
        generating = 1j * math.sqrt(2.0) * np.sin(theta) * np.exp(
            2j * s_value * np.sin(theta)
        )
        coefficients = np.fft.fft(generating) / grid
        modes = np.fft.fftfreq(grid, 1.0 / grid)
        mass = float(np.sum(np.abs(coefficients) ** 2))
        moment = float(np.sum(modes * modes * np.abs(coefficients) ** 2))
        expected = 1.0 + s_value * s_value
        high = float(np.sum(np.abs(coefficients[np.abs(modes) > 0.4 * grid]) ** 2))
        rows.append(
            {
                "s": s_value,
                "grid": grid,
                "mass": mass,
                "massError": abs(mass - 1.0),
                "gradientMoment": moment,
                "expectedGradientMoment": expected,
                "gradientRelativeError": relative_error(moment, expected),
                "boundaryMass": high,
                "passed": abs(mass - 1.0) < 2.0e-12
                and relative_error(moment, expected) < 2.0e-11
                and high < 1.0e-20,
            }
        )
    return rows


def action_value(sigma: float, order: int = 160) -> tuple[float, float, int]:
    nodes, weights = roots_legendre(order)
    r_values = 0.5 * (nodes + 1.0)
    weights = 0.5 * weights
    total = 0.0
    max_boundary = 0.0
    max_cutoff = 0
    for r_value, weight in zip(r_values, weights, strict=True):
        y_value = float(r_value ** 1.5)
        s_value = sigma * (1.0 - math.exp(-y_value))
        q_value, boundary, nmax = q_density(s_value)
        transformed = 1.5 * (
            1.0 + 1.5 * math.log(1.0 / float(r_value))
        ) * math.exp(-2.0 * (1.0 + MU) * y_value)
        total += float(weight) * transformed * q_value
        max_boundary = max(max_boundary, boundary)
        max_cutoff = max(max_cutoff, nmax)
    return total, max_boundary, max_cutoff


def action_rows(progress: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case, sigma in enumerate((16.0, 32.0, 64.0, 128.0, 256.0, 512.0), start=1):
        value, boundary, nmax = action_value(sigma)
        row = {
            "sigma": sigma,
            "action": value,
            "scaledAction": value * sigma ** (2.0 / 3.0) / math.log(sigma),
            "maxBoundaryDerivativeMass": boundary,
            "maxCutoff": nmax,
            "passed": value > 0.0 and math.isfinite(value) and boundary < 1.0e-18,
        }
        rows.append(row)
        append_ndjson(progress, {"time": utc_now(), "stage": "action", "case": case, **row})
    return rows


def frozen_cubic(sigma: float, step: float) -> float:
    endpoint = sigma * (1.0 - math.exp(-1.0))
    count = int(math.ceil(endpoint / step)) + 1
    s_values = np.linspace(0.0, endpoint, count)
    argument = 2.0 * s_values
    u_values = (jv(0, argument) - jv(2, argument)) / math.sqrt(2.0)
    derivative = (jv(3, argument) - 3.0 * jv(1, argument)) / math.sqrt(2.0)
    weight = np.power(1.0 - s_values / sigma, 2.0 + 2.0 * MU)
    return float(simpson(4.0 * weight * np.abs(u_values * derivative), x=s_values))


def frozen_cubic_rows(progress: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    target = 16.0 / math.pi**2
    for case, sigma in enumerate((16.0, 32.0, 64.0, 128.0, 256.0, 512.0, 1024.0, 2048.0), start=1):
        value = frozen_cubic(sigma, 0.008)
        fine = frozen_cubic(sigma, 0.004) if sigma in (128.0, 512.0, 2048.0) else value
        row = {
            "sigma": sigma,
            "cubic": value,
            "cubicOverLogSigma": value / math.log(sigma),
            "asymptoticConstant": target,
            "fineCubic": fine,
            "stepRelativeDifference": relative_error(value, fine),
            "cubicOverSigma": value / sigma,
            "passed": value > 0.0 and relative_error(value, fine) < 2.0e-5,
        }
        rows.append(row)
        append_ndjson(progress, {"time": utc_now(), "stage": "frozen-cubic", "case": case, **row})
    return rows


def dissipative_cayley(sigma: float, step_scale: float) -> dict[str, float]:
    nmax = max(48, int(math.ceil(12.0 + 5.0 * math.sqrt(sigma))))
    modes = np.arange(-nmax, nmax + 1, dtype=float)
    state = np.zeros(modes.size, dtype=float)
    state[nmax + 1] = 1.0 / math.sqrt(2.0)
    state[nmax - 1] = -1.0 / math.sqrt(2.0)
    steps = int(math.ceil(math.sqrt(sigma) / step_scale))
    step = 1.0 / steps
    half_heat = np.exp(-modes * modes * step / 2.0)

    def integrand(y_value: float) -> float:
        return 4.0 * sigma * math.exp(-(3.0 + 2.0 * MU) * y_value) * abs(
            state[nmax + 1] * (state[nmax] - state[nmax + 2])
        )

    y_value = 0.0
    previous = integrand(y_value)
    integral = 0.0
    for _ in range(steps):
        state *= half_heat
        midpoint = y_value + step / 2.0
        alpha = step * sigma * math.exp(-midpoint)
        rhs = state.copy()
        rhs[1:] += 0.5 * alpha * state[:-1]
        rhs[:-1] -= 0.5 * alpha * state[1:]
        matrix = np.zeros((3, state.size), dtype=float)
        matrix[0, 1:] = 0.5 * alpha
        matrix[1, :] = 1.0
        matrix[2, :-1] = -0.5 * alpha
        state = solve_banded(
            (1, 1), matrix, rhs, overwrite_ab=True, overwrite_b=True, check_finite=False
        )
        state *= half_heat
        y_value += step
        current = integrand(y_value)
        integral += 0.5 * (previous + current) * step
        previous = current
    return {
        "cubic": integral,
        "steps": float(steps),
        "nmax": float(nmax),
        "boundaryMass": float(state[0] ** 2 + state[-1] ** 2),
        "finalNormSquared": float(np.dot(state, state)),
    }


def dissipative_rows(progress: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case, sigma in enumerate((32.0, 128.0, 512.0, 2048.0), start=1):
        fine = dissipative_cayley(sigma, 0.000625)
        coarse = dissipative_cayley(sigma, 0.00125)
        row = {
            "sigma": sigma,
            "cubic": fine["cubic"],
            "coarseCubic": coarse["cubic"],
            "timeRefinementRelativeDifference": relative_error(fine["cubic"], coarse["cubic"]),
            "cubicOverLogSigma": fine["cubic"] / math.log(sigma),
            "steps": int(fine["steps"]),
            "nmax": int(fine["nmax"]),
            "boundaryMass": fine["boundaryMass"],
            "finalNormSquared": fine["finalNormSquared"],
            "passed": relative_error(fine["cubic"], coarse["cubic"]) < 0.006
            and fine["boundaryMass"] < 1.0e-18,
        }
        rows.append(row)
        append_ndjson(progress, {"time": utc_now(), "stage": "dissipative", "case": case, **row})
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    repository_root = Path(__file__).resolve().parents[1]
    started = time.perf_counter()
    progress = output / "independent-progress.ndjson"
    resources = output / "independent-resource.ndjson"
    monitor = output / "independent-monitor.log"
    for path in (progress, resources, monitor):
        path.write_text("", encoding="utf-8")

    config = {
        "schemaVersion": SCHEMA_VERSION,
        "audit": AUDIT_NAME,
        "mu": MU,
        "actionQuadratureOrder": 160,
        "frozenCubicStep": 0.008,
        "dissipativeMethod": "finite-chain diagonal/Cayley Strang split",
        "dissipativeFineStepScale": 0.000625,
        "dissipativeCoarseStepScale": 0.00125,
        "gitCommit": git_commit(repository_root),
    }
    (output / "independent-config.json").write_text(
        json.dumps(config, indent=2) + "\n", encoding="utf-8"
    )
    environment = {
        "python": sys.version,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scipy": __import__("scipy").__version__,
        "cpuCount": os.cpu_count(),
    }
    (output / "independent-environment.txt").write_text(
        "\n".join(f"{key}={value}" for key, value in environment.items()) + "\n",
        encoding="utf-8",
    )
    append_ndjson(progress, {"time": utc_now(), "stage": "start", "config": config})
    append_ndjson(resources, resource_row(started, "start"))

    stages: list[tuple[str, list[dict[str, Any]]]] = [
        ("danger-window", danger_window_rows()),
        ("bessel", angular_bessel_rows()),
        ("action", action_rows(progress)),
        ("frozen-cubic", frozen_cubic_rows(progress)),
        ("dissipative", dissipative_rows(progress)),
    ]
    for name, rows in stages:
        write_csv(output / f"independent-{name}.csv", rows)
        append_ndjson(progress, {"time": utc_now(), "stage": name, "status": "complete", "rows": len(rows)})
        append_ndjson(resources, resource_row(started, name))

    checks = {
        "dangerWindow": all(bool(row["classificationPassed"]) for row in stages[0][1]),
        "angularParseval": all(bool(row["passed"]) for row in stages[1][1]),
        "actionFinite": all(bool(row["passed"]) for row in stages[2][1]),
        "actionScaledStable": max(row["scaledAction"] for row in stages[2][1][-3:])
        / min(row["scaledAction"] for row in stages[2][1][-3:])
        < 1.25,
        "frozenCubic": all(bool(row["passed"]) for row in stages[3][1]),
        "frozenCubicSublinear": stages[3][1][-1]["cubicOverSigma"] < 0.01,
        "dissipativeConvergence": all(bool(row["passed"]) for row in stages[4][1]),
    }
    result = {
        "schemaVersion": SCHEMA_VERSION,
        "audit": AUDIT_NAME,
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
        "counts": {name: len(rows) for name, rows in stages},
        "asymptoticCubicConstant": 16.0 / math.pi**2,
        "elapsedSeconds": time.perf_counter() - started,
        "maxRssMb": max_rss_mb(),
        "gitCommit": git_commit(repository_root),
        "limitations": [
            "finite binary64 corroboration only",
            "independent finite-chain cutoff is not an invariant PDE subsystem",
            "dissipative logarithmic growth is not proved",
            "no general three-dimensional regularity conclusion",
        ],
    }
    (output / "independent-result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    monitor.write_text(
        f"[{utc_now()}] status={result['status']} elapsed={result['elapsedSeconds']:.3f}s "
        f"checks={sum(checks.values())}/{len(checks)}\n",
        encoding="utf-8",
    )
    append_ndjson(resources, resource_row(started, "complete"))
    append_ndjson(progress, {"time": utc_now(), "stage": "complete", "status": result["status"]})
    print(json.dumps(result, indent=2))
    if result["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
