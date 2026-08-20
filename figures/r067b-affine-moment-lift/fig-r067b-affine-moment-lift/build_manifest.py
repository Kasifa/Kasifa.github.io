#!/usr/bin/env python3
"""Build the formal manifest for Figure R0.67B-1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def record(path: Path, **extra: object) -> dict[str, object]:
    return {
        "path": path.name,
        "bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        **extra,
    }


def main() -> None:
    metadata = json.loads((HERE / "figure-data-metadata.json").read_text())
    png = Image.open(HERE / "figure.png")
    manifest = {
        "schemaVersion": "1.0",
        "figureId": "fig-r067b-affine-moment-lift",
        "status": "formal",
        "createdAt": "2026-08-20T21:10:00+08:00",
        "analyticalQuestion": (
            "Does lifting mass and all four free first moments isolate the "
            "sixth-order dominant root from the infinite-dimensional spatial remainder?"
        ),
        "supportedClaim": (
            "Exact arithmetic constructs a 1600-dimensional affine lift, verifies "
            "all four first moments directly through seven binary levels, and proves "
            "the strict hierarchy 26<256<300<mu. The complete heat-weighted "
            "five-simplex projection sign is not certified."
        ),
        "claimBoundary": (
            "No complete heat projection, all-order Picard control, norm inflation, "
            "singularity, global regularity, or Millennium-problem claim."
        ),
        "git": {
            "sourceCommit": metadata["sourceCommit"],
            "certificateCommit": metadata["certificateCommit"],
            "repository": "Kasifa/Kasifa.github.io",
            "dirtyAtCertifiedRun": False,
        },
        "sourceData": [
            {
                "fileName": "sixth-order-affine-moment-audit.json",
                "location": metadata["certificate"],
                "bytes": (ROOT / metadata["certificate"]).stat().st_size,
                "sha256": metadata["certificateSha256"],
                "extractionCommand": "python3 prepare_data.py",
            }
        ],
        "data": [
            record(HERE / "direct-levels.csv", format="csv", schema="seven exact direct mass and first-moment checks"),
            record(HERE / "spectral-scales.csv", format="csv", schema="four certified spectral and remainder scales"),
            record(HERE / "lift-blocks.csv", format="csv", schema="nine nonzero blocks of the finite affine lift"),
            record(HERE / "figure-data-metadata.json", format="json", schema="pinned certificate, commits, checks, and claim boundary"),
            record(HERE / "figure-data-resources.csv", format="csv", schema="deterministic extraction resource record"),
            record(HERE / "plot-resources.csv", format="csv", schema="final rendering resource record"),
        ],
        "computation": {
            "kind": "exact-audit",
            "configuration": "320 sign/carry states, four free first moments, seven direct binary levels",
            "precision": "Python integers and Fractions for proof fields; binary64 only for plotted positions",
            "solver": "exact digit moment transfer, direct five-polynomial convolution, and exact spectral enclosures",
            "command": "python3 research/sixth_order_affine_moment_audit.py --max-direct-level 7 --progress --output research/certificates/r067b/sixth-order-affine-moment-audit.json",
            "wallTimeSeconds": 2.04,
        },
        "compute": {
            "host": "local Mac workstation",
            "operatingSystem": "macOS 26.6.1 arm64",
            "cpu": "Apple M5 Max",
            "gpu": "not used",
            "memoryGiB": 36,
            "processes": 1,
            "threadsPerProcess": 1,
        },
        "environment": {
            "python": "3.12.13",
            "matplotlib": "3.11.1",
            "packagesLock": "requirements-research.txt",
        },
        "figure": {
            "script": "plot.py",
            "widthMillimetres": 178,
            "heightMillimetres": 105,
            "profile": "journal-default",
            "outputs": [
                record(HERE / "figure.pdf"),
                record(HERE / "figure.svg"),
                record(
                    HERE / "figure.png",
                    dpi=600,
                    pixels=f"{png.width} by {png.height}",
                ),
            ],
        },
        "chartContract": {
            "family": "one direct-audit panel, one spectral-threshold panel, and one block-lift schematic",
            "takeaway": "the exact affine lift leaves a 256-scale remainder strictly below mu",
            "nonColorEncoding": "marker shapes, direct labels, block positions, and interval shading",
            "outputFootprint": "double-column 178 by 105 millimetres with PDF, SVG, and 600 dpi PNG",
        },
        "qa": {
            "status": "passed",
            "dataCrossChecked": True,
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "pdfFontsEmbedded": True,
            "notes": (
                "Color PNG, true grayscale conversion, and Poppler-rendered PDF "
                "were inspected at final size; the heat-projection boundary remains legible."
            ),
        },
        "caption": {"english": "caption.md"},
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
