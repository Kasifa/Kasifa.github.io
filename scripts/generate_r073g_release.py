#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the fail-closed transactional R0.73G GitHub Pages release."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import tempfile

from generate_r072o_release import assert_clean, once, required, section
from generate_r072p_release import assert_mathjax_clean
from r073g_release_content import (
    CERTIFICATE_RELATIVE,
    CLOSED,
    EXPERIMENT_RELATIVE,
    FALSE,
    FIGURE_ID,
    FIGURE_RELATIVE,
    HOME_G_CARD,
    HOME_LATEST_SPOTLIGHT,
    HOME_NEXT,
    NOTE_ARTICLE,
    NOTE_HERO,
    OPEN,
    R073F_RELEASE_BASELINE,
    R073G_RELEASE_TARGET,
)

ROOT = Path(os.environ.get(
    "R073G_RELEASE_ROOT", Path(__file__).resolve().parents[1]
)).resolve()
PUBLIC = ROOT / "public"

CERTIFIED_REPORT_COMMIT = "21c11ba3eef7f2b5dc3f107957e0744a0471745d"
EXPERIMENT_PACKAGE_COMMIT = "0679192b65a294bb211c96decc47bb046ab60b93"
FIGURE_PACKAGE_COMMIT = "TO_BE_FILLED_AFTER_FIGURE_PACKAGE_COMMIT"
CERTIFICATE_PACKAGE_COMMIT = "TO_BE_FILLED_AFTER_CERTIFICATE_COMMIT"
FIGURE_METADATA_SEAL_COMMIT = "TO_BE_FILLED_AFTER_FIGURE_SEAL_COMMIT"
FIGURE_PUBLICATION_COMMIT = "TO_BE_FILLED_AFTER_FIGURE_PUBLICATION_COMMIT"
FIGURE_PACKAGE_COMMIT_PLACEHOLDER = "TO_BE_FILLED_AFTER_FIGURE_PACKAGE_COMMIT"
CERTIFICATE_COMMIT_PLACEHOLDER = "TO_BE_FILLED_AFTER_CERTIFICATE_COMMIT"
FIGURE_SEAL_COMMIT_PLACEHOLDER = "TO_BE_FILLED_AFTER_FIGURE_SEAL_COMMIT"
FIGURE_PUBLICATION_COMMIT_PLACEHOLDER = (
    "TO_BE_FILLED_AFTER_FIGURE_PUBLICATION_COMMIT"
)

CLOSED_KEYS = (
    "exactDecayingShearPerturbationEquation",
    "selectedSeedPlanarInvariantClass",
    "selectedNonlinearOrbitGlobalSmoothness",
    "topEigenvectorPolynomialH3Cost",
    "fixedWindowH3Bootstrap",
    "allModeQuadraticRemainderBound",
    "nonlinearRelativeAmplification",
    "topEigenvectorDoubleRowLeakage",
)

FALSE_KEYS = (
    "singleLinearRowNonlinearInvariant",
    "kineticL2QuadraticRemainderBound",
    "selectedRowCanCreateThreeDimensionalVortexStretching",
    "oneRowGainAloneImpliesOrderOneDeparture",
    "oneRowGainAloneImpliesFiniteTimeSingularity",
)

OPEN_KEYS = (
    "naturalSeedOrderOneDeparture",
    "targetedCubicModeConvolutionEstimate",
    "harmonicResolvedEvenOddPropagation",
    "transverseThreeDimensionalTriadClosure",
    "singleBackgroundSingleOrbitInstability",
    "completeOSSquireA2DirectSum",
    "Clay",
)

CERTIFICATE_FALSE_SHORTCUT_KEYS = FALSE_KEYS
CERTIFICATE_OPEN_KEYS = OPEN_KEYS

GAP_FALSE_KEYS = (
    "singleLinearRowNonlinearInvariant",
    "selectedRowCanCreateThreeDimensionalVortexStretching",
    "oneRowGainAloneImpliesOrderOneDeparture",
    "oneRowGainAloneImpliesFiniteTimeSingularity",
)

GAP_OPEN_KEYS = (
    "naturalSeedOrderOneDeparture",
    "sharpBilinearEvolutionAtUnstableRate",
    "transverseThreeDimensionalTriadClosure",
    "singleBackgroundSingleOrbitInstability",
    "completeOSSquireA2DirectSum",
    "Clay",
)

CERTIFICATE_BOUNDARY_ONLY_KEYS = (
    "machineProofOfProsePdeArgument",
    "finiteDiagnosticProvesContinuumTopSpace",
    "finiteDiagnosticProvesUniformH3Bound",
    "finiteLeakageProvesNonlinearInstability",
    "naturalSeedOrderOneDeparture",
    "threeDimensionalVortexStretchingFromSelectedPlanarRow",
    "generalThreeDimensionalRegularityConclusion",
    "finiteTimeSingularity",
    "Clay",
)

SOURCE_PATHS = (
    "research/r073g_problem_freeze.md",
    "research/r073g_nonlinear_shadowing_proof.md",
    "research/r073g_operator_derivation.md",
    "research/r073g_adversarial_audit.md",
    "research/r073g_independent_analytic_audit.md",
    "research/r073g_report-source.md",
    "research/r073g_gap_matrix.md",
    "research/r073g_literature_audit.md",
)

FIGURE_IMMUTABLE_FILES = (
    "README.md",
    "caption.md",
    "config.json",
    "figure.pdf",
    "figure.png",
    "figure.svg",
    "plot.py",
    "qa-final-size.png",
    "qa-grayscale.png",
    "qa-pdf.png",
    "qa-protocol.md",
    "qa-report.md",
    "requirements.txt",
    "results.json",
)

FIGURE_METADATA_CORE_FILES = (
    "contract.json",
    "command.txt",
    "validate.py",
    "validation.json",
)

PUBLIC_VOICE_BANS = (
    "\u6211\u4eec",
    "\u653b\u5173",
    "\u4e3b\u653b",
    "\u7a81\u7834",
    "\u7814\u7a76\u7eaa\u5f8b",
    "\u4e09\u91cd\u5ba1\u8ba1",
    "\u6740\u6b7b\u9519\u8bef\u60f3\u6cd5",
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
    return (
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def assert_public_voice(value: str, label: str) -> None:
    for phrase in PUBLIC_VOICE_BANS:
        if phrase in value:
            raise RuntimeError(label + ": reader-facing voice violation")


def replace_all(html: str, old: str, new: str, label: str) -> str:
    if old not in html:
        raise RuntimeError(label + ": source not found")
    return html.replace(old, new)


def git_object_bytes(commit: str, relative: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{commit}:{relative}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout


def verify_complete_flat_ledger(directory: Path, label: str) -> None:
    ledger = directory / "SHA256SUMS"
    if not ledger.is_file():
        raise RuntimeError(label + ": SHA256SUMS is missing")
    declared: list[str] = []
    for row in ledger.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/\\\r\n]+)", row)
        if match is None:
            raise RuntimeError(label + ": malformed SHA256SUMS row")
        name = match.group(2)
        if name in declared:
            raise RuntimeError(label + ": duplicate SHA256SUMS entry " + name)
        candidate = directory / name
        if (
            not candidate.is_file()
            or candidate.is_symlink()
            or digest(candidate) != match.group(1)
        ):
            raise RuntimeError(label + ": hash mismatch " + name)
        declared.append(name)
    if declared != sorted(declared):
        raise RuntimeError(label + ": SHA256SUMS must be sorted")
    actual = sorted(
        path.name
        for path in directory.iterdir()
        if path.name != "SHA256SUMS" and path.is_file() and not path.is_symlink()
    )
    if sorted(declared) != actual:
        raise RuntimeError(label + ": SHA256SUMS inventory is incomplete")
    unexpected = [
        path.name
        for path in directory.iterdir()
        if path.name != "SHA256SUMS"
        and (not path.is_file() or path.is_symlink())
    ]
    if unexpected:
        raise RuntimeError(label + ": unexpected package entry " + unexpected[0])


def manifest_candidate(manifest: Path, relative: str) -> Path:
    root_candidate = ROOT / relative
    if root_candidate.is_file():
        return root_candidate
    return manifest.parent / relative


def verify_manifest_hashes(path: Path, label: str) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    checked = 0
    for group in (
        "sources",
        "inputs",
        "outputs",
        "sourceBindings",
        "experimentBindings",
        "outputBindings",
        "packageBindings",
        "packageSourceBindings",
        "contentBindings",
        "files",
        "analyticSourceBindings",
        "scientificOutputs",
    ):
        for row in payload.get(group, []):
            if not isinstance(row, dict):
                continue
            relative = str(row.get("path", ""))
            expected = str(row.get("sha256", ""))
            if not relative or not re.fullmatch(r"[0-9a-f]{64}", expected):
                raise RuntimeError(f"{label}: malformed {group} hash row")
            candidate = manifest_candidate(path, relative)
            if not candidate.is_file() or digest(candidate) != expected:
                raise RuntimeError(f"{label}: stale {group} hash {relative}")
            if row.get("bytes") is not None and candidate.stat().st_size != row["bytes"]:
                raise RuntimeError(f"{label}: stale {group} size {relative}")
            checked += 1
    if checked == 0:
        raise RuntimeError(label + ": no content hashes were checked")
    return payload


def verify_source_bindings(payload: dict, label: str) -> None:
    rows = payload.get("sourceBindings", payload.get("analyticSourceBindings", []))
    if not isinstance(rows, list) or len(rows) != len(SOURCE_PATHS):
        raise RuntimeError(label + ": source binding inventory is not exactly eight files")
    by_path = {
        str(row.get("path", "")): row
        for row in rows
        if isinstance(row, dict)
    }
    if set(by_path) != set(SOURCE_PATHS) or len(by_path) != len(rows):
        raise RuntimeError(label + ": source binding path set is not exact")
    default_commit = str(payload.get("sourceCommit", ""))
    for relative in SOURCE_PATHS:
        row = by_path.get(relative)
        if row is None:
            raise RuntimeError(label + ": source binding is missing " + relative)
        commit = str(
            row.get(
                "commit",
                row.get("sourceCommit", default_commit),
            )
        )
        if commit != CERTIFIED_REPORT_COMMIT:
            raise RuntimeError(label + ": source commit mismatch " + relative)
        frozen = git_object_bytes(commit, relative)
        if sha256_bytes(frozen) != row.get("sha256"):
            raise RuntimeError(label + ": frozen source hash mismatch " + relative)
        if row.get("bytes") is not None and len(frozen) != row["bytes"]:
            raise RuntimeError(label + ": frozen source size mismatch " + relative)
        current = ROOT / relative
        if not current.is_file() or current.read_bytes() != frozen:
            raise RuntimeError(label + ": working source differs from commit " + relative)


def verify_sealed_directory(directory: Path, commit: str, label: str) -> None:
    subprocess.run(
        ["git", "cat-file", "-e", commit + "^{commit}"],
        cwd=ROOT,
        check=True,
    )
    for current in directory.iterdir():
        if not current.is_file():
            continue
        relative = current.relative_to(ROOT).as_posix()
        try:
            frozen = git_object_bytes(commit, relative)
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(label + ": file absent from sealed commit " + relative) from exc
        if current.read_bytes() != frozen:
            raise RuntimeError(label + ": sealed file changed " + relative)


def verify_exact_flat_directory_at_commit(
    directory: Path,
    commit: str,
    label: str,
) -> None:
    subprocess.run(
        ["git", "cat-file", "-e", commit + "^{commit}"],
        cwd=ROOT,
        check=True,
    )
    prefix = directory.relative_to(ROOT).as_posix()
    frozen = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", commit, "--", prefix],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    current = [
        path.relative_to(ROOT).as_posix()
        for path in directory.iterdir()
        if path.is_file() and not path.is_symlink()
    ]
    if sorted(frozen) != sorted(current):
        raise RuntimeError(label + ": sealed directory inventory changed")
    verify_sealed_directory(directory, commit, label)


