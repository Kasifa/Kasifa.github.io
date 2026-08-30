#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the fail-closed transactional R0.73J GitHub Pages release.

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
from pathlib import Path
import re
import subprocess
import tempfile

from generate_r072o_release import assert_clean, once, required, section
from generate_r072p_release import assert_mathjax_clean
from r073j_release_content import (
    AUDIT_STATUS,
    CLOSED,
    FAILURE_HISTORY,
    FIGURE_ID,
    FIGURE_RELATIVE,
    HOME_I_CARD,
    HOME_LATEST_SPOTLIGHT,
    HOME_NEXT,
    NOTE_ARTICLE,
    NOTE_HERO,
    OPEN,
    R073I_BASELINE,
    R073J_TARGET,
)


ROOT = Path(os.environ.get(
    "R073J_RELEASE_ROOT", Path(__file__).resolve().parents[1]
)).resolve()
PUBLIC = ROOT / "public"

ANALYTIC_SOURCE_COMMIT = "ec321d9612389e1f5b056561f12023b5314bcbf3"
EXPERIMENT_PACKAGE_COMMIT = "5fa1c04d01dd639bc97f3dadcd93122d618b8053"
FIGURE_PACKAGE_COMMIT = "e1ef753a3b4af6204a243147b36975cfe614643e"
RELEASE_SOURCE_COMMIT = "4560d00cf3f1261cadfa5b000091e8a0524d75b5"

COMMIT_PLACEHOLDERS = (
    ANALYTIC_SOURCE_COMMIT,
    EXPERIMENT_PACKAGE_COMMIT,
    FIGURE_PACKAGE_COMMIT,
    RELEASE_SOURCE_COMMIT,
)

RELEASE_SOURCE_EXACT_PATHS = (
    ".github/workflows/pages.yml",
    ".github/workflows/release-publication-gate.yml",
    "research/validate_figure_package.py",
    "scripts/r073j_release_content.py",
    "scripts/add-r073j-translations.mjs",
    "scripts/generate_r072o_release.py",
    "scripts/generate_r072p_release.py",
    "scripts/generate_note_index.py",
    "scripts/i18n-lib.mjs",
    "scripts/run-release-publication-gate.mjs",
    "tests/bilingual-content.test.mjs",
    "tests/internal-public-links.test.mjs",
    "tests/release-publication-gate-runner.test.mjs",
    "tests/release-publication-invariant.test.mjs",
    "tests/r073j-continuum-branch-gate.test.mjs",
    "tests/r073j-release.test.mjs",
    "tests/site-route-current-boundary.test.mjs",
)

SOURCE_PATHS = (
    "research/r073j_problem_freeze.md",
    "research/r073j_continuum_branch_theorem.md",
    "research/r073j_analytic_proof.md",
    "research/r073j_overlap_analytic_proof.md",
    "research/r073j_analytic_audit.md",
    "research/r073j_adversarial_audit.md",
    "research/r073j_literature_audit.md",
    "research/r073j_gap_matrix.md",
    "research/r073j_bilingual_dictionary.md",
    "research/r073j_report-source.md",
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
        raise RuntimeError("R0.73J release generator is not UTF-8") from exc
    value, count = re.subn(
        r'(?m)^RELEASE_SOURCE_COMMIT = "[^"]+"$',
        'RELEASE_SOURCE_COMMIT = "__NORMALIZED_RELEASE_SOURCE_COMMIT__"',
        value,
    )
    if count != 1:
        raise RuntimeError("R0.73J release generator must have exactly one release-source pin")
    return value.encode("utf-8")


def verify_exact_directory_at_commit(directory: Path, commit: str, label: str) -> None:
    current = regular_flat_paths(directory, label)
    frozen = git_paths(commit, directory.relative_to(ROOT).as_posix())
    if current != frozen:
        raise RuntimeError(label + ": directory inventory differs from sealed commit")
    for relative in current:
        if (ROOT / relative).read_bytes() != git_bytes(commit, relative):
            raise RuntimeError(label + ": file differs from sealed commit " + relative)


def verify_flat_ledger(directory: Path, label: str) -> None:
    paths = regular_flat_paths(directory, label)
    ledger = directory / "SHA256SUMS"
    if ledger.relative_to(ROOT).as_posix() not in paths:
        raise RuntimeError(label + ": SHA256SUMS missing")
    declared: list[str] = []
    for row in ledger.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/\\\r\n]+)", row)
        if match is None:
            raise RuntimeError(label + ": malformed SHA256SUMS row")
        name = match.group(2)
        path = directory / name
        if name in declared or not path.is_file() or path.is_symlink():
            raise RuntimeError(label + ": invalid ledger entry " + name)
        if digest(path) != match.group(1):
            raise RuntimeError(label + ": hash mismatch " + name)
        declared.append(name)
    actual = sorted(path.name for path in directory.iterdir() if path.name != "SHA256SUMS")
    if declared != sorted(declared) or declared != actual:
        raise RuntimeError(label + ": ledger inventory is not exact and sorted")


def ensure_commits_ready() -> None:
    if any(value.startswith("TO_BE_FILLED_") for value in COMMIT_PLACEHOLDERS):
        raise RuntimeError(
            "R0.73J release is intentionally sealed shut: replace the "
            "release-source commit placeholder after that commit"
        )
    chain = (("analytic source", ANALYTIC_SOURCE_COMMIT),
             ("complete experiment package", EXPERIMENT_PACKAGE_COMMIT),
             ("complete figure package", FIGURE_PACKAGE_COMMIT),
             ("release source", RELEASE_SOURCE_COMMIT))
    for label, commit in chain:
        require_commit(commit, "R0.73J " + label)
    for (left_label, left), (right_label, right) in zip(chain, chain[1:]):
        if not is_ancestor(left, right):
            raise RuntimeError(f"R0.73J commit order invalid: {left_label} < {right_label}")
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()
    if not is_ancestor(RELEASE_SOURCE_COMMIT, head):
        raise RuntimeError("R0.73J release source commit is not an ancestor of HEAD")
    for relative in RELEASE_SOURCE_EXACT_PATHS:
        if git_bytes(RELEASE_SOURCE_COMMIT, relative) != (ROOT / relative).read_bytes():
            raise RuntimeError("R0.73J release source is not pinned: " + relative)
    generator_relative = "scripts/generate_r073j_release.py"
    if normalized_release_generator(git_bytes(RELEASE_SOURCE_COMMIT, generator_relative)) != normalized_release_generator((ROOT / generator_relative).read_bytes()):
        raise RuntimeError("R0.73J release generator differs from pinned source outside its self pin")


def validate_analytic_sources() -> None:
    for relative in SOURCE_PATHS:
        path = ROOT / relative
        if not path.is_file() or path.is_symlink():
            raise RuntimeError("missing R0.73J analytic source: " + relative)
        if path.read_bytes() != git_bytes(ANALYTIC_SOURCE_COMMIT, relative):
            raise RuntimeError("R0.73J source differs from analytic source commit: " + relative)

    source_text = {relative: (ROOT / relative).read_text(encoding="utf-8")
                   for relative in SOURCE_PATHS}
    combined = "\n".join(source_text.values())
    for token in (
        "(167/1000,173/1000)", "0.585343", "0.585009", "1.84154",
        "5.49948", "0.164355", "76", "83", "depth-two", "Clay",
    ):
        if token not in combined:
            raise RuntimeError("R0.73J analytic source missing boundary token: " + token)
    gap = source_text["research/r073j_gap_matrix.md"]
    for key in ("J0", "J1", "J2", "J3", "J4", "J5", "J6", "J7",
                "J8", "J9", "J10", "J11"):
        if key not in gap:
            raise RuntimeError("R0.73J gap matrix lost " + key)
    for token in ("shared raw", "shared-grid", "wrapping-inconclusive"):
        if token.lower() not in combined.lower():
            raise RuntimeError("R0.73J audit qualification missing: " + token)
    for label, value in source_text.items():
        assert_public_voice(value, "R0.73J " + label)


