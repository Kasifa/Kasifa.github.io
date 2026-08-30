#!/usr/bin/env python3
"""Validate a sealed R0.73K finite diagnostic package, fail closed."""

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
REQUIRED_MANIFEST_PATHS = (
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


class PackageFailure(RuntimeError):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path,
        default=HERE / "package_validation.json",
    )
    return parser.parse_args()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PackageFailure(message)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def strict_json(path: Path) -> dict[str, Any]:
    def reject_constant(value: str) -> None:
        raise ValueError("non-finite JSON constant: " + value)

    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            if key in output:
                raise ValueError("duplicate JSON key: " + key)
            output[key] = value
        return output

    value = json.loads(
        path.read_text(encoding="utf-8"),
        parse_constant=reject_constant,
        object_pairs_hook=unique_object,
    )
    require(type(value) is dict, "JSON root must be an object: " + str(path))
    return value


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def resolve_bound_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def validate_ndjson(path: Path, start_event: str, end_event: str) -> int:
    require(path.is_file() and path.stat().st_size > 0,
            "monitoring log is absent or empty: " + str(path))
    events: list[str] = []
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            require(bool(line.strip()),
                    f"blank NDJSON line: {path}:{line_number}")
            row = json.loads(line)
            require(type(row) is dict and type(row.get("event")) is str,
                    f"invalid NDJSON event: {path}:{line_number}")
            for value in row.values():
                if type(value) is float:
                    require(math.isfinite(value),
                            f"non-finite NDJSON value: {path}:{line_number}")
            events.append(row["event"])
    require(events[0] == start_event,
            f"unexpected first event in {path}: {events[0]}")
    require(events[-1] == end_event,
            f"unexpected final event in {path}: {events[-1]}")
    return len(events)


def parse_checksums(path: Path) -> dict[str, str]:
    output: dict[str, str] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        pieces = line.split("  ", 1)
        require(len(pieces) == 2,
                f"malformed checksum line {line_number}")
        digest, relative = pieces
        require(len(digest) == 64 and all(c in "0123456789abcdef" for c in digest),
                f"invalid SHA-256 on line {line_number}")
        require(relative not in output,
                "duplicate checksum path: " + relative)
        output[relative] = digest
    return output


