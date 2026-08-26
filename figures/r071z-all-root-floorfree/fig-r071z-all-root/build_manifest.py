#!/usr/bin/env python3
"""Build the formal or draft manifest and checksum ledger for R0.71Z-1."""

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
    record: dict[str, object] = {"path": name, "bytes": path.stat().st_size, "sha256": digest(path)}
    if path.suffix.lower() == ".png":
        with Image.open(path) as image:
            record["pixels"] = [image.width, image.height]
            if "dpi" in image.info:
                record["dpi"] = [float(value) for value in image.info["dpi"]]
    return record


def parse_bool(value: str) -> bool:
    if value == "true":
        return True
    if value == "false":
        return False
    raise argparse.ArgumentTypeError("expected true or false")


def main(status: str, source_commit: str, dirty: bool) -> None:
    missing = [name for name in ASSETS if not (ROOT / name).is_file()]
    if missing:
        raise FileNotFoundError(f"missing manifest assets: {missing}")
    if status == "formal":
        if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
            raise ValueError("formal source commit must be a full 40-character hash")
        if dirty:
            raise ValueError("formal source/certificate run cannot be dirty")

    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    contract = json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))
    results = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
    metadata = json.loads((ROOT / "figure-data-metadata.json").read_text(encoding="utf-8"))
    validation = json.loads((ROOT / "validation.json").read_text(encoding="utf-8"))
    if validation["status"] != "passed":
        raise RuntimeError("validation.json did not pass")

    records = [asset_record(name) for name in ASSETS]
    by_name = {record["path"]: record for record in records}
    figure_config = config["figure"]
    created = datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="seconds")
    source_records = metadata["sourceCertificates"]
    payload = {
        "schemaVersion": "1.0.0",
        "figureId": config["figureId"],
        "release": config["release"],
        "status": status,
        "analyticalQuestion": contract["analyticalQuestion"],
        "supportedClaim": contract["takeaway"],
        "takeaway": contract["takeaway"],
        "claimBoundary": contract["claimBoundary"],
        "createdAt": created,
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": source_commit,
            "certificateCommit": source_commit,
            "dirtyAtCertifiedRun": dirty,
            "scopeNote": "The commit contains the R0.71Z theorem, primary certificate, and independent certificate. This figure is a deterministic downstream extraction and reconstruction.",
        },
        "sourceData": [
            {
                "location": "repository",
                "fileName": record["path"],
                "bytes": record["bytes"],
                "sha256": record["sha256"],
                "extractionCommand": "python produce_data.py --config config.json",
            }
            for record in source_records
        ],
        "data": [
            {
                **by_name["config.json"],
                "format": "json",
                "schema": "source certificates, coupling laws, retention range, physical figure dimensions, and claim classifications",
            },
            {
                **by_name["results.json"],
                "format": "json",
                "schema": "source hashes, reconstructed exact factors, fitted powers, fixed constants, and cross-check errors",
            },
            {
                **by_name["data.csv"],
                "format": "csv",
                "schema": "panel, series, M, N, eta, eta power, R, plotted and raw values, normalizer, units, formula, evidence class, source, and note",
            },
            {
                **by_name["data.json"],
                "format": "json",
                "schema": "lossless plot rows and evidence classes",
            },
            {
                **by_name["figure-data-metadata.json"],
                "format": "json",
                "schema": "source and data hashes, row count, evidence map, and claim boundary",
            },
            {
                **by_name["validation.json"],
                "format": "json",
                "schema": "independent formula reconstruction, source hashes, asymptotic fits, export checks, and final-size QA checks",
            },
            {
                **by_name["progress.ndjson"],
                "format": "ndjson",
                "schema": "timestamped extraction, reconstruction, plotting, QA, and validation stages",
            },
            {
                **by_name["resource-log.ndjson"],
                "format": "ndjson",
                "schema": "timestamped wall time, process CPU, peak resident set, load, and logical CPU records",
            },
        ],
        "evidenceMap": metadata["evidenceMap"],
        "asymptoticPowers": results["derivedFigureFits"],
        "independentAsymptoticPowers": validation["independentPowers"],
        "computation": {
            "kind": "exact-audit plus high-precision presentation sampling",
            "configuration": "R0.71Z unit phases; M=2^j+1 for j=1..30; eta=1, M^(1/2), and M^(6/7); fixed-window heat retention at R=1..32 with nu=0.02, d=8, A0=0.05",
            "precision": "source 110-digit Decimal theorem audit, independent binary64 finite-matrix certificate, and independent binary64 figure reconstruction",
            "solver": "no PDE solver or DNS; exact finite formulas, deterministic certificate extraction, and log-log descriptive fits over the stored tail grid",
            "formalCommand": "commands recorded in command.txt",
            "wallTimeSeconds": float(results["producerWallSeconds"]) + float(validation["wallSeconds"]),
            "producerWallSeconds": results["producerWallSeconds"],
            "validatorWallSeconds": validation["wallSeconds"],
            "fittedData": True,
            "fitBoundary": "tail regressions describe stored exact theorem rows and do not replace the analytic M^-2, M^-1, M^-5/6, or M^0 derivations",
            "analyticTheoremEnvelope": True,
            "certificateExtraction": True,
            "independentFiniteMatrixCorroboration": True,
            "exactAllRootSlopeMassTheorem": True,
            "launchInclusiveMixedWindowLedger": True,
            "fixedWindowRetentionCounterexample": True,
            "exactStrongCouplingRootConstruction": False,
            "pdeTimeStepping": False,
            "dns": False,
            "universalEndpointTheorem": False,
            "navierStokesRegularityResult": False,
            "randomSeed": None,
            "monitoring": {
                "enabled": True,
                "progressLog": "progress.ndjson",
                "resourceLog": "resource-log.ndjson",
                "trackedFields": [
                    "stage",
                    "M",
                    "MOverKs",
                    "rowCount",
                    "elapsedSeconds",
                    "processUserCpuSeconds",
                    "processSystemCpuSeconds",
                    "maximumResidentSetRaw"
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
            "matplotlib": "3.11.1",
            "pillow": "12.3.0",
            "poppler": "bundled runtime",
            "packagesLock": "requirements.txt",
        },
        "figure": {
            "profile": "journal-default",
            "script": "plot.py",
            "widthMillimetres": figure_config["widthMillimetres"],
            "heightMillimetres": figure_config["heightMillimetres"],
            "outputs": [
                {**by_name["figure.pdf"]},
                {**by_name["figure.svg"]},
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
    (ROOT / "manifest.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    ledger = ASSETS + ["manifest.json"]
    (ROOT / "SHA256SUMS").write_text("\n".join(f"{digest(ROOT / name)}  {name}" for name in ledger) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": status,
                "assets": len(ASSETS),
                "sourceCommit": source_commit,
                "dirtyAtCertifiedRun": dirty,
                "manifestSha256": digest(ROOT / "manifest.json"),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--status", choices=("draft", "formal"), required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--dirty-at-certified-run", type=parse_bool, required=True)
    arguments = parser.parse_args()
    main(arguments.status, arguments.source_commit, arguments.dirty_at_certified_run)
