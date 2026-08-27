#!/usr/bin/env python3
"""Cross-check independent R0.72K producer and audit artifacts."""

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def relative_error(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--certificate-dir",
        type=Path,
        default=Path("research/certificates/r072k"),
    )
    return parser.parse_args()


def normalized_independent_row(row: dict[str, Any]) -> dict[str, float | int]:
    n_value = int(row["N"])
    n_squared = float(n_value**2)
    return {
        "R": int(row["R"]),
        "N": n_value,
        "firstRootPayment": float(row["firstRootPayment"]),
        "mixedRowMeasuredTwice": float(row["twiceMixedRow"]),
        "trueCubicMeasuredTwice": float(row["twiceTrueCubicRow"]),
        "directionalMeasuredUpper": float(row["measuredCompleteLedgerUpper"]),
        "directionalTheoremProxy": float(row["analyticCompleteLedgerProxy"]),
        "exactRootAtom": float(row["exactRootLower"]),
        "rootAtomOverN2": float(row["exactRootLower"]) / n_squared,
        "measuredUpperOverN2": (
            float(row["measuredCompleteLedgerUpper"]) / n_squared
        ),
        "theoremProxyOverN2": (
            float(row["analyticCompleteLedgerProxy"]) / n_squared
        ),
        "normalizedMeasuredCompleteUpper": float(
            row["normalizedMeasuredCompleteUpper"]
        ),
        "normalizedTheoremCompleteProxy": float(
            row["normalizedAnalyticCompleteProxy"]
        ),
    }


def main() -> int:
    args = parse_args()
    directory = args.certificate_dir.resolve()
    producer_path = directory / "result.json"
    independent_path = directory / "independent-result.json"
    producer = json.loads(producer_path.read_text(encoding="utf-8"))
    independent = json.loads(independent_path.read_text(encoding="utf-8"))

    producer_rows = {
        int(row["R"]): row for row in producer["commonBandCases"]
    }
    independent_rows = {
        int(row["R"]): normalized_independent_row(row)
        for row in independent["ledgerCases"]
    }
    if set(producer_rows) != set(independent_rows):
        raise ValueError("producer and independent R grids differ")

    tolerances = {
        "firstRootPayment": 2.0e-12,
        "mixedRowMeasuredTwice": 2.0e-8,
        "trueCubicMeasuredTwice": 2.0e-8,
        "directionalMeasuredUpper": 2.0e-8,
        "directionalTheoremProxy": 3.0e-5,
        "exactRootAtom": 2.0e-7,
        "rootAtomOverN2": 2.0e-7,
        "measuredUpperOverN2": 2.0e-8,
        "theoremProxyOverN2": 3.0e-5,
        "normalizedMeasuredCompleteUpper": 3.0e-5,
        "normalizedTheoremCompleteProxy": 3.0e-5,
    }
    cases: list[dict[str, Any]] = []
    for r_value in sorted(producer_rows):
        left = producer_rows[r_value]
        right = independent_rows[r_value]
        errors = {
            key: relative_error(float(left[key]), float(right[key]))
            for key in tolerances
        }
        checks = {
            key: bool(math.isfinite(errors[key]) and errors[key] <= tolerance)
            for key, tolerance in tolerances.items()
        }
        checks["N"] = int(left["N"]) == int(right["N"])
        cases.append(
            {
                "R": r_value,
                "status": "passed" if all(checks.values()) else "failed",
                "relativeErrors": errors,
                "checks": checks,
            }
        )

    producer_sharpness = {
        int(row["epsilonDenominator"]): float(row["theoremRatio"])
        for row in producer["sharpnessCases"]
        if int(row["epsilonNumerator"]) == 1
    }
    independent_sharpness = {
        int(row["n"]): float(row["sharpnessRatio"])
        for row in independent["sharpnessCases"]
    }
    shared_sharpness = sorted(set(producer_sharpness) & set(independent_sharpness))
    sharpness_errors = {
        str(n_value): relative_error(
            producer_sharpness[n_value], independent_sharpness[n_value]
        )
        for n_value in shared_sharpness
    }

    producer_scalar = {
        int(row["frequencyCount"]): float(row["theoremRatio"])
        for row in producer["complexCircleCases"]
    }
    independent_scalar = {
        int(row["frequency"]): float(row["inequalityRatio"])
        for row in independent["complexScalarCases"]
    }
    shared_scalar = sorted(set(producer_scalar) & set(independent_scalar))
    scalar_errors = {
        str(frequency): relative_error(
            producer_scalar[frequency], independent_scalar[frequency]
        )
        for frequency in shared_scalar
    }

    maxima = {
        key: max(case["relativeErrors"][key] for case in cases)
        for key in tolerances
    }
    auxiliary_checks = {
        "sharedSharpnessCases": len(shared_sharpness) >= 5,
        "sharedScalarCases": len(shared_scalar) >= 4,
        "sharpnessRatiosAgree": max(sharpness_errors.values()) <= 2.0e-12,
        "complexScalarRatiosAgree": max(scalar_errors.values()) <= 2.0e-12,
    }
    passed = (
        producer.get("status") == "passed"
        and independent.get("status") == "passed"
        and all(case["status"] == "passed" for case in cases)
        and all(auxiliary_checks.values())
    )
    result = {
        "schemaVersion": 1,
        "audit": "R0.72K producer-independent cross-check",
        "status": "passed" if passed else "failed",
        "generatedAt": utc_now(),
        "producerStatus": producer.get("status"),
        "independentStatus": independent.get("status"),
        "tolerances": tolerances,
        "maximumRelativeErrors": maxima,
        "auxiliaryChecks": auxiliary_checks,
        "sharpnessRelativeErrors": sharpness_errors,
        "complexScalarRelativeErrors": scalar_errors,
        "cases": cases,
        "boundary": (
            "This is a binary64 cross-route comparison of finite diagnostics "
            "and SHA-traced inherited ledgers. The analytic report, not this "
            "comparison, proves the root-sampling and common-band theorems."
        ),
    }
    output_path = directory / "crosscheck.json"
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": result["status"],
                "cases": len(cases),
                "maximumRelativeErrors": maxima,
                "auxiliaryChecks": auxiliary_checks,
            },
            sort_keys=True,
        )
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
