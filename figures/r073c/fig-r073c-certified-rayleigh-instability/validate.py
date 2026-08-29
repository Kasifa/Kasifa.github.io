#!/usr/bin/env python3
"""Fail-closed structural validator for the R0.73C formal figure."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

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


def file_record(path: Path) -> dict[str, object]:
    return {
        "path": str(path.relative_to(ROOT)),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def main() -> int:
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
    boundary = contract["claimBoundary"]
    require(boundary["exactCubicNeutralSpectrum"] is True,
            "neutral theorem missing")
    require(boundary["infiniteDimensionalFrozenRayleighInstability"] is True,
            "C4 theorem missing")
    for key in (
        "smoothTraceCurveItselfIsCertified", "finiteFourierRowsAreTheorem",
        "rootUniqueness", "algebraicSimplicity",
        "viscousSpectralPersistence", "nonautonomousTransfer",
        "nonlinearNavierStokesClosure", "clayMillenniumProblemSolved",
    ):
        require(boundary[key] is False, "escaped claim boundary: " + key)

    reader = PdfReader(HERE / "figure.pdf")
    require(len(reader.pages) == 1, "figure PDF is not one page")
    page = reader.pages[0]
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)
    require(abs(width - 504.0) < 1.0 and abs(height - 373.68) < 1.0,
            "figure PDF dimensions changed")
    text = page.extract_text() or ""
    for token in ("C3", "C4", "C5", "C6", "CLOSED", "OPEN",
                  "CONDITIONAL", "Fourier cutoff"):
        require(token in text, "PDF text missing: " + token)

    with Image.open(HERE / "figure.png") as image:
        require(image.size == (4200, 3114), "600 dpi PNG dimensions changed")
    with Image.open(HERE / "qa-final-size.png") as image:
        require(image.size == (2100, 1557), "final-size QA dimensions changed")
    with Image.open(HERE / "qa-grayscale.png") as image:
        require(image.size == (2100, 1557), "grayscale QA dimensions changed")

    svg = (HERE / "figure.svg").read_text(encoding="utf-8")
    for token in ("C3", "C4", "C5", "C6", "certified periodic mode"):
        require(token in svg, "SVG text missing: " + token)
    require("<image" not in svg, "SVG unexpectedly rasterized")

    checks = {
        "inventoryComplete": True,
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
        "schemaVersion": "r073c-figure-validation-v1",
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
        "pdfPoints": [width, height],
        "pngPixels": [4200, 3114],
        "claimBoundary": boundary,
    }
    (HERE / "validation.json").write_text(
        canonical(validation), encoding="utf-8")

    source_names = required + ["validation.json"]
    manifest = {
        "schemaVersion": "r073c-figure-manifest-v1",
        "release": "R0.73C",
        "figureId": config["figureId"],
        "status": "formal",
        "created": "2026-08-30",
        "masters": ["figure.pdf", "figure.svg", "figure.png"],
        "publication": {
            "directory": "public/assets/r073c",
            "fileStem": config["figureId"],
            "byteIdentityRequired": True,
        },
        "qa": {
            "status": "passed",
            "visualInspectionExplicit": True,
            "finalSize": "qa-final-size.png",
            "grayscale": "qa-grayscale.png",
            "pdfRaster": "qa-pdf.png",
            "report": "qa-report.md",
        },
        "files": [file_record(HERE / name) for name in source_names],
        "inputBindings": [results["intervalInput"], results["fourierInput"],
                          results["finiteValidation"]],
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

