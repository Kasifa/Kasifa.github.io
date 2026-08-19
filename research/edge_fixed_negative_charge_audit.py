#!/usr/bin/env python3
"""R0.45 exact fixed-negative-charge tail audit.

For an input tail monomial of charge s=-1 and degree j, put t=1/j.  The
degree-80 center polynomial has charges q>=-1, and the exact weighted column
is a finite sum of rational functions on

    0 <= t <= 1/J,    J=min{j>80: j-1 is divisible by 3}=82.

The q=-1 terms vanish.  The q=0 and q>=2 terms are increasing in t.  The
only decreasing terms have q=1.  Their total negative derivative is bounded
uniformly on the interval, while the degree-one q=2 seed alone contributes
at least 3r.  Exact GMP arithmetic verifies that the resulting derivative
lower bound is positive at the certified radii.  Hence every admissible
tail degree is covered and the exact maximum occurs at j=82; no degree grid
or coefficient-sign cancellation is used in the proof.

The script replaces only the inherited s=-1 column in R0.44, recomputes the
complete Banach restart and canonical-stretch construction, and retains a
few exact degrees as implementation regressions.  It concerns the reduced
canonical edge generating system and does not prove regularity or singularity
for the three-dimensional Navier--Stokes equation.
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
import edge_common_slope_tail_audit as r044
import edge_degree_resolved_tail_audit as r041
import edge_rational_asymptotic_audit as r028
import edge_short_continuation_audit as r036
import edge_stretch_transport_audit as r042
import edge_weighted_restart_audit as r037


Rational = gmpy2.mpq
Polynomial = dict[tuple[int, int], Rational]

R044_CERTIFICATE = Path(
    "research/certificates/r044/edge-common-slope-tail.json"
)
R044_EXPECTED_SHA256 = (
    "7966771f25305211907e11e1a7ab7b6d784b1a14e3db92b3cbec37b96382bb1f"
)
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(
            f"[R0.45 +{elapsed:8.2f}s] {stage}{suffix}",
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


def exact_negative_charge_value(
    terms: list[tuple[int, int, Rational]],
    inverse_degree: Rational,
) -> Rational:
    """Exact s=-1 weighted column as a function F_r(t), t=1/j."""

    value = Rational(0)
    for degree, charge, weighted_coefficient in terms:
        degree_factor = Rational(1) + degree * inverse_degree
        degree_factor /= Rational(1) + (degree - 1) * inverse_degree
        if charge == -1:
            contribution = Rational(0)
        elif charge == 0:
            contribution = degree_factor * degree * inverse_degree / 3
        elif charge == 1:
            # On t<=1/82 and i<=80, 1-i*t is strictly positive.
            contribution = degree_factor * (1 - degree * inverse_degree) / 3
        else:
            contribution = (
                degree_factor
                * (charge + degree * inverse_degree)
                * Rational(charge + 1, 3 * (charge - 1))
            )
        value += weighted_coefficient * contribution
    return value


def negative_charge_endpoint_theorem(
    terms: list[tuple[int, int, Rational]],
    minimum_degree: int,
) -> dict[str, object]:
    """Certify F'_r(t)>0 on [0,1/J] and return the exact endpoint."""

    upper_t = Rational(1, minimum_degree)
    q_one_terms = [item for item in terms if item[1] == 1]
    obstruction = sum(
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
    seed_matches = [
        coefficient
        for degree, charge, coefficient in terms
        if degree == 1 and charge == 2
    ]
    if len(seed_matches) != 1:
        raise AssertionError("expected one degree-one q=2 seed")
    seed_weight = seed_matches[0]
    seed_derivative_lower_bound = 3 * seed_weight
    derivative_margin = seed_derivative_lower_bound - obstruction
    endpoint_at_infinity = exact_negative_charge_value(terms, Rational(0))
    endpoint_at_minimum = exact_negative_charge_value(terms, upper_t)
    if derivative_margin <= 0:
        raise AssertionError("fixed s=-1 derivative lower bound is not positive")
    return {
        "inputCharge": -1,
        "minimumTailDegree": minimum_degree,
        "admissibleDegreeLattice": f"j>80 and j congruent to 1 modulo 3",
        "inverseDegreeInterval": [
            r037.rational_record(Rational(0)),
            r037.rational_record(upper_t),
        ],
        "qOneTermCount": len(q_one_terms),
        "qOneNegativeDerivativeUpperBound": r037.rational_record(obstruction),
        "degreeOneQTwoSeedWeight": r037.rational_record(seed_weight),
        "seedDerivativeLowerBound": r037.rational_record(
            seed_derivative_lower_bound
        ),
        "fullDerivativeLowerBound": r037.rational_record(derivative_margin),
        "endpointAtInfinity": r037.rational_record(endpoint_at_infinity),
        "endpointAtMinimumDegree": r037.rational_record(endpoint_at_minimum),
        "maximumEndpoint": "j=82",
        "bound": r037.rational_record(endpoint_at_minimum),
        "proof": (
            "q=-1 terms vanish; q=0 and q>=2 terms increase with t=1/j; "
            "only q=1 terms decrease. Their derivative magnitude is at most "
            "Qhat on 0<=t<=1/82, while the (i,q)=(1,2) seed contributes "
            "r(3+2t)>=3r. The exact inequality 3r-Qhat>0 makes the complete "
            "column strictly increasing in t, so its maximum is the true "
            "lattice endpoint j=82."
        ),
        "coefficientSignCancellationUsed": False,
        "finiteDegreeGridUsedInProof": False,
        "classification": (
            "all-order exact fixed-charge theorem covering every admissible "
            "tail degree j>80 at input charge s=-1"
        ),
    }


def fixed_negative_charge_tail_bound(
    polynomial: Polynomial,
    radius: Rational,
    cutoff: int,
    charge_cutoff: int,
) -> dict[str, object]:
    """Replace the inherited R0.44 s=-1 bound by its exact endpoint theorem."""

    inherited = r044.common_slope_tail_bound(
        polynomial,
        radius,
        cutoff,
        charge_cutoff,
    )
    minimum_degree = r039.minimum_tail_degree(-1, cutoff)
    theorem = negative_charge_endpoint_theorem(
        r039.weighted_base_terms(polynomial, radius),
        minimum_degree,
    )
    inherited_minus_one = next(
        record for record in inherited["finiteColumns"] if record["inputCharge"] == -1
    )
    exact_value = rational(theorem["bound"]["exact"])
    direct_value = r041.exact_tail_column(
        polynomial,
        radius,
        minimum_degree,
        -1,
    )
    if exact_value != direct_value:
        raise AssertionError("closed s=-1 endpoint does not match exact column")

    columns = [
        theorem if record["inputCharge"] == -1 else record
        for record in inherited["finiteColumns"]
    ]
    finite_maximum = max(
        columns,
        key=lambda record: rational(record["bound"]["exact"]),
    )
    finite_value = rational(finite_maximum["bound"]["exact"])
    large_value = rational(inherited["largeChargeSector"]["bound"]["exact"])
    if large_value > finite_value:
        maximum_value = large_value
        maximum_sector = f">={charge_cutoff}"
    else:
        maximum_value = finite_value
        maximum_sector = str(finite_maximum["inputCharge"])
    digest_input = [
        (str(record["inputCharge"]), rational(record["bound"]["exact"]))
        for record in columns
    ]
    digest_input.append((f">={charge_cutoff}", large_value))
    return {
        **inherited,
        "finiteColumns": columns,
        "maximumFiniteColumn": finite_maximum,
        "maximumBound": r037.rational_record(maximum_value),
        "maximumSector": maximum_sector,
        "columnBoundsSha256": r041.digest_records(digest_input),
        "fixedNegativeChargeTheorem": theorem,
        "inheritedR044NegativeChargeBound": inherited_minus_one["bound"],
        "classification": (
            "all-order induced weighted-l1 bound covering every tail charge "
            "and degree, with an exact monotonic endpoint theorem for s=-1"
        ),
    }


def negative_charge_degree_regression(
    polynomial: Polynomial,
    radius: Rational,
    tail: dict[str, object],
    degree_offsets: list[int],
) -> dict[str, object]:
    """Finite exact degree checks; these are not used in the proof."""

    minimum_degree = tail["fixedNegativeChargeTheorem"]["minimumTailDegree"]
    endpoint = rational(tail["fixedNegativeChargeTheorem"]["bound"]["exact"])
    records = []
    digest_input = []
    previous: Rational | None = None
    for offset in degree_offsets:
        degree = minimum_degree + offset
        if (degree - 1) % 3:
            raise AssertionError("degree offset left the s=-1 lattice")
        value = r041.exact_tail_column(polynomial, radius, degree, -1)
        records.append(
            {
                "inputDegree": degree,
                "inverseDegree": r037.rational_record(Rational(1, degree)),
                "exactColumn": r037.rational_record(value),
                "atOrBelowEndpoint": value <= endpoint,
                "strictlyBelowPrevious": previous is None or value < previous,
                "classification": "finite exact implementation regression only",
            }
        )
        digest_input.append((str(degree), value))
        previous = value
    return {
        "inputCharge": -1,
        "degreeOffsets": degree_offsets,
        "records": records,
        "strictlyDecreasingWithDegree": all(
            record["strictlyBelowPrevious"] for record in records
        ),
        "allAtOrBelowEndpoint": all(record["atOrBelowEndpoint"] for record in records),
        "exactColumnsSha256": r041.digest_records(digest_input),
        "classification": (
            "finite exact regression only; infinite degree coverage follows "
            "from the derivative theorem"
        ),
    }


def build_payload(
    maximum_degree: int,
    entry_radius: Rational,
    target_radius: Rational,
    failure_probe_radius: Rational,
    charge_cutoff: int,
    regression_degree_offsets: list[int],
    ball_divisor: int,
    show_progress: bool,
    source_commit: str | None,
) -> dict[str, object]:
    started = time.perf_counter()
    progress(show_progress, started, "loading pinned R0.44 certificate")
    if sha256(R044_CERTIFICATE) != R044_EXPECTED_SHA256:
        raise AssertionError("R0.44 certificate hash mismatch")
    r044_certificate = json.loads(R044_CERTIFICATE.read_text(encoding="utf-8"))
    pinned_entry = rational(r044_certificate["restartCertificate"]["radius"]["exact"])
    pinned_target = rational(r044_certificate["negativeControl"]["radius"]["exact"])
    pinned_target_failure = rational(
        r044_certificate["negativeControl"]["tailLinearizationBound"]["exact"]
    )
    if entry_radius != pinned_entry or target_radius != pinned_target:
        raise AssertionError("R0.45 entry and target must be pinned by R0.44")
    if not entry_radius < target_radius < failure_probe_radius:
        raise AssertionError("R0.45 radii are not strictly ordered")

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
    progress(show_progress, started, "forming complete polynomial residual")
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
            "forming exact s=-1 tail and canonical-stretch bounds",
            label=label,
            radius=str(radius),
        )
        tail = fixed_negative_charge_tail_bound(
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

    progress(show_progress, started, "checking finite exact s=-1 columns")
    regression = negative_charge_degree_regression(
        polynomial,
        target_radius,
        tails["target"],
        regression_degree_offsets,
    )

    entry = restarts["entry"]
    target = restarts["target"]
    failure = restarts["failureProbe"]
    entry_tail = rational(entry["tailLinearizationBound"]["exact"])
    target_tail = rational(target["tailLinearizationBound"]["exact"])
    failure_tail = rational(failure["tailLinearizationBound"]["exact"])
    target_inherited = rational(
        tails["target"]["inheritedR044NegativeChargeBound"]["exact"]
    )
    target_large = rational(tails["target"]["largeChargeSector"]["bound"]["exact"])
    failure_large = rational(
        tails["failureProbe"]["largeChargeSector"]["bound"]["exact"]
    )
    target_theorem = tails["target"]["fixedNegativeChargeTheorem"]
    failure_theorem = tails["failureProbe"]["fixedNegativeChargeTheorem"]
    target_derivative_margin = rational(
        target_theorem["fullDerivativeLowerBound"]["exact"]
    )
    failure_derivative_margin = rational(
        failure_theorem["fullDerivativeLowerBound"]["exact"]
    )
    polynomial_digest = r037.polynomial_digest(polynomial)
    residual_digest = r037.polynomial_digest(residual)
    pinned_polynomial_digest = r044_certificate["restartCertificate"][
        "degreeEightyPolynomialSha256"
    ]
    pinned_residual_digest = r044_certificate["restartCertificate"][
        "exactResidualSha256"
    ]

    checks = {
        "r044CertificateHashMatches": True,
        "r044CertifiedRadiusBecomesEntry": entry_radius == pinned_entry,
        "r044FailureProbeBecomesTarget": target_radius == pinned_target,
        "r044InheritedTargetBoundFails": pinned_target_failure > 1,
        "r044InheritedTargetBoundReproduced": target_inherited == pinned_target_failure,
        "entryCompleteTailPasses": entry_tail < 1,
        "entryCanonicalFieldsPass": entry["canonicalFieldsPass"],
        "targetExtendsEntryRadius": target_radius > entry_radius,
        "failureProbeIsNextMillesimal": (
            failure_probe_radius - target_radius == Rational(1, 1000)
        ),
        "chargeCutoffExceedsAllCenterCharges": charge_cutoff > 2 * maximum_degree,
        "minusOneMinimumDegreeIs82": target_theorem["minimumTailDegree"] == 82,
        "targetHasTwentySevenQOneTerms": target_theorem["qOneTermCount"] == 27,
        "targetDerivativeMarginPositive": target_derivative_margin > 0,
        "failureDerivativeMarginPositive": failure_derivative_margin > 0,
        "targetExactEndpointStrictlyImprovesInheritedBound": target_tail < target_inherited,
        "targetExactEndpointPasses": target_tail < 1,
        "targetLargeSectorPasses": target_large < 1,
        "targetWorstSectorIsMinusOne": tails["target"]["maximumSector"] == "-1",
        "targetFixedPointPasses": target["fixedPointPasses"],
        "targetStretchPasses": target["stretchPasses"],
        "targetCanonicalFieldsPass": target["canonicalFieldsPass"],
        "targetDirectTransportStillFails": rational(target["directTransportBound"]["exact"]) > 1,
        "failureProbeLargeSectorStillPasses": failure_large < 1,
        "failureProbeExactMinusOneColumnFails": failure_tail > 1,
        "failureProbeWorstSectorIsMinusOne": tails["failureProbe"]["maximumSector"] == "-1",
        "failureProbeFixedPointFails": not failure["fixedPointPasses"],
        "failureProbePolynomialStretchStillPasses": (
            rational(failure["stretchOperator"]["maximumPolynomialBound"]["exact"]) < 1
        ),
        "finiteDegreeRegressionsDecrease": regression["strictlyDecreasingWithDegree"],
        "finiteDegreeRegressionsBelowEndpoint": regression["allAtOrBelowEndpoint"],
        "polynomialDigestMatchesR044": polynomial_digest == pinned_polynomial_digest,
        "residualDigestMatchesR044": residual_digest == pinned_residual_digest,
        "residualStartsAboveCutoff": residual_degrees[0] == maximum_degree + 1,
        "residualEndsAtDoubleCutoff": residual_degrees[-1] == 2 * maximum_degree,
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise AssertionError(f"R0.45 checks failed: {failed}")

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
                "all-order exact s=-1 endpoint theorem and exact common-radius "
                "restart at 371/1000"
            ),
            "notClaimed": [
                "three-dimensional Navier-Stokes global regularity",
                "finite-time blow-up",
                "a singularity at the failed probe",
                "an all-order theorem from finite degree checks",
                "the true analytic radius of the reduced system",
            ],
        },
        "git": r039.git_state(source_commit),
        "input": {
            "r044": {
                "path": str(R044_CERTIFICATE),
                "sha256": R044_EXPECTED_SHA256,
                "sourceCommit": r044_certificate["git"]["commit"],
            }
        },
        "allOrderTheorem": {
            "exactVariable": "t=1/j",
            "domain": "s=-1, j>80, j congruent to 1 modulo 3; 0<=t<=1/82",
            "exactTermForQNotOne": (
                "|a_iq| r^i (1+i*t)/(1+(i-1)*t) "
                "|q+i*t| |q+1|/(3|q-1|)"
            ),
            "exactTermForQOne": (
                "|a_i1| r^i (1-i^2*t^2)/(3(1+(i-1)*t))"
            ),
            "signClassification": (
                "q=-1 terms vanish; q=0 and q>=2 terms increase; only q=1 "
                "terms decrease"
            ),
            "negativeDerivativeBound": (
                "Qhat_r(T)=sum_i |a_i1|r^i[(i-1)+2i^2T+i^2(i-1)T^2]/3"
            ),
            "positiveSeedBound": "the (i,q)=(1,2) seed gives r(3+2t)>=3r",
            "conclusion": (
                "F'_r(t)>=3r-Qhat_r(1/82)>0, so the exact maximum over every "
                "admissible tail degree is F_r(1/82), the j=82 column"
            ),
            "targetCertificate": target_theorem,
            "coefficientSignCancellationUsed": False,
            "finiteDegreeGridUsedInProof": False,
            "classification": "formal all-order fixed-charge theorem",
        },
        "entryControl": {
            **entry,
            "exactNegativeChargeColumn": tails["entry"]["fixedNegativeChargeTheorem"],
            "commonSlopeLargeSector": tails["entry"]["largeChargeSector"],
            "statement": "the R0.44 certified radius remains a strict pass",
        },
        "restartCertificate": {
            **target,
            "entryRadius": r037.rational_record(entry_radius),
            "radiusGainFromR044": r037.rational_record(target_radius / entry_radius),
            "fixedChargeGainFromR044": r037.rational_record((target_radius / entry_radius) ** 3),
            "polynomialCutoff": maximum_degree,
            "chargeCutoff": charge_cutoff,
            "r044InheritedNegativeChargeBound": tails["target"]["inheritedR044NegativeChargeBound"],
            "exactNegativeChargeColumn": target_theorem,
            "commonSlopeLargeSector": tails["target"]["largeChargeSector"],
            "finiteMaximumTailColumn": tails["target"]["maximumFiniteColumn"],
            "degreeEightyPolynomialTerms": len(polynomial),
            "degreeEightyPolynomialSha256": polynomial_digest,
            "exactResidualTerms": len(residual),
            "exactResidualSha256": residual_digest,
            "residualDegreeRange": [residual_degrees[0], residual_degrees[-1]],
            "statement": (
                "the active Banach restart and inherited canonical-stretch "
                "construction certify a, phi, U, and V at radius 371/1000"
            ),
        },
        "negativeControl": {
            **failure,
            "exactNegativeChargeColumn": failure_theorem,
            "commonSlopeLargeSector": tails["failureProbe"]["largeChargeSector"],
            "finiteMaximumTailColumn": tails["failureProbe"]["maximumFiniteColumn"],
            "classification": (
                "the next millesimal radius fails by the exact j=82, s=-1 "
                "induced column while the large sector and polynomial stretch "
                "still pass; this is not evidence of a singularity"
            ),
        },
        "finiteRegression": {
            "negativeChargeDegrees": regression,
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
    parser.add_argument("--entry-radius", default="37/100")
    parser.add_argument("--target-radius", default="371/1000")
    parser.add_argument("--failure-probe-radius", default="372/1000")
    parser.add_argument("--charge-cutoff", type=int, default=241)
    parser.add_argument(
        "--regression-degree-offsets",
        type=parse_int_list,
        default=parse_int_list("0,3,6,18,918"),
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
        arguments.regression_degree_offsets,
        arguments.ball_divisor,
        arguments.progress,
        arguments.source_commit,
    )
    if arguments.check and not all(payload["checks"].values()):
        raise SystemExit("R0.45 checks failed")
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
