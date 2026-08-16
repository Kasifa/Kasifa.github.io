#!/usr/bin/env python3
"""Exact finite polarization improvement for the R0.15 quotient.

The R0.15 angular gradient suggests opposite rotations inside each pump and
catalyst pair.  This script chooses finite rational chart parameters

    t_P = p,  t_Q = -p,  t_B = q,  t_D = -q,

with p and q rationally parameterized so the leading normalization factors
are also rational:

    p = 24 m/(1-12 m^2),  1+p^2/12 = u^2,
    q =  6 n/(1- 3 n^2),  1+q^2/ 3 = v^2.

The concrete choice is m=28/155, n=7/25 and x=5377/5000.  Because opposite
members have equal magnitudes, the full delta-dependent pump normalization is
common to the pump pair and the catalyst normalization is common to the
catalyst pair.  After exact cancellation of every negative Laurent power,
only the rational leading factors u and v affect the limiting constant.

The resulting target and external energies are exact rational numbers.  The
script proves that their quotient is below the already certified rational
lower bound 45.739348 for the old fixed-polarization optimum, hence gives a
strict finite polarization improvement without floating-point optimization.

This remains a finite fifth-order calculation and is not a PDE estimate.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
import hashlib
import json

import fifth_order_tree_audit as tree
import polarization_first_variation_audit as first
import two_amplitude_global_audit as amplitude


Rational = Fraction
Vector = tree.Vector
VectorSeries = tree.VectorSeries
FrequencyExpansion = tree.FrequencyExpansion
Polynomial = tree.Polynomial

M_PARAMETER = Rational(28, 155)
N_PARAMETER = Rational(7, 25)
X_CANDIDATE = Rational(5377, 5000)


def conic_parameters() -> dict[str, Rational]:
    m = M_PARAMETER
    n = N_PARAMETER
    pump_chart = 24 * m / (1 - 12 * m * m)
    pump_norm = (1 + 12 * m * m) / (1 - 12 * m * m)
    catalyst_chart = 6 * n / (1 - 3 * n * n)
    catalyst_norm = (1 + 3 * n * n) / (1 - 3 * n * n)
    if 1 + pump_chart * pump_chart / 12 != pump_norm * pump_norm:
        raise AssertionError("The pump conic normalization identity failed.")
    if 1 + catalyst_chart * catalyst_chart / 3 != catalyst_norm * catalyst_norm:
        raise AssertionError("The catalyst conic normalization identity failed.")
    return {
        "pumpChart": pump_chart,
        "pumpNorm": pump_norm,
        "catalystChart": catalyst_chart,
        "catalystNorm": catalyst_norm,
    }


def perturbed_positive_polarizations() -> tuple[VectorSeries, ...]:
    parameters = conic_parameters()
    chart_values = (
        parameters["pumpChart"],
        -parameters["pumpChart"],
        parameters["catalystChart"],
        -parameters["catalystChart"],
    )
    result = []
    for frequency, polarization, chart in zip(
        tree.POSITIVE_FREQUENCIES,
        tree.POSITIVE_POLARIZATION_SERIES,
        chart_values,
        strict=True,
    ):
        tangent = first.tangent_series(frequency, polarization)
        result.append(tree.series_add(
            polarization,
            tree.series_scale(chart, tangent),
            0,
            2,
        ))
    return tuple(result)


def normalized_aggregate() -> tuple[
    dict[FrequencyExpansion, dict[tuple[int, int], Vector]],
    int,
]:
    positive = perturbed_positive_polarizations()
    initial = positive + positive
    frequencies = tree.signed_frequencies()
    coefficients = tree.pure_tree_coefficients(frequencies, initial)
    aggregated: dict[
        tuple[FrequencyExpansion, tuple[int, int]],
        VectorSeries,
    ] = {}
    for degree, value in coefficients[5].items():
        output = tree.degree_frequency(degree, frequencies)
        catalyst_degree = tree.catalyst_degrees(degree)
        key = output, catalyst_degree
        aggregated[key] = tree.series_add(
            aggregated.get(key, {}),
            value,
            -5,
            0,
        )

    parameters = conic_parameters()
    pump_norm = parameters["pumpNorm"]
    catalyst_norm = parameters["catalystNorm"]
    pole_count = 0
    by_frequency: dict[
        FrequencyExpansion,
        dict[tuple[int, int], Vector],
    ] = defaultdict(dict)
    for (output, catalyst_degree), value in aggregated.items():
        for power in range(-5, 0):
            if not tree.is_zero_vector(value.get(power, tree.ZERO_VECTOR)):
                pole_count += 1
        constant = value.get(0, tree.ZERO_VECTOR)
        if tree.is_zero_vector(constant):
            continue
        catalyst_count = sum(catalyst_degree)
        pump_count = 6 - catalyst_count
        normalization = (
            pump_norm**pump_count * catalyst_norm**catalyst_count
        )
        by_frequency[output][catalyst_degree] = tree.vector_scale(
            1 / normalization,
            constant,
        )
    return dict(by_frequency), pole_count


def equal_amplitude_in_x(polynomial: Polynomial) -> dict[int, Rational]:
    epsilon = tree.substitute_equal_amplitudes(polynomial, 1)
    result: dict[int, Rational] = {}
    for epsilon_power, coefficient in epsilon.items():
        if epsilon_power % 2 != 0:
            raise AssertionError("An odd equal-amplitude power survived.")
        result[epsilon_power // 2] = coefficient / 2**epsilon_power
    return result


def evaluate(polynomial: dict[int, Rational], value: Rational) -> Rational:
    return sum(
        (coefficient * value**power for power, coefficient in polynomial.items()),
        start=Rational(0),
    )


def rational_digest(value: Rational) -> str:
    return hashlib.sha256(
        f"{value.numerator}/{value.denominator}".encode("ascii")
    ).hexdigest()


def audit() -> dict[str, object]:
    by_frequency, pole_count = normalized_aggregate()
    total = tree.energy_polynomial(by_frequency)
    target = tree.energy_polynomial(
        by_frequency,
        {tree.NEXT_A_POSITIVE, tree.NEXT_A_NEGATIVE},
    )
    external: Polynomial = {
        powers: total.get(powers, tree.ZERO_R) - target.get(powers, tree.ZERO_R)
        for powers in set(total).union(target)
        if total.get(powers, tree.ZERO_R) != target.get(powers, tree.ZERO_R)
    }
    target_x = equal_amplitude_in_x(target)
    external_x = equal_amplitude_in_x(external)
    target_value = evaluate(target_x, X_CANDIDATE)
    external_value = evaluate(external_x, X_CANDIDATE)
    if target_value <= 0:
        raise AssertionError("The finite candidate has no positive target energy.")
    ratio = external_value / target_value
    old_rational_lower = Rational(
        int(amplitude.COMPLEX_LOWER_BOUND.p),
        int(amplitude.COMPLEX_LOWER_BOUND.q),
    )
    if not ratio < old_rational_lower:
        raise AssertionError("The finite candidate did not strictly improve R0.15.")
    target_fraction = target_value / (target_value + external_value)
    parameters = conic_parameters()
    return {
        "scope": "finite fifth-order polarization candidate",
        "parameters": {
            "m": str(M_PARAMETER),
            "n": str(N_PARAMETER),
            "pumpChart": str(parameters["pumpChart"]),
            "catalystChart": str(parameters["catalystChart"]),
            "pumpNorm": str(parameters["pumpNorm"]),
            "catalystNorm": str(parameters["catalystNorm"]),
            "x": str(X_CANDIDATE),
        },
        "aggregatedFrequencyCount": len(by_frequency),
        "uncancelledLaurentPoleCount": pole_count,
        "externalOverTarget": {
            "decimal": float(ratio),
            "exactDigest": rational_digest(ratio),
        },
        "oldFixedPolarizationRationalLowerBound": str(old_rational_lower),
        "strictImprovementMarginOverOldLowerBound": float(
            old_rational_lower - ratio
        ),
        "targetFraction": {
            "decimal": float(target_fraction),
            "percent": 100 * float(target_fraction),
            "exactDigest": rational_digest(target_fraction),
        },
        "targetValueDigest": rational_digest(target_value),
        "externalValueDigest": rational_digest(external_value),
    }


def validate(result: dict[str, object]) -> None:
    assert result["parameters"]["m"] == "28/155"
    assert result["parameters"]["n"] == "7/25"
    assert result["parameters"]["x"] == "5377/5000"
    assert result["aggregatedFrequencyCount"] == 332
    assert result["uncancelledLaurentPoleCount"] == 0
    assert result["externalOverTarget"]["decimal"] < 18.036
    assert result["externalOverTarget"]["exactDigest"] == (
        "e6de533aa93feb1d0e61cae4ac789805e0aa829a820ab79f72d4161bcbc07998"
    )
    assert result["strictImprovementMarginOverOldLowerBound"] > 27.7
    assert result["targetFraction"]["percent"] > 5.253
    assert result["targetFraction"]["exactDigest"] == (
        "f76ed408ec4a94a05cdb89d2a4d374073733d07c11c00624e37b259f54254620"
    )
    assert result["targetValueDigest"] == (
        "7d576bd4525e76444f8410ca984a81c08f3fe7024971c25332a56d37a3684bf4"
    )
    assert result["externalValueDigest"] == (
        "6e0a43a4b5ccac1b268a834cdd1384c9c390b129416f0dac3bea4cf4b8a43ac8"
    )


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
