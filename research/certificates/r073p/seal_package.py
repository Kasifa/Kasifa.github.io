#!/usr/bin/env python3
"""Apply or verify the two-stage R0.73P formula-diagnostic provenance seal."""

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
    "README.md",
    "command.txt",
    "config.json",
    "requirements.txt",
    "compute_formula_diagnostic.py",
    "independent_validate.py",
    "assemble_certificate.py",
    "validate_certificate.py",
    "seal_package.py",
}
GENERATED_FILES = {
    "source-data.csv",
    "diagnostic.json",
    "independent_validation.json",
    "certificate.json",
    "validation.json",
    "environment.json",
    "progress.ndjson",
    "resource-log.ndjson",
    "manifest.json",
    "SHA256SUMS",
}
PACKAGE_FILES = SOURCE_FILES | GENERATED_FILES


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument(
        "--source-commit",
        default="",
        help="explicit immutable 40-hex commit containing all nine source files",
    )
    return parser.parse_args()


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(path: Path) -> dict[str, object]:
    return {"path": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_json(path: Path) -> dict:
    require(path.is_file() and not path.is_symlink(), "missing regular JSON: " + path.name)
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), "JSON root is not an object: " + path.name)
    return value


def source_commit_bindings(source_commit: str) -> list[dict[str, object]]:
    require(
        re.fullmatch(r"[0-9a-f]{40}", source_commit) is not None,
        "source commit must be a full lowercase 40-hex hash",
    )
    commit_check = subprocess.run(
        ["git", "cat-file", "-e", source_commit + "^{commit}"],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    require(commit_check.returncode == 0, "source commit is not an available commit object")
    bindings: list[dict[str, object]] = []
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
        match = re.fullmatch(
            r"100(?:644|755) blob ([0-9a-f]+)\t" + re.escape(relative), tree
        )
        require(match is not None, "source commit lacks regular source blob: " + relative)
        blob = subprocess.run(
            ["git", "show", source_commit + ":" + relative],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
        require(
            len(blob) == path.stat().st_size
            and hashlib.sha256(blob).hexdigest() == sha256(path),
            "source commit blob differs from current source: " + relative,
        )
        bindings.append({
            "path": relative,
            "bytes": len(blob),
            "sha256": hashlib.sha256(blob).hexdigest(),
            "gitBlobObjectId": match.group(1),
        })
    return bindings


def verify_ledger() -> None:
    ledger = HERE / "SHA256SUMS"
    require(ledger.is_file() and not ledger.is_symlink(), "SHA256SUMS missing")
    rows = ledger.read_text(encoding="utf-8").strip().splitlines()
    require(len(rows) == 18, "SHA256SUMS line count drift")
    names: list[str] = []
    for row in rows:
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/\\\r\n]+)", row)
        require(match is not None, "invalid SHA256SUMS row: " + row)
        path = HERE / match.group(2)
        require(
            path.is_file() and not path.is_symlink() and sha256(path) == match.group(1),
            "SHA256SUMS binding failed: " + match.group(2),
        )
        names.append(match.group(2))
    require(names == sorted(PACKAGE_FILES - {"SHA256SUMS"}), "SHA256SUMS inventory drift")


