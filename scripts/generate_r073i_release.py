#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the fail-closed transactional R0.73I GitHub Pages release.

The generator intentionally does not create the note/recap PDFs or English
translations.  Those remain later publication stages.  Until the five sealed
commit pins below are replaced, every validating/applying invocation fails
closed; ``--help`` remains side-effect free.
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
from r073i_release_content import (
    CERTIFICATE_RELATIVE,
    CLOSED,
    FALSE,
    FIGURE_ID,
    FIGURE_RELATIVE,
    HOME_I_CARD,
    HOME_LATEST_SPOTLIGHT,
    HOME_NEXT,
    NOTE_ARTICLE,
    NOTE_HERO,
    OPEN,
    R073H_BASELINE,
    R073I_TARGET,
)


ROOT = Path(os.environ.get(
    "R073I_RELEASE_ROOT", Path(__file__).resolve().parents[1]
)).resolve()
PUBLIC = ROOT / "public"

ANALYTIC_SOURCE_COMMIT = "f8a0879edb8a2a3772bf3bd34f60d900bc367e71"
EXPERIMENT_PACKAGE_COMMIT = "5180ab1f9c4f5955647e0f2a1fcadb070fc407ad"
FIGURE_PACKAGE_COMMIT = "e04f6bf569a91a6814be04fc74409ef02075dc23"
CERTIFICATE_PACKAGE_COMMIT = "4ab51d1251cb5f5ca85c82731ac7f8e7b512c368"
RELEASE_SOURCE_COMMIT = "TO_BE_FILLED_AFTER_RELEASE_SOURCE_COMMIT"

COMMIT_PLACEHOLDERS = (
    ANALYTIC_SOURCE_COMMIT,
    EXPERIMENT_PACKAGE_COMMIT,
    FIGURE_PACKAGE_COMMIT,
    CERTIFICATE_PACKAGE_COMMIT,
    RELEASE_SOURCE_COMMIT,
)

CLOSED_KEYS = (
    "inheritedEndpointStrictlyBelowOneOver450",
    "improvedContinuumUpperAction",
    "zeroWindowTangentAction",
)

FALSE_KEYS = (
    "fixedWindowActionFromInheritedInputs",
    "theoremEndpointEqualsOneOver450",
    "actionLimitAloneGivesBoundedPrefactor",
    "finitePilotProvesContinuumAction",
    "finiteWkbProvesContinuumTwoTermLaw",
)

OPEN_KEYS = (
    "canonicalSelectedBranch",
    "explicitPositiveActionWindow",
    "uniformRankOneViscousBranch",
    "matchingSelectedGainAction",
    "twoTermSelectedGainAsymptotic",
    "actionResolvedBackwardLocalization",
    "prescribedActionSeedDeparture",
    "fixedBackgroundLyapunovInstability",
    "transverseThreeDimensionalClosure",
    "finiteTimeSingularity",
    "Clay",
)

SOURCE_PATHS = (
    "research/r073i_problem_freeze.md",
    "research/r073i_continuum_upper_action_proof.md",
    "research/r073i_zero_window_tangent_proof.md",
    "research/r073i_fixed_window_no_go.md",
    "research/r073i_independent_analytic_audit.md",
    "research/r073i_adversarial_audit.md",
    "research/r073i_literature_audit.md",
    "research/r073i_gap_matrix.md",
    "research/r073i_bilingual_dictionary.md",
    "research/r073i_report-source.md",
)

CERTIFICATE_FILE_PATHS = (
    "README.md",
    "requirements.txt",
    "command.txt",
    "generate_certificate.py",
    "independent_recompute.py",
    "validate_certificate.py",
    "seal_package.py",
    "certificate.json",
    "independent_recompute.json",
    "validation.json",
    "environment.json",
    "progress.ndjson",
)

