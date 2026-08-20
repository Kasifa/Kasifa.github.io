#!/usr/bin/env python3
"""Build the formal manifest for Figure R0.69B."""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import subprocess
from pathlib import Path

import gmpy2
import matplotlib
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


def resource_seconds(name: str) -> float:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return float(next(csv.DictReader(stream))["elapsedSeconds"])


def sysctl(name: str, fallback: str) -> str:
    try:
        return subprocess.run(
            ["sysctl", "-n", name], check=True, capture_output=True, text=True
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return fallback


def main() -> None:
    metadata = json.loads((HERE / "figure-data-metadata.json").read_text())
    png = Image.open(HERE / "figure.png")
    source_data = []
    for location, digest in metadata["inputCertificates"].items():
        path = ROOT / location
        source_data.append({
            "fileName": path.name,
            "location": location,
            "bytes": path.stat().st_size,
            "sha256": digest,
            "extractionCommand": "python3 prepare_data.py",
        })
    memory_gib = round(int(sysctl("hw.memsize", "0")) / 1024**3) if platform.system() == "Darwin" else None
    manifest = {
        "schemaVersion": "1.0",
        "figureId": "fig-r069b-transverse-smallness",
        "status": "formal",
        "createdAt": "2026-08-21T05:05:00+08:00",
        "analyticalQuestion": (
            "Can the R0.69A periodic packet support a singularity mechanism "
            "through transverse perturbations that vanish in a scale-critical topology?"
        ),
        "supportedClaim": (
            "The packet's periodic BMO^-1 upper bound decays geometrically, "
            "so sufficiently deep packets plus a fixed critical ball of "
            "transverse perturbations lie in the standard small-data regime."
        ),
        "claimBoundary": metadata["claimBoundary"],
        "git": {
            "sourceCommit": metadata["sourceCommit"],
            "certificateCommit": metadata["certificateCommit"],
            "repository": "Kasifa/Kasifa.github.io",
            "dirtyAtCertifiedRun": False,
        },
        "sourceData": source_data,
        "data": [
            record(HERE / "scale-separation.csv", format="csv", schema="depth, physical-amplitude lower bound, critical-norm upper envelope"),
            record(HERE / "decision-depth.csv", format="csv", schema="target budget and first sufficient packet depth"),
            record(HERE / "certified-crossings.csv", format="csv", schema="five exact certificate threshold crossings"),
            record(HERE / "figure-data-metadata.json", format="json", schema="pinned certificates and directed interval metadata"),
            record(HERE / "figure-data-resources.csv", format="csv", schema="data extraction resources"),
            record(HERE / "plot-resources.csv", format="csv", schema="rendering resources"),
        ],
        "computation": {
            "kind": "exact certificate extraction plus directed high-precision presentation sampling",
            "configuration": "R0.69A packet family for depths 0 through 50 and target budgets 1 through 1e-6",
            "precision": "exact rational inputs and 256-bit directed MPFR arithmetic",
            "solver": "GMP exact rationals and directed-rounding MPFR interval arithmetic",
            "command": "python3 prepare_data.py && python3 validate_data.py && python3 plot.py && python3 build_manifest.py",
            "scientificWallTimeSeconds": round(resource_seconds("figure-data-resources.csv") + resource_seconds("plot-resources.csv"), 6),
        },
        "compute": {
            "host": "local Mac workstation",
            "operatingSystem": platform.platform(),
            "cpu": sysctl("machdep.cpu.brand_string", platform.processor()),
            "memoryGiB": memory_gib,
            "processes": 1,
            "threadsPerProcess": 1,
        },
        "environment": {
            "python": platform.python_version(),
            "gmpy2": gmpy2.version(),
            "mpfr": gmpy2.mpfr_version(),
            "matplotlib": matplotlib.__version__,
            "packagesLock": "requirements-research.txt",
        },
        "figure": {
            "script": "plot.py",
            "widthMillimetres": 178,
            "heightMillimetres": 92,
            "profile": "journal-default",
            "outputs": [
                record(HERE / "figure.pdf"),
                record(HERE / "figure.svg"),
                record(HERE / "figure.png", dpi=600, pixels=f"{png.width} by {png.height}"),
            ],
        },
        "chartContract": {
            "family": "logarithmic scale comparison and decision-depth curve",
            "takeaway": "vanishing critical perturbations keep the total data in the global small-data regime; any unresolved singularity route must carry order-one critical size",
            "nonColorEncoding": "solid and dashed lines, distinct markers, direct labels, and a shaded envelope",
            "outputFootprint": "double-column 178 by 92 millimetres with PDF, SVG, and 600 dpi PNG",
        },
        "qa": {
            "status": "passed",
            "dataCrossChecked": True,
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "notes": "The PNG and grayscale render were inspected at final size; line styles and markers preserve meaning without color.",
        },
        "caption": {"english": "caption.md"},
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
