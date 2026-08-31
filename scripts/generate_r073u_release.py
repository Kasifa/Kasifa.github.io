#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fail-closed R0.73U GitHub Pages release transaction.

The mathematical copy comes from ``r073u_release_content.py``.  This file owns
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

from r073u_release_content import (
    CANONICAL_SOURCE_PATHS,
    CLOSED_LEDGER,
    FINITE_LEDGER,
    FIGURE_ARCHIVE_RELATIVE,
    FIGURE_ID,
    FIGURE_SOURCE_RELATIVE,
    INITIAL_TIME_BOUNDARY_ZH,
    OPEN_LEDGER,
    PLANNED_AUDIT_PATHS,
    R073T_BASELINE,
    R073U_TARGET,
    RELEASE,
    SITE_VERSION,
    CanonicalSourceError,
    ReleaseContent,
    load_release_content,
)


ROOT = Path(os.environ.get(
    "R073U_RELEASE_ROOT", Path(__file__).resolve().parents[1]
)).resolve()
PUBLIC = ROOT / "public"
ZERO_COMMIT = "0" * 40

# Binding order is oldest to newest.  The published R0.73T baseline and the
# four-file R0.73U analytic layer and both scientific packages are immutable.
# The final reader-content layer is immutable.  Only the release-source self-pin
# deliberately remains zero until the release-source paths are committed;
# --source-dry-run is usable in both states while --check-only and --apply fail
# closed pre-seal.
RELEASE_BASELINE_COMMIT = "3d23297f072b2059da3981b69ce5a8301ed690d7"
ANALYTIC_SOURCE_COMMIT = "84e808dae473f6381cbf9df55a71f5fe81a1cfce"
FINITE_SOURCE_COMMIT = "6c79f23152116f5d420be6ff03653500ab02ef0e"
FINITE_PACKAGE_COMMIT = "044bfb3f7e5af98e2615f60747c9e5109ef12d7c"
FIGURE_PACKAGE_COMMIT = "6c20af03a21488fea3f060738084fa9048437984"
FIGURE_METADATA_INPUT_COMMIT = "478674623bbbd9c9953c13048fd3455644736084"
FIGURE_METADATA_RESEAL_COMMIT = "8f425d85a614b3d307715b4bf4f5daa5fff23693"
FINAL_CONTENT_COMMIT = "552ce0015e5eac0bf1d93968304ec53c7181774e"
RELEASE_SOURCE_COMMIT = "a3eabb5ec6ddb24342a44f92ab4efbb1a44834d0"

BINDING_ORDER = (
    ("R0.73T published baseline", RELEASE_BASELINE_COMMIT),
    ("R0.73U analytic source", ANALYTIC_SOURCE_COMMIT),
    ("R0.73U finite source", FINITE_SOURCE_COMMIT),
    ("R0.73U sealed finite package", FINITE_PACKAGE_COMMIT),
    ("R0.73U formal figure package", FIGURE_PACKAGE_COMMIT),
    ("R0.73U final reader content", FINAL_CONTENT_COMMIT),
    ("R0.73U figure metadata inputs", FIGURE_METADATA_INPUT_COMMIT),
    ("R0.73U figure metadata reseal", FIGURE_METADATA_RESEAL_COMMIT),
    ("R0.73U release source", RELEASE_SOURCE_COMMIT),
)

ANALYTIC_EXACT_PATHS = (
    "research/r073u_problem_freeze.md",
    "research/r073u_tensor_heat_hierarchy.md",
    "research/r073u_independent_analytic_audit.md",
    "research/r073u_primary_literature_audit.md",
)
FINAL_CONTENT_EXACT_PATHS = (
    "research/r073u_claim_source_ledger.md",
    "research/r073u_evidence_gap_matrix.md",
    "research/r073u_finite_diagnostic_audit.md",
    "research/r073u_report-source.md",
    "research/r073u_bilingual_dictionary.md",
    "research/r073u_figure_source_audit.md",
    "research/r073u_figure_source_reaudit.md",
)
FINITE_EXACT_ROOTS = ("research/certificates/r073u",)
FIGURE_EXACT_ROOTS = (FIGURE_SOURCE_RELATIVE,)
BASELINE_EXACT_PATHS = (
    "VERSION",
    "research/release-manifest.json",
    "research/formal-archive-inventory.json",
    "public/site-version.json",
    "public/notes/r0-73t.html",
    "public/recap-r0-61-r0-73t.html",
    "public/research-review.html",
    "public/literature-review.html",
    "public/notes/index.html",
)
RELEASE_SOURCE_EXACT_PATHS = (
    "scripts/r073u_release_content.py",
    "scripts/generate_r073u_release.py",
    "scripts/add-r073u-translations.mjs",
    "scripts/bind-r073u-pdfs.mjs",
    "scripts/render-note-pdf.mjs",
    "tests/r073u-tensor-heat-hierarchy-gate.test.mjs",
    "tests/r073u-release.test.mjs",
    "tests/site-route-current-boundary.test.mjs",
)

