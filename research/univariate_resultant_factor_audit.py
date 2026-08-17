#!/usr/bin/env python3
"""Factor and count exact roots of a saved univariate resultant.

The input is one atomic checkpoint written by
``positive_region_boundary_resultants.py``.  This small audit is also used to
benchmark SymPy's Python-FLINT ground-domain backend against the pure-Python
domain before committing to long elimination runs.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
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
    factor_started = time.perf_counter()
    unit, factors = sp.factor_list(polynomial.as_expr())
    factor_seconds = time.perf_counter() - factor_started
    emit("factorization completed", started, factors=len(factors), factorSeconds=round(factor_seconds, 3))
    records = []
    for factor, multiplicity in factors:
        item = sp.Poly(factor, variable, domain=sp.QQ)
        root_started = time.perf_counter()
        positive = int(item.count_roots(0, sp.oo))
        root_seconds = time.perf_counter() - root_started
        records.append(
            {
                "degree": item.degree(),
                "multiplicity": int(multiplicity),
                "zeroRoot": bool(item.eval(0) == 0),
                "positiveRootCount": positive,
                "rootCountSeconds": root_seconds,
            }
        )
        emit(
            "factor root count completed",
            started,
            degree=item.degree(),
            multiplicity=int(multiplicity),
            positiveRoots=positive,
        )
    result = {
        "schemaVersion": 1,
        "scope": "univariate resultant factor and positive-root audit",
        "groundTypes": GROUND_TYPES,
        "sympyVersion": sp.__version__,
        "degree": polynomial.degree(),
        "unit": str(unit),
        "factorSeconds": factor_seconds,
        "factors": records,
        "wallSeconds": time.perf_counter() - started,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    emit("resultant factor audit completed", started)


if __name__ == "__main__":
    main()
