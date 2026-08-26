#!/usr/bin/env python3
"""Producer-side validation for the R0.71P journal-figure data."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path


def close(left: float, right: float, relative: float = 2.0e-12) -> bool:
    return abs(left - right) <= relative * max(abs(left), abs(right), 1.0)


def require(condition: bool, label: str, checks: dict[str, bool]) -> None:
    checks[label] = bool(condition)
    if not condition:
        raise AssertionError(label)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("data.csv"))
    parser.add_argument("--metadata", type=Path, default=Path("figure-data-metadata.json"))
    parser.add_argument("--output", type=Path, default=Path("validation.json"))
    args = parser.parse_args()

    with args.data.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault((row["panel"], row["series"]), []).append(row)

    checks: dict[str, bool] = {}
    expected = {
        ("A", "positiveAtomComparison"): 6,
        ("B", "cellLedger"): 6,
        ("B", "batchSummary"): 3,
        ("C", "hardEntryMass"): 7,
        ("C", "softEntryMass"): 7,
        ("C", "ordinaryTimeBudget"): 7,
        ("C", "CtSquareMass"): 7,
        ("C", "denominatorMass"): 7,
        ("D", "targetMode"): 4,
        ("D", "nseMetric"): 7,
        ("D", "claimBoundary"): 1,
    }
    require(set(grouped) == set(expected), "seriesSet", checks)
    for key, count in expected.items():
        require(len(grouped[key]) == count, f"count_{key[0]}_{key[1]}", checks)
    require(len(rows) == 62, "rowCount62", checks)
    require(metadata["rows"] == len(rows), "metadataRowCount", checks)
    require(metadata["release"] == "R0.71P", "release", checks)
    require(metadata["frequencies"] == [1, 2, 4, 8, 16, 32, 64], "frequencyGrid", checks)
    require(metadata["independentRandomSeed"] == 71071, "independentSeed", checks)
    require(metadata["independentTrialCount"] == 64, "independentTrials", checks)
    require(not metadata["dns"], "notDNS", checks)
    require(not metadata["pdeTimeStepping"], "notTimeStepping", checks)
    require(not metadata["fittedData"], "notFitted", checks)
    require(not metadata["intervalCertified"], "notIntervalCertified", checks)
    require(metadata["independentMaximumCellRatio"] <= 1.0 + 3e-14, "independentCellBound", checks)
    require(metadata["independentMaximumEntryToOverlapRatio"] <= 1.0 + 3e-14, "independentOverlapBound", checks)
    require(metadata["independentMaximumEntryCountError"] == 0.0, "independentEntryCount", checks)
    require(metadata["independentMaximumSoftRelativeError"] < 2e-10, "independentSoftMass", checks)
    require(metadata["independentNseMaximumResidual"] < 2e-13, "independentNse", checks)

    panel_a = {
        (row["case"], row["component"]): float(row["value"])
        for row in grouped[("A", "positiveAtomComparison")]
    }
    expected_a = {
        ("odd crossing m=1", "segmentedSoftEntry"): 1.0,
        ("odd crossing m=1", "ordinaryHardPositiveAtom"): 1.0,
        ("odd crossing m=1", "missingTouchMass"): 0.0,
        ("even touch m=2", "segmentedSoftEntry"): 1.0,
        ("even touch m=2", "ordinaryHardPositiveAtom"): 0.0,
        ("even touch m=2", "missingTouchMass"): 1.0,
    }
    require(set(panel_a) == set(expected_a), "panelAKeys", checks)
    for key, target in expected_a.items():
        require(close(panel_a[key], target), f"panelA_{key[0]}_{key[1]}", checks)

    cell = {
        (row["case"], row["component"]): float(row["value"])
        for row in grouped[("B", "cellLedger")]
    }
    expected_cell = {
        ("cell Q1", "entryAtom"): 0.9,
        ("cell Q1", "localSupportBudget"): 1.0,
        ("cell Q2", "entryAtom"): 0.0,
        ("cell Q2", "localSupportBudget"): 2.6,
        ("cell Q3", "entryAtom"): 4.9,
        ("cell Q3", "localSupportBudget"): 5.0,
    }
    require(set(cell) == set(expected_cell), "panelBCellKeys", checks)
    for key, target in expected_cell.items():
        require(close(cell[key], target), f"panelB_{key[0]}_{key[1]}", checks)
    summary = {
        row["component"]: float(row["value"])
        for row in grouped[("B", "batchSummary")]
    }
    require(close(summary["entrySum"], 5.8), "batchEntrySum", checks)
    require(close(summary["localEnergySum"], 8.6), "batchLocalSum", checks)
    require(close(summary["overlapGlobalBudget"], 12.0), "batchOverlapBudget", checks)
    require(summary["entrySum"] <= summary["localEnergySum"] <= summary["overlapGlobalBudget"], "batchChain", checks)

    frequencies = metadata["frequencies"]
    c_data = {
        series: {int(row["N"]): float(row["value"]) for row in grouped[("C", series)]}
        for series in ("hardEntryMass", "softEntryMass", "ordinaryTimeBudget", "CtSquareMass", "denominatorMass")
    }
    for frequency in frequencies:
        require(close(c_data["hardEntryMass"][frequency], frequency), f"hardN{frequency}", checks)
        require(close(c_data["softEntryMass"][frequency], frequency / (1 + frequency**-2)), f"softN{frequency}", checks)
        require(close(c_data["ordinaryTimeBudget"][frequency], 2 * math.pi), f"dtN{frequency}", checks)
        require(close(c_data["CtSquareMass"][frequency], math.pi), f"CtN{frequency}", checks)
        require(close(c_data["denominatorMass"][frequency], math.pi / frequency**2), f"dN{frequency}", checks)
    require(c_data["hardEntryMass"][64] == 64.0, "entryGrowth", checks)
    require(c_data["denominatorMass"][64] < 1e-3, "denominatorDecay", checks)

    modes = {(float(row["x"]), float(row["y"])) for row in grouped[("D", "targetMode")]}
    require(modes == {(-1.0, -1.0), (-1.0, 1.0), (1.0, -1.0), (1.0, 1.0)}, "fourModes", checks)
    nse = {row["component"]: float(row["value"]) for row in grouped[("D", "nseMetric")]}
    targets = {"Y0": 1.0, "F2": 0.25, "c2": 1.0, "pairing": 0.5, "entryAtom": 0.25, "projectionBudget": 0.25, "sharpnessRatio": 1.0}
    require(set(nse) == set(targets), "nseMetricSet", checks)
    for key, target in targets.items():
        require(close(nse[key], target), f"nse_{key}", checks)
    boundary = grouped[("D", "claimBoundary")][0]["note"]
    require("initial jet" in boundary.lower(), "initialJetBoundary", checks)
    require("repeated" in boundary.lower(), "noRepeatedBoundary", checks)
    c_evidence = {row["evidenceClass"] for row in rows if row["panel"] == "C"}
    require(len(c_evidence) == 1 and "not NSE" in next(iter(c_evidence)), "abstractNotNSE", checks)
    require("not a coupled NSE" in metadata["claimBoundary"], "metadataAbstractBoundary", checks)

    payload = {
        "release": "R0.71P",
        "status": "passed",
        "checkCount": len(checks),
        "checks": checks,
        "rowCount": len(rows),
        "method": "independent formula reconstruction against certificate-backed CSV rows",
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
