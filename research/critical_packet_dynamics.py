#!/usr/bin/env python3
"""Short-time Fourier--Galerkin audit for the R0.4 critical packet.

This is a finite-dimensional numerical experiment, not a regularity proof.
The state uses Fourier-series coefficients b_k in the rescaled equation

    b'_k = -nu |k/N|^2 b_k + (rho/N^4) P_k (b x curl b)_k.

The rotational form, Leray projection, symmetric cutoff, and 2/3 dealiasing
make the inviscid L2 cancellation directly auditable.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass

import numpy as np


CENTERS = np.asarray(
    [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [-1.0, -1.0, 0.0]],
)
AMPLITUDES = np.asarray(
    [
        [0.0, 1.0, -1.0 - 1.0j],
        [-1.0, 0.0, -1.0],
        [-1.0 - 1.0j, 1.0 + 1.0j, 1.0],
    ],
    dtype=np.complex128,
)


def smooth_bump(distance_squared: float, delta: float) -> float:
    normalized = distance_squared / delta**2
    if normalized >= 1.0:
        return 0.0
    return math.exp(1.0 - 1.0 / (1.0 - normalized))


def profile_at(
    frequency: np.ndarray,
    delta: float,
    amplitudes: np.ndarray = AMPLITUDES,
) -> np.ndarray:
    value = np.zeros(3, dtype=np.complex128)
    length_squared = float(np.dot(frequency, frequency))
    for center, amplitude in zip(CENTERS, amplitudes, strict=True):
        for sign in (1.0, -1.0):
            bump = smooth_bump(float(np.sum((frequency - sign * center) ** 2)), delta)
            if bump == 0.0:
                continue
            signed_amplitude = amplitude if sign > 0 else np.conjugate(amplitude)
            projected = signed_amplitude - frequency * (
                np.dot(frequency, signed_amplitude) / length_squared
            )
            value += bump * projected
    return value


def packet_coefficients(
    scale: int,
    delta: float,
    amplitudes: np.ndarray = AMPLITUDES,
) -> dict[tuple[int, int, int], np.ndarray]:
    radius = delta * scale
    candidates: set[tuple[int, int, int]] = set()
    for center in CENTERS.astype(int):
        for sign in (1, -1):
            lattice_center = sign * scale * center
            lower = np.ceil(lattice_center - radius).astype(int)
            upper = np.floor(lattice_center + radius).astype(int)
            for k0 in range(lower[0], upper[0] + 1):
                for k1 in range(lower[1], upper[1] + 1):
                    for k2 in range(lower[2], upper[2] + 1):
                        candidates.add((k0, k1, k2))

    records: dict[tuple[int, int, int], np.ndarray] = {}
    for wavevector in sorted(candidates):
        coefficient = profile_at(
            np.asarray(wavevector, dtype=float) / scale,
            delta,
            amplitudes,
        )
        if np.vdot(coefficient, coefficient).real > 0.0:
            records[wavevector] = coefficient
    return records


@dataclass
class SpectralSystem:
    scale: int
    delta: float
    grid: int
    cutoff: int
    viscosity: float
    rho: float
    amplitudes: np.ndarray | None = None

    def __post_init__(self) -> None:
        if 3 * self.cutoff >= self.grid:
            raise ValueError("grid must exceed three times the component cutoff")
        frequencies = np.rint(np.fft.fftfreq(self.grid) * self.grid).astype(int)
        self.kx = frequencies[:, None, None]
        self.ky = frequencies[None, :, None]
        self.kz = frequencies[None, None, :]
        self.k_squared = self.kx**2 + self.ky**2 + self.kz**2
        self.k_magnitude = np.sqrt(self.k_squared)
        self.mask = (
            (np.abs(self.kx) <= self.cutoff)
            & (np.abs(self.ky) <= self.cutoff)
            & (np.abs(self.kz) <= self.cutoff)
        )
        self.mask &= self.k_squared > 0
        self.negative_indices = (-np.arange(self.grid)) % self.grid
        self.initial_support = np.zeros((self.grid, self.grid, self.grid), dtype=bool)

    def project(self, vector: np.ndarray) -> np.ndarray:
        dot = self.kx * vector[0] + self.ky * vector[1] + self.kz * vector[2]
        inverse = np.zeros_like(self.k_squared, dtype=float)
        np.divide(1.0, self.k_squared, out=inverse, where=self.k_squared > 0)
        projected = vector.copy()
        projected[0] -= self.kx * dot * inverse
        projected[1] -= self.ky * dot * inverse
        projected[2] -= self.kz * dot * inverse
        projected *= self.mask[None, ...]
        return projected

    def enforce_reality(self, vector: np.ndarray) -> np.ndarray:
        opposite = np.take(vector, self.negative_indices, axis=1)
        opposite = np.take(opposite, self.negative_indices, axis=2)
        opposite = np.take(opposite, self.negative_indices, axis=3)
        return self.project(0.5 * (vector + np.conjugate(opposite)))

    def initial_state(self) -> np.ndarray:
        state = np.zeros((3, self.grid, self.grid, self.grid), dtype=np.complex128)
        amplitudes = AMPLITUDES if self.amplitudes is None else self.amplitudes
        records = packet_coefficients(self.scale, self.delta, amplitudes)
        for wavevector, coefficient in records.items():
            if max(abs(component) for component in wavevector) > self.cutoff:
                raise ValueError(f"initial mode {wavevector} lies outside the cutoff")
            index = tuple(component % self.grid for component in wavevector)
            state[(slice(None),) + index] = coefficient
            self.initial_support[index] = True
        return self.enforce_reality(state)

    def rotational_nonlinearity(self, state: np.ndarray) -> np.ndarray:
        normalization = float(self.grid**3)
        velocity = np.fft.ifftn(normalization * state, axes=(-3, -2, -1))
        curl_coefficients = np.empty_like(state)
        curl_coefficients[0] = 1.0j * (self.ky * state[2] - self.kz * state[1])
        curl_coefficients[1] = 1.0j * (self.kz * state[0] - self.kx * state[2])
        curl_coefficients[2] = 1.0j * (self.kx * state[1] - self.ky * state[0])
        vorticity = np.fft.ifftn(
            normalization * curl_coefficients,
            axes=(-3, -2, -1),
        )
        cross_product = np.empty_like(velocity)
        cross_product[0] = velocity[1] * vorticity[2] - velocity[2] * vorticity[1]
        cross_product[1] = velocity[2] * vorticity[0] - velocity[0] * vorticity[2]
        cross_product[2] = velocity[0] * vorticity[1] - velocity[1] * vorticity[0]
        coefficients = np.fft.fftn(cross_product, axes=(-3, -2, -1)) / normalization
        return self.project(coefficients)

    def rhs(self, state: np.ndarray) -> np.ndarray:
        linear = -(self.viscosity / self.scale**2) * self.k_squared * state
        nonlinear = (self.rho / self.scale**4) * self.rotational_nonlinearity(state)
        return linear + nonlinear

    def rk4_step(self, state: np.ndarray, step: float) -> np.ndarray:
        k1 = self.rhs(state)
        k2 = self.rhs(state + 0.5 * step * k1)
        k3 = self.rhs(state + 0.5 * step * k2)
        k4 = self.rhs(state + step * k3)
        advanced = state + (step / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        return self.enforce_reality(advanced)

    def diagnostics(self, state: np.ndarray, initial: np.ndarray, tau: float) -> dict[str, float]:
        nonlinear = self.rotational_nonlinearity(state)
        coefficient_size = np.sum(np.abs(state) ** 2, axis=0)
        h_half_squared = float(np.sum(self.k_magnitude * coefficient_size))
        h_three_half_squared = float(np.sum(self.k_magnitude**3 * coefficient_size))
        transfer = -float(
            np.real(np.sum(self.k_magnitude[None, ...] * np.conjugate(state) * nonlinear))
        )
        l2_pairing = float(np.real(np.vdot(state, nonlinear)))
        nonlinear_viscous_ratio = (
            self.rho * (-transfer) / (self.viscosity * self.scale**2 * h_three_half_squared)
        )
        outside_h_half = float(
            np.sum(self.k_magnitude[~self.initial_support] * coefficient_size[~self.initial_support])
        )
        heat_reference = initial * np.exp(
            -self.viscosity * tau * self.k_squared / self.scale**2
        )[None, ...]
        heat_energy = float(
            np.sum(self.k_magnitude * np.sum(np.abs(heat_reference) ** 2, axis=0))
        )
        alignment_numerator = float(
            np.real(
                np.sum(
                    self.k_magnitude[None, ...]
                    * np.conjugate(heat_reference)
                    * state
                )
            )
        )
        phase_alignment = alignment_numerator / math.sqrt(heat_energy * h_half_squared)
        dot = self.kx * state[0] + self.ky * state[1] + self.kz * state[2]
        divergence_residual = float(np.max(np.abs(dot)))
        opposite = np.take(state, self.negative_indices, axis=1)
        opposite = np.take(opposite, self.negative_indices, axis=2)
        opposite = np.take(opposite, self.negative_indices, axis=3)
        reality_residual = float(np.max(np.abs(opposite - np.conjugate(state))))
        active = coefficient_size > 1e-24
        return {
            "tau": tau,
            "hHalfSquared": h_half_squared,
            "hThreeHalfSquared": h_three_half_squared,
            "transfer": transfer,
            "criticalRatio": abs(transfer)
            / (math.sqrt(h_half_squared) * h_three_half_squared),
            "nonlinearViscousRatio": nonlinear_viscous_ratio,
            "outsideHHalfFraction": outside_h_half / h_half_squared,
            "heatPhaseAlignment": phase_alignment,
            "activeModeCount": int(np.count_nonzero(active)),
            "l2SkewResidual": abs(l2_pairing),
            "divergenceResidual": divergence_residual,
            "realityResidual": reality_residual,
        }


def evolve(
    *,
    scale: int,
    delta: float,
    grid: int,
    cutoff: int,
    viscosity: float,
    gamma: float,
    step: float,
    final_time: float,
    checkpoints: list[float],
    amplitudes: np.ndarray | None = None,
) -> dict[str, object]:
    calibration = SpectralSystem(
        scale,
        delta,
        grid,
        cutoff,
        viscosity,
        rho=1.0,
        amplitudes=amplitudes,
    )
    initial = calibration.initial_state()
    initial_nonlinear = calibration.rotational_nonlinearity(initial)
    size = np.sum(np.abs(initial) ** 2, axis=0)
    initial_dissipation = float(np.sum(calibration.k_magnitude**3 * size))
    initial_transfer = -float(
        np.real(
            np.sum(
                calibration.k_magnitude[None, ...]
                * np.conjugate(initial)
                * initial_nonlinear
            )
        )
    )
    if initial_transfer >= 0:
        raise RuntimeError("the selected packet does not inject H^{1/2} energy")
    critical_amplitude = (
        viscosity * scale**2 * initial_dissipation / (-initial_transfer)
    )
    rho = gamma * critical_amplitude
    system = SpectralSystem(
        scale,
        delta,
        grid,
        cutoff,
        viscosity,
        rho,
        amplitudes=amplitudes,
    )
    state = system.initial_state()
    initial = state.copy()
    trajectory = [system.diagnostics(state, initial, 0.0)]
    checkpoint_steps = {round(value / step): value for value in checkpoints}
    total_steps = round(final_time / step)
    if not math.isclose(total_steps * step, final_time, abs_tol=1e-12):
        raise ValueError("final time must be an integer multiple of the time step")
    for index in range(1, total_steps + 1):
        state = system.rk4_step(state, step)
        if index in checkpoint_steps:
            trajectory.append(system.diagnostics(state, initial, checkpoint_steps[index]))

    return {
        "parameters": {
            "scale": scale,
            "delta": delta,
            "grid": grid,
            "componentCutoff": cutoff,
            "viscosity": viscosity,
            "gamma": gamma,
            "rho": rho,
            "criticalAmplitude": critical_amplitude,
            "timeStep": step,
            "finalTime": final_time,
            "initialModeCount": len(
                packet_coefficients(
                    scale,
                    delta,
                    AMPLITUDES if amplitudes is None else amplitudes,
                )
            ),
        },
        "trajectory": trajectory,
    }


def relative_difference(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1e-300)


def run_audit() -> dict[str, object]:
    common = {
        "scale": 10,
        "delta": 0.12,
        "cutoff": 15,
        "viscosity": 1.0,
        "final_time": 0.1,
        "checkpoints": [0.00125, 0.0025, 0.005, 0.01, 0.025, 0.05, 0.1],
    }
    reference = evolve(grid=48, gamma=1.2, step=0.00125, **common)
    smaller_step = evolve(grid=48, gamma=1.2, step=0.000625, **common)
    larger_grid = evolve(grid=64, gamma=1.2, step=0.00125, **common)
    smaller_cutoff = evolve(
        grid=48,
        gamma=1.2,
        step=0.00125,
        **{**common, "cutoff": 13},
    )
    subcritical = evolve(grid=48, gamma=0.5, step=0.00125, **common)
    ref_end = reference["trajectory"][-1]
    step_end = smaller_step["trajectory"][-1]
    grid_end = larger_grid["trajectory"][-1]
    cutoff_end = smaller_cutoff["trajectory"][-1]
    compared_fields = [
        "hHalfSquared",
        "transfer",
        "outsideHHalfFraction",
        "heatPhaseAlignment",
    ]
    return {
        "statement": "finite-dimensional dealiased Fourier--Galerkin audit; not a PDE proof",
        "reference": reference,
        "subcritical": subcritical,
        "convergence": {
            "timeStepHalvingRelativeDifferences": {
                field: relative_difference(ref_end[field], step_end[field])
                for field in compared_fields
            },
            "gridEmbeddingRelativeDifferences": {
                field: relative_difference(ref_end[field], grid_end[field])
                for field in compared_fields
            },
            "cutoff13Versus15RelativeDifferences": {
                field: relative_difference(ref_end[field], cutoff_end[field])
                for field in compared_fields
            },
            "smallerStepEndpoint": step_end,
            "largerGridEndpoint": grid_end,
            "smallerCutoffEndpoint": cutoff_end,
        },
    }


def validate(audit: dict[str, object]) -> None:
    reference = audit["reference"]
    trajectory = reference["trajectory"]
    initial = trajectory[0]
    endpoint = trajectory[-1]
    assert abs(initial["nonlinearViscousRatio"] - 1.2) < 1e-12
    assert endpoint["outsideHHalfFraction"] > 0.0
    assert endpoint["heatPhaseAlignment"] < 1.0
    assert endpoint["heatPhaseAlignment"] > 0.0
    for snapshot in trajectory:
        assert snapshot["divergenceResidual"] < 1e-9
        assert snapshot["realityResidual"] < 1e-9
        assert snapshot["l2SkewResidual"] < 1e-8
    convergence = audit["convergence"]
    assert max(convergence["timeStepHalvingRelativeDifferences"].values()) < 1e-4
    assert max(convergence["gridEmbeddingRelativeDifferences"].values()) < 2e-10
    cutoff = convergence["cutoff13Versus15RelativeDifferences"]
    assert cutoff["hHalfSquared"] < 0.01
    assert cutoff["outsideHHalfFraction"] < 0.01
    assert cutoff["heatPhaseAlignment"] < 0.01


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-validate", action="store_true")
    args = parser.parse_args()
    audit = run_audit()
    if not args.no_validate:
        validate(audit)
    print(json.dumps(audit, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
