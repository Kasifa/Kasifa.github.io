#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the fail-closed transactional R0.73K GitHub Pages release.

The generator intentionally does not create the note/recap PDFs or English
translations.  Those remain later publication stages.  The analytic and
complete-package commits are frozen below.  Until the release-source pin is
replaced, every validating/applying invocation fails closed; ``--help``
remains side-effect free.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile

from generate_r072o_release import assert_clean, once, required, section
from generate_r072p_release import assert_mathjax_clean
from r073k_release_content import (
    CLOSED,
    FIGURE_ID,
    FIGURE_RELATIVE,
    FINITE,
    HOME_K_CARD,
    HOME_LATEST_SPOTLIGHT,
    HOME_NEXT,
    NOTE_ARTICLE,
    NOTE_HERO,
    OPEN,
    RECAP_PHASE,
    R073J_BASELINE,
    R073K_TARGET,
)


ROOT = Path(os.environ.get(
    "R073K_RELEASE_ROOT", Path(__file__).resolve().parents[1]
)).resolve()
PUBLIC = ROOT / "public"

ANALYTIC_SOURCE_COMMIT = "631127efdebbeaf5f41c60e16cb976e43fdbbfbf"
EXPERIMENT_PACKAGE_COMMIT = "ce0cfc6ad54060c1ac4fb1fa449e367f361f95ea"
FIGURE_PACKAGE_COMMIT = "07ed776a7f116f0a5f447c2f4c8b6203313d77eb"
RELEASE_BASELINE_COMMIT = "07ed776a7f116f0a5f447c2f4c8b6203313d77eb"
RELEASE_SOURCE_COMMIT = "TO_BE_FILLED_RELEASE_SOURCE_COMMIT"

COMMIT_PLACEHOLDERS = (
    ANALYTIC_SOURCE_COMMIT,
    EXPERIMENT_PACKAGE_COMMIT,
    FIGURE_PACKAGE_COMMIT,
    RELEASE_BASELINE_COMMIT,
    RELEASE_SOURCE_COMMIT,
)

RELEASE_SOURCE_EXACT_PATHS = (
    ".github/workflows/pages.yml",
    ".github/workflows/release-publication-gate.yml",
    "research/validate_figure_package.py",
    "scripts/r073k_release_content.py",
    "scripts/add-r073k-translations.mjs",
    "scripts/generate_r073k_release.py",
    "scripts/generate_r072o_release.py",
    "scripts/generate_r072p_release.py",
    "scripts/generate_note_index.py",
    "scripts/i18n-lib.mjs",
    "scripts/render-note-pdf.mjs",
    "scripts/bind-r073k-pdfs.mjs",
    "scripts/run-release-publication-gate.mjs",
    "tests/bilingual-content.test.mjs",
    "tests/internal-public-links.test.mjs",
    "tests/release-publication-gate-runner.test.mjs",
    "tests/release-publication-invariant.test.mjs",
    "tests/r073k-uniform-viscous-branch-gate.test.mjs",
    "tests/r073k-release.test.mjs",
    "tests/site-route-current-boundary.test.mjs",
)

BASELINE_EXACT_PATHS = (
    "VERSION",
    "research/release-manifest.json",
    "research/formal-archive-inventory.json",
    "public/site-version.json",
    "public/research-review.html",
    "public/literature-review.html",
    "public/recap-r0-61-r0-73j.html",
    "public/notes/index.html",
)

SOURCE_PATHS = (
    "research/r073k_problem_freeze.md",
    "research/r073k_uniform_viscous_branch_proof.md",
    "research/r073k_independent_analytic_audit.md",
    "research/r073k_adversarial_audit.md",
    "research/r073k_finite_diagnostic_audit.md",
    "research/r073k_literature_audit.md",
    "research/r073k_gap_matrix.md",
    "research/r073k_bilingual_dictionary.md",
    "research/r073k_report-source.md",
)

FIGURE_SOURCE_PATHS = (
    "README.md",
    "caption.md",
    "command.txt",
    "config.json",
    "contract.json",
    "plot.py",
    "qa-protocol.md",
    "qa-report.md",
    "requirements.txt",
    "validate.py",
)

FIGURE_PACKAGE_PATHS = (
    "README.md",
    "SHA256SUMS",
    "caption.md",
    "command.txt",
    "config.json",
    "contract.json",
    "environment.json",
    "figure.pdf",
    "figure.png",
    "figure.svg",
    "manifest.json",
    "plot.py",
    "progress.ndjson",
    "qa-final-size.png",
    "qa-grayscale.png",
    "qa-pdf.png",
    "qa-protocol.md",
    "qa-report.md",
    "requirements.txt",
    "resource-log.ndjson",
    "results.json",
    "source-data.csv",
    "validate.py",
    "validation.json",
)

PUBLIC_VOICE_BANS = (
    "我们", "攻关", "主攻", "突破", "研究纪律", "三重审计", "杀死错误想法",
)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def json_bytes(payload: object) -> bytes:
    return (json.dumps(payload, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def strict_json(path: Path, label: str) -> dict:
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
            path.read_text(encoding="utf-8"),
            parse_constant=reject,
            object_pairs_hook=unique,
        )
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        raise RuntimeError(label + ": invalid strict JSON") from exc
    if not isinstance(value, dict):
        raise RuntimeError(label + ": expected JSON object")
    return value


def assert_public_voice(value: str, label: str) -> None:
    for phrase in PUBLIC_VOICE_BANS:
        if phrase in value:
            raise RuntimeError(label + ": reader-facing voice violation " + phrase)


def replace_all(value: str, old: str, new: str, label: str) -> str:
    if old not in value:
        raise RuntimeError(label + ": source not found")
    return value.replace(old, new)


def require_commit(commit: str, label: str) -> None:
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise RuntimeError(label + ": expected full lowercase Git SHA")
    result = subprocess.run(
        ["git", "cat-file", "-t", commit], cwd=ROOT,
        capture_output=True, text=True,
    )
    if result.returncode != 0 or result.stdout.strip() != "commit":
        raise RuntimeError(label + ": not a commit object")


def is_ancestor(older: str, newer: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", older, newer], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def git_bytes(commit: str, relative: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{commit}:{relative}"], cwd=ROOT,
        check=True, capture_output=True,
    ).stdout


def git_paths(commit: str, relative: str) -> list[str]:
    output = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", commit, "--", relative],
        cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout
    return sorted(row for row in output.splitlines() if row)


def regular_flat_paths(directory: Path, label: str) -> list[str]:
    if not directory.is_dir() or directory.is_symlink():
        raise RuntimeError(label + ": missing real directory")
    rows: list[str] = []
    for path in directory.iterdir():
        if not path.is_file() or path.is_symlink():
            raise RuntimeError(label + ": non-regular entry " + path.name)
        rows.append(path.relative_to(ROOT).as_posix())
    return sorted(rows)


def normalized_release_generator(payload: bytes) -> bytes:
    try:
        value = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError("R0.73K release generator is not UTF-8") from exc
    value, count = re.subn(
        r'(?m)^RELEASE_SOURCE_COMMIT = "[^"]+"$',
        'RELEASE_SOURCE_COMMIT = "__NORMALIZED_RELEASE_SOURCE_COMMIT__"',
        value,
    )
    if count != 1:
        raise RuntimeError("R0.73K release generator must have exactly one release-source pin")
    return value.encode("utf-8")


def verify_exact_directory_at_commit(directory: Path, commit: str, label: str) -> None:
    current = regular_flat_paths(directory, label)
    frozen = git_paths(commit, directory.relative_to(ROOT).as_posix())
    if current != frozen:
        raise RuntimeError(label + ": directory inventory differs from sealed commit")
    for relative in current:
        if (ROOT / relative).read_bytes() != git_bytes(commit, relative):
            raise RuntimeError(label + ": file differs from sealed commit " + relative)



def verify_flat_ledger(
    directory: Path,
    label: str,
    *,
    require_sorted: bool,
    allowed_repository_paths: frozenset[str] = frozenset(),
) -> None:
    paths = regular_flat_paths(directory, label)
    ledger = directory / "SHA256SUMS"
    if ledger.relative_to(ROOT).as_posix() not in paths:
        raise RuntimeError(label + ": SHA256SUMS missing")
    declared: list[str] = []
    for row in ledger.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\\\r\n]+)", row)
        if match is None:
            raise RuntimeError(label + ": malformed SHA256SUMS row")
        relative = match.group(2)
        relative_path = PurePosixPath(relative)
        if (
            relative_path.is_absolute()
            or relative_path.as_posix() != relative
            or any(part in {"", ".", ".."} for part in relative_path.parts)
        ):
            raise RuntimeError(label + ": unsafe SHA256SUMS path " + relative)
        if "/" in relative:
            package_prefix = PurePosixPath(directory.relative_to(ROOT).as_posix())
            if relative_path.parent == package_prefix:
                path = ROOT / relative_path
            elif relative in allowed_repository_paths:
                path = ROOT / relative_path
            else:
                raise RuntimeError(label + ": undeclared repository ledger path " + relative)
        else:
            path = directory / relative
        resolved = path.resolve()
        if resolved == ROOT or ROOT not in resolved.parents:
            raise RuntimeError(label + ": ledger path escaped repository " + relative)
        if relative in declared or not path.is_file() or path.is_symlink():
            raise RuntimeError(label + ": invalid ledger entry " + relative)
        if digest(path) != match.group(1):
            raise RuntimeError(label + ": hash mismatch " + relative)
        declared.append(relative)
    if require_sorted and declared != sorted(declared):
        raise RuntimeError(label + ": ledger is not sorted")
    local_declared = sorted(
        (directory / relative).relative_to(ROOT).as_posix()
        if "/" not in relative else relative
        for relative in declared
        if "/" not in relative
        or Path(relative).parent == directory.relative_to(ROOT)
    )
    actual = sorted(
        path.relative_to(ROOT).as_posix() for path in directory.iterdir()
        if path.name not in {"SHA256SUMS", "package_validation.json"}
    )
    if local_declared != actual:
        raise RuntimeError(label + ": ledger inventory is not exact"
                           + f"; declared={local_declared}; actual={actual}")


def verify_baseline_sources() -> None:
    for relative in BASELINE_EXACT_PATHS:
        path = ROOT / relative
        if not path.is_file() or path.is_symlink():
            raise RuntimeError("R0.73K baseline source is not a regular file: " + relative)
        if path.read_bytes() != git_bytes(RELEASE_BASELINE_COMMIT, relative):
            raise RuntimeError("R0.73K baseline source differs from frozen commit: " + relative)
    verify_exact_directory_at_commit(
        PUBLIC / "notes", RELEASE_BASELINE_COMMIT, "R0.73K baseline notes",
    )

