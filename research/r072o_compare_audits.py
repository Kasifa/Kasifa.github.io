#!/usr/bin/env python3
"""Compare the independent R0.72O exact and finite audits."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any


SCREEN_FIELDS = (
    "p",
    "epsilon",
    "LR",
    "LRepsilon",
    "ZExact",
    "oldDirectNormalized",
    "edDirectNormalized",
    "edOverOld",
    "predictedWindowRatio",
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def relative_error(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate-dir", type=Path, required=True)
    args = parser.parse_args()
    root = args.certificate_dir.resolve()
    producer_result = read_json(root / "producer-result.json")
    independent_result = read_json(root / "independent-result.json")
    producer_exp = read_json(root / "producer-exponents.json")
    independent_exp = read_json(root / "independent-exponents.json")
    producer_deg = read_csv(root / "producer-degeneracy.csv")
    independent_deg = read_csv(root / "independent-degeneracy.csv")
    producer_screen = read_csv(root / "producer-window.csv")
    independent_screen = read_csv(root / "independent-window.csv")

    if len(producer_screen) != len(independent_screen):
        raise RuntimeError("window grids have different lengths")
    if len(producer_deg) != len(independent_deg):
        raise RuntimeError("degeneracy grids have different lengths")

    comparisons: list[dict[str, Any]] = []
    maximum = {field: 0.0 for field in SCREEN_FIELDS}
    for left, right in zip(producer_screen, independent_screen, strict=True):
        key_left = (left["R"], left["regime"], left["level"])
        key_right = (right["R"], right["regime"], right["level"])
        if key_left != key_right:
            raise RuntimeError(f"window grid mismatch: {key_left} != {key_right}")
        for field in SCREEN_FIELDS:
            error = relative_error(float(left[field]), float(right[field]))
            maximum[field] = max(maximum[field], error)
            comparisons.append(
                {
                    "R": int(left["R"]),
                    "regime": left["regime"],
                    "level": float(left["level"]),
                    "field": field,
                    "producer": float(left[field]),
                    "independent": float(right[field]),
                    "relativeDifference": error,
                    "tolerance": 2.0e-12,
                    "passed": math.isfinite(error) and error <= 2.0e-12,
                }
            )

    degeneracy_equal = all(
        all(
            (
                left[key].lower() == right[key].lower()
                if key == "passed"
                else left[key] == right[key]
            )
            for key in (
                "R",
                "secondCarrierCoefficient",
                "firstDerivativeAtZero",
                "secondDerivativeAtZero",
                "thirdDerivativeAtZero",
                "expectedThirdDerivative",
                "passed",
            )
        )
        for left, right in zip(producer_deg, independent_deg, strict=True)
    )
    exact_equal = producer_exp == independent_exp
    checks = {
        "producerPassed": producer_result["status"] == "passed",
        "independentPassed": independent_result["status"] == "passed",
        "exactExponentLedgersIdentical": exact_equal,
        "degeneracyTablesIdentical": degeneracy_equal,
        "screenGridsAgree": all(row["passed"] for row in comparisons),
        "generalPConclusionRemainsConditional": (
            producer_result["checks"]["generalPResultMarkedConditional"]
            and independent_result["checks"]["generalPResultMarkedConditional"]
        ),
    }
    result = {
        "schemaVersion": 1,
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
        "maximumRelativeDifferences": maximum,
        "comparisons": comparisons,
        "limitations": (
            "Agreement audits exact exponent bookkeeping and deterministic "
            "screen values. It does not replace the analytic semigroup theorem "
            "or prove unconditional multi-carrier enhanced dissipation."
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
