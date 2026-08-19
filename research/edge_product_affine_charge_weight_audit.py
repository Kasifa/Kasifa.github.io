#!/usr/bin/env python3
"""R0.53 exact audit for one fixed product-affine charge weight.

For the exact degree-80 reduced canonical edge center, use

    omega_s = c^s (1 + lambda |s|) (1 + mu |s|)

with the simple rational parameters

    c = 396403/500000,
    lambda = mu = 153931/500000.

Each affine factor is submultiplicative with constant one, hence so is their
product.  The zero-charge column is the sharp column for this fixed weight.
This script isolates its unique positive root in an exact width-10^-18 box,
checks every fixed positive charge below 280, proves the two exceptional
charges, and uses exact parity/Bernstein certificates for all charges s>=280.
It also verifies an exact fixed-point restart at r=95657/250000.

The resulting rational witness lies strictly beyond the R0.52 global upper
bound for the complete single-affine family.  This disproves degeneration of
the product-affine family to that boundary.  It does not optimize the complete
product-affine family, construct a critical-space bridge for arbitrary
three-dimensional fields, or prove or disprove three-dimensional
Navier--Stokes regularity.
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

import edge_affine_charge_weight_audit as r051
import edge_affine_family_kkt_audit as r052
import edge_charge_degree_lattice_audit as r047
import edge_charge_resolved_audit as r039
import edge_charge_threshold_root_audit as r048
import edge_rational_asymptotic_audit as r028
import edge_short_continuation_audit as r036
import edge_weighted_restart_audit as r037


Rational = gmpy2.mpq
Poly = list[Rational]
Polynomial = dict[tuple[int, int], Rational]

R052_CERTIFICATE = Path(
    "research/certificates/r052/edge-affine-family-global.json"
)
R052_EXPECTED_SHA256 = (
    "b79e59ec327bc02b64e23ad3f903b6d61860a075d59ff75a43d82f5684590def"
)
POLYNOMIAL_SHA256 = (
    "056a0adba7f3cba41a6e9bd6d943a8f59be28f50f44c6035df1f68393ed26be7"
)
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(
            f"[R0.53 +{elapsed:8.2f}s] {stage}{suffix}",
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


def product_ratio(
    input_charge: int,
    center_charge: int,
    lam: Rational,
    mu: Rational,
) -> Rational:
    return r051.affine_ratio(input_charge, center_charge, lam) * r051.affine_ratio(
        input_charge, center_charge, mu
    )


def exact_product_column_polynomial(
    terms: list[tuple[int, int, Rational]],
    maximum_degree: int,
    input_degree: int,
    input_charge: int,
    lam: Rational,
    mu: Rational,
) -> Poly:
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
            * product_ratio(input_charge, charge, lam, mu)
        )
    return r047.trim(result)


def product_fixed_charge_endpoint_polynomials(
    terms: list[tuple[int, int, Rational]],
    maximum_degree: int,
    input_charge: int,
    lam: Rational,
    mu: Rational,
) -> tuple[Poly, Poly, int]:
    """Exact all-degree convex endpoints for one fixed charge s>=2."""

    minimum_degree = r039.minimum_tail_degree(input_charge, maximum_degree)
    maximum_slope = Rational(input_charge, minimum_degree)
    infinity = [Rational(0)] * (maximum_degree + 1)
    minimum = [Rational(0)] * (maximum_degree + 1)
    for degree, charge, coefficient in terms:
        if input_charge + charge <= 0:
            raise AssertionError("positive input charge met nonpositive output")
        common = (
            coefficient
            * Rational(degree + minimum_degree, degree + minimum_degree - 1)
            * Rational(
                abs(input_charge - charge),
                3 * abs(input_charge + charge),
            )
            * product_ratio(input_charge, charge, lam, mu)
        )
        infinity[degree] += common * abs(charge)
        minimum[degree] += common * abs(
            degree * maximum_slope - charge
        )
    return r047.trim(infinity), r047.trim(minimum), minimum_degree


def product_zero_sector_polynomial(
    terms: list[tuple[int, int, Rational]],
    maximum_degree: int,
    lam: Rational,
    mu: Rational,
) -> Poly:
    minimum_degree = r039.minimum_tail_degree(0, maximum_degree)
    result = [Rational(0)] * (maximum_degree + 1)
    for degree, charge, coefficient in terms:
        if charge == 0:
            continue
        result[degree] += (
            coefficient
            * Rational(degree + minimum_degree, degree + minimum_degree - 1)
            * Rational(abs(charge), 3)
            * (1 + lam * abs(charge))
            * (1 + mu * abs(charge))
        )
    return r047.trim(result)


def product_plus_one_polynomial(
    terms: list[tuple[int, int, Rational]],
    maximum_degree: int,
    lam: Rational,
    mu: Rational,
) -> Poly:
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
            * product_ratio(1, charge, lam, mu)
        )
    return r047.trim(result)


def minus_one_endpoint_certificate(
    terms: list[tuple[int, int, Rational]],
    maximum_degree: int,
    radius: Rational,
    lam: Rational,
    mu: Rational,
) -> dict[str, object]:
    """Prove the product-affine s=-1 column is maximal at j=82."""

    minimum_degree = r039.minimum_tail_degree(-1, maximum_degree)
    upper_t = Rational(1, minimum_degree)
    weighted = [
        (degree, charge, coefficient * radius**degree)
        for degree, charge, coefficient in terms
    ]
    q_one_terms = [item for item in weighted if item[1] == 1]
    negative_derivative = sum(
        (
            coefficient
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
        for degree, charge, coefficient in weighted
        if degree == 1 and charge == 2
    ]
    if len(seeds) != 1:
        raise AssertionError("expected one degree-one q=2 seed")
    seed_derivative = 3 * seeds[0]
    exceptional_ratio = Rational(1, (1 + lam) * (1 + mu))
    derivative_margin = seed_derivative - exceptional_ratio * negative_derivative
    if derivative_margin <= 0:
        raise AssertionError("product-affine s=-1 derivative margin is not positive")
    endpoint_poly = exact_product_column_polynomial(
        terms,
        maximum_degree,
        minimum_degree,
        -1,
        lam,
        mu,
    )
    return {
        "inputCharge": -1,
        "minimumTailDegree": minimum_degree,
        "inverseDegreeInterval": [
            r037.rational_record(Rational(0)),
            r037.rational_record(upper_t),
        ],
        "qOneTermCount": len(q_one_terms),
        "qOneProductAffineRatio": r037.rational_record(exceptional_ratio),
        "weightedQOneDerivativeUpperBound": r037.rational_record(
            exceptional_ratio * negative_derivative
        ),
        "seedDerivativeLowerBound": r037.rational_record(seed_derivative),
        "fullDerivativeLowerBound": r037.rational_record(derivative_margin),
        "endpointPolynomial": endpoint_poly,
        "proof": (
            "q=-1 terms vanish; q=0 and q>=2 terms have nonnegative "
            "t=1/j derivative. Only q=1 can decrease. Its product-affine "
            "output/input ratio is 1/((1+lambda)(1+mu)), and the weighted "
            "q=2 seed exceeds the complete q=1 derivative upper bound"
        ),
        "allDegreeEndpointProved": True,
        "classification": "formal exact all-degree product-affine s=-1 theorem",
    }


def product_large_charge_certificate(
    terms: list[tuple[int, int, Rational]],
    maximum_degree: int,
    radius: Rational,
    charge_cutoff: int,
) -> dict[str, object]:
    """Exact parity/Bernstein theorem for every s>=charge_cutoff."""

    if maximum_degree != 80 or charge_cutoff % 2:
        raise AssertionError("R0.53 uses an even large-charge cutoff at N=80")
    envelope_terms = []
    for degree, charge, coefficient in terms:
        envelope = (
            Rational(1)
            if charge == -1
            else (1 + Rational(charge, charge_cutoff)) ** 2
        )
        envelope_terms.append(
            (degree, charge, coefficient * radius**degree * envelope)
        )

    common_degree_floor = charge_cutoff // 2
    zero_endpoint = Rational(0)
    for degree, charge, coefficient in envelope_terms:
        zero_endpoint += (
            coefficient
            * Rational(
                degree + common_degree_floor,
                degree + common_degree_floor - 1,
            )
            * (
                Rational(charge_cutoff + 1, charge_cutoff - 1)
                if charge == -1
                else Rational(1)
            )
            * abs(charge)
            / 3
        )

    even_numerator, even_denominator, even_factors = (
        r047.endpoint_rational_function(envelope_terms, "even")
    )
    odd_numerator, odd_denominator, odd_factors = (
        r047.endpoint_rational_function(envelope_terms, "odd")
    )
    even_upper = Rational(1, charge_cutoff)
    odd_upper = Rational(1, charge_cutoff + 1)
    even_derivative = r047.rational_function_derivative_certificate(
        even_numerator,
        even_denominator,
        even_factors,
        even_upper,
        1,
    )
    odd_derivative = r047.rational_function_derivative_certificate(
        odd_numerator,
        odd_denominator,
        odd_factors,
        odd_upper,
        -1,
    )
    even_first = r047.rational_function_value(
        even_numerator, even_denominator, even_upper
    )
    even_limit = r047.rational_function_value(
        even_numerator, even_denominator, Rational(0)
    )
    odd_first = r047.rational_function_value(
        odd_numerator, odd_denominator, odd_upper
    )
    odd_limit = r047.rational_function_value(
        odd_numerator, odd_denominator, Rational(0)
    )
    if even_limit != odd_limit:
        raise AssertionError("parity endpoint functions have different limits")
    if not even_derivative["allSignedBernsteinCoefficientsPositive"]:
        raise AssertionError("even large-charge derivative certificate failed")
    if not odd_derivative["allSignedBernsteinCoefficientsPositive"]:
        raise AssertionError("odd large-charge derivative certificate failed")
    candidates = [
        ("zero endpoint", zero_endpoint),
        (f"even s={charge_cutoff}", even_first),
        ("odd s->infinity", odd_limit),
    ]
    maximum_source, maximum = max(candidates, key=lambda item: item[1])
    return {
        "chargeRange": f"s>={charge_cutoff}",
        "coefficientwiseEnvelope": (
            "q=-1 uses factor 1; q>=0 uses (1+q/S)^2 because each "
            "affine ratio is at most 1+q/s<=1+q/S"
        ),
        "zeroEndpointUniform": r037.rational_record(zero_endpoint),
        "evenEndpoint": {
            "firstCharge": charge_cutoff,
            "valueAtFirstCharge": r037.rational_record(even_first),
            "limit": r037.rational_record(even_limit),
            "derivativeCertificate": even_derivative,
        },
        "oddEndpoint": {
            "firstCharge": charge_cutoff + 1,
            "valueAtFirstCharge": r037.rational_record(odd_first),
            "limit": r037.rational_record(odd_limit),
            "derivativeCertificate": odd_derivative,
        },
        "bound": r037.rational_record(maximum),
        "maximumSource": maximum_source,
        "allChargesAndDegreesCovered": True,
        "classification": "formal exact product-affine large-charge theorem",
    }


def product_weighted_norm(
    polynomial: Polynomial,
    radius: Rational,
    character: Rational,
    lam: Rational,
    mu: Rational,
) -> Rational:
    return sum(
        (
            abs(coefficient)
            * radius ** r039.degree(exponent)
            * character ** r039.charge(exponent)
            * (1 + lam * abs(r039.charge(exponent)))
            * (1 + mu * abs(r039.charge(exponent)))
            for exponent, coefficient in polynomial.items()
        ),
        Rational(0),
    )


def build_payload(
    maximum_degree: int,
    character: Rational,
    lam: Rational,
    mu: Rational,
    radius_lower: Rational,
    radius_upper: Rational,
    restart_radius: Rational,
    charge_cutoff: int,
    ball_divisor: int,
    show_progress: bool,
    source_commit: str | None,
) -> dict[str, object]:
    started = time.perf_counter()
    progress(show_progress, started, "loading pinned R0.52 certificate")
    if sha256(R052_CERTIFICATE) != R052_EXPECTED_SHA256:
        raise AssertionError("R0.52 certificate hash mismatch")
    r052_certificate = json.loads(R052_CERTIFICATE.read_text(encoding="utf-8"))
    previous_upper = rational(
        r052_certificate["globalAffineFamilyBound"]["optimalRadiusUpper"]["exact"]
    )
    if maximum_degree != 80 or charge_cutoff != 280:
        raise AssertionError("R0.53 is pinned to N=80 and S=280")
    if character != Rational(396403, 500000):
        raise AssertionError("R0.53 character changed")
    if lam != Rational(153931, 500000) or mu != lam:
        raise AssertionError("R0.53 product-affine parameters changed")
    if radius_lower != Rational(382628602237879637, 10**18):
        raise AssertionError("R0.53 root lower endpoint changed")
    if radius_upper != Rational(382628602237879638, 10**18):
        raise AssertionError("R0.53 root upper endpoint changed")
    if restart_radius != Rational(95657, 250000):
        raise AssertionError("R0.53 restart radius changed")

    progress(show_progress, started, "constructing exact degree-80 center and residual")
    active_field, _, _, recurrence_interactions = r028.rational_edge_recurrence(
        maximum_degree, show_progress, started
    )
    polynomial = r036.field_to_polynomial(active_field, maximum_degree)
    seed = {(1, 0): Rational(1), (0, 1): Rational(1)}
    residual = r036.add(
        polynomial,
        r036.scale(seed, -1),
        r036.scale(r036.phi(polynomial), -1),
    )
    if r036.truncate(residual, maximum_degree):
        raise AssertionError("degree recurrence has residual below cutoff")
    polynomial_digest = r037.polynomial_digest(polynomial)
    if polynomial_digest != POLYNOMIAL_SHA256:
        raise AssertionError("degree-80 polynomial digest changed")
    terms = r051.charge_scaled_terms(polynomial, character)

    progress(show_progress, started, "isolating the zero-charge threshold root")
    zero_poly = product_zero_sector_polynomial(
        terms, maximum_degree, lam, mu
    )
    threshold_poly = r048.threshold_polynomial(zero_poly)
    lower_sign = r047.poly_evaluate(threshold_poly, radius_lower)
    upper_sign = r047.poly_evaluate(threshold_poly, radius_upper)
    if lower_sign >= 0 or upper_sign <= 0:
        raise AssertionError("zero-charge root box has incorrect endpoint signs")
    if zero_poly[0] != 0 or not all(value > 0 for value in zero_poly[1:]):
        raise AssertionError("zero-charge polynomial lost strict positive form")
    sturm = r048.sturm_sequence(threshold_poly)
    sturm_lower = r048.sturm_endpoint_record(sturm, radius_lower)
    sturm_upper = r048.sturm_endpoint_record(sturm, radius_upper)
    root_count = sturm_lower["variations"] - sturm_upper["variations"]
    if root_count != 1:
        raise AssertionError("Sturm chain did not isolate exactly one root")

    zero_lower = r047.poly_evaluate(zero_poly, radius_lower)
    zero_restart = r047.poly_evaluate(zero_poly, restart_radius)
    competitor_records: list[dict[str, object]] = []
    competitor_values: list[tuple[str, Rational]] = []

    progress(
        show_progress,
        started,
        "auditing every fixed positive charge",
        first=2,
        last=charge_cutoff - 1,
    )
    for input_charge in range(2, charge_cutoff):
        infinity, minimum, degree_floor = (
            product_fixed_charge_endpoint_polynomials(
                terms,
                maximum_degree,
                input_charge,
                lam,
                mu,
            )
        )
        infinity_upper = r047.poly_evaluate(infinity, radius_upper)
        minimum_upper = r047.poly_evaluate(minimum, radius_upper)
        if infinity_upper >= minimum_upper:
            endpoint = "x=0"
            endpoint_poly = infinity
            value = infinity_upper
        else:
            endpoint = f"j={degree_floor}"
            endpoint_poly = minimum
            value = minimum_upper
        label = f"s={input_charge},{endpoint}"
        restart_value = r047.poly_evaluate(endpoint_poly, restart_radius)
        competitor_values.append((label, value))
        competitor_records.append(
            {
                "label": label,
                "sector": "fixed positive charge",
                "inputCharge": input_charge,
                "minimumTailDegree": degree_floor,
                "endpoint": endpoint,
                "upperBoundAtRootBoxRight": r037.rational_record(value),
                "gapBelowZeroEquality": r037.rational_record(1 - value),
                "belowZeroAtRestart": restart_value < zero_restart,
                "coefficientCount": len(endpoint_poly),
                "allCoefficientsNonnegative": r048.all_nonnegative(endpoint_poly),
                "coefficientSha256": r047.polynomial_digest(endpoint_poly),
            }
        )

    progress(show_progress, started, "auditing the exceptional charges")
    plus_poly = product_plus_one_polynomial(terms, maximum_degree, lam, mu)
    minus_certificate = minus_one_endpoint_certificate(
        terms, maximum_degree, radius_upper, lam, mu
    )
    minus_poly = minus_certificate.pop("endpointPolynomial")
    for label, sector, poly, proof in [
        (
            "s=1",
            "plus-one input charge",
            plus_poly,
            "termwise all-degree finite-charge bound with exact product ratios",
        ),
        (
            "s=-1",
            "minus-one input charge",
            minus_poly,
            minus_certificate["proof"],
        ),
    ]:
        if not r048.all_nonnegative(poly):
            raise AssertionError(f"{label} polynomial lost nonnegativity")
        value = r047.poly_evaluate(poly, radius_upper)
        restart_value = r047.poly_evaluate(poly, restart_radius)
        competitor_values.append((label, value))
        competitor_records.append(
            {
                "label": label,
                "sector": sector,
                "upperBoundAtRootBoxRight": r037.rational_record(value),
                "gapBelowZeroEquality": r037.rational_record(1 - value),
                "belowZeroAtRestart": restart_value < zero_restart,
                "coefficientCount": len(poly),
                "allCoefficientsNonnegative": True,
                "coefficientSha256": r047.polynomial_digest(poly),
                "proof": proof,
            }
        )

    progress(show_progress, started, "certifying the complete large-charge tail")
    large = product_large_charge_certificate(
        terms,
        maximum_degree,
        radius_upper,
        charge_cutoff,
    )
    large_value = rational(large["bound"]["exact"])
    competitor_values.append((f"s>={charge_cutoff}", large_value))
    competitor_records.append(
        {
            "label": f"s>={charge_cutoff}",
            "sector": "large positive charge",
            "upperBoundAtRootBoxRight": large["bound"],
            "gapBelowZeroEquality": r037.rational_record(1 - large_value),
            "belowZeroAtRestart": large_value < zero_restart,
            "proof": (
                "coefficientwise squared-affine envelope followed by exact "
                "even/odd rational endpoint and Bernstein derivative theorems"
            ),
        }
    )

    nearest_label, nearest_value = max(competitor_values, key=lambda item: item[1])
    minimum_gap = 1 - nearest_value
    if minimum_gap <= 0:
        raise AssertionError("a competitor reached the zero-charge root box")
    if not all(record["belowZeroAtRestart"] for record in competitor_records):
        raise AssertionError("zero-charge column is not the restart maximum")

    progress(show_progress, started, "checking the exact fixed-point restart")
    polynomial_norm = product_weighted_norm(
        polynomial, restart_radius, character, lam, mu
    )
    residual_norm = product_weighted_norm(
        residual, restart_radius, character, lam, mu
    )
    linear_bound = zero_restart
    margin = 1 - linear_bound
    ball_radius = margin / ball_divisor
    quadratic_constant = Rational(3)
    residual_allowance = (
        margin * ball_radius - quadratic_constant * ball_radius**2
    )
    mapping_upper = (
        residual_norm
        + linear_bound * ball_radius
        + quadratic_constant * ball_radius**2
    )
    lipschitz_upper = linear_bound + 2 * quadratic_constant * ball_radius
    fixed_point = (
        margin > 0
        and residual_norm < residual_allowance
        and mapping_upper < ball_radius
        and lipschitz_upper < 1
    )
    if not fixed_point:
        raise AssertionError("product-affine weighted fixed-point restart failed")

    root_gain_lower = radius_lower / previous_upper
    restart_gain = restart_radius / previous_upper
    checks = {
        "r052CertificateHashMatches": True,
        "polynomialDigestMatchesR052": polynomial_digest == POLYNOMIAL_SHA256,
        "productAffineParametersArePositive": (
            character > 0 and lam >= 0 and mu >= 0
        ),
        "productAffineWeightIsSubmultiplicativeWithConstantOne": True,
        "zeroPolynomialHasPositiveNonconstantCoefficients": (
            zero_poly[0] == 0 and all(value > 0 for value in zero_poly[1:])
        ),
        "zeroThresholdStrictlyIncreasesInRadius": True,
        "rootEndpointSignsAreStrict": lower_sign < 0 < upper_sign,
        "sturmChainCountsExactlyOneRoot": root_count == 1,
        "rootBoxWidthIsOneEminusEighteen": (
            radius_upper - radius_lower == Rational(1, 10**18)
        ),
        "rootLowerBoundExceedsR052GlobalUpperBound": radius_lower > previous_upper,
        "allFixedPositiveChargesCovered": (
            sum(
                record["sector"] == "fixed positive charge"
                for record in competitor_records
            )
            == charge_cutoff - 2
        ),
        "plusAndMinusSectorsCovered": all(
            any(record["label"] == label for record in competitor_records)
            for label in ["s=1", "s=-1"]
        ),
        "minusOneAllDegreeEndpointProved": minus_certificate[
            "allDegreeEndpointProved"
        ],
        "largeChargeEvenBernsteinCertificatePasses": large["evenEndpoint"]
        ["derivativeCertificate"]["allSignedBernsteinCoefficientsPositive"],
        "largeChargeOddBernsteinCertificatePasses": large["oddEndpoint"]
        ["derivativeCertificate"]["allSignedBernsteinCoefficientsPositive"],
        "largeChargeAllOrdersCovered": large["allChargesAndDegreesCovered"],
        "allCompetitorsCovered": len(competitor_records) == charge_cutoff + 1,
        "allCompetitorsStrictlyBelowZeroOnRootBox": minimum_gap > 0,
        "zeroChargeColumnIsRestartMaximum": all(
            record["belowZeroAtRestart"] for record in competitor_records
        ),
        "restartRadiusExceedsR052GlobalUpperBound": restart_radius > previous_upper,
        "restartLinearBoundIsBelowOne": linear_bound < 1,
        "restartResidualUsesProductAffineWeightedNorm": True,
        "restartFixedPointPasses": fixed_point,
        "noTailDegreeGridUsed": True,
        "noLargeChargeGridUsed": True,
        "noFloatingPointSignDecision": True,
        "completeProductFamilyOptimalityNotClaimed": True,
        "threeDimensionalNavierStokesRegularityNotClaimed": True,
    }
    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError("R0.53 checks failed: " + ", ".join(failed))
    progress(
        show_progress,
        started,
        "all exact checks passed",
        checks=len(checks),
        competitors=len(competitor_records),
        nearestCompetitor=nearest_label,
    )

    return {
        "schemaVersion": "1.0",
        "scope": {
            "system": "reduced canonical edge generating system",
            "theorem": (
                "one fixed rational product-affine charge weight has a unique "
                "zero-charge threshold root and a certified all-order restart "
                "strictly beyond the complete single-affine family"
            ),
            "notClaimed": [
                "global optimality in the complete product-affine family",
                "optimization over every possible Banach norm",
                "a critical-norm bridge for arbitrary three-dimensional velocity fields",
                "three-dimensional Navier-Stokes regularity or singularity",
            ],
        },
        "input": {
            "maximumTotalDegree": maximum_degree,
            "chargeCutoff": charge_cutoff,
            "character": r037.rational_record(character),
            "lambda": r037.rational_record(lam),
            "mu": r037.rational_record(mu),
            "weightFormula": "omega_s=c^s(1+lambda|s|)(1+mu|s|)",
            "rootBox": [
                r037.rational_record(radius_lower),
                r037.rational_record(radius_upper),
            ],
            "restartRadius": r037.rational_record(restart_radius),
            "ballDivisor": ball_divisor,
        },
        "weightTheorem": {
            "positive": character > 0 and lam >= 0 and mu >= 0,
            "submultiplicativeInequality": (
                "apply 1+t|a+b|<=(1+t|a|)(1+t|b|) separately for "
                "t=lambda and t=mu; multiply the two inequalities"
            ),
            "algebraConstant": r037.rational_record(Rational(1)),
            "classification": "formal all-integer charge-weight theorem",
        },
        "finiteConstruction": {
            "maximumTotalDegree": maximum_degree,
            "centerTerms": len(terms),
            "recurrenceOrderedInteractions": recurrence_interactions,
            "degreeEightyPolynomialSha256": polynomial_digest,
            "classification": "finite exact degree-80 construction",
        },
        "thresholdTheorem": {
            "activeSector": "s=0,j=81",
            "rootIsolation": {
                "lower": r037.rational_record(radius_lower),
                "upper": r037.rational_record(radius_upper),
                "width": r037.rational_record(radius_upper - radius_lower),
                "lowerThresholdSign": r037.rational_record(lower_sign),
                "upperThresholdSign": r037.rational_record(upper_sign),
                "sturmVariationsLower": sturm_lower,
                "sturmVariationsUpper": sturm_upper,
                "positiveRootCountInBox": root_count,
            },
            "strictMonotonicity": (
                "the zero-charge polynomial has zero constant term and "
                "strictly positive coefficients in every degree 1 through 80"
            ),
            "globallyUniquePositiveRoot": True,
            "classification": "formal exact fixed-weight threshold theorem",
        },
        "comparisonWithR052": {
            "r052CompleteAffineUpper": r037.rational_record(previous_upper),
            "productAffineRootLower": r037.rational_record(radius_lower),
            "rootRadiusGainLowerFactor": r037.rational_record(root_gain_lower),
            "restartRadius": r037.rational_record(restart_radius),
            "restartGainFactor": r037.rational_record(restart_gain),
            "strictCounterexampleToBoundaryDegeneration": radius_lower > previous_upper,
            "interpretation": (
                "the product-affine family strictly exceeds the globally "
                "certified optimum of the complete single-affine family"
            ),
        },
        "competitorDominance": {
            "activeEquality": "s=0,j=81",
            "records": competitor_records,
            "recordsCovered": len(competitor_records),
            "nearestCompetitor": nearest_label,
            "nearestCompetitorUpperBound": r037.rational_record(nearest_value),
            "minimumGap": r037.rational_record(minimum_gap),
            "zeroColumnAtRootBoxLeft": r037.rational_record(zero_lower),
            "classification": "formal exact all-order competitor theorem",
        },
        "minusOneAllDegreeTheorem": minus_certificate,
        "largeChargeEnvelopeTheorem": large,
        "restartCertificate": {
            "radius": r037.rational_record(restart_radius),
            "character": r037.rational_record(character),
            "lambda": r037.rational_record(lam),
            "mu": r037.rational_record(mu),
            "productAffineWeightedPolynomialNorm": r037.rational_record(
                polynomial_norm
            ),
            "productAffineWeightedResidualNorm": r037.rational_record(residual_norm),
            "linearizationBound": r037.rational_record(linear_bound),
            "contractionMargin": r037.rational_record(margin),
            "chosenBallRadius": r037.rational_record(ball_radius),
            "quadraticConstant": r037.rational_record(quadratic_constant),
            "residualAllowance": r037.rational_record(residual_allowance),
            "mappingUpperBound": r037.rational_record(mapping_upper),
            "lipschitzUpperBound": r037.rational_record(lipschitz_upper),
            "fixedPointPasses": fixed_point,
            "classification": (
                "exact fixed-point certificate in the product-affine "
                "weighted coefficient Banach algebra"
            ),
        },
        "remainingBeyondR053": [
            "optimize or globally enclose the complete product-affine family",
            "decide whether the symmetric interior diagnostic root is globally optimal",
            "construct or rule out a scale-critical bridge to the full three-dimensional PDE",
        ],
        "checks": checks,
        "git": r039.git_state(source_commit),
        "computation": {
            "createdUtc": datetime.now(timezone.utc).isoformat(),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "exactBackend": f"gmpy2 {gmpy2.version()} / GMP {gmpy2.mp_version()}",
            "randomness": False,
            "gpu": False,
            "decimalDecisionUse": False,
            "wallSeconds": time.perf_counter() - started,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-total-degree", type=int, default=80)
    parser.add_argument("--character", default="396403/500000")
    parser.add_argument("--lambda", dest="lam", default="153931/500000")
    parser.add_argument("--mu", default="153931/500000")
    parser.add_argument(
        "--radius-lower", default="382628602237879637/1000000000000000000"
    )
    parser.add_argument(
        "--radius-upper", default="382628602237879638/1000000000000000000"
    )
    parser.add_argument("--restart-radius", default="95657/250000")
    parser.add_argument("--charge-cutoff", type=int, default=280)
    parser.add_argument("--ball-divisor", type=int, default=1_000_000)
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
        rational(arguments.character),
        rational(arguments.lam),
        rational(arguments.mu),
        rational(arguments.radius_lower),
        rational(arguments.radius_upper),
        rational(arguments.restart_radius),
        arguments.charge_cutoff,
        arguments.ball_divisor,
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