def ensure_commits_ready() -> None:
    if any(value.startswith("TO_BE_FILLED_") for value in COMMIT_PLACEHOLDERS):
        raise RuntimeError(
            "R0.73K release is intentionally sealed shut: replace every "
            "commit placeholder only after the corresponding frozen commit"
        )
    chain = (("analytic source", ANALYTIC_SOURCE_COMMIT),
             ("complete experiment package", EXPERIMENT_PACKAGE_COMMIT),
             ("complete figure package", FIGURE_PACKAGE_COMMIT),
             ("release baseline", RELEASE_BASELINE_COMMIT),
             ("release source", RELEASE_SOURCE_COMMIT))
    for label, commit in chain:
        require_commit(commit, "R0.73K " + label)
    for (left_label, left), (right_label, right) in zip(chain, chain[1:]):
        if not is_ancestor(left, right):
            raise RuntimeError(f"R0.73K commit order invalid: {left_label} < {right_label}")
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()
    if not is_ancestor(RELEASE_SOURCE_COMMIT, head):
        raise RuntimeError("R0.73K release source commit is not an ancestor of HEAD")
    generator_relative = "scripts/generate_r073k_release.py"
    for relative in RELEASE_SOURCE_EXACT_PATHS:
        if relative == generator_relative:
            continue
        if git_bytes(RELEASE_SOURCE_COMMIT, relative) != (ROOT / relative).read_bytes():
            raise RuntimeError("R0.73K release source is not pinned: " + relative)
    frozen = normalized_release_generator(git_bytes(RELEASE_SOURCE_COMMIT, generator_relative))
    current = normalized_release_generator((ROOT / generator_relative).read_bytes())
    if frozen != current:
        raise RuntimeError("R0.73K release generator differs from pinned source outside its self pin")

def validate_analytic_sources() -> None:
    source_text: dict[str, str] = {}
    for relative in SOURCE_PATHS:
        path = ROOT / relative
        if not path.is_file() or path.is_symlink():
            raise RuntimeError("missing R0.73K analytic source: " + relative)
        if path.read_bytes() != git_bytes(ANALYTIC_SOURCE_COMMIT, relative):
            raise RuntimeError("R0.73K source differs from analytic source commit: " + relative)
        source_text[relative] = path.read_text(encoding="utf-8")
    combined = "\n".join(source_text.values())
    for token in (
        "Gamma_*", "1/450", "0.12", "0.16", "1/25", "9/5", "5/9",
        "O(\\varepsilon)", "fullNormResolventConvergence=FALSE",
        "ANALYTIC PASS", "1,190", "952", "Clay",
    ):
        if token not in combined:
            raise RuntimeError("R0.73K analytic source missing boundary token: " + token)
    gap = source_text["research/r073k_gap_matrix.md"]
    for index in range(13):
        if f"K{index}" not in gap:
            raise RuntimeError("R0.73K gap matrix lost K" + str(index))
    if "K8" not in gap or "OPEN" not in gap or "K9" not in gap or "CLOSED" not in gap:
        raise RuntimeError("R0.73K threshold or finite-diagnostic boundary drifted")
    finite = source_text["research/r073k_finite_diagnostic_audit.md"].lower()
    if "continuum" not in finite or "finite" not in finite:
        raise RuntimeError("R0.73K finite audit lost continuum boundary")
    for label, value in source_text.items():
        assert_public_voice(value, "R0.73K " + label)

def validate_experiment() -> dict:
    directory = ROOT / "experiments/r073k"
    verify_exact_directory_at_commit(directory, EXPERIMENT_PACKAGE_COMMIT, "R0.73K experiment")
    verify_flat_ledger(
        directory,
        "R0.73K experiment",
        require_sorted=False,
        allowed_repository_paths=frozenset({
            "research/r073k_viscous_branch_diagnostic.py",
        }),
    )
    manifest = strict_json(directory / "manifest.json", "R0.73K experiment manifest")
    primary = strict_json(directory / "viscous_branch_diagnostic.json", "R0.73K primary")
    independent = strict_json(directory / "independent_validation.json", "R0.73K independent")
    package = strict_json(directory / "package_validation.json", "R0.73K package validation")
    schemas = {
        "manifest": (manifest, "r073k-finite-diagnostic-manifest-v1"),
        "primary": (primary, "r073k-viscous-branch-diagnostic-v1"),
        "independent": (independent, "r073k-independent-finite-validation-v1"),
        "package": (package, "r073k-package-validation-v1"),
    }
    for label, (payload, expected) in schemas.items():
        if payload.get("schemaVersion") != expected:
            raise RuntimeError("R0.73K experiment " + label + " schema drifted")
    if (
        manifest.get("release") != "R0.73K"
        or manifest.get("status") != "sealed"
        or not all(manifest.get("checks", {}).values())
        or primary.get("status") != "passed"
        or primary.get("allChecksPass") is not True
        or not all(primary.get("checks", {}).values())
        or independent.get("status") != "passed"
        or independent.get("allChecksPass") is not True
        or not all(independent.get("checks", {}).values())
        or package.get("status") != "passed"
        or package.get("allChecksPass") is not True
        or not all(package.get("checks", {}).values())
    ):
        raise RuntimeError("R0.73K finite diagnostic failed")
    if manifest.get("claimBoundary") != {
        "clayProblemSolved": False,
        "continuumTheoremCertifiedByThisManifest": False,
        "finiteDimensionalDiagnosticSealed": True,
    }:
        raise RuntimeError("R0.73K experiment claim boundary drifted")
    if independent.get("claimBoundary", {}).get(
        "continuumTheoremCertifiedByThisValidator"
    ) is not False:
        raise RuntimeError("R0.73K independent validator escaped finite scope")
    details = package.get("details", {})
    if (
        details.get("primaryRows") != 1190
        or details.get("crossCutoffRows") != 952
        or details.get("checksumCount") != 16
        or details.get("manifestFileCount") != 15
    ):
        raise RuntimeError("R0.73K finite package inventory drifted")
    if (
        len(primary.get("rows", [])) != 1190
        or len(primary.get("crossCutoffComparisons", [])) != 952
        or len(independent.get("sentinels", [])) != 8
    ):
        raise RuntimeError("R0.73K row or sentinel inventory drifted")
    errors = independent.get("maximumAbsoluteErrors", {})
    if not (
        errors.get("lambdaReal", 1.0) < 1.1e-14
        and errors.get("projectorDifferenceFromEpsilonZero", 1.0) < 5.0e-14
        and errors.get("lambdaQuotientReal", 1.0) < 3.7e-7
    ):
        raise RuntimeError("R0.73K independent comparison drifted")
    maximums = primary.get("maximums", {})
    if not (
        maximums.get("largestTwoCutoffsCoreEigenvalueDifference", 1.0) < 7.6e-15
        and maximums.get("largestTwoCutoffsCoreEmbeddedProjectorDifference", 1.0) < 5.7e-14
        and maximums.get("rightAlgebraicResidual", 1.0) < 1.7e-14
        and maximums.get("leftAlgebraicResidual", 1.0) < 8.1e-15
    ):
        raise RuntimeError("R0.73K primary maximums drifted")
    for row in manifest.get("files", []):
        relative = str(row.get("path", ""))
        path = ROOT / relative
        if not path.is_file() or path.is_symlink():
            raise RuntimeError("R0.73K manifest file missing: " + relative)
        if digest(path) != row.get("sha256") or path.stat().st_size != row.get("bytes"):
            raise RuntimeError("R0.73K manifest binding drifted: " + relative)
    return manifest

