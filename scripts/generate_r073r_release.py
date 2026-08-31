#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fail-closed R0.73R GitHub Pages release skeleton.

The mathematical copy comes from ``r073r_release_content.py``.  This file
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

from r073r_release_content import (
    CANONICAL_SOURCE_PATHS,
    FIGURE_ARCHIVE_RELATIVE,
    FIGURE_ID,
    FIGURE_SOURCE_RELATIVE,
    R073Q_BASELINE,
    R073R_TARGET,
    RELEASE,
    SITE_VERSION,
    CanonicalSourceError,
    ReleaseContent,
    load_release_content,
)


ROOT = Path(os.environ.get(
    "R073R_RELEASE_ROOT", Path(__file__).resolve().parents[1]
)).resolve()
PUBLIC = ROOT / "public"
ZERO_COMMIT = "0" * 40

# Binding order (oldest to newest): published R0.73Q baseline -> analytic
# source -> finite package -> formal figure package -> final reader-facing
# content -> release-source code.  The published baseline and reviewed A--D
# inputs are frozen below.  The release-source pin alone remains deliberately
# zero until these four files are committed together and reviewed.
ANALYTIC_SOURCE_COMMIT = "25b20d225202359de2fd2d95ed86dd4b372d23a5"
FINITE_PACKAGE_COMMIT = "6809fc92a2d1338fb77fb3bf5a72d16ed158d807"
FIGURE_PACKAGE_COMMIT = "f3d8ac3b04aa122a44f112d554c4991ecfb6f36e"
RELEASE_BASELINE_COMMIT = "66a523bcc49aadc4df81ab39542fc4dfdbac14d0"
FINAL_CONTENT_COMMIT = "fb0ea0dfaf753de4c19b9155daf320b4fca8cb6a"
RELEASE_SOURCE_COMMIT = "46f4e6c408fe527648674cc7152c096055863ab0"

BINDING_ORDER = (
    ("R0.73Q release baseline", RELEASE_BASELINE_COMMIT),
    ("analytic source", ANALYTIC_SOURCE_COMMIT),
    ("finite package", FINITE_PACKAGE_COMMIT),
    ("figure package", FIGURE_PACKAGE_COMMIT),
    ("final content", FINAL_CONTENT_COMMIT),
    ("R0.73R release source", RELEASE_SOURCE_COMMIT),
)

ANALYTIC_EXACT_PATHS = (
    "research/r073r_problem_freeze.md",
    "research/r073r_shell_concentration_candidate.md",
    "research/r073r_lp_caloric_certificate_proof.md",
    "research/r073r_primary_literature_audit.md",
    "research/r073r_independent_analytic_audit.md",
    "research/r073r_claim_source_ledger.md",
    "research/r073r_evidence_gap_matrix.md",
)
FINAL_CONTENT_EXACT_PATHS = (
    "research/r073r_finite_diagnostic_audit.md",
    "research/r073r_report-source.md",
    "research/r073r_bilingual_dictionary.md",
)
FINITE_EXACT_ROOTS = ("research/certificates/r073r",)
FIGURE_EXACT_ROOTS = (FIGURE_SOURCE_RELATIVE,)
BASELINE_EXACT_PATHS = (
    "VERSION",
    "research/release-manifest.json",
    "research/formal-archive-inventory.json",
    "public/site-version.json",
    "public/notes/r0-73q.html",
    "public/recap-r0-61-r0-73q.html",
    "public/research-review.html",
    "public/literature-review.html",
    "public/notes/index.html",
)
RELEASE_SOURCE_EXACT_PATHS = (
    "scripts/r073r_release_content.py",
    "scripts/generate_r073r_release.py",
    "tests/r073r-shell-phase-gate.test.mjs",
    "tests/r073r-release.test.mjs",
)

