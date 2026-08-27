#!/usr/bin/env python3
"""Cross-check the independent R0.72L producer and audit artifacts."""

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
        default=Path("research/certificates/r072l"),
    )
    return parser.parse_args()


def indexed(rows: list[dict[str, Any]], keys: tuple[str, ...]) -> dict[tuple[Any, ...], dict[str, Any]]:
    return {tuple(row[key] for key in keys): row for row in rows}


def compare_rows(
    producer_rows: list[dict[str, Any]],
    independent_rows: list[dict[str, Any]],
    index_keys: tuple[str, ...],
    value_tolerances: dict[str, float],
) -> tuple[list[dict[str, Any]], dict[str, float]]:
    left = indexed(producer_rows, index_keys)
    right = indexed(independent_rows, index_keys)
    if set(left) != set(right):
        raise ValueError(f"row grids differ for keys {index_keys}")
    cases: list[dict[str, Any]] = []
    maxima = {key: 0.0 for key in value_tolerances}
    for index in sorted(left):
        errors = {
            key: relative_error(float(left[index][key]), float(right[index][key]))
            for key in value_tolerances
        }
        checks = {
            key: math.isfinite(errors[key]) and errors[key] <= tolerance
            for key, tolerance in value_tolerances.items()
        }
        for key, value in errors.items():
            maxima[key] = max(maxima[key], value)
        cases.append(
            {
                "index": list(index),
                "status": "passed" if all(checks.values()) else "failed",
                "relativeErrors": errors,
                "checks": checks,
            }
        )
    return cases, maxima


def main() -> int:
    args = parse_args()
    directory = args.certificate_dir.resolve()
    producer = json.loads((directory / "result.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (directory / "independent-result.json").read_text(encoding="utf-8")
    )

    algebra_tolerances = {"L2Bound": 3.0e-14, "L4Bound": 3.0e-14, "Z": 3.0e-14}
    local_tolerances = {
        "epsilon": 3.0e-14,
        "closureScale": 3.0e-14,
        "tau": 3.0e-14,
        "ZNormalizedConstantOne": 3.0e-14,
        "rawLedgerAtSample": 3.0e-14,
        "L4AtKZero": 3.0e-14,
    }
    closure_tolerances = {
        "epsilon": 3.0e-14,
        "closureScale": 3.0e-14,
        "epsilonOverClosureScale": 3.0e-14,
        "normalizedLedgerProxy": 3.0e-14,
    }
    galerkin_tolerances = {
        "rootCountPrediction": 3.0e-14,
        "GRootMass": 1.0e-4,
        "CubicRow": 5.0e-6,
        "MixedRow": 1.0e-6,
        "AR": 3.0e-14,
        "BR": 3.0e-14,
    }
    algebra_cases, algebra_maxima = compare_rows(
        producer["optimizationCases"],
        independent["algebraCases"],
        ("R", "p", "epsilon", "K"),
        algebra_tolerances,
    )
    local_cases, local_maxima = compare_rows(
        producer["localFloorCases"],
        independent["localFloorCases"],
        ("R", "p"),
        local_tolerances,
    )
    closure_cases, closure_maxima = compare_rows(
        producer["closureCases"],
        independent["closureCases"],
        ("R", "p"),
        closure_tolerances,
    )
    galerkin_cases, galerkin_maxima = compare_rows(
        producer["galerkinCases"],
        independent["galerkinCases"],
        ("R", "sigma"),
        galerkin_tolerances,
    )

    producer_galerkin = indexed(producer["galerkinCases"], ("R", "sigma"))
    independent_galerkin = indexed(independent["galerkinCases"], ("R", "sigma"))
    root_counts_agree = all(
        int(producer_galerkin[key]["rootCount"])
        == int(independent_galerkin[key]["rootCount"])
        for key in producer_galerkin
    )
    producer_support = producer["fullSupportAudit"]
    independent_support = independent["fullSupportAudit"]
    support_errors = {
        key: relative_error(float(producer_support[key]), float(independent_support[key]))
        for key in ["insideNormW2e0", "outsideNormW2e0", "outsideOverInside"]
    }
    auxiliary_checks = {
        "producerPassed": producer.get("status") == "passed",
        "independentPassed": independent.get("status") == "passed",
        "producerExactExponentChecksPassed": all(
            producer["exponentAudit"]["checks"].values()
        ),
        "algebraCasesAgree": all(case["status"] == "passed" for case in algebra_cases),
        "localFloorCasesAgree": all(case["status"] == "passed" for case in local_cases),
        "closureCasesAgree": all(case["status"] == "passed" for case in closure_cases),
        "galerkinCasesAgree": all(case["status"] == "passed" for case in galerkin_cases),
        "galerkinRootCountsAgree": root_counts_agree,
        "leakageValuesAgree": max(support_errors.values()) <= 3.0e-15,
        "bothRoutesDeclareFiniteBoundary": bool(producer.get("limitations"))
        and bool(independent.get("limitations")),
    }
    passed = all(auxiliary_checks.values())
    result = {
        "schemaVersion": 1,
        "audit": "R0.72L producer-independent cross-check",
        "status": "passed" if passed else "failed",
        "generatedAt": utc_now(),
        "producerStatus": producer.get("status"),
        "independentStatus": independent.get("status"),
        "tolerances": {
            "algebra": algebra_tolerances,
            "localFloor": local_tolerances,
            "closure": closure_tolerances,
            "galerkin": galerkin_tolerances,
        },
        "maximumRelativeErrors": {
            "algebra": algebra_maxima,
            "localFloor": local_maxima,
            "closure": closure_maxima,
            "galerkin": galerkin_maxima,
            "fullSupport": support_errors,
        },
        "auxiliaryChecks": auxiliary_checks,
        "algebraCases": algebra_cases,
        "localFloorCases": local_cases,
        "closureCases": closure_cases,
        "galerkinCases": galerkin_cases,
        "boundary": (
            "This cross-route comparison covers finite normalized-algebra "
            "samples and binary64 Galerkin diagnostics. The analytic report, "
            "not this file, proves L.1--L.5 and the no-finite-support theorem. "
            "The projected ODE is not an invariant full-lattice model and no "
            "general Navier--Stokes regularity conclusion is asserted."
        ),
    }
    (directory / "crosscheck.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": result["status"],
                "algebraCases": len(algebra_cases),
                "localFloorCases": len(local_cases),
                "closureCases": len(closure_cases),
                "galerkinCases": len(galerkin_cases),
                "maximumRelativeErrors": result["maximumRelativeErrors"],
                "auxiliaryChecks": auxiliary_checks,
            },
            sort_keys=True,
        )
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
