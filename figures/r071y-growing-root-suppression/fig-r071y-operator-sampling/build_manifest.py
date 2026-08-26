#!/usr/bin/env python3
"""Build the formal/provisional manifest and checksum ledger for R0.71Y-1."""

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


def main(status: str, source_commit: str, certificate_commit: str, dirty: bool) -> None:
    missing = [name for name in ASSETS if not (ROOT / name).is_file()]
    if missing:
        raise FileNotFoundError(f"missing manifest assets: {missing}")
    if status == "formal":
        for label, value in (("source commit", source_commit), ("certificate commit", certificate_commit)):
            if not re.fullmatch(r"[0-9a-f]{40}", value):
                raise ValueError(f"formal {label} must be a full 40-character hash")
        if dirty:
            raise ValueError("formal source/certificate run cannot be dirty")

    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    contract = json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))
    results = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
    metadata = json.loads((ROOT / "figure-data-metadata.json").read_text(encoding="utf-8"))
    validation = json.loads((ROOT / "validation.json").read_text(encoding="utf-8"))
    if validation["status"] != "passed":
        raise RuntimeError("validation.json did not pass")
    if source_commit != config["sourceCertificateCommit"] or certificate_commit != config["sourceCertificateCommit"]:
        raise RuntimeError("manifest commit arguments differ from config sourceCertificateCommit")

    records = [asset_record(name) for name in ASSETS]
    by_name = {record["path"]: record for record in records}
    figure_config = config["figure"]
    source_records = metadata["sourceCertificates"]
    created = datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="seconds")
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
            "certificateCommit": certificate_commit,
            "dirtyAtCertifiedRun": dirty,
            "scopeNote": "dirtyAtCertifiedRun refers to the committed R0.71Y theorem certificates; this figure is a deterministic downstream extraction and reconstruction",
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
                "schema": "source certificates, fixed coupling and gap laws, equal-grid N values, physical figure dimensions, and claim classifications",
            },
            {
                **by_name["results.json"],
                "format": "json",
                "schema": "source hashes, reconstructed theorem factors, independent cross-checks, fitted powers, and conditioning rows",
            },
            {
                **by_name["data.csv"],
                "format": "csv",
                "schema": "panel, theorem series, N, M, h, delta_obs, plotted value, raw value, normalizer, units, formulas, evidence class, source, and note",
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
                "schema": "source-commit verification, independent theorem reconstruction, fit checks, output checks, and final-size QA checks",
            },
            {
                **by_name["progress.ndjson"],
                "format": "ndjson",
                "schema": "timestamped extraction, reconstruction, plotting, QA, and validation events",
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
            "configuration": "R0.71Y unit phases M=2N+1; N=1..2^20; fixed delta_obs=1/8; separated h=0.05 and h=N^-1; canonical equal-grid r_l=l with h=N^-3 at N=4..64",
            "precision": "source 90-digit Decimal theorem audit, independent binary64 finite-matrix certificate, and independent binary64 figure reconstruction",
            "solver": "no PDE solver or DNS; exact finite formulas, deterministic source extraction, and log-log descriptive fits over the stored tail grid",
            "formalCommand": "commands recorded in command.txt",
            "wallTimeSeconds": float(results["producerWallSeconds"]) + float(validation["wallSeconds"]),
            "producerWallSeconds": results["producerWallSeconds"],
            "validatorWallSeconds": validation["wallSeconds"],
            "fittedData": True,
            "fitBoundary": "tail regressions describe the stored exact theorem rows and do not replace their analytic N^-1/N^-2 proofs",
            "analyticTheoremEnvelope": True,
            "certificateExtraction": True,
            "independentFiniteMatrixCorroboration": True,
            "exactGrowingRootConstruction": False,
            "completeAllRootCount": False,
            "quantitativeIftRadiusUpperBound": False,
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
                    "N",
                    "latticeFactor",
                    "fixedDeltaObsEnvelope",
                    "log10InverseLower",
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
                "manifest": "manifest.json",
                "checksumLedger": "SHA256SUMS",
                "gitCommitHashes": {"sourceCommit": source_commit, "certificateCommit": certificate_commit},
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
    args = parser.parse_args()
    main(args.status, args.source_commit, args.certificate_commit, args.dirty_at_certified_run == "true")
