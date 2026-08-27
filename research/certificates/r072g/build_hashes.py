#!/usr/bin/env python3
"""Write stable SHA-256 checksums for the R0.72G certificate package."""

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
    OUTPUT.write_text(
        "\n".join(
            f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}"
            for path in paths
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
