#!/usr/bin/env python3
"""Producer finite audit for the R0.72G complete one-carrier root mass.

The audit evolves the real invariant lattice in scaled time with fixed-step
RK4, detects every resolved sign-changing target root, refines it with a
cubic Hermite interpolant, and accumulates the corresponding squared slope.
It also records dyadic mass packets and step/radius/horizon pressure checks.

This is deterministic binary64 corroboration.  The analytic all-root theorem
is in r072g_report-source.md; this program is not interval arithmetic and
does not certify an infinite lattice or unresolved roots.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time
from typing import Any, Iterable

import numpy as np
import scipy
from scipy.optimize import brentq


Q0 = 4
MU = Q0**-2
DEFAULT_R = (8, 12, 16, 24, 32, 48, 64)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace(
        "+00:00", "Z"
    )


def rss_bytes() -> int:
    raw = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return raw if sys.platform == "darwin" else 1024 * raw


def git_revision() -> str | None:
    try:
        run = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return run.stdout.strip() or None


class Monitor:
    def __init__(self, progress: Path | None, resources: Path | None) -> None:
        self.started = time.perf_counter()
        self.cpu_started = time.process_time()
        self.index = 0
        self.progress = self._open(progress)
        self.resources = self._open(resources)

    @staticmethod
    def _open(path: Path | None):
        if path is None:
            return None
        path.parent.mkdir(parents=True, exist_ok=True)
        return path.open("w", encoding="utf-8")

    def event(self, stage: str, status: str, message: str, **fields: Any) -> None:
        self.index += 1
        elapsed = time.perf_counter() - self.started
        cpu = time.process_time() - self.cpu_started
        row = {
            "schemaVersion": "r072g-producer-monitor-v1",
            "timestampUtc": utc_now(),
            "eventIndex": self.index,
            "stage": stage,
            "status": status,
            "message": message,
            "elapsedSeconds": elapsed,
            "processCpuSeconds": cpu,
            "peakRssBytes": rss_bytes(),
            **fields,
        }
        if self.progress is not None:
            self.progress.write(json.dumps(row, sort_keys=True) + "\n")
            self.progress.flush()
        if self.resources is not None:
            resource_row = {
                key: row[key]
                for key in (
                    "schemaVersion",
                    "timestampUtc",
                    "eventIndex",
                    "stage",
                    "status",
                    "elapsedSeconds",
                    "processCpuSeconds",
                    "peakRssBytes",
                )
            }
            resource_row["logicalCpus"] = os.cpu_count()
            self.resources.write(json.dumps(resource_row, sort_keys=True) + "\n")
            self.resources.flush()
        print(
            f"[{row['timestampUtc']}] {stage}/{status} {message} "
            f"elapsed={elapsed:.2f}s rss={row['peakRssBytes']/2**20:.1f}MiB",
            file=sys.stderr,
            flush=True,
        )

    def close(self) -> None:
        for handle in (self.progress, self.resources):
            if handle is not None:
                handle.close()


def rhs(
    tau: float, state: np.ndarray, damping: np.ndarray, delta: float
) -> np.ndarray:
    result = -damping * state
    amplitude = math.exp(-tau / delta)
    result[1:] += amplitude * state[:-1]
    result[:-1] -= amplitude * state[1:]
    return result


def rk4(
    tau: float,
    state: np.ndarray,
    step: float,
    damping: np.ndarray,
    delta: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    k1 = rhs(tau, state, damping, delta)
    k2 = rhs(tau + step / 2, state + step * k1 / 2, damping, delta)
    k3 = rhs(tau + step / 2, state + step * k2 / 2, damping, delta)
    k4 = rhs(tau + step, state + step * k3, damping, delta)
    right = state + step * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return right, k1, rhs(tau + step, right, damping, delta)


def hermite(
    s: float, left: float, right: float, dl: float, dr: float, step: float
) -> float:
    return (
        (2 * s**3 - 3 * s**2 + 1) * left
        + (s**3 - 2 * s**2 + s) * step * dl
        + (-2 * s**3 + 3 * s**2) * right
        + (s**3 - s**2) * step * dr
    )


def hermite_component(
    s: float,
    left: np.ndarray,
    right: np.ndarray,
    dl: np.ndarray,
    dr: np.ndarray,
    step: float,
    index: int,
) -> float:
    return hermite(
        s,
        float(left[index]),
        float(right[index]),
        float(dl[index]),
        float(dr[index]),
        step,
    )


def dyadic_packets(roots: Iterable[dict[str, float]], final_tau: float) -> list[dict[str, float | int]]:
    roots = list(roots)
    packets: list[dict[str, float | int]] = []
    left = 0.0
    right = 1.0
    while left < final_tau:
        members = [row for row in roots if left <= row["tau"] < right]
        packets.append(
            {
                "tauLeft": left,
                "tauRight": min(right, final_tau),
                "rootCount": len(members),
                "slopeMass": float(sum(row["slopeSquare"] for row in members)),
            }
        )
        left = right
        right *= 2.0
    return packets


def scan(
    r_value: int,
    step_size: float,
    horizon_factor: float,
    radius_factor: float,
    edge_width: int,
    monitor: Monitor,
    label: str,
    keep_roots: bool = False,
) -> tuple[dict[str, Any], list[dict[str, float]]]:
    delta = float(r_value**4)
    ed_scale = math.sqrt(delta)
    final_tau = horizon_factor * ed_scale
    radius = int(math.ceil(radius_factor * r_value)) + edge_width
    indices = np.arange(-radius, radius + 1, dtype=np.float64)
    damping = (indices**2 + MU) / delta
    target = radius
    state = np.zeros(indices.size, dtype=np.float64)
    state[target - 1] = 1.0
    tau = 0.0
    target_left = 0.0
    roots: list[dict[str, float]] = []
    maximum_edge_fraction = 0.0
    maximum_norm = 1.0
    maximum_residual = 0.0
    steps = 0
    next_fraction = 0.25
    started = time.perf_counter()
    monitor.event(
        label,
        "started",
        f"R={r_value} delta={delta:g}",
        R=r_value,
        delta=delta,
        finalTau=final_tau,
        step=step_size,
        radius=radius,
        dimension=int(indices.size),
    )
    while tau < final_tau - 1e-15:
        step = min(step_size, final_tau - tau)
        right_state, dl, dr = rk4(tau, state, step, damping, delta)
        target_right = float(right_state[target])
        if tau > 0.0 and target_left * target_right < 0.0:
            root_fn = lambda s: hermite(
                s,
                target_left,
                target_right,
                float(dl[target]),
                float(dr[target]),
                step,
            )
            fraction = float(
                brentq(root_fn, 0.0, 1.0, xtol=2e-14, rtol=2e-14)
            )
            root_tau = tau + fraction * step
            left_neighbor = hermite_component(
                fraction, state, right_state, dl, dr, step, target - 1
            )
            right_neighbor = hermite_component(
                fraction, state, right_state, dl, dr, step, target + 1
            )
            slope = math.exp(-root_tau / delta) * (
                left_neighbor - right_neighbor
            )
            residual = abs(root_fn(fraction))
            maximum_residual = max(maximum_residual, residual)
            roots.append(
                {
                    "tau": root_tau,
                    "tauOverSqrtDelta": root_tau / ed_scale,
                    "slope": slope,
                    "slopeSquare": slope * slope,
                    "interpolatedTargetResidual": residual,
                }
            )
        state = right_state
        tau += step
        target_left = target_right
        steps += 1
        if steps % 100 == 0 or tau >= final_tau - 1e-15:
            norm_square = float(np.dot(state, state))
            maximum_norm = max(maximum_norm, math.sqrt(max(norm_square, 0.0)))
            edge_square = float(np.dot(state[:edge_width], state[:edge_width]))
            edge_square += float(np.dot(state[-edge_width:], state[-edge_width:]))
            maximum_edge_fraction = max(
                maximum_edge_fraction, edge_square / max(norm_square, 1e-300)
            )
        if tau / final_tau + 1e-12 >= next_fraction:
            monitor.event(
                label,
                "progress",
                f"R={r_value} reached {int(100*next_fraction)}%",
                R=r_value,
                fraction=min(tau / final_tau, 1.0),
                rootsFound=len(roots),
                steps=steps,
            )
            next_fraction += 0.25

    complete_mass = float(sum(row["slopeSquare"] for row in roots))
    selected_mass = float(
        sum(row["slopeSquare"] for row in roots[: min(r_value, len(roots))])
    )
    result: dict[str, Any] = {
        "label": label,
        "R": r_value,
        "delta": delta,
        "enhancedDissipationScale": ed_scale,
        "horizonFactor": horizon_factor,
        "finalTau": final_tau,
        "step": step_size,
        "radiusFactor": radius_factor,
        "radius": radius,
        "dimension": int(indices.size),
        "steps": steps,
        "rootCount": len(roots),
        "selectedRootCount": min(r_value, len(roots)),
        "selectedSlopeMass": selected_mass,
        "completeSlopeMass": complete_mass,
        "selectedToCompleteMassRatio": selected_mass / complete_mass,
        "completeMassOverLogDelta": complete_mass / math.log(delta),
        "selectedMassOverLogDelta": selected_mass / math.log(delta),
        "rootCountOverSqrtDelta": len(roots) / ed_scale,
        "maximumInterpolatedTargetResidual": maximum_residual,
        "maximumEdgeEnergyFraction": maximum_edge_fraction,
        "maximumStateNorm": maximum_norm,
        "finalStateNorm": float(np.linalg.norm(state)),
        "elapsedSeconds": time.perf_counter() - started,
        "dyadicPackets": dyadic_packets(roots, final_tau),
    }
    monitor.event(
        label,
        "completed",
        f"R={r_value} roots={len(roots)} mass={complete_mass:.8f}",
        R=r_value,
        rootCount=len(roots),
        completeSlopeMass=complete_mass,
        elapsedSecondsForScan=result["elapsedSeconds"],
    )
    return result, roots if keep_roots else []


def relative_difference(a: float, b: float) -> float:
    return abs(a - b) / max(abs(a), abs(b), 1e-300)


def fit_log(rows: list[dict[str, Any]]) -> dict[str, float]:
    x = np.asarray([math.log(row["delta"]) for row in rows], dtype=float)
    y = np.asarray([row["completeSlopeMass"] for row in rows], dtype=float)
    slope, intercept = np.polyfit(x, y, 1)
    residual = y - (slope * x + intercept)
    return {
        "slopeAgainstLogDelta": float(slope),
        "intercept": float(intercept),
        "rmse": float(math.sqrt(np.mean(residual**2))),
        "targetFourOverPiSquared": 4 / math.pi**2,
        "relativeSlopeDifferenceFromDiagnosticTarget": relative_difference(
            float(slope), 4 / math.pi**2
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--roots-output", type=Path)
    parser.add_argument("--progress-log", type=Path)
    parser.add_argument("--resource-log", type=Path)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    monitor = Monitor(args.progress_log, args.resource_log)
    try:
        r_values = (8, 12) if args.smoke else DEFAULT_R
        step = 0.04 if args.smoke else 0.02
        horizon = 6.0 if args.smoke else 12.0
        rows: list[dict[str, Any]] = []
        root_rows: list[dict[str, Any]] = []
        for r_value in r_values:
            row, roots = scan(
                r_value,
                step,
                horizon,
                10.0,
                12,
                monitor,
                f"main-R{r_value}",
                keep_roots=args.roots_output is not None,
            )
            rows.append(row)
            for index, root in enumerate(roots, start=1):
                root_rows.append({"R": r_value, "rootIndex": index, **root})

        pressure: dict[str, Any] = {}
        if not args.smoke:
            base_r = 32
            base = next(row for row in rows if row["R"] == base_r)
            fine, _ = scan(
                base_r, 0.01, 12.0, 12.0, 12, monitor, "pressure-step", False
            )
            largest = rows[-1]
            wide, _ = scan(
                int(largest["R"]),
                0.02,
                12.0,
                14.0,
                12,
                monitor,
                "pressure-radius-largest",
                False,
            )
            long, _ = scan(
                base_r, 0.02, 20.0, 12.0, 12, monitor, "pressure-horizon", False
            )
            pressure = {
                "baseR": base_r,
                "largestRadiusPressureR": largest["R"],
                "stepRelativeDifference": relative_difference(
                    base["completeSlopeMass"], fine["completeSlopeMass"]
                ),
                "stepRootCountDifference": base["rootCount"] - fine["rootCount"],
                "radiusRelativeDifference": relative_difference(
                    largest["completeSlopeMass"], wide["completeSlopeMass"]
                ),
                "radiusRootCountDifference": largest["rootCount"] - wide["rootCount"],
                "horizonRelativeMassIncrease": (
                    long["completeSlopeMass"] - base["completeSlopeMass"]
                )
                / base["completeSlopeMass"],
                "horizonRootCountIncrease": long["rootCount"] - base["rootCount"],
                "fine": fine,
                "wide": wide,
                "long": long,
            }

        fit_rows = rows[-4:] if len(rows) >= 4 else rows
        fit = fit_log(fit_rows)
        checks = [
            {
                "name": "contractive_evolution",
                "passed": all(row["maximumStateNorm"] <= 1.000001 for row in rows),
                "value": max(row["maximumStateNorm"] for row in rows),
            },
            {
                "name": "root_interpolation_residual",
                "passed": all(
                    row["maximumInterpolatedTargetResidual"] < 1e-12 for row in rows
                ),
                "value": max(row["maximumInterpolatedTargetResidual"] for row in rows),
            },
            {
                "name": "lattice_edge_diagnostic",
                "passed": all(row["maximumEdgeEnergyFraction"] < 5e-3 for row in rows),
                "value": max(row["maximumEdgeEnergyFraction"] for row in rows),
            },
            {
                "name": "complete_contains_selected",
                "passed": all(
                    row["completeSlopeMass"] >= row["selectedSlopeMass"] > 0
                    for row in rows
                ),
                "value": min(row["selectedToCompleteMassRatio"] for row in rows),
            },
        ]
        if pressure:
            checks.extend(
                [
                    {
                        "name": "step_pressure",
                        "passed": pressure["stepRelativeDifference"] < 1e-4
                        and pressure["stepRootCountDifference"] == 0,
                        "value": pressure["stepRelativeDifference"],
                    },
                    {
                        "name": "radius_pressure",
                        "passed": pressure["radiusRelativeDifference"] < 1e-5,
                        "value": pressure["radiusRelativeDifference"],
                    },
                    {
                        "name": "horizon_mass_tail",
                        "passed": pressure["horizonRelativeMassIncrease"] < 1e-5,
                        "value": pressure["horizonRelativeMassIncrease"],
                    },
                    {
                        "name": "diagnostic_log_slope",
                        "passed": fit["relativeSlopeDifferenceFromDiagnosticTarget"] < 0.08,
                        "value": fit,
                    },
                ]
            )

        result = {
            "schemaVersion": "r072g-producer-certificate-v1",
            "auditId": "R0.72G-complete-root-producer",
            "createdAtUtc": utc_now(),
            "allRequiredChecksPassed": all(check["passed"] for check in checks),
            "method": {
                "evolution": "fixed-step RK4 on the real invariant lattice in scaled tau",
                "rootDetection": "sign change plus cubic Hermite and Brent refinement",
                "deltas": [row["delta"] for row in rows],
                "mainStep": step,
                "mainHorizonFactorTimesSqrtDelta": horizon,
                "mainRadiusFactorTimesDeltaOneFourth": 10,
                "binaryPrecision": "IEEE-754 binary64",
                "randomness": False,
            },
            "rows": rows,
            "pressure": pressure,
            "logFit": fit,
            "checks": checks,
            "environment": {
                "python": sys.version,
                "numpy": np.__version__,
                "scipy": scipy.__version__,
                "platform": platform.platform(),
                "logicalCpus": os.cpu_count(),
                "gitRevisionAtRun": git_revision(),
            },
            "scope": {
                "intervalArithmetic": False,
                "finiteLattice": True,
                "finiteTimeWindow": True,
                "signChangingRootsResolved": True,
                "tangentRootsNumericallyCertified": False,
                "completeRootUpperBoundInExactOneCarrier": True,
                "generalTriangularCompleteRootBound": False,
                "arbitraryNSECompleteRootBound": False,
                "continuationCriterion": False,
                "provesNSERegularity": False,
                "provesNSESingularity": False,
                "claim": "finite corroboration only; analytic theorem is in r072g_report-source.md",
            },
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        if args.roots_output is not None:
            args.roots_output.parent.mkdir(parents=True, exist_ok=True)
            with args.roots_output.open("w", newline="", encoding="utf-8") as handle:
                fieldnames = [
                    "R",
                    "rootIndex",
                    "tau",
                    "tauOverSqrtDelta",
                    "slope",
                    "slopeSquare",
                    "interpolatedTargetResidual",
                ]
                writer = csv.DictWriter(handle, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(root_rows)
        monitor.event(
            "audit",
            "completed",
            f"allRequiredChecksPassed={result['allRequiredChecksPassed']}",
            output=str(args.output),
        )
        if not result["allRequiredChecksPassed"]:
            raise SystemExit(1)
    finally:
        monitor.close()


if __name__ == "__main__":
    main()