CORE_TARGET_OUTPUTS = (
    "public/notes/r0-73r.html",
    "public/recap-r0-61-r0-73r.html",
    "public/research-review.html",
    "public/literature-review.html",
    "public/notes/index.html",
    "public/site-version.json",
    "research/release-manifest.json",
    "research/formal-archive-inventory.json",
    "VERSION",
)
LATER_STAGE_OUTPUTS = (
    "public/notes/r0-73r.pdf",
    "public/recap-r0-61-r0-73r.pdf",
    "research/r073r_pdf_bindings.json",
    "translations/en.json",
    "public/i18n-en.js",
    "scripts/i18n-snapshots/r073r-missing.json",
)
PUBLICATION_STAGE_ORDER = (
    "freeze-r073q-baseline",
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


def verify_pinned_paths_exist(commit: str, paths: tuple[str, ...], label: str) -> None:
    """Verify immutable baseline inputs without requiring stale worktree bytes.

    Release targets are deliberately regenerated from the pinned baseline, so
    their current worktree copies may be either the old baseline or a prior
    deterministic apply.  The baseline manifests and page markers are checked
    again when the staged target is assembled.
    """
    for relative in paths:
        try:
            git_bytes(commit, relative)
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(label + ": path absent from pin at " + relative) from exc


def normalized_release_generator(payload: bytes) -> bytes:
    try:
        value = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError("R0.73R release generator is not UTF-8") from exc
    value, count = re.subn(
        r'(?m)^RELEASE_SOURCE_COMMIT = (?:ZERO_COMMIT|"[0-9a-f]{40}")$',
        'RELEASE_SOURCE_COMMIT = "__NORMALIZED_RELEASE_SOURCE_COMMIT__"',
        value,
    )
    if count != 1:
        raise RuntimeError("R0.73R generator must expose exactly one release-source pin")
    return value.encode("utf-8")


def verify_release_source(commit: str) -> None:
    for relative in RELEASE_SOURCE_EXACT_PATHS:
        current = current_regular_bytes(relative)
        frozen = git_bytes(commit, relative)
        if relative == "scripts/generate_r073r_release.py":
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
    base = "research/certificates/r073r"
    manifest = strict_json_file(f"{base}/manifest.json", "R0.73R certificate manifest")
    config = strict_json_file(f"{base}/config.json", "R0.73R certificate config")
    diagnostic = strict_json_file(f"{base}/diagnostic.json", "R0.73R diagnostic")
    independent = strict_json_file(
        f"{base}/independent_validation.json", "R0.73R independent validation"
    )
    certificate = strict_json_file(f"{base}/certificate.json", "R0.73R certificate")
    validation = strict_json_file(f"{base}/validation.json", "R0.73R certificate validation")
    if (
        manifest.get("schemaVersion") != "r073r-matched-phase-shell-manifest-v1"
        or manifest.get("release") != RELEASE
        or manifest.get("status") != "sealed"
        or manifest.get("finalSeal") is not True
        or manifest.get("sourceCommitAssigned") is not True
        or manifest.get("sourceCommit") != ANALYTIC_SOURCE_COMMIT
        or manifest.get("allPrerequisiteChecksPass") is not True
    ):
        raise RuntimeError("R0.73R certificate is not final-sealed to the analytic commit")
    for payload, label in (
        (diagnostic, "R0.73R diagnostic"),
        (independent, "R0.73R independent validation"),
        (certificate, "R0.73R certificate"),
        (validation, "R0.73R certificate validation"),
    ):
        require_pass_payload(payload, label)
    boundary = config.get("claimBoundary")
    if (
        not isinstance(boundary, dict)
        or any(payload.get("claimBoundary") != boundary
               for payload in (manifest, diagnostic, certificate, validation))
        or independent.get("claimBoundary") != boundary
        or manifest.get("independentClaimBoundary") != boundary
    ):
        raise RuntimeError("R0.73R certificate claim boundaries disagree")
    for key in (
        "annularHeatProxyIsExactHeatNorm",
        "continuumPdeProofCertified",
        "heatFlowIntegralComputed",
        "intervalArithmeticUsed",
        "navierStokesSimulation",
        "pdeNecessityEstablished",
        "globalRegularityEstablished",
        "finiteTimeSingularityEstablished",
        "clayProblemSolved",
    ):
        if boundary.get(key) is not False:
            raise RuntimeError("R0.73R certificate overclaims " + key)
    for key in (
        "dirichletSixthMomentIdentity",
        "finiteFormulaDiagnosticOnly",
        "matchedFourierSupportAndMagnitudes",
        "rudinShapiroEnergyIdentity",
        "scalingTableIsDiagnostic",
    ):
        if boundary.get(key) is not True:
            raise RuntimeError("R0.73R certificate lost diagnostic fact " + key)
    if (
        diagnostic.get("rowCount") != 16
        or independent.get("rowCount") != 16
        or certificate.get("rowCount") != 16
        or validation.get("rowCount") != 16
        or manifest.get("checkInventory") != {
            "independent": 65, "primary": 114, "structural": 115,
        }
    ):
        raise RuntimeError("R0.73R certificate source-data counts drifted")
    formulas = certificate.get("formulaStatements")
    required_formulas = {
        "annularHeatProxy": "N^(-1/2) ||W_{R,m}||_6; diagnostic proxy, not an exact heat norm",
        "coefficientMagnitudeSquared": "1/(2*m^2)",
        "dirichletUnivariateL6Sixth": "(11*m^5+5*m^3+4*m)/20",
        "fieldL2Squared": "1",
        "fieldL6Sixth": "5*S_R^2/(2*m^6)",
        "scalingAmplitude": "alpha_m=N^(1/2)*m^(-2/3)",
        "supportSize": "2*m^2",
    }
    if not isinstance(formulas, dict) or any(
        formulas.get(key) != value for key, value in required_formulas.items()
    ):
        raise RuntimeError("R0.73R certificate formula ledger drifted")
    run_package_verifier(
        f"{base}/validate_certificate.py",
        ["--verify-only"],
        "R0.73R certificate scientific validator",
    )
    run_package_verifier(
        f"{base}/seal_package.py",
        ["--verify-only", "--source-commit", ANALYTIC_SOURCE_COMMIT],
        "R0.73R certificate",
    )
    return manifest


def validate_figure_package(certificate_manifest: dict) -> dict:
    base = FIGURE_SOURCE_RELATIVE
    manifest = strict_json_file(f"{base}/manifest.json", "R0.73R figure manifest")
    config = strict_json_file(f"{base}/config.json", "R0.73R figure config")
    contract = strict_json_file(f"{base}/contract.json", "R0.73R figure contract")
    results = strict_json_file(f"{base}/results.json", "R0.73R figure results")
    validation = strict_json_file(f"{base}/validation.json", "R0.73R figure validation")
    if (
        manifest.get("schemaVersion") != "research-figure-manifest-v1"
        or manifest.get("status") != "formal"
        or manifest.get("sourceCommitAssigned") is not True
        or manifest.get("git", {}).get("sourceCommit") != ANALYTIC_SOURCE_COMMIT
        or manifest.get("allPrerequisiteChecksPass") is not True
        or manifest.get("qa", {}).get("status") != "passed"
        or certificate_manifest.get("sourceCommit") != ANALYTIC_SOURCE_COMMIT
    ):
        raise RuntimeError("R0.73R figure is not final-sealed to the analytic commit")
    if (
        results.get("schemaVersion") != "r073r-phase-coherence-results-v1"
        or results.get("mode") != "render-preseal"
        or results.get("figureId") != FIGURE_ID
        or results.get("pdfGenerated") is not True
        or results.get("rowCount") != 141
    ):
        raise RuntimeError("R0.73R figure results drifted")
    checks = validation.get("checks")
    if (
        validation.get("status") != "formal-passed"
        or validation.get("allAutomatedChecksPass") is not True
        or not isinstance(checks, dict)
        or not checks
        or not all(value is True for value in checks.values())
        or validation.get("sourceCommitAssigned") is not True
        or validation.get("figureId") != FIGURE_ID
    ):
        raise RuntimeError("R0.73R figure validation provenance drifted")
    boundary = contract.get("claimBoundary")
    if (
        not isinstance(boundary, dict)
        or validation.get("claimBoundary") != boundary
    ):
        raise RuntimeError("R0.73R figure claim boundaries disagree")
    if (
        config.get("figureId") != FIGURE_ID
        or results.get("isAnalyticScalingGuide") is not True
        or results.get("isFittedScalingLaw") is not False
        or results.get("isNavierStokesSimulation") is not False
        or results.get("dgxUsed") is not False
    ):
        raise RuntimeError("R0.73R figure result/configuration boundary drifted")
    facts = results.get("facts")
    if (
        not isinstance(facts, dict)
        or facts.get("panelA", {}).get("positivePacketRowCount") != 128
        or facts.get("panelA", {}).get("rowCountPerFamily") != 64
        or facts.get("panelA", {}).get("fullSupportSizePerFamily") != 128
        or facts.get("panelA", {}).get("supportAndModuliMatched") is not True
        or facts.get("scaling", {}).get("rowCount") != 13
        or facts.get("scaling", {}).get("phaseSeparationPower") != 2.0 / 3.0
    ):
        raise RuntimeError("R0.73R figure row accounting drifted")
    for key in (
        "fittedScalingLaw",
        "navierStokesSimulation",
        "necessaryRegularityCriterion",
        "unsafeDynamics",
        "arbitraryL2SmallDataSafe",
        "nonlinearPdeCertificate",
        "finiteTimeSingularity",
        "clayProblemSolved",
    ):
        if boundary.get(key) is not False:
            raise RuntimeError("R0.73R figure overclaims " + key)
    for key in (
        "analyticPowersOnly",
        "fieldsHaveZeroConvection",
    ):
        if boundary.get(key) is not True:
            raise RuntimeError("R0.73R figure lost diagnostic fact " + key)
    output_rows = results.get("outputs", [])
    output_by_name = {
        row.get("path"): row for row in output_rows if isinstance(row, dict)
    }
    for suffix in ("pdf", "svg", "png"):
        name = f"figure.{suffix}"
        payload = current_regular_bytes(f"{base}/{name}")
        row = output_by_name.get(name)
        if row is None or row.get("bytes") != len(payload) or row.get("sha256") != sha256(payload):
            raise RuntimeError("R0.73R figure master is not manifest-bound: " + name)
    verifier_arguments = [
        "--final", "--verify-only", "--confirm-visual-qa",
        "--source-commit", ANALYTIC_SOURCE_COMMIT,
    ]
    dependency_root = os.environ.get("R073R_FIGURE_DEPS", "/tmp/r073r-figure-deps")
    if not Path(dependency_root).is_dir():
        raise RuntimeError(
            "R0.73R figure dependency directory missing; set R073R_FIGURE_DEPS"
        )
    verifier_arguments[0:0] = ["--deps", dependency_root]
    run_package_verifier(
        f"{base}/validate.py", verifier_arguments, "R0.73R figure"
    )
    return manifest


def final_content_readiness(content: ReleaseContent) -> tuple[bool, list[str]]:
    failures: list[str] = []
    if not content.publication_ready:
        failures.append("analyticReadiness=" + content.readiness_detail)
    if content.next_release.lower() != "r0.73s":
        failures.append("nextRelease=" + content.next_release)
    if "PENDING" in content.closed_ledger:
        failures.append("analyticBoundary=PENDING")
    return not failures, failures


def verify_inputs() -> ReleaseContent:
    ensure_commits_ready()
    verify_exact_paths(ANALYTIC_SOURCE_COMMIT, ANALYTIC_EXACT_PATHS, "analytic source")
    verify_exact_roots(FINITE_PACKAGE_COMMIT, FINITE_EXACT_ROOTS, "finite package")
    verify_exact_roots(FIGURE_PACKAGE_COMMIT, FIGURE_EXACT_ROOTS, "figure package")
    verify_exact_paths(FINAL_CONTENT_COMMIT, FINAL_CONTENT_EXACT_PATHS, "final content")
    verify_pinned_paths_exist(RELEASE_BASELINE_COMMIT, BASELINE_EXACT_PATHS, "release baseline")
    verify_release_source(RELEASE_SOURCE_COMMIT)
    certificate_manifest = validate_certificate_package()
    validate_figure_package(certificate_manifest)
    content = load_release_content(ROOT)
    ready, failures = final_content_readiness(content)
    if not ready:
        raise RuntimeError("R0.73R final content is not release-ready: " + ", ".join(failures))
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
    tokens = ["R0.73R", "/i18n-en.js?v=1.58"]
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
    value = decode_baseline("public/notes/r0-73q.html")
    description = (
        "研究笔记 R0.73R：经典周期热--Besov 等价、三层 Fourier 证书、"
        "匹配相位分离、零非线性边界与 L2-only 开放问题。"
    )
    value = replace_regex(value, r'<meta name="description" content="[^"]*">',
                          f'<meta name="description" content="{description}">', "note description")
    value = replace_regex(value, r'<meta property="og:title" content="[^"]*">',
                          f'<meta property="og:title" content="{html.escape(content.document_title_en, quote=True)}">', "note OG title")
    value = replace_regex(value, r'<meta property="og:description" content="[^"]*">',
                          f'<meta property="og:description" content="{html.escape(content.lead_zh, quote=True)}">', "note OG description")
    value = replace_regex(value, r'<meta property="og:image" content="[^"]*">',
                          f'<meta property="og:image" content="https://kasifa.github.io/assets/r073r/{FIGURE_ID}.png">', "note OG image")
    value = replace_regex(value, r'<title>.*?</title>',
                          f'<title>{html.escape(content.document_title_en)}</title>', "note title")
    note_styles = """  <style>
    .table-wrap{width:100%;margin:28px 0;overflow-x:auto}
    .table-wrap table{margin:0;table-layout:fixed}
    .table-wrap th,.table-wrap td{overflow-wrap:anywhere;word-break:normal;hyphens:auto}
    article p,article li{overflow-wrap:anywhere}
    article pre{max-width:100%;overflow-x:auto;white-space:pre}
    blockquote{max-width:760px;margin:24px 0;padding:2px 0 2px 20px;border-left:3px solid var(--gold);color:var(--muted)}
    blockquote p{max-width:none;margin:.4rem 0}
    @media(max-width:520px){.table-wrap table{display:table;min-width:760px}article mjx-container[display="true"]{width:100%!important;min-width:0!important;max-width:100%;overflow-x:auto;overflow-y:hidden}article mjx-container:not([display="true"]){display:inline-block!important;max-width:100%;overflow-x:auto;overflow-y:hidden;vertical-align:middle}}
    @media print{.table-wrap{overflow:visible}.table-wrap table{display:table;min-width:0;font-size:6.7pt}.table-wrap th,.table-wrap td{padding:5px 4px}blockquote{break-inside:avoid;margin:14px 0}}
  </style>
"""
    value = replace_once(value, "</head>", note_styles + "</head>", "note semantic styles")
    value = replace_once(value, "/i18n-en.js?v=1.57", "/i18n-en.js?v=1.58", "note i18n")
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
        '按原编号区分定理、有限计算与开放问题。</div><div>研究笔记 R0.73R · '
        f'{content.date}<br><a href="/">返回研究主页</a></div></footer>', "note footer",
    )
    assert_public_html(value, "R0.73R note")
    if "/note-retro.css" not in value:
        raise RuntimeError("R0.73R note lost retro stylesheet")
    return value


