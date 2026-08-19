#!/usr/bin/env python3
"""R0.32 certified finite diagnostic for fixed-charge singularity candidates.

The exact edge recurrence is extended through a user-selected total degree.
For the charge-one series U_1(R) and V_1(R), the script constructs diagonal
D-log Pade approximants from several exact truncations.  Their rational
denominators are treated as exact polynomials: real candidate roots are
isolated with Sturm methods, numerator noncancellation and residue signs are
certified by rational interval arithmetic, and 160/256-bit evaluations are
recorded as independent numerical regressions.

This certifies poles of finite rational approximants and the stability of a
defined candidate cluster.  It does not prove that the original fixed-charge
series has a singularity at the cluster, that the candidate is dominant, or
that three-dimensional Navier--Stokes solutions are singular or regular.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import gzip
import hashlib
import json
import os
from pathlib import Path
import pickle
import platform
import sys
import tempfile
import time

import gmpy2
import mpmath as mp
import sympy as sp

import edge_rational_asymptotic_audit as r028


sys.set_int_max_str_digits(0)


Rational = gmpy2.mpq
RationalLayer = list[Rational]
RationalField = list[RationalLayer | None]
CHECKPOINT_SCHEMA = "r032-edge-recurrence-v1"
R028_CERTIFICATE = Path("research/certificates/r028/edge-rational-asymptotic.json")
K_MAJORANT = Rational(81, 4)
TRANSPORT_WINDOW = (sp.Rational(-3, 4), sp.Rational(-7493, 10000))
D_ZERO_WINDOW = (sp.Rational(-29, 40), sp.Rational(-361, 500))
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(
            f"[R0.32 +{elapsed:8.2f}s] {stage}{suffix}",
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


def field_digest(field: RationalField, completed_degree: int) -> str:
    digest = hashlib.sha256()
    for degree in range(1, completed_degree + 1):
        layer = field[degree]
        if layer is None:
            raise AssertionError(f"missing layer {degree}")
        digest.update(f"L={degree}:".encode("ascii"))
        for value in layer:
            digest.update(str(value).encode("ascii"))
            digest.update(b",")
    return digest.hexdigest()


def atomic_checkpoint_write(
    path: Path,
    completed_degree: int,
    interactions: int,
    a: RationalField,
    u: RationalField,
    v: RationalField,
) -> dict[str, object]:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + f".tmp-{os.getpid()}")
    payload = {
        "schema": CHECKPOINT_SCHEMA,
        "completedDegree": completed_degree,
        "interactions": interactions,
        "a": a[: completed_degree + 1],
        "u": u[: completed_degree + 1],
        "v": v[: completed_degree + 1],
    }
    with temporary.open("wb") as raw_target:
        with gzip.GzipFile(
            filename="",
            mode="wb",
            compresslevel=6,
            fileobj=raw_target,
            mtime=0,
        ) as target:
            pickle.dump(payload, target, protocol=pickle.HIGHEST_PROTOCOL)
    os.replace(temporary, path)
    return {
        "completedDegree": completed_degree,
        "bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def load_checkpoint(
    path: Path, maximum_degree: int
) -> tuple[int, int, RationalField, RationalField, RationalField]:
    with gzip.open(path, "rb") as source:
        payload = pickle.load(source)
    if not isinstance(payload, dict) or payload.get("schema") != CHECKPOINT_SCHEMA:
        raise ValueError("checkpoint schema mismatch")
    completed_degree = int(payload["completedDegree"])
    if completed_degree < 1 or completed_degree > maximum_degree:
        raise ValueError("checkpoint degree is outside the requested range")
    fields: list[RationalField] = []
    for name in ("a", "u", "v"):
        field = payload[name]
        if not isinstance(field, list) or len(field) != completed_degree + 1:
            raise ValueError(f"invalid checkpoint field {name}")
        field.extend([None] * (maximum_degree - completed_degree))
        fields.append(field)
    return completed_degree, int(payload["interactions"]), *fields


def resumable_rational_edge_recurrence(
    maximum_degree: int,
    show_progress: bool,
    started: float,
    checkpoint_path: Path | None = None,
    resume: bool = False,
    checkpoint_interval: int = 10,
) -> tuple[RationalField, RationalField, RationalField, int, dict[str, object]]:
    """Return exact a,u,v fields with optional atomic checkpoint/restart."""

    if maximum_degree < 1:
        raise ValueError("maximum degree must be positive")
    if checkpoint_interval < 1:
        raise ValueError("checkpoint interval must be positive")
    zero = Rational(0)
    one = Rational(1)
    checkpoint_records: list[dict[str, object]] = []

    if resume:
        if checkpoint_path is None or not checkpoint_path.exists():
            raise FileNotFoundError("--resume requires an existing checkpoint")
        completed, interactions, a, u, v = load_checkpoint(
            checkpoint_path, maximum_degree
        )
        progress(
            show_progress,
            started,
            "resumed exact recurrence",
            completedDegree=completed,
            cumulativeInteractions=interactions,
        )
    else:
        a = [None] * (maximum_degree + 1)
        u = [None] * (maximum_degree + 1)
        v = [None] * (maximum_degree + 1)
        a[1] = [one, one]
        u[1] = [Rational(-1, 12), zero]
        v[1] = [zero, Rational(-1, 3)]
        completed = 1
        interactions = 0

    for leaf_count in range(completed + 1, maximum_degree + 1):
        charged_a_numerator = [zero] * (leaf_count + 1)
        zero_a_numerator = [zero] * (leaf_count + 1)
        u_numerator = [zero] * (leaf_count + 1)
        v_numerator = [zero] * (leaf_count + 1)
        layer_interactions = 0

        for left_leaf_count in range(1, leaf_count):
            right_leaf_count = leaf_count - left_leaf_count
            left_a_layer = a[left_leaf_count]
            right_a_layer = a[right_leaf_count]
            right_u_layer = u[right_leaf_count]
            right_v_layer = v[right_leaf_count]
            if any(
                layer is None
                for layer in (
                    left_a_layer,
                    right_a_layer,
                    right_u_layer,
                    right_v_layer,
                )
            ):
                raise AssertionError("missing recurrence layer")

            for left_k, left_a in enumerate(left_a_layer):  # type: ignore[arg-type]
                if left_a == 0:
                    continue
                for right_k, right_a in enumerate(right_a_layer):  # type: ignore[arg-type]
                    right_u = right_u_layer[right_k]  # type: ignore[index]
                    right_v = right_v_layer[right_k]  # type: ignore[index]
                    if right_a == 0 and right_u == 0 and right_v == 0:
                        continue
                    determinant = (
                        left_leaf_count * right_k
                        - left_k * right_leaf_count
                    )
                    if determinant == 0:
                        continue
                    output_k = left_k + right_k
                    u_numerator[output_k] += determinant * left_a * right_u
                    v_numerator[output_k] += determinant * left_a * right_v
                    if 3 * output_k == leaf_count:
                        zero_a_numerator[output_k] += (
                            determinant
                            * right_leaf_count
                            * left_a
                            * right_a
                        )
                    else:
                        right_charge = 3 * right_k - right_leaf_count
                        charged_a_numerator[output_k] += (
                            determinant * right_charge * left_a * right_a
                        )
                    layer_interactions += 1

        next_a = [zero] * (leaf_count + 1)
        next_u = [value / (leaf_count - 1) for value in u_numerator]
        next_v = [value / (leaf_count - 1) for value in v_numerator]
        for catalyst_count in range(1, leaf_count):
            charge = 3 * catalyst_count - leaf_count
            numerator = (
                zero_a_numerator[catalyst_count]
                if charge == 0
                else charged_a_numerator[catalyst_count]
            )
            denominator = (
                leaf_count * (leaf_count - 1)
                if charge == 0
                else charge * (leaf_count - 1)
            )
            next_a[catalyst_count] = numerator / denominator

        a[leaf_count] = next_a
        u[leaf_count] = next_u
        v[leaf_count] = next_v
        interactions += layer_interactions

        should_log = leaf_count % 10 == 0 or leaf_count == maximum_degree
        if should_log:
            progress(
                show_progress,
                started,
                "exact recurrence layer",
                totalDegree=leaf_count,
                layerInteractions=layer_interactions,
                cumulativeInteractions=interactions,
            )
        if checkpoint_path is not None and (
            leaf_count % checkpoint_interval == 0
            or leaf_count == maximum_degree
        ):
            record = atomic_checkpoint_write(
                checkpoint_path, leaf_count, interactions, a, u, v
            )
            checkpoint_records.append(record)
            progress(
                show_progress,
                started,
                "checkpoint written",
                **record,
            )

    checkpoint_summary: dict[str, object] = {
        "enabled": checkpoint_path is not None,
        "resumeRequested": resume,
        "intervalDegrees": checkpoint_interval,
        "writes": checkpoint_records,
    }
    if checkpoint_path is not None and checkpoint_path.exists():
        checkpoint_summary["final"] = {
            "completedDegree": maximum_degree,
            "bytes": checkpoint_path.stat().st_size,
            "sha256": hashlib.sha256(checkpoint_path.read_bytes()).hexdigest(),
        }
    return a, u, v, interactions, checkpoint_summary


def checkpoint_resume_regression() -> dict[str, object]:
    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="r032-checkpoint-") as directory:
        checkpoint = Path(directory) / "state.pkl.gz"
        resumable_rational_edge_recurrence(
            12, False, started, checkpoint, False, 6
        )
        resumed = resumable_rational_edge_recurrence(
            18, False, started, checkpoint, True, 6
        )
        direct_a, direct_u, direct_v, direct_interactions = (
            r028.rational_edge_recurrence(18, False, started)
        )
        passed = (
            resumed[3] == direct_interactions
            and resumed[0] == direct_a
            and resumed[1] == direct_u
            and resumed[2] == direct_v
        )
    return {
        "passed": passed,
        "splitDegrees": [12, 18],
        "directInteractions": direct_interactions,
        "resumedInteractions": resumed[3],
    }


def endpoint_records(
    a: RationalField,
    u: RationalField,
    v: RationalField,
    maximum_degree: int,
    p_center: Rational,
    q_center: Rational,
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for parameter in range(1, (maximum_degree + 1) // 3 + 1):
        degree = 3 * parameter - 1
        if degree > maximum_degree:
            break
        a_value = a[degree][parameter]  # type: ignore[index]
        u_value = u[degree][parameter]  # type: ignore[index]
        v_value = v[degree][parameter]  # type: ignore[index]
        d_value = p_center * u_value + q_center * v_value
        records.append(
            {
                "parameter": parameter,
                "totalDegree": degree,
                "charge": 1,
                "a": str(a_value),
                "u": str(u_value),
                "v": str(v_value),
                "dCenter": str(d_value),
            }
        )
    return records


def r028_endpoint_regression(records: list[dict[str, object]]) -> dict[str, object]:
    old = json.loads(R028_CERTIFICATE.read_text(encoding="utf-8"))["endpoints"]
    failures: list[dict[str, object]] = []
    for expected, actual in zip(old, records):
        for field in ("a", "u", "v"):
            if expected[field]["fraction"] != actual[field]:
                failures.append(
                    {
                        "parameter": actual["parameter"],
                        "field": field,
                    }
                )
    return {
        "passed": not failures,
        "completeHistoricalCoverage": len(records) >= len(old),
        "checkedParameters": min(len(records), len(old)),
        "failures": failures[:10],
    }


def fraction_series(
    records: list[dict[str, object]], field: str
) -> list[Fraction]:
    return [Fraction(str(record[field])) for record in records]


def dlog_coefficients(coefficients: list[Fraction]) -> list[Fraction]:
    if not coefficients or coefficients[0] == 0:
        raise ValueError("D-log normalization requires a nonzero constant term")
    result: list[Fraction] = []
    for degree in range(len(coefficients) - 1):
        right = (degree + 1) * coefficients[degree + 1]
        for index in range(1, degree + 1):
            right -= coefficients[index] * result[degree - index]
        result.append(right / coefficients[0])
    return result


def exact_pade(
    coefficients: list[Fraction], numerator_degree: int, denominator_degree: int
) -> tuple[list[sp.Rational], list[sp.Rational]]:
    required = numerator_degree + denominator_degree + 1
    if len(coefficients) < required:
        raise ValueError("insufficient Taylor coefficients for requested Pade order")
    c = [sp.Rational(item.numerator, item.denominator) for item in coefficients]
    matrix = sp.Matrix(
        [
            [
                c[numerator_degree + row + 1 - column]
                for column in range(1, denominator_degree + 1)
            ]
            for row in range(denominator_degree)
        ]
    )
    right = sp.Matrix(
        [-c[numerator_degree + row + 1] for row in range(denominator_degree)]
    )
    denominator_tail = list(matrix.inv() * right)
    denominator = [sp.S.One, *denominator_tail]
    numerator = [
        sum(
            denominator[index] * c[degree - index]
            for index in range(min(degree, denominator_degree) + 1)
        )
        for degree in range(numerator_degree + 1)
    ]
    return numerator, denominator


def polynomial(
    coefficients: list[sp.Rational], variable: sp.Symbol
) -> sp.Poly:
    return sp.Poly(
        sum(value * variable**index for index, value in enumerate(coefficients)),
        variable,
        domain=sp.QQ,
    )


def polynomial_digest(poly: sp.Poly) -> dict[str, object]:
    _denominator, integer_poly = poly.clear_denoms(convert=True)
    _content, primitive = integer_poly.primitive()
    if primitive.LC() < 0:
        primitive = -primitive
    coefficients = primitive.all_coeffs()
    serialized = ",".join(str(value) for value in coefficients)
    return {
        "degree": primitive.degree(),
        "primitiveIntegerCoefficientSha256": hashlib.sha256(
            serialized.encode("ascii")
        ).hexdigest(),
        "maximumCoefficientDigits": max(len(str(abs(value))) for value in coefficients),
    }


Interval = tuple[sp.Rational, sp.Rational]


def interval_add(left: Interval, right: Interval) -> Interval:
    return left[0] + right[0], left[1] + right[1]


def interval_multiply(left: Interval, right: Interval) -> Interval:
    values = [a * b for a in left for b in right]
    return min(values), max(values)


def interval_divide(left: Interval, right: Interval) -> Interval:
    if right[0] <= 0 <= right[1]:
        raise ZeroDivisionError("interval denominator contains zero")
    values = [a / b for a in left for b in right]
    return min(values), max(values)


def polynomial_interval(poly: sp.Poly, domain: Interval) -> Interval:
    result = (sp.S.Zero, sp.S.Zero)
    for coefficient in poly.all_coeffs():
        result = interval_add(
            interval_multiply(result, domain),
            (coefficient, coefficient),
        )
    return result


def interval_record(interval: Interval, digits: int = 18) -> dict[str, object]:
    return {
        "lower": str(interval[0]),
        "upper": str(interval[1]),
        "decimal": [
            str(sp.N(interval[0], digits)),
            str(sp.N(interval[1], digits)),
        ],
        "width": str(interval[1] - interval[0]),
    }


def mp_polynomial_value(
    coefficients: list[sp.Rational], value: mp.mpf
) -> mp.mpf:
    result = mp.mpf("0")
    for coefficient in reversed(coefficients):
        result = result * value + mp.mpf(str(coefficient.p)) / mp.mpf(
            str(coefficient.q)
        )
    return result


def numerical_root_regression(
    denominator: list[sp.Rational], exact_interval: Interval
) -> dict[str, object]:
    results: dict[int, mp.mpf] = {}
    center = (exact_interval[0] + exact_interval[1]) / 2
    for precision in (160, 256):
        with mp.workprec(precision):
            initial = mp.mpf(str(center.p)) / mp.mpf(str(center.q))
            root = mp.findroot(
                lambda value: mp_polynomial_value(denominator, value),
                initial,
                solver="newton",
                tol=mp.power(2, -(precision - 20)),
                verify=True,
            )
            results[precision] = +root
    with mp.workprec(256):
        difference = abs(results[160] - results[256])
        return {
            "bits160": mp.nstr(results[160], 45),
            "bits256": mp.nstr(results[256], 70),
            "absoluteDifference": mp.nstr(difference, 20),
        }


def select_isolated_root(
    poly: sp.Poly, window: Interval, isolation_power: int = 32
) -> tuple[Interval, int]:
    intervals = poly.intervals(eps=sp.Rational(1, 10**isolation_power))
    selected = [
        (interval, multiplicity)
        for interval, multiplicity in intervals
        if interval[0] > window[0] and interval[1] < window[1]
    ]
    if len(selected) != 1:
        raise AssertionError(
            f"expected one isolated root in {window}, found {len(selected)}"
        )
    return selected[0]


def approximant_record(
    field_name: str,
    coefficients: list[Fraction],
    cut: int,
    window: Interval,
) -> dict[str, object]:
    order = (cut - 2) // 2
    dlog = dlog_coefficients(coefficients[:cut])
    numerator, denominator = exact_pade(dlog, order, order)
    variable = sp.symbols("R")
    numerator_poly = polynomial(numerator, variable)
    denominator_poly = polynomial(denominator, variable)
    root_interval, multiplicity = select_isolated_root(
        denominator_poly, window
    )
    numerator_at_root = polynomial_interval(numerator_poly, root_interval)
    derivative_at_root = polynomial_interval(
        denominator_poly.diff(), root_interval
    )
    if numerator_at_root[0] <= 0 <= numerator_at_root[1]:
        raise AssertionError("Pade numerator may vanish at candidate root")
    residue = interval_divide(numerator_at_root, derivative_at_root)
    gcd_degree = sp.gcd(numerator_poly, denominator_poly).degree()
    if multiplicity != 1 or gcd_degree != 0:
        raise AssertionError("candidate is not a simple uncancelled approximant pole")
    return {
        "field": field_name,
        "coefficientCut": cut,
        "padeOrder": [order, order],
        "candidateWindow": interval_record(window),
        "isolatedRoot": interval_record(root_interval, 30),
        "multiplicity": multiplicity,
        "numeratorAtRoot": interval_record(numerator_at_root),
        "denominatorDerivativeAtRoot": interval_record(derivative_at_root),
        "residue": interval_record(residue, 24),
        "gcdDegree": gcd_degree,
        "numerator": polynomial_digest(numerator_poly),
        "denominator": polynomial_digest(denominator_poly),
        "dualPrecision": numerical_root_regression(denominator, root_interval),
    }


def root_interval_from_record(record: dict[str, object]) -> Interval:
    item = record["isolatedRoot"]
    return sp.Rational(item["lower"]), sp.Rational(item["upper"])


def residue_interval_from_record(record: dict[str, object]) -> Interval:
    item = record["residue"]
    return sp.Rational(item["lower"]), sp.Rational(item["upper"])


def hull_record(records: list[dict[str, object]]) -> dict[str, object]:
    intervals = [root_interval_from_record(record) for record in records]
    return interval_record(
        (min(item[0] for item in intervals), max(item[1] for item in intervals)),
        24,
    )


def coefficient_ratio_records(
    values: list[Fraction], minimum_parameter: int
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for index in range(max(1, minimum_parameter - 1), len(values)):
        ratio = abs(values[index - 1] / values[index])
        records.append(
            {
                "parameter": index + 1,
                "exact": str(ratio),
                "decimal": str(sp.N(sp.Rational(ratio.numerator, ratio.denominator), 18)),
            }
        )
    return records


def candidate_diagnostics(
    records: list[dict[str, object]], minimum_cut: int, cut_step: int,
    show_progress: bool, started: float,
) -> dict[str, object]:
    if minimum_cut < 8 or minimum_cut % 2:
        raise ValueError("minimum cut must be an even integer at least 8")
    maximum_cut = len(records)
    cuts = list(range(minimum_cut, maximum_cut + 1, cut_step))
    cuts = [cut for cut in cuts if cut % 2 == 0]
    if not cuts or cuts[-1] != maximum_cut:
        raise ValueError("cut schedule must include the even maximum endpoint count")

    series = {
        "u": fraction_series(records, "u"),
        "v": fraction_series(records, "v"),
        "dCenter": fraction_series(records, "dCenter"),
    }
    transport: list[dict[str, object]] = []
    for field_name in ("u", "v"):
        for cut in cuts:
            progress(
                show_progress,
                started,
                "exact D-log Pade isolation",
                field=field_name,
                coefficientCut=cut,
            )
            transport.append(
                approximant_record(
                    field_name, series[field_name], cut, TRANSPORT_WINDOW
                )
            )

    d_zeros: list[dict[str, object]] = []
    for cut in cuts:
        progress(
            show_progress,
            started,
            "exact zero-candidate classification",
            field="dCenter",
            coefficientCut=cut,
        )
        d_zeros.append(
            approximant_record("dCenter", series["dCenter"], cut, D_ZERO_WINDOW)
        )

    tail_minimum_cut = max(minimum_cut, maximum_cut - 8)
    tail_transport = [
        record
        for record in transport
        if int(record["coefficientCut"]) >= tail_minimum_cut
    ]
    all_residues = [residue_interval_from_record(record) for record in transport]
    zero_residues = [residue_interval_from_record(record) for record in d_zeros]
    dual_differences = [
        mp.mpf(record["dualPrecision"]["absoluteDifference"])
        for record in transport + d_zeros
    ]
    transport_hull = hull_record(transport)
    tail_hull = hull_record(tail_transport)
    checks = {
        "uniqueSimpleTransportPolePerApproximant": all(
            record["multiplicity"] == 1 and record["gcdDegree"] == 0
            for record in transport
        ),
        "transportResiduesStrictlyBelowMinusOneHalf": all(
            interval[1] < sp.Rational(-1, 2) for interval in all_residues
        ),
        "allTransportClusterWidthBelowThreeTimesTenToMinusFour": bool(
            sp.Rational(transport_hull["width"]) < sp.Rational(3, 10000)
        ),
        "tailTransportClusterWidthBelowOneTimesTenToMinusFour": bool(
            maximum_cut < 42
            or sp.Rational(tail_hull["width"]) < sp.Rational(1, 10000)
        ),
        "dCenterResiduesPositiveAndNearOne": all(
            interval[0] > sp.Rational(49, 50)
            and interval[1] < sp.Rational(103, 100)
            for interval in zero_residues
        ),
        "dualPrecisionAgreement": max(dual_differences) < mp.mpf("1e-40"),
    }
    return {
        "definition": {
            "fixedChargeSeries": "F_1(R)=[Xi^1]F(R,Xi)=sum_(N>=1) f_(N,1) R^N",
            "normalization": "hat F_1(R)=F_1(R)/R",
            "dlog": "G_F=(hat F_1)'/hat F_1",
            "localInterpretation": (
                "if hat F=C(R)(1-R/R*)^(-gamma) with analytic nonzero C, "
                "then G_F has a simple pole at R* with residue -gamma; "
                "a zero of multiplicity m gives residue +m"
            ),
        },
        "cutSchedule": cuts,
        "transportApproximants": transport,
        "transportClusterHull": transport_hull,
        "tailMinimumCut": tail_minimum_cut,
        "tailTransportClusterHull": tail_hull,
        "dCenterZeroApproximants": d_zeros,
        "dCenterZeroClusterHull": hull_record(d_zeros),
        "coefficientRatios": {
            "u": coefficient_ratio_records(series["u"], 42),
            "v": coefficient_ratio_records(series["v"], 42),
        },
        "checks": checks,
    }


def fixed_charge_analyticity_theorem() -> dict[str, object]:
    radius = Rational(1, 1) / K_MAJORANT**3
    return {
        "statement": (
            "R0.31 implies every fixed-charge U and V series is absolutely "
            "analytic for |R|<(4/81)^3"
        ),
        "reason": (
            "the charge-q coefficient at R^k has total degree 3k-q and is "
            "bounded by the corresponding total-degree l1 layer norm"
        ),
        "guaranteedRadius": {
            "exact": str(radius),
            "decimal": r028.rational_decimal(radius, 18),
        },
        "candidateOutsideProvedContinuation": True,
    }


def build_payload(arguments: argparse.Namespace) -> dict[str, object]:
    started = time.perf_counter()
    checkpoint_test = checkpoint_resume_regression()
    progress(
        arguments.progress,
        started,
        "completed checkpoint-resume regression",
        passed=checkpoint_test["passed"],
    )

    root_payload = json.loads(R028_CERTIFICATE.read_text(encoding="utf-8"))
    p_center = Rational(root_payload["rootBox"]["center"]["p"])
    q_center = Rational(root_payload["rootBox"]["center"]["q"])
    a, u, v, interactions, checkpoint_summary = (
        resumable_rational_edge_recurrence(
            arguments.max_total_degree,
            arguments.progress,
            started,
            arguments.checkpoint,
            arguments.resume,
            arguments.checkpoint_interval,
        )
    )
    records = endpoint_records(
        a, u, v, arguments.max_total_degree, p_center, q_center
    )
    old_regression = r028_endpoint_regression(records)
    progress(
        arguments.progress,
        started,
        "completed R0.28 endpoint regression",
        passed=old_regression["passed"],
        endpointCount=len(records),
    )
    diagnostic = candidate_diagnostics(
        records,
        arguments.minimum_cut,
        arguments.cut_step,
        arguments.progress,
        started,
    )
    checks = {
        "checkpointResumeRegression": checkpoint_test,
        "r028EndpointRegression": old_regression,
        "candidateDiagnostics": {
            "passed": all(diagnostic["checks"].values()),
            **diagnostic["checks"],
        },
    }
    progress(
        arguments.progress,
        started,
        "completed R0.32 finite candidate certificate",
        passed=all(item["passed"] for item in checks.values()),
    )
    return {
        "scope": {
            "result": (
                "certified finite D-log Pade stability cluster for exact "
                "charge-one edge coefficients"
            ),
            "maximumExactTotalDegree": arguments.max_total_degree,
            "maximumEndpointParameter": len(records),
            "classification": "finite exact diagnostic, not a singularity theorem",
            "limitations": [
                "the isolated roots are poles of finite rational approximants, not certified singularities of the original fixed-charge series",
                "no analytic continuation or Taylor remainder bound reaches the candidate cluster",
                "stability across truncations does not prove dominance or convergence of Pade poles",
                "the reduced edge system is not the full three-dimensional Navier-Stokes equation",
                "no Navier-Stokes regularity or blow-up conclusion is claimed",
            ],
        },
        "allOrderInput": fixed_charge_analyticity_theorem(),
        "exactEndpoints": records,
        "diagnostic": diagnostic,
        "checks": checks,
        "digests": {
            "aThroughMaximumDegree": field_digest(a, arguments.max_total_degree),
            "uThroughMaximumDegree": field_digest(u, arguments.max_total_degree),
            "vThroughMaximumDegree": field_digest(v, arguments.max_total_degree),
        },
        "computation": {
            "backend": "GMP exact rationals + SymPy exact polynomial isolation",
            "recurrenceOrderedInteractions": interactions,
            "checkpoint": checkpoint_summary,
            "wallSeconds": time.perf_counter() - started,
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "gmpy2": gmpy2.version(),
            "gmp": gmpy2.mp_version(),
            "mpmath": mp.__version__,
            "sympy": sp.__version__,
        },
        "git": r028.git_source_state(),
    }


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-total-degree", type=int, default=149)
    parser.add_argument("--minimum-cut", type=int, default=30)
    parser.add_argument("--cut-step", type=int, default=2)
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--checkpoint-interval", type=int, default=25)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--progress-log", type=Path)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    if arguments.max_total_degree < 89:
        parser.error("--max-total-degree must be at least 89 (30 endpoints)")
    if (arguments.max_total_degree + 1) % 3:
        parser.error("--max-total-degree must equal 3*N-1")
    if arguments.cut_step < 1:
        parser.error("--cut-step must be positive")
    if arguments.resume and arguments.checkpoint is None:
        parser.error("--resume requires --checkpoint")
    return arguments


def main() -> None:
    global PROGRESS_LOG
    arguments = parse_arguments()
    if arguments.progress_log is not None:
        if arguments.progress_log.exists():
            raise SystemExit("--progress-log already exists; choose a new path")
        arguments.progress_log.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_LOG = arguments.progress_log
    payload = build_payload(arguments)
    if arguments.check:
        failures = [
            name for name, check in payload["checks"].items() if not check["passed"]
        ]
        if failures:
            raise AssertionError("R0.32 checks failed: " + ", ".join(failures))
    if arguments.output is None:
        json.dump(
            payload,
            sys.stdout,
            ensure_ascii=False,
            indent=2 if arguments.pretty else None,
            sort_keys=True,
        )
        sys.stdout.write("\n")
    else:
        r028.atomic_json_write(arguments.output, payload, arguments.pretty)


if __name__ == "__main__":
    main()
