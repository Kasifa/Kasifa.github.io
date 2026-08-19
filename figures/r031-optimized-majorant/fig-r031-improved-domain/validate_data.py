#!/usr/bin/env python3
"""Cross-check the R0.31 figure data against the exact certificate."""

from __future__ import annotations

import csv
from fractions import Fraction
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
CERTIFICATE = REPOSITORY / "research/certificates/r031/edge-optimized-majorant.json"


def rows(path: str) -> list[dict[str, str]]:
    with (PACKAGE / path).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def convolution_constant(degree: int) -> Fraction:
    return degree**3 * sum(
        (
            Fraction(
                min(left_degree, degree - left_degree),
                left_degree**3 * (degree - left_degree) ** 3,
            )
            for left_degree in range(1, degree)
        ),
        Fraction(0),
    )


def main() -> None:
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    theorem = payload["formalTheorem"]
    checks = payload["checks"]
    kernel = rows("kernel.csv")
    tail = rows("tail-bound.csv")
    domains = rows("domains.csv")

    assert payload["git"] == {
        "commit": "dfdf19ae3706d376deae02b9ff804060bf37d626",
        "dirty": False,
    }
    assert theorem["majorantConstant"] == "K=81/4"
    assert theorem["commonAnalyticDomain"] == "max(|Z|,|W|)<4/81"
    assert checks["kernelProof"]["passed"] is True
    assert checks["aChargeSupport"]["passed"] is True
    assert checks["improvedLayerMajorants"]["passed"] is True
    assert checks["transportDivisibility"]["passed"] is True

    assert len(kernel) == 295
    for degree, row in enumerate(kernel, start=2):
        assert int(row["degree"]) == degree
        expected = convolution_constant(degree)
        assert Fraction(row["exact"]) == expected
        assert abs(float(row["decimal"]) - float(expected)) < 1e-14
        if degree == 2:
            assert expected == 8
        else:
            assert expected <= Fraction(27, 4)

    assert len(tail) == 504
    previous: Fraction | None = None
    for degree, row in enumerate(tail, start=297):
        assert int(row["degree"]) == degree
        expected = Fraction(10000, 2187) + Fraction(640, degree) + Fraction(
            1600, degree**2
        )
        value = Fraction(row["exact"])
        assert value == expected
        assert value < Fraction(27, 4)
        assert previous is None or value < previous
        previous = value

    assert domains == [
        {
            "quantity": "a,U,V",
            "r030_exact": "1/96",
            "r031_exact": "4/81",
            "improvement_exact": "128/27",
        },
        {
            "quantity": "logs,phi,factorization",
            "r030_exact": "1/192",
            "r031_exact": "4/81",
            "improvement_exact": "256/27",
        },
    ]

    degree_119 = payload["finiteLayerDiagnostics"][-1]
    assert degree_119["totalDegree"] == 119
    roots = {
        name: float(record["nthRoot"])
        for name, record in degree_119["fields"].items()
    }
    assert 1.15 < roots["a"] < 1.16
    assert 1.21 < roots["U"] < 1.22
    assert 1.21 < roots["V"] < 1.22
    print("validated 295 exact kernel rows, 504 analytic-tail rows, and the R0.31 theorem contract")


if __name__ == "__main__":
    main()
