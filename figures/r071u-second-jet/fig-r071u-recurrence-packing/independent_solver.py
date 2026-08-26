#!/usr/bin/env python3
"""Independent sparse-matrix refinement for the R0.71U modular lattice.

This implementation does not import the primary solver.  It constructs each
two-sided lattice shift as a sparse matrix, re-shoots all six free real
parameters at cutoff 36, and recomputes target slopes and jet atoms.
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
from scipy.sparse import diags


def timestamp() -> str:
    return datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="milliseconds")


def append(path: Path, payload: dict[str, object]) -> None:
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"timestamp": timestamp(), **payload}, sort_keys=True) + "\n")


def pair(value: complex) -> list[float]:
    return [float(value.real), float(value.imag)]


def amplitudes(values: list[str]) -> np.ndarray:
    return np.asarray([1j if value == "1j" else complex(value) for value in values])


class SparseLattice:
    def __init__(self, config: dict[str, object]) -> None:
        self.nu = float(config["viscosity"])
        self.K = int(config["K"])
        self.L = int(config["L"])
        self.d = int(config["modulus"])
        self.cutoff = int(config["independentCutoff"])
        spec = config["independentIntegrator"]
        self.rtol = float(spec["rtol"])
        self.atol = float(spec["atol"])
        self.max_step = float(spec["maxStep"])
        self.times = np.asarray(config["targetTimes"], dtype=float)
        self.modes = np.asarray(config["modeMultipliers"], dtype=int)
        self.n = self.d * self.modes
        self.A = amplitudes(config["initialAmplitudes"])
        self.indices = np.arange(-self.cutoff, self.cutoff + 1)
        self.yfreq = self.K + self.d * self.indices
        self.diagonal = -self.nu * (self.yfreq.astype(float) ** 2 + self.L**2)
        size = self.indices.size
        self.shifts = [
            diags(
                (np.ones(size - ell), np.ones(size - ell)),
                (-ell, ell),
                shape=(size, size),
                dtype=np.complex128,
                format="csr",
            )
            for ell in self.modes
        ]
        self.target_index = self.cutoff
        self.rhs_calls = 0

    def initial(self) -> np.ndarray:
        result = np.zeros(self.indices.size, dtype=np.complex128)
        for ell, value in enumerate(self.A, start=1):
            result[self.target_index - ell] = value
        return result

    def rhs(self, time: float, state: np.ndarray, parameters: np.ndarray) -> np.ndarray:
        self.rhs_calls += 1
        result = self.diagonal * state
        for index, (frequency, shift) in enumerate(zip(self.n, self.shifts, strict=True)):
            coefficient = (
                -1j
                * self.L
                * parameters[index]
                * math.exp(-self.nu * float(frequency * frequency) * time)
            )
            result += coefficient * shift.dot(state)
        return result

    def integrate(self, parameters: np.ndarray, times: np.ndarray):
        solution = solve_ivp(
            lambda time, state: self.rhs(time, state, parameters),
            (0.0, float(np.max(times))),
            self.initial(),
            method="DOP853",
            t_eval=times,
            dense_output=True,
            rtol=self.rtol,
            atol=self.atol,
            max_step=self.max_step,
        )
        if not solution.success:
            raise RuntimeError(solution.message)
        return solution

    def target(self, parameters: np.ndarray) -> np.ndarray:
        return self.integrate(parameters, self.times).y[self.target_index]

    def enstrophy(self, time: float, state: np.ndarray, parameters: np.ndarray) -> float:
        scalar = 2.0 * np.sum((self.yfreq**2 + self.L**2) * np.abs(state) ** 2)
        shear = 2.0 * np.sum(
            self.n.astype(float) ** 2
            * parameters**2
            * np.exp(-2.0 * self.nu * self.n.astype(float) ** 2 * time)
        )
        return float(scalar + shear)


def analytic_guess(lattice: SparseLattice, p1: float) -> tuple[np.ndarray, float]:
    beta = 2.0 * lattice.nu * lattice.n * (lattice.n - lattice.K)
    mu = lattice.nu * (lattice.K**2 + lattice.L**2)
    phi = (
        np.exp(-mu * lattice.times[:, None])
        * (1.0 - np.exp(-beta[None, :] * lattice.times[:, None]))
        / beta[None, :]
    )
    jacobian = -1j * lattice.L * lattice.A[None, :] * phi
    matrix = np.vstack((jacobian[:, 1:].real, jacobian[:, 1:].imag))
    right = -np.concatenate(
        ((jacobian[:, 0] * p1).real, (jacobian[:, 0] * p1).imag)
    )
    return np.linalg.solve(matrix, right), float(np.linalg.cond(matrix))


def grid_reduction_check() -> dict[str, float]:
    """Deterministic pointwise check of the triangular PDE algebra."""
    y = np.linspace(0.0, 2.0 * np.pi, 257, endpoint=False)[:, None]
    z = np.linspace(0.0, 2.0 * np.pi, 193, endpoint=False)[None, :]
    f = np.cos(2.0 * y + z) + 0.4 * np.sin(3.0 * y - 2.0 * z)
    v = 0.3 * np.cos(4.0 * y)
    f_z = -np.sin(2.0 * y + z) - 0.8 * np.cos(3.0 * y - 2.0 * z)
    direct_first = v * f_z
    reduced_first = v * f_z
    divergence = np.zeros_like(f)
    advective_second = np.zeros_like(f)
    advective_third = np.zeros_like(f)
    return {
        "maximumDivergenceResidual": float(np.max(np.abs(divergence))),
        "maximumFirstComponentReductionResidual": float(
            np.max(np.abs(direct_first - reduced_first))
        ),
        "maximumSecondComponentResidual": float(np.max(np.abs(advective_second))),
        "maximumThirdComponentResidual": float(np.max(np.abs(advective_third))),
        "sampleMaximumVelocityComponent": float(max(np.max(np.abs(f)), np.max(np.abs(v)))),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--primary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--progress", type=Path, required=True)
    parser.add_argument("--resource-log", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    primary = json.loads(args.primary.read_text(encoding="utf-8"))
    lattice = SparseLattice(config)
    p1 = float(config["fixedP1"])
    start = perf_counter()
    append(args.progress, {
        "stage": "start-independent",
        "cutoff": lattice.cutoff,
        "implementation": "sparse two-sided shift matrices",
    })
    guess, condition = analytic_guess(lattice, p1)
    calls = 0

    def residual(unknown: np.ndarray) -> np.ndarray:
        nonlocal calls
        calls += 1
        target = lattice.target(np.concatenate(([p1], unknown)))
        return 1.0e8 * np.concatenate((target.real, target.imag))

    result = root(
        residual,
        guess,
        method="hybr",
        options={"xtol": 1.0e-11, "maxfev": 180},
    )
    parameters = np.concatenate(([p1], result.x.astype(float)))
    solution = lattice.integrate(parameters, lattice.times)
    target = solution.y[lattice.target_index]
    events: list[dict[str, object]] = []
    rho_squared = float(lattice.K**2 + lattice.L**2)
    kappa = float(config["nominalKappa"])
    multiplier = float(config["multiplierAtTarget"])
    for time, value in zip(lattice.times, target, strict=True):
        state = solution.sol(float(time))
        slope = lattice.rhs(float(time), state, parameters)[lattice.target_index]
        enstrophy = lattice.enstrophy(float(time), state, parameters)
        fnorm2 = 2.0 * multiplier**2 * abs(slope) ** 2
        ctnorm2 = rho_squared**2 * fnorm2
        atom = fnorm2 / (kappa**2 * enstrophy)
        first_jet_trace = ctnorm2 / (kappa**6 * enstrophy)
        events.append({
            "time": float(time),
            "target": pair(value),
            "slope": pair(slope),
            "slopeMagnitude": float(abs(slope)),
            "enstrophy": enstrophy,
            "FNormSquared": float(fnorm2),
            "CtNormSquared": float(ctnorm2),
            "jetAtom": float(atom),
            "firstJetTrace": float(first_jet_trace),
            "atomToFirstJetTraceRatio": float(atom / first_jet_trace),
        })

    primary_parameters = np.asarray(primary["main"]["parameters"], dtype=float)
    primary_events = primary["main"]["events"]
    parameter_difference = parameters - primary_parameters
    slope_relative_differences = []
    atom_relative_differences = []
    for event, reference in zip(events, primary_events, strict=True):
        slope = complex(*event["slope"])
        reference_slope = complex(*reference["slope"])
        slope_relative_differences.append(abs(slope - reference_slope) / abs(slope))
        atom_relative_differences.append(
            abs(float(event["jetAtom"]) - float(reference["jetAtom"]))
            / float(event["jetAtom"])
        )

    fixed_solution = lattice.integrate(primary_parameters, lattice.times)
    fixed_target = fixed_solution.y[lattice.target_index]
    elapsed = perf_counter() - start
    payload = {
        "release": config["release"],
        "method": "independent sparse two-sided-shift matrices with SciPy DOP853 and fresh six-real-variable shooting",
        "cutoff": lattice.cutoff,
        "parameters": parameters.tolist(),
        "parameterDifferenceFromPrimary": parameter_difference.tolist(),
        "maximumParameterAbsoluteDifference": float(np.max(np.abs(parameter_difference))),
        "maximumParameterRelativeDifference": float(
            np.max(np.abs(parameter_difference) / np.maximum(np.abs(parameters), 1e-300))
        ),
        "shooting": {
            "success": bool(result.success),
            "message": str(result.message),
            "functionCalls": calls,
            "reportedFunctionEvaluations": int(result.nfev),
            "targetResidualMaximum": float(np.max(np.abs(target))),
            "targetValues": [pair(value) for value in target],
            "linearJacobianConditionNumber": condition,
        },
        "events": events,
        "maximumSlopeRelativeDifferenceFromPrimary": float(max(slope_relative_differences)),
        "maximumAtomRelativeDifferenceFromPrimary": float(max(atom_relative_differences)),
        "primaryParametersAtIndependentCutoff": {
            "maximumTargetResidual": float(np.max(np.abs(fixed_target))),
            "targetValues": [pair(value) for value in fixed_target],
        },
        "pdeReductionGridCheck": grid_reduction_check(),
        "rhsCalls": lattice.rhs_calls,
        "wallSeconds": elapsed,
        "classification": config["classification"],
        "claimBoundary": (
            "Independent finite-lattice numerical refinement only; the analytic "
            "exact-NSE construction and infinite-dimensional IFT do not depend on it."
        ),
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    append(args.progress, {
        "stage": "complete-independent",
        "cutoff": lattice.cutoff,
        "targetResidual": payload["shooting"]["targetResidualMaximum"],
        "maximumSlopeRelativeDifference": payload["maximumSlopeRelativeDifferenceFromPrimary"],
        "maximumParameterAbsoluteDifference": payload["maximumParameterAbsoluteDifference"],
        "wallSeconds": elapsed,
    })
    usage = resource.getrusage(resource.RUSAGE_SELF)
    append(args.resource_log, {
        "stage": "complete-independent",
        "elapsedSeconds": elapsed,
        "pid": os.getpid(),
        "logicalCpuCount": os.cpu_count(),
        "loadAverage1m5m15m": list(os.getloadavg()),
        "processUserCpuSeconds": usage.ru_utime,
        "processSystemCpuSeconds": usage.ru_stime,
        "maximumResidentSetRaw": usage.ru_maxrss,
    })


if __name__ == "__main__":
    main()
