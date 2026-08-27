#!/usr/bin/env python3
"""Independent numerical/algebraic producer audit for R0.72E.

The program starts from the raw one-carrier parameters with the fixed value
``q0 = 4``.  It does not read a certificate, a report, or any other research
output.  It recomputes

* the exact launch data/enstrophy ledger and all amplitude powers;
* frozen Bessel roots and prefix slope masses for R = 8, 16, 32, 64;
* the negative-Sobolev action for delta = 16, ..., 512 with an independent
  Strang split-step Fourier method; and
* the H1 barrier and the one-third exponent ledger.

Progress is always printed to stderr.  Optional progress/resource logs are
newline-delimited JSON so a run remains monitorable without shell redirects.
The numerical computation is corroborative; it is not an interval proof.
"""

from __future__ import annotations

import argparse
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
from typing import Any, Callable, Sequence

PROCESS_STARTED_WALL = time.perf_counter()
PROCESS_STARTED_CPU = time.process_time()
PROCESS_STARTED_USAGE = resource.getrusage(resource.RUSAGE_SELF)

try:
    import numpy as np
except ImportError as exc:  # pragma: no cover - exercised only in a bad env
    raise SystemExit(
        "r072e_exact_audit.py requires NumPy; install requirements-research.txt"
    ) from exc

try:
    import scipy
    from scipy.special import jn_zeros, jv
except ImportError as exc:  # pragma: no cover - exercised only in a bad env
    raise SystemExit(
        "r072e_exact_audit.py requires SciPy; install requirements-research.txt"
    ) from exc


AUDIT_ID = "R0.72E-exact-producer-audit"
SCHEMA_VERSION = 1
Q0 = 4
DEFAULT_DELTAS = (16, 32, 64, 128, 256, 512)
DEFAULT_BESSEL_COUNTS = (8, 16, 32, 64)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace(
        "+00:00", "Z"
    )


def json_number(value: float) -> float:
    """Convert NumPy scalars and reject silent NaN/Inf JSON output."""

    result = float(value)
    if not math.isfinite(result):
        raise FloatingPointError(f"non-finite result: {result!r}")
    return result


def parse_positive_ints(text: str, label: str) -> tuple[int, ...]:
    try:
        values = tuple(int(part.strip()) for part in text.split(",") if part.strip())
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"{label} must be comma-separated integers") from exc
    if not values or any(value <= 0 for value in values):
        raise argparse.ArgumentTypeError(f"{label} must contain positive integers")
    if tuple(sorted(set(values))) != values:
        raise argparse.ArgumentTypeError(f"{label} must be strictly increasing")
    return values


def git_revision() -> str | None:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=5,
        )
    except (FileNotFoundError, subprocess.SubprocessError):
        return None
    return completed.stdout.strip() or None


def peak_rss_bytes() -> int:
    # macOS reports bytes; Linux and most BSD builds report KiB.
    raw = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return raw if sys.platform == "darwin" else raw * 1024


class RunMonitor:
    """Mirror concise progress to stderr and optional NDJSON files."""

    def __init__(self, progress_path: Path | None, resource_path: Path | None) -> None:
        # Include NumPy/SciPy import and argument parsing in the reported run cost.
        self.started_wall = PROCESS_STARTED_WALL
        self.started_cpu = PROCESS_STARTED_CPU
        self.started_user_cpu = float(PROCESS_STARTED_USAGE.ru_utime)
        self.started_system_cpu = float(PROCESS_STARTED_USAGE.ru_stime)
        self.progress_path = progress_path
        self.resource_path = resource_path
        if progress_path is not None and resource_path is not None:
            if progress_path.resolve() == resource_path.resolve():
                raise ValueError("--progress-log and --resource-log must be different paths")
        for path in (progress_path, resource_path):
            if path is not None:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("", encoding="utf-8")

    @property
    def elapsed(self) -> float:
        return time.perf_counter() - self.started_wall

    def _append(self, path: Path | None, row: dict[str, Any]) -> None:
        if path is None:
            return
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, sort_keys=True, separators=(",", ":")))
            handle.write("\n")

    def emit(self, stage: str, message: str, **fields: Any) -> None:
        timestamp = utc_now()
        elapsed = self.elapsed
        progress_row = {
            "timestampUtc": timestamp,
            "stage": stage,
            "message": message,
            "elapsedSeconds": round(elapsed, 6),
            **fields,
        }
        self._append(self.progress_path, progress_row)
        print(
            f"[{timestamp}] [{stage}] +{elapsed:.2f}s {message}",
            file=sys.stderr,
            flush=True,
        )

        usage = resource.getrusage(resource.RUSAGE_SELF)
        resource_row = {
            "timestampUtc": timestamp,
            "stage": stage,
            "elapsedSeconds": round(elapsed, 6),
            "processCpuSeconds": round(time.process_time() - self.started_cpu, 6),
            "userCpuSeconds": round(float(usage.ru_utime) - self.started_user_cpu, 6),
            "systemCpuSeconds": round(
                float(usage.ru_stime) - self.started_system_cpu, 6
            ),
            "peakRssBytes": peak_rss_bytes(),
            "logicalCpus": os.cpu_count(),
            **fields,
        }
        self._append(self.resource_path, resource_row)


