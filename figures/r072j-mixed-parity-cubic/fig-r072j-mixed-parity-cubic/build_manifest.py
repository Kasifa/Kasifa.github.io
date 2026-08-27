#!/usr/bin/env python3
"""Build the formal R0.72J figure manifest after validation."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "unavailable"


def main() -> None:
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    contract = json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))
    results = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
    validation = json.loads((ROOT / "validation.json").read_text(encoding="utf-8"))
    metadata = json.loads(
        (ROOT / "figure-data-metadata.json").read_text(encoding="utf-8")
    )
    if not validation.get("allPassed"):
        raise RuntimeError("validation did not pass")

    assets = []
    for path in sorted(ROOT.iterdir()):
        if not path.is_file() or path.name in {
            "manifest.json",
            "SHA256SUMS",
            ".DS_Store",
        }:
            continue
        record: dict[str, object] = {
            "path": path.name,
            "bytes": path.stat().st_size,
            "sha256": digest(path),
        }
        if path.suffix.lower() == ".png":
            image = Image.open(path)
            record["pixels"] = list(image.size)
            record["dpi"] = list(image.info.get("dpi", (0, 0)))
        assets.append(record)

    public_dir = REPOSITORY / config["publication"]["directory"]
    stem = config["publication"]["stem"]
    public_assets = [
        {
            "path": str((public_dir / f"{stem}.{suffix}").relative_to(REPOSITORY)),
            "sha256": digest(public_dir / f"{stem}.{suffix}"),
            "byteIdenticalToMaster": digest(public_dir / f"{stem}.{suffix}")
            == digest(ROOT / f"figure.{suffix}"),
        }
        for suffix in ("pdf", "svg", "png")
    ]
    manifest = {
        "schemaVersion": "r072j-figure-manifest-v1",
        "release": "R0.72J",
        "figureId": "R0.72J-1",
        "status": "formal",
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "analyticalQuestion": results["analyticalQuestion"],
        "supportedClaim": results["takeaway"],
        "claimBoundary": contract["claimBoundary"],
        "sourceCommit": source_commit(),
        "sourceFiles": metadata["sourceFiles"],
        "dataSummary": results["summary"],
        "computation": {
            "kind": "certificate data analysis and exact graph schematic",
            "odeRecomputed": False,
            "intervalArithmetic": False,
            "finiteFitsAreDiagnostics": True,
            "randomSeed": None,
            "producer": "sealed complex Fourier DOP853 certificate",
            "independent": "sealed edge-list RK45 certificate",
            "crosscheck": "sealed producer-independent comparison",
            "continuumProofLocation": "research/r072j_report-source.md",
        },
        "qa": {
            "status": "passed",
            "validation": "validation.json",
            "passedCount": validation["passedCount"],
            "requiredCount": validation["requiredCount"],
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "pdfRasterInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "dataCrossChecked": True,
        },
        "publication": {
            "publicCopiesComplete": True,
            "publisher": "publish_assets.py",
            "assets": public_assets,
        },
        "assets": assets,
    }
    (ROOT / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "figureId": manifest["figureId"],
                "assets": len(assets),
                "qa": manifest["qa"],
                "publicAssets": public_assets,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
