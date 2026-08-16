#!/usr/bin/env python3
"""Mode-by-mode transfer budget for the R0.6 dense candidate.

This is a finite Fourier--Galerkin diagnostic.  It separates contributions
from the plane k_z=0, from off-plane modes, and from the initial packet
support.  The calculation uses the same normalization and calibration as
``optimized_packet_dynamics.py``.
"""

from __future__ import annotations

import json
import math

import numpy as np

from critical_packet_dynamics import SpectralSystem
from optimized_packet_dynamics import FIXED_INJECTION_CANDIDATE


def representative(wavevector: tuple[int, int, int]) -> bool:
    for component in wavevector:
        if component != 0:
            return component > 0
    return False


def spectral_snapshot(
    system: SpectralSystem,
    state: np.ndarray,
    tau: float,
    top_count: int = 0,
) -> dict[str, object]:
    nonlinear = system.rotational_nonlinearity(state)
    component_transfer = -np.real(
        system.k_magnitude[None, ...] * np.conjugate(state) * nonlinear
    )
    mode_transfer = np.sum(component_transfer, axis=0)
    coefficient_size = np.sum(np.abs(state) ** 2, axis=0)
    weighted_energy = system.k_magnitude * coefficient_size
    plane = np.broadcast_to(system.kz == 0, system.k_squared.shape)
    off_plane = ~plane
    generated = ~system.initial_support
    total_energy = float(np.sum(weighted_energy))
    transfer = float(np.sum(mode_transfer))
    gradient_energy = float(np.sum(system.k_squared * coefficient_size))
    vertical_gradient_energy = float(
        np.sum(np.broadcast_to(system.kz**2, system.k_squared.shape) * coefficient_size)
    )
    snapshot: dict[str, object] = {
        "tau": tau,
        "hHalfSquared": total_energy,
        "transfer": transfer,
        "planeTransfer": float(np.sum(mode_transfer[plane])),
        "offPlaneTransfer": float(np.sum(mode_transfer[off_plane])),
        "initialSupportTransfer": float(
            np.sum(mode_transfer[system.initial_support])
        ),
        "generatedTransfer": float(np.sum(mode_transfer[generated])),
        "componentTransfer": [
            float(np.sum(component_transfer[axis])) for axis in range(3)
        ],
        "offPlaneHHalfFraction": float(
            np.sum(weighted_energy[off_plane]) / total_energy
        ),
        "verticalDerivativeFraction": vertical_gradient_energy / gradient_energy,
    }

    if top_count > 0:
        frequencies = np.rint(np.fft.fftfreq(system.grid) * system.grid).astype(int)
        records = []
        threshold = max(1e-14, 1e-12 * float(np.max(np.abs(mode_transfer))))
        for index_array in np.argwhere(np.abs(mode_transfer) > threshold):
            index = tuple(int(value) for value in index_array)
            wavevector = tuple(int(frequencies[value]) for value in index)
            if not representative(wavevector):
                continue
            opposite = tuple((-value) % system.grid for value in index)
            pair_transfer = float(mode_transfer[index] + mode_transfer[opposite])
            pair_energy = float(weighted_energy[index] + weighted_energy[opposite])
            records.append(
                {
                    "wavevectorPair": [wavevector, tuple(-value for value in wavevector)],
                    "transfer": pair_transfer,
                    "hHalfEnergy": pair_energy,
                    "plane": wavevector[2] == 0,
                    "initialSupport": bool(system.initial_support[index]),
                }
            )
        records.sort(key=lambda record: abs(record["transfer"]), reverse=True)
        snapshot["largestTransferPairs"] = records[:top_count]
    return snapshot


def calibrated_system(step: float) -> tuple[SpectralSystem, np.ndarray, float]:
    common = {
        "scale": 10,
        "delta": 0.12,
        "grid": 48,
        "cutoff": 15,
        "viscosity": 1.0,
        "amplitudes": FIXED_INJECTION_CANDIDATE,
    }
    calibration = SpectralSystem(rho=1.0, **common)
    initial = calibration.initial_state()
    nonlinear = calibration.rotational_nonlinearity(initial)
    coefficient_size = np.sum(np.abs(initial) ** 2, axis=0)
    dissipation = float(
        np.sum(calibration.k_magnitude**3 * coefficient_size)
    )
    transfer = -float(
        np.real(
            np.sum(
                calibration.k_magnitude[None, ...]
                * np.conjugate(initial)
                * nonlinear
            )
        )
    )
    critical_amplitude = common["viscosity"] * common["scale"] ** 2 * dissipation / (-transfer)
    system = SpectralSystem(rho=1.2 * critical_amplitude, **common)
    state = system.initial_state()
    return system, state, step


def run(step: float, detailed: bool) -> dict[str, object]:
    system, state, step = calibrated_system(step)
    final_time = 0.1
    selected_steps = {
        round(0.05 / step): 0.05,
        round(0.1 / step): 0.1,
    }
    initial = spectral_snapshot(system, state, 0.0, top_count=12 if detailed else 0)
    previous = initial
    sign_bracket = None
    selected = {"0.00000": initial}
    total_steps = round(final_time / step)
    for index in range(1, total_steps + 1):
        state = system.rk4_step(state, step)
        tau = index * step
        current = spectral_snapshot(
            system,
            state,
            tau,
            top_count=12 if detailed and index in selected_steps else 0,
        )
        if sign_bracket is None and previous["transfer"] < 0 <= current["transfer"]:
            fraction = -previous["transfer"] / (
                current["transfer"] - previous["transfer"]
            )
            crossing = previous["tau"] + fraction * step
            sign_bracket = {
                "interpolatedTime": crossing,
                "before": previous,
                "after": current,
            }
        if index in selected_steps:
            selected[f"{selected_steps[index]:.5f}"] = current
        previous = current
    if sign_bracket is None:
        raise RuntimeError("no transfer sign change found")
    return {
        "parameters": {
            "step": step,
            "rho": system.rho,
            "scale": system.scale,
            "delta": system.delta,
            "grid": system.grid,
            "cutoff": system.cutoff,
        },
        "selected": selected,
        "transferSignChange": sign_bracket,
    }


def validate() -> dict[str, object]:
    reference = run(step=0.00125, detailed=True)
    half_step = run(step=0.000625, detailed=False)
    at_five = reference["selected"]["0.05000"]
    assert abs(at_five["hHalfSquared"] - 293.1247816866135) < 2e-9
    assert abs(at_five["transfer"] + 167.84357039642487) < 2e-9
    for snapshot in reference["selected"].values():
        assert abs(
            snapshot["transfer"]
            - snapshot["planeTransfer"]
            - snapshot["offPlaneTransfer"]
        ) < 1e-10
        assert abs(
            snapshot["transfer"]
            - snapshot["initialSupportTransfer"]
            - snapshot["generatedTransfer"]
        ) < 1e-10
    crossing_difference = abs(
        reference["transferSignChange"]["interpolatedTime"]
        - half_step["transferSignChange"]["interpolatedTime"]
    )
    assert crossing_difference < 2e-4
    return {
        "reference": reference,
        "stepHalving": {
            "interpolatedSignChangeTime": half_step["transferSignChange"][
                "interpolatedTime"
            ],
            "absoluteDifference": crossing_difference,
        },
        "statement": (
            "finite-dimensional signed mode budget; categories partition the "
            "computed transfer but do not constitute a PDE error estimate"
        ),
    }


def main() -> None:
    print(json.dumps(validate(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
