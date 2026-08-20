#!/usr/bin/env python3
"""Build the formal manifest for Figure R0.68A."""

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
    certificate = ROOT / "research/certificates/r068a/all-order-tail-reduction-audit.json"
    png = Image.open(HERE / "figure.png")
    manifest = {
        "schemaVersion": "1.0",
        "figureId": "fig-r068a-all-order-tail",
        "status": "formal",
        "createdAt": "2026-08-20T23:24:00+08:00",
        "analyticalQuestion": (
            "After retaining orders through eight, does the complete periodic "
            "target tail contract at quartic-critical amplitude?"
        ),
        "supportedClaim": (
            "The sum of every target term of order at least ten is less than "
            "(1/30000)(43/64)^r times the quadratic target coefficient."
        ),
        "claimBoundary": (
            "The eighth-order heat term remains open, and the theorem is restricted "
            "to the globally smooth invariant-shear packet."
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
            "sha256": metadata["r068aCertificateSha256"],
            "extractionCommand": "python3 prepare_data.py",
        }],
        "data": [
            record(HERE / "tail-bounds.csv", format="csv", schema="seventeen four-bit tail bounds"),
            record(HERE / "contraction-rates.csv", format="csv", schema="certified and probe contraction factors"),
            record(HERE / "order-status.csv", format="csv", schema="finite-order reduction status"),
            record(HERE / "figure-data-metadata.json", format="json", schema="pinned certificates and provenance"),
            record(HERE / "plot-resources.csv", format="csv", schema="rendering resources"),
        ],
        "computation": {
            "kind": "exact analytic audit",
            "configuration": "sectorwise Dyson chain, p>=9 exponential tail, periodic target m_r=(2M_r+13)/15",
            "precision": "rational and Q(sqrt(2)) comparisons; decimals are display only",
            "command": "python3 research/all_order_tail_reduction_audit.py --output research/certificates/r068a/all-order-tail-reduction-audit.json --progress",
        },
        "environment": {
            "python": "3.12",
            "matplotlib": "3.10.5",
        },
        "figure": {
            "script": "plot.py",
            "widthMillimetres": 178,
            "heightMillimetres": 100,
            "profile": "journal-default",
            "outputs": [
                record(HERE / "figure.pdf"),
                record(HERE / "figure.svg"),
                record(HERE / "figure.png", dpi=600, pixels=f"{png.width} by {png.height}"),
            ],
        },
        "chartContract": {
            "family": "highlighted geometric line, contraction comparison, and order-status strip",
            "takeaway": "the infinite target tail is closed jointly and order eight is the only finite gate",
            "nonColorEncoding": "solid versus dashed lines, filled versus open markers, direct labels, and an open diamond",
            "outputFootprint": "double-column 178 by 100 millimetres with PDF, SVG, and 600 dpi PNG",
        },
        "qa": {
            "status": "passed",
            "dataCrossChecked": True,
            "finalSizeInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "notes": "The PNG and Poppler-rendered PDF were inspected; the open eighth-order gate is not encoded by color alone.",
        },
        "caption": {"english": "caption.md"},
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
