#!/usr/bin/env python3
"""Build a rational univariate representation for one finite R0.20 face.

For a square-free zero-dimensional two-polynomial system, the penultimate
subresultant is generically linear in the eliminated variable.  On a selected
irreducible resultant component it gives

    A(t) y + B(t) = 0,

where ``t`` is the retained coordinate.  Exact interval evaluation of
``-B/A`` on every isolated positive ``t`` root then certifies the sign of the
paired coordinate and removes projection artifacts without relying on a
multistart scan.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from decimal import Decimal, localcontext
from fractions import Fraction
import gzip
import json
from pathlib import Path
import sys
import time

import sympy as sp
from sympy.external.gmpy import GROUND_TYPES


if hasattr(sys, "set_int_max_str_digits"):
    # Exact interval endpoints can legitimately contain several thousand
    # decimal digits after cancellation-heavy rational division.
    sys.set_int_max_str_digits(0)


Rational = Fraction
Interval = tuple[Rational, Rational]


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
    if payload.get("schemaVersion") != 1:
        raise ValueError("R0.20 boundary cache schema version 1 is required")
    return payload


def parse_bivariate(rows: list[list[object]], variables: tuple[sp.Symbol, sp.Symbol]) -> sp.Poly:
    return sp.Poly(
        sp.Add(*(
            sp.Rational(int(row[2]), int(row[3]))
            * variables[0] ** int(row[0])
            * variables[1] ** int(row[1])
            for row in rows
        )),
        *variables,
        domain=sp.QQ,
    )


def parse_rational(value: str) -> Rational:
    numerator, denominator = value.split("/", 1)
    return Rational(int(numerator), int(denominator))


def interval_add(left: Interval, right: Interval) -> Interval:
    return left[0] + right[0], left[1] + right[1]


def interval_multiply(left: Interval, right: Interval) -> Interval:
    values = [left[a] * right[b] for a in range(2) for b in range(2)]
    return min(values), max(values)


def interval_divide(left: Interval, right: Interval) -> Interval:
    if right[0] <= 0 <= right[1]:
        raise ArithmeticError("denominator interval crossed zero")
    reciprocal = (Rational(1, right[1]), Rational(1, right[0]))
    if reciprocal[0] > reciprocal[1]:
        reciprocal = reciprocal[1], reciprocal[0]
    return interval_multiply(left, reciprocal)


def polynomial_interval(source: sp.Poly, domain: Interval) -> Interval:
    center = (domain[0] + domain[1]) / 2
    radius = (domain[1] - domain[0]) / 2
    sympy_center = sp.Rational(center.numerator, center.denominator)
    center_value_sympy = source.eval(sympy_center)
    center_value = Rational(
        int(center_value_sympy.p),
        int(center_value_sympy.q),
    )
    derivative = source.diff()
    upper = max(abs(domain[0]), abs(domain[1]))
    variation = Rational(0)
    for (power,), coefficient in derivative.terms():
        value = Rational(int(coefficient.p), int(coefficient.q))
        variation += abs(value) * upper**power * radius
    return center_value - variation, center_value + variation


def serialize(source: sp.Poly) -> list[list[str]]:
    return [
        [str(powers[0]), str(int(coefficient.p)), str(int(coefficient.q))]
        for powers, coefficient in source.terms()
    ]


def decimal(value: Rational, digits: int = 30) -> str:
    with localcontext() as context:
        context.prec = digits
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def refine_root_interval(
    component: sp.Poly,
    domain: Interval,
    digits: int,
) -> Interval:
    lower, upper = sp.refine_root(
        component.as_expr(),
        sp.Rational(domain[0].numerator, domain[0].denominator),
        sp.Rational(domain[1].numerator, domain[1].denominator),
        eps=sp.Rational(1, 10**digits),
    )
    return (
        Rational(int(lower.p), int(lower.q)),
        Rational(int(upper.p), int(upper.q)),
    )


def serialize_interval(domain: Interval) -> dict[str, str]:
    return {
        "lower": f"{domain[0].numerator}/{domain[0].denominator}",
        "upper": f"{domain[1].numerator}/{domain[1].denominator}",
        "lowerDecimal": decimal(domain[0]),
        "upperDecimal": decimal(domain[1]),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--face", required=True)
    parser.add_argument("--retained-variable", default="x")
    parser.add_argument("--isolation", type=Path, required=True)
    parser.add_argument("--component-degree", type=int, required=True)
    parser.add_argument("--max-refinement-digits", type=int, default=2560)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    started = time.perf_counter()
    face = load_cache(arguments.cache)["faces"][arguments.face]
    variables = tuple(sp.symbols(" ".join(face["freeVariables"])))
    retained = next(variable for variable in variables if str(variable) == arguments.retained_variable)
    eliminated = next(variable for variable in variables if variable != retained)
    functions = [parse_bivariate(rows, variables) for rows in face["reducedStationary"]]
    emit(
        "computing subresultant sequence",
        started,
        face=arguments.face,
        retained=str(retained),
        eliminated=str(eliminated),
        groundTypes=GROUND_TYPES,
    )
    sequence = sp.subresultants(functions[0].as_expr(), functions[1].as_expr(), eliminated)
    degrees = [sp.Poly(item, eliminated).degree() for item in sequence]
    emit("subresultant sequence completed", started, length=len(sequence), eliminatedDegrees=degrees)
    linear_expression = next(
        item for item in reversed(sequence) if sp.Poly(item, eliminated).degree() == 1
    )
    resultant_expression = next(
        item for item in reversed(sequence) if sp.Poly(item, eliminated).degree() == 0
    )
    linear = sp.Poly(linear_expression, eliminated)
    coefficient_a = sp.Poly(linear.coeff_monomial(eliminated), retained, domain=sp.QQ)
    coefficient_b = sp.Poly(linear.coeff_monomial(1), retained, domain=sp.QQ)
    linear_content = sp.gcd(coefficient_a, coefficient_b)
    coefficient_a = sp.exquo(coefficient_a, linear_content)
    coefficient_b = sp.exquo(coefficient_b, linear_content)
    resultant = sp.Poly(resultant_expression, retained, domain=sp.QQ)
    factors = [
        sp.Poly(factor, retained, domain=sp.QQ)
        for factor, _multiplicity in sp.factor_list(resultant.as_expr())[1]
        if sp.Poly(factor, retained, domain=sp.QQ).degree() == arguments.component_degree
    ]
    if len(factors) != 1:
        raise AssertionError("the requested resultant component was not unique")
    component = factors[0]
    coefficient_a = coefficient_a.rem(component)
    coefficient_b = coefficient_b.rem(component)
    emit(
        "normalized linear subresultant",
        started,
        contentDegree=linear_content.degree(),
        coefficientADegree=coefficient_a.degree(),
        coefficientBDegree=coefficient_b.degree(),
        coefficientAComponentGcdDegree=sp.gcd(coefficient_a, component).degree(),
        coefficientBComponentGcdDegree=sp.gcd(coefficient_b, component).degree(),
    )
    isolation = json.loads(arguments.isolation.read_text(encoding="utf-8"))
    intervals = [
        interval
        for factor in isolation["positiveFactors"]
        if factor["degree"] == arguments.component_degree
        for interval in factor["intervals"]
    ]
    pairs = []
    for index, record in enumerate(intervals, start=1):
        supplied_interval = record
        retained_interval = (
            parse_rational(record["lower"]),
            parse_rational(record["upper"]),
        )
        refinement_digits = int(isolation.get("isolationDigits", 24))
        while True:
            a_interval = polynomial_interval(coefficient_a, retained_interval)
            b_interval = polynomial_interval(coefficient_b, retained_interval)
            if not (a_interval[0] <= 0 <= a_interval[1]):
                paired_interval = interval_divide(
                    (-b_interval[1], -b_interval[0]),
                    a_interval,
                )
                sign = (
                    "positive"
                    if paired_interval[0] > 0
                    else "negative"
                    if paired_interval[1] < 0
                    else "unresolved"
                )
                if sign != "unresolved":
                    break
            next_digits = max(160, 2 * refinement_digits)
            if next_digits > arguments.max_refinement_digits:
                raise ArithmeticError(
                    "adaptive exact refinement did not resolve the paired-coordinate sign"
                )
            retained_interval = refine_root_interval(component, retained_interval, next_digits)
            refinement_digits = next_digits
            emit(
                "adaptively refined retained root",
                started,
                index=index,
                isolationDigits=refinement_digits,
            )
        pairs.append(
            {
                "index": index,
                "suppliedRetainedInterval": supplied_interval,
                "retainedInterval": serialize_interval(retained_interval),
                "retainedIsolationDigits": refinement_digits,
                "coefficientANonzero": True,
                "eliminatedInterval": serialize_interval(paired_interval),
                "eliminatedSign": sign,
            }
        )
        emit("paired isolated retained root", started, index=index, eliminatedSign=sign)
    result = {
        "schemaVersion": 1,
        "scope": "exact rational univariate representation on one resultant component",
        "proofStatus": "exact paired-coordinate sign on every supplied isolated component root",
        "face": arguments.face,
        "retainedVariable": str(retained),
        "eliminatedVariable": str(eliminated),
        "groundTypes": GROUND_TYPES,
        "componentDegree": component.degree(),
        "subresultantEliminatedDegrees": degrees,
        "linearRelation": {
            "removedContentDegree": linear_content.degree(),
            "coefficientA": serialize(coefficient_a),
            "coefficientB": serialize(coefficient_b),
        },
        "pairs": pairs,
        "wallSeconds": time.perf_counter() - started,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    emit("boundary rational univariate representation completed", started)


if __name__ == "__main__":
    main()
