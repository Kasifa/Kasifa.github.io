#!/usr/bin/env python3
"""Fail-closed validation of a formal R0.72W figure package."""

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


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
CERTIFICATE_ROOT = REPOSITORY / "research/certificates/r072w"
FIGURE_ID = "fig-r072w-exact-tail-transfer"
SOURCE_FILES = {
    "README.md",
    "caption.md",
    "command.txt",
    "config.json",
    "contract.json",
    "environment.txt",
    "plot.py",
    "qa-protocol.md",
    "requirements.txt",
    "validate.py",
}
GENERATED = {
    "data.csv",
    "results.json",
    "validation.json",
    "progress.ndjson",
    "resource-log.ndjson",
    "qa-report.md",
    "figure.svg",
    "figure.pdf",
    "figure.png",
    "qa-final-size.png",
    "qa-grayscale.png",
    "qa-pdf.png",
    "manifest.json",
    "SHA256SUMS",
}
EXPECTED_ROWS = 744
EXPECTED_NUMERICAL_ROWS = 15
PUBLIC = REPOSITORY / "public/assets/r072w"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    if not path.is_file() or path.is_symlink():
        raise RuntimeError(f"required regular file is absent: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"JSON root must be an object: {path}")
    return value


def validate_certificate_commit(manifest: dict) -> dict:
    certificate_manifest = load(CERTIFICATE_ROOT / "manifest.json")
    git = manifest.get("git", {})
    source_commit = str(git.get("sourceCommit", ""))
    certificate_commit = str(git.get("certificateCommit", ""))
    if (
        certificate_manifest.get("status") != "formal"
        or source_commit != certificate_manifest.get("sourceCommit")
        or not re.fullmatch(r"[0-9a-f]{40}", source_commit)
        or not re.fullmatch(r"[0-9a-f]{40}", certificate_commit)
        or source_commit == certificate_commit
        or manifest.get("qa", {}).get("visualInspectionExplicit") is not True
    ):
        raise RuntimeError(
            "formal source/certificate/visual-QA lineage is inconsistent"
        )
    for commit in (source_commit, certificate_commit):
        if subprocess.run(
            ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
            cwd=REPOSITORY,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode:
            raise RuntimeError(f"invalid formal lineage commit: {commit}")
    if subprocess.run(
        ["git", "merge-base", "--is-ancestor", source_commit, certificate_commit],
        cwd=REPOSITORY,
    ).returncode:
        raise RuntimeError("certificateCommit does not descend from sourceCommit")
    for name in (
        "manifest.json",
        "certificate.json",
        "independent.json",
        "crosscheck.json",
        "SHA256SUMS",
    ):
        relative = f"research/certificates/r072w/{name}"
        committed = subprocess.check_output(
            ["git", "show", f"{certificate_commit}:{relative}"],
            cwd=REPOSITORY,
        )
        working = (REPOSITORY / relative).read_bytes()
        if committed != working:
            raise RuntimeError(
                f"working formal certificate differs from "
                f"{certificate_commit}:{relative}"
            )
    subprocess.run(
        [
            sys.executable,
            "research/certificates/r072w/validate_certificate.py",
            "--require-formal",
        ],
        cwd=REPOSITORY,
        check=True,
    )
    return load(CERTIFICATE_ROOT / "certificate.json")


def validate_claim_boundary(contract: dict, certificate: dict) -> None:
    boundary = contract.get("claimBoundary", {})
    required_true = {
        "weightedNonabsorbedRemainderEstimateProved",
        "growingCoreAbsorptionProved",
        "globalTermwiseRemainderAbsorptionFalse",
        "exactFamilyUnitCellCoercivityProved",
        "exactWholeLineGraphCoercivityProved",
        "exactPeriodicGraphCoercivityProved",
        "exactPeriodicBlockContractionProved",
    }
    required_false = {
        "numericalDiagnosticIsProof",
        "numericalDiagnosticDeterminesAnalyticConstant",
        "outerTimeConcatenationProved",
        "timeLengthUniformity",
        "nonlinearNavierStokesClosureProved",
        "clayMillenniumProblemSolved",
    }
    if any(boundary.get(key) is not True for key in required_true):
        raise RuntimeError("source claim boundary lost a proved/false analytic item")
    if any(boundary.get(key) is not False for key in required_false):
        raise RuntimeError("source claim boundary overstates an open item")
    certificate_boundary = certificate.get("claimBoundary", {})
    for key, value in boundary.items():
        if key in certificate_boundary and certificate_boundary[key] != value:
            raise RuntimeError(f"certificate/source claim-boundary drift: {key}")


def validate_ledger() -> None:
    ledger = ROOT / "SHA256SUMS"
    if not ledger.is_file() or ledger.is_symlink():
        raise RuntimeError("flat SHA256SUMS ledger is absent")
    names: list[str] = []
    for row in ledger.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/\\\r\n]+)", row)
        if not match:
            raise RuntimeError(f"malformed SHA256SUMS row: {row}")
        expected, name = match.groups()
        path = ROOT / name
        if not path.is_file() or path.is_symlink() or digest(path) != expected:
            raise RuntimeError(f"SHA256SUMS drift: {name}")
        names.append(name)
    actual = sorted(
        path.name
        for path in ROOT.iterdir()
        if path.is_file() and path.name != "SHA256SUMS"
    )
    if names != sorted(set(names)) or names != actual:
        raise RuntimeError(
            "SHA256SUMS must cover every flat regular file exactly once"
        )
    if set(actual) != (SOURCE_FILES | GENERATED) - {"SHA256SUMS"}:
        raise RuntimeError(
            "formal figure package contains an unexpected or missing file"
        )


