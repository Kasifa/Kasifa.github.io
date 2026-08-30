#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the fail-closed transactional R0.73F GitHub Pages release."""

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
from r073f_release_content import (
    CERTIFICATE_RELATIVE,
    CLOSED,
    EXPERIMENT_RELATIVE,
    FALSE,
    FIGURE_ID,
    FIGURE_RELATIVE,
    HOME_F_CARD,
    HOME_LATEST_SPOTLIGHT,
    HOME_NEXT,
    NOTE_ARTICLE,
    NOTE_HERO,
    OPEN,
    R073E_RELEASE_BASELINE,
    R073F_RELEASE_TARGET,
)

ROOT = Path(os.environ.get(
    "R073F_RELEASE_ROOT", Path(__file__).resolve().parents[1]
)).resolve()
PUBLIC = ROOT / "public"

CERTIFIED_REPORT_COMMIT = "5edb1702314feca3e9d47a186b30fc53079cd67a"
FIGURE_PACKAGE_COMMIT = "3a34494445de938c5cf01862b1db258e6a6d5ecf"
CERTIFICATE_PACKAGE_COMMIT = "5f9c21f5443e5d5b7350a6d71df8ba417890291c"
FIGURE_METADATA_SEAL_COMMIT = "b17905719d2293a8d356fd94ffcd086554075e75"
FIGURE_PUBLICATION_COMMIT = "affbd8c744f69cbc12183cbea82d4ee5be48b2a9"
CERTIFICATE_COMMIT_PLACEHOLDER = "TO_BE_FILLED_AFTER_CERTIFICATE_COMMIT"
FIGURE_SEAL_COMMIT_PLACEHOLDER = "TO_BE_FILLED_AFTER_FIGURE_SEAL_COMMIT"

CLOSED_KEYS = (
    "boundedPerturbationRoughnessWithNoninvertibleStableSemigroup",
    "movingProfileUniformSpectralStrip",
    "movingProfileUniformContour",
    "movingInstantaneousProjectionNormC1",
    "movingProfileEvolutionDichotomy",
    "movingUnstableFiberStartsAtFrozenTopSpace",
    "fixedSmallEndpointExponentialLowerLaw",
    "fixedWindowExponentialLowerLaw",
    "fixedWindowLogGainThetaLambda",
)

FALSE_KEYS = (
    "frozenSpectralGapImpliesUniformDichotomy",
    "spectralGapPlusBoundedC1PlusCommonDomainImpliesMovingDichotomy",
    "instantaneousPositiveSpectralAbscissaImpliesFixedWindowGrowth",
)

OPEN_KEYS = (
    "explicitWindowSize",
    "sharpExponentialRate",
    "normalizedLogGainLimitExists",
    "arbitraryEndpointBeyondSmallWindow",
    "dynamicProjectionEqualsInstantaneousRieszProjection",
    "graphDomainKatoTransport",
    "singleEpsilonIndependentInitialOrbit",
    "certifiedSigmaStarIsRightmost",
    "inviscidEigenvalueSimple",
    "completeOSSquireA2DirectSum",
    "matchingFixedWindowLowerAcrossAllRows",
    "nonlinearNavierStokes",
    "Clay",
)

# The certificate uses a canonical machine-facing ledger that is deliberately
# distinct from the reader-facing report/gap tokens above.  In particular,
# one certificate shortcut covers two related FALSE rows in the public ledger.
CERTIFICATE_FALSE_SHORTCUT_KEYS = (
    "positiveInstantaneousSpectralAbscissaImpliesFixedWindowGrowth",
    "spectralGapPlusCommonDomainImpliesUniformMovingDichotomy",
)

CERTIFICATE_OPEN_KEYS = (
    "Clay",
    "arbitraryEndpointBeyondSmallWindow",
    "certifiedSigmaStarIsRightmost",
    "completeOSSquireA2DirectSum",
    "dynamicProjectionEqualsInstantaneousRieszProjection",
    "explicitWindowSize",
    "graphDomainKatoTransport",
    "inviscidEigenvalueSimple",
    "nonlinearNavierStokes",
    "normalizedLogGainLimitExists",
    "sharpExponentialRate",
    "singleEpsilonIndependentInitialOrbit",
)

CERTIFICATE_BOUNDARY_ONLY_KEYS = (
    "counterexamplesDescribeExactFourierRow",
    "diagnosticDIsCertifiedD0",
    "finiteDiagnosticProvesContinuumTheorem",
)

