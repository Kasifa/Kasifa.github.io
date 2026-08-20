#!/usr/bin/env python3
"""Build the formal manifest for Figure R0.67C-2."""

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
        "figureId": "fig-r067c2-dominant-heat",
        "status": "formal",
        "createdAt": "2026-08-20T23:30:00+08:00",
        "analyticalQuestion": "Does the dominant complete sixth-order five-simplex heat projection have a strict sign?",
        "supportedClaim": (
            "A 67,200-dimensional degree-six centred jet, signed-shift defect "
            "aggregation, and global seventh-derivative majorant give a strict "
            "negative interval for the dominant complete sixth-order heat projection."
        ),
        "claimBoundary": (
            "Only one fixed sixth-order periodic projection is controlled; all "
            "Picard orders, norm inflation, singularity, global regularity, and "
            "the Millennium problem remain open."
        ),
        "git": {
            "sourceCommit": metadata["sourceCommit"],
            "certificateCommit": metadata["certificateCommit"],
            "repository": "Kasifa/Kasifa.github.io",
            "dirtyAtCertifiedRun": False,
        },
        "sourceData": [{
            "fileName": "sixth-order-heat-dominant-projection-audit.json",
            "location": metadata["certificate"],
            "bytes": (ROOT / metadata["certificate"]).stat().st_size,
            "sha256": metadata["certificateSha256"],
            "extractionCommand": (
                "python3 prepare_data.py --certificate-commit "
                "cd4124a4c781ba6593635d23aab425515a2ee155"
            ),
        }],
        "data": [
            record(HERE / "projection-intervals.csv", format="csv", schema="guarded jet, correction, and complete projection intervals"),
            record(HERE / "derivative-budget.csv", format="csv", schema="raw, guarded, and zero-contact derivative levels"),
            record(HERE / "spectral-scales.csv", format="csv", schema="degree-six, affine, finite, and dominant scales"),
            record(HERE / "figure-data-metadata.json", format="json", schema="pinned certificate and provenance"),
            record(HERE / "figure-data-resources.csv", format="csv", schema="deterministic extraction resources"),
            record(HERE / "plot-resources.csv", format="csv", schema="rendering resources"),
        ],
        "computation": {
            "kind": "exact-audit",
            "configuration": "320 states, 210 centred moments per state, ten heat shuffles, seventh derivative majorant",
            "precision": "exact integer combinatorics and root bracket with guarded binary64 analytic-numerical enclosures",
            "solver": "exact CRT mass projector, triangular moment solves, signed shift collision, and simplex monomial integration",
            "command": "python3 research/sixth_order_heat_dominant_projection_audit.py --output research/certificates/r067c2/sixth-order-heat-dominant-projection-audit.json --progress",
            "wallTimeSeconds": metadata["runtimeSeconds"],
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
                record(HERE / "figure.png", dpi=600, pixels=f"{png.width} by {png.height}"),
            ],
        },
        "chartContract": {
            "family": "guarded interval, derivative budget, and logarithmic spectral scale panels",
            "takeaway": "the complete dominant sixth-order heat projection stays strictly negative after the full resolvent correction",
            "nonColorEncoding": "interval endpoints, distinct marker shapes, zero line, direct values, and logarithmic positions",
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
            "notes": "Color, grayscale, and Poppler-rendered PDF were inspected at final size; the strict negative endpoint is legible.",
        },
        "caption": {"english": "caption.md"},
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
