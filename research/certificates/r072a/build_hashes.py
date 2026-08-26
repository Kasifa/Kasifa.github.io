#!/usr/bin/env python3
"""Build the R0.72A certificate SHA-256 ledger."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ASSETS = (
    "README.md",
    "config.json",
    "command.txt",
    "seed.txt",
    "environment.txt",
    "producer-monitor.log",
    "independent-monitor.log",
    "result.json",
    "independent-result.json",
    "build_hashes.py",
)


def main() -> None:
    missing = [name for name in ASSETS if not (ROOT / name).is_file()]
    if missing:
        raise FileNotFoundError(f"missing certificate assets: {missing}")
    lines = []
    for name in ASSETS:
        digest = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        lines.append(f"{digest}  {name}")
    (ROOT / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {len(lines)} certificate hashes")


if __name__ == "__main__":
    main()