def strip_manifest_hash_row(payload: bytes, label: str) -> bytes:
    rows = payload.splitlines(keepends=True)
    matches = [
        index
        for index, row in enumerate(rows)
        if re.fullmatch(rb"[0-9a-f]{64}  manifest\.json\r?\n?", row)
    ]
    if len(matches) != 1:
        raise RuntimeError(label + ": expected exactly one manifest hash row")
    return b"".join(row for index, row in enumerate(rows) if index != matches[0])


def verify_metadata_overlay(directory: Path) -> None:
    if len(FIGURE_IMMUTABLE_FILES) != 14 or len(set(FIGURE_IMMUTABLE_FILES)) != 14:
        raise RuntimeError("R0.73G F inventory must contain exactly 14 immutable files")
    verify_named_files_at_commit(
        directory,
        FIGURE_METADATA_SEAL_COMMIT,
        FIGURE_METADATA_CORE_FILES,
        "R0.73G figure metadata core",
    )

    manifest_path = directory / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if "publication" not in manifest:
        raise RuntimeError("R0.73G figure manifest is missing publication overlay")
    without_publication = dict(manifest)
    del without_publication["publication"]
    relative_manifest = manifest_path.relative_to(ROOT).as_posix()
    if json_bytes(without_publication) != git_object_bytes(
        FIGURE_METADATA_SEAL_COMMIT,
        relative_manifest,
    ):
        raise RuntimeError("R0.73G publication-free manifest differs from seal S")

    ledger_path = directory / "SHA256SUMS"
    current_ledger = strip_manifest_hash_row(
        ledger_path.read_bytes(),
        "R0.73G current figure ledger",
    )
    sealed_ledger = strip_manifest_hash_row(
        git_object_bytes(
            FIGURE_METADATA_SEAL_COMMIT,
            ledger_path.relative_to(ROOT).as_posix(),
        ),
        "R0.73G seal-S figure ledger",
    )
    if current_ledger != sealed_ledger:
        raise RuntimeError("R0.73G SHA ledger changed beyond the manifest hash row")


def verify_named_files_at_commit(
    directory: Path,
    commit: str,
    names: tuple[str, ...],
    label: str,
) -> None:
    subprocess.run(
        ["git", "cat-file", "-e", commit + "^{commit}"],
        cwd=ROOT,
        check=True,
    )
    for name in names:
        current = directory / name
        if not current.is_file():
            raise RuntimeError(label + ": immutable file is missing " + name)
        relative = current.relative_to(ROOT).as_posix()
        try:
            frozen = git_object_bytes(commit, relative)
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(
                label + ": immutable file absent from package commit " + name
            ) from exc
        if current.read_bytes() != frozen:
            raise RuntimeError(label + ": immutable package file changed " + name)


def checks_pass(payload: dict) -> bool:
    checks = payload.get("checks")
    exact_checks_pass = (
        isinstance(checks, dict)
        and bool(checks)
        and all(value is True for value in checks.values())
    )
    validations = payload.get("validations")
    exact_validations_pass = (
        isinstance(validations, list)
        and bool(validations)
        and all(
            isinstance(row, dict) and row.get("pass") is True
            for row in validations
        )
    )
    if "allChecksPass" in payload:
        return (
            payload.get("allChecksPass") is True
            and (exact_checks_pass or exact_validations_pass)
        )
    return (
        payload.get("status") in {"passed", "validated"}
        and exact_checks_pass
    )


def png_density(path: Path) -> tuple[int, int, int]:
    payload = path.read_bytes()
    if not payload.startswith(b"\x89PNG\r\n\x1a\n"):
        raise RuntimeError("R0.73G PNG signature is invalid")
    offset = 8
    while offset + 12 <= len(payload):
        length = struct.unpack(">I", payload[offset:offset + 4])[0]
        kind = payload[offset + 4:offset + 8]
        data = payload[offset + 8:offset + 8 + length]
        if kind == b"pHYs" and len(data) == 9:
            return struct.unpack(">IIB", data)
        offset += 12 + length
    raise RuntimeError("R0.73G PNG has no physical-density metadata")


def require_output_record(manifest: dict, figure: Path, suffix: str) -> dict:
    expected_name = f"figure.{suffix}"
    rows = manifest.get("outputs")
    if not isinstance(rows, list):
        rows = manifest.get("figure", {}).get("outputs", [])
    matches = [
        row
        for row in rows
        if Path(str(row.get("path", ""))).name == expected_name
    ]
    if len(matches) != 1:
        raise RuntimeError("R0.73G figure manifest output mismatch: " + suffix)
    row = matches[0]
    path = figure / expected_name
    if row.get("sha256") != digest(path):
        raise RuntimeError("R0.73G figure output hash mismatch: " + suffix)
    if row.get("bytes") is not None and row["bytes"] != path.stat().st_size:
        raise RuntimeError("R0.73G figure output size mismatch: " + suffix)
    return row


def validate_publication_assets(manifest: dict, directory: Path) -> None:
    publication = manifest.get("publication")
    if not isinstance(publication, dict):
        raise RuntimeError("R0.73G figure publication binding is missing")
    if (
        publication.get("byteIdentityRequired") is not True
        or publication.get("publicCopiesComplete") is not True
        or publication.get("directory") != "public/assets/r073g"
        or publication.get("fileStem") != FIGURE_ID
    ):
        raise RuntimeError("R0.73G figure publication contract is inconsistent")
    rows = publication.get("assets")
    if not isinstance(rows, list) or len(rows) != 3:
        raise RuntimeError("R0.73G publication must bind exactly three assets")
    by_path = {
        str(row.get("path", "")): row
        for row in rows
        if isinstance(row, dict)
    }
    expected_paths = {
        f"public/assets/r073g/{FIGURE_ID}.{suffix}"
        for suffix in ("pdf", "svg", "png")
    }
    if set(by_path) != expected_paths or len(by_path) != len(rows):
        raise RuntimeError("R0.73G publication asset path set is not exact")

    for suffix in ("pdf", "svg", "png"):
        relative = f"public/assets/r073g/{FIGURE_ID}.{suffix}"
        public_path = ROOT / relative
        source_path = directory / f"figure.{suffix}"
        if (
            not public_path.is_file()
            or public_path.is_symlink()
            or public_path.read_bytes() != source_path.read_bytes()
        ):
            raise RuntimeError("R0.73G public asset is not byte-identical: " + suffix)
        payload = public_path.read_bytes()
        row = by_path[relative]
        output = require_output_record(manifest, directory, suffix)
        if (
            row.get("bytes") != len(payload)
            or row.get("sha256") != sha256_bytes(payload)
            or output.get("bytes") != row.get("bytes")
            or output.get("sha256") != row.get("sha256")
            or git_object_bytes(FIGURE_PUBLICATION_COMMIT, relative) != payload
        ):
            raise RuntimeError("R0.73G public asset binding mismatch: " + suffix)


def ensure_release_commits_ready() -> None:
    bindings = (
        (
            "figure package",
            FIGURE_PACKAGE_COMMIT,
            FIGURE_PACKAGE_COMMIT_PLACEHOLDER,
        ),
        (
            "certificate package",
            CERTIFICATE_PACKAGE_COMMIT,
            CERTIFICATE_COMMIT_PLACEHOLDER,
        ),
        (
            "figure metadata seal",
            FIGURE_METADATA_SEAL_COMMIT,
            FIGURE_SEAL_COMMIT_PLACEHOLDER,
        ),
        (
            "figure publication",
            FIGURE_PUBLICATION_COMMIT,
            FIGURE_PUBLICATION_COMMIT_PLACEHOLDER,
        ),
    )
    for label, value, placeholder in bindings:
        if value == placeholder:
            raise RuntimeError(
                "R0.73G release is intentionally sealed shut: replace "
                + placeholder + " with the " + label + " commit"
            )
        if not re.fullmatch(r"[0-9a-f]{40}", value):
            raise RuntimeError(
                "R0.73G " + label + " commit must be a full Git SHA"
            )


