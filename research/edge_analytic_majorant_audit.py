#!/usr/bin/env python3
"""R0.30 exact audit for the all-order analytic majorant theorem.

For total-degree layers, define the coefficient l1 norms

    A_L = sum_k |a_(L,k)|,
    F_L = sum_k |f_(L,k)|.

Symmetrizing the active recurrence and using the exact charge support q >= -1
gives the all-order scalar inequalities

    A_L <= (3/2) sum_(i+j=L) min(i,j) A_i A_j,
    F_L <=       sum_(i+j=L) min(i,j) A_i F_j.

The elementary convolution constant

    H_L = L^3 sum_(i+j=L) min(i,j)/(i^3 j^3) < 32

then closes the induction with K=96:

    A_L <= 2 K^(L-1)/L^3,
    ||U_L||_1, ||V_L||_1 <= K^(L-1)/L^3,

where U=-12u and V=-3v.  The proof is all-order; this script reconstructs
the exact GMP arrays only as an independent finite regression.  It does not
locate a dominant singularity or imply a Navier--Stokes regularity theorem.
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
import edge_rational_asymptotic_audit as r028


Rational = gmpy2.mpq
Field = r028.RationalField
K_MAJORANT = 96
H_BOUND = 32
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, message: str) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        print(f"[R0.30 +{elapsed:8.2f}s] {message}", file=sys.stderr, flush=True)
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


def decimal(value: Rational, digits: int = 18) -> str:
    context = gmpy2.get_context()
    previous_precision = context.precision
    context.precision = 256
    try:
        return format(gmpy2.mpfr(value), f".{digits}g")
    finally:
        context.precision = previous_precision


def positive_root_decimal(value: Rational, order: int, digits: int = 18) -> str:
    if value <= 0 or order <= 0:
        raise ValueError("positive root requires a positive value and order")
    context = gmpy2.get_context()
    previous_precision = context.precision
    context.precision = 256
    try:
        root = gmpy2.exp(gmpy2.log(gmpy2.mpfr(value)) / order)
        return format(root, f".{digits}g")
    finally:
        context.precision = previous_precision


def rational_record(value: Rational) -> dict[str, object]:
    numerator = gmpy2.numer(value)
    denominator = gmpy2.denom(value)
    return {
        "exact": str(value),
        "decimal": decimal(value),
        "numeratorDigits": len(str(abs(numerator))),
        "denominatorDigits": len(str(denominator)),
        "sha256": hashlib.sha256(str(value).encode("ascii")).hexdigest(),
    }


def normalized_fields(u: Field, v: Field) -> tuple[Field, Field]:
    normalized_u: Field = [None] * len(u)
    normalized_v: Field = [None] * len(v)
    for degree in range(1, len(u)):
        u_layer = u[degree]
        v_layer = v[degree]
        if u_layer is None or v_layer is None:
            raise AssertionError("missing transport layer")
        normalized_u[degree] = [-12 * value for value in u_layer]
        normalized_v[degree] = [-3 * value for value in v_layer]
    return normalized_u, normalized_v


def layer_l1_norms(field: Field) -> list[Rational | None]:
    norms: list[Rational | None] = [None] * len(field)
    for degree in range(1, len(field)):
        layer = field[degree]
        if layer is None:
            raise AssertionError("missing field layer")
        norms[degree] = sum((abs(value) for value in layer), Rational(0))
    return norms


def norm_digest(norms: list[Rational | None]) -> str:
    digest = hashlib.sha256()
    for degree in range(1, len(norms)):
        value = norms[degree]
        if value is None:
            raise AssertionError("missing norm")
        digest.update(f"{degree}:{value}\n".encode("ascii"))
    return digest.hexdigest()


def convolution_constant(degree: int) -> Rational:
    total = Rational(0)
    for left_degree in range(1, degree):
        right_degree = degree - left_degree
        total += Rational(
            min(left_degree, right_degree),
            left_degree**3 * right_degree**3,
        )
    return degree**3 * total


def verify_majorants(
    a_norms: list[Rational | None],
    u_norms: list[Rational | None],
    v_norms: list[Rational | None],
    maximum_degree: int,
) -> dict[str, object]:
    failures: list[dict[str, object]] = []
    maximum_h = Rational(0)
    maximum_h_degree = 0
    maximum_utilization = {"a": (Rational(0), 0), "U": (Rational(0), 0), "V": (Rational(0), 0)}

    for degree in range(2, maximum_degree + 1):
        h_value = convolution_constant(degree)
        if h_value > maximum_h:
            maximum_h = h_value
            maximum_h_degree = degree
        if h_value >= H_BOUND:
            failures.append({"check": "H_L < 32", "degree": degree, "value": str(h_value)})

        bounds = {
            "a": Rational(2 * K_MAJORANT ** (degree - 1), degree**3),
            "U": Rational(K_MAJORANT ** (degree - 1), degree**3),
            "V": Rational(K_MAJORANT ** (degree - 1), degree**3),
        }
        values = {"a": a_norms[degree], "U": u_norms[degree], "V": v_norms[degree]}
        for field_name, value in values.items():
            if value is None:
                raise AssertionError("missing layer norm")
            utilization = value / bounds[field_name]
            if utilization > maximum_utilization[field_name][0]:
                maximum_utilization[field_name] = (utilization, degree)
            if value > bounds[field_name]:
                failures.append(
                    {
                        "check": f"{field_name} layer majorant",
                        "degree": degree,
                        "value": str(value),
                        "bound": str(bounds[field_name]),
                    }
                )

    return {
        "passed": not failures,
        "checkedThroughTotalDegree": maximum_degree,
        "finiteMaximumH": {"degree": maximum_h_degree, **rational_record(maximum_h)},
        "maximumFiniteMajorantUtilizationExcludingDegreeOne": {
            name: {"degree": item[1], **rational_record(item[0])}
            for name, item in maximum_utilization.items()
        },
        "failures": failures[:10],
    }


def divisibility_check(u: Field, v: Field, maximum_degree: int) -> dict[str, object]:
    failures: list[dict[str, object]] = []
    for degree in range(1, maximum_degree + 1):
        u_layer = u[degree]
        v_layer = v[degree]
        if u_layer is None or v_layer is None:
            raise AssertionError("missing transport layer")
        if u_layer[degree] != 0:
            failures.append(
                {
                    "field": "U",
                    "degree": degree,
                    "forbiddenPureWCoefficient": str(u_layer[degree]),
                }
            )
        if v_layer[0] != 0:
            failures.append(
                {
                    "field": "V",
                    "degree": degree,
                    "forbiddenPureZCoefficient": str(v_layer[0]),
                }
            )
    return {
        "passed": not failures,
        "checkedThroughTotalDegree": maximum_degree,
        "statement": "U is divisible by Z and V is divisible by W",
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
        record: dict[str, object] = {"totalDegree": degree, "fields": {}}
        for name, values in norms.items():
            value = values[degree]
            if value is None:
                raise AssertionError("missing layer norm")
            bound = Rational(
                (2 if name == "a" else 1) * K_MAJORANT ** (degree - 1),
                degree**3,
            )
            field_record: dict[str, object] = {
                "l1Norm": rational_record(value),
                "nthRoot": positive_root_decimal(value, degree),
                "majorantUtilization": rational_record(value / bound),
            }
            if degree > 3:
                previous = values[degree - 3]
                if previous is None or previous <= 0:
                    raise AssertionError("missing positive three-step predecessor")
                field_record["threeStepBlockPerDegree"] = positive_root_decimal(
                    value / previous, 3
                )
            record["fields"][name] = field_record
        records.append(record)
    return records


def build_payload(maximum_degree: int, show_progress: bool) -> dict[str, object]:
    started = time.perf_counter()
    progress(show_progress, started, f"starting GMP recurrence through degree {maximum_degree}")

    original_progress = r028.progress

    def recurrence_progress(_enabled: bool, _started: float, message: str) -> None:
        progress(show_progress, started, message)

    r028.progress = recurrence_progress
    try:
        a, u, v, recurrence_interactions = r028.rational_edge_recurrence(
            maximum_degree, False, started
        )
    finally:
        r028.progress = original_progress
    progress(
        show_progress,
        started,
        f"completed recurrence; interactions {recurrence_interactions}",
    )

    normalized_u, normalized_v = normalized_fields(u, v)
    norms = {
        "a": layer_l1_norms(a),
        "U": layer_l1_norms(normalized_u),
        "V": layer_l1_norms(normalized_v),
    }
    support = r029.charge_support_check(a, maximum_degree)
    majorants = verify_majorants(
        norms["a"], norms["U"], norms["V"], maximum_degree
    )
    divisibility = divisibility_check(normalized_u, normalized_v, maximum_degree)
    progress(show_progress, started, "completed exact layer-norm and divisibility checks")

    return {
        "scope": {
            "result": "all-order common analyticity domain with an exact finite layer-norm regression",
            "maximumCheckedTotalDegree": maximum_degree,
            "limitations": [
                "the analyticity theorem concerns the reduced edge formal system, not the full three-dimensional Navier-Stokes equation",
                "the degree-limited GMP computation is a regression and finite growth diagnostic, not the proof of the all-order majorant",
                "the conservative radius does not locate the nearest or dominant complex singularity",
                "no endpoint coefficient asymptotic or Navier-Stokes regularity theorem is claimed",
            ],
        },
        "formalTheorem": {
            "layerNorms": {
                "A_L": "sum_k |a_(L,k)|",
                "F_L": "sum_k |f_(L,k)|",
            },
            "symmetrizedRecurrences": {
                "active": "A_L <= (3/2) sum_(i+j=L) min(i,j) A_i A_j",
                "transport": "F_L <= sum_(i+j=L) min(i,j) A_i F_j",
            },
            "kernelLemma": {
                "definition": "H_L=L^3 sum_(i+j=L) min(i,j)/(i^3 j^3)",
                "bound": "H_L<32",
                "proofBound": "H_L<=16 sum_(i>=1) i^-2<32",
            },
            "majorantConstant": K_MAJORANT,
            "coefficientBounds": {
                "a": "A_L <= 2*96^(L-1)/L^3",
                "U": "sum_k |U_(L,k)| <= 96^(L-1)/L^3",
                "V": "sum_k |V_(L,k)| <= 96^(L-1)/L^3",
            },
            "analyticDomains": {
                "aUV": "max(|Z|,|W|)<1/96",
                "logarithmsAndPhi": "max(|Z|,|W|)<1/192",
                "quotientTailBound": "|U/Z-1|, |V/W-1| <= 1/8 on the closed polydisc of radius 1/192",
            },
            "analyticIdentity": "phi=(1/2) log(UV/(ZW)) and the R0.29 exponential factorization hold analytically on max(|Z|,|W|)<1/192",
        },
        "checks": {
            "aChargeSupport": support,
            "layerMajorants": majorants,
            "transportDivisibility": divisibility,
        },
        "finiteLayerDiagnostics": layer_records(norms, maximum_degree),
        "digests": {name: norm_digest(values) for name, values in norms.items()},
        "computation": {
            "backend": r028.base.RATIONAL_BACKEND,
            "recurrenceOrderedInteractions": recurrence_interactions,
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
        if not payload["checks"]["aChargeSupport"]["passed"]:
            raise AssertionError("active charge-support regression failed")
        if not payload["checks"]["layerMajorants"]["passed"]:
            raise AssertionError("analytic majorant regression failed")
        if not payload["checks"]["transportDivisibility"]["passed"]:
            raise AssertionError("transport divisibility regression failed")
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
