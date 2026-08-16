#!/usr/bin/env python3
"""Tangential six-mode modulation and first normal forcing.

The projected ODE is not the full Navier--Stokes evolution: it keeps only the
original six Fourier modes.  Its purpose is to separate motion tangent to the
six-mode space from the normal modes created at first order.
"""

from __future__ import annotations

import json
import math

import numpy as np

from six_mode_coercivity import closed_form_diagnostics
from triad_leakage_variation import (
    ORIGINAL_PARAMETERS,
    analytic_fixed_injection_candidates,
    bilinear,
    diagnostics,
    field_from_parameters,
    normalize,
)


SQRT2 = math.sqrt(2.0)


def tangent_nonlinearity(parameters: np.ndarray) -> np.ndarray:
    values = [
        complex(parameters[2 * index], parameters[2 * index + 1])
        for index in range(6)
    ]
    alpha, zeta, beta, eta, gamma, theta = values
    output = [
        -1.0j * np.conjugate(beta) * np.conjugate(gamma),
        1.0j
        * (
            np.conjugate(beta) * np.conjugate(theta)
            + np.conjugate(gamma) * np.conjugate(eta)
        ),
        1.0j * np.conjugate(alpha) * np.conjugate(gamma),
        1.0j
        * (
            np.conjugate(alpha) * np.conjugate(theta)
            - np.conjugate(gamma) * np.conjugate(zeta)
        ),
        0.0j,
        -1.0j
        * (
            np.conjugate(alpha) * np.conjugate(eta)
            + np.conjugate(beta) * np.conjugate(zeta)
        ),
    ]
    flattened = np.empty(12)
    for index, value in enumerate(output):
        flattened[2 * index] = value.real
        flattened[2 * index + 1] = value.imag
    return flattened


def tangent_rhs(
    parameters: np.ndarray,
    viscosity: float,
    amplitude: float,
) -> np.ndarray:
    laplacian_weights = np.repeat([1.0, 1.0, 1.0, 1.0, 2.0, 2.0], 2)
    return (
        -viscosity * laplacian_weights * parameters
        - amplitude * tangent_nonlinearity(parameters)
    )


def h_three_half_squared(parameters: np.ndarray) -> float:
    values = [
        complex(parameters[2 * index], parameters[2 * index + 1])
        for index in range(6)
    ]
    alpha, zeta, beta, eta, gamma, theta = values
    horizontal_vertical = (
        abs(alpha) ** 2 + abs(zeta) ** 2 + abs(beta) ** 2 + abs(eta) ** 2
    )
    closing = 2.0 * abs(gamma) ** 2 + abs(theta) ** 2
    return 2.0 * horizontal_vertical + 4.0 * SQRT2 * closing


def reduced_parameters(horizontal: float, scalar: float, closing: float) -> np.ndarray:
    """Return alpha=beta=A, zeta=eta=-Y, gamma=0, theta=-i C."""

    return np.asarray(
        [
            horizontal,
            0.0,
            -scalar,
            0.0,
            horizontal,
            0.0,
            -scalar,
            0.0,
            0.0,
            0.0,
            0.0,
            -closing,
        ],
        dtype=float,
    )


def reduced_rhs(
    state: np.ndarray,
    viscosity: float,
    amplitude: float,
) -> np.ndarray:
    horizontal, scalar, closing = state
    return np.asarray(
        [
            -viscosity * horizontal,
            -viscosity * scalar - amplitude * horizontal * closing,
            -2.0 * viscosity * closing + 2.0 * amplitude * horizontal * scalar,
        ]
    )


def rk4_step(
    state: np.ndarray,
    step: float,
    viscosity: float,
    amplitude: float,
) -> np.ndarray:
    first = reduced_rhs(state, viscosity, amplitude)
    second = reduced_rhs(state + 0.5 * step * first, viscosity, amplitude)
    third = reduced_rhs(state + 0.5 * step * second, viscosity, amplitude)
    fourth = reduced_rhs(state + step * third, viscosity, amplitude)
    return state + step * (first + 2.0 * second + 2.0 * third + fourth) / 6.0


def normal_forcing(parameters: np.ndarray) -> list[dict[str, object]]:
    support = set(field_from_parameters(parameters))
    nonlinear = bilinear(
        field_from_parameters(parameters),
        field_from_parameters(parameters),
    )
    records = []
    for wavevector, coefficient in sorted(nonlinear.items()):
        if wavevector in support or np.vdot(coefficient, coefficient).real < 1e-28:
            continue
        records.append(
            {
                "wavevector": wavevector,
                "coefficient": [
                    [float(value.real), float(value.imag)] for value in coefficient
                ],
                "hHalfContribution": float(
                    np.linalg.norm(wavevector)
                    * np.vdot(coefficient, coefficient).real
                ),
            }
        )
    return records


