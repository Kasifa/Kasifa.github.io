#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fail-closed R0.73W GitHub Pages release transaction.

The reader copy is owned by :mod:`r073w_release_content`.  This module binds
that copy to immutable analytic/certificate/figure/release layers, derives all
public counts from canonical paths or parsed DOM, and first assembles the
proposed GitHub Pages transaction entirely in memory.

``--source-dry-run`` is read-only while later pins are pending.
``--check-only`` validates the complete in-memory transaction.  ``--apply``
uses the same gates, writes isolated temporary files, and installs each target
with atomic replacement and rollback.  Translation and synchronized PDF
production remain separate later transactions and are never invoked here.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from typing import Iterable

from r073w_release_content import (
    CANONICAL_SOURCE_PATHS,
    CLOSED_LEDGER,
    EXACT_SCOPE_BOUNDARY_ZH,
    FIGURE_ARCHIVE_RELATIVE,
    FIGURE_ID,
    FIGURE_SOURCE_RELATIVE,
    FINITE_LEDGER,
    OPEN_LEDGER,
    PLANNED_AUDIT_PATHS,
    R073V_BASELINE,
    R073W_TARGET,
    RELEASE,
    SITE_VERSION,
    CanonicalSourceError,
    ReleaseContent,
    load_release_content,
)


ROOT = Path(os.environ.get(
    "R073W_RELEASE_ROOT", Path(__file__).resolve().parents[1]
)).resolve()
PUBLIC = ROOT / "public"
ZERO_COMMIT = "0" * 40

BASELINE_COMMIT = "4970477d0c08992cd6881d4f3fe40362f41a7738"
FINITE_SOURCE_COMMIT = "b9f3b3943df1e2abf6abc2f51c1fb25d1f1e8440"
FINITE_PACKAGE_COMMIT = "68893eccd7f5b6047bf2b00c5262913e23fadbc3"
FINAL_CONTENT_COMMIT = "855e341e371302f315c5535006193f8ce0703740"
FINAL_CONTENT_COMMIT_STATUS = "IMMUTABLE_AFTER_FIGURE_AND_LEDGER_CLOSURE"
FIGURE_SOURCE_COMMIT = "ac6293ac4d0c46c696d2ec8e29d3fb1350e341f1"
FIGURE_PACKAGE_COMMIT = "60b0e869bbaa3a0ace185bf450e067d79fcd79b3"
RELEASE_SOURCE_COMMIT = "fe229ebc58efb4fe68144dd5662535f3fb6c3fc5"
NORMALIZED_RELEASE_SOURCE_COMMIT = "__NORMALIZED_RELEASE_SOURCE_COMMIT__"
FINAL_CONTENT_COMMIT_REQUIRED_STATUS = "IMMUTABLE_AFTER_FIGURE_AND_LEDGER_CLOSURE"

BINDING_ORDER = (
    ("R0.73V published baseline", BASELINE_COMMIT),
    ("R0.73W finite/canonical source", FINITE_SOURCE_COMMIT),
    ("R0.73W sealed finite package", FINITE_PACKAGE_COMMIT),
    ("R0.73W formal figure source/raw package", FIGURE_SOURCE_COMMIT),
    ("R0.73W formal figure package", FIGURE_PACKAGE_COMMIT),
    ("R0.73W final reader-content module", FINAL_CONTENT_COMMIT),
    ("R0.73W release source", RELEASE_SOURCE_COMMIT),
)

CERTIFICATE_ROOT = "research/certificates/r073w"
CERTIFICATE_SOURCE_PATHS = (
    f"{CERTIFICATE_ROOT}/README.md",
    f"{CERTIFICATE_ROOT}/audit-checklist.json",
    f"{CERTIFICATE_ROOT}/claim-boundary.md",
    f"{CERTIFICATE_ROOT}/command.txt",
    f"{CERTIFICATE_ROOT}/compute_fourier_certificate.py",
    f"{CERTIFICATE_ROOT}/contract.json",
    f"{CERTIFICATE_ROOT}/independent_trig_certificate.py",
    f"{CERTIFICATE_ROOT}/requirements.txt",
    f"{CERTIFICATE_ROOT}/seal_package.py",
)
CERTIFICATE_RESULT_PATHS = (
    f"{CERTIFICATE_ROOT}/results.json",
    f"{CERTIFICATE_ROOT}/independent-results.json",
)
CERTIFICATE_ARCHIVE_PATHS = tuple(sorted(
    CERTIFICATE_SOURCE_PATHS + CERTIFICATE_RESULT_PATHS + (
        f"{CERTIFICATE_ROOT}/manifest.json",
        f"{CERTIFICATE_ROOT}/SHA256SUMS",
    )
))

FIGURE_SOURCE_NAMES = (
    "README.md", "caption.md", "chart-contract-and-source-data.md", "command.txt",
    "config.json", "contract.json", "plot.py", "qa-protocol.md", "requirements.txt",
    "validate.py",
)
FIGURE_RAW_RESULT_NAMES = (
    "source-data.csv", "figure.pdf", "figure.svg", "figure.png",
    "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png", "environment.json",
    "results.json", "progress.ndjson", "resource-log.ndjson",
)
FIGURE_METADATA_NAMES = (
    "validation.json", "manifest.json", "qa-report.md", "SHA256SUMS",
)
FIGURE_SOURCE_PATHS = tuple(
    f"{FIGURE_SOURCE_RELATIVE}/{name}" for name in FIGURE_SOURCE_NAMES
)
FIGURE_RAW_RESULT_PATHS = tuple(
    f"{FIGURE_SOURCE_RELATIVE}/{name}" for name in FIGURE_RAW_RESULT_NAMES
)
FIGURE_PACKAGE_PATHS = tuple(sorted(
    FIGURE_SOURCE_PATHS + FIGURE_RAW_RESULT_PATHS + tuple(
        f"{FIGURE_SOURCE_RELATIVE}/{name}" for name in FIGURE_METADATA_NAMES
    )
))

FINAL_CONTENT_PATHS = tuple(CANONICAL_SOURCE_PATHS) + tuple(PLANNED_AUDIT_PATHS) + (
    "scripts/r073w_release_content.py",
)
BASELINE_PATHS = (
    "VERSION",
    "research/release-manifest.json",
    "research/formal-archive-inventory.json",
    "public/site-version.json",
    "public/notes/r0-73v.html",
    "public/recap-r0-61-r0-73v.html",
    "public/research-review.html",
    "public/literature-review.html",
    "public/notes/index.html",
)

