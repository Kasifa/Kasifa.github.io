#!/usr/bin/env python3
"""Build the R0.72L archive manifest and SHA-256 ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import socket
import subprocess
import sys
from datetime import datetime
from typing import Any

from PIL import Image


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
PACKAGE_ASSETS = [
    "README.md", "caption.md", "figure-contract.md", "contract.json", "config.json", "command.txt", "requirements.txt",
    "plot.py", "qa_images.py", "publish_assets.py", "validate.py", "build_manifest.py", "environment.txt",
    "progress.ndjson", "resource-log.ndjson", "data.csv", "results.json", "validation.json", "qa-report.md",
    "figure.pdf", "figure.svg", "figure.png", "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png",
]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def git_output(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPOSITORY, text=True, stderr=subprocess.DEVNULL).strip()


def parse_bool(value: str | None, label: str) -> bool | None:
    if value is None:
        return None
    normalized = value.strip().lower()
    if normalized not in {"true", "false"}:
        raise ValueError(f"{label} must be true or false")
    return normalized == "true"


def asset(name: str) -> dict[str, Any]:
    path = ROOT / name
    record: dict[str, Any] = {"path": name, "bytes": path.stat().st_size, "sha256": digest(path)}
    if path.suffix.lower() == ".png":
        with Image.open(path) as image:
            record["pixels"] = [image.width, image.height]
            record["dpiMetadata"] = [float(value) for value in image.info.get("dpi", (0.0, 0.0))]
    return record


def memory_gib() -> float:
    try:
        raw = subprocess.check_output(["sysctl", "-n", "hw.memsize"], text=True, stderr=subprocess.DEVNULL).strip()
        return round(int(raw) / 1024**3, 2)
    except Exception:
        return -1.0


def main(status: str) -> None:
    missing = [name for name in PACKAGE_ASSETS if not (ROOT / name).is_file()]
    if missing:
        raise FileNotFoundError(f"missing package assets: {missing}")
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    contract = json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))
    results = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
    validation = json.loads((ROOT / "validation.json").read_text(encoding="utf-8"))
    if results.get("status") != "built" or results.get("newPdeEvolution") is not False:
        raise RuntimeError("results.json must describe a built no-new-PDE figure")
    if validation.get("status") != "passed" or not validation.get("allPassed"):
        raise RuntimeError("validation.json must pass before manifest construction")
    visual = os.environ.get("R072L_VISUAL_QA_INSPECTED", "").strip().lower() == "true"
    if not visual:
        raise RuntimeError("R072L_VISUAL_QA_INSPECTED=true is required")

    head = git_output("rev-parse", "HEAD")
    dirty_runtime = bool(git_output("status", "--porcelain=v1", "--untracked-files=normal"))
    if status == "formal":
        source_commit = os.environ.get("R072L_SOURCE_COMMIT", "").strip().lower()
        certificate_commit = os.environ.get("R072L_CERTIFICATE_COMMIT", "").strip().lower()
        dirty = parse_bool(os.environ.get("R072L_DIRTY_AT_CERTIFIED_RUN"), "R072L_DIRTY_AT_CERTIFIED_RUN")
        if not FULL_SHA.fullmatch(source_commit) or not FULL_SHA.fullmatch(certificate_commit):
            raise ValueError("formal manifest requires full R072L_SOURCE_COMMIT and R072L_CERTIFICATE_COMMIT values")
        for commit in (source_commit, certificate_commit):
            git_output("cat-file", "-e", f"{commit}^{{commit}}")
        if dirty is not False:
            raise RuntimeError("formal manifest requires R072L_DIRTY_AT_CERTIFIED_RUN=false")
        git_record = {"repository": "Kasifa/Kasifa.github.io", "sourceCommit": source_commit, "certificateCommit": certificate_commit, "dirtyAtCertifiedRun": False, "manifestBuildHead": head}
    else:
        git_record = {"repository": "Kasifa/Kasifa.github.io", "commit": head, "dirty": dirty_runtime}

    records = [asset(name) for name in PACKAGE_ASSETS]
    by_name = {record["path"]: record for record in records}
    source_data = []
    for relative, expected in sorted(results["sourceSha256"].items()):
        path = REPOSITORY / relative
        if not path.is_file() or digest(path) != expected:
            raise RuntimeError(f"source lineage changed after figure build: {relative}")
        source_data.append({"location": "repository", "fileName": relative, "bytes": path.stat().st_size, "sha256": expected, "extractionCommand": "analytic report equations sampled by plot.py; projected ODE integrated only for finite diagnostics"})

    publication = config["publication"]
    public_assets = []
    for suffix in ("pdf", "svg", "png"):
        path = REPOSITORY / publication["directory"] / f"{publication['stem']}.{suffix}"
        master = ROOT / f"figure.{suffix}"
        if not path.is_file() or digest(path) != digest(master):
            raise RuntimeError(f"public {suffix} is absent or not byte-identical")
        public_assets.append({"path": str(path.relative_to(REPOSITORY)), "bytes": path.stat().st_size, "sha256": digest(path), "byteIdenticalToMaster": True})

    figure_outputs = []
    for name in ("figure.pdf", "figure.svg", "figure.png"):
        record = dict(by_name[name])
        if name.endswith(".png"):
            record["dpi"] = 600
        figure_outputs.append(record)
    data_names = ("config.json", "contract.json", "results.json", "data.csv", "validation.json", "progress.ndjson", "resource-log.ndjson")
    schemas = {
        "config.json": "figure geometry, panel grids, publication path, and palette",
        "contract.json": "analytic claims, finite diagnostics, and claim boundary",
        "results.json": "source/output hashes, finite summaries, timing, and no-new-PDE declaration",
        "data.csv": "panel,route,series,x,y,rawValue,auxiliary,source,pointer,note",
        "validation.json": "formula, geometry, raster, lineage, leakage, boundary, and publication checks",
        "progress.ndjson": "timestamped build stages and output hashes",
        "resource-log.ndjson": "build wall time, peak resident set, and row count",
    }
    formats = {"data.csv": "csv", "progress.ndjson": "ndjson", "resource-log.ndjson": "ndjson"}
    data = [{**by_name[name], "format": formats.get(name, "json"), "schema": schemas[name]} for name in data_names]
    env_lines = dict(line.split("=", 1) for line in (ROOT / "environment.txt").read_text(encoding="utf-8").splitlines() if "=" in line)
    payload = {
        "schemaVersion": "1.0",
        "figureId": "fig-r072l-strong-window",
        "release": "R0.72L",
        "status": status,
        "createdAt": datetime.now().astimezone().isoformat(timespec="seconds"),
        "analyticalQuestion": "How far does the enstrophy-aware common-band root ledger close beyond perturbative exposure, and why cannot a three-mode projected divergence decide the full lattice?",
        "supportedClaim": "For the declared corrected common-band family, the normalized complete-root ledger is uniformly bounded in the growing moderate strong-coupling window epsilon lesssim p^(2/3) R^(2/3) (1+log R), and decays under the corresponding little-o relation. A nonzero real-carrier convolution has no nonzero finite-support invariant subsystem; the first omitted-shell norm ratio is exactly 1/sqrt(2).",
        "claimBoundary": contract["claimBoundary"],
        "git": git_record,
        "computation": {
            "kind": "data-analysis",
            "configuration": "analytic equation sampling plus seven deterministic exact-projected-ODE RK4 cases; no PDE evolution",
            "precision": "IEEE binary64 for presentation sampling and projected-ODE diagnostics; exact symbolic leakage ratio from report equations",
            "solver": "deterministic fixed-step RK4 for the projected ODE only; analytic formulas for all other panels",
            "formalCommand": "commands recorded in command.txt",
            "wallTimeSeconds": results["elapsedSeconds"],
            "continuumProofLocation": "research/r072l_report-source.md",
            "finiteFitsAreDiagnostics": True,
            "newPdeEvolution": False,
            "pdeTimeStepping": False,
            "randomSeed": None,
            "monitoring": {"enabled": True, "reportIntervalSeconds": 0.0, "progressLog": "progress.ndjson", "resourceLog": "resource-log.ndjson", "trackedFields": ["event", "rows", "elapsedSeconds", "maxRssMb", "outputs"]},
        },
        "compute": {"host": socket.gethostname(), "operatingSystem": platform.platform(), "cpu": platform.processor() or platform.machine(), "memoryGiB": memory_gib(), "processes": 1, "threadsPerProcess": 1, "logicalCpuCount": os.cpu_count(), "gpu": "not used", "dgx": "not used"},
        "environment": {"python": env_lines.get("python", sys.version).split()[0], "matplotlib": env_lines.get("matplotlib", "unavailable"), "numpy": env_lines.get("numpy", "unavailable"), "pillow": "12.3.0", "pypdf": "6.10.0", "packagesLock": "requirements.txt"},
        "data": data,
        "dataSummary": results["summary"],
        "sourceData": source_data,
        "figure": {"widthMillimetres": float(config["figure"]["widthMillimetres"]), "heightMillimetres": float(config["figure"]["heightMillimetres"]), "profile": "journal-default", "script": "plot.py", "outputs": figure_outputs},
        "caption": {"english": "caption.md"},
        "publication": {"directory": publication["directory"], "stem": publication["stem"], "publisher": "publish_assets.py", "publicCopiesComplete": True, "assets": public_assets},
        "qa": {"status": "passed", "automaticCheckCount": validation["checkCount"], "automaticChecks": "validation.json", "visualInspectionExplicit": visual, "finalSizeInspected": visual, "grayscaleInspected": visual, "labelsAndLegendsInspected": visual, "scalesAndUnitsInspected": visual, "dataCrossChecked": True, "pdfRasterInspected": visual, "finalSizePreview": "qa-final-size.png", "grayscalePreview": "qa-grayscale.png", "pdfRenderPreview": "qa-pdf.png", "manualReport": "qa-report.md"},
        "outputs": records,
    }
    (ROOT / "manifest.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    checksum_names = PACKAGE_ASSETS + ["manifest.json"]
    (ROOT / "SHA256SUMS").write_text("\n".join(f"{digest(ROOT / name)}  {name}" for name in checksum_names) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "assets": len(records), "sourceData": len(source_data), "publicAssets": len(public_assets)}, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--status", choices=("candidate", "formal"), default="candidate")
    args = parser.parse_args()
    main(args.status)