CORE_TARGET_OUTPUTS = (
    "public/notes/r0-73u.html",
    "public/recap-r0-61-r0-73u.html",
    "public/research-review.html",
    "public/literature-review.html",
    "public/notes/index.html",
    "public/site-version.json",
    "research/release-manifest.json",
    "research/formal-archive-inventory.json",
    "VERSION",
)
LATER_STAGE_OUTPUTS = (
    "public/notes/r0-73u.pdf",
    "public/recap-r0-61-r0-73u.pdf",
    "research/r073u_note_pdf_render.json",
    "research/r073u_recap_pdf_render.json",
    "research/r073u_pdf_bindings.json",
    "translations/en.json",
    "public/i18n-en.js",
    "scripts/i18n-snapshots/r073u-missing.json",
)
FIGURE_PUBLIC_OUTPUTS = (
    f"{FIGURE_ARCHIVE_RELATIVE}/manifest.json",
    f"public/{FIGURE_ARCHIVE_RELATIVE}/manifest.json",
    f"public/assets/r073u/{FIGURE_ID}.pdf",
    f"public/assets/r073u/{FIGURE_ID}.svg",
    f"public/assets/r073u/{FIGURE_ID}.png",
)
PUBLICATION_STAGE_ORDER = (
    "freeze-r073t-published-baseline",
    "freeze-r073u-analytic-and-package-sources",
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
        raise RuntimeError("R0.73U normalized release-source pin slot drift")
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
            raise RuntimeError("R0.73U binding commits are not in declared ancestry order")


def verify_commit_paths(commit: str, paths: tuple[str, ...], label: str) -> None:
    for relative in paths:
        committed = git_bytes(commit, relative)
        present = current_regular_bytes(relative)
        if relative == "scripts/generate_r073u_release.py":
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
        raise RuntimeError(relative + ": frozen R0.73T baseline is not UTF-8") from exc


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
    tokens = ["R0.73U", "/i18n-en.js?v=1.61"]
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


def require_initial_time_figure_boundary(contract: dict) -> None:
    """Reject the invalid reading of the sign pair as a trajectory symmetry."""
    try:
        caption = current_regular_bytes(
            f"{FIGURE_SOURCE_RELATIVE}/caption.md"
        ).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError("R0.73U figure caption is not UTF-8") from exc
    initial_time = re.compile(r"(?:initial[- ](?:time|state)|t\s*=\s*0)", re.I)
    if (
        initial_time.search(caption) is None
        or "not a trajectory symmetry" not in caption.lower()
        or contract.get("normalization", {}).get("evaluationTime") != "initial time t=0"
        or contract.get("claimBoundary", {}).get("initialTimeTangentOnly") is not True
        or contract.get("claimBoundary", {}).get("trajectorySymmetryClaim") is not False
    ):
        raise RuntimeError(
            "R0.73U figure must state that the u/-u tangent separation is an "
            "initial-time (t=0) fact, not a trajectory symmetry"
        )


def validate_certificate_package() -> dict:
    base = "research/certificates/r073u"
    manifest = strict_json_file(f"{base}/manifest.json", "R0.73U certificate manifest")
    checklist = strict_json_file(
        f"{base}/audit-checklist.json", "R0.73U certificate checklist"
    )
    results = strict_json_file(f"{base}/results.json", "R0.73U certificate results")
    expected_inventory = {
        "analyticSourceFileCount": 4,
        "boundFileCount": 7,
        "generatedFileCount": 3,
        "packageFileCount": 9,
        "sha256SumsLineCount": 8,
        "sourceFileCount": 6,
    }
    if (
        manifest.get("schemaVersion") != "r073u-exact-tensor-heat-manifest-v1"
        or manifest.get("release") != RELEASE
        or manifest.get("status") != "sealed"
        or manifest.get("finalSeal") is not True
        or manifest.get("sourceCommitAssigned") is not True
        or manifest.get("sourceCommit") != ANALYTIC_SOURCE_COMMIT
        or manifest.get("analyticSourceCommit") != ANALYTIC_SOURCE_COMMIT
        or manifest.get("certificateSourceCommitAssigned") is not True
        or manifest.get("certificateSourceCommit") != FINITE_SOURCE_COMMIT
        or manifest.get("allPrerequisiteChecksPass") is not True
        or manifest.get("checkInventory") != {"exact": 75, "required": 75}
        or manifest.get("inventory") != expected_inventory
    ):
        raise RuntimeError("R0.73U certificate is not final-sealed to the analytic commit")
    required_checks = checklist.get("requiredChecks")
    audit = results.get("audit")
    if (
        checklist.get("schemaVersion") != 1
        or not isinstance(required_checks, list)
        or len(required_checks) != 75
        or len({row.get("id") for row in required_checks if isinstance(row, dict)}) != 75
        or results.get("schemaVersion") != 1
        or not isinstance(audit, dict)
        or audit.get("required") != 75
        or audit.get("passed") != 75
        or not isinstance(audit.get("results"), list)
        or len(audit["results"]) != 75
        or not all(isinstance(row, dict) and row.get("pass") is True
                   for row in audit["results"])
    ):
        raise RuntimeError("R0.73U certificate exact 75-check audit drifted")
    producer = results.get("producer")
    if (
        results.get("arithmetic")
        != "Python standard-library fractions.Fraction; exact Gaussian rationals; no floating point"
        or not isinstance(producer, dict)
        or producer.get("standardLibraryOnly") is not True
        or producer.get("gpu") != "not used"
        or producer.get("network") != "not used"
        or producer.get("dgx") != "not used"
        or producer.get("ordinaryTranslationPath") != "LOCAL_DIRECT_NO_DGX"
    ):
        raise RuntimeError("R0.73U certificate arithmetic/compute boundary drifted")
    boundary = manifest.get("claimBoundary")
    if not isinstance(boundary, str) or not all(token in boundary for token in (
        "Exact finite Fourier coefficients", "no generic PDE integration",
        "global regularity", "Clay conclusion",
    )):
        raise RuntimeError("R0.73U certificate claim boundary drifted")

    actual = sorted(
        path.name for path in (ROOT / base).iterdir()
        if path.is_file() and not path.is_symlink()
    )
    expected = sorted({
        "README.md", "SHA256SUMS", "audit-checklist.json", "command.txt",
        "compute_exact_certificate.py", "manifest.json", "requirements.txt",
        "results.json", "seal_package.py",
    })
    if actual != expected:
        raise RuntimeError("R0.73U certificate nine-file inventory drifted")
    recorded = manifest.get("files")
    if not isinstance(recorded, list) or len(recorded) != 7:
        raise RuntimeError("R0.73U certificate manifest-bound inventory drifted")
    by_name = {
        row.get("path"): row for row in recorded
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    }
    if set(by_name) != set(expected) - {"manifest.json", "SHA256SUMS"}:
        raise RuntimeError("R0.73U certificate manifest file paths drifted")
    for name, row in by_name.items():
        payload = current_regular_bytes(f"{base}/{name}")
        if row.get("bytes") != len(payload) or row.get("sha256") != sha256(payload):
            raise RuntimeError("R0.73U certificate manifest is not byte-bound: " + name)
    source_names = {
        "README.md", "audit-checklist.json", "command.txt",
        "compute_exact_certificate.py", "requirements.txt", "seal_package.py",
    }
    analytic_rows = manifest.get("sourceBindings")
    if not isinstance(analytic_rows, list) or {
        row.get("path") for row in analytic_rows if isinstance(row, dict)
    } != set(ANALYTIC_EXACT_PATHS):
        raise RuntimeError("R0.73U certificate analytic-source inventory drifted")
    source_rows = manifest.get("certificateSourceBindings")
    commit_rows = manifest.get("certificateSourceCommitBindings")
    if (
        not isinstance(source_rows, list)
        or {row.get("path") for row in source_rows if isinstance(row, dict)} != source_names
        or not isinstance(commit_rows, list)
        or {Path(str(row.get("path"))).name for row in commit_rows if isinstance(row, dict)}
        != source_names
    ):
        raise RuntimeError("R0.73U certificate six-source inventory drifted")
    run_package_verifier(
        f"{base}/compute_exact_certificate.py", ["--check-only"],
        "R0.73U exact certificate producer",
    )
    run_package_verifier(
        f"{base}/seal_package.py",
        ["--analytic-source-commit", ANALYTIC_SOURCE_COMMIT,
         "--certificate-source-commit", FINITE_SOURCE_COMMIT, "--check-only"],
        "R0.73U certificate provenance seal",
    )
    return manifest


def validate_figure_package(certificate_manifest: dict) -> dict:
    base = FIGURE_SOURCE_RELATIVE
    manifest = strict_json_file(f"{base}/manifest.json", "R0.73U figure manifest")
    config = strict_json_file(f"{base}/config.json", "R0.73U figure config")
    contract = strict_json_file(f"{base}/contract.json", "R0.73U figure contract")
    results = strict_json_file(f"{base}/results.json", "R0.73U figure results")
    validation = strict_json_file(f"{base}/validation.json", "R0.73U figure validation")
    require_initial_time_figure_boundary(contract)
    if (
        manifest.get("schemaVersion")
        != "r073u-tensor-heat-hierarchy-manifest-v1"
        or manifest.get("figureId") != FIGURE_ID
        or manifest.get("finalSeal") is not True
        or manifest.get("sourceCommitAssigned") is not True
        or manifest.get("sourceCommit") != ANALYTIC_SOURCE_COMMIT
        or manifest.get("validation") != {
            "checksPassed": 325, "checksRequired": 325, "status": "PASS",
        }
        or certificate_manifest.get("sourceCommit") != ANALYTIC_SOURCE_COMMIT
    ):
        raise RuntimeError("R0.73U figure is not source-bound and QA-confirmed")
    source_git = manifest.get("git")
    if (
        manifest.get("release") != RELEASE
        or manifest.get("status") != "formal"
        or manifest.get("publicationStatus") != "staged"
        or not isinstance(source_git, dict)
        or source_git.get("sourceCommit") != ANALYTIC_SOURCE_COMMIT
        or source_git.get("certificateCommit") != FINITE_PACKAGE_COMMIT
        or source_git.get("figureMetadataResealCommit")
        != FIGURE_METADATA_INPUT_COMMIT
        or source_git.get("dirtyAtCertifiedRun") is not False
        or not isinstance(manifest.get("computation"), dict)
        or manifest["computation"].get("kind") != "exact-formula-audit"
        or not isinstance(manifest.get("compute"), dict)
        or not isinstance(manifest.get("environment"), dict)
    ):
        raise RuntimeError("R0.73U figure global provenance contract drifted")
    if (
        config.get("schemaVersion") != "r073u-tensor-heat-hierarchy-figure-config-v1"
        or config.get("figureId") != FIGURE_ID
        or config.get("widthMillimetres") != 178.0
        or config.get("heightMillimetres") != 100.0
        or config.get("pngDpi") != 600
        or results.get("schemaVersion")
        != "r073u-tensor-heat-hierarchy-figure-results-v1"
        or results.get("figureId") != FIGURE_ID
        or results.get("rowCount") != 138
        or results.get("allSourceChecksPass") is not True
        or results.get("series") != {
            "analyticCurveSamples": 111,
            "analyticSchematic": 4,
            "exactFiniteDiagnostic": 22,
            "exactPeak": 1,
        }
    ):
        raise RuntimeError("R0.73U figure result/configuration drifted")
    checks = validation.get("checks")
    if (
        validation.get("schemaVersion")
        != "r073u-tensor-heat-hierarchy-validation-v1"
        or validation.get("figureId") != FIGURE_ID
        or validation.get("status") != "PASS"
        or validation.get("finalSeal") is not True
        or validation.get("sourceCommitAssigned") is not True
        or validation.get("sourceCommit") != ANALYTIC_SOURCE_COMMIT
        or validation.get("checksPassed") != 325
        or validation.get("checksRequired") != 325
        or validation.get("visualQaConfirmed") is not True
        or not isinstance(checks, list)
        or len(checks) != 325
        or not all(isinstance(row, dict) and row.get("pass") is True for row in checks)
    ):
        raise RuntimeError("R0.73U figure validation provenance drifted")
    boundary = contract.get("claimBoundary")
    if (
        contract.get("schemaVersion")
        != "r073u-tensor-heat-hierarchy-figure-contract-v1"
        or contract.get("figureId") != FIGURE_ID
        or contract.get("release") != RELEASE
        or not isinstance(boundary, dict)
        or any(payload.get("claimBoundary") != boundary
               for payload in (manifest, results))
    ):
        raise RuntimeError("R0.73U figure claim boundary is absent")
    for key in (
        "fittedScalingLaw",
        "navierStokesSimulation",
        "singularSolution",
        "regularityCriterionImproved",
        "globalRegularityEstablished",
        "clayProblemSolved",
    ):
        if boundary.get(key) is not False:
            raise RuntimeError("R0.73U figure overclaims " + key)
    if boundary.get("exactFormulaAndFiniteDiagnosticOnly") is not True:
        raise RuntimeError("R0.73U figure lost its exact finite evidence class")
    recorded = manifest.get("files")
    if not isinstance(recorded, list) or len(recorded) != 23:
        raise RuntimeError("R0.73U figure sealed inventory drifted")
    by_name = {
        row.get("path"): row for row in recorded
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    }
    if len(by_name) != len(recorded):
        raise RuntimeError("R0.73U figure sealed inventory contains duplicate paths")
    for name, row in by_name.items():
        payload = current_regular_bytes(f"{base}/{name}")
        if row.get("bytes") != len(payload) or row.get("sha256") != sha256(payload):
            raise RuntimeError("R0.73U figure manifest is not byte-bound: " + name)
    dependency_root = os.environ.get(
        "R073U_FIGURE_DEPS", "/Users/kasifa/.cache/codex-runtimes/r073s-figure-python"
    )
    executable = os.environ.get(
        "R073U_FIGURE_PYTHON",
        "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3",
    )
    if not Path(dependency_root).is_dir() or not Path(executable).is_file():
        raise RuntimeError(
            "R0.73U figure verifier runtime missing; set R073U_FIGURE_DEPS and R073U_FIGURE_PYTHON"
        )
    run_package_verifier(
        f"{base}/validate.py",
        ["--deps", dependency_root, "--verify-only"],
        "R0.73U figure",
        executable=executable,
    )
    return manifest


def certificate_summary() -> dict[str, object]:
    root = ROOT / "research/certificates/r073u"
    manifest_path = root / "manifest.json"
    if not manifest_path.is_file() or manifest_path.is_symlink():
        return {"present": root.is_dir(), "finalSeal": False, "status": "missing-manifest"}
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {"present": True, "finalSeal": False, "status": "invalid-manifest"}
    final = (
        manifest.get("schemaVersion") == "r073u-exact-tensor-heat-manifest-v1"
        and manifest.get("release") == RELEASE
        and manifest.get("status") == "sealed"
        and manifest.get("finalSeal") is True
        and manifest.get("sourceCommitAssigned") is True
        and manifest.get("sourceCommit") == ANALYTIC_SOURCE_COMMIT
        and manifest.get("certificateSourceCommitAssigned") is True
        and manifest.get("certificateSourceCommit") == FINITE_SOURCE_COMMIT
        and manifest.get("allPrerequisiteChecksPass") is True
        and manifest.get("checkInventory") == {"exact": 75, "required": 75}
    )
    return {
        "present": True,
        "finalSeal": final,
        "status": manifest.get("status", "hash-bound-without-source-commit"),
        "schemaVersion": manifest.get("schemaVersion"),
        "sha256": sha256(manifest_path.read_bytes()),
    }


def figure_summary() -> dict[str, object]:
    root = ROOT / FIGURE_SOURCE_RELATIVE
    manifest_path = root / "manifest.json"
    if not manifest_path.is_file() or manifest_path.is_symlink():
        return {"present": root.is_dir(), "formal": False, "status": "missing-manifest"}
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {"present": True, "formal": False, "status": "invalid-manifest"}
    formal = (
        manifest.get("schemaVersion")
        == "r073u-tensor-heat-hierarchy-manifest-v1"
        and manifest.get("figureId") == FIGURE_ID
        and manifest.get("finalSeal") is True
        and manifest.get("sourceCommitAssigned") is True
        and manifest.get("sourceCommit") == ANALYTIC_SOURCE_COMMIT
        and manifest.get("validation") == {
            "checksPassed": 325,
            "checksRequired": 325,
            "status": "PASS",
        }
    )
    return {
        "present": True,
        "formal": formal,
        "status": "source-bound-qa-passed" if formal else "incomplete",
        "figureId": manifest.get("figureId"),
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
    value = decode_baseline("public/notes/r0-73t.html")
    description = (
        "研究笔记 R0.73U：完整局部乘积张量的 heat covariance、同尺度压力重建、"
        "两条临界 stress 估计，以及四站点二次状态非自治见证。"
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
        f'<meta property="og:image" content="https://kasifa.github.io/assets/r073u/{FIGURE_ID}.png">',
        "note OG image",
    )
    value = replace_regex(
        value, r'<title>.*?</title>',
        f'<title>{html.escape(content.document_title_en)}</title>', "note title",
    )
    value = replace_once(value, "/i18n-en.js?v=1.60", "/i18n-en.js?v=1.61", "note i18n")
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
        f'<div>研究笔记 R0.73U · {html.escape(content.date)}<br>'
        '<a href="/">返回研究主页</a></div></footer>',
        "note footer",
    )
    assert_public_html(value, "R0.73U note")
    if "/note-retro.css" not in value or value.count(FIGURE_ID) < 4:
        raise RuntimeError("R0.73U note lost retro stylesheet or formal figure links")
    return value


def build_recap(content: ReleaseContent) -> str:
    value = decode_baseline("public/recap-r0-61-r0-73t.html")
    value = value.replace("/i18n-en.js?v=1.60", "/i18n-en.js?v=1.61")
    value = value.replace("R0.61–R0.73T", "R0.61–R0.73U")
    value = value.replace(
        "R0.61–R0.73U · 2026-08-31",
        f"R0.61–R0.73U · {content.date}",
    )
    value = value.replace(
        "R0.61–R0.73U 回顾 · 2026-08-31",
        f"R0.61–R0.73U 回顾 · {content.date}",
    )
    value = value.replace("R0.61 到 R0.73T", "R0.61 到 R0.73U")
    value = value.replace("R0.69P–R0.73T", "R0.69P–R0.73U")
    value = value.replace("R0.70A–R0.73T", "R0.70A–R0.73U")
    value = value.replace("回顾截止节点：R0.73T", "回顾截止节点：R0.73U")
    value = value.replace("收录节点：136", "收录节点：137")
    value = value.replace("回顾截止时公开笔记：196", "回顾截止时公开笔记：197")
    value = value.replace("136 节", "137 节").replace("136 个节点", "137 个节点")
    value = value.replace("98 个版本", "99 个版本").replace("98 节", "99 节")
    value = value.replace("74 个满足", "75 个满足").replace("74 节", "75 节")
    value = value.replace("55 个阶段", "56 个阶段")
    value = value.replace("55 个研究阶段", "56 个研究阶段")
    value = value.replace("<strong>136</strong>", "<strong>137</strong>")
    value = value.replace("<strong>98</strong>", "<strong>99</strong>")
    value = value.replace("<strong>74</strong>", "<strong>75</strong>")
    value, duplicate_phase_count = re.subn(
        r'(<article class="phase"><h3>)(R0\.73[N-T]) · \2 \| ',
        r"\1\2 | ",
        value,
    )
    if duplicate_phase_count != 7:
        raise RuntimeError(
            "R0.73U recap expected seven duplicated R0.73N--T phase titles, found "
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
        'R0.73U 共 137 个节点；最新一节分开 heat covariance、同尺度压力重建、'
        '临界 stress 行与二次状态非自治。">',
        "recap description",
    )
    value = replace_regex(
        value, r'<meta property="og:description" content="[^"]*">',
        '<meta property="og:description" content="56 个阶段、137 个节点：从约化递推和环带排除'
        '到完整张量 heat hierarchy、压力重建与精确非自治见证。">',
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
        '<span class="node-ref"><a href="/notes/r0-73u.html">R0.73U</a>'
        '<span class="node-state kind-closed">闭</span></span>'
    )
    value = replace_once(
        value,
        '          </div>\n        </section>\n\n        <section id="retained"',
        f'            {node}\n          </div>\n        </section>\n\n        <section id="retained"',
        "recap node append",
    )
    retained = (
        '<li>R0.73U 把状态提升为完整局部乘积张量：heat covariance 逐点半正定并满足精确'
        '尺度方程，完整张量在同一尺度重建压力。条件临界 stress 行已经假设 '
        '<code>L_t^4L_x^6</code>；能量行在零尺度损失 <code>s^(-1/2)</code>。四站点符号对'
        '只排除偶二次状态的单值带符号切向量，不排除 signed augmentation。'
        f'{html.escape(INITIAL_TIME_BOUNDARY_ZH)} NOT CLAY。</li>'
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
        '<p>不能把 137 个节点或 99 个公开版本解释成 Clay 完成比例。'
        '同尺度压力重建成立；但零尺度能量控制、有限张量闭合与任意数据正则性保持开放。'
        '任意三维初值全局正则性仍为 OPEN。</p></section>',
        "recap current value",
    )
    value = replace_regex(
        value, r'<section id="next">.*?</section>',
        '<section id="next"><div class="section-no">05 / 下一步</div>'
        f'<h2>{html.escape(content.next_release)}：最小 signed third-order lift</h2>'
        f'<p>{html.escape(content.next_gate_zh)}</p></section>',
        "recap next gate",
    )
    value = replace_regex(
        value, r'<section id="claims">.*?</section>',
        '<section id="claims"><div class="section-no">06 / 说明边界</div>'
        '<h2>经典结果、本地有限结论和开放问题分开列示</h2>'
        '<p>R0.70A–R0.73U 的 99 节已公开；75 节完整封存；24 节旧档待回补。</p>'
        f'<p>{html.escape(CLOSED_LEDGER)}</p>'
        f'<p>{html.escape(FINITE_LEDGER)}</p>'
        f'<p>{html.escape(OPEN_LEDGER)}</p>'
        '<p>R0.73U 的有限公式证书和正式附图只复算精确稀疏 Fourier 恒等式与见证族；'
        '它们不积分一般非线性解，不运行 Navier--Stokes 仿真。'
        f'{html.escape(INITIAL_TIME_BOUNDARY_ZH)} NOT CLAY。</p>'
        '</section>',
        "recap exact boundary",
    )
    value = replace_regex(
        value, r'<section id="reproduce">.*?</section>',
        '<section id="reproduce"><div class="section-no">07 / 原始资料</div>'
        '<h2>逐节笔记、证明、审计、证书、附图和历史回顾</h2>'
        '<p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · '
        '<a href="/recap-r0-61-r0-73t.html">保留 R0.73T 历史回顾</a> · '
        '<a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · '
        '<a href="/notes/r0-73u.html">打开最新节点 R0.73U</a></p>'
        '<p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073u_report-source.md">查看 canonical report</a> · '
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073u_tensor_heat_hierarchy.md">查看解析证明</a> · '
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073u_primary_literature_audit.md">查看一手文献审计</a> · '
        '<a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073u">查看有限证书</a> · '
        f'<a href="/assets/r073u/{FIGURE_ID}.pdf">下载期刊附图</a> · '
        '<a href="/recap-r0-61-r0-73u.pdf">下载同步 PDF</a></p>'
        '<p>经典结论由一手来源承担；本地解析证明承担一侧推论和 no-go；有限诊断只作可复现错误探测。'
        'NOT CLAY。</p></section>',
        "recap reproduction",
    )
    value = value.replace("/recap-r0-61-r0-73t.pdf", "/recap-r0-61-r0-73u.pdf")
    value = value.replace("R0.73T 回顾", "R0.73U 回顾")
    for stale in ("<strong>136</strong>", "<strong>98</strong>", "<strong>74</strong>"):
        if stale in value:
            raise RuntimeError("R0.73U recap retained stale metric " + stale)
    if value.count('<article class="phase">') != 56:
        raise RuntimeError("R0.73U recap must contain exactly 56 phase articles")
    if "55 个阶段" in value or "55 个研究阶段" in value:
        raise RuntimeError("R0.73U recap retained a stale displayed phase count")
    assert_public_html(value, "R0.73U recap")
    return value


def latest_spotlight(content: ReleaseContent) -> str:
    return (
        '<section class="route-overview latest-release-spotlight" id="latest-release" '
        'aria-labelledby="latest-release-title"><div class="route-overview-inner">'
        '<header class="route-map-header"><div>'
        f'<p class="eyebrow">LATEST RELEASE · R0.73U · {html.escape(content.date)}</p>'
        f'<h2 class="route-map-title" id="latest-release-title">{html.escape(content.public_title_zh)}</h2>'
        f'<p class="route-map-intro">{html.escape(content.home_zh)}</p></div>'
        '<nav class="route-map-actions" aria-label="最新发布快捷入口">'
        '<a class="route-map-latest" href="/notes/r0-73u.pdf">阅读最新 R0.73U 研究笔记 →</a>'
        '<a href="/recap-r0-61-r0-73u.html">137 节累计回顾</a>'
        '<a href="/notes/">197 篇研究笔记总索引</a>'
        '<a href="#r073u">查看首页完整 R0.73U 卡片</a></nav></header>'
        '<div class="route-legend" aria-label="最新发布计数">'
        '<span><i class="route-legend-mark kept" aria-hidden="true"></i>'
        'R0.70A–R0.73U · 99 节已公开</span>'
        '<span><i class="route-legend-mark kept" aria-hidden="true"></i>75 节完整封存</span>'
        '<span><i class="route-legend-mark current" aria-hidden="true"></i>'
        '当前端点 R0.73U</span></div></div></section>'
    )


def update_home(content: ReleaseContent) -> str:
    value = decode_baseline("public/research-review.html")
    value = value.replace('data-site-version="1.60"', 'data-site-version="1.61"')
    value = value.replace("/i18n-en.js?v=1.60", "/i18n-en.js?v=1.61")
    value = value.replace("/site-refresh.js?v=1.60", "/site-refresh.js?v=1.61")
    value = replace_regex(
        value, r'<section class="route-overview latest-release-spotlight".*?</section>',
        latest_spotlight(content), "home latest spotlight",
    )
    marker = '<div class="task-one" id="r073t" data-release="r073t"'
    value = replace_once(value, marker, content.home_card + "\n          " + marker, "home card insert")
    value = value.replace("<strong>196</strong>公开研究笔记", "<strong>197</strong>公开研究笔记")
    value = value.replace("<strong>v1.60</strong>网页版本", "<strong>v1.61</strong>网页版本")
    value = value.replace("<strong>R0.73T</strong>最新研究节点", "<strong>R0.73U</strong>最新研究节点")
    value = replace_regex(
        value, r'<strong>[^<]+</strong>当前方向',
        '<strong>tensor heat hierarchy / signed-flux boundary</strong>当前方向',
        "home current direction",
    )
    value = value.replace("NEXT · R0.73U", "NEXT · R0.73V")
    value = replace_regex(
        value, r'<h3>R0\.73U 下一接口</h3><p>.*?</p>',
        f'<h3>{html.escape(content.next_release)} 下一接口</h3>'
        f'<p>{html.escape(content.next_gate_zh)}</p>',
        "home next interface",
    )
    value = value.replace(
        "R0.70A–R0.73T：98 节已公开，74 节完整封存",
        "R0.70A–R0.73U：99 节已公开，75 节完整封存",
    )
    value = value.replace("Research topology · R0.1–R0.73T", "Research topology · R0.1–R0.73U")
    value = value.replace(
        '<a class="route-map-latest" href="#r073t">跳到首页 R0.73T 卡片 →</a>',
        '<a class="route-map-latest" href="#r073u">跳到首页 R0.73U 卡片 →</a>',
    )
    value = value.replace(
        '/recap-r0-61-r0-73t.html">阅读 R0.60 之后的累计回顾',
        '/recap-r0-61-r0-73u.html">阅读 R0.60 之后的累计回顾',
    )
    value = value.replace("/recap-r0-61-r0-73t.html", "/recap-r0-61-r0-73u.html")
    value = value.replace("/recap-r0-61-r0-73t.pdf", "/recap-r0-61-r0-73u.pdf")
    value = value.replace("综述 v1.60 ·", "综述 v1.61 ·")
    value = value.replace(
        "<strong>2026-08-31</strong>最近修订",
        f"<strong>{html.escape(content.date)}</strong>最近修订",
    )
    value = value.replace(
        "综述 v1.61 · 2026-08-31",
        f"综述 v1.61 · {html.escape(content.date)}",
    )
    value = value.replace(
        '<span class="route-range">R0.69P–R0.73T</span>',
        '<span class="route-range">R0.69P–R0.73U</span>',
    )
    value = replace_regex(
        value, r"R0\.73T：[^<。]+已分列",
        "R0.73U：完整张量 heat hierarchy、同尺度压力重建与二次状态 no-go 已分列",
        "home route summary",
    )
    value = value.replace('<span>R0.72R–R0.73T：</span>', '<span>R0.72R–R0.73U：</span>')
    value = replace_regex(
        value, r"(→ shellwise phase certificate → [^<]+)</p>",
        lambda match: match.group(1) + " → tensor heat hierarchy</p>",
        "home route tail",
    )
    current_paragraph = (
        f'<p>{html.escape(content.recap_zh)} '
        '<span>heat covariance scale PDE</span>；'
        '<span>same-scale pressure reconstruction</span>；'
        '<span>quadratic-state non-autonomy</span>。零尺度能量控制仍开放。</p>'
    )
    value = replace_once(
        value, '              <details class="tree-notes" open>',
        "              " + current_paragraph + '\n              <details class="tree-notes" open>',
        "home route current paragraph",
    )
    value = value.replace('<summary>展开 106 篇公开笔记</summary>', '<summary>展开 107 篇公开笔记</summary>')
    value = value.replace('aria-label="R0.69P–R0.73T"', 'aria-label="R0.69P–R0.73U"')
    value = replace_once(
        value,
        '                  <a class="milestone" href="/notes/r0-73t.html">R0.73T</a>',
        '                  <a class="milestone" href="/notes/r0-73t.html">R0.73T</a>\n'
        '                  <a class="milestone" href="/notes/r0-73u.html">R0.73U</a>',
        "home route R0.73U link",
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
        '<p class="eyebrow">累计回顾 R0.61–R0.73U · 2026-09-01</p>'
        '<h3>R0.60 recap 之后的累计回顾收录 137 个节点；全站现有 197 篇公开研究笔记</h3>'
        '<p>累计回顾现分 56 个阶段，完整保留 R0.61–R0.73U；最新节点分开记录 heat covariance、'
        '同尺度压力重建、临界 stress 行、二次状态 non-autonomy、有限精确诊断和正式附图。</p>'
        '<p>R0.70A–R0.73U 共 99 个版本已公开；75 个按当前 formal-figure 合同完整封存，'
        '24 个旧版附图档案仍列入回补清单。</p>'
        f'<p><strong>阶段判断：</strong>&nbsp;{html.escape(content.recap_zh)} '
        '任意三维初值全局正则性与 Clay 保持 OPEN。</p>'
        '<p><a href="/recap-r0-61-r0-73u.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · '
        '<a href="/recap-r0-61-r0-73u.pdf">下载同步 PDF</a></p></div>'
    )
    value = replace_regex(
        value, r'<div class="task-one" id="post-r060-recap".*?</div>',
        recap_card, "home cumulative recap card",
    )
    value = value.replace(
        "本站 R0.69P–R0.73T 路线放在同一张图中",
        "本站 R0.69P–R0.73U 路线放在同一张图中",
    )
    for stale in (
        "Research topology · R0.1–R0.73T",
        "累计回顾收录 136 个节点；全站现有 196 篇公开研究笔记",
        '<summary>展开 106 篇公开笔记</summary>',
        "<strong>v1.60</strong>网页版本",
        "<strong>R0.73T</strong>最新研究节点",
        'data-site-version="1.60"',
        "/site-refresh.js?v=1.60",
        '<h3>R0.73U 下一接口</h3>',
    ):
        if stale in value:
            raise RuntimeError("R0.73U home retained stale latest marker " + stale)
    assert_public_html(value, "R0.73U home")
    return value


def update_literature(content: ReleaseContent) -> str:
    value = decode_baseline("public/literature-review.html")
    value = value.replace("/i18n-en.js?v=1.60", "/i18n-en.js?v=1.61")
    value = value.replace("文献综述 v1.60 ·", "文献综述 v1.61 ·")
    value = value.replace(
        "文献综述 v1.61 · 2026-08-31",
        f"文献综述 v1.61 · {html.escape(content.date)}",
    )
    marker = '<span class="route-r073t-deck-update">'
    start = value.find(marker)
    end = value.find("</span>", start)
    if start < 0 or end < 0:
        raise RuntimeError("literature R0.73T deck marker missing")
    end += len("</span>")
    value = value[:end] + content.literature_update + value[end:]
    value = value.replace("/recap-r0-61-r0-73t.html", "/recap-r0-61-r0-73u.html")
    value = value.replace("136 节", "137 节")
    value = value.replace("R0.69P–R0.73T", "R0.69P–R0.73U")
    route_step = (
        '<div class="route-step kept"><header><b>R0.73U</b>'
        '<strong>tensor heat hierarchy and the signed-flux boundary</strong></header>'
        f'<p><strong>{html.escape(content.public_title_zh)}</strong></p>'
        '<p>R0.70A–R0.73U：99 节已公开，75 节完整封存。</p>'
        f'<p>{html.escape(content.recap_zh)} <a href="/notes/r0-73u.html">研究笔记</a> '
        '<a href="/recap-r0-61-r0-73u.html">当前累计回顾</a> '
        '<a href="#r073u-boundary">文献边界</a></p></div>'
        '<div class="route-step pause"><header><b>开放接口 · R0.73V</b>'
        '<strong>minimal signed third-order lift</strong></header>'
        '<p>下一步加入最小带符号三阶状态，并检查其物理时间方程能否由 heat 尺度导数或 Stokes smoothing 支付；'
        '任意初值全局正则性与 Clay 保持 OPEN。</p></div>'
    )
    value = replace_regex(
        value,
        r'<div class="route-step pause"><header><b>开放接口 · R0\.73U</b>.*?</div>',
        route_step, "literature current route step",
    )
    literature_boundary = (
        '<h3 id="r073u-boundary">R0.73U 的 KHM、精确 filtering 与带符号三阶通量邻近文献</h3>'
        '<p><a href="https://doi.org/10.1098/rspa.1938.0013">von Kármán--Howarth 1938</a> 与 '
        '<a href="https://doi.org/10.1017/S0022112001003949">Hill 2001</a> 承担经典两点层级；'
        '<a href="https://doi.org/10.1017/S0022112092001733">Germano 1992</a> 承担 filtering 与层间 stress identity。'
        '这些对象必须与本站的局部乘积张量分开。</p>'
        '<p><a href="https://arxiv.org/abs/chao-dyn/9602018">Eyink 1996</a>、'
        '<a href="https://doi.org/10.1007/BF02099744">Constantin--E--Titi 1994</a> 与 '
        '<a href="https://doi.org/10.1088/0951-7715/13/1/312">Duchon--Robert 2000</a> 给出带符号三阶传递语境；'
        '<a href="https://doi.org/10.1017/jfm.2026.11485">Zambrano--Duraisamy 2026</a> 是受限于齐次各向同性湍流的模型闭合。'
        'Tran--Yu--Dritschel 2021 与 centered pressure variance 有直接公式层碰撞。限定式检索未找到相同打包，'
        '但未检出不是新颖性、优先权或不存在证明。</p>'
        '<div class="boundary"><strong>R0.73U 的主张边界</strong>'
        f'<p>{html.escape(CLOSED_LEDGER)}</p>'
        f'<p>{html.escape(FINITE_LEDGER)}</p>'
        f'<p>{html.escape(OPEN_LEDGER)}</p>'
        '<p>一手来源承担经典碰撞；本地解析证明只承担 heat covariance、临界 stress 推论与精确 no-go；'
        '有限包只复算公式诊断，不认证连续 PDE。'
        f'{html.escape(INITIAL_TIME_BOUNDARY_ZH)} NOT CLAY。</p></div>'
    )
    value = replace_once(
        value, '          <ol class="criteria">',
        "          " + literature_boundary + '\n          <ol class="criteria">',
        "literature R0.73U boundary",
    )
    if "开放接口 · R0.73V" not in value or 'id="r073u-boundary"' not in value:
        raise RuntimeError("R0.73U literature route/boundary was not advanced")
    assert_public_html(value, "R0.73U literature")
    for token in ("VERIFIED_CLASSICAL", "INTERNAL_EXACT", "优先权"):
        if token not in value:
            raise RuntimeError("R0.73U literature lost boundary token " + token)
    return value


def build_manifest_outputs(content: ReleaseContent) -> dict[Path, bytes]:
    release = strict_json_bytes(
        git_bytes(RELEASE_BASELINE_COMMIT, "research/release-manifest.json"),
        "release manifest",
    )
    for key, expected in R073T_BASELINE.items():
        if release.get(key) != expected:
            raise RuntimeError("R0.73T release-manifest baseline drift: " + key)
    release.update({
        **R073U_TARGET,
        "latestReleaseGate": "tests/r073u-tensor-heat-hierarchy-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r073u-release.test.mjs",
    })

    site = strict_json_bytes(
        git_bytes(RELEASE_BASELINE_COMMIT, "public/site-version.json"), "site version"
    )
    expected_site = {
        "schemaVersion": "research-site-version-v1",
        "version": "1.60",
        "latestRelease": "R0.73T",
        "publicHtmlNoteCount": 196,
        "publishedDate": "2026-08-31",
    }
    if site != expected_site:
        raise RuntimeError("R0.73T site-version baseline drift")
    site.update({
        "version": SITE_VERSION,
        "latestRelease": RELEASE,
        "publicHtmlNoteCount": 197,
        "publishedDate": content.date,
    })

    inventory = strict_json_bytes(
        git_bytes(RELEASE_BASELINE_COMMIT, "research/formal-archive-inventory.json"),
        "formal archive inventory",
    )
    state = (
        inventory.get("latestPublishedRelease"),
        inventory.get("publishedReleaseCount"),
        inventory.get("formalSealedReleaseCount"),
        inventory.get("legacyFormalFigureBacklogCount"),
    )
    if state != ("r073t", 98, 74, 24):
        raise RuntimeError("R0.73T formal-archive baseline drift")
    for key in ("publishedReleases", "formalSealedReleases"):
        rows = inventory.get(key)
        if not isinstance(rows, list) or rows[-1:] != ["r073t"] or "r073u" in rows:
            raise RuntimeError("formal archive is not append-only: " + key)
        rows.append("r073u")
    inventory.update({
        "latestPublishedRelease": "r073u",
        "publishedReleaseCount": 99,
        "formalSealedReleaseCount": 75,
        "legacyFormalFigureBacklogCount": 24,
    })
    inventory_payload = json_bytes(inventory)
    release["formalArchiveInventory"] = {
        "path": "research/formal-archive-inventory.json",
        "sha256": sha256(inventory_payload),
    }
    return {
        ROOT / "research/release-manifest.json": json_bytes(release),
        ROOT / "research/formal-archive-inventory.json": inventory_payload,
        PUBLIC / "site-version.json": json_bytes(site),
        ROOT / "VERSION": b"1.61\n",
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
        with tempfile.TemporaryDirectory(prefix="r073u-index-") as temporary:
            notes = Path(temporary)
            for relative in git_paths(RELEASE_BASELINE_COMMIT, "public/notes"):
                name = Path(relative).name
                if re.fullmatch(r"r0-[0-9a-z]+\.(?:html|pdf)", name):
                    (notes / name).write_bytes(git_bytes(RELEASE_BASELINE_COMMIT, relative))
            note_index.ROOT, note_index.PUBLIC, note_index.NOTES = ROOT, PUBLIC, notes
            note_index.OUTPUT = notes / "index.html"
            existing = [note_index.parse_note(path) for path in note_index.note_files()]
            if len(existing) != 196 or existing[0].slug != "r0-73t":
                raise RuntimeError("R0.73U note-index baseline is not exact")
            latest = note_index.Note(
                slug="r0-73u",
                code=RELEASE,
                title=content.document_title_en.split("｜", 1)[-1].strip(),
                major=73,
                has_pdf=True,
            )
            note_index.json = TargetJson
            note_index.latest_recap_href = lambda: "/recap-r0-61-r0-73u.html"
            value = note_index.render([latest, *existing])
    finally:
        note_index.json = old_json
        note_index.latest_recap_href = old_recap
        note_index.ROOT, note_index.PUBLIC, note_index.NOTES, note_index.OUTPUT = old_paths
    assert_public_html(value, "R0.73U note index", require_boundary=False)
    if "prefers-color-scheme: dark" not in value:
        raise RuntimeError("R0.73U index lost automatic dark theme")
    return value


def formal_figure_payloads(source: Path) -> dict[str, bytes]:
    source_manifest = strict_json_file(
        f"{FIGURE_SOURCE_RELATIVE}/manifest.json", "R0.73U sealed figure manifest"
    )
    source_git = source_manifest.get("git")
    if (
        source_manifest.get("schemaVersion")
        != "r073u-tensor-heat-hierarchy-manifest-v1"
        or source_manifest.get("figureId") != FIGURE_ID
        or source_manifest.get("publicationStatus") != "staged"
        or source_manifest.get("finalSeal") is not True
        or source_manifest.get("sourceCommitAssigned") is not True
        or source_manifest.get("sourceCommit") != ANALYTIC_SOURCE_COMMIT
        or not isinstance(source_git, dict)
        or source_git.get("sourceCommit") != ANALYTIC_SOURCE_COMMIT
        or source_git.get("certificateCommit") != FINITE_PACKAGE_COMMIT
        or source_git.get("figureMetadataResealCommit")
        != FIGURE_METADATA_INPUT_COMMIT
        or source_git.get("dirtyAtCertifiedRun") is not False
        or source_manifest.get("validation") != {
            "checksPassed": 325,
            "checksRequired": 325,
            "status": "PASS",
        }
    ):
        raise RuntimeError("R0.73U source figure is not a source-bound sealed package")

    actual = sorted(
        path.name for path in source.iterdir()
        if path.is_file() and not path.is_symlink()
    )
    recorded = source_manifest.get("files")
    if (
        len(actual) != 25
        or not isinstance(recorded, list)
        or len(recorded) != 23
        or set(actual) != {
            *(str(row.get("path")) for row in recorded if isinstance(row, dict)),
            "manifest.json",
            "SHA256SUMS",
        }
    ):
        raise RuntimeError("R0.73U formal figure inventory is incomplete or unsealed")
    by_name = {
        row.get("path"): row for row in recorded
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    }
    for name, row in by_name.items():
        payload = current_regular_bytes(f"{FIGURE_SOURCE_RELATIVE}/{name}")
        if row.get("bytes") != len(payload) or row.get("sha256") != sha256(payload):
            raise RuntimeError("R0.73U sealed figure record is not byte-bound: " + name)

    environment = strict_json_file(
        f"{FIGURE_SOURCE_RELATIVE}/environment.json", "R0.73U figure environment"
    )
    contract = strict_json_file(
        f"{FIGURE_SOURCE_RELATIVE}/contract.json", "R0.73U figure contract"
    )
    require_initial_time_figure_boundary(contract)
    results = strict_json_file(
        f"{FIGURE_SOURCE_RELATIVE}/results.json", "R0.73U figure results"
    )
    validation = strict_json_file(
        f"{FIGURE_SOURCE_RELATIVE}/validation.json", "R0.73U figure validation"
    )
    progress_rows = strict_ndjson_file(
        f"{FIGURE_SOURCE_RELATIVE}/progress.ndjson", "R0.73U figure progress log"
    )
    resource_rows = strict_ndjson_file(
        f"{FIGURE_SOURCE_RELATIVE}/resource-log.ndjson", "R0.73U figure resource log"
    )
    execution = environment.get("execution")
    if (
        environment.get("schemaVersion") != "r073u-tensor-heat-hierarchy-environment-v1"
        or not isinstance(execution, dict)
        or execution.get("dgxUsed") is not False
        or execution.get("ordinaryTranslationPath") != "LOCAL_DIRECT_NO_DGX"
        or len(progress_rows) != 4
        or len(resource_rows) != 4
        or progress_rows[-1].get("stage") != "complete"
        or resource_rows[-1].get("stage") != "complete"
        or progress_rows[-1].get("elapsedSeconds")
        != resource_rows[-1].get("elapsedSeconds")
        or validation.get("checksPassed") != 325
        or validation.get("checksRequired") != 325
        or results.get("rowCount") != 138
    ):
        raise RuntimeError("R0.73U figure monitoring or compute boundary drifted")

    claim_boundary = contract.get("claimBoundary")
    if (
        contract.get("schemaVersion")
        != "r073u-tensor-heat-hierarchy-figure-contract-v1"
        or contract.get("release") != RELEASE
        or contract.get("figureId") != FIGURE_ID
        or contract.get("authoritativeAnalyticSourceCommit")
        != ANALYTIC_SOURCE_COMMIT
        or not isinstance(claim_boundary, dict)
        or source_manifest.get("analyticalQuestion")
        != contract.get("analyticalQuestion")
        or source_manifest.get("supportedClaim") != contract.get("supportedClaim")
        or source_manifest.get("claimBoundary") != claim_boundary
        or results.get("claimBoundary") != claim_boundary
    ):
        raise RuntimeError("R0.73U figure contract or claim boundary drifted")

    def record(name: str, schema: str) -> dict[str, object]:
        payload = current_regular_bytes(f"{FIGURE_SOURCE_RELATIVE}/{name}")
        return {"path": name, "schema": schema, "bytes": len(payload), "sha256": sha256(payload)}

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
            "path": f"public/assets/r073u/{FIGURE_ID}.{suffix}",
            "bytes": row["bytes"],
            "sha256": row["sha256"],
        }
        for suffix, row in zip(("pdf", "svg", "png"), outputs)
    ]
    formal = {
        "schemaVersion": "research-figure-manifest-v1",
        "figureId": FIGURE_ID,
        "release": RELEASE,
        "status": "formal",
        "publicationStatus": "published",
        "analyticalQuestion": source_manifest["analyticalQuestion"],
        "supportedClaim": source_manifest["supportedClaim"],
        "createdAt": source_manifest["createdAt"],
        "git": {
            **source_git,
            "certificateSourceCommit": FINITE_SOURCE_COMMIT,
            "certificatePackageCommit": FINITE_PACKAGE_COMMIT,
            "figurePackageCommit": FIGURE_PACKAGE_COMMIT,
            "figureMetadataInputCommit": FIGURE_METADATA_INPUT_COMMIT,
            "figureMetadataResealCommit": FIGURE_METADATA_RESEAL_COMMIT,
        },
        "computation": source_manifest["computation"],
        "compute": source_manifest["compute"],
        "environment": source_manifest["environment"],
        "data": [
            record("source-data.csv", "r073u-tensor-heat-hierarchy-source-v1"),
            record("results.json", "r073u-tensor-heat-hierarchy-figure-results-v1"),
            record("validation.json", "r073u-tensor-heat-hierarchy-validation-v1"),
            record("progress.ndjson", "progress-ndjson-v1"),
            record("resource-log.ndjson", "resource-log-ndjson-v1"),
        ],
        "sourceData": [],
        "figure": {"outputs": outputs},
        "caption": {"english": "caption.md"},
        "qa": {
            "status": "passed",
            "validationChecks": 325,
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "dataCrossChecked": True,
            "qaArtifacts": [
                record("qa-pdf.png", "qa-raster-v1"),
                record("qa-final-size.png", "qa-raster-v1"),
                record("qa-grayscale.png", "qa-raster-v1"),
            ],
        },
        "claimBoundary": claim_boundary,
        "sourceSeal": source_manifest,
        "publication": {
            "archiveDirectory": f"public/{FIGURE_ARCHIVE_RELATIVE}",
            "directory": "public/assets/r073u",
            "fileStem": FIGURE_ID,
            "byteIdentityRequired": True,
            "publicCopiesComplete": True,
            "assets": public_assets,
        },
        "packageInventory": {"paths": actual, "expectedFileCount": len(actual)},
    }
    payloads = {
        name: json_bytes(formal) if name == "manifest.json" else (source / name).read_bytes()
        for name in actual if name != "SHA256SUMS"
    }
    payloads["SHA256SUMS"] = "".join(
        f"{sha256(payloads[name])}  {name}\n" for name in sorted(payloads)
    ).encode("utf-8")
    if sorted(payloads) != actual:
        raise RuntimeError("R0.73U formal figure staging changed the package inventory")
    return payloads

