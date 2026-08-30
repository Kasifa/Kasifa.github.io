#!/usr/bin/env python3
"""Seal the completed R0.73L finite diagnostic package."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PATHS = (
    "research/r073l_adiabatic_diagnostic.py",
    "experiments/r073l/README.md",
    "experiments/r073l/config.json",
    "experiments/r073l/requirements.txt",
    "experiments/r073l/command.txt",
    "experiments/r073l/independent_validate.py",
    "experiments/r073l/seal_package.py",
    "experiments/r073l/validate_package.py",
    "experiments/r073l/adiabatic_diagnostic.json",
    "experiments/r073l/progress.ndjson",
    "experiments/r073l/resources.ndjson",
    "experiments/r073l/environment.json",
    "experiments/r073l/independent_validation.json",
    "experiments/r073l/independent_progress.ndjson",
    "experiments/r073l/independent_resources.ndjson",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def record(relative: str) -> dict[str, object]:
    path = ROOT / relative
    if not path.is_file() or path.is_symlink():
        raise RuntimeError("required file is absent: " + relative)
    return {
        "path": relative,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def main() -> int:
    primary = json.loads(
        (HERE / "adiabatic_diagnostic.json").read_text(encoding="utf-8")
    )
    independent = json.loads(
        (HERE / "independent_validation.json").read_text(encoding="utf-8")
    )
    if primary.get("status") != "passed" or not primary.get("allChecksPass"):
        raise RuntimeError("primary diagnostic did not pass")
    if independent.get("status") != "passed" or not independent.get("allChecksPass"):
        raise RuntimeError("independent validation did not pass")
    records = [record(relative) for relative in PATHS]
    manifest = {
        "schemaVersion": "r073l-finite-diagnostic-manifest-v1",
        "release": "R0.73L",
        "createdUtc": datetime.now(timezone.utc).isoformat(),
        "status": "sealed",
        "files": records,
        "checks": {
            "primaryPassed": True,
            "independentValidationPassed": True,
            "allRequiredFilesPresent": True,
        },
        "claimBoundary": {
            "finiteDimensionalDiagnosticSealed": True,
            "continuumTheoremCertifiedByManifest": False,
            "clayProblemSolved": False,
        },
    }
    manifest_path = HERE / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    records_with_manifest = records + [
        record("experiments/r073l/manifest.json")
    ]
    (HERE / "SHA256SUMS").write_text(
        "".join(
            f"{row['sha256']}  {row['path']}\n"
            for row in records_with_manifest
        ),
        encoding="utf-8",
    )
    print(json.dumps({"event": "sealed", "files": len(records_with_manifest)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

