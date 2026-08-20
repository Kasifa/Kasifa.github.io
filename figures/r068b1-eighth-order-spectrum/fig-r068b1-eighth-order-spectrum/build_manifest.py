#!/usr/bin/env python3
"""Build the formal manifest for Figure R0.68B-1."""

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
    certificate = ROOT / "research/certificates/r068b1/eighth-order-cycle-audit.json"
    png = Image.open(HERE / "figure.png")
    manifest = {
        "schemaVersion": "1.0",
        "figureId": "fig-r068b1-eighth-order-spectrum",
        "status": "formal",
        "createdAt": "2026-08-21T00:25:00+08:00",
        "analyticalQuestion": (
            "What exact spectrum and reachable projection control the zero-time "
            "eighth-order seven-carrier target on the repeated-0100 packet?"
        ),
        "supportedClaim": (
            "The 1,792-state transfer has exact cycle ranks 204, 148, 148; its "
            "reachable scalar has one dominant root near 6438.80687 and a strictly "
            "negative dominant projection coefficient."
        ),
        "claimBoundary": (
            "This is a fixed-order zero-time algebraic theorem. The complete "
            "heat-weighted seven-simplex, the full Picard series, singularity, "
            "global regularity, and the Millennium problem remain open."
        ),
        "git": {
            "sourceCommit": metadata["sourceCommit"],
            "certificateCommit": metadata["certificateCommit"],
            "repository": "Kasifa/Kasifa.github.io",
            "dirtyAtCertifiedRun": False,
        },
        "sourceData": [{
            "fileName": certificate.name,
            "location": str(certificate.relative_to(ROOT)),
            "bytes": certificate.stat().st_size,
            "sha256": metadata["certificateSha256"],
            "extractionCommand": "python3 prepare_data.py",
        }],
        "data": [
            record(HERE / "rank-collapse.csv", format="csv", schema="ambient and exact cycle ranks"),
            record(HERE / "spectral-blocks.csv", format="csv", schema="exact image characteristic blocks and spectral roles"),
            record(HERE / "reachable-sequence.csv", format="csv", schema="82 exact integer values and dominant-root normalization"),
            record(HERE / "certified-scales.csv", format="csv", schema="strict root, projection, remainder, and probe-rate bounds"),
            record(HERE / "figure-data-metadata.json", format="json", schema="pinned certificate and provenance"),
            record(HERE / "figure-data-resources.csv", format="csv", schema="deterministic extraction resources"),
            record(HERE / "plot-resources.csv", format="csv", schema="rendering resources"),
        ],
        "computation": {
            "kind": "exact-audit",
            "configuration": "1,792 states, repeated 0100 cycle, exact image restriction, degree-33 reachable recurrence",
            "precision": "exact integer and rational linear algebra, modular cross-checks, exact Schur transforms; decimals are display only",
            "solver": "SciPy sparse transfer construction, SymPy DomainMatrix exact ranks and characteristic polynomial, GMP-backed integers",
            "command": "python research/eighth_order_cycle_audit.py --source-commit 3ddf6d30965837311c0b659d5fb21e41c3b80f14 --max-direct-level 6 --sequence-terms 82 --progress --output research/certificates/r068b1/eighth-order-cycle-audit.json",
            "wallTimeSeconds": 228.5643471670046,
            "monitoring": {
                "enabled": True,
                "reportIntervalSeconds": 5,
                "trackedFields": ["wallSeconds", "processTreeRssMiB", "cpuPercent", "gpuMemoryMiB", "status"],
                "resourceLog": "research/certificates/r068b1/resources.csv",
                "peakRssMiB": 649.312,
                "samples": 47,
            },
        },
        "compute": {
            "host": "local Mac workstation",
            "operatingSystem": "macOS 26.6.1 arm64",
            "cpu": "Apple M5 Max",
            "gpu": "not used",
            "memoryGiB": 36,
            "processes": 1,
            "threadsPerProcess": 18,
        },
        "environment": {
            "python": "3.12.13",
            "matplotlib": "3.11.1",
            "packagesLock": "research/requirements-r068b.txt",
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
            "family": "rank collapse, exact factor-dimension strip, and normalized recurrence convergence",
            "takeaway": "the zero-time eighth-order target has one reachable dominant root with a strictly negative projection",
            "nonColorEncoding": "hatches, factor boundaries, direct labels, marker shapes, zero line, and interval endpoints",
            "outputFootprint": "double-column 178 by 105 millimetres with PDF, SVG, and 600 dpi PNG",
        },
        "qa": {
            "status": "passed",
            "dataCrossChecked": True,
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "notes": "The 600 dpi PNG, grayscale conversion, and Poppler-rendered PDF were inspected at final size; hatches retain all factor distinctions without color.",
        },
        "caption": {"english": "caption.md"},
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
