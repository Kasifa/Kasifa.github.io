#!/usr/bin/env python3
"""Copy the three formal figure exports to the public site byte-for-byte."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    destination = REPOSITORY / config["publication"]["directory"]
    destination.mkdir(parents=True, exist_ok=True)
    stem = config["publication"]["stem"]
    for suffix in ("pdf", "svg", "png"):
        source = ROOT / f"figure.{suffix}"
        target = destination / f"{stem}.{suffix}"
        shutil.copyfile(source, target)
        if digest(source) != digest(target):
            raise RuntimeError(f"publication copy differs: {target}")
    print("public PDF/SVG/PNG copies are byte-identical")


if __name__ == "__main__":
    main()