def stage_figure_assets(staged: dict[Path, bytes]) -> None:
    source = ROOT / FIGURE_SOURCE_RELATIVE
    if not source.is_dir() or source.is_symlink() or not (source / "manifest.json").is_file():
        raise RuntimeError("R0.73U formal figure package is incomplete")
    payloads = formal_figure_payloads(source)
    for name, payload in payloads.items():
        staged[ROOT / FIGURE_ARCHIVE_RELATIVE / name] = payload
        staged[PUBLIC / FIGURE_ARCHIVE_RELATIVE / name] = payload
    for suffix in ("pdf", "svg", "png"):
        staged[PUBLIC / f"assets/r073u/{FIGURE_ID}.{suffix}"] = payloads[f"figure.{suffix}"]


def build_staged(content: ReleaseContent) -> dict[Path, bytes]:
    staged: dict[Path, bytes] = {}
    stage_figure_assets(staged)
    staged[PUBLIC / "notes/r0-73u.html"] = build_note(content).encode("utf-8")
    staged[PUBLIC / "recap-r0-61-r0-73u.html"] = build_recap(content).encode("utf-8")
    staged[PUBLIC / "research-review.html"] = update_home(content).encode("utf-8")
    staged[PUBLIC / "literature-review.html"] = update_literature(content).encode("utf-8")
    staged.update(build_manifest_outputs(content))
    staged[PUBLIC / "notes/index.html"] = build_note_index(
        content, staged[PUBLIC / "site-version.json"]
    ).encode("utf-8")
    missing = [relative for relative in CORE_TARGET_OUTPUTS if ROOT / relative not in staged]
    if missing:
        raise RuntimeError("R0.73U staged transaction omitted: " + repr(missing))
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
            temporary = target.parent / f".{target.name}.r073u-{nonce}-{index}.tmp"
            backup = target.parent / f".{target.name}.r073u-{nonce}-{index}.bak"
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
        "targetAccounting": R073U_TARGET,
        "baselineAccounting": R073T_BASELINE,
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
    verify_pinned_paths_exist(RELEASE_BASELINE_COMMIT, BASELINE_EXACT_PATHS, "R0.73T baseline")
    verify_commit_paths(ANALYTIC_SOURCE_COMMIT, ANALYTIC_EXACT_PATHS, "R0.73U analytic source")
    verify_commit_trees(FINITE_PACKAGE_COMMIT, FINITE_EXACT_ROOTS, "R0.73U finite package")
    verify_commit_trees(
        FIGURE_METADATA_RESEAL_COMMIT,
        FIGURE_EXACT_ROOTS,
        "R0.73U figure metadata reseal",
    )
    verify_commit_paths(FINAL_CONTENT_COMMIT, FINAL_CONTENT_EXACT_PATHS, "R0.73U final content")
    verify_commit_paths(RELEASE_SOURCE_COMMIT, RELEASE_SOURCE_EXACT_PATHS, "R0.73U release source")
    certificate_manifest = validate_certificate_package()
    validate_figure_package(certificate_manifest)
    content = load_release_content(ROOT)
    if not content.publication_ready:
        raise RuntimeError("R0.73U canonical content is not publication-ready: " + repr(content.readiness_failures))
    if certificate_summary().get("finalSeal") is not True:
        raise RuntimeError("R0.73U finite certificate lacks its final immutable-source seal")
    if figure_summary().get("formal") is not True:
        raise RuntimeError("R0.73U formal figure package is absent or unsealed")
    if not PUBLIC_TRANSACTION_IMPLEMENTED:
        raise RuntimeError("R0.73U public transaction implementation is disabled")
    return content


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate or explicitly apply the fail-closed R0.73U release transaction."
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
    summary = {
        "release": RELEASE,
        "siteVersion": SITE_VERSION,
        "checkOnly": args.check_only,
        "applied": args.apply,
        "writes": 0 if args.check_only else len(staged),
        "wouldWrite": len(staged),
        "publicationStageIncomplete": True,
        "pdfGenerated": False,
        "translationsGenerated": False,
    }
    if args.check_only:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return
    commit_transaction(staged)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except CanonicalSourceError as exc:
        raise SystemExit("R0.73U canonical-source gate failed: " + str(exc)) from exc
