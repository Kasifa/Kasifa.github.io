#!/usr/bin/env python3
"""Independent finite numerical audit for R0.72E.

This program imports neither an R0.72E producer nor any producer output.  It
checks two different finite-dimensional shadows of the analytic argument:

* a fixed-step real-lattice RK4 scan discovers the Bessel target roots and
  recomputes their selected squared-slope mass at fixed ``q0=4``;
* an adaptive implicit BDF solve on the same real invariant lattice estimates
  the full dimensionless negative-Sobolev action for ``delta=16,...,128``.

The physical ``D/Y/q0`` ledger is then rebuilt from the raw amplitudes.  These
binary64 finite-lattice calculations corroborate constants, signs, and power
bookkeeping.  They are not interval arithmetic and do not prove the analytic
infinite-lattice or Malliavin-density statements in R0.72E.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import json
import math
import os
from pathlib import Path
import platform
import resource
import sys
import time
from typing import Any, Callable

import numpy as np
import scipy
from scipy.integrate import simpson, solve_ivp
from scipy.optimize import brentq
from scipy.sparse import diags
from scipy.special import j0, jn_zeros


Q0 = 4
MU = Q0**-2
R_VALUES = (8, 16, 32, 64)
ACTION_DELTAS = (16.0, 32.0, 64.0, 128.0)
ROOT_STEP = 0.004
ROOT_RIGHT_MARGIN = 0.30
ACTION_X = 1.0
ACTION_RADIUS = 64
ACTION_CHECK_RADIUS = 88
ACTION_RTOL = 2.0e-9
ACTION_ATOL = 2.0e-11
ACTION_TIGHT_RTOL = 4.0e-10
ACTION_TIGHT_ATOL = 4.0e-12
ACTION_QUADRATURE_INTERVALS = 128
EDGE_WIDTH = 8


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--progress-log",
        type=Path,
        help="optional NDJSON progress log written by this process",
    )
    parser.add_argument(
        "--resource-log",
        type=Path,
        help="optional NDJSON CPU/RSS resource log written by this process",
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="run a reduced preflight (R=8,16 and delta=16,32)",
    )
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def current_rss_bytes() -> int:
    """Return process RSS when psutil exists, otherwise peak RSS."""

    try:
        import psutil  # type: ignore[import-not-found]

        return int(psutil.Process(os.getpid()).memory_info().rss)
    except (ImportError, OSError):
        usage = resource.getrusage(resource.RUSAGE_SELF)
        raw = int(usage.ru_maxrss)
        return raw if sys.platform == "darwin" else 1024 * raw


def peak_rss_bytes() -> int:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    raw = int(usage.ru_maxrss)
    return raw if sys.platform == "darwin" else 1024 * raw


class Monitor:
    """Mirror progress to stderr and optional self-owned NDJSON logs."""

    def __init__(self, progress_path: Path | None, resource_path: Path | None):
        self.started_wall = time.perf_counter()
        self.started_cpu = time.process_time()
        self.event_index = 0
        self.logical_cpus = int(os.cpu_count() or 1)
        self.progress_handle = self._open(progress_path)
        self.resource_handle = self._open(resource_path)

    @staticmethod
    def _open(path: Path | None):
        if path is None:
            return None
        path.parent.mkdir(parents=True, exist_ok=True)
        return path.open("w", encoding="utf-8")

    def close(self) -> None:
        for handle in (self.progress_handle, self.resource_handle):
            if handle is not None:
                handle.flush()
                handle.close()

    def event(
        self,
        stage: str,
        status: str,
        message: str,
        **fields: object,
    ) -> None:
        self.event_index += 1
        elapsed = time.perf_counter() - self.started_wall
        cpu = time.process_time() - self.started_cpu
        rss = current_rss_bytes()
        sample: dict[str, object] = {
            "schemaVersion": "r072e-monitor-v1",
            "timestamp": utc_now(),
            "eventIndex": self.event_index,
            "stage": stage,
            "status": status,
            "message": message,
            "elapsedSeconds": elapsed,
            "processCpuSeconds": cpu,
            "averageCpuPercentOfOneCore": 100.0 * cpu / max(elapsed, 1.0e-12),
            "averageLogicalCpuCapacityFraction": (
                cpu / max(elapsed * self.logical_cpus, 1.0e-12)
            ),
            "rssBytes": rss,
            "peakRssBytes": peak_rss_bytes(),
            "logicalCpus": self.logical_cpus,
            **fields,
        }
        print(
            "[{}] {}/{} {} | elapsed={:.2f}s cpu={:.2f}s rss={:.1f}MiB".format(
                sample["timestamp"],
                stage,
                status,
                message,
                elapsed,
                cpu,
                rss / 2.0**20,
            ),
            file=sys.stderr,
            flush=True,
        )
        if self.progress_handle is not None:
            self.progress_handle.write(json.dumps(sample, sort_keys=True) + "\n")
            self.progress_handle.flush()
        if self.resource_handle is not None:
            resource_sample = {
                "schemaVersion": "r072e-resource-v1",
                "timestamp": sample["timestamp"],
                "eventIndex": self.event_index,
                "stage": stage,
                "status": status,
                "elapsedSeconds": elapsed,
                "processCpuSeconds": cpu,
                "averageCpuPercentOfOneCore": sample[
                    "averageCpuPercentOfOneCore"
                ],
                "averageLogicalCpuCapacityFraction": sample[
                    "averageLogicalCpuCapacityFraction"
                ],
                "rssBytes": rss,
                "peakRssBytes": sample["peakRssBytes"],
                "logicalCpus": self.logical_cpus,
                **fields,
            }
            self.resource_handle.write(
                json.dumps(resource_sample, sort_keys=True) + "\n"
            )
            self.resource_handle.flush()


def check(name: str, passed: bool, value: object, requirement: str) -> dict[str, object]:
    return {
        "name": name,
        "passed": bool(passed),
        "value": value,
        "requirement": requirement,
    }


def real_rhs(
    time_value: float,
    state: np.ndarray,
    indices: np.ndarray,
    delta: float,
    time_scale: float,
) -> np.ndarray:
    """Invariant real lattice for F_r=(-i)^r u_r.

    ``time_scale=delta`` means the independent variable is tau=delta*x;
    ``time_scale=1`` means it is the scaled physical variable x.
    """

    derivative = -((indices**2 + MU) / time_scale) * state
    amplitude = (delta / time_scale) * math.exp(-time_value / time_scale)
    derivative[1:] += amplitude * state[:-1]
    derivative[:-1] -= amplitude * state[1:]
    return derivative


def rk4_step(
    tau: float,
    state: np.ndarray,
    step: float,
    indices: np.ndarray,
    delta: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rhs: Callable[[float, np.ndarray], np.ndarray] = lambda t, u: real_rhs(
        t, u, indices, delta, delta
    )
    k1 = rhs(tau, state)
    k2 = rhs(tau + step / 2.0, state + step * k1 / 2.0)
    k3 = rhs(tau + step / 2.0, state + step * k2 / 2.0)
    k4 = rhs(tau + step, state + step * k3)
    next_state = state + step * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
    return next_state, k1, rhs(tau + step, next_state)


def hermite_state(
    fraction: float,
    left: np.ndarray,
    right: np.ndarray,
    left_derivative: np.ndarray,
    right_derivative: np.ndarray,
    step: float,
) -> np.ndarray:
    s = fraction
    h00 = 2.0 * s**3 - 3.0 * s**2 + 1.0
    h10 = s**3 - 2.0 * s**2 + s
    h01 = -2.0 * s**3 + 3.0 * s**2
    h11 = s**3 - s**2
    return (
        h00 * left
        + h10 * step * left_derivative
        + h01 * right
        + h11 * step * right_derivative
    )


def solve_roots(r_value: int, monitor: Monitor, smoke: bool) -> dict[str, object]:
    delta = float(r_value**4)
    radius = 5 * r_value + 30
    indices = np.arange(-radius, radius + 1, dtype=float)
    target = radius
    state = np.zeros(indices.size, dtype=float)
    state[target - 1] = 1.0
    limiting_zeros = jn_zeros(1, r_value)
    final_tau = float(limiting_zeros[-1] / 2.0 + ROOT_RIGHT_MARGIN)
    step_size = ROOT_STEP if not smoke else 2.0 * ROOT_STEP
    tau = 0.0
    previous_target = float(state[target])
    roots: list[dict[str, float]] = []
    maximum_norm = 1.0
    minimum_norm = 1.0
    steps = 0
    started = time.perf_counter()
    next_milestone = 0.25

    while tau < final_tau - 1.0e-15:
        step = min(step_size, final_tau - tau)
        next_state, left_derivative, right_derivative = rk4_step(
            tau, state, step, indices, delta
        )
        next_target = float(next_state[target])
        if tau > 0.0 and previous_target * next_target < 0.0:

            def interpolated_target(fraction: float) -> float:
                return float(
                    hermite_state(
                        fraction,
                        state,
                        next_state,
                        left_derivative,
                        right_derivative,
                        step,
                    )[target]
                )

            fraction = float(
                brentq(interpolated_target, 0.0, 1.0, xtol=2.0e-14, rtol=2.0e-14)
            )
            root_tau = tau + fraction * step
            root_state = hermite_state(
                fraction,
                state,
                next_state,
                left_derivative,
                right_derivative,
                step,
            )
            amplitude = math.exp(-root_tau / delta)
            h_value = amplitude * (root_state[target - 1] - root_state[target + 1])
            roots.append(
                {
                    "tau": root_tau,
                    "x": root_tau / delta,
                    "physicalTime": root_tau / (delta * Q0**2),
                    "h": float(h_value),
                    "hSquare": float(h_value**2),
                    "stateNormSquare": float(np.dot(root_state, root_state)),
                    "thetaDerivativeNormSquare": float(
                        np.dot(indices**2, root_state**2)
                    ),
                    "interpolatedTargetResidual": abs(
                        interpolated_target(fraction)
                    ),
                }
            )

        norm = float(np.linalg.norm(next_state))
        maximum_norm = max(maximum_norm, norm)
        minimum_norm = min(minimum_norm, norm)
        tau += step
        state = next_state
        previous_target = next_target
        steps += 1
        fraction_done = tau / final_tau
        if fraction_done + 1.0e-12 >= next_milestone:
            monitor.event(
                "root-scan",
                "progress",
                f"R={r_value} reached {int(round(100 * next_milestone))}%",
                R=r_value,
                delta=delta,
                fraction=min(fraction_done, 1.0),
                rootsFound=len(roots),
                steps=steps,
            )
            next_milestone += 0.25

    if len(roots) != r_value:
        raise AssertionError(f"sign scan found {len(roots)} roots for R={r_value}")

    exact_mass = float(sum(row["hSquare"] for row in roots))
    bessel_mass = float(4.0 * np.sum(j0(limiting_zeros) ** 2))
    limiting_roots = limiting_zeros / 2.0
    root_shifts = [
        float(row["tau"] - limiting)
        for row, limiting in zip(roots, limiting_roots, strict=True)
    ]
    return {
        "R": r_value,
        "q0": Q0,
        "mu": MU,
        "delta": delta,
        "physicalShearAmplitude": Q0**2 * delta,
        "radius": radius,
        "dimension": int(indices.size),
        "step": step_size,
        "steps": steps,
        "finalTau": final_tau,
        "scaledLayerLength": final_tau / delta,
        "physicalLayerLength": final_tau / (delta * Q0**2),
        "exactSelectedMass": exact_mass,
        "besselMass": bessel_mass,
        "massDifference": exact_mass - bessel_mass,
        "relativeMassDifference": (exact_mass - bessel_mass) / bessel_mass,
        "maximumRootShift": max(abs(value) for value in root_shifts),
        "R2TimesMaximumRootShift": r_value**2 * max(abs(value) for value in root_shifts),
        "maximumNorm": maximum_norm,
        "minimumNorm": minimum_norm,
        "maximumTargetResidual": max(
            float(row["interpolatedTargetResidual"]) for row in roots
        ),
        "elapsedSeconds": time.perf_counter() - started,
        "roots": roots,
    }


def action_integrand(
    times: np.ndarray,
    states: np.ndarray,
    indices: np.ndarray,
) -> np.ndarray:
    differences = np.zeros_like(states)
    differences[1:, :] += states[:-1, :]
    differences[:-1, :] -= states[1:, :]
    weights = 1.0 / (indices**2 + MU)
    return np.exp(-2.0 * times) * np.sum(
        weights[:, None] * differences**2, axis=0
    )


def action_boundaries(delta: float, final_x: float) -> list[float]:
    mixing_scales = np.array(
        [0.0, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0, 128.0]
    )
    candidates = [float(value / delta) for value in mixing_scales]
    candidates.extend(float(value) for value in np.linspace(0.0, final_x, 5))
    candidates.append(final_x)
    return sorted({min(final_x, max(0.0, value)) for value in candidates})


def solve_action(
    delta: float,
    radius: int,
    monitor: Monitor,
    smoke: bool,
    label: str,
    rtol: float = ACTION_RTOL,
    atol: float = ACTION_ATOL,
) -> dict[str, object]:
    indices = np.arange(-radius, radius + 1, dtype=float)
    dimension = int(indices.size)
    state = np.zeros(dimension, dtype=float)
    state[radius - 1] = 1.0
    final_x = 0.25 if smoke else ACTION_X
    intervals = 48 if smoke else ACTION_QUADRATURE_INTERVALS
    if intervals % 2:
        raise AssertionError("Simpson interval count must be even")
    boundaries = action_boundaries(delta, final_x)
    diagonal = -(indices**2 + MU)
    off_diagonal = np.ones(dimension - 1, dtype=float)
    action_fine = 0.0
    action_coarse = 0.0
    nfev = njev = nlu = 0
    maximum_norm = 1.0
    maximum_edge_fraction = 0.0
    maximum_endpoint_norm_increase = 0.0
    previous_endpoint_norm = 1.0
    solver_messages: list[str] = []
    started = time.perf_counter()

    def ode_rhs(x_value: float, vector: np.ndarray) -> np.ndarray:
        return real_rhs(x_value, vector, indices, delta, 1.0)

    def ode_jacobian(x_value: float, _vector: np.ndarray):
        amplitude = delta * math.exp(-x_value)
        return diags(
            [amplitude * off_diagonal, diagonal, -amplitude * off_diagonal],
            offsets=[-1, 0, 1],
            shape=(dimension, dimension),
            format="csc",
        )

    for segment_index, (left, right) in enumerate(
        zip(boundaries[:-1], boundaries[1:], strict=True), start=1
    ):
        if right <= left:
            continue
        solution = solve_ivp(
            ode_rhs,
            (left, right),
            state,
            method="BDF",
            rtol=rtol,
            atol=atol,
            jac=ode_jacobian,
            dense_output=True,
            max_step=(right - left) / 4.0,
        )
        if not solution.success or solution.sol is None:
            raise RuntimeError(
                f"BDF failed for delta={delta}, radius={radius}: {solution.message}"
            )
        grid = np.linspace(left, right, intervals + 1)
        sampled_states = np.asarray(solution.sol(grid), dtype=float)
        sampled_integrand = action_integrand(grid, sampled_states, indices)
        action_fine += float(simpson(sampled_integrand, x=grid))
        action_coarse += float(simpson(sampled_integrand[::2], x=grid[::2]))
        norms = np.linalg.norm(sampled_states, axis=0)
        maximum_norm = max(maximum_norm, float(np.max(norms)))
        endpoint_norm = float(norms[-1])
        maximum_endpoint_norm_increase = max(
            maximum_endpoint_norm_increase,
            endpoint_norm - previous_endpoint_norm,
        )
        previous_endpoint_norm = endpoint_norm
        energies = np.sum(sampled_states**2, axis=0)
        edge_energies = np.sum(sampled_states[:EDGE_WIDTH, :] ** 2, axis=0)
        edge_energies += np.sum(sampled_states[-EDGE_WIDTH:, :] ** 2, axis=0)
        maximum_edge_fraction = max(
            maximum_edge_fraction,
            float(np.max(edge_energies / np.maximum(energies, 1.0e-300))),
        )
        state = np.asarray(solution.y[:, -1], dtype=float)
        nfev += int(solution.nfev)
        njev += int(solution.njev)
        nlu += int(solution.nlu)
        solver_messages.append(str(solution.message))
        monitor.event(
            "action-bdf",
            "progress",
            (
                f"{label} delta={delta:g}, radius={radius}: "
                f"segment {segment_index}/{len(boundaries) - 1}"
            ),
            label=label,
            delta=delta,
            radius=radius,
            segment=segment_index,
            segments=len(boundaries) - 1,
            x=right,
            partialAction=action_fine,
            nfev=nfev,
            nlu=nlu,
        )

    relative_defect = abs(action_fine - action_coarse) / max(action_fine, 1.0e-300)
    return {
        "label": label,
        "delta": delta,
        "q0": Q0,
        "mu": MU,
        "finalX": final_x,
        "physicalFinalTime": final_x / Q0**2,
        "radius": radius,
        "dimension": dimension,
        "rtol": rtol,
        "atol": atol,
        "quadratureIntervalsPerSegment": intervals,
        "segmentBoundaries": boundaries,
        "actionFine": action_fine,
        "actionCoarse": action_coarse,
        "quadratureAbsoluteDefect": abs(action_fine - action_coarse),
        "quadratureRelativeDefect": relative_defect,
        "deltaTimesAction": delta * action_fine,
        "deltaActionOverOnePlusLog": (
            delta * action_fine / (1.0 + math.log(2.0 + delta))
        ),
        "maximumNorm": maximum_norm,
        "finalNorm": float(np.linalg.norm(state)),
        "maximumEndpointNormIncrease": maximum_endpoint_norm_increase,
        "maximumEdgeEnergyFraction": maximum_edge_fraction,
        "nfev": nfev,
        "njev": njev,
        "nlu": nlu,
        "solverMessages": sorted(set(solver_messages)),
        "elapsedSeconds": time.perf_counter() - started,
    }


def physical_ledger(
    root_rows: list[dict[str, object]],
    action_rows: list[dict[str, object]],
) -> dict[str, object]:
    """Rebuild every physical factor from P=q0^2*delta and S^2."""

    root_ledgers: list[dict[str, object]] = []
    for root_row in root_rows:
        delta = float(root_row["delta"])
        p_amplitude = Q0**2 * delta
        s_square = delta / math.log(2.0 + delta)
        data = (
            2.0 * p_amplitude**2 * (1.0 + Q0**2)
            + 2.0 * s_square * (Q0**2 + 2.0)
        )
        launch_y = 2.0 * Q0**2 * p_amplitude**2 + 2.0 * s_square * (
            1.0 + Q0**2
        )
        selected_ledger = 0.0
        atom_rows: list[dict[str, float]] = []
        roots = root_row["roots"]
        if not isinstance(roots, list):
            raise TypeError("root list missing")
        for root in roots:
            if not isinstance(root, dict):
                raise TypeError("root row malformed")
            x_value = float(root["x"])
            y_at_root = (
                2.0 * Q0**2 * p_amplitude**2 * math.exp(-2.0 * x_value)
                + 2.0
                * s_square
                * (
                    float(root["stateNormSquare"])
                    + Q0**2 * float(root["thetaDerivativeNormSquare"])
                )
            )
            atom = (
                s_square
                * p_amplitude**2
                * float(root["hSquare"])
                / y_at_root
            )
            selected_ledger += atom
            atom_rows.append(
                {
                    "x": x_value,
                    "physicalTime": x_value / Q0**2,
                    "exactYAtRoot": y_at_root,
                    "multiplierNormalizedAtom": atom,
                }
            )
        root_ledgers.append(
            {
                "R": int(root_row["R"]),
                "delta": delta,
                "P": p_amplitude,
                "SSquare": s_square,
                "DExact": data,
                "DOverDeltaSquare": data / delta**2,
                "DOneThird": data ** (1.0 / 3.0),
                "DOneThirdOverDeltaTwoThird": data ** (1.0 / 3.0)
                / delta ** (2.0 / 3.0),
                "YLaunchExact": launch_y,
                "selectedSlopeMass": float(root_row["exactSelectedMass"]),
                "multiplierNormalization": "c_star=1",
                "selectedLedgerUsingExactFullY": selected_ledger,
                "ledgerOverDOneThird": selected_ledger / data ** (1.0 / 3.0),
                "atoms": atom_rows,
            }
        )

    action_ledgers: list[dict[str, float]] = []
    for action_row in action_rows:
        delta = float(action_row["delta"])
        q_action = float(action_row["actionFine"])
        final_x = float(action_row["finalX"])
        physical_t = final_x / Q0**2
        p_amplitude = Q0**2 * delta
        s_square = delta / math.log(2.0 + delta)
        d_exact = (
            2.0 * p_amplitude**2 * (1.0 + Q0**2)
            + 2.0 * s_square * (Q0**2 + 2.0)
        )
        y_shear_floor = (
            2.0
            * Q0**2
            * p_amplitude**2
            * math.exp(-2.0 * final_x)
        )
        physical_action = (
            2.0 * s_square * p_amplitude**2 * Q0**-4 * q_action
        )
        charge_floor_bound_from_identities = physical_action / (
            physical_t * y_shear_floor
        )
        charge_floor_bound_collapsed = (
            math.exp(2.0 * final_x)
            * s_square
            * q_action
            / (final_x * Q0**4)
        )
        action_ledgers.append(
            {
                "delta": delta,
                "P": p_amplitude,
                "SSquare": s_square,
                "DExact": d_exact,
                "DOneThird": d_exact ** (1.0 / 3.0),
                "YShearFloor": y_shear_floor,
                "dimensionlessActionQ": q_action,
                "physicalHMinusOneFactor": Q0**-2,
                "physicalTimeJacobian": Q0**-2,
                "inverseShearFrequencyFactor": Q0**-2,
                "preAverageQ0Factor": Q0**-6,
                "physicalActionExact": physical_action,
                "physicalIntervalLength": physical_t,
                "normalizedChargeFloorBoundFromIdentities": (
                    charge_floor_bound_from_identities
                ),
                "normalizedChargeFloorBoundCollapsed": (
                    charge_floor_bound_collapsed
                ),
                "floorBoundIdentityDefect": abs(
                    charge_floor_bound_from_identities
                    - charge_floor_bound_collapsed
                ),
            }
        )

    log_delta = np.log([float(row["delta"]) for row in root_ledgers])
    log_data = np.log([float(row["DExact"]) for row in root_ledgers])
    log_ratio = np.log(
        [float(row["ledgerOverDOneThird"]) for row in root_ledgers]
    )
    return {
        "normalization": {
            "q0": Q0,
            "mu": MU,
            "PDefinition": "P=q0^2*delta",
            "SSquareDefinition": "S^2=delta/log(2+delta)",
            "DIdentity": "2*P^2*(1+q0^2)+2*S^2*(q0^2+2)",
            "YIdentity": (
                "2*q0^2*P^2*exp(-2x)+"
                "2*S^2*(||F||_2^2+q0^2||d_theta F||_2^2)"
            ),
            "physicalActionIdentity": "2*S^2*P^2*q0^-4*Q",
            "preAverageChargeFactor": "S^2*exp(2X)*q0^-6*Q",
        },
        "q0FactorAudit": {
            "threeQ0MinusTwoFactors": [Q0**-2, Q0**-2, Q0**-2],
            "theirProduct": Q0**-6,
            "expectedProduct": 1.0 / Q0**6,
            "afterPhysicalTimeAverageAtX1": Q0**-4,
        },
        "exactExponentLedger": {
            "deltaAsPowerOfR": 4,
            "DDeltaPower": 2,
            "DOneThirdDeltaPower": str(Fraction(2, 3)),
            "boundedLambdaDeltaPower": 0,
            "rootLedgerDeltaPower": 1,
            "ratioDeltaPower": str(Fraction(1, 3)),
            "ratioRPower": str(Fraction(4, 3)),
        },
        "empiricalDataDeltaExponent": float(np.polyfit(log_delta, log_data, 1)[0]),
        "empiricalLedgerRatioDeltaExponent": float(
            np.polyfit(log_delta, log_ratio, 1)[0]
        ),
        "rootLedgers": root_ledgers,
        "actionLedgers": action_ledgers,
    }


def main() -> None:
    args = parse_args()
    monitor = Monitor(args.progress_log, args.resource_log)
    started = time.perf_counter()
    try:
        monitor.event(
            "audit",
            "started",
            "R0.72E independent finite audit started",
            smokeMode=args.smoke,
            q0=Q0,
        )
        root_values = R_VALUES[:2] if args.smoke else R_VALUES
        action_deltas = ACTION_DELTAS[:2] if args.smoke else ACTION_DELTAS
        root_rows: list[dict[str, object]] = []
        for r_value in root_values:
            monitor.event(
                "root-scan",
                "started",
                f"R={r_value} real-lattice RK4 sign scan",
                R=r_value,
                delta=float(r_value**4),
            )
            row = solve_roots(r_value, monitor, args.smoke)
            root_rows.append(row)
            monitor.event(
                "root-scan",
                "completed",
                f"R={r_value}: {len(row['roots'])} roots, mass={float(row['exactSelectedMass']):.10f}",
                R=r_value,
                roots=len(row["roots"]),
                selectedMass=row["exactSelectedMass"],
                caseElapsedSeconds=row["elapsedSeconds"],
            )

        action_rows: list[dict[str, object]] = []
        for delta in action_deltas:
            monitor.event(
                "action-bdf",
                "started",
                f"primary BDF action solve for delta={delta:g}",
                delta=delta,
                radius=ACTION_RADIUS,
            )
            row = solve_action(
                delta, ACTION_RADIUS, monitor, args.smoke, label="primary"
            )
            action_rows.append(row)
            monitor.event(
                "action-bdf",
                "completed",
                f"delta={delta:g}: Q={float(row['actionFine']):.10e}",
                delta=delta,
                radius=ACTION_RADIUS,
                action=row["actionFine"],
                caseElapsedSeconds=row["elapsedSeconds"],
            )

        check_delta = float(action_deltas[-1])
        monitor.event(
            "action-truncation",
            "started",
            f"larger-radius action check for delta={check_delta:g}",
            delta=check_delta,
            radius=ACTION_CHECK_RADIUS,
        )
        radius_check = solve_action(
            check_delta,
            ACTION_CHECK_RADIUS,
            monitor,
            args.smoke,
            label="larger-radius-check",
        )
        primary_check_row = action_rows[-1]
        radius_relative_difference = abs(
            float(radius_check["actionFine"])
            - float(primary_check_row["actionFine"])
        ) / float(radius_check["actionFine"])
        monitor.event(
            "action-truncation",
            "completed",
            f"relative action difference={radius_relative_difference:.3e}",
            delta=check_delta,
            primaryRadius=ACTION_RADIUS,
            checkRadius=ACTION_CHECK_RADIUS,
            relativeDifference=radius_relative_difference,
        )

        monitor.event(
            "action-tolerance",
            "started",
            f"tighter-tolerance action check for delta={check_delta:g}",
            delta=check_delta,
            radius=ACTION_RADIUS,
            rtol=ACTION_TIGHT_RTOL,
            atol=ACTION_TIGHT_ATOL,
        )
        tolerance_check = solve_action(
            check_delta,
            ACTION_RADIUS,
            monitor,
            args.smoke,
            label="tighter-tolerance-check",
            rtol=ACTION_TIGHT_RTOL,
            atol=ACTION_TIGHT_ATOL,
        )
        tolerance_relative_difference = abs(
            float(tolerance_check["actionFine"])
            - float(primary_check_row["actionFine"])
        ) / float(tolerance_check["actionFine"])
        monitor.event(
            "action-tolerance",
            "completed",
            f"relative action difference={tolerance_relative_difference:.3e}",
            delta=check_delta,
            radius=ACTION_RADIUS,
            relativeDifference=tolerance_relative_difference,
        )

        ledger = physical_ledger(root_rows, action_rows)
        log_coefficient = 8.0 / math.pi**2
        log_residuals = [
            {
                "R": int(row["R"]),
                "massMinusLeadingLog": float(row["exactSelectedMass"])
                - log_coefficient * math.log(float(row["R"])),
            }
            for row in root_rows
        ]
        action_values = [float(row["actionFine"]) for row in action_rows]
        normalized_actions = [
            float(row["deltaActionOverOnePlusLog"]) for row in action_rows
        ]
        quadrature_defects = [
            float(row["quadratureRelativeDefect"]) for row in action_rows
        ] + [
            float(radius_check["quadratureRelativeDefect"]),
            float(tolerance_check["quadratureRelativeDefect"]),
        ]
        edge_fractions = [
            float(row["maximumEdgeEnergyFraction"]) for row in action_rows
        ] + [
            float(radius_check["maximumEdgeEnergyFraction"]),
            float(tolerance_check["maximumEdgeEnergyFraction"]),
        ]
        root_mass_tolerance = 2.0e-3 if args.smoke else 5.0e-5
        checks = [
            check(
                "discovered_root_count",
                all(len(row["roots"]) == row["R"] for row in root_rows),
                [len(row["roots"]) for row in root_rows],
                "unseeded sign scan finds exactly R positive crossings",
            ),
            check(
                "root_target_residual",
                max(float(row["maximumTargetResidual"]) for row in root_rows)
                < 2.0e-12,
                max(float(row["maximumTargetResidual"]) for row in root_rows),
                "Hermite-refined target residual is below 2e-12",
            ),
            check(
                "contractive_root_evolution",
                max(float(row["maximumNorm"]) for row in root_rows)
                <= 1.0 + 1.0e-8,
                max(float(row["maximumNorm"]) for row in root_rows),
                "fixed-step real RK4 evolution is contractive to tolerance",
            ),
            check(
                "bessel_mass_agreement",
                abs(float(root_rows[-1]["relativeMassDifference"]))
                < root_mass_tolerance,
                root_rows[-1]["relativeMassDifference"],
                f"largest-R mass agrees with frozen Bessel mass within {root_mass_tolerance:g}",
            ),
            check(
                "root_shift_decay",
                all(
                    float(later["maximumRootShift"])
                    < float(earlier["maximumRootShift"])
                    for earlier, later in zip(root_rows[:-1], root_rows[1:], strict=True)
                ),
                [row["maximumRootShift"] for row in root_rows],
                "maximum root shift decreases on the tested dyadic sequence",
            ),
            check(
                "action_positive_and_decreasing",
                all(value > 0.0 for value in action_values)
                and all(
                    later < earlier
                    for earlier, later in zip(
                        action_values[:-1], action_values[1:], strict=True
                    )
                ),
                action_values,
                "finite action is positive and decreases with coupling",
            ),
            check(
                "action_log_over_delta_scale",
                max(normalized_actions) / min(normalized_actions) < 2.0,
                normalized_actions,
                "delta*Q/(1+log(2+delta)) varies by less than a factor two",
            ),
            check(
                "action_quadrature_refinement",
                max(quadrature_defects) < 2.0e-4,
                max(quadrature_defects),
                "fine/coarse composite Simpson defect is below 2e-4 relative",
            ),
            check(
                "action_contractivity",
                max(
                    [float(row["maximumNorm"]) for row in action_rows]
                    + [
                        float(radius_check["maximumNorm"]),
                        float(tolerance_check["maximumNorm"]),
                    ]
                )
                <= 1.0 + 2.0e-6,
                max(
                    [float(row["maximumNorm"]) for row in action_rows]
                    + [
                        float(radius_check["maximumNorm"]),
                        float(tolerance_check["maximumNorm"]),
                    ]
                ),
                "BDF finite evolution remains contractive to tolerance",
            ),
            check(
                "action_boundary_negligible",
                max(edge_fractions) < 1.0e-10,
                max(edge_fractions),
                "outer eight-mode energy fraction stays below 1e-10",
            ),
            check(
                "action_radius_stability",
                radius_relative_difference < 2.0e-5,
                radius_relative_difference,
                "primary and larger-radius actions agree within 2e-5 relative",
            ),
            check(
                "action_tolerance_stability",
                tolerance_relative_difference < 2.0e-5,
                tolerance_relative_difference,
                "primary and tighter-tolerance actions agree within 2e-5 relative",
            ),
            check(
                "exact_q0_factor",
                abs(
                    float(ledger["q0FactorAudit"]["theirProduct"])
                    - float(ledger["q0FactorAudit"]["expectedProduct"])
                )
                < 1.0e-18,
                ledger["q0FactorAudit"],
                "three independently exposed q0^-2 factors multiply to q0^-6",
            ),
            check(
                "physical_charge_identity",
                max(
                    float(row["floorBoundIdentityDefect"])
                    for row in ledger["actionLedgers"]
                )
                < 2.0e-15,
                max(
                    float(row["floorBoundIdentityDefect"])
                    for row in ledger["actionLedgers"]
                ),
                "direct shear-floor upper bound equals the collapsed q0-factor formula",
            ),
            check(
                "data_delta_square_power",
                abs(float(ledger["empiricalDataDeltaExponent"]) - 2.0) < 2.0e-4,
                ledger["empiricalDataDeltaExponent"],
                "raw exact D has empirical delta exponent two",
            ),
            check(
                "one_third_exponent_reconstruction",
                ledger["exactExponentLedger"]["ratioDeltaPower"] == "1/3"
                and ledger["exactExponentLedger"]["ratioRPower"] == "4/3"
                and float(ledger["empiricalLedgerRatioDeltaExponent"]) > 0.24,
                {
                    "exact": ledger["exactExponentLedger"],
                    "empirical": ledger["empiricalLedgerRatioDeltaExponent"],
                },
                "D^(1/3) leaves delta^(1/3)=R^(4/3), with positive finite trend",
            ),
        ]

        payload: dict[str, Any] = {
            "schemaVersion": "r072e-independent-audit-v1",
            "release": "R0.72E",
            "generatedAt": utc_now(),
            "smokeMode": bool(args.smoke),
            "algorithm": {
                "rootState": "real invariant phase F_r=(-i)^r u_r",
                "rootIntegrator": "fixed-step classical RK4",
                "rootDiscovery": "unseeded sign changes plus cubic Hermite interpolation",
                "actionIntegrator": "SciPy solve_ivp BDF with analytic sparse tridiagonal Jacobian",
                "actionQuadrature": "nested composite Simpson on BDF dense output",
                "importsProducer": False,
                "readsProducerOutput": False,
            },
            "configuration": {
                "q0": Q0,
                "mu": MU,
                "RValues": list(root_values),
                "actionDeltas": list(action_deltas),
                "rootStep": ROOT_STEP if not args.smoke else 2.0 * ROOT_STEP,
                "rootRightMargin": ROOT_RIGHT_MARGIN,
                "actionFinalX": 0.25 if args.smoke else ACTION_X,
                "actionPhysicalFinalTime": (
                    (0.25 if args.smoke else ACTION_X) / Q0**2
                ),
                "actionRadius": ACTION_RADIUS,
                "actionCheckRadius": ACTION_CHECK_RADIUS,
                "actionRtol": ACTION_RTOL,
                "actionAtol": ACTION_ATOL,
                "actionTightRtol": ACTION_TIGHT_RTOL,
                "actionTightAtol": ACTION_TIGHT_ATOL,
                "actionQuadratureIntervalsPerSegment": (
                    48 if args.smoke else ACTION_QUADRATURE_INTERVALS
                ),
                "edgeWidth": EDGE_WIDTH,
            },
            "environment": {
                "python": platform.python_version(),
                "platform": platform.platform(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "numpy": np.__version__,
                "scipy": scipy.__version__,
                "logicalCpus": int(os.cpu_count() or 1),
                "threadEnvironment": {
                    key: os.environ.get(key)
                    for key in (
                        "OMP_NUM_THREADS",
                        "OPENBLAS_NUM_THREADS",
                        "MKL_NUM_THREADS",
                        "VECLIB_MAXIMUM_THREADS",
                    )
                },
            },
            "logCoefficient": log_coefficient,
            "logResiduals": log_residuals,
            "rootFiniteLattice": root_rows,
            "actionFiniteLattice": action_rows,
            "actionRadiusCheck": {
                "primary": primary_check_row,
                "largerRadius": radius_check,
                "relativeDifference": radius_relative_difference,
            },
            "actionToleranceCheck": {
                "primary": primary_check_row,
                "tighterTolerance": tolerance_check,
                "relativeDifference": tolerance_relative_difference,
            },
            "physicalLedger": ledger,
            "checks": checks,
            "allPassed": all(row["passed"] for row in checks),
            "elapsedSeconds": time.perf_counter() - started,
            "monitoring": {
                "stderr": True,
                "progressLog": str(args.progress_log) if args.progress_log else None,
                "resourceLog": str(args.resource_log) if args.resource_log else None,
            },
            "scope": {
                "precision": "IEEE-754 binary64",
                "finiteLattice": True,
                "intervalArithmetic": False,
                "provesInfiniteLattice": False,
                "provesMalliavinDensityBound": False,
                "provesNSERegularity": False,
                "note": "Independent finite numerical corroboration only.",
            },
        }
        if not payload["allPassed"]:
            failed = [row["name"] for row in checks if not row["passed"]]
            monitor.event(
                "audit",
                "failed",
                f"independent checks failed: {failed}",
                failedChecks=failed,
            )
            raise AssertionError(f"independent checks failed: {failed}")

        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        monitor.event(
            "audit",
            "completed",
            f"R0.72E independent audit passed in {payload['elapsedSeconds']:.2f}s",
            output=str(args.output),
            allPassed=True,
        )
    finally:
        monitor.close()


if __name__ == "__main__":
    main()