FIGURE_INPUT_PATHS = (
    "experiments/r073i/action_rows.csv",
    "experiments/r073i/gain_rows.csv",
    "experiments/r073i/summary.json",
    "experiments/r073i/manifest.json",
    "experiments/r073i/SHA256SUMS",
    "research/r073i_continuum_upper_action_proof.md",
    "research/r073h_problem_freeze.md",
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

FIGURE_OUTPUT_PATHS = (
    "source-data.csv",
    "figure.pdf",
    "figure.svg",
    "figure.png",
    "qa-final-size.png",
    "qa-grayscale.png",
    "qa-pdf.png",
    "environment.json",
    "progress.ndjson",
    "results.json",
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
    "results.json",
    "source-data.csv",
    "validate.py",
)

EXPERIMENT_SOURCE_PATHS = (
    "experiments/r073i/README.md",
    "experiments/r073i/command.txt",
    "experiments/r073i/config.json",
    "experiments/r073i/requirements.txt",
    "experiments/r073i/summary.schema.json",
    "experiments/r073i/selected_gain_action_diagnostic.py",
    "experiments/r073i/validate.py",
    "tests/r073i-finite-diagnostic.test.mjs",
)

EXPERIMENT_GENERATED_PATHS = (
    "action_rows.csv",
    "gain_rows.csv",
    "comparison_rows.csv",
    "environment.json",
    "summary.json",
    "progress.ndjson",
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


def verify_hash_rows(
    payload: dict,
    expected_groups: dict[str, tuple[str, ...]],
    base: Path,
    label: str,
) -> None:
    for group, expected_paths in expected_groups.items():
        rows = payload.get(group)
        if not isinstance(rows, list) or not rows:
            raise RuntimeError(label + ": missing nonempty hash group " + group)
        actual_paths: list[str] = []
        for row in rows:
            if not isinstance(row, dict):
                raise RuntimeError(label + ": malformed hash row in " + group)
            relative = str(row.get("path", ""))
            expected = str(row.get("sha256", ""))
            if relative in actual_paths:
                raise RuntimeError(label + ": duplicate hash path in " + group)
            actual_paths.append(relative)
            candidate = (base / relative) if "/" not in relative else (ROOT / relative)
            if not re.fullmatch(r"[0-9a-f]{64}", expected) or not candidate.is_file():
                raise RuntimeError(label + ": missing hash target in " + group + ": " + relative)
            if candidate.is_symlink() or digest(candidate) != expected:
                raise RuntimeError(label + ": stale hash in " + group + ": " + relative)
            if not isinstance(row.get("bytes"), int) or candidate.stat().st_size != row["bytes"]:
                raise RuntimeError(label + ": stale byte count in " + group + ": " + relative)
        if tuple(actual_paths) != expected_paths:
            raise RuntimeError(label + ": exact path inventory drifted in " + group)


def ensure_commits_ready() -> None:
    if any(value.startswith("TO_BE_FILLED_") for value in COMMIT_PLACEHOLDERS):
        raise RuntimeError(
            "R0.73I release is intentionally sealed shut: replace the "
            "release-source commit placeholder after that commit"
        )
    chain = (
        ("analytic source", ANALYTIC_SOURCE_COMMIT),
        ("experiment package", EXPERIMENT_PACKAGE_COMMIT),
        ("figure package", FIGURE_PACKAGE_COMMIT),
        ("certificate package", CERTIFICATE_PACKAGE_COMMIT),
        ("release source", RELEASE_SOURCE_COMMIT),
    )
    for label, commit in chain:
        require_commit(commit, "R0.73I " + label)
    commits = [commit for _, commit in chain]
    if len(commits) != len(set(commits)):
        raise RuntimeError("R0.73I A/E/F/C/R commits must be distinct")
    for (left_label, left), (right_label, right) in zip(chain, chain[1:]):
        if not is_ancestor(left, right):
            raise RuntimeError(f"R0.73I commit order invalid: {left_label} < {right_label}")
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()
    if not is_ancestor(RELEASE_SOURCE_COMMIT, head):
        raise RuntimeError("R0.73I release source commit is not an ancestor of HEAD")


def _gap_status_present(gap: str, key: str, status: str) -> bool:
    escaped = re.escape(key)
    return re.search(
        rf"\|\s*[^|]*`{escaped}`\s*\|\s*{re.escape(status)}\s*\|",
        gap,
    ) is not None


def validate_analytic_sources() -> None:
    for relative in SOURCE_PATHS:
        path = ROOT / relative
        if not path.is_file() or path.is_symlink():
            raise RuntimeError("missing R0.73I analytic source: " + relative)
        if path.read_bytes() != git_bytes(ANALYTIC_SOURCE_COMMIT, relative):
            raise RuntimeError("R0.73I source differs from analytic source commit: " + relative)

    report = (ROOT / "research/r073i_report-source.md").read_text(encoding="utf-8")
    gap = (ROOT / "research/r073i_gap_matrix.md").read_text(encoding="utf-8")
    upper = (ROOT / "research/r073i_continuum_upper_action_proof.md").read_text(encoding="utf-8")
    tangent = (ROOT / "research/r073i_zero_window_tangent_proof.md").read_text(encoding="utf-8")
    no_go = (ROOT / "research/r073i_fixed_window_no_go.md").read_text(encoding="utf-8")
    independent = (ROOT / "research/r073i_independent_analytic_audit.md").read_text(encoding="utf-8")
    adversarial = (ROOT / "research/r073i_adversarial_audit.md").read_text(encoding="utf-8")
    literature = (ROOT / "research/r073i_literature_audit.md").read_text(encoding="utf-8")
    dictionary = (ROOT / "research/r073i_bilingual_dictionary.md").read_text(encoding="utf-8")

    for key in CLOSED_KEYS:
        if not _gap_status_present(gap, key, "CLOSED"):
            raise RuntimeError("R0.73I CLOSED ledger drift: " + key)
    for key in FALSE_KEYS:
        if not _gap_status_present(gap, key, "FALSE AS INFERENCE"):
            raise RuntimeError("R0.73I FALSE-AS-INFERENCE ledger drift: " + key)
    for key in OPEN_KEYS:
        if not _gap_status_present(gap, key, "OPEN"):
            raise RuntimeError("R0.73I OPEN ledger drift: " + key)

    theorem_tokens = (
        "d_0<\\frac{\\sqrt{19/180}}{392}",
        "\\Omega_H(D)",
        "-\\frac D4",
        "zero-window tangent",
        "fixed positive window",
    )
    for token in theorem_tokens:
        if token not in report and token not in upper and token not in tangent:
            raise RuntimeError("R0.73I theorem source missing token: " + token)
    for token in ("aD", "\\kappa D^2", "\\varepsilon^{-1}", "FALSE AS INFERENCE"):
        if token not in no_go and token not in report:
            raise RuntimeError("R0.73I no-go source missing token: " + token)
    if "MATHEMATICAL FINAL PASS" not in independent:
        raise RuntimeError("R0.73I independent audit is not final pass")
    if "No adversarial test above invalidates" not in adversarial:
        raise RuntimeError("R0.73I adversarial audit verdict drifted")
    for token in (
        "10.1088/0305-4470/25/21/027",
        "math-ph/0607054",
        "math-ph/0608059",
        "1804.11213",
        "2509.18070",
        "2312.16938",
    ):
        if token not in literature:
            raise RuntimeError("R0.73I literature audit missing primary-source token: " + token)
    for token in (
        "inherited endpoint", "zero-window tangent action",
        "fixed-window action", "FALSE AS INFERENCE",
    ):
        if token not in dictionary:
            raise RuntimeError("R0.73I bilingual dictionary missing token: " + token)

    for label, value in (
        ("report", report), ("gap", gap), ("upper proof", upper),
        ("tangent proof", tangent), ("no-go", no_go),
        ("independent audit", independent), ("adversarial audit", adversarial),
        ("literature", literature), ("dictionary", dictionary),
    ):
        assert_public_voice(value, "R0.73I " + label)


def validate_certificate() -> dict:
    directory = ROOT / CERTIFICATE_RELATIVE
    verify_exact_directory_at_commit(directory, CERTIFICATE_PACKAGE_COMMIT, "R0.73I certificate")
    verify_flat_ledger(directory, "R0.73I certificate")
    manifest = strict_json(directory / "manifest.json", "R0.73I certificate manifest")
    certificate = strict_json(directory / "certificate.json", "R0.73I certificate")
    validation = strict_json(directory / "validation.json", "R0.73I certificate validation")
    independent = strict_json(directory / "independent_recompute.json", "R0.73I independent recompute")
    schemas = {
        "manifest": (manifest, "r073i-certificate-manifest-v1"),
        "certificate": (certificate, "r073i-exact-certificate-v1"),
        "validation": (validation, "r073i-certificate-validation-v1"),
        "independent": (independent, "r073i-independent-recompute-v1"),
    }
    for label, (payload, expected_schema) in schemas.items():
        if payload.get("schemaVersion") != expected_schema:
            raise RuntimeError("R0.73I certificate " + label + " schema drifted")
    if (
        manifest.get("release") != "R0.73I"
        or manifest.get("status") != "formal"
        or manifest.get("allPrerequisiteChecksPass") is not True
        or manifest.get("sourceCommit") != FIGURE_PACKAGE_COMMIT
    ):
        raise RuntimeError("R0.73I certificate manifest failed or lost provenance")
    if certificate.get("sourceCommit") != FIGURE_PACKAGE_COMMIT:
        raise RuntimeError("R0.73I certificate source binding drifted")
    if (
        certificate.get("allChecksPass") is not True
        or validation.get("allChecksPass") is not True
        or independent.get("allChecksPass") is not True
    ):
        raise RuntimeError("R0.73I exact or independent certificate failed")

    expected_ledger = {
        "Clay": "OPEN",
        "actionLimitAloneGivesBoundedPrefactor": "FALSE_AS_INFERENCE",
        "canonicalSelectedBranch": "OPEN",
        "finitePilotProvesContinuumAction": "FALSE_AS_INFERENCE",
        "finiteTimeSingularity": "OPEN",
        "fixedBackgroundLyapunovInstability": "OPEN",
        "fixedWindowActionFromInheritedInputs": "FALSE_AS_INFERENCE",
        "improvedContinuumUpperAction": "CLOSED",
        "inheritedEndpointStrictlyBelowOneOver450": "CLOSED",
        "matchingSelectedGainAction": "OPEN",
        "prescribedActionSeedDeparture": "OPEN",
        "transverseThreeDimensionalClosure": "OPEN",
        "zeroWindowTangentAction": "CLOSED",
    }
    if certificate.get("claimLedger") != expected_ledger:
        raise RuntimeError("R0.73I certificate claim ledger is not exact")
    endpoint = certificate.get("endpointAudit", {})
    upper = certificate.get("continuumUpperAction", {})
    tangent = certificate.get("zeroWindowTangent", {})
    finite = certificate.get("finiteDiagnostic", {})
    if endpoint.get("d0StrictUpperBoundExpression") != "sqrt(19/180)/392":
        raise RuntimeError("R0.73I endpoint certificate drifted")
    if upper.get("range") != "0<=D<=1/450" or upper.get("matchingActionClaimed") is not False:
        raise RuntimeError("R0.73I upper-action boundary drifted")
    if (
        tangent.get("fixedPositiveWindowLimitClaimed") is not False
        or tangent.get("jointTwoParameterLimitClaimed") is not False
    ):
        raise RuntimeError("R0.73I zero-window quantifier boundary drifted")
    finite_boundary = finite.get("claimBoundary", {})
    if (
        finite.get("diagnosticOnly") is not True
        or finite_boundary.get("finiteActionIsContinuumAction") is not False
        or finite_boundary.get("finiteWkbCorrectionIsAsymptoticTheorem") is not False
        or finite_boundary.get("oneOver450IsTheoremEndpoint") is not False
        or finite.get("counts") != {
            "actionRows": 18, "comparisonRows": 36,
            "gainRows": 36, "windowCount": 3,
        }
    ):
        raise RuntimeError("R0.73I finite diagnostic escaped its boundary")
    windows = finite.get("windowSummaries", [])
    if (
        not isinstance(windows, list)
        or [row.get("windowId") for row in windows] != [
            "explicit-pilot", "analytic-upper-bound", "one-over-450"
        ]
        or abs(float(windows[-1].get("endpoint", 0)) - 1 / 450) > 1e-15
        or "not the currently known theorem endpoint" not in str(windows[-1].get("role", ""))
    ):
        raise RuntimeError("R0.73I finite window inventory drifted")

    bindings = certificate.get("sourceBindings")
    expected_binding_paths = (
        "research/r073i_problem_freeze.md",
        "research/r073i_continuum_upper_action_proof.md",
        "research/r073i_zero_window_tangent_proof.md",
        "research/r073i_fixed_window_no_go.md",
        "research/r073i_gap_matrix.md",
        "research/r073i_report-source.md",
        "research/r073i_bilingual_dictionary.md",
        "research/r073i_independent_analytic_audit.md",
        "research/r073i_adversarial_audit.md",
        "research/r073i_literature_audit.md",
        "experiments/r073i/selected_gain_action_diagnostic.py",
        "experiments/r073i/validate.py",
        "experiments/r073i/config.json",
        "experiments/r073i/summary.json",
        "experiments/r073i/manifest.json",
    )
    verify_hash_rows(
        {"sourceBindings": bindings},
        {"sourceBindings": expected_binding_paths},
        directory,
        "R0.73I certificate source bindings",
    )
    for row in bindings:
        if git_bytes(FIGURE_PACKAGE_COMMIT, row["path"]) != (ROOT / row["path"]).read_bytes():
            raise RuntimeError("R0.73I certificate input differs from figure-package source commit")
    verify_hash_rows(
        manifest,
        {"files": CERTIFICATE_FILE_PATHS},
        directory,
        "R0.73I certificate manifest",
    )
    return certificate


def validate_experiment() -> dict:
    directory = ROOT / "experiments/r073i"
    verify_exact_directory_at_commit(directory, EXPERIMENT_PACKAGE_COMMIT, "R0.73I experiment")
    verify_flat_ledger(directory, "R0.73I experiment")
    manifest = strict_json(directory / "manifest.json", "R0.73I experiment manifest")
    summary = strict_json(directory / "summary.json", "R0.73I experiment summary")
    if manifest.get("schemaVersion") != "r073i-finite-manifest-v1":
        raise RuntimeError("R0.73I experiment manifest schema drifted")
    if summary.get("schemaVersion") != "r073i-finite-summary-v1":
        raise RuntimeError("R0.73I experiment summary schema drifted")
    if (
        manifest.get("release") != "R0.73I-finite-diagnostic"
        or manifest.get("sourceCommit") != ANALYTIC_SOURCE_COMMIT
        or manifest.get("allChecksPass") is not True
        or manifest.get("diagnosticOnly") is not True
        or manifest.get("smokeMode") is not False
        or summary.get("allChecksPass") is not True
        or summary.get("diagnosticOnly") is not True
    ):
        raise RuntimeError("R0.73I finite experiment failed or escaped scope")
    boundary = manifest.get("claimBoundary", {})
    if summary.get("claimBoundary") != boundary or boundary != {
        "analyticUpperBoundEqualsD0": False,
        "clayProblemSolved": False,
        "finiteActionIsContinuumAction": False,
        "finiteBinary64GalerkinDiagnostic": True,
        "finiteWkbCorrectionIsAsymptoticTheorem": False,
        "matchingContinuumGainActionEstablished": False,
        "oneOver450IsTheoremEndpoint": False,
        "ordinaryCutoffAgreementIsTailProof": False,
        "prescribedActionSeedDepartureEstablished": False,
        "selectedFiniteBranchIsContinuumBranch": False,
    }:
        raise RuntimeError("R0.73I finite experiment claim boundary drifted")
    if summary.get("counts") != {
        "actionRows": 18, "comparisonRows": 36,
        "gainRows": 36, "windowCount": 3,
    }:
        raise RuntimeError("R0.73I finite experiment row inventory drifted")
    verify_hash_rows(
        manifest,
        {
            "sourceBindings": EXPERIMENT_SOURCE_PATHS,
            "generatedBindings": EXPERIMENT_GENERATED_PATHS,
        },
        directory,
        "R0.73I experiment manifest",
    )
    for row in manifest.get("sourceBindings", []):
        if git_bytes(ANALYTIC_SOURCE_COMMIT, row["path"]) != (ROOT / row["path"]).read_bytes():
            raise RuntimeError("R0.73I experiment source differs from analytic commit")
    return manifest


def validate_figure(certificate: dict) -> dict:
    directory = ROOT / FIGURE_RELATIVE
    verify_exact_directory_at_commit(directory, FIGURE_PACKAGE_COMMIT, "R0.73I figure")
    verify_flat_ledger(directory, "R0.73I figure")
    manifest = strict_json(directory / "manifest.json", "R0.73I figure manifest")
    results = strict_json(directory / "results.json", "R0.73I figure results")
    contract = strict_json(directory / "contract.json", "R0.73I figure contract")
    config = strict_json(directory / "config.json", "R0.73I figure config")
    schemas = {
        "manifest": (manifest, "r073i-action-boundary-manifest-v1"),
        "results": (results, "r073i-action-boundary-results-v1"),
        "contract": (contract, "r073i-action-boundary-contract-v1"),
        "config": (config, "r073i-action-boundary-config-v1"),
    }
    for label, (payload, expected_schema) in schemas.items():
        if payload.get("schemaVersion") != expected_schema:
            raise RuntimeError("R0.73I figure " + label + " schema drifted")
    if (
        manifest.get("release") != "R0.73I"
        or manifest.get("figureId") != FIGURE_ID
        or manifest.get("status") != "formal"
        or manifest.get("diagnosticOnly") is not True
        or manifest.get("sourceCommit") != EXPERIMENT_PACKAGE_COMMIT
    ):
        raise RuntimeError("R0.73I figure status or provenance drifted")
    if (
        results.get("sourceCommit") != EXPERIMENT_PACKAGE_COMMIT
        or results.get("status") != "passed"
        or results.get("diagnosticOnly") is not True
    ):
        raise RuntimeError("R0.73I figure results failed or lost provenance")
    boundary = contract.get("claimBoundary", {})
    expected_boundary = {
        "formalFiniteDiagnosticFigure": True,
        "experimentInputsPassedTheirFiniteValidator": True,
        "finiteActionIsContinuumAction": False,
        "finiteWkbCorrectionIsAsymptoticTheorem": False,
        "ordinaryCutoffAgreementIsTailProof": False,
        "inverseLambdaGuideIsFittedRateOrProof": False,
        "analyticUpperBoundEqualsD0": False,
        "oneOver450IsTheoremEndpoint": False,
        "matchingContinuumGainActionEstablished": False,
        "clayProblemSolved": False,
    }
    if (
        boundary != expected_boundary
        or manifest.get("claimBoundary") != expected_boundary
        or results.get("claimBoundary") != expected_boundary
    ):
        raise RuntimeError("R0.73I figure escaped its exact claim boundary")
    if certificate.get("finiteDiagnostic", {}).get("diagnosticOnly") is not True:
        raise RuntimeError("R0.73I figure lacks a diagnostic-only certificate parent")

    verify_hash_rows(
        manifest,
        {
            "inputBindings": FIGURE_INPUT_PATHS,
            "sourceBindings": FIGURE_SOURCE_PATHS,
            "outputBindings": FIGURE_OUTPUT_PATHS,
        },
        directory,
        "R0.73I figure manifest",
    )
    for row in manifest.get("inputBindings", []):
        if git_bytes(EXPERIMENT_PACKAGE_COMMIT, row["path"]) != (ROOT / row["path"]).read_bytes():
            raise RuntimeError("R0.73I figure input differs from experiment-package commit")
    for row in manifest.get("sourceBindings", []):
        relative = f"{FIGURE_RELATIVE}/{row['path']}"
        if git_bytes(EXPERIMENT_PACKAGE_COMMIT, relative) != (directory / row["path"]).read_bytes():
            raise RuntimeError("R0.73I figure source differs from experiment-package commit")

    if tuple(path.name for path in sorted(directory.iterdir())) != tuple(sorted(FIGURE_PACKAGE_PATHS)):
        raise RuntimeError("R0.73I figure package inventory drifted")
    outputs = {row["path"]: row for row in manifest.get("outputBindings", [])}
    if set(name for name in outputs if name.startswith("figure.")) != {
        "figure.pdf", "figure.svg", "figure.png"
    }:
        raise RuntimeError("R0.73I figure master inventory is not exact")
    if not (directory / "figure.pdf").read_bytes().startswith(b"%PDF"):
        raise RuntimeError("R0.73I figure PDF signature invalid")
    svg = (directory / "figure.svg").read_text(encoding="utf-8").lower()
    if "<svg" not in svg or "<image" in svg or "<text" not in svg:
        raise RuntimeError("R0.73I figure SVG is absent or rasterized")
    png = (directory / "figure.png").read_bytes()
    if not png.startswith(b"\x89PNG\r\n\x1a\n") or b"pHYs" not in png:
        raise RuntimeError("R0.73I figure PNG metadata missing")
    if results.get("sourceDataRows") != 28 or results.get("panelA", {}).get("finiteRowCount") != 9:
        raise RuntimeError("R0.73I figure finite row inventory drifted")
    if results.get("panelB", {}).get("finiteRowCount") != 15:
        raise RuntimeError("R0.73I figure WKB row inventory drifted")
    return manifest


def validate_inputs() -> tuple[dict, dict]:
    ensure_commits_ready()
    validate_analytic_sources()
    validate_experiment()
    certificate = validate_certificate()
    figure = validate_figure(certificate)
    return certificate, figure


def _target_html() -> dict[str, str]:
    target: dict[str, str] = {}
    for relative in (
        "notes/r0-73i.html",
        "recap-r0-61-r0-73i.html",
        "research-review.html",
        "literature-review.html",
        "notes/index.html",
    ):
        path = PUBLIC / relative
        if not path.is_file() or path.is_symlink():
            raise RuntimeError("R0.73I target HTML missing: " + relative)
        value = path.read_text(encoding="utf-8")
        assert_clean(value, "R0.73I target " + relative)
        assert_mathjax_clean(value, "R0.73I target " + relative, check_naked=True)
        assert_public_voice(value, "R0.73I target " + relative)
        if "/i18n-en.js?v=1.49" not in value:
            raise RuntimeError("R0.73I target HTML has stale i18n cache: " + relative)
        target[relative] = value
    return target


def preflight_release_state() -> str:
    release = strict_json(ROOT / "research/release-manifest.json", "release manifest")
    site = strict_json(PUBLIC / "site-version.json", "site version")
    inventory = strict_json(ROOT / "research/formal-archive-inventory.json", "archive inventory")
    root_version = (ROOT / "VERSION").read_text(encoding="utf-8")

    if release.get("latestCompletedRelease") == "r073i":
        for key, value in R073I_TARGET.items():
            if release.get(key) != value:
                raise RuntimeError("R0.73I target release-manifest drifted: " + key)
        if release.get("latestReleaseGate") != "tests/r073i-action-boundary-gate.test.mjs":
            raise RuntimeError("R0.73I target gate binding drifted")
        if release.get("latestReleasePublicationTest") != "tests/r073i-release.test.mjs":
            raise RuntimeError("R0.73I target publication-test binding drifted")
        if site != {
            "schemaVersion": "research-site-version-v1",
            "version": "1.49",
            "latestRelease": "R0.73I",
            "publicHtmlNoteCount": 185,
            "publishedDate": "2026-08-30",
        }:
            raise RuntimeError("R0.73I target site-version is not exact")
        if root_version != "1.49\n":
            raise RuntimeError("R0.73I target VERSION is not 1.49")
        state = (
            inventory.get("latestPublishedRelease"),
            inventory.get("publishedReleaseCount"),
            inventory.get("formalSealedReleaseCount"),
            inventory.get("legacyFormalFigureBacklogCount"),
        )
        if state != ("r073i", 87, 63, 24):
            raise RuntimeError("R0.73I target formal archive is not exact")

        baseline_inventory = json.loads(git_bytes(
            RELEASE_SOURCE_COMMIT, "research/formal-archive-inventory.json"
        ))
        expected_inventory = json.loads(json.dumps(baseline_inventory))
        for key in ("publishedReleases", "formalSealedReleases"):
            rows = expected_inventory.get(key)
            if not isinstance(rows, list) or rows[-1:] != ["r073h"] or "r073i" in rows:
                raise RuntimeError("R0.73I sealed baseline inventory is invalid: " + key)
            rows.append("r073i")
        expected_inventory.update({
            "latestPublishedRelease": "r073i",
            "publishedReleaseCount": 87,
            "formalSealedReleaseCount": 63,
            "legacyFormalFigureBacklogCount": 24,
        })
        if inventory != expected_inventory:
            raise RuntimeError("R0.73I target formal archive is not the exact append-only successor")
        for key, count in (("publishedReleases", 87), ("formalSealedReleases", 63)):
            rows = inventory[key]
            if len(rows) != count or len(set(rows)) != count:
                raise RuntimeError("R0.73I target archive sequence is not unique: " + key)
        if not set(inventory["formalSealedReleases"]).issubset(inventory["publishedReleases"]):
            raise RuntimeError("R0.73I sealed releases are not a subset of published releases")
        if release.get("formalArchiveInventory") != {
            "path": "research/formal-archive-inventory.json",
            "sha256": digest(ROOT / "research/formal-archive-inventory.json"),
        }:
            raise RuntimeError("R0.73I target archive-inventory binding drifted")
        if len(list((PUBLIC / "notes").glob("r0-*.html"))) != 185:
            raise RuntimeError("R0.73I target note count is not 185")

        html = _target_html()
        note = html["notes/r0-73i.html"]
        for token in (
            CLOSED, FALSE, OPEN, "NOT CLAY", "FALSE_AS_INFERENCE",
            "先固定窗口取", "三个窗口分开标记", "不证明连续体两项式",
        ):
            if token not in note:
                raise RuntimeError("R0.73I target note lost boundary token: " + token)
        recap = html["recap-r0-61-r0-73i.html"]
        start = recap.find('<section id="node-index">')
        end = recap.find("</section>", start)
        if start < 0 or end <= start:
            raise RuntimeError("R0.73I target recap node index is absent")
        links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', recap[start:end])
        if len(links) != 125 or len(set(links)) != 125:
            raise RuntimeError("R0.73I target recap is not 125 unique nodes")
        if recap.count('<article class="phase">') != 44:
            raise RuntimeError("R0.73I target recap is not 44 phases")
        for token in (
            "87</strong><span>R0.70A–R0.73I 已公开版本",
            "63</strong><span>当前 formal-figure 合同下完整封存",
            "24</strong><span>旧版附图档案待回补",
        ):
            if token not in recap:
                raise RuntimeError("R0.73I target recap accounting drifted")
        home = html["research-review.html"]
        route = re.search(
            r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73I">(.*?)</nav>',
            home, flags=re.S,
        )
        route_links = [] if route is None else re.findall(
            r'href="/notes/(r0-[^"]+)\.html"', route.group(1)
        )
        if len(route_links) != 95 or len(set(route_links)) != 95:
            raise RuntimeError("R0.73I target home route is not 95 unique links")
        if home.count('data-release="r073i"') != 1 or "/notes/r0-73i.html" not in home:
            raise RuntimeError("R0.73I target home card is absent")
        literature = html["literature-review.html"]
        if (
            'id="r073i-boundary"' not in literature
            or 'class="route-r073i-deck-update"' not in literature
            or "没有直接给出本题固定正窗口的 matching action" not in literature
        ):
            raise RuntimeError("R0.73I target literature boundary is absent")
        if 'data-note="r0-73i"' not in html["notes/index.html"]:
            raise RuntimeError("R0.73I target note-index entry is absent")
        return "target"

    if any(release.get(key) != value for key, value in R073H_BASELINE.items()):
        raise RuntimeError("R0.73I release state is neither exact R0.73H source nor exact R0.73I target")
    if site != {
        "schemaVersion": "research-site-version-v1",
        "version": "1.48",
        "latestRelease": "R0.73H",
        "publicHtmlNoteCount": 184,
        "publishedDate": "2026-08-30",
    }:
        raise RuntimeError("R0.73I site-version baseline is not exact")
    if root_version != "1.48\n":
        raise RuntimeError("R0.73I VERSION baseline is not 1.48")
    state = (
        inventory.get("latestPublishedRelease"), inventory.get("publishedReleaseCount"),
        inventory.get("formalSealedReleaseCount"), inventory.get("legacyFormalFigureBacklogCount"),
    )
    if state != ("r073h", 86, 62, 24):
        raise RuntimeError("R0.73I formal archive baseline is not exact")
    if len(list((PUBLIC / "notes").glob("r0-*.html"))) != 184:
        raise RuntimeError("R0.73I expected exactly 184 baseline HTML notes")
    for path in (
        PUBLIC / "notes/r0-73i.html",
        PUBLIC / "notes/r0-73i.pdf",
        PUBLIC / "recap-r0-61-r0-73i.html",
        PUBLIC / "recap-r0-61-r0-73i.pdf",
        PUBLIC / "assets/r073i",
        PUBLIC / FIGURE_RELATIVE,
    ):
        if path.exists() or path.is_symlink():
            raise RuntimeError("R0.73I baseline path already exists: " + str(path))
    for relative, tokens in {
        "research-review.html": ("R0.73H", "184", "R0.73I"),
        "literature-review.html": ("R0.73H", "开放接口 · R0.73I"),
        "notes/index.html": ("R0.73H", "184 篇公开研究笔记"),
        "recap-r0-61-r0-73h.html": ("R0.61–R0.73H", "124", "43 个研究阶段"),
    }.items():
        value = (PUBLIC / relative).read_text(encoding="utf-8")
        for token in tokens:
            if token not in value:
                raise RuntimeError(f"R0.73I baseline {relative} missing {token}")
    return "source"


def build_note() -> str:
    html = (PUBLIC / "notes/r0-73h.html").read_text(encoding="utf-8")
    metadata = (
        ("description", r'<meta name="description" content=".*?">',
         '<meta name="description" content="研究笔记 R0.73I：继承端点校正、连续体上作用量与零窗口切向速率已闭合；固定正窗口的匹配作用量仍开放。">'),
        ("og title", r'<meta property="og:title" content=".*?">',
         '<meta property="og:title" content="R0.73I｜Selected-gain action endpoint audit">'),
        ("og description", r'<meta property="og:description" content=".*?">',
         '<meta property="og:description" content="A continuum upper action and zero-window tangent rate are proved; fixed-window matching action and bounded prefactor remain open.">'),
        ("og image", r'<meta property="og:image" content=".*?">',
         f'<meta property="og:image" content="https://kasifa.github.io/assets/r073i/{FIGURE_ID}.png">'),
        ("title", r'<title>.*?</title>',
         '<title>R0.73I｜Selected-gain action endpoint audit</title>'),
    )
    for label, pattern, value in metadata:
        html = section(html, pattern, value, "H note " + label)
    html = required(html, "/i18n-en.js?v=1.48", "/i18n-en.js?v=1.49", "H note i18n")
    toc_items = (
        ("result", "00 · direct decision"),
        ("endpoint", "01 · inherited endpoint"),
        ("upper", "02 · continuum upper action"),
        ("tangent", "03 · zero-window tangent"),
        ("quantifiers", "04 · quantifier order"),
        ("selection", "05 · selection no-go"),
        ("prefactor", "06 · prefactor no-go"),
        ("seed", "07 · prescribed seed"),
        ("finite", "08 · finite action diagnostic"),
        ("wkb", "09 · finite WKB diagnostic"),
        ("certificate", "10 · certificate"),
        ("literature", "11 · literature boundary"),
        ("audit", "12 · independent audit"),
        ("figure", "13 · journal figure"),
        ("boundary", "14 · exact boundary"),
        ("value", "15 · value"),
        ("next", "16 · R0.73J"),
        ("reproduce", "17 · reproduction"),
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
        '<div>研究笔记 R0.73I · 2026-08-30<br><a href="/">返回研究主页</a></div></footer>'
    )
    html = section(html, r"<footer>.*?</footer>", footer, "H note footer")
    match = re.search(r"<nav>(.*?)</nav>", html, flags=re.S)
    anchors = re.findall(r'href="#([^"]+)"', match.group(1)) if match else []
    expected = [anchor for anchor, _ in toc_items]
    if anchors != expected or len(anchors) != len(set(anchors)):
        raise RuntimeError("R0.73I note nav anchors are not unique and ordered")
    assert_clean(html, "R0.73I note")
    assert_mathjax_clean(html, "R0.73I note", check_naked=True)
    assert_public_voice(html, "R0.73I note")
    return html


def build_recap() -> str:
    html = (PUBLIC / "recap-r0-61-r0-73h.html").read_text(encoding="utf-8")
    metadata = (
        ("description", r'<meta name="description" content=".*?">',
         '<meta name="description" content="R0.60 之后的完整研究回顾：R0.61 到 R0.73I 共 125 个节点；最新一节校正继承端点并分离零窗口切向速率与固定窗口作用量。">'),
        ("og title", r'<meta property="og:title" content=".*?">',
         '<meta property="og:title" content="R0.61–R0.73I｜R0.60 之后的研究回顾">'),
        ("og description", r'<meta property="og:description" content=".*?">',
         '<meta property="og:description" content="44 个阶段、125 个节点：从约化递推和环带排除到选定增益作用量的端点审计。">'),
        ("title", r"<title>.*?</title>",
         "<title>R0.61–R0.73I｜R0.60 之后的研究回顾</title>"),
    )
    for label, pattern, value in metadata:
        html = section(html, pattern, value, "H recap " + label)
    html = required(html, "/i18n-en.js?v=1.48", "/i18n-en.js?v=1.49", "H recap i18n")
    hero = r'''    <header class="hero"><div class="hero-inner"><div><div class="eyebrow">累计回顾 · R0.61–R0.73I · 2026-08-30</div><h1>R0.60 之后的研究回顾</h1><p class="lead">这页保留 R0.61 到 R0.73I 的全部 125 个节点。R0.61–R0.69W 从约化递推走到严格环带排除；R0.70A–R0.71Z 检查移动尺度、临界账本、内部 entry 与 complete-root 边界；R0.72A–R0.73B 处理 strong coupling、critical log、碰撞几何与完整线性 Fourier--Leray 行；R0.73C–F 依次认证冻结 Rayleigh 不稳定、黏性谱簇持续、固定正半平面传递和移动剖面固定窗口增益；R0.73G–H 从过小种子的相对放大推进到按实际增益归一化的平面固定距离偏离；R0.73I 校正继承端点，证明连续体上作用量与零窗口切向速率，同时用精确反例隔离固定窗口 matching action 和 bounded prefactor 的缺口。预设指数种子、固定背景、横向三维、奇性与 Clay 没有被外推。</p></div><div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.73I</strong><p>收录节点：125</p><p>回顾截止时公开笔记：185</p><p>回顾截止节点：R0.73I</p><p>问题状态：仍未解决</p></div></div></header>'''
    html = section(html, r'    <header class="hero">.*?</header>', hero, "H recap hero")
    for old, new in (
        ("02 · 124 节完整索引", "02 · 125 节完整索引"),
        ("01 · 43 个研究阶段", "01 · 44 个研究阶段"),
        ("R0.60 之后的路线分成 43 个阶段", "R0.60 之后的路线分成 44 个阶段"),
        ('data-current-route="R0.69P–R0.73H"', 'data-current-route="R0.69P–R0.73I"'),
    ):
        html = required(html, old, new, "H recap counter")
    result = r'''        <section id="result"><div class="section-no">00 / 回顾范围</div><h2>版本数、封存数和数学结论分开报告</h2><div class="metrics"><div class="metric"><strong>125</strong><span>R0.61–R0.73I 研究节点</span></div><div class="metric"><strong>87</strong><span>R0.70A–R0.73I 已公开版本</span></div><div class="metric"><strong>63</strong><span>当前 formal-figure 合同下完整封存</span></div><div class="metric"><strong>24</strong><span>旧版附图档案待回补</span></div></div><p>R0.00–R0.60 保留在上一份阶段回顾。R0.70A–R0.73I 的 87 个版本已经公开，其中 63 个满足当前完整封存合同，24 个历史版本仍欠 formal-figure 回补。公开和封存不表示 Clay 问题已经解决。</p></section>'''
    html = section(html, r'        <section id="result">.*?</section>', result, "H recap result")
    phase = r'''            <article class="phase"><h3>R0.73I · Endpoint audit, upper action, and zero-window tangent</h3><p>解析部分证明继承端点满足 \(D=d_0<\sqrt{19/180}/392<1/450\)，并给出完整传播子的连续体一侧作用量与严格黏性因子。完整顶谱块的最小、最大增益只在先 \(\varepsilon\downarrow0\)、再 \(D\downarrow0\) 的顺序下共享切向速率 \(a\)。</p><p>两个精确有限维反例证明：现有抽象输入不能推出固定正窗口的唯一作用量或有界前因子。\(N=48\) binary64 的三个 action/WKB 窗口均为有限诊断；\(D_{\rm ub}\) 只是 \(d_0\) 的严格上界，\(1/450\) 位于继承定理端点之外。</p><p>__CLOSED__。__FALSE__。__OPEN__。</p><div class="links"><a href="/notes/r0-73i.html">R0.73I</a><a href="/assets/r073i/__FIGURE_ID__.pdf">R0.73I 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073i">R0.73I 证书</a></div></article>
'''.replace("__CLOSED__", CLOSED).replace("__FALSE__", FALSE).replace("__OPEN__", OPEN).replace("__FIGURE_ID__", FIGURE_ID)
    marker = '          </div>\n        </section>\n\n        <section id="node-index">'
    html = once(html, marker, phase + marker, "H recap phase")
    html = required(html, "R0.61–R0.73H 的 124 节公开笔记", "R0.61–R0.73I 的 125 节公开笔记", "H recap node title")
    node_h = '            <span class="node-ref"><a href="/notes/r0-73h.html">R0.73H</a><span class="node-state kind-closed">闭</span></span>\n'
    node_i = '            <span class="node-ref"><a href="/notes/r0-73i.html">R0.73I</a><span class="node-state kind-closed">闭</span></span>\n'
    html = once(html, node_h, node_h + node_i, "H recap node")
    retained = '            <li>R0.73I 校正继承端点并闭合连续体上作用量与零窗口切向速率；固定正窗口的规范谱支、匹配作用量、有界前因子、固定背景、横向三维、奇性与 Clay 保持 OPEN。</li>\n'
    html = once(html, "          </ul>\n          <p>这些结果可以分别整理成", retained + "          </ul>\n          <p>这些结果可以分别整理成", "H recap retained")
    value = r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>零窗口切向速率不等于固定窗口 matching action</h2><p>不能把 125 个节点或 87 个公开版本解释成 Clay 完成比例。R0.73I 的严格增量是端点校正、连续体一侧上作用量与迭代零窗口切向定理；固定正窗口的唯一简单谱支、两侧作用量和有界前因子仍未证明。有限 WKB 吻合只提供下一步的围道与绝热路线信息。</p></section>'''
    html = section(html, r'        <section id="value">.*?</section>', value, "H recap value")
    next_gate = r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.73J 认证唯一简单右端谱支</h2><p>先在显式正窗口上计数 Rayleigh/Evans 零点、证明简单性并排除更右谱点；然后再处理黏性谱支与非自伴绝热余项。该门未闭合前，不把有限矩阵谱支当作连续体 matching action。</p></section>'''
    html = section(html, r'        <section id="next">.*?</section>', next_gate, "H recap next")
    claims = r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>定理、有限计算、反例和开放问题分开列示</h2><p>R0.70A–R0.73I 的 87 节已公开；63 节完整封存；24 节旧档待回补。</p><p>__CLOSED__。</p><p>__FALSE__。</p><p>__OPEN__。</p><p><code>FALSE_AS_INFERENCE</code> 只否定从现有输入推出目标结论；它不否定真实 PDE 算子可能具有固定窗口 matching action。</p></section>'''
    claims = claims.replace("__CLOSED__", CLOSED).replace("__FALSE__", FALSE).replace("__OPEN__", OPEN)
    html = section(html, r'        <section id="claims">.*?</section>', claims, "H recap claims")
    reproduce = r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证明、反例、审计、证书、附图和历史回顾</h2><p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-73h.html">保留 R0.73H 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-73i.html">打开最新节点 R0.73I</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073i_continuum_upper_action_proof.md">查看上作用量证明</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073i_zero_window_tangent_proof.md">查看零窗口证明</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073i_fixed_window_no_go.md">查看固定窗口反例</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073i">查看正式证书</a> · <a href="/assets/r073i/__FIGURE_ID__.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-73i.pdf">下载同步 PDF</a></p><p>连续体结论来自解析证明和独立解析审计；三个 Fourier--Galerkin 窗口只作有限诊断。</p></section>'''.replace("__FIGURE_ID__", FIGURE_ID)
    html = section(html, r'        <section id="reproduce">.*?</section>', reproduce, "H recap reproduce")
    footer = '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>我按原编号记录定理、有限计算、反例和未解决的问题。</div><div>R0.61–R0.73I 回顾 · 2026-08-30<br><a href="/">返回研究主页</a></div></footer>'
    html = section(html, r"<footer>.*?</footer>", footer, "H recap footer")
    start = html.index('<section id="node-index">')
    end = html.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', html[start:end])
    if len(links) != 125 or len(set(links)) != 125:
        raise RuntimeError("R0.73I recap expected 125 unique nodes")
    if html.count('<article class="phase">') != 44:
        raise RuntimeError("R0.73I recap expected 44 phases")
    if "R0.60 之后的研究回顾" not in html or ">R0.61<" not in html:
        raise RuntimeError("R0.73I recap must start after R0.60, at R0.61")
    assert_clean(html, "R0.73I recap")
    assert_mathjax_clean(html, "R0.73I recap", check_naked=True)
    assert_public_voice(html, "R0.73I recap")
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
        ('data-site-version="1.48"', 'data-site-version="1.49"'),
        ("/i18n-en.js?v=1.48", "/i18n-en.js?v=1.49"),
        ("/site-refresh.js?v=1.48", "/site-refresh.js?v=1.49"),
        ("<strong>v1.48</strong>网页版本", "<strong>v1.49</strong>网页版本"),
        ("<strong>184</strong>公开研究笔记", "<strong>185</strong>公开研究笔记"),
        ("<strong>R0.73H</strong>最新研究节点", "<strong>R0.73I</strong>最新研究节点"),
        ('<a class="route-map-latest" href="#r073h">跳到首页 R0.73H 卡片 →</a>',
         '<a class="route-map-latest" href="#r073i">跳到首页 R0.73I 卡片 →</a>'),
        ("selected gain matching action / prescribed seed scale",
         "rightmost continuum branch / fixed-window action"),
        ("Research topology · R0.1–R0.73H", "Research topology · R0.1–R0.73I"),
        ("R0.70A–R0.73H：86 节已公开，62 节完整封存",
         "R0.70A–R0.73I：87 节已公开，63 节完整封存"),
        ('<span class="route-range">R0.69P–R0.73H</span>',
         '<span class="route-range">R0.69P–R0.73I</span>'),
        ('aria-label="R0.69P–R0.73H"', 'aria-label="R0.69P–R0.73I"'),
        ("展开 94 篇公开笔记", "展开 95 篇公开笔记"),
        ("本站 R0.69P–R0.73H 路线", "本站 R0.69P–R0.73I 路线"),
        ("综述 v1.48 · 2026-08-30", "综述 v1.49 · 2026-08-30"),
        ("上次综述 v1.47 · 2026-08-30", "上次综述 v1.48 · 2026-08-30"),
    ):
        html = required(html, old, new, "H home " + old)
    html = replace_all(
        html, "/recap-r0-61-r0-73h.html", "/recap-r0-61-r0-73i.html",
        "H home recap HTML links",
    )
    html = replace_all(
        html, "/recap-r0-61-r0-73h.pdf", "/recap-r0-61-r0-73i.pdf",
        "H home recap PDF links",
    )
    historical = (
        r'<strong style="color:var(--gold)">下一步 R0.73I：</strong>&nbsp;'
        r'建立选定增益 \(G_\Lambda\) 的匹配作用量。'
    )
    html = required(
        html, historical, historical.replace("下一步", "当时的下一步"),
        "H home historical next",
    )
    focus = r'<div class="summary-item"><strong>我目前关注</strong><span>R0.73I 已校正继承端点，并闭合连续体上作用量与零窗口切向速率。下一关在显式正窗口上认证唯一简单右端谱支；固定窗口 matching action、有界前因子、固定背景与横向三维仍为 OPEN。</span></div>'
    html = section(
        html,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        focus,
        "H home focus",
    )
    html = required(
        html,
        "<h3>R0.73H：按实际增益归一化的平面固定距离偏离已闭合</h3>",
        "<h3>R0.73I：端点校正、连续体上作用量与零窗口切向速率已闭合</h3>",
        "H home current title",
    )
    html = required(
        html, "<span>R0.72R–R0.73H：</span>", "<span>R0.72R–R0.73I：</span>",
        "H home path range",
    )
    html = required(
        html,
        "actual-gain-normalized planar fixed-distance departure</p>",
        "actual-gain-normalized planar fixed-distance departure → endpoint audit / continuum upper action / zero-window tangent</p>",
        "H home path tail",
    )
    link_h = '<a class="milestone" href="/notes/r0-73h.html">R0.73H</a>'
    html = once(
        html, link_h,
        link_h + '\n                  <a class="milestone" href="/notes/r0-73i.html">R0.73I</a>',
        "H home route link",
    )
    route_h = r'''              <p>R0.73H 用实际选定增益归一化初态，并以精确谐波选择律、倍频行连续数值横坐标界、Stieltjes 局部化和四阶余项闭合平面固定距离偏离。预设指数种子、固定背景、横向三维、奇性与 Clay 保持 OPEN。</p>
'''
    route_i = r'''              <p>R0.73I 证明继承端点严格小于 \(1/450\)，给完整移动传播子一个连续体上作用量，并证明完整顶谱块最小、最大增益共享零窗口切向速率。两个精确反例只否定由现有输入推出固定窗口作用量和有界前因子；有限 action/WKB 数据不承担连续体定理。</p>
'''
    html = once(html, route_h, route_h + route_i, "H home current route summary")
    html = section(
        html, r'            <article class="tree-node next">.*?</article>',
        HOME_NEXT, "H home next gate",
    )
    recap = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem"><p class="eyebrow">累计回顾 R0.61–R0.73I · 2026-08-30</p><h3>R0.60 recap 之后的累计回顾收录 125 个节点；全站现有 185 篇公开研究笔记</h3><p>累计回顾现分 44 个阶段，完整保留 R0.61–R0.73I；最新节点分开记录 continuum theorem、exact counterexample、finite diagnostic、文献边界和 open gate。</p><p>R0.70A–R0.73I 共 87 个版本已公开；63 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p><p><strong>阶段判断：</strong>&nbsp;继承端点、连续体上作用量与零窗口切向速率已闭合；固定正窗口的规范谱支、matching action、有界前因子、固定背景、横向三维、奇性与 Clay 保持 OPEN。</p><p><a href="/recap-r0-61-r0-73i.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-73i.pdf">下载同步 PDF</a></p></div>'''
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
    if html.count('data-release="r073i"') != 1:
        raise RuntimeError("home must contain exactly one R0.73I card")
    if html.count('<strong style="color:var(--gold)">下一步 R0.73J：') != 1:
        raise RuntimeError("home must contain exactly one current R0.73J gate")
    route = re.search(
        r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73I">(.*?)</nav>',
        html, flags=re.S,
    )
    links = [] if route is None else re.findall(
        r'href="/notes/r0-[^"]+\.html"', route.group(1)
    )
    if len(links) != 95 or len(set(links)) != 95:
        raise RuntimeError("home current-route index must contain 95 unique note links")
    assert_clean(html, "R0.73I home")
    assert_mathjax_clean(html, "R0.73I home", check_naked=True)
    assert_public_voice(html, "R0.73I home")
    return html


def update_literature() -> str:
    html = (PUBLIC / "literature-review.html").read_text(encoding="utf-8")
    for old, new in (
        ("/i18n-en.js?v=1.48", "/i18n-en.js?v=1.49"),
        ("本站 R0.69P–R0.73H 只列为研究笔记",
         "本站 R0.69P–R0.73I 只列为研究笔记"),
        ("文献综述 v1.48 · 2026-08-30", "文献综述 v1.49 · 2026-08-30"),
        ("累计回顾与 124 节索引", "累计回顾与 125 节索引"),
        ("打开 124 节完整索引", "打开 125 节完整索引"),
    ):
        html = required(html, old, new, "H literature " + old)
    html = replace_all(
        html, "/recap-r0-61-r0-73h.html", "/recap-r0-61-r0-73i.html",
        "H literature recap links",
    )
    deck_h = r'''<span class="route-r073h-deck-update">R0.73H 再以实际增益归一化和谐波能量局部化闭合 varying-background planar fixed-distance departure；\(d=0.01>1/450\) 仅属有限诊断，预设下界指数种子、固定背景 Lyapunov 不稳定、横向三维、奇性与 Clay 保持 OPEN。</span></p>'''
    deck_i = deck_h[:-4] + r'''<span class="route-r073i-deck-update">R0.73I 校正继承端点，给出连续体上作用量和零窗口切向速率；固定正窗口 matching action、有界前因子与连续体两项式仍为 OPEN。三个 \(N=48\) action/WKB 窗口只作有限诊断。</span></p>'''
    html = required(html, deck_h, deck_i, "H literature route deck I endpoint")
    old_open = r'''<div class="route-step pause"><header><b>开放接口 · R0.73I</b><strong>matching action for the selected gain</strong></header><p>为 \(G_\Lambda\) 建立匹配上、下作用量，判断 gain-normalized seed 能否改写为可预设的显式指数尺度。</p></div>'''
    new_steps = r'''<div class="route-step kept"><header><b>R0.73I</b><strong>endpoint audit, upper action, zero-window tangent</strong></header><p>继承端点严格小于 \(1/450\)；完整传播子有连续体一侧作用量；完整顶谱块的最小、最大增益共享零窗口切向速率。固定正窗口 matching action 和 bounded prefactor 未闭合。<a href="/notes/r0-73i.html">研究笔记</a> <a href="/recap-r0-61-r0-73i.html">当前累计回顾</a> <a href="#r073i-boundary">文献边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.73J</b><strong>unique simple rightmost continuum branch</strong></header><p>在显式正窗口上计数 Rayleigh/Evans 零点、证明简单性并排除更右谱点；随后再处理黏性谱支与非自伴绝热余项。</p></div>'''
    html = once(html, old_open, new_steps, "H literature route")
    boundary = r'''

          <h3 id="r073i-boundary">R0.73I 的选定增益作用量与绝热文献边界</h3>
          <p><a href="https://doi.org/10.1088/0305-4470/25/21/027">Nenciu--Rasche 1992</a>在两能级非自伴矩阵中给 least-dissipative branch 的绝热展开；<a href="https://arxiv.org/abs/math-ph/0607054">Abou Salem--Fröhlich 2007</a>、<a href="https://arxiv.org/abs/math-ph/0608059">Joye 2007</a>与<a href="https://arxiv.org/abs/1804.11213">Schmid 2019</a>分别给 common-domain closed generators、解析 gap evolution 与 Kato-stable families 的绝热框架。它们都把本题尚未证明的简单右端谱支、统一隔离、投影正则性和 complement evolution bound 作为假设，且不自动处理 \(B_\varepsilon=B_0-\varepsilon L\) 的双重奇异参数。</p>
          <p><a href="https://arxiv.org/abs/2509.18070">Colombo--Dolce--Montalto--Ventura 2025</a>给 stationary periodic long-wave 简单不稳定模态先例；<a href="https://arxiv.org/abs/2312.16938">Bian--Grenier 2023</a>给不同 half-space 几何中的 adjoint-selected rank-one term 与非正规余项；<a href="https://doi.org/10.1126/science.261.5121.578">Trefethen--Trefethen--Reddy--Driscoll 1993</a>说明谱图不能代替 transient-growth 控制。限定检索没有直接给出本题固定正窗口的 matching action 或 bounded-prefactor 两项式；这是本次检索的 non-collision 结论，不是原创性、优先权或不存在性声明。</p>
          <div class="boundary"><strong>R0.73I 的主张边界</strong><p>__CLOSED__。</p><p>__FALSE__。</p><p>__OPEN__。</p><p>有限 \(N=48\) action/WKB 吻合不证明连续体谱支、作用量或两项绝热展开。</p></div>'''
    boundary = boundary.replace("__CLOSED__", CLOSED).replace("__FALSE__", FALSE).replace("__OPEN__", OPEN)
    match = re.search(
        r'(<h3 id="r073h-boundary">.*?<div class="boundary">.*?</div>)',
        html, flags=re.S,
    )
    if match is None:
        raise RuntimeError("H literature expected R0.73H boundary")
    html = once(
        html, match.group(1), match.group(1) + boundary,
        "H literature boundary",
    )
    references = r'''            <li id="ref-139">G. Nenciu and G. Rasche. <a href="https://doi.org/10.1088/0305-4470/25/21/027"><em>On the adiabatic theorem for nonself-adjoint Hamiltonians</em></a>. Journal of Physics A 25 (1992), 5741--5751.</li>
            <li id="ref-140">W. K. Abou Salem and J. Fröhlich. <a href="https://doi.org/10.1007/s00220-007-0198-2"><em>Adiabatic Theorems for Quantum Resonances</em></a>. Communications in Mathematical Physics 273 (2007), 651--675; <a href="https://arxiv.org/abs/math-ph/0607054">author preprint</a>.</li>
            <li id="ref-141">A. Joye. <a href="https://doi.org/10.1007/s00220-007-0299-y"><em>General Adiabatic Evolution with a Gap Condition</em></a>. Communications in Mathematical Physics 275 (2007), 139--162; <a href="https://arxiv.org/abs/math-ph/0608059">author preprint</a>.</li>
            <li id="ref-142">J. Schmid. <a href="https://doi.org/10.1142/S0129055X19500144"><em>Adiabatic theorems for general linear operators with time-independent domains</em></a>. Reviews in Mathematical Physics 31 (2019), 1950014; <a href="https://arxiv.org/abs/1804.11213">author preprint</a>.</li>
            <li id="ref-143">M. Colombo, M. Dolce, R. Montalto and P. Ventura. <a href="https://arxiv.org/abs/2509.18070"><em>Long-wave instability of periodic shear flows for the 2D Navier--Stokes equations</em></a>. Preprint (2025).</li>
            <li id="ref-144">D. Bian and E. Grenier. <a href="https://arxiv.org/abs/2312.16938"><em>Asymptotic behaviour of solutions of linearized Navier Stokes equations in the long waves regime</em></a>. Preprint (2023).</li>
            <li id="ref-145">L. N. Trefethen, A. E. Trefethen, S. C. Reddy and T. A. Driscoll. <a href="https://doi.org/10.1126/science.261.5121.578"><em>Hydrodynamic Stability Without Eigenvalues</em></a>. Science 261 (1993), 578--584.</li>
'''
    html = once(
        html, '          </ol>\n          <p class="source-note">',
        references + '          </ol>\n          <p class="source-note">',
        "H literature references",
    )
    assert_clean(html, "R0.73I literature")
    assert_mathjax_clean(html, "R0.73I literature", check_naked=True)
    assert_public_voice(html, "R0.73I literature")
    return html


def build_manifest_outputs() -> dict[Path, bytes]:
    release_path = ROOT / "research/release-manifest.json"
    release = strict_json(release_path, "release manifest")
    for key, value in R073H_BASELINE.items():
        if release.get(key) != value:
            raise RuntimeError("release manifest changed during R0.73I generation: " + key)
    release.update({
        **R073I_TARGET,
        "latestReleaseGate": "tests/r073i-action-boundary-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r073i-release.test.mjs",
    })
    release.pop("nextReleaseSourceStage", None)

    site_path = PUBLIC / "site-version.json"
    site = strict_json(site_path, "site version")
    if site != {
        "schemaVersion": "research-site-version-v1",
        "version": "1.48",
        "latestRelease": "R0.73H",
        "publicHtmlNoteCount": 184,
        "publishedDate": "2026-08-30",
    }:
        raise RuntimeError("site-version changed during R0.73I generation")
    site.update({
        "version": "1.49",
        "latestRelease": "R0.73I",
        "publicHtmlNoteCount": 185,
        "publishedDate": "2026-08-30",
    })

    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = strict_json(inventory_path, "formal archive inventory")
    state = (
        inventory.get("latestPublishedRelease"), inventory.get("publishedReleaseCount"),
        inventory.get("formalSealedReleaseCount"), inventory.get("legacyFormalFigureBacklogCount"),
    )
    if state != ("r073h", 86, 62, 24):
        raise RuntimeError("formal archive changed during R0.73I generation")
    for key in ("publishedReleases", "formalSealedReleases"):
        rows = inventory.get(key)
        if not isinstance(rows, list) or rows[-1:] != ["r073h"] or "r073i" in rows:
            raise RuntimeError("formal archive is not append-only: " + key)
        rows.append("r073i")
    inventory.update({
        "latestPublishedRelease": "r073i",
        "publishedReleaseCount": 87,
        "formalSealedReleaseCount": 63,
        "legacyFormalFigureBacklogCount": 24,
    })
    if (
        len(inventory["publishedReleases"]) != 87
        or len(set(inventory["publishedReleases"])) != 87
        or len(inventory["formalSealedReleases"]) != 63
        or len(set(inventory["formalSealedReleases"])) != 63
    ):
        raise RuntimeError("formal archive count or uniqueness mismatch after R0.73I")
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
        ROOT / "VERSION": b"1.49\n",
    }


