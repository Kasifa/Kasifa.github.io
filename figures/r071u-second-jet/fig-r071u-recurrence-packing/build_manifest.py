#!/usr/bin/env python3
"""Build the draft/formal manifest and SHA256 ledger for Figure R0.71U."""

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
    "modular_solver.py",
    "independent_solver.py",
    "assemble_data.py",
    "validate_data.py",
    "independent_validate.py",
    "plot.py",
    "qa_images.py",
    "build_manifest.py",
    "primary-results.json",
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
    primary = json.loads((ROOT / "primary-results.json").read_text(encoding="utf-8"))
    independent = json.loads((ROOT / "independent-results.json").read_text(encoding="utf-8"))
    validation = json.loads((ROOT / "validation.json").read_text(encoding="utf-8"))
    independent_validation = json.loads(
        (ROOT / "independent-validation.json").read_text(encoding="utf-8")
    )
    records = [record(name) for name in ASSETS]
    by_name = {item["path"]: item for item in records}

    def data_record(name: str, file_format: str, schema: str) -> dict[str, object]:
        return {**by_name[name], "format": file_format, "schema": schema}

    data = [
        data_record(
            "config.json",
            "json",
            "exact modular problem, p1 sweep, cutoffs, annulus radius, DOP853 tolerances, and classification flags",
        ),
        data_record(
            "primary-results.json",
            "json",
            "vectorized mcut=24 shooting, target trace, root slopes, enstrophy, atoms, p1 sweep, and cutoff sweep",
        ),
        data_record(
            "independent-results.json",
            "json",
            "fresh sparse-shift mcut=36 shooting, target residuals, slopes, atoms, PDE reduction check, and primary differences",
        ),
        data_record(
            "progress.ndjson",
            "ndjson",
            "timestamped primary sweep, cutoff sweep, independent run, validation failure record, and final validation completion",
        ),
        data_record(
            "resource-log.ndjson",
            "ndjson",
            "timestamped local process CPU, system CPU, load average, logical CPU count, and peak-resident-set snapshots",
        ),
        data_record(
            "data.csv",
            "csv",
            "panel,series,case,x,y,time,p1,cutoff,value,unit,formula,evidenceClass,note",
        ),
        data_record(
            "figure-data-metadata.json",
            "json",
            "input hashes, row count, evidence map, annulus gap, classification, and claim boundary",
        ),
        data_record(
            "validation.json",
            "json",
            "producer-side PDE, residual, passage, atom, small-curve, cutoff, annulus, and provenance checks",
        ),
        data_record(
            "independent-validation.json",
            "json",
            "standalone formula reconstruction, sparse-run checks, and PDF/SVG/PNG/QA validation",
        ),
    ]
    payload = {
        "schemaVersion": "1.0",
        "figureId": "fig-r071u-recurrence-packing",
        "release": "R0.71U",
        "status": status,
        "analyticalQuestion": (
            "Can one compact target annulus of a genuine smooth unforced NSE "
            "trajectory return to zero at three prescribed positive times, "
            "and how do its jet atoms scale on the local recurrence curve?"
        ),
        "supportedClaim": (
            "In the audited finite modular lattices, six real shooting "
            "parameters produce three prescribed simple target returns. A "
            "separate sparse cutoff-36 implementation reproduces the parameters "
            "and slopes, while five re-shot p1 values exhibit the analytic "
            "quadratic atom-collapse boundary."
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
                "exact 2.5D triangular NSE Fourier reduction; nu=0.02, "
                "K=L=1, d=8, seven real shear parameters, three prescribed "
                "times; primary mcut=24 and independent sparse mcut=36"
            ),
            "precision": "IEEE binary64 complex Fourier coefficients",
            "solver": (
                "primary vectorized two-sided modular shifts and independent "
                "sparse shift matrices; SciPy DOP853 time integration and "
                "MINPACK hybr shooting of six real variables"
            ),
            "formalCommand": "commands recorded in command.txt",
            "wallTimeSeconds": primary["wallSeconds"] + independent["wallSeconds"],
            "finiteGalerkin": True,
            "pdeTimeStepping": True,
            "dns": False,
            "fittedData": True,
            "fitBoundary": (
                "three descriptive log-log slopes use five separately re-shot "
                "p1 samples; the analytic O(p1^2) theorem does not depend on the fit"
            ),
            "monitoring": {
                "enabled": True,
                "reportIntervalSeconds": 0.1,
                "trackedFields": [
                    "stage",
                    "p1",
                    "cutoff",
                    "completed",
                    "targetResidual",
                    "minimumSlope",
                    "elapsedSeconds",
                    "etaSeconds",
                    "processUserCpuSeconds",
                    "maximumResidentSetRaw"
                ],
                "progressLog": "progress.ndjson",
                "resourceLog": "resource-log.ndjson",
            },
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
            "dgx": "not used",
        },
        "environment": {
            "python": "3.12.13",
            "numpy": "2.5.2",
            "scipy": "1.18.0",
            "matplotlib": "3.11.1",
            "pillow": "12.3.0",
            "pypdf": "6.10.0",
            "packagesLock": "requirements.txt",
        },
        "evidenceMap": metadata["evidenceMap"],
        "data": data,
        "sourceData": [],
        "figure": {
            "profile": "journal-default",
            "widthMillimetres": 178.05,
            "heightMillimetres": 134.11,
            "script": "plot.py",
            "outputs": [
                by_name["figure.pdf"],
                by_name["figure.svg"],
                {**by_name["figure.png"], "dpi": 600},
            ],
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
            "dataCrossChecked": True,
        },
        "outputs": records,
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
