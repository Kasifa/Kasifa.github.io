#!/usr/bin/env python3
"""Independently validate an R0.73I finite diagnostic package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import sys
from typing import Mapping


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
EVIDENCE_CLASS = "finite-binary64-galerkin-diagnostic-only"

ACTION_FIELDS = (
    "schemaVersion", "evidenceClass", "diagnosticOnly", "smokeMode",
    "windowId", "endpoint", "endpointExpression", "endpointRole", "N",
    "quadratureOrder", "finiteAction", "finiteAverageRate",
    "finiteWkbCorrection", "berryIntegral", "viscousIntegral",
    "edgeAtZeroReal", "edgeAtEndpointReal", "minimumNodeRealGap",
    "minimumNodeComplexSeparation", "maximumNodeEigenCondition",
    "maximumNodeEigenResidualRelative", "maximumDerivativeResidualRelative",
)

GAIN_FIELDS = (
    "schemaVersion", "evidenceClass", "diagnosticOnly", "smokeMode",
    "gridKind", "windowId", "endpoint", "endpointRole", "N", "Lambda",
    "epsilon", "integrator", "fastStep", "stepCount", "logSelectedGain",
    "LambdaInverseLogGain", "finiteAction", "finiteAverageRate",
    "finiteWkbCorrection", "residualLogGainMinusLambdaAction",
    "residualMinusWkb", "topClusterDimension", "topEigenvalueReal",
    "topEigenvalueImag", "topRealGap", "topComplexSeparation",
    "topEigenCondition", "topEigenResidualRelative", "wallTimeSeconds",
)

COMPARISON_FIELDS = (
    "schemaVersion", "evidenceClass", "diagnosticOnly", "smokeMode",
    "kind", "windowId", "leftLabel", "rightLabel", "absoluteDifference",
    "tolerance", "passCheck", "diagnosticInterpretation",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, required=True)
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path, fields: tuple[str, ...]) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or ()) != fields:
            raise ValueError(f"unexpected CSV header in {path.name}")
        rows = list(reader)
    if not rows:
        raise ValueError(f"empty CSV: {path.name}")
    if any(set(row) != set(fields) for row in rows):
        raise ValueError(f"CSV row keys changed: {path.name}")
    return rows


def finite(row: Mapping[str, str], key: str) -> float:
    value = float(row[key])
    if not math.isfinite(value):
        raise ValueError(f"nonfinite {key}")
    return value


def integer(row: Mapping[str, str], key: str) -> int:
    value = int(row[key])
    return value


def strict_bool(value: str) -> bool:
    if value == "true":
        return True
    if value == "false":
        return False
    raise ValueError(f"invalid strict boolean: {value}")


def close(left: float, right: float, absolute: float = 2.0e-13) -> bool:
    return abs(left - right) <= absolute * max(1.0, abs(left), abs(right))


def endpoint(expression: str) -> float:
    values = {
        "1e-4": 1.0e-4,
        "sqrt(19/180)/392": math.sqrt(19.0 / 180.0) / 392.0,
        "1/450": 1.0 / 450.0,
    }
    if expression not in values:
        raise ValueError(f"unknown endpoint expression: {expression}")
    return values[expression]


def binding_valid(row: Mapping[str, object], base: Path) -> bool:
    path = base / str(row["path"])
    return (
        path.is_file()
        and path.stat().st_size == int(row["bytes"])
        and sha256(path) == row["sha256"]
    )


def main() -> int:
    directory = ARGS.directory.resolve()
    required = {
        "action_rows.csv", "gain_rows.csv", "comparison_rows.csv",
        "environment.json", "summary.json", "manifest.json",
        "progress.ndjson", "SHA256SUMS",
    }
    missing = sorted(name for name in required if not (directory / name).is_file())
    if missing:
        raise RuntimeError(f"missing generated files: {missing}")

    summary = load_json(directory / "summary.json")
    manifest = load_json(directory / "manifest.json")
    environment = load_json(directory / "environment.json")
    schema = load_json(HERE / "summary.schema.json")
    if not all(isinstance(value, dict) for value in (summary, manifest, environment, schema)):
        raise RuntimeError("JSON roots must be objects")

    action_rows = read_csv(directory / "action_rows.csv", ACTION_FIELDS)
    gain_rows = read_csv(directory / "gain_rows.csv", GAIN_FIELDS)
    comparison_rows = read_csv(directory / "comparison_rows.csv", COMPARISON_FIELDS)

    summary_keys = set(summary)
    required_summary = set(schema["required"])
    allowed_summary = set(schema["properties"])
    summary_shape = required_summary <= summary_keys <= allowed_summary
    schema_header = (
        summary.get("schemaVersion") == "r073i-finite-summary-v1"
        and summary.get("release") == "R0.73I-finite-diagnostic"
        and summary.get("evidenceClass") == EVIDENCE_CLASS
        and summary.get("diagnosticOnly") is True
    )
    configuration = summary.get("configuration", {})
    action_spec = configuration.get("action", {})
    gain_spec = configuration.get("gain", {})
    windows = configuration.get("windows", [])
    window_ids = [str(row["id"]) for row in windows]
    endpoints_valid = (
        window_ids == ["explicit-pilot", "analytic-upper-bound", "one-over-450"]
        and all(close(float(row["endpoint"]), endpoint(str(row["expression"])), 2.0e-15) for row in windows)
        and all("not" in str(row["role"]).lower() for row in windows)
    )

    cutoffs = [int(value) for value in action_spec["cutoffs"]]
    orders = [int(value) for value in action_spec["quadratureOrders"]]
    primary_order = int(action_spec["primaryQuadratureOrder"])
    lambdas = [int(value) for value in gain_spec["lambdas"]]
    cutoff_grid = [int(value) for value in gain_spec["cutoffComparison"]["cutoffs"]]
    step_grid = [float(value) for value in gain_spec["stepComparison"]["fastSteps"]]
    expected_action_count = len(windows) * len(cutoffs) * len(orders)
    expected_gain_count = len(windows) * (
        len(lambdas) + len(cutoff_grid) + len(step_grid) + 1
    )
    expected_comparison_count = len(windows) * (
        len(cutoffs) * (len(orders) - 1)
        + 2 * (len(cutoffs) - 1)
        + (len(cutoff_grid) - 1)
        + (len(step_grid) - 1)
        + 1
    )
    counts_valid = (
        len(action_rows) == expected_action_count
        and len(gain_rows) == expected_gain_count
        and len(comparison_rows) == expected_comparison_count
        and summary.get("counts") == {
            "actionRows": expected_action_count,
            "gainRows": expected_gain_count,
            "comparisonRows": expected_comparison_count,
            "windowCount": len(windows),
        }
    )

    action_map: dict[tuple[str, int, int], dict[str, str]] = {}
    action_rows_valid = True
    for row in action_rows:
        key = (row["windowId"], integer(row, "N"), integer(row, "quadratureOrder"))
        action_rows_valid = action_rows_valid and key not in action_map
        action_map[key] = row
        action_rows_valid = action_rows_valid and row["evidenceClass"] == EVIDENCE_CLASS
        action_rows_valid = action_rows_valid and strict_bool(row["diagnosticOnly"])
        action_rows_valid = action_rows_valid and row["windowId"] in window_ids
        action_rows_valid = action_rows_valid and "not" in row["endpointRole"].lower()
        action_rows_valid = action_rows_valid and close(
            finite(row, "endpoint"), endpoint(row["endpointExpression"]), 2.0e-15
        )
        action_rows_valid = action_rows_valid and close(
            finite(row, "finiteAction") / finite(row, "endpoint"),
            finite(row, "finiteAverageRate"),
        )
        action_rows_valid = action_rows_valid and abs(
            finite(row, "finiteWkbCorrection")
            + finite(row, "berryIntegral")
            + finite(row, "viscousIntegral")
        ) <= 2.0e-15
        for key_name in (
            "minimumNodeRealGap", "minimumNodeComplexSeparation",
            "maximumNodeEigenCondition", "maximumNodeEigenResidualRelative",
            "maximumDerivativeResidualRelative",
        ):
            action_rows_valid = action_rows_valid and finite(row, key_name) >= 0.0

    gain_maps: dict[str, dict[tuple[object, ...], dict[str, str]]] = {}
    gain_rows_valid = True
    for row in gain_rows:
        gain_maps.setdefault(row["gridKind"], {})[
            (row["windowId"], integer(row, "N"), integer(row, "Lambda"), finite(row, "fastStep"))
        ] = row
        gain_rows_valid = gain_rows_valid and row["evidenceClass"] == EVIDENCE_CLASS
        gain_rows_valid = gain_rows_valid and strict_bool(row["diagnosticOnly"])
        gain_rows_valid = gain_rows_valid and row["windowId"] in window_ids
        gain_rows_valid = gain_rows_valid and "not" in row["endpointRole"].lower()
        n_cut = integer(row, "N")
        lam = integer(row, "Lambda")
        action = action_map[(row["windowId"], n_cut, primary_order)]
        gain_rows_valid = gain_rows_valid and close(
            finite(row, "finiteAction"), finite(action, "finiteAction")
        )
        gain_rows_valid = gain_rows_valid and close(finite(row, "epsilon"), 1.0 / lam)
        log_gain = finite(row, "logSelectedGain")
        residual = log_gain - lam * finite(row, "finiteAction")
        gain_rows_valid = gain_rows_valid and close(
            finite(row, "LambdaInverseLogGain"), log_gain / lam
        )
        gain_rows_valid = gain_rows_valid and close(
            finite(row, "residualLogGainMinusLambdaAction"), residual
        )
        gain_rows_valid = gain_rows_valid and close(
            finite(row, "residualMinusWkb"),
            residual - finite(row, "finiteWkbCorrection"),
        )
        gain_rows_valid = gain_rows_valid and integer(row, "topClusterDimension") == 1
        gain_rows_valid = gain_rows_valid and integer(row, "stepCount") > 0
        gain_rows_valid = gain_rows_valid and finite(row, "topEigenResidualRelative") >= 0.0

    comparisons_valid = True
    for row in comparison_rows:
        difference = finite(row, "absoluteDifference")
        tolerance = finite(row, "tolerance")
        passed = difference <= tolerance
        comparisons_valid = comparisons_valid and strict_bool(row["diagnosticOnly"])
        comparisons_valid = comparisons_valid and row["evidenceClass"] == EVIDENCE_CLASS
        comparisons_valid = comparisons_valid and strict_bool(row["passCheck"]) is passed
        comparisons_valid = comparisons_valid and passed
        comparisons_valid = comparisons_valid and row["windowId"] in window_ids
        interpretation = row["diagnosticInterpretation"].lower()
        comparisons_valid = comparisons_valid and (
            "finite" in interpretation or "ordinary" in interpretation
        )

    boundary = summary.get("claimBoundary", {})
    boundary_valid = (
        boundary.get("finiteBinary64GalerkinDiagnostic") is True
        and all(
            value is False for key, value in boundary.items()
            if key != "finiteBinary64GalerkinDiagnostic"
        )
        and manifest.get("claimBoundary") == boundary
        and "none" in str(manifest.get("continuumConclusion", "")).lower()
    )

    generated_bindings_valid = all(
        binding_valid(row, directory) for row in manifest.get("generatedBindings", [])
    )
    source_bindings_valid = all(
        binding_valid(row, ROOT) for row in manifest.get("sourceBindings", [])
    )
    expected_generated = {
        "action_rows.csv", "gain_rows.csv", "comparison_rows.csv",
        "environment.json", "summary.json", "progress.ndjson",
    }
    generated_binding_names = {
        str(row["path"]) for row in manifest.get("generatedBindings", [])
    }
    generated_bindings_valid = generated_bindings_valid and generated_binding_names == expected_generated

    ledger_rows = []
    for line in (directory / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        pieces = line.split("  ", 1)
        if len(pieces) != 2 or len(pieces[0]) != 64 or "/" in pieces[1]:
            raise ValueError(f"invalid SHA256 ledger row: {line}")
        ledger_rows.append((pieces[0], pieces[1]))
    actual_names = sorted(
        path.name for path in directory.iterdir()
        if path.is_file() and path.name != "SHA256SUMS"
    )
    ledger_valid = (
        [name for _, name in ledger_rows] == actual_names
        and all(sha256(directory / name) == digest for digest, name in ledger_rows)
    )

    progress_rows = [
        json.loads(line) for line in (directory / "progress.ndjson").read_text(encoding="utf-8").splitlines()
    ]
    progress_valid = (
        len(progress_rows) >= 3
        and progress_rows[0].get("event") == "start"
        and progress_rows[-1].get("event") == "complete"
        and [int(row["sequence"]) for row in progress_rows] == list(range(1, len(progress_rows) + 1))
    )

    summary_checks = summary.get("checks", {})
    summary_valid = (
        summary.get("allChecksPass") is True
        and bool(summary_checks)
        and all(value is True for value in summary_checks.values())
        and manifest.get("allChecksPass") is True
        and environment.get("sourceCommit") == summary.get("sourceCommit") == manifest.get("sourceCommit")
        and environment.get("precision") == "numpy.complex128 / IEEE-754 binary64 components"
        and environment.get("randomnessUsed") is False
    )

    checks = {
        "summarySchemaShape": summary_shape and schema_header,
        "endpointsAndRolesFailClosed": endpoints_valid,
        "declaredCountsExact": counts_valid,
        "actionRowsIndependentlyChecked": action_rows_valid,
        "gainRowsIndependentlyChecked": gain_rows_valid,
        "comparisonsIndependentlyChecked": comparisons_valid,
        "claimBoundaryFailClosed": boundary_valid,
        "generatedBindingsValid": generated_bindings_valid,
        "sourceBindingsValid": source_bindings_valid,
        "sha256LedgerComplete": ledger_valid,
        "progressLogComplete": progress_valid,
        "summaryAndEnvironmentConsistent": summary_valid,
    }
    result = {
        "schemaVersion": "r073i-finite-validation-v1",
        "directory": str(directory),
        "checks": checks,
        "allChecksPass": all(checks.values()),
        "counts": {
            "actionRows": len(action_rows),
            "gainRows": len(gain_rows),
            "comparisonRows": len(comparison_rows),
            "ledgerRows": len(ledger_rows),
        },
        "continuumConclusion": "none; validation covers only the finite archived package",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["allChecksPass"] else 2


ARGS = parse_args()

if __name__ == "__main__":
    raise SystemExit(main())
