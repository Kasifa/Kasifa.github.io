#!/usr/bin/env python3
"""Producer-side validation for the R0.71O journal-figure data."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path


def require(condition: bool, label: str, checks: dict[str, bool]) -> None:
    checks[label] = bool(condition)
    if not condition:
        raise AssertionError(label)


def close(left: float, right: float, relative: float = 2.0e-12) -> bool:
    return abs(left - right) <= relative * max(abs(left), abs(right), 1.0)


def monotone(values: list[float], increasing: bool = True) -> bool:
    pairs = zip(values, values[1:])
    return all(a <= b + 2.0e-14 for a, b in pairs) if increasing else all(
        a + 2.0e-14 >= b for a, b in pairs
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("data.csv"))
    parser.add_argument(
        "--metadata", type=Path, default=Path("figure-data-metadata.json")
    )
    parser.add_argument("--output", type=Path, default=Path("validation.json"))
    args = parser.parse_args()
    with args.data.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault((row["panel"], row["series"]), []).append(row)

    checks: dict[str, bool] = {}
    expected_groups = {
        ("A", "softProfile"): 482,
        ("A", "faceAtom"): 4,
        ("B", "faceLedger"): 12,
        ("C", "softFaceTV"): 7,
        ("C", "denominatorMass"): 7,
        ("C", "CtSquareMass"): 7,
        ("D", "targetMode"): 4,
        ("D", "nseMetric"): 7,
        ("D", "claimBoundary"): 1,
    }
    require(set(grouped) == set(expected_groups), "seriesSet", checks)
    for key, count in expected_groups.items():
        require(len(grouped[key]) == count, f"count_{key[0]}_{key[1]}", checks)
    require(len(rows) == 531, "rowCount531", checks)
    require(metadata["rows"] == len(rows), "metadataRowCount", checks)
    require(metadata["release"] == "R0.71O", "release", checks)
    require(metadata["profileSampleCountPerCase"] == 241, "profileSamples", checks)
    require(
        metadata["frequencies"] == [1, 2, 4, 8, 16, 32, 64],
        "frequencyGrid",
        checks,
    )
    require(metadata["randomSeed"] is None, "deterministicRuntime", checks)
    require(metadata["dns"] is False, "notDNS", checks)
    require(metadata["pdeTimeStepping"] is False, "notTimeStepping", checks)
    require(metadata["fittedData"] is False, "notFitted", checks)
    require(metadata["intervalCertified"] is False, "notIntervalCertified", checks)
    require(
        metadata["independentMaximumProfileMassError"] < 2.0e-11,
        "independentProfileMass",
        checks,
    )
    require(
        metadata["independentMaximumVariationRelativeError"] < 2.0e-10,
        "independentVariation",
        checks,
    )
    require(
        metadata["independentNseMaximumResidual"] < 2.0e-12,
        "independentNseResidual",
        checks,
    )

    profiles: dict[str, list[tuple[float, float]]] = {}
    for row in grouped[("A", "softProfile")]:
        profiles.setdefault(row["case"], []).append(
            (float(row["x"]), float(row["value"]))
        )
    require(set(profiles) == {"odd m=1, b>0", "even m=2, b>0"}, "profileCases", checks)
    for case, pairs in profiles.items():
        pairs.sort()
        require(len(pairs) == 241, f"{case}_count", checks)
        require(close(pairs[0][0], -4.0) and close(pairs[-1][0], 4.0), f"{case}_domain", checks)
        zero = min(pairs, key=lambda pair: abs(pair[0]))
        require(close(zero[0], 0.0) and close(zero[1], 0.0), f"{case}_zero", checks)
    odd = dict(profiles["odd m=1, b>0"])
    even = dict(profiles["even m=2, b>0"])
    require(close(odd[-1.0], 0.0), "oddInactiveLeft", checks)
    require(close(odd[1.0], 0.5), "oddUnitProfile", checks)
    require(close(even[-1.0], 0.5) and close(even[1.0], 0.5), "evenUnitProfile", checks)
    odd_sorted = sorted(profiles["odd m=1, b>0"])
    even_sorted = sorted(profiles["even m=2, b>0"])
    require(all(close(value, 0.0) for x, value in odd_sorted if x < 0), "oddLeftZero", checks)
    require(monotone([value for x, value in odd_sorted if x >= 0]), "oddRightMonotone", checks)
    require(monotone([value for x, value in even_sorted if x <= 0], increasing=False), "evenLeftDip", checks)
    require(monotone([value for x, value in even_sorted if x >= 0]), "evenRightRise", checks)

    atoms = {
        (row["case"], row["component"]): float(row["value"])
        for row in grouped[("A", "faceAtom")]
    }
    require(atoms[("odd m=1, b>0", "positiveAtom")] == 1.0, "oddPositiveAtom", checks)
    require(atoms[("odd m=1, b>0", "negativeAtom")] == 0.0, "oddNegativeAtom", checks)
    require(atoms[("even m=2, b>0", "positiveAtom")] == 1.0, "evenPositiveAtom", checks)
    require(atoms[("even m=2, b>0", "negativeAtom")] == 1.0, "evenNegativeAtom", checks)

    ledger = {
        (row["case"], row["component"]): float(row["value"])
        for row in grouped[("B", "faceLedger")]
    }
    expected_ledger = {
        "odd m=1": {"Aplus": 1.0, "Aminus": 0.0, "signedAtom": 1.0, "hardBVJump": 1.0, "relaxedJordan": 1.0, "relaxationDefect": 0.0},
        "even m=2": {"Aplus": 1.0, "Aminus": 1.0, "signedAtom": 0.0, "hardBVJump": 0.0, "relaxedJordan": 2.0, "relaxationDefect": 2.0},
    }
    for case, expected in expected_ledger.items():
        for component, value in expected.items():
            require(close(ledger[(case, component)], value), f"ledger_{case}_{component}", checks)
        require(
            close(
                ledger[(case, "relaxedJordan")]
                - ledger[(case, "hardBVJump")],
                ledger[(case, "relaxationDefect")],
            ),
            f"ledgerDefectIdentity_{case}",
            checks,
        )

    panel_c = {
        series: {int(row["N"]): float(row["value"]) for row in grouped[("C", series)]}
        for series in ("softFaceTV", "denominatorMass", "CtSquareMass")
    }
    for frequency in metadata["frequencies"]:
        require(
            close(panel_c["softFaceTV"][frequency], 2.0 * frequency**3 / (frequency**2 + 1.0)),
            f"faceTV_N{frequency}",
            checks,
        )
        require(
            close(panel_c["denominatorMass"][frequency], math.pi / frequency**2),
            f"denominatorMass_N{frequency}",
            checks,
        )
        require(close(panel_c["CtSquareMass"][frequency], math.pi), f"CtMass_N{frequency}", checks)
    require(panel_c["softFaceTV"][64] > 120.0, "largeFaceTV", checks)
    require(panel_c["denominatorMass"][64] < 1.0e-3, "smallDenominatorMass", checks)
    require(
        all(
            "not NSE" in row["evidenceClass"]
            for series in ("softFaceTV", "denominatorMass", "CtSquareMass")
            for row in grouped[("C", series)]
        ),
        "abstractEvidenceVisible",
        checks,
    )

    modes = {(int(float(row["x"])), int(float(row["y"]))) for row in grouped[("D", "targetMode")]}
    require(modes == {(-1, -1), (-1, 1), (1, -1), (1, 1)}, "fourTargetModes", checks)
    require(all(close(float(row["value"]), 0.25) for row in grouped[("D", "targetMode")]), "modeMagnitudes", checks)
    metrics = {row["component"]: float(row["value"]) for row in grouped[("D", "nseMetric")]}
    require(
        metrics == {
            "targetModeCount": 4.0,
            "Y0": 1.0,
            "F2": 0.25,
            "G2": 0.5,
            "Ct2": 1.0,
            "Bt": 0.5,
            "rightTrace": 0.25,
        },
        "nseMetrics",
        checks,
    )
    boundary = grouped[("D", "claimBoundary")][0]["note"]
    require("one-sided local initial-jet" in boundary, "oneSidedBoundary", checks)
    require("does not produce arbitrarily many internal NSE faces" in boundary, "noInternalFaceCount", checks)
    require("abstract smooth Hilbert path" in metadata["claimBoundary"], "metadataAbstractBoundary", checks)
    require("No continuation" in metadata["claimBoundary"], "metadataRegularityBoundary", checks)

    payload = {
        "release": "R0.71O",
        "status": "pass",
        "checks": checks,
        "metrics": {
            "rowCount": len(rows),
            "producerCheckCount": len(checks),
            "maximumIndependentProfileMassError": metadata[
                "independentMaximumProfileMassError"
            ],
            "maximumIndependentVariationRelativeError": metadata[
                "independentMaximumVariationRelativeError"
            ],
            "independentNseMaximumResidual": metadata[
                "independentNseMaximumResidual"
            ],
            "N64SoftFaceTV": panel_c["softFaceTV"][64],
            "N64DenominatorMass": panel_c["denominatorMass"][64],
            "nseRightEntryTrace": metrics["rightTrace"],
        },
    }
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