def validate_figure() -> dict:
    directory = ROOT / FIGURE_RELATIVE
    verify_exact_directory_at_commit(directory, FIGURE_PACKAGE_COMMIT, "R0.73K figure")
    verify_flat_ledger(directory, "R0.73K figure", require_sorted=True)
    manifest = strict_json(directory / "manifest.json", "R0.73K figure manifest")
    results = strict_json(directory / "results.json", "R0.73K figure results")
    contract = strict_json(directory / "contract.json", "R0.73K figure contract")
    config = strict_json(directory / "config.json", "R0.73K figure config")
    validation = strict_json(directory / "validation.json", "R0.73K figure validation")
    schemas = {
        "manifest": (manifest, "r073k-uniform-viscous-branch-figure-manifest-v1"),
        "results": (results, "r073k-uniform-viscous-branch-figure-results-v1"),
        "contract": (contract, "r073k-uniform-viscous-branch-figure-contract-v1"),
        "config": (config, "r073k-uniform-viscous-branch-figure-config-v1"),
        "validation": (validation, "r073k-uniform-viscous-branch-figure-validation-v1"),
    }
    for label, (payload, expected) in schemas.items():
        if payload.get("schemaVersion") != expected:
            raise RuntimeError("R0.73K figure " + label + " schema drifted")
    if (
        manifest.get("release") != "R0.73K"
        or manifest.get("figureId") != FIGURE_ID
        or manifest.get("status") != "formal"
        or results.get("status") != "passed"
        or results.get("allChecksPass") is not True
        or validation.get("status") != "passed"
        or not all(validation.get("checks", {}).values())
    ):
        raise RuntimeError("R0.73K figure status failed")
    boundary = manifest.get("claimBoundary", {})
    expected_boundary = {
        "adiabaticRemainderCertified": False,
        "clayProblemSolved": False,
        "continuumViscousBranchCertifiedByFigure": False,
        "explicitContinuumViscosityThresholdCertified": False,
        "finiteDimensionalDiagnostic": True,
        "finiteTimeSingularityCertified": False,
        "formalValidatedDiagnosticFigure": True,
        "independentFiniteRecomputationPassed": True,
        "nonlinearNavierStokesCertified": False,
        "transverseThreeDimensionalClosureCertified": False,
    }
    if (
        boundary != expected_boundary
        or results.get("claimBoundary") != boundary
        or validation.get("claimBoundary") != boundary
    ):
        raise RuntimeError("R0.73K figure claim boundaries disagree")
    if results.get("rowCounts") != {
        "crossCutoff": 952,
        "crossCutoffSummaries": 4,
        "cutoffSummaries": 5,
        "displayCore": 204,
        "primary": 1190,
        "sourceData": 213,
    }:
        raise RuntimeError("R0.73K figure row counts drifted")
    decisions = results.get("decisions", {})
    if not (
        decisions.get("maximumCoreLambdaImaginaryAbs", 1.0) < 1.4e-15
        and decisions.get("maximumCoreProjectorDifference", 1.0) < 0.181
        and decisions.get("maximumCoreProjectorNorm", 2.0) < 1.684
        and decisions.get("minimumCoreLeftRightOverlap", 0.0) > 0.593
        and decisions.get("largestTwoCutoffsCoreEigenvalueDifference", 1.0) < 7.6e-15
        and decisions.get("largestTwoCutoffsCoreEmbeddedProjectorDifference", 1.0) < 5.7e-14
    ):
        raise RuntimeError("R0.73K figure decisions drifted")
    formats = validation.get("formats", {})
    if (
        validation.get("allChecksPass") is not True
        or validation.get("automaticStatus") != "passed"
        or len(validation.get("checks", {})) != 22
        or formats.get("pngPixels") != [4204, 2787]
        or formats.get("pngDpiMetadata") != [599.9988, 599.9988]
        or formats.get("pdfImageXObjects") != 0
        or formats.get("svgRasterImages") != 0
    ):
        raise RuntimeError("R0.73K figure validation details drifted")
    actual = tuple(path.name for path in sorted(directory.iterdir()))
    if actual != tuple(sorted(FIGURE_PACKAGE_PATHS)):
        raise RuntimeError("R0.73K figure package inventory drifted")
    rows = manifest.get("files", [])
    declared = {str(row.get("path", "")): row for row in rows if isinstance(row, dict)}
    expected_declared = set(FIGURE_PACKAGE_PATHS) - {"manifest.json", "SHA256SUMS"}
    if set(declared) != expected_declared:
        raise RuntimeError("R0.73K figure manifest inventory drifted")
    for name, row in declared.items():
        path = directory / name
        if digest(path) != row.get("sha256") or path.stat().st_size != row.get("bytes"):
            raise RuntimeError("R0.73K figure manifest hash drifted: " + name)
    for row in manifest.get("inputBindings", []):
        relative = str(row.get("path", ""))
        path = ROOT / relative
        if not path.is_file() or digest(path) != row.get("sha256"):
            raise RuntimeError("R0.73K figure input binding drifted: " + relative)
        if git_bytes(EXPERIMENT_PACKAGE_COMMIT, relative) != path.read_bytes():
            raise RuntimeError("R0.73K figure input differs from experiment commit: " + relative)
    for name in FIGURE_SOURCE_PATHS:
        relative = f"{FIGURE_RELATIVE}/{name}"
        if git_bytes(FIGURE_PACKAGE_COMMIT, relative) != (directory / name).read_bytes():
            raise RuntimeError("R0.73K figure source differs from figure commit: " + name)
    if not (directory / "figure.pdf").read_bytes().startswith(b"%PDF"):
        raise RuntimeError("R0.73K figure PDF signature invalid")
    svg = (directory / "figure.svg").read_text(encoding="utf-8").lower()
    if "<svg" not in svg or "<image" in svg or "<text" not in svg:
        raise RuntimeError("R0.73K figure SVG is absent or rasterized")
    png = (directory / "figure.png").read_bytes()
    if not png.startswith(b"\x89PNG\r\n\x1a\n") or b"pHYs" not in png:
        raise RuntimeError("R0.73K figure PNG metadata missing")
    return manifest
def validate_inputs() -> tuple[dict, dict]:
    ensure_commits_ready()
    validate_analytic_sources()
    experiment = validate_experiment()
    figure = validate_figure()
    return experiment, figure


def _target_html() -> dict[str, str]:
    target: dict[str, str] = {}
    for relative in (
        "notes/r0-73k.html",
        "recap-r0-61-r0-73k.html",
        "research-review.html",
        "literature-review.html",
        "notes/index.html",
    ):
        path = PUBLIC / relative
        if not path.is_file() or path.is_symlink():
            raise RuntimeError("R0.73K target HTML missing: " + relative)
        value = path.read_text(encoding="utf-8")
        assert_clean(value, "R0.73K target " + relative)
        assert_mathjax_clean(value, "R0.73K target " + relative, check_naked=True)
        assert_public_voice(value, "R0.73K target " + relative)
        if "/i18n-en.js?v=1.51" not in value:
            raise RuntimeError("R0.73K target HTML has stale i18n cache: " + relative)
        target[relative] = value
    return target


def preflight_release_state() -> str:
    release = strict_json(ROOT / "research/release-manifest.json", "release manifest")
    site = strict_json(PUBLIC / "site-version.json", "site version")
    inventory = strict_json(ROOT / "research/formal-archive-inventory.json", "archive inventory")
    root_version = (ROOT / "VERSION").read_text(encoding="utf-8")

    if release.get("latestCompletedRelease") == "r073k":
        for key, value in R073K_TARGET.items():
            if release.get(key) != value:
                raise RuntimeError("R0.73K target release-manifest drifted: " + key)
        if release.get("latestReleaseGate") != "tests/r073k-uniform-viscous-branch-gate.test.mjs":
            raise RuntimeError("R0.73K target gate binding drifted")
        if release.get("latestReleasePublicationTest") != "tests/r073k-release.test.mjs":
            raise RuntimeError("R0.73K target publication-test binding drifted")
        if site != {
            "schemaVersion": "research-site-version-v1",
            "version": "1.51",
            "latestRelease": "R0.73K",
            "publicHtmlNoteCount": 187,
            "publishedDate": "2026-08-31",
        } or root_version != "1.51\n":
            raise RuntimeError("R0.73K target site version drifted")
        state = (
            inventory.get("latestPublishedRelease"),
            inventory.get("publishedReleaseCount"),
            inventory.get("formalSealedReleaseCount"),
            inventory.get("legacyFormalFigureBacklogCount"),
        )
        if state != ("r073k", 89, 65, 24):
            raise RuntimeError("R0.73K target formal archive is not exact")
        baseline_inventory = json.loads(git_bytes(
            RELEASE_BASELINE_COMMIT, "research/formal-archive-inventory.json"
        ))
        expected = json.loads(json.dumps(baseline_inventory))
        for key in ("publishedReleases", "formalSealedReleases"):
            rows = expected.get(key)
            if not isinstance(rows, list) or rows[-1:] != ["r073j"] or "r073k" in rows:
                raise RuntimeError("R0.73K sealed baseline inventory invalid: " + key)
            rows.append("r073k")
        expected.update({
            "latestPublishedRelease": "r073k",
            "publishedReleaseCount": 89,
            "formalSealedReleaseCount": 65,
            "legacyFormalFigureBacklogCount": 24,
        })
        if inventory != expected:
            raise RuntimeError("R0.73K target archive is not exact append-only successor")
        for key, count in (("publishedReleases", 89), ("formalSealedReleases", 65)):
            rows = inventory.get(key, [])
            if len(rows) != count or len(set(rows)) != count:
                raise RuntimeError("R0.73K target archive sequence drifted: " + key)
        if not set(inventory["formalSealedReleases"]).issubset(inventory["publishedReleases"]):
            raise RuntimeError("R0.73K sealed inventory escaped published inventory")
        if release.get("formalArchiveInventory") != {
            "path": "research/formal-archive-inventory.json",
            "sha256": digest(ROOT / "research/formal-archive-inventory.json"),
        }:
            raise RuntimeError("R0.73K target archive binding drifted")
        if len(list((PUBLIC / "notes").glob("r0-*.html"))) != 187:
            raise RuntimeError("R0.73K target note count is not 187")
        html = _target_html()
        expected_html = {
            "notes/r0-73k.html": build_note(),
            "recap-r0-61-r0-73k.html": build_recap(),
            "research-review.html": update_home(),
            "literature-review.html": update_literature(),
            "notes/index.html": build_note_index(json_bytes(site)),
        }
        for relative, expected in expected_html.items():
            if html[relative] != expected:
                raise RuntimeError(
                    "R0.73K target HTML differs from deterministic builder: " + relative
                )
        for token in (
            CLOSED, FINITE, OPEN, "NOT CLAY", "1190", "952",
            "0.12", "0.16", "1/25", "fullNormResolventConvergence=FALSE",
        ):
            if token not in html["notes/r0-73k.html"]:
                raise RuntimeError("R0.73K target note lost token: " + token)
        recap = html["recap-r0-61-r0-73k.html"]
        start = recap.find('<section id="node-index">')
        end = recap.find("</section>", start)
        links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', recap[start:end])
        if (
            start < 0 or end <= start
            or len(links) != 127 or len(set(links)) != 127
            or recap.count('<article class="phase">') != 46
        ):
            raise RuntimeError("R0.73K target recap inventory drifted")
        home = html["research-review.html"]
        route = re.search(
            r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73K">(.*?)</nav>',
            home, flags=re.S,
        )
        route_links = [] if route is None else re.findall(
            r'href="/notes/(r0-[^"]+)\.html"', route.group(1)
        )
        if (
            len(route_links) != 97 or len(set(route_links)) != 97
            or home.count('data-release="r073k"') != 1
        ):
            raise RuntimeError("R0.73K target home route drifted")
        if (
            'id="r073k-boundary"' not in html["literature-review.html"]
            or 'class="route-r073k-deck-update"' not in html["literature-review.html"]
        ):
            raise RuntimeError("R0.73K target literature boundary absent")
        if 'data-note="r0-73k"' not in html["notes/index.html"]:
            raise RuntimeError("R0.73K target note index absent")
        return "target"

    if any(release.get(key) != value for key, value in R073J_BASELINE.items()):
        raise RuntimeError("R0.73K state is neither exact R0.73J source nor exact target")
    if site != {
        "schemaVersion": "research-site-version-v1",
        "version": "1.50",
        "latestRelease": "R0.73J",
        "publicHtmlNoteCount": 186,
        "publishedDate": "2026-08-30",
    } or root_version != "1.50\n":
        raise RuntimeError("R0.73K baseline site version drifted")
    state = (
        inventory.get("latestPublishedRelease"), inventory.get("publishedReleaseCount"),
        inventory.get("formalSealedReleaseCount"), inventory.get("legacyFormalFigureBacklogCount"),
    )
    if state != ("r073j", 88, 64, 24):
        raise RuntimeError("R0.73K formal archive baseline drifted")
    verify_baseline_sources()
    if len(list((PUBLIC / "notes").glob("r0-*.html"))) != 186:
        raise RuntimeError("R0.73K expected exactly 186 baseline HTML notes")
    for path in (
        PUBLIC / "notes/r0-73k.html", PUBLIC / "notes/r0-73k.pdf",
        PUBLIC / "recap-r0-61-r0-73k.html", PUBLIC / "recap-r0-61-r0-73k.pdf",
        PUBLIC / "assets/r073k", PUBLIC / FIGURE_RELATIVE,
    ):
        if path.exists() or path.is_symlink():
            raise RuntimeError("R0.73K baseline path already exists: " + str(path))
    for relative, tokens in {
        "research-review.html": ("R0.73J", "186", "R0.73K"),
        "literature-review.html": ("R0.73J", "开放接口 · R0.73K"),
        "notes/index.html": ("R0.73J", "186 篇公开研究笔记"),
        "recap-r0-61-r0-73j.html": ("R0.61–R0.73J", "126", "45 个研究阶段"),
    }.items():
        value = (PUBLIC / relative).read_text(encoding="utf-8")
        for token in tokens:
            if token not in value:
                raise RuntimeError(f"R0.73K baseline {relative} missing {token}")
    return "source"