def build_recap(content: ReleaseContent) -> str:
    value = decode_baseline("public/recap-r0-61-r0-73q.html")
    value = value.replace("/i18n-en.js?v=1.57", "/i18n-en.js?v=1.58")
    value = value.replace("R0.61–R0.73Q", "R0.61–R0.73R")
    value = value.replace("R0.61 到 R0.73Q", "R0.61 到 R0.73R")
    value = value.replace("R0.69P–R0.73Q", "R0.69P–R0.73R")
    value = value.replace("R0.70A–R0.73Q", "R0.70A–R0.73R")
    value = value.replace("回顾截止节点：R0.73Q", "回顾截止节点：R0.73R")
    value = value.replace("收录节点：133", "收录节点：134")
    value = value.replace("回顾截止时公开笔记：193", "回顾截止时公开笔记：194")
    value = value.replace("133 节", "134 节").replace("133 个节点", "134 个节点")
    value = value.replace("95 个版本", "96 个版本").replace("95 节", "96 节")
    value = value.replace("71 个满足", "72 个满足").replace("71 节", "72 节")
    # The R0.73Q baseline contains 52 phase articles; R0.73R adds one.
    value = value.replace("52 个阶段", "53 个阶段")
    value = value.replace("52 个研究阶段", "53 个研究阶段")
    value = replace_once(
        value,
        "      #retained li{margin:.14rem 0;line-height:1.4}\n",
        "      #retained li{margin:.14rem 0;line-height:1.4}\n"
        "      #reproduce .section-no{margin-bottom:.1rem}\n"
        "      #reproduce h2{font-size:1.8rem;margin:.2rem 0 .35rem}\n"
        "      #reproduce p{font-size:.9rem;line-height:1.35;margin:.15rem 0}\n"
        "      #reproduce{margin-bottom:0}\n"
        "      #claims{margin-bottom:10px}\n"
        "      #claims p{line-height:1.45;margin:.2rem 0}\n"
        "      .layout{padding-bottom:0}\n",
        "recap print final-section spacing",
    )
    value = value.replace("<strong>133</strong>", "<strong>134</strong>")
    value = value.replace("<strong>95</strong>", "<strong>96</strong>")
    value = value.replace("<strong>71</strong>", "<strong>72</strong>")
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
        'R0.73R 共 134 个节点；最新一节分开经典热--Besov 机制、逐壳证书、相位分离与 L2-only 开放边界。">',
        "recap description",
    )
    value = replace_regex(
        value,
        r'<meta property="og:description" content="[^"]*">',
        '<meta property="og:description" content="53 个阶段、134 个节点：从约化递推和环带排除到逐壳相位证书与零非线性边界。">',
        "recap OG description",
    )
    value = replace_once(value, "          </div>\n        </section>\n\n        <section id=\"node-index\"",
                         content.recap_phase + "\n          </div>\n        </section>\n\n        <section id=\"node-index\"", "recap phase append")
    node = '<span class="node-ref"><a href="/notes/r0-73r.html">R0.73R</a><span class="node-state kind-closed">闭</span></span>'
    value = replace_once(value, "          </div>\n        </section>\n\n        <section id=\"retained\"",
                         f"            {node}\n          </div>\n        </section>\n\n        <section id=\"retained\"", "recap node append")
    retained = (
        '<li>R0.73R 将经典周期热--Besov 等价写成逐壳能量与集中度预算，并给出精确卷积、'
        '加法重数和支撑计数三层证书。同支撑同幅值的 Dirichlet/Rudin--Shapiro 场仍有 '
        '\\(m^{2/3}\\) 热流迹分离；两族对流非线性均为零，L2-only 与 Clay 保持开放。</li>'
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
        '<h2>经典热流机制、相位信息与开放边界已经分开</h2>'
        f'<p>{html.escape(content.recap_zh)}</p>'
        '<p>不能把 134 个节点或 96 个公开版本解释成 Clay 完成比例。'
        '有限 matched-pair 计算只认证公式；零非线性例子不覆盖任意 L2-small 数据。'
        '有限时奇性和任意初值全局正则性仍为 OPEN。</p></section>',
        "recap current value",
    )
    value = replace_regex(
        value,
        r'<section id="next">.*?</section>',
        '<section id="next"><div class="section-no">05 / 下一步</div>'
        f'<h2>{html.escape(content.next_release)}：低成本相位代理量</h2>'
        f'<p>{html.escape(content.math_next_gate_zh)}</p></section>',
        "recap next gate",
    )
    value = replace_regex(
        value,
        r'<section id="claims">.*?</section>',
        '<section id="claims"><div class="section-no">06 / 说明边界</div>'
        '<h2>连续定理、有限诊断和开放问题分开列示</h2>'
        '<p>R0.70A–R0.73R 的 96 节已公开；72 节完整封存；24 节旧档待回补。</p>'
        f'<p>{html.escape(content.closed_ledger)}</p>'
        f'<p>{html.escape(content.finite_ledger)}</p>'
        f'<p>{html.escape(content.open_ledger)}</p>'
        '<p>R0.73R 的有限公式诊断和正式附图只复算 matched Fourier 支撑、六次矩与解析标度；'
        '它们不是 Navier--Stokes 仿真，两族非线性严格为零，不认证奇性或 Clay。NOT CLAY。</p></section>',
        "recap exact boundary",
    )
    value = replace_regex(
        value,
        r'<section id="reproduce">.*?</section>',
        '<section id="reproduce"><div class="section-no">07 / 原始资料</div>'
        '<h2>逐节笔记、证明、审计、证书、附图和历史回顾</h2>'
        '<p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · '
        '<a href="/recap-r0-61-r0-73q.html">保留 R0.73Q 历史回顾</a> · '
        '<a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · '
        '<a href="/notes/r0-73r.html">打开最新节点 R0.73R</a></p>'
        '<p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073r_report-source.md">查看 canonical report</a> · '
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073r_lp_caloric_certificate_proof.md">查看 LP--caloric 证明</a> · '
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073r_primary_literature_audit.md">查看一手文献审计</a> · '
        '<a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073r">查看有限诊断包</a> · '
        f'<a href="/assets/r073r/{FIGURE_ID}.pdf">下载期刊附图</a> · '
        '<a href="/recap-r0-61-r0-73r.pdf">下载同步 PDF</a></p>'
        '<p>连续定理由解析证明承担；有限诊断只作可复现错误探测。</p></section>',
        "recap reproduction",
    )
    value = value.replace("/recap-r0-61-r0-73q.pdf", "/recap-r0-61-r0-73r.pdf")
    value = value.replace("R0.73Q 回顾", "R0.73R 回顾")
    for stale in ("<strong>133</strong>", "<strong>95</strong>", "<strong>71</strong>"):
        if stale in value:
            raise RuntimeError("R0.73R recap retained stale metric " + stale)
    if value.count('<article class="phase">') != 53:
        raise RuntimeError("R0.73R recap must contain exactly 53 phase articles")
    if (
        "51 个阶段" in value or "52 个阶段" in value
        or "51 个研究阶段" in value or "52 个研究阶段" in value
    ):
        raise RuntimeError("R0.73R recap retained a stale displayed phase count")
    assert_public_html(value, "R0.73R recap")
    return value