SOURCE_PATHS = (
    "research/r073f_problem_freeze.md",
    "research/r073f_moving_dichotomy_proof.md",
    "research/r073f_report-source.md",
    "research/r073f_gap_matrix.md",
    "research/r073f_literature_audit.md",
    "research/r073f_independent_analytic_audit.md",
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
        "outputBindings",
        "packageBindings",
        "packageSourceBindings",
        "contentBindings",
        "files",
        "analyticSourceBindings",
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
        raise RuntimeError(label + ": source binding inventory is not exactly six files")
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
        raise RuntimeError("R0.73F F inventory must contain exactly 14 immutable files")
    verify_named_files_at_commit(
        directory,
        FIGURE_METADATA_SEAL_COMMIT,
        FIGURE_METADATA_CORE_FILES,
        "R0.73F figure metadata core",
    )

    manifest_path = directory / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if "publication" not in manifest:
        raise RuntimeError("R0.73F figure manifest is missing publication overlay")
    without_publication = dict(manifest)
    del without_publication["publication"]
    relative_manifest = manifest_path.relative_to(ROOT).as_posix()
    if json_bytes(without_publication) != git_object_bytes(
        FIGURE_METADATA_SEAL_COMMIT,
        relative_manifest,
    ):
        raise RuntimeError("R0.73F publication-free manifest differs from seal S")

    ledger_path = directory / "SHA256SUMS"
    current_ledger = strip_manifest_hash_row(
        ledger_path.read_bytes(),
        "R0.73F current figure ledger",
    )
    sealed_ledger = strip_manifest_hash_row(
        git_object_bytes(
            FIGURE_METADATA_SEAL_COMMIT,
            ledger_path.relative_to(ROOT).as_posix(),
        ),
        "R0.73F seal-S figure ledger",
    )
    if current_ledger != sealed_ledger:
        raise RuntimeError("R0.73F SHA ledger changed beyond the manifest hash row")


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
    if payload.get("allChecksPass") is True:
        return True
    checks = payload.get("checks")
    return (
        payload.get("status") == "passed"
        and isinstance(checks, dict)
        and bool(checks)
        and all(checks.values())
    )


def png_density(path: Path) -> tuple[int, int, int]:
    payload = path.read_bytes()
    if not payload.startswith(b"\x89PNG\r\n\x1a\n"):
        raise RuntimeError("R0.73F PNG signature is invalid")
    offset = 8
    while offset + 12 <= len(payload):
        length = struct.unpack(">I", payload[offset:offset + 4])[0]
        kind = payload[offset + 4:offset + 8]
        data = payload[offset + 8:offset + 8 + length]
        if kind == b"pHYs" and len(data) == 9:
            return struct.unpack(">IIB", data)
        offset += 12 + length
    raise RuntimeError("R0.73F PNG has no physical-density metadata")


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
        raise RuntimeError("R0.73F figure manifest output mismatch: " + suffix)
    row = matches[0]
    path = figure / expected_name
    if row.get("sha256") != digest(path):
        raise RuntimeError("R0.73F figure output hash mismatch: " + suffix)
    if row.get("bytes") is not None and row["bytes"] != path.stat().st_size:
        raise RuntimeError("R0.73F figure output size mismatch: " + suffix)
    return row


def validate_publication_assets(manifest: dict, directory: Path) -> None:
    publication = manifest.get("publication")
    if not isinstance(publication, dict):
        raise RuntimeError("R0.73F figure publication binding is missing")
    if (
        publication.get("byteIdentityRequired") is not True
        or publication.get("publicCopiesComplete") is not True
        or publication.get("directory") != "public/assets/r073f"
        or publication.get("fileStem") != FIGURE_ID
    ):
        raise RuntimeError("R0.73F figure publication contract is inconsistent")
    rows = publication.get("assets")
    if not isinstance(rows, list) or len(rows) != 3:
        raise RuntimeError("R0.73F publication must bind exactly three assets")
    by_path = {
        str(row.get("path", "")): row
        for row in rows
        if isinstance(row, dict)
    }
    expected_paths = {
        f"public/assets/r073f/{FIGURE_ID}.{suffix}"
        for suffix in ("pdf", "svg", "png")
    }
    if set(by_path) != expected_paths or len(by_path) != len(rows):
        raise RuntimeError("R0.73F publication asset path set is not exact")

    for suffix in ("pdf", "svg", "png"):
        relative = f"public/assets/r073f/{FIGURE_ID}.{suffix}"
        public_path = ROOT / relative
        source_path = directory / f"figure.{suffix}"
        if (
            not public_path.is_file()
            or public_path.is_symlink()
            or public_path.read_bytes() != source_path.read_bytes()
        ):
            raise RuntimeError("R0.73F public asset is not byte-identical: " + suffix)
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
            raise RuntimeError("R0.73F public asset binding mismatch: " + suffix)


def ensure_certificate_commit_ready() -> None:
    if CERTIFICATE_PACKAGE_COMMIT == CERTIFICATE_COMMIT_PLACEHOLDER:
        raise RuntimeError(
            "R0.73F release is intentionally sealed shut: replace "
            "TO_BE_FILLED_AFTER_CERTIFICATE_COMMIT with the certificate commit"
        )
    if not re.fullmatch(r"[0-9a-f]{40}", CERTIFICATE_PACKAGE_COMMIT):
        raise RuntimeError("R0.73F certificate commit must be a full Git SHA")


def ensure_figure_seal_commit_ready() -> None:
    if FIGURE_METADATA_SEAL_COMMIT == FIGURE_SEAL_COMMIT_PLACEHOLDER:
        raise RuntimeError(
            "R0.73F release is intentionally sealed shut: replace "
            "TO_BE_FILLED_AFTER_FIGURE_SEAL_COMMIT with the figure metadata "
            "seal commit"
        )
    if not re.fullmatch(r"[0-9a-f]{40}", FIGURE_METADATA_SEAL_COMMIT):
        raise RuntimeError("R0.73F figure metadata seal commit must be a full Git SHA")


def is_commit_ancestor(ancestor: str, descendant: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def verify_release_commit_chain() -> None:
    commits = (
        CERTIFIED_REPORT_COMMIT,
        FIGURE_PACKAGE_COMMIT,
        CERTIFICATE_PACKAGE_COMMIT,
        FIGURE_METADATA_SEAL_COMMIT,
        FIGURE_PUBLICATION_COMMIT,
    )
    if len(set(commits)) != len(commits):
        raise RuntimeError("R0.73F source/F/C/S/P commits must be strictly distinct")
    for commit in commits:
        subprocess.run(
            ["git", "cat-file", "-e", commit + "^{commit}"],
            cwd=ROOT,
            check=True,
        )
    for ancestor, descendant, label in (
        (CERTIFIED_REPORT_COMMIT, FIGURE_PACKAGE_COMMIT, "source < F"),
        (FIGURE_PACKAGE_COMMIT, CERTIFICATE_PACKAGE_COMMIT, "F < C"),
        (CERTIFICATE_PACKAGE_COMMIT, FIGURE_METADATA_SEAL_COMMIT, "C < S"),
        (FIGURE_METADATA_SEAL_COMMIT, FIGURE_PUBLICATION_COMMIT, "S < P"),
    ):
        if not is_commit_ancestor(ancestor, descendant):
            raise RuntimeError("R0.73F commit order is invalid: " + label)
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    for commit, label in (
        (FIGURE_PACKAGE_COMMIT, "F"),
        (CERTIFICATE_PACKAGE_COMMIT, "C"),
        (FIGURE_METADATA_SEAL_COMMIT, "S"),
        (FIGURE_PUBLICATION_COMMIT, "P"),
    ):
        if not is_commit_ancestor(commit, head):
            raise RuntimeError(f"R0.73F {label} commit is not an ancestor of HEAD")


def preflight_release_state() -> None:
    expected_baseline = {
        "latestCompletedRelease": "r073e",
        "siteVersion": "1.45",
        "publicHtmlNoteCount": 181,
        "postR060RecapNodeCount": 121,
        "nextRelease": "r073f",
        "latestReleaseGate": "tests/r073e-halfplane-transfer-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r073e-release.test.mjs",
        "postR070APublishedReleaseCount": 83,
        "postR070AFormalSealedReleaseCount": 59,
        "legacyFormalFigureBacklogCount": 24,
    }
    expected_target = {
        "latestCompletedRelease": "r073f",
        "siteVersion": "1.46",
        "publicHtmlNoteCount": 182,
        "postR060RecapNodeCount": 122,
        "nextRelease": "r073g",
        "postR070APublishedReleaseCount": 84,
        "postR070AFormalSealedReleaseCount": 60,
        "legacyFormalFigureBacklogCount": 24,
    }
    if R073E_RELEASE_BASELINE != expected_baseline:
        raise RuntimeError("R0.73F content module changed the exact R0.73E baseline")
    if R073F_RELEASE_TARGET != expected_target:
        raise RuntimeError("R0.73F content module changed the exact v1.46 target")

    release_path = ROOT / "research/release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    for key, value in R073E_RELEASE_BASELINE.items():
        if release.get(key) != value:
            raise RuntimeError(f"release manifest is not exactly at R0.73E: {key}")
    if release.get("nextReleaseSourceStage") is not None:
        raise RuntimeError("R0.73E baseline has an unexpected source-stage payload")

    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    inventory_state = (
        inventory.get("latestPublishedRelease"),
        inventory.get("publishedReleaseCount"),
        inventory.get("formalSealedReleaseCount"),
        inventory.get("legacyFormalFigureBacklogCount"),
    )
    if inventory_state != ("r073e", 83, 59, 24):
        raise RuntimeError("formal archive inventory is not exactly at R0.73E")
    if (
        inventory.get("publishedReleases", [])[-1:] != ["r073e"]
        or inventory.get("formalSealedReleases", [])[-1:] != ["r073e"]
    ):
        raise RuntimeError("R0.73E inventory tails are not exact")
    formal = release.get("formalArchiveInventory", {})
    if (
        formal.get("path") != "research/formal-archive-inventory.json"
        or formal.get("sha256") != digest(inventory_path)
    ):
        raise RuntimeError("R0.73E release manifest lost its inventory binding")

    site = json.loads((PUBLIC / "site-version.json").read_text(encoding="utf-8"))
    if site != {
        "schemaVersion": "research-site-version-v1",
        "version": "1.45",
        "latestRelease": "R0.73E",
        "publicHtmlNoteCount": 181,
        "publishedDate": "2026-08-30",
    }:
        raise RuntimeError("public site-version is not exactly at R0.73E")
    if (ROOT / "VERSION").read_text(encoding="utf-8") != "1.45\n":
        raise RuntimeError("root VERSION is not R0.73E v1.45")
    if len(list((PUBLIC / "notes").glob("r0-*.html"))) != 181:
        raise RuntimeError("R0.73E preflight expected 181 public HTML notes")

    forbidden = (
        "notes/r0-73f.html",
        "notes/r0-73f.pdf",
        "recap-r0-61-r0-73f.html",
        "recap-r0-61-r0-73f.pdf",
        f"assets/r073f/{FIGURE_ID}.pdf",
        f"assets/r073f/{FIGURE_ID}.svg",
        f"assets/r073f/{FIGURE_ID}.png",
    )
    for relative in forbidden:
        if (PUBLIC / relative).exists():
            raise RuntimeError("R0.73E preflight found premature output: " + relative)

    home = (PUBLIC / "research-review.html").read_text(encoding="utf-8")
    for token in (
        'data-site-version="1.45"',
        "<strong>181</strong>公开研究笔记",
        "<strong>R0.73E</strong>最新研究节点",
        'aria-label="R0.69P–R0.73E"',
        "R0.70A–R0.73E：83 节已公开，59 节完整封存",
    ):
        if token not in home:
            raise RuntimeError("R0.73E home baseline missing token: " + token)
    if 'data-release="r073f"' in home:
        raise RuntimeError("R0.73E home already contains an R0.73F card")
    route = re.search(
        r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73E">'
        r"(.*?)</nav>",
        home,
        flags=re.S,
    )
    if route is None or len(re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))) != 91:
        raise RuntimeError("R0.73E home must contain 91 current-route links")

    recap = (PUBLIC / "recap-r0-61-r0-73e.html").read_text(encoding="utf-8")
    start = recap.index('<section id="node-index">')
    end = recap.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', recap[start:end])
    if len(links) != 121 or len(set(links)) != 121:
        raise RuntimeError("R0.73E recap must contain 121 unique nodes")
    if recap.count('<article class="phase">') != 40:
        raise RuntimeError("R0.73E recap must contain 40 phases")
    for value, label in ((home, "home"), (recap, "recap")):
        assert_public_voice(value, "R0.73E baseline " + label)


