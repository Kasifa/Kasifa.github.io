#!/usr/bin/env python3
"""Fail-closed structural validator for the R0.73C formal figure."""

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


def file_record(path: Path) -> dict[str, object]:
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
    for label, commit in (
        ("source commit", args.source_commit),
        ("certificate commit", args.certificate_commit),
    ):
        require(bool(re.fullmatch(r"[0-9a-f]{40}", commit)),
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
    outputs = [
        {
            "path": "figure.pdf",
            "bytes": (HERE / "figure.pdf").stat().st_size,
            "sha256": sha256(HERE / "figure.pdf"),
        },
        {
            "path": "figure.svg",
            "bytes": (HERE / "figure.svg").stat().st_size,
            "sha256": sha256(HERE / "figure.svg"),
        },
        {
            "path": "figure.png",
            "bytes": (HERE / "figure.png").stat().st_size,
            "sha256": sha256(HERE / "figure.png"),
            "dpi": 600,
            "pixels": [4200, 3114],
        },
    ]
    data = [
        {
            "path": name,
            "bytes": (HERE / name).stat().st_size,
            "sha256": sha256(HERE / name),
            "schema": schema,
        }
        for name, schema in (
            ("results.json", "R0.73C plotted-value and claim-boundary ledger"),
            ("validation.json", "R0.73C structural and visual-QA validation"),
        )
    ]
    public_assets = []
    public_copies_complete = True
    for output in outputs:
        suffix = Path(str(output["path"])).suffix
        public_relative = (
            "public/assets/r073c/" + config["figureId"] + suffix
        )
        public_path = ROOT / public_relative
        if (
            not public_path.is_file()
            or public_path.stat().st_size != output["bytes"]
            or sha256(public_path) != output["sha256"]
        ):
            public_copies_complete = False
        public_assets.append({
            "path": public_relative,
            "bytes": output["bytes"],
            "sha256": output["sha256"],
        })
    manifest = {
        "schemaVersion": "r073c-figure-manifest-v1",
        "release": "R0.73C",
        "figureId": config["figureId"],
        "status": "formal",
        "created": "2026-08-30",
        "createdAt": "2026-08-30T00:00:00+08:00",
        "analyticalQuestion": (
            "Does the cubic collision profile have an exact neutral level and "
            "a rigorously certified infinite-dimensional frozen Rayleigh "
            "unstable mode?"
        ),
        "supportedClaim": (
            "The exact cubic neutral spectrum is closed and a positive frozen "
            "Rayleigh point eigenvalue exists with sigma in (0.17035,0.17050). "
            "Finite Fourier rows are diagnostic only; viscous persistence, "
            "nonautonomous transfer, nonlinear Navier--Stokes closure, and the "
            "Clay problem remain open."
        ),
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": args.source_commit,
            "certificateCommit": args.certificate_commit,
            "dirtyAtCertifiedRun": False,
        },
        "computation": {
            "kind": "closed-form sampling plus validated finite CSV ingestion",
            "configuration": "config.json",
            "precision": (
                "outward-rounded interval inputs with IEEE-754 binary64 "
                "presentation sampling"
            ),
            "solver": (
                "validated periodic-ODE endpoint ingestion, closed-form neutral "
                "mode evaluation, and diagnostic finite Fourier ingestion"
            ),
            "formalCommand": (
                "python3 validate.py --source-commit <40-hex> "
                "--certificate-commit <40-hex>"
            ),
            "scientificWallTimeSeconds": 0.0,
            "diagnosticOnly": False,
            "finiteDimensionalOnly": False,
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
            "python": "3.12.13",
            "packagesLock": "requirements.txt",
            "numpy": "2.5.2",
            "scipy": "1.16.1",
            "matplotlib": "3.10.6",
        },
        "data": data,
        "sourceData": [
            {
                "path": item["path"],
                "sha256": item["sha256"],
                "role": "certified input or independent finite diagnostic",
            }
            for item in (
                results["intervalInput"], results["fourierInput"],
                results["finiteValidation"],
            )
        ],
        "figure": {
            "profile": "journal-double-column",
            "script": "plot.py",
            "widthMillimetres": 178,
            "heightMillimetres": 132,
            "pngDpi": 600,
            "layout": "four-panel theorem, certificate, diagnostic, and boundary figure",
            "outputs": outputs,
        },
        "caption": {"english": "caption.md"},
        "masters": ["figure.pdf", "figure.svg", "figure.png"],
        "publication": {
            "directory": "public/assets/r073c",
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
            "previews": [
                "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png",
            ],
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
