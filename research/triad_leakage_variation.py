#!/usr/bin/env python3
"""Fixed-injection leakage variation on the six-mode central triad.

The optimization is finite dimensional. Published candidates are stored so
their diagnostics can be checked without rerunning a global search. When
``--optimize`` is used, SLSQP receives analytic gradients derived from

    D B(u,u)[h] = B(h,u) + B(u,h).

No numerical optimum in this file is claimed to be a global extremum.
"""

from __future__ import annotations

import argparse
import json
import math
from typing import Callable

import numpy as np


CENTERS = [(1, 0, 0), (0, 1, 0), (-1, -1, 0)]
ORIGINAL_PARAMETERS = np.asarray(
    [1, 0, -1, -1, -1, 0, -1, 0, -1, -1, 1, 0],
    dtype=float,
)

PUBLISHED_CANDIDATES = {
    "1.00": np.asarray(
        [
            -7.9902398721021908e-02,
            -3.0352088413930004e-02,
            4.5355079663950937e-01,
            1.7228339646669966e-01,
            2.4864746432034120e-02,
            8.1776020972355951e-02,
            -1.4113559161133962e-01,
            -4.6418577934245309e-01,
            6.5535661086785579e-08,
            -1.6507485228493448e-07,
            1.0141096416914086e-01,
            -6.8915240569487916e-03,
        ]
    ),
    "0.75": np.asarray(
        [
            -6.7569497702601282e-03,
            7.3419693203799749e-02,
            -4.4820817350216896e-02,
            4.8694562087472565e-01,
            -6.4737472907271068e-02,
            3.5288654797591940e-02,
            -4.2935947222522314e-01,
            2.3405277651547141e-01,
            1.9374525836718659e-07,
            -1.0559849677598166e-07,
            8.0508201783968114e-02,
            3.4733560039769878e-02,
        ]
    ),
    "0.50": np.asarray(
        [
            -5.9761794513698611e-02,
            5.0347145461034585e-03,
            -4.9102242680627367e-01,
            4.1383947504044276e-02,
            -2.5554231285313658e-02,
            5.4254408680124620e-02,
            -2.0997786536145868e-01,
            4.4576603919090257e-01,
            1.8232245843428518e-07,
            -3.9615793353085322e-07,
            -6.6842113617739798e-02,
            2.4865235271695547e-02,
        ]
    ),
    "0.25": np.asarray(
        [
            -2.6357111196225899e-02,
            3.3022267497774919e-02,
            3.0975923757297635e-01,
            -3.8796259975154140e-01,
            -2.7849508206174427e-02,
            3.1765610714991899e-02,
            3.2717222565672793e-01,
            -3.7329948385050482e-01,
            -4.9675539280003471e-07,
            -7.9496768316988949e-07,
            -4.9456546780411149e-02,
            -8.8655275736343984e-03,
        ]
    ),
}


def amplitudes_from_parameters(parameters: np.ndarray) -> list[np.ndarray]:
    values = np.asarray(
        [parameters[2 * index] + 1.0j * parameters[2 * index + 1] for index in range(6)]
    )
    return [
        np.asarray([0, values[0], values[1]], dtype=np.complex128),
        np.asarray([values[2], 0, values[3]], dtype=np.complex128),
        np.asarray([values[4], -values[4], values[5]], dtype=np.complex128),
    ]


def field_from_parameters(parameters: np.ndarray) -> dict[tuple[int, int, int], np.ndarray]:
    field: dict[tuple[int, int, int], np.ndarray] = {}
    for wavevector, amplitude in zip(
        CENTERS,
        amplitudes_from_parameters(parameters),
        strict=True,
    ):
        field[wavevector] = amplitude
        field[tuple(-component for component in wavevector)] = np.conjugate(amplitude)
    return field


def bilinear(
    left: dict[tuple[int, int, int], np.ndarray],
    right: dict[tuple[int, int, int], np.ndarray],
) -> dict[tuple[int, int, int], np.ndarray]:
    raw: dict[tuple[int, int, int], np.ndarray] = {}
    for p, left_coefficient in left.items():
        for q, right_coefficient in right.items():
            output = tuple(p[axis] + q[axis] for axis in range(3))
            if output == (0, 0, 0):
                continue
            contribution = 1.0j * np.dot(q, left_coefficient) * right_coefficient
            raw[output] = raw.get(output, np.zeros(3, dtype=np.complex128)) + contribution

    projected: dict[tuple[int, int, int], np.ndarray] = {}
    for wavevector, coefficient in raw.items():
        frequency = np.asarray(wavevector, dtype=float)
        projected[wavevector] = coefficient - frequency * (
            np.dot(frequency, coefficient) / np.dot(frequency, frequency)
        )
    return projected


def hhalf_pairing(
    left: dict[tuple[int, int, int], np.ndarray],
    right: dict[tuple[int, int, int], np.ndarray],
    support: set[tuple[int, int, int]] | None = None,
) -> float:
    common = set(left).intersection(right)
    if support is not None:
        common.intersection_update(support)
    return float(
        sum(
            np.linalg.norm(wavevector)
            * np.vdot(left[wavevector], right[wavevector]).real
            for wavevector in common
        )
    )