def integrate_reduced_candidate(
    gamma: float = 1.2,
    viscosity: float = 1.0,
    step: float = 1e-5,
    final_time: float = 0.1,
) -> dict[str, object]:
    original = normalize(ORIGINAL_PARAMETERS)
    injection = abs(diagnostics(original)["transfer"])
    analytic = analytic_fixed_injection_candidates(injection)["largeRoot"]
    parameters = np.asarray(analytic["parameters"], dtype=float)
    horizontal = parameters[0]
    scalar = -parameters[2]
    closing = -parameters[11]
    state = np.asarray([horizontal, scalar, closing])
    initial_parameters = reduced_parameters(*state)
    initial_transfer = closed_form_diagnostics(initial_parameters)["transfer"]
    dissipation = h_three_half_squared(initial_parameters)
    critical_amplitude = viscosity * dissipation / (-initial_transfer)
    amplitude = gamma * critical_amplitude
    checkpoints = [0.0, 0.001, 0.0025, 0.005, 0.01, 0.025, 0.05, 0.1]
    trajectory = []
    scalar_sign_change_time = None

    def snapshot(time: float, current: np.ndarray) -> dict[str, float]:
        current_parameters = reduced_parameters(*current)
        values = closed_form_diagnostics(current_parameters)
        return {
            "time": time,
            "horizontal": float(current[0]),
            "scalar": float(current[1]),
            "closing": float(current[2]),
            "energy": values["energy"],
            "transfer": values["transfer"],
            "outsideSquared": values["outsideSquared"],
        }

    time = 0.0
    checkpoint_index = 0
    trajectory.append(snapshot(time, state))
    checkpoint_index += 1
    total_steps = int(round(final_time / step))
    for _ in range(total_steps):
        previous_state = state.copy()
        previous_time = time
        state = rk4_step(state, step, viscosity, amplitude)
        time += step
        if (
            scalar_sign_change_time is None
            and previous_state[1] > 0
            and state[1] <= 0
        ):
            fraction = previous_state[1] / (previous_state[1] - state[1])
            scalar_sign_change_time = previous_time + fraction * step
        while (
            checkpoint_index < len(checkpoints)
            and time >= checkpoints[checkpoint_index] - step / 2.0
        ):
            trajectory.append(snapshot(checkpoints[checkpoint_index], state))
            checkpoint_index += 1

    return {
        "parameters": {
            "viscosity": viscosity,
            "gamma": gamma,
            "criticalAmplitude": critical_amplitude,
            "amplitude": amplitude,
            "step": step,
            "finalTime": final_time,
        },
        "trajectory": trajectory,
        "scalarSignChangeTime": scalar_sign_change_time,
        "initialNormalForcing": normal_forcing(initial_parameters),
    }


def validate() -> dict[str, object]:
    random = np.random.default_rng(20260816)
    maximum_tangent_error = 0.0
    for _ in range(200):
        parameters = random.normal(size=12)
        field = field_from_parameters(parameters)
        nonlinear = bilinear(field, field)
        closed = tangent_nonlinearity(parameters)
        direct_values = [
            nonlinear[(1, 0, 0)][1],
            nonlinear[(1, 0, 0)][2],
            nonlinear[(0, 1, 0)][0],
            nonlinear[(0, 1, 0)][2],
            nonlinear[(-1, -1, 0)][0],
            nonlinear[(-1, -1, 0)][2],
        ]
        direct = np.empty(12)
        for index, value in enumerate(direct_values):
            direct[2 * index] = value.real
            direct[2 * index + 1] = value.imag
        maximum_tangent_error = max(
            maximum_tangent_error,
            float(np.max(np.abs(closed - direct))),
        )
    audit = integrate_reduced_candidate()
    half_step = integrate_reduced_candidate(step=5e-6)
    assert maximum_tangent_error < 2e-14
    assert len(audit["initialNormalForcing"]) == 4
    assert all(
        record["coefficient"][0] == [0.0, 0.0]
        and record["coefficient"][1] == [0.0, 0.0]
        for record in audit["initialNormalForcing"]
    )
    fields = ("energy", "transfer", "outsideSquared")
    convergence = {
        field: max(
            abs(left[field] - right[field])
            / max(abs(left[field]), abs(right[field]), 1e-300)
            for left, right in zip(
                audit["trajectory"],
                half_step["trajectory"],
                strict=True,
            )
        )
        for field in fields
    }
    convergence["scalarSignChangeTime"] = abs(
        audit["scalarSignChangeTime"] - half_step["scalarSignChangeTime"]
    ) / half_step["scalarSignChangeTime"]
    assert max(convergence.values()) < 2e-9
    return {
        "closedTangentFormulaMaximumAbsoluteError": maximum_tangent_error,
        "reducedCandidate": audit,
        "stepHalvingMaximumRelativeDifferences": convergence,
        "statement": (
            "the reduced ODE is the tangent projection on the central support; "
            "it is not the full Navier--Stokes evolution"
        ),
    }


def main() -> None:
    print(json.dumps(validate(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
