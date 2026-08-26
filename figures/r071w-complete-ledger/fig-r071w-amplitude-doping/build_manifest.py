#!/usr/bin/env python3
"""Build the formal/provisional manifest and SHA256 ledger for Figure R0.71W."""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
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
    "produce_data.py",
    "plot.py",
    "qa_images.py",
    "validate.py",
    "build_manifest.py",
    "results.json",
    "data.csv",
    "data.json",
    "figure-data-metadata.json",
    "validation.json",
    "progress.ndjson",
    "resource-log.ndjson",
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


def asset_record(name: str) -> dict[str, object]:
    path = ROOT / name
    record: dict[str, object] = {
        "path": name,
        "bytes": path.stat().st_size,
        "sha256": digest(path),
    }
    if path.suffix.lower() == ".png":
        with Image.open(path) as image:
            record["pixels"] = [image.width, image.height]
            if "dpi" in image.info:
                record["dpi"] = [float(value) for value in image.info["dpi"]]
    return record


def main(status: str, source_commit: str, certificate_commit: str, dirty: bool) -> None:
    missing = [name for name in ASSETS if not (ROOT / name).is_file()]
    if missing:
        raise FileNotFoundError(f"missing manifest assets: {missing}")
    if status == "formal":
        for label, value in (
            ("source commit", source_commit),
            ("certificate commit", certificate_commit),
        ):
            if not re.fullmatch(r"[0-9a-f]{40}", value):
                raise ValueError(f"formal {label} must be a full 40-character hash")
        if dirty:
            raise ValueError("formal source/certificate run cannot be dirty")

    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    contract = json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))
    results = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
    metadata = json.loads(
        (ROOT / "figure-data-metadata.json").read_text(encoding="utf-8")
    )
    validation = json.loads((ROOT / "validation.json").read_text(encoding="utf-8"))
    if results["status"] != "passed" or validation["status"] != "passed":
        raise RuntimeError("producer and independent validation must pass")
    qa_report = (ROOT / "qa-report.md").read_text(encoding="utf-8")
    if "PENDING" in qa_report:
        raise RuntimeError("manual final-size QA remains pending")
    if source_commit != config["sourceCertificateCommit"]:
        raise RuntimeError("source commit does not match config provenance")
    if certificate_commit != config["sourceCertificateCommit"]:
        raise RuntimeError("certificate commit does not match config provenance")

    records = [asset_record(name) for name in ASSETS]
    by_name = {record["path"]: record for record in records}
    source_data = []
    for source in metadata["sourceCertificates"]:
        source_data.append(
            {
                "label": source["label"],
                "location": source["location"],
                "fileName": source["fileName"],
                "bytes": source["bytes"],
                "sha256": source["sha256"],
                "status": source["status"],
                "extractionCommand": source["extractionCommand"],
                "commit": certificate_commit,
            }
        )

    payload = {
        "schemaVersion": "1.0",
        "figureId": config["figureId"],
        "release": config["release"],
        "status": status,
        "createdAt": datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(
            timespec="seconds"
        ),
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": source_commit,
            "certificateCommit": certificate_commit,
            "dirtyAtCertifiedRun": dirty,
            "scopeNote": (
                "dirtyAtCertifiedRun refers only to committed research inputs and "
                "certificates; generated figure-package assets are downstream outputs"
            ),
        },
        "analyticalQuestion": contract["analyticalQuestion"],
        "supportedClaim": contract["takeaway"],
        "claimBoundary": contract["claimBoundary"],
        "computation": {
            "kind": "data-analysis",
            "configuration": (
                "R0.71W amplitude doping alpha=3/2; nu=.02; target=(1,1); "
                "d=8; roots=(.1,.2)/q^2; B_q=A_q q; analytic q=2^8..2^32 "
                "in steps of four powers; retained coset q=256..4096, R=40; "
                "q=1024 radius audit R=15,30,60 against R=40"
            ),
            "precision": (
                "certificate extraction from the committed primary high-precision "
                "and independent ledgers, plus IEEE binary64 retained-coset output"
            ),
            "solver": (
                "no solver rerun in the figure producer; committed nonlinear source "
                "uses SciPy DOP853 with nonlinear least-squares/root continuation"
            ),
            "formalCommand": "commands recorded in command.txt",
            "wallTimeSeconds": results["wallSeconds"] + validation["wallSeconds"],
            "producerWallSeconds": results["wallSeconds"],
            "validatorWallSeconds": validation["wallSeconds"],
            "certificateExtraction": True,
            "finiteRetainedCosetIntegration": True,
            "pdeTimeStepping": False,
            "dns": False,
            "continuumIftProof": False,
            "spectralConvergenceProof": False,
            "randomSeed": None,
            "fittedData": True,
            "fitBoundary": (
                "displayed fitted powers are descriptive corroboration of the "
                "certificate's analytic orders; they do not prove continuum limits"
            ),
            "monitoring": {
                "enabled": True,
                "progressLog": "progress.ndjson",
                "resourceLog": "resource-log.ndjson",
                "trackedFields": [
                    "stage",
                    "q",
                    "rootResidual",
                    "atomProxy",
                    "rotationalCharge",
                    "normalizedSlope",
                    "elapsedSeconds",
                    "processUserCpuSeconds",
                    "processSystemCpuSeconds",
                    "maximumResidentSetRaw",
                ],
            },
        },
        "compute": {
            "host": "local Mac workstation, Apple Silicon arm64",
            "operatingSystem": "macOS 26.6.2 (build 25G83)",
            "cpu": "Apple M5 Max",
            "memoryGiB": 36,
            "logicalCpuCount": 18,
            "processes": 1,
            "threadsPerProcess": 1,
            "gpu": "not used",
            "dgx": "not used",
        },
        "environment": {
            "python": "3.12.13",
            "numpy": "2.3.5",
            "scipy": "1.16.1",
            "matplotlib": "3.11.1",
            "pillow": "12.3.0",
            "poppler": "bundled runtime",
            "packagesLock": "requirements.txt",
        },
        "asymptoticPowers": results["derivedFigureFits"],
        "independentAsymptoticPowers": validation["independentPowers"],
        "evidenceMap": metadata["evidenceMap"],
        "data": [
            {
                **by_name["config.json"],
                "format": "json",
                "schema": "source certificates, parameters, q grids, truncation radii, figure dimensions, and claim classification",
            },
            {
                **by_name["results.json"],
                "format": "json",
                "schema": "complete analytic and retained-coset source rows, certificate checks, source hashes, and fitted powers",
            },
            {
                **by_name["data.csv"],
                "format": "csv",
                "schema": "panel, series, q, x, y, unit, formula, evidence class, source, and note",
            },
            {
                **by_name["data.json"],
                "format": "json",
                "schema": "lossless plot rows and evidence classes",
            },
            {
                **by_name["figure-data-metadata.json"],
                "format": "json",
                "schema": "source/data hashes, row count, evidence map, and claim boundary",
            },
            {
                **by_name["validation.json"],
                "format": "json",
                "schema": "independent certificate/data reconstruction, log-log refits, raster/vector/PDF checks, and QA checks",
            },
            {
                **by_name["progress.ndjson"],
                "format": "ndjson",
                "schema": "timestamped extraction, case, plotting, QA, and validation events",
            },
            {
                **by_name["resource-log.ndjson"],
                "format": "ndjson",
                "schema": "timestamped wall time, process CPU, peak resident set, load, and logical CPU records",
            },
        ],
        "sourceData": source_data,
        "figure": {
            "profile": "journal-default",
            "widthMillimetres": config["figure"]["widthMillimetres"],
            "heightMillimetres": config["figure"]["heightMillimetres"],
            "script": "plot.py",
            "outputs": [
                by_name["figure.pdf"],
                by_name["figure.svg"],
                {**by_name["figure.png"], "dpi": 600, "archivalDpi": 600},
            ],
        },
        "caption": {"english": "caption.md"},
        "qa": {
            "automaticChecks": "validation.json",
            "automaticCheckCount": validation["checkCount"],
            "independentMethod": validation["method"],
            "manualReport": "qa-report.md",
            "colorPreview": "qa-original.png",
            "grayscalePreview": "qa-grayscale.png",
            "pdfRenderPreview": "qa-pdf.png",
            "status": "passed",
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "dataCrossChecked": True,
            "nonColorEncodingInspected": True,
            "pdfRenderInspected": True,
            "evidenceBoundaryInspected": True,
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
    print(
        json.dumps(
            {
                "status": status,
                "assets": len(ASSETS),
                "manifest": "manifest.json",
                "checksumLedger": "SHA256SUMS",
                "gitCommitHashes": {
                    "sourceCommit": source_commit,
                    "certificateCommit": certificate_commit,
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--status", choices=("provisional", "formal"), default="provisional")
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
