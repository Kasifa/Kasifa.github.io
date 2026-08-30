#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fail-closed R0.73N GitHub Pages release skeleton.

The mathematical copy comes from ``r073n_release_content.py``.  This file
owns only release binding, deterministic page assembly, accounting, and the
transaction boundary.  Six immutable commits must be filled in, in the
declared ancestry order, before ``--check-only`` or ``--apply`` can read a
public baseline.  ``--source-dry-run`` is intentionally read-only and may be
used while those pins are still zero.

The HTML/PDF translation and PDF-binding stages are separate.  Consequently
an HTML apply, when eventually authorized, still leaves the publication gate
incomplete until those later stages pass.
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

from r073n_release_content import (
    CANONICAL_SOURCE_PATHS,
    FIGURE_ARCHIVE_RELATIVE,
    FIGURE_ID,
    FIGURE_SOURCE_RELATIVE,
    R073M_BASELINE,
    R073N_TARGET,
    RELEASE,
    SITE_VERSION,
    CanonicalSourceError,
    ReleaseContent,
    load_release_content,
)


ROOT = Path(os.environ.get(
    "R073N_RELEASE_ROOT", Path(__file__).resolve().parents[1]
)).resolve()
PUBLIC = ROOT / "public"
ZERO_COMMIT = "0" * 40

# Binding order (oldest to newest): published R0.73M baseline -> analytic
# source -> finite package -> formal figure package -> final reader-facing
# content -> release-source code.  All six pins remain deliberately sealed
# shut until their exact commits are
# reviewed and substituted in a later, explicit binding step.
ANALYTIC_SOURCE_COMMIT = "23526aa667aba1880a768ff4c1db35536edce737"
FINITE_PACKAGE_COMMIT = "1ff95492df564501af30cc1bc2fc1e193cd22f6f"
FIGURE_PACKAGE_COMMIT = "1ff95492df564501af30cc1bc2fc1e193cd22f6f"
RELEASE_BASELINE_COMMIT = "623afb9210fa65027fdd7ae97ee0af107116d798"
FINAL_CONTENT_COMMIT = "1ff95492df564501af30cc1bc2fc1e193cd22f6f"
RELEASE_SOURCE_COMMIT = "1a1a471dd4139a97ca5a073b43fc0ce670a15368"

BINDING_ORDER = (
    ("R0.73M release baseline", RELEASE_BASELINE_COMMIT),
    ("analytic source", ANALYTIC_SOURCE_COMMIT),
    ("finite package", FINITE_PACKAGE_COMMIT),
    ("figure package", FIGURE_PACKAGE_COMMIT),
    ("final content", FINAL_CONTENT_COMMIT),
    ("R0.73N release source", RELEASE_SOURCE_COMMIT),
)

ANALYTIC_EXACT_PATHS = (
    "research/r073n_problem_freeze.md",
    "research/r073n_fixed_background_no_go_proof.md",
    "research/r073n_scaling_obstruction.md",
    "research/r073n_independent_analytic_audit.md",
    "research/r073n_adversarial_audit.md",
    "research/r073n_literature_audit.md",
    "research/r073n_claim_source_ledger.md",
    "research/r073n_gap_matrix.md",
)
FINITE_EXACT_ROOTS = ("research/certificates/r073n",)
FINAL_CONTENT_EXACT_PATHS = (
    "research/r073n_finite_diagnostic_audit.md",
    "research/r073n_report-source.md",
    "research/r073n_bilingual_dictionary.md",
)
FIGURE_EXACT_ROOTS = (FIGURE_SOURCE_RELATIVE,)
BASELINE_EXACT_PATHS = (
    "VERSION",
    "research/release-manifest.json",
    "research/formal-archive-inventory.json",
    "public/site-version.json",
    "public/notes/r0-73m.html",
    "public/recap-r0-61-r0-73m.html",
    "public/research-review.html",
    "public/literature-review.html",
    "public/notes/index.html",
)
RELEASE_SOURCE_EXACT_PATHS = (
    "scripts/r073n_release_content.py",
    "scripts/generate_r073n_release.py",
    "scripts/add-r073n-translations.mjs",
    "scripts/bind-r073n-pdfs.mjs",
    "tests/r073n-fixed-background-no-go-gate.test.mjs",
    "tests/r073n-release.test.mjs",
)