def validate_analytic_sources() -> None:
    subprocess.run(
        ["git", "cat-file", "-e", CERTIFIED_REPORT_COMMIT + "^{commit}"],
        cwd=ROOT,
        check=True,
    )
    for relative in SOURCE_PATHS:
        path = ROOT / relative
        if not path.is_file():
            raise RuntimeError("missing R0.73F analytic source: " + relative)
        if path.read_bytes() != git_object_bytes(CERTIFIED_REPORT_COMMIT, relative):
            raise RuntimeError("R0.73F source differs from sourceCommit: " + relative)

    report = (ROOT / "research/r073f_report-source.md").read_text(encoding="utf-8")
    gap = (ROOT / "research/r073f_gap_matrix.md").read_text(encoding="utf-8")
    proof = (ROOT / "research/r073f_moving_dichotomy_proof.md").read_text(encoding="utf-8")
    audit = (ROOT / "research/r073f_independent_analytic_audit.md").read_text(encoding="utf-8")
    literature = (ROOT / "research/r073f_literature_audit.md").read_text(encoding="utf-8")

    for key in CLOSED_KEYS:
        for source, label in ((report, "report"), (gap, "gap")):
            if key + "=CLOSED" not in source:
                raise RuntimeError(f"R0.73F {label} lost CLOSED token: {key}")
    for key in FALSE_KEYS:
        for source, label in ((report, "report"), (gap, "gap")):
            if key + "=FALSE" not in source:
                raise RuntimeError(f"R0.73F {label} lost FALSE token: {key}")
    for key in OPEN_KEYS:
        expected = (
            key + "=OPEN_NOT_USED"
            if key == "graphDomainKatoTransport"
            else key + "=OPEN"
        )
        if expected not in report:
            raise RuntimeError("R0.73F report lost OPEN token: " + key)

    for token in (
        "rho<\\frac{\\nu}{16K^2}",
        "By (4.14)",
        "fixed physical observation window",
        "complete all-row OS--Squire",
        "no conclusion about the Clay problem",
    ):
        if token not in proof:
            raise RuntimeError("R0.73F proof missing token: " + token)
    for token in (
        "Initial adversarial verdict: NOT PASS",
        "FINAL PASS",
        "Finite diagnostics are not part of the proof",
        "Complete all-row OS--Squire",
        "Clay Millennium",
    ):
        if token not in audit:
            raise RuntimeError("R0.73F independent audit missing token: " + token)
    for token in (
        "Latushkin--Schnaubelt",
        "Coppel",
        "Schnaubelt",
        "Schmid",
        "Joye",
        "not an originality or",
    ):
        if token not in literature:
            raise RuntimeError("R0.73F literature audit missing token: " + token)
    for token in (
        "| F1 |",
        "| F12 |",
        "diagnostics and counterexamples cannot change any continuum state.",
    ):
        if token not in gap:
            raise RuntimeError("R0.73F gap matrix missing token: " + token)

    for value, label in (
        (NOTE_HERO, "note hero"),
        (NOTE_ARTICLE, "note article"),
        (HOME_F_CARD, "home card"),
        (HOME_LATEST_SPOTLIGHT, "home spotlight"),
        (HOME_NEXT, "home next"),
    ):
        assert_public_voice(value, "R0.73F " + label)