def validate_experiment() -> dict:
    directory = ROOT / "experiments/r073j"
    verify_exact_directory_at_commit(directory, EXPERIMENT_PACKAGE_COMMIT, "R0.73J experiment")
    verify_flat_ledger(directory, "R0.73J experiment")
    manifest = strict_json(directory / "manifest.json", "R0.73J experiment manifest")
    summary = strict_json(directory / "summary.json", "R0.73J experiment summary")
    if manifest.get("schemaVersion") != "r073j-validated-computation-manifest-v1":
        raise RuntimeError("R0.73J experiment manifest schema drifted")
    if summary.get("schemaVersion") != "r073j-continuum-spectral-branch-summary-v1":
        raise RuntimeError("R0.73J experiment summary schema drifted")
    if (
        manifest.get("release") != "R0.73J"
        or manifest.get("sourceCommit") != ANALYTIC_SOURCE_COMMIT
        or manifest.get("allChecksPass") is not True
        or manifest.get("diagnosticOnly") is not False
        or manifest.get("sharedRawGridLimitationDeclared") is not True
        or manifest.get("naturalBoxAuditIsPrerequisite") is not False
        or summary.get("status") != "passed"
    ):
        raise RuntimeError("R0.73J experiment failed or lost its audit boundary")
    boundary = manifest.get("claimBoundary", {})
    if summary.get("claimBoundary") != boundary or boundary != {
        "continuumSpectralBranchCertified": True,
        "kineticOverlapAndPhaseAnchorCertified": True,
        "viscousRankOneBranchCertified": False,
        "nonselfadjointAdiabaticRemainderCertified": False,
        "transverseThreeDimensionalClosureCertified": False,
        "finiteTimeSingularityCertified": False,
        "clayProblemSolved": False,
    }:
        raise RuntimeError("R0.73J experiment claim boundary drifted")
    theorem = summary.get("theorem", {})
    if theorem != {
        "parameterInterval": "0 <= d <= 1/450",
        "rootInterval": "167/1000 < lambda_0(d) < 173/1000",
        "onlySpectrumRightOf": "Re(lambda) > 11/100",
        "otherSpectrumUpperRealPart": "11/100",
        "strictRealPartGap": "57/1000",
        "conservativeGap": "1/20",
        "algebraicallySimple": True,
        "realAnalyticBranch": True,
    }:
        raise RuntimeError("R0.73J experiment theorem ledger drifted")
    for group in ("sourceBindings", "evidenceBindings", "generatedBindings"):
        rows = manifest.get(group)
        if not isinstance(rows, list) or not rows:
            raise RuntimeError("R0.73J experiment missing " + group)
        for row in rows:
            relative = str(row.get("path", ""))
            path = ROOT / relative if "/" in relative else directory / relative
            if not path.is_file() or digest(path) != row.get("sha256") or path.stat().st_size != row.get("bytes"):
                raise RuntimeError("R0.73J experiment stale binding: " + relative)
            if group != "generatedBindings" and git_bytes(ANALYTIC_SOURCE_COMMIT, relative) != path.read_bytes():
                raise RuntimeError("R0.73J experiment input differs from frozen commit: " + relative)
    frozen = {
        "research/r073j_analytic_proof.md": "81061d6f77e97fca33dafa0643820ab3860ae02b4042fe742eac1d91f1f108f0",
        "research/r073j_analytic_audit.md": "f134d4a828ed0f91c62899a41e9640b8e5ed211f375a4a92913e76a1f537de5e",
        "research/r073j_overlap_analytic_proof.md": "89c94e9d3ab9cd892f4f20ff8d2a3932b3f5fef6e82135ea2e64f39148c42f02",
        "experiments/r073j/contour_certificate.json": "60c770beaf0dc9a3da99ba6ab7bff234b506aa7d8bc72a0aad7b55471b571a38",
        "experiments/r073j/overlap_certificate.json": "12e1505cacb807d83a611b96d5b928bd4302c9faef16030566d3e178234180ab",
        "experiments/r073j/independent_validation.json": "203b7af48933cdb49c0a0b59751c0b0435cf26ae48ea01e08f203900ad554d57",
        "experiments/r073j/natural_box_validation.json": "2d92b6055ba847ffeda2a36a11d7c294df6d65925fd5e7dd00ec0cf6f7645c9a",
    }
    for relative, expected in frozen.items():
        if digest(ROOT / relative) != expected:
            raise RuntimeError("R0.73J frozen proof/certificate hash drifted: " + relative)
    contour = strict_json(directory / "contour_certificate.json", "contour certificate")
    overlap = strict_json(directory / "overlap_certificate.json", "overlap certificate")
    independent = strict_json(directory / "independent_validation.json", "contour audit")
    independent_overlap = strict_json(directory / "independent_overlap_validation.json", "overlap audit")
    natural = strict_json(directory / "natural_box_validation.json", "natural-box audit")
    refine = strict_json(directory / "natural_box_refinement.json", "depth-two audit")
    deep = strict_json(directory / "natural_box_refinement_deep.json", "deep audit")
    failure = strict_json(directory / "failure_ledger.json", "failure ledger")
    cd, od = contour.get("decisions", {}), overlap.get("decisions", {})
    if contour.get("status") != "passed" or len(contour.get("panels", [])) != 64:
        raise RuntimeError("R0.73J contour certificate is incomplete")
    if not (cd.get("globalBoundaryNonzeroForAllD") is True and cd.get("localBoundaryNonzeroForAllD") is True
            and cd.get("globalBasePositiveOrientationWinding") == 1 and cd.get("localBasePositiveOrientationWinding") == 1
            and str(cd.get("globalMinimumAbsoluteLower", "")).startswith("[5.499484")
            and str(cd.get("localMinimumAbsoluteLower", "")).startswith("[0.164355")):
        raise RuntimeError("R0.73J contour decisions drifted")
    if overlap.get("status") != "passed" or len(overlap.get("cells", [])) != 128:
        raise RuntimeError("R0.73J overlap certificate is incomplete")
    if not (str(od.get("minimumKineticOverlapLower", "")).startswith("[0.585343")
            and str(od.get("minimumAnchorAbsoluteLower", "")).startswith("[1.841548")):
        raise RuntimeError("R0.73J overlap decisions drifted")
    if independent.get("classification") != "independent-postprocessing-from-shared-raw-grid":
        raise RuntimeError("R0.73J shared raw-grid contour boundary drifted")
    if "shared-raw-grid" not in json.dumps(independent_overlap, ensure_ascii=False):
        raise RuntimeError("R0.73J shared raw-grid overlap boundary drifted")
    nd, rd, dd = natural.get("decisions", {}), refine.get("decisions", {}), deep.get("decisions", {})
    if natural.get("status") != "failed" or (nd.get("passedBoxCount"), nd.get("failedBoxCount")) != (76, 7):
        raise RuntimeError("R0.73J natural-box first-round ledger drifted")
    if refine.get("status") != "inconclusive" or (rd.get("originalFailedParentCount"), rd.get("secondLevelPassedBoxCount"), rd.get("secondLevelFailedBoxCount")) != (7, 16, 96):
        raise RuntimeError("R0.73J depth-two 1/7 ledger drifted")
    if deep.get("status") != "passed" or dd.get("resolvedOriginalParentCount") != 7 or dd.get("finalInconclusiveLeafBoxCount") != 0:
        raise RuntimeError("R0.73J deep natural-box audit is not complete")
    if len(failure.get("entries", [])) != 2:
        raise RuntimeError("R0.73J failure-method ledger drifted")
    return manifest


