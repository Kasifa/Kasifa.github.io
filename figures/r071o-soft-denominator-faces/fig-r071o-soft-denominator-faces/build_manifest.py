#!/usr/bin/env python3
"""Build the R0.71O journal-figure manifest and SHA-256 ledger."""

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
    if "Status: passed" not in qa_text:
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
        "release": "R0.71O",
        "status": status,
        "figureId": "fig-r071o-soft-denominator-faces",
        "createdAt": datetime.now().astimezone().isoformat(timespec="seconds"),
        "repositoryBaseCommit": base_commit,
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": source_commit,
            "certificateCommit": certificate_commit,
            "dirtyAtCertifiedRun": dirty,
        },
        "analyticalQuestion": (
            "What survives when the soft denominator approaches an isolated "
            "zero, and can ordinary denominator-mass and first-time-derivative "
            "budgets control the one-sided face cost?"
        ),
        "supportedClaim": (
            "Finite-order soft layers have explicit signed and Jordan atoms; "
            "signed cancellation does not remove relaxed face cost. Ordinary "
            "abstract quadratic budgets do not control its zero count, while "
            "one exact NSE initial jet realizes one positive right entry trace."
        ),
        "evidenceMap": metadata["panelEvidence"],
        "claimBoundary": metadata["claimBoundary"],
        "computation": {
            "kind": "exact-audit",
            "configuration": (
                "exact SymPy soft-profile and Fourier-convolution certificate; "
                "standalone SciPy quadrature and order-32 NumPy FFT certificate; "
                "deterministic presentation sampling at 241 profile points and "
                "N=1,2,4,8,16,32,64"
            ),
            "precision": metadata["precision"],
            "solver": "exact algebra and instantaneous initial jets; no PDE time stepping",
            "formalCommand": "commands recorded in command.txt",
            "wallTimeSeconds": (
                metadata["independentAuditWallTimeSeconds"]
                + metadata["dataGenerationWallTimeSeconds"]
            ),
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
            "scipy": "1.18.0",
            "sympy": "1.14.0",
            "matplotlib": "3.11.1",
            "pillow": "12.3.0",
            "pypdf": "6.10.0",
        },
        "data": [
            {
                **by_name["exact-certificate.json"],
                "format": "json",
                "schema": "exact symbolic soft identities, finite-order faces, oscillatory formulas, and NSE initial Fourier convolution",
            },
            {
                **by_name["independent-certificate.json"],
                "format": "json",
                "schema": "standalone quadrature, oscillatory-path, and order-32 FFT cross-checks",
            },
            {
                **by_name["data.csv"],
                "format": "csv",
                "schema": "panel,series,case,component,order,N,x,y,value,unit,formula,evidenceClass,note",
            },
            {
                **by_name["figure-data-metadata.json"],
                "format": "json",
                "schema": "certificate hashes, evidence classes, residuals, runtime, and claim boundary",
            },
            {
                **by_name["validation.json"],
                "format": "json",
                "schema": "producer-side profile, face-ledger, scaling, Fourier-mode, and claim-boundary checks",
            },
            {
                **by_name["independent-validation.json"],
                "format": "json",
                "schema": "independent Decimal, PDF, SVG, PNG, and final-size QA checks",
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
