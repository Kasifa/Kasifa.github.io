#!/usr/bin/env python3
"""Construct exact Bernstein strip certificates at the two R0.20 x-boundaries.

The saturated third stationary polynomial is denoted by ``F(p,q,x)``.  Near
``x=0`` it has the negative principal part

    -A(q) (p-2)^2 - B(q) x,

and near ``x=infinity`` its reversed polynomial

    H(p,q,t) = t^deg_x(F) F(p,q,1/t)

has the positive principal part ``C(p) (q-3)^10 + D(p) t``.  This program
turns those asymptotic statements into finite-width, exact certificates.

For dyadic ``delta`` and ``epsilon`` it compactifies the unbounded transverse
variable, splits the signed displacement at zero, maps each half-strip to the
unit cube, and converts the resulting rational polynomial to tensor-product
Bernstein form using exact ``Fraction`` arithmetic.  A strip is certified if
all Bernstein coefficients have the required weak sign and the terminal
coefficient layer in the positive boundary-distance variable has the strict
sign.  The terminal layer makes the polynomial strict at every finite point
of the open physical strip, while allowing its known zero on the compact
boundary itself.

This remains a statement about the finite fifth-order model, not the
Navier--Stokes PDE.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
from fractions import Fraction
import gzip
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys
import time
from typing import Iterable


Rational = Fraction
PowerMap = dict[tuple[int, int, int], Rational]
SYSTEM_NAME = "saturated_stationary_x"


def emit(stage: str, started: float, **fields: object) -> None:
    print(
        json.dumps(
            {
                "timestampUtc": datetime.now(timezone.utc).isoformat(),
                "elapsedSeconds": round(time.perf_counter() - started, 3),
                "stage": stage,
                **fields,
            },
            separators=(",", ":"),
        ),
        file=sys.stderr,
        flush=True,
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            block = stream.read(1024 * 1024)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def load_rows(path: Path) -> list[list[object]]:
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        payload = json.load(stream)
    if payload.get("schemaVersion") != 2:
        raise ValueError("R0.20 exact cache schema version 2 is required")
    return payload["polynomials"][SYSTEM_NAME]


def coefficient(row: list[object]) -> Rational:
    return Rational(int(row[3]), int(row[4]))


def evaluate_rows(
    rows: list[list[object]],
    point: tuple[Rational, Rational, Rational],
) -> Rational:
    return sum(
        coefficient(row)
        * math.prod(point[axis] ** int(row[axis]) for axis in range(3))
        for row in rows
    )


def add_term(target: defaultdict[tuple[int, int, int], Rational], powers: tuple[int, int, int], value: Rational) -> None:
    if value:
        target[powers] += value


def zero_base(rows: list[list[object]]) -> tuple[PowerMap, tuple[int, int, int]]:
    """Return (r,v,x) powers after p=2+r and q=v/(1-v)."""
    degree_q = max(int(row[1]) for row in rows)
    degree_r = max(int(row[0]) for row in rows)
    degree_x = max(int(row[2]) for row in rows)
    result: defaultdict[tuple[int, int, int], Rational] = defaultdict(Rational)
    for row in rows:
        power_p, power_q, power_x = map(int, row[:3])
        source = coefficient(row)
        for power_r in range(power_p + 1):
            p_factor = math.comb(power_p, power_r) * 2 ** (power_p - power_r)
            for extra_v in range(degree_q - power_q + 1):
                value = source * p_factor * math.comb(degree_q - power_q, extra_v)
                if extra_v % 2:
                    value = -value
                add_term(result, (power_r, power_q + extra_v, power_x), value)
    return dict(result), (degree_r, degree_q, degree_x)


def infinity_base(rows: list[list[object]]) -> tuple[PowerMap, tuple[int, int, int]]:
    """Return (u,r,t) powers after p=u/(1-u), q=3+r, x=1/t."""
    degree_p = max(int(row[0]) for row in rows)
    degree_r = max(int(row[1]) for row in rows)
    degree_x = max(int(row[2]) for row in rows)
    result: defaultdict[tuple[int, int, int], Rational] = defaultdict(Rational)
    for row in rows:
        power_p, power_q, power_x = map(int, row[:3])
        source = coefficient(row)
        power_t = degree_x - power_x
        for extra_u in range(degree_p - power_p + 1):
            p_factor = math.comb(degree_p - power_p, extra_u)
            if extra_u % 2:
                p_factor = -p_factor
            for power_r in range(power_q + 1):
                q_factor = math.comb(power_q, power_r) * 3 ** (power_q - power_r)
                add_term(
                    result,
                    (power_p + extra_u, power_r, power_t),
                    source * p_factor * q_factor,
                )
    return dict(result), (degree_p, degree_r, degree_x)


def affine_axis(source: PowerMap, axis: int, offset: Rational, scale: Rational) -> PowerMap:
    """Apply old_variable = offset + scale * new_variable on one axis."""
    if offset == 0:
        return {
            powers: value * scale ** powers[axis]
            for powers, value in source.items()
            if value
        }
    result: defaultdict[tuple[int, int, int], Rational] = defaultdict(Rational)
    for powers, value in source.items():
        old_power = powers[axis]
        for new_power in range(old_power + 1):
            new_powers = list(powers)
            new_powers[axis] = new_power
            transformed = (
                value
                * math.comb(old_power, new_power)
                * offset ** (old_power - new_power)
                * scale ** new_power
            )
            add_term(result, tuple(new_powers), transformed)
    return dict(result)


def dense_power(source: PowerMap, degrees: tuple[int, int, int]) -> list[Rational]:
    n1, n2 = degrees[1] + 1, degrees[2] + 1
    dense = [Rational(0)] * math.prod(degree + 1 for degree in degrees)
    for powers, value in source.items():
        dense[(powers[0] * n1 + powers[1]) * n2 + powers[2]] = value
    return dense


def flat_index(powers: tuple[int, int, int], degrees: tuple[int, int, int]) -> int:
    return (powers[0] * (degrees[1] + 1) + powers[1]) * (degrees[2] + 1) + powers[2]


def power_to_bernstein(source: PowerMap, degrees: tuple[int, int, int]) -> list[Rational]:
    """Convert a unit-cube power tensor to Bernstein coefficients exactly."""
    current = dense_power(source, degrees)
    ranges = [range(degree + 1) for degree in degrees]
    for axis, degree in enumerate(degrees):
        transformed = [Rational(0)] * len(current)
        other_axes = [candidate for candidate in range(3) if candidate != axis]
        for fixed in itertools.product(*(ranges[candidate] for candidate in other_axes)):
            base = [0, 0, 0]
            base[other_axes[0]], base[other_axes[1]] = fixed
            for bernstein_index in range(degree + 1):
                total = Rational(0)
                denominator_cache = math.comb(degree, bernstein_index)
                for power_index in range(bernstein_index + 1):
                    base[axis] = power_index
                    value = current[flat_index(tuple(base), degrees)]
                    if value:
                        total += value * Rational(
                            math.comb(bernstein_index, power_index),
                            math.comb(degree, power_index),
                        )
                base[axis] = bernstein_index
                transformed[flat_index(tuple(base), degrees)] = total
        current = transformed
    return current


def rational_text(value: Rational) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def coefficient_digest(values: Iterable[Rational]) -> str:
    digest = hashlib.sha256()
    for value in values:
        digest.update(f"{value.numerator}/{value.denominator}\n".encode("ascii"))
    return digest.hexdigest()


def power_map_digest(source: PowerMap) -> str:
    digest = hashlib.sha256()
    for powers, value in sorted(source.items()):
        digest.update(
            (
                f"{powers[0]},{powers[1]},{powers[2]}:"
                f"{value.numerator}/{value.denominator}\n"
            ).encode("ascii")
        )
    return digest.hexdigest()


def evaluate_power(source: PowerMap, point: tuple[Rational, Rational, Rational]) -> Rational:
    return sum(
        value * math.prod(point[axis] ** powers[axis] for axis in range(3))
        for powers, value in source.items()
    )


def evaluate_bernstein(
    values: list[Rational],
    degrees: tuple[int, int, int],
    point: tuple[Rational, Rational, Rational],
) -> Rational:
    basis = []
    for axis, degree in enumerate(degrees):
        coordinate = point[axis]
        basis.append([
            math.comb(degree, index)
            * coordinate ** index
            * (1 - coordinate) ** (degree - index)
            for index in range(degree + 1)
        ])
    return sum(
        values[flat_index((i, j, k), degrees)]
        * basis[0][i]
        * basis[1][j]
        * basis[2][k]
        for i in range(degrees[0] + 1)
        for j in range(degrees[1] + 1)
        for k in range(degrees[2] + 1)
    )


def sign_record(values: list[Rational], degrees: tuple[int, int, int], required_sign: int) -> dict[str, object]:
    negative = sum(value < 0 for value in values)
    zero = sum(value == 0 for value in values)
    positive = len(values) - negative - zero
    last_distance_layer = [
        values[flat_index((i, j, degrees[2]), degrees)]
        for i in range(degrees[0] + 1)
        for j in range(degrees[1] + 1)
    ]
    weak = positive == 0 if required_sign < 0 else negative == 0
    terminal_strict = (
        all(value < 0 for value in last_distance_layer)
        if required_sign < 0
        else all(value > 0 for value in last_distance_layer)
    )
    return {
        "coefficientCount": len(values),
        "negativeCount": negative,
        "zeroCount": zero,
        "positiveCount": positive,
        "weakRequiredSign": weak,
        "terminalBoundaryDistanceLayerStrict": terminal_strict,
        "minimum": rational_text(min(values)),
        "maximum": rational_text(max(values)),
        "terminalLayerMinimum": rational_text(min(last_distance_layer)),
        "terminalLayerMaximum": rational_text(max(last_distance_layer)),
        "exactCoefficientDigest": coefficient_digest(values),
        "certified": weak and terminal_strict,
    }


def chart_attempt(
    base: PowerMap,
    degrees: tuple[int, int, int],
    displacement_axis: int,
    transverse_axis: int | None,
    transverse_depth: int,
    delta: Rational,
    epsilon: Rational,
    required_sign: int,
) -> dict[str, object]:
    cell_count = 1 if transverse_axis is None else 2 ** transverse_depth
    cells = []
    for cell_index in range(cell_count):
        if transverse_axis is None:
            cell_base = base
            lower, upper = Rational(0), Rational(1)
        else:
            lower = Rational(cell_index, cell_count)
            upper = Rational(cell_index + 1, cell_count)
            cell_base = affine_axis(
                base,
                transverse_axis,
                lower,
                upper - lower,
            )
        halves = []
        for label, offset in (("negative", -delta), ("positive", Rational(0))):
            local = affine_axis(cell_base, displacement_axis, offset, delta)
            local = affine_axis(local, 2, Rational(0), epsilon)
            bernstein = power_to_bernstein(local, degrees)
            check_point = (Rational(2, 7), Rational(3, 7), Rational(5, 11))
            if evaluate_power(local, check_point) != evaluate_bernstein(
                bernstein,
                degrees,
                check_point,
            ):
                raise AssertionError("exact power/Bernstein reconstruction failed")
            record = sign_record(bernstein, degrees, required_sign)
            record["exactReconstructionCheck"] = True
            record["signedDisplacementHalf"] = label
            halves.append(record)
        cells.append(
            {
                "transverseCompactInterval": [rational_text(lower), rational_text(upper)],
                "halves": halves,
                "certified": all(record["certified"] for record in halves),
            }
        )
    return {
        "delta": rational_text(delta),
        "epsilon": rational_text(epsilon),
        "transverseSubdivisionDepth": transverse_depth,
        "cells": cells,
        "certified": all(cell["certified"] for cell in cells),
    }


def search_chart(
    name: str,
    base: PowerMap,
    degrees: tuple[int, int, int],
    displacement_axis: int,
    transverse_axis: int | None,
    required_sign: int,
    transverse_depths: range,
    delta_exponents: range,
    epsilon_exponents: range,
    started: float,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    attempts = []
    for transverse_depth in transverse_depths:
        for delta_exponent in delta_exponents:
            delta = Rational(1, 2 ** delta_exponent)
            for epsilon_exponent in epsilon_exponents:
                epsilon = Rational(1, 2 ** epsilon_exponent)
                record = chart_attempt(
                    base,
                    degrees,
                    displacement_axis,
                    transverse_axis,
                    transverse_depth,
                    delta,
                    epsilon,
                    required_sign,
                )
                attempts.append(
                    {
                        "transverseSubdivisionDepth": transverse_depth,
                        "deltaExponent": delta_exponent,
                        "epsilonExponent": epsilon_exponent,
                        "certified": record["certified"],
                    }
                )
                emit(
                    "tested exact boundary strip",
                    started,
                    chart=name,
                    transverseSubdivisionDepth=transverse_depth,
                    deltaExponent=delta_exponent,
                    epsilonExponent=epsilon_exponent,
                    certified=record["certified"],
                )
                if record["certified"]:
                    record["deltaExponent"] = delta_exponent
                    record["epsilonExponent"] = epsilon_exponent
                    return record, attempts
    raise RuntimeError(f"no exact strip certificate found for {name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-delta-exponent", type=int, default=12)
    parser.add_argument("--max-epsilon-exponent", type=int, default=36)
    parser.add_argument("--max-transverse-depth", type=int, default=4)
    arguments = parser.parse_args()
    started = time.perf_counter()
    rows = load_rows(arguments.cache)
    zero_polynomial, zero_degrees = zero_base(rows)
    infinity_polynomial, infinity_degrees = infinity_base(rows)
    zero_check_point = (Rational(1, 5), Rational(2, 7), Rational(1, 11))
    zero_r, zero_v, zero_x = zero_check_point
    if evaluate_power(zero_polynomial, zero_check_point) != (
        (1 - zero_v) ** zero_degrees[1]
        * evaluate_rows(
            rows,
            (2 + zero_r, zero_v / (1 - zero_v), zero_x),
        )
    ):
        raise AssertionError("the exact x=0 compactification identity failed")
    infinity_check_point = (Rational(2, 7), Rational(-1, 5), Rational(1, 11))
    infinity_u, infinity_r, infinity_t = infinity_check_point
    if evaluate_power(infinity_polynomial, infinity_check_point) != (
        (1 - infinity_u) ** infinity_degrees[0]
        * infinity_t ** infinity_degrees[2]
        * evaluate_rows(
            rows,
            (
                infinity_u / (1 - infinity_u),
                3 + infinity_r,
                1 / infinity_t,
            ),
        )
    ):
        raise AssertionError("the exact x=infinity compactification identity failed")
    emit(
        "constructed exact compact boundary polynomials",
        started,
        zeroTerms=len(zero_polynomial),
        infinityTerms=len(infinity_polynomial),
    )

    zero, zero_attempts = search_chart(
        "x=0",
        zero_polynomial,
        zero_degrees,
        0,
        None,
        -1,
        range(0, 1),
        range(1, arguments.max_delta_exponent + 1),
        range(1, arguments.max_epsilon_exponent + 1),
        started,
    )
    infinity, infinity_attempts = search_chart(
        "x=infinity",
        infinity_polynomial,
        infinity_degrees,
        1,
        0,
        1,
        range(1, arguments.max_transverse_depth + 1),
        range(1, arguments.max_delta_exponent + 1),
        range(1, arguments.max_epsilon_exponent + 1),
        started,
    )

    # These dyadic sub-strips lie strictly inside the wider exact physical
    # certificates and align after finitely many midpoint subdivisions in the
    # global compact cube (u,v,w).
    zero_core = (
        (Rational(5, 8), Rational(11, 16)),
        (Rational(0), Rational(1)),
        (Rational(0), Rational(1, 16)),
    )
    infinity_core = (
        (Rational(0), Rational(1)),
        (Rational(47, 64), Rational(49, 64)),
        (Rational(7, 8), Rational(1)),
    )
    zero_delta = Rational(zero["delta"])
    zero_epsilon = Rational(zero["epsilon"])
    infinity_delta = Rational(infinity["delta"])
    infinity_epsilon = Rational(infinity["epsilon"])
    if not (
        zero_core[0][0] / (1 - zero_core[0][0]) >= 2 - zero_delta
        and zero_core[0][1] / (1 - zero_core[0][1]) <= 2 + zero_delta
        and zero_core[2][1] / (1 - zero_core[2][1]) <= zero_epsilon
    ):
        raise AssertionError("the dyadic x=0 core was not inside its exact strip")
    if not (
        infinity_core[1][0] / (1 - infinity_core[1][0]) >= 3 - infinity_delta
        and infinity_core[1][1] / (1 - infinity_core[1][1]) <= 3 + infinity_delta
        and (1 - infinity_core[2][0]) / infinity_core[2][0] <= infinity_epsilon
    ):
        raise AssertionError("the dyadic x=infinity core was not inside its exact strip")

    def compact_box_record(box: tuple[tuple[Rational, Rational], ...]) -> list[list[str]]:
        return [[rational_text(lower), rational_text(upper)] for lower, upper in box]

    result = {
        "schemaVersion": 1,
        "scope": "exact finite-width strip exclusion around both degenerate x-boundary components",
        "cache": str(arguments.cache.resolve()),
        "cacheSha256": sha256_file(arguments.cache),
        "stationaryEquation": SYSTEM_NAME,
        "constructionIdentityChecks": {
            "zeroBoundaryCompactification": True,
            "infinityBoundaryCompactification": True,
        },
        "proofStatus": (
            "complete exact Bernstein sign exclusion in the two recorded strips; "
            "the complement remains assigned to the global cube audit"
        ),
        "zeroBoundary": {
            "physicalStrip": "0<x<=epsilon, |p-2|<=delta, 0<=q<infinity",
            "compactification": "q=v/(1-v)",
            "requiredSign": "strictly negative",
            "degrees": list(zero_degrees),
            "baseTermCount": len(zero_polynomial),
            "basePolynomialDigest": power_map_digest(zero_polynomial),
            "certificate": zero,
            "dyadicCoreCompactCube": compact_box_record(zero_core),
            "searchAttempts": zero_attempts,
        },
        "infinityBoundary": {
            "physicalStrip": "0<t=1/x<=epsilon, |q-3|<=delta, 0<=p<infinity",
            "compactification": "p=u/(1-u)",
            "requiredSign": "strictly positive",
            "degrees": list(infinity_degrees),
            "baseTermCount": len(infinity_polynomial),
            "basePolynomialDigest": power_map_digest(infinity_polynomial),
            "certificate": infinity,
            "dyadicCoreCompactCube": compact_box_record(infinity_core),
            "searchAttempts": infinity_attempts,
        },
        "wallSeconds": time.perf_counter() - started,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    emit("exact boundary-strip audit completed", started)


if __name__ == "__main__":
    main()
