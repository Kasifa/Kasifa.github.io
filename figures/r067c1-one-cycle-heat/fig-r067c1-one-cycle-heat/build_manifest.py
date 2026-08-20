#!/usr/bin/env python3
"""Build the formal manifest for Figure R0.67C-1."""

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
        "figureId": "fig-r067c1-one-cycle-heat",
        "status": "formal",
        "createdAt": "2026-08-20T22:00:00+08:00",
        "analyticalQuestion": (
            "Does the complete five-simplex sixth-order heat observable have "
            "a rigorously nonzero sign at the first stationary four-bit cycle?"
        ),
        "supportedClaim": (
            "Exact enumeration of 34,690 valid carrier tuples and all ten time "
            "orders, combined with a degree-32 rational Taylor enclosure, proves "
            "that the complete M=16 sixth-order heat coefficient is strictly positive."
        ),
        "claimBoundary": (
            "The dominant asymptotic heat projection, all-order Picard control, "
            "singularity, global regularity, and any Millennium-problem claim remain open."
        ),
        "git": {
            "sourceCommit": metadata["sourceCommit"],
            "certificateCommit": metadata["certificateCommit"],
            "repository": "Kasifa/Kasifa.github.io",
            "dirtyAtCertifiedRun": False,
        },
        "sourceData": [
            {
                "fileName": "sixth-order-heat-one-cycle-audit.json",
                "location": metadata["certificate"],
                "bytes": (ROOT / metadata["certificate"]).stat().st_size,
                "sha256": metadata["certificateSha256"],
                "extractionCommand": "python3 prepare_data.py",
            }
        ],
        "data": [
            record(HERE / "enumeration-by-a.csv", format="csv", schema="sixteen exact carrier-A slices"),
            record(HERE / "partial-sums.csv", format="csv", schema="degree-zero through degree-32 Taylor partial sums"),
            record(HERE / "certificate-scales.csv", format="csv", schema="strict coefficient interval, tail bound, and separation ratio"),
            record(HERE / "figure-data-metadata.json", format="json", schema="pinned certificate, commits, checks, and claim boundary"),
            record(HERE / "figure-data-resources.csv", format="csv", schema="deterministic extraction resource record"),
            record(HERE / "plot-resources.csv", format="csv", schema="final rendering resource record"),
        ],
        "computation": {
            "kind": "exact-audit",
            "configuration": "M=16, q=2, 34,690 valid tuples, ten time orders, Taylor degree 32",
            "precision": "Python integers and Fractions for proof fields; binary64 only for plotted positions",
            "solver": "direct signed carrier enumeration, complete homogeneous recurrence, and exact rational tail majorant",
            "command": "python3 research/sixth_order_heat_one_cycle_audit.py --output research/certificates/r067c1/sixth-order-heat-one-cycle-audit.json --order 32 --progress",
            "wallTimeSeconds": 3.35,
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
            "family": "one enumeration panel, one convergence panel, and one logarithmic certificate panel",
            "takeaway": "the complete first-cycle heat coefficient is positive with a tail ten orders smaller",
            "nonColorEncoding": "bar versus diamond, open-circle convergence markers, direct labels, and logarithmic positions",
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
                "were inspected at final size; the finite-scale boundary remains legible."
            ),
        },
        "caption": {"english": "caption.md"},
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
