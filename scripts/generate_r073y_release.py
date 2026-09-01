#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fail-closed, note-only R0.73Y GitHub Pages release transaction.

``--source-dry-run`` is read-only and remains useful while immutable package,
figure, content, and release pins are pending. ``--check-only`` constructs the
complete proposed transaction in memory. ``--apply`` installs exactly that map
with atomic replacement and rollback. Translation and the synchronized note
PDF are later transactions. No mode creates or edits a recap.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from typing import Iterable

from r073y_release_content import (
    CANONICAL_SOURCE_PATHS,
    CLOSED_LEDGER,
    EXACT_SCOPE_BOUNDARY_ZH,
    FIGURE_ARCHIVE_RELATIVE,
    FIGURE_ID,
    FIGURE_SOURCE_RELATIVE,
    FINITE_LEDGER,
    FROZEN_RESEARCH_SOURCE_PATHS,
    LATEST_RECAP_HTML,
    LATEST_RECAP_PDF,
    LATEST_RECAP_RELEASE,
    OPEN_LEDGER,
    PLANNED_AUDIT_PATHS,
    R073X_BASELINE,
    R073Y_TARGET,
    RELEASE,
    RELEASE_ID,
    SITE_VERSION,
    CanonicalSourceError,
    ReleaseContent,
    load_release_content,
    source_status,
)


ROOT = Path(os.environ.get("R073Y_RELEASE_ROOT", Path(__file__).resolve().parents[1])).resolve()
PUBLIC = ROOT / "public"

BASELINE_COMMIT = "cb0ab52b27891478e159d69cae1ce4ed8b96b522"
RESEARCH_SOURCE_COMMIT = "1ecc6fe20a921db9d0876dbd4484a3aa4ca7ec66"
CERTIFICATE_PACKAGE_COMMIT = "1811bb8e93c17b570ab58b10842f22695f0e2b3c"
FIGURE_SOURCE_COMMIT = "e37bf12cb5c2a8eb975e5097229dbc48fa597b35"
FIGURE_PACKAGE_COMMIT = "05fdbc717a02be9f88fafc2b67a658e706b40be4"
FINAL_CONTENT_COMMIT = "7f4215772a0c97a3d9f71ab5aa8363869e442adb"
RELEASE_SOURCE_COMMIT = "ec9ac1eb479bb2f688780ae5ae0c0294940c4645"
NORMALIZED_RELEASE_SOURCE_COMMIT = "__NORMALIZED_RELEASE_SOURCE_COMMIT__"
PENDING_PIN_RE = re.compile(r"^PENDING_[A-Z0-9_]+_40_HEX$")

BINDING_ORDER = (
    ("R0.73X published baseline", BASELINE_COMMIT),
    ("R0.73Y frozen research source", RESEARCH_SOURCE_COMMIT),
    ("R0.73Y certificate package", CERTIFICATE_PACKAGE_COMMIT),
    ("R0.73Y figure source/raw package", FIGURE_SOURCE_COMMIT),
    ("R0.73Y formal figure package", FIGURE_PACKAGE_COMMIT),
    ("R0.73Y final reader content", FINAL_CONTENT_COMMIT),
    ("R0.73Y release source", RELEASE_SOURCE_COMMIT),
)

CERTIFICATE_ROOT = "research/certificates/r073y"
READER_CORRECTION_PATH = "research/r073y_reader_quantifier_correction.md"
FIGURE_SOURCE_NAMES = (
    "README.md", "caption.md", "chart-contract-and-source-data.md", "command.txt",
    "config.json", "contract.json", "plot.py", "qa-protocol.md", "requirements.txt",
    "validate.py",
)
FIGURE_RAW_RESULT_NAMES = (
    "environment.json", "figure.pdf", "figure.png", "figure.svg",
    "progress.ndjson", "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png",
    "resource-log.ndjson", "results.json", "source-data.csv",
)
FIGURE_METADATA_NAMES = ("SHA256SUMS", "manifest.json", "qa-report.md", "validation.json")
FIGURE_SOURCE_PATHS = tuple(f"{FIGURE_SOURCE_RELATIVE}/{name}" for name in FIGURE_SOURCE_NAMES)
FIGURE_RAW_RESULT_PATHS = tuple(f"{FIGURE_SOURCE_RELATIVE}/{name}" for name in FIGURE_RAW_RESULT_NAMES)
FIGURE_PACKAGE_PATHS = tuple(sorted(
    FIGURE_SOURCE_PATHS + FIGURE_RAW_RESULT_PATHS
    + tuple(f"{FIGURE_SOURCE_RELATIVE}/{name}" for name in FIGURE_METADATA_NAMES)
))

TRANSLATION_SCRIPT_PATH = "scripts/add-r073y-translations.mjs"
PDF_BINDER_SCRIPT_PATH = "scripts/bind-r073y-pdfs.mjs"
RELEASE_TEST_PATH = "tests/r073y-release.test.mjs"
INTERFACE_TEST_PATH = "tests/r073y-exact-shear-gate.test.mjs"
RELEASE_SOURCE_PATHS = (
    ".github/workflows/pages.yml",
    ".github/workflows/release-publication-gate.yml",
    "scripts/r073y_release_content.py",
    "scripts/generate_r073y_release.py",
    "scripts/generate_note_index.py",
    TRANSLATION_SCRIPT_PATH,
    PDF_BINDER_SCRIPT_PATH,
    "scripts/render-note-pdf.mjs",
    "scripts/run-release-publication-gate.mjs",
    "tests/release-publication-gate-runner.test.mjs",
    "tests/release-publication-invariant.test.mjs",
    INTERFACE_TEST_PATH,
    RELEASE_TEST_PATH,
    "tests/site-route-current-boundary.test.mjs",
)
FINAL_CONTENT_PATHS = tuple(CANONICAL_SOURCE_PATHS) + tuple(PLANNED_AUDIT_PATHS) + (
    "scripts/r073y_release_content.py",
)
BASELINE_PATHS = (
    "VERSION",
    "research/release-manifest.json",
    "research/formal-archive-inventory.json",
    "public/site-version.json",
    "public/notes/r0-73x.html",
    LATEST_RECAP_HTML,
    LATEST_RECAP_PDF,
    "public/research-review.html",
    "public/literature-review.html",
    "public/notes/index.html",
)

