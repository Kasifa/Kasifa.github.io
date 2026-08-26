#!/usr/bin/env python3
"""Pseudo-spectral Fourier--Galerkin shooting for the R0.71T figure.

The calculation stays in the x3-independent, three-component invariant
subspace of the periodic three-dimensional NSE.  It integrates the finite
Galerkin ODE and shoots an eight-real-dimensional target-shell correction so
that the |k|^2=2, k3=0 velocity shell vanishes at a prescribed positive time.
This is numerical corroboration of the analytic flow-map argument, not DNS or
a continuum PDE proof.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
import json
import math
import os
from pathlib import Path
import resource
from time import perf_counter
from typing import Callable
from zoneinfo import ZoneInfo

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root


TAUS = (0.005, 0.01, 0.02, 0.04, 0.08)


def timestamp() -> str:
    return datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="milliseconds")


def append_progress(path: Path, event: str, **payload: object) -> None:
    record = {"timestamp": timestamp(), "event": event, **payload}
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, sort_keys=True) + "\n")


def append_resource(path: Path, stage: str) -> None:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({
            "timestamp": timestamp(),
            "stage": stage,
            "pid": os.getpid(),
            "logicalCpuCount": os.cpu_count(),
            "loadAverage1m5m15m": list(os.getloadavg()),
            "processUserCpuSeconds": usage.ru_utime,
            "processSystemCpuSeconds": usage.ru_stime,
            "maximumResidentSetRaw": usage.ru_maxrss,
        }, sort_keys=True) + "\n")


def vector_norm_squared(values: np.ndarray) -> float:
    return float(np.vdot(values.ravel(), values.ravel()).real)


@dataclass
class SolveRecord:
    tau: float
    correction: np.ndarray
    endpoint: np.ndarray
    event_state: np.ndarray
    root_calls: int
    root_residual: float
    integration_calls: int
    function_evaluations: int


class PseudoSpectralGalerkin:
    """Dealiased finite Galerkin ODE in the x3-independent 3C sector."""

    representatives = ((1, 1), (1, -1))

    def __init__(
        self,
        grid_order: int,
        cutoff: int,
        viscosity: float,
        rtol: float,
        atol: float,
    ) -> None:
        if grid_order < 3 * cutoff + 1:
            raise ValueError("grid order is too small for retained quadratic modes")
        self.grid_order = grid_order
        self.cutoff = cutoff
        self.viscosity = viscosity
        self.rtol = rtol
        self.atol = atol
        integers = np.fft.fftfreq(grid_order, d=1.0 / grid_order)
        k1, k2 = np.meshgrid(integers, integers, indexing="ij")
        self.waves = np.stack([k1, k2, np.zeros_like(k1)], axis=-1)
        self.wave_squared = np.sum(self.waves * self.waves, axis=-1)
        self.retained = (
            (np.abs(k1) <= cutoff)
            & (np.abs(k2) <= cutoff)
            & (self.wave_squared > 0.0)
        )
        self.target = self.wave_squared == 2.0
        self._rhs_calls = 0

    def index(self, wave: tuple[int, int]) -> tuple[int, int]:
        return wave[0] % self.grid_order, wave[1] % self.grid_order

    def leray(self, coefficients: np.ndarray) -> np.ndarray:
        result = coefficients.copy()
        radial = np.sum(self.waves * result, axis=-1)
        nonzero = self.wave_squared > 0.0
        result[nonzero] -= (
            self.waves[nonzero]
            * (radial[nonzero] / self.wave_squared[nonzero])[:, None]
        )
        result[~nonzero] = 0.0
        return result

    def truncate(self, coefficients: np.ndarray) -> np.ndarray:
        result = self.leray(coefficients)
        result[~self.retained] = 0.0
        return result

    def seed(self, amplitude: float = 1.0) -> np.ndarray:
        result = np.zeros(
            (self.grid_order, self.grid_order, 3), dtype=np.complex128
        )
        for wave in ((1, 0), (-1, 0)):
            result[self.index(wave)] = (0.0, amplitude / 2.0, 0.0)
        for wave in ((0, 1), (0, -1)):
            result[self.index(wave)] = (0.0, 0.0, amplitude / 2.0)
        return result

    @staticmethod
    def polarizations(wave: tuple[int, int]) -> tuple[np.ndarray, np.ndarray]:
        length = math.hypot(*wave)
        return (
            np.asarray([-wave[1] / length, wave[0] / length, 0.0]),
            np.asarray([0.0, 0.0, 1.0]),
        )

    def from_target_coordinates(self, coordinates: np.ndarray) -> np.ndarray:
        if coordinates.shape != (8,):
            raise ValueError("target coordinate vector must have length eight")
        result = np.zeros(
            (self.grid_order, self.grid_order, 3), dtype=np.complex128
        )
        cursor = 0
        for wave in self.representatives:
            for polarization in self.polarizations(wave):
                real_part = coordinates[cursor]
                imaginary_part = coordinates[cursor + 1]
                coefficient = (
                    (real_part + 1j * imaginary_part)
                    * polarization
                    / math.sqrt(2.0)
                )
                result[self.index(wave)] += coefficient
                result[self.index((-wave[0], -wave[1]))] += np.conjugate(coefficient)
                cursor += 2
        return result

    def target_coordinates(self, coefficients: np.ndarray) -> np.ndarray:
        coordinates: list[float] = []
        for wave in self.representatives:
            coefficient = coefficients[self.index(wave)]
            for polarization in self.polarizations(wave):
                scalar = np.vdot(polarization, coefficient) * math.sqrt(2.0)
                coordinates.extend((float(scalar.real), float(scalar.imag)))
        return np.asarray(coordinates)

    def curl(self, coefficients: np.ndarray) -> np.ndarray:
        return 1j * np.cross(self.waves, coefficients)

    def nonlinear(self, coefficients: np.ndarray) -> np.ndarray:
        normalization = self.grid_order**2
        velocity = np.fft.ifft2(
            coefficients * normalization, axes=(0, 1)
        )
        vorticity_hat = self.curl(coefficients)
        vorticity = np.fft.ifft2(
            vorticity_hat * normalization, axes=(0, 1)
        )
        lamb = np.cross(velocity, vorticity)
        lamb_hat = np.fft.fft2(lamb, axes=(0, 1)) / normalization
        return self.truncate(lamb_hat)

    def rhs(self, _time: float, flattened: np.ndarray) -> np.ndarray:
        self._rhs_calls += 1
        coefficients = flattened.reshape(self.grid_order, self.grid_order, 3)
        derivative = (
            -self.viscosity * self.wave_squared[..., None] * coefficients
            + self.nonlinear(coefficients)
        )
        derivative[~self.retained] = 0.0
        return derivative.ravel()

    def integrate(
        self,
        initial: np.ndarray,
        final_time: float,
        evaluation_times: np.ndarray | None = None,
    ) -> tuple[np.ndarray, int]:
        before = self._rhs_calls
        solution = solve_ivp(
            self.rhs,
            (0.0, final_time),
            initial.ravel(),
            method="DOP853",
            t_eval=evaluation_times,
            rtol=self.rtol,
            atol=self.atol,
            max_step=max(final_time / 8.0, 1e-5),
        )
        if not solution.success:
            raise RuntimeError(solution.message)
        states = solution.y.T.reshape(
            -1, self.grid_order, self.grid_order, 3
        )
        return states, self._rhs_calls - before

    def shoot(self, tau: float, seed: np.ndarray) -> SolveRecord:
        forcing_zero = self.nonlinear(seed)
        initial_guess = -tau * self.target_coordinates(forcing_zero)
        root_calls = 0
        integration_calls = 0
        function_evaluations = 0
        last_endpoint: np.ndarray | None = None

        def residual(coordinates: np.ndarray) -> np.ndarray:
            nonlocal root_calls, integration_calls, function_evaluations, last_endpoint
            root_calls += 1
            initial = seed + self.from_target_coordinates(coordinates)
            states, evaluations = self.integrate(initial, tau)
            integration_calls += 1
            function_evaluations += evaluations
            last_endpoint = states[-1]
            return self.target_coordinates(last_endpoint)

        solution = root(
            residual,
            initial_guess,
            method="hybr",
            options={"xtol": 2e-11, "maxfev": 120},
        )
        final_residual = residual(solution.x)
        if not solution.success and np.linalg.norm(final_residual) > 2e-9:
            raise RuntimeError(f"shooting failed at tau={tau}: {solution.message}")
        residual_norm = float(np.linalg.norm(final_residual))
        if residual_norm > 2e-9:
            raise AssertionError(f"target residual too large at tau={tau}: {residual_norm}")
        assert last_endpoint is not None
        initial = seed + self.from_target_coordinates(solution.x)
        return SolveRecord(
            tau=tau,
            correction=solution.x.copy(),
            endpoint=final_residual,
            event_state=last_endpoint.copy(),
            root_calls=root_calls,
            root_residual=residual_norm,
            integration_calls=integration_calls,
            function_evaluations=function_evaluations,
        )


def reality_residual(coefficients: np.ndarray, model: PseudoSpectralGalerkin) -> float:
    residual = 0.0
    for first in range(-model.cutoff, model.cutoff + 1):
        for second in range(-model.cutoff, model.cutoff + 1):
            if first == second == 0:
                continue
            left = coefficients[model.index((first, second))]
            right = coefficients[model.index((-first, -second))]
            residual = max(residual, float(np.max(np.abs(right - np.conjugate(left)))))
    return residual


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--progress", type=Path, required=True)
    parser.add_argument("--resource-log", type=Path, required=True)
    parser.add_argument("--grid-order", type=int, default=10)
    parser.add_argument("--cutoff", type=int, default=2)
    parser.add_argument("--viscosity", type=float, default=1.0)
    parser.add_argument("--rtol", type=float, default=2e-11)
    parser.add_argument("--atol", type=float, default=2e-13)
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.progress.write_text("", encoding="utf-8")
    args.resource_log.write_text("", encoding="utf-8")
    append_resource(args.resource_log, "producer-start")
    started = perf_counter()
    model = PseudoSpectralGalerkin(
        args.grid_order,
        args.cutoff,
        args.viscosity,
        args.rtol,
        args.atol,
    )
    seed = model.seed()
    forcing_zero = model.nonlinear(seed)
    forcing_zero_coordinates = model.target_coordinates(forcing_zero)
    forcing_zero_norm = float(np.linalg.norm(forcing_zero_coordinates))
    seed_enstrophy = vector_norm_squared(model.curl(seed))
    append_progress(
        args.progress,
        "producer-start",
        gridOrder=args.grid_order,
        cutoff=args.cutoff,
        viscosity=args.viscosity,
        tauCount=len(TAUS),
        retainedModeCount=int(np.count_nonzero(model.retained)),
    )

    records: list[dict[str, object]] = []
    selected_record: SolveRecord | None = None
    for position, tau in enumerate(TAUS, start=1):
        lap_started = perf_counter()
        append_progress(
            args.progress,
            "shoot-start",
            tau=tau,
            completed=position - 1,
            total=len(TAUS),
        )
        record = model.shoot(tau, seed)
        if math.isclose(tau, 0.04):
            selected_record = record
        correction_norm = float(np.linalg.norm(record.correction))
        precompensation_ratio = correction_norm / (tau * forcing_zero_norm)
        event_forcing = model.nonlinear(record.event_state)
        event_forcing_coordinates = model.target_coordinates(event_forcing)
        event_forcing_norm_squared = float(
            np.dot(event_forcing_coordinates, event_forcing_coordinates)
        )
        event_enstrophy = vector_norm_squared(model.curl(record.event_state))
        a_plus = event_forcing_norm_squared / event_enstrophy
        event_c_slope_squared = 4.0 * event_forcing_norm_squared
        slope_charge = event_c_slope_squared / (4.0 * event_enstrophy)
        row = {
            "tau": tau,
            "correctionCoordinates": record.correction.tolist(),
            "correctionNorm": correction_norm,
            "leadingCorrectionNorm": tau * forcing_zero_norm,
            "precompensationRatio": precompensation_ratio,
            "targetResidual": record.root_residual,
            "rootCalls": record.root_calls,
            "integrationCalls": record.integration_calls,
            "rhsEvaluations": record.function_evaluations,
            "eventEnstrophy": event_enstrophy,
            "eventForcingNormSquared": event_forcing_norm_squared,
            "APlus": a_plus,
            "slopeCharge": slope_charge,
            "slopeIdentityResidual": abs(a_plus - slope_charge),
            "realityResidual": reality_residual(record.event_state, model),
            "wallSeconds": perf_counter() - lap_started,
        }
        records.append(row)
        elapsed = perf_counter() - started
        eta = elapsed / position * (len(TAUS) - position)
        append_progress(
            args.progress,
            "shoot-complete",
            tau=tau,
            targetResidual=record.root_residual,
            rootCalls=record.root_calls,
            APlus=a_plus,
            elapsedSeconds=elapsed,
            etaSeconds=eta,
            completed=position,
            total=len(TAUS),
        )

    if selected_record is None:
        raise AssertionError("selected tau=0.04 record is missing")
    selected_tau = selected_record.tau
    sample_times = np.linspace(0.0, 2.0 * selected_tau, 161)
    selected_initial = seed + model.from_target_coordinates(
        selected_record.correction
    )
    trajectory_states, trajectory_evaluations = model.integrate(
        selected_initial,
        2.0 * selected_tau,
        sample_times,
    )
    event_index = int(np.argmin(np.abs(sample_times - selected_tau)))
    event_state = trajectory_states[event_index]
    event_direction = model.target_coordinates(model.nonlinear(event_state))
    event_direction /= np.linalg.norm(event_direction)
    normalization = selected_tau * forcing_zero_norm
    trajectory = []
    for time, state in zip(sample_times, trajectory_states):
        coordinates = model.target_coordinates(state)
        principal = float(np.dot(coordinates, event_direction))
        transverse = float(np.linalg.norm(coordinates - principal * event_direction))
        trajectory.append({
            "time": float(time),
            "timeOverTau": float(time / selected_tau),
            "principalCoefficient": principal,
            "transverseNorm": transverse,
            "principalNormalized": principal / normalization,
            "transverseNormalized": transverse / normalization,
        })
    trajectory_event_residual = float(
        np.linalg.norm(model.target_coordinates(event_state))
    )
    append_progress(
        args.progress,
        "trajectory-complete",
        tau=selected_tau,
        samples=len(trajectory),
        eventResidual=trajectory_event_residual,
        rhsEvaluations=trajectory_evaluations,
    )

    payload = {
        "release": "R0.71T",
        "status": "passed",
        "method": "dealiased pseudo-spectral evaluation of a finite Fourier--Galerkin ODE",
        "model": {
            "periodicDomain": "(R/2piZ)^3",
            "invariantSector": "x3-independent three-component velocity",
            "gridOrder": args.grid_order,
            "cutoff": args.cutoff,
            "retainedModeSet": "k3=0, max(|k1|,|k2|)<=Kcut, k!=0",
            "retainedModeCount": int(np.count_nonzero(model.retained)),
            "target": "k3=0 and |k|^2=2",
            "targetRealDimension": 8,
            "viscosity": args.viscosity,
            "finiteGalerkin": True,
            "pdeTimeStepping": True,
            "dns": False,
        },
        "solver": {
            "integrator": "SciPy solve_ivp DOP853",
            "rootSolver": "SciPy hybr",
            "relativeTolerance": args.rtol,
            "absoluteTolerance": args.atol,
            "rootTolerance": 2e-11,
            "maximumStep": "final_time/8",
            "precision": "IEEE binary64 complex Fourier coefficients",
        },
        "seed": {
            "velocity": "u_*(x)=(0,cos(x_1),cos(x_2))",
            "enstrophy": seed_enstrophy,
            "targetForcingCoordinates": forcing_zero_coordinates.tolist(),
            "targetForcingNorm": forcing_zero_norm,
            "targetForcingNormSquared": forcing_zero_norm**2,
        },
        "tauRuns": records,
        "trajectory": {
            "tau": selected_tau,
            "normalization": "tau*||P_*F(u_*)||_2",
            "eventDirection": event_direction.tolist(),
            "eventTargetResidual": trajectory_event_residual,
            "samples": trajectory,
        },
        "wallSeconds": perf_counter() - started,
        "claimBoundary": (
            "Finite Fourier--Galerkin corroboration in an invariant sector. "
            "It is not DNS, a continuum error estimate, or a replacement for "
            "the local NSE flow-map implicit-function theorem."
        ),
    }
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    append_progress(
        args.progress,
        "producer-complete",
        status="passed",
        wallSeconds=payload["wallSeconds"],
        maximumTargetResidual=max(row["targetResidual"] for row in records),
    )
    append_resource(args.resource_log, "producer-complete")


if __name__ == "__main__":
    main()
