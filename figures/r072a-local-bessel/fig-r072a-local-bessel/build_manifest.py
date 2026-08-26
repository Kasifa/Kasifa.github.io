#!/usr/bin/env python3
"""Build manifest and SHA-256 ledger for Figure R0.72A-1."""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
from zoneinfo import ZoneInfo

from PIL import Image


ROOT = Path(__file__).resolve().parent
ASSETS = (
    "README.md",
    "caption.md",
    "contract.json",
    "config.json",
    "command.txt",
    "environment.txt",
    "requirements.txt",
    "build_figure.py",
    "qa_images.py",
    "validate.py",
    "build_manifest.py",
    "data.csv",
    "data.json",
    "results.json",
    "figure-data-metadata.json",
    "validation.json",
    "progress.ndjson",
    "resource-log.ndjson",
    "figure.pdf",
    "figure.svg",
    "figure.png",
    "qa-original.png",
    "qa-grayscale.png",
    "qa-pdf.png",
    "qa-report.md",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--status", choices=("draft", "formal"), required=True)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    if args.status == "formal" and re.fullmatch(r"[0-9a-f]{40}", args.source_commit) is None:
        raise ValueError("formal source commit must be a full 40-character hash")
    missing = [name for name in ASSETS if not (ROOT / name).is_file()]
    if missing:
        raise FileNotFoundError(f"missing manifest assets: {missing}")
    validation = json.loads((ROOT / "validation.json").read_text(encoding="utf-8"))
    if validation["status"] != "passed":
        raise RuntimeError("validation did not pass")
    contract = json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    records = []
    for name in ASSETS:
        path = ROOT / name
        record: dict[str, object] = {
            "path": name,
            "bytes": path.stat().st_size,
            "sha256": digest(path),
        }
        if path.suffix.lower() == ".png":
            with Image.open(path) as image:
                record["pixels"] = [image.width, image.height]
                record["dpi"] = list(image.info.get("dpi", (0.0, 0.0)))
        records.append(record)
    payload = {
        "schemaVersion": "r072a-figure-manifest-v1",
        "figureId": config["figureId"],
        "release": config["release"],
        "status": args.status,
        "createdAt": datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="seconds"),
        "sourceCommit": args.source_commit,
        "analyticalQuestion": contract["analyticalQuestion"],
        "supportedClaim": contract["takeaway"],
        "claimBoundary": contract["claimBoundary"],
        "assets": records,
        "computation": {
            "producer": "complex DOP853 finite bilateral lattice",
            "independent": "real fixed-step RK4 finite bilateral lattice",
            "randomSeed": None,
            "pdeDNS": False,
            "gpu": False,
            "dgx": False,
            "continuumProofLocation": "research/r072a_report-source.md",
        },
    }
    (ROOT / "manifest.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    lines = [f"{record['sha256']}  {record['path']}" for record in records]
    (ROOT / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"status": args.status, "assets": len(records)}, indent=2))


if __name__ == "__main__":
    main()
