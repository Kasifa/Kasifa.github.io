#!/usr/bin/env python3
"""Build the manifest for Figure R0.68B-2f/g/h."""

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
    for key, digest_key in (
        ("momentCertificate", "momentSha256"),
        ("heatCertificate", "heatSha256"),
        ("defectCertificate", "defectSha256"),
        ("verificationCertificate", "verificationSha256"),
    ):
        source = ROOT / metadata[key]
        source_data.append({
            "fileName": source.name,
            "location": str(source.relative_to(ROOT)),
            "bytes": source.stat().st_size,
            "sha256": metadata[digest_key],
            "extractionCommand": "python3 prepare_data.py",
        })
    manifest = {
        "schemaVersion": "1.0",
        "figureId": "fig-r068b2fgh-corrected-heat",
        "status": "formal",
        "createdAt": "2026-08-21T04:10:00+08:00",
        "analyticalQuestion": "Does the guarded degree-ten heat jet remain negative after the complete signature defect and resolvent correction?",
        "supportedClaim": "For one fixed eighth-order coefficient, the corrected dominant-heat interval has a strictly negative upper endpoint.",
        "claimBoundary": metadata["claimBoundary"],
        "git": {
            "momentSourceCommit": metadata["momentSourceCommit"],
            "momentArchiveCommit": metadata["momentArchiveCommit"],
            "heatSourceCommit": metadata["heatSourceCommit"],
            "heatArchiveCommit": metadata["heatArchiveCommit"],
            "defectSourceCommit": metadata["defectSourceCommit"],
            "defectArchiveCommit": metadata["defectArchiveCommit"],
            "dirtyAtCertifiedRuns": False,
            "repository": "Kasifa/Kasifa.github.io",
        },
        "sourceData": source_data,
        "data": [
            record(HERE / "moment-radius-by-degree.csv", format="csv", schema="degree, channel count, raw maximum radius, and global centred maximum radius"),
            record(HERE / "heat-partial-by-degree.csv", format="csv", schema="degree and guarded heat partial interval"),
            record(HERE / "sign-budget.csv", format="csv", schema="heat magnitude lower bound, correction upper bound, and strict residual margin"),
            record(HERE / "certified-summary.csv", format="csv", schema="certificate dimensions, endpoints, hashes, and verification status"),
            record(HERE / "figure-data-metadata.json", format="json", schema="pinned certificate paths, hashes, and commits"),
            record(HERE / "figure-data-resources.csv", format="csv", schema="deterministic data-extraction resource record"),
            record(HERE / "plot-resources.csv", format="csv", schema="deterministic rendering resource record"),
        ],
        "computation": {
            "kind": "guarded interval certificate visualization",
            "configuration": "complete degree-ten moment lift, exact heat time series with strict tail, exact signature compression, and guarded resolvent correction",
            "precision": "exact combinatorics and rationals with guarded IEEE binary128 centre-radius arithmetic",
            "command": "python3 prepare_data.py && python3 validate_data.py && python3 plot.py && python3 build_manifest.py",
            "certifiedWallTimeSeconds": 512.856 + 41.642 + 17.045,
        },
        "compute": {
            "certificateHost": "NVIDIA DGX Spark",
            "architecture": "aarch64",
            "compiler": "GCC 13.3.0",
            "logicalCpuCores": 20,
            "formalDefectThreads": 18,
            "formalDefectMaximumRssKiB": 474984,
            "renderHost": "local Mac workstation",
            "renderGpu": "not used",
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
                record(HERE / "figure.png", dpi=600, pixels=f"{png.width} by {png.height}"),
            ],
        },
        "chartContract": {
            "family": "log-radius convergence, heat partial values, and sign-budget comparison",
            "takeaway": "the complete guarded correction is smaller than the certified heat magnitude for one fixed coefficient",
            "nonColorEncoding": "marker shapes, hatching, direct labels, and explicit bound directions",
            "outputFootprint": "double-column 178 by 105 millimetres with PDF, SVG, and 600 dpi PNG",
        },
        "qa": {
            "status": "passed",
            "dataCrossChecked": True,
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "notes": "The PNG and grayscale render were inspected at final size; markers, hatching, and labels preserve meaning without color.",
        },
        "caption": {"english": "caption.md"},
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
