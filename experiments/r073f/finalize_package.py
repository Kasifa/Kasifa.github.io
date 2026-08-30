#!/usr/bin/env python3
"""Write the R0.73F finite package manifest and SHA-256 ledger."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--directory", type=Path, required=True)
args = parser.parse_args()
directory = args.directory.resolve()
root = directory.parents[1]
summary = json.loads((directory / "summary.json").read_text(encoding="utf-8"))
independent = json.loads(
    (directory / "independent_validation.json").read_text(encoding="utf-8")
)

manifest_path = directory / "manifest.json"
ledger_path = directory / "SHA256SUMS"
excluded = {manifest_path.name, ledger_path.name}
files = []
for path in sorted(directory.iterdir()):
    if path.is_file() and path.name not in excluded:
        files.append({
            "path": f"experiments/r073f/{path.name}",
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })

unexpected_directories = [
    path.name for path in sorted(directory.iterdir()) if path.is_dir()
]
if unexpected_directories:
    raise RuntimeError(
        "archive directory must not contain cache/subdirectories: "
        + ", ".join(unexpected_directories)
    )

source_commit = subprocess.check_output(
    ["git", "rev-parse", "5edb170^{commit}"], cwd=root, text=True
).strip()
analytic_paths = [
    "research/r073f_problem_freeze.md",
    "research/r073f_moving_dichotomy_proof.md",
    "research/r073f_gap_matrix.md",
    "research/r073f_literature_audit.md",
    "research/r073f_independent_analytic_audit.md",
    "research/r073f_report-source.md",
]
analytic_bindings = []
for relative in analytic_paths:
    payload = subprocess.check_output(
        ["git", "show", f"{source_commit}:{relative}"], cwd=root
    )
    analytic_bindings.append({
        "path": relative,
        "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "sourceCommit": source_commit,
    })

manifest = {
    "schemaVersion": "r073f-finite-manifest-v1",
    "release": "R0.73F-finite-diagnostic",
    "createdUtc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "status": "validated" if summary["allPrimaryChecksPass"] and independent["allChecksPass"] else "failed",
    "sourceCommit": source_commit,
    "analyticSourceBindings": analytic_bindings,
    "diagnosticPhysicalEndpoint": summary["diagnosticPhysicalEndpoint"],
    "diagnosticEndpointIsCertifiedD0": False,
    "primaryAllChecksPass": summary["allPrimaryChecksPass"],
    "independentAllChecksPass": independent["allChecksPass"],
    "scientificWallTimeSeconds": summary["scientificWallTimeSeconds"],
    "independentWallTimeSeconds": independent["wallTimeSeconds"],
    "inventoryPolicy": {
        "scope": "all regular files directly inside experiments/r073f",
        "manifestFilesExcludes": ["manifest.json", "SHA256SUMS"],
        "sha256LedgerExcludes": ["SHA256SUMS"],
        "benchmarkIncluded": True,
        "cacheDirectoriesForbidden": True
    },
    "files": files,
    "claimBoundary": summary["claimBoundary"],
}
manifest_path.write_text(
    json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)

ledger_files = sorted(
    path for path in directory.iterdir()
    if path.is_file() and path.name != ledger_path.name
)
ledger_path.write_text(
    "".join(f"{sha256(path)}  {path.name}\n" for path in ledger_files),
    encoding="utf-8",
)
raise SystemExit(0 if manifest["status"] == "validated" else 2)
