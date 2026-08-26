#!/usr/bin/env python3
"""Build the manifest and checksum ledger for the R0.71T figure."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image


ROOT = Path(__file__).resolve().parent
ASSETS = [
    "README.md",
    "caption.md",
    "figure-contract.md",
    "contract.json",
    "config.json",
    "command.txt",
    "environment.txt",
    "requirements.txt",
    "galerkin_shoot.py",
    "independent_galerkin.py",
    "assemble_data.py",
    "validate_data.py",
    "independent_validate.py",
    "plot.py",
    "qa_images.py",
    "build_manifest.py",
    "solver-results.json",
    "independent-results.json",
    "progress.ndjson",
    "resource-log.ndjson",
    "data.csv",
    "figure-data-metadata.json",
    "validation.json",
    "independent-validation.json",
    "figure.pdf",
    "figure.svg",
    "figure.png",
    "qa-original.png",
    "qa-grayscale.png",
    "qa-pdf.png",
    "qa-report.md",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(name: str) -> dict[str, object]:
    path = ROOT / name
    result: dict[str, object] = {
        "path": name,
        "bytes": path.stat().st_size,
        "sha256": digest(path),
    }
    if path.suffix.lower() == ".png":
        with Image.open(path) as image:
            result["pixels"] = f"{image.width} by {image.height}"
    return result


def main(status: str, source_commit: str, certificate_commit: str, dirty: bool) -> None:
    missing = [name for name in ASSETS if not (ROOT / name).is_file()]
    if missing:
        raise FileNotFoundError(missing)
    metadata = json.loads((ROOT / "figure-data-metadata.json").read_text(encoding="utf-8"))
    producer = json.loads((ROOT / "solver-results.json").read_text(encoding="utf-8"))
    independent_run = json.loads((ROOT / "independent-results.json").read_text(encoding="utf-8"))
    validation = json.loads((ROOT / "validation.json").read_text(encoding="utf-8"))
    independent_validation = json.loads((ROOT / "independent-validation.json").read_text(encoding="utf-8"))
    records = [record(name) for name in ASSETS]
    by_name = {item["path"]: item for item in records}

    def data_record(name: str, file_format: str, schema: str) -> dict[str, object]:
        return {**by_name[name], "format": file_format, "schema": schema}

    data = [
        data_record(
            "config.json",
            "json",
            "seed, target shell, time values, Galerkin truncations, solver tolerances, and classification flags",
        ),
        data_record(
            "solver-results.json",
            "json",
            "primary pseudo-spectral shooting runs, event atoms, residuals, and selected trajectory samples",
        ),
        data_record(
            "independent-results.json",
            "json",
            "direct-convolution same-truncation parity and N=12,Kcut=3 refined validation run",
        ),
        data_record(
            "progress.ndjson",
            "ndjson",
            "timestamped stages, tau progress, target residuals, elapsed time, and ETA",
        ),
        data_record(
            "resource-log.ndjson",
            "ndjson",
            "timestamped local process CPU, load average, logical CPU count, and peak-resident-set snapshots",
        ),
        data_record(
            "data.csv",
            "csv",
            "panel,series,case,N,Kcut,x,y,value,unit,formula,evidenceClass,note",
        ),
        data_record(
            "figure-data-metadata.json",
            "json",
            "input hashes, evidence map, configurations, numerical classification, and claim boundary",
        ),
        data_record(
            "validation.json",
            "json",
            "producer-side shooting, crossing, slope-identity, scaling, and boundary checks",
        ),
        data_record(
            "independent-validation.json",
            "json",
            "standalone raw-run, formula, progress, PDF, SVG, PNG, and boundary checks",
        ),
    ]
    payload = {
        "schemaVersion": "1.0",
        "figureId": "fig-r071t-internal-entry",
        "release": "R0.71T",
        "status": status,
        "analyticalQuestion": (
            "Does finite Galerkin evolution corroborate the positive-time "
            "internal target-shell zero from the local NSE flow-map "
            "construction, and does double scaling separate its entry atom "
            "from the bare normalized Leray time budget?"
        ),
        "supportedClaim": (
            "In the audited finite Galerkin systems, an eight-dimensional "
            "initial target-shell correction produces a simple positive-time "
            "zero, its norm has the predicted first-order coefficient, and "
            "the atom equals the slope-charge reconstruction. The exact "
            "leading double-scaling ledger has atom-to-budget ratio proportional "
            "to lambda squared."
        ),
        "claimBoundary": metadata["claimBoundary"],
        "createdAt": datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="seconds"),
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": source_commit,
            "certificateCommit": certificate_commit,
            "dirtyAtCertifiedRun": dirty,
        },
        "computation": {
            "kind": "simulation",
            "configuration": (
                "x3-independent three-component periodic Galerkin sector; "
                "primary N=10,Kcut=2 at five tau values; independent direct "
                "convolution at N=10,Kcut=2 and N=12,Kcut=3 for tau=0.04"
            ),
            "precision": "IEEE binary64 complex Fourier coefficients",
            "solver": (
                "primary dealiased pseudo-spectral and independent direct-"
                "convolution Galerkin right-hand sides; SciPy DOP853 time "
                "integration and hybr eight-real-dimensional root shooting"
            ),
            "formalCommand": "commands recorded in command.txt",
            "wallTimeSeconds": producer["wallSeconds"] + independent_run["wallSeconds"],
            "finiteGalerkin": True,
            "pdeTimeStepping": True,
            "dns": False,
            "fittedData": False,
            "monitoring": {
                "enabled": True,
                "reportIntervalSeconds": 0.1,
                "trackedFields": [
                    "stage",
                    "tau",
                    "completed",
                    "targetResidual",
                    "rootCalls",
                    "APlus",
                    "elapsedSeconds",
                    "etaSeconds",
                    "processCpuSeconds",
                    "maximumResidentSetRaw"
                ],
                "progressLog": "progress.ndjson",
                "resourceLog": "resource-log.ndjson"
            }
        },
        "compute": {
            "host": "local Mac workstation, Apple Silicon arm64",
            "operatingSystem": "macOS 26.6.2 (build 25G83)",
            "cpu": "Apple M5 Max",
            "memoryGiB": 36,
            "processes": 1,
            "threadsPerProcess": 1,
            "logicalCpuCount": 18,
            "gpu": "not used",
            "dgx": "not used"
        },
        "environment": {
            "python": "3.12.13",
            "numpy": "2.5.2",
            "scipy": "1.18.0",
            "matplotlib": "3.11.1",
            "pillow": "12.3.0",
            "pypdf": "6.10.0",
            "packagesLock": "requirements.txt"
        },
        "evidenceMap": metadata["evidenceMap"],
        "data": data,
        "sourceData": [],
        "figure": {
            "profile": "journal-default",
            "widthMillimetres": 178,
            "heightMillimetres": 124,
            "script": "plot.py",
            "outputs": [
                by_name["figure.pdf"],
                by_name["figure.svg"],
                {**by_name["figure.png"], "dpi": 600}
            ]
        },
        "caption": {"english": "caption.md"},
        "qa": {
            "automaticChecks": "validation.json",
            "automaticCheckCount": validation["checkCount"],
            "independentChecks": "independent-validation.json",
            "independentCheckCount": independent_validation["checkCount"],
            "independentMethod": independent_validation["method"],
            "manualReport": "qa-report.md",
            "originalPreview": "qa-original.png",
            "grayscalePreview": "qa-grayscale.png",
            "pdfRenderPreview": "qa-pdf.png",
            "status": "passed",
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "dataCrossChecked": True
        },
        "outputs": records
    }
    (ROOT / "manifest.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    ledger = ASSETS + ["manifest.json"]
    (ROOT / "SHA256SUMS").write_text(
        "\n".join(f"{digest(ROOT / name)}  {name}" for name in ledger) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", choices=("draft", "formal"), default="draft")
    parser.add_argument("--source-commit", default="pending")
    parser.add_argument("--certificate-commit", default="pending")
    parser.add_argument("--dirty-at-certified-run", choices=("true", "false"), default="true")
    arguments = parser.parse_args()
    main(
        arguments.status,
        arguments.source_commit,
        arguments.certificate_commit,
        arguments.dirty_at_certified_run == "true",
    )