def diagnostics(parameters: np.ndarray) -> dict[str, float]:
    field = field_from_parameters(parameters)
    nonlinear = bilinear(field, field)
    support = set(field)
    outside = set(nonlinear).difference(support)
    energy = hhalf_pairing(field, field)
    transfer = hhalf_pairing(field, nonlinear, support)
    inside_squared = hhalf_pairing(nonlinear, nonlinear, support)
    outside_squared = hhalf_pairing(nonlinear, nonlinear, outside)
    score = (
        abs(transfer) / math.sqrt(energy * outside_squared)
        if energy > 0 and outside_squared > 0
        else 0.0
    )
    return {
        "energy": energy,
        "transfer": transfer,
        "insideSquared": inside_squared,
        "outsideSquared": outside_squared,
        "injectionOverEscape": score,
        "escapePerInjection": 1.0 / score if score > 0 else math.inf,
    }


PARAMETER_BASIS = [
    field_from_parameters(np.eye(12, dtype=float)[index]) for index in range(12)
]


def diagnostics_with_gradients(
    parameters: np.ndarray,
) -> tuple[dict[str, float], dict[str, np.ndarray]]:
    field = field_from_parameters(parameters)
    nonlinear = bilinear(field, field)
    support = set(field)
    outside = set(nonlinear).difference(support)
    values = diagnostics(parameters)
    energy_gradient = np.empty(12)
    transfer_gradient = np.empty(12)
    outside_gradient = np.empty(12)
    for index, direction in enumerate(PARAMETER_BASIS):
        derivative = bilinear(direction, field)
        second = bilinear(field, direction)
        for wavevector, coefficient in second.items():
            derivative[wavevector] = derivative.get(
                wavevector,
                np.zeros(3, dtype=np.complex128),
            ) + coefficient
        energy_gradient[index] = 2 * hhalf_pairing(field, direction)
        transfer_gradient[index] = hhalf_pairing(direction, nonlinear, support) + hhalf_pairing(
            field,
            derivative,
            support,
        )
        outside_gradient[index] = 2 * hhalf_pairing(
            nonlinear,
            derivative,
            outside,
        )
    return values, {
        "energy": energy_gradient,
        "transfer": transfer_gradient,
        "outsideSquared": outside_gradient,
    }


def normalize(parameters: np.ndarray) -> np.ndarray:
    return parameters / math.sqrt(diagnostics(parameters)["energy"])


def symmetric_2d3c_parameters(t_value: float) -> np.ndarray:
    amplitude_squared = 1.0 / (4.0 * (t_value + 2.0))
    horizontal = math.sqrt(amplitude_squared)
    closing = math.sqrt(math.sqrt(2.0) * amplitude_squared)
    vertical_ratio = math.sqrt(t_value)
    return np.asarray(
        [
            horizontal,
            0,
            -vertical_ratio * horizontal,
            0,
            horizontal,
            0,
            -vertical_ratio * horizontal,
            0,
            0,
            0,
            0,
            -closing,
        ],
        dtype=float,
    )


def symmetric_subfamily_injection(t_value: float) -> float:
    return (
        (math.sqrt(2.0) - 1.0)
        * 2.0 ** 0.25
        * math.sqrt(t_value)
        / (2.0 * (t_value + 2.0) ** 1.5)
    )


def bisect_root(function: Callable[[float], float], lower: float, upper: float) -> float:
    left_value = function(lower)
    right_value = function(upper)
    if left_value * right_value > 0:
        raise ValueError("root is not bracketed")
    for _ in range(100):
        middle = 0.5 * (lower + upper)
        middle_value = function(middle)
        if left_value * middle_value <= 0:
            upper = middle
            right_value = middle_value
        else:
            lower = middle
            left_value = middle_value
    return 0.5 * (lower + upper)


def analytic_fixed_injection_candidates(injection: float) -> dict[str, object]:
    equation = lambda value: symmetric_subfamily_injection(value) - injection
    small_root = bisect_root(equation, 1e-15, 1.0)
    large_root = bisect_root(equation, 1.0, 1e6)

    def record(root: float) -> dict[str, object]:
        parameters = symmetric_2d3c_parameters(root)
        return {
            "t": root,
            "r": math.sqrt(root),
            "parameters": parameters.tolist(),
            **diagnostics(parameters),
        }

    return {
        "formula": {
            "energy": "4 A^2(1+r^2)+2 sqrt(2) C^2",
            "transferMagnitude": "4(sqrt(2)-1) r A^2 C",
            "outsideSquared": "4 sqrt(5) A^2 C^2",
            "stationaryCondition": "C^2=sqrt(2) A^2",
        },
        "smallRoot": record(small_root),
        "largeRoot": record(large_root),
    }


def finite_difference_gradient(
    function: Callable[[np.ndarray], float],
    parameters: np.ndarray,
    step: float = 1e-6,
) -> np.ndarray:
    gradient = np.empty_like(parameters)
    for index in range(len(parameters)):
        positive = parameters.copy()
        negative = parameters.copy()
        positive[index] += step
        negative[index] -= step
        gradient[index] = (function(positive) - function(negative)) / (2 * step)
    return gradient


