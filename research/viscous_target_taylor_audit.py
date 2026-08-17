#!/usr/bin/env python3
"""R0.21 exact first viscous correction at the R0.20 global root.

The R0.20 theorem concerns the degree-six, fifth time-Taylor coefficient of
the selected cone relay.  This audit begins the finite-time bridge.  It tags
every coefficient by its signed input-leaf count and retains the heat
operator in the dimensionless time variable

    tau = 4^(2 n) t.

The target frequency needs six input leaves.  Exact frequency arithmetic
shows that it is unreachable with one through five leaves, reachable with
exactly six leaves, and unreachable with seven leaves.  Consequently:

* target Taylor orders zero through four vanish, even with viscosity;
* the order-five target is the R0.20 pure nonlinear coefficient;
* the pure nonlinear order-six target vanishes;
* the full order-six target consists only of one heat insertion into the
  five-interaction trees.

The script computes the order-five through order-seven target vectors as
exact polynomials in the antisymmetric chart variables p and q.  At order
seven it separates two heat insertions from the new eight-leaf pure
nonlinear trees.  Exact rational interval evaluation then encloses both
relative corrections throughout the radius-1e-6 R0.20 root box.

Finite-shell complex128 calculations are included only as a convergence
cross-check.  This audit does not bound the Taylor tail from order eight
onward and does not prove a Navier--Stokes regularity or singularity result.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import platform
import sys
import time
from typing import Iterable

import numpy as np

import antisymmetric_symbolic_quotient_audit as anti
import fifth_order_tree_audit as tree
import polarization_first_variation_audit as first
from polarization_relay import geometry, unit
import two_shell_taylor as shell


Rational = Fraction
Degree = tree.Degree
Poly = anti.Poly
PolyVector = anti.PolyVector
PolyVectorSeries = anti.PolyVectorSeries

MAXIMUM_TIME_ORDER = 7
MAXIMUM_LEAF_COUNT = 8
ROOT_CERTIFICATE = Path("research/certificates/r020/interior-root-certificates.json")
ZERO_POLY_VECTOR = anti.ZERO_POLY_VECTOR


def progress(enabled: bool, started: float, message: str) -> None:
    if enabled:
        print(f"[R0.21 +{time.perf_counter() - started:8.2f}s] {message}", file=sys.stderr, flush=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def compositions(total: int, length: int) -> Iterable[Degree]:
    if length == 1:
        yield (total,)
        return
    for first_value in range(total + 1):
        for rest in compositions(total - first_value, length - 1):
            yield (first_value,) + rest


def target_leaf_degrees(leaf_count: int) -> list[Degree]:
    frequencies = tree.signed_frequencies()
    return [
        degree
        for degree in compositions(leaf_count, len(frequencies))
        if tree.degree_frequency(degree, frequencies) == tree.NEXT_A_POSITIVE
    ]


def target_subdegrees() -> set[Degree]:
    """Return degrees that can be subtrees of an order-five or order-seven target."""

    result: set[Degree] = set()
    for final_degree in target_leaf_degrees(6) + target_leaf_degrees(8):
        for degree in itertools_product_ranges(final_degree):
            if degree_size(degree):
                result.add(degree)
    return result


def itertools_product_ranges(maxima: Degree) -> Iterable[Degree]:
    """Small local replacement for itertools.product over integer ranges."""

    def visit(axis: int, prefix: Degree) -> Iterable[Degree]:
        if axis == len(maxima):
            yield prefix
            return
        for value in range(maxima[axis] + 1):
            yield from visit(axis + 1, prefix + (value,))

    yield from visit(0, ())


def degree_size(degree: Degree) -> int:
    return sum(degree)


def heat_series(
    degree: Degree,
    value: PolyVectorSeries,
    frequencies: tuple[tree.FrequencyExpansion, ...],
    minimum_power: int,
    maximum_power: int,
) -> PolyVectorSeries:
    """Apply -delta^2 |K(delta)|^2 to a polynomial vector series."""

    leading, offset = tree.degree_frequency(degree, frequencies)
    rate = {
        0: tree.dot(leading, leading),
        1: 2 * tree.dot(leading, offset),
        2: tree.dot(offset, offset),
    }
    result: PolyVectorSeries = {}
    for vector_power, coefficient in value.items():
        for rate_power, rate_coefficient in rate.items():
            output_power = vector_power + rate_power
            if not minimum_power <= output_power <= maximum_power:
                continue
            contribution = anti.poly_vector_scale(-rate_coefficient, coefficient)
            updated = anti.poly_vector_add(
                result.get(output_power, ZERO_POLY_VECTOR),
                contribution,
            )
            if updated == ZERO_POLY_VECTOR:
                result.pop(output_power, None)
            else:
                result[output_power] = updated
    return result


def viscous_polynomial_tree(
    show_progress: bool = False,
) -> list[dict[Degree, PolyVectorSeries]]:
    """Compute exact heat-inclusive coefficients through time order six."""

    started = time.perf_counter()
    frequencies = tree.signed_frequencies()
    initial = anti.signed_polynomial_inputs()
    allowed_degrees = target_subdegrees()
    coefficients: list[dict[Degree, PolyVectorSeries]] = [
        {} for _ in range(MAXIMUM_TIME_ORDER + 1)
    ]
    for index, polarization in enumerate(initial):
        degree = tuple(
            int(index == coordinate) for coordinate in range(len(frequencies))
        )
        if degree in allowed_degrees:
            coefficients[0][degree] = polarization

    for order in range(MAXIMUM_TIME_ORDER):
        minimum_power = -(order + 1)
        maximum_power = MAXIMUM_TIME_ORDER - (order + 1)
        output: dict[Degree, PolyVectorSeries] = {}

        for degree, value in coefficients[order].items():
            heated = anti.poly_series_scale(
                Rational(1, order + 1),
                heat_series(
                    degree,
                    value,
                    frequencies,
                    minimum_power,
                    maximum_power,
                ),
            )
            output[degree] = anti.poly_series_add(
                output.get(degree, {}),
                heated,
                minimum_power,
                maximum_power,
            )

        for left_order in range(order + 1):
            right_order = order - left_order
            for left_degree, left in coefficients[left_order].items():
                for right_degree, right in coefficients[right_order].items():
                    degree = tree.degree_add(left_degree, right_degree)
                    if degree not in allowed_degrees:
                        continue
                    interaction = anti.poly_series_scale(
                        Rational(1, order + 1),
                        anti.polynomial_bilinear_series(
                            left_degree,
                            left,
                            right_degree,
                            right,
                            frequencies,
                            minimum_power,
                            maximum_power,
                        ),
                    )
                    output[degree] = anti.poly_series_add(
                        output.get(degree, {}),
                        interaction,
                        minimum_power,
                        maximum_power,
                    )

        coefficients[order + 1] = {
            degree: value for degree, value in output.items() if value
        }
        progress(
            show_progress,
            started,
            f"time order {order + 1}: {len(coefficients[order + 1])} tagged coefficients",
        )
    return coefficients


def target_series(
    coefficients: list[dict[Degree, PolyVectorSeries]],
    order: int,
    leaf_count: int | None = None,
    catalyst_count: int | None = None,
) -> tuple[PolyVectorSeries, list[Degree]]:
    frequencies = tree.signed_frequencies()
    retained: list[Degree] = []
    result: PolyVectorSeries = {}
    for degree, value in coefficients[order].items():
        if leaf_count is not None and degree_size(degree) != leaf_count:
            continue
        if catalyst_count is not None and sum(tree.catalyst_degrees(degree)) != catalyst_count:
            continue
        if tree.degree_frequency(degree, frequencies) != tree.NEXT_A_POSITIVE:
            continue
        retained.append(degree)
        result = anti.poly_series_add(result, value, -order, 0)
    return result, retained


def target_scalar(vector: PolyVector) -> Poly:
    """Project on (2,-1,-1); the common scalar is irrelevant to a ratio."""

    return anti.poly_add(
        anti.poly_scale(2, vector[0]),
        anti.poly_add(anti.poly_scale(-1, vector[1]), anti.poly_scale(-1, vector[2])),
    )


def line_defect_polynomials(vector: PolyVector) -> tuple[Poly, Poly]:
    return (
        anti.poly_add(vector[1], anti.poly_scale(-1, vector[2])),
        anti.poly_add(vector[0], anti.poly_scale(2, vector[1])),
    )


def poly_interval(
    polynomial: Poly,
    p_interval: tuple[Rational, Rational],
    q_interval: tuple[Rational, Rational],
) -> tuple[Rational, Rational]:
    """Natural exact interval evaluation on a positive p-q box."""

    p_lower, p_upper = p_interval
    q_lower, q_upper = q_interval
    lower = Rational(0)
    upper = Rational(0)
    for (p_power, q_power), coefficient in polynomial.items():
        monomial_lower = p_lower**p_power * q_lower**q_power
        monomial_upper = p_upper**p_power * q_upper**q_power
        if coefficient >= 0:
            lower += coefficient * monomial_lower
            upper += coefficient * monomial_upper
        else:
            lower += coefficient * monomial_upper
            upper += coefficient * monomial_lower
    return lower, upper


def interval_divide(
    numerator: tuple[Rational, Rational],
    denominator: tuple[Rational, Rational],
) -> tuple[Rational, Rational]:
    if denominator[0] <= 0 <= denominator[1]:
        raise ZeroDivisionError("The denominator interval contains zero.")
    values = [
        numerator_endpoint / denominator_endpoint
        for numerator_endpoint in numerator
        for denominator_endpoint in denominator
    ]
    return min(values), max(values)


def interval_add(
    left: tuple[Rational, Rational],
    right: tuple[Rational, Rational],
) -> tuple[Rational, Rational]:
    return left[0] + right[0], left[1] + right[1]


def interval_multiply(
    left: tuple[Rational, Rational],
    right: tuple[Rational, Rational],
) -> tuple[Rational, Rational]:
    values = [
        left_endpoint * right_endpoint
        for left_endpoint in left
        for right_endpoint in right
    ]
    return min(values), max(values)


def interval_scale(
    value: Rational,
    interval: tuple[Rational, Rational],
) -> tuple[Rational, Rational]:
    endpoints = value * interval[0], value * interval[1]
    return min(endpoints), max(endpoints)


def polynomial_record(polynomial: Poly) -> dict[str, object]:
    payload = "\n".join(
        f"{powers[0]},{powers[1]}:{coefficient.numerator}/{coefficient.denominator}"
        for powers, coefficient in sorted(polynomial.items())
    )
    return {
        "termCount": len(polynomial),
        "degreeP": max((powers[0] for powers in polynomial), default=-1),
        "degreeQ": max((powers[1] for powers in polynomial), default=-1),
        "sha256": hashlib.sha256(payload.encode("ascii")).hexdigest(),
        "terms": [
            [powers[0], powers[1], str(coefficient)]
            for powers, coefficient in sorted(polynomial.items())
        ],
    }


def evaluate_vector_series(
    series: tree.VectorSeries,
    delta: float,
) -> np.ndarray:
    return np.asarray(
        [
            sum(float(coefficient[axis]) * delta**power for power, coefficient in series.items())
            for axis in range(3)
        ],
        dtype=float,
    )


def optimized_initial_field(
    level: int,
    p_value: float,
    q_value: float,
    x_value: float,
) -> shell.Field:
    delta = 4.0 ** (-level)
    charts = (p_value, -p_value, q_value, -q_value)
    amplitudes = (1.0, 1.0, math.sqrt(x_value) / 2.0, math.sqrt(x_value) / 2.0)
    entries = []
    for frequency, numerator, chart, amplitude in zip(
        tree.POSITIVE_FREQUENCIES,
        tree.POSITIVE_POLARIZATION_SERIES,
        charts,
        amplitudes,
        strict=True,
    ):
        wavevector = np.rint(
            np.asarray(
                [
                    float(frequency[0][axis]) / delta + float(frequency[1][axis])
                    for axis in range(3)
                ]
            )
        ).astype(int)
        tangent = first.tangent_series(frequency, numerator)
        polarization = evaluate_vector_series(numerator, delta) + chart * evaluate_vector_series(
            tangent, delta
        )
        entries.append((wavevector, amplitude * unit(polarization)))
    return shell.real_field(entries)


def numeric_taylor(
    initial: shell.Field,
    level: int,
    include_heat: bool,
) -> list[shell.Field]:
    coefficients = [initial]
    for order in range(MAXIMUM_TIME_ORDER):
        right_hand_side = shell.heat_operator(coefficients[order], level) if include_heat else {}
        for left_order in range(order + 1):
            interaction = shell.bilinear(
                coefficients[left_order], coefficients[order - left_order]
            )
            for wavevector, value in interaction.items():
                shell.add_coefficient(right_hand_side, wavevector, -value)
        coefficients.append(
            shell.clean(
                {
                    wavevector: value / (order + 1)
                    for wavevector, value in right_hand_side.items()
                }
            )
        )
    return coefficients


def finite_shell_cross_checks(
    levels: list[int],
    root: tuple[float, float, float],
) -> list[dict[str, object]]:
    records = []
    for level in levels:
        initial = optimized_initial_field(level, *root)
        full = numeric_taylor(initial, level, include_heat=True)
        inviscid = numeric_taylor(initial, level, include_heat=False)
        target = tuple(int(value) for value in geometry(level + 1)["a"])
        fifth = full[5].get(target, shell.ZERO)
        sixth = full[6].get(target, shell.ZERO)
        seventh = full[7].get(target, shell.ZERO)
        denominator = float(np.vdot(fifth, fifth).real)
        sixth_ratio = complex(np.vdot(fifth, sixth) / denominator)
        seventh_ratio = complex(np.vdot(fifth, seventh) / denominator)
        sixth_line_defect = float(np.linalg.norm(sixth - sixth_ratio * fifth))
        seventh_line_defect = float(np.linalg.norm(seventh - seventh_ratio * fifth))
        records.append(
            {
                "level": level,
                "supportCounts": [len(field) for field in full],
                "targetNormsByTimeOrder": [
                    float(np.linalg.norm(field.get(target, shell.ZERO))) for field in full
                ],
                "orderFiveHeatDifferenceNorm": float(
                    np.linalg.norm(full[5].get(target, shell.ZERO) - inviscid[5].get(target, shell.ZERO))
                ),
                "pureNonlinearOrderSixNorm": float(
                    np.linalg.norm(inviscid[6].get(target, shell.ZERO))
                ),
                "pureNonlinearOrderSevenNorm": float(
                    np.linalg.norm(inviscid[7].get(target, shell.ZERO))
                ),
                "relativeOrderSixOverFive": {
                    "real": sixth_ratio.real,
                    "imaginary": sixth_ratio.imag,
                },
                "relativeOrderSevenOverFive": {
                    "real": seventh_ratio.real,
                    "imaginary": seventh_ratio.imag,
                },
                "orderSixTargetLineDefect": sixth_line_defect,
                "orderSevenTargetLineDefect": seventh_line_defect,
            }
        )
    return records


def load_root_box() -> tuple[dict[str, Rational], Rational, str]:
    payload = json.loads(ROOT_CERTIFICATE.read_text())
    root = payload["roots"][0]
    center = {
        variable: Rational(root["polishedRoot"][variable]) for variable in ("p", "q", "x")
    }
    radius = Rational(root["stationarySystemCertificate"]["radius"])
    return center, radius, sha256(ROOT_CERTIFICATE)


def audit(levels: list[int], show_progress: bool) -> dict[str, object]:
    started = time.perf_counter()
    center, radius, certificate_hash = load_root_box()
    leaf_support = {
        leaf_count: target_leaf_degrees(leaf_count) for leaf_count in range(1, 9)
    }
    progress(show_progress, started, "exact target leaf reachability finished")

    coefficients = viscous_polynomial_tree(show_progress=show_progress)
    fifth_series, fifth_degrees = target_series(coefficients, 5)
    sixth_series, sixth_degrees = target_series(coefficients, 6)
    seventh_heat_series, seventh_heat_degrees = target_series(
        coefficients, 7, leaf_count=6
    )
    seventh_two_catalyst_series, seventh_two_catalyst_degrees = target_series(
        coefficients, 7, leaf_count=8, catalyst_count=2
    )
    seventh_four_catalyst_series, seventh_four_catalyst_degrees = target_series(
        coefficients, 7, leaf_count=8, catalyst_count=4
    )
    fifth_vector = fifth_series.get(0, ZERO_POLY_VECTOR)
    sixth_vector = sixth_series.get(0, ZERO_POLY_VECTOR)
    seventh_heat_vector = seventh_heat_series.get(0, ZERO_POLY_VECTOR)
    seventh_two_catalyst_vector = seventh_two_catalyst_series.get(0, ZERO_POLY_VECTOR)
    seventh_four_catalyst_vector = seventh_four_catalyst_series.get(0, ZERO_POLY_VECTOR)
    fifth_poles = sum(
        sum(len(component) for component in fifth_series.get(power, ZERO_POLY_VECTOR))
        for power in range(-5, 0)
    )
    sixth_poles = sum(
        sum(len(component) for component in sixth_series.get(power, ZERO_POLY_VECTOR))
        for power in range(-6, 0)
    )
    seventh_series_parts = (
        seventh_heat_series,
        seventh_two_catalyst_series,
        seventh_four_catalyst_series,
    )
    seventh_poles = [
        sum(
            sum(len(component) for component in series.get(power, ZERO_POLY_VECTOR))
            for power in range(-7, 0)
        )
        for series in seventh_series_parts
    ]
    fifth_defects = line_defect_polynomials(fifth_vector)
    sixth_defects = line_defect_polynomials(sixth_vector)
    seventh_defects = [
        line_defect_polynomials(vector)
        for vector in (
            seventh_heat_vector,
            seventh_two_catalyst_vector,
            seventh_four_catalyst_vector,
        )
    ]
    fifth_scalar = target_scalar(fifth_vector)
    sixth_scalar = target_scalar(sixth_vector)
    seventh_heat_scalar = target_scalar(seventh_heat_vector)
    seventh_two_catalyst_scalar = target_scalar(seventh_two_catalyst_vector)
    seventh_four_catalyst_scalar = target_scalar(seventh_four_catalyst_vector)

    p_interval = center["p"] - radius, center["p"] + radius
    q_interval = center["q"] - radius, center["q"] + radius
    fifth_interval = poly_interval(fifth_scalar, p_interval, q_interval)
    sixth_interval = poly_interval(sixth_scalar, p_interval, q_interval)
    ratio_interval = interval_divide(sixth_interval, fifth_interval)
    seventh_heat_interval = poly_interval(seventh_heat_scalar, p_interval, q_interval)
    seventh_two_catalyst_interval = poly_interval(
        seventh_two_catalyst_scalar, p_interval, q_interval
    )
    seventh_four_catalyst_interval = poly_interval(
        seventh_four_catalyst_scalar, p_interval, q_interval
    )
    u_interval = (
        1 + p_interval[0] ** 2 / 12,
        1 + p_interval[1] ** 2 / 12,
    )
    v_interval = (
        1 + q_interval[0] ** 2 / 3,
        1 + q_interval[1] ** 2 / 3,
    )
    x_interval = center["x"] - radius, center["x"] + radius
    seventh_heat_ratio = interval_divide(seventh_heat_interval, fifth_interval)
    seventh_two_catalyst_ratio = interval_scale(
        Rational(-1, 6),
        interval_divide(
            interval_divide(seventh_two_catalyst_interval, fifth_interval),
            u_interval,
        ),
    )
    seventh_four_catalyst_ratio = interval_scale(
        Rational(-1, 6),
        interval_multiply(
            interval_divide(
                interval_divide(seventh_four_catalyst_interval, fifth_interval),
                v_interval,
            ),
            interval_scale(Rational(1, 4), x_interval),
        ),
    )
    seventh_ratio_interval = interval_add(
        interval_add(seventh_heat_ratio, seventh_two_catalyst_ratio),
        seventh_four_catalyst_ratio,
    )
    progress(show_progress, started, "exact root-box interval evaluation finished")

    cross_checks = finite_shell_cross_checks(
        levels,
        (float(center["p"]), float(center["q"]), float(center["x"])),
    )
    progress(show_progress, started, "finite-shell cross-checks finished")

    return {
        "schemaVersion": 1,
        "scope": "first viscous target correction at the R0.20 global root",
        "proofStatus": (
            "exact support and polynomial certificate through time order seven; "
            "Taylor tail from order eight onward remains open"
        ),
        "configuration": {
            "dimensionlessTime": "tau=4^(2n)t",
            "viscosity": 1,
            "maximumTimeOrder": MAXIMUM_TIME_ORDER,
            "maximumRetainedLeafCount": MAXIMUM_LEAF_COUNT,
            "rootCertificate": str(ROOT_CERTIFICATE),
            "rootCertificateSha256": certificate_hash,
            "rootBoxRadius": str(radius),
            "finiteShellLevels": levels,
        },
        "exactLeafReachability": {
            str(leaf_count): {
                "targetDegreeCount": len(degrees),
                "degrees": [list(degree) for degree in degrees],
            }
            for leaf_count, degrees in leaf_support.items()
        },
        "exactConsequences": {
            "targetAbsentThroughTimeOrderFour": all(
                not leaf_support[leaf_count] for leaf_count in range(1, 6)
            ),
            "sixLeafTargetDegreeCount": len(leaf_support[6]),
            "pureNonlinearOrderSixAbsent": not leaf_support[7],
            "firstPossiblePostLeadingPureNonlinearOrder": 7 if leaf_support[8] else None,
        },
        "targetPolynomials": {
            "orderFive": {
                "retainedTaggedDegrees": [list(degree) for degree in fifth_degrees],
                "uncancelledNegativeLaurentTerms": fifth_poles,
                "targetLineDefectsAreZeroPolynomials": not any(fifth_defects),
                "scalar": polynomial_record(fifth_scalar),
            },
            "orderSixOneHeatInsertion": {
                "retainedTaggedDegrees": [list(degree) for degree in sixth_degrees],
                "uncancelledNegativeLaurentTerms": sixth_poles,
                "targetLineDefectsAreZeroPolynomials": not any(sixth_defects),
                "scalar": polynomial_record(sixth_scalar),
            },
            "orderSevenTwoHeatInsertions": {
                "retainedTaggedDegrees": [list(degree) for degree in seventh_heat_degrees],
                "uncancelledNegativeLaurentTerms": seventh_poles[0],
                "targetLineDefectsAreZeroPolynomials": not any(seventh_defects[0]),
                "scalar": polynomial_record(seventh_heat_scalar),
            },
            "orderSevenPureNonlinearTwoCatalystLeaves": {
                "retainedTaggedDegrees": [
                    list(degree) for degree in seventh_two_catalyst_degrees
                ],
                "uncancelledNegativeLaurentTerms": seventh_poles[1],
                "targetLineDefectsAreZeroPolynomials": not any(seventh_defects[1]),
                "scalar": polynomial_record(seventh_two_catalyst_scalar),
            },
            "orderSevenPureNonlinearFourCatalystLeaves": {
                "retainedTaggedDegrees": [
                    list(degree) for degree in seventh_four_catalyst_degrees
                ],
                "uncancelledNegativeLaurentTerms": seventh_poles[2],
                "targetLineDefectsAreZeroPolynomials": not any(seventh_defects[2]),
                "scalar": polynomial_record(seventh_four_catalyst_scalar),
            },
        },
        "rootBoxCertificate": {
            "center": {variable: str(value) for variable, value in center.items()},
            "orderFiveScalarInterval": [str(fifth_interval[0]), str(fifth_interval[1])],
            "orderSixScalarInterval": [str(sixth_interval[0]), str(sixth_interval[1])],
            "relativeOrderSixOverFiveInterval": [
                str(ratio_interval[0]),
                str(ratio_interval[1]),
            ],
            "relativeOrderSixOverFiveDecimal": [
                float(ratio_interval[0]),
                float(ratio_interval[1]),
            ],
            "strictlyOpposesOrderFive": ratio_interval[1] < 0,
            "relativeOrderSevenOverFiveComponentsDecimal": {
                "twoHeatInsertions": [
                    float(seventh_heat_ratio[0]),
                    float(seventh_heat_ratio[1]),
                ],
                "pureNonlinearTwoCatalystLeaves": [
                    float(seventh_two_catalyst_ratio[0]),
                    float(seventh_two_catalyst_ratio[1]),
                ],
                "pureNonlinearFourCatalystLeaves": [
                    float(seventh_four_catalyst_ratio[0]),
                    float(seventh_four_catalyst_ratio[1]),
                ],
            },
            "relativeOrderSevenOverFiveInterval": [
                str(seventh_ratio_interval[0]),
                str(seventh_ratio_interval[1]),
            ],
            "relativeOrderSevenOverFiveDecimal": [
                float(seventh_ratio_interval[0]),
                float(seventh_ratio_interval[1]),
            ],
        },
        "finiteShellCrossChecks": cross_checks,
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "platform": platform.platform(),
        },
        "wallSeconds": time.perf_counter() - started,
    }


def validate(result: dict[str, object]) -> None:
    exact = result["exactConsequences"]
    assert exact["targetAbsentThroughTimeOrderFour"] is True
    assert exact["sixLeafTargetDegreeCount"] == 3
    assert exact["pureNonlinearOrderSixAbsent"] is True
    assert exact["firstPossiblePostLeadingPureNonlinearOrder"] == 7
    fifth = result["targetPolynomials"]["orderFive"]
    sixth = result["targetPolynomials"]["orderSixOneHeatInsertion"]
    seventh_parts = [
        result["targetPolynomials"]["orderSevenTwoHeatInsertions"],
        result["targetPolynomials"]["orderSevenPureNonlinearTwoCatalystLeaves"],
        result["targetPolynomials"]["orderSevenPureNonlinearFourCatalystLeaves"],
    ]
    assert fifth["uncancelledNegativeLaurentTerms"] == 0
    assert sixth["uncancelledNegativeLaurentTerms"] == 0
    assert fifth["targetLineDefectsAreZeroPolynomials"] is True
    assert sixth["targetLineDefectsAreZeroPolynomials"] is True
    for part in seventh_parts:
        assert part["uncancelledNegativeLaurentTerms"] == 0
        assert part["targetLineDefectsAreZeroPolynomials"] is True
    certificate = result["rootBoxCertificate"]
    assert certificate["strictlyOpposesOrderFive"] is True
    lower, upper = certificate["relativeOrderSixOverFiveDecimal"]
    assert -2.62 < lower < upper < -2.60
    seventh_lower, seventh_upper = certificate["relativeOrderSevenOverFiveDecimal"]
    assert -2.83 < seventh_lower < seventh_upper < -2.79
    for record in result["finiteShellCrossChecks"]:
        assert record["targetNormsByTimeOrder"][:5] == [0.0] * 5
        assert record["orderFiveHeatDifferenceNorm"] == 0.0
        assert record["pureNonlinearOrderSixNorm"] == 0.0
        assert abs(record["relativeOrderSixOverFive"]["imaginary"]) < 1.0e-12
        assert record["relativeOrderSixOverFive"]["real"] < 0
        assert record["orderSixTargetLineDefect"] < 1.0e-9
        assert record["pureNonlinearOrderSevenNorm"] > 0
        assert abs(record["relativeOrderSevenOverFive"]["imaginary"]) < 1.0e-12
        assert record["relativeOrderSevenOverFive"]["real"] < 0
        assert record["orderSevenTargetLineDefect"] < 1.0e-8
    final_ratio = result["finiteShellCrossChecks"][-1]["relativeOrderSevenOverFive"]["real"]
    assert seventh_lower < final_ratio < seventh_upper


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--levels", type=int, nargs="+", default=[2, 3, 4, 5, 6])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    result = audit(arguments.levels, arguments.progress)
    if arguments.check:
        validate(result)
    text = json.dumps(
        result,
        ensure_ascii=False,
        indent=2 if arguments.pretty else None,
        sort_keys=True,
    )
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
