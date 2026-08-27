#!/usr/bin/env python3
"""Build the R0.72M archive manifest and SHA-256 ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from datetime import datetime
from typing import Any

from PIL import Image


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
PACKAGE_ASSETS = [
    "README.md", "caption.md", "figure-contract.md", "contract.json", "config.json", "command.txt",
    "requirements.txt", "plot.py", "qa_images.py", "publish_assets.py", "validate.py", "build_manifest.py",
    "environment.txt", "progress.ndjson", "resource-log.ndjson", "data.csv", "results.json",
    "validation.json", "qa-report.md", "figure.pdf", "figure.svg", "figure.png",
    "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png",
]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def git_output(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPOSITORY, text=True, stderr=subprocess.DEVNULL).strip()


def asset(name: str) -> dict[str, Any]:
    path = ROOT / name
    record: dict[str, Any] = {"path": name, "bytes": path.stat().st_size, "sha256": digest(path)}
    if path.suffix.lower() == ".png":
        with Image.open(path) as image:
            record["pixels"] = [image.width, image.height]
            record["dpiMetadata"] = [float(value) for value in image.info.get("dpi", (0.0, 0.0))]
    return record


def main(status: str) -> None:
    missing = [name for name in PACKAGE_ASSETS if not (ROOT / name).is_file()]
    if missing:
        raise FileNotFoundError(f"missing package assets: {missing}")
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    contract = json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))
    results = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
    validation = json.loads((ROOT / "validation.json").read_text(encoding="utf-8"))
    if results.get("status") != "built" or results.get("newPdeEvolution") is not False:
        raise RuntimeError("results must describe a built no-new-PDE figure")
    if validation.get("status") != "passed" or not validation.get("allPassed"):
        raise RuntimeError("validation must pass before manifest construction")
    visual = os.environ.get("R072M_VISUAL_QA_INSPECTED", "").strip().lower() == "true"
    if not visual:
        raise RuntimeError("R072M_VISUAL_QA_INSPECTED=true is required")
    head = git_output("rev-parse", "HEAD")
    if status == "formal":
        source_commit = os.environ.get("R072M_SOURCE_COMMIT", "").strip().lower()
        certificate_commit = os.environ.get("R072M_CERTIFICATE_COMMIT", "").strip().lower()
        dirty = os.environ.get("R072M_DIRTY_AT_CERTIFIED_RUN", "").strip().lower()
        if not FULL_SHA.fullmatch(source_commit) or not FULL_SHA.fullmatch(certificate_commit):
            raise ValueError("formal manifest requires full source and certificate commits")
        for commit in (source_commit, certificate_commit):
            git_output("cat-file", "-e", f"{commit}^{{commit}}")
        if dirty != "false":
            raise RuntimeError("formal manifest requires dirtyAtCertifiedRun=false")
        git_record = {"repository": "Kasifa/Kasifa.github.io", "sourceCommit": source_commit, "certificateCommit": certificate_commit, "dirtyAtCertifiedRun": False, "manifestBuildHead": head}
    else:
        git_record = {"repository": "Kasifa/Kasifa.github.io", "commit": head, "dirty": bool(git_output("status", "--porcelain=v1", "--untracked-files=normal"))}
    records = [asset(name) for name in PACKAGE_ASSETS]
    publication = config["publication"]
    public_assets = []
    for suffix in ("pdf", "svg", "png"):
        public = REPOSITORY / publication["directory"] / f"{publication['stem']}.{suffix}"
        master = ROOT / f"figure.{suffix}"
        if not public.is_file() or digest(public) != digest(master):
            raise RuntimeError(f"public {suffix} is absent or not byte-identical")
        public_assets.append({"path": str(public.relative_to(REPOSITORY)), "bytes": public.stat().st_size, "sha256": digest(public), "byteIdenticalToMaster": True})
    source_data = []
    for relative, expected in sorted(results["sourceSha256"].items()):
        path = REPOSITORY / relative
        if not path.is_file() or digest(path) != expected:
            raise RuntimeError(f"source lineage changed: {relative}")
        source_data.append({"location": "repository", "fileName": relative, "bytes": path.stat().st_size, "sha256": expected})
    payload = {
        "schemaVersion": "1.0", "figureId": "fig-r072m-danger-window", "release": "R0.72M",
        "status": status, "createdAt": datetime.now().astimezone().isoformat(timespec="seconds"),
        "analyticalQuestion": "Where can the inherited scalar cubic term be large, and where does the exact one-carrier full-lattice phase-mixing reference lie relative to that interval?",
        "supportedClaim": "The scalar danger set is an exact middle interval. The full-lattice zero-diffusion reference has Bessel solution, sigma-squared gradient moment, lifted action of order sigma^(4/3) log sigma, and frozen true-cubic coefficient 16/pi^2; at fixed geometry it lies in the action-poor branch.",
        "claimBoundary": contract["claimBoundary"], "git": git_record,
        "computation": {"kind": "analytic-formula sampling plus finite certificate visualization", "precision": "IEEE binary64 for plotted corroboration", "solver": "producer FFT splitting and independent finite-chain Cayley splitting only in Panel D", "continuumProofLocation": "research/r072m_report-source.md", "finiteFitsAreDiagnostics": True, "newPdeEvolution": False, "pdeTimeStepping": False, "randomSeed": None, "monitoring": {"enabled": True, "progressLog": "progress.ndjson", "resourceLog": "resource-log.ndjson"}},
        "data": [{"path": name, "bytes": (ROOT / name).stat().st_size, "sha256": digest(ROOT / name)} for name in ("config.json", "contract.json", "results.json", "data.csv", "validation.json", "progress.ndjson", "resource-log.ndjson")],
        "dataSummary": results["summary"], "sourceData": source_data,
        "figure": {"widthMillimetres": float(config["figure"]["widthMillimetres"]), "heightMillimetres": float(config["figure"]["heightMillimetres"]), "profile": "journal-default", "script": "plot.py", "outputs": [asset(name) for name in ("figure.pdf", "figure.svg", "figure.png")]},
        "caption": {"english": "caption.md"},
        "publication": {"directory": publication["directory"], "stem": publication["stem"], "publisher": "publish_assets.py", "publicCopiesComplete": True, "assets": public_assets},
        "qa": {"status": "passed", "automaticCheckCount": validation["checkCount"], "automaticChecks": "validation.json", "visualInspectionExplicit": visual, "finalSizeInspected": visual, "grayscaleInspected": visual, "labelsAndLegendsInspected": visual, "scalesAndUnitsInspected": visual, "dataCrossChecked": True, "pdfRasterInspected": visual, "finalSizePreview": "qa-final-size.png", "grayscalePreview": "qa-grayscale.png", "pdfRenderPreview": "qa-pdf.png", "manualReport": "qa-report.md"},
        "outputs": records,
    }
    (ROOT / "manifest.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    names = PACKAGE_ASSETS + ["manifest.json"]
    (ROOT / "SHA256SUMS").write_text("\n".join(f"{digest(ROOT / name)}  {name}" for name in names) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "assets": len(records), "sourceData": len(source_data), "publicAssets": len(public_assets)}, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", choices=("candidate", "formal"), default="candidate")
    args = parser.parse_args()
    main(args.status)
