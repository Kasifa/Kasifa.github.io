#!/usr/bin/env python3
"""Independent standard-library audit for R0.71J.

This checker imports neither the SymPy producer nor any project Fourier
helper.  It independently reconstructs the broad-parent 2D3C datum by direct
Fourier convolution and Leray projection, checks the all-shell positive
defect identity at deterministic sample points, and evaluates the pure-heat
profiles and K**2 full-frame separation.  It is not a DNS calculation.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Sequence


ComplexVector = tuple[complex, complex, complex]
Frequency = tuple[int, int, int]
Field = dict[Frequency, ComplexVector]


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


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
            tuple(complex(entry) for entry in frequency),  # type: ignore[arg-type]
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
        radius_squared = sum(entry * entry for entry in frequency)
        if radius_squared == 0:
            projected = value
        else:
            k_dot = sum(frequency[index] * value[index] for index in range(3))
            projected = tuple(
                value[index] - frequency[index] * k_dot / radius_squared
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


def restrict_parent(field: Field) -> Field:
    return {
        frequency: value
        for frequency, value in field.items()
        if 16 <= sum(entry * entry for entry in frequency) <= 32
    }


def restrict_horizontal_abs(field: Field, horizontal_abs: int) -> Field:
    return {
        frequency: value
        for frequency, value in field.items()
        if abs(frequency[0]) == horizontal_abs
    }


def close(left: float, right: float, tolerance: float = 2.0e-12) -> bool:
    return abs(left - right) <= tolerance * max(1.0, abs(left), abs(right))


def positive_defect_audit() -> dict[str, object]:
    maximum_hard = 0.0
    maximum_soft = 0.0
    sample_count = 257
    for index in range(sample_count):
        phase = (index + 0.5) / sample_count
        nu = 0.3 + phase
        shell_scale = 0.8 + 3.2 * phase
        z_value = 0.2 + 0.7 * phase
        a_value = z_value * z_value
        signed_joint = 0.55 * math.sin(7.0 * phase) - 0.18
        joint_plus = max(signed_joint, 0.0)
        joint_minus = max(-signed_joint, 0.0)
        theta_epsilon = phase / (1.0 + phase)
        weight = shell_scale**-2
        a_t = (
            2.0 * z_value * (joint_plus - joint_minus)
            - 2.0 * nu * shell_scale**2 * a_value
        )
        hard_left = 2.0 * weight * z_value * joint_plus
        hard_right = (
            weight * a_t
            + 2.0 * nu * a_value
            + 2.0 * weight * z_value * joint_minus
        )
        maximum_hard = max(maximum_hard, abs(hard_left - hard_right))

        soft_a_t = (
            2.0 * z_value * (joint_plus - joint_minus)
            - 2.0
            * nu
            * shell_scale**2
            * (1.0 + theta_epsilon)
            * a_value
        )
        soft_right = (
            weight * soft_a_t
            + 2.0 * nu * (1.0 + theta_epsilon) * a_value
            + 2.0 * weight * z_value * joint_minus
        )
        maximum_soft = max(maximum_soft, abs(hard_left - soft_right))
    require(maximum_hard < 1.0e-14, "hard positive-defect identity")
    require(maximum_soft < 1.0e-14, "soft positive-defect identity")
    return {
        "passed": True,
        "sampleCount": sample_count,
        "maximumHardResidual": maximum_hard,
        "maximumSoftResidual": maximum_soft,
    }


def broad_parent_fourier_audit() -> dict[str, object]:
    e2 = (0j, 1 + 0j, 0j)
    e3 = (0j, 0j, 1 + 0j)
    velocity: Field = {
        (1, 0, 0): e2,
        (-1, 0, 0): e2,
        (0, 4, 0): (0j, 0j, 0.25j),
        (0, -4, 0): (0j, 0j, -0.25j),
        (0, 5, 0): (0j, 0j, -0.2j),
        (0, -5, 0): (0j, 0j, 0.2j),
    }
    for channel in (4, 5):
        for horizontal_sign in (-1, 1):
            velocity[(horizontal_sign, channel, 0)] = e3
            velocity[(-horizontal_sign, -channel, 0)] = e3

    omega = field_curl(velocity)
    lamb = leray(field_cross(velocity, omega))
    parent_f = restrict_parent(lamb)
    parent_c = field_curl(restrict_parent(omega))
    values = {
        "kineticEnergy": field_norm_squared(velocity),
        "YOverK2": field_norm_squared(omega),
        "FParentNormSquaredOverK2": field_norm_squared(parent_f),
        "dParentOverK4": field_norm_squared(parent_c),
        "BParentOverK3Real": field_pair(parent_f, parent_c).real,
        "BParentOverK3Imaginary": field_pair(parent_f, parent_c).imag,
    }
    expected = {
        "kineticEnergy": 2041.0 / 200.0,
        "YOverK2": 178.0,
        "FParentNormSquaredOverK2": 500.0,
        "dParentOverK4": 3942.0,
        "BParentOverK3Real": 0.0,
        "BParentOverK3Imaginary": 0.0,
    }
    maximum_residual = max(abs(values[key] - expected[key]) for key in expected)
    require(maximum_residual < 2.0e-12, "independent broad-parent constants")

    groups = {}
    expected_groups = {
        0: (328.0, 82.0, 36.0),
        1: (8.0, 3860.0, -36.0),
        2: (164.0, 0.0, 0.0),
    }
    for horizontal_abs in (0, 1, 2):
        f_group = restrict_horizontal_abs(parent_f, horizontal_abs)
        c_group = restrict_horizontal_abs(parent_c, horizontal_abs)
        row = (
            field_norm_squared(f_group),
            field_norm_squared(c_group),
            field_pair(f_group, c_group).real,
        )
        require(
            max(abs(value - target) for value, target in zip(row, expected_groups[horizontal_abs]))
            < 2.0e-12,
            f"horizontal group {horizontal_abs}",
        )
        groups[str(horizontal_abs)] = {
            "F2": row[0],
            "d": row[1],
            "B": row[2],
        }

    f_radii = sorted(
        {sum(entry * entry for entry in frequency) for frequency in parent_f}
    )
    c_radii = sorted(
        {sum(entry * entry for entry in frequency) for frequency in parent_c}
    )
    require(f_radii == [16, 17, 20, 25, 26, 29], "parent F radii")
    require(c_radii == [16, 17, 25, 26], "parent C radii")
    require(parent_f == lamb, "every initial Lamb mode lies in the flat parent")
    require(
        {abs(frequency[1]) for frequency in parent_f} == {4, 5},
        "initial Lamb vertical channels",
    )
    return {
        "passed": True,
        "maximumResidual": maximum_residual,
        "values": values,
        "horizontalFrequencyGroups": groups,
        "FRadiusSquared": f_radii,
        "CRadiusSquared": c_radii,
        "allInitialLambModesInParent": True,
        "absoluteVerticalChannels": [4, 5],
    }


def heat_profiles(theta: float) -> tuple[float, float, float, float, float]:
    b_value = 4.0 * (math.exp(-34.0 * theta) - math.exp(-52.0 * theta))
    d_value = (
        32.0 * math.exp(-32.0 * theta)
        + 50.0 * math.exp(-50.0 * theta)
        + 1156.0 * math.exp(-34.0 * theta)
        + 2704.0 * math.exp(-52.0 * theta)
    )
    y_value = (
        2.0 * math.exp(-2.0 * theta)
        + 2.0 * math.exp(-32.0 * theta)
        + 2.0 * math.exp(-50.0 * theta)
        + 68.0 * math.exp(-34.0 * theta)
        + 104.0 * math.exp(-52.0 * theta)
    )
    f_squared = (
        4.0 * math.exp(-34.0 * theta)
        + 192.0 * math.exp(-36.0 * theta)
        + 4.0 * math.exp(-52.0 * theta)
        + 300.0 * math.exp(-54.0 * theta)
    )
    amplitude = b_value**2 / (d_value * y_value)
    return b_value, d_value, y_value, f_squared, amplitude


def direct_heat_reconstruction_audit() -> dict[str, object]:
    e2 = (0j, 1 + 0j, 0j)
    e3 = (0j, 0j, 1 + 0j)
    initial: Field = {
        (1, 0, 0): e2,
        (-1, 0, 0): e2,
        (0, 4, 0): (0j, 0j, 0.25j),
        (0, -4, 0): (0j, 0j, -0.25j),
        (0, 5, 0): (0j, 0j, -0.2j),
        (0, -5, 0): (0j, 0j, 0.2j),
    }
    for channel in (4, 5):
        for horizontal_sign in (-1, 1):
            initial[(horizontal_sign, channel, 0)] = e3
            initial[(-horizontal_sign, -channel, 0)] = e3

    sample_thetas = [0.0, math.log(2.0) / 18.0] + [0.01 * index for index in range(1, 21)]
    maximum_residual = 0.0
    for theta in sample_thetas:
        velocity = {
            frequency: tuple(
                entry
                * math.exp(
                    -sum(component * component for component in frequency) * theta
                )
                for entry in value
            )
            for frequency, value in initial.items()
        }
        omega = field_curl(velocity)
        lamb = leray(field_cross(velocity, omega))
        parent_f = restrict_parent(lamb)
        parent_c = field_curl(restrict_parent(omega))
        direct = (
            field_pair(parent_f, parent_c).real,
            field_norm_squared(parent_c),
            field_norm_squared(omega),
            field_norm_squared(parent_f),
        )
        expected = heat_profiles(theta)[:4]
        maximum_residual = max(
            maximum_residual,
            *(abs(value - target) for value, target in zip(direct, expected)),
        )
    require(maximum_residual < 2.0e-11, "direct heat Fourier reconstruction")
    return {
        "passed": True,
        "sampleCount": len(sample_thetas),
        "maximumResidual": maximum_residual,
        "method": "heat-decay every initial Fourier coefficient, then rebuild curl, convolution, Leray projection, parent F, and parent C",
    }


def heat_and_scaling_audit() -> dict[str, object]:
    theta_star = math.log(2.0) / 18.0
    b_value, d_value, y_value, f_squared, amplitude = heat_profiles(theta_star)
    expected_b = 2.0 ** (1.0 / 9.0) / 2.0
    expected_d = (
        57.0 * 2.0 ** (1.0 / 9.0) * (2.0 ** (1.0 / 9.0) + 44.0) / 4.0
    )
    expected_y = 2.0 ** (1.0 / 9.0) * (
        0.75 * 2.0 ** (1.0 / 9.0) + 2.0 ** (7.0 / 9.0) + 30.0
    )
    expected_f = 1.5 * 2.0 ** (1.0 / 9.0) + 85.5
    expected_amplitude = 4.0 / (
        57.0
        * (2.0 ** (1.0 / 9.0) + 44.0)
        * (
            3.0 * 2.0 ** (1.0 / 9.0)
            + 4.0 * 2.0 ** (7.0 / 9.0)
            + 120.0
        )
    )
    for value, expected, label in (
        (b_value, expected_b, "B star"),
        (d_value, expected_d, "d star"),
        (y_value, expected_y, "Y star"),
        (f_squared, expected_f, "F star"),
        (amplitude, expected_amplitude, "amplitude star"),
    ):
        require(close(value, expected), label)
    require(heat_profiles(0.0)[0] == 0.0, "zero entry B")
    require(heat_profiles(0.0)[4] == 0.0, "zero entry amplitude")

    frequencies = [8, 16, 32, 64, 128]
    ratio_lower = []
    for frequency in frequencies:
        creation_lower = amplitude / (64.0 * frequency**2)
        heat_upper = (1.0 - math.exp(-2.0 * theta_star)) / (2.0 * frequency**4)
        ratio_lower.append(creation_lower / heat_upper)
    successive = [
        ratio_lower[index + 1] / ratio_lower[index]
        for index in range(len(ratio_lower) - 1)
    ]
    require(max(abs(value - 4.0) for value in successive) < 2.0e-14, "K^2 law")

    # The deterministic frame estimate uses only support and the vertical
    # spectral gap: kappa_j^-2 <= 4|xi|^-2 and |xi| >= 4K.
    frame_constant = 4.0
    vertical_gap_squared = 16.0
    lamb_over_y = 4.0
    density_constant = frame_constant * lamb_over_y / vertical_gap_squared
    require(close(density_constant, 1.0), "full-frame heat density constant")
    return {
        "passed": True,
        "thetaStar": theta_star,
        "BAtThetaStarOverK3": b_value,
        "dAtThetaStarOverK4": d_value,
        "YAtThetaStarOverK2": y_value,
        "FAtThetaStarSquaredOverK2": f_squared,
        "aAtThetaStar": amplitude,
        "frameHeatDensityConstant": density_constant,
        "frequencies": frequencies,
        "creationOverHeatLowerAtNu1": ratio_lower,
        "successiveRatios": successive,
    }


def main(output: Path | None = None) -> None:
    payload = {
        "status": "passed",
        "positiveDefect": positive_defect_audit(),
        "broadParentFourier": broad_parent_fourier_audit(),
        "directHeatFourierReconstruction": direct_heat_reconstruction_audit(),
        "heatAndScaling": heat_and_scaling_audit(),
        "claims": {
            "allShellCancellationAfterPositivePartsRejected": True,
            "parentOnlyFrameChecked": True,
            "totalHeatPaymentRejectedForThatFrame": True,
            "matchedSpatialCellsChecked": False,
            "facePaidWeightedBVRejected": False,
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
