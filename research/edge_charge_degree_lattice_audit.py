#!/usr/bin/env python3
"""R0.47 exact charge-degree lattice endpoint audit.

R0.46 certified the reduced canonical edge generating system at r=0.376 in
the zero/nonzero-charge two-block norm.  At r=0.377, its inherited
large-positive-charge bound was 1.003041..., but that estimate separately
maximized the degree factor, the q=-1 charge ratio, and the common slope.

This audit retains the exact charge-degree lattice relation.  For every fixed
positive input charge s, let J_s be the minimum admissible tail degree.  The
exact i-dependent degree factor is bounded by its value at J_s *inside* the
complete positive sum.  The remaining common-slope function is convex, so
every degree j>=J_s is controlled by the endpoints x=0 and x=s/J_s.

For 2<=s<241, all 239 fixed charges are evaluated exactly.  This is a finite
enumeration of analytic all-degree theorems, not a finite tail-degree grid.

For s>=241, the lattice has two exact branches:

    even s: J_s=s/2,       x=2;
    odd  s: J_s=(s+3)/2,   x=2s/(s+3).

Writing y=1/s turns the two endpoint sums into exact rational functions.
After clearing their positive linear denominators, the even derivative has
strictly positive Bernstein coefficients on 0<=y<=1/242, while the negative
odd derivative has strictly positive Bernstein coefficients on
0<=y<=1/241.  Thus the even branch is maximized at s=242 and the odd branch
is bounded by its y=0 limit.  No charge cutoff beyond the analytic split, no
tail-degree scan, coefficient-sign cancellation, or floating-point threshold
decision is used.

The exact fixed-charge s=162 endpoint then becomes limiting.  The target
r=0.376932 passes, while the adjacent millionth r=0.376933 fails in the true
j=81, s=162 induced column of this specific two-block weighted-l1 norm.
This is not a singularity theorem and does not prove failure of another norm
or of a nonlinear existence argument.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import sys
import time

import gmpy2

import edge_charge_resolved_audit as r039
import edge_degree_resolved_tail_audit as r041
import edge_rational_asymptotic_audit as r028
import edge_short_continuation_audit as r036
import edge_two_block_weight_audit as r046
import edge_weighted_restart_audit as r037


Rational = gmpy2.mpq
Polynomial = dict[tuple[int, int], Rational]
Poly = list[Rational]

R046_CERTIFICATE = Path(
    "research/certificates/r046/edge-two-block-weight.json"
)
R046_EXPECTED_SHA256 = (
    "9310267b894c32b61034ec5e8f34b7d49144028830713a5e86b59d5be00109d1"
)
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(
            f"[R0.47 +{elapsed:8.2f}s] {stage}{suffix}",
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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rational(value: str | int | Rational) -> Rational:
    return Rational(value)


def trim(poly: Poly) -> Poly:
    result = poly[:]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def poly_add(left: Poly, right: Poly) -> Poly:
    result = [Rational(0)] * max(len(left), len(right))
    for index, coefficient in enumerate(left):
        result[index] += coefficient
    for index, coefficient in enumerate(right):
        result[index] += coefficient
    return trim(result)


def poly_scale(poly: Poly, scalar: Rational) -> Poly:
    return trim([coefficient * scalar for coefficient in poly])


def poly_multiply(left: Poly, right: Poly) -> Poly:
    result = [Rational(0)] * (len(left) + len(right) - 1)
    for left_index, left_coefficient in enumerate(left):
        if left_coefficient == 0:
            continue
        for right_index, right_coefficient in enumerate(right):
            if right_coefficient:
                result[left_index + right_index] += (
                    left_coefficient * right_coefficient
                )
    return trim(result)


def poly_derivative(poly: Poly) -> Poly:
    if len(poly) <= 1:
        return [Rational(0)]
    return trim(
        [Rational(index) * poly[index] for index in range(1, len(poly))]
    )


def poly_evaluate(poly: Poly, value: Rational) -> Rational:
    result = Rational(0)
    for coefficient in reversed(poly):
        result = result * value + coefficient
    return result


def divide_linear(poly: Poly, slope: int) -> Poly:
    """Divide an exactly divisible polynomial by 1+slope*y."""

    if slope == 0:
        return poly[:]
    if len(poly) < 2:
        raise AssertionError("cannot divide a constant by a nonconstant factor")
    quotient = [Rational(0)] * (len(poly) - 1)
    quotient[0] = poly[0]
    for index in range(1, len(quotient)):
        quotient[index] = poly[index] - slope * quotient[index - 1]
    if poly[-1] != slope * quotient[-1]:
        raise AssertionError("inexact linear polynomial division")
    return trim(quotient)


def denominator_polynomial(factor_counts: dict[int, int]) -> Poly:
    result = [Rational(1)]
    for slope, multiplicity in sorted(factor_counts.items()):
        if slope == 0:
            continue
        for _ in range(multiplicity):
            result = poly_multiply(
                result,
                [Rational(1), Rational(slope)],
            )
    return result


def polynomial_digest(poly: Poly) -> str:
    serialized = "".join(f"{index}:{coefficient}\n" for index, coefficient in enumerate(poly))
    return hashlib.sha256(serialized.encode("ascii")).hexdigest()


def power_coefficients_on_unit_interval(
    poly: Poly,
    lower: Rational,
    upper: Rational,
) -> Poly:
    """Return coefficients of poly(lower+(upper-lower)*t)."""

    degree = len(poly) - 1
    width = upper - lower
    result = [Rational(0)] * (degree + 1)
    for power, coefficient in enumerate(poly):
        for transformed_power in range(power + 1):
            result[transformed_power] += (
                coefficient
                * math.comb(power, transformed_power)
                * lower ** (power - transformed_power)
                * width**transformed_power
            )
    return trim(result)


def bernstein_coefficients(
    poly: Poly,
    lower: Rational,
    upper: Rational,
) -> Poly:
    """Exact degree-n Bernstein coefficients on [lower, upper]."""

    power = power_coefficients_on_unit_interval(poly, lower, upper)
    degree = len(poly) - 1
    power.extend([Rational(0)] * (degree + 1 - len(power)))
    result = []
    for bernstein_index in range(degree + 1):
        value = sum(
            (
                power[power_index]
                * Rational(
                    math.comb(bernstein_index, power_index),
                    math.comb(degree, power_index),
                )
                for power_index in range(bernstein_index + 1)
            ),
            Rational(0),
        )
        result.append(value)
    return result


def positive_denominator_upper(
    factor_counts: dict[int, int],
    upper: Rational,
) -> Rational:
    result = Rational(1)
    for slope, multiplicity in factor_counts.items():
        if slope == 0:
            continue
        endpoint = 1 + slope * upper
        if endpoint <= 0:
            raise AssertionError("rational-function denominator can vanish")
        result *= max(Rational(1), endpoint) ** multiplicity
    return result


def rational_function_derivative_certificate(
    numerator: Poly,
    denominator: Poly,
    factor_counts: dict[int, int],
    upper: Rational,
    expected_sign: int,
) -> dict[str, object]:
    """Certify one derivative sign by exact Bernstein coefficients."""

    derivative_numerator = poly_add(
        poly_multiply(poly_derivative(numerator), denominator),
        poly_scale(
            poly_multiply(numerator, poly_derivative(denominator)),
            Rational(-1),
        ),
    )
    signed = poly_scale(derivative_numerator, Rational(expected_sign))
    coefficients = bernstein_coefficients(
        signed,
        Rational(0),
        upper,
    )
    minimum = min(coefficients)
    maximum = max(coefficients)
    if minimum <= 0:
        raise AssertionError("Bernstein derivative sign certificate failed")
    denominator_upper = positive_denominator_upper(factor_counts, upper)
    derivative_magnitude_lower = minimum / denominator_upper**2
    return {
        "interval": [
            r037.rational_record(Rational(0)),
            r037.rational_record(upper),
        ],
        "expectedDerivativeSign": "+" if expected_sign == 1 else "-",
        "numeratorDegree": len(numerator) - 1,
        "denominatorDegree": len(denominator) - 1,
        "derivativeNumeratorDegree": len(derivative_numerator) - 1,
        "linearFactorCount": len(factor_counts),
        "denominatorDegreeFromFactors": sum(factor_counts.values()),
        "denominatorPositive": True,
        "bernsteinDegree": len(coefficients) - 1,
        "bernsteinCoefficientCount": len(coefficients),
        "allSignedBernsteinCoefficientsPositive": True,
        "minimumSignedBernsteinCoefficient": r037.rational_record(minimum),
        "maximumSignedBernsteinCoefficient": r037.rational_record(maximum),
        "denominatorUpperBound": r037.rational_record(denominator_upper),
        "derivativeMagnitudeLowerBound": r037.rational_record(
            derivative_magnitude_lower
        ),
        "numeratorSha256": polynomial_digest(numerator),
        "denominatorSha256": polynomial_digest(denominator),
        "derivativeNumeratorSha256": polynomial_digest(derivative_numerator),
        "signedBernsteinSha256": polynomial_digest(coefficients),
        "subdivisionCount": 1,
        "proof": (
            "the rational denominator is positive; the derivative numerator "
            "has the stated sign because every exact degree-n Bernstein "
            "coefficient on the complete interval has that strict sign"
        ),
        "classification": "formal exact continuous-interval sign certificate",
    }


def endpoint_rational_function(
    terms: list[tuple[int, int, Rational]],
    branch: str,
) -> tuple[Poly, Poly, dict[int, int]]:
    """Build the exact even or odd minimum-lattice endpoint as E(y)."""

    if branch not in {"even", "odd"}:
        raise ValueError("branch must be even or odd")
    term_denominators: list[dict[int, int]] = []
    term_numerators: list[tuple[Poly, Rational]] = []
    common_factor_counts: dict[int, int] = {}

    for degree, charge, weighted_coefficient in terms:
        if not -1 <= charge <= 2 * degree:
            raise AssertionError("center term left the active support cone")
        if branch == "even":
            denominator_slopes = [2 * (degree - 1), charge]
            numerator = poly_multiply(
                [Rational(1), Rational(2 * degree)],
                [Rational(1), Rational(-charge)],
            )
            coefficient = (
                weighted_coefficient * abs(2 * degree - charge) / 3
            )
        else:
            denominator_slopes = [2 * degree + 1, charge, 3]
            numerator = poly_multiply(
                [Rational(1), Rational(2 * degree + 3)],
                [Rational(1), Rational(-charge)],
            )
            if charge < 2 * degree:
                absolute_numerator = [
                    Rational(2 * degree - charge),
                    Rational(-3 * charge),
                ]
            elif charge == 2 * degree:
                absolute_numerator = [
                    Rational(0),
                    Rational(6 * degree),
                ]
            else:
                raise AssertionError("odd endpoint met charge above 2i")
            numerator = poly_multiply(numerator, absolute_numerator)
            coefficient = weighted_coefficient / 3

        factor_counts: dict[int, int] = {}
        for slope in denominator_slopes:
            if slope:
                factor_counts[slope] = factor_counts.get(slope, 0) + 1
        for slope, multiplicity in factor_counts.items():
            common_factor_counts[slope] = max(
                common_factor_counts.get(slope, 0),
                multiplicity,
            )
        term_denominators.append(factor_counts)
        term_numerators.append((numerator, coefficient))

    denominator = denominator_polynomial(common_factor_counts)
    numerator = [Rational(0)]
    for factor_counts, (term_numerator, coefficient) in zip(
        term_denominators,
        term_numerators,
        strict=True,
    ):
        quotient = denominator[:]
        for slope, multiplicity in factor_counts.items():
            for _ in range(multiplicity):
                quotient = divide_linear(quotient, slope)
        numerator = poly_add(
            numerator,
            poly_scale(
                poly_multiply(term_numerator, quotient),
                coefficient,
            ),
        )
    return numerator, denominator, common_factor_counts


def rational_function_value(
    numerator: Poly,
    denominator: Poly,
    value: Rational,
) -> Rational:
    denominator_value = poly_evaluate(denominator, value)
    if denominator_value <= 0:
        raise AssertionError("endpoint rational denominator is not positive")
    return poly_evaluate(numerator, value) / denominator_value


def fixed_positive_columns(
    terms: list[tuple[int, int, Rational]],
    cutoff: int,
    charge_cutoff: int,
) -> list[dict[str, object]]:
    """Exact i-dependent two-endpoint theorem for 2<=s<S."""

    records: list[dict[str, object]] = []
    for input_charge in range(2, charge_cutoff):
        minimum_degree = r039.minimum_tail_degree(input_charge, cutoff)
        maximum_slope = Rational(input_charge, minimum_degree)
        endpoint_zero = Rational(0)
        endpoint_minimum = Rational(0)
        for degree, charge, weighted_coefficient in terms:
            if input_charge + charge <= 0:
                raise AssertionError("positive input charge met zero output")
            degree_factor = Rational(
                degree + minimum_degree,
                degree + minimum_degree - 1,
            )
            charge_factor = Rational(
                abs(input_charge - charge),
                3 * abs(input_charge + charge),
            )
            common_weight = (
                weighted_coefficient * degree_factor * charge_factor
            )
            endpoint_zero += common_weight * abs(charge)
            endpoint_minimum += common_weight * abs(
                degree * maximum_slope - charge
            )
        bound = max(endpoint_zero, endpoint_minimum)
        records.append(
            {
                "inputCharge": input_charge,
                "minimumTailDegree": minimum_degree,
                "maximumInputSlope": r037.rational_record(maximum_slope),
                "endpointAtInfinity": r037.rational_record(endpoint_zero),
                "endpointAtMinimumDegree": r037.rational_record(
                    endpoint_minimum
                ),
                "maximumEndpoint": (
                    "x=0"
                    if endpoint_zero >= endpoint_minimum
                    else "x=s/J_s"
                ),
                "bound": r037.rational_record(bound),
                "proof": (
                    "for j>=J_s, each exact degree factor d_i(j) is at most "
                    "d_i(J_s); after retaining d_i(J_s) inside the complete "
                    "sum, the common-slope core is convex on "
                    "0<=x<=s/J_s and is maximized at one of its two endpoints"
                ),
                "classification": (
                    "formal all-degree fixed-charge endpoint theorem with "
                    "the exact i-dependent minimum-degree factors"
                ),
            }
        )
    return records


def large_lattice_sector(
    terms: list[tuple[int, int, Rational]],
    cutoff: int,
    charge_cutoff: int,
) -> dict[str, object]:
    """All-order parity theorem for every s>=S and every admissible j."""

    if charge_cutoff != 241 or cutoff != 80:
        raise AssertionError("R0.47 parity constants are pinned to N=80,S=241")

    zero_endpoint_uniform = Rational(0)
    common_degree_floor = 121
    for degree, charge, weighted_coefficient in terms:
        degree_factor = Rational(
            degree + common_degree_floor,
            degree + common_degree_floor - 1,
        )
        charge_factor = (
            Rational(charge_cutoff + 1, charge_cutoff - 1)
            if charge == -1
            else Rational(1)
        )
        zero_endpoint_uniform += (
            weighted_coefficient
            * degree_factor
            * charge_factor
            * abs(charge)
            / 3
        )

    even_numerator, even_denominator, even_factors = (
        endpoint_rational_function(terms, "even")
    )
    odd_numerator, odd_denominator, odd_factors = (
        endpoint_rational_function(terms, "odd")
    )
    even_upper = Rational(1, 242)
    odd_upper = Rational(1, 241)
    even_derivative = rational_function_derivative_certificate(
        even_numerator,
        even_denominator,
        even_factors,
        even_upper,
        1,
    )
    odd_derivative = rational_function_derivative_certificate(
        odd_numerator,
        odd_denominator,
        odd_factors,
        odd_upper,
        -1,
    )
    even_at_242 = rational_function_value(
        even_numerator,
        even_denominator,
        even_upper,
    )
    even_limit = rational_function_value(
        even_numerator,
        even_denominator,
        Rational(0),
    )
    odd_at_241 = rational_function_value(
        odd_numerator,
        odd_denominator,
        odd_upper,
    )
    odd_limit = rational_function_value(
        odd_numerator,
        odd_denominator,
        Rational(0),
    )
    if even_limit != odd_limit:
        raise AssertionError("parity endpoint functions have different limits")
    maximum = max(zero_endpoint_uniform, even_at_242, odd_limit)
    maximum_source = max(
        [
            ("x=0 uniform", zero_endpoint_uniform),
            ("even s=242,j=121", even_at_242),
            ("odd y=0 limit", odd_limit),
        ],
        key=lambda item: item[1],
    )[0]
    return {
        "inputChargeRange": [charge_cutoff, None],
        "fixedChargeReduction": (
            "for each s, retain d_i(J_s) inside the complete convex "
            "common-slope sum and reduce all j>=J_s to x=0 or x=s/J_s"
        ),
        "zeroEndpointUniformBound": r037.rational_record(
            zero_endpoint_uniform
        ),
        "latticeParity": {
            "even": "s even => J_s=s/2 and x=s/J_s=2",
            "odd": "s odd => J_s=(s+3)/2 and x=s/J_s=2s/(s+3)",
        },
        "evenEndpoint": {
            "variable": "y=1/s",
            "interval": "0<=y<=1/242",
            "valueAtS242": r037.rational_record(even_at_242),
            "valueAtInfinity": r037.rational_record(even_limit),
            "derivativeCertificate": even_derivative,
            "conclusion": (
                "E_even'(y)>0, so every even s>=242 is bounded by s=242"
            ),
        },
        "oddEndpoint": {
            "variable": "y=1/s",
            "interval": "0<=y<=1/241",
            "valueAtS241": r037.rational_record(odd_at_241),
            "valueAtInfinity": r037.rational_record(odd_limit),
            "derivativeCertificate": odd_derivative,
            "absoluteValueBranches": (
                "q=2i gives 6iy/(1+3y); every q<2i has "
                "(2i-q-3qy)/(1+3y)>0 because q<=2i-3<241<=s"
            ),
            "conclusion": (
                "E_odd'(y)<0, so every odd s>=241 is bounded by its "
                "y=0 limit"
            ),
        },
        "maximumSource": maximum_source,
        "bound": r037.rational_record(maximum),
        "coefficientSignCancellationUsed": False,
        "tailDegreeGridUsedInProof": False,
        "largeChargeGridUsedInProof": False,
        "proof": (
            "the fixed-charge convex endpoint reduction covers every j; "
            "the exact parity formulas and Bernstein derivative signs cover "
            "the two infinite charge branches continuously"
        ),
        "classification": (
            "formal all-order charge-degree lattice theorem for every "
            "integer s>=241 and every admissible tail degree"
        ),
    }


def lattice_tail_bound(
    polynomial: Polynomial,
    radius: Rational,
    cutoff: int,
    charge_cutoff: int,
    zero_charge_weight: Rational,
) -> dict[str, object]:
    """Five exhaustive sectors with sharp positive-charge lattice bounds."""

    inherited = r046.two_block_tail_bound(
        polynomial,
        radius,
        cutoff,
        charge_cutoff,
        zero_charge_weight,
    )
    terms = r039.weighted_base_terms(polynomial, radius)
    fixed_records = fixed_positive_columns(terms, cutoff, charge_cutoff)
    fixed_maximum = max(
        fixed_records,
        key=lambda record: rational(record["bound"]["exact"]),
    )
    large = large_lattice_sector(terms, cutoff, charge_cutoff)
    candidates = [
        ("0", rational(inherited["zeroInputColumn"]["bound"]["exact"])),
        ("-1", rational(inherited["minusOneColumn"]["bound"]["exact"])),
        ("1", rational(inherited["plusOneColumn"]["bound"]["exact"])),
        (
            str(fixed_maximum["inputCharge"]),
            rational(fixed_maximum["bound"]["exact"]),
        ),
        (f">={charge_cutoff}", rational(large["bound"]["exact"])),
    ]
    maximum_sector, maximum_value = max(candidates, key=lambda item: item[1])
    return {
        "zeroChargeWeight": r037.rational_record(zero_charge_weight),
        "zeroInputColumn": inherited["zeroInputColumn"],
        "minusOneColumn": inherited["minusOneColumn"],
        "plusOneColumn": inherited["plusOneColumn"],
        "fixedPositiveChargeRange": [2, charge_cutoff - 1],
        "fixedPositiveChargeColumns": fixed_records,
        "fixedPositiveChargeMaximum": fixed_maximum,
        "largeChargeLatticeSector": large,
        "maximumBound": r037.rational_record(maximum_value),
        "maximumSector": maximum_sector,
        "r046Bound": inherited["maximumBound"],
        "r046MaximumSector": inherited["maximumSector"],
        "sectorDigestSha256": r041.digest_records(candidates),
        "proof": (
            "s=0, s=-1, s=1, 2<=s<S, and s>=S are disjoint and "
            "exhaustive; every sector record is all-order"
        ),
        "classification": (
            "formal all-order correlated two-block weighted-column theorem "
            "with exact charge-degree lattice endpoints"
        ),
        "_fixedByCharge": {
            record["inputCharge"]: record for record in fixed_records
        },
    }


def public_tail_record(tail: dict[str, object]) -> dict[str, object]:
    return {key: value for key, value in tail.items() if not key.startswith("_")}


def finite_column_regression(
    polynomial: Polynomial,
    radius: Rational,
    tail: dict[str, object],
    zero_charge_weight: Rational,
    charge_cutoff: int,
    charges: list[int],
    degree_offsets: list[int],
) -> dict[str, object]:
    """Finite exact implementation checks; not the all-order proof."""

    records = []
    digest_input = []
    fixed_by_charge = tail["_fixedByCharge"]
    for input_charge in charges:
        minimum_degree = r039.minimum_tail_degree(input_charge, 80)
        if input_charge == -1:
            sector = tail["minusOneColumn"]
        elif input_charge == 0:
            sector = tail["zeroInputColumn"]
        elif input_charge == 1:
            sector = tail["plusOneColumn"]
        elif input_charge < charge_cutoff:
            sector = fixed_by_charge[input_charge]
        else:
            sector = tail["largeChargeLatticeSector"]
        sector_bound = rational(sector["bound"]["exact"])
        for offset in degree_offsets:
            input_degree = minimum_degree + offset
            split = r046.split_exact_column(
                polynomial,
                radius,
                input_degree,
                input_charge,
                zero_charge_weight,
            )
            value = split["weightedRatio"]
            if value > sector_bound:
                raise AssertionError("finite column exceeded analytic sector")
            records.append(
                {
                    "inputCharge": input_charge,
                    "inputDegree": input_degree,
                    "exactWeightedColumn": r037.rational_record(value),
                    "allOrderSectorBound": r037.rational_record(sector_bound),
                    "belowSectorBound": True,
                }
            )
            digest_input.append((f"{input_charge}:{input_degree}", value))
    return {
        "charges": charges,
        "degreeOffsets": degree_offsets,
        "columnsChecked": len(records),
        "records": records,
        "allBelowSectorBounds": True,
        "exactColumnsSha256": r041.digest_records(digest_input),
        "classification": (
            "finite exact implementation regressions; all-order coverage "
            "comes from the fixed-charge convex endpoints and parity "
            "Bernstein sign certificates"
        ),
    }


def build_payload(
    maximum_degree: int,
    entry_radius: Rational,
    target_radius: Rational,
    failure_probe_radius: Rational,
    zero_charge_weight: Rational,
    charge_cutoff: int,
    regression_charges: list[int],
    regression_degree_offsets: list[int],
    ball_divisor: int,
    show_progress: bool,
    source_commit: str | None,
) -> dict[str, object]:
    started = time.perf_counter()
    progress(show_progress, started, "loading pinned R0.46 certificate")
    if sha256(R046_CERTIFICATE) != R046_EXPECTED_SHA256:
        raise AssertionError("R0.46 certificate hash mismatch")
    r046_certificate = json.loads(R046_CERTIFICATE.read_text(encoding="utf-8"))
    pinned_entry = rational(
        r046_certificate["restartCertificate"]["radius"]["exact"]
    )
    if entry_radius != pinned_entry:
        raise AssertionError("R0.47 entry radius must be the R0.46 target")
    if not entry_radius < target_radius < failure_probe_radius:
        raise AssertionError("R0.47 radii are not strictly ordered")
    if failure_probe_radius - target_radius != Rational(1, 1_000_000):
        raise AssertionError("R0.47 probe must be the adjacent millionth")
    if zero_charge_weight != Rational(3, 4):
        raise AssertionError("R0.47 keeps the R0.46 weight kappa=3/4")

    progress(
        show_progress,
        started,
        "constructing exact degree recurrence",
        maximumDegree=maximum_degree,
    )
    active, _, _, recurrence_interactions = r028.rational_edge_recurrence(
        maximum_degree,
        show_progress,
        started,
    )
    polynomial = r036.field_to_polynomial(active, maximum_degree)
    seed = {(1, 0): Rational(1), (0, 1): Rational(1)}
    progress(show_progress, started, "forming complete polynomial residual")
    residual = r036.add(
        polynomial,
        r036.scale(seed, -1),
        r036.scale(r036.phi(polynomial), -1),
    )
    if r036.truncate(residual, maximum_degree):
        raise AssertionError("degree recurrence has a residual below cutoff")
    residual_degrees = sorted({r039.degree(exponent) for exponent in residual})

    tails: dict[str, dict[str, object]] = {}
    restarts: dict[str, dict[str, object]] = {}
    for label, radius in (
        ("entry", entry_radius),
        ("target", target_radius),
        ("failureProbe", failure_probe_radius),
    ):
        progress(
            show_progress,
            started,
            "forming exact lattice tail and weighted restart",
            label=label,
            radius=str(radius),
        )
        tail = lattice_tail_bound(
            polynomial,
            radius,
            maximum_degree,
            charge_cutoff,
            zero_charge_weight,
        )
        tails[label] = tail
        restarts[label] = r046.block_restart_diagnostics(
            polynomial,
            residual,
            radius,
            tail,
            maximum_degree,
            ball_divisor,
            zero_charge_weight,
        )

    progress(show_progress, started, "checking finite exact columns")
    regression = finite_column_regression(
        polynomial,
        target_radius,
        tails["target"],
        zero_charge_weight,
        charge_cutoff,
        regression_charges,
        regression_degree_offsets,
    )

    entry = restarts["entry"]
    target = restarts["target"]
    failure = restarts["failureProbe"]
    target_tail = rational(target["tailLinearizationBound"]["exact"])
    failure_tail = rational(failure["tailLinearizationBound"]["exact"])
    target_old = rational(tails["target"]["r046Bound"]["exact"])
    target_fixed = tails["target"]["fixedPositiveChargeMaximum"]
    failure_fixed = tails["failureProbe"]["fixedPositiveChargeMaximum"]
    target_fixed_value = rational(target_fixed["bound"]["exact"])
    failure_fixed_value = rational(failure_fixed["bound"]["exact"])
    target_large = rational(
        tails["target"]["largeChargeLatticeSector"]["bound"]["exact"]
    )
    failure_large = rational(
        tails["failureProbe"]["largeChargeLatticeSector"]["bound"]["exact"]
    )
    target_exact_s162 = r046.split_exact_column(
        polynomial,
        target_radius,
        81,
        162,
        zero_charge_weight,
    )["weightedRatio"]
    failure_exact_s162 = r046.split_exact_column(
        polynomial,
        failure_probe_radius,
        81,
        162,
        zero_charge_weight,
    )["weightedRatio"]
    polynomial_digest = r037.polynomial_digest(polynomial)
    residual_digest = r037.polynomial_digest(residual)
    pinned_polynomial_digest = r046_certificate["restartCertificate"][
        "degreeEightyPolynomialSha256"
    ]
    pinned_residual_digest = r046_certificate["restartCertificate"][
        "exactResidualSha256"
    ]
    target_large_record = tails["target"]["largeChargeLatticeSector"]
    failure_large_record = tails["failureProbe"]["largeChargeLatticeSector"]

    checks = {
        "r046CertificateHashMatches": True,
        "r046TargetBecomesEntryRadius": entry_radius == pinned_entry,
        "zeroChargeWeightRemainsThreeQuarters": (
            zero_charge_weight == Rational(3, 4)
        ),
        "entryLatticeTailPasses": (
            rational(entry["tailLinearizationBound"]["exact"]) < 1
        ),
        "entryCanonicalFieldsPass": entry["canonicalFieldsPass"],
        "targetExtendsR046": target_radius > entry_radius,
        "targetR046SeparatedBoundFails": target_old > 1,
        "targetFixedPositiveMaximumIsS162": (
            target_fixed["inputCharge"] == 162
        ),
        "targetFixedPositiveEndpointIsMinimumDegree": (
            target_fixed["maximumEndpoint"] == "x=s/J_s"
            and target_fixed["minimumTailDegree"] == 81
        ),
        "targetFixedPositiveBoundIsExactS162Column": (
            target_fixed_value == target_exact_s162
        ),
        "targetFixedPositiveBoundPasses": target_fixed_value < 1,
        "targetLargeLatticeBoundPasses": target_large < 1,
        "targetLargeMaximumIsEvenS242": (
            target_large_record["maximumSource"] == "even s=242,j=121"
        ),
        "targetEvenBernsteinCertificatePasses": (
            target_large_record["evenEndpoint"]["derivativeCertificate"]
            ["allSignedBernsteinCoefficientsPositive"]
        ),
        "targetOddBernsteinCertificatePasses": (
            target_large_record["oddEndpoint"]["derivativeCertificate"]
            ["allSignedBernsteinCoefficientsPositive"]
        ),
        "targetWorstSectorIsS162": tails["target"]["maximumSector"] == "162",
        "targetTailPasses": target_tail < 1,
        "targetFixedPointPasses": target["fixedPointPasses"],
        "targetStretchPasses": target["stretchPasses"],
        "targetCanonicalFieldsPass": target["canonicalFieldsPass"],
        "targetDirectTransportStillFails": (
            rational(target["directTransportBound"]["exact"]) > 1
        ),
        "failureProbeIsAdjacentMillionth": (
            failure_probe_radius - target_radius
            == Rational(1, 1_000_000)
        ),
        "failureProbeLargeLatticeBoundStillPasses": failure_large < 1,
        "failureProbeEvenBernsteinCertificatePasses": (
            failure_large_record["evenEndpoint"]["derivativeCertificate"]
            ["allSignedBernsteinCoefficientsPositive"]
        ),
        "failureProbeOddBernsteinCertificatePasses": (
            failure_large_record["oddEndpoint"]["derivativeCertificate"]
            ["allSignedBernsteinCoefficientsPositive"]
        ),
        "failureProbeFixedPositiveMaximumIsS162": (
            failure_fixed["inputCharge"] == 162
        ),
        "failureProbeBoundIsExactS162Column": (
            failure_fixed_value == failure_exact_s162
        ),
        "failureProbeExactS162ColumnFails": failure_exact_s162 > 1,
        "failureProbeWorstSectorIsS162": (
            tails["failureProbe"]["maximumSector"] == "162"
        ),
        "failureProbeTailFails": failure_tail > 1,
        "failureProbeFixedPointFails": not failure["fixedPointPasses"],
        "failureProbePolynomialStretchStillPasses": (
            rational(
                failure["stretchOperator"]["maximumPolynomialBound"]["exact"]
            )
            < 1
        ),
        "all239FixedPositiveChargesCovered": (
            len(tails["target"]["fixedPositiveChargeColumns"]) == 239
        ),
        "finiteRegressionsBelowAnalyticSectors": regression[
            "allBelowSectorBounds"
        ],
        "polynomialDigestMatchesR046": polynomial_digest == pinned_polynomial_digest,
        "residualDigestMatchesR046": residual_digest == pinned_residual_digest,
        "residualStartsAboveCutoff": residual_degrees[0] == maximum_degree + 1,
        "residualEndsAtDoubleCutoff": residual_degrees[-1] == 2 * maximum_degree,
        "chargeCutoffExceedsAllCenterCharges": charge_cutoff > 2 * maximum_degree,
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise AssertionError(f"R0.47 checks failed: {failed}")

    elapsed = time.perf_counter() - started
    progress(
        show_progress,
        started,
        "all exact checks passed",
        checks=len(checks),
        targetRadius=str(target_radius),
        targetTail=target["tailLinearizationBound"]["exact"],
        failureRadius=str(failure_probe_radius),
        failureTail=failure["tailLinearizationBound"]["exact"],
    )
    return {
        "scope": {
            "system": "reduced canonical edge generating system",
            "claim": (
                "all-order charge-degree lattice endpoint theorem and exact "
                "two-block common-radius restart at 94233/250000"
            ),
            "notClaimed": [
                "three-dimensional Navier-Stokes global regularity",
                "finite-time blow-up",
                "a singularity at the failed probe",
                "failure of every possible norm or nonlinear construction",
                "an all-order theorem from the finite regression columns",
                "the true analytic radius of the reduced system",
            ],
        },
        "git": r039.git_state(source_commit),
        "input": {
            "r046": {
                "path": str(R046_CERTIFICATE),
                "sha256": R046_EXPECTED_SHA256,
                "sourceCommit": r046_certificate["git"]["commit"],
            }
        },
        "latticeTheorem": {
            "norm": (
                "||f||_(r,kappa)=kappa||P_0 f||_(B_r)+"
                "||P_nonzero f||_(B_r), kappa=3/4"
            ),
            "fixedPositiveCharges": (
                "for each 2<=s<241, retain d_i(J_s) inside the complete "
                "convex common-slope sum and check its two exact endpoints"
            ),
            "largePositiveCharges": (
                "for s>=241, use the exact even/odd formulas for J_s and "
                "certify the two continuous y=1/s derivative signs by "
                "strict Bernstein coefficients"
            ),
            "finiteChargeEnumerationUsed": True,
            "finiteChargeEnumerationScope": "the finite theorem list 2<=s<241",
            "tailDegreeGridUsedInProof": False,
            "largeChargeGridUsedInProof": False,
            "coefficientSignCancellationUsed": False,
            "floatingPointThresholdDecisionUsed": False,
            "classification": "formal all-order charge-degree lattice theorem",
        },
        "entryControl": {
            **entry,
            "tail": public_tail_record(tails["entry"]),
            "statement": "the R0.46 certified radius remains a strict pass",
        },
        "restartCertificate": {
            **target,
            "entryRadius": r037.rational_record(entry_radius),
            "radiusGainFromR046": r037.rational_record(
                target_radius / entry_radius
            ),
            "cubicFixedChargeGainFromR046": r037.rational_record(
                (target_radius / entry_radius) ** 3
            ),
            "polynomialCutoff": maximum_degree,
            "chargeCutoff": charge_cutoff,
            "tail": public_tail_record(tails["target"]),
            "degreeEightyPolynomialTerms": len(polynomial),
            "degreeEightyPolynomialSha256": polynomial_digest,
            "exactResidualTerms": len(residual),
            "exactResidualSha256": residual_digest,
            "residualDegreeRange": [residual_degrees[0], residual_degrees[-1]],
            "statement": (
                "the lattice-sharp two-block Banach restart and inherited "
                "canonical-stretch construction certify a, phi, U, and V "
                "at radius 94233/250000"
            ),
        },
        "negativeControl": {
            **failure,
            "tail": public_tail_record(tails["failureProbe"]),
            "exactFailingColumn": {
                "inputCharge": 162,
                "inputDegree": 81,
                "value": r037.rational_record(failure_exact_s162),
            },
            "classification": (
                "the adjacent millionth fails in the true j=81,s=162 "
                "induced column of this specific two-block weighted-l1 norm; "
                "this is not a singularity theorem or a failure result for "
                "other norms or nonlinear existence methods"
            ),
        },
        "finiteRegression": {
            "weightedColumns": regression,
            "recurrenceMaximumDegree": maximum_degree,
            "recurrenceOrderedInteractions": recurrence_interactions,
        },
        "checks": checks,
        "computation": {
            "exactBackend": "gmpy2.mpq (GMP rational arithmetic)",
            "decimalDecisionUse": False,
            "randomness": False,
            "wallSeconds": elapsed,
            "python": platform.python_version(),
            "platform": platform.platform(),
            "createdUtc": datetime.now(timezone.utc).isoformat(),
        },
    }


def parse_int_list(value: str) -> list[int]:
    try:
        items = [int(item.strip()) for item in value.split(",") if item.strip()]
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from error
    if not items:
        raise argparse.ArgumentTypeError("at least one integer is required")
    return items


def main() -> None:
    global PROGRESS_LOG
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-total-degree", type=int, default=80)
    parser.add_argument("--entry-radius", default="376/1000")
    parser.add_argument("--target-radius", default="376932/1000000")
    parser.add_argument("--failure-probe-radius", default="376933/1000000")
    parser.add_argument("--zero-charge-weight", default="3/4")
    parser.add_argument("--charge-cutoff", type=int, default=241)
    parser.add_argument(
        "--regression-charges",
        type=parse_int_list,
        default=parse_int_list("-1,0,1,2,162,164,240,241,242,300"),
    )
    parser.add_argument(
        "--regression-degree-offsets",
        type=parse_int_list,
        default=parse_int_list("0,3,18"),
    )
    parser.add_argument("--ball-divisor", type=int, default=1_000_000)
    parser.add_argument("--source-commit")
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--progress-log", type=Path)
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    if arguments.max_total_degree != 80:
        raise SystemExit("R0.47 is pinned to --max-total-degree 80")
    if arguments.charge_cutoff != 241:
        raise SystemExit("R0.47 is pinned to --charge-cutoff 241")
    if arguments.ball_divisor <= 32:
        raise SystemExit("--ball-divisor must exceed 32")
    if any(item % 3 for item in arguments.regression_degree_offsets):
        raise SystemExit("degree offsets must be multiples of 3")

    entry_radius = rational(arguments.entry_radius)
    target_radius = rational(arguments.target_radius)
    failure_probe_radius = rational(arguments.failure_probe_radius)
    zero_charge_weight = rational(arguments.zero_charge_weight)

    PROGRESS_LOG = arguments.progress_log
    if PROGRESS_LOG is not None:
        PROGRESS_LOG.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_LOG.write_text("", encoding="utf-8")

    payload = build_payload(
        arguments.max_total_degree,
        entry_radius,
        target_radius,
        failure_probe_radius,
        zero_charge_weight,
        arguments.charge_cutoff,
        arguments.regression_charges,
        arguments.regression_degree_offsets,
        arguments.ball_divisor,
        arguments.progress,
        arguments.source_commit,
    )
    if arguments.check and not all(payload["checks"].values()):
        raise SystemExit("R0.47 checks failed")
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