def validate_experiment() -> None:
    directory = ROOT / EXPERIMENT_RELATIVE
    for name in (
        "summary.json",
        "independent_validation.json",
        "manifest.json",
        "SHA256SUMS",
    ):
        if not (directory / name).is_file():
            raise RuntimeError("missing R0.73F experiment input: " + name)
    verify_complete_flat_ledger(directory, "R0.73F experiment")
    verify_sealed_directory(
        directory, FIGURE_PACKAGE_COMMIT, "R0.73F experiment"
    )
    summary = json.loads((directory / "summary.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (directory / "independent_validation.json").read_text(encoding="utf-8")
    )
    manifest = verify_manifest_hashes(
        directory / "manifest.json", "R0.73F experiment manifest"
    )
    if summary.get("allPrimaryChecksPass") is not True:
        raise RuntimeError("R0.73F primary finite diagnostic is not passed")
    if independent.get("allChecksPass") is not True:
        raise RuntimeError("R0.73F independent finite validation is not passed")
    if (
        manifest.get("release") != "R0.73F-finite-diagnostic"
        or manifest.get("status") != "validated"
        or manifest.get("sourceCommit") != CERTIFIED_REPORT_COMMIT
    ):
        raise RuntimeError("R0.73F experiment manifest identity is inconsistent")
    verify_source_bindings(manifest, "R0.73F experiment manifest")
    for payload, label in ((summary, "primary"), (independent, "independent"), (manifest, "manifest")):
        boundary = payload.get("claimBoundary", {})
        if boundary.get("finiteBinary64Diagnostic") is not True:
            raise RuntimeError(f"R0.73F {label} lost finite diagnostic status")
        for key in (
            "finiteGainProvesContinuumDichotomy",
            "finiteRateEqualsAnalyticKappa",
            "finiteTopEqualsContinuumTop",
            "ordinaryCutoffAgreementIsTailProof",
            "sampledTimeIsContinuousTimeBound",
            "nonlinearNavierStokes",
            "Clay",
        ):
            if boundary.get(key) is not False:
                raise RuntimeError(f"R0.73F {label} escaped boundary: {key}")
    if summary.get("diagnosticEndpointIsCertifiedD0") is not False:
        raise RuntimeError("R0.73F finite endpoint was confused with certified d0")


def validate_certificate() -> dict:
    ensure_certificate_commit_ready()
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
            raise RuntimeError("missing R0.73F certificate input: " + name)
    verify_complete_flat_ledger(directory, "R0.73F certificate")
    verify_sealed_directory(
        directory, CERTIFICATE_PACKAGE_COMMIT, "R0.73F certificate"
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
        directory / "manifest.json", "R0.73F certificate manifest"
    )
    if not checks_pass(independent) or not checks_pass(validation):
        raise RuntimeError("R0.73F certificate package is not independently passed")
    source_commit = str(
        certificate.get("sourceCommit", manifest.get("sourceCommit", ""))
    )
    if source_commit != CERTIFIED_REPORT_COMMIT:
        raise RuntimeError("R0.73F certificate sourceCommit is not exact")
    verify_source_bindings(manifest, "R0.73F certificate manifest")

    closed_claims = certificate.get("closedClaims")
    if not isinstance(closed_claims, dict) or set(closed_claims) != set(CLOSED_KEYS):
        raise RuntimeError("R0.73F certificate closedClaims key set is not exact")
    for key in CLOSED_KEYS:
        if closed_claims[key] != "CLOSED":
            raise RuntimeError("R0.73F certificate claim is not CLOSED: " + key)

    false_shortcuts = certificate.get("falseShortcuts")
    if (
        not isinstance(false_shortcuts, dict)
        or set(false_shortcuts) != set(CERTIFICATE_FALSE_SHORTCUT_KEYS)
    ):
        raise RuntimeError("R0.73F certificate falseShortcuts key set is not exact")
    for key in CERTIFICATE_FALSE_SHORTCUT_KEYS:
        if false_shortcuts[key] != "FALSE_IN_GENERAL":
            raise RuntimeError("R0.73F certificate shortcut is not FALSE: " + key)

    open_claims = certificate.get("openClaims")
    if (
        not isinstance(open_claims, dict)
        or set(open_claims) != set(CERTIFICATE_OPEN_KEYS)
    ):
        raise RuntimeError("R0.73F certificate openClaims key set is not exact")
    for key in CERTIFICATE_OPEN_KEYS:
        expected = "OPEN_NOT_USED" if key == "graphDomainKatoTransport" else "OPEN"
        if open_claims[key] != expected:
            raise RuntimeError("R0.73F certificate claim has wrong OPEN state: " + key)

    boundary = certificate.get("claimBoundary")
    expected_boundary = set(CERTIFICATE_OPEN_KEYS) | set(CERTIFICATE_BOUNDARY_ONLY_KEYS)
    if not isinstance(boundary, dict) or set(boundary) != expected_boundary:
        raise RuntimeError("R0.73F certificate claimBoundary key set is not exact")
    for key in expected_boundary:
        if boundary[key] is not False:
            raise RuntimeError("R0.73F certificate escaped claim boundary: " + key)

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
        raise RuntimeError("R0.73F certificate commit does not descend from sourceCommit")
    return certificate


def validate_figure(certificate: dict) -> dict:
    ensure_certificate_commit_ready()
    ensure_figure_seal_commit_ready()
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
            raise RuntimeError("missing R0.73F formal figure input: " + name)
    verify_complete_flat_ledger(directory, "R0.73F figure")
    verify_named_files_at_commit(
        directory,
        FIGURE_PACKAGE_COMMIT,
        FIGURE_IMMUTABLE_FILES,
        "R0.73F figure",
    )
    verify_metadata_overlay(directory)
    verify_exact_flat_directory_at_commit(
        directory,
        FIGURE_PUBLICATION_COMMIT,
        "R0.73F figure publication seal",
    )
    manifest = verify_manifest_hashes(
        directory / "manifest.json", "R0.73F figure manifest"
    )
    contract = json.loads((directory / "contract.json").read_text(encoding="utf-8"))
    validation = json.loads(
        (directory / "validation.json").read_text(encoding="utf-8")
    )
    if (
        manifest.get("figureId") != FIGURE_ID
        or manifest.get("status") != "formal"
        or manifest.get("release") not in ("R0.73F", "R0.73F-finite-diagnostic")
    ):
        raise RuntimeError("R0.73F figure identity or formal status mismatch")
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
        raise RuntimeError("R0.73F figure provenance chain is inconsistent")
    verify_source_bindings(manifest, "R0.73F figure manifest")
    if not checks_pass(validation):
        raise RuntimeError("R0.73F figure validation is not passed")

    claims = contract.get("claimBoundary", {})
    if claims.get("formalFiniteDiagnosticFigure") is not True:
        raise RuntimeError("R0.73F figure lost formal finite-diagnostic status")
    for key, value in claims.items():
        if key != "formalFiniteDiagnosticFigure" and value is not False:
            raise RuntimeError("R0.73F figure escaped boundary: " + key)

    certificate_outputs = certificate.get("formalFigure")
    if not isinstance(certificate_outputs, dict):
        certificate_outputs = certificate.get("journalFigure")
    if not isinstance(certificate_outputs, dict):
        raise RuntimeError("R0.73F certificate has no figure hash ledger")
    for suffix in ("pdf", "svg", "png"):
        output = require_output_record(manifest, directory, suffix)
        sealed = certificate_outputs.get(suffix)
        if not isinstance(sealed, dict):
            raise RuntimeError(
                "R0.73F certificate figure entry is missing: " + suffix
            )
        current = directory / f"figure.{suffix}"
        if (
            sealed.get("sha256") != digest(current)
            or sealed.get("bytes") != current.stat().st_size
            or output.get("sha256") != sealed.get("sha256")
            or output.get("bytes") != sealed.get("bytes")
        ):
            raise RuntimeError("R0.73F certificate/figure output mismatch: " + suffix)
    if not (directory / "figure.pdf").read_bytes().startswith(b"%PDF"):
        raise RuntimeError("R0.73F formal PDF signature is invalid")
    svg = (directory / "figure.svg").read_text(encoding="utf-8")
    if "<svg" not in svg or "<image" in svg:
        raise RuntimeError("R0.73F formal SVG is absent or rasterized")
    x_density, y_density, unit = png_density(directory / "figure.png")
    if unit != 1 or abs(x_density - 23622) > 100 or abs(y_density - 23622) > 100:
        raise RuntimeError("R0.73F formal PNG is not tagged at 600 dpi")
    png_record = require_output_record(manifest, directory, "png")
    if png_record.get("dpi") not in (None, 600):
        raise RuntimeError("R0.73F figure manifest does not declare 600 dpi")
    validate_publication_assets(manifest, directory)
    return manifest


def validate_inputs() -> tuple[dict, dict]:
    validate_analytic_sources()
    validate_experiment()
    certificate = validate_certificate()
    figure_manifest = validate_figure(certificate)
    return certificate, figure_manifest


def build_note() -> str:
    html = (PUBLIC / "notes/r0-73e.html").read_text(encoding="utf-8")
    metadata = (
        (
            "description",
            r'<meta name="description" content=".*?">',
            '<meta name="description" content="研究笔记 R0.73F：一条精确线性 Fourier 行上的移动剖面二分与固定窗口指数增益；全行、非线性与 Clay 仍开放。">',
        ),
        (
            "og title",
            r'<meta property="og:title" content=".*?">',
            '<meta property="og:title" content="R0.73F｜Moving-profile dichotomy and fixed-window exponential gain">',
        ),
        (
            "og description",
            r'<meta property="og:description" content=".*?">',
            '<meta property="og:description" content="A one-row linear theorem closes fixed-window exponential gain; finite diagnostics, all-row control, nonlinear dynamics, and Clay remain separate.">',
        ),
        (
            "og image",
            r'<meta property="og:image" content=".*?">',
            f'<meta property="og:image" content="https://kasifa.github.io/assets/r073f/{FIGURE_ID}.png">',
        ),
        (
            "title",
            r'<title>.*?</title>',
            '<title>R0.73F｜Moving-profile dichotomy and fixed-window exponential gain</title>',
        ),
    )
    for label, pattern, value in metadata:
        html = section(html, pattern, value, "F note " + label)
    html = required(
        html, "/i18n-en.js?v=1.45", "/i18n-en.js?v=1.46", "F note i18n"
    )
    nav = (
        '<nav><a href="#result">结论</a><a href="#row">精确行</a>'
        '<a href="#frozen">冻结输入</a><a href="#roughness">粗糙性</a>'
        '<a href="#graphs">图空间</a><a href="#instantaneous">瞬时围道</a>'
        '<a href="#clamp">精确剖面</a><a href="#gain">窗口下界</a>'
        '<a href="#order">指数阶</a><a href="#false">反例</a>'
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
        ("row", "01 · exact row"),
        ("frozen", "02 · frozen input"),
        ("roughness", "03 · roughness"),
        ("graphs", "04 · graph invariance"),
        ("instantaneous", "05 · instantaneous contour"),
        ("clamp", "06 · exact profile"),
        ("gain", "07 · fixed-window lower law"),
        ("order", "08 · exponential order"),
        ("false", "09 · exact negative checks"),
        ("finite", "10 · finite diagnostic"),
        ("literature", "11 · literature boundary"),
        ("audit", "12 · independent audit"),
        ("figure", "13 · journal figure"),
        ("boundary", "14 · exact boundary"),
        ("value", "15 · value"),
        ("next", "16 · R0.73G"),
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
        '<div>研究笔记 R0.73F · 2026-08-30<br><a href="/">返回研究主页</a></div></footer>'
    )
    html = section(html, r"<footer>.*?</footer>", footer, "F note footer")
    assert_clean(html, "R0.73F note")
    assert_mathjax_clean(html, "R0.73F note")
    assert_public_voice(html, "R0.73F note")
    return html


def build_recap() -> str:
    html = (PUBLIC / "recap-r0-61-r0-73e.html").read_text(encoding="utf-8")
    metadata = (
        (
            "description",
            r'<meta name="description" content=".*?">',
            '<meta name="description" content="R0.60 之后的完整研究回顾：R0.61 到 R0.73F 共 122 个节点；最新一节闭合一条精确线性行的固定窗口指数增益。">',
        ),
        (
            "og title",
            r'<meta property="og:title" content=".*?">',
            '<meta property="og:title" content="R0.61–R0.73F｜R0.60 之后的研究回顾">',
        ),
        (
            "og description",
            r'<meta property="og:description" content=".*?">',
            '<meta property="og:description" content="四十一个阶段、122 个节点：从约化递推和环带排除到一条精确线性行的固定窗口指数增益。">',
        ),
        (
            "title",
            r"<title>.*?</title>",
            "<title>R0.61–R0.73F｜R0.60 之后的研究回顾</title>",
        ),
    )
    for label, pattern, value in metadata:
        html = section(html, pattern, value, "F recap " + label)
    html = required(
        html, "/i18n-en.js?v=1.45", "/i18n-en.js?v=1.46", "F recap i18n"
    )
    hero = r'''    <header class="hero"><div class="hero-inner"><div><div class="eyebrow">累计回顾 · R0.61–R0.73F · 2026-08-30</div><h1>R0.60 之后的研究回顾</h1><p class="lead">这页保留 R0.61 到 R0.73F 的全部 122 个节点。R0.61–R0.69W 从约化递推走到严格环带排除；R0.70A–R0.71Z 检查移动尺度、临界账本、内部 entry 与 complete-root 边界；R0.72A–R0.73B 处理 strong coupling、critical log、碰撞几何与完整线性 Fourier--Leray 行；R0.73C–F 依次认证冻结 Rayleigh 不稳定、静态黏性持续、固定正半平面传递和移动剖面固定窗口指数增益。完整全行、非线性与 Clay 没有被外推。</p></div><div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.73F</strong><p>收录节点：122</p><p>回顾截止时公开笔记：182</p><p>回顾截止节点：R0.73F</p><p>问题状态：仍未解决</p></div></div></header>'''
    html = section(html, r'    <header class="hero">.*?</header>', hero, "F recap hero")
    for old, new in (
        ("02 · 121 节完整索引", "02 · 122 节完整索引"),
        ("01 · 四十个研究阶段", "01 · 四十一个研究阶段"),
        ("R0.60 之后的路线分成四十个阶段", "R0.60 之后的路线分成四十一个阶段"),
        ('data-current-route="R0.69P–R0.73E"', 'data-current-route="R0.69P–R0.73F"'),
    ):
        html = required(html, old, new, "F recap counter")
    result = r'''        <section id="result"><div class="section-no">00 / 回顾范围</div><h2>版本数、封存数和数学结论分开报告</h2><div class="metrics"><div class="metric"><strong>122</strong><span>R0.61–R0.73F 研究节点</span></div><div class="metric"><strong>84</strong><span>R0.70A–R0.73F 已公开版本</span></div><div class="metric"><strong>60</strong><span>当前 formal-figure 合同下完整封存</span></div><div class="metric"><strong>24</strong><span>旧版附图档案待回补</span></div></div><p>R0.00–R0.60 保留在上一份阶段回顾。R0.70A–R0.73F 的 84 个版本已经公开，其中 60 个满足当前完整封存合同，24 个历史版本仍欠 formal-figure 回补。公开和封存不表示 Clay 问题已经解决。</p></section>'''
    html = section(html, r'        <section id="result">.*?</section>', result, "F recap result")
    phase = r'''            <article class="phase"><h3>R0.73F · Moving-profile dichotomy and fixed-window exponential gain</h3><p>R0.73E 的统一冻结二分与精确 \(49d/4\) profile drift 进入 Lyapunov--Perron 图构造；稳定抛物半群保持单侧，负时间只用于有限维 top block。</p><p>局部瞬时共同围道、移动动力学不稳定束与每个固定观察窗口内的 \(e^{c_D|\Lambda|}\) 算子范数下界闭合。有限诊断只承担复算和附图，不证明 continuum theorem。</p><p>__CLOSED__。__FALSE__。__OPEN__。</p><div class="links"><a href="/notes/r0-73f.html">R0.73F</a><a href="/assets/r073f/__FIGURE_ID__.pdf">R0.73F 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073f">R0.73F 证书</a></div></article>
'''.replace("__CLOSED__", CLOSED).replace("__FALSE__", FALSE).replace("__OPEN__", OPEN).replace("__FIGURE_ID__", FIGURE_ID)
    marker = '          </div>\n        </section>\n\n        <section id="node-index">'
    html = once(html, marker, phase + marker, "F recap phase")
    html = required(
        html,
        "R0.61–R0.73E 的 121 节公开笔记",
        "R0.61–R0.73F 的 122 节公开笔记",
        "F recap node title",
    )
    node_e = '            <span class="node-ref"><a href="/notes/r0-73e.html">R0.73E</a><span class="node-state kind-closed">闭</span></span>\n'
    node_f = '            <span class="node-ref"><a href="/notes/r0-73f.html">R0.73F</a><span class="node-state kind-closed">闭</span></span>\n'
    html = once(html, node_e, node_e + node_f, "F recap node")
    retained = '            <li>R0.73F 闭合一条精确线性 Fourier 行上的局部移动二分与固定窗口指数增益；finite diagnostic、完整全行、nonlinear 与 Clay 边界保持分离。</li>\n'
    html = once(
        html,
        "          </ul>\n          <p>这些结果可以分别整理成",
        retained + "          </ul>\n          <p>这些结果可以分别整理成",
        "F recap retained",
    )
    value = r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>一条精确线性行的固定窗口指数增益已成为定理；非线性闭合仍不存在</h2><p>不能把 122 个节点或 84 个公开版本解释成 Clay 完成比例。R0.73F 的严格增量是 conditional one-row operator theorem，不是有限矩阵外推，也不是 all-row 或 nonlinear 结论。</p></section>'''
    html = section(html, r'        <section id="value">.*?</section>', value, "F recap value")
    next_gate = r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.73G 冻结精确衰减剪切流附近的非线性扰动 bootstrap</h2><p>明确 seed size、Sobolev topology、lifespan 与 mode-convolution remainder；目标是给出闭合证明，或给出阻止闭合的否定障碍。</p></section>'''
    html = section(html, r'        <section id="next">.*?</section>', next_gate, "F recap next")
    claims = (
        r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2><p>R0.70A–R0.73F 的 84 节已公开；60 节完整封存；24 节旧档待回补。</p><p>__CLOSED__。</p><p>__FALSE__。</p><p>__OPEN__。</p></section>'''
        .replace("__CLOSED__", CLOSED)
        .replace("__FALSE__", FALSE)
        .replace("__OPEN__", OPEN)
    )
    html = section(html, r'        <section id="claims">.*?</section>', claims, "F recap claims")
    reproduce = r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证明、审计、证书、有限诊断、附图和历史回顾</h2><p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-73e.html">保留 R0.73E 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-73f.html">打开最新节点 R0.73F</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073f_moving_dichotomy_proof.md">查看 R0.73F 证明</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073f_independent_analytic_audit.md">查看独立解析审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073f">查看正式证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/experiments/r073f">查看有限诊断与监控记录</a> · <a href="/assets/r073f/__FIGURE_ID__.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-73f.pdf">下载同步 PDF</a></p><p>continuum theorem 来自解析证明与独立审计。Fourier cutoff 只做诊断和附图。</p></section>'''.replace("__FIGURE_ID__", FIGURE_ID)
    html = section(html, r'        <section id="reproduce">.*?</section>', reproduce, "F recap reproduce")
    footer = '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>我按原编号记录推导、反例和未解决的问题。</div><div>R0.61–R0.73F 回顾 · 2026-08-30<br><a href="/">返回研究主页</a></div></footer>'
    html = section(html, r"<footer>.*?</footer>", footer, "F recap footer")
    start = html.index('<section id="node-index">')
    end = html.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', html[start:end])
    if len(links) != 122 or len(set(links)) != 122:
        raise RuntimeError("R0.73F recap expected 122 unique nodes")
    if html.count('<article class="phase">') != 41:
        raise RuntimeError("R0.73F recap expected 41 phases")
    assert_clean(html, "R0.73F recap")
    assert_mathjax_clean(html, "R0.73F recap", check_naked=False)
    assert_public_voice(html, "R0.73F recap")
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
        ('data-site-version="1.45"', 'data-site-version="1.46"'),
        ("/i18n-en.js?v=1.45", "/i18n-en.js?v=1.46"),
        ("/site-refresh.js?v=1.45", "/site-refresh.js?v=1.46"),
        ("<strong>v1.45</strong>网页版本", "<strong>v1.46</strong>网页版本"),
        ("<strong>181</strong>公开研究笔记", "<strong>182</strong>公开研究笔记"),
        ("<strong>R0.73E</strong>最新研究节点", "<strong>R0.73F</strong>最新研究节点"),
        (
            '<a class="route-map-latest" href="#r073e">跳到首页 R0.73E 卡片 →</a>',
            '<a class="route-map-latest" href="#r073f">跳到首页 R0.73F 卡片 →</a>',
        ),
        (
            "moving-profile top-bundle gap / evolution dichotomy / fixed-window exponential test",
            "nonlinear seed / Sobolev topology / lifespan / mode-convolution remainder",
        ),
        ("Research topology · R0.1–R0.73E", "Research topology · R0.1–R0.73F"),
        (
            "R0.70A–R0.73E：83 节已公开，59 节完整封存",
            "R0.70A–R0.73F：84 节已公开，60 节完整封存",
        ),
        (
            '<span class="route-range">R0.69P–R0.73E</span>',
            '<span class="route-range">R0.69P–R0.73F</span>',
        ),
        ('aria-label="R0.69P–R0.73E"', 'aria-label="R0.69P–R0.73F"'),
        ("展开 91 篇公开笔记", "展开 92 篇公开笔记"),
        ("本站 R0.69P–R0.73E 路线", "本站 R0.69P–R0.73F 路线"),
        ("综述 v1.45 · 2026-08-30", "综述 v1.46 · 2026-08-30"),
        ("上次综述 v1.44 · 2026-08-30", "上次综述 v1.45 · 2026-08-30"),
    ):
        html = required(html, old, new, "F home " + old)
    html = replace_all(
        html,
        "/recap-r0-61-r0-73e.html",
        "/recap-r0-61-r0-73f.html",
        "F home recap HTML links",
    )
    html = replace_all(
        html,
        "/recap-r0-61-r0-73e.pdf",
        "/recap-r0-61-r0-73f.pdf",
        "F home recap PDF links",
    )
    historical = '<strong style="color:var(--gold)">下一步 R0.73F：</strong>&nbsp;证明或否证固定小物理窗口上的 moving-profile top bundle 统一谱隙与演化二分。'
    html = required(
        html,
        historical,
        historical.replace("下一步", "当时的下一步"),
        "F home historical E next",
    )
    focus = r'<div class="summary-item"><strong>我目前关注</strong><span>R0.73F 已闭合一条精确线性 Fourier 行上的移动剖面二分和固定窗口指数增益。下一关冻结非线性 seed size、Sobolev topology、lifespan 与 mode-convolution remainder。</span></div>'
    html = section(
        html,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        focus,
        "F home focus",
    )
    html = required(
        html,
        "<h3>R0.73E：固定正半平面分裂与对数快时间传递已闭合</h3>",
        "<h3>R0.73F：移动剖面二分与固定窗口指数增益已闭合</h3>",
        "F home current title",
    )
    html = required(
        html,
        "<span>R0.72R–R0.73E：</span>",
        "<span>R0.72R–R0.73F：</span>",
        "F home path range",
    )
    html = required(
        html,
        "certified frozen Rayleigh instability → static viscous cluster persistence → fixed-half-plane logarithmic transfer</p>",
        "certified frozen Rayleigh instability → static viscous cluster persistence → fixed-half-plane logarithmic transfer → moving-profile fixed-window dichotomy</p>",
        "F home path tail",
    )
    link_e = '<a class="milestone" href="/notes/r0-73e.html">R0.73E</a>'
    html = once(
        html,
        link_e,
        link_e + '\n                  <a class="milestone" href="/notes/r0-73f.html">R0.73F</a>',
        "F home route link",
    )
    route_f = '              <p>R0.73F 用带保守半径的 Lyapunov--Perron 图构造把 R0.73E 冻结二分传递到精确移动剖面，闭合一条精确线性行的固定窗口指数增益。finite diagnostic、完整全行、nonlinear 与 Clay 边界保持分离。</p>\n'
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
    recap = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem"><p class="eyebrow">累计回顾 R0.61–R0.73F · 2026-08-30</p><h3>R0.60 recap 之后的累计回顾收录 122 个节点；全站现有 182 篇公开研究笔记</h3><p>累计回顾现分四十一个阶段，完整保留 R0.61–R0.73F；最新节点分开记录 operator theorem、finite diagnostic、文献边界和 open gate。</p><p>R0.70A–R0.73F 共 84 个版本已公开；60 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p><p><strong>阶段判断：</strong>&nbsp;一条精确线性行上的移动剖面二分与固定窗口指数增益已闭合；完整全行、nonlinear 与 Clay 保持 OPEN。</p><p><a href="/recap-r0-61-r0-73f.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-73f.pdf">下载同步 PDF</a></p></div>'''
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
        '          </div>\n\n' + HOME_F_CARD + '\n        </section>\n\n      </article>',
        "F home card",
    )
    if html.count('data-release="r073f"') != 1:
        raise RuntimeError("home must contain exactly one R0.73F card")
    if html.count('<strong style="color:var(--gold)">下一步 R0.73G：') != 1:
        raise RuntimeError("home must contain exactly one current R0.73G gate")
    route = re.search(
        r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73F">'
        r"(.*?)</nav>",
        html,
        flags=re.S,
    )
    if route is None or len(re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))) != 92:
        raise RuntimeError("home current-route index must contain 92 note links")
    assert_clean(html, "R0.73F home")
    assert_mathjax_clean(html, "R0.73F home", check_naked=False)
    assert_public_voice(html, "R0.73F home")
    return html