def log_fit(xs: Sequence[float], ys: Sequence[float]) -> dict[str, float]:
    if len(xs) < 2 or len(xs) != len(ys):
        raise ValueError("a log-log fit needs at least two paired values")
    log_x = np.log(np.asarray(xs, dtype=np.float64))
    log_y = np.log(np.asarray(ys, dtype=np.float64))
    slope, intercept = np.polyfit(log_x, log_y, deg=1)
    prediction = slope * log_x + intercept
    residual = log_y - prediction
    ss_res = float(np.dot(residual, residual))
    centered = log_y - float(np.mean(log_y))
    ss_tot = float(np.dot(centered, centered))
    r_squared = 1.0 if ss_tot == 0.0 else 1.0 - ss_res / ss_tot
    return {
        "slope": json_number(slope),
        "intercept": json_number(intercept),
        "rSquared": json_number(r_squared),
    }


def bounded_sequence(values: Sequence[float], allowed_spread: float) -> dict[str, Any]:
    minimum = min(values)
    maximum = max(values)
    spread = maximum / minimum
    return {
        "minimum": json_number(minimum),
        "maximum": json_number(maximum),
        "maxToMin": json_number(spread),
        "allowedMaxToMin": allowed_spread,
        "passed": bool(minimum > 0.0 and spread <= allowed_spread),
    }


