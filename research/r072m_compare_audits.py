#!/usr/bin/env python3
"""Cross-check the two independent R0.72M finite audit routes."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any


def read_rows(path: Path, key: str) -> dict[float, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return {float(row[key]): row for row in csv.DictReader(handle)}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def relative_error(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def compare_table(
    directory: Path,
    stem: str,
    key: str,
    fields: tuple[str, ...],
) -> list[dict[str, Any]]:
    producer = read_rows(directory / f"producer-{stem}.csv", key)
    independent = read_rows(directory / f"independent-{stem}.csv", key)
    if producer.keys() != independent.keys():
        raise ValueError(f"case keys differ for {stem}")
    rows: list[dict[str, Any]] = []
    for case in sorted(producer):
        for field in fields:
            left = float(producer[case][field])
            right = float(independent[case][field])
            rows.append(
                {
                    "table": stem,
                    "case": case,
                    "field": field,
                    "producer": left,
                    "independent": right,
                    "relativeDifference": relative_error(left, right),
                }
            )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate-dir", type=Path, required=True)
    args = parser.parse_args()
    directory = args.certificate_dir.resolve()

    producer_result = read_json(directory / "result.json")
    independent_result = read_json(directory / "independent-result.json")
    comparisons: list[dict[str, Any]] = []
    comparisons.extend(
        compare_table(
            directory,
            "bessel",
            "s",
            ("mass", "gradientMoment", "expectedGradientMoment"),
        )
    )
    comparisons.extend(
        compare_table(directory, "action", "sigma", ("action", "scaledAction"))
    )
    comparisons.extend(
        compare_table(
            directory,
            "frozen-cubic",
            "sigma",
            ("cubic", "cubicOverLogSigma", "asymptoticConstant"),
        )
    )
    comparisons.extend(
        compare_table(
            directory,
            "dissipative",
            "sigma",
            ("cubic", "cubicOverLogSigma", "finalNormSquared"),
        )
    )

    maxima: dict[str, float] = {}
    field_maxima: dict[str, float] = {}
    for row in comparisons:
        maxima[row["table"]] = max(
            maxima.get(row["table"], 0.0), float(row["relativeDifference"])
        )
        field_key = f"{row['table']}:{row['field']}"
        field_maxima[field_key] = max(
            field_maxima.get(field_key, 0.0), float(row["relativeDifference"])
        )
    checks = {
        "producerPassed": producer_result.get("status") == "passed",
        "independentPassed": independent_result.get("status") == "passed",
        "besselAgreement": maxima.get("bessel", math.inf) < 5.0e-10,
        "actionAgreement": maxima.get("action", math.inf) < 1.0e-3,
        "frozenCubicAgreement": maxima.get("frozen-cubic", math.inf) < 5.0e-5,
        "dissipativeCubicAgreement": field_maxima.get("dissipative:cubic", math.inf) < 2.0e-3
        and field_maxima.get("dissipative:cubicOverLogSigma", math.inf) < 2.0e-3,
        "dissipativeNormAgreement": field_maxima.get("dissipative:finalNormSquared", math.inf) < 1.2e-2,
        "constantAgreement": relative_error(
            float(producer_result["asymptoticCubicConstant"]),
            float(independent_result["asymptoticCubicConstant"]),
        )
        < 1.0e-15,
    }
    output = {
        "schemaVersion": 1,
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
        "maximumRelativeDifferences": maxima,
        "maximumRelativeDifferencesByField": field_maxima,
        "comparisons": comparisons,
        "limitations": "Agreement of two finite binary64 routes is corroboration, not an analytic or interval proof.",
    }
    (directory / "crosscheck.json").write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2))
    if output["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
