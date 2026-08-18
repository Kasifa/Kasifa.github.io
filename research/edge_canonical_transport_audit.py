#!/usr/bin/env python3
"""R0.29 exact audit of the canonical transport reduction.

The R0.28 rational arrays satisfy

    (L - 1) u = {a, u},    (L - 1) v = {a, v},

with u_1=-Z/12 and v_1=-W/3.  If U=-12u and V=-3v, formal uniqueness and
the Jacobi identity give the all-order identities

    {U,V} = U V,
    U / V = (Z/W) exp(-a).

Consequently the sharp series factors as

    d = p u + q v = v (q + p Z exp(-a)/(4W)).

The theorem is algebraic and does not depend on a finite computation.  This
script independently reconstructs exp(-a) over exact GMP rationals and checks
both coefficient identities through a requested total degree.  It also records
the exact upward charge coupling k f_(k,q+1) that prevents any fixed finite set
of charge sectors from closing under the transport recurrence.
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


Rational = gmpy2.mpq
Layer = list[Rational]
Field = list[Layer | None]
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, message: str) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        print(f"[R0.29 +{elapsed:8.2f}s] {message}", file=sys.stderr, flush=True)
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


def exp_negative_a(
    a: Field,
    maximum_degree: int,
    show_progress: bool,
    started: float,
) -> list[Layer]:
    """Return exp(-a) from L E = -(L a) E over exact rationals."""

    zero = Rational(0)
    exponential = [[Rational(1)]] + [
        [zero] * (degree + 1) for degree in range(1, maximum_degree + 1)
    ]
    for degree in range(1, maximum_degree + 1):
        numerator = [zero] * (degree + 1)
        for a_degree in range(1, degree + 1):
            e_degree = degree - a_degree
            a_layer = a[a_degree]
            if a_layer is None:
                raise AssertionError("missing a layer")
            for a_k, a_value in enumerate(a_layer):
                if a_value == 0:
                    continue
                for e_k, e_value in enumerate(exponential[e_degree]):
                    if e_value != 0:
                        numerator[a_k + e_k] -= (
                            a_degree * a_value * e_value
                        )
        exponential[degree] = [value / degree for value in numerator]
        if degree % 20 == 0 or degree == maximum_degree:
            progress(
                show_progress,
                started,
                f"constructed exp(-a) through total degree {degree}",
            )
    return exponential


def field_digest(field: Field | list[Layer]) -> str:
    digest = hashlib.sha256()
    for degree, layer in enumerate(field):
        if layer is None:
            continue
        for catalyst_count, value in enumerate(layer):
            digest.update(
                f"{degree},{catalyst_count}:{value}\n".encode("ascii")
            )
    return digest.hexdigest()


def maximum_fraction_digits(field: Field | list[Layer]) -> dict[str, int]:
    maximum_numerator = 1
    maximum_denominator = 1
    for layer in field:
        if layer is None:
            continue
        for value in layer:
            if value == 0:
                continue
            maximum_numerator = max(
                maximum_numerator,
                len(str(abs(gmpy2.numer(value)))),
            )
            maximum_denominator = max(
                maximum_denominator,
                len(str(gmpy2.denom(value))),
            )
    return {
        "maximumNumeratorDigits": maximum_numerator,
        "maximumDenominatorDigits": maximum_denominator,
    }


def validate_canonical_identities(
    u: Field,
    v: Field,
    exponential: list[Layer],
    maximum_degree: int,
    show_progress: bool,
    started: float,
) -> dict[str, object]:
    """Check {u,v}=uv and 4Wu=Zv exp(-a) coefficient by coefficient."""

    zero = Rational(0)
    coefficient_checks = 0
    convolution_interactions = 0
    first_failure: dict[str, object] | None = None

    for total_degree in range(2, maximum_degree + 1):
        product_uv = [zero] * (total_degree + 1)
        bracket_uv = [zero] * (total_degree + 1)
        for left_degree in range(1, total_degree):
            right_degree = total_degree - left_degree
            left_layer = u[left_degree]
            right_layer = v[right_degree]
            if left_layer is None or right_layer is None:
                raise AssertionError("missing transport layer")
            for left_k, left_value in enumerate(left_layer):
                if left_value == 0:
                    continue
                for right_k, right_value in enumerate(right_layer):
                    if right_value == 0:
                        continue
                    output_k = left_k + right_k
                    product = left_value * right_value
                    determinant = (
                        left_degree * right_k - left_k * right_degree
                    )
                    product_uv[output_k] += product
                    bracket_uv[output_k] += determinant * product
                    convolution_interactions += 1

        ve_degree = total_degree - 1
        product_ve = [zero] * (ve_degree + 1)
        for v_degree in range(1, ve_degree + 1):
            e_degree = ve_degree - v_degree
            v_layer = v[v_degree]
            if v_layer is None:
                raise AssertionError("missing v layer")
            for v_k, v_value in enumerate(v_layer):
                if v_value == 0:
                    continue
                for e_k, e_value in enumerate(exponential[e_degree]):
                    if e_value == 0:
                        continue
                    product_ve[v_k + e_k] += v_value * e_value
                    convolution_interactions += 1

        previous_u_layer = u[total_degree - 1]
        if previous_u_layer is None:
            raise AssertionError("missing u layer")
        for catalyst_count in range(total_degree + 1):
            coefficient_checks += 2
            if bracket_uv[catalyst_count] != product_uv[catalyst_count]:
                first_failure = {
                    "identity": "{u,v}=uv",
                    "totalDegree": total_degree,
                    "catalystCount": catalyst_count,
                    "left": str(bracket_uv[catalyst_count]),
                    "right": str(product_uv[catalyst_count]),
                }
                break
            left = (
                4 * previous_u_layer[catalyst_count - 1]
                if 0 <= catalyst_count - 1 < len(previous_u_layer)
                else zero
            )
            right = (
                product_ve[catalyst_count]
                if catalyst_count < len(product_ve)
                else zero
            )
            if left != right:
                first_failure = {
                    "identity": "4Wu=Zv exp(-a)",
                    "totalDegree": total_degree,
                    "catalystCount": catalyst_count,
                    "left": str(left),
                    "right": str(right),
                }
                break
        if first_failure is not None:
            break
        if total_degree % 20 == 0 or total_degree == maximum_degree:
            progress(
                show_progress,
                started,
                f"validated canonical identities through degree {total_degree}",
            )

    return {
        "passed": first_failure is None,
        "maximumTotalDegree": maximum_degree,
        "coefficientChecks": coefficient_checks,
        "exactConvolutionInteractions": convolution_interactions,
        "firstFailure": first_failure,
    }


def charge_support_check(a: Field, maximum_degree: int) -> dict[str, object]:
    violations: list[dict[str, object]] = []
    nonzero_coefficients = 0
    for degree in range(1, maximum_degree + 1):
        layer = a[degree]
        if layer is None:
            raise AssertionError("missing a layer")
        for catalyst_count, value in enumerate(layer):
            if value == 0:
                continue
            nonzero_coefficients += 1
            charge = 3 * catalyst_count - degree
            if charge < -1:
                violations.append(
                    {
                        "totalDegree": degree,
                        "catalystCount": catalyst_count,
                        "charge": charge,
                        "value": str(value),
                    }
                )
    return {
        "passed": not violations,
        "nonzeroCoefficients": nonzero_coefficients,
        "minimumAllowedCharge": -1,
        "violations": violations[:10],
    }


def build_payload(maximum_degree: int, show_progress: bool) -> dict[str, object]:
    started = time.perf_counter()
    progress(
        show_progress,
        started,
        f"starting exact rational recurrence through degree {maximum_degree}",
    )
    a, u, v, recurrence_interactions = r028.rational_edge_recurrence(
        maximum_degree,
        False,
        started,
    )
    progress(
        show_progress,
        started,
        f"completed rational recurrence; interactions {recurrence_interactions}",
    )
    exponential = exp_negative_a(a, maximum_degree, show_progress, started)
    identities = validate_canonical_identities(
        u,
        v,
        exponential,
        maximum_degree,
        show_progress,
        started,
    )
    support = charge_support_check(a, maximum_degree)
    progress(show_progress, started, "completed exact canonical audit")

    return {
        "scope": {
            "result": (
                "all-order log-canonical transport reduction with an exact "
                "finite coefficient regression"
            ),
            "maximumCheckedTotalDegree": maximum_degree,
            "limitations": [
                "the coefficient regression is finite, although the formal identities are all-order",
                "the identities do not prove endpoint coefficient signs",
                "no dominant-singularity or Navier-Stokes regularity theorem is claimed",
            ],
        },
        "formalTheorem": {
            "definitions": {
                "U": "-12u",
                "V": "-3v",
                "bracket": "{f,g}=(Z d_Z f)(W d_W g)-(W d_W f)(Z d_Z g)",
            },
            "identities": {
                "logCanonical": "{U,V}=UV",
                "ratio": "U/V=(Z/W) exp(-a)",
                "polynomial": "4 W u=Z v exp(-a)",
                "sharpFactorization": "d=v(q+p Z exp(-a)/(4W))",
                "transportHierarchy": (
                    "(L-m-n)(U^m V^n)={a,U^m V^n}"
                ),
            },
            "finiteChargeClosureObstruction": {
                "chargeCoordinates": "R=Z^2W, Xi=Z^-1, L=3k-q",
                "aSupport": "a_(k,q)=0 for q<-1 and a_(0,-1)=1",
                "transportRecurrence": (
                    "(3k-q-1)f_(k,q)=k f_(k,q+1)+lower-degree convolution terms"
                ),
                "consequence": (
                    "no fixed finite upper set of charge sectors is closed; "
                    "an invariant cone must control an infinite weighted charge ladder"
                ),
            },
        },
        "checks": {
            "canonicalIdentities": identities,
            "aChargeSupport": support,
        },
        "digests": {
            "a": field_digest(a),
            "u": field_digest(u),
            "v": field_digest(v),
            "expNegativeA": field_digest(exponential),
        },
        "fractionSizes": {
            "a": maximum_fraction_digits(a),
            "u": maximum_fraction_digits(u),
            "v": maximum_fraction_digits(v),
            "expNegativeA": maximum_fraction_digits(exponential),
        },
        "computation": {
            "backend": r028.base.RATIONAL_BACKEND,
            "recurrenceOrderedInteractions": recurrence_interactions,
            "identityConvolutionInteractions": identities[
                "exactConvolutionInteractions"
            ],
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
    if arguments.max_total_degree < 3:
        raise SystemExit("--max-total-degree must be at least 3")
    if arguments.progress_log is not None:
        if arguments.progress_log.exists():
            raise SystemExit("--progress-log already exists; choose a new run path")
        arguments.progress_log.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_LOG = arguments.progress_log
    payload = build_payload(arguments.max_total_degree, arguments.progress)
    if arguments.check:
        if not payload["checks"]["canonicalIdentities"]["passed"]:
            raise AssertionError("canonical identity regression failed")
        if not payload["checks"]["aChargeSupport"]["passed"]:
            raise AssertionError("negative-charge support regression failed")
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
