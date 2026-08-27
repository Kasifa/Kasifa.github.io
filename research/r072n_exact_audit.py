#!/usr/bin/env python3
"""Producer finite audit for R0.72N.

The report contains the proofs.  This program independently evolves the
dissipative generating function with an angular FFT Strang split and checks
finite instances of the moment barrier, critical-log action, scalar danger
screen, and true cubic.  Binary64 curves corroborate the theorem ledger; they
are not an interval proof or a general Navier--Stokes computation.
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


AUDIT = "R0.72N producer dissipative-carrier audit"
SCHEMA_VERSION = 1
MU = 1.0
SIGMAS = (
    16.0,
    32.0,
    64.0,
    128.0,
    256.0,
    512.0,
    1024.0,
    2048.0,
    8192.0,
    32768.0,
)
GRID = 1024
FINE_SCALE = 1280.0
COARSE_SCALE = 640.0


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def git_commit(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
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


def append_ndjson(path: Path, value: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, sort_keys=True) + "\n")


def relative_error(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def advance_fft(
    state: np.ndarray,
    y0: float,
    y1: float,
    sigma: float,
    theta: np.ndarray,
    modes: np.ndarray,
) -> np.ndarray:
    dy = y1 - y0
    half_heat = np.exp(-modes * modes * dy / 2.0)
    state = np.fft.ifft(np.fft.fft(state) * half_heat)
    mixing_action = sigma * (math.exp(-y0) - math.exp(-y1))
    state *= np.exp(2j * mixing_action * np.sin(theta))
    return np.fft.ifft(np.fft.fft(state) * half_heat)


def diagnostics(
    state: np.ndarray,
    theta: np.ndarray,
    modes: np.ndarray,
) -> tuple[float, float, float, float, float]:
    coefficients = np.fft.fft(state) / state.size
    mass = float(np.sum(np.abs(coefficients) ** 2))
    moment = float(np.sum(modes * modes * np.abs(coefficients) ** 2))
    b_coefficients = np.fft.fft(2j * np.sin(theta) * state) / state.size
    action_density = float(
        np.sum(np.abs(b_coefficients) ** 2 / (MU + modes * modes))
    )
    cubic_product = float(
        abs(coefficients[1] * (coefficients[0] - coefficients[2]))
    )
    high_mass = float(
        np.sum(np.abs(coefficients[np.abs(modes) > 0.4 * state.size]) ** 2)
    )
    return mass, moment, action_density, cubic_product, high_mass


def solve_case(sigma: float, scale: float) -> dict[str, float]:
    grid = GRID
    theta = 2.0 * math.pi * np.arange(grid) / grid
    modes = np.fft.fftfreq(grid, 1.0 / grid)
    state = 1j * math.sqrt(2.0) * np.sin(theta)
    steps = int(math.ceil(scale * sigma ** (1.0 / 3.0)))
    dr = 1.0 / steps
    action = 0.0
    cubic = 0.0
    max_moment = 1.0
    max_high_mass = 0.0

    for index in range(steps):
        r0 = index * dr
        rm = (index + 0.5) * dr
        r1 = (index + 1.0) * dr
        y0 = r0 ** 1.5
        ym = rm ** 1.5
        y1 = r1 ** 1.5
        middle = advance_fft(state, y0, ym, sigma, theta, modes)
        mass, moment, density, product, high_mass = diagnostics(
            middle, theta, modes
        )
        action_weight = 1.5 * (
            1.0 + 1.5 * math.log(1.0 / rm)
        ) * math.exp(-2.0 * (1.0 + MU) * ym)
        cubic_weight = (
            6.0
            * sigma
            * math.sqrt(rm)
            * math.exp(-(3.0 + 2.0 * MU) * ym)
        )
        action += action_weight * density * dr
        cubic += cubic_weight * product * dr
        max_moment = max(max_moment, moment)
        max_high_mass = max(max_high_mass, high_mass)
        state = advance_fft(middle, ym, y1, sigma, theta, modes)

    final_mass, final_moment, _, _, final_high = diagnostics(state, theta, modes)
    max_moment = max(max_moment, final_moment)
    max_high_mass = max(max_high_mass, final_high)
    x_value = sigma * sigma * action
    k_proxy = 1.0 + max_moment
    u_value = sigma ** (7.0 / 3.0)
    v_value = sigma ** (1.0 / 3.0)
    t_proxy = min(u_value, v_value * x_value) / (k_proxy + x_value)
    return {
        "steps": float(steps),
        "grid": float(grid),
        "maxMoment": max_moment,
        "action": action,
        "liftedAction": x_value,
        "kProxy": k_proxy,
        "actionPoorRatio": sigma ** (1.0 / 3.0) * x_value / k_proxy,
        "tProxy": t_proxy,
        "tOverV": t_proxy / v_value,
        "cubic": cubic,
        "finalMass": final_mass,
        "maxHighModeMass": max_high_mass,
    }


def build_rows(progress: Path, resources: Path, started: float) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case, sigma in enumerate(SIGMAS, start=1):
        coarse = solve_case(sigma, COARSE_SCALE)
        fine = solve_case(sigma, FINE_SCALE)
        barrier = max(1.0, (2.0 * sigma) ** (2.0 / 3.0))
        row = {
            "sigma": sigma,
            "steps": int(fine["steps"]),
            "grid": int(fine["grid"]),
            "maxMoment": fine["maxMoment"],
            "momentBarrier": barrier,
            "momentOverBarrier": fine["maxMoment"] / barrier,
            "momentRefinementRelativeDifference": relative_error(
                fine["maxMoment"], coarse["maxMoment"]
            ),
            "action": fine["action"],
            "scaledAction": (
                fine["action"] * sigma ** (2.0 / 3.0) / math.log(sigma)
            ),
            "actionRefinementRelativeDifference": relative_error(
                fine["action"], coarse["action"]
            ),
            "liftedAction": fine["liftedAction"],
            "kProxy": fine["kProxy"],
            "actionPoorRatio": fine["actionPoorRatio"],
            "tProxy": fine["tProxy"],
            "tOverV": fine["tOverV"],
            "cubic": fine["cubic"],
            "cubicOverLogSigma": fine["cubic"] / math.log(sigma),
            "cubicOverSqrtSigma": fine["cubic"] / math.sqrt(sigma),
            "cubicRefinementRelativeDifference": relative_error(
                fine["cubic"], coarse["cubic"]
            ),
            "finalMass": fine["finalMass"],
            "maxHighModeMass": fine["maxHighModeMass"],
        }
        row["passed"] = (
            row["maxMoment"] <= barrier * (1.0 + 2.0e-3)
            and row["momentRefinementRelativeDifference"] < 0.02
            and row["actionRefinementRelativeDifference"] < 0.025
            and row["cubicRefinementRelativeDifference"] < 0.025
            and row["maxHighModeMass"] < 1.0e-18
            and math.isfinite(row["action"])
            and row["action"] > 0.0
            and math.isfinite(row["cubic"])
            and row["cubic"] > 0.0
        )
        rows.append(row)
        event = {"time": utc_now(), "stage": "case", "case": case, **row}
        append_ndjson(progress, event)
        append_ndjson(resources, resource_row(started, f"sigma-{sigma:g}"))
        print(
            f"[producer {case}/{len(SIGMAS)}] sigma={sigma:g} "
            f"D/barrier={row['momentOverBarrier']:.4f} "
            f"A*sig^(2/3)/log={row['scaledAction']:.4f} "
            f"T/V={row['tOverV']:.4f} "
            f"C/sqrt(sig)={row['cubicOverSqrtSigma']:.4f} "
            f"pass={row['passed']}",
            flush=True,
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    root = Path(__file__).resolve().parents[1]
    started = time.perf_counter()
    progress = output / "producer-progress.ndjson"
    resources = output / "producer-resource.ndjson"
    monitor = output / "producer-monitor.log"
    for path in (progress, resources, monitor):
        path.write_text("", encoding="utf-8")

    config = {
        "schemaVersion": SCHEMA_VERSION,
        "audit": AUDIT,
        "mu": MU,
        "sigmas": SIGMAS,
        "method": "angular FFT exact-mixing Strang split on uniform r=y^(2/3)",
        "grid": GRID,
        "fineScale": FINE_SCALE,
        "coarseScale": COARSE_SCALE,
        "gitCommit": git_commit(root),
    }
    (output / "config.json").write_text(
        json.dumps(config, indent=2) + "\n", encoding="utf-8"
    )
    (output / "environment.txt").write_text(
        "\n".join(
            [
                f"python={sys.version}",
                f"platform={platform.platform()}",
                f"numpy={np.__version__}",
                f"cpuCount={os.cpu_count()}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    append_ndjson(progress, {"time": utc_now(), "stage": "start", "config": config})
    append_ndjson(resources, resource_row(started, "start"))
    rows = build_rows(progress, resources, started)
    write_csv(output / "producer-dissipative.csv", rows)

    checks = {
        "allFiniteCasesPassed": all(bool(row["passed"]) for row in rows),
        "momentBarrierRespected": all(
            row["maxMoment"] <= row["momentBarrier"] * (1.0 + 2.0e-3)
            for row in rows
        ),
        "actionPositive": all(row["action"] > 0.0 for row in rows),
        "actionPoorRatioGrows": rows[-1]["actionPoorRatio"] > rows[0]["actionPoorRatio"],
        "scalarScreenApproachesV": rows[-1]["tOverV"] > 0.9,
        "cubicSublinearDiagnostic": rows[-1]["cubicOverSqrtSigma"] < rows[0]["cubicOverSqrtSigma"],
        "spatialTailSmall": max(row["maxHighModeMass"] for row in rows) < 1.0e-18,
    }
    result = {
        "schemaVersion": SCHEMA_VERSION,
        "audit": AUDIT,
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
        "counts": {"dissipative": len(rows)},
        "provedExponents": {
            "momentUpper": 2.0 / 3.0,
            "actionLowerBeforeLift": -2.0 / 3.0,
            "scalarScreen": 1.0 / 3.0,
            "trueCubicUpper": 1.0 / 2.0,
        },
        "elapsedSeconds": time.perf_counter() - started,
        "maxRssMb": max_rss_mb(),
        "gitCommit": git_commit(root),
        "limitations": [
            "finite binary64 corroboration only",
            "K, U, V, and lifted action in the scalar diagnostic suppress fixed geometry constants",
            "the enhanced-dissipation theorem, not these curves, proves the cubic upper bound",
            "the apparent logarithmic cubic trend is not proved",
            "no general three-dimensional regularity conclusion",
        ],
    }
    (output / "result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    message = (
        f"[{utc_now()}] status={result['status']} "
        f"elapsed={result['elapsedSeconds']:.3f}s "
        f"checks={sum(checks.values())}/{len(checks)}\n"
    )
    monitor.write_text(message, encoding="utf-8")
    append_ndjson(resources, resource_row(started, "complete"))
    append_ndjson(
        progress,
        {"time": utc_now(), "stage": "complete", "status": result["status"]},
    )
    print(json.dumps(result, indent=2), flush=True)
    if result["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