def build_note() -> str:
    html = git_bytes(
        RELEASE_BASELINE_COMMIT, "public/notes/r0-73j.html"
    ).decode("utf-8")
    metadata = (
        ("description", r'<meta name="description" content=".*?">',
         '<meta name="description" content="研究笔记 R0.73K：共同圆内唯一的实代数简单黏性谱支、Riesz 投影在算子范数下的一致收敛、固定半平面内无其他谱点，以及补空间预解式与半群增长上界。">'),
        ("og title", r'<meta property="og:title" content=".*?">',
         '<meta property="og:title" content="R0.73K｜Parameter-uniform viscous rank-one branch">'),
        ("og description", r'<meta property="og:description" content=".*?">',
         '<meta property="og:description" content="For the certified shear family, a parameter-uniform viscous rank-one branch is proved below an existential viscosity threshold, with operator-norm convergence of Riesz projections, an O(epsilon) eigenvalue-shift estimate, and fixed-half-plane reduced-resolvent and semigroup bounds.">'),
        ("og image", r'<meta property="og:image" content=".*?">',
         f'<meta property="og:image" content="https://kasifa.github.io/assets/r073k/{FIGURE_ID}.png">'),
        ("title", r'<title>.*?</title>',
         '<title>R0.73K｜Parameter-uniform viscous rank-one branch</title>'),
    )
    for label, pattern, value in metadata:
        html = section(html, pattern, value, "K note " + label)
    html = required(html, "/i18n-en.js?v=1.50", "/i18n-en.js?v=1.51", "K note i18n")
    toc_items = (
        ("result", "00 · direct result"),
        ("singular", "01 · singular limit"),
        ("projection", "02 · Riesz projection"),
        ("rate", "03 · first-order rate"),
        ("conditioning", "04 · conditioning"),
        ("halfplane", "05 · fixed half-plane"),
        ("audit", "06 · independent audits"),
        ("diagnostic", "07 · finite diagnostic"),
        ("figure", "08 · journal figure"),
        ("literature", "09 · literature boundary"),
        ("boundary", "10 · exact boundary"),
        ("value", "11 · value"),
        ("next", "12 · R0.73L"),
        ("reproduce", "13 · reproduction"),
    )
    nav = "<nav>" + "".join(
        f'<a href="#{anchor}">{label.split(" · ", 1)[1]}</a>'
        for anchor, label in toc_items
    ) + '<a href="/">返回主页</a></nav>'
    html = section(html, r'<nav><a href="#result">.*?</nav>', nav, "K note nav")
    html = section(html, r'    <header class="hero">.*?</header>', NOTE_HERO, "K note hero")
    toc = (
        '      <aside class="toc"><strong>CONTENTS</strong><ol>\n'
        + "".join(
            f'        <li><a href="#{anchor}">{label}</a></li>'
            for anchor, label in toc_items
        )
        + "\n      </ol></aside>"
    )
    html = section(html, r'      <aside class="toc">.*?</aside>', toc, "K note toc")
    html = section(html, r'      <article>.*?</article>', NOTE_ARTICLE, "K note article")
    footer = (
        "<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>"
        "我按原编号记录定理、有限计算、反例和未解决的问题。</div>"
        '<div>研究笔记 R0.73K · 2026-08-31<br><a href="/">返回研究主页</a></div></footer>'
    )
    html = section(html, r"<footer>.*?</footer>", footer, "K note footer")
    match = re.search(r"<nav>(.*?)</nav>", html, flags=re.S)
    anchors = re.findall(r'href="#([^"]+)"', match.group(1)) if match else []
    expected = [anchor for anchor, _ in toc_items]
    if anchors != expected or len(anchors) != len(set(anchors)):
        raise RuntimeError("R0.73K note nav anchors are not unique and ordered")
    for token in (CLOSED, FINITE, OPEN, "NOT CLAY", "1190", "952", "0.12", "0.16"):
        if token not in html:
            raise RuntimeError("R0.73K note lost token: " + token)
    assert_clean(html, "R0.73K note")
    assert_mathjax_clean(html, "R0.73K note", check_naked=True)
    assert_public_voice(html, "R0.73K note")
    return html


