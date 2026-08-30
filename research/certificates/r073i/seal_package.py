#!/usr/bin/env python3
"""Seal the flat R0.73I certificate directory with manifest and SHA256."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=Path(__file__).parent)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parsed = args()
    directory = parsed.directory.resolve()
    required = (
        "README.md", "requirements.txt", "command.txt",
        "generate_certificate.py", "independent_recompute.py",
        "validate_certificate.py", "seal_package.py", "certificate.json",
        "independent_recompute.json", "validation.json", "environment.json",
        "progress.ndjson",
    )
    for name in required:
        if not (directory / name).is_file():
            raise RuntimeError("missing package file: " + name)
    certificate = json.loads((directory / "certificate.json").read_text(encoding="utf-8"))
    independent = json.loads((directory / "independent_recompute.json").read_text(encoding="utf-8"))
    validation = json.loads((directory / "validation.json").read_text(encoding="utf-8"))
    if certificate.get("sourceCommit") != parsed.source_commit:
        raise RuntimeError("source commit mismatch")
    if not all(value.get("allChecksPass") is True for value in
               (certificate, independent, validation)):
        raise RuntimeError("a prerequisite package did not pass")
    rows = []
    for name in required:
        path = directory / name
        rows.append({"path": name, "bytes": path.stat().st_size, "sha256": digest(path)})
    manifest = {
        "schemaVersion": "r073i-certificate-manifest-v1",
        "release": "R0.73I",
        "status": "formal",
        "allPrerequisiteChecksPass": True,
        "sourceCommit": parsed.source_commit,
        "evidenceBoundary": {
            "exactArithmeticAndLogicalCounterexamples": True,
            "finiteDiagnosticOnly": True,
            "matchingContinuumGainActionEstablished": False,
            "ClayProblemSolved": False,
        },
        "files": rows,
    }
    if not parsed.write:
        print(json.dumps(manifest, indent=2, sort_keys=True))
        return
    (directory / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    names = sorted(path.name for path in directory.iterdir()
                   if path.is_file() and path.name != "SHA256SUMS")
    (directory / "SHA256SUMS").write_text(
        "".join(f"{digest(directory / name)}  {name}\n" for name in names),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

