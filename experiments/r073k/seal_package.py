#!/usr/bin/env python3
"""Seal the completed R0.73K finite diagnostic package."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
GENERATED = {"manifest.json", "SHA256SUMS"}
PATHS = (
    "research/r073k_viscous_branch_diagnostic.py",
    "experiments/r073k/README.md",
    "experiments/r073k/config.json",
    "experiments/r073k/requirements.txt",
    "experiments/r073k/command.txt",
    "experiments/r073k/independent_validate.py",
    "experiments/r073k/validate_package.py",
    "experiments/r073k/seal_package.py",
    "experiments/r073k/viscous_branch_diagnostic.json",
    "experiments/r073k/progress.ndjson",
    "experiments/r073k/resources.ndjson",
    "experiments/r073k/environment.json",
    "experiments/r073k/independent_validation.json",
    "experiments/r073k/independent_progress.ndjson",
    "experiments/r073k/independent_resources.ndjson",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def record(relative: str) -> dict[str, object]:
    path = ROOT / relative
    require(path.is_file() and not path.is_symlink(),
            "required package file is absent: " + relative)
    return {"path": relative, "bytes": path.stat().st_size,
            "sha256": sha256(path)}


def main() -> int:
    primary = json.loads(
        (HERE / "viscous_branch_diagnostic.json").read_text(encoding="utf-8")
    )
    independent = json.loads(
        (HERE / "independent_validation.json").read_text(encoding="utf-8")
    )
    require(primary.get("status") == "passed"
            and primary.get("allChecksPass") is True,
            "primary diagnostic did not pass")
    require(independent.get("status") == "passed"
            and independent.get("allChecksPass") is True,
            "independent validation did not pass")
    records = [record(relative) for relative in PATHS]
    manifest = {
        "schemaVersion": "r073k-finite-diagnostic-manifest-v1",
        "release": "R0.73K",
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
            "continuumTheoremCertifiedByThisManifest": False,
            "clayProblemSolved": False,
        },
    }
    manifest_path = HERE / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    checksum_records = records + [record("experiments/r073k/manifest.json")]
    (HERE / "SHA256SUMS").write_text(
        "".join(f"{row['sha256']}  {row['path']}\n" for row in checksum_records),
        encoding="utf-8",
    )
    print(json.dumps({"event": "sealed", "files": len(checksum_records)},
                     sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
