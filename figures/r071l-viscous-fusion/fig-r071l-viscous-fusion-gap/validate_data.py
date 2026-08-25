#!/usr/bin/env python3
"""Producer-side validation of the R0.71L figure data."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def require(condition, label, checks):
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
    grouped = {}
    for row in rows:
        grouped.setdefault((row["panel"], row["series"]), []).append(row)
    checks = {}
    expected = {
        ("A", "localizedLaplacian"): 321,
        ("A", "rawCollarContribution"): 321,
        ("A", "fusedViscous"): 321,
        ("B", "integratedCoefficient"): 6,
        ("C", "scalingExponent"): 5,
        ("D", "dependency"): 5,
    }
    require(set(grouped) == set(expected), "seriesSet", checks)
    for key, count in expected.items():
        require(len(grouped[key]) == count, f"count_{key[0]}_{key[1]}", checks)
    require(len(rows) == metadata["rows"], "metadataRowCount", checks)
    require(metadata["randomSeed"] is None, "deterministic", checks)
    require(metadata["dns"] is False, "notDNS", checks)
    require(metadata["pdeTimeStepping"] is False, "notPDETimeStepper", checks)
    require(metadata["fittedData"] is False, "notFitted", checks)
    a_rows = {key[1]: grouped[key] for key in grouped if key[0] == "A"}
    cancellation = max(
        abs(float(left["value"]) + float(right["value"]))
        for left, right in zip(a_rows["localizedLaplacian"], a_rows["rawCollarContribution"])
    )
    fused = max(abs(float(row["value"])) for row in a_rows["fusedViscous"])
    require(cancellation < 5.0e-15, "expandedRowsCancel", checks)
    require(fused < 5.0e-15, "fusedRowZero", checks)
    b = {row["category"]: float(row["value"]) for row in grouped[("B", "integratedCoefficient")]}
    tangent_residual = abs(b["heat tangent"] + b["raw collar"] - b["fused tangent"])
    joint_residual = abs(b["radial"] + b["fused tangent"] + b["normalization"] - b["joint source"])
    require(tangent_residual < 2.0e-14, "integratedTangentFusion", checks)
    require(joint_residual < 2.0e-14, "integratedJointFusion", checks)
    c = {row["category"]: float(row["value"]) for row in grouped[("C", "scalingExponent")]}
    require(c == {"local heat": -4.0, "positive creation": -2.0, "raw collar": -2.0, "fused tangent": -2.0, "joint source": -2.0}, "scalingLedger", checks)
    payload = {
        "release": "R0.71L",
        "status": "pass",
        "checks": checks,
        "metrics": {
            "rowCount": len(rows),
            "maximumExactCancellationResidual": cancellation,
            "maximumFusedProfile": fused,
            "integratedTangentFusionResidualScaled": tangent_residual,
            "integratedJointFusionResidualScaled": joint_residual,
        },
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
