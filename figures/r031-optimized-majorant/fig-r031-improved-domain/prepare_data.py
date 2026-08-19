#!/usr/bin/env python3
"""Extract the R0.31 exact kernel, analytic tail, and domain comparison."""

from __future__ import annotations

import csv
from fractions import Fraction
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
CERTIFICATE = REPOSITORY / "research/certificates/r031/edge-optimized-majorant.json"


def write_rows(path: Path, fieldnames: tuple[str, ...], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(
            target,
            fieldnames=fieldnames,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    records = payload["checks"]["kernelProof"]["finiteExactRange"]["records"]
    write_rows(
        PACKAGE / "kernel.csv",
        ("degree", "exact", "decimal"),
        [
            {
                "degree": record["totalDegree"],
                "exact": record["exact"],
                "decimal": record["decimal"],
            }
            for record in records
        ],
    )

    tail_rows: list[dict[str, object]] = []
    for degree in range(297, 801):
        bound = Fraction(10000, 2187) + Fraction(640, degree) + Fraction(
            1600, degree**2
        )
        tail_rows.append(
            {
                "degree": degree,
                "exact": str(bound),
                "decimal": format(float(bound), ".16g"),
            }
        )
    write_rows(
        PACKAGE / "tail-bound.csv",
        ("degree", "exact", "decimal"),
        tail_rows,
    )

    write_rows(
        PACKAGE / "domains.csv",
        ("quantity", "r030_exact", "r031_exact", "improvement_exact"),
        [
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
        ],
    )


if __name__ == "__main__":
    main()
