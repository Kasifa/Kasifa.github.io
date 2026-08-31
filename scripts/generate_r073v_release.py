#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fail-closed R0.73V GitHub Pages release transaction.

The mathematical copy comes from ``r073v_release_content.py``.  This file owns
only immutable-source binding, deterministic page assembly, release accounting,
formal-figure publication copies, and the atomic transaction boundary.
``--source-dry-run`` remains read-only while pins are incomplete.  Both
``--check-only`` and ``--apply`` require every layer in ``BINDING_ORDER``.

Translations, synchronized PDFs, and PDF/HTML bindings are deliberately later
stages; applying this transaction alone never constitutes a completed release.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile

from r073v_release_content import (
    CANONICAL_SOURCE_PATHS,
    CLOSED_LEDGER,
    FINITE_LEDGER,
    FIGURE_ARCHIVE_RELATIVE,
    FIGURE_ID,
    FIGURE_SOURCE_RELATIVE,
    EXACT_SCOPE_BOUNDARY_ZH,
    OPEN_LEDGER,
    PLANNED_AUDIT_PATHS,
    R073U_BASELINE,
    R073V_TARGET,
    RELEASE,
    SITE_VERSION,
    CanonicalSourceError,
    ReleaseContent,
    load_release_content,
)


ROOT = Path(os.environ.get(
    "R073V_RELEASE_ROOT", Path(__file__).resolve().parents[1]
)).resolve()
PUBLIC = ROOT / "public"
ZERO_COMMIT = "0" * 40

# Binding order is oldest to newest.  The published R0.73U baseline, the
# R0.73V analytic layer, and the exact certificate are immutable.
# The final reader-content layer is immutable.  Only the release-source self-pin
# deliberately remains zero until the release-source paths are committed;
# --source-dry-run is usable in both states while --check-only and --apply fail
# closed pre-seal.
RELEASE_BASELINE_COMMIT = "ebc75b1614994d09eafd60ac926469dcebb54b94"
ANALYTIC_SOURCE_COMMIT = "25636c886f1ee2449418b5548b42f9f0fa269b47"
FINITE_SOURCE_COMMIT = "7c445c522a241bdc8b867b6fce0f0fed9b82e97d"
FINITE_PACKAGE_COMMIT = "b34d91ea96c257b943f11d134e8024138e5f3cb0"
FIGURE_SOURCE_COMMIT = "680fde5a24834b8e1c877f651eb20b119c671f49"
FIGURE_PACKAGE_COMMIT = "b413586aa7a7389f8943acb2469eb28cdbbf31f3"
FINAL_CONTENT_COMMIT = "5d5b0ae7ba9bc35acbb729f97052c7673c351904"
RELEASE_SOURCE_COMMIT = "3b54b9210726d8cef9c9302e686afb0054b89ae2"

BINDING_ORDER = (
    ("R0.73U published baseline", RELEASE_BASELINE_COMMIT),
    ("R0.73V finite source", FINITE_SOURCE_COMMIT),
    ("R0.73V sealed finite package", FINITE_PACKAGE_COMMIT),
    ("R0.73V analytic source", ANALYTIC_SOURCE_COMMIT),
    ("R0.73V formal figure source/raw package", FIGURE_SOURCE_COMMIT),
    ("R0.73V formal figure package", FIGURE_PACKAGE_COMMIT),
    ("R0.73V final reader content", FINAL_CONTENT_COMMIT),
    ("R0.73V release source", RELEASE_SOURCE_COMMIT),
)

ANALYTIC_EXACT_PATHS = (
    "research/r073v_problem_freeze.md",
    "research/r073v_independent_analytic_audit.md",
    "research/r073v_primary_literature_audit.md",
)
FINAL_CONTENT_EXACT_PATHS = (
    "research/r073v_signed_third_order_heat_lift.md",
    "research/r073v_claim_source_ledger.md",
    "research/r073v_evidence_gap_matrix.md",
    "research/r073v_finite_diagnostic_audit.md",
    "research/r073v_report-source.md",
    "research/r073v_bilingual_dictionary.md",
    "research/r073v_figure_source_audit.md",
    "research/r073v_figure_source_reaudit.md",
)
FINITE_EXACT_ROOTS = ("research/certificates/r073v",)
FIGURE_EXACT_ROOTS = (FIGURE_SOURCE_RELATIVE,)
BASELINE_EXACT_PATHS = (
    "VERSION",
    "research/release-manifest.json",
    "research/formal-archive-inventory.json",
    "public/site-version.json",
    "public/notes/r0-73u.html",
    "public/recap-r0-61-r0-73u.html",
    "public/research-review.html",
    "public/literature-review.html",
    "public/notes/index.html",
)
RELEASE_SOURCE_EXACT_PATHS = (
    ".github/workflows/pages.yml",
    ".github/workflows/release-publication-gate.yml",
    "scripts/r073v_release_content.py",
    "scripts/generate_r073v_release.py",
    "scripts/add-r073v-translations.mjs",
    "scripts/bind-r073v-pdfs.mjs",
    "scripts/render-note-pdf.mjs",
    "tests/r073v-signed-third-order-interface-gate.test.mjs",
    "tests/r073v-release.test.mjs",
    "tests/site-route-current-boundary.test.mjs",
)

CORE_TARGET_OUTPUTS = (
    "public/notes/r0-73v.html",
    "public/recap-r0-61-r0-73v.html",
    "public/research-review.html",
    "public/literature-review.html",
    "public/notes/index.html",
    "public/research/r073v/r073v_figure_source_audit.md",
    "public/research/r073v/r073v_figure_source_reaudit.md",
    "public/site-version.json",
    "research/release-manifest.json",
    "research/formal-archive-inventory.json",
    "VERSION",
)
LATER_STAGE_OUTPUTS = (
    "public/notes/r0-73v.pdf",
    "public/recap-r0-61-r0-73v.pdf",
    "research/r073v_note_pdf_render.json",
    "research/r073v_recap_pdf_render.json",
    "research/r073v_pdf_bindings.json",
    "translations/en.json",
    "public/i18n-en.js",
    "scripts/i18n-snapshots/r073v-missing.json",
)
FIGURE_PUBLIC_OUTPUTS = (
    f"research/{FIGURE_ARCHIVE_RELATIVE}/manifest.json",
    f"public/{FIGURE_ARCHIVE_RELATIVE}/manifest.json",
    f"public/assets/r073v/{FIGURE_ID}.pdf",
    f"public/assets/r073v/{FIGURE_ID}.svg",
    f"public/assets/r073v/{FIGURE_ID}.png",
)
PUBLICATION_STAGE_ORDER = (
    "freeze-r073u-published-baseline",
    "freeze-r073v-analytic-and-package-sources",
    "seal-finite-package-to-immutable-source",
    "seal-formal-figure-to-immutable-source",
    "freeze-final-report-and-bilingual-ledger",
    "freeze-release-source-and-fill-normalized-pin",
    "apply-html-manifest-and-figure-transaction",
    "capture-review-and-apply-local-translations",
    "render-synchronized-note-and-recap-pdfs",
    "bind-html-pdf-hashes-and-titles",
    "run-publication-gate-then-deploy-from-main",
)

PUBLIC_TRANSACTION_IMPLEMENTED = True
NORMALIZED_RELEASE_SOURCE_COMMIT = "__NORMALIZED_RELEASE_SOURCE_COMMIT__"
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


def current_regular_bytes(relative: str) -> bytes:
    path = ROOT / relative
    if not path.is_file() or path.is_symlink():
        raise RuntimeError(relative + ": expected a regular nonsymlink file")
    return path.read_bytes()


def strict_json_file(relative: str, label: str) -> dict:
    return strict_json_bytes(current_regular_bytes(relative), label)


def strict_ndjson_file(relative: str, label: str) -> list[dict]:
    try:
        text = current_regular_bytes(relative).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError(label + ": invalid UTF-8") from exc
    lines = text.splitlines()
    if not lines or any(not line.strip() for line in lines):
        raise RuntimeError(label + ": expected nonempty NDJSON without blank rows")
    return [
        strict_json_bytes((line + "\n").encode("utf-8"), f"{label} row {index}")
        for index, line in enumerate(lines, start=1)
    ]


def run_git(arguments: list[str], *, binary: bool = False) -> str | bytes:
    completed = subprocess.run(
        ["git", *arguments], cwd=ROOT, check=False,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "git command failed: git " + " ".join(arguments) + ": "
            + completed.stderr.decode("utf-8", "replace").strip()
        )
    return completed.stdout if binary else completed.stdout.decode("utf-8").strip()


def git_bytes(commit: str, relative: str) -> bytes:
    value = run_git(["cat-file", "blob", f"{commit}:{relative}"], binary=True)
    assert isinstance(value, bytes)
    return value


def git_paths(commit: str, relative: str) -> list[str]:
    value = run_git(["ls-tree", "-r", "--name-only", commit, "--", relative])
    assert isinstance(value, str)
    return sorted(row for row in value.splitlines() if row)


def normalized_release_generator(payload: bytes) -> bytes:
    text = payload.decode("utf-8")
    pattern = r'(?m)^RELEASE_SOURCE_COMMIT = (?:ZERO_COMMIT|"[0-9a-f]{40}")$'
    replacement = f'RELEASE_SOURCE_COMMIT = "{NORMALIZED_RELEASE_SOURCE_COMMIT}"'
    normalized, count = re.subn(pattern, replacement, text)
    if count != 1:
        raise RuntimeError("R0.73V normalized release-source pin slot drift")
    return normalized.encode("utf-8")


def require_full_commit(value: str, label: str) -> None:
    if value == ZERO_COMMIT:
        raise RuntimeError(
            f"{label}: unsealed 40-zero commit pin; binding remains fail-closed"
        )
    if re.fullmatch(r"[0-9a-f]{40}", value) is None:
        raise RuntimeError(label + ": expected full lowercase 40-hex commit")
    run_git(["cat-file", "-e", value + "^{commit}"])


