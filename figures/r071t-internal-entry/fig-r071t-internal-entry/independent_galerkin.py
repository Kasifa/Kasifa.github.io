#!/usr/bin/env python3
"""Independent direct-convolution Galerkin audit for R0.71T.

This implementation shares no solver code with ``galerkin_shoot.py``.  It
stores retained Fourier modes in a flat dictionary ordering and evaluates the
quadratic term by direct convolution rather than FFT multiplication.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import math
import os
from pathlib import Path
import resource
from time import perf_counter
from zoneinfo import ZoneInfo

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root


def timestamp() -> str:
    return datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="milliseconds")


def append_progress(path: Path, event: str, **payload: object) -> None:
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({
            "timestamp": timestamp(),
            "event": event,
            **payload,
        }, sort_keys=True) + "\n")


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


class DirectConvolutionGalerkin:
    representatives = ((1, 1), (1, -1))

    def __init__(self, cutoff: int, viscosity: float, rtol: float, atol: float) -> None:
        self.cutoff = cutoff
        self.viscosity = viscosity
        self.rtol = rtol
        self.atol = atol
        self.modes = [
            (first, second)
            for first in range(-cutoff, cutoff + 1)
            for second in range(-cutoff, cutoff + 1)
            if (first, second) != (0, 0)
        ]
        self.lookup = {mode: index for index, mode in enumerate(self.modes)}
        self.waves = np.asarray([
            [float(first), float(second), 0.0]
            for first, second in self.modes
        ])
        self.wave_squared = np.sum(self.waves**2, axis=1)
        identity = np.eye(3)
        self.projectors = np.asarray([
            identity - np.outer(wave, wave) / squared
            for wave, squared in zip(self.waves, self.wave_squared)
        ])
        out_indices: list[int] = []
        left_indices: list[int] = []
        right_indices: list[int] = []
        right_waves: list[np.ndarray] = []
        for left_index, left in enumerate(self.modes):
            for right_index, right in enumerate(self.modes):
                output = (left[0] + right[0], left[1] + right[1])
                output_index = self.lookup.get(output)
                if output_index is None:
                    continue
                out_indices.append(output_index)
                left_indices.append(left_index)
                right_indices.append(right_index)
                right_waves.append(self.waves[right_index])
        self.out_indices = np.asarray(out_indices, dtype=np.int64)
        self.left_indices = np.asarray(left_indices, dtype=np.int64)
        self.right_indices = np.asarray(right_indices, dtype=np.int64)
        self.right_waves = np.asarray(right_waves)
        self.rhs_calls = 0

    def seed(self) -> np.ndarray:
        state = np.zeros((len(self.modes), 3), dtype=np.complex128)
        for wave in ((1, 0), (-1, 0)):
            state[self.lookup[wave]] = (0.0, 0.5, 0.0)
        for wave in ((0, 1), (0, -1)):
            state[self.lookup[wave]] = (0.0, 0.0, 0.5)
        return state

    @staticmethod
    def polarizations(wave: tuple[int, int]) -> tuple[np.ndarray, np.ndarray]:
        length = math.hypot(*wave)
        return (
            np.asarray([-wave[1] / length, wave[0] / length, 0.0]),
            np.asarray([0.0, 0.0, 1.0]),
        )

    def from_target_coordinates(self, coordinates: np.ndarray) -> np.ndarray:
        state = np.zeros((len(self.modes), 3), dtype=np.complex128)
        cursor = 0
        for wave in self.representatives:
            for polarization in self.polarizations(wave):
                coefficient = (
                    (coordinates[cursor] + 1j * coordinates[cursor + 1])
                    * polarization
                    / math.sqrt(2.0)
                )
                state[self.lookup[wave]] += coefficient
                negative = (-wave[0], -wave[1])
                state[self.lookup[negative]] += np.conjugate(coefficient)
                cursor += 2
        return state

    def target_coordinates(self, state: np.ndarray) -> np.ndarray:
        values: list[float] = []
        for wave in self.representatives:
            coefficient = state[self.lookup[wave]]
            for polarization in self.polarizations(wave):
                scalar = math.sqrt(2.0) * np.vdot(polarization, coefficient)
                values.extend((float(scalar.real), float(scalar.imag)))
        return np.asarray(values)

    def project(self, state: np.ndarray) -> np.ndarray:
        return np.einsum("nij,nj->ni", self.projectors, state)

    def nonlinear(self, state: np.ndarray) -> np.ndarray:
        dot_products = np.einsum(
            "ij,ij->i", state[self.left_indices], self.right_waves
        )
        contributions = (
            -1j
            * dot_products[:, None]
            * state[self.right_indices]
        )
        raw = np.zeros_like(state)
        np.add.at(raw, self.out_indices, contributions)
        return self.project(raw)

    def curl(self, state: np.ndarray) -> np.ndarray:
        return 1j * np.cross(self.waves, state)

    def rhs(self, _time: float, flat: np.ndarray) -> np.ndarray:
        self.rhs_calls += 1
        state = flat.reshape(-1, 3)
        return (
            -self.viscosity * self.wave_squared[:, None] * state
            + self.nonlinear(state)
        ).ravel()

    def integrate(self, initial: np.ndarray, final_time: float) -> np.ndarray:
        solution = solve_ivp(
            self.rhs,
            (0.0, final_time),
            initial.ravel(),
            method="DOP853",
            rtol=self.rtol,
            atol=self.atol,
            max_step=max(final_time / 11.0, 1e-5),
        )
        if not solution.success:
            raise RuntimeError(solution.message)
        return solution.y[:, -1].reshape(-1, 3)

    def shoot(self, tau: float) -> dict[str, object]:
        seed = self.seed()
        f0 = self.nonlinear(seed)
        f0_coordinates = self.target_coordinates(f0)
        initial_guess = -tau * f0_coordinates
        calls = 0

        def residual(coordinates: np.ndarray) -> np.ndarray:
            nonlocal calls
            calls += 1
            endpoint = self.integrate(
                seed + self.from_target_coordinates(coordinates), tau
            )
            return self.target_coordinates(endpoint)

        solved = root(
            residual,
            initial_guess,
            method="hybr",
            options={"xtol": 1e-11, "maxfev": 140},
        )
        endpoint = self.integrate(
            seed + self.from_target_coordinates(solved.x), tau
        )
        endpoint_residual = float(np.linalg.norm(self.target_coordinates(endpoint)))
        if (not solved.success) and endpoint_residual > 2e-9:
            raise RuntimeError(solved.message)
        if endpoint_residual > 2e-9:
            raise AssertionError(endpoint_residual)
        event_forcing_coordinates = self.target_coordinates(
            self.nonlinear(endpoint)
        )
        forcing_norm_squared = float(np.dot(
            event_forcing_coordinates, event_forcing_coordinates
        ))
        enstrophy = float(np.vdot(
            self.curl(endpoint).ravel(), self.curl(endpoint).ravel()
        ).real)
        correction_norm = float(np.linalg.norm(solved.x))
        f0_norm = float(np.linalg.norm(f0_coordinates))
        a_plus = forcing_norm_squared / enstrophy
        return {
            "tau": tau,
            "cutoff": self.cutoff,
            "retainedModeCount": len(self.modes),
            "interactionCount": len(self.out_indices),
            "correctionCoordinates": solved.x.tolist(),
            "correctionNorm": correction_norm,
            "precompensationRatio": correction_norm / (tau * f0_norm),
            "targetResidual": endpoint_residual,
            "rootCalls": calls,
            "rhsEvaluations": self.rhs_calls,
            "eventEnstrophy": enstrophy,
            "eventForcingNormSquared": forcing_norm_squared,
            "APlus": a_plus,
            "slopeCharge": (4.0 * forcing_norm_squared) / (4.0 * enstrophy),
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--producer", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--progress", type=Path, required=True)
    parser.add_argument("--resource-log", type=Path, required=True)
    parser.add_argument("--viscosity", type=float, default=1.0)
    parser.add_argument("--rtol", type=float, default=8e-12)
    parser.add_argument("--atol", type=float, default=8e-14)
    args = parser.parse_args()
    started = perf_counter()
    producer = json.loads(args.producer.read_text(encoding="utf-8"))
    append_resource(args.resource_log, "independent-start")
    producer_row = next(
        row for row in producer["tauRuns"]
        if math.isclose(float(row["tau"]), 0.04)
    )
    append_progress(
        args.progress,
        "independent-start",
        method="direct Fourier convolution",
        configurations=["N=10,Kcut=2", "N=12,Kcut=3"],
    )
    runs = []
    for grid_order, cutoff in ((10, 2), (12, 3)):
        model = DirectConvolutionGalerkin(
            cutoff, args.viscosity, args.rtol, args.atol
        )
        lap_started = perf_counter()
        row = model.shoot(0.04)
        row["gridOrder"] = grid_order
        row["wallSeconds"] = perf_counter() - lap_started
        runs.append(row)
        append_progress(
            args.progress,
            "independent-configuration-complete",
            gridOrder=grid_order,
            cutoff=cutoff,
            targetResidual=row["targetResidual"],
            APlus=row["APlus"],
            wallSeconds=row["wallSeconds"],
        )
    same = runs[0]
    refined = runs[1]
    comparisons = {
        "sameTruncationPrecompensationDifference": abs(
            same["precompensationRatio"] - producer_row["precompensationRatio"]
        ),
        "sameTruncationAPlusDifference": abs(
            same["APlus"] - producer_row["APlus"]
        ),
        "refinedVsPrimaryPrecompensationDifference": abs(
            refined["precompensationRatio"] - producer_row["precompensationRatio"]
        ),
        "refinedVsPrimaryAPlusDifference": abs(
            refined["APlus"] - producer_row["APlus"]
        ),
    }
    if comparisons["sameTruncationPrecompensationDifference"] > 2e-9:
        raise AssertionError(comparisons)
    if comparisons["sameTruncationAPlusDifference"] > 2e-9:
        raise AssertionError(comparisons)
    if comparisons["refinedVsPrimaryPrecompensationDifference"] > 2e-4:
        raise AssertionError(comparisons)
    if comparisons["refinedVsPrimaryAPlusDifference"] > 2e-4:
        raise AssertionError(comparisons)
    payload = {
        "release": "R0.71T",
        "status": "passed",
        "method": "standalone retained-mode direct Fourier convolution",
        "finiteGalerkin": True,
        "pdeTimeStepping": True,
        "dns": False,
        "solver": {
            "integrator": "SciPy solve_ivp DOP853",
            "rootSolver": "SciPy hybr",
            "relativeTolerance": args.rtol,
            "absoluteTolerance": args.atol,
            "maximumStep": "final_time/11",
        },
        "runs": runs,
        "comparisons": comparisons,
        "wallSeconds": perf_counter() - started,
        "claimBoundary": (
            "Independent finite-dimensional corroboration only; no continuum "
            "truncation error, DNS resolution, or regularity conclusion."
        ),
    }
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    append_progress(
        args.progress,
        "independent-complete",
        status="passed",
        wallSeconds=payload["wallSeconds"],
        comparisons=comparisons,
    )
    append_resource(args.resource_log, "independent-complete")


if __name__ == "__main__":
    main()
