#!/usr/bin/env python3
"""Extract the R0.30 convolution-kernel table from the exact certificate."""

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
    maximum_degree = payload["scope"]["maximumCheckedTotalDegree"]
    with (PACKAGE / "kernel.csv").open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(
            target,
            fieldnames=("degree", "exact", "decimal"),
            lineterminator="\n",
        )
        writer.writeheader()
        for degree in range(2, maximum_degree + 1):
            value = convolution_constant(degree)
            writer.writerow(
                {
                    "degree": degree,
                    "exact": str(value),
                    "decimal": format(float(value), ".16g"),
                }
            )


if __name__ == "__main__":
    main()