def validate_data(rows: list[dict[str, str]]) -> None:
    numerical = [
        row
        for row in rows
        if row.get("kind") == "forward-adjoint-propagator-norm"
    ]
    if len(rows) != EXPECTED_ROWS or len(numerical) != EXPECTED_NUMERICAL_ROWS:
        raise RuntimeError("R0.72W analytic/numerical row inventory drift")
    if {row.get("panel") for row in rows} != {"A", "B", "C"}:
        raise RuntimeError("three-panel data inventory drift")
    if {
        (row.get("series"), int(row.get("resolution", 0)), int(row.get("timeSteps", 0)))
        for row in numerical
    } != {
        ("coarse", 512, 1000),
        ("medium", 1024, 2000),
        ("fine", 2048, 4000),
    }:
        raise RuntimeError("resolution-level configuration drift")
    if {float(row["alpha"]) for row in numerical} != {1.0, 0.75, 0.5, 0.35, 0.25}:
        raise RuntimeError("diagnostic alpha ledger drift")
    for row in numerical:
        values = [
            float(row["normEstimate"]),
            float(row["powerResidual"]),
            float(row["adjointDefect"]),
            float(row["relativeToFine"]),
        ]
        if not all(math.isfinite(value) and value >= 0.0 for value in values):
            raise RuntimeError("non-finite numerical audit value")
        if values[0] <= 0.0 or values[0] > 1.0 + 5.0e-12:
            raise RuntimeError("discrete energy-contraction range failed")
        if row.get("powerIterations") != "32":
            raise RuntimeError("fixed power-iteration ledger drift")
        if row.get("status") != "deterministic numerical diagnostic only; not proof":
            raise RuntimeError("numerical claim-boundary label drift")


def validate_progress() -> None:
    rows = [
        json.loads(row)
        for row in (ROOT / "progress.ndjson").read_text(encoding="utf-8").splitlines()
        if row.strip()
    ]
    if not rows or rows[0].get("event") != "build-start":
        raise RuntimeError("progress log does not start with build-start")
    completed = [row for row in rows if row.get("event") == "diagnostic-complete"]
    if len(completed) != EXPECTED_NUMERICAL_ROWS:
        raise RuntimeError("progress log lacks one completion per diagnostic")
    if rows[-1].get("event") != "archive-ready":
        raise RuntimeError("progress log does not end with archive-ready")