def validate_figure() -> dict:
    directory = ROOT / FIGURE_RELATIVE
    verify_exact_directory_at_commit(directory, FIGURE_PACKAGE_COMMIT, "R0.73J figure")
    verify_flat_ledger(directory, "R0.73J figure")
    manifest = strict_json(directory / "manifest.json", "R0.73J figure manifest")
    results = strict_json(directory / "results.json", "R0.73J figure results")
    contract = strict_json(directory / "contract.json", "R0.73J figure contract")
    config = strict_json(directory / "config.json", "R0.73J figure config")
    validation = strict_json(directory / "validation.json", "R0.73J figure validation")
    schemas = {"manifest": (manifest, "r073j-continuum-branch-figure-manifest-v1"),
               "results": (results, "r073j-continuum-branch-figure-results-v1"),
               "contract": (contract, "r073j-continuum-branch-figure-contract-v1"),
               "config": (config, "r073j-continuum-branch-figure-config-v1"),
               "validation": (validation, "r073j-continuum-branch-figure-validation-v1")}
    for label, (payload, expected_schema) in schemas.items():
        if payload.get("schemaVersion") != expected_schema:
            raise RuntimeError("R0.73J figure " + label + " schema drifted")
    if (
        manifest.get("release") != "R0.73J"
        or manifest.get("figureId") != FIGURE_ID
        or manifest.get("status") != "formal"
        or manifest.get("publicationStatus") != "prepublication"
        or manifest.get("git", {}).get("publicationCommitAssigned") is not False
    ):
        raise RuntimeError("R0.73J figure status or provenance drifted")
    if results.get("status") != "passed" or validation.get("status") != "passed" or not all(validation.get("checks", {}).values()):
        raise RuntimeError("R0.73J figure results failed or lost provenance")
    boundary = manifest.get("claimBoundary", {})
    if not (boundary.get("continuumSpectralBranchCountCertified") is True
            and boundary.get("kineticOverlapThresholdCertified") is True
            and boundary.get("viscousBranchCertified") is False
            and boundary.get("adiabaticRemainderCertified") is False
            and boundary.get("clayProblemSolved") is False
            and results.get("claimBoundary") == boundary
            and validation.get("claimBoundary") == boundary):
        raise RuntimeError("R0.73J figure escaped its exact claim boundary")
    rows = manifest.get("files", [])
    if not isinstance(rows, list) or {row.get("path") for row in rows} != set(FIGURE_PACKAGE_PATHS) - {"manifest.json", "SHA256SUMS"}:
        raise RuntimeError("R0.73J figure manifest inventory drifted")
    for row in rows:
        path = directory / str(row.get("path", ""))
        if digest(path) != row.get("sha256") or path.stat().st_size != row.get("bytes"):
            raise RuntimeError("R0.73J figure manifest hash drifted: " + str(row.get("path")))
    for row in manifest.get("inputBindings", []):
        if git_bytes(EXPERIMENT_PACKAGE_COMMIT, row["path"]) != (ROOT / row["path"]).read_bytes():
            raise RuntimeError("R0.73J figure input differs from experiment-package commit")
    for name in FIGURE_SOURCE_PATHS:
        relative = f"{FIGURE_RELATIVE}/{name}"
        if git_bytes(FIGURE_PACKAGE_COMMIT, relative) != (directory / name).read_bytes():
            raise RuntimeError("R0.73J figure source differs from figure commit: " + name)

    if tuple(path.name for path in sorted(directory.iterdir())) != tuple(sorted(FIGURE_PACKAGE_PATHS)):
        raise RuntimeError("R0.73J figure package inventory drifted")
    outputs = {row["path"]: row for row in manifest.get("figure", {}).get("outputs", [])}
    if set(outputs) != {"figure.pdf", "figure.svg", "figure.png"}:
        raise RuntimeError("R0.73J figure master inventory is not exact")
    if not (directory / "figure.pdf").read_bytes().startswith(b"%PDF"):
        raise RuntimeError("R0.73J figure PDF signature invalid")
    svg = (directory / "figure.svg").read_text(encoding="utf-8").lower()
    if "<svg" not in svg or "<image" in svg or "<text" not in svg:
        raise RuntimeError("R0.73J figure SVG is absent or rasterized")
    png = (directory / "figure.png").read_bytes()
    if not png.startswith(b"\x89PNG\r\n\x1a\n") or b"pHYs" not in png:
        raise RuntimeError("R0.73J figure PNG metadata missing")
    counts = results.get("rowCounts", {})
    decisions = results.get("decisions", {})
    if counts != {"globalContourPanels": 56, "localContourPanels": 8,
                  "overlapCells": 128, "sourceData": 192}:
        raise RuntimeError("R0.73J figure row inventory drifted")
    if not (decisions.get("globalBasePositiveOrientationWinding") == 1
            and decisions.get("localBasePositiveOrientationWinding") == 1
            and decisions.get("globalMinimum") > 5.49948
            and decisions.get("localMinimum") > 0.164355
            and decisions.get("overlapMinimum") > 0.585343):
        raise RuntimeError("R0.73J figure decisions drifted")
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
        "notes/r0-73j.html",
        "recap-r0-61-r0-73j.html",
        "research-review.html",
        "literature-review.html",
        "notes/index.html",
    ):
        path = PUBLIC / relative
        if not path.is_file() or path.is_symlink():
            raise RuntimeError("R0.73J target HTML missing: " + relative)
        value = path.read_text(encoding="utf-8")
        assert_clean(value, "R0.73J target " + relative)
        assert_mathjax_clean(value, "R0.73J target " + relative, check_naked=True)
        assert_public_voice(value, "R0.73J target " + relative)
        if "/i18n-en.js?v=1.50" not in value:
            raise RuntimeError("R0.73J target HTML has stale i18n cache: " + relative)
        target[relative] = value
    return target


def preflight_release_state() -> str:
    release = strict_json(ROOT / "research/release-manifest.json", "release manifest")
    site = strict_json(PUBLIC / "site-version.json", "site version")
    inventory = strict_json(ROOT / "research/formal-archive-inventory.json", "archive inventory")
    root_version = (ROOT / "VERSION").read_text(encoding="utf-8")

    if release.get("latestCompletedRelease") == "r073j":
        for key, value in R073J_TARGET.items():
            if release.get(key) != value:
                raise RuntimeError("R0.73J target release-manifest drifted: " + key)
        if release.get("latestReleaseGate") != "tests/r073j-continuum-branch-gate.test.mjs":
            raise RuntimeError("R0.73J target gate binding drifted")
        if release.get("latestReleasePublicationTest") != "tests/r073j-release.test.mjs":
            raise RuntimeError("R0.73J target publication-test binding drifted")
        if site != {
            "schemaVersion": "research-site-version-v1",
            "version": "1.50",
            "latestRelease": "R0.73J",
            "publicHtmlNoteCount": 186,
            "publishedDate": "2026-08-30",
        }:
            raise RuntimeError("R0.73J target site-version is not exact")
        if root_version != "1.50\n":
            raise RuntimeError("R0.73J target VERSION is not 1.50")
        state = (
            inventory.get("latestPublishedRelease"),
            inventory.get("publishedReleaseCount"),
            inventory.get("formalSealedReleaseCount"),
            inventory.get("legacyFormalFigureBacklogCount"),
        )
        if state != ("r073j", 88, 64, 24):
            raise RuntimeError("R0.73J target formal archive is not exact")

        baseline_inventory = json.loads(git_bytes(
            RELEASE_SOURCE_COMMIT, "research/formal-archive-inventory.json"
        ))
        expected_inventory = json.loads(json.dumps(baseline_inventory))
        for key in ("publishedReleases", "formalSealedReleases"):
            rows = expected_inventory.get(key)
            if not isinstance(rows, list) or rows[-1:] != ["r073i"] or "r073j" in rows:
                raise RuntimeError("R0.73J sealed baseline inventory is invalid: " + key)
            rows.append("r073j")
        expected_inventory.update({
            "latestPublishedRelease": "r073j",
            "publishedReleaseCount": 88,
            "formalSealedReleaseCount": 64,
            "legacyFormalFigureBacklogCount": 24,
        })
        if inventory != expected_inventory:
            raise RuntimeError("R0.73J target formal archive is not the exact append-only successor")
        for key, count in (("publishedReleases", 88), ("formalSealedReleases", 64)):
            rows = inventory[key]
            if len(rows) != count or len(set(rows)) != count:
                raise RuntimeError("R0.73J target archive sequence is not unique: " + key)
        if not set(inventory["formalSealedReleases"]).issubset(inventory["publishedReleases"]):
            raise RuntimeError("R0.73J sealed releases are not a subset of published releases")
        if release.get("formalArchiveInventory") != {
            "path": "research/formal-archive-inventory.json",
            "sha256": digest(ROOT / "research/formal-archive-inventory.json"),
        }:
            raise RuntimeError("R0.73J target archive-inventory binding drifted")
        if len(list((PUBLIC / "notes").glob("r0-*.html"))) != 186:
            raise RuntimeError("R0.73J target note count is not 186")

        html = _target_html()
        note = html["notes/r0-73j.html"]
        for token in (
            CLOSED, FAILURE_HISTORY, AUDIT_STATUS, OPEN, "NOT CLAY", "0.585343", "0.585009",
            "76", "83", "depth-two", "2896/2896", "0.00714950",
        ):
            if token not in note:
                raise RuntimeError("R0.73J target note lost boundary token: " + token)
        recap = html["recap-r0-61-r0-73j.html"]
        start = recap.find('<section id="node-index">')
        end = recap.find("</section>", start)
        if start < 0 or end <= start:
            raise RuntimeError("R0.73J target recap node index is absent")
        links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', recap[start:end])
        if len(links) != 126 or len(set(links)) != 126:
            raise RuntimeError("R0.73J target recap is not 126 unique nodes")
        if recap.count('<article class="phase">') != 45:
            raise RuntimeError("R0.73J target recap is not 45 phases")
        for token in (
            "88</strong><span>R0.70A–R0.73J 已公开版本",
            "64</strong><span>当前 formal-figure 合同下完整封存",
            "24</strong><span>旧版附图档案待回补",
        ):
            if token not in recap:
                raise RuntimeError("R0.73J target recap accounting drifted")
        home = html["research-review.html"]
        route = re.search(
            r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73J">(.*?)</nav>',
            home, flags=re.S,
        )
        route_links = [] if route is None else re.findall(
            r'href="/notes/(r0-[^"]+)\.html"', route.group(1)
        )
        if len(route_links) != 96 or len(set(route_links)) != 96:
            raise RuntimeError("R0.73J target home route is not 96 unique links")
        if home.count('data-release="r073j"') != 1 or "/notes/r0-73j.html" not in home:
            raise RuntimeError("R0.73J target home card is absent")
        literature = html["literature-review.html"]
        if (
            'id="r073j-boundary"' not in literature
            or 'class="route-r073j-deck-update"' not in literature
            or "2896/2896" not in literature
        ):
            raise RuntimeError("R0.73J target literature boundary is absent")
        if 'data-note="r0-73j"' not in html["notes/index.html"]:
            raise RuntimeError("R0.73J target note-index entry is absent")
        return "target"

    if any(release.get(key) != value for key, value in R073I_BASELINE.items()):
        raise RuntimeError("R0.73J release state is neither exact R0.73I source nor exact R0.73J target")
    if site != {
        "schemaVersion": "research-site-version-v1",
        "version": "1.49",
        "latestRelease": "R0.73I",
        "publicHtmlNoteCount": 185,
        "publishedDate": "2026-08-30",
    }:
        raise RuntimeError("R0.73J site-version baseline is not exact")
    if root_version != "1.49\n":
        raise RuntimeError("R0.73J VERSION baseline is not 1.49")
    state = (
        inventory.get("latestPublishedRelease"), inventory.get("publishedReleaseCount"),
        inventory.get("formalSealedReleaseCount"), inventory.get("legacyFormalFigureBacklogCount"),
    )
    if state != ("r073i", 87, 63, 24):
        raise RuntimeError("R0.73J formal archive baseline is not exact")
    if len(list((PUBLIC / "notes").glob("r0-*.html"))) != 185:
        raise RuntimeError("R0.73J expected exactly 185 baseline HTML notes")
    for path in (
        PUBLIC / "notes/r0-73j.html",
        PUBLIC / "notes/r0-73j.pdf",
        PUBLIC / "recap-r0-61-r0-73j.html",
        PUBLIC / "recap-r0-61-r0-73j.pdf",
        PUBLIC / "assets/r073j",
        PUBLIC / FIGURE_RELATIVE,
    ):
        if path.exists() or path.is_symlink():
            raise RuntimeError("R0.73J baseline path already exists: " + str(path))
    for relative, tokens in {
        "research-review.html": ("R0.73I", "185", "R0.73J"),
        "literature-review.html": ("R0.73I", "开放接口 · R0.73J"),
        "notes/index.html": ("R0.73I", "185 篇公开研究笔记"),
        "recap-r0-61-r0-73i.html": ("R0.61–R0.73I", "125", "44 个研究阶段"),
    }.items():
        value = (PUBLIC / relative).read_text(encoding="utf-8")
        for token in tokens:
            if token not in value:
                raise RuntimeError(f"R0.73J baseline {relative} missing {token}")
    return "source"


