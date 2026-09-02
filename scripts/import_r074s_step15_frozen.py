#!/usr/bin/env python3
"""Import the immutable R0.74S Step 15 package from its frozen commit."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("/Users/kasifa/Documents/Math/navier-stokes-r074m")
COMMIT = "afb44bc0ecc6db6dbff9a252951ccc9182478717"
FILES = {
    "research/r074s_hybrid_flux_tail_equivalence.md": "2e41f89e2ed13c09f64f09ace1b7884303e9add0b874e934ba210519b8a8ba5d",
    "research/r074s_terminal_crown_coercivity.md": "c62fc127c6d6381075653819a4672cae69f1ac4e2b7b45ee2d0b033ab770fd80",
    "research/r074s_hybrid_crown_primary_audit.md": "4b5a9943d69da7d97cd5214f36fed98f09a7f58cada2139e8ab76e6e07d1ce28",
    "research/r074s_hybrid_crown_independent_audit.md": "805707ea3890bd825f1a63cc10985bc24fd5f297c784d1e8b0a1d1c15ba5fef6",
    "research/r074s_hybrid_crown_certificate_report.md": "6777bc9cbfdaf0d079407e24269822e52bb36ffda13b828bdd7440a554050d87",
    "research/r074s_hybrid_crown_certificate.json": "38e4d15c76b4bb9a2523173c0da816d6862f9e24fe59595d9953a7aa9516a7b8",
    "scripts/r074s_hybrid_crown_certificate.py": "84c1d8aac5399b71a98cefc4a8ff6a0e13835c8a19e47bd5693ac76fe2bcced4",
    "scripts/r074s_hybrid_crown_certificate_independent.rb": "e21f186f65052335a2ad97f1fd3dfdeada0d548c9369b7040adb77436320af0e",
}


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(SOURCE), *args])


def main() -> None:
    head = git("rev-parse", "HEAD").decode().strip()
    if git("cat-file", "-t", COMMIT).decode().strip() != "commit":
        raise RuntimeError(f"frozen commit is unavailable: {COMMIT}")

    imported: list[dict[str, str | int]] = []
    for relative, expected in FILES.items():
        payload = git("show", f"{COMMIT}:{relative}")
        actual = hashlib.sha256(payload).hexdigest()
        if actual != expected:
            raise RuntimeError(f"frozen object hash drift: {relative}: {actual}")
        target = ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        imported.append({"path": relative, "sha256": actual, "bytes": len(payload)})

    if git("rev-parse", "HEAD").decode().strip() != head:
        raise RuntimeError("source HEAD changed during import")
    print(json.dumps({"source": str(SOURCE), "sourceHeadObserved": head, "commit": COMMIT, "readMode": "git-show-frozen-commit-only", "imported": imported}, indent=2))


if __name__ == "__main__":
    main()