def build_recap() -> str:
    html = git_bytes(
        RELEASE_BASELINE_COMMIT, "public/recap-r0-61-r0-73j.html"
    ).decode("utf-8")
    metadata = (
        ("description", r'<meta name="description" content=".*?">',
         '<meta name="description" content="R0.60 之后的完整研究回顾：R0.61 到 R0.73K 共 127 个节点；最新一节闭合参数一致黏性 rank-one 谱支与补空间控制。">'),
        ("og title", r'<meta property="og:title" content=".*?">',
         '<meta property="og:title" content="R0.61–R0.73K｜R0.60 之后的研究回顾">'),
        ("og description", r'<meta property="og:description" content=".*?">',
         '<meta property="og:description" content="46 个阶段、127 个节点：从约化递推和环带排除到参数一致黏性谱支。">'),
        ("title", r"<title>.*?</title>",
         "<title>R0.61–R0.73K｜R0.60 之后的研究回顾</title>"),
    )
    for label, pattern, value in metadata:
        html = section(html, pattern, value, "K recap " + label)
    html = required(html, "/i18n-en.js?v=1.50", "/i18n-en.js?v=1.51", "K recap i18n")
    hero = r'''    <header class="hero"><div class="hero-inner"><div><div class="eyebrow">累计回顾 · R0.61–R0.73K · 2026-08-31</div><h1>R0.60 之后的研究回顾</h1><p class="lead">本页保留 R0.61 到 R0.73K 的全部 127 个节点。R0.61–R0.69W 从约化递推走到严格环带排除；R0.70A–R0.71Z 检查移动尺度、临界账本、内部 entry 与 complete-root 边界；R0.72A–R0.73B 处理 strong coupling、critical log、碰撞几何与完整线性 Fourier--Leray 行；R0.73C–I 依次处理冻结 Rayleigh 不稳定、黏性谱簇持续、固定正半平面传递、移动剖面增益、非线性相对放大、平面固定距离偏离与零窗口作用量边界。R0.73J 认证无黏连续谱支；R0.73K 在共同但未显式数值化的黏度阈值内闭合共同圆内唯一的实代数简单黏性谱支、Riesz 投影在算子范数下的一致收敛、特征值偏移的 \(O(\varepsilon)\) 上界、条件数、固定半平面内无其他谱点，以及补空间 reduced-resolvent 与半群增长上界。绝热跟踪、非线性、横向三维、奇性与 Clay 没有被外推。</p></div><div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.73K</strong><p>收录节点：127</p><p>回顾截止时公开笔记：187</p><p>回顾截止节点：R0.73K</p><p>问题状态：仍未解决</p></div></div></header>'''
    html = section(html, r'    <header class="hero">.*?</header>', hero, "K recap hero")
    for old, new in (
        ("02 · 126 节完整索引", "02 · 127 节完整索引"),
        ("01 · 45 个研究阶段", "01 · 46 个研究阶段"),
        ("R0.60 之后的路线分成 45 个阶段", "R0.60 之后的路线分成 46 个阶段"),
        ('data-current-route="R0.69P–R0.73J"', 'data-current-route="R0.69P–R0.73K"'),
    ):
        html = required(html, old, new, "K recap counter")
    result = r'''        <section id="result"><div class="section-no">00 / 回顾范围</div><h2>版本数、封存数和数学结论分开报告</h2><div class="metrics"><div class="metric"><strong>127</strong><span>R0.61–R0.73K 研究节点</span></div><div class="metric"><strong>89</strong><span>R0.70A–R0.73K 已公开版本</span></div><div class="metric"><strong>65</strong><span>当前 formal-figure 合同下完整封存</span></div><div class="metric"><strong>24</strong><span>旧版附图档案待回补</span></div></div><p>R0.00–R0.60 保留在上一份阶段回顾。R0.70A–R0.73K 的 89 个版本已经公开，其中 65 个满足当前完整封存合同，24 个历史版本仍欠 formal-figure 回补。公开和封存不表示 Clay 问题已经解决。</p></section>'''
    html = section(html, r'        <section id="result">.*?</section>', result, "K recap result")
    marker = '          </div>\n        </section>\n\n        <section id="node-index">'
    html = once(html, marker, RECAP_PHASE + "\n" + marker, "K recap phase")
    html = required(
        html, "R0.61–R0.73J 的 126 节公开笔记",
        "R0.61–R0.73K 的 127 节公开笔记", "K recap node title",
    )
    node_j = '            <span class="node-ref"><a href="/notes/r0-73j.html">R0.73J</a><span class="node-state kind-closed">闭</span></span>\n'
    node_k = '            <span class="node-ref"><a href="/notes/r0-73k.html">R0.73K</a><span class="node-state kind-closed">闭</span></span>\n'
    html = once(html, node_j, node_j + node_k, "K recap node")
    retained = (
        '            <li>R0.73K 闭合共同小黏度范围内、共同圆内唯一的实代数简单黏性谱支、'
        'Riesz 投影在算子范数下的一致收敛、特征值偏移的 \(O(\\varepsilon)\) 上界、条件数、固定半平面内无其他谱点，'
        '以及补空间 reduced-resolvent 与半群增长上界；显式黏度阈值、绝热跟踪、三维闭合、奇性与 Clay 保持 OPEN。</li>\n'
    )
    html = once(
        html, "          </ul>\n          <p>这些结果可以分别整理成",
        retained + "          </ul>\n          <p>这些结果可以分别整理成",
        "K recap retained",
    )
    value = r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>静态谱支输入已经具备，动态跟踪仍未证明</h2><p>不能把 127 个节点或 89 个公开版本解释成 Clay 完成比例。R0.73K 的严格增量是共同圆内参数一致的黏性 rank-one 谱支、Riesz 投影在算子范数下的一致收敛、特征值偏移的 \(O(\varepsilon)\) 上界、固定半平面内无其他谱点，以及补空间 reduced-resolvent 与半群增长上界；共同阈值只以存在性方式给出，尚未显式量化，非自伴绝热跟踪、非线性增长与横向三维仍未证明。</p></section>'''
    html = section(html, r'        <section id="value">.*?</section>', value, "K recap value")
    next_gate = r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.73L 检查非自伴绝热跟踪</h2><p>下一节在共同定义域和上述非正规谱分解下估计移动投影耦合，检查 \(D_*/\varepsilon\) 时间尺度上的有界前因子和匹配作用量。</p></section>'''
    html = section(html, r'        <section id="next">.*?</section>', next_gate, "K recap next")
    claims = r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>连续定理、有限诊断和开放问题分开列示</h2><p>R0.70A–R0.73K 的 89 节已公开；65 节完整封存；24 节旧档待回补。</p><p>__CLOSED__。</p><p>__FINITE__。</p><p>__OPEN__。</p><p>1,190 个有限谱状态和 952 个跨 cutoff 比较只验证两个有限实现的一致性，不认证连续 Riesz 秩、共同黏度阈值或补空间半群上界。NOT CLAY。</p></section>'''
    claims = claims.replace("__CLOSED__", CLOSED).replace("__FINITE__", FINITE).replace("__OPEN__", OPEN)
    html = section(html, r'        <section id="claims">.*?</section>', claims, "K recap claims")
    reproduce = r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证明、审计、实验、附图和历史回顾</h2><p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-73j.html">保留 R0.73J 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-73k.html">打开最新节点 R0.73K</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073k_uniform_viscous_branch_proof.md">查看解析证明</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073k_independent_analytic_audit.md">查看独立解析审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073k_adversarial_audit.md">查看反例式审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/experiments/r073k">查看有限诊断包</a> · <a href="/assets/r073k/__FIGURE_ID__.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-73k.pdf">下载同步 PDF</a></p><p>连续定理由解析证明承担；有限诊断只作可复现错误探测。</p></section>'''.replace("__FIGURE_ID__", FIGURE_ID)
    html = section(html, r'        <section id="reproduce">.*?</section>', reproduce, "K recap reproduce")
    footer = r'''  <footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>我按原编号记录定理、有限计算、反例和未解决的问题。</div><div>R0.61–R0.73K 回顾 · 2026-08-31<br><a href="/">返回研究主页</a></div></footer>'''
    html = section(html, r"  <footer>.*?</footer>", footer, "K recap footer")
    start = html.find('<section id="node-index">')
    end = html.find("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', html[start:end])
    if len(links) != 127 or len(set(links)) != 127:
        raise RuntimeError("R0.73K recap expected 127 unique nodes")
    if html.count('<article class="phase">') != 46:
        raise RuntimeError("R0.73K recap expected 46 phases")
    assert_clean(html, "R0.73K recap")
    assert_mathjax_clean(html, "R0.73K recap", check_naked=True)
    assert_public_voice(html, "R0.73K recap")
    return html


def update_home() -> str:
    html = git_bytes(
        RELEASE_BASELINE_COMMIT, "public/research-review.html"
    ).decode("utf-8")
    html = section(
        html,
        r'    <section class="route-overview latest-release-spotlight".*?</section>',
        HOME_LATEST_SPOTLIGHT,
        "K home latest spotlight",
    )
    for old, new in (
        ('data-site-version="1.50"', 'data-site-version="1.51"'),
        ("/i18n-en.js?v=1.50", "/i18n-en.js?v=1.51"),
        ("/site-refresh.js?v=1.50", "/site-refresh.js?v=1.51"),
        ("<strong>v1.50</strong>网页版本", "<strong>v1.51</strong>网页版本"),
        ("<strong>186</strong>公开研究笔记", "<strong>187</strong>公开研究笔记"),
        ("<strong>R0.73J</strong>最新研究节点", "<strong>R0.73K</strong>最新研究节点"),
        ('<a class="route-map-latest" href="#r073j">跳到首页 R0.73J 卡片 →</a>',
         '<a class="route-map-latest" href="#r073k">跳到首页 R0.73K 卡片 →</a>'),
        ("viscous branch / uniform projection control",
         "non-selfadjoint adiabatic tracking / bounded prefactor"),
        ("Research topology · R0.1–R0.73J", "Research topology · R0.1–R0.73K"),
        ("R0.70A–R0.73J：88 节已公开，64 节完整封存",
         "R0.70A–R0.73K：89 节已公开，65 节完整封存"),
        ('<span class="route-range">R0.69P–R0.73J</span>',
         '<span class="route-range">R0.69P–R0.73K</span>'),
        ('aria-label="R0.69P–R0.73J"', 'aria-label="R0.69P–R0.73K"'),
        ("展开 96 篇公开笔记", "展开 97 篇公开笔记"),
        ("本站 R0.69P–R0.73J 路线", "本站 R0.69P–R0.73K 路线"),
        ("综述 v1.50 · 2026-08-30", "综述 v1.51 · 2026-08-31"),
        ("上次综述 v1.49 · 2026-08-30", "上次综述 v1.50 · 2026-08-30"),
    ):
        html = required(html, old, new, "K home " + old)
    html = replace_all(
        html, "/recap-r0-61-r0-73j.html", "/recap-r0-61-r0-73k.html",
        "K home recap HTML links",
    )
    html = replace_all(
        html, "/recap-r0-61-r0-73j.pdf", "/recap-r0-61-r0-73k.pdf",
        "K home recap PDF links",
    )
    historical = (r'<strong style="color:var(--gold)">下一步 R0.73K：</strong>&nbsp;'
                  r'认证黏性谱支和统一投影控制。')
    html = required(
        html, historical, historical.replace("下一步", "当时的下一步"),
        "K home historical next",
    )
    focus = r'<div class="summary-item"><strong>我目前关注</strong><span>R0.73K 已闭合共同圆内参数一致的黏性 rank-one 谱支、Riesz 投影在算子范数下的一致收敛、特征值偏移的 \(O(\varepsilon)\) 上界、条件数、固定半平面内无其他谱点，以及补空间 reduced-resolvent 与半群增长上界。共同黏度阈值只以存在性方式给出，尚未显式量化；下一关是非自伴绝热跟踪。</span></div>'
    html = section(
        html,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        focus,
        "K home focus",
    )
    html = required(
        html,
        "<h3>R0.73J：周期 Rayleigh 连续算子上的唯一简单最右谱支已认证</h3>",
        "<h3>R0.73K：参数一致黏性 rank-one 谱支与补空间控制已闭合</h3>",
        "K home current title",
    )
    html = required(
        html, "<span>R0.72R–R0.73J：</span>", "<span>R0.72R–R0.73K：</span>",
        "K home path range",
    )
    html = required(
        html,
        "endpoint audit / continuum upper action / zero-window tangent → unique simple rightmost spectral branch of the continuum operator</p>",
        "endpoint audit / continuum upper action / zero-window tangent → unique simple rightmost continuum branch → parameter-uniform viscous rank-one branch</p>",
        "K home path tail",
    )
    link_j = '<a class="milestone" href="/notes/r0-73j.html">R0.73J</a>'
    html = once(
        html, link_j,
        link_j + '\n                  <a class="milestone" href="/notes/r0-73k.html">R0.73K</a>',
        "K home route link",
    )
    route_j = r'''              <p>R0.73J 认证周期 Rayleigh 连续算子上的唯一简单最右谱支 \(\lambda_0(d)\in(0.167,0.173)\)、严格谱隙 \(>0.057\)、左右重叠和固定相位锚。自然盒首轮 76/83、depth-two 1/7 的 wrapping 历史保留；自适应 depth five 最终覆盖 83/83 个选定盒。</p>
'''
    route_k = r'''              <p>R0.73K 证明：在共同但未显式量化的黏度阈值内，无黏特征值在整个 \(d\in[0,1/450]\) 上延拓为共同圆内唯一的实代数简单黏性谱支；Riesz 投影在算子范数下一致收敛，特征值偏移满足 \(O(\varepsilon)\) 上界。固定半平面 \(\operatorname{Re}z\ge0.12\) 内无其他谱点；选定 rank-one 谱块的逆向指数 \(0.16\) 与保守安全间隔 \(1/25\) 同时受控。<span>parameter-uniform viscous rank-one branch</span>；<span>finite diagnostic: 1190 states / 952 cross-cutoff comparisons</span>。有限数据只作诊断。</p>
'''
    html = once(html, route_j, route_j + route_k, "K home current route summary")
    html = section(
        html, r'            <article class="tree-node next">.*?</article>',
        HOME_NEXT, "K home next gate",
    )
    recap = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem"><p class="eyebrow">累计回顾 R0.61–R0.73K · 2026-08-31</p><h3>R0.60 recap 之后的累计回顾收录 127 个节点；全站现有 187 篇公开研究笔记</h3><p>累计回顾现分 46 个阶段，完整保留 R0.61–R0.73K；最新节点分开记录奇异极限证明、两份解析审计、有限诊断和开放问题。</p><p>R0.70A–R0.73K 共 89 个版本已公开；65 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p><p><strong>阶段判断：</strong>&nbsp;静态黏性谱支、补空间 reduced-resolvent 与半群增长上界已经闭合；显式黏度阈值、非自伴绝热、非线性、横向三维、奇性与 Clay 保持 OPEN。</p><p><a href="/recap-r0-61-r0-73k.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-73k.pdf">下载同步 PDF</a></p></div>'''
    html = section(
        html, r'          <div class="task-one" id="post-r060-recap".*?</div>',
        recap, "K home recap",
    )
    marker = '          </div>\n        </section>\n\n      </article>'
    html = once(
        html, marker,
        '          </div>\n\n' + HOME_K_CARD + '\n        </section>\n\n      </article>',
        "K home card",
    )
    if html.count('data-release="r073k"') != 1:
        raise RuntimeError("home must contain exactly one R0.73K card")
    if html.count('<strong style="color:var(--gold)">下一步 R0.73L：') != 1:
        raise RuntimeError("home must contain exactly one current R0.73L gate")
    route = re.search(
        r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73K">(.*?)</nav>',
        html, flags=re.S,
    )
    links = [] if route is None else re.findall(
        r'href="/notes/r0-[^"]+\.html"', route.group(1)
    )
    if len(links) != 97 or len(set(links)) != 97:
        raise RuntimeError("home current-route index must contain 97 unique note links")
    assert_clean(html, "R0.73K home")
    assert_mathjax_clean(html, "R0.73K home", check_naked=True)
    assert_public_voice(html, "R0.73K home")
    return html


def update_literature() -> str:
    html = git_bytes(
        RELEASE_BASELINE_COMMIT, "public/literature-review.html"
    ).decode("utf-8")
    for old, new in (
        ("/i18n-en.js?v=1.50", "/i18n-en.js?v=1.51"),
        ("本站 R0.69P–R0.73J 只列为研究笔记",
         "本站 R0.69P–R0.73K 只列为研究笔记"),
        ("文献综述 v1.50 · 2026-08-30", "文献综述 v1.51 · 2026-08-31"),
        ("累计回顾与 126 节索引", "累计回顾与 127 节索引"),
        ("打开 126 节完整索引", "打开 127 节完整索引"),
    ):
        html = required(html, old, new, "K literature " + old)
    html = replace_all(
        html, "/recap-r0-61-r0-73j.html", "/recap-r0-61-r0-73k.html",
        "K literature recap links",
    )
    deck_j = r'''<span class="route-r073j-deck-update">R0.73J 在连续算子层面认证周期 Rayleigh 唯一简单最右谱支、显式谱隙、左右重叠和固定相位锚。自然盒首轮 76/83、depth-two 1/7 的失败历史保留；自适应 depth five 最终覆盖 83/83 个选定盒与 2896/2896 个叶盒。</span></p>'''
    deck_k = deck_j[:-4] + r'''<span class="route-r073k-deck-update">R0.73K 在共同但未显式量化的黏度阈值内闭合共同圆内唯一的实代数简单黏性谱支、Riesz 投影在算子范数下的一致收敛、特征值偏移的 \(O(\varepsilon)\) 上界、条件数、固定半平面内无其他谱点，以及补空间 reduced-resolvent 与半群增长上界。1,190 个有限状态与 952 个跨 cutoff 比较只作诊断。</span></p>'''
    html = required(html, deck_j, deck_k, "K literature route deck endpoint")
    old_open = r'''<div class="route-step pause"><header><b>开放接口 · R0.73K</b><strong>viscous branch and uniform projection control</strong></header><p>检查小黏性扰动下的唯一谱支、Riesz 投影和补空间半群界；随后再处理非自伴绝热余项。</p></div>'''
    new_steps = r'''<div class="route-step kept"><header><b>R0.73K</b><strong>parameter-uniform viscous rank-one branch</strong></header><p>共同小黏度范围内、共同圆内唯一的实代数简单黏性谱支、Riesz 投影在算子范数下的一致收敛、特征值偏移的 \(O(\varepsilon)\) 上界、固定半平面内无其他谱点，以及补空间 reduced-resolvent 与半群增长上界已经闭合。共同阈值只以存在性方式给出，尚未显式量化。<a href="/notes/r0-73k.html">研究笔记</a> <a href="/recap-r0-61-r0-73k.html">当前累计回顾</a> <a href="#r073k-boundary">文献边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.73L</b><strong>non-selfadjoint adiabatic tracking</strong></header><p>在共同定义域和上述非正规谱分解下估计移动投影耦合，检查 \(D_*/\varepsilon\) 时间尺度上的有界前因子和匹配作用量。</p></div>'''
    html = once(html, old_open, new_steps, "K literature route")
    boundary = r'''

          <h3 id="r073k-boundary">R0.73K 的黏性消失谱持续文献边界</h3>
          <p><a href="#ref-156">Shvydkoy--Friedlander</a>已经证明一般环面 Navier--Stokes 算子中、位于 Euler 本质谱阈值右侧的孤立不稳定谱在黏性消失时持续，总代数重数保持。因此 R0.73K 不声称首个一般谱持续定理。<a href="#ref-157">Kato 的一般结果</a>表明，全预解式若按算子范数收敛，紧 resolvent 性会传至极限；结合本模型两端的紧性差异可知该收敛不可能成立。</p>
          <p><a href="#ref-158">collectively compact 理论</a>与<a href="#ref-159">operator Rouché 理论</a>提供有限维谱块保持的先例。<a href="#ref-160">Li--Lin</a>、<a href="#ref-161">Quarisa--Rodrigo</a>、<a href="#ref-162">Grenier--Nguyen</a>和<a href="#ref-163">Y. C. Li</a>处理不同周期、通道或边界层几何中的黏性模态；它们的尺度与本节固定 \(\gamma=1/2\) 的无壁周期问题不同。<a href="#ref-164">近期周期长波结果</a>要求波数随黏度缩放，不能直接覆盖这里的固定波数极限。</p>
          <p><a href="#ref-165">周期 Evans 理论</a>没有自动给出降阶奇异极限；<a href="#ref-166">Prüss 的半群判据</a>说明局部 Riesz 圆或谱隙不能替代完整竖线 resolvent。限定检索没有发现一条结果同时给出本节所需的整个 \(d\) 区间、Riesz 投影在算子范数下的一致收敛、特征值偏移的 \(O(\varepsilon)\) 上界、rank-one 条件数，以及固定半平面内补空间 reduced-resolvent 与半群增长上界。这只表示在本次限定检索所核验的来源中未发现完全重合的定理，不是穷尽性、原创性或优先权声明。</p>
          <div class="boundary"><strong>R0.73K 的主张边界</strong><p>__CLOSED__。</p><p>__FINITE__。</p><p>__OPEN__。</p><p>这是特定两谐波周期剪切流族的连续算子定理，并附带有限 Fourier 诊断；它不是显式黏度阈值、绝热跟踪、非线性不稳定、三维闭合、有限时间奇性或 Clay 证明。NOT CLAY。</p></div>'''
    boundary = boundary.replace("__CLOSED__", CLOSED).replace("__FINITE__", FINITE).replace("__OPEN__", OPEN)
    match = re.search(
        r'(<h3 id="r073j-boundary">.*?<div class="boundary">.*?</div>)',
        html, flags=re.S,
    )
    if match is None:
        raise RuntimeError("K literature expected R0.73J boundary")
    html = once(
        html, match.group(1), match.group(1) + boundary,
        "K literature boundary",
    )
    references = r'''            <li id="ref-156">R. Shvydkoy and S. Friedlander. <a href="https://doi.org/10.1016/j.anihpc.2007.05.004"><em>The unstable spectrum of the Navier--Stokes operator in the limit of vanishing viscosity</em></a>. Ann. Inst. H. Poincaré C 25 (2008), 713--724; <a href="https://www.numdam.org/articles/10.1016/j.anihpc.2007.05.004/">NUMDAM</a>.</li>
            <li id="ref-157">T. Kato. <a href="https://doi.org/10.1007/978-3-642-66282-9"><em>Perturbation Theory for Linear Operators</em></a>. Springer, 1995 reprint.</li>
            <li id="ref-158">P. M. Anselone and T. W. Palmer. <a href="https://doi.org/10.2140/pjm.1968.25.423"><em>Spectral analysis of collectively compact, strongly convergent operator sequences</em></a>. Pacific J. Math. 25 (1968), 423--431.</li>
            <li id="ref-159">I. C. Gohberg and E. I. Sigal. <a href="https://doi.org/10.1070/SM1971v013n04ABEH003702"><em>An operator generalization of the logarithmic residue theorem and the theorem of Rouché</em></a>. Math. USSR-Sb. 13 (1971), 603--625.</li>
            <li id="ref-160">Y. C. Li and Z. Lin. <a href="https://doi.org/10.1137/100794912"><em>A Resolution of the Sommerfeld Paradox</em></a>. SIAM J. Math. Anal. 43 (2011), 1923--1954.</li>
            <li id="ref-161">L. Quarisa and J. L. Rodrigo. <a href="https://arxiv.org/abs/2304.08696"><em>The adjoint Rayleigh and Orr--Sommerfeld equations: Green function and eigenmodes</em></a>. J. Math. Anal. Appl. 543 (2025), 128884.</li>
            <li id="ref-162">E. Grenier and T. T. Nguyen. <a href="https://arxiv.org/abs/1803.11024"><em>\(L^\infty\) Instability of Prandtl Layers</em></a>. Ann. PDE 5 (2019), Article 18.</li>
            <li id="ref-163">Y. C. Li. <a href="https://doi.org/10.4310/DPDE.2005.v2.n2.a4"><em>Invariant Manifolds and Their Zero-Viscosity Limits for Navier--Stokes Equations</em></a>. Dynamics of PDE 2 (2005), 159--186.</li>
            <li id="ref-164">M. Colombo, M. Dolce, R. Montalto and P. Ventura. <a href="https://arxiv.org/abs/2509.18070"><em>Long-wave instability of periodic shear flows for the 2D Navier--Stokes equations</em></a>. Preprint, 2025.</li>
            <li id="ref-165">K. Zumbrun. <a href="https://doi.org/10.4171/ZAA/1469"><em>2-Modified Characteristic Fredholm Determinants, Hill's Method, and the Periodic Evans Function of Gardner</em></a>. Z. Anal. Anwend. 31 (2012), 463--472.</li>
            <li id="ref-166">J. Prüss. <a href="https://doi.org/10.1090/S0002-9947-1984-0743749-9"><em>On the spectrum of \(C_0\)-semigroups</em></a>. Trans. Amer. Math. Soc. 284 (1984), 847--857.</li>
'''
    html = once(
        html, '          </ol>\n          <p class="source-note">',
        references + '          </ol>\n          <p class="source-note">',
        "K literature references",
    )
    ids = re.findall(r'\bid="([^"]+)"', html)
    if len(ids) != len(set(ids)):
        duplicates = sorted({value for value in ids if ids.count(value) > 1})
        raise RuntimeError("R0.73K literature duplicate HTML ids: " + ", ".join(duplicates))
    for number in range(156, 167):
        if ids.count(f"ref-{number}") != 1:
            raise RuntimeError(f"R0.73K literature reference ref-{number} is not unique")
    assert_clean(html, "R0.73K literature")
    assert_mathjax_clean(html, "R0.73K literature", check_naked=True)
    assert_public_voice(html, "R0.73K literature")
    return html


def build_manifest_outputs() -> dict[Path, bytes]:
    release_path = ROOT / "research/release-manifest.json"
    release = strict_json(release_path, "release manifest")
    for key, value in R073J_BASELINE.items():
        if release.get(key) != value:
            raise RuntimeError("release manifest changed during R0.73K generation: " + key)
    release.update({
        **R073K_TARGET,
        "latestReleaseGate": "tests/r073k-uniform-viscous-branch-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r073k-release.test.mjs",
    })
    release.pop("nextReleaseSourceStage", None)

    site_path = PUBLIC / "site-version.json"
    site = strict_json(site_path, "site version")
    if site != {
        "schemaVersion": "research-site-version-v1",
        "version": "1.50",
        "latestRelease": "R0.73J",
        "publicHtmlNoteCount": 186,
        "publishedDate": "2026-08-30",
    }:
        raise RuntimeError("site-version changed during R0.73K generation")
    site.update({
        "version": "1.51",
        "latestRelease": "R0.73K",
        "publicHtmlNoteCount": 187,
        "publishedDate": "2026-08-31",
    })

    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = strict_json(inventory_path, "formal archive inventory")
    state = (
        inventory.get("latestPublishedRelease"), inventory.get("publishedReleaseCount"),
        inventory.get("formalSealedReleaseCount"), inventory.get("legacyFormalFigureBacklogCount"),
    )
    if state != ("r073j", 88, 64, 24):
        raise RuntimeError("formal archive changed during R0.73K generation")
    for key in ("publishedReleases", "formalSealedReleases"):
        rows = inventory.get(key)
        if not isinstance(rows, list) or rows[-1:] != ["r073j"] or "r073k" in rows:
            raise RuntimeError("formal archive is not append-only: " + key)
        rows.append("r073k")
    inventory.update({
        "latestPublishedRelease": "r073k",
        "publishedReleaseCount": 89,
        "formalSealedReleaseCount": 65,
        "legacyFormalFigureBacklogCount": 24,
    })
    if (
        len(inventory["publishedReleases"]) != 89
        or len(set(inventory["publishedReleases"])) != 89
        or len(inventory["formalSealedReleases"]) != 65
        or len(set(inventory["formalSealedReleases"])) != 65
    ):
        raise RuntimeError("formal archive count or uniqueness mismatch after R0.73K")
    if not set(inventory["formalSealedReleases"]).issubset(inventory["publishedReleases"]):
        raise RuntimeError("formal archive sealed list escaped the published list")
    inventory_payload = json_bytes(inventory)
    release["formalArchiveInventory"] = {
        "path": "research/formal-archive-inventory.json",
        "sha256": sha256_bytes(inventory_payload),
    }
    return {
        release_path: json_bytes(release),
        site_path: json_bytes(site),
        inventory_path: inventory_payload,
        ROOT / "VERSION": b"1.51\n",
    }


def build_note_index(site_payload: bytes) -> str:
    import generate_note_index as note_index

    target_site = json.loads(site_payload.decode("utf-8"))
    old_json = note_index.json
    old_latest_recap_href = note_index.latest_recap_href
    old_paths = (note_index.ROOT, note_index.PUBLIC, note_index.NOTES, note_index.OUTPUT)

    class TargetJson:
        @staticmethod
        def loads(_payload: str) -> dict:
            return target_site

    try:
        with tempfile.TemporaryDirectory(prefix="r073k-baseline-notes-") as temporary:
            frozen_notes = Path(temporary)
            for relative in git_paths(RELEASE_BASELINE_COMMIT, "public/notes"):
                name = Path(relative).name
                if re.fullmatch(r"r0-[0-9a-z]+\.(?:html|pdf)", name):
                    (frozen_notes / name).write_bytes(
                        git_bytes(RELEASE_BASELINE_COMMIT, relative)
                    )
            note_index.ROOT = ROOT
            note_index.PUBLIC = PUBLIC
            note_index.NOTES = frozen_notes
            note_index.OUTPUT = frozen_notes / "index.html"
            existing = [note_index.parse_note(path) for path in note_index.note_files()]
            if len(existing) != 186 or any(note.slug == "r0-73k" for note in existing):
                raise RuntimeError("R0.73K note-index frozen baseline is not exact")
            latest = note_index.Note(
                slug="r0-73k", code="R0.73K",
                title="Parameter-uniform viscous rank-one branch",
                major=73, has_pdf=True,
            )
            note_index.json = TargetJson
            note_index.latest_recap_href = lambda: "/recap-r0-61-r0-73k.html"
            index = note_index.render([latest] + existing)
    finally:
        note_index.json = old_json
        note_index.latest_recap_href = old_latest_recap_href
        note_index.ROOT, note_index.PUBLIC, note_index.NOTES, note_index.OUTPUT = old_paths
    for token in (
        'data-site-version="1.51"',
        "187 篇公开研究笔记",
        "<strong>R0.73K</strong><span>最新研究节点</span>",
        'data-note="r0-73k"',
        "/recap-r0-61-r0-73k.html",
        "研究笔记总索引 · v1.51 · 2026-08-31",
    ):
        if token not in index:
            raise RuntimeError("R0.73K note index missing token: " + token)
    assert_clean(index, "R0.73K note index")
    assert_mathjax_clean(index, "R0.73K note index", check_naked=True)
    assert_public_voice(index, "R0.73K note index")
    return index


def stage_figure_assets(staged: dict[Path, bytes], figure_manifest: dict) -> None:
    source = ROOT / FIGURE_RELATIVE
    archive_target = PUBLIC / FIGURE_RELATIVE
    for name in FIGURE_PACKAGE_PATHS:
        staged[archive_target / name] = (source / name).read_bytes()

    outputs = figure_manifest.get("figure", {}).get("outputs", [])
    by_name = {
        str(row.get("path", "")): row for row in outputs
        if isinstance(row, dict)
    }
    web_target = PUBLIC / "assets/r073k"
    for suffix in ("pdf", "svg", "png"):
        name = f"figure.{suffix}"
        row = by_name.get(name)
        payload = (source / name).read_bytes()
        if (
            row is None
            or sha256_bytes(payload) != row.get("sha256")
            or len(payload) != row.get("bytes")
        ):
            raise RuntimeError("R0.73K public figure master is not manifest-bound: " + name)
        staged[web_target / f"{FIGURE_ID}.{suffix}"] = payload


def validate_staged(staged: dict[Path, bytes]) -> None:
    required_paths = (
        PUBLIC / "notes/r0-73k.html",
        PUBLIC / "recap-r0-61-r0-73k.html",
        PUBLIC / "research-review.html",
        PUBLIC / "literature-review.html",
        PUBLIC / "notes/index.html",
        PUBLIC / "site-version.json",
        ROOT / "research/release-manifest.json",
        ROOT / "research/formal-archive-inventory.json",
        ROOT / "VERSION",
    )
    for path in required_paths:
        if path not in staged:
            raise RuntimeError("R0.73K transaction missing staged path " + str(path))
    for name in FIGURE_PACKAGE_PATHS:
        if PUBLIC / FIGURE_RELATIVE / name not in staged:
            raise RuntimeError("R0.73K transaction omitted figure-package asset " + name)
    for suffix in ("pdf", "svg", "png"):
        if PUBLIC / f"assets/r073k/{FIGURE_ID}.{suffix}" not in staged:
            raise RuntimeError("R0.73K transaction omitted web figure master " + suffix)
    for path in staged:
        if path.suffix.lower() == ".pdf" and (
            "assets/r073k" not in path.as_posix()
            and FIGURE_RELATIVE not in path.as_posix()
        ):
            raise RuntimeError("R0.73K HTML transaction must not generate note or recap PDFs")

    html_paths = (
        PUBLIC / "notes/r0-73k.html",
        PUBLIC / "recap-r0-61-r0-73k.html",
        PUBLIC / "research-review.html",
        PUBLIC / "literature-review.html",
        PUBLIC / "notes/index.html",
    )
    for path in html_paths:
        value = staged[path].decode("utf-8")
        assert_clean(value, path.name)
        assert_mathjax_clean(value, path.name, check_naked=True)
        assert_public_voice(value, path.name)
        if "/i18n-en.js?v=1.51" not in value:
            raise RuntimeError("R0.73K staged HTML has stale i18n version: " + path.name)
    note = staged[PUBLIC / "notes/r0-73k.html"].decode("utf-8")
    for token in (
        CLOSED, FINITE, OPEN, "NOT CLAY", "1190", "952", "0.12", "0.16",
        "1/25", "fullNormResolventConvergence=FALSE", "1.008", "0.5939991104",
    ):
        if token not in note:
            raise RuntimeError("R0.73K staged note lost boundary token: " + token)
    recap = staged[PUBLIC / "recap-r0-61-r0-73k.html"].decode("utf-8")
    start = recap.index('<section id="node-index">')
    end = recap.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', recap[start:end])
    if (
        len(links) != 127
        or len(set(links)) != 127
        or recap.count('<article class="phase">') != 46
    ):
        raise RuntimeError("R0.73K staged recap inventory is invalid")
    home = staged[PUBLIC / "research-review.html"].decode("utf-8")
    route = re.search(
        r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73K">(.*?)</nav>',
        home, flags=re.S,
    )
    route_links = [] if route is None else re.findall(
        r'href="/notes/(r0-[^"]+)\.html"', route.group(1)
    )
    for token in (
        "<h3>R0.73K：参数一致黏性 rank-one 谱支与补空间控制已闭合</h3>",
        "parameter-uniform viscous rank-one branch",
        "finite diagnostic: 1190 states / 952 cross-cutoff comparisons",
    ):
        if token not in home:
            raise RuntimeError("R0.73K staged home lost route token: " + token)
    if len(route_links) != 97 or len(set(route_links)) != 97:
        raise RuntimeError("R0.73K staged home route inventory is invalid")
    literature = staged[PUBLIC / "literature-review.html"].decode("utf-8")
    for token in (
        'class="route-r073k-deck-update"', 'id="r073k-boundary"',
        CLOSED, FINITE, OPEN, "ref-156", "ref-166",
    ):
        if token not in literature:
            raise RuntimeError("R0.73K staged literature lost token: " + token)
    literature_ids = re.findall(r'\bid="([^"]+)"', literature)
    if len(literature_ids) != len(set(literature_ids)):
        raise RuntimeError("R0.73K staged literature contains duplicate HTML ids")
    site = json.loads(staged[PUBLIC / "site-version.json"])
    release = json.loads(staged[ROOT / "research/release-manifest.json"])
    inventory = json.loads(staged[ROOT / "research/formal-archive-inventory.json"])
    if (
        site.get("version") != "1.51"
        or site.get("publicHtmlNoteCount") != 187
        or release.get("postR060RecapNodeCount") != 127
        or release.get("postR070APublishedReleaseCount") != 89
        or release.get("postR070AFormalSealedReleaseCount") != 65
        or release.get("legacyFormalFigureBacklogCount") != 24
        or inventory.get("publishedReleaseCount") != 89
        or inventory.get("formalSealedReleaseCount") != 65
    ):
        raise RuntimeError("R0.73K staged accounting drifted")


def ensure_transaction_parent(path: Path, created: list[Path]) -> None:
    missing: list[Path] = []
    cursor = path.parent
    while not cursor.exists():
        resolved = cursor.resolve()
        if resolved == ROOT or ROOT not in resolved.parents:
            raise RuntimeError("transaction parent escaped repository: " + str(path))
        missing.append(cursor)
        cursor = cursor.parent
    if not cursor.is_dir() or cursor.is_symlink():
        raise RuntimeError("transaction parent is not a real directory: " + str(cursor))
    for directory in reversed(missing):
        directory.mkdir()
        created.append(directory)


def write_temp_for(path: Path, payload: bytes, mode: int) -> Path:
    if not path.parent.is_dir() or path.parent.is_symlink():
        raise RuntimeError("transaction temporary parent is not a real directory: " + str(path.parent))
    descriptor, temporary = tempfile.mkstemp(prefix="." + path.name + ".r073k-", dir=path.parent)
    try:
        os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
    except Exception:
        try:
            os.close(descriptor)
        except OSError:
            pass
        Path(temporary).unlink(missing_ok=True)
        raise
    return Path(temporary)


def sync_transaction_directories(paths: list[Path]) -> None:
    directories = {
        directory
        for path in paths
        for directory in (path.parent, path.parent.parent)
        if directory.exists() and (directory == ROOT or ROOT in directory.parents)
    }
    for directory in sorted(directories, key=lambda value: value.as_posix()):
        descriptor = os.open(directory, os.O_RDONLY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)


def commit_transaction(staged: dict[Path, bytes]) -> None:
    ordered = sorted(staged, key=lambda path: path.as_posix())
    if not ordered:
        raise RuntimeError("R0.73K transaction is empty")
    for path in ordered:
        resolved = path.resolve()
        if resolved == ROOT or ROOT not in resolved.parents:
            raise RuntimeError("transaction target escaped repository: " + str(path))
        if path.exists() and (not path.is_file() or path.is_symlink()):
            raise RuntimeError("transaction target is not a regular file: " + str(path))
    backups = {
        path: path.read_bytes() if path.is_file() else None
        for path in ordered
    }
    modes = {
        path: (path.stat().st_mode & 0o777) if path.exists() else 0o644
        for path in ordered
    }
    temporary: dict[Path, Path] = {}
    replaced: list[Path] = []
    created_directories: list[Path] = []
    committed = False
    try:
        for path in ordered:
            ensure_transaction_parent(path, created_directories)
            temporary[path] = write_temp_for(path, staged[path], modes[path])
        for path in ordered:
            os.replace(temporary[path], path)
            replaced.append(path)
        for path, payload in staged.items():
            if path.read_bytes() != payload:
                raise RuntimeError("transaction readback mismatch: " + str(path))
        sync_transaction_directories(ordered)
        committed = True
    except Exception:
        for path in reversed(replaced):
            old = backups[path]
            if old is None:
                path.unlink(missing_ok=True)
            else:
                rollback = write_temp_for(path, old, modes[path])
                os.replace(rollback, path)
        sync_transaction_directories(ordered)
        raise
    finally:
        for path in temporary.values():
            path.unlink(missing_ok=True)
        if not committed:
            for directory in reversed(created_directories):
                try:
                    directory.rmdir()
                except FileNotFoundError:
                    pass
                except OSError as exc:
                    raise RuntimeError(
                        "transaction rollback left a nonempty created directory: " + str(directory)
                    ) from exc


def verify_materialized_figure_assets(figure_manifest: dict) -> None:
    source = ROOT / FIGURE_RELATIVE
    archive = PUBLIC / FIGURE_RELATIVE
    for name in FIGURE_PACKAGE_PATHS:
        target = archive / name
        if not target.is_file() or target.is_symlink():
            raise RuntimeError("R0.73K materialized figure-package asset missing: " + name)
        if target.read_bytes() != (source / name).read_bytes():
            raise RuntimeError("R0.73K public figure-package asset is not byte-identical: " + name)
    rows = {
        str(row.get("path", "")): row
        for row in figure_manifest.get("figure", {}).get("outputs", [])
        if isinstance(row, dict)
    }
    for suffix in ("pdf", "svg", "png"):
        source_path = source / f"figure.{suffix}"
        target_path = PUBLIC / f"assets/r073k/{FIGURE_ID}.{suffix}"
        row = rows.get(f"figure.{suffix}")
        if row is None or not target_path.is_file() or target_path.is_symlink():
            raise RuntimeError("R0.73K materialized web figure missing: " + suffix)
        if target_path.read_bytes() != source_path.read_bytes():
            raise RuntimeError("R0.73K public web figure is not byte-identical: " + suffix)
        if digest(target_path) != row.get("sha256") or target_path.stat().st_size != row.get("bytes"):
            raise RuntimeError("R0.73K materialized web figure escaped manifest: " + suffix)


def publication_stage_incomplete() -> bool:
    pdfs = (
        PUBLIC / "notes/r0-73k.pdf",
        PUBLIC / "recap-r0-61-r0-73k.pdf",
    )
    if any(
        not path.is_file()
        or path.is_symlink()
        or not path.read_bytes().startswith(b"%PDF")
        for path in pdfs
    ):
        return True
    try:
        snapshot = json.loads(
            (ROOT / "scripts/i18n-snapshots/r073k-missing.json").read_text(encoding="utf-8")
        )
        translations = json.loads(
            (ROOT / "translations/en.json").read_text(encoding="utf-8")
        )
        bundle = (PUBLIC / "i18n-en.js").read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError, ValueError):
        return True
    if not isinstance(snapshot, list) or not snapshot:
        return True
    by_id = {
        row.get("id"): row for row in translations
        if isinstance(row, dict) and re.fullmatch(r"r073k\d{3}", str(row.get("id", "")))
    } if isinstance(translations, list) else {}
    if len(by_id) != len(snapshot):
        return True
    for index, snapshot_row in enumerate(snapshot, 1):
        row = by_id.get(f"r073k{index:03d}")
        snapshot_en = (
            str(snapshot_row.get("en", "")).strip()
            if isinstance(snapshot_row, dict)
            else ""
        )
        if (
            not isinstance(snapshot_row, dict)
            or not isinstance(row, dict)
            or not snapshot_en
            or re.search(r"[\u3400-\u9fff]", snapshot_en) is not None
            or row.get("zh") != snapshot_row.get("zh")
            or row.get("en") != snapshot_en
            or not isinstance(row.get("en"), str)
            or not row.get("en", "").strip()
            or re.search(r"[\u3400-\u9fff]", row.get("en", "")) is not None
            or (
                json.dumps(row.get("zh"), ensure_ascii=False)
                + ": "
                + json.dumps(row.get("en"), ensure_ascii=False)
            ) not in bundle
        ):
            return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Validate or explicitly apply the staged R0.73K HTML/manifest transaction. "
            "Note/recap PDF and translation completion remain separate publication steps."
        )
    )
    action = parser.add_mutually_exclusive_group()
    action.add_argument(
        "--check-only", action="store_true",
        help="validate sealed inputs and the source or materialized target without writing",
    )
    action.add_argument(
        "--apply", action="store_true",
        help="explicitly apply the HTML/manifest transaction from the exact R0.73J source",
    )
    args = parser.parse_args()
    if not args.check_only and not args.apply:
        parser.print_help()
        return

    release_state = preflight_release_state()
    _, figure_manifest = validate_inputs()
    if release_state == "target":
        synchronized_assets = 0
        try:
            verify_materialized_figure_assets(figure_manifest)
        except RuntimeError:
            if not args.apply:
                raise
            resealed: dict[Path, bytes] = {}
            stage_figure_assets(resealed, figure_manifest)
            commit_transaction(resealed)
            synchronized_assets = len(resealed)
            verify_materialized_figure_assets(figure_manifest)
        print(json.dumps({
            "release": "R0.73K",
            "siteVersion": "1.51",
            "notes": 187,
            "recapNodes": 127,
            "published": 89,
            "formalSealed": 65,
            "legacyBacklog": 24,
            "phases": 46,
            "routeNotes": 97,
            "next": "R0.73L",
            "rootVersion": "1.51",
            "noOp": synchronized_assets == 0,
            "publicationStageIncomplete": publication_stage_incomplete(),
            "pdfGenerated": False,
            "translationsGenerated": False,
            "synchronizedAssets": synchronized_assets,
        }, ensure_ascii=False))
        return

    staged: dict[Path, bytes] = {}
    stage_figure_assets(staged, figure_manifest)
    staged[PUBLIC / "notes/r0-73k.html"] = build_note().encode("utf-8")
    staged[PUBLIC / "recap-r0-61-r0-73k.html"] = build_recap().encode("utf-8")
    staged[PUBLIC / "research-review.html"] = update_home().encode("utf-8")
    staged[PUBLIC / "literature-review.html"] = update_literature().encode("utf-8")
    manifest_outputs = build_manifest_outputs()
    staged.update(manifest_outputs)
    staged[PUBLIC / "notes/index.html"] = build_note_index(
        staged[PUBLIC / "site-version.json"]
    ).encode("utf-8")
    validate_staged(staged)
    if args.check_only:
        print(json.dumps({
            "release": "R0.73K",
            "sourceState": "R0.73J",
            "checkOnly": True,
            "wouldWrite": len(staged),
            "publicationStageIncomplete": True,
        }, ensure_ascii=False))
        return

    commit_transaction(staged)
    if len(list((PUBLIC / "notes").glob("r0-*.html"))) != 187:
        raise RuntimeError("R0.73K postcommit note count is not 187")
    verify_materialized_figure_assets(figure_manifest)
    print(json.dumps({
        "release": "R0.73K",
        "siteVersion": "1.51",
        "notes": 187,
        "recapNodes": 127,
        "published": 89,
        "formalSealed": 65,
        "legacyBacklog": 24,
        "phases": 46,
        "routeNotes": 97,
        "next": "R0.73L",
        "rootVersion": "1.51",
        "noOp": False,
        "publicationStageIncomplete": True,
        "pdfGenerated": False,
        "translationsGenerated": False,
    }, ensure_ascii=False))



if __name__ == "__main__":
    main()