def is_commit_ancestor(ancestor: str, descendant: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def verify_release_commit_chain() -> None:
    ensure_release_commits_ready()
    commits = (
        CERTIFIED_REPORT_COMMIT,
        EXPERIMENT_PACKAGE_COMMIT,
        FIGURE_PACKAGE_COMMIT,
        CERTIFICATE_PACKAGE_COMMIT,
        FIGURE_METADATA_SEAL_COMMIT,
        FIGURE_PUBLICATION_COMMIT,
    )
    if len(set(commits)) != len(commits):
        raise RuntimeError(
            "R0.73G source/E/F/C/S/P commits must be strictly distinct"
        )
    for commit in commits:
        subprocess.run(
            ["git", "cat-file", "-e", commit + "^{commit}"],
            cwd=ROOT,
            check=True,
        )
    for ancestor, descendant, label in (
        (CERTIFIED_REPORT_COMMIT, FIGURE_PACKAGE_COMMIT, "source < F"),
        (CERTIFIED_REPORT_COMMIT, EXPERIMENT_PACKAGE_COMMIT, "source < E"),
        (EXPERIMENT_PACKAGE_COMMIT, FIGURE_PACKAGE_COMMIT, "E < F"),
        (FIGURE_PACKAGE_COMMIT, CERTIFICATE_PACKAGE_COMMIT, "F < C"),
        (CERTIFICATE_PACKAGE_COMMIT, FIGURE_METADATA_SEAL_COMMIT, "C < S"),
        (FIGURE_METADATA_SEAL_COMMIT, FIGURE_PUBLICATION_COMMIT, "S < P"),
    ):
        if not is_commit_ancestor(ancestor, descendant):
            raise RuntimeError("R0.73G commit order is invalid: " + label)
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    for commit, label in (
        (EXPERIMENT_PACKAGE_COMMIT, "E"),
        (FIGURE_PACKAGE_COMMIT, "F"),
        (CERTIFICATE_PACKAGE_COMMIT, "C"),
        (FIGURE_METADATA_SEAL_COMMIT, "S"),
        (FIGURE_PUBLICATION_COMMIT, "P"),
    ):
        if not is_commit_ancestor(commit, head):
            raise RuntimeError(f"R0.73G {label} commit is not an ancestor of HEAD")


def preflight_release_state() -> None:
    expected_baseline = {
        "latestCompletedRelease": "r073f",
        "siteVersion": "1.46",
        "publicHtmlNoteCount": 182,
        "postR060RecapNodeCount": 122,
        "nextRelease": "r073g",
        "latestReleaseGate": "tests/r073f-moving-dichotomy-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r073f-release.test.mjs",
        "postR070APublishedReleaseCount": 84,
        "postR070AFormalSealedReleaseCount": 60,
        "legacyFormalFigureBacklogCount": 24,
    }
    expected_target = {
        "latestCompletedRelease": "r073g",
        "siteVersion": "1.47",
        "publicHtmlNoteCount": 183,
        "postR060RecapNodeCount": 123,
        "nextRelease": "r073h",
        "postR070APublishedReleaseCount": 85,
        "postR070AFormalSealedReleaseCount": 61,
        "legacyFormalFigureBacklogCount": 24,
    }
    if R073F_RELEASE_BASELINE != expected_baseline:
        raise RuntimeError("R0.73G content module changed the exact R0.73F baseline")
    if R073G_RELEASE_TARGET != expected_target:
        raise RuntimeError("R0.73G content module changed the exact v1.47 target")

    release_path = ROOT / "research/release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    for key, value in R073F_RELEASE_BASELINE.items():
        if release.get(key) != value:
            raise RuntimeError(f"release manifest is not exactly at R0.73F: {key}")
    if release.get("nextReleaseSourceStage") is not None:
        raise RuntimeError("R0.73F baseline has an unexpected source-stage payload")

    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    inventory_state = (
        inventory.get("latestPublishedRelease"),
        inventory.get("publishedReleaseCount"),
        inventory.get("formalSealedReleaseCount"),
        inventory.get("legacyFormalFigureBacklogCount"),
    )
    if inventory_state != ("r073f", 84, 60, 24):
        raise RuntimeError("formal archive inventory is not exactly at R0.73F")
    if (
        inventory.get("publishedReleases", [])[-1:] != ["r073f"]
        or inventory.get("formalSealedReleases", [])[-1:] != ["r073f"]
    ):
        raise RuntimeError("R0.73F inventory tails are not exact")
    formal = release.get("formalArchiveInventory", {})
    if (
        formal.get("path") != "research/formal-archive-inventory.json"
        or formal.get("sha256") != digest(inventory_path)
    ):
        raise RuntimeError("R0.73F release manifest lost its inventory binding")

    site = json.loads((PUBLIC / "site-version.json").read_text(encoding="utf-8"))
    if site != {
        "schemaVersion": "research-site-version-v1",
        "version": "1.46",
        "latestRelease": "R0.73F",
        "publicHtmlNoteCount": 182,
        "publishedDate": "2026-08-30",
    }:
        raise RuntimeError("public site-version is not exactly at R0.73F")
    if (ROOT / "VERSION").read_text(encoding="utf-8") != "1.46\n":
        raise RuntimeError("root VERSION is not R0.73F v1.46")
    if len(list((PUBLIC / "notes").glob("r0-*.html"))) != 182:
        raise RuntimeError("R0.73F preflight expected 182 public HTML notes")

    forbidden = (
        "notes/r0-73g.html",
        "notes/r0-73g.pdf",
        "recap-r0-61-r0-73g.html",
        "recap-r0-61-r0-73g.pdf",
        f"assets/r073g/{FIGURE_ID}.pdf",
        f"assets/r073g/{FIGURE_ID}.svg",
        f"assets/r073g/{FIGURE_ID}.png",
    )
    for relative in forbidden:
        if (PUBLIC / relative).exists():
            raise RuntimeError("R0.73F preflight found premature output: " + relative)

    home = (PUBLIC / "research-review.html").read_text(encoding="utf-8")
    for token in (
        'data-site-version="1.46"',
        "<strong>182</strong>公开研究笔记",
        "<strong>R0.73F</strong>最新研究节点",
        'aria-label="R0.69P–R0.73F"',
        "R0.70A–R0.73F：84 节已公开，60 节完整封存",
    ):
        if token not in home:
            raise RuntimeError("R0.73F home baseline missing token: " + token)
    if 'data-release="r073g"' in home:
        raise RuntimeError("R0.73F home already contains an R0.73G card")
    route = re.search(
        r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73F">'
        r"(.*?)</nav>",
        home,
        flags=re.S,
    )
    if (
        route is None
        or len(re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))) != 92
    ):
        raise RuntimeError("R0.73F home must contain 92 current-route links")

    recap = (PUBLIC / "recap-r0-61-r0-73f.html").read_text(encoding="utf-8")
    start = recap.index('<section id="node-index">')
    end = recap.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', recap[start:end])
    if len(links) != 122 or len(set(links)) != 122:
        raise RuntimeError("R0.73F recap must contain 122 unique nodes")
    if recap.count('<article class="phase">') != 41:
        raise RuntimeError("R0.73F recap must contain 41 phases")
    for value, label in ((home, "home"), (recap, "recap")):
        assert_public_voice(value, "R0.73F baseline " + label)

    ensure_release_commits_ready()

def validate_analytic_sources() -> None:
    subprocess.run(
        ["git", "cat-file", "-e", CERTIFIED_REPORT_COMMIT + "^{commit}"],
        cwd=ROOT,
        check=True,
    )
    for relative in SOURCE_PATHS:
        path = ROOT / relative
        if not path.is_file():
            raise RuntimeError("missing R0.73G analytic source: " + relative)
        if path.read_bytes() != git_object_bytes(CERTIFIED_REPORT_COMMIT, relative):
            raise RuntimeError("R0.73G source differs from sourceCommit: " + relative)

    report = (ROOT / "research/r073g_report-source.md").read_text(encoding="utf-8")
    gap = (ROOT / "research/r073g_gap_matrix.md").read_text(encoding="utf-8")
    proof = (
        ROOT / "research/r073g_nonlinear_shadowing_proof.md"
    ).read_text(encoding="utf-8")
    operator = (
        ROOT / "research/r073g_operator_derivation.md"
    ).read_text(encoding="utf-8")
    adversarial = (
        ROOT / "research/r073g_adversarial_audit.md"
    ).read_text(encoding="utf-8")
    independent = (
        ROOT / "research/r073g_independent_analytic_audit.md"
    ).read_text(encoding="utf-8")
    literature = (
        ROOT / "research/r073g_literature_audit.md"
    ).read_text(encoding="utf-8")

    for key in CLOSED_KEYS:
        for source, label in ((report, "report"), (gap, "gap")):
            if key + "=CLOSED" not in source:
                raise RuntimeError(f"R0.73G {label} lost CLOSED token: {key}")
    for key in FALSE_KEYS:
        expected = (
            key + "=FALSE_AS_INFERENCE"
            if key == "oneRowGainAloneImpliesOrderOneDeparture"
            else key + "=FALSE"
        )
        if expected not in report:
            raise RuntimeError(f"R0.73G report lost FALSE token: {key}")
    for key in GAP_FALSE_KEYS:
        expected = (
            key + "=FALSE_AS_INFERENCE"
            if key == "oneRowGainAloneImpliesOrderOneDeparture"
            else key + "=FALSE"
        )
        if expected not in gap:
            raise RuntimeError(f"R0.73G gap lost FALSE token: {key}")
    for key in OPEN_KEYS:
        if key + "=OPEN" not in report:
            raise RuntimeError(f"R0.73G report lost OPEN token: {key}")
    for key in GAP_OPEN_KEYS:
        if key + "=OPEN" not in gap:
            raise RuntimeError(f"R0.73G gap lost OPEN token: {key}")

    for token in (
        r"T_D=\frac{d_D}{4}",
        r"\|\phi_\Lambda\|_{H^3}\le C_{\rm top}\Lambda^2",
        r"Y'\le a\Lambda Y+bY^2",
        r"e^{-(M_D-\kappa_D)_+\Lambda}",
        r"K_z=0,\pm2",
        r"n^2-\frac{15}{4}",
    ):
        if token not in proof and token not in report:
            raise RuntimeError("R0.73G proof chain missing token: " + token)
    for token in (
        "natural seed",
        "still open",
        "exact kinetic-to-velocity map",
    ):
        if token.lower() not in operator.lower():
            raise RuntimeError("R0.73G operator derivation missing token: " + token)
    if "POST-REPAIR SUBSTANTIVE VERDICT: FINAL PASS" not in adversarial:
        raise RuntimeError("R0.73G adversarial audit is not FINAL PASS")
    if "**Correction obligations:** none" not in independent:
        raise RuntimeError("R0.73G independent audit has correction obligations")
    for token in (
        "bounded non-collision finding",
        "priority claim is made.",
        "math/0508173",
        "1803.11024",
        "1604.01831",
        "2509.18070",
    ):
        if token not in literature:
            raise RuntimeError("R0.73G literature audit missing token: " + token)

    for value, label in (
        (NOTE_HERO, "note hero"),
        (NOTE_ARTICLE, "note article"),
        (HOME_G_CARD, "home card"),
        (HOME_LATEST_SPOTLIGHT, "home spotlight"),
        (HOME_NEXT, "home next"),
    ):
        assert_public_voice(value, "R0.73G " + label)

