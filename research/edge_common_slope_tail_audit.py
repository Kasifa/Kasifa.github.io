#!/usr/bin/env python3
"""R0.44 exact common-slope active-tail audit.

R0.43 bounded the large positive-charge active-tail sector term by term.
For a center monomial of degree i and charge q and a strict-tail input of
degree j and charge s, the exact weighted column contribution is

    (i+j)/(i+j-1) * |i*(s/j)-q| * (s-q)/(3*(s+q)).

The previous bound maximized |i*(s/j)-q| separately for every center term.
That loses the fact that the input slope

    x = s/j in [0,2]

is common to the complete positive sum.  In the sector s>=S, the support
cone and strict-tail condition give

    j >= J_S := max(N+1, ceil(S/2)).

Because every degree and charge prefactor is positive, the full column is
bounded by

    H_r(x) = sum c_iq(r) d_i beta_q |i*x-q| / 3,

where d_i=(i+J_S)/(i+J_S-1), beta_-1=(S+1)/(S-1), and beta_q=1 for q>=0.
The function H_r is a positive sum of absolute affine functions, hence is
convex on [0,2].  Its all-order maximum is therefore exactly reduced to the
two common endpoints x=0 and x=2.  No coefficient-sign cancellation, charge
cutoff beyond S, degree grid, or finite slope scan is used in the proof.

The script preserves the R0.41 finite-charge columns, recomputes the complete
Banach restart and R0.42 canonical-stretch construction, and keeps finite
large-charge columns and all breakpoints of H_r as implementation regressions
only.  All threshold decisions use exact GMP rationals.  This theorem concerns
the reduced canonical edge generating system and does not prove regularity or
singularity for the three-dimensional Navier--Stokes equation.
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

import edge_charge_degree_floor_audit as r043
import edge_charge_resolved_audit as r039
import edge_degree_resolved_tail_audit as r041
import edge_rational_asymptotic_audit as r028
import edge_short_continuation_audit as r036
import edge_stretch_transport_audit as r042
import edge_weighted_restart_audit as r037


Rational = gmpy2.mpq
Polynomial = dict[tuple[int, int], Rational]

R043_CERTIFICATE = Path(
    "research/certificates/r043/edge-charge-degree-floor.json"
)
R043_EXPECTED_SHA256 = (
    "0ebaaf6c5a9f731e5b2846f3042553bebd6748b298ce31919e8f423e41369bf8"
)
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(
            f"[R0.44 +{elapsed:8.2f}s] {stage}{suffix}",
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


def charge_factor_upper(base_charge: int, charge_cutoff: int) -> Rational:
    """Positive charge-ratio bound valid for every s>=charge_cutoff."""

    if base_charge == -1:
        return Rational(charge_cutoff + 1, charge_cutoff - 1)
    if base_charge < -1:
        raise AssertionError("common-slope bound received q<-1")
    return Rational(1)


def common_slope_value(
    terms: list[tuple[int, int, Rational]],
    slope: Rational,
    cutoff: int,
    charge_cutoff: int,
) -> Rational:
    """Evaluate the positive piecewise-linear common-slope envelope H_r."""

    minimum_degree = r043.charge_implied_degree_floor(cutoff, charge_cutoff)
    value = Rational(0)
    for base_degree, base_charge, weighted_coefficient in terms:
        degree_factor = Rational(
            base_degree + minimum_degree,
            base_degree + minimum_degree - 1,
        )
        value += (
            weighted_coefficient
            * degree_factor
            * charge_factor_upper(base_charge, charge_cutoff)
            * abs(base_degree * slope - base_charge)
            / 3
        )
    return value


def common_slope_large_sector(
    terms: list[tuple[int, int, Rational]],
    cutoff: int,
    charge_cutoff: int,
) -> dict[str, object]:
    """All-order large-sector bound from the two common slope endpoints."""

    endpoint_zero = common_slope_value(
        terms,
        Rational(0),
        cutoff,
        charge_cutoff,
    )
    endpoint_two = common_slope_value(
        terms,
        Rational(2),
        cutoff,
        charge_cutoff,
    )
    maximum = max(endpoint_zero, endpoint_two)
    minimum_degree = r043.charge_implied_degree_floor(cutoff, charge_cutoff)
    return {
        "inputChargeRange": [charge_cutoff, None],
        "inputSlopeRange": [0, 2],
        "chargeImpliedDegreeFloor": minimum_degree,
        "degreeFactor": "(i+J_S)/(i+J_S-1)",
        "negativeChargeRatioFactor": r037.rational_record(
            Rational(charge_cutoff + 1, charge_cutoff - 1)
        ),
        "nonnegativeChargeRatioFactor": r037.rational_record(Rational(1)),
        "endpointAtZero": r037.rational_record(endpoint_zero),
        "endpointAtTwo": r037.rational_record(endpoint_two),
        "maximumEndpoint": "x=0" if endpoint_zero >= endpoint_two else "x=2",
        "bound": r037.rational_record(maximum),
        "proof": (
            "after positive termwise degree and charge-ratio domination, the "
            "complete center sum H_r(x) is a positive sum of |i*x-q| and is "
            "therefore convex on the common interval 0<=x<=2; its maximum is "
            "at x=0 or x=2"
        ),
        "classification": (
            "all-order analytic sector covering every integer s>=S and every "
            "admissible j>N in the bivariate support cone"
        ),
    }


def common_slope_tail_bound(
    polynomial: Polynomial,
    radius: Rational,
    cutoff: int,
    charge_cutoff: int,
) -> dict[str, object]:
    """R0.41 finite columns plus the common-slope large-sector theorem."""

    inherited = r041.degree_resolved_tail_bound(
        polynomial,
        radius,
        cutoff,
        charge_cutoff,
    )
    large = common_slope_large_sector(
        r039.weighted_base_terms(polynomial, radius),
        cutoff,
        charge_cutoff,
    )
    large_value = rational(large["bound"]["exact"])
    finite_maximum = inherited["maximumFiniteColumn"]
    finite_value = rational(finite_maximum["bound"]["exact"])
    if large_value > finite_value:
        maximum_value = large_value
        maximum_sector = f">={charge_cutoff}"
    else:
        maximum_value = finite_value
        maximum_sector = str(finite_maximum["inputCharge"])

    digest_input = [
        (str(record["inputCharge"]), rational(record["bound"]["exact"]))
        for record in inherited["finiteColumns"]
    ]
    digest_input.append((f">={charge_cutoff}", large_value))
    return {
        **inherited,
        "largeChargeSector": large,
        "maximumBound": r037.rational_record(maximum_value),
        "maximumSector": maximum_sector,
        "columnBoundsSha256": r041.digest_records(digest_input),
        "classification": (
            "all-order induced weighted-l1 bound covering every charge and "
            "degree above the polynomial cutoff; the infinite positive-charge "
            "sector retains one common input slope across the full center sum"
        ),
    }


def breakpoint_regression(
    terms: list[tuple[int, int, Rational]],
    sector: dict[str, object],
    cutoff: int,
    charge_cutoff: int,
) -> dict[str, object]:
    """Finite implementation check at every kink of H_r; not the proof."""

    slopes = {Rational(0), Rational(2)}
    for base_degree, base_charge, _weighted_coefficient in terms:
        if 0 <= base_charge <= 2 * base_degree:
            slopes.add(Rational(base_charge, base_degree))
    records = [
        (
            slope,
            common_slope_value(terms, slope, cutoff, charge_cutoff),
        )
        for slope in sorted(slopes)
    ]
    endpoint_bound = rational(sector["bound"]["exact"])
    maximum_slope, maximum_value = max(records, key=lambda item: item[1])
    digest = r041.digest_records(
        [(str(slope), value) for slope, value in records]
    )
    return {
        "breakpointCount": len(records),
        "maximumBreakpointSlope": r037.rational_record(maximum_slope),
        "maximumBreakpointValue": r037.rational_record(maximum_value),
        "endpointBound": r037.rational_record(endpoint_bound),
        "allBreakpointsBelowEndpointBound": all(
            value <= endpoint_bound for _slope, value in records
        ),
        "breakpointValuesSha256": digest,
        "classification": (
            "finite exact implementation regression only; all-order coverage "
            "comes from convexity of the complete common-slope envelope"
        ),
    }


def finite_large_charge_regression(
    polynomial: Polynomial,
    radius: Rational,
    tail: dict[str, object],
    charges: list[int],
    degree_offsets: list[int],
    cutoff: int,
) -> dict[str, object]:
    """Finite exact columns inside the analytic large sector."""

    sector_bound = rational(tail["largeChargeSector"]["bound"]["exact"])
    records = []
    digest_input = []
    for input_charge in charges:
        minimum_degree = r039.minimum_tail_degree(input_charge, cutoff)
        for offset in degree_offsets:
            input_degree = minimum_degree + offset
            if (input_degree + input_charge) % 3:
                raise AssertionError("degree offset left the bivariate lattice")
            value = r041.exact_tail_column(
                polynomial,
                radius,
                input_degree,
                input_charge,
            )
            records.append(
                {
                    "inputCharge": input_charge,
                    "inputDegree": input_degree,
                    "inputSlope": r037.rational_record(
                        Rational(input_charge, input_degree)
                    ),
                    "exactColumn": r037.rational_record(value),
                    "belowSectorBound": value <= sector_bound,
                    "classification": (
                        "finite exact implementation regression only"
                    ),
                }
            )
            digest_input.append((f"{input_charge}:{input_degree}", value))
    return {
        "inputCharges": charges,
        "degreeOffsets": degree_offsets,
        "records": records,
        "allBelowSectorBound": all(record["belowSectorBound"] for record in records),
        "exactColumnsSha256": r041.digest_records(digest_input),
        "classification": (
            "finite exact regression only; the infinite sector is proved by "
            "the common-slope convexity theorem"
        ),
    }


def build_payload(
    maximum_degree: int,
    entry_radius: Rational,
    target_radius: Rational,
    failure_probe_radius: Rational,
    charge_cutoff: int,
    regression_charges: list[int],
    regression_degree_offsets: list[int],
    ball_divisor: int,
    show_progress: bool,
    source_commit: str | None,
) -> dict[str, object]:
    started = time.perf_counter()
    progress(show_progress, started, "loading pinned R0.43 certificate")
    if sha256(R043_CERTIFICATE) != R043_EXPECTED_SHA256:
        raise AssertionError("R0.43 certificate hash mismatch")
    r043_certificate = json.loads(R043_CERTIFICATE.read_text(encoding="utf-8"))
    pinned_entry_radius = rational(
        r043_certificate["negativeControl"]["radius"]["exact"]
    )
    pinned_entry_failure = rational(
        r043_certificate["negativeControl"]["tailLinearizationBound"]["exact"]
    )
    if entry_radius != pinned_entry_radius:
        raise AssertionError("R0.44 entry radius must be the R0.43 negative control")
    if not entry_radius < target_radius < failure_probe_radius:
        raise AssertionError("R0.44 radii are not strictly ordered")

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
    support_charges = [r039.charge(exponent) for exponent in polynomial]
    if min(support_charges) < -1 or max(support_charges) > 2 * maximum_degree:
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
            "forming common-slope tail and canonical-stretch bounds",
            label=label,
            radius=str(radius),
        )
        tail = common_slope_tail_bound(
            polynomial,
            radius,
            maximum_degree,
            charge_cutoff,
        )
        tails[label] = tail
        restarts[label] = r042.restart_diagnostics(
            polynomial,
            residual,
            radius,
            tail,
            maximum_degree,
            ball_divisor,
        )

    progress(show_progress, started, "checking every common-slope breakpoint")
    breakpoint_check = breakpoint_regression(
        r039.weighted_base_terms(polynomial, target_radius),
        tails["target"]["largeChargeSector"],
        maximum_degree,
        charge_cutoff,
    )
    progress(
        show_progress,
        started,
        "checking finite exact large-charge columns",
        charges=len(regression_charges),
        offsets=len(regression_degree_offsets),
    )
    regression = finite_large_charge_regression(
        polynomial,
        target_radius,
        tails["target"],
        regression_charges,
        regression_degree_offsets,
        maximum_degree,
    )

    entry = restarts["entry"]
    target = restarts["target"]
    failure = restarts["failureProbe"]
    entry_tail = rational(entry["tailLinearizationBound"]["exact"])
    target_tail = rational(target["tailLinearizationBound"]["exact"])
    failure_tail = rational(failure["tailLinearizationBound"]["exact"])
    entry_large = rational(tails["entry"]["largeChargeSector"]["bound"]["exact"])
    target_large = rational(tails["target"]["largeChargeSector"]["bound"]["exact"])
    failure_large = rational(
        tails["failureProbe"]["largeChargeSector"]["bound"]["exact"]
    )
    target_finite = rational(
        tails["target"]["maximumFiniteColumn"]["bound"]["exact"]
    )
    failure_finite = rational(
        tails["failureProbe"]["maximumFiniteColumn"]["bound"]["exact"]
    )
    legacy_target = r043.charge_degree_floor_tail_bound(
        polynomial,
        target_radius,
        maximum_degree,
        charge_cutoff,
    )
    legacy_target_large = rational(
        legacy_target["largeChargeSector"]["bound"]["exact"]
    )
    minimum_degree = r043.charge_implied_degree_floor(
        maximum_degree,
        charge_cutoff,
    )
    polynomial_digest = r037.polynomial_digest(polynomial)
    residual_digest = r037.polynomial_digest(residual)
    pinned_polynomial_digest = r043_certificate["restartCertificate"][
        "degreeEightyPolynomialSha256"
    ]
    pinned_residual_digest = r043_certificate["restartCertificate"][
        "exactResidualSha256"
    ]

    checks = {
        "r043CertificateHashMatches": True,
        "r043NegativeControlBecomesEntryRadius": entry_radius == pinned_entry_radius,
        "r043EntryBoundFails": pinned_entry_failure > 1,
        "entryCommonSlopeLargeSectorPasses": entry_large < 1,
        "entryCompleteTailPasses": entry_tail < 1,
        "entryCanonicalFieldsPass": entry["canonicalFieldsPass"],
        "targetExtendsEntryRadius": target_radius > entry_radius,
        "failureProbeIsNextMillesimal": (
            failure_probe_radius - target_radius == Rational(1, 1000)
        ),
        "chargeCutoffExceedsAllCenterCharges": (
            charge_cutoff > 2 * maximum_degree
        ),
        "supportConeImpliesDegreeFloor121": minimum_degree == 121,
        "targetCommonSlopeMaximumIsX2": (
            tails["target"]["largeChargeSector"]["maximumEndpoint"] == "x=2"
        ),
        "targetCommonSlopeStrictlyImprovesR043": target_large < legacy_target_large,
        "targetLegacyLargeSectorFails": legacy_target_large > 1,
        "targetCommonSlopeLargeSectorPasses": target_large < 1,
        "targetWorstFiniteChargeIsMinusOne": (
            tails["target"]["maximumFiniteColumn"]["inputCharge"] == -1
        ),
        "targetFiniteChargeDominatesLargeSector": target_finite > target_large,
        "targetWorstSectorIsMinusOne": tails["target"]["maximumSector"] == "-1",
        "targetTailPasses": target_tail < 1,
        "targetFixedPointPasses": target["fixedPointPasses"],
        "targetStretchPasses": target["stretchPasses"],
        "targetCanonicalFieldsPass": target["canonicalFieldsPass"],
        "targetDirectTransportStillFails": (
            rational(target["directTransportBound"]["exact"]) > 1
        ),
        "failureProbeLargeSectorStillPasses": failure_large < 1,
        "failureProbeWorstFiniteChargeIsMinusOne": (
            tails["failureProbe"]["maximumFiniteColumn"]["inputCharge"] == -1
        ),
        "failureProbeFiniteChargeFails": failure_finite > 1,
        "failureProbeTailFails": failure_tail > 1,
        "failureProbePolynomialStretchStillPasses": (
            rational(
                failure["stretchOperator"]["maximumPolynomialBound"]["exact"]
            )
            < 1
        ),
        "breakpointRegressionsPass": breakpoint_check[
            "allBreakpointsBelowEndpointBound"
        ],
        "finiteLargeChargeRegressionsPass": regression["allBelowSectorBound"],
        "finiteChargeColumnsUnchangedFromR041": (
            tails["target"]["finiteColumns"] == legacy_target["finiteColumns"]
        ),
        "polynomialDigestMatchesR043": polynomial_digest == pinned_polynomial_digest,
        "residualDigestMatchesR043": residual_digest == pinned_residual_digest,
        "residualStartsAboveCutoff": (
            residual_degrees and residual_degrees[0] == maximum_degree + 1
        ),
        "residualEndsAtDoubleCutoff": (
            residual_degrees and residual_degrees[-1] == 2 * maximum_degree
        ),
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise AssertionError(f"R0.44 checks failed: {failed}")

    elapsed = time.perf_counter() - started
    progress(
        show_progress,
        started,
        "all exact checks passed",
        checks=len(checks),
        targetRadius=str(target_radius),
        targetTail=target["tailLinearizationBound"]["exact"],
        failureTail=failure["tailLinearizationBound"]["exact"],
    )
    return {
        "scope": {
            "system": "reduced canonical edge generating system",
            "claim": (
                "all-order common-slope endpoint theorem for the large positive-"
                "charge active-tail sector and exact common-radius restart at 37/100"
            ),
            "notClaimed": [
                "three-dimensional Navier-Stokes global regularity",
                "finite-time blow-up",
                "a singularity at the failed probe",
                "an all-order theorem from finite breakpoint or column checks",
                "the true analytic radius of the reduced system",
            ],
        },
        "git": r039.git_state(source_commit),
        "input": {
            "r043": {
                "path": str(R043_CERTIFICATE),
                "sha256": R043_EXPECTED_SHA256,
                "sourceCommit": r043_certificate["git"]["commit"],
            }
        },
        "allOrderTheorem": {
            "exactColumnFactor": (
                "(i+j)/(i+j-1) * |i*(s/j)-q| * (s-q)/(3*(s+q))"
            ),
            "commonVariables": "x=s/j and y=1/s",
            "supportDomain": (
                "s>=S, j>N, -j<=s<=2j; hence 0<=x<=2 and "
                "j>=J_S=max(N+1,ceil(S/2))"
            ),
            "positiveDomination": (
                "(i+j)/(i+j-1)<=d_i; for q=-1, (s+1)/(s-1)<="
                "(S+1)/(S-1); for q>=0, 0<=(s-q)/(s+q)<=1"
            ),
            "commonSlopeEnvelope": (
                "H_r(x)=sum |a_iq| r^i d_i beta_q |i*x-q|/3"
            ),
            "convexityReduction": (
                "H_r is a positive sum of absolute affine functions, so "
                "sup_{0<=x<=2} H_r(x)=max(H_r(0),H_r(2))"
            ),
            "chargeCoverage": f"every integer input charge s>={charge_cutoff}",
            "degreeCoverage": f"every admissible input degree j>{maximum_degree}",
            "coefficientSignCancellationUsed": False,
            "finiteGridUsedInProof": False,
            "classification": "formal all-order theorem",
        },
        "entryControl": {
            **entry,
            "r043FailedBound": r037.rational_record(pinned_entry_failure),
            "commonSlopeLargeSector": tails["entry"]["largeChargeSector"],
            "statement": (
                "the preassigned R0.43 failure at 0.331 becomes a strict pass"
            ),
        },
        "restartCertificate": {
            **target,
            "entryRadius": r037.rational_record(entry_radius),
            "radiusGainFromR043": r037.rational_record(
                target_radius
                / rational(r043_certificate["restartCertificate"]["radius"]["exact"])
            ),
            "fixedChargeGainFromR043": r037.rational_record(
                (
                    target_radius
                    / rational(
                        r043_certificate["restartCertificate"]["radius"]["exact"]
                    )
                )
                ** 3
            ),
            "polynomialCutoff": maximum_degree,
            "chargeCutoff": charge_cutoff,
            "chargeImpliedDegreeFloor": minimum_degree,
            "r043LargeSectorAtTarget": r037.rational_record(legacy_target_large),
            "commonSlopeLargeSector": tails["target"]["largeChargeSector"],
            "finiteMaximumTailColumn": tails["target"]["maximumFiniteColumn"],
            "degreeEightyPolynomialTerms": len(polynomial),
            "degreeEightyPolynomialSha256": polynomial_digest,
            "exactResidualTerms": len(residual),
            "exactResidualSha256": residual_digest,
            "residualDegreeRange": [residual_degrees[0], residual_degrees[-1]],
            "statement": (
                "the active Banach restart and inherited canonical-stretch "
                "construction certify a, phi, U, and V at radius 37/100"
            ),
        },
        "negativeControl": {
            **failure,
            "commonSlopeLargeSector": tails["failureProbe"]["largeChargeSector"],
            "finiteMaximumTailColumn": tails["failureProbe"]["maximumFiniteColumn"],
            "classification": (
                "the next millesimal radius fails in the inherited s=-1 finite-"
                "charge column while the common-slope large sector still passes; "
                "this is not evidence of a singularity"
            ),
        },
        "finiteRegression": {
            "commonSlopeBreakpoints": breakpoint_check,
            "largeChargeColumns": regression,
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
    parser.add_argument("--entry-radius", default="331/1000")
    parser.add_argument("--target-radius", default="37/100")
    parser.add_argument("--failure-probe-radius", default="371/1000")
    parser.add_argument("--charge-cutoff", type=int, default=241)
    parser.add_argument(
        "--regression-charges",
        type=parse_int_list,
        default=parse_int_list("241,242,243,300,480,600,1000"),
    )
    parser.add_argument(
        "--regression-degree-offsets",
        type=parse_int_list,
        default=parse_int_list("0,3,12"),
    )
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
    if arguments.charge_cutoff <= 2 * arguments.max_total_degree:
        raise SystemExit("--charge-cutoff must exceed twice the polynomial cutoff")
    if arguments.ball_divisor <= 6:
        raise SystemExit("--ball-divisor must exceed 6")
    if any(item < arguments.charge_cutoff for item in arguments.regression_charges):
        raise SystemExit("regression charges must lie in the large-charge sector")
    if any(item < 0 or item % 3 for item in arguments.regression_degree_offsets):
        raise SystemExit("degree offsets must be nonnegative multiples of 3")

    entry_radius = rational(arguments.entry_radius)
    target_radius = rational(arguments.target_radius)
    failure_probe_radius = rational(arguments.failure_probe_radius)
    if not 0 < entry_radius < target_radius < failure_probe_radius:
        raise SystemExit("radii must satisfy 0 < entry < target < failure probe")

    PROGRESS_LOG = arguments.progress_log
    if PROGRESS_LOG is not None:
        PROGRESS_LOG.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_LOG.write_text("", encoding="utf-8")

    payload = build_payload(
        arguments.max_total_degree,
        entry_radius,
        target_radius,
        failure_probe_radius,
        arguments.charge_cutoff,
        arguments.regression_charges,
        arguments.regression_degree_offsets,
        arguments.ball_divisor,
        arguments.progress,
        arguments.source_commit,
    )
    if arguments.check and not all(payload["checks"].values()):
        raise SystemExit("R0.44 checks failed")
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
