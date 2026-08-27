#!/usr/bin/env python3
"""Producer finite audit for R0.72M.

The analytic report is the proof.  This program checks the scalar danger
window, full-lattice Bessel identities, the complete negative-norm action
scaling, the frozen cubic logarithm, and a converged dissipative diagnostic.
All numerical output is finite binary64 corroboration, not an interval proof
or a Navier--Stokes regularity result.
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
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import simpson
from scipy.special import jvp, roots_legendre


AUDIT_NAME = "R0.72M producer phase-mixing audit"
SCHEMA_VERSION = 1
MU = 1.0
SEED = 72013


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


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


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
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


def lattice_cutoff(s_value: float) -> int:
    return max(64, int(math.ceil(2.0 * s_value + 20.0 * (1.0 + s_value) ** (1.0 / 3.0) + 40.0)))


def q_density(s_value: float, mu: float = MU) -> tuple[float, float, int]:
    nmax = lattice_cutoff(s_value)
    modes = np.arange(-nmax, nmax + 1, dtype=float)
    derivative = 2.0 * math.sqrt(2.0) * jvp(modes, 2.0 * s_value, 2)
    q_value = float(np.sum(derivative * derivative / (mu + modes * modes)))
    boundary = float(derivative[0] ** 2 + derivative[-1] ** 2)
    return q_value, boundary, nmax


def danger_window_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    cases = [
        (7.0, 2.0, 0.5),
        (120.0, 5.0, 3.0),
        (4096.0, 16.0, 11.0),
        (1.0e7, 125.0, 37.0),
    ]
    for u_value, v_value, k_value in cases:
        h_value = u_value / v_value
        maximum = u_value / (k_value + h_value)
        for fraction in (0.2, 0.7, 1.0, 1.3):
            threshold = fraction * maximum
            nonempty = threshold < maximum
            if nonempty:
                left = threshold * k_value / (v_value - threshold)
                right = u_value / threshold - k_value
                samples = np.geomspace(max(left * 0.5, 1.0e-12), right * 1.5, 4001)
                values = np.minimum(u_value, v_value * samples) / (k_value + samples)
                predicted = (samples > left) & (samples < right)
                observed = values > threshold
                classification = bool(np.array_equal(predicted, observed))
            else:
                left = math.nan
                right = math.nan
                samples = np.geomspace(1.0e-12, max(10.0 * h_value, 1.0), 4001)
                values = np.minimum(u_value, v_value * samples) / (k_value + samples)
                classification = bool(np.all(values <= threshold * (1.0 + 2.0e-13)))
            rows.append(
                {
                    "U": u_value,
                    "V": v_value,
                    "K": k_value,
                    "H": h_value,
                    "thresholdFraction": fraction,
                    "threshold": threshold,
                    "maximum": maximum,
                    "leftEndpoint": left,
                    "rightEndpoint": right,
                    "nonempty": nonempty,
                    "classificationPassed": classification,
                }
            )
    return rows


def bessel_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for s_value in (0.0, 0.5, 2.0, 8.0, 32.0, 128.0, 512.0):
        nmax = lattice_cutoff(s_value)
        modes = np.arange(-nmax, nmax + 1, dtype=float)
        values = math.sqrt(2.0) * jvp(modes, 2.0 * s_value, 1)
        mass = float(np.sum(values * values))
        moment = float(np.sum(modes * modes * values * values))
        expected = 1.0 + s_value * s_value
        boundary = float(values[0] ** 2 + values[-1] ** 2)
        rows.append(
            {
                "s": s_value,
                "nmax": nmax,
                "mass": mass,
                "massError": abs(mass - 1.0),
                "gradientMoment": moment,
                "expectedGradientMoment": expected,
                "gradientRelativeError": relative_error(moment, expected),
                "boundaryMass": boundary,
                "passed": abs(mass - 1.0) < 2.0e-11
                and relative_error(moment, expected) < 3.0e-10
                and boundary < 1.0e-20,
            }
        )
    return rows


def action_value(sigma: float, quadrature_order: int = 192) -> tuple[float, float, int]:
    nodes, weights = roots_legendre(quadrature_order)
    r_values = 0.5 * (nodes + 1.0)
    weights = 0.5 * weights
    total = 0.0
    max_boundary = 0.0
    max_cutoff = 0
    for r_value, weight in zip(r_values, weights, strict=True):
        y_value = float(r_value ** 1.5)
        s_value = sigma * (1.0 - math.exp(-y_value))
        q_value, boundary, cutoff = q_density(s_value)
        transformed_weight = 1.5 * (
            1.0 + 1.5 * math.log(1.0 / float(r_value))
        ) * math.exp(-2.0 * (1.0 + MU) * y_value)
        total += float(weight) * transformed_weight * q_value
        max_boundary = max(max_boundary, boundary)
        max_cutoff = max(max_cutoff, cutoff)
    return total, max_boundary, max_cutoff


def action_rows(progress: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, sigma in enumerate((16.0, 32.0, 64.0, 128.0, 256.0, 512.0), start=1):
        value, boundary, cutoff = action_value(sigma)
        scaled = value * sigma ** (2.0 / 3.0) / math.log(sigma)
        row = {
            "sigma": sigma,
            "action": value,
            "scaledAction": scaled,
            "maxBoundaryDerivativeMass": boundary,
            "maxCutoff": cutoff,
            "passed": math.isfinite(value) and value > 0.0 and boundary < 1.0e-18,
        }
        rows.append(row)
        append_ndjson(progress, {"time": utc_now(), "stage": "action", "case": index, **row})
    return rows


def frozen_cubic(sigma: float, step: float) -> float:
    endpoint = sigma * (1.0 - math.exp(-1.0))
    count = int(math.ceil(endpoint / step)) + 1
    s_values = np.linspace(0.0, endpoint, count)
    u_values = math.sqrt(2.0) * jvp(1, 2.0 * s_values, 1)
    derivative = 2.0 * math.sqrt(2.0) * jvp(1, 2.0 * s_values, 2)
    weights = np.power(1.0 - s_values / sigma, 2.0 + 2.0 * MU)
    return float(simpson(4.0 * weights * np.abs(u_values * derivative), x=s_values))


def frozen_cubic_rows(progress: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    target = 16.0 / (math.pi * math.pi)
    for index, sigma in enumerate((16.0, 32.0, 64.0, 128.0, 256.0, 512.0, 1024.0, 2048.0), start=1):
        value = frozen_cubic(sigma, 0.01)
        ratio = value / math.log(sigma)
        fine = frozen_cubic(sigma, 0.005) if sigma in (128.0, 512.0, 2048.0) else value
        row = {
            "sigma": sigma,
            "cubic": value,
            "cubicOverLogSigma": ratio,
            "asymptoticConstant": target,
            "fineCubic": fine,
            "stepRelativeDifference": relative_error(value, fine),
            "cubicOverSigma": value / sigma,
            "passed": value > 0.0 and relative_error(value, fine) < 2.0e-5,
        }
        rows.append(row)
        append_ndjson(progress, {"time": utc_now(), "stage": "frozen-cubic", "case": index, **row})
    return rows


def dissipative_fft(sigma: float, step_scale: float, grid: int = 2048) -> dict[str, float]:
    theta = 2.0 * math.pi * np.arange(grid) / grid
    modes = np.fft.fftfreq(grid, 1.0 / grid)
    steps = int(math.ceil(math.sqrt(sigma) / step_scale))
    step = 1.0 / steps
    state = 1j * math.sqrt(2.0) * np.sin(theta)
    half_heat = np.exp(-modes * modes * step / 2.0)

    def integrand(y_value: float) -> tuple[float, float]:
        coeff = np.fft.fft(state) / grid
        value = 4.0 * sigma * math.exp(-(3.0 + 2.0 * MU) * y_value) * abs(
            coeff[1] * (coeff[0] - coeff[2])
        )
        high = float(np.sum(np.abs(coeff[np.abs(modes) > 0.4 * grid]) ** 2))
        return float(value), high

    y_value = 0.0
    previous, max_high = integrand(y_value)
    integral = 0.0
    for _ in range(steps):
        state = np.fft.ifft(np.fft.fft(state) * half_heat)
        midpoint = y_value + step / 2.0
        state *= np.exp(2j * sigma * math.exp(-midpoint) * np.sin(theta) * step)
        state = np.fft.ifft(np.fft.fft(state) * half_heat)
        y_value += step
        current, high = integrand(y_value)
        integral += 0.5 * (previous + current) * step
        previous = current
        max_high = max(max_high, high)
    return {
        "cubic": integral,
        "steps": float(steps),
        "grid": float(grid),
        "maxHighModeMass": max_high,
        "finalNormSquared": float(np.mean(np.abs(state) ** 2)),
    }


def dissipative_rows(progress: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, sigma in enumerate((32.0, 128.0, 512.0, 2048.0), start=1):
        fine = dissipative_fft(sigma, 0.00125)
        coarse = dissipative_fft(sigma, 0.0025)
        row = {
            "sigma": sigma,
            "cubic": fine["cubic"],
            "coarseCubic": coarse["cubic"],
            "timeRefinementRelativeDifference": relative_error(fine["cubic"], coarse["cubic"]),
            "cubicOverLogSigma": fine["cubic"] / math.log(sigma),
            "steps": int(fine["steps"]),
            "grid": int(fine["grid"]),
            "maxHighModeMass": fine["maxHighModeMass"],
            "finalNormSquared": fine["finalNormSquared"],
            "passed": relative_error(fine["cubic"], coarse["cubic"]) < 0.012
            and fine["maxHighModeMass"] < 1.0e-18,
        }
        rows.append(row)
        append_ndjson(progress, {"time": utc_now(), "stage": "dissipative", "case": index, **row})
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    progress = output / "producer-progress.ndjson"
    resource_log = output / "producer-resource.ndjson"
    monitor = output / "producer-monitor.log"
    for path in (progress, resource_log, monitor):
        path.write_text("", encoding="utf-8")

    config = {
        "schemaVersion": SCHEMA_VERSION,
        "audit": AUDIT_NAME,
        "mu": MU,
        "seed": SEED,
        "actionQuadratureOrder": 192,
        "frozenCubicStep": 0.01,
        "dissipativeGrid": 2048,
        "dissipativeFineStepScale": 0.00125,
        "dissipativeCoarseStepScale": 0.0025,
        "gitCommit": git_commit(),
    }
    (output / "config.json").write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    (output / "seed.txt").write_text(f"{SEED}\n", encoding="utf-8")
    environment = {
        "python": sys.version,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scipy": __import__("scipy").__version__,
        "cpuCount": os.cpu_count(),
    }
    (output / "environment.txt").write_text(
        "\n".join(f"{key}={value}" for key, value in environment.items()) + "\n",
        encoding="utf-8",
    )
    append_ndjson(progress, {"time": utc_now(), "stage": "start", "config": config})
    append_ndjson(resource_log, resource_row(started, "start"))

    stages: list[tuple[str, list[dict[str, Any]]]] = []
    stages.append(("danger-window", danger_window_rows()))
    stages.append(("bessel", bessel_rows()))
    stages.append(("action", action_rows(progress)))
    stages.append(("frozen-cubic", frozen_cubic_rows(progress)))
    stages.append(("dissipative", dissipative_rows(progress)))

    for name, rows in stages:
        write_csv(output / f"producer-{name}.csv", rows)
        append_ndjson(progress, {"time": utc_now(), "stage": name, "status": "complete", "rows": len(rows)})
        append_ndjson(resource_log, resource_row(started, name))

    checks = {
        "dangerWindow": all(bool(row["classificationPassed"]) for row in stages[0][1]),
        "besselIdentities": all(bool(row["passed"]) for row in stages[1][1]),
        "actionFinite": all(bool(row["passed"]) for row in stages[2][1]),
        "actionScaledStable": max(row["scaledAction"] for row in stages[2][1][-3:])
        / min(row["scaledAction"] for row in stages[2][1][-3:])
        < 1.25,
        "frozenCubic": all(bool(row["passed"]) for row in stages[3][1]),
        "frozenCubicRatioRises": all(
            stages[3][1][index + 1]["cubicOverLogSigma"]
            >= stages[3][1][index]["cubicOverLogSigma"] - 3.0e-4
            for index in range(len(stages[3][1]) - 1)
        ),
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
        "gitCommit": git_commit(),
        "limitations": [
            "finite binary64 corroboration only",
            "zero-diffusion reference is not the dissipative PDE",
            "dissipative logarithmic growth is not proved",
            "no general three-dimensional regularity conclusion",
        ],
    }
    (output / "result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    monitor.write_text(
        f"[{utc_now()}] status={result['status']} elapsed={result['elapsedSeconds']:.3f}s "
        f"checks={sum(checks.values())}/{len(checks)}\n",
        encoding="utf-8",
    )
    append_ndjson(resource_log, resource_row(started, "complete"))
    append_ndjson(progress, {"time": utc_now(), "stage": "complete", "status": result["status"]})
    print(json.dumps(result, indent=2))
    if result["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
