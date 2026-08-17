#!/usr/bin/env python3
"""Exactly audit the four finite codimension-two edges of R0.20.

After fixing ``p`` and ``q`` independently at zero or infinity, the target
fraction is a rational function of ``x`` alone.  This script constructs each
edge from the exact three-variable cache, removes the endpoint factor from
the derivative numerator, counts and isolates every positive root by Sturm
methods, and proves the unique positive root is the strict global edge
maximum.  All reported bounds use exact rational interval arithmetic.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from decimal import Decimal, localcontext
import gzip
import hashlib
import json
from pathlib import Path
import sys
import time

import sympy as sp


P, Q, X = sp.symbols("p q x", positive=True)
VARIABLES = (P, Q, X)
SIDES = ("zero", "infinity")
Interval = tuple[sp.Rational, sp.Rational]


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


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


def load_cache(path: Path) -> dict[str, object]:
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        payload = json.load(stream)
    if payload.get("schemaVersion") != 2:
        raise ValueError("R0.20 exact cache schema version 2 is required")
    return payload


def parse_polynomial(rows: list[list[object]]) -> sp.Poly:
    return sp.Poly(
        sp.Add(*(
            sp.Rational(int(row[3]), int(row[4]))
            * P ** int(row[0])
            * Q ** int(row[1])
            * X ** int(row[2])
            for row in rows
        )),
        *VARIABLES,
        domain=sp.QQ,
    )


def coefficient_face(source: sp.Poly, variable: sp.Symbol, side: str) -> sp.Poly:
    axis = source.gens.index(variable)
    powers_on_axis = [powers[axis] for powers, _coefficient in source.terms()]
    power = min(powers_on_axis) if side == "zero" else max(powers_on_axis)
    remaining = tuple(item for item in source.gens if item != variable)
    expression = sp.Add(*(
        coefficient
        * sp.prod(
            source.gens[index] ** powers[index]
            for index in range(len(source.gens))
            if index != axis
        )
        for powers, coefficient in source.terms()
        if powers[axis] == power
    ))
    return sp.Poly(expression, *remaining, domain=sp.QQ)


def valuation(source: sp.Poly) -> int:
    return min(powers[0] for powers, _coefficient in source.terms())


def digest(source: sp.Poly) -> str:
    text = "\n".join(
        f"{','.join(map(str, powers))}:{coefficient}"
        for powers, coefficient in source.terms()
    )
    return hashlib.sha256(text.encode("ascii")).hexdigest()


def serialize(source: sp.Poly) -> list[list[str]]:
    return [
        [str(powers[0]), str(int(coefficient.p)), str(int(coefficient.q))]
        for powers, coefficient in source.terms()
    ]


def interval_add(left: Interval, right: Interval) -> Interval:
    return left[0] + right[0], left[1] + right[1]


def interval_multiply(left: Interval, right: Interval) -> Interval:
    values = [left[a] * right[b] for a in range(2) for b in range(2)]
    return min(values), max(values)


def polynomial_interval(source: sp.Poly, domain: Interval) -> Interval:
    result = (sp.Rational(0), sp.Rational(0))
    for coefficient in source.all_coeffs():
        result = interval_add(
            interval_multiply(result, domain),
            (coefficient, coefficient),
        )
    return result


def interval_divide(left: Interval, right: Interval) -> Interval:
    if right[0] <= 0 <= right[1]:
        raise ArithmeticError("denominator interval crossed zero")
    return interval_multiply(left, (1 / right[1], 1 / right[0]))


def rational_string(value: sp.Rational) -> str:
    return f"{int(value.p)}/{int(value.q)}"


def decimal_string(value: sp.Rational, precision: int = 60) -> str:
    with localcontext() as context:
        context.prec = precision
        return str(Decimal(int(value.p)) / Decimal(int(value.q)))


def interval_record(domain: Interval) -> dict[str, str]:
    return {
        "lower": rational_string(domain[0]),
        "upper": rational_string(domain[1]),
        "lowerDecimal": decimal_string(domain[0]),
        "upperDecimal": decimal_string(domain[1]),
    }


def audit_edge(
    target: sp.Poly,
    total: sp.Poly,
    p_side: str,
    q_side: str,
    isolation_digits: int,
) -> dict[str, object]:
    target_edge = coefficient_face(
        coefficient_face(target, P, p_side),
        Q,
        q_side,
    )
    total_edge = coefficient_face(
        coefficient_face(total, P, p_side),
        Q,
        q_side,
    )
    if target_edge.gens != (X,) or total_edge.gens != (X,):
        raise AssertionError("edge extraction did not leave x as the sole variable")
    zero_order_difference = valuation(target_edge) - valuation(total_edge)
    infinity_order_difference = total_edge.degree() - target_edge.degree()
    if zero_order_difference <= 0 or infinity_order_difference <= 0:
        raise AssertionError("the target fraction did not vanish at both edge endpoints")
    if any(coefficient <= 0 for coefficient in target_edge.coeffs()):
        raise AssertionError("the target-energy edge polynomial was not positive for x>0")
    if any(coefficient <= 0 for coefficient in total_edge.all_coeffs()):
        raise AssertionError("the total-energy edge polynomial was not coefficient-positive")

    stationary = sp.Poly(
        target_edge.diff().as_expr() * total_edge.as_expr()
        - target_edge.as_expr() * total_edge.diff().as_expr(),
        X,
        domain=sp.QQ,
    )
    endpoint_valuation = valuation(stationary)
    reduced = sp.exquo(
        stationary,
        sp.Poly(X**endpoint_valuation, X, domain=sp.QQ),
    )
    positive_count = int(reduced.count_roots(0, sp.oo))
    if positive_count != 1:
        raise AssertionError("the reduced edge derivative did not have exactly one positive root")
    intervals = [
        (lower, upper, int(multiplicity))
        for (lower, upper), multiplicity in reduced.intervals(
            eps=sp.Rational(1, 10**isolation_digits)
        )
        if lower > 0
    ]
    if len(intervals) != 1 or intervals[0][2] != 1:
        raise AssertionError("the unique positive edge root was not simple and isolated")
    root_interval = intervals[0][:2]
    target_interval = polynomial_interval(target_edge, root_interval)
    total_interval = polynomial_interval(total_edge, root_interval)
    fraction_interval = interval_divide(target_interval, total_interval)
    stationary_derivative_interval = polynomial_interval(stationary.diff(), root_interval)

    leading_sign = sp.sign(reduced.LC())
    constant_sign = sp.sign(reduced.TC())
    strict_maximum = (
        constant_sign > 0
        and leading_sign < 0
        and stationary_derivative_interval[1] < 0
    )
    if not strict_maximum:
        raise AssertionError("the isolated edge root was not certified as the global maximum")

    return {
        "edge": f"p_{p_side}__q_{q_side}",
        "fixedSides": {"p": p_side, "q": q_side},
        "endpointLimits": {
            "x_zero": "0",
            "x_infinity": "0",
            "zeroOrderDifference": zero_order_difference,
            "infinityOrderDifference": infinity_order_difference,
        },
        "target": {
            "degree": target_edge.degree(),
            "termCount": len(target_edge.terms()),
            "digest": digest(target_edge),
        },
        "total": {
            "degree": total_edge.degree(),
            "termCount": len(total_edge.terms()),
            "digest": digest(total_edge),
            "allCoefficientsStrictlyPositive": True,
        },
        "stationary": {
            "degree": stationary.degree(),
            "endpointFactor": f"x^{endpoint_valuation}",
            "reducedDegree": reduced.degree(),
            "reducedDigest": digest(reduced),
            "reducedExact": serialize(reduced),
            "positiveRootCount": positive_count,
            "positiveRootSimple": True,
            "constantSign": int(constant_sign),
            "leadingSign": int(leading_sign),
        },
        "rootInterval": interval_record(root_interval),
        "targetFractionInterval": interval_record(fraction_interval),
        "targetFractionPercentMidpoint": float(
            100 * sum(fraction_interval) / 2
        ),
        "stationaryDerivativeInterval": interval_record(stationary_derivative_interval),
        "classification": "unique strict global maximum on the open edge",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--isolation-digits", type=int, default=70)
    arguments = parser.parse_args()
    started = time.perf_counter()
    cache = load_cache(arguments.cache)
    target = parse_polynomial(cache["polynomials"]["target"])
    external = parse_polynomial(cache["polynomials"]["external"])
    total = target + external
    emit("loaded exact target and total", started)

    edges = []
    for p_side in SIDES:
        for q_side in SIDES:
            emit("auditing compact edge", started, pSide=p_side, qSide=q_side)
            edges.append(
                audit_edge(
                    target,
                    total,
                    p_side,
                    q_side,
                    arguments.isolation_digits,
                )
            )
    result = {
        "schemaVersion": 1,
        "scope": "exact finite codimension-two edge audit",
        "proofStatus": (
            "all four finite p/q edges have exactly one positive stationary "
            "point, certified as their strict global maximum"
        ),
        "configuration": {"isolationDigits": arguments.isolation_digits},
        "edges": edges,
        "wallSeconds": time.perf_counter() - started,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    emit("compact edge audit completed", started, edges=len(edges))


if __name__ == "__main__":
    main()
