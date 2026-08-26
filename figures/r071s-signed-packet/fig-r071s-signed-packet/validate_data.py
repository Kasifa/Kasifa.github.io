#!/usr/bin/env python3
"""Producer-side validation for the R0.71S figure table."""

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
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = list(csv.DictReader(args.data.open(encoding="utf-8")))
    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    checks: list[dict[str, object]] = []

    def check(label: str, condition: bool, detail: object) -> None:
        if not condition:
            raise AssertionError(label)
        checks.append({"label": label, "passed": True, "detail": detail})

    check("row count matches metadata", len(rows) == metadata["rows"], len(rows))
    panels = {row["panel"] for row in rows}
    check("all four panels present", panels == {"A", "B", "C", "D"}, sorted(panels))

    for row in (item for item in rows if item["panel"] == "A"):
        k = float(row["x"])
        value = float(row["y"])
        expected = 8.0 * k * k if row["series"] == "critical H^-1 packet cost" else 8.0
        check(
            f"panel A {row['series']} K={k:g}",
            math.isclose(value, expected, rel_tol=2e-14),
            {"value": value, "expected": expected},
        )

    b_rows = [row for row in rows if row["panel"] == "B"]
    for overlap in sorted({float(row["x"]) for row in b_rows}):
        group = {
            row["series"]: float(row["y"])
            for row in b_rows if float(row["x"]) == overlap
        }
        check(
            f"panel B enclosure p={overlap:g}",
            group["exact Rayleigh lower"] <= group["largest eigenvalue"] <= group["exact row-sum upper"],
            group,
        )

    c_rows = [row for row in rows if row["panel"] == "C"]
    strong_values = [
        float(row["y"]) for row in c_rows
        if row["series"] == "strong L2 heat coefficient"
    ]
    check(
        "panel C strong coefficient constant",
        max(strong_values) - min(strong_values) < 2e-12,
        strong_values,
    )
    for row in c_rows:
        if row["series"] == "critical H^-1 heat cost":
            k = float(row["x"])
            strong = next(
                float(item["y"]) for item in c_rows
                if item["series"] == "strong L2 heat coefficient"
                and item["x"] == row["x"]
            )
            ratio = float(row["y"]) / strong
            check(
                f"panel C K squared ratio K={k:g}",
                math.isclose(ratio, k * k, rel_tol=2e-14),
                ratio,
            )

    d_rows = [row for row in rows if row["panel"] == "D"]
    for x in sorted({row["x"] for row in d_rows}, key=float):
        group = {
            row["series"]: float(row["y"])
            for row in d_rows if row["x"] == x
        }
        condition = (
            math.isclose(
                group["Jordan response"],
                2.0 * group["positive face response"],
                rel_tol=2e-14,
            )
            and group["signed precursor response"] == 0.0
            and group["zero-mean detector response"] == 0.0
        )
        check(f"panel D exact responses n={x}", condition, group)

    boundary = metadata["claimBoundary"]
    check(
        "claim boundary excludes positive-time NSE plot",
        "not plotted as a positive-time result" in boundary,
        boundary,
    )
    check(
        "panel D non-NSE boundary",
        "not an NSE trajectory" in boundary,
        boundary,
    )
    result = {"status": "passed", "checkCount": len(checks), "checks": checks}
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
