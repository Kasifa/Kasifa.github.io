#!/usr/bin/env python3
"""Build the final SHA-256 ledger for the R0.72M certificate bundle."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> None:
    files = sorted(
        path
        for path in ROOT.iterdir()
        if path.is_file() and path.name not in {"SHA256SUMS", ".DS_Store"}
    )
    if not files:
        raise RuntimeError("certificate directory contains no artifacts")
    (ROOT / "SHA256SUMS").write_text(
        "\n".join(f"{digest(path)}  {path.name}" for path in files) + "\n",
        encoding="utf-8",
    )
    print(f"R0.72M certificate SHA256SUMS: {len(files)} files")


if __name__ == "__main__":
    main()