def build_note() -> str:
    html = (PUBLIC / "notes/r0-73i.html").read_text(encoding="utf-8")
    metadata = (
        ("description", r'<meta name="description" content=".*?">',
         '<meta name="description" content="研究笔记 R0.73J：周期 Rayleigh 唯一简单最右谱支、统一谱隙、重叠和相位锚在连续算子层面闭合。">'),
        ("og title", r'<meta property="og:title" content=".*?">',
         '<meta property="og:title" content="R0.73J｜Periodic Rayleigh continuum-operator spectral-branch certificate">'),
        ("og description", r'<meta property="og:description" content=".*?">',
         '<meta property="og:description" content="A unique algebraically simple rightmost spectral branch of the continuum operator is certified, with an explicit gap, overlap, phase anchor, and audit boundary.">'),
        ("og image", r'<meta property="og:image" content=".*?">',
         f'<meta property="og:image" content="https://kasifa.github.io/assets/r073j/{FIGURE_ID}.png">'),
        ("title", r'<title>.*?</title>',
         '<title>R0.73J｜Periodic Rayleigh continuum-operator spectral-branch certificate</title>'),
    )
    for label, pattern, value in metadata:
        html = section(html, pattern, value, "H note " + label)
    html = required(html, "/i18n-en.js?v=1.49", "/i18n-en.js?v=1.50", "H note i18n")
    toc_items = (
        ("result", "00 · direct result"), ("bridge", "01 · analytic bridge"),
        ("contours", "02 · contour certificate"), ("overlap", "03 · overlap and phase"),
        ("independence", "04 · audit boundary"), ("natural", "05 · natural-box audit"),
        ("failures", "06 · failed methods"), ("figure", "07 · journal figure"),
        ("boundary", "08 · exact boundary"), ("literature", "09 · literature boundary"),
        ("value", "10 · value"), ("next", "11 · R0.73K"),
        ("reproduce", "12 · reproduction"),
    )
    nav = "<nav>" + "".join(
        f'<a href="#{anchor}">{label.split(" · ", 1)[1]}</a>'
        for anchor, label in toc_items
    ) + '<a href="/">返回主页</a></nav>'
    html = section(html, r'<nav><a href="#result">.*?</nav>', nav, "H note nav")
    html = section(html, r'    <header class="hero">.*?</header>', NOTE_HERO, "H note hero")
    toc = (
        '      <aside class="toc"><strong>CONTENTS</strong><ol>\n'
        + "".join(f'        <li><a href="#{anchor}">{label}</a></li>' for anchor, label in toc_items)
        + "\n      </ol></aside>"
    )
    html = section(html, r'      <aside class="toc">.*?</aside>', toc, "H note toc")
    html = section(html, r'      <article>.*?</article>', NOTE_ARTICLE, "H note article")
    footer = (
        "<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>"
        "我按原编号记录定理、有限计算、反例和未解决的问题。</div>"
        '<div>研究笔记 R0.73J · 2026-08-30<br><a href="/">返回研究主页</a></div></footer>'
    )
    html = section(html, r"<footer>.*?</footer>", footer, "H note footer")
    match = re.search(r"<nav>(.*?)</nav>", html, flags=re.S)
    anchors = re.findall(r'href="#([^"]+)"', match.group(1)) if match else []
    expected = [anchor for anchor, _ in toc_items]
    if anchors != expected or len(anchors) != len(set(anchors)):
        raise RuntimeError("R0.73J note nav anchors are not unique and ordered")
    assert_clean(html, "R0.73J note")
    assert_mathjax_clean(html, "R0.73J note", check_naked=True)
    assert_public_voice(html, "R0.73J note")
    return html


