#!/usr/bin/env python3
"""Build the manifest and checksum ledger for the R0.71S figure."""

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
    result: dict[str, object] = {
        "path": name,
        "bytes": path.stat().st_size,
        "sha256": digest(path),
    }
    if path.suffix.lower() == ".png":
        with Image.open(path) as image:
            result["pixels"] = f"{image.width} by {image.height}"
    return result


def main(
    status: str,
    source_commit: str,
    certificate_commit: str,
    dirty: bool,
) -> None:
    missing = [name for name in ASSETS if not (ROOT / name).is_file()]
    if missing:
        raise FileNotFoundError(missing)
    metadata = json.loads(
        (ROOT / "figure-data-metadata.json").read_text(encoding="utf-8")
    )
    validation = json.loads(
        (ROOT / "validation.json").read_text(encoding="utf-8")
    )
    independent = json.loads(
        (ROOT / "independent-validation.json").read_text(encoding="utf-8")
    )
    independent_certificate = json.loads(
        (ROOT / "independent-certificate.json").read_text(encoding="utf-8")
    )
    records = [record(name) for name in ASSETS]
    by_name = {item["path"]: item for item in records}
    data_records = [
        {
            **by_name["exact-certificate.json"],
            "format": "json",
            "schema": (
                "box diagonal, finite Gram, adjoint heat, bilinear mean, "
                "even-touch, and genuine initial-face exact certificate"
            ),
        },
        {
            **by_name["independent-certificate.json"],
            "format": "json",
            "schema": (
                "standalone NumPy and quadrature reconstruction of the "
                "R0.71S finite packet checks"
            ),
        },
        {
            **by_name["data.csv"],
            "format": "csv",
            "schema": (
                "panel,series,case,N,x,y,value,unit,formula,"
                "evidenceClass,note"
            ),
        },
        {
            **by_name["figure-data-metadata.json"],
            "format": "json",
            "schema": (
                "provenance hashes, evidence map, parameters, runtime, "
                "and claim boundary"
            ),
        },
        {
            **by_name["validation.json"],
            "format": "json",
            "schema": "producer-side table and boundary checks",
        },
        {
            **by_name["independent-validation.json"],
            "format": "json",
            "schema": "independent CSV, certificate, PDF, SVG, and PNG checks",
        },
    ]
    payload = {
        "schemaVersion": "1.0",
        "figureId": "fig-r071s-signed-packet",
        "release": "R0.71S",
        "status": status,
        "analyticalQuestion": (
            "Can a signed or separable bilinear parabolic packet retain "
            "entry-direction information without inverse-height sampling "
            "or temporal Gram growth?"
        ),
        "supportedClaim": (
            "For the audited nonzero-mean box and adjoint-heat packets, "
            "constant directional data costs one inverse parabolic height, "
            "while dense same-direction packets have a growing finite Gram "
            "constant. At an abstract even touch, the signed face and a "
            "zero-mean separable detector have zero response."
        ),
        "claimBoundary": metadata["claimBoundary"],
        "createdAt": datetime.now(
            ZoneInfo("Asia/Shanghai")
        ).isoformat(timespec="seconds"),
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": source_commit,
            "certificateCommit": certificate_commit,
            "dirtyAtCertifiedRun": dirty,
        },
        "computation": {
            "kind": "exact-audit plus high-precision presentation sampling",
            "configuration": (
                "exact rational box and even-touch ledgers, deterministic "
                "finite Gram eigenvalues, and closed-form adjoint heat packets"
            ),
            "precision": (
                "exact Python Fraction identities plus deterministic IEEE "
                "binary64 NumPy eigenvalue and quadrature checks"
            ),
            "solver": (
                "closed-form finite packet identities and matrix "
                "diagonalization; no PDE time stepping"
            ),
            "formalCommand": "commands recorded in command.txt",
            "wallTimeSeconds": (
                metadata["generationWallSeconds"]
                + float(independent_certificate.get("elapsedSeconds", 0.0))
            ),
            "dns": False,
            "pdeTimeStepping": False,
            "fittedData": False,
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
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "dataCrossChecked": True,
        },
        "outputs": records,
    }
    (ROOT / "manifest.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    ledger = ASSETS + ["manifest.json"]
    (ROOT / "SHA256SUMS").write_text(
        "\n".join(
            f"{digest(ROOT / name)}  {name}"
            for name in ledger
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--status",
        choices=("draft", "formal"),
        default="draft",
    )
    parser.add_argument("--source-commit", default="pending")
    parser.add_argument("--certificate-commit", default="pending")
    parser.add_argument(
        "--dirty-at-certified-run",
        choices=("true", "false"),
        default="true",
    )
    args = parser.parse_args()
    main(
        args.status,
        args.source_commit,
        args.certificate_commit,
        args.dirty_at_certified_run == "true",
    )
