#!/usr/bin/env python3
"""Exact R0.17 improvement with independently tuned pump and catalyst charts.

R0.16 tied the pump and catalyst conic parameters to one scale.  The first
variation at that point showed opposite corrections: the pump rotation had
to decrease while the catalyst rotation had to increase.  This script
separates the two parameters and certifies the refined rational point

    m = 429/2500,
    n = 4271/10000,
    x = 26213/10000.

It recomputes both the R0.16 reference and the new candidate with the complete
signed fifth-order tree.  Every comparison is an exact rational
cross-multiplication; decimal values are included only for reading.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json

import fifth_order_tree_audit as tree
import polarization_finite_candidate_audit as finite


Rational = Fraction

REFERENCE_M = Rational(28, 155)
REFERENCE_N = Rational(7, 25)
REFERENCE_X = Rational(5377, 5000)

CANDIDATE_M = Rational(429, 2500)
CANDIDATE_N = Rational(4271, 10000)
CANDIDATE_X = Rational(26213, 10000)


def rational_digest(value: Rational) -> str:
    return hashlib.sha256(
        f"{value.numerator}/{value.denominator}".encode("ascii")
    ).hexdigest()


def conic_parameters(m: Rational, n: Rational) -> dict[str, Rational]:
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


def energy_values(
    m: Rational,
    n: Rational,
    x_value: Rational,
) -> tuple[Rational, Rational, int, int]:
    old_m = finite.M_PARAMETER
    old_n = finite.N_PARAMETER
    try:
        finite.M_PARAMETER = m
        finite.N_PARAMETER = n
        by_frequency, pole_count = finite.normalized_aggregate()
    finally:
        finite.M_PARAMETER = old_m
        finite.N_PARAMETER = old_n

    total = tree.energy_polynomial(by_frequency)
    target = tree.energy_polynomial(
        by_frequency,
        {tree.NEXT_A_POSITIVE, tree.NEXT_A_NEGATIVE},
    )
    external: tree.Polynomial = {
        powers: total.get(powers, tree.ZERO_R)
        - target.get(powers, tree.ZERO_R)
        for powers in set(total).union(target)
        if total.get(powers, tree.ZERO_R)
        != target.get(powers, tree.ZERO_R)
    }
    target_x = finite.equal_amplitude_in_x(target)
    external_x = finite.equal_amplitude_in_x(external)
    target_value = finite.evaluate(target_x, x_value)
    external_value = finite.evaluate(external_x, x_value)
    if target_value <= 0 or external_value <= 0:
        raise AssertionError("Both energy pieces must be positive.")
    return target_value, external_value, len(by_frequency), pole_count


def point_record(
    m: Rational,
    n: Rational,
    x_value: Rational,
    target_value: Rational,
    external_value: Rational,
    frequency_count: int,
    pole_count: int,
) -> dict[str, object]:
    parameters = conic_parameters(m, n)
    ratio = external_value / target_value
    target_fraction = target_value / (target_value + external_value)
    return {
        "parameters": {
            "m": str(m),
            "n": str(n),
            "pumpChart": str(parameters["pumpChart"]),
            "catalystChart": str(parameters["catalystChart"]),
            "pumpNorm": str(parameters["pumpNorm"]),
            "catalystNorm": str(parameters["catalystNorm"]),
            "x": str(x_value),
        },
        "aggregatedFrequencyCount": frequency_count,
        "uncancelledLaurentPoleCount": pole_count,
        "externalOverTarget": {
            "decimal": float(ratio),
            "exactDigest": rational_digest(ratio),
        },
        "targetFraction": {
            "decimal": float(target_fraction),
            "percent": 100 * float(target_fraction),
            "exactDigest": rational_digest(target_fraction),
        },
        "targetValueDigest": rational_digest(target_value),
        "externalValueDigest": rational_digest(external_value),
    }


def audit() -> dict[str, object]:
    reference_values = energy_values(
        REFERENCE_M,
        REFERENCE_N,
        REFERENCE_X,
    )
    candidate_values = energy_values(
        CANDIDATE_M,
        CANDIDATE_N,
        CANDIDATE_X,
    )
    reference_target, reference_external, _, _ = reference_values
    candidate_target, candidate_external, _, _ = candidate_values
    reference_ratio = reference_external / reference_target
    candidate_ratio = candidate_external / candidate_target
    if not candidate_ratio < reference_ratio:
        raise AssertionError("The decoupled candidate did not improve R0.16.")
    if not candidate_ratio < Rational(158015, 10000):
        raise AssertionError("The candidate missed the rational upper bound.")
    candidate_fraction = candidate_target / (
        candidate_target + candidate_external
    )
    if not candidate_fraction > Rational(59518, 1_000_000):
        raise AssertionError("The target fraction missed its rational bound.")

    return {
        "scope": "decoupled antisymmetric finite fifth-order candidate",
        "referenceR016": point_record(
            REFERENCE_M,
            REFERENCE_N,
            REFERENCE_X,
            *reference_values,
        ),
        "candidateR017": point_record(
            CANDIDATE_M,
            CANDIDATE_N,
            CANDIDATE_X,
            *candidate_values,
        ),
        "strictExternalOverTargetImprovement": {
            "decimal": float(reference_ratio - candidate_ratio),
            "exactDigest": rational_digest(reference_ratio - candidate_ratio),
        },
        "relativeRatioReductionPercent": (
            100 * float((reference_ratio - candidate_ratio) / reference_ratio)
        ),
        "targetFractionIncreasePercentagePoints": (
            100
            * float(
                candidate_fraction
                - reference_target / (reference_target + reference_external)
            )
        ),
        "certifiedRationalUpperBound": "158015/10000",
        "certifiedTargetFractionLowerBound": "59518/1000000",
    }


def validate(result: dict[str, object]) -> None:
    reference = result["referenceR016"]
    candidate = result["candidateR017"]
    assert reference["externalOverTarget"]["exactDigest"] == (
        "e6de533aa93feb1d0e61cae4ac789805e0aa829a820ab79f72d4161bcbc07998"
    )
    assert candidate["parameters"]["m"] == "429/2500"
    assert candidate["parameters"]["n"] == "4271/10000"
    assert candidate["parameters"]["x"] == "26213/10000"
    assert candidate["aggregatedFrequencyCount"] == 332
    assert candidate["uncancelledLaurentPoleCount"] == 0
    assert candidate["externalOverTarget"]["exactDigest"] == (
        "b03c07a99a7b19d3f3198e6099a19fa6a1335b0b8ad1db6f6f3a72f0884d7cd2"
    )
    assert candidate["targetFraction"]["exactDigest"] == (
        "d88148c260ebf6b434ca8081d77110f1580097cebc7bf64c6c6b1ea111644199"
    )
    assert result["strictExternalOverTargetImprovement"]["decimal"] > 2.23
    assert result["relativeRatioReductionPercent"] > 12
    assert result["targetFractionIncreasePercentagePoints"] > 0.69


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
