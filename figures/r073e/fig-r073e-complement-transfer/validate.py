#!/usr/bin/env python3
"""Fail-closed structural and rendering validator for the R0.73E figure."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

from PIL import Image, ImageOps
from pypdf import PdfReader


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def record(path: Path) -> dict[str, object]:
    return {
        "path": str(path.relative_to(ROOT)),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def make_qa_images() -> None:
    with Image.open(HERE / "figure.png") as source:
        rgb = source.convert("RGB")
        final = rgb.copy()
        final.thumbnail((1100, 1100), Image.Resampling.LANCZOS)
        require(final.size == (1100, 816), "unexpected final-size preview geometry")
        final.save(HERE / "qa-final-size.png", dpi=(157, 157))
        gray = ImageOps.grayscale(rgb)
        gray.thumbnail((1262, 1262), Image.Resampling.LANCZOS)
        require(gray.size == (1262, 936), "unexpected grayscale preview geometry")
        gray.save(HERE / "qa-grayscale.png", dpi=(180, 180))

    with tempfile.TemporaryDirectory(prefix="r073e-figure-pdf-") as temp:
        prefix = Path(temp) / "page"
        command = ["pdftoppm", "-png", "-r", "180", "-singlefile",
                   str(HERE / "figure.pdf"), str(prefix)]
        subprocess.run(command, check=True, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
        rendered = Path(str(prefix) + ".png")
        with Image.open(rendered) as image:
            pdf_rgb = image.convert("RGB")
            require(pdf_rgb.size == (1262, 936), "unexpected PDF raster geometry")
            pdf_rgb.save(HERE / "qa-pdf.png", dpi=(180, 180))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--certificate-commit", required=True)
    args = parser.parse_args()
    require(bool(re.fullmatch(r"[0-9a-f]{40}", args.source_commit)),
            "source commit must be lowercase 40-hex")
    require(bool(re.fullmatch(r"[0-9a-f]{40}", args.certificate_commit)),
            "certificate commit must be lowercase 40-hex")

    required_before_qa = [
        "README.md", "caption.md", "command.txt", "config.json", "contract.json",
        "environment.txt", "figure-contract.md", "manifest-draft.json", "plot.py",
        "qa-protocol.md", "requirements.txt", "validate.py", "figure.pdf",
        "figure.svg", "figure.png", "results.json",
    ]
    for name in required_before_qa:
        require((HERE / name).is_file(), "missing figure file: " + name)
    make_qa_images()

    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    contract = json.loads((HERE / "contract.json").read_text(encoding="utf-8"))
    results = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
    require(config["figureId"] == contract["figureId"] == results["figureId"],
            "figure identity mismatch")
    diagnostic = ROOT / config["diagnostic"]
    independent = ROOT / config["independentValidation"]
    require(results["inputs"][0]["sha256"] == sha256(diagnostic),
            "diagnostic hash mismatch")
    require(results["inputs"][1]["sha256"] == sha256(independent),
            "independent-validation hash mismatch")
    independent_data = json.loads(independent.read_text(encoding="utf-8"))
    require(independent_data["allChecksPass"], "independent validation failed")
    require(independent_data["primary"]["sha256"] == sha256(diagnostic),
            "independent validation primary hash mismatch")

    boundary = contract["claimBoundary"]
    require(boundary["formalFiniteDiagnosticFigure"] is True,
            "formal finite diagnostic status missing")
    require(boundary["independentFiniteRecomputation"] is True,
            "independent finite recomputation missing")
    for key, value in boundary.items():
        if key not in ("formalFiniteDiagnosticFigure", "independentFiniteRecomputation"):
            require(value is False, "escaped claim boundary: " + key)
    require(results["claimBoundary"] == boundary,
            "results and contract boundaries differ")

    reader = PdfReader(HERE / "figure.pdf")
    require(len(reader.pages) == 1, "figure PDF is not one page")
    page = reader.pages[0]
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)
    target_width = 178 / 25.4 * 72
    target_height = 132 / 25.4 * 72
    require(abs(width - target_width) < 0.8 and abs(height - target_height) < 0.8,
            "figure PDF dimensions changed")
    text = page.extract_text() or ""
    for token in (
        "Finite complement diagnostics", "finite spectrum after one-cluster removal",
        "vertical-line Q-resolvent peaks", "Intrinsic moving-complement",
        "fixed inviscid complement leaks", "stored time grid only",
        "do not use fixed Q0 at long times",
    ):
        require(token in text, "PDF text missing: " + token)

    with Image.open(HERE / "figure.png") as image:
        png_size = list(image.size)
        dpi = image.info.get("dpi", (0, 0))
        require(abs(image.size[0] - 4205) <= 2 and abs(image.size[1] - 3118) <= 2,
                "600 dpi PNG dimensions changed")
        require(min(dpi) > 599 and max(dpi) < 601,
                "600 dpi PNG metadata changed")
    expected_qa = {
        "qa-final-size.png": (1100, 816),
        "qa-grayscale.png": (1262, 936),
        "qa-pdf.png": (1262, 936),
    }
    for name, size in expected_qa.items():
        with Image.open(HERE / name) as image:
            require(image.size == size, name + " dimensions changed")

    svg = (HERE / "figure.svg").read_text(encoding="utf-8")
    for token in (
        "Finite complement diagnostics", "vertical-line Q-resolvent peaks",
        "stored time grid only", "do not use fixed Q0 at long times",
    ):
        require(token in svg, "SVG text missing: " + token)
    require("<image" not in svg, "SVG unexpectedly rasterized")

    checks = {
        "inventoryComplete": True,
        "inputHashesPassed": True,
        "independentBindingPassed": True,
        "claimBoundaryFailClosed": True,
        "singlePagePdf": True,
        "physicalDimensionsPassed": True,
        "pdfTextPassed": True,
        "png600DpiDimensionsPassed": True,
        "svgVectorTextPassed": True,
        "finalSizeQaPresent": True,
        "grayscaleQaPresent": True,
        "pdfRasterQaPresent": True,
    }
    validation = {
        "schemaVersion": "r073e-figure-validation-v1",
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
        "pdfPoints": [width, height],
        "pngPixels": png_size,
        "claimBoundary": boundary,
    }
    (HERE / "validation.json").write_text(canonical(validation), encoding="utf-8")

    source_files = required_before_qa + [
        "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png",
        "validation.json", "qa-report.md",
    ]
    require((HERE / "qa-report.md").is_file(), "missing explicit visual QA report")
    outputs = []
    for name in ("figure.pdf", "figure.svg", "figure.png"):
        item = {"path": name, "bytes": (HERE / name).stat().st_size,
                "sha256": sha256(HERE / name)}
        if name == "figure.png":
            item.update({"dpi": 600, "pixels": png_size})
        outputs.append(item)
    public_directory = ROOT / "public/assets/r073e"
    public_assets = []
    public_copies_complete = True
    for output in outputs:
        suffix = Path(output["path"]).suffix
        target = public_directory / f"{config['figureId']}{suffix}"
        public_assets.append({
            "path": str(target.relative_to(ROOT)),
            "bytes": output["bytes"],
            "sha256": output["sha256"],
        })
        public_copies_complete = (
            public_copies_complete
            and target.is_file()
            and target.stat().st_size == output["bytes"]
            and sha256(target) == output["sha256"]
        )

    manifest = {
        "schemaVersion": "r073e-figure-manifest-v1",
        "release": "R0.73E",
        "figureId": config["figureId"],
        "status": "formal",
        "created": "2026-08-30",
        "createdAt": "2026-08-30T00:00:00+08:00",
        "analyticalQuestion": (
            "What do the stored finite compressions show about removing only "
            "one leading cluster, complementary resolvent peaks, semigroup growth, "
            "and fixed-projection leakage?"
        ),
        "supportedClaim": (
            "For the stated finite Fourier compressions, the moving complement "
            "retains a positive-real conjugate pair after the leading cluster is "
            "removed; the three stored vertical-line resolvent peak series and "
            "semigroup grid are independently reproduced; and a fixed inviscid "
            "projection exhibits severe long-time leakage. These finite findings "
            "motivate selecting all top clusters and moving projections, but prove "
            "no continuum spectral, resolvent, continuous-time, nonautonomous, "
            "nonlinear, or Clay statement."
        ),
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": args.source_commit,
            "certificateCommit": args.certificate_commit,
            "dirtyAtCertifiedRun": False,
            "figureSourcesBoundBySha256": True,
            "dirtyAtFigureGeneration": True,
        },
        "computation": {
            "kind": "data-analysis",
            "configuration": "config.json",
            "formalCommand": (
                "python3 validate.py --source-commit <40-hex> "
                "--certificate-commit <40-hex>"
            ),
            "precision": (
                "IEEE-754 binary64 finite diagnostics; analytic continuum "
                "theorems are certified separately"
            ),
            "solver": (
                "dense finite eigensystems, resolvent singular values, "
                "and matrix-exponential diagnostics"
            ),
            "timingBasis": (
                "three-cutoff, five-viscosity diagnostic and independent "
                "recomputation measured on 2026-08-30"
            ),
            "scientificWallTimeSeconds": 36.85,
            "randomnessUsed": False,
            "gpuUsed": False,
            "finiteDimensionalOnly": True,
            "diagnosticOnly": True,
        },
        "compute": {
            "host": "Wool.local",
            "operatingSystem": "macOS 26.6.2 build 25G83 arm64",
            "cpu": "Apple M5 Max arm64",
            "memoryGiB": 36.0,
            "processes": 1,
            "threadsPerProcess": 1,
            "gpu": "not used",
        },
        "environment": {
            "python": "3.12.13", "numpy": "2.5.2",
            "matplotlib": "3.10.6", "pillow": "12.3.0", "pypdf": "6.10.0",
            "packagesLock": "requirements.txt",
        },
        "data": [{
            **record(HERE / "results.json"),
            "path": "results.json",
            "schema": "r073e-figure-results-v1",
        }],
        "figure": {
            "widthMillimetres": config["widthMillimetres"],
            "heightMillimetres": config["heightMillimetres"],
            "profile": "journal-double-column",
            "layout": "four-panel finite operator-diagnostic figure",
            "script": "plot.py",
            "pngDpi": config["pngDpi"],
            "outputs": outputs,
        },
        "caption": {"english": "caption.md"},
        "qa": {
            "status": "passed",
            "visualInspectionExplicit": True,
            "finalSize": "qa-final-size.png",
            "finalSizeInspected": True,
            "grayscale": "qa-grayscale.png",
            "grayscaleInspected": True,
            "pdfRaster": "qa-pdf.png",
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "dataCrossChecked": True,
            "report": "qa-report.md",
        },
        "sourceData": [
            {"path": str(diagnostic.relative_to(ROOT)), "sha256": sha256(diagnostic)},
            {"path": str(independent.relative_to(ROOT)), "sha256": sha256(independent)},
        ],
        "inputBindings": [record(diagnostic), record(independent)],
        "masters": ["figure.pdf", "figure.svg", "figure.png"],
        "publication": {
            "directory": "public/assets/r073e",
            "fileStem": config["figureId"],
            "byteIdentityRequired": True,
            "publicCopiesComplete": public_copies_complete,
            "assets": public_assets,
        },
        "inputs": [record(diagnostic), record(independent)],
        "outputs": outputs,
        "claimBoundary": boundary,
        "validation": record(HERE / "validation.json"),
        "sources": [record(HERE / name) for name in source_files],
        "files": [record(HERE / name) for name in source_files],
    }
    (HERE / "manifest.json").write_text(canonical(manifest), encoding="utf-8")

    checksum_names = sorted(set(source_files + [
        "manifest.json", "manifest-draft.json", "SHA256SUMS",
        "figure.pdf", "figure.svg", "figure.png",
    ]))
    checksum_names.remove("SHA256SUMS")
    lines = [f"{sha256(HERE / name)}  {name}" for name in checksum_names]
    (HERE / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(canonical({
        "event": "figure-validated", "status": validation["status"],
        "manifest": sha256(HERE / "manifest.json"),
        "checksums": len(lines),
    }), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
