#!/usr/bin/env python3
"""Standalone scalar recomputation for the R0.73B certificate.

No producer module is imported.  The script reads only the targeted CSV,
refits five decisive low-gap exponents, and evaluates the fixed-Lambda
triangular singular values by power iteration.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def exponent(rows: list[dict[str, str]], norm: str, p_value: float) -> float:
    subset = sorted((
        row for row in rows
        if row["norm"] == norm and float(row["p"]) == p_value
    ), key=lambda row: float(row["mu"]))[:4]
    if len(subset) != 4:
        raise AssertionError(f"missing rows for {norm}, p={p_value}")
    xs = [math.log(float(row["mu"])) for row in subset]
    ys = [math.log(float(row["gain"])) for row in subset]
    xm = sum(xs) / 4
    ym = sum(ys) / 4
    slope = sum((x - xm) * (y - ym) for x, y in zip(xs, ys)) / sum(
        (x - xm) ** 2 for x in xs
    )
    return max(0.0, -slope)


def triangular_gain(lam: float, end: float = 0.75) -> float:
    tau = end
    d1 = math.exp(-tau)
    d2 = math.exp(-4.0 * tau)
    z1 = lam * tau * math.exp(-end) / 4.0
    z2 = lam * tau * math.exp(-4.0 * end) / 4.0
    matrix = [
        [1.0, 0.0, 0.0, 0.0, 0.0],
        [z2, d2, 0.0, 0.0, 0.0],
        [z1, 0.0, d1, 0.0, 0.0],
        [-z1, 0.0, 0.0, d1, 0.0],
        [-z2, 0.0, 0.0, 0.0, d2],
    ]
    gram = [[sum(matrix[k][i] * matrix[k][j] for k in range(5))
             for j in range(5)] for i in range(5)]
    vector = [1.0, 0.25, -0.5, 0.75, -1.0]
    for _ in range(200):
        product = [sum(gram[i][j] * vector[j] for j in range(5))
                   for i in range(5)]
        length = math.sqrt(sum(value * value for value in product))
        vector = [value / length for value in product]
    rayleigh = sum(
        vector[i] * gram[i][j] * vector[j]
        for i in range(5) for j in range(5)
    )
    return math.sqrt(rayleigh)


def main() -> int:
    path = ROOT / "experiments/r073b/targeted_asymptotics.csv"
    with path.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    exponents = {
        "rawQFixedC": exponent(rows, "raw_q", 0.0),
        "rawQFixedLambda": exponent(rows, "raw_q", 0.5),
        "kineticFixedC": exponent(rows, "kinetic", 0.0),
        "kineticFixedLambda": exponent(rows, "kinetic", 0.5),
        "overweightFixedLambda": exponent(rows, "kinetic_over", 0.5),
    }
    expected = {
        "rawQFixedC": 1.0,
        "rawQFixedLambda": 0.5,
        "kineticFixedC": 0.5,
        "kineticFixedLambda": 0.0,
        "overweightFixedLambda": 0.25,
    }
    errors = {key: abs(exponents[key] - expected[key]) for key in expected}
    gains = {str(lam): triangular_gain(lam)
             for lam in (0.25, 1.0, 4.0, 16.0)}
    status = "passed" if max(errors.values()) <= 5e-3 else "failed"
    result = {
        "schemaVersion": 1,
        "status": status,
        "finiteDimensionalOnly": True,
        "source": "experiments/r073b/targeted_asymptotics.csv",
        "selectedObservedExponents": exponents,
        "selectedExpectedExponents": expected,
        "maximumSelectedExponentError": max(errors.values()),
        "fixedLambdaTriangularGains": gains,
        "method": "scalar least squares and 5x5 power iteration",
        "producerImported": False,
        "claimBoundary": {
            "finiteCsvRecomputed": True,
            "infiniteDimensionalLimitProved": False,
            "galerkinTailBoundProved": False,
        },
    }
    (HERE / "independent_recompute.json").write_text(
        canonical(result), encoding="utf-8"
    )
    print(canonical(result), end="")
    return 0 if status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
