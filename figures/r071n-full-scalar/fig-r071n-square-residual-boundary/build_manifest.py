#!/usr/bin/env python3
"""Build the R0.71N journal-figure manifest and SHA-256 ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime
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
    item: dict[str, object] = {
        "path": name,
        "bytes": path.stat().st_size,
        "sha256": digest(path),
    }
    if name.endswith(".png"):
        with Image.open(path) as image:
            item["pixels"] = f"{image.width} by {image.height}"
        if name == "figure.png":
            item["dpi"] = 600
    return item


def main(status: str, source_commit: str, certificate_commit: str, dirty: bool) -> None:
    missing = [name for name in ASSETS if not (ROOT / name).is_file()]
    if missing:
        raise FileNotFoundError(missing)
    validation = json.loads((ROOT / "validation.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (ROOT / "independent-validation.json").read_text(encoding="utf-8")
    )
    metadata = json.loads(
        (ROOT / "figure-data-metadata.json").read_text(encoding="utf-8")
    )
    if validation["status"] != "pass" or independent["status"] != "pass":
        raise RuntimeError("both validation paths must pass")
    qa_text = (ROOT / "qa-report.md").read_text(encoding="utf-8")
    qa_passed = "Status: passed" in qa_text
    if not qa_passed:
        raise RuntimeError("visual QA must pass before manifest construction")

    records = [record(name) for name in ASSETS]
    by_name = {item["path"]: item for item in records}
    base_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    payload = {
        "schemaVersion": "1.0",
        "release": "R0.71N",
        "status": status,
        "figureId": "fig-r071n-square-residual-boundary",
        "createdAt": datetime.now().astimezone().isoformat(timespec="seconds"),
        "repositoryBaseCommit": base_commit,
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": source_commit,
            "certificateCommit": certificate_commit,
            "dirtyAtCertifiedRun": dirty,
        },
        "analyticalQuestion": (
            "Does the complete fixed-cell scalar retain a coercive positive "
            "square after the local filtered-enstrophy substitution?"
        ),
        "supportedClaim": (
            "The complete scalar has an exact square--residual form. The local "
            "filtered-enstrophy substitution cancels that square exactly and "
            "leaves a signed second jet. Every surviving numerator row remains "
            "at the critical scaling order."
        ),
        "evidenceMap": metadata["panelEvidence"],
        "claimBoundary": metadata["claimBoundary"],
        "computation": {
            "kind": "exact-audit",
            "configuration": (
                "exact symbolic audit and deterministic alias-safe 48^3, 64^3, "
                "and 80^3 finite Fourier checks; Panel values selected at 64^3"
            ),
            "precision": metadata["precision"],
            "solver": "instantaneous NSE jets; no PDE time stepping",
            "formalCommand": "commands recorded in command.txt",
            "wallTimeSeconds": metadata["wallTimeSeconds"],
            "pdeTimeStepping": False,
            "dns": False,
            "fittedData": False,
            "intervalCertified": False,
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
            "pypdf": "6.10.0",
        },
        "data": [
            {
                **by_name["data.csv"],
                "format": "csv",
                "schema": "panel,series,witness,stage,component,x,value,unit,formula,evidenceClass,note",
            },
            {
                **by_name["figure-data-metadata.json"],
                "format": "json",
                "schema": "certificate hashes, witness residuals, evidence classes, and claim boundary",
            },
            {
                **by_name["validation.json"],
                "format": "json",
                "schema": "producer-side structure, value, sign, scaling, and claim-boundary checks",
            },
            {
                **by_name["independent-validation.json"],
                "format": "json",
                "schema": "independent Decimal, PDF, SVG, and PNG checks",
            },
        ],
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
            "automaticCheckCount": len(validation["checks"]),
            "independentChecks": "independent-validation.json",
            "independentCheckCount": len(independent["checks"]),
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
    parser.add_argument(
        "--dirty-at-certified-run", choices=("true", "false"), default="true"
    )
    args = parser.parse_args()
    main(
        args.status,
        args.source_commit,
        args.certificate_commit,
        args.dirty_at_certified_run == "true",
    )