def validate() -> tuple[dict[str, bool], dict[str, object]]:
    config_path = HERE / "config.json"
    primary_path = HERE / "viscous_branch_diagnostic.json"
    environment_path = HERE / "environment.json"
    independent_path = HERE / "independent_validation.json"
    manifest_path = HERE / "manifest.json"
    checksums_path = HERE / "SHA256SUMS"
    for path in (
        config_path, primary_path, environment_path, independent_path,
        manifest_path, checksums_path,
    ):
        require(path.is_file() and not path.is_symlink(),
                "required sealed file is absent: " + str(path))

    config = strict_json(config_path)
    primary = strict_json(primary_path)
    environment = strict_json(environment_path)
    independent = strict_json(independent_path)
    manifest = strict_json(manifest_path)

    schema_checks = (
        config.get("schemaVersion") == "r073k-viscous-branch-config-v1"
        and primary.get("schemaVersion") == "r073k-viscous-branch-diagnostic-v1"
        and environment.get("schemaVersion") == "r073k-finite-diagnostic-environment-v1"
        and independent.get("schemaVersion") == "r073k-independent-finite-validation-v1"
        and manifest.get("schemaVersion") == "r073k-finite-diagnostic-manifest-v1"
    )
    require(schema_checks, "one or more package schemas do not match")
    require(primary.get("status") == "passed"
            and primary.get("allChecksPass") is True,
            "primary pass decision is absent")
    require(independent.get("status") == "passed"
            and independent.get("allChecksPass") is True,
            "independent pass decision is absent")
    require(manifest.get("status") == "sealed",
            "manifest is not sealed")

    records = manifest.get("files")
    require(type(records) is list, "manifest.files is not an array")
    by_path: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(records):
        require(type(row) is dict,
                f"manifest record {index} is not an object")
        require(set(row) == {"path", "bytes", "sha256"},
                f"manifest record {index} has wrong keys")
        relative = row["path"]
        require(type(relative) is str and relative not in by_path,
                f"invalid or duplicate manifest path at record {index}")
        require(relative in REQUIRED_MANIFEST_PATHS,
                "unexpected manifest path: " + relative)
        path = ROOT / relative
        require(path.is_file() and not path.is_symlink(),
                "manifest target is absent: " + relative)
        require(type(row["bytes"]) is int and row["bytes"] == path.stat().st_size,
                "manifest byte count mismatch: " + relative)
        require(row["sha256"] == sha256(path),
                "manifest digest mismatch: " + relative)
        by_path[relative] = row
    require(set(by_path) == set(REQUIRED_MANIFEST_PATHS),
            "manifest required-path set mismatch")

    checksums = parse_checksums(checksums_path)
    expected_checksum_paths = set(REQUIRED_MANIFEST_PATHS) | {
        "experiments/r073k/manifest.json"
    }
    require(set(checksums) == expected_checksum_paths,
            "SHA256SUMS path set mismatch")
    for relative, digest in checksums.items():
        require(digest == sha256(ROOT / relative),
                "SHA256SUMS digest mismatch: " + relative)

    producer = resolve_bound_path(primary["sourceBinding"]["path"])
    bound_config = resolve_bound_path(primary["configurationBinding"]["path"])
    require(producer == ROOT / "research/r073k_viscous_branch_diagnostic.py",
            "primary source binding points elsewhere")
    require(bound_config.resolve() == config_path.resolve(),
            "primary configuration binding points elsewhere")
    require(primary["sourceBinding"]["sha256"] == sha256(producer),
            "primary source binding digest mismatch")
    require(primary["configurationBinding"]["sha256"] == sha256(config_path),
            "primary configuration binding digest mismatch")
    require(environment["configurationSha256"] == sha256(config_path),
            "environment configuration digest mismatch")
    require(independent["primary"]["sha256"] == sha256(primary_path),
            "independent primary digest mismatch")
    require(independent["configuration"]["sha256"] == sha256(config_path),
            "independent configuration digest mismatch")
    independent_source = ROOT / independent["validator"]["path"]
    require(independent_source == HERE / "independent_validate.py",
            "independent validator binding points elsewhere")
    require(independent["validator"]["sha256"] == sha256(independent_source),
            "independent validator digest mismatch")

    config_boundary = config["claimBoundary"]
    primary_boundary = primary["claimBoundary"]
    independent_boundary = independent["claimBoundary"]
    manifest_boundary = manifest["claimBoundary"]
    boundary_closed = (
        config_boundary["finiteDimensionalOnly"] is True
        and config_boundary[
            "continuumTheoremCertifiedByThisConfiguration"
        ] is False
        and config_boundary[
            "explicitContinuumViscosityThresholdCertified"
        ] is False
        and primary_boundary["finiteKineticCompressionComputed"] is True
        and primary_boundary["bothAlgebraicResidualsComputed"] is True
        and primary_boundary["finiteIntertwiningResidualsComputed"] is True
        and primary_boundary[
            "finiteProjectorIdempotencyCheckedByLowRankFormula"
        ] is True
        and primary_boundary[
            "ordinaryCutoffAgreementIsContinuumProof"
        ] is False
        and primary_boundary[
            "fixedCircleCountIsContinuumRieszRankProof"
        ] is False
        and primary_boundary[
            "uniformViscosityThresholdCertifiedHere"
        ] is False
        and primary_boundary[
            "infiniteDimensionalProjectionConvergenceProvedHere"
        ] is False
        and primary_boundary["complementSemigroupBoundProvedHere"] is False
        and primary_boundary["nonlinearNavierStokesProvedHere"] is False
        and primary_boundary["clayProblemSolved"] is False
        and independent_boundary["independentFiniteRecomputation"] is True
        and independent_boundary[
            "continuumTheoremCertifiedByThisValidator"
        ] is False
        and independent_boundary[
            "uniformContinuumViscosityThresholdCertifiedHere"
        ] is False
        and independent_boundary["nonlinearNavierStokesProvedHere"] is False
        and manifest_boundary["finiteDimensionalDiagnosticSealed"] is True
        and manifest_boundary[
            "continuumTheoremCertifiedByThisManifest"
        ] is False
        and manifest_boundary["clayProblemSolved"] is False
    )
    require(boundary_closed, "one or more claim boundaries escaped")

    log_counts = {
        "progress": validate_ndjson(HERE / "progress.ndjson", "start", "complete"),
        "resources": validate_ndjson(HERE / "resources.ndjson", "start", "complete"),
        "independentProgress": validate_ndjson(
            HERE / "independent_progress.ndjson", "start", "complete"
        ),
        "independentResources": validate_ndjson(
            HERE / "independent_resources.ndjson", "start", "complete"
        ),
    }
    checks = {
        "schemasMatch": True,
        "primaryAllChecksPass": True,
        "independentAllChecksPass": True,
        "manifestSealed": True,
        "manifestRecordsMatchFiles": True,
        "sha256SumsMatchFiles": True,
        "sourceAndConfigurationBindingsMatch": True,
        "monitoringLogsComplete": True,
        "claimBoundariesFailClosed": True,
    }
    details: dict[str, object] = {
        "manifestFileCount": len(records),
        "checksumCount": len(checksums),
        "monitoringEventCounts": log_counts,
        "primaryRows": len(primary["rows"]),
        "crossCutoffRows": len(primary["crossCutoffComparisons"]),
    }
    return checks, details


def main() -> int:
    args = parse_args()
    try:
        checks, details = validate()
        output = {
            "schemaVersion": "r073k-package-validation-v1",
            "release": "R0.73K",
            "createdUtc": utc_now(),
            "status": "passed",
            "validator": {
                "path": "experiments/r073k/validate_package.py",
                "sha256": sha256(Path(__file__).resolve()),
            },
            "checks": checks,
            "details": details,
            "allChecksPass": True,
            "claimBoundary": {
                "finitePackageValidated": True,
                "continuumTheoremCertifiedByThisValidation": False,
                "clayProblemSolved": False,
            },
        }
        return_code = 0
    except (PackageFailure, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        output = {
            "schemaVersion": "r073k-package-validation-v1",
            "release": "R0.73K",
            "createdUtc": utc_now(),
            "status": "failed",
            "failure": f"{type(error).__name__}: {error}",
            "checks": {},
            "allChecksPass": False,
            "claimBoundary": {
                "finitePackageValidated": False,
                "continuumTheoremCertifiedByThisValidation": False,
                "clayProblemSolved": False,
            },
        }
        return_code = 2
    atomic_json(args.output, output)
    print(json.dumps({
        "event": "package-validation-complete",
        "status": output["status"],
        "allChecksPass": output["allChecksPass"],
        "output": str(args.output),
    }, sort_keys=True))
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