def validate_experiment() -> None:
    directory = ROOT / EXPERIMENT_RELATIVE
    required_names = (
        "nonlinear_row_leakage_diagnostic.py",
        "nonlinear_row_leakage_summary.json",
        "nonlinear_row_leakage_rows.csv",
        "nonlinear_row_leakage_convergence.csv",
        "independent_validation.json",
        "manifest.json",
        "SHA256SUMS",
    )
    for name in required_names:
        if not (directory / name).is_file():
            raise RuntimeError("missing R0.73G experiment input: " + name)
    verify_complete_flat_ledger(directory, "R0.73G experiment")
    verify_sealed_directory(
        directory, EXPERIMENT_PACKAGE_COMMIT, "R0.73G experiment"
    )
    summary = json.loads(
        (directory / "nonlinear_row_leakage_summary.json").read_text(
            encoding="utf-8"
        )
    )
    independent = json.loads(
        (directory / "independent_validation.json").read_text(encoding="utf-8")
    )
    manifest = verify_manifest_hashes(
        directory / "manifest.json", "R0.73G experiment manifest"
    )
    if (
        summary.get("diagnosticOnly") is not True
        or summary.get("evidenceClass") != "finite-binary64-diagnostic-only"
        or summary.get("crossValidation", {}).get("allKernelChecksPass") is not True
    ):
        raise RuntimeError("R0.73G primary finite diagnostic is not passed")
    if not checks_pass(independent):
        raise RuntimeError("R0.73G independent finite validation is not passed")
    producer = manifest.get("producerSourceBinding", {})
    diagnostic_relative = "experiments/r073g/nonlinear_row_leakage_diagnostic.py"
    if (
        manifest.get("release") != "R0.73G-finite-diagnostic"
        or manifest.get("status") != "validated"
        or manifest.get("diagnosticOnly") is not True
        or manifest.get("primaryAllChecksPass") is not True
        or manifest.get("independentAllChecksPass") is not True
        or producer.get("path") != diagnostic_relative
        or producer.get("sourceCommit") != CERTIFIED_REPORT_COMMIT
        or producer.get("sha256") != digest(ROOT / diagnostic_relative)
        or producer.get("bytes") != (ROOT / diagnostic_relative).stat().st_size
        or producer.get("sourceBeforeRunGateEnforced") is not True
        or producer.get("workingSourceMatchesCommitAtRun") is not True
        or git_object_bytes(CERTIFIED_REPORT_COMMIT, diagnostic_relative)
        != (ROOT / diagnostic_relative).read_bytes()
    ):
        raise RuntimeError("R0.73G experiment manifest identity is inconsistent")

    for payload, label in (
        (summary, "primary"),
        (independent, "independent"),
        (manifest, "manifest"),
    ):
        boundary = payload.get("claimBoundary", {})
        if boundary.get("finiteBinary64Diagnostic") is not True:
            raise RuntimeError(f"R0.73G {label} lost finite diagnostic status")
        for key in (
            "finiteH3CostProvesUniformContinuumH3Bound",
            "finiteLeakageProvesNonlinearInstability",
            "finiteTopEqualsContinuumTop",
            "ordinaryCutoffAgreementIsTailBound",
            "threeDimensionalVortexStretchingPresentInThisPlanarRow",
            "transitionThresholdEstablished",
            "clayProblemSolved",
        ):
            if boundary.get(key) is not False:
                raise RuntimeError(f"R0.73G {label} escaped boundary: {key}")


def validate_certificate() -> dict:
    ensure_release_commits_ready()
    directory = ROOT / CERTIFICATE_RELATIVE
    required_names = (
        "certificate.json",
        "independent_recompute.json",
        "validation.json",
        "manifest.json",
        "validate_certificate.py",
        "SHA256SUMS",
    )
    for name in required_names:
        if not (directory / name).is_file():
            raise RuntimeError("missing R0.73G certificate input: " + name)
    verify_complete_flat_ledger(directory, "R0.73G certificate")
    verify_sealed_directory(
        directory, CERTIFICATE_PACKAGE_COMMIT, "R0.73G certificate"
    )

    certificate = json.loads(
        (directory / "certificate.json").read_text(encoding="utf-8")
    )
    independent = json.loads(
        (directory / "independent_recompute.json").read_text(encoding="utf-8")
    )
    validation = json.loads(
        (directory / "validation.json").read_text(encoding="utf-8")
    )
    manifest = verify_manifest_hashes(
        directory / "manifest.json", "R0.73G certificate manifest"
    )
    if (
        not checks_pass(certificate)
        or not checks_pass(independent)
        or not checks_pass(validation)
    ):
        raise RuntimeError("R0.73G certificate package is not independently passed")
    source_commit = str(
        certificate.get("sourceCommit", manifest.get("sourceCommit", ""))
    )
    if (
        source_commit != CERTIFIED_REPORT_COMMIT
        or certificate.get("release") != "R0.73G"
        or manifest.get("release") != "R0.73G"
        or manifest.get("status") != "validated-content-addressed-unsealed"
        or manifest.get("sourceCommit") != CERTIFIED_REPORT_COMMIT
        or certificate.get("experimentCommit") != EXPERIMENT_PACKAGE_COMMIT
        or independent.get("experimentCommit") != EXPERIMENT_PACKAGE_COMMIT
        or validation.get("experimentCommit") != EXPERIMENT_PACKAGE_COMMIT
        or manifest.get("experimentCommit") != EXPERIMENT_PACKAGE_COMMIT
        or certificate.get("figurePackageCommit") != FIGURE_PACKAGE_COMMIT
        or independent.get("figurePackageCommit") != FIGURE_PACKAGE_COMMIT
        or validation.get("figurePackageCommit") != FIGURE_PACKAGE_COMMIT
        or manifest.get("figurePackageCommit") != FIGURE_PACKAGE_COMMIT
    ):
        raise RuntimeError("R0.73G certificate provenance commits are not exact")
    verify_source_bindings(manifest, "R0.73G certificate manifest")

    ledgers = certificate.get("claimLedgers")
    if not isinstance(ledgers, dict):
        raise RuntimeError("R0.73G certificate claimLedgers are missing")
    report_ledger = ledgers.get("reportSourceBoundary")
    gap_ledger = ledgers.get("gapMatrixReleaseDecisions")
    expected_report = {
        **{key: "CLOSED" for key in CLOSED_KEYS},
        **{
            key: (
                "FALSE_AS_INFERENCE"
                if key == "oneRowGainAloneImpliesOrderOneDeparture"
                else "FALSE"
            )
            for key in FALSE_KEYS
        },
        **{key: "OPEN" for key in OPEN_KEYS},
    }
    expected_gap = {
        **{key: "CLOSED" for key in CLOSED_KEYS},
        **{
            key: (
                "FALSE_AS_INFERENCE"
                if key == "oneRowGainAloneImpliesOrderOneDeparture"
                else "FALSE"
            )
            for key in GAP_FALSE_KEYS
        },
        **{key: "OPEN" for key in GAP_OPEN_KEYS},
    }
    if report_ledger != expected_report or gap_ledger != expected_gap:
        raise RuntimeError("R0.73G certificate claim ledger is not exact")
    if (
        independent.get("claimLedgers") != ledgers
        or validation.get("claimLedgers") != ledgers
    ):
        raise RuntimeError("R0.73G independent certificate ledgers drifted")

    boundary = certificate.get("claimBoundary")
    expected_boundary = set(CERTIFICATE_BOUNDARY_ONLY_KEYS)
    if not isinstance(boundary, dict) or set(boundary) != expected_boundary:
        raise RuntimeError("R0.73G certificate claimBoundary key set is not exact")
    for key in expected_boundary:
        if boundary[key] is not False:
            raise RuntimeError("R0.73G certificate escaped claim boundary: " + key)
    independent_boundary = independent.get("claimBoundary")
    if (
        not isinstance(independent_boundary, dict)
        or not independent_boundary
        or any(value is not False for value in independent_boundary.values())
        or validation.get("claimBoundary") != boundary
    ):
        raise RuntimeError("R0.73G independent certificate boundary drifted")

    subprocess.run(
        ["git", "cat-file", "-e", CERTIFICATE_PACKAGE_COMMIT + "^{commit}"],
        cwd=ROOT,
        check=True,
    )
    if subprocess.run(
        [
            "git", "merge-base", "--is-ancestor",
            CERTIFIED_REPORT_COMMIT, CERTIFICATE_PACKAGE_COMMIT,
        ],
        cwd=ROOT,
    ).returncode != 0:
        raise RuntimeError("R0.73G certificate commit does not descend from sourceCommit")
    return certificate


