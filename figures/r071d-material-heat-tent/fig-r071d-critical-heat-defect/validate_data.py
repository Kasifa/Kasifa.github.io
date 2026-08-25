#!/usr/bin/env python3
"""Independent reconstruction of the R0.71D formal figure data."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RHO = 0.5
WAVENUMBERS = [1, 2, 4, 8, 16, 32, 64, 128]
THETAS = [0.25, 0.5, 1.0]


def close(first: float, second: float, tolerance: float = 3e-14) -> bool:
    return abs(first - second) <= tolerance * max(1.0, abs(first), abs(second))


with (ROOT / "data.csv").open(newline="", encoding="utf-8") as stream:
    rows = list(csv.DictReader(stream))

geometry = [row for row in rows if row["kind"] == "geometry"]
ledger = [row for row in rows if row["kind"] == "ledger"]
scaling = [row for row in rows if row["kind"] == "scaling"]
boxes = [row for row in rows if row["kind"] == "box"]

checks = {
    "rowCount": len(rows) == 274,
    "geometryCount": len(geometry) == 241,
    "ledgerCount": len(ledger) == 1,
    "scalingCount": len(scaling) == len(WAVENUMBERS),
    "boxCount": len(boxes) == len(WAVENUMBERS) * len(THETAS),
    "geometryReconstruction": all(
        close(float(row["phi_plus"]), (1 + RHO * math.cos(2 * float(row["z"]))) / 2)
        and close(float(row["phi_minus"]), (1 - RHO * math.cos(2 * float(row["z"]))) / 2)
        and close(float(row["omega_sq"]), math.cos(float(row["z"])) ** 2)
        for row in geometry
    ),
    "ledgerReconstruction": (
        close(float(ledger[0]["beta_plus_norm"]), -RHO / 2)
        and close(float(ledger[0]["beta_minus_norm"]), RHO / 2)
        and close(float(ledger[0]["parent_norm"]), 0)
        and close(float(ledger[0]["fine_defect_norm"]), RHO**2 / (2 + RHO))
    ),
    "criticalScalingReconstruction": all(
        int(row["k"]) == wave
        and close(float(row["critical_rate"]), wave**2 * RHO**2 / (2 + RHO))
        and close(float(row["critical_rate_over_k2"]), RHO**2 / (2 + RHO))
        for row, wave in zip(scaling, WAVENUMBERS)
    ),
    "boxReconstruction": all(
        close(
            float(row["box_cost"]),
            RHO**2 * (1 - math.exp(-2 * float(row["theta"]))) / (2 * (2 + RHO)),
        )
        and row["cauchy_ratio"] == "1"
        for row in boxes
    ),
    "parentCancellationExactInCsv": (
        float(ledger[0]["beta_plus_norm"]) + float(ledger[0]["beta_minus_norm"]) == 0
    ),
    "refinedLedgerStrictlyPositive": float(ledger[0]["fine_defect_norm"]) > 0,
    "allWavenumbersPresentForEveryTheta": all(
        sorted(int(row["k"]) for row in boxes if close(float(row["theta"]), theta)) == WAVENUMBERS
        for theta in THETAS
    ),
}

if not all(checks.values()):
    raise AssertionError({key: value for key, value in checks.items() if not value})

payload = {
    "release": "R0.71D-independent-figure",
    "status": "pass",
    "method": "fresh CSV reconstruction without importing plot.py",
    "checks": checks,
    "claimBoundary": "Checks exact displayed formulas only; no PDE simulation or general regularity claim.",
}
(ROOT / "independent-validation.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps(payload, indent=2, sort_keys=True))
