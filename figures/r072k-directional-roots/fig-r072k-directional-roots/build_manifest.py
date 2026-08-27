#!/usr/bin/env python3
"""Build the R0.72K formal manifest and SHA-256 ledger after validation."""

from __future__ import annotations

import argparse
import hashlib
from importlib import metadata as package_metadata
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
from zoneinfo import ZoneInfo

from PIL import Image


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
TIMEZONE = ZoneInfo("Asia/Shanghai")
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
PACKAGE_ASSETS = [
    "README.md",
    "caption.md",
    "figure-contract.md",
    "contract.json",
    "config.json",
    "command.txt",
    "requirements.txt",
    "plot.py",
    "qa_images.py",
    "publish_assets.py",
    "validate.py",
    "build_manifest.py",
    "environment.txt",
    "progress.ndjson",
    "resource-log.ndjson",
    "data.csv",
    "results.json",
    "validation.json",
    "qa-report.md",
    "figure.pdf",
    "figure.svg",
    "figure.png",
    "qa-final-size.png",
    "qa-grayscale.png",
    "qa-pdf.png",
]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


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
            record["dpiMetadata"] = [
                float(value) for value in image.info.get("dpi", (0.0, 0.0))
            ]
    return record


def git_output(*arguments: str) -> str:
    return subprocess.check_output(
        ["git", *arguments],
        cwd=REPOSITORY,
        text=True,
        stderr=subprocess.DEVNULL,
    ).strip()


def validate_commit(value: str | None, label: str) -> str:
    normalized = str(value or "").strip().lower()
    if not FULL_SHA.fullmatch(normalized):
        raise ValueError(f"{label} must be an explicit full 40-character SHA")
    try:
        git_output("cat-file", "-e", f"{normalized}^{{commit}}")
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise ValueError(f"{label} is not a locally resolvable commit") from exc
    return normalized


def parse_boolean(value: str | None, label: str) -> bool | None:
    if value is None:
        return None
    normalized = value.strip().lower()
    if normalized not in {"true", "false"}:
        raise ValueError(f"{label} must be true or false")
    return normalized == "true"


def runtime_dirty() -> bool:
    return bool(git_output("status", "--porcelain=v1", "--untracked-files=normal"))


def package_version(distribution: str) -> str:
    try:
        return package_metadata.version(distribution)
    except package_metadata.PackageNotFoundError:
        return "unavailable"