CORE_TARGET_OUTPUTS = (
    "public/notes/r0-73n.html",
    "public/recap-r0-61-r0-73n.html",
    "public/research-review.html",
    "public/literature-review.html",
    "public/notes/index.html",
    "public/site-version.json",
    "research/release-manifest.json",
    "research/formal-archive-inventory.json",
    "VERSION",
)
LATER_STAGE_OUTPUTS = (
    "public/notes/r0-73n.pdf",
    "public/recap-r0-61-r0-73n.pdf",
    "research/r073n_pdf_bindings.json",
    "translations/en.json",
    "public/i18n-en.js",
    "scripts/i18n-snapshots/r073n-missing.json",
)
PUBLICATION_STAGE_ORDER = (
    "freeze-r073m-baseline",
    "freeze-analytic-source",
    "seal-finite-package-to-analytic-source",
    "seal-figure-package-to-analytic-source",
    "freeze-final-report-dictionary-and-finite-audit",
    "freeze-release-source-and-fill-normalized-pin-slot",
    "apply-html-manifest-and-figure-transaction",
    "capture-review-and-apply-translations",
    "render-synchronized-note-and-recap-pdfs",
    "bind-html-pdf-hashes-and-titles",
    "run-publication-tests-then-deploy",
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


def strict_json_file(relative: str, label: str) -> dict:
    return strict_json_bytes(current_regular_bytes(relative), label)


def git(*arguments: str, text: bool = False) -> bytes | str:
    result = subprocess.run(
        ["git", *arguments], cwd=ROOT, check=True,
        capture_output=True, text=text,
    )
    return result.stdout


def git_bytes(commit: str, relative: str) -> bytes:
    return git("show", f"{commit}:{relative}")  # type: ignore[return-value]


def git_paths(commit: str, relative: str) -> list[str]:
    output = git("ls-tree", "-r", "--name-only", commit, "--", relative, text=True)
    return sorted(row for row in str(output).splitlines() if row)


def require_commit(commit: str, label: str) -> None:
    if commit == ZERO_COMMIT:
        raise RuntimeError(
            f"{label}: unsealed 40-zero commit pin; binding remains fail-closed"
        )
    if re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        raise RuntimeError(label + ": expected a full lowercase Git SHA")
    result = subprocess.run(
        ["git", "cat-file", "-t", commit], cwd=ROOT,
        capture_output=True, text=True,
    )
    if result.returncode or result.stdout.strip() != "commit":
        raise RuntimeError(label + ": pin is not a commit object")


def ensure_commits_ready() -> None:
    for label, commit in BINDING_ORDER:
        require_commit(commit, label)
    for (older_label, older), (newer_label, newer) in zip(BINDING_ORDER, BINDING_ORDER[1:]):
        result = subprocess.run(
            ["git", "merge-base", "--is-ancestor", older, newer], cwd=ROOT,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        if result.returncode:
            raise RuntimeError(
                f"binding order violated: {older_label} is not an ancestor of {newer_label}"
            )


def current_regular_bytes(relative: str) -> bytes:
    path = ROOT / relative
    if not path.is_file() or path.is_symlink():
        raise RuntimeError(relative + ": expected a regular nonsymlink file")
    return path.read_bytes()


def verify_exact_paths(commit: str, paths: tuple[str, ...], label: str) -> None:
    for relative in paths:
        current = current_regular_bytes(relative)
        if current != git_bytes(commit, relative):
            raise RuntimeError(label + ": worktree differs from pin at " + relative)


def normalized_release_generator(payload: bytes) -> bytes:
    try:
        value = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError("R0.73N release generator is not UTF-8") from exc
    value, count = re.subn(
        r'(?m)^RELEASE_SOURCE_COMMIT = (?:ZERO_COMMIT|"[0-9a-f]{40}")$',
        'RELEASE_SOURCE_COMMIT = "__NORMALIZED_RELEASE_SOURCE_COMMIT__"',
        value,
    )
    if count != 1:
        raise RuntimeError("R0.73N generator must expose exactly one release-source pin")
    return value.encode("utf-8")


def verify_release_source(commit: str) -> None:
    for relative in RELEASE_SOURCE_EXACT_PATHS:
        current = current_regular_bytes(relative)
        frozen = git_bytes(commit, relative)
        if relative == "scripts/generate_r073n_release.py":
            current = normalized_release_generator(current)
            frozen = normalized_release_generator(frozen)
        if current != frozen:
            raise RuntimeError("release source: worktree differs from pin at " + relative)


def verify_exact_roots(commit: str, roots: tuple[str, ...], label: str) -> None:
    for root in roots:
        path = ROOT / root
        if path.is_file():
            verify_exact_paths(commit, (root,), label)
            continue
        if not path.is_dir() or path.is_symlink():
            raise RuntimeError(label + ": missing real directory " + root)
        current = sorted(
            item.relative_to(ROOT).as_posix()
            for item in path.rglob("*") if item.is_file() and not item.is_symlink()
        )
        frozen = git_paths(commit, root)
        if current != frozen:
            raise RuntimeError(label + ": directory inventory drift at " + root)
        verify_exact_paths(commit, tuple(current), label)


def run_package_verifier(relative: str, arguments: list[str], label: str) -> None:
    command = [sys.executable, "-B", str(ROOT / relative), *arguments]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        detail = (result.stderr or result.stdout).strip()
        raise RuntimeError(label + " --verify-only failed: " + detail[-2000:])


def require_pass_payload(payload: dict, label: str) -> None:
    if payload.get("status") != "passed" or payload.get("allChecksPass") is not True:
        raise RuntimeError(label + ": status/allChecksPass drift")
    checks = payload.get("checks")
    if isinstance(checks, dict) and (not checks or not all(value is True for value in checks.values())):
        raise RuntimeError(label + ": one or more checks failed")


def validate_certificate_package() -> dict:
    base = "research/certificates/r073n"
    manifest = strict_json_file(f"{base}/manifest.json", "R0.73N certificate manifest")
    config = strict_json_file(f"{base}/config.json", "R0.73N certificate config")
    diagnostic = strict_json_file(f"{base}/diagnostic.json", "R0.73N diagnostic")
    independent = strict_json_file(
        f"{base}/independent_validation.json", "R0.73N independent validation"
    )
    certificate = strict_json_file(f"{base}/certificate.json", "R0.73N certificate")
    validation = strict_json_file(f"{base}/validation.json", "R0.73N certificate validation")
    if (
        manifest.get("schemaVersion") != "r073n-finite-strain-manifest-v1"
        or manifest.get("release") != RELEASE
        or manifest.get("status") != "sealed"
        or manifest.get("finalSeal") is not True
        or manifest.get("sourceCommitAssigned") is not True
        or manifest.get("sourceCommit") != ANALYTIC_SOURCE_COMMIT
        or manifest.get("allPrerequisiteChecksPass") is not True
    ):
        raise RuntimeError("R0.73N certificate is not final-sealed to the analytic commit")
    for payload, label in (
        (diagnostic, "R0.73N diagnostic"),
        (independent, "R0.73N independent validation"),
        (certificate, "R0.73N certificate"),
        (validation, "R0.73N certificate validation"),
    ):
        require_pass_payload(payload, label)
    boundary = config.get("claimBoundary")
    if not isinstance(boundary, dict) or any(
        payload.get("claimBoundary") != boundary
        for payload in (manifest, diagnostic, independent, certificate, validation)
    ):
        raise RuntimeError("R0.73N certificate claim boundaries disagree")
    for key in (
        "finiteComputationProvesContinuumEnergyEstimate",
        "finiteComputationProvesFixedMemberStabilityTube",
        "finiteComputationProvesInheritedActionInterval",
        "fullThreeDimensionalFPSH3L2StabilityCertified",
        "singleFixedBackgroundLyapunovInstabilityCertified",
        "sharpFamilyLipschitzExponentCertified",
        "transverseCriticalNormGrowthCertified",
        "finiteTimeSingularityCertified",
        "clayProblemSolved",
    ):
        if boundary.get(key) is not False:
            raise RuntimeError("R0.73N certificate overclaims " + key)
    if certificate.get("sourceData") != {
        **certificate.get("sourceData", {}),
        "totalRows": 605,
        "strainSamples": 241,
        "cumulativeSamples": 243,
        "markedBasepointSamples": 121,
    }:
        raise RuntimeError("R0.73N certificate source-data counts drifted")
    validator_arguments = ["--verify-only"]
    dependency_root = os.environ.get("R073N_CERTIFICATE_DEPS", "/tmp/r073n-deps")
    if not Path(dependency_root).is_dir():
        raise RuntimeError(
            "R0.73N certificate dependency directory missing; set R073N_CERTIFICATE_DEPS"
        )
    validator_arguments[0:0] = ["--deps", dependency_root]
    run_package_verifier(
        f"{base}/validate_certificate.py",
        validator_arguments,
        "R0.73N certificate scientific validator",
    )
    run_package_verifier(
        f"{base}/seal_package.py",
        ["--verify-only", "--source-commit", ANALYTIC_SOURCE_COMMIT],
        "R0.73N certificate",
    )
    return manifest


def validate_figure_package(certificate_manifest: dict) -> dict:
    base = FIGURE_SOURCE_RELATIVE
    manifest = strict_json_file(f"{base}/manifest.json", "R0.73N figure manifest")
    config = strict_json_file(f"{base}/config.json", "R0.73N figure config")
    contract = strict_json_file(f"{base}/contract.json", "R0.73N figure contract")
    results = strict_json_file(f"{base}/results.json", "R0.73N figure results")
    validation = strict_json_file(f"{base}/validation.json", "R0.73N figure validation")
    if (
        manifest.get("schemaVersion") != "r073n-finite-strain-figure-manifest-v1"
        or manifest.get("figureId") != FIGURE_ID
        or manifest.get("release") != RELEASE
        or manifest.get("status") != "sealed"
        or manifest.get("finalSeal") is not True
        or manifest.get("sourceCommitAssigned") is not True
        or manifest.get("sourceCommit") != ANALYTIC_SOURCE_COMMIT
        or manifest.get("upstreamCertificateSourceCommit") != ANALYTIC_SOURCE_COMMIT
        or manifest.get("publicationStatus") != "not-published"
        or manifest.get("allPrerequisiteChecksPass") is not True
        or certificate_manifest.get("sourceCommit") != ANALYTIC_SOURCE_COMMIT
    ):
        raise RuntimeError("R0.73N figure is not final-sealed to the analytic commit")
    if (
        results.get("status") != "passed-sealed"
        or results.get("allChecksPass") is not True
        or results.get("finalSeal") is not True
        or results.get("sourceCommitAssigned") is not True
        or results.get("sourceCommit") != ANALYTIC_SOURCE_COMMIT
    ):
        raise RuntimeError("R0.73N figure results are not sealed")
    require_pass_payload(validation, "R0.73N figure validation")
    if (
        validation.get("finalSeal") is not True
        or validation.get("sourceCommitAssigned") is not True
        or validation.get("sourceCommit") != ANALYTIC_SOURCE_COMMIT
    ):
        raise RuntimeError("R0.73N figure validation provenance drifted")
    boundary = contract.get("claimBoundary")
    if (
        not isinstance(boundary, dict)
        or config.get("claimBoundary") != boundary
        or results.get("claimBoundary") != boundary
        or manifest.get("claimBoundary") != boundary
    ):
        raise RuntimeError("R0.73N figure claim boundaries disagree")
    for key in (
        "finiteComputationProvesContinuumEnergyEstimate",
        "finiteComputationProvesFixedMemberStabilityTube",
        "finiteComputationProvesInheritedActionInterval",
        "fullThreeDimensionalFPSH3L2StabilityCertified",
        "singleFixedBackgroundLyapunovInstabilityCertified",
        "sharpFamilyLipschitzExponentCertified",
        "transverseCriticalNormGrowthCertified",
        "finiteTimeSingularityCertified",
        "clayProblemSolved",
    ):
        if boundary.get(key) is not False:
            raise RuntimeError("R0.73N figure overclaims " + key)
    inventory = manifest.get("packageInventory")
    if (
        not isinstance(inventory, dict)
        or inventory.get("expectedFileCount") != 25
        or inventory.get("sourceFileCount") != 10
        or inventory.get("generatedFileCount") != 15
        or inventory.get("manifestBoundFileCount") != 23
        or inventory.get("sha256SumsLineCount") != 24
    ):
        raise RuntimeError("R0.73N figure package inventory drifted")
    output_rows = manifest.get("figure", {}).get("outputs", [])
    output_by_name = {
        row.get("path"): row for row in output_rows if isinstance(row, dict)
    }
    for suffix in ("pdf", "svg", "png"):
        name = f"figure.{suffix}"
        payload = current_regular_bytes(f"{base}/{name}")
        row = output_by_name.get(name)
        if row is None or row.get("bytes") != len(payload) or row.get("sha256") != sha256(payload):
            raise RuntimeError("R0.73N figure master is not manifest-bound: " + name)
    verifier_arguments = ["--verify-only", "--source-commit", ANALYTIC_SOURCE_COMMIT]
    dependency_root = os.environ.get("R073N_FIGURE_DEPS", "/tmp/r073n-deps")
    if not Path(dependency_root).is_dir():
        raise RuntimeError(
            "R0.73N figure dependency directory missing; set R073N_FIGURE_DEPS"
        )
    verifier_arguments[0:0] = ["--deps", dependency_root]
    run_package_verifier(
        f"{base}/validate.py", verifier_arguments, "R0.73N figure"
    )
    return manifest


def final_content_readiness(content: ReleaseContent) -> tuple[bool, list[str]]:
    observed: dict[str, list[tuple[str, str]]] = {}
    by_path: dict[str, dict[str, list[str]]] = {}
    for relative in FINAL_CONTENT_EXACT_PATHS:
        value = current_regular_bytes(relative).decode("utf-8")
        by_path[relative] = {}
        for key, state in re.findall(
            r"(?m)^([A-Za-z][A-Za-z0-9]*)=([A-Z0-9][A-Z0-9_]*)\s*$", value
        ):
            observed.setdefault(key, []).append((relative, state))
            by_path[relative].setdefault(key, []).append(state)
    required = {
        "finiteDiagnosticValidation": "PASS",
        "finiteDiagnosticPackage": "CLOSED",
        "sourceCommitAssigned": "TRUE",
        "finalSeal": "TRUE",
        "formalFigurePackage": "PASS",
        "publicReleaseContent": "READY",
    }
    failures: list[str] = []
    for key, expected in required.items():
        rows = observed.get(key, [])
        values = {state for _, state in rows}
        if values != {expected}:
            rendered = ",".join(f"{path}:{state}" for path, state in rows) or "MISSING"
            failures.append(f"{key} expected {expected}; observed {rendered}")
        required_paths = (
            FINAL_CONTENT_EXACT_PATHS
            if key != "publicReleaseContent"
            else (
                "research/r073n_report-source.md",
                "research/r073n_bilingual_dictionary.md",
            )
        )
        missing_paths = [
            path for path in required_paths
            if set(by_path[path].get(key, [])) != {expected}
        ]
        if missing_paths:
            failures.append(key + " missing exact per-file coverage: " + ",".join(missing_paths))
    if "publicRelease" in observed:
        rendered = ",".join(f"{path}:{state}" for path, state in observed["publicRelease"])
        failures.append("stale publicRelease token: " + rendered)
    if content.next_release.lower() != "r0.73o":
        failures.append("nextRelease=" + content.next_release)
    if "PENDING" in content.status:
        failures.append("reportStatus=PENDING")
    return not failures, failures


def verify_inputs() -> ReleaseContent:
    ensure_commits_ready()
    verify_exact_paths(ANALYTIC_SOURCE_COMMIT, ANALYTIC_EXACT_PATHS, "analytic source")
    verify_exact_roots(FINITE_PACKAGE_COMMIT, FINITE_EXACT_ROOTS, "finite package")
    verify_exact_roots(FIGURE_PACKAGE_COMMIT, FIGURE_EXACT_ROOTS, "figure package")
    verify_exact_paths(FINAL_CONTENT_COMMIT, FINAL_CONTENT_EXACT_PATHS, "final content")
    verify_exact_paths(RELEASE_BASELINE_COMMIT, BASELINE_EXACT_PATHS, "release baseline")
    verify_release_source(RELEASE_SOURCE_COMMIT)
    certificate_manifest = validate_certificate_package()
    validate_figure_package(certificate_manifest)
    content = load_release_content(ROOT)
    ready, failures = final_content_readiness(content)
    if not ready:
        raise RuntimeError("R0.73N final content is not release-ready: " + ", ".join(failures))
    return content


def decode_baseline(relative: str) -> str:
    try:
        return git_bytes(RELEASE_BASELINE_COMMIT, relative).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError(relative + ": frozen baseline is not UTF-8") from exc


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
    tokens = ["R0.73N", "/i18n-en.js?v=1.54"]
    if require_boundary:
        tokens.append("NOT CLAY")
    for token in tokens:
        if token not in value:
            raise RuntimeError(label + ": missing token " + token)


def note_toc(content: ReleaseContent) -> str:
    rows = "".join(
        f'<li><a href="#{section.anchor}">{section.number:02d} · '
        f'{section.title}</a></li>' for section in content.sections
    )
    rows += '<li><a href="#release-boundary">B · exact boundary</a></li>'
    rows += '<li><a href="#figure">F · journal figure</a></li>'
    rows += '<li><a href="#reproduce">R · reproduction</a></li>'
    return f'<aside class="toc"><strong>CONTENTS</strong><ol>{rows}</ol></aside>'


def build_note(content: ReleaseContent) -> str:
    value = decode_baseline("public/notes/r0-73m.html")
    description = "研究笔记 R0.73N：固定成员有限应变稳定、族转移障碍、审计边界与独立有限诊断。"
    value = replace_regex(value, r'<meta name="description" content="[^"]*">',
                          f'<meta name="description" content="{description}">', "note description")
    value = replace_regex(value, r'<meta property="og:title" content="[^"]*">',
                          f'<meta property="og:title" content="{html.escape(content.document_title_en, quote=True)}">', "note OG title")
    value = replace_regex(value, r'<meta property="og:description" content="[^"]*">',
                          f'<meta property="og:description" content="{html.escape(content.lead_zh, quote=True)}">', "note OG description")
    value = replace_regex(value, r'<meta property="og:image" content="[^"]*">',
                          f'<meta property="og:image" content="https://kasifa.github.io/assets/r073n/{FIGURE_ID}.png">', "note OG image")
    value = replace_regex(value, r'<title>.*?</title>',
                          f'<title>{html.escape(content.document_title_en)}</title>', "note title")
    value = replace_once(value, "/i18n-en.js?v=1.53", "/i18n-en.js?v=1.54", "note i18n")
    navigation = ''.join(
        f'<a href="#{section.anchor}">{section.title}</a>' for section in content.sections
    ) + '<a href="#figure">journal figure</a><a href="#release-boundary">exact boundary</a><a href="#reproduce">reproduction</a><a href="/">返回主页</a>'
    value = replace_regex(
        value,
        r'(<header class="bar"><div class="bar-inner">\s*<a class="brand".*?</a>\s*)<nav>.*?</nav>',
        lambda match: match.group(1) + '<nav>' + navigation + '</nav>',
        "note navigation",
    )
    value = replace_regex(value, r'<header class="hero">.*?</header>', content.note_hero, "note hero")
    value = replace_regex(value, r'<aside class="toc">.*?</aside>', note_toc(content), "note TOC")
    value = replace_regex(value, r'<article>.*?</article>', content.note_article, "note article")
    value = replace_regex(
        value, r'<footer>.*?</footer>',
        '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>'
        '按原编号区分定理、有限计算与开放问题。</div><div>研究笔记 R0.73N · '
        f'{content.date}<br><a href="/">返回研究主页</a></div></footer>', "note footer",
    )
    assert_public_html(value, "R0.73N note")
    if "/note-retro.css" not in value:
        raise RuntimeError("R0.73N note lost retro stylesheet")
    return value


def build_recap(content: ReleaseContent) -> str:
    value = decode_baseline("public/recap-r0-61-r0-73m.html")
    value = value.replace("/i18n-en.js?v=1.53", "/i18n-en.js?v=1.54")
    value = value.replace("R0.61–R0.73M", "R0.61–R0.73N")
    value = value.replace("R0.61 到 R0.73M", "R0.61 到 R0.73N")
    value = value.replace("R0.69P–R0.73M", "R0.69P–R0.73N")
    value = value.replace("R0.70A–R0.73M", "R0.70A–R0.73N")
    value = value.replace("回顾截止节点：R0.73M", "回顾截止节点：R0.73N")
    value = value.replace("收录节点：129", "收录节点：130")
    value = value.replace("回顾截止时公开笔记：189", "回顾截止时公开笔记：190")
    value = value.replace("129 节", "130 节").replace("129 个节点", "130 个节点")
    value = value.replace("91 个版本", "92 个版本").replace("91 节", "92 节")
    value = value.replace("67 个满足", "68 个满足").replace("67 节", "68 节")
    value = value.replace("<strong>129</strong>", "<strong>130</strong>")
    value = value.replace("<strong>91</strong>", "<strong>92</strong>")
    value = value.replace("<strong>67</strong>", "<strong>68</strong>")
    value = replace_regex(
        value,
        r'(<header class="hero">.*?<p class="lead">)(.*?)(</p>)',
        lambda match: match.group(1) + match.group(2) + " "
        + html.escape(content.recap_zh) + match.group(3),
        "recap hero current result",
    )
    value = replace_regex(
        value,
        r'<meta name="description" content="[^"]*">',
        '<meta name="description" content="R0.60 之后的完整研究回顾：R0.61 到 '
        'R0.73N 共 130 个节点；最新一节分开固定成员稳定性与变背景族非一致放大。">',
        "recap description",
    )
    value = replace_regex(
        value,
        r'<meta property="og:description" content="[^"]*">',
        '<meta property="og:description" content="48 个阶段、130 个节点：从约化递推和环带排除到固定成员有限应变稳定性与族转移障碍。">',
        "recap OG description",
    )
    value = replace_once(value, "          </div>\n        </section>\n\n        <section id=\"node-index\"",
                         content.recap_phase + "\n          </div>\n        </section>\n\n        <section id=\"node-index\"", "recap phase append")
    node = '<span class="node-ref"><a href="/notes/r0-73n.html">R0.73N</a><span class="node-state kind-closed">闭</span></span>'
    value = replace_once(value, "          </div>\n        </section>\n\n        <section id=\"retained\"",
                         f"            {node}\n          </div>\n        </section>\n\n        <section id=\"retained\"", "recap node append")
    retained = (
        '<li>R0.73N 把 R0.73M 的变背景族结论与固定成员问题严格分开：每个固定有限 '
        '\\(\\Lambda\\) 具有正的全三维同步 \\(H^3,H^3\\) 稳定管，平面子系统具有真正的 '
        '\\(L^2\\) 初值小性；全三维 FPS \\(H^3,L^2\\) 仍为 OPEN。</li>'
    )
    value = replace_once(
        value,
        '          </ul>\n          <p>这些结果可以分别整理成条件定理、精确恒等式、反例或计算辅助分析。',
        f'            {retained}\n          </ul>\n          <p>这些结果可以分别整理成条件定理、精确恒等式、反例或计算辅助分析。',
        "recap retained result append",
    )
    value = replace_regex(
        value,
        r'<section id="value">.*?</section>',
        '<section id="value"><div class="section-no">04 / 目前的判断</div>'
        '<h2>变背景族与固定成员的量词边界已经分开</h2>'
        f'<p>{html.escape(content.recap_zh)}</p>'
        '<p>不能把 130 个节点或 92 个公开版本解释成 Clay 完成比例。'
        '本节关闭的是一条错误的族到单成员推理，不是一般固定背景不稳定性、横向三维增长、'
        '有限时奇性或全局正则性。</p></section>',
        "recap current value",
    )
    value = replace_regex(
        value,
        r'<section id="next">.*?</section>',
        '<section id="next"><div class="section-no">05 / 下一步</div>'
        f'<h2>{html.escape(content.next_release)}：冻结结构不同的固定背景候选问题</h2>'
        f'<p>{html.escape(content.math_next_gate_zh)}</p></section>',
        "recap next gate",
    )
    value = replace_regex(
        value,
        r'<section id="claims">.*?</section>',
        '<section id="claims"><div class="section-no">06 / 说明边界</div>'
        '<h2>连续定理、有限诊断和开放问题分开列示</h2>'
        '<p>R0.70A–R0.73N 的 92 节已公开；68 节完整封存；24 节旧档待回补。</p>'
        f'<p>{html.escape(content.closed_ledger)}</p>'
        f'<p>{html.escape(content.finite_ledger)}</p>'
        f'<p>{html.escape(content.open_ledger)}</p>'
        '<p>605 行 R0.73N 有限源数据和正式附图只作复现与错误探测；不认证连续证明、'
        '固定成员最优半径、横向三维、奇性或 Clay。NOT CLAY。</p></section>',
        "recap exact boundary",
    )
    value = replace_regex(
        value,
        r'<section id="reproduce">.*?</section>',
        '<section id="reproduce"><div class="section-no">07 / 原始资料</div>'
        '<h2>逐节笔记、证明、审计、证书、附图和历史回顾</h2>'
        '<p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · '
        '<a href="/recap-r0-61-r0-73m.html">保留 R0.73M 历史回顾</a> · '
        '<a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · '
        '<a href="/notes/r0-73n.html">打开最新节点 R0.73N</a></p>'
        '<p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073n_report-source.md">查看 canonical report</a> · '
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073n_fixed_background_no_go_proof.md">查看连续证明</a> · '
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073n_literature_audit.md">查看有界文献审计</a> · '
        '<a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073n">查看有限诊断包</a> · '
        f'<a href="/assets/r073n/{FIGURE_ID}.pdf">下载期刊附图</a> · '
        '<a href="/recap-r0-61-r0-73n.pdf">下载同步 PDF</a></p>'
        '<p>连续定理由解析证明承担；有限诊断只作可复现错误探测。</p></section>',
        "recap reproduction",
    )
    value = value.replace("/recap-r0-61-r0-73m.pdf", "/recap-r0-61-r0-73n.pdf")
    value = value.replace("R0.73M 回顾", "R0.73N 回顾")
    for stale in ("<strong>129</strong>", "<strong>91</strong>", "<strong>67</strong>"):
        if stale in value:
            raise RuntimeError("R0.73N recap retained stale metric " + stale)
    assert_public_html(value, "R0.73N recap")
    return value


def update_home(content: ReleaseContent) -> str:
    value = decode_baseline("public/research-review.html")
    value = value.replace("/i18n-en.js?v=1.53", "/i18n-en.js?v=1.54")
    value = replace_regex(value, r'<section class="route-overview latest-release-spotlight".*?</section>',
                          content.latest_spotlight, "home latest spotlight")
    marker = '<div class="task-one" id="r073m" data-release="r073m"'
    value = replace_once(value, marker, content.home_card + "\n          " + marker, "home card insert")
    value = value.replace("<strong>189</strong>公开研究笔记", "<strong>190</strong>公开研究笔记")
    value = value.replace("NEXT · R0.73N", "NEXT · R0.73O")
    value = value.replace("R0.70A–R0.73M：91 节已公开，67 节完整封存",
                          "R0.70A–R0.73N：92 节已公开，68 节完整封存")
    value = value.replace("Research topology · R0.1–R0.73M", "Research topology · R0.1–R0.73N")
    value = value.replace('<a class="route-map-latest" href="#r073m">跳到首页 R0.73M 卡片 →</a>',
                          '<a class="route-map-latest" href="#r073n">跳到首页 R0.73N 卡片 →</a>')
    value = value.replace('/recap-r0-61-r0-73m.html">阅读 R0.60 之后的累计回顾',
                          '/recap-r0-61-r0-73n.html">阅读 R0.60 之后的累计回顾')
    value = value.replace('<span class="route-range">R0.69P–R0.73M</span>',
                          '<span class="route-range">R0.69P–R0.73N</span>')
    value = value.replace('R0.73M：prescribed-action 平面非线性固定距离偏离已闭合',
                          'R0.73N：固定成员有限应变稳定性与族转移障碍已闭合')
    value = value.replace('<span>R0.72R–R0.73M：</span>', '<span>R0.72R–R0.73N：</span>')
    value = value.replace(
        '→ prescribed-action planar nonlinear fixed-distance departure</p>',
        '→ prescribed-action planar nonlinear fixed-distance departure → fixed-member finite-strain stability / family-transfer obstruction</p>',
    )
    current_paragraph = (
        f'<p>{html.escape(content.recap_zh)}<span>fixed-member finite-strain stability</span>；'
        '<span>family-transfer obstruction</span>。有限诊断与正式附图只作复现与错误探测。</p>'
    )
    value = replace_once(
        value,
        '              <details class="tree-notes" open>',
        '              ' + current_paragraph + '\n              <details class="tree-notes" open>',
        "home route current paragraph",
    )
    value = value.replace('<summary>展开 99 篇公开笔记</summary>', '<summary>展开 100 篇公开笔记</summary>')
    value = value.replace('aria-label="R0.69P–R0.73M"', 'aria-label="R0.69P–R0.73N"')
    value = replace_once(
        value,
        '                  <a class="milestone" href="/notes/r0-73m.html">R0.73M</a>',
        '                  <a class="milestone" href="/notes/r0-73m.html">R0.73M</a>\n'
        '                  <a class="milestone" href="/notes/r0-73n.html">R0.73N</a>',
        "home route R0.73N link",
    )
    value = replace_regex(
        value,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>'
        + html.escape(content.recap_zh) + ' 下一关是 ' + html.escape(content.next_release)
        + '：' + html.escape(content.math_next_gate_zh) + '</span></div>',
        "home focus summary",
    )
    recap_card = (
        '<div class="task-one" id="post-r060-recap" style="margin-top:2rem">'
        '<p class="eyebrow">累计回顾 R0.61–R0.73N · 2026-08-31</p>'
        '<h3>R0.60 recap 之后的累计回顾收录 130 个节点；全站现有 190 篇公开研究笔记</h3>'
        '<p>累计回顾现分 48 个阶段，完整保留 R0.61–R0.73N；最新节点分开记录固定成员连续证明、'
        '两份解析审计、有界文献边界、有限诊断和正式附图。</p>'
        '<p>R0.70A–R0.73N 共 92 个版本已公开；68 个按当前 formal-figure 合同完整封存，'
        '24 个旧版附图档案仍列入回补清单。</p>'
        f'<p><strong>阶段判断：</strong>&nbsp;{html.escape(content.recap_zh)} '
        '横向三维临界增长、奇性与 Clay 保持 OPEN。</p>'
        '<p><a href="/recap-r0-61-r0-73n.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · '
        '<a href="/recap-r0-61-r0-73n.pdf">下载同步 PDF</a></p></div>'
    )
    value = replace_regex(
        value,
        r'<div class="task-one" id="post-r060-recap".*?</div>',
        recap_card,
        "home cumulative recap card",
    )
    value = value.replace(
        '<h3>固定背景 Lyapunov 不稳定性的可行性与障碍审计</h3><p>辨认变背景 family-level theorem 能否转化成固定基流问题；不预设闭合，结构性失败就封存为 no-go。横向三维与 Clay 保持为更后的 OPEN 接口。</p>',
        f'<h3>冻结结构不同的固定背景候选问题</h3><p>{html.escape(content.math_next_gate_zh)}</p>',
    )
    for stale in (
        "Research topology · R0.1–R0.73M",
        "累计回顾收录 129 个节点；全站现有 189 篇公开研究笔记",
        '<summary>展开 99 篇公开笔记</summary>',
    ):
        if stale in value:
            raise RuntimeError("R0.73N home retained stale latest marker " + stale)
    assert_public_html(value, "R0.73N home")
    return value


def update_literature(content: ReleaseContent) -> str:
    value = decode_baseline("public/literature-review.html")
    value = value.replace("/i18n-en.js?v=1.53", "/i18n-en.js?v=1.54")
    marker = '<span class="route-r073m-deck-update">'
    start = value.find(marker)
    end = value.find("</span>", start)
    if start < 0 or end < 0:
        raise RuntimeError("literature R0.73M deck marker missing")
    end += len("</span>")
    value = value[:end] + content.literature_update + value[end:]
    value = value.replace("/recap-r0-61-r0-73m.html", "/recap-r0-61-r0-73n.html")
    value = value.replace("129 节", "130 节")
    value = value.replace("R0.69P–R0.73M", "R0.69P–R0.73N")
    assert_public_html(value, "R0.73N literature")
    if "bounded" not in value.lower() or "优先权" not in value:
        raise RuntimeError("R0.73N literature lost bounded/non-priority boundary")
    return value


def build_manifest_outputs(content: ReleaseContent) -> dict[Path, bytes]:
    release = strict_json_bytes(
        git_bytes(RELEASE_BASELINE_COMMIT, "research/release-manifest.json"),
        "release manifest",
    )
    for key, expected in R073M_BASELINE.items():
        if release.get(key) != expected:
            raise RuntimeError("R0.73M release-manifest baseline drift: " + key)
    release.update({
        **R073N_TARGET,
        "latestReleaseGate": "tests/r073n-fixed-background-no-go-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r073n-release.test.mjs",
    })

    site = strict_json_bytes(
        git_bytes(RELEASE_BASELINE_COMMIT, "public/site-version.json"), "site version"
    )
    expected_site = {
        "schemaVersion": "research-site-version-v1", "version": "1.53",
        "latestRelease": "R0.73M", "publicHtmlNoteCount": 189,
        "publishedDate": "2026-08-31",
    }
    if site != expected_site:
        raise RuntimeError("R0.73M site-version baseline drift")
    site.update({
        "version": SITE_VERSION, "latestRelease": RELEASE,
        "publicHtmlNoteCount": 190, "publishedDate": content.date,
    })

    inventory = strict_json_bytes(
        git_bytes(RELEASE_BASELINE_COMMIT, "research/formal-archive-inventory.json"),
        "formal archive inventory",
    )
    state = (
        inventory.get("latestPublishedRelease"), inventory.get("publishedReleaseCount"),
        inventory.get("formalSealedReleaseCount"), inventory.get("legacyFormalFigureBacklogCount"),
    )
    if state != ("r073m", 91, 67, 24):
        raise RuntimeError("R0.73M formal-archive baseline drift")
    for key in ("publishedReleases", "formalSealedReleases"):
        rows = inventory.get(key)
        if not isinstance(rows, list) or rows[-1:] != ["r073m"] or "r073n" in rows:
            raise RuntimeError("formal archive is not append-only: " + key)
        rows.append("r073n")
    inventory.update({
        "latestPublishedRelease": "r073n", "publishedReleaseCount": 92,
        "formalSealedReleaseCount": 68, "legacyFormalFigureBacklogCount": 24,
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
        ROOT / "VERSION": b"1.54\n",
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
        with tempfile.TemporaryDirectory(prefix="r073n-index-") as temporary:
            notes = Path(temporary)
            for relative in git_paths(RELEASE_BASELINE_COMMIT, "public/notes"):
                name = Path(relative).name
                if re.fullmatch(r"r0-[0-9a-z]+\.(?:html|pdf)", name):
                    (notes / name).write_bytes(git_bytes(RELEASE_BASELINE_COMMIT, relative))
            existing = []
            note_index.ROOT, note_index.PUBLIC, note_index.NOTES = ROOT, PUBLIC, notes
            note_index.OUTPUT = notes / "index.html"
            existing = [note_index.parse_note(path) for path in note_index.note_files()]
            if len(existing) != 189 or existing[0].slug != "r0-73m":
                raise RuntimeError("R0.73N note-index baseline is not exact")
            latest = note_index.Note(
                slug="r0-73n", code=RELEASE,
                title=content.document_title_en.split("｜", 1)[-1].strip(),
                major=73, has_pdf=True,
            )
            note_index.json = TargetJson
            note_index.latest_recap_href = lambda: "/recap-r0-61-r0-73n.html"
            value = note_index.render([latest, *existing])
    finally:
        note_index.json = old_json
        note_index.latest_recap_href = old_recap
        note_index.ROOT, note_index.PUBLIC, note_index.NOTES, note_index.OUTPUT = old_paths
    assert_public_html(value, "R0.73N note index", require_boundary=False)
    if "prefers-color-scheme: dark" not in value:
        raise RuntimeError("R0.73N index lost automatic dark theme")
    return value


def stage_figure_assets(staged: dict[Path, bytes]) -> None:
    source = ROOT / FIGURE_SOURCE_RELATIVE
    files = sorted(path for path in source.iterdir() if path.is_file() and not path.is_symlink())
    if not files or not (source / "manifest.json").is_file():
        raise RuntimeError("R0.73N formal figure package is incomplete")
    for path in files:
        staged[PUBLIC / FIGURE_ARCHIVE_RELATIVE / path.name] = path.read_bytes()
    for suffix in ("pdf", "svg", "png"):
        master = source / f"figure.{suffix}"
        if not master.is_file() or master.is_symlink():
            raise RuntimeError("R0.73N figure master missing: " + master.name)
        staged[PUBLIC / f"assets/r073n/{FIGURE_ID}.{suffix}"] = master.read_bytes()


def build_staged(content: ReleaseContent) -> dict[Path, bytes]:
    staged: dict[Path, bytes] = {}
    stage_figure_assets(staged)
    staged[PUBLIC / "notes/r0-73n.html"] = build_note(content).encode("utf-8")
    staged[PUBLIC / "recap-r0-61-r0-73n.html"] = build_recap(content).encode("utf-8")
    staged[PUBLIC / "research-review.html"] = update_home(content).encode("utf-8")
    staged[PUBLIC / "literature-review.html"] = update_literature(content).encode("utf-8")
    staged.update(build_manifest_outputs(content))
    staged[PUBLIC / "notes/index.html"] = build_note_index(
        content, staged[PUBLIC / "site-version.json"]
    ).encode("utf-8")
    missing = [relative for relative in CORE_TARGET_OUTPUTS if ROOT / relative not in staged]
    if missing:
        raise RuntimeError("R0.73N staged transaction omitted: " + repr(missing))
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
            temporary = target.parent / f".{target.name}.r073n-{nonce}-{index}.tmp"
            backup = target.parent / f".{target.name}.r073n-{nonce}-{index}.bak"
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
            target = row["target"]
            backup = row["backup"]
            if row["installed"] and Path(target).exists():
                Path(target).unlink()
            if row["backed_up"] and Path(backup).exists():
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


def source_dry_run() -> dict:
    content = load_release_content(ROOT)
    figure_source = ROOT / FIGURE_SOURCE_RELATIVE
    certificate_source = ROOT / "research/certificates/r073n"
    final_ready, final_failures = final_content_readiness(content)
    return {
        "release": RELEASE,
        "mode": "source-dry-run",
        "canonicalSources": len(content.source_sha256),
        "canonicalSourceSha256": content.source_sha256,
        "sections": len(content.sections),
        "fullThreeDimensionalFPS_H3_L2": "OPEN",
        "figureSourcePresent": figure_source.is_dir() and not figure_source.is_symlink(),
        "certificateSourcePresent": certificate_source.is_dir() and not certificate_source.is_symlink(),
        "commitPinsReady": all(commit != ZERO_COMMIT for _, commit in BINDING_ORDER),
        "finalContentReady": final_ready,
        "finalContentPending": final_failures,
        "bindingOrder": [label for label, _ in BINDING_ORDER],
        "publicationStageOrder": list(PUBLICATION_STAGE_ORDER),
        "coreOutputsPlanned": list(CORE_TARGET_OUTPUTS),
        "laterStageOutputsPlanned": list(LATER_STAGE_OUTPUTS),
        "writes": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate or explicitly apply the fail-closed R0.73N release transaction."
    )
    action = parser.add_mutually_exclusive_group()
    action.add_argument(
        "--source-dry-run", action="store_true",
        help="validate canonical sources and output plan without commit pins or public reads",
    )
    action.add_argument(
        "--check-only", action="store_true",
        help="validate pinned inputs and construct all outputs in memory without writing",
    )
    action.add_argument(
        "--apply", action="store_true",
        help="apply the pinned HTML/manifest/figure transaction; PDFs and translations remain separate",
    )
    args = parser.parse_args()
    if not (args.source_dry_run or args.check_only or args.apply):
        parser.print_help()
        return
    if args.source_dry_run:
        print(json.dumps(source_dry_run(), ensure_ascii=False, indent=2))
        return

    content = verify_inputs()
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
        raise SystemExit("R0.73N canonical-source gate failed: " + str(exc)) from exc
