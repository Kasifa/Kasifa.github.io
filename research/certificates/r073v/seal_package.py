#!/usr/bin/env python3
"""Create or verify the fail-closed two-path seal for R0.73V."""

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
SOURCE_FILES = (
    "README.md",
    "audit-checklist.json",
    "command.txt",
    "compute_exact_certificate.py",
    "contract.json",
    "independent_recompute.py",
    "requirements.txt",
    "seal_package.py",
)
GENERATED_INPUTS = ("independent-results.json", "results.json")
BOUND_FILES = tuple(sorted(SOURCE_FILES + GENERATED_INPUTS))
MANIFEST = HERE / "manifest.json"
SUMS = HERE / "SHA256SUMS"


def need(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canon(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def load(path: Path) -> dict[str, Any]:
    need(path.is_file() and not path.is_symlink(), "missing regular JSON: " + str(path))
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys)
    need(isinstance(value, dict), "JSON root is not an object: " + str(path))
    return value


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def record(name: str) -> dict[str, object]:
    path = HERE / name
    need(path.is_file() and not path.is_symlink(), "missing regular package file: " + name)
    return {"bytes": path.stat().st_size, "path": name, "sha256": digest(path)}


def run(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[bytes]:
    completed = subprocess.run(command, cwd=cwd, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(
        completed.returncode == 0,
        "command failed: " + " ".join(command) + ": " + completed.stderr.decode("utf-8", "replace").strip(),
    )
    return completed


def git(arguments: list[str], binary: bool = False) -> str | bytes:
    value = run(["git", *arguments]).stdout
    return value if binary else value.decode("utf-8").strip()


def verify_paths() -> tuple[dict[str, Any], dict[str, Any], dict[str, object]]:
    primary_script = HERE / "compute_exact_certificate.py"
    independent_script = HERE / "independent_recompute.py"
    run([sys.executable, "-B", str(primary_script), "--check-only"])
    run([sys.executable, "-B", str(independent_script), "--check-only"])
    primary = load(HERE / "results.json")
    independent = load(HERE / "independent-results.json")
    audit = primary.get("audit")
    need(isinstance(audit, dict), "primary audit missing")
    need(audit.get("passed") == 66 and audit.get("required") == 66, "primary check inventory drift")
    rows = audit.get("results")
    need(isinstance(rows, list) and len(rows) == 66, "primary result rows drift")
    need(all(isinstance(row, dict) and row.get("pass") is True for row in rows), "primary check failure")
    need(primary.get("commonCore") == independent.get("commonCore"), "two-path commonCore mismatch")
    need(primary["producer"]["scriptSha256"] == digest(primary_script), "primary producer hash mismatch")
    need(independent["producer"]["scriptSha256"] == digest(independent_script), "independent producer hash mismatch")
    need(independent["independence"]["importsPrimaryProducer"] is False, "independence flag drift")
    source = independent_script.read_text(encoding="utf-8")
    need("import compute_exact_certificate" not in source, "independent path imports primary producer")
    need("from compute_exact_certificate" not in source, "independent path imports primary producer")
    common_text = canon(primary["commonCore"])
    comparison = {
        "commonCoreByteIdentical": True,
        "commonCoreSha256": digest_bytes(common_text.encode("utf-8")),
        "completeTableDigest": primary["commonCore"]["tableDigest"],
        "independentImportsPrimaryProducer": False,
        "independentPolynomialRepresentation": independent["independence"]["polynomialRepresentation"],
        "primaryPolynomialRepresentation": "sparse exponent-to-Gaussian dictionaries",
    }
    return primary, independent, comparison


def commit_bindings(source_commit: str | None) -> list[dict[str, object]]:
    if source_commit is None:
        return []
    need(re.fullmatch(r"[0-9a-f]{40}", source_commit) is not None, "source commit must be full lowercase 40-hex")
    git(["cat-file", "-e", source_commit + "^{commit}"])
    bindings: list[dict[str, object]] = []
    for name in SOURCE_FILES:
        path = HERE / name
        repository_path = path.relative_to(ROOT).as_posix()
        committed = git(["cat-file", "blob", source_commit + ":" + repository_path], binary=True)
        need(isinstance(committed, bytes), "binary git-output error")
        current = path.read_bytes()
        need(committed == current, "source commit blob differs from current source: " + repository_path)
        object_id = git(["rev-parse", source_commit + ":" + repository_path])
        need(isinstance(object_id, str) and re.fullmatch(r"[0-9a-f]{40,64}", object_id) is not None,
             "invalid git object id: " + repository_path)
        bindings.append({
            "bytes": len(current),
            "gitBlobObjectId": object_id,
            "path": repository_path,
            "sha256": digest_bytes(current),
        })
    return bindings


def build(source_commit: str | None) -> dict[str, object]:
    primary, independent, comparison = verify_paths()
    bindings = commit_bindings(source_commit)
    final = source_commit is not None
    need(len(bindings) == (len(SOURCE_FILES) if final else 0), "source binding inventory drift")
    inventory = {
        "boundFileCount": len(BOUND_FILES),
        "generatedFileCount": len(GENERATED_INPUTS) + 2,
        "packageFileCount": len(BOUND_FILES) + 2,
        "sha256SumsLineCount": len(BOUND_FILES) + 1,
        "sourceFileCount": len(SOURCE_FILES),
    }
    need(inventory == {
        "boundFileCount": 10,
        "generatedFileCount": 4,
        "packageFileCount": 12,
        "sha256SumsLineCount": 11,
        "sourceFileCount": 8,
    }, "package inventory drift")
    return {
        "allPrerequisiteChecksPass": True,
        "arithmetic": primary["arithmetic"],
        "checkInventory": {"exact": 66, "required": 66, "twoPathComparisons": 2},
        "claimBoundary": primary["claimBoundary"],
        "comparison": comparison,
        "files": [record(name) for name in BOUND_FILES],
        "finalSeal": final,
        "inventory": inventory,
        "release": "R0.73V",
        "schemaVersion": "r073v-signed-third-order-exact-manifest-v1",
        "scopeFlags": primary["scope"],
        "sourceBindings": [record(name) for name in SOURCE_FILES],
        "sourceCommit": source_commit,
        "sourceCommitAssigned": final,
        "sourceCommitAssignedMeaning": (
            "The explicit immutable commit contains byte-identical copies of all eight source files."
            if final else
            "No immutable source commit is assigned; this is a hash-bound pre-seal."
        ),
        "sourceCommitBindings": bindings,
        "status": "sealed" if final else "hash-bound-uncommitted",
    }


def sum_text(manifest_text: str) -> str:
    lines = [f"{digest(HERE / name)}  {name}" for name in BOUND_FILES]
    lines.append(f"{digest_bytes(manifest_text.encode('utf-8'))}  manifest.json")
    return "\n".join(sorted(lines)) + "\n"


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit")
    parser.add_argument("--check-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    options = arguments()
    expected = build(options.source_commit)
    manifest_text = canon(expected)
    sums_text = sum_text(manifest_text)
    if options.check_only:
        need(MANIFEST.is_file() and not MANIFEST.is_symlink(), "missing regular manifest.json")
        need(SUMS.is_file() and not SUMS.is_symlink(), "missing regular SHA256SUMS")
        need(MANIFEST.read_text(encoding="utf-8") == manifest_text, "manifest.json is stale")
        need(SUMS.read_text(encoding="utf-8") == sums_text, "SHA256SUMS is stale")
    else:
        MANIFEST.write_text(manifest_text, encoding="utf-8")
        SUMS.write_text(sums_text, encoding="utf-8")
    print(canon({
        "checkOnly": options.check_only,
        "exactChecks": 66,
        "finalSeal": expected["finalSeal"],
        "packageFiles": expected["inventory"]["packageFileCount"],
        "status": expected["status"],
        "twoPathCommonCoreByteIdentical": expected["comparison"]["commonCoreByteIdentical"],
    }), end="")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print("R073V_SEAL=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
