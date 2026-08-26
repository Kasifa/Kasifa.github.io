#!/usr/bin/env python3
"""Independent binary64/FFT/finite-ODE audit for R0.72D.

This program imports neither the producer nor its result.  Rudin--Shapiro
signs are generated directly from overlapping binary ``11`` pairs.  FFT
sampling tests the heat-weighted multiplier, while independent truncated
ODE solves apply the exact endpoint correction

    zeta = -P0 U(tau)G / P0 U(tau)e0

at ``tau=M^-3``.  The solves corroborate the perturbative construction and
its scales.  They are not interval arithmetic, infinite-lattice DNS, a
rigorous numerical lower bound with unknown comparison constants, or a proof
of Navier--Stokes regularity.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import platform
import resource
import sys
import time

import numpy as np
import scipy
from scipy.integrate import simpson, solve_ivp


# Raw parameters are deliberately repeated rather than read from the producer.
NU = 0.15
KAPPA = NU
K_Z = 1.10
GAMMA = 0.20
AMPLITUDE = 1.0
Q_SCALE = 1.0
RS_PREFIX_CONSTANT = 2.0 + math.sqrt(2.0)
FFT_GENERATIONS = (3, 5, 7, 9, 11)
ODE_GENERATIONS = (3, 4, 5, 6)
FFT_POINTS_PER_MAX_FREQUENCY = 32
HEAT_S_MAX = 16.0
HEAT_S_GRID = np.unique(
    np.concatenate(
        [
            np.linspace(0.0, 2.0, 81),
            np.linspace(2.1, HEAT_S_MAX, 140),
        ]
    )
)
ODE_RADIUS_FACTOR = 6
ODE_RTOL = 2.0e-10
ODE_ATOL = 2.0e-12


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--progress-log", type=Path)
    parser.add_argument("--resource-log", type=Path)
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def emit(message: str) -> None:
    print(f"[{utc_now()}] {message}", file=sys.stderr, flush=True)


def append_json(path: Path | None, payload: dict[str, object]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(payload, sort_keys=True) + "\n")


def progress(path: Path | None, stage: str, **fields: object) -> None:
    append_json(path, {"timestampUtc": utc_now(), "stage": stage, **fields})


def resource_snapshot(
    path: Path | None, stage: str, started: float, **fields: object
) -> None:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    append_json(
        path,
        {
            "timestampUtc": utc_now(),
            "stage": stage,
            "elapsedSeconds": time.perf_counter() - started,
            "userCpuSeconds": usage.ru_utime,
            "systemCpuSeconds": usage.ru_stime,
            "maximumResidentSetRaw": usage.ru_maxrss,
            "logicalCpuCount": os.cpu_count(),
            **fields,
        },
    )


def check(
    name: str, passed: bool, value: object, requirement: str
) -> dict[str, object]:
    return {
        "name": name,
        "passed": bool(passed),
        "value": value,
        "requirement": requirement,
    }


def binary_rudin_shapiro(m_value: int) -> np.ndarray:
    signs = np.empty(m_value, dtype=np.int8)
    for index in range(m_value):
        signs[index] = -1 if (index & (index >> 1)).bit_count() % 2 else 1
    return signs


def next_power_of_two(value: int) -> int:
    return 1 << (value - 1).bit_length()


def carrier_moment(m_value: int) -> int:
    carriers = np.arange(m_value, 2 * m_value, dtype=np.int64)
    return int(np.dot(carriers, carriers))


def complex_polynomial_grid(
    coefficients: np.ndarray, frequencies: np.ndarray, n_fft: int
) -> np.ndarray:
    packed = np.zeros(n_fft, dtype=np.complex128)
    packed[frequencies] = coefficients
    return np.fft.ifft(packed) * float(n_fft)


def fft_rudin_shapiro_audit() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    maximum_endpoint_defect = 0.0
    maximum_prefix_over_bound = 0.0
    maximum_pq_identity_defect = 0.0

    for generation in FFT_GENERATIONS:
        m_value = 1 << generation
        signs = binary_rudin_shapiro(m_value)
        n_fft = next_power_of_two(FFT_POINTS_PER_MAX_FREQUENCY * 2 * m_value)

        values = complex_polynomial_grid(
            signs.astype(float), np.arange(m_value, dtype=int), n_fft
        )
        endpoint = int(signs.sum())
        endpoint_defect = abs(endpoint * endpoint - 2 * m_value)
        maximum_endpoint_defect = max(maximum_endpoint_defect, endpoint_defect)

        prefix_lengths = sorted(
            {
                1,
                2,
                3,
                max(1, m_value // 8),
                max(1, m_value // 4),
                max(1, m_value // 2),
                m_value - 1,
                m_value,
            }
        )
        prefix_ratios: list[float] = []
        for length in prefix_lengths:
            prefix_values = complex_polynomial_grid(
                signs[:length].astype(float), np.arange(length, dtype=int), n_fft
            )
            ratio = float(np.max(np.abs(prefix_values))) / (
                RS_PREFIX_CONSTANT * math.sqrt(m_value)
            )
            prefix_ratios.append(ratio)
            maximum_prefix_over_bound = max(maximum_prefix_over_bound, ratio)

        half = m_value // 2
        if half:
            p_half = signs[:half].astype(float)
            q_half = signs[half:].astype(float)
            p_values = complex_polynomial_grid(
                p_half, np.arange(half, dtype=int), n_fft
            )
            q_values = complex_polynomial_grid(
                q_half, np.arange(half, dtype=int), n_fft
            )
            # The second half equals Q_(n-1); the phase shift has unit modulus.
            identity = np.abs(p_values) ** 2 + np.abs(q_values) ** 2
            pq_defect = float(np.max(np.abs(identity - float(m_value))))
            maximum_pq_identity_defect = max(
                maximum_pq_identity_defect, pq_defect
            )
        else:
            pq_defect = 0.0

        rows.append(
            {
                "generation": generation,
                "M": m_value,
                "coefficientEnergy": int(np.dot(signs.astype(int), signs.astype(int))),
                "PAtOne": endpoint,
                "PAtOneSquaredDefect": endpoint_defect,
                "sampledPMaximum": float(np.max(np.abs(values))),
                "sampledPMaximumOverSqrt2M": float(
                    np.max(np.abs(values)) / math.sqrt(2.0 * m_value)
                ),
                "sampledPrefixLengths": prefix_lengths,
                "maximumSampledPrefixOverAnalyticBound": max(prefix_ratios),
                "halfGenerationParallelogramDefect": pq_defect,
                "fftSize": n_fft,
            }
        )

    return {
        "generationRule": "epsilon_j=(-1)^(popcount(j & (j>>1)))",
        "rows": rows,
        "maximumEndpointDefect": maximum_endpoint_defect,
        "maximumSampledPrefixOverAnalyticBound": maximum_prefix_over_bound,
        "maximumSampledHalfGenerationIdentityDefect": maximum_pq_identity_defect,
    }


def physical_multiplier_norm_fft(
    m_value: int,
    signs: np.ndarray,
    scaled_time: float,
    n_fft: int,
) -> float:
    carriers = np.arange(m_value, 2 * m_value, dtype=int)
    weights = np.exp(-scaled_time * (carriers.astype(float) / m_value) ** 2)
    analytic = complex_polynomial_grid(signs.astype(float) * weights, carriers, n_fft)
    return 2.0 * abs(K_Z) * AMPLITUDE * float(np.max(np.abs(analytic.real)))


def heat_fft_audit() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    l1_values: list[float] = []
    l2_square_values: list[float] = []
    m_values: list[float] = []
    maximum_pointwise_over_envelope = 0.0

    for generation in FFT_GENERATIONS:
        m_value = 1 << generation
        signs = binary_rudin_shapiro(m_value)
        n_fft = next_power_of_two(FFT_POINTS_PER_MAX_FREQUENCY * 2 * m_value)
        norms = np.array(
            [
                physical_multiplier_norm_fft(
                    m_value, signs, float(s_value), n_fft
                )
                for s_value in HEAT_S_GRID
            ],
            dtype=float,
        )
        envelope = (
            2.0
            * abs(K_Z)
            * AMPLITUDE
            * RS_PREFIX_CONSTANT
            * math.sqrt(m_value)
            * np.exp(-HEAT_S_GRID)
        )
        pointwise_ratio = float(np.max(norms / envelope))
        maximum_pointwise_over_envelope = max(
            maximum_pointwise_over_envelope, pointwise_ratio
        )

        time_jacobian = 1.0 / (KAPPA * m_value**2)
        l1_truncated = float(simpson(norms, x=HEAT_S_GRID) * time_jacobian)
        l2_square_truncated = float(
            simpson(norms**2, x=HEAT_S_GRID) * time_jacobian
        )
        l1_tail_bound = float(
            2.0
            * abs(K_Z)
            * AMPLITUDE
            * RS_PREFIX_CONSTANT
            * math.sqrt(m_value)
            * math.exp(-HEAT_S_MAX)
            * time_jacobian
        )
        l2_tail_bound = float(
            (
                2.0
                * abs(K_Z)
                * AMPLITUDE
                * RS_PREFIX_CONSTANT
                * math.sqrt(m_value)
            )
            ** 2
            * math.exp(-2.0 * HEAT_S_MAX)
            * time_jacobian
            / 2.0
        )
        l1_values.append(l1_truncated)
        l2_square_values.append(l2_square_truncated)
        m_values.append(float(m_value))
        rows.append(
            {
                "generation": generation,
                "M": m_value,
                "fftSize": n_fft,
                "initialMultiplierNorm": float(norms[0]),
                "initialNormOverExactOddEndpoint": float(
                    norms[0]
                    / (2.0 * abs(K_Z) * AMPLITUDE * math.sqrt(2.0 * m_value))
                ),
                "maximumPointwiseOverAbelEnvelope": pointwise_ratio,
                "observedTruncatedL1": l1_truncated,
                "L1TailEnvelope": l1_tail_bound,
                "MThreeHalvesTimesObservedL1OverA": (
                    m_value**1.5 * l1_truncated / AMPLITUDE
                ),
                "observedTruncatedL2Square": l2_square_truncated,
                "L2SquareTailEnvelope": l2_tail_bound,
                "MTimesObservedL2SquareOverASquared": (
                    m_value * l2_square_truncated / AMPLITUDE**2
                ),
            }
        )

    l1_power = float(np.polyfit(np.log(m_values), np.log(l1_values), 1)[0])
    l2_square_power = float(
        np.polyfit(np.log(m_values), np.log(l2_square_values), 1)[0]
    )
    return {
        "scaledTime": "s=kappa*M^2*t",
        "sampledRange": [float(HEAT_S_GRID[0]), float(HEAT_S_GRID[-1])],
        "sampleCount": int(HEAT_S_GRID.size),
        "rows": rows,
        "fittedObservedL1Power": l1_power,
        "fittedObservedL2SquarePower": l2_square_power,
        "maximumPointwiseOverAbelEnvelope": maximum_pointwise_over_envelope,
        "scope": "truncated sampled norms plus an analytic envelope for the omitted tail",
    }


def ode_rhs_factory(
    m_value: int, radius_factor: int
) -> tuple[callable, np.ndarray, np.ndarray, int, float, float]:
    signs = binary_rudin_shapiro(m_value).astype(float)
    carriers = np.arange(m_value, 2 * m_value, dtype=int)
    radius = radius_factor * m_value
    modes = np.arange(-radius, radius + 1, dtype=float)
    dimension = modes.size
    target = radius
    tau = float(m_value ** -3)
    delta = GAMMA * m_value**1.5 / AMPLITUDE

    def rhs(scaled_time: float, flat_state: np.ndarray) -> np.ndarray:
        state = flat_state.reshape(2, dimension)
        output = -tau * NU * modes[None, :] ** 2 * state
        physical_time = tau * scaled_time
        weights = np.exp(-KAPPA * carriers.astype(float) ** 2 * physical_time)
        coupling = -1j * tau * delta * K_Z * AMPLITUDE
        for carrier, sign, weight in zip(carriers, signs, weights, strict=True):
            coefficient = coupling * sign * weight
            output[:, carrier:] += coefficient * state[:, :-carrier]
            output[:, :-carrier] += coefficient * state[:, carrier:]
        return output.reshape(-1)

    return rhs, signs, carriers, target, tau, delta


def run_ode_case(m_value: int, radius_factor: int) -> dict[str, object]:
    rhs, signs, carriers, target, tau, delta = ode_rhs_factory(
        m_value, radius_factor
    )
    radius = radius_factor * m_value
    dimension = 2 * radius + 1
    initial = np.zeros((2, dimension), dtype=np.complex128)
    launch = initial[0]
    target_column = initial[1]
    orientation = 1.0 if K_Z >= 0 else -1.0
    for carrier, sign in zip(carriers, signs, strict=True):
        value = 1j * orientation * sign / math.sqrt(2.0)
        launch[target - carrier] = value
        launch[target + carrier] = value
    target_column[target] = 1.0

    solution = solve_ivp(
        rhs,
        (0.0, 1.0),
        initial.reshape(-1),
        method="DOP853",
        rtol=ODE_RTOL,
        atol=ODE_ATOL,
        t_eval=[1.0],
    )
    if not solution.success:
        raise RuntimeError(f"finite ODE failed for M={m_value}: {solution.message}")
    terminal = solution.y[:, -1].reshape(2, dimension)
    evolved_launch = terminal[0]
    evolved_target = terminal[1]
    zeta = -evolved_launch[target] / evolved_target[target]
    normalization = math.sqrt(m_value) / math.sqrt(m_value + abs(zeta) ** 2)
    root_state = normalization * (evolved_launch + zeta * evolved_target)

    root_residual = abs(root_state[target])
    root_scale = max(
        float(np.linalg.norm(evolved_launch)),
        abs(zeta) * float(np.linalg.norm(evolved_target)),
        np.finfo(float).tiny,
    )
    relative_root_residual = float(root_residual / root_scale)

    weights_tau = np.exp(-KAPPA * carriers.astype(float) ** 2 * tau)
    h_tau = -1j * K_Z * AMPLITUDE * np.sum(
        signs
        * weights_tau
        * (root_state[target - carriers] + root_state[target + carriers])
    )
    h0 = math.sqrt(2.0) * abs(K_Z) * AMPLITUDE * m_value

    rhs_terminal = rhs(1.0, root_state[None, :].repeat(2, axis=0).reshape(-1))
    # Only the first repeated row is used; repeating avoids a second RHS shape.
    target_derivative = rhs_terminal.reshape(2, dimension)[0, target] / tau
    slope_identity_defect = float(
        abs(target_derivative - delta * h_tau)
        / max(abs(delta * h_tau), np.finfo(float).tiny)
    )

    initial_root_state = normalization * (launch + zeta * target_column)
    initial_norm_square = float(np.vdot(initial_root_state, initial_root_state).real)
    terminal_norm_square = float(np.vdot(root_state, root_state).real)

    k_s = carrier_moment(m_value)
    k_v = AMPLITUDE**2 * k_s
    k_f = normalization**2 * k_s
    p_amplitude = delta * Q_SCALE**2
    s_square = 3.0 * p_amplitude**2 * k_v / k_f
    energy = s_square * k_f + p_amplitude**2 * k_v
    atom = (
        s_square
        * p_amplitude**2
        * abs(h_tau) ** 2
        / (Q_SCALE**2 * energy)
    )
    atom_over_d13 = atom / (Q_SCALE**2 * energy) ** (1.0 / 3.0)
    charge_upper = (
        p_amplitude**2
        * s_square
        * AMPLITUDE**2
        / (Q_SCALE**4 * energy)
    )

    return {
        "M": m_value,
        "carrierRange": [m_value, 2 * m_value - 1],
        "radiusFactor": radius_factor,
        "dimension": dimension,
        "tau": tau,
        "delta": delta,
        "deltaTimesAOverGammaMThreeHalves": (
            delta * AMPLITUDE / (GAMMA * m_value**1.5)
        ),
        "solver": {
            "method": "DOP853",
            "rtol": ODE_RTOL,
            "atol": ODE_ATOL,
            "functionEvaluations": int(solution.nfev),
            "status": int(solution.status),
        },
        "zetaReal": float(zeta.real),
        "zetaImag": float(zeta.imag),
        "zetaAbsolute": float(abs(zeta)),
        "normalization": normalization,
        "normalizedLaunchNormSquared": initial_norm_square,
        "sqrtMTimesZetaAbsoluteOverGamma": (
            math.sqrt(m_value) * abs(zeta) / GAMMA
        ),
        "relativeRootResidual": relative_root_residual,
        "h0": h0,
        "hTauReal": float(h_tau.real),
        "hTauImag": float(h_tau.imag),
        "hTauAbsoluteOverH0": float(abs(h_tau) / h0),
        "slopeIdentityRelativeDefect": slope_identity_defect,
        "initialNormSquared": initial_norm_square,
        "terminalNormSquared": terminal_norm_square,
        "terminalOverInitialNormSquared": terminal_norm_square / initial_norm_square,
        "Ks": k_s,
        "Kv": k_v,
        "activeMomentKf": k_f,
        "KfOverKs": k_f / k_s,
        "S2KfOverP2Kv": s_square * k_f / (p_amplitude**2 * k_v),
        "launchAtomOverDOneThirdModel": float(atom_over_d13),
        "atomOverGammaFourThirds": float(atom_over_d13 / GAMMA ** (4.0 / 3.0)),
        "fullChargeUpperModel": float(charge_upper),
        "chargeOverGammaSquared": float(charge_upper / GAMMA**2),
    }


def finite_ode_audit(
    progress_path: Path | None,
    resource_path: Path | None,
    started: float,
) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    for generation in ODE_GENERATIONS:
        m_value = 1 << generation
        emit(f"finite ODE root test M={m_value}")
        row = run_ode_case(m_value, ODE_RADIUS_FACTOR)
        rows.append(row)
        progress(
            progress_path,
            "ode-case-complete",
            M=m_value,
            relativeRootResidual=row["relativeRootResidual"],
            hRatio=row["hTauAbsoluteOverH0"],
        )
        resource_snapshot(
            resource_path,
            "ode-case-complete",
            started,
            M=m_value,
            dimension=row["dimension"],
        )

    m_values = np.array([float(row["M"]) for row in rows])
    zeta_values = np.array([float(row["zetaAbsolute"]) for row in rows])
    atom_values = np.array(
        [float(row["launchAtomOverDOneThirdModel"]) for row in rows]
    )
    charge_values = np.array(
        [float(row["fullChargeUpperModel"]) for row in rows]
    )
    zeta_power = float(np.polyfit(np.log(m_values), np.log(zeta_values), 1)[0])
    atom_power = float(np.polyfit(np.log(m_values), np.log(atom_values), 1)[0])
    charge_power = float(np.polyfit(np.log(m_values), np.log(charge_values), 1)[0])

    pressure_m = 32
    pressure_rows = [
        run_ode_case(pressure_m, radius_factor)
        for radius_factor in (4, 6, 8)
    ]
    reference = pressure_rows[1]
    maximum_pressure_zeta_relative_defect = max(
        abs(float(row["zetaAbsolute"]) - float(reference["zetaAbsolute"]))
        / max(float(reference["zetaAbsolute"]), np.finfo(float).tiny)
        for row in pressure_rows
    )
    maximum_pressure_h_relative_defect = max(
        abs(float(row["hTauAbsoluteOverH0"]) - float(reference["hTauAbsoluteOverH0"]))
        / max(float(reference["hTauAbsoluteOverH0"]), np.finfo(float).tiny)
        for row in pressure_rows
    )

    return {
        "equation": "dF/dt=-nu*r^2*F-i*delta*Kz*a*sum_j epsilon_j exp(-kappa*r_j^2*t)(T_rj+T_-rj)F",
        "rootCorrection": "zeta=-P0*U(tau)G/(P0*U(tau)e0)",
        "rootTime": "tau=M^-3",
        "rows": rows,
        "fittedPowers": {
            "zetaAbsolute": zeta_power,
            "launchAtomOverDOneThird": atom_power,
            "fullChargeUpper": charge_power,
        },
        "pressureTest": {
            "M": pressure_m,
            "radiusFactors": [4, 6, 8],
            "rows": pressure_rows,
            "maximumZetaRelativeDefect": maximum_pressure_zeta_relative_defect,
            "maximumHRatioRelativeDefect": maximum_pressure_h_relative_defect,
        },
    }


def main() -> None:
    args = parse_args()
    started = time.perf_counter()
    emit("R0.72D independent audit started")
    progress(args.progress_log, "independent-start")
    resource_snapshot(args.resource_log, "independent-start", started)

    rs = fft_rudin_shapiro_audit()
    emit("binary Rudin--Shapiro and FFT prefix checks complete")
    progress(args.progress_log, "fft-rudin-shapiro-complete")

    heat = heat_fft_audit()
    emit(
        "heat FFT audit complete: "
        f"L1 power {heat['fittedObservedL1Power']:.6f}, "
        f"L2-square power {heat['fittedObservedL2SquarePower']:.6f}"
    )
    progress(
        args.progress_log,
        "heat-fft-complete",
        l1Power=heat["fittedObservedL1Power"],
        l2SquarePower=heat["fittedObservedL2SquarePower"],
    )
    resource_snapshot(args.resource_log, "heat-fft-complete", started)

    ode = finite_ode_audit(args.progress_log, args.resource_log, started)
    emit("finite ODE and truncation-pressure tests complete")
    progress(args.progress_log, "finite-ode-complete")

    ode_rows = ode["rows"]
    pressure = ode["pressureTest"]
    endpoint_rows = rs["rows"]
    checks = [
        check(
            "binary Rudin--Shapiro signs have the odd endpoint identity",
            rs["maximumEndpointDefect"] == 0
            and all(row["coefficientEnergy"] == row["M"] for row in endpoint_rows),
            {"maximumEndpointDefect": rs["maximumEndpointDefect"]},
            "sum epsilon_j squared equals 2M and sum epsilon_j^2=M",
        ),
        check(
            "FFT samples obey the dyadic prefix envelope",
            rs["maximumSampledPrefixOverAnalyticBound"] <= 1.0 + 2.0e-13
            and rs["maximumSampledHalfGenerationIdentityDefect"] < 2.0e-9,
            {
                "prefixOverBound": rs["maximumSampledPrefixOverAnalyticBound"],
                "parallelogramDefect": rs["maximumSampledHalfGenerationIdentityDefect"],
            },
            "sampled prefixes lie below (2+sqrt(2))*sqrt(M) and the sampled P/Q identity closes",
        ),
        check(
            "heat-weighted FFT multipliers obey the Abel envelope",
            heat["maximumPointwiseOverAbelEnvelope"] <= 1.0 + 3.0e-13,
            heat["maximumPointwiseOverAbelEnvelope"],
            "all sampled ||V(t)|| values lie below the analytic heat envelope",
        ),
        check(
            "observed heat multiplier L1 has the M^-3/2 scale",
            abs(float(heat["fittedObservedL1Power"]) + 1.5) < 0.04,
            heat["fittedObservedL1Power"],
            "binary64 FFT/quadrature fit is within 0.04 of -3/2",
        ),
        check(
            "observed heat multiplier L2-square has the M^-1 scale",
            abs(float(heat["fittedObservedL2SquarePower"]) + 1.0) < 0.04,
            heat["fittedObservedL2SquarePower"],
            "binary64 FFT/quadrature fit is within 0.04 of -1",
        ),
        check(
            "endpoint correction creates an interior root",
            max(float(row["relativeRootResidual"]) for row in ode_rows) < 2.0e-13,
            max(float(row["relativeRootResidual"]) for row in ode_rows),
            "|P0 U(tau)(G+zeta e0)| is below 2e-13 relative to the evolved columns",
        ),
        check(
            "root correction has the predicted M^-1/2 size",
            abs(float(ode["fittedPowers"]["zetaAbsolute"]) + 0.5) < 0.10,
            {
                "fittedPower": ode["fittedPowers"]["zetaAbsolute"],
                "terminalScaledZeta": ode_rows[-1]["sqrtMTimesZetaAbsoluteOverGamma"],
            },
            "|zeta|=Theta(M^-1/2) on the finite ODE family",
        ),
        check(
            "root row remains aligned at tau=M^-3",
            float(ode_rows[-1]["hTauAbsoluteOverH0"]) > 0.96
            and float(ode_rows[-1]["hTauAbsoluteOverH0"])
            > float(ode_rows[0]["hTauAbsoluteOverH0"]),
            {
                "firstRatio": ode_rows[0]["hTauAbsoluteOverH0"],
                "terminalRatio": ode_rows[-1]["hTauAbsoluteOverH0"],
            },
            "|h(tau)|/h0 approaches one along the audited sequence",
        ),
        check(
            "finite ODE root slope equals delta times the target row",
            max(float(row["slopeIdentityRelativeDefect"]) for row in ode_rows) < 3.0e-13,
            max(float(row["slopeIdentityRelativeDefect"]) for row in ode_rows),
            "F0(tau)=0 implies F0'(tau)=delta*h(tau)",
        ),
        check(
            "truncated skew-diffusive evolution is contractive",
            max(float(row["terminalOverInitialNormSquared"]) for row in ode_rows)
            <= 1.0 + 2.0e-10,
            max(float(row["terminalOverInitialNormSquared"]) for row in ode_rows),
            "the corrected state norm does not increase under diffusion plus skew coupling",
        ),
        check(
            "physical launch normalization and amplitude balance are exact",
            max(
                abs(float(row["normalizedLaunchNormSquared"]) - float(row["M"]))
                for row in ode_rows
            )
            < 3.0e-13
            and max(
                abs(float(row["S2KfOverP2Kv"]) - 3.0) for row in ode_rows
            )
            < 3.0e-13,
            {
                "maximumNormSquareDefect": max(
                    abs(float(row["normalizedLaunchNormSquared"]) - float(row["M"]))
                    for row in ode_rows
                ),
                "maximumBalanceDefect": max(
                    abs(float(row["S2KfOverP2Kv"]) - 3.0) for row in ode_rows
                ),
                "terminalKfOverKs": ode_rows[-1]["KfOverKs"],
            },
            "the corrected vector is normalized to M and S^2*Kf=3*P^2*Kv uses its actual active moment",
        ),
        check(
            "normalized launch-root model stays nonzero",
            abs(float(ode["fittedPowers"]["launchAtomOverDOneThird"])) < 0.10
            and min(float(row["atomOverGammaFourThirds"]) for row in ode_rows) > 0.0,
            {
                "fittedPower": ode["fittedPowers"]["launchAtomOverDOneThird"],
                "terminalScaledAtom": ode_rows[-1]["atomOverGammaFourThirds"],
            },
            "the finite-ODE atom divided by the model D^(1/3) remains at gamma^(4/3) scale",
        ),
        check(
            "full rotational-charge comparison stays bounded",
            abs(float(ode["fittedPowers"]["fullChargeUpper"])) < 0.10
            and max(float(row["chargeOverGammaSquared"]) for row in ode_rows) < 0.5,
            {
                "fittedPower": ode["fittedPowers"]["fullChargeUpper"],
                "terminalScaledCharge": ode_rows[-1]["chargeOverGammaSquared"],
            },
            "(3/4)*(delta*a)^2/Ks remains at gamma^2 scale",
        ),
        check(
            "finite ODE pressure test is stable under truncation radius",
            float(pressure["maximumZetaRelativeDefect"]) < 2.0e-7
            and float(pressure["maximumHRatioRelativeDefect"]) < 2.0e-7,
            {
                "maximumZetaRelativeDefect": pressure["maximumZetaRelativeDefect"],
                "maximumHRatioRelativeDefect": pressure["maximumHRatioRelativeDefect"],
            },
            "radius factors 4, 6, and 8 agree to 2e-7 for M=32",
        ),
    ]
    all_passed = all(bool(row["passed"]) for row in checks)

    payload = {
        "schemaVersion": "r072d-dynamical-ledger-independent-v1",
        "release": "R0.72D",
        "generatedAtUtc": utc_now(),
        "allPassed": all_passed,
        "checkCount": len(checks),
        "passedCheckCount": sum(bool(row["passed"]) for row in checks),
        "independence": {
            "importsProducer": False,
            "readsProducerResult": False,
            "rawParametersRepeatedLocally": True,
            "rudinShapiroPath": "overlapping binary 11-pair parity only",
        },
        "arithmetic": {
            "format": "IEEE-754 binary64/complex128",
            "intervalArithmetic": False,
            "multiplierNorm": "uniform-grid FFT samples",
            "quadrature": "composite Simpson rule in scaled time",
            "finiteODE": "SciPy DOP853 on symmetric finite Fourier truncations",
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
        "parameters": {
            "nu": NU,
            "kappa": KAPPA,
            "Kz": K_Z,
            "gamma": GAMMA,
            "a": AMPLITUDE,
            "q": Q_SCALE,
            "fftGenerations": list(FFT_GENERATIONS),
            "odeGenerations": list(ODE_GENERATIONS),
            "fftPointsPerMaximumFrequency": FFT_POINTS_PER_MAX_FREQUENCY,
            "heatScaledTimeMaximum": HEAT_S_MAX,
            "odeRadiusFactor": ODE_RADIUS_FACTOR,
            "odeRtol": ODE_RTOL,
            "odeAtol": ODE_ATOL,
            "randomness": False,
        },
        "rudinShapiroFFT": rs,
        "heatMultiplierFFT": heat,
        "finiteODE": ode,
        "checks": checks,
        "scope": {
            "intervalArithmetic": False,
            "provesAllGenerations": False,
            "provesInfiniteLattice": False,
            "rigorousUnknownConstantLowerBound": False,
            "provesNSERegularity": False,
            "note": (
                "FFT grids and finite ODE truncations corroborate the analytic scales. "
                "The report, not these binary64 samples, carries the perturbative argument."
            ),
        },
        "elapsedSeconds": time.perf_counter() - started,
    }

    if not all_passed:
        failed = [row["name"] for row in checks if not row["passed"]]
        raise AssertionError(f"independent checks failed: {failed}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    progress(
        args.progress_log,
        "independent-complete",
        allPassed=all_passed,
        checkCount=len(checks),
        elapsedSeconds=payload["elapsedSeconds"],
    )
    resource_snapshot(
        args.resource_log,
        "independent-complete",
        started,
        allPassed=all_passed,
        checkCount=len(checks),
    )
    emit(f"R0.72D independent audit passed in {payload['elapsedSeconds']:.2f}s")


if __name__ == "__main__":
    main()