def build_recap() -> str:
    html = (PUBLIC / "recap-r0-61-r0-73i.html").read_text(encoding="utf-8")
    metadata = (
        ("description", r'<meta name="description" content=".*?">',
         '<meta name="description" content="R0.60 之后的完整研究回顾：R0.61 到 R0.73J 共 126 个节点；最新一节认证周期 Rayleigh 连续算子上的唯一简单最右谱支。">'),
        ("og title", r'<meta property="og:title" content=".*?">',
         '<meta property="og:title" content="R0.61–R0.73J｜R0.60 之后的研究回顾">'),
        ("og description", r'<meta property="og:description" content=".*?">',
         '<meta property="og:description" content="45 个阶段、126 个节点：从约化递推和环带排除到周期 Rayleigh 连续算子谱支认证。">'),
        ("title", r"<title>.*?</title>",
         "<title>R0.61–R0.73J｜R0.60 之后的研究回顾</title>"),
    )
    for label, pattern, value in metadata:
        html = section(html, pattern, value, "H recap " + label)
    html = required(html, "/i18n-en.js?v=1.49", "/i18n-en.js?v=1.50", "H recap i18n")
    hero = r'''    <header class="hero"><div class="hero-inner"><div><div class="eyebrow">累计回顾 · R0.61–R0.73J · 2026-08-30</div><h1>R0.60 之后的研究回顾</h1><p class="lead">这页保留 R0.61 到 R0.73J 的全部 126 个节点。R0.61–R0.69W 从约化递推走到严格环带排除；R0.70A–R0.71Z 检查移动尺度、临界账本、内部 entry 与 complete-root 边界；R0.72A–R0.73B 处理 strong coupling、critical log、碰撞几何与完整线性 Fourier--Leray 行；R0.73C–I 依次认证冻结 Rayleigh 不稳定、黏性谱簇持续、固定正半平面传递、移动剖面增益、非线性相对放大、平面固定距离偏离以及零窗口作用量边界。R0.73J 在连续算子层面认证唯一简单最右谱支、显式谱隙、左右重叠和相位锚。自然盒首轮和 depth-two wrapping 历史保留；自适应 depth five 最终覆盖 83/83 个选定盒。黏性延拓、非自伴绝热、固定背景、横向三维、奇性与 Clay 没有被外推。</p></div><div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.73J</strong><p>收录节点：126</p><p>回顾截止时公开笔记：186</p><p>回顾截止节点：R0.73J</p><p>问题状态：仍未解决</p></div></div></header>'''
    html = section(html, r'    <header class="hero">.*?</header>', hero, "H recap hero")
    for old, new in (
        ("02 · 125 节完整索引", "02 · 126 节完整索引"),
        ("01 · 44 个研究阶段", "01 · 45 个研究阶段"),
        ("R0.60 之后的路线分成 44 个阶段", "R0.60 之后的路线分成 45 个阶段"),
        ('data-current-route="R0.69P–R0.73I"', 'data-current-route="R0.69P–R0.73J"'),
    ):
        html = required(html, old, new, "H recap counter")
    result = r'''        <section id="result"><div class="section-no">00 / 回顾范围</div><h2>版本数、封存数和数学结论分开报告</h2><div class="metrics"><div class="metric"><strong>126</strong><span>R0.61–R0.73J 研究节点</span></div><div class="metric"><strong>88</strong><span>R0.70A–R0.73J 已公开版本</span></div><div class="metric"><strong>64</strong><span>当前 formal-figure 合同下完整封存</span></div><div class="metric"><strong>24</strong><span>旧版附图档案待回补</span></div></div><p>R0.00–R0.60 保留在上一份阶段回顾。R0.70A–R0.73J 的 88 个版本已经公开，其中 64 个满足当前完整封存合同，24 个历史版本仍欠 formal-figure 回补。公开和封存不表示 Clay 问题已经解决。</p></section>'''
    html = section(html, r'        <section id="result">.*?</section>', result, "H recap result")
    phase = r'''            <article class="phase"><h3>R0.73J · Periodic Rayleigh continuum-operator spectral-branch certificate</h3><p>连续算子上存在唯一实、代数简单的最右谱支 \(\lambda_0(d)\in(0.167,0.173)\)。其余谱点实部不超过 \(0.11\)，严格谱隙大于 \(0.057\)，可取 \(g_*=1/20\)。主证书给出重叠 \(>0.585343\)、共享对应冻结网格的第二后处理 \(>0.585009\)、相位锚 \(>1.84154\)，全局与局部围道下界分别 \(>5.49948\)、\(>0.164355\)，绕数均为 1。</p><p>自然盒首轮 76/83 通过，depth-two 仅解析 1/7 个原失败父盒。自适应推进到 depth five 后，7/7 父盒、83/83 个选定盒与 2896/2896 最终叶盒全部通过，最小 Evans 下界 \(>0.00714950\)。它仍是辅助抽样；独立 overlap raw-ODE 三盒尚未运行。有限 Galerkin 诊断中实部约 \(0.04\) 的较弱不稳定共轭对不承担连续算子存在性或重数证明权重，也不与只计数 \(\operatorname{Re}\lambda>0.11\) 区域的唯一性结论冲突。</p><p>__CLOSED__。__FAILURE_HISTORY__。__AUDIT_STATUS__。__OPEN__。NOT CLAY。</p><div class="links"><a href="/notes/r0-73j.html">R0.73J</a><a href="/assets/r073j/__FIGURE_ID__.pdf">R0.73J 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/experiments/r073j">R0.73J 实验包</a></div></article>
'''.replace("__CLOSED__", CLOSED).replace("__FAILURE_HISTORY__", FAILURE_HISTORY).replace("__AUDIT_STATUS__", AUDIT_STATUS).replace("__OPEN__", OPEN).replace("__FIGURE_ID__", FIGURE_ID)
    marker = '          </div>\n        </section>\n\n        <section id="node-index">'
    html = once(html, marker, phase + marker, "H recap phase")
    html = required(html, "R0.61–R0.73I 的 125 节公开笔记", "R0.61–R0.73J 的 126 节公开笔记", "H recap node title")
    node_h = '            <span class="node-ref"><a href="/notes/r0-73i.html">R0.73I</a><span class="node-state kind-closed">闭</span></span>\n'
    node_i = '            <span class="node-ref"><a href="/notes/r0-73j.html">R0.73J</a><span class="node-state kind-closed">闭</span></span>\n'
    html = once(html, node_h, node_h + node_i, "H recap node")
    retained = '            <li>R0.73J 闭合周期 Rayleigh 连续算子上的唯一简单最右谱支、显式谱隙、左右重叠与固定相位锚；黏性延拓、非自伴绝热、横向三维、奇性与 Clay 保持 OPEN。</li>\n'
    html = once(html, "          </ul>\n          <p>这些结果可以分别整理成", retained + "          </ul>\n          <p>这些结果可以分别整理成", "H recap retained")
    value = r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>固定正窗口的谱支选择门槛已经闭合</h2><p>不能把 126 个节点或 88 个公开版本解释成 Clay 完成比例。R0.73J 的严格增量是连续算子上的唯一简单最右谱支、统一谱隙、左右重叠和相位锚；黏性谱支延拓、补空间控制和非自伴绝热余项仍未证明。</p></section>'''
    html = section(html, r'        <section id="value">.*?</section>', value, "H recap value")
    next_gate = r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.73K 检查黏性谱支与统一投影控制</h2><p>下一节处理小黏性扰动下的唯一谱支、Riesz 投影和补空间半群界；随后才进入非自伴绝热余项。</p></section>'''
    html = section(html, r'        <section id="next">.*?</section>', next_gate, "H recap next")
    claims = r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>定理、计算审计、失败历史和开放问题分开列示</h2><p>R0.70A–R0.73J 的 88 节已公开；64 节完整封存；24 节旧档待回补。</p><p>__CLOSED__。</p><p>__FAILURE_HISTORY__。</p><p>__AUDIT_STATUS__。</p><p>__OPEN__。</p><p>自然盒最终通过不改变各项第二实现共用对应冻结原始网格的独立性限定，也不补上尚未运行的 overlap raw-ODE 三盒。</p></section>'''
    claims = claims.replace("__CLOSED__", CLOSED).replace("__FAILURE_HISTORY__", FAILURE_HISTORY).replace("__AUDIT_STATUS__", AUDIT_STATUS).replace("__OPEN__", OPEN)
    html = section(html, r'        <section id="claims">.*?</section>', claims, "H recap claims")
    reproduce = r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、定理、证明、审计、实验、附图和历史回顾</h2><p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-73i.html">保留 R0.73I 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-73j.html">打开最新节点 R0.73J</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073j_continuum_branch_theorem.md">查看定理</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073j_analytic_proof.md">查看解析证明</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073j_adversarial_audit.md">查看证据审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/experiments/r073j">查看正式实验包</a> · <a href="/assets/r073j/__FIGURE_ID__.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-73j.pdf">下载同步 PDF</a></p><p>围道证书承担完整参数一致证明；自然盒是算法不同的辅助抽样复核。</p></section>'''.replace("__FIGURE_ID__", FIGURE_ID)
    html = section(html, r'        <section id="reproduce">.*?</section>', reproduce, "H recap reproduce")
    footer = '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>我按原编号记录定理、有限计算、反例和未解决的问题。</div><div>R0.61–R0.73J 回顾 · 2026-08-30<br><a href="/">返回研究主页</a></div></footer>'
    html = section(html, r"<footer>.*?</footer>", footer, "H recap footer")
    start = html.index('<section id="node-index">')
    end = html.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', html[start:end])
    if len(links) != 126 or len(set(links)) != 126:
        raise RuntimeError("R0.73J recap expected 126 unique nodes")
    if html.count('<article class="phase">') != 45:
        raise RuntimeError("R0.73J recap expected 45 phases")
    if "R0.60 之后的研究回顾" not in html or ">R0.61<" not in html:
        raise RuntimeError("R0.73J recap must start after R0.60, at R0.61")
    assert_clean(html, "R0.73J recap")
    assert_mathjax_clean(html, "R0.73J recap", check_naked=True)
    assert_public_voice(html, "R0.73J recap")
    return html


