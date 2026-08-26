#!/usr/bin/env python3
"""Producer-side validation for the R0.71T figure table and raw runs."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--producer", type=Path, required=True)
    parser.add_argument("--independent", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = list(csv.DictReader(args.data.open(encoding="utf-8")))
    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    producer = json.loads(args.producer.read_text(encoding="utf-8"))
    independent = json.loads(args.independent.read_text(encoding="utf-8"))
    checks: list[dict[str, object]] = []

    def check(label: str, condition: bool, detail: object) -> None:
        if not condition:
            raise AssertionError(f"{label}: {detail}")
        checks.append({"label": label, "passed": True, "detail": detail})

    check("row count", len(rows) == metadata["rows"], len(rows))
    check("all four panels", {row["panel"] for row in rows} == {"A", "B", "C", "D"}, sorted({row["panel"] for row in rows}))
    check(
        "numerical classification",
        metadata["finiteGalerkin"] is True
        and metadata["pdeTimeStepping"] is True
        and metadata["dns"] is False,
        {key: metadata[key] for key in ("finiteGalerkin", "pdeTimeStepping", "dns")},
    )
    check(
        "primary configuration",
        producer["model"]["gridOrder"] == 10
        and producer["model"]["cutoff"] == 2
        and producer["model"]["targetRealDimension"] == 8,
        producer["model"],
    )
    refined = next(run for run in independent["runs"] if run["cutoff"] == 3)
    check(
        "independent refined configuration",
        refined["gridOrder"] == 12 and refined["cutoff"] == 3,
        {"N": refined["gridOrder"], "Kcut": refined["cutoff"]},
    )
    maximum_target = max(float(run["targetResidual"]) for run in producer["tauRuns"])
    check("all shot target residuals", maximum_target < 1e-12, maximum_target)
    check(
        "refined target residual",
        float(refined["targetResidual"]) < 1e-12,
        refined["targetResidual"],
    )

    primary_a = sorted(
        (float(row["x"]), float(row["y"]))
        for row in rows
        if row["panel"] == "A" and row["series"] == "primary precompensation ratio"
    )
    check("five tau values", [item[0] for item in primary_a] == [0.005, 0.01, 0.02, 0.04, 0.08], primary_a)
    deviations = [abs(value - 1.0) for _, value in primary_a]
    check(
        "precompensation approaches leading coefficient",
        deviations == sorted(deviations) and deviations[0] < 1e-5,
        deviations,
    )
    comparison = independent["comparisons"]
    check(
        "direct-convolution parity",
        comparison["sameTruncationPrecompensationDifference"] < 1e-10
        and comparison["sameTruncationAPlusDifference"] < 1e-10,
        comparison,
    )
    check(
        "refined truncation stability",
        comparison["refinedVsPrimaryPrecompensationDifference"] < 2e-4
        and comparison["refinedVsPrimaryAPlusDifference"] < 2e-4,
        comparison,
    )

    b_rows = [row for row in rows if row["panel"] == "B"]
    event = {
        row["series"]: float(row["y"])
        for row in b_rows if math.isclose(float(row["x"]), 1.0, abs_tol=1e-14)
    }
    check(
        "internal shell zero",
        abs(event["signed principal coefficient"]) < 1e-12
        and event["transverse target norm"] < 1e-12,
        event,
    )
    principal = sorted(
        (float(row["x"]), float(row["y"]))
        for row in b_rows if row["series"] == "signed principal coefficient"
    )
    check(
        "crossing is internal and signed",
        principal[0][1] < 0.0 and principal[-1][1] > 0.0,
        {"left": principal[0], "right": principal[-1]},
    )

    c_rows = [row for row in rows if row["panel"] == "C"]
    c_errors = []
    for tau in (0.005, 0.01, 0.02, 0.04, 0.08):
        group = {
            row["series"]: float(row["y"])
            for row in c_rows if math.isclose(float(row["x"]), tau, abs_tol=1e-14)
        }
        c_errors.append(abs(group["entry atom A+"] - group["slope-charge reconstruction"]))
    check("slope identity at every tau", max(c_errors) < 2e-15, c_errors)
    smallest_tau_atom = next(
        float(row["y"]) for row in c_rows
        if row["series"] == "entry atom A+" and math.isclose(float(row["x"]), 0.005)
    )
    check("entry atom approaches one quarter", abs(smallest_tau_atom - 0.25) < 0.003, smallest_tau_atom)

    d_rows = [row for row in rows if row["panel"] == "D"]
    slopes = {}
    for series, expected in (
        ("leading internal atom", -4.0),
        ("leading bare budget", -6.0),
        ("atom-to-budget ratio", 2.0),
    ):
        values = sorted(
            (float(row["x"]), float(row["y"]))
            for row in d_rows if row["series"] == series
        )
        observed = [
            math.log(second_y / first_y, 2.0) / math.log(second_x / first_x, 2.0)
            for (first_x, first_y), (second_x, second_y) in zip(values, values[1:])
        ]
        slopes[series] = observed
        check(f"exact {series} exponent", max(abs(value - expected) for value in observed) < 2e-13, observed)

    boundary = metadata["claimBoundary"]
    check(
        "claim boundary",
        "no continuum Galerkin error bound" in boundary
        and "DNS claim" in boundary
        and "regularity theorem" in boundary,
        boundary,
    )
    result = {
        "status": "passed",
        "checkCount": len(checks),
        "checks": checks,
    }
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
