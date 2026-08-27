#!/usr/bin/env python3
"""Build the R0.72N archive manifest and SHA-256 ledger."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
from datetime import datetime
from typing import Any

from PIL import Image


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
FIGURE_COMMAND = (
    "python3 figures/r072n-dissipative-carrier/"
    "fig-r072n-dissipative-carrier/plot.py"
)
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
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def git_output(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=REPOSITORY,
        text=True,
        stderr=subprocess.DEVNULL,
    ).strip()


def asset(name: str, *, declared_dpi: int | None = None) -> dict[str, Any]:
    path = ROOT / name
    record: dict[str, Any] = {
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
        if declared_dpi is not None:
            record["dpi"] = declared_dpi
    return record


def package_version(distribution: str) -> str:
    try:
        return importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        return "not installed"


def physical_memory_gib() -> float:
    try:
        page_size = int(os.sysconf("SC_PAGE_SIZE"))
        page_count = int(os.sysconf("SC_PHYS_PAGES"))
        if page_size > 0 and page_count > 0:
            return round(page_size * page_count / (1024**3), 3)
    except (OSError, TypeError, ValueError):
        pass
    try:
        raw = subprocess.check_output(
            ["sysctl", "-n", "hw.memsize"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        memory_bytes = int(raw)
        if memory_bytes > 0:
            return round(memory_bytes / (1024**3), 3)
    except (OSError, subprocess.CalledProcessError, ValueError):
        pass
    raise RuntimeError("unable to determine physical memory for manifest")


def cpu_description() -> str:
    try:
        value = subprocess.check_output(
            ["sysctl", "-n", "machdep.cpu.brand_string"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        value = ""
    return value or platform.processor() or platform.machine()


def main(status: str) -> None:
    missing = [name for name in PACKAGE_ASSETS if not (ROOT / name).is_file()]
    if missing:
        raise FileNotFoundError(f"missing package assets: {missing}")
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    contract = json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))
    results = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
    validation = json.loads(
        (ROOT / "validation.json").read_text(encoding="utf-8")
    )
    if (
        results.get("status") != "built"
        or results.get("newPdeEvolution") is not False
        or results.get("pdeTimeStepping") is not False
        or results.get("finiteFitsPlotted") is not False
        or results.get("logarithmicCubicDiagnosticOnly") is not True
    ):
        raise RuntimeError(
            "results must describe a built, no-new-evolution, no-fit figure with a diagnostic logarithmic curve"
        )
    if validation.get("status") != "passed" or not validation.get("allPassed"):
        raise RuntimeError("validation must pass before manifest construction")
    visual = (
        os.environ.get("R072N_VISUAL_QA_INSPECTED", "").strip().lower()
        == "true"
    )
    if not visual:
        raise RuntimeError("R072N_VISUAL_QA_INSPECTED=true is required")

    head = git_output("rev-parse", "HEAD")
    if status == "formal":
        source_commit = os.environ.get("R072N_SOURCE_COMMIT", "").strip().lower()
        certificate_commit = (
            os.environ.get("R072N_CERTIFICATE_COMMIT", "").strip().lower()
        )
        dirty = (
            os.environ.get("R072N_DIRTY_AT_CERTIFIED_RUN", "").strip().lower()
        )
        if not FULL_SHA.fullmatch(source_commit) or not FULL_SHA.fullmatch(
            certificate_commit
        ):
            raise ValueError(
                "formal manifest requires full source and certificate commits"
            )
        for commit in (source_commit, certificate_commit):
            git_output("cat-file", "-e", f"{commit}^{{commit}}")
        if dirty != "false":
            raise RuntimeError("formal manifest requires dirtyAtCertifiedRun=false")
        git_record = {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": source_commit,
            "certificateCommit": certificate_commit,
            "dirtyAtCertifiedRun": False,
            "manifestBuildHead": head,
        }
    else:
        git_record = {
            "repository": "Kasifa/Kasifa.github.io",
            "commit": head,
            "dirty": bool(
                git_output("status", "--porcelain=v1", "--untracked-files=normal")
            ),
        }

    records = [asset(name) for name in PACKAGE_ASSETS]
    publication = config["publication"]
    public_assets = []
    for suffix in ("pdf", "svg", "png"):
        public = (
            REPOSITORY
            / publication["directory"]
            / f"{publication['stem']}.{suffix}"
        )
        master = ROOT / f"figure.{suffix}"
        if not public.is_file() or digest(public) != digest(master):
            raise RuntimeError(f"public {suffix} is absent or not byte-identical")
        public_assets.append(
            {
                "path": str(public.relative_to(REPOSITORY)),
                "bytes": public.stat().st_size,
                "sha256": digest(public),
                "byteIdenticalToMaster": True,
            }
        )

    source_data = []
    for relative, expected in sorted(results["sourceSha256"].items()):
        path = REPOSITORY / relative
        if not path.is_file() or digest(path) != expected:
            raise RuntimeError(f"source lineage changed: {relative}")
        source_data.append(
            {
                "location": "repository",
                "fileName": relative,
                "bytes": path.stat().st_size,
                "sha256": expected,
                "extractionCommand": FIGURE_COMMAND,
            }
        )

    data_schemas = {
        "config.json": (
            "R0.72N source paths, sigma grid, panel definitions, validation "
            "thresholds, figure dimensions, publication target, and palette"
        ),
        "contract.json": (
            "analytical question, rigorous claims, finite normalized proxy "
            "boundary, panel claims, and render policy"
        ),
        "results.json": (
            "source and output hashes, row and sigma counts, cross-route "
            "summary, runtime, and no-new-evolution declarations"
        ),
        "data.csv": (
            "panel, route, series, kind, x, y, source, pointer, and note"
        ),
        "validation.json": (
            "producer-side asset, formula, certificate, route, lineage, "
            "publication, claim-boundary, and visual-QA checks"
        ),
        "progress.ndjson": (
            "timestamped start, data extraction, and completion events"
        ),
        "resource-log.ndjson": (
            "timestamped wall time, peak resident set, and plotted-row count"
        ),
    }
    data_formats = {
        "config.json": "json",
        "contract.json": "json",
        "results.json": "json",
        "data.csv": "csv",
        "validation.json": "json",
        "progress.ndjson": "ndjson",
        "resource-log.ndjson": "ndjson",
    }

    payload = {
        "schemaVersion": "1.0",
        "figureId": "fig-r072n-dissipative-carrier",
        "release": "R0.72N",
        "status": status,
        "createdAt": datetime.now().astimezone().isoformat(timespec="seconds"),
        "analyticalQuestion": contract["analyticalQuestion"],
        "supportedClaim": contract["supportedTakeaway"],
        "claimBoundary": contract["claimBoundary"],
        "git": git_record,
        "computation": {
            "kind": "data-analysis",
            "configuration": (
                "ten sigma cases from 16 through 32768 on producer and "
                "independent dissipative routes; 241 exact moment-barrier "
                "samples, a two-endpoint scalar ceiling, and finite normalized "
                "moment, action, scalar-screen, and cubic diagnostics"
            ),
            "precision": "IEEE binary64 for plotted finite corroboration",
            "solver": (
                "no PDE solver rerun in the figure package; committed inputs "
                "come from a producer angular-FFT exact-mixing audit and an "
                "independent finite-real-chain fourth-order Taylor exponential audit"
            ),
            "formalCommand": "commands recorded in command.txt",
            "wallTimeSeconds": float(results["elapsedSeconds"]),
            "upstreamSolvers": (
                "producer angular FFT exact-mixing and independent "
                "finite-real-chain fourth-order Taylor exponential audits"
            ),
            "continuumProofLocation": config["analyticSource"],
            "figureRunsNewPdeEvolution": False,
            "pdeTimeStepping": False,
            "finiteFitsAreDiagnostics": True,
            "finiteFitPlotted": False,
            "logarithmicCubicTheorem": False,
            "randomSeed": None,
            "monitoring": {
                "enabled": True,
                "progressLog": "progress.ndjson",
                "resourceLog": "resource-log.ndjson",
                "trackedFields": [
                    "event",
                    "rows",
                    "elapsedSeconds",
                    "maxRssMb",
                ],
            },
        },
        "compute": {
            "host": platform.node() or "local host",
            "operatingSystem": platform.platform() or sys.platform,
            "cpu": cpu_description(),
            "memoryGiB": physical_memory_gib(),
            "logicalCpuCount": os.cpu_count(),
            "processes": 1,
            "threadsPerProcess": 1,
            "gpu": "not used by figure extraction",
            "dgx": "not used by figure extraction",
        },
        "environment": {
            "python": sys.version.split()[0],
            "numpy": package_version("numpy"),
            "matplotlib": package_version("matplotlib"),
            "pillow": package_version("pillow"),
            "pypdf": package_version("pypdf"),
            "packagesLock": "requirements.txt",
        },
        "data": [
            {
                "path": name,
                "bytes": (ROOT / name).stat().st_size,
                "sha256": digest(ROOT / name),
                "format": data_formats[name],
                "schema": data_schemas[name],
            }
            for name in (
                "config.json",
                "contract.json",
                "results.json",
                "data.csv",
                "validation.json",
                "progress.ndjson",
                "resource-log.ndjson",
            )
        ],
        "dataSummary": results["summary"],
        "sourceData": source_data,
        "figure": {
            "widthMillimetres": float(config["figure"]["widthMillimetres"]),
            "heightMillimetres": float(config["figure"]["heightMillimetres"]),
            "profile": "journal-default",
            "layout": "2x2",
            "script": "plot.py",
            "outputs": [
                asset(name)
                if name != "figure.png"
                else asset(
                    name,
                    declared_dpi=int(config["figure"]["pngDpi"]),
                )
                for name in ("figure.pdf", "figure.svg", "figure.png")
            ],
        },
        "caption": {"english": "caption.md"},
        "publication": {
            "directory": publication["directory"],
            "stem": publication["stem"],
            "publisher": "publish_assets.py",
            "publicCopiesComplete": True,
            "assets": public_assets,
        },
        "qa": {
            "status": "passed",
            "automaticCheckCount": validation["checkCount"],
            "automaticChecks": "validation.json",
            "visualInspectionExplicit": visual,
            "finalSizeInspected": visual,
            "grayscaleInspected": visual,
            "labelsAndLegendsInspected": visual,
            "theoremDiagnosticDistinctionInspected": visual,
            "scalesAndUnitsInspected": visual,
            "dataCrossChecked": True,
            "pdfRasterInspected": visual,
            "finalSizePreview": "qa-final-size.png",
            "grayscalePreview": "qa-grayscale.png",
            "pdfRenderPreview": "qa-pdf.png",
            "manualReport": "qa-report.md",
        },
        "outputs": records,
    }
    (ROOT / "manifest.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    names = sorted(PACKAGE_ASSETS + ["manifest.json"])
    (ROOT / "SHA256SUMS").write_text(
        "\n".join(f"{digest(ROOT / name)}  {name}" for name in names) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": status,
                "assets": len(records),
                "sourceData": len(source_data),
                "publicAssets": len(public_assets),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--status", choices=("candidate", "formal"), default="candidate"
    )
    args = parser.parse_args()
    main(args.status)
