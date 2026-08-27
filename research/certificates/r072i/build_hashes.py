#!/usr/bin/env python3
"""Build a stable SHA-256 manifest for the R0.72I certificate bundle."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXCLUDED = {"SHA256SUMS", "__pycache__", ".DS_Store"}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    files = [
        path
        for path in ROOT.iterdir()
        if path.is_file() and path.name not in EXCLUDED
    ]
    lines = [f"{digest(path)}  {path.name}" for path in sorted(files)]
    (ROOT / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
