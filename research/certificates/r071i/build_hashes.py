#!/usr/bin/env python3
"""Build the pinned SHA256SUMS file for the R0.71I release bundle."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


CERTIFICATE = Path(__file__).resolve().parent
ROOT = CERTIFICATE.parents[2]
FIGURE = ROOT / "figures" / "r071i-joint" / "fig-r071i-joint-volume-gap"
PATHS = [
    CERTIFICATE / "README.md",
    CERTIFICATE / "command.txt",
    CERTIFICATE / "environment.txt",
    CERTIFICATE / "result.json",
    CERTIFICATE / "independent-result.json",
    CERTIFICATE / "build_hashes.py",
    ROOT / "research" / "r071i_exact_audit.py",
    ROOT / "research" / "r071i_independent_audit.py",
    ROOT / "research" / "r071i_report-source.md",
    ROOT / "research" / "r071i_gap_matrix.md",
    ROOT / "research" / "r071i_literature_audit.md",
    ROOT / "research" / "r071i_independent_audit.md",
    FIGURE / "manifest.json",
    FIGURE / "data.csv",
    FIGURE / "validation.json",
    FIGURE / "independent-validation.json",
    FIGURE / "figure.pdf",
    FIGURE / "figure.svg",
    FIGURE / "figure.png",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    missing = [path for path in PATHS if not path.is_file()]
    if missing:
        raise FileNotFoundError(
            "missing release inputs: " + ", ".join(map(str, missing))
        )
    lines = []
    for path in PATHS:
        relative = Path(os.path.relpath(path, CERTIFICATE))
        lines.append(f"{sha256(path)}  {relative.as_posix()}")
    (CERTIFICATE / "SHA256SUMS").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
