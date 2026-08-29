#!/usr/bin/env python3
"""Fail-closed structural, numerical, and rendering checks for Figure R0.73F."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def configure_dependencies(path: str | None) -> None:
    if path:
        sys.path.insert(0, path)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def record(path: Path, relative_to: Path = ROOT) -> dict[str, Any]:
    return {
        "path": str(path.relative_to(relative_to)),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def make_qa_images(Image: Any, ImageOps: Any) -> None:
    with Image.open(HERE / "figure.png") as source:
        rgb = source.convert("RGB")
        final = rgb.resize((1780, 1320), Image.Resampling.LANCZOS)
        final.save(HERE / "qa-final-size.png", dpi=(254, 254))
        gray = ImageOps.grayscale(final)
        gray.save(HERE / "qa-grayscale.png", dpi=(254, 254))

    executable = shutil.which("pdftoppm")
    require(executable is not None, "pdftoppm is required for PDF raster QA")
    with tempfile.TemporaryDirectory(prefix="r073f-pdf-qa-") as temp:
        prefix = Path(temp) / "page"
        subprocess.run(
            [executable, "-png", "-r", "180", "-singlefile",
             str(HERE / "figure.pdf"), str(prefix)],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        with Image.open(Path(str(prefix) + ".png")) as rendered:
            rendered.convert("RGB").save(HERE / "qa-pdf.png", dpi=(180, 180))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default=None)
    parser.add_argument("--qa-status", choices=("pending", "passed"), default="pending")
    parser.add_argument("--qa-note", default="")
    args = parser.parse_args()
    configure_dependencies(args.deps)

    from PIL import Image, ImageOps
    from pypdf import PdfReader

    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    results = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
    summary = json.loads((ROOT / config["inputs"]["summary"]).read_text(encoding="utf-8"))
    independent = json.loads((ROOT / config["inputs"]["independent"]).read_text(encoding="utf-8"))

    for item in results["inputs"]:
        path = ROOT / item["path"]
        require(path.is_file(), "missing input: " + item["path"])
        require(path.stat().st_size == item["bytes"], "input size changed: " + item["path"])
        require(sha256(path) == item["sha256"], "input hash changed: " + item["path"])
    require(results["configBinding"]["sha256"] == sha256(HERE / "config.json"),
            "figure config changed after rendering")
    require(summary["allPrimaryChecksPass"] is True, "primary checks failed")
    require(independent["allChecksPass"] is True, "independent checks failed")
    require(summary["diagnosticEndpointIsCertifiedD0"] is False,
            "diagnostic endpoint escaped its claim boundary")

    boundary = results["claimBoundary"]
    require(boundary["formalFiniteDiagnosticFigure"] is True,
            "finite diagnostic figure declaration missing")
    for key, value in boundary.items():
        if key != "formalFiniteDiagnosticFigure":
            require(value is False, "escaped claim boundary: " + key)

    for name in ("figure.pdf", "figure.svg", "figure.png"):
        require((HERE / name).is_file(), "missing master: " + name)
    reader = PdfReader(HERE / "figure.pdf")
    require(len(reader.pages) == 1, "PDF must contain exactly one page")
    page = reader.pages[0]
    points = [float(page.mediabox.width), float(page.mediabox.height)]
    expected = [config["widthMillimetres"] / 25.4 * 72,
                config["heightMillimetres"] / 25.4 * 72]
    require(max(abs(a - b) for a, b in zip(points, expected)) < 0.8,
            "PDF physical dimensions changed")
    pdf_text = page.extract_text() or ""
    for token in ("Fixed-window finite gains", "Numerical cross-checks",
                  "Exact nonnormal prefactor trap", "Exact rotating-edge trap",
                  "not certified"):
        require(token in pdf_text, "PDF text missing: " + token)

    with Image.open(HERE / "figure.png") as image:
        pixels = list(image.size)
        dpi = image.info.get("dpi", (0, 0))
        require(abs(pixels[0] - 4205) <= 2 and abs(pixels[1] - 3118) <= 2,
                "PNG pixel dimensions changed")
        require(min(dpi) > 599 and max(dpi) < 601, "PNG is not tagged at 600 dpi")
    svg = (HERE / "figure.svg").read_text(encoding="utf-8")
    require("<image" not in svg, "SVG unexpectedly contains a raster image")
    for token in ("Fixed-window finite gains", "Exact rotating-edge trap"):
        require(token in svg, "SVG text missing: " + token)

    require(max(results["panelB"]["independentMaximumRateDifference"]) < 5e-5,
            "independent normalized-rate discrepancy exceeds declared threshold")
    require(summary["finiteSentinels"]["maximumDriftRatio"] <= 1.0 + 2e-12,
            "finite sampled drift exceeds the analytic comparison bound")
    require(summary["finiteSentinels"]["minimumR073BUpperSlack"] >= -2e-9,
            "R0.73B five-sixteenths sentinel failed")
    require(abs(results["panelD"]["exactBranchIntegral"] + 0.25) < 1e-15,
            "rotating counterexample exact integral changed")

    make_qa_images(Image, ImageOps)
    qa_note = args.qa_note.strip()
    if args.qa_status == "passed":
        require(bool(qa_note), "a passed QA requires --qa-note")
    qa = {
        "status": args.qa_status,
        "visualInspectionExplicit": args.qa_status == "passed",
        "finalSizeInspected": args.qa_status == "passed",
        "grayscaleInspected": args.qa_status == "passed",
        "labelsAndLegendsInspected": args.qa_status == "passed",
        "scalesAndUnitsInspected": args.qa_status == "passed",
        "dataCrossChecked": args.qa_status == "passed",
        "finalSize": "qa-final-size.png",
        "grayscale": "qa-grayscale.png",
        "pdfRaster": "qa-pdf.png",
        "report": "qa-report.md",
        "note": qa_note or "awaiting explicit visual inspection",
    }
    report_text = (
        "# R0.73F figure QA report\n\n"
        f"Status: **{args.qa_status}**.\n\n"
        f"Inspection note: {qa['note']}.\n\n"
        "The validator confirmed one-page PDF geometry, 600 dpi PNG metadata, "
        "vector SVG text, source hashes, finite numerical sentinels, and the "
        "fail-closed claim boundary. Visual inspection is recorded only when "
        "the status is `passed`. This QA certifies presentation integrity, not "
        "a continuum theorem.\n"
    )
    (HERE / "qa-report.md").write_text(report_text, encoding="utf-8")

    checks = {
        "inputHashesPassed": True,
        "primaryAndIndependentChecksPassed": True,
        "claimBoundaryFailClosed": True,
        "singlePagePdf": True,
        "physicalDimensionsPassed": True,
        "pdfTextPassed": True,
        "png600DpiPassed": True,
        "svgVectorTextPassed": True,
        "r073bFiveSixteenthsSentinelPassed": True,
        "driftRatioSentinelPassed": True,
        "exactCounterexamplesPassed": True,
        "qaRastersPresent": True,
        "visualQaPassed": args.qa_status == "passed",
    }
    validation = {
        "schemaVersion": "r073f-figure-validation-v1",
        "status": "passed" if all(checks.values()) else "pending",
        "checks": checks,
        "pdfPoints": points,
        "pngPixels": pixels,
        "claimBoundary": boundary,
    }
    (HERE / "validation.json").write_text(canonical(validation), encoding="utf-8")

    source_files = [
        "README.md", "caption.md", "command.txt", "config.json", "plot.py",
        "qa-protocol.md", "requirements.txt", "validate.py", "results.json",
        "validation.json", "qa-report.md", "figure.pdf", "figure.svg",
        "figure.png", "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png",
    ]
    file_records = [record(HERE / name) for name in source_files]
    output_records = []
    for name in ("figure.pdf", "figure.svg", "figure.png"):
        item = record(HERE / name, HERE)
        if name == "figure.png":
            item.update({"dpi": 600, "pixels": pixels})
        output_records.append(item)

    uname = platform.uname()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    source_commit = subprocess.check_output(
        ["git", "rev-parse", "5edb170^{commit}"], cwd=ROOT, text=True
    ).strip()
    analytic_paths = [
        "research/r073f_problem_freeze.md",
        "research/r073f_moving_dichotomy_proof.md",
        "research/r073f_gap_matrix.md",
        "research/r073f_literature_audit.md",
        "research/r073f_independent_analytic_audit.md",
        "research/r073f_report-source.md",
    ]
    analytic_bindings = []
    for relative in analytic_paths:
        payload = subprocess.check_output(
            ["git", "show", f"{source_commit}:{relative}"], cwd=ROOT
        )
        analytic_bindings.append({
            "path": relative,
            "bytes": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
            "sourceCommit": source_commit,
        })
    manifest = {
        "schemaVersion": "r073f-figure-manifest-v1",
        "figureId": config["figureId"],
        "status": "validated" if args.qa_status == "passed" else "draft",
        "analyticalQuestion": "What do the declared finite moving-profile propagations and two exact abstract counterexamples diagnose about a fixed-window roughness route?",
        "supportedClaim": "The declared N=96 binary64 endpoint gains and finite top-block conorms are reproducible under step halving and an independent explicit-Fourier construction; two exact examples show why spectral edge data alone do not control a uniform prefactor or transported direction. No continuum claim follows.",
        "createdAt": "2026-08-30T00:00:00+08:00",
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "generationBaseCommit": head,
            "sourceCommit": source_commit,
            "contentAddressedUnsealed": True,
            "reasonUnsealed": "new R0.73F sources are not yet committed; do not claim a clean certified Git run"
        },
        "sourceBindings": analytic_bindings,
        "computation": {
            "kind": "data-analysis",
            "configuration": "config.json",
            "precision": "IEEE-754 binary64 finite diagnostics; exact formulas in panels C-D",
            "solver": "CSV/JSON ingestion and deterministic Matplotlib rendering",
            "command": "python3 plot.py --deps /tmp/r073c-deps; python3 validate.py --deps /tmp/r073c-deps --qa-status passed --qa-note <note>",
            "wallTimeSeconds": summary["scientificWallTimeSeconds"] + independent["wallTimeSeconds"],
            "diagnosticOnly": True,
            "finiteDimensionalOnly": True,
        },
        "compute": {
            "host": uname.node,
            "operatingSystem": f"{uname.system} {uname.release} {uname.machine}",
            "cpu": "Apple M5 Max arm64",
            "memoryGiB": 36,
            "processes": 1,
            "threadsPerProcess": int(os.environ.get("OPENBLAS_NUM_THREADS", "4")),
            "gpu": "not used",
        },
        "environment": {
            "python": platform.python_version(),
            "numpy": "2.5.2",
            "matplotlib": "3.10.6",
            "pillow": "12.3.0",
            "pypdf": "6.10.0",
            "packagesLock": "requirements.txt",
        },
        "data": [{**record(HERE / "results.json", HERE), "schema": results["schemaVersion"]}],
        "sourceData": results["inputs"],
        "figure": {
            "profile": "journal-double-column",
            "layout": "four-panel finite diagnostic and exact-counterexample figure",
            "widthMillimetres": config["widthMillimetres"],
            "heightMillimetres": config["heightMillimetres"],
            "script": "plot.py",
            "outputs": output_records,
        },
        "caption": {"english": "caption.md"},
        "qa": qa,
        "claimBoundary": boundary,
        "inventoryPolicy": {
            "scope": "all regular files directly inside the figure package",
            "manifestFilesExcludes": ["manifest.json", "SHA256SUMS"],
            "sha256LedgerExcludes": ["SHA256SUMS"],
            "cacheDirectoriesForbidden": True,
        },
        "files": file_records,
    }
    (HERE / "manifest.json").write_text(canonical(manifest), encoding="utf-8")

    ledger_paths = sorted((HERE / name for name in source_files + ["manifest.json"]),
                          key=lambda path: path.name)
    ledger = "".join(f"{sha256(path)}  {path.name}\n" for path in ledger_paths)
    (HERE / "SHA256SUMS").write_text(ledger, encoding="utf-8")
    return 0 if validation["status"] in ("passed", "pending") else 1


if __name__ == "__main__":
    raise SystemExit(main())
