#!/usr/bin/env python3
"""Apply or verify the two-stage R0.73N diagnostic package provenance seal."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_FILES = {
    "README.md", "command.txt", "config.json", "requirements.txt",
    "compute_diagnostic.py", "independent_validate.py", "assemble_certificate.py",
    "validate_certificate.py", "seal_package.py",
}
GENERATED_FILES = {
    "diagnostic.json", "source-data.csv", "independent_validation.json",
    "certificate.json", "validation.json", "environment.json", "progress.ndjson",
    "resource-log.ndjson", "manifest.json", "SHA256SUMS",
}
PACKAGE_FILES = SOURCE_FILES | GENERATED_FILES


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument(
        "--source-commit",
        default="",
        help="immutable 40-hex R0.73N theorem-source commit for final sealing",
    )
    return parser.parse_args()


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(path: Path) -> dict[str, object]:
    return {"path": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}


def source_commit_bindings(source_commit: str) -> list[dict[str, object]]:
    if re.fullmatch(r"[0-9a-f]{40}", source_commit) is None:
        raise RuntimeError("source commit must be a full lowercase 40-hex hash")
    commit_check = subprocess.run(
        ["git", "cat-file", "-e", source_commit + "^{commit}"],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    if commit_check.returncode != 0:
        raise RuntimeError("source commit is not an available commit object")
    bindings = []
    for name in sorted(SOURCE_FILES):
        path = HERE / name
        relative = path.relative_to(ROOT).as_posix()
        tree = subprocess.run(
            ["git", "ls-tree", source_commit, "--", relative],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        match = re.fullmatch(r"100(?:644|755) blob ([0-9a-f]+)\t" + re.escape(relative), tree)
        if match is None:
            raise RuntimeError("source commit lacks a regular source blob: " + relative)
        blob = subprocess.run(
            ["git", "show", source_commit + ":" + relative],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
        committed_sha = hashlib.sha256(blob).hexdigest()
        current_sha = sha256(path)
        if committed_sha != current_sha or len(blob) != path.stat().st_size:
            raise RuntimeError("source commit blob differs from current source: " + relative)
        bindings.append({
            "path": relative,
            "bytes": len(blob),
            "sha256": committed_sha,
            "gitBlobObjectId": match.group(1),
        })
    return bindings


def verify_ledger() -> None:
    rows = (HERE / "SHA256SUMS").read_text(encoding="utf-8").strip().splitlines()
    if len(rows) != len(PACKAGE_FILES) - 1:
        raise RuntimeError("SHA256SUMS line count drift")
    names = []
    for row in rows:
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/\\\r\n]+)", row)
        if match is None:
            raise RuntimeError("invalid SHA256SUMS row: " + row)
        path = HERE / match.group(2)
        if not path.is_file() or path.is_symlink() or sha256(path) != match.group(1):
            raise RuntimeError("SHA256SUMS binding failed: " + match.group(2))
        names.append(match.group(2))
    if names != sorted(PACKAGE_FILES - {"SHA256SUMS"}):
        raise RuntimeError("SHA256SUMS inventory drift")


def main() -> None:
    args = parse_args()
    required_before_seal = PACKAGE_FILES - {"manifest.json", "SHA256SUMS"}
    for name in required_before_seal:
        path = HERE / name
        if not path.is_file() or path.is_symlink():
            raise RuntimeError("missing package file: " + name)
    actual = {path.name for path in HERE.iterdir() if path.is_file()}
    if args.verify_only:
        if actual != PACKAGE_FILES:
            raise RuntimeError("hash-bound 19-file inventory drift")
        manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
        if manifest.get("schemaVersion") != "r073n-finite-strain-manifest-v1":
            raise RuntimeError("manifest schema drift")
        if manifest.get("inventory") != {
            "sourceFileCount": 9,
            "generatedFileCount": 10,
            "manifestBoundFileCount": 17,
            "sha256SumsLineCount": 18,
            "packageFileCount": 19,
        }:
            raise RuntimeError("manifest inventory drift")
        file_rows = manifest.get("files", [])
        if [row.get("path") for row in file_rows] != sorted(
            PACKAGE_FILES - {"manifest.json", "SHA256SUMS"}
        ):
            raise RuntimeError("manifest file-record inventory drift")
        for row in file_rows:
            path = HERE / row["path"]
            if (
                not path.is_file() or path.is_symlink()
                or path.stat().st_size != row["bytes"]
                or sha256(path) != row["sha256"]
            ):
                raise RuntimeError("manifest binding failed: " + row["path"])
        if manifest.get("sourceBindings") != [
            record(HERE / name) for name in sorted(SOURCE_FILES)
        ]:
            raise RuntimeError("manifest source bindings drift")
        verify_ledger()
        assigned = manifest.get("sourceCommitAssigned")
        if assigned is True:
            source_commit = manifest.get("sourceCommit")
            if args.source_commit and args.source_commit != source_commit:
                raise RuntimeError("requested source commit differs from sealed manifest")
            bindings = source_commit_bindings(str(source_commit))
            if manifest.get("sourceCommitBindings") != bindings:
                raise RuntimeError("sealed source-commit bindings drift")
            if manifest.get("status") != "sealed" or manifest.get("finalSeal") is not True:
                raise RuntimeError("sealed package status drift")
            status = "sealed"
        else:
            if args.source_commit:
                raise RuntimeError("manifest is not sealed to the requested source commit")
            if manifest.get("status") != "hash-bound-uncommitted" or manifest.get("finalSeal") is not False:
                raise RuntimeError("uncommitted package status drift")
            if "sourceCommit" in manifest or "sourceCommitBindings" in manifest:
                raise RuntimeError("uncommitted manifest contains source-commit claims")
            status = "hash-bound-uncommitted"
        print(canonical({"status": status, "verifyOnly": True, "files": 19}), end="")
        return
    if not actual <= PACKAGE_FILES:
        raise RuntimeError("unexpected file in package: " + repr(sorted(actual - PACKAGE_FILES)))
    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    primary = json.loads((HERE / "diagnostic.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (HERE / "independent_validation.json").read_text(encoding="utf-8")
    )
    certificate = json.loads((HERE / "certificate.json").read_text(encoding="utf-8"))
    validation = json.loads((HERE / "validation.json").read_text(encoding="utf-8"))
    if not all(payload.get("allChecksPass") is True for payload in (
        primary, independent, certificate, validation,
    )):
        raise RuntimeError("cannot seal failed prerequisite")
    final = bool(args.source_commit)
    committed_bindings = source_commit_bindings(args.source_commit) if final else None
    manifest = {
        "schemaVersion": "r073n-finite-strain-manifest-v1",
        "release": "R0.73N",
        "status": "sealed" if final else "hash-bound-uncommitted",
        "finalSeal": final,
        "allPrerequisiteChecksPass": True,
        "sourceCommitAssigned": final,
        "sourceCommitAssignedMeaning": (
            "The immutable commit contains byte-identical copies of all nine source files."
            if final else
            "The pre-seal state binds source bytes by SHA-256; a parent release may assign "
            "an immutable source commit later."
        ),
        "inventory": {
            "sourceFileCount": 9,
            "generatedFileCount": 10,
            "manifestBoundFileCount": 17,
            "sha256SumsLineCount": 18,
            "packageFileCount": 19,
        },
        "sourceBindings": [record(HERE / name) for name in sorted(SOURCE_FILES)],
        "files": [
            record(HERE / name)
            for name in sorted(PACKAGE_FILES - {"manifest.json", "SHA256SUMS"})
        ],
        "claimBoundary": config["claimBoundary"],
    }
    if final:
        manifest["sourceCommit"] = args.source_commit
        manifest["sourceCommitBindings"] = committed_bindings
    else:
        manifest["finalSealPendingReason"] = (
            "No immutable R0.73N theorem-source commit was provided."
        )
    (HERE / "manifest.json").write_text(canonical(manifest), encoding="utf-8")
    ledger = "".join(
        f"{sha256(HERE / name)}  {name}\n"
        for name in sorted(PACKAGE_FILES - {"SHA256SUMS"})
    )
    (HERE / "SHA256SUMS").write_text(ledger, encoding="utf-8")
    verify_ledger()
    print(canonical({
        "status": "sealed" if final else "hash-bound-uncommitted",
        "verifyOnly": False,
        "files": 19,
        "sourceCommitAssigned": final,
    }), end="")


if __name__ == "__main__":
    main()
