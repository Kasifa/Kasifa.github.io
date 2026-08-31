#!/usr/bin/env python3
"""Create or verify the fail-closed R0.73U analytic/certificate seal.

The top-level sourceCommit is the frozen four-file analytic source commit.
Certificate sources are hash-bound immediately and have a separate optional
certificateSourceCommit for the later immutable-source final-seal stage.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

ANALYTIC_SOURCE_COMMIT = "84e808dae473f6381cbf9df55a71f5fe81a1cfce"
OBSOLETE_ANALYTIC_SOURCE_COMMIT = "72493751370aa948947000df169e21199fc5c95d"
ANALYTIC_SOURCE_FILES = (
    "research/r073u_problem_freeze.md",
    "research/r073u_tensor_heat_hierarchy.md",
    "research/r073u_independent_analytic_audit.md",
    "research/r073u_primary_literature_audit.md",
)
SOURCE_FILES = (
    "README.md",
    "audit-checklist.json",
    "command.txt",
    "compute_exact_certificate.py",
    "requirements.txt",
    "seal_package.py",
)
PRESEAL_OUTPUTS = ("results.json",)
BOUND_FILES = tuple(sorted(SOURCE_FILES + PRESEAL_OUTPUTS))
MANIFEST_PATH = HERE / "manifest.json"
SUMS_PATH = HERE / "SHA256SUMS"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    output: dict[str, object] = {}
    for key, value in pairs:
        require(key not in output, "duplicate JSON key: " + key)
        output[key] = value
    return output


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink(), "missing regular JSON: " + str(path))
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate_keys,
    )
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
    return {
        "bytes": path.stat().st_size,
        "path": name,
        "sha256": sha256(path),
    }


def run_process(arguments: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[bytes]:
    completed = subprocess.run(
        arguments,
        cwd=cwd,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    require(
        completed.returncode == 0,
        "command failed: " + " ".join(arguments) + ": "
        + completed.stderr.decode("utf-8", "replace").strip(),
    )
    return completed


def run_git(arguments: list[str], binary: bool = False) -> str | bytes:
    completed = run_process(["git", *arguments])
    if binary:
        return completed.stdout
    return completed.stdout.decode("utf-8").strip()


def verify_exact_results() -> dict[str, Any]:
    producer = HERE / "compute_exact_certificate.py"
    require(producer.is_file() and not producer.is_symlink(), "missing regular exact producer")
    run_process([sys.executable, "-B", str(producer), "--check-only"])
    results = load_json(HERE / "results.json")
    audit = results.get("audit")
    require(isinstance(audit, dict), "results audit is missing")
    require(audit.get("passed") == 75, "results passed-check count drift")
    require(audit.get("required") == 75, "results required-check count drift")
    rows = audit.get("results")
    require(isinstance(rows, list) and len(rows) == 75, "results check inventory drift")
    require(
        all(isinstance(row, dict) and row.get("pass") is True for row in rows),
        "one or more exact checks did not pass",
    )
    producer_metadata = results.get("producer")
    require(isinstance(producer_metadata, dict), "results producer metadata is missing")
    require(producer_metadata.get("standardLibraryOnly") is True,
            "standard-library-only boundary drift")
    require(producer_metadata.get("gpu") == "not used", "GPU boundary drift")
    require(producer_metadata.get("network") == "not used", "network boundary drift")
    require(producer_metadata.get("dgx") == "not used", "DGX boundary drift")
    require(producer_metadata.get("ordinaryTranslationPath") == "LOCAL_DIRECT_NO_DGX",
            "ordinary translation boundary drift")
    require(producer_metadata.get("scriptSha256") == sha256(producer),
            "results producer hash differs from current script")
    checklist = HERE / "audit-checklist.json"
    require(audit.get("checklistSha256") == sha256(checklist),
            "results checklist hash differs from current checklist")
    return results


def valid_commit(commit: str, label: str) -> None:
    require(
        re.fullmatch(r"[0-9a-f]{40}", commit) is not None,
        label + " must be full lowercase 40-hex",
    )
    run_git(["cat-file", "-e", commit + "^{commit}"])


def analytic_source_bindings(commit: str) -> list[dict[str, object]]:
    require(commit != OBSOLETE_ANALYTIC_SOURCE_COMMIT,
            "obsolete analytic source commit is explicitly rejected")
    require(commit == ANALYTIC_SOURCE_COMMIT,
            "analytic source commit differs from the frozen R0.73U commit")
    valid_commit(commit, "analytic source commit")
    bindings: list[dict[str, object]] = []
    for repository_path in ANALYTIC_SOURCE_FILES:
        committed = run_git(["cat-file", "blob", commit + ":" + repository_path], binary=True)
        require(isinstance(committed, bytes), "internal binary git-output error")
        current_path = ROOT / repository_path
        require(current_path.is_file() and not current_path.is_symlink(),
                "missing regular analytic source: " + repository_path)
        current = current_path.read_bytes()
        require(current == committed,
                "working analytic source differs from frozen commit: " + repository_path)
        object_id = run_git(["rev-parse", commit + ":" + repository_path])
        require(isinstance(object_id, str)
                and re.fullmatch(r"[0-9a-f]{40,64}", object_id) is not None,
                "invalid analytic Git blob object id: " + repository_path)
        bindings.append({
            "bytes": len(committed),
            "gitBlobObjectId": object_id,
            "path": repository_path,
            "sha256": sha256_bytes(committed),
        })
    require(len(bindings) == 4, "analytic binding inventory drift")
    return bindings


def certificate_commit_bindings(commit: str | None) -> list[dict[str, object]]:
    if commit is None:
        return []
    valid_commit(commit, "certificate source commit")
    bindings: list[dict[str, object]] = []
    for name in SOURCE_FILES:
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), "missing regular source file: " + name)
        repository_path = path.relative_to(ROOT).as_posix()
        committed = run_git(["cat-file", "blob", commit + ":" + repository_path], binary=True)
        require(isinstance(committed, bytes), "internal binary git-output error")
        current = path.read_bytes()
        require(committed == current,
                "certificate source commit blob differs from current source: " + repository_path)
        object_id = run_git(["rev-parse", commit + ":" + repository_path])
        require(isinstance(object_id, str)
                and re.fullmatch(r"[0-9a-f]{40,64}", object_id) is not None,
                "invalid certificate Git blob object id: " + repository_path)
        bindings.append({
            "bytes": len(current),
            "gitBlobObjectId": object_id,
            "path": repository_path,
            "sha256": sha256_bytes(current),
        })
    return bindings


def build_manifest(
    analytic_commit: str,
    certificate_commit: str | None,
) -> dict[str, object]:
    results = verify_exact_results()
    analytic_bindings = analytic_source_bindings(analytic_commit)
    certificate_bindings = certificate_commit_bindings(certificate_commit)
    final = certificate_commit is not None
    require(len(certificate_bindings) == (len(SOURCE_FILES) if final else 0),
            "certificate source commit binding inventory drift")
    files = [record(name) for name in BOUND_FILES]
    sources = [record(name) for name in SOURCE_FILES]
    inventory = {
        "analyticSourceFileCount": len(ANALYTIC_SOURCE_FILES),
        "boundFileCount": len(BOUND_FILES),
        "generatedFileCount": len(PRESEAL_OUTPUTS) + 2,
        "packageFileCount": len(BOUND_FILES) + 2,
        "sha256SumsLineCount": len(BOUND_FILES) + 1,
        "sourceFileCount": len(SOURCE_FILES),
    }
    require(inventory == {
        "analyticSourceFileCount": 4,
        "boundFileCount": 7,
        "generatedFileCount": 3,
        "packageFileCount": 9,
        "sha256SumsLineCount": 8,
        "sourceFileCount": 6,
    }, "sealed inventory drift")
    return {
        "allPrerequisiteChecksPass": True,
        "analyticSourceBindings": analytic_bindings,
        "analyticSourceCommit": analytic_commit,
        "analyticSourceCommitAssigned": True,
        "arithmetic": results["arithmetic"],
        "certificateSourceBindings": sources,
        "certificateSourceCommit": certificate_commit,
        "certificateSourceCommitAssigned": final,
        "certificateSourceCommitAssignedMeaning": (
            "The explicit immutable certificate commit contains byte-identical copies of all six certificate source files."
            if final else
            "Certificate sources are SHA-256-bound but no immutable certificate source commit is assigned yet."
        ),
        "certificateSourceCommitBindings": certificate_bindings,
        "checkInventory": {
            "exact": int(results["audit"]["passed"]),
            "required": int(results["audit"]["required"]),
        },
        "claimBoundary": results["claimBoundary"],
        "files": files,
        "finalSeal": final,
        "inventory": inventory,
        "obsoleteAnalyticSourceCommit": OBSOLETE_ANALYTIC_SOURCE_COMMIT,
        "obsoleteAnalyticSourceCommitAccepted": False,
        "release": "R0.73U",
        "schemaVersion": "r073u-exact-tensor-heat-manifest-v1",
        "sourceBindings": analytic_bindings,
        "sourceCommit": analytic_commit,
        "sourceCommitAssigned": True,
        "sourceCommitAssignedMeaning": (
            "sourceCommit is the frozen four-file analytic source commit; "
            "certificate immutability is tracked separately by certificateSourceCommit."
        ),
        "sourceCommitBindings": analytic_bindings,
        "status": "sealed" if final else "analytic-source-bound-certificate-hash-bound",
    }


def expected_sums(manifest_text: str) -> str:
    lines = [f"{sha256(HERE / name)}  {name}" for name in BOUND_FILES]
    lines.append(f"{sha256_bytes(manifest_text.encode('utf-8'))}  manifest.json")
    return "\n".join(sorted(lines)) + "\n"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--analytic-source-commit",
        default=ANALYTIC_SOURCE_COMMIT,
        help="must equal the frozen four-file analytic source commit",
    )
    parser.add_argument(
        "--certificate-source-commit",
        help="optional immutable commit containing all six certificate source files",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="verify manifest.json and SHA256SUMS without writing",
    )
    return parser.parse_args()


def main() -> int:
    options = parse_arguments()
    expected = build_manifest(
        options.analytic_source_commit,
        options.certificate_source_commit,
    )
    manifest_text = canonical(expected)
    sums_text = expected_sums(manifest_text)
    if options.check_only:
        require(MANIFEST_PATH.is_file() and not MANIFEST_PATH.is_symlink(),
                "missing regular manifest.json")
        require(SUMS_PATH.is_file() and not SUMS_PATH.is_symlink(),
                "missing regular SHA256SUMS")
        require(MANIFEST_PATH.read_text(encoding="utf-8") == manifest_text,
                "manifest.json is stale or inconsistent")
        require(SUMS_PATH.read_text(encoding="utf-8") == sums_text,
                "SHA256SUMS is stale or inconsistent")
    else:
        MANIFEST_PATH.write_text(manifest_text, encoding="utf-8")
        SUMS_PATH.write_text(sums_text, encoding="utf-8")
    print(canonical({
        "analyticSourceCommit": expected["analyticSourceCommit"],
        "certificateSourceCommitAssigned": expected["certificateSourceCommitAssigned"],
        "checkOnly": options.check_only,
        "exactChecks": expected["checkInventory"]["exact"],
        "finalSeal": expected["finalSeal"],
        "manifestBoundFiles": expected["inventory"]["boundFileCount"],
        "packageFiles": expected["inventory"]["packageFileCount"],
        "status": expected["status"],
    }), end="")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"R073U_SEAL=FAIL {error}", file=sys.stderr)
        raise SystemExit(1)
