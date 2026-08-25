#!/usr/bin/env python3
"""Validate the archived R0.71G figure data and exact reference columns."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np


EXPECTED_SIGN_EXITS = {
    1.0: 0.4335008669647834,
    0.5: 0.8937395113568223,
    0.2: 2.3347686381614055,
    0.1: 4.798940447595622,
    0.05: 9.77625005813992,
}


def require(condition: bool, label: str, checks: dict[str, bool]):
    checks[label] = bool(condition)
    if not condition:
        raise AssertionError(label)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("data.csv"))
    parser.add_argument(
        "--metadata", type=Path, default=Path("figure-data-metadata.json")
    )
    parser.add_argument("--output", type=Path, default=Path("validation.json"))
    args = parser.parse_args()
    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    with args.data.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        for key in ("mu", "theta", "value", "aux"):
            row[key] = float(row[key])

    checks: dict[str, bool] = {}
    require(metadata["release"] == "R0.71G", "release", checks)
    require(metadata["rows"] == len(rows) == 5292, "rowCount", checks)
    require(metadata["randomSeed"] is None, "deterministic", checks)
    require(metadata["dns"] is False, "notDNS", checks)
    require(metadata["pdeTimeStepping"] is False, "reducedChain", checks)
    require(metadata["chain"]["radius"] == 24, "chainRadius", checks)
    require(metadata["chain"]["step"] == 0.00025, "timeStep", checks)

    profiles = [row for row in rows if row["recordType"] == "profile"]
    sign_rows = [row for row in rows if row["recordType"] == "signExit"]
    q_rows = [row for row in rows if row["recordType"] == "qExit"]
    functional = [row for row in rows if row["recordType"] == "functional"]
    require(len(profiles) == 5260, "profileRows", checks)
    require(len(sign_rows) == 5, "signEventRows", checks)
    require(len(q_rows) == 15, "relativeEventRows", checks)
    require(len(functional) == 12, "functionalRows", checks)

    maximum_initial_error = 0.0
    maximum_rescaling_error = 0.0
    for mu in EXPECTED_SIGN_EXITS:
        initial = [
            row
            for row in profiles
            if np.isclose(row["mu"], mu) and np.isclose(row["theta"], 0.0)
        ]
        require(len(initial) == 2, f"initialRowsMu{mu}", checks)
        h_initial = next(row for row in initial if row["level"] == "H")
        q_initial = next(row for row in initial if row["level"] == "qRelative")
        maximum_initial_error = max(
            maximum_initial_error,
            abs(h_initial["value"] - 1.0),
            abs(h_initial["aux"] - 1.0),
            abs(q_initial["value"] - 1.0),
        )
        selected_h = [
            row
            for row in profiles
            if np.isclose(row["mu"], mu) and row["level"] == "H"
        ]
        for row in selected_h:
            maximum_rescaling_error = max(
                maximum_rescaling_error,
                abs(row["aux"] - np.exp(4.0 * row["theta"]) * row["value"]),
            )
    require(maximum_initial_error < 1.0e-14, "initialNormalization", checks)
    require(maximum_rescaling_error < 2.0e-12, "rescaledHColumn", checks)

    maximum_sign_error = 0.0
    observed_exits = {}
    for row in sign_rows:
        mu = row["mu"]
        observed_exits[mu] = row["theta"]
        maximum_sign_error = max(
            maximum_sign_error, abs(row["theta"] - EXPECTED_SIGN_EXITS[mu])
        )
        require(abs(row["aux"] - 1.0 / mu) < 1.0e-14, f"inverseMu{mu}", checks)
    require(maximum_sign_error < 2.0e-6, "signExitAgreement", checks)
    ordered = [observed_exits[mu] for mu in (1.0, 0.5, 0.2, 0.1, 0.05)]
    require(all(first < second for first, second in zip(ordered, ordered[1:])), "signExitMonotoneCheckedSequence", checks)

    maximum_exact_limit_error = 0.0
    for row in q_rows:
        level = float(row["level"])
        maximum_exact_limit_error = max(
            maximum_exact_limit_error, abs(row["aux"] + np.log(level) / 6.0)
        )
        require(row["theta"] < observed_exits[row["mu"]], f"relativeBeforeSignMu{row['mu']}Level{level}", checks)
    require(maximum_exact_limit_error < 1.0e-14, "exactWeakLimitColumn", checks)

    maximum_functional_error = 0.0
    for row in functional:
        n = int(round(row["theta"]))
        maximum_functional_error = max(
            maximum_functional_error,
            abs(row["value"] - n),
            abs(row["aux"] - (4.0**n - 1.0) / (3.0 * 4.0**n)),
        )
    require(maximum_functional_error < 1.0e-14, "functionalExactColumns", checks)
    require(functional[-1]["value"] == 12.0, "unweightedGrowth", checks)
    require(functional[-1]["aux"] < 1.0 / 3.0, "weightedBound", checks)

    boundary = metadata["chain"]["maximumOuterTwoModeMass"]
    require(max(float(value) for value in boundary.values()) < 1.0e-80, "outerModeMass", checks)

    payload = {
        "release": "R0.71G",
        "status": "pass",
        "checks": checks,
        "metrics": {
            "maximumInitialError": maximum_initial_error,
            "maximumRescaledHError": maximum_rescaling_error,
            "maximumSignExitDifferenceFromAdaptiveAudit": maximum_sign_error,
            "maximumExactLimitColumnError": maximum_exact_limit_error,
            "maximumFunctionalColumnError": maximum_functional_error,
        },
        "claimBoundary": (
            "Validates finite reduced-chain data and exact plotted columns only; it is not a PDE simulation or a general residence theorem."
        ),
    }
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