def validate_figure(certificate: dict) -> dict:
    ensure_release_commits_ready()
    verify_release_commit_chain()
    directory = ROOT / FIGURE_RELATIVE
    required_names = (
        "figure.pdf",
        "figure.svg",
        "figure.png",
        "manifest.json",
        "contract.json",
        "validation.json",
        "caption.md",
        "validate.py",
        "SHA256SUMS",
    )
    for name in required_names:
        if not (directory / name).is_file():
            raise RuntimeError("missing R0.73G formal figure input: " + name)
    verify_complete_flat_ledger(directory, "R0.73G figure")
    verify_named_files_at_commit(
        directory,
        FIGURE_PACKAGE_COMMIT,
        FIGURE_IMMUTABLE_FILES,
        "R0.73G figure",
    )
    verify_metadata_overlay(directory)
    verify_exact_flat_directory_at_commit(
        directory,
        FIGURE_PUBLICATION_COMMIT,
        "R0.73G figure publication seal",
    )
    manifest = verify_manifest_hashes(
        directory / "manifest.json", "R0.73G figure manifest"
    )
    contract = json.loads((directory / "contract.json").read_text(encoding="utf-8"))
    validation = json.loads(
        (directory / "validation.json").read_text(encoding="utf-8")
    )
    if (
        manifest.get("figureId") != FIGURE_ID
        or manifest.get("status") != "formal"
        or manifest.get("release") not in ("R0.73G", "R0.73G-finite-diagnostic")
    ):
        raise RuntimeError("R0.73G figure identity or formal status mismatch")
    figure_git = manifest.get("git", {})
    recorded_figure_commit = figure_git.get(
        "figurePackageCommit",
        figure_git.get(
            "originalFigurePackageCommit",
            figure_git.get("validatedFigureCommit"),
        ),
    )
    if (
        figure_git.get("sourceCommit") != CERTIFIED_REPORT_COMMIT
        or recorded_figure_commit != FIGURE_PACKAGE_COMMIT
        or figure_git.get("certificateCommit") != CERTIFICATE_PACKAGE_COMMIT
    ):
        raise RuntimeError("R0.73G figure provenance chain is inconsistent")
    verify_source_bindings(manifest, "R0.73G figure manifest")
    if not checks_pass(validation):
        raise RuntimeError("R0.73G figure validation is not passed")

    claims = contract.get("claimBoundary", {})
    if claims.get("formalFiniteDiagnosticFigure") is not True:
        raise RuntimeError("R0.73G figure lost formal finite-diagnostic status")
    for key, value in claims.items():
        if key != "formalFiniteDiagnosticFigure" and value is not False:
            raise RuntimeError("R0.73G figure escaped boundary: " + key)

    certificate_outputs = certificate.get("formalFigure")
    if not isinstance(certificate_outputs, dict):
        certificate_outputs = certificate.get("journalFigure")
    if not isinstance(certificate_outputs, dict):
        raise RuntimeError("R0.73G certificate has no figure hash ledger")
    for suffix in ("pdf", "svg", "png"):
        output = require_output_record(manifest, directory, suffix)
        sealed = certificate_outputs.get(suffix)
        if not isinstance(sealed, dict):
            raise RuntimeError(
                "R0.73G certificate figure entry is missing: " + suffix
            )
        current = directory / f"figure.{suffix}"
        if (
            sealed.get("sha256") != digest(current)
            or sealed.get("bytes") != current.stat().st_size
            or output.get("sha256") != sealed.get("sha256")
            or output.get("bytes") != sealed.get("bytes")
        ):
            raise RuntimeError("R0.73G certificate/figure output mismatch: " + suffix)
    if not (directory / "figure.pdf").read_bytes().startswith(b"%PDF"):
        raise RuntimeError("R0.73G formal PDF signature is invalid")
    svg = (directory / "figure.svg").read_text(encoding="utf-8")
    if "<svg" not in svg or "<image" in svg:
        raise RuntimeError("R0.73G formal SVG is absent or rasterized")
    x_density, y_density, unit = png_density(directory / "figure.png")
    if unit != 1 or abs(x_density - 23622) > 100 or abs(y_density - 23622) > 100:
        raise RuntimeError("R0.73G formal PNG is not tagged at 600 dpi")
    png_record = require_output_record(manifest, directory, "png")
    if png_record.get("dpi") not in (None, 600):
        raise RuntimeError("R0.73G figure manifest does not declare 600 dpi")
    validate_publication_assets(manifest, directory)
    return manifest


def validate_inputs() -> tuple[dict, dict]:
    validate_analytic_sources()
    validate_experiment()
    certificate = validate_certificate()
    figure_manifest = validate_figure(certificate)
    return certificate, figure_manifest


def build_note() -> str:
    html = (PUBLIC / "notes/r0-73f.html").read_text(encoding="utf-8")
    metadata = (
        (
            "description",
            r'<meta name="description" content=".*?">',
            '<meta name="description" content="研究笔记 R0.73G：过小种子的非线性相对放大与精确二维全局正则性屏障；自然种子、order-one departure、横向三维与 Clay 仍开放。">',
        ),
        (
            "og title",
            r'<meta property="og:title" content=".*?">',
            '<meta property="og:title" content="R0.73G｜Nonlinear relative amplification and the exact planar barrier">',
        ),
        (
            "og description",
            r'<meta property="og:description" content=".*?">',
            '<meta property="og:description" content="An over-small seed retains nonlinear relative amplification, while the selected orbit stays in a globally regular planar subsystem; natural-scale and transverse-3D claims remain open.">',
        ),
        (
            "og image",
            r'<meta property="og:image" content=".*?">',
            f'<meta property="og:image" content="https://kasifa.github.io/assets/r073g/{FIGURE_ID}.png">',
        ),
        (
            "title",
            r'<title>.*?</title>',
            '<title>R0.73G｜Nonlinear relative amplification and the exact planar barrier</title>',
        ),
    )
    for label, pattern, value in metadata:
        html = section(html, pattern, value, "F note " + label)
    html = required(
        html, "/i18n-en.js?v=1.46", "/i18n-en.js?v=1.47", "F note i18n"
    )
    nav = (
        '<nav><a href="#result">结论</a><a href="#background">精确背景</a>'
        '<a href="#equation">扰动方程</a><a href="#planar">二维屏障</a>'
        '<a href="#launch">光滑启动</a><a href="#bootstrap">强范数闭合</a>'
        '<a href="#remainder">全模态余项</a><a href="#seed">种子上限</a>'
        '<a href="#leakage">行泄漏</a><a href="#false">反例</a>'
        '<a href="#finite">有限诊断</a><a href="#literature">文献</a>'
        '<a href="#audit">审计</a><a href="#figure">附图</a>'
        '<a href="#boundary">边界</a><a href="#value">价值</a>'
        '<a href="#next">下一步</a><a href="#reproduce">复现</a>'
        '<a href="/">返回主页</a></nav>'
    )
    html = section(html, r'<nav><a href="#result">.*?</nav>', nav, "F note nav")
    html = section(html, r'    <header class="hero">.*?</header>', NOTE_HERO, "F note hero")
    toc_items = (
        ("result", "00 · direct decision"),
        ("background", "01 · exact background"),
        ("equation", "02 · full perturbation"),
        ("planar", "03 · exact planar barrier"),
        ("launch", "04 · smooth launch"),
        ("bootstrap", "05 · strong-norm bootstrap"),
        ("remainder", "06 · all-mode remainder"),
        ("seed", "07 · explicit seed ceiling"),
        ("leakage", "08 · exact row leakage"),
        ("false", "09 · exact negative checks"),
        ("finite", "10 · finite diagnostic"),
        ("literature", "11 · literature boundary"),
        ("audit", "12 · independent audit"),
        ("figure", "13 · journal figure"),
        ("boundary", "14 · exact boundary"),
        ("value", "15 · value"),
        ("next", "16 · R0.73H"),
        ("reproduce", "17 · reproduction"),
    )
    toc = (
        '      <aside class="toc"><strong>CONTENTS</strong><ol>\n'
        + "".join(
            f'        <li><a href="#{anchor}">{label}</a></li>'
            for anchor, label in toc_items
        )
        + "\n      </ol></aside>"
    )
    html = section(html, r'      <aside class="toc">.*?</aside>', toc, "F note toc")
    html = section(html, r'      <article>.*?</article>', NOTE_ARTICLE, "F note article")
    footer = (
        "<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>"
        "我按原编号记录推导、反例和未解决的问题。</div>"
        '<div>研究笔记 R0.73G · 2026-08-30<br><a href="/">返回研究主页</a></div></footer>'
    )
    html = section(html, r"<footer>.*?</footer>", footer, "F note footer")
    note_nav = re.search(r"<nav>(.*?)</nav>", html, flags=re.S)
    nav_anchors = (
        re.findall(r'href="#([^"]+)"', note_nav.group(1))
        if note_nav is not None else []
    )
    expected_anchors = [anchor for anchor, _ in toc_items]
    if nav_anchors != expected_anchors or len(nav_anchors) != len(set(nav_anchors)):
        raise RuntimeError("R0.73G note nav anchors are not unique and ordered")
    assert_clean(html, "R0.73G note")
    assert_mathjax_clean(html, "R0.73G note")
    assert_public_voice(html, "R0.73G note")
    return html


