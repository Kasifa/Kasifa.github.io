#!/usr/bin/env python3
"""Build or verify the R0.73X source-commit-bound evidence archive."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Any


HERE = Path(__file__).resolve().parent
DEFAULT_REPOSITORY = HERE.parents[2]
SOURCE_FILES = (
    "README.md",
    "audit-checklist.json",
    "claim-boundary.md",
    "command.txt",
    "contract.json",
    "requirements.txt",
    "seal_package.py",
)
EVIDENCE = (
    (
        "scripts/r073x_gaussian_tail_certificate.py",
        "gaussian-producer.py",
        "d2708a1cc267fb61dcbd1ecb4c00be46b9746175c0b5a77dab044e8138590925",
    ),
    (
        "research/r073x_gaussian_tail_certificate.json",
        "gaussian-results.json",
        "136b40fb6d30d4fd671e5dc3049817266986f595da46e9a6b6a31a409fe3f836",
    ),
    (
        "research/r073x_gaussian_tail_certificate_report.md",
        "gaussian-report.md",
        "e678ee897e2e574fd3cc3b5bb674fc82524c7897a7546786c4958704c03ab248",
    ),
    (
        "research/r073x_gaussian_tail_independent_audit.md",
        "gaussian-independent-audit.md",
        "9ecbc927a25eb95c23604bfbe85c1c633a83cd4765d1405d626ea006ef9a706a",
    ),
    (
        "scripts/r073x_finite_fourier_harness.py",
        "fourier-producer.py",
        "c34a8ed89a9ae3e8c16b965781ff1947ec41128617dc4548ac53c0f66974c3cd",
    ),
    (
        "research/r073x_finite_fourier_harness_results.json",
        "fourier-results.json",
        "c25c7dc8841628d5cc18cb7198251f1ce6beda58a17da300bb08c0738d19eb30",
    ),
    (
        "research/r073x_finite_fourier_harness_report.md",
        "fourier-report.md",
        "f4a83107ab8f8a0f50d11cf41b245566ec5c584f50406111eeda35d114b0cb34",
    ),
)
ARCHIVE_FILES = tuple(item[1] for item in EVIDENCE)
BOUND_FILES = tuple(sorted(SOURCE_FILES + ARCHIVE_FILES))
MANIFEST = HERE / "manifest.json"
SUMS = HERE / "SHA256SUMS"
EXPECTED_FILES = set(BOUND_FILES) | {"manifest.json", "SHA256SUMS"}


def need(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def reject_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    need(path.is_file() and not path.is_symlink(), "missing regular JSON: " + str(path))
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    need(isinstance(value, dict), "JSON root must be an object: " + str(path))
    return value


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256(path: Path) -> str:
    need(path.is_file() and not path.is_symlink(), "missing regular file: " + str(path))
    return sha256_bytes(path.read_bytes())


def run_git(repository: Path, *arguments: str, binary: bool = False) -> str | bytes:
    completed = subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=True,
        capture_output=True,
        text=not binary,
    )
    return completed.stdout


def run_producer(repository: Path, relative: str, required_tokens: tuple[str, ...]) -> str:
    completed = subprocess.run(
        [sys.executable, "-B", str(repository / relative), "--check-only"],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    )
    for token in required_tokens:
        need(token in completed.stdout, f"producer output missing token {token!r}")
    return completed.stdout


def verify_gaussian_regeneration(repository: Path) -> None:
    script = repository / "scripts/r073x_gaussian_tail_certificate.py"
    spec = importlib.util.spec_from_file_location("r073x_gaussian_certificate_seal", script)
    need(spec is not None and spec.loader is not None, "cannot load Gaussian producer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    regenerated = module.generate()
    stored = (repository / "research/r073x_gaussian_tail_certificate.json").read_text(encoding="utf-8")
    need(module.canonical(regenerated) == stored, "Gaussian stored result is stale")


def validate_claims(repository: Path) -> dict[str, object]:
    gaussian = load_json(repository / "research/r073x_gaussian_tail_certificate.json")
    fourier = load_json(repository / "research/r073x_finite_fourier_harness_results.json")
    audit = (repository / "research/r073x_gaussian_tail_independent_audit.md").read_text(encoding="utf-8")
    need(gaussian.get("overall") == "PASS", "Gaussian overall is not PASS")
    need(
        gaussian.get("payload_sha256")
        == "fcac97440dde87d00103f3a09b346bdd918c9fbb7360ee792edc2c8d0357e3b7",
        "Gaussian payload digest mismatch",
    )
    need(gaussian["claim_boundary"]["pde_regularization"] is False, "Gaussian PDE boundary widened")
    need(gaussian["claim_boundary"]["clay_conclusion"] == "OPEN", "Gaussian Clay row widened")
    need("PASS WITH THE ORIGINAL CLAIM BOUNDARY" in audit, "independent audit verdict missing")
    need(fourier["exactSelfChecks"]["twoPairCutoffSplit"] == "225/1024 = 27/512 + 171/1024", "two-pair split mismatch")
    decisions = fourier["candidateDecisions"]
    need(decisions["fixedHarmonicProbeQuadraticAbsorption"].startswith("REFUTED_EXACTLY"), "harmonic absorption status mismatch")
    need(decisions["compactCutoffQuadraticAbsorption_5_1_5_2"].startswith("OPEN_IN_THIS_HARNESS"), "compact-cutoff boundary widened")
    scope = fourier["scope"]
    need(scope["navierStokesSimulation"] is False, "Fourier harness mislabeled as simulation")
    need(scope["absoluteValuesIntervalCertified"] is False, "absolute diagnostic mislabeled interval-certified")
    need(scope["clayConclusion"] == "OPEN" and scope["notClay"] is True, "Fourier Clay row widened")
    need(scope["dgxUsed"] is False, "unexpected DGX claim")
    return {
        "gaussianOverall": gaussian["overall"],
        "gaussianPayloadSha256": gaussian["payload_sha256"],
        "gaussianIndependentAudit": "PASS_WITH_ORIGINAL_CLAIM_BOUNDARY",
        "fourierExactTwoPairSplit": fourier["exactSelfChecks"]["twoPairCutoffSplit"],
        "fourierFixedHarmonicAbsorption": "REFUTED_EXACTLY",
        "fourierCompactCutoff": "OPEN",
        "notClay": True,
    }


def build_manifest(repository: Path) -> dict[str, object]:
    contract = load_json(HERE / "contract.json")
    checklist = load_json(HERE / "audit-checklist.json")
    need(contract["claimBoundary"]["notClay"] is True, "contract NOT CLAY boundary missing")
    need(checklist["required"]["notClay"] is True, "checklist NOT CLAY boundary missing")
    source_commit = contract.get("sourceCommit")
    need(isinstance(source_commit, str), "contract source commit is missing")
    need(re.fullmatch(r"[0-9a-f]{40}", source_commit) is not None, "invalid source commit")
    resolved_commit = str(run_git(repository, "rev-parse", f"{source_commit}^{{commit}}")).strip()
    need(resolved_commit == source_commit, "contract source commit does not resolve exactly")
    bindings: list[dict[str, object]] = []
    for canonical_path, archive_name, expected_sha in EVIDENCE:
        source = repository / canonical_path
        need(sha256(source) == expected_sha, "canonical evidence digest mismatch: " + canonical_path)
        archived = HERE / archive_name
        need(archived.read_bytes() == source.read_bytes(), "archive copy mismatch: " + archive_name)
        blob = run_git(repository, "rev-parse", f"{source_commit}:{canonical_path}")
        blob_id = str(blob).strip()
        committed_bytes = run_git(repository, "show", f"{source_commit}:{canonical_path}", binary=True)
        need(committed_bytes == source.read_bytes(), "source differs from immutable Git blob: " + canonical_path)
        scoped = str(run_git(repository, "status", "--porcelain=v1", "--", canonical_path)).strip()
        need(not scoped, "canonical evidence path is dirty: " + canonical_path)
        bindings.append({
            "archive": archive_name,
            "bytes": archived.stat().st_size,
            "canonicalPath": canonical_path,
            "gitBlobObjectId": blob_id,
            "sha256": expected_sha,
        })
    claims = validate_claims(repository)
    records = [
        {"bytes": (HERE / name).stat().st_size, "path": name, "sha256": sha256(HERE / name)}
        for name in BOUND_FILES
    ]
    return {
        "schemaVersion": "r073x-formal-evidence-manifest-v1",
        "release": "R0.73X",
        "status": "SOURCE_COMMIT_BOUND_PACKAGE_HASH_SEALED",
        "sourceCommit": source_commit,
        "sourceCommitAssignedMeaning": "All seven canonical evidence inputs are byte-identical to immutable Git blobs at this commit.",
        "sourceBindings": bindings,
        "claims": claims,
        "inventory": {
            "archiveEvidenceFiles": len(ARCHIVE_FILES),
            "boundFileCount": len(BOUND_FILES),
            "packageFileCount": len(EXPECTED_FILES),
            "sha256SumsLineCount": len(BOUND_FILES) + 1,
        },
        "files": records,
        "scope": {
            "navierStokesSimulation": False,
            "compactCutoffAbsorption": "OPEN",
            "weightedTentCarleson": "OPEN",
            "epsilonRegularity": "OPEN",
            "globalRegularity": "OPEN",
            "clayConclusion": "OPEN",
            "notClay": True,
            "dgxUsed": False,
            "ordinaryTranslationPath": "LOCAL_DIRECT_NO_DGX",
        },
        "packageCommitBound": False,
        "packageCommitBoundary": "The publication owner must commit this directory before it can be called package-commit-bound.",
    }


def expected_sums(manifest_text: str) -> str:
    rows = [f"{sha256(HERE / name)}  {name}" for name in BOUND_FILES]
    rows.append(f"{sha256_bytes(manifest_text.encode('utf-8'))}  manifest.json")
    return "\n".join(rows) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--repository", type=Path, default=DEFAULT_REPOSITORY)
    args = parser.parse_args()
    repository = args.repository.resolve()
    need((repository / ".git").exists() or (repository / ".git").is_file(), "repository Git metadata missing")

    run_producer(
        repository,
        "scripts/r073x_gaussian_tail_certificate.py",
        ("R073X_GAUSSIAN_KERNEL=PASS", "R073X_PAYLOAD_SHA256=fcac97440dde87d00103f3a09b346bdd918c9fbb7360ee792edc2c8d0357e3b7", "R073X_CLAY=OPEN"),
    )
    verify_gaussian_regeneration(repository)
    run_producer(
        repository,
        "scripts/r073x_finite_fourier_harness.py",
        ("R073X_EXACT_CHECKS=PASS", "R073X_HARMONIC_ABSORPTION=REFUTED_EXACTLY", "R073X_COMPACT_CUTOFF_ABSORPTION=OPEN_IN_THIS_HARNESS", "R073X_CLAY=OPEN"),
    )

    if not args.check_only:
        for canonical_path, archive_name, expected_sha in EVIDENCE:
            source = repository / canonical_path
            need(sha256(source) == expected_sha, "source changed before archive copy: " + canonical_path)
            shutil.copyfile(source, HERE / archive_name)
    else:
        need(MANIFEST.is_file() and SUMS.is_file(), "sealed metadata missing")

    manifest = build_manifest(repository)
    manifest_text = canonical(manifest)
    sums_text = expected_sums(manifest_text)
    if args.check_only:
        need(MANIFEST.read_text(encoding="utf-8") == manifest_text, "manifest is stale")
        need(SUMS.read_text(encoding="utf-8") == sums_text, "SHA256SUMS is stale")
    else:
        MANIFEST.write_text(manifest_text, encoding="utf-8")
        SUMS.write_text(sums_text, encoding="utf-8")

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    need(actual_files == EXPECTED_FILES, f"package inventory mismatch: {sorted(actual_files ^ EXPECTED_FILES)}")
    print("R073X_FORMAL_EVIDENCE=PASS")
    print("R073X_SOURCE_COMMIT=" + str(manifest["sourceCommit"]))
    print("R073X_GAUSSIAN=PASS_WITH_ORIGINAL_CLAIM_BOUNDARY")
    print("R073X_HARMONIC_PROBE_ABSORPTION=REFUTED_EXACTLY")
    print("R073X_COMPACT_CUTOFF=OPEN")
    print("R073X_CLAY=OPEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
