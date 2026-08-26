#!/usr/bin/env python3
"""Producer-side validation for the R0.71Q figure table."""

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
    check("all four panels present", {row["panel"] for row in rows} == {"A", "B", "C", "D"}, sorted({row["panel"] for row in rows}))

    b64 = [row for row in rows if row["panel"] == "B" and row["N"] == "64"]
    check("N=64 Blaschke series complete", len(b64) == 3, [row["series"] for row in b64])
    bound = float(next(row["y"] for row in b64 if row["series"] == "Jensen bound"))
    check("N=64 Jensen near sharp", 64.0 <= bound < 65.5, bound)

    c64 = [row for row in rows if row["panel"] == "C" and row["N"] == "64"]
    union = float(next(row["y"] for row in c64 if row["series"] == "distinct union"))
    summed = float(next(row["y"] for row in c64 if row["series"] == "summed capacity"))
    check("component union grows", union == 64.0 and summed > union, {"union": union, "summed": summed})

    d64 = [row for row in rows if row["panel"] == "D" and row["N"] == "64"]
    windows = float(next(row["y"] for row in d64 if row["series"] == "owned windows"))
    growth = float(next(row["y"] for row in d64 if row["series"] == "relative complex growth"))
    check("cover tax separated from local growth", windows == 64.0 and math.isclose(growth, math.cosh(3 * math.pi / 4) ** 2), {"windows": windows, "growth": growth})

    result = {"status": "passed", "checkCount": len(checks), "checks": checks}
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
