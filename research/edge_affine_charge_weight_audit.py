#!/usr/bin/env python3
"""R0.51 exact audit for one affine charge weight.

For the exact degree-80 center, fix

    omega_s = c^s (1 + lambda |s|),
    c = 19939/25000, lambda = 7653/10000.

The elementary inequality

    1 + lambda |a+b| <= (1 + lambda |a|)(1 + lambda |b|)

makes this a submultiplicative charge weight with algebra constant one.  The
script constructs every fixed-charge endpoint exactly and proves that the
true (j,s)=(81,162) column is the unique active column near its threshold.
Its positive coefficient polynomial has one root in

    0.382624471846022 < r_* < 0.382624471846023.

The sectors s=0, s=-1, s=1, 2<=s<241, and s>=241 are exhaustive.  Fixed
positive charges use exact convex endpoints.  The large-charge branch is
bounded by a coefficientwise affine envelope and the existing parity/
Bernstein theorem.  The s=-1 endpoint proof is repeated with its only
negative derivative contribution reduced by 1/(1+lambda).

All sign decisions use GMP rationals.  The theorem concerns one reduced
canonical edge generating system and one fixed affine weighted norm.  It is
not an optimization over every Banach norm, a bridge theorem for arbitrary
three-dimensional velocity fields, or a proof of Navier--Stokes regularity.
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

import edge_charge_character_optimization_audit as r050
import edge_charge_degree_lattice_audit as r047
import edge_charge_resolved_audit as r039
import edge_charge_threshold_root_audit as r048
import edge_rational_asymptotic_audit as r028
import edge_short_continuation_audit as r036
import edge_weighted_restart_audit as r037


Rational = gmpy2.mpq
Polynomial = dict[tuple[int, int], Rational]
Poly = list[Rational]

R050_CERTIFICATE = Path(
    "research/certificates/r050/edge-charge-character-optimization.json"
)
R050_EXPECTED_SHA256 = (
    "fc173a2108ef881d21d9d54046085f0d5daf5cc33ed50e024ca32ec867f7b79a"
)
R050_POLYNOMIAL_SHA256 = (
    "056a0adba7f3cba41a6e9bd6d943a8f59be28f50f44c6035df1f68393ed26be7"
)
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(
            f"[R0.51 +{elapsed:8.2f}s] {stage}{suffix}",
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


def affine_ratio(input_charge: int, center_charge: int, lam: Rational) -> Rational:
    output_charge = input_charge + center_charge
    return Rational(1 + lam * abs(output_charge), 1 + lam * abs(input_charge))


def charge_scaled_terms(
    polynomial: Polynomial, character: Rational
) -> list[tuple[int, int, Rational]]:
    return [
        (
            r039.degree(exponent),
            r039.charge(exponent),
            abs(coefficient) * character ** r039.charge(exponent),
        )
        for exponent, coefficient in polynomial.items()
    ]


def exact_affine_column_polynomial(
    terms: list[tuple[int, int, Rational]],
    maximum_degree: int,
    input_degree: int,
    input_charge: int,
    lam: Rational,
) -> Poly:
    result = [Rational(0)] * (maximum_degree + 1)
    for degree, charge, coefficient in terms:
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
            * affine_ratio(input_charge, charge, lam)
        )
        result[degree] += coefficient * factor
    return r047.trim(result)


def affine_fixed_charge_endpoint_polynomials(
    terms: list[tuple[int, int, Rational]],
    maximum_degree: int,
    input_charge: int,
    lam: Rational,
) -> tuple[Poly, Poly, int]:
    """Exact all-degree convex endpoints for one fixed s>=2."""

    minimum_degree = r039.minimum_tail_degree(input_charge, maximum_degree)
    maximum_slope = Rational(input_charge, minimum_degree)
    infinity = [Rational(0)] * (maximum_degree + 1)
    minimum = [Rational(0)] * (maximum_degree + 1)
    for degree, charge, coefficient in terms:
        if input_charge + charge <= 0:
            raise AssertionError("positive input charge met nonpositive output")
        common = (
            coefficient
            * Rational(
                degree + minimum_degree,
                degree + minimum_degree - 1,
            )
            * Rational(
                abs(input_charge - charge),
                3 * abs(input_charge + charge),
            )
            * affine_ratio(input_charge, charge, lam)
        )
        infinity[degree] += common * abs(charge)
        minimum[degree] += common * abs(
            degree * maximum_slope - charge
        )
    return r047.trim(infinity), r047.trim(minimum), minimum_degree


def affine_zero_sector_polynomial(
    terms: list[tuple[int, int, Rational]],
    maximum_degree: int,
    lam: Rational,
) -> Poly:
    minimum_degree = r039.minimum_tail_degree(0, maximum_degree)
    result = [Rational(0)] * (maximum_degree + 1)
    for degree, charge, coefficient in terms:
        if charge == 0:
            continue
        result[degree] += (
            coefficient
            * Rational(
                degree + minimum_degree,
                degree + minimum_degree - 1,
            )
            * Rational(abs(charge), 3)
            * (1 + lam * abs(charge))
        )
    return r047.trim(result)


def affine_plus_one_polynomial(
    terms: list[tuple[int, int, Rational]],
    maximum_degree: int,
    lam: Rational,
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
            * affine_ratio(1, charge, lam)
        )
    return r047.trim(result)


def minus_one_endpoint_certificate(
    terms: list[tuple[int, int, Rational]],
    maximum_degree: int,
    radius: Rational,
    lam: Rational,
) -> dict[str, object]:
    """Prove the affine s=-1 column is maximal at j=82."""

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
    exceptional_ratio = Rational(1, 1 + lam)
    derivative_margin = seed_derivative - exceptional_ratio * negative_derivative
    if derivative_margin <= 0:
        raise AssertionError("affine s=-1 derivative margin is not positive")
    endpoint_poly = exact_affine_column_polynomial(
        terms,
        maximum_degree,
        minimum_degree,
        -1,
        lam,
    )
    return {
        "inputCharge": -1,
        "minimumTailDegree": minimum_degree,
        "inverseDegreeInterval": [
            r037.rational_record(Rational(0)),
            r037.rational_record(upper_t),
        ],
        "qOneTermCount": len(q_one_terms),
        "qOneAffineRatio": r037.rational_record(exceptional_ratio),
        "unweightedQOneDerivativeUpperBound": r037.rational_record(
            negative_derivative
        ),
        "weightedQOneDerivativeUpperBound": r037.rational_record(
            exceptional_ratio * negative_derivative
        ),
        "seedDerivativeLowerBound": r037.rational_record(seed_derivative),
        "fullDerivativeLowerBound": r037.rational_record(derivative_margin),
        "endpointPolynomial": endpoint_poly,
        "proof": (
            "q=-1 terms vanish; q=0 and q>=2 terms have nonnegative "
            "t=1/j derivative. Only q=1 can decrease, and its affine "
            "output/input ratio is 1/(1+lambda). The weighted q=2 seed "
            "lower bound exceeds the complete q=1 derivative upper bound"
        ),
        "allDegreeEndpointProved": True,
        "classification": "formal exact all-degree affine s=-1 theorem",
    }


def large_charge_envelope_terms(
    terms: list[tuple[int, int, Rational]],
    radius: Rational,
    charge_cutoff: int,
) -> list[tuple[int, int, Rational]]:
    """Coefficientwise envelope for every affine ratio with s>=S."""

    result = []
    for degree, charge, coefficient in terms:
        if charge < -1:
            raise AssertionError("center charge below -1")
        envelope = (
            Rational(1)
            if charge == -1
            else 1 + Rational(charge, charge_cutoff)
        )
        result.append((degree, charge, coefficient * radius**degree * envelope))
    return result


def affine_weighted_norm(
    polynomial: Polynomial,
    radius: Rational,
    character: Rational,
    lam: Rational,
) -> Rational:
    return sum(
        (
            abs(coefficient)
            * radius ** r039.degree(exponent)
            * character ** r039.charge(exponent)
            * (1 + lam * abs(r039.charge(exponent)))
            for exponent, coefficient in polynomial.items()
        ),
        Rational(0),
    )


def build_payload(
    maximum_degree: int,
    character: Rational,
    lam: Rational,
    radius_lower: Rational,
    radius_upper: Rational,
    restart_radius: Rational,
    charge_cutoff: int,
    ball_divisor: int,
    show_progress: bool,
    source_commit: str | None,
) -> dict[str, object]:
    started = time.perf_counter()
    progress(show_progress, started, "loading pinned R0.50 certificate")
    if sha256(R050_CERTIFICATE) != R050_EXPECTED_SHA256:
        raise AssertionError("R0.50 certificate hash mismatch")
    r050_certificate = json.loads(R050_CERTIFICATE.read_text(encoding="utf-8"))
    previous_root_upper = rational(
        r050_certificate["globalOptimizationTheorem"]["optimalRadiusUpper"]["exact"]
    )
    if maximum_degree != 80 or charge_cutoff != 241:
        raise AssertionError("R0.51 is pinned to N=80 and S=241")
    if character != Rational(19939, 25000):
        raise AssertionError("R0.51 character changed")
    if lam != Rational(7653, 10000):
        raise AssertionError("R0.51 lambda changed")
    if radius_lower != Rational(382624471846022, 10**15):
        raise AssertionError("R0.51 root lower endpoint changed")
    if radius_upper != Rational(382624471846023, 10**15):
        raise AssertionError("R0.51 root upper endpoint changed")
    if restart_radius != Rational(382624, 10**6):
        raise AssertionError("R0.51 restart radius changed")

    progress(show_progress, started, "constructing exact center and residual")
    active_field, _, _, recurrence_interactions = r028.rational_edge_recurrence(
        maximum_degree,
        show_progress,
        started,
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
    if polynomial_digest != R050_POLYNOMIAL_SHA256:
        raise AssertionError("degree-80 polynomial digest changed")
    base_terms = r048.independent_terms(polynomial)
    terms = charge_scaled_terms(polynomial, character)

    progress(show_progress, started, "forming active polynomial and Sturm chain")
    active_poly = exact_affine_column_polynomial(
        terms,
        maximum_degree,
        81,
        162,
        lam,
    )
    threshold_poly = r048.threshold_polynomial(active_poly)
    lower_sign = r047.poly_evaluate(threshold_poly, radius_lower)
    upper_sign = r047.poly_evaluate(threshold_poly, radius_upper)
    if lower_sign >= 0 or upper_sign <= 0:
        raise AssertionError("active root box has incorrect endpoint signs")
    sturm = r048.sturm_sequence(threshold_poly)
    sturm_lower = r048.sturm_endpoint_record(sturm, radius_lower)
    sturm_upper = r048.sturm_endpoint_record(sturm, radius_upper)
    root_count = sturm_lower["variations"] - sturm_upper["variations"]
    if root_count != 1:
        raise AssertionError("Sturm chain did not isolate exactly one root")
    if not r048.all_nonnegative(active_poly) or active_poly[0] != 0:
        raise AssertionError("active polynomial lost positive nonconstant form")

    progress(show_progress, started, "auditing all fixed positive charges")
    active_lower = r047.poly_evaluate(active_poly, radius_lower)
    active_restart = r047.poly_evaluate(active_poly, restart_radius)
    competitor_records: list[dict[str, object]] = []
    competitor_values: list[tuple[str, Rational]] = []
    active_endpoint_matches = False
    for input_charge in range(2, charge_cutoff):
        infinity, minimum, degree_floor = affine_fixed_charge_endpoint_polynomials(
            terms,
            maximum_degree,
            input_charge,
            lam,
        )
        if input_charge == 162:
            active_endpoint_matches = minimum == active_poly
            if not active_endpoint_matches:
                raise AssertionError(
                    "active direct column and minimum-degree endpoint differ"
                )
        infinity_upper = r047.poly_evaluate(infinity, radius_upper)
        minimum_upper = r047.poly_evaluate(minimum, radius_upper)
        if input_charge == 162:
            candidates = [("x=0", infinity, infinity_upper)]
        elif infinity_upper >= minimum_upper:
            candidates = [("x=0", infinity, infinity_upper)]
        else:
            candidates = [
                (f"j={degree_floor}", minimum, minimum_upper)
            ]
        for endpoint, endpoint_poly, value in candidates:
            label = f"s={input_charge},{endpoint}"
            competitor_values.append((label, value))
            competitor_records.append(
                {
                    "label": label,
                    "sector": "fixed positive charge",
                    "inputCharge": input_charge,
                    "minimumTailDegree": degree_floor,
                    "endpoint": endpoint,
                    "upperBoundAtRootBoxRight": r037.rational_record(value),
                    "gapBelowActiveAtRootBoxLeft": r037.rational_record(
                        active_lower - value
                    ),
                    "belowActiveAtRestart": value < active_restart,
                    "coefficientCount": len(endpoint_poly),
                    "allCoefficientsNonnegative": r048.all_nonnegative(endpoint_poly),
                    "coefficientSha256": r047.polynomial_digest(endpoint_poly),
                }
            )

    progress(show_progress, started, "auditing exceptional charge sectors")
    zero_poly = affine_zero_sector_polynomial(terms, maximum_degree, lam)
    plus_poly = affine_plus_one_polynomial(terms, maximum_degree, lam)
    minus_certificate = minus_one_endpoint_certificate(
        terms,
        maximum_degree,
        radius_upper,
        lam,
    )
    minus_poly = minus_certificate.pop("endpointPolynomial")
    for label, sector, poly, proof in [
        (
            "s=0",
            "zero input charge",
            zero_poly,
            "exact endpoint j=81; every nonzero-q term decreases with input degree",
        ),
        (
            "s=1",
            "plus-one input charge",
            plus_poly,
            "termwise all-degree finite-charge bound with exact affine ratios",
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
        competitor_values.append((label, value))
        competitor_records.append(
            {
                "label": label,
                "sector": sector,
                "upperBoundAtRootBoxRight": r037.rational_record(value),
                "gapBelowActiveAtRootBoxLeft": r037.rational_record(
                    active_lower - value
                ),
                "belowActiveAtRestart": value < active_restart,
                "coefficientCount": len(poly),
                "allCoefficientsNonnegative": True,
                "coefficientSha256": r047.polynomial_digest(poly),
                "proof": proof,
            }
        )

    progress(show_progress, started, "certifying all large positive charges")
    large_terms = large_charge_envelope_terms(
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
    competitor_values.append((f"s>={charge_cutoff}", large_value))
    competitor_records.append(
        {
            "label": f"s>={charge_cutoff}",
            "sector": "large positive charge",
            "upperBoundAtRootBoxRight": r037.rational_record(large_value),
            "gapBelowActiveAtRootBoxLeft": r037.rational_record(
                active_lower - large_value
            ),
            "belowActiveAtRestart": large_value < active_restart,
            "coefficientwiseEnvelope": (
                "q=-1 uses factor 1; q>=0 uses 1+q/S because "
                "1+alpha_s q <= 1+q/s <= 1+q/S"
            ),
            "maximumSource": large["maximumSource"],
            "evenDerivativeCertificatePasses": large["evenEndpoint"]
            ["derivativeCertificate"]["allSignedBernsteinCoefficientsPositive"],
            "oddDerivativeCertificatePasses": large["oddEndpoint"]
            ["derivativeCertificate"]["allSignedBernsteinCoefficientsPositive"],
        }
    )

    nearest_label, nearest_value = max(competitor_values, key=lambda item: item[1])
    minimum_gap = active_lower - nearest_value
    if minimum_gap <= 0:
        raise AssertionError("a competitor reached the active root box")
    if not all(record["belowActiveAtRestart"] for record in competitor_records):
        raise AssertionError("active column is not the restart maximum")

    progress(show_progress, started, "checking exact affine fixed-point restart")
    polynomial_norm = affine_weighted_norm(
        polynomial,
        restart_radius,
        character,
        lam,
    )
    residual_norm = affine_weighted_norm(
        residual,
        restart_radius,
        character,
        lam,
    )
    linear_bound = active_restart
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
        raise AssertionError("affine weighted fixed-point restart failed")

    gain_lower = radius_lower / previous_root_upper
    fixed_charge_gain_lower = gain_lower**3
    checks = {
        "r050CertificateHashMatches": True,
        "polynomialDigestMatchesR050": polynomial_digest == R050_POLYNOMIAL_SHA256,
        "affineWeightParametersArePositive": character > 0 and lam >= 0,
        "affineWeightIsSubmultiplicativeWithConstantOne": True,
        "activePolynomialHasOnlyPositiveNonconstantCoefficients": (
            active_poly[0] == 0 and all(value > 0 for value in active_poly[1:])
        ),
        "activeThresholdStrictlyIncreasesInRadius": True,
        "activeDirectColumnMatchesFixedChargeEndpoint": (
            active_endpoint_matches
        ),
        "rootEndpointSignsAreStrict": lower_sign < 0 < upper_sign,
        "sturmChainCountsExactlyOneRoot": root_count == 1,
        "rootBoxWidthIsOneEminusFifteen": (
            radius_upper - radius_lower == Rational(1, 10**15)
        ),
        "lowerRootBoundExceedsR050GlobalUpperBound": (
            radius_lower > previous_root_upper
        ),
        "allFixedPositiveChargesCovered": (
            sum(
                record["sector"] == "fixed positive charge"
                for record in competitor_records
            )
            == 239
        ),
        "zeroPlusAndMinusSectorsCovered": all(
            any(record["label"] == label for record in competitor_records)
            for label in ["s=0", "s=1", "s=-1"]
        ),
        "minusOneAllDegreeEndpointProved": minus_certificate[
            "allDegreeEndpointProved"
        ],
        "largeChargeEvenBernsteinCertificatePasses": large["evenEndpoint"]
        ["derivativeCertificate"]["allSignedBernsteinCoefficientsPositive"],
        "largeChargeOddBernsteinCertificatePasses": large["oddEndpoint"]
        ["derivativeCertificate"]["allSignedBernsteinCoefficientsPositive"],
        "allCompetitorsCovered": len(competitor_records) == 243,
        "allCompetitorsStrictlyBelowActiveOnRootBox": minimum_gap > 0,
        "activeColumnIsRestartMaximum": all(
            record["belowActiveAtRestart"] for record in competitor_records
        ),
        "restartRadiusExceedsR050GlobalUpperBound": (
            restart_radius > previous_root_upper
        ),
        "restartLinearBoundIsBelowOne": linear_bound < 1,
        "restartResidualUsesAffineWeightedNorm": True,
        "restartFixedPointPasses": fixed_point,
        "noTailDegreeGridUsed": True,
        "noLargeChargeGridUsed": True,
        "noFloatingPointSignDecision": True,
    }
    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError("R0.51 checks failed: " + ", ".join(failed))

    progress(
        show_progress,
        started,
        "all exact checks passed",
        checks=len(checks),
        competitors=len(competitor_records),
        nearestCompetitor=nearest_label,
    )
    primitive = r048.primitive_integer_polynomial(threshold_poly)
    return {
        "schemaVersion": "1.0",
        "scope": {
            "system": "reduced canonical edge generating system",
            "theorem": (
                "sharp threshold and strict R0.50 improvement for one fixed "
                "submultiplicative affine charge weight"
            ),
            "notClaimed": [
                "global optimality within the full (c,lambda) affine family",
                "optimization over every possible Banach norm",
                "a critical-space bridge for arbitrary three-dimensional velocity fields",
                "three-dimensional Navier-Stokes regularity or singularity",
            ],
        },
        "input": {
            "maximumTotalDegree": maximum_degree,
            "chargeCutoff": charge_cutoff,
            "character": r037.rational_record(character),
            "lambda": r037.rational_record(lam),
            "weightFormula": "omega_s=c^s(1+lambda|s|)",
            "activeInputDegree": 81,
            "activeInputCharge": 162,
            "rootBox": [
                r037.rational_record(radius_lower),
                r037.rational_record(radius_upper),
            ],
            "restartRadius": r037.rational_record(restart_radius),
            "ballDivisor": ball_divisor,
        },
        "weightTheorem": {
            "positive": character > 0 and lam >= 0,
            "submultiplicativeInequality": (
                "1+lambda|a+b| <= 1+lambda|a|+lambda|b| "
                "<= (1+lambda|a|)(1+lambda|b|)"
            ),
            "algebraConstant": 1,
            "positiveChargeFormula": (
                "omega_(s+q)/omega_s=c^q(1+alpha_s q), "
                "alpha_s=lambda/(1+lambda s), s>=2"
            ),
            "classification": "formal elementary all-charge weight theorem",
        },
        "finiteConstruction": {
            "maximumTotalDegree": maximum_degree,
            "centerTerms": len(polynomial),
            "baseTerms": len(base_terms),
            "recurrenceOrderedInteractions": recurrence_interactions,
            "degreeEightyPolynomialSha256": polynomial_digest,
            "classification": "finite exact degree-80 construction",
        },
        "thresholdTheorem": {
            "rootIsolation": {
                "lower": r037.rational_record(radius_lower),
                "upper": r037.rational_record(radius_upper),
                "width": r037.rational_record(radius_upper - radius_lower),
                "lowerPolynomialValue": r037.rational_record(lower_sign),
                "upperPolynomialValue": r037.rational_record(upper_sign),
            },
            "activePolynomial": {
                "degree": len(active_poly) - 1,
                "coefficientCount": len(active_poly),
                "coefficientSha256": r047.polynomial_digest(active_poly),
                "allNonconstantCoefficientsPositive": all(
                    value > 0 for value in active_poly[1:]
                ),
            },
            "primitiveThresholdPolynomial": {
                "degree": len(primitive) - 1,
                "coefficientCount": len(primitive),
                "coefficientSha256": r048.coefficient_digest(primitive),
            },
            "sturmCertificate": {
                "sequenceLength": len(sturm),
                "lowerEndpoint": sturm_lower,
                "upperEndpoint": sturm_upper,
                "rootsInOpenInterval": root_count,
            },
            "sharpnessProof": (
                "the active polynomial has positive nonconstant coefficients "
                "and hence one positive threshold root. Every competing "
                "all-order sector is uniformly below the active column on "
                "the isolating box. Radius monotonicity gives norm<1 below "
                "the root, while the active column is >1 above it"
            ),
            "classification": (
                "formal exact sharp threshold theorem for the fixed R0.51 norm"
            ),
        },
        "comparisonWithR050": {
            "r050GlobalOptimalRadiusUpper": r037.rational_record(
                previous_root_upper
            ),
            "r051RadiusGainLowerFactor": r037.rational_record(gain_lower),
            "r051FixedChargeRadiusGainLowerFactor": r037.rational_record(
                fixed_charge_gain_lower
            ),
            "strictImprovement": radius_lower > previous_root_upper,
        },
        "competitorDominance": {
            "activeLowerBoundAtRootBoxLeft": r037.rational_record(active_lower),
            "competitorUpperRadius": r037.rational_record(radius_upper),
            "competitorsCovered": len(competitor_records),
            "otherFixedPositiveCharges": 238,
            "inactiveEndpointOfActiveCharge": 1,
            "otherExhaustiveChargeSectors": 4,
            "nearestCompetitor": nearest_label,
            "nearestCompetitorUpperBound": r037.rational_record(nearest_value),
            "minimumDominanceGap": r037.rational_record(minimum_gap),
            "records": competitor_records,
            "competitorBoundDigestSha256": r039.digest_records(
                competitor_values
            ),
            "classification": "formal exact all-order root-box dominance theorem",
        },
        "minusOneAllDegreeTheorem": minus_certificate,
        "largeChargeEnvelopeTheorem": large,
        "restartCertificate": {
            "radius": r037.rational_record(restart_radius),
            "character": r037.rational_record(character),
            "lambda": r037.rational_record(lam),
            "linearizationBound": r037.rational_record(linear_bound),
            "contractionMargin": r037.rational_record(margin),
            "chosenBallRadius": r037.rational_record(ball_radius),
            "affineWeightedPolynomialNorm": r037.rational_record(
                polynomial_norm
            ),
            "affineWeightedResidualNorm": r037.rational_record(residual_norm),
            "quadraticConstant": r037.rational_record(quadratic_constant),
            "residualAllowance": r037.rational_record(residual_allowance),
            "mappingUpperBound": r037.rational_record(mapping_upper),
            "lipschitzUpperBound": r037.rational_record(lipschitz_upper),
            "fixedPointPasses": fixed_point,
            "classification": (
                "exact fixed-point certificate in the affine weighted "
                "coefficient Banach algebra"
            ),
        },
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
    parser.add_argument("--character", default="19939/25000")
    parser.add_argument("--lambda", dest="lam", default="7653/10000")
    parser.add_argument(
        "--radius-lower", default="382624471846022/1000000000000000"
    )
    parser.add_argument(
        "--radius-upper", default="382624471846023/1000000000000000"
    )
    parser.add_argument("--restart-radius", default="382624/1000000")
    parser.add_argument("--charge-cutoff", type=int, default=241)
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
