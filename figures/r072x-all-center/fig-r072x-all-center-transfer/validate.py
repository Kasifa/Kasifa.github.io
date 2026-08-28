#!/usr/bin/env python3
"""Fail-closed validation for the R0.72X all-center figure package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[2]
FIGURE_ID = "fig-r072x-all-center-transfer"
EXPECTED_LANCZOS_RITZ_POLICY = {
    "minDimension": 8,
    "maxDimension": 32,
    "checkEvery": 4,
    "relativeResidualTolerance": 1.0e-10,
    "reorthogonalizationPasses": 2,
}
EXPECTED_QA_THRESHOLDS = {
    "maxRelativeToFine": 5.0e-4,
    "maxAdjointDefect": 1.0e-10,
    "maxRitzResidual": 1.0e-8,
    "maxRayleighNormDefect": 1.0e-10,
}
EXPECTED_DATA_FIELDS = [
    "panel", "kind", "series", "physicalCenter", "alpha", "resolution",
    "timeSteps", "krylovDimension", "normEstimate", "ritzResidual",
    "rayleighNormDefect", "adjointDefect", "relativeToFine",
    "interfaceValue", "expectedPower", "blockHalfWidth", "fullBlockCount",
    "formula", "status",
]
EXPECTED_TRACKED_FIELDS = [
    "event", "physicalCenter", "alpha", "level", "resolution", "timeSteps",
    "normEstimate", "krylovDimension", "ritzResidual", "ritzCheckpoints",
    "rayleighNormDefect", "adjointDefect", "completed", "total",
    "etaSeconds", "elapsedSeconds", "maxResidentSetPlatformUnits",
]
EXPECTED_CLAIM_BOUNDARY = {
    "allCenterExactFamilyGraphCoercivityProvedInBoundReport": True,
    "allStartExactPathSemigroupProvedInBoundReport": True,
    "fixedMarginA1EnhancedDissipationImportedInBoundReport": True,
    "exactA2PathBlochUniformProvedInBoundReport": True,
    "periodicRepresentativeBetaZeroExactA1A2A1ConcatenationProvedInBoundReport": True,
    "shrinkingInterfaceFixedShapeA1HypothesesFalseInBoundReport": True,
    "numericalDiagnosticIsProof": False,
    "numericalDiagnosticEvaluatesAnalyticQ": False,
    "numericalDiagnosticIsInfiniteDimensionalOperatorNorm": False,
    "forcedHMinusOneTransferProved": False,
    "completeLinearizedShearSubsystemProved": False,
    "a1A2A1ConcatenationBlochUniform": False,
    "allPhysicalRowsUniformContraction": False,
    "nonlinearNavierStokesClosureProved": False,
    "clayMillenniumProblemSolved": False,
}
EXPECTED_DIAGNOSTIC_LIMITATIONS = [
    "single fixed seed and a small actual Ritz residual do not certify the global largest singular value of the finite propagator",
    "Krylov breakdown before dimension 8 is conservatively rejected even if it could be a happy exact closure",
]
SOURCE_FILES = {
    "README.md", "caption.md", "command.txt", "config.json",
    "contract.json", "environment.txt", "plot.py", "qa-protocol.md",
    "requirements.txt", "validate.py",
}
GENERATED_FILES = {
    "data.csv", "results.json", "validation.json", "progress.ndjson",
    "resource-log.ndjson", "qa-report.md", "figure.svg", "figure.pdf",
    "figure.png", "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png",
    "manifest.json", "SHA256SUMS",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    raise RuntimeError(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-formal", action="store_true")
    args = parser.parse_args()
    names = {path.name for path in PACKAGE.iterdir() if path.is_file()}
    manifest_path = PACKAGE / "manifest.json"
    if not manifest_path.is_file():
        if args.require_formal:
            fail("formal R0.72X figure package is absent")
        if names != SOURCE_FILES:
            fail("source-stage inventory is not exact")
        print(json.dumps({"status": "source", "errors": []}, indent=2))
        return 0

    if names != SOURCE_FILES | GENERATED_FILES:
        fail("formal-stage inventory is not exact")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    config = json.loads((PACKAGE / "config.json").read_text(encoding="utf-8"))
    results = json.loads((PACKAGE / "results.json").read_text(encoding="utf-8"))
    validation = json.loads((PACKAGE / "validation.json").read_text(encoding="utf-8"))
    if args.require_formal and manifest.get("status") != "formal":
        fail("formal status required")
    if manifest.get("figureId") != FIGURE_ID:
        fail("figure identity mismatch")
    if manifest.get("release") != "R0.72X":
        fail("release mismatch")
    if manifest.get("claimBoundary") != EXPECTED_CLAIM_BOUNDARY:
        fail("claim boundary is not exact")
    if manifest.get("diagnosticLimitations") != EXPECTED_DIAGNOSTIC_LIMITATIONS:
        fail("diagnostic limitations are not exact")
    if EXPECTED_DIAGNOSTIC_LIMITATIONS[0] not in results.get("claimsNotMade", []):
        fail("single-seed global-top limitation is absent")
    if manifest.get("simulation", {}).get("kind") != "simulation":
        fail("simulation schema mismatch")
    if manifest.get("simulation", {}).get("diagnosticOnly") is not True:
        fail("diagnostic boundary missing")
    if manifest.get("simulation", {}).get("randomSeed", "missing") is not None:
        fail("random seed must be null")
    if config.get("panelA", {}).get(
        "lanczosRitzPolicy"
    ) != EXPECTED_LANCZOS_RITZ_POLICY:
        fail("configured Lanczos-Ritz policy is not exact")
    if manifest.get("simulation", {}).get(
        "lanczosRitzPolicy"
    ) != EXPECTED_LANCZOS_RITZ_POLICY:
        fail("archived Lanczos-Ritz policy is not exact")
    if manifest.get("simulation", {}).get("monitoring", {}).get("enabled") is not True:
        fail("monitoring must be enabled")
    if manifest.get("simulation", {}).get("monitoring", {}).get(
        "trackedFields"
    ) != EXPECTED_TRACKED_FIELDS:
        fail("monitoring field ledger is not exact")
    if manifest.get("qa", {}).get("status") != "passed":
        fail("QA status is not passed")
    max_relative_to_fine = validation.get("numericalSummary", {}).get(
        "maxRelativeToFine"
    )
    if not isinstance(max_relative_to_fine, (int, float)) or not math.isfinite(
        max_relative_to_fine
    ):
        fail("maximum relative-to-fine diagnostic is invalid")
    if results.get("numericalSummary", {}).get(
        "maxRelativeToFine"
    ) != max_relative_to_fine:
        fail("relative-to-fine diagnostic disagrees across summaries")
    for key in (
        "finalSizeInspected", "grayscaleInspected",
        "labelsAndLegendsInspected", "scalesAndUnitsInspected",
        "dataCrossChecked",
    ):
        if manifest.get("qa", {}).get(key) is not True:
            fail(f"QA key false: {key}")
    source_commit = manifest.get("git", {}).get("sourceCommit", "")
    certificate_commit = manifest.get("git", {}).get("certificateCommit", "")
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        fail("source commit is invalid")
    if not re.fullmatch(r"[0-9a-f]{40}", certificate_commit):
        fail("certificate commit is invalid")
    if source_commit == certificate_commit:
        fail("source and certificate commits must be distinct")
    if subprocess.run(
        ["git", "merge-base", "--is-ancestor", source_commit, certificate_commit],
        cwd=ROOT,
    ).returncode:
        fail("certificate commit does not descend from source commit")

    with (PACKAGE / "data.csv").open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    if fieldnames != EXPECTED_DATA_FIELDS:
        fail("raw data schema is not exact")
    numerical = [row for row in rows if row["kind"] == "full-exact-block-forward-adjoint-norm"]
    interface = [row for row in rows if row["kind"] == "exact-interface-scaling"]
    tiling = [row for row in rows if row["kind"] == "exact-full-block-count"]
    if (len(rows), len(numerical), len(interface), len(tiling)) != (170, 150, 15, 5):
        fail("row-count contract failed")
    centers = sorted({float(row["physicalCenter"]) for row in numerical})
    if abs(centers[0] + math.log(2.0)) > 1e-14:
        fail("left endpoint missing")
    if abs(centers[-1] - (1.0 - math.log(2.0))) > 1e-14:
        fail("right endpoint missing")
    if 0.0 not in centers:
        fail("collision center missing")
    finite_fields = (
        "normEstimate",
        "ritzResidual",
        "rayleighNormDefect",
        "adjointDefect",
        "relativeToFine",
    )
    for index, row in enumerate(numerical):
        try:
            finite_values = [float(row[field]) for field in finite_fields]
        except (KeyError, TypeError, ValueError) as error:
            fail(f"numerical row {index} cannot be parsed: {error}")
        if not all(math.isfinite(value) for value in finite_values):
            fail(f"numerical row {index} contains a non-finite scalar")
        if row["series"] == "fine" and float(row["relativeToFine"]) != 0.0:
            fail(f"fine numerical row {index} is not exactly relative-to-self zero")
    if any(not (0.0 < float(row["normEstimate"]) <= 1.0 + 5e-12) for row in numerical):
        fail("discrete contraction audit failed")
    dimensions = [int(row["krylovDimension"]) for row in numerical]
    if any(
        not (
            EXPECTED_LANCZOS_RITZ_POLICY["minDimension"] <= dimension
            <= EXPECTED_LANCZOS_RITZ_POLICY["maxDimension"]
            and (
                dimension - EXPECTED_LANCZOS_RITZ_POLICY["minDimension"]
            ) % EXPECTED_LANCZOS_RITZ_POLICY["checkEvery"] == 0
        )
        for dimension in dimensions
    ):
        fail("row Krylov dimension violates the exact range or stride")
    if any(
        float(row["ritzResidual"])
        > EXPECTED_LANCZOS_RITZ_POLICY["relativeResidualTolerance"]
        for row in numerical
    ):
        fail("row actual Ritz residual exceeds the stopping tolerance")
    thresholds = config.get("panelB", {}).get("qaThresholds", {})
    if thresholds != EXPECTED_QA_THRESHOLDS:
        fail("predeclared numerical QA thresholds are not exact")
    if validation.get("qaThresholds") != EXPECTED_QA_THRESHOLDS:
        fail("archived numerical QA thresholds are not exact")
    numerical_maxima = {
        "maxRelativeToFine": max(
            float(row["relativeToFine"])
            for row in numerical
            if row["series"] != "fine"
        ),
        "maxAdjointDefect": max(float(row["adjointDefect"]) for row in numerical),
        "maxRitzResidual": max(float(row["ritzResidual"]) for row in numerical),
        "maxRayleighNormDefect": max(
            float(row["rayleighNormDefect"]) for row in numerical
        ),
    }
    for key, actual in numerical_maxima.items():
        threshold = thresholds[key]
        if not math.isfinite(actual):
            fail(f"numerical QA diagnostic is not finite: {key}")
        if actual > threshold:
            fail(f"numerical QA threshold failed: {key}")
        if validation.get("numericalSummary", {}).get(key) != actual:
            fail(f"numerical diagnostic disagrees with raw rows: {key}")
        if results.get("numericalSummary", {}).get(key) != actual:
            fail(f"result diagnostic disagrees with raw rows: {key}")
    dimension_summary = {
        "minKrylovDimension": min(dimensions),
        "maxKrylovDimension": max(dimensions),
    }
    for key, actual in dimension_summary.items():
        if validation.get("numericalSummary", {}).get(key) != actual:
            fail(f"validation Krylov summary disagrees with raw rows: {key}")
        if results.get("numericalSummary", {}).get(key) != actual:
            fail(f"result Krylov summary disagrees with raw rows: {key}")
    if any(float(row["interfaceValue"]) <= 0.0 for row in interface):
        fail("interface positivity failed")
    for row in tiling:
        alpha = float(row["alpha"])
        if int(row["fullBlockCount"]) != math.floor(1.0 / (0.5 * alpha * alpha)):
            fail("tiling arithmetic failed")

    ledger_rows = (PACKAGE / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    ledger_names = []
    for ledger_row in ledger_rows:
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/\\\r\n]+)", ledger_row)
        if not match:
            fail(f"malformed hash row: {ledger_row}")
        expected, name = match.groups()
        if sha256(PACKAGE / name) != expected:
            fail(f"hash mismatch: {name}")
        ledger_names.append(name)
    expected_ledger = sorted(name for name in names if name != "SHA256SUMS")
    if ledger_names != expected_ledger:
        fail("hash-ledger inventory mismatch")

    for extension in ("pdf", "svg", "png"):
        master = PACKAGE / f"figure.{extension}"
        public = ROOT / "public/assets/r072x" / f"{FIGURE_ID}.{extension}"
        if args.require_formal and master.read_bytes() != public.read_bytes():
            fail(f"public {extension} is not byte-identical")
    print(json.dumps({
        "status": manifest.get("status"),
        "errors": [],
        "rows": len(rows),
        "maxRelativeToFine": max_relative_to_fine,
        "maxRitzResidual": numerical_maxima["maxRitzResidual"],
        "maxRayleighNormDefect": numerical_maxima["maxRayleighNormDefect"],
        **dimension_summary,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
