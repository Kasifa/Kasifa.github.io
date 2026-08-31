#!/usr/bin/env python3
"""Create or verify the two-stage provenance seal for R0.73R."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any, Optional, Union


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_FILES = (
    "README.md",
    "assemble_certificate.py",
    "command.txt",
    "compute_formula_diagnostic.py",
    "config.json",
    "independent_validate.py",
    "requirements.txt",
    "seal_package.py",
    "validate_certificate.py",
)
PRESEAL_OUTPUTS = (
    "certificate.json",
    "diagnostic.json",
    "environment.json",
    "independent_validation.json",
    "progress.ndjson",
    "resource-log.ndjson",
    "source-data.csv",
    "validation.json",
)
BOUND_FILES = tuple(sorted(SOURCE_FILES + PRESEAL_OUTPUTS))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit")
    parser.add_argument("--verify-only", action="store_true")
    return parser.parse_args()


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink(), "missing regular JSON: " + str(path))
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), "JSON root is not an object: " + str(path))
    return value


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def record(name: str) -> dict[str, object]:
    path = HERE / name
    require(path.is_file() and not path.is_symlink(), "missing regular package file: " + name)
    return {"bytes": path.stat().st_size, "path": name, "sha256": sha256(path)}


def run_git(arguments: list[str], binary: bool = False) -> Union[str, bytes]:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    require(
        completed.returncode == 0,
        "git command failed: git " + " ".join(arguments) + ": "
        + completed.stderr.decode("utf-8", "replace").strip(),
    )
    return completed.stdout if binary else completed.stdout.decode("utf-8").strip()


def commit_bindings(source_commit: Optional[str]) -> list[dict[str, object]]:
    if source_commit is None:
        return []
    require(re.fullmatch(r"[0-9a-f]{40}", source_commit) is not None, "source commit must be full lowercase 40-hex")
    run_git(["cat-file", "-e", source_commit + "^{commit}"])
    bindings: list[dict[str, object]] = []
    for name in SOURCE_FILES:
        repository_path = (HERE / name).relative_to(ROOT).as_posix()
        committed = run_git(["cat-file", "blob", source_commit + ":" + repository_path], binary=True)
        require(isinstance(committed, bytes), "internal binary git-output error")
        current = (HERE / name).read_bytes()
        require(committed == current, "source commit blob differs from current source: " + repository_path)
        object_id = run_git(["rev-parse", source_commit + ":" + repository_path])
        require(isinstance(object_id, str) and re.fullmatch(r"[0-9a-f]{40,64}", object_id) is not None, "invalid git blob object id")
        bindings.append({
            "bytes": len(current),
            "gitBlobObjectId": object_id,
            "path": repository_path,
            "sha256": sha256_bytes(current),
        })
    return bindings


def build_manifest(source_commit: Optional[str]) -> dict[str, object]:
    config = load_json(HERE / "config.json")
    diagnostic = load_json(HERE / "diagnostic.json")
    independent = load_json(HERE / "independent_validation.json")
    certificate = load_json(HERE / "certificate.json")
    validation = load_json(HERE / "validation.json")
    require(diagnostic.get("allChecksPass") is True, "primary diagnostic did not pass")
    require(independent.get("allChecksPass") is True, "independent validation did not pass")
    require(certificate.get("allPrerequisiteChecksPass") is True, "certificate prerequisites did not pass")
    require(validation.get("allChecksPass") is True, "structural validation did not pass")
    claim = config["claimBoundary"]
    require(
        diagnostic.get("claimBoundary") == claim
        and independent.get("claimBoundary") == claim
        and certificate.get("claimBoundary") == claim
        and validation.get("claimBoundary") == claim,
        "claim-boundary drift across layers",
    )

    files = [record(name) for name in BOUND_FILES]
    sources = [record(name) for name in SOURCE_FILES]
    inventory_config = config["expectedInventory"]
    inventory = {
        "generatedFileCount": len(PRESEAL_OUTPUTS) + 2,
        "manifestBoundFileCount": len(BOUND_FILES),
        "packageFileCount": len(BOUND_FILES) + 2,
        "sha256SumsLineCount": len(BOUND_FILES) + 1,
        "sourceFileCount": len(SOURCE_FILES),
    }
    require(inventory["generatedFileCount"] == int(inventory_config["generatedFileCount"]), "generated-file count drift")
    require(inventory["manifestBoundFileCount"] == int(inventory_config["preSealBoundFileCount"]), "bound-file count drift")
    require(inventory["packageFileCount"] == int(inventory_config["packageFileCount"]), "package-file count drift")
    require(inventory["sha256SumsLineCount"] == int(inventory_config["sha256SumsLineCount"]), "sum-line count drift")
    require(inventory["sourceFileCount"] == int(inventory_config["sourceFileCount"]), "source-file count drift")
    final = source_commit is not None
    return {
        "allPrerequisiteChecksPass": True,
        "checkInventory": {
            "independent": int(independent["checkCount"]),
            "primary": int(diagnostic["checkCount"]),
            "structural": int(validation["checkCount"]),
        },
        "claimBoundary": claim,
        "files": files,
        "finalSeal": final,
        "independentClaimBoundary": independent["claimBoundary"],
        "inventory": inventory,
        "release": "R0.73R",
        "schemaVersion": "r073r-matched-phase-shell-manifest-v1",
        "sourceBindings": sources,
        "sourceCommit": source_commit,
        "sourceCommitAssigned": final,
        "sourceCommitAssignedMeaning": (
            "The explicit immutable commit contains byte-identical copies of all nine source files."
            if final
            else "No immutable source commit has been assigned; this is a hash-bound pre-seal."
        ),
        "sourceCommitBindings": commit_bindings(source_commit),
        "status": "sealed" if final else "hash-bound-uncommitted",
    }


def expected_sums(manifest_text: str) -> str:
    lines = [f"{sha256(HERE / name)}  {name}" for name in BOUND_FILES]
    lines.append(f"{sha256_bytes(manifest_text.encode('utf-8'))}  manifest.json")
    return "\n".join(sorted(lines)) + "\n"


def main() -> None:
    args = parse_args()
    manifest_path = HERE / "manifest.json"
    sums_path = HERE / "SHA256SUMS"
    expected = build_manifest(args.source_commit)
    manifest_text = canonical(expected)
    sums_text = expected_sums(manifest_text)
    if args.verify_only:
        require(manifest_path.is_file() and not manifest_path.is_symlink(), "missing regular manifest.json")
        require(sums_path.is_file() and not sums_path.is_symlink(), "missing regular SHA256SUMS")
        require(manifest_path.read_text(encoding="utf-8") == manifest_text, "manifest.json is stale or inconsistent")
        require(sums_path.read_text(encoding="utf-8") == sums_text, "SHA256SUMS is stale or inconsistent")
    else:
        manifest_path.write_text(manifest_text, encoding="utf-8")
        sums_path.write_text(sums_text, encoding="utf-8")
    print(canonical({
        "finalSeal": expected["finalSeal"],
        "manifestBoundFiles": expected["inventory"]["manifestBoundFileCount"],
        "packageFiles": expected["inventory"]["packageFileCount"],
        "sourceCommitAssigned": expected["sourceCommitAssigned"],
        "status": expected["status"],
        "verifyOnly": args.verify_only,
    }), end="")


if __name__ == "__main__":
    main()
