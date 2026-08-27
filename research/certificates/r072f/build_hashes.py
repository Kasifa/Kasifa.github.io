#!/usr/bin/env python3
"""Write stable SHA-256 checksums for the R0.72F certificate package."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "SHA256SUMS"


def main() -> None:
    paths = sorted(
        path
        for path in ROOT.iterdir()
        if path.is_file() and path.name not in {OUTPUT.name, ".DS_Store"}
    )
    lines = [
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}"
        for path in paths
    ]
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