def update_home(content: ReleaseContent) -> str:
    value = decode_baseline("public/research-review.html")
    value = value.replace('data-site-version="1.57"', 'data-site-version="1.58"')
    value = value.replace("/i18n-en.js?v=1.57", "/i18n-en.js?v=1.58")
    value = value.replace("/site-refresh.js?v=1.57", "/site-refresh.js?v=1.58")
    value = replace_regex(value, r'<section class="route-overview latest-release-spotlight".*?</section>',
                          content.latest_spotlight, "home latest spotlight")
    marker = '<div class="task-one" id="r073q" data-release="r073q"'
    value = replace_once(value, marker, content.home_card + "\n          " + marker, "home card insert")
    value = value.replace("<strong>193</strong>公开研究笔记", "<strong>194</strong>公开研究笔记")
    value = value.replace("<strong>v1.57</strong>网页版本", "<strong>v1.58</strong>网页版本")
    value = value.replace("<strong>R0.73Q</strong>最新研究节点", "<strong>R0.73R</strong>最新研究节点")
    value = value.replace(
        "<strong>critical heat-flow tube / endpoint boundary</strong>当前方向",
        "<strong>shellwise phase certificate / classical Besov boundary</strong>当前方向",
    )
    value = value.replace("NEXT · R0.73R", "NEXT · R0.73S")
    value = replace_regex(
        value,
        r'<h3>R0\.73R 下一接口</h3><p>.*?</p>',
        f'<h3>{html.escape(content.next_release)} 下一接口</h3>'
        f'<p>{html.escape(content.math_next_gate_zh)}</p>',
        "home next interface",
    )
    value = value.replace("R0.70A–R0.73Q：95 节已公开，71 节完整封存",
                          "R0.70A–R0.73R：96 节已公开，72 节完整封存")
    value = value.replace("Research topology · R0.1–R0.73Q", "Research topology · R0.1–R0.73R")
    value = value.replace('<a class="route-map-latest" href="#r073q">跳到首页 R0.73Q 卡片 →</a>',
                          '<a class="route-map-latest" href="#r073r">跳到首页 R0.73R 卡片 →</a>')
    value = value.replace('/recap-r0-61-r0-73q.html">阅读 R0.60 之后的累计回顾',
                          '/recap-r0-61-r0-73r.html">阅读 R0.60 之后的累计回顾')
    value = value.replace("/recap-r0-61-r0-73q.html", "/recap-r0-61-r0-73r.html")
    value = value.replace("/recap-r0-61-r0-73q.pdf", "/recap-r0-61-r0-73r.pdf")
    value = value.replace("综述 v1.57 ·", "综述 v1.58 ·")
    value = value.replace('<span class="route-range">R0.69P–R0.73Q</span>',
                          '<span class="route-range">R0.69P–R0.73R</span>')
    value = value.replace('R0.73Q：临界热流稳定管、严格扩域与端点边界已分列',
                          'R0.73R：经典热--Besov、逐壳相位证书与零非线性边界已分列')
    value = value.replace('<span>R0.72R–R0.73Q：</span>', '<span>R0.72R–R0.73R：</span>')
    value = value.replace(
        '→ critical H1/2 stability / N^-1/2 frequency gate → critical heat-flow tube / endpoint boundary</p>',
        '→ critical H1/2 stability / N^-1/2 frequency gate → critical heat-flow tube / endpoint boundary → shellwise phase certificate</p>',
    )
    current_paragraph = (
        f'<p>{html.escape(content.recap_zh)}<span>classical heat--Besov mechanism</span>；'
        '<span>matched phase separation</span>。两族对流非线性严格为零。</p>'
    )
    value = replace_once(
        value,
        '              <details class="tree-notes" open>',
        '              ' + current_paragraph + '\n              <details class="tree-notes" open>',
        "home route current paragraph",
    )
    value = value.replace('<summary>展开 103 篇公开笔记</summary>', '<summary>展开 104 篇公开笔记</summary>')
    value = value.replace('aria-label="R0.69P–R0.73Q"', 'aria-label="R0.69P–R0.73R"')
    value = replace_once(
        value,
        '                  <a class="milestone" href="/notes/r0-73q.html">R0.73Q</a>',
        '                  <a class="milestone" href="/notes/r0-73q.html">R0.73Q</a>\n'
        '                  <a class="milestone" href="/notes/r0-73r.html">R0.73R</a>',
        "home route R0.73R link",
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
        '<p class="eyebrow">累计回顾 R0.61–R0.73R · 2026-08-31</p>'
        '<h3>R0.60 recap 之后的累计回顾收录 134 个节点；全站现有 194 篇公开研究笔记</h3>'
        '<p>累计回顾现分 53 个阶段，完整保留 R0.61–R0.73R；最新节点分开记录经典热--Besov 等价、'
        '三层 Fourier 证书、相位分离、零非线性边界、有限公式诊断和正式附图。</p>'
        '<p>R0.70A–R0.73R 共 96 个版本已公开；72 个按当前 formal-figure 合同完整封存，'
        '24 个旧版附图档案仍列入回补清单。</p>'
        f'<p><strong>阶段判断：</strong>&nbsp;{html.escape(content.recap_zh)} '
        '任意 L2-only 入口、奇性与 Clay 保持 OPEN。</p>'
        '<p><a href="/recap-r0-61-r0-73r.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · '
        '<a href="/recap-r0-61-r0-73r.pdf">下载同步 PDF</a></p></div>'
    )
    value = replace_regex(
        value,
        r'<div class="task-one" id="post-r060-recap".*?</div>',
        recap_card,
        "home cumulative recap card",
    )
    value = value.replace(
        '<h3>检查 L2-only / 高频输入接口</h3><p>直接检查 \\(L^2\\)-only / 高频输入接口，确定初始 \\(L^2\\) 很小而 \\(H^3\\) 很大时现有稳定管在哪一步失效，并测试哪些可审计的频率局部化条件能够恢复严格控制。</p>',
        f'<h3>{html.escape(content.next_release)} 下一接口</h3><p>{html.escape(content.math_next_gate_zh)}</p>',
    )
    value = value.replace(
        "本站 R0.69P–R0.73Q 路线放在同一张图中",
        "本站 R0.69P–R0.73R 路线放在同一张图中",
    )
    for stale in (
        "Research topology · R0.1–R0.73Q",
        "累计回顾收录 133 个节点；全站现有 193 篇公开研究笔记",
        '<summary>展开 103 篇公开笔记</summary>',
        "<strong>v1.57</strong>网页版本",
        "<strong>R0.73Q</strong>最新研究节点",
        'data-site-version="1.57"',
        "/site-refresh.js?v=1.57",
        '<h3>R0.73R 下一接口</h3>',
    ):
        if stale in value:
            raise RuntimeError("R0.73R home retained stale latest marker " + stale)
    assert_public_html(value, "R0.73R home")
    return value


