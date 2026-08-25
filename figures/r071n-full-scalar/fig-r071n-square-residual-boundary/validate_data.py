#!/usr/bin/env python3
"""Producer-side validation for the R0.71N journal-figure data."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


EXPECTED = {
    "seed 49": {
        "P": 5023.642509952941,
        "R": 749.9219442938775,
        "J": 1.352354294391183,
        "z": 0.0037338304858202916,
    },
    "seed 5": {
        "P": 5167.69457947911,
        "R": -25941.29401331811,
        "J": -7.371344134519265,
        "z": 0.0019598744198175808,
    },
}


def require(condition, label, checks):
    checks[label] = bool(condition)
    if not condition:
        raise AssertionError(label)


def close(left, right, relative=2.0e-12):
    return abs(left - right) <= relative * max(abs(left), abs(right), 1.0)


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
    grouped = {}
    for row in rows:
        grouped.setdefault((row["panel"], row["series"]), []).append(row)
    checks = {}
    expected_groups = {
        ("A", "structureFlow"): 4,
        ("B", "positiveSquare"): 2,
        ("B", "signedResidual"): 2,
        ("B", "numeratorTotal"): 2,
        ("B", "normalizerRoot"): 2,
        ("C", "z"): 2,
        ("C", "J"): 2,
        ("D", "scalingExponent"): 4,
        ("D", "nextGate"): 1,
    }
    require(set(grouped) == set(expected_groups), "seriesSet", checks)
    for key, count in expected_groups.items():
        require(len(grouped[key]) == count, f"count_{key[0]}_{key[1]}", checks)
    require(len(rows) == 21, "rowCount21", checks)
    require(metadata["rows"] == len(rows), "metadataRowCount", checks)
    require(metadata["release"] == "R0.71N", "release", checks)
    require(metadata["selectedGridOrder"] == 64, "selectedGridOrder", checks)
    require(metadata["gridOrders"] == [48, 64, 80], "threeGridOrders", checks)
    require(metadata["randomSeed"] is None, "deterministicRuntime", checks)
    require(metadata["dns"] is False, "notDNS", checks)
    require(metadata["pdeTimeStepping"] is False, "notTimeStepping", checks)
    require(metadata["fittedData"] is False, "notFitted", checks)
    require(metadata["intervalCertified"] is False, "notIntervalTheorem", checks)
    require(
        metadata["resolutionMaximumRelativeResidual"] < 2.0e-10,
        "resolutionAgreement",
        checks,
    )

    by_series_witness = {
        (row["series"], row["witness"]): float(row["value"])
        for row in rows if row["witness"]
    }
    for witness, values in EXPECTED.items():
        p_square = by_series_witness[("positiveSquare", witness)]
        residual = by_series_witness[("signedResidual", witness)]
        total = by_series_witness[("numeratorTotal", witness)]
        root = by_series_witness[("normalizerRoot", witness)]
        z_value = by_series_witness[("z", witness)]
        j_value = by_series_witness[("J", witness)]
        require(close(p_square, values["P"]), f"{witness}_P", checks)
        require(close(residual, values["R"]), f"{witness}_R", checks)
        require(close(z_value, values["z"]), f"{witness}_z", checks)
        require(close(j_value, values["J"]), f"{witness}_J", checks)
        require(close(total, p_square + residual), f"{witness}_sum", checks)
        require(close(j_value, total / root), f"{witness}_normalizedJ", checks)
        require(p_square > 0.0, f"{witness}_positiveSquare", checks)
        require(z_value > 0.0, f"{witness}_positiveZ", checks)
        require(
            metadata["witnesses"][witness]["maxJRepresentationRelativeResidual"]
            < 2.0e-10,
            f"{witness}_JRepresentationResidual",
            checks,
        )
        require(
            metadata["witnesses"][witness]["squareCancellationRelativeResidual"]
            < 2.0e-10,
            f"{witness}_squareCancellationResidual",
            checks,
        )
    require(by_series_witness[("J", "seed 49")] > 0, "positiveJ", checks)
    require(by_series_witness[("J", "seed 5")] < 0, "negativeJ", checks)
    require(
        by_series_witness[("signedResidual", "seed 49")] > 0,
        "positiveResidualSeed49",
        checks,
    )
    require(
        by_series_witness[("signedResidual", "seed 5")] < 0,
        "negativeResidualSeed5",
        checks,
    )

    stage_rows = sorted(grouped[("A", "structureFlow")], key=lambda row: float(row["x"]))
    require(
        [row["stage"] for row in stage_rows]
        == [
            "complete derivative",
            "square plus residual",
            "local enstrophy substitution",
            "signed second jet",
        ],
        "structuralStageOrder",
        checks,
    )
    require(
        all(row["evidenceClass"] == "exact fixed-cell theorem" for row in stage_rows),
        "panelAExactEvidence",
        checks,
    )

    scaling = {
        row["component"]: float(row["value"])
        for row in grouped[("D", "scalingExponent")]
    }
    require(
        scaling
        == {"numerator": 5.0, "root": 2.0, "J": 3.0, "weighted creation": 0.0},
        "scalingExponents",
        checks,
    )
    require(close(scaling["numerator"] - scaling["root"], scaling["J"]), "JScalingDifference", checks)
    gate = grouped[("D", "nextGate")][0]
    require(gate["stage"] == "R0.71O face gate", "nextGateLabel", checks)
    require("no face estimate" in gate["note"], "faceClaimBoundary", checks)
    require(
        all(
            "not interval theorem" in row["evidenceClass"]
            for key in (("B", "positiveSquare"), ("B", "signedResidual"), ("C", "z"), ("C", "J"))
            for row in grouped[key]
        ),
        "diagnosticEvidenceLabels",
        checks,
    )

    payload = {
        "release": "R0.71N",
        "status": "pass",
        "checks": checks,
        "metrics": {
            "rowCount": len(rows),
            "producerCheckCount": len(checks),
            "resolutionMaximumRelativeResidual": metadata[
                "resolutionMaximumRelativeResidual"
            ],
            "seed49NumeratorTotal": by_series_witness[("numeratorTotal", "seed 49")],
            "seed5NumeratorTotal": by_series_witness[("numeratorTotal", "seed 5")],
        },
    }
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
