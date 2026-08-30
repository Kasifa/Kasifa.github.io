#!/usr/bin/env python3
"""Fail-closed structural, numerical, and rendering checks for R0.73G."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_COMMIT = "21c11ba3eef7f2b5dc3f107957e0744a0471745d"
EXPERIMENT_COMMIT = "0679192b65a294bb211c96decc47bb046ab60b93"
ANALYTIC_PATHS = (
    "research/r073g_problem_freeze.md",
    "research/r073g_nonlinear_shadowing_proof.md",
    "research/r073g_operator_derivation.md",
    "research/r073g_adversarial_audit.md",
    "research/r073g_independent_analytic_audit.md",
    "research/r073g_literature_audit.md",
    "research/r073g_gap_matrix.md",
    "research/r073g_report-source.md",
)
TRUE_DIAGNOSTIC_FACT_KEYS = {
    "actualFiniteTopEigenprofileUsed",
    "finiteBinary64Diagnostic",
    "twoIndependentFourierKernelsCrossChecked",
}
TRUE_BOUNDARY_KEYS = {"formalFiniteDiagnosticFigure"}


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


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


def git_bytes(commit: str, relative: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{relative}"], cwd=ROOT)


def require_commit(commit: str, label: str) -> None:
    result = subprocess.run(
        ["git", "cat-file", "-e", commit + "^{commit}"], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    require(result.returncode == 0, label + " is not a Git commit")


def require_ancestor(older: str, newer: str, message: str) -> None:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", older, newer], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    require(result.returncode == 0, message)


def historical_binding(commit: str, relative: str) -> dict[str, Any]:
    payload = git_bytes(commit, relative)
    return {
        "path": relative,
        "bytes": len(payload),
        "sha256": sha256_bytes(payload),
        "sourceCommit": commit,
    }


def make_qa_images(Image: Any, ImageOps: Any) -> None:
    with Image.open(HERE / "figure.png") as source:
        rgb = source.convert("RGB")
        final = rgb.resize((1780, 1320), Image.Resampling.LANCZOS)
        final.save(HERE / "qa-final-size.png", dpi=(254, 254))
        ImageOps.grayscale(final).save(HERE / "qa-grayscale.png", dpi=(254, 254))

    executable = shutil.which("pdftoppm")
    require(executable is not None, "pdftoppm is required for PDF raster QA")
    with tempfile.TemporaryDirectory(prefix="r073g-pdf-qa-") as temp:
        prefix = Path(temp) / "page"
        subprocess.run(
            [executable, "-png", "-r", "180", "-singlefile",
             str(HERE / "figure.pdf"), str(prefix)],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        with Image.open(Path(str(prefix) + ".png")) as rendered:
            rendered.convert("RGB").save(HERE / "qa-pdf.png", dpi=(180, 180))


def verify_flat_inventory() -> None:
    unexpected = [path.name for path in HERE.iterdir()
                  if not path.is_file() or path.is_symlink()]
    require(not unexpected, "figure package contains a directory or symlink")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--experiment-commit", required=True)
    parser.add_argument("--renderer-source-commit", required=True)
    parser.add_argument("--qa-status", choices=("pending", "passed"), default="pending")
    parser.add_argument("--qa-note", default="")
    args = parser.parse_args()
    if args.deps:
        sys.path.insert(0, args.deps)

    from PIL import Image, ImageOps
    from pypdf import PdfReader

    supplied = (
        (args.source_commit, SOURCE_COMMIT, "source commit"),
        (args.experiment_commit, EXPERIMENT_COMMIT, "experiment commit"),
    )
    for actual, expected, label in supplied:
        require(bool(re.fullmatch(r"[0-9a-f]{40}", actual)), label + " must be 40-hex")
        require(actual == expected, label + " differs from the frozen value")
        require_commit(actual, label)
    require(bool(re.fullmatch(r"[0-9a-f]{40}", args.renderer_source_commit)),
            "renderer source commit must be 40-hex")
    require_commit(args.renderer_source_commit, "renderer source commit")
    require_ancestor(SOURCE_COMMIT, EXPERIMENT_COMMIT,
                     "analytic source is not an ancestor of the experiment package")
    require_ancestor(EXPERIMENT_COMMIT, args.renderer_source_commit,
                     "experiment package is not an ancestor of renderer source")
    require(subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                   text=True).strip() == args.renderer_source_commit,
            "formal generation must run exactly at the frozen renderer source commit")
    require(git_bytes(args.renderer_source_commit,
                      str((HERE / "validate.py").relative_to(ROOT)))
            == (HERE / "validate.py").read_bytes(),
            "working validator differs from the frozen renderer source commit")

    verify_flat_inventory()
    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    results = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
    summary_path = ROOT / config["inputs"]["summary"]
    independent_path = ROOT / config["inputs"]["independent"]
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    independent = json.loads(independent_path.read_text(encoding="utf-8"))
    experiment_manifest = json.loads(
        (ROOT / "experiments/r073g/manifest.json").read_text(encoding="utf-8")
    )

    require(results["figureId"] == config["figureId"], "figure identity mismatch")
    require(results["evidenceClass"] == "finite-binary64-diagnostic-only",
            "figure evidence class changed")
    for item in results["inputs"]:
        path = ROOT / item["path"]
        require(path.is_file(), "missing input: " + item["path"])
        require(record(path) == item, "input binding changed: " + item["path"])
        require(git_bytes(EXPERIMENT_COMMIT, item["path"]) == path.read_bytes(),
                "input differs from experiment commit: " + item["path"])
    require(results["configBinding"] == record(HERE / "config.json"),
            "config binding changed after render")
    require(summary["diagnosticOnly"] is True, "primary diagnostic boundary missing")
    require(summary["crossValidation"]["allKernelChecksPass"] is True,
            "primary kernel checks failed")
    require(independent["allChecksPass"] is True, "independent checks failed")
    require(experiment_manifest["status"] == "validated",
            "experiment package is not validated")
    require(experiment_manifest["determinismCheck"]["sameCommandScientificRerunByteIdentical"]
            is True, "experiment determinism check missing")
    require(experiment_manifest["grid"]["rowCount"] == 28,
            "formal finite grid no longer has 28 rows")

    facts = results["diagnosticFacts"]
    require(set(facts) == TRUE_DIAGNOSTIC_FACT_KEYS,
            "diagnostic-fact inventory changed")
    require(all(facts.values()), "a declared diagnostic fact is false")
    boundary = results["claimBoundary"]
    require(set(boundary) == TRUE_BOUNDARY_KEYS | {
        "clayProblemSolved",
        "finiteH3CostProvesUniformContinuumH3Bound",
        "finiteLeakageProvesNonlinearInstability",
        "finiteTopEqualsContinuumTop",
        "ordinaryCutoffAgreementIsTailBound",
        "threeDimensionalVortexStretchingPresentInThisPlanarRow",
        "transitionThresholdEstablished",
    }, "claim-boundary inventory changed")
    for key, value in boundary.items():
        require(value is (key in TRUE_BOUNDARY_KEYS), "escaped claim boundary: " + key)

    for item in results["outputs"]:
        path = ROOT / item["path"]
        require(path.is_file(), "missing figure output: " + item["path"])
        require(record(path) == item, "figure output changed after render: " + item["path"])
    reader = PdfReader(HERE / "figure.pdf")
    require(len(reader.pages) == 1, "PDF must contain exactly one page")
    page = reader.pages[0]
    points = [float(page.mediabox.width), float(page.mediabox.height)]
    expected_points = [config["widthMillimetres"] / 25.4 * 72,
                       config["heightMillimetres"] / 25.4 * 72]
    require(max(abs(a - b) for a, b in zip(points, expected_points)) < 0.8,
            "PDF physical dimensions changed")
    pdf_text = page.extract_text() or ""
    for token in ("Frozen top eigenvalue", "Physical Sobolev cost",
                  "Generated rows", "Numerical cross-checks", "diagnostic only"):
        require(token in pdf_text, "PDF text missing: " + token)
    with Image.open(HERE / "figure.png") as image:
        pixels = list(image.size)
        dpi = image.info.get("dpi", (0, 0))
        require(abs(pixels[0] - 4205) <= 2 and abs(pixels[1] - 3118) <= 2,
                "PNG dimensions changed")
        require(min(dpi) > 599 and max(dpi) < 601, "PNG is not tagged at 600 dpi")
    svg = (HERE / "figure.svg").read_text(encoding="utf-8")
    require("<image" not in svg, "SVG unexpectedly contains raster data")
    for token in ("Frozen top eigenvalue", "Generated rows", "diagnostic only"):
        require(token in svg, "SVG text missing: " + token)

    observed = results["observed"]
    require(abs(observed["maximumFinestCutoffRelativeChange"]
                - 5.749359085030244e-14) < 1e-26,
            "cutoff-comparison sentinel changed")
    require(results["crossValidation"]["allChecksPass"] is True,
            "figure cross-validation status failed")
    require(results["crossValidation"]["primaryMaximumScaleOneDifference"] < 1e-12,
            "primary kernel discrepancy exceeded tolerance")
    require(results["crossValidation"]["independentMaximumScaleOneError"] < 1e-12,
            "independent kernel discrepancy exceeded tolerance")

    make_qa_images(Image, ImageOps)
    note = args.qa_note.strip()
    if args.qa_status == "passed":
        require(bool(note), "passed QA requires a non-empty inspection note")
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
        "note": note or "awaiting explicit visual inspection",
    }
    report = (
        "# R0.73G figure QA report\n\n"
        f"Status: **{args.qa_status}**.\n\n"
        f"Inspection note: {qa['note']}.\n\n"
        "The validator confirmed one-page PDF geometry, 600 dpi PNG metadata, "
        "vector SVG text, immutable input hashes, the two independent finite "
        "kernel checks, and the fail-closed claim boundary. This QA certifies "
        "presentation integrity only; it is not a continuum tail estimate, a "
        "transition threshold, or a Clay-problem conclusion.\n"
    )
    (HERE / "qa-report.md").write_text(report, encoding="utf-8")

    checks = {
        "commitChainPassed": True,
        "inputHashesPassed": True,
        "experimentPackageValidated": True,
        "scientificRerunDeterminismPassed": True,
        "primaryAndIndependentKernelChecksPassed": True,
        "claimBoundaryFailClosed": True,
        "singlePagePdf": True,
        "physicalDimensionsPassed": True,
        "pdfTextPassed": True,
        "png600DpiPassed": True,
        "svgVectorTextPassed": True,
        "finiteSentinelsPassed": True,
        "qaRastersPresent": True,
        "visualQaPassed": args.qa_status == "passed",
    }
    validation = {
        "schemaVersion": "r073g-figure-validation-v1",
        "status": "passed" if all(checks.values()) else "pending",
        "checks": checks,
        "pdfPoints": points,
        "pngPixels": pixels,
        "claimBoundary": boundary,
    }
    (HERE / "validation.json").write_text(canonical(validation), encoding="utf-8")

    excluded = {"manifest.json", "SHA256SUMS"}
    names = sorted(path.name for path in HERE.iterdir()
                   if path.is_file() and path.name not in excluded)
    file_records = [record(HERE / name) for name in names]
    source_bindings = [historical_binding(SOURCE_COMMIT, path)
                       for path in ANALYTIC_PATHS]
    uname = platform.uname()
    manifest = {
        "schemaVersion": "r073g-figure-manifest-v1",
        "figureId": config["figureId"],
        "status": "validated" if args.qa_status == "passed" else "draft",
        "analyticalQuestion": "How does the selected finite top row interact quadratically, and what does that reveal about the planar nonlinear shadowing route?",
        "supportedClaim": "The declared 28 finite Fourier compressions reproduce a positive frozen top row, its physical H3 cost, and nonzero quadratic leakage to Kz=0 and Kz=2 under two independent kernels. The finite checks do not supply a continuum tail bound, a transition threshold, three-dimensional stretching, or a Clay-problem conclusion.",
        "createdAt": "2026-08-30T00:00:00+08:00",
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": SOURCE_COMMIT,
            "experimentCommit": EXPERIMENT_COMMIT,
            "rendererSourceCommit": args.renderer_source_commit,
            "contentAddressedUnsealed": True,
            "reasonUnsealed": "the generated figure package F and certificate C have not yet been committed",
        },
        "sourceBindings": source_bindings,
        "experimentManifestBinding": historical_binding(
            EXPERIMENT_COMMIT, "experiments/r073g/manifest.json"
        ),
        "computation": {
            "kind": "data-analysis",
            "configuration": "config.json",
            "precision": "IEEE-754 binary64 finite Fourier diagnostics",
            "solver": "committed CSV/JSON ingestion and deterministic Matplotlib rendering",
            "command": "python3 plot.py --deps /tmp/r073c-deps; python3 validate.py --deps /tmp/r073c-deps --source-commit <S> --experiment-commit <E> --renderer-source-commit <R> --qa-status passed --qa-note <note>",
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
            "scipy": "1.16.1",
            "matplotlib": "3.10.6",
            "pillow": "12.3.0",
            "pypdf": "6.10.0",
            "packagesLock": "requirements.txt",
        },
        "data": [{**record(HERE / "results.json", HERE),
                  "schema": results["schemaVersion"]}],
        "sourceData": results["inputs"],
        "figure": {
            "profile": "journal-double-column",
            "layout": "four-panel finite top-row and nonlinear-leakage diagnostic",
            "script": "plot.py",
            "widthMillimetres": config["widthMillimetres"],
            "heightMillimetres": config["heightMillimetres"],
            "outputs": [record(HERE / name, HERE)
                        | ({"dpi": 600, "pixels": pixels} if name == "figure.png" else {})
                        for name in ("figure.pdf", "figure.svg", "figure.png")],
        },
        "caption": {"english": "caption.md"},
        "qa": qa,
        "diagnosticFacts": facts,
        "claimBoundary": boundary,
        "files": file_records,
        "inventoryPolicy": {
            "scope": "all regular files directly inside the figure package",
            "cacheDirectoriesForbidden": True,
            "manifestFilesExcludes": ["manifest.json", "SHA256SUMS"],
            "sha256LedgerExcludes": ["SHA256SUMS"],
        },
    }
    (HERE / "manifest.json").write_text(canonical(manifest), encoding="utf-8")
    ledger_names = sorted(path.name for path in HERE.iterdir()
                          if path.is_file() and path.name != "SHA256SUMS")
    (HERE / "SHA256SUMS").write_text(
        "".join(f"{sha256(HERE / name)}  {name}\n" for name in ledger_names),
        encoding="utf-8",
    )
    verify_flat_inventory()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
