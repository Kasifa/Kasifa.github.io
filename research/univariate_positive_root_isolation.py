#!/usr/bin/env python3
"""Exactly isolate positive roots of factors in a saved resultant."""

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


def rational_string(value: sp.Rational) -> str:
    return f"{int(value.p)}/{int(value.q)}"


def decimal_string(value: sp.Rational, precision: int = 45) -> str:
    with localcontext() as context:
        context.prec = precision
        return str(Decimal(int(value.p)) / Decimal(int(value.q)))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--digits", type=int, default=24)
    parser.add_argument("--component-degree", type=int)
    parser.add_argument("--known-positive-count", type=int)
    arguments = parser.parse_args()
    if arguments.known_positive_count is not None and arguments.component_degree is None:
        raise ValueError("--known-positive-count requires --component-degree")
    started = time.perf_counter()
    payload = json.loads(arguments.checkpoint.read_text(encoding="utf-8"))
    variable = sp.symbols(payload["keep"])
    polynomial = sp.Poly(
        sp.Add(*(
            sp.Rational(int(row[1]), int(row[2])) * variable ** int(row[0])
            for row in payload["exact"]
        )),
        variable,
        domain=sp.QQ,
    )
    emit("loaded exact resultant", started, degree=polynomial.degree(), groundTypes=GROUND_TYPES)
    _unit, factors = sp.factor_list(polynomial.as_expr())
    tolerance = sp.Rational(1, 10**arguments.digits)
    records = []
    for factor_index, (factor, multiplicity) in enumerate(factors, start=1):
        item = sp.Poly(factor, variable, domain=sp.QQ)
        if arguments.component_degree is not None and item.degree() != arguments.component_degree:
            continue
        if arguments.known_positive_count is None:
            positive_count = int(item.count_roots(0, sp.oo))
            if item.eval(0) == 0:
                positive_count -= 1
        else:
            positive_count = arguments.known_positive_count
        if positive_count <= 0:
            continue
        emit(
            "isolating positive factor roots",
            started,
            factor=factor_index,
            degree=item.degree(),
            positiveRoots=positive_count,
        )
        intervals = item.intervals(
            eps=tolerance,
            inf=sp.Rational(0),
        )
        positive_intervals = []
        for (lower, upper), root_multiplicity in intervals:
            if upper <= 0:
                continue
            if lower < 0:
                raise AssertionError("a root interval crossed zero")
            midpoint = (lower + upper) / 2
            positive_intervals.append(
                {
                    "lower": rational_string(lower),
                    "upper": rational_string(upper),
                    "lowerDecimal": decimal_string(lower),
                    "upperDecimal": decimal_string(upper),
                    "midpointDecimal": decimal_string(midpoint),
                    "multiplicity": int(root_multiplicity),
                }
            )
        if len(positive_intervals) != positive_count:
            raise AssertionError("positive root isolation count mismatch")
        records.append(
            {
                "factorIndex": factor_index,
                "degree": item.degree(),
                "resultantMultiplicity": int(multiplicity),
                "positiveRootCount": positive_count,
                "intervals": positive_intervals,
            }
        )
        emit("positive factor roots isolated", started, factor=factor_index)
    result = {
        "schemaVersion": 1,
        "scope": "exact positive resultant-root isolation",
        "groundTypes": GROUND_TYPES,
        "sympyVersion": sp.__version__,
        "resultantDegree": polynomial.degree(),
        "isolationDomain": ["0", "infinity"],
        "requestedComponentDegree": arguments.component_degree,
        "assertedPositiveRootCount": arguments.known_positive_count,
        "isolationDigits": arguments.digits,
        "positiveFactors": records,
        "wallSeconds": time.perf_counter() - started,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    emit("positive resultant-root isolation completed", started)


if __name__ == "__main__":
    main()
