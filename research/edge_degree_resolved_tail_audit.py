#!/usr/bin/env python3
"""R0.41 exact degree-resolved active-tail audit.

For a degree-i, charge-q base monomial and a degree-j, charge-s tail
monomial, R0.39 bounded the exact weighted column factor by applying

    |i*s/j-q| <= |q| + i*|s|/j

term by term and then setting j equal to the smallest admissible degree.
That estimate is all-order but loses the common input slope s/j.

For every fixed charge 2 <= s < S, this audit instead writes x=s/j and
separates only the harmless degree prefactor:

    (i+j)/(i+j-1) <= (J_s+1)/J_s.

The remaining complete center sum is

    H_s(x) = sum |p_iq| r^i |i*x-q| |s-q|/(3|s+q|).

It is convex on 0 <= x <= s/J_s, so its maximum is exactly at x=0 or
x=s/J_s.  The three exceptional charges s=-1,0,1 retain the proved R0.39
columns, while s>=S retains the proved analytic large-charge sector.
Thus the resulting bound covers every admissible charge and every degree
j>N; finite column scans below are regressions only.

All decisions use exact GMP rationals.  This concerns the reduced edge
generating system and does not prove regularity or blow-up for the full
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
import edge_slope_resolved_transport_audit as r040


Rational = gmpy2.mpq
Polynomial = dict[tuple[int, int], Rational]

R040_CERTIFICATE = Path(
    "research/certificates/r040/edge-slope-resolved-transport.json"
)
R040_EXPECTED_SHA256 = (
    "cc6257637b42798e9fdf17ef66531bf263072057f38c130320ed108fb116fc3b"
)
PROGRESS_LOG: Path | None = None


def rational(value: str | int | Rational) -> Rational:
    return Rational(value)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(
            f"[R0.41 +{elapsed:8.2f}s] {stage}{suffix}",
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


def digest_records(records: list[tuple[str, Rational]]) -> str:
    serialized = "".join(f"{label}:{value}\n" for label, value in records)
    return hashlib.sha256(serialized.encode("ascii")).hexdigest()


def common_endpoint_column(
    terms: list[tuple[int, int, Rational]],
    input_charge: int,
    minimum_degree: int,
) -> dict[str, object]:
    """All-order column for 2<=s<S from two common slope endpoints."""

    if input_charge < 2:
        raise ValueError("common-endpoint column requires input charge at least 2")
    endpoint_zero = Rational(0)
    endpoint_minimum = Rational(0)
    input_slope = Rational(input_charge, minimum_degree)
    for base_degree, base_charge, weighted_coefficient in terms:
        if input_charge + base_charge <= 0:
            raise AssertionError("positive input charge met an exceptional output")
        charge_factor = Rational(
            abs(input_charge - base_charge),
            3 * abs(input_charge + base_charge),
        )
        endpoint_zero += (
            weighted_coefficient * charge_factor * abs(base_charge)
        )
        endpoint_minimum += (
            weighted_coefficient
            * charge_factor
            * abs(base_degree * input_slope - base_charge)
        )
    prefactor = Rational(minimum_degree + 1, minimum_degree)
    maximum_core = max(endpoint_zero, endpoint_minimum)
    return {
        "inputCharge": input_charge,
        "minimumTailDegree": minimum_degree,
        "maximumInputSlope": r037.rational_record(input_slope),
        "degreePrefactor": r037.rational_record(prefactor),
        "coreEndpointAtInfinity": r037.rational_record(endpoint_zero),
        "coreEndpointAtMinimumDegree": r037.rational_record(endpoint_minimum),
        "maximumCoreEndpoint": (
            "x=0" if endpoint_zero >= endpoint_minimum else "x=s/J_s"
        ),
        "bound": r037.rational_record(prefactor * maximum_core),
        "classification": (
            "all-order fixed-charge column: the complete core is convex in "
            "x=s/j and the separated degree prefactor is uniform for j>=J_s"
        ),
    }


def degree_resolved_tail_bound(
    polynomial: Polynomial,
    radius: Rational,
    cutoff: int,
    charge_cutoff: int,
) -> dict[str, object]:
    """Cover all charges using exact finite endpoints and one large sector."""

    terms = r039.weighted_base_terms(polynomial, radius)
    columns: list[dict[str, object]] = []
    digest_input: list[tuple[str, Rational]] = []

    for input_charge in range(-1, charge_cutoff):
        minimum_degree = r039.minimum_tail_degree(input_charge, cutoff)
        if input_charge <= 1:
            value = sum(
                (
                    weighted_coefficient
                    * r039.finite_charge_factor(
                        base_degree,
                        base_charge,
                        input_charge,
                        minimum_degree,
                    )
                    for base_degree, base_charge, weighted_coefficient in terms
                ),
                Rational(0),
            )
            record = {
                "inputCharge": input_charge,
                "minimumTailDegree": minimum_degree,
                "bound": r037.rational_record(value),
                "classification": (
                    "inherited all-order exceptional-charge column from R0.39"
                ),
            }
        else:
            record = common_endpoint_column(
                terms,
                input_charge,
                minimum_degree,
            )
            value = rational(record["bound"]["exact"])
        columns.append(record)
        digest_input.append((str(input_charge), value))

    large_value = sum(
        (
            weighted_coefficient
            * r039.large_charge_factor(
                base_degree,
                base_charge,
                cutoff,
                charge_cutoff,
            )
            for base_degree, base_charge, weighted_coefficient in terms
        ),
        Rational(0),
    )
    large_record = {
        "inputChargeRange": [charge_cutoff, None],
        "bound": r037.rational_record(large_value),
        "classification": (
            "inherited R0.39 analytic sector covering every s>=S and j>N"
        ),
    }
    digest_input.append((f">={charge_cutoff}", large_value))

    finite_maximum = max(
        columns,
        key=lambda record: rational(record["bound"]["exact"]),
    )
    finite_maximum_value = rational(finite_maximum["bound"]["exact"])
    if large_value > finite_maximum_value:
        maximum_value = large_value
        maximum_sector = f">={charge_cutoff}"
    else:
        maximum_value = finite_maximum_value
        maximum_sector = str(finite_maximum["inputCharge"])

    return {
        "finiteChargeRange": [-1, charge_cutoff - 1],
        "commonEndpointChargeRange": [2, charge_cutoff - 1],
        "exceptionalInheritedCharges": [-1, 0, 1],
        "finiteColumns": columns,
        "finiteColumnCount": len(columns),
        "maximumFiniteColumn": finite_maximum,
        "largeChargeSector": large_record,
        "maximumBound": r037.rational_record(maximum_value),
        "maximumSector": maximum_sector,
        "columnBoundsSha256": digest_records(digest_input),
        "classification": (
            "all-order induced weighted-l1 bound covering every charge and "
            "every degree above the polynomial cutoff"
        ),
    }


def exact_tail_column(
    polynomial: Polynomial,
    radius: Rational,
    input_degree: int,
    input_charge: int,
) -> Rational:
    if input_degree <= 0:
        raise ValueError("input degree must be positive")
    if input_degree + input_charge < 0 or (input_degree + input_charge) % 3:
        raise ValueError("degree and charge do not define a bivariate monomial")
    if 2 * input_degree < input_charge:
        raise ValueError("input charge lies outside the active cone")
    return sum(
        (
            Rational(r039.degree(exponent) + input_degree, input_degree)
            * abs(
                r039.monomial_derivative_coefficient(
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
    transport = r040.slope_resolved_transport_bound(
        polynomial,
        radius,
        cutoff,
        ball_radius,
    )
    transport_bound = rational(transport["maximumTotalBound"]["exact"])
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
        "transport": transport,
        "transportBound": r037.rational_record(transport_bound),
        "fixedPointPasses": (
            margin > 0
            and ball_radius > 0
            and residual_norm < residual_allowance
            and mapping_upper < ball_radius
            and lipschitz_upper < 1
        ),
        "transportPasses": transport_bound < 1,
    }


def finite_degree_regressions(
    polynomial: Polynomial,
    radius: Rational,
    tail: dict[str, object],
    input_charge: int,
    input_degrees: list[int],
) -> dict[str, object]:
    sector = next(
        record
        for record in tail["finiteColumns"]
        if record["inputCharge"] == input_charge
    )
    sector_bound = rational(sector["bound"]["exact"])
    records = []
    for input_degree in input_degrees:
        value = exact_tail_column(
            polynomial,
            radius,
            input_degree,
            input_charge,
        )
        records.append(
            {
                "inputDegree": input_degree,
                "inputCharge": input_charge,
                "exactColumn": r037.rational_record(value),
                "allOrderSectorBound": r037.rational_record(sector_bound),
                "belowSectorBound": value <= sector_bound,
                "classification": "finite exact regression only",
            }
        )
    return {
        "inputCharge": input_charge,
        "inputDegrees": input_degrees,
        "records": records,
        "allBelowSectorBound": all(
            record["belowSectorBound"] for record in records
        ),
        "classification": (
            "finite exact implementation regressions; the all-order statement "
            "comes from convexity and the uniform degree prefactor"
        ),
    }


def finite_multicharge_regression(
    polynomial: Polynomial,
    radius: Rational,
    tail: dict[str, object],
    charge_cutoff: int,
    degree_offsets: list[int],
) -> dict[str, object]:
    """Sample every common-endpoint charge at several admissible degrees."""

    sector_records = {
        record["inputCharge"]: record
        for record in tail["finiteColumns"]
    }
    checked = 0
    maximum_ratio = Rational(0)
    worst_charge: int | None = None
    worst_degree: int | None = None
    worst_value = Rational(0)
    worst_bound = Rational(0)
    digest_input: list[tuple[str, Rational]] = []
    for input_charge in range(2, charge_cutoff):
        sector_record = sector_records[input_charge]
        minimum_degree = sector_record["minimumTailDegree"]
        sector_bound = rational(sector_record["bound"]["exact"])
        for offset in degree_offsets:
            input_degree = minimum_degree + offset
            value = exact_tail_column(
                polynomial,
                radius,
                input_degree,
                input_charge,
            )
            if value > sector_bound:
                raise AssertionError(
                    f"finite column s={input_charge}, j={input_degree} "
                    "exceeded its all-order bound"
                )
            ratio = value / sector_bound if sector_bound else Rational(0)
            digest_input.append((f"{input_charge}:{input_degree}", value))
            checked += 1
            if ratio > maximum_ratio:
                maximum_ratio = ratio
                worst_charge = input_charge
                worst_degree = input_degree
                worst_value = value
                worst_bound = sector_bound
    return {
        "inputChargeRange": [2, charge_cutoff - 1],
        "degreeOffsetsFromMinimum": degree_offsets,
        "columnsChecked": checked,
        "allBelowSectorBounds": True,
        "maximumExactToBoundRatio": r037.rational_record(maximum_ratio),
        "worstRegression": {
            "inputCharge": worst_charge,
            "inputDegree": worst_degree,
            "exactColumn": r037.rational_record(worst_value),
            "allOrderSectorBound": r037.rational_record(worst_bound),
        },
        "exactColumnsSha256": digest_records(digest_input),
        "classification": (
            "finite exact multicharge implementation regression only"
        ),
    }


def build_payload(
    maximum_degree: int,
    target_radius: Rational,
    acceptance_radius: Rational,
    failure_probe_radius: Rational,
    charge_cutoff: int,
    finite_degrees: list[int],
    formula_regression_degree: int,
    ball_divisor: int,
    show_progress: bool,
    source_commit: str | None,
) -> dict[str, object]:
    started = time.perf_counter()
    progress(show_progress, started, "loading pinned R0.40 certificate")
    if sha256(R040_CERTIFICATE) != R040_EXPECTED_SHA256:
        raise AssertionError("R0.40 certificate hash mismatch")
    r040_certificate = json.loads(R040_CERTIFICATE.read_text(encoding="utf-8"))
    previous_radius = rational(
        r040_certificate["restartCertificate"]["targetRadius"]["exact"]
    )
    preassigned_acceptance = rational(
        r040_certificate["negativeControl"]["radius"]["exact"]
    )
    if acceptance_radius != preassigned_acceptance:
        raise AssertionError("R0.41 acceptance radius must equal the R0.40 probe")
    if not previous_radius < acceptance_radius <= target_radius:
        raise AssertionError("radii are not ordered beyond R0.40")
    if failure_probe_radius <= target_radius:
        raise AssertionError("failure probe must exceed the target")

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

    progress(
        show_progress,
        started,
        "forming all-order degree-resolved tail bounds",
        finiteCharges=charge_cutoff + 1,
    )
    target_tail = degree_resolved_tail_bound(
        polynomial, target_radius, maximum_degree, charge_cutoff
    )
    acceptance_tail = degree_resolved_tail_bound(
        polynomial, acceptance_radius, maximum_degree, charge_cutoff
    )
    probe_tail = degree_resolved_tail_bound(
        polynomial, failure_probe_radius, maximum_degree, charge_cutoff
    )
    legacy_acceptance = r039.charge_resolved_tail_bound(
        polynomial, acceptance_radius, maximum_degree, charge_cutoff
    )
    legacy_target = r039.charge_resolved_tail_bound(
        polynomial, target_radius, maximum_degree, charge_cutoff
    )

    target_restart = restart_diagnostics(
        polynomial,
        residual,
        target_radius,
        target_tail,
        maximum_degree,
        ball_divisor,
    )
    acceptance_restart = restart_diagnostics(
        polynomial,
        residual,
        acceptance_radius,
        acceptance_tail,
        maximum_degree,
        ball_divisor,
    )
    probe_restart = restart_diagnostics(
        polynomial,
        residual,
        failure_probe_radius,
        probe_tail,
        maximum_degree,
        ball_divisor,
    )

    progress(
        show_progress,
        started,
        "auditing finite exact degree columns",
        inputCharge=162,
        count=len(finite_degrees),
    )
    finite_regressions = finite_degree_regressions(
        polynomial,
        target_radius,
        target_tail,
        162,
        finite_degrees,
    )
    multicharge_regression = finite_multicharge_regression(
        polynomial,
        target_radius,
        target_tail,
        charge_cutoff,
        [0, 3, 12, 60, 240],
    )
    degree_eighty_one_scan = r039.exact_tail_column_scan(
        polynomial,
        target_radius,
        81,
    )
    formula_regression = r039.monomial_formula_regression(
        formula_regression_degree
    )

    target_tail_value = rational(target_tail["maximumBound"]["exact"])
    acceptance_tail_value = rational(
        acceptance_tail["maximumBound"]["exact"]
    )
    probe_tail_value = rational(probe_tail["maximumBound"]["exact"])
    legacy_acceptance_value = rational(
        legacy_acceptance["maximumBound"]["exact"]
    )
    pinned_legacy_acceptance = rational(
        r040_certificate["negativeControl"][
            "activeTailLinearizationBound"
        ]["exact"]
    )
    polynomial_digest = r037.polynomial_digest(polynomial)
    residual_digest = r037.polynomial_digest(residual)
    target_transport = rational(target_restart["transportBound"]["exact"])
    probe_transport = rational(probe_restart["transportBound"]["exact"])

    checks = {
        "r040CertificateHashMatches": True,
        "r040ProbeBecomesAcceptanceTest": (
            acceptance_radius == preassigned_acceptance
        ),
        "targetExceedsR040Radius": target_radius > previous_radius,
        "targetExceedsAcceptanceRadius": target_radius > acceptance_radius,
        "targetDegreeResolvedTailBelowOne": target_tail_value < 1,
        "acceptanceDegreeResolvedTailBelowOne": acceptance_tail_value < 1,
        "probeDegreeResolvedTailBelowOne": probe_tail_value < 1,
        "legacyAcceptanceTailFails": legacy_acceptance_value > 1,
        "legacyAcceptanceMatchesR040": (
            legacy_acceptance_value == pinned_legacy_acceptance
        ),
        "polynomialDigestMatchesR040": (
            polynomial_digest
            == r040_certificate["restartCertificate"][
                "degreeEightyPolynomialSha256"
            ]
        ),
        "residualDigestMatchesR040": (
            residual_digest
            == r040_certificate["restartCertificate"][
                "exactResidualSha256"
            ]
        ),
        "targetFixedPointPasses": target_restart["fixedPointPasses"],
        "targetTransportPasses": target_restart["transportPasses"],
        "acceptanceFixedPointPasses": acceptance_restart["fixedPointPasses"],
        "acceptanceTransportPasses": acceptance_restart["transportPasses"],
        "probeFixedPointPasses": probe_restart["fixedPointPasses"],
        "probeTransportFails": not probe_restart["transportPasses"],
        "targetWorstSectorIsLargeCharge": (
            target_tail["maximumSector"] == f">={charge_cutoff}"
        ),
        "targetTransportWorstEndpointIsTwo": (
            target_restart["transport"]["maximumTotalEndpoint"] == "x=2"
        ),
        "probeFailsOnlyTransportAmongRestartGates": (
            probe_tail_value < 1
            and probe_restart["fixedPointPasses"]
            and probe_transport > 1
        ),
        "finiteDegreeRegressionsPass": finite_regressions[
            "allBelowSectorBound"
        ],
        "finiteMultichargeRegressionPasses": multicharge_regression[
            "allBelowSectorBounds"
        ],
        "degreeEightyOneWorstChargeIs162": (
            degree_eighty_one_scan["maximumColumnCharge"] == 162
        ),
        "monomialFormulaRegressionPasses": formula_regression["passed"],
        "residualStartsAboveCutoff": (
            residual_degrees and residual_degrees[0] == maximum_degree + 1
        ),
        "residualEndsAtDoubleCutoff": (
            residual_degrees and residual_degrees[-1] == 2 * maximum_degree
        ),
        "allFiniteChargesCovered": (
            target_tail["finiteColumnCount"] == charge_cutoff + 1
        ),
        "allCommonEndpointChargesCovered": (
            target_tail["commonEndpointChargeRange"]
            == [2, charge_cutoff - 1]
        ),
        "negativeControlIsAdjacent": (
            failure_probe_radius - target_radius == Rational(3, 4000)
        ),
        "targetTailStrictlyImprovesLegacy": (
            target_tail_value
            < rational(legacy_target["maximumBound"]["exact"])
        ),
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise AssertionError(f"R0.41 checks failed: {failed}")

    elapsed = time.perf_counter() - started
    progress(
        show_progress,
        started,
        "all exact checks passed",
        checks=len(checks),
        targetRadius=str(target_radius),
        targetTail=str(target_tail_value),
        targetTransport=str(target_transport),
    )

    return {
        "scope": {
            "system": "reduced canonical edge generating system",
            "claim": (
                "all-order degree-resolved active-tail theorem and exact "
                "radius restart at 9/32"
            ),
            "notClaimed": [
                "three-dimensional Navier-Stokes global regularity",
                "finite-time blow-up",
                "a singularity at the failed probe",
                "an all-order theorem from finite column scans",
            ],
        },
        "git": r039.git_state(source_commit),
        "input": {
            "r040": {
                "path": str(R040_CERTIFICATE),
                "sha256": R040_EXPECTED_SHA256,
                "sourceCommit": r040_certificate["git"]["commit"],
            }
        },
        "allOrderTheorem": {
            "exactColumnCore": (
                "H_s(x)=sum |p_iq| r^i |i*x-q| |s-q|/(3|s+q|)"
            ),
            "degreeVariable": "x=s/j in [0,s/J_s]",
            "convexity": (
                "H_s is a positive sum of absolute affine functions"
            ),
            "degreePrefactor": (
                "(i+j)/(i+j-1)<=1+1/J_s for every i>=1 and j>=J_s"
            ),
            "finitePositiveCharges": [2, charge_cutoff - 1],
            "exceptionalInheritedCharges": [-1, 0, 1],
            "largeChargeSector": [charge_cutoff, None],
            "degreeCoverage": f"every admissible j>{maximum_degree}",
            "classification": "formal all-order theorem",
        },
        "activeTailKernel": target_tail,
        "legacyComparison": {
            "acceptanceRadius": r037.rational_record(acceptance_radius),
            "legacyAcceptanceTail": legacy_acceptance["maximumBound"],
            "degreeResolvedAcceptanceTail": acceptance_tail["maximumBound"],
            "targetRadius": r037.rational_record(target_radius),
            "legacyTargetTail": legacy_target["maximumBound"],
            "degreeResolvedTargetTail": target_tail["maximumBound"],
        },
        "acceptanceTest": acceptance_restart,
        "restartCertificate": {
            **target_restart,
            "previousRadius": r037.rational_record(previous_radius),
            "radiusGainFromR040": r037.rational_record(
                target_radius / previous_radius
            ),
            "fixedChargeGainFromR040": r037.rational_record(
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
                "there is a unique active correction supported above degree "
                "80, and the two-endpoint transport inverse constructs the "
                "canonical normalized fields at radius 9/32"
            ),
        },
        "negativeControl": {
            **probe_restart,
            "classification": (
                "the present sufficient transport inequality fails while the "
                "new all-order active-tail fixed point still passes; this is "
                "not evidence of a singularity or loss of analyticity"
            ),
        },
        "finiteRegression": {
            "degreeColumnsAtCharge162": finite_regressions,
            "multichargeColumns": multicharge_regression,
            "degreeEightyOneScan": degree_eighty_one_scan,
            "monomialCoefficientFormula": formula_regression,
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


def atomic_json_write(path: Path, payload: dict[str, object], pretty: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2 if pretty else None,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def parse_degree_list(value: str) -> list[int]:
    degrees = sorted({int(item) for item in value.split(",") if item.strip()})
    if not degrees:
        raise argparse.ArgumentTypeError("degree list must not be empty")
    return degrees


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-total-degree", type=int, default=80)
    parser.add_argument("--target-radius", default="9/32")
    parser.add_argument("--acceptance-radius", default="257/1000")
    parser.add_argument("--failure-probe-radius", default="141/500")
    parser.add_argument("--charge-cutoff", type=int, default=241)
    parser.add_argument(
        "--finite-degrees",
        type=parse_degree_list,
        default=parse_degree_list("81,84,87,90,99,120,162,243,324,486,810,1620"),
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
        raise SystemExit("maximum degree must be at least two")
    if arguments.charge_cutoff <= 2:
        raise SystemExit("charge cutoff must exceed two")
    if arguments.ball_divisor <= 6:
        raise SystemExit("ball divisor must exceed six")
    for input_degree in arguments.finite_degrees:
        if input_degree <= arguments.max_total_degree:
            raise SystemExit("finite regression degrees must exceed the cutoff")
        if (input_degree + 162) % 3 or 2 * input_degree < 162:
            raise SystemExit(
                f"degree {input_degree} is inadmissible for input charge 162"
            )

    global PROGRESS_LOG
    PROGRESS_LOG = arguments.progress_log
    if PROGRESS_LOG is not None:
        PROGRESS_LOG.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_LOG.write_text("", encoding="utf-8")

    payload = build_payload(
        arguments.max_total_degree,
        rational(arguments.target_radius),
        rational(arguments.acceptance_radius),
        rational(arguments.failure_probe_radius),
        arguments.charge_cutoff,
        arguments.finite_degrees,
        arguments.formula_regression_degree,
        arguments.ball_divisor,
        arguments.progress,
        arguments.source_commit,
    )
    if arguments.check and not all(payload["checks"].values()):
        raise SystemExit("one or more exact checks failed")
    if arguments.output is not None:
        atomic_json_write(arguments.output, payload, arguments.pretty)
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
