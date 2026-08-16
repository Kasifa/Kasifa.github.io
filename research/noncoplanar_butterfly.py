#!/usr/bin/env python3
"""Minimal non-coplanar triad butterfly and short-time Galerkin audit.

The five unsigned wavevectors are

    a=(1,0,0), b=(0,1,0), c=(-1,-1,0),
    d=(0,0,1), e=(-1,0,-1).

They form the two triads a+b+c=0 and a+d+e=0.  The triads share only a,
so their union spans three dimensions.  A four-real-parameter polarization is

    u_a=(0,A,B),       u_b=(A,0,B),       u_c=(0,0,-i C),
    u_d=(B,A,0),       u_e=(0,-i D,0),

with conjugate coefficients at the negative wavevectors.  The closed formulas
in ``closed_form_diagnostics`` are algebraic.  The time integrations are
finite-dimensional, dealiased Fourier--Galerkin calculations and are not PDE
error estimates or regularity results.
"""

from __future__ import annotations

import json
import math

import numpy as np

from critical_packet_dynamics import SpectralSystem
from triad_leakage_variation import bilinear, hhalf_pairing


SQRT2 = math.sqrt(2.0)
SQRT3 = math.sqrt(3.0)
SQRT5 = math.sqrt(5.0)
SQRT6 = math.sqrt(6.0)

A_MODE = (1, 0, 0)
B_MODE = (0, 1, 0)
C_MODE = (-1, -1, 0)
D_MODE = (0, 0, 1)
E_MODE = (-1, 0, -1)
CENTERS = [A_MODE, B_MODE, C_MODE, D_MODE, E_MODE]


