#!/usr/bin/env python3
"""Compare the independent R0.72N finite diagnostics."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any


FIELDS = (
    "maxMoment",
    "action",
    "liftedAction",
    "actionPoorRatio",
    "tOverV",
    "cubic",
)
TOLERANCES = {
    "maxMoment": 0.005,
    "action": 0.005,
    "liftedAction": 0.005,
    "actionPoorRatio": 0.005,
    "tOverV": 0.005,
    "cubic": 0.005,
}


def read_rows(path: Path) -> dict[float, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return {float(row["sigma"]): row for row in csv.DictReader(handle)}


def relative_error(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate-dir", type=Path, required=True)
    args = parser.parse_args()
    root = args.certificate_dir.resolve()
    producer = read_rows(root / "producer-dissipative.csv")
    independent = read_rows(root / "independent-dissipative.csv")
    if producer.keys() != independent.keys():
        raise RuntimeError("producer and independent sigma grids differ")

    comparisons: list[dict[str, Any]] = []
    maxima = {field: 0.0 for field in FIELDS}
    for sigma in sorted(producer):
        for field in FIELDS:
            left = float(producer[sigma][field])
            right = float(independent[sigma][field])
            error = relative_error(left, right)
            maxima[field] = max(maxima[field], error)
            comparisons.append(
                {
                    "sigma": sigma,
                    "field": field,
                    "producer": left,
                    "independent": right,
                    "relativeDifference": error,
                    "tolerance": TOLERANCES[field],
                    "passed": math.isfinite(error) and error <= TOLERANCES[field],
                }
            )

    checks = {
        "sameSigmaGrid": producer.keys() == independent.keys(),
        "allFiniteComparisonsPassed": all(row["passed"] for row in comparisons),
        "bothRespectMomentBarrier": all(
            float(rows[sigma]["maxMoment"])
            <= float(rows[sigma]["momentBarrier"]) * (1.0 + 2.0e-3)
            for rows in (producer, independent)
            for sigma in rows
        ),
        "bothShowPositiveAction": all(
            float(rows[sigma]["action"]) > 0.0
            for rows in (producer, independent)
            for sigma in rows
        ),
        "bothRemainBelowSqrtEnvelopeAtLastGridPoint": all(
            float(rows[max(rows)]["cubicOverSqrtSigma"]) < 0.2
            for rows in (producer, independent)
        ),
    }
    result = {
        "schemaVersion": 1,
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
        "maximumRelativeDifferences": maxima,
        "comparisons": comparisons,
        "limitations": (
            "Agreement is finite binary64 corroboration, not an analytic, "
            "interval, or full Navier--Stokes proof."
        ),
    }
    (root / "crosscheck.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))
    if result["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
