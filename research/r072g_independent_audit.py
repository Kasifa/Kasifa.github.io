#!/usr/bin/env python3
"""Independent split-step audit of the R0.72G complete root mass.

This route does not import the producer.  It evolves the complex
Fourier-angle equation with exact diagonal heat half-steps and an exact
integral of the time-dependent cosine potential on each step.  Target roots
are refined from a cubic Hermite interpolant of the target trace, and the
root slope is the derivative of that interpolant.

The output is finite binary64 evidence, not interval arithmetic.  The
analytic proof and its scope are recorded in r072g_report-source.md.
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
from typing import Any

import numpy as np
import scipy
from scipy.optimize import brentq


Q0 = 4
MU = Q0**-2
DEFAULT_R = (8, 12, 16, 24, 32)


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
            "schemaVersion": "r072g-independent-monitor-v1",
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
            keep = {
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
            keep["logicalCpus"] = os.cpu_count()
            self.resources.write(json.dumps(keep, sort_keys=True) + "\n")
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


def next_power_of_two(value: int) -> int:
    return 1 << (value - 1).bit_length()


def hermite(
    s: float, left: float, right: float, dl: float, dr: float, step: float
) -> float:
    return (
        (2 * s**3 - 3 * s**2 + 1) * left
        + (s**3 - 2 * s**2 + s) * step * dl
        + (-2 * s**3 + 3 * s**2) * right
        + (s**3 - s**2) * step * dr
    )


def hermite_derivative(
    s: float, left: float, right: float, dl: float, dr: float, step: float
) -> float:
    return (
        (6 * s**2 - 6 * s) * left
        + (3 * s**2 - 4 * s + 1) * step * dl
        + (-6 * s**2 + 6 * s) * right
        + (3 * s**2 - 2 * s) * step * dr
    ) / step


def scan(
    r_value: int,
    step_size: float,
    horizon_factor: float,
    radius_factor: float,
    edge_width: int,
    monitor: Monitor,
    label: str,
    keep_roots: bool,
) -> tuple[dict[str, Any], list[dict[str, float]]]:
    delta = float(r_value**4)
    ed_scale = math.sqrt(delta)
    final_tau = horizon_factor * ed_scale
    requested_radius = int(math.ceil(radius_factor * r_value)) + edge_width
    grid_size = next_power_of_two(2 * requested_radius + 2)
    modes = np.rint(np.fft.fftfreq(grid_size, d=1 / grid_size)).astype(int)
    theta = 2 * math.pi * np.arange(grid_size) / grid_size
    cosine = np.cos(theta)
    coefficients = np.zeros(grid_size, dtype=np.complex128)
    minus_one = int(np.flatnonzero(modes == -1)[0])
    plus_one = int(np.flatnonzero(modes == 1)[0])
    zero = int(np.flatnonzero(modes == 0)[0])
    coefficients[minus_one] = 1j
    tau = 0.0
    target_left = 0.0
    h_left = 1.0
    roots: list[dict[str, float]] = []
    maximum_imaginary_target = 0.0
    maximum_norm = 1.0
    maximum_edge_fraction = 0.0
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
        gridSize=grid_size,
        maximumMode=int(np.max(np.abs(modes))),
    )

    while tau < final_tau - 1e-15:
        step = min(step_size, final_tau - tau)
        heat = np.exp(-((modes.astype(float) ** 2 + MU) / delta) * step / 2)
        coefficients *= heat
        alpha = 2 * delta * (
            math.exp(-tau / delta) - math.exp(-(tau + step) / delta)
        )
        values = np.fft.ifft(coefficients) * grid_size
        values *= np.exp(-1j * alpha * cosine)
        coefficients = np.fft.fft(values) / grid_size
        coefficients *= heat
        next_tau = tau + step
        target_complex = coefficients[zero]
        target_right = float(target_complex.real)
        maximum_imaginary_target = max(
            maximum_imaginary_target, abs(float(target_complex.imag))
        )
        h_complex = -1j * math.exp(-next_tau / delta) * (
            coefficients[minus_one] + coefficients[plus_one]
        )
        h_right = float(h_complex.real)
        maximum_imaginary_target = max(
            maximum_imaginary_target, abs(float(h_complex.imag))
        )
        derivative_left = h_left - (MU / delta) * target_left
        derivative_right = h_right - (MU / delta) * target_right

        if tau > 0.0 and target_left * target_right < 0.0:
            root_fn = lambda s: hermite(
                s,
                target_left,
                target_right,
                derivative_left,
                derivative_right,
                step,
            )
            fraction = float(
                brentq(root_fn, 0.0, 1.0, xtol=2e-14, rtol=2e-14)
            )
            root_tau = tau + fraction * step
            slope = hermite_derivative(
                fraction,
                target_left,
                target_right,
                derivative_left,
                derivative_right,
                step,
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

        coefficients_norm = float(np.vdot(coefficients, coefficients).real)
        maximum_norm = max(maximum_norm, math.sqrt(max(coefficients_norm, 0.0)))
        boundary = np.abs(modes) >= grid_size // 2 - edge_width
        edge_square = float(np.vdot(coefficients[boundary], coefficients[boundary]).real)
        maximum_edge_fraction = max(
            maximum_edge_fraction, edge_square / max(coefficients_norm, 1e-300)
        )
        tau = next_tau
        target_left = target_right
        h_left = h_right
        steps += 1
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
    result = {
        "label": label,
        "R": r_value,
        "delta": delta,
        "enhancedDissipationScale": ed_scale,
        "horizonFactor": horizon_factor,
        "finalTau": final_tau,
        "step": step_size,
        "radiusFactor": radius_factor,
        "requestedRadius": requested_radius,
        "gridSize": grid_size,
        "maximumMode": int(np.max(np.abs(modes))),
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
        "maximumImaginaryTargetOrSlope": maximum_imaginary_target,
        "maximumEdgeEnergyFraction": maximum_edge_fraction,
        "maximumStateNorm": maximum_norm,
        "finalStateNorm": float(np.linalg.norm(coefficients)),
        "elapsedSeconds": time.perf_counter() - started,
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
        step = 0.08 if args.smoke else 0.04
        horizon = 6.0 if args.smoke else 12.0
        rows: list[dict[str, Any]] = []
        root_rows: list[dict[str, Any]] = []
        for r_value in r_values:
            row, roots = scan(
                r_value,
                step,
                horizon,
                12.0,
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
            base_r = 24
            base = next(row for row in rows if row["R"] == base_r)
            fine, _ = scan(
                base_r, 0.02, 12.0, 12.0, 12, monitor, "pressure-step", False
            )
            wide, _ = scan(
                base_r, 0.04, 12.0, 18.0, 12, monitor, "pressure-radius", False
            )
            long, _ = scan(
                base_r, 0.04, 20.0, 12.0, 12, monitor, "pressure-horizon", False
            )
            pressure = {
                "baseR": base_r,
                "stepRelativeDifference": relative_difference(
                    base["completeSlopeMass"], fine["completeSlopeMass"]
                ),
                "stepRootCountDifference": base["rootCount"] - fine["rootCount"],
                "radiusRelativeDifference": relative_difference(
                    base["completeSlopeMass"], wide["completeSlopeMass"]
                ),
                "radiusRootCountDifference": base["rootCount"] - wide["rootCount"],
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
                "name": "real_phase_invariant",
                "passed": all(
                    row["maximumImaginaryTargetOrSlope"] < 2e-11 for row in rows
                ),
                "value": max(row["maximumImaginaryTargetOrSlope"] for row in rows),
            },
            {
                "name": "contractive_evolution",
                "passed": all(row["maximumStateNorm"] <= 1.00001 for row in rows),
                "value": max(row["maximumStateNorm"] for row in rows),
            },
            {
                "name": "root_interpolation_residual",
                "passed": all(
                    row["maximumInterpolatedTargetResidual"] < 2e-12 for row in rows
                ),
                "value": max(row["maximumInterpolatedTargetResidual"] for row in rows),
            },
            {
                "name": "spectral_edge_pressure",
                "passed": all(row["maximumEdgeEnergyFraction"] < 1e-8 for row in rows),
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
                        "passed": pressure["stepRelativeDifference"] < 2e-3
                        and pressure["stepRootCountDifference"] == 0,
                        "value": pressure["stepRelativeDifference"],
                    },
                    {
                        "name": "radius_pressure",
                        "passed": pressure["radiusRelativeDifference"] < 2e-4,
                        "value": pressure["radiusRelativeDifference"],
                    },
                    {
                        "name": "horizon_mass_tail",
                        "passed": pressure["horizonRelativeMassIncrease"] < 2e-4,
                        "value": pressure["horizonRelativeMassIncrease"],
                    },
                    {
                        "name": "diagnostic_log_slope",
                        "passed": fit["relativeSlopeDifferenceFromDiagnosticTarget"] < 0.15,
                        "value": fit,
                    },
                ]
            )

        result = {
            "schemaVersion": "r072g-independent-certificate-v1",
            "auditId": "R0.72G-complete-root-independent",
            "createdAtUtc": utc_now(),
            "allRequiredChecksPassed": all(check["passed"] for check in checks),
            "method": {
                "evolution": "time-dependent Fourier Strang split step",
                "heatStep": "exact diagonal half steps",
                "potentialStep": "exact integral of exp(-tau/delta) on each step",
                "rootDetection": "sign change plus target-only cubic Hermite refinement",
                "deltas": [row["delta"] for row in rows],
                "mainStep": step,
                "mainHorizonFactorTimesSqrtDelta": horizon,
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
                "finiteSpectralGrid": True,
                "finiteTimeWindow": True,
                "signChangingRootsResolved": True,
                "tangentRootsNumericallyCertified": False,
                "completeRootUpperBoundInExactOneCarrier": True,
                "generalTriangularCompleteRootBound": False,
                "arbitraryNSECompleteRootBound": False,
                "continuationCriterion": False,
                "provesNSERegularity": False,
                "provesNSESingularity": False,
                "claim": "independent finite corroboration only; analytic theorem is in r072g_report-source.md",
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
