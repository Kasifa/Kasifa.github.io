#!/usr/bin/env python3
"""Build the pinned SHA256SUMS file for the R0.71H release bundle."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


CERTIFICATE = Path(__file__).resolve().parent
ROOT = CERTIFICATE.parents[2]
PATHS = [
    CERTIFICATE / "README.md",
    CERTIFICATE / "command.txt",
    CERTIFICATE / "environment.txt",
    CERTIFICATE / "result.json",
    CERTIFICATE / "independent-result.json",
    CERTIFICATE / "build_hashes.py",
    ROOT / "research" / "r071h_exact_audit.py",
    ROOT / "research" / "r071h_independent_audit.py",
    ROOT / "research" / "r071h_report-source.md",
    ROOT / "research" / "r071h_gap_matrix.md",
    ROOT / "research" / "r071h_literature_audit.md",
    ROOT / "research" / "r071h_independent_audit.md",
    ROOT
    / "figures"
    / "r071h-angular"
    / "fig-r071h-angular-curvature"
    / "manifest.json",
    ROOT
    / "figures"
    / "r071h-angular"
    / "fig-r071h-angular-curvature"
    / "data.csv",
    ROOT
    / "figures"
    / "r071h-angular"
    / "fig-r071h-angular-curvature"
    / "figure.pdf",
    ROOT
    / "figures"
    / "r071h-angular"
    / "fig-r071h-angular-curvature"
    / "figure.svg",
    ROOT
    / "figures"
    / "r071h-angular"
    / "fig-r071h-angular-curvature"
    / "figure.png",
]


def main() -> None:
    missing = [path for path in PATHS if not path.is_file()]
    if missing:
        raise FileNotFoundError("missing release inputs: " + ", ".join(map(str, missing)))
    lines = []
    for path in PATHS:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        relative = Path(os.path.relpath(path, CERTIFICATE))
        lines.append(f"{digest}  {relative.as_posix()}")
    (CERTIFICATE / "SHA256SUMS").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
