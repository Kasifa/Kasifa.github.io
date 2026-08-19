#!/usr/bin/env python3
"""R0.48 exact threshold-root audit for the charge-degree lattice norm.

R0.47 isolates the same true minimum-degree input column, with charge s=162
and degree j=81, at both ends of an adjacent millionth window.  This audit
promotes those endpoint data to an exact full-window dominance statement and
a sharp-threshold theorem for the current norm.

The active column is a finite polynomial

    A(r) = sum_i alpha_i r^i

with 80 strictly positive nonconstant coefficients.  The threshold
polynomial P(r)=A(r)-1 therefore has P(0)=-1 and P'(r)>0 for every r>0.
An exact Sturm sequence independently counts one root in the isolated
interval

    0.376932499290527340 < r_* < 0.376932499290527341.

No floating-point value is used for a sign decision.

The remaining sectors are controlled on the full window
[0.376932,0.376933] by a monotone sandwich.  Every exact column is a
nonnegative sum of powers of r.  Hence each competing column at any radius
in the window is bounded by the pinned R0.47 all-order certificate at the
right endpoint, while the active column is bounded below by its exact value
at the left endpoint.  All 238 other fixed positive charges, the inactive
endpoint of charge 162, and the four other exhaustive charge sectors remain
strictly below the active column on the entire window.

This is a sharp threshold theorem for one reduced generating system and one
specific induced norm.  It is not a singularity theorem, a proof of
three-dimensional Navier-Stokes regularity, or a statement about every norm
or nonlinear construction.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import time

import gmpy2

import edge_charge_degree_lattice_audit as r047
import edge_charge_resolved_audit as r039
import edge_rational_asymptotic_audit as r028
import edge_short_continuation_audit as r036
import edge_weighted_restart_audit as r037


Rational = gmpy2.mpq
Integer = gmpy2.mpz
Polynomial = dict[tuple[int, int], Rational]
Poly = list[Rational]

R047_CERTIFICATE = Path(
    "research/certificates/r047/edge-charge-degree-lattice.json"
)
R047_EXPECTED_SHA256 = (
    "e45bc20ddeab9efde83dafefc84514df0260f8831c102c4621f0fdcd43dea6c9"
)
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(
            f"[R0.48 +{elapsed:8.2f}s] {stage}{suffix}",
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


def coefficient_digest(coefficients: list[int | Rational]) -> str:
    serialized = "".join(
        f"{index}:{coefficient}\n"
        for index, coefficient in enumerate(coefficients)
    )
    return hashlib.sha256(serialized.encode("ascii")).hexdigest()


def add_coefficient(poly: Poly, degree: int, coefficient: Rational) -> None:
    poly[degree] += coefficient


def independent_terms(
    polynomial: Polynomial,
) -> list[tuple[int, int, Rational]]:
    return [
        (
            r039.degree(exponent),
            r039.charge(exponent),
            abs(coefficient),
        )
        for exponent, coefficient in polynomial.items()
    ]


def exact_column_polynomial(
    terms: list[tuple[int, int, Rational]],
    maximum_degree: int,
    input_degree: int,
    input_charge: int,
    zero_charge_weight: Rational,
) -> Poly:
    """Coefficient polynomial of one exact weighted induced column."""

    result = [Rational(0)] * (maximum_degree + 1)
    input_weight = (
        zero_charge_weight if input_charge == 0 else Rational(1)
    )
    for degree, charge, coefficient in terms:
        output_weight = (
            zero_charge_weight
            if charge + input_charge == 0
            else Rational(1)
        )
        factor = (
            Rational(degree + input_degree, input_degree)
            * abs(
                r039.monomial_derivative_coefficient(
                    degree,
                    charge,
                    input_degree,
                    input_charge,
                )
            )
            * output_weight
            / input_weight
        )
        add_coefficient(result, degree, coefficient * factor)
    return r047.trim(result)


def fixed_charge_endpoint_polynomials(
    terms: list[tuple[int, int, Rational]],
    maximum_degree: int,
    input_charge: int,
) -> tuple[Poly, Poly, int]:
    """The two exact convex endpoints for one fixed positive charge."""

    minimum_degree = r039.minimum_tail_degree(input_charge, maximum_degree)
    maximum_slope = Rational(input_charge, minimum_degree)
    infinity_endpoint = [Rational(0)] * (maximum_degree + 1)
    minimum_endpoint = [Rational(0)] * (maximum_degree + 1)
    for degree, charge, coefficient in terms:
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
        common = coefficient * degree_factor * charge_factor
        add_coefficient(
            infinity_endpoint,
            degree,
            common * abs(charge),
        )
        add_coefficient(
            minimum_endpoint,
            degree,
            common * abs(degree * maximum_slope - charge),
        )
    return (
        r047.trim(infinity_endpoint),
        r047.trim(minimum_endpoint),
        minimum_degree,
    )


def zero_sector_polynomial(
    terms: list[tuple[int, int, Rational]],
    maximum_degree: int,
    zero_charge_weight: Rational,
) -> Poly:
    minimum_degree = r039.minimum_tail_degree(0, maximum_degree)
    result = [Rational(0)] * (maximum_degree + 1)
    for degree, charge, coefficient in terms:
        if charge == 0:
            continue
        factor = (
            Rational(
                degree + minimum_degree,
                degree + minimum_degree - 1,
            )
            * abs(charge)
            / (3 * zero_charge_weight)
        )
        add_coefficient(result, degree, coefficient * factor)
    return r047.trim(result)


def plus_one_sector_polynomial(
    terms: list[tuple[int, int, Rational]],
    maximum_degree: int,
    zero_charge_weight: Rational,
) -> Poly:
    minimum_degree = r039.minimum_tail_degree(1, maximum_degree)
    result = [Rational(0)] * (maximum_degree + 1)
    for degree, charge, coefficient in terms:
        output_weight = zero_charge_weight if charge == -1 else Rational(1)
        factor = (
            r039.finite_charge_factor(
                degree,
                charge,
                1,
                minimum_degree,
            )
            * output_weight
        )
        add_coefficient(result, degree, coefficient * factor)
    return r047.trim(result)


def threshold_polynomial(active_column: Poly) -> Poly:
    result = active_column[:]
    result[0] -= 1
    return r047.trim(result)


def primitive_integer_polynomial(poly: Poly) -> list[Integer]:
    common_denominator = Integer(1)
    for coefficient in poly:
        common_denominator = gmpy2.lcm(
            common_denominator,
            coefficient.denominator,
        )
    integers = [
        Integer(coefficient * common_denominator)
        for coefficient in poly
    ]
    content = Integer(0)
    for coefficient in integers:
        content = gmpy2.gcd(content, abs(coefficient))
    if content == 0:
        raise AssertionError("zero polynomial has no primitive normalization")
    integers = [coefficient // content for coefficient in integers]
    if integers[-1] < 0:
        integers = [-coefficient for coefficient in integers]
    return integers


def polynomial_divmod(dividend: Poly, divisor: Poly) -> tuple[Poly, Poly]:
    """Exact Euclidean division over Q."""

    dividend = r047.trim(dividend)
    divisor = r047.trim(divisor)
    if len(divisor) == 1 and divisor[0] == 0:
        raise ZeroDivisionError("polynomial division by zero")
    quotient = [Rational(0)] * max(1, len(dividend) - len(divisor) + 1)
    while len(dividend) >= len(divisor) and not (
        len(dividend) == 1 and dividend[0] == 0
    ):
        shift = len(dividend) - len(divisor)
        factor = dividend[-1] / divisor[-1]
        quotient[shift] += factor
        for index, coefficient in enumerate(divisor):
            dividend[index + shift] -= factor * coefficient
        dividend = r047.trim(dividend)
    return r047.trim(quotient), r047.trim(dividend)


def normalize_sturm_polynomial(poly: Poly) -> Poly:
    """Scale by a positive constant so the leading coefficient is +/-1."""

    poly = r047.trim(poly)
    if len(poly) == 1 and poly[0] == 0:
        raise AssertionError("zero polynomial in Sturm sequence")
    scale = abs(poly[-1])
    return [coefficient / scale for coefficient in poly]


def sturm_sequence(poly: Poly) -> list[Poly]:
    sequence = [
        normalize_sturm_polynomial(poly),
        normalize_sturm_polynomial(r047.poly_derivative(poly)),
    ]
    while len(sequence[-1]) > 1:
        _quotient, remainder = polynomial_divmod(
            sequence[-2],
            sequence[-1],
        )
        if len(remainder) == 1 and remainder[0] == 0:
            raise AssertionError("threshold polynomial is not square-free")
        sequence.append(
            normalize_sturm_polynomial(
                [-coefficient for coefficient in remainder]
            )
        )
    return sequence


def exact_sign(value: Rational) -> int:
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


def sturm_endpoint_record(
    sequence: list[Poly],
    value: Rational,
) -> dict[str, object]:
    signs = [
        exact_sign(r047.poly_evaluate(poly, value))
        for poly in sequence
    ]
    nonzero = [sign for sign in signs if sign]
    variations = sum(
        left != right for left, right in zip(nonzero, nonzero[1:])
    )
    return {
        "value": r037.rational_record(value),
        "signs": "".join("+" if sign > 0 else "-" if sign < 0 else "0" for sign in signs),
        "zeroValues": signs.count(0),
        "variations": variations,
    }


def decimal_root_isolation(
    poly: Poly,
    window_lower: Rational,
    window_upper: Rational,
    decimal_digits: int,
) -> tuple[Rational, Rational, int]:
    """Return adjacent decimal rationals bracketing the unique root."""

    scale = Integer(10) ** decimal_digits
    scaled_lower = window_lower * scale
    scaled_upper = window_upper * scale
    if scaled_lower.denominator != 1 or scaled_upper.denominator != 1:
        raise AssertionError("decimal scale does not contain the root window")
    lower_integer = Integer(scaled_lower)
    upper_integer = Integer(scaled_upper)
    if r047.poly_evaluate(poly, window_lower) >= 0:
        raise AssertionError("root window lower endpoint is not negative")
    if r047.poly_evaluate(poly, window_upper) <= 0:
        raise AssertionError("root window upper endpoint is not positive")
    decisions = 0
    while upper_integer - lower_integer > 1:
        midpoint_integer = (lower_integer + upper_integer) // 2
        midpoint = Rational(midpoint_integer, scale)
        sign = exact_sign(r047.poly_evaluate(poly, midpoint))
        if sign == 0:
            raise AssertionError("threshold root unexpectedly rational at scale")
        if sign < 0:
            lower_integer = midpoint_integer
        else:
            upper_integer = midpoint_integer
        decisions += 1
    return (
        Rational(lower_integer, scale),
        Rational(upper_integer, scale),
        decisions,
    )


def all_nonnegative(poly: Poly) -> bool:
    return all(coefficient >= 0 for coefficient in poly)


def terminating_decimal(value: Rational, decimal_places: int) -> str:
    """Render an exactly terminating rational without binary floating point."""

    sign = "-" if value < 0 else ""
    numerator = abs(value.numerator)
    denominator = value.denominator
    integer_part, remainder = divmod(numerator, denominator)
    digits: list[str] = []
    for _ in range(decimal_places):
        remainder *= 10
        digit, remainder = divmod(remainder, denominator)
        digits.append(str(digit))
    if remainder != 0:
        raise AssertionError(
            "requested decimal precision does not terminate the rational"
        )
    return f"{sign}{integer_part}." + "".join(digits)


def build_payload(
    maximum_degree: int,
    window_lower: Rational,
    window_upper: Rational,
    root_decimal_digits: int,
    zero_charge_weight: Rational,
    charge_cutoff: int,
    show_progress: bool,
    source_commit: str | None,
) -> dict[str, object]:
    started = time.perf_counter()
    progress(show_progress, started, "loading pinned R0.47 certificate")
    if sha256(R047_CERTIFICATE) != R047_EXPECTED_SHA256:
        raise AssertionError("R0.47 certificate hash mismatch")
    r047_certificate = json.loads(R047_CERTIFICATE.read_text(encoding="utf-8"))
    pinned_target = rational(
        r047_certificate["restartCertificate"]["radius"]["exact"]
    )
    pinned_probe = rational(
        r047_certificate["negativeControl"]["radius"]["exact"]
    )
    if window_lower != pinned_target or window_upper != pinned_probe:
        raise AssertionError("R0.48 window must equal the R0.47 adjacent millionth")
    if window_upper - window_lower != Rational(1, 1_000_000):
        raise AssertionError("R0.48 window width must be one millionth")
    if zero_charge_weight != Rational(3, 4):
        raise AssertionError("R0.48 keeps kappa=3/4")
    if maximum_degree != 80 or charge_cutoff != 241:
        raise AssertionError("R0.48 is pinned to N=80 and S=241")

    progress(
        show_progress,
        started,
        "constructing exact degree recurrence",
        maximumDegree=maximum_degree,
    )
    active_field, _, _, recurrence_interactions = (
        r028.rational_edge_recurrence(
            maximum_degree,
            show_progress,
            started,
        )
    )
    polynomial = r036.field_to_polynomial(active_field, maximum_degree)
    polynomial_digest = r037.polynomial_digest(polynomial)
    pinned_polynomial_digest = r047_certificate["restartCertificate"][
        "degreeEightyPolynomialSha256"
    ]
    if polynomial_digest != pinned_polynomial_digest:
        raise AssertionError("degree-80 polynomial digest changed")
    terms = independent_terms(polynomial)

    progress(show_progress, started, "forming active threshold polynomial")
    active_column = exact_column_polynomial(
        terms,
        maximum_degree,
        81,
        162,
        zero_charge_weight,
    )
    fixed_infinity, fixed_minimum, minimum_degree = (
        fixed_charge_endpoint_polynomials(
            terms,
            maximum_degree,
            162,
        )
    )
    if minimum_degree != 81 or active_column != fixed_minimum:
        raise AssertionError("active exact column and convex endpoint disagree")
    threshold = threshold_polynomial(active_column)
    primitive = primitive_integer_polynomial(threshold)
    derivative = r047.poly_derivative(threshold)
    if threshold[0] != -1:
        raise AssertionError("threshold polynomial must have constant -1")
    if not all(coefficient > 0 for coefficient in threshold[1:]):
        raise AssertionError("active column lost strict positive coefficients")
    if not all(coefficient > 0 for coefficient in derivative):
        raise AssertionError("threshold derivative is not coefficient-positive")

    target_active_value = r047.poly_evaluate(active_column, window_lower)
    probe_active_value = r047.poly_evaluate(active_column, window_upper)
    pinned_target_active = rational(
        r047_certificate["restartCertificate"]["tail"]
        ["fixedPositiveChargeMaximum"]["bound"]["exact"]
    )
    pinned_probe_active = rational(
        r047_certificate["negativeControl"]["tail"]
        ["fixedPositiveChargeMaximum"]["bound"]["exact"]
    )
    if target_active_value != pinned_target_active:
        raise AssertionError("active target value disagrees with R0.47")
    if probe_active_value != pinned_probe_active:
        raise AssertionError("active probe value disagrees with R0.47")

    progress(
        show_progress,
        started,
        "isolating decimal root",
        decimalDigits=root_decimal_digits,
    )
    root_lower, root_upper, bisection_decisions = decimal_root_isolation(
        threshold,
        window_lower,
        window_upper,
        root_decimal_digits,
    )
    lower_sign_value = r047.poly_evaluate(threshold, root_lower)
    upper_sign_value = r047.poly_evaluate(threshold, root_upper)

    progress(show_progress, started, "building exact Sturm sequence")
    sturm = sturm_sequence(threshold)
    sturm_lower = sturm_endpoint_record(sturm, root_lower)
    sturm_upper = sturm_endpoint_record(sturm, root_upper)
    sturm_root_count = (
        sturm_lower["variations"] - sturm_upper["variations"]
    )
    sturm_degrees = [len(poly) - 1 for poly in sturm]
    sturm_digests = [r047.polynomial_digest(poly) for poly in sturm]

    progress(show_progress, started, "certifying full-window dominance")
    pinned_probe_tail = r047_certificate["negativeControl"]["tail"]
    fixed_records = pinned_probe_tail["fixedPositiveChargeColumns"]
    fixed_by_charge = {
        record["inputCharge"]: record for record in fixed_records
    }
    if len(fixed_by_charge) != 239:
        raise AssertionError("R0.47 fixed-charge theorem list is incomplete")

    competitor_records: list[dict[str, object]] = []
    for input_charge in range(2, charge_cutoff):
        infinity, minimum, degree_floor = fixed_charge_endpoint_polynomials(
            terms,
            maximum_degree,
            input_charge,
        )
        if not all_nonnegative(infinity) or not all_nonnegative(minimum):
            raise AssertionError("fixed-charge endpoint lost coefficient positivity")
        infinity_at_probe = r047.poly_evaluate(infinity, window_upper)
        minimum_at_probe = r047.poly_evaluate(minimum, window_upper)
        record = fixed_by_charge[input_charge]
        pinned_bound = rational(record["bound"]["exact"])
        if max(infinity_at_probe, minimum_at_probe) != pinned_bound:
            raise AssertionError(
                f"fixed-charge probe mismatch at s={input_charge}"
            )
        if input_charge == 162:
            if minimum_at_probe != probe_active_value:
                raise AssertionError("active endpoint mismatch at probe")
            candidates = [
                (
                    "fixed s=162 inactive x=0 endpoint",
                    infinity_at_probe,
                    infinity,
                    "x=0",
                )
            ]
        else:
            endpoint_name = (
                "x=0"
                if infinity_at_probe >= minimum_at_probe
                else "x=s/J_s"
            )
            endpoint_poly = (
                infinity
                if infinity_at_probe >= minimum_at_probe
                else minimum
            )
            candidates = [
                (
                    f"fixed s={input_charge}",
                    pinned_bound,
                    endpoint_poly,
                    endpoint_name,
                )
            ]
        for label, upper_bound, endpoint_poly, endpoint_name in candidates:
            gap = target_active_value - upper_bound
            competitor_records.append(
                {
                    "label": label,
                    "sector": "fixed positive charge",
                    "inputCharge": input_charge,
                    "minimumTailDegree": degree_floor,
                    "endpoint": endpoint_name,
                    "upperBoundAtWindowRight": r037.rational_record(
                        upper_bound
                    ),
                    "gapBelowActiveAtWindowLeft": r037.rational_record(gap),
                    "coefficientCount": len(endpoint_poly),
                    "allCoefficientsNonnegative": True,
                    "coefficientSha256": r047.polynomial_digest(endpoint_poly),
                }
            )

    zero_poly = zero_sector_polynomial(
        terms,
        maximum_degree,
        zero_charge_weight,
    )
    minus_poly = exact_column_polynomial(
        terms,
        maximum_degree,
        82,
        -1,
        zero_charge_weight,
    )
    plus_poly = plus_one_sector_polynomial(
        terms,
        maximum_degree,
        zero_charge_weight,
    )
    sector_polynomials = [
        ("s=0", "zeroInputColumn", zero_poly),
        ("s=-1", "minusOneColumn", minus_poly),
        ("s=1", "plusOneColumn", plus_poly),
    ]
    for label, certificate_key, sector_poly in sector_polynomials:
        if not all_nonnegative(sector_poly):
            raise AssertionError(f"{label} sector lost coefficient positivity")
        upper_bound = r047.poly_evaluate(sector_poly, window_upper)
        pinned_bound = rational(
            pinned_probe_tail[certificate_key]["bound"]["exact"]
        )
        if upper_bound != pinned_bound:
            raise AssertionError(f"{label} probe value disagrees with R0.47")
        competitor_records.append(
            {
                "label": label,
                "sector": label,
                "upperBoundAtWindowRight": r037.rational_record(upper_bound),
                "gapBelowActiveAtWindowLeft": r037.rational_record(
                    target_active_value - upper_bound
                ),
                "coefficientCount": len(sector_poly),
                "allCoefficientsNonnegative": True,
                "coefficientSha256": r047.polynomial_digest(sector_poly),
            }
        )

    large_upper = rational(
        pinned_probe_tail["largeChargeLatticeSector"]["bound"]["exact"]
    )
    competitor_records.append(
        {
            "label": f"s>={charge_cutoff}",
            "sector": "large positive charge",
            "upperBoundAtWindowRight": r037.rational_record(large_upper),
            "gapBelowActiveAtWindowLeft": r037.rational_record(
                target_active_value - large_upper
            ),
            "allExactColumnsMonotoneInRadius": True,
            "rightEndpointAllOrderCertificate": {
                "source": "R0.47 negative-control large-charge lattice sector",
                "evenDerivativeCertificatePasses": (
                    pinned_probe_tail["largeChargeLatticeSector"]
                    ["evenEndpoint"]["derivativeCertificate"]
                    ["allSignedBernsteinCoefficientsPositive"]
                ),
                "oddDerivativeCertificatePasses": (
                    pinned_probe_tail["largeChargeLatticeSector"]
                    ["oddEndpoint"]["derivativeCertificate"]
                    ["allSignedBernsteinCoefficientsPositive"]
                ),
            },
        }
    )

    competitor_values = [
        (
            record["label"],
            rational(record["upperBoundAtWindowRight"]["exact"]),
        )
        for record in competitor_records
    ]
    competitor_label, competitor_maximum = max(
        competitor_values,
        key=lambda item: item[1],
    )
    minimum_dominance_gap = target_active_value - competitor_maximum
    dominance_digest = r039.digest_records(competitor_values)

    checks = {
        "r047CertificateHashMatches": True,
        "windowMatchesR047AdjacentMillionth": (
            window_lower == pinned_target and window_upper == pinned_probe
        ),
        "zeroChargeWeightRemainsThreeQuarters": (
            zero_charge_weight == Rational(3, 4)
        ),
        "polynomialDigestMatchesR047": (
            polynomial_digest == pinned_polynomial_digest
        ),
        "activeColumnIsExactS162J81": (
            active_column == fixed_minimum and minimum_degree == 81
        ),
        "targetValueMatchesR047": (
            target_active_value == pinned_target_active
        ),
        "probeValueMatchesR047": (
            probe_active_value == pinned_probe_active
        ),
        "thresholdConstantIsMinusOne": threshold[0] == -1,
        "allEightyNonconstantCoefficientsPositive": (
            len(threshold) == 81
            and all(coefficient > 0 for coefficient in threshold[1:])
        ),
        "derivativePositiveOnPositiveAxis": (
            all(coefficient > 0 for coefficient in derivative)
        ),
        "windowLowerIsStrictPass": (
            r047.poly_evaluate(threshold, window_lower) < 0
        ),
        "windowUpperIsStrictFail": (
            r047.poly_evaluate(threshold, window_upper) > 0
        ),
        "isolatedLowerSignNegative": lower_sign_value < 0,
        "isolatedUpperSignPositive": upper_sign_value > 0,
        "isolatedWidthIsOneDecimalUnit": (
            root_upper - root_lower
            == Rational(1, Integer(10) ** root_decimal_digits)
        ),
        "sturmDegreesDescendToZero": (
            sturm_degrees == list(range(80, -1, -1))
        ),
        "sturmEndpointsAreNotRoots": (
            sturm_lower["zeroValues"] == 0
            and sturm_upper["zeroValues"] == 0
        ),
        "sturmCountsExactlyOneRoot": sturm_root_count == 1,
        "allTwoHundredFortyThreeCompetitorsCovered": (
            len(competitor_records) == 243
        ),
        "allCompetitorsBelowActiveAcrossWindow": (
            minimum_dominance_gap > 0
            and all(
                rational(record["gapBelowActiveAtWindowLeft"]["exact"]) > 0
                for record in competitor_records
            )
        ),
        "nearestCompetitorIsS164": competitor_label == "fixed s=164",
        "largeChargeProbeCertificatePasses": (
            competitor_records[-1]["rightEndpointAllOrderCertificate"]
            ["evenDerivativeCertificatePasses"]
            and competitor_records[-1]["rightEndpointAllOrderCertificate"]
            ["oddDerivativeCertificatePasses"]
        ),
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise AssertionError(f"R0.48 checks failed: {failed}")

    elapsed = time.perf_counter() - started
    progress(
        show_progress,
        started,
        "all exact checks passed",
        checks=len(checks),
        rootLower=str(root_lower),
        rootUpper=str(root_upper),
        sturmRoots=sturm_root_count,
        competitors=len(competitor_records),
        nearestCompetitor=competitor_label,
    )
    return {
        "scope": {
            "system": "reduced canonical edge generating system",
            "norm": (
                "||f||_(r,kappa)=kappa||P_0 f||_(B_r)+"
                "||P_nonzero f||_(B_r), kappa=3/4"
            ),
            "claim": (
                "exact sharp threshold root for the induced two-block "
                "weighted-l1 tail linearization norm on the adjacent "
                "millionth window"
            ),
            "notClaimed": [
                "three-dimensional Navier-Stokes global regularity",
                "finite-time blow-up",
                "a PDE singularity at the norm threshold",
                "failure of analytic continuation",
                "failure of every equivalent or anisotropic norm",
                "a fixed-point construction at the threshold itself",
                "irreducibility of the degree-80 threshold polynomial",
            ],
        },
        "git": r039.git_state(source_commit),
        "input": {
            "r047": {
                "path": str(R047_CERTIFICATE),
                "sha256": R047_EXPECTED_SHA256,
                "sourceCommit": r047_certificate["git"]["commit"],
            }
        },
        "thresholdTheorem": {
            "window": {
                "lower": r037.rational_record(window_lower),
                "upper": r037.rational_record(window_upper),
                "width": r037.rational_record(window_upper - window_lower),
            },
            "activeColumn": {
                "inputCharge": 162,
                "inputDegree": 81,
                "isTrueInducedColumn": True,
                "coefficientCount": len(active_column),
                "allCoefficientsNonnegative": all_nonnegative(active_column),
                "allNonconstantCoefficientsPositive": True,
                "coefficientSha256": r047.polynomial_digest(active_column),
                "valueAtWindowLower": r037.rational_record(
                    target_active_value
                ),
                "valueAtWindowUpper": r037.rational_record(
                    probe_active_value
                ),
            },
            "polynomial": {
                "definition": "P(r)=C_r(81,162)-1",
                "degree": len(threshold) - 1,
                "rationalCoefficientSha256": r047.polynomial_digest(
                    threshold
                ),
                "primitiveIntegerCoefficientSha256": coefficient_digest(
                    primitive
                ),
                "primitiveIntegerCoefficientsAscending": [
                    str(coefficient) for coefficient in primitive
                ],
                "primitiveCoefficientCount": len(primitive),
                "primitiveMaximumCoefficientDigits": max(
                    len(str(abs(coefficient))) for coefficient in primitive
                ),
                "constantSign": "-",
                "positiveNonconstantCoefficientCount": len(threshold) - 1,
                "derivativePositiveForEveryPositiveRadius": True,
                "positiveRootIsGloballyUnique": True,
            },
            "rootIsolation": {
                "lower": r037.rational_record(root_lower),
                "upper": r037.rational_record(root_upper),
                "width": r037.rational_record(root_upper - root_lower),
                "display": (
                    "0.376932499290527340 < r_* < "
                    "0.376932499290527341"
                ),
                "midpointDisplayOnly": terminating_decimal(
                    (root_lower + root_upper) / 2,
                    root_decimal_digits + 1,
                ),
                "decimalDigits": root_decimal_digits,
                "exactBisectionDecisions": bisection_decisions,
                "lowerPolynomialValue": r037.rational_record(
                    lower_sign_value
                ),
                "upperPolynomialValue": r037.rational_record(
                    upper_sign_value
                ),
                "floatingPointSignDecisionUsed": False,
            },
            "sturmCertificate": {
                "sequenceLength": len(sturm),
                "degrees": sturm_degrees,
                "normalizedLeadingCoefficientAbsoluteValue": "1",
                "polynomialSha256BySequenceIndex": sturm_digests,
                "lowerEndpoint": sturm_lower,
                "upperEndpoint": sturm_upper,
                "rootCount": sturm_root_count,
                "proof": (
                    "the variation count falls by exactly one across the "
                    "isolating interval; all divisions and endpoint signs "
                    "use exact GMP rational arithmetic"
                ),
                "classification": "formal exact Sturm root-count certificate",
            },
            "fullWindowDominance": {
                "activeLowerBoundAtWindowLeft": r037.rational_record(
                    target_active_value
                ),
                "competitorUpperRadius": r037.rational_record(window_upper),
                "competitorsCovered": len(competitor_records),
                "otherFixedPositiveCharges": 238,
                "inactiveEndpointOfActiveCharge": 1,
                "otherExhaustiveChargeSectors": 4,
                "nearestCompetitor": competitor_label,
                "nearestCompetitorUpperBoundAtWindowRight": (
                    r037.rational_record(competitor_maximum)
                ),
                "minimumDominanceGap": r037.rational_record(
                    minimum_dominance_gap
                ),
                "records": competitor_records,
                "competitorBoundDigestSha256": dominance_digest,
                "tailDegreeGridUsed": False,
                "chargeGridBeyondFiniteTheoremListUsed": False,
                "monotoneSandwichProof": (
                    "every exact weighted column is a nonnegative sum of "
                    "powers of r, so each competitor on the window is at "
                    "most its pinned all-order R0.47 bound at the right "
                    "endpoint; the active exact column is at least its "
                    "left-endpoint value, and every recorded exact gap is "
                    "strictly positive"
                ),
            },
            "conclusion": {
                "belowRoot": (
                    "for every r in [0.376932,r_*), the full induced norm "
                    "equals the active C_r(81,162) column and is below one"
                ),
                "atRoot": (
                    "at r_*, the full induced norm equals the active true "
                    "column and is exactly one"
                ),
                "aboveRoot": (
                    "for every r in (r_*,0.376933], the active true column "
                    "exceeds one, so the current sufficient contraction "
                    "criterion fails"
                ),
                "classification": (
                    "formal local sharp-threshold theorem for the current "
                    "induced two-block weighted-l1 norm"
                ),
            },
        },
        "finiteConstruction": {
            "degreeEightyPolynomialTerms": len(polynomial),
            "degreeEightyPolynomialSha256": polynomial_digest,
            "recurrenceMaximumDegree": maximum_degree,
            "recurrenceOrderedInteractions": recurrence_interactions,
            "classification": (
                "finite exact construction of the center polynomial; the "
                "tail coverage and threshold comparison are all-order"
            ),
        },
        "checks": checks,
        "computation": {
            "exactBackend": "gmpy2.mpq/mpz (GMP rational and integer arithmetic)",
            "decimalDecisionUse": False,
            "randomness": False,
            "wallSeconds": elapsed,
            "python": platform.python_version(),
            "platform": platform.platform(),
            "createdUtc": datetime.now(timezone.utc).isoformat(),
        },
    }


def main() -> None:
    global PROGRESS_LOG
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-total-degree", type=int, default=80)
    parser.add_argument("--window-lower", default="376932/1000000")
    parser.add_argument("--window-upper", default="376933/1000000")
    parser.add_argument("--root-decimal-digits", type=int, default=18)
    parser.add_argument("--zero-charge-weight", default="3/4")
    parser.add_argument("--charge-cutoff", type=int, default=241)
    parser.add_argument("--source-commit")
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--progress-log", type=Path)
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    if arguments.max_total_degree != 80:
        raise SystemExit("R0.48 is pinned to --max-total-degree 80")
    if arguments.charge_cutoff != 241:
        raise SystemExit("R0.48 is pinned to --charge-cutoff 241")
    if arguments.root_decimal_digits < 7:
        raise SystemExit("--root-decimal-digits must be at least 7")

    PROGRESS_LOG = arguments.progress_log
    if PROGRESS_LOG is not None:
        PROGRESS_LOG.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_LOG.write_text("", encoding="utf-8")

    payload = build_payload(
        arguments.max_total_degree,
        rational(arguments.window_lower),
        rational(arguments.window_upper),
        arguments.root_decimal_digits,
        rational(arguments.zero_charge_weight),
        arguments.charge_cutoff,
        arguments.progress,
        arguments.source_commit,
    )
    if arguments.check and not all(payload["checks"].values()):
        raise SystemExit("R0.48 checks failed")
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
