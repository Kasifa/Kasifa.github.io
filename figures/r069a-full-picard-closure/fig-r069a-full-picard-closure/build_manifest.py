#!/usr/bin/env python3
"""Build the formal manifest for Figure R0.69A."""

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
    certificate = ROOT / "research/certificates/r069a/full-picard-target-closure.json"
    png = Image.open(HERE / "figure.png")
    manifest = {
        "schemaVersion": "1.0",
        "figureId": "fig-r069a-full-picard-closure",
        "status": "formal",
        "createdAt": "2026-08-21T04:30:00+08:00",
        "analyticalQuestion": (
            "Does the nonzero quartic target branch survive the complete "
            "Picard series at quartic-critical amplitude?"
        ),
        "supportedClaim": (
            "The complete normalized target coefficient converges to a "
            "strictly greater-than-one interval, while orders six, eight, "
            "and at least ten vanish."
        ),
        "claimBoundary": metadata["claimBoundary"],
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
            record(HERE / "limit-interval.csv", format="csv", schema="strict quartic correction and full normalized limit intervals"),
            record(HERE / "decay-rates.csv", format="csv", schema="sixth, eighth, and all-order-tail contraction rates"),
            record(HERE / "rate-envelopes.csv", format="csv", schema="twenty-one four-bit rate envelopes"),
            record(HERE / "order-status.csv", format="csv", schema="complete Picard-order closure status"),
            record(HERE / "figure-data-metadata.json", format="json", schema="pinned certificate and provenance"),
            record(HERE / "figure-data-resources.csv", format="csv", schema="data extraction resources"),
            record(HERE / "plot-resources.csv", format="csv", schema="rendering resources"),
        ],
        "computation": {
            "kind": "exact-audit plus high-precision presentation sampling",
            "configuration": "periodic 0100 target, quartic-critical amplitude, all Picard orders",
            "precision": "exact rational inputs plus 256-bit directed MPFR enclosure of the quadratic limit",
            "solver": "GMP exact rationals and directed-rounding MPFR interval arithmetic",
            "command": "python3 prepare_data.py && python3 validate_data.py && python3 plot.py && python3 build_manifest.py",
            "scientificWallTimeSeconds": 0.088489,
        },
        "compute": {
            "host": "local Mac workstation",
            "operatingSystem": "macOS 26.6 (Darwin 25.6.0, arm64)",
            "cpu": "Apple M5 Max",
            "memoryGiB": 36,
            "processes": 1,
            "threadsPerProcess": 1,
        },
        "environment": {
            "python": "3.12.13",
            "gmpy2": "2.3.1",
            "mpfr": "4.2.2",
            "matplotlib": "3.11.1",
            "packagesLock": "requirements-research.txt",
        },
        "figure": {
            "script": "plot.py",
            "widthMillimetres": 178,
            "heightMillimetres": 103,
            "profile": "journal-default",
            "outputs": [
                record(HERE / "figure.pdf"),
                record(HERE / "figure.svg"),
                record(HERE / "figure.png", dpi=600, pixels=f"{png.width} by {png.height}"),
            ],
        },
        "chartContract": {
            "family": "strict interval, contraction-rate comparison, and logarithmic rate envelopes",
            "takeaway": "the quartic branch survives the complete Picard sum and every remaining order vanishes at the selected amplitude",
            "nonColorEncoding": "distinct marker shapes, line styles, direct numeric labels, and an interval bar",
            "outputFootprint": "double-column 178 by 103 millimetres with PDF, SVG, and 600 dpi PNG",
        },
        "qa": {
            "status": "passed",
            "dataCrossChecked": True,
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "notes": "The PNG and grayscale PDF render were inspected at final size; line styles and markers preserve meaning without color.",
        },
        "caption": {"english": "caption.md"},
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
