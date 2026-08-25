#!/usr/bin/env python3
"""Build the pinned SHA256SUMS file for the R0.71K release bundle."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


CERTIFICATE = Path(__file__).resolve().parent
ROOT = CERTIFICATE.parents[2]
FIGURE = ROOT / "figures" / "r071k-matched-cells" / "fig-r071k-matched-cell-gap"
PATHS = [
    CERTIFICATE / "README.md",
    CERTIFICATE / "command.txt",
    CERTIFICATE / "environment.txt",
    CERTIFICATE / "result.json",
    CERTIFICATE / "independent-result.json",
    CERTIFICATE / "build_hashes.py",
    ROOT / "research" / "r071k_exact_audit.py",
    ROOT / "research" / "r071k_independent_audit.py",
    ROOT / "research" / "r071k_report-source.md",
    ROOT / "research" / "r071k_gap_matrix.md",
    ROOT / "research" / "r071k_literature_audit.md",
    ROOT / "research" / "r071k_independent_audit.md",
    FIGURE / "manifest.json",
    FIGURE / "data.csv",
    FIGURE / "figure-data-metadata.json",
    FIGURE / "validation.json",
    FIGURE / "independent-validation.json",
    FIGURE / "figure.pdf",
    FIGURE / "figure.svg",
    FIGURE / "figure.png",
]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> None:
    missing = [path for path in PATHS if not path.is_file()]
    if missing:
        raise FileNotFoundError("missing release inputs: " + ", ".join(map(str, missing)))
    lines = []
    for path in PATHS:
        relative = Path(os.path.relpath(path, CERTIFICATE))
        lines.append(f"{digest(path)}  {relative.as_posix()}")
    (CERTIFICATE / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