def raw_parameter_ledger(
    counts: Sequence[int], bessel_masses: dict[int, float]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Recompute all physical quantities from the raw amplitude definitions."""

    q0 = float(Q0)
    rows: list[dict[str, Any]] = []
    for r_value in counts:
        delta = float(r_value**4)
        p = q0**2 * delta
        s2 = delta / math.log(2.0 + delta)

        shear_velocity = 2.0 * p**2
        active_velocity = 2.0 * s2
        shear_enstrophy = 2.0 * q0**2 * p**2
        active_enstrophy = 2.0 * s2 * (q0**2 + 1.0)
        velocity_l2 = shear_velocity + active_velocity
        vorticity_l2 = shear_enstrophy + active_enstrophy
        data_size = velocity_l2 + vorticity_l2
        data_closed_form = 2.0 * p**2 * (1.0 + q0**2) + 2.0 * s2 * (
            q0**2 + 2.0
        )
        data_absolute_residual = abs(data_size - data_closed_form)
        data_relative_residual = data_absolute_residual / max(
            abs(data_size), abs(data_closed_form), 1.0
        )

        h1_barrier = max(1.0, (2.0 * delta) ** (2.0 / 3.0))
        active_enstrophy_barrier = 2.0 * s2 * (1.0 + q0**2 * h1_barrier)
        barrier_core = s2 * h1_barrier
        source_at_barrier = 4.0 * delta * math.sqrt(h1_barrier)
        damping_at_barrier = 2.0 * h1_barrier**2

        mass = bessel_masses[r_value]
        root_ledger_proxy = s2 * mass
        pure_power_ratio = delta / data_size ** (1.0 / 3.0)
        bessel_weighted_ratio = root_ledger_proxy / data_size ** (1.0 / 3.0)

        rows.append(
            {
                "R": r_value,
                "delta": delta,
                "P": p,
                "S2": s2,
                "launch": {
                    "velocityL2Squared": velocity_l2,
                    "vorticityL2Squared": vorticity_l2,
                    "shearVelocityL2Squared": shear_velocity,
                    "activeVelocityL2Squared": active_velocity,
                    "shearEnstrophy": shear_enstrophy,
                    "activeEnstrophy": active_enstrophy,
                    "dataSizeD": data_size,
                    "closedFormD": data_closed_form,
                    "closedFormAbsoluteResidual": data_absolute_residual,
                    "closedFormRelativeResidual": data_relative_residual,
                    "DOverDeltaSquared": data_size / delta**2,
                },
                "h1Barrier": {
                    "phiThetaSquaredUpper": h1_barrier,
                    "activeEnstrophyUpper": active_enstrophy_barrier,
                    "S2TimesBarrier": barrier_core,
                    "S2TimesBarrierOverDeltaSquared": barrier_core / delta**2,
                    "activeBarrierOverLaunchShearEnstrophy": (
                        active_enstrophy_barrier / shear_enstrophy
                    ),
                    "sourceAtBarrier": source_at_barrier,
                    "quadraticDampingAtBarrier": damping_at_barrier,
                    "barrierBalanceRelativeResidual": abs(
                        source_at_barrier - damping_at_barrier
                    )
                    / damping_at_barrier,
                },
                "rootLedgerScaling": {
                    "frozenBesselMass": mass,
                    "S2TimesMassProxy": root_ledger_proxy,
                    "purePowerRatioDeltaOverDOneThird": pure_power_ratio,
                    "besselWeightedRatioProxy": bessel_weighted_ratio,
                },
            }
        )

    deltas = [row["delta"] for row in rows]
    data_values = [row["launch"]["dataSizeD"] for row in rows]
    barrier_values = [row["h1Barrier"]["S2TimesBarrier"] for row in rows]
    pure_ratios = [
        row["rootLedgerScaling"]["purePowerRatioDeltaOverDOneThird"]
        for row in rows
    ]
    weighted_ratios = [
        row["rootLedgerScaling"]["besselWeightedRatioProxy"] for row in rows
    ]
    return rows, {
        "fitsAgainstDelta": {
            "D": log_fit(deltas, data_values),
            "S2H1Barrier": log_fit(deltas, barrier_values),
            "purePowerRatio": log_fit(deltas, pure_ratios),
            "besselWeightedRatio": log_fit(deltas, weighted_ratios),
        },
        "expectedPowers": {
            "deltaInR": 4.0,
            "PInDelta": 1.0,
            "shearEnstrophyInDelta": 2.0,
            "DInDelta": 2.0,
            "S2H1BarrierInDeltaIgnoringLog": 5.0 / 3.0,
            "rootLedgerInDelta": 1.0,
            "DOneThirdInDelta": 2.0 / 3.0,
            "ratioInDelta": 1.0 / 3.0,
            "ratioInR": 4.0 / 3.0,
        },
        "formula": {
            "delta": "R^4",
            "P": "q0^2 * delta",
            "S2": "delta / log(2 + delta)",
            "D": "2*P^2*(1+q0^2) + 2*S2*(q0^2+2)",
            "h1Barrier": "max(1, (2*delta)^(2/3))",
            "selectedRootProxy": "S2 * frozenBesselSlopeMass",
            "ratioPowerLedger": "delta / D^(1/3), with bounded Lambda1",
        },
    }


def bessel_audit(counts: Sequence[int]) -> tuple[dict[str, Any], dict[int, float]]:
    maximum = max(counts)
    roots = np.asarray(jn_zeros(1, maximum), dtype=np.float64)
    # At a zero j of J1, J1'(j) = J0(j).  The frozen row slope is 2 J1'(j).
    slopes = 2.0 * np.asarray(jv(0, roots), dtype=np.float64)
    slope_squares = slopes**2
    cumulative = np.cumsum(slope_squares)
    target = 8.0 / math.pi**2
    rows: list[dict[str, Any]] = []
    masses: dict[int, float] = {}
    for count in counts:
        mass = float(cumulative[count - 1])
        masses[count] = mass
        ratio = mass / math.log(float(count))
        rows.append(
            {
                "R": count,
                "firstPositiveJ1Zero": float(roots[0]),
                "lastPositiveJ1Zero": float(roots[count - 1]),
                "lastTau": float(roots[count - 1] / 2.0),
                "selectedSlopeMass": mass,
                "massOverLogR": ratio,
                "targetEightOverPiSquared": target,
                "absoluteTargetError": abs(ratio - target),
                "relativeTargetError": abs(ratio - target) / target,
            }
        )
    residuals = np.abs(jv(1, roots))
    return {
        "definition": {
            "tauK": "j_(1,k)/2",
            "frozenSlope": "2*J1'(j_(1,k)) = 2*J0(j_(1,k))",
            "mass": "sum_{k<=R} |2*J0(j_(1,k))|^2",
            "asymptotic": "mass/log(R) -> 8/pi^2",
        },
        "prefixRows": rows,
        "roots": [float(value) for value in roots],
        "taus": [float(value / 2.0) for value in roots],
        "frozenSlopes": [float(value) for value in slopes],
        "rootResidual": {
            "maximumAbsJ1AtRoot": float(np.max(residuals)),
            "rmsAbsJ1AtRoot": float(np.sqrt(np.mean(residuals**2))),
        },
    }, masses


@dataclass(frozen=True)
class FourierConfig:
    modes: int
    x_max: float
    phase_step: float
    max_step: float
    progress_fraction: float


def validate_fourier_config(config: FourierConfig) -> None:
    if config.modes < 64 or config.modes % 2:
        raise ValueError("--fourier-modes must be an even integer at least 64")
    if config.x_max <= 0.0:
        raise ValueError("--x-max must be positive")
    if config.phase_step <= 0.0 or config.max_step <= 0.0:
        raise ValueError("--phase-step and --max-step must be positive")
    if not 0.0 < config.progress_fraction <= 1.0:
        raise ValueError("--progress-fraction must lie in (0,1]")


def action_integrand(coefficients: np.ndarray, modes: np.ndarray, x: float) -> float:
    """Return ||V(x) phi||_{A_q^-1}^2 in normalized Fourier Parseval."""

    shifted = np.zeros_like(coefficients)
    factor = -1j * math.exp(-x)
    shifted[1:] += factor * coefficients[:-1]
    shifted[:-1] += factor * coefficients[1:]
    weights = 1.0 / (modes * modes + Q0 ** -2)
    return float(np.sum(np.abs(shifted) ** 2 * weights).real)


def solve_action(
    delta: float,
    config: FourierConfig,
    progress: Callable[[float, int, float, float], None] | None = None,
) -> dict[str, Any]:
    """Strang split the diagonal heat part and exact-in-time potential part."""

    validate_fourier_config(config)
    size = config.modes
    modes = np.arange(-size // 2, size // 2, dtype=np.float64)
    theta = 2.0 * math.pi * np.arange(size, dtype=np.float64) / size
    cosine = np.cos(theta)
    diagonal_rates = modes * modes + Q0 ** -2

    coefficients = np.zeros(size, dtype=np.complex128)
    minus_one_index = size // 2 - 1
    coefficients[minus_one_index] = 1j

    x = 0.0
    steps = 0
    action = 0.0
    integrand = action_integrand(coefficients, modes, x)
    initial_integrand = integrand
    max_h1 = float(np.sum((modes * modes) * np.abs(coefficients) ** 2).real)
    max_l2 = float(np.sum(np.abs(coefficients) ** 2).real)
    max_tail_fraction = 0.0
    next_progress = config.progress_fraction

    while x < config.x_max:
        local_amplitude = delta * math.exp(-x)
        phase_limited_step = config.phase_step / max(local_amplitude, 1.0e-300)
        step = min(config.max_step, phase_limited_step, config.x_max - x)
        if step <= 0.0:
            raise RuntimeError("non-positive split-step size")

        half_heat = np.exp(-0.5 * step * diagonal_rates)
        coefficients *= half_heat

        # The potential-only propagator is exact over [x,x+step]:
        # exp(-2 i delta integral(e^-s ds) cos(theta)).
        phase_integral = delta * (math.exp(-x) - math.exp(-(x + step)))
        grid_values = np.fft.ifft(np.fft.ifftshift(coefficients)) * size
        grid_values *= np.exp(-2j * phase_integral * cosine)
        coefficients = np.fft.fftshift(np.fft.fft(grid_values) / size)
        coefficients *= half_heat

        new_x = x + step
        new_integrand = action_integrand(coefficients, modes, new_x)
        action += 0.5 * step * (integrand + new_integrand)
        x = new_x
        integrand = new_integrand
        steps += 1

        absolute_sq = np.abs(coefficients) ** 2
        l2 = float(np.sum(absolute_sq).real)
        h1 = float(np.sum((modes * modes) * absolute_sq).real)
        max_l2 = max(max_l2, l2)
        max_h1 = max(max_h1, h1)
        tail_mask = np.abs(modes) >= 0.4 * size
        tail_fraction = float(np.sum(absolute_sq[tail_mask]).real) / max(l2, 1.0e-300)
        max_tail_fraction = max(max_tail_fraction, tail_fraction)

        fraction = x / config.x_max
        if progress is not None and fraction + 1.0e-14 >= next_progress:
            progress(min(fraction, 1.0), steps, action, max_tail_fraction)
            next_progress += config.progress_fraction

    final_abs_sq = np.abs(coefficients) ** 2
    final_l2 = float(np.sum(final_abs_sq).real)
    final_h1 = float(np.sum((modes * modes) * final_abs_sq).real)
    barrier = max(1.0, (2.0 * delta) ** (2.0 / 3.0))
    return {
        "delta": delta,
        "Q": action,
        "steps": steps,
        "initialIntegrand": initial_integrand,
        "finalIntegrand": integrand,
        "initialL2Squared": 1.0,
        "finalL2Squared": final_l2,
        "maximumL2Squared": max_l2,
        "finalH1SeminormSquared": final_h1,
        "maximumH1SeminormSquared": max_h1,
        "analyticH1Barrier": barrier,
        "maximumH1ToBarrier": max_h1 / barrier,
        "maximumSpectralTailFraction": max_tail_fraction,
        "deltaQOverLogDelta": delta * action / math.log(delta),
        "S2Q": delta * action / math.log(2.0 + delta),
    }


def action_audit(
    deltas: Sequence[int], config: FourierConfig, monitor: RunMonitor
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    coarse_modes = max(64, config.modes // 2)
    if coarse_modes % 2:
        coarse_modes += 1
    coarse = FourierConfig(
        modes=coarse_modes,
        x_max=config.x_max,
        phase_step=2.0 * config.phase_step,
        max_step=2.0 * config.max_step,
        progress_fraction=config.progress_fraction,
    )

    for delta_int in deltas:
        delta = float(delta_int)
        monitor.emit(
            "action-coarse-start",
            f"delta={delta_int}: coarse split-step run",
            delta=delta_int,
            modes=coarse.modes,
        )

        def coarse_progress(fraction: float, steps: int, q_value: float, tail: float) -> None:
            monitor.emit(
                "action-coarse-progress",
                f"delta={delta_int}: {100.0*fraction:.0f}%",
                delta=delta_int,
                fraction=round(fraction, 6),
                steps=steps,
                partialQ=q_value,
                maximumTailFraction=tail,
            )

        coarse_row = solve_action(delta, coarse, coarse_progress)

        monitor.emit(
            "action-fine-start",
            f"delta={delta_int}: fine split-step run",
            delta=delta_int,
            modes=config.modes,
        )

        def fine_progress(fraction: float, steps: int, q_value: float, tail: float) -> None:
            monitor.emit(
                "action-fine-progress",
                f"delta={delta_int}: {100.0*fraction:.0f}%",
                delta=delta_int,
                fraction=round(fraction, 6),
                steps=steps,
                partialQ=q_value,
                maximumTailFraction=tail,
            )

        fine_row = solve_action(delta, config, fine_progress)
        relative_difference = abs(fine_row["Q"] - coarse_row["Q"]) / max(
            abs(fine_row["Q"]), 1.0e-300
        )
        row = {
            **fine_row,
            "coarseQ": coarse_row["Q"],
            "coarseSteps": coarse_row["steps"],
            "coarseModes": coarse.modes,
            "fineCoarseRelativeDifference": relative_difference,
        }
        rows.append(row)
        monitor.emit(
            "action-delta-complete",
            (
                f"delta={delta_int}: Q={fine_row['Q']:.8e}, "
                f"fine/coarse rel={relative_difference:.3e}"
            ),
            delta=delta_int,
            Q=fine_row["Q"],
            relativeDifference=relative_difference,
        )

    delta_values = [float(row["delta"]) for row in rows]
    q_values = [float(row["Q"]) for row in rows]
    return {
        "equation": (
            "phi_x=(partial_theta^2-q0^-2)phi"
            "-2*i*delta*exp(-x)*cos(theta)*phi, phi(0)=i*exp(-i*theta)"
        ),
        "action": "integral_0^X ||V(x)phi||_(q0^-2-partial_theta^2)^(-1)^2 dx",
        "method": {
            "name": "time-dependent Strang split-step Fourier",
            "heatSubstep": "exact diagonal Fourier multiplier",
            "potentialSubstep": "exact integral of exp(-x) over each time step",
            "quadrature": "trapezoidal on the adaptive split-step grid",
            "adaptiveRule": "h=min(maxStep,phaseStep/(delta*exp(-x)),X-x)",
            "fine": {
                "modes": config.modes,
                "xMax": config.x_max,
                "phaseStep": config.phase_step,
                "maxStep": config.max_step,
            },
            "coarse": {
                "modes": coarse.modes,
                "xMax": coarse.x_max,
                "phaseStep": coarse.phase_step,
                "maxStep": coarse.max_step,
            },
        },
        "rows": rows,
        "fitsAgainstDelta": {
            "Q": log_fit(delta_values, q_values),
            "deltaQOverLogDelta": log_fit(
                delta_values, [row["deltaQOverLogDelta"] for row in rows]
            ),
            "S2Q": log_fit(delta_values, [row["S2Q"] for row in rows]),
        },
    }


def make_checks(
    bessel: dict[str, Any],
    raw_rows: list[dict[str, Any]],
    power_ledger: dict[str, Any],
    action: dict[str, Any],
    requested_deltas: Sequence[int],
    requested_counts: Sequence[int],
) -> dict[str, dict[str, Any]]:
    bessel_rows = bessel["prefixRows"]
    mass_errors = [row["absoluteTargetError"] for row in bessel_rows]
    mass_last_relative = bessel_rows[-1]["relativeTargetError"]
    root_residual = bessel["rootResidual"]["maximumAbsJ1AtRoot"]

    data_absolute_residual = max(
        row["launch"]["closedFormAbsoluteResidual"] for row in raw_rows
    )
    data_relative_residual = max(
        row["launch"]["closedFormRelativeResidual"] for row in raw_rows
    )
    barrier_balance = max(
        row["h1Barrier"]["barrierBalanceRelativeResidual"] for row in raw_rows
    )
    barrier_ratios = [
        row["h1Barrier"]["S2TimesBarrierOverDeltaSquared"] for row in raw_rows
    ]
    active_shear_ratios = [
        row["h1Barrier"]["activeBarrierOverLaunchShearEnstrophy"]
        for row in raw_rows
    ]

    action_rows = action["rows"]
    delta_q_log = [row["deltaQOverLogDelta"] for row in action_rows]
    s2_q = [row["S2Q"] for row in action_rows]
    convergence = max(row["fineCoarseRelativeDifference"] for row in action_rows)
    tails = max(row["maximumSpectralTailFraction"] for row in action_rows)
    h1_numeric = max(row["maximumH1ToBarrier"] for row in action_rows)
    l2_growth = max(row["maximumL2Squared"] for row in action_rows) - 1.0

    pure_slope = power_ledger["fitsAgainstDelta"]["purePowerRatio"]["slope"]
    weighted_slope = power_ledger["fitsAgainstDelta"]["besselWeightedRatio"]["slope"]
    d_slope = power_ledger["fitsAgainstDelta"]["D"]["slope"]

    full_delta_grid = tuple(requested_deltas) == DEFAULT_DELTAS
    full_bessel_grid = tuple(requested_counts) == DEFAULT_BESSEL_COUNTS
    return {
        "fixedQ0": {
            "value": Q0,
            "expected": 4,
            "passed": Q0 == 4,
        },
        "defaultDeltaGrid": {
            "observed": list(requested_deltas),
            "expected": list(DEFAULT_DELTAS),
            "passed": full_delta_grid,
            "informationalWhenCustomGrid": True,
        },
        "defaultBesselGrid": {
            "observed": list(requested_counts),
            "expected": list(DEFAULT_BESSEL_COUNTS),
            "passed": full_bessel_grid,
            "informationalWhenCustomGrid": True,
        },
        "exactDataRecomposition": {
            "maximumAbsoluteResidual": data_absolute_residual,
            "maximumRelativeResidual": data_relative_residual,
            "relativeTolerance": 2.0e-15,
            "note": "absolute ulp size grows with D; the pass criterion is relative",
            "passed": data_relative_residual <= 2.0e-15,
        },
        "dataDeltaPowerTwo": {
            "fittedExponent": d_slope,
            "expected": 2.0,
            "tolerance": 0.01,
            "passed": abs(d_slope - 2.0) <= 0.01,
        },
        "besselRoots": {
            "maximumAbsJ1Residual": root_residual,
            "tolerance": 1.0e-10,
            "passed": root_residual <= 1.0e-10,
        },
        "besselMassOverLogR": {
            "firstAbsoluteError": mass_errors[0],
            "lastAbsoluteError": mass_errors[-1],
            "lastRelativeError": mass_last_relative,
            "requiredLastRelativeError": 0.30,
            "passed": bool(
                mass_errors[-1] < mass_errors[0] and mass_last_relative <= 0.30
            ),
        },
        "splitStepConvergence": {
            "maximumFineCoarseRelativeDifference": convergence,
            "tolerance": 0.08,
            "passed": convergence <= 0.08,
        },
        "spectralTruncation": {
            "maximumTailFraction": tails,
            "tolerance": 1.0e-8,
            "passed": tails <= 1.0e-8,
        },
        "l2Dissipation": {
            "maximumL2SquaredExcessAboveOne": l2_growth,
            "tolerance": 1.0e-10,
            "passed": l2_growth <= 1.0e-10,
        },
        "deltaQOverLogDeltaBounded": bounded_sequence(delta_q_log, 4.0),
        "S2QBounded": bounded_sequence(s2_q, 4.0),
        "h1BarrierBalance": {
            "maximumRelativeResidual": barrier_balance,
            "tolerance": 1.0e-12,
            "passed": barrier_balance <= 1.0e-12,
        },
        "h1BarrierNumerical": {
            "maximumObservedToAnalyticBarrier": h1_numeric,
            "tolerance": 1.001,
            "passed": h1_numeric <= 1.001,
        },
        "activeH1BelowShearScale": {
            "firstS2BarrierOverDeltaSquared": barrier_ratios[0],
            "lastS2BarrierOverDeltaSquared": barrier_ratios[-1],
            "firstActiveBarrierOverShear": active_shear_ratios[0],
            "lastActiveBarrierOverShear": active_shear_ratios[-1],
            "passed": bool(
                barrier_ratios[-1] < barrier_ratios[0]
                and active_shear_ratios[-1] < active_shear_ratios[0]
            ),
        },
        "ratioExponentOneThird": {
            "purePowerFittedExponentInDelta": pure_slope,
            "besselWeightedFittedExponentInDelta": weighted_slope,
            "expectedExponentInDelta": 1.0 / 3.0,
            "expectedExponentInR": 4.0 / 3.0,
            "purePowerTolerance": 0.01,
            "finiteBesselTolerance": 0.10,
            "passed": bool(
                abs(pure_slope - 1.0 / 3.0) <= 0.01
                and abs(weighted_slope - 1.0 / 3.0) <= 0.10
            ),
        },
    }


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="JSON audit output")
    parser.add_argument(
        "--progress-log", type=Path, help="optional NDJSON progress log (truncated)"
    )
    parser.add_argument(
        "--resource-log", type=Path, help="optional NDJSON resource log (truncated)"
    )
    parser.add_argument(
        "--deltas",
        default=",".join(str(value) for value in DEFAULT_DELTAS),
        help="strictly increasing action couplings",
    )
    parser.add_argument(
        "--bessel-counts",
        default=",".join(str(value) for value in DEFAULT_BESSEL_COUNTS),
        help="strictly increasing Bessel prefix sizes",
    )
    parser.add_argument("--fourier-modes", type=int, default=512)
    parser.add_argument("--x-max", type=float, default=6.0)
    parser.add_argument(
        "--phase-step",
        type=float,
        default=0.06,
        help="maximum delta*exp(-x)*h for the fine run",
    )
    parser.add_argument("--max-step", type=float, default=0.01)
    parser.add_argument("--progress-fraction", type=float, default=0.25)
    return parser.parse_args()


def main() -> int:
    args = arguments()
    try:
        deltas = parse_positive_ints(args.deltas, "--deltas")
        counts = parse_positive_ints(args.bessel_counts, "--bessel-counts")
        config = FourierConfig(
            modes=args.fourier_modes,
            x_max=args.x_max,
            phase_step=args.phase_step,
            max_step=args.max_step,
            progress_fraction=args.progress_fraction,
        )
        validate_fourier_config(config)
        monitor = RunMonitor(args.progress_log, args.resource_log)
    except (argparse.ArgumentTypeError, ValueError) as exc:
        print(f"configuration error: {exc}", file=sys.stderr)
        return 2

    monitor.emit("start", f"starting {AUDIT_ID}", q0=Q0)
    monitor.emit("bessel-start", f"computing {max(counts)} positive J1 roots")
    bessel, masses = bessel_audit(counts)
    monitor.emit(
        "bessel-complete",
        f"computed roots and masses through R={max(counts)}",
        maximumRootResidual=bessel["rootResidual"]["maximumAbsJ1AtRoot"],
    )

    monitor.emit("raw-ledger-start", "recomputing amplitudes, data, and enstrophy")
    raw_rows, power_ledger = raw_parameter_ledger(counts, masses)
    monitor.emit("raw-ledger-complete", "raw physical ledger complete")

    monitor.emit("action-start", f"running action grid {list(deltas)}")
    action = action_audit(deltas, config, monitor)
    monitor.emit("action-complete", "all split-step action runs complete")

    checks = make_checks(bessel, raw_rows, power_ledger, action, deltas, counts)
    required_check_names = [
        name
        for name in checks
        if name not in {"defaultDeltaGrid", "defaultBesselGrid"}
    ]
    all_required_passed = all(bool(checks[name]["passed"]) for name in required_check_names)
    default_grid_complete = bool(
        checks["defaultDeltaGrid"]["passed"] and checks["defaultBesselGrid"]["passed"]
    )

    environment = {
        "python": sys.version,
        "pythonExecutable": sys.executable,
        "pythonImplementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "logicalCpus": os.cpu_count(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "gitRevision": git_revision(),
        "commandLine": sys.argv,
        "floatingPoint": "IEEE-754 binary64 / NumPy complex128",
        "fftBackend": "numpy.fft (pocketfft)",
    }
    result: dict[str, Any] = {
        "schemaVersion": SCHEMA_VERSION,
        "auditId": AUDIT_ID,
        "status": "passed" if all_required_passed else "failed",
        "defaultGridComplete": default_grid_complete,
        "createdUtc": utc_now(),
        "elapsedSeconds": monitor.elapsed,
        "inputPolicy": {
            "externalResearchInputsRead": False,
            "certificateInputsRead": False,
            "statement": (
                "All quantities are generated from constants and raw formulas "
                "in this program."
            ),
        },
        "configuration": {
            "q0": Q0,
            "deltas": list(deltas),
            "besselCounts": list(counts),
            "fourierModes": config.modes,
            "xMax": config.x_max,
            "phaseStep": config.phase_step,
            "maxStep": config.max_step,
            "progressFraction": config.progress_fraction,
            "progressLog": str(args.progress_log) if args.progress_log else None,
            "resourceLog": str(args.resource_log) if args.resource_log else None,
        },
        "environment": environment,
        "rawParameters": {
            "q0": Q0,
            "nu": 1,
            "d": 1,
            "Kz": 1,
            "z1": 1,
            "Ky": 0,
            "r1": 1,
            "initialActiveMode": -1,
            "initialCoefficient": "i",
        },
        "bessel": bessel,
        "physicalLedger": {
            "rows": raw_rows,
            **power_ledger,
        },
        "negativeSobolevAction": action,
        "checks": checks,
        "allRequiredChecksPassed": all_required_passed,
        "limitations": [
            "Floating-point calculations are not directed-rounding interval proofs.",
            (
                "Frozen Bessel masses corroborate the asymptotic root ledger; "
                "exact dissipative-root persistence is analytic."
            ),
            (
                "The split-step action values test scaling on a finite delta "
                "grid and finite Fourier truncation."
            ),
        ],
    }

    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode("utf-8")
    result["payloadSha256BeforeChecksumField"] = hashlib.sha256(canonical).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    monitor.emit(
        "complete",
        f"wrote {args.output}; status={result['status']}",
        output=str(args.output),
        status=result["status"],
        elapsedSeconds=result["elapsedSeconds"],
    )
    return 0 if all_required_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
