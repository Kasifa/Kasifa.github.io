#!/usr/bin/env python3
"""Audit the weighted exceptional systems at the two R0.20 x-boundaries.

The compact stationary system has degenerate real boundary components
``x=0, p=2`` and ``x=infinity, q=3``.  This script performs the weighted
changes

    x = s^2,     p = 2 + s y,
    x = s^(-9),  q = 3 + s y,

and extracts the exact lowest powers of ``s``.  On both principal weighted
charts the third stationary equation has a sign-definite exceptional leading
form, so the exceptional divisor contains no common stationary zero.

This is the algebraic core of the boundary-layer exclusion.  Explicit strip
widths and the complementary projective charts remain separate tasks.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import sys
import time

import sympy as sp


P, Q, X = sp.symbols("p q x")
S, Y = sp.symbols("s y")
VARIABLES = (P, Q, X)
SYSTEM_NAMES = (
    "saturated_stationary_p",
    "saturated_stationary_q",
    "saturated_stationary_x",
)


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


def leading_form(source: sp.Poly, variable_order: tuple[sp.Symbol, ...]) -> tuple[int, sp.Poly]:
    valuation = min(powers[0] for powers, _coefficient in source.terms())
    expression = sp.Add(*(
        coefficient
        * sp.prod(
            variable_order[index - 1] ** powers[index]
            for index in range(1, len(powers))
        )
        for powers, coefficient in source.terms()
        if powers[0] == valuation
    ))
    return valuation, sp.Poly(expression, *variable_order, domain=sp.QQ)


def digest(source: sp.Poly) -> str:
    text = "\n".join(
        f"{','.join(map(str, powers))}:{coefficient}"
        for powers, coefficient in source.terms()
    )
    return hashlib.sha256(text.encode("ascii")).hexdigest()


def polynomial_record(source: sp.Poly) -> dict[str, object]:
    return {
        "variables": [str(variable) for variable in source.gens],
        "degrees": [source.degree(variable) for variable in source.gens],
        "termCount": len(source.terms()),
        "exactDigest": digest(source),
        "exactTerms": [
            [*map(int, powers), str(int(coefficient.p)), str(int(coefficient.q))]
            for powers, coefficient in source.terms()
        ],
    }


def zero_chart(functions: list[sp.Poly]) -> dict[str, object]:
    records = []
    leading = []
    if len(functions) != len(SYSTEM_NAMES):
        raise ValueError("unexpected stationary-system length")
    for name, function in zip(SYSTEM_NAMES, functions):
        transformed = sp.Poly(
            sp.expand(function.as_expr().subs({P: 2 + S * Y, X: S**2})),
            S,
            Y,
            Q,
            domain=sp.QQ,
        )
        valuation, form = leading_form(transformed, (Y, Q))
        leading.append(form)
        records.append({"equation": name, "sValuation": valuation, "leadingForm": polynomial_record(form)})

    third = leading[2]
    unit, factors = sp.factor_list(third.as_expr())
    nontrivial = [
        (sp.Poly(factor, Y, Q, domain=sp.QQ), multiplicity)
        for factor, multiplicity in factors
        if sp.Poly(factor, Y, Q, domain=sp.QQ).total_degree() > 2
    ]
    if len(nontrivial) != 1:
        raise AssertionError("the x=0 exceptional third form did not have the expected factorization")
    positive_factor, multiplicity = nontrivial[0]
    if multiplicity != 1 or unit >= 0:
        raise AssertionError("the x=0 exceptional sign was not negative")
    as_y = sp.Poly(positive_factor.as_expr(), Y)
    if as_y.degree() != 2 or as_y.coeff_monomial(Y) != 0:
        raise AssertionError("the x=0 positive factor was not quadratic in y^2")
    y2 = sp.Poly(as_y.coeff_monomial(Y**2), Q, domain=sp.QQ)
    y0 = sp.Poly(as_y.coeff_monomial(1), Q, domain=sp.QQ)
    if any(coefficient <= 0 for coefficient in y2.coeffs() + y0.coeffs()):
        raise AssertionError("the x=0 exceptional factor was not coefficient-positive")
    return {
        "boundaryComponent": "x=0, p=2",
        "weightedMap": {"x": "s^2", "p": "2+s*y"},
        "equations": records,
        "thirdEquationSign": "strictly negative for q>=0 and real y",
        "signCertificate": {
            "overallUnit": str(unit),
            "positiveFactorMultiplicity": multiplicity,
            "ySquaredCoefficient": polynomial_record(y2),
            "constantInY": polynomial_record(y0),
            "allNonzeroCoefficientsStrictlyPositive": True,
        },
        "exceptionalCommonZero": False,
    }


def infinity_chart(functions: list[sp.Poly]) -> dict[str, object]:
    records = []
    leading = []
    if len(functions) != len(SYSTEM_NAMES):
        raise ValueError("unexpected stationary-system length")
    for name, function in zip(SYSTEM_NAMES, functions):
        x_degree = function.degree(X)
        compact_expression = sp.Add(*(
            coefficient
            * P ** powers[0]
            * Q ** powers[1]
            * S ** (9 * (x_degree - powers[2]))
            for powers, coefficient in function.terms()
        ))
        transformed = sp.Poly(
            sp.expand(compact_expression.subs(Q, 3 + S * Y)),
            S,
            Y,
            P,
            domain=sp.QQ,
        )
        valuation, form = leading_form(transformed, (Y, P))
        leading.append(form)
        records.append({"equation": name, "sValuation": valuation, "leadingForm": polynomial_record(form)})

    third = leading[2]
    unit, factors = sp.factor_list(third.as_expr())
    quadratic_factors = [
        sp.Poly(factor, P, domain=sp.QQ)
        for factor, multiplicity in factors
        if multiplicity == 1 and sp.Poly(factor, Y, P, domain=sp.QQ).degree(P) == 2
    ]
    if len(quadratic_factors) != 1 or unit <= 0:
        raise AssertionError("the x=infinity exceptional third form was not positive quadratic type")
    quadratic = quadratic_factors[0]
    discriminant = sp.discriminant(quadratic.as_expr(), P)
    if quadratic.LC() <= 0 or discriminant >= 0:
        raise AssertionError("the x=infinity exceptional quadratic was not strictly positive")
    return {
        "boundaryComponent": "x=infinity, q=3",
        "weightedMap": {"x": "s^-9", "q": "3+s*y"},
        "equations": records,
        "thirdEquationSign": "strictly positive for real p and real y",
        "signCertificate": {
            "overallUnit": str(unit),
            "quadratic": polynomial_record(quadratic),
            "leadingCoefficient": str(quadratic.LC()),
            "discriminant": str(discriminant),
            "discriminantStrictlyNegative": True,
        },
        "exceptionalCommonZero": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    started = time.perf_counter()
    cache = load_cache(arguments.cache)
    functions = [parse_polynomial(cache["polynomials"][name]) for name in SYSTEM_NAMES]
    emit("loaded exact saturated stationary system", started)
    zero = zero_chart(functions)
    emit("audited weighted x=0 chart", started)
    infinity = infinity_chart(functions)
    emit("audited weighted x=infinity chart", started)
    result = {
        "schemaVersion": 1,
        "scope": "weighted exceptional-divisor audit at both compact x-boundaries",
        "proofStatus": (
            "the third stationary equation is sign-definite on both principal "
            "weighted exceptional divisors; explicit strip widths and complementary charts pending"
        ),
        "zeroChart": zero,
        "infinityChart": infinity,
        "wallSeconds": time.perf_counter() - started,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    emit("boundary blow-up audit completed", started)


if __name__ == "__main__":
    main()