def build_note_index(site_payload: bytes) -> str:
    import generate_note_index as note_index

    existing = [note_index.parse_note(path) for path in note_index.note_files()]
    if len(existing) != 184 or any(note.slug == "r0-73i" for note in existing):
        raise RuntimeError("R0.73I note-index baseline is not exact")
    latest = note_index.Note(
        slug="r0-73i",
        code="R0.73I",
        title="Selected-gain action endpoint audit",
        major=73,
        has_pdf=True,
    )
    target_site = json.loads(site_payload.decode("utf-8"))
    old_json = note_index.json
    old_latest_recap_href = note_index.latest_recap_href

    class TargetJson:
        @staticmethod
        def loads(_payload: str) -> dict:
            return target_site

    try:
        note_index.json = TargetJson
        note_index.latest_recap_href = lambda: "/recap-r0-61-r0-73i.html"
        index = note_index.render([latest] + existing)
    finally:
        note_index.json = old_json
        note_index.latest_recap_href = old_latest_recap_href
    for token in (
        'data-site-version="1.49"',
        "185 篇公开研究笔记",
        "<strong>R0.73I</strong><span>最新研究节点</span>",
        'data-note="r0-73i"',
        "/recap-r0-61-r0-73i.html",
        "研究笔记总索引 · v1.49 · 2026-08-30",
    ):
        if token not in index:
            raise RuntimeError("R0.73I note index missing token: " + token)
    assert_clean(index, "R0.73I note index")
    assert_mathjax_clean(index, "R0.73I note index", check_naked=True)
    assert_public_voice(index, "R0.73I note index")
    return index