def build_recap() -> str:
    html = (PUBLIC / "recap-r0-61-r0-73f.html").read_text(encoding="utf-8")
    metadata = (
        (
            "description",
            r'<meta name="description" content=".*?">',
            '<meta name="description" content="R0.60 之后的完整研究回顾：R0.61 到 R0.73G 共 123 个节点；最新一节闭合过小种子的非线性相对放大，并证明所选轨道受精确二维全局正则性屏障约束。">',
        ),
        (
            "og title",
            r'<meta property="og:title" content=".*?">',
            '<meta property="og:title" content="R0.61–R0.73G｜R0.60 之后的研究回顾">',
        ),
        (
            "og description",
            r'<meta property="og:description" content=".*?">',
            '<meta property="og:description" content="四十二个阶段、123 个节点：从约化递推和环带排除到过小种子的非线性相对放大与精确二维屏障。">',
        ),
        (
            "title",
            r"<title>.*?</title>",
            "<title>R0.61–R0.73G｜R0.60 之后的研究回顾</title>",
        ),
    )
    for label, pattern, value in metadata:
        html = section(html, pattern, value, "F recap " + label)
    html = required(
        html, "/i18n-en.js?v=1.46", "/i18n-en.js?v=1.47", "F recap i18n"
    )
    hero = r'''    <header class="hero"><div class="hero-inner"><div><div class="eyebrow">累计回顾 · R0.61–R0.73G · 2026-08-30</div><h1>R0.60 之后的研究回顾</h1><p class="lead">这页保留 R0.61 到 R0.73G 的全部 123 个节点。R0.61–R0.69W 从约化递推走到严格环带排除；R0.70A–R0.71Z 检查移动尺度、临界账本、内部 entry 与 complete-root 边界；R0.72A–R0.73B 处理 strong coupling、critical log、碰撞几何与完整线性 Fourier--Leray 行；R0.73C–F 依次认证冻结 Rayleigh 不稳定、黏性谱簇持续、固定正半平面传递和移动剖面固定窗口增益。R0.73G 把该一行线性下界升级为一个过小种子的非线性相对放大定理，同时证明所选真实轨道严格留在全局光滑的二维不变子空间。自然种子、order-one departure、横向三维与 Clay 没有被外推。</p></div><div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.73G</strong><p>收录节点：123</p><p>回顾截止时公开笔记：183</p><p>回顾截止节点：R0.73G</p><p>问题状态：仍未解决</p></div></div></header>'''
    html = section(html, r'    <header class="hero">.*?</header>', hero, "F recap hero")
    for old, new in (
        ("02 · 122 节完整索引", "02 · 123 节完整索引"),
        ("01 · 四十一个研究阶段", "01 · 四十二个研究阶段"),
        ("R0.60 之后的路线分成四十一个阶段", "R0.60 之后的路线分成四十二个阶段"),
        ('data-current-route="R0.69P–R0.73F"', 'data-current-route="R0.69P–R0.73G"'),
    ):
        html = required(html, old, new, "F recap counter")
    result = r'''        <section id="result"><div class="section-no">00 / 回顾范围</div><h2>版本数、封存数和数学结论分开报告</h2><div class="metrics"><div class="metric"><strong>123</strong><span>R0.61–R0.73G 研究节点</span></div><div class="metric"><strong>85</strong><span>R0.70A–R0.73G 已公开版本</span></div><div class="metric"><strong>61</strong><span>当前 formal-figure 合同下完整封存</span></div><div class="metric"><strong>24</strong><span>旧版附图档案待回补</span></div></div><p>R0.00–R0.60 保留在上一份阶段回顾。R0.70A–R0.73G 的 85 个版本已经公开，其中 61 个满足当前完整封存合同，24 个历史版本仍欠 formal-figure 回补。公开和封存不表示 Clay 问题已经解决。</p></section>'''
    html = section(html, r'        <section id="result">.*?</section>', result, "F recap result")
    phase = r'''            <article class="phase"><h3>R0.73G · Nonlinear relative amplification and the exact planar barrier</h3><p>R0.73F 的一行移动剖面下界进入完整 Navier--Stokes 扰动方程。显式 \(H^3\) Riccati bootstrap 与不选择 Fourier 行的 \(L^2\) 余项能量估计，对一个指数级过小种子保留至少一半线性相对增益。</p><p>同一真实共轭 launch 严格属于二维不变子空间，完整轨道因周期二维 Navier--Stokes 全局正则性而全局光滑。第一轮卷积产生 \(K_z=0,\pm2\)，所以单一行并非非线性不变；有限诊断只复核成本与泄漏，不承担 continuum proof。</p><p>__CLOSED__。__FALSE__。__OPEN__。</p><div class="links"><a href="/notes/r0-73g.html">R0.73G</a><a href="/assets/r073g/__FIGURE_ID__.pdf">R0.73G 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073g">R0.73G 证书</a></div></article>
'''.replace("__CLOSED__", CLOSED).replace("__FALSE__", FALSE).replace("__OPEN__", OPEN).replace("__FIGURE_ID__", FIGURE_ID)
    marker = '          </div>\n        </section>\n\n        <section id="node-index">'
    html = once(html, marker, phase + marker, "F recap phase")
    html = required(
        html,
        "R0.61–R0.73F 的 122 节公开笔记",
        "R0.61–R0.73G 的 123 节公开笔记",
        "F recap node title",
    )
    node_e = '            <span class="node-ref"><a href="/notes/r0-73f.html">R0.73F</a><span class="node-state kind-closed">闭</span></span>\n'
    node_f = '            <span class="node-ref"><a href="/notes/r0-73g.html">R0.73G</a><span class="node-state kind-closed">闭</span></span>\n'
    html = once(html, node_e, node_e + node_f, "F recap node")
    retained = '            <li>R0.73G 对一个显式过小种子闭合完整方程中的非线性相对放大，同时证明所选轨道留在全局光滑二维子空间；自然种子、order-one departure、横向三维与 Clay 保持 OPEN。</li>\n'
    html = once(
        html,
        "          </ul>\n          <p>这些结果可以分别整理成",
        retained + "          </ul>\n          <p>这些结果可以分别整理成",
        "F recap retained",
    )
    value = r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>过小种子的非线性相对增益已成为定理；所选轨道同时受二维正则性屏障约束</h2><p>不能把 123 个节点或 85 个公开版本解释成 Clay 完成比例。R0.73G 的严格增量是 conditional exact nonlinear relative-amplification theorem，并非自然尺度的 order-one instability，也不含横向三维 vortex stretching 或奇性结论。</p></section>'''
    html = section(html, r'        <section id="value">.*?</section>', value, "F recap value")
    next_gate = r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.73H 检查自然种子的 harmonic-resolved 余项与横向三维接口</h2><p>先分离 even 二阶响应与 odd 三阶反馈，检验 \(e^{-\kappa_D\Lambda}\) 自然种子能否达到 order one；再冻结 \(K_x\ne0\) 或非零第一速度分量的 transverse coupling。</p></section>'''
    html = section(html, r'        <section id="next">.*?</section>', next_gate, "F recap next")
    claims = (
        r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2><p>R0.70A–R0.73G 的 85 节已公开；61 节完整封存；24 节旧档待回补。</p><p>__CLOSED__。</p><p>__FALSE__。</p><p>__OPEN__。</p></section>'''
        .replace("__CLOSED__", CLOSED)
        .replace("__FALSE__", FALSE)
        .replace("__OPEN__", OPEN)
    )
    html = section(html, r'        <section id="claims">.*?</section>', claims, "F recap claims")
    reproduce = r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证明、审计、证书、有限诊断、附图和历史回顾</h2><p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-73f.html">保留 R0.73F 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-73g.html">打开最新节点 R0.73G</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073g_nonlinear_shadowing_proof.md">查看 R0.73G 证明</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073g_operator_derivation.md">查看独立算子推导</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073g_independent_analytic_audit.md">查看独立解析审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073g">查看正式证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/experiments/r073g">查看有限诊断与监控记录</a> · <a href="/assets/r073g/__FIGURE_ID__.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-73g.pdf">下载同步 PDF</a></p><p>continuum theorem 来自解析证明与两份解析审计。Fourier cutoff 只做诊断和附图。</p></section>'''.replace("__FIGURE_ID__", FIGURE_ID)
    html = section(html, r'        <section id="reproduce">.*?</section>', reproduce, "F recap reproduce")
    footer = '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>我按原编号记录推导、反例和未解决的问题。</div><div>R0.61–R0.73G 回顾 · 2026-08-30<br><a href="/">返回研究主页</a></div></footer>'
    html = section(html, r"<footer>.*?</footer>", footer, "F recap footer")
    start = html.index('<section id="node-index">')
    end = html.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', html[start:end])
    if len(links) != 123 or len(set(links)) != 123:
        raise RuntimeError("R0.73G recap expected 123 unique nodes")
    if html.count('<article class="phase">') != 42:
        raise RuntimeError("R0.73G recap expected 42 phases")
    if "R0.60 之后的研究回顾" not in html or ">R0.61<" not in html:
        raise RuntimeError("R0.73G recap must start after R0.60, at R0.61")
    assert_clean(html, "R0.73G recap")
    assert_mathjax_clean(html, "R0.73G recap", check_naked=False)
    assert_public_voice(html, "R0.73G recap")
    return html


def update_home() -> str:
    html = (PUBLIC / "research-review.html").read_text(encoding="utf-8")
    html = section(
        html,
        r'    <section class="route-overview latest-release-spotlight".*?</section>',
        HOME_LATEST_SPOTLIGHT,
        "F home latest spotlight",
    )
    for old, new in (
        ('data-site-version="1.46"', 'data-site-version="1.47"'),
        ("/i18n-en.js?v=1.46", "/i18n-en.js?v=1.47"),
        ("/site-refresh.js?v=1.46", "/site-refresh.js?v=1.47"),
        ("<strong>v1.46</strong>网页版本", "<strong>v1.47</strong>网页版本"),
        ("<strong>182</strong>公开研究笔记", "<strong>183</strong>公开研究笔记"),
        ("<strong>R0.73F</strong>最新研究节点", "<strong>R0.73G</strong>最新研究节点"),
        (
            '<a class="route-map-latest" href="#r073f">跳到首页 R0.73F 卡片 →</a>',
            '<a class="route-map-latest" href="#r073g">跳到首页 R0.73G 卡片 →</a>',
        ),
        (
            "nonlinear seed / Sobolev topology / lifespan / mode-convolution remainder",
            "natural seed / harmonic remainder / transverse 3D coupling",
        ),
        ("Research topology · R0.1–R0.73F", "Research topology · R0.1–R0.73G"),
        (
            "R0.70A–R0.73F：84 节已公开，60 节完整封存",
            "R0.70A–R0.73G：85 节已公开，61 节完整封存",
        ),
        (
            '<span class="route-range">R0.69P–R0.73F</span>',
            '<span class="route-range">R0.69P–R0.73G</span>',
        ),
        ('aria-label="R0.69P–R0.73F"', 'aria-label="R0.69P–R0.73G"'),
        ("展开 92 篇公开笔记", "展开 93 篇公开笔记"),
        ("本站 R0.69P–R0.73F 路线", "本站 R0.69P–R0.73G 路线"),
        ("综述 v1.46 · 2026-08-30", "综述 v1.47 · 2026-08-30"),
        ("上次综述 v1.45 · 2026-08-30", "上次综述 v1.46 · 2026-08-30"),
    ):
        html = required(html, old, new, "F home " + old)
    html = replace_all(
        html,
        "/recap-r0-61-r0-73f.html",
        "/recap-r0-61-r0-73g.html",
        "F home recap HTML links",
    )
    html = replace_all(
        html,
        "/recap-r0-61-r0-73f.pdf",
        "/recap-r0-61-r0-73g.pdf",
        "F home recap PDF links",
    )
    historical = '<strong style="color:var(--gold)">下一步 R0.73G：</strong>&nbsp;冻结并审计精确衰减剪切流附近的非线性 bootstrap，明确 seed size、Sobolev topology、lifespan 与 mode-convolution remainder。'
    html = required(
        html,
        historical,
        historical.replace("下一步", "当时的下一步"),
        "F home historical E next",
    )
    focus = r'<div class="summary-item"><strong>我目前关注</strong><span>R0.73G 已对一个显式过小种子闭合非线性相对放大，并证明所选轨道严格留在全局光滑的二维不变子空间。下一关检查自然种子的 harmonic-resolved 余项与 transverse 3D coupling。</span></div>'
    html = section(
        html,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        focus,
        "F home focus",
    )
    html = required(
        html,
        "<h3>R0.73F：移动剖面二分与固定窗口指数增益已闭合</h3>",
        "<h3>R0.73G：过小种子的非线性相对放大与精确二维屏障已闭合</h3>",
        "F home current title",
    )
    html = required(
        html,
        "<span>R0.72R–R0.73F：</span>",
        "<span>R0.72R–R0.73G：</span>",
        "F home path range",
    )
    html = required(
        html,
        "certified frozen Rayleigh instability → static viscous cluster persistence → fixed-half-plane logarithmic transfer → moving-profile fixed-window dichotomy</p>",
        "certified frozen Rayleigh instability → static viscous cluster persistence → fixed-half-plane logarithmic transfer → moving-profile fixed-window dichotomy → over-small-seed nonlinear relative amplification / exact planar barrier</p>",
        "F home path tail",
    )
    link_e = '<a class="milestone" href="/notes/r0-73f.html">R0.73F</a>'
    html = once(
        html,
        link_e,
        link_e + '\n                  <a class="milestone" href="/notes/r0-73g.html">R0.73G</a>',
        "F home route link",
    )
    route_f = '              <p>R0.73G 用显式 \\(H^3\\) bootstrap 和全模态 \\(L^2\\) 余项估计，把 R0.73F 的一行下界升级为一个过小种子的非线性相对放大。所选真实轨道同时严格留在全局光滑的二维不变子空间；自然种子、order-one departure、横向三维与 Clay 保持 OPEN。</p>\n'
    html = once(
        html,
        '              <details class="tree-notes" open>',
        route_f + '              <details class="tree-notes" open>',
        "F home route summary",
    )
    html = section(
        html,
        r'            <article class="tree-node next">.*?</article>',
        HOME_NEXT,
        "F home next",
    )
    recap = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem"><p class="eyebrow">累计回顾 R0.61–R0.73G · 2026-08-30</p><h3>R0.60 recap 之后的累计回顾收录 123 个节点；全站现有 183 篇公开研究笔记</h3><p>累计回顾现分四十二个阶段，完整保留 R0.61–R0.73G；最新节点分开记录 exact nonlinear theorem、planar barrier、finite diagnostic、文献边界和 open gate。</p><p>R0.70A–R0.73G 共 85 个版本已公开；61 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p><p><strong>阶段判断：</strong>&nbsp;过小种子的非线性相对放大与所选轨道的精确二维全局正则性屏障已闭合；自然种子、order-one departure、横向三维与 Clay 保持 OPEN。</p><p><a href="/recap-r0-61-r0-73g.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-73g.pdf">下载同步 PDF</a></p></div>'''
    html = section(
        html,
        r'          <div class="task-one" id="post-r060-recap".*?</div>',
        recap,
        "F home recap",
    )
    marker = '          </div>\n        </section>\n\n      </article>'
    html = once(
        html,
        marker,
        '          </div>\n\n' + HOME_G_CARD + '\n        </section>\n\n      </article>',
        "F home card",
    )
    if html.count('data-release="r073g"') != 1:
        raise RuntimeError("home must contain exactly one R0.73G card")
    if html.count('<strong style="color:var(--gold)">下一步 R0.73H：') != 1:
        raise RuntimeError("home must contain exactly one current R0.73H gate")
    route = re.search(
        r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73G">'
        r"(.*?)</nav>",
        html,
        flags=re.S,
    )
    if route is None or len(re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))) != 93:
        raise RuntimeError("home current-route index must contain 93 note links")
    assert_clean(html, "R0.73G home")
    assert_mathjax_clean(html, "R0.73G home", check_naked=False)
    assert_public_voice(html, "R0.73G home")
    return html


