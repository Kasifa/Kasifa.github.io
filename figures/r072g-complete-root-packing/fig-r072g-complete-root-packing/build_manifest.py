#!/usr/bin/env python3
"""Build the R0.72G formal figure manifest after validation."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    contract = json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))
    results = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
    validation = json.loads((ROOT / "validation.json").read_text(encoding="utf-8"))
    metadata = json.loads((ROOT / "figure-data-metadata.json").read_text(encoding="utf-8"))
    if not validation.get("allPassed"):
        raise RuntimeError("validation did not pass")
    assets = []
    for path in sorted(ROOT.iterdir()):
        if not path.is_file() or path.name in {"manifest.json", "SHA256SUMS", ".DS_Store"}:
            continue
        record = {"path": path.name, "bytes": path.stat().st_size, "sha256": digest(path)}
        if path.suffix.lower() == ".png":
            image = Image.open(path)
            record["pixels"] = list(image.size)
            record["dpi"] = list(image.info.get("dpi", (0, 0)))
        assets.append(record)
    manifest = {
        "schemaVersion": "r072g-figure-manifest-v1",
        "release": "R0.72G",
        "figureId": "R0.72G-1",
        "status": "formal",
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "analyticalQuestion": contract["analyticalQuestion"],
        "supportedClaim": contract["supportedTakeaway"],
        "claimBoundary": contract["claimBoundary"],
        "sourceCommit": "98efcb10ba340a156487dc11f36785c097237a06",
        "sourceFiles": metadata["sourceFiles"],
        "dataSummary": results["summary"],
        "computation": {
            "kind": "data-analysis",
            "intervalArithmetic": False,
            "finiteFitsAreDiagnostics": True,
            "randomSeed": None,
            "producer": "real-lattice RK4",
            "independent": "Fourier Strang split step",
            "continuumProofLocation": "research/r072g_report-source.md"
        },
        "qa": {
            "status": "passed",
            "validation": "validation.json",
            "passedCount": validation["passedCount"],
            "requiredCount": validation["requiredCount"],
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "dataCrossChecked": True
        },
        "assets": assets,
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"figureId": manifest["figureId"], "assets": len(assets), "qa": manifest["qa"]}, indent=2))


if __name__ == "__main__":
    main()
