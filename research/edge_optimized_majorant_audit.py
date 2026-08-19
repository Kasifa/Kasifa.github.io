#!/usr/bin/env python3
"""R0.31 exact audit for the improved all-order edge majorant.

R0.30 used the deliberately coarse convolution estimate H_L < 32.  The
split estimate proved in R0.31 gives

    H_2 = 8,
    H_L <= 27/4 for every L >= 3.

The finite part of that proof checks L=3,...,296 over exact GMP rationals.
For L>=297, a closed rational upper bound is already below 27/4.  This
improves the majorant constant from 96 to K=81/4 and gives a common analytic
polydisc max(|Z|,|W|)<4/81 for a, U, V, and their logarithmic canonical
factorization.

The theorem is for the reduced two-variable edge system.  The degree-limited
recurrence below is an implementation regression, not the all-order proof and
not a Navier--Stokes regularity or singularity theorem.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import sys
import time

import gmpy2

import edge_analytic_majorant_audit as r030
import edge_canonical_transport_audit as r029
import edge_rational_asymptotic_audit as r028


Rational = gmpy2.mpq
Field = r028.RationalField
K_MAJORANT = Rational(81, 4)
KERNEL_BOUND = Rational(27, 4)
FINITE_KERNEL_MAXIMUM_DEGREE = 296
TAIL_START_DEGREE = 297
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, message: str) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        print(f"[R0.31 +{elapsed:8.2f}s] {message}", file=sys.stderr, flush=True)
    if PROGRESS_LOG is not None:
        record = {
            "timestampUtc": datetime.now(timezone.utc).isoformat(),
            "elapsedSeconds": elapsed,
            "stage": message,
        }
        with PROGRESS_LOG.open("a", encoding="utf-8") as target:
            target.write(json.dumps(record, ensure_ascii=False) + "\n")
            target.flush()
            os.fsync(target.fileno())


def tail_kernel_upper_bound(degree: int) -> Rational:
    """Return the R0.31 closed bound valid for degree at least 297."""

    return Rational(10000, 2187) + Rational(640, degree) + Rational(
        1600, degree**2
    )


def kernel_proof_certificate() -> dict[str, object]:
    head = sum((Rational(1, n**2) for n in range(1, 6)), Rational(0))
    convex_tail = Rational(2, 11)
    zeta_upper = head + convex_tail
    records: list[dict[str, object]] = []
    maximum_after_degree_two = (Rational(0), 0)
    failures: list[dict[str, object]] = []

    for degree in range(2, FINITE_KERNEL_MAXIMUM_DEGREE + 1):
        value = r030.convolution_constant(degree)
        records.append({"totalDegree": degree, **r030.rational_record(value)})
        if degree >= 3 and value > maximum_after_degree_two[0]:
            maximum_after_degree_two = (value, degree)
        expected_bound = Rational(8) if degree == 2 else KERNEL_BOUND
        if value > expected_bound:
            failures.append(
                {
                    "totalDegree": degree,
                    "value": str(value),
                    "bound": str(expected_bound),
                }
            )

    tail_at_threshold = tail_kernel_upper_bound(TAIL_START_DEGREE)
    if not zeta_upper < Rational(5, 3):
        failures.append({"check": "zeta(2) < 5/3", "value": str(zeta_upper)})
    if not tail_at_threshold < KERNEL_BOUND:
        failures.append(
            {
                "check": "tail bound at threshold",
                "value": str(tail_at_threshold),
                "bound": str(KERNEL_BOUND),
            }
        )
    if maximum_after_degree_two != (KERNEL_BOUND, 3):
        failures.append(
            {
                "check": "finite maximum for L>=3",
                "degree": maximum_after_degree_two[1],
                "value": str(maximum_after_degree_two[0]),
            }
        )

    return {
        "passed": not failures,
        "definition": "H_L=L^3 sum_(i+j=L) min(i,j)/(i^3 j^3)",
        "theorem": "H_2=8 and H_L<=27/4 for every integer L>=3",
        "finiteExactRange": {
            "minimumTotalDegree": 2,
            "maximumTotalDegree": FINITE_KERNEL_MAXIMUM_DEGREE,
            "backend": "GMP rational arithmetic",
            "records": records,
        },
        "finiteMaximumForDegreeAtLeastThree": {
            "degree": maximum_after_degree_two[1],
            **r030.rational_record(maximum_after_degree_two[0]),
        },
        "analyticTail": {
            "startsAtTotalDegree": TAIL_START_DEGREE,
            "split": "1<=i<=L/10 and L/10<i<=L/2",
            "zetaTwoUpperCertificate": {
                "firstFiveTerms": str(head),
                "convexMidpointTail": str(convex_tail),
                "sum": str(zeta_upper),
                "target": "5/3",
                "gap": str(Rational(5, 3) - zeta_upper),
            },
            "upperBoundFormula": "10000/2187 + 640/L + 1600/L^2",
            "valueAtThreshold": r030.rational_record(tail_at_threshold),
            "target": r030.rational_record(KERNEL_BOUND),
            "monotonicity": "strictly decreasing for positive L",
        },
        "failures": failures[:10],
    }


def improved_layer_bound(field_name: str, degree: int) -> Rational:
    factor = 2 if field_name == "a" else 1
    return Rational(factor) * K_MAJORANT ** (degree - 1) / degree**3


def verify_improved_majorants(
    norms: dict[str, list[Rational | None]], maximum_degree: int
) -> dict[str, object]:
    failures: list[dict[str, object]] = []
    maximum_utilization = {
        "a": (Rational(0), 0),
        "U": (Rational(0), 0),
        "V": (Rational(0), 0),
    }
    for degree in range(1, maximum_degree + 1):
        for field_name, values in norms.items():
            value = values[degree]
            if value is None:
                raise AssertionError("missing layer norm")
            bound = improved_layer_bound(field_name, degree)
            utilization = value / bound
            if utilization > maximum_utilization[field_name][0]:
                maximum_utilization[field_name] = (utilization, degree)
            if value > bound:
                failures.append(
                    {
                        "field": field_name,
                        "totalDegree": degree,
                        "value": str(value),
                        "bound": str(bound),
                    }
                )
    return {
        "passed": not failures,
        "checkedThroughTotalDegree": maximum_degree,
        "majorantConstant": r030.rational_record(K_MAJORANT),
        "maximumUtilization": {
            field_name: {
                "degree": record[1],
                **r030.rational_record(record[0]),
            }
            for field_name, record in maximum_utilization.items()
        },
        "failures": failures[:10],
    }


def layer_records(
    norms: dict[str, list[Rational | None]], maximum_degree: int
) -> list[dict[str, object]]:
    selected = sorted(
        {
            degree
            for degree in (1, 2, 3, 6, 12, 24, 40, 60, 80, 100, maximum_degree)
            if degree <= maximum_degree
        }
    )
    records: list[dict[str, object]] = []
    for degree in selected:
        fields: dict[str, object] = {}
        for field_name, values in norms.items():
            value = values[degree]
            if value is None:
                raise AssertionError("missing layer norm")
            field_record: dict[str, object] = {
                "l1Norm": r030.rational_record(value),
                "nthRoot": r030.positive_root_decimal(value, degree),
                "improvedMajorantUtilization": r030.rational_record(
                    value / improved_layer_bound(field_name, degree)
                ),
            }
            if degree > 3:
                predecessor = values[degree - 3]
                if predecessor is None or predecessor <= 0:
                    raise AssertionError("missing positive three-step predecessor")
                field_record["threeStepBlockPerDegree"] = (
                    r030.positive_root_decimal(value / predecessor, 3)
                )
            fields[field_name] = field_record
        records.append({"totalDegree": degree, "fields": fields})
    return records


def build_payload(maximum_degree: int, show_progress: bool) -> dict[str, object]:
    started = time.perf_counter()
    progress(show_progress, started, "constructing exact kernel certificate")
    kernel = kernel_proof_certificate()
    progress(show_progress, started, "completed all-order kernel proof certificate")

    original_progress = r028.progress

    def recurrence_progress(_enabled: bool, _started: float, message: str) -> None:
        progress(show_progress, started, message)

    r028.progress = recurrence_progress
    try:
        a, u, v, interactions = r028.rational_edge_recurrence(
            maximum_degree, False, started
        )
    finally:
        r028.progress = original_progress
    progress(show_progress, started, f"completed recurrence; interactions {interactions}")

    normalized_u, normalized_v = r030.normalized_fields(u, v)
    norms = {
        "a": r030.layer_l1_norms(a),
        "U": r030.layer_l1_norms(normalized_u),
        "V": r030.layer_l1_norms(normalized_v),
    }
    checks = {
        "kernelProof": kernel,
        "aChargeSupport": r029.charge_support_check(a, maximum_degree),
        "improvedLayerMajorants": verify_improved_majorants(norms, maximum_degree),
        "transportDivisibility": r030.divisibility_check(
            normalized_u, normalized_v, maximum_degree
        ),
    }
    progress(show_progress, started, "completed improved majorant regressions")

    return {
        "scope": {
            "result": "improved all-order common analyticity domain with exact finite regressions",
            "maximumCheckedTotalDegree": maximum_degree,
            "limitations": [
                "the theorem concerns the reduced two-variable edge system, not the full three-dimensional Navier-Stokes equation",
                "the GMP recurrence is a finite implementation regression and is not the proof of the all-order kernel estimate",
                "the improved domain remains a lower bound and does not locate the nearest singular variety",
                "no endpoint coefficient asymptotic or Navier-Stokes regularity theorem is claimed",
            ],
        },
        "formalTheorem": {
            "kernelBound": "H_2=8 and H_L<=27/4 for every L>=3",
            "majorantConstant": "K=81/4",
            "coefficientBounds": {
                "a": "A_L <= 2*(81/4)^(L-1)/L^3",
                "U": "sum_k |U_(L,k)| <= (81/4)^(L-1)/L^3",
                "V": "sum_k |V_(L,k)| <= (81/4)^(L-1)/L^3",
            },
            "commonAnalyticDomain": "max(|Z|,|W|)<4/81",
            "logarithmArgument": "for Kr<1, each quotient tail is less than sum_(L>=2) 1/[L(L-1)]=1",
            "analyticIdentity": "the R0.29 canonical logarithms and exponential factorization are analytic on the same polydisc max(|Z|,|W|)<4/81",
        },
        "checks": checks,
        "finiteLayerDiagnostics": layer_records(norms, maximum_degree),
        "digests": {name: r030.norm_digest(values) for name, values in norms.items()},
        "computation": {
            "backend": r028.base.RATIONAL_BACKEND,
            "recurrenceOrderedInteractions": interactions,
            "wallSeconds": time.perf_counter() - started,
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "gmpy2": gmpy2.version(),
            "gmp": gmpy2.mp_version(),
        },
        "git": r028.git_source_state(),
    }


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-total-degree", type=int, default=60)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--progress-log",
        type=Path,
        help="append-only NDJSON progress record; must not already exist",
    )
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> None:
    global PROGRESS_LOG
    arguments = parse_arguments()
    if arguments.max_total_degree < 4:
        raise SystemExit("--max-total-degree must be at least 4")
    if arguments.progress_log is not None:
        if arguments.progress_log.exists():
            raise SystemExit("--progress-log already exists; choose a new run path")
        arguments.progress_log.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_LOG = arguments.progress_log
    payload = build_payload(arguments.max_total_degree, arguments.progress)
    if arguments.check:
        for check_name, check in payload["checks"].items():
            if not check["passed"]:
                raise AssertionError(f"R0.31 check failed: {check_name}")
    if arguments.output is not None:
        r028.atomic_json_write(arguments.output, payload, arguments.pretty)
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
