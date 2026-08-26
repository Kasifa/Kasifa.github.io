#!/usr/bin/env python3
"""Build the provisional/formal manifest and SHA256 ledger for Figure R0.71V."""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
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

    records = [asset_record(name) for name in ASSETS]
    by_name = {record["path"]: record for record in records}
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
        },
        "analyticalQuestion": contract["analyticalQuestion"],
        "supportedClaim": contract["takeaway"],
        "claimBoundary": contract["claimBoundary"],
        "fixedTargetNormalization": {
            "targetKy": 1,
            "targetKz": 1,
            "rhoSquared": 2,
            "kappaStar": 1,
            "targetMultiplierMStar": 1,
            "reducedAtomToJ": 2,
            "reducedFirstIntegralToB1Star": 8,
            "reducedSecondIntegralToB2Star": 8,
            "reducedHeightChargeToHSquare": 8,
            "reducedDToD": 1,
        },
        "mainEvent": {
            "rootIndex": 2,
            "scaledRoot": 0.2,
            "atomField": "secondRootAtom",
            "firstRootMayBePaidSeparately": True,
            "totalAtomIsAuxiliaryOnly": True,
        },
        "computation": {
            "kind": "exact-audit",
            "configuration": (
                "N=2; q=8,16,32,64,128,256; nu=.02; "
                "Ky=Kz=kappa*=m*=1; rho^2=2; d=8; A=.05; "
                "roots=.1,.2; ell=.5; background Q=4, B=.25; epsilon=q^-2"
            ),
            "precision": (
                "IEEE binary64 producer and 80-digit mpmath independent "
                "interpolation reconstruction"
            ),
            "solver": (
                "closed heat-response functions, 2 by 2 interpolation solve, "
                "adaptive one-dimensional quadrature, and critical-point search"
            ),
            "formalCommand": "commands recorded in command.txt",
            "wallTimeSeconds": results["wallSeconds"] + validation["wallSeconds"],
            "producerWallSeconds": results["wallSeconds"],
            "validatorWallSeconds": validation["wallSeconds"],
            "nonlinearTrajectoryIntegration": False,
            "pdeTimeStepping": False,
            "finiteGalerkin": False,
            "dns": False,
            "covariantDilation": False,
            "randomSeed": None,
            "fittedData": True,
            "fitBoundary": (
                "tail-four log slopes are descriptive finite-q checks; analytic "
                "power orders do not depend on the fit"
            ),
            "monitoring": {
                "enabled": True,
                "progressLog": "progress.ndjson",
                "resourceLog": "resource-log.ndjson",
                "trackedFields": [
                    "stage",
                    "q",
                    "targetResidualMaximum",
                    "secondRootAtom",
                    "firstRow",
                    "secondRow",
                    "internalD",
                    "terminalD",
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
            "mpmath": "1.3.0",
            "packagesLock": "requirements.txt",
        },
        "asymptoticPowers": results["fittedExponentsTailFour"],
        "independentAsymptoticPowers": validation["independentPowersTailFour"],
        "evidenceMap": metadata["evidenceMap"],
        "data": [
            {**by_name["config.json"], "format": "json", "schema": "fixed target, roots, q sweep, annular weights, background, quadrature, and output configuration"},
            {**by_name["results.json"], "format": "json", "schema": "complete producer response, root, atom, jet-row, excursion, prefactor, fit, timing, and check ledger"},
            {**by_name["data.csv"], "format": "csv", "schema": "panel, series, q, scaled time, value, units, evidence class, event semantics, and fixed-target normalization"},
            {**by_name["data.json"], "format": "json", "schema": "lossless plot rows, field schema, fixed-target normalization, and claim boundary"},
            {**by_name["figure-data-metadata.json"], "format": "json", "schema": "input hashes, evidence map, row count, fixed-target normalization, and claim boundary"},
            {**by_name["validation.json"], "format": "json", "schema": "standalone 80-digit reconstruction, quadrature, prefactor, exponent, artifact, and output checks"},
            {**by_name["progress.ndjson"], "format": "ndjson", "schema": "timestamped producer, q-case, plotting, QA, and independent-validation progress events"},
            {**by_name["resource-log.ndjson"], "format": "ndjson", "schema": "timestamped wall time, process CPU, peak resident set, host load, and logical CPU snapshots"},
        ],
        "sourceData": [],
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
            "secondRootSemanticsInspected": True,
            "targetShellPrefactorsInspected": True,
        },
        "outputs": records,
    }
    (ROOT / "manifest.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    ledger = ASSETS + ["manifest.json"]
    (ROOT / "SHA256SUMS").write_text(
        "\n".join(f"{digest(ROOT / name)}  {name}" for name in ledger) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": status,
        "assets": len(ASSETS),
        "manifest": "manifest.json",
        "checksumLedger": "SHA256SUMS",
        "gitCommitHashes": {
            "sourceCommit": source_commit,
            "certificateCommit": certificate_commit,
        },
    }, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
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
