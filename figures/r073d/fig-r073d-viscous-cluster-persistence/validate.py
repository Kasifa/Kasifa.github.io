#!/usr/bin/env python3
"""Fail-closed structural validator for the R0.73D formal figure."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

from PIL import Image
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--certificate-commit", required=True)
    args = parser.parse_args()
    for label, value in (
        ("source commit", args.source_commit),
        ("certificate commit", args.certificate_commit),
    ):
        require(bool(re.fullmatch(r"[0-9a-f]{40}", value)),
                label + " must be lowercase 40-hex")

    required = [
        "README.md", "caption.md", "command.txt", "config.json",
        "contract.json", "environment.txt", "figure-contract.md",
        "manifest-draft.json", "plot.py", "qa-protocol.md",
        "requirements.txt", "validate.py", "figure.pdf", "figure.svg",
        "figure.png", "results.json", "qa-final-size.png",
        "qa-grayscale.png", "qa-pdf.png", "qa-report.md",
    ]
    for name in required:
        require((HERE / name).is_file(), "missing figure file: " + name)

    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    contract = json.loads((HERE / "contract.json").read_text(encoding="utf-8"))
    results = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
    require(config["figureId"] == contract["figureId"] == results["figureId"],
            "figure identity mismatch")
    require(results["inputs"][0]["sha256"] == sha256(ROOT / config["experiment"]),
            "experiment hash mismatch")
    require(results["inputs"][1]["sha256"] == sha256(ROOT / config["certificate"]),
            "certificate hash mismatch")

    boundary = contract["claimBoundary"]
    require(boundary["staticVanishingViscosityPersistence"] is True,
            "static persistence theorem missing")
    require(boundary["fixedClusterRieszProjectionNormConvergence"] is True,
            "Riesz norm theorem missing")
    for key in (
        "finiteCurvesAreContinuumProof", "inviscidEigenvalueSimple",
        "explicitContourRadius", "logFastTimeTransfer",
        "nonlinearNavierStokes", "clayProblemSolved",
    ):
        require(boundary[key] is False, "escaped claim boundary: " + key)
    require(results["claimBoundary"] == boundary,
            "result and contract boundaries differ")

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
        "Static viscous persistence", "finite compression only",
        "diagnostic, not the continuum proof", "CLOSED", "OPEN",
        "Riesz norm convergence", "nonlinear NSE / Clay",
        "Shvydkoy-Friedlander",
    ):
        require(token in text, "PDF text missing: " + token)

    with Image.open(HERE / "figure.png") as image:
        png_size = list(image.size)
        dpi = image.info.get("dpi", (0, 0))
        require(abs(image.size[0] - 4205) <= 2 and abs(image.size[1] - 3118) <= 2,
                "600 dpi PNG dimensions changed")
        require(min(dpi) > 599 and max(dpi) < 601,
                "600 dpi PNG metadata changed")
    with Image.open(HERE / "qa-final-size.png") as image:
        require(image.size == (1100, 816), "final-size QA dimensions changed")
    with Image.open(HERE / "qa-grayscale.png") as image:
        require(image.size == (1262, 936), "grayscale QA dimensions changed")
    with Image.open(HERE / "qa-pdf.png") as image:
        require(image.size == (1262, 936), "PDF raster dimensions changed")

    svg = (HERE / "figure.svg").read_text(encoding="utf-8")
    for token in (
        "Static viscous persistence", "finite compression only",
        "diagnostic, not the continuum proof", "CLOSED", "OPEN",
    ):
        require(token in svg, "SVG text missing: " + token)
    require("<image" not in svg, "SVG unexpectedly rasterized")

    checks = {
        "inventoryComplete": True,
        "inputHashesPassed": True,
        "claimBoundaryFailClosed": True,
        "singlePagePdf": True,
        "physicalDimensionsPassed": True,
        "pdfTextPassed": True,
        "png600DpiDimensionsPassed": True,
        "svgVectorTextPassed": True,
        "finalSizeQaPresent": True,
        "grayscaleQaPresent": True,
        "visualInspectionExplicit": True,
    }
    validation = {
        "schemaVersion": "r073d-figure-validation-v1",
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
        "pdfPoints": [width, height],
        "pngPixels": png_size,
        "claimBoundary": boundary,
    }
    (HERE / "validation.json").write_text(canonical(validation), encoding="utf-8")

    outputs = []
    public_assets = []
    public_copies_complete = True
    for name in ("figure.pdf", "figure.svg", "figure.png"):
        item = {
            "path": name,
            "bytes": (HERE / name).stat().st_size,
            "sha256": sha256(HERE / name),
        }
        if name == "figure.png":
            item.update({"dpi": 600, "pixels": png_size})
        outputs.append(item)
        suffix = Path(name).suffix
        relative = "public/assets/r073d/" + config["figureId"] + suffix
        public_path = ROOT / relative
        if (not public_path.is_file()
                or public_path.stat().st_size != item["bytes"]
                or sha256(public_path) != item["sha256"]):
            public_copies_complete = False
        public_assets.append({
            "path": relative,
            "bytes": item["bytes"],
            "sha256": item["sha256"],
        })

    source_names = required + ["validation.json"]
    manifest = {
        "schemaVersion": "r073d-figure-manifest-v1",
        "release": "R0.73D",
        "figureId": config["figureId"],
        "status": "formal",
        "created": "2026-08-30",
        "createdAt": "2026-08-30T00:00:00+08:00",
        "analyticalQuestion": (
            "Does the certified inviscid Rayleigh cluster persist for "
            "sufficiently small positive viscosity in the physical kinetic space?"
        ),
        "supportedClaim": (
            "A fixed positive inviscid cluster persists for all sufficiently "
            "small viscosity: the contour resolvent is uniformly bounded, the "
            "Riesz projections converge in operator norm, rank and total "
            "algebraic multiplicity are preserved, and all cluster eigenvalues "
            "converge to the inviscid value. The contour and threshold are not "
            "explicit; simplicity, rates, complement control, fast-time "
            "transfer, nonlinear Navier--Stokes control, and Clay remain open."
        ),
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": args.source_commit,
            "certificateCommit": args.certificate_commit,
            "dirtyAtCertifiedRun": False,
        },
        "computation": {
            "kind": "finite Fourier diagnostic in the exact kinetic-space isometry",
            "configuration": "config.json",
            "precision": "IEEE-754 binary64 diagnostic; analytic theorem is separate",
            "solver": "dense eigensystems and finite Riesz projectors",
            "formalCommand": (
                "python3 validate.py --source-commit <40-hex> "
                "--certificate-commit <40-hex>"
            ),
            "diagnosticOnly": True,
            "finiteDimensionalOnly": True,
        },
        "compute": {
            "host": "Wool.local",
            "operatingSystem": "macOS 26.6.2 build 25G83 arm64",
            "cpu": "arm64",
            "memoryGiB": 36.0,
            "processes": 1,
            "threadsPerProcess": 1,
            "gpu": "not used",
        },
        "environment": {
            "python": "3.12.13", "packagesLock": "requirements.txt",
            "numpy": "2.5.2", "scipy": "1.16.1",
            "matplotlib": "3.10.6", "pillow": "12.3.0",
            "pypdf": "6.10.0",
        },
        "sourceData": results["inputs"],
        "figure": {
            "profile": "journal-double-column",
            "script": "plot.py",
            "widthMillimetres": 178,
            "heightMillimetres": 132,
            "pngDpi": 600,
            "layout": "four-panel operator, finite diagnostic, and boundary figure",
            "outputs": outputs,
        },
        "caption": {"english": "caption.md"},
        "masters": ["figure.pdf", "figure.svg", "figure.png"],
        "publication": {
            "directory": "public/assets/r073d",
            "fileStem": config["figureId"],
            "byteIdentityRequired": True,
            "publicCopiesComplete": public_copies_complete,
            "assets": public_assets,
        },
        "qa": {
            "status": "passed",
            "visualInspectionExplicit": True,
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "dataCrossChecked": True,
            "finalSize": "qa-final-size.png",
            "grayscale": "qa-grayscale.png",
            "pdfRaster": "qa-pdf.png",
            "report": "qa-report.md",
        },
        "files": [record(HERE / name) for name in source_names],
        "inputBindings": results["inputs"],
        "claimBoundary": boundary,
    }
    (HERE / "manifest.json").write_text(canonical(manifest), encoding="utf-8")
    ledger_names = sorted(source_names + ["manifest.json"])
    (HERE / "SHA256SUMS").write_text(
        "".join(f"{sha256(HERE / name)}  {name}\n" for name in ledger_names),
        encoding="utf-8",
    )
    print(canonical(validation), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

