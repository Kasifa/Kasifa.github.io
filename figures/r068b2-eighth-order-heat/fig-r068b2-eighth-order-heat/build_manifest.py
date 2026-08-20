#!/usr/bin/env python3
"""Build the manifest for Figure R0.68B-2."""

from __future__ import annotations

import csv
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


def peak_rss(path: Path) -> float:
    with path.open(newline="", encoding="utf-8") as stream:
        return max(float(row["rssMiB"]) for row in csv.DictReader(stream))


def main() -> None:
    metadata = json.loads((HERE / "figure-data-metadata.json").read_text())
    one_cycle = ROOT / metadata["oneCycleCertificate"]
    jet = ROOT / metadata["jetPilotArchive"]
    one_cycle_report = json.loads(one_cycle.read_text())
    jet_report = json.loads(jet.read_text())
    png = Image.open(HERE / "figure.png")
    manifest = {
        "schemaVersion": "1.0",
        "figureId": "fig-r068b2-eighth-order-heat",
        "status": "formal",
        "createdAt": "2026-08-21T01:10:00+08:00",
        "analyticalQuestion": "What is already rigorous, and what numerical signal remains to be bounded, in the complete eighth-order heat projection?",
        "supportedClaim": "The complete M=16 seven-simplex heat sum is strictly positive, while the full reachable degree-eight dominant heat jet is a stable negative binary64 signal near -1.4923824320e-8.",
        "claimBoundary": "The first-cycle interval is exact. The degree-eight dominant pairing is exploratory until the zero-eight-jet defect resolvent and the global ninth derivative are bounded. No Navier-Stokes regularity claim is made.",
        "git": {
            "sourceCommit": metadata["jetPilotSourceCommit"],
            "certificateCommit": metadata["jetPilotArchiveCommit"],
            "dirtyAtCertifiedRun": False,
            "oneCycleSourceCommit": metadata["oneCycleSourceCommit"],
            "oneCycleArchiveCommit": metadata["oneCycleArchiveCommit"],
            "jetPilotSourceCommit": metadata["jetPilotSourceCommit"],
            "jetPilotArchiveCommit": metadata["jetPilotArchiveCommit"],
            "repository": "Kasifa/Kasifa.github.io",
        },
        "sourceData": [
            {"fileName": one_cycle.name, "location": str(one_cycle.relative_to(ROOT)), "bytes": one_cycle.stat().st_size, "sha256": metadata["oneCycleSha256"], "extractionCommand": "python3 prepare_data.py"},
            {"fileName": jet.name, "location": str(jet.relative_to(ROOT)), "bytes": jet.stat().st_size, "sha256": metadata["jetPilotSha256"], "extractionCommand": "python3 prepare_data.py"},
        ],
        "data": [
            record(HERE / "state-compression.csv", format="csv", schema="exact suffix depth, retained states, and transitions"),
            record(HERE / "jet-convergence.csv", format="csv", schema="binary64 cumulative heat pairing and increments by degree"),
            record(HERE / "moment-residuals.csv", format="csv", schema="channels, Neumann terms, and relative residual by degree"),
            record(HERE / "certified-summary.csv", format="csv", schema="exact first-cycle interval and degree-eight pilot summary"),
            record(HERE / "figure-data-metadata.json", format="json", schema="pinned archive provenance"),
            record(HERE / "figure-data-resources.csv", format="csv", schema="deterministic extraction resources"),
            record(HERE / "plot-resources.csv", format="csv", schema="rendering resources"),
        ],
        "computation": {
            "kind": "data-analysis",
            "configuration": "Exact M=16 seven-simplex audit plus six-variable degree-eight dominant heat-jet convergence analysis",
            "precision": "Exact integer and rational first-cycle enclosure; binary64 affine moments and heat-jet pairing with two-order cross-check",
            "solver": "Exact suffix-state dynamic program, SciPy sparse subset transfers, Neumann moment solves, and truncated heat Taylor algebra",
            "command": "python3 prepare_data.py && python3 validate_data.py && python3 plot.py && python3 build_manifest.py",
            "wallTimeSeconds": one_cycle_report["runtime"]["elapsedSeconds"] + jet_report["runtime"]["elapsedSeconds"],
            "oneCycle": {
                "kind": "exact rational Taylor audit",
                "configuration": "M=16, 7,823,536 labelled tuples, 35 shuffles, Taylor order 44",
                "wallTimeSeconds": one_cycle_report["runtime"]["elapsedSeconds"],
                "peakRssMiB": peak_rss(ROOT / "research/certificates/r068b2a/resources.csv"),
            },
            "jetPilot": {
                "kind": "binary64 sparse affine-moment convergence pilot",
                "configuration": "1,792 states, six variables, degree eight, 3,003 channels per state, 35 shuffles",
                "wallTimeSeconds": jet_report["runtime"]["elapsedSeconds"],
                "peakRssMiB": peak_rss(ROOT / "research/certificates/r068b2b-pilot/resources.csv"),
            },
        },
        "compute": {"host": "local Mac workstation", "operatingSystem": "macOS 26.6.1 arm64", "cpu": "Apple M5 Max", "gpu": "not used", "memoryGiB": 36, "processes": 1, "threadsPerProcess": 18},
        "environment": {"python": "3.12.13", "numpy": "2.5.2", "scipy": "1.18.0", "matplotlib": "3.11.1", "packagesLock": "research/requirements-r068b.txt"},
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
            "family": "exact state compression, exact interval, and jet-degree convergence",
            "takeaway": "the finite block is rigorously positive and the dominant degree-eight jet is stably negative but not yet certified",
            "nonColorEncoding": "marker shapes, line styles, direct labels, zero lines, and explicit evidence labels",
            "outputFootprint": "double-column 178 by 105 millimetres with PDF, SVG, and 600 dpi PNG",
        },
        "qa": {
            "status": "passed",
            "dataCrossChecked": True,
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "notes": "The 600 dpi PNG, grayscale conversion, and Poppler-rendered PDF were inspected at final size; marker shapes and line styles preserve the distinctions without color.",
        },
        "caption": {"english": "caption.md"},
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