def update_literature() -> str:
    html = (PUBLIC / "literature-review.html").read_text(encoding="utf-8")
    for old, new in (
        ("/i18n-en.js?v=1.45", "/i18n-en.js?v=1.46"),
        (
            "本站 R0.69P–R0.73E 只列为研究笔记",
            "本站 R0.69P–R0.73F 只列为研究笔记",
        ),
        ("文献综述 v1.45 · 2026-08-30", "文献综述 v1.46 · 2026-08-30"),
        ("累计回顾与 121 节索引", "累计回顾与 122 节索引"),
        ("打开 121 节完整索引", "打开 122 节完整索引"),
    ):
        html = required(html, old, new, "F literature " + old)
    html = replace_all(
        html,
        "/recap-r0-61-r0-73e.html",
        "/recap-r0-61-r0-73f.html",
        "F literature recap links",
    )
    old_open = r'<div class="route-step pause"><header><b>开放接口 · R0.73F</b><strong>moving-profile top bundle on a fixed physical window</strong></header><p>证明或否证统一谱隙与演化二分，目标是 fixed-window \(e^{c|\Lambda|}\)；graph-domain/Kato transport 仍只是候选方法。</p></div>'
    new_steps = r'''<div class="route-step kept"><header><b>R0.73F</b><strong>moving-profile dichotomy and fixed-window exponential gain</strong></header><p>带统一 prefactor 的冻结二分、精确有界 profile drift 与 Lyapunov--Perron 图构造闭合一条精确线性行的 fixed-window \(e^{c_D|\Lambda|}\)。<a href="/notes/r0-73f.html">研究笔记</a> <a href="/recap-r0-61-r0-73f.html">当前累计回顾</a> <a href="#r073f-boundary">文献边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.73G</b><strong>nonlinear perturbation bootstrap near the exact decaying shear</strong></header><p>冻结 seed size、Sobolev topology、lifespan 与 mode-convolution remainder，证明 bootstrap 闭合或给出否定障碍。</p></div>'''
    html = once(html, old_open, new_steps, "F literature route")
    boundary = r'''

          <h3 id="r073f-boundary">R0.73F 的非自治二分、瞬时投影与有限诊断边界</h3>
          <p><a href="https://doi.org/10.1006/jdeq.1999.3668">Latushkin--Schnaubelt 1999</a>给出稳定部分可不可逆、只要求不稳定纤维反向可逆的 dichotomy 约定；<a href="https://doi.org/10.1007/BFb0067780">Coppel 1978</a>是有限维 roughness 先例。<a href="https://iana.math.kit.edu/downloads/iana3/schnaubelt/Paper/ed.pdf">Schnaubelt 1999</a>需要完整的 (P1)、(ED) 与定量小性条件；<a href="https://doi.org/10.1142/S0129055X19500144">Schmid 2019</a>和<a href="https://doi.org/10.1007/s00220-007-0299-y">Joye 2007</a>也保留共同域、正则性、谱隙或解析性假设。R0.73F 的关键 roughness 步骤自包含；一般文献不替代精确行上的 \(49d/4\) 漂移验证，也不提供非线性或 Clay 结论。本节不作原创性或优先权声明。</p>
          <div class="boundary"><strong>R0.73F 的主张边界</strong><p>__CLOSED__。</p><p>__FALSE__。</p><p>__OPEN__。有限 Fourier 数据不承担 continuum proof。</p></div>'''
    boundary = (
        boundary
        .replace("__CLOSED__", CLOSED)
        .replace("__FALSE__", FALSE)
        .replace("__OPEN__", OPEN)
    )
    match = re.search(
        r'(<h3 id="r073e-boundary">.*?<div class="boundary">.*?</div>)',
        html,
        flags=re.S,
    )
    if match is None:
        raise RuntimeError("F literature expected R0.73E boundary")
    html = once(
        html, match.group(1), match.group(1) + boundary, "F literature boundary"
    )
    references = r'''            <li id="ref-122">W. A. Coppel. <a href="https://doi.org/10.1007/BFb0067780"><em>Dichotomies in Stability Theory</em></a>. Lecture Notes in Mathematics 629, Springer, 1978.</li>
            <li id="ref-123">R. Schnaubelt. <a href="https://iana.math.kit.edu/downloads/iana3/schnaubelt/Paper/ed.pdf"><em>Sufficient conditions for exponential stability and dichotomy of evolution equations</em></a>. Forum Mathematicum 11 (1999), 543--566.</li>
            <li id="ref-124">A. Joye. <a href="https://doi.org/10.1007/s00220-007-0299-y"><em>General Adiabatic Evolution with a Gap Condition</em></a>. Communications in Mathematical Physics 275 (2007), 139--162.</li>
'''
    html = once(
        html,
        '          </ol>\n          <p class="source-note">',
        references + '          </ol>\n          <p class="source-note">',
        "F literature references",
    )
    terminal = "R0.73E 用固定正半平面完备性、完整 top cluster 相对二分和固定生成元 Volterra 论证闭合 logarithmic fast-time transfer；moving-profile fixed-window、完整 OS--Squire、nonlinear 与 Clay 仍为 OPEN。"
    terminal_f = terminal + "R0.73F 再用有界扰动 roughness、精确 clamped profile 与移动不稳定束闭合一条精确线性行的 fixed-window exponential lower law；finite diagnostic、完整全行、nonlinear 与 Clay 边界保持分离。"
    html = required(html, terminal, terminal_f, "F literature deck terminal")
    assert_clean(html, "R0.73F literature")
    assert_mathjax_clean(html, "R0.73F literature", check_naked=False)
    assert_public_voice(html, "R0.73F literature")
    return html


