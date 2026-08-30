#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the fail-closed transactional R0.73L GitHub Pages release.

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
from r073l_release_content import (
    CLOSED,
    FIGURE_ID,
    FIGURE_RELATIVE,
    FINITE,
    HOME_L_CARD,
    HOME_LATEST_SPOTLIGHT,
    HOME_NEXT,
    NOTE_ARTICLE,
    NOTE_HERO,
    OPEN,
    RECAP_PHASE,
    R073K_BASELINE,
    R073L_TARGET,
)


ROOT = Path(os.environ.get(
    "R073L_RELEASE_ROOT", Path(__file__).resolve().parents[1]
)).resolve()
PUBLIC = ROOT / "public"

ANALYTIC_SOURCE_COMMIT = "09752a821fb1c7cafca74702c1a775d1e8a8713f"
EXPERIMENT_PACKAGE_COMMIT = "09752a821fb1c7cafca74702c1a775d1e8a8713f"
FIGURE_PACKAGE_COMMIT = "212e383d5d5f4fb49b5b58d086c351217901ec2d"
RELEASE_BASELINE_COMMIT = "212e383d5d5f4fb49b5b58d086c351217901ec2d"
RELEASE_SOURCE_COMMIT = "53b1bf0e84b9af159add7fcfb423f0502a3a1e01"

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
    "scripts/r073l_release_content.py",
    "scripts/add-r073l-translations.mjs",
    "scripts/generate_r073l_release.py",
    "scripts/generate_r072o_release.py",
    "scripts/generate_r072p_release.py",
    "scripts/generate_note_index.py",
    "scripts/i18n-lib.mjs",
    "scripts/render-note-pdf.mjs",
    "scripts/bind-r073l-pdfs.mjs",
    "scripts/run-release-publication-gate.mjs",
    "research/r073l_bilingual_dictionary.md",
    "tests/bilingual-content.test.mjs",
    "tests/internal-public-links.test.mjs",
    "tests/release-publication-gate-runner.test.mjs",
    "tests/release-publication-invariant.test.mjs",
    "tests/r073l-adiabatic-tracking-gate.test.mjs",
    "tests/r073l-release.test.mjs",
    "tests/site-route-current-boundary.test.mjs",
)

BASELINE_EXACT_PATHS = (
    "VERSION",
    "research/release-manifest.json",
    "research/formal-archive-inventory.json",
    "public/site-version.json",
    "public/research-review.html",
    "public/literature-review.html",
    "public/recap-r0-61-r0-73k.html",
    "public/notes/index.html",
)

