#!/usr/bin/env python3
"""Build the R0.71I manifest and SHA-256 ledger after validation."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
ASSET_NAMES = [
    "README.md",
    "caption.md",
    "figure-contract.md",
    "contract.json",
    "command.txt",
    "environment.txt",
    "generate_data.py",
    "plot.py",
    "validate_data.py",
    "independent_validate.py",
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


def description(name: str) -> dict[str, object]:
    path = ROOT / name
    result: dict[str, object] = {
        "path": name,
        "bytes": path.stat().st_size,
        "sha256": digest(path),
    }
    if name.endswith(".png"):
        with Image.open(path) as image:
            result["pixels"] = f"{image.width} by {image.height}"
        if name == "figure.png":
            result["dpi"] = 600
    return result


def main(
    status: str,
    source_commit: str,
    certificate_commit: str,
    dirty_at_certified_run: bool,
) -> None:
    missing = [name for name in ASSET_NAMES if not (ROOT / name).is_file()]
    if missing:
        raise FileNotFoundError(f"missing assets: {missing}")

    metadata = json.loads(
        (ROOT / "figure-data-metadata.json").read_text(encoding="utf-8")
    )
    validation = json.loads((ROOT / "validation.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (ROOT / "independent-validation.json").read_text(encoding="utf-8")
    )
    base_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    with Image.open(ROOT / "figure.png") as image:
        figure_pixels = f"{image.width} by {image.height}"

    outputs = [description(name) for name in ASSET_NAMES]
    by_name = {str(item["path"]): item for item in outputs}
    payload = {
        "schemaVersion": "1.0",
        "release": "R0.71I",
        "status": status,
        "figureId": "fig-r071i-joint-volume-gap",
        "createdAt": "2026-08-25T23:55:00+08:00",
        "repositoryBaseCommit": base_commit,
        "sourceState": "formal package generated during the R0.71I release construction",
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": source_commit,
            "certificateCommit": certificate_commit,
            "dirtyAtCertifiedRun": dirty_at_certified_run,
        },
        "analyticalQuestion": (
            "Can joint amplitude-direction heat cancellation convert the available "
            "physical-time heat volume into a K^-2-weighted BV budget?"
        ),
        "supportedClaim": (
            "A two-mode common-heat path has zero outer faces but a positive interior "
            "pulse, and its weighted trace-to-volume ratio is exactly proportional to "
            "K^2. A fixed-energy global-smooth 2D3C NSE family realizes a zero-entry "
            "positive limiting pulse for one fixed smooth radial two-ring multiplier. "
            "A separate two-cell refresh calculation has exact cost 3/28 for U=1."
        ),
        "claimBoundary": (
            "Panels A-B are an abstract common-heat model. Panel C is a closed-form "
            "fixed-window K-to-infinity limit, not a finite-K trajectory, and its "
            "multiplier is not the preselected broad dyadic frame. Panel D changes the "
            "cutoff shape. The package gives a volume-only obstruction, not a full "
            "face-paid BV no-go, regularity theorem, singularity claim, originality "
            "claim, or Millennium-problem conclusion."
        ),
        "computation": {
            "kind": "exact-audit plus high-precision presentation sampling",
            "configuration": (
                "567 closed-form presentation rows: common-heat zero-face pulse, "
                "exact K^2 ratio, fixed-window K-to-infinity 2D3C limiting profiles, "
                "and complementary-cutoff refresh curve"
            ),
            "precision": "IEEE binary64 producer; 70-digit Decimal independent checker",
            "solver": (
                "closed-form formula evaluation plus independent Decimal recomputation; "
                "no ODE or PDE time stepping"
            ),
            "formalCommand": (
                "PYTHONDONTWRITEBYTECODE=1 ../../../tmp/r068b-venv/bin/python "
                "generate_data.py --output data.csv --metadata figure-data-metadata.json "
                "&& PYTHONDONTWRITEBYTECODE=1 ../../../tmp/r068b-venv/bin/python "
                "validate_data.py --data data.csv --metadata figure-data-metadata.json "
                "--output validation.json && PYTHONDONTWRITEBYTECODE=1 "
                "../../../tmp/r068b-venv/bin/python independent_validate.py --data "
                "data.csv --output independent-validation.json"
            ),
            "wallTimeSeconds": 6.0,
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
            {
                "path": "data.csv",
                "format": "csv",
                "schema": (
                    f"{metadata['rows']} closed-form presentation rows with panel id, "
                    "abscissa, plotted ordinates, exact references, and scope labels"
                ),
                "bytes": by_name["data.csv"]["bytes"],
                "sha256": by_name["data.csv"]["sha256"],
            },
            {
                "path": "figure-data-metadata.json",
                "format": "json",
                "schema": "row counts, formula identifiers, precision, and generation boundary",
                "bytes": by_name["figure-data-metadata.json"]["bytes"],
                "sha256": by_name["figure-data-metadata.json"]["sha256"],
            },
            {
                "path": "validation.json",
                "format": "json",
                "schema": "producer validation status, check ledger, and maximum formula error",
                "bytes": by_name["validation.json"]["bytes"],
                "sha256": by_name["validation.json"]["sha256"],
            },
            {
                "path": "independent-validation.json",
                "format": "json",
                "schema": "independent 70-digit Decimal check ledger and error metrics",
                "bytes": by_name["independent-validation.json"]["bytes"],
                "sha256": by_name["independent-validation.json"]["sha256"],
            },
        ],
        "sourceData": [],
        "figure": {
            "profile": "journal-default",
            "widthMillimetres": 178,
            "heightMillimetres": 108,
            "script": "plot.py",
            "outputs": [
                by_name["figure.pdf"],
                by_name["figure.svg"],
                {
                    **by_name["figure.png"],
                    "dpi": 600,
                    "pixels": figure_pixels,
                },
            ],
        },
        "qa": {
            "automaticChecks": "validation.json",
            "automaticCheckCount": len(validation["checks"]),
            "independentChecks": "independent-validation.json",
            "independentCheckCount": len(independent["checks"]),
            "manualReport": "qa-report.md",
            "originalPreview": "qa-original.png",
            "grayscalePreview": "qa-grayscale.png",
            "status": "passed",
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "dataCrossChecked": True,
            "maximumFormulaError": validation["metrics"]["maximumFormulaError"],
            "maximumIndependentDecimalFormulaError": independent["metrics"][
                "maximumDecimalFormulaError"
            ],
        },
        "caption": {
            "english": "caption.md",
        },
        "outputs": outputs,
    }
    (ROOT / "manifest.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    ledger_names = sorted(ASSET_NAMES + ["manifest.json"])
    ledger = "".join(f"{digest(ROOT / name)}  {name}\n" for name in ledger_names)
    (ROOT / "SHA256SUMS").write_text(ledger, encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", choices=("draft", "formal"), default="draft")
    parser.add_argument("--source-commit")
    parser.add_argument("--certificate-commit")
    parser.add_argument(
        "--dirty-at-certified-run",
        choices=("true", "false"),
        default="true",
    )
    arguments = parser.parse_args()
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    main(
        arguments.status,
        arguments.source_commit or head,
        arguments.certificate_commit or head,
        arguments.dirty_at_certified_run == "true",
    )