def update_home() -> str:
    html = (PUBLIC / "research-review.html").read_text(encoding="utf-8")
    html = section(
        html,
        r'    <section class="route-overview latest-release-spotlight".*?</section>',
        HOME_LATEST_SPOTLIGHT,
        "H home latest spotlight",
    )
    for old, new in (
        ('data-site-version="1.49"', 'data-site-version="1.50"'),
        ("/i18n-en.js?v=1.49", "/i18n-en.js?v=1.50"),
        ("/site-refresh.js?v=1.49", "/site-refresh.js?v=1.50"),
        ("<strong>v1.49</strong>网页版本", "<strong>v1.50</strong>网页版本"),
        ("<strong>185</strong>公开研究笔记", "<strong>186</strong>公开研究笔记"),
        ("<strong>R0.73I</strong>最新研究节点", "<strong>R0.73J</strong>最新研究节点"),
        ('<a class="route-map-latest" href="#r073i">跳到首页 R0.73I 卡片 →</a>',
         '<a class="route-map-latest" href="#r073j">跳到首页 R0.73J 卡片 →</a>'),
        ("rightmost continuum branch / fixed-window action",
         "viscous branch / uniform projection control"),
        ("Research topology · R0.1–R0.73I", "Research topology · R0.1–R0.73J"),
        ("R0.70A–R0.73I：87 节已公开，63 节完整封存",
         "R0.70A–R0.73J：88 节已公开，64 节完整封存"),
        ('<span class="route-range">R0.69P–R0.73I</span>',
         '<span class="route-range">R0.69P–R0.73J</span>'),
        ('aria-label="R0.69P–R0.73I"', 'aria-label="R0.69P–R0.73J"'),
        ("展开 95 篇公开笔记", "展开 96 篇公开笔记"),
        ("本站 R0.69P–R0.73I 路线", "本站 R0.69P–R0.73J 路线"),
        ("综述 v1.49 · 2026-08-30", "综述 v1.50 · 2026-08-30"),
        ("上次综述 v1.48 · 2026-08-30", "上次综述 v1.49 · 2026-08-30"),
    ):
        html = required(html, old, new, "H home " + old)
    html = replace_all(
        html, "/recap-r0-61-r0-73i.html", "/recap-r0-61-r0-73j.html",
        "H home recap HTML links",
    )
    html = replace_all(
        html, "/recap-r0-61-r0-73i.pdf", "/recap-r0-61-r0-73j.pdf",
        "H home recap PDF links",
    )
    historical = (r'<strong style="color:var(--gold)">下一步 R0.73J：</strong>&nbsp;'
                  r'认证唯一简单右端谱支及其显式正窗口。')
    html = required(
        html, historical, historical.replace("下一步", "当时的下一步"),
        "H home historical next",
    )
    focus = r'<div class="summary-item"><strong>我目前关注</strong><span>R0.73J 已认证周期 Rayleigh 连续算子上的唯一简单最右谱支、显式谱隙、左右重叠和固定相位锚。自然盒自适应 depth five 已覆盖 83/83 个选定盒；下一关是黏性谱支与统一投影控制。</span></div>'
    html = section(
        html,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        focus,
        "H home focus",
    )
    html = required(
        html,
        "<h3>R0.73I：端点校正、连续体上作用量与零窗口切向速率已闭合</h3>",
        "<h3>R0.73J：周期 Rayleigh 连续算子上的唯一简单最右谱支已认证</h3>",
        "H home current title",
    )
    html = required(
        html, "<span>R0.72R–R0.73I：</span>", "<span>R0.72R–R0.73J：</span>",
        "H home path range",
    )
    html = required(
        html,
        "endpoint audit / continuum upper action / zero-window tangent</p>",
        "endpoint audit / continuum upper action / zero-window tangent → unique simple rightmost spectral branch of the continuum operator</p>",
        "H home path tail",
    )
    link_h = '<a class="milestone" href="/notes/r0-73i.html">R0.73I</a>'
    html = once(
        html, link_h,
        link_h + '\n                  <a class="milestone" href="/notes/r0-73j.html">R0.73J</a>',
        "H home route link",
    )
    route_h = r'''              <p>R0.73I 证明继承端点严格小于 \(1/450\)，给完整移动传播子一个连续体上作用量，并证明完整顶谱块最小、最大增益共享零窗口切向速率。两个精确反例只否定由现有输入推出固定窗口作用量和有界前因子；有限 action/WKB 数据不承担连续体定理。</p>
'''
    route_i = r'''              <p>R0.73J 认证周期 Rayleigh 连续算子上的唯一简单最右谱支 \(\lambda_0(d)\in(0.167,0.173)\)、严格谱隙 \(>0.057\)、左右重叠和固定相位锚。自然盒首轮 76/83、depth-two 1/7 的 wrapping 历史保留；自适应 depth five 最终覆盖 83/83 个选定盒。</p>
'''
    html = once(html, route_h, route_h + route_i, "H home current route summary")
    html = section(
        html, r'            <article class="tree-node next">.*?</article>',
        HOME_NEXT, "H home next gate",
    )
    recap = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem"><p class="eyebrow">累计回顾 R0.61–R0.73J · 2026-08-30</p><h3>R0.60 recap 之后的累计回顾收录 126 个节点；全站现有 186 篇公开研究笔记</h3><p>累计回顾现分 45 个阶段，完整保留 R0.61–R0.73J；最新节点分开记录连续算子定理、完整围道证书、共享网格审计边界、自然盒深审计和开放门。</p><p>R0.70A–R0.73J 共 88 个版本已公开；64 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p><p><strong>阶段判断：</strong>&nbsp;唯一简单最右谱支、显式谱隙、左右重叠与固定相位锚已闭合；黏性谱支、非自伴绝热、固定背景、横向三维、奇性与 Clay 保持 OPEN。</p><p><a href="/recap-r0-61-r0-73j.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-73j.pdf">下载同步 PDF</a></p></div>'''
    html = section(
        html, r'          <div class="task-one" id="post-r060-recap".*?</div>',
        recap, "H home recap",
    )
    marker = '          </div>\n        </section>\n\n      </article>'
    html = once(
        html, marker,
        '          </div>\n\n' + HOME_I_CARD + '\n        </section>\n\n      </article>',
        "H home card",
    )
    if html.count('data-release="r073j"') != 1:
        raise RuntimeError("home must contain exactly one R0.73J card")
    if html.count('<strong style="color:var(--gold)">下一步 R0.73K：') != 1:
        raise RuntimeError("home must contain exactly one current R0.73K gate")
    route = re.search(
        r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73J">(.*?)</nav>',
        html, flags=re.S,
    )
    links = [] if route is None else re.findall(
        r'href="/notes/r0-[^"]+\.html"', route.group(1)
    )
    if len(links) != 96 or len(set(links)) != 96:
        raise RuntimeError("home current-route index must contain 96 unique note links")
    assert_clean(html, "R0.73J home")
    assert_mathjax_clean(html, "R0.73J home", check_naked=True)
    assert_public_voice(html, "R0.73J home")
    return html


