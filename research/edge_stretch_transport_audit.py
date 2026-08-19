#!/usr/bin/env python3
"""R0.42 exact canonical-stretch transport audit.

R0.40 bounded the normalized transport fields directly with

    T_a = (L-1)^(-1) {a, .}.

At r=141/500 the exact x=2 polynomial column of T_a is already larger
than one.  The R0.29 canonical identities give a different, equivalent
construction:

    U = Z exp(phi-a/2),   V = W exp(phi+a/2),
    L phi - {a,phi} = (X-Y)a/2.

Thus only the zero-initial stretch phi must be inverted.  On the
degree-weighted Wiener space its operator is

    S_a = L^(-1) {a, .}.

For a base monomial (i,q) and an input monomial (j,s), the exact weighted
column factor is |i(s/j)-q|/3.  The complete column is convex in the common
input slope x=s/j in [-1,2], and unlike T_a it has no degree prefactor.
Consequently its all-order norm is the maximum of two genuine endpoint
columns.  The unknown active correction is handled by explicit endpoint
multipliers.

All threshold decisions use exact GMP rationals.  Finite coefficient and
column regressions check the implementation only.  The theorem concerns the
reduced canonical edge system and does not prove three-dimensional
Navier--Stokes regularity or singularity.
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

import edge_canonical_transport_audit as r029
import edge_degree_resolved_tail_audit as r041
import edge_rational_asymptotic_audit as r028
import edge_short_continuation_audit as r036
import edge_slope_resolved_transport_audit as r040
import edge_weighted_restart_audit as r037
import edge_charge_resolved_audit as r039


Rational = gmpy2.mpq
Exponent = tuple[int, int]
Polynomial = dict[Exponent, Rational]
Layer = list[Rational]
Field = list[Layer | None]

R041_CERTIFICATE = Path(
    "research/certificates/r041/edge-degree-resolved-tail.json"
)
R041_EXPECTED_SHA256 = (
    "1eb4bbe5f7e53e9eacf7f445b716194ab492603a7de35884549e9c7def640653"
)
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(
            f"[R0.42 +{elapsed:8.2f}s] {stage}{suffix}",
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


def stretch_monomial_coefficient(
    base_degree: int,
    base_charge: int,
    input_degree: int,
    input_charge: int,
) -> Rational:
    """Coefficient of one monomial pair in L^(-1){a,f}."""

    return Rational(
        base_degree * input_charge - base_charge * input_degree,
        3 * (base_degree + input_degree),
    )


def stretch_endpoint_factor(
    base_degree: int,
    base_charge: int,
    input_slope: int,
) -> Rational:
    """Weighted B_r column factor at x=-1 or x=2."""

    if input_slope not in (-1, 2):
        raise AssertionError("stretch endpoint slope must be -1 or 2")
    return Rational(
        abs(base_degree * input_slope - base_charge),
        3,
    )


def polynomial_stretch_endpoint_bounds(
    polynomial: Polynomial,
    radius: Rational,
) -> dict[str, object]:
    """Exact all-order endpoint norm for the finite polynomial center."""

    records = []
    for label, slope in (("x=-1", -1), ("x=2", 2)):
        value = sum(
            (
                abs(coefficient)
                * radius ** r039.degree(exponent)
                * stretch_endpoint_factor(
                    r039.degree(exponent),
                    r039.charge(exponent),
                    slope,
                )
                for exponent, coefficient in polynomial.items()
            ),
            Rational(0),
        )
        records.append(
            {
                "label": label,
                "inputSlope": slope,
                "bound": r037.rational_record(value),
            }
        )
    maximum = max(records, key=lambda item: rational(item["bound"]["exact"]))
    return {
        "endpointColumns": records,
        "maximumBound": maximum["bound"],
        "maximumEndpoint": maximum["label"],
        "classification": (
            "exact induced weighted-l1 norm of the polynomial stretch "
            "operator; complete-column convexity covers every input slope "
            "and the cancellation of the output degree leaves no input-degree "
            "prefactor"
        ),
    }


def stretch_tail_endpoint_constants(cutoff: int) -> dict[str, Rational]:
    """Endpoint multipliers for an active correction supported above N."""

    first_tail_degree = cutoff + 1
    return {
        "x=-1": Rational(1),
        "x=2": Rational(
            2 * first_tail_degree + 1,
            3 * first_tail_degree,
        ),
    }


def stretch_operator_bound(
    polynomial: Polynomial,
    radius: Rational,
    cutoff: int,
    correction_norm_bound: Rational,
) -> dict[str, object]:
    polynomial_bounds = polynomial_stretch_endpoint_bounds(polynomial, radius)
    constants = stretch_tail_endpoint_constants(cutoff)
    totals = []
    for record in polynomial_bounds["endpointColumns"]:
        label = record["label"]
        polynomial_value = rational(record["bound"]["exact"])
        correction = constants[label] * correction_norm_bound
        totals.append(
            {
                **record,
                "tailMultiplier": r037.rational_record(constants[label]),
                "tailContributionUpperBound": r037.rational_record(correction),
                "totalBound": r037.rational_record(polynomial_value + correction),
            }
        )
    maximum = max(
        totals,
        key=lambda item: rational(item["totalBound"]["exact"]),
    )
    return {
        "endpointColumns": totals,
        "maximumPolynomialBound": polynomial_bounds["maximumBound"],
        "maximumPolynomialEndpoint": polynomial_bounds["maximumEndpoint"],
        "maximumTotalBound": maximum["totalBound"],
        "maximumTotalEndpoint": maximum["label"],
        "tailHypothesis": f"active correction supported on degrees >{cutoff}",
        "classification": (
            "all-order two-endpoint bound for S_a=L^(-1){a,.}, including "
            "the unknown active correction"
        ),
    }


def stretch_rhs_bound(
    polynomial: Polynomial,
    radius: Rational,
    correction_norm_bound: Rational,
) -> dict[str, object]:
    """Bound b=L^(-1)(X-Y)a/2 in the degree-weighted Wiener norm."""

    polynomial_value = sum(
        (
            abs(coefficient)
            * radius ** r039.degree(exponent)
            * Rational(
                abs(r039.degree(exponent) - 2 * r039.charge(exponent)),
                6,
            )
            for exponent, coefficient in polynomial.items()
        ),
        Rational(0),
    )
    tail_multiplier = Rational(1, 2)
    tail_contribution = tail_multiplier * correction_norm_bound
    return {
        "polynomialBound": r037.rational_record(polynomial_value),
        "tailMultiplier": r037.rational_record(tail_multiplier),
        "tailContributionUpperBound": r037.rational_record(tail_contribution),
        "totalBound": r037.rational_record(polynomial_value + tail_contribution),
        "proof": (
            "X-Y multiplies degree-charge (i,q) by (i-2q)/3; after L^(-1) "
            "and the B_r output weight cancel, the column factor is "
            "|i-2q|/6, at most i/2 on the active cone"
        ),
    }


def exact_stretch_column(
    polynomial: Polynomial,
    radius: Rational,
    input_degree: int,
    input_charge: int,
) -> Rational:
    """Exact weighted-l1 column ratio for one stretch input monomial."""

    return sum(
        (
            Rational(r039.degree(exponent) + input_degree, input_degree)
            * abs(
                stretch_monomial_coefficient(
                    r039.degree(exponent),
                    r039.charge(exponent),
                    input_degree,
                    input_charge,
                )
            )
            * abs(coefficient)
            * radius ** r039.degree(exponent)
            for exponent, coefficient in polynomial.items()
        ),
        Rational(0),
    )


def finite_stretch_column_scan(
    polynomial: Polynomial,
    radius: Rational,
    input_degree: int,
) -> dict[str, object]:
    """Finite column regression; the theorem itself is all-order."""

    columns = []
    for input_w_degree in range(input_degree + 1):
        input_charge = 3 * input_w_degree - input_degree
        columns.append(
            (
                input_charge,
                exact_stretch_column(
                    polynomial,
                    radius,
                    input_degree,
                    input_charge,
                ),
            )
        )
    maximum_charge, maximum_value = max(columns, key=lambda item: item[1])
    return {
        "inputDegree": input_degree,
        "admissibleColumns": len(columns),
        "maximumColumnCharge": maximum_charge,
        "maximumInputSlope": r037.rational_record(
            Rational(maximum_charge, input_degree)
        ),
        "maximumWeightedColumnRatio": r037.rational_record(maximum_value),
        "classification": "finite exact stretch-column regression only",
    }


def stretch_formula_regression(maximum_degree: int) -> dict[str, object]:
    """Compare the closed coefficient with L^(-1) applied to the bracket."""

    active_base = [
        (total_degree - w_degree, w_degree)
        for total_degree in range(1, maximum_degree + 1)
        for w_degree in range(total_degree + 1)
        if 3 * w_degree - total_degree >= -1
    ]
    full_input = [
        (total_degree - w_degree, w_degree)
        for total_degree in range(1, maximum_degree + 1)
        for w_degree in range(total_degree + 1)
    ]
    checked = 0
    zero_images = 0
    for base_exponent in active_base:
        for input_exponent in full_input:
            expected_exponent = (
                base_exponent[0] + input_exponent[0],
                base_exponent[1] + input_exponent[1],
            )
            expected = stretch_monomial_coefficient(
                r039.degree(base_exponent),
                r039.charge(base_exponent),
                r039.degree(input_exponent),
                r039.charge(input_exponent),
            )
            image = r036.inverse_l(
                r036.bracket(
                    {base_exponent: Rational(1)},
                    {input_exponent: Rational(1)},
                )
            )
            if image.get(expected_exponent, Rational(0)) != expected:
                raise AssertionError("stretch coefficient formula mismatch")
            if any(exponent != expected_exponent for exponent in image):
                raise AssertionError("stretch monomial produced another exponent")
            if not image:
                zero_images += 1
            checked += 1
    return {
        "maximumInputDegree": maximum_degree,
        "activeBaseDimension": len(active_base),
        "fullInputDimension": len(full_input),
        "orderedPairsChecked": checked,
        "zeroImages": zero_images,
        "passed": True,
        "classification": "finite exact implementation regression",
    }


def stretch_series(active: Field, maximum_degree: int) -> list[Layer]:
    """Solve L phi-{a,phi}=(X-Y)a/2 through a finite degree."""

    zero = Rational(0)
    phi = [[zero]] + [
        [zero] * (degree + 1) for degree in range(1, maximum_degree + 1)
    ]
    for degree in range(1, maximum_degree + 1):
        active_layer = active[degree]
        if active_layer is None:
            raise AssertionError("missing active layer in stretch regression")
        numerator = [
            Rational(degree - 2 * w_degree, 2) * coefficient
            for w_degree, coefficient in enumerate(active_layer)
        ]
        for base_degree in range(1, degree):
            input_degree = degree - base_degree
            base_layer = active[base_degree]
            input_layer = phi[input_degree]
            if base_layer is None:
                raise AssertionError("missing active layer")
            for base_w, base_value in enumerate(base_layer):
                if base_value == 0:
                    continue
                for input_w, input_value in enumerate(input_layer):
                    if input_value == 0:
                        continue
                    determinant = (
                        base_degree * input_w - base_w * input_degree
                    )
                    numerator[base_w + input_w] += (
                        determinant * base_value * input_value
                    )
        phi[degree] = [value / degree for value in numerator]
    return phi


def field_linear_combination(
    left: list[Layer],
    right: Field,
    right_scale: Rational,
    maximum_degree: int,
) -> list[Layer]:
    output = [[Rational(0)]]
    for degree in range(1, maximum_degree + 1):
        right_layer = right[degree]
        if right_layer is None:
            raise AssertionError("missing field layer")
        output.append(
            [
                left[degree][index] + right_scale * right_layer[index]
                for index in range(degree + 1)
            ]
        )
    return output


def exp_field(field: list[Layer], maximum_degree: int) -> list[Layer]:
    """Return exp(field) for a zero-constant finite series."""

    zero = Rational(0)
    exponential = [[Rational(1)]] + [
        [zero] * (degree + 1) for degree in range(1, maximum_degree + 1)
    ]
    for degree in range(1, maximum_degree + 1):
        numerator = [zero] * (degree + 1)
        for field_degree in range(1, degree + 1):
            exponential_degree = degree - field_degree
            for field_w, field_value in enumerate(field[field_degree]):
                if field_value == 0:
                    continue
                for exponential_w, exponential_value in enumerate(
                    exponential[exponential_degree]
                ):
                    if exponential_value != 0:
                        numerator[field_w + exponential_w] += (
                            field_degree * field_value * exponential_value
                        )
        exponential[degree] = [value / degree for value in numerator]
    return exponential


def factorization_regression(
    active: Field,
    u: Field,
    v: Field,
    maximum_degree: int,
) -> dict[str, object]:
    """Check U=Z exp(phi-a/2), V=W exp(phi+a/2) finitely."""

    phi = stretch_series(active, maximum_degree)
    minus = field_linear_combination(
        phi, active, Rational(-1, 2), maximum_degree
    )
    plus = field_linear_combination(
        phi, active, Rational(1, 2), maximum_degree
    )
    exp_minus = exp_field(minus, maximum_degree)
    exp_plus = exp_field(plus, maximum_degree)
    coefficient_checks = 0
    divisibility_checks = 0
    for quotient_degree in range(0, maximum_degree):
        field_degree = quotient_degree + 1
        u_layer = u[field_degree]
        v_layer = v[field_degree]
        if u_layer is None or v_layer is None:
            raise AssertionError("missing transport layer")
        if u_layer[field_degree] != 0:
            raise AssertionError("U is not divisible by Z")
        if v_layer[0] != 0:
            raise AssertionError("V is not divisible by W")
        divisibility_checks += 2
        for quotient_w in range(quotient_degree + 1):
            normalized_u = -12 * u_layer[quotient_w]
            normalized_v = -3 * v_layer[quotient_w + 1]
            if normalized_u != exp_minus[quotient_degree][quotient_w]:
                raise AssertionError("U stretch factorization mismatch")
            if normalized_v != exp_plus[quotient_degree][quotient_w]:
                raise AssertionError("V stretch factorization mismatch")
            coefficient_checks += 2
    return {
        "maximumTransportDegree": maximum_degree,
        "coefficientChecks": coefficient_checks,
        "divisibilityChecks": divisibility_checks,
        "stretchSha256": r029.field_digest(phi),
        "expMinusSha256": r029.field_digest(exp_minus),
        "expPlusSha256": r029.field_digest(exp_plus),
        "passed": True,
        "classification": (
            "finite exact factorization regression; the all-order identity "
            "comes from the R0.29 formal theorem and triangular uniqueness"
        ),
    }


def restart_diagnostics(
    polynomial: Polynomial,
    residual: Polynomial,
    radius: Rational,
    tail: dict[str, object],
    cutoff: int,
    ball_divisor: int,
) -> dict[str, object]:
    tail_bound = rational(tail["maximumBound"]["exact"])
    margin = 1 - tail_bound
    ball_radius = margin / ball_divisor if margin > 0 else Rational(0)
    polynomial_norm = r037.weighted_wiener_norm(polynomial, radius)
    residual_norm = r037.weighted_wiener_norm(residual, radius)
    residual_allowance = margin * ball_radius - 3 * ball_radius**2
    mapping_upper = (
        residual_norm + tail_bound * ball_radius + 3 * ball_radius**2
    )
    lipschitz_upper = tail_bound + 6 * ball_radius
    stretch = stretch_operator_bound(
        polynomial,
        radius,
        cutoff,
        ball_radius,
    )
    stretch_bound = rational(stretch["maximumTotalBound"]["exact"])
    rhs = stretch_rhs_bound(polynomial, radius, ball_radius)
    rhs_bound = rational(rhs["totalBound"]["exact"])
    stretch_inverse = (
        Rational(1, 1) / (1 - stretch_bound)
        if stretch_bound < 1
        else None
    )
    phi_bound = rhs_bound * stretch_inverse if stretch_inverse is not None else None
    direct_transport = r040.slope_resolved_transport_bound(
        polynomial,
        radius,
        cutoff,
        ball_radius,
    )
    direct_transport_bound = rational(
        direct_transport["maximumTotalBound"]["exact"]
    )
    fixed_point_passes = (
        margin > 0
        and ball_radius > 0
        and residual_norm < residual_allowance
        and mapping_upper < ball_radius
        and lipschitz_upper < 1
    )
    return {
        "radius": r037.rational_record(radius),
        "tailLinearizationBound": r037.rational_record(tail_bound),
        "tailMaximumSector": tail["maximumSector"],
        "contractionMargin": r037.rational_record(margin),
        "ballDivisor": ball_divisor,
        "chosenBallRadius": r037.rational_record(ball_radius),
        "degreeEightyPolynomialNorm": r037.rational_record(polynomial_norm),
        "exactResidualNorm": r037.rational_record(residual_norm),
        "residualAllowance": r037.rational_record(residual_allowance),
        "mappingUpperBound": r037.rational_record(mapping_upper),
        "lipschitzUpperBound": r037.rational_record(lipschitz_upper),
        "stretchOperator": stretch,
        "stretchOperatorBound": r037.rational_record(stretch_bound),
        "stretchInverseNormUpperBound": (
            r037.rational_record(stretch_inverse)
            if stretch_inverse is not None
            else None
        ),
        "stretchRightHandSide": rhs,
        "stretchSolutionNormUpperBound": (
            r037.rational_record(phi_bound) if phi_bound is not None else None
        ),
        "directTransportComparison": direct_transport,
        "directTransportBound": r037.rational_record(direct_transport_bound),
        "fixedPointPasses": fixed_point_passes,
        "stretchPasses": stretch_bound < 1,
        "canonicalFieldsPass": fixed_point_passes and stretch_bound < 1,
    }


def build_payload(
    maximum_degree: int,
    target_radius: Rational,
    acceptance_radius: Rational,
    failure_probe_radius: Rational,
    charge_cutoff: int,
    finite_column_degrees: list[int],
    formula_regression_degree: int,
    factorization_degree: int,
    ball_divisor: int,
    show_progress: bool,
    source_commit: str | None,
) -> dict[str, object]:
    started = time.perf_counter()
    progress(show_progress, started, "loading pinned R0.41 certificate")
    if sha256(R041_CERTIFICATE) != R041_EXPECTED_SHA256:
        raise AssertionError("R0.41 certificate hash mismatch")
    r041_certificate = json.loads(R041_CERTIFICATE.read_text(encoding="utf-8"))
    previous_radius = rational(
        r041_certificate["restartCertificate"]["radius"]["exact"]
    )
    preassigned_acceptance = rational(
        r041_certificate["negativeControl"]["radius"]["exact"]
    )
    pinned_direct_failure = rational(
        r041_certificate["negativeControl"]["transportBound"]["exact"]
    )

    progress(
        show_progress,
        started,
        "constructing exact degree recurrence",
        maximumDegree=maximum_degree,
    )
    active, u, v, recurrence_interactions = r028.rational_edge_recurrence(
        maximum_degree,
        show_progress,
        started,
    )
    polynomial = r036.field_to_polynomial(active, maximum_degree)
    if any(r039.charge(exponent) < -1 for exponent in polynomial):
        raise AssertionError("polynomial left the active support cone")

    seed = {(1, 0): Rational(1), (0, 1): Rational(1)}
    progress(
        show_progress,
        started,
        "forming complete polynomial residual",
        maximumResidualDegree=2 * maximum_degree,
    )
    residual = r036.add(
        polynomial,
        r036.scale(seed, -1),
        r036.scale(r036.phi(polynomial), -1),
    )
    if r036.truncate(residual, maximum_degree):
        raise AssertionError("degree recurrence has a residual below the cutoff")
    residual_degrees = sorted({r039.degree(exponent) for exponent in residual})

    restarts: dict[str, dict[str, object]] = {}
    tails: dict[str, dict[str, object]] = {}
    for label, radius in (
        ("acceptance", acceptance_radius),
        ("target", target_radius),
        ("failureProbe", failure_probe_radius),
    ):
        progress(
            show_progress,
            started,
            "forming all-order active and stretch bounds",
            label=label,
            radius=str(radius),
        )
        tail = r041.degree_resolved_tail_bound(
            polynomial,
            radius,
            maximum_degree,
            charge_cutoff,
        )
        tails[label] = tail
        restarts[label] = restart_diagnostics(
            polynomial,
            residual,
            radius,
            tail,
            maximum_degree,
            ball_divisor,
        )

    progress(
        show_progress,
        started,
        "checking exact stretch coefficient formula",
        maximumDegree=formula_regression_degree,
    )
    formula_regression = stretch_formula_regression(formula_regression_degree)
    finite_columns = []
    for input_degree in finite_column_degrees:
        progress(
            show_progress,
            started,
            "auditing finite exact stretch columns",
            inputDegree=input_degree,
        )
        finite_columns.append(
            finite_stretch_column_scan(
                polynomial,
                target_radius,
                input_degree,
            )
        )

    progress(
        show_progress,
        started,
        "checking canonical exponential factorization",
        maximumDegree=factorization_degree,
    )
    factorization = factorization_regression(
        active,
        u,
        v,
        factorization_degree,
    )

    acceptance = restarts["acceptance"]
    target = restarts["target"]
    failure = restarts["failureProbe"]
    polynomial_digest = r037.polynomial_digest(polynomial)
    residual_digest = r037.polynomial_digest(residual)
    target_endpoint_bound = rational(
        target["stretchOperator"]["maximumPolynomialBound"]["exact"]
    )

    checks = {
        "r041CertificateHashMatches": True,
        "r041FailureBecomesAcceptanceTest": (
            acceptance_radius == preassigned_acceptance
        ),
        "pinnedDirectFailureMatches": (
            rational(acceptance["directTransportBound"]["exact"])
            == pinned_direct_failure
        ),
        "acceptanceDirectTransportFails": (
            rational(acceptance["directTransportBound"]["exact"]) > 1
        ),
        "acceptanceStretchConstructionPasses": acceptance["canonicalFieldsPass"],
        "targetExceedsR041": target_radius > previous_radius,
        "targetActiveFixedPointPasses": target["fixedPointPasses"],
        "targetStretchPasses": target["stretchPasses"],
        "targetCanonicalFieldsPass": target["canonicalFieldsPass"],
        "targetDirectTransportFails": (
            rational(target["directTransportBound"]["exact"]) > 1
        ),
        "failureProbeIsNextMillesimal": (
            failure_probe_radius - target_radius == Rational(1, 1000)
        ),
        "failureProbeActiveTailFails": (
            rational(failure["tailLinearizationBound"]["exact"]) > 1
        ),
        "failureProbePolynomialStretchStillPasses": (
            rational(
                failure["stretchOperator"]["maximumPolynomialBound"]["exact"]
            )
            < 1
        ),
        "targetWorstActiveSectorIsLargeCharge": (
            tails["target"]["maximumSector"] == f">={charge_cutoff}"
        ),
        "targetWorstStretchEndpointIsTwo": (
            target["stretchOperator"]["maximumTotalEndpoint"] == "x=2"
        ),
        "closedStretchCoefficientFormulaExact": formula_regression["passed"],
        "allInputSlopesCoveredByConvexEndpointReduction": True,
        "allInputDegreesCoveredWithoutPrefactor": True,
        "tailEndpointConstantsExact": (
            stretch_tail_endpoint_constants(maximum_degree)["x=-1"] == 1
            and stretch_tail_endpoint_constants(maximum_degree)["x=2"]
            == Rational(163, 243)
        ),
        "finiteColumnRegressionsBelowTheorem": all(
            rational(column["maximumWeightedColumnRatio"]["exact"])
            <= target_endpoint_bound
            for column in finite_columns
        ),
        "finiteColumnsAttainEndpointTheorem": all(
            rational(column["maximumWeightedColumnRatio"]["exact"])
            == target_endpoint_bound
            for column in finite_columns
        ),
        "canonicalFactorizationRegressionPasses": factorization["passed"],
        "polynomialDigestMatchesR041": (
            polynomial_digest
            == r041_certificate["restartCertificate"][
                "degreeEightyPolynomialSha256"
            ]
        ),
        "residualDigestMatchesR041": (
            residual_digest
            == r041_certificate["restartCertificate"]["exactResidualSha256"]
        ),
        "residualStartsAboveCutoff": (
            residual_degrees and residual_degrees[0] == maximum_degree + 1
        ),
        "residualEndsAtDoubleCutoff": (
            residual_degrees and residual_degrees[-1] == 2 * maximum_degree
        ),
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise AssertionError(f"R0.42 checks failed: {failed}")

    elapsed = time.perf_counter() - started
    progress(
        show_progress,
        started,
        "all exact checks passed",
        checks=len(checks),
        targetRadius=str(target_radius),
        targetTail=target["tailLinearizationBound"]["exact"],
        targetStretch=target["stretchOperatorBound"]["exact"],
    )

    return {
        "scope": {
            "system": "reduced canonical edge generating system",
            "claim": (
                "all-order canonical-stretch transport theorem and exact "
                "common radius restart at 329/1000"
            ),
            "notClaimed": [
                "three-dimensional Navier-Stokes global regularity",
                "finite-time blow-up",
                "a singularity at the failed probe",
                "an all-order theorem from finite coefficient checks",
            ],
        },
        "git": r039.git_state(source_commit),
        "input": {
            "r041": {
                "path": str(R041_CERTIFICATE),
                "sha256": R041_EXPECTED_SHA256,
                "sourceCommit": r041_certificate["git"]["commit"],
            }
        },
        "allOrderTheorem": {
            "canonicalFactorization": (
                "U=Z exp(phi-a/2), V=W exp(phi+a/2)"
            ),
            "stretchEquation": "L phi-{a,phi}=(X-Y)a/2",
            "stretchOperator": "S_a=L^(-1){a,.}",
            "exactColumnFactor": "|i*(s/j)-q|/3",
            "inputSlopeRange": "x=s/j in [-1,2]",
            "convexity": (
                "the complete polynomial column is a positive sum of absolute "
                "affine functions of the common slope x"
            ),
            "degreeCancellation": (
                "the B_r output weight cancels the L^(-1) divisor exactly, "
                "so the column has no input-degree prefactor"
            ),
            "tailEndpointMultipliers": {
                label: r037.rational_record(value)
                for label, value in stretch_tail_endpoint_constants(
                    maximum_degree
                ).items()
            },
            "rhsTailMultiplier": r037.rational_record(Rational(1, 2)),
            "degreeCoverage": "every positive input degree",
            "chargeCoverage": "every bivariate input charge -j<=s<=2j",
            "classification": "formal all-order theorem",
        },
        "acceptanceTest": {
            **acceptance,
            "preassignedByR041": True,
            "classification": (
                "the R0.41 direct-transport failure passes through the "
                "equivalent canonical-stretch construction"
            ),
        },
        "restartCertificate": {
            **target,
            "previousRadius": r037.rational_record(previous_radius),
            "radiusGainFromR041": r037.rational_record(
                target_radius / previous_radius
            ),
            "fixedChargeGainFromR041": r037.rational_record(
                (target_radius / previous_radius) ** 3
            ),
            "polynomialCutoff": maximum_degree,
            "chargeCutoff": charge_cutoff,
            "degreeEightyPolynomialTerms": len(polynomial),
            "degreeEightyPolynomialSha256": polynomial_digest,
            "exactResidualTerms": len(residual),
            "exactResidualSha256": residual_digest,
            "residualDegreeRange": [residual_degrees[0], residual_degrees[-1]],
            "statement": (
                "the active Banach restart constructs a at radius 329/1000; "
                "the canonical-stretch Neumann inverse constructs phi, and "
                "the exact exponentials construct the canonical U and V"
            ),
        },
        "negativeControl": {
            **failure,
            "classification": (
                "the next millesimal radius fails the present all-order active "
                "tail inequality while the degree-80 polynomial stretch "
                "operator remains below one; this is not evidence of a "
                "singularity or loss of analyticity"
            ),
        },
        "finiteRegression": {
            "stretchCoefficientFormula": formula_regression,
            "stretchColumns": finite_columns,
            "canonicalFactorization": factorization,
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


def parse_degree_list(value: str) -> list[int]:
    try:
        degrees = [int(item.strip()) for item in value.split(",") if item.strip()]
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from error
    if not degrees:
        raise argparse.ArgumentTypeError("at least one degree is required")
    return degrees


def main() -> None:
    global PROGRESS_LOG
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-total-degree", type=int, default=80)
    parser.add_argument("--target-radius", default="329/1000")
    parser.add_argument("--acceptance-radius", default="141/500")
    parser.add_argument("--failure-probe-radius", default="33/100")
    parser.add_argument("--charge-cutoff", type=int, default=241)
    parser.add_argument(
        "--finite-column-degrees",
        type=parse_degree_list,
        default=parse_degree_list("1,2,5,20,81"),
    )
    parser.add_argument("--formula-regression-degree", type=int, default=10)
    parser.add_argument("--factorization-degree", type=int, default=30)
    parser.add_argument("--ball-divisor", type=int, default=1_000_000)
    parser.add_argument("--source-commit")
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--progress-log", type=Path)
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    if arguments.max_total_degree < 2:
        raise SystemExit("--max-total-degree must be at least 2")
    if arguments.charge_cutoff < 2:
        raise SystemExit("--charge-cutoff must be at least 2")
    if arguments.formula_regression_degree < 1:
        raise SystemExit("--formula-regression-degree must be positive")
    if not 2 <= arguments.factorization_degree <= arguments.max_total_degree:
        raise SystemExit("--factorization-degree must lie between 2 and the cutoff")
    if arguments.ball_divisor <= 6:
        raise SystemExit("--ball-divisor must exceed 6")
    if any(item < 1 for item in arguments.finite_column_degrees):
        raise SystemExit("finite column degrees must be positive")

    target_radius = rational(arguments.target_radius)
    acceptance_radius = rational(arguments.acceptance_radius)
    failure_probe_radius = rational(arguments.failure_probe_radius)
    if not 0 < acceptance_radius < target_radius < failure_probe_radius:
        raise SystemExit("radii must satisfy 0 < acceptance < target < failure")

    PROGRESS_LOG = arguments.progress_log
    if PROGRESS_LOG is not None:
        PROGRESS_LOG.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_LOG.write_text("", encoding="utf-8")

    payload = build_payload(
        arguments.max_total_degree,
        target_radius,
        acceptance_radius,
        failure_probe_radius,
        arguments.charge_cutoff,
        arguments.finite_column_degrees,
        arguments.formula_regression_degree,
        arguments.factorization_degree,
        arguments.ball_divisor,
        arguments.progress,
        arguments.source_commit,
    )
    if arguments.check and not all(payload["checks"].values()):
        raise SystemExit("R0.42 checks failed")
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
