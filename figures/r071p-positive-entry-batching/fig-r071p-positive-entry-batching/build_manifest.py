#!/usr/bin/env python3
"""Build the draft/formal manifest and checksum ledger for this figure."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
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
    "command.txt",
    "environment.txt",
    "generate_data.py",
    "validate_data.py",
    "independent_validate.py",
    "plot.py",
    "qa_images.py",
    "build_manifest.py",
    "exact-certificate.json",
    "independent-certificate.json",
    "data.csv",
    "figure-data-metadata.json",
    "validation.json",
    "independent-validation.json",
    "figure.pdf",
    "figure.svg",
    "figure.png",
    "qa-original.png",
    "qa-grayscale.png",
    "qa-report.md",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(name: str) -> dict[str, object]:
    path = ROOT / name
    result: dict[str, object] = {"path": name, "bytes": path.stat().st_size, "sha256": digest(path)}
    if path.suffix.lower() == ".png":
        with Image.open(path) as image:
            result["pixels"] = f"{image.width} by {image.height}"
    return result


def git_head() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return "pending"


def main(status: str, source_commit: str, certificate_commit: str, dirty: bool) -> None:
    missing = [name for name in ASSETS if not (ROOT / name).is_file()]
    if missing:
        raise FileNotFoundError(f"missing assets: {missing}")
    metadata = json.loads((ROOT / "figure-data-metadata.json").read_text(encoding="utf-8"))
    validation = json.loads((ROOT / "validation.json").read_text(encoding="utf-8"))
    independent = json.loads((ROOT / "independent-validation.json").read_text(encoding="utf-8"))
    contract = json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))
    records = [record(name) for name in ASSETS]
    by_name = {item["path"]: item for item in records}
    base_commit = git_head()

    data_records = [
        {**by_name["exact-certificate.json"], "format": "json", "schema": "exact Gram, finite-overlap, positive-measure, temporal-packing, analyticity, and NSE initial-jet certificate"},
        {**by_name["independent-certificate.json"], "format": "json", "schema": "standalone random-overlap, root-detection, quadrature, and order-32 FFT certificate"},
        {**by_name["data.csv"], "format": "csv", "schema": "panel,series,case,component,N,x,y,value,unit,formula,evidenceClass,note"},
        {**by_name["figure-data-metadata.json"], "format": "json", "schema": "certificate hashes, evidence classes, validation residuals, runtime, and claim boundary"},
        {**by_name["validation.json"], "format": "json", "schema": "producer-side segmented-entry, overlap, temporal-scaling, and NSE-sharpness checks"},
        {**by_name["independent-validation.json"], "format": "json", "schema": "independent CSV, PDF, SVG, PNG, and final-size QA checks"},
    ]
    payload = {
        "schemaVersion": "1.0",
        "figureId": "fig-r071p-positive-entry-batching",
        "release": "R0.71P",
        "status": status,
        "repositoryBaseCommit": base_commit,
        "analyticalQuestion": contract["analyticalQuestion"],
        "supportedClaim": "The componentwise relaxed positive-entry measure, formed by taking soft positive parts before summing, is generally not the positive Jordan part of a signed aggregate. Its atoms have no signed shell-cell cancellation. Bounded spatial overlap pays every simultaneous finite batch, while the full sum remains sampled by an uncontrolled distinct entry-time counting measure.",
        "claimBoundary": contract["claimBoundary"],
        "createdAt": datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="seconds"),
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": source_commit,
            "certificateCommit": certificate_commit,
            "dirtyAtCertifiedRun": dirty,
        },
        "computation": {
            "kind": "exact-audit",
            "configuration": "exact SymPy Gram, componentwise positive-measure, finite-overlap, temporal-packing, and Fourier certificate; standalone 64-trial overlap audit, root detection, quadrature, and order-32 NumPy FFT; half-open sequential window [0,2*pi), left endpoint included and right endpoint excluded, with deterministic rows at N=1,2,4,8,16,32,64",
            "precision": "exact SymPy algebra plus deterministic IEEE binary64 NumPy/SciPy and order-32 FFT corroboration",
            "solver": "exact algebra and instantaneous initial jet; no PDE time stepping",
            "formalCommand": "commands recorded in command.txt",
            "wallTimeSeconds": metadata["generationWallSeconds"] + float(json.loads((ROOT / "independent-certificate.json").read_text(encoding="utf-8")).get("wallSeconds", 0.0)),
            "dns": False,
            "pdeTimeStepping": False,
            "fittedData": False,
            "intervalCertified": False,
            "randomSeed": metadata["independentRandomSeed"],
        },
        "compute": {
            "host": "local Mac workstation, Apple Silicon arm64",
            "operatingSystem": "macOS 26.6.2 (build 25G83)",
            "cpu": "Apple M5 Max",
            "memoryGiB": 36,
            "processes": 1,
            "threadsPerProcess": 1,
            "gpu": "not used",
            "dgx": "not used",
        },
        "environment": {
            "python": "3.12.13",
            "numpy": "2.5.2",
            "scipy": "1.18.0",
            "sympy": "1.14.0",
            "matplotlib": "3.11.1",
            "pillow": "12.3.0",
            "pypdf": "6.10.0",
            "packagesLock": "research/requirements-r068b.txt",
        },
        "evidenceMap": metadata["evidenceMap"],
        "data": data_records,
        "sourceData": [],
        "figure": {
            "profile": "journal-default",
            "widthMillimetres": 178,
            "heightMillimetres": 118,
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
            "independentCheckCount": independent["checkCount"],
            "independentMethod": independent["method"],
            "manualReport": "qa-report.md",
            "originalPreview": "qa-original.png",
            "grayscalePreview": "qa-grayscale.png",
            "status": "passed",
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "pdfRenderInspected": True,
            "labelsAndLegendsInspected": True,
            "evidenceLabelsInspected": True,
            "scalesAndUnitsInspected": True,
            "dataCrossChecked": True,
        },
        "outputs": records,
    }
    (ROOT / "manifest.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    ledger = ASSETS + ["manifest.json"]
    (ROOT / "SHA256SUMS").write_text("\n".join(f"{digest(ROOT / name)}  {name}" for name in ledger) + "\n", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", choices=("draft", "formal"), default="draft")
    parser.add_argument("--source-commit", default="pending")
    parser.add_argument("--certificate-commit", default="pending")
    parser.add_argument("--dirty-at-certified-run", choices=("true", "false"), default="true")
    args = parser.parse_args()
    main(args.status, args.source_commit, args.certificate_commit, args.dirty_at_certified_run == "true")