SOURCE_PATHS = (
    "research/r073l_problem_freeze.md",
    "research/r073l_adiabatic_tracking_proof.md",
    "research/r073l_independent_analytic_audit.md",
    "research/r073l_adversarial_audit.md",
    "research/r073l_finite_diagnostic_audit.md",
    "research/r073l_literature_audit.md",
    "research/r073l_gap_matrix.md",
    "research/r073l_report-source.md",
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
        raise RuntimeError("R0.73L release generator is not UTF-8") from exc
    value, count = re.subn(
        r'(?m)^RELEASE_SOURCE_COMMIT = "[^"]+"$',
        'RELEASE_SOURCE_COMMIT = "__NORMALIZED_RELEASE_SOURCE_COMMIT__"',
        value,
    )
    if count != 1:
        raise RuntimeError("R0.73L release generator must have exactly one release-source pin")
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
            raise RuntimeError("R0.73L baseline source is not a regular file: " + relative)
        if path.read_bytes() != git_bytes(RELEASE_BASELINE_COMMIT, relative):
            raise RuntimeError("R0.73L baseline source differs from frozen commit: " + relative)
    verify_exact_directory_at_commit(
        PUBLIC / "notes", RELEASE_BASELINE_COMMIT, "R0.73L baseline notes",
    )

def ensure_commits_ready() -> None:
    if any(value.startswith("TO_BE_FILLED_") for value in COMMIT_PLACEHOLDERS):
        raise RuntimeError(
            "R0.73L release is intentionally sealed shut: replace every "
            "commit placeholder only after the corresponding frozen commit"
        )
    chain = (("analytic source", ANALYTIC_SOURCE_COMMIT),
             ("complete experiment package", EXPERIMENT_PACKAGE_COMMIT),
             ("complete figure package", FIGURE_PACKAGE_COMMIT),
             ("release baseline", RELEASE_BASELINE_COMMIT),
             ("release source", RELEASE_SOURCE_COMMIT))
    for label, commit in chain:
        require_commit(commit, "R0.73L " + label)
    for (left_label, left), (right_label, right) in zip(chain, chain[1:]):
        if not is_ancestor(left, right):
            raise RuntimeError(f"R0.73L commit order invalid: {left_label} < {right_label}")
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()
    if not is_ancestor(RELEASE_SOURCE_COMMIT, head):
        raise RuntimeError("R0.73L release source commit is not an ancestor of HEAD")
    generator_relative = "scripts/generate_r073l_release.py"
    for relative in RELEASE_SOURCE_EXACT_PATHS:
        if relative == generator_relative:
            continue
        if git_bytes(RELEASE_SOURCE_COMMIT, relative) != (ROOT / relative).read_bytes():
            raise RuntimeError("R0.73L release source is not pinned: " + relative)
    frozen = normalized_release_generator(git_bytes(RELEASE_SOURCE_COMMIT, generator_relative))
    current = normalized_release_generator((ROOT / generator_relative).read_bytes())
    if frozen != current:
        raise RuntimeError("R0.73L release generator differs from pinned source outside its self pin")

def validate_analytic_sources() -> None:
    source_text: dict[str, str] = {}
    for relative in SOURCE_PATHS:
        path = ROOT / relative
        if not path.is_file() or path.is_symlink():
            raise RuntimeError("missing R0.73L analytic source: " + relative)
        if path.read_bytes() != git_bytes(ANALYTIC_SOURCE_COMMIT, relative):
            raise RuntimeError("R0.73L source differs from analytic source commit: " + relative)
        source_text[relative] = path.read_text(encoding="utf-8")
    combined = "\n".join(source_text.values())
    for token in (
        "1/450", "0.12", "0.16", "1/25", "9/5",
        "O(\\varepsilon)", "fixed-fast-time", "commonDomainEvolution=CLOSED",
        "nonselfadjointAdiabaticTracking=CLOSED", "1.02813", "PASS", "Clay",
    ):
        if token not in combined:
            raise RuntimeError("R0.73L analytic source missing boundary token: " + token)
    gap = source_text["research/r073l_gap_matrix.md"]
    for index in range(1, 9):
        if not re.search(rf"\| L{index} \|[^\n]+\| CLOSED", gap):
            raise RuntimeError("R0.73L gap matrix lost closed L" + str(index))
    if not re.search(r"\| F1 \|[^\n]+\| PRIMARY PASS; independent validation PASS; FIGURE PASS", gap):
        raise RuntimeError("R0.73L finite gate F1 drifted")
    for token in ("explicit \\(\\varepsilon_L\\)", "prefactor", "nonlinear 2D", "Clay closure"):
        if token not in gap or "OPEN" not in gap:
            raise RuntimeError("R0.73L open boundary drifted: " + token)
    finite = source_text["research/r073l_finite_diagnostic_audit.md"].lower()
    if "continuum" not in finite or "finite" not in finite:
        raise RuntimeError("R0.73L finite audit lost continuum boundary")
    for label, value in source_text.items():
        assert_public_voice(value, "R0.73L " + label)

def validate_experiment() -> dict:
    directory = ROOT / "experiments/r073l"
    verify_exact_directory_at_commit(directory, EXPERIMENT_PACKAGE_COMMIT, "R0.73L experiment")
    verify_flat_ledger(
        directory,
        "R0.73L experiment",
        require_sorted=False,
        allowed_repository_paths=frozenset({
            "research/r073l_adiabatic_diagnostic.py",
        }),
    )
    manifest = strict_json(directory / "manifest.json", "R0.73L experiment manifest")
    primary = strict_json(directory / "adiabatic_diagnostic.json", "R0.73L primary")
    independent = strict_json(directory / "independent_validation.json", "R0.73L independent")
    package = strict_json(directory / "package_validation.json", "R0.73L package validation")
    schemas = {
        "manifest": (manifest, "r073l-finite-diagnostic-manifest-v1"),
        "primary": (primary, "r073l-adiabatic-diagnostic-v1"),
        "independent": (independent, "r073l-independent-validation-v1"),
        "package": (package, "r073l-package-validation-v1"),
    }
    for label, (payload, expected) in schemas.items():
        if payload.get("schemaVersion") != expected:
            raise RuntimeError("R0.73L experiment " + label + " schema drifted")
    if (
        manifest.get("release") != "R0.73L"
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
        raise RuntimeError("R0.73L finite diagnostic failed")
    if manifest.get("claimBoundary") != {
        "clayProblemSolved": False,
        "continuumTheoremCertifiedByManifest": False,
        "finiteDimensionalDiagnosticSealed": True,
    }:
        raise RuntimeError("R0.73L experiment claim boundary drifted")
    if independent.get("claimBoundary", {}).get("continuumProof") is not False:
        raise RuntimeError("R0.73L independent validator escaped finite scope")
    details = package.get("details", {})
    if (
        details.get("checksumFiles") != 16
        or details.get("manifestFiles") != 15
    ):
        raise RuntimeError("R0.73L finite package inventory drifted")
    if (
        len(primary.get("cases", [])) != 15
        or len(independent.get("cases", [])) != 5
    ):
        raise RuntimeError("R0.73L primary or independent case inventory drifted")
    errors = independent.get("maximums", {})
    if not (
        errors.get("finestVsPrimaryNormalizedGain", 1.0) < 1.9e-9
        and errors.get("finestVsPrimaryLeakage", 1.0) < 1.8e-9
        and errors.get("lastTwoNormalizedGain", 1.0) < 5.6e-9
        and errors.get("lastTwoLeakage", 1.0) < 5.2e-9
    ):
        raise RuntimeError("R0.73L independent comparison drifted")
    maximums = primary.get("maximums", {})
    if not (
        maximums.get("backwardActionResidualAbs", 1.0) < 6.72e-4
        and maximums.get("largestPairTerminalNormalizedGainDifference", 1.0) < 7.0e-15
        and maximums.get("largestPairTerminalLeakageRatioDifference", 1.0) < 3.2e-15
        and maximums.get("lambdaImaginaryAbs", 1.0) < 6.7e-16
    ):
        raise RuntimeError("R0.73L primary maximums drifted")
    scaling = primary.get("epsilonScalingByCutoff", {}).get("64", {})
    if (
        abs(scaling.get("terminalLeakageTailThreeLogLogSlope", 0.0)
            - 1.0281276356834264) > 1e-13
        or scaling.get("terminalNormalizedGainRange") !=
        [0.9993290525496814, 0.9998284900372003]
    ):
        raise RuntimeError("R0.73L primary scaling summary drifted")
    for row in manifest.get("files", []):
        relative = str(row.get("path", ""))
        path = ROOT / relative
        if not path.is_file() or path.is_symlink():
            raise RuntimeError("R0.73L manifest file missing: " + relative)
        if digest(path) != row.get("sha256") or path.stat().st_size != row.get("bytes"):
            raise RuntimeError("R0.73L manifest binding drifted: " + relative)
    return manifest

def validate_figure() -> dict:
    directory = ROOT / FIGURE_RELATIVE
    verify_exact_directory_at_commit(directory, FIGURE_PACKAGE_COMMIT, "R0.73L figure")
    verify_flat_ledger(directory, "R0.73L figure", require_sorted=True)
    manifest = strict_json(directory / "manifest.json", "R0.73L figure manifest")
    results = strict_json(directory / "results.json", "R0.73L figure results")
    contract = strict_json(directory / "contract.json", "R0.73L figure contract")
    config = strict_json(directory / "config.json", "R0.73L figure config")
    validation = strict_json(directory / "validation.json", "R0.73L figure validation")
    schemas = {
        "manifest": (manifest, "r073l-adiabatic-tracking-figure-manifest-v1"),
        "results": (results, "r073l-figure-results-v1"),
        "contract": (contract, "r073l-adiabatic-tracking-figure-contract-v1"),
        "config": (config, "r073l-adiabatic-tracking-figure-config-v1"),
        "validation": (validation, "r073l-figure-validation-v1"),
    }
    for label, (payload, expected) in schemas.items():
        if payload.get("schemaVersion") != expected:
            raise RuntimeError("R0.73L figure " + label + " schema drifted")
    if (
        manifest.get("release") != "R0.73L"
        or manifest.get("figureId") != FIGURE_ID
        or manifest.get("status") != "formal"
        or results.get("status") != "passed"
        or results.get("allChecksPass") is not True
        or validation.get("status") != "passed"
        or not all(validation.get("checks", {}).values())
    ):
        raise RuntimeError("R0.73L figure status failed")
    boundary = manifest.get("claimBoundary", {})
    expected_boundary = contract.get("claimBoundary")
    if (
        boundary != expected_boundary
        or results.get("claimBoundary") != boundary
        or boundary.get("finiteDimensionalDiagnostic") is not True
        or boundary.get("continuumAdiabaticTheoremCertifiedByFigure") is not False
        or boundary.get("nonlinearNavierStokesCertified") is not False
        or boundary.get("transverseThreeDimensionalClosureCertified") is not False
        or boundary.get("clayProblemSolved") is not False
    ):
        raise RuntimeError("R0.73L figure claim boundaries disagree")
    if results.get("sourceRows") != 346:
        raise RuntimeError("R0.73L figure row counts drifted")
    decisions = results.get("summary", {})
    if not (
        decisions.get("displayCutoff") == 64
        and decisions.get("comparisonCutoff") == 48
        and abs(decisions.get("tailThreeLeakageSlope", 0.0) - 1.0281276356834264) < 1e-13
        and decisions.get("terminalNormalizedGainRange") ==
        [0.9993290525496814, 0.9998284900372003]
        and decisions.get("maximumBackwardActionResidualAbs", 1.0) < 6.72e-4
        and all(row.get("ratioToTolerance", 1.0) < 1.0
                for row in decisions.get("validationMetrics", []))
    ):
        raise RuntimeError("R0.73L figure decisions drifted")
    formats = validation.get("details", {}).get("exports", {})
    if (
        validation.get("allChecksPass") is not True
        or len(validation.get("checks", {})) != 7
        or formats.get("pngPixels") != [4204, 3023]
        or formats.get("pdfPages") != 1
        or formats.get("svgRasterImages") != 0
    ):
        raise RuntimeError("R0.73L figure validation details drifted")
    actual = tuple(path.name for path in sorted(directory.iterdir()))
    if actual != tuple(sorted(FIGURE_PACKAGE_PATHS)):
        raise RuntimeError("R0.73L figure package inventory drifted")
    rows = manifest.get("files", [])
    declared = {str(row.get("path", "")): row for row in rows if isinstance(row, dict)}
    expected_declared = set(FIGURE_PACKAGE_PATHS) - {"manifest.json", "SHA256SUMS"}
    if set(declared) != expected_declared:
        raise RuntimeError("R0.73L figure manifest inventory drifted")
    for name, row in declared.items():
        path = directory / name
        if digest(path) != row.get("sha256") or path.stat().st_size != row.get("bytes"):
            raise RuntimeError("R0.73L figure manifest hash drifted: " + name)
    for row in manifest.get("inputBindings", []):
        relative = str(row.get("path", ""))
        path = ROOT / relative
        if not path.is_file() or digest(path) != row.get("sha256"):
            raise RuntimeError("R0.73L figure input binding drifted: " + relative)
        if git_bytes(EXPERIMENT_PACKAGE_COMMIT, relative) != path.read_bytes():
            raise RuntimeError("R0.73L figure input differs from experiment commit: " + relative)
    for name in FIGURE_SOURCE_PATHS:
        relative = f"{FIGURE_RELATIVE}/{name}"
        if git_bytes(FIGURE_PACKAGE_COMMIT, relative) != (directory / name).read_bytes():
            raise RuntimeError("R0.73L figure source differs from figure commit: " + name)
    if not (directory / "figure.pdf").read_bytes().startswith(b"%PDF"):
        raise RuntimeError("R0.73L figure PDF signature invalid")
    svg = (directory / "figure.svg").read_text(encoding="utf-8").lower()
    if "<svg" not in svg or "<image" in svg or "<text" not in svg:
        raise RuntimeError("R0.73L figure SVG is absent or rasterized")
    png = (directory / "figure.png").read_bytes()
    if not png.startswith(b"\x89PNG\r\n\x1a\n") or b"pHYs" not in png:
        raise RuntimeError("R0.73L figure PNG metadata missing")
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
        "notes/r0-73l.html",
        "recap-r0-61-r0-73l.html",
        "research-review.html",
        "literature-review.html",
        "notes/index.html",
    ):
        path = PUBLIC / relative
        if not path.is_file() or path.is_symlink():
            raise RuntimeError("R0.73L target HTML missing: " + relative)
        value = path.read_text(encoding="utf-8")
        assert_clean(value, "R0.73L target " + relative)
        assert_mathjax_clean(value, "R0.73L target " + relative, check_naked=True)
        assert_public_voice(value, "R0.73L target " + relative)
        if "/i18n-en.js?v=1.52" not in value:
            raise RuntimeError("R0.73L target HTML has stale i18n cache: " + relative)
        target[relative] = value
    return target


def preflight_release_state() -> str:
    release = strict_json(ROOT / "research/release-manifest.json", "release manifest")
    site = strict_json(PUBLIC / "site-version.json", "site version")
    inventory = strict_json(ROOT / "research/formal-archive-inventory.json", "archive inventory")
    root_version = (ROOT / "VERSION").read_text(encoding="utf-8")

    if release.get("latestCompletedRelease") == "r073l":
        for key, value in R073L_TARGET.items():
            if release.get(key) != value:
                raise RuntimeError("R0.73L target release-manifest drifted: " + key)
        if release.get("latestReleaseGate") != "tests/r073l-adiabatic-tracking-gate.test.mjs":
            raise RuntimeError("R0.73L target gate binding drifted")
        if release.get("latestReleasePublicationTest") != "tests/r073l-release.test.mjs":
            raise RuntimeError("R0.73L target publication-test binding drifted")
        if site != {
            "schemaVersion": "research-site-version-v1",
            "version": "1.52",
            "latestRelease": "R0.73L",
            "publicHtmlNoteCount": 188,
            "publishedDate": "2026-08-31",
        } or root_version != "1.52\n":
            raise RuntimeError("R0.73L target site version drifted")
        state = (
            inventory.get("latestPublishedRelease"),
            inventory.get("publishedReleaseCount"),
            inventory.get("formalSealedReleaseCount"),
            inventory.get("legacyFormalFigureBacklogCount"),
        )
        if state != ("r073l", 90, 66, 24):
            raise RuntimeError("R0.73L target formal archive is not exact")
        baseline_inventory = json.loads(git_bytes(
            RELEASE_BASELINE_COMMIT, "research/formal-archive-inventory.json"
        ))
        expected = json.loads(json.dumps(baseline_inventory))
        for key in ("publishedReleases", "formalSealedReleases"):
            rows = expected.get(key)
            if not isinstance(rows, list) or rows[-1:] != ["r073k"] or "r073l" in rows:
                raise RuntimeError("R0.73L sealed baseline inventory invalid: " + key)
            rows.append("r073l")
        expected.update({
            "latestPublishedRelease": "r073l",
            "publishedReleaseCount": 90,
            "formalSealedReleaseCount": 66,
            "legacyFormalFigureBacklogCount": 24,
        })
        if inventory != expected:
            raise RuntimeError("R0.73L target archive is not exact append-only successor")
        for key, count in (("publishedReleases", 90), ("formalSealedReleases", 66)):
            rows = inventory.get(key, [])
            if len(rows) != count or len(set(rows)) != count:
                raise RuntimeError("R0.73L target archive sequence drifted: " + key)
        if not set(inventory["formalSealedReleases"]).issubset(inventory["publishedReleases"]):
            raise RuntimeError("R0.73L sealed inventory escaped published inventory")
        if release.get("formalArchiveInventory") != {
            "path": "research/formal-archive-inventory.json",
            "sha256": digest(ROOT / "research/formal-archive-inventory.json"),
        }:
            raise RuntimeError("R0.73L target archive binding drifted")
        if len(list((PUBLIC / "notes").glob("r0-*.html"))) != 188:
            raise RuntimeError("R0.73L target note count is not 188")
        html = _target_html()
        expected_html = {
            "notes/r0-73l.html": build_note(),
            "recap-r0-61-r0-73l.html": build_recap(),
            "research-review.html": update_home(),
            "literature-review.html": update_literature(),
            "notes/index.html": build_note_index(json_bytes(site)),
        }
        for relative, expected in expected_html.items():
            if html[relative] != expected:
                raise RuntimeError(
                    "R0.73L target HTML differs from deterministic builder: " + relative
                )
        for token in (
            CLOSED, FINITE, OPEN, "NOT CLAY", "15 条主轨迹", "1.0281276",
            "6.711726", "0.12", "0.16", "R0.73M",
        ):
            if token not in html["notes/r0-73l.html"]:
                raise RuntimeError("R0.73L target note lost token: " + token)
        recap = html["recap-r0-61-r0-73l.html"]
        start = recap.find('<section id="node-index">')
        end = recap.find("</section>", start)
        links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', recap[start:end])
        if (
            start < 0 or end <= start
            or len(links) != 128 or len(set(links)) != 128
            or recap.count('<article class="phase">') != 47
        ):
            raise RuntimeError("R0.73L target recap inventory drifted")
        home = html["research-review.html"]
        route = re.search(
            r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73L">(.*?)</nav>',
            home, flags=re.S,
        )
        route_links = [] if route is None else re.findall(
            r'href="/notes/(r0-[^"]+)\.html"', route.group(1)
        )
        if (
            len(route_links) != 98 or len(set(route_links)) != 98
            or home.count('data-release="r073l"') != 1
        ):
            raise RuntimeError("R0.73L target home route drifted")
        if (
            'id="r073l-boundary"' not in html["literature-review.html"]
            or 'class="route-r073l-deck-update"' not in html["literature-review.html"]
        ):
            raise RuntimeError("R0.73L target literature boundary absent")
        if 'data-note="r0-73l"' not in html["notes/index.html"]:
            raise RuntimeError("R0.73L target note index absent")
        return "target"

    if any(release.get(key) != value for key, value in R073K_BASELINE.items()):
        raise RuntimeError("R0.73L state is neither exact R0.73K source nor exact target")
    if site != {
        "schemaVersion": "research-site-version-v1",
        "version": "1.51",
        "latestRelease": "R0.73K",
        "publicHtmlNoteCount": 187,
        "publishedDate": "2026-08-31",
    } or root_version != "1.51\n":
        raise RuntimeError("R0.73L baseline site version drifted")
    state = (
        inventory.get("latestPublishedRelease"), inventory.get("publishedReleaseCount"),
        inventory.get("formalSealedReleaseCount"), inventory.get("legacyFormalFigureBacklogCount"),
    )
    if state != ("r073k", 89, 65, 24):
        raise RuntimeError("R0.73L formal archive baseline drifted")
    verify_baseline_sources()
    if len(list((PUBLIC / "notes").glob("r0-*.html"))) != 187:
        raise RuntimeError("R0.73L expected exactly 187 baseline HTML notes")
    for path in (
        PUBLIC / "notes/r0-73l.html", PUBLIC / "notes/r0-73l.pdf",
        PUBLIC / "recap-r0-61-r0-73l.html", PUBLIC / "recap-r0-61-r0-73l.pdf",
    ):
        if path.exists() or path.is_symlink():
            raise RuntimeError("R0.73L baseline path already exists: " + str(path))
    archive = PUBLIC / FIGURE_RELATIVE
    masters = PUBLIC / "assets/r073l"
    if archive.exists() or masters.exists():
        if (
            not archive.is_dir() or archive.is_symlink()
            or not masters.is_dir() or masters.is_symlink()
        ):
            raise RuntimeError("R0.73L prestaged figure paths are incomplete")
        archive_names = sorted(path.name for path in archive.iterdir())
        if archive_names != sorted(FIGURE_PACKAGE_PATHS):
            raise RuntimeError("R0.73L prestaged archive inventory drifted")
        source = ROOT / FIGURE_RELATIVE
        for name in FIGURE_PACKAGE_PATHS:
            if (archive / name).read_bytes() != (source / name).read_bytes():
                raise RuntimeError("R0.73L prestaged archive differs: " + name)
        expected_masters = [f"{FIGURE_ID}.{suffix}" for suffix in ("pdf", "png", "svg")]
        if sorted(path.name for path in masters.iterdir()) != sorted(expected_masters):
            raise RuntimeError("R0.73L prestaged web-master inventory drifted")
        for suffix in ("pdf", "png", "svg"):
            if (masters / f"{FIGURE_ID}.{suffix}").read_bytes() != (source / f"figure.{suffix}").read_bytes():
                raise RuntimeError("R0.73L prestaged web master differs: " + suffix)
    for relative, tokens in {
        "research-review.html": ("R0.73K", "187", "R0.73L"),
        "literature-review.html": ("R0.73K", "开放接口 · R0.73L"),
        "notes/index.html": ("R0.73K", "187 篇公开研究笔记"),
        "recap-r0-61-r0-73k.html": ("R0.61–R0.73K", "127", "46 个研究阶段"),
    }.items():
        value = (PUBLIC / relative).read_text(encoding="utf-8")
        for token in tokens:
            if token not in value:
                raise RuntimeError(f"R0.73L baseline {relative} missing {token}")
    return "source"


def build_note() -> str:
    html = git_bytes(
        RELEASE_BASELINE_COMMIT, "public/notes/r0-73k.html"
    ).decode("utf-8")
    metadata = (
        ("description", r'<meta name="description" content=".*?">',
         '<meta name="description" content="研究笔记 R0.73L：共同定义域上的非自伴绝热跟踪、移动补空间相对衰减、匹配增长作用量、独立审计与有限诊断。">'),
        ("og title", r'<meta property="og:title" content=".*?">',
         '<meta property="og:title" content="R0.73L｜Parameter-uniform nonselfadjoint adiabatic tracking">'),
        ("og description", r'<meta property="og:description" content=".*?">',
         '<meta property="og:description" content="For the sealed periodic shear model, the exact nonautonomous selected orbit tracks the Kato branch with O(epsilon) relative error and gain comparable to the viscous and inviscid spectral actions.">'),
        ("og image", r'<meta property="og:image" content=".*?">',
         f'<meta property="og:image" content="https://kasifa.github.io/assets/r073l/{FIGURE_ID}.png">'),
        ("title", r'<title>.*?</title>',
         '<title>R0.73L｜Parameter-uniform nonselfadjoint adiabatic tracking</title>'),
    )
    for label, pattern, value in metadata:
        html = section(html, pattern, value, "K note " + label)
    html = required(html, "/i18n-en.js?v=1.51", "/i18n-en.js?v=1.52", "K note i18n")
    toc_items = (
        ("result", "00 · direct result"),
        ("obstruction", "01 · nonnormal obstruction"),
        ("kato", "02 · Kato transport"),
        ("block", "03 · fixed fast block"),
        ("volterra", "04 · forward Volterra"),
        ("tracking", "05 · vector tracking"),
        ("localization", "06 · forward-orbit localization"),
        ("audits", "07 · independent audits"),
        ("diagnostic", "08 · finite diagnostic"),
        ("figure", "09 · journal figure"),
        ("literature", "10 · Deep Research boundary"),
        ("boundary", "11 · exact boundary"),
        ("value", "12 · value"),
        ("next", "13 · R0.73M"),
        ("reproduce", "14 · reproduction"),
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
        '<div>研究笔记 R0.73L · 2026-08-31<br><a href="/">返回研究主页</a></div></footer>'
    )
    html = section(html, r"<footer>.*?</footer>", footer, "K note footer")
    match = re.search(r"<nav>(.*?)</nav>", html, flags=re.S)
    anchors = re.findall(r'href="#([^"]+)"', match.group(1)) if match else []
    expected = [anchor for anchor, _ in toc_items]
    if anchors != expected or len(anchors) != len(set(anchors)):
        raise RuntimeError("R0.73L note nav anchors are not unique and ordered")
    for token in (
        CLOSED, FINITE, OPEN, "NOT CLAY", "15 条主轨迹", "1.0281276",
        "6.711726", "0.12", "0.16", "R0.73M",
    ):
        if token not in html:
            raise RuntimeError("R0.73L note lost token: " + token)
    assert_clean(html, "R0.73L note")
    assert_mathjax_clean(html, "R0.73L note", check_naked=True)
    assert_public_voice(html, "R0.73L note")
    return html


def build_recap() -> str:
    html = git_bytes(
        RELEASE_BASELINE_COMMIT, "public/recap-r0-61-r0-73k.html"
    ).decode("utf-8")
    metadata = (
        ("description", r'<meta name="description" content=".*?">',
         '<meta name="description" content="R0.60 之后的完整研究回顾：R0.61 到 R0.73L 共 128 个节点；最新一节把冻结 rank-one 谱信息升级为参数一致的真实非自治绝热跟踪。">'),
        ("og title", r'<meta property="og:title" content=".*?">',
         '<meta property="og:title" content="R0.61–R0.73L｜R0.60 之后的研究回顾">'),
        ("og description", r'<meta property="og:description" content=".*?">',
         '<meta property="og:description" content="47 个阶段、128 个节点：从约化递推和环带排除到非自伴绝热跟踪与匹配增长作用量。">'),
        ("title", r"<title>.*?</title>",
         "<title>R0.61–R0.73L｜R0.60 之后的研究回顾</title>"),
    )
    for label, pattern, value in metadata:
        html = section(html, pattern, value, "K recap " + label)
    html = required(html, "/i18n-en.js?v=1.51", "/i18n-en.js?v=1.52", "K recap i18n")
    hero = r'''    <header class="hero"><div class="hero-inner"><div><div class="eyebrow">累计回顾 · R0.61–R0.73L · 2026-08-31</div><h1>R0.60 之后的研究回顾</h1><p class="lead">本页保留 R0.61 到 R0.73L 的全部 128 个节点。R0.61–R0.69W 从约化递推走到严格环带排除；R0.70A–R0.71Z 检查移动尺度、临界账本、内部 entry 与 complete-root 边界；R0.72A–R0.73B 处理 strong coupling、critical log、碰撞几何与完整线性 Fourier--Leray 行；R0.73C–I 依次处理冻结 Rayleigh 不稳定、黏性谱簇持续、固定正半平面传递、移动剖面增益、非线性相对放大、平面固定距离偏离与零窗口作用量边界。R0.73J 认证无黏连续谱支，R0.73K 闭合参数一致的黏性 rank-one 谱支及补空间余隙；R0.73L 再用 Kato intertwining、固定快时间块和前向 Volterra 吸收，把这些冻结输入升级为完整慢窗上的真实非自治增长，并得到匹配作用量、\(O(\varepsilon)\) 相对跟踪和 forward-orbit localization。显式绝热阈值、prefactor 极限、两项 WKB、二维非线性、横向三维、奇性与 Clay 没有被外推。</p></div><div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.73L</strong><p>收录节点：128</p><p>回顾截止时公开笔记：188</p><p>回顾截止节点：R0.73L</p><p>问题状态：仍未解决</p></div></div></header>'''
    html = section(html, r'    <header class="hero">.*?</header>', hero, "K recap hero")
    for old, new in (
        ("02 · 127 节完整索引", "02 · 128 节完整索引"),
        ("01 · 46 个研究阶段", "01 · 47 个研究阶段"),
        ("R0.60 之后的路线分成 46 个阶段", "R0.60 之后的路线分成 47 个阶段"),
        ('data-current-route="R0.69P–R0.73K"', 'data-current-route="R0.69P–R0.73L"'),
    ):
        html = required(html, old, new, "K recap counter")
    result = r'''        <section id="result"><div class="section-no">00 / 回顾范围</div><h2>版本数、封存数和数学结论分开报告</h2><div class="metrics"><div class="metric"><strong>128</strong><span>R0.61–R0.73L 研究节点</span></div><div class="metric"><strong>90</strong><span>R0.70A–R0.73L 已公开版本</span></div><div class="metric"><strong>66</strong><span>当前 formal-figure 合同下完整封存</span></div><div class="metric"><strong>24</strong><span>旧版附图档案待回补</span></div></div><p>R0.00–R0.60 保留在上一份阶段回顾。R0.70A–R0.73L 的 90 个版本已经公开，其中 66 个满足当前完整封存合同，24 个历史版本仍欠 formal-figure 回补。公开和封存不表示 Clay 问题已经解决。</p></section>'''
    html = section(html, r'        <section id="result">.*?</section>', result, "K recap result")
    marker = '          </div>\n        </section>\n\n        <section id="node-index">'
    html = once(html, marker, RECAP_PHASE + "\n" + marker, "K recap phase")
    html = required(
        html, "R0.61–R0.73K 的 127 节公开笔记",
        "R0.61–R0.73L 的 128 节公开笔记", "K recap node title",
    )
    node_j = '            <span class="node-ref"><a href="/notes/r0-73k.html">R0.73K</a><span class="node-state kind-closed">闭</span></span>\n'
    node_k = '            <span class="node-ref"><a href="/notes/r0-73l.html">R0.73L</a><span class="node-state kind-closed">闭</span></span>\n'
    html = once(html, node_j, node_j + node_k, "K recap node")
    retained = (
        '            <li>R0.73L 闭合共同定义域演化、Kato intertwining、移动补空间相对稳定、'
        '非自伴绝热跟踪、matching selected gain action 和 action-resolved backward localization；'
        '显式绝热阈值、prefactor 极限、两项 WKB、二维非线性、三维闭合、奇性与 Clay 保持 OPEN。</li>\n'
    )
    html = once(
        html, "          </ul>\n          <p>这些结果可以分别整理成",
        retained + "          </ul>\n          <p>这些结果可以分别整理成",
        "K recap retained",
    )
    value = r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>冻结谱信息已经升级为真实长时间非自治增长</h2><p>不能把 128 个节点或 90 个公开版本解释成 Clay 完成比例。R0.73L 的严格增量是：在同一个小参数同时控制黏性与慢时间的情形下，精确 selected orbit 在完整慢窗上以 \(O(\varepsilon)\) 相对误差跟踪 Kato branch，精确增益与黏性及无黏谱作用量只差统一的两侧乘法常数。显式阈值、prefactor 极限、两项 WKB、二维非线性增长与横向三维仍未证明。</p></section>'''
    html = section(html, r'        <section id="value">.*?</section>', value, "K recap value")
    next_gate = r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.73M 检查绝热尺度上的二维非线性离轨 bootstrap</h2><p>下一节冻结 linear seed、退出时间和二次 Duhamel 余项，检查非线性误差能否在 selected action 达到预定阈值前被严格吸收；若不等式不能闭合，就停在线性定理。</p></section>'''
    html = section(html, r'        <section id="next">.*?</section>', next_gate, "K recap next")
    claims = r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>连续定理、有限诊断和开放问题分开列示</h2><p>R0.70A–R0.73L 的 90 节已公开；66 节完整封存；24 节旧档待回补。</p><p>__CLOSED__。</p><p>__FINITE__。</p><p>__OPEN__。</p><p>15 条主轨迹、5 条独立重算和 346 行附图源数据只作有限维复现与错误探测，不认证连续绝热定理、二维非线性、横向三维或 Clay。NOT CLAY。</p></section>'''
    claims = claims.replace("__CLOSED__", CLOSED).replace("__FINITE__", FINITE).replace("__OPEN__", OPEN)
    html = section(html, r'        <section id="claims">.*?</section>', claims, "K recap claims")
    reproduce = r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证明、审计、实验、附图和历史回顾</h2><p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-73k.html">保留 R0.73K 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-73l.html">打开最新节点 R0.73L</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073l_adiabatic_tracking_proof.md">查看解析证明</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073l_independent_analytic_audit.md">查看独立解析审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073l_adversarial_audit.md">查看反例式审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/experiments/r073l">查看有限诊断包</a> · <a href="/assets/r073l/__FIGURE_ID__.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-73l.pdf">下载同步 PDF</a></p><p>连续定理由解析证明承担；有限诊断只作可复现错误探测。</p></section>'''.replace("__FIGURE_ID__", FIGURE_ID)
    html = section(html, r'        <section id="reproduce">.*?</section>', reproduce, "K recap reproduce")
    footer = r'''  <footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>我按原编号记录定理、有限计算、反例和未解决的问题。</div><div>R0.61–R0.73L 回顾 · 2026-08-31<br><a href="/">返回研究主页</a></div></footer>'''
    html = section(html, r"  <footer>.*?</footer>", footer, "K recap footer")
    start = html.find('<section id="node-index">')
    end = html.find("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', html[start:end])
    if len(links) != 128 or len(set(links)) != 128:
        raise RuntimeError("R0.73L recap expected 128 unique nodes")
    if html.count('<article class="phase">') != 47:
        raise RuntimeError("R0.73L recap expected 47 phases")
    assert_clean(html, "R0.73L recap")
    assert_mathjax_clean(html, "R0.73L recap", check_naked=True)
    assert_public_voice(html, "R0.73L recap")
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
        ('data-site-version="1.51"', 'data-site-version="1.52"'),
        ("/i18n-en.js?v=1.51", "/i18n-en.js?v=1.52"),
        ("/site-refresh.js?v=1.51", "/site-refresh.js?v=1.52"),
        ("<strong>v1.51</strong>网页版本", "<strong>v1.52</strong>网页版本"),
        ("<strong>187</strong>公开研究笔记", "<strong>188</strong>公开研究笔记"),
        ("<strong>R0.73K</strong>最新研究节点", "<strong>R0.73L</strong>最新研究节点"),
        ('<a class="route-map-latest" href="#r073k">跳到首页 R0.73K 卡片 →</a>',
         '<a class="route-map-latest" href="#r073l">跳到首页 R0.73L 卡片 →</a>'),
        ("Research topology · R0.1–R0.73K", "Research topology · R0.1–R0.73L"),
        ("R0.70A–R0.73K：89 节已公开，65 节完整封存",
         "R0.70A–R0.73L：90 节已公开，66 节完整封存"),
        ('<span class="route-range">R0.69P–R0.73K</span>',
         '<span class="route-range">R0.69P–R0.73L</span>'),
        ('aria-label="R0.69P–R0.73K"', 'aria-label="R0.69P–R0.73L"'),
        ("展开 97 篇公开笔记", "展开 98 篇公开笔记"),
        ("本站 R0.69P–R0.73K 路线", "本站 R0.69P–R0.73L 路线"),
        ("综述 v1.51 · 2026-08-31", "综述 v1.52 · 2026-08-31"),
        ("上次综述 v1.50 · 2026-08-30", "上次综述 v1.51 · 2026-08-31"),
    ):
        html = required(html, old, new, "K home " + old)
    html = replace_all(
        html, "/recap-r0-61-r0-73k.html", "/recap-r0-61-r0-73l.html",
        "K home recap HTML links",
    )
    html = replace_all(
        html, "/recap-r0-61-r0-73k.pdf", "/recap-r0-61-r0-73l.pdf",
        "K home recap PDF links",
    )
    historical = (r'<strong style="color:var(--gold)">下一步 R0.73L：</strong>&nbsp;'
                  r'证明或否定非自伴绝热跟踪及其有界前因子。')
    html = required(
        html, historical, historical.replace("下一步", "当时的下一步"),
        "K home historical next",
    )
    focus = r'<div class="summary-item"><strong>我目前关注</strong><span>R0.73L 已把 R0.73K 的冻结 rank-one 谱输入升级为真实非自治演化：共同定义域 Kato transport、移动补空间相对衰减、\(O(\varepsilon)\) 相对跟踪、匹配黏性与无黏作用量的两侧增益，以及 forward-orbit localization 均已闭合。下一关是 R0.73M 的二维非线性离轨 bootstrap。</span></div>'
    html = section(
        html,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        focus,
        "K home focus",
    )
    html = required(
        html,
        "<h3>R0.73K：参数一致黏性 rank-one 谱支与补空间控制已闭合</h3>",
        "<h3>R0.73L：非自伴绝热跟踪与匹配作用量已闭合</h3>",
        "K home current title",
    )
    html = required(
        html, "<span>R0.72R–R0.73K：</span>", "<span>R0.72R–R0.73L：</span>",
        "K home path range",
    )
    html = required(
        html,
        "endpoint audit / continuum upper action / zero-window tangent → unique simple rightmost spectral branch of the continuum operator → parameter-uniform viscous rank-one branch</p>",
        "endpoint audit / continuum upper action / zero-window tangent → unique simple rightmost spectral branch of the continuum operator → parameter-uniform viscous rank-one branch → non-selfadjoint adiabatic tracking / matching selected action</p>",
        "K home path tail",
    )
    link_j = '<a class="milestone" href="/notes/r0-73k.html">R0.73K</a>'
    html = once(
        html, link_j,
        link_j + '\n                  <a class="milestone" href="/notes/r0-73l.html">R0.73L</a>',
        "K home route link",
    )
    route_j = r'''              <p>R0.73K 证明：在共同但未显式量化的黏度阈值内，无黏特征值在整个 \(d\in[0,1/450]\) 上延拓为共同圆内唯一的实代数简单黏性谱支；Riesz 投影在算子范数下一致收敛，特征值偏移满足 \(O(\varepsilon)\) 上界。固定半平面 \(\operatorname{Re}z\ge0.12\) 内无其他谱点；选定 rank-one 谱块的逆向指数 \(0.16\) 与保守安全间隔 \(1/25\) 同时受控。<span>parameter-uniform viscous rank-one branch</span>；<span>finite diagnostic: 1190 states / 952 cross-cutoff comparisons</span>。有限数据只作诊断。</p>
'''
    route_k = r'''              <p>R0.73L 再用 Kato intertwining、固定快时间块和前向 Volterra 吸收，证明真实 selected orbit 在完整慢窗上以 \(O(\varepsilon)\) 相对误差跟踪移动 rank-one 谱线；精确增益与黏性及无黏谱作用量只差统一两侧乘法常数，后向定位由同一条前向轨道相除得到。<span>parameter-uniform nonselfadjoint adiabatic tracking</span>；<span>finite diagnostic: 15 primary / 5 independent / 346 figure rows</span>。有限数据只作复现与错误探测。</p>
'''
    html = once(html, route_j, route_j + route_k, "K home current route summary")
    html = section(
        html, r'            <article class="tree-node next">.*?</article>',
        HOME_NEXT, "K home next gate",
    )
    recap = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem"><p class="eyebrow">累计回顾 R0.61–R0.73L · 2026-08-31</p><h3>R0.60 recap 之后的累计回顾收录 128 个节点；全站现有 188 篇公开研究笔记</h3><p>累计回顾现分 47 个阶段，完整保留 R0.61–R0.73L；最新节点分开记录连续证明、两份解析审计、Deep Research 文献边界、有限诊断和正式附图。</p><p>R0.70A–R0.73L 共 90 个版本已公开；66 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p><p><strong>阶段判断：</strong>&nbsp;非自伴绝热跟踪、匹配 selected action 与 forward-orbit localization 已在封存模型内闭合；显式绝热阈值、prefactor 极限、两项 WKB、二维非线性、横向三维、奇性与 Clay 保持 OPEN。</p><p><a href="/recap-r0-61-r0-73l.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-73l.pdf">下载同步 PDF</a></p></div>'''
    html = section(
        html, r'          <div class="task-one" id="post-r060-recap".*?</div>',
        recap, "K home recap",
    )
    marker = '          </div>\n        </section>\n\n      </article>'
    html = once(
        html, marker,
        '          </div>\n\n' + HOME_L_CARD + '\n        </section>\n\n      </article>',
        "K home card",
    )
    if html.count('data-release="r073l"') != 1:
        raise RuntimeError("home must contain exactly one R0.73L card")
    if html.count('<strong style="color:var(--gold)">下一步 R0.73M：') != 1:
        raise RuntimeError("home must contain exactly one current R0.73M gate")
    route = re.search(
        r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73L">(.*?)</nav>',
        html, flags=re.S,
    )
    links = [] if route is None else re.findall(
        r'href="/notes/r0-[^"]+\.html"', route.group(1)
    )
    if len(links) != 98 or len(set(links)) != 98:
        raise RuntimeError("home current-route index must contain 98 unique note links")
    assert_clean(html, "R0.73L home")
    assert_mathjax_clean(html, "R0.73L home", check_naked=True)
    assert_public_voice(html, "R0.73L home")
    return html


def update_literature() -> str:
    html = git_bytes(
        RELEASE_BASELINE_COMMIT, "public/literature-review.html"
    ).decode("utf-8")
    for old, new in (
        ("/i18n-en.js?v=1.51", "/i18n-en.js?v=1.52"),
        ("本站 R0.69P–R0.73K 只列为研究笔记",
         "本站 R0.69P–R0.73L 只列为研究笔记"),
        ("文献综述 v1.51 · 2026-08-31", "文献综述 v1.52 · 2026-08-31"),
        ("累计回顾与 127 节索引", "累计回顾与 128 节索引"),
        ("打开 127 节完整索引", "打开 128 节完整索引"),
        ("资料截止：2026-08-30", "资料截止：2026-08-31"),
    ):
        html = required(html, old, new, "K literature " + old)
    html = replace_all(
        html, "/recap-r0-61-r0-73k.html", "/recap-r0-61-r0-73l.html",
        "K literature recap links",
    )
    deck_j = r'''<span class="route-r073k-deck-update">R0.73K 在共同但未显式量化的黏度阈值内闭合共同圆内唯一的实代数简单黏性谱支、Riesz 投影在算子范数下的一致收敛、特征值偏移的 \(O(\varepsilon)\) 上界、条件数、固定半平面内无其他谱点，以及补空间 reduced-resolvent 与半群增长上界。1,190 个有限状态与 952 个跨 cutoff 比较只作诊断。</span></p>'''
    deck_k = deck_j[:-4] + r'''<span class="route-r073l-deck-update">R0.73L 用 Kato intertwining、固定快时间块和前向 Volterra 吸收，把冻结 rank-one 谱输入升级为真实非自治演化：相对跟踪误差为 \(O(\varepsilon)\)，精确增益与黏性及无黏谱作用量只差统一两侧乘法常数，后向定位由同一条前向轨道相除得到。15 条主轨迹、5 条独立重算和 346 行附图源数据只作有限诊断。</span></p>'''
    html = required(html, deck_j, deck_k, "K literature route deck endpoint")
    old_open = r'''<div class="route-step pause"><header><b>开放接口 · R0.73L</b><strong>non-selfadjoint adiabatic tracking</strong></header><p>在共同定义域和上述非正规谱分解下估计移动投影耦合，检查 \(D_*/\varepsilon\) 时间尺度上的有界前因子和匹配作用量。</p></div>'''
    new_steps = r'''<div class="route-step kept"><header><b>R0.73L</b><strong>parameter-uniform nonselfadjoint adiabatic tracking</strong></header><p>共同定义域 Kato transport、固定快时间块、移动补空间相对衰减、前向 Volterra 吸收、matching selected action 和 forward-orbit localization 已经闭合。显式阈值、prefactor 极限和两项 WKB 仍开放。<a href="/notes/r0-73l.html">研究笔记</a> <a href="/recap-r0-61-r0-73l.html">当前累计回顾</a> <a href="#r073l-boundary">文献边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.73M</b><strong>adiabatic-scale two-dimensional nonlinear departure bootstrap</strong></header><p>冻结 linear seed、退出时间和二次 Duhamel 余项，检查非线性误差能否在 selected action 达到阈值前被严格吸收。</p></div>'''
    html = once(html, old_open, new_steps, "K literature route")
    boundary = r'''

          <h3 id="r073l-boundary">R0.73L 的非自伴绝热跟踪文献边界</h3>
          <p><a href="#ref-167">Schmid</a>给出共同定义域上一般线性算子的绝热定理，是本节最接近的抽象先例；但其直接 \(O(\varepsilon)\) 比较使用 Kato stability、graph-space 正则性和二阶投影正则性，这些常数没有在当前黏性奇异极限中被统一验证。<a href="#ref-168">Abou Salem--Fröhlich</a>处理 nonnormal common-domain generator，但 quasi-bounded 情形会带来不适合当前增长支的指数比较因子。</p>
          <p><a href="#ref-169">Joye</a>说明非平凡 nilpotent block 可产生次指数 prefactor；R0.73K 的 rank-one 代数简单性因此是必要输入。<a href="#ref-170">Avron--Fraas--Graf--Grech</a>处理 contraction-semigroup generators，但当前归一化补空间尚未在一个共同范数下证明 contractive。<a href="#ref-171">Kato</a>提供 parallel-transport commutator 的原始结构；<a href="#ref-172">Nenciu--Rasche</a>给出有限维非自伴绝热失效的警示。</p>
          <p>限定检索没有发现一条现成定理同时覆盖这里的双参数统一性：同一个 \(\varepsilon\) 既乘在无界椭圆项前，又决定 \(D_*/\varepsilon\) 的绝热时间。R0.73L 因而在封存模型内使用固定快时间块直接证明移动补空间相对估计，只需统一 \(P_\varepsilon'\) 界，不声称一般非自伴绝热理论的首创、强化或优先权。</p>
          <div class="boundary"><strong>R0.73L 的主张边界</strong><p>__CLOSED__。</p><p>__FINITE__。</p><p>__OPEN__。</p><p>这是特定两谐波周期剪切流族的连续线性绝热定理，并附带有限 Fourier 诊断；它不是显式绝热阈值、prefactor 极限、两项 WKB、非线性不稳定、三维闭合、有限时间奇性或 Clay 证明。NOT CLAY。</p></div>'''
    boundary = boundary.replace("__CLOSED__", CLOSED).replace("__FINITE__", FINITE).replace("__OPEN__", OPEN)
    match = re.search(
        r'(<h3 id="r073k-boundary">.*?<div class="boundary">.*?</div>)',
        html, flags=re.S,
    )
    if match is None:
        raise RuntimeError("K literature expected R0.73K boundary")
    html = once(
        html, match.group(1), match.group(1) + boundary,
        "K literature boundary",
    )
    references = r'''            <li id="ref-167">J. Schmid. <a href="https://arxiv.org/abs/1804.11213"><em>Adiabatic theorems for general linear operators with time-independent domains</em></a>. Asymptotic Analysis 113 (2019), 1--64; <a href="https://doi.org/10.1142/S0129055X19500144">DOI</a>.</li>
            <li id="ref-168">W. K. Abou Salem and J. Fröhlich. <a href="https://arxiv.org/abs/math-ph/0607054"><em>Adiabatic theorems for quantum resonances</em></a>. Communications in Mathematical Physics 273 (2007), 651--675.</li>
            <li id="ref-169">A. Joye. <a href="https://arxiv.org/abs/math-ph/0608059"><em>General adiabatic evolution with a gap condition</em></a>. Communications in Mathematical Physics 275 (2007), 139--162.</li>
            <li id="ref-170">J. E. Avron, M. Fraas, G. M. Graf and P. Grech. <a href="https://arxiv.org/abs/1106.4661"><em>Adiabatic theorems for generators of contracting evolutions</em></a>. Communications in Mathematical Physics 314 (2012), 163--191.</li>
            <li id="ref-171">T. Kato. <a href="https://www.jstage.jst.go.jp/article/jpsj1946/5/6/5_6_435/_article"><em>On the adiabatic theorem of quantum mechanics</em></a>. Journal of the Physical Society of Japan 5 (1950), 435--439.</li>
            <li id="ref-172">G. Nenciu and G. Rasche. <a href="https://doi.org/10.1088/0305-4470/25/21/027"><em>On the adiabatic theorem for nonself-adjoint Hamiltonians</em></a>. Journal of Physics A 25 (1992), 5741--5751.</li>
'''
    html = once(
        html, '          </ol>\n          <p class="source-note">',
        references + '          </ol>\n          <p class="source-note">',
        "K literature references",
    )
    ids = re.findall(r'\bid="([^"]+)"', html)
    if len(ids) != len(set(ids)):
        duplicates = sorted({value for value in ids if ids.count(value) > 1})
        raise RuntimeError("R0.73L literature duplicate HTML ids: " + ", ".join(duplicates))
    for number in range(167, 173):
        if ids.count(f"ref-{number}") != 1:
            raise RuntimeError(f"R0.73L literature reference ref-{number} is not unique")
    assert_clean(html, "R0.73L literature")
    assert_mathjax_clean(html, "R0.73L literature", check_naked=True)
    assert_public_voice(html, "R0.73L literature")
    return html


def build_manifest_outputs() -> dict[Path, bytes]:
    release_path = ROOT / "research/release-manifest.json"
    release = strict_json(release_path, "release manifest")
    for key, value in R073K_BASELINE.items():
        if release.get(key) != value:
            raise RuntimeError("release manifest changed during R0.73L generation: " + key)
    release.update({
        **R073L_TARGET,
        "latestReleaseGate": "tests/r073l-adiabatic-tracking-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r073l-release.test.mjs",
    })
    release.pop("nextReleaseSourceStage", None)

    site_path = PUBLIC / "site-version.json"
    site = strict_json(site_path, "site version")
    if site != {
        "schemaVersion": "research-site-version-v1",
        "version": "1.51",
        "latestRelease": "R0.73K",
        "publicHtmlNoteCount": 187,
        "publishedDate": "2026-08-31",
    }:
        raise RuntimeError("site-version changed during R0.73L generation")
    site.update({
        "version": "1.52",
        "latestRelease": "R0.73L",
        "publicHtmlNoteCount": 188,
        "publishedDate": "2026-08-31",
    })

    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = strict_json(inventory_path, "formal archive inventory")
    state = (
        inventory.get("latestPublishedRelease"), inventory.get("publishedReleaseCount"),
        inventory.get("formalSealedReleaseCount"), inventory.get("legacyFormalFigureBacklogCount"),
    )
    if state != ("r073k", 89, 65, 24):
        raise RuntimeError("formal archive changed during R0.73L generation")
    for key in ("publishedReleases", "formalSealedReleases"):
        rows = inventory.get(key)
        if not isinstance(rows, list) or rows[-1:] != ["r073k"] or "r073l" in rows:
            raise RuntimeError("formal archive is not append-only: " + key)
        rows.append("r073l")
    inventory.update({
        "latestPublishedRelease": "r073l",
        "publishedReleaseCount": 90,
        "formalSealedReleaseCount": 66,
        "legacyFormalFigureBacklogCount": 24,
    })
    if (
        len(inventory["publishedReleases"]) != 90
        or len(set(inventory["publishedReleases"])) != 90
        or len(inventory["formalSealedReleases"]) != 66
        or len(set(inventory["formalSealedReleases"])) != 66
    ):
        raise RuntimeError("formal archive count or uniqueness mismatch after R0.73L")
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
        ROOT / "VERSION": b"1.52\n",
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
        with tempfile.TemporaryDirectory(prefix="r073l-baseline-notes-") as temporary:
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
            if len(existing) != 187 or any(note.slug == "r0-73l" for note in existing):
                raise RuntimeError("R0.73L note-index frozen baseline is not exact")
            latest = note_index.Note(
                slug="r0-73l", code="R0.73L",
                title="Parameter-uniform nonselfadjoint adiabatic tracking",
                major=73, has_pdf=True,
            )
            note_index.json = TargetJson
            note_index.latest_recap_href = lambda: "/recap-r0-61-r0-73l.html"
            index = note_index.render([latest] + existing)
    finally:
        note_index.json = old_json
        note_index.latest_recap_href = old_latest_recap_href
        note_index.ROOT, note_index.PUBLIC, note_index.NOTES, note_index.OUTPUT = old_paths
    for token in (
        'data-site-version="1.52"',
        "188 篇公开研究笔记",
        "<strong>R0.73L</strong><span>最新研究节点</span>",
        'data-note="r0-73l"',
        "/recap-r0-61-r0-73l.html",
        "研究笔记总索引 · v1.52 · 2026-08-31",
    ):
        if token not in index:
            raise RuntimeError("R0.73L note index missing token: " + token)
    assert_clean(index, "R0.73L note index")
    assert_mathjax_clean(index, "R0.73L note index", check_naked=True)
    assert_public_voice(index, "R0.73L note index")
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
    web_target = PUBLIC / "assets/r073l"
    for suffix in ("pdf", "svg", "png"):
        name = f"figure.{suffix}"
        row = by_name.get(name)
        payload = (source / name).read_bytes()
        if (
            row is None
            or sha256_bytes(payload) != row.get("sha256")
            or len(payload) != row.get("bytes")
        ):
            raise RuntimeError("R0.73L public figure master is not manifest-bound: " + name)
        staged[web_target / f"{FIGURE_ID}.{suffix}"] = payload


def validate_staged(staged: dict[Path, bytes]) -> None:
    required_paths = (
        PUBLIC / "notes/r0-73l.html",
        PUBLIC / "recap-r0-61-r0-73l.html",
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
            raise RuntimeError("R0.73L transaction missing staged path " + str(path))
    for name in FIGURE_PACKAGE_PATHS:
        if PUBLIC / FIGURE_RELATIVE / name not in staged:
            raise RuntimeError("R0.73L transaction omitted figure-package asset " + name)
    for suffix in ("pdf", "svg", "png"):
        if PUBLIC / f"assets/r073l/{FIGURE_ID}.{suffix}" not in staged:
            raise RuntimeError("R0.73L transaction omitted web figure master " + suffix)
    for path in staged:
        if path.suffix.lower() == ".pdf" and (
            "assets/r073l" not in path.as_posix()
            and FIGURE_RELATIVE not in path.as_posix()
        ):
            raise RuntimeError("R0.73L HTML transaction must not generate note or recap PDFs")

    html_paths = (
        PUBLIC / "notes/r0-73l.html",
        PUBLIC / "recap-r0-61-r0-73l.html",
        PUBLIC / "research-review.html",
        PUBLIC / "literature-review.html",
        PUBLIC / "notes/index.html",
    )
    for path in html_paths:
        value = staged[path].decode("utf-8")
        assert_clean(value, path.name)
        assert_mathjax_clean(value, path.name, check_naked=True)
        assert_public_voice(value, path.name)
        if "/i18n-en.js?v=1.52" not in value:
            raise RuntimeError("R0.73L staged HTML has stale i18n version: " + path.name)
    note = staged[PUBLIC / "notes/r0-73l.html"].decode("utf-8")
    for token in (
        CLOSED, FINITE, OPEN, "NOT CLAY", "15 条主轨迹", "1.0281276",
        "6.711726", "0.12", "0.16", "R0.73M",
    ):
        if token not in note:
            raise RuntimeError("R0.73L staged note lost boundary token: " + token)
    recap = staged[PUBLIC / "recap-r0-61-r0-73l.html"].decode("utf-8")
    start = recap.index('<section id="node-index">')
    end = recap.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', recap[start:end])
    if (
        len(links) != 128
        or len(set(links)) != 128
        or recap.count('<article class="phase">') != 47
    ):
        raise RuntimeError("R0.73L staged recap inventory is invalid")
    home = staged[PUBLIC / "research-review.html"].decode("utf-8")
    route = re.search(
        r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73L">(.*?)</nav>',
        home, flags=re.S,
    )
    route_links = [] if route is None else re.findall(
        r'href="/notes/(r0-[^"]+)\.html"', route.group(1)
    )
    for token in (
        "<h3>R0.73L：非自伴绝热跟踪与匹配作用量已闭合</h3>",
        "parameter-uniform nonselfadjoint adiabatic tracking",
        "finite diagnostic: 15 primary / 5 independent / 346 figure rows",
    ):
        if token not in home:
            raise RuntimeError("R0.73L staged home lost route token: " + token)
    if len(route_links) != 98 or len(set(route_links)) != 98:
        raise RuntimeError("R0.73L staged home route inventory is invalid")
    literature = staged[PUBLIC / "literature-review.html"].decode("utf-8")
    for token in (
        'class="route-r073l-deck-update"', 'id="r073l-boundary"',
        CLOSED, FINITE, OPEN, "ref-167", "ref-172", "开放接口 · R0.73M",
    ):
        if token not in literature:
            raise RuntimeError("R0.73L staged literature lost token: " + token)
    literature_ids = re.findall(r'\bid="([^"]+)"', literature)
    if len(literature_ids) != len(set(literature_ids)):
        raise RuntimeError("R0.73L staged literature contains duplicate HTML ids")
    site = json.loads(staged[PUBLIC / "site-version.json"])
    release = json.loads(staged[ROOT / "research/release-manifest.json"])
    inventory = json.loads(staged[ROOT / "research/formal-archive-inventory.json"])
    if (
        site.get("version") != "1.52"
        or site.get("publicHtmlNoteCount") != 188
        or release.get("postR060RecapNodeCount") != 128
        or release.get("postR070APublishedReleaseCount") != 90
        or release.get("postR070AFormalSealedReleaseCount") != 66
        or release.get("legacyFormalFigureBacklogCount") != 24
        or inventory.get("publishedReleaseCount") != 90
        or inventory.get("formalSealedReleaseCount") != 66
    ):
        raise RuntimeError("R0.73L staged accounting drifted")


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
    descriptor, temporary = tempfile.mkstemp(prefix="." + path.name + ".r073l-", dir=path.parent)
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
        raise RuntimeError("R0.73L transaction is empty")
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
            raise RuntimeError("R0.73L materialized figure-package asset missing: " + name)
        if target.read_bytes() != (source / name).read_bytes():
            raise RuntimeError("R0.73L public figure-package asset is not byte-identical: " + name)
    rows = {
        str(row.get("path", "")): row
        for row in figure_manifest.get("figure", {}).get("outputs", [])
        if isinstance(row, dict)
    }
    for suffix in ("pdf", "svg", "png"):
        source_path = source / f"figure.{suffix}"
        target_path = PUBLIC / f"assets/r073l/{FIGURE_ID}.{suffix}"
        row = rows.get(f"figure.{suffix}")
        if row is None or not target_path.is_file() or target_path.is_symlink():
            raise RuntimeError("R0.73L materialized web figure missing: " + suffix)
        if target_path.read_bytes() != source_path.read_bytes():
            raise RuntimeError("R0.73L public web figure is not byte-identical: " + suffix)
        if digest(target_path) != row.get("sha256") or target_path.stat().st_size != row.get("bytes"):
            raise RuntimeError("R0.73L materialized web figure escaped manifest: " + suffix)


def publication_stage_incomplete() -> bool:
    pdfs = (
        PUBLIC / "notes/r0-73l.pdf",
        PUBLIC / "recap-r0-61-r0-73l.pdf",
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
            (ROOT / "scripts/i18n-snapshots/r073l-missing.json").read_text(encoding="utf-8")
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
        if isinstance(row, dict) and re.fullmatch(r"r073l\d{3}", str(row.get("id", "")))
    } if isinstance(translations, list) else {}
    if len(by_id) != len(snapshot):
        return True
    for index, snapshot_row in enumerate(snapshot, 1):
        row = by_id.get(f"r073l{index:03d}")
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
            "Validate or explicitly apply the staged R0.73L HTML/manifest transaction. "
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
        help="explicitly apply the HTML/manifest transaction from the exact R0.73K source",
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
            "release": "R0.73L",
            "siteVersion": "1.52",
            "notes": 188,
            "recapNodes": 128,
            "published": 90,
            "formalSealed": 66,
            "legacyBacklog": 24,
            "phases": 47,
            "routeNotes": 98,
            "next": "R0.73M",
            "rootVersion": "1.52",
            "noOp": synchronized_assets == 0,
            "publicationStageIncomplete": publication_stage_incomplete(),
            "pdfGenerated": False,
            "translationsGenerated": False,
            "synchronizedAssets": synchronized_assets,
        }, ensure_ascii=False))
        return

    staged: dict[Path, bytes] = {}
    stage_figure_assets(staged, figure_manifest)
    staged[PUBLIC / "notes/r0-73l.html"] = build_note().encode("utf-8")
    staged[PUBLIC / "recap-r0-61-r0-73l.html"] = build_recap().encode("utf-8")
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
            "release": "R0.73L",
            "sourceState": "R0.73K",
            "checkOnly": True,
            "wouldWrite": len(staged),
            "publicationStageIncomplete": True,
        }, ensure_ascii=False))
        return

    commit_transaction(staged)
    if len(list((PUBLIC / "notes").glob("r0-*.html"))) != 188:
        raise RuntimeError("R0.73L postcommit note count is not 188")
    verify_materialized_figure_assets(figure_manifest)
    print(json.dumps({
        "release": "R0.73L",
        "siteVersion": "1.52",
        "notes": 188,
        "recapNodes": 128,
        "published": 90,
        "formalSealed": 66,
        "legacyBacklog": 24,
        "phases": 47,
        "routeNotes": 98,
        "next": "R0.73M",
        "rootVersion": "1.52",
        "noOp": False,
        "publicationStageIncomplete": True,
        "pdfGenerated": False,
        "translationsGenerated": False,
    }, ensure_ascii=False))



if __name__ == "__main__":
    main()
