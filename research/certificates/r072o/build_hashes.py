#!/usr/bin/env python3
"""Build the stable SHA-256 ledger for the R0.72O certificate bundle."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LEDGER = ROOT / "SHA256SUMS"
TEMP_LEDGER = ROOT / ".SHA256SUMS.tmp"
EXCLUDED = {LEDGER.name, TEMP_LEDGER.name, ".DS_Store"}
REQUIRED = {
    "README.md",
    "build_hashes.py",
    "command.txt",
    "crosscheck.json",
    "environment.txt",
    "independent-config.json",
    "independent-degeneracy.csv",
    "independent-environment.txt",
    "independent-exponents.json",
    "independent-monitor.log",
    "independent-progress.ndjson",
    "independent-resource.ndjson",
    "independent-result.json",
    "independent-window.csv",
    "producer-config.json",
    "producer-degeneracy.csv",
    "producer-exponents.json",
    "producer-monitor.log",
    "producer-progress.ndjson",
    "producer-resource.ndjson",
    "producer-result.json",
    "producer-window.csv",
    "write_environment.py",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def artifacts() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.iterdir():
        if path.name in EXCLUDED:
            continue
        if path.is_symlink():
            raise RuntimeError(
                f"certificate artifact must not be a symlink: {path.name}"
            )
        if not path.is_file():
            continue
        if "\n" in path.name or "\r" in path.name:
            raise RuntimeError("certificate artifact name contains a newline")
        files.append(path)

    names = {path.name for path in files}
    missing = sorted(REQUIRED - names)
    if missing:
        raise RuntimeError(
            f"certificate bundle is incomplete: {', '.join(missing)}"
        )
    return sorted(files, key=lambda path: path.name.encode("utf-8"))


def main() -> None:
    files = artifacts()
    payload = "".join(f"{digest(path)}  {path.name}\n" for path in files)
    TEMP_LEDGER.write_text(payload, encoding="utf-8", newline="\n")
    TEMP_LEDGER.replace(LEDGER)
    print(f"R0.72O certificate SHA256SUMS: {len(files)} files")


if __name__ == "__main__":
    main()
