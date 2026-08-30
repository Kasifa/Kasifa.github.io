#!/usr/bin/env python3
"""Seal the R0.73H source/results package with an exact file inventory."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_FILES = (
    "README.md",
    "command.txt",
    "config.json",
    "requirements.txt",
    "exact_q2_certificate.py",
    "independent_exact_q2.py",
    "primary_diagnostic.py",
    "independent_validate.py",
    "generate_certificate.py",
    "validate_certificate.py",
    "seal_package.py",
)
GENERATED_FILES = (
    "exact_q2_certificate.json",
    "independent_exact_q2.json",
    "primary_rows.csv",
    "cutoff_convergence.csv",
    "step_convergence.csv",
    "coefficient_snapshots.npz",
    "environment.json",
    "primary_summary.json",
    "progress.ndjson",
    "primary_manifest.json",
    "independent_validation.json",
    "independent_progress.ndjson",
    "certificate.json",
    "validation.json",
)
SOURCE_RELATIVE = tuple(f"research/certificates/r073h/{name}" for name in SOURCE_FILES)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", default="")
    parser.add_argument("--package-dir", type=Path, default=HERE)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def no_duplicate_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValueError(f"nonfinite JSON constant: {value}")


def load_json(path: Path) -> dict[str, object]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=no_duplicate_pairs,
        parse_constant=reject_constant,
    )
    if not isinstance(value, dict):
        raise ValueError(f"top-level JSON value is not an object: {path.name}")
    return value


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def binding(path: Path, base: Path) -> dict[str, object]:
    if not path.is_file() or path.is_symlink():
        raise RuntimeError(f"expected regular non-symlink file: {path}")
    return {
        "path": path.resolve().relative_to(base.resolve()).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def source_gate(source_commit: str, smoke: bool) -> dict[str, object]:
    if smoke:
        return {"enforced": False, "sourceCommit": None, "allSourceBlobsMatch": False}
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise RuntimeError("formal seal requires a full lowercase source commit")
    resolved = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", f"{source_commit}^{{commit}}"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    if resolved != source_commit:
        raise RuntimeError("source commit did not resolve exactly")
    head = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    if subprocess.run(
        ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", source_commit, head],
        check=False,
    ).returncode != 0:
        raise RuntimeError("source commit is not an ancestor of HEAD")
    bindings = []
    for relative in SOURCE_RELATIVE:
        path = ROOT / relative
        tree = subprocess.run(
            ["git", "-C", str(ROOT), "ls-tree", source_commit, relative],
            check=True, capture_output=True, text=True,
        ).stdout.split()
        if len(tree) < 3 or tree[0] not in {"100644", "100755"}:
            raise RuntimeError(f"source is not a regular Git blob: {relative}")
        committed = subprocess.run(
            ["git", "-C", str(ROOT), "show", f"{source_commit}:{relative}"],
            check=True, capture_output=True,
        ).stdout
        working = path.read_bytes()
        if committed != working:
            raise RuntimeError(f"working source differs from source commit: {relative}")
        bindings.append({
            "path": relative,
            "gitMode": tree[0],
            "bytes": len(working),
            "sha256": hashlib.sha256(working).hexdigest(),
        })
    return {
        "enforced": True,
        "sourceCommit": source_commit,
        "headAtSeal": head,
        "sourceCommitIsAncestorOfHead": True,
        "allSourceBlobsMatch": True,
        "bindings": bindings,
    }


def provenance_matches(value: object, smoke: bool, source_commit: str) -> bool:
    if not isinstance(value, dict):
        return False
    if smoke:
        return value.get("enforced") is False and value.get("sourceCommit") is None
    return (
        value.get("enforced") is True
        and value.get("sourceCommit") == source_commit
        and value.get("allSourceBlobsMatch") is True
    )


def main() -> int:
    args = parse_args()
    package = args.package_dir.resolve()
    if args.smoke:
        if is_within(package, HERE):
            raise RuntimeError("smoke seal package must be outside the formal source tree")
    elif package != HERE.resolve():
        raise RuntimeError("formal seal must use research/certificates/r073h")
    provenance = source_gate(args.source_commit, args.smoke)
    expected = set(GENERATED_FILES if args.smoke else SOURCE_FILES + GENERATED_FILES)
    manifest_path = package / "manifest.json"
    sums_path = package / "SHA256SUMS"
    if (manifest_path.exists() or sums_path.exists()) and not args.overwrite:
        raise RuntimeError("refusing to overwrite an existing seal without --overwrite")
    for name in expected:
        binding(package / name, package)
    actual = {path.name for path in package.iterdir() if path.is_file() and not path.is_symlink()}
    symlinks = {path.name for path in package.iterdir() if path.is_symlink()}
    allowed_existing = expected | ({"manifest.json", "SHA256SUMS"} if args.overwrite else set())
    if actual != allowed_existing or symlinks:
        missing = sorted(expected - actual)
        extra = sorted(actual - allowed_existing)
        raise RuntimeError(f"package inventory mismatch before seal; missing={missing}, extra={extra}, symlinks={sorted(symlinks)}")

    certificate = load_json(package / "certificate.json")
    validation = load_json(package / "validation.json")
    prerequisites_pass = (
        certificate.get("allChecksPass") is True
        and validation.get("allChecksPass") is True
        and certificate.get("smokeMode") is args.smoke
        and validation.get("smokeMode") is args.smoke
        and provenance_matches(certificate.get("sourceProvenance"), args.smoke, args.source_commit)
        and provenance_matches(validation.get("sourceProvenance"), args.smoke, args.source_commit)
    )
    if not prerequisites_pass:
        raise RuntimeError("certificate or validation prerequisite did not pass")
    manifest = {
        "schemaVersion": "r073h-sealed-package-manifest-v1",
        "release": "R0.73H",
        "smokeMode": args.smoke,
        "sourceCommit": None if args.smoke else args.source_commit,
        "inventory": {
            "sourceFileCount": 0 if args.smoke else len(SOURCE_FILES),
            "generatedFileCount": len(GENERATED_FILES),
            "manifestFileCount": len(expected),
            "sha256SumsLineCount": len(expected) + 1,
        },
        "files": [binding(package / name, package) for name in sorted(expected)],
        "allPrerequisiteChecksPass": prerequisites_pass,
        "claimBoundary": {
            "exactRationalComponentIsContinuumProofSubcertificateOnly": True,
            "numericalComponentIsFiniteBinary64GalerkinDiagnosticOnly": True,
            "ordinaryCutoffAgreementIsTailProof": False,
            "generalThreeDimensionalRegularityConclusion": False,
            "Clay": False,
        },
    }
    manifest_temporary = package / ".manifest.json.tmp"
    sums_temporary = package / ".SHA256SUMS.tmp"
    manifest_temporary.write_text(canonical(manifest), encoding="utf-8")
    checksum_rows = []
    for name in sorted(expected):
        checksum_rows.append(f"{sha256(package / name)}  {name}")
    checksum_rows.append(f"{sha256(manifest_temporary)}  manifest.json")
    checksum_rows.sort(key=lambda row: row.split("  ", 1)[1])
    sums_temporary.write_text("\n".join(checksum_rows) + "\n", encoding="ascii")
    os.replace(manifest_temporary, manifest_path)
    os.replace(sums_temporary, sums_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