def update_literature() -> str:
    html = (PUBLIC / "literature-review.html").read_text(encoding="utf-8")
    for old, new in (
        ("/i18n-en.js?v=1.46", "/i18n-en.js?v=1.47"),
        (
            "本站 R0.69P–R0.73F 只列为研究笔记",
            "本站 R0.69P–R0.73G 只列为研究笔记",
        ),
        ("文献综述 v1.46 · 2026-08-30", "文献综述 v1.47 · 2026-08-30"),
        ("累计回顾与 122 节索引", "累计回顾与 123 节索引"),
        ("打开 122 节完整索引", "打开 123 节完整索引"),
    ):
        html = required(html, old, new, "F literature " + old)
    html = replace_all(
        html,
        "/recap-r0-61-r0-73f.html",
        "/recap-r0-61-r0-73g.html",
        "F literature recap links",
    )
    old_open = r'<div class="route-step pause"><header><b>开放接口 · R0.73G</b><strong>nonlinear perturbation bootstrap near the exact decaying shear</strong></header><p>冻结 seed size、Sobolev topology、lifespan 与 mode-convolution remainder，证明 bootstrap 闭合或给出否定障碍。</p></div>'
    new_steps = r'''<div class="route-step kept"><header><b>R0.73G</b><strong>nonlinear relative amplification and the exact planar barrier</strong></header><p>显式过小种子上的 \(H^3\) bootstrap 与全模态 \(L^2\) 余项估计保留至少一半线性相对增益；同一轨道严格留在全局光滑的二维不变子空间。<a href="/notes/r0-73g.html">研究笔记</a> <a href="/recap-r0-61-r0-73g.html">当前累计回顾</a> <a href="#r073g-boundary">文献边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.73H</b><strong>natural seed, harmonic remainder, and transverse 3D coupling</strong></header><p>分离 even 二阶响应与 odd 三阶反馈，检验自然种子的 order-one departure；再建立 \(K_x\ne0\) 或非零第一速度分量的横向三维接口。</p></div>'''
    html = once(html, old_open, new_steps, "F literature route")
    boundary = r'''

          <h3 id="r073g-boundary">R0.73G 的非线性 bootstrap、二维屏障与有限诊断边界</h3>
          <p><a href="https://doi.org/10.1007/s00220-006-1526-7">Friedlander--Pavlović--Shvydkoy 2006</a>给出 steady autonomous Navier--Stokes 的解析半群 bootstrap；<a href="https://doi.org/10.1002/1097-0312%28200009%2953%3A9%3C1067%3A%3AAID-CPA1%3E3.0.CO%3B2-Q">Grenier 2000</a>与<a href="https://numdam.org/item/AIHPC_2003__20_1_87_0/">Desjardins--Grenier 2003</a>展示高阶 corrector、interaction algebra 和 residual control 的额外义务。<a href="https://doi.org/10.1007/s40818-019-0074-3">Grenier--Nguyen 2019</a>处理带边界层、解析性与小外力的热演化剖面；<a href="https://doi.org/10.1007/s00332-016-9330-9">Bedrossian--Vicol--Wang 2018</a>属于近 Couette 稳定区。R0.73G 的证明自包含；这些文献不替代过小种子估计，也不提供自然尺度、横向三维或 Clay 结论。本节不作原创性或优先权声明。</p>
          <div class="boundary"><strong>R0.73G 的主张边界</strong><p>__CLOSED__。</p><p>__FALSE__。</p><p>__OPEN__。有限 Fourier 数据不承担 continuum proof。</p></div>'''
    boundary = (
        boundary
        .replace("__CLOSED__", CLOSED)
        .replace("__FALSE__", FALSE)
        .replace("__OPEN__", OPEN)
    )
    match = re.search(
        r'(<h3 id="r073f-boundary">.*?<div class="boundary">.*?</div>)',
        html,
        flags=re.S,
    )
    if match is None:
        raise RuntimeError("F literature expected R0.73F boundary")
    html = once(
        html, match.group(1), match.group(1) + boundary, "F literature boundary"
    )
    references = r'''            <li id="ref-125">S. Friedlander, N. Pavlović and R. Shvydkoy. <a href="https://doi.org/10.1007/s00220-006-1526-7"><em>Nonlinear instability for the Navier--Stokes equations</em></a>. Communications in Mathematical Physics 264 (2006), 335--347.</li>
            <li id="ref-126">E. Grenier. <a href="https://doi.org/10.1002/1097-0312%28200009%2953%3A9%3C1067%3A%3AAID-CPA1%3E3.0.CO%3B2-Q"><em>On the nonlinear instability of Euler and Prandtl equations</em></a>. Communications on Pure and Applied Mathematics 53 (2000), 1067--1091.</li>
            <li id="ref-127">B. Desjardins and E. Grenier. <a href="https://numdam.org/item/AIHPC_2003__20_1_87_0/"><em>Linear instability implies nonlinear instability for various types of viscous boundary layers</em></a>. Annales de l'Institut Henri Poincaré C 20 (2003), 87--106.</li>
            <li id="ref-128">Z. Lin and C. Zeng. <a href="https://doi.org/10.1002/cpa.21457"><em>Unstable Manifolds of Euler Equations</em></a>. Communications on Pure and Applied Mathematics 66 (2013), 1803--1836; <a href="https://doi.org/10.1002/cpa.21521">corrigendum</a>.</li>
            <li id="ref-129">E. Grenier and T. T. Nguyen. <a href="https://doi.org/10.1007/s40818-019-0074-3"><em>L-infinity instability of Prandtl layers</em></a>. Annals of PDE 5 (2019), article 18.</li>
            <li id="ref-130">J. Bedrossian, V. Vicol and F. Wang. <a href="https://doi.org/10.1007/s00332-016-9330-9"><em>The Sobolev stability threshold for 2D shear flows near Couette</em></a>. Journal of Nonlinear Science 28 (2018), 2051--2075.</li>
            <li id="ref-131">J. Bedrossian, P. Germain and N. Masmoudi. <a href="https://annals.math.princeton.edu/2017/185-2/p04"><em>On the stability threshold for the 3D Couette flow in Sobolev regularity</em></a>. Annals of Mathematics 185 (2017), 541--608.</li>
            <li id="ref-132">M. Colombo, M. Dolce, R. Montalto and P. Ventura. <a href="https://arxiv.org/abs/2509.18070"><em>Long-wave instability of periodic shear flows for the 2D Navier--Stokes equations</em></a>. Current preprint (2025).</li>
            <li id="ref-133">D. Bian and E. Grenier. <a href="https://arxiv.org/abs/2206.01318"><em>Onset of nonlinear instabilities in monotonic viscous boundary layers</em></a>. Preprint heuristic/conjecture (2022).</li>
'''
    html = once(
        html,
        '          </ol>\n          <p class="source-note">',
        references + '          </ol>\n          <p class="source-note">',
        "F literature references",
    )
    terminal = "R0.73F 再用有界扰动 roughness、精确 clamped profile 与移动不稳定束闭合一条精确线性行的 fixed-window exponential lower law；finite diagnostic、完整全行、nonlinear 与 Clay 边界保持分离。"
    terminal_f = terminal + "R0.73G 再用显式强范数 bootstrap 与全模态余项能量估计，把该一行下界升级为过小种子的 nonlinear relative amplification；所选真实轨道严格留在全局光滑二维子空间。自然种子、order-one departure、横向三维与 Clay 保持 OPEN。"
    html = required(html, terminal, terminal_f, "F literature deck terminal")
    assert_clean(html, "R0.73G literature")
    assert_mathjax_clean(html, "R0.73G literature", check_naked=False)
    assert_public_voice(html, "R0.73G literature")
    return html


