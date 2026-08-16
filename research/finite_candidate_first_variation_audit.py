#!/usr/bin/env python3
"""Exact first variations at the refined finite R0.17 candidate.

The candidate lies on the antisymmetric chart

    (t_P,t_Q,t_B,t_D) = (p,-p,q,-q),

with conic parameters m=429/2500, n=4271/10000 and equal-amplitude
variable x=26213/10000.  It is a rationalized Newton refinement of the clean
R0.17 Hessian point.

This script differentiates the complete signed fifth-order tree again at the
finite point.  Unlike the finite-value audit, independent variations of the
four chart coordinates destroy the common normalization inside a pair.  The
input jets therefore include the full delta-dependent unit normalization

    sqrt(6) (N+tM)/|N+tM|,

expanded exactly through the order needed by the fifth-order Laurent tree.
The conic parameters make every leading square root rational.  All remaining
coefficients use Fraction arithmetic.

The output gives the four chart derivatives and the derivative in x.  It is a
finite-order diagnostic, not a global polarization optimization or a PDE
estimate.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
import hashlib
import json
import math

import fifth_order_tree_audit as tree
import polarization_finite_candidate_audit as finite
import polarization_first_variation_audit as first


Rational = Fraction
Vector = tree.Vector
VectorSeries = tree.VectorSeries
FrequencyExpansion = tree.FrequencyExpansion
Degree = tree.Degree
ScalarSeries = dict[int, Rational]
JetSeries = first.JetSeries

MAXIMUM_INPUT_POWER = tree.MAXIMUM_ORDER
PARAMETER_LABELS = first.PARAMETER_LABELS
ZERO_JET = first.ZERO_JET
M_PARAMETER = Rational(429, 2500)
N_PARAMETER = Rational(4271, 10000)
X_CANDIDATE = Rational(26213, 10000)


def candidate_parameters() -> dict[str, Rational]:
    m = M_PARAMETER
    n = N_PARAMETER
    pump_chart = 24 * m / (1 - 12 * m * m)
    pump_norm = (1 + 12 * m * m) / (1 - 12 * m * m)
    catalyst_chart = 6 * n / (1 - 3 * n * n)
    catalyst_norm = (1 + 3 * n * n) / (1 - 3 * n * n)
    if 1 + pump_chart * pump_chart / 12 != pump_norm * pump_norm:
        raise AssertionError("The pump conic identity failed.")
    if 1 + catalyst_chart * catalyst_chart / 3 != catalyst_norm * catalyst_norm:
        raise AssertionError("The catalyst conic identity failed.")
    return {
        "pumpChart": pump_chart,
        "pumpNorm": pump_norm,
        "catalystChart": catalyst_chart,
        "catalystNorm": catalyst_norm,
    }


def scalar_series_multiply(
    left: ScalarSeries,
    right: ScalarSeries,
    maximum_power: int,
) -> ScalarSeries:
    result: ScalarSeries = {}
    for left_power, left_value in left.items():
        for right_power, right_value in right.items():
            power = left_power + right_power
            if power > maximum_power:
                continue
            result[power] = result.get(power, tree.ZERO_R) + (
                left_value * right_value
            )
    return {
        power: value for power, value in result.items() if value != 0
    }


def scalar_series_scale(value: Rational, series: ScalarSeries) -> ScalarSeries:
    return {
        power: value * coefficient
        for power, coefficient in series.items()
        if value * coefficient != 0
    }


def scalar_vector_series_multiply(
    scalar: ScalarSeries,
    vector: VectorSeries,
    maximum_power: int,
) -> VectorSeries:
    result: VectorSeries = {}
    for scalar_power, scalar_value in scalar.items():
        for vector_power, vector_value in vector.items():
            power = scalar_power + vector_power
            if power > maximum_power:
                continue
            result[power] = tree.vector_add(
                result.get(power, tree.ZERO_VECTOR),
                tree.vector_scale(scalar_value, vector_value),
            )
    return {
        power: value
        for power, value in result.items()
        if not tree.is_zero_vector(value)
    }


def rational_square_root(value: Rational) -> Rational:
    if value <= 0:
        raise ValueError("A normalization constant must be positive.")
    numerator = math.isqrt(value.numerator)
    denominator = math.isqrt(value.denominator)
    if numerator * numerator != value.numerator:
        raise ValueError("The normalization numerator is not a square.")
    if denominator * denominator != value.denominator:
        raise ValueError("The normalization denominator is not a square.")
    return Rational(numerator, denominator)


def inverse_square_root_series(
    value: ScalarSeries,
    maximum_power: int,
) -> ScalarSeries:
    """Return G with value*G^2 = 1 through the requested power."""

    constant = value.get(0, tree.ZERO_R)
    root = rational_square_root(constant)
    result: ScalarSeries = {0: 1 / root}
    for power in range(1, maximum_power + 1):
        square = scalar_series_multiply(result, result, power)
        product = scalar_series_multiply(value, square, power)
        known = product.get(power, tree.ZERO_R)
        result[power] = -known / (2 * constant * result[0])
        if result[power] == 0:
            del result[power]

    square = scalar_series_multiply(result, result, maximum_power)
    product = scalar_series_multiply(value, square, maximum_power)
    if product.get(0, tree.ZERO_R) != 1:
        raise AssertionError("The inverse-square-root constant failed.")
    if any(
        product.get(power, tree.ZERO_R) != 0
        for power in range(1, maximum_power + 1)
    ):
        raise AssertionError("The inverse-square-root recurrence failed.")
    return result


def normalized_input_jet(
    index: int,
    chart: Rational,
    frequency: FrequencyExpansion,
    numerator: VectorSeries,
) -> JetSeries:
    tangent = first.tangent_series(frequency, numerator)
    unnormalized = tree.series_add(
        numerator,
        tree.series_scale(chart, tangent),
        0,
        MAXIMUM_INPUT_POWER,
    )
    norm_squared = scalar_series_scale(
        Rational(1, 6),
        first.scalar_series_dot(unnormalized, unnormalized),
    )
    inverse_norm = inverse_square_root_series(
        norm_squared,
        MAXIMUM_INPUT_POWER,
    )
    base = scalar_vector_series_multiply(
        inverse_norm,
        unnormalized,
        MAXIMUM_INPUT_POWER,
    )

    tangent_norm_squared = scalar_series_scale(
        Rational(1, 6),
        first.scalar_series_dot(tangent, tangent),
    )
    inverse_norm_squared = scalar_series_multiply(
        inverse_norm,
        inverse_norm,
        MAXIMUM_INPUT_POWER,
    )
    inverse_norm_cubed = scalar_series_multiply(
        inverse_norm_squared,
        inverse_norm,
        MAXIMUM_INPUT_POWER,
    )
    inverse_norm_derivative = scalar_series_scale(
        -chart,
        scalar_series_multiply(
            tangent_norm_squared,
            inverse_norm_cubed,
            MAXIMUM_INPUT_POWER,
        ),
    )
    derivative = tree.series_add(
        scalar_vector_series_multiply(
            inverse_norm,
            tangent,
            MAXIMUM_INPUT_POWER,
        ),
        scalar_vector_series_multiply(
            inverse_norm_derivative,
            unnormalized,
            MAXIMUM_INPUT_POWER,
        ),
        0,
        MAXIMUM_INPUT_POWER,
    )

    entries: list[VectorSeries] = [base, {}, {}, {}, {}]
    entries[index + 1] = derivative
    return tuple(entries)  # type: ignore[return-value]


def initial_jets() -> tuple[JetSeries, ...]:
    parameters = candidate_parameters()
    charts = (
        parameters["pumpChart"],
        -parameters["pumpChart"],
        parameters["catalystChart"],
        -parameters["catalystChart"],
    )
    positive = tuple(
        normalized_input_jet(index, chart, frequency, numerator)
        for index, (chart, frequency, numerator) in enumerate(
            zip(
                charts,
                tree.POSITIVE_FREQUENCIES,
                tree.POSITIVE_POLARIZATION_SERIES,
                strict=True,
            )
        )
    )
    return positive + positive


def differentiated_tree() -> list[dict[Degree, JetSeries]]:
    frequencies = tree.signed_frequencies()
    jets = initial_jets()
    coefficients: list[dict[Degree, JetSeries]] = [
        {} for _ in range(tree.MAXIMUM_ORDER + 1)
    ]
    for index, jet in enumerate(jets):
        degree = tuple(
            int(index == coordinate) for coordinate in range(len(frequencies))
        )
        coefficients[0][degree] = jet

    for order in range(tree.MAXIMUM_ORDER):
        minimum = -(order + 1)
        maximum = tree.MAXIMUM_ORDER - (order + 1)
        output: dict[Degree, JetSeries] = {}
        for left_order in range(order + 1):
            right_order = order - left_order
            for left_degree, left in coefficients[left_order].items():
                for right_degree, right in coefficients[right_order].items():
                    degree = tree.degree_add(left_degree, right_degree)
                    value = first.jet_scale(
                        Rational(1, order + 1),
                        first.jet_bilinear(
                            left_degree,
                            left,
                            right_degree,
                            right,
                            frequencies,
                            minimum,
                            maximum,
                        ),
                    )
                    output[degree] = first.jet_add(
                        output.get(degree, ZERO_JET),
                        value,
                        minimum,
                        maximum,
                    )
        coefficients[order + 1] = output
    return coefficients


def aggregate_limit() -> tuple[
    dict[FrequencyExpansion, dict[tuple[int, int], tuple[Vector, ...]]],
    list[int],
]:
    frequencies = tree.signed_frequencies()
    coefficients = differentiated_tree()
    aggregated: dict[
        tuple[FrequencyExpansion, tuple[int, int]],
        JetSeries,
    ] = {}
    for degree, jet in coefficients[5].items():
        output = tree.degree_frequency(degree, frequencies)
        catalyst_degree = tree.catalyst_degrees(degree)
        key = output, catalyst_degree
        aggregated[key] = first.jet_add(
            aggregated.get(key, ZERO_JET),
            jet,
            -5,
            0,
        )

    pole_counts = [0] * 5
    by_frequency: dict[
        FrequencyExpansion,
        dict[tuple[int, int], tuple[Vector, ...]],
    ] = defaultdict(dict)
    for (output, catalyst_degree), jet in aggregated.items():
        for component in range(5):
            for power in range(-5, 0):
                if not tree.is_zero_vector(
                    jet[component].get(power, tree.ZERO_VECTOR)
                ):
                    pole_counts[component] += 1
        constants = tuple(
            jet[component].get(0, tree.ZERO_VECTOR)
            for component in range(5)
        )
        if any(not tree.is_zero_vector(value) for value in constants):
            by_frequency[output][catalyst_degree] = constants
    return dict(by_frequency), pole_counts


def polynomial_derivative(polynomial: dict[int, Rational]) -> dict[int, Rational]:
    return {
        power - 1: power * coefficient
        for power, coefficient in polynomial.items()
        if power > 0 and coefficient != 0
    }


def equal_amplitude_from_total_degree(
    polynomial: dict[int, Rational],
) -> dict[int, Rational]:
    result: dict[int, Rational] = {}
    for epsilon_power, coefficient in polynomial.items():
        if epsilon_power % 2 != 0:
            raise AssertionError("An odd equal-amplitude power survived.")
        x_power = epsilon_power // 2
        result[x_power] = result.get(x_power, tree.ZERO_R) + (
            coefficient / 2**epsilon_power
        )
    return {
        power: coefficient
        for power, coefficient in result.items()
        if coefficient != 0
    }


def rational_digest(value: Rational) -> str:
    return hashlib.sha256(
        f"{value.numerator}/{value.denominator}".encode("ascii")
    ).hexdigest()


def audit() -> dict[str, object]:
    by_frequency, pole_counts = aggregate_limit()
    total_jets = first.energy_jets(by_frequency)
    target_jets = first.energy_jets(
        by_frequency,
        {tree.NEXT_A_POSITIVE, tree.NEXT_A_NEGATIVE},
    )
    total = tuple(
        equal_amplitude_from_total_degree(polynomial)
        for polynomial in total_jets
    )
    target = tuple(
        equal_amplitude_from_total_degree(polynomial)
        for polynomial in target_jets
    )
    external = tuple(
        {
            power: total[index].get(power, tree.ZERO_R)
            - target[index].get(power, tree.ZERO_R)
            for power in set(total[index]).union(target[index])
            if total[index].get(power, tree.ZERO_R)
            != target[index].get(power, tree.ZERO_R)
        }
        for index in range(5)
    )

    x_value = X_CANDIDATE
    target_value = finite.evaluate(target[0], x_value)
    external_value = finite.evaluate(external[0], x_value)
    denominator = target_value * target_value
    derivatives: list[Rational] = []
    for index in range(1, 5):
        target_derivative = finite.evaluate(target[index], x_value)
        external_derivative = finite.evaluate(external[index], x_value)
        derivatives.append(
            (
                external_derivative * target_value
                - external_value * target_derivative
            )
            / denominator
        )

    target_x_derivative = finite.evaluate(
        polynomial_derivative(target[0]),
        x_value,
    )
    external_x_derivative = finite.evaluate(
        polynomial_derivative(external[0]),
        x_value,
    )
    x_derivative = (
        external_x_derivative * target_value
        - external_value * target_x_derivative
    ) / denominator
    ratio = external_value / target_value
    target_fraction = target_value / (target_value + external_value)

    parameters = candidate_parameters()
    return {
        "scope": "first variations at the refined finite R0.17 candidate",
        "parameters": {
            "m": str(M_PARAMETER),
            "n": str(N_PARAMETER),
            "pumpChart": str(parameters["pumpChart"]),
            "catalystChart": str(parameters["catalystChart"]),
            "x": str(X_CANDIDATE),
        },
        "aggregatedFrequencyCount": len(by_frequency),
        "uncancelledLaurentPoleCounts": {
            label: count
            for label, count in zip(
                ("base", *PARAMETER_LABELS),
                pole_counts,
                strict=True,
            )
        },
        "externalOverTarget": {
            "decimal": float(ratio),
            "exactDigest": rational_digest(ratio),
        },
        "targetFractionPercent": 100 * float(target_fraction),
        "chartDerivatives": [
            {
                "parameter": label,
                "decimal": float(value),
                "sign": -1 if value < 0 else (1 if value > 0 else 0),
                "exactDigest": rational_digest(value),
            }
            for label, value in zip(
                PARAMETER_LABELS,
                derivatives,
                strict=True,
            )
        ],
        "amplitudeXDerivative": {
            "decimal": float(x_derivative),
            "sign": -1 if x_derivative < 0 else (1 if x_derivative > 0 else 0),
            "exactDigest": rational_digest(x_derivative),
        },
    }


def validate(result: dict[str, object]) -> None:
    assert result["parameters"]["m"] == "429/2500"
    assert result["parameters"]["n"] == "4271/10000"
    assert result["parameters"]["x"] == "26213/10000"
    assert result["aggregatedFrequencyCount"] == 334
    assert all(
        count == 0
        for count in result["uncancelledLaurentPoleCounts"].values()
    )
    assert abs(
        result["externalOverTarget"]["decimal"] - 15.801443619697901
    ) < 1e-12
    assert result["externalOverTarget"]["exactDigest"] == (
        "b03c07a99a7b19d3f3198e6099a19fa6a1335b0b8ad1db6f6f3a72f0884d7cd2"
    )
    assert result["targetFractionPercent"] > 5.9518
    assert len(result["chartDerivatives"]) == 4
    assert max(
        abs(value["decimal"]) for value in result["chartDerivatives"]
    ) < 0.001
    assert abs(result["amplitudeXDerivative"]["decimal"]) < 0.0004


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    result = audit()
    if arguments.check:
        validate(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