def update_literature(content: ReleaseContent) -> str:
    value = decode_baseline("public/literature-review.html")
    value = value.replace("/i18n-en.js?v=1.57", "/i18n-en.js?v=1.58")
    value = value.replace("文献综述 v1.57 ·", "文献综述 v1.58 ·")
    marker = '<span class="route-r073q-deck-update">'
    start = value.find(marker)
    end = value.find("</span>", start)
    if start < 0 or end < 0:
        raise RuntimeError("literature R0.73Q deck marker missing")
    end += len("</span>")
    value = value[:end] + content.literature_update + value[end:]
    value = value.replace("/recap-r0-61-r0-73q.html", "/recap-r0-61-r0-73r.html")
    value = value.replace("133 节", "134 节")
    value = value.replace("R0.69P–R0.73Q", "R0.69P–R0.73R")
    route_step = (
        '<div class="route-step kept"><header><b>R0.73R</b>'
        '<strong>shellwise phase certificate and classical Besov boundary</strong></header>'
        f'<p>{html.escape(content.recap_zh)} <a href="/notes/r0-73r.html">研究笔记</a> '
        '<a href="/recap-r0-61-r0-73r.html">当前累计回顾</a> '
        '<a href="#r073r-boundary">文献边界</a></p></div>'
        '<div class="route-step pause"><header><b>开放接口 · R0.73S</b>'
        '<strong>lower-cost deterministic phase proxy or no-go</strong></header>'
        f'<p>{html.escape(content.math_next_gate_zh)} 任意初值全局正则性与 Clay 保持 OPEN。</p></div>'
    )
    value = replace_regex(
        value,
        r'<div class="route-step pause"><header><b>开放接口 · R0\.73R</b>.*?</div>',
        route_step,
        "literature current route step",
    )
    literature_boundary = (
        '<h3 id="r073r-boundary">R0.73R 的逐壳相位证书与经典碰撞边界</h3>'
        '<p><a href="https://doi.org/10.1016/j.ansens.2006.07.002">Chemin--Gallagher 2006</a>'
        '已给出周期负指标 Besov 范数的热半群与 LP 定义；这一函数空间等价属于经典内容。'
        '<a href="https://doi.org/10.1090/S0002-9939-1959-0116184-5">Rudin 1959</a>'
        '是 Rudin--Shapiro 平坦性机制的历史来源之一。</p>'
        '<p>稀疏频集、随机相位、改进 Sobolev、谱投影和振荡大数据也都有直接先例。'
        '限定检索未发现完全相同的三维 matched pair；这不构成新颖性或优先权证明。</p>'
        '<div class="boundary"><strong>R0.73R 的主张边界</strong>'
        f'<p>{html.escape(content.closed_ledger)}</p>'
        f'<p>{html.escape(content.finite_ledger)}</p>'
        f'<p>{html.escape(content.open_ledger)}</p>'
        '<p>一手来源审计不承担新颖性或优先权声明；有限诊断不承担连续证明权重。NOT CLAY。</p></div>'
    )
    value = replace_once(
        value,
        '          <ol class="criteria">',
        '          ' + literature_boundary + '\n          <ol class="criteria">',
        "literature R0.73R boundary",
    )
    if "开放接口 · R0.73S" not in value or 'id="r073r-boundary"' not in value:
        raise RuntimeError("R0.73R literature route/boundary was not advanced")
    assert_public_html(value, "R0.73R literature")
    if "VERIFIED_CLASSICAL" not in value or "优先权" not in value:
        raise RuntimeError("R0.73R literature lost classical/non-priority boundary")
    return value


