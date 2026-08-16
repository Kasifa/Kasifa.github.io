#!/usr/bin/env python3
"""Dense cross-shell packet and exact first-Picard audit.

The two input centers and the target center are

    P = -c = (1, 1, 0),  Q = -e = (1, 0, 1),
    K = P + Q = (2, 1, 1) = M a.

Around +/-P and +/-Q this script places lattice balls of radius delta*N.
The Fourier coefficients have critical normalization N**-2 and are projected
separately onto each frequency's divergence-free plane.

The first Picard term is integrated exactly pair by pair:

    w(t) = - integral_0^t exp((t-s) Delta)
                     P[(exp(s Delta)u0 . grad) exp(s Delta)u0] ds.

This is a finite Fourier calculation.  The accompanying asymptotic formulas
are Riemann-sum and small-packet calculations; no nonlinear Picard remainder
is estimated here.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import math

import numpy as np


P_CENTER = np.asarray([1, 1, 0], dtype=np.int64)
Q_CENTER = np.asarray([1, 0, 1], dtype=np.int64)
K_CENTER = P_CENTER + Q_CENTER
H_DIRECTION = np.asarray([1, -1, -1], dtype=float)
A_POLARIZATION = 1.0j * np.asarray([0, 0, 1], dtype=np.complex128)
B_POLARIZATION = 1.0j * np.asarray([0, 1, 0], dtype=np.complex128)
VISCOSITY = 1.0
TAU_STAR = math.log(3.0 / 2.0) / 2.0
BALL_VOLUME = 4.0 * math.pi / 3.0
CONVOLUTION_SQUARE_INTEGRAL = 2176.0 * math.pi**3 / 2835.0
SMALL_DELTA_TARGET_CONSTANT = 136.0 * math.pi * math.sqrt(6.0) / 688905.0
TRANSPORTED_A_POLARIZATION = np.asarray([0, 1, -1], dtype=np.complex128)


@dataclass(frozen=True)
class Lobe:
    name: str
    center: np.ndarray
    polarization: np.ndarray


LOBES = (
    Lobe("P", P_CENTER, A_POLARIZATION),
    Lobe("Q", Q_CENTER, B_POLARIZATION),
    Lobe("-P", -P_CENTER, np.conjugate(A_POLARIZATION)),
    Lobe("-Q", -Q_CENTER, np.conjugate(B_POLARIZATION)),
)


def project_divergence_free(
    wavevectors: np.ndarray,
    amplitudes: np.ndarray,
) -> np.ndarray:
    """Apply the Leray matrix row by row."""

    vectors = np.asarray(wavevectors, dtype=float)
    values = np.asarray(amplitudes, dtype=np.complex128)
    if values.ndim == 1:
        values = np.broadcast_to(values, vectors.shape)
    squared = np.sum(vectors * vectors, axis=1)
    longitudinal = np.sum(vectors * values, axis=1) / squared
    return values - vectors * longitudinal[:, None]


def lattice_ball(radius: float) -> np.ndarray:
    bound = int(math.floor(radius))
    records = []
    threshold = radius**2 + 1e-12
    for first in range(-bound, bound + 1):
        for second in range(-bound, bound + 1):
            for third in range(-bound, bound + 1):
                if first**2 + second**2 + third**2 <= threshold:
                    records.append((first, second, third))
    return np.asarray(records, dtype=np.int64)


def central_kernel() -> dict[str, object]:
    raw_target = 1.0j * (
        np.dot(Q_CENTER, A_POLARIZATION) * B_POLARIZATION
        + np.dot(P_CENTER, B_POLARIZATION) * A_POLARIZATION
    )
    target = project_divergence_free(
        K_CENTER[None, :],
        raw_target[None, :],
    )[0]

    difference_center = P_CENTER - Q_CENTER
    raw_difference = 1.0j * (
        np.dot(-Q_CENTER, A_POLARIZATION) * np.conjugate(B_POLARIZATION)
        + np.dot(P_CENTER, np.conjugate(B_POLARIZATION)) * A_POLARIZATION
    )
    difference = project_divergence_free(
        difference_center[None, :],
        raw_difference[None, :],
    )[0]
    random = np.random.default_rng(20260816)
    rank_one_error = 0.0
    for _ in range(1000):
        alpha, gamma, beta, delta = (
            random.normal(size=4) + 1.0j * random.normal(size=4)
        )
        first = np.asarray([alpha, -alpha, gamma], dtype=np.complex128)
        second = np.asarray([beta, delta, -beta], dtype=np.complex128)
        raw = 1.0j * (
            np.dot(Q_CENTER, first) * second
            + np.dot(P_CENTER, second) * first
        )
        projected = project_divergence_free(K_CENTER[None, :], raw[None, :])[0]
        scalar = 1.0j * (
            4.0 * alpha * beta
            + beta * gamma
            + alpha * delta
            - 2.0 * gamma * delta
        ) / 3.0
        expected = scalar * H_DIRECTION
        rank_one_error = max(
            rank_one_error,
            float(np.max(np.abs(projected - expected))),
        )
    return {
        "P": P_CENTER.tolist(),
        "Q": Q_CENTER.tolist(),
        "K": K_CENTER.tolist(),
        "closureResidual": (P_CENTER + Q_CENTER - K_CENTER).tolist(),
        "targetRaw": [[float(value.real), float(value.imag)] for value in raw_target],
        "targetProjected": [
            [float(value.real), float(value.imag)] for value in target
        ],
        "targetProjectedSquared": float(np.vdot(target, target).real),
        "targetHDirectionImaginaryPairing": float(
            np.dot(H_DIRECTION, target).imag
        ),
        "differenceProjectedSquared": float(np.vdot(difference, difference).real),
        "rankOneRangeDirection": H_DIRECTION.astype(int).tolist(),
        "rankOneFormula": (
            "P_K i[(Q.A)B+(P.B)A] "
            "= i(4*alpha*beta+beta*gamma+alpha*delta-2*gamma*delta)"
            "/3 * (1,-1,-1)"
        ),
        "rankOneRandomMaximumError": rank_one_error,
        "transportedA1Polarization": [
            [float(value.real), float(value.imag)]
            for value in TRANSPORTED_A_POLARIZATION
        ],
        "rangeToTransportedPairing": [
            float(np.dot(H_DIRECTION, TRANSPORTED_A_POLARIZATION).real),
            float(np.dot(H_DIRECTION, TRANSPORTED_A_POLARIZATION).imag),
        ],
        "selfDerivativeP": [
            float(np.dot(P_CENTER, A_POLARIZATION).real),
            float(np.dot(P_CENTER, A_POLARIZATION).imag),
        ],
        "selfDerivativeQ": [
            float(np.dot(Q_CENTER, B_POLARIZATION).real),
            float(np.dot(Q_CENTER, B_POLARIZATION).imag),
        ],
    }


def heat_scalar(tau: float) -> float:
    output_squared = float(np.dot(K_CENTER, K_CENTER))
    input_squared = float(
        np.dot(P_CENTER, P_CENTER) + np.dot(Q_CENTER, Q_CENTER)
    )
    return (
        math.exp(-input_squared * tau) - math.exp(-output_squared * tau)
    ) / (output_squared - input_squared)


def small_delta_formula(delta: float, tau: float = TAU_STAR) -> dict[str, float]:
    input_leading = 4.0 * math.sqrt(2.0) * BALL_VOLUME * delta**3
    scalar = heat_scalar(tau)
    target_raw_leading = (
        2.0
        * math.sqrt(6.0)
        * (4.0 / 3.0)
        * scalar**2
        * CONVOLUTION_SQUARE_INTEGRAL
        * delta**9
    )
    normalized = target_raw_leading / input_leading**2
    return {
        "delta": delta,
        "tau": tau,
        "heatScalar": scalar,
        "inputEnergyLeading": input_leading,
        "targetRawEnergyLeading": target_raw_leading,
        "normalizedTargetLeading": normalized,
        "closedNormalizedTargetLeading": SMALL_DELTA_TARGET_CONSTANT * delta**3,
    }


def build_groups(N: int, delta: float) -> tuple[list[dict[str, object]], np.ndarray]:
    if not isinstance(N, int) or N < 1:
        raise ValueError("N must be a positive integer")
    if not 0.0 < delta < 0.25:
        raise ValueError("delta must lie in (0, 0.25)")

    displacements = lattice_ball(delta * N)
    groups = []
    normalization = N**-2
    for lobe in LOBES:
        wavevectors = N * lobe.center[None, :] + displacements
        coefficients = normalization * project_divergence_free(
            wavevectors,
            lobe.polarization,
        )
        groups.append(
            {
                "name": lobe.name,
                "wavevectors": wavevectors,
                "coefficients": coefficients,
                "squared": np.sum(wavevectors * wavevectors, axis=1),
            }
        )
    return groups, displacements


def input_diagnostics(
    groups: list[dict[str, object]],
) -> dict[str, float]:
    energy = 0.0
    divergence = 0.0
    lookup: dict[tuple[int, int, int], np.ndarray] = {}
    for group in groups:
        for wavevector, coefficient in zip(
            group["wavevectors"],
            group["coefficients"],
            strict=True,
        ):
            key = tuple(int(value) for value in wavevector)
            if key in lookup:
                raise AssertionError(f"overlapping input lobes at {key}")
            lookup[key] = coefficient
            energy += float(
                np.linalg.norm(wavevector)
                * np.vdot(coefficient, coefficient).real
            )
            divergence = max(
                divergence,
                float(abs(np.dot(wavevector, coefficient))),
            )

    reality = 0.0
    for wavevector, coefficient in lookup.items():
        opposite = tuple(-value for value in wavevector)
        reality = max(
            reality,
            float(np.max(np.abs(lookup[opposite] - np.conjugate(coefficient)))),
        )
    return {
        "modeCount": len(lookup),
        "hHalfSquared": energy,
        "divergenceResidual": divergence,
        "realityResidual": reality,
    }


def duhamel_factor(
    output_squared: np.ndarray,
    input_squared: np.ndarray,
    time: float,
    viscosity: float,
) -> np.ndarray:
    difference = output_squared - input_squared
    result = np.empty_like(difference, dtype=float)
    equal = difference == 0
    result[equal] = time * np.exp(-viscosity * output_squared[equal] * time)
    result[~equal] = (
        np.exp(-viscosity * input_squared[~equal] * time)
        - np.exp(-viscosity * output_squared[~equal] * time)
    ) / (viscosity * difference[~equal])
    return result


def accumulate_first_picard(
    groups: list[dict[str, object]],
    N: int,
    tau: float,
    viscosity: float,
) -> dict[tuple[int, int, int], np.ndarray]:
    time = tau / N**2
    output: dict[tuple[int, int, int], np.ndarray] = {}
    for left in groups:
        left_waves = left["wavevectors"]
        left_coefficients = left["coefficients"]
        left_squared = left["squared"]
        for right in groups:
            right_waves = right["wavevectors"]
            right_coefficients = right["coefficients"]
            right_squared = right["squared"]
            for index, (p_wave, p_coefficient) in enumerate(
                zip(left_waves, left_coefficients, strict=True)
            ):
                output_waves = p_wave[None, :] + right_waves
                output_squared = np.sum(output_waves * output_waves, axis=1)
                nonzero = output_squared > 0
                if not np.any(nonzero):
                    continue
                selected_waves = output_waves[nonzero]
                selected_squared = output_squared[nonzero]
                selected_coefficients = right_coefficients[nonzero]
                derivatives = right_waves[nonzero] @ p_coefficient
                raw = 1.0j * derivatives[:, None] * selected_coefficients
                longitudinal = (
                    np.sum(selected_waves * raw, axis=1) / selected_squared
                )
                projected = raw - selected_waves * longitudinal[:, None]
                factors = duhamel_factor(
                    selected_squared,
                    left_squared[index] + right_squared[nonzero],
                    time,
                    viscosity,
                )
                contributions = -factors[:, None] * projected
                for wavevector, contribution in zip(
                    selected_waves,
                    contributions,
                    strict=True,
                ):
                    key = tuple(int(value) for value in wavevector)
                    if key in output:
                        output[key] += contribution
                    else:
                        output[key] = contribution.copy()
    return output


def output_diagnostics(
    output: dict[tuple[int, int, int], np.ndarray],
    N: int,
    delta: float,
    input_energy: float,
) -> dict[str, float]:
    target = 0.0
    leakage = 0.0
    divergence = 0.0
    target_radius_squared = (2.0 * delta * N + 1e-9) ** 2
    positive_center = N * K_CENTER
    negative_center = -positive_center
    for wavevector_tuple, coefficient in output.items():
        wavevector = np.asarray(wavevector_tuple, dtype=float)
        contribution = float(
            np.linalg.norm(wavevector) * np.vdot(coefficient, coefficient).real
        )
        in_target = min(
            np.sum((wavevector - positive_center) ** 2),
            np.sum((wavevector - negative_center) ** 2),
        ) <= target_radius_squared
        if in_target:
            target += contribution
        else:
            leakage += contribution
        divergence = max(
            divergence,
            float(abs(np.dot(wavevector, coefficient))),
        )

    total = target + leakage
    return {
        "outputModeCount": len(output),
        "targetHHalfSquared": target,
        "leakageHHalfSquared": leakage,
        "totalHHalfSquared": total,
        "normalizedTargetHHalfSquared": target / input_energy**2,
        "normalizedLeakageHHalfSquared": leakage / input_energy**2,
        "targetFraction": target / total,
        "leakageToTarget": leakage / target,
        "divergenceResidual": divergence,
    }


def packet_audit(
    N: int,
    delta: float = 0.12,
    tau: float = TAU_STAR,
    viscosity: float = VISCOSITY,
) -> dict[str, object]:
    groups, displacements = build_groups(N, delta)
    input_record = input_diagnostics(groups)
    output = accumulate_first_picard(groups, N, tau, viscosity)
    output_record = output_diagnostics(
        output,
        N,
        delta,
        input_record["hHalfSquared"],
    )
    lattice_count = len(displacements)
    return {
        "N": N,
        "delta": delta,
        "tau": tau,
        "viscosity": viscosity,
        "latticeBallCount": lattice_count,
        "latticeBallDensity": lattice_count / N**3,
        "targetCenterOrderedPairMultiplicity": 2 * lattice_count,
        "normalizedTargetMultiplicity": 2 * lattice_count / N**3,
        "expectedTargetMultiplicityLimit": 2 * BALL_VOLUME * delta**3,
        "input": input_record,
        "output": output_record,
        "smallDelta": small_delta_formula(delta, tau),
        "targetToSmallDeltaLeadingRatio": output_record[
            "normalizedTargetHHalfSquared"
        ]
        / (SMALL_DELTA_TARGET_CONSTANT * delta**3),
    }


def delta_scaling_audit() -> list[dict[str, object]]:
    """Keep delta*N nearly fixed while varying the relative packet width."""

    records = []
    for delta, N in ((0.08, 54), (0.10, 43), (0.12, 36), (0.15, 29), (0.18, 24)):
        packet = packet_audit(N, delta)
        output = packet["output"]
        records.append(
            {
                "delta": delta,
                "N": N,
                "latticeRadius": delta * N,
                "latticeBallCount": packet["latticeBallCount"],
                "normalizedTargetHHalfSquared": output[
                    "normalizedTargetHHalfSquared"
                ],
                "targetOverDeltaCubed": output[
                    "normalizedTargetHHalfSquared"
                ]
                / delta**3,
                "targetToSmallDeltaLeadingRatio": packet[
                    "targetToSmallDeltaLeadingRatio"
                ],
                "leakageToTarget": output["leakageToTarget"],
                "leakageToTargetOverDeltaSquared": output["leakageToTarget"]
                / delta**2,
                "targetFraction": output["targetFraction"],
            }
        )
    return records


def run_audit(
    scales: tuple[int, ...] = (18, 24, 30, 36, 48),
    delta: float = 0.12,
) -> dict[str, object]:
    return {
        "statement": (
            "exact finite Fourier first-Picard calculation and continuum "
            "Riemann-sum asymptotics; no nonlinear remainder estimate"
        ),
        "centralKernel": central_kernel(),
        "constants": {
            "tauStar": TAU_STAR,
            "ballVolume": BALL_VOLUME,
            "convolutionSquareIntegral": CONVOLUTION_SQUARE_INTEGRAL,
            "smallDeltaTargetConstant": SMALL_DELTA_TARGET_CONSTANT,
            "formula": (
                "lim_delta delta^-3 lim_N H_target(normalized) "
                "= 136*pi*sqrt(6)/688905"
            ),
        },
        "packets": [packet_audit(N, delta) for N in scales],
        "deltaScaling": delta_scaling_audit(),
    }


def validate(audit: dict[str, object]) -> None:
    central = audit["centralKernel"]
    assert central["closureResidual"] == [0, 0, 0]
    assert abs(central["targetProjectedSquared"] - 4.0 / 3.0) < 2e-15
    assert abs(central["targetHDirectionImaginaryPairing"] - 2.0) < 2e-15
    assert central["differenceProjectedSquared"] < 2e-30
    assert central["rankOneRandomMaximumError"] < 4e-15
    assert central["rangeToTransportedPairing"] == [0.0, 0.0]
    assert central["selfDerivativeP"] == [0.0, 0.0]
    assert central["selfDerivativeQ"] == [0.0, 0.0]
    assert abs(heat_scalar(TAU_STAR) - 2.0 / 27.0) < 2e-15
    for packet in audit["packets"]:
        assert packet["input"]["divergenceResidual"] < 2e-15
        assert packet["input"]["realityResidual"] == 0.0
        assert packet["output"]["divergenceResidual"] < 2e-15
        assert packet["output"]["normalizedTargetHHalfSquared"] > 0.0
        assert packet["output"]["targetFraction"] > 0.5
        assert packet["targetCenterOrderedPairMultiplicity"] == 2 * packet[
            "latticeBallCount"
        ]
    for record in audit["deltaScaling"]:
        assert 0.9 < record["targetToSmallDeltaLeadingRatio"] < 1.1
        assert 0.7 < record["leakageToTargetOverDeltaSquared"] < 1.0
        assert record["targetFraction"] > 0.97


def main() -> None:
    audit = run_audit()
    validate(audit)
    print(json.dumps(audit, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
