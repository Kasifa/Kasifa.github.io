#!/usr/bin/env python3
"""R0.50 exploratory two-parameter charge-character optimization.

This script is deliberately classified as exploration.  It reconstructs the
exact degree-80 center used by R0.49, derives the positive Laurent polynomial

    A(r,c) = sum_(i,q) b_(i,q) r^i c^q

for the true input column (j,s)=(81,162), and numerically solves

    A(r,c)=1,             d A(r,e^t)/dt = 0.

The solve locates the candidate that maximizes the active-column threshold in
the multiplicative-character family.  It is not an interval certificate and
does not prove that the same column dominates every competing sector near the
candidate.  Those are separate R0.50 obligations.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import time

import gmpy2
import mpmath

import edge_charge_resolved_audit as r039
import edge_charge_threshold_root_audit as r048
import edge_rational_asymptotic_audit as r028
import edge_short_continuation_audit as r036


Rational = gmpy2.mpq


def progress(started: float, stage: str, **details: object) -> None:
    payload = "" if not details else " " + json.dumps(details, sort_keys=True)
    print(
        f"[R0.50 explore +{time.perf_counter() - started:8.2f}s] {stage}{payload}",
        file=sys.stderr,
        flush=True,
    )


def to_mpf(value: Rational) -> mpmath.mpf:
    return mpmath.mpf(int(value.numerator)) / mpmath.mpf(
        int(value.denominator)
    )


def active_laurent_terms(
    terms: list[tuple[int, int, Rational]],
    input_degree: int,
    input_charge: int,
) -> list[tuple[int, int, Rational]]:
    result = []
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
        )
        weighted = coefficient * factor
        if weighted:
            result.append((degree, charge, weighted))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-total-degree", type=int, default=80)
    parser.add_argument("--digits", type=int, default=100)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    if arguments.max_total_degree != 80:
        raise SystemExit("the R0.50 exploration is pinned to degree 80")
    if arguments.digits < 60:
        raise SystemExit("--digits must be at least 60")

    started = time.perf_counter()
    progress(started, "constructing exact degree-80 center")
    active_field, _, _, recurrence_interactions = (
        r028.rational_edge_recurrence(
            arguments.max_total_degree,
            True,
            started,
        )
    )
    polynomial = r036.field_to_polynomial(
        active_field,
        arguments.max_total_degree,
    )
    independent = r048.independent_terms(polynomial)
    laurent = active_laurent_terms(independent, 81, 162)
    progress(
        started,
        "formed exact active Laurent polynomial",
        terms=len(laurent),
        minimumCharge=min(charge for _, charge, _ in laurent),
        maximumCharge=max(charge for _, charge, _ in laurent),
    )

    mpmath.mp.dps = arguments.digits
    numeric_terms = [
        (degree, charge, to_mpf(coefficient))
        for degree, charge, coefficient in laurent
    ]

    def moment(r: mpmath.mpf, c: mpmath.mpf, degree_power: int, charge_power: int) -> mpmath.mpf:
        return mpmath.fsum(
            coefficient
            * degree**degree_power
            * charge**charge_power
            * r**degree
            * c**charge
            for degree, charge, coefficient in numeric_terms
        )

    def equations(r: mpmath.mpf, c: mpmath.mpf) -> tuple[mpmath.mpf, mpmath.mpf]:
        return moment(r, c, 0, 0) - 1, moment(r, c, 0, 1)

    progress(started, "solving A=1 and log-c derivative=0")
    candidate_r, candidate_c = mpmath.findroot(
        equations,
        (mpmath.mpf("0.383"), mpmath.mpf("0.8")),
        solver="mdnewton",
        tol=mpmath.mpf(10) ** (-(arguments.digits - 20)),
        verify=True,
    )
    value = moment(candidate_r, candidate_c, 0, 0)
    log_c_derivative = moment(candidate_r, candidate_c, 0, 1)
    log_c_second = moment(candidate_r, candidate_c, 0, 2)
    log_r_derivative = moment(candidate_r, candidate_c, 1, 0)
    mixed_log_derivative = moment(candidate_r, candidate_c, 1, 1)

    def root_for_character(character: str) -> mpmath.mpf:
        c = mpmath.mpf(character)
        return mpmath.findroot(
            lambda radius: moment(radius, c, 0, 0) - 1,
            candidate_r,
        )

    root_four_fifths = root_for_character("0.8")
    threshold_gain = candidate_r / root_four_fifths
    fixed_charge_gain = threshold_gain**3
    second_derivative_of_root_in_log_c = -log_c_second / (
        log_r_derivative / candidate_r
    )

    negative_charge_terms = sum(1 for _, q, _ in laurent if q < 0)
    zero_charge_terms = sum(1 for _, q, _ in laurent if q == 0)
    positive_charge_terms = sum(1 for _, q, _ in laurent if q > 0)
    payload = {
        "schemaVersion": "0.1-exploratory",
        "classification": (
            "high-precision candidate localization; not an interval proof "
            "and not a competitor-dominance certificate"
        ),
        "createdAtUtc": datetime.now(timezone.utc).isoformat(),
        "finiteConstruction": {
            "maximumTotalDegree": arguments.max_total_degree,
            "centerTerms": len(polynomial),
            "activeLaurentTerms": len(laurent),
            "recurrenceOrderedInteractions": recurrence_interactions,
            "chargeRange": [
                min(charge for _, charge, _ in laurent),
                max(charge for _, charge, _ in laurent),
            ],
            "negativeChargeTerms": negative_charge_terms,
            "zeroChargeTerms": zero_charge_terms,
            "positiveChargeTerms": positive_charge_terms,
            "allCoefficientsPositive": all(
                coefficient > 0 for _, _, coefficient in laurent
            ),
        },
        "candidate": {
            "r": mpmath.nstr(candidate_r, arguments.digits),
            "c": mpmath.nstr(candidate_c, arguments.digits),
            "A": mpmath.nstr(value, arguments.digits),
            "logCFirstDerivative": mpmath.nstr(
                log_c_derivative,
                arguments.digits,
            ),
            "logCSecondDerivative": mpmath.nstr(
                log_c_second,
                arguments.digits,
            ),
            "logRFirstDerivative": mpmath.nstr(
                log_r_derivative,
                arguments.digits,
            ),
            "mixedLogDerivative": mpmath.nstr(
                mixed_log_derivative,
                arguments.digits,
            ),
            "rootSecondDerivativeWithRespectToLogC": mpmath.nstr(
                second_derivative_of_root_in_log_c,
                arguments.digits,
            ),
        },
        "comparisonWithR049": {
            "rootAtFourFifths": mpmath.nstr(
                root_four_fifths,
                arguments.digits,
            ),
            "optimalToFourFifthsThresholdFactor": mpmath.nstr(
                threshold_gain,
                arguments.digits,
            ),
            "optimalToFourFifthsFixedChargeRadiusFactor": mpmath.nstr(
                fixed_charge_gain,
                arguments.digits,
            ),
        },
        "formalStructureToCertify": {
            "AIsStrictlyIncreasingInR": True,
            "AIsStrictlyConvexInLogC": True,
            "AIsCoerciveInLogC": negative_charge_terms > 0
            and positive_charge_terms > 0,
            "remainingObligations": [
                "isolate the simultaneous root in an exact rational box",
                "certify all 243 competitor inequalities on a rational box",
                "certify the all-order large-charge branches uniformly in c",
                "separate finite degree-80 construction from all-order claims",
            ],
        },
        "wallTimeSeconds": time.perf_counter() - started,
    }
    progress(
        started,
        "candidate localized",
        r=mpmath.nstr(candidate_r, 30),
        c=mpmath.nstr(candidate_c, 30),
    )
    rendered = json.dumps(payload, indent=2, sort_keys=True)
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
