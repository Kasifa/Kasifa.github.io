#!/usr/bin/env python3
"""Exact joint Hessian at the clean finite R0.17 candidate.

The candidate is

    m=6/35, n=3/7, x=37/14,

which gives antisymmetric chart coordinates

    (t_P,t_Q,t_B,t_D)=(5040/793,-5040/793,63/11,-63/11).

This script propagates the base value, four first derivatives and ten second
derivatives through the complete signed fifth-order Laurent tree.  Each input
jet includes the full delta-dependent unit normalization.  It then evaluates
the amplitude-polarization Hessian of the external/target quotient at the
rational x value.

The pair-exchange symmetry splits common and opposite rotations.  In
particular, the common catalyst curvature decides whether the negative
direction found at the old R0.15 point survives at this finite candidate.
The calculation is finite-order and does not estimate a PDE remainder.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
import hashlib
import json

import numpy as np
import sympy as sp

import fifth_order_tree_audit as tree
import finite_candidate_first_variation_audit as finite_first
import polarization_first_variation_audit as first
import polarization_second_variation_audit as second


Rational = Fraction
Vector = tree.Vector
VectorSeries = tree.VectorSeries
FrequencyExpansion = tree.FrequencyExpansion
Degree = tree.Degree
DerivativeKey = second.DerivativeKey
JetSeries = second.JetSeries

M_PARAMETER = Rational(6, 35)
N_PARAMETER = Rational(3, 7)
X_CANDIDATE = Rational(37, 14)
MAXIMUM_INPUT_POWER = tree.MAXIMUM_ORDER


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
    norm_squared = finite_first.scalar_series_scale(
        Rational(1, 6),
        first.scalar_series_dot(unnormalized, unnormalized),
    )
    inverse_norm = finite_first.inverse_square_root_series(
        norm_squared,
        MAXIMUM_INPUT_POWER,
    )
    base = finite_first.scalar_vector_series_multiply(
        inverse_norm,
        unnormalized,
        MAXIMUM_INPUT_POWER,
    )

    tangent_norm_squared = finite_first.scalar_series_scale(
        Rational(1, 6),
        first.scalar_series_dot(tangent, tangent),
    )
    inverse_norm_squared = finite_first.scalar_series_multiply(
        inverse_norm,
        inverse_norm,
        MAXIMUM_INPUT_POWER,
    )
    inverse_norm_cubed = finite_first.scalar_series_multiply(
        inverse_norm_squared,
        inverse_norm,
        MAXIMUM_INPUT_POWER,
    )
    inverse_norm_fourth = finite_first.scalar_series_multiply(
        inverse_norm_squared,
        inverse_norm_squared,
        MAXIMUM_INPUT_POWER,
    )
    inverse_norm_fifth = finite_first.scalar_series_multiply(
        inverse_norm_fourth,
        inverse_norm,
        MAXIMUM_INPUT_POWER,
    )
    inverse_norm_derivative = finite_first.scalar_series_scale(
        -chart,
        finite_first.scalar_series_multiply(
            tangent_norm_squared,
            inverse_norm_cubed,
            MAXIMUM_INPUT_POWER,
        ),
    )
    derivative = tree.series_add(
        finite_first.scalar_vector_series_multiply(
            inverse_norm,
            tangent,
            MAXIMUM_INPUT_POWER,
        ),
        finite_first.scalar_vector_series_multiply(
            inverse_norm_derivative,
            unnormalized,
            MAXIMUM_INPUT_POWER,
        ),
        0,
        MAXIMUM_INPUT_POWER,
    )

    first_second_term = finite_first.scalar_series_scale(
        Rational(-1),
        finite_first.scalar_series_multiply(
            tangent_norm_squared,
            inverse_norm_cubed,
            MAXIMUM_INPUT_POWER,
        ),
    )
    tangent_norm_fourth = finite_first.scalar_series_multiply(
        tangent_norm_squared,
        tangent_norm_squared,
        MAXIMUM_INPUT_POWER,
    )
    second_second_term = finite_first.scalar_series_scale(
        3 * chart * chart,
        finite_first.scalar_series_multiply(
            tangent_norm_fourth,
            inverse_norm_fifth,
            MAXIMUM_INPUT_POWER,
        ),
    )
    inverse_norm_second_derivative = {
        power: first_second_term.get(power, tree.ZERO_R)
        + second_second_term.get(power, tree.ZERO_R)
        for power in set(first_second_term).union(second_second_term)
        if first_second_term.get(power, tree.ZERO_R)
        + second_second_term.get(power, tree.ZERO_R)
        != 0
    }
    second_derivative = tree.series_add(
        finite_first.scalar_vector_series_multiply(
            finite_first.scalar_series_scale(
                Rational(2),
                inverse_norm_derivative,
            ),
            tangent,
            MAXIMUM_INPUT_POWER,
        ),
        finite_first.scalar_vector_series_multiply(
            inverse_norm_second_derivative,
            unnormalized,
            MAXIMUM_INPUT_POWER,
        ),
        0,
        MAXIMUM_INPUT_POWER,
    )

    return {
        second.BASE_KEY: base,
        (index,): derivative,
        (index, index): second_derivative,
    }


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
                    value = second.jet_scale(
                        Rational(1, order + 1),
                        second.jet_bilinear(
                            left_degree,
                            left,
                            right_degree,
                            right,
                            frequencies,
                            minimum,
                            maximum,
                        ),
                    )
                    output[degree] = second.jet_add(
                        output.get(degree, {}),
                        value,
                        minimum,
                        maximum,
                    )
        coefficients[order + 1] = output
    return coefficients


def aggregate_limit() -> tuple[
    dict[
        FrequencyExpansion,
        dict[tuple[int, int], dict[DerivativeKey, Vector]],
    ],
    dict[DerivativeKey, int],
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
        aggregated[key] = second.jet_add(
            aggregated.get(key, {}),
            jet,
            -5,
            0,
        )

    pole_counts = {key: 0 for key in second.ALL_KEYS}
    by_frequency: dict[
        FrequencyExpansion,
        dict[tuple[int, int], dict[DerivativeKey, Vector]],
    ] = defaultdict(dict)
    for (output, catalyst_degree), jet in aggregated.items():
        constants: dict[DerivativeKey, Vector] = {}
        for key in second.ALL_KEYS:
            component = jet.get(key, {})
            for power in range(-5, 0):
                if not tree.is_zero_vector(
                    component.get(power, tree.ZERO_VECTOR)
                ):
                    pole_counts[key] += 1
            constant = component.get(0, tree.ZERO_VECTOR)
            if not tree.is_zero_vector(constant):
                constants[key] = constant
        if constants:
            by_frequency[output][catalyst_degree] = constants
    return dict(by_frequency), pole_counts


def rational_digest(value: sp.Rational) -> str:
    return hashlib.sha256(
        f"{int(value.p)}/{int(value.q)}".encode("ascii")
    ).hexdigest()


def evaluate(expression: sp.Expr) -> sp.Rational:
    value = sp.cancel(expression.subs(
        second.X_VAR,
        sp.Rational(X_CANDIDATE.numerator, X_CANDIDATE.denominator),
    ))
    if not value.is_Rational:
        raise AssertionError("The candidate evaluation is not rational.")
    return value


def quotient_record(
    external: dict[DerivativeKey, sp.Expr],
    target: dict[DerivativeKey, sp.Expr],
) -> dict[str, object]:
    base_external = external[second.BASE_KEY]
    base_target = target[second.BASE_KEY]
    quotient = sp.cancel(base_external / base_target)
    gradient_expressions = [
        sp.cancel(
            (
                external[(index,)] * base_target
                - base_external * target[(index,)]
            )
            / base_target**2
        )
        for index in range(4)
    ]
    hessian_expressions: list[list[sp.Expr]] = []
    for left in range(4):
        row = []
        for right in range(4):
            key = tuple(sorted((left, right)))
            row.append(sp.cancel(
                external[key] / base_target
                - external[(left,)] * target[(right,)] / base_target**2
                - external[(right,)] * target[(left,)] / base_target**2
                - base_external * target[key] / base_target**2
                + 2
                * base_external
                * target[(left,)]
                * target[(right,)]
                / base_target**3
            ))
        hessian_expressions.append(row)

    amplitude_first = evaluate(sp.diff(quotient, second.X_VAR))
    amplitude_second = evaluate(sp.diff(quotient, second.X_VAR, 2))
    gradient = [evaluate(value) for value in gradient_expressions]
    mixed = [
        evaluate(sp.diff(value, second.X_VAR))
        for value in gradient_expressions
    ]
    hessian = [
        [evaluate(value) for value in row]
        for row in hessian_expressions
    ]

    exact_symmetry_checks = {
        "pumpGradientSumZero": gradient[0] + gradient[1] == 0,
        "catalystGradientSumZero": gradient[2] + gradient[3] == 0,
        "pumpMixedSumZero": mixed[0] + mixed[1] == 0,
        "catalystMixedSumZero": mixed[2] + mixed[3] == 0,
        "pumpDiagonalEqual": hessian[0][0] == hessian[1][1],
        "catalystDiagonalEqual": hessian[2][2] == hessian[3][3],
        "crossParallelEqual": hessian[0][2] == hessian[1][3],
        "crossOppositeEqual": hessian[0][3] == hessian[1][2],
    }
    if not all(exact_symmetry_checks.values()):
        raise AssertionError("The pair-exchange symmetry failed.")

    def quadratic(direction: tuple[int, int, int, int]) -> sp.Rational:
        return sum(
            (
                direction[left] * hessian[left][right] * direction[right]
                for left in range(4)
                for right in range(4)
            ),
            start=sp.Rational(0),
        )

    def bilinear(
        left_direction: tuple[int, int, int, int],
        right_direction: tuple[int, int, int, int],
    ) -> sp.Rational:
        return sum(
            (
                left_direction[left]
                * hessian[left][right]
                * right_direction[right]
                for left in range(4)
                for right in range(4)
            ),
            start=sp.Rational(0),
        )

    directions = {
        "commonPump": (1, 1, 0, 0),
        "oppositePump": (1, -1, 0, 0),
        "commonCatalyst": (0, 0, 1, 1),
        "oppositeCatalyst": (0, 0, 1, -1),
    }
    curvatures = {
        label: quadratic(direction)
        for label, direction in directions.items()
    }
    common_cross = bilinear(
        directions["commonPump"],
        directions["commonCatalyst"],
    )
    opposite_cross = bilinear(
        directions["oppositePump"],
        directions["oppositeCatalyst"],
    )
    symmetric_block = sp.Matrix([
        [curvatures["commonPump"], common_cross],
        [common_cross, curvatures["commonCatalyst"]],
    ])
    opposite_pump_mixed = mixed[0] - mixed[1]
    opposite_catalyst_mixed = mixed[2] - mixed[3]
    antisymmetric_joint_block = sp.Matrix([
        [
            amplitude_second,
            opposite_pump_mixed,
            opposite_catalyst_mixed,
        ],
        [
            opposite_pump_mixed,
            curvatures["oppositePump"],
            opposite_cross,
        ],
        [
            opposite_catalyst_mixed,
            opposite_cross,
            curvatures["oppositeCatalyst"],
        ],
    ])
    sylvester_minors = {
        "symmetricFirst": symmetric_block[:1, :1].det(),
        "symmetricDeterminant": symmetric_block.det(),
        "antisymmetricJointFirst": antisymmetric_joint_block[:1, :1].det(),
        "antisymmetricJointSecond": antisymmetric_joint_block[:2, :2].det(),
        "antisymmetricJointDeterminant": antisymmetric_joint_block.det(),
    }
    joint_positive_definite = all(
        value > 0 for value in sylvester_minors.values()
    )

    hessian_decimal = np.asarray([
        [float(value) for value in row]
        for row in hessian
    ])
    mixed_decimal = np.asarray([float(value) for value in mixed])
    reduced_decimal = hessian_decimal - np.outer(
        mixed_decimal,
        mixed_decimal,
    ) / float(amplitude_second)

    return {
        "externalOverTargetDecimal": float(evaluate(quotient)),
        "amplitudeFirstDerivative": {
            "decimal": float(amplitude_first),
            "exactDigest": rational_digest(amplitude_first),
        },
        "amplitudeSecondDerivative": {
            "decimal": float(amplitude_second),
            "exactDigest": rational_digest(amplitude_second),
        },
        "chartGradient": [
            {
                "parameter": label,
                "decimal": float(value),
                "exactDigest": rational_digest(value),
            }
            for label, value in zip(
                first.PARAMETER_LABELS,
                gradient,
                strict=True,
            )
        ],
        "amplitudePolarizationMixedChartDecimal": [
            float(value) for value in mixed
        ],
        "polarizationHessianChartDecimal": hessian_decimal.tolist(),
        "polarizationHessianChartEigenvaluesDecimal": np.linalg.eigvalsh(
            hessian_decimal
        ).tolist(),
        "amplitudeOptimizedChartEigenvaluesDecimal": np.linalg.eigvalsh(
            reduced_decimal
        ).tolist(),
        "exactPairSymmetryChecks": exact_symmetry_checks,
        "pairDirectionCurvatures": {
            label: {
                "decimal": float(value),
                "sign": -1 if value < 0 else (1 if value > 0 else 0),
                "exactDigest": rational_digest(value),
            }
            for label, value in curvatures.items()
        },
        "jointHessianSylvesterMinors": {
            label: {
                "decimal": float(value),
                "sign": -1 if value < 0 else (1 if value > 0 else 0),
                "exactDigest": rational_digest(value),
            }
            for label, value in sylvester_minors.items()
        },
        "jointHessianPositiveDefiniteCertified": joint_positive_definite,
    }


def audit() -> dict[str, object]:
    by_frequency, pole_counts = aggregate_limit()
    total_polynomials = second.energy_jets(by_frequency)
    target_polynomials = second.energy_jets(
        by_frequency,
        {tree.NEXT_A_POSITIVE, tree.NEXT_A_NEGATIVE},
    )
    total = {
        key: second.equal_amplitude_expression(value)
        for key, value in total_polynomials.items()
    }
    target = {
        key: second.equal_amplitude_expression(value)
        for key, value in target_polynomials.items()
    }
    external = {
        key: sp.expand(total[key] - target[key])
        for key in second.ALL_KEYS
    }
    parameters = candidate_parameters()
    return {
        "scope": "joint second variations at the clean R0.17 candidate",
        "parameters": {
            "m": str(M_PARAMETER),
            "n": str(N_PARAMETER),
            "pumpChart": str(parameters["pumpChart"]),
            "catalystChart": str(parameters["catalystChart"]),
            "x": str(X_CANDIDATE),
        },
        "derivativeKeyCount": len(second.ALL_KEYS),
        "aggregatedFrequencyCount": len(by_frequency),
        "uncancelledLaurentPoleCounts": {
            second.key_label(key): count
            for key, count in pole_counts.items()
        },
        "quotient": quotient_record(external, target),
    }


def validate(result: dict[str, object]) -> None:
    assert result["parameters"]["m"] == "6/35"
    assert result["parameters"]["n"] == "3/7"
    assert result["parameters"]["x"] == "37/14"
    assert result["derivativeKeyCount"] == 15
    assert result["aggregatedFrequencyCount"] == 334
    assert all(
        count == 0
        for count in result["uncancelledLaurentPoleCounts"].values()
    )
    quotient = result["quotient"]
    assert abs(
        quotient["externalOverTargetDecimal"] - 15.802476770259613
    ) < 1e-12
    assert all(quotient["exactPairSymmetryChecks"].values())
    assert quotient["amplitudeSecondDerivative"]["decimal"] > 0
    assert all(
        value["sign"] > 0
        for value in quotient["pairDirectionCurvatures"].values()
    )
    assert all(
        value["sign"] > 0
        for value in quotient["jointHessianSylvesterMinors"].values()
    )
    assert quotient["jointHessianSylvesterMinors"][
        "symmetricDeterminant"
    ]["exactDigest"] == (
        "18aec509bc29e549bb4c4d9fb148b2c13c1b920bc6e651be6ff9149a521f1369"
    )
    assert quotient["jointHessianSylvesterMinors"][
        "antisymmetricJointDeterminant"
    ]["exactDigest"] == (
        "154a840ba956afa43a13255bc6f4590f7760a8c6945f2b716e60b8f4d2497a17"
    )
    assert quotient["jointHessianPositiveDefiniteCertified"]


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