def published_audit() -> dict[str, object]:
    original = normalize(ORIGINAL_PARAMETERS)
    original_values = diagnostics(original)
    frontier = []
    for fraction, candidate in PUBLISHED_CANDIDATES.items():
        values = diagnostics(candidate)
        frontier.append({"injectionFraction": float(fraction), **values})
    return {
        "statement": "stored finite-dimensional candidates; no global-optimality claim",
        "original": original_values,
        "frontier": frontier,
        "analyticSymmetricSubfamily": analytic_fixed_injection_candidates(
            abs(original_values["transfer"])
        ),
        "fixedInjectionParameters": analytic_fixed_injection_candidates(
            abs(original_values["transfer"])
        )["largeRoot"]["parameters"],
    }


def optimize_fixed_injection(
    injection_fraction: float,
    starts: int,
    seed: int,
) -> dict[str, object]:
    from scipy.optimize import minimize

    original = normalize(ORIGINAL_PARAMETERS)
    minimum_injection = injection_fraction * abs(diagnostics(original)["transfer"])
    random = np.random.default_rng(seed)
    best = None
    for index in range(starts):
        initial = original if index == 0 else normalize(random.normal(size=12))

        def objective(value: np.ndarray) -> float:
            return diagnostics_with_gradients(value)[0]["outsideSquared"]

        def objective_jacobian(value: np.ndarray) -> np.ndarray:
            return diagnostics_with_gradients(value)[1]["outsideSquared"]

        def energy_constraint(value: np.ndarray) -> float:
            return diagnostics_with_gradients(value)[0]["energy"] - 1.0

        def energy_jacobian(value: np.ndarray) -> np.ndarray:
            return diagnostics_with_gradients(value)[1]["energy"]

        def injection_constraint(value: np.ndarray) -> float:
            transfer = diagnostics_with_gradients(value)[0]["transfer"]
            return transfer**2 - minimum_injection**2

        def injection_jacobian(value: np.ndarray) -> np.ndarray:
            values, gradients = diagnostics_with_gradients(value)
            return 2 * values["transfer"] * gradients["transfer"]

        result = minimize(
            objective,
            initial,
            jac=objective_jacobian,
            method="SLSQP",
            constraints=[
                {"type": "eq", "fun": energy_constraint, "jac": energy_jacobian},
                {"type": "ineq", "fun": injection_constraint, "jac": injection_jacobian},
            ],
            options={"maxiter": 500, "ftol": 1e-13},
        )
        values = diagnostics(result.x)
        feasible = (
            abs(values["energy"] - 1) < 1e-7
            and abs(values["transfer"]) >= minimum_injection * (1 - 1e-6)
        )
        if feasible and (best is None or values["outsideSquared"] < best[0]["outsideSquared"]):
            best = (values, result)
    if best is None:
        raise RuntimeError("no feasible candidate found")
    values, result = best
    return {
        "injectionFraction": injection_fraction,
        "starts": starts,
        "success": bool(result.success),
        "message": result.message,
        "values": values,
        "parameters": result.x.tolist(),
    }


def validate() -> None:
    test_point = normalize(np.arange(1, 13, dtype=float))
    values, gradients = diagnostics_with_gradients(test_point)
    checks = {
        "energy": lambda value: diagnostics(value)["energy"],
        "transfer": lambda value: diagnostics(value)["transfer"],
        "outsideSquared": lambda value: diagnostics(value)["outsideSquared"],
    }
    for name, function in checks.items():
        numerical = finite_difference_gradient(function, test_point)
        relative = np.linalg.norm(numerical - gradients[name]) / max(
            np.linalg.norm(numerical),
            1e-300,
        )
        assert relative < 2e-8, (name, relative)

    audit = published_audit()
    original = audit["original"]
    fixed = audit["frontier"][0]
    analytic = audit["analyticSymmetricSubfamily"]["largeRoot"]
    assert abs(original["energy"] - 1) < 1e-12
    assert abs(fixed["energy"] - 1) < 1e-10
    assert abs(abs(fixed["transfer"] / original["transfer"]) - 1) < 1e-10
    assert fixed["escapePerInjection"] < original["escapePerInjection"] / 10
    assert abs(analytic["outsideSquared"] / fixed["outsideSquared"] - 1) < 1e-10
    assert abs(abs(analytic["transfer"] / fixed["transfer"]) - 1) < 1e-10
    assert all(
        audit["frontier"][index]["outsideSquared"]
        > audit["frontier"][index + 1]["outsideSquared"]
        for index in range(len(audit["frontier"]) - 1)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--optimize", action="store_true")
    parser.add_argument("--starts", type=int, default=12)
    parser.add_argument("--fraction", type=float, default=1.0)
    args = parser.parse_args()
    validate()
    if args.optimize:
        output = optimize_fixed_injection(args.fraction, args.starts, seed=20260816)
    else:
        output = published_audit()
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
