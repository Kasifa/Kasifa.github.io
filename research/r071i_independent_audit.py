#!/usr/bin/env python3
"""Independent standard-library audit for R0.71I.

This checker imports neither the SymPy producer nor any project Fourier
helper.  It independently tests the hard/soft joint identities along a
smooth three-dimensional Hilbert path, rebuilds the symmetric 2D3C datum by
direct Fourier convolution and Leray projection, and checks the two-power
heat-volume scaling and cutoff-refresh constants.  It is an algebraic and
quadrature audit, not a Navier--Stokes simulation.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Callable, Iterable, Sequence


Vector = list[float]
ComplexVector = tuple[complex, complex, complex]
Frequency = tuple[int, int, int]
Field = dict[Frequency, ComplexVector]


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def dot(left: Sequence[float], right: Sequence[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def add(left: Sequence[float], right: Sequence[float]) -> Vector:
    return [a + b for a, b in zip(left, right)]


def subtract(left: Sequence[float], right: Sequence[float]) -> Vector:
    return [a - b for a, b in zip(left, right)]


def scale(factor: float, value: Sequence[float]) -> Vector:
    return [factor * entry for entry in value]


def norm_squared(value: Sequence[float]) -> float:
    return dot(value, value)


def project_tangent(direction: Sequence[float], value: Sequence[float]) -> Vector:
    return subtract(value, scale(dot(direction, value), direction))


def simpson(
    function: Callable[[float], float],
    left: float,
    right: float,
    intervals: int = 12000,
) -> float:
    require(intervals > 0 and intervals % 2 == 0, "even Simpson count")
    step = (right - left) / intervals
    total = function(left) + function(right)
    for index in range(1, intervals):
        total += (4.0 if index % 2 else 2.0) * function(left + index * step)
    return total * step / 3.0


def path(t: float) -> tuple[Vector, Vector, Vector, Vector, float, float]:
    c_value = [
        1.1 + 0.2 * math.sin(0.7 * t),
        0.8 + 0.15 * t + 0.04 * t * t,
        0.6 + 0.1 * math.cos(1.3 * t),
    ]
    c_derivative = [
        0.14 * math.cos(0.7 * t),
        0.15 + 0.08 * t,
        -0.13 * math.sin(1.3 * t),
    ]
    tangent_seed = [
        0.12 * math.cos(0.9 * t),
        -0.08 * math.sin(0.5 * t),
        0.05 * t,
    ]
    tangent_seed_derivative = [
        -0.108 * math.sin(0.9 * t),
        -0.04 * math.cos(0.5 * t),
        0.05,
    ]
    f_value = add(scale(1.35, c_value), tangent_seed)
    f_derivative = add(scale(1.35, c_derivative), tangent_seed_derivative)
    y_value = 2.4 + 0.3 * t + 0.08 * t * t
    y_derivative = 0.3 + 0.16 * t
    return f_value, f_derivative, c_value, c_derivative, y_value, y_derivative


def joint_path_audit() -> dict[str, float | int | bool]:
    lam = 0.73
    epsilon = 0.19
    maxima = {
        "hardDirection": 0.0,
        "hardBeta": 0.0,
        "hardZ": 0.0,
        "hardScalar": 0.0,
        "hardPythagorean": 0.0,
        "softDirection": 0.0,
        "softBeta": 0.0,
        "softZ": 0.0,
        "softScalar": 0.0,
    }
    minimum_beta = math.inf
    samples = 101
    for index in range(samples):
        t = 1.7 * index / (samples - 1)
        f_value, f_t, c_value, c_t, y_value, y_t = path(t)
        rho = math.sqrt(norm_squared(c_value))
        direction = scale(1.0 / rho, c_value)
        direction_t = scale(
            1.0 / rho,
            project_tangent(direction, c_t),
        )
        n_value = add(f_t, scale(lam, f_value))
        m_value = add(c_t, scale(lam, c_value))
        pm = project_tangent(direction, m_value)
        direction_model = scale(1.0 / rho, pm)
        beta = dot(f_value, direction)
        minimum_beta = min(minimum_beta, beta)
        beta_t = dot(f_t, direction) + dot(f_value, direction_t)
        pf = project_tangent(direction, f_value)
        s_value = dot(n_value, direction) + dot(pf, pm) / rho
        maxima["hardDirection"] = max(
            maxima["hardDirection"],
            max(abs(a - b) for a, b in zip(direction_t, direction_model)),
        )
        maxima["hardBeta"] = max(
            maxima["hardBeta"], abs(beta_t + lam * beta - s_value)
        )

        sqrt_y = math.sqrt(y_value)
        x_value = scale(1.0 / sqrt_y, f_value)
        z_value = beta / sqrt_y
        logarithmic_y = y_t / y_value
        z_t = beta_t / sqrt_y - 0.5 * logarithmic_y * z_value
        joint = s_value / sqrt_y - 0.5 * logarithmic_y * z_value
        maxima["hardZ"] = max(
            maxima["hardZ"], abs(z_t + lam * z_value - joint)
        )
        a_value = z_value * z_value
        a_t = 2.0 * z_value * z_t
        maxima["hardScalar"] = max(
            maxima["hardScalar"],
            abs(a_t + 2.0 * lam * a_value - 2.0 * z_value * joint),
        )
        xi_t = add(scale(z_t, direction), scale(z_value, direction_t))
        xi_left = add(xi_t, scale(lam * z_value, direction))
        pythagorean_right = joint * joint + a_value * norm_squared(pm) / rho**2
        maxima["hardPythagorean"] = max(
            maxima["hardPythagorean"],
            abs(norm_squared(xi_left) - pythagorean_right),
        )

        soft_radius = math.sqrt(rho * rho + epsilon)
        soft_direction = scale(1.0 / soft_radius, c_value)
        soft_pair = dot(soft_direction, c_t)
        soft_direction_t = scale(
            1.0 / soft_radius,
            subtract(c_t, scale(soft_pair, soft_direction)),
        )
        soft_pm = subtract(m_value, scale(dot(soft_direction, m_value), soft_direction))
        soft_model = add(
            scale(1.0 / soft_radius, soft_pm),
            scale(-lam * epsilon / (rho * rho + epsilon), soft_direction),
        )
        maxima["softDirection"] = max(
            maxima["softDirection"],
            max(abs(a - b) for a, b in zip(soft_direction_t, soft_model)),
        )
        soft_beta = dot(f_value, soft_direction)
        soft_beta_t = dot(f_t, soft_direction) + dot(f_value, soft_direction_t)
        soft_s = dot(n_value, soft_direction) + dot(f_value, soft_pm) / soft_radius
        theta_epsilon = epsilon / (rho * rho + epsilon)
        maxima["softBeta"] = max(
            maxima["softBeta"],
            abs(
                soft_beta_t
                + lam * (1.0 + theta_epsilon) * soft_beta
                - soft_s
            ),
        )
        soft_z = soft_beta / sqrt_y
        soft_z_t = soft_beta_t / sqrt_y - 0.5 * logarithmic_y * soft_z
        soft_joint = soft_s / sqrt_y - 0.5 * logarithmic_y * soft_z
        maxima["softZ"] = max(
            maxima["softZ"],
            abs(
                soft_z_t
                + lam * (1.0 + theta_epsilon) * soft_z
                - soft_joint
            ),
        )
        soft_a = soft_z * soft_z
        soft_a_t = 2.0 * soft_z * soft_z_t
        maxima["softScalar"] = max(
            maxima["softScalar"],
            abs(
                soft_a_t
                + 2.0 * lam * (1.0 + theta_epsilon) * soft_a
                - 2.0 * soft_z * soft_joint
            ),
        )

    require(minimum_beta > 0.0, "positive branch along hard path")
    require(max(maxima.values()) < 2.0e-14, "joint identity residual")
    return {
        "passed": True,
        "sampleCount": samples,
        "minimumBeta": minimum_beta,
        **{"maximum" + key[0].upper() + key[1:] + "Residual": value for key, value in maxima.items()},
    }


def frequency_add(left: Frequency, right: Frequency) -> Frequency:
    return tuple(a + b for a, b in zip(left, right))  # type: ignore[return-value]


def complex_cross(left: ComplexVector, right: ComplexVector) -> ComplexVector:
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def field_curl(field: Field) -> Field:
    result: Field = {}
    for frequency, value in field.items():
        k_cross = complex_cross(
            (complex(frequency[0]), complex(frequency[1]), complex(frequency[2])),
            value,
        )
        result[frequency] = tuple(1j * entry for entry in k_cross)  # type: ignore[assignment]
    return result


def field_cross(left: Field, right: Field) -> Field:
    result: Field = {}
    for left_frequency, left_value in left.items():
        for right_frequency, right_value in right.items():
            frequency = frequency_add(left_frequency, right_frequency)
            term = complex_cross(left_value, right_value)
            previous = result.get(frequency, (0j, 0j, 0j))
            result[frequency] = tuple(a + b for a, b in zip(previous, term))  # type: ignore[assignment]
    return result


def leray(field: Field) -> Field:
    result: Field = {}
    for frequency, value in field.items():
        k2 = sum(entry * entry for entry in frequency)
        if k2 == 0:
            projected = value
        else:
            k_dot = sum(frequency[index] * value[index] for index in range(3))
            projected = tuple(
                value[index] - frequency[index] * k_dot / k2
                for index in range(3)
            )
        if sum(abs(entry) ** 2 for entry in projected) > 1.0e-28:
            result[frequency] = projected  # type: ignore[assignment]
    return result


def field_norm_squared(field: Field) -> float:
    return sum(abs(entry) ** 2 for value in field.values() for entry in value)


def field_pair(left: Field, right: Field) -> complex:
    frequencies = set(left) | set(right)
    return sum(
        left.get(frequency, (0j, 0j, 0j))[index].conjugate()
        * right.get(frequency, (0j, 0j, 0j))[index]
        for frequency in frequencies
        for index in range(3)
    )


def restrict(field: Field, frequencies: Iterable[Frequency]) -> Field:
    keep = set(frequencies)
    return {frequency: value for frequency, value in field.items() if frequency in keep}


def fourier_pulse_audit() -> dict[str, object]:
    e2 = (0j, 1 + 0j, 0j)
    e3 = (0j, 0j, 1 + 0j)
    velocity: Field = {
        (1, 0, 0): e2,
        (-1, 0, 0): e2,
        (0, 2, 0): (0j, 0j, 0.5j),
        (0, -2, 0): (0j, 0j, -0.5j),
        (0, 3, 0): (0j, 0j, -1j / 3.0),
        (0, -3, 0): (0j, 0j, 1j / 3.0),
    }
    for channel, coefficient in ((2, 0.2), (3, 0.1)):
        for horizontal_sign in (-1, 1):
            velocity[(horizontal_sign, channel, 0)] = (
                0j,
                0j,
                complex(coefficient),
            )
            velocity[(-horizontal_sign, -channel, 0)] = (
                0j,
                0j,
                complex(coefficient),
            )
    keep = {
        (horizontal_sign, vertical_frequency, 0)
        for horizontal_sign in (-1, 1)
        for vertical_frequency in (-3, -2, 2, 3)
    }
    omega = field_curl(velocity)
    lamb = leray(field_cross(velocity, omega))
    f_value = restrict(lamb, keep)
    c_value = field_curl(restrict(omega, keep))
    values = {
        "kineticEnergy": field_norm_squared(velocity),
        "YOverK2": field_norm_squared(omega),
        "FNormSquaredOverK2": field_norm_squared(f_value),
        "dOverK4": field_norm_squared(c_value),
        "BOverK3Real": field_pair(f_value, c_value).real,
        "BOverK3Imaginary": field_pair(f_value, c_value).imag,
    }
    expected = {
        "kineticEnergy": 263.0 / 90.0,
        "YOverK2": 36.0 / 5.0,
        "FNormSquaredOverK2": 8.0,
        "dOverK4": 8.0,
        "BOverK3Real": 0.0,
        "BOverK3Imaginary": 0.0,
    }
    maximum_residual = max(abs(values[key] - expected[key]) for key in expected)
    require(maximum_residual < 2.0e-14, "independent Fourier constants")

    per_mode = {}
    for frequency in sorted(keep):
        per_mode[str(frequency)] = {
            "u3": [velocity[frequency][2].real, velocity[frequency][2].imag],
            "F3OverK": [f_value[frequency][2].real, f_value[frequency][2].imag],
            "C3OverK2": [c_value[frequency][2].real, c_value[frequency][2].imag],
        }
    return {
        "passed": True,
        "maximumResidual": maximum_residual,
        "values": values,
        "perRetainedMode": per_mode,
    }


def heat_and_scaling_audit() -> dict[str, object]:
    sqrt17 = math.sqrt(17.0)
    x_star = (sqrt17 - 3.0) / 4.0
    peak = (71.0 - 17.0 * sqrt17) / 16.0
    tv = 2.0 * peak
    tau_star = -0.5 * math.log(x_star)
    dense_x = [index / 200000.0 for index in range(200001)]
    dense_values = [x * (1.0 - x) ** 2 / (2.0 * (1.0 + x)) for x in dense_x]
    numerical_peak = max(dense_values)
    require(abs(numerical_peak - peak) < 2.0e-10, "common heat peak")

    heat_integral = simpson(
        lambda tau: 0.5 * (math.exp(-2.0 * tau) + math.exp(-4.0 * tau)),
        0.0,
        30.0,
    )
    require(abs(heat_integral - 3.0 / 8.0) < 1.0e-11, "heat integral")
    joint_square_integral = simpson(
        lambda tau: (
            math.exp(-6.0 * tau)
            * (math.exp(-2.0 * tau) + 3.0) ** 2
            / (2.0 * (1.0 + math.exp(-2.0 * tau)) ** 3)
        ),
        0.0,
        30.0,
    )
    expected_joint_square = 0.75 * (1.0 - math.log(2.0))
    require(
        abs(joint_square_integral - expected_joint_square) < 2.0e-11,
        "joint-square integral",
    )

    theta_star = math.log(2.0) / 10.0

    def q0(theta: float) -> float:
        value = math.exp(-10.0 * theta)
        return 4.0 * value * (1.0 - value) ** 2 / (1.0 + value)

    def y0(theta: float) -> float:
        return (
            2.0 * math.exp(-2.0 * theta)
            + 2.0 * math.exp(-8.0 * theta)
            + 2.0 * math.exp(-18.0 * theta)
            + 0.8 * math.exp(-10.0 * theta)
            + 0.4 * math.exp(-20.0 * theta)
        )

    def g0(theta: float) -> float:
        return 4.0 * (
            math.exp(-10.0 * theta) + math.exp(-20.0 * theta)
        ) / y0(theta)

    a_star = q0(theta_star) / y0(theta_star)
    expected_a_star = 2.0 / (
        3.0 * (1.0 + 3.0 * 2.0 ** 0.2 + 2.0 * 2.0 ** 0.8)
    )
    require(abs(q0(theta_star) - 1.0 / 3.0) < 2.0e-15, "Q0 at theta star")
    require(abs(a_star - expected_a_star) < 2.0e-15, "A0 at theta star")
    g_integral = simpson(g0, 0.0, theta_star, 4000)
    ratios = []
    for frequency in (8.0, 16.0, 32.0, 64.0):
        weighted_bv_lower = a_star / (2.0 * frequency**2)
        weighted_volume = g_integral / frequency**4
        ratios.append(weighted_bv_lower / weighted_volume)
    normalized_ratios = [
        ratios[index + 1] / ratios[index] for index in range(len(ratios) - 1)
    ]
    require(max(abs(value - 4.0) for value in normalized_ratios) < 2.0e-14, "K^2 ratio")

    refresh_gap = 0.25 - 1.0 / 7.0
    require(abs(refresh_gap - 3.0 / 28.0) < 2.0e-16, "refresh gap")
    return {
        "passed": True,
        "commonHeat": {
            "xAtPeak": x_star,
            "tauAtPeak": tau_star,
            "peak": peak,
            "totalVariation": tv,
            "heatIntegralInTau": heat_integral,
            "jointSquareIntegral": joint_square_integral,
            "jointSquareExact": expected_joint_square,
        },
        "true2D3CLimit": {
            "thetaStar": theta_star,
            "Q0AtThetaStar": q0(theta_star),
            "A0AtThetaStar": a_star,
            "G0IntegralToThetaStar": g_integral,
            "frequencies": [8, 16, 32, 64],
            "weightedBVLowerOverWeightedVolume": ratios,
            "successiveRatios": normalized_ratios,
        },
        "cutoffRefresh": {
            "aggregateAtDelta0OverU2": 0.25,
            "aggregateAtDelta1OverU2": 1.0 / 7.0,
            "gapOverU2": refresh_gap,
        },
    }


def main(output: Path | None = None) -> None:
    payload = {
        "status": "passed",
        "jointPath": joint_path_audit(),
        "fourierZeroEntryPulse": fourier_pulse_audit(),
        "heatAndScaling": heat_and_scaling_audit(),
        "claims": {
            "hardAndSoftIdentitiesChecked": True,
            "symmetricEightTargetModesChecked": True,
            "heatVolumeAloneRejectedForDeclaredLimit": True,
            "fullWeightedBVRejected": False,
            "regularityTheoremClaimed": False,
            "originalityClaimed": False,
        },
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if output is None:
        print(rendered, end="")
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    main(arguments.output)
