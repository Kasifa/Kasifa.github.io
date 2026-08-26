#!/usr/bin/env python3
"""Build the R0.72B-1 formal figure manifest."""

from __future__ import annotations

from datetime import datetime
import hashlib
import json
from pathlib import Path
import subprocess
from zoneinfo import ZoneInfo

from PIL import Image


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
TIMEZONE = ZoneInfo("Asia/Shanghai")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    contract = json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))
    validation = json.loads((ROOT / "validation.json").read_text(encoding="utf-8"))
    if not validation["allPassed"]:
        raise RuntimeError("validation did not pass")
    assets: list[dict[str, object]] = []
    excluded = {"manifest.json", "SHA256SUMS", ".DS_Store"}
    for path in sorted(ROOT.iterdir()):
        if not path.is_file() or path.name in excluded:
            continue
        row: dict[str, object] = {
            "path": path.name,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        if path.suffix.lower() == ".png":
            image = Image.open(path)
            row["pixels"] = [image.width, image.height]
            row["dpi"] = [float(value) for value in image.info.get("dpi", (0.0, 0.0))]
        assets.append(row)
    try:
        source_commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        source_commit = "unknown"
    payload = {
        "schemaVersion": "r072b-figure-manifest-v1",
        "release": "R0.72B",
        "figureId": "R0.72B-1",
        "status": "formal",
        "createdAt": datetime.now(TIMEZONE).isoformat(timespec="seconds"),
        "sourceCommit": source_commit,
        "analyticalQuestion": contract["analyticalQuestion"],
        "supportedClaim": contract["takeaway"],
        "claimBoundary": contract["claimBoundary"],
        "computation": {
            "continuumProofLocation": "research/r072b_report-source.md",
            "producer": "80-digit mpmath algebra and quadrature",
            "independent": "binary64 finite matrix, DOP853, and QUADPACK",
            "intervalArithmetic": False,
            "pdeDNS": False,
            "dgx": False,
            "gpu": False,
            "randomSeed": None,
        },
        "assets": assets,
    }
    (ROOT / "manifest.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"manifest written with {len(assets)} assets")


if __name__ == "__main__":
    main()
