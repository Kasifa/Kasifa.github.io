#!/usr/bin/env python3
"""Producer-side validation for the R0.71R figure table."""

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
    a0 = [row for row in rows if row["panel"] == "A" and math.isclose(float(row["x"]), 0.0)]
    a2 = [row for row in rows if row["panel"] == "A" and math.isclose(float(row["x"]), 2.0)]
    check("rho endpoints complete", len(a0) == 2 and len(a2) == 2, [len(a0), len(a2)])
    b64 = [row for row in rows if row["panel"] == "B" and row["N"] == "64"]
    gamma = float(next(row["y"] for row in b64 if row["series"] == "Gamma_2 jet surrogate"))
    law = float(next(row["y"] for row in b64 if row["series"] == "K squared law"))
    check("NSE Taylor-jet K squared law", math.isclose(gamma, law), {"jetSurrogate": gamma, "law": law})
    c = [row for row in rows if row["panel"] == "C"]
    check("even-touch entry remains one", all(float(row["y"]) == 1.0 for row in c if row["series"] == "positive entry"), len(c))
    d64 = [row for row in rows if row["panel"] == "D" and row["N"] == "64"]
    union_entry = float(next(row["y"] for row in d64 if row["series"] == "component-union entries"))
    union_source = float(next(row["y"] for row in d64 if row["series"] == "component source"))
    check("component union separated from source", union_entry == 64.0 and union_source < 3.0, {"entries": union_entry, "source": union_source})
    result = {"status": "passed", "checkCount": len(checks), "checks": checks}
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
