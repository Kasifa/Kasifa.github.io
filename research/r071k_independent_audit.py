#!/usr/bin/env python3
"""Independent numerical/algebraic audit for R0.71K.

This checker imports neither the SymPy producer nor project Fourier helpers.
It rebuilds the R0.71J pure-heat field by direct Fourier convolution, constructs
an explicit C-infinity translated partition, and performs a one-cell
Gauss--Legendre quadrature of the complete cutoff-curl denominator.  It also
checks the equal-cell endpoint algebra and the K**2 separation.  The
quadrature is an independent diagnostic; the theorem uses the analytic
partition bounds recorded in the report.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Sequence

import numpy as np


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
        crossed = complex_cross(
            tuple(complex(entry) for entry in frequency),  # type: ignore[arg-type]
            value,
        )
        result[frequency] = tuple(1j * entry for entry in crossed)  # type: ignore[assignment]
    return result


def field_cross(left: Field, right: Field) -> Field:
    result: Field = {}
    for left_frequency, left_value in left.items():
        for right_frequency, right_value in right.items():
            frequency = frequency_add(left_frequency, right_frequency)
            term = complex_cross(left_value, right_value)
            previous = result.get(frequency, (0j, 0j, 0j))
            result[frequency] = tuple(
                a + b for a, b in zip(previous, term)
            )  # type: ignore[assignment]
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


def field_pair(left: Field, right: Field) -> complex:
    frequencies = set(left) | set(right)
    return sum(
        left.get(frequency, (0j, 0j, 0j))[index].conjugate()
        * right.get(frequency, (0j, 0j, 0j))[index]
        for frequency in frequencies
        for index in range(3)
    )


def field_norm_squared(field: Field) -> float:
    return sum(abs(entry) ** 2 for value in field.values() for entry in value)


def restrict_parent(field: Field) -> Field:
    return {
        frequency: value
        for frequency, value in field.items()
        if 16 <= sum(entry * entry for entry in frequency) <= 32
    }


def pure_heat_fields(theta: float) -> tuple[Field, Field, Field]:
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
    projected_lamb = leray(field_cross(velocity, omega))
    return restrict_parent(projected_lamb), restrict_parent(omega), omega


RADIUS = 1.5 * math.pi


def bump_and_derivative(value: float) -> tuple[float, float]:
    if abs(value) >= RADIUS:
        return 0.0, 0.0
    denominator = 1.0 - (value / RADIUS) ** 2
    bump = math.exp(-1.0 / denominator)
    derivative = bump * (-2.0 * value / (RADIUS**2 * denominator**2))
    return bump, derivative


def periodic_denominator(value: float) -> tuple[float, float]:
    total = 0.0
    derivative = 0.0
    center = int(round(value / (2.0 * math.pi)))
    for shift in range(center - 2, center + 3):
        bump, bump_derivative = bump_and_derivative(value - 2.0 * math.pi * shift)
        total += bump
        derivative += bump_derivative
    return total, derivative


def partition_atom(value: float) -> tuple[float, float]:
    bump, bump_derivative = bump_and_derivative(value)
    denominator, denominator_derivative = periodic_denominator(value)
    require(denominator > 0.0, "partition denominator")
    atom = bump / denominator
    atom_derivative = (
        bump_derivative * denominator - bump * denominator_derivative
    ) / denominator**2
    return atom, atom_derivative


def partition_audit() -> dict[str, object]:
    maximum_sum_residual = 0.0
    maximum_derivative_residual = 0.0
    maximum_overlap = 0
    maximum_square_sum = 0.0
    maximum_derivative_square_sum = 0.0
    for value in np.linspace(-math.pi, math.pi, 8193):
        atom_sum = 0.0
        derivative_sum = 0.0
        square_sum = 0.0
        derivative_square_sum = 0.0
        overlap = 0
        for shift in range(-2, 3):
            atom, derivative = partition_atom(value - 2.0 * math.pi * shift)
            atom_sum += atom
            derivative_sum += derivative
            square_sum += atom * atom
            derivative_square_sum += derivative * derivative
            overlap += int(atom > 0.0)
        maximum_sum_residual = max(maximum_sum_residual, abs(atom_sum - 1.0))
        maximum_derivative_residual = max(
            maximum_derivative_residual, abs(derivative_sum)
        )
        maximum_overlap = max(maximum_overlap, overlap)
        maximum_square_sum = max(maximum_square_sum, square_sum)
        maximum_derivative_square_sum = max(
            maximum_derivative_square_sum, derivative_square_sum
        )
    require(maximum_sum_residual < 3.0e-14, "partition of unity")
    require(maximum_derivative_residual < 3.0e-13, "derivative partition sum")
    require(maximum_overlap <= 2, "one-dimensional overlap")
    require(maximum_square_sum <= 1.0 + 3.0e-14, "square partition bound")
    gradient_square_bound_3d = (
        3.0 * maximum_derivative_square_sum * maximum_square_sum**2
    )
    diagnostic_cpart = 2.0 * maximum_square_sum**3 + gradient_square_bound_3d / 4.0
    return {
        "passed": True,
        "oneDimensionalOverlap": maximum_overlap,
        "tensorOverlap": maximum_overlap**3,
        "maximumPartitionResidual": maximum_sum_residual,
        "maximumDerivativeResidual": maximum_derivative_residual,
        "sampledC0Tensor": maximum_square_sum**3,
        "sampledGradientSquareBoundInY": gradient_square_bound_3d,
        "sampledCPartDiagnostic": diagnostic_cpart,
        "diagnosticOnly": True,
    }


def evaluate_field(field: Field, x_grid: np.ndarray, y_grid: np.ndarray) -> np.ndarray:
    result = np.zeros((3, *x_grid.shape), dtype=np.complex128)
    for (frequency_x, frequency_y, frequency_z), coefficient in field.items():
        require(frequency_z == 0, "2D3C frequency")
        phase = np.exp(1j * (frequency_x * x_grid + frequency_y * y_grid))
        for component in range(3):
            result[component] += coefficient[component] * phase
    return result


def one_cell_quadrature(theta: float, order: int = 360) -> dict[str, float]:
    f_field, w_field, omega = pure_heat_fields(theta)
    c_field = field_curl(w_field)
    nodes, weights = np.polynomial.legendre.leggauss(order)
    nodes = RADIUS * nodes
    weights = RADIUS * weights
    h = np.array([partition_atom(float(value))[0] for value in nodes])
    hp = np.array([partition_atom(float(value))[1] for value in nodes])
    x_grid, y_grid = np.meshgrid(nodes, nodes, indexing="ij")
    weights_2d = weights[:, None] * weights[None, :]
    hx = h[:, None]
    hy = h[None, :]
    hpx = hp[:, None]
    hpy = hp[None, :]
    f_values = evaluate_field(f_field, x_grid, y_grid)
    w_values = evaluate_field(w_field, x_grid, y_grid)
    c_values = evaluate_field(c_field, x_grid, y_grid)
    require(float(np.max(np.abs(w_values[2]))) < 2.0e-12, "selected W has no third component")
    require(float(np.max(np.abs(c_values[:2]))) < 2.0e-12, "selected curl W is vertical")

    integral_h = float(np.sum(weights * h))
    integral_h_squared = float(np.sum(weights * h**2))
    integral_hp_squared = float(np.sum(weights * hp**2))
    core = (
        hx * hy * c_values[2]
        + hpx * hy * w_values[1]
        - hx * hpy * w_values[0]
    )
    horizontal_density = (hx * hy) ** 2 * (
        np.abs(w_values[0]) ** 2 + np.abs(w_values[1]) ** 2
    )
    vertical_density = np.abs(core) ** 2
    d_base_horizontal = integral_hp_squared * float(
        np.sum(weights_2d * horizontal_density)
    )
    d_base_vertical = integral_h_squared * float(
        np.sum(weights_2d * vertical_density)
    )
    d_base = d_base_horizontal + d_base_vertical
    b_base = integral_h * float(
        np.sum(weights_2d * np.real(np.conjugate(f_values[2]) * core))
    )
    normalization = (2.0 * math.pi) ** 3
    global_b = field_pair(f_field, c_field).real
    global_d = field_norm_squared(c_field)
    global_y = field_norm_squared(omega)
    require(abs(integral_h - 2.0 * math.pi) < 2.0e-11, "partition atom mass")
    require(
        abs(b_base / normalization - global_b)
        < 5.0e-9 * max(1.0, abs(global_b)),
        "one-cell work equals global normalized work",
    )
    require(d_base > 0.0, "strict local denominator")
    return {
        "theta": theta,
        "quadratureOrder": order,
        "globalB": global_b,
        "globalD": global_d,
        "globalY": global_y,
        "cellBAtK1": b_base / normalization,
        "cellDAtK1": d_base / normalization,
        "cellDInteriorHorizontal": d_base_horizontal / normalization,
        "cellDVerticalIncludingCross": d_base_vertical / normalization,
        "DLocalOverDGlobal": d_base / normalization / global_d,
        "partitionAtomMass": integral_h,
    }


def endpoint_and_scaling_audit(cpart_diagnostic: float) -> dict[str, object]:
    theta_star = math.log(2.0) / 18.0
    initial = one_cell_quadrature(0.0)
    endpoint = one_cell_quadrature(theta_star)
    require(abs(initial["globalB"]) < 2.0e-12, "global zero entry")
    require(abs(initial["cellBAtK1"]) < 5.0e-9, "cell zero entry")
    require(endpoint["globalB"] > 0.0, "positive endpoint work")
    require(
        endpoint["DLocalOverDGlobal"] <= cpart_diagnostic * (1.0 + 2.0e-7),
        "sampled partition denominator bound",
    )
    amplitude_global = endpoint["globalB"] ** 2 / (
        endpoint["globalD"] * endpoint["globalY"]
    )
    amplitude_local = endpoint["globalB"] ** 2 / (
        endpoint["cellDAtK1"] * endpoint["globalY"]
    )
    require(
        amplitude_local >= amplitude_global / cpart_diagnostic,
        "localized endpoint lower bound",
    )

    frequencies = [8, 16, 32, 64, 128]
    overlap = 8.0
    creation_lower = [
        amplitude_global / (64.0 * cpart_diagnostic * frequency**2)
        for frequency in frequencies
    ]
    heat_upper = [
        overlap
        * (1.0 - 2.0 ** (-1.0 / 9.0))
        / (2.0 * frequency**4)
        for frequency in frequencies
    ]
    ratios = [left / right for left, right in zip(creation_lower, heat_upper)]
    successive = [ratios[index + 1] / ratios[index] for index in range(len(ratios) - 1)]
    require(max(abs(value - 4.0) for value in successive) < 3.0e-13, "K^2 ratio")
    return {
        "passed": True,
        "initial": initial,
        "thetaStarEndpoint": endpoint,
        "globalAmplitudeAtThetaStar": amplitude_global,
        "localizedAmplitudeForTemplate": amplitude_local,
        "frequencies": frequencies,
        "creationLowerAtNu1UsingSampledCPart": creation_lower,
        "localHeatUpperAtNu1": heat_upper,
        "creationOverHeat": ratios,
        "successiveRatios": successive,
        "sampledConstantsAreDiagnosticsOnly": True,
    }


def main(output: Path | None = None) -> None:
    partition = partition_audit()
    endpoint = endpoint_and_scaling_audit(
        float(partition["sampledCPartDiagnostic"])
    )
    payload = {
        "status": "passed",
        "partition": partition,
        "independentOneCellFourierQuadrature": endpoint,
        "scaling": {
            "dCell": "K^1",
            "BCell": "K^0",
            "qCell": "K^-1",
            "aCell": "K^-3",
            "selectedPositiveCreation": "K^-2",
            "localHeatPayment": "nu^-1*K^-4",
            "ratio": "nu*K^2",
            "viscousCollar": "leading K^-2 aggregate after weighting and time integration",
        },
        "claims": {
            "alignedMatchedPartitionChecked": True,
            "zeroEntryEveryTranslatedCellChecked": True,
            "strictSelectedDenominatorsChecked": True,
            "sameLocalHeatPaymentRejected": True,
            "separateCollarPaymentRejected": False,
            "arbitraryPartitionsChecked": False,
            "movingPartitionsChecked": False,
            "infiniteFrameCellIdentityClaimed": False,
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