def sysctl_value(name: str) -> str | None:
    try:
        value = subprocess.check_output(
            ["sysctl", "-n", name], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    return value or None


def memory_gib() -> float:
    raw = sysctl_value("hw.memsize")
    if raw is not None and raw.isdigit():
        return round(int(raw) / 1024**3, 2)
    if hasattr(os, "sysconf"):
        try:
            pages = int(os.sysconf("SC_PHYS_PAGES"))
            page_size = int(os.sysconf("SC_PAGE_SIZE"))
            return round(pages * page_size / 1024**3, 2)
        except (OSError, ValueError):
            pass
    return -1.0


def data_record(
    records: dict[str, dict[str, object]],
    name: str,
    file_format: str,
    schema: str,
) -> dict[str, object]:
    return {**records[name], "format": file_format, "schema": schema}


def main(
    *,
    status: str,
    source_commit_value: str | None,
    certificate_commit_value: str | None,
    dirty_value: str | None,
    visual_qa_value: str | None,
) -> None:
    missing = [name for name in PACKAGE_ASSETS if not (ROOT / name).is_file()]
    if missing:
        raise FileNotFoundError(f"missing package assets: {missing}")

    source_commit = validate_commit(source_commit_value, "sourceCommit")
    certificate_commit = validate_commit(
        certificate_commit_value, "certificateCommit"
    )
    explicit_dirty = parse_boolean(dirty_value, "dirtyAtCertifiedRun")
    if explicit_dirty is None:
        dirty = runtime_dirty()
        dirty_evidence = "runtime git status --porcelain=v1 --untracked-files=normal"
    else:
        dirty = explicit_dirty
        dirty_evidence = "explicit command-line or R072K_DIRTY_AT_CERTIFIED_RUN"
    visual_qa = parse_boolean(visual_qa_value, "visualQaInspected")
    visual_qa = False if visual_qa is None else visual_qa

    if status == "formal" and dirty:
        raise RuntimeError(
            "formal manifest refused: dirtyAtCertifiedRun is true"
        )
    if status == "formal" and not visual_qa:
        raise RuntimeError(
            "formal manifest refused: final-size, grayscale, and PDF-raster "
            "surfaces must be explicitly inspected"
        )

    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    contract = json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))
    results = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
    validation = json.loads(
        (ROOT / "validation.json").read_text(encoding="utf-8")
    )
    if not validation.get("allPassed") or validation.get("status") != "passed":
        raise RuntimeError("validation.json must pass before manifest construction")
    if results.get("status") != "built" or results.get("newPdeEvolution") is not False:
        raise RuntimeError("results.json does not describe the sealed no-new-PDE build")

    records_list = [asset_record(name) for name in PACKAGE_ASSETS]
    records = {str(record["path"]): record for record in records_list}
    source_hashes = results["sourceSha256"]
    source_data = []
    for relative, expected_hash in sorted(source_hashes.items()):
        path = (REPOSITORY / relative).resolve()
        repository = REPOSITORY.resolve()
        if path != repository and repository not in path.parents:
            raise ValueError(f"source path escapes repository: {relative}")
        if not path.is_file() or digest(path) != expected_hash:
            raise RuntimeError(f"source lineage changed after figure build: {relative}")
        source_data.append(
            {
                "location": "repository",
                "fileName": relative,
                "bytes": path.stat().st_size,
                "sha256": expected_hash,
                "extractionCommand": (
                    "read-only ingestion by plot.py; no PDE time evolution"
                ),
            }
        )

    public_dir = (REPOSITORY / config["publication"]["directory"]).resolve()
    stem = config["publication"]["stem"]
    public_assets = []
    for suffix in ("pdf", "svg", "png"):
        public_path = public_dir / f"{stem}.{suffix}"
        if not public_path.is_file():
            raise FileNotFoundError(public_path)
        master_path = ROOT / f"figure.{suffix}"
        if digest(public_path) != digest(master_path):
            raise RuntimeError(f"public {suffix} is not byte-identical to master")
        public_assets.append(
            {
                "path": str(public_path.relative_to(REPOSITORY)),
                "bytes": public_path.stat().st_size,
                "sha256": digest(public_path),
                "byteIdenticalToMaster": True,
            }
        )

    cpu = (
        sysctl_value("machdep.cpu.brand_string")
        or platform.processor()
        or platform.machine()
        or "unavailable"
    )
    data = [
        data_record(
            records,
            "config.json",
            "json",
            "figure geometry, source-certificate paths, publication path, expected grids, tolerances, and palette",
        ),
        data_record(
            records,
            "contract.json",
            "json",
            "analytic claims, finite diagnostics, and claim boundary",
        ),
        data_record(
            records,
            "results.json",
            "json",
            "source/output hashes, finite summary, timing, resource use, and no-new-PDE declaration",
        ),
        data_record(
            records,
            "data.csv",
            "csv",
            "panel,route,series,x,y,rawValue,auxiliary,source,pointer",
        ),
        data_record(
            records,
            "validation.json",
            "json",
            "certificate, lineage, exact-ratio, scaling, geometry, raster, caption, and publication checks",
        ),
        data_record(
            records,
            "progress.ndjson",
            "ndjson",
            "timestamped figure-build stages and output hashes",
        ),
        data_record(
            records,
            "resource-log.ndjson",
            "ndjson",
            "figure-build wall time, peak resident set, and row count",
        ),
    ]

    payload: dict[str, Any] = {
        "schemaVersion": "1.0",
        "release": "R0.72K",
        "figureId": "fig-r072k-directional-roots",
        "status": status,
        "createdAt": datetime.now(TIMEZONE).isoformat(timespec="seconds"),
        "analyticalQuestion": (
            "Can directional projection replace a false complex Rolle step, "
            "and does the resulting complete common-band root ledger remain "
            "below the physical critical-log payment?"
        ),
        "supportedClaim": " ".join(contract["analyticClaims"]),
        "claimBoundary": contract["claimBoundary"],
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": source_commit,
            "certificateCommit": certificate_commit,
            "dirtyAtCertifiedRun": dirty,
            "dirtyEvidence": dirty_evidence,
            "manifestBuildHead": git_output("rev-parse", "HEAD"),
        },
        "computation": {
            "kind": "data-analysis",
            "configuration": (
                "analytic complex trajectory and exact rational sharpness "
                "cases combined with separately sealed R0.72K producer and "
                "independent transforms of archived R0.72J finite evolutions"
            ),
            "precision": (
                "exact rational sharpness arithmetic at certificate stage; "
                "IEEE binary64 plotting of sealed finite certificate values"
            ),
            "solver": (
                "no solver and no PDE time stepping in the figure build; "
                "plot.py performs deterministic certificate ingestion"
            ),
            "formalCommand": "commands recorded in command.txt",
            "wallTimeSeconds": float(results["elapsedSeconds"]),
            "pdeTimeStepping": False,
            "newPdeEvolution": False,
            "intervalArithmetic": False,
            "finiteFitsAreDiagnostics": True,
            "randomSeed": None,
            "continuumProofLocation": "research/r072k_report-source.md",
            "monitoring": {
                "enabled": True,
                "reportIntervalSeconds": 0.0,
                "trackedFields": [
                    "event",
                    "rows",
                    "elapsedSeconds",
                    "maxRssMb",
                    "outputs",
                ],
                "progressLog": "progress.ndjson",
                "resourceLog": "resource-log.ndjson",
            },
        },
        "compute": {
            "host": socket.gethostname() or "unavailable",
            "operatingSystem": platform.platform(),
            "cpu": cpu,
            "memoryGiB": memory_gib(),
            "processes": 1,
            "threadsPerProcess": 1,
            "logicalCpuCount": os.cpu_count() or 1,
            "gpu": "not used",
            "dgx": "not used",
        },
        "environment": {
            "python": platform.python_version(),
            "numpy": package_version("numpy"),
            "matplotlib": package_version("matplotlib"),
            "pillow": package_version("Pillow"),
            "pypdf": package_version("pypdf"),
            "packagesLock": "requirements.txt",
        },
        "data": data,
        "sourceData": source_data,
        "dataSummary": results["summary"],
        "figure": {
            "profile": "journal-default",
            "widthMillimetres": float(config["figure"]["widthMillimetres"]),
            "heightMillimetres": float(config["figure"]["heightMillimetres"]),
            "script": "plot.py",
            "outputs": [
                records["figure.pdf"],
                records["figure.svg"],
                {**records["figure.png"], "dpi": 600},
            ],
        },
        "caption": {"english": "caption.md"},
        "qa": {
            "automaticChecks": "validation.json",
            "automaticCheckCount": validation["requiredCount"],
            "manualReport": "qa-report.md",
            "finalSizePreview": "qa-final-size.png",
            "grayscalePreview": "qa-grayscale.png",
            "pdfRenderPreview": "qa-pdf.png",
            "status": "passed",
            "visualInspectionExplicit": visual_qa,
            "finalSizeInspected": visual_qa,
            "grayscaleInspected": visual_qa,
            "pdfRasterInspected": visual_qa,
            "labelsAndLegendsInspected": visual_qa,
            "scalesAndUnitsInspected": visual_qa,
            "dataCrossChecked": True,
        },
        "publication": {
            "directory": config["publication"]["directory"],
            "stem": stem,
            "publisher": "publish_assets.py",
            "publicCopiesComplete": True,
            "assets": public_assets,
        },
        "outputs": records_list,
    }

    (ROOT / "manifest.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    ledger = PACKAGE_ASSETS + ["manifest.json"]
    (ROOT / "SHA256SUMS").write_text(
        "\n".join(f"{digest(ROOT / name)}  {name}" for name in ledger) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "figureId": payload["figureId"],
                "status": status,
                "assets": len(records_list),
                "sourceCommit": source_commit,
                "certificateCommit": certificate_commit,
                "dirtyAtCertifiedRun": dirty,
                "dirtyEvidence": dirty_evidence,
                "visualQaInspected": visual_qa,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--status",
        choices=("draft", "formal"),
        default=os.environ.get("R072K_MANIFEST_STATUS", "draft"),
    )
    parser.add_argument(
        "--source-commit", default=os.environ.get("R072K_SOURCE_COMMIT")
    )
    parser.add_argument(
        "--certificate-commit",
        default=os.environ.get("R072K_CERTIFICATE_COMMIT"),
    )
    parser.add_argument(
        "--dirty-at-certified-run",
        choices=("true", "false"),
        default=os.environ.get("R072K_DIRTY_AT_CERTIFIED_RUN"),
    )
    parser.add_argument(
        "--visual-qa-inspected",
        choices=("true", "false"),
        default=os.environ.get("R072K_VISUAL_QA_INSPECTED"),
    )
    arguments = parser.parse_args()
    main(
        status=arguments.status,
        source_commit_value=arguments.source_commit,
        certificate_commit_value=arguments.certificate_commit,
        dirty_value=arguments.dirty_at_certified_run,
        visual_qa_value=arguments.visual_qa_inspected,
    )
