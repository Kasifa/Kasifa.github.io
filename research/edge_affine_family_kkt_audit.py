#!/usr/bin/env python3
"""R0.52 exact global-bound audit for the full affine charge-weight family.

For the exact degree-80 center, consider

    omega_s(c, lambda) = c^s (1 + lambda |s|),
    c > 0, lambda >= 0.

The R0.51 fixed rational weight lies close to a point where the true
(j,s)=(81,162) column and the zero-charge column are both active.  Introduce

    alpha = lambda / (1 + 162 lambda),
    delta = 1 - 162 alpha.

Then 0 <= alpha < 1/162, lambda=alpha/delta, and the active column is linear
in alpha.  With active Laurent moments M_k and zero-sector Laurent moments
U_0,U_1,T_0,T_1, the exact stationary system is

    F = c [M_0 + alpha M_1 - 1] = 0,
    G = c [delta (U_0 - 1) + alpha U_1] = 0,
    H = c^2 [(M_1 + alpha M_2) U_1
             - delta^2 M_1 T_0 - alpha delta M_1 T_1] = 0.

The positive factors c, c^2 and delta only clear Laurent/rational
denominators.  The third equation is the coordinate-invariant determinant

    (d_t B_162)(d_alpha Z_0) - (d_alpha B_162)(d_t Z_0) = 0,
    t=log(c),

multiplied by c^2 delta^2.

This script constructs the three equations from GMP rationals and certifies
one and only one zero in a pinned rational box using an exact Krawczyk
inclusion.  It proves strict constrained local maximality and covers every
inactive finite-charge, all-degree, and infinite large-charge sector on the
box.

For a global upper bound, alpha is eliminated from the active and zero-sector
inequalities.  At the rational upper radius the resulting Laurent feasibility
function has a log-c derivative with exactly three positive roots by
Descartes' rule and three exact sign-changing boxes.  Exact endpoint and
Bernstein signs then exclude the complete c>0, lambda>=0 parameter domain.
Together with the certified local root, this gives a width-10^-40 global
enclosure for the optimum of the degree-80 affine family.  It does not turn
that enclosure into an exact uniqueness theorem, construct a critical-space
bridge for arbitrary three-dimensional fields, or prove or disprove
three-dimensional Navier--Stokes regularity.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import time
from typing import Callable

import gmpy2
import mpmath as mp

import edge_affine_charge_weight_audit as r051
import edge_charge_character_optimization_audit as r050
import edge_charge_degree_lattice_audit as r047
import edge_charge_resolved_audit as r039
import edge_charge_threshold_root_audit as r048
import edge_rational_asymptotic_audit as r028
import edge_short_continuation_audit as r036
import edge_weighted_restart_audit as r037


Rational = gmpy2.mpq
Interval = tuple[Rational, Rational]
Vector = list[Rational]
Matrix = list[list[Rational]]
IntervalMatrix = list[list[Interval]]

ACTIVE_CHARGE = 162
R051_CERTIFICATE = Path("research/certificates/r051/edge-affine-charge-weight.json")
R051_EXPECTED_SHA256 = (
    "db72d40ee304d1a6ce5dd96d9f5971e78037675e79c837e409c5691bb8aa582f"
)
R051_POLYNOMIAL_SHA256 = (
    "056a0adba7f3cba41a6e9bd6d943a8f59be28f50f44c6035df1f68393ed26be7"
)
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(
            f"[R0.52 +{elapsed:8.2f}s] {stage}{suffix}",
            file=sys.stderr,
            flush=True,
        )
    if PROGRESS_LOG is not None:
        record = {
            "timestampUtc": datetime.now(timezone.utc).isoformat(),
            "elapsedSeconds": elapsed,
            "stage": stage,
            **details,
        }
        with PROGRESS_LOG.open("a", encoding="utf-8") as target:
            target.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
            target.flush()
            os.fsync(target.fileno())


def rational(value: str | int | Rational) -> Rational:
    return Rational(value)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact_rational_record(value: Rational) -> dict[str, object]:
    """Record huge proof intermediates without duplicating multi-megabyte integers."""

    numerator = gmpy2.numer(value)
    denominator = gmpy2.denom(value)
    return {
        "decimal": r037.rational_decimal(value),
        "numeratorDigits": len(str(abs(numerator))),
        "denominatorDigits": len(str(denominator)),
        "sha256": r037.rational_digest(value),
    }


def point(value: Rational) -> Interval:
    return value, value


def interval_add(left: Interval, right: Interval) -> Interval:
    return left[0] + right[0], left[1] + right[1]


def interval_negate(value: Interval) -> Interval:
    return -value[1], -value[0]


def interval_subtract(left: Interval, right: Interval) -> Interval:
    return interval_add(left, interval_negate(right))


def interval_multiply(left: Interval, right: Interval) -> Interval:
    products = (
        left[0] * right[0],
        left[0] * right[1],
        left[1] * right[0],
        left[1] * right[1],
    )
    return min(products), max(products)


def interval_divide(left: Interval, right: Interval) -> Interval:
    if right[0] <= 0 <= right[1]:
        raise ZeroDivisionError("interval denominator contains zero")
    reciprocal = (Rational(1, right[1]), Rational(1, right[0]))
    return interval_multiply(left, reciprocal)


def interval_scale(value: Interval, factor: Rational) -> Interval:
    return interval_multiply(value, point(factor))


def interval_power(value: Interval, exponent: int) -> Interval:
    if value[0] <= 0:
        raise ValueError("Laurent interval powers require a positive interval")
    if exponent >= 0:
        return value[0] ** exponent, value[1] ** exponent
    return value[1] ** exponent, value[0] ** exponent


def interval_abs_upper(value: Interval) -> Rational:
    return max(abs(value[0]), abs(value[1]))


@dataclass(frozen=True)
class PointJet:
    value: Rational
    gradient: tuple[Rational, Rational, Rational]
    hessian: tuple[
        tuple[Rational, Rational, Rational],
        tuple[Rational, Rational, Rational],
        tuple[Rational, Rational, Rational],
    ]

    @staticmethod
    def constant(value: Rational) -> "PointJet":
        zero = Rational(0)
        return PointJet(
            value,
            (zero, zero, zero),
            ((zero, zero, zero), (zero, zero, zero), (zero, zero, zero)),
        )

    @staticmethod
    def variable(value: Rational, index: int) -> "PointJet":
        gradient = [Rational(0), Rational(0), Rational(0)]
        gradient[index] = Rational(1)
        zero = Rational(0)
        return PointJet(
            value,
            tuple(gradient),
            ((zero, zero, zero), (zero, zero, zero), (zero, zero, zero)),
        )

    def __add__(self, other: "PointJet") -> "PointJet":
        return PointJet(
            self.value + other.value,
            tuple(a + b for a, b in zip(self.gradient, other.gradient, strict=True)),
            tuple(
                tuple(
                    self.hessian[row][column] + other.hessian[row][column]
                    for column in range(3)
                )
                for row in range(3)
            ),
        )

    def __neg__(self) -> "PointJet":
        return PointJet(
            -self.value,
            tuple(-item for item in self.gradient),
            tuple(
                tuple(-self.hessian[row][column] for column in range(3))
                for row in range(3)
            ),
        )

    def __sub__(self, other: "PointJet") -> "PointJet":
        return self + (-other)

    def __mul__(self, other: "PointJet") -> "PointJet":
        return PointJet(
            self.value * other.value,
            tuple(
                left * other.value + self.value * right
                for left, right in zip(self.gradient, other.gradient, strict=True)
            ),
            tuple(
                tuple(
                    self.hessian[row][column] * other.value
                    + self.gradient[row] * other.gradient[column]
                    + self.gradient[column] * other.gradient[row]
                    + self.value * other.hessian[row][column]
                    for column in range(3)
                )
                for row in range(3)
            ),
        )

    def scale(self, factor: Rational) -> "PointJet":
        return PointJet(
            factor * self.value,
            tuple(factor * item for item in self.gradient),
            tuple(
                tuple(factor * self.hessian[row][column] for column in range(3))
                for row in range(3)
            ),
        )


@dataclass(frozen=True)
class IntervalJet:
    value: Interval
    gradient: tuple[Interval, Interval, Interval]
    hessian: tuple[
        tuple[Interval, Interval, Interval],
        tuple[Interval, Interval, Interval],
        tuple[Interval, Interval, Interval],
    ]

    @staticmethod
    def constant(value: Interval) -> "IntervalJet":
        zero = point(Rational(0))
        return IntervalJet(
            value,
            (zero, zero, zero),
            ((zero, zero, zero), (zero, zero, zero), (zero, zero, zero)),
        )

    @staticmethod
    def variable(value: Interval, index: int) -> "IntervalJet":
        zero = point(Rational(0))
        gradient = [zero, zero, zero]
        gradient[index] = point(Rational(1))
        return IntervalJet(
            value,
            tuple(gradient),
            ((zero, zero, zero), (zero, zero, zero), (zero, zero, zero)),
        )

    def __add__(self, other: "IntervalJet") -> "IntervalJet":
        return IntervalJet(
            interval_add(self.value, other.value),
            tuple(
                interval_add(left, right)
                for left, right in zip(self.gradient, other.gradient, strict=True)
            ),
            tuple(
                tuple(
                    interval_add(
                        self.hessian[row][column],
                        other.hessian[row][column],
                    )
                    for column in range(3)
                )
                for row in range(3)
            ),
        )

    def __neg__(self) -> "IntervalJet":
        return IntervalJet(
            interval_negate(self.value),
            tuple(interval_negate(item) for item in self.gradient),
            tuple(
                tuple(
                    interval_negate(self.hessian[row][column])
                    for column in range(3)
                )
                for row in range(3)
            ),
        )

    def __sub__(self, other: "IntervalJet") -> "IntervalJet":
        return self + (-other)

    def __mul__(self, other: "IntervalJet") -> "IntervalJet":
        return IntervalJet(
            interval_multiply(self.value, other.value),
            tuple(
                interval_add(
                    interval_multiply(left, other.value),
                    interval_multiply(self.value, right),
                )
                for left, right in zip(self.gradient, other.gradient, strict=True)
            ),
            tuple(
                tuple(
                    interval_add(
                        interval_add(
                            interval_multiply(
                                self.hessian[row][column], other.value
                            ),
                            interval_multiply(
                                self.gradient[row], other.gradient[column]
                            ),
                        ),
                        interval_add(
                            interval_multiply(
                                self.gradient[column], other.gradient[row]
                            ),
                            interval_multiply(
                                self.value, other.hessian[row][column]
                            ),
                        ),
                    )
                    for column in range(3)
                )
                for row in range(3)
            ),
        )

    def scale(self, factor: Rational) -> "IntervalJet":
        return IntervalJet(
            interval_scale(self.value, factor),
            tuple(interval_scale(item, factor) for item in self.gradient),
            tuple(
                tuple(
                    interval_scale(self.hessian[row][column], factor)
                    for column in range(3)
                )
                for row in range(3)
            ),
        )


def point_moment(
    terms: list[tuple[int, int, Rational]],
    radius: Rational,
    character: Rational,
    charge_power: int,
) -> PointJet:
    value = Rational(0)
    derivative_r = Rational(0)
    derivative_c = Rational(0)
    derivative_rr = Rational(0)
    derivative_rc = Rational(0)
    derivative_cc = Rational(0)
    for degree, charge, coefficient in terms:
        weighted = coefficient * charge**charge_power
        monomial = weighted * radius**degree * character**charge
        value += monomial
        derivative_r += degree * weighted * radius ** (degree - 1) * character**charge
        derivative_c += charge * weighted * radius**degree * character ** (charge - 1)
        derivative_rr += (
            degree
            * (degree - 1)
            * weighted
            * radius ** (degree - 2)
            * character**charge
        )
        derivative_rc += (
            degree
            * charge
            * weighted
            * radius ** (degree - 1)
            * character ** (charge - 1)
        )
        derivative_cc += (
            charge
            * (charge - 1)
            * weighted
            * radius**degree
            * character ** (charge - 2)
        )
    zero = Rational(0)
    return PointJet(
        value,
        (derivative_r, derivative_c, zero),
        (
            (derivative_rr, derivative_rc, zero),
            (derivative_rc, derivative_cc, zero),
            (zero, zero, zero),
        ),
    )


def interval_moment(
    terms: list[tuple[int, int, Rational]],
    radius: Interval,
    character: Interval,
    charge_power: int,
) -> IntervalJet:
    zero = point(Rational(0))
    value = zero
    derivative_r = zero
    derivative_c = zero
    derivative_rr = zero
    derivative_rc = zero
    derivative_cc = zero
    for degree, charge, coefficient in terms:
        weighted = coefficient * charge**charge_power
        value = interval_add(
            value,
            interval_scale(
                interval_multiply(
                    interval_power(radius, degree),
                    interval_power(character, charge),
                ),
                weighted,
            ),
        )
        derivative_r = interval_add(
            derivative_r,
            interval_scale(
                interval_multiply(
                    interval_power(radius, degree - 1),
                    interval_power(character, charge),
                ),
                degree * weighted,
            ),
        )
        derivative_c = interval_add(
            derivative_c,
            interval_scale(
                interval_multiply(
                    interval_power(radius, degree),
                    interval_power(character, charge - 1),
                ),
                charge * weighted,
            ),
        )
        derivative_rr = interval_add(
            derivative_rr,
            interval_scale(
                interval_multiply(
                    interval_power(radius, degree - 2),
                    interval_power(character, charge),
                ),
                degree * (degree - 1) * weighted,
            ),
        )
        derivative_rc = interval_add(
            derivative_rc,
            interval_scale(
                interval_multiply(
                    interval_power(radius, degree - 1),
                    interval_power(character, charge - 1),
                ),
                degree * charge * weighted,
            ),
        )
        derivative_cc = interval_add(
            derivative_cc,
            interval_scale(
                interval_multiply(
                    interval_power(radius, degree),
                    interval_power(character, charge - 2),
                ),
                charge * (charge - 1) * weighted,
            ),
        )
    return IntervalJet(
        value,
        (derivative_r, derivative_c, zero),
        (
            (derivative_rr, derivative_rc, zero),
            (derivative_rc, derivative_cc, zero),
            (zero, zero, zero),
        ),
    )


def zero_terms(
    terms: list[tuple[int, int, Rational]], maximum_degree: int
) -> list[tuple[int, int, Rational]]:
    minimum_degree = r039.minimum_tail_degree(0, maximum_degree)
    result = []
    for degree, charge, coefficient in terms:
        if charge == 0:
            continue
        result.append(
            (
                degree,
                charge,
                coefficient
                * Rational(degree + minimum_degree, degree + minimum_degree - 1)
                * Rational(abs(charge), 3),
            )
        )
    return result


def upper_charge_scaled_terms(
    terms: list[tuple[int, int, Rational]], character_box: Interval
) -> list[tuple[int, int, Rational]]:
    lower, upper = character_box
    return [
        (
            degree,
            charge,
            coefficient * (lower if charge < 0 else upper) ** charge,
        )
        for degree, charge, coefficient in terms
    ]


def affine_ratio_upper(
    input_charge: int,
    center_charge: int,
    lambda_box: Interval,
) -> Rational:
    return max(
        r051.affine_ratio(input_charge, center_charge, endpoint)
        for endpoint in lambda_box
    )


def positive_endpoint_envelopes(
    terms: list[tuple[int, int, Rational]],
    maximum_degree: int,
    input_charge: int,
    lambda_box: Interval,
) -> tuple[list[Rational], list[Rational], int]:
    minimum_degree = r039.minimum_tail_degree(input_charge, maximum_degree)
    maximum_slope = Rational(input_charge, minimum_degree)
    infinity = [Rational(0)] * (maximum_degree + 1)
    minimum = [Rational(0)] * (maximum_degree + 1)
    for degree, charge, coefficient in terms:
        common = (
            coefficient
            * Rational(degree + minimum_degree, degree + minimum_degree - 1)
            * Rational(
                abs(input_charge - charge),
                3 * abs(input_charge + charge),
            )
            * affine_ratio_upper(input_charge, charge, lambda_box)
        )
        infinity[degree] += common * abs(charge)
        minimum[degree] += common * abs(degree * maximum_slope - charge)
    return r047.trim(infinity), r047.trim(minimum), minimum_degree


def plus_one_envelope(
    terms: list[tuple[int, int, Rational]],
    maximum_degree: int,
    lambda_box: Interval,
) -> list[Rational]:
    minimum_degree = r039.minimum_tail_degree(1, maximum_degree)
    result = [Rational(0)] * (maximum_degree + 1)
    for degree, charge, coefficient in terms:
        result[degree] += (
            coefficient
            * r039.finite_charge_factor(
                degree,
                charge,
                1,
                minimum_degree,
            )
            * affine_ratio_upper(1, charge, lambda_box)
        )
    return r047.trim(result)


def exact_column_envelope(
    terms: list[tuple[int, int, Rational]],
    maximum_degree: int,
    input_degree: int,
    input_charge: int,
    lambda_box: Interval,
) -> list[Rational]:
    result = [Rational(0)] * (maximum_degree + 1)
    for degree, charge, coefficient in terms:
        result[degree] += (
            coefficient
            * Rational(degree + input_degree, input_degree)
            * abs(
                r039.monomial_derivative_coefficient(
                    degree,
                    charge,
                    input_degree,
                    input_charge,
                )
            )
            * affine_ratio_upper(input_charge, charge, lambda_box)
        )
    return r047.trim(result)


def uniform_minus_one_endpoint(
    terms: list[tuple[int, int, Rational]],
    raw_terms: list[tuple[int, int, Rational]],
    maximum_degree: int,
    radius_upper: Rational,
    character_box: Interval,
    lambda_box: Interval,
) -> dict[str, object]:
    minimum_degree = r039.minimum_tail_degree(-1, maximum_degree)
    upper_t = Rational(1, minimum_degree)
    character_lower, character_upper = character_box
    lambda_lower, _ = lambda_box
    q_one_terms = [item for item in raw_terms if item[1] == 1]
    negative_derivative = sum(
        (
            coefficient
            * radius_upper**degree
            * character_upper
            * (
                (degree - 1)
                + 2 * degree**2 * upper_t
                + degree**2 * (degree - 1) * upper_t**2
            )
            / 3
            for degree, _charge, coefficient in q_one_terms
        ),
        Rational(0),
    )
    seeds = [
        coefficient
        for degree, charge, coefficient in raw_terms
        if degree == 1 and charge == 2
    ]
    if len(seeds) != 1:
        raise AssertionError("expected one degree-one q=2 seed")
    seed_derivative = 3 * seeds[0] * radius_upper * character_lower**2
    exceptional_ratio = Rational(1, 1 + lambda_lower)
    margin = seed_derivative - exceptional_ratio * negative_derivative
    if margin <= 0:
        raise AssertionError("uniform affine s=-1 derivative margin is not positive")
    endpoint = exact_column_envelope(
        terms,
        maximum_degree,
        minimum_degree,
        -1,
        lambda_box,
    )
    return {
        "minimumTailDegree": minimum_degree,
        "qOneTermCount": len(q_one_terms),
        "uniformDerivativeMargin": compact_rational_record(margin),
        "endpointPolynomial": endpoint,
        "allDegreeEndpointProved": True,
        "proof": (
            "the q=2 seed is bounded from below with c_L, while the complete "
            "decreasing q=1 contribution is bounded from above with c_U and "
            "lambda_L; the exact positive margin makes j=82 the uniform maximum"
        ),
    }


def inactive_sector_certificate(
    raw_terms: list[tuple[int, int, Rational]],
    maximum_degree: int,
    radius_box: Interval,
    character_box: Interval,
    lambda_box: Interval,
    charge_cutoff: int,
    show_progress: bool,
    started: float,
) -> dict[str, object]:
    radius_upper = radius_box[1]
    terms = upper_charge_scaled_terms(raw_terms, character_box)
    records: list[dict[str, object]] = []
    values: list[tuple[str, Rational]] = []
    progress(show_progress, started, "bounding every fixed positive charge on the root box")
    for input_charge in range(2, charge_cutoff):
        infinity, minimum, degree_floor = positive_endpoint_envelopes(
            terms,
            maximum_degree,
            input_charge,
            lambda_box,
        )
        infinity_value = r047.poly_evaluate(infinity, radius_upper)
        if input_charge == ACTIVE_CHARGE:
            label = f"s={input_charge},x=0"
            value = infinity_value
            endpoint = "x=0; j=81 is the active equality and is excluded"
            polynomial = infinity
        else:
            minimum_value = r047.poly_evaluate(minimum, radius_upper)
            if infinity_value >= minimum_value:
                label = f"s={input_charge},x=0"
                value = infinity_value
                endpoint = "x=0"
                polynomial = infinity
            else:
                label = f"s={input_charge},j={degree_floor}"
                value = minimum_value
                endpoint = f"j={degree_floor}"
                polynomial = minimum
        if value >= 1:
            raise AssertionError(f"inactive fixed positive sector {label} reached one")
        values.append((label, value))
        records.append(
            {
                "label": label,
                "inputCharge": input_charge,
                "endpoint": endpoint,
                "upperBoundOnRootBox": compact_rational_record(value),
                "gapBelowOne": compact_rational_record(1 - value),
                "coefficientSha256": r047.polynomial_digest(polynomial),
                "allCoefficientsNonnegative": r048.all_nonnegative(polynomial),
            }
        )

    progress(show_progress, started, "bounding the plus-one and minus-one sectors")
    plus = plus_one_envelope(terms, maximum_degree, lambda_box)
    plus_value = r047.poly_evaluate(plus, radius_upper)
    minus = uniform_minus_one_endpoint(
        terms,
        raw_terms,
        maximum_degree,
        radius_upper,
        character_box,
        lambda_box,
    )
    minus_poly = minus.pop("endpointPolynomial")
    minus_value = r047.poly_evaluate(minus_poly, radius_upper)
    for label, value, polynomial, proof in [
        (
            "s=1",
            plus_value,
            plus,
            "termwise all-degree finite-charge envelope over c and lambda",
        ),
        ("s=-1", minus_value, minus_poly, minus["proof"]),
    ]:
        if value >= 1:
            raise AssertionError(f"inactive exceptional sector {label} reached one")
        values.append((label, value))
        records.append(
            {
                "label": label,
                "upperBoundOnRootBox": compact_rational_record(value),
                "gapBelowOne": compact_rational_record(1 - value),
                "coefficientSha256": r047.polynomial_digest(polynomial),
                "allCoefficientsNonnegative": r048.all_nonnegative(polynomial),
                "proof": proof,
            }
        )

    progress(show_progress, started, "certifying all infinite large-charge branches")
    large_terms = r051.large_charge_envelope_terms(
        terms,
        radius_upper,
        charge_cutoff,
    )
    large = r047.large_lattice_sector(
        large_terms,
        maximum_degree,
        charge_cutoff,
    )
    large_value = rational(large["bound"]["exact"])
    if large_value >= 1:
        raise AssertionError("large-charge affine envelope reached one")
    values.append((f"s>={charge_cutoff}", large_value))
    records.append(
        {
            "label": f"s>={charge_cutoff}",
            "upperBoundOnRootBox": compact_rational_record(large_value),
            "gapBelowOne": compact_rational_record(1 - large_value),
            "maximumSource": large["maximumSource"],
            "evenDerivativeCertificatePasses": large["evenEndpoint"]
            ["derivativeCertificate"]["allSignedBernsteinCoefficientsPositive"],
            "oddDerivativeCertificatePasses": large["oddEndpoint"]
            ["derivativeCertificate"]["allSignedBernsteinCoefficientsPositive"],
            "proof": (
                "q=-1 uses factor one; q>=0 uses 1+q/S, uniformly for every "
                "lambda>=0, followed by the exact parity/Bernstein theorem"
            ),
        }
    )
    nearest_label, nearest_value = max(values, key=lambda item: item[1])
    return {
        "parameterBox": {
            "radius": [r037.rational_record(value) for value in radius_box],
            "character": [r037.rational_record(value) for value in character_box],
            "lambda": [r037.rational_record(value) for value in lambda_box],
        },
        "activeEqualities": ["s=162,j=81", "s=0,j=81"],
        "inactiveRecords": records,
        "inactiveRecordsCovered": len(records),
        "finitePositiveChargesCovered": charge_cutoff - 2,
        "nearestInactiveSector": nearest_label,
        "nearestInactiveUpperBound": compact_rational_record(nearest_value),
        "minimumGapBelowOne": compact_rational_record(1 - nearest_value),
        "_minimumGap": 1 - nearest_value,
        "minusOneAllDegreeTheorem": minus,
        "largeChargeAllOrderPasses": (
            large["evenEndpoint"]["derivativeCertificate"]
            ["allSignedBernsteinCoefficientsPositive"]
            and large["oddEndpoint"]["derivativeCertificate"]
            ["allSignedBernsteinCoefficientsPositive"]
        ),
        "proof": (
            "r, c^q, and each affine ratio are bounded termwise at exact box "
            "endpoints. Positive coefficients make the envelopes simultaneous. "
            "Fixed-charge convex endpoints, the exceptional all-degree theorems, "
            "and the large-charge parity theorem exhaust every inactive sector."
        ),
        "classification": "formal exact uniform inactive-sector theorem on the root box",
    }


def laurent_add(
    *items: tuple[dict[int, Rational], Rational],
) -> dict[int, Rational]:
    result: dict[int, Rational] = {}
    for polynomial, scale in items:
        for exponent, coefficient in polynomial.items():
            result[exponent] = result.get(exponent, Rational(0)) + scale * coefficient
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def laurent_multiply(
    left: dict[int, Rational], right: dict[int, Rational]
) -> dict[int, Rational]:
    result: dict[int, Rational] = {}
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = left_exponent + right_exponent
            result[exponent] = (
                result.get(exponent, Rational(0))
                + left_coefficient * right_coefficient
            )
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def fixed_radius_moment(
    terms: list[tuple[int, int, Rational]],
    radius: Rational,
    charge_factor: Callable[[int], int],
) -> dict[int, Rational]:
    result: dict[int, Rational] = {}
    for degree, charge, coefficient in terms:
        result[charge] = result.get(charge, Rational(0)) + (
            coefficient * radius**degree * charge_factor(charge)
        )
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def shifted_laurent_polynomial(
    polynomial: dict[int, Rational], shift: int
) -> list[Rational]:
    if min(polynomial) + shift < 0:
        raise ValueError("shift does not clear all Laurent exponents")
    result = [Rational(0)] * (max(polynomial) + shift + 1)
    for exponent, coefficient in polynomial.items():
        result[exponent + shift] = coefficient
    return r047.trim(result)


def sign_variations(coefficients: list[Rational]) -> int:
    signs = [1 if coefficient > 0 else -1 for coefficient in coefficients if coefficient]
    return sum(left != right for left, right in zip(signs, signs[1:]))


def global_affine_upper_certificate(
    active_terms: list[tuple[int, int, Rational]],
    zero_base_terms: list[tuple[int, int, Rational]],
    radius_upper: Rational,
    local_character_box: Interval,
    r050_global_radius_upper: Rational,
    show_progress: bool,
    started: float,
) -> dict[str, object]:
    one = {0: Rational(1)}
    m0 = fixed_radius_moment(active_terms, radius_upper, lambda _q: 1)
    m1 = fixed_radius_moment(active_terms, radius_upper, lambda q: q)
    u0 = fixed_radius_moment(zero_base_terms, radius_upper, lambda _q: 1)
    u1 = fixed_radius_moment(zero_base_terms, radius_upper, abs)
    t0 = fixed_radius_moment(zero_base_terms, radius_upper, lambda q: q)
    one_minus_u0 = laurent_add((one, Rational(1)), (u0, Rational(-1)))
    m0_minus_one = laurent_add((m0, Rational(1)), (one, Rational(-1)))
    zero_denominator = laurent_add(
        (u1, Rational(1)),
        (one_minus_u0, Rational(ACTIVE_CHARGE)),
    )
    feasibility = laurent_add(
        (
            laurent_multiply(m1, one_minus_u0),
            Rational(-1),
        ),
        (
            laurent_multiply(m0_minus_one, zero_denominator),
            Rational(-1),
        ),
    )
    derivative = {
        exponent: exponent * coefficient
        for exponent, coefficient in feasibility.items()
        if exponent * coefficient
    }
    feasibility_poly = shifted_laurent_polynomial(feasibility, 2)
    derivative_poly = shifted_laurent_polynomial(derivative, 2)
    variations = sign_variations(derivative_poly)
    if variations != 3:
        raise AssertionError("eliminated derivative lost its three-sign-variation form")

    derivative_root_boxes = [
        (
            Rational(209259689509981531418051886110, 10**30),
            Rational(209259689509981531418051886111, 10**30),
        ),
        local_character_box,
        (
            Rational(1239043039314477659185496131618, 10**30),
            Rational(1239043039314477659185496131619, 10**30),
        ),
    ]
    expected_signs = [(-1, 1), (1, -1), (-1, 1)]
    root_records = []
    for index, (root_box, signs) in enumerate(
        zip(derivative_root_boxes, expected_signs, strict=True), start=1
    ):
        lower_value = r047.poly_evaluate(derivative_poly, root_box[0])
        upper_value = r047.poly_evaluate(derivative_poly, root_box[1])
        if signs[0] * lower_value <= 0 or signs[1] * upper_value <= 0:
            raise AssertionError(f"eliminated derivative root box {index} lost its signs")
        root_records.append(
            {
                "index": index,
                "box": [r037.rational_record(value) for value in root_box],
                "lowerValue": compact_rational_record(lower_value),
                "upperValue": compact_rational_record(upper_value),
                "signChange": ["-" if signs[0] < 0 else "+", "-" if signs[1] < 0 else "+"],
            }
        )
    # Three disjoint sign-changing boxes give at least three positive roots.
    # Descartes gives at most three, including multiplicity, hence these are all
    # the positive roots and each is simple.
    if not (
        derivative_root_boxes[0][1] < derivative_root_boxes[1][0]
        < derivative_root_boxes[1][1] < derivative_root_boxes[2][0]
    ):
        raise AssertionError("derivative root boxes are not disjoint and ordered")

    progress(
        show_progress,
        started,
        "certifying the eliminated local maximum by exact Bernstein coefficients",
    )
    maximum_box_bernstein = r047.bernstein_coefficients(
        feasibility_poly,
        local_character_box[0],
        local_character_box[1],
    )
    maximum_bernstein = max(maximum_box_bernstein)
    minimum_bernstein = min(maximum_box_bernstein)
    if maximum_bernstein >= 0:
        raise AssertionError("eliminated feasibility is not negative on the maximum box")

    character_lower = Rational(1337, 10000)
    character_upper = Rational(803, 1000)
    u0_lower = r047.poly_evaluate(shifted_laurent_polynomial(u0, 1), character_lower)
    t0_lower = r047.poly_evaluate(shifted_laurent_polynomial(t0, 1), character_lower)
    m1_upper = r047.poly_evaluate(shifted_laurent_polynomial(m1, 1), character_upper)
    feasibility_lower = r047.poly_evaluate(feasibility_poly, character_lower)
    feasibility_upper = r047.poly_evaluate(feasibility_poly, character_upper)
    # The shifted U0/T0/M1 values include one positive factor c.
    if u0_lower <= character_lower:
        raise AssertionError("lower-c zero sector exclusion failed")
    if t0_lower >= 0:
        raise AssertionError("lower-c zero sector monotonicity failed")
    if m1_upper <= 0:
        raise AssertionError("upper-c active moment exclusion failed")
    if feasibility_lower >= 0 or feasibility_upper >= 0:
        raise AssertionError("eliminated feasibility boundary signs failed")
    if radius_upper <= r050_global_radius_upper:
        raise AssertionError("global affine upper radius does not exceed R0.50")

    return {
        "radius": r037.rational_record(radius_upper),
        "elimination": {
            "activeConstraint": "M0+alpha*M1<=1",
            "zeroConstraint": "U0+alpha*U1/(1-162*alpha)<=1",
            "necessaryConditionsAboveR050": ["M0>1", "M1<0", "U0<1"],
            "feasibilityFunction": (
                "E=(-M1)*(1-U0)-(M0-1)*(U1+162*(1-U0))"
            ),
            "criterion": "feasibility implies E>=0",
            "clearedPolynomialDegree": len(feasibility_poly) - 1,
            "clearedPolynomialSha256": r047.polynomial_digest(feasibility_poly),
            "logDerivativePolynomialDegree": len(derivative_poly) - 1,
            "logDerivativePolynomialSha256": r047.polynomial_digest(derivative_poly),
        },
        "derivativeRootTheorem": {
            "descartesSignVariations": variations,
            "positiveRootsAtMost": variations,
            "disjointSignChangingBoxes": root_records,
            "positiveRootsAtLeast": len(root_records),
            "positiveRootsExactly": len(root_records),
            "allPositiveRootsSimple": True,
            "monotonicityPattern": "decreasing, increasing, decreasing, increasing",
            "classification": "formal exact all-positive-axis root-count theorem",
        },
        "relevantCharacterInterval": {
            "lower": r037.rational_record(character_lower),
            "upper": r037.rational_record(character_upper),
            "belowLower": {
                "cTimesU0AtBoundary": compact_rational_record(u0_lower),
                "cTimesT0AtBoundary": compact_rational_record(t0_lower),
                "proof": (
                    "T0 is strictly increasing in log(c), is negative at c_L, "
                    "and U0(c_L)>1; hence U0>1 for every c<=c_L"
                ),
            },
            "aboveUpper": {
                "cTimesM1AtBoundary": compact_rational_record(m1_upper),
                "proof": (
                    "M1 is strictly increasing in log(c), is positive at c_U, "
                    "and the R0.50 global theorem gives M0>1 at this radius; "
                    "hence B=M0+alpha*M1>1 for every c>=c_U"
                ),
            },
            "endpointFeasibilityValues": [
                compact_rational_record(feasibility_lower),
                compact_rational_record(feasibility_upper),
            ],
        },
        "maximumBoxSignCertificate": {
            "box": [r037.rational_record(value) for value in local_character_box],
            "coefficientCount": len(maximum_box_bernstein),
            "allBernsteinCoefficientsNegative": maximum_bernstein < 0,
            "minimumBernsteinCoefficient": compact_rational_record(minimum_bernstein),
            "maximumBernsteinCoefficient": compact_rational_record(maximum_bernstein),
            "signedBernsteinSha256": r047.polynomial_digest(
                [-value for value in maximum_box_bernstein]
            ),
            "classification": "formal exact complete-interval sign certificate",
        },
        "globalExclusion": {
            "noFeasibleAffineWeightAtRadius": True,
            "proof": (
                "outside [c_L,c_U], U0>1 or M0>1 with M1>=0. Inside, the "
                "three-root derivative theorem shows that E can attain a maximum "
                "only at c_L, c_U, or the second derivative-root box. The endpoint "
                "values and every Bernstein coefficient on that box are negative, "
                "so E<0 throughout the remaining domain."
            ),
            "monotonicRadiusExtension": (
                "B and Z have positive coefficients and strictly increase in r; "
                "therefore no radius at or above r_U is feasible"
            ),
            "classification": "formal exact complete-parameter-domain upper bound",
        },
    }


def point_equations(
    active_terms: list[tuple[int, int, Rational]],
    zero_base_terms: list[tuple[int, int, Rational]],
    coordinates: tuple[Rational, Rational, Rational],
) -> tuple[PointJet, PointJet, PointJet]:
    radius, character, alpha = coordinates
    c = PointJet.variable(character, 1)
    a = PointJet.variable(alpha, 2)
    one = PointJet.constant(Rational(1))
    delta = one - a.scale(Rational(ACTIVE_CHARGE))
    moments = [
        point_moment(active_terms, radius, character, power) for power in range(3)
    ]
    u0 = point_moment(zero_base_terms, radius, character, 0)
    # zero_base_terms already contain |q|, so U1 and T1 need one extra |q|.
    # Split signed and absolute moments explicitly below.
    u1 = point_moment(
        [(i, q, coefficient * Rational(abs(q))) for i, q, coefficient in zero_base_terms],
        radius,
        character,
        0,
    )
    t0 = point_moment(zero_base_terms, radius, character, 1)
    t1 = point_moment(
        [(i, q, coefficient * Rational(abs(q))) for i, q, coefficient in zero_base_terms],
        radius,
        character,
        1,
    )
    f = c * (moments[0] + a * moments[1] - one)
    g = c * (delta * (u0 - one) + a * u1)
    h_core = (
        (moments[1] + a * moments[2]) * u1
        - delta * delta * moments[1] * t0
        - a * delta * moments[1] * t1
    )
    h = c * c * h_core
    return f, g, h


def interval_equations(
    active_terms: list[tuple[int, int, Rational]],
    zero_base_terms: list[tuple[int, int, Rational]],
    box: tuple[Interval, Interval, Interval],
) -> tuple[IntervalJet, IntervalJet, IntervalJet]:
    radius, character, alpha = box
    c = IntervalJet.variable(character, 1)
    a = IntervalJet.variable(alpha, 2)
    one = IntervalJet.constant(point(Rational(1)))
    delta = one - a.scale(Rational(ACTIVE_CHARGE))
    moments = [
        interval_moment(active_terms, radius, character, power)
        for power in range(3)
    ]
    absolute_zero_terms = [
        (i, q, coefficient * Rational(abs(q)))
        for i, q, coefficient in zero_base_terms
    ]
    u0 = interval_moment(zero_base_terms, radius, character, 0)
    u1 = interval_moment(absolute_zero_terms, radius, character, 0)
    t0 = interval_moment(zero_base_terms, radius, character, 1)
    t1 = interval_moment(absolute_zero_terms, radius, character, 1)
    f = c * (moments[0] + a * moments[1] - one)
    g = c * (delta * (u0 - one) + a * u1)
    h_core = (
        (moments[1] + a * moments[2]) * u1
        - delta * delta * moments[1] * t0
        - a * delta * moments[1] * t1
    )
    h = c * c * h_core
    return f, g, h


def invert_matrix(matrix: Matrix) -> Matrix:
    size = len(matrix)
    augmented = [
        row[:] + [Rational(int(i == j)) for j in range(size)]
        for i, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if augmented[row][column] != 0),
            None,
        )
        if pivot is None:
            raise ZeroDivisionError("singular rational matrix")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [item / scale for item in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor:
                augmented[row] = [
                    left - factor * right
                    for left, right in zip(
                        augmented[row], augmented[column], strict=True
                    )
                ]
    return [row[size:] for row in augmented]


def matrix_vector(matrix: Matrix, vector: Vector) -> Vector:
    return [
        sum((coefficient * value for coefficient, value in zip(row, vector, strict=True)), Rational(0))
        for row in matrix
    ]


def local_maximum_certificate(
    interval_jets: tuple[IntervalJet, IntervalJet, IntervalJet],
) -> dict[str, object]:
    f, g, _h = interval_jets
    rho = interval_divide(interval_negate(f.gradient[2]), g.gradient[2])
    denominator = interval_add(
        f.gradient[0],
        interval_multiply(rho, g.gradient[0]),
    )
    mu = interval_divide(point(Rational(1)), denominator)
    nu = interval_multiply(rho, mu)
    licq_minor = interval_subtract(
        interval_multiply(f.gradient[0], g.gradient[2]),
        interval_multiply(f.gradient[2], g.gradient[0]),
    )
    if mu[0] <= 0 or nu[0] <= 0:
        raise AssertionError("KKT multipliers are not uniformly positive")
    if licq_minor[0] <= 0:
        raise AssertionError("active constraint gradients failed LICQ")

    zero = point(Rational(0))
    tangent = (zero, g.gradient[2], interval_negate(g.gradient[1]))
    lagrangian_constraint_hessian = []
    for row in range(3):
        hessian_row = []
        for column in range(3):
            hessian_row.append(
                interval_add(
                    interval_multiply(mu, f.hessian[row][column]),
                    interval_multiply(nu, g.hessian[row][column]),
                )
            )
        lagrangian_constraint_hessian.append(hessian_row)
    curvature = zero
    for row in range(3):
        for column in range(3):
            curvature = interval_add(
                curvature,
                interval_multiply(
                    interval_multiply(tangent[row], lagrangian_constraint_hessian[row][column]),
                    tangent[column],
                ),
            )
    if curvature[0] <= 0:
        raise AssertionError("strict second-order local maximum test failed")
    return {
        "multiplierRatioNuOverMu": [
            compact_rational_record(rho[0]),
            compact_rational_record(rho[1]),
        ],
        "mu": [compact_rational_record(mu[0]), compact_rational_record(mu[1])],
        "nu": [compact_rational_record(nu[0]), compact_rational_record(nu[1])],
        "strictComplementarity": mu[0] > 0 and nu[0] > 0,
        "licqMinor": [
            compact_rational_record(licq_minor[0]),
            compact_rational_record(licq_minor[1]),
        ],
        "licqPasses": licq_minor[0] > 0,
        "tangentChoice": "tau=(0,G_alpha,-G_c)",
        "constraintHessianCurvature": [
            compact_rational_record(curvature[0]),
            compact_rational_record(curvature[1]),
        ],
        "strictSecondOrderCondition": curvature[0] > 0,
        "proof": (
            "at the certified root H=0 is the c-alpha stationarity determinant. "
            "The exact interval multipliers in grad(r)=mu*grad(F)+nu*grad(G) "
            "are positive, LICQ holds, and tau^T(mu Hess(F)+nu Hess(G)) tau>0. "
            "Since Hess(r)=0, the Lagrangian is strictly negative on the "
            "one-dimensional critical tangent space."
        ),
        "classification": "formal exact strict constrained local-maximum theorem",
    }


def krawczyk_certificate(
    active_terms: list[tuple[int, int, Rational]],
    zero_base_terms: list[tuple[int, int, Rational]],
    box: tuple[Interval, Interval, Interval],
) -> dict[str, object]:
    center = tuple((lower + upper) / 2 for lower, upper in box)
    radii = [(upper - lower) / 2 for lower, upper in box]
    equations = point_equations(active_terms, zero_base_terms, center)
    values = [equation.value for equation in equations]
    jacobian = [list(equation.gradient) for equation in equations]
    inverse = invert_matrix(jacobian)
    interval_jets = interval_equations(active_terms, zero_base_terms, box)
    jacobian_interval: IntervalMatrix = [
        list(equation.gradient) for equation in interval_jets
    ]

    correction = matrix_vector(inverse, values)
    corrected_center = [coordinate - item for coordinate, item in zip(center, correction, strict=True)]
    remainder: IntervalMatrix = []
    for row in range(3):
        remainder_row = []
        for column in range(3):
            product = point(Rational(0))
            for inner in range(3):
                product = interval_add(
                    product,
                    interval_scale(jacobian_interval[inner][column], inverse[row][inner]),
                )
            identity = point(Rational(int(row == column)))
            remainder_row.append(interval_subtract(identity, product))
        remainder.append(remainder_row)

    image = []
    image_radii = []
    for row in range(3):
        radius = sum(
            (
                interval_abs_upper(remainder[row][column]) * radii[column]
                for column in range(3)
            ),
            Rational(0),
        )
        image_radii.append(radius)
        image.append((corrected_center[row] - radius, corrected_center[row] + radius))
    strict_inclusion = all(
        lower < image_lower < image_upper < upper
        for (lower, upper), (image_lower, image_upper) in zip(box, image, strict=True)
    )
    if not strict_inclusion:
        raise AssertionError("exact Krawczyk image is not strictly inside the root box")

    return {
        "center": [r037.rational_record(value) for value in center],
        "pointResidual": [compact_rational_record(value) for value in values],
        "pointJacobian": [
            [compact_rational_record(value) for value in row] for row in jacobian
        ],
        "pointJacobianInverse": [
            [compact_rational_record(value) for value in row] for row in inverse
        ],
        "intervalJacobian": [
            [
                [
                    compact_rational_record(value[0]),
                    compact_rational_record(value[1]),
                ]
                for value in row
            ]
            for row in jacobian_interval
        ],
        "newtonCorrectedCenter": [
            compact_rational_record(value) for value in corrected_center
        ],
        "krawczykImageRadii": [
            compact_rational_record(value) for value in image_radii
        ],
        "krawczykImage": [
            [
                compact_rational_record(value[0]),
                compact_rational_record(value[1]),
            ]
            for value in image
        ],
        "strictlyInsideBox": strict_inclusion,
        "theorem": (
            "the exact Krawczyk image K(x0,X) is strictly contained in the "
            "interior of X; therefore F=G=H=0 has exactly one zero in X"
        ),
        "classification": "formal exact local existence-and-uniqueness certificate",
        "_intervalJets": interval_jets,
    }


def mp_value(value: Rational) -> mp.mpf:
    return mp.mpf(int(value.numerator)) / int(value.denominator)


def high_precision_localization(
    active_terms: list[tuple[int, int, Rational]],
    zero_base_terms: list[tuple[int, int, Rational]],
    initial: tuple[Rational, Rational, Rational],
    digits: int,
) -> dict[str, str]:
    mp.mp.dps = digits
    active = [(i, q, mp_value(coefficient)) for i, q, coefficient in active_terms]
    zero = [(i, q, mp_value(coefficient)) for i, q, coefficient in zero_base_terms]

    def equations(radius: mp.mpf, character: mp.mpf, alpha: mp.mpf):
        moments = [mp.mpf("0"), mp.mpf("0"), mp.mpf("0")]
        for degree, charge, coefficient in active:
            monomial = coefficient * radius**degree * character**charge
            moments[0] += monomial
            moments[1] += charge * monomial
            moments[2] += charge**2 * monomial
        u0 = u1 = t0 = t1 = mp.mpf("0")
        for degree, charge, coefficient in zero:
            monomial = coefficient * radius**degree * character**charge
            u0 += monomial
            u1 += abs(charge) * monomial
            t0 += charge * monomial
            t1 += charge * abs(charge) * monomial
        delta = 1 - ACTIVE_CHARGE * alpha
        f = character * (moments[0] + alpha * moments[1] - 1)
        g = character * (delta * (u0 - 1) + alpha * u1)
        h = character**2 * (
            (moments[1] + alpha * moments[2]) * u1
            - delta**2 * moments[1] * t0
            - alpha * delta * moments[1] * t1
        )
        return f, g, h

    root = mp.findroot(
        equations,
        tuple(mp_value(value) for value in initial),
        solver="mdnewton",
        tol=mp.mpf(10) ** (-(digits - 15)),
        maxsteps=100,
    )
    radius, character, alpha = root
    lam = alpha / (1 - ACTIVE_CHARGE * alpha)
    residual = equations(radius, character, alpha)
    return {
        "radius": mp.nstr(radius, digits),
        "character": mp.nstr(character, digits),
        "alpha162": mp.nstr(alpha, digits),
        "lambda": mp.nstr(lam, digits),
        "maximumAbsoluteResidual": mp.nstr(max(abs(value) for value in residual), 12),
        "classification": "high-precision diagnostic localization only",
    }


def build_payload(
    maximum_degree: int,
    radius_box: Interval,
    character_box: Interval,
    alpha_box: Interval,
    charge_cutoff: int,
    localization_digits: int,
    show_progress: bool,
    source_commit: str | None,
) -> dict[str, object]:
    started = time.perf_counter()
    progress(show_progress, started, "loading pinned R0.51 certificate")
    if sha256(R051_CERTIFICATE) != R051_EXPECTED_SHA256:
        raise AssertionError("R0.51 certificate hash mismatch")
    if maximum_degree != 80 or charge_cutoff != 241:
        raise AssertionError("R0.52 audit is pinned to N=80 and S=241")
    box = (radius_box, character_box, alpha_box)
    if not all(0 < lower < upper for lower, upper in box):
        raise AssertionError("all root-box intervals must be positive and ordered")
    if not alpha_box[1] < Rational(1, ACTIVE_CHARGE):
        raise AssertionError("alpha box leaves the lambda>=0 compactification domain")

    progress(show_progress, started, "constructing exact degree-80 center")
    active_field, _, _, recurrence_interactions = r028.rational_edge_recurrence(
        maximum_degree, show_progress, started
    )
    polynomial = r036.field_to_polynomial(active_field, maximum_degree)
    polynomial_digest = r037.polynomial_digest(polynomial)
    if polynomial_digest != R051_POLYNOMIAL_SHA256:
        raise AssertionError("degree-80 polynomial digest changed")
    terms = r048.independent_terms(polynomial)
    active_terms = r050.active_laurent_terms(terms, 81, ACTIVE_CHARGE)
    zero_base_terms = zero_terms(terms, maximum_degree)
    if min(q for _, q, _ in active_terms) != -1:
        raise AssertionError("active Laurent support changed")
    if min(q for _, q, _ in zero_base_terms) != -1:
        raise AssertionError("zero-sector Laurent support changed")

    progress(show_progress, started, "localizing the stationary candidate at high precision")
    midpoint = tuple((lower + upper) / 2 for lower, upper in box)
    localization = high_precision_localization(
        active_terms, zero_base_terms, midpoint, localization_digits
    )
    progress(
        show_progress,
        started,
        "running exact rational Krawczyk inclusion",
        radius=localization["radius"][:24],
        character=localization["character"][:24],
        alpha=localization["alpha162"][:24],
    )
    krawczyk = krawczyk_certificate(active_terms, zero_base_terms, box)
    interval_jets = krawczyk.pop("_intervalJets")
    progress(show_progress, started, "certifying strict constrained local maximality")
    local_maximum = local_maximum_certificate(interval_jets)

    alpha_lower, alpha_upper = alpha_box
    lambda_lower = alpha_lower / (1 - ACTIVE_CHARGE * alpha_lower)
    lambda_upper = alpha_upper / (1 - ACTIVE_CHARGE * alpha_upper)
    progress(show_progress, started, "certifying every inactive sector on the root box")
    inactive = inactive_sector_certificate(
        terms,
        maximum_degree,
        radius_box,
        character_box,
        (lambda_lower, lambda_upper),
        charge_cutoff,
        show_progress,
        started,
    )
    inactive_minimum_gap = inactive.pop("_minimumGap")
    r051_certificate = json.loads(R051_CERTIFICATE.read_text(encoding="utf-8"))
    r050_global_radius_upper = rational(
        r051_certificate["comparisonWithR050"]["r050GlobalOptimalRadiusUpper"]
        ["exact"]
    )
    progress(show_progress, started, "eliminating alpha on the complete parameter domain")
    global_upper = global_affine_upper_certificate(
        active_terms,
        zero_base_terms,
        radius_box[1],
        character_box,
        r050_global_radius_upper,
        show_progress,
        started,
    )
    r051_root_upper = rational(
        r051_certificate["thresholdTheorem"]["rootIsolation"]["upper"]["exact"]
    )
    gain_lower = radius_box[0] / r051_root_upper
    checks = {
        "r051CertificateHashMatches": True,
        "polynomialDigestMatchesR051": polynomial_digest == R051_POLYNOMIAL_SHA256,
        "alphaCompactificationInsideDomain": alpha_box[1] < Rational(1, ACTIVE_CHARGE),
        "lambdaBoxIsPositive": lambda_lower > 0,
        "krawczykImageStrictlyInsideBox": krawczyk["strictlyInsideBox"],
        "uniqueLocalStationaryRootCertified": krawczyk["strictlyInsideBox"],
        "strictConstrainedLocalMaximumCertified": local_maximum[
            "strictSecondOrderCondition"
        ],
        "positiveKktMultipliersCertified": local_maximum[
            "strictComplementarity"
        ],
        "activeConstraintLicqCertified": local_maximum["licqPasses"],
        "allInactiveRootBoxSectorsStrictlyBelowOne": inactive_minimum_gap > 0,
        "allFixedPositiveRootBoxSectorsCovered": (
            inactive["finitePositiveChargesCovered"] == charge_cutoff - 2
        ),
        "minusOneAllDegreeRootBoxTheoremPasses": inactive[
            "minusOneAllDegreeTheorem"
        ]["allDegreeEndpointProved"],
        "largeChargeAllOrderRootBoxTheoremPasses": inactive[
            "largeChargeAllOrderPasses"
        ],
        "globalEliminatedDerivativeHasExactlyThreePositiveRoots": global_upper[
            "derivativeRootTheorem"
        ]["positiveRootsExactly"]
        == 3,
        "globalEliminatedMaximumBoxIsStrictlyNegative": global_upper[
            "maximumBoxSignCertificate"
        ]["allBernsteinCoefficientsNegative"],
        "completeAffineDomainExcludedAtUpperRadius": global_upper[
            "globalExclusion"
        ]["noFeasibleAffineWeightAtRadius"],
        "globalAffineRadiusGapIsOneEminusForty": (
            radius_box[1] - radius_box[0] == Rational(1, 10**40)
        ),
        "localRadiusStrictlyExceedsR051FixedRoot": radius_box[0] > r051_root_upper,
        "localGainLowerFactorExceedsOne": gain_lower > 1,
        "noFloatingPointSignDecision": True,
        "exactGlobalMaximizerUniquenessNotClaimed": True,
        "threeDimensionalNavierStokesRegularityNotClaimed": True,
    }
    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError("R0.52 checks failed: " + ", ".join(failed))
    progress(show_progress, started, "all exact checks passed", checks=len(checks))

    return {
        "schemaVersion": "1.0",
        "scope": {
            "system": "reduced canonical edge generating system",
            "theorem": (
                "exact local root and inactive-sector theorem together with a "
                "width-10^-40 global optimum enclosure for the complete "
                "degree-80 affine charge-weight family"
            ),
            "notClaimed": [
                "an exact-real uniqueness theorem for the global affine maximizer",
                "optimization over all possible Banach norms",
                "a critical-norm bridge for arbitrary three-dimensional velocity fields",
                "three-dimensional Navier-Stokes regularity or singularity",
            ],
        },
        "weight": {
            "formula": "omega_s(c,lambda)=c^s(1+lambda*|s|)",
            "compactification": "alpha=lambda/(1+162*lambda)",
            "inverse": "lambda=alpha/(1-162*alpha)",
            "domain": "c>0, 0<=alpha<1/162",
        },
        "exactSystem": {
            "variables": ["r", "c", "alpha"],
            "delta": "1-162*alpha",
            "equations": [
                "F=c*(M0+alpha*M1-1)",
                "G=c*(delta*(U0-1)+alpha*U1)",
                (
                    "H=c^2*((M1+alpha*M2)*U1-delta^2*M1*T0"
                    "-alpha*delta*M1*T1)"
                ),
            ],
            "stationarityIdentity": (
                "H=c^2*delta^2*((d_t B162)(d_alpha Z0)"
                "-(d_alpha B162)(d_t Z0))"
            ),
            "positiveClearingFactors": ["c", "c*delta", "c^2*delta^2"],
            "classification": "formal exact polynomialized three-equation system",
        },
        "finiteConstruction": {
            "maximumTotalDegree": maximum_degree,
            "chargeCutoff": charge_cutoff,
            "centerTerms": len(terms),
            "activeTerms": len(active_terms),
            "zeroSectorTerms": len(zero_base_terms),
            "recurrenceOrderedInteractions": recurrence_interactions,
            "degreeEightyPolynomialSha256": polynomial_digest,
            "classification": "finite exact degree-80 construction",
        },
        "rootIsolation": {
            "radius": [
                r037.rational_record(radius_box[0]),
                r037.rational_record(radius_box[1]),
            ],
            "character": [
                r037.rational_record(character_box[0]),
                r037.rational_record(character_box[1]),
            ],
            "alpha162": [
                r037.rational_record(alpha_box[0]),
                r037.rational_record(alpha_box[1]),
            ],
            "lambda": [
                r037.rational_record(lambda_lower),
                r037.rational_record(lambda_upper),
            ],
            "highPrecisionDiagnostic": localization,
            "krawczykCertificate": krawczyk,
            "localMaximumCertificate": local_maximum,
            "classification": "formal exact rational local root box",
        },
        "comparisonWithR051": {
            "r051RootUpper": r037.rational_record(r051_root_upper),
            "localRootRadiusLower": r037.rational_record(radius_box[0]),
            "radiusGainLowerFactor": r037.rational_record(gain_lower),
            "interpretation": (
                "the locally stationary affine-family radius is strictly above the "
                "fixed R0.51 rational-weight threshold; global optimality remains open"
            ),
        },
        "inactiveSectorTheorem": inactive,
        "globalAffineFamilyBound": {
            "optimalRadiusLower": r037.rational_record(radius_box[0]),
            "optimalRadiusUpper": r037.rational_record(radius_box[1]),
            "gapWidth": r037.rational_record(radius_box[1] - radius_box[0]),
            "lowerProof": (
                "the exact Krawczyk root has both active columns equal to one, "
                "all 242 inactive sector envelopes are below one, and its radius "
                "lies strictly above r_L"
            ),
            "upperProof": (
                "the eliminated feasibility theorem excludes every c>0 and "
                "lambda>=0 at r_U; radius monotonicity excludes all larger radii"
            ),
            "whatRemains": (
                "the width-10^-40 enclosure does not by itself identify the local "
                "KKT root with the unique global maximizer as an exact real number"
            ),
            "classification": (
                "formal exact global lower-and-upper bound for the complete affine family"
            ),
        },
        "globalUpperCertificate": global_upper,
        "remainingBeyondR052": [
            "turn the width-10^-40 global enclosure into an exact uniqueness theorem if useful",
            "test larger submultiplicative weight families without losing all-order sector closure",
            "construct or rule out a critical-space bridge to the full three-dimensional PDE",
        ],
        "checks": checks,
        "git": r039.git_state(source_commit),
        "computation": {
            "createdUtc": datetime.now(timezone.utc).isoformat(),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "exactBackend": f"gmpy2 {gmpy2.version()} / GMP {gmpy2.mp_version()}",
            "localizationBackend": f"mpmath {mp.__version__} at {localization_digits} decimal digits",
            "randomness": False,
            "gpu": False,
            "decimalDecisionUse": False,
            "wallSeconds": time.perf_counter() - started,
        },
    }


def parse_box(lower: str, upper: str) -> Interval:
    return rational(lower), rational(upper)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-total-degree", type=int, default=80)
    parser.add_argument(
        "--radius-lower",
        default="3826244718485988314760952288871012330925/10000000000000000000000000000000000000000",
    )
    parser.add_argument(
        "--radius-upper",
        default="3826244718485988314760952288871012330926/10000000000000000000000000000000000000000",
    )
    parser.add_argument(
        "--character-lower",
        default="7975595104326214175951774729017091063394/10000000000000000000000000000000000000000",
    )
    parser.add_argument(
        "--character-upper",
        default="7975595104326214175951774729017091063395/10000000000000000000000000000000000000000",
    )
    parser.add_argument(
        "--alpha-lower",
        default="61234500552300731923346973685049743915/10000000000000000000000000000000000000000",
    )
    parser.add_argument(
        "--alpha-upper",
        default="61234500552300731923346973685049743916/10000000000000000000000000000000000000000",
    )
    parser.add_argument("--localization-digits", type=int, default=100)
    parser.add_argument("--charge-cutoff", type=int, default=241)
    parser.add_argument("--source-commit")
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--progress-log", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    global PROGRESS_LOG
    PROGRESS_LOG = arguments.progress_log
    if PROGRESS_LOG is not None:
        PROGRESS_LOG.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_LOG.write_text("", encoding="utf-8")

    payload = build_payload(
        arguments.max_total_degree,
        parse_box(arguments.radius_lower, arguments.radius_upper),
        parse_box(arguments.character_lower, arguments.character_upper),
        parse_box(arguments.alpha_lower, arguments.alpha_upper),
        arguments.charge_cutoff,
        arguments.localization_digits,
        arguments.progress,
        arguments.source_commit,
    )
    if arguments.check:
        failed = [name for name, value in payload["checks"].items() if not value]
        if failed:
            raise SystemExit("failed checks: " + ", ".join(failed))
    if arguments.output:
        r039.atomic_json_write(arguments.output, payload, arguments.pretty)
    else:
        json.dump(
            payload,
            sys.stdout,
            ensure_ascii=False,
            indent=2 if arguments.pretty else None,
            sort_keys=True,
        )
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