def build_manifest_outputs() -> dict[Path, bytes]:
    release_path = ROOT / "research/release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    for key, value in R073E_RELEASE_BASELINE.items():
        if release.get(key) != value:
            raise RuntimeError("release manifest changed during generation: " + key)
    release.update({
        **R073F_RELEASE_TARGET,
        "latestReleaseGate": "tests/r073f-moving-dichotomy-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r073f-release.test.mjs",
    })
    release.pop("nextReleaseSourceStage", None)

    site_path = PUBLIC / "site-version.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    if site != {
        "schemaVersion": "research-site-version-v1",
        "version": "1.45",
        "latestRelease": "R0.73E",
        "publicHtmlNoteCount": 181,
        "publishedDate": "2026-08-30",
    }:
        raise RuntimeError("site-version changed during R0.73F generation")
    site.update({
        "version": "1.46",
        "latestRelease": "R0.73F",
        "publicHtmlNoteCount": 182,
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
    if state != ("r073e", 83, 59, 24):
        raise RuntimeError("formal archive changed during R0.73F generation")
    for key in ("publishedReleases", "formalSealedReleases"):
        if inventory[key][-1] != "r073e" or "r073f" in inventory[key]:
            raise RuntimeError("formal archive is not append-only: " + key)
        inventory[key].append("r073f")
    inventory.update({
        "latestPublishedRelease": "r073f",
        "publishedReleaseCount": 84,
        "formalSealedReleaseCount": 60,
        "legacyFormalFigureBacklogCount": 24,
    })
    if (
        len(inventory["publishedReleases"]) != 84
        or len(inventory["formalSealedReleases"]) != 60
    ):
        raise RuntimeError("formal archive count mismatch after R0.73F")
    inventory_payload = json_bytes(inventory)
    release["formalArchiveInventory"] = {
        "path": "research/formal-archive-inventory.json",
        "sha256": sha256_bytes(inventory_payload),
    }
    return {
        release_path: json_bytes(release),
        site_path: json_bytes(site),
        inventory_path: inventory_payload,
        ROOT / "VERSION": b"1.46\n",
    }


def build_note_index(site_payload: bytes) -> str:
    import generate_note_index as note_index

    existing = [note_index.parse_note(path) for path in note_index.note_files()]
    if len(existing) != 181 or any(note.slug == "r0-73f" for note in existing):
        raise RuntimeError("R0.73F note-index baseline is not exact")
    latest = note_index.Note(
        slug="r0-73f",
        code="R0.73F",
        title="Moving-profile dichotomy and fixed-window exponential gain",
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
        note_index.latest_recap_href = lambda: "/recap-r0-61-r0-73f.html"
        index = note_index.render(notes)
    finally:
        note_index.json = old_json
        note_index.latest_recap_href = old_latest_recap_href
    for token in (
        'data-site-version="1.46"',
        "182 篇公开研究笔记",
        "<strong>R0.73F</strong><span>最新研究节点</span>",
        'data-note="r0-73f"',
        "/recap-r0-61-r0-73f.html",
        "研究笔记总索引 · v1.46 · 2026-08-30",
    ):
        if token not in index:
            raise RuntimeError("R0.73F note index missing token: " + token)
    assert_clean(index, "R0.73F note index")
    assert_public_voice(index, "R0.73F note index")
    return index


def stage_figure_assets(
    staged: dict[Path, bytes],
    figure_manifest: dict,
) -> None:
    source = ROOT / FIGURE_RELATIVE
    target = PUBLIC / "assets/r073f"
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
            raise RuntimeError("R0.73F public figure source is not manifest-bound")
        staged[target / f"{FIGURE_ID}.{suffix}"] = payload


def validate_staged(staged: dict[Path, bytes]) -> None:
    required_paths = (
        PUBLIC / "notes/r0-73f.html",
        PUBLIC / "recap-r0-61-r0-73f.html",
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
            raise RuntimeError("R0.73F transaction is missing staged path " + str(path))
    for path in staged:
        if path.suffix.lower() == ".pdf" and "assets/r073f" not in path.as_posix():
            raise RuntimeError("R0.73F HTML transaction must not generate PDFs")
    for path in (
        PUBLIC / "notes/r0-73f.html",
        PUBLIC / "recap-r0-61-r0-73f.html",
        PUBLIC / "research-review.html",
        PUBLIC / "literature-review.html",
        PUBLIC / "notes/index.html",
    ):
        value = staged[path].decode("utf-8")
        assert_clean(value, path.name)
        assert_mathjax_clean(value, path.name, check_naked=False)
        assert_public_voice(value, path.name)
    note = staged[PUBLIC / "notes/r0-73f.html"].decode("utf-8")
    for token in (CLOSED, FALSE, OPEN, "ONE-ROW LINEAR THEOREM", "NOT CLAY"):
        if token not in note:
            raise RuntimeError("R0.73F staged note lost boundary token")
    recap = staged[PUBLIC / "recap-r0-61-r0-73f.html"].decode("utf-8")
    start = recap.index('<section id="node-index">')
    end = recap.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', recap[start:end])
    if len(links) != 122 or len(set(links)) != 122:
        raise RuntimeError("R0.73F staged recap node inventory is invalid")
    if recap.count('<article class="phase">') != 41:
        raise RuntimeError("R0.73F staged recap phase inventory is invalid")
    home = staged[PUBLIC / "research-review.html"].decode("utf-8")
    route = re.search(
        r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73F">'
        r"(.*?)</nav>",
        home,
        flags=re.S,
    )
    if route is None or len(re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))) != 92:
        raise RuntimeError("R0.73F staged home route inventory is invalid")


def write_temp_for(path: Path, payload: bytes, mode: int) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix="." + path.name + ".r073f-",
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
    staged[PUBLIC / "notes/r0-73f.html"] = build_note().encode("utf-8")
    staged[PUBLIC / "recap-r0-61-r0-73f.html"] = build_recap().encode("utf-8")
    staged[PUBLIC / "research-review.html"] = update_home().encode("utf-8")
    staged[PUBLIC / "literature-review.html"] = update_literature().encode("utf-8")
    manifest_outputs = build_manifest_outputs()
    staged.update(manifest_outputs)
    staged[PUBLIC / "notes/index.html"] = build_note_index(
        staged[PUBLIC / "site-version.json"]
    ).encode("utf-8")
    validate_staged(staged)
    commit_transaction(staged)

    if len(list((PUBLIC / "notes").glob("r0-*.html"))) != 182:
        raise RuntimeError("R0.73F postcommit note count is not 182")
    source = ROOT / FIGURE_RELATIVE
    target = PUBLIC / "assets/r073f"
    for suffix in ("pdf", "svg", "png"):
        if digest(source / f"figure.{suffix}") != digest(
            target / f"{FIGURE_ID}.{suffix}"
        ):
            raise RuntimeError(
                "R0.73F public figure is not byte-identical: " + suffix
            )
    print(json.dumps({
        "release": "R0.73F",
        "siteVersion": "1.46",
        "notes": 182,
        "recapNodes": 122,
        "published": 84,
        "formalSealed": 60,
        "legacyBacklog": 24,
        "phases": 41,
        "routeNotes": 92,
        "next": "R0.73G",
        "rootVersion": "1.46",
        "pdfGenerated": False,
        "translationsGenerated": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
