#!/usr/bin/env python3
"""Independent reconstruction of the R0.71E formal figure data."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WAVENUMBERS = [1, 2, 4, 8, 16, 32, 64, 128]
THETAS = [0.25, 0.5, 1.0]


def close(first: float, second: float, tolerance: float = 4e-14) -> bool:
    return abs(first - second) <= tolerance * max(1.0, abs(first), abs(second))


with (ROOT / "data.csv").open(newline="", encoding="utf-8") as stream:
    rows = list(csv.DictReader(stream))

decomposition = [row for row in rows if row["kind"] == "decomposition"]
profile = [row for row in rows if row["kind"] == "profile"]
scaling = [row for row in rows if row["kind"] == "scaling"]
boxes = [row for row in rows if row["kind"] == "box"]

checks = {
    "rowCount": len(rows) == 522,
    "decompositionCount": len(decomposition) == 241,
    "profileCount": len(profile) == 241,
    "scalingCount": len(scaling) == len(WAVENUMBERS),
    "boxCount": len(boxes) == 4 * len(WAVENUMBERS),
    "decompositionReconstruction": all(
        close(float(row["stretch_norm"]), 2 * math.exp(-4 * float(row["tau"])))
        and close(
            float(row["commutator_norm"]),
            2 * (math.exp(-4 * float(row["tau"])) - math.exp(-2 * float(row["tau"]))),
        )
        and close(
            float(row["combined_norm"]),
            2 * (2 * math.exp(-4 * float(row["tau"])) - math.exp(-2 * float(row["tau"]))),
        )
        for row in decomposition
    ),
    "profileReconstruction": all(
        close(float(row["q_profile"]), math.exp(-2 * float(row["tau"])))
        and close(float(row["bulk_area"]), 0.5)
        for row in profile
    ),
    "profileBottomOne": close(float(profile[0]["q_profile"]), 1.0),
    "profileDisplayTailBelowThreePerMille": float(profile[-1]["q_profile"]) < 0.003,
    "scalingReconstruction": all(
        int(row["k"]) == wave
        and close(float(row["trace_ratio"]), 2 * wave**2)
        and close(float(row["trace_ratio_over_k2"]), 2.0)
        and close(float(row["bottom_coefficient"]), wave**2 / 8)
        and close(float(row["normalized_bulk"]), 1 / 16)
        for row, wave in zip(scaling, WAVENUMBERS)
    ),
    "finiteBoxReconstruction": all(
        close(
            float(row["finite_box"]),
            (1 - math.exp(-2 * float(row["theta"]))) / 16,
        )
        for row in boxes
        if row["theta"] != "inf"
    ),
    "infiniteBoxReconstruction": all(
        close(float(row["finite_box"]), 1 / 16)
        for row in boxes
        if row["theta"] == "inf"
    ),
    "allWavenumbersPresentForEveryHeight": all(
        sorted(int(row["k"]) for row in boxes if row["theta"] == label) == WAVENUMBERS
        for label in ["0.25", "0.5", "1", "inf"]
    ),
    "finiteBoxIndependentOfK": all(
        len({row["finite_box"] for row in boxes if row["theta"] == label}) == 1
        for label in ["0.25", "0.5", "1", "inf"]
    ),
    "combinedWorkStartsAtTwo": close(float(decomposition[0]["combined_norm"]), 2.0),
    "combinedWorkChangesSign": (
        any(float(row["combined_norm"]) > 0 for row in decomposition)
        and any(float(row["combined_norm"]) < 0 for row in decomposition)
    ),
}

if not all(checks.values()):
    raise AssertionError({key: value for key, value in checks.items() if not value})

payload = {
    "release": "R0.71E-independent-figure",
    "status": "pass",
    "method": "fresh CSV reconstruction without importing plot.py",
    "checks": checks,
    "claimBoundary": "Checks exact displayed formulas only; no PDE simulation, trace integrability, or general regularity claim.",
}
(ROOT / "independent-validation.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps(payload, indent=2, sort_keys=True))
