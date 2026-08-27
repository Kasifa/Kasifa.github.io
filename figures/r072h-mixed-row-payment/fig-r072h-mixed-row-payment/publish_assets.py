#!/usr/bin/env python3
"""Publish byte-identical figure masters to public/figures."""

from __future__ import annotations

import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]


def main() -> None:
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    destination = REPOSITORY / config["publication"]["directory"]
    destination.mkdir(parents=True, exist_ok=True)
    stem = config["publication"]["stem"]
    for suffix in ("pdf", "svg", "png"):
        shutil.copyfile(ROOT / f"figure.{suffix}", destination / f"{stem}.{suffix}")
    print(f"published {stem}.pdf/.svg/.png")


if __name__ == "__main__":
    main()