def update_literature() -> str:
    html = (PUBLIC / "literature-review.html").read_text(encoding="utf-8")
    for old, new in (
        ("/i18n-en.js?v=1.49", "/i18n-en.js?v=1.50"),
        ("本站 R0.69P–R0.73I 只列为研究笔记",
         "本站 R0.69P–R0.73J 只列为研究笔记"),
        ("文献综述 v1.49 · 2026-08-30", "文献综述 v1.50 · 2026-08-30"),
        ("累计回顾与 125 节索引", "累计回顾与 126 节索引"),
        ("打开 125 节完整索引", "打开 126 节完整索引"),
    ):
        html = required(html, old, new, "H literature " + old)
    html = replace_all(
        html, "/recap-r0-61-r0-73i.html", "/recap-r0-61-r0-73j.html",
        "H literature recap links",
    )
    deck_h = r'''<span class="route-r073i-deck-update">R0.73I 校正继承端点，给出连续体上作用量和零窗口切向速率；固定正窗口 matching action、有界前因子与连续体两项式仍为 OPEN。三个 \(N=48\) action/WKB 窗口只作有限诊断。</span></p>'''
    deck_i = deck_h[:-4] + r'''<span class="route-r073j-deck-update">R0.73J 在连续算子层面认证周期 Rayleigh 唯一简单最右谱支、显式谱隙、左右重叠和固定相位锚。自然盒首轮 76/83、depth-two 1/7 的失败历史保留；自适应 depth five 最终覆盖 83/83 个选定盒与 2896/2896 个叶盒。</span></p>'''
    html = required(html, deck_h, deck_i, "H literature route deck I endpoint")
    old_open = r'''<div class="route-step pause"><header><b>开放接口 · R0.73J</b><strong>unique simple rightmost continuum branch</strong></header><p>在显式正窗口上计数 Rayleigh/Evans 零点、证明简单性并排除更右谱点；随后再处理黏性谱支与非自伴绝热余项。</p></div>'''
    new_steps = r'''<div class="route-step kept"><header><b>R0.73J</b><strong>periodic Rayleigh continuum-operator spectral-branch certificate</strong></header><p>唯一简单最右谱支、显式谱隙、左右重叠和固定相位锚已经闭合。各项第二实现共用对应冻结原始网格和独立 overlap raw-ODE 三盒的边界保持明确。<a href="/notes/r0-73j.html">研究笔记</a> <a href="/recap-r0-61-r0-73j.html">当前累计回顾</a> <a href="#r073j-boundary">文献边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.73K</b><strong>viscous branch and uniform projection control</strong></header><p>检查小黏性扰动下的唯一谱支、Riesz 投影和补空间半群界；随后再处理非自伴绝热余项。</p></div>'''
    html = once(html, old_open, new_steps, "H literature route")
    boundary = r'''

          <h3 id="r073j-boundary">R0.73J 的周期 Rayleigh--Evans 文献边界</h3>
          <p>主文献审计区分<a href="#ref-146">周期 Evans 零点阶数与代数重数</a>、<a href="#ref-149">验证围道计算</a>、<a href="#ref-150">Chebyshev 参数插值</a>、<a href="#ref-155">Howard 包络</a>和<a href="#ref-151">退化临界层</a>。<a href="#ref-153">解析插值余项</a>、<a href="#ref-152">抽象 Hamiltonian index 路线</a>与<a href="#ref-154">标准 Euler 应用的有界权重限制</a>也单独核对。现有文献提供方法先例，但不直接给出这里的特定算子、完整参数窗、统一重叠或相位锚证书。</p>
          <p>主围道证书覆盖全部参数边界；围道的 range/winding 与重叠的 center--Lipschitz 第二实现各自共用对应的冻结原始 ODE 网格，均未独立重算 raw ODE。自然盒 raw-ODE 抽样在自适应 depth five 后覆盖 83/83 个选定盒与 2896/2896 个最终叶盒，最小 Evans 下界大于 \(0.00714950\)；独立 overlap raw-ODE 三盒仍未运行。</p>
          <div class="boundary"><strong>R0.73J 的主张边界</strong><p>__CLOSED__。</p><p>__FAILURE_HISTORY__。</p><p>__AUDIT_STATUS__。</p><p>__OPEN__。</p><p>这是连续算子谱支认证，不是黏性谱支、非自伴绝热余项、三维闭合或 Clay 证明。NOT CLAY。</p></div>'''
    boundary = boundary.replace("__CLOSED__", CLOSED).replace("__FAILURE_HISTORY__", FAILURE_HISTORY).replace("__AUDIT_STATUS__", AUDIT_STATUS).replace("__OPEN__", OPEN)
    match = re.search(
        r'(<h3 id="r073i-boundary">.*?<div class="boundary">.*?</div>)',
        html, flags=re.S,
    )
    if match is None:
        raise RuntimeError("H literature expected R0.73I boundary")
    html = once(
        html, match.group(1), match.group(1) + boundary,
        "H literature boundary",
    )
    references = r'''            <li id="ref-146">K. Zumbrun. <a href="https://doi.org/10.4171/ZAA/1469"><em>2-Modified Characteristic Fredholm Determinants, Hill's Method, and the Periodic Evans Function of Gardner</em></a>. Z. Anal. Anwend. 31 (2012), 463--472.</li>
            <li id="ref-147">M. A. Johnson and K. Zumbrun. <a href="https://doi.org/10.1137/100809349"><em>Convergence of Hill's Method for Nonselfadjoint Operators</em></a>. SIAM J. Numer. Anal. 50 (2012), 64--78.</li>
            <li id="ref-148">H. R. Dullin and R. Marangell. <a href="https://doi.org/10.1016/j.physd.2023.133954"><em>An Evans function for the linearised 2D Euler equations using Hill's determinant</em></a>. Physica D 457 (2024), 133954.</li>
            <li id="ref-149">B. Barker and K. Zumbrun. <a href="https://doi.org/10.1142/S0218202516500585"><em>Numerical proof of stability of viscous shock profiles</em></a>. Math. Models Methods Appl. Sci. 26 (2016), 2451--2469.</li>
            <li id="ref-150">K. Xu. <a href="https://doi.org/10.1016/j.apnum.2015.12.002"><em>The Chebyshev points of the first kind</em></a>. Applied Numerical Mathematics 102 (2016), 17--30.</li>
            <li id="ref-151">D. Bian and E. Grenier. <a href="https://arxiv.org/abs/2408.00977"><em>Singularities of Rayleigh equation</em></a>. Preprint (2024).</li>
            <li id="ref-152">Z. Lin and C. Zeng. <a href="https://arxiv.org/abs/1703.04016"><em>Instability, index theorem, and exponential trichotomy for Linear Hamiltonian PDEs</em></a>. Preprint revision (2021).</li>
            <li id="ref-153">L. N. Trefethen. <a href="https://people.maths.ox.ac.uk/trefethen/trefethen_sample.pdf"><em>Approximation Theory and Approximation Practice</em></a>. SIAM (2013), Theorem 8.1.</li>
            <li id="ref-154">Z. Lin. <a href="https://doi.org/10.1137/S0036141002406266"><em>Instability of Some Ideal Plane Flows</em></a>. SIAM J. Math. Anal. 35 (2003), 318--356.</li>
            <li id="ref-155">L. N. Howard. <a href="https://www.math.fsu.edu/~moore/SeminarFiles/Howard61.pdf"><em>Note on a paper of John W. Miles</em></a>. J. Fluid Mech. 10 (1961), 509--512.</li>
'''
    html = once(
        html, '          </ol>\n          <p class="source-note">',
        references + '          </ol>\n          <p class="source-note">',
        "H literature references",
    )
    ids = re.findall(r'\bid="([^"]+)"', html)
    if len(ids) != len(set(ids)):
        duplicates = sorted({value for value in ids if ids.count(value) > 1})
        raise RuntimeError("R0.73J literature duplicate HTML ids: " + ", ".join(duplicates))
    for number in range(146, 156):
        if ids.count(f"ref-{number}") != 1:
            raise RuntimeError(f"R0.73J literature reference ref-{number} is not unique")
    assert_clean(html, "R0.73J literature")
    assert_mathjax_clean(html, "R0.73J literature", check_naked=True)
    assert_public_voice(html, "R0.73J literature")
    return html


def build_manifest_outputs() -> dict[Path, bytes]:
    release_path = ROOT / "research/release-manifest.json"
    release = strict_json(release_path, "release manifest")
    for key, value in R073I_BASELINE.items():
        if release.get(key) != value:
            raise RuntimeError("release manifest changed during R0.73J generation: " + key)
    release.update({
        **R073J_TARGET,
        "latestReleaseGate": "tests/r073j-continuum-branch-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r073j-release.test.mjs",
    })
    release.pop("nextReleaseSourceStage", None)

    site_path = PUBLIC / "site-version.json"
    site = strict_json(site_path, "site version")
    if site != {
        "schemaVersion": "research-site-version-v1",
        "version": "1.49",
        "latestRelease": "R0.73I",
        "publicHtmlNoteCount": 185,
        "publishedDate": "2026-08-30",
    }:
        raise RuntimeError("site-version changed during R0.73J generation")
    site.update({
        "version": "1.50",
        "latestRelease": "R0.73J",
        "publicHtmlNoteCount": 186,
        "publishedDate": "2026-08-30",
    })

    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = strict_json(inventory_path, "formal archive inventory")
    state = (
        inventory.get("latestPublishedRelease"), inventory.get("publishedReleaseCount"),
        inventory.get("formalSealedReleaseCount"), inventory.get("legacyFormalFigureBacklogCount"),
    )
    if state != ("r073i", 87, 63, 24):
        raise RuntimeError("formal archive changed during R0.73J generation")
    for key in ("publishedReleases", "formalSealedReleases"):
        rows = inventory.get(key)
        if not isinstance(rows, list) or rows[-1:] != ["r073i"] or "r073j" in rows:
            raise RuntimeError("formal archive is not append-only: " + key)
        rows.append("r073j")
    inventory.update({
        "latestPublishedRelease": "r073j",
        "publishedReleaseCount": 88,
        "formalSealedReleaseCount": 64,
        "legacyFormalFigureBacklogCount": 24,
    })
    if (
        len(inventory["publishedReleases"]) != 88
        or len(set(inventory["publishedReleases"])) != 88
        or len(inventory["formalSealedReleases"]) != 64
        or len(set(inventory["formalSealedReleases"])) != 64
    ):
        raise RuntimeError("formal archive count or uniqueness mismatch after R0.73J")
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
        ROOT / "VERSION": b"1.50\n",
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
        note_index.ROOT = ROOT
        note_index.PUBLIC = PUBLIC
        note_index.NOTES = PUBLIC / "notes"
        note_index.OUTPUT = note_index.NOTES / "index.html"
        existing = [note_index.parse_note(path) for path in note_index.note_files()]
        if len(existing) != 185 or any(note.slug == "r0-73j" for note in existing):
            raise RuntimeError("R0.73J note-index baseline is not exact")
        latest = note_index.Note(
            slug="r0-73j", code="R0.73J",
            title="Periodic Rayleigh continuum-operator spectral-branch certificate",
            major=73, has_pdf=True,
        )
        note_index.json = TargetJson
        note_index.latest_recap_href = lambda: "/recap-r0-61-r0-73j.html"
        index = note_index.render([latest] + existing)
    finally:
        note_index.json = old_json
        note_index.latest_recap_href = old_latest_recap_href
        note_index.ROOT, note_index.PUBLIC, note_index.NOTES, note_index.OUTPUT = old_paths
    for token in (
        'data-site-version="1.50"',
        "186 篇公开研究笔记",
        "<strong>R0.73J</strong><span>最新研究节点</span>",
        'data-note="r0-73j"',
        "/recap-r0-61-r0-73j.html",
        "研究笔记总索引 · v1.50 · 2026-08-30",
    ):
        if token not in index:
            raise RuntimeError("R0.73J note index missing token: " + token)
    assert_clean(index, "R0.73J note index")
    assert_mathjax_clean(index, "R0.73J note index", check_naked=True)
    assert_public_voice(index, "R0.73J note index")
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
    web_target = PUBLIC / "assets/r073j"
    for suffix in ("pdf", "svg", "png"):
        name = f"figure.{suffix}"
        row = by_name.get(name)
        payload = (source / name).read_bytes()
        if (
            row is None
            or sha256_bytes(payload) != row.get("sha256")
            or len(payload) != row.get("bytes")
        ):
            raise RuntimeError("R0.73J public figure master is not manifest-bound: " + name)
        staged[web_target / f"{FIGURE_ID}.{suffix}"] = payload


