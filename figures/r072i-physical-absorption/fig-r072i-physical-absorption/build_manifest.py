#!/usr/bin/env python3
"""Build the formal R0.72I figure manifest after validation."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent


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

    manifest = {
        "schemaVersion": "r072i-figure-manifest-v1",
        "release": "R0.72I",
        "figureId": "R0.72I-1",
        "status": "formal",
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "analyticalQuestion": "Can every factor in the R0.72H complete-root corollary be absorbed term by term into the critical-log physical payment, and does a failed factorization imply a physical counterfamily?",
        "supportedClaim": "The generic B_A factor is not individually absorbed for delta=M, but odd-carrier parity makes the measured cubic exposure and the resulting physical ledger much smaller; coupling optimization of the proved perturbative scaling envelope still decays.",
        "claimBoundary": contract["claimBoundary"],
        "sourceCommit": source_commit(),
        "sourceFiles": metadata["sourceFiles"],
        "dataSummary": results["summary"],
        "computation": {
            "kind": "data-analysis",
            "intervalArithmetic": False,
            "finiteFitsAreDiagnostics": True,
            "randomSeed": None,
            "producer": "complex Fourier lattice, direct parity observations, DOP853, and Simpson quadrature",
            "independent": "overlaid automatically when an independent certificate CSV is present",
            "continuumProofLocation": "research/r072i_report-source.md",
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
            "dataCrossChecked": True,
        },
        "publication": {
            "localMastersComplete": True,
            "publicCopiesRequiredDuringBuild": False,
            "publisher": "publish_assets.py",
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
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
