#!/usr/bin/env python3
"""Independent finite audit for R0.72N.

This route works directly on a finite real Fourier chain and uses a
diagonal-heat/fourth-order exponential split.  It does not import the FFT
producer.  Agreement
is finite binary64 corroboration and never substitutes for the analytic
full-chain proof or the cited enhanced-dissipation theorem.
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


AUDIT = "R0.72N independent finite-chain audit"
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
FINE_SCALE = 1600.0
COARSE_SCALE = 800.0


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


def apply_b(state: np.ndarray) -> np.ndarray:
    value = np.zeros_like(state)
    value[1:] += state[:-1]
    value[:-1] -= state[1:]
    return value


def fourth_order_mix(state: np.ndarray, alpha: float) -> np.ndarray:
    """Fourth-order Taylor action for exp(alpha B) on the finite chain."""
    first = apply_b(state)
    second = apply_b(first)
    third = apply_b(second)
    fourth = apply_b(third)
    return (
        state
        + alpha * first
        + 0.5 * alpha**2 * second
        + (alpha**3 / 6.0) * third
        + (alpha**4 / 24.0) * fourth
    )


def advance_chain(
    state: np.ndarray,
    modes: np.ndarray,
    y0: float,
    y1: float,
    sigma: float,
) -> np.ndarray:
    dy = y1 - y0
    state = state * np.exp(-modes * modes * dy / 2.0)
    alpha = sigma * (math.exp(-y0) - math.exp(-y1))
    state = fourth_order_mix(state, alpha)
    return state * np.exp(-modes * modes * dy / 2.0)


def diagnostics(
    state: np.ndarray,
    modes: np.ndarray,
    center: int,
) -> tuple[float, float, float, float, float]:
    mass = float(np.dot(state, state))
    moment = float(np.dot(modes * state, modes * state))
    b_state = np.zeros_like(state)
    b_state[1:] += state[:-1]
    b_state[:-1] -= state[1:]
    action_density = float(
        np.sum(b_state * b_state / (MU + modes * modes))
    )
    cubic_product = float(abs(state[center + 1] * (state[center] - state[center + 2])))
    boundary_mass = float(state[0] ** 2 + state[-1] ** 2)
    return mass, moment, action_density, cubic_product, boundary_mass


def solve_case(sigma: float, scale: float) -> dict[str, float]:
    nmax = max(48, int(math.ceil(16.0 + 8.0 * math.sqrt(sigma))))
    modes = np.arange(-nmax, nmax + 1, dtype=float)
    center = nmax
    state = np.zeros(modes.size, dtype=float)
    state[center + 1] = 1.0 / math.sqrt(2.0)
    state[center - 1] = -1.0 / math.sqrt(2.0)
    steps = int(math.ceil(scale * sigma ** (1.0 / 3.0)))
    dr = 1.0 / steps
    action = 0.0
    cubic = 0.0
    max_moment = 1.0
    max_boundary_mass = 0.0

    for index in range(steps):
        r0 = index * dr
        rm = (index + 0.5) * dr
        r1 = (index + 1.0) * dr
        y0 = r0 ** 1.5
        ym = rm ** 1.5
        y1 = r1 ** 1.5
        middle = advance_chain(state, modes, y0, ym, sigma)
        mass, moment, density, product, boundary = diagnostics(
            middle, modes, center
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
        max_boundary_mass = max(max_boundary_mass, boundary)
        state = advance_chain(middle, modes, ym, y1, sigma)

    final_mass, final_moment, _, _, final_boundary = diagnostics(
        state, modes, center
    )
    max_moment = max(max_moment, final_moment)
    max_boundary_mass = max(max_boundary_mass, final_boundary)
    x_value = sigma * sigma * action
    k_proxy = 1.0 + max_moment
    u_value = sigma ** (7.0 / 3.0)
    v_value = sigma ** (1.0 / 3.0)
    t_proxy = min(u_value, v_value * x_value) / (k_proxy + x_value)
    return {
        "steps": float(steps),
        "nmax": float(nmax),
        "maxMoment": max_moment,
        "action": action,
        "liftedAction": x_value,
        "kProxy": k_proxy,
        "actionPoorRatio": sigma ** (1.0 / 3.0) * x_value / k_proxy,
        "tProxy": t_proxy,
        "tOverV": t_proxy / v_value,
        "cubic": cubic,
        "finalMass": final_mass,
        "boundaryMass": max_boundary_mass,
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
            "nmax": int(fine["nmax"]),
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
            "boundaryMass": fine["boundaryMass"],
        }
        row["passed"] = (
            row["maxMoment"] <= barrier * (1.0 + 2.0e-3)
            and row["momentRefinementRelativeDifference"] < 0.02
            and row["actionRefinementRelativeDifference"] < 0.025
            and row["cubicRefinementRelativeDifference"] < 0.025
            and row["boundaryMass"] < 1.0e-18
            and math.isfinite(row["action"])
            and row["action"] > 0.0
            and math.isfinite(row["cubic"])
            and row["cubic"] > 0.0
        )
        rows.append(row)
        append_ndjson(
            progress,
            {"time": utc_now(), "stage": "case", "case": case, **row},
        )
        append_ndjson(resources, resource_row(started, f"sigma-{sigma:g}"))
        print(
            f"[independent {case}/{len(SIGMAS)}] sigma={sigma:g} "
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
    progress = output / "independent-progress.ndjson"
    resources = output / "independent-resource.ndjson"
    monitor = output / "independent-monitor.log"
    for path in (progress, resources, monitor):
        path.write_text("", encoding="utf-8")

    config = {
        "schemaVersion": SCHEMA_VERSION,
        "audit": AUDIT,
        "mu": MU,
        "sigmas": SIGMAS,
        "method": "finite real chain with diagonal-heat/fourth-order exponential Strang split",
        "fineScale": FINE_SCALE,
        "coarseScale": COARSE_SCALE,
        "gitCommit": git_commit(root),
    }
    (output / "independent-config.json").write_text(
        json.dumps(config, indent=2) + "\n", encoding="utf-8"
    )
    (output / "independent-environment.txt").write_text(
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
    write_csv(output / "independent-dissipative.csv", rows)

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
        "boundaryTailSmall": max(row["boundaryMass"] for row in rows) < 1.0e-18,
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
            "the finite chain is not an invariant Navier--Stokes subsystem",
            "K, U, V, and lifted action in the scalar diagnostic suppress fixed geometry constants",
            "the enhanced-dissipation theorem, not these curves, proves the cubic upper bound",
            "the apparent logarithmic cubic trend is not proved",
            "no general three-dimensional regularity conclusion",
        ],
    }
    (output / "independent-result.json").write_text(
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