def build_manifest_outputs(content: ReleaseContent) -> dict[Path, bytes]:
    release = strict_json_bytes(
        git_bytes(RELEASE_BASELINE_COMMIT, "research/release-manifest.json"),
        "release manifest",
    )
    for key, expected in R073Q_BASELINE.items():
        if release.get(key) != expected:
            raise RuntimeError("R0.73Q release-manifest baseline drift: " + key)
    release.update({
        **R073R_TARGET,
        "latestReleaseGate": "tests/r073r-shell-phase-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r073r-release.test.mjs",
    })

    site = strict_json_bytes(
        git_bytes(RELEASE_BASELINE_COMMIT, "public/site-version.json"), "site version"
    )
    expected_site = {
        "schemaVersion": "research-site-version-v1", "version": "1.57",
        "latestRelease": "R0.73Q", "publicHtmlNoteCount": 193,
        "publishedDate": "2026-08-31",
    }
    if site != expected_site:
        raise RuntimeError("R0.73Q site-version baseline drift")
    site.update({
        "version": SITE_VERSION, "latestRelease": RELEASE,
        "publicHtmlNoteCount": 194, "publishedDate": content.date,
    })

    inventory = strict_json_bytes(
        git_bytes(RELEASE_BASELINE_COMMIT, "research/formal-archive-inventory.json"),
        "formal archive inventory",
    )
    state = (
        inventory.get("latestPublishedRelease"), inventory.get("publishedReleaseCount"),
        inventory.get("formalSealedReleaseCount"), inventory.get("legacyFormalFigureBacklogCount"),
    )
    if state != ("r073q", 95, 71, 24):
        raise RuntimeError("R0.73Q formal-archive baseline drift")
    for key in ("publishedReleases", "formalSealedReleases"):
        rows = inventory.get(key)
        if not isinstance(rows, list) or rows[-1:] != ["r073q"] or "r073r" in rows:
            raise RuntimeError("formal archive is not append-only: " + key)
        rows.append("r073r")
    inventory.update({
        "latestPublishedRelease": "r073r", "publishedReleaseCount": 96,
        "formalSealedReleaseCount": 72, "legacyFormalFigureBacklogCount": 24,
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
        ROOT / "VERSION": b"1.58\n",
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
        with tempfile.TemporaryDirectory(prefix="r073r-index-") as temporary:
            notes = Path(temporary)
            for relative in git_paths(RELEASE_BASELINE_COMMIT, "public/notes"):
                name = Path(relative).name
                if re.fullmatch(r"r0-[0-9a-z]+\.(?:html|pdf)", name):
                    (notes / name).write_bytes(git_bytes(RELEASE_BASELINE_COMMIT, relative))
            existing = []
            note_index.ROOT, note_index.PUBLIC, note_index.NOTES = ROOT, PUBLIC, notes
            note_index.OUTPUT = notes / "index.html"
            existing = [note_index.parse_note(path) for path in note_index.note_files()]
            if len(existing) != 193 or existing[0].slug != "r0-73q":
                raise RuntimeError("R0.73R note-index baseline is not exact")
            latest = note_index.Note(
                slug="r0-73r", code=RELEASE,
                title=content.document_title_en.split("｜", 1)[-1].strip(),
                major=73, has_pdf=True,
            )
            note_index.json = TargetJson
            note_index.latest_recap_href = lambda: "/recap-r0-61-r0-73r.html"
            value = note_index.render([latest, *existing])
    finally:
        note_index.json = old_json
        note_index.latest_recap_href = old_recap
        note_index.ROOT, note_index.PUBLIC, note_index.NOTES, note_index.OUTPUT = old_paths
    assert_public_html(value, "R0.73R note index", require_boundary=False)
    if "prefers-color-scheme: dark" not in value:
        raise RuntimeError("R0.73R index lost automatic dark theme")
    return value


def formal_figure_payloads(source: Path) -> dict[str, bytes]:
    manifest = strict_json_file(
        f"{FIGURE_SOURCE_RELATIVE}/manifest.json", "R0.73R formal figure manifest"
    )
    if (
        manifest.get("schemaVersion") != "research-figure-manifest-v1"
        or manifest.get("figureId") != FIGURE_ID
        or manifest.get("status") != "formal"
        or manifest.get("allPrerequisiteChecksPass") is not True
        or manifest.get("sourceCommitAssigned") is not True
        or manifest.get("git", {}).get("sourceCommit") != ANALYTIC_SOURCE_COMMIT
    ):
        raise RuntimeError("R0.73R source figure is not a commit-bound formal package")

    actual = sorted(
        path.name for path in source.iterdir()
        if path.is_file() and not path.is_symlink()
    )
    required = {
        "manifest.json", "SHA256SUMS", "figure.pdf", "figure.svg", "figure.png",
        "qa-pdf.png", "qa-final-size.png", "qa-grayscale.png",
        "source-data.csv", "results.json", "validation.json", "contract.json",
        "config.json", "environment.json", "caption.md",
    }
    if not required.issubset(actual):
        raise RuntimeError(
            "R0.73R formal figure inventory is incomplete: "
            + repr(sorted(required - set(actual)))
        )

    recorded = [
        *manifest.get("data", []),
        *manifest.get("figure", {}).get("outputs", []),
        *manifest.get("qa", {}).get("qaArtifacts", []),
    ]
    for row in recorded:
        if not isinstance(row, dict) or not isinstance(row.get("path"), str):
            raise RuntimeError("R0.73R formal figure contains an invalid file record")
        payload = current_regular_bytes(f"{FIGURE_SOURCE_RELATIVE}/{row['path']}")
        if row.get("bytes") != len(payload) or row.get("sha256") != sha256(payload):
            raise RuntimeError(
                "R0.73R formal figure record is not byte-bound: " + row["path"]
            )

    public_assets: list[dict[str, object]] = []
    for suffix in ("pdf", "svg", "png"):
        payload = current_regular_bytes(f"{FIGURE_SOURCE_RELATIVE}/figure.{suffix}")
        public_assets.append({
            "path": f"public/assets/r073r/{FIGURE_ID}.{suffix}",
            "bytes": len(payload),
            "sha256": sha256(payload),
        })

    formal = {
        **json.loads(json.dumps(manifest)),
        "release": RELEASE,
        "publicationStatus": "published",
        "publication": {
            "archiveDirectory": f"public/{FIGURE_ARCHIVE_RELATIVE}",
            "directory": "public/assets/r073r",
            "fileStem": FIGURE_ID,
            "byteIdentityRequired": True,
            "publicCopiesComplete": True,
            "assets": public_assets,
        },
        "packageInventory": {
            "paths": actual,
            "expectedFileCount": len(actual),
        },
    }
    payloads = {
        name: (
            json_bytes(formal)
            if name == "manifest.json"
            else (source / name).read_bytes()
        )
        for name in actual if name != "SHA256SUMS"
    }
    payloads["SHA256SUMS"] = "".join(
        f"{sha256(payloads[name])}  {name}\n" for name in sorted(payloads)
    ).encode("utf-8")
    if sorted(payloads) != actual:
        raise RuntimeError("R0.73R formal figure staging changed the package inventory")
    return payloads

def stage_figure_assets(staged: dict[Path, bytes]) -> None:
    source = ROOT / FIGURE_SOURCE_RELATIVE
    if not source.is_dir() or source.is_symlink() or not (source / "manifest.json").is_file():
        raise RuntimeError("R0.73R formal figure package is incomplete")
    payloads = formal_figure_payloads(source)
    for name, payload in payloads.items():
        staged[ROOT / FIGURE_ARCHIVE_RELATIVE / name] = payload
        staged[PUBLIC / FIGURE_ARCHIVE_RELATIVE / name] = payload
    for suffix in ("pdf", "svg", "png"):
        staged[PUBLIC / f"assets/r073r/{FIGURE_ID}.{suffix}"] = payloads[f"figure.{suffix}"]


def build_staged(content: ReleaseContent) -> dict[Path, bytes]:
    staged: dict[Path, bytes] = {}
    stage_figure_assets(staged)
    staged[PUBLIC / "notes/r0-73r.html"] = build_note(content).encode("utf-8")
    staged[PUBLIC / "recap-r0-61-r0-73r.html"] = build_recap(content).encode("utf-8")
    staged[PUBLIC / "research-review.html"] = update_home(content).encode("utf-8")
    staged[PUBLIC / "literature-review.html"] = update_literature(content).encode("utf-8")
    staged.update(build_manifest_outputs(content))
    staged[PUBLIC / "notes/index.html"] = build_note_index(
        content, staged[PUBLIC / "site-version.json"]
    ).encode("utf-8")
    missing = [relative for relative in CORE_TARGET_OUTPUTS if ROOT / relative not in staged]
    if missing:
        raise RuntimeError("R0.73R staged transaction omitted: " + repr(missing))
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
            temporary = target.parent / f".{target.name}.r073r-{nonce}-{index}.tmp"
            backup = target.parent / f".{target.name}.r073r-{nonce}-{index}.bak"
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
    certificate_source = ROOT / "research/certificates/r073r"
    final_ready, final_failures = final_content_readiness(content)
    return {
        "release": RELEASE,
        "siteVersion": SITE_VERSION,
        "mode": "source-dry-run",
        "targetAccounting": R073R_TARGET,
        "canonicalSources": len(content.source_sha256),
        "canonicalSourcesPlanned": len(CANONICAL_SOURCE_PATHS),
        "canonicalSourceSha256": content.source_sha256,
        "missingCanonicalSources": list(content.missing_canonical_sources),
        "sections": len(content.sections),
        "uniformL2OnlyStrongRadius": "OPEN",
        "zeroNonlinearityBoundary": "CLOSED",
        "translationPath": "LOCAL_DIRECT_NO_DGX",
        "clayConclusion": "OPEN",
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
        description="Validate or explicitly apply the fail-closed R0.73R release transaction."
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
        raise SystemExit("R0.73R canonical-source gate failed: " + str(exc)) from exc
