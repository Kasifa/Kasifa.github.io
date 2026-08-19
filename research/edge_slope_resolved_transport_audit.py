#!/usr/bin/env python3
"""R0.40 exact input-slope-resolved transport audit.

For T_a f=(L-1)^(-1){a,f}, a base monomial of degree-charge (i,q)
and an input monomial of degree-charge (j,s) contribute the weighted
Wiener column factor

    (i+j)/(i+j-1) * abs(i*(s/j)-q) / 3.

For fixed j the complete polynomial column sum is convex in x=s/j on
[-1,2], hence its maximum is attained at the two genuine monomials
x=-1 and x=2.  At either endpoint every summand decreases with j, so
the all-order polynomial operator norm is attained at j=1.  This gives
the exact two-column formula

    max(
      sum |a_(i,q)| r^i (i+1)/i (i+q)/3,
      sum |a_(i,q)| r^i (i+1)/i (2*i-q)/3
    ).

For the unknown active correction supported on degrees i>N, the same
two endpoint columns are bounded by explicit multiples of its weighted
Wiener norm.  No input-degree, input-charge, or input-slope cutoff occurs.

All threshold decisions use exact GMP rationals.  The result concerns the
reduced edge generating system, not regularity or blow-up for the full
three-dimensional Navier--Stokes equation.
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

import edge_rational_asymptotic_audit as r028
import edge_short_continuation_audit as r036
import edge_weighted_restart_audit as r037
import edge_charge_resolved_audit as r039


Rational = gmpy2.mpq
Exponent = tuple[int, int]
Polynomial = dict[Exponent, Rational]

R039_CERTIFICATE = Path(
    "research/certificates/r039/edge-charge-resolved.json"
)
R039_EXPECTED_SHA256 = (
    "59b978c1c5384edb394adc76add0950b3c8e6666f6562dfc199584c22dd0e700"
)
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(
            f"[R0.40 +{elapsed:8.2f}s] {stage}{suffix}",
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


def transport_monomial_coefficient(
    base_degree: int,
    base_charge: int,
    input_degree: int,
    input_charge: int,
) -> Rational:
    """Coefficient of one monomial pair in (L-1)^(-1){a,f}."""

    return Rational(
        base_degree * input_charge - base_charge * input_degree,
        3 * (base_degree + input_degree - 1),
    )


def endpoint_factor(
    base_degree: int,
    base_charge: int,
    input_slope: int,
) -> Rational:
    """Weighted column factor at j=1 and x=s/j in {-1,2}."""

    if input_slope not in (-1, 2):
        raise AssertionError("endpoint slope must be -1 or 2")
    return Rational(
        (base_degree + 1)
        * abs(base_degree * input_slope - base_charge),
        3 * base_degree,
    )


def polynomial_endpoint_bounds(
    polynomial: Polynomial,
    radius: Rational,
) -> dict[str, object]:
    """Exact two endpoint columns for the finite polynomial center."""

    records = []
    for label, slope in (("x=-1", -1), ("x=2", 2)):
        value = sum(
            (
                abs(coefficient)
                * radius ** r039.degree(exponent)
                * endpoint_factor(
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
                "inputDegree": 1,
                "inputCharge": slope,
                "inputSlope": slope,
                "bound": r037.rational_record(value),
            }
        )
    maximum_record = max(
        records,
        key=lambda record: rational(record["bound"]["exact"]),
    )
    return {
        "endpointColumns": records,
        "maximumBound": maximum_record["bound"],
        "maximumEndpoint": maximum_record["label"],
        "classification": (
            "exact induced weighted-l1 norm of the polynomial transport "
            "operator; convexity reduces all input slopes to x=-1 or x=2 "
            "and monotonicity reduces every input degree to j=1"
        ),
    }


def tail_endpoint_constants(cutoff: int) -> dict[str, Rational]:
    """Endpoint multipliers for active corrections of degree >N."""

    first_tail_degree = cutoff + 1
    return {
        "x=-1": Rational(first_tail_degree + 1, first_tail_degree),
        "x=2": Rational(
            (first_tail_degree + 1) * (2 * first_tail_degree + 1),
            3 * first_tail_degree**2,
        ),
    }


def slope_resolved_transport_bound(
    polynomial: Polynomial,
    radius: Rational,
    cutoff: int,
    correction_norm_bound: Rational,
) -> dict[str, object]:
    polynomial_bounds = polynomial_endpoint_bounds(polynomial, radius)
    constants = tail_endpoint_constants(cutoff)
    totals = []
    for record in polynomial_bounds["endpointColumns"]:
        label = record["label"]
        polynomial_value = rational(record["bound"]["exact"])
        correction_value = constants[label] * correction_norm_bound
        totals.append(
            {
                **record,
                "tailMultiplier": r037.rational_record(constants[label]),
                "tailContributionUpperBound": r037.rational_record(
                    correction_value
                ),
                "totalBound": r037.rational_record(
                    polynomial_value + correction_value
                ),
            }
        )
    maximum_record = max(
        totals,
        key=lambda record: rational(record["totalBound"]["exact"]),
    )
    return {
        "endpointColumns": totals,
        "maximumPolynomialBound": polynomial_bounds["maximumBound"],
        "maximumPolynomialEndpoint": polynomial_bounds["maximumEndpoint"],
        "maximumTotalBound": maximum_record["totalBound"],
        "maximumTotalEndpoint": maximum_record["label"],
        "tailHypothesis": f"active correction supported on degrees >{cutoff}",
        "classification": (
            "all-order two-endpoint bound for the polynomial center plus "
            "the unknown strict-tail correction"
        ),
    }


def exact_transport_column(
    polynomial: Polynomial,
    radius: Rational,
    input_degree: int,
    input_charge: int,
) -> Rational:
    """Exact weighted-l1 column ratio for one input monomial."""

    return sum(
        (
            Rational(r039.degree(exponent) + input_degree, input_degree)
            * abs(
                transport_monomial_coefficient(
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


def finite_transport_column_scan(
    polynomial: Polynomial,
    radius: Rational,
    input_degree: int,
) -> dict[str, object]:
    """Finite implementation regression; not part of the all-order proof."""

    columns = []
    for input_w_degree in range(input_degree + 1):
        input_charge = 3 * input_w_degree - input_degree
        value = exact_transport_column(
            polynomial,
            radius,
            input_degree,
            input_charge,
        )
        columns.append((input_charge, value))
    maximum_charge, maximum_value = max(columns, key=lambda item: item[1])
    return {
        "inputDegree": input_degree,
        "admissibleColumns": len(columns),
        "maximumColumnCharge": maximum_charge,
        "maximumInputSlope": r037.rational_record(
            Rational(maximum_charge, input_degree)
        ),
        "maximumWeightedColumnRatio": r037.rational_record(maximum_value),
        "classification": "finite exact transport-column regression only",
    }


def transport_formula_regression(maximum_degree: int) -> dict[str, object]:
    """Compare the closed coefficient with the original bracket operator."""

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
            expected = transport_monomial_coefficient(
                r039.degree(base_exponent),
                r039.charge(base_exponent),
                r039.degree(input_exponent),
                r039.charge(input_exponent),
            )
            image = r036.inverse_l_minus_one(
                r036.bracket(
                    {base_exponent: Rational(1)},
                    {input_exponent: Rational(1)},
                )
            )
            if image.get(expected_exponent, Rational(0)) != expected:
                raise AssertionError("transport coefficient formula mismatch")
            if any(exponent != expected_exponent for exponent in image):
                raise AssertionError("transport monomial produced another exponent")
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


def build_payload(
    maximum_degree: int,
    target_radius: Rational,
    failure_probe_radius: Rational,
    charge_cutoff: int,
    finite_column_degrees: list[int],
    formula_regression_degree: int,
    ball_divisor: int,
    show_progress: bool,
    source_commit: str | None,
) -> dict[str, object]:
    started = time.perf_counter()
    progress(show_progress, started, "loading pinned R0.39 certificate")
    if sha256(R039_CERTIFICATE) != R039_EXPECTED_SHA256:
        raise AssertionError("R0.39 certificate hash mismatch")
    r039_certificate = json.loads(R039_CERTIFICATE.read_text(encoding="utf-8"))
    previous_radius = rational(
        r039_certificate["restartCertificate"]["targetRadius"]["exact"]
    )
    r031_radius = rational(
        r039_certificate["restartCertificate"]["r031Radius"]["exact"]
    )
    if target_radius <= previous_radius:
        raise AssertionError("R0.40 target must exceed the R0.39 radius")

    progress(
        show_progress,
        started,
        "constructing exact degree recurrence",
        maximumDegree=maximum_degree,
    )
    active_field, _, _, recurrence_interactions = r028.rational_edge_recurrence(
        maximum_degree,
        show_progress,
        started,
    )
    polynomial = r036.field_to_polynomial(active_field, maximum_degree)
    if any(r039.charge(exponent) < -1 for exponent in polynomial):
        raise AssertionError("degree polynomial left the active support cone")

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
    low_residual = r036.truncate(residual, maximum_degree)
    if low_residual:
        raise AssertionError("degree recurrence has a residual below the cutoff")
    residual_degrees = sorted({r039.degree(exponent) for exponent in residual})

    progress(
        show_progress,
        started,
        "forming all-order active-tail bounds",
        finiteCharges=charge_cutoff + 1,
    )
    tail = r039.charge_resolved_tail_bound(
        polynomial,
        target_radius,
        maximum_degree,
        charge_cutoff,
    )
    probe_tail = r039.charge_resolved_tail_bound(
        polynomial,
        failure_probe_radius,
        maximum_degree,
        charge_cutoff,
    )
    tail_bound = rational(tail["maximumBound"]["exact"])
    probe_tail_bound = rational(probe_tail["maximumBound"]["exact"])

    polynomial_norm = r037.weighted_wiener_norm(polynomial, target_radius)
    residual_norm = r037.weighted_wiener_norm(residual, target_radius)
    contraction_margin = 1 - tail_bound
    ball_radius = contraction_margin / ball_divisor
    residual_allowance = (
        contraction_margin * ball_radius - 3 * ball_radius**2
    )
    mapping_upper_bound = (
        residual_norm + tail_bound * ball_radius + 3 * ball_radius**2
    )
    lipschitz_upper_bound = tail_bound + 6 * ball_radius
    solution_norm_upper_bound = polynomial_norm + ball_radius

    progress(
        show_progress,
        started,
        "forming exact two-endpoint transport bound",
    )
    transport = slope_resolved_transport_bound(
        polynomial,
        target_radius,
        maximum_degree,
        ball_radius,
    )
    transport_operator_bound = rational(
        transport["maximumTotalBound"]["exact"]
    )
    transport_inverse_bound = 1 / (1 - transport_operator_bound)
    r039_termwise_transport_bound = (
        r039.refined_transport_bound(polynomial, target_radius)
        + 2 * ball_radius
    )
    old_scalar_transport_bound = 2 * solution_norm_upper_bound

    probe_polynomial_transport = polynomial_endpoint_bounds(
        polynomial,
        failure_probe_radius,
    )
    probe_polynomial_transport_bound = rational(
        probe_polynomial_transport["maximumBound"]["exact"]
    )

    progress(
        show_progress,
        started,
        "checking exact transport coefficient formula",
        maximumDegree=formula_regression_degree,
    )
    formula_regression = transport_formula_regression(
        formula_regression_degree
    )

    finite_columns = []
    for input_degree in finite_column_degrees:
        progress(
            show_progress,
            started,
            "auditing finite exact transport columns",
            inputDegree=input_degree,
        )
        finite_columns.append(
            finite_transport_column_scan(
                polynomial,
                target_radius,
                input_degree,
            )
        )

    target_polynomial_transport_bound = rational(
        transport["maximumPolynomialBound"]["exact"]
    )
    candidate_fixed_charge_lower = rational(
        r039_certificate["candidateComparison"][
            "tailTransportCandidateModulusLower"
        ]["exact"]
    )
    candidate_gap_factor = candidate_fixed_charge_lower / target_radius**3

    checks = {
        "pinnedInputHash": True,
        "activeSupportConePreserved": all(
            r039.charge(exponent) >= -1 for exponent in polynomial
        ),
        "originRecurrenceThroughCutoff": not low_residual,
        "residualBeginsAboveCutoff": min(residual_degrees) > maximum_degree,
        "residualEndsAtTwiceCutoff": (
            max(residual_degrees) <= 2 * maximum_degree
        ),
        "targetRadiusExceedsR039": target_radius > previous_radius,
        "closedTransportCoefficientFormulaExact": formula_regression["passed"],
        "allInputSlopesCoveredByConvexEndpointReduction": True,
        "allInputDegreesCoveredByMonotoneDegreeReduction": True,
        "activeTailBoundBelowOne": tail_bound < 1,
        "residualFitsContractionBall": residual_norm < residual_allowance,
        "ballMapsStrictlyInsideItself": mapping_upper_bound < ball_radius,
        "ballLipschitzConstantBelowOne": lipschitz_upper_bound < 1,
        "r039TermwiseTransportBoundFailsAtTarget": (
            r039_termwise_transport_bound > 1
        ),
        "slopeResolvedTransportBoundBelowOne": transport_operator_bound < 1,
        "oldScalarTransportBoundFailsAtTarget": old_scalar_transport_bound > 1,
        "nearbyProbeFailsActiveTailCondition": (
            failure_probe_radius > target_radius and probe_tail_bound > 1
        ),
        "probePolynomialTransportStillBelowOne": (
            probe_polynomial_transport_bound < 1
        ),
        "finiteTransportColumnsBelowEndpointTheorem": all(
            rational(column["maximumWeightedColumnRatio"]["exact"])
            <= target_polynomial_transport_bound
            for column in finite_columns
        ),
        "finiteCandidateRemainsOutsideCertifiedDisk": candidate_gap_factor > 1,
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        diagnostics = {
            "failed": failed,
            "targetTail": r037.rational_record(tail_bound),
            "targetTransport": r037.rational_record(transport_operator_bound),
            "oldTermwiseTransport": r037.rational_record(
                r039_termwise_transport_bound
            ),
            "probeTail": r037.rational_record(probe_tail_bound),
            "probePolynomialTransport": r037.rational_record(
                probe_polynomial_transport_bound
            ),
        }
        raise AssertionError(
            "one or more R0.40 checks failed: "
            + json.dumps(diagnostics, sort_keys=True)
        )

    payload = {
        "scope": {
            "result": (
                "an exact all-order two-endpoint theorem for normalized "
                "transport and a larger common analytic radius for the reduced fields"
            ),
            "classification": (
                "all-order Banach-space theorem, exact rational degree-80 restart "
                "certificate, and finite exact implementation regressions"
            ),
            "limitations": [
                "the active correction theorem remains restricted to q>=-1",
                "the transport endpoint theorem uses the isotropic weighted Wiener norm",
                "the nearby negative control fails only the present active-tail bound",
                "the result concerns the reduced edge generating equation rather than the full PDE",
                "the R0.32 finite Pade candidate remains outside the certified fixed-charge disk",
                "no Navier-Stokes regularity or blow-up conclusion is claimed",
            ],
        },
        "input": {
            "r039": {
                "path": str(R039_CERTIFICATE),
                "sha256": R039_EXPECTED_SHA256,
                "sourceCommit": r039_certificate["git"]["commit"],
            }
        },
        "allOrderTheorem": {
            "space": r039_certificate["allOrderTheorem"]["space"],
            "transportColumnFactor": (
                "(i+j)/(i+j-1)*abs(i*(s/j)-q)/3"
            ),
            "slopeReduction": (
                "for fixed j the complete absolute column sum is convex in "
                "x=s/j on [-1,2], so its maximum is attained at x=-1 or x=2"
            ),
            "degreeReduction": (
                "at either endpoint every factor (i+j)/(i+j-1) decreases "
                "with j, so the maximum over every input degree is attained at j=1"
            ),
            "polynomialNormIdentity": (
                "||T_p||=max(sum |p_(i,q)|r^i(i+1)(i+q)/(3i), "
                "sum |p_(i,q)|r^i(i+1)(2i-q)/(3i))"
            ),
            "strictTailEndpointConstants": {
                label: r037.rational_record(value)
                for label, value in tail_endpoint_constants(
                    maximum_degree
                ).items()
            },
            "strictTailProof": (
                "for i>N and -1<=q<=2i, divide each endpoint factor by "
                "the B_r input weight i; the maxima occur at q=2i for x=-1 "
                "and q=-1 for x=2, then both expressions decrease with i"
            ),
            "coverage": (
                "every bivariate input monomial has j>=1 and s/j in [-1,2]; "
                "the two endpoints are the actual degree-one monomials Z and W"
            ),
        },
        "activeTailKernel": tail,
        "transportKernel": transport,
        "restartCertificate": {
            "polynomialCutoff": maximum_degree,
            "chargeCutoff": charge_cutoff,
            "targetRadius": r037.rational_record(target_radius),
            "r039Radius": r037.rational_record(previous_radius),
            "r031Radius": r037.rational_record(r031_radius),
            "radiusGainFromR039": r037.rational_record(
                target_radius / previous_radius
            ),
            "radiusGainFromR031": r037.rational_record(
                target_radius / r031_radius
            ),
            "fixedChargeGainFromR039": r037.rational_record(
                (target_radius / previous_radius) ** 3
            ),
            "fixedChargeGainFromR031": r037.rational_record(
                (target_radius / r031_radius) ** 3
            ),
            "degreeEightyPolynomialSha256": r037.polynomial_digest(polynomial),
            "degreeEightyPolynomialTerms": len(polynomial),
            "degreeEightyPolynomialNorm": r037.rational_record(polynomial_norm),
            "activeTailLinearizationBound": r037.rational_record(tail_bound),
            "contractionMargin": r037.rational_record(contraction_margin),
            "exactResidualSha256": r037.polynomial_digest(residual),
            "exactResidualTerms": len(residual),
            "residualDegreeRange": [
                min(residual_degrees),
                max(residual_degrees),
            ],
            "exactResidualNorm": r037.rational_record(residual_norm),
            "ballDivisor": ball_divisor,
            "chosenBallRadius": r037.rational_record(ball_radius),
            "residualAllowance": r037.rational_record(residual_allowance),
            "residualToAllowanceRatio": r037.rational_record(
                residual_norm / residual_allowance
            ),
            "mappingUpperBound": r037.rational_record(mapping_upper_bound),
            "lipschitzUpperBound": r037.rational_record(lipschitz_upper_bound),
            "solutionNormUpperBound": r037.rational_record(
                solution_norm_upper_bound
            ),
            "r039TermwiseTransportBound": r037.rational_record(
                r039_termwise_transport_bound
            ),
            "slopeResolvedTransportBound": r037.rational_record(
                transport_operator_bound
            ),
            "transportInverseNormUpperBound": r037.rational_record(
                transport_inverse_bound
            ),
            "oldScalarTransportBound": r037.rational_record(
                old_scalar_transport_bound
            ),
            "statement": (
                "there is a unique degree-greater-than-80 active correction; "
                "triangular formal uniqueness identifies it with the canonical "
                "active series, and the exact two-endpoint transport Neumann "
                "bound constructs canonical U and V at the same radius"
            ),
        },
        "negativeControl": {
            "radius": r037.rational_record(failure_probe_radius),
            "activeTailLinearizationBound": r037.rational_record(
                probe_tail_bound
            ),
            "polynomialTransportEndpointBound": (
                probe_polynomial_transport["maximumBound"]
            ),
            "polynomialTransportMaximumEndpoint": (
                probe_polynomial_transport["maximumEndpoint"]
            ),
            "classification": (
                "failure of the present sufficient active-tail inequality only; "
                "the exact polynomial transport endpoint bound still passes, "
                "and this is not evidence of nonanalyticity or a singularity"
            ),
        },
        "candidateComparison": {
            "classification": "finite R0.32 diagnostic only",
            "tailTransportCandidateModulusLower": r037.rational_record(
                candidate_fixed_charge_lower
            ),
            "certifiedFixedChargeRadius": r037.rational_record(
                target_radius**3
            ),
            "candidateGapFactorLower": r037.rational_record(
                candidate_gap_factor
            ),
            "meaning": (
                "the finite candidate remains outside the proved disk and is "
                "not certified as a singularity"
            ),
        },
        "finiteRegression": {
            "transportCoefficientFormula": formula_regression,
            "transportColumns": finite_columns,
            "recurrenceMaximumDegree": maximum_degree,
            "recurrenceOrderedInteractions": recurrence_interactions,
        },
        "checks": checks,
        "computation": {
            "backend": r028.base.RATIONAL_BACKEND,
            "randomSeed": None,
            "wallSeconds": time.perf_counter() - started,
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "gmpy2": gmpy2.version(),
            "gmp": gmpy2.mp_version(),
        },
        "git": r039.git_state(source_commit),
    }
    progress(
        show_progress,
        started,
        "completed R0.40 slope-resolved transport certificate",
        checks=len(checks),
        passed=True,
    )
    return payload


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
    parser.add_argument("--target-radius", default="32/125")
    parser.add_argument("--failure-probe-radius", default="257/1000")
    parser.add_argument("--charge-cutoff", type=int, default=241)
    parser.add_argument(
        "--finite-column-degrees",
        type=parse_degree_list,
        default=parse_degree_list("1,2,5,20,81"),
    )
    parser.add_argument("--formula-regression-degree", type=int, default=10)
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
    if arguments.ball_divisor <= 6:
        raise SystemExit("--ball-divisor must exceed 6")
    if any(item < 1 for item in arguments.finite_column_degrees):
        raise SystemExit("finite column degrees must be positive")

    target_radius = rational(arguments.target_radius)
    failure_probe_radius = rational(arguments.failure_probe_radius)
    if target_radius <= 0:
        raise SystemExit("--target-radius must be positive")
    if failure_probe_radius <= target_radius:
        raise SystemExit("--failure-probe-radius must exceed the target")

    PROGRESS_LOG = arguments.progress_log
    if PROGRESS_LOG is not None:
        PROGRESS_LOG.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_LOG.write_text("", encoding="utf-8")

    payload = build_payload(
        arguments.max_total_degree,
        target_radius,
        failure_probe_radius,
        arguments.charge_cutoff,
        arguments.finite_column_degrees,
        arguments.formula_regression_degree,
        arguments.ball_divisor,
        arguments.progress,
        arguments.source_commit,
    )
    if arguments.check and not all(payload["checks"].values()):
        raise SystemExit("R0.40 checks failed")
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