def stage_figure_assets(staged: dict[Path, bytes], figure_manifest: dict) -> None:
    source = ROOT / FIGURE_RELATIVE
    archive_target = PUBLIC / FIGURE_RELATIVE
    for name in FIGURE_PACKAGE_PATHS:
        staged[archive_target / name] = (source / name).read_bytes()

    outputs = figure_manifest.get("outputBindings", [])
    by_name = {
        str(row.get("path", "")): row for row in outputs
        if isinstance(row, dict)
    }
    web_target = PUBLIC / "assets/r073i"
    for suffix in ("pdf", "svg", "png"):
        name = f"figure.{suffix}"
        row = by_name.get(name)
        payload = (source / name).read_bytes()
        if (
            row is None
            or sha256_bytes(payload) != row.get("sha256")
            or len(payload) != row.get("bytes")
        ):
            raise RuntimeError("R0.73I public figure master is not manifest-bound: " + name)
        staged[web_target / f"{FIGURE_ID}.{suffix}"] = payload


def validate_staged(staged: dict[Path, bytes]) -> None:
    required_paths = (
        PUBLIC / "notes/r0-73i.html",
        PUBLIC / "recap-r0-61-r0-73i.html",
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
            raise RuntimeError("R0.73I transaction missing staged path " + str(path))
    for name in FIGURE_PACKAGE_PATHS:
        if PUBLIC / FIGURE_RELATIVE / name not in staged:
            raise RuntimeError("R0.73I transaction omitted figure-package asset " + name)
    for suffix in ("pdf", "svg", "png"):
        if PUBLIC / f"assets/r073i/{FIGURE_ID}.{suffix}" not in staged:
            raise RuntimeError("R0.73I transaction omitted web figure master " + suffix)
    for path in staged:
        if path.suffix.lower() == ".pdf" and (
            "assets/r073i" not in path.as_posix()
            and FIGURE_RELATIVE not in path.as_posix()
        ):
            raise RuntimeError("R0.73I HTML transaction must not generate note or recap PDFs")

    html_paths = (
        PUBLIC / "notes/r0-73i.html",
        PUBLIC / "recap-r0-61-r0-73i.html",
        PUBLIC / "research-review.html",
        PUBLIC / "literature-review.html",
        PUBLIC / "notes/index.html",
    )
    for path in html_paths:
        value = staged[path].decode("utf-8")
        assert_clean(value, path.name)
        assert_mathjax_clean(value, path.name, check_naked=True)
        assert_public_voice(value, path.name)
        if "/i18n-en.js?v=1.49" not in value:
            raise RuntimeError("R0.73I staged HTML has stale i18n version: " + path.name)
    note = staged[PUBLIC / "notes/r0-73i.html"].decode("utf-8")
    for token in (
        CLOSED, FALSE, OPEN, "NOT CLAY", "FALSE_AS_INFERENCE",
        "先固定窗口取", "三个窗口分开标记", "不证明连续体两项式",
    ):
        if token not in note:
            raise RuntimeError("R0.73I staged note lost boundary token: " + token)
    recap = staged[PUBLIC / "recap-r0-61-r0-73i.html"].decode("utf-8")
    start = recap.index('<section id="node-index">')
    end = recap.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', recap[start:end])
    if (
        len(links) != 125
        or len(set(links)) != 125
        or recap.count('<article class="phase">') != 44
    ):
        raise RuntimeError("R0.73I staged recap inventory is invalid")
    home = staged[PUBLIC / "research-review.html"].decode("utf-8")
    route = re.search(
        r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73I">(.*?)</nav>',
        home, flags=re.S,
    )
    route_links = [] if route is None else re.findall(
        r'href="/notes/(r0-[^"]+)\.html"', route.group(1)
    )
    if len(route_links) != 95 or len(set(route_links)) != 95:
        raise RuntimeError("R0.73I staged home route inventory is invalid")
    literature = staged[PUBLIC / "literature-review.html"].decode("utf-8")
    if (
        'class="route-r073i-deck-update"' not in literature
        or "没有直接给出本题固定正窗口的 matching action" not in literature
    ):
        raise RuntimeError("R0.73I staged literature route endpoint is invalid")
    site = json.loads(staged[PUBLIC / "site-version.json"])
    release = json.loads(staged[ROOT / "research/release-manifest.json"])
    inventory = json.loads(staged[ROOT / "research/formal-archive-inventory.json"])
    if (
        site.get("publicHtmlNoteCount") != 185
        or release.get("postR060RecapNodeCount") != 125
        or release.get("postR070APublishedReleaseCount") != 87
        or release.get("postR070AFormalSealedReleaseCount") != 63
        or release.get("legacyFormalFigureBacklogCount") != 24
        or inventory.get("publishedReleaseCount") != 87
        or inventory.get("formalSealedReleaseCount") != 63
    ):
        raise RuntimeError("R0.73I staged accounting drifted")


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
    descriptor, temporary = tempfile.mkstemp(prefix="." + path.name + ".r073i-", dir=path.parent)
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
        raise RuntimeError("R0.73I transaction is empty")
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
            raise RuntimeError("R0.73I materialized figure-package asset missing: " + name)
        if target.read_bytes() != (source / name).read_bytes():
            raise RuntimeError("R0.73I public figure-package asset is not byte-identical: " + name)
    rows = {
        str(row.get("path", "")): row
        for row in figure_manifest.get("outputBindings", [])
        if isinstance(row, dict)
    }
    for suffix in ("pdf", "svg", "png"):
        source_path = source / f"figure.{suffix}"
        target_path = PUBLIC / f"assets/r073i/{FIGURE_ID}.{suffix}"
        row = rows.get(f"figure.{suffix}")
        if row is None or not target_path.is_file() or target_path.is_symlink():
            raise RuntimeError("R0.73I materialized web figure missing: " + suffix)
        if target_path.read_bytes() != source_path.read_bytes():
            raise RuntimeError("R0.73I public web figure is not byte-identical: " + suffix)
        if digest(target_path) != row.get("sha256") or target_path.stat().st_size != row.get("bytes"):
            raise RuntimeError("R0.73I materialized web figure escaped manifest: " + suffix)


def publication_stage_incomplete() -> bool:
    pdfs = (
        PUBLIC / "notes/r0-73i.pdf",
        PUBLIC / "recap-r0-61-r0-73i.pdf",
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
            (ROOT / "scripts/i18n-snapshots/r073i-missing.json").read_text(encoding="utf-8")
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
        if isinstance(row, dict) and re.fullmatch(r"r073i\d{3}", str(row.get("id", "")))
    } if isinstance(translations, list) else {}
    if len(by_id) != len(snapshot):
        return True
    for index, snapshot_row in enumerate(snapshot, 1):
        row = by_id.get(f"r073i{index:03d}")
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
            "Validate or explicitly apply the staged R0.73I HTML/manifest transaction. "
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
        help="explicitly apply the HTML/manifest transaction from the exact R0.73H source",
    )
    args = parser.parse_args()
    if not args.check_only and not args.apply:
        parser.print_help()
        return

    release_state = preflight_release_state()
    _, figure_manifest = validate_inputs()
    if release_state == "target":
        verify_materialized_figure_assets(figure_manifest)
        print(json.dumps({
            "release": "R0.73I",
            "siteVersion": "1.49",
            "notes": 185,
            "recapNodes": 125,
            "published": 87,
            "formalSealed": 63,
            "legacyBacklog": 24,
            "phases": 44,
            "routeNotes": 95,
            "next": "R0.73J",
            "rootVersion": "1.49",
            "noOp": True,
            "publicationStageIncomplete": publication_stage_incomplete(),
            "pdfGenerated": False,
            "translationsGenerated": False,
        }, ensure_ascii=False))
        return

    staged: dict[Path, bytes] = {}
    stage_figure_assets(staged, figure_manifest)
    staged[PUBLIC / "notes/r0-73i.html"] = build_note().encode("utf-8")
    staged[PUBLIC / "recap-r0-61-r0-73i.html"] = build_recap().encode("utf-8")
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
            "release": "R0.73I",
            "sourceState": "R0.73H",
            "checkOnly": True,
            "wouldWrite": len(staged),
            "publicationStageIncomplete": True,
        }, ensure_ascii=False))
        return

    commit_transaction(staged)
    if len(list((PUBLIC / "notes").glob("r0-*.html"))) != 185:
        raise RuntimeError("R0.73I postcommit note count is not 185")
    verify_materialized_figure_assets(figure_manifest)
    print(json.dumps({
        "release": "R0.73I",
        "siteVersion": "1.49",
        "notes": 185,
        "recapNodes": 125,
        "published": 87,
        "formalSealed": 63,
        "legacyBacklog": 24,
        "phases": 44,
        "routeNotes": 95,
        "next": "R0.73J",
        "rootVersion": "1.49",
        "noOp": False,
        "publicationStageIncomplete": True,
        "pdfGenerated": False,
        "translationsGenerated": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
