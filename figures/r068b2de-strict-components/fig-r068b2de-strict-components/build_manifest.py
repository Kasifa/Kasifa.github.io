#!/usr/bin/env python3
"""Build the manifest for Figure R0.68B-2d/e."""

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
    source_data = []
    source_reports = []
    for key, digest_key in (
        ("derivativeCertificate", "derivativeSha256"),
        ("massCertificate", "massSha256"),
        ("pilotCertificate", "pilotSha256"),
    ):
        source = ROOT / metadata[key]
        source_reports.append(json.loads(source.read_text()))
        source_data.append(
            {
                "fileName": source.name,
                "location": str(source.relative_to(ROOT)),
                "bytes": source.stat().st_size,
                "sha256": metadata[digest_key],
                "extractionCommand": "python3 prepare_data.py",
            }
        )
    manifest = {
        "schemaVersion": "1.0",
        "figureId": "fig-r068b2de-strict-components",
        "status": "formal",
        "createdAt": "2026-08-21T02:20:00+08:00",
        "analyticalQuestion": "Which degree-ten eighth-order heat sign components are now strict, and what combined inequality remains numerical?",
        "supportedClaim": "All 4,368 eleventh-order derivative majorants and all 1,792 dominant mass coordinates have exact rational certificates.",
        "claimBoundary": "The displayed positive sign gap still uses binary64 moment, heat, defect, and resolvent quantities. It is not a final heat-sign theorem and makes no Navier-Stokes regularity claim.",
        "git": {
            "sourceCommit": metadata["derivativeSourceCommit"],
            "certificateCommit": metadata["massArchiveCommit"],
            "dirtyAtCertifiedRun": False,
            "derivativeSourceCommit": metadata["derivativeSourceCommit"],
            "derivativeArchiveCommit": metadata["derivativeArchiveCommit"],
            "massSourceCommit": metadata["massSourceCommit"],
            "massArchiveCommit": metadata["massArchiveCommit"],
            "pilotSourceCommit": metadata["pilotSourceCommit"],
            "pilotArchiveCommit": metadata["pilotArchiveCommit"],
            "repository": "Kasifa/Kasifa.github.io",
        },
        "sourceData": source_data,
        "data": [
            record(HERE / "derivative-bounds.csv", format="csv", schema="pure coordinate, exact upper bound, scaled upper, and global-maximum flag"),
            record(HERE / "interval-margins.csv", format="csv", schema="certified width, declared gate, and decimal-order margin"),
            record(HERE / "pilot-budget.csv", format="csv", schema="sign-budget component, magnitude, scaled magnitude, and evidence class"),
            record(HERE / "certified-summary.csv", format="csv", schema="certificate counts, exact-vector hashes, and pilot budget summary"),
            record(HERE / "figure-data-metadata.json", format="json", schema="pinned certificate paths, hashes, and source commits"),
            record(HERE / "figure-data-resources.csv", format="csv", schema="deterministic data-extraction resource record"),
            record(HERE / "plot-resources.csv", format="csv", schema="deterministic rendering resource record"),
        ],
        "computation": {
            "kind": "data-analysis",
            "configuration": "Exact GMP derivative majorant, exact rational dominant-mass residue intervals, and binary64 degree-ten sign-budget diagnostic",
            "precision": "Exact rational panels (a,b); binary64 mixed-evidence panel (c)",
            "solver": "GMP complete homogeneous polynomials, exact degree-33 reachable residue intervals, and archived degree-ten defect pilot",
            "command": "python3 prepare_data.py && python3 validate_data.py && python3 plot.py && python3 build_manifest.py",
            "wallTimeSeconds": sum(
                report["runtime"]["elapsedSeconds"] for report in source_reports
            ),
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
            "gmpy2": "2.3.1",
            "gmp": "6.3.0",
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
            "family": "benchmark bars, interval margins, and sign-budget comparison",
            "takeaway": "the derivative and dominant-mass gates are strict; the combined sign gap remains numerical",
            "nonColorEncoding": "hatching, direct labels, benchmark lines, and explicit evidence classes",
            "outputFootprint": "double-column 178 by 105 millimetres with PDF, SVG, and 600 dpi PNG",
        },
        "qa": {
            "status": "passed",
            "dataCrossChecked": True,
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "notes": "The PNG, SVG, and PDF were inspected at final size; hatching and direct labels preserve evidence classes without color.",
        },
        "caption": {"english": "caption.md"},
    }
    (HERE / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n"
    )


if __name__ == "__main__":
    main()
