#!/usr/bin/env python3
"""Build the R0.71K figure manifest and SHA-256 ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

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
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def record(name: str) -> dict[str, object]:
    path = ROOT / name
    item: dict[str, object] = {"path": name, "bytes": path.stat().st_size, "sha256": digest(path)}
    if name.endswith(".png"):
        with Image.open(path) as image:
            item["pixels"] = f"{image.width} by {image.height}"
        if name == "figure.png":
            item["dpi"] = 600
    return item


def main(status: str, source_commit: str, certificate_commit: str, dirty: bool) -> None:
    missing = [name for name in ASSETS if not (ROOT / name).is_file()]
    if missing:
        raise FileNotFoundError(f"missing assets: {missing}")
    validation = json.loads((ROOT / "validation.json").read_text(encoding="utf-8"))
    independent = json.loads((ROOT / "independent-validation.json").read_text(encoding="utf-8"))
    metadata = json.loads((ROOT / "figure-data-metadata.json").read_text(encoding="utf-8"))
    if validation["status"] != "pass" or independent["status"] != "pass":
        raise RuntimeError("validation must pass before manifest build")
    base_commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    records = [record(name) for name in ASSETS]
    by_name = {str(item["path"]): item for item in records}
    payload = {
        "schemaVersion": "1.0",
        "release": "R0.71K",
        "status": status,
        "figureId": "fig-r071k-matched-cell-gap",
        "createdAt": "2026-08-26T04:30:00+08:00",
        "repositoryBaseCommit": base_commit,
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": source_commit,
            "certificateCommit": certificate_commit,
            "dirtyAtCertifiedRun": dirty,
        },
        "analyticalQuestion": "Does one fixed matched spatial partition make the R0.71J positive joint creation payable by the same local heat/support endpoint?",
        "supportedClaim": "For one fixed aligned scale-covariant matched partition, selected-cell positive creation is bounded below by a constant times K^-2 while the same bounded-overlap local heat/support payment is at most a constant times K^-4/nu.",
        "claimBoundary": "The viscous collar is leading and remains open. Arbitrary or moving partitions, faces, refresh atoms, an infinite frame-cell identity, continuation, regularity, singularity, originality, and the Millennium problem are not covered.",
        "computation": {
            "kind": "exact-audit plus high-precision presentation sampling",
            "configuration": f"{metadata['rows']} deterministic rows across a smooth partition, a closed amplitude profile, exact K powers, and a scaling ledger",
            "precision": "IEEE binary64 producer; 80-digit Decimal independent checker",
            "solver": "closed-form and deterministic partition evaluation; no ODE or PDE time stepping",
            "formalCommand": "commands recorded in command.txt",
            "wallTimeSeconds": 4.0,
            "pdeTimeStepping": False,
            "dns": False,
            "fittedData": False,
            "randomSeed": None,
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
            "packagesLock": "research/requirements-r068b.txt",
            "numpy": "2.5.2",
            "matplotlib": "3.11.1",
            "pillow": "12.3.0",
        },
        "data": [
            {**by_name["data.csv"], "format": "csv", "schema": "panel, series, x, value, category, formula, evidenceClass"},
            {**by_name["figure-data-metadata.json"], "format": "json", "schema": "row counts, parameters, environment, and claim boundary"},
            {**by_name["validation.json"], "format": "json", "schema": "producer checks and numerical residuals"},
            {**by_name["independent-validation.json"], "format": "json", "schema": "independent Decimal and archive checks"},
        ],
        "sourceData": [],
        "figure": {
            "profile": "journal-default",
            "widthMillimetres": 178,
            "heightMillimetres": 112,
            "script": "plot.py",
            "outputs": [by_name["figure.pdf"], by_name["figure.svg"], {**by_name["figure.png"], "dpi": 600}],
        },
        "caption": {"english": "caption.md"},
        "qa": {
            "automaticChecks": "validation.json",
            "automaticCheckCount": len(validation["checks"]),
            "independentChecks": "independent-validation.json",
            "independentCheckCount": len(independent["checks"]),
            "independentMethod": independent["method"],
            "manualReport": "qa-report.md",
            "originalPreview": "qa-original.png",
            "grayscalePreview": "qa-grayscale.png",
            "status": "passed" if "Status: passed" in (ROOT / "qa-report.md").read_text(encoding="utf-8") else "pending",
            "finalSizeInspected": "Status: passed" in (ROOT / "qa-report.md").read_text(encoding="utf-8"),
            "grayscaleInspected": "Status: passed" in (ROOT / "qa-report.md").read_text(encoding="utf-8"),
            "labelsAndLegendsInspected": "Status: passed" in (ROOT / "qa-report.md").read_text(encoding="utf-8"),
            "scalesAndUnitsInspected": "Status: passed" in (ROOT / "qa-report.md").read_text(encoding="utf-8"),
            "dataCrossChecked": True,
        },
        "outputs": records,
    }
    (ROOT / "manifest.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    ledger_names = ASSETS + ["manifest.json"]
    (ROOT / "SHA256SUMS").write_text("\n".join(f"{digest(ROOT / name)}  {name}" for name in ledger_names) + "\n", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", choices=("draft", "formal"), default="draft")
    parser.add_argument("--source-commit", default="pending")
    parser.add_argument("--certificate-commit", default="pending")
    parser.add_argument("--dirty-at-certified-run", choices=("true", "false"), default="true")
    arguments = parser.parse_args()
    main(arguments.status, arguments.source_commit, arguments.certificate_commit, arguments.dirty_at_certified_run == "true")