def validate_archive_metadata(manifest: dict) -> None:
    computation = manifest.get("computation", {})
    monitoring = computation.get("monitoring", {})
    if (
        computation.get("kind") != "simulation"
        or not computation.get("configuration")
        or not computation.get("formalCommand")
        or not computation.get("precision")
        or not computation.get("solver")
        or not isinstance(computation.get("wallTimeSeconds"), (int, float))
        or computation.get("wallTimeSeconds", 0) <= 0
        or monitoring.get("enabled") is not True
        or not isinstance(monitoring.get("reportIntervalSeconds"), (int, float))
        or monitoring.get("reportIntervalSeconds", 0) <= 0
        or not monitoring.get("trackedFields")
    ):
        raise RuntimeError("formal computation and monitoring metadata are incomplete")
    compute = manifest.get("compute", {})
    if (
        not isinstance(compute.get("memoryGiB"), (int, float))
        or compute.get("memoryGiB", 0) <= 0
    ):
        raise RuntimeError("formal compute memory metadata are incomplete")
    data_paths = {
        record.get("path")
        for record in manifest.get("data", [])
        if isinstance(record, dict)
    }
    if not {"progress.ndjson", "resource-log.ndjson"}.issubset(data_paths):
        raise RuntimeError("formal monitoring logs are absent from the data inventory")
    source_data = manifest.get("sourceData", [])
    if not source_data or any(
        not isinstance(record, dict) or not record.get("extractionCommand")
        for record in source_data
    ):
        raise RuntimeError("formal source-data extraction commands are incomplete")
    if manifest.get("qa", {}).get("scalesAndUnitsInspected") is not True:
        raise RuntimeError("formal scales-and-units QA is incomplete")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-formal", action="store_true")
    args = parser.parse_args()
    if not args.require_formal:
        parser.error("strict validation requires --require-formal")

    manifest = load(ROOT / "manifest.json")
    validation = load(ROOT / "validation.json")
    results = load(ROOT / "results.json")
    contract = load(ROOT / "contract.json")
    config = load(ROOT / "config.json")
    if (
        manifest.get("status") != "formal"
        or manifest.get("release") != "R0.72W"
        or manifest.get("figureId") != FIGURE_ID
        or contract.get("figureId") != FIGURE_ID
        or contract.get("stage") != "source-only"
        or contract.get("simulationPerformedAtSourceStage") is not False
        or config.get("panelC", {}).get("diagnosticOnly") is not True
    ):
        raise RuntimeError("formal R0.72W identity or source contract drift")
    if (
        validation.get("status") != "passed"
        or not all(validation.get("checks", {}).values())
        or validation.get("rowCount") != EXPECTED_ROWS
    ):
        raise RuntimeError("automatic figure validation failed")
    if (
        results.get("status") != "passed"
        or results.get("pdeSimulation") is not True
        or results.get("diagnosticOnly") is not True
        or results.get("randomSeed", "not-null") is not None
        or manifest.get("computation", {}).get("diagnosticOnly") is not True
        or manifest.get("computation", {}).get("randomSeed", "not-null") is not None
    ):
        raise RuntimeError("formal numerical diagnostic boundary drift")
    validate_archive_metadata(manifest)

    certificate = validate_certificate_commit(manifest)
    validate_claim_boundary(contract, certificate)
    validate_ledger()
    rows = list(csv.DictReader((ROOT / "data.csv").open(encoding="utf-8")))
    validate_data(rows)
    validate_progress()

    if (ROOT / "figure.pdf").read_bytes()[:4] != b"%PDF":
        raise RuntimeError("formal PDF signature drift")
    svg = (ROOT / "figure.svg").read_text(encoding="utf-8")
    for token in (
        "exact periodic scalar-row block contraction: CLOSED",
        "outer concatenation / nonlinear / Clay: OPEN",
        "NUMERICAL DIAGNOSTIC ONLY",
        "NOT PROOF",
        "global termwise absorption: FALSE",
    ):
        if escape_for_svg(token) not in svg:
            raise RuntimeError(f"visible theorem/diagnostic boundary absent: {token}")

    for extension in ("pdf", "svg", "png"):
        master = ROOT / f"figure.{extension}"
        public = PUBLIC / f"{FIGURE_ID}.{extension}"
        if not public.is_file() or public.is_symlink() or public.read_bytes() != master.read_bytes():
            raise RuntimeError(f"public {extension} is absent or not byte-identical")

    if manifest.get("publication", {}).get("publicCopiesComplete") is not True:
        raise RuntimeError("formal publication inventory is incomplete")
    if any(
        not entry.get("byteIdenticalToMaster")
        for entry in manifest.get("publication", {}).get("assets", [])
    ):
        raise RuntimeError("manifest public byte-identity claim failed")
    print("R0.72W formal figure validation: passed")


def escape_for_svg(value: str) -> str:
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


if __name__ == "__main__":
    main()