def main() -> None:
    args = parse_args()
    for name in PACKAGE_FILES - {"manifest.json", "SHA256SUMS"}:
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), "missing package file: " + name)
    actual = {path.name for path in HERE.iterdir() if path.is_file()}

    if args.verify_only:
        require(actual == PACKAGE_FILES, "hash-bound 19-file inventory drift")
        manifest = load_json(HERE / "manifest.json")
        require(
            manifest.get("schemaVersion") == "r073p-formula-diagnostic-manifest-v1",
            "manifest schema drift",
        )
        require(manifest.get("release") == "R0.73P", "manifest release drift")
        require(manifest.get("allPrerequisiteChecksPass") is True, "manifest prerequisite drift")
        require(manifest.get("inventory") == {
            "sourceFileCount": 9,
            "generatedFileCount": 10,
            "manifestBoundFileCount": 17,
            "sha256SumsLineCount": 18,
            "packageFileCount": 19,
        }, "manifest inventory drift")
        file_rows = manifest.get("files", [])
        require(
            [row.get("path") for row in file_rows]
            == sorted(PACKAGE_FILES - {"manifest.json", "SHA256SUMS"}),
            "manifest file-record inventory drift",
        )
        require(
            all(
                (HERE / row["path"]).is_file()
                and not (HERE / row["path"]).is_symlink()
                and (HERE / row["path"]).stat().st_size == row["bytes"]
                and sha256(HERE / row["path"]) == row["sha256"]
                for row in file_rows
            ),
            "manifest file binding failed",
        )
        require(
            manifest.get("sourceBindings")
            == [record(HERE / name) for name in sorted(SOURCE_FILES)],
            "manifest source bindings drift",
        )
        config = load_json(HERE / "config.json")
        independent = load_json(HERE / "independent_validation.json")
        require(
            manifest.get("claimBoundary") == config.get("claimBoundary")
            and manifest.get("independentClaimBoundary")
            == independent.get("claimBoundary"),
            "manifest claim-boundary drift",
        )
        verify_ledger()
        assigned = manifest.get("sourceCommitAssigned")
        if assigned is True:
            source_commit = manifest.get("sourceCommit")
            require(
                not args.source_commit or args.source_commit == source_commit,
                "requested source commit differs from sealed manifest",
            )
            bindings = source_commit_bindings(str(source_commit))
            require(
                manifest.get("sourceCommitBindings") == bindings,
                "source-commit bindings drift",
            )
            require(
                manifest.get("status") == "sealed"
                and manifest.get("finalSeal") is True,
                "final seal status drift",
            )
            status = "sealed"
        else:
            require(not args.source_commit, "preseal is not bound to the requested commit")
            require(
                manifest.get("status") == "hash-bound-uncommitted"
                and manifest.get("finalSeal") is False,
                "preseal status drift",
            )
            require(
                "sourceCommit" not in manifest
                and "sourceCommitBindings" not in manifest,
                "preseal contains unsupported source-commit claims",
            )
            status = "hash-bound-uncommitted"
        print(canonical({"status": status, "verifyOnly": True, "files": 19}), end="")
        return

    require(
        actual <= PACKAGE_FILES,
        "unexpected file in package: " + repr(sorted(actual - PACKAGE_FILES)),
    )
    config = load_json(HERE / "config.json")
    primary = load_json(HERE / "diagnostic.json")
    independent = load_json(HERE / "independent_validation.json")
    certificate = load_json(HERE / "certificate.json")
    validation = load_json(HERE / "validation.json")
    require(
        all(
            payload.get("allChecksPass") is True
            and payload.get("status") == "passed"
            for payload in (primary, independent, certificate, validation)
        ),
        "cannot seal a failed prerequisite",
    )
    require(
        primary.get("claimBoundary") == config.get("claimBoundary")
        and independent.get("claimBoundary") == config.get("claimBoundary")
        and certificate.get("claimBoundary") == config.get("claimBoundary")
        and validation.get("claimBoundary") == config.get("claimBoundary"),
        "cannot seal claim-boundary drift",
    )
    final = bool(args.source_commit)
    committed_bindings = source_commit_bindings(args.source_commit) if final else None
    manifest = {
        "schemaVersion": "r073p-formula-diagnostic-manifest-v1",
        "release": "R0.73P",
        "status": "sealed" if final else "hash-bound-uncommitted",
        "finalSeal": final,
        "allPrerequisiteChecksPass": True,
        "sourceCommitAssigned": final,
        "sourceCommitAssignedMeaning": (
            "The explicit immutable commit contains byte-identical copies of all nine source files."
            if final
            else "The preseal binds source bytes by SHA-256; an immutable source commit may be assigned later."
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
        "independentClaimBoundary": independent["claimBoundary"],
    }
    if final:
        manifest["sourceCommit"] = args.source_commit
        manifest["sourceCommitBindings"] = committed_bindings
    else:
        manifest["finalSealPendingReason"] = (
            "No immutable R0.73P certificate-source commit was provided."
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