def verify_binding_order() -> None:
    for label, commit in BINDING_ORDER:
        require_full_commit(commit, label)
    for (_, older), (_, newer) in zip(BINDING_ORDER, BINDING_ORDER[1:]):
        completed = subprocess.run(
            ["git", "merge-base", "--is-ancestor", older, newer],
            cwd=ROOT, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        if completed.returncode != 0:
            raise RuntimeError("R0.73V binding commits are not in declared ancestry order")


def verify_commit_paths(commit: str, paths: tuple[str, ...], label: str) -> None:
    for relative in paths:
        committed = git_bytes(commit, relative)
        present = current_regular_bytes(relative)
        if relative == "scripts/generate_r073v_release.py":
            committed = normalized_release_generator(committed)
            present = normalized_release_generator(present)
        if committed != present:
            raise RuntimeError(label + ": committed blob differs from working source " + relative)


def verify_commit_trees(commit: str, roots: tuple[str, ...], label: str) -> None:
    for relative_root in roots:
        current_root = ROOT / relative_root
        if not current_root.is_dir() or current_root.is_symlink():
            raise RuntimeError(label + ": missing regular directory " + relative_root)
        output = run_git(["ls-tree", "-r", "--name-only", commit, "--", relative_root])
        assert isinstance(output, str)
        committed_paths = tuple(sorted(row for row in output.splitlines() if row))
        if not committed_paths:
            raise RuntimeError(label + ": committed tree is empty " + relative_root)
        current_paths = tuple(sorted(
            path.relative_to(ROOT).as_posix()
            for path in current_root.rglob("*")
            if path.is_file() or path.is_symlink()
        ))
        if committed_paths != current_paths:
            raise RuntimeError(label + ": committed tree inventory differs from working source " + relative_root)
        verify_commit_paths(commit, committed_paths, label)


def verify_pinned_paths_exist(commit: str, paths: tuple[str, ...], label: str) -> None:
    """Verify frozen baseline inputs without comparing regenerated worktree bytes."""
    for relative in paths:
        try:
            git_bytes(commit, relative)
        except RuntimeError as exc:
            raise RuntimeError(label + ": path absent from pin at " + relative) from exc


def decode_baseline(relative: str) -> str:
    try:
        return git_bytes(RELEASE_BASELINE_COMMIT, relative).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError(relative + ": frozen R0.73U baseline is not UTF-8") from exc


def replace_once(value: str, old: str, new: str, label: str) -> str:
    count = value.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one marker, found {count}")
    return value.replace(old, new, 1)


def replace_regex(value: str, pattern: str, replacement, label: str) -> str:
    callback = replacement if callable(replacement) else lambda _match: replacement
    result, count = re.subn(pattern, callback, value, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"{label}: expected one regex match, found {count}")
    return result


def assert_public_html(value: str, label: str, *, require_boundary: bool = True) -> None:
    if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", value):
        raise RuntimeError(label + ": control character")
    for phrase in PUBLIC_VOICE_BANS:
        if phrase in value:
            raise RuntimeError(label + ": public-voice violation " + phrase)
    tokens = ["R0.73V", "/i18n-en.js?v=1.62"]
    if require_boundary:
        tokens.append("NOT CLAY")
    for token in tokens:
        if token not in value:
            raise RuntimeError(label + ": missing token " + token)


def run_package_verifier(
    relative: str,
    arguments: list[str],
    label: str,
    *,
    executable: str | None = None,
) -> None:
    command = [executable or sys.executable, "-B", str(ROOT / relative), *arguments]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        detail = (result.stderr or result.stdout).strip()
        raise RuntimeError(label + " --verify-only failed: " + detail[-3000:])


def require_pass_payload(payload: dict, label: str) -> None:
    if not (
        payload.get("allChecksPass") is True
        or payload.get("allPrerequisiteChecksPass") is True
    ):
        raise RuntimeError(label + ": pass flag drift")
    checks = payload.get("checks")
    if isinstance(checks, dict):
        passed = bool(checks) and all(value is True for value in checks.values())
    elif isinstance(checks, list):
        passed = bool(checks) and all(
            isinstance(row, dict) and row.get("pass") is True for row in checks
        )
    else:
        passed = checks is None
    if not passed:
        raise RuntimeError(label + ": one or more checks failed")


def require_exact_scope_figure_boundary(contract: dict) -> None:
    """Reject minimality, whole-field collision, hierarchy, or Clay overclaims."""
    try:
        caption = current_regular_bytes(
            f"{FIGURE_SOURCE_RELATIVE}/caption.md"
        ).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError("R0.73V figure caption is not UTF-8") from exc
    boundary = contract.get("claimBoundary")
    if not isinstance(boundary, dict):
        raise RuntimeError("R0.73V figure claim boundary is absent")
    forbidden = {
        "informationTheoreticMinimalityEstablished": False,
        "wholeFieldNonRecoveryEstablished": False,
        "fourthOrderNonClosureEstablished": False,
        "finiteHierarchyNoGoEstablished": False,
        "pdeClosureEstablished": False,
        "globalRegularityEstablished": False,
        "clayProblemSolved": False,
    }
    for key, expected in forbidden.items():
        if boundary.get(key) is not expected:
            raise RuntimeError("R0.73V figure overclaim boundary drifted: " + key)
    folded = caption.casefold()
    if not all(token in folded for token in (
        "coefficientwise", "no closure theorem", "clay conclusion follows",
    )):
        raise RuntimeError(
            "R0.73V caption lost coefficientwise / no-Clay-conclusion scope"
        )


def validate_certificate_package() -> dict:
    base = "research/certificates/r073v"
    manifest = strict_json_file(f"{base}/manifest.json", "R0.73V certificate manifest")
    checklist = strict_json_file(
        f"{base}/audit-checklist.json", "R0.73V certificate checklist"
    )
    results = strict_json_file(f"{base}/results.json", "R0.73V certificate results")
    independent = strict_json_file(
        f"{base}/independent-results.json", "R0.73V independent certificate results"
    )
    expected_inventory = {
        "boundFileCount": 10,
        "generatedFileCount": 4,
        "packageFileCount": 12,
        "sha256SumsLineCount": 11,
        "sourceFileCount": 8,
    }
    inventory = {
        "README.md", "SHA256SUMS", "audit-checklist.json", "command.txt",
        "compute_exact_certificate.py", "contract.json", "independent-results.json",
        "independent_recompute.py", "manifest.json", "requirements.txt",
        "results.json", "seal_package.py",
    }
    source_names = {
        "README.md", "audit-checklist.json", "command.txt",
        "compute_exact_certificate.py", "contract.json", "independent_recompute.py",
        "requirements.txt", "seal_package.py",
    }
    scope = manifest.get("scopeFlags")
    comparison = manifest.get("comparison")
    if (
        manifest.get("schemaVersion")
        != "r073v-signed-third-order-exact-manifest-v1"
        or manifest.get("release") != RELEASE
        or manifest.get("status") != "sealed"
        or manifest.get("finalSeal") is not True
        or manifest.get("sourceCommitAssigned") is not True
        or manifest.get("sourceCommit") != FINITE_SOURCE_COMMIT
        or manifest.get("allPrerequisiteChecksPass") is not True
        or manifest.get("checkInventory") != {
            "exact": 66, "required": 66, "twoPathComparisons": 2,
        }
        or manifest.get("inventory") != expected_inventory
        or not isinstance(scope, dict)
        or scope.get("coefficientwiseNonRecoveryOnly") is not True
        or scope.get("cAloneInformationTheoreticallyInsufficient") != "OPEN"
        or scope.get("arbitraryThreeDimensionalGlobalRegularity") != "OPEN"
        or scope.get("clayConclusion") != "OPEN"
        or scope.get("notClay") is not True
        or scope.get("ordinaryTranslationPath") != "LOCAL_DIRECT_NO_DGX"
        or not isinstance(comparison, dict)
        or comparison.get("commonCoreByteIdentical") is not True
        or comparison.get("independentImportsPrimaryProducer") is not False
        or comparison.get("completeTableDigest")
        != "a7494d44f45b1249a513ac4d44476b7ce5af622b0d59928f4e4631d9715c22f7"
    ):
        raise RuntimeError("R0.73V certificate is not final-sealed to its source and scope")

    required_checks = checklist.get("requiredChecks")
    audit = results.get("audit")
    if (
        checklist.get("schemaVersion") != 1
        or not isinstance(required_checks, list)
        or len(required_checks) != 66
        or len({row.get("id") for row in required_checks if isinstance(row, dict)}) != 66
        or not isinstance(audit, dict)
        or audit.get("required") != 66
        or audit.get("passed") != 66
        or not isinstance(audit.get("results"), list)
        or len(audit["results"]) != 66
        or not all(isinstance(row, dict) and row.get("pass") is True
                   for row in audit["results"])
        or results.get("commonCore", {}).get("tableDigest")
        != independent.get("commonCore", {}).get("tableDigest")
        or results.get("commonCore") != independent.get("commonCore")
    ):
        raise RuntimeError("R0.73V certificate exact 66-check/two-path audit drifted")

    producer = results.get("producer")
    if (
        results.get("arithmetic")
        != "fractions.Fraction Gaussian rationals and finite q-polynomials; no floating point"
        or not isinstance(producer, dict)
        or producer.get("standardLibraryOnly") is not True
        or producer.get("floatingPoint") != "not used"
        or producer.get("gpu") != "not used"
        or producer.get("network") != "not used"
        or producer.get("dgx") != "not used"
        or results.get("scope", {}).get("ordinaryTranslationPath")
        != "LOCAL_DIRECT_NO_DGX"
    ):
        raise RuntimeError("R0.73V certificate arithmetic/compute boundary drifted")
    boundary = manifest.get("claimBoundary")
    if not isinstance(boundary, str) or not all(token in boundary for token in (
        "Exact finite Fourier q-polynomials", "no information-theoretic minimality",
        "global regularity", "Clay conclusion",
    )):
        raise RuntimeError("R0.73V certificate claim boundary drifted")

    actual = {
        path.name for path in (ROOT / base).iterdir()
        if path.is_file() and not path.is_symlink()
    }
    if actual != inventory:
        raise RuntimeError("R0.73V certificate twelve-file inventory drifted")
    recorded = manifest.get("files")
    if not isinstance(recorded, list) or len(recorded) != 10:
        raise RuntimeError("R0.73V certificate manifest-bound inventory drifted")
    by_name = {
        row.get("path"): row for row in recorded
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    }
    if set(by_name) != inventory - {"manifest.json", "SHA256SUMS"}:
        raise RuntimeError("R0.73V certificate manifest file paths drifted")
    for name, row in by_name.items():
        payload = current_regular_bytes(f"{base}/{name}")
        if row.get("bytes") != len(payload) or row.get("sha256") != sha256(payload):
            raise RuntimeError("R0.73V certificate manifest is not byte-bound: " + name)
    source_rows = manifest.get("sourceBindings")
    commit_rows = manifest.get("sourceCommitBindings")
    if (
        not isinstance(source_rows, list)
        or {row.get("path") for row in source_rows if isinstance(row, dict)}
        != source_names
        or not isinstance(commit_rows, list)
        or {Path(str(row.get("path"))).name
            for row in commit_rows if isinstance(row, dict)}
        != source_names
    ):
        raise RuntimeError("R0.73V certificate eight-source inventory drifted")

    run_package_verifier(
        f"{base}/compute_exact_certificate.py", ["--check-only"],
        "R0.73V exact certificate producer",
    )
    run_package_verifier(
        f"{base}/independent_recompute.py", ["--check-only"],
        "R0.73V independent exact certificate producer",
    )
    run_package_verifier(
        f"{base}/seal_package.py",
        ["--source-commit", FINITE_SOURCE_COMMIT, "--check-only"],
        "R0.73V certificate provenance seal",
    )
    return manifest

def validate_figure_package(certificate_manifest: dict) -> dict:
    base = FIGURE_SOURCE_RELATIVE
    manifest = strict_json_file(f"{base}/manifest.json", "R0.73V figure manifest")
    config = strict_json_file(f"{base}/config.json", "R0.73V figure config")
    contract = strict_json_file(f"{base}/contract.json", "R0.73V figure contract")
    environment = strict_json_file(f"{base}/environment.json", "R0.73V figure environment")
    results = strict_json_file(f"{base}/results.json", "R0.73V figure results")
    validation = strict_json_file(f"{base}/validation.json", "R0.73V figure validation")
    require_exact_scope_figure_boundary(contract)

    seal = manifest.get("seal")
    git = manifest.get("git")
    qa = manifest.get("qa")
    if (
        manifest.get("schemaVersion") != "research-figure-manifest-v1"
        or manifest.get("figureSchemaVersion")
        != "r073v-signed-third-order-interface-manifest-v1"
        or manifest.get("figureId") != FIGURE_ID
        or manifest.get("release") != RELEASE
        or manifest.get("status") != "formal"
        or manifest.get("publicationStatus") != "staged"
        or not isinstance(seal, dict)
        or seal.get("artifactHashBound") is not True
        or seal.get("certificateCommitBound") is not True
        or seal.get("certificateCommonCoreByteIdentical") is not True
        or seal.get("figureSourceCommitAssigned") is not True
        or seal.get("requiresParentFigureSourceCommitFinalReseal") is not False
        or seal.get("figureSourceCommit") != FIGURE_SOURCE_COMMIT
        or seal.get("state") != "formal-figure-source-seal"
        or not isinstance(git, dict)
        or git.get("figureSourceCommit") != FIGURE_SOURCE_COMMIT
        or git.get("sourceCommit") != FIGURE_SOURCE_COMMIT
        or git.get("certificateSourceCommit") != FINITE_SOURCE_COMMIT
        or git.get("certificateCommit") != FINITE_PACKAGE_COMMIT
        or git.get("dirtyAtCertifiedRun") is not False
        or not isinstance(qa, dict)
        or qa.get("status") != "passed"
        or certificate_manifest.get("sourceCommit") != FINITE_SOURCE_COMMIT
    ):
        raise RuntimeError("R0.73V figure is not source-bound and QA-confirmed")

    if (
        config.get("schemaVersion")
        != "r073v-signed-third-order-interface-figure-config-v1"
        or config.get("figureId") != FIGURE_ID
        or config.get("widthMillimetres") != 178.0
        or config.get("heightMillimetres") != 118.0
        or config.get("pngDpi") != 600
        or contract.get("schemaVersion")
        != "r073v-signed-third-order-interface-figure-contract-v1"
        or contract.get("release") != RELEASE
        or contract.get("figureId") != FIGURE_ID
        or contract.get("certificate", {}).get("sourceCommit") != FINITE_SOURCE_COMMIT
        or contract.get("certificate", {}).get("packageCommit") != FINITE_PACKAGE_COMMIT
        or contract.get("compute", {}).get("dgxUsed") is not False
        or contract.get("compute", {}).get("ordinaryTranslationPath")
        != "LOCAL_DIRECT_NO_DGX"
    ):
        raise RuntimeError("R0.73V figure configuration/contract drifted")

    source_rows = current_regular_bytes(f"{base}/source-data.csv").decode("utf-8").splitlines()
    series = results.get("series")
    if (
        results.get("schemaVersion")
        != "r073v-signed-third-order-interface-figure-results-v1"
        or results.get("figureId") != FIGURE_ID
        or results.get("allSourceChecksPass") is not True
        or not isinstance(results.get("rowCount"), int)
        or results.get("rowCount") != len(source_rows) - 1
        or not isinstance(series, dict)
        or series.get("total") != results.get("rowCount")
        or sum(value for key, value in series.items()
               if key != "total" and isinstance(value, int))
        != results.get("rowCount")
    ):
        raise RuntimeError("R0.73V figure source-data/result accounting drifted")

    checks = validation.get("checks")
    required = validation.get("required")
    if (
        validation.get("schemaVersion")
        != "r073v-signed-third-order-interface-validation-v1"
        or validation.get("status") != "PASS"
        or validation.get("visualQaConfirmed") is not True
        or not isinstance(required, int)
        or required <= 0
        or validation.get("passed") != required
        or not isinstance(checks, list)
        or len(checks) != required
        or not all(isinstance(row, dict) and row.get("pass") is True for row in checks)
        or qa.get("validationChecks") != required
    ):
        raise RuntimeError("R0.73V figure validation provenance drifted")

    claim_boundary = contract.get("claimBoundary")
    if (
        not isinstance(claim_boundary, dict)
        or manifest.get("claimBoundary") != claim_boundary
        or results.get("claimBoundary") != claim_boundary
    ):
        raise RuntimeError("R0.73V figure claim boundary is absent or inconsistent")

    execution = environment.get("execution")
    if (
        not isinstance(execution, dict)
        or execution.get("dgxUsed") is not False
        or execution.get("gpu") != "not used"
        or execution.get("network") != "not used"
        or execution.get("ordinaryTranslationPath") != "LOCAL_DIRECT_NO_DGX"
    ):
        raise RuntimeError("R0.73V figure local-compute boundary drifted")
    progress_rows = strict_ndjson_file(
        f"{base}/progress.ndjson", "R0.73V figure progress log"
    )
    resource_rows = strict_ndjson_file(
        f"{base}/resource-log.ndjson", "R0.73V figure resource log"
    )
    if (
        len(progress_rows) != len(resource_rows)
        or not progress_rows
        or progress_rows[-1].get("stage") != "complete"
        or resource_rows[-1].get("stage") != "complete"
        or any(row.get("dgxUsed") is not False for row in resource_rows)
        or any(row.get("ordinaryTranslationPath") != "LOCAL_DIRECT_NO_DGX"
               for row in resource_rows)
    ):
        raise RuntimeError("R0.73V figure monitoring boundary drifted")

    package_names = {
        "README.md", "SHA256SUMS", "caption.md", "chart-contract-and-source-data.md",
        "command.txt", "config.json", "contract.json", "environment.json",
        "figure.pdf", "figure.png", "figure.svg", "manifest.json", "plot.py",
        "progress.ndjson", "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png",
        "qa-protocol.md", "qa-report.md", "requirements.txt", "resource-log.ndjson",
        "results.json", "source-data.csv", "validate.py", "validation.json",
    }
    actual = {
        path.name for path in (ROOT / base).iterdir()
        if path.is_file() and not path.is_symlink()
    }
    if actual != package_names:
        raise RuntimeError("R0.73V figure 25-file inventory drifted")
    sums = {}
    for line in current_regular_bytes(f"{base}/SHA256SUMS").decode("utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/]+)", line)
        if match is None or match.group(2) in sums:
            raise RuntimeError("R0.73V figure SHA256SUMS syntax/inventory drifted")
        sums[match.group(2)] = match.group(1)
    if set(sums) != package_names - {"SHA256SUMS"}:
        raise RuntimeError("R0.73V figure SHA256SUMS paths drifted")
    for name, digest in sums.items():
        if sha256(current_regular_bytes(f"{base}/{name}")) != digest:
            raise RuntimeError("R0.73V figure SHA256SUMS mismatch: " + name)

    source_bindings = seal.get("figureSourceBindings")
    if not isinstance(source_bindings, list) or len(source_bindings) != 21:
        raise RuntimeError("R0.73V figure source/raw commit bindings drifted")
    source_paths = tuple(
        str(row.get("path")) for row in source_bindings if isinstance(row, dict)
    )
    if len(source_paths) != 21 or any(
        not path.startswith(FIGURE_SOURCE_RELATIVE + "/") for path in source_paths
    ):
        raise RuntimeError("R0.73V figure source/raw binding paths drifted")
    verify_commit_paths(FIGURE_SOURCE_COMMIT, source_paths, "R0.73V figure source/raw")

    local_dependency_root = Path(
        "/Users/kasifa/.cache/codex-runtimes/r073s-figure-python"
    )
    local_executable = Path(
        "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
    )
    dependency_override = os.environ.get("R073V_FIGURE_DEPS")
    executable_override = os.environ.get("R073V_FIGURE_PYTHON")
    dependency_root = (
        Path(dependency_override) if dependency_override
        else local_dependency_root if local_dependency_root.is_dir()
        else None
    )
    executable = (
        Path(executable_override) if executable_override
        else local_executable if local_executable.is_file()
        else Path(sys.executable)
    )
    if not executable.is_file() or (
        dependency_root is not None and not dependency_root.is_dir()
    ):
        raise RuntimeError(
            "R0.73V figure verifier runtime missing; install requirements.txt or set "
            "R073V_FIGURE_DEPS and R073V_FIGURE_PYTHON"
        )
    verifier_arguments = ["--verify-only"]
    if dependency_root is not None:
        verifier_arguments = ["--deps", str(dependency_root), *verifier_arguments]
    run_package_verifier(
        f"{base}/validate.py", verifier_arguments, "R0.73V figure",
        executable=str(executable),
    )
    return manifest

def certificate_summary() -> dict[str, object]:
    root = ROOT / "research/certificates/r073v"
    manifest_path = root / "manifest.json"
    if not manifest_path.is_file() or manifest_path.is_symlink():
        return {"present": root.is_dir(), "finalSeal": False, "status": "missing-manifest"}
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {"present": True, "finalSeal": False, "status": "invalid-manifest"}
    final = (
        manifest.get("schemaVersion")
        == "r073v-signed-third-order-exact-manifest-v1"
        and manifest.get("release") == RELEASE
        and manifest.get("status") == "sealed"
        and manifest.get("finalSeal") is True
        and manifest.get("sourceCommitAssigned") is True
        and manifest.get("sourceCommit") == FINITE_SOURCE_COMMIT
        and manifest.get("allPrerequisiteChecksPass") is True
        and manifest.get("checkInventory") == {
            "exact": 66, "required": 66, "twoPathComparisons": 2,
        }
        and manifest.get("scopeFlags", {}).get("coefficientwiseNonRecoveryOnly")
        is True
    )
    return {
        "present": True,
        "finalSeal": final,
        "status": manifest.get("status", "incomplete"),
        "schemaVersion": manifest.get("schemaVersion"),
        "checks": manifest.get("checkInventory"),
        "sha256": sha256(manifest_path.read_bytes()),
    }


def figure_summary() -> dict[str, object]:
    root = ROOT / FIGURE_SOURCE_RELATIVE
    manifest_path = root / "manifest.json"
    validation_path = root / "validation.json"
    if (
        not manifest_path.is_file() or manifest_path.is_symlink()
        or not validation_path.is_file() or validation_path.is_symlink()
    ):
        return {"present": root.is_dir(), "formal": False, "status": "missing-metadata"}
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        validation = json.loads(validation_path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {"present": True, "formal": False, "status": "invalid-metadata"}
    seal = manifest.get("seal")
    required = validation.get("required")
    formal = (
        manifest.get("schemaVersion") == "research-figure-manifest-v1"
        and manifest.get("figureSchemaVersion")
        == "r073v-signed-third-order-interface-manifest-v1"
        and manifest.get("figureId") == FIGURE_ID
        and manifest.get("status") == "formal"
        and manifest.get("publicationStatus") == "staged"
        and isinstance(seal, dict)
        and seal.get("figureSourceCommitAssigned") is True
        and seal.get("requiresParentFigureSourceCommitFinalReseal") is False
        and seal.get("figureSourceCommit") == FIGURE_SOURCE_COMMIT
        and manifest.get("qa", {}).get("status") == "passed"
        and validation.get("schemaVersion")
        == "r073v-signed-third-order-interface-validation-v1"
        and validation.get("status") == "PASS"
        and isinstance(required, int) and required > 0
        and validation.get("passed") == required
        and isinstance(validation.get("checks"), list)
        and len(validation["checks"]) == required
    )
    return {
        "present": True,
        "formal": formal,
        "status": "source-bound-qa-passed" if formal else "prepublication-seal",
        "figureId": manifest.get("figureId"),
        "validationChecks": required,
        "sourceCommitAssigned":
            seal.get("figureSourceCommitAssigned") if isinstance(seal, dict) else False,
        "sha256": sha256(manifest_path.read_bytes()),
    }

def note_toc(content: ReleaseContent) -> str:
    rows = "".join(
        f'<li><a href="#{section.anchor}">{section.number:02d} · '
        f'{html.escape(section.title)}</a></li>' for section in content.sections
    )
    rows += '<li><a href="#release-boundary">B · exact boundary</a></li>'
    rows += '<li><a href="#figure">F · journal figure</a></li>'
    rows += '<li><a href="#reproduce">R · reproduction</a></li>'
    return f'<aside class="toc"><strong>CONTENTS</strong><ol>{rows}</ol></aside>'


def build_note(content: ReleaseContent) -> str:
    value = decode_baseline("public/notes/r0-73u.html")
    description = (
        "研究笔记 R0.73V：压力感知的有符号三阶 heat 提升、完整 Germano stress 界面、"
        "条件性临界通量行、精确 3→4 物理时间边界与有限系数证书。"
    )
    value = replace_regex(
        value, r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{description}">', "note description",
    )
    value = replace_regex(
        value, r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{html.escape(content.document_title_en, quote=True)}">',
        "note OG title",
    )
    value = replace_regex(
        value, r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{html.escape(content.lead_zh, quote=True)}">',
        "note OG description",
    )
    value = replace_regex(
        value, r'<meta property="og:image" content="[^"]*">',
        f'<meta property="og:image" content="https://kasifa.github.io/assets/r073v/{FIGURE_ID}.png">',
        "note OG image",
    )
    value = replace_regex(
        value, r'<title>.*?</title>',
        f'<title>{html.escape(content.document_title_en)}</title>', "note title",
    )
    value = replace_once(value, "/i18n-en.js?v=1.61", "/i18n-en.js?v=1.62", "note i18n")
    navigation = "".join(
        f'<a href="#{section.anchor}">{html.escape(section.title)}</a>'
        for section in content.sections
    )
    navigation += (
        '<a href="#figure">journal figure</a>'
        '<a href="#release-boundary">exact boundary</a>'
        '<a href="#reproduce">reproduction</a><a href="/">返回主页</a>'
    )
    value = replace_regex(
        value,
        r'(<header class="bar"><div class="bar-inner">\s*<a class="brand".*?</a>\s*)<nav>.*?</nav>',
        lambda match: match.group(1) + "<nav>" + navigation + "</nav>",
        "note navigation",
    )
    value = replace_regex(value, r'<header class="hero">.*?</header>', content.note_hero, "note hero")
    value = replace_regex(value, r'<aside class="toc">.*?</aside>', note_toc(content), "note TOC")
    value = replace_regex(value, r'<article>.*?</article>', content.note_article, "note article")
    value = replace_regex(
        value, r'<footer>.*?</footer>',
        '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>'
        '按原编号区分经典结果、本地严格结果、有限计算与开放问题。</div>'
        f'<div>研究笔记 R0.73V · {html.escape(content.date)}<br>'
        '<a href="/">返回研究主页</a></div></footer>',
        "note footer",
    )
    assert_public_html(value, "R0.73V note")
    if "/note-retro.css" not in value or value.count(FIGURE_ID) < 4:
        raise RuntimeError("R0.73V note lost retro stylesheet or formal figure links")
    return value


def build_recap(content: ReleaseContent) -> str:
    value = decode_baseline("public/recap-r0-61-r0-73u.html")
    value = value.replace("/i18n-en.js?v=1.61", "/i18n-en.js?v=1.62")
    value = value.replace("R0.61–R0.73U", "R0.61–R0.73V")
    value = value.replace(
        "R0.61–R0.73V · 2026-08-31",
        f"R0.61–R0.73V · {content.date}",
    )
    value = value.replace(
        "R0.61–R0.73V 回顾 · 2026-08-31",
        f"R0.61–R0.73V 回顾 · {content.date}",
    )
    value = value.replace("R0.61 到 R0.73U", "R0.61 到 R0.73V")
    value = value.replace("R0.69P–R0.73U", "R0.69P–R0.73V")
    value = value.replace("R0.70A–R0.73U", "R0.70A–R0.73V")
    value = value.replace("回顾截止节点：R0.73U", "回顾截止节点：R0.73V")
    value = value.replace("收录节点：137", "收录节点：138")
    value = value.replace("回顾截止时公开笔记：197", "回顾截止时公开笔记：198")
    value = value.replace("137 节", "138 节").replace("137 个节点", "138 个节点")
    value = value.replace("99 个版本", "100 个版本").replace("99 节", "100 节")
    value = value.replace("75 个满足", "76 个满足").replace("75 节", "76 节")
    value = value.replace("56 个阶段", "57 个阶段")
    value = value.replace("56 个研究阶段", "57 个研究阶段")
    value = value.replace("<strong>137</strong>", "<strong>138</strong>")
    value = value.replace("<strong>99</strong>", "<strong>100</strong>")
    value = value.replace("<strong>75</strong>", "<strong>76</strong>")
    value, duplicate_phase_count = re.subn(
        r'(<article class="phase"><h3>)(R0\.73[N-T]) · \2 \| ',
        r"\1\2 | ",
        value,
    )
    if duplicate_phase_count != 0:
        raise RuntimeError(
            "R0.73V recap unexpectedly retained duplicated phase titles: "
            + str(duplicate_phase_count)
        )
    value = replace_regex(
        value, r'(<header class="hero">.*?<p class="lead">)(.*?)(</p>)',
        lambda match: match.group(1) + match.group(2) + " "
        + html.escape(content.recap_zh) + match.group(3),
        "recap hero current result",
    )
    value = replace_regex(
        value, r'<meta name="description" content="[^"]*">',
        '<meta name="description" content="R0.60 之后的完整研究回顾：R0.61 到 '
        'R0.73V 共 138 个节点；最新一节分开有符号三阶尺度生成、完整压力账本、'
        '条件临界行与 3→4 物理时间边界。">',
        "recap description",
    )
    value = replace_regex(
        value, r'<meta property="og:description" content="[^"]*">',
        '<meta property="og:description" content="57 个阶段、138 个节点：从约化递推和环带排除'
        '到压力感知的有符号三阶 heat 提升与精确下一层余项。">',
        "recap OG description",
    )
    value = replace_once(
        value,
        '          </div>\n        </section>\n\n        <section id="node-index"',
        content.recap_phase
        + '\n          </div>\n        </section>\n\n        <section id="node-index"',
        "recap phase append",
    )
    node = (
        '<span class="node-ref"><a href="/notes/r0-73v.html">R0.73V</a>'
        '<span class="node-state kind-closed">闭</span></span>'
    )
    value = replace_once(
        value,
        '          </div>\n        </section>\n\n        <section id="retained"',
        f'            {node}\n          </div>\n        </section>\n\n        <section id="retained"',
        "recap node append",
    )
    retained = (
        '<li>R0.73V 以 <code>χ_s</code> 精确填入二次张量方程的有符号三次槽，并以 '
        '<code>κ_s,Q_s,R_s</code> 展开完整压力感知 stress 界面。临界 <code>κ,Q</code> 行'
        '已经假设 <code>L_t^4L_x^6</code>；压力–应变导数行仍开放。有限证书只给出'
        '选定系数的不可吸收和一个非零四次下一层余项。'
        f'{html.escape(EXACT_SCOPE_BOUNDARY_ZH)} NOT CLAY。</li>'
    )
    value = replace_once(
        value,
        '          </ul>\n          <p>这些结果可以分别整理成条件定理、精确恒等式、反例或计算辅助分析。',
        f'            {retained}\n          </ul>\n'
        '          <p>这些结果可以分别整理成条件定理、精确恒等式、反例或计算辅助分析。',
        "recap retained result append",
    )
    value = replace_regex(
        value, r'<section id="value">.*?</section>',
        '<section id="value"><div class="section-no">04 / 目前的判断</div>'
        '<h2>压力恢复、临界预算与带符号信息障碍已经分开</h2>'
        f'<p>{html.escape(content.recap_zh)}</p>'
        '<p>不能把 138 个节点或 100 个公开版本解释成 Clay 完成比例。'
        '有符号三阶尺度生成律成立；但压力–应变临界控制、物理时间闭合与任意数据正则性保持开放。'
        '任意三维初值全局正则性仍为 OPEN。</p></section>',
        "recap current value",
    )
    value = replace_regex(
        value, r'<section id="next">.*?</section>',
        '<section id="next"><div class="section-no">05 / 下一步</div>'
        f'<h2>{html.escape(content.next_release)}：沿精确下一层边界继续</h2>'
        f'<p>{html.escape(content.next_gate_zh)}</p></section>',
        "recap next gate",
    )
    value = replace_regex(
        value, r'<section id="claims">.*?</section>',
        '<section id="claims"><div class="section-no">06 / 说明边界</div>'
        '<h2>经典结果、本地有限结论和开放问题分开列示</h2>'
        '<p>R0.70A–R0.73V 的 100 节已公开；76 节完整封存；24 节旧档待回补。</p>'
        f'<p>{html.escape(CLOSED_LEDGER)}</p>'
        f'<p>{html.escape(FINITE_LEDGER)}</p>'
        f'<p>{html.escape(OPEN_LEDGER)}</p>'
        '<p>R0.73V 的有限公式证书和正式附图只复算精确稀疏 Fourier 恒等式与见证族；'
        '它们不积分一般非线性解，不运行 Navier--Stokes 仿真。'
        f'{html.escape(EXACT_SCOPE_BOUNDARY_ZH)} NOT CLAY。</p>'
        '</section>',
        "recap exact boundary",
    )
    value = replace_regex(
        value, r'<section id="reproduce">.*?</section>',
        '<section id="reproduce"><div class="section-no">07 / 原始资料</div>'
        '<h2>逐节笔记、证明、审计、证书、附图和历史回顾</h2>'
        '<p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · '
        '<a href="/recap-r0-61-r0-73u.html">保留 R0.73U 历史回顾</a> · '
        '<a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · '
        '<a href="/notes/r0-73v.html">打开最新节点 R0.73V</a></p>'
        '<p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073v_report-source.md">查看 canonical report</a> · '
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073v_signed_third_order_heat_lift.md">查看解析证明</a> · '
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073v_primary_literature_audit.md">查看一手文献审计</a> · '
        '<a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073v">查看有限证书</a> · '
        f'<a href="/assets/r073v/{FIGURE_ID}.pdf">下载期刊附图</a> · '
        '<a href="/recap-r0-61-r0-73v.pdf">下载同步 PDF</a></p>'
        '<p>经典结论由一手来源承担；本地解析证明承担精确恒等式和条件推论；有限证书只作可复现系数核验。'
        'NOT CLAY。</p></section>',
        "recap reproduction",
    )
    value = value.replace("/recap-r0-61-r0-73u.pdf", "/recap-r0-61-r0-73v.pdf")
    value = value.replace("R0.73U 回顾", "R0.73V 回顾")
    for stale in ("<strong>137</strong>", "<strong>99</strong>", "<strong>75</strong>"):
        if stale in value:
            raise RuntimeError("R0.73V recap retained stale metric " + stale)
    if value.count('<article class="phase">') != 57:
        raise RuntimeError("R0.73V recap must contain exactly 57 phase articles")
    if "56 个阶段" in value or "56 个研究阶段" in value:
        raise RuntimeError("R0.73V recap retained a stale displayed phase count")
    assert_public_html(value, "R0.73V recap")
    return value


def latest_spotlight(content: ReleaseContent) -> str:
    return (
        '<section class="route-overview latest-release-spotlight" id="latest-release" '
        'aria-labelledby="latest-release-title"><div class="route-overview-inner">'
        '<header class="route-map-header"><div>'
        f'<p class="eyebrow">LATEST RELEASE · R0.73V · {html.escape(content.date)}</p>'
        f'<h2 class="route-map-title" id="latest-release-title">{html.escape(content.public_title_zh)}</h2>'
        f'<p class="route-map-intro">{html.escape(content.home_zh)}</p></div>'
        '<nav class="route-map-actions" aria-label="最新发布快捷入口">'
        '<a class="route-map-latest" href="/notes/r0-73v.pdf">阅读最新 R0.73V 研究笔记 →</a>'
        '<a href="/recap-r0-61-r0-73v.html">138 节累计回顾</a>'
        '<a href="/notes/">198 篇研究笔记总索引</a>'
        '<a href="#r073v">查看首页完整 R0.73V 卡片</a></nav></header>'
        '<div class="route-legend" aria-label="最新发布计数">'
        '<span><i class="route-legend-mark kept" aria-hidden="true"></i>'
        'R0.70A–R0.73V · 100 节已公开</span>'
        '<span><i class="route-legend-mark kept" aria-hidden="true"></i>76 节完整封存</span>'
        '<span><i class="route-legend-mark current" aria-hidden="true"></i>'
        '当前端点 R0.73V</span></div></div></section>'
    )


def update_home(content: ReleaseContent) -> str:
    value = decode_baseline("public/research-review.html")
    value = value.replace('data-site-version="1.61"', 'data-site-version="1.62"')
    value = value.replace("/i18n-en.js?v=1.61", "/i18n-en.js?v=1.62")
    value = value.replace("/site-refresh.js?v=1.61", "/site-refresh.js?v=1.62")
    value = replace_regex(
        value, r'<section class="route-overview latest-release-spotlight".*?</section>',
        latest_spotlight(content), "home latest spotlight",
    )
    marker = '<div class="task-one" id="r073u" data-release="r073u"'
    value = replace_once(value, marker, content.home_card + "\n          " + marker, "home card insert")
    value = value.replace("<strong>197</strong>公开研究笔记", "<strong>198</strong>公开研究笔记")
    value = value.replace("<strong>v1.61</strong>网页版本", "<strong>v1.62</strong>网页版本")
    value = value.replace("<strong>R0.73U</strong>最新研究节点", "<strong>R0.73V</strong>最新研究节点")
    value = replace_regex(
        value, r'<strong>[^<]+</strong>当前方向',
        '<strong>pressure-aware signed third-order heat lift</strong>当前方向',
        "home current direction",
    )
    value = value.replace("NEXT · R0.73V", "NEXT · R0.73W")
    value = replace_regex(
        value, r'<h3>R0\.73V 下一接口</h3><p>.*?</p>',
        f'<h3>{html.escape(content.next_release)} 下一接口</h3>'
        f'<p>{html.escape(content.next_gate_zh)}</p>',
        "home next interface",
    )
    value = value.replace(
        "R0.70A–R0.73U：99 节已公开，75 节完整封存",
        "R0.70A–R0.73V：100 节已公开，76 节完整封存",
    )
    value = value.replace("Research topology · R0.1–R0.73U", "Research topology · R0.1–R0.73V")
    value = value.replace(
        '<a class="route-map-latest" href="#r073u">跳到首页 R0.73U 卡片 →</a>',
        '<a class="route-map-latest" href="#r073v">跳到首页 R0.73V 卡片 →</a>',
    )
    value = value.replace(
        '/recap-r0-61-r0-73u.html">阅读 R0.60 之后的累计回顾',
        '/recap-r0-61-r0-73v.html">阅读 R0.60 之后的累计回顾',
    )
    value = value.replace("/recap-r0-61-r0-73u.html", "/recap-r0-61-r0-73v.html")
    value = value.replace("/recap-r0-61-r0-73u.pdf", "/recap-r0-61-r0-73v.pdf")
    value = value.replace("综述 v1.61 ·", "综述 v1.62 ·")
    value = value.replace(
        "<strong>2026-08-31</strong>最近修订",
        f"<strong>{html.escape(content.date)}</strong>最近修订",
    )
    value = value.replace(
        "综述 v1.62 · 2026-09-01",
        f"综述 v1.62 · {html.escape(content.date)}",
    )
    value = value.replace(
        '<span class="route-range">R0.69P–R0.73U</span>',
        '<span class="route-range">R0.69P–R0.73V</span>',
    )
    value = replace_regex(
        value, r"R0\.73U：[^<。]+已分列",
        "R0.73V：有符号三阶尺度生成、完整压力账本与精确 3→4 边界已分列",
        "home route summary",
    )
    value = value.replace('<span>R0.72R–R0.73U：</span>', '<span>R0.72R–R0.73V：</span>')
    value = replace_regex(
        value, r"(→ shellwise phase certificate → [^<]+)</p>",
        lambda match: match.group(1) + " → pressure-aware signed third-order heat lift</p>",
        "home route tail",
    )
    current_paragraph = (
        f'<p>{html.escape(content.recap_zh)} '
        '<span>signed cross-covariance scale PDE</span>；'
        '<span>pressure-aware Germano interface</span>；'
        '<span>selected quartic next-level remainder</span>。物理时间闭合仍开放。</p>'
    )
    value = replace_once(
        value, '              <details class="tree-notes" open>',
        "              " + current_paragraph + '\n              <details class="tree-notes" open>',
        "home route current paragraph",
    )
    value = value.replace('<summary>展开 107 篇公开笔记</summary>', '<summary>展开 108 篇公开笔记</summary>')
    value = value.replace('aria-label="R0.69P–R0.73U"', 'aria-label="R0.69P–R0.73V"')
    value = replace_once(
        value,
        '                  <a class="milestone" href="/notes/r0-73u.html">R0.73U</a>',
        '                  <a class="milestone" href="/notes/r0-73u.html">R0.73U</a>\n'
        '                  <a class="milestone" href="/notes/r0-73v.html">R0.73V</a>',
        "home route R0.73V link",
    )
    value = replace_regex(
        value, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>'
        + html.escape(content.recap_zh) + " 下一关是 " + html.escape(content.next_release)
        + "：" + html.escape(content.next_gate_zh) + "</span></div>",
        "home focus summary",
    )
    recap_card = (
        '<div class="task-one" id="post-r060-recap" style="margin-top:2rem">'
        '<p class="eyebrow">累计回顾 R0.61–R0.73V · 2026-09-01</p>'
        '<h3>R0.60 recap 之后的累计回顾收录 138 个节点；全站现有 198 篇公开研究笔记</h3>'
        '<p>累计回顾现分 57 个阶段，完整保留 R0.61–R0.73V；最新节点分开记录有符号三阶'
        'heat 提升、完整压力账本、条件临界行、精确 3→4 边界和有限系数证书。</p>'
        '<p>R0.70A–R0.73V 共 100 个版本已公开；76 个按当前 formal-figure 合同完整封存，'
        '24 个旧版附图档案仍列入回补清单。</p>'
        f'<p><strong>阶段判断：</strong>&nbsp;{html.escape(content.recap_zh)} '
        '任意三维初值全局正则性与 Clay 保持 OPEN。</p>'
        '<p><a href="/recap-r0-61-r0-73v.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · '
        '<a href="/recap-r0-61-r0-73v.pdf">下载同步 PDF</a></p></div>'
    )
    value = replace_regex(
        value, r'<div class="task-one" id="post-r060-recap".*?</div>',
        recap_card, "home cumulative recap card",
    )
    value = value.replace(
        "本站 R0.69P–R0.73U 路线放在同一张图中",
        "本站 R0.69P–R0.73V 路线放在同一张图中",
    )
    for stale in (
        "Research topology · R0.1–R0.73U",
        "累计回顾收录 137 个节点；全站现有 197 篇公开研究笔记",
        '<summary>展开 107 篇公开笔记</summary>',
        "<strong>v1.61</strong>网页版本",
        "<strong>R0.73U</strong>最新研究节点",
        'data-site-version="1.61"',
        "/site-refresh.js?v=1.61",
        '<h3>R0.73V 下一接口</h3>',
    ):
        if stale in value:
            raise RuntimeError("R0.73V home retained stale latest marker " + stale)
    assert_public_html(value, "R0.73V home")
    return value


def update_literature(content: ReleaseContent) -> str:
    value = decode_baseline("public/literature-review.html")
    value = value.replace("/i18n-en.js?v=1.61", "/i18n-en.js?v=1.62")
    value = value.replace("文献综述 v1.61 ·", "文献综述 v1.62 ·")
    value = value.replace(
        "文献综述 v1.62 · 2026-09-01",
        f"文献综述 v1.62 · {html.escape(content.date)}",
    )
    marker = '<span class="route-r073u-deck-update">'
    start = value.find(marker)
    end = value.find("</span>", start)
    if start < 0 or end < 0:
        raise RuntimeError("literature R0.73U deck marker missing")
    end += len("</span>")
    value = value[:end] + content.literature_update + value[end:]
    value = value.replace("/recap-r0-61-r0-73u.html", "/recap-r0-61-r0-73v.html")
    value = value.replace("137 节", "138 节")
    value = value.replace("R0.69P–R0.73U", "R0.69P–R0.73V")
    route_step = (
        '<div class="route-step kept"><header><b>R0.73V</b>'
        '<strong>pressure-aware signed third-order heat lift</strong></header>'
        f'<p><strong>{html.escape(content.public_title_zh)}</strong></p>'
        '<p>R0.70A–R0.73V：100 节已公开，76 节完整封存。</p>'
        f'<p>{html.escape(content.recap_zh)} <a href="/notes/r0-73v.html">研究笔记</a> '
        '<a href="/recap-r0-61-r0-73v.html">当前累计回顾</a> '
        '<a href="#r073v-boundary">文献边界</a></p></div>'
        '<div class="route-step pause"><header><b>开放接口 · R0.73W</b>'
        '<strong>quantitative control at the exact next-level boundary</strong></header>'
        f'<p>{html.escape(content.next_gate_zh)} 任意初值全局正则性与 Clay 保持 OPEN。</p></div>'
    )
    value = replace_regex(
        value,
        r'<div class="route-step pause"><header><b>开放接口 · R0\.73V</b>.*?</div>',
        route_step, "literature current route step",
    )
    literature_boundary = (
        '<h3 id="r073v-boundary">R0.73V 的精确 filtered-moment 层级与压力感知三阶界面</h3>'
        '<p><a href="https://doi.org/10.1098/rspa.1938.0013">von Kármán--Howarth 1938</a> 与 '
        '<a href="https://doi.org/10.1017/S0022112001003949">Hill 2001</a> 承担经典两点层级；'
        '<a href="https://doi.org/10.1017/S0022112092001733">Germano 1992</a> 承担 filtering 与层间 stress identity。'
        'Germano 的完整二阶 stress 方程明确包含速度三阶、压力–速度、压力–应变和梯度协方差。'
        '<a href="https://doi.org/10.1070/IM1993v041n03ABEH002274">Fursikov 1993</a> 提供严格统计矩层级语境。'
        '这些对象和假设与本站的确定性局部 heat 状态不同。限定式检索未找到当前第三 heat-cumulant PDE 或'
        '有限局部 heat-moment 状态的普遍最小性/no-go 定理；未检出不是新颖性、优先权或不存在证明。</p>'
        '<div class="boundary"><strong>R0.73V 的主张边界</strong>'
        f'<p>{html.escape(CLOSED_LEDGER)}</p>'
        f'<p>{html.escape(FINITE_LEDGER)}</p>'
        f'<p>{html.escape(OPEN_LEDGER)}</p>'
        '<p>一手来源承担经典层级；本地解析证明承担精确尺度恒等式与条件推论；'
        '有限包只复算选定 Fourier 系数和下一层余项，不认证连续 PDE。'
        f'{html.escape(EXACT_SCOPE_BOUNDARY_ZH)} NOT CLAY。</p></div>'
    )
    value = replace_once(
        value, '          <ol class="criteria">',
        "          " + literature_boundary + '\n          <ol class="criteria">',
        "literature R0.73V boundary",
    )
    if (
        "开放接口 · R0.73W" not in value
        or "开放接口 · R0.73V" in value
        or 'id="r073v-boundary"' not in value
    ):
        raise RuntimeError("R0.73V literature route/boundary was not advanced")
    assert_public_html(value, "R0.73V literature")
    for token in ("VERIFIED_CLASSICAL", "INTERNAL_EXACT", "优先权"):
        if token not in value:
            raise RuntimeError("R0.73V literature lost boundary token " + token)
    return value


def build_manifest_outputs(content: ReleaseContent) -> dict[Path, bytes]:
    release = strict_json_bytes(
        git_bytes(RELEASE_BASELINE_COMMIT, "research/release-manifest.json"),
        "release manifest",
    )
    if release.get("schemaVersion") != "research-release-manifest-v1":
        raise RuntimeError("R0.73U release-manifest schema drift")
    for key, expected in R073U_BASELINE.items():
        if release.get(key) != expected:
            raise RuntimeError("R0.73U release-manifest baseline drift: " + key)

    version_parts = str(release["siteVersion"]).split(".")
    if len(version_parts) != 2 or not all(part.isdigit() for part in version_parts):
        raise RuntimeError("R0.73U site version is not a two-part decimal")
    derived_version = f"{version_parts[0]}.{int(version_parts[1]) + 1:02d}"
    derived_target = {
        "latestCompletedRelease": "r073v",
        "siteVersion": derived_version,
        "publicHtmlNoteCount": int(release["publicHtmlNoteCount"]) + 1,
        "postR060RecapNodeCount": int(release["postR060RecapNodeCount"]) + 1,
        "nextRelease": "r073w",
        "postR070APublishedReleaseCount":
            int(release["postR070APublishedReleaseCount"]) + 1,
        "postR070AFormalSealedReleaseCount":
            int(release["postR070AFormalSealedReleaseCount"]) + 1,
        "legacyFormalFigureBacklogCount":
            int(release["legacyFormalFigureBacklogCount"]),
    }
    if derived_version != SITE_VERSION or derived_target != R073V_TARGET:
        raise RuntimeError("R0.73V accounting target is not the derived one-step successor")
    release.update({
        **derived_target,
        "latestReleaseGate":
            "tests/r073v-signed-third-order-interface-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r073v-release.test.mjs",
    })

    site = strict_json_bytes(
        git_bytes(RELEASE_BASELINE_COMMIT, "public/site-version.json"), "site version"
    )
    if (
        site.get("schemaVersion") != "research-site-version-v1"
        or site.get("version") != R073U_BASELINE["siteVersion"]
        or site.get("latestRelease") != "R0.73U"
        or site.get("publicHtmlNoteCount")
        != R073U_BASELINE["publicHtmlNoteCount"]
    ):
        raise RuntimeError("R0.73U site-version baseline drift")
    site.update({
        "version": derived_version,
        "latestRelease": RELEASE,
        "publicHtmlNoteCount": derived_target["publicHtmlNoteCount"],
        "publishedDate": content.date,
    })

    inventory = strict_json_bytes(
        git_bytes(RELEASE_BASELINE_COMMIT, "research/formal-archive-inventory.json"),
        "formal archive inventory",
    )
    if inventory.get("schemaVersion") != "formal-archive-inventory-v1":
        raise RuntimeError("R0.73U formal-archive schema drift")
    published = inventory.get("publishedReleases")
    sealed = inventory.get("formalSealedReleases")
    if (
        not isinstance(published, list)
        or not isinstance(sealed, list)
        or len(published) != inventory.get("publishedReleaseCount")
        or len(sealed) != inventory.get("formalSealedReleaseCount")
        or published[-1:] != ["r073u"]
        or sealed[-1:] != ["r073u"]
        or "r073v" in published
        or "r073v" in sealed
        or inventory.get("latestPublishedRelease") != "r073u"
        or inventory.get("legacyFormalFigureBacklogCount")
        != R073U_BASELINE["legacyFormalFigureBacklogCount"]
    ):
        raise RuntimeError("R0.73U formal archive is not an exact append-only baseline")
    published.append("r073v")
    sealed.append("r073v")
    inventory.update({
        "latestPublishedRelease": "r073v",
        "publishedReleaseCount": len(published),
        "formalSealedReleaseCount": len(sealed),
        "legacyFormalFigureBacklogCount":
            R073U_BASELINE["legacyFormalFigureBacklogCount"],
    })
    if (
        inventory["publishedReleaseCount"]
        != derived_target["postR070APublishedReleaseCount"]
        or inventory["formalSealedReleaseCount"]
        != derived_target["postR070AFormalSealedReleaseCount"]
    ):
        raise RuntimeError("R0.73V manifest and archive derived counts disagree")

    inventory_payload = json_bytes(inventory)
    release["formalArchiveInventory"] = {
        "path": "research/formal-archive-inventory.json",
        "sha256": sha256(inventory_payload),
    }
    return {
        ROOT / "research/release-manifest.json": json_bytes(release),
        ROOT / "research/formal-archive-inventory.json": inventory_payload,
        PUBLIC / "site-version.json": json_bytes(site),
        ROOT / "VERSION": (derived_version + "\n").encode("ascii"),
    }

def build_note_index(content: ReleaseContent, site_payload: bytes) -> str:
    import generate_note_index as note_index

    target_site = json.loads(site_payload.decode("utf-8"))
    old_json = note_index.json
    old_recap = note_index.latest_recap_href
    old_paths = note_index.ROOT, note_index.PUBLIC, note_index.NOTES, note_index.OUTPUT

    class TargetJson:
        @staticmethod
        def loads(_value: str) -> dict:
            return target_site

    try:
        with tempfile.TemporaryDirectory(prefix="r073v-index-") as temporary:
            notes = Path(temporary)
            for relative in git_paths(RELEASE_BASELINE_COMMIT, "public/notes"):
                name = Path(relative).name
                if re.fullmatch(r"r0-[0-9a-z]+\.(?:html|pdf)", name):
                    (notes / name).write_bytes(git_bytes(RELEASE_BASELINE_COMMIT, relative))
            note_index.ROOT, note_index.PUBLIC, note_index.NOTES = ROOT, PUBLIC, notes
            note_index.OUTPUT = notes / "index.html"
            existing = [note_index.parse_note(path) for path in note_index.note_files()]
            if len(existing) != R073U_BASELINE["publicHtmlNoteCount"] or existing[0].slug != "r0-73u":
                raise RuntimeError("R0.73V note-index baseline is not exact")
            latest = note_index.Note(
                slug="r0-73v",
                code=RELEASE,
                title=content.document_title_en.split("｜", 1)[-1].strip(),
                major=73,
                has_pdf=True,
            )
            note_index.json = TargetJson
            note_index.latest_recap_href = lambda: "/recap-r0-61-r0-73v.html"
            value = note_index.render([latest, *existing])
    finally:
        note_index.json = old_json
        note_index.latest_recap_href = old_recap
        note_index.ROOT, note_index.PUBLIC, note_index.NOTES, note_index.OUTPUT = old_paths
    assert_public_html(value, "R0.73V note index", require_boundary=False)
    if "prefers-color-scheme: dark" not in value:
        raise RuntimeError("R0.73V index lost automatic dark theme")
    return value


def formal_figure_payloads(source: Path) -> dict[str, bytes]:
    source_manifest = strict_json_file(
        f"{FIGURE_SOURCE_RELATIVE}/manifest.json", "R0.73V sealed figure manifest"
    )
    seal = source_manifest.get("seal")
    if (
        source_manifest.get("schemaVersion") != "research-figure-manifest-v1"
        or source_manifest.get("figureSchemaVersion")
        != "r073v-signed-third-order-interface-manifest-v1"
        or source_manifest.get("figureId") != FIGURE_ID
        or source_manifest.get("publicationStatus") != "staged"
        or source_manifest.get("status") != "formal"
        or not isinstance(seal, dict)
        or seal.get("figureSourceCommitAssigned") is not True
        or seal.get("figureSourceCommit") != FIGURE_SOURCE_COMMIT
        or seal.get("requiresParentFigureSourceCommitFinalReseal") is not False
        or source_manifest.get("qa", {}).get("status") != "passed"
    ):
        raise RuntimeError("R0.73V source figure is not a source-bound sealed package")

    actual = sorted(
        path.name for path in source.iterdir()
        if path.is_file() and not path.is_symlink()
    )
    if len(actual) != 25 or "manifest.json" not in actual or "SHA256SUMS" not in actual:
        raise RuntimeError("R0.73V formal figure inventory is incomplete or unsealed")

    outputs = []
    for suffix in ("pdf", "svg", "png"):
        name = f"figure.{suffix}"
        payload = current_regular_bytes(f"{FIGURE_SOURCE_RELATIVE}/{name}")
        row: dict[str, object] = {
            "path": name, "bytes": len(payload), "sha256": sha256(payload),
        }
        if suffix == "png":
            row["dpi"] = 600
        outputs.append(row)
    public_assets = [
        {
            "path": f"public/assets/r073v/{FIGURE_ID}.{suffix}",
            "bytes": row["bytes"],
            "sha256": row["sha256"],
        }
        for suffix, row in zip(("pdf", "svg", "png"), outputs)
    ]

    published = json.loads(json.dumps(source_manifest))
    published["publicationStatus"] = "published"
    published["publication"] = {
        "archiveDirectory": f"public/{FIGURE_ARCHIVE_RELATIVE}",
        "researchArchiveDirectory": f"research/{FIGURE_ARCHIVE_RELATIVE}",
        "directory": "public/assets/r073v",
        "fileStem": FIGURE_ID,
        "byteIdentityRequired": True,
        "publicCopiesComplete": True,
        "assets": public_assets,
        "releaseSourceCommit": RELEASE_SOURCE_COMMIT,
        "figureSourceCommit": FIGURE_SOURCE_COMMIT,
        "figurePackageCommit": FIGURE_PACKAGE_COMMIT,
    }
    published["sourcePublicationStatus"] = source_manifest["publicationStatus"]

    payloads = {
        name: (json_bytes(published) if name == "manifest.json"
               else current_regular_bytes(f"{FIGURE_SOURCE_RELATIVE}/{name}"))
        for name in actual if name != "SHA256SUMS"
    }
    payloads["SHA256SUMS"] = "".join(
        f"{sha256(payloads[name])}  {name}\n" for name in sorted(payloads)
    ).encode("utf-8")
    if sorted(payloads) != actual or len(payloads["SHA256SUMS"].splitlines()) != 24:
        raise RuntimeError("R0.73V formal figure staging changed the package inventory")
    return payloads

def stage_figure_assets(staged: dict[Path, bytes]) -> None:
    source = ROOT / FIGURE_SOURCE_RELATIVE
    if not source.is_dir() or source.is_symlink() or not (source / "manifest.json").is_file():
        raise RuntimeError("R0.73V formal figure package is incomplete")
    payloads = formal_figure_payloads(source)
    for name, payload in payloads.items():
        staged[ROOT / "research" / FIGURE_ARCHIVE_RELATIVE / name] = payload
        staged[PUBLIC / FIGURE_ARCHIVE_RELATIVE / name] = payload
    for suffix in ("pdf", "svg", "png"):
        staged[PUBLIC / f"assets/r073v/{FIGURE_ID}.{suffix}"] = payloads[f"figure.{suffix}"]


def build_staged(content: ReleaseContent) -> dict[Path, bytes]:
    staged: dict[Path, bytes] = {}
    stage_figure_assets(staged)
    staged[PUBLIC / "notes/r0-73v.html"] = build_note(content).encode("utf-8")
    staged[PUBLIC / "recap-r0-61-r0-73v.html"] = build_recap(content).encode("utf-8")
    staged[PUBLIC / "research-review.html"] = update_home(content).encode("utf-8")
    staged[PUBLIC / "literature-review.html"] = update_literature(content).encode("utf-8")
    staged[PUBLIC / "research/r073v/r073v_figure_source_audit.md"] = current_regular_bytes(
        "research/r073v_figure_source_audit.md"
    )
    staged[PUBLIC / "research/r073v/r073v_figure_source_reaudit.md"] = current_regular_bytes(
        "research/r073v_figure_source_reaudit.md"
    )
    staged.update(build_manifest_outputs(content))
    staged[PUBLIC / "notes/index.html"] = build_note_index(
        content, staged[PUBLIC / "site-version.json"]
    ).encode("utf-8")
    missing = [relative for relative in CORE_TARGET_OUTPUTS if ROOT / relative not in staged]
    if missing:
        raise RuntimeError("R0.73V staged transaction omitted: " + repr(missing))
    for path, payload in staged.items():
        if path.suffix == ".html":
            assert_public_html(
                payload.decode("utf-8"), path.name,
                require_boundary=path != PUBLIC / "notes/index.html",
            )
    return staged


def _lstat(path: Path) -> os.stat_result | None:
    try:
        return path.lstat()
    except FileNotFoundError:
        return None


def _assert_safe_directory_chain(
    parent: Path, *, created_directories: list[Path] | None = None,
) -> None:
    try:
        relative = parent.relative_to(ROOT)
    except ValueError as exc:
        raise RuntimeError("transaction parent escaped repository") from exc
    if any(part in ("", ".", "..") for part in relative.parts):
        raise RuntimeError("unsafe transaction parent traversal: " + str(parent))

    root_status = _lstat(ROOT)
    if root_status is None or stat.S_ISLNK(root_status.st_mode) or not stat.S_ISDIR(root_status.st_mode):
        raise RuntimeError("unsafe transaction root: " + str(ROOT))

    cursor = ROOT
    for part in relative.parts:
        cursor = cursor / part
        status = _lstat(cursor)
        if status is None:
            if created_directories is None:
                raise RuntimeError("missing transaction parent: " + str(cursor))
            created = False
            try:
                cursor.mkdir()
                created = True
            except FileExistsError:
                pass
            status = _lstat(cursor)
            if created:
                created_directories.append(cursor)
        if status is None or stat.S_ISLNK(status.st_mode) or not stat.S_ISDIR(status.st_mode):
            raise RuntimeError("unsafe transaction ancestor: " + str(cursor))


def _assert_safe_transaction_target(path: Path) -> None:
    try:
        relative = path.relative_to(ROOT)
    except ValueError as exc:
        raise RuntimeError("transaction target escaped repository") from exc
    if not relative.parts or any(part in ("", ".", "..") for part in relative.parts):
        raise RuntimeError("unsafe transaction target traversal: " + str(path))
    status = _lstat(path)
    if status is not None and (stat.S_ISLNK(status.st_mode) or not stat.S_ISREG(status.st_mode)):
        raise RuntimeError("unsafe transaction target: " + str(path))


def commit_transaction(staged: dict[Path, bytes]) -> None:
    ordered = sorted(staged)
    created_directories: list[Path] = []
    for path in ordered:
        _assert_safe_transaction_target(path)
        _assert_safe_directory_chain(path.parent, created_directories=created_directories)

    nonce = f"{os.getpid()}-{os.urandom(8).hex()}"
    rows: list[dict[str, object]] = []
    try:
        for index, target in enumerate(ordered):
            _assert_safe_directory_chain(target.parent)
            _assert_safe_transaction_target(target)
            temporary = target.parent / f".{target.name}.r073v-{nonce}-{index}.tmp"
            backup = target.parent / f".{target.name}.r073v-{nonce}-{index}.bak"
            if _lstat(temporary) is not None or _lstat(backup) is not None:
                raise RuntimeError("transaction scratch collision")
            with temporary.open("xb") as stream:
                stream.write(staged[target])
                stream.flush()
                os.fsync(stream.fileno())
            rows.append({
                "target": target, "temporary": temporary, "backup": backup,
                "existed": target.exists(), "backed_up": False, "installed": False,
            })
        for row in rows:
            if row["existed"]:
                _assert_safe_directory_chain(Path(row["target"]).parent)
                _assert_safe_transaction_target(Path(row["target"]))
                os.replace(row["target"], row["backup"])
                row["backed_up"] = True
        for row in rows:
            _assert_safe_directory_chain(Path(row["target"]).parent)
            _assert_safe_transaction_target(Path(row["target"]))
            os.replace(row["temporary"], row["target"])
            row["installed"] = True
    except BaseException:
        for row in reversed(rows):
            target = Path(row["target"])
            backup = Path(row["backup"])
            if row["installed"] and target.exists():
                target.unlink()
            if row["backed_up"] and backup.exists():
                os.replace(backup, target)
        raise
    finally:
        for row in rows:
            for key in ("temporary", "backup"):
                scratch = Path(row[key])
                if scratch.exists():
                    scratch.unlink()
        for directory in reversed(created_directories):
            try:
                directory.rmdir()
            except OSError:
                pass


def source_dry_run() -> dict[str, object]:
    content = load_release_content(ROOT)
    certificate = certificate_summary()
    figure = figure_summary()
    release_source_presence = {
        relative: (ROOT / relative).is_file() and not (ROOT / relative).is_symlink()
        for relative in RELEASE_SOURCE_EXACT_PATHS
    }
    return {
        "release": RELEASE,
        "siteVersion": SITE_VERSION,
        "mode": "source-dry-run",
        "title": content.release_title_en,
        "publicTitleZh": content.public_title_zh,
        "targetAccounting": R073V_TARGET,
        "baselineAccounting": R073U_BASELINE,
        "canonicalSources": len(content.source_sha256),
        "canonicalSourcesPlanned": len(CANONICAL_SOURCE_PATHS) + len(PLANNED_AUDIT_PATHS),
        "canonicalSourceSha256": content.source_sha256,
        "sections": len(content.sections),
        "publicationReady": content.publication_ready,
        "readinessFailures": list(content.readiness_failures),
        "certificate": certificate,
        "figure": figure,
        "releaseSourcePresence": release_source_presence,
        "releaseSourceReady": all(release_source_presence.values()),
        "commitPinsReady": all(commit != ZERO_COMMIT for _, commit in BINDING_ORDER),
        "publicTransactionImplemented": PUBLIC_TRANSACTION_IMPLEMENTED,
        "bindingOrder": [label for label, _ in BINDING_ORDER],
        "publicationStageOrder": list(PUBLICATION_STAGE_ORDER),
        "coreOutputsPlanned": list(CORE_TARGET_OUTPUTS),
        "laterStageOutputsPlanned": list(LATER_STAGE_OUTPUTS),
        "figureOutputsPlanned": list(FIGURE_PUBLIC_OUTPUTS),
        "translationPath": "LOCAL_DIRECT_NO_DGX",
        "clayConclusion": "OPEN",
        "writes": 0,
    }


def verify_release_inputs() -> ReleaseContent:
    verify_binding_order()
    verify_pinned_paths_exist(RELEASE_BASELINE_COMMIT, BASELINE_EXACT_PATHS, "R0.73U baseline")
    verify_commit_paths(ANALYTIC_SOURCE_COMMIT, ANALYTIC_EXACT_PATHS, "R0.73V analytic source")
    verify_commit_trees(FINITE_PACKAGE_COMMIT, FINITE_EXACT_ROOTS, "R0.73V finite package")
    verify_commit_trees(
        FIGURE_PACKAGE_COMMIT,
        FIGURE_EXACT_ROOTS,
        "R0.73V sealed figure package",
    )
    verify_commit_paths(FINAL_CONTENT_COMMIT, FINAL_CONTENT_EXACT_PATHS, "R0.73V final content")
    verify_commit_paths(RELEASE_SOURCE_COMMIT, RELEASE_SOURCE_EXACT_PATHS, "R0.73V release source")
    certificate_manifest = validate_certificate_package()
    validate_figure_package(certificate_manifest)
    content = load_release_content(ROOT)
    if not content.publication_ready:
        raise RuntimeError("R0.73V canonical content is not publication-ready: " + repr(content.readiness_failures))
    if certificate_summary().get("finalSeal") is not True:
        raise RuntimeError("R0.73V finite certificate lacks its final immutable-source seal")
    if figure_summary().get("formal") is not True:
        raise RuntimeError("R0.73V formal figure package is absent or unsealed")
    if not PUBLIC_TRANSACTION_IMPLEMENTED:
        raise RuntimeError("R0.73V public transaction implementation is disabled")
    return content


def pending_changes(staged: dict[Path, bytes]) -> dict[Path, bytes]:
    """Return only byte changes; a second apply is therefore a zero-write run."""
    changed: dict[Path, bytes] = {}
    for path, payload in staged.items():
        status = _lstat(path)
        if status is not None and (
            stat.S_ISLNK(status.st_mode) or not stat.S_ISREG(status.st_mode)
        ):
            raise RuntimeError("unsafe staged comparison target: " + str(path))
        if status is None or path.read_bytes() != payload:
            changed[path] = payload
    return changed


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate or explicitly apply the fail-closed R0.73V release transaction."
    )
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--source-dry-run", action="store_true")
    actions.add_argument("--check-only", action="store_true")
    actions.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if not (args.source_dry_run or args.check_only or args.apply):
        parser.print_help()
        return
    if args.source_dry_run:
        print(json.dumps(source_dry_run(), ensure_ascii=False, indent=2))
        return
    content = verify_release_inputs()
    staged = build_staged(content)
    changed = pending_changes(staged)
    summary = {
        "release": RELEASE,
        "siteVersion": SITE_VERSION,
        "checkOnly": args.check_only,
        "applied": args.apply,
        "writes": 0 if args.check_only else len(changed),
        "wouldWrite": len(changed),
        "stagedOutputs": len(staged),
        "publicationStageIncomplete": True,
        "pdfGenerated": False,
        "translationsGenerated": False,
    }
    if args.check_only:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return
    commit_transaction(changed)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except CanonicalSourceError as exc:
        raise SystemExit("R0.73V canonical-source gate failed: " + str(exc)) from exc
