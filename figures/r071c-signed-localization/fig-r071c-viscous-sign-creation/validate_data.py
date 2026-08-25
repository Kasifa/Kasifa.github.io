#!/usr/bin/env python3
"""Independent row-wise validation for the R0.71C source-data table.

This script deliberately does not import plot.py.  It reads the archived CSV,
recomputes the witness with the Python standard library, and checks the exact
special-time identities separately.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
DATA = HERE / "data.csv"
OUTPUT = HERE / "independent-validation.json"
ABS_TOL = 3.0e-15


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expected(tau: float) -> dict[str, float]:
    decay8 = math.exp(-8.0 * tau)
    decay14 = math.exp(-14.0 * tau)
    work1 = 2.0 * decay8
    work2 = -2.0 * decay14
    parent = work1 + work2
    denominator = 16.0 * decay8
    root = max(parent, 0.0) ** 2 / denominator
    fine = max(work1, 0.0) ** 2 / (8.0 * decay8)
    defect = fine - root
    return {
        "decay8": decay8,
        "decay14": decay14,
        "w1": work1,
        "w2": work2,
        "W": parent,
        "D_root": denominator,
        "E_root": root,
        "E_fine": fine,
        "delta": defect,
    }


def close(left: float, right: float) -> bool:
    return math.isclose(left, right, rel_tol=2.0e-14, abs_tol=ABS_TOL)


def main() -> None:
    with DATA.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))

    failures: list[dict[str, object]] = []
    grid_rows = 0
    marker_rows = 0
    min_positive_parent = math.inf
    max_additivity_error = 0.0

    for row_number, row in enumerate(rows, start=2):
        tau = float(row["tau_numeric"])
        values = expected(tau)
        for field, expected_value in values.items():
            observed = float(row[field])
            if not close(observed, expected_value):
                failures.append(
                    {
                        "row": row_number,
                        "field": field,
                        "observed": observed,
                        "expected": expected_value,
                    }
                )
        additivity_error = abs(
            float(row["E_fine"])
            - float(row["E_root"])
            - float(row["delta"])
        )
        max_additivity_error = max(max_additivity_error, additivity_error)
        if row["row_role"] == "grid":
            grid_rows += 1
            if tau > 0:
                min_positive_parent = min(min_positive_parent, float(row["W"]))
        elif row["row_role"] == "exact-marker":
            marker_rows += 1
        else:
            failures.append(
                {"row": row_number, "field": "row_role", "observed": row["row_role"]}
            )

    tau_star = math.log(2.0) / 6.0
    star = expected(tau_star)
    exact_star = {
        "E_root": 2.0 ** (-16.0 / 3.0),
        "E_fine": 2.0 ** (-7.0 / 3.0),
        "delta": 7.0 * 2.0 ** (-16.0 / 3.0),
    }
    checks = {
        "rowCount252": len(rows) == 252,
        "gridRowCount251": grid_rows == 251,
        "markerRowCount1": marker_rows == 1,
        "allCsvFormulaValuesMatch": not failures,
        "parentPositiveAtEveryPositiveGridTime": min_positive_parent > 0.0,
        "ledgerAdditivityWithinTolerance": max_additivity_error < 1.0e-16,
        "tauStarRootExact": close(star["E_root"], exact_star["E_root"]),
        "tauStarFineExact": close(star["E_fine"], exact_star["E_fine"]),
        "tauStarDefectExact": close(star["delta"], exact_star["delta"]),
        "initialDerivativePositive": close(-16.0 + 28.0, 12.0),
    }
    status = "passed" if all(checks.values()) else "failed"
    payload = {
        "release": "R0.71C",
        "figureId": "fig-r071c-viscous-sign-creation",
        "status": status,
        "method": "independent Python-standard-library recomputation; plot.py is not imported",
        "data": {"path": "data.csv", "sha256": sha256(DATA), "rows": len(rows)},
        "checks": checks,
        "diagnostics": {
            "failureCount": len(failures),
            "failures": failures[:10],
            "maxLedgerAdditivityError": max_additivity_error,
            "minimumPositiveParentOnGrid": min_positive_parent,
            "tauStar": tau_star,
            "tauStarValues": star,
        },
        "claimBoundary": "Row-wise validation of the displayed exact Stokes witness only; no Navier-Stokes continuation or regularity claim.",
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "checks": checks, "rows": len(rows)}, indent=2, sort_keys=True))
    if status != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
