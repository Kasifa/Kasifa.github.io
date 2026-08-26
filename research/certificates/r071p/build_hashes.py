#!/usr/bin/env python3
"""Build the SHA-256 ledger for the R0.71P certificate bundle."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BUNDLE = Path(__file__).resolve().parent
FIGURE = (
    ROOT
    / "figures"
    / "r071p-positive-entry-batching"
    / "fig-r071p-positive-entry-batching"
)
FILES = [
    BUNDLE / "README.md",
    BUNDLE / "command.txt",
    BUNDLE / "environment.txt",
    BUNDLE / "result.json",
    BUNDLE / "independent-result.json",
    BUNDLE / "build_hashes.py",
    ROOT / "research" / "r071p_exact_audit.py",
    ROOT / "research" / "r071p_independent_audit.py",
    ROOT / "research" / "r071p_report-source.md",
    ROOT / "research" / "r071p_gap_matrix.md",
    ROOT / "research" / "r071p_literature_audit.md",
    ROOT / "research" / "r071p_independent_audit.md",
    ROOT / "public" / "notes" / "r0-71p.html",
    ROOT / "public" / "notes" / "r0-71p.pdf",
    ROOT / "public" / "recap-r0-61-r0-71p.html",
    ROOT / "public" / "recap-r0-61-r0-71p.pdf",
    ROOT / "public" / "figures" / "r0-71p-positive-entry-batching.pdf",
    ROOT / "public" / "figures" / "r0-71p-positive-entry-batching.svg",
    ROOT / "public" / "figures" / "r0-71p-positive-entry-batching.png",
    FIGURE / "README.md",
    FIGURE / "caption.md",
    FIGURE / "contract.json",
    FIGURE / "manifest.json",
    FIGURE / "SHA256SUMS",
    FIGURE / "exact-certificate.json",
    FIGURE / "independent-certificate.json",
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


lines = []
for path in FILES:
    if not path.is_file():
        raise FileNotFoundError(path)
    relative = Path(os.path.relpath(path, BUNDLE))
    lines.append(f"{digest(path)}  {relative}")
(BUNDLE / "SHA256SUMS").write_text(
    "\n".join(lines) + "\n", encoding="utf-8"
)