def negate(wavevector: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(-component for component in wavevector)


def butterfly_field(
    horizontal: float,
    transverse: float,
    first_closing: float,
    second_closing: float,
) -> dict[tuple[int, int, int], np.ndarray]:
    """Return the real divergence-free butterfly field."""

    amplitudes = [
        np.asarray([0.0, horizontal, transverse], dtype=np.complex128),
        np.asarray([horizontal, 0.0, transverse], dtype=np.complex128),
        np.asarray([0.0, 0.0, -1.0j * first_closing], dtype=np.complex128),
        np.asarray([transverse, horizontal, 0.0], dtype=np.complex128),
        np.asarray([0.0, -1.0j * second_closing, 0.0], dtype=np.complex128),
    ]
    field: dict[tuple[int, int, int], np.ndarray] = {}
    for wavevector, coefficient in zip(CENTERS, amplitudes, strict=True):
        field[wavevector] = coefficient
        field[negate(wavevector)] = np.conjugate(coefficient)
    return field


def vorticity_field(
    field: dict[tuple[int, int, int], np.ndarray],
) -> dict[tuple[int, int, int], np.ndarray]:
    return {
        wavevector: 1.0j
        * np.cross(np.asarray(wavevector, dtype=float), coefficient)
        for wavevector, coefficient in field.items()
    }


def stretching_components_direct(
    field: dict[tuple[int, int, int], np.ndarray],
) -> np.ndarray:
    """Return integral averages of omega_j (omega dot grad) u_j."""

    vorticity = vorticity_field(field)
    stretching: dict[tuple[int, int, int], np.ndarray] = {}
    for p, omega_p in vorticity.items():
        for q, velocity_q in field.items():
            output = tuple(p[axis] + q[axis] for axis in range(3))
            if output == (0, 0, 0):
                continue
            contribution = 1.0j * np.dot(q, omega_p) * velocity_q
            stretching[output] = stretching.get(
                output,
                np.zeros(3, dtype=np.complex128),
            ) + contribution

    components = np.zeros(3)
    for wavevector, omega_k in vorticity.items():
        coefficient = stretching.get(
            wavevector,
            np.zeros(3, dtype=np.complex128),
        )
        components += np.real(np.conjugate(omega_k) * coefficient)
    return components


def closed_form_diagnostics(
    horizontal: float,
    transverse: float,
    first_closing: float,
    second_closing: float,
) -> dict[str, object]:
    """Return exact scalar formulas for the four-parameter polarization."""

    horizontal_squared = horizontal**2
    transverse_squared = transverse**2
    first_squared = first_closing**2
    second_squared = second_closing**2
    base = horizontal_squared + transverse_squared
    closing = first_squared + second_squared
    mixed_base = base - horizontal * transverse
    mixed_closing = 2.0 * closing - first_closing * second_closing

    energy = 6.0 * base + 2.0 * SQRT2 * closing
    h_three_half_squared = 6.0 * base + 4.0 * SQRT2 * closing
    enstrophy = 6.0 * base + 4.0 * closing
    transfer = (
        4.0
        * (SQRT2 - 1.0)
        * horizontal
        * transverse
        * (first_closing + second_closing)
    )
    stretching_components = np.asarray(
        [
            -2.0
            * horizontal
            * transverse
            * (first_closing + second_closing),
            -2.0 * horizontal * transverse * first_closing,
            -2.0 * horizontal * transverse * second_closing,
        ]
    )
    outside_squared = (
        4.0 * SQRT2 * (horizontal**4 + transverse**4)
        + 4.0 * SQRT3 / 3.0 * mixed_base * mixed_closing
        + 4.0
        * SQRT5
        * (horizontal_squared * first_squared + transverse_squared * second_squared)
        + 8.0 * SQRT6 / 3.0 * first_squared * second_squared
    )
    return {
        "hHalfSquared": energy,
        "hThreeHalfSquared": h_three_half_squared,
        "enstrophy": enstrophy,
        "hHalfTransfer": transfer,
        "stretchingComponents": stretching_components.tolist(),
        "totalStretching": float(np.sum(stretching_components)),
        "horizontalStretching": float(np.sum(stretching_components[:2])),
        "outsideSquared": outside_squared,
    }


def direct_diagnostics(
    horizontal: float,
    transverse: float,
    first_closing: float,
    second_closing: float,
) -> dict[str, object]:
    field = butterfly_field(
        horizontal,
        transverse,
        first_closing,
        second_closing,
    )
    nonlinear = bilinear(field, field)
    support = set(field)
    outside = set(nonlinear).difference(support)
    h_three_half_squared = float(
        sum(
            np.linalg.norm(wavevector) ** 3
            * np.vdot(coefficient, coefficient).real
            for wavevector, coefficient in field.items()
        )
    )
    enstrophy = float(
        sum(
            np.dot(wavevector, wavevector)
            * np.vdot(coefficient, coefficient).real
            for wavevector, coefficient in field.items()
        )
    )
    components = stretching_components_direct(field)
    return {
        "hHalfSquared": hhalf_pairing(field, field),
        "hThreeHalfSquared": h_three_half_squared,
        "enstrophy": enstrophy,
        "hHalfTransfer": hhalf_pairing(field, nonlinear, support),
        "stretchingComponents": components.tolist(),
        "totalStretching": float(np.sum(components)),
        "horizontalStretching": float(np.sum(components[:2])),
        "outsideSquared": hhalf_pairing(nonlinear, nonlinear, outside),
    }


def representative(wavevector: tuple[int, int, int]) -> bool:
    for component in wavevector:
        if component != 0:
            return component > 0
    return False


def triad_relations() -> list[dict[str, object]]:
    records = []
    for first in range(len(CENTERS)):
        for second in range(first + 1, len(CENTERS)):
            for third in range(second + 1, len(CENTERS)):
                chosen = [CENTERS[first], CENTERS[second], CENTERS[third]]
                for signs in (
                    (-1, -1, -1),
                    (-1, -1, 1),
                    (-1, 1, -1),
                    (-1, 1, 1),
                    (1, -1, -1),
                    (1, -1, 1),
                    (1, 1, -1),
                    (1, 1, 1),
                ):
                    total = tuple(
                        sum(signs[index] * chosen[index][axis] for index in range(3))
                        for axis in range(3)
                    )
                    if total == (0, 0, 0):
                        normalized_signs = signs
                        if next(sign for sign in signs if sign != 0) < 0:
                            normalized_signs = tuple(-sign for sign in signs)
                        record = {
                            "indices": [first, second, third],
                            "signs": list(normalized_signs),
                        }
                        if record not in records:
                            records.append(record)
    records.sort(key=lambda record: record["indices"])
    return records


def outside_mode_records(
    horizontal: float,
    transverse: float,
    first_closing: float,
    second_closing: float,
) -> list[dict[str, object]]:
    field = butterfly_field(
        horizontal,
        transverse,
        first_closing,
        second_closing,
    )
    nonlinear = bilinear(field, field)
    records = []
    for wavevector, coefficient in sorted(nonlinear.items()):
        if wavevector in field or not representative(wavevector):
            continue
        size = float(np.vdot(coefficient, coefficient).real)
        if size < 1e-28:
            continue
        records.append(
            {
                "wavevectorPair": [wavevector, negate(wavevector)],
                "coefficient": [
                    [float(value.real), float(value.imag)] for value in coefficient
                ],
                "pairHHalfContribution": 2.0
                * np.linalg.norm(wavevector)
                * size,
            }
        )
    return records


def normalized_symmetric_candidate() -> tuple[float, float, float, float]:
    amplitude = 1.0 / math.sqrt(12.0 + 4.0 * SQRT2)
    return amplitude, -amplitude, amplitude, amplitude


def state_from_candidate(
    system: SpectralSystem,
    parameters: tuple[float, float, float, float],
) -> np.ndarray:
    state = np.zeros(
        (3, system.grid, system.grid, system.grid),
        dtype=np.complex128,
    )
    for wavevector, coefficient in butterfly_field(*parameters).items():
        index = tuple(component % system.grid for component in wavevector)
        state[(slice(None),) + index] = coefficient
        system.initial_support[index] = True
    return system.enforce_reality(state)


def component_stretching_spectral(
    system: SpectralSystem,
    state: np.ndarray,
) -> dict[str, object]:
    normalization = float(system.grid**3)
    vorticity = np.empty_like(state)
    vorticity[0] = 1.0j * (system.ky * state[2] - system.kz * state[1])
    vorticity[1] = 1.0j * (system.kz * state[0] - system.kx * state[2])
    vorticity[2] = 1.0j * (system.kx * state[1] - system.ky * state[0])
    physical_vorticity = np.fft.ifftn(
        normalization * vorticity,
        axes=(-3, -2, -1),
    )
    frequencies = [system.kx, system.ky, system.kz]
    stretching = np.empty_like(state)
    for component in range(3):
        physical_component = np.zeros_like(physical_vorticity[0])
        for derivative in range(3):
            velocity_derivative = np.fft.ifftn(
                normalization
                * (1.0j * frequencies[derivative] * state[component]),
                axes=(-3, -2, -1),
            )
            physical_component += (
                physical_vorticity[derivative] * velocity_derivative
            )
        stretching[component] = np.fft.fftn(
            physical_component,
            axes=(-3, -2, -1),
        ) / normalization

    component_pairing = np.real(
        np.sum(np.conjugate(vorticity) * stretching, axis=(1, 2, 3))
    )
    mode_pairing = np.real(
        np.sum(np.conjugate(vorticity) * stretching, axis=0)
    )
    return {
        "components": component_pairing.tolist(),
        "total": float(np.sum(component_pairing)),
        "horizontal": float(np.sum(component_pairing[:2])),
        "initialSupport": float(np.sum(mode_pairing[system.initial_support])),
        "generated": float(np.sum(mode_pairing[~system.initial_support])),
    }


def spectral_snapshot(
    system: SpectralSystem,
    state: np.ndarray,
    time: float,
) -> dict[str, object]:
    rotational = system.rotational_nonlinearity(state)
    coefficient_size = np.sum(np.abs(state) ** 2, axis=0)
    h_half = float(np.sum(system.k_magnitude * coefficient_size))
    h_three_half = float(np.sum(system.k_magnitude**3 * coefficient_size))
    enstrophy = float(np.sum(system.k_squared * coefficient_size))
    h_two = float(np.sum(system.k_squared**2 * coefficient_size))
    h_half_mode_growth = np.real(
        np.sum(
            system.k_magnitude[None, ...]
            * np.conjugate(state)
            * rotational,
            axis=0,
        )
    )
    h_half_growth = float(np.sum(h_half_mode_growth))
    stretching = component_stretching_spectral(system, state)
    outside_size = float(
        np.sum(
            system.k_magnitude[~system.initial_support]
            * coefficient_size[~system.initial_support]
        )
    )
    normal_size = np.sum(np.abs(rotational) ** 2, axis=0)
    dot = system.kx * state[0] + system.ky * state[1] + system.kz * state[2]
    opposite = np.take(state, system.negative_indices, axis=1)
    opposite = np.take(opposite, system.negative_indices, axis=2)
    opposite = np.take(opposite, system.negative_indices, axis=3)
    return {
        "time": time,
        "hHalfSquared": h_half,
        "hThreeHalfSquared": h_three_half,
        "enstrophy": enstrophy,
        "hTwoSquared": h_two,
        "hHalfGrowth": h_half_growth,
        "initialSupportHHalfGrowth": float(
            np.sum(h_half_mode_growth[system.initial_support])
        ),
        "generatedHHalfGrowth": float(
            np.sum(h_half_mode_growth[~system.initial_support])
        ),
        "halfHHalfNetRate": (
            -system.viscosity * h_three_half + system.rho * h_half_growth
        ),
        "stretching": stretching,
        "halfEnstrophyNetRate": (
            -system.viscosity * h_two + system.rho * stretching["total"]
        ),
        "outsideHHalfFraction": outside_size / h_half,
        "normalForcingSquared": float(
            np.sum(
                system.k_magnitude[~system.initial_support]
                * normal_size[~system.initial_support]
            )
        ),
        "activeModeCount": int(np.count_nonzero(coefficient_size > 1e-24)),
        "l2SkewResidual": abs(float(np.real(np.vdot(state, rotational)))),
        "divergenceResidual": float(np.max(np.abs(dot))),
        "realityResidual": float(
            np.max(np.abs(opposite - np.conjugate(state)))
        ),
    }


def interpolate_crossing(
    previous: dict[str, object],
    current: dict[str, object],
    field: str,
) -> tuple[float, float]:
    previous_value = float(previous[field])
    current_value = float(current[field])
    fraction = previous_value / (previous_value - current_value)
    time = float(previous["time"]) + fraction * (
        float(current["time"]) - float(previous["time"])
    )
    energy = float(previous["hHalfSquared"]) + fraction * (
        float(current["hHalfSquared"]) - float(previous["hHalfSquared"])
    )
    return time, energy


def evolve(
    *,
    projected: bool,
    grid: int,
    cutoff: int,
    step: float,
    final_time: float,
    rho: float,
    checkpoints: list[float],
) -> dict[str, object]:
    system = SpectralSystem(
        scale=1,
        delta=0.0,
        grid=grid,
        cutoff=cutoff,
        viscosity=1.0,
        rho=rho,
    )
    state = state_from_candidate(system, normalized_symmetric_candidate())
    support_mask = system.initial_support[None, ...]

    def rhs(value: np.ndarray) -> np.ndarray:
        output = system.rhs(value)
        if projected:
            output *= support_mask
        return output

    def advance(value: np.ndarray) -> np.ndarray:
        first = rhs(value)
        second = rhs(value + 0.5 * step * first)
        third = rhs(value + 0.5 * step * second)
        fourth = rhs(value + step * third)
        output = value + step * (first + 2.0 * second + 2.0 * third + fourth) / 6.0
        output = system.enforce_reality(output)
        if projected:
            output *= support_mask
        return output

    current = spectral_snapshot(system, state, 0.0)
    cumulative_components = np.zeros(3)
    cumulative_h_half_growth = 0.0
    current["cumulativeScaledStretchingComponents"] = cumulative_components.tolist()
    current["cumulativeScaledHHalfGrowth"] = cumulative_h_half_growth
    trajectory = [current.copy()]
    checkpoint_steps = {round(time / step): time for time in checkpoints}
    total_steps = round(final_time / step)
    if not math.isclose(total_steps * step, final_time, abs_tol=1e-12):
        raise ValueError("final time must be an integer multiple of the time step")
    peak = None
    original_support_crossing = None

    for index in range(1, total_steps + 1):
        previous = current
        state = advance(state)
        time = index * step
        current = spectral_snapshot(system, state, time)
        previous_components = np.asarray(previous["stretching"]["components"])
        current_components = np.asarray(current["stretching"]["components"])
        cumulative_components += (
            0.5 * system.rho * step * (previous_components + current_components)
        )
        cumulative_h_half_growth += (
            0.5
            * system.rho
            * step
            * (float(previous["hHalfGrowth"]) + float(current["hHalfGrowth"]))
        )
        current["cumulativeScaledStretchingComponents"] = (
            cumulative_components.tolist()
        )
        current["cumulativeScaledHHalfGrowth"] = cumulative_h_half_growth

        if (
            peak is None
            and float(previous["halfHHalfNetRate"]) > 0.0
            and float(current["halfHHalfNetRate"]) <= 0.0
        ):
            peak_time, peak_energy = interpolate_crossing(
                previous,
                current,
                "halfHHalfNetRate",
            )
            peak = {"time": peak_time, "hHalfSquared": peak_energy}
        if (
            original_support_crossing is None
            and float(previous["initialSupportHHalfGrowth"]) > 0.0
            and float(current["initialSupportHHalfGrowth"]) <= 0.0
        ):
            crossing_time, _ = interpolate_crossing(
                previous,
                current,
                "initialSupportHHalfGrowth",
            )
            original_support_crossing = crossing_time
        if index in checkpoint_steps:
            saved = current.copy()
            saved["time"] = checkpoint_steps[index]
            trajectory.append(saved)

    if peak is None:
        raise RuntimeError("the H^(1/2) peak was not bracketed")
    return {
        "parameters": {
            "projected": projected,
            "grid": grid,
            "componentCutoff": cutoff,
            "timeStep": step,
            "finalTime": final_time,
            "viscosity": system.viscosity,
            "rho": system.rho,
        },
        "trajectory": trajectory,
        "hHalfPeak": peak,
        "initialSupportGrowthSignChangeTime": original_support_crossing,
    }


def relative_difference(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1e-300)


def comparison(reference: dict[str, object], other: dict[str, object]) -> dict[str, float]:
    reference_end = reference["trajectory"][-1]
    other_end = other["trajectory"][-1]
    fields = [
        "hHalfSquared",
        "hThreeHalfSquared",
        "hHalfGrowth",
        "outsideHHalfFraction",
        "cumulativeScaledHHalfGrowth",
    ]
    result = {
        field: relative_difference(
            float(reference_end[field]),
            float(other_end[field]),
        )
        for field in fields
    }
    result["totalStretching"] = relative_difference(
        float(reference_end["stretching"]["total"]),
        float(other_end["stretching"]["total"]),
    )
    result["cumulativeHorizontalStretching"] = relative_difference(
        sum(reference_end["cumulativeScaledStretchingComponents"][:2]),
        sum(other_end["cumulativeScaledStretchingComponents"][:2]),
    )
    result["peakTime"] = relative_difference(
        float(reference["hHalfPeak"]["time"]),
        float(other["hHalfPeak"]["time"]),
    )
    result["peakEnergy"] = relative_difference(
        float(reference["hHalfPeak"]["hHalfSquared"]),
        float(other["hHalfPeak"]["hHalfSquared"]),
    )
    return result


def run_audit() -> dict[str, object]:
    random = np.random.default_rng(20260816)
    maximum_formula_error = 0.0
    for _ in range(1000):
        parameters = random.normal(size=4)
        closed = closed_form_diagnostics(*parameters)
        direct = direct_diagnostics(*parameters)
        scalar_fields = [
            "hHalfSquared",
            "hThreeHalfSquared",
            "enstrophy",
            "hHalfTransfer",
            "totalStretching",
            "horizontalStretching",
            "outsideSquared",
        ]
        for field in scalar_fields:
            scale = max(1.0, abs(float(closed[field])), abs(float(direct[field])))
            maximum_formula_error = max(
                maximum_formula_error,
                abs(float(closed[field]) - float(direct[field])) / scale,
            )
        maximum_formula_error = max(
            maximum_formula_error,
            float(
                np.max(
                    np.abs(
                        np.asarray(closed["stretchingComponents"])
                        - np.asarray(direct["stretchingComponents"])
                    )
                )
            ),
        )

    candidate_parameters = normalized_symmetric_candidate()
    candidate = closed_form_diagnostics(*candidate_parameters)
    critical_amplitude = float(candidate["hThreeHalfSquared"]) / -float(
        candidate["hHalfTransfer"]
    )
    rho = 1.2 * critical_amplitude
    common = {
        "final_time": 0.06,
        "rho": rho,
        "checkpoints": [0.005, 0.01, 0.025, 0.05, 0.0545, 0.06],
    }
    reference = evolve(
        projected=False,
        grid=28,
        cutoff=7,
        step=0.0005,
        **common,
    )
    projected = evolve(
        projected=True,
        grid=28,
        cutoff=7,
        step=0.0005,
        **common,
    )
    half_step = evolve(
        projected=False,
        grid=28,
        cutoff=7,
        step=0.00025,
        **common,
    )
    cutoff_six = evolve(
        projected=False,
        grid=24,
        cutoff=6,
        step=0.0005,
        **common,
    )
    cutoff_eight = evolve(
        projected=False,
        grid=28,
        cutoff=8,
        step=0.0005,
        **common,
    )
    grid_embedding = evolve(
        projected=False,
        grid=32,
        cutoff=7,
        step=0.0005,
        **common,
    )

    return {
        "statement": (
            "closed formulas are algebraic; time evolutions are dealiased "
            "finite Fourier--Galerkin audits, not PDE error estimates"
        ),
        "geometry": {
            "centers": CENTERS,
            "rank": int(np.linalg.matrix_rank(np.asarray(CENTERS, dtype=float))),
            "triadRelations": triad_relations(),
            "unsignedModeCount": len(CENTERS),
            "signedModeCount": 2 * len(CENTERS),
        },
        "closedFormula": {
            "randomSamples": 1000,
            "maximumRelativeOrAbsoluteError": maximum_formula_error,
        },
        "candidate": {
            "parameters": candidate_parameters,
            **candidate,
            "criticalAmplitude": critical_amplitude,
            "rho": rho,
            "initialHorizontalStretchingFraction": float(
                candidate["horizontalStretching"]
                / candidate["totalStretching"]
            ),
            "outsideModes": outside_mode_records(*candidate_parameters),
        },
        "fullGalerkin": reference,
        "supportProjected": projected,
        "convergence": {
            "timeStepHalving": comparison(reference, half_step),
            "cutoff6Versus7": comparison(reference, cutoff_six),
            "cutoff8Versus7": comparison(reference, cutoff_eight),
            "grid28Versus32Embedding": comparison(reference, grid_embedding),
        },
    }


def validate(audit: dict[str, object]) -> None:
    geometry = audit["geometry"]
    assert geometry["rank"] == 3
    assert geometry["unsignedModeCount"] == 5
    assert len(geometry["triadRelations"]) == 2
    assert audit["closedFormula"]["maximumRelativeOrAbsoluteError"] < 2e-14

    candidate = audit["candidate"]
    assert abs(candidate["hHalfSquared"] - 1.0) < 2e-15
    assert candidate["hHalfTransfer"] < 0.0
    assert candidate["totalStretching"] > 0.0
    assert abs(
        candidate["totalStretching"]
        + (SQRT2 + 1.0) * candidate["hHalfTransfer"]
    ) < 2e-15
    assert abs(candidate["initialHorizontalStretchingFraction"] - 0.75) < 2e-15
    assert candidate["outsideSquared"] > 0.0
    # The generic four-parameter family has ten representative outside pairs.
    # In the symmetric candidate A^2=B^2 cancels the (0,1,-1) pair.
    assert len(candidate["outsideModes"]) == 9

    reference = audit["fullGalerkin"]
    projected = audit["supportProjected"]
    initial = reference["trajectory"][0]
    at_five = next(
        snapshot
        for snapshot in reference["trajectory"]
        if math.isclose(snapshot["time"], 0.05)
    )
    assert abs(
        candidate["rho"] * initial["hHalfGrowth"]
        / initial["hThreeHalfSquared"]
        - 1.2
    ) < 2e-14
    assert reference["hHalfPeak"]["hHalfSquared"] > 1.09
    assert projected["hHalfPeak"]["hHalfSquared"] < 1.01
    assert reference["hHalfPeak"]["time"] > 3.0 * projected["hHalfPeak"]["time"]
    assert at_five["initialSupportHHalfGrowth"] < 0.0
    assert at_five["generatedHHalfGrowth"] > 0.0
    assert at_five["stretching"]["generated"] > at_five["stretching"]["initialSupport"]
    assert reference["initialSupportGrowthSignChangeTime"] is not None

    for evolution in (reference, projected):
        for snapshot in evolution["trajectory"]:
            assert snapshot["divergenceResidual"] < 2e-12
            assert snapshot["realityResidual"] < 2e-12
            assert snapshot["l2SkewResidual"] < 2e-12
            components = snapshot["stretching"]["components"]
            assert abs(components[1] - components[2]) < 2e-12

    convergence = audit["convergence"]
    # Instantaneous RK4 fields converge much faster; the cumulative quantities
    # use a trapezoidal time integral and therefore set the visible threshold.
    assert max(convergence["timeStepHalving"].values()) < 1.1e-5
    assert max(convergence["cutoff6Versus7"].values()) < 2e-3
    assert max(convergence["cutoff8Versus7"].values()) < 7e-4
    assert max(convergence["grid28Versus32Embedding"].values()) < 2e-12


def main() -> None:
    audit = run_audit()
    validate(audit)
    print(json.dumps(audit, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
