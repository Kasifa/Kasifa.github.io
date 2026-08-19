#!/usr/bin/env python3
"""R0.43 exact charge-implied degree-floor audit.

R0.42 left one all-order active-tail sector unresolved at r=33/100.  For a
base monomial of degree i and charge q and a tail input of degree j and
charge s, that sector used s>=S but retained only the generic tail fact
j>N in the degree prefactor

    (i+j)/(i+j-1).

The bivariate support cone also gives s<=2j.  Hence every input in the large
positive-charge sector satisfies

    j >= max(N+1, ceil(S/2)).

For N=80 and S=241 this raises the uniform degree floor from 81 to 121.
The remaining R0.39 large-charge estimates are unchanged: q=-1 uses
(s+1)/(s-1)<=(S+1)/(S-1), while q>=0 uses
(s-q)/(s+q)<=1 and convexity of |i(s/j)-q| on 0<=s/j<=2.

This script replaces only that degree prefactor, preserves every finite
charge column from R0.41, and re-runs the complete Banach restart and R0.42
canonical-stretch construction.  All threshold decisions use exact GMP
rationals.  Finite column scans check the implementation only.  The theorem
concerns the reduced canonical edge generating system and does not prove
three-dimensional Navier--Stokes regularity or singularity.
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

import edge_charge_resolved_audit as r039
import edge_degree_resolved_tail_audit as r041
import edge_rational_asymptotic_audit as r028
import edge_short_continuation_audit as r036
import edge_stretch_transport_audit as r042
import edge_weighted_restart_audit as r037


Rational = gmpy2.mpq
Polynomial = dict[tuple[int, int], Rational]

R042_CERTIFICATE = Path(
    "research/certificates/r042/edge-stretch-transport.json"
)
R042_EXPECTED_SHA256 = (
    "0c426070c47afb519fc9c705cbe11ed59b82ee6b28e766696280379b15e5dfa5"
)
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(
            f"[R0.43 +{elapsed:8.2f}s] {stage}{suffix}",
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


def charge_implied_degree_floor(cutoff: int, charge_cutoff: int) -> int:
    """Uniform j floor from j>N and s>=S with the support condition s<=2j."""

    return max(cutoff + 1, (charge_cutoff + 1) // 2)


def large_charge_degree_floor_factor(
    base_degree: int,
    base_charge: int,
    cutoff: int,
    charge_cutoff: int,
) -> Rational:
    """Uniform large-positive-charge column factor with the sharper j floor."""

    if charge_cutoff <= 2 * cutoff:
        raise ValueError("large-charge cutoff must exceed every center charge")
    minimum_degree = charge_implied_degree_floor(cutoff, charge_cutoff)
    degree_factor = Rational(
        base_degree + minimum_degree,
        base_degree + minimum_degree - 1,
    )
    if base_charge == -1:
        return (
            degree_factor
            * (2 * base_degree + 1)
            * Rational(charge_cutoff + 1, 3 * (charge_cutoff - 1))
        )
    if base_charge < -1:
        raise AssertionError("large-charge bound received q<-1")
    return (
        degree_factor
        * max(base_charge, abs(2 * base_degree - base_charge))
        / 3
    )


def grouped_large_charge_contributions(
    terms: list[tuple[int, int, Rational]],
    cutoff: int,
    charge_cutoff: int,
) -> list[dict[str, object]]:
    groups = (
        ("q=-1", lambda q: q == -1),
        ("q=0", lambda q: q == 0),
        ("q=1", lambda q: q == 1),
        ("q=2", lambda q: q == 2),
        ("q>=3", lambda q: q >= 3),
    )
    records = []
    for label, predicate in groups:
        legacy = Rational(0)
        improved = Rational(0)
        for base_degree, base_charge, weighted_coefficient in terms:
            if not predicate(base_charge):
                continue
            legacy += weighted_coefficient * r039.large_charge_factor(
                base_degree,
                base_charge,
                cutoff,
                charge_cutoff,
            )
            improved += weighted_coefficient * large_charge_degree_floor_factor(
                base_degree,
                base_charge,
                cutoff,
                charge_cutoff,
            )
        records.append(
            {
                "baseChargeGroup": label,
                "legacyContribution": r037.rational_record(legacy),
                "improvedContribution": r037.rational_record(improved),
                "reduction": r037.rational_record(legacy - improved),
            }
        )
    return records


def charge_degree_floor_tail_bound(
    polynomial: Polynomial,
    radius: Rational,
    cutoff: int,
    charge_cutoff: int,
) -> dict[str, object]:
    """R0.41 finite columns plus the charge-implied large-sector floor."""

    inherited = r041.degree_resolved_tail_bound(
        polynomial,
        radius,
        cutoff,
        charge_cutoff,
    )
    terms = r039.weighted_base_terms(polynomial, radius)
    legacy_large = sum(
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
    improved_large = sum(
        (
            weighted_coefficient
            * large_charge_degree_floor_factor(
                base_degree,
                base_charge,
                cutoff,
                charge_cutoff,
            )
            for base_degree, base_charge, weighted_coefficient in terms
        ),
        Rational(0),
    )
    finite_maximum = inherited["maximumFiniteColumn"]
    finite_maximum_value = rational(finite_maximum["bound"]["exact"])
    if improved_large > finite_maximum_value:
        maximum_value = improved_large
        maximum_sector = f">={charge_cutoff}"
    else:
        maximum_value = finite_maximum_value
        maximum_sector = str(finite_maximum["inputCharge"])

    digest_input = [
        (str(record["inputCharge"]), rational(record["bound"]["exact"]))
        for record in inherited["finiteColumns"]
    ]
    digest_input.append((f">={charge_cutoff}", improved_large))
    minimum_degree = charge_implied_degree_floor(cutoff, charge_cutoff)
    large_record = {
        "inputChargeRange": [charge_cutoff, None],
        "genericTailDegreeFloor": cutoff + 1,
        "chargeImpliedDegreeFloor": minimum_degree,
        "supportImplication": (
            "s>=S and s<=2j imply j>=ceil(S/2); combine with j>N"
        ),
        "legacyBound": r037.rational_record(legacy_large),
        "bound": r037.rational_record(improved_large),
        "strictReduction": r037.rational_record(legacy_large - improved_large),
        "baseChargeContributions": grouped_large_charge_contributions(
            terms,
            cutoff,
            charge_cutoff,
        ),
        "classification": (
            "all-order analytic sector covering every s>=S and j>N; the "
            "bivariate support cone supplies the uniform degree floor"
        ),
    }
    return {
        **inherited,
        "largeChargeSector": large_record,
        "maximumBound": r037.rational_record(maximum_value),
        "maximumSector": maximum_sector,
        "columnBoundsSha256": r041.digest_records(digest_input),
        "classification": (
            "all-order induced weighted-l1 bound covering every charge and "
            "every degree above the polynomial cutoff, with the large "
            "positive-charge sector coupled to its support-implied degree floor"
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
    """Finite exact large-sector columns; the theorem itself is analytic."""

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
            record = {
                "inputCharge": input_charge,
                "inputDegree": input_degree,
                "exactColumn": r037.rational_record(value),
                "allOrderLargeSectorBound": r037.rational_record(sector_bound),
                "belowSectorBound": value <= sector_bound,
                "classification": "finite exact implementation regression only",
            }
            records.append(record)
            digest_input.append((f"{input_charge}:{input_degree}", value))
    return {
        "inputCharges": charges,
        "degreeOffsetsFromMinimum": degree_offsets,
        "columnsChecked": len(records),
        "records": records,
        "allBelowSectorBound": all(record["belowSectorBound"] for record in records),
        "exactColumnsSha256": r041.digest_records(digest_input),
        "classification": (
            "finite exact regression only; all-order coverage follows from "
            "the support cone and the analytic termwise bounds"
        ),
    }


def build_payload(
    maximum_degree: int,
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
    progress(show_progress, started, "loading pinned R0.42 certificate")
    if sha256(R042_CERTIFICATE) != R042_EXPECTED_SHA256:
        raise AssertionError("R0.42 certificate hash mismatch")
    r042_certificate = json.loads(R042_CERTIFICATE.read_text(encoding="utf-8"))
    previous_radius = rational(
        r042_certificate["restartCertificate"]["radius"]["exact"]
    )
    preassigned_target = rational(
        r042_certificate["negativeControl"]["radius"]["exact"]
    )
    pinned_legacy_target = rational(
        r042_certificate["negativeControl"]["tailLinearizationBound"]["exact"]
    )
    if target_radius != preassigned_target:
        raise AssertionError("R0.43 target must be the R0.42 negative control")
    if not previous_radius < target_radius < failure_probe_radius:
        raise AssertionError("radii are not ordered beyond R0.42")

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

    tails = {}
    restarts = {}
    for label, radius in (
        ("previous", previous_radius),
        ("target", target_radius),
        ("failureProbe", failure_probe_radius),
    ):
        progress(
            show_progress,
            started,
            "forming charge-degree coupled tail and stretch bounds",
            label=label,
            radius=str(radius),
        )
        tail = charge_degree_floor_tail_bound(
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

    legacy_target = r041.degree_resolved_tail_bound(
        polynomial,
        target_radius,
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

    target = restarts["target"]
    failure = restarts["failureProbe"]
    target_tail = rational(target["tailLinearizationBound"]["exact"])
    failure_tail = rational(failure["tailLinearizationBound"]["exact"])
    target_legacy = rational(legacy_target["maximumBound"]["exact"])
    target_large = rational(tails["target"]["largeChargeSector"]["bound"]["exact"])
    target_finite = rational(
        tails["target"]["maximumFiniteColumn"]["bound"]["exact"]
    )
    degree_floor = charge_implied_degree_floor(maximum_degree, charge_cutoff)
    polynomial_digest = r037.polynomial_digest(polynomial)
    residual_digest = r037.polynomial_digest(residual)

    checks = {
        "r042CertificateHashMatches": True,
        "r042NegativeControlBecomesPreassignedTarget": (
            target_radius == preassigned_target
        ),
        "legacyTargetMatchesPinnedR042Failure": (
            target_legacy == pinned_legacy_target
        ),
        "legacyTargetFails": target_legacy > 1,
        "supportConeImpliesDegreeFloor121": degree_floor == 121,
        "chargeCutoffExceedsAllCenterCharges": charge_cutoff > 2 * maximum_degree,
        "improvedLargeSectorIsStrictlySmaller": target_large < target_legacy,
        "targetWorstSectorRemainsLargeCharge": (
            tails["target"]["maximumSector"] == f">={charge_cutoff}"
        ),
        "targetLargeSectorDominatesFiniteColumns": target_large > target_finite,
        "targetTailPasses": target_tail < 1,
        "targetFixedPointPasses": target["fixedPointPasses"],
        "targetStretchPasses": target["stretchPasses"],
        "targetCanonicalFieldsPass": target["canonicalFieldsPass"],
        "failureProbeIsNextMillesimal": (
            failure_probe_radius - target_radius == Rational(1, 1000)
        ),
        "failureProbeTailFails": failure_tail > 1,
        "failureProbePolynomialStretchStillPasses": (
            rational(
                failure["stretchOperator"]["maximumPolynomialBound"]["exact"]
            )
            < 1
        ),
        "finiteLargeChargeRegressionsPass": regression["allBelowSectorBound"],
        "finiteChargeColumnsUnchangedFromR041": (
            tails["target"]["finiteColumns"] == legacy_target["finiteColumns"]
        ),
        "polynomialDigestMatchesR042": (
            polynomial_digest
            == r042_certificate["restartCertificate"][
                "degreeEightyPolynomialSha256"
            ]
        ),
        "residualDigestMatchesR042": (
            residual_digest
            == r042_certificate["restartCertificate"]["exactResidualSha256"]
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
        raise AssertionError(f"R0.43 checks failed: {failed}")

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
                "all-order charge-implied degree floor in the large positive-"
                "charge active-tail sector and exact common-radius restart at "
                "33/100"
            ),
            "notClaimed": [
                "three-dimensional Navier-Stokes global regularity",
                "finite-time blow-up",
                "a singularity at the failed probe",
                "an all-order theorem from finite column checks",
                "the true analytic radius of the reduced system",
            ],
        },
        "git": r039.git_state(source_commit),
        "input": {
            "r042": {
                "path": str(R042_CERTIFICATE),
                "sha256": R042_EXPECTED_SHA256,
                "sourceCommit": r042_certificate["git"]["commit"],
            }
        },
        "allOrderTheorem": {
            "largeChargeHypothesis": f"s>={charge_cutoff}",
            "bivariateSupport": "-j<=s<=2j",
            "strictTailHypothesis": f"j>{maximum_degree}",
            "degreeFloorFormula": "j>=max(N+1,ceil(S/2))",
            "genericDegreeFloor": maximum_degree + 1,
            "chargeImpliedDegreeFloor": degree_floor,
            "oldDegreeFactor": "(i+N+1)/(i+N)",
            "newDegreeFactor": "(i+J_S)/(i+J_S-1)",
            "qMinusOneBounds": (
                "(s+1)/(s-1)<=(S+1)/(S-1) and |i(s/j)+1|<=2i+1"
            ),
            "nonnegativeChargeBounds": (
                "(s-q)/(s+q)<=1 and |i(s/j)-q|<="
                "max(q,|2i-q|) on 0<=s/j<=2"
            ),
            "degreeCoverage": "every j>N in the bivariate support cone",
            "chargeCoverage": f"every integer input charge s>={charge_cutoff}",
            "classification": "formal all-order theorem",
        },
        "legacyFailureAtTarget": {
            "radius": r037.rational_record(target_radius),
            "tailBound": r037.rational_record(target_legacy),
            "source": "R0.42 negative control using the R0.41 large sector",
        },
        "previousRadiusControl": {
            **restarts["previous"],
            "classification": "R0.42 radius recomputed with the sharper theorem",
        },
        "restartCertificate": {
            **target,
            "previousRadius": r037.rational_record(previous_radius),
            "radiusGainFromR042": r037.rational_record(
                target_radius / previous_radius
            ),
            "fixedChargeGainFromR042": r037.rational_record(
                (target_radius / previous_radius) ** 3
            ),
            "polynomialCutoff": maximum_degree,
            "chargeCutoff": charge_cutoff,
            "chargeImpliedDegreeFloor": degree_floor,
            "finiteMaximumTailColumn": r037.rational_record(target_finite),
            "largeChargeTailSector": tails["target"]["largeChargeSector"],
            "degreeEightyPolynomialTerms": len(polynomial),
            "degreeEightyPolynomialSha256": polynomial_digest,
            "exactResidualTerms": len(residual),
            "exactResidualSha256": residual_digest,
            "residualDegreeRange": [residual_degrees[0], residual_degrees[-1]],
            "statement": (
                "the active Banach restart and the inherited canonical-stretch "
                "construction certify a, phi, U, and V at radius 33/100"
            ),
        },
        "negativeControl": {
            **failure,
            "classification": (
                "the next millesimal radius fails the improved all-order active-"
                "tail inequality; this is not evidence of a singularity or "
                "loss of analyticity"
            ),
        },
        "finiteRegression": {
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
    parser.add_argument("--target-radius", default="33/100")
    parser.add_argument("--failure-probe-radius", default="331/1000")
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
        raise SystemExit("regression degree offsets must be nonnegative multiples of 3")

    target_radius = rational(arguments.target_radius)
    failure_probe_radius = rational(arguments.failure_probe_radius)
    if not 0 < target_radius < failure_probe_radius:
        raise SystemExit("radii must satisfy 0 < target < failure probe")

    PROGRESS_LOG = arguments.progress_log
    if PROGRESS_LOG is not None:
        PROGRESS_LOG.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_LOG.write_text("", encoding="utf-8")

    payload = build_payload(
        arguments.max_total_degree,
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
        raise SystemExit("R0.43 checks failed")
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
