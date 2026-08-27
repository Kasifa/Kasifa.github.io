#!/usr/bin/env python3
"""Compare independently generated R0.72J producer and audit results."""

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def relative_error(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate-dir",
        type=Path,
        default=Path("research/certificates/r072j"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    producer_path = args.certificate_dir / "result.json"
    independent_path = args.certificate_dir / "independent-result.json"
    producer = json.loads(producer_path.read_text(encoding="utf-8"))
    independent = json.loads(independent_path.read_text(encoding="utf-8"))
    producer_rows = {int(row["R"]): row for row in producer["cases"]}
    independent_rows = {int(row["R"]): row for row in independent["cases"]}
    if set(producer_rows) != set(independent_rows):
        raise ValueError("producer and independent R grids differ")

    tolerances = {
        "criticalQ": 3.0e-5,
        "mixedRow": 2.0e-8,
        "deltaIntegralAbsHB": 2.0e-8,
        "rootH": 2.0e-7,
        "theta": 2.0e-12,
        "D": 2.0e-12,
        "normalizedTrueCubic": 3.0e-5,
        "normalizedMeasuredBvUpperProxy": 3.0e-5,
        "exactExposure": 2.0e-12,
        "uncorrectedB0Abs": 2.0e-12,
    }
    exact_keys = [
        "N",
        "orderedPositiveTriangles",
        "signedTriangles",
        "orderedPositiveFormula",
        "signedTriangleFormula",
        "cayleyGraphNonBipartite",
    ]
    cases: list[dict[str, Any]] = []
    for R in sorted(producer_rows):
        left = producer_rows[R]
        right = independent_rows[R]
        errors = {
            key: relative_error(float(left[key]), float(right[key]))
            for key in tolerances
        }
        exact_matches = {key: left[key] == right[key] for key in exact_keys}
        checks = {
            key: bool(math.isfinite(errors[key]) and errors[key] <= tolerance)
            for key, tolerance in tolerances.items()
        }
        checks.update(
            {f"exact:{key}": bool(value) for key, value in exact_matches.items()}
        )
        cases.append(
            {
                "R": R,
                "status": "passed" if all(checks.values()) else "failed",
                "relativeErrors": errors,
                "exactMatches": exact_matches,
                "checks": checks,
            }
        )
    maxima = {
        key: max(case["relativeErrors"][key] for case in cases)
        for key in tolerances
    }
    passed = (
        producer.get("status") == "passed"
        and independent.get("status") == "passed"
        and all(case["status"] == "passed" for case in cases)
    )
    result = {
        "schemaVersion": 1,
        "audit": "R0.72J producer-independent cross-check",
        "status": "passed" if passed else "failed",
        "generatedAt": utc_now(),
        "producerStatus": producer.get("status"),
        "independentStatus": independent.get("status"),
        "tolerances": tolerances,
        "maximumRelativeErrors": maxima,
        "cases": cases,
        "boundary": (
            "Both implementations construct one exact complex root.  This "
            "comparison is binary64 agreement, not an interval or complete-root certificate."
        ),
    }
    output_path = args.certificate_dir / "crosscheck.json"
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": result["status"],
                "cases": len(cases),
                "maximumRelativeErrors": maxima,
            },
            sort_keys=True,
        )
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
