#!/usr/bin/env python3
"""Build the R0.71Y certificate checksum ledger."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
FILES = [
    ROOT / "README.md",
    ROOT / "command.txt",
    ROOT / "environment.txt",
    ROOT / "build_hashes.py",
    ROOT / "result.json",
    ROOT / "independent-result.json",
    REPO / "research/r071x_gap_matrix.md",
    REPO / "research/r071y_report-source.md",
    REPO / "research/r071y_literature_audit.md",
    REPO / "research/r071y_gap_matrix.md",
    REPO / "research/r071y_independent_audit.md",
    REPO / "research/r071y_exact_audit.py",
    REPO / "research/r071y_independent_audit.py",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    missing = [str(path) for path in FILES if not path.is_file()]
    if missing:
        raise FileNotFoundError(missing)
    lines = []
    for path in FILES:
        try:
            relative = path.relative_to(ROOT)
        except ValueError:
            relative = Path("../../..") / path.relative_to(REPO)
        lines.append(f"{digest(path)}  {relative}")
    (ROOT / "SHA256SUMS").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
