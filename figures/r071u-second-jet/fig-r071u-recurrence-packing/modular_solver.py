#!/usr/bin/env python3
"""Primary finite-lattice corroboration for the R0.71U recurrence family.

The exact invariant NSE subclass is u=(f,0,v), with

    v_t = nu v_yy,
    f_t + v f_z = nu(f_yy + f_zz).

At fixed z-frequency L, the modular y-frequency lattice k_m=K+d*m obeys

    a_m' = -nu[(K+d*m)^2+L^2] a_m
           - i L sum_l p_l exp(-nu(d*l)^2 t)(a_{m-l}+a_{m+l}).

This script truncates the lattice, uses DOP853, and shoots six real
parameters.  It is finite-Galerkin numerical corroboration, not DNS and not
an error-controlled proof of the infinite lattice or the analytic IFT.
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
from zoneinfo import ZoneInfo

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root


def timestamp() -> str:
    return datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="milliseconds")


def append_ndjson(path: Path, payload: dict[str, object]) -> None:
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"timestamp": timestamp(), **payload}, sort_keys=True) + "\n")


def append_resource(path: Path, stage: str, elapsed: float) -> None:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    append_ndjson(path, {
        "stage": stage,
        "elapsedSeconds": elapsed,
        "pid": os.getpid(),
        "logicalCpuCount": os.cpu_count(),
        "loadAverage1m5m15m": list(os.getloadavg()),
        "processUserCpuSeconds": usage.ru_utime,
        "processSystemCpuSeconds": usage.ru_stime,
        "maximumResidentSetRaw": usage.ru_maxrss,
    })


def complex_pair(value: complex) -> list[float]:
    return [float(value.real), float(value.imag)]


@dataclass(frozen=True)
class Problem:
    nu: float
    K: int
    L: int
    d: int
    target_times: np.ndarray
    amplitudes: np.ndarray
    mode_multipliers: np.ndarray
    kappa: float
    multiplier: float

    @property
    def shear_frequencies(self) -> np.ndarray:
        return self.d * self.mode_multipliers

    @property
    def rho_squared(self) -> float:
        return float(self.K * self.K + self.L * self.L)


class ModularLattice:
    """Vectorized primary implementation of the truncated modular lattice."""

    def __init__(
        self,
        problem: Problem,
        cutoff: int,
        rtol: float,
        atol: float,
        max_step: float,
    ) -> None:
        self.problem = problem
        self.cutoff = cutoff
        self.indices = np.arange(-cutoff, cutoff + 1, dtype=int)
        self.y_frequencies = problem.K + problem.d * self.indices
        self.decay = problem.nu * (
            self.y_frequencies.astype(float) ** 2 + problem.L**2
        )
        self.target_index = cutoff
        self.rtol = rtol
        self.atol = atol
        self.max_step = max_step
        self.rhs_calls = 0

    def initial_state(self) -> np.ndarray:
        state = np.zeros(2 * self.cutoff + 1, dtype=np.complex128)
        for ell, amplitude in enumerate(self.problem.amplitudes, start=1):
            if ell > self.cutoff:
                raise ValueError("cutoff does not contain every initial mode")
            state[self.target_index - ell] = amplitude
        return state

    def rhs(self, time: float, state: np.ndarray, parameters: np.ndarray) -> np.ndarray:
        self.rhs_calls += 1
        derivative = -self.decay * state
        for ell, shear_frequency in enumerate(
            self.problem.shear_frequencies, start=1
        ):
            coefficient = (
                -1j
                * self.problem.L
                * parameters[ell - 1]
                * math.exp(-self.problem.nu * shear_frequency**2 * time)
            )
            derivative[ell:] += coefficient * state[:-ell]
            derivative[:-ell] += coefficient * state[ell:]
        return derivative

    def integrate(
        self,
        parameters: np.ndarray,
        evaluation_times: np.ndarray,
        *,
        dense_output: bool = False,
    ):
        final_time = float(np.max(evaluation_times))
        solution = solve_ivp(
            lambda time, state: self.rhs(time, state, parameters),
            (0.0, final_time),
            self.initial_state(),
            method="DOP853",
            t_eval=evaluation_times,
            dense_output=dense_output,
            rtol=self.rtol,
            atol=self.atol,
            max_step=self.max_step,
        )
        if not solution.success:
            raise RuntimeError(solution.message)
        return solution

    def target_values(self, parameters: np.ndarray) -> np.ndarray:
        solution = self.integrate(parameters, self.problem.target_times)
        return solution.y[self.target_index]

    def enstrophy(self, time: float, state: np.ndarray, parameters: np.ndarray) -> float:
        scalar = 2.0 * np.sum(
            (self.y_frequencies.astype(float) ** 2 + self.problem.L**2)
            * np.abs(state) ** 2
        )
        shear_frequencies = self.problem.shear_frequencies.astype(float)
        shear = 2.0 * np.sum(
            shear_frequencies**2
            * parameters**2
            * np.exp(-2.0 * self.problem.nu * shear_frequencies**2 * time)
        )
        return float(scalar + shear)


def parse_amplitudes(values: list[str]) -> np.ndarray:
    parsed: list[complex] = []
    for value in values:
        if value == "1j":
            parsed.append(1j)
        elif value == "1":
            parsed.append(1.0 + 0j)
        else:
            parsed.append(complex(value))
    return np.asarray(parsed, dtype=np.complex128)


def load_problem(config: dict[str, object]) -> Problem:
    return Problem(
        nu=float(config["viscosity"]),
        K=int(config["K"]),
        L=int(config["L"]),
        d=int(config["modulus"]),
        target_times=np.asarray(config["targetTimes"], dtype=float),
        amplitudes=parse_amplitudes(config["initialAmplitudes"]),
        mode_multipliers=np.asarray(config["modeMultipliers"], dtype=int),
        kappa=float(config["nominalKappa"]),
        multiplier=float(config["multiplierAtTarget"]),
    )


def linear_guess(problem: Problem, p1: float) -> tuple[np.ndarray, dict[str, object]]:
    n = problem.shear_frequencies.astype(float)
    mu = problem.nu * problem.rho_squared
    beta = 2.0 * problem.nu * n * (n - problem.K)
    times = problem.target_times[:, None]
    phi = np.exp(-mu * times) * (1.0 - np.exp(-beta[None, :] * times)) / beta[None, :]
    derivative = -1j * problem.L * problem.amplitudes[None, :] * phi
    matrix = np.vstack((derivative[:, 1:].real, derivative[:, 1:].imag))
    right = -np.concatenate(
        ((derivative[:, 0] * p1).real, (derivative[:, 0] * p1).imag)
    )
    guess = np.linalg.solve(matrix, right)
    return guess, {
        "mu": mu,
        "beta": beta.tolist(),
        "jacobianConditionNumber": float(np.linalg.cond(matrix)),
        "jacobianRank": int(np.linalg.matrix_rank(matrix)),
        "linearResidualInfinityNorm": float(
            np.max(np.abs(derivative @ np.concatenate(([p1], guess))))
        ),
    }


def shoot(
    lattice: ModularLattice,
    p1: float,
    initial_guess: np.ndarray,
) -> tuple[np.ndarray, dict[str, object]]:
    calls = 0
    scale = 1.0e8

    def residual(unknown: np.ndarray) -> np.ndarray:
        nonlocal calls
        calls += 1
        parameters = np.concatenate(([p1], unknown.astype(float)))
        target = lattice.target_values(parameters)
        return scale * np.concatenate((target.real, target.imag))

    result = root(
        residual,
        initial_guess,
        method="hybr",
        options={"xtol": 2.0e-11, "maxfev": 160},
    )
    parameters = np.concatenate(([p1], result.x.astype(float)))
    final_target = lattice.target_values(parameters)
    maximum_residual = float(np.max(np.abs(final_target)))
    if maximum_residual > 2.0e-14:
        raise RuntimeError(
            f"shooting residual {maximum_residual:.3e} exceeds the safety threshold"
        )
    return parameters, {
        "success": bool(result.success),
        "message": str(result.message),
        "functionCalls": calls,
        "reportedFunctionEvaluations": int(result.nfev),
        "scaledResidualInfinityNorm": float(np.max(np.abs(result.fun))),
        "targetResidualMaximum": maximum_residual,
        "targetValues": [complex_pair(value) for value in final_target],
    }


def state_ledger(
    lattice: ModularLattice,
    parameters: np.ndarray,
    evaluation_times: np.ndarray,
) -> tuple[list[dict[str, object]], object]:
    solution = lattice.integrate(parameters, evaluation_times, dense_output=True)
    ledger: list[dict[str, object]] = []
    problem = lattice.problem
    rho4 = problem.rho_squared**2
    for time in problem.target_times:
        state = solution.sol(float(time))
        target = state[lattice.target_index]
        slope = lattice.rhs(float(time), state, parameters)[lattice.target_index]
        enstrophy = lattice.enstrophy(float(time), state, parameters)
        f_norm_squared = 2.0 * problem.multiplier**2 * abs(slope) ** 2
        c_t_norm_squared = rho4 * f_norm_squared
        atom = f_norm_squared / (problem.kappa**2 * enstrophy)
        first_jet_trace = c_t_norm_squared / (problem.kappa**6 * enstrophy)
        ledger.append({
            "time": float(time),
            "target": complex_pair(target),
            "slope": complex_pair(slope),
            "slopeMagnitude": float(abs(slope)),
            "enstrophy": enstrophy,
            "FNormSquared": float(f_norm_squared),
            "CtNormSquared": float(c_t_norm_squared),
            "positivePairing": float(problem.rho_squared * f_norm_squared),
            "jetAtom": float(atom),
            "firstJetTrace": float(first_jet_trace),
            "atomToFirstJetTraceRatio": float(atom / first_jet_trace),
        })
    return ledger, solution


def trace_records(
    lattice: ModularLattice,
    parameters: np.ndarray,
    solution,
    evaluation_times: np.ndarray,
) -> list[dict[str, float]]:
    values = solution.y[lattice.target_index]
    return [
        {
            "time": float(time),
            "real": float(value.real),
            "imag": float(value.imag),
            "magnitude": float(abs(value)),
        }
        for time, value in zip(evaluation_times, values, strict=True)
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--progress", type=Path, required=True)
    parser.add_argument("--resource-log", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    problem = load_problem(config)
    primary_spec = config["primaryIntegrator"]
    primary_cutoff = int(config["primaryCutoff"])
    start = perf_counter()
    args.progress.write_text("", encoding="utf-8")
    args.resource_log.write_text("", encoding="utf-8")
    append_ndjson(args.progress, {
        "stage": "start",
        "cutoff": primary_cutoff,
        "targetTimes": problem.target_times.tolist(),
        "finiteGalerkin": True,
        "pdeTimeStepping": True,
        "dns": False,
    })
    append_resource(args.resource_log, "start", perf_counter() - start)

    lattice = ModularLattice(
        problem,
        primary_cutoff,
        float(primary_spec["rtol"]),
        float(primary_spec["atol"]),
        float(primary_spec["maxStep"]),
    )
    sweep: list[dict[str, object]] = []
    last_guess: np.ndarray | None = None
    linear_audits: dict[str, object] = {}
    total_cases = len(config["p1Sweep"])
    for index, p1_raw in enumerate(config["p1Sweep"], start=1):
        p1 = float(p1_raw)
        guess, linear_audit = linear_guess(problem, p1)
        if last_guess is not None:
            continuation_guess = last_guess * (p1 / float(sweep[-1]["p1"]))
            if np.linalg.norm(continuation_guess - guess) < 0.25 * max(np.linalg.norm(guess), 1e-30):
                guess = continuation_guess
        before_rhs = lattice.rhs_calls
        parameters, shooting = shoot(lattice, p1, guess)
        ledger, _ = state_ledger(lattice, parameters, problem.target_times)
        elapsed = perf_counter() - start
        sweep.append({
            "p1": p1,
            "parameters": parameters.tolist(),
            "shooting": shooting,
            "events": ledger,
            "rhsCalls": lattice.rhs_calls - before_rhs,
        })
        linear_audits[f"p1={p1:.8g}"] = linear_audit
        last_guess = parameters[1:]
        eta = elapsed / index * (total_cases - index)
        append_ndjson(args.progress, {
            "stage": "shooting-sweep",
            "completed": index,
            "total": total_cases,
            "p1": p1,
            "targetResidual": shooting["targetResidualMaximum"],
            "minimumSlope": min(float(item["slopeMagnitude"]) for item in ledger),
            "elapsedSeconds": elapsed,
            "etaSeconds": eta,
        })
        append_resource(args.resource_log, f"sweep-p1-{p1:.8g}", elapsed)

    fixed_p1 = float(config["fixedP1"])
    matching = [item for item in sweep if float(item["p1"]) == fixed_p1]
    if len(matching) != 1:
        raise RuntimeError("fixed p1 must occur exactly once in p1Sweep")
    main_case = matching[0]
    main_parameters = np.asarray(main_case["parameters"], dtype=float)
    trace_times = np.linspace(0.0, 0.08, 1601)
    main_ledger, main_solution = state_ledger(
        lattice, main_parameters, trace_times
    )
    main_trace = trace_records(lattice, main_parameters, main_solution, trace_times)
    main_case = {
        **main_case,
        "events": main_ledger,
        "trace": main_trace,
    }

    cutoffs: list[dict[str, object]] = []
    cutoff_slopes: dict[int, np.ndarray] = {}
    cutoff_targets: dict[int, np.ndarray] = {}
    for index, cutoff_raw in enumerate(config["convergenceCutoffs"], start=1):
        cutoff = int(cutoff_raw)
        candidate = ModularLattice(
            problem,
            cutoff,
            float(primary_spec["rtol"]),
            float(primary_spec["atol"]),
            float(primary_spec["maxStep"]),
        )
        solution = candidate.integrate(main_parameters, problem.target_times)
        targets = solution.y[candidate.target_index]
        slopes: list[complex] = []
        boundary: list[float] = []
        for column, time in enumerate(problem.target_times):
            state = solution.y[:, column]
            slopes.append(
                candidate.rhs(float(time), state, main_parameters)[candidate.target_index]
            )
            boundary.append(float(max(abs(state[0]), abs(state[-1]))))
        cutoff_targets[cutoff] = np.asarray(targets)
        cutoff_slopes[cutoff] = np.asarray(slopes)
        cutoffs.append({
            "cutoff": cutoff,
            "targetValues": [complex_pair(value) for value in targets],
            "maximumTargetResidual": float(np.max(np.abs(targets))),
            "slopes": [complex_pair(value) for value in slopes],
            "maximumBoundaryCoefficient": float(max(boundary)),
            "rhsCalls": candidate.rhs_calls,
        })
        elapsed = perf_counter() - start
        append_ndjson(args.progress, {
            "stage": "cutoff-sweep",
            "completed": index,
            "total": len(config["convergenceCutoffs"]),
            "cutoff": cutoff,
            "maximumTargetResidual": float(np.max(np.abs(targets))),
            "maximumBoundaryCoefficient": float(max(boundary)),
            "elapsedSeconds": elapsed,
        })
    reference_cutoff = max(cutoff_slopes)
    reference_slopes = cutoff_slopes[reference_cutoff]
    reference_targets = cutoff_targets[reference_cutoff]
    for record in cutoffs:
        cutoff = int(record["cutoff"])
        record["maximumTargetDifferenceToM36"] = float(
            np.max(np.abs(cutoff_targets[cutoff] - reference_targets))
        )
        record["maximumRelativeSlopeDifferenceToM36"] = float(
            np.max(
                np.abs(cutoff_slopes[cutoff] - reference_slopes)
                / np.maximum(np.abs(reference_slopes), 1e-300)
            )
        )

    scaling_fits: list[dict[str, float]] = []
    p1_values = np.asarray([float(item["p1"]) for item in sweep])
    for event_index, time in enumerate(problem.target_times):
        atoms = np.asarray([
            float(item["events"][event_index]["jetAtom"]) for item in sweep
        ])
        fit = np.polyfit(np.log(p1_values), np.log(atoms), 1)
        scaling_fits.append({
            "time": float(time),
            "logLogExponent": float(fit[0]),
            "logPrefactor": float(fit[1]),
            "minimumAtom": float(np.min(atoms)),
            "maximumAtom": float(np.max(atoms)),
        })

    elapsed = perf_counter() - start
    payload = {
        "release": config["release"],
        "method": "vectorized finite modular Fourier lattice with SciPy DOP853 and six-real-variable hybr shooting",
        "configuration": config,
        "pdeReduction": {
            "velocity": "u=(f(y,z,t),0,v(y,t))",
            "divergence": "partial_x f + partial_z v = 0",
            "advection": "(u dot grad)u=(v f_z,0,0)",
            "reducedEquations": [
                "v_t=nu v_yy",
                "f_t+v f_z=nu(f_yy+f_zz)"
            ],
            "pressure": "constant"
        },
        "latticeFormula": "a_m'=-nu[(K+dm)^2+L^2]a_m-iL sum_l p_l exp(-nu(dl)^2t)(a_(m-l)+a_(m+l))",
        "linearAudits": linear_audits,
        "main": main_case,
        "parameterSweep": sweep,
        "scalingFits": scaling_fits,
        "cutoffSweep": cutoffs,
        "totalRhsCalls": lattice.rhs_calls + sum(int(item["rhsCalls"]) for item in cutoffs),
        "wallSeconds": elapsed,
        "classification": config["classification"],
        "claimBoundary": (
            "Finite Fourier-lattice corroboration of an analytically proved exact-NSE "
            "recurrence family. No continuum truncation error bound, DNS result, or "
            "numerical proof of the IFT or second-jet packing theorem is asserted."
        ),
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    append_ndjson(args.progress, {
        "stage": "complete-primary",
        "targetResidual": main_case["shooting"]["targetResidualMaximum"],
        "minimumSlope": min(float(item["slopeMagnitude"]) for item in main_ledger),
        "wallSeconds": elapsed,
        "rhsCalls": payload["totalRhsCalls"],
    })
    append_resource(args.resource_log, "complete-primary", elapsed)


if __name__ == "__main__":
    main()
