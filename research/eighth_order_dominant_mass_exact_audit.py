#!/usr/bin/env python3
"""R0.68B-2e exact dominant-mass interval audit.

The reachable vector sequence for the eighth-order cycle obeys an exact
degree-33 recurrence after one transient.  For every one of the 1,792 state
coordinates, this script forms the exact generating numerator and evaluates
its dominant-pole residue over a refined rational bracket of the positive
quartic root.

All certification arithmetic uses fractions.  Binary64 is used only for
display and for a non-certifying comparison with the earlier power iteration.
The result certifies the dominant mass vector, not its degree-ten moment lift.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import sys
import time
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

import numpy as np

import eighth_order_cycle_audit as cycle
import eighth_order_heat_jet_pilot as pilot


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    if not enabled:
        return
    fields = " ".join(f"{key}={value}" for key, value in details.items())
    print(
        f"[R0.68B-2e exact mass +{time.perf_counter() - started:8.2f}s] "
        f"{stage}{(' ' + fields) if fields else ''}",
        file=sys.stderr,
        flush=True,
    )


def decimal(value: Fraction, digits: int = 50) -> str:
    with localcontext() as context:
        context.prec = digits
        return format(Decimal(value.numerator) / Decimal(value.denominator), ".42e")


def fraction_record(value: Fraction) -> dict[str, str]:
    canonical = f"{value.numerator}/{value.denominator}"
    return {
        "numerator": str(value.numerator),
        "denominator": str(value.denominator),
        "decimal": decimal(value),
        "sha256": hashlib.sha256(canonical.encode("ascii")).hexdigest(),
    }


def interval_multiply(
    left: tuple[Fraction, Fraction], right: tuple[Fraction, Fraction]
) -> tuple[Fraction, Fraction]:
    values = tuple(
        left[left_index] * right[right_index]
        for left_index in (0, 1)
        for right_index in (0, 1)
    )
    return min(values), max(values)


def interval_horner(
    coefficients: list[int], argument: tuple[Fraction, Fraction]
) -> tuple[Fraction, Fraction]:
    result = (Fraction(coefficients[0]), Fraction(coefficients[0]))
    for coefficient in coefficients[1:]:
        product = interval_multiply(result, argument)
        result = product[0] + coefficient, product[1] + coefficient
    return result


def interval_negative_ratio(
    numerator: tuple[Fraction, Fraction],
    denominator: tuple[Fraction, Fraction],
) -> tuple[Fraction, Fraction]:
    if not denominator[1] < 0:
        raise AssertionError("dominant residue denominator must stay negative")
    values = tuple(
        -numerator[numerator_index] / denominator[denominator_index]
        for numerator_index in (0, 1)
        for denominator_index in (0, 1)
    )
    return min(values), max(values)


def refined_root_interval(
    bisections: int,
) -> tuple[tuple[Fraction, Fraction], tuple[int | Fraction, int | Fraction]]:
    lower, upper = cycle.DOMINANT_ROOT_INTERVAL
    lower_value = cycle.evaluate_polynomial(cycle.SCALED_QUARTIC, lower)
    upper_value = cycle.evaluate_polynomial(cycle.SCALED_QUARTIC, upper)
    if not lower_value < 0 < upper_value:
        raise AssertionError("upstream dominant-root bracket has invalid signs")
    for _ in range(bisections):
        midpoint = (lower + upper) / 2
        value = cycle.evaluate_polynomial(cycle.SCALED_QUARTIC, midpoint)
        if value < 0:
            lower, lower_value = midpoint, value
        elif value > 0:
            upper, upper_value = midpoint, value
        else:
            raise AssertionError("unexpected rational root")
    return (lower, upper), (lower_value, upper_value)


def exact_reachable_vectors(
    recurrence_degree: int,
) -> list[list[int]]:
    transfers = [
        cycle.signed_digit_transfer(0),
        cycle.signed_digit_transfer(1),
    ]
    rows = [cycle.exact_transfer_rows(transfer) for transfer in transfers]
    vectors = [
        [int(value) for value in cycle.initial_vector(dtype=object)]
    ]
    for _ in range(recurrence_degree + 1):
        vectors.append(cycle.apply_exact_cycle(rows, vectors[-1]))
    return vectors


def dominant_mass_intervals(
    root_interval: tuple[Fraction, Fraction],
    report_progress: bool = False,
    started: float = 0.0,
) -> tuple[list[Fraction], list[Fraction], dict[str, object]]:
    recurrence = cycle.reachable_polynomial()
    degree = len(recurrence) - 1
    vectors = exact_reachable_vectors(degree)
    vector_residual = [
        vectors[degree + 1][state]
        + sum(
            recurrence[index] * vectors[degree + 1 - index][state]
            for index in range(1, degree + 1)
        )
        for state in range(cycle.DIMENSION)
    ]
    if any(vector_residual):
        raise AssertionError("reachable vector recurrence failed")
    progress(
        report_progress,
        started,
        "exact recurrence verified",
        degree=degree,
        states=cycle.DIMENSION,
    )

    numerators = [
        [
            sum(
                recurrence[index] * vectors[power - index][state]
                for index in range(power + 1)
            )
            for state in range(cycle.DIMENSION)
        ]
        for power in range(degree + 1)
    ]
    denominator = interval_horner(
        [
            index * recurrence[index]
            for index in range(1, len(recurrence))
        ],
        root_interval,
    )
    if not denominator[1] < 0:
        raise AssertionError("reachable denominator derivative crosses zero")

    lowers: list[Fraction] = []
    uppers: list[Fraction] = []
    maximum_width = Fraction(0)
    maximum_width_state = -1
    for state in range(cycle.DIMENSION):
        numerator = interval_horner(
            [numerators[power][state] for power in range(degree + 1)],
            root_interval,
        )
        lower, upper = interval_negative_ratio(numerator, denominator)
        lowers.append(lower)
        uppers.append(upper)
        if upper - lower > maximum_width:
            maximum_width = upper - lower
            maximum_width_state = state
    canonical = "\n".join(
        f"{state}:{lowers[state].numerator}/{lowers[state].denominator}:"
        f"{uppers[state].numerator}/{uppers[state].denominator}"
        for state in range(cycle.DIMENSION)
    )
    return lowers, uppers, {
        "recurrenceDegree": degree,
        "vectorRecurrenceResidualIsZero": True,
        "residueDenominatorLower": fraction_record(denominator[0]),
        "residueDenominatorUpper": fraction_record(denominator[1]),
        "maximumCoordinateWidth": fraction_record(maximum_width),
        "maximumCoordinateWidthState": maximum_width_state,
        "canonicalIntervalVectorSha256": hashlib.sha256(
            canonical.encode("ascii")
        ).hexdigest(),
        "canonicalIntervalVectorFormat": (
            "state:lowerNumerator/lowerDenominator:"
            "upperNumerator/upperDenominator, newline separated"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--source-commit", default="uncommitted")
    parser.add_argument("--bisections", type=int, default=192)
    parser.add_argument("--progress", action="store_true")
    arguments = parser.parse_args()
    if arguments.bisections < 64:
        parser.error("--bisections must be at least 64")
    started = time.perf_counter()

    root_interval, root_values = refined_root_interval(arguments.bisections)
    progress(
        arguments.progress,
        started,
        "root refined",
        bisections=arguments.bisections,
        width=decimal(root_interval[1] - root_interval[0]),
    )
    lowers, uppers, mass_metadata = dominant_mass_intervals(
        root_interval, arguments.progress, started
    )
    observable = pilot.OBSERVABLE_STATE
    midpoints = np.array(
        [float((lower + upper) / 2) for lower, upper in zip(lowers, uppers)]
    )
    root_midpoint = float(sum(root_interval, Fraction(0)) / 2)
    transfers = [
        cycle.signed_digit_transfer(0),
        cycle.signed_digit_transfer(1),
    ]
    float_cycle = cycle.cycle_matrix(transfers).astype(float)
    float_residual = float(
        np.max(np.abs(float_cycle @ midpoints - root_midpoint * midpoints))
    )
    power, power_metadata = pilot.reachable_dominant_mass(
        float_cycle, root_midpoint
    )
    power_difference = float(np.max(np.abs(power - midpoints)))

    checks = {
        "refinedQuarticRootHasExactSignBracket": root_values[0] < 0 < root_values[1],
        "rootBracketIsNarrowerThanOneEminusSixty": (
            root_interval[1] - root_interval[0] < Fraction(1, 10**60)
        ),
        "reachableVectorRecurrenceIsExact": mass_metadata[
            "vectorRecurrenceResidualIsZero"
        ],
        "allStateIntervalsAreOrdered": all(
            lower <= upper for lower, upper in zip(lowers, uppers)
        ),
        "all1792StateIntervalsArePresent": len(lowers) == cycle.DIMENSION,
        "massIntervalsAreNarrowerThanOneEminusFifty": max(
            upper - lower for lower, upper in zip(lowers, uppers)
        )
        < Fraction(1, 10**50),
        "observableMassIsStrictlyNegative": uppers[observable] < 0,
        "binary64MidpointEigenResidualIsSmall": float_residual < 1.0e-11,
        "powerIterationCrossCheckIsClose": power_difference < 5.0e-14,
    }
    if not all(checks.values()):
        raise AssertionError(f"exact mass checks failed: {checks}")

    report = {
        "schemaVersion": "1.0",
        "status": "strict-passed",
        "classification": (
            "exact rational interval certificate for all 1,792 coordinates "
            "of the reachable dominant eighth-order mass vector"
        ),
        "checks": {key: bool(value) for key, value in checks.items()},
        "parameters": {
            "states": cycle.DIMENSION,
            "rootBisections": arguments.bisections,
            "upstreamRootBracket": [
                str(cycle.DOMINANT_ROOT_INTERVAL[0]),
                str(cycle.DOMINANT_ROOT_INTERVAL[1]),
            ],
        },
        "dominantRoot": {
            "lower": fraction_record(root_interval[0]),
            "upper": fraction_record(root_interval[1]),
            "width": fraction_record(root_interval[1] - root_interval[0]),
            "quarticAtLower": fraction_record(Fraction(root_values[0])),
            "quarticAtUpper": fraction_record(Fraction(root_values[1])),
        },
        "dominantMass": {
            **mass_metadata,
            "observableState": observable,
            "observableLower": fraction_record(lowers[observable]),
            "observableUpper": fraction_record(uppers[observable]),
            "binary64MidpointEigenResidualMaximum": float_residual,
            "powerIterationMaximumDifference": power_difference,
            "powerIterationResidualMaximum": power_metadata[
                "maximumEigenResidual"
            ],
        },
        "provenance": {
            "sourceCommit": arguments.source_commit,
            "arithmetic": "fractions.Fraction exact rational arithmetic",
        },
        "runtime": {
            "elapsedSeconds": time.perf_counter() - started,
            "python": platform.python_version(),
            "numpy": np.__version__,
        },
        "limitations": [
            "This certificate isolates the dominant mass vector only.",
            "The degree-ten moment lift, heat jet, and defect still require enclosures.",
            "No statement is made about general three-dimensional Navier-Stokes regularity.",
        ],
    }
    serialized = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(serialized)
    sys.stdout.write(serialized)
    progress(
        arguments.progress,
        started,
        "complete",
        width=mass_metadata["maximumCoordinateWidth"]["decimal"],
        observable=f"[{decimal(lowers[observable])},{decimal(uppers[observable])}]",
    )


if __name__ == "__main__":
    main()
