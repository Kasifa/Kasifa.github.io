#!/usr/bin/env python3
"""Refine previously isolated exact roots without repeating root counting.

The input isolation file supplies rational brackets for the positive roots of
one resultant factor.  Each bracket already contains exactly one simple root;
``sympy.refine_root`` therefore only has to tighten those certified brackets.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from decimal import Decimal, localcontext
import json
from pathlib import Path
import sys
import time

import sympy as sp
from sympy.external.gmpy import GROUND_TYPES


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


def parse_rational(value: str) -> sp.Rational:
    numerator, denominator = value.split("/", 1)
    return sp.Rational(int(numerator), int(denominator))


def rational_string(value: sp.Rational) -> str:
    return f"{int(value.p)}/{int(value.q)}"


def decimal_string(value: sp.Rational, precision: int) -> str:
    with localcontext() as context:
        context.prec = precision
        return str(Decimal(int(value.p)) / Decimal(int(value.q)))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--isolation", type=Path, required=True)
    parser.add_argument("--component-degree", type=int, required=True)
    parser.add_argument("--digits", type=int, default=80)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    if arguments.digits < 1:
        raise ValueError("--digits must be positive")

    started = time.perf_counter()
    checkpoint = json.loads(arguments.checkpoint.read_text(encoding="utf-8"))
    variable = sp.symbols(checkpoint["keep"])
    resultant = sp.Poly(
        sp.Add(*(
            sp.Rational(int(row[1]), int(row[2])) * variable ** int(row[0])
            for row in checkpoint["exact"]
        )),
        variable,
        domain=sp.QQ,
    )
    factors = [
        sp.Poly(factor, variable, domain=sp.QQ)
        for factor, _multiplicity in sp.factor_list(resultant.as_expr())[1]
        if sp.Poly(factor, variable, domain=sp.QQ).degree() == arguments.component_degree
    ]
    if len(factors) != 1:
        raise AssertionError("the requested resultant component was not unique")
    component = factors[0]
    emit(
        "loaded exact resultant component",
        started,
        resultantDegree=resultant.degree(),
        componentDegree=component.degree(),
        groundTypes=GROUND_TYPES,
    )

    payload = json.loads(arguments.isolation.read_text(encoding="utf-8"))
    matching_records = [
        record
        for record in payload["positiveFactors"]
        if int(record["degree"]) == arguments.component_degree
    ]
    if len(matching_records) != 1:
        raise AssertionError("the isolation file did not contain one requested component")

    tolerance = sp.Rational(1, 10**arguments.digits)
    decimal_precision = arguments.digits + 15
    refined_intervals = []
    for index, record in enumerate(matching_records[0]["intervals"], start=1):
        lower = parse_rational(record["lower"])
        upper = parse_rational(record["upper"])
        refined_lower, refined_upper = sp.refine_root(
            component.as_expr(),
            lower,
            upper,
            eps=tolerance,
        )
        if not (lower <= refined_lower < refined_upper <= upper):
            raise AssertionError("refined interval escaped its certified parent bracket")
        midpoint = (refined_lower + refined_upper) / 2
        refined_intervals.append(
            {
                "lower": rational_string(refined_lower),
                "upper": rational_string(refined_upper),
                "lowerDecimal": decimal_string(refined_lower, decimal_precision),
                "upperDecimal": decimal_string(refined_upper, decimal_precision),
                "midpointDecimal": decimal_string(midpoint, decimal_precision),
                "multiplicity": int(record["multiplicity"]),
                "parentLower": record["lower"],
                "parentUpper": record["upper"],
            }
        )
        emit(
            "refined isolated root",
            started,
            index=index,
            bracketWidthExponent=arguments.digits,
        )

    matching_records[0]["intervals"] = refined_intervals
    result = {
        **payload,
        "isolationDigits": arguments.digits,
        "refinedFrom": str(arguments.isolation),
        "refinementMethod": "exact SymPy refine_root on a previously certified bracket",
        "groundTypes": GROUND_TYPES,
        "sympyVersion": sp.__version__,
        "wallSeconds": time.perf_counter() - started,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    emit("exact root-interval refinement completed", started)


if __name__ == "__main__":
    main()
