#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fail-closed R0.73S GitHub Pages release transaction.

The mathematical copy comes from ``r073s_release_content.py``.  This file owns
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
import subprocess
import sys
import tempfile

from r073s_release_content import (
    CANONICAL_SOURCE_PATHS,
    CLOSED_LEDGER,
    FINITE_LEDGER,
    FIGURE_ARCHIVE_RELATIVE,
    FIGURE_ID,
    FIGURE_SOURCE_RELATIVE,
    OPEN_LEDGER,
    R073R_BASELINE,
    R073S_TARGET,
    RELEASE,
    SITE_VERSION,
    CanonicalSourceError,
    ReleaseContent,
    load_release_content,
)


ROOT = Path(os.environ.get(
    "R073S_RELEASE_ROOT", Path(__file__).resolve().parents[1]
)).resolve()
PUBLIC = ROOT / "public"
ZERO_COMMIT = "0" * 40

# Binding order is oldest to newest.  The analytic source commit is also the
# explicit sourceCommit in both sealed scientific packages.  Certificate and
# figure artifacts were committed atomically, so those two pins are equal.
# Final reader copy and this release source remain zero until separately
# committed and reviewed.
RELEASE_BASELINE_COMMIT = "71b562d45529ac45d2423d598fcc0f7f0845ea4b"
ANALYTIC_SOURCE_COMMIT = "72e4c12760dc3b837dec328ee96a29736fe93c99"
FINITE_PACKAGE_COMMIT = "4bb49ecc380e4b41d33e3102af4f47de016b5653"
FIGURE_PACKAGE_COMMIT = "4bb49ecc380e4b41d33e3102af4f47de016b5653"
FINAL_CONTENT_COMMIT = "ee6b4f15733f68ead337eb04d29620fd8b98e60d"
RELEASE_SOURCE_COMMIT = ZERO_COMMIT

BINDING_ORDER = (
    ("R0.73R published baseline", RELEASE_BASELINE_COMMIT),
    ("R0.73S analytic source", ANALYTIC_SOURCE_COMMIT),
    ("R0.73S finite package", FINITE_PACKAGE_COMMIT),
    ("R0.73S formal figure package", FIGURE_PACKAGE_COMMIT),
    ("R0.73S final reader content", FINAL_CONTENT_COMMIT),
    ("R0.73S release source", RELEASE_SOURCE_COMMIT),
)

ANALYTIC_EXACT_PATHS = (
    "research/r073s_problem_freeze.md",
    "research/r073s_quadratic_autocorrelation_certificate.md",
    "research/r073s_primary_literature_audit.md",
    "research/r073s_independent_analytic_audit.md",
    "research/r073s_independent_literature_readback.md",
)
FINAL_CONTENT_EXACT_PATHS = (
    "research/r073s_claim_source_ledger.md",
    "research/r073s_evidence_gap_matrix.md",
    "research/r073s_finite_diagnostic_audit.md",
    "research/r073s_report-source.md",
    "research/r073s_bilingual_dictionary.md",
)
FINITE_EXACT_ROOTS = ("research/certificates/r073s",)
FIGURE_EXACT_ROOTS = (FIGURE_SOURCE_RELATIVE,)
BASELINE_EXACT_PATHS = (
    "VERSION",
    "research/release-manifest.json",
    "research/formal-archive-inventory.json",
    "public/site-version.json",
    "public/notes/r0-73r.html",
    "public/recap-r0-61-r0-73r.html",
    "public/research-review.html",
    "public/literature-review.html",
    "public/notes/index.html",
)
RELEASE_SOURCE_EXACT_PATHS = (
    "scripts/r073s_release_content.py",
    "scripts/generate_r073s_release.py",
    "scripts/add-r073s-translations.mjs",
    "scripts/bind-r073s-pdfs.mjs",
    "tests/r073s-autocorrelation-gate.test.mjs",
    "tests/r073s-release.test.mjs",
    "tests/site-route-current-boundary.test.mjs",
)