CORE_OUTPUTS = (
    "public/notes/r0-73y.html",
    "public/research-review.html",
    "public/literature-review.html",
    "public/notes/index.html",
    "public/research/r073y/r073y_figure_source_audit.md",
    "public/research/r073y/r073y_figure_source_reaudit.md",
    "public/site-version.json",
    "research/release-manifest.json",
    "research/formal-archive-inventory.json",
    "VERSION",
)
FIGURE_RESEARCH_ARCHIVE_OUTPUTS = tuple(
    f"research/{FIGURE_ARCHIVE_RELATIVE}/{name}"
    for name in sorted(FIGURE_SOURCE_NAMES + FIGURE_RAW_RESULT_NAMES + FIGURE_METADATA_NAMES)
)
FIGURE_PUBLIC_ARCHIVE_OUTPUTS = tuple(
    f"public/{FIGURE_ARCHIVE_RELATIVE}/{name}"
    for name in sorted(FIGURE_SOURCE_NAMES + FIGURE_RAW_RESULT_NAMES + FIGURE_METADATA_NAMES)
)
FIGURE_PUBLIC_ASSET_OUTPUTS = tuple(
    f"public/assets/r073y/{FIGURE_ID}.{suffix}" for suffix in ("pdf", "svg", "png")
)
LATER_STAGE_OUTPUTS = (
    "public/notes/r0-73y.pdf",
    "research/r073y_note_pdf_render.json",
    "research/r073y_pdf_bindings.json",
    "translations/en.json",
    "public/i18n-en.js",
    "scripts/i18n-snapshots/r073y-missing.json",
)
PROTECTED_RECAP_HASHES = {
    "public/notes/r0-73x.html": "5e98103df24a01b690fca104938c65dec96ad00f7d40e2c9798e7dc859d6afcb",
    "public/notes/r0-73x.pdf": "0c1c97a754fe2c15310dff184c2d3ed142c40c53e400f5ba4895757808e267c7",
    LATEST_RECAP_HTML: "44e38b7a6855edfd92842d2c5eb75792e03f5fb1ca6de6902a1402dcbe0a3776",
    LATEST_RECAP_PDF: "e95324099393b5be917cb32b29d4986c4c8699fa3ba21904d7a7b5304e6501fa",
    "research/r073x_pdf_bindings.json": "e255810c20c13c8c90020847685048a1dde88bf513b33e7440bb7ccec5507f87",
    "research/r073x_recap_pdf_render.json": "a19ca701c402504e4e0b93d2ca442fdd665aa93219caa726d64f3f5ff3c00101",
}
PROTECTED_RECAP_ASSET_COUNT = 154
PROTECTED_RECAP_LEDGER_SHA256 = "f76860a8a3d8f1b3cd83b98e566bc3ffd09461175c234dfffe35864f05b5d643"
PUBLICATION_STAGE_ORDER = (
    "freeze-r073x-published-baseline",
    "freeze-r073y-research-source",
    "seal-r073y-certificate-package",
    "seal-r073y-formal-figure-source-and-package",
    "freeze-reviewed-reader-content",
    "freeze-release-source-and-fill-normalized-self-pin",
    "validate-in-memory-note-only-transaction",
    "capture-review-and-apply-local-translations",
    "render-and-bind-synchronized-note-pdf",
    "run-publication-gate-then-deploy-from-main",
)


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def strict_json_bytes(payload: bytes, label: str) -> dict:
    def reject(value: str) -> None:
        raise ValueError("non-finite JSON constant: " + value)

    def unique(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON key: " + key)
            result[key] = value
        return result

    try:
        value = json.loads(payload.decode("utf-8"), parse_constant=reject, object_pairs_hook=unique)
    except (UnicodeDecodeError, ValueError) as exc:
        raise RuntimeError(label + ": invalid strict JSON") from exc
    if not isinstance(value, dict):
        raise RuntimeError(label + ": expected a JSON object")
    return value


def is_conflict_copy(relative: str | Path) -> bool:
    return any(re.search(r" \d+(?=\.[^.]+$|$)", part) is not None for part in Path(relative).parts)


def current_bytes(relative: str) -> bytes:
    path = ROOT / relative
    if not path.is_file() or path.is_symlink() or is_conflict_copy(relative):
        raise RuntimeError(relative + ": expected canonical regular nonsymlink file")
    return path.read_bytes()


def run_git(arguments: list[str], *, binary: bool = False) -> str | bytes:
    result = subprocess.run(["git", *arguments], cwd=ROOT, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise RuntimeError(
            "git command failed: git " + " ".join(arguments) + ": "
            + result.stderr.decode("utf-8", "replace").strip()
        )
    return result.stdout if binary else result.stdout.decode("utf-8").strip()


def git_bytes(commit: str, relative: str) -> bytes:
    value = run_git(["cat-file", "blob", f"{commit}:{relative}"], binary=True)
    assert isinstance(value, bytes)
    return value


def git_paths(commit: str, root: str) -> tuple[str, ...]:
    value = run_git(["ls-tree", "-r", "--name-only", commit, "--", root])
    assert isinstance(value, str)
    return tuple(sorted(row for row in value.splitlines() if row))


def canonical_tree_files(relative_root: str) -> tuple[str, ...]:
    root = ROOT / relative_root
    if not root.is_dir() or root.is_symlink():
        raise RuntimeError("missing regular directory: " + relative_root)
    values: list[str] = []
    for path in root.rglob("*"):
        if path.is_symlink():
            raise RuntimeError(
                "canonical package tree contains a symlink: "
                + path.relative_to(ROOT).as_posix()
            )
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT).as_posix()
        if is_conflict_copy(relative):
            raise RuntimeError("OneDrive conflict copy entered canonical tree: " + relative)
        values.append(relative)
    return tuple(sorted(values))


def commit_ready(value: str) -> bool:
    return re.fullmatch(r"[0-9a-f]{40}", value) is not None


def pin_blockers() -> list[str]:
    return [label + "=" + commit for label, commit in BINDING_ORDER if not commit_ready(commit)]


def normalized_release_generator(payload: bytes) -> bytes:
    try:
        value = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError("R0.73Y release generator is not UTF-8") from exc
    pattern = r'(?m)^RELEASE_SOURCE_COMMIT = "(?:[0-9a-f]{40}|PENDING_RELEASE_SOURCE_COMMIT_40_HEX)"$'
    replacement = f'RELEASE_SOURCE_COMMIT = "{NORMALIZED_RELEASE_SOURCE_COMMIT}"'
    normalized, count = re.subn(pattern, replacement, value)
    if count != 1:
        raise RuntimeError("R0.73Y normalized release-source slot drifted")
    return normalized.encode("utf-8")


def verify_ancestry_and_pins() -> None:
    blockers = pin_blockers()
    if blockers:
        raise RuntimeError("immutable release pins remain pending: " + repr(blockers))
    for label, commit in BINDING_ORDER:
        run_git(["cat-file", "-e", commit + "^{commit}"])
    for index in range(len(BINDING_ORDER) - 1):
        older = BINDING_ORDER[index][1]
        newer = BINDING_ORDER[index + 1][1]
        result = subprocess.run(["git", "merge-base", "--is-ancestor", older, newer], cwd=ROOT, check=False)
        if result.returncode:
            raise RuntimeError("R0.73Y binding commits are not in ancestry order")


def verify_paths(commit: str, paths: Iterable[str], label: str) -> None:
    for relative in paths:
        committed = git_bytes(commit, relative)
        present = current_bytes(relative)
        if relative == "scripts/generate_r073y_release.py":
            committed = normalized_release_generator(committed)
            present = normalized_release_generator(present)
        if committed != present:
            raise RuntimeError(label + ": committed/current bytes differ: " + relative)


def verify_tree(commit: str, relative_root: str, label: str) -> None:
    committed = tuple(path for path in git_paths(commit, relative_root) if not is_conflict_copy(path))
    present = canonical_tree_files(relative_root)
    if not committed or committed != present:
        raise RuntimeError(label + ": committed/current tree inventory differs")
    verify_paths(commit, committed, label)


def snapshot_tree() -> dict[str, tuple[int, int, str]]:
    values: dict[str, tuple[int, int, str]] = {}
    for root_name in ("research", "scripts"):
        base = ROOT / root_name
        for path in base.rglob("*"):
            if path.is_file() and not path.is_symlink():
                relative = path.relative_to(ROOT).as_posix()
                status = path.stat()
                values[relative] = (status.st_size, status.st_mtime_ns, sha256(path.read_bytes()))
    return values


def run_read_only_check(relative: str, arguments: list[str], label: str) -> None:
    before = snapshot_tree()
    result = subprocess.run(
        [sys.executable, "-B", str(ROOT / relative), *arguments], cwd=ROOT,
        check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    after = snapshot_tree()
    if before != after:
        changed = sorted(set(before) ^ set(after) | {key for key in set(before) & set(after) if before[key] != after[key]})
        raise RuntimeError(label + " wrote or changed files: " + repr(changed[:20]))
    if result.returncode:
        raise RuntimeError(label + " failed: " + (result.stderr or result.stdout)[-3000:])


def parse_sums(payload: bytes, label: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in payload.decode("utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/]+)", line)
        if match is None or match.group(2) in result:
            raise RuntimeError(label + ": malformed SHA256SUMS")
        result[match.group(2)] = match.group(1)
    return result


def certificate_paths() -> tuple[str, ...]:
    return canonical_tree_files(CERTIFICATE_ROOT)


def certificate_summary() -> dict[str, object]:
    path = ROOT / CERTIFICATE_ROOT / "manifest.json"
    if not path.is_file() or path.is_symlink():
        return {"finalSeal": False, "pending": "certificate-manifest-missing", "inventoryDerived": True}
    try:
        manifest = strict_json_bytes(path.read_bytes(), "R0.73Y certificate manifest")
    except RuntimeError as exc:
        return {"finalSeal": False, "pending": str(exc), "inventoryDerived": True}
    return {
        "finalSeal": manifest.get("status") == "SEALED"
        and manifest.get("source", {}).get("git_commit_sha1") == RESEARCH_SOURCE_COMMIT,
        "status": manifest.get("status"),
        "sourceCommit": manifest.get("source", {}).get("git_commit_sha1"),
        "inventory": manifest.get("inventory"),
        "inventoryDerived": True,
    }


def validate_certificate() -> dict:
    base = ROOT / CERTIFICATE_ROOT
    manifest = strict_json_bytes(current_bytes(f"{CERTIFICATE_ROOT}/manifest.json"), "R0.73Y certificate manifest")
    paths = certificate_paths()
    names = {Path(path).name for path in paths}
    inventory = manifest.get("inventory")
    rows = manifest.get("files")
    contract = strict_json_bytes(current_bytes(f"{CERTIFICATE_ROOT}/contract.json"), "R0.73Y certificate contract")
    checklist = strict_json_bytes(current_bytes(f"{CERTIFICATE_ROOT}/audit-checklist.json"), "R0.73Y certificate audit")
    bindings = contract.get("source", {}).get("inputs")
    if (
        manifest.get("schema") != "r073y-formal-certificate-manifest-v1"
        or manifest.get("release") != RELEASE
        or manifest.get("status") != "SEALED"
        or manifest.get("source", {}).get("git_commit_sha1") != RESEARCH_SOURCE_COMMIT
        or not isinstance(inventory, dict)
        or inventory.get("package_file_count") != len(paths)
        or not isinstance(rows, list)
        or inventory.get("manifest_entry_count") != len(rows)
        or not isinstance(bindings, list)
        or len(bindings) != len(FROZEN_RESEARCH_SOURCE_PATHS)
        or inventory.get("sha256sums_entry_count") != len(paths) - 1
        or manifest.get("claim_boundary", {}).get("not_clay") is not True
        or manifest.get("claim_boundary", {}).get("clay_problem_solved") is not False
        or manifest.get("claim_boundary", {}).get("production_only_coercive_bridge")
        != "FALSE_BY_EXACT_NSE_FAMILY"
        or contract.get("schema") != "r073y-formal-certificate-contract-v1"
        or contract.get("source", {}).get("git_commit_sha1") != RESEARCH_SOURCE_COMMIT
        or checklist.get("schema") != "r073y-formal-certificate-audit-v1"
        or checklist.get("status") != "PASS"
        or checklist.get("not_clay") is not True
    ):
        raise RuntimeError("R0.73Y certificate manifest/inventory contract drifted")
    if len(names) != len(paths) or not {"manifest.json", "SHA256SUMS"}.issubset(names):
        raise RuntimeError("R0.73Y certificate inventory contains duplicate/nested names")
    bound = {row.get("path"): row for row in rows if isinstance(row, dict) and isinstance(row.get("path"), str)}
    if len(bound) != len(rows) or set(bound) != names - {"manifest.json", "SHA256SUMS"}:
        raise RuntimeError("R0.73Y certificate bound-file inventory drifted")
    for name, row in bound.items():
        payload = current_bytes(f"{CERTIFICATE_ROOT}/{name}")
        if row.get("bytes") != len(payload) or row.get("sha256") != sha256(payload):
            raise RuntimeError("R0.73Y certificate byte binding drifted: " + name)
    seen_canonical: set[str] = set()
    seen_archive: set[str] = set()
    for row in bindings:
        if not isinstance(row, dict):
            raise RuntimeError("R0.73Y certificate source binding is not an object")
        canonical = row.get("path")
        archive_binding = row.get("archive_binding")
        archive = None
        if isinstance(archive_binding, str) and ":" in archive_binding:
            archive = archive_binding.split(":", 1)[1]
        if (
            not isinstance(canonical, str) or canonical not in FROZEN_RESEARCH_SOURCE_PATHS
            or not isinstance(archive_binding, str)
            or canonical in seen_canonical
            or (archive is not None and (archive not in names or archive in seen_archive))
        ):
            raise RuntimeError("R0.73Y certificate source binding path drifted")
        seen_canonical.add(canonical)
        if archive is not None:
            seen_archive.add(archive)
        payload = current_bytes(canonical)
        if payload != git_bytes(RESEARCH_SOURCE_COMMIT, canonical) or row.get("sha256") != sha256(payload):
            raise RuntimeError("R0.73Y certificate immutable source binding drifted: " + canonical)
        if archive is not None:
            archive_payload = current_bytes(f"{CERTIFICATE_ROOT}/{archive}")
            if archive_binding.startswith("reversible-relocation:"):
                archive_declared = contract.get("archive", {}).get("flat_producer", {}).get("sha256")
                if archive_declared != sha256(archive_payload):
                    raise RuntimeError("R0.73Y relocated producer archive hash drifted")
            elif archive_payload != payload:
                raise RuntimeError("R0.73Y byte-identical archive binding drifted: " + canonical)
    sums = parse_sums(current_bytes(f"{CERTIFICATE_ROOT}/SHA256SUMS"), "R0.73Y certificate")
    if set(sums) != names - {"SHA256SUMS"}:
        raise RuntimeError("R0.73Y certificate SHA256SUMS inventory drifted")
    for name, digest in sums.items():
        if sha256(current_bytes(f"{CERTIFICATE_ROOT}/{name}")) != digest:
            raise RuntimeError("R0.73Y certificate SHA256SUMS mismatch: " + name)
    run_read_only_check("scripts/r073y_exact_shear_certificate.py", ["--check-only"], "R0.73Y exact-shear certificate")
    return manifest


def figure_summary() -> dict[str, object]:
    base = ROOT / FIGURE_SOURCE_RELATIVE
    files = [] if not base.is_dir() else sorted(path.name for path in base.iterdir() if path.is_file() and not path.is_symlink())
    manifest_path = base / "manifest.json"
    return {
        "figureId": FIGURE_ID,
        "filesPresent": files,
        "expectedFileCount": 25,
        "formal": len(files) == 25 and manifest_path.is_file(),
        "scopeLabel": "ANALYTIC_EXACT_WITNESS_NOT_DNS",
    }


def validate_figure(certificate: dict) -> dict:
    base = FIGURE_SOURCE_RELATIVE
    paths = canonical_tree_files(base)
    if paths != FIGURE_PACKAGE_PATHS or len(paths) != 25:
        raise RuntimeError("R0.73Y formal figure must have the exact 25-file inventory")
    manifest = strict_json_bytes(current_bytes(f"{base}/manifest.json"), "R0.73Y figure manifest")
    contract = strict_json_bytes(current_bytes(f"{base}/contract.json"), "R0.73Y figure contract")
    validation = strict_json_bytes(current_bytes(f"{base}/validation.json"), "R0.73Y figure validation")
    seal = manifest.get("seal", {})
    bindings = seal.get("figureSourceBindings")
    if (
        manifest.get("schemaVersion") != "research-figure-manifest-v1"
        or manifest.get("figureSchemaVersion") != "r073y-exact-shear-obstruction-manifest-v1"
        or manifest.get("figureId") != FIGURE_ID or manifest.get("release") != RELEASE
        or manifest.get("status") != "formal" or manifest.get("publicationStatus") != "staged"
        or contract.get("figureId") != FIGURE_ID
        or contract.get("sourceAuthority", {}).get("commit") != RESEARCH_SOURCE_COMMIT
        or contract.get("claimBoundary", {}).get("analyticExactWitness") is not True
        or contract.get("claimBoundary", {}).get("navierStokesSimulation") is not False
        or contract.get("claimBoundary", {}).get("dns") is not False
        or contract.get("claimBoundary", {}).get("notClay") is not True
        or contract.get("claimBoundary", {}).get("strictGradientCovarianceRequiresNonzeroAmplitude") is not True
        or contract.get("claimBoundary", {}).get("zeroAmplitudeMemberCovariance") != "zero"
        or validation.get("schemaVersion") != "r073y-exact-shear-validation-v3"
        or validation.get("status") != "PASS"
        or validation.get("sealState") != "formal-figure-source-seal"
        or seal.get("figureSourceCommitAssigned") is not True
        or seal.get("figureSourceCommit") != FIGURE_SOURCE_COMMIT
        or seal.get("figureSourceCommitBound") is not True
        or seal.get("requiresFigureSourceCommitFinalReseal") is not False
        or not isinstance(bindings, list) or len(bindings) != 21
        or manifest.get("qa", {}).get("status") != "passed"
        or manifest.get("git", {}).get("sourceEvidenceCommit") != RESEARCH_SOURCE_COMMIT
        or manifest.get("git", {}).get("figureSourceCommit") != FIGURE_SOURCE_COMMIT
        or manifest.get("claimBoundary", {}).get("analyticExactWitness") is not True
        or manifest.get("claimBoundary", {}).get("dns") is not False
        or manifest.get("claimBoundary", {}).get("strictGradientCovarianceRequiresNonzeroAmplitude") is not True
        or manifest.get("claimBoundary", {}).get("zeroAmplitudeMemberCovariance") != "zero"
        or certificate.get("source", {}).get("git_commit_sha1") != RESEARCH_SOURCE_COMMIT
    ):
        raise RuntimeError("R0.73Y formal figure seal/scope contract drifted")
    expected_bound = set(FIGURE_SOURCE_NAMES + FIGURE_RAW_RESULT_NAMES)
    by_path = {row.get("path"): row for row in bindings if isinstance(row, dict)}
    if set(by_path) != expected_bound:
        raise RuntimeError("R0.73Y figure source/raw binding inventory drifted")
    for name, row in by_path.items():
        relative = f"{base}/{name}"
        payload = current_bytes(relative)
        if row.get("sha256") != sha256(payload) or row.get("bytes") != len(payload):
            raise RuntimeError("R0.73Y figure source/raw byte binding drifted: " + relative)
    sums = parse_sums(current_bytes(f"{base}/SHA256SUMS"), "R0.73Y figure")
    if set(sums) != {Path(path).name for path in paths} - {"SHA256SUMS"}:
        raise RuntimeError("R0.73Y figure SHA256SUMS inventory drifted")
    for name, digest in sums.items():
        if sha256(current_bytes(f"{base}/{name}")) != digest:
            raise RuntimeError("R0.73Y figure SHA256SUMS mismatch: " + name)
    return manifest


def decode_baseline(relative: str) -> str:
    return git_bytes(BASELINE_COMMIT, relative).decode("utf-8")


def replace_once(value: str, old: str, new: str, label: str) -> str:
    count = value.count(old)
    if count != 1:
        raise RuntimeError(label + f": expected one replacement site, found {count}")
    return value.replace(old, new, 1)


def assert_public_html(value: str, label: str, *, require_boundary: bool = True) -> None:
    if re.search(r"<!doctype html>", value, re.IGNORECASE) is None:
        raise RuntimeError(label + ": missing HTML doctype")
    for token in ('lang="zh-CN"', "/i18n-en.js?v=1.65"):
        if token not in value:
            raise RuntimeError(label + ": missing " + token)
    if require_boundary and "NOT CLAY" not in value:
        raise RuntimeError(label + ": missing NOT CLAY boundary")
    if any(phrase in value for phrase in ("我们", "攻关", "主攻", "解决了千禧年")):
        raise RuntimeError(label + ": reader voice drifted")


def note_page(content: ReleaseContent) -> str:
    baseline = decode_baseline("public/notes/r0-73x.html")
    head_match = re.search(r"(?s)\A(.*?</head>)", baseline)
    if head_match is None:
        raise RuntimeError("R0.73X note template lacks head")
    head = head_match.group(1)
    head = re.sub(r"<title>.*?</title>", f"<title>{html.escape(content.document_title_en)}</title>", head, count=1, flags=re.DOTALL)
    head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Exact shear gives zero production for every real amplitude at every positive heat scale; gradient covariance is strictly positive only for nonzero amplitude and is zero at A=0. This is a literature-calibrated production-only no-go, not a regularity theorem.">', head, count=1)
    head = head.replace('data-site-version="1.64"', 'data-site-version="1.65"').replace('/i18n-en.js?v=1.64', '/i18n-en.js?v=1.65')
    if 'data-site-version="1.65"' not in head:
        head = head.replace('<html lang="zh-CN">', '<html lang="zh-CN" data-site-version="1.65">')
    value = (
        head + "\n<body><nav class=\"top\"><a href=\"/research-review.html\">研究首页</a>"
        "<span>R0.73Y · NOT CLAY</span></nav><main>\n"
        + content.note_hero + "\n" + content.note_article
        + "\n</main></body></html>\n"
    )
    assert_public_html(value, "R0.73Y note")
    return value


def home_page(content: ReleaseContent) -> str:
    value = decode_baseline("public/research-review.html")
    value = value.replace("v=1.64", "v=1.65").replace('data-site-version="1.64"', 'data-site-version="1.65"')
    value = value.replace("v1.64", "v1.65")
    value = replace_once(value, "<strong>200</strong>公开研究笔记", "<strong>201</strong>公开研究笔记", "home note count")
    value = replace_once(value, "<strong>R0.73X</strong>最新研究节点", "<strong>R0.73Y</strong>最新研究节点", "home latest")
    value = replace_once(
        value,
        '<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title">'
        + value.split('<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title">', 1)[1].split("</section>", 1)[0]
        + "</section>",
        '<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title">'
        '<div class="route-overview-inner"><header class="route-map-header"><div>'
        f'<p class="eyebrow">LATEST RELEASE · R0.73Y · {html.escape(content.date)}</p>'
        f'<h2 class="route-map-title" id="latest-release-title">{html.escape(content.public_title_zh)}</h2>'
        '<p class="route-map-intro">exact shear NSE 给出一条解析障碍：'
        '对每个实振幅，zero production at every positive scale；仅当 A != 0 时，'
        'strictly positive heat covariance 才成立，A = 0 时它为零。'
        '这只否定 production-only coercivity；Vreman（2004）已直接覆盖 basic shear 碰撞，'
        '因此我不申报该机制的新颖性或优先权。analytic exact witness / not DNS；NOT CLAY。</p>'
        '</div><nav class="route-map-actions" aria-label="最新发布快捷入口">'
        '<a class="route-map-latest" href="/notes/r0-73y.pdf">阅读最新 R0.73Y 研究笔记 →</a>'
        '<a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（R0.61–R0.73X，140 节）</a>'
        '<a href="/notes/">201 篇研究笔记总索引</a>'
        '<a href="#r073y">查看首页完整 R0.73Y 卡片</a>'
        '</nav></header><div class="route-legend" aria-label="最新发布计数">'
        '<span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.73Y · 103 节已公开</span>'
        '<span><i class="route-legend-mark kept" aria-hidden="true"></i>79 节完整封存</span>'
        '<span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.73Y</span>'
        '</div></div></section>',
        "home latest spotlight",
    )
    value = replace_once(value, "Research topology · R0.1–R0.73X", "Research topology · R0.1–R0.73Y", "home topology range")
    value = replace_once(value, 'href="#r073x">跳到首页 R0.73X 卡片 →', 'href="#r073y">跳到首页 R0.73Y 卡片 →', "home topology latest action")
    value = replace_once(value, "R0.70A–R0.73X：102 节已公开，78 节完整封存", "R0.70A–R0.73Y：103 节已公开，79 节完整封存", "home topology action count")
    value = replace_once(value, '<span class="route-range">R0.69P–R0.73X</span>', '<span class="route-range">R0.69P–R0.73Y</span>', "home current range")
    value = replace_once(value, 'aria-label="R0.69P–R0.73X"', 'aria-label="R0.69P–R0.73Y"', "home current note label")
    value = replace_once(value, "<summary>展开 110 篇公开笔记</summary>", "<summary>展开 111 篇公开笔记</summary>", "home current note count")
    value = replace_once(
        value,
        "<h3>R0.73X：Gaussian 速度尾、代数 pressure 尾、positive-scale size 与 open coercivity bridge 已分列</h3>",
        "<h3>R0.73Y：exact shear kernel、全振幅零 production、A != 0 时严格正 heat covariance 与 production-only no-go 已分列</h3>",
        "home current title",
    )
    value = replace_once(value, "<span>R0.72R–R0.73X：</span>", "<span>R0.72R–R0.73Y：</span>", "home current path range")
    value = replace_once(
        value,
        "→ tensor heat hierarchy → explicit exterior tails and the open coercivity bridge</p>",
        "→ tensor heat hierarchy → explicit exterior tails and the open coercivity bridge → exact shear all-scale production obstruction</p>",
        "home current path endpoint",
    )
    value = replace_once(
        value,
        '                  <a class="milestone" href="/notes/r0-73x.html">R0.73X</a>',
        '                  <a class="milestone" href="/notes/r0-73x.html">R0.73X</a>\n'
        '                  <a class="milestone" href="/notes/r0-73y.html">R0.73Y</a>',
        "home route note insertion",
    )
    next_node = re.compile(
        r'<div class="tree-row">\s*<article class="tree-node next">\s*'
        r'<div class="tree-node-head"><span class="route-range">NEXT · R0\.73Y</span>.*?</article>\s*</div>',
        re.DOTALL,
    )
    replacement = (
        '<div class="tree-row">\n            <article class="tree-node next">\n'
        '              <div class="tree-node-head"><span class="route-range">NEXT · R0.73Z</span>'
        '<span class="tree-state current">下一检查点</span></div>\n'
        f'              <h3>R0.73Z 下一接口</h3><p>{html.escape(content.next_gate_zh)}</p>\n'
        '            </article>\n          </div>'
    )
    value, count = next_node.subn(replacement, value, count=1)
    if count != 1:
        raise RuntimeError("home next-interface replacement drifted")
    marker = '<div class="task-one" id="r073x" data-release="r073x"'
    position = value.find(marker)
    if position < 0:
        raise RuntimeError("home lacks canonical R0.73X card insertion marker")
    value = value[:position] + content.home_card + "\n          " + value[position:]
    # The recap remains a previous milestone and its card/link must remain X.
    value = replace_once(value, "全站现有 200 篇公开研究笔记", "全站现有 201 篇公开研究笔记", "home recap card current-site count")
    if "/recap-r0-61-r0-73y" in value:
        raise RuntimeError("home must not invent an R0.73Y recap")
    if value.count('data-release="r073y"') != 1:
        raise RuntimeError("home must contain exactly one R0.73Y card")
    assert_public_html(value, "R0.73Y home")
    return value


def literature_page(content: ReleaseContent) -> str:
    value = decode_baseline("public/literature-review.html")
    value = value.replace("v=1.64", "v=1.65").replace('data-site-version="1.64"', 'data-site-version="1.65"')
    value = value.replace("v1.64", "v1.65")
    if 'data-site-version="1.65"' not in value:
        value = replace_once(value, '<html lang="zh-CN">', '<html lang="zh-CN" data-site-version="1.65">', "literature site version")
    value = replace_once(value, "本站 R0.69P–R0.73X 只列为研究笔记", "本站 R0.69P–R0.73Y 只列为研究笔记", "literature evidence range")
    deck_end = '<span class="route-r073v-deck-update">'
    if deck_end not in value:
        raise RuntimeError("literature route deck insertion marker drifted")
    deck_close = value.index("</span></p>", value.index(deck_end))
    value = value[:deck_close + len("</span>")] + content.literature_update + value[deck_close + len("</span>"):]
    old_pause = re.compile(
        r'<div class="route-step pause"><header><b>开放接口 · R0\.73Y</b>'
        r'<strong>signed-to-absolute coercivity bridge</strong></header><p>.*?</p></div>',
        re.DOTALL,
    )
    new_route = (
        '<div class="route-step kept"><header><b>R0.73Y</b>'
        '<strong>exact shear kernel and production-only no-go</strong></header>'
        f'<p><strong>{html.escape(content.public_title_zh)}</strong></p>'
        '<p>R0.70A–R0.73Y：103 节已公开，79 节完整封存。</p>'
        '<p>Exact shear 对每个实振幅在每个正 heat scale 上的 production 都为零；'
        '梯度 heat covariance 仅在 A != 0 时严格为正，A = 0 时为零。'
        '这给出 production-only functional 的解析 no-go，不给出 regularity theorem。 '
        '<a href="/notes/r0-73y.html">研究笔记</a> '
        '<a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap</a> '
        '<a href="#r073y-boundary">文献边界</a></p></div>'
        '<div class="route-step pause"><header><b>开放接口 · R0.73Z</b>'
        '<strong>scale-critical covariance and quotient coercivity</strong></header>'
        f'<p>{html.escape(content.next_gate_zh)} 任意初值全局正则性与 Clay 保持 OPEN。</p></div>'
    )
    value, count = old_pause.subn(new_route, value, count=1)
    if count != 1:
        raise RuntimeError("literature route endpoint replacement drifted")
    boundary_marker = '<h3 id="r073x-boundary">'
    boundary_start = value.index(boundary_marker)
    boundary_close = value.index('</div>', boundary_start) + len('</div>')
    update = (
        '\n<h3 id="r073y-boundary">R0.73Y：exact shear kernel 与 production-only no-go</h3>'
        '<p>' + content.literature_update + '</p>'
        '<div class="boundary"><strong>R0.73Y 的主张边界</strong>'
        '<p>' + html.escape(CLOSED_LEDGER) + '</p><p>' + html.escape(FINITE_LEDGER) + '</p>'
        '<p>FINITE：strictPositivityFromSampling=FALSE；basicShearNoveltyOrPriority=NOT_CLAIMED</p>'
        '<p>' + html.escape(OPEN_LEDGER) + '。' + html.escape(EXACT_SCOPE_BOUNDARY_ZH) + ' NOT CLAY。</p></div>'
    )
    value = value[:boundary_close] + update + value[boundary_close:]
    if value.count('id="r073y-boundary"') != 1:
        raise RuntimeError("literature page lacks one R0.73Y boundary")
    assert_public_html(value, "R0.73Y literature")
    return value


def note_index(content: ReleaseContent) -> str:
    value = decode_baseline("public/notes/index.html")
    value = value.replace("v=1.64", "v=1.65").replace('data-site-version="1.64"', 'data-site-version="1.65"')
    value = value.replace("v1.64", "v1.65")
    value = value.replace("200 篇公开研究笔记", "201 篇公开研究笔记")
    value = value.replace("最新节点 R0.73X", "最新节点 R0.73Y")
    value = replace_once(
        value,
        '<a href="/recap-r0-61-r0-73x.html">累计回顾</a>',
        '<a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap</a>',
        "index recap milestone label",
    )
    value = replace_once(value, "<strong>200</strong>", "<strong>201</strong>", "index HTML count")
    value = replace_once(value, "<strong>R0.73X</strong>", "<strong>R0.73Y</strong>", "index latest")
    value = value.replace("157 个同步 PDF", "158 个同步 PDF").replace("<strong>157</strong>", "<strong>158</strong>")
    value = replace_once(value, "<span><span>24</span> <span>篇</span></span>", "<span><span>25</span> <span>篇</span></span>", "index R0.73 group count")
    entry_title = html.escape(content.release_title_en.split(" | ", 1)[1])
    link = f'''          <li class="note-entry" data-note="r0-73y">
            <article>
              <div class="entry-copy">
                <p class="note-code">R0.73Y</p>
                <h3>{entry_title}</h3>
              </div>
              <nav class="entry-files" aria-label="R0.73Y files">
                <a class="file-link html" href="/notes/r0-73y.html" aria-label="Read R0.73Y HTML">HTML</a>
                <a class="file-link pdf" href="/notes/r0-73y.pdf" aria-label="Download R0.73Y PDF">PDF</a>
              </nav>
            </article>
          </li>\n'''
    match = re.search(r'(?m)^          <li class="note-entry" data-note="r0-73x">', value)
    if match is None:
        raise RuntimeError("note index lacks canonical R0.73X insertion marker")
    value = value[:match.start()] + link + value[match.start():]
    if value.count('<li class="note-entry"') != 201:
        raise RuntimeError("note-index DOM does not derive 201 canonical notes")
    if "/recap-r0-61-r0-73y" in value:
        raise RuntimeError("note index must not invent an R0.73Y recap")
    assert_public_html(value, "R0.73Y note index", require_boundary=False)
    return value


def manifest_payloads() -> dict[Path, bytes]:
    release = strict_json_bytes(git_bytes(BASELINE_COMMIT, "research/release-manifest.json"), "baseline release manifest")
    archive = strict_json_bytes(git_bytes(BASELINE_COMMIT, "research/formal-archive-inventory.json"), "baseline formal archive")
    published = archive.get("publishedReleases")
    sealed = archive.get("formalSealedReleases")
    backlog = archive.get("legacyFormalFigureBacklog")
    if not isinstance(published, list) or not isinstance(sealed, list) or not isinstance(backlog, list):
        raise RuntimeError("formal archive arrays are malformed")
    if published[-1:] != ["r073x"] or sealed[-1:] != ["r073x"] or "r073y" in published + sealed:
        raise RuntimeError("formal archive is not at the R0.73X baseline")
    published.append("r073y")
    sealed.append("r073y")
    archive.update({
        "latestPublishedRelease": "r073y",
        "publishedReleaseCount": len(published),
        "formalSealedReleaseCount": len(sealed),
        "legacyFormalFigureBacklogCount": len(backlog),
    })
    if (len(published), len(sealed), len(backlog)) != (103, 79, 24):
        raise RuntimeError("formal archive derived counts do not reach 103/79/24")
    archive_payload = json_bytes(archive)
    release.update({
        "latestCompletedRelease": "r073y",
        "siteVersion": "1.65",
        "publicHtmlNoteCount": 201,
        "postR060PublishedNodeCount": 141,
        "postR060RecapNodeCount": 140,
        "latestRecapRelease": "r073x",
        "latestRecapHtml": "/recap-r0-61-r0-73x.html",
        "latestRecapPdf": "/recap-r0-61-r0-73x.pdf",
        "nextRelease": "r073z",
        "latestReleaseGate": INTERFACE_TEST_PATH,
        "latestReleasePublicationTest": RELEASE_TEST_PATH,
        "latestReleaseTranslationScript": TRANSLATION_SCRIPT_PATH,
        "latestReleasePdfBinder": PDF_BINDER_SCRIPT_PATH,
        "postR070APublishedReleaseCount": 103,
        "postR070AFormalSealedReleaseCount": 79,
        "legacyFormalFigureBacklogCount": 24,
        "publicPdfNoteCount": 158,
        "recapPolicy": "MILESTONE_ONLY",
        "completionRule": (
            "Each completed research section publishes one note release. Its core transaction "
            "publishes the reviewed Chinese HTML and current routes first; local translation and "
            "the synchronized note PDF are separate later stages. Formal sealing still requires "
            "the stated proof or negative result, required certificates, independent audit, the "
            "formal figure package, accounting and publication gates. A cumulative recap is "
            "created only at a declared major milestone; a non-milestone release preserves the "
            "previous recap bytes and records published-node and recap-node counts separately."
        ),
        "formalArchiveInventory": {
            "path": "research/formal-archive-inventory.json",
            "sha256": sha256(archive_payload),
        },
    })
    site = {
        "schemaVersion": "research-site-version-v1",
        "version": "1.65",
        "latestRelease": "R0.73Y",
        "publicHtmlNoteCount": 201,
        "postR060PublishedNodeCount": 141,
        "postR060RecapNodeCount": 140,
        "latestRecapRelease": "R0.73X",
        "publicPdfNoteCount": 158,
        "publishedDate": "2026-09-01",
    }
    return {
        ROOT / "research/release-manifest.json": json_bytes(release),
        ROOT / "research/formal-archive-inventory.json": archive_payload,
        PUBLIC / "site-version.json": json_bytes(site),
        ROOT / "VERSION": b"1.65\n",
    }


def figure_payloads() -> dict[str, bytes]:
    paths = canonical_tree_files(FIGURE_SOURCE_RELATIVE)
    if paths != FIGURE_PACKAGE_PATHS:
        raise RuntimeError("R0.73Y figure staging inventory is not exactly 25 files")
    names = tuple(Path(path).name for path in paths)
    if len(set(names)) != len(names):
        raise RuntimeError("R0.73Y figure package contains nested/duplicate basenames")
    payloads = {
        Path(relative).name: current_bytes(relative)
        for relative in paths if Path(relative).name != "SHA256SUMS"
    }
    manifest = strict_json_bytes(payloads["manifest.json"], "R0.73Y figure manifest")
    manifest["publicationStatus"] = "published"
    manifest["sourcePublicationStatus"] = "staged"
    manifest["publication"] = {
        "archiveDirectory": f"public/{FIGURE_ARCHIVE_RELATIVE}",
        "researchArchiveDirectory": f"research/{FIGURE_ARCHIVE_RELATIVE}",
        "directory": "public/assets/r073y",
        "fileStem": FIGURE_ID,
        "byteIdentityRequired": True,
        "publicCopiesComplete": True,
        "assets": [
            {
                "path": f"public/assets/r073y/{FIGURE_ID}.{suffix}",
                "bytes": len(payloads[f"figure.{suffix}"]),
                "sha256": sha256(payloads[f"figure.{suffix}"]),
            }
            for suffix in ("pdf", "svg", "png")
        ],
        "releaseSourceCommit": RELEASE_SOURCE_COMMIT,
        "figureSourceCommit": FIGURE_SOURCE_COMMIT,
        "figurePackageCommit": FIGURE_PACKAGE_COMMIT,
    }
    payloads["manifest.json"] = json_bytes(manifest)
    payloads["SHA256SUMS"] = "".join(
        f"{sha256(payloads[name])}  {name}\n" for name in sorted(payloads)
    ).encode("utf-8")
    return payloads


def stage_figure(staged: dict[Path, bytes]) -> None:
    payloads = figure_payloads()
    for name, payload in payloads.items():
        staged[ROOT / f"research/{FIGURE_ARCHIVE_RELATIVE}/{name}"] = payload
        staged[PUBLIC / f"{FIGURE_ARCHIVE_RELATIVE}/{name}"] = payload
    for suffix in ("pdf", "svg", "png"):
        staged[PUBLIC / f"assets/r073y/{FIGURE_ID}.{suffix}"] = payloads[f"figure.{suffix}"]


def protected_recap_asset_paths() -> tuple[str, ...]:
    paths = [
        relative for relative in git_paths(BASELINE_COMMIT, "public")
        if re.fullmatch(r"public/recap-[^/]+\.(?:html|pdf)", relative)
    ]
    baseline_public = tuple(sorted(paths))
    current_public: list[str] = []
    for path in PUBLIC.iterdir():
        if re.fullmatch(r"recap-[^/]+\.(?:html|pdf)", path.name) is None:
            continue
        relative = path.relative_to(ROOT).as_posix()
        if path.is_symlink() or not path.is_file() or is_conflict_copy(relative):
            raise RuntimeError("unsafe public recap artifact: " + relative)
        current_public.append(relative)
    if tuple(sorted(current_public)) != baseline_public:
        raise RuntimeError("public recap inventory differs from the R0.73X milestone baseline")
    for path in (ROOT / "research").glob("r073y*recap*"):
        raise RuntimeError(
            "note-only R0.73Y release contains an undeclared recap artifact: "
            + path.relative_to(ROOT).as_posix()
        )
    paths.extend(("research/r073x_pdf_bindings.json", "research/r073x_recap_pdf_render.json"))
    values = tuple(sorted(paths))
    if len(values) != PROTECTED_RECAP_ASSET_COUNT:
        raise RuntimeError("R0.73X baseline recap-asset inventory drifted")
    return values


def protected_recap_state() -> dict[str, str]:
    # Two historical note files plus every one of the 154 recap artifacts are
    # immutable inputs to this note-only release.  The aggregate ledger makes
    # an omitted old recap fail closed without hard-coding 152 public hashes.
    ledger_rows: list[str] = []
    for relative in protected_recap_asset_paths():
        baseline = git_bytes(BASELINE_COMMIT, relative)
        present = current_bytes(relative)
        digest = sha256(baseline)
        if present != baseline or sha256(present) != digest:
            raise RuntimeError("protected recap asset drifted: " + relative)
        ledger_rows.append(digest + "  " + relative)
    ledger = ("\n".join(ledger_rows) + "\n").encode("utf-8")
    if sha256(ledger) != PROTECTED_RECAP_LEDGER_SHA256:
        raise RuntimeError("protected recap aggregate SHA ledger drifted")
    values: dict[str, str] = {}
    for relative, digest in PROTECTED_RECAP_HASHES.items():
        payload = current_bytes(relative)
        if sha256(payload) != digest or payload != git_bytes(BASELINE_COMMIT, relative):
            raise RuntimeError("protected R0.73X note/recap/PDF binding drifted: " + relative)
        values[relative] = digest
    return values


def canonical_baseline_note_count() -> int:
    return len(tuple(path for path in git_paths(BASELINE_COMMIT, "public/notes") if re.fullmatch(r"public/notes/r0-[0-9a-z-]+\.html", path)))


def validate_staged(staged: dict[Path, bytes]) -> None:
    expected = set(ROOT / relative for relative in CORE_OUTPUTS + FIGURE_RESEARCH_ARCHIVE_OUTPUTS + FIGURE_PUBLIC_ARCHIVE_OUTPUTS + FIGURE_PUBLIC_ASSET_OUTPUTS)
    missing = sorted(path.relative_to(ROOT).as_posix() for path in expected - set(staged))
    if missing:
        raise RuntimeError("R0.73Y in-memory transaction omitted: " + repr(missing))
    forbidden = [path for path in staged if "recap-r0-61-r0-73" in path.name]
    if forbidden:
        raise RuntimeError("note-only transaction attempted to stage a recap: " + repr(forbidden))
    protected_recap_state()
    for source_relative in FIGURE_PACKAGE_PATHS:
        name = Path(source_relative).name
        source = current_bytes(source_relative)
        research_copy = staged[ROOT / f"research/{FIGURE_ARCHIVE_RELATIVE}/{name}"]
        public_copy = staged[PUBLIC / f"{FIGURE_ARCHIVE_RELATIVE}/{name}"]
        if research_copy != public_copy:
            raise RuntimeError("R0.73Y research/public figure mirrors differ: " + name)
        if name not in {"manifest.json", "SHA256SUMS"} and research_copy != source:
            raise RuntimeError("R0.73Y formal-figure scientific payload drifted: " + name)
    publication_figure = strict_json_bytes(
        staged[ROOT / f"research/{FIGURE_ARCHIVE_RELATIVE}/manifest.json"],
        "staged R0.73Y publication figure manifest",
    )
    if (
        publication_figure.get("publicationStatus") != "published"
        or publication_figure.get("sourcePublicationStatus") != "staged"
        or publication_figure.get("publication", {}).get("publicCopiesComplete") is not True
    ):
        raise RuntimeError("R0.73Y formal-figure publication routing drifted")
    if canonical_baseline_note_count() + 1 != 201:
        raise RuntimeError("canonical note paths do not derive target count 201")
    note = staged[PUBLIC / "notes/r0-73y.html"].decode("utf-8")
    home = staged[PUBLIC / "research-review.html"].decode("utf-8")
    index = staged[PUBLIC / "notes/index.html"].decode("utf-8")
    if (
        "analytic exact witness / not DNS" not in note
        or "Vreman" not in note
        or "NOT CLAY" not in note
        or "production 对所有实振幅为零" not in note
        or "gradient covariance：STRICTLY POSITIVE FOR A ≠ 0; ZERO FOR A = 0" not in note
        or "A = 0 时为平凡零场" not in note
        or "/recap-r0-61-r0-73y" in note + home + index
        or 'data-release="r073y"' not in home
        or index.count('<li class="note-entry"') != 201
    ):
        raise RuntimeError("R0.73Y public note/route boundary drifted")
    release = strict_json_bytes(staged[ROOT / "research/release-manifest.json"], "staged release manifest")
    expected_accounting = {
        "latestCompletedRelease": "r073y", "siteVersion": "1.65",
        "publicHtmlNoteCount": 201, "postR060PublishedNodeCount": 141,
        "postR060RecapNodeCount": 140, "latestRecapRelease": "r073x",
        "nextRelease": "r073z", "postR070APublishedReleaseCount": 103,
        "postR070AFormalSealedReleaseCount": 79,
        "legacyFormalFigureBacklogCount": 24, "publicPdfNoteCount": 158,
    }
    if any(release.get(key) != value for key, value in expected_accounting.items()):
        raise RuntimeError("staged accounting is not 201/141/140/103/79/24/158")
    for path, payload in staged.items():
        if path.suffix == ".html":
            assert_public_html(payload.decode("utf-8"), path.name, require_boundary=path != PUBLIC / "notes/index.html")


def build_staged(content: ReleaseContent) -> dict[Path, bytes]:
    staged: dict[Path, bytes] = {}
    stage_figure(staged)
    staged[PUBLIC / "notes/r0-73y.html"] = note_page(content).encode("utf-8")
    staged[PUBLIC / "research-review.html"] = home_page(content).encode("utf-8")
    staged[PUBLIC / "literature-review.html"] = literature_page(content).encode("utf-8")
    staged[PUBLIC / "notes/index.html"] = note_index(content).encode("utf-8")
    for relative in PLANNED_AUDIT_PATHS:
        staged[PUBLIC / "research/r073y" / Path(relative).name] = current_bytes(relative)
    staged.update(manifest_payloads())
    validate_staged(staged)
    return staged


def release_source_presence() -> dict[str, bool]:
    return {relative: (ROOT / relative).is_file() and not (ROOT / relative).is_symlink() and not is_conflict_copy(relative) for relative in RELEASE_SOURCE_PATHS}


def _lstat(path: Path) -> os.stat_result | None:
    try:
        return path.lstat()
    except FileNotFoundError:
        return None


def _safe_relative(path: Path) -> Path:
    try:
        relative = path.relative_to(ROOT)
    except ValueError as exc:
        raise RuntimeError("transaction target escaped repository: " + str(path)) from exc
    if not relative.parts or any(part in ("", ".", "..") for part in relative.parts) or is_conflict_copy(relative):
        raise RuntimeError("unsafe transaction target: " + str(path))
    return relative


def _safe_parent(path: Path, created: list[Path]) -> None:
    relative = _safe_relative(path / "placeholder").parent
    cursor = ROOT
    for part in relative.parts:
        cursor /= part
        status = _lstat(cursor)
        if status is None:
            cursor.mkdir()
            created.append(cursor)
            status = _lstat(cursor)
        if status is None or stat.S_ISLNK(status.st_mode) or not stat.S_ISDIR(status.st_mode):
            raise RuntimeError("unsafe transaction parent: " + str(cursor))


def apply_transaction(staged: dict[Path, bytes]) -> dict[str, object]:
    if not staged:
        raise RuntimeError("refusing empty transaction")
    ordered = sorted(staged)
    relatives = {path: _safe_relative(path) for path in ordered}
    scratch = Path(tempfile.mkdtemp(prefix=".r073y-release-", dir=ROOT))
    created: list[Path] = []
    installed: list[Path] = []
    backups: dict[Path, Path] = {}
    try:
        for target in ordered:
            temporary = scratch / "staged" / relatives[target]
            temporary.parent.mkdir(parents=True, exist_ok=True)
            temporary.write_bytes(staged[target])
            if temporary.read_bytes() != staged[target]:
                raise RuntimeError("temporary payload readback failed")
        for target in ordered:
            _safe_parent(target.parent, created)
            if target.exists():
                if target.is_symlink() or not target.is_file():
                    raise RuntimeError("unsafe existing transaction target: " + str(target))
                backup = scratch / "backup" / relatives[target]
                backup.parent.mkdir(parents=True, exist_ok=True)
                os.replace(target, backup)
                backups[target] = backup
        for target in ordered:
            os.replace(scratch / "staged" / relatives[target], target)
            installed.append(target)
        for target in ordered:
            if target.read_bytes() != staged[target]:
                raise RuntimeError("applied payload readback failed: " + str(target))
    except BaseException:
        for target in reversed(installed):
            if target.is_file() and not target.is_symlink():
                target.unlink()
        for target, backup in backups.items():
            if backup.exists():
                os.replace(backup, target)
        for directory in reversed(created):
            try:
                directory.rmdir()
            except OSError:
                pass
        shutil.rmtree(scratch, ignore_errors=True)
        raise
    shutil.rmtree(scratch)
    return {
        "transaction": "ATOMIC_REPLACE_WITH_ROLLBACK",
        "appliedOutputs": len(staged),
        "sha256": {relatives[path].as_posix(): sha256(staged[path]) for path in ordered},
        "temporaryScratchRemoved": not scratch.exists(),
    }


def source_dry_run() -> dict[str, object]:
    status = source_status(ROOT)
    presence = release_source_presence()
    blockers = pin_blockers()
    return {
        **status,
        "mode": "source-dry-run",
        "researchSourceCommit": RESEARCH_SOURCE_COMMIT,
        "bindingOrder": [{"layer": label, "commit": commit, "ready": commit_ready(commit)} for label, commit in BINDING_ORDER],
        "normalizedReleaseSourceCommit": NORMALIZED_RELEASE_SOURCE_COMMIT,
        "commitPinsReady": not blockers,
        "commitPinBlockers": blockers,
        "certificate": certificate_summary(),
        "certificateInventoryPolicy": "DERIVED_FROM_MANIFEST_AND_REGULAR_FILES",
        "figure": figure_summary(),
        "figureExpectedFileCount": 25,
        "figureScopeLabel": "ANALYTIC_EXACT_WITNESS_NOT_DNS",
        "protectedRecapHashes": PROTECTED_RECAP_HASHES,
        "protectedRecapAssetCount": PROTECTED_RECAP_ASSET_COUNT,
        "protectedRecapLedgerSha256": PROTECTED_RECAP_LEDGER_SHA256,
        "recapGenerated": False,
        "recapProtectedByteIdentical": True,
        "releaseSourcePresence": presence,
        "releaseSourceReady": all(presence.values()),
        "coreOutputsPlanned": list(CORE_OUTPUTS),
        "laterStageOutputsPlanned": list(LATER_STAGE_OUTPUTS),
        "publicationStageOrder": list(PUBLICATION_STAGE_ORDER),
        "releaseApplication": "IMPLEMENTED_BUT_FAIL_CLOSED_UNTIL_ALL_PINS_AND_GATES_PASS",
        "ordinaryTranslationPath": "LOCAL_DIRECT_NO_DGX",
        "dgxUsed": False,
        "clayConclusion": "OPEN",
        "published": False,
        "writes": 0,
    }


def verify_release_inputs() -> ReleaseContent:
    verify_ancestry_and_pins()
    if READER_CORRECTION_PATH not in FINAL_CONTENT_PATHS:
        raise RuntimeError("R0.73Y final-content inventory omitted the reader quantifier correction")
    for relative in BASELINE_PATHS:
        git_bytes(BASELINE_COMMIT, relative)
    verify_paths(RESEARCH_SOURCE_COMMIT, FROZEN_RESEARCH_SOURCE_PATHS, "R0.73Y frozen research")
    verify_tree(CERTIFICATE_PACKAGE_COMMIT, CERTIFICATE_ROOT, "R0.73Y certificate package")
    verify_paths(FIGURE_SOURCE_COMMIT, FIGURE_SOURCE_PATHS + FIGURE_RAW_RESULT_PATHS, "R0.73Y figure source/raw")
    verify_tree(FIGURE_PACKAGE_COMMIT, FIGURE_SOURCE_RELATIVE, "R0.73Y figure package")
    verify_paths(FINAL_CONTENT_COMMIT, FINAL_CONTENT_PATHS, "R0.73Y final reader content")
    verify_paths(RELEASE_SOURCE_COMMIT, RELEASE_SOURCE_PATHS, "R0.73Y release source")
    certificate = validate_certificate()
    validate_figure(certificate)
    protected_recap_state()
    content = load_release_content(ROOT)
    if not content.publication_ready:
        raise RuntimeError("R0.73Y canonical content is not publication-ready: " + repr(content.readiness_failures))
    if not all(release_source_presence().values()):
        raise RuntimeError("R0.73Y release source inventory is incomplete")
    return content


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate or atomically apply the fail-closed note-only R0.73Y release.")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--source-dry-run", action="store_true")
    action.add_argument("--check-only", action="store_true")
    action.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if not (args.source_dry_run or args.check_only or args.apply):
        parser.print_help()
        return
    if args.source_dry_run:
        print(json.dumps(source_dry_run(), ensure_ascii=False, indent=2))
        return
    content = verify_release_inputs()
    staged = build_staged(content)
    report: dict[str, object] = {
        "release": RELEASE,
        "siteVersion": SITE_VERSION,
        "stagedOutputs": len(staged),
        "recapGenerated": False,
        "protectedRecapHashes": protected_recap_state(),
        "stagedSha256": {path.relative_to(ROOT).as_posix(): sha256(payload) for path, payload in sorted(staged.items())},
        "pdfGenerated": False,
        "translationsGenerated": False,
        "networkUsed": False,
        "dgxUsed": False,
    }
    if args.check_only:
        report.update({"checkOnly": True, "transaction": "IN_MEMORY_ONLY", "writes": 0, "localCoreApplied": False, "githubPublished": False})
    else:
        transaction = apply_transaction(staged)
        report.update({"checkOnly": False, "apply": True, **transaction, "writes": transaction["appliedOutputs"], "localCoreApplied": True, "githubPublished": False})
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except CanonicalSourceError as exc:
        raise SystemExit("R0.73Y canonical-source gate failed: " + str(exc)) from exc
    except RuntimeError as exc:
        raise SystemExit("R0.73Y release gate failed: " + str(exc)) from exc