def build_manifest_outputs() -> dict[Path, bytes]:
    release_path = ROOT / "research/release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    for key, value in R073F_RELEASE_BASELINE.items():
        if release.get(key) != value:
            raise RuntimeError("release manifest changed during generation: " + key)
    release.update({
        **R073G_RELEASE_TARGET,
        "latestReleaseGate": "tests/r073g-nonlinear-bootstrap-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r073g-release.test.mjs",
    })
    release.pop("nextReleaseSourceStage", None)

    site_path = PUBLIC / "site-version.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    if site != {
        "schemaVersion": "research-site-version-v1",
        "version": "1.46",
        "latestRelease": "R0.73F",
        "publicHtmlNoteCount": 182,
        "publishedDate": "2026-08-30",
    }:
        raise RuntimeError("site-version changed during R0.73G generation")
    site.update({
        "version": "1.47",
        "latestRelease": "R0.73G",
        "publicHtmlNoteCount": 183,
        "publishedDate": "2026-08-30",
    })

    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    state = (
        inventory.get("latestPublishedRelease"),
        inventory.get("publishedReleaseCount"),
        inventory.get("formalSealedReleaseCount"),
        inventory.get("legacyFormalFigureBacklogCount"),
    )
    if state != ("r073f", 84, 60, 24):
        raise RuntimeError("formal archive changed during R0.73G generation")
    for key in ("publishedReleases", "formalSealedReleases"):
        if inventory[key][-1] != "r073f" or "r073g" in inventory[key]:
            raise RuntimeError("formal archive is not append-only: " + key)
        inventory[key].append("r073g")
    inventory.update({
        "latestPublishedRelease": "r073g",
        "publishedReleaseCount": 85,
        "formalSealedReleaseCount": 61,
        "legacyFormalFigureBacklogCount": 24,
    })
    if (
        len(inventory["publishedReleases"]) != 85
        or len(inventory["formalSealedReleases"]) != 61
    ):
        raise RuntimeError("formal archive count mismatch after R0.73G")
    inventory_payload = json_bytes(inventory)
    release["formalArchiveInventory"] = {
        "path": "research/formal-archive-inventory.json",
        "sha256": sha256_bytes(inventory_payload),
    }
    return {
        release_path: json_bytes(release),
        site_path: json_bytes(site),
        inventory_path: inventory_payload,
        ROOT / "VERSION": b"1.47\n",
    }


def build_note_index(site_payload: bytes) -> str:
    import generate_note_index as note_index

    existing = [note_index.parse_note(path) for path in note_index.note_files()]
    if len(existing) != 182 or any(note.slug == "r0-73g" for note in existing):
        raise RuntimeError("R0.73G note-index baseline is not exact")
    latest = note_index.Note(
        slug="r0-73g",
        code="R0.73G",
        title="Nonlinear relative amplification and the exact planar barrier",
        major=73,
        has_pdf=False,
    )
    notes = [latest] + existing
    target_site = json.loads(site_payload.decode("utf-8"))
    old_json = note_index.json
    old_latest_recap_href = note_index.latest_recap_href

    class TargetJson:
        @staticmethod
        def loads(_payload: str) -> dict:
            return target_site

    try:
        note_index.json = TargetJson
        note_index.latest_recap_href = lambda: "/recap-r0-61-r0-73g.html"
        index = note_index.render(notes)
    finally:
        note_index.json = old_json
        note_index.latest_recap_href = old_latest_recap_href
    for token in (
        'data-site-version="1.47"',
        "183 篇公开研究笔记",
        "<strong>R0.73G</strong><span>最新研究节点</span>",
        'data-note="r0-73g"',
        "/recap-r0-61-r0-73g.html",
        "研究笔记总索引 · v1.47 · 2026-08-30",
    ):
        if token not in index:
            raise RuntimeError("R0.73G note index missing token: " + token)
    assert_clean(index, "R0.73G note index")
    assert_public_voice(index, "R0.73G note index")
    return index


def stage_figure_assets(
    staged: dict[Path, bytes],
    figure_manifest: dict,
) -> None:
    source = ROOT / FIGURE_RELATIVE
    target = PUBLIC / "assets/r073g"
    rows = figure_manifest.get("outputs")
    if not isinstance(rows, list):
        rows = figure_manifest.get("figure", {}).get("outputs", [])
    output_hashes = {
        Path(str(row["path"])).name: row["sha256"]
        for row in rows
    }
    for suffix in ("pdf", "svg", "png"):
        name = f"figure.{suffix}"
        payload = (source / name).read_bytes()
        if sha256_bytes(payload) != output_hashes.get(name):
            raise RuntimeError("R0.73G public figure source is not manifest-bound")
        staged[target / f"{FIGURE_ID}.{suffix}"] = payload


def validate_staged(staged: dict[Path, bytes]) -> None:
    required_paths = (
        PUBLIC / "notes/r0-73g.html",
        PUBLIC / "recap-r0-61-r0-73g.html",
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
            raise RuntimeError("R0.73G transaction is missing staged path " + str(path))
    for path in staged:
        if path.suffix.lower() == ".pdf" and "assets/r073g" not in path.as_posix():
            raise RuntimeError("R0.73G HTML transaction must not generate PDFs")
    for path in (
        PUBLIC / "notes/r0-73g.html",
        PUBLIC / "recap-r0-61-r0-73g.html",
        PUBLIC / "research-review.html",
        PUBLIC / "literature-review.html",
        PUBLIC / "notes/index.html",
    ):
        value = staged[path].decode("utf-8")
        assert_clean(value, path.name)
        assert_mathjax_clean(value, path.name, check_naked=False)
        assert_public_voice(value, path.name)
    note = staged[PUBLIC / "notes/r0-73g.html"].decode("utf-8")
    for token in (CLOSED, FALSE, OPEN, "EXACT NONLINEAR THEOREM", "NOT CLAY"):
        if token not in note:
            raise RuntimeError("R0.73G staged note lost boundary token")
    recap = staged[PUBLIC / "recap-r0-61-r0-73g.html"].decode("utf-8")
    start = recap.index('<section id="node-index">')
    end = recap.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', recap[start:end])
    if len(links) != 123 or len(set(links)) != 123:
        raise RuntimeError("R0.73G staged recap node inventory is invalid")
    if recap.count('<article class="phase">') != 42:
        raise RuntimeError("R0.73G staged recap phase inventory is invalid")
    home = staged[PUBLIC / "research-review.html"].decode("utf-8")
    route = re.search(
        r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73G">'
        r"(.*?)</nav>",
        home,
        flags=re.S,
    )
    if route is None or len(re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))) != 93:
        raise RuntimeError("R0.73G staged home route inventory is invalid")


def write_temp_for(path: Path, payload: bytes, mode: int) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix="." + path.name + ".r073g-",
        dir=path.parent,
    )
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
    backups: dict[Path, bytes | None] = {
        path: path.read_bytes() if path.is_file() else None
        for path in ordered
    }
    modes = {
        path: (path.stat().st_mode & 0o777) if path.exists() else 0o644
        for path in ordered
    }
    temporary: dict[Path, Path] = {}
    replaced: list[Path] = []
    try:
        for path in ordered:
            if ROOT not in path.resolve().parents:
                raise RuntimeError("transaction target escaped repository: " + str(path))
            temporary[path] = write_temp_for(path, staged[path], modes[path])
        for path in ordered:
            os.replace(temporary[path], path)
            replaced.append(path)
        for path, payload in staged.items():
            if path.read_bytes() != payload:
                raise RuntimeError("transaction readback mismatch: " + str(path))
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


def main() -> None:
    preflight_release_state()
    _, figure_manifest = validate_inputs()

    staged: dict[Path, bytes] = {}
    stage_figure_assets(staged, figure_manifest)
    staged[PUBLIC / "notes/r0-73g.html"] = build_note().encode("utf-8")
    staged[PUBLIC / "recap-r0-61-r0-73g.html"] = build_recap().encode("utf-8")
    staged[PUBLIC / "research-review.html"] = update_home().encode("utf-8")
    staged[PUBLIC / "literature-review.html"] = update_literature().encode("utf-8")
    manifest_outputs = build_manifest_outputs()
    staged.update(manifest_outputs)
    staged[PUBLIC / "notes/index.html"] = build_note_index(
        staged[PUBLIC / "site-version.json"]
    ).encode("utf-8")
    validate_staged(staged)
    commit_transaction(staged)

    if len(list((PUBLIC / "notes").glob("r0-*.html"))) != 183:
        raise RuntimeError("R0.73G postcommit note count is not 183")
    source = ROOT / FIGURE_RELATIVE
    target = PUBLIC / "assets/r073g"
    for suffix in ("pdf", "svg", "png"):
        if digest(source / f"figure.{suffix}") != digest(
            target / f"{FIGURE_ID}.{suffix}"
        ):
            raise RuntimeError(
                "R0.73G public figure is not byte-identical: " + suffix
            )
    print(json.dumps({
        "release": "R0.73G",
        "siteVersion": "1.47",
        "notes": 183,
        "recapNodes": 123,
        "published": 85,
        "formalSealed": 61,
        "legacyBacklog": 24,
        "phases": 42,
        "routeNotes": 93,
        "next": "R0.73H",
        "rootVersion": "1.47",
        "pdfGenerated": False,
        "translationsGenerated": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