CORE_TARGET_OUTPUTS = (
    "public/notes/r0-73s.html",
    "public/recap-r0-61-r0-73s.html",
    "public/research-review.html",
    "public/literature-review.html",
    "public/notes/index.html",
    "public/site-version.json",
    "research/release-manifest.json",
    "research/formal-archive-inventory.json",
    "VERSION",
)
LATER_STAGE_OUTPUTS = (
    "public/notes/r0-73s.pdf",
    "public/recap-r0-61-r0-73s.pdf",
    "research/r073s_pdf_bindings.json",
    "translations/en.json",
    "public/i18n-en.js",
    "scripts/i18n-snapshots/r073s-missing.json",
)
FIGURE_PUBLIC_OUTPUTS = (
    f"{FIGURE_ARCHIVE_RELATIVE}/manifest.json",
    f"public/{FIGURE_ARCHIVE_RELATIVE}/manifest.json",
    f"public/assets/r073s/{FIGURE_ID}.pdf",
    f"public/assets/r073s/{FIGURE_ID}.svg",
    f"public/assets/r073s/{FIGURE_ID}.png",
)
PUBLICATION_STAGE_ORDER = (
    "freeze-r073r-published-baseline",
    "freeze-r073s-analytic-and-package-sources",
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
        raise RuntimeError("R0.73S normalized release-source pin slot drift")
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
            raise RuntimeError("R0.73S binding commits are not in declared ancestry order")


def verify_commit_paths(commit: str, paths: tuple[str, ...], label: str) -> None:
    for relative in paths:
        committed = git_bytes(commit, relative)
        present = current_regular_bytes(relative)
        if relative == "scripts/generate_r073s_release.py":
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
        raise RuntimeError(relative + ": frozen R0.73R baseline is not UTF-8") from exc


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
    tokens = ["R0.73S", "/i18n-en.js?v=1.59"]
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


def validate_certificate_package() -> dict:
    base = "research/certificates/r073s"
    manifest = strict_json_file(f"{base}/manifest.json", "R0.73S certificate manifest")
    config = strict_json_file(f"{base}/config.json", "R0.73S certificate config")
    diagnostic = strict_json_file(f"{base}/diagnostic.json", "R0.73S diagnostic")
    independent = strict_json_file(
        f"{base}/independent_validation.json", "R0.73S independent validation"
    )
    certificate = strict_json_file(f"{base}/certificate.json", "R0.73S certificate")
    validation = strict_json_file(f"{base}/validation.json", "R0.73S certificate validation")
    if (
        manifest.get("schemaVersion") != "r073s-quadratic-autocorrelation-manifest-v2"
        or manifest.get("release") != RELEASE
        or manifest.get("status") != "sealed"
        or manifest.get("finalSeal") is not True
        or manifest.get("sourceCommitAssigned") is not True
        or manifest.get("sourceCommit") != ANALYTIC_SOURCE_COMMIT
        or manifest.get("allPrerequisiteChecksPass") is not True
    ):
        raise RuntimeError("R0.73S certificate is not final-sealed to the analytic commit")
    for payload, label in (
        (diagnostic, "R0.73S diagnostic"),
        (independent, "R0.73S independent validation"),
        (certificate, "R0.73S certificate"),
        (validation, "R0.73S certificate validation"),
    ):
        require_pass_payload(payload, label)
    boundary = config.get("claimBoundary")
    if (
        not isinstance(boundary, dict)
        or any(payload.get("claimBoundary") != boundary
               for payload in (manifest, diagnostic, independent, certificate, validation))
        or manifest.get("independentClaimBoundary") != boundary
    ):
        raise RuntimeError("R0.73S certificate claim boundaries disagree")
    for key in (
        "arithmeticComplexityLowerBound",
        "clayProblemSolved",
        "continuumPdeProofCertified",
        "finiteTimeSingularityEstablished",
        "globalRegularityEstablished",
        "heatFlowIntegralComputed",
        "intervalArithmeticUsed",
        "navierStokesSimulation",
        "pdeNecessityEstablished",
        "runtimeBenchmark",
        "universalRuntimeLowerBound",
    ):
        if boundary.get(key) is not False:
            raise RuntimeError("R0.73S certificate overclaims " + key)
    for key in (
        "exactFiniteFormulaDiagnosticOnly",
        "predeclaredStrictSubsetNoGo",
        "quadraticAutocorrelationUpperBoundChecked",
    ):
        if boundary.get(key) is not True:
            raise RuntimeError("R0.73S certificate lost finite diagnostic fact " + key)
    if (
        diagnostic.get("rowCount") != 43
        or independent.get("rowCount") != 43
        or certificate.get("rowCount") != 43
        or validation.get("rowCount") != 43
        or manifest.get("checkInventory") != {
            "independent": 54, "primary": 226, "structural": 289,
        }
    ):
        raise RuntimeError("R0.73S certificate source-data counts drifted")
    formulas = certificate.get("formulaStatements")
    required_formulas = {
        "autocorrelation": "C(h)=sum_k a(k+h) dot conjugate(a(k))=Fourier(|f|^2)(h)",
        "autocorrelationSupport": "D_C=cardinality(support(C))",
        "differenceSet": "D_delta=cardinality(S-S), with D_C<=D_delta",
        "exactQuartic": "Q=sum_h |C(h)|^2=||f||_4^4",
        "matchedProxy": "scaled alpha_m*N^(-1/2)*(A_m*Q_m)^(1/6)",
        "quadraticCertificate": "||f||_6^6 <= A*Q, A=sum_h |C(h)|",
        "supportSurrogates": "A <= min(M*E^2, sqrt(D_C*Q)) <= min(M*E^2, sqrt(|S-S|*Q))",
    }
    if not isinstance(formulas, dict) or any(
        formulas.get(key) != value for key, value in required_formulas.items()
    ):
        raise RuntimeError("R0.73S certificate formula ledger drifted")
    run_package_verifier(
        f"{base}/validate_certificate.py", ["--verify-only"],
        "R0.73S certificate scientific validator",
    )
    run_package_verifier(
        f"{base}/seal_package.py",
        ["--source-commit", ANALYTIC_SOURCE_COMMIT, "--verify-only"],
        "R0.73S certificate provenance seal",
    )
    return manifest


def validate_figure_package(certificate_manifest: dict) -> dict:
    base = FIGURE_SOURCE_RELATIVE
    manifest = strict_json_file(f"{base}/manifest.json", "R0.73S figure manifest")
    config = strict_json_file(f"{base}/config.json", "R0.73S figure config")
    contract = strict_json_file(f"{base}/contract.json", "R0.73S figure contract")
    results = strict_json_file(f"{base}/results.json", "R0.73S figure results")
    validation = strict_json_file(f"{base}/validation.json", "R0.73S figure validation")
    if (
        manifest.get("schemaVersion") != "r073s-quadratic-certificate-figure-manifest-v1"
        or manifest.get("release") != RELEASE
        or manifest.get("figureId") != FIGURE_ID
        or manifest.get("status") != "sealed"
        or manifest.get("finalSeal") is not True
        or manifest.get("sourceCommitAssigned") is not True
        or manifest.get("sourceCommit") != ANALYTIC_SOURCE_COMMIT
        or manifest.get("visualQaConfirmed") is not True
        or certificate_manifest.get("sourceCommit") != ANALYTIC_SOURCE_COMMIT
    ):
        raise RuntimeError("R0.73S figure is not final-sealed to the analytic commit")
    if (
        config.get("schemaVersion") != "r073s-quadratic-certificate-figure-config-v1"
        or config.get("figureId") != FIGURE_ID
        or results.get("schemaVersion") != "r073s-quadratic-certificate-results-v1"
        or results.get("figureId") != FIGURE_ID
        or results.get("rowCount") != 179
    ):
        raise RuntimeError("R0.73S figure result/configuration drifted")
    checks = validation.get("checks")
    if (
        validation.get("schemaVersion") != "r073s-quadratic-certificate-figure-validation-v1"
        or validation.get("figureId") != FIGURE_ID
        or validation.get("allChecksPass") is not True
        or validation.get("sourceCommit") != ANALYTIC_SOURCE_COMMIT
        or not isinstance(checks, list)
        or not checks
        or not all(isinstance(row, dict) and row.get("pass") is True for row in checks)
    ):
        raise RuntimeError("R0.73S figure validation provenance drifted")
    boundary = contract.get("claimBoundary")
    if not isinstance(boundary, dict):
        raise RuntimeError("R0.73S figure claim boundary is absent")
    for key in (
        "fittedScalingLaw",
        "navierStokesSimulation",
        "complexityLowerBound",
        "necessaryRegularityCriterion",
        "unsafeDynamics",
        "finiteTimeSingularity",
        "arbitraryL2SmallDataSafe",
        "clayProblemSolved",
    ):
        if boundary.get(key) is not False:
            raise RuntimeError("R0.73S figure overclaims " + key)
    for key in ("exactFormulaAndUpperBoundOnly", "sharpnessLiftHasZeroConvection"):
        if boundary.get(key) is not True:
            raise RuntimeError("R0.73S figure lost diagnostic fact " + key)
    recorded = manifest.get("files")
    if not isinstance(recorded, list) or manifest.get("boundFileCount") != len(recorded):
        raise RuntimeError("R0.73S figure sealed inventory drifted")
    by_name = {
        row.get("path"): row for row in recorded
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    }
    if len(by_name) != len(recorded):
        raise RuntimeError("R0.73S figure sealed inventory contains duplicate paths")
    for name, row in by_name.items():
        payload = current_regular_bytes(f"{base}/{name}")
        if row.get("bytes") != len(payload) or row.get("sha256") != sha256(payload):
            raise RuntimeError("R0.73S figure manifest is not byte-bound: " + name)
    output_by_name = {
        row.get("path"): row for row in results.get("outputs", [])
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    }
    for name in ("figure.pdf", "figure.svg", "figure.png"):
        payload = current_regular_bytes(f"{base}/{name}")
        row = output_by_name.get(name)
        if row is None or row.get("bytes") != len(payload) or row.get("sha256") != sha256(payload):
            raise RuntimeError("R0.73S figure output is not result-bound: " + name)
    dependency_root = os.environ.get(
        "R073S_FIGURE_DEPS", "/Users/kasifa/.cache/codex-runtimes/r073s-figure-python"
    )
    executable = os.environ.get(
        "R073S_FIGURE_PYTHON",
        "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3",
    )
    if not Path(dependency_root).is_dir() or not Path(executable).is_file():
        raise RuntimeError(
            "R0.73S figure verifier runtime missing; set R073S_FIGURE_DEPS and R073S_FIGURE_PYTHON"
        )
    run_package_verifier(
        f"{base}/validate.py",
        ["--deps", dependency_root, "--final", "--verify-only"],
        "R0.73S figure",
        executable=executable,
    )
    return manifest


def certificate_summary() -> dict[str, object]:
    root = ROOT / "research/certificates/r073s"
    manifest_path = root / "manifest.json"
    if not manifest_path.is_file() or manifest_path.is_symlink():
        return {"present": root.is_dir(), "finalSeal": False, "status": "missing-manifest"}
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {"present": True, "finalSeal": False, "status": "invalid-manifest"}
    final = (
        manifest.get("release") == RELEASE
        and manifest.get("status") == "sealed"
        and manifest.get("finalSeal") is True
        and manifest.get("sourceCommitAssigned") is True
        and isinstance(manifest.get("sourceCommit"), str)
        and re.fullmatch(r"[0-9a-f]{40}", manifest["sourceCommit"]) is not None
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
        manifest.get("release") == RELEASE
        and manifest.get("figureId") == FIGURE_ID
        and manifest.get("status") == "sealed"
        and manifest.get("finalSeal") is True
        and manifest.get("sourceCommitAssigned") is True
        and isinstance(manifest.get("sourceCommit"), str)
        and re.fullmatch(r"[0-9a-f]{40}", manifest["sourceCommit"]) is not None
        and manifest.get("visualQaConfirmed") is True
    )
    return {
        "present": True,
        "formal": formal,
        "status": manifest.get("status"),
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
    value = decode_baseline("public/notes/r0-73r.html")
    description = (
        "研究笔记 R0.73S：完整二次自相关充分证书、差集支撑尖锐障碍、"
        "低摘要不可辨识性与零非线性边界。"
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
        f'<meta property="og:image" content="https://kasifa.github.io/assets/r073s/{FIGURE_ID}.png">',
        "note OG image",
    )
    value = replace_regex(
        value, r'<title>.*?</title>',
        f'<title>{html.escape(content.document_title_en)}</title>', "note title",
    )
    value = replace_once(value, "/i18n-en.js?v=1.58", "/i18n-en.js?v=1.59", "note i18n")
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
        f'<div>研究笔记 R0.73S · {html.escape(content.date)}<br>'
        '<a href="/">返回研究主页</a></div></footer>',
        "note footer",
    )
    assert_public_html(value, "R0.73S note")
    if "/note-retro.css" not in value or value.count(FIGURE_ID) < 4:
        raise RuntimeError("R0.73S note lost retro stylesheet or formal figure links")
    return value


def build_recap(content: ReleaseContent) -> str:
    value = decode_baseline("public/recap-r0-61-r0-73r.html")
    value = value.replace("/i18n-en.js?v=1.58", "/i18n-en.js?v=1.59")
    value = value.replace("R0.61–R0.73R", "R0.61–R0.73S")
    value = value.replace("R0.61 到 R0.73R", "R0.61 到 R0.73S")
    value = value.replace("R0.69P–R0.73R", "R0.69P–R0.73S")
    value = value.replace("R0.70A–R0.73R", "R0.70A–R0.73S")
    value = value.replace("回顾截止节点：R0.73R", "回顾截止节点：R0.73S")
    value = value.replace("收录节点：134", "收录节点：135")
    value = value.replace("回顾截止时公开笔记：194", "回顾截止时公开笔记：195")
    value = value.replace("134 节", "135 节").replace("134 个节点", "135 个节点")
    value = value.replace("96 个版本", "97 个版本").replace("96 节", "97 节")
    value = value.replace("72 个满足", "73 个满足").replace("72 节", "73 节")
    value = value.replace("53 个阶段", "54 个阶段")
    value = value.replace("53 个研究阶段", "54 个研究阶段")
    value = value.replace("<strong>134</strong>", "<strong>135</strong>")
    value = value.replace("<strong>96</strong>", "<strong>97</strong>")
    value = value.replace("<strong>72</strong>", "<strong>73</strong>")
    value = replace_regex(
        value, r'(<header class="hero">.*?<p class="lead">)(.*?)(</p>)',
        lambda match: match.group(1) + match.group(2) + " "
        + html.escape(content.recap_zh) + match.group(3),
        "recap hero current result",
    )
    value = replace_regex(
        value, r'<meta name="description" content="[^"]*">',
        '<meta name="description" content="R0.60 之后的完整研究回顾：R0.61 到 '
        'R0.73S 共 135 个节点；最新一节分开经典自相关不等式、本地有限证书、'
        '差集障碍与低摘要 no-go。">',
        "recap description",
    )
    value = replace_regex(
        value, r'<meta property="og:description" content="[^"]*">',
        '<meta property="og:description" content="54 个阶段、135 个节点：从约化递推和环带排除'
        '到二次自相关证书、尖锐差集障碍与低摘要不可辨识性。">',
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
        '<span class="node-ref"><a href="/notes/r0-73s.html">R0.73S</a>'
        '<span class="node-state kind-closed">闭</span></span>'
    )
    value = replace_once(
        value,
        '          </div>\n        </section>\n\n        <section id="retained"',
        f'            {node}\n          </div>\n        </section>\n\n        <section id="retained"',
        "recap node append",
    )
    retained = (
        '<li>R0.73S 把逐壳六次矩充分上界降到完整二次自相关，并分开三条事实：'
        '基础不等式与差集 Nikolskii 分支属于经典直接推论；选定移位尾界与有限证书可精确复算；'
        '固定宽比环带上的差集因子和低摘要不可辨识性给出严格 no-go。'
        '这不包含运行时间下界、Navier--Stokes 仿真或 Clay 结论。</li>'
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
        '<h2>经典碰撞、本地证书与信息障碍已经分开</h2>'
        f'<p>{html.escape(content.recap_zh)}</p>'
        '<p>不能把 135 个节点或 97 个公开版本解释成 Clay 完成比例。'
        '完整有限自相关确实决定六次矩；被否定的是预先声明的严格子集或低阶摘要。'
        '任意三维初值全局正则性仍为 OPEN。</p></section>',
        "recap current value",
    )
    value = replace_regex(
        value, r'<section id="next">.*?</section>',
        '<section id="next"><div class="section-no">05 / 下一步</div>'
        f'<h2>{html.escape(content.next_release)}：动态逐壳自相关预算</h2>'
        f'<p>{html.escape(content.next_gate_zh)}</p></section>',
        "recap next gate",
    )
    value = replace_regex(
        value, r'<section id="claims">.*?</section>',
        '<section id="claims"><div class="section-no">06 / 说明边界</div>'
        '<h2>经典结果、本地有限结论和开放问题分开列示</h2>'
        '<p>R0.70A–R0.73S 的 97 节已公开；73 节完整封存；24 节旧档待回补。</p>'
        f'<p>{html.escape(CLOSED_LEDGER)}</p>'
        f'<p>{html.escape(FINITE_LEDGER)}</p>'
        f'<p>{html.escape(OPEN_LEDGER)}</p>'
        '<p>R0.73S 的有限公式证书和正式附图只复算自相关、矩与反例族；'
        '它们不计算热流积分，不运行 Navier--Stokes，也不建立复杂度下界。NOT CLAY。</p>'
        '</section>',
        "recap exact boundary",
    )
    value = replace_regex(
        value, r'<section id="reproduce">.*?</section>',
        '<section id="reproduce"><div class="section-no">07 / 原始资料</div>'
        '<h2>逐节笔记、证明、审计、证书、附图和历史回顾</h2>'
        '<p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · '
        '<a href="/recap-r0-61-r0-73r.html">保留 R0.73R 历史回顾</a> · '
        '<a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · '
        '<a href="/notes/r0-73s.html">打开最新节点 R0.73S</a></p>'
        '<p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073s_report-source.md">查看 canonical report</a> · '
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073s_quadratic_autocorrelation_certificate.md">查看解析证明</a> · '
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073s_primary_literature_audit.md">查看一手文献审计</a> · '
        '<a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073s">查看有限证书</a> · '
        f'<a href="/assets/r073s/{FIGURE_ID}.pdf">下载期刊附图</a> · '
        '<a href="/recap-r0-61-r0-73s.pdf">下载同步 PDF</a></p>'
        '<p>经典结论由一手来源承担；本地解析证明承担 no-go；有限诊断只作可复现错误探测。'
        'NOT CLAY。</p></section>',
        "recap reproduction",
    )
    value = value.replace("/recap-r0-61-r0-73r.pdf", "/recap-r0-61-r0-73s.pdf")
    value = value.replace("R0.73R 回顾", "R0.73S 回顾")
    for stale in ("<strong>134</strong>", "<strong>96</strong>", "<strong>72</strong>"):
        if stale in value:
            raise RuntimeError("R0.73S recap retained stale metric " + stale)
    if value.count('<article class="phase">') != 54:
        raise RuntimeError("R0.73S recap must contain exactly 54 phase articles")
    if "53 个阶段" in value or "53 个研究阶段" in value:
        raise RuntimeError("R0.73S recap retained a stale displayed phase count")
    assert_public_html(value, "R0.73S recap")
    return value


def latest_spotlight(content: ReleaseContent) -> str:
    return (
        '<section class="route-overview latest-release-spotlight" id="latest-release" '
        'aria-labelledby="latest-release-title"><div class="route-overview-inner">'
        '<header class="route-map-header"><div>'
        f'<p class="eyebrow">LATEST RELEASE · R0.73S · {html.escape(content.date)}</p>'
        f'<h2 class="route-map-title" id="latest-release-title">{html.escape(content.public_title_zh)}</h2>'
        f'<p class="route-map-intro">{html.escape(content.home_zh)}</p></div>'
        '<nav class="route-map-actions" aria-label="最新发布快捷入口">'
        '<a class="route-map-latest" href="/notes/r0-73s.pdf">阅读最新 R0.73S 研究笔记 →</a>'
        '<a href="/recap-r0-61-r0-73s.html">135 节累计回顾</a>'
        '<a href="/notes/">195 篇研究笔记总索引</a>'
        '<a href="#r073s">查看首页完整 R0.73S 卡片</a></nav></header>'
        '<div class="route-legend" aria-label="最新发布计数">'
        '<span><i class="route-legend-mark kept" aria-hidden="true"></i>'
        'R0.70A–R0.73S · 97 节已公开</span>'
        '<span><i class="route-legend-mark kept" aria-hidden="true"></i>73 节完整封存</span>'
        '<span><i class="route-legend-mark current" aria-hidden="true"></i>'
        '当前端点 R0.73S</span></div></div></section>'
    )


def update_home(content: ReleaseContent) -> str:
    value = decode_baseline("public/research-review.html")
    value = value.replace('data-site-version="1.58"', 'data-site-version="1.59"')
    value = value.replace("/i18n-en.js?v=1.58", "/i18n-en.js?v=1.59")
    value = value.replace("/site-refresh.js?v=1.58", "/site-refresh.js?v=1.59")
    value = replace_regex(
        value, r'<section class="route-overview latest-release-spotlight".*?</section>',
        latest_spotlight(content), "home latest spotlight",
    )
    marker = '<div class="task-one" id="r073r" data-release="r073r"'
    value = replace_once(value, marker, content.home_card + "\n          " + marker, "home card insert")
    value = value.replace("<strong>194</strong>公开研究笔记", "<strong>195</strong>公开研究笔记")
    value = value.replace("<strong>v1.58</strong>网页版本", "<strong>v1.59</strong>网页版本")
    value = value.replace("<strong>R0.73R</strong>最新研究节点", "<strong>R0.73S</strong>最新研究节点")
    value = value.replace(
        "<strong>shellwise phase certificate / classical Besov boundary</strong>当前方向",
        "<strong>quadratic autocorrelation certificate / exact no-go boundary</strong>当前方向",
    )
    value = value.replace("NEXT · R0.73S", "NEXT · R0.73T")
    value = replace_regex(
        value, r'<h3>R0\.73S 下一接口</h3><p>.*?</p>',
        f'<h3>{html.escape(content.next_release)} 下一接口</h3>'
        f'<p>{html.escape(content.next_gate_zh)}</p>',
        "home next interface",
    )
    value = value.replace(
        "R0.70A–R0.73R：96 节已公开，72 节完整封存",
        "R0.70A–R0.73S：97 节已公开，73 节完整封存",
    )
    value = value.replace("Research topology · R0.1–R0.73R", "Research topology · R0.1–R0.73S")
    value = value.replace(
        '<a class="route-map-latest" href="#r073r">跳到首页 R0.73R 卡片 →</a>',
        '<a class="route-map-latest" href="#r073s">跳到首页 R0.73S 卡片 →</a>',
    )
    value = value.replace(
        '/recap-r0-61-r0-73r.html">阅读 R0.60 之后的累计回顾',
        '/recap-r0-61-r0-73s.html">阅读 R0.60 之后的累计回顾',
    )
    value = value.replace("/recap-r0-61-r0-73r.html", "/recap-r0-61-r0-73s.html")
    value = value.replace("/recap-r0-61-r0-73r.pdf", "/recap-r0-61-r0-73s.pdf")
    value = value.replace("综述 v1.58 ·", "综述 v1.59 ·")
    value = value.replace(
        '<span class="route-range">R0.69P–R0.73R</span>',
        '<span class="route-range">R0.69P–R0.73S</span>',
    )
    value = value.replace(
        "R0.73R：经典热--Besov、逐壳相位证书与零非线性边界已分列",
        "R0.73S：二次自相关证书、尖锐差集障碍与低摘要 no-go 已分列",
    )
    value = value.replace('<span>R0.72R–R0.73R：</span>', '<span>R0.72R–R0.73S：</span>')
    value = value.replace(
        "→ shellwise phase certificate</p>",
        "→ shellwise phase certificate → quadratic autocorrelation certificate</p>",
    )
    current_paragraph = (
        f'<p>{html.escape(content.recap_zh)} '
        '<span>quadratic autocorrelation certificate</span>；'
        '<span>difference-support obstruction</span>；'
        '<span>low-summary non-identifiability</span>。'
        '基础不等式直接落在经典 Nikolskii 与 Fourier 估计内。</p>'
    )
    value = replace_once(
        value, '              <details class="tree-notes" open>',
        "              " + current_paragraph + '\n              <details class="tree-notes" open>',
        "home route current paragraph",
    )
    value = value.replace('<summary>展开 104 篇公开笔记</summary>', '<summary>展开 105 篇公开笔记</summary>')
    value = value.replace('aria-label="R0.69P–R0.73R"', 'aria-label="R0.69P–R0.73S"')
    value = replace_once(
        value,
        '                  <a class="milestone" href="/notes/r0-73r.html">R0.73R</a>',
        '                  <a class="milestone" href="/notes/r0-73r.html">R0.73R</a>\n'
        '                  <a class="milestone" href="/notes/r0-73s.html">R0.73S</a>',
        "home route R0.73S link",
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
        '<p class="eyebrow">累计回顾 R0.61–R0.73S · 2026-08-31</p>'
        '<h3>R0.60 recap 之后的累计回顾收录 135 个节点；全站现有 195 篇公开研究笔记</h3>'
        '<p>累计回顾现分 54 个阶段，完整保留 R0.61–R0.73S；最新节点分开记录经典碰撞、'
        '二次自相关证书、尖锐差集障碍、低摘要不可辨识性、有限公式诊断和正式附图。</p>'
        '<p>R0.70A–R0.73S 共 97 个版本已公开；73 个按当前 formal-figure 合同完整封存，'
        '24 个旧版附图档案仍列入回补清单。</p>'
        f'<p><strong>阶段判断：</strong>&nbsp;{html.escape(content.recap_zh)} '
        '任意三维初值全局正则性与 Clay 保持 OPEN。</p>'
        '<p><a href="/recap-r0-61-r0-73s.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · '
        '<a href="/recap-r0-61-r0-73s.pdf">下载同步 PDF</a></p></div>'
    )
    value = replace_regex(
        value, r'<div class="task-one" id="post-r060-recap".*?</div>',
        recap_card, "home cumulative recap card",
    )
    value = value.replace(
        "本站 R0.69P–R0.73R 路线放在同一张图中",
        "本站 R0.69P–R0.73S 路线放在同一张图中",
    )
    for stale in (
        "Research topology · R0.1–R0.73R",
        "累计回顾收录 134 个节点；全站现有 194 篇公开研究笔记",
        '<summary>展开 104 篇公开笔记</summary>',
        "<strong>v1.58</strong>网页版本",
        "<strong>R0.73R</strong>最新研究节点",
        'data-site-version="1.58"',
        "/site-refresh.js?v=1.58",
        '<h3>R0.73S 下一接口</h3>',
    ):
        if stale in value:
            raise RuntimeError("R0.73S home retained stale latest marker " + stale)
    assert_public_html(value, "R0.73S home")
    return value


def update_literature(content: ReleaseContent) -> str:
    value = decode_baseline("public/literature-review.html")
    value = value.replace("/i18n-en.js?v=1.58", "/i18n-en.js?v=1.59")
    value = value.replace("文献综述 v1.58 ·", "文献综述 v1.59 ·")
    marker = '<span class="route-r073r-deck-update">'
    start = value.find(marker)
    end = value.find("</span>", start)
    if start < 0 or end < 0:
        raise RuntimeError("literature R0.73R deck marker missing")
    end += len("</span>")
    value = value[:end] + content.literature_update + value[end:]
    value = value.replace("/recap-r0-61-r0-73r.html", "/recap-r0-61-r0-73s.html")
    value = value.replace("134 节", "135 节")
    value = value.replace("R0.69P–R0.73R", "R0.69P–R0.73S")
    route_step = (
        '<div class="route-step kept"><header><b>R0.73S</b>'
        '<strong>quadratic autocorrelation certificate and exact no-go boundary</strong></header>'
        f'<p>{html.escape(content.recap_zh)} <a href="/notes/r0-73s.html">研究笔记</a> '
        '<a href="/recap-r0-61-r0-73s.html">当前累计回顾</a> '
        '<a href="#r073s-boundary">文献边界</a></p></div>'
        '<div class="route-step pause"><header><b>开放接口 · R0.73T</b>'
        '<strong>dynamic autocorrelation budget across shells</strong></header>'
        '<p>下一步检查逐壳动态自相关预算能否与非线性通量相容；'
        '任意初值全局正则性与 Clay 保持 OPEN。</p></div>'
    )
    value = replace_regex(
        value,
        r'<div class="route-step pause"><header><b>开放接口 · R0\.73S</b>.*?</div>',
        route_step, "literature current route step",
    )
    literature_boundary = (
        '<h3 id="r073s-boundary">R0.73S 的二次自相关证书与直接经典碰撞边界</h3>'
        '<p><a href="https://doi.org/10.1017/S1446788700038878">Nessel--Wilmes 1978</a>'
        '的 Theorem 1 直接给出有限谱 Nikolskii 支撑因子；'
        '<a href="https://doi.org/10.1017/S0004972700044427">Edwards 1972</a>'
        '提供紧 Abel 群 Hausdorff--Young 背景。基础自相关不等式与差集分支属于经典直接推论。</p>'
        '<p><a href="https://doi.org/10.1109/TIT.1985.1057071">Høholdt--Jensen--Justesen 1985</a>、'
        '<a href="https://doi.org/10.1007/s00041-004-3049-y">Doche--Habsieger 2005</a>和'
        '<a href="https://doi.org/10.1016/j.aim.2017.09.022">Rodgers 2018</a>'
        '覆盖 Rudin--Shapiro 的相关、merit factor 与矩行为。'
        '本地工作不承担新颖性或优先权声明。</p>'
        '<div class="boundary"><strong>R0.73S 的主张边界</strong>'
        f'<p>{html.escape(CLOSED_LEDGER)}</p>'
        f'<p>{html.escape(FINITE_LEDGER)}</p>'
        f'<p>{html.escape(OPEN_LEDGER)}</p>'
        '<p>一手来源承担经典碰撞；本地证明只承担有限充分证书与严格 no-go；'
        '完整有限自相关仍能决定六次矩。NOT CLAY。</p></div>'
    )
    value = replace_once(
        value, '          <ol class="criteria">',
        "          " + literature_boundary + '\n          <ol class="criteria">',
        "literature R0.73S boundary",
    )
    if "开放接口 · R0.73T" not in value or 'id="r073s-boundary"' not in value:
        raise RuntimeError("R0.73S literature route/boundary was not advanced")
    assert_public_html(value, "R0.73S literature")
    for token in ("VERIFIED_CLASSICAL", "NOT_PROVED", "优先权"):
        if token not in value:
            raise RuntimeError("R0.73S literature lost boundary token " + token)
    return value


def build_manifest_outputs(content: ReleaseContent) -> dict[Path, bytes]:
    release = strict_json_bytes(
        git_bytes(RELEASE_BASELINE_COMMIT, "research/release-manifest.json"),
        "release manifest",
    )
    for key, expected in R073R_BASELINE.items():
        if release.get(key) != expected:
            raise RuntimeError("R0.73R release-manifest baseline drift: " + key)
    release.update({
        **R073S_TARGET,
        "latestReleaseGate": "tests/r073s-autocorrelation-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r073s-release.test.mjs",
    })

    site = strict_json_bytes(
        git_bytes(RELEASE_BASELINE_COMMIT, "public/site-version.json"), "site version"
    )
    expected_site = {
        "schemaVersion": "research-site-version-v1",
        "version": "1.58",
        "latestRelease": "R0.73R",
        "publicHtmlNoteCount": 194,
        "publishedDate": "2026-08-31",
    }
    if site != expected_site:
        raise RuntimeError("R0.73R site-version baseline drift")
    site.update({
        "version": SITE_VERSION,
        "latestRelease": RELEASE,
        "publicHtmlNoteCount": 195,
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
    if state != ("r073r", 96, 72, 24):
        raise RuntimeError("R0.73R formal-archive baseline drift")
    for key in ("publishedReleases", "formalSealedReleases"):
        rows = inventory.get(key)
        if not isinstance(rows, list) or rows[-1:] != ["r073r"] or "r073s" in rows:
            raise RuntimeError("formal archive is not append-only: " + key)
        rows.append("r073s")
    inventory.update({
        "latestPublishedRelease": "r073s",
        "publishedReleaseCount": 97,
        "formalSealedReleaseCount": 73,
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
        ROOT / "VERSION": b"1.59\n",
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
        with tempfile.TemporaryDirectory(prefix="r073s-index-") as temporary:
            notes = Path(temporary)
            for relative in git_paths(RELEASE_BASELINE_COMMIT, "public/notes"):
                name = Path(relative).name
                if re.fullmatch(r"r0-[0-9a-z]+\.(?:html|pdf)", name):
                    (notes / name).write_bytes(git_bytes(RELEASE_BASELINE_COMMIT, relative))
            note_index.ROOT, note_index.PUBLIC, note_index.NOTES = ROOT, PUBLIC, notes
            note_index.OUTPUT = notes / "index.html"
            existing = [note_index.parse_note(path) for path in note_index.note_files()]
            if len(existing) != 194 or existing[0].slug != "r0-73r":
                raise RuntimeError("R0.73S note-index baseline is not exact")
            latest = note_index.Note(
                slug="r0-73s",
                code=RELEASE,
                title=content.document_title_en.split("｜", 1)[-1].strip(),
                major=73,
                has_pdf=True,
            )
            note_index.json = TargetJson
            note_index.latest_recap_href = lambda: "/recap-r0-61-r0-73s.html"
            value = note_index.render([latest, *existing])
    finally:
        note_index.json = old_json
        note_index.latest_recap_href = old_recap
        note_index.ROOT, note_index.PUBLIC, note_index.NOTES, note_index.OUTPUT = old_paths
    assert_public_html(value, "R0.73S note index", require_boundary=False)
    if "prefers-color-scheme: dark" not in value:
        raise RuntimeError("R0.73S index lost automatic dark theme")
    return value


def formal_figure_payloads(source: Path) -> dict[str, bytes]:
    source_manifest = strict_json_file(
        f"{FIGURE_SOURCE_RELATIVE}/manifest.json", "R0.73S sealed figure manifest"
    )
    if (
        source_manifest.get("schemaVersion") != "r073s-quadratic-certificate-figure-manifest-v1"
        or source_manifest.get("release") != RELEASE
        or source_manifest.get("figureId") != FIGURE_ID
        or source_manifest.get("status") != "sealed"
        or source_manifest.get("finalSeal") is not True
        or source_manifest.get("sourceCommitAssigned") is not True
        or source_manifest.get("sourceCommit") != ANALYTIC_SOURCE_COMMIT
        or source_manifest.get("visualQaConfirmed") is not True
    ):
        raise RuntimeError("R0.73S source figure is not a commit-bound sealed package")
    actual = sorted(
        path.name for path in source.iterdir()
        if path.is_file() and not path.is_symlink()
    )
    required = {
        "manifest.json", "SHA256SUMS", "figure.pdf", "figure.svg", "figure.png",
        "qa-pdf.png", "qa-final-size.png", "qa-grayscale.png",
        "source-data.csv", "results.json", "validation.json", "contract.json",
        "config.json", "environment.json", "caption.md", "requirements.txt",
        "progress.ndjson", "resource-log.ndjson", "plot.py",
    }
    if not required.issubset(actual):
        raise RuntimeError(
            "R0.73S formal figure inventory is incomplete: "
            + repr(sorted(required - set(actual)))
        )
    recorded = source_manifest.get("files")
    if not isinstance(recorded, list):
        raise RuntimeError("R0.73S sealed figure file inventory is absent")
    expected_recorded = set(actual) - {"manifest.json", "SHA256SUMS"}
    by_name = {
        row.get("path"): row for row in recorded
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    }
    if set(by_name) != expected_recorded:
        raise RuntimeError("R0.73S sealed figure inventory does not cover package files")
    for name, row in by_name.items():
        payload = current_regular_bytes(f"{FIGURE_SOURCE_RELATIVE}/{name}")
        if row.get("bytes") != len(payload) or row.get("sha256") != sha256(payload):
            raise RuntimeError("R0.73S sealed figure record is not byte-bound: " + name)

    environment = strict_json_file(
        f"{FIGURE_SOURCE_RELATIVE}/environment.json", "R0.73S figure environment"
    )
    contract = strict_json_file(
        f"{FIGURE_SOURCE_RELATIVE}/contract.json", "R0.73S figure contract"
    )
    results = strict_json_file(
        f"{FIGURE_SOURCE_RELATIVE}/results.json", "R0.73S figure results"
    )
    result_rows = {
        row.get("path"): row for row in results.get("outputs", [])
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    }

    def record(name: str, schema: str) -> dict[str, object]:
        payload = current_regular_bytes(f"{FIGURE_SOURCE_RELATIVE}/{name}")
        return {"path": name, "schema": schema, "bytes": len(payload), "sha256": sha256(payload)}

    outputs: list[dict[str, object]] = []
    for suffix in ("pdf", "svg", "png"):
        name = f"figure.{suffix}"
        payload = current_regular_bytes(f"{FIGURE_SOURCE_RELATIVE}/{name}")
        result_row = result_rows.get(name)
        if result_row is None or result_row.get("sha256") != sha256(payload):
            raise RuntimeError("R0.73S figure result ledger lost " + name)
        row: dict[str, object] = {
            "path": name, "bytes": len(payload), "sha256": sha256(payload),
        }
        if suffix == "png":
            row["dpi"] = 600
        outputs.append(row)
    public_assets = [
        {
            "path": f"public/assets/r073s/{FIGURE_ID}.{suffix}",
            "bytes": row["bytes"], "sha256": row["sha256"],
        }
        for suffix, row in zip(("pdf", "svg", "png"), outputs)
    ]
    formal = {
        "schemaVersion": "research-figure-manifest-v1",
        "figureId": FIGURE_ID,
        "release": RELEASE,
        "status": "formal",
        "publicationStatus": "published",
        "analyticalQuestion": (
            "What does the complete quadratic autocorrelation certificate control, "
            "and which support or low-summary factors cannot be removed?"
        ),
        "supportedClaim": (
            "Exact formula audit of the autocorrelation upper bound, its sharp "
            "difference-support obstruction, and the low-summary no-go."
        ),
        "createdAt": environment.get("createdAt"),
        "git": {
            "repository": "https://github.com/Kasifa/Kasifa.github.io.git",
            "sourceCommit": ANALYTIC_SOURCE_COMMIT,
            "certificateCommit": FINITE_PACKAGE_COMMIT,
            "dirtyAtCertifiedRun": False,
        },
        "computation": {
            "kind": "exact-formula-audit",
            "configuration": "config.json",
            "precision": "exact integer/rational formulas with deterministic rendering",
            "solver": "closed-form finite audit",
            "formalCommand": "python plot.py --render-preseal; python validate.py --final --verify-only",
            "scientificWallTimeSeconds": 0.930649958900176,
            "monitoring": {
                "enabled": True,
                "progressLog": "progress.ndjson",
                "resourceLog": "resource-log.ndjson",
            },
        },
        "compute": {
            "host": environment.get("host"),
            "operatingSystem": environment.get("operatingSystem"),
            "cpu": f"{environment.get('machine')} / {environment.get('logicalCpuCount')} logical CPUs",
            "memoryGiB": environment.get("memoryGiB"),
            "processes": environment.get("processes"),
            "threadsPerProcess": environment.get("threadsPerProcess"),
            "gpu": environment.get("gpu"),
            "dgxUsed": environment.get("dgxUsed"),
        },
        "environment": {
            "python": environment.get("python"),
            "packagesLock": "requirements.txt",
            "packages": environment.get("packages"),
        },
        "data": [
            record("source-data.csv", "r073s-quadratic-certificate-figure-source-v1"),
            record("results.json", "r073s-quadratic-certificate-results-v1"),
            record("validation.json", "r073s-quadratic-certificate-figure-validation-v1"),
            record("progress.ndjson", "progress-ndjson-v1"),
            record("resource-log.ndjson", "resource-log-ndjson-v1"),
        ],
        "sourceData": [],
        "figure": {"outputs": outputs},
        "caption": {"english": "caption.md"},
        "qa": {
            "status": "passed",
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
        "claimBoundary": contract.get("claimBoundary"),
        "sourceSeal": source_manifest,
        "publication": {
            "archiveDirectory": f"public/{FIGURE_ARCHIVE_RELATIVE}",
            "directory": "public/assets/r073s",
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
        raise RuntimeError("R0.73S formal figure staging changed the package inventory")
    return payloads


def stage_figure_assets(staged: dict[Path, bytes]) -> None:
    source = ROOT / FIGURE_SOURCE_RELATIVE
    if not source.is_dir() or source.is_symlink() or not (source / "manifest.json").is_file():
        raise RuntimeError("R0.73S formal figure package is incomplete")
    payloads = formal_figure_payloads(source)
    for name, payload in payloads.items():
        staged[ROOT / FIGURE_ARCHIVE_RELATIVE / name] = payload
        staged[PUBLIC / FIGURE_ARCHIVE_RELATIVE / name] = payload
    for suffix in ("pdf", "svg", "png"):
        staged[PUBLIC / f"assets/r073s/{FIGURE_ID}.{suffix}"] = payloads[f"figure.{suffix}"]


def build_staged(content: ReleaseContent) -> dict[Path, bytes]:
    staged: dict[Path, bytes] = {}
    stage_figure_assets(staged)
    staged[PUBLIC / "notes/r0-73s.html"] = build_note(content).encode("utf-8")
    staged[PUBLIC / "recap-r0-61-r0-73s.html"] = build_recap(content).encode("utf-8")
    staged[PUBLIC / "research-review.html"] = update_home(content).encode("utf-8")
    staged[PUBLIC / "literature-review.html"] = update_literature(content).encode("utf-8")
    staged.update(build_manifest_outputs(content))
    staged[PUBLIC / "notes/index.html"] = build_note_index(
        content, staged[PUBLIC / "site-version.json"]
    ).encode("utf-8")
    missing = [relative for relative in CORE_TARGET_OUTPUTS if ROOT / relative not in staged]
    if missing:
        raise RuntimeError("R0.73S staged transaction omitted: " + repr(missing))
    for path, payload in staged.items():
        if path.suffix == ".html":
            assert_public_html(
                payload.decode("utf-8"), path.name,
                require_boundary=path != PUBLIC / "notes/index.html",
            )
    return staged


def commit_transaction(staged: dict[Path, bytes]) -> None:
    ordered = sorted(staged)
    created_directories: list[Path] = []
    for path in ordered:
        try:
            path.relative_to(ROOT)
        except ValueError as exc:
            raise RuntimeError("transaction target escaped repository") from exc
        if path.exists() and (not path.is_file() or path.is_symlink()):
            raise RuntimeError("unsafe transaction target: " + str(path))
        missing: list[Path] = []
        cursor = path.parent
        while not cursor.exists():
            missing.append(cursor)
            cursor = cursor.parent
        if not cursor.is_dir() or cursor.is_symlink():
            raise RuntimeError("unsafe transaction parent: " + str(cursor))
        for directory in reversed(missing):
            directory.mkdir()
            created_directories.append(directory)

    nonce = f"{os.getpid()}-{os.urandom(8).hex()}"
    rows: list[dict[str, object]] = []
    try:
        for index, target in enumerate(ordered):
            temporary = target.parent / f".{target.name}.r073s-{nonce}-{index}.tmp"
            backup = target.parent / f".{target.name}.r073s-{nonce}-{index}.bak"
            if temporary.exists() or backup.exists():
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
                os.replace(row["target"], row["backup"])
                row["backed_up"] = True
        for row in rows:
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
        "targetAccounting": R073S_TARGET,
        "baselineAccounting": R073R_BASELINE,
        "canonicalSources": len(content.source_sha256),
        "canonicalSourcesPlanned": len(CANONICAL_SOURCE_PATHS),
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
    verify_pinned_paths_exist(RELEASE_BASELINE_COMMIT, BASELINE_EXACT_PATHS, "R0.73R baseline")
    verify_commit_paths(ANALYTIC_SOURCE_COMMIT, ANALYTIC_EXACT_PATHS, "R0.73S analytic source")
    verify_commit_trees(FINITE_PACKAGE_COMMIT, FINITE_EXACT_ROOTS, "R0.73S finite package")
    verify_commit_trees(FIGURE_PACKAGE_COMMIT, FIGURE_EXACT_ROOTS, "R0.73S formal figure package")
    verify_commit_paths(FINAL_CONTENT_COMMIT, FINAL_CONTENT_EXACT_PATHS, "R0.73S final content")
    verify_commit_paths(RELEASE_SOURCE_COMMIT, RELEASE_SOURCE_EXACT_PATHS, "R0.73S release source")
    certificate_manifest = validate_certificate_package()
    validate_figure_package(certificate_manifest)
    content = load_release_content(ROOT)
    if not content.publication_ready:
        raise RuntimeError("R0.73S canonical content is not publication-ready: " + repr(content.readiness_failures))
    if certificate_summary().get("finalSeal") is not True:
        raise RuntimeError("R0.73S finite certificate lacks its final immutable-source seal")
    if figure_summary().get("formal") is not True:
        raise RuntimeError("R0.73S formal figure package is absent or unsealed")
    if not PUBLIC_TRANSACTION_IMPLEMENTED:
        raise RuntimeError("R0.73S public transaction implementation is disabled")
    return content


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate or explicitly apply the fail-closed R0.73S release transaction."
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
        raise SystemExit("R0.73S canonical-source gate failed: " + str(exc)) from exc