def validate_staged(staged: dict[Path, bytes]) -> None:
    required_paths = (
        PUBLIC / "notes/r0-73j.html",
        PUBLIC / "recap-r0-61-r0-73j.html",
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
            raise RuntimeError("R0.73J transaction missing staged path " + str(path))
    for name in FIGURE_PACKAGE_PATHS:
        if PUBLIC / FIGURE_RELATIVE / name not in staged:
            raise RuntimeError("R0.73J transaction omitted figure-package asset " + name)
    for suffix in ("pdf", "svg", "png"):
        if PUBLIC / f"assets/r073j/{FIGURE_ID}.{suffix}" not in staged:
            raise RuntimeError("R0.73J transaction omitted web figure master " + suffix)
    for path in staged:
        if path.suffix.lower() == ".pdf" and (
            "assets/r073j" not in path.as_posix()
            and FIGURE_RELATIVE not in path.as_posix()
        ):
            raise RuntimeError("R0.73J HTML transaction must not generate note or recap PDFs")

    html_paths = (
        PUBLIC / "notes/r0-73j.html",
        PUBLIC / "recap-r0-61-r0-73j.html",
        PUBLIC / "research-review.html",
        PUBLIC / "literature-review.html",
        PUBLIC / "notes/index.html",
    )
    for path in html_paths:
        value = staged[path].decode("utf-8")
        assert_clean(value, path.name)
        assert_mathjax_clean(value, path.name, check_naked=True)
        assert_public_voice(value, path.name)
        if "/i18n-en.js?v=1.50" not in value:
            raise RuntimeError("R0.73J staged HTML has stale i18n version: " + path.name)
    note = staged[PUBLIC / "notes/r0-73j.html"].decode("utf-8")
    for token in (
        CLOSED, FAILURE_HISTORY, AUDIT_STATUS, OPEN, "NOT CLAY", "0.585343", "0.585009",
        "76", "83", "depth-two", "2896/2896", "0.00714950",
    ):
        if token not in note:
            raise RuntimeError("R0.73J staged note lost boundary token: " + token)
    recap = staged[PUBLIC / "recap-r0-61-r0-73j.html"].decode("utf-8")
    start = recap.index('<section id="node-index">')
    end = recap.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', recap[start:end])
    if (
        len(links) != 126
        or len(set(links)) != 126
        or recap.count('<article class="phase">') != 45
    ):
        raise RuntimeError("R0.73J staged recap inventory is invalid")
    home = staged[PUBLIC / "research-review.html"].decode("utf-8")
    route = re.search(
        r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73J">(.*?)</nav>',
        home, flags=re.S,
    )
    route_links = [] if route is None else re.findall(
        r'href="/notes/(r0-[^"]+)\.html"', route.group(1)
    )
    if len(route_links) != 96 or len(set(route_links)) != 96:
        raise RuntimeError("R0.73J staged home route inventory is invalid")
    literature = staged[PUBLIC / "literature-review.html"].decode("utf-8")
    if (
        'class="route-r073j-deck-update"' not in literature
        or "2896/2896" not in literature
    ):
        raise RuntimeError("R0.73J staged literature route endpoint is invalid")
    literature_ids = re.findall(r'\bid="([^"]+)"', literature)
    if len(literature_ids) != len(set(literature_ids)):
        raise RuntimeError("R0.73J staged literature contains duplicate HTML ids")
    site = json.loads(staged[PUBLIC / "site-version.json"])
    release = json.loads(staged[ROOT / "research/release-manifest.json"])
    inventory = json.loads(staged[ROOT / "research/formal-archive-inventory.json"])
    if (
        site.get("publicHtmlNoteCount") != 186
        or release.get("postR060RecapNodeCount") != 126
        or release.get("postR070APublishedReleaseCount") != 88
        or release.get("postR070AFormalSealedReleaseCount") != 64
        or release.get("legacyFormalFigureBacklogCount") != 24
        or inventory.get("publishedReleaseCount") != 88
        or inventory.get("formalSealedReleaseCount") != 64
    ):
        raise RuntimeError("R0.73J staged accounting drifted")


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
    descriptor, temporary = tempfile.mkstemp(prefix="." + path.name + ".r073j-", dir=path.parent)
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


def commit_transaction(staged: dict[Path, bytes]) -> None:
    ordered = sorted(staged, key=lambda path: path.as_posix())
    if not ordered:
        raise RuntimeError("R0.73J transaction is empty")
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
        committed = True
    except Exception:
        for path in reversed(replaced):
            old = backups[path]
            if old is None:
                path.unlink(missing_ok=True)
            else:
                rollback = write_temp_for(path, old, modes[path])
                os.replace(rollback, path)
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
            raise RuntimeError("R0.73J materialized figure-package asset missing: " + name)
        if target.read_bytes() != (source / name).read_bytes():
            raise RuntimeError("R0.73J public figure-package asset is not byte-identical: " + name)
    rows = {
        str(row.get("path", "")): row
        for row in figure_manifest.get("figure", {}).get("outputs", [])
        if isinstance(row, dict)
    }
    for suffix in ("pdf", "svg", "png"):
        source_path = source / f"figure.{suffix}"
        target_path = PUBLIC / f"assets/r073j/{FIGURE_ID}.{suffix}"
        row = rows.get(f"figure.{suffix}")
        if row is None or not target_path.is_file() or target_path.is_symlink():
            raise RuntimeError("R0.73J materialized web figure missing: " + suffix)
        if target_path.read_bytes() != source_path.read_bytes():
            raise RuntimeError("R0.73J public web figure is not byte-identical: " + suffix)
        if digest(target_path) != row.get("sha256") or target_path.stat().st_size != row.get("bytes"):
            raise RuntimeError("R0.73J materialized web figure escaped manifest: " + suffix)


def publication_stage_incomplete() -> bool:
    pdfs = (
        PUBLIC / "notes/r0-73j.pdf",
        PUBLIC / "recap-r0-61-r0-73j.pdf",
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
            (ROOT / "scripts/i18n-snapshots/r073j-missing.json").read_text(encoding="utf-8")
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
        if isinstance(row, dict) and re.fullmatch(r"r073j\d{3}", str(row.get("id", "")))
    } if isinstance(translations, list) else {}
    if len(by_id) != len(snapshot):
        return True
    for index, snapshot_row in enumerate(snapshot, 1):
        row = by_id.get(f"r073j{index:03d}")
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
            "Validate or explicitly apply the staged R0.73J HTML/manifest transaction. "
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
        help="explicitly apply the HTML/manifest transaction from the exact R0.73I source",
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
            # A later provenance-only reseal may harden the archived package
            # while preserving all three scientific master bytes.  In that
            # case --apply repairs the public package mirror transactionally.
            resealed: dict[Path, bytes] = {}
            stage_figure_assets(resealed, figure_manifest)
            commit_transaction(resealed)
            synchronized_assets = len(resealed)
            verify_materialized_figure_assets(figure_manifest)
        print(json.dumps({
            "release": "R0.73J",
            "siteVersion": "1.50",
            "notes": 186,
            "recapNodes": 126,
            "published": 88,
            "formalSealed": 64,
            "legacyBacklog": 24,
            "phases": 45,
            "routeNotes": 96,
            "next": "R0.73K",
            "rootVersion": "1.50",
            "noOp": True,
            "publicationStageIncomplete": publication_stage_incomplete(),
            "pdfGenerated": False,
            "translationsGenerated": False,
            "synchronizedAssets": synchronized_assets,
        }, ensure_ascii=False))
        return

    staged: dict[Path, bytes] = {}
    stage_figure_assets(staged, figure_manifest)
    staged[PUBLIC / "notes/r0-73j.html"] = build_note().encode("utf-8")
    staged[PUBLIC / "recap-r0-61-r0-73j.html"] = build_recap().encode("utf-8")
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
            "release": "R0.73J",
            "sourceState": "R0.73I",
            "checkOnly": True,
            "wouldWrite": len(staged),
            "publicationStageIncomplete": True,
        }, ensure_ascii=False))
        return

    commit_transaction(staged)
    if len(list((PUBLIC / "notes").glob("r0-*.html"))) != 186:
        raise RuntimeError("R0.73J postcommit note count is not 186")
    verify_materialized_figure_assets(figure_manifest)
    print(json.dumps({
        "release": "R0.73J",
        "siteVersion": "1.50",
        "notes": 186,
        "recapNodes": 126,
        "published": 88,
        "formalSealed": 64,
        "legacyBacklog": 24,
        "phases": 45,
        "routeNotes": 96,
        "next": "R0.73K",
        "rootVersion": "1.50",
        "noOp": False,
        "publicationStageIncomplete": True,
        "pdfGenerated": False,
        "translationsGenerated": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
