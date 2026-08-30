#!/usr/bin/env python3
"""Validate the sealed R0.73L finite diagnostic package, fail closed."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REQUIRED = (
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


class PackageFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PackageFailure(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def strict_json(path: Path) -> dict[str, Any]:
    def reject(value: str) -> None:
        raise ValueError("non-finite JSON constant: " + value)

    value = json.loads(path.read_text(encoding="utf-8"), parse_constant=reject)
    require(type(value) is dict, "JSON root is not an object: " + str(path))
    return value


def validate_log(path: Path) -> int:
    require(path.is_file() and path.stat().st_size > 0,
            "monitor log is absent: " + str(path))
    events = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        row = json.loads(line)
        require(type(row) is dict and type(row.get("event")) is str,
                f"bad event at {path}:{line_number}")
        for value in row.values():
            if type(value) is float:
                require(math.isfinite(value),
                        f"non-finite value at {path}:{line_number}")
        events.append(row["event"])
    require(events[0] == "start" and events[-1] == "complete",
            "monitor endpoints are incomplete: " + str(path))
    return len(events)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=HERE / "package_validation.json")
    return parser.parse_args()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def validate() -> tuple[dict[str, bool], dict[str, object]]:
    config_path = HERE / "config.json"
    primary_path = HERE / "adiabatic_diagnostic.json"
    independent_path = HERE / "independent_validation.json"
    environment_path = HERE / "environment.json"
    manifest_path = HERE / "manifest.json"
    checksums_path = HERE / "SHA256SUMS"
    config = strict_json(config_path)
    primary = strict_json(primary_path)
    independent = strict_json(independent_path)
    environment = strict_json(environment_path)
    manifest = strict_json(manifest_path)
    require(config["schemaVersion"] == "r073l-adiabatic-diagnostic-config-v1",
            "configuration schema mismatch")
    require(primary["schemaVersion"] == "r073l-adiabatic-diagnostic-v1",
            "primary schema mismatch")
    require(independent["schemaVersion"] == "r073l-independent-validation-v1",
            "independent schema mismatch")
    require(environment["schemaVersion"] == "r073l-adiabatic-environment-v1",
            "environment schema mismatch")
    require(manifest["schemaVersion"] == "r073l-finite-diagnostic-manifest-v1",
            "manifest schema mismatch")
    require(primary["status"] == "passed" and primary["allChecksPass"] is True,
            "primary pass decision is absent")
    require(independent["status"] == "passed"
            and independent["allChecksPass"] is True,
            "independent pass decision is absent")
    require(manifest["status"] == "sealed", "manifest is not sealed")

    records = {row["path"]: row for row in manifest["files"]}
    require(set(records) == set(REQUIRED), "manifest path set mismatch")
    for relative, row in records.items():
        path = ROOT / relative
        require(path.is_file() and not path.is_symlink(),
                "manifest target missing: " + relative)
        require(path.stat().st_size == row["bytes"],
                "manifest byte mismatch: " + relative)
        require(sha256(path) == row["sha256"],
                "manifest digest mismatch: " + relative)

    checksum_rows = {}
    for line in checksums_path.read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        require(relative not in checksum_rows, "duplicate checksum path")
        checksum_rows[relative] = digest
    expected = set(REQUIRED) | {"experiments/r073l/manifest.json"}
    require(set(checksum_rows) == expected, "checksum path set mismatch")
    for relative, digest in checksum_rows.items():
        require(digest == sha256(ROOT / relative),
                "checksum mismatch: " + relative)

    require(primary["sourceBinding"]["sha256"]
            == sha256(ROOT / primary["sourceBinding"]["path"]),
            "primary source binding mismatch")
    require(primary["configurationBinding"]["sha256"] == sha256(config_path),
            "primary configuration binding mismatch")
    require(environment["configurationSha256"] == sha256(config_path),
            "environment configuration binding mismatch")
    require(independent["sourceBinding"]["sha256"]
            == sha256(ROOT / independent["sourceBinding"]["path"]),
            "independent source binding mismatch")
    require(independent["configurationBinding"]["sha256"] == sha256(config_path),
            "independent configuration binding mismatch")
    require(independent["primaryBinding"]["sha256"] == sha256(primary_path),
            "independent primary binding mismatch")

    event_counts = {
        "primaryProgress": validate_log(HERE / "progress.ndjson"),
        "primaryResources": validate_log(HERE / "resources.ndjson"),
        "independentProgress": validate_log(HERE / "independent_progress.ndjson"),
        "independentResources": validate_log(HERE / "independent_resources.ndjson"),
    }
    boundary = primary["claimBoundary"]
    require(boundary["finiteScalingIsContinuumProof"] is False
            and boundary["finiteCutoffAgreementIsContinuumProof"] is False
            and boundary["clayProblemSolved"] is False,
            "primary claim boundary is open")
    checks = {
        "schemasMatch": True,
        "primaryPassed": True,
        "independentPassed": True,
        "manifestAndChecksumsMatch": True,
        "sourceBindingsMatch": True,
        "monitoringComplete": True,
        "claimBoundaryClosed": True,
    }
    details = {
        "eventCounts": event_counts,
        "manifestFiles": len(records),
        "checksumFiles": len(checksum_rows),
    }
    return checks, details


def main() -> int:
    args = parse_args()
    try:
        checks, details = validate()
        payload = {
            "schemaVersion": "r073l-package-validation-v1",
            "createdUtc": datetime.now(timezone.utc).isoformat(),
            "status": "passed",
            "checks": checks,
            "details": details,
            "allChecksPass": True,
        }
        code = 0
    except (PackageFailure, KeyError, TypeError, ValueError) as error:
        payload = {
            "schemaVersion": "r073l-package-validation-v1",
            "createdUtc": datetime.now(timezone.utc).isoformat(),
            "status": "failed",
            "failure": f"{type(error).__name__}: {error}",
            "allChecksPass": False,
        }
        code = 2
    atomic_json(args.output, payload)
    print(json.dumps({"event": "validation", "status": payload["status"]}))
    return code


if __name__ == "__main__":
    raise SystemExit(main())