TRANSLATION_SCRIPT_PATH = "scripts/add-r073w-translations.mjs"
PDF_BINDER_SCRIPT_PATH = "scripts/bind-r073w-pdfs.mjs"
RELEASE_TEST_PATH = "tests/r073w-release.test.mjs"
INTERFACE_TEST_PATH = "tests/r073w-signed-production-gate.test.mjs"
RELEASE_SOURCE_PATHS = (
    ".github/workflows/pages.yml",
    ".github/workflows/release-publication-gate.yml",
    "scripts/r073w_release_content.py",
    "scripts/generate_r073w_release.py",
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

CORE_OUTPUTS = (
    "public/notes/r0-73w.html",
    "public/recap-r0-61-r0-73w.html",
    "public/research-review.html",
    "public/literature-review.html",
    "public/notes/index.html",
    "public/research/r073w/r073w_figure_source_audit.md",
    "public/research/r073w/r073w_figure_source_reaudit.md",
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
    f"public/assets/r073w/{FIGURE_ID}.{suffix}" for suffix in ("pdf", "svg", "png")
)
LATER_STAGE_OUTPUTS = (
    "public/notes/r0-73w.pdf",
    "public/recap-r0-61-r0-73w.pdf",
    "research/r073w_note_pdf_render.json",
    "research/r073w_recap_pdf_render.json",
    "research/r073w_pdf_bindings.json",
    "translations/en.json",
    "public/i18n-en.js",
    "scripts/i18n-snapshots/r073w-missing.json",
)
PUBLICATION_STAGE_ORDER = (
    "freeze-r073v-published-baseline",
    "freeze-r073w-canonical-and-finite-sources",
    "seal-finite-package-to-immutable-source",
    "seal-formal-figure-to-immutable-source",
    "freeze-final-reader-content",
    "freeze-release-source-and-fill-normalized-self-pin",
    "validate-in-memory-html-manifest-figure-transaction",
    "capture-review-and-apply-local-translations",
    "render-synchronized-note-and-recap-pdfs",
    "bind-html-pdf-hashes-and-titles",
    "run-publication-gate-then-deploy-from-main",
)

PUBLIC_VOICE_BANS = (
    "我们", "攻关", "主攻", "突破", "研究纪律", "三重审计",
    "杀死错误想法", "颠覆性", "世界首个", "接近解决",
    "解决了千禧年", "证明了全局正则性", "原创性定理", "首次证明",
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
        value = json.loads(
            payload.decode("utf-8"), parse_constant=reject,
            object_pairs_hook=unique,
        )
    except (UnicodeDecodeError, ValueError) as exc:
        raise RuntimeError(label + ": invalid strict JSON") from exc
    if not isinstance(value, dict):
        raise RuntimeError(label + ": expected a JSON object")
    return value


def current_bytes(relative: str) -> bytes:
    path = ROOT / relative
    if not path.is_file() or path.is_symlink():
        raise RuntimeError(relative + ": expected a regular nonsymlink file")
    return path.read_bytes()


def strict_json_file(relative: str, label: str) -> dict:
    return strict_json_bytes(current_bytes(relative), label)


def run_git(arguments: list[str], *, binary: bool = False) -> str | bytes:
    result = subprocess.run(
        ["git", *arguments], cwd=ROOT, check=False,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
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


def normalized_release_generator(payload: bytes) -> bytes:
    """Normalize the intentionally self-referential release commit slot."""
    try:
        value = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError("R0.73W release generator is not UTF-8") from exc
    pattern = r'(?m)^RELEASE_SOURCE_COMMIT = (?:ZERO_COMMIT|"[0-9a-f]{40}")$'
    replacement = f'RELEASE_SOURCE_COMMIT = "{NORMALIZED_RELEASE_SOURCE_COMMIT}"'
    normalized, count = re.subn(pattern, replacement, value)
    if count != 1:
        raise RuntimeError("R0.73W normalized release-source pin slot drifted")
    return normalized.encode("utf-8")


def is_conflict_copy(relative: str | Path) -> bool:
    """Recognize OneDrive's ``name 2/3/4.ext`` conflict-copy convention."""
    return any(
        re.search(r" [234](?=\.[^.]+$|$)", part) is not None
        for part in Path(relative).parts
    )


def canonical_tree_files(relative_root: str) -> tuple[str, ...]:
    root = ROOT / relative_root
    if not root.is_dir() or root.is_symlink():
        raise RuntimeError("missing regular directory: " + relative_root)
    values = []
    for path in root.rglob("*"):
        if not path.is_file() or path.is_symlink():
            continue
        relative = path.relative_to(ROOT).as_posix()
        if not is_conflict_copy(relative):
            values.append(relative)
    return tuple(sorted(values))


def require_commit(commit: str, label: str) -> None:
    if commit == ZERO_COMMIT:
        raise RuntimeError(label + ": ZERO_COMMIT; layer is not ready")
    if re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        raise RuntimeError(label + ": expected full lowercase 40-hex commit")
    run_git(["cat-file", "-e", commit + "^{commit}"])


def verify_ancestry_and_pins() -> None:
    if FINAL_CONTENT_COMMIT_STATUS != FINAL_CONTENT_COMMIT_REQUIRED_STATUS:
        raise RuntimeError(
            "R0.73W final reader-content commit remains explicitly provisional; "
            "freeze the post-figure/post-ledger content and update both the pin "
            "and FINAL_CONTENT_COMMIT_STATUS"
        )
    for label, commit in BINDING_ORDER:
        require_commit(commit, label)
    for (_, older), (_, newer) in zip(BINDING_ORDER, BINDING_ORDER[1:]):
        result = subprocess.run(
            ["git", "merge-base", "--is-ancestor", older, newer],
            cwd=ROOT, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        if result.returncode:
            raise RuntimeError("R0.73W binding commits are not in ancestry order")


def verify_paths(commit: str, paths: Iterable[str], label: str) -> None:
    for relative in paths:
        if is_conflict_copy(relative):
            raise RuntimeError(label + ": conflict copy entered canonical inventory")
        committed = git_bytes(commit, relative)
        present = current_bytes(relative)
        if relative == "scripts/generate_r073w_release.py":
            committed = normalized_release_generator(committed)
            present = normalized_release_generator(present)
        if committed != present:
            raise RuntimeError(label + ": committed/current bytes differ: " + relative)


def verify_tree(commit: str, relative_root: str, label: str) -> None:
    committed = tuple(
        path for path in git_paths(commit, relative_root)
        if not is_conflict_copy(path)
    )
    current = canonical_tree_files(relative_root)
    if not committed or committed != current:
        raise RuntimeError(label + ": committed/current tree inventory differs")
    verify_paths(commit, committed, label)


def run_check(relative: str, arguments: list[str], label: str) -> None:
    result = subprocess.run(
        [sys.executable, "-B", str(ROOT / relative), *arguments],
        cwd=ROOT, check=False, capture_output=True, text=True,
    )
    if result.returncode:
        detail = (result.stderr or result.stdout).strip()
        raise RuntimeError(label + " failed: " + detail[-3000:])


def validate_certificate() -> dict:
    manifest = strict_json_file(
        f"{CERTIFICATE_ROOT}/manifest.json", "R0.73W certificate manifest"
    )
    checklist = strict_json_file(
        f"{CERTIFICATE_ROOT}/audit-checklist.json", "R0.73W certificate checklist"
    )
    primary = strict_json_file(
        f"{CERTIFICATE_ROOT}/results.json", "R0.73W certificate results"
    )
    independent = strict_json_file(
        f"{CERTIFICATE_ROOT}/independent-results.json",
        "R0.73W independent certificate results",
    )
    expected_inventory = {
        "boundFileCount": 11,
        "generatedFileCount": 4,
        "packageFileCount": 13,
        "sha256SumsLineCount": 12,
        "sourceFileCount": 9,
    }
    expected_names = {Path(path).name for path in CERTIFICATE_ARCHIVE_PATHS}
    actual_names = {
        path.name for path in (ROOT / CERTIFICATE_ROOT).iterdir()
        if path.is_file() and not path.is_symlink() and not is_conflict_copy(path)
    }
    comparison = manifest.get("comparison")
    scope = manifest.get("scopeFlags")
    if (
        manifest.get("schemaVersion")
        != "r073w-signed-production-exact-manifest-v1"
        or manifest.get("release") != RELEASE
        or manifest.get("status") != "SEALED_COMMIT_BOUND"
        or manifest.get("finalSeal") is not True
        or manifest.get("sourceCommitAssigned") is not True
        or manifest.get("sourceCommit") != FINITE_SOURCE_COMMIT
        or manifest.get("allPrerequisiteChecksPass") is not True
        or manifest.get("primaryWitnessKey") != "rankThreeExtension"
        or manifest.get("checkInventory") != {
            "exactPerPath": 56,
            "requiredPerPath": 56,
            "twoPathComparisons": 2,
        }
        or manifest.get("inventory") != expected_inventory
        or manifest.get("ordinaryTranslationPath") != "LOCAL_DIRECT_NO_DGX"
        or manifest.get("dgxUsed") is not False
        or not isinstance(comparison, dict)
        or comparison.get("commonCoreByteIdentical") is not True
        or comparison.get("independentImportsPrimaryProducer") is not False
        or not isinstance(scope, dict)
        or scope.get("primaryWitnessFrequencyRank") != 3
        or scope.get("retainedLowerDimensionalDiagnostic") != "2D3C"
        or scope.get("arbitraryThreeDimensionalGlobalRegularity") != "OPEN"
        or scope.get("clayConclusion") != "OPEN"
        or scope.get("notClay") is not True
        or scope.get("ordinaryTranslationPath") != "LOCAL_DIRECT_NO_DGX"
        or scope.get("dgxUsed") is not False
    ):
        raise RuntimeError("R0.73W certificate final seal or scope drifted")
    required = checklist.get("requiredChecks")
    if not isinstance(required, list) or len(required) != 56:
        raise RuntimeError("R0.73W certificate checklist is not 56 rows")
    if len({row.get("id") for row in required if isinstance(row, dict)}) != 56:
        raise RuntimeError("R0.73W certificate checklist IDs are not unique")
    for result, label in ((primary, "primary"), (independent, "independent")):
        audit = result.get("audit")
        if (
            not isinstance(audit, dict)
            or audit.get("required") != 56
            or audit.get("passed") != 56
            or not isinstance(audit.get("rows"), list)
            or len(audit["rows"]) != 56
            or not all(isinstance(row, dict) and row.get("pass") is True
                       for row in audit["rows"])
        ):
            raise RuntimeError(f"R0.73W {label} 56-check audit drifted")
    if primary.get("commonCore") != independent.get("commonCore"):
        raise RuntimeError("R0.73W producer commonCore objects differ")
    if actual_names != expected_names:
        raise RuntimeError("R0.73W certificate 13-file inventory drifted")
    rows = manifest.get("files")
    source_rows = manifest.get("sourceBindings")
    commit_rows = manifest.get("sourceCommitBindings")
    if (
        not isinstance(rows, list) or len(rows) != 11
        or not isinstance(source_rows, list) or len(source_rows) != 9
        or not isinstance(commit_rows, list) or len(commit_rows) != 9
    ):
        raise RuntimeError("R0.73W certificate 11/9/9 binding inventory drifted")
    by_name = {
        row.get("path"): row for row in rows
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    }
    if set(by_name) != expected_names - {"manifest.json", "SHA256SUMS"}:
        raise RuntimeError("R0.73W certificate bound path set drifted")
    for name, row in by_name.items():
        payload = current_bytes(f"{CERTIFICATE_ROOT}/{name}")
        if row.get("bytes") != len(payload) or row.get("sha256") != sha256(payload):
            raise RuntimeError("R0.73W certificate byte binding drifted: " + name)
    run_check(
        f"{CERTIFICATE_ROOT}/compute_fourier_certificate.py", ["--check-only"],
        "R0.73W primary certificate",
    )
    run_check(
        f"{CERTIFICATE_ROOT}/independent_trig_certificate.py", ["--check-only"],
        "R0.73W independent certificate",
    )
    run_check(
        f"{CERTIFICATE_ROOT}/seal_package.py",
        ["--source-commit", FINITE_SOURCE_COMMIT, "--check-only"],
        "R0.73W commit-bound certificate seal",
    )
    return manifest


def figure_summary() -> dict[str, object]:
    base = ROOT / FIGURE_SOURCE_RELATIVE
    source_files = [] if not base.is_dir() else [
        path.name for path in base.iterdir()
        if path.is_file() and not path.is_symlink() and not is_conflict_copy(path)
    ]
    manifest_path = base / "manifest.json"
    validation_path = base / "validation.json"
    summary: dict[str, object] = {
        "figureId": FIGURE_ID,
        "sourceFilesPresent": sorted(source_files),
        "expectedSourceFiles": list(FIGURE_SOURCE_NAMES),
        "expectedRawResultFiles": list(FIGURE_RAW_RESULT_NAMES),
        "expectedPackageFileCount": len(FIGURE_PACKAGE_PATHS),
        "manifestPresent": manifest_path.is_file() and not manifest_path.is_symlink(),
        "validationPresent": validation_path.is_file() and not validation_path.is_symlink(),
        "formal": False,
    }
    if not summary["manifestPresent"]:
        summary["pending"] = "formal-figure-manifest-missing"
        return summary
    try:
        manifest = strict_json_bytes(manifest_path.read_bytes(), "R0.73W figure manifest")
    except RuntimeError as exc:
        summary["pending"] = str(exc)
        return summary
    summary.update({
        "schemaVersion": manifest.get("schemaVersion"),
        "figureSchemaVersion": manifest.get("figureSchemaVersion"),
        "status": manifest.get("status"),
        "publicationStatus": manifest.get("publicationStatus"),
    })
    validation: dict | None = None
    required: object = None
    passed: object = None
    if summary["validationPresent"]:
        validation = strict_json_bytes(
            validation_path.read_bytes(), "R0.73W figure validation"
        )
        # The raw producer uses checksRequired/checksPassed; the final content
        # contract uses required/passed.  Report either without guessing a
        # future fixed check count.
        required = validation.get("required", validation.get("checksRequired"))
        passed = validation.get("passed", validation.get("checksPassed"))
        summary["validation"] = {
            "schemaVersion": validation.get("schemaVersion"),
            "status": validation.get("status"),
            "passed": passed,
            "required": required,
            "checksObserved": len(validation.get("checks", []))
            if isinstance(validation.get("checks"), list) else None,
        }
    seal = manifest.get("seal")
    qa = manifest.get("qa")
    checks = validation.get("checks") if isinstance(validation, dict) else None
    summary["formal"] = bool(
        FIGURE_SOURCE_COMMIT != ZERO_COMMIT
        and manifest.get("schemaVersion") == "research-figure-manifest-v1"
        and manifest.get("figureSchemaVersion")
        == "r073w-signed-production-manifest-v1"
        and manifest.get("status") == "formal"
        and manifest.get("publicationStatus") == "staged"
        and isinstance(seal, dict)
        and seal.get("figureSourceCommitAssigned") is True
        and seal.get("figureSourceCommit") == FIGURE_SOURCE_COMMIT
        and seal.get("requiresParentFigureSourceCommitFinalReseal") is False
        and isinstance(qa, dict) and qa.get("status") == "passed"
        and isinstance(validation, dict)
        and validation.get("schemaVersion")
        == "r073w-signed-production-validation-v1"
        and validation.get("status") == "PASS"
        and isinstance(required, int) and required > 0
        and passed == required
        and isinstance(checks, list) and len(checks) == required
    )
    if not summary["formal"]:
        summary["pending"] = "formal-figure-final-seal-or-immutable-pin-pending"
    return summary


def validate_figure(certificate: dict) -> dict:
    base = FIGURE_SOURCE_RELATIVE
    manifest = strict_json_file(f"{base}/manifest.json", "R0.73W figure manifest")
    validation = strict_json_file(
        f"{base}/validation.json", "R0.73W figure validation"
    )
    seal = manifest.get("seal")
    qa = manifest.get("qa")
    passed = validation.get("passed")
    required = validation.get("required")
    if (
        manifest.get("schemaVersion") != "research-figure-manifest-v1"
        or manifest.get("figureSchemaVersion")
        != "r073w-signed-production-manifest-v1"
        or manifest.get("figureId") != FIGURE_ID
        or manifest.get("release") != RELEASE
        or manifest.get("status") != "formal"
        or manifest.get("publicationStatus") != "staged"
        or not isinstance(seal, dict)
        or seal.get("figureSourceCommitAssigned") is not True
        or seal.get("figureSourceCommit") != FIGURE_SOURCE_COMMIT
        or seal.get("requiresParentFigureSourceCommitFinalReseal") is not False
        or seal.get("state") != "formal-figure-source-seal"
        or not isinstance(qa, dict) or qa.get("status") != "passed"
        or validation.get("schemaVersion")
        != "r073w-signed-production-validation-v1"
        or validation.get("status") != "PASS"
        or not isinstance(required, int) or required <= 0
        or passed != required
        or qa.get("validationChecks") != required
        or not isinstance(validation.get("checks"), list)
        or len(validation["checks"]) != required
        or not all(isinstance(row, dict) and row.get("pass") is True
                   for row in validation["checks"])
        or certificate.get("sourceCommit") != FINITE_SOURCE_COMMIT
    ):
        raise RuntimeError("R0.73W formal figure seal/validation drifted")
    actual = set(canonical_tree_files(base))
    if actual != set(FIGURE_PACKAGE_PATHS):
        raise RuntimeError("R0.73W formal figure 25-file inventory drifted")
    bindings = seal.get("figureSourceBindings")
    expected_bound = set(FIGURE_SOURCE_PATHS + FIGURE_RAW_RESULT_PATHS)
    if not isinstance(bindings, list) or len(bindings) != len(expected_bound):
        raise RuntimeError("R0.73W figure source/raw binding count drifted")
    bound_paths = {
        row.get("path") for row in bindings
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    }
    if bound_paths != expected_bound:
        raise RuntimeError("R0.73W figure source/raw binding paths drifted")
    sums: dict[str, str] = {}
    for line in current_bytes(f"{base}/SHA256SUMS").decode("utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/]+)", line)
        if match is None or match.group(2) in sums:
            raise RuntimeError("R0.73W figure SHA256SUMS syntax drifted")
        sums[match.group(2)] = match.group(1)
    expected_sum_names = {Path(path).name for path in FIGURE_PACKAGE_PATHS} - {"SHA256SUMS"}
    if set(sums) != expected_sum_names:
        raise RuntimeError("R0.73W figure SHA256SUMS inventory drifted")
    for name, digest in sums.items():
        if sha256(current_bytes(f"{base}/{name}")) != digest:
            raise RuntimeError("R0.73W figure SHA256SUMS mismatch: " + name)
    return manifest


def certificate_summary() -> dict[str, object]:
    path = ROOT / CERTIFICATE_ROOT / "manifest.json"
    if not path.is_file() or path.is_symlink():
        return {"finalSeal": False, "pending": "certificate-manifest-missing"}
    manifest = strict_json_bytes(path.read_bytes(), "R0.73W certificate manifest")
    return {
        "finalSeal": manifest.get("finalSeal") is True,
        "status": manifest.get("status"),
        "sourceCommit": manifest.get("sourceCommit"),
        "primaryWitnessKey": manifest.get("primaryWitnessKey"),
        "inventory": manifest.get("inventory"),
        "checks": manifest.get("checkInventory"),
        "commonCoreByteIdentical": manifest.get("comparison", {}).get(
            "commonCoreByteIdentical"
        ),
    }


def decode_baseline(relative: str) -> str:
    try:
        return git_bytes(BASELINE_COMMIT, relative).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError(relative + ": baseline is not UTF-8") from exc


def replace_once(value: str, old: str, new: str, label: str) -> str:
    count = value.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one marker, found {count}")
    return value.replace(old, new, 1)


def replace_regex_once(value: str, pattern: str, replacement: str, label: str) -> str:
    # Use a callback so LaTeX backslashes in generated HTML are literal and
    # are never interpreted as regular-expression replacement escapes.
    result, count = re.subn(
        pattern, lambda _match: replacement, value, count=1, flags=re.S
    )
    if count != 1:
        raise RuntimeError(f"{label}: expected one regex marker, found {count}")
    return result


def assert_public_html(value: str, label: str, *, require_boundary: bool = True) -> None:
    if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", value):
        raise RuntimeError(label + ": control character")
    for phrase in PUBLIC_VOICE_BANS:
        if phrase in value:
            raise RuntimeError(label + ": public voice violation: " + phrase)
    for token in ("R0.73W", "/i18n-en.js?v=1.63"):
        if token not in value:
            raise RuntimeError(label + ": missing token " + token)
    if require_boundary and "NOT CLAY" not in value:
        raise RuntimeError(label + ": missing NOT CLAY boundary")


def note_page(content: ReleaseContent) -> str:
    title = html.escape(content.document_title_en)
    value = f'''<!doctype html>
<html lang="zh-CN" data-site-version="1.63">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><script>document.documentElement.classList.add('js')</script>
<script defer src="/i18n-en.js?v=1.63"></script>
<style>:root{{--paper:#f3ecd8;--ink:#26231d;--rule:#8b2f2b;--muted:#625d52}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:17px/1.75 Georgia,"Noto Serif SC",serif}}.top{{border-bottom:3px double var(--ink);padding:12px 5vw;display:flex;justify-content:space-between}}main{{width:min(920px,90vw);margin:auto}}.hero{{padding:64px 0 32px;border-bottom:1px solid var(--ink)}}h1{{font-size:clamp(2rem,6vw,4.3rem);line-height:1.05}}h2{{margin-top:3rem;color:var(--rule)}}.stamp,.section-no{{font:700 12px/1.4 ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase}}article{{padding:20px 0 80px}}.equation{{overflow:auto;background:#fff8e8;padding:14px;border-left:4px solid var(--rule)}}a{{color:#702824}}img{{max-width:100%;height:auto}}@media(max-width:600px){{body{{font-size:15px}}}}</style></head>
<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.73W · NOT CLAY</span></nav><main>
{content.note_hero}
{content.note_article}
</main></body></html>'''
    assert_public_html(value, "R0.73W note")
    return value


def recap_page(content: ReleaseContent) -> str:
    value = decode_baseline("public/recap-r0-61-r0-73v.html")
    value = value.replace("/i18n-en.js?v=1.62", "/i18n-en.js?v=1.63")
    value = value.replace('data-site-version="1.62"', 'data-site-version="1.63"')
    for old, new in (
        ("R0.61–R0.73V", "R0.61–R0.73W"),
        ("R0.61 到 R0.73V", "R0.61 到 R0.73W"),
        ("R0.69P–R0.73V", "R0.69P–R0.73W"),
        ("R0.70A–R0.73V", "R0.70A–R0.73W"),
        ("回顾截止节点：R0.73V", "回顾截止节点：R0.73W"),
        ("收录节点：138", "收录节点：139"),
        ("回顾截止时公开笔记：198", "回顾截止时公开笔记：199"),
        ("138 节", "139 节"),
        ("138 个节点", "139 个节点"),
        ("100 个版本", "101 个版本"),
        ("100 节", "101 节"),
        ("76 个满足", "77 个满足"),
        ("76 节", "77 节"),
        ("57 个阶段", "58 个阶段"),
        ("57 个研究阶段", "58 个研究阶段"),
        ("<strong>138</strong>", "<strong>139</strong>"),
        ("<strong>100</strong>", "<strong>101</strong>"),
        ("<strong>76</strong>", "<strong>77</strong>"),
    ):
        value = value.replace(old, new)
    value = replace_regex_once(
        value,
        r'<meta name="description" content="[^"]*">',
        '<meta name="description" content="R0.60 之后的完整研究回顾：R0.61 到 R0.73W '
        '共 139 个节点；最新一节分开带符号亚滤波 production、heat-plane 特征线、'
        '能量类尺度损失、精确反例与局部化缺口。">',
        "recap meta description",
    )
    value = replace_regex_once(
        value,
        r'<meta property="og:description" content="[^"]*">',
        '<meta property="og:description" content="58 个阶段、139 个节点：从约化递推和环带排除，'
        '推进到带符号亚滤波 production 的精确恒等式、能量类边界与反例证书。">',
        "recap Open Graph description",
    )
    value = replace_once(
        value,
        '          </div>\n        </section>\n\n        <section id="node-index"',
        content.recap_phase
        + '\n          </div>\n        </section>\n\n        <section id="node-index"',
        "recap phase append",
    )
    node = (
        '<span class="node-ref"><a href="/notes/r0-73w.html">R0.73W</a>'
        '<span class="node-state kind-closed">闭</span></span>'
    )
    value = replace_once(
        value,
        '          </div>\n        </section>\n\n        <section id="retained"',
        f'            {node}\n          </div>\n        </section>\n\n        <section id="retained"',
        "recap node append",
    )
    value = replace_regex_once(
        value, r'<section id="value">.*?</section>',
        '<section id="value"><div class="section-no">04 / 目前的判断</div>'
        '<h2>精确带符号支付、能量类尺度损失与反例边界已经分开</h2>'
        f'<p>{html.escape(content.recap_zh)}</p>'
        '<p>139 个节点或 101 个公开版本都不是 Clay 完成比例。局部化、零尺度一致控制、'
        'continuation criterion 与任意三维数据正则性保持开放。NOT CLAY。</p></section>',
        "recap current value",
    )
    value = replace_regex_once(
        value, r'<section id="next">.*?</section>',
        '<section id="next"><div class="section-no">05 / 下一步</div>'
        f'<h2>{html.escape(content.next_release)}：局部 heat-characteristic 与 defect 账本</h2>'
        f'<p>{html.escape(content.next_gate_zh)}</p></section>',
        "recap next gate",
    )
    value = replace_regex_once(
        value, r'<section id="claims">.*?</section>',
        '<section id="claims"><div class="section-no">06 / 说明边界</div>'
        '<h2>经典、本地解析、有限证书与开放命题分开列示</h2>'
        '<p>R0.70A–R0.73W 的 101 节已公开；77 节完整封存；24 节旧档待回补。</p>'
        f'<p>{html.escape(CLOSED_LEDGER)}</p><p>{html.escape(FINITE_LEDGER)}</p>'
        f'<p>{html.escape(OPEN_LEDGER)}</p><p>{html.escape(EXACT_SCOPE_BOUNDARY_ZH)} '
        'NOT CLAY。</p></section>',
        "recap exact boundary",
    )
    value = value.replace(
        'href="/recap-r0-61-r0-73v.html"', 'href="/recap-r0-61-r0-73w.html"'
    )
    value = value.replace(
        'href="/recap-r0-61-r0-73v.pdf"', 'href="/recap-r0-61-r0-73w.pdf"'
    )
    value = replace_regex_once(
        value, r'<section id="reproduce">.*?</section>',
        '<section id="reproduce"><div class="section-no">07 / 原始资料</div>'
        '<h2>逐节笔记、证明、审计、证书、附图和历史回顾</h2>'
        '<p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · '
        '<a href="/recap-r0-61-r0-73v.html">保留 R0.73V 历史回顾</a> · '
        '<a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · '
        '<a href="/notes/r0-73w.html">打开最新节点 R0.73W</a></p>'
        '<p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073w_report-source.md">查看 canonical report</a> · '
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073w_signed_production_identities.md">查看解析证明</a> · '
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073w_primary_literature_audit.md">查看一手文献审计</a> · '
        '<a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073w">查看有限证书</a> · '
        '<a href="/assets/r073w/fig-r073w-signed-production.pdf">下载期刊附图</a> · '
        '<a href="/recap-r0-61-r0-73w.pdf">下载同步 PDF</a></p>'
        '<p>经典结论由一手来源承担；本地解析证明承担精确恒等式和条件推论；有限证书只作可复现系数核验。NOT CLAY。</p>'
        '</section>',
        "recap current source links",
    )
    if value.count('<article class="phase">') != 58:
        raise RuntimeError("R0.73W recap must contain exactly 58 phase articles")
    if value.count('class="node-ref"') != 139:
        raise RuntimeError("R0.73W recap DOM must derive exactly 139 nodes")
    assert_public_html(value, "R0.73W recap")
    return value


def home_page(content: ReleaseContent) -> str:
    value = decode_baseline("public/research-review.html")
    value = value.replace("v=1.62", "v=1.63").replace('data-site-version="1.62"', 'data-site-version="1.63"')
    value = replace_once(value, "<strong>v1.62</strong>", "<strong>v1.63</strong>", "home version")
    value = value.replace("v1.62", "v1.63")
    value = replace_once(value, "<strong>198</strong>公开研究笔记", "<strong>199</strong>公开研究笔记", "home note count")
    value = replace_once(value, "<strong>R0.73V</strong>最新研究节点", "<strong>R0.73W</strong>最新研究节点", "home latest")
    value = replace_regex_once(
        value,
        r'<section class="route-overview latest-release-spotlight".*?</section>',
        '<section class="route-overview latest-release-spotlight" id="latest-release"><div class="route-overview-inner">'
        + '<p class="eyebrow">LATEST RELEASE · R0.73W · ' + html.escape(content.date) + '</p>'
        + '<h2>' + html.escape(content.public_title_zh) + '</h2><p>' + html.escape(content.home_zh) + '</p>'
        + '<p><a href="/notes/r0-73w.pdf">阅读最新 R0.73W 研究笔记 →</a> · '
        + '<a href="/recap-r0-61-r0-73w.html">139 节累计回顾</a> · '
        + '<a href="/notes/">199 篇研究笔记总索引</a></p>'
        + '<p>R0.70A–R0.73W · 101 节已公开 · 77 节完整封存 · NOT CLAY</p></div></section>',
        "home latest spotlight",
    )
    marker = '<div class="task-one" id="r073v" data-release="r073v"'
    value = replace_once(
        value, marker, content.home_card + "\n          " + marker,
        "home card reverse-chronological insert",
    )
    value = value.replace("NEXT · R0.73W", "NEXT · R0.73X")
    value = replace_regex_once(
        value, r'<h3>R0\.73W 下一接口</h3><p>.*?</p>',
        f'<h3>{html.escape(content.next_release)} 下一接口</h3>'
        f'<p>{html.escape(content.next_gate_zh)}</p>',
        "home next interface",
    )
    value = value.replace(
        "R0.70A–R0.73V：100 节已公开，76 节完整封存",
        "R0.70A–R0.73W：101 节已公开，77 节完整封存",
    )
    value = replace_regex_once(
        value,
        r'<div class="task-one" id="post-r060-recap".*?</div>',
        '<div class="task-one" id="post-r060-recap" style="margin-top:2rem">'
        '<p class="eyebrow">累计回顾 R0.61–R0.73W · ' + html.escape(content.date) + '</p>'
        '<h3>R0.60 recap 之后的累计回顾收录 139 个节点；全站现有 199 篇公开研究笔记</h3>'
        '<p>累计回顾现分 58 个阶段，完整保留 R0.61–R0.73W；最新节点分开记录带符号亚滤波 '
        'production、heat-plane 特征线、能量类尺度损失、精确反例与局部化缺口。</p>'
        '<p>R0.70A–R0.73W 共 101 个版本已公开；77 个按当前 formal-figure 合同完整封存，'
        '24 个旧版附图档案仍列入回补清单。</p>'
        '<p><strong>阶段判断：</strong>&nbsp;' + html.escape(content.recap_zh) + ' '
        '任意三维初值全局正则性与 Clay 保持 OPEN。</p>'
        '<p><a href="/recap-r0-61-r0-73w.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · '
        '<a href="/recap-r0-61-r0-73w.pdf">下载同步 PDF</a></p></div>',
        "home cumulative recap card",
    )
    value = value.replace("/recap-r0-61-r0-73v.html", "/recap-r0-61-r0-73w.html")
    value = value.replace("/recap-r0-61-r0-73v.pdf", "/recap-r0-61-r0-73w.pdf")
    assert_public_html(value, "R0.73W home")
    return value


def literature_page(content: ReleaseContent) -> str:
    value = decode_baseline("public/literature-review.html")
    value = value.replace("v=1.62", "v=1.63").replace('data-site-version="1.62"', 'data-site-version="1.63"')
    value = value.replace("v1.62", "v1.63")
    route_step = (
        '<div class="route-step kept"><header><b>R0.73W</b>'
        '<strong>signed subfilter production and heat-plane characteristics</strong></header>'
        f'<p><strong>{html.escape(content.public_title_zh)}</strong></p>'
        '<p>R0.70A–R0.73W：101 节已公开，77 节完整封存。</p>'
        f'<p>{html.escape(content.recap_zh)} '
        '<a href="/notes/r0-73w.html">研究笔记</a> '
        '<a href="/recap-r0-61-r0-73w.html">当前累计回顾</a> '
        '<a href="#r073w-boundary">文献边界</a></p></div>'
        '<div class="route-step pause"><header><b>开放接口 · R0.73X</b>'
        '<strong>localized heat-characteristic and defect ledger</strong></header>'
        f'<p>{html.escape(content.next_gate_zh)} '
        '任意初值全局正则性与 Clay 保持 OPEN。</p></div>'
    )
    value = replace_regex_once(
        value,
        r'<div class="route-step pause"><header><b>开放接口 · R0\.73W</b>.*?</div>',
        route_step,
        "literature current route step",
    )
    value = value.replace("/recap-r0-61-r0-73v.html", "/recap-r0-61-r0-73w.html")
    block = (
        '<section id="r073w-boundary"><h3>R0.73W 文献归属与主张边界</h3><p>'
        + content.literature_update + '</p><p>' + html.escape(CLOSED_LEDGER) + '</p><p>'
        + html.escape(FINITE_LEDGER) + '</p><p>' + html.escape(OPEN_LEDGER)
        + '。' + html.escape(EXACT_SCOPE_BOUNDARY_ZH) + ' NOT CLAY。</p></section>'
    )
    value = replace_once(value, "</main>", block + "\n  </main>", "literature append")
    assert_public_html(value, "R0.73W literature")
    return value


def note_index(content: ReleaseContent) -> str:
    value = decode_baseline("public/notes/index.html")
    value = value.replace("v=1.62", "v=1.63").replace('data-site-version="1.62"', 'data-site-version="1.63"')
    value = value.replace("v1.62", "v1.63")
    value = value.replace("198 篇公开研究笔记", "199 篇公开研究笔记")
    value = value.replace("最新节点 R0.73V", "最新节点 R0.73W")
    value = replace_once(value, "<strong>198</strong>", "<strong>199</strong>", "index HTML count")
    value = replace_once(value, "<strong>155</strong>", "<strong>156</strong>", "index PDF count")
    value = replace_once(value, "<strong>R0.73V</strong>", "<strong>R0.73W</strong>", "index latest")
    value = replace_once(value, "<span>22</span> <span>篇</span>", "<span>23</span> <span>篇</span>", "index series count")
    value = value.replace("/recap-r0-61-r0-73v.html", "/recap-r0-61-r0-73w.html")
    link = (
        '          <li class="note-entry" data-note="r0-73w"><article>'
        '<div class="entry-copy"><p class="note-code">R0.73W</p><h3>'
        + html.escape(content.document_title_en.split("|", 1)[-1].strip())
        + '</h3></div><nav class="entry-files" aria-label="R0.73W files">'
        '<a class="file-link html" href="/notes/r0-73w.html" aria-label="Read R0.73W HTML">HTML</a>'
        '<a class="file-link pdf" href="/notes/r0-73w.pdf" aria-label="Download R0.73W PDF">PDF</a>'
        '</nav></article></li>'
    )
    match = re.search(r'<li class="note-entry" data-note="r0-73v">', value)
    if match is None:
        raise RuntimeError("note index lacks canonical r073v insertion marker")
    value = value[:match.start()] + link + "\n" + value[match.start():]
    if value.count('<li class="note-entry"') != 199:
        raise RuntimeError("note-index DOM does not derive 199 canonical notes")
    assert_public_html(value, "R0.73W note index", require_boundary=False)
    return value


def manifest_payloads(content: ReleaseContent) -> dict[Path, bytes]:
    release = strict_json_bytes(
        git_bytes(BASELINE_COMMIT, "research/release-manifest.json"),
        "baseline release manifest",
    )
    archive = strict_json_bytes(
        git_bytes(BASELINE_COMMIT, "research/formal-archive-inventory.json"),
        "baseline formal archive",
    )
    site = strict_json_bytes(
        git_bytes(BASELINE_COMMIT, "public/site-version.json"),
        "baseline site version",
    )
    if any(release.get(key) != value for key, value in R073V_BASELINE.items()):
        raise RuntimeError("R0.73V baseline release accounting drifted")
    published = archive.get("publishedReleases")
    sealed = archive.get("formalSealedReleases")
    if not isinstance(published, list) or not isinstance(sealed, list):
        raise RuntimeError("formal archive release arrays are absent")
    if published[-1:] != ["r073v"] or sealed[-1:] != ["r073v"]:
        raise RuntimeError("formal archive is not at r073v baseline")
    if "r073w" in published or "r073w" in sealed:
        raise RuntimeError("formal archive already contains r073w")
    published.append("r073w")
    sealed.append("r073w")
    archive.update({
        "latestPublishedRelease": "r073w",
        "publishedReleaseCount": len(published),
        "formalSealedReleaseCount": len(sealed),
        "legacyFormalFigureBacklogCount": 24,
    })
    if (
        len(published) != R073W_TARGET["postR070APublishedReleaseCount"]
        or len(sealed) != R073W_TARGET["postR070AFormalSealedReleaseCount"]
    ):
        raise RuntimeError("formal archive derived counts do not reach 101/77")
    archive_payload = json_bytes(archive)
    release.update({
        "latestCompletedRelease": "r073w",
        "siteVersion": SITE_VERSION,
        "publicHtmlNoteCount": R073W_TARGET["publicHtmlNoteCount"],
        "postR060RecapNodeCount": R073W_TARGET["postR060RecapNodeCount"],
        "nextRelease": "r073x",
        "latestReleaseGate": INTERFACE_TEST_PATH,
        "latestReleasePublicationTest": RELEASE_TEST_PATH,
        "postR070APublishedReleaseCount": len(published),
        "postR070AFormalSealedReleaseCount": len(sealed),
        "legacyFormalFigureBacklogCount": 24,
        "formalArchiveInventory": {
            "path": "research/formal-archive-inventory.json",
            "sha256": sha256(archive_payload),
        },
    })
    site.update({
        "version": SITE_VERSION,
        "latestRelease": RELEASE,
        "publicHtmlNoteCount": R073W_TARGET["publicHtmlNoteCount"],
        "publishedDate": content.date,
    })
    return {
        ROOT / "research/release-manifest.json": json_bytes(release),
        ROOT / "research/formal-archive-inventory.json": archive_payload,
        PUBLIC / "site-version.json": json_bytes(site),
        ROOT / "VERSION": b"1.63\n",
    }


def figure_payloads() -> dict[str, bytes]:
    paths = canonical_tree_files(FIGURE_SOURCE_RELATIVE)
    if set(paths) != set(FIGURE_PACKAGE_PATHS):
        raise RuntimeError("R0.73W figure staging inventory is not the canonical 25 files")
    names = tuple(Path(path).name for path in paths)
    if len(set(names)) != len(names):
        raise RuntimeError("R0.73W figure package contains nested/duplicate basenames")
    if not {"manifest.json", "SHA256SUMS", "figure.pdf", "figure.svg", "figure.png"}.issubset(names):
        raise RuntimeError("R0.73W figure package lacks canonical publication files")
    payloads = {Path(path).name: current_bytes(path) for path in paths if Path(path).name != "SHA256SUMS"}
    manifest = strict_json_bytes(payloads["manifest.json"], "R0.73W figure manifest")
    manifest["publicationStatus"] = "published"
    manifest["sourcePublicationStatus"] = "staged"
    manifest["publication"] = {
        "archiveDirectory": f"public/{FIGURE_ARCHIVE_RELATIVE}",
        "researchArchiveDirectory": f"research/{FIGURE_ARCHIVE_RELATIVE}",
        "directory": "public/assets/r073w",
        "fileStem": FIGURE_ID,
        "byteIdentityRequired": True,
        "publicCopiesComplete": True,
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
        staged[ROOT / "research" / FIGURE_ARCHIVE_RELATIVE / name] = payload
        staged[PUBLIC / FIGURE_ARCHIVE_RELATIVE / name] = payload
    for suffix in ("pdf", "svg", "png"):
        staged[PUBLIC / f"assets/r073w/{FIGURE_ID}.{suffix}"] = payloads[f"figure.{suffix}"]


def canonical_baseline_note_count() -> int:
    paths = git_paths(BASELINE_COMMIT, "public/notes")
    values = [
        path for path in paths
        if re.fullmatch(r"public/notes/r0-[0-9a-z]+\.html", path)
        and not is_conflict_copy(path)
    ]
    return len(values)


def validate_staged(staged: dict[Path, bytes]) -> None:
    for path in staged:
        relative = path.relative_to(ROOT).as_posix()
        if is_conflict_copy(relative):
            raise RuntimeError("OneDrive conflict copy entered staged transaction: " + relative)
    required_outputs = (
        CORE_OUTPUTS + FIGURE_RESEARCH_ARCHIVE_OUTPUTS
        + FIGURE_PUBLIC_ARCHIVE_OUTPUTS + FIGURE_PUBLIC_ASSET_OUTPUTS
    )
    missing = [relative for relative in required_outputs if ROOT / relative not in staged]
    if missing:
        raise RuntimeError("R0.73W in-memory transaction omitted: " + repr(missing))
    if canonical_baseline_note_count() + 1 != 199:
        raise RuntimeError("canonical note paths do not derive target count 199")
    recap = staged[PUBLIC / "recap-r0-61-r0-73w.html"].decode("utf-8")
    if recap.count('class="node-ref"') != 139:
        raise RuntimeError("recap DOM does not derive 139 indexed nodes")
    if recap.count('<article class="phase">') != 58:
        raise RuntimeError("recap DOM does not derive 58 grouped phase articles")
    if (
        "最新一节分开带符号亚滤波 production、heat-plane 特征线" not in recap
        or "打开最新节点 R0.73W" not in recap
        or "research/r073w_report-source.md" not in recap
        or "research/certificates/r073w" not in recap
        or "/assets/r073w/fig-r073w-signed-production.pdf" not in recap
        or "打开最新节点 R0.73V" in recap
    ):
        raise RuntimeError("recap current metadata/source surface is stale")
    home = staged[PUBLIC / "research-review.html"].decode("utf-8")
    if home.count('data-release="r073w"') != 1 or home.count('id="latest-release"') != 1:
        raise RuntimeError("home DOM lacks one canonical R0.73W route/card")
    recap_card_match = re.search(
        r'<div class="task-one" id="post-r060-recap".*?</div>', home, re.DOTALL
    )
    if recap_card_match is None:
        raise RuntimeError("home DOM lacks the cumulative recap card")
    recap_card = recap_card_match.group(0)
    if not all(token in recap_card for token in (
        "R0.61–R0.73W", "139 个节点", "199 篇公开研究笔记", "58 个阶段",
        "101 个版本已公开", "77 个按当前 formal-figure 合同完整封存",
    )) or any(token in recap_card for token in (
        "累计回顾 R0.61–R0.73V", "完整保留 R0.61–R0.73V",
        "R0.70A–R0.73V 共", "138 个节点", "198 篇公开研究笔记", "57 个阶段",
    )):
        raise RuntimeError("home cumulative recap card is stale")
    index = staged[PUBLIC / "notes/index.html"].decode("utf-8")
    if index.count('data-note="r0-73w"') != 1:
        raise RuntimeError("note-index DOM lacks one canonical R0.73W entry")
    release = strict_json_bytes(staged[ROOT / "research/release-manifest.json"], "staged release manifest")
    expected = {
        "latestCompletedRelease": "r073w",
        "siteVersion": "1.63",
        "publicHtmlNoteCount": 199,
        "postR060RecapNodeCount": 139,
        "nextRelease": "r073x",
        "postR070APublishedReleaseCount": 101,
        "postR070AFormalSealedReleaseCount": 77,
        "legacyFormalFigureBacklogCount": 24,
    }
    if any(release.get(key) != value for key, value in expected.items()):
        raise RuntimeError("staged release accounting is not 1.63/199/139/101/77/24")
    for path, payload in staged.items():
        if path.suffix == ".html":
            assert_public_html(
                payload.decode("utf-8"), path.name,
                require_boundary=path != PUBLIC / "notes/index.html",
            )


def build_staged(content: ReleaseContent) -> dict[Path, bytes]:
    """Build and fully validate the transaction without writing any target."""
    staged: dict[Path, bytes] = {}
    stage_figure(staged)
    staged[PUBLIC / "notes/r0-73w.html"] = note_page(content).encode("utf-8")
    staged[PUBLIC / "recap-r0-61-r0-73w.html"] = recap_page(content).encode("utf-8")
    staged[PUBLIC / "research-review.html"] = home_page(content).encode("utf-8")
    staged[PUBLIC / "literature-review.html"] = literature_page(content).encode("utf-8")
    staged[PUBLIC / "notes/index.html"] = note_index(content).encode("utf-8")
    for relative in PLANNED_AUDIT_PATHS:
        staged[PUBLIC / "research/r073w" / Path(relative).name] = current_bytes(relative)
    staged.update(manifest_payloads(content))
    validate_staged(staged)
    return staged


def release_source_presence() -> dict[str, bool]:
    return {
        relative: (ROOT / relative).is_file()
        and not (ROOT / relative).is_symlink()
        and not is_conflict_copy(relative)
        for relative in RELEASE_SOURCE_PATHS
    }


def _lstat(path: Path) -> os.stat_result | None:
    try:
        return path.lstat()
    except FileNotFoundError:
        return None


def _safe_target_relative(path: Path) -> Path:
    try:
        relative = path.relative_to(ROOT)
    except ValueError as exc:
        raise RuntimeError("transaction target escaped repository: " + str(path)) from exc
    if not relative.parts or any(part in ("", ".", "..") for part in relative.parts):
        raise RuntimeError("unsafe transaction target traversal: " + str(path))
    if is_conflict_copy(relative):
        raise RuntimeError("conflict copy cannot be a transaction target: " + relative.as_posix())
    return relative


def _assert_safe_root() -> None:
    status = _lstat(ROOT)
    if (
        status is None or stat.S_ISLNK(status.st_mode)
        or not stat.S_ISDIR(status.st_mode)
    ):
        raise RuntimeError("unsafe transaction root: " + str(ROOT))


def _assert_safe_target(path: Path, *, allow_missing_parents: bool) -> Path:
    relative = _safe_target_relative(path)
    _assert_safe_root()
    cursor = ROOT
    for part in relative.parts[:-1]:
        cursor = cursor / part
        status = _lstat(cursor)
        if status is None:
            if allow_missing_parents:
                break
            raise RuntimeError("missing transaction parent: " + str(cursor))
        if stat.S_ISLNK(status.st_mode) or not stat.S_ISDIR(status.st_mode):
            raise RuntimeError("unsafe transaction ancestor: " + str(cursor))
    status = _lstat(path)
    if status is not None and (
        stat.S_ISLNK(status.st_mode) or not stat.S_ISREG(status.st_mode)
    ):
        raise RuntimeError("unsafe transaction target: " + str(path))
    return relative


def _ensure_safe_parent(parent: Path, created: list[Path]) -> None:
    try:
        relative = parent.relative_to(ROOT)
    except ValueError as exc:
        raise RuntimeError("transaction parent escaped repository: " + str(parent)) from exc
    _assert_safe_root()
    cursor = ROOT
    for part in relative.parts:
        if part in ("", ".", "..") or is_conflict_copy(part):
            raise RuntimeError("unsafe transaction parent component: " + part)
        cursor = cursor / part
        status = _lstat(cursor)
        if status is None:
            try:
                cursor.mkdir(mode=0o755)
                created.append(cursor)
            except FileExistsError:
                pass
            status = _lstat(cursor)
        if status is None or stat.S_ISLNK(status.st_mode) or not stat.S_ISDIR(status.st_mode):
            raise RuntimeError("unsafe transaction ancestor: " + str(cursor))


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _remove_transaction_scratch(path: Path) -> None:
    if path.parent != ROOT or not path.name.startswith(".r073w-release-"):
        raise RuntimeError("refusing unsafe transaction scratch cleanup: " + str(path))
    status = _lstat(path)
    if status is None:
        return
    if stat.S_ISLNK(status.st_mode) or not stat.S_ISDIR(status.st_mode):
        raise RuntimeError("unsafe transaction scratch directory: " + str(path))
    shutil.rmtree(path)


def apply_transaction(staged: dict[Path, bytes]) -> dict[str, object]:
    """Install an already validated staged map with atomic replaces and rollback."""
    if not staged:
        raise RuntimeError("refusing to apply an empty R0.73W transaction")
    ordered = sorted(staged)
    relatives: dict[Path, Path] = {}
    for target in ordered:
        relatives[target] = _assert_safe_target(target, allow_missing_parents=True)
        payload = staged[target]
        if not isinstance(payload, bytes):
            raise RuntimeError("transaction payload is not bytes: " + str(target))

    scratch = Path(tempfile.mkdtemp(prefix=".r073w-release-", dir=ROOT))
    staged_root = scratch / "staged"
    backup_root = scratch / "backup"
    created_directories: list[Path] = []
    rows: list[dict[str, object]] = []
    rollback_errors: list[str] = []
    committed = False
    try:
        # Phase 1: materialize and verify every payload in an isolated tree.
        for target in ordered:
            relative = relatives[target]
            temporary = staged_root / relative
            temporary.parent.mkdir(parents=True, exist_ok=True)
            with temporary.open("xb") as stream:
                stream.write(staged[target])
                stream.flush()
                os.fsync(stream.fileno())
            if temporary.read_bytes() != staged[target]:
                raise RuntimeError("temporary transaction payload readback failed: " + relative.as_posix())
            backup = backup_root / relative
            backup.parent.mkdir(parents=True, exist_ok=True)
            rows.append({
                "target": target,
                "relative": relative,
                "temporary": temporary,
                "backup": backup,
                "existed": False,
                "backedUp": False,
                "installed": False,
            })
        _fsync_directory(scratch)

        # Phase 2: create only required safe parents, then snapshot all old
        # targets into the scratch tree before installing any new payload.
        for row in rows:
            target = Path(row["target"])
            _ensure_safe_parent(target.parent, created_directories)
            _assert_safe_target(target, allow_missing_parents=False)
            row["existed"] = _lstat(target) is not None
        for row in rows:
            if row["existed"]:
                target = Path(row["target"])
                backup = Path(row["backup"])
                _assert_safe_target(target, allow_missing_parents=False)
                os.replace(target, backup)
                row["backedUp"] = True

        # Phase 3: each installation is atomic on the repository filesystem.
        for row in rows:
            target = Path(row["target"])
            temporary = Path(row["temporary"])
            _assert_safe_target(target, allow_missing_parents=False)
            os.replace(temporary, target)
            row["installed"] = True
            _fsync_directory(target.parent)

        # Phase 4: byte-for-byte readback while rollback is still possible.
        for row in rows:
            target = Path(row["target"])
            relative = Path(row["relative"])
            _assert_safe_target(target, allow_missing_parents=False)
            if target.read_bytes() != staged[target]:
                raise RuntimeError("applied transaction readback failed: " + relative.as_posix())
        committed = True
    except BaseException as exc:
        for row in reversed(rows):
            target = Path(row["target"])
            backup = Path(row["backup"])
            try:
                if row["installed"] and _lstat(target) is not None:
                    status = _lstat(target)
                    if status is None or stat.S_ISLNK(status.st_mode) or not stat.S_ISREG(status.st_mode):
                        raise RuntimeError("unsafe installed target during rollback: " + str(target))
                    target.unlink()
                if row["backedUp"] and _lstat(backup) is not None:
                    _ensure_safe_parent(target.parent, created_directories)
                    os.replace(backup, target)
                    _fsync_directory(target.parent)
            except BaseException as rollback_exc:
                rollback_errors.append(str(rollback_exc))
        for directory in reversed(created_directories):
            try:
                directory.rmdir()
            except OSError:
                pass
        if rollback_errors:
            raise RuntimeError(
                "R0.73W transaction failed and rollback was incomplete; scratch retained at "
                + str(scratch) + "; rollback errors=" + repr(rollback_errors)
            ) from exc
        _remove_transaction_scratch(scratch)
        raise
    finally:
        if committed and _lstat(scratch) is not None:
            _remove_transaction_scratch(scratch)

    return {
        "transaction": "ATOMIC_REPLACE_WITH_ROLLBACK",
        "appliedOutputs": len(rows),
        "createdDirectories": [
            path.relative_to(ROOT).as_posix() for path in created_directories
        ],
        "sha256": {
            relatives[path].as_posix(): sha256(staged[path]) for path in ordered
        },
        "temporaryScratchRemoved": _lstat(scratch) is None,
    }


def source_dry_run() -> dict[str, object]:
    content = load_release_content(ROOT)
    presence = release_source_presence()
    zero_layers = [label for label, commit in BINDING_ORDER if commit == ZERO_COMMIT]
    pin_blockers = list(zero_layers)
    if FINAL_CONTENT_COMMIT_STATUS != FINAL_CONTENT_COMMIT_REQUIRED_STATUS:
        pin_blockers.append(
            "R0.73W final reader-content commit is explicitly provisional"
        )
    return {
        "release": RELEASE,
        "siteVersion": SITE_VERSION,
        "mode": "source-dry-run",
        "title": content.release_title_en,
        "publicTitleZh": content.public_title_zh,
        "baselineAccounting": R073V_BASELINE,
        "targetAccounting": R073W_TARGET,
        "canonicalSources": list(CANONICAL_SOURCE_PATHS),
        "canonicalSourceSha256": content.source_sha256,
        "plannedAuditPaths": list(PLANNED_AUDIT_PATHS),
        "finiteCertificateSourcePaths": list(CERTIFICATE_SOURCE_PATHS),
        "finiteCertificateResultPaths": list(CERTIFICATE_RESULT_PATHS),
        "certificateArchivePaths": list(CERTIFICATE_ARCHIVE_PATHS),
        "figureSourcePaths": list(FIGURE_SOURCE_PATHS),
        "figureRawResultPaths": list(FIGURE_RAW_RESULT_PATHS),
        "figurePackagePaths": list(FIGURE_PACKAGE_PATHS),
        "certificate": certificate_summary(),
        "figure": figure_summary(),
        "publicationReady": content.publication_ready,
        "readinessFailures": list(content.readiness_failures),
        "commitPinsReady": not pin_blockers,
        "commitPinBlockers": pin_blockers,
        "zeroCommitLayers": zero_layers,
        "finalContentCommit": FINAL_CONTENT_COMMIT,
        "finalContentCommitStatus": FINAL_CONTENT_COMMIT_STATUS,
        "finalContentCommitPrerequisitesSatisfied": {
            "formalFigureFinalSeal": True,
            "canonicalLedgerClosure": True,
        },
        "releaseSourcePresence": presence,
        "releaseSourceReady": all(presence.values()),
        "publicTransaction": "IN_MEMORY_GATE_THEN_ATOMIC_REPLACE_WITH_ROLLBACK",
        "publicWritesImplemented": True,
        "releaseApplication": "IMPLEMENTED_BUT_FAIL_CLOSED_UNTIL_ALL_PINS_AND_GATES_PASS",
        "published": False,
        "coreOutputsPlanned": list(CORE_OUTPUTS),
        "figureResearchArchiveOutputsPlanned": list(FIGURE_RESEARCH_ARCHIVE_OUTPUTS),
        "figurePublicArchiveOutputsPlanned": list(FIGURE_PUBLIC_ARCHIVE_OUTPUTS),
        "figurePublicAssetOutputsPlanned": list(FIGURE_PUBLIC_ASSET_OUTPUTS),
        "laterStageOutputsPlanned": list(LATER_STAGE_OUTPUTS),
        "translationScriptExpected": TRANSLATION_SCRIPT_PATH,
        "pdfBinderScriptExpected": PDF_BINDER_SCRIPT_PATH,
        "releaseTestExpected": RELEASE_TEST_PATH,
        "interfaceTestExpected": INTERFACE_TEST_PATH,
        "publicationStageOrder": list(PUBLICATION_STAGE_ORDER),
        "ordinaryTranslationPath": "LOCAL_DIRECT_NO_DGX",
        "dgxUsed": False,
        "clayConclusion": "OPEN",
        "writes": 0,
    }


def verify_release_inputs() -> ReleaseContent:
    verify_ancestry_and_pins()
    for relative in BASELINE_PATHS:
        git_bytes(BASELINE_COMMIT, relative)
    verify_paths(FINITE_SOURCE_COMMIT, CERTIFICATE_SOURCE_PATHS, "R0.73W finite source")
    verify_tree(FINITE_PACKAGE_COMMIT, CERTIFICATE_ROOT, "R0.73W certificate package")
    verify_paths(FINAL_CONTENT_COMMIT, FINAL_CONTENT_PATHS, "R0.73W final content")
    verify_paths(
        FIGURE_SOURCE_COMMIT, FIGURE_SOURCE_PATHS + FIGURE_RAW_RESULT_PATHS,
        "R0.73W figure source/raw",
    )
    verify_tree(FIGURE_PACKAGE_COMMIT, FIGURE_SOURCE_RELATIVE, "R0.73W figure package")
    verify_paths(RELEASE_SOURCE_COMMIT, RELEASE_SOURCE_PATHS, "R0.73W release source")
    certificate = validate_certificate()
    validate_figure(certificate)
    content = load_release_content(ROOT)
    if not content.publication_ready:
        raise RuntimeError(
            "R0.73W canonical content is not publication-ready: "
            + repr(content.readiness_failures)
        )
    if not all(release_source_presence().values()):
        raise RuntimeError("R0.73W translation/binder/test release sources are pending")
    return content


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate or atomically apply the fail-closed R0.73W release transaction."
    )
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
        "stagedSha256": {
            path.relative_to(ROOT).as_posix(): sha256(payload)
            for path, payload in sorted(staged.items())
        },
        "pdfGenerated": False,
        "translationsGenerated": False,
        "networkUsed": False,
        "dgxUsed": False,
    }
    if args.check_only:
        report.update({
            "checkOnly": True,
            "transaction": "IN_MEMORY_ONLY",
            "writes": 0,
            "localCoreApplied": False,
            "githubPublished": False,
        })
    else:
        transaction = apply_transaction(staged)
        report.update({
            "checkOnly": False,
            "apply": True,
            **transaction,
            "writes": transaction["appliedOutputs"],
            "localCoreApplied": True,
            "githubPublished": False,
        })
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except CanonicalSourceError as exc:
        raise SystemExit("R0.73W canonical-source gate failed: " + str(exc)) from exc
    except RuntimeError as exc:
        raise SystemExit("R0.73W release gate failed: " + str(exc)) from exc
