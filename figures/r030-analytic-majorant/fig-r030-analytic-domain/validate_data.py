#!/usr/bin/env python3
"""Cross-check the R0.30 figure data against its exact certificate."""

from __future__ import annotations

import csv
from fractions import Fraction
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
CERTIFICATE = REPOSITORY / "research/certificates/r030/edge-analytic-majorant.json"


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
    maximum_degree = payload["scope"]["maximumCheckedTotalDegree"]
    rows = list(csv.DictReader((PACKAGE / "kernel.csv").open(encoding="utf-8")))

    assert payload["git"]["dirty"] is False
    assert payload["git"]["commit"] == "641db99147d30f51bfc70c8881a70743f6bd063d"
    assert theorem["majorantConstant"] == 96
    assert theorem["analyticDomains"]["aUV"] == "max(|Z|,|W|)<1/96"
    assert theorem["analyticDomains"]["logarithmsAndPhi"] == "max(|Z|,|W|)<1/192"
    assert checks["aChargeSupport"]["passed"] is True
    assert checks["layerMajorants"]["passed"] is True
    assert checks["transportDivisibility"]["passed"] is True
    assert checks["layerMajorants"]["finiteMaximumH"]["exact"] == "8"
    assert checks["layerMajorants"]["finiteMaximumH"]["degree"] == 2
    assert len(rows) == maximum_degree - 1 == 118

    for degree, row in enumerate(rows, start=2):
        assert int(row["degree"]) == degree
        expected = convolution_constant(degree)
        assert Fraction(row["exact"]) == expected
        assert abs(float(row["decimal"]) - float(expected)) < 1e-14
        assert expected < 32

    degree_119 = payload["finiteLayerDiagnostics"][-1]
    assert degree_119["totalDegree"] == 119
    roots = {
        name: float(record["nthRoot"])
        for name, record in degree_119["fields"].items()
    }
    assert 1.15 < roots["a"] < 1.16
    assert 1.21 < roots["U"] < 1.22
    assert 1.21 < roots["V"] < 1.22
    print("validated 118 exact kernel rows and the R0.30 theorem contract")


if __name__ == "__main__":
    main()
